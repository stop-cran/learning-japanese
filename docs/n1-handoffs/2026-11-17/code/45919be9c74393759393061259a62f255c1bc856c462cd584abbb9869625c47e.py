"""Closure-history checks for fresh B134 reviews, not execution or teaching approval.

The caller must first collect and adjudicate each actual review with its frozen
controller. These checks prevent that later archive from erasing the original
claims or relabelling fresh independent reviews as original confirmations.
"""
import json
import re
import sys
from pathlib import Path

from b132_closure_records import SHA256, UUID, archive_path
from b134_initial_records import INITIALS, actual_initial, disposition_ids
from common import WS, freeze_json, frozen, require, sha, start_guard
from run_b134_closure_checks import BASE, BATCH, CANDIDATE, MEMBERS

FAILED_SESSION = "73081d97-2224-47e3-a8de-113e7dd1d7a2"
REJECTION_SHA = "a895cbbcbcdddf072e6142722c52e71e87bc8331714f9929f734b1197759585b"
CAPACITY_SHA = "64d870d60c3fb68c060b208a9e751b6d4ea2c277c19e91012ea2c0b82ca4ba19"
MODE = "fresh-independent-reviews-plus-coordinator-reconciliation"
REVIEW_REFS = ("report", "final", "acceptance", "adjudication", "context", "structure")


def bound(ref, inventory, original_sha=None):
    archive_path(ref["path"])
    require(isinstance(ref["sha256"], str) and SHA256.fullmatch(ref["sha256"])
            and inventory.get(ref["path"]) == ref["sha256"], "Unbound review-history evidence")
    if original_sha is not None:
        require(ref.get("originalSha256", ref["sha256"]) == original_sha,
                "Historical evidence lost its original binding")


def validate_history(closure, reviewed):
    """Validate identities and retained history after the execution collectors pass."""
    require(isinstance(reviewed, str) and re.fullmatch(r"[0-9a-f]{40}", reviewed)
            and reviewed != CANDIDATE
            and closure["batch"] == BATCH and closure["base"] == BASE
            and closure["members"] == MEMBERS and closure["initialSnapshot"] == CANDIDATE
            and closure["reviewedSnapshot"] == reviewed and closure["publication"] == "PENDING"
            and closure["reviewMode"] == MODE
            and closure["originalReviewerConfirmation"] is False,
            "Wrong snapshot or misleading replacement-review attribution")
    entries, inventory = closure["reviewLineage"], closure["recordedFileSha256"]
    require(isinstance(entries, list) and len(entries) == 4, "Expected two original and two fresh reviews")
    by_run = {entry["run"]: entry for entry in entries}
    require(len(by_run) == len(entries), "Duplicate accepted review run")
    originals = [entry for entry in entries if entry["role"] == "initial"]
    require(len(originals) == 2 and {entry["family"] for entry in originals} == set(INITIALS),
            "Original review history is incomplete")
    for entry in originals:
        known = INITIALS[entry["family"]]
        require(entry["session"] == known["session"] and entry["snapshot"] == CANDIDATE
                and entry["run"] == "N1-B134-" + entry["family"].upper() + "-001"
                and entry["verdict"] == known["verdict"] and entry["reviewAccepted"] is True,
                "Original identity, verdict or evidence acceptance was rewritten")
        for field in ("acceptance", "final"):
            bound(entry[field], inventory, known[field])
    runs = closure["finalRuns"]
    require(isinstance(runs, list) and len(runs) == 2 and len(set(runs)) == 2
            and all(run in by_run for run in runs), "Two distinct fresh final runs are required")
    finals = [by_run[run] for run in runs]
    require({entry["family"] for entry in finals} == set(INITIALS)
            and len({entry["session"] for entry in entries}) == 4,
            "Fresh reviews must have distinct same-family successors")
    excluded = {FAILED_SESSION, *(known["session"] for known in INITIALS.values())}
    for entry in finals:
        family = entry["family"]
        require(entry["role"] == "replacement-independent" and UUID.fullmatch(entry["session"])
                and entry["session"] not in excluded
                and entry["snapshot"] == reviewed and entry["reviewAccepted"] is True
                and entry["verdict"] in ("CLEAN", "NEEDS FIX", "UNVERIFIED")
                and "confirmation" not in entry
                and entry["originalSession"] == INITIALS[family]["session"]
                and entry["replacesInitialRun"] == "N1-B134-" + family.upper() + "-001"
                and entry["originalReviewerConfirmation"] is False,
                "Fresh review identity is substituted or relabelled as confirmation")
    for entry in entries:
        for field in REVIEW_REFS:
            bound(entry[field], inventory)
    held = closure["replacementBasis"]
    require(held["reason"] == "original-reviewer-context-capacity"
            and held["status"] == "HOLD" and held["reviewAccepted"] is False,
            "Capacity hold cannot count as a review")
    bound(held["measurement"], inventory, CAPACITY_SHA)
    rejected = closure["nonAcceptedReviews"]
    require(isinstance(rejected, list) and len(rejected) == 1
            and rejected[0]["session"] == FAILED_SESSION
            and rejected[0]["status"] == "REJECTED_PREPARATION_AND_LAUNCH_NOT_CARD_VERDICT"
            and rejected[0]["reviewAccepted"] is False
            and rejected[0]["reportPresent"] is False
            and "verdict" not in rejected[0] and "confirmation" not in rejected[0],
            "Rejected preparation was lost or promoted to a teaching verdict")
    bound(rejected[0]["rejection"], inventory, REJECTION_SHA)


def validate_resolution(resolution, closure, reviewed, original_claims):
    """Require evidence-bound decisions for every original and fresh review claim.

    original_claims comes from collect_initial_record and includes each unchanged
    raw report. A CLEAN fresh review cannot silently replace those obligations.
    """
    validate_history(closure, reviewed)
    require(set(original_claims) == set(INITIALS), "Both collected original claim sets are required")
    entries = closure["reviewLineage"]
    by_run = {entry["run"]: entry for entry in entries}
    expected = {entry["run"]: entry["adjudication"]["sha256"] for entry in entries}
    require(resolution["batch"] == BATCH and resolution["initialSnapshot"] == CANDIDATE
            and resolution["reviewedSnapshot"] == reviewed
            and resolution["mode"] == MODE
            and resolution["originalReviewerConfirmation"] is False
            and resolution["adjudicationSha256"] == expected
            and resolution["remainingActionableFindings"] == []
            and resolution["remainingConsequentialClaims"] == [],
            "Resolution is unbound or has outstanding work")
    required = set()
    for family, value in original_claims.items():
        run = "N1-B134-" + family.upper() + "-001"
        require(value["reportSha256"] == by_run[run]["report"].get(
            "originalSha256", by_run[run]["report"]["sha256"]),
            "Original claim inventory describes another report")
        require(sha(value["report"]) == value["reportSha256"], "Original report bytes changed")
        require(all(value["claims"][field] == by_run[run][field] for field in
                    ("acceptedFindings", "openClaimIds", "coordinatorClaimIds")),
                "Original claim inventory differs from the collected lineage")
        required.update((run, claim) for claim in disposition_ids(value["report"], value["claims"]))
    for run in closure["finalRuns"]:
        entry = by_run[run]
        for field in ("acceptedFindings", "openClaimIds", "coordinatorClaimIds"):
            values = entry[field]
            require(isinstance(values, list) and all(isinstance(item, str) and item for item in values)
                    and len(values) == len(set(values)), "Fresh claim inventory is incomplete")
            required.update((run, claim) for claim in values)
    dispositions = resolution["dispositions"]
    require(isinstance(dispositions, list), "Missing claim dispositions")
    actual = set()
    for item in dispositions:
        identity = (item["run"], item["id"])
        require(identity in required and identity not in actual,
                "Unexpected or duplicate resolution identity")
        require(item["status"] in ("resolved", "withdrawn", "optional")
                and isinstance(item["reason"], str) and item["reason"].strip()
                and isinstance(item["evidence"], list) and item["evidence"],
                "Unresolved or unsupported claim disposition")
        for ref in item["evidence"]:
            bound(ref, closure["recordedFileSha256"])
        actual.add(identity)
    require(actual == required, "An original or fresh review claim lacks a disposition")


def main(output):
    root = WS / "scratch-134" / "review"
    require(output.parent == root and not output.exists(), "Use a new direct review output directory")
    guard, _ = start_guard("B134 replacement history preparation")
    try:
        collected = {}
        for family in INITIALS:
            spec, refs, _, claims = actual_initial(family)
            report = frozen(refs["report"]["path"], refs["report"]["sha256"])
            collected[family] = {
                "spec": spec, "refs": refs, "claims": claims,
                "requiredDispositionIds": disposition_ids(report, claims),
            }
            guard.check()
        history = {}
        for name, relative, expected in (
            ("capacity", "confirmation-capacity-fallback-001/measurement.json", CAPACITY_SHA),
            ("rejection", "fresh-independent-001-rejection/rejection.json", REJECTION_SHA),
        ):
            path = root / relative
            history[name] = {"path": str(path), "sha256": expected}
            value = json.loads(frozen(path, expected))
            if name == "capacity":
                require(value["status"] == "HOLD" and value["startupGate"] == 700000
                        and value["projectedPeak"] > value["startupGate"], "Capacity hold differs")
            else:
                require(value["status"] == "REJECTED_PREPARATION_AND_LAUNCH_NOT_CARD_VERDICT"
                        and value["session"] == FAILED_SESSION and value["reportExists"] is False,
                        "Rejected-run evidence differs")
                events = value["eventSnapshot"]
                require(len(frozen(events["path"], events["sha256"])) == events["bytes"],
                        "Rejected event snapshot differs")
            guard.check()
        result = {
            "status": "PREPARED_NOT_REVIEW_CLOSURE", "batch": BATCH,
            "initialSnapshot": CANDIDATE, "reviewMode": MODE,
            "originalReviewerConfirmation": False, "originals": collected, "history": history,
            "producerSha256": sha(frozen(Path(__file__))),
            "limits": "Original claim obligations and rejected/held history only. No replacement "
                      "review admitted or accepted, no claim resolved, no publication authorized.",
        }
    finally:
        memory = guard.finish()
        require(not memory["breach"], "History preparation RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(output / "index.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "b134_review_history.py NEW_OUTPUT_DIRECTORY")
    main(Path(sys.argv[1]).resolve())
