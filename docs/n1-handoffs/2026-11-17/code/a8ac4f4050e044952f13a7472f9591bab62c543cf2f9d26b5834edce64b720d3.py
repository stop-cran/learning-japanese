"""Read-only B134 review-run audit (v4). Preserves the raw record before any parsing or verdict.

v4 differs from v2 only by a required maxWebFetches limit (0 makes any web_fetch a breach), an
explicit web-search/browser breach, and explicit final-audit readback/completion labels.

A mechanically clean final result is only FINAL_AUDIT_NEEDS_CLAIM_CHECK: every report claim and
any ambiguous response grouping still needs full-record adjudication before acceptance.
"""
import argparse
import datetime
import ipaddress
import json
import re
import stat
import sys
import traceback
from pathlib import Path
from urllib.parse import urlsplit

sys.path.append(r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from review_chain_with_optional import digest, optional_unit_map, validate_selection
from b134_common import (
    CAPACITY, CAPACITY_SHA, CORE, CORE_SHA, HERE as LIFECYCLE, PACKET, PROTOCOL,
    frozen, prompt_core_release_message, validate_prompt_only_event_shape, verify_core, verify_packet,
)

HERE = Path(__file__).resolve().parent
OUTPUT_BASE = LIFECYCLE
PREFLIGHT = LIFECYCLE / "audit-configs-015" / "preflight.json"
PREFLIGHT_SHA = "f9cf056904cb37379f6e207c665366118383f5291dddc30f4643cac75d89ed94"
REQUIRED_CONFIG = ("run", "candidate", "base", "publishedBaseline", "role", "originalSession",
                   "originalReviewerConfirmation", "kickoff", "kickoffText", "promptSha256",
                   "prompt", "report", "coordinator", "expectedFamily",
                   "coreManifest", "coreManifestSha256", "reference", "files", "maxWebFetches",
                   "completionContract", "completionContractScope", "reportStructureContract",
                   "reportStructureChecker",
                   "bootstrapRecordPath", "coreAuthorizationPath", "coreReleaseMessage",
                   "bootstrapResponseText", "capacityForecastSha256", "contextProfile",
                   "packetInventorySha256", "losslessVerificationSha256")
VIEW_KEYS = {"path", "forceReadLargeFiles", "view_range"}
COMPLETION_CONTRACT = "entire-message-enum-v1"
COMPLETION_ENUM = re.compile(r"(?:CLEAN|NEEDS FIX|UNVERIFIED)(?:\r?\n)?")


class IntegrityError(Exception):
    """A frozen input changed or lost its ReadOnly flag: the pass cannot be accepted."""


def arguments(raw):
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return raw


def load_events(record_bytes):
    """Parse JSONL; an unparseable unterminated final line marks a live, incomplete record."""
    lines = record_bytes.decode("utf-8").split("\n")
    tail = lines.pop()
    events = [json.loads(line) for line in lines if line.strip()]
    incomplete = False
    if tail.strip():
        try:
            events.append(json.loads(tail))
        except json.JSONDecodeError:
            incomplete = True
    return events, incomplete


def public_https(url):
    try:
        parts = urlsplit(url)
        host = (parts.hostname or "").lower()
    except ValueError:
        return False
    if parts.scheme != "https" or not host or parts.username or parts.password:
        return False
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal", ".lan")):
        return False
    try:
        return ipaddress.ip_address(host).is_global
    except ValueError:
        return "." in host


def patch_text(patch, report):
    """Return the created text when the patch is exactly one Add File of the report."""
    lines = patch.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if (len(lines) < 4 or lines[0] != "*** Begin Patch" or lines[1] != "*** Add File: " + report
            or lines[-1] != "*** End Patch" or any(not line.startswith("+") for line in lines[2:-1])):
        return None
    return "".join(line[1:] + "\n" for line in lines[2:-1])


def validate_bootstrap_authorization(config, session, config_raw):
    profile = config["contextProfile"]
    bootstrap_path = Path(config["bootstrapRecordPath"])
    authorization_path = Path(config["coreAuthorizationPath"])
    bootstrap_raw = require_frozen(bootstrap_path)
    bootstrap = json.loads(bootstrap_raw)
    snapshot_path = Path(bootstrap["eventSnapshotPath"])
    snapshot_raw = require_frozen(snapshot_path, bootstrap["eventSnapshotSha256"])
    authorization_raw = require_frozen(authorization_path)
    authorization = json.loads(authorization_raw)
    if (bootstrap.get("status") != "PROMPT_ONLY_BOOTSTRAP_PASS"
            or bootstrap.get("sessionId") != session
            or bootstrap.get("run") != config["run"]
            or bootstrap.get("candidate") != config["candidate"]
            or bootstrap.get("base") != config["base"]
            or bootstrap.get("configSha256") != digest(config_raw)
            or bootstrap.get("kickoffSha256") != digest(config["kickoffText"].encode("utf-8"))
            or bootstrap.get("promptSha256") != digest(require_frozen(
                config["prompt"], config["promptSha256"]))
            or bootstrap.get("eventSnapshotBytes") != len(snapshot_raw)
            or bootstrap.get("eventCount") is None
            or bootstrap.get("eventSnapshotLastType") != "session.usage_checkpoint"
            or bootstrap.get("eventSnapshotPath") != str(snapshot_path)
            or bootstrap.get("selectedModel") != profile["selectedModel"]
            or bootstrap.get("contextTier") != "long_context"
            or bootstrap.get("maxPromptTokens") != profile["maxPromptTokens"]
            or authorization.get("status") != "CORE_RELEASE_AUTHORIZED"
            or authorization.get("sessionId") != session
            or authorization.get("run") != config["run"]
            or authorization.get("candidate") != config["candidate"]
            or authorization.get("base") != config["base"]
            or authorization.get("configSha256") != digest(config_raw)
            or authorization.get("bootstrapRecordSha256") != digest(bootstrap_raw)
            or authorization.get("bootstrapRecordPath") != str(bootstrap_path)
            or authorization.get("eventSnapshotSha256") != bootstrap["eventSnapshotSha256"]
            or authorization.get("eventSnapshotPath") != str(snapshot_path)
            or authorization.get("selectedModel") != profile["selectedModel"]
            or authorization.get("contextTier") != "long_context"
            or authorization.get("maxPromptTokens") != profile["maxPromptTokens"]
            or authorization.get("usageRecords") != bootstrap.get("usageRecords")
            or authorization.get("actualPeakInputTokens") != bootstrap.get("actualPeakInputTokens")
            or authorization.get("compactionEvents") != []):
        raise IntegrityError("Bootstrap/core-release record is not bound to this run")
    events, incomplete = load_events(snapshot_raw)
    if incomplete:
        raise IntegrityError("Prompt-only event snapshot is incomplete")
    validate_prompt_only_event_shape(events)
    starts = [event["data"] for event in events if event.get("type") == "session.start"]
    usage = [event.get("data", {}).get("usage") for event in events
             if event.get("type") == "session.usage_record"]
    tool_starts = [event["data"] for event in events if event.get("type") == "tool.execution_start"]
    tool_completes = [event["data"] for event in events if event.get("type") == "tool.execution_complete"]
    requested = [request for event in events if event.get("type") == "assistant.message"
                 for request in event.get("data", {}).get("toolRequests", [])]
    users = [event.get("data", {}).get("content") for event in events if event.get("type") == "user.message"]
    assistant_final = [event.get("data", {}).get("content") for event in events
                       if event.get("type") == "assistant.message"
                       and not event.get("data", {}).get("toolRequests")]
    compactions = [event.get("type") for event in events
                   if str(event.get("type", "")).startswith("session.compaction")]
    if (not snapshot_raw.endswith(b"\n") or len(starts) != 1 or len(events) != bootstrap["eventCount"]
            or starts[0].get("sessionId") != session
            or starts[0].get("selectedModel") != profile["selectedModel"]
            or starts[0].get("contextTier") != "long_context"
            or events[-1].get("type") != "session.usage_checkpoint"
            or users != [config["kickoffText"]]
            or len(requested) != 1
            or len(tool_starts) != 1 or tool_starts[0].get("toolName") != "view"
            or tool_starts[0].get("arguments", {}).get("path") != config["prompt"]
            or tool_starts[0].get("arguments", {}).get("forceReadLargeFiles") is not True
            or tool_starts[0].get("arguments", {}).get("view_range") is not None
            or set(tool_starts[0].get("arguments", {})) - VIEW_KEYS
            or len(tool_completes) != 1 or tool_completes[0].get("success") is not True
            or tool_starts[0].get("toolCallId") != tool_completes[0].get("toolCallId")
            or requested[0].get("name", "").removeprefix("functions.") != "view"
            or requested[0].get("toolCallId") != tool_starts[0].get("toolCallId")
            or arguments(requested[0].get("arguments")) != tool_starts[0].get("arguments")
            or (tool_completes[0].get("result") or {}).get("content")
            != frozen(config["prompt"], config["promptSha256"]).decode("utf-8")
            or len(assistant_final) != 1 or assistant_final[0] != config["bootstrapResponseText"]
            or not usage or any(not isinstance(item, dict)
                                or item.get("model") != profile["selectedModel"]
                                or item.get("maxPromptTokens") != profile["maxPromptTokens"]
                                or type(item.get("inputTokens")) is not int
                                or not 0 <= item["inputTokens"] <= profile["maxPromptTokens"]
                                for item in usage)
            or bootstrap.get("usageRecords") != len(usage)
            or bootstrap.get("actualPeakInputTokens") != max(item["inputTokens"] for item in usage)
            or compactions):
        raise IntegrityError("Prompt-only bootstrap telemetry or event boundary differs")
    return bootstrap, authorization, snapshot_raw, len(events), digest(authorization_raw)


def audit_base(events, config, core, reference, extension=None, phase1_text=None, phase2_text=None,
          final=False, record_incomplete=False):
    bootstrap_count = config.get("_bootstrapSnapshotEventCount")
    if bootstrap_count is not None:
        validate_prompt_only_event_shape(events[:bootstrap_count])
    if config.get("completionContract") != COMPLETION_CONTRACT:
        raise IntegrityError("The v4 auditor requires its explicit entire-message enum contract")
    fetch_limit = config.get("maxWebFetches")
    if type(fetch_limit) is not int or fetch_limit < 0:
        raise IntegrityError("The v4 auditor requires an explicit non-negative integer maxWebFetches")
    breaches, notes, calls, sends = [], [], [], []
    pending, covered, requested_args = {}, set(), {}
    usage_models, assistant_models = [], set()
    core_paths = [segment["path"] for segment in core["segments"]]
    extension_paths = [segment["path"] for segment in (extension or {"segments": []})["segments"]]
    chain_paths = set(core_paths) | set(extension_paths)
    sums = verify_packet()
    unit_index = json.loads(frozen(
        PACKET / "evidence/kanjidic2-full-unit-index.json",
        sums["evidence/kanjidic2-full-unit-index.json"]))
    optional_units = optional_unit_map(unit_index)
    report, coordinator = config["report"], config["coordinator"]
    family = config["expectedFamily"].lower()
    kickoff = Path(config["kickoff"]).read_bytes().decode("utf-8")
    prompt = Path(config["prompt"]).read_bytes().decode("utf-8")
    bootstrap = bootstrap_reply = core_released = phase2 = completed = readback_ok = False
    writes = readbacks = fetches = seen_core = seen_extension = user_count = unexpected_users = 0
    written_text = None
    response_calls, response_text = {}, {}
    last_complete = last_turn_end = last_user = -1
    first_call, missing_api = True, False

    def breach(reason):
        breaches.append(reason)

    def from_coordinator(data):
        source = data.get("source")
        if source is not None:
            return source == "agent-" + coordinator
        envelope = re.search(r"(?s)<cross_session_message>(.*?)</cross_session_message>",
                             data.get("transformedContent") or "")
        return bool(envelope and re.search(
            r"(?m)^from_(?:project_)?session_id:\s*" + re.escape(coordinator) + r"\s*$", envelope[1]))

    for index, event in enumerate(events):
        kind, data = event.get("type"), event.get("data") or {}
        if kind == "session.usage_record":
            usage = data.get("usage") or {}
            model = usage.get("responseModel")
            usage_models.append({"event": index, "model": usage.get("model"), "responseModel": model})
            if model and not model.lower().startswith(family):
                breach(f"Unexpected response model: {model}")
        elif kind == "user.message":
            user_count += 1
            last_user = index
            content = data.get("content")
            if user_count == 1:
                if content != kickoff:
                    breach("Delivered kickoff is not byte-equal to the frozen kickoff")
                if not from_coordinator(data):
                    breach("Kickoff provenance is not the coordinator")
            elif (content == config["coreReleaseMessage"] and from_coordinator(data)):
                if (core_released or not bootstrap or not bootstrap_reply
                        or index < config["_bootstrapSnapshotEventCount"]):
                    breach("Core release did not follow the verified prompt-only bootstrap")
                core_released = True
            elif phase2_text is not None and content == phase2_text and from_coordinator(data):
                if phase2 or len(sends) != 1:
                    breach("Invalid or duplicate phase-2 transition")
                phase2 = True
            else:
                unexpected_users += 1
                notes.append(f"Unexpected user message at event {index}; adjudicate before acceptance")
        elif kind == "assistant.turn_end":
            last_turn_end = index
        elif kind == "assistant.message":
            text = data.get("content") or ""
            model = data.get("model")
            if model:
                assistant_models.add(model)
                if not model.lower().startswith(family):
                    breach(f"Unexpected assistant model: {model}")
            api = data.get("apiCallId")
            if not api:
                missing_api = True
            key = api or f"event-{index}"
            response_text[key] = response_text.get(key, "") + "\n" + text
            requests = data.get("toolRequests") or []
            if not requests:
                if bootstrap and not core_released:
                    if text != config["bootstrapResponseText"]:
                        breach("Prompt-only turn did not end with the exact bootstrap response")
                    else:
                        bootstrap_reply = True
                continue
            response_calls[key] = response_calls.get(key, 0) + len(requests)
            if response_calls[key] > 1:
                breach("More than one tool call in one model response")
            for request in requests:
                name = str(request.get("name", "")).removeprefix("functions.")
                args = arguments(request.get("arguments"))
                cid = request.get("toolCallId")
                record = {"id": cid, "name": name, "event": index, "phase": 2 if phase2 else 1,
                          "timestamp": event.get("timestamp"), "arguments": args}
                if not cid or cid in pending or any(call["id"] == cid for call in calls):
                    breach("Missing or duplicate tool call identity")
                if pending:
                    breach("Tool call while a previous call is outstanding")
                calls.append(record)
                pending[cid] = record
                requested_args[cid] = args
                if first_call:
                    first_call = False
                    record["role"] = "bootstrap"
                    if (name != "view" or not isinstance(args, dict) or args.get("path") != config["prompt"]
                            or args.get("forceReadLargeFiles") is not True
                            or args.get("view_range") is not None or set(args) - VIEW_KEYS):
                        breach("First call is not the exact forced-full instruction view")
                    continue
                if not bootstrap:
                    breach("A tool call preceded verified bootstrap completion")
                if not core_released:
                    breach("Evidence/tool access preceded explicit core-release authorization")
                if completed:
                    breach("Tool call after task completion")
                elif len(sends) >= 2 and name != "task_complete":
                    breach("Tool call after the completion message")
                if len(sends) == 1 and not phase2:
                    breach("Tool call during the phase gap")
                if name in ("create", "apply_patch"):
                    record["arguments"] = "<report write>"
                if name == "view":
                    if not isinstance(args, dict):
                        breach("Unsupported view argument shape")
                        continue
                    path = args.get("path")
                    record["path"] = path
                    forced = args.get("forceReadLargeFiles", None)
                    if args.get("view_range") is not None or set(args) - VIEW_KEYS or forced not in (None, True):
                        breach("View is not a complete read without view_range")
                    if path == report and forced is not True:
                        breach("Report readback is not a forced full read")
                    if path in core_paths:
                        position = core_paths.index(path) + 1
                        record["role"] = f"core-{position}"
                        if position > seen_core + 1 or (position > 1 and core_paths[position - 2] not in covered):
                            breach("Core chain read out of order or before previous coverage")
                        seen_core = max(seen_core, position)
                    elif path in extension_paths:
                        position = extension_paths.index(path) + 1
                        record["role"] = f"extension-{position}"
                        if (not phase2 or position > seen_extension + 1
                                or (position > 1 and extension_paths[position - 2] not in covered)):
                            breach("Extension read before phase 2 or out of order")
                        seen_extension = max(seen_extension, position)
                    elif path == report:
                        readbacks += 1
                        record["role"] = "report-readback"
                        if not phase2 or writes != 1 or readbacks != 1:
                            breach("Invalid report readback")
                    elif path == config["prompt"]:
                        breach("Instruction file re-read")
                    else:
                        breach(f"Out-of-scope view: {path}")
                elif name == "web_fetch":
                    fetches += 1
                    url = args.get("url", "") if isinstance(args, dict) else ""
                    record["url"] = url
                    if fetches > fetch_limit:
                        breach(f"web_fetch beyond the configured limit of {fetch_limit} (over-cap fetch)")
                    elif not isinstance(args, dict) or not isinstance(url, str) or not public_https(url):
                        breach("Invalid, non-public or over-cap fetch")
                    else:
                        announcement = text
                        if url not in announcement or len(re.sub(r"[\W_]", "", announcement.replace(url, ""))) < 3:
                            breach("Fetch lacks a public same-response URL and reason")
                    if not api:
                        notes.append(f"Fetch {cid} lacks apiCallId grouping; adjudicate its announcement")
                elif name in ("create", "apply_patch"):
                    writes += 1
                    text_written = None
                    if name == "create":
                        if (isinstance(args, dict) and set(args) <= {"path", "file_text"}
                                and args.get("path") == report and isinstance(args.get("file_text"), str)):
                            text_written = args["file_text"]
                    elif isinstance(args, str):
                        text_written = patch_text(args, report)
                    if text_written is None:
                        breach("Write is not exactly one complete creation of the report")
                    else:
                        record["writtenSha256"] = digest(text_written.encode("utf-8"))
                        record["writtenChars"] = len(text_written)
                    if writes == 1:
                        written_text = text_written
                    if writes != 1 or not phase2 or extension is None or not chain_paths <= covered:
                        breach("Report write before complete required coverage, or a repeated write")
                elif name == "send_session_message":
                    message = args.get("message") if isinstance(args, dict) else None
                    sends.append(message if isinstance(message, str) else "")
                    record["message"] = message
                    if not isinstance(args, dict) or not isinstance(message, str):
                        breach("Malformed coordinator message")
                        continue
                    extra = set(args) - {"session_id", "message"}
                    if extra:
                        notes.append(f"Message {cid} carried extra arguments {sorted(extra)}; adjudicate")
                    if args.get("session_id") != coordinator or len(sends) > 2:
                        breach("Wrong message recipient or excessive messages")
                    if len(sends) == 1:
                        if not set(core_paths) <= covered:
                            breach("Selection sent before complete core coverage")
                        selection = validate_selection(message, reference, optional_units)
                        breaches.extend("Selection: " + error for error in selection["errors"])
                        if phase1_text is not None and message != phase1_text:
                            breach("Phase-1 message differs from the frozen list")
                    elif len(sends) == 2:
                        if (not phase2 or writes != 1 or not readback_ok
                                or COMPLETION_ENUM.fullmatch(message) is None):
                            breach("Invalid completion message or premature completion")
                elif name == "task_complete":
                    if not phase2 or len(sends) != 2:
                        breach("Premature task completion")
                    completed = True
                elif (name == "web_search" or "browser" in name.lower()
                      or (name == "open_canvas" and isinstance(args, dict) and args.get("canvasId") == "browser")):
                    breach(f"Web search or browser call: {name}")
                else:
                    breach(f"Disallowed tool: {name}")
        elif kind == "tool.execution_start":
            cid = data.get("toolCallId")
            record = pending.get(cid)
            if record is None:
                breach("Tool execution started without an admitted request")
                continue
            if str(data.get("toolName", record["name"])).removeprefix("functions.") != record["name"]:
                breach(f"Executed tool differs from the request: {cid}")
            if "arguments" in data and arguments(data["arguments"]) != requested_args[cid]:
                breach(f"Executed arguments differ from the request: {cid}")
            if data.get("model") and not str(data["model"]).lower().startswith(family):
                breach(f"Unexpected executing model: {data['model']}")
        elif kind == "tool.execution_complete":
            cid = data.get("toolCallId")
            record = pending.pop(cid, None)
            if record is None:
                breach("Unmatched tool completion")
                continue
            last_complete = index
            record["success"] = data.get("success")
            result = data.get("result")
            returned = result.get("content") if isinstance(result, dict) else None
            if data.get("success") is not True:
                if record.get("role") == "bootstrap":
                    breach("Bootstrap read failed")
                else:
                    notes.append(f"Failed {record['name']} call {cid}; adjudicate")
                continue
            if record["name"] != "view":
                continue
            path = record.get("path")
            if record.get("role") == "bootstrap":
                if returned == prompt:
                    bootstrap = True
                else:
                    breach("Bootstrap read is not byte-equal to the frozen prompt")
            elif path in chain_paths:
                if returned == Path(path).read_bytes().decode("utf-8"):
                    covered.add(path)
                else:
                    breach("View output differs from the complete frozen segment: " + path)
            elif path == report:
                disk = Path(report).read_bytes().decode("utf-8") if Path(report).is_file() else None
                if returned is not None and returned == disk:
                    readback_ok = True
                else:
                    breach("Report readback differs from the report on disk")
    if missing_api:
        notes.append("Some assistant messages lack apiCallId; response grouping needs adjudication")
    actual = sorted({m["responseModel"] for m in usage_models if m["responseModel"]})
    idle = last_turn_end > max(last_complete, last_user) and not pending
    report_mode = None
    if final:
        if not readback_ok:
            breach("Final audit lacks a verified report readback")
        if len(sends) < 2:
            breach("Final audit lacks the completion message")
        if (not bootstrap or not bootstrap_reply or not core_released or pending or len(sends) != 2
                or writes != 1 or not readback_ok or not phase2):
            breach("Incomplete two-phase execution")
        if extension is None or not chain_paths <= covered:
            breach("Incomplete required read coverage")
        if not actual:
            breach("Actual response model was not verified")
        if phase1_text is None or phase2_text is None:
            breach("Final audit lacks the frozen phase messages")
        disk = Path(report).read_bytes().decode("utf-8") if Path(report).is_file() else None
        if written_text is not None and disk is not None:
            if disk == written_text:
                report_mode = "exact"
            elif disk.replace("\r\n", "\n") == written_text.replace("\r\n", "\n"):
                report_mode = "line-endings-normalized"
                notes.append("Report on disk equals its single write after CRLF normalization")
            else:
                breach("Report on disk differs from its single write")
        elif writes == 1:
            breach("Report on disk is missing or its write was malformed")
    if breaches:
        status = "VOID"
    elif record_incomplete or (final and not idle):
        status = "PENDING"
        notes.append("Record still live or reviewer turn not ended; re-run the audit later")
    elif unexpected_users:
        status = "HOLD"
    elif final:
        status = "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
    elif len(sends) == 1 and not phase2 and bootstrap and bootstrap_reply and core_released and actual and idle:
        status = "PHASE1_READY"
    else:
        status = "PENDING"
    return {
        "status": status, "breaches": breaches, "notes": notes, "bootstrapVerified": bootstrap,
        "bootstrapReplyVerified": bootstrap_reply, "coreReleaseVerified": core_released,
        "actualResponseModels": actual, "assistantModels": sorted(assistant_models),
        "modelRecords": usage_models, "reviewerIdle": idle, "recordIncomplete": record_incomplete,
        "unexpectedUserMessages": unexpected_users,
        "coreRead": len(set(core_paths) & covered), "coreRequired": len(core_paths),
        "extensionRead": len(set(extension_paths) & covered), "extensionRequired": len(extension_paths),
        "writes": writes, "readbacks": readbacks, "readbackVerified": readback_ok,
        "reportBinding": report_mode, "fetches": fetches, "maxWebFetches": fetch_limit, "messages": sends,
        "phase1ListSha256": digest(sends[0].encode("utf-8")) if sends else None,
        "calls": calls,
        "acceptanceLimit": "Mechanism audit only. Every report claim and ambiguous response grouping still requires full-record adjudication.",
    }



def audit(events, config, core, reference, extension=None, phase1_text=None, phase2_text=None,
          final=False, record_incomplete=False, session=None):
    from b134_capacity import load_forecast, validate_capacity_config
    from b134_runtime import context_telemetry, validate_prepared_extension
    from b134_common import CAPACITY, CAPACITY_SHA, HERE as LIFECYCLE, frozen, sha
    if config.get("capacityForecastSha256") != sha(frozen(CAPACITY, CAPACITY_SHA)):
        raise IntegrityError("Measured capacity binding changed/missing")
    validate_capacity_config(config)
    forecast = load_forecast()
    result = audit_base(events, config, core, reference, extension, phase1_text, phase2_text,
                        final, record_incomplete)
    result["run"] = config["run"]
    result["capacityTelemetry"] = context_telemetry(
        events, forecast, config["expectedFamily"], session)
    if result["capacityTelemetry"]["status"] != "PASS":
        result["breaches"].extend(result["capacityTelemetry"]["errors"])
        result["status"] = ("HOLD_CONTEXT_COMPACTED" if result["capacityTelemetry"]["compactions"]
                            else "HOLD_CONTEXT_UNVERIFIED")
    if extension is not None:
        if phase1_text is None or phase2_text is None:
            raise IntegrityError("Final audit lacks frozen independent phase messages")
        phase1_record = json.loads(frozen(LIFECYCLE / (config["run"] + "-phase1.json")))
        original = Path(phase1_record["auditDir"]) / "audit.json"
        result["extensionEvidenceCapacity"] = validate_prepared_extension(
            config, extension, phase1_text, phase2_text, original, require_fresh_report=not final)
    return result


def require_frozen(path, expected=None):
    path = Path(path)
    if not path.is_file():
        raise IntegrityError(f"Missing frozen input: {path}")
    if path.stat().st_mode & stat.S_IWRITE:
        raise IntegrityError(f"Frozen input is writable: {path}")
    data = path.read_bytes()
    if expected is not None and digest(data) != expected:
        raise IntegrityError(f"Frozen input hash changed: {path}")
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--events-file", type=Path, help="Re-audit a preserved snapshot instead of the live record")
    parser.add_argument("--extension", type=Path)
    parser.add_argument("--phase1-list", type=Path)
    parser.add_argument("--phase2-message", type=Path)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[0-9A-Za-z-]{8,64}", args.session):
        parser.error("Invalid session identifier")
    if args.phase2_message and not (args.extension and args.phase1_list):
        parser.error("Phase-2 audits require --extension and --phase1-list")
    if args.final and not args.phase2_message:
        parser.error("Final audits require --extension, --phase1-list and --phase2-message")
    config_raw = require_frozen(args.config)
    config = json.loads(config_raw)
    missing = [key for key in REQUIRED_CONFIG if key not in config]
    if missing or not re.fullmatch(r"[0-9A-Za-z-]+", str(config.get("run", ""))):
        parser.error(f"Invalid config; missing {missing}")
    preflight = json.loads(frozen(PREFLIGHT, PREFLIGHT_SHA))
    spec = preflight.get("runs", {}).get(config["expectedFamily"])
    if (preflight.get("status") != "PASS_MEASURED_CAPACITY_NOT_REVIEWER_ADMISSION"
            or spec is None or spec.get("run") != config["run"]
            or Path(spec["auditConfig"]["path"]).resolve() != args.config.resolve()
            or digest(config_raw) != spec["auditConfig"]["sha256"]
            or config.get("candidate") != CANDIDATE or config.get("base") != BASE
            or config.get("publishedBaseline") != "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
            or config.get("role") != "replacement-independent"
            or config.get("originalReviewerConfirmation") is not False
            or config.get("originalSession") != INITIALS[config["expectedFamily"]]["session"]
            or config.get("report") != spec["report"]
            or config.get("kickoff") != spec["kickoff"]
            or config.get("kickoffText") != spec["kickoffText"]
            or config.get("prompt") != spec["prompt"]["path"]
            or config.get("promptSha256") != spec["prompt"]["sha256"]
            or config.get("completionContract") != COMPLETION_CONTRACT
            or config.get("completionContractScope") != "coordinator-tool-message-only"
            or config.get("reportStructureContract") != "report-structure-v1"
            or config.get("reportStructureChecker") != str(PROTOCOL / "check-report-structure-b134-013.py")
            or config.get("coreManifest") != str(CORE)
            or config.get("coreManifestSha256") != CORE_SHA
            or config.get("capacityForecastSha256") != CAPACITY_SHA
            or config.get("packetInventorySha256") != "adeac0009e52039a57fd3121a45f0e91eb697a6f35b131db0517922f3d1b540c"
            or config.get("losslessVerificationSha256") != "7ad06c861b4af2b2f722e54e6e200531919fb6cad6f8cd81541ea2d291571577"):
        raise IntegrityError("Config is not bound to the immutable preflight/core/capacity")
    if (not isinstance(config["files"], list) or not config["files"]
            or len({item.get("path") for item in config["files"] if isinstance(item, dict)}) != len(config["files"])
            or not any(item.get("path") == config["reportStructureChecker"]
                       and item.get("sha256") for item in config["files"] if isinstance(item, dict))):
        raise IntegrityError("Frozen input inventory or report checker binding is incomplete")
    for item in config["files"]:
        require_frozen(item["path"], item["sha256"])
    prompt_text = require_frozen(config["prompt"], config["promptSha256"]).decode("utf-8")
    if config["coreReleaseMessage"] != prompt_core_release_message(prompt_text):
        raise IntegrityError("Configured core release message differs from the frozen prompt")
    verify_core()
    frozen(CAPACITY, CAPACITY_SHA)
    verify_packet()
    root = OUTPUT_BASE / config["run"] / (
        "audit-" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%f"))
    root.mkdir(parents=True)
    source = args.events_file or Path.home() / ".copilot" / "session-state" / args.session / "events.jsonl"
    result = {"session": args.session, "eventsSource": str(source), "final": args.final}
    try:
        record_bytes = source.read_bytes()
    except OSError as exc:
        record_bytes = None
        result.update(status="AUDIT_ERROR", error=f"Cannot read record: {exc}")
    if record_bytes is not None:
        with (root / "events.jsonl").open("xb") as stream:
            stream.write(record_bytes)
        result.update(eventsSha256=digest(record_bytes), eventsBytes=len(record_bytes))
        try:
            bootstrap, authorization, snapshot_raw, snapshot_count, authorization_sha = \
                validate_bootstrap_authorization(config, args.session, config_raw)
            if not record_bytes.startswith(snapshot_raw):
                raise IntegrityError("Live event stream does not preserve the exact bootstrap prefix")
            result["bootstrapRecord"] = {
                "path": config["bootstrapRecordPath"],
                "sha256": digest(require_frozen(config["bootstrapRecordPath"])),
            }
            result["coreAuthorization"] = {
                "path": config["coreAuthorizationPath"], "sha256": authorization_sha,
            }
            result["bootstrapEventSnapshot"] = {
                "path": bootstrap["eventSnapshotPath"],
                "sha256": bootstrap["eventSnapshotSha256"],
            }
            config["_bootstrapSnapshotEventCount"] = snapshot_count
            config["_bootstrapSnapshotSha256"] = bootstrap["eventSnapshotSha256"]
            config["_coreAuthorizationSha256"] = authorization_sha
            for item in config["files"]:
                require_frozen(item["path"], item["sha256"])
            core = json.loads(require_frozen(config["coreManifest"]))
            for segment in core["segments"]:
                require_frozen(segment["path"], segment["sha256"])
            reference = json.loads(require_frozen(config["reference"]))
            extension = None
            if args.extension:
                extension = json.loads(require_frozen(args.extension))
                for segment in extension["segments"]:
                    require_frozen(segment["path"], segment["sha256"])
            phase1 = require_frozen(args.phase1_list).decode("utf-8") if args.phase1_list else None
            phase2 = require_frozen(args.phase2_message).decode("utf-8") if args.phase2_message else None
            events, incomplete = load_events(record_bytes)
            result["eventsCount"] = len(events)
            result.update(audit(events, config, core, reference, extension, phase1, phase2,
                                args.final, incomplete, args.session))
        except IntegrityError as exc:
            result.update(status="VOID", breaches=[str(exc)],
                          quarantine="No observation from this pass may become evidence or a later hint.")
        except Exception as exc:  # The snapshot is preserved; no verdict is drawn from a failed audit.
            result.update(status="AUDIT_ERROR", error=f"{type(exc).__name__}: {exc}",
                          traceback=traceback.format_exc())
    if result.get("status") == "PHASE1_READY":
        with (root / "phase1-list.txt").open("xb") as stream:
            stream.write(result["messages"][0].encode("utf-8"))
    with (root / "audit.json").open("xb") as stream:
        stream.write((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    for path in root.iterdir():
        path.chmod(stat.S_IREAD)
    summary = {key: result.get(key) for key in (
        "status", "breaches", "notes", "error", "actualResponseModels", "reviewerIdle", "coreRead",
        "coreRequired", "extensionRead", "extensionRequired", "reportBinding", "eventsSha256")}
    print(json.dumps(summary, ensure_ascii=False))
    print("Audit: " + str(root / "audit.json"))
    return {"VOID": 1, "AUDIT_ERROR": 2}.get(result.get("status"), 0)


if __name__ == "__main__":
    sys.exit(main())
