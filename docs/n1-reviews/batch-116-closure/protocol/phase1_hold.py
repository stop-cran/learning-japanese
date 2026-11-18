"""Narrow phase-1 HOLD gate: accept only runtime autopilot continuations after the sole phase-1 send.

The frozen auditor routes every non-coordinator user message to HOLD for adjudication. This gate
re-derives, from the audit's own preserved record, that each such message is an empty autopilot
continuation (no cross-session envelope or packet content) arriving after the phase-1 send, and that
the reviewer made no further tool request. A bound, ReadOnly coordinator adjudication is required.
"""
import json
import re
import stat
from pathlib import Path

from review_chain import digest

DECISION = "PHASE1_ACCEPTED_AFTER_ADJUDICATION"
NOTE = re.compile(r"Unexpected user message at event (\d+); adjudicate before acceptance")
STAMP = re.compile(r"\A<current_datetime>[^<\n]*</current_datetime>\n\n")


def autopilot_body(data):
    return STAMP.sub("", data.get("transformedContent") or "", count=1)


def check(phase1, phase1_bytes, audit_path, adjudication_path, reply_bytes):
    """Return None when the phase-1 audit may build an extension; otherwise a refusal reason."""
    if phase1.get("breaches") != []:
        return "Phase-1 audit has breaches"
    if phase1.get("phase1ListSha256") != digest(reply_bytes):
        return "Phase-1 list is not bound to the audit"
    if phase1.get("status") == "PHASE1_READY":
        return None
    if phase1.get("status") != "HOLD":
        return "Phase-1 audit is neither ready nor an adjudicable hold"
    if (phase1.get("recordIncomplete") or not phase1.get("bootstrapVerified") or not phase1.get("reviewerIdle")
            or not phase1.get("actualResponseModels") or phase1.get("coreRead") != phase1.get("coreRequired")
            or len(phase1.get("messages") or []) != 1 or phase1.get("writes") or phase1.get("fetches")):
        return "Phase-1 hold is not otherwise complete"
    indices = []
    for note in phase1.get("notes") or []:
        match = NOTE.fullmatch(note)
        if not match:
            return f"Unadjudicable note: {note}"
        indices.append(int(match[1]))
    if not indices or len(indices) != phase1.get("unexpectedUserMessages"):
        return "Hold notes do not match the unexpected-message count"
    if adjudication_path is None:
        return "Hold requires a coordinator adjudication"
    if adjudication_path.stat().st_mode & stat.S_IWRITE:
        return "Adjudication is writable"
    adjudication = json.loads(adjudication_path.read_bytes())
    if (adjudication.get("decision") != DECISION or adjudication.get("auditSha256") != digest(phase1_bytes)
            or adjudication.get("phase1ListSha256") != digest(reply_bytes)
            or sorted(adjudication.get("autopilotEvents") or []) != sorted(indices)):
        return "Adjudication is not bound to this audit, list and events"
    events_path = audit_path.parent / "events.jsonl"
    if events_path.stat().st_mode & stat.S_IWRITE:
        return "Preserved record is writable"
    record = events_path.read_bytes()
    if digest(record) != phase1.get("eventsSha256"):
        return "Preserved record hash differs from the audit"
    events = [json.loads(line) for line in record.decode("utf-8").split("\n") if line.strip()]
    sends = [(i, request.get("toolCallId")) for i, event in enumerate(events)
             if event.get("type") == "assistant.message"
             for request in (event.get("data") or {}).get("toolRequests") or []
             if request.get("name") == "send_session_message"]
    if len(sends) != 1:
        return "Record does not contain exactly one phase-1 send"
    send_index, send_id = sends[0]
    bodies = set()
    for index, event in enumerate(events):
        kind, data = event.get("type"), event.get("data") or {}
        if index <= send_index:
            continue
        if kind == "assistant.message" and data.get("toolRequests"):
            return f"Tool request after the phase-1 send at event {index}"
        if kind == "tool.execution_start" and data.get("toolCallId") != send_id:
            return f"Tool execution after the phase-1 send at event {index}"
        if kind == "user.message":
            body = autopilot_body(data)
            if (index not in indices or data.get("source") != "autopilot" or data.get("content") != ""
                    or "<cross_session_message>" in body or not body.strip()):
                return f"User message at event {index} is not an empty autopilot continuation"
            bodies.add(body)
    if any(not (send_index < index < len(events)) for index in indices) or len(bodies) != 1:
        return "Hold events are not uniform autopilot continuations after the send"
    if adjudication.get("autopilotBodySha256") != digest(next(iter(bodies)).encode("utf-8")):
        return "Adjudication does not bind the continuation text"
    return None


def adjudicable_events(phase1_bytes):
    """Event indices named by HOLD notes, for building the adjudication record."""
    phase1 = json.loads(phase1_bytes)
    return [int(NOTE.fullmatch(note)[1]) for note in phase1.get("notes") or [] if NOTE.fullmatch(note)]


def body_digest(events_path, index):
    events = [json.loads(line) for line in Path(events_path).read_bytes().decode("utf-8").split("\n") if line.strip()]
    return digest(autopilot_body(events[index]["data"]).encode("utf-8"))
