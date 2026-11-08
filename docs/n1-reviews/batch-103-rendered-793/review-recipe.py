"""Resume original batch-103 reviewers using the committed rendered dossier."""
import datetime
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import struct
import sys

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "1b433be5-2dc7-4b81-b332-57694a5f3bd0"
D = R / "docs" / "n1-reviews" / "batch-103-rendered-792"
W = C / "batch-103-rendered-793"
HEAD = "ba8917b6d35e044bf96d059beb44a7bd7392f2de"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
MODELS = {"claude": "claude-opus-5.5", "gpt": "gpt-6.1-sol"}
SESSIONS = {"claude": "eb1a8995-1568-4cd5-b7bb-0a1056233592",
            "gpt": "93b54be3-157e-4b13-a32c-e48e9f51c8d8"}


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def git(*args, repo=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(repo), *args],
                                   encoding="utf-8").strip()


def absent(pid):
    return subprocess.run(["pwsh", "-NoProfile", "-Command",
                           f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                          capture_output=True).returncode == 0


def frozen():
    for repo, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", repo=repo) == head
        assert git("log", "-1", "--format=%G?", repo=repo) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", repo=repo)
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (13320, L.name, "running")
    assert not absent(13320)
    progress = load(C / "progress.json")
    assert (progress["checkpoint"], progress["batch"], progress["status"]) == (792, "103", "continue")


def prepare():
    frozen()
    assert not W.exists()
    W.mkdir()
    p = load(C / "progress.json")
    shutil.copyfile(C / "progress.json", L / "progress-before-793.json")
    request = (L / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == p["checkpoint"] == 792
    state = {
        "execution": 793, "batch": "103", "startedAt": now(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME103 serial original-family rendered confirmations, actual source/image/tool/process audits and durable LOCAL checkpoint; no native rerun/publication/104.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": len(request),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint parsed; operative contract, full approved issue and final792 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": load(L / "preflight-793.json"),
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs/control helpers only; optional historical-session recipes not accessed.",
        "status": "rendered-confirmations-preparing",
        "previousDenial": "Preserved execution792 atomic-save denial and parent recovery; cause/handle owner unknown. No retry or bypass.",
    }
    assert "execution793StartingState" not in p
    p["execution793StartingState"] = state
    tmp = C / "progress.json.793-start.tmp"
    assert not tmp.exists()
    save(tmp, p)
    os.replace(tmp, C / "progress.json")
    reread = load(C / "progress.json")
    original = load(L / "progress-before-793.json")
    assert all(reread[k] == v for k, v in original.items())
    save(L / "starting-state-793.json", state)
    for kind, args in [("help", ["--help"]), ("config-help", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (W / f"cli-{kind}.txt").write_bytes(result.stdout)
    catalog = (W / "cli-config-help.txt").read_text(encoding="utf-8-sig")
    assert all(f'"{m}"' in catalog for m in MODELS.values())
    for resource in load(D / "review-resources.json"):
        path = Path(resource["path"])
        archived = gzip.decompress(Path(resource["archive"]).read_bytes())
        assert hashlib.sha256(archived).hexdigest() == resource["sha256"]
        assert sha(path) == resource["sha256"]
    for image in load(D / "original-png-scope.json")["images"]:
        assert sha(Path(image["path"])) == image["sha256"]
    assert not git("diff", "08e76c1688ada4898a79e25e13650687dadf65d1", HEAD,
                   "--", "kanji", "words", "strokes", "manifest.json")
    for label in MODELS:
        prompt = gzip.decompress((D / f"{label}-review-task.txt.gz").read_bytes()).decode("utf-8-sig")
        prompt = prompt.replace("current source snapshot 878b65a7480d0e6a24d00789d8fd98b32d296522",
                                "current source snapshot " + HEAD)
        (W / f"{label}-task.txt").write_text(prompt, encoding="utf-8")
    print("Starting state persisted; exact committed resources, images, unchanged teaching and actual catalog verified.")


def run(label, transport=False):
    frozen()
    prefix = label + ("-transport" if transport else "")
    subprocess.run(["pwsh", "-NoProfile", "-File", str(C / "preflight-793.ps1"),
                    "-ReceiptName", f"preflight-793-before-{prefix}.json"], check=True)
    if label == "gpt":
        prior = load(W / "claude-execution.json")
        assert prior["processExited"] and prior["exitCode"] == 0
        assert absent(prior["launcherPid"])
    resources = load(D / "review-resources.json")
    images = load(D / "original-png-scope.json")["images"]
    for resource in resources:
        assert sha(Path(resource["path"])) == resource["sha256"]
    for image in images:
        assert sha(Path(image["path"])) == image["sha256"]
    raw = W / f"{prefix}.jsonl"
    assert not raw.exists(), "Never overwrite original execution"
    prompt = (W / f"{label}-task.txt").read_text(encoding="utf-8")
    if transport:
        prior = load(W / f"{label}-execution.json")
        assert prior["processExited"] and absent(prior["launcherPid"])
        assert len({i["path"] for i in prior["successfulImageOpens"]}) == 73
        assert not prior["allOriginalImageBytesDelivered"]
        counts = {}
        for image in prior["successfulImageOpens"]:
            for payload in image["payloads"]:
                key = json.dumps({k: payload[k] for k in [
                    "equalsOriginalBytes", "pngDimensions", "originalPngDimensions"]}, sort_keys=True)
                counts[key] = counts.get(key, 0) + 1
        prompt = (
            "DEPENDENT ORIGINAL-SESSION DELIVERY-SCOPE CLARIFICATION ONLY. No new blind initial credit; "
            "no teaching/source/native change, edits or new tests. Reconcile your OWN just-completed report below "
            "against actual execution evidence. Do not reopen all resources/images or repeat the review. "
            "The coordinator requested each of the 73 ORIGINAL file paths directly, without creating or supplying "
            "rescaled substitutes, but actual CLI view binaryResultsForLlm automatically delivered PNG renditions "
            "with the following measured payload/source dimensions and byte equality counts:\n"
            + json.dumps(counts, ensure_ascii=False, indent=2)
            + f"\nThere were {len(prior['successfulImageOpens'])} successful image tool responses over73 distinct "
            "paths. Every such tool response says Viewed image file successfully and contains an image payload. "
            "These are TOOL responses, NOT proof all images were retained in every model request. "
            + ("Your report describes52 unsuccessful/image-limit reads. Actual events instead record125 successful "
               "image tool responses (52 repeated paths beyond73) and ONE session.warning image_limit: "
               "'Removed25 images from the model request to stay within the50-image request limit. "
               "User-provided images were prioritized over tool-generated images, with newer messages kept first.' "
               "Please correct the unsupported tool-failure/notice count, distinguishing actual tool return, "
               "request pruning, eventual reported visual inspection, context compaction and uncertainty. "
               if label == "gpt" else "")
            + "All assigned source text ranges were returned exactly; "
            "one tool per response/no overlap. Actual delivered image payloads are NOT original bytes/pixels. "
            "Original file hashes are still intact. Byte-distinct hashes do NOT establish distinct visual states. "
            "Your previous image observations are about those delivered renditions, not unmediated original/native "
            "pixels. This is automatic tool transport, not coordinator-controlled scaling or new independent evidence. "
            "Do not infer what a higher-resolution pixel contains. "
            "Return compact Snapshot;Scope;Verdicts;Findings;Optional;Limits clarification. State whether your bounded "
            "legibility/distinguishability, sampled semantic and inherited text verdicts still hold at the ACTUALLY "
            "delivered scale, and identify any consequential unresolved glyph/text issue if demonstrated. Explicitly "
            "leave full-resolution original-pixel/equal-comprehension/physical-phone/native-speaker evidence UNVERIFIED. "
            "Do not manufacture a failure from automatic scaling alone or convert a limitation into full-resolution "
            "approval. No new visual inspection is requested/claimed. Only your own report follows, never the other "
            "reviewer's findings.\n\n"
            + (W / f"{label}.md").read_text(encoding="utf-8")
        )
        (W / f"{prefix}-task.txt").write_text(prompt, encoding="utf-8")
    cmd = [shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
           "--model", MODELS[label], "--session-id", SESSIONS[label], "--no-ask-user",
           "--allow-tool=view", "--disable-builtin-mcps", "--available-tools=view",
           "--no-custom-instructions", "--output-format", "json",
           "--log-dir", str(W / f"{prefix}-logs"),
           "--usage-output-file", str(W / f"{prefix}-usage.json"), "-p", prompt]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("xb") as out, (W / f"{prefix}-stderr.txt").open("xb") as err:
        process = subprocess.Popen(cmd, stdout=out, stderr=err, env=env)
        save(W / f"{prefix}-active.json", {"pid": process.pid, "sessionId": SESSIONS[label],
                                         "requestedModel": MODELS[label], "startedAt": started})
        print(f"Original-session {label} reviewer PID {process.pid}; logs {raw}", flush=True)
        code = process.wait()
    save(W / f"{prefix}-process.json", {"launcherPid": process.pid, "startedAt": started,
         "completedAt": now(), "exitCode": code, "command": cmd, "processExited": absent(process.pid)})
    audit(prefix)
    frozen()


def audit(label):
    raw = W / f"{label}.jsonl"
    events = [json.loads(x) for x in raw.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
    messages = [e["data"] for e in events if e.get("type") == "assistant.message"]
    report = W / f"{label}.md"
    report_text = (messages[-1].get("content", "") if messages else "No completed report.") + "\n"
    if report.exists():
        assert report.read_text(encoding="utf-8") == report_text
    else:
        report.write_text(report_text, encoding="utf-8")
    resources = {r["path"]: r for r in load(D / "review-resources.json")}
    images = {r["path"]: r for r in load(D / "original-png-scope.json")["images"]}
    returned = {path: set() for path in resources}
    calls, active, overlaps, image_opens = {}, set(), [], []
    for e in events:
        data = e.get("data", {})
        if e.get("type") == "tool.execution_start":
            key = data["toolCallId"]
            if active:
                overlaps.append({"starting": key, "active": sorted(active)})
            active.add(key)
            calls[key] = {"name": data["toolName"], "arguments": data["arguments"],
                          "startedAt": e["timestamp"]}
        elif e.get("type") == "tool.execution_complete":
            key = data["toolCallId"]
            active.discard(key)
            result = data.get("result", {}).get("content", "")
            if not isinstance(result, str):
                result = json.dumps(result, ensure_ascii=False)
            call = calls[key]
            call.update(completedAt=e["timestamp"], success=data["success"],
                        returnedCharacters=len(result),
                        returnedSha256=hashlib.sha256(result.encode()).hexdigest(),
                        truncationMarker=any(t in result for t in [
                            "[Output truncated", "File too large to read", "<note>Content truncated",
                            "Invalid view_range"]))
            path = call["arguments"].get("path")
            if path in resources:
                lines = Path(path).read_text(encoding="utf-8").splitlines(keepends=True)
                a, b = call["arguments"].get("view_range", [1, -1])
                expected = "".join(lines[a - 1:None if b == -1 else b])
                norm = lambda s: s.replace("\r\n", "\n").rstrip()
                exact = norm(expected) in norm(result)
                call["exactRequestedTextContainedInResult"] = exact
                if exact and data["success"]:
                    returned[path].update(range(a, len(lines) + 1 if b == -1 else b + 1))
            if path in images:
                binary = data.get("result", {}).get("binaryResultsForLlm", [])
                payloads = []
                original = Path(path).read_bytes()
                for item in binary:
                    if item.get("type") == "image" and isinstance(item.get("data"), str):
                        content = base64.b64decode(item["data"], validate=True)
                        payloads.append({
                            "type": item["type"], "mimeType": item.get("mimeType"),
                            "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
                            "equalsOriginalBytes": content == original,
                            "pngDimensions": list(struct.unpack(">II", content[16:24]))
                            if content.startswith(b"\x89PNG\r\n\x1a\n") else None,
                            "originalPngDimensions": list(struct.unpack(">II", original[16:24])),
                        })
                call["imagePayloads"] = payloads
                if data["success"]:
                    image_opens.append({"path": path, "success": True,
                                        "payloads": payloads,
                                        "returnedCharacters": len(result)})
    coverage = [{"path": p, "lines": r["lines"],
                 "missingLines": sorted(set(range(1, r["lines"] + 1)) - returned[p])}
                for p, r in resources.items()]
    usage_file = W / f"{label}-usage.json"
    usage = load(usage_file) if usage_file.exists() else None
    process = load(W / f"{label}-process.json")
    family = label.split("-")[0]
    record = {
        **process, "snapshot": HEAD, "unchangedTeachingSnapshot": "08e76c1688ada4898a79e25e13650687dadf65d1",
        "sessionId": SESSIONS[family], "requestedModel": MODELS[family],
        "actualModels": sorted({m.get("model", "") for m in messages}),
        "usageCurrentModel": usage.get("currentModel") if usage else None,
        "availableTools": ["view"], "toolCalls": list(calls.values()),
        "configurationEvidence": [e["data"] for e in events if e.get("type") in [
            "session.info", "session.tools_updated"]],
        "warnings": [e for e in events if e.get("type") == "session.warning"],
        "observedToolOverlaps": overlaps, "unfinishedTools": sorted(active),
        "multiToolResponseCount": sum(len(m.get("toolRequests", [])) > 1 for m in messages),
        "textCoverage": coverage, "allAssignedTextReturned": not any(r["missingLines"] for r in coverage),
        "successfulImageOpens": image_opens,
        "missingImages": sorted(set(images) - {i["path"] for i in image_opens}),
        "allOriginalImageBytesDelivered": set(images) == {i["path"] for i in image_opens}
        and all(any(p["equalsOriginalBytes"] for p in i["payloads"]) for i in image_opens),
        "successfulImageOpenCount": len(image_opens),
        "distinctSuccessfulImagePaths": len({i["path"] for i in image_opens}),
        "distinctDeliveredOriginalHashes": len({
            p["sha256"] for i in image_opens for p in i["payloads"] if p["equalsOriginalBytes"]}),
        "rawExecutionSha256": sha(raw), "reportSha256": sha(report), "usage": usage,
        "limits": "Process/tool/returned-byte audit is not comprehension or full-resolution image certification. Successful image tool results require separate payload/visual-delivery inspection."
    }
    execution_path = W / f"{label}-execution.json"
    if execution_path.exists():
        initial = W / f"{label}-initial-audit.json"
        assert not initial.exists()
        shutil.copyfile(execution_path, initial)
    save(execution_path, record)
    print(json.dumps({k: record[k] for k in [
        "actualModels", "exitCode", "processExited", "allAssignedTextReturned",
        "observedToolOverlaps", "multiToolResponseCount", "missingImages"]}))


if __name__ == "__main__":
    {"prepare": prepare, "run": lambda: run(sys.argv[2]),
     "transport": lambda: run(sys.argv[2], transport=True),
     "audit": lambda: audit(sys.argv[2])}[sys.argv[1]]()
