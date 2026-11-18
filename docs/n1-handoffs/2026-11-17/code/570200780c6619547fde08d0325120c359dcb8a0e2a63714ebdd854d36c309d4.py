"""Verify and freeze completed coordinator execution receipts without rewriting bytes."""
import json
from datetime import datetime, timezone
from pathlib import Path

from common import freeze_json, frozen, readonly, require, sha, start_guard
from prepare_b131_source_facts import CANDIDATE, HERE, RUNNER

EXECUTIONS = (
    "source-facts-preparation-execution-001", "source-verification-execution-001",
    "source-union-verification-execution-001", "source-union-tests-001",
    "payload-verifier-preparation-execution-001", "payload-verification-execution-001",
    "payload-tests-001", "gate-evidence-recovery-execution-001", "gate-verification-execution-002",
    "packet-evidence-recovery-execution-001", "packet-verification-execution-002",
    "admission-evidence-tests-001",
)


def main():
    require(not (HERE / "verification-execution-preservation-001.json").exists(), "Preserve existing capture")
    guard, _ = start_guard("B131 verification execution preservation")
    records = {}
    try:
        for name in EXECUTIONS:
            receipt_path, log_path = HERE / name / "receipt.json", HERE / name / "output.log"
            receipt_raw, log_raw = receipt_path.read_bytes(), log_path.read_bytes()
            receipt = json.loads(receipt_raw)
            require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                    and receipt["logSha256"] == sha(log_raw) and receipt["runnerSha256"] == RUNNER["sha256"]
                    and not receipt["cleanupError"] and not receipt["memory"]["breach"],
                    "Unsuccessful or changed coordinator execution: " + name)
            records[name] = {"previouslyReadOnly": {"receipt": readonly(receipt_path), "log": readonly(log_path)}}
            for kind, path, raw in (("receipt", receipt_path, receipt_raw), ("log", log_path, log_raw)):
                path.chmod(0o444)
                require(frozen(path) == raw, "Execution bytes changed while freezing")
                records[name][kind] = {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}
            guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "verification-execution-preservation-001.json", {
        "status": "PASS", "candidate": CANDIDATE, "observedAt": datetime.now(timezone.utc).isoformat(),
        "records": records, "memory": memory, "producerSha256": sha(frozen(Path(__file__))),
        "limits": "Actual receipt/log bindings and current ReadOnly preservation; no retrospective claim "
                  "that previously writable artifacts were immutable before this observation.",
    })))


if __name__ == "__main__":
    main()
