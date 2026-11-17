"""Preserve the coordinator phase-2 delivery mismatch and derive an identity-only fresh initial."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha
from prepare_b130_review_tools import derive


ROOT = WS / "scratch-130" / "review"
RUN = "N1-B130-CLAUDE-003"
GAP = "Tool call during the phase gap"
EXTENSION = "Extension read before phase 2 or out of order"
BREACHES = [GAP, EXTENSION] * 9 + [
    GAP, "Report write before complete required coverage, or a repeated write",
    GAP, "Invalid report readback", GAP, "Invalid completion message or premature completion",
    "Incomplete two-phase execution"]


def bound(path, expected=None):
    return {"path": str(path), "sha256": sha(frozen(path, expected))}


def main():
    preflight_path = ROOT / "prompts" / "preflight-compact-003.json"
    preflight = json.loads(frozen(preflight_path))
    spec = preflight["runs"]["claude"]
    require(spec["run"] == RUN, "Preflight run differs")
    config = json.loads(frozen(spec["auditConfig"]))
    for item in config["files"]:
        frozen(item["path"], item["sha256"])
    phase_path, final_path = ROOT / f"{RUN}-phase1.json", ROOT / f"{RUN}-final.json"
    phase, final = json.loads(frozen(phase_path)), json.loads(frozen(final_path))
    require(phase["status"] == "PHASE1_READY" and phase["readyForPhase2"] and not phase["breaches"]
            and phase["coreRead"] == phase["coreRequired"] == 87 and phase["context"]["status"] == "PASS"
            and phase["session"] == final["session"], "Actual phase-1 record differs")
    audit_path = Path(final["finalAudit"]["path"])
    audit = json.loads(frozen(audit_path, final["finalAudit"]["sha256"]))
    events_path = audit_path.parent / "events.jsonl"
    events_raw = frozen(events_path, audit["eventsSha256"])
    context = json.loads(frozen(final["context"]["path"], final["context"]["sha256"]))
    frozen(final["structure"]["path"], final["structure"]["sha256"])
    require(final["status"] == "HOLD" and audit["status"] == "VOID" and audit["breaches"] == BREACHES
            and audit["coreRead"] == audit["coreRequired"] == 87
            and audit["extensionRead"] == audit["extensionRequired"] == 9
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
            and audit["fetches"] == 0 and audit["unexpectedUserMessages"] == 1 and audit["reviewerIdle"]
            and len(audit["messages"]) == 2 and context["status"] == "PASS", "Actual final failure differs")
    phase2_path = ROOT / f"{RUN}-phase2-message.txt"
    phase2 = frozen(phase2_path).decode("utf-8")
    events = [json.loads(line) for line in events_raw.decode("utf-8").splitlines()]
    users = [(i, e["data"]["content"]) for i, e in enumerate(events) if e.get("type") == "user.message"]
    require(len(users) == 2 and users[0][1] == spec["kickoffText"], "User-message sequence differs")
    delivered_index, delivered = users[1]
    require(delivered != phase2 and phase2 == delivered + "\nMissing entries: none"
            and "\n" not in delivered, "Delivered phase-2 mismatch differs")
    extension_calls = [c for c in audit["calls"] if "-extension\\" in str(c.get("arguments"))]
    require(len(extension_calls) == 9 and min(c["event"] for c in extension_calls) > delivered_index,
            "Extension reads did not follow the delivered message")
    execution = ROOT / "claude-003-final-execution-001"
    receipt = json.loads((execution / "receipt.json").read_bytes())
    require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 1
            and not receipt["cleanupError"] and not receipt["memory"]["breach"]
            and receipt["logSha256"] == sha((execution / "output.log").read_bytes()), "Failure receipt differs")
    for name in ("receipt.json", "output.log"):
        (execution / name).chmod(0o444)
    report = Path(spec["report"])
    require(report.exists() and not (ROOT / f"{RUN}-acceptance.json").exists(), "Report/acceptance state differs")
    report.chmod(0o444)
    held = freeze_json(ROOT / f"{RUN}-hold.json", {
        "batch": 130, "run": RUN, "session": final["session"], "candidate": final["candidate"],
        "status": "VOID_COORDINATOR_PHASE2_MESSAGE_MISMATCH", "reviewAccepted": False, "finalAcceptance": False,
        "preflight": bound(preflight_path), "phase1": bound(phase_path), "final": bound(final_path),
        "audit": bound(audit_path), "events": bound(events_path), "context": final["context"],
        "structure": final["structure"], "phase2Message": bound(phase2_path),
        "deliveredPhase2": {"eventIndex": delivered_index, "sha256": sha(delivered.encode("utf-8")),
                            "missingSuffix": "\nMissing entries: none"},
        "report": {"path": str(report), "sha256": sha(report.read_bytes()), "quarantined": True},
        "reason": "The coordinator sent only the first line (the extension path) of the frozen two-line "
                  "phase-2 message and omitted 'Missing entries: none'. The auditor therefore never "
                  "recognized phase 2 and VOIDed all later calls. Phase 1 was clean (87/87, context PASS); "
                  "all nine extension reads followed the delivered message. This is a coordinator protocol "
                  "breach, not a reviewer breach, but the frozen exact-message gate is not waived or relabeled.",
        "quarantine": "The report, selection and observations from this run are not accepted and may not be "
                      "supplied to an author or fresh reviewer. The coordinator has not read the report text.",
        "failureExecution": {name: bound(execution / name) for name in ("receipt.json", "output.log")},
    })
    derivation = derive("build-prompts-b130-complete.py", "build-prompts-b130-attempt004.py", [
        ("build-prompts-b130-complete.py", "build-prompts-b130-attempt004.py"),
        ('"preflight-compact-003.json"', '"preflight-compact-004.json"'),
        ('"template-compact-003.txt"', '"template-compact-004.txt"'),
        ('{label}-003"', '{label}-004"'), ('-{key}-003.txt"', '-{key}-004.txt"'),
        ('-{key}-003.md"', '-{key}-004.md"'), ('"initial-claude-003.txt"', '"initial-claude-004.txt"'),
        ('"initial-gpt-003.txt"', '"initial-gpt-004.txt"'), ('review 003"', 'review 004"'),
    ])
    print(freeze_json(ROOT / "attempt004-review-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY", "producer": bound(Path(__file__)),
        "voidInitial": held, "derivation": derivation,
        "limits": "Unchanged frozen packet, ordered core, neutral complete-core gate and audit/acceptance rules. "
                  "Only fresh run identity changes; the reviewer prompt gains no new text. No earlier findings, "
                  "selection or comparisons are supplied. Lifecycle calls must explicitly select "
                  "prompts/preflight-compact-004.json. The coordinator must send the printed phase-2 message "
                  "byte-exactly, including every line; admission and actual startup remain mandatory.",
    }))


if __name__ == "__main__":
    main()
