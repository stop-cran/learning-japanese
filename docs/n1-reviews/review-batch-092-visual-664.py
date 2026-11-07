import base64
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
V = R / "docs" / "n1-reviews"
N = V / "batch-092-native" / "execution-663"
L = C / "logs" / "263029da-d7c3-4b2a-a042-b89f35767592"
HEAD = "09c9cfde7513a0dc7a7ca5a07d28131a3476015f"
TEACHING = "6246dc622f7139c2a0e16d2e03847d6494391fae"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PACKET = C / "batch-092-visual-664-packet.txt"
SESSIONS = {
    "claude": ("claude-opus-5.5", "2f27854e-184a-4f54-8d7d-962197573318"),
    "gpt": ("gpt-6.1-sol", "4ff2dfd7-8eed-456f-8f4d-4acd64d2a820"),
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now().astimezone().isoformat()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def absent(pid):
    return subprocess.run(
        ["pwsh", "-NoProfile", "-Command",
         f"if(Get-Process -Id {int(pid)} -ErrorAction SilentlyContinue){{exit 1}}"],
        capture_output=True,
    ).returncode == 0


def ownership():
    command = r"""
$ErrorActionPreference='Stop'
$runner=Get-Content 'C:\Users\stop-\n1-kanji-workspace\control\runner.json' -Raw | ConvertFrom-Json
if($runner.pid -ne 19008 -or $runner.sessionId -ne '263029da-d7c3-4b2a-a042-b89f35767592'){throw 'Runner identity uncertain'}
$p=Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while($p -and $p.ProcessId -ne 19008){$p=Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)"}
if(-not $p){throw 'Expected live parent ancestry not established'}
$command=$p.CommandLine
if($command -match '(?i)-EncodedCommand\s+([A-Za-z0-9+/=]+)'){
 $command=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
}
if(-not $command.Contains('C:\Users\stop-\n1-kanji-workspace\control\runner.ps1')){throw 'Parent launcher command uncertain'}
"""
    subprocess.run(["pwsh", "-NoProfile", "-Command", command], check=True, capture_output=True)


def frozen():
    ownership()
    for root, expected in [(R, HEAD), (A, ANDROID)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 663 and state["batch"] == "092"
    assert not git("diff", TEACHING, HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")


def prepare():
    frozen()
    assert not PACKET.exists()
    backup = L / "progress-before-664.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["execution663CoordinatorCheckpoint"]["savedCommit"] == HEAD
    state = load(C / "progress.json")
    state["execution664StartingState"] = {
        "execution": 664, "batch": "092", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID,
        "scope": "SAME092 original Claude then original GPT serial dependent visual confirmations; signed LOCAL evidence only; no publication/093.",
        "request": {
            "sha256": sha(request), "bytes": request.stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final663 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": "Live parent19008 ancestry, exact session and decoded launcher verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed source/evidence only; no optional historical session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    state.update(
        stage="batch-092-original-session-dependent-visual-confirmations",
        nextAction="SAME092 serial original Claude then original GPT rendered follow-ups; preserve actual reports, model identity, image returns and process/tool serialization before local reconciliation. No publication/093.",
    )
    save(C / "progress.json", state)
    for name, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-092-visual-cli-{name}-664.txt").write_bytes(result.stdout)
    catalog = (C / "batch-092-visual-cli-config-664.txt").read_text(encoding="utf-8-sig")
    assert all(f'"{model}"' in catalog for model, _ in SESSIONS.values())
    help_text = (C / "batch-092-visual-cli-help-664.txt").read_text(encoding="utf-8-sig")
    assert "--available-tools" in help_text and "--resume" in help_text
    evidence = load(R / "docs" / "n1-sources" / "execution-663.json")
    for item in evidence["artifacts"]:
        assert sha(R.joinpath(*item["path"].split("/"))) == item["sha256"]
    images = [N / item["file"] for item in evidence["visualInspection"]["inspectedOriginalPngs"]]
    assert len(images) == 25
    parts = [
        f"DEPENDENT VISUAL FOLLOW-UP: signed HEAD {HEAD}; unchanged teaching {TEACHING}.",
        "Not new blind initial review. No other reviewer's report or coordinator visual opinions included. Native assertions are supplied receipts, NOT reviewer-executed tests.",
    ]
    for path in [R / "kanji" / "\u5208.md", R / "words" / "\u5208\u308b.md",
                 N / "n1-092-article-route.json"]:
        parts.append(f"RESOURCE {path}; SHA256 {sha(path)}\n{path.read_text(encoding='utf-8-sig')}")
    parts.append("NATIVE EXECUTION RECEIPT ONLY:\n" +
                 json.dumps(evidence["executionReceipt"], ensure_ascii=False, indent=2))
    parts.append("EXACT REUSED SUPPORT DIFF:\n" + git(
        "-c", "core.quotepath=false", "diff",
        "40c5160cc3b92077a886720084ba3d18454a4859", TEACHING,
        "--", "words/\u5208\u308b.md"))
    parts.append("TEACHING DIFF BETWEEN INITIAL REVIEW AND CURRENT HEAD (empty):\n" +
                 git("diff", TEACHING, HEAD, "--",
                     "kanji", "words", "articles", "strokes", "manifest.json"))
    parts.append("VIEW THESE 25 ORIGINAL PNGS IN THIS ORDER, ONE AT A TIME:\n" +
                 "\n".join(map(str, images)))
    PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(C / "batch-092-visual-664-inputs.json", {
        "packet": {"path": str(PACKET), "sha256": sha(PACKET)},
        "images": [{"path": str(p), "sha256": sha(p)} for p in images],
        "capturedPngs": 42, "assignedOriginalPngViews": 25,
        "remainingPngsNotAssigned": 17,
        "head": HEAD, "teachingSnapshot": TEACHING,
        "sourceEvidence": "docs/n1-sources/execution-663.json",
        "sourceEvidenceSha256": sha(R / "docs" / "n1-sources" / "execution-663.json"),
    })
    print("Prepared", PACKET.stat().st_size, "bytes; 25 original PNGs; historical state retained.")


def make_prompt(label, model, session):
    return f"""Resource-constrained SERIAL visual-inspection operation in your ORIGINAL session {session}, actual model {model}.
DEPENDENT follow-up, NOT a new blind initial review. Signed evidence HEAD {HEAD}; unchanged teaching {TEACHING}.
Task acceptance requires EXACTLY ONE view call per assistant message. Interpret each image before deciding to read the next; that dependency forbids batching. Do not use parallel tool calls or a wrapper. An otherwise successful report with overlapping calls is NOT accepted.
FIRST read ONLY your own original report {V / ('batch-092-initial-' + label + '.md')}.
In a SEPARATE subsequent assistant message read ENTIRE {PACKET}, forceReadLargeFiles=true, no range.
Then view ALL25 ORIGINAL PNGs listed at its end IN ORDER, ONE tool call per message, waiting for each result. No edits, shell, delegation, other reports or coordinator opinions; only view is exposed.
If vision unavailable or text truncated, disclose and recover missing ranges serially, never substitute hash/cmap/hasGlyph for viewing.

Assess EACH complete kanji\\刈.md and reused words\\刈る.md (only componentlink/direct収穫guard changed). Inherit your own textual correctness/coverage unless images establish a defect. Both unrestricted刈除 readingsがいじょ/かいじょ recognized/unselected, no frequency/obsolete claim. Rawonガイ,カイ then kunか.る sourceorder kept; onlykunかる selected, ownlinkedrow/か+writtenる. Nativegodan/transitive/objectを/result短く/cutting-growing-things and cutting-versus-all-harvesting distinctions; shape-onlymnemonic not history, canonical刀18 versus visible刂. ExistingN3 identity/reading/title/original切るguard unchanged. No fresh dictionary retrieval claim.
Inspect all16 scopedHan in THREE actualCompose panels across FOUR production fontselections Gothic/Mincho/Textbook/Brush, especially fallbackU+5202刂 and 刈/切/刀/乃/凹/凸 distinction and whole刈除. 64individual+4wholewordPaint probes are NOT68exported/viewedPNGs or identifiedfallbackface. Readability/distinguishability, not uniformfontcosmetics, is the gate.
Inspect BOTH complete article projections using complementary original views and supplied fulltext/native-scrollassertions. Readingtable is horizontally scrollable; complementary views, not simultaneousfullcolumnvisibility, are intended. If assignedviews do not establish something, state the limitation; additional originals in {N} available only if needed. Selected25of42 images are NOT42freshviews; remaining17 not separately assigned. Some routeimages are exactduplicates, not independentrenderings.
Inspect N1selection124cards, actual pictured meaningoption labels mow;reap versus concave;sunken/convex;protruding/thereupon;possessive no. Production N1 AND All exactthreecuratedwrongcards/zerofallback are suppliedreceipt evidence unless pictured. Close ownpriorunverifiedfallbacklimit ONLY testedconfigurations, not everyfuturecustompool/oldclient.
Inspect onlykunかる question/correctfeedback/1of1Done; noonkey offered. Fullrawreference readings in feedback are NOTextraofferedkeys; full/Lite equality/persistedGood keys are suppliedreceipt. Inspect fourpinnedstrokes/injectedtrace/practicefeedback/recallgiveup. ActualUI explicitlymodelunavailable/shape-onlygrading: NOThumanhandwriting/successfulMLKit/phone.
ONEallmappedbaselinepair刈/刈る/TWOdirections and forward/backlink/SystemBack/offlineroute; directguards are not a synonymclique.
Supplied fullarchive62c6d3e2 through productionContentSyncONCE imported1115kanji5070words124N1zeroProblems/contentVersion8445a5717d080dcc/acceptedRoomreadingEpoch1. TWOcases terminalpercase0/noskips; own helper5580 stopped. These are supplied receipts, not your tests. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. No newphysicalphone acceptance.

Return COMPLETE report: Snapshot;Scope(actualmodel, actualtext/image reads);Verdicts(correctness/scopedcoverage/renderedcomprehensibility EACHarticle, identify inheritedtextualconclusions);Findings(severity;facet;file/PNG:location;preciseclaim+impact;remedy;evidence;confidence ornone);Optional;Limits.
Reconcile OWN prior limitations; preserve optional suggestions/residualuncertainty. Disclose tool-resizedimages, unviewed17originals, sourceandmodelreadlimits, unverifiedfallbackface/Paintimages. API35emulator is notphysicalphone/native-speaker/measuredlearning. No newblindinitialcredit. Currentmain/combinedchecks/CI/publicZIP/publication/phone/generalrelease/whole-set remain latergates. No edits/questions/nextbatch.
"""


def run(label):
    frozen()
    if label == "gpt":
        prior = load(C / "batch-092-visual-664-claude-execution.json")
        assert prior["exitCode"] == 0 and not prior["observedToolOverlaps"]
        assert not prior["unfinishedTools"] and prior["allAssignedResourcesSuccessfullyReturned"]
        assert absent(prior["launcherPid"]), "Previous reviewer process still present"
    inputs = load(C / "batch-092-visual-664-inputs.json")
    assert sha(PACKET) == inputs["packet"]["sha256"]
    images = [Path(i["path"]) for i in inputs["images"]]
    assert all(sha(Path(i["path"])) == i["sha256"] for i in inputs["images"])
    model, session = SESSIONS[label]
    prefix = C / f"batch-092-visual-664-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    prompt = make_prompt(label, model, session)
    prefix.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    command = [
        shutil.which("copilot"), "-C", str(R), "--add-dir", str(C),
        "--resume=" + session, "--model", model, "--no-ask-user",
        "--allow-tool=view", "--available-tools=view", "--disable-builtin-mcps",
        "--no-custom-instructions", "--output-format", "json",
        "--log-dir", str(C / "review-logs" / prefix.name),
        "--usage-output-file", str(prefix.with_suffix(".usage.json")), "-p", prompt,
    ]
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    started = now()
    with raw.open("wb") as out, prefix.with_suffix(".stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=env)
        save(prefix.with_suffix(".active.json"),
             {"pid": process.pid, "sessionId": session, "model": model, "startedAt": started})
        print("Started original-session dependent review", process.pid, session, model, flush=True)
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        (messages[-1].get("content", "") if messages else "No completed report.") + "\n", encoding="utf-8")
    required = {str(PACKET), str(V / f"batch-092-initial-{label}.md"), *map(str, images)}
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
            call.update({
                "completedAt": event["timestamp"], "success": data["success"],
                "returnedCharacters": len(result),
                "returnedSha256": hashlib.sha256(result.encode()).hexdigest(),
                "truncationMarker": any(s in result for s in [
                    "[Output truncated", "File too large to read",
                    "<note>Content truncated", "Invalid view_range"]),
            })
            path = call["arguments"].get("path")
            if path in required and data["success"] and not call["truncationMarker"]:
                if path.endswith(".png"):
                    payloads = data.get("result", {}).get("binaryResultsForLlm", [])
                    assert len(payloads) == 1 and payloads[0]["mimeType"] == "image/png"
                    payload = base64.b64decode(payloads[0]["data"], validate=True)
                    with Image.open(io.BytesIO(payload)) as image:
                        image.load()
                        dimensions = list(image.size)
                    decoded.append({
                        "path": path, "sourceSha256": sha(Path(path)),
                        "returnedSha256": hashlib.sha256(payload).hexdigest(),
                        "returnedDimensions": dimensions, "returnedBytes": len(payload),
                    })
                    returned.add(path)
                else:
                    norm = lambda s: s.replace("\r\n", "\n").rstrip()
                    exact = norm(Path(path).read_text(encoding="utf-8-sig")) in norm(result)
                    call["entireRequestedTextContained"] = exact
                    if exact:
                        returned.add(path)
    usage = load(prefix.with_suffix(".usage.json")) if prefix.with_suffix(".usage.json").exists() else None
    record = {
        "execution": 664, "batch": "092", "snapshot": HEAD, "teachingSnapshot": TEACHING,
        "dependentOriginalSession": True, "newBlindInitialReviewCredit": False,
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
        "limits": "Payload audit establishes delivery and serialization, not comprehension. Dependent original-session review, not new blind initial coverage. 25 of42 original PNGs assigned.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    assert absent(process.pid), "Reviewer must exit before its result is accepted"
    frozen()
    print(json.dumps({k: record[k] for k in [
        "exitCode", "actualModels", "missingResources", "observedToolOverlaps"]}), flush=True)
    assert code == 0 and record["actualModels"] == [model] and usage["currentModel"] == model
    assert not active and not overlaps and not (required - returned)
    assert [i["path"] for i in decoded] == list(map(str, images))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] in SESSIONS:
        run(sys.argv[1])
    else:
        raise ValueError(sys.argv[1])
