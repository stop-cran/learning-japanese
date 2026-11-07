"""Serial original-session native evidence confirmations; no runtime authoring."""
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
N = V / "batch-094-native" / "execution-682"
SESSION = "b9183a91-cd55-4fa5-9e7a-075b07bf6030"
L = C / "logs" / SESSION
HEAD = "577eb626dafec18e5bbd8d9eb257a75b1dac775e"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
MODELS = {"claude": ("claude-opus-5.5", "edf22897-9f87-4a3b-b20f-4c2fd839013a"),
          "gpt": ("gpt-6.1-sol", "65fd64ff-aae2-40af-927e-bf19b52fecb6")}


def load(p):
    return json.loads(p.read_bytes())


def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args, repo=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(repo), *args],
                                   encoding="utf-8").strip()


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
    decoded = base64.b64decode(encoded).decode("utf-16-le")
    assert str(C / "runner.ps1") in decoded
    launcher = (C / "runner.ps1").read_text(encoding="utf-8-sig")
    assert "$lock.Dispose()" in launcher
    assert "'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None'" in launcher
    return {"parentPid": 19008, "session": SESSION, "decodedLauncherMatches": True,
            "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
            "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain]}


def frozen(final=False):
    proof = ownership()
    assert git("rev-parse", "HEAD^" if final else "HEAD") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "HEAD", repo=A) == APP
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", repo=A)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (682, "094")
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
    assert count == 8438 and manifest["contentVersion"] == "eeae47753a460f72"
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestFresh": True, "runtimeChanged": False}


def prepare():
    proof = frozen()
    assert not (L / "progress-before-683.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-683.json")
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution682CoordinatorCheckpoint"] == p["execution682CoordinatorCheckpoint"]
    p["execution683StartingState"] = {
        "execution": 683, "batch": "094", "startedAt": now(), "startingHead": HEAD, "androidHead": APP,
        "scope": "SAME094 serial original-session rendered confirmations and bounded observed-choice adjudication; signed LOCAL evidence checkpoint only, no publication/095.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and complete embedded checkpoint decoded. Operative contract, complete issue and final682 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": proof,
        "artifactPathPreflight": "Approved control and committed packets only. No optional historical-session helpers accessed.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-094-original-session-rendered-confirmations-in-progress", blocker=None,
             nextAction=p["execution683StartingState"]["scope"])
    save(C / "progress.json", p)
    save(L / "runtime-preflight-683.json", runtime())
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-094-rendered-cli-{kind}-683.txt").write_bytes(result.stdout)
    sys.path.insert(0, str(R / "tools"))
    from extract_n1_jmdict import extract
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    dictionary = C / "inputs" / "n1-implementation-JMdict_e.gz"
    selected = extract(dictionary.read_bytes(), snapshot["inputs"][dictionary.name]["sha256"],
                       ["1298090", "1337570"])
    (C / "batch-094-rendered-observed-pair-683.xml").write_bytes(selected)
    route = load(N / "n1-094-article-route.json")
    body = {k: v for k, v in route.items()
            if k not in {"directGuardBuilderChecks", "productionBuilderN1AndAllExactChoices"}}
    parts = ["SUPPLIED NATIVE RECEIPT (not reviewer-run tests)\n" + json.dumps(body, ensure_ascii=False, indent=2)]
    for name in ["kanji/削.md", "words/削る.md", "words/削除.md", "kanji/除.md", "words/縮める.md"]:
        content = (R / name).read_text(encoding="utf-8")
        parts.append(f"COMPLETE CURRENT ARTICLE {name}; SHA256 {sha(R / name)}\n" +
                     "\n".join(f"{i}: {s}" for i, s in enumerate(content.splitlines(), 1)))
    parts += ["COMPLETE TWO FROZEN JMDICT FAMILIES; source compressed SHA256 " + sha(dictionary) +
              "; XML source SHA/version from docs/n1-source-snapshot.json; frozen2026-11-02; EDRDG CC BY-SA4.0\n" +
              selected.decode("utf-8"),
              "QUIZ CONTRACT docs/content-format.md:152-177\n" +
              "\n".join((R / "docs" / "content-format.md").read_text(encoding="utf-8").splitlines()[151:177])]
    # Lossless grouping keeps all 384 assertions while avoiding duplicate long option records.
    for key in ["productionBuilderN1AndAllExactChoices", "directGuardBuilderChecks"]:
        groups = {}
        for i, row in enumerate(route[key]):
            value = json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
            groups.setdefault(value, []).append(i)
        parts.append(f"COMPLETE {key}: {len(route[key])} indexed records, "
                     f"{len(groups)} distinct full records; all zero-based indices retained.")
        parts.extend(json.dumps({"indices": indices, "record": json.loads(value)},
                                ensure_ascii=False, separators=(",", ":")) for value, indices in groups.items())
        assert sorted(i for indices in groups.values() for i in indices) == list(range(len(route[key])))
    parts.append("CONTACT SHEET SOURCE BINDINGS\n" + (N / "contact-sheets" / "index.json").read_text(encoding="utf-8"))
    common = "\n\n".join(parts)
    for label in MODELS:
        own = "\n\n".join((V / f"batch-094-{kind}-{label}.md").read_text(encoding="utf-8")
                          for kind in ["initial", "confirm-679"])
        text = "YOUR OWN COMPLETE PREVIOUS REPORTS\n" + own + "\n\nCOMMON EVIDENCE\n" + common
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
            path = C / f"batch-094-rendered-{label}-packet-683-{i:02d}.txt"
            assert not path.exists()
            path.write_text(chunk, encoding="utf-8")
            resources.append(str(path))
        resources += [str(N / f"n1-094-font-panel-{i}.png") for i in range(1, 6)]
        resources += [str(N / "contact-sheets" / f"sheet-{i:02d}.png") for i in range(1, 21)]
        save(C / f"batch-094-rendered-{label}-resources-683.json", resources)
    save(C / "batch-094-rendered-packet-provenance-683.json", {
        "source": str(dictionary), "sourceSha256": sha(dictionary),
        "selectedEntryIds": ["1298090", "1337570"], "completeFamilies": True,
        "selectionSha256": hashlib.sha256(selected).hexdigest(),
        "routeSource": str(N / "n1-094-article-route.json"), "routeSha256": sha(N / "n1-094-article-route.json"),
        "kanjiRecords": 64, "wordRecords": 384, "grouping": "Lossless exact-row grouping with every original index.",
        "commonEvidenceSha256": hashlib.sha256(common.encode()).hexdigest()})
    print("Starting state and bounded complete evidence prepared; runtime frozen.", flush=True)


def review(label, repair=False):
    frozen()
    if label == "gpt":
        prior = load(C / "batch-094-rendered-683-claude-execution.json")
        repair_record = load(C / "batch-094-rendered-683-claude-serial-repair-execution.json")
        assert not prior["acceptedExecution"] and len(prior["observedToolOverlaps"]) == 1
        assert not prior["unfinishedTools"]
        assert set(prior["requiredResources"]) == set(prior["successfullyReturnedResources"])
        assert repair_record["acceptedExecution"] and len(repair_record["actualDecodedImageReturns"]) == 2
        for record in [prior, repair_record]:
            subprocess.run(["pwsh", "-NoProfile", "-Command",
                            f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                           capture_output=True, check=True)
    if repair:
        assert label == "claude"
        prior = load(C / "batch-094-rendered-683-claude-execution.json")
        assert not prior["acceptedExecution"] and len(prior["observedToolOverlaps"]) == 1
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {prior['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       capture_output=True, check=True)
    model, session = MODELS[label]
    assert f'"{model}"' in (C / "batch-094-rendered-cli-config-683.txt").read_text(encoding="utf-8-sig")
    resources = load(C / f"batch-094-rendered-{label}-resources-683.json")
    prefix = C / f"batch-094-rendered-683-{label}"
    if repair:
        resources = [str(prefix.with_suffix(".md")),
                     str(N / "n1-094-font-panel-1.png"), str(N / "n1-094-font-panel-2.png")]
        prefix = C / "batch-094-rendered-683-claude-serial-repair"
    raw = prefix.with_suffix(".jsonl")
    assert not raw.exists(), "Never overwrite original reviewer evidence"
    prompt = f"""DEPENDENT rendered confirmation in YOUR ORIGINAL session {session}; requested actual model {model}.
Frozen signed content HEAD {HEAD}; native fullarchive18ad4bed and unchanged reviewed teaching4089e881; versioneeae47753a460f72.
This is NOT a fresh blind initial review. No teaching edits occur during either reviewer.
Read ALL resources below IN ORDER, EXACTLY ONE view call per response, wait for result before next.
Only read-only view exposed; no shell, edits, delegation, other reports or parallel tool calls.
Text chunks each <14000characters: full read without ranges. PNGs must be decoded/viewed, not inferred from hashes.
{chr(10).join(resources)}
First text contains YOUR OWN original and confirmation reports, not the other model's. Common evidence is the same for both.
Common evidence includes complete current 削/削る/削除/除/縮める articles, COMPLETE two applicable frozen JMdict families,
complete native route assertions, ALL64 exact kanji pool choices and ALL384 word guard builder records with every original
index retained (losslessly grouped identical records), pairwise quiz contract and sheet-to-original bindings.
Then five original four-font panels cover all41Han including source-only 斫 and components 刂/氵/阝.
Then20contact sheets cover all80remaining PNGs at reduced scale. Disclose reduced-image limits; if necessary inspect a
specific original from the same directory serially and explain why. Do not equate nonblank/hasGlyph/hash with legibility.
Check actual glyph distinctions, source-only wording/readings, full reading tables (left/right scrolled captures), wrapping,
all4articles/3reciprocalpairs/6directions/SystemBack/offline/N1selection/meaning/curatedさく+けずる/drawing traces+recall.
Assess exact displayed defaultN1 wrong labels刑/criminalpunishment,弐/twoformalnumeral,乏/scarce;lacking for削.
Only刑 curated is in N1; 前N5 and判N3 excluded, two production fallbacks. Also inspect ALL64 bounded pool records;
do not confuse bounded sample safety with exhaustive random fallback safety.
384 direct-pair successes only prove three specific guards, not every other option's semantics. Evaluate the observed
削る versus 縮める 'shorten;reduce;shrink' as a HYPOTHESIS using full families/articles and exact displayed quiz operation.
Establish whether a direct exclusion is warranted (with impact/source/confidence), or explain why not; no manufactured quota.
Other concrete consequential defects observed in actual options remain reportable; no corpus-wide speculation required.
Nine injected reference strokes and give-up recall/persistence do NOT certify human handwriting/MLKit.
Native682 coordinator receipts:2 terminalcase0/no skips; fullarchive productionContentSyncONCE;1117kanji5070words126N1
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
Snapshot remains signed {HEAD}, unchanged runtime/teaching. Your original683 complete report and execution are
preserved immutable. Process10176 exited0; all12text chunks and25images returned; exactly panels1+2 overlapped,
therefore that execution is REJECTED for strict serial acceptance. Do not retroactively label it compliant.
EVERYTHING AFTER THOSE TWO PANELS was serial and remains historical evidence; do not repeat broad reads.
Read EXACTLY these THREE resources, in order, ONE view call per response and WAIT for result before next:
{chr(10).join(resources)}
First is YOUR OWN complete report. Freshly decode each PNG separately; confirm scoped glyph legibility and
distinctions across four fonts, including blade/side forms and source-only component appearance on these two panels.
This only repairs those two observations, not the original execution, not new blind credit and not the whole review.
Keep your original article/quiz findings, hypothesis/optional/limitations unchanged unless these two images establish
a precise regression. In particular the uncorrected 削る/縮める exclusion remains unresolved; no edit has occurred.
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
        "execution": 683, "batch": "094", "snapshot": HEAD, "sessionId": session,
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
