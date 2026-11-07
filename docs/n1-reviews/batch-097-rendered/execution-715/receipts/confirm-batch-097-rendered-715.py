"""Serial original-session rendered confirmations; no runtime content changes."""
import base64
import datetime
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
N = V / "batch-097-native" / "execution-714"
SESSION = "14a1dd8e-9ff4-4d2d-8bbd-8df6259c9e7c"
L = C / "logs" / SESSION
HEAD = "e75b4bb14ba5ee3183a973be7752033721a5246e"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
MODELS = {
    "claude": ("claude-opus-5.5", "3a0b6dd8-6212-4ceb-a430-3127aac6969e"),
    "gpt": ("gpt-6.1-sol", "9f31594c-f091-4d47-9276-12249f0c848d"),
}
BASE = C / "confirm-batch-096-rendered-706.py"
spec = importlib.util.spec_from_file_location("prior_rendered", BASE)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
prior.SESSION = SESSION
save, load, sha, now, git, stopped = (
    prior.save, prior.load, prior.sha, prior.now, prior.git, prior.stopped
)


def frozen():
    proof = prior.ownership()
    for repo, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", repo=repo) == head
        assert git("log", "-1", "--format=%G?", repo=repo) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", repo=repo)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (714, "097", "continue")
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
                path = R.joinpath(*name.split("/"))
                actual = sha(path) if kind in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                } else sha256(path)
                assert actual == digest, name
                count += 1
    assert (count, manifest["contentVersion"]) == (8447, "a066afceaf1f447a")
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestFresh": True, "runtimeChanged": False}


def persist(p):
    temp = C / "progress.715.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")


def prepare():
    proof = frozen()
    backup = L / "progress-before-715.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution714CoordinatorCheckpoint"] == p["execution714CoordinatorCheckpoint"]
    subprocess.run(["git", "--no-pager", "-C", str(R), "fetch", "--quiet", "origin"], check=True)
    p["execution715StartingState"] = {
        "execution": 715, "batch": "097", "startedAt": now(), "startingHead": HEAD,
        "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME097 serial original-session rendered confirmations; normally signed LOCAL evidence checkpoint only; no publication/098.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed. Operative contract, complete issue and terminal714 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": proof,
        "artifactPathPreflight": "Approved control and committed evidence only; no optional historical-session helper accessed.",
        "runtime": runtime(), "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-097-original-session-rendered-confirmations-in-progress",
             nextAction=p["execution715StartingState"]["scope"], blocker=None)
    persist(p)
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-097-rendered-cli-{kind}-715.txt").write_bytes(result.stdout)
    route = load(N / "n1-097-article-route.json")
    pools, guards = route["productionBuilderN1AndAllExactChoices"], route["directGuardBuilderChecks"]
    assert len(pools) == 64 and len(guards) == 512
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

    for name in ["kanji\\剣.md", "words\\剣.md", "words\\真剣.md", "kanji\\真.md"]:
        add(R / name)
    parts.append("EXACT UNCHANGED TEACHING DIFF, source checkpoint to reviewed draft\n" +
                 git("diff", "fb8a532bb0230e0576b854ba71899252cb28542b",
                     "1fa1ac69b88383ef424c0a69d34020ccca83c313", "--", "kanji", "words"))
    for name in ["batch-097-jmdict.xml", "batch-097-comparison-jmdict.xml",
                 "batch-097-character-public-text.txt", "batch-097-shinken-public-text.txt"]:
        add(R / "docs" / "n1-sources" / name)
    parts.append("QUIZ CONTRACT docs\\content-format.md:152-177\n" +
                 "\n".join((R / "docs" / "content-format.md").read_text(encoding="utf-8").splitlines()[151:177]))
    parts.append("ALL 64 EXACT KANJI BUILDER RECORDS, zero-based indices\n" +
                 "\n".join(json.dumps({"index": i, **row}, ensure_ascii=False, separators=(",", ":"))
                           for i, row in enumerate(pools)))
    identities = sorted({json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                         for row in guards for o in row["options"]})
    lookup = {identity: i for i, identity in enumerate(identities)}
    encoded = []
    for i, row in enumerate(guards):
        indices = [lookup[json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))]
                   for o in row["options"]]
        encoded.append([i, row["target"], row["excluded"], row["pool"], row["direction"], row["seed"], indices])
        restored = dict(zip(["target", "excluded", "pool", "direction", "seed"], encoded[-1][1:6]))
        restored["options"] = [json.loads(identities[index]) for index in indices]
        assert restored == row
        assert not any(o["word"] == row["excluded"] for o in row["options"])
    parts.append("LOSSLESS WORD-OPTION DICTIONARY: index -> exact {word,label} object\n" +
                 "\n".join(f"{i}:{value}" for i, value in enumerate(identities)))
    parts.append("ALL 512 EXACT WORD GUARD RECORDS. Row schema:\n"
                 "[originalZeroBasedIndex,target,excluded,pool,direction,seed,orderedOptionDictionaryIndices]\n"
                 "Every original row reconstructed and compared equal before packet creation.\n" +
                 "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in encoded))
    add(N / "contact-sheets" / "index.json")
    common = "\n\n".join(parts)
    for label in MODELS:
        own = (V / f"batch-097-initial-{label}.md").read_text(encoding="utf-8")
        text = "YOUR OWN COMPLETE PREVIOUS REPORT\n" + own + "\n\nCOMMON EVIDENCE\n" + common
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
            path = C / f"batch-097-rendered-{label}-packet-715-{i:02d}.txt"
            assert not path.exists()
            path.write_text(chunk, encoding="utf-8")
            resources.append(str(path))
        resources += [str(N / f"n1-097-font-panel-{i}.png") for i in range(1, 4)]
        resources += [str(N / "contact-sheets" / f"sheet-{i:02d}.png") for i in range(1, 14)]
        save(C / f"batch-097-rendered-{label}-resources-715.json", resources)
    save(C / "batch-097-rendered-packet-provenance-715.json", {
        "snapshot": HEAD, "nativeSnapshot": route["contentSnapshot"],
        "reviewedTeachingSnapshot": "1fa1ac69b88383ef424c0a69d34020ccca83c313",
        "routeSource": str(N / "n1-097-article-route.json"), "routeSha256": sha(N / "n1-097-article-route.json"),
        "kanjiRecords": 64, "wordRecords": 512, "wordRecordReconstructionExact": True,
        "sources": sources, "commonEvidenceSha256": hashlib.sha256(common.encode()).hexdigest(),
        "sourceAccess": "Committed full lexical/comparison families and public text, not fresh upstream retrieval.",
    })
    print("Starting state persisted; exact runtime verified; last packet chunks", len(chunks), flush=True)


def review(label):
    frozen()
    if label == "gpt":
        record = load(C / "batch-097-rendered-715-claude-execution.json")
        assert record["acceptedExecution"]
        stopped(record)
    model, session = MODELS[label]
    assert f'"{model}"' in (C / "batch-097-rendered-cli-config-715.txt").read_text(encoding="utf-8-sig")
    resources = load(C / f"batch-097-rendered-{label}-resources-715.json")
    prefix = C / f"batch-097-rendered-715-{label}"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    prompt = f"""DEPENDENT rendered confirmation in YOUR ORIGINAL session {session}; requested model {model}.
Frozen signed content HEAD {HEAD}; native fullarchive83e5c090; unchanged reviewed teaching1fa1ac69/versiona066afceaf1f447a.
This is NOT a fresh blind initial review. No teaching edits occur during either reviewer.
Read ALL resources below IN ORDER. EXACTLY ONE view call per response; WAIT for result before next.
Only read-only view exposed; no shell, edits, delegation, other reports or parallel tool calls.
Text chunks <12000UTF8bytes: full read without ranges. PNGs must be decoded/viewed, not inferred from hashes.
{chr(10).join(resources)}
First text contains YOUR OWN original report, not the other model's or author adjudication.
Common evidence is identical: both complete newarticles剣kanji/剣つるぎ and both reusedarticles真剣/真 with EXACT
changedpassages(diff); complete main/comparisonJMdict and publicdictionarytext; complete nativeassertions;
ALL64 exact kanjichoices and ALL512 wordguardrecords. Wordrows use LOSSLESS word/labeldictionary with every
originalrowindex and orderedoptionpreserved; coordinator reconstructedALL512 exactly.
Then THREE original fourfontpanels cover all20Han especially刂fallback; inspect wholewordprobes.
Then13contactsheets cover all52remainingPNG at reducedscale. Disclose reducedimagelimits. If necessary
inspect a specific original in that same directory SERIALLY and explain why. hasGlyph/hash/nonblank is not legibility.
Check actual glyph distinctions, full readingtable(left/rightscroll), wrapping, TWOcompletearticles and EXACTTWO
reusedchanges(words真剣line27,kanji真line37); THREEreciprocalpairs/SIXdirections/ONEactivatedbaselinepair/
SystemBack/offline/N1selection/meaning/BOTHonけんandkunつるぎ/drawingtrace+giveuprecall.
Allrawケン/[つるぎ] and exactexplicitcuration preserved full/Lite; BOTHkeysGood/Done2of2.
Actual displayed defaultN1 wronglabels are剖/dissect;splitopen,剛/sturdy;unyieldingstrength,蚊/mosquito.
TWOcuratedwrongcards available inN1; 則N2 excluded, ONEactualproductionfallback蚊. ActualUIcapture is separate
from builderseed0 and must NOT be inferred from that record.
Inspect ALL64 boundedN1/All/custom/randomN1subset records and actuallabels/ordinarysenses, not titledifferences.
27unique sampledlabels include矛/spear;polearm. Check answer-equivalence, not merely sharedweapondomain.
ALL512 successes prove only FOUR specified directguards 剣with刀/日本刀/刃/真剣 across BOTHdirections/
BOTHtargetorientations/All+custom/16seeds; NOT all-other-option semanticsafety. Inspect exact choices for
demonstrated consequential ambiguity, no manufacturedquota or wholecorpus speculativeexpansion.
Preserve YOUR original hypotheses/optionaldispositions. Full original initialsourcepacket already supplied in
YOUR session; omitted rawmetadata/18comparisonbodies here is NOT a newblind137familyreview.
TENinjectedreferencestrokes and giveuprecall/persistence do NOT certify humanhandwriting/MLKit.
Native714 suppliedreceipts: TWOterminalcase0/noskips; fullarchive productionContentSyncONCE;1120kanji5073words129N1,
zeroProblems/Roomepoch1. API35emulator5580 stopped; qualifiedTESTONLYAndroid1c1b7bf4 retainingproductionf9b59a2,
NOT latestappmain. No new reviewer-run native tests, physicalphone/generalrelease/whole-set/publication claim.
Maintain YOUR original findings/optional/hypotheses history; no retroactiveindependence or freshdiscoveryclaim.
Return COMPLETE Snapshot;Scope(actual model/session, actual text resources, decoded images, omissions/scale);
Verdicts separately correctness/scopedcoverage/comprehensibility CLEAN/NEEDS FIX/UNVERIFIED per assignednewarticle
and EACHboundedchangedreusedpassage, plus boundedrendered/quizscope; Findings(severity/facet/file:lines,claim+impact,
remedy,evidence,confidence ornone);Reconciliation(resolved/partiallyresolved/unresolved/withdrawn/optional);
Optional;Limits. Do not silently label any consequential unresolvedchoiceclaim CLEAN. No questions or edits.
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
        "execution": 715, "batch": "097", "snapshot": HEAD, "sessionId": session,
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
        "limits": "Actual returned payloads establish delivery, not comprehension. Contact-sheet scale and image resizing disclosed.",
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
