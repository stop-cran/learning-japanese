"""Original-session, serial rendered confirmations for the frozen batch096."""
import base64
import datetime
import gzip
import hashlib
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
N = V / "batch-096-native" / "execution-705"
SESSION = "8b390120-e5a5-4836-8377-1b2432ea66d5"
L = C / "logs" / SESSION
HEAD = "7f2c17b3141d6a8855aff978a671f7d6ce6c3a5a"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
MODELS = {
    "claude": ("claude-opus-5.5", "de7596b6-1f69-43e0-b297-c3e600fa712a"),
    "gpt": ("gpt-6.1-sol", "ca536738-97f2-4841-b985-321ce12b37c1"),
}


def load(p):
    return json.loads(p.read_bytes())


def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


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
    assert (p["checkpoint"], p["batch"], p["status"]) == (705, "096", "continue")
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
    assert (count, manifest["contentVersion"]) == (8444, "54645b95fe8e939c")
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestFresh": True, "runtimeChanged": False}


def persist(p):
    temp = C / "progress.706.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")


def stopped(record):
    subprocess.run(["pwsh", "-NoProfile", "-NonInteractive", "-Command",
                    f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                   capture_output=True, check=True)


def prepare():
    proof = frozen()
    backup = L / "progress-before-706.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution705CoordinatorCheckpoint"] == p["execution705CoordinatorCheckpoint"]
    subprocess.run(["git", "--no-pager", "-C", str(R), "fetch", "--quiet", "origin"], check=True)
    p["execution706StartingState"] = {
        "execution": 706, "batch": "096", "startedAt": now(), "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME096 serial original-session rendered confirmations and bounded observed-choice adjudication; signed LOCAL evidence checkpoint only; no publication/097.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded. Operative contract, complete issue and final705 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": proof,
        "artifactPathPreflight": "Approved control and committed packets only; no optional historical-session helpers accessed.",
        "runtime": runtime(), "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-096-original-session-rendered-confirmations-in-progress",
             nextAction=p["execution706StartingState"]["scope"], blocker=None)
    persist(p)
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-096-rendered-cli-{kind}-706.txt").write_bytes(result.stdout)
    route = load(N / "n1-096-article-route.json")
    assert len(route["productionBuilderN1AndAllExactChoices"]) == 64
    assert len(route["directGuardBuilderChecks"]) == 1536
    parts = ["SUPPLIED NATIVE RECEIPT (not reviewer-run tests)\n" + json.dumps(
        {k: v for k, v in route.items()
         if k not in {"directGuardBuilderChecks", "productionBuilderN1AndAllExactChoices"}},
        ensure_ascii=False, indent=2)]
    sources = []

    def add(path):
        body = path.read_text(encoding="utf-8-sig")
        parts.append(f"COMPLETE SOURCE {path}; SHA256 {sha(path)}\n" +
                     "\n".join(f"{i}: {s}" for i, s in enumerate(body.splitlines(), 1)))
        sources.append({"path": str(path), "sha256": sha(path)})

    for name in ["kanji/剛.md", "words/剛健.md"]:
        add(R / name)
    for name in ["batch-096-jmdict.xml", "batch-096-comparison-jmdict.xml",
                 "batch-096-character-public-text.txt", "batch-096-gouken-public-text.txt"]:
        add(R / "docs" / "n1-sources" / name)
    parts.append("QUIZ CONTRACT docs/content-format.md:152-177\n" +
                 "\n".join((R / "docs" / "content-format.md").read_text(encoding="utf-8").splitlines()[151:177]))
    parts.append("ALL 64 EXACT KANJI BUILDER RECORDS, zero-based indices\n" +
                 "\n".join(json.dumps({"index": i, **row}, ensure_ascii=False, separators=(",", ":"))
                           for i, row in enumerate(route["productionBuilderN1AndAllExactChoices"])))
    rows = route["directGuardBuilderChecks"]
    identities = sorted({json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                         for row in rows for o in row["options"]})
    lookup = {identity: i for i, identity in enumerate(identities)}
    encoded = []
    for i, row in enumerate(rows):
        indices = [lookup[json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))]
                   for o in row["options"]]
        encoded.append([i, row["target"], row["excluded"], row["pool"], row["direction"], row["seed"], indices])
        restored = dict(zip(["target", "excluded", "pool", "direction", "seed"], encoded[-1][1:6]))
        restored["options"] = [json.loads(identities[index]) for index in indices]
        assert restored == row
        assert not any(o["word"] == row["excluded"] for o in row["options"])
    parts.append("LOSSLESS WORD-OPTION DICTIONARY: index -> exact {word,label} object\n" +
                 "\n".join(f"{i}:{value}" for i, value in enumerate(identities)))
    parts.append("ALL 1536 EXACT WORD GUARD RECORDS. Row schema:\n"
                 "[originalZeroBasedIndex,target,excluded,pool,direction,seed,orderedOptionDictionaryIndices]\n"
                 "Every original row reconstructed and compared equal before packet creation.\n" +
                 "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in encoded))
    add(N / "contact-sheets" / "index.json")
    common = "\n\n".join(parts)
    for label in MODELS:
        own = "\n\n".join((V / f"batch-096-{stage}-{label}.md").read_text(encoding="utf-8")
                            for stage in ["initial", "supplement"])
        text = "YOUR OWN COMPLETE PREVIOUS REPORTS\n" + own + "\n\nCOMMON EVIDENCE\n" + common
        chunks, chunk = [], ""
        for line in text.splitlines(keepends=True):
            assert len(line.encode("utf-8")) < 12000
            if len((chunk + line).encode("utf-8")) > 12000:
                chunks.append(chunk)
                chunk = ""
            chunk += line
        if chunk:
            chunks.append(chunk)
        resources = []
        for i, chunk in enumerate(chunks, 1):
            path = C / f"batch-096-rendered-{label}-packet-706-{i:02d}.txt"
            assert not path.exists()
            path.write_text(chunk, encoding="utf-8")
            resources.append(str(path))
        resources += [str(N / f"n1-096-font-panel-{i}.png") for i in range(1, 5)]
        resources += [str(N / "contact-sheets" / f"sheet-{i:02d}.png") for i in range(1, 11)]
        save(C / f"batch-096-rendered-{label}-resources-706.json", resources)
    save(C / "batch-096-rendered-packet-provenance-706.json", {
        "snapshot": HEAD, "nativeSnapshot": route["contentSnapshot"],
        "reviewedTeachingSnapshot": "b26bcf9b328872b1575cf89e187973fea0a32a31",
        "routeSource": str(N / "n1-096-article-route.json"), "routeSha256": sha(N / "n1-096-article-route.json"),
        "kanjiRecords": 64, "wordRecords": 1536, "wordRecordReconstructionExact": True,
        "sources": sources, "commonEvidenceSha256": hashlib.sha256(common.encode()).hexdigest(),
        "sourceAccess": "Committed full lexical/comparison families and public text, not fresh upstream retrieval.",
    })
    print("Starting state persisted; exact runtime verified; text chunks", len(chunks), flush=True)


def review(label):
    frozen()
    if label == "gpt":
        prior = load(C / "batch-096-rendered-706-claude-execution.json")
        assert prior["acceptedExecution"]
        stopped(prior)
    model, session = MODELS[label]
    assert f'"{model}"' in (C / "batch-096-rendered-cli-config-706.txt").read_text(encoding="utf-8-sig")
    resources = load(C / f"batch-096-rendered-{label}-resources-706.json")
    prefix = C / f"batch-096-rendered-706-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    prompt = f"""DEPENDENT rendered confirmation in YOUR ORIGINAL session {session}; requested model {model}.
Frozen signed content HEAD {HEAD}; native fullarchive58129f19; unchanged reviewed teachingb26bcf9b/version54645b95fe8e939c.
This is NOT a fresh blind initial review. No teaching edits occur during either reviewer.
Read ALL resources below IN ORDER. EXACTLY ONE view call per response; WAIT for result before next.
Only read-only view exposed; no shell, edits, delegation, other reports or parallel tool calls.
Text chunks <12000UTF8bytes: full read without ranges. PNGs must be decoded/viewed, not inferred from hashes.
{chr(10).join(resources)}
First text contains YOUR OWN original and supplemental reports, not the other model's.
Common evidence is identical: both current complete articles剛/剛健, complete member/comparison JMdict packets
and public-source text; complete native assertions; ALL64 exact kanji pool choices and ALL1536 word guard
builder records. Word rows use a LOSSLESS {{"word","label"}} dictionary with every original row index and
ordered option preserved; coordinator reconstructed ALL1536 rows and compared exact equality.
Then FOUR original four-font panels cover all28Han including冂/刂fallback.
Then10contact sheets cover all37remainingPNG at reduced scale. Disclose reduced-image limits; if necessary
inspect a specific original in that same directory SERIALLY and explain why. hasGlyph/hash/nonblank is not legibility.
Check actual glyph distinctions, source-only wording/readings, full readingtable(left/rightscroll), wrapping,
BOTHarticles/ONEreciprocalpair/TWOdirections/ZEROactivatedbaselinepairs/SystemBack/offline/N1selection/
meaning/onlyごうandnoKun/drawingtrace+giveuprecall. Supplementalコウ is outside pinnedmetadata, not a new question.
Actual displayed defaultN1 wronglabels are剖/dissect;split open,削/shave;sharpen;pare,儒/Confucian;Confucian scholar.
TWOcuratedwrongcards available inN1; 則N2 excluded, ONEactualproductionfallback儒. This displayed capture is
separate from builderseed0 and must not be inferred from that record.
Inspect ALL64 bounded N1/All/custom/randomN1subset records and actual labels/ordinary senses, not title differences.
All1536 successes prove only TWELVE specified directguards across BOTHdirections/BOTHtargetorientations,
All/custom/16seeds; NOT all-other-option semantic safety. Report a precise consequential ambiguous displayed
option if established; no manufactured quota or whole-corpus speculative expansion. Distinguish broader related
ideas (e.g.克overcome) from answer equivalence. Strong/hard options in untested pools remain outside the sample.
Preserve YOUR original hypotheses/optional dispositions. Initial/source supplements were already supplied in
YOUR session; omitted supplemental families in this rendered packet are not a new blind102family review.
TEN injected reference strokes and give-up recall/persistence do NOT certify humanhandwriting/MLKit.
Native705 supplied receipts:2 terminalcase0/no skips; fullarchive productionContentSyncONCE;1119kanji5072words128N1
zeroProblems/Roomepoch1. API35emulator5580 stopped; qualifiedTESTONLYAndroid1c1b7bf4 retainingproductionf9b59a2,
NOT latestappmain. No new reviewer-run native tests, physicalphone/generalrelease/whole-set/publication claim.
Maintain YOUR original findings/optional/hypotheses history; no retroactive independence or fresh discovery claim.
Return COMPLETE Snapshot;Scope(actual model/session, actual text resources, decoded images, omissions/scale);
Verdicts separately correctness/scopedcoverage/comprehensibility CLEAN/NEEDS FIX/UNVERIFIED per assigned article
and bounded rendered/quiz scope; Findings(severity/facet/file:lines,claim+impact,remedy,evidence,confidence ornone);
Reconciliation(resolved/partiallyresolved/unresolved/withdrawn/optional);Optional;Limits.
Do not silently label any consequential unresolved choice claim CLEAN. No questions or edits.
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
        "execution": 706, "batch": "096", "snapshot": HEAD, "sessionId": session,
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
        "limits": "Serial process and actual returned payloads establish delivery, not comprehension. Contact-sheet scale and image resizing disclosed.",
    }
    save(C / (prefix.name + "-execution.json"), record)
    stopped(record)
    print(json.dumps({k: record[k] for k in ["exitCode", "actualModels", "acceptedExecution", "observedToolOverlaps"]}), flush=True)
    frozen()
    assert accepted, "Preserve incomplete evidence and yield; do not silently accept"


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "review":
        review(sys.argv[2])
