"""Bind the desktop completion-message transport to its already-audited tool call.

The raw requested/completed external-tool envelopes are retained and checked,
not dropped. They may wrap only the single admitted completion message to this
coordinator. Native-create/CRLF, source, capacity and semantic checks remain V4's.
"""
import re
import sys
from pathlib import Path

from common import WS, frozen, load_module, require

PARENT = Path(__file__).with_name("b134_revision_confirmation_v4.py")
PARENT_SHA = "9457d59614d5d34ef22c2a2b1c7e5134cca3d098ee7abca94ec4c1f9e4819e38"
frozen(PARENT, PARENT_SHA)
parent = load_module("b134_confirmation_pinned_transport_v4", PARENT)
legacy = parent.legacy
legacy.PINS["nativeTransportV4"] = (PARENT, PARENT_SHA)
original_event_envelope = legacy.event_envelope
EXTERNAL = {"external_tool.requested", "external_tool.completed"}
legacy.BOOKKEEPING = legacy.BOOKKEEPING | EXTERNAL


def check_external_message(events, session):
    external = [(i, row) for i, row in enumerate(events) if row["type"] in EXTERNAL]
    if not external:
        return
    require(len(external) == 2 and external[0][1]["type"] == "external_tool.requested"
            and external[1][1]["type"] == "external_tool.completed",
            "External completion transport is duplicated, incomplete or reordered")
    request_index, request_event = external[0]
    end_index, end_event = external[1]
    request, end = request_event["data"], end_event["data"]
    require(set(request) == {"requestId", "sessionId", "toolCallId", "toolName",
                             "arguments", "workingDirectory"}
            and set(end) == {"requestId"}
            and isinstance(request["requestId"], str)
            and re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",
                             request["requestId"])
            and end["requestId"] == request["requestId"]
            and request["sessionId"] == session
            and request["toolName"] == "send_session_message"
            and request["workingDirectory"] == str(WS.parent),
            "External completion transport identity differs")
    args = request["arguments"]
    require(isinstance(args, dict) and set(args) == {"session_id", "message"}
            and args["session_id"] == legacy.COORDINATOR
            and args["message"] in ("CONFIRMED", "NEEDS FIX", "UNVERIFIED",
                                    "CONFIRMED\n", "NEEDS FIX\n", "UNVERIFIED\n"),
            "External transport contains an unadmitted message")
    identity = request["toolCallId"]
    calls = [
        call for row in events if row["type"] == "assistant.message"
        for call in (row.get("data") or {}).get("toolRequests", [])
        if call.get("toolCallId") == identity
    ]
    starts = [(i, row["data"]) for i, row in enumerate(events)
              if row["type"] == "tool.execution_start"
              and row["data"].get("toolCallId") == identity]
    ends = [(i, row["data"]) for i, row in enumerate(events)
            if row["type"] == "tool.execution_complete"
            and row["data"].get("toolCallId") == identity]
    require(len(calls) == len(starts) == len(ends) == 1
            and str(calls[0].get("name", "")).removeprefix("functions.") == request["toolName"]
            and calls[0].get("arguments") == args
            and starts[0][1].get("toolName") == request["toolName"]
            and starts[0][1].get("arguments") == args
            and ends[0][1].get("success") is True
            and starts[0][0] < request_index < end_index < ends[0][0],
            "External transport does not wrap the exact successful completion call")


def event_envelope(prefix, suffix, family, session):
    check_external_message(suffix, session)
    return original_event_envelope(prefix, suffix, family, session)


legacy.event_envelope = event_envelope
legacy.__file__ = __file__
check_native_create = parent.check_native_create
transport_valid = parent.transport_valid


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    require(argv and argv[0] in ("admit", "final", "accept"),
            "This repair only operates on existing frozen follow-up preparations")
    return legacy.main(argv)


if __name__ == "__main__":
    sys.exit(main())
