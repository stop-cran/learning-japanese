"""Prepare isolated original-family followups on the independently verified S1 correction."""
import copy
import json
import re
import stat
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, write_frozen
from confirm_followup import build_followup
from confirm_v2 import clean
from prepare_b125_confirmations import REVIEWERS, additional, response_is_isolated, shared_is_neutral
from verify_b125_reconciliation_003 import COMPARISONS, INVENTORY_SHA, PARENT, PREFIX

CANDIDATE = "f2d2ddf87a0f1a721920241a88a61e28a98fa6f2"
PROOF_SHA = "b0429c6363d34443b3d7bc9e3d385c2b22d6c0ea40c8fc4a49f2306e15687ff5"
SCRATCH = WS / "scratch-125"
REVIEW = SCRATCH / "review"
INVENTORY_FIELDS = {"kanji", "title", "onyomi", "kunyomi", "quizOnyomi", "quizKunyomi", "tags", "sha256"}


def inventory_lines(value):
    require(value["parent"] == PARENT and value["count"] == len(value["cards"])
            and len({row["kanji"] for row in value["cards"]}) == value["count"],
            "Incomplete or duplicate source inventory")
    require(all(set(row) == INVENTORY_FIELDS for row in value["cards"]), "Unexpected inventory fields")
    rows = [{key: entry for key, entry in row.items() if key != "sha256"} for row in value["cards"]]
    raw = "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows).encode("utf-8")
    require([json.loads(line) for line in raw.decode().splitlines()] == rows, "Inventory derivative changed values")
    return raw


def capture_verified(path, digest):
    raw = path.read_bytes()
    require(sha(raw) == digest, f"Verified input changed before capture: {path}")
    path.chmod(stat.S_IREAD)
    frozen(path, digest)
    return raw


def main():
    config = load_batch(125)
    clean(config, CANDIDATE)
    proof = json.loads(frozen(REVIEW / "reconciliation-003-independent-proof.json", PROOF_SHA))
    require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE and proof["parent"] == PARENT
            and proof["reviewAccepted"] is False and proof["confirmationAccepted"] is False
            and proof["runtimeChanged"] == ["kanji/侵.md"], "Signed S1 verification is not applicable")
    neutral = REVIEW / "confirmation-002-neutral"
    require(not neutral.exists(), "Preserve existing followup inputs")
    summary = copy.deepcopy(proof)
    for key in ("responses", "changedFiles", "handoffSha256"):
        del summary[key]
    summary.update(status="PASS_MECHANICAL_ONLY", semanticAcceptance=False,
                   independentProofSha256=PROOF_SHA,
                   currentInventoryApplicability="Every non-target card is unchanged; the target title, tags and "
                   "all reading/practice fields are unchanged. The complete parent inventory therefore also "
                   "describes these fields on this signed successor. Exclusion lists are read from current cards.")
    path = neutral / "verification-summary.json"
    freeze_json(path, summary)
    shared = [additional(path, "verification/signed-s1-correction.json")]

    original_inventory = SCRATCH / "reconciliation-003-inventory-002" / "card-inventory.json"
    inventory_raw = capture_verified(original_inventory, INVENTORY_SHA)
    inventory = json.loads(inventory_raw)
    require(inventory["count"] == proof["parentInventoryCards"] == 1245, "Inventory coverage differs")
    derivative_path = neutral / "complete-title-reading-inventory.txt"
    derivative = write_frozen(derivative_path, inventory_lines(inventory))
    derivative_receipt = neutral / "inventory-derivative.json"
    freeze_json(derivative_receipt, {
        "parent": PARENT, "currentCandidate": CANDIDATE, "cards": 1245,
        "source": {"path": str(original_inventory), "sha256": INVENTORY_SHA},
        "output": derivative, "omittedFields": ["/cards/*/sha256"],
        "representation": "One compact JSON object per line, preserving source row order and every title, "
                          "on/kun list, explicit practice list and tag. Null and empty arrays remain distinct. "
                          "Only per-card hash fields are omitted; the independently verified complete "
                          "original, with those hashes, remains local.",
    })
    shared += [additional(derivative_receipt, "evidence/inventory-derivative.json"),
               additional(derivative_path, "evidence/complete-title-reading-inventory.txt")]

    bindings = proof["gateSets"]["committed"]
    directory = SCRATCH / bindings["directory"]
    capture_verified(directory / "summary.json", bindings["summary"])
    shared.append(additional(directory / "summary.json", "committed-checks/summary.json"))
    for row in proof["gates"]["committed"]:
        name = row["gate"]
        capture_verified(directory / f"{name}.json", row["receiptSha256"])
        capture_verified(directory / f"{name}.log", row["logSha256"])
        shared.append(additional(directory / f"{name}.log", f"committed-checks/{name}.log"))
    require({row["gate"] for row in proof["gates"]["committed"]} == set(CHECKS), "Committed gate set differs")
    for name, bindings in proof["evidenceReceipts"].items():
        receipt_path = SCRATCH / name
        capture_verified(receipt_path, bindings["receiptSha256"])
        capture_verified(receipt_path.with_suffix(".log"), bindings["logSha256"])
        if name.endswith("reading.json"):
            shared += [additional(receipt_path, "evidence/explicit-reading-command.json"),
                       additional(receipt_path.with_suffix(".log"), "evidence/explicit-reading-model.log")]

    old_neutral = REVIEW / "confirmation-001-neutral"
    derivatives = json.loads(frozen(old_neutral / "capture-derivatives.json"))
    shin = next(row for row in derivatives["captures"] if row["character"] == "侵")
    original = frozen(Path(shin["original"]["path"]), shin["original"]["sha256"])
    derivative = frozen(Path(shin["derivative"]["path"]), shin["derivative"]["sha256"])
    require(derivative == original + b"\n", "Full source capture derivative differs")
    capture_receipt = neutral / "source-capture-derivative.json"
    freeze_json(capture_receipt, {
        "candidate": CANDIDATE, "capture": shin,
        "transformation": "Reused complete original response plus exactly one LF; remove the last byte "
                          "to restore the original. No new fetch and no source-content edits.",
        "retention": "Complete external capture and all mixed chain segments containing it remain local.",
    })
    shared += [additional(capture_receipt, "evidence/source-capture-derivative.json"),
               additional(Path(shin["derivative"]["path"]),
                          "evidence/external-snapshots/reconciliation-003/shin-response-plus-lf.html")]
    revised = ["kanji/侵.md", "words/侵入.md", "words/低い.md", "words/短い.md",
               *(f"kanji/{char}.md" for char in sorted(COMPARISONS)),
               "docs/n1-sources/batch-125/kanjidic2-selected-records.xml",
               *(PREFIX + name for name in ("disposition.md", "source-receipt.json",
                                            "kanjidic2-records.xml", "jmdict-records.xml"))]
    blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
    for raw in [*(blob(path) for path in revised), *(frozen(item["path"]) for item in shared)]:
        require(shared_is_neutral(raw), "Cross-review material in neutral inputs")
    prepared = []
    for family, (session, initial_run, initial_sha) in REVIEWERS.items():
        run = f"N1-B125-{family.upper()}-CONFIRM-002"
        prior_path = REVIEW / "confirm" / f"N1-B125-{family.upper()}-CONFIRM-001-acceptance.json"
        prior_raw = frozen(prior_path)
        prior = json.loads(prior_raw)
        expected_verdict = "CONFIRMED" if family == "claude" else "UNVERIFIED"
        require(prior["candidate"] == PARENT and prior["verdict"] == expected_verdict
                and prior["confirmationAccepted"] is (family == "claude")
                and prior["openClaimIds"] == ([] if family == "claude" else ["S1"]),
                "Earlier snapshot acceptance or hold changed")
        response = blob(PREFIX + f"{family}-response-003.md")
        require(sha(response) == proof["responses"][family] and response_is_isolated(family, response),
                "Family response changed")
        response_path = neutral / f"response-{family}.md"
        write_frozen(response_path, response)
        spec = {
            "batch": 125, "run": run, "family": family, "candidate": CANDIDATE, "session": session,
            "acceptance": {"path": str(REVIEW / f"{initial_run}-acceptance.json"), "sha256": initial_sha},
            "prior": {"path": str(prior_path), "sha256": sha(prior_raw)},
            "basis": "accepted-confirmation" if family == "claude" else "held-confirmation",
            "priorVerdict": expected_verdict, "openClaimIds": prior["openClaimIds"],
            "revisedSources": revised, "originalSources": [],
            "additionalSources": [additional(response_path, "author-response/current.md"), *shared],
        }
        spec_path = REVIEW / "confirm" / f"{run}-spec.json"
        freeze_json(spec_path, spec)
        build_followup(spec_path)
        prepared.append(run)
    freeze_json(REVIEW / "confirmation-002-preparation.json", {
        "candidate": CANDIDATE, "parent": PARENT, "proofSha256": PROOF_SHA, "runs": prepared,
        "runtimeDelta": True, "evidenceOnlyAdapterUsed": False, "reviewersLaunched": False,
        "limits": "Neutral source/host evidence and family-isolated responses prepared; substantive "
                  "original-reviewer confirmation and publication remain pending.",
    })


if __name__ == "__main__":
    main()
