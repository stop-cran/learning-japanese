"""Preserve an incomplete initial and derive a blind, complete-core replacement."""
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha
from prepare_b130_review_tools import derive


ROOT = WS / "scratch-130" / "review"
RUN = "N1-B130-CLAUDE-002"
GATE = (
    "PHASE-1 SEND GATE: Before sending any selection, verify that you have read every "
    "numbered core segment through segment {{SEGMENTS}} and its END OF CHAIN terminator. "
    "Finishing the title index is not finishing the core: the curated cards and all supplied "
    "external-source extracts must also have been read. If any core segment remains, follow "
    "NEXT SEGMENT and continue reading instead of sending a message. Reading missing core "
    "segments in phase 2 cannot repair a premature phase-1 selection."
)


def bound(path):
    return {"path": str(path), "sha256": sha(frozen(path))}


def main():
    preflight_path = ROOT / "prompts" / "preflight-compact-001.json"
    preflight = json.loads(frozen(preflight_path))
    specification = preflight["runs"]["claude"]
    config = json.loads(frozen(specification["auditConfig"]))
    for item in config["files"]:
        frozen(item["path"], item["sha256"])
    phase_path = ROOT / f"{RUN}-phase1.json"
    phase = json.loads(frozen(phase_path))
    audit_path = Path(phase["auditDir"]) / "audit.json"
    audit = json.loads(frozen(audit_path, phase["auditSha256"]))
    require(phase["run"] == RUN and phase["status"] == audit["status"] == "VOID"
            and phase["breaches"] == audit["breaches"] == ["Selection sent before complete core coverage"]
            and phase["coreRead"] == audit["coreRead"] == 79
            and phase["coreRequired"] == audit["coreRequired"] == 87
            and phase["context"]["status"] == "PASS" and not phase["readyForPhase2"]
            and audit["writes"] == audit["readbacks"] == audit["extensionRead"] == 0
            and len(audit["messages"]) == 1, "Actual premature-selection failure differs")
    require(not Path(specification["report"]).exists()
            and not (ROOT / f"{RUN}-acceptance.json").exists()
            and not (ROOT / f"{RUN}-extension.json").exists(), "Void run advanced")
    frozen(Path(phase["auditDir"]) / "events.jsonl", phase["eventsSha256"])
    execution = ROOT / "claude-002-phase1-execution-001"
    receipt = json.loads((execution / "receipt.json").read_bytes())
    require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 1
            and not receipt["cleanupError"] and not receipt["memory"]["breach"]
            and receipt["logSha256"] == sha((execution / "output.log").read_bytes()), "Failure receipt differs")
    for name in ("receipt.json", "output.log"):
        (execution / name).chmod(0o444)
    held = freeze_json(ROOT / f"{RUN}-hold.json", {
        "batch": 130, "run": RUN, "session": phase["session"], "candidate": phase["candidate"],
        "status": "VOID_PREMATURE_SELECTION", "reviewAccepted": False, "finalAcceptance": False,
        "preflight": bound(preflight_path), "phase1": bound(phase_path), "audit": bound(audit_path),
        "events": bound(Path(phase["auditDir"]) / "events.jsonl"),
        "core": bound(Path(config["coreManifest"])), "report": None,
        "reason": "The reviewer sent its sole selection after 79 of 87 core segments. "
                  "The returned segment79 bytes contained the valid NEXT SEGMENT path to80. "
                  "Five curated cards and seven external extracts were not read. No compaction occurred.",
        "quarantine": "No selection, observation or comparison from this incomplete run is accepted "
                      "or may be supplied to an author or fresh reviewer. Do not resume it in phase2.",
        "failureExecution": {name: bound(execution / name) for name in ("receipt.json", "output.log")},
    })
    anchor = '    require(render(text, b116) == source, "B116 render-equality proof failed")\n'
    original = "PHASE 1 (selection). Read all {{SEGMENTS}} core segments in full. Then select:"
    replacement = "PHASE 1 (selection). Read all {{SEGMENTS}} core segments in full.\n\n"
    replacement += GATE + "\n\nThen select:"
    addition = (
        f"    gate_anchor = {original!r}\n"
        '    require(text.count(gate_anchor) == 1, "Phase-1 completeness anchor differs")\n'
        f"    text = text.replace(gate_anchor, {replacement!r})\n"
    )
    derivation = derive("build-prompts-b130-compact.py", "build-prompts-b130-complete.py", [
        ("build-prompts-b130-compact.py", "build-prompts-b130-complete.py"),
        ('"preflight-compact-001.json"', '"preflight-compact-002.json"'),
        ('"template-compact-001.txt"', '"template-compact-002.txt"'),
        ("-002", "-003"), ("review 002", "review 003"),
        (anchor, anchor + addition),
        ("the curated-slot list and a neutral external-snapshot read line differ.",
         "the curated-slot list, a neutral external-snapshot read line and a neutral complete-core gate differ."),
    ])
    print(freeze_json(ROOT / "complete-core-review-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY", "producer": bound(Path(__file__)),
        "voidInitial": held, "derivation": derivation, "neutralCompletenessGate": GATE,
        "limits": "Unchanged frozen packet, ordered core and audit/acceptance rules. "
                  "Only fresh identity and neutral completeness emphasis change. No earlier findings "
                  "or selected comparisons are supplied. Lifecycle calls must explicitly select "
                  "prompts/preflight-compact-002.json; admission and actual startup remain mandatory.",
    }))


if __name__ == "__main__":
    main()
