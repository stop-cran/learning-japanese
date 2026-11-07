"""Bounded original-session confirmations of frozen batch095 native evidence."""
import base64
import datetime
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
V = R / "docs" / "n1-reviews"
N = V / "batch-095-native" / "execution-694"
SESSION = "501bec26-ce09-47dc-a16f-93494848e51f"
L = C / "logs" / SESSION
HEAD = "86966dc49fb3a22014aea0dac2b568bc7045e56d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
MODELS = {
    "claude": ("claude-opus-5.5", "ede78c28-e889-47b5-be0b-21533da61551"),
    "gpt": ("gpt-6.1-sol", "ee7498e0-d3ad-46bf-bbc9-82761892cab0"),
}


def load(p):
    return json.loads(p.read_bytes())


def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def git(*args, repo=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(repo), *args],
        encoding="utf-8",
    ).strip()


def ownership():
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, SESSION, "running")
    script = f"""
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
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    return {
        "parentPid": 19008, "session": SESSION, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
    }


def frozen():
    proof = ownership()
    for repo, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", repo=repo) == head
        assert git("log", "-1", "--format=%G?", repo=repo) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", repo=repo)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (694, "095", "continue")
    return proof


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for kind, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                actual = sha(R / name) if kind in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == digest, name
                count += 1
    assert (count, manifest["contentVersion"]) == (8441, "463619d79972e9f2")
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestFresh": True, "runtimeChanged": False}


def persist(p):
    temp = C / "progress.695.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")


def prepare():
    proof = frozen()
    backup = L / "progress-before-695.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution694CoordinatorCheckpoint"] == p["execution694CoordinatorCheckpoint"]
    p["execution695StartingState"] = {
        "execution": 695, "batch": "095", "startedAt": now(), "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME095 serial original-session rendered confirmations and bounded observed-choice adjudication; signed LOCAL evidence checkpoint only; no publication/096.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded. Operative contract, complete issue and final694 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": proof,
        "artifactPathPreflight": "Approved control and committed packets only; no optional historical-session helpers accessed.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-095-original-session-rendered-confirmations-in-progress",
             nextAction=p["execution695StartingState"]["scope"], blocker=None)
    persist(p)
    save(L / "runtime-preflight-695.json", runtime())
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-095-rendered-cli-{kind}-695.txt").write_bytes(result.stdout)
    route = load(N / "n1-095-article-route.json")
    parts = ["SUPPLIED NATIVE RECEIPT (not reviewer-run tests)\n" + json.dumps(
        {k: v for k, v in route.items()
         if k not in {"directGuardBuilderChecks", "productionBuilderN1AndAllExactChoices"}},
        ensure_ascii=False, indent=2)]
    for name in ["kanji/剖.md", "words/解剖.md", "kanji/解.md"]:
        content = (R / name).read_text(encoding="utf-8")
        parts.append(f"COMPLETE CURRENT ARTICLE {name}; SHA256 {sha(R / name)}\n" +
                     "\n".join(f"{i}: {s}" for i, s in enumerate(content.splitlines(), 1)))
    for filename in ["batch-095-jmdict.xml", "batch-095-comparison-jmdict.xml",
                     "batch-095-character-public-text.txt", "batch-095-kaibou-public-text.txt"]:
        source = R / "docs" / "n1-sources" / filename
        parts.append(f"COMPLETE COMMITTED SOURCE {filename}; SHA256 {sha(source)}\n" +
                     source.read_text(encoding="utf-8"))
    parts.append("QUIZ CONTRACT docs/content-format.md:152-177\n" +
                 "\n".join((R / "docs" / "content-format.md").read_text(encoding="utf-8").splitlines()[151:177]))
    for key in ["productionBuilderN1AndAllExactChoices", "directGuardBuilderChecks"]:
        groups = {}
        for i, row in enumerate(route[key]):
            value = json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
            groups.setdefault(value, []).append(i)
        parts.append(f"COMPLETE {key}: {len(route[key])} indexed records; "
                     f"{len(groups)} distinct full records; all zero-based indices retained.")
        parts.extend(json.dumps({"indices": indices, "record": json.loads(value)},
                                ensure_ascii=False, separators=(",", ":")) for value, indices in groups.items())
        assert sorted(i for indices in groups.values() for i in indices) == list(range(len(route[key])))
    parts.append("CONTACT SHEET SOURCE BINDINGS\n" + (N / "contact-sheets" / "index.json").read_text(encoding="utf-8"))
    common = "\n\n".join(parts)
    for label in MODELS:
        own = (V / f"batch-095-initial-{label}.md").read_text(encoding="utf-8")
        text = "YOUR OWN COMPLETE PREVIOUS REPORT\n" + own + "\n\nCOMMON EVIDENCE\n" + common
        chunks, chunk = [], ""
        for line in text.splitlines(keepends=True):
            if len(chunk) + len(line) > 14000:
                chunks.append(chunk)
                chunk = ""
            chunk += line
        if chunk:
            chunks.append(chunk)
        resources = []
        for i, chunk in enumerate(chunks, 1):
            path = C / f"batch-095-rendered-{label}-packet-695-{i:02d}.txt"
            assert not path.exists()
            path.write_text(chunk, encoding="utf-8")
            resources.append(str(path))
        resources += [str(N / f"n1-095-font-panel-{i}.png") for i in range(1, 5)]
        resources += [str(N / "contact-sheets" / f"sheet-{i:02d}.png") for i in range(1, 15)]
        save(C / f"batch-095-rendered-{label}-resources-695.json", resources)
    save(C / "batch-095-rendered-packet-provenance-695.json", {
        "snapshot": HEAD, "nativeSnapshot": "cc74834756847ad23fad6a721bb0a02ca859fa99",
        "routeSource": str(N / "n1-095-article-route.json"), "routeSha256": sha(N / "n1-095-article-route.json"),
        "kanjiRecords": 64, "wordRecords": 384,
        "grouping": "Lossless exact-row grouping retains every record field and original index.",
        "sourceFamilies": 37, "commonEvidenceSha256": hashlib.sha256(common.encode()).hexdigest(),
        "sourceAccess": "Committed full lexical/comparison families and public text, not fresh upstream retrieval.",
    })
    print("Starting state persisted; frozen runtime and bounded evidence verified.", flush=True)


def review(label, repair=False):
    frozen()
    if label == "gpt":
        prior = load(C / "batch-095-rendered-695-claude-execution.json")
        repaired = load(C / "batch-095-rendered-695-claude-serial-repair-execution.json")
        assert not prior["acceptedExecution"] and len(prior["observedToolOverlaps"]) == 1
        assert repaired["acceptedExecution"] and len(repaired["actualDecodedImageReturns"]) == 2
        for record in [prior, repaired]:
            subprocess.run(["pwsh", "-NoProfile", "-Command",
                            f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                           capture_output=True, check=True)
    model, session = MODELS[label]
    assert f'"{model}"' in (C / "batch-095-rendered-cli-config-695.txt").read_text(encoding="utf-8-sig")
    resources = load(C / f"batch-095-rendered-{label}-resources-695.json")
    prefix = C / f"batch-095-rendered-695-{label}"
    if repair:
        assert label == "claude"
        prior = load(C / "batch-095-rendered-695-claude-execution.json")
        assert not prior["acceptedExecution"] and len(prior["observedToolOverlaps"]) == 1
        assert not prior["unfinishedTools"]
        assert set(prior["requiredResources"]) == set(prior["successfullyReturnedResources"])
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {prior['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       capture_output=True, check=True)
        resources = [str(prefix.with_suffix(".md")),
                     str(N / "n1-095-font-panel-1.png"), str(N / "n1-095-font-panel-2.png")]
        prefix = C / "batch-095-rendered-695-claude-serial-repair"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    prompt = f"""DEPENDENT rendered confirmation in YOUR ORIGINAL session {session}; actual requested model {model}.
Frozen signed content HEAD {HEAD}; native fullarchivecc748347; unchanged reviewed teaching8c4e1650/version463619d79972e9f2.
This is NOT a fresh blind initial review. No teaching edits occur during either reviewer.
Read ALL resources below IN ORDER. EXACTLY ONE view call per response; WAIT for result before next.
Only read-only view exposed; no shell, edits, delegation, other reports or parallel tool calls.
Text chunks <14000characters: full read without ranges. PNGs must be decoded/viewed, not inferred from hashes.
{chr(10).join(resources)}
First text contains YOUR OWN original report, not the other model's. Common evidence is the same for both.
It contains all three current articles剖/解剖/解, all37 complete frozen JMdict families and public-source text,
complete native assertions, ALL64 exact kanji pool choices and ALL384 word guard builder records with every
original index retained (losslessly grouped identical records), pairwise quiz contract and sheet bindings.
Then FOUR original four-font panels cover all32Han, including亻/刂/阝 system fallback.
Then14contact sheets cover all56remaining PNGs at reduced scale. Disclose reduced-image limits; if necessary
inspect a specific original from the same directory serially and explain why. Nonblank/hasGlyph/hash does NOT prove legibility.
Check actual glyph distinctions, source-only wording/readings, full reading tables(left/right scrolled captures), wrapping,
allTHREEarticles/TWOreciprocalpairs/FOURdirections/SystemBack/offline/N1selection/meaning/onlyぼうandnoKun/drawingtrace+recall.
Assess exact displayed defaultN1 wrong labels冒/brave danger;venture,刈/mow;reap,企/plan;undertake against剖/dissect;split open.
ZERO curated wrongcards are in N1:部N3/倍N2/副N2 excluded, THREE productionfallbacks.
Inspect ALL64 bounded N1/All/custom/randomN1subset records and actual labels/ordinary senses, not just titles being different.
All384 successes prove only THREE specific guards解剖/分析,解剖/分解,解剖/検査 across both directions and target orientations,
All/custom/16seeds; NOT all-other-option semantic safety. Report a precise consequential ambiguous displayed option if
established; no manufactured quota or whole-corpus speculative expansion. Preserve your original optional/hypothesis
dispositions separately; actual解体 card absent,臨床診察 and調査 distinctions are source-bounded, not unrestricted guarantees.
TEN injected reference strokes and give-up recall/persistence do NOT certify human handwriting/MLKit.
Native694 coordinator receipts:2 terminalcase0/no skips; fullarchive productionContentSyncONCE;1118kanji5071words127N1
zeroProblems/Roomepoch1. API35emulator5580 stopped, qualifiedTESTONLYAndroid1c1b7bf4 retaining productionf9b59a2,
NOT latestappmain. No new reviewer-run native tests, physicalphone/generalrelease/whole-set/publication claim.
Maintain YOUR original findings/optional/hypotheses history; no retroactive discovery/independence claim.
Return complete Snapshot;Scope(actual model/session, actual text resources, decoded images, omissions/scale);
Verdicts separately correctness/scopedcoverage/comprehensibility CLEAN/NEEDS FIX/UNVERIFIED per assigned article/passage
and bounded rendered/quiz scope; Findings(severity/facet/file:lines,claim+impact,remedy,evidence,confidence or none);
Reconciliation(resolved/partiallyresolved/unresolved/withdrawn/optional);Optional;Limits.
Do not silently label any consequential unresolved choice claim CLEAN. No questions or edits.
"""
    if repair:
        prompt = f"""ORIGINAL SESSION {session}, actual model {model}: smallest SERIAL REPAIR of exactly two PNG reads.
Snapshot remains signed {HEAD}, unchanged runtime/teaching. Original695 complete report and execution are
preserved immutable. Process12284 exited0; all14text chunks and18images returned; exactly panels1+2 overlapped,
therefore that execution is REJECTED for strict serial acceptance. Do not retroactively label it compliant.
All other observations were serial and remain historical evidence; do not repeat broad reads.
Read EXACTLY these THREE resources, in order, ONE view call per response and WAIT for result before next:
{chr(10).join(resources)}
First is YOUR OWN complete report. Freshly decode each PNG separately; confirm scoped glyph legibility and
distinctions across four fonts, including blade/side forms and fallback component appearance on these two panels.
This only repairs those two observations, not the original execution, not new blind credit and not the whole review.
Keep your original article/quiz findings, hypothesis/optional/limitations unchanged unless these two images establish
a precise regression. Your newly raised optional citation-line hypothesis remains a hypothesis, not a proven defect.
No other resources, no parallel calls, shell, delegation or edits. Return Snapshot;Scope(actual model/session/3reads);
Verdicts separately correctness/scopedcoverage/comprehensibility for these two panels only;
Findings;Reconciliation(original overlap rejected forever, two fresh serial observations only);Optional;Limits.
Do not claim phone, successfulMLKit, latestappmain, tests, upstream or publication. Native receipts inherited only.
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
            path = call["arguments"].get("path", "")
            if data["success"] and path:
                if path.endswith(".png"):
                    payloads = data.get("result", {}).get("binaryResultsForLlm", [])
                    if len(payloads) == 1 and payloads[0]["mimeType"] == "image/png":
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
                and not active and not overlaps and all(c["name"] == "view" for c in calls.values())
                and all(p in returned for p in resources))
    record = {
        "execution": 695, "batch": "095", "snapshot": HEAD, "sessionId": session,
        "dependentOriginalSession": True, "newBlindInitialReviewCredit": False,
        "requestedModel": model, "actualModels": models, "usageCurrentModel": usage.get("currentModel"),
        "launcherPid": process.pid, "startedAt": started, "completedAt": now(), "exitCode": code,
        "command": command, "toolCalls": list(calls.values()), "observedToolOverlaps": overlaps,
        "unfinishedTools": sorted(active), "requiredResources": resources,
        "successfullyReturnedResources": returned, "actualDecodedImageReturns": images,
        "acceptedExecution": accepted, "rawSha256": sha(raw), "reportSha256": sha(prefix.with_suffix(".md")),
        "usage": usage, "availableTools": ["view"],
        "configurationEvidence": [e["data"] for e in events if e["type"] == "session.info"
                                  and e["data"].get("infoType") == "configuration"],
        "limits": "Audited serial process and returned payloads establish delivery, not comprehension. Contact-sheet scale and returned image resizing disclosed.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    print(json.dumps({k: record[k] for k in ["exitCode", "actualModels", "acceptedExecution", "observedToolOverlaps"]}), flush=True)
    frozen()
    assert accepted, "Preserve incomplete evidence and yield; do not silently accept"


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "review":
        review(sys.argv[2], repair=len(sys.argv) > 3 and sys.argv[3] == "repair")
