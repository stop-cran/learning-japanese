import base64
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
V = R / "docs" / "n1-reviews"
L = C / "logs" / "e4c9335d-36a1-412f-9b3f-ffd733c97de2"
HEAD = "4d6ea7640109a90a510d94083480b7c33c6e7ab2"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SESSION = L.name
PNG = V / "batch-091-native" / "execution-654" / "n1-091-kanji-04.png"
SESSIONS = {
    "claude": ("claude-opus-5.5", "075924f2-f60b-4ae0-bf3f-341db3dfbd74"),
    "gpt": ("gpt-6.1-sol", "8da57d75-100b-4996-acf7-f52b0b446472"),
}
STAGE = "revised-rendering-confirmed-awaiting-combined-current-main-acceptance"
NEXT = (
    "SAME091 only: read docs/n1-sources/execution-655.json and "
    "docs/n1-reviews/batch-091-rendered-reconciliation-655.json. "
    "Both original reviewer sessions serially inspected their own prior report, complete unchanged "
    "kanji article and NEW native654 mnemonic PNG on signed4d6ea764. Dependent revised-layout "
    "confirmation only, no new blind-review credit; preserve original GPT non-discovery and "
    "Claude651 overlap violation. V1 text resolved653; revised import/rendering654 and dependent "
    "rendered confirmation655 complete within exact recorded scope. Next bounded checkpoint: "
    "fetch current main, normal non-rewriting merge if needed, regenerate derived output and run "
    "ALL combined-tree content/Python/vocabulary/baseline/link/membership/reading/font/budget/"
    "applicable Android acceptance gates; independently review any substantive teaching change. "
    "Do not blindly rerun unchanged native/source/review work. No publication until all gates pass; "
    "then normal signed owner fast-forward, terminal green CI and EVERY immutable public ZIP "
    "runtime hash plus unchanged18000entries/42MiBcompressed/80MiBinflated/56MiBretained/"
    "perfile-media-safepath guards, owner issue receipt and checkpoint. No092/newrunner. "
    "Parent19008 owns runner.lock: verify live ancestry/exact session/decoded launcher/"
    "checkpoint/exact signed heads/whollyclean; NO child reacquire/delete/unlock. "
    "Approved control and committed evidence only; no optional historicalsessionhelpers. "
    "Preserve/report/yield actual new denial/signinghang/uncertainownership. "
    "Native654 one terminalcase0/no skips/full archivefe3ec10b/ContentSyncONCE/"
    "versionbfe65483a821fc13/1114kanji5070words123N1/zeroProblems/Roomepoch1; "
    "GlyphTest NOT rerun, inherit650 limits. Test-onlyAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOT latestappmain. Unknown fallbackface/Paintprobe/injectedtrace/no successfulMLKit/"
    "source/read/native-emulator limits remain. Published117/1228,1111remaining; "
    "physicalphone/generalrelease/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args, repo=R):
    return subprocess.check_output(["git", "-C", str(repo), "--no-pager", *args],
                                   encoding="utf-8").strip()


def ownership():
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == SESSION
    script = f"""
$ErrorActionPreference='Stop'
$id={os.getpid()}; $chain=@()
while($id -gt 0){{
  $p=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
  if(!$p){{break}}
  $chain+=@{{pid=[int]$p.ProcessId;parent=[int]$p.ParentProcessId;name=$p.Name;command=$p.CommandLine}}
  if($id -eq 19008){{break}}
  $id=$p.ParentProcessId
}}
$chain | ConvertTo-Json -Depth 4 -Compress
"""
    chain = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert chain[-1]["pid"] == 19008
    assert any(p["name"].lower() == "copilot.exe" and SESSION in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    decoded = base64.b64decode(encoded).decode("utf-16-le")
    assert str(C / "runner.ps1") in decoded
    return {"parentRunnerPid": 19008, "sessionId": SESSION,
            "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
            "launcherCommandMatches": True, "parentLockTouched": False}


def frozen(final=False):
    proof = ownership()
    assert git("rev-parse", "HEAD^" if final else "HEAD") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 654 and state["batch"] == "091"
    return proof


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for kind, section in manifest.items():
        if isinstance(section, dict):
            for path, expected in section.items():
                if isinstance(expected, str) and len(expected) == 64:
                    file = R.joinpath(*path.split("/"))
                    actual = sha(file) if kind in {
                        "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                    } else sha256(file)
                    assert actual == expected, path
                    count += 1
    assert count == 8432 and manifest["contentVersion"] == "bfe65483a821fc13"
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    return {"runtimeHashesVerified": count, "manifestFresh": True,
            "contentVersion": manifest["contentVersion"], "manifestSha256": sha(R / "manifest.json"),
            "runtimeUnchangedFromSignedNativeSnapshot": True}


def prepare():
    proof = frozen()
    backup = L / "progress-before-655.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["batch091RevisedNativeCheckpoint"]["savedCommit"] == HEAD
    state = load(C / "progress.json")
    state["execution655StartingState"] = {
        "execution": 655, "batch": "091", "startedAt": now(), "startingHead": HEAD,
        "androidHead": ANDROID, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME091 smallest serial original-session NEW mnemonic PNG confirmations; signed LOCAL evidence only, no publication/092.",
        "request": {"sha256": sha(request), "bytes": request.stat().st_size,
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete issue and final654 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": proof,
        "artifactPathPreflight": "Approved control and committed source/review evidence only; no optional historical session helpers accessed.",
        "actualNewPermissionDenials": [],
    }
    state.update(stage="batch-091-revised-rendering-original-session-confirmations",
                 nextAction="SAME091 original Claude then GPT serial dependent confirmation of the NEW654 mnemonic PNG; archive complete reports/process evidence and persist signed local checkpoint.")
    save(C / "progress.json", state)
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-091-rendered-cli-{kind}-655.txt").write_bytes(result.stdout)
    print("Starting state persisted; exact signed clean worktrees and parent ownership verified.", flush=True)


def review(label):
    frozen()
    if label == "gpt":
        previous = load(C / "batch-091-rendered-655-claude-execution.json")
        assert previous["acceptedExecution"]
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {previous['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       capture_output=True, check=True)
    model, session = SESSIONS[label]
    assert f'"{model}"' in (C / "batch-091-rendered-cli-config-655.txt").read_text(encoding="utf-8-sig")
    prefix = C / f"batch-091-rendered-655-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    resources = [V / f"batch-091-mnemonic-653-{label}.md", R / "kanji" / "\u5203.md", PNG]
    prompt = f"""DEPENDENT revised-native-rendering confirmation in ORIGINAL session {session}; requested model {model}.
Frozen signed HEAD {HEAD}; no uncommitted changes. This is NOT a fresh blind initial review.
Exactly ONE view call per response, wait for result before next. Serial inspection is the actual operation; overlapping tools invalidate acceptance.
Only read-only view is exposed; no shell, edits, delegation, other reports, broad dictionary/image rereads or questions.
Read these THREE resources COMPLETELY IN THIS ORDER, one call per response:
{chr(10).join(map(str, resources))}
Your own complete653 report is supplied, not the other reviewer's. No teaching has changed since your653 confirmation of signed1cfd5bd3.
The NEW third resource is native654's original900x2000 capture of CURRENT contentVersion bfe65483a821fc13, not old650/653 PNG evidence.
Inspect the decoded image freshly. Compare the entire revised mnemonic paragraph against the complete article, especially separate-stroke/font qualification, crossing diagram explanation and explicit nonhistorical disclaimer.
Assess ONLY this paragraph's native readability/layout/comprehensibility and bounded regression. Do not recertify unchanged words/readings/quiz/strokes or manufacture findings.
Coordinator supplied receipts, NOT your own tests: native654 imported full archivefe3ec10b through production ContentSync ONCE,1114kanji/5070words/123N1/zeroProblems/Roomepoch1;
one selected ArticleTest terminalcase0/no skips. Forty-seven new captures preserved; coordinator viewed only this one. Unchanged GlyphTest NOT rerun; inherit650 font evidence and limits.
Qualified test-onlyAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain; API35 emulator, not phone. Unknown fallbackface/Paintprobe/injectedtrace/not human handwriting/no successfulMLKit limits remain.
V1 text resolved653; your earlier non-discovery or optional suggestions stay historical, not rewritten agreement. Claude651 overlap violation remains rejected; this follow-up must itself be serial.
State whether revised-version-rendering limitation is resolved/partially resolved within this exact screenshot scope, distinguishing retained broader limitations.
Return concise complete report with Snapshot;Scope(actual model and exact resources);Verdicts(correctness/scopedcoverage/comprehensibility for changed kanji; unchanged word inherited);Findings(severity/facet/file:line/claim+impact/remedy/evidence/confidence or none);Optional;Limits.
Do NOT treat hashes as viewing or claim tests/upstream/fontface/device evidence you did not perform. Currentmain/combinedchecks/CI/publicZIP/publication/phone/generalrelease/whole-set remain outside scope.
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
    accepted = (code == 0 and models == [model] and usage.get("currentModel") == model
                and not active and not overlaps and len(calls) == 3
                and all(call["name"] == "view" for call in calls.values())
                and returned == list(map(str, resources)))
    record = {
        "execution": 655, "batch": "091", "snapshot": HEAD, "sessionId": session,
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
        "limits": "Complete returned resources and serial process audited, not proof of comprehension; exact one revised native image, not all47captures or physical phone.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({k: record[k] for k in ["exitCode", "actualModels", "acceptedExecution", "observedToolOverlaps"]}), flush=True)
    frozen()
    assert accepted, "Preserve incomplete evidence and yield; do not silently accept"


def archive():
    frozen()
    verification = runtime()
    records = [load(C / f"batch-091-rendered-655-{label}-execution.json") for label in SESSIONS]
    assert records[0]["completedAt"] < records[1]["startedAt"]
    for record in records:
        assert record["acceptedExecution"] and record["exitCode"] == 0
        assert len(record["toolCalls"]) == 3 and len(record["actualDecodedImageReturns"]) == 1
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       capture_output=True, check=True)
    receipts = []
    sources = [Path(__file__), C / "post-batch-091-rendered-655.ps1"]
    sources += [C / f"batch-091-rendered-cli-{kind}-655.txt" for kind in ["help", "config"]]
    for label, record in zip(SESSIONS, records):
        prefix = C / f"batch-091-rendered-655-{label}"
        raw = prefix.with_suffix(".jsonl")
        assert sha(raw) == record["rawSha256"]
        assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
        target = V / (raw.name + ".gz")
        assert not target.exists()
        with target.open("wb") as file:
            with gzip.GzipFile(filename="", mode="wb", fileobj=file, mtime=0) as compressed:
                compressed.write(raw.read_bytes())
        assert gzip.decompress(target.read_bytes()) == raw.read_bytes()
        receipts.append({"source": str(raw), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(raw), "archiveSha256": sha(target), "losslessGzip": True})
        sources += [prefix.with_suffix(s) for s in [
            ".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"]]
        sources.append(C / (prefix.name + "-execution.json"))
    for source in sources:
        target = V / source.name
        assert not target.exists()
        shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(target)})
    evidence = {
        "schemaVersion": 1, "execution": 655, "batch": "091", "status": STAGE,
        "reviewedSnapshot": HEAD, "dependentOriginalSessionConfirmations": records,
        "newBlindInitialReviewCredit": False, "originalReportsAndProcessViolationsPreserved": True,
        "reconciliation": [{
            "id": "V1", "severity": "minor", "facet": "rendered comprehensibility",
            "file": "kanji/\u5203.md:24", "status": "resolved",
            "priorDisposition": "Text resolved653; native revised-version import/rendering confirmed654, original-reviewer rendered confirmation pending.",
            "currentDisposition": "Both original sessions confirm complete revised mnemonic readable and unclipped in the new654 capture; no established regression. Revised-rendering limitation resolved for exact paragraph/screenshot, only partially resolved more broadly.",
            "evidence": PNG.relative_to(R).as_posix(), "imageSha256": sha(PNG),
            "claudeDisposition": "Original localized V1 remains resolved; exact new native layout confirmed. Optional detached/direction/here wording remains optional.",
            "gptDisposition": "No prior defect discovery; unchanged history, no retroactive agreement. Exact revised native layout now confirmed.",
            "processDisposition": "Both exited0; three complete serial views and one actual decoded PNG each; zero overlaps/unfinished tools. Original Claude651 overlap violation remains rejected, not repaired retroactively.",
            "confidence": "High for exact pictured paragraph and supplied native654 provenance; no universal device/font/learning-effectiveness claim.",
        }],
        "findings": [],
        "optional": [
            "No new optional suggestion. Retain all original optional notes/hypotheses and exact source/read limitations; no expansion required.",
        ],
        "validation": verification, "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "nativeReceipt": "docs/n1-sources/execution-654.json",
        "visualScope": {"capturedPngs": 47, "newPngsViewedPerReviewer": 1,
                        "remainingNewPngsNotViewedPerReviewer": 46,
                        "coordinatorViewedSameOnePng": True},
        "limits": [
            "Dependent original-session rendering confirmation, not new blind initial review or native-speaker certification.",
            "Tool/process/payload audit proves resource delivery, not comprehension. View image return is resized; original PNG preserved.",
            "Native654 import/test/version assertions are inherited coordinator receipts, not reviewer tests or fresh native655 execution.",
            "Qualified test-onlyAndroid1c1b7bf4 retaining productionf9b59a2 is NOT latestappmain; API35 emulator not physical phone.",
            "GlyphTest NOT rerun; inherit650 exact font evidence, unknown fallbackface/Paintprobe, injectedtrace/no successfulMLKit limitations.",
            "Currentmain integration, all combined acceptance checks, CI, public ZIP, publication, physicalphone/generalrelease/whole-set outstanding.",
        ],
        "nextAction": NEXT,
    }
    save(V / "batch-091-rendered-reconciliation-655.json", evidence)
    save(R / "docs" / "n1-sources" / "execution-655.json", {
        "schemaVersion": 1, "execution": 655, "batch": "091", "status": STAGE,
        "startingState": load(C / "progress.json")["execution655StartingState"],
        "reviewRecord": "docs/n1-reviews/batch-091-rendered-reconciliation-655.json",
        "receipts": receipts, "runtime": verification,
        "twoFamilyDependentRenderedConfirmation": "complete",
        "reviewerProcessesLaunched": 2, "serialProcessAndToolsVerified": True,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": "7100a3873282b54515b9ef130766e77cf151a47b",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Both complete serial rendered confirmations archived; runtime untouched.", flush=True)


def finalize():
    frozen(final=True)
    verification = runtime()
    source = R / "docs" / "n1-sources" / "execution-655.json"
    evidence = load(source)
    expected_names = {item["archive"] for item in evidence["receipts"]}
    expected_names.update({
        source.relative_to(R).as_posix(),
        "docs/n1-reviews/batch-091-rendered-reconciliation-655.json",
    })
    names = subprocess.check_output(
        ["git", "-C", str(R), "diff", "--name-only", "-z", HEAD, "HEAD"]).decode("utf-8").split("\0")
    assert set(filter(None, names)) == expected_names
    for item in evidence["receipts"]:
        file = R.joinpath(*item["archive"].split("/"))
        assert sha(file) == item["archiveSha256"]
        if item.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(file.read_bytes())).hexdigest() == item["sourceSha256"]
    prefix = str(C / "batch-091-rendered-655-issue-")
    body = Path(prefix + "body.txt").read_bytes().decode("utf-8-sig")
    receipt = load(Path(prefix + "receipt.json"))
    posted = load(Path(prefix + "posted.json"))
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = load(C / "progress.json"), load(L / "progress-before-655.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[key] == value for key, value in before.items() if key not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 655, "checkpoint": 655, "batch": "091",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-655.json",
        "reviewRecord": "docs/n1-reviews/batch-091-rendered-reconciliation-655.json",
        "twoFamilyDependentRenderedConfirmation": "complete", "V1": "resolved",
        "originalClaudePid": 27896, "originalGptPid": 24700,
        "bothReviewerProcessesExited": True, "serialViewCallsPerReviewer": 3,
        "decodedNewPngsPerReviewer": 1, "observedToolOverlaps": 0,
        "priorClaudeToolOverlapViolationPreserved": True,
        **verification, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": "7100a3873282b54515b9ef130766e77cf151a47b",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    state.update(checkpoint=655, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution655CoordinatorCheckpoint"] = checkpoint
    state["batch091RevisedRenderedCheckpoint"] = checkpoint
    state["execution655StartingState"]["status"] = "signed-local-revised-rendering-confirmation-checkpoint-complete"
    save(C / "progress.json", state)
    reread = load(C / "progress.json")
    assert all(reread[key] == value for key, value in before.items() if key not in allowed)
    save(L / "checkpoint-655.json", checkpoint)
    print("Persisted checkpoint655; original historical root values preserved:", len(before), flush=True)
    print(checkpoint["savedCommit"], receipt["html_url"], flush=True)


if __name__ == "__main__":
    action = sys.argv[1]
    if action in {"prepare", "archive", "finalize"}:
        {"prepare": prepare, "archive": archive, "finalize": finalize}[action]()
    else:
        review(action)
