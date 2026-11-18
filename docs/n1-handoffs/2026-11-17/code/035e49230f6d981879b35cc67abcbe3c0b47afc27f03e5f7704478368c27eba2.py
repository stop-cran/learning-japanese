"""Repeatable GPT004 preparation verification; optional exclusive frozen handoff, never admission."""
import json
import sys
from pathlib import Path

from b131_review_v4_common import (
    DEFAULT_PREFLIGHT, HERE, IMMUTABLE_BINDINGS, POLICY, RECORDS, TELEMETRY, TELEMETRY_SHA, TOOLS,
    freeze_json, frozen, require, sha, start_guard)
from b131_capacity_003 import PROFILES, load_forecast
from b131_preflight_004 import path_inventory, verify_protocol, verify_subset


def main(seal=False):
    guard, _ = start_guard("B131 GPT004 final preparation verification")
    try:
        subset = verify_subset(guard, initial=True)
        preflight = json.loads(frozen(DEFAULT_PREFLIGHT))
        protocol = verify_protocol(preflight)
        inventory = path_inventory(preflight)
        readiness = preflight["pathReadiness"]
        require(json.loads(frozen(readiness["path"], readiness["sha256"]))["inventory"] == inventory,
                "Frozen path inventory differs from actual004 paths")
        spec = preflight["runs"]["gpt"]
        run = spec["run"]
        for suffix in ("admission.json", "launch.json", "phase1.json", "extension.json",
                       "phase2-message.txt", "final.json", "acceptance.json"):
            require(not (HERE / f"{run}-{suffix}").exists(), "Do not admit/launch/overwrite reviewer state")
        require(not (HERE / run).exists(), "No actual GPT004 audit directory should exist yet")
        test_path = HERE / "validation-004" / "result.json"
        tests = json.loads(frozen(test_path))
        require(tests["status"] == "PASS" and tests["tests"] >= 37
                and tests["failures"] == tests["errors"] == 0
                and not tests["memory"]["breach"], "Focused validation has not passed")
        frozen(test_path.parent / "output.log", tests["outputSha256"])
        forecast = load_forecast()
        result = {
            "status": "VERIFIED_GPT004_PREPARATION_ONLY", "protocol": protocol, "pathInventory": inventory,
            "unchangedEvidence": subset, "contextProfiles": PROFILES,
            "forecastPhase1Tokens": forecast["bootstrapTokens"] + forecast["coreTokens"],
            "projectedStartupWorstCase": forecast["projectedWorstCasePeak"], "startupGate": 700000,
            "gptPrePhase2Gate": 710000, "tests": {
                "path": str(test_path), "sha256": sha(frozen(test_path)), "passed": tests["tests"]},
            "preflight": {"path": str(DEFAULT_PREFLIGHT), "sha256": sha(frozen(DEFAULT_PREFLIGHT))},
            "sequentialPrerequisite": preflight["sequentialPrerequisite"],
            "limits": "Forecast and compaction trigger are not guarantees. Fresh full unfiltered serial "
                      "admission, RAM and exact model/context/no-compaction checks remain mandatory. "
                      "Filesystem probes cannot guarantee future ACL/path availability.",
            "notPerformed": ["No reviewer admitted/launched/messaged/resumed/reclassified",
                             "No GPT003 events/audit/list or Claude findings/report/adjudication opened",
                             "No teaching/source/core/forecast edits, commits, pushes or publication"]}
        if seal:
            config = json.loads(frozen(spec["auditConfig"]))
            paths = [Path(row["path"]) for row in config["files"]]
            paths += [DEFAULT_PREFLIGHT, Path(spec["auditConfig"]), Path(readiness["path"]), test_path,
                      test_path.parent / "output.log", TELEMETRY, HERE / "runset-build-004.json",
                      HERE / "coordinator-step006.diff", HERE / "coordinator-adapter005.diff",
                      HERE / "fresh-step007.diff"]
            artifacts = [{"path": str(path), "sha256": sha(frozen(path)), "bytes": path.stat().st_size}
                         for path in dict.fromkeys(paths)]
            prefix = ("$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'; "
                      "$env:PYTHONDONTWRITEBYTECODE='1'; $receipt='" + str(RECORDS / "preparation-v4-command-")
                      + "'+[guid]::NewGuid().ToString('N'); python -B '"
                      + str(RECORDS / "guarded-test-v3.py") + "' $receipt python -B '"
                      + str(TOOLS / "run_b127_tool.py") + "' ")
            commands = {"verify": prefix + "'" + str(TOOLS / "verify_b131_gpt004.py") + "'"}
            for action, argument in (("admit", "admissionRequest"), ("launch", "sessionId"),
                                     ("phase1", "sessionId"), ("final", "sessionId"), ("accept", "adjudication")):
                commands[action] = (prefix + "'" + str(TOOLS / "step_b131_neutral_007.py")
                                    + "' 131 gpt " + action + " $" + argument + " '" + str(DEFAULT_PREFLIGHT) + "'")
            command_proof = freeze_json(HERE / "guarded-commands-004.json", {
                "commands": commands,
                "arguments": {"admissionRequest": "Fresh full unfiltered status/roster request<120sec, observedAt.",
                              "sessionId": "Fresh GPT004 app session only; NEVER GPT003.",
                              "adjudication": "Frozen substantive adjudication of GPT004 bound to current candidate/final/report."},
                "limits": "Only verify was executed. Launch records a future app-created session, not a model launcher. "
                          "No script execution-policy change or .ps1 wrapper required."})
            result.update(artifacts=artifacts, commands=command_proof,
                          immutableBindings=[{"path": str(path), "sha256": digest}
                                             for path, digest in IMMUTABLE_BINDINGS],
                          neutralTelemetrySha256=TELEMETRY_SHA,
                          capacityPolicySha256=sha(frozen(POLICY)))
        memory = guard.finish()
        require(not memory["breach"], "GPT004 verification RAM breach")
        result["memory"] = memory
        if seal:
            print(json.dumps({"handoff": freeze_json(HERE / "preparation-handoff-004.json", result),
                              "commands": command_proof, "tests": result["tests"]}))
        else:
            print(json.dumps(result, ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    require(sys.argv[1:] in ([], ["--freeze"]), "Expected no argument or --freeze")
    main(seal=sys.argv[1:] == ["--freeze"])
