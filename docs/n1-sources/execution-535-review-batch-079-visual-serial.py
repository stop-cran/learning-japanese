import importlib.util
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

spec = importlib.util.spec_from_file_location("visual", Path(__file__).with_name("review-batch-079-visual.py"))
visual = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visual)


def run(family):
    model, session = visual.SESSIONS[family]
    freeze = visual.verify_freeze()
    prefix = "batch-079-visual-" + family + "-serial"
    raw = visual.C / (prefix + ".jsonl")
    assert not raw.exists(), "Never overwrite prior reviewer evidence"
    if family == "claude":
        rejected = visual.load(visual.V / "batch-079-visual-claude-execution.json")
        assert rejected["exitCode"] == 0 and not rejected["processAndCoverageAccepted"]
        assert rejected["observedToolOverlaps"] and rejected["multiToolResponses"]
    else:
        prior_path = visual.V / "batch-079-visual-claude-serial-execution.json"
        prior = visual.load(prior_path)
        assert prior["exitCode"] == 0 and prior["processAndCoverageAccepted"]
    resources = [freeze["packet"]] + [
        str(visual.N / names[0]) for names in freeze["imageAliasGroups"].values()
    ]
    assert len(resources) == 30
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = visual.now()
    turns = []
    task = (visual.C / "batch-079-visual-task.txt").read_text(encoding="utf-8")
    turns_dir = visual.C / (prefix + "-turns")
    turns_dir.mkdir(exist_ok=False)
    visual.save(turns_dir / "authorization.json", {
        "sharedTaskSha256": visual.sha(visual.V / "batch-079-visual-task.txt"),
        "resources": resources,
        "method": "Host dispatches one assigned resource per original-session CLI turn, verifies process exit and exact one successful view before next. Final report turn has zero tools.",
        "priorClaudeProcessViolation": "Original 30 reads returned all source/images but 25 tool overlaps and two multi-tool responses; original report and payloads retained, not accepted.",
    })
    with raw.open("wb") as combined:
        for index in range(31):
            final = index == 30
            if final:
                prompt = (
                    "FINAL SAME079 bounded dependent visual report, original session/model. "
                    "The host has now completed and archived 30 serial one-resource CLI turns; each child exited before the next. "
                    "Use your directly inspected complete packet and all29 images. NO tools, NO repeated reads. "
                    "Return the COMPLETE Snapshot/Scope/Verdicts/Findings/Optional/Limits report required below. "
                    "Do not silently rehabilitate the earlier Claude overlapping run: it is preserved/rejected for process compliance. "
                    "This dispatch pass reads are fresh/serial, same bytes/snapshot; distinguish these facts from inherited lexical conclusions. "
                    "Include all four assignments, exact image/source coverage, optional dispositions, original supplemental conclusions, "
                    "fonts/table/route/drawing/persistence/phone limits, no general certification.\n\n" + task
                )
            else:
                resource = resources[index]
                prompt = (
                    f"SAME079 strict host-dispatched serial visual confirmation, original session/model. "
                    f"Resource {index + 1}/30. This CLI child MUST read ONLY this one resource: {resource}\n"
                    "Make EXACTLY ONE view call, no other call and no tools afterward; then stop with a brief observation about THIS resource only. "
                    "Do NOT read the rest of the sequence or issue a final overall verdict yet. Host supplies the next file in a new turn only AFTER this process exits. "
                    "This one-resource instruction supersedes the earlier all-files-in-one-turn request. "
                    "No parallel calls, shell, edits, delegation or questions. "
                    + ("Use forceReadLargeFiles=true and no view_range; read the complete packet. " if index == 0 else "Inspect the actual PNG pixels, not its filename or inherited descriptions. ")
                    + "If unavailable/truncated, report it; do not substitute another read. "
                    "Same frozen evidence dcfcbb43; teaching0f7f20e9, native envelope3fdc0bf9. "
                    "All177lexicalfamilies and prior supplemental resolution inherited; no fresh upstream/native/phone claims. "
                    "Source packet/native execution are supplied evidence. "
                    + ("Read this common task for scope only; it does NOT authorize reading more than the single resource above:\n" + task if index == 0 else "")
                )
            prompt_file = turns_dir / f"turn-{index + 1:02d}-prompt.txt"
            prompt_file.write_text(prompt, encoding="utf-8")
            turn_raw = turns_dir / f"turn-{index + 1:02d}.jsonl"
            usage = turns_dir / f"turn-{index + 1:02d}-usage.json"
            command = [
                shutil.which("copilot"), "-C", str(visual.R), "--add-dir", str(visual.C),
                "--model", model, "--session-id", session, "--no-ask-user",
                "--allow-tool=view", "--disable-builtin-mcps", "--available-tools=view",
                "--no-custom-instructions", "--output-format", "json",
                "--log-dir", str(visual.C / "review-logs" / prefix),
                "--usage-output-file", str(usage), "-p", prompt,
            ]
            turn_start = visual.now()
            with turn_raw.open("wb") as out, (turns_dir / f"turn-{index + 1:02d}-stderr.txt").open("wb") as err:
                proc = subprocess.Popen(command, stdout=out, stderr=err, env=env)
                visual.save(visual.C / (prefix + "-active.json"), {
                    "pid": proc.pid, "sessionId": session, "startedAt": turn_start,
                    "requestedModel": model, "resourceIndex": index + 1,
                })
                print(f"{family} resource {index + 1}/31 running PID {proc.pid}", flush=True)
                code = proc.wait()
            data = turn_raw.read_bytes()
            combined.write(data)
            combined.flush()
            events = [json.loads(line) for line in data.decode("utf-8-sig").splitlines() if line.strip()]
            calls = [e["data"] for e in events if e["type"] == "tool.execution_start"]
            completions = [e["data"] for e in events if e["type"] == "tool.execution_complete"]
            messages = [e["data"] for e in events if e["type"] == "assistant.message"]
            terminal = [e for e in events if e["type"] == "result"]
            accepted = (
                code == 0 and len(calls) == len(completions) == (0 if final else 1)
                and (final or calls[0]["toolName"] == "view" and calls[0]["arguments"].get("path") == resource
                     and completions[0]["success"])
                and not any(len(m.get("toolRequests", [])) > 1 for m in messages)
                and len(terminal) == 1 and terminal[0]["exitCode"] == 0
                and terminal[0]["sessionId"] == session
            )
            row = {
                "turn": index + 1, "launcherPid": proc.pid, "startedAt": turn_start,
                "completedAt": visual.now(), "exitCode": code, "singleResourceAccepted": accepted,
                "resource": None if final else resource, "rawSha256": visual.sha(turn_raw),
                "requestedModel": model, "sessionId": session,
            }
            turns.append(row)
            visual.save(turns_dir / "processes.json", turns)
            assert accepted, "Original bounded dispatch evidence retained; stop on actual process/read failure."
            if index:
                assert datetime.fromisoformat(turns[-2]["completedAt"]) < datetime.fromisoformat(turn_start)
            visual.verify_freeze()
            print(f"{family} resource {index + 1}/31 exited0, {len(calls)} serial tool", flush=True)
    shutil.copyfile(usage, visual.C / (prefix + "-usage.json"))
    visual.save(visual.C / (prefix + "-process.json"), {
        "launcherPid": turns[-1]["launcherPid"], "requestedModel": model, "sessionId": session,
        "startedAt": started, "completedAt": visual.now(), "exitCode": 0,
        "evidenceHead": visual.HEAD, "reviewedTeachingSnapshot": visual.TEACHING,
        "hostDispatchedTurns": turns, "actualChildProcessesExitedBeforeNext": True,
    })
    visual.archive(family, serial=True)


if __name__ == "__main__":
    run(sys.argv[1])
