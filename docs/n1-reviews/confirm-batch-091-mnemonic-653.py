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
spec = importlib.util.spec_from_file_location("visual651", C / "review-batch-091-visual-651.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
R, A, V = prior.R, prior.A, prior.V
L = C / "logs" / "a297e8a5-d6d6-4e38-bd4a-552dcf57a8e7"
HEAD = "1cfd5bd36e707ee78ba4401e48ffba9815854d58"
load, save, sha, git, now = prior.load, prior.save, prior.sha, prior.git, prior.now
IMAGES = [prior.N / name for name in [
    "n1-091-font-panel-3.png", "n1-091-meaning-question.png", "n1-091-drawing-trace.png"
]]


def frozen():
    prior.L = L
    prior.ownership()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == prior.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 652 and state["batch"] == "091"


def prepare():
    frozen()
    backup = L / "progress-before-653.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["batch091MnemonicCorrectionCheckpoint"]["savedCommit"] == HEAD
    state = load(C / "progress.json")
    state["execution653StartingState"] = {
        "execution": 653, "batch": "091", "startedAt": now(),
        "startingHead": HEAD, "androidHead": prior.ANDROID,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME091 original Claude then GPT SERIAL bounded mnemonic confirmations; signed local evidence only, no publication/092.",
        "request": {"sha256": sha(request), "bytes": request.stat().st_size,
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed before acting; operative contract, complete issue and final652 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial printing failed on cp1252 after successful full read/parse; UTF-8 output corrected."},
        "runnerLockRole": "Live parent19008 ancestry, exact session and decoded launcher verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed evidence only; no optional historical session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    state.update(stage="batch-091-original-session-mnemonic-confirmations",
                 nextAction="SAME091 original Claude then GPT serial changed-passage and three original image confirmations on signed1cfd5bd3; inspect actual process/tool receipts, reconcile and persist local checkpoint.")
    save(C / "progress.json", state)
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-091-mnemonic-cli-{kind}-653.txt").write_bytes(result.stdout)
    print("Starting state persisted; exact signed clean worktrees and parent ownership verified.", flush=True)


def run(label):
    frozen()
    if label == "gpt":
        previous = load(C / "batch-091-mnemonic-653-claude-execution.json")
        assert previous["acceptedExecution"]
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {previous['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       check=True, capture_output=True)
    model, session = prior.SESSIONS[label]
    assert f'"{model}"' in (C / "batch-091-mnemonic-cli-config-653.txt").read_text(encoding="utf-8-sig")
    prefix = C / f"batch-091-mnemonic-653-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    own = V / ("batch-091-visual-651-claude.md" if label == "claude" else "batch-091-visual-652-gpt.md")
    diff = V / "batch-091-mnemonic-correction-652.diff"
    article = R / "kanji" / "\u5203.md"
    resources = [own, diff, article, *IMAGES]
    prompt = f"""DEPENDENT changed-passage confirmation in ORIGINAL session {session}; model {model}.
Frozen signed HEAD {HEAD}. Exactly ONE view tool call per assistant response, wait for its result before next.
SERIAL inspection is the actual task, not independent lookups to batch. Overlapping tool calls invalidate acceptance.
Only view is exposed; no shell, edits, delegation, other reports, broad source rereads, new blind-review credit or questions.
Read these six resources COMPLETELY IN THIS ORDER, one call per response:
{chr(10).join(str(p) for p in resources)}
Your own previous report is supplied, not the other reviewer's. The exact diff changes ONLY the kanji mnemonic paragraph and derived manifest.
Assess whether the revised paragraph accurately and clearly accommodates BOTH detached shortmark in default Gothic and crossing shortmark in other fonts/the pinned diagram, without historical/etymological overclaim.
Inspect all three original images freshly and compare with the full revised kanji article. Do not equate image hashes with viewing.
No new word/metadata/readings/order/quiz/links/stroke geometry change. Inherit your own prior textual conclusions and preserved optional hypotheses/limits; do not freshly certify unrelated content.
IMPORTANT old PNGs show OLD contentVersion cb3c857f3614485d; CURRENT version bfe65483a821fc13 has NOT been natively imported or rendered. Old PNGs support shape comparison ONLY, NOT revised text layout.
Native650 two terminalcases0/no skips, ContentSync once/full archive f6b2ee39, 1114kanji/5070words/123N1/zeroProblems/Roomepoch1 are inherited coordinator receipts, NOT your tests or the revised version.
API35/test-onlyAndroid1c1b7bf4 retaining productionf9b59a2, unknown actual fallbackface, injectedtrace not humanhandwriting/successfulMLKit, phone/generalrelease/whole-set/currentmain/CI/publicZIP limits remain.
Claude's prior batched-image execution remains rejected as serial-process acceptance even if original visual observation is useful; do not rewrite history. This new follow-up must itself be serial.
Return full compact report: Snapshot;Scope(actual model, exact text/image reads);Verdicts(correctness/scopedcoverage/comprehensibility for changed kanji; word inherited unchanged);Findings(severity/facet/file:line/claim+impact/remedy/evidence/confidence or none);Optional;Limits.
Reconcile YOUR own prior finding/limits as resolved/partially resolved/unresolved/withdrawn/optional. If your prior report found no defect, state that rather than inventing agreement. State precisely whether this wording introduces any regression and whether original images establish its descriptive accuracy. Revised native rendering remains unperformed, not an article defect by itself.
"""
    prefix.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    command = [shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
               "--resume=" + session, "--model", model, "--no-ask-user",
               "--allow-tool=view", "--available-tools=view", "--disable-builtin-mcps",
               "--no-custom-instructions", "--output-format", "json",
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
        print("Started original", label, process.pid, session, flush=True)
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        (messages[-1].get("content", "") if messages else "No completed report.") + "\n", encoding="utf-8")
    active, calls, overlaps, returned, images = set(), {}, [], [], []
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
            call.update(completedAt=event["timestamp"], success=data["success"],
                        returnedCharacters=len(result), returnedSha256=hashlib.sha256(result.encode()).hexdigest())
            path = call["arguments"].get("path")
            if path in map(str, resources) and data["success"]:
                if path.endswith(".png"):
                    payloads = data.get("result", {}).get("binaryResultsForLlm", [])
                    assert len(payloads) == 1 and payloads[0]["mimeType"] == "image/png"
                    payload = base64.b64decode(payloads[0]["data"], validate=True)
                    with Image.open(io.BytesIO(payload)) as image:
                        image.load()
                        dimensions = list(image.size)
                    images.append({"path": path, "sourceSha256": sha(Path(path)),
                                   "returnedSha256": hashlib.sha256(payload).hexdigest(),
                                   "returnedDimensions": dimensions})
                    returned.append(path)
                else:
                    norm = lambda s: s.replace("\r\n", "\n").rstrip()
                    call["entireRequestedTextContained"] = norm(Path(path).read_text(encoding="utf-8-sig")) in norm(result)
                    if call["entireRequestedTextContained"]:
                        returned.append(path)
    usage = load(prefix.with_suffix(".usage.json")) if prefix.with_suffix(".usage.json").exists() else {}
    models = sorted({m.get("model", "") for m in messages})
    accepted = code == 0 and models == [model] and usage.get("currentModel") == model and not active and not overlaps and returned == list(map(str, resources))
    record = {
        "execution": 653, "batch": "091", "snapshot": HEAD, "sessionId": session,
        "dependentOriginalSession": True, "newBlindInitialReviewCredit": False,
        "requestedModel": model, "actualModels": models, "usageCurrentModel": usage.get("currentModel"),
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "command": command, "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "unfinishedTools": sorted(active), "requiredResources": list(map(str, resources)),
        "successfullyReturnedResources": returned, "actualDecodedImageReturns": images,
        "acceptedExecution": accepted, "rawSha256": sha(raw), "reportSha256": sha(prefix.with_suffix(".md")),
        "usage": usage, "availableTools": ["view"],
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"
                                  and e["data"].get("infoType") == "configuration"],
        "limits": "Audited serial execution and complete returned resources, not proof of comprehension. Original PNGs show old version, not revised native rendering. Historical Claude tool-overlap violation remains rejected.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({k: record[k] for k in ["exitCode", "actualModels", "acceptedExecution", "observedToolOverlaps"]}), flush=True)
    frozen()
    assert accepted, "Preserve failed/incomplete execution and yield; do not silently accept"


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    else:
        run(sys.argv[1])
