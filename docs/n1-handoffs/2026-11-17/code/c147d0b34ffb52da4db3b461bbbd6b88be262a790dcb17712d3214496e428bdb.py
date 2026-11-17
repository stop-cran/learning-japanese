"""Fresh B134 reviewer bootstrap and phase-boundary gate; no session is launched."""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review")
FINAL = ROOT / "fresh-independent-002" / "projected-successor-007"
PROTOCOL = FINAL / "protocol-002"
CAPACITY = FINAL / "capacity-measurement-001.json"
sys.path.insert(0, str(ROOT.parents[1] / "review-tools"))
from common import write_frozen
COORDINATOR = "2451b10d-02a9-46ab-82d5-d90993f0cb8b"
PROFILES = {
    "claude": {"selectedModel": "claude-opus-5.5", "maxPromptTokens": 952000, "prePhase2Gate": 740000},
    "gpt": {"selectedModel": "gpt-6.1-sol", "maxPromptTokens": 922000, "prePhase2Gate": 710000},
}
PRECEDENT_PROTOCOL = ROOT / "neutral-preparation-001" / "projected-successor-001" / "protocol-001"
sys.path.insert(0, str(PRECEDENT_PROTOCOL))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def frozen(path):
    return Path(path).read_bytes()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_events(path):
    raw = frozen(path)
    return [json.loads(line) for line in raw.decode("utf-8").splitlines()], raw


def event_data(event):
    data = event.get("data") or {}
    require(isinstance(data, dict), "Invalid event data")
    return data


def validate_runtime(events, family):
    profile = PROFILES[family]
    starts, usages, compactions = [], [], []
    for event in events:
        kind, data = event.get("type"), event_data(event)
        if kind == "session.start":
            starts.append(data)
        elif kind == "session.usage_record":
            usage = data.get("usage")
            require(isinstance(usage, dict), "Missing actual session usage")
            usages.append(usage)
        elif isinstance(kind, str) and kind.startswith("session.compaction"):
            compactions.append(kind)
    require(len(starts) == 1, "Expected exactly one actual session.start")
    require(starts[0].get("selectedModel") == profile["selectedModel"],
            "Actual selectedModel differs from required profile")
    require(starts[0].get("contextTier") == "long_context",
            "Actual contextTier is not explicitly long_context")
    require(usages, "No actual usage telemetry")
    for usage in usages:
        require(type(usage.get("inputTokens")) is int and usage["inputTokens"] >= 0,
                "Missing or invalid actual inputTokens")
        require(type(usage.get("maxPromptTokens")) is int
                and usage["maxPromptTokens"] == profile["maxPromptTokens"],
                "Actual maxPromptTokens differs from the exact profile")
        require(usage["inputTokens"] <= profile["maxPromptTokens"],
                "Observed input exceeds actual maxPromptTokens")
        for key in ("model", "responseModel"):
            value = usage.get(key)
            require(value is None or (isinstance(value, str)
                    and value.lower().startswith(family)), "Mixed or invalid usage model family")
    require(not compactions, "Context compaction invalidates reviewer admission")
    return {
        "selectedModel": starts[0]["selectedModel"], "contextTier": starts[0]["contextTier"],
        "maxPromptTokens": profile["maxPromptTokens"],
        "actualPeakInputTokens": max(row["inputTokens"] for row in usages),
        "usageRecords": len(usages), "compactions": compactions,
    }


def verify_bootstrap(events, event_bytes, family, config):
    """Accept only a finished prompt-read turn, before any evidence chain is delivered."""
    require(config.get("expectedFamily") == family, "Run family/config mismatch")
    profile = PROFILES[family]
    require(config.get("contextProfile") == {
        **profile, "contextTier": "long_context"
    }, "Frozen config profile differs from the exact selected-model/context/usage gate")
    telemetry = validate_runtime(events, family)
    prompt_path = Path(config["prompt"])
    prompt = frozen(prompt_path).decode("utf-8")
    kickoff = frozen(config["kickoff"]).decode("utf-8")
    user_rows, requests, completions, turn_ends = [], [], [], []
    for index, event in enumerate(events):
        kind, data = event.get("type"), event_data(event)
        if kind == "user.message":
            user_rows.append((index, data))
        elif kind == "assistant.message":
            for request in data.get("toolRequests") or []:
                require(isinstance(request, dict), "Invalid bootstrap tool request")
                requests.append((index, data, request))
        elif kind == "tool.execution_complete":
            completions.append((index, data))
        elif kind == "assistant.turn_end":
            turn_ends.append(index)
    require(len(user_rows) == 1 and user_rows[0][1].get("content") == kickoff,
            "Bootstrap must contain only the exact frozen kickoff message")
    require(user_rows[0][1].get("source") == "agent-" + COORDINATOR,
            "Kickoff provenance is not the coordinator")
    require(len(requests) == 1, "Bootstrap permits exactly one tool call")
    request_index, _, request = requests[0]
    args = request.get("arguments")
    if isinstance(args, str):
        args = json.loads(args)
    require(request.get("name", "").removeprefix("functions.") == "view"
            and isinstance(args, dict) and args.get("path") == str(prompt_path)
            and args.get("forceReadLargeFiles") is True
            and args.get("view_range") is None
            and not (set(args) - {"path", "forceReadLargeFiles", "view_range"}),
            "Bootstrap call must be one full, unbounded read of the frozen prompt")
    require(request_index > user_rows[0][0], "Prompt read preceded the coordinator kickoff")
    call_id = request.get("toolCallId")
    require(call_id and len(completions) == 1, "Bootstrap completion is missing or ambiguous")
    completion_index, completion = completions[0]
    require(completion_index > request_index and completion.get("toolCallId") == call_id
            and completion.get("success") is True,
            "Prompt read did not complete successfully")
    if completion.get("toolName") is not None:
        require(completion["toolName"].removeprefix("functions.") == "view",
                "Executed bootstrap tool differs from the request")
    executed_args = completion.get("arguments")
    if executed_args is not None:
        if isinstance(executed_args, str):
            executed_args = json.loads(executed_args)
        require(executed_args == args, "Executed prompt-read arguments differ")
    result = completion.get("result")
    returned = result.get("content") if isinstance(result, dict) else None
    require(returned == prompt, "Bootstrap returned bytes differ from the frozen prompt")
    require(turn_ends and turn_ends[-1] > completion_index,
            "Bootstrap must end and wait after the prompt read")
    require(not any(index > completion_index and event.get("type") == "user.message"
                    for index, event in enumerate(events)),
            "Additional user message occurred before coordinator telemetry verification")
    return {
        "status": "PASS_BOOTSTRAP_WAIT",
        "family": family,
        "runtime": telemetry,
        "prompt": {"path": str(prompt_path), "sha256": sha(prompt.encode("utf-8"))},
        "kickoffSha256": sha(kickoff.encode("utf-8")),
        "eventsSha256": sha(event_bytes),
        "firstAction": "one forced full prompt read",
        "coreChainDelivered": False,
        "nextAction": "coordinator verifies this live session's actual telemetry before core delivery",
    }


def authorize_core(bootstrap_record, events_path):
    """Refuse the core chain unless the frozen capacity forecast and bootstrap both pass."""
    capacity = json.loads(frozen(CAPACITY))
    require(bootstrap_record.get("status") == "PASS_BOOTSTRAP_WAIT",
            "Verified prompt-only bootstrap required")
    events, raw = read_events(events_path)
    require(sha(raw) == bootstrap_record.get("eventsSha256"),
            "Live bootstrap event snapshot changed")
    require(capacity.get("decision") == "PASS_ESTIMATE"
            and capacity.get("chosenCaps") is not None
            and capacity.get("completeRecordTrial", {}).get("trials"),
            "HOLD_ESTIMATE: current packet has no passing D/E cap; core delivery is prohibited")
    startup = next((row for row in capacity["trials"] if row["caps"] == capacity["chosenCaps"]), None)
    require(startup is not None and startup["outcome"] == "PASS_ESTIMATE"
            and startup["startupForecast"] <= capacity["startupGate"],
            "Capacity record does not prove a passing startup forecast")
    telemetry = validate_runtime(events, bootstrap_record["family"])
    require(telemetry == bootstrap_record["runtime"], "Actual runtime telemetry changed after bootstrap")
    first = json.loads(frozen(FINAL / "fresh-independent-core-001.json"))["segments"][0]["path"]
    return {"status": "PASS_CORE_DELIVERY", "message": first,
            "coreManifest": str(FINAL / "fresh-independent-core-001.json"),
            "coreManifestSha256": sha(frozen(FINAL / "fresh-independent-core-001.json"))}


def audit_core_boundary(events, family, config, core, reference, extension=None,
                        phase1_text=None, phase2_text=None, final=False, record_incomplete=False):
    """Audit the prompt-only turn and the exact later core-start before using B134's two-phase audit."""
    require(config.get("expectedFamily") == family, "Audit family/config mismatch")
    validate_runtime(events, family)
    prompt = frozen(config["prompt"]).decode("utf-8")
    kickoff = frozen(config["kickoff"]).decode("utf-8")
    first_segment = core["segments"][0]["path"]
    user_rows = [(i, event_data(event)) for i, event in enumerate(events)
                 if event.get("type") == "user.message"]
    required_users = [kickoff, first_segment] + ([phase2_text] if final else [])
    require([row.get("content") for _, row in user_rows] == required_users,
            "User message sequence differs from kickoff, core-start, and optional phase two")
    require(user_rows[0][1].get("source") == "agent-" + COORDINATOR,
            "Kickoff provenance is not the coordinator")
    require(user_rows[1][1].get("source") == "agent-" + COORDINATOR,
            "Core-start provenance is not the coordinator")

    prompt_completion = next((i for i, event in enumerate(events)
                              if event.get("type") == "tool.execution_complete"
                              and (event_data(event).get("result") or {}).get("content") == prompt), None)
    require(prompt_completion is not None, "Frozen bootstrap prompt read is missing")
    bootstrap_end = next((i for i in range(prompt_completion + 1, len(events))
                          if events[i].get("type") == "assistant.turn_end"), None)
    require(bootstrap_end is not None and user_rows[1][0] > bootstrap_end,
            "Core chain was delivered before the prompt-only bootstrap turn ended")
    prefix = events[:bootstrap_end + 1]
    prefix_bytes = b"".join((json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8")
                            for event in prefix)
    verify_bootstrap(prefix, prefix_bytes, family, config)

    core_message_index = user_rows[1][0]
    core_views = []
    for index, event in enumerate(events):
        if event.get("type") != "assistant.message":
            continue
        for request in event_data(event).get("toolRequests") or []:
            if bootstrap_end < index < core_message_index:
                raise ValueError("A tool call occurred between bootstrap wait and core delivery")
            name = request.get("name", "").removeprefix("functions.")
            args = request.get("arguments")
            if isinstance(args, str):
                args = json.loads(args)
            path = args.get("path") if isinstance(args, dict) else None
            if name == "view" and isinstance(path, str) and path in {
                    segment["path"] for segment in core["segments"]}:
                core_views.append((index, path))
            if index < core_message_index and name != "view":
                raise ValueError("Non-read tool action occurred before core delivery")
    require(core_views and core_views[0][1] == first_segment
            and core_views[0][0] > core_message_index,
            "First core read does not follow the exact core-start message")
    require(not any(index < core_message_index for index, _ in core_views),
            "A core segment was read before coordinator telemetry verification")
    prompt_views = []
    for event in events:
        if event.get("type") == "assistant.message":
            for request in event_data(event).get("toolRequests") or []:
                args = request.get("arguments")
                if isinstance(args, str):
                    args = json.loads(args)
                if isinstance(args, dict) and args.get("path") == str(Path(config["prompt"])):
                    prompt_views.append(args)
    require(len(prompt_views) == 1, "Prompt may be read only once in the full reviewer run")

    filtered = [event for index, event in enumerate(events) if index != core_message_index]
    spec = importlib.util.spec_from_file_location(
        "b134_legacy_audit_for_fresh_002", PRECEDENT_PROTOCOL / "audit-review-b134-001.py")
    auditor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(auditor)
    legacy = auditor.audit_base(filtered, config, core, reference, extension,
                                phase1_text, phase2_text, final, record_incomplete)
    legacy["bootstrapBoundaryVerified"] = True
    legacy["coreDeliveryMessageSha256"] = sha(first_segment.encode("utf-8"))
    return legacy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    boot = sub.add_parser("bootstrap")
    boot.add_argument("--family", choices=tuple(PROFILES), required=True)
    boot.add_argument("--events", type=Path, required=True)
    boot.add_argument("--config", type=Path, required=True)
    boot.add_argument("--output", type=Path, required=True)
    audit = sub.add_parser("audit-boundary")
    audit.add_argument("--family", choices=tuple(PROFILES), required=True)
    audit.add_argument("--events", type=Path, required=True)
    audit.add_argument("--config", type=Path, required=True)
    audit.add_argument("--core", type=Path, required=True)
    audit.add_argument("--reference", type=Path, required=True)
    core = sub.add_parser("authorize-core")
    core.add_argument("--bootstrap", type=Path, required=True)
    core.add_argument("--events", type=Path, required=True)
    args = parser.parse_args()
    if args.action == "bootstrap":
        events, raw = read_events(args.events)
        result = verify_bootstrap(events, raw, args.family, json.loads(frozen(args.config)))
        record = write_frozen(args.output, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print(json.dumps(record, ensure_ascii=False))
    elif args.action == "audit-boundary":
        events, _ = read_events(args.events)
        config, core, reference = (json.loads(frozen(path)) for path in
                                   (args.config, args.core, args.reference))
        print(json.dumps(audit_core_boundary(events, args.family, config, core, reference),
                         ensure_ascii=False))
    else:
        record = json.loads(frozen(args.bootstrap))
        print(json.dumps(authorize_core(record, args.events), ensure_ascii=False))


if __name__ == "__main__":
    main()
