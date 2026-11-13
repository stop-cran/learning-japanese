"""Adjudicate runtime autopilot continuation nudges flagged by a HOLD audit.

The frozen auditor reports every non-kickoff, non-phase-2 user message as HOLD. When the
reviewer session runs in autopilot mode, the runtime injects fixed "not yet marked complete"
nudges whenever the reviewer correctly idles at a boundary. This tool accepts only those exact
nudges, proves no tool activity other than task_complete answered them, and writes a derived
snapshot without them so the unmodified frozen auditor can be re-run with --events-file.
Anything else stays HOLD for manual handling.
"""
import argparse
import datetime
import hashlib
import json
import re
import stat
import sys
from pathlib import Path

BOILERPLATE = (
    "You have not yet marked the task as complete using the task_complete tool. If you were planning,"
    " stop planning and start implementing. You aren't done until you have fully completed the task.\n\n"
    "IMPORTANT: Do NOT call task_complete if:\n"
    "- You have open questions or ambiguities - make good decisions and keep working\n"
    "- You encountered an error - try to resolve it or find an alternative approach\n"
    "- There are remaining steps - complete them first\n\n"
    "Keep working autonomously until the task is truly finished, then call task_complete."
)
TRANSFORMED = re.compile(r"<current_datetime>[0-9T:.+\-Z]+</current_datetime>\n\n" + re.escape(BOILERPLATE))
NOTE = re.compile(r"Unexpected user message at event (\d+); adjudicate before acceptance")
ALLOWED_NOTES = {"Report on disk equals its single write after CRLF normalization"}
TOOL_EVENTS = {"tool.execution_start", "tool.execution_complete", "external_tool.requested",
               "external_tool.completed"}


class Rejected(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def frozen_bytes(path):
    if path.stat().st_mode & stat.S_IWRITE:
        raise Rejected(f"Input is writable: {path}")
    return path.read_bytes()


def is_continuation(event):
    data = event.get("data") or {}
    return (event.get("type") == "user.message" and data.get("source") == "autopilot"
            and data.get("isAutopilotContinuation") is True and data.get("content") == ""
            and TRANSFORMED.fullmatch(data.get("transformedContent") or "") is not None)


def tool_names(event):
    kind, data = event.get("type"), event.get("data") or {}
    if kind == "assistant.message":
        return [request.get("name") for request in data.get("toolRequests") or []]
    if kind in TOOL_EVENTS:
        return [data.get("toolName")]
    return []


def adjudicate(audit_path, out_root):
    audit_path = Path(audit_path)
    audit = json.loads(frozen_bytes(audit_path))
    record = frozen_bytes(audit_path.parent / "events.jsonl")
    if audit.get("status") != "HOLD" or audit.get("breaches"):
        raise Rejected("Only a breach-free HOLD audit can be adjudicated")
    if audit.get("eventsSha256") != digest(record):
        raise Rejected("Preserved snapshot does not match its audit")
    flagged = []
    for note in audit.get("notes") or []:
        if note in ALLOWED_NOTES:
            continue
        match = NOTE.fullmatch(note)
        if not match:
            raise Rejected(f"Unhandled audit note: {note}")
        flagged.append(int(match[1]))
    if not flagged or audit.get("unexpectedUserMessages") != len(flagged):
        raise Rejected("Flagged messages do not match the audit count")
    lines = record.decode("utf-8").split("\n")
    if lines[-1].strip():
        raise Rejected("Snapshot ends with an unterminated line")
    positions = [number for number, line in enumerate(lines) if line.strip()]
    events = [json.loads(lines[number]) for number in positions]
    for index in flagged:
        if not is_continuation(events[index]):
            raise Rejected(f"Event {index} is not an exact autopilot continuation")
        for later in events[index + 1:]:
            if later.get("type") == "user.message" and not is_continuation(later):
                break
            for name in tool_names(later):
                if name != "task_complete":
                    raise Rejected(f"Tool {name} answered the continuation at event {index}")
    removed = {positions[index] for index in flagged}
    filtered = "\n".join(line for number, line in enumerate(lines) if number not in removed).encode("utf-8")
    root = Path(out_root) / ("continuations-" + datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y%m%dT%H%M%S%f"))
    root.mkdir(parents=True)
    result = {
        "status": "CONTINUATIONS_ADJUDICATED",
        "sourceAudit": str(audit_path), "sourceAuditSha256": digest(audit_path.read_bytes()),
        "sourceEventsSha256": digest(record), "retainedNotes": [note for note in audit.get("notes") or [] if note in ALLOWED_NOTES], "filteredEventsSha256": digest(filtered),
        "removed": [{"event": index, "id": events[index].get("id"),
                     "timestamp": events[index].get("timestamp")} for index in flagged],
        "basis": "Exact runtime autopilot continuation nudges with empty content; no tool other than"
                 " task_complete answered them. They carry no review content.",
        "limit": "The derived snapshot must still pass the unmodified frozen auditor; claims still need"
                 " adjudication.",
    }
    with (root / "events-filtered.jsonl").open("xb") as stream:
        stream.write(filtered)
    with (root / "adjudication.json").open("xb") as stream:
        stream.write((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    for path in root.iterdir():
        path.chmod(stat.S_IREAD)
    return root, result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        root, result = adjudicate(args.audit, args.audit.parent.parent)
    except Rejected as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}))
        return 1
    print(json.dumps({key: result[key] for key in ("status", "filteredEventsSha256", "removed")}))
    print("Filtered: " + str(root / "events-filtered.jsonl"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
