import base64
import gzip
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("previous_visual_recipe", C / "review-batch-091-visual-651.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
R, A, V = prior.R, prior.A, prior.V
load, save, sha, git, now = prior.load, prior.save, prior.sha, prior.git, prior.now
L = C / "logs" / "c3ddbba8-0ad7-4c8b-bbad-4033deaece14"
HEAD = "e19a64832234160ae46ec48ea417687ca7bfe881"


def frozen():
    prior.L = L
    prior.ownership()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == prior.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 651 and state["batch"] == "091"
    assert not git("diff", prior.TEACHING, HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")


def prepare():
    frozen()
    backup = L / "progress-before-652.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["execution651CoordinatorCheckpoint"]["savedCommit"] == HEAD
    state = load(C / "progress.json")
    state["execution652StartingState"] = {
        "execution": 652, "batch": "091", "startedAt": now(),
        "startingHead": HEAD, "androidHead": prior.ANDROID,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME091 original GPT dependent visual assessment, then bounded local reconciliation if warranted; no publication/092.",
        "request": {"sha256": sha(request), "bytes": request.stat().st_size,
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete issue and final651 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry, exact session and decoded launcher verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed evidence only; no optional historical session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    state.update(stage="batch-091-original-gpt-dependent-visual-assessment",
                 nextAction="SAME091 preserve original GPT rendered assessment without Claude findings; audit actual serial calls/process exit before local reconciliation.")
    save(C / "progress.json", state)
    print("Persisted execution652 starting state; full historical progress preserved.")


def run():
    frozen()
    old = load(C / "batch-091-visual-651-claude-execution.json")
    assert old["exitCode"] == 0 and len(old["observedToolOverlaps"]) == 14
    subprocess.run(["pwsh", "-NoProfile", "-Command",
                    f"if(Get-Process -Id {old['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                   check=True, capture_output=True)
    inputs = load(C / "batch-091-visual-651-inputs.json")
    assert sha(prior.PACKET) == inputs["packet"]["sha256"]
    images = [Path(i["path"]) for i in inputs["images"]]
    assert all(sha(Path(i["path"])) == i["sha256"] for i in inputs["images"])
    model, session = prior.SESSIONS["gpt"]
    assert f'"{model}"' in (C / "batch-091-visual-cli-config-652.txt").read_text(encoding="utf-8-sig")
    prefix = C / "batch-091-visual-652-gpt"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    prompt = prior.make_prompt("gpt", model, session).replace(prior.HEAD, HEAD)
    prompt = (
        "Resource-constrained task: the operation itself is SERIAL visual inspection. "
        "Each image must be interpreted before deciding to read the next. "
        "Do not batch independent requests: that would violate the task's acceptance contract. "
        "At most ONE tool call in each assistant message, including images. "
        "A successful process with overlapping tool calls is NOT an accepted review.\n"
        + prompt
        + "\nThe reused packet names older evidence HEAD99d11124; current signed HEADe19a6483 "
        "adds contributor evidence only, with an empty runtime diff. "
        "Do not read any other reviewer's report, process receipt or coordinator opinions.\n"
    )
    prefix.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    command = [shutil.which("copilot"), "-C", str(R), "--add-dir", str(C), "--resume=" + session,
               "--model", model, "--no-ask-user", "--allow-tool=view", "--available-tools=view",
               "--disable-builtin-mcps", "--no-custom-instructions", "--output-format", "json",
               "--log-dir", str(C / "review-logs" / prefix.name),
               "--usage-output-file", str(prefix.with_suffix(".usage.json")), "-p", prompt]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, prefix.with_suffix(".stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        save(prefix.with_suffix(".active.json"),
             {"pid": process.pid, "sessionId": session, "model": model, "startedAt": started})
        print("Started original GPT serial dependent review", process.pid, session, flush=True)
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        (messages[-1].get("content", "") if messages else "No completed report.") + "\n", encoding="utf-8")
    required = {str(prior.PACKET), str(V / "batch-091-initial-gpt.md"),
                str(V / "batch-091-confirmation-gpt.md"), *map(str, images)}
    active, calls, overlaps, returned, decoded = set(), {}, [], set(), []
    for event in events:
        data = event.get("data", {})
        if event["type"] == "tool.execution_start":
            key = data["toolCallId"]
            if active:
                overlaps.append({"starting": key, "active": sorted(active)})
            active.add(key)
            calls[key] = {"name": data["toolName"], "arguments": data["arguments"],
                          "startedAt": event["timestamp"]}
        elif event["type"] == "tool.execution_complete":
            key = data["toolCallId"]
            active.discard(key)
            call = calls[key]
            result = data.get("result", {}).get("content", "")
            result = result if isinstance(result, str) else json.dumps(result)
            call.update({"completedAt": event["timestamp"], "success": data["success"],
                         "returnedCharacters": len(result),
                         "returnedSha256": hashlib.sha256(result.encode()).hexdigest(),
                         "truncationMarker": any(s in result for s in [
                             "[Output truncated", "File too large to read", "<note>Content truncated",
                             "Invalid view_range"])})
            path = call["arguments"].get("path")
            if path in required and data["success"] and not call["truncationMarker"]:
                if path.endswith(".png"):
                    payloads = data.get("result", {}).get("binaryResultsForLlm", [])
                    assert len(payloads) == 1 and payloads[0]["mimeType"] == "image/png"
                    payload = base64.b64decode(payloads[0]["data"], validate=True)
                    with Image.open(io.BytesIO(payload)) as image:
                        image.load()
                        dimensions = list(image.size)
                    decoded.append({"path": path, "sourceSha256": sha(Path(path)),
                                    "returnedSha256": hashlib.sha256(payload).hexdigest(),
                                    "returnedDimensions": dimensions, "returnedBytes": len(payload)})
                    returned.add(path)
                else:
                    norm = lambda s: s.replace("\r\n", "\n").rstrip()
                    exact = norm(Path(path).read_text(encoding="utf-8-sig")) in norm(result)
                    call["entireRequestedTextContained"] = exact
                    if exact:
                        returned.add(path)
    usage = load(prefix.with_suffix(".usage.json")) if prefix.with_suffix(".usage.json").exists() else None
    record = {
        "execution": 652, "batch": "091", "snapshot": HEAD, "teachingSnapshot": prior.TEACHING,
        "dependentOriginalSession": True, "newBlindReviewCredit": False,
        "sessionId": session, "requestedModel": model,
        "actualModels": sorted({m.get("model", "") for m in messages}),
        "usageCurrentModel": usage.get("currentModel") if usage else None,
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "command": command, "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "unfinishedTools": sorted(active), "requiredResources": sorted(required),
        "successfullyReturnedResources": sorted(returned), "missingResources": sorted(required - returned),
        "allAssignedResourcesSuccessfullyReturned": not (required - returned),
        "actualDecodedImageReturns": decoded, "rawSha256": sha(raw),
        "reportSha256": sha(prefix.with_suffix(".md")), "usage": usage,
        "availableTools": ["view"],
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"
                                  and e["data"].get("infoType") == "configuration"],
        "priorClaudeViolationPreservedNotAccepted": True,
        "limits": "Payload audit establishes delivery and serial execution, not comprehension. Dependent original-session review, not new blind initial coverage.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    with gzip.GzipFile(filename="", mode="wb", fileobj=(V / (prefix.name + ".jsonl.gz")).open("wb"), mtime=0) as archive:
        archive.write(raw.read_bytes())
    print(json.dumps({k: record[k] for k in [
        "exitCode", "actualModels", "missingResources", "observedToolOverlaps"]}), flush=True)
    assert code == 0 and record["actualModels"] == [model] and usage["currentModel"] == model
    assert not active and not overlaps and not (required - returned)
    assert [i["path"] for i in decoded] == list(map(str, images))
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", prior.TEACHING, HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")


if __name__ == "__main__":
    {"prepare": prepare, "gpt": run}[sys.argv[1]]()
