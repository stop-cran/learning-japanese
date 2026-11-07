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

C = Path(__file__).parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
V = R / "docs" / "n1-reviews"
N = V / "batch-089-native" / "execution-632"
L = C / "logs" / "cb82a0d8-5174-4b40-8f66-1fe1551fb391"
HEAD = "cc8e90416d207d879058c22e493fbba78a2b3603"
TEACHING = "4b84608b5ca8889d45a176667975524f6645bd8d"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SESSIONS = {
    "claude": ("claude-opus-5.5", "a56b5dcb-9fed-4785-848e-41708f65598f"),
    "gpt": ("gpt-6.1-sol", "3286add7-2824-4df6-933a-c8bba3890927"),
}
PACKET = C / "batch-089-visual-633-packet.txt"
IMAGES = [N / "inspection" / f"contact-{i:02d}.png" for i in range(1, 9)]
IMAGES += [N / f"n1-089-font-panel-{i}.png" for i in (1, 2, 3)]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now().astimezone().isoformat()


def git(*args, repo=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(repo), *args], encoding="utf-8"
    ).strip()


def frozen():
    assert git("rev-parse", "HEAD") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    state, runner = load(C / "progress.json"), load(C / "runner.json")
    assert state["checkpoint"] == 632 and state["batch"] == "089"
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name
    command = (
        '$p=Get-CimInstance Win32_Process -Filter "ProcessId=$PID";'
        "$found=$false; while($p){if($p.ProcessId -eq 19008){$found=$true;break};"
        '$p=Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)"};'
        "if(-not $found){exit 1}"
    )
    subprocess.run(["pwsh", "-NoProfile", "-Command", command], check=True, capture_output=True)
    assert not git("diff", TEACHING, HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")


def prepare():
    frozen()
    assert not PACKET.exists()
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["execution632CoordinatorCheckpoint"]["savedCommit"] == HEAD
    shutil.copyfile(C / "progress.json", L / "progress-before-633.json")
    state = load(C / "progress.json")
    state["execution633StartingState"] = {
        "execution": 633, "batch": "089", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME089 original-session serial dependent visual confirmations; signed LOCAL evidence only; no publication/090.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete issue and final632 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 verified through current child ancestry and exact runner session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed sources only; no optional historical session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-089-dependent-visual-confirmations"
    state["nextAction"] = "SAME089 original Claude then original GPT serial dependent visual confirmations, preserving full reports/process limits; local evidence checkpoint only."
    save(C / "progress.json", state)
    parts = [
        f"DEPENDENT VISUAL EVIDENCE: frozen signed HEAD {HEAD}; unchanged teaching {TEACHING}.",
        "Not new blind review. Native assertions below are supplied receipts, NOT reviewer-executed tests. No other reviewer's report or coordinator visual opinions are included.",
    ]
    for path in [R / "kanji" / "\u51f6.md", R / "words" / "\u51f6\u4f5c.md",
                 N / "execution.json", N / "n1-089-article-route.json",
                 N / "inspection" / "contact-map.json"]:
        parts.append(f"RESOURCE {path}; SHA256 {sha(path)}\n{path.read_text(encoding='utf-8-sig')}")
    parts.append("ONLY CHANGED REUSED PASSAGE:\n" + git(
        "diff", TEACHING + "^", TEACHING, "--", "kanji/\u4f5c.md"))
    parts.append("EXACT TEACHING DIFF FROM INITIAL REVIEW TO CURRENT HEAD:\n" + git(
        "diff", TEACHING, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json"))
    parts.append("VIEW ALL ACTUAL PNGS SERIALLY:\n" + "\n".join(map(str, IMAGES)))
    PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(C / "batch-089-visual-633-inputs.json", {
        "packet": {"path": str(PACKET), "sha256": sha(PACKET)},
        "images": [{"path": str(p), "sha256": sha(p)} for p in IMAGES],
        "head": HEAD, "teachingSnapshot": TEACHING,
    })
    print("Prepared", PACKET.stat().st_size, "bytes;", len(IMAGES), "images")


def run(label):
    frozen()
    model, session = SESSIONS[label]
    if label == "gpt":
        prior = load(C / "batch-089-visual-633-claude-execution.json")
        assert prior["exitCode"] == 0 and prior["allAssignedResourcesSuccessfullyReturned"]
        assert not prior["unfinishedTools"] and not prior["observedToolOverlaps"]
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {prior['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       check=True, capture_output=True)
    prefix = C / f"batch-089-visual-633-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    assert f'"{model}"' in (C / "batch-089-visual-cli-config-633.txt").read_text(encoding="utf-8-sig")
    inputs = load(C / "batch-089-visual-633-inputs.json")
    assert sha(PACKET) == inputs["packet"]["sha256"]
    assert all(sha(Path(i["path"])) == i["sha256"] for i in inputs["images"])
    prompt = f"""DEPENDENT visual follow-up in your ORIGINAL session {session}, actual model {model}.
Frozen signed HEAD {HEAD}; unchanged initial teaching {TEACHING}. NOT new blind initial review.
MANDATORY: EXACTLY ONE view call PER assistant response, starting with the TWO TEXT reads. Never batch text or image reads; wait for each result before requesting the next.
FIRST read ONLY your own original report {V / ('batch-089-initial-' + label + '.md')}.
In a SEPARATE subsequent response read the ENTIRE {PACKET} with forceReadLargeFiles=true.
Then view ALL ELEVEN PNG paths at its end, ONE call per response, SERIALLY: eight mapped whole-frame contact sheets cover all43captures; three separate original Compose font panels. Additional originals under {N} are available if legibility requires. No other reports/opinions, shell, edits, delegation or parallel calls; only view is exposed.
If vision/decoding unavailable or text truncated, disclose and recover missing ranges serially; never substitute hashes/cmap/hasGlyph for viewing.

Assess EACH new kanji\\凶.md, new words\\凶作.md, and ONLY changed reused kanji\\作.md navigation line. Inherit original textual correctness/coverage unless images establish a defect; no fresh dictionary-retrieval claim.
Inspect all23 scoped Han in four production font selections Gothic/Mincho/Textbook/Brush, especially crossing乂 U+4E42 and open-topped凵 U+51F5 versus凶/凡/凸/凹. 92individual+4wholewordPaint probes are recycled hashes, NOT96exported/viewedPNGs or identifiedfallbackface. Actual glyph evidence is Compose panels. No cosmetic font-uniformity requirement.
Inspect BOTH complete new article projections and the one changed 作 linked example line (unchanged legacy作 not newly approved). Reading table can scroll horizontally: complementary captures expose row; assess actual readability, not static clipping alone. Meaning illfortune/evil versus wholecompound agricultural senses; shape mnemonic explicitly not etymology; one raw onキョウ/order, rawkun[]/explicitquizkun[], selectedキョウwith own linked凶作 row. わるい/まがごと are glosses not added readings.
凶作 is an agricultural noun/verypooryield, not harvestverb/necessarilyzeroyield/famine/badwork/everydisappointment. Check both example readings/translations, 不作/豊作, compound-specific 作crop/yield not universal kanji-sense partition. TWO mapped reciprocalpairs/fourdirections/one direct凶作-収穫wordguard/SystemBack/offline. Source/sense correctness inherited, not new independentupstream.
Check actual pictured and supplied production N1 AND All four meaning options: illfortune;evil versus 凡commonplace;mediocre, 凸convex;protruding, 凹concave;sunken; allthreecuratedwrongcards available/zerofallback. Actual reading alternatives, singlequeuedonきょう Good/1of1done, rawkun[]/explicitquizkun[]/FullLite agreement. Close prior fallback-unverified limit ONLY for these tested configurations, not everyfuturecustompool/oldclient. All production is supplied receipt unless separately pictured.
Inspect N1selection121cards, fourstroke injectedtrace/practicefeedback/recallgiveup. Supplied fullarchive72614eda through productionContentSyncONCE imported1112kanji5068words121N1zeroProblems/acceptedVersionc6562f11cb371053/epoch1; BOTHnative terminalcase0/no skips. These are supplied receipts NOT your tests. Injectedtrace/giveup is NOT humanhandwriting/offlineMLKit/phone; unavailablemodel/shape-onlyfeedback explicit. Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. No new nativephone acceptance.

Return COMPLETE report: Snapshot;Scope(actual model, actual text/image reads);Verdicts(correctness/scopedcoverage/renderedcomprehensibility EACH new article plus changed作passage, identify inheritedtextual conclusions);Findings(severity;facet;file/PNG:location;claim+impact;remedy;evidence;confidence ornone);Optional;Limits.
Reconcile OWN prior limitations; preserve optional suggestions and residual uncertainty. Disclose incomplete reads, tool-resized contactsheets/originalfontpanels, not identifiedfallbackface/96PaintPNGs, API35 emulator not physicalphone/native-speaker. Preserve original GPT redundant/truncated-tail read limits; this is dependent follow-up not replacement initial review. Currentmain/combinedchecks/CI/publicZIP/publication/phone/generalrelease/whole-set remain later gates. No edits/questions/nextbatch.
"""
    prefix.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    exe = load(V / "batch-089-initial-claude-execution.json")["command"][0]
    command = [exe, "-C", str(R), "--add-dir", str(C), "--resume=" + session,
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
        print("Started", label, process.pid, session, flush=True)
        code = process.wait()
    events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    messages = [e["data"] for e in events if e["type"] == "assistant.message"]
    prefix.with_suffix(".md").write_text(
        (messages[-1].get("content", "") if messages else "No completed report.") + "\n", encoding="utf-8")
    required = {str(PACKET), str(V / f"batch-089-initial-{label}.md"), *map(str, IMAGES)}
    active, calls, overlaps, returned, images = set(), {}, [], set(), []
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
                    with Image.open(path) as image:
                        source_dimensions = list(image.size)
                    images.append({"path": path, "sourceSha256": sha(Path(path)),
                                   "sourceDimensions": source_dimensions,
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
        "execution": 633, "batch": "089", "snapshot": HEAD, "teachingSnapshot": TEACHING,
        "dependentOriginalSession": True, "newBlindReviewCredit": False,
        "sessionId": session, "requestedModel": model,
        "actualModels": sorted({m.get("model", "") for m in messages}),
        "usageCurrentModel": usage.get("currentModel") if usage else None,
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "unfinishedTools": sorted(active), "requiredResources": sorted(required),
        "successfullyReturnedResources": sorted(returned), "missingResources": sorted(required - returned),
        "allAssignedResourcesSuccessfullyReturned": not (required - returned),
        "actualDecodedImageReturns": images, "rawSha256": sha(raw),
        "reportSha256": sha(prefix.with_suffix(".md")), "usage": usage,
        "availableTools": ["view"],
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"
                                  and e["data"].get("infoType") == "configuration"],
        "limits": "Payload/range audit establishes delivery, not comprehension. Actual report records visual observations and limitations.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({k: record[k] for k in [
        "exitCode", "actualModels", "missingResources", "observedToolOverlaps"]}))
    assert code == 0 and record["actualModels"] == [model] and usage["currentModel"] == model
    assert not active and not overlaps and not (required - returned)
    assert [i["path"] for i in images] == list(map(str, IMAGES))
    frozen()


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] in SESSIONS:
        run(sys.argv[1])
    else:
        raise ValueError(sys.argv[1])
