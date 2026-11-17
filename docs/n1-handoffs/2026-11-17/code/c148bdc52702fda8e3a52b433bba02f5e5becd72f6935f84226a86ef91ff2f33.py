"""Adjudicate one exact runtime-only reminder after the completed, unchanged Claude004 review."""
import copy
import json
from pathlib import Path

from b130_context_confirmation import ROOT, binding
from common import freeze_json, frozen, load_module, require, sha, write_frozen
from confirm_b130_fresh_context import clean, preflight
from common import load_batch

RUN = "N1-B130-CLAUDE-CONFIRM-004"
OUT = ROOT / "confirm"
RAW = OUT / RUN / "audit-20261116T135840716486"
RAW_AUDIT_SHA = "273bfcc4aa5c10b57fa90dbfa2efc8be1a37530ce244ef03346952cbb53dea99"
NOTICE_SHA = "3f1214fcf0b7a0e35bc51596253aecac72a2e2dd8a3646a7101c9815874b5bee"
INDEX = 253


def event_sha(event):
    return sha(json.dumps(event, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())


def classify_control(events):
    require(len(events) == 268 and event_sha(events[INDEX]) == NOTICE_SHA,
            "Not the independently inspected exact control event")
    users = [i for i, event in enumerate(events) if event["type"] == "user.message"]
    require(len(users) == 2 and users[-1] == INDEX, "Additional or misplaced user input")
    notice = events[INDEX]["data"]
    require(notice["source"] == "autopilot" and notice["content"] == ""
            and notice["isAutopilotContinuation"] is True and notice["delivery"] == "idle",
            "Not a runtime completion reminder")
    starts = [(i, event["data"]) for i, event in enumerate(events)
              if event["type"] == "tool.execution_start"]
    sends = [(i, data) for i, data in starts if data["toolName"] == "send_session_message"]
    require(len(sends) == 1 and sends[0][0] < INDEX
            and sends[0][1]["arguments"]["message"] == "CONFIRMED",
            "Reminder did not follow the completed confirmation")
    send_id = sends[0][1]["toolCallId"]
    completions = [i for i, event in enumerate(events) if event["type"] == "tool.execution_complete"
                   and event["data"]["toolCallId"] == send_id and event["data"].get("success") is True]
    require(len(completions) == 1 and completions[0] < INDEX, "Completion send had not succeeded")
    later = [(i, data) for i, data in starts if i > sends[0][0]]
    require(len(later) == 1 and later[0][0] > INDEX
            and later[0][1]["toolName"] == "task_complete"
            and event_sha(events[later[0][0]]) == "c54d0450933280f480e743602cda313c5cf454313074ebf7f4af617e2b44dacc",
            "Review activity continued beyond the one permitted completion")
    result = copy.deepcopy(events)
    result[INDEX]["type"] = "system.adjudicated_runtime_completion_reminder"
    require(all(left == right for i, (left, right) in enumerate(zip(events, result)) if i != INDEX),
            "Other events changed in the classified view")
    return result


def main():
    raw_audit = json.loads(frozen(RAW / "audit.json", RAW_AUDIT_SHA))
    require(raw_audit["status"] == "HOLD" and raw_audit["unexpectedUserMessages"] == 1
            and not raw_audit["breaches"] and raw_audit["reviewerIdle"]
            and not raw_audit["recordIncomplete"], "Original hold changed")
    raw = frozen(RAW / "events.jsonl", raw_audit["eventsSha256"])
    events = [json.loads(line) for line in raw[raw_audit["offset"]:].splitlines()]
    classified = classify_control(events)
    record, config = preflight(OUT / f"{RUN}-preflight.json")
    require(record["run"] == RUN and record["session"] == raw_audit["session"], "Wrong review identity")
    clean(load_batch(130), record["candidate"])
    chain = json.loads(frozen(config["chainManifest"]))
    auditor = load_module("b130_original_confirmation_auditor", OUT / "audit-confirm.py")
    repeated = auditor.audit(events, config, chain, True, False)
    require(all(value == raw_audit[key] for key, value in repeated.items()),
            "Original full audit no longer reproduces exactly")
    checked = auditor.audit(classified, config, chain, True, False)
    require(checked["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
            and checked["unexpectedUserMessages"] == 0 and not checked["breaches"]
            and all(value == repeated[key] for key, value in checked.items()
                    if key not in ("status", "notes", "unexpectedUserMessages")),
            "More than the one control-message classification changed")
    destination = OUT / RUN / "audit-adjudicated-control-001"
    raw_copy = write_frozen(destination / "events.jsonl", raw)
    classification = freeze_json(destination / "control-adjudication.json", {
        "run": RUN, "rawAudit": binding(RAW / "audit.json"), "events": raw_copy,
        "eventIndexWithinAdmittedSlice": INDEX, "eventSha256": NOTICE_SHA,
        "rawUnexpectedUserMessages": 1, "classifiedRuntimeCompletionReminders": 1,
        "decision": "Runtime-generated empty-content autopilot reminder arrived AFTER report write, "
                    "readback and successful verdict send. Its only following tool was the already "
                    "permitted task_complete with the identical verdict. It supplied no review evidence, "
                    "changed no report or conclusion, and prompted no further review operation.",
        "limits": "Exact-event adjudication, not an allowance for arbitrary runtime/user messages. "
                  "The original HOLD, full raw log and failed finalization remain unchanged. "
                  "This classification is not substantive acceptance or publication.",
        "producer": binding(__file__),
    })
    audit = {**raw_audit, **checked, "rawAudit": binding(RAW / "audit.json"),
             "controlAdjudication": classification,
             "auditBasis": "Full unchanged raw log with one explicitly classified post-completion control event"}
    audit_binding = freeze_json(destination / "audit.json", audit)
    report_path = Path(config["report"])
    report_path.chmod(0o444)
    report = binding(report_path)
    context_checker = load_module("b130_control_context", ROOT / "check-run-context.py")
    context = context_checker.check(destination / "events.jsonl")
    structure_checker = load_module("b130_control_structure", OUT / "check-confirm-structure.py")
    structure = structure_checker.check(frozen(report_path).decode(), RUN, record["candidate"],
                                        config["dispositionIds"], chain, checked["messages"][0])
    require(context["status"] == structure["status"] == "PASS", "Context or report structure failed")
    context_binding = freeze_json(OUT / f"{RUN}-context.json", context)
    structure_binding = freeze_json(OUT / f"{RUN}-structure.json", structure)
    final = freeze_json(OUT / f"{RUN}-final.json", {
        "run": RUN, "candidate": record["candidate"], "session": record["session"],
        "audit": audit_binding, "context": context_binding, "structure": structure_binding,
        "report": report, "confirmation": structure["confirmation"],
        "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
        "rawAudit": binding(RAW / "audit.json"), "controlAdjudication": classification,
    })
    print(json.dumps({"final": final, "report": report, "controlAdjudication": classification,
                      "context": context, "structure": structure}))


if __name__ == "__main__":
    main()
