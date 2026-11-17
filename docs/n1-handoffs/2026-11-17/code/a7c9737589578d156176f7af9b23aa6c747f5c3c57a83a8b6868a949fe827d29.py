"""Retain the actual final/checker and exact external-input closure repairs."""
import json
from pathlib import Path

from close_b134_v2 import CONFIGS, EXTERNAL, SOURCE, SOURCE_SHA
from common import WS, freeze_json, frozen, require, sha, write_frozen

ROOT = WS / "scratch-134" / "review"
LIFE = ROOT / "fresh-independent-002" / "lifecycle-011"
OUT = ROOT / "coordinator-final-repairs-retention-001"


def ref(path, expected=None):
    raw = frozen(path, expected)
    return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


def execution(name, expected_exit, reason):
    path = ROOT / name
    receipt_ref = ref(path / "receipt.json")
    receipt = json.loads(frozen(receipt_ref["path"], receipt_ref["sha256"]))
    require(receipt["exitCode"] == expected_exit
            and receipt["cleanupError"] is None and receipt["memory"]["breach"] is None,
            "Execution outcome changed: " + name)
    return {"receipt": receipt_ref, "log": ref(path / "output.log", receipt["logSha256"]),
            "exitCode": expected_exit, "disposition": reason, "rawExecutionRemainsLocal": True}


def main():
    require(not OUT.exists(), "Preserve existing retention")
    existing = ROOT / "claude-fresh003-adjudication-001" / "additional-evidence.json"
    evidence = json.loads(frozen(existing,
        "186510ed6e70e34e7971c60affd826f1a93b97c8c50720aa50b3d00d122f9917"))
    for item in evidence:
        frozen(item["path"], item["sha256"])
    repair = ROOT / "report-checker-repair-001"
    inventory = json.loads(frozen(repair / "inventory.json",
        "53a0ddc41da466ad426ef37da1e08674e6b34f4947ff28a9e234bb7c7c02f5c0"))
    for name, digest in inventory["files"].items():
        frozen(repair / name, digest)
    for name in ("test-checker-cli.py", "freeze-and-test-controller.py", "controller-routing.json"):
        evidence.append({"archivePath": "protocol/report-checker-repair/" + name,
                         **ref(repair / name, inventory["files"][name])})
    for name in ("close_b134_v2.py", "test_close_b134_v2.py"):
        captured = write_frozen(OUT / name, frozen(WS / "review-tools" / name))
        evidence.append({"archivePath": "protocol/" + name, **captured})
    proof = {
        "status": "BOUND_ACTUAL_REVIEW_AND_INFRASTRUCTURE_REPAIRS_NOT_CLOSURE",
        "candidate": "355cccb840d22e7313e79f234eb93d1367e00352",
        "unchangedConfigSha256": CONFIGS,
        "checker": {
            "scope": "D/E inline delimiters only; original path/range validation and F/O grammar unchanged. No report/config edits.",
            "inventory": ref(repair / "inventory.json"),
            "validation": ref(repair / "validation.json"),
            "tests": execution("report-checker-repair-test-001", 0,
                              "Six real-CLI controls pass, including original failure reproduction and strict invalid citation rejection."),
            "originalFailure": execution("claude-fresh003-final-execution-001", 1,
                                         "Original inline extractor rejected valid parenthesized D/E source references."),
            "successfulFinal": execution("claude-fresh003-final-repaired-001", 0,
                                         "Actual final passed with the unchanged full report and original NEEDS FIX verdict."),
        },
        "closureInputScope": {
            "originalAssembler": ref(SOURCE, SOURCE_SHA),
            "scope": "Only nineteen exact resolved path+supplied-hash producer inputs shared by both frozen config inventories supplement the original review reader. No blanket workspace or tools-directory access.",
            "pinnedExternalInputs": [ref(path, digest) for path, digest in sorted(EXTERNAL.items())],
            "originalFailure": execution("claude-fresh003-collector-execution-001", 1,
                                         "Original reader rejected already-pinned external tool files outside scratch-134/review."),
            "readControls": execution("closure-bound-input-controls-001", 0,
                                      "Initial five scope/hash controls pass; not evidence for the later entrypoint routing controls."),
            "finalControls": execution("closure-bound-input-controls-002", 0,
                                       "All seven controls pass, including mandatory archive retention and restoring the original reader on assembly failure."),
            "actualCollection": execution("claude-fresh003-collector-execution-002", 0,
                                          "The actual accepted Claude review passed the unchanged replacement collector and fresh claim-inventory check."),
        },
        "actualReview": {
            "final": ref(LIFE / "N1-B134-CLAUDE-FRESH-003-final.json"),
            "adjudication": ref(ROOT / "claude-fresh003-adjudication-001" / "adjudication.json"),
            "acceptance": ref(LIFE / "N1-B134-CLAUDE-FRESH-003-acceptance.json"),
            "collection": ref(ROOT / "claude-fresh003-collector-001" / "review-input.json"),
            "adjudicationExecution": execution("claude-fresh003-adjudication-execution-001", 0,
                                               "24 source/runtime checks and explicit F1/O1-O3 dispositions; no reviewer verdict rewriting."),
            "acceptanceExecution": execution("claude-fresh003-accept-execution-001", 0,
                                             "Review evidence accepted, not final closure or publication."),
        },
        "limits": [
            "Raw logs, full events and private captures remain local; archived code and hash bindings retain producer provenance.",
            "All original 29 claims and all consequential fresh claims still require final resolution.",
            "No GPT result, full two-family dry/real closure, signed integration or publication is asserted.",
        ],
    }
    bound = freeze_json(OUT / "provenance.json", proof)
    evidence.append({"archivePath": "verification/final-repairs-provenance.json", **bound})
    print(json.dumps({"evidence": freeze_json(OUT / "evidence.json", evidence),
                      "provenance": bound, "archiveRefs": len(evidence)}))


if __name__ == "__main__":
    main()
