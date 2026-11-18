import json
import stat
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha

ROOT = WS / "scratch-134" / "review"
HERE = Path(__file__).parent
RUNNER = "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
GUARD = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"


def ref(path):
    return {"path": str(path), "sha256": sha(frozen(path))}


def main():
    target = HERE / "claude-evidence.json"
    require(not target.exists(), "Preserve the existing sealed evidence index")
    executions = {}
    expected = {
        "revision-confirmation-v3-controls-exec-001": 0,
        "revision-confirmation-v4-controls-exec-001": 0,
        "revision-confirmation-v5-controls-exec-001": 0,
        "revision-confirmation-claude-final-exec-001": 1,
        "revision-confirmation-claude-final-exec-002": 1,
        "revision-confirmation-claude-final-exec-003": 1,
        "revision-confirmation-claude-final-exec-004": 0,
        "revision-confirmation-claude-accept-exec-001": 0,
    }
    for name, exit_code in expected.items():
        receipt_path, log_path = ROOT / name / "receipt.json", ROOT / name / "output.log"
        receipt = json.loads(receipt_path.read_bytes())
        require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == exit_code
                and receipt["cleanupError"] is None
                and receipt["runnerSha256"] == RUNNER and receipt["guardSha256"] == GUARD
                and receipt["memory"]["breach"] is None
                and receipt["memory"]["freeRamBeforeBytes"] > 2 * 1024**3
                and receipt["memory"]["minimumObservedFreeRamBytes"] >= 1024**3
                and receipt["logSha256"] == sha(log_path.read_bytes()),
                f"Unverified execution receipt: {name}")
        for path in (receipt_path, log_path):
            path.chmod(stat.S_IREAD)
        executions[name] = {"expectedExit": exit_code, "receipt": ref(receipt_path), "log": ref(log_path)}
    producer = HERE / "b134_revision_confirmation_v5.py"
    accepted = json.loads(frozen(ROOT / "revision-confirmation-claude-accept-001" / "acceptance.json"))
    require(accepted["confirmationAccepted"] is True and accepted["verdict"] == "CONFIRMED"
            and accepted["priorRawVerdict"] == "NEEDS FIX"
            and accepted["producer"] == ref(producer) and accepted["deliveryCredit"] == 0,
            "Actual same-reviewer bounded acceptance missing")
    controls = {
        str(version): ref(ROOT / f"revision-confirmation-v{version}-controls-001" / "result.json")
        for version in (3, 4, 5)
    }
    failures = []
    reasons = ("Native creation absent from added event allowlist",
               "Native LF request written with Windows CRLF",
               "Desktop completion transport envelopes absent from event allowlist")
    for number, reason in enumerate(reasons, 1):
        area = ROOT / f"revision-confirmation-claude-final-{number:03}"
        require(not (area / "final.json").exists(), "Failed attempt acquired a final result")
        failures.append({"attempt": number, "reason": reason,
                         "rawEvents": ref(area / "events.jsonl"),
                         "auditMemory": ref(area / "audit-memory.json")})
    code = [
        ref(HERE / name) for name in (
            "b134_revision_confirmation_v3.py", "test-native-create.py",
            "b134_revision_confirmation_v4.py", "test-native-transport.py",
            "b134_revision_confirmation_v5.py", "test-external-message.py",
            "decision-claude-001.json", "seal-claude-evidence.py")
    ]
    result = {
        "status": "ACTUAL_CLAUDE_BOUNDED_REVISION_ACCEPTED",
        "candidate": accepted["candidate"], "selectedProducer": ref(producer),
        "acceptance": ref(ROOT / "revision-confirmation-claude-accept-001" / "acceptance.json"),
        "adjudication": accepted["adjudication"], "final": accepted["final"], "report": accepted["report"],
        "controls": controls, "actualReplay": ref(ROOT / "revision-confirmation-v5-controls-001" / "actual-replay.json"),
        "executions": executions, "failedAttempts": failures, "repairFiles": code,
        "dispositions": {"F1": "DECLINE ACCEPTED", "O1": "DECLINE ACCEPTED",
                         "O2": "DECLINE ACCEPTED", "O3": "DECLINE ACCEPTED"},
        "limits": [
            "All original code, raw events and reports remain unchanged; compatibility is versioned.",
            "Native create and deterministic LF-to-CRLF expansion are disclosed, not byte-exact-write claims.",
            "External desktop events must bind the exact single successful completion message.",
            "The literal F1 token is retained; earlier withdrawn status and NEEDS FIX are not rewritten.",
            "GPT has not been contacted. No closure, integration or publication credit."
        ],
    }
    print(json.dumps(freeze_json(target, result)))


if __name__ == "__main__":
    main()
