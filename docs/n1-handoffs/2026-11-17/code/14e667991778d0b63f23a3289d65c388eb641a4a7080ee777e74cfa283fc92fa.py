"""Bind the import-only repair and preserved failures for the final closure."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha

ROOT = WS / "scratch-134" / "review"
LIFE = ROOT / "fresh-independent-002" / "lifecycle-011"
REPAIR = ROOT / "lifecycle-runtime-repair-001"
OUT = ROOT / "coordinator-runtime-repair-retention-001"


def ref(path, expected=None):
    raw = frozen(path, expected)
    return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


def execution(name, expected_exit, cause):
    path = ROOT / name
    receipt_ref = ref(path / "receipt.json")
    receipt = json.loads(frozen(receipt_ref["path"], receipt_ref["sha256"]))
    require(receipt["exitCode"] == expected_exit
            and receipt["cleanupError"] is None
            and receipt["memory"]["breach"] is None, "Execution status changed: " + name)
    return {
        "receipt": receipt_ref,
        "log": ref(path / "output.log", receipt["logSha256"]),
        "exitCode": expected_exit,
        "disposition": cause,
        "rawExecutionRemainsLocal": True,
    }


def main():
    require(not OUT.exists(), "Preserve existing retention output")
    sources = (
        ("original-auditor.py", LIFE / "protocol-014" / "audit-review-b134-014.py",
         "1fbc57b7f26cfbf099de828dbeb9b34d643a643262b5fa1b2c42329bedde81f6"),
        ("original-controller.py", LIFE / "protocol-014" / "step-b134-014.py",
         "940638df7a5ef763f2e5b932115bb447d85129577d3a0770b72138f6baa605df"),
        ("audit-entry.py", REPAIR / "audit-entry.py",
         "9e5b4466dc0f095dac12c505269b64c89401ae2366bc9c2e823a1f161f501479"),
        ("controller-entry.py", REPAIR / "controller-entry.py",
         "8fa17d56513e9452bf41c7562e59e38f6a3ed6960113c92c34f70aadd67d69c4"),
    )
    evidence = [{"archivePath": "protocol/runtime-repair/" + name, **ref(path, digest)}
                for name, path, digest in sources]
    configs = {
        family: ref(LIFE / "audit-configs-020" / ("audit-" + family + "-fresh-003.json"), digest)
        for family, digest in (
            ("claude", "05688385b07d0b00a9a98077014a26aae23a6e06713c7ddb29e78855a3d12d22"),
            ("gpt", "387f8763fd7514704baaa1fe2c8b7a7fcbd39ac28917ba06600d79e670308571"))
    }
    regression_ref = ref(REPAIR / "actual-cli-regression.json",
                         "29f701f8af608a13636b7fe0e66ded904cbdd17683df0eb310bad5a07913165b")
    regression = json.loads(frozen(regression_ref["path"], regression_ref["sha256"]))
    audit = json.loads(frozen(regression["audit"]["path"], regression["audit"]["sha256"]))
    require(regression["status"] == "PASS_REAL_PHASE1_CLI"
            and audit["status"] == "PHASE1_READY" and audit["breaches"] == []
            and audit["coreRead"] == audit["coreRequired"] == 64,
            "Real CLI regression is not complete")
    events = ref(Path(regression["audit"]["path"]).with_name("events.jsonl"),
                 regression["eventsSha256"])
    require(events["bytes"] == regression["eventsBytes"], "Regression event length changed")
    phase = ref(LIFE / "N1-B134-CLAUDE-FRESH-003-phase1.json",
                "efc3e6185dba80e19deb2cf827de0fee7da7c95719488352b03f5cf10c48ec53")
    phase_record = json.loads(frozen(phase["path"], phase["sha256"]))
    require(phase_record["readyForPhase2"] is True
            and phase_record["extensionEvidenceCapacity"]["status"] == "PASS",
            "Actual phase-one continuation did not pass")
    failures = [
        execution("b134-lifecycle-run-de2e31b0a5da4d1da578b5177262e6e0", 1,
                  "Original controller failed because the auditor main lacked imports; not reviewer misconduct."),
        execution("b134-lifecycle-execution-a741def6fc394925b875025a97551119", 1,
                  "Original auditor raised NameError before creating an audit."),
        execution("lifecycle-runtime-repair-cli-test-001", 1,
                  "The first regression assertion confused 90 sources with 64 segments; failure retained."),
        execution("coordinator-runtime-repair-retention-execution-001", 1,
                  "Retention initially rejected the still-writable completed regression-failure receipt; verified and frozen before retry."),
        execution("coordinator-runtime-repair-retention-execution-002", 1,
                  "Retention then rejected the still-writable successful regression receipt; all completed receipt/log pairs verified and frozen before retry."),
    ]
    passed = [
        execution("lifecycle-runtime-repair-cli-test-002", 0,
                  "Real repaired CLI regression passed on the immutable phase-one event stream."),
        execution("lifecycle-runtime-repair-phase1-001", 0,
                  "Actual repaired controller passed phase one and prepared the selected extension."),
    ]
    proof = {
        "status": "BOUND_IMPORT_ONLY_RUNTIME_REPAIR_NOT_REVIEW_ACCEPTANCE",
        "candidate": "355cccb840d22e7313e79f234eb93d1367e00352",
        "repair": "Supply BASE, CANDIDATE and INITIALS from their original modules to the unchanged auditor main; redirect only the original controller auditor executable path/hash.",
        "sourceFiles": evidence,
        "unchangedConfigs": configs,
        "realCliRegression": regression_ref,
        "regressionEventsLocalOnly": events,
        "actualPhase1": phase,
        "failedExecutions": failures,
        "successfulExecutions": passed,
        "limits": [
            "Original files, bootstrap authorization and core are not replaced or rebound.",
            "Raw events, receipts and logs remain local; hashes retain their exact provenance.",
            "Final reviewer event audits, substantive adjudication, serial GPT review and publication remain separate requirements.",
        ],
    }
    proof_ref = freeze_json(OUT / "provenance.json", proof)
    evidence.append({"archivePath": "verification/runtime-repair-provenance.json", **proof_ref})
    print(json.dumps(freeze_json(OUT / "evidence.json", evidence)))


if __name__ == "__main__":
    main()
