"""Read-only B115 confirmation-run audit, single phase. Derived from the B114 confirmation audit.

The completion message must follow the entire-message enum contract: its whole value is exactly CONFIRMED,
NEEDS FIX or UNVERIFIED, optionally followed by one LF or CRLF.

The reviewer session already holds its initial-review history, so the audit covers only the record bytes
after a pre-delivery offset whose prefix hash was frozen before the kickoff was sent. The raw record is
preserved before any parsing or verdict. A mechanically clean final result is only
FINAL_AUDIT_NEEDS_CLAIM_CHECK: every report claim still needs full-record adjudication before acceptance.
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

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from review_chain import digest  # noqa: E402

OUTPUT_BASE = HERE
REQUIRED_CONFIG = ("run", "kickoff", "prompt", "report", "coordinator", "expectedFamily",
                   "chainManifest", "files", "completionContract")
VIEW_KEYS = {"path", "forceReadLargeFiles", "view_range"}
COMPLETION_CONTRACT = "entire-message-enum-v1"
COMPLETION_ENUM = re.compile(r"(?:CONFIRMED|NEEDS FIX|UNVERIFIED)(?:\r?\n)?")


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


def audit(events, config, chain, final=False, record_incomplete=False):
    if config.get("completionContract") != COMPLETION_CONTRACT:
        raise IntegrityError("The B115 confirmation auditor requires its entire-message enum contract")
    breaches, notes, calls, sends = [], [], [], []
    pending, covered, requested_args = {}, set(), {}
    usage_models, assistant_models = [], set()
    chain_paths = [segment["path"] for segment in chain["segments"]]
    report, coordinator = config["report"], config["coordinator"]
    family = config["expectedFamily"].lower()
    kickoff = Path(config["kickoff"]).read_bytes().decode("utf-8")
    prompt = Path(config["prompt"]).read_bytes().decode("utf-8")
    bootstrap = completed = readback_ok = False
    writes = readbacks = fetches = seen = user_count = unexpected_users = 0
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
            else:
                unexpected_users += 1
                notes.append(f"Unexpected user message at event {index}; adjudicate before acceptance")
        elif user_count == 0:
            if kind in ("assistant.message", "tool.execution_start", "tool.execution_complete"):
                breach(f"Activity before the kickoff in the audited slice: {kind} at event {index}")
            continue
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
                record = {"id": cid, "name": name, "event": index,
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
                elif sends and name != "task_complete":
                    breach("Tool call after the completion message")
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
                    if path in chain_paths:
                        position = chain_paths.index(path) + 1
                        record["role"] = f"chain-{position}"
                        if position > seen + 1 or (position > 1 and chain_paths[position - 2] not in covered):
                            breach("Chain read out of order or before previous coverage")
                        if writes:
                            notes.append(f"Chain segment {position} re-viewed after the report write; adjudicate")
                        seen = max(seen, position)
                    elif path == report:
                        readbacks += 1
                        record["role"] = "report-readback"
                        if writes != 1 or readbacks != 1:
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
                    if writes != 1 or not set(chain_paths) <= covered:
                        breach("Report write before complete chain coverage, or a repeated write")
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
                    if args.get("session_id") != coordinator or len(sends) > 1:
                        breach("Wrong message recipient or excessive messages")
                    if writes != 1 or not readback_ok or COMPLETION_ENUM.fullmatch(message) is None:
                        breach("Invalid completion message or premature completion")
                elif name == "task_complete":
                    if len(sends) != 1:
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
    if user_count == 0:
        notes.append("Kickoff not yet present in the audited slice")
    if missing_api:
        notes.append("Some assistant messages lack apiCallId; response grouping needs adjudication")
    actual = sorted({m["responseModel"] for m in usage_models if m["responseModel"]})
    idle = user_count > 0 and last_turn_end > max(last_complete, last_user) and not pending
    report_mode = None
    if final:
        if not bootstrap or pending or len(sends) != 1 or writes != 1 or not readback_ok:
            breach("Incomplete confirmation execution")
        if not set(chain_paths) <= covered:
            breach("Incomplete required chain coverage")
        if not actual:
            breach("Actual response model was not verified")
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
    elif record_incomplete or (final and not idle) or user_count == 0:
        status = "PENDING"
        notes.append("Record still live or reviewer turn not ended; re-run the audit later")
    elif unexpected_users:
        status = "HOLD"
    elif final:
        status = "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
    else:
        status = "PENDING"
    return {
        "status": status, "breaches": breaches, "notes": notes, "bootstrapVerified": bootstrap,
        "actualResponseModels": actual, "assistantModels": sorted(assistant_models),
        "modelRecords": usage_models, "reviewerIdle": idle, "recordIncomplete": record_incomplete,
        "unexpectedUserMessages": unexpected_users,
        "chainRead": len(set(chain_paths) & covered), "chainRequired": len(chain_paths),
        "writes": writes, "readbacks": readbacks, "readbackVerified": readback_ok,
        "reportBinding": report_mode, "fetches": fetches, "messages": sends, "calls": calls,
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
    parser.add_argument("--offset", type=int, required=True, help="Record byte length frozen before delivery")
    parser.add_argument("--prefix-sha256", required=True, help="SHA-256 of the record's first --offset bytes")
    parser.add_argument("--events-file", type=Path, help="Re-audit a preserved snapshot instead of the live record")
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[0-9A-Za-z-]{8,64}", args.session):
        parser.error("Invalid session identifier")
    if args.offset < 0 or not re.fullmatch(r"[0-9a-f]{64}", args.prefix_sha256):
        parser.error("Invalid offset or prefix hash")
    config = json.loads(args.config.read_bytes())
    missing = [key for key in REQUIRED_CONFIG if key not in config]
    if missing or not re.fullmatch(r"[0-9A-Za-z-]+", str(config.get("run", ""))):
        parser.error(f"Invalid config; missing {missing}")
    root = OUTPUT_BASE / config["run"] / (
        "audit-" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%f"))
    root.mkdir(parents=True)
    source = args.events_file or Path.home() / ".copilot" / "session-state" / args.session / "events.jsonl"
    result = {"session": args.session, "eventsSource": str(source), "final": args.final,
              "offset": args.offset, "prefixSha256": args.prefix_sha256}
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
            prefix = record_bytes[:args.offset]
            if (len(record_bytes) < args.offset or digest(prefix) != args.prefix_sha256
                    or (args.offset and not prefix.endswith(b"\n"))):
                raise ValueError("Record prefix differs from the pre-delivery snapshot; the slice cannot be bound")
            sliced = record_bytes[args.offset:]
            result.update(sliceSha256=digest(sliced), sliceBytes=len(sliced))
            for item in config["files"]:
                require_frozen(item["path"], item["sha256"])
            chain = json.loads(require_frozen(config["chainManifest"]))
            for segment in chain["segments"]:
                require_frozen(segment["path"], segment["sha256"])
            events, incomplete = load_events(sliced)
            result["eventsCount"] = len(events)
            result.update(audit(events, config, chain, args.final, incomplete))
        except IntegrityError as exc:
            result.update(status="VOID", breaches=[str(exc)],
                          quarantine="No observation from this pass may become evidence or a later hint.")
        except Exception as exc:  # The snapshot is preserved; no verdict is drawn from a failed audit.
            result.update(status="AUDIT_ERROR", error=f"{type(exc).__name__}: {exc}",
                          traceback=traceback.format_exc())
    with (root / "audit.json").open("xb") as stream:
        stream.write((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    for path in root.iterdir():
        path.chmod(stat.S_IREAD)
    summary = {key: result.get(key) for key in (
        "status", "breaches", "notes", "error", "actualResponseModels", "reviewerIdle", "chainRead",
        "chainRequired", "reportBinding", "eventsSha256", "sliceSha256")}
    print(json.dumps(summary, ensure_ascii=False))
    print("Audit: " + str(root / "audit.json"))
    return {"VOID": 1, "AUDIT_ERROR": 2}.get(result.get("status"), 0)


if __name__ == "__main__":
    sys.exit(main())
