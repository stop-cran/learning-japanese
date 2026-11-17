"""Explicit native-create compatibility repair for the frozen V2 follow-up.

The inherited B116 auditor already validates native create and Add File equally.
V1's extra event allowlist accidentally excluded native create. Retain that failed
audit and the original prompt; do not rewrite the actual report or event stream.
Native create additionally requires the host's successful create-file edit record.
All context, roster, source, report-content and single-write checks remain intact.
"""
import inspect
import sys
from pathlib import Path

from common import WS, frozen, load_module, require

ROOT = WS / "scratch-134" / "review"
PARENT = (ROOT / "integration-confirmation-prep-001" / "selected-runtime-003"
          / "b134_revision_confirmation_v2.py")
PARENT_SHA = "7cd7c37e2f868584d6212336ec29fdd66576684d0e8ef0c6a899c6a8c5e6f125"
frozen(PARENT, PARENT_SHA)
parent = load_module("b134_confirmation_pinned_v2_for_create", PARENT)
legacy = parent.legacy
legacy.PINS["followupV2"] = (PARENT, PARENT_SHA)

original_envelope = inspect.getsource(legacy.event_envelope)
before = 'allowed_tools = {"view", "apply_patch", "send_session_message"}'
after = 'allowed_tools = {"view", "apply_patch", "create", "send_session_message"}'
require(original_envelope.count(before) == 1, "Event allowlist repair anchor changed")
repaired_envelope = original_envelope.replace(before, after, 1)
require(repaired_envelope.replace(after, before, 1) == original_envelope,
        "Event allowlist repair is not reversible")
exec(compile(repaired_envelope, str(__file__), "exec"), legacy.__dict__)
original_audit_snapshot = legacy.audit_snapshot


def check_native_create(events, report):
    requests = [
        call for row in events if row["type"] == "assistant.message"
        for call in (row.get("data") or {}).get("toolRequests", [])
        if str(call.get("name", "")).removeprefix("functions.") == "create"
    ]
    require(len(requests) <= 1, "More than one native report creation")
    if not requests:
        return
    call = requests[0]
    args = call.get("arguments")
    require(isinstance(args, dict) and set(args) == {"path", "file_text"}
            and args["path"] == report and isinstance(args["file_text"], str)
            and args["file_text"], "Native create is not the exact complete report")
    identity = call.get("toolCallId")
    require(isinstance(identity, str) and identity, "Native create lacks a call identity")
    starts = [
        row["data"] for row in events if row["type"] == "tool.execution_start"
        and row["data"].get("toolCallId") == identity
    ]
    ends = [
        row["data"] for row in events if row["type"] == "tool.execution_complete"
        and row["data"].get("toolCallId") == identity
    ]
    require(len(starts) == len(ends) == 1
            and str(starts[0].get("toolName", "")).removeprefix("functions.") == "create"
            and starts[0].get("arguments") == args
            and ends[0].get("success") is True
            and ends[0].get("fileEdits") == [{"path": report, "kind": "create"}],
            "Native create lacks its exact successful host creation record")
    require(Path(report).read_bytes() == args["file_text"].encode("utf-8"),
            "Native created report bytes changed")


def audit_snapshot(raw, record, config, chain, admission):
    prefix = legacy.read(admission["prefix"])
    require(len(prefix) == admission["offset"] and raw.startswith(prefix),
            "Admission prefix changed")
    check_native_create(legacy.parse_events(raw[len(prefix):]), config["report"])
    return original_audit_snapshot(raw, record, config, chain, admission)


legacy.audit_snapshot = audit_snapshot
legacy.__file__ = __file__


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    require(argv and argv[0] in ("admit", "final", "accept"),
            "This repair only operates on existing frozen follow-up preparations")
    return legacy.main(argv)


if __name__ == "__main__":
    sys.exit(main())
