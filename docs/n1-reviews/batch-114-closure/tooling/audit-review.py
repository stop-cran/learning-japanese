"""Read-only B114 review-run audit. Preserves the raw record before any parsing or verdict.

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

from review_chain import digest, validate_selection

HERE = Path(__file__).resolve().parent
OUTPUT_BASE = HERE
REQUIRED_CONFIG = ("run", "kickoff", "prompt", "report", "coordinator", "expectedFamily",
                   "coreManifest", "reference", "files")
VIEW_KEYS = {"path", "forceReadLargeFiles", "view_range"}
VERDICT = re.compile(r"\b(CLEAN|NEEDS FIX|UNVERIFIED)\b")
HASH_LIKE = re.compile(r"\b[0-9a-fA-F]{32,}\b")


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


def audit(events, config, core, reference, extension=None, phase1_text=None, phase2_text=None,
          final=False, record_incomplete=False):
    breaches, notes, calls, sends = [], [], [], []
    pending, covered, requested_args = {}, set(), {}
    usage_models, assistant_models = [], set()
    core_paths = [segment["path"] for segment in core["segments"]]
    extension_paths = [segment["path"] for segment in (extension or {"segments": []})["segments"]]
    chain_paths = set(core_paths) | set(extension_paths)
    report, coordinator = config["report"], config["coordinator"]
    family = config["expectedFamily"].lower()
    kickoff = Path(config["kickoff"]).read_bytes().decode("utf-8")
    prompt = Path(config["prompt"]).read_bytes().decode("utf-8")
    bootstrap = phase2 = completed = readback_ok = False
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
                    if not isinstance(args, dict) or fetches > 3 or not isinstance(url, str) or not public_https(url):
                        breach("Invalid, non-public or over-cap fetch")
                    else:
                        announcement = response_text[key]
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
                        selection = validate_selection(message, reference)
                        breaches.extend("Selection: " + error for error in selection["errors"])
                        if phase1_text is not None and message != phase1_text:
                            breach("Phase-1 message differs from the frozen list")
                    elif len(sends) == 2:
                        lines = message.rstrip("\r\n").splitlines()
                        if (not phase2 or writes != 1 or not readback_ok or len(lines) != 2
                                or lines[0] != report or not VERDICT.search(lines[1])
                                or HASH_LIKE.search(message)):
                            breach("Invalid completion message or premature completion")
                elif name == "task_complete":
                    if not phase2 or len(sends) != 2:
                        breach("Premature task completion")
                    completed = True
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
        if not bootstrap or pending or len(sends) != 2 or writes != 1 or not readback_ok or not phase2:
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
    elif len(sends) == 1 and not phase2 and bootstrap and actual and idle:
        status = "PHASE1_READY"
    else:
        status = "PENDING"
    return {
        "status": status, "breaches": breaches, "notes": notes, "bootstrapVerified": bootstrap,
        "actualResponseModels": actual, "assistantModels": sorted(assistant_models),
        "modelRecords": usage_models, "reviewerIdle": idle, "recordIncomplete": record_incomplete,
        "unexpectedUserMessages": unexpected_users,
        "coreRead": len(set(core_paths) & covered), "coreRequired": len(core_paths),
        "extensionRead": len(set(extension_paths) & covered), "extensionRequired": len(extension_paths),
        "writes": writes, "readbacks": readbacks, "readbackVerified": readback_ok,
        "reportBinding": report_mode, "fetches": fetches, "messages": sends,
        "phase1ListSha256": digest(sends[0].encode("utf-8")) if sends else None,
        "calls": calls,
        "acceptanceLimit": "Mechanism audit only. Every report claim and ambiguous response grouping still requires full-record adjudication.",
    }


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
    config = json.loads(args.config.read_bytes())
    missing = [key for key in REQUIRED_CONFIG if key not in config]
    if missing or not re.fullmatch(r"[0-9A-Za-z-]+", str(config.get("run", ""))):
        parser.error(f"Invalid config; missing {missing}")
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
                                args.final, incomplete))
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
