"""Synthetic controller transitions and actual wrapper rejection; never starts a reviewer."""
import copy
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from b134_common import HERE, PROTOCOL, ROOT, CORE, CORE_SHA, frozen, sha, freeze_json, write_frozen, require, start_guard

CASE = HERE / "synthetic-controller-validation-001"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PROTOCOL / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


FIXTURE = module("b134_controller_fixture", "test-synthetic-protocol-b134-001.py")
STEP, AUDIT, PREPARE = FIXTURE.STEP, FIXTURE.AUDIT, FIXTURE.PREPARE
import b134_common
import b134_runtime


def jsonl(events):
    return b"".join((json.dumps(e, ensure_ascii=False) + "\n").encode() for e in events)


def positive_controller():
    """All app observations are fabricated locally; real immutable packet checks remain active."""
    preflight = json.loads(frozen(HERE / "audit-configs-001" / "preflight.json"))
    spec = copy.deepcopy(preflight["runs"]["claude"])
    config = json.loads(frozen(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"]))
    report = CASE / "reports" / "fixture.md"
    report.parent.mkdir(parents=True, exist_ok=False)
    config["report"] = spec["report"] = str(report)
    spec["auditConfig"] = freeze_json(CASE / "config.json", config)
    core = json.loads(frozen(CORE, CORE_SHA))
    reference = json.loads(frozen(config["reference"]))
    events = FIXTURE.events_for(config, core)
    events[0]["data"]["selectedModel"] = "claude-opus-5.5"
    events[2]["data"]["usage"].update(model="claude-fixture", responseModel="claude-fixture", maxPromptTokens=952000)
    for event in events:
        if event["type"] == "assistant.message":
            event["data"]["model"] = "claude-fixture"
    first = AUDIT.audit(events, config, core, reference)
    require(first["status"] == "PHASE1_READY", "Synthetic first phase failed")
    audit_dir = CASE / config["run"] / "audit-phase1"
    raw = jsonl(events)
    first["eventsSha256"] = sha(raw)
    write_frozen(audit_dir / "events.jsonl", raw)
    audit_binding = freeze_json(audit_dir / "audit.json", first)
    write_frozen(audit_dir / "phase1-list.txt", b"D: none\nE: none\nO: none")
    # This synthetic roster is never substituted for a live reviewer observation.
    status = {"summary": {"total": 1}, "sessions": [{
        "id": config["coordinator"], "name": "synthetic coordinator", "activity": {"status": "busy"}}]}
    status_path = freeze_json(CASE / "status.json", status)["path"]
    roster_path = freeze_json(CASE / "roster.json", [{"id": config["coordinator"]}])["path"]
    request_path = freeze_json(CASE / "request.json", {
        "statusPath": status_path, "rosterPath": roster_path, "observedAt": STEP.now().isoformat()})["path"]
    real_child = STEP.child

    def extension_child(*args):
        require(Path(args[0]).name == "prepare-extension-b134-001.py", "Unexpected synthetic child")
        with patch.object(PREPARE, "HERE", CASE), patch.object(sys, "argv", list(map(str, args))):
            PREPARE.main()
        return 0, "In-process synthetic extension adapter; no subprocess/reviewer launched.", str(CASE)

    session = "synthetic-claude-observation-001"
    with patch.object(STEP, "HERE", CASE), patch.object(STEP, "inputs", return_value=(spec, config)):
        # Inputs are routed to isolated synthetic report/config paths for this fixture.
        # Production inputs independently passes the forecast; observations remain fabricated.
        STEP.admit("claude", request_path)
        admission = next(CASE.glob(config["run"] + "-admission-*/admission.json"))
        home = CASE / "fabricated-home"
        event_path = home / ".copilot" / "session-state" / session / "events.jsonl"
        write_frozen(event_path, jsonl(events[:2]))
        with patch("pathlib.Path.home", return_value=home):
            STEP.launch("claude", session, admission)
        with patch.object(STEP, "audit", return_value=(audit_dir / "audit.json", first, "synthetic snapshot")), \
             patch.object(STEP, "child", side_effect=extension_child), \
             patch.object(b134_runtime, "HERE", CASE):
            require(STEP.phase1("claude", session) == 0, "Synthetic phase1 transition failed")
        extension = json.loads(frozen(CASE / (config["run"] + "-extension.json")))
        message = frozen(CASE / (config["run"] + "-phase2-message.txt")).decode()
        report_text = (HERE / "synthetic-validation-001" / "two-phase" / "report" / "synthetic.md").read_text("utf-8")
        report_text = report_text.replace("N1-B134-GPT-001", config["run"])
        final_events = copy.deepcopy(events)
        final_events.append({"type": "user.message", "data": {
            "content": message, "source": "agent-" + config["coordinator"]}})

        def call(name, args, result):
            cid = "synthetic-phase2-" + str(len(final_events))
            final_events.extend([
                {"type": "assistant.message", "data": {"model": "claude-fixture", "apiCallId": cid,
                    "toolRequests": [{"toolCallId": cid, "name": name, "arguments": args}]}},
                {"type": "tool.execution_complete", "data": {
                    "toolCallId": cid, "success": True, "result": {"content": result}}}])
        for segment in extension["segments"]:
            call("view", {"path": segment["path"], "forceReadLargeFiles": True}, frozen(segment["path"]).decode())
        patch_text = "*** Begin Patch\n*** Add File: " + str(report) + "\n"
        patch_text += "".join("+" + line + "\n" for line in report_text.splitlines())
        patch_text += "*** End Patch\n"
        call("apply_patch", patch_text, "Synthetic exclusive creation only")
        with report.open("xb") as stream:
            stream.write(report_text.encode())
        require(report.read_bytes() == report_text.encode(), "Synthetic exclusive report readback failed")
        call("view", {"path": str(report), "forceReadLargeFiles": True}, report_text)
        call("send_session_message", {"session_id": config["coordinator"], "message": "UNVERIFIED"}, "Synthetic only")
        final_events.append({"type": "assistant.turn_end", "data": {}})
        with patch.object(b134_common, "HERE", CASE), patch.object(b134_runtime, "HERE", CASE):
            final_audit = AUDIT.audit(final_events, config, core, reference, extension,
                                      "D: none\nE: none\nO: none", message, final=True)
        require(final_audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK", str(final_audit["breaches"]))
        final_dir = CASE / config["run"] / "audit-final"
        final_raw = jsonl(final_events)
        require(final_raw.startswith(raw), "Synthetic final snapshot does not extend phase1")
        final_audit["eventsSha256"] = sha(final_raw)
        write_frozen(final_dir / "events.jsonl", final_raw)
        freeze_json(final_dir / "audit.json", final_audit)
        with patch.object(STEP, "audit", return_value=(final_dir / "audit.json", final_audit, "synthetic snapshot")):
            require(STEP.final("claude", session) == 0, "Synthetic final transition failed")
        final_path = CASE / (config["run"] + "-final.json")
        final_record = json.loads(frozen(final_path))
        adjudication = freeze_json(CASE / "adjudication.json", {
            "candidate": config["candidate"], "run": config["run"], "finalSha256": sha(frozen(final_path)),
            "reportSha256": final_record["report"]["sha256"], "claimsAdjudicated": True,
            "verdict": "UNVERIFIED", "claimChecks": [{
                "claim": "This fabricated report is solely a controller test.",
                "evidence": "Locally fabricated events, no real reviewer session.",
                "disposition": "Synthetic UNVERIFIED; no teaching claim or acceptance."}]})
        STEP.accept("claude", Path(adjudication["path"]))
        # Verify exact-message and readback/completion rejection using the full fabricated final.
        for mutation in ("wrong-phase2", "wrong-readback", "wrong-completion", "second-write"):
            altered = copy.deepcopy(final_events)
            if mutation == "wrong-phase2":
                next(e for e in reversed(altered) if e["type"] == "user.message")["data"]["content"] += "\nchanged"
            elif mutation == "wrong-readback":
                altered[-4]["data"]["result"]["content"] = "wrong synthetic report"
            elif mutation == "wrong-completion":
                altered[-3]["data"]["toolRequests"][0]["arguments"]["message"] = "UNVERIFIED " + str(report)
            else:
                # Insert another successful write before completion.
                request = next(e for e in altered if e["type"] == "assistant.message"
                               and e["data"].get("toolRequests", [{}])[0].get("name") == "apply_patch")
                extra = copy.deepcopy(request)
                extra["data"]["apiCallId"] = "synthetic-repeated-write"
                extra["data"]["toolRequests"][0]["toolCallId"] = "synthetic-repeated-write"
                altered[-3:-3] = [extra, {"type": "tool.execution_complete", "data": {
                    "toolCallId": "synthetic-repeated-write", "success": True,
                    "result": {"content": "not executed"}}}]
            rejected = AUDIT.audit_base(altered, config, core, reference, extension,
                                         "D: none\nE: none\nO: none", message, final=True)
            require(rejected["status"] == "VOID", "Failed final negative control: " + mutation)
    return {"controllerActions": ["admit", "launch-observation", "phase1", "final", "accept"],
            "syntheticOnly": True, "syntheticObservationRoutingOnly": True,
            "realChildStructureCheckerExercised": True, "reportExclusiveCreateReadback": "PASS",
            "finalNegativeControls": 4, "case": str(CASE)}


def wrapper_rejections():
    runner = module("b134_wrapper_cleanup", str(ROOT / "guarded-test-v3.py"))
    wrapper = PROTOCOL / "run-step-b134-001.ps1"
    rows = []
    for action in ("admit", "launch", "phase1", "final", "accept"):
        command = ["pwsh", "-NoProfile", "-File", str(wrapper), "-Action", action, "-Model", "claude"]
        if action in ("admit", "launch", "accept"):
            command += ["-InputPath", str(CASE / "absent-synthetic-input.json")]
        if action in ("launch", "phase1", "final"):
            command += ["-SessionId", "synthetic-never-launched"]
        process = None
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
            while True:
                try:
                    stdout, stderr = process.communicate(timeout=0.1)
                    break
                except subprocess.TimeoutExpired:
                    continue
        finally:
            runner.stop_child(process)
        require(process.returncode != 0, "Wrapper accepted missing observations")
        combined = stdout.decode("utf-8") + stderr.decode("utf-8")
        require("FileNotFoundError" in combined, "Wrapper failed for an unexpected reason")
        match = re.search(r"Guarded execution evidence: (.+)", combined)
        require(match, "Wrapper execution evidence missing")
        directory = Path(match[1].strip())
        require(directory.parent == ROOT, "Wrapper output not a direct review-root child")
        receipt_raw = frozen(directory / "receipt.json")
        receipt = json.loads(receipt_raw)
        frozen(directory / "output.log", receipt["logSha256"])
        require(receipt["exitCode"] != 0 and not receipt["memory"]["breach"]
                and receipt["cleanupError"] is None, "Rejection breached resources or cleanup")
        write_frozen(CASE / "wrapper-rejections" / (action + "-stdout.log"), stdout)
        write_frozen(CASE / "wrapper-rejections" / (action + "-stderr.log"), stderr)
        rows.append({"action": action, "command": command, "exitCode": process.returncode,
                     "receipt": {"path": str(directory / "receipt.json"), "sha256": sha(receipt_raw)}})
    return rows


if __name__ == "__main__":
    require(not CASE.exists(), "Preserve existing synthetic controller artifacts")
    guard, _ = start_guard("B134 full synthetic controller and wrapper rejection")
    try:
        positive = positive_controller()
        rejections = wrapper_rejections()
        print(json.dumps(freeze_json(HERE / "controller-validation-001.json", {
            "status": "PASS_SYNTHETIC_CONTROLLER_AND_REAL_WRAPPER_REJECTIONS",
            "positive": positive, "wrapperRejections": rejections,
            "limits": "No real reviewer launched or admitted. Synthetic observations never authorize a real run."})))
    finally:
        require(not guard.finish()["breach"], "Controller test RAM breach")
