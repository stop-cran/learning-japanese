"""Bounded combined acceptance; the live parent retains runner.lock."""
import ast
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
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "b212b472-70c6-4c56-bf3f-d60fc3a970a0"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = V / "batch-087-combined-acceptance-616"
HEAD = "a721b53a6046ba724e59c427e2d3017cdd53e720"
MAIN = "6eaa018dcbcabe57d9e22ddf6b07c6b8ee2dfea6"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "eb3a9413cccd4f57"
STAGE = "batch-087-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME087 normal signed owner fast-forward publication and exact public acceptance next; NO088. "
    "Read docs/n1-sources/execution-616.json and docs/n1-reviews/batch-087-combined-acceptance-616. "
    "Current main6eaa018d already ancestor; normal nonrewriting merge Already up to date, no teaching change. "
    "Fresh full Python/validator/vocabulary/manifest/budget/source/baseline/membership/two readings/"
    "two reciprocal pairs/four directions/seven direct guards/pinned six strokes/font provenance and "
    "actual sibling RealContentTest3+RareHanTest1 zero skips passed. All8420 runtime hashes/"
    "versioneb3a9413cccd4f57 unchanged; 1110kanji5066words119N1labels124named members. "
    "Original611 blind ClaudeOpus5.5/GPT6.1Sol,614 native two terminalcase0 and615 dependent original-session "
    "visuals reverified, not rerun. Full archive404f507d productionContentSyncONCE zeroProblems/Roomepoch1. "
    "Both kunkeysなぎ/なぐ scheduled, on[]; modernweather凪ぐ versus feelings和ぐ/classical forms separate. "
    "All21Han/fourCompose fonts readable; actualfallbackface unknown, contact sheets downscaled. "
    "DefaultN1 yuzu pictured; seeded613chestnut/Allwind JSON only; no universal futurepool safety. "
    "Paint84+8 recycled hashes NOT92exportedPNGs; injectedtrace/recallgiveup NOT handwriting/MLKit/phone. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latestappmain. "
    "Before push fetch freshmain; if advanced normallymerge/reconcile/regenerate/revalidate and independently "
    "review substantivechangedteaching. Normal signing/ownerstop-cran processscopedtoken/fastforward only; "
    "no amend/forcepush/globalauthswitch. Verify exactremoteSHA/terminalgreen relevantCI/EVERYruntimehash "
    "and manifest in EXACTimmutableGitHubZIP/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepathguards. Persist authored/reviewed/integrated/publishedSHAs/ledgers/counts and "
    "verifiedownerissue60 BEFORE088. Published113/1228,1115remaining/latestpublic6eaa018d unchanged until "
    "verified delivery; 087notpublished. Separate earlierN2保案派第策結 preserved, not acceptedissue60batches. "
    "Physicalphone/generalrelease/whole-set outstanding; projectincomplete. Preserve all original source/"
    "review/process/denial/OOM/readdepth/downscale/pool/font/phone limits and optional dispositions. "
    "Parent19008 retainsrunner.lock throughout; verify liveancestry/currentrunnersession/checkpoint/"
    "exactsignedheads/whollycleanworktrees; NEVERchildacquire/delete/unlock. Approvedcontrol/committedsources/"
    "frozenworkspaceinputs only, no optionalhistoricalsessionhelpers. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. No088, new native/reviewer absent new concern, or unreviewed push."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".616.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)


def context():
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    command = (
        "$ids=@();$p=$PID;for($i=0;$i -lt 10 -and $p;$i++){"
        "$r=Get-CimInstance Win32_Process -Filter \"ProcessId=$p\";"
        "if(-not $r){break};$ids+=$r.ProcessId;$p=$r.ParentProcessId};"
        "ConvertTo-Json -InputObject $ids"
    )
    ids = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", command], encoding="utf-8"))
    assert 19008 in ids, ids
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    return ids


def start():
    ids = context()
    clean(R, HEAD)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (
        615, "087", "continue", "visual-review-closed-awaiting-combined-acceptance")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 615
    assert not (L / "progress-before-616.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-616.json")
    state = {
        "execution": 616, "batch": "087", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME087 combined current-main acceptance and signed LOCAL evidence only; no publication/088 or new native/reviewer absent changed teaching/new concern.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete approved issue and final615 directly inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial final-lines print hit cp1252; direct final range then read successfully."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact current runner session verified; no child lock acquisition/delete/unlock.",
        "ancestryPids": ids,
        "artifactPathPreflight": "Approved control helpers, frozen workspace inputs and committed source/review evidence only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-616.json", state)
    p["execution616StartingState"] = state
    p.update(stage="batch-087-combined-main-integration-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-616.json")
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    print("Starting scope persisted with full history; parent lock untouched.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    context()
    clean(R, HEAD)
    assert git("merge-base", MAIN, HEAD) == MAIN
    result = batch_audit(R, "087")
    ledger = load(S / "batch-087-progress.json")
    prior = load(S / "batch-087-draft-audit.json")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(gzip.decompress(jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    packets = []
    for packet in ledger["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        expected = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / packet["xml"]).read_bytes()
        packets.append({"path": packet["xml"], "families": len(ids),
                        "freshFrozenExtractionMatches": True, "sha256": sha(S / packet["xml"])})
    assert sum(p["families"] for p in packets) == 25
    kd_root = ET.fromstring(kd)
    records = {e.findtext("literal"): e for e in kd_root.findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    occurrences = 0
    for name in ["batch-087-kanjidic2.xml", "batch-087-comparison-kanjidic2.xml"]:
        packet = ET.parse(S / name).getroot()
        for row in packet.findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            occurrences += 1
    assert occurrences == 5
    baseline = load(S / "baseline-inventory.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in prior["baselineMetadataExceptions"]:
                expected["quiz_exclusions"] = prior["baselineMetadataExceptions"][name]
            if name in prior["baselineKanjiDistractorException"]:
                expected["distractors"] = prior["baselineKanjiDistractorException"][name]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and len(named) == 1232
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    chars = {path.stem for path in (R / "kanji").glob("*.md")}
    separate, nonmembers = set("保案派第策結"), set("坊的誰身阪")
    assert len(published) == 113 and chars - old == published | separate | nonmembers | {"凪"}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    actual_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert actual_counts == {"kanji": 1110, "words": 5066, "n1Labels": 119,
                             "namedSourceMembersPresent": 124}
    assert {f"words/{p.name}" for p in (R / "words").glob("*.md")
            if "凪" in metadata(R, f"words/{p.name}")["kanji"]} == {"words/凪.md", "words/凪ぐ.md"}
    assert all("jlpt" not in metadata(R, name) for name in ["words/凪.md", "words/凪ぐ.md"])
    guards = {tuple(sorted((row["word"], other)))
              for row in ledger["wordQuizAudit"]["directExclusions"] for other in row["exclude"]}
    assert len(guards) == 7
    stroke = load(S / "batch-087-stroke-evidence.json")
    svg = (S / "batch-087-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "凪.json") == convert("凪", svg.decode("utf-8"))
    font = load(S / "batch-087-draft-font-audit.json")
    text = "".join((R / n).read_text(encoding="utf-8") for n in font["completeNewArticleScope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert han == font["actualHan"] and len(han) == 21
    for row in font["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path) == row["sha256"]
        with TTFont(path) as face:
            cmap = face.getBestCmap()
        assert {c: ord(c) in cmap for c in han} == row["actualPresence"]
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json") and manifest["contentVersion"] == VERSION
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8420
    result.update(
        execution=616, latestMain=MAIN, preIntegrationHead=HEAD, upstreamAlreadyAncestor=True,
        normalMergeResult="Already up to date; no artificial merge.",
        runtimeHashesVerified=checked, frozenInputsVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterOccurrencesVerified=occurrences,
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=prior["baselineMetadataExceptions"],
        baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
        exactMembershipAccounted=True, currentCounts=actual_counts,
        publishedIssue60Additions=113, acceptedUnpublishedIssue60Additions=["凪"],
        separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
        remainingIssue60Acceptance=1115, sixEarlierPlacementsCountedAsIssue60Accepted=False,
        requiredAllMappedPairs=2, directedLinksVerified=4, directWordExclusionPairs=7,
        pinnedStrokeGeometryExactlyRegenerated=True, scopedHan=han, fontProvenanceReverified=True,
        runtimePublished=False,
        limits="Mechanical source/baseline/link/reading/hash/font provenance audit, not fresh linguistic/native review. Original reviewer/native limitations retained.",
    )
    save(L / "combined-source-audit-616.json", result)
    print("Combined source audit passed; all8420 runtime hashes and exact membership verified.")


def checks():
    context()
    clean(R, HEAD)
    for name, args in [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]:
        command = [sys.executable, "-X", "utf8", "-B", *args]
        with (L / f"{name}-616.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-616.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-087-reconciliation.json")
    visual = load(V / "batch-087-visual-reconciliation-615.json")
    assert text["textualReviewClosed"] and text["findings"] == []
    assert visual["findings"] == [] and visual["serialProcessesExited"]
    assert visual["eachReviewerImagesDecoded"] == 12 and visual["eachReviewerSerialViewCalls"] == 14
    for name, expected in text["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    reports = []
    for prefix, group in [("initial", text["processes"]), ("visual-615", visual["processes"])]:
        previous = None
        for label, process in group.items():
            assert process["actualModels"] == [
                "claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
            assert process["exitCode"] == 0
            report = V / f"batch-087-{prefix}-{label}.md"
            assert sha(report) == process["reportSha256"]
            execution = load(V / f"batch-087-{prefix}-{label}-execution.json")
            assert execution["sessionId"] == process["sessionId"] and execution["exitCode"] == 0
            assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
            raw = V / f"batch-087-{prefix}-{label}.jsonl"
            if prefix == "initial":
                assert sha(raw) == process["rawExecutionSha256"] and process["allAssignedRangesReturned"]
            else:
                assert hashlib.sha256(gzip.decompress(raw.with_suffix(".jsonl.gz").read_bytes())).hexdigest() == process["rawSha256"]
                assert process["allAssignedResourcesSuccessfullyReturned"] and not process["missingResources"]
                assert len(process["toolCalls"]) == 14
            if previous is not None:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
            previous = process["completedAt"]
            reports.append({"report": report.relative_to(R).as_posix(),
                            "reportSha256": sha(report), "sessionId": process["sessionId"],
                            "actualModels": process["actualModels"], "exitCode": 0, "rerun": False})
    receipts_verified = 0
    for number in [614, 615]:
        evidence = load(S / f"execution-{number}.json")
        for row in evidence["receipts"]:
            path = R / row["archive"]
            assert sha(path) == row["archiveSha256"], path
            data = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
            assert hashlib.sha256(data).hexdigest() == row["sourceSha256"], path
            receipts_verified += 1
    native = load(S / "execution-614.json")
    execution = native["executionReceipt"]
    assert execution["passed"] and execution["terminalSuccessCases"] == 2
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    route = native["nativeRoute"]
    assert {k: route[k] for k in ["archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "archiveRequests": 1, "importedKanji": 1110, "importedWords": 5066, "n1Cards": 119, "problems": 0}
    assert route["contentVersion"] == VERSION and route["acceptedReadingParserEpoch"] == 1
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["なぎ", "なぐ"]
    assert not git("diff", text["reviewedTeachingSnapshot"], HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", PRODUCTION, APP, "--", "core/src/main", "app/src/main",
                   "gradle.properties", root=A)
    return {"reviewReports": reports, "nativeTerminalCaseStatuses": [0, 0],
            "archiveReceiptsReverified": receipts_verified, "newNativeOrReviewerRuns": 0,
            "nativeRuntimeMatchesCurrentCombinedTree": True, "nativeRoute": route,
            "nativeEvidence": "docs/n1-sources/execution-614.json",
            "visualEvidence": "docs/n1-reviews/batch-087-visual-reconciliation-615.json",
            "inheritedSourceTextLimits": text["limits"],
            "inheritedVisualLimits": visual["limits"], "visualDispositions": visual["dispositions"],
            "rerunDisposition": "Current main already included; teaching/runtime/app production/font bytes unchanged. Existing native and original dependent visuals remain applicable; no new concern established."}


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-616.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-616.txt").read_text().strip() == "0 error(s)"
    assert VERSION in (L / "manifest-616.txt").read_text()
    vocabulary = (L / "vocabulary-616.txt").read_text().strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-616.json")["exitCode"] == 0
    assert (L / "host-exit-616.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-616.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-616.txt").read_text().strip())
    ended = datetime.fromisoformat((L / "host-end-616.txt").read_text().strip())
    suites = []
    for relative, names in [
        ("core\\build\\test-results\\test\\TEST-io.github.stopcran.kanji.core.RealContentTest.xml",
         {"parsesRealContentRepoWhenPresent", "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
          "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent"}),
        ("app\\build\\test-results\\testDebugUnitTest\\TEST-io.github.stopcran.kanji.core.RareHanTest.xml",
         {"contentRareCharactersAreCoveredByBundledFont"}),
    ]:
        path = A / relative
        xml = ET.parse(path).getroot()
        assert xml.attrib["tests"] == str(len(names))
        assert all(xml.attrib[k] == "0" for k in ["skipped", "errors", "failures"])
        assert {x.attrib["name"] for x in xml.findall("testcase")} == names
        assert not any(xml.findall(".//" + name) for name in ["skipped", "failure", "error"])
        stamp = datetime.fromisoformat(xml.attrib["timestamp"]).astimezone(timezone.utc)
        assert started <= stamp <= ended and path.stat().st_mtime >= started.timestamp()
        suites.append({"path": str(path), "sha256": sha(path), "suite": xml.attrib,
                       "cases": [x.attrib for x in xml.findall("testcase")]})
    assert all((A / module / ".." / ".." / "learning-japanese").resolve() == R for module in ["app", "core"])
    source = load(L / "combined-source-audit-616.json")
    inheritance = inherited()
    budget = ast.literal_eval((L / "budget-616.txt").read_text())
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    assert not D.exists()
    D.mkdir()
    receipts = []
    paths = [
        *(L / name for name in ["starting-state-616.json", "combined-source-audit-616.json", "merge-616.txt",
          "python-tests-616.txt", "validate-616.txt", "manifest-616.txt", "vocabulary-616.txt", "budget-616.txt",
          "host-616.txt", "host-exit-616.txt", "host-command-616.json", "host-start-616.txt", "host-end-616.txt",
          "runner-ancestry-616.json"]),
        *(L / f"{name}-exit-616.json" for name in ["python-tests", "validate", "manifest", "vocabulary", "budget"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-087-combined-host-616.ps1",
        C / "post-batch-087-combined-616.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
    ]
    for path in paths:
        target = D / (path.name + ".gz" if path.suffix == ".txt" else path.name)
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "sha256": sha(target),
                         "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 616, "batch": "087", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-616.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "normalMerge": True,
        "upstreamAlreadyAncestor": True, "mergeResult": "Already up to date.", "newMergeCommit": False,
        "conflicts": [], "substantiveTeachingConflictEdits": [], "batchTeachingUnchanged": True,
        "runtimeBytesUnchanged": True, "sourceAudit": source, "pythonTestsPassed": int(match[1]),
        "validatorErrors": 0, "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary,
        "manifestFresh": True, "contentVersion": VERSION, "localBudget": budget, "hostSuites": suites,
        "hostChecksFresh": True, "hostTestsExecuted": 4, "androidHead": APP,
        "productionAndroidBytesUnchanged": True, "inheritedAcceptance": inheritance, "receipts": receipts,
        "runtimeAccepted": True, "runtimePublished": False, "publishedAdditions": 113,
        "remainingAdditions": 1115, "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Local combined-tree acceptance only, not publication or fresh linguistic/native review. Existing vocabulary pilot2122/2431 is consistency, not full coverage. All original source/process/read-depth/denial/OOM/downscale/pool/font/MLKit/phone limitations and optional dispositions preserved. Physical phone/general release/whole set outstanding.",
    }
    save(S / "execution-616.json", evidence)
    path = S / "batch-087-progress.json"
    ledger = load(path)
    ledger["preCombined616State"] = {
        k: ledger.get(k) for k in ["status", "nextAction", "reviewClosed", "runtimeAccepted", "runtimePublished"]}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True,
                  runtimePublished=False, combinedAcceptance="docs/n1-sources/execution-616.json", nextAction=NEXT)
    save(path, ledger)
    body = (
        f"Batch087 checkpoint616: **combined current-main acceptance passed locally; publication next**. "
        f"Fresh main `{MAIN}` already ancestors reviewed local `{HEAD}`; normal non-rewriting merge returned "
        "'Already up to date'. No artificial merge, conflict or teaching edit.\n\n"
        f"Fresh {match[1]} Python tests, validator0errors, actual vocabulary consistency (`{vocabulary}`), "
        "regenerated fresh manifest, frozen inputs/decompressed dictionary hashes,25complete lexical families/"
        "5raw character records, original985kanji/4942words/985strokes with recorded exceptions, exact membership, "
        "both reading dispositions, two reciprocal pairs/four directions, seven direct guards, pinned six-stroke "
        "regeneration and all21Han/font provenance passed. All8420runtime hashes/"
        f"version`{VERSION}` unchanged;1110kanji/5066words/119N1labels/124named members. "
        "Fresh actual-sibling RealContentTest3+RareHanTest1 with zero skips/errors/failures, explicitJDK17/SDK, "
        "oneworker/in-processKotlin/existingapproved2GiBHOSTinit. TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
        "not latestappmain; no app/guest heap change.\n\n"
        "Original611 blind ClaudeOpus5.5/GPT6.1Sol and615 dependent original-session visuals reverified, not rerun. "
        "614 two terminalcase0 native and fullarchive404f507d productionContentSyncONCE/"
        "zeroProblems/acceptedepoch1 remain applicable to unchangedruntime. Bothkunkeysなぎ/なぐ, on[]; "
        "modern weather凪ぐ separated from feelings和ぐ/classical forms. All21Han/fourCompose families readable. "
        "DefaultN1yuzu pictured; seed613chestnut/Allwind receiptJSON only, not universal futurepool safety. "
        "Contact sheets downscaled; fallback face unidentified; Paint84+8 recycledhashes NOT92PNGs; "
        "injectedtrace/giveup NOT humanhandwriting/MLKit/phone. Original reports/evidence/limitations preserved.\n\n"
        f"Local budget:{budget['entries']:,}entries/{budget['retainedBytes']:,}retained/"
        f"{budget['inflatedBytes']:,}inflated/{budget['localZipBytes']:,}compressed bytes. "
        "Original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath guards unchanged. "
        "Evidence:`docs/n1-sources/execution-616.json`, `docs/n1-reviews/batch-087-combined-acceptance-616`.\n\n"
        "**Next bounded checkpoint: freshmain recheck, normal signed owner fast-forward publication, "
        "exact remoteSHA/terminalgreenCI/EVERYimmutablepublicZIP runtime hash and original budgets, "
        "durable publication/verifiedowner issue receipt BEFORE088.** No push/088 here. "
        "Published113/1228;1115remaining unchanged; separate earlierN2source placements not counted as issue60batches. "
        "Compatiblef9b59a2+ required; physicalphone/generalrelease/whole-set outstanding; project incomplete. "
        "Live parent19008 ancestry/session verified, runner.lock untouched; no optionalhistoricalsessionhelper "
        "or actualnewpermissiondenial.\n"
    )
    (L / "issue-body-616.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance and lossless evidence archived; ready for signed LOCAL checkpoint.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-616.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["sha256"]
    receipt = load(L / "issue-verified-616.json")
    assert receipt["user"]["login"] == "stop-cran"
    body = (L / "issue-body-616.txt").read_bytes().decode("utf-8")
    assert receipt["body"] == body
    before = load(L / "progress-before-616.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 615 and p["batch"] == "087"
    row = {
        "schemaVersion": 1, "execution": 616, "checkpoint": 616, "batch": "087",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-616.json", "evidenceSha256": sha(S / "execution-616.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "upstreamAlreadyAncestor": True,
        "runtimeHashesVerified": 8420, "contentVersion": VERSION,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "freshHostTestsPassed": 4, "hostSkips": 0,
        "runtimeAccepted": True, "runtimePublished": False, "runtimeBytesUnchanged": True,
        "newNativeOrReviewerRuns": 0, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 113, "remainingAdditions": 1115, "lastPublishedCommit": MAIN,
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "issueUpdate": receipt["html_url"], "ownerIssueAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(L / "issue-verified-616.json"), "nextAction": NEXT, "blocker": None,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p.update(checkpoint=616, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution616CoordinatorCheckpoint"] = row
    p["batch087CombinedAcceptanceCheckpoint"] = row
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(L / "checkpoint-verification-616.json", row)
    print(f"Checkpoint616 persisted at signed {saved}; full history preserved. SAME087 publication next; no088.")


if __name__ == "__main__":
    {"start": start, "audit": audit, "checks": checks, "record": record, "finish": finish}[sys.argv[1]]()
