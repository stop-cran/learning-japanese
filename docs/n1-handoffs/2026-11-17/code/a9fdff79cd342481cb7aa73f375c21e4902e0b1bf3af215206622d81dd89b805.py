"""Observe, audit and adjudicate B134 reviews; never launches or messages a reviewer."""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path
from b134_common import (
    BASE, CANDIDATE, COORDINATOR, CORE, CORE_SHA, CAPACITY_SHA, HERE, PACKET, PROOFS,
    PROTOCOL, REPO, ROOT, WS,
    freeze_json, frozen, require, sha, start_guard, validate_report_destination, verify_packet, write_frozen)
from b134_capacity import load_forecast, startup_bound, validate_capacity_config
sys.path.insert(0, str(HERE / "tools"))
sys.path.insert(0, str(WS / "review-tools"))
from verify_b134_sources import FINGERPRINT, Git, OWNER
from b134_initial_records import INITIALS
from b134_review_history import FAILED_SESSION

PREFLIGHT = HERE / "audit-configs-013" / "preflight.json"
PREFLIGHT_SHA = "5419c88d609c7b8e89bef8080311c7a7987bb6f77ec749df8e27e31398067abe"
AUDIT_PATH = PROTOCOL / "audit-review-b134-011.py"
AUDIT_SHA = "c54c76d0433c26460058676e9ad2bd568c4c3518e5d3dab81382c3cea237fdf6"
BOOTSTRAP_RESPONSE = "PROMPT READ; WAITING FOR COORDINATOR CORE RELEASE."
RUNNER = ROOT / "guarded-test-v3.py"
RUNNER_SHA = "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
def now():
    return datetime.datetime.now(datetime.timezone.utc)


def child(*args):
    """Pinned runner, uniquely named output, bounded waits and inherited child PYTHONPATH."""
    frozen(RUNNER, RUNNER_SHA)
    cleanup_spec = __import__("importlib.util", fromlist=["spec_from_file_location"])
    spec = cleanup_spec.spec_from_file_location("b134_runner_cleanup", RUNNER)
    cleanup = cleanup_spec.module_from_spec(spec)
    spec.loader.exec_module(cleanup)
    output = ROOT / ("b134-lifecycle-execution-" + uuid.uuid4().hex)
    command = [sys.executable, "-B", str(RUNNER), str(output), sys.executable, "-B", *map(str, args)]
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
           "PYTHONPATH": os.pathsep.join((str(PROTOCOL), str(WS / "review-tools"),
                                         os.environ.get("PYTHONPATH", "")))}
    guard, _ = start_guard("B134 lifecycle child")
    process = None
    try:
        process = subprocess.Popen(command, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        while True:
            guard.check()
            try:
                stdout, stderr = process.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                continue
        receipt_raw = (output / "receipt.json").read_bytes()
        log = (output / "output.log").read_bytes()
        receipt = json.loads(receipt_raw)
        require(receipt["runnerSha256"] == RUNNER_SHA and receipt["logSha256"] == sha(log)
                and receipt["cleanupError"] is None and not receipt["memory"]["breach"]
                and receipt["childExitCodeAfterCleanup"] == receipt["exitCode"]
                and process.returncode == (0 if receipt["exitCode"] == 0 else 1),
                "Guarded child integrity/resource failure")
        for name, raw in (("runner-stdout.log", stdout), ("runner-stderr.log", stderr)):
            write_frozen(output / "captured" / name, raw)
        return receipt["exitCode"], log.decode("utf-8"), str(output)
    finally:
        cleanup.stop_child(process)
        for name in ("output.log", "receipt.json"):
            path = output / name
            if path.exists():
                path.chmod(0o444)
        require(not guard.finish()["breach"], "Lifecycle child RAM breach")


def inputs(family, fresh_report=True, require_estimate=True):
    preflight = json.loads(frozen(PREFLIGHT, PREFLIGHT_SHA))
    require(preflight["order"] == ["claude", "gpt"]
            and set(preflight["runs"]) == {"claude", "gpt"}, "Reviewer order differs")
    spec = preflight["runs"][family]
    config = json.loads(frozen(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"]))
    require(config["candidate"] == CANDIDATE and config["base"] == BASE
            and config["publishedBaseline"] == "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
            and config["run"] == spec["run"] and config["expectedFamily"] == family
            and config["role"] == "replacement-independent"
            and config["originalReviewerConfirmation"] is False
            and config["originalSession"] == INITIALS[family]["session"]
            and config["report"] == spec["report"]
            and config["kickoff"] == spec["kickoff"]
            and config["kickoffText"] == spec["kickoffText"]
            and config["prompt"] == spec["prompt"]["path"]
            and config["promptSha256"] == spec["prompt"]["sha256"]
            and spec["launch"]["model"] == config["contextProfile"]["selectedModel"]
            and spec["launch"]["contextTier"] == "long_context"
            and config["contextProfile"]["contextTier"] == "long_context",
            "Identity, report, prompt or explicit runtime profile differs")
    require(config.get("completionContract") == "entire-message-enum-v1"
            and config.get("reportStructureContract") == "report-structure-v1"
            and config.get("reportStructureChecker") == str(PROTOCOL / "check-report-structure-b134-011.py"),
            "Frozen report checker or completion contract differs")
    files = config.get("files")
    require(isinstance(files, list) and files
            and all(isinstance(row, dict) and set(row) == {"path", "sha256"}
                    and Path(row["path"]).is_absolute() for row in files)
            and len({row["path"] for row in files}) == len(files)
            and any(row["path"] == config["reportStructureChecker"] for row in files),
            "Frozen input inventory is incomplete or ambiguous")
    for row in config["files"]:
        frozen(row["path"], row["sha256"])
    validate_capacity_config(config)
    forecast = load_forecast()
    bound = startup_bound(forecast, family, len(frozen(config["prompt"], spec["prompt"]["sha256"])))
    if require_estimate:
        require(bound["status"] == "PASS_ESTIMATE", "Startup capacity estimate failed")
    else:
        require(bound["status"] in ("PASS_ESTIMATE", "HOLD_ESTIMATE"), "Invalid startup estimate")
    if fresh_report:
        validate_report_destination(spec)
    return spec, config


def roster_check(status, roster, session_name, observed):
    rows = status["sessions"]
    require(isinstance(rows, list) and isinstance(roster, list) and rows, "Full status/roster required")
    ids, roster_ids = [r["id"] for r in rows], [r["id"] for r in roster]
    require(len(ids) == len(set(ids)) == status["summary"]["total"] == len(roster_ids)
            and len(roster_ids) == len(set(roster_ids)) and set(ids) == set(roster_ids),
            "Incomplete/mismatched roster")
    age = (now() - observed).total_seconds()
    require(0 <= age < 120, "Admission observation stale or future-dated")
    require(all(row["id"] == COORDINATOR or
                (row["activity"]["status"] == "idle" and not row.get("is_running", False))
                for row in rows), "Another session active or unknown")
    require(not any(row["name"].strip() == session_name for row in rows), "Reviewer session already exists")
    return len(rows)


def admit(family, argument):
    spec, config = inputs(family)
    run = spec["run"]
    if family == "gpt":
        prior = json.loads(frozen(HERE / "N1-B134-CLAUDE-FRESH-002-acceptance.json"))
        require(prior["reviewAccepted"] is True and prior["candidate"] == CANDIDATE
                and prior["run"] == "N1-B134-CLAUDE-FRESH-002", "Fresh Claude review acceptance prerequisite missing")
    request_path = Path(argument)
    request_raw = request_path.read_bytes()
    request = json.loads(request_raw)
    require(set(request) == {"statusPath", "rosterPath", "observedAt"}, "Invalid admission request")
    status_raw, roster_raw = (Path(request[k]).read_bytes() for k in ("statusPath", "rosterPath"))
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    observed = datetime.datetime.fromisoformat(request["observedAt"])
    require(observed.tzinfo is not None, "Observation timezone missing")
    count = roster_check(json.loads(status_raw), roster, spec["launch"]["sessionName"], observed)
    guard, resource = start_guard("B134 reviewer admission")
    try:
        git = Git(REPO, {"path": str(RUNNER), "sha256": RUNNER_SHA}, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate identity changed")
        for name, binding in PROOFS.items():
            proof = json.loads(frozen(binding["path"], binding["sha256"]))
            if name == "source-completeness-verification-008.json":
                require(proof["candidate"] == CANDIDATE and proof["base"] == BASE
                        and proof["publishedBaseline"] == "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
                        and proof["status"] == "PASS_COMPLETE_SOURCE_AND_PACKET_INTEGRITY",
                        "Source completeness proof differs")
            elif name == "packet-verification-001/verification.json":
                require(proof["status"] == "PASS", "Coordinator packet-verification proof differs")
            else:
                require(proof["candidate"] == CANDIDATE and proof["status"] == "PASS",
                        "Signed reconciliation proof differs")
        verify_packet(guard)
        require(resource.available_ram() > 2 * 1024 ** 3, "Insufficient startup RAM")
        validate_report_destination(spec)
        require(0 <= (now() - observed).total_seconds() < 120, "Admission observation expired during verification")
        for p in (HERE / f"{run}-launch.json", HERE / f"{run}-bootstrap.json",
                  HERE / f"{run}-core-authorization.json", HERE / f"{run}-phase1.json",
                  HERE / f"{run}-extension.json", HERE / f"{run}-final.json"):
            require(not p.exists(), "Existing run artifact: " + str(p))
        token = uuid.uuid4().hex
        target = HERE / f"{run}-admission-{token}"
        bindings = {"request": write_frozen(target / "request.json", request_raw),
                    "status": write_frozen(target / "status.json", status_raw),
                    "roster": write_frozen(target / "roster.txt", roster_raw)}
        result = freeze_json(target / "admission.json", {
            "run": run, "batch": 134, "candidate": CANDIDATE, "admitted": True,
            "createdAt": now().isoformat(), "observedAt": observed.isoformat(), "sessionCount": count,
            "preflightSha256": PREFLIGHT_SHA, "auditConfigSha256": spec["auditConfig"]["sha256"],
            "snapshots": bindings, "launch": spec["launch"], "kickoff": spec["kickoffText"],
            "limits": "Fresh startup observation only, not a reservation or content acceptance."})
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Admission RAM breach")


def launch(family, session, admission_path):
    spec, config = inputs(family)
    admission_raw = frozen(admission_path)
    admission = json.loads(admission_raw)
    age = (now() - datetime.datetime.fromisoformat(admission["createdAt"])).total_seconds()
    require(admission_path.parent.parent == HERE and admission_path.name == "admission.json"
            and admission_path.parent.name.startswith(config["run"] + "-admission-")
            and admission["admitted"] is True and admission["run"] == config["run"]
            and admission["candidate"] == CANDIDATE and admission["preflightSha256"] == PREFLIGHT_SHA
            and admission["auditConfigSha256"] == spec["auditConfig"]["sha256"]
            and admission["launch"] == spec["launch"] and admission["kickoff"] == spec["kickoffText"]
            and 0 <= age < 120,
            "Admission missing/stale")
    for binding in admission["snapshots"].values():
        frozen(binding["path"], binding["sha256"])
    events_path = Path.home() / ".copilot" / "session-state" / session / "events.jsonl"
    events = [json.loads(line) for line in events_path.read_bytes().decode("utf-8").splitlines()]
    starts = [e["data"] for e in events if e.get("type") == "session.start"]
    users = [e["data"]["content"] for e in events if e.get("type") == "user.message"]
    require(len(starts) == 1 and starts[0].get("sessionId") == session
            and starts[0].get("selectedModel") == spec["launch"]["model"]
            and starts[0].get("contextTier") == "long_context" and users == [spec["kickoffText"]],
            "Launched session identity, actual context tier or kickoff differs")
    print(json.dumps(freeze_json(HERE / f"{config['run']}-launch.json", {
        "run": config["run"], "session": session, "candidate": CANDIDATE,
        "admission": {"path": str(admission_path), "sha256": sha(admission_raw)},
        "kickoffSha256": sha(spec["kickoffText"].encode("ascii")), "start": starts[0]})))


def prompt_only_events(session, spec, config):
    event_path = Path.home() / ".copilot" / "session-state" / session / "events.jsonl"
    raw = event_path.read_bytes()
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    profile = config["contextProfile"]
    starts = [event["data"] for event in events if event.get("type") == "session.start"]
    users = [event.get("data", {}).get("content") for event in events if event.get("type") == "user.message"]
    tool_starts = [event["data"] for event in events if event.get("type") == "tool.execution_start"]
    tool_completes = [event["data"] for event in events if event.get("type") == "tool.execution_complete"]
    usages = [event.get("data", {}).get("usage") for event in events
              if event.get("type") == "session.usage_record"]
    assistant_final = [event.get("data", {}).get("content") for event in events
                       if event.get("type") == "assistant.message"
                       and not event.get("data", {}).get("toolRequests")]
    requested = [request for event in events if event.get("type") == "assistant.message"
                 for request in event.get("data", {}).get("toolRequests", [])]
    compactions = [event.get("type") for event in events
                   if str(event.get("type", "")).startswith("session.compaction")]
    allowed_types = {"session.start", "user.message", "session.usage_record", "assistant.message",
                     "assistant.turn_end", "tool.execution_start", "tool.execution_complete"}
    request_arguments = requested[0].get("arguments") if len(requested) == 1 else None
    if isinstance(request_arguments, str):
        request_arguments = json.loads(request_arguments)
    require(all(event.get("type") in allowed_types for event in events)
            and len(requested) == 1 and len(users) == 1
            and sum(event.get("type") == "assistant.turn_end" for event in events) == 1
            and events[-1].get("type") == "assistant.turn_end",
            "Bootstrap event snapshot contains activity outside the prompt-only turn")
    require(len(starts) == 1 and starts[0].get("sessionId") == session
            and starts[0].get("selectedModel") == profile["selectedModel"]
            and starts[0].get("contextTier") == "long_context",
            "Bootstrap selected model/contextTier differs")
    require(users == [spec["kickoffText"]], "Bootstrap received an unexpected user message")
    require(len(tool_starts) == len(tool_completes) == 1
            and tool_starts[0].get("toolName") == "view"
            and tool_starts[0].get("arguments", {}).get("path") == config["prompt"]
            and tool_starts[0].get("arguments", {}).get("forceReadLargeFiles") is True
            and tool_starts[0].get("arguments", {}).get("view_range") is None
            and not (set(tool_starts[0].get("arguments", {}))
                     - {"path", "forceReadLargeFiles", "view_range"})
            and tool_starts[0].get("toolCallId") == tool_completes[0].get("toolCallId")
            and tool_completes[0].get("success") is True
            and requested[0].get("name", "").removeprefix("functions.") == "view"
            and requested[0].get("toolCallId") == tool_starts[0].get("toolCallId")
            and request_arguments == tool_starts[0].get("arguments"),
            "Bootstrap was not exactly one complete prompt-only view")
    returned = (tool_completes[0].get("result") or {}).get("content")
    prompt_raw = frozen(config["prompt"], spec["prompt"]["sha256"])
    require(returned == prompt_raw.decode("utf-8"), "Bootstrap view did not return the exact frozen prompt")
    require(usages and all(isinstance(item, dict)
            and item.get("model") == profile["selectedModel"]
            and item.get("maxPromptTokens") == profile["maxPromptTokens"]
            and type(item.get("inputTokens")) is int
            and 0 <= item["inputTokens"] <= profile["maxPromptTokens"] for item in usages),
            "Bootstrap usage model or maxPromptTokens differs")
    require(not compactions, "Context compaction occurred during prompt-only bootstrap")
    require(assistant_final == [config["bootstrapResponseText"]], "Bootstrap response differs")
    return event_path, raw, events, starts[0], usages


def audit(config_path, session, *extra):
    frozen(AUDIT_PATH, AUDIT_SHA)
    code, output, receipt = child(AUDIT_PATH, "--session", session,
                                  "--config", config_path, *extra)
    match = re.search(r"^Audit: (.+)$", output, re.M)
    require(match is not None, f"Auditor failed (exit {code}); preserved: {receipt}")
    path = Path(match[1].strip())
    return path, json.loads(frozen(path)), receipt


def bootstrap(family, session):
    spec, config = inputs(family)
    run = config["run"]
    launch_record = json.loads(frozen(HERE / f"{run}-launch.json"))
    require(launch_record["session"] == session, "Session differs from launch")
    path = Path(config["bootstrapRecordPath"])
    require(path.parent == HERE and not path.exists(), "Bootstrap record exists or is outside lifecycle")
    _, event_raw, events, start, usages = prompt_only_events(session, spec, config)
    snapshot_path = HERE / f"{run}-bootstrap-events-{session}.jsonl"
    write_frozen(snapshot_path, event_raw)
    record = {
        "status": "PROMPT_ONLY_BOOTSTRAP_PASS", "run": run, "sessionId": session,
        "candidate": CANDIDATE, "base": BASE,
        "configSha256": sha(frozen(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"])),
        "kickoffSha256": sha(spec["kickoffText"].encode("utf-8")),
        "promptSha256": sha(frozen(config["prompt"], spec["prompt"]["sha256"])),
        "selectedModel": start["selectedModel"], "contextTier": start["contextTier"],
        "maxPromptTokens": config["contextProfile"]["maxPromptTokens"],
        "usageRecords": len(usages), "actualPeakInputTokens": max(row["inputTokens"] for row in usages),
        "compactionEvents": [], "eventSnapshotPath": str(snapshot_path),
        "eventSnapshotSha256": sha(event_raw), "eventSnapshotBytes": len(event_raw),
        "eventCount": len(events), "eventSnapshotLastType": events[-1]["type"],
        "limits": "Prompt-only bootstrap; core delivery remains blocked until explicit coordinator authorization.",
    }
    write_frozen(path, (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(record, ensure_ascii=False))


def authorize_core(family, session):
    spec, config = inputs(family)
    run = config["run"]
    bootstrap_path = Path(config["bootstrapRecordPath"])
    authorization_path = Path(config["coreAuthorizationPath"])
    require(bootstrap_path.is_file() and authorization_path.parent == HERE
            and not authorization_path.exists(), "Bootstrap is absent or core authorization exists")
    bootstrap_raw = frozen(bootstrap_path)
    bootstrap_record = json.loads(bootstrap_raw)
    event_path, event_raw, events, start, usages = prompt_only_events(session, spec, config)
    snapshot_path = Path(bootstrap_record["eventSnapshotPath"])
    snapshot = frozen(snapshot_path, bootstrap_record["eventSnapshotSha256"])
    config_raw = frozen(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"])
    require(event_raw == snapshot and bootstrap_record["sessionId"] == session
            and bootstrap_record["status"] == "PROMPT_ONLY_BOOTSTRAP_PASS"
            and bootstrap_record["candidate"] == CANDIDATE and bootstrap_record["base"] == BASE
            and bootstrap_record["run"] == run and bootstrap_record["configSha256"] == sha(config_raw)
            and bootstrap_record["eventSnapshotBytes"] == len(snapshot)
            and bootstrap_record["eventCount"] == len(events)
            and bootstrap_record["selectedModel"] == start["selectedModel"]
            and bootstrap_record["contextTier"] == start["contextTier"]
            and bootstrap_record["maxPromptTokens"] == config["contextProfile"]["maxPromptTokens"],
            "Bootstrap event snapshot/config/session binding differs")
    authorization = {
        "status": "CORE_RELEASE_AUTHORIZED", "run": run, "sessionId": session,
        "candidate": CANDIDATE, "base": BASE, "configSha256": sha(config_raw),
        "bootstrapRecordPath": str(bootstrap_path), "bootstrapRecordSha256": sha(bootstrap_raw),
        "eventSnapshotPath": str(snapshot_path), "eventSnapshotSha256": sha(snapshot),
        "selectedModel": start["selectedModel"], "contextTier": start["contextTier"],
        "maxPromptTokens": config["contextProfile"]["maxPromptTokens"],
        "usageRecords": len(usages), "actualPeakInputTokens": max(row["inputTokens"] for row in usages),
        "compactionEvents": [], "authorizedAt": now().isoformat(),
        "limits": "Core release requires coordinator confirmation of this prompt-only snapshot.",
    }
    write_frozen(authorization_path,
                 (json.dumps(authorization, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(authorization, ensure_ascii=False))
    print("CORE RELEASE MESSAGE (send exactly):\n" + config["coreReleaseMessage"])


def require_core_authorized(family, session, config, config_raw):
    bootstrap_raw = frozen(config["bootstrapRecordPath"])
    bootstrap_record = json.loads(bootstrap_raw)
    authorization = json.loads(frozen(config["coreAuthorizationPath"]))
    snapshot = frozen(bootstrap_record["eventSnapshotPath"], bootstrap_record["eventSnapshotSha256"])
    event_path = Path.home() / ".copilot" / "session-state" / session / "events.jsonl"
    require(event_path.read_bytes().startswith(snapshot)
            and bootstrap_record["sessionId"] == session and bootstrap_record["run"] == config["run"]
            and bootstrap_record["configSha256"] == sha(config_raw)
            and authorization["status"] == "CORE_RELEASE_AUTHORIZED"
            and authorization["run"] == config["run"] and authorization["sessionId"] == session
            and authorization["candidate"] == CANDIDATE and authorization["base"] == BASE
            and authorization["configSha256"] == sha(config_raw)
            and authorization["bootstrapRecordSha256"] == sha(bootstrap_raw)
            and authorization["eventSnapshotPath"] == bootstrap_record["eventSnapshotPath"]
            and authorization["eventSnapshotSha256"] == bootstrap_record["eventSnapshotSha256"]
            and authorization["selectedModel"] == config["contextProfile"]["selectedModel"]
            and authorization["contextTier"] == "long_context"
            and authorization["maxPromptTokens"] == config["contextProfile"]["maxPromptTokens"]
            and authorization["compactionEvents"] == [],
            "Prompt-only bootstrap has not been explicitly authorized for core delivery")


def phase1(family, session):
    spec, config = inputs(family)
    run = config["run"]
    launch_record = json.loads(frozen(HERE / f"{run}-launch.json"))
    require(launch_record["session"] == session, "Session differs from launch")
    config_raw = frozen(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"])
    require_core_authorized(family, session, config, config_raw)
    path, result, audit_receipt = audit(spec["auditConfig"]["path"], session)
    if result["status"] != "PHASE1_READY" or result["breaches"]:
        print(json.dumps(freeze_json(HERE / (run + "-phase1-hold-" + uuid.uuid4().hex + ".json"),
              {"status": "HOLD", "audit": str(path), "auditReceipt": audit_receipt})))
        return 1
    code, output, receipt = child(PROTOCOL / "prepare-extension-b134-011.py", "--config", spec["auditConfig"]["path"],
                                  "--reply", path.parent / "phase1-list.txt", "--phase1-audit", path)
    if code != 0:
        print(json.dumps(freeze_json(HERE / (run + "-phase1-hold-" + uuid.uuid4().hex + ".json"),
              {"status": "HOLD_EXTENSION", "audit": str(path), "extensionReceipt": receipt})))
        return 1
    from b134_runtime import validate_prepared_extension
    ext = json.loads(frozen(HERE / f"{run}-extension.json"))
    message = frozen(HERE / f"{run}-phase2-message.txt").decode("utf-8")
    reply = frozen(path.parent / "phase1-list.txt").decode("utf-8")
    checked = validate_prepared_extension(config, ext, reply, message, path)
    freeze_json(HERE / f"{run}-phase1.json", {
        "run": run, "session": session, "readyForPhase2": True, "auditDir": str(path.parent),
        "auditSha256": sha(frozen(path)), "auditReceipt": audit_receipt, "extensionReceipt": receipt,
        "extensionEvidenceCapacity": checked})
    print("PHASE2 MESSAGE (send exactly):\n" + message)
    return 0


def final(family, session):
    spec, config = inputs(family, fresh_report=False)
    run = config["run"]
    phase = json.loads(frozen(HERE / f"{run}-phase1.json"))
    require(phase["readyForPhase2"] and phase["session"] == session, "Phase 1 mismatch")
    ext, message = HERE / f"{run}-extension.json", HERE / f"{run}-phase2-message.txt"
    reply = Path(phase["auditDir"]) / "phase1-list.txt"
    path, result, receipt = audit(spec["auditConfig"]["path"], session, "--extension", ext,
                                  "--phase1-list", reply, "--phase2-message", message, "--final")
    problems = []
    if (result["status"] != "FINAL_AUDIT_NEEDS_CLAIM_CHECK" or result.get("breaches")
            or result["unexpectedUserMessages"] or not result["reviewerIdle"]
            or result["coreRead"] != result["coreRequired"]
            or result["extensionRead"] != result["extensionRequired"]
            or result["writes"] != 1 or result["readbacks"] != 1 or not result["readbackVerified"]
            or result["fetches"] or len(result["messages"]) != 2):
        problems.append("Final event audit incomplete or breached")
    events = frozen(path.parent / "events.jsonl", result["eventsSha256"])
    if not events.startswith(frozen(Path(phase["auditDir"]) / "events.jsonl")):
        problems.append("Final events do not extend phase-1 snapshot")
    report = Path(config["report"])
    structure = None
    if report.is_file():
        report.chmod(0o444)
        checker = Path(config["reportStructureChecker"])
        code, stdout, checker_receipt = child(checker,
            "--report", report, "--core-manifest", config["coreManifest"], "--extension", ext,
            "--reference", config["reference"], "--phase1-list", reply, "--phase2-message", message,
            "--audit", path, "--run", run)
        require(code in (0, 1) and stdout.strip(), "Structure checker failed")
        structure = json.loads(stdout)
        if structure["status"] != "PASS":
            problems.append("Report structure failed")
    else:
        problems.append("Report missing")
        checker_receipt = None
    record = {"run": run, "session": session, "candidate": CANDIDATE,
              "status": "HOLD" if problems else "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
              "problems": problems, "audit": {"path": str(path), "sha256": sha(frozen(path))},
              "auditReceipt": receipt, "structure": structure, "structureReceipt": checker_receipt,
              "report": {"path": str(report), "sha256": sha(frozen(report))} if report.is_file() else None}
    name = f"{run}-final.json" if not problems else f"{run}-final-hold-{uuid.uuid4().hex}.json"
    print(json.dumps(freeze_json(HERE / name, record)))
    return 1 if problems else 0


def accept(family, adjudication_path):
    spec, config = inputs(family, fresh_report=False)
    run = config["run"]
    require(spec["role"] == "replacement-independent"
            and spec["originalReviewerConfirmation"] is False
            and spec["originalSession"] == INITIALS[family]["session"],
            "Fresh replacement-review role or predecessor binding differs")
    final_path = HERE / f"{run}-final.json"
    final_raw = frozen(final_path)
    final_record = json.loads(final_raw)
    require(final_record["session"] not in (spec["originalSession"], FAILED_SESSION,
                                            INITIALS[family]["session"])
            and final_record["run"] == run and run.endswith("-FRESH-002"),
            "Fresh independent-review identity differs")
    adjudication_raw = frozen(adjudication_path)
    adjudication = json.loads(adjudication_raw)
    require(final_record["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and adjudication["candidate"] == CANDIDATE and adjudication["run"] == run
            and adjudication["finalSha256"] == sha(final_raw)
            and adjudication["reportSha256"] == final_record["report"]["sha256"]
            and sha(frozen(config["report"])) == final_record["report"]["sha256"]
            and adjudication["claimsAdjudicated"] is True
            and adjudication["verdict"] in ("CLEAN", "NEEDS FIX", "UNVERIFIED")
            and adjudication["verdict"] == final_record["structure"]["overall"]
            and isinstance(adjudication.get("coordinatorClaimIds"), list)
            and isinstance(adjudication["claimChecks"], list) and adjudication["claimChecks"]
            and all(isinstance(item, dict)
                    and all(isinstance(item.get(key), str) and item[key].strip()
                            for key in ("claim", "evidence", "disposition"))
                    for item in adjudication["claimChecks"]),
            "Bound substantive claim adjudication required")
    print(json.dumps(freeze_json(HERE / f"{run}-acceptance.json", {
        "run": run, "candidate": CANDIDATE, "reviewAccepted": True,
        "verdict": adjudication["verdict"], "finalSha256": sha(final_raw),
        "reportSha256": final_record["report"]["sha256"],
        "adjudication": {"path": str(adjudication_path), "sha256": sha(adjudication_raw)},
        "limits": "Review acceptance only; findings require justified signed changes and original-reviewer confirmation."})))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", choices=("claude", "gpt"))
    parser.add_argument("action", choices=("admit", "launch", "bootstrap", "authorize-core",
                                           "phase1", "final", "accept"))
    parser.add_argument("argument")
    parser.add_argument("--admission", type=Path)
    args = parser.parse_args()
    if args.action == "admit":
        admit(args.family, args.argument)
    elif args.action == "launch":
        require(args.admission is not None, "Launch observation requires --admission")
        launch(args.family, args.argument, args.admission)
    elif args.action == "bootstrap":
        bootstrap(args.family, args.argument)
    elif args.action == "authorize-core":
        authorize_core(args.family, args.argument)
    elif args.action == "phase1":
        return phase1(args.family, args.argument)
    elif args.action == "final":
        return final(args.family, args.argument)
    else:
        accept(args.family, Path(args.argument))
    return 0


if __name__ == "__main__":
    sys.exit(main())
