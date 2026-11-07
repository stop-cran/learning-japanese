"""Verify batch 096 against current main without touching the parent runner lock."""
import ast
import base64
import copy
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "299afd0f-ad92-4c3b-91c9-b6b56934517d"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
HEAD = "f2b3c7dad3118f7be014a4495009b575dcf097a5"
MAIN = "4c2416e4c5925e6910b32215412bb1b795f60524"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
STAGE = "combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME096 publication only next. Read docs/n1-sources/execution-707.json and "
    "docs/n1-reviews/batch-096-combined-acceptance-707.json at the normally signed "
    "review-closed checkpoint. Fresh main4c2416e4 was already an ancestor; "
    "git merge --no-edit origin/main returned Already up to date; ZERO incoming "
    "runtime/teaching paths and no conflict/merge commit. Full current runtime "
    "equals native705 manifest54645b95fe8e939c/8444hashes exactly, so inherited "
    "two terminalcase0/nativeContentSyncONCE/1119kanji5072words128N1/zeroProblems/"
    "epoch1/oneonGOU-noKun/ONEreciprocalpair-TWOdirections/Back-offline-tenstrokes/"
    "fourfontpanels-all28Han and original706rendered confirmations remain applicable; "
    "NOT a new native run, no changed-manifest import claim. Original702 "
    "claude-opus-5.5 then gpt-6.1-sol blind initials plus own-session supplements "
    "and706 dependent confirmations preserved with actual process/model/read limits. "
    "Bounded64kanji/1536twelvewordguard samples CLEAN; untested seeds/pools/"
    "all-other-word-option semantics UNVERIFIED. Fresh707 all372Python, validate, "
    "regeneratedmanifest, vocabularypilot2122of2431, complete frozen sources/"
    "fullbaseline/readings/stroke/allmappedlinks/font provenance/8444hashes/"
    "originalbudgets and FOUR Android RealContentTHREE+RareHanONE/no skips passed. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "Local reviewClosed=[U+525B], published=[]; counts STILL122of1228/1106remaining. "
    "Fetch latestoriginmain before publication; if advanced, normal nonrewriting "
    "merge/reconcile/regenerate/revalidate ACTUALcombinedtree and independently "
    "confirm any substantive changed teaching; reassess exact changed-native scope. "
    "Never push unreviewed content or bypass signing/branchprotection. After all "
    "gates, scoped stop-cran owner token ONLY in publication child; verify identity, "
    "normal signed ownerfastforward to origin/main (no authswitch/tokenpersist/"
    "forcepush/amend), verify exactremoteSHA/terminalgreenCI/EVERY immutable "
    "publicZIP runtimeentryhash/manifest equality/original18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath. Local "
    "nativeZIP is NOT publicacceptance. Preserve authored/reviewed/integrated/"
    "published SHAs, write source/publication ledgers and exactownerissue receipt; "
    "checkpoint accepted publication before starting097. Parent19008 retains "
    "runner.lock: verify liveancestry/session/signedheads/whollyclean; NO child "
    "acquire/delete/unlock/readprobe. Approved control/committed evidence/frozen "
    "inputs only, no optional historicalsessionhelpers. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. Physicalphone/generalrelease/"
    "whole-set outstanding; no phone/humanhandwriting/MLKit/universalquiz-safety "
    "claim. No097 or secondrunner or runtimepublication at707."
)
sys.path.insert(0, str(R / "tools"))


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, value):
    temp = p.with_suffix(p.suffix + ".707.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(p)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def context(clean=True, content=HEAD):
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    script = f"""
$id={os.getpid()};$chain=@()
while($id -gt 0 -and $chain.Count -lt 12){{
 $p=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(!$p){{break}}
 $chain+=@{{pid=[int]$p.ProcessId;parent=[int]$p.ParentProcessId;name=$p.Name;command=$p.CommandLine}}
 if($id -eq 19008){{break}}
 $id=$p.ParentProcessId
}}
$chain|ConvertTo-Json -Depth 4 -Compress
"""
    chain = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert chain[-1]["pid"] == 19008
    assert any(p["name"].lower() == "copilot.exe" and L.name in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (706, "096", "continue")
    assert git("rev-parse", "origin/main") == MAIN
    for root, expected in [(R, content), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if clean or root == A:
            assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)
    return {
        "parentPid": 19008, "session": L.name, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
    }


def runtime():
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
            "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True,
            "runtimeChanged": False}


def start():
    role = context()
    before = L / "progress-before-707.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution706CoordinatorCheckpoint"] == p["execution706CoordinatorCheckpoint"]
    assert git("merge-base", "--is-ancestor", MAIN, HEAD) == ""
    assert not git("diff", HEAD + "...origin/main", "--name-only")
    state = {
        "execution": 707, "batch": "096", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME096 combined-current-main acceptance and signed LOCAL review-closed checkpoint; no publication/097.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, entire approved issue and final706 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed packets/frozen workspace inputs only; no optional historical-session helpers accessed.",
        "integration": {"result": "Already up to date; current origin/main is an ancestor.",
                        "newIncomingPaths": [], "overlappingTeaching": [], "mergeCommitNeeded": False},
    }
    save(L / "starting-state-707.json", state)
    p["execution707StartingState"] = state
    p.update(stage="batch-096-combined-main-acceptance-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    assert all(p[k] == v for k, v in load(before).items() if k not in {"stage", "nextAction", "blocker"})
    print("SAME096 combined acceptance started; current main already integrated, parent lock untouched.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    context()
    result = batch_audit(R, "096")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(gzip.decompress(jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    ledger = load(S / "batch-096-progress.json")
    packets = []
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        expected = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / packet["xml"]).read_bytes()
        if i < 2:
            suffix = "full-family-reading.txt.gz" if i == 0 else "comparison-full-family-reading.txt.gz"
            compact = gzip.decompress((S / f"batch-096-{suffix}").read_bytes())
            assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact.decode("utf-8") + "</JMdict>")] == [
                canonical(e) for e in ET.fromstring(expected)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(S / packet["xml"]),
                        "freshFrozenExtractionMatches": True})
    assert sum(p["families"] for p in packets) == 105 and result["dictionaryFamilies"] == 102
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    count = 0
    for name in ["batch-096-kanjidic2.xml", "batch-096-comparison-kanjidic2.xml"]:
        for row in ET.parse(S / name).getroot().findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            count += 1
    assert count == 12
    draft = load(S / "batch-096-draft-audit.json")
    exceptions = draft["baselineMetadataExceptions"]
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in load(S / "baseline-inventory.json")["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name in draft["baselineKanjiDistractorException"]:
                expected["distractors"] = draft["baselineKanjiDistractorException"][name]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and len(named) == 1232
    chars = {p.stem for p in (R / "kanji").glob("*.md")}
    before = json.loads(git("show", f"{MAIN}:manifest.json"))
    old = {Path(n).stem for n in before["files"] if n.startswith("kanji/")}
    assert chars - old == {"\u525b"} and not old - chars
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    for char in "\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50":
        assert metadata(R, f"kanji/{char}.md")["jlpt"] == 2
    current_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert current_counts == {"kanji": 1119, "words": 5072, "n1Labels": 128, "namedSourceMembersPresent": 133}
    pairs = {(c, row["article"]) for row in ledger["supportMappings"]
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {("\u525b", "words/\u525b\u5065.md")}
    word = metadata(R, "words/\u525b\u5065.md")
    assert "jlpt" not in word and word["kanji"] == ["\u525b", "\u5065"]
    assert not (R / "kanji" / "\u5065.md").exists()
    assert len(word["quiz_exclusions"]) == 12
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
    svg = (S / "batch-096-kanjivg.svg").read_bytes()
    stroke = load(S / "batch-096-stroke-evidence.json")
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "\u525b.json") == convert("\u525b", svg.decode("utf-8"))
    font = load(S / "batch-096-draft-font-audit.json")
    text = "".join((R / name).read_text(encoding="utf-8") for name in font["completeArticleScope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert han == font["actualHan"] and len(han) == 28
    for row in font["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path) == row["sha256"]
        with TTFont(path) as face:
            cmap = face.getBestCmap()
        assert {c: ord(c) in cmap for c in han} == row["actualPresence"]
    result.update(
        execution=707, combinedContentHead=HEAD, integratedMain=MAIN,
        mainAlreadyAncestor=True, incomingRuntimeChanges=[], runtime=runtime(),
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        packets=packets, familyOccurrences=105, distinctFamilies=102,
        completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException=draft["baselineKanjiDistractorException"],
        currentCounts=current_counts, allMappedReciprocalPairs=1, directedLinksVerified=2,
        activatedBaselinePairs=0, pinnedStrokeGeometryExactlyRegenerated=True,
        scopedHan=han, fontProvenanceReverified=True,
        limits="Fresh mechanical combined audit, not a new linguistic/native/phone or public-archive review.",
    )
    save(L / "combined-source-audit-707.json", result)
    print("Frozen sources/baseline/readings/strokes/all mapped links/font provenance and 8444 hashes passed.")


def checks():
    context()
    for name, arguments in [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]:
        command = [sys.executable, "-X", "utf8", "-B", *arguments]
        with (L / f"{name}-707.txt").open("w", encoding="utf-8") as output:
            completed = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-707.json", {"command": command, "exitCode": completed.returncode})
        assert completed.returncode == 0, name
        print(name, "passed", flush=True)
    audit()


def inherited():
    textual = load(V / "batch-096-reconciliation.json")
    rendered = load(V / "batch-096-rendered-reconciliation-706.json")
    native = load(S / "execution-705.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert rendered["actionableRemainingFindings"] == 0
    assert rendered["consequentialUnresolvedInScopeClaims"] == 0
    for name, value in textual["reviewedRuntimeHashes"].items():
        assert sha(R / name) == value, name
    previous = None
    for name, process in textual["processes"].items():
        expected = "claude-opus-5.5" if name.endswith("claude") else "gpt-6.1-sol"
        assert process["actualModels"] == [expected] and process["exitCode"] == 0
        assert process["allAssignedRangesReturned"] and not process["observedToolOverlaps"]
        assert process["exactFullPacketReturnedInOneCall"]
        assert sha(V / process["report"]) == process["reportSha256"]
        assert sha(V / f"batch-096-{name}.jsonl") == process["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    receipts_checked = 0
    for row in load(S / "execution-706.json")["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
        receipts_checked += 1
    previous = None
    for label in ["claude", "gpt"]:
        record = load(V / f"batch-096-rendered-706-{label}-execution.json")
        assert record["acceptedExecution"] and record["exitCode"] == 0
        assert record["actualModels"] == ["claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(record["startedAt"])
        previous = record["completedAt"]
    assert native["terminalPerCaseStatus"] == [0, 0] and native["nativeTestsSkipped"] == 0
    assert native["fullArchiveImportedOnce"] and native["contentVersion"] == runtime()["contentVersion"]
    route = load(R / native["routeEvidence"])
    assert (route["archiveRequests"], route["importedKanji"], route["importedWords"],
            route["n1Cards"], route["problems"], route["acceptedReadingParserEpoch"]) == (1, 1119, 5072, 128, 0, 1)
    assert route["offline"] and route["reciprocalLinkAndSystemBack"] and route["drawingTraceThenRecall"]
    assert len(route["productionBuilderN1AndAllExactChoices"]) == 64
    assert len(route["directGuardBuilderChecks"]) == 1536
    for row in load(R / native["artifactIndex"]):
        assert sha(R / row["path"]) == row["sha256"]
        receipts_checked += 1
    assert not git("diff", native["contentSnapshot"], HEAD, "--", "manifest.json")
    assert not git("diff", "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", APP,
                   "--", "core/src/main", "app/src/main", "gradle.properties", root=A)
    frozen = load(S / "execution-704.json")["fixtureVerification"]
    path = Path(frozen["archive"])
    assert path.is_relative_to(C) and sha(path) == frozen["archiveSha256"]
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        manifests = [n for n in names if n.endswith("/manifest.json")]
        assert len(manifests) == 1
        prefix = manifests[0][:-len("manifest.json")]
        manifest = load(R / "manifest.json")
        assert json.loads(archive.read(manifests[0])) == manifest
        verified = 0
        for kind, entries in manifest.items():
            if isinstance(entries, dict):
                for name, digest in entries.items():
                    raw = archive.read(prefix + name)
                    normalized = raw if kind in {
                        "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else raw.replace(b"\r\n", b"\n")
                    assert hashlib.sha256(normalized).hexdigest() == digest, name
                    assert normalized == ((R / name).read_bytes() if kind in {
                        "images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                        else (R / name).read_bytes().replace(b"\r\n", b"\n")), name
                    verified += 1
        assert verified == 8444
    return {
        "initialRecord": "docs/n1-reviews/batch-096-reconciliation.json",
        "nativeRecord": "docs/n1-sources/execution-705.json",
        "renderedRecord": "docs/n1-reviews/batch-096-rendered-reconciliation-706.json",
        "receiptHashesReverified": receipts_checked,
        "originalTeachingAndStrokesUnchanged": True,
        "native705EqualsCombinedManifest": True, "nativeArchiveRuntimeHashesReverified": verified,
        "nativeArchiveSha256": frozen["archiveSha256"],
        "newNativeRuns": 0, "newReviewers": 0,
        "originalLimits": {"textual": textual["limits"], "native": native["limits"], "rendered": rendered["limits"]},
        "incomingTeachingReview": "Not needed: ZERO incoming changes; current main already an ancestor.",
        "changedNativeScope": "None: exact full manifest and every imported runtime payload remain identical. Reuse explicitly attributed native705 evidence, not a new import.",
    }


def record():
    context()
    assert not git("diff", "--check")
    tests = (L / "python-tests-707.txt").read_text(encoding="utf-8-sig")
    assert re.search(r"^Ran 372 tests in ", tests, re.M) and re.search(r"^OK$", tests, re.M)
    assert "skipped=" not in tests
    assert (L / "validate-707.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    assert (L / "vocabulary-707.txt").read_text(encoding="utf-8").strip() == (
        "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot")
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-707.json")["exitCode"] == 0
    assert (L / "host-exit-707.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-707.txt").read_text(encoding="utf-8-sig")
    begin = datetime.fromisoformat((L / "host-start-707.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((L / "host-end-707.txt").read_text(encoding="utf-8-sig").strip())
    suites = []
    for module, task, cls, names in [
        ("core", "test", "RealContentTest", {
            "parsesRealContentRepoWhenPresent", "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
            "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent"}),
        ("app", "testDebugUnitTest", "RareHanTest", {"contentRareCharactersAreCoveredByBundledFont"}),
    ]:
        path = A / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{cls}.xml"
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == len(names)
        assert all(xml.attrib[k] == "0" for k in ["skipped", "errors", "failures"])
        assert {x.attrib["name"] for x in xml.findall("testcase")} == names
        assert not any(xml.findall(".//" + name) for name in ["skipped", "failure", "error"])
        stamp = datetime.fromisoformat(xml.attrib["timestamp"]).astimezone(timezone.utc)
        assert begin <= stamp <= end and path.stat().st_mtime >= begin.timestamp()
        suites.append({"path": str(path), "sha256": sha(path), "suite": xml.attrib,
                       "cases": [x.attrib for x in xml.findall("testcase")]})
    assert all((A / module / ".." / ".." / "learning-japanese").resolve() == R for module in ["app", "core"])
    budget = ast.literal_eval((L / "budget-707.txt").read_text(encoding="utf-8"))
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    inheritance = inherited()
    source = load(L / "combined-source-audit-707.json")
    assert source["exactBaseRuntimePreservedOutsideRecordedChanges"]
    directory = V / "batch-096-combined-acceptance-707"
    assert not directory.exists()
    directory.mkdir()
    paths = [
        *(L / name for name in ["starting-state-707.json", "combined-source-audit-707.json",
          "python-tests-707.txt", "validate-707.txt", "manifest-707.txt", "vocabulary-707.txt",
          "budget-707.txt", "host-707.txt", "host-exit-707.txt", "host-command-707.json",
          "host-start-707.txt", "host-end-707.txt"]),
        *(L / f"{name}-exit-707.json" for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-096-host-707.ps1",
        C / "post-batch-096-combined-707.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        A / "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    ]
    receipts = []
    for path in paths:
        raw = path.read_bytes()
        compressed = path.suffix == ".txt"
        target = directory / (path.name + (".gz" if compressed else ""))
        assert not target.exists(), target
        target.write_bytes(gzip.compress(raw, mtime=0) if compressed else raw)
        assert (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes()) == raw
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "archiveSha256": sha(target),
                         "losslessGzip": compressed})
    evidence = {
        "schemaVersion": 1, "execution": 707, "batch": "096", "status": STAGE,
        "startingState": load(L / "starting-state-707.json"),
        "authoredTeachingSnapshot": "b26bcf9b328872b1575cf89e187973fea0a32a31",
        "reviewedSnapshot": HEAD, "combinedTestedSnapshot": HEAD,
        "integratedMain": MAIN, "mainAlreadyAncestor": True, "incomingChanges": [],
        "substantiveTeachingChanged": False, "runtime": runtime(),
        "checks": {"pythonTests": 372, "validatorErrors": 0, "manifestFresh": True,
                   "vocabulary": "2122/2431 reviewed prompts; stage=pilot; not full coverage",
                   "originalArchiveBudgets": budget, "androidTests": suites,
                   "androidTestsTotal": 4, "androidSkipped": 0, "freshAndroidExecution": True,
                   "actualResolvedContentRoot": str(R), "gradleExitCode": 0},
        "sourceAudit": source, "inheritedAcceptance": inheritance, "receipts": receipts,
        "reviewClosed": ["\u525b"], "published": [], "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "runtimeAccepted": True,
        "runtimeAcceptanceScope": "Local bounded owner-testing acceptance; not public delivery/general release.",
        "runtimePublished": False, "newReviewers": 0, "newNativeRuns": 0,
        "qualifiedTestOnlyAndroid": APP, "unchangedProductionAndroid": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "latestAppMainClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "publishedAdditions": 122, "remainingAdditions": 1106, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "limits": [
            "Prior reports/native receipts remain inherited, not newly performed. Byte/hash rechecks do not certify comprehension.",
            "Bounded64kanji/1536direct-guard samples only; untested pools/seeds/all-other word-option semantic safety UNVERIFIED.",
            "Injected strokes/give-up recall are not human handwriting/MLKit; exact fallback face unidentified.",
            "Physical-phone/general-release and whole-set acceptance outstanding.",
            "No new main delta, so no additional changed-teaching review or native rerun required. Any later main advance must be reassessed.",
            "Immutable public ZIP/terminal CI/owner fast-forward/verified publication issue remain pending. Local archive not public acceptance.",
        ],
        "nextAction": NEXT,
    }
    save(S / "execution-707.json", evidence)
    save(V / "batch-096-combined-acceptance-707.json", evidence)
    path = S / "batch-096-progress.json"
    ledger = load(path)
    ledger.update(status=STAGE, reviewClosed=["\u525b"], published=[], nextAction=NEXT)
    ledger["pendingGates"] = [
        "Fresh main check before normal signed owner fast-forward; non-rewriting merge/reconcile/revalidate and changed-teaching/native scope reassessment if main advances.",
        "Terminal green CI, every immutable public ZIP runtime entry/hash under original budgets, exact owner issue receipt and durable accepted publication checkpoint; no097 before publication.",
    ]
    ledger["combinedAcceptance707"] = {
        "evidence": "docs/n1-sources/execution-707.json",
        "reviewRecord": "docs/n1-reviews/batch-096-combined-acceptance-707.json",
        "status": STAGE, "reviewClosed": ["\u525b"], "runtimeAccepted": True,
        "runtimePublished": False, "contentVersion": "54645b95fe8e939c",
        "mainAlreadyAncestor": True, "incomingChanges": [], "native705StillExact": True,
        "freshPythonTests": 372, "freshAndroidTests": 4, "freshAndroidSkipped": 0,
        "historicalLimitDisposition": "Earlier draft/pending limits retained as historical; this record supersedes local acceptance status only, not public delivery.",
    }
    save(path, ledger)
    print("Combined local bounded acceptance archived; no runtime changes or publication.")


def issue():
    body = (
        "Batch096 / checkpoint707: **combined-current-main acceptance complete locally; not yet published**.\n\n"
        "Current `origin/main` remains `4c2416e4`; it is already an ancestor of signed `f2b3c7da`. "
        "Normal non-rewriting merge returned Already up to date: zero incoming teaching/runtime changes. "
        "The exact manifest `54645b95fe8e939c` and all8,444 runtime hashes still match native705's full "
        "production ContentSync import. Its two terminal native case successes and serial two-family "
        "rendered confirmations remain inherited, not rerun or relabelled as fresh evidence.\n\n"
        "Fresh combined checks passed:372 Python tests, validator0 errors, regenerated manifest unchanged, "
        "vocabulary consistency2122/2431 pilot prompts (not complete coverage), full frozen dictionaries/"
        "baseline/readings/strokes/all-mapped links/font provenance and four non-skipped Android cases "
        "(RealContentTest3, RareHanTest1). Local packaging:8,466 entries;30,280,311 compressed/"
        "44,620,567 inflated/44,352,229 retained bytes, within unchanged guards. Qualified TESTONLY "
        "Android `1c1b7bf4` retains production `f9b59a2`; this is not latest app main.\n\n"
        "剛 is locally review-closed with necessary support剛健, soleゴウ/noKun and twelve direct word guards. "
        "No substantive content was edited. Original blind/supplement/rendered reports and limitations "
        "are preserved. Bounded64 kanji/1536 guard records are not universal quiz-safety certification; "
        "untested pools/seeds/all-other-word-option semantics remain UNVERIFIED.\n\n"
        "Evidence:`docs/n1-sources/execution-707.json` and "
        "`docs/n1-reviews/batch-096-combined-acceptance-707.json` in the signed local checkpoint. "
        "**Next:** fresh-main check, normal authorized owner fast-forward, terminal-green CI and every "
        "immutable public ZIP runtime hash/budget check, then publication ledgers/checkpoint before097. "
        "Published coverage stays122/1228,1106 remaining until delivery is verified. Physical-phone/"
        "general-release/whole-set acceptance remains outstanding. Parent runner lock untouched; "
        "no historical-session helper access or new permission denial."
    )
    (C / "batch-096-combined-707-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print("Owner issue body prepared.")


def finalize():
    head = git("rev-parse", "HEAD")
    context(content=head)
    assert git("rev-parse", "HEAD^") == "7564b28d41574897272dbcc46be80447b9d3ffdf"
    assert git("rev-parse", "HEAD^^") == HEAD
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-707.json")
    expected = {r["archive"] for r in evidence["receipts"]} | {
        "docs/n1-sources/execution-707.json", "docs/n1-reviews/batch-096-combined-acceptance-707.json",
        "docs/n1-sources/batch-096-progress.json",
        "docs/n1-sources/execution-707-finalization-correction.py",
        "docs/n1-sources/execution-707-finalization-correction.json"}
    assert set(git("diff", "--name-only", HEAD, "HEAD").splitlines()) == expected
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    prefix = C / "batch-096-combined-707-issue-"
    body = Path(str(prefix) + "body.txt").read_bytes().decode("utf-8-sig")
    receipt = load(Path(str(prefix) + "receipt.json"))
    posted = load(Path(str(prefix) + "posted.json"))
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = load(C / "progress.json"), load(L / "progress-before-707.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 707, "checkpoint": 707, "batch": "096",
        "savedCommit": head, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-707.json",
        "reviewRecord": "docs/n1-reviews/batch-096-combined-acceptance-707.json",
        "authoredTeachingSnapshot": evidence["authoredTeachingSnapshot"],
        "reviewedSnapshot": HEAD, "combinedTestedSnapshot": HEAD, "integratedMain": MAIN,
        "mainAlreadyAncestor": True, "incomingChanges": [], **runtime(),
        "reviewClosed": ["\u525b"], "published": [], "runtimeAccepted": True,
        "runtimeAcceptanceScope": evidence["runtimeAcceptanceScope"], "runtimePublished": False,
        "freshPythonTests": 372, "freshAndroidTests": 4, "freshAndroidSkipped": 0,
        "newNativeRuns": 0, "newReviewers": 0, "native705StillExact": True,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 122, "remainingAdditions": 1106, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "checkpointHelper": str(Path(__file__)), "checkpointHelperSha256": sha(Path(__file__)),
        "finalizationCorrection": "docs/n1-sources/execution-707-finalization-correction.json",
        "nextAction": NEXT,
    }
    state.update(checkpoint=707, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution707CoordinatorCheckpoint"] = checkpoint
    state["batch096CombinedAcceptanceCheckpoint"] = checkpoint
    state["execution707StartingState"]["status"] = "signed-local-combined-acceptance-checkpoint-complete"
    save(C / "progress.json", state)
    reread = load(C / "progress.json")
    assert all(reread[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-707.json", checkpoint)
    print("Checkpoint707 persisted; all", len(before), "original historical root values preserved.")
    print(head, receipt["html_url"])


if __name__ == "__main__":
    {"start": start, "checks": checks, "preflight": context,
     "record": record, "issue": issue, "finalize": finalize}[sys.argv[1]]()
