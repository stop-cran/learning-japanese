"""Build family-isolated confirmations for the verified signed B128 successor.

Full mode:      prepare_b128_confirmations.py CANDIDATE PROOF_SHA
Staged dry run: prepare_b128_confirmations.py --staged-dry-run OUTPUT_JSON
"""
import copy
import json
import re
import sys
from pathlib import Path

from common import (freeze_json, frozen, git, json_bytes, load_batch, require, sha, start_guard,
                    verify_packet, write_frozen)
from confirm_b127 import build, clean
from finalize_b128 import check_proof
from verify_b128_reconciliation import (ADDED_GUARDS, CARD, DISTRACTORS, FAMILY, GATES, MEMBER,
                                        NEW_LEDGER, NOTES, OLD_GUARDS, ORIGINAL, OTHERS, PARENT, PREFIX,
                                        REVIEW)

TOOLING_SHA = "82523e34974a05eef8804faa65c8395243d4966d9656a5b5057e4805a5f14f95"
REVIEWERS = {
    "claude": ("1f199715-ebef-41e0-9e84-fda61248555f",
               "de03c659e4b10ce4d567d2ad816084241ff4f4b1136893e3e7b0989dc0482832", "response-a.md", {}),
    "gpt": ("40f6292a-b52f-4d9a-ac86-25bbc5cad512",
            "90783d34d9e4d5263bc510cf5a47d8fa1c0af14ad5125d110c397fad225c3a2d", "response-b.md",
            {"basis": "adjudicated-initial", "priorVerdict": "UNVERIFIED"}),
}
INITIAL_VERDICTS = {"claude": "NEEDS FIX", "gpt": "UNVERIFIED"}
# Verdicts are uppercase enums; ordinary prose such as "not a clean opposite" stays shareable.
VERDICTS = re.compile(r"\bCLEAN\b|NEEDS FIX|\bCONFIRMED\b|\bUNVERIFIED\b")
REVISED = [CARD, f"words/{MEMBER}.md", NEW_LEDGER]
REVISED += [f"kanji/{char}.md" for char in sorted(set(OTHERS) | set(OLD_GUARDS) | set(DISTRACTORS))]
REVISED += [ORIGINAL + name for name in ("jmdict-selected-records.xml", "kanjidic2-selected-records.xml")]
REVISED += [PREFIX + name for name in (
    "pair-dispositions.json", "jmdict-complete-records.xml", "kanjidic2-complete-records.xml",
    "source-notes.json", "selector-membership.json", "source-verification-002.json", "source-receipt.json",
    "summary.md")]
ORIGINALS = [f"evidence/external-snapshots/{i:02d}-extract.txt" for i in range(1, 4)]
ORIGINALS += ["evidence/external-snapshots/manifest.json"]
NOTES_HEADING = "+### Batch 128: bounded reconciliation"
NEUTRAL = REVIEW / "confirmation-001-neutral"


def shared_is_neutral(raw):
    text = raw.decode("utf-8")
    return not (any(pattern.search(text) for pattern in FAMILY.values()) or VERDICTS.search(text))


def response_is_isolated(family, raw):
    text = raw.decode("utf-8")
    return {name for name, pattern in FAMILY.items() if pattern.search(text)} == {family}


def neutral_receipt(receipt):
    result = copy.deepcopy(receipt)
    del result["admissionBindings"]
    result["derivation"] = {
        "originalSignedPath": PREFIX + "source-receipt-002.json",
        "originalSha256": sha(json_bytes(receipt)),
        "onlyOmittedTopLevelKey": "admissionBindings",
        "reason": "Contains family-specific report/adjudication identities. Selector membership, complete "
                  "records, verification bindings and record counts are unchanged.",
    }
    return result


def notes_delta(raw):
    text = raw.decode("utf-8")
    added = [line for line in text.splitlines() if line.startswith("+") and not line.startswith("+++")]
    removed = [line for line in text.splitlines() if line.startswith("-") and not line.startswith("---")]
    hunks = [line for line in text.splitlines() if line.startswith("@@")]
    require(added and added[0] == NOTES_HEADING and not removed and len(hunks) == 1,
            "Authoring-notes delta is not the single B128 insertion")
    return raw


def additional(path, source):
    return {"path": str(path), "source": source, "sha256": sha(frozen(path))}


def collect(blob, notes_raw, responses_expected=None):
    """Return shared derivatives and per-family responses after neutrality checks."""
    receipt_raw = blob(PREFIX + "source-receipt-002.json")
    receipt = json.loads(receipt_raw)
    require(receipt_raw == json_bytes(receipt), "Source receipt serialization differs")
    neutral_source = neutral_receipt(receipt)
    require({key: value for key, value in neutral_source.items() if key != "derivation"}
            == {key: value for key, value in receipt.items() if key != "admissionBindings"},
            "Neutral derivative changed source evidence")
    responses = {}
    for family, (_, _, name, _) in REVIEWERS.items():
        raw = blob(PREFIX + name)
        require(response_is_isolated(family, raw), f"Family response leaked: {family}")
        require(responses_expected is None or responses_expected[name] == sha(raw),
                f"Family response changed: {family}")
        responses[family] = raw
    for path in REVISED:
        require(shared_is_neutral(blob(path)), f"Family provenance in shared input: {path}")
    notes_delta(notes_raw)
    require(shared_is_neutral(notes_raw) and shared_is_neutral(json_bytes(neutral_source)),
            "Notes delta or neutral source receipt leaks review provenance")
    return {"receiptRaw": receipt_raw, "neutralSource": neutral_source, "responses": responses}


def check_reviewers(config):
    for family, (session, acceptance_sha, _, _) in REVIEWERS.items():
        initial = f"N1-B128-{family.upper()}-001"
        accepted = json.loads(frozen(REVIEW / f"{initial}-acceptance.json", acceptance_sha))
        launch = json.loads(frozen(REVIEW / f"{initial}-launch.json"))
        require(accepted["run"] == initial and accepted["reviewAccepted"] is True
                and accepted["verdict"] == INITIAL_VERDICTS[family]
                and accepted["candidate"] == config["candidate"] and launch["session"] == session,
                f"Original review is not accepted: {family}")
        frozen(Path(accepted["report"]["path"]), accepted["report"]["sha256"])
        require(not (REVIEW / "confirm" / f"N1-B128-{family.upper()}-CONFIRM-001-spec.json").exists(),
                f"Confirmation already prepared: {family}")


def check_tooling():
    tooling = json.loads(frozen(REVIEW / "confirm" / "tooling-preflight.json", TOOLING_SHA))
    require(tooling["batch"] == 128 and tooling["status"] == "PASS_PREPARATION_ONLY"
            and tooling["exitCode"] == 0, "Confirmation tooling is not ready")
    for item in tooling["derivations"]:
        frozen(item["output"]["path"], item["output"]["sha256"])
    for field in ("output", "helper"):
        item = tooling["engineDerivation"][field]
        frozen(item["path"], item["sha256"])


def notes_diff(config, *revisions):
    return git(config, "diff", "--no-color", "-U0", *revisions, "--", NOTES)


def check_gate_files(directory, summary_sha, rows):
    files = [(directory / "summary.json", summary_sha, "committed-checks/summary.json")]
    require(set(rows) == set(GATES), "Committed gate set differs")
    files += [(directory / f"{name}.log", rows[name], f"committed-checks/{name}.log") for name in GATES]
    shared = []
    for path, digest, source in files:
        require(shared_is_neutral(frozen(path, digest)), f"Shared input leaks: {source}")
        shared.append(additional(path, source))
    return shared


def dry_run(output):
    config = load_batch(128)
    guard, _ = start_guard("B128 staged confirmation dry run")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == PARENT, "Dry run needs the staged parent")
        blob = lambda path: git(config, "show", f":{path}")
        check_tooling()
        check_reviewers(config)
        _, sums, _ = verify_packet(config, guard)
        require(all(path in sums for path in ORIGINALS), "Unbound original source")
        collected = collect(blob, notes_diff(config, "--cached", PARENT))
        guard.check()
        author = REVIEW.parent / "reconciliation-author-gates-001"
        summary_raw = frozen(author / "summary.json")
        logs = json.loads(summary_raw)["logs"]
        for path in [author / "summary.json", *(author / f"{name}.log" for name in GATES)]:
            require(shared_is_neutral(frozen(path)), f"Author gate proxy leaks: {path.name}")
        require(not NEUTRAL.exists(), "Neutral confirmation inputs already exist")
        result = {
            "batch": 128, "status": "PASS_STAGED_DRY_RUN_ONLY", "head": PARENT,
            "revisedSources": len(REVISED), "originalSources": ORIGINALS,
            "responses": {family: sha(raw) for family, raw in collected["responses"].items()},
            "neutralReceiptSha256": sha(json_bytes(collected["neutralSource"])),
            "authorGateProxy": {"summarySha256": sha(summary_raw), "logs": len(logs)},
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Pre-signing staged-index dry run. No spec, chain, prompt or neutral input was written; "
                      "committed gate logs are checked only after signing.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Confirmation dry run RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(Path(output), result)))


def main(candidate, proof_sha):
    config = load_batch(128)
    guard, _ = start_guard("B128 isolated confirmation preparation")
    try:
        clean(config, candidate)
        proof = json.loads(frozen(REVIEW / "reconciliation-001-independent-proof.json", proof_sha))
        check_proof(proof, candidate, config)
        require(proof["openUnguardedClaims"] == [] and proof["addedDirectGuards"] == ADDED_GUARDS,
                "Proof scope differs")
        check_tooling()
        check_reviewers(config)
        blob = lambda path: git(config, "show", f"{candidate}:{path}")
        collected = collect(blob, notes_diff(config, PARENT, candidate), proof["responses"])
        require(sha(collected["receiptRaw"]) == proof["sourceReceiptSha256"], "Source receipt differs from proof")
        guard.check()
        summary = {key: proof[key] for key in (
            "batch", "candidate", "parent", "base", "signature", "runtimeChanged", "runtimeEntries",
            "manifestSha256", "contentVersion", "sourceReceiptSha256", "dispositionsSha256", "sources",
            "gateSets", "preservation", "addedDirectGuards", "totalDirectGuards", "conservativeGuardIds",
            "openUnguardedClaims")}
        summary.update(
            status="PASS_MECHANICAL_ONLY", sourceProofSha256=proof_sha, semanticAcceptance=False,
            limits="Signed bytes, complete dictionary selections and host gates only. The finite "
                   "author dispositions require independent evaluation; conservative guards retain "
                   "linguistic uncertainty. No native/device, arbitrary-pool or publication acceptance.")
        require(shared_is_neutral(json_bytes(summary)), "Neutral summary leaks review provenance")
        committed = proof["gateSets"]["committed"]
        directory = Path(committed["directory"])
        rows = {row["gate"]: row["logSha256"] for row in committed["gates"]}
        require(not NEUTRAL.exists(), "Preserve existing neutral inputs")
        summary_path, receipt_path = NEUTRAL / "verification-summary.json", NEUTRAL / "source-receipt.json"
        notes_path = NEUTRAL / "authoring-notes-delta.patch"
        freeze_json(summary_path, summary)
        freeze_json(receipt_path, collected["neutralSource"])
        write_frozen(notes_path, notes_delta(notes_diff(config, PARENT, candidate)))
        shared = [additional(summary_path, "verification/signed-correction-summary.json"),
                  additional(receipt_path, "evidence/reconciliation/source-receipt.json"),
                  additional(notes_path, "diffs/authoring-notes.patch"),
                  *check_gate_files(directory, committed["summarySha256"], rows)]
        prepared = []
        for family, (session, acceptance_sha, _, basis) in REVIEWERS.items():
            initial = f"N1-B128-{family.upper()}-001"
            run = f"N1-B128-{family.upper()}-CONFIRM-001"
            acceptance_path = REVIEW / f"{initial}-acceptance.json"
            response_path = NEUTRAL / f"response-{family}.md"
            write_frozen(response_path, collected["responses"][family])
            spec = {
                "batch": 128, "run": run, "family": family, "candidate": candidate, "session": session,
                **basis, "acceptance": {"path": str(acceptance_path), "sha256": acceptance_sha},
                "revisedSources": REVISED, "originalSources": ORIGINALS,
                "additionalSources": [additional(response_path, "author-response/current.md"), *shared],
            }
            path = REVIEW / "confirm" / f"{run}-spec.json"
            freeze_json(path, spec)
            build(path)
            prepared.append(run)
            guard.check()
        result = {
            "batch": 128, "candidate": candidate, "runsPrepared": prepared, "verificationSha256": proof_sha,
            "neutralReceiptSha256": sha(json_bytes(collected["neutralSource"])),
            "implementedDirectPairs": ADDED_GUARDS, "unguardedOpenFinitePairs": [],
            "gptBasis": REVIEWERS["gpt"][3], "reviewersLaunched": False,
            "isolation": "Only the owning family's unchanged report and response are present in its "
                         "chain. Shared evidence is neutral; the complete source receipt is preserved "
                         "signed, with only admissionBindings omitted in the derivative.",
            "limits": "Readiness only, not semantic or publication acceptance. External extracts and "
                      "mixed read-chain segments remain local.",
            "producerSha256": sha(Path(__file__).read_bytes()),
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Confirmation preparation RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(REVIEW / "confirmation-001-preparation.json", result)))


if __name__ == "__main__":
    if sys.argv[1:2] == ["--staged-dry-run"] and len(sys.argv) == 3:
        dry_run(sys.argv[2])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        raise SystemExit(__doc__)
