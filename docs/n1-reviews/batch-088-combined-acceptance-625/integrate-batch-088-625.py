"""Combined-tree acceptance under the live parent launcher, without lock access."""
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
L = C / "logs" / "0d6e2c6f-10b8-44bf-84e5-be642ac5afd2"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = V / "batch-088-combined-acceptance-625"
HEAD = "9f72a69bcf0bd4da505cfebfe1b30b937dcd6f53"
MAIN = "8a36f8cd81c0e35c330079881cac1a1f3a771e26"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "afff40af0e155dbe"
STAGE = "batch-088-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME088 normal signed owner fast-forward publication and exact public acceptance next; NO089. "
    "Read docs/n1-sources/execution-625.json and docs/n1-reviews/batch-088-combined-acceptance-625. "
    "Freshmain8a36f8cd already ancestor; normal nonrewriting merge Already up to date; no teaching/runtime change. "
    "Fresh fullPython/validator/vocabulary/manifest/budget/source/baseline/exactmembership/all4readings/"
    "1mappedpair/2directions/4directguards/pinned12strokes/27Hanfontprovenance passed. Actual sibling "
    "RealContentTest3+RareHanTest1 fresh, zero skips. All8423runtimehashes/versionafff40af0e155dbe unchanged; "
    "1111kanji5067words120N1labels125namedmembers. Original620 blind ClaudeOpus5.5/GPT6.1Sol,623native "
    "both terminalcase0 and624 dependent original-session visuals reverified, NOT rerun. Original Claude "
    "first2TEXTview overlap preserved with same-session strictlyserial2text correction; all11PNGviews serial, "
    "then GPT13serialcalls after actual exit. No new blindcredit. Fullarchivee445d826 productionContentSyncONCE "
    "zeroProblems/Roomepoch1, onlyonkeyがい and explicitkun[], rawガイ/カイ+かちどき/やわらぐ/order preserved. "
    "ActualN1/All options victorysong;triumph versus凡/凸/凹, all3curated/zero fallback; not futurecustompool "
    "certification. Botharticles/1mappedpair/2directions/4guards/SystemBack/offline/12injectedstrokes/"
    "trace-recallgiveup, NOT humanhandwriting/MLKit/phone. All27Han/fourComposefonts including几/豈/鬨 visible; "
    "fallbackface unknown;112Paintprobes hashes NOT separatelyviewedPNGs; contact sheets downscaled. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latestappmain. Beforepush fetchfreshmain; "
    "ifadvanced normallymerge/reconcile/regenerate/revalidate and independentlyreview substantiveteaching. "
    "Normalsigning/ownerstop-cran processscopedtoken/fastforward only; noamend/forcepush/globalauthswitch. "
    "Verify exactremoteSHA/terminalgreen relevantCI/EVERYruntimehash and manifestequality in EXACTimmutable"
    "GitHubZIP/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepathguards. "
    "Persist authored/reviewed/integrated/publishedSHAs/ledgers/counts/verifiedownerissue60 BEFORE089. "
    "Published114/1228,1114remaining/latestpublic8a36f8cd unchanged until verifieddelivery. Physicalphone/"
    "generalrelease/whole-set outstanding; projectincomplete. Preserve all original source/review/process/"
    "denial/OOM/readdepth/downscale/pool/font/phone limits and optionaldispositions. Parent19008 retains"
    "runner.lock; verify liveancestry/currentrunnersession/checkpoint/exactsignedheads/whollycleanworktrees; "
    "NEVERchildacquire/delete/unlock. Approvedcontrol/committedsources/frozenworkspaceinputs only, no optional"
    "historicalsessionhelpers. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "No089 or newnative/reviewer absent new concern, productionappchange, heap/guardincrease or unreviewedpush."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".625.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


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
        624, "088", "continue", "visual-review-closed-awaiting-combined-acceptance")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["batch088VisualReviewCheckpoint"]["checkpoint"] == 624
    assert not (L / "progress-before-625.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-625.json")
    state = {
        "execution": 625, "batch": "088", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME088 combined current-main acceptance and signed LOCAL evidence only; no publication/089 or new native/reviewer absent changed teaching/new concern.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete approved issue and final624 directly inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial parsed final-state print hit cp1252 after successful full parse; direct final range read successfully."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact current runner session verified; no child lock acquisition/delete/unlock.",
        "ancestryPids": ids,
        "artifactPathPreflight": "Approved control helpers, frozen workspace inputs and committed source/review evidence only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-625.json", state)
    p["execution625StartingState"] = state
    p.update(stage="batch-088-combined-main-integration-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-625.json")
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
    result = batch_audit(R, "088")
    ledger = load(S / "batch-088-progress.json")
    prior = load(S / "batch-088-draft-audit.json")
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
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    occurrences = 0
    for name in ["batch-088-kanjidic2.xml", "batch-088-comparison-kanjidic2.xml"]:
        for row in ET.parse(S / name).getroot().findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            occurrences += 1
    assert occurrences == 6
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
    assert len(published) == 114 and chars - old == published | separate | nonmembers | {"凱"}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    actual_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert actual_counts == {"kanji": 1111, "words": 5067, "n1Labels": 120,
                             "namedSourceMembersPresent": 125}
    assert {f"words/{p.name}" for p in (R / "words").glob("*.md")
            if "凱" in metadata(R, f"words/{p.name}")["kanji"]} == {"words/凱旋.md"}
    assert "jlpt" not in metadata(R, "words/凱旋.md")
    guards = {tuple(sorted((row["word"], other)))
              for row in ledger["wordQuizAudit"]["directExclusions"] for other in row["exclude"]}
    assert len(guards) == 4
    stroke = load(S / "batch-088-stroke-evidence.json")
    svg = (S / "batch-088-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "凱.json") == convert("凱", svg.decode("utf-8"))
    assert stroke["dictionaryStrokeCount"] == stroke["sourceStrokePaths"] == 12
    font = load(S / "batch-088-draft-font-audit.json")
    text = "".join((R / n).read_text(encoding="utf-8") for n in font["completeNewArticleScope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert han == font["actualHan"] and len(han) == 27
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
    assert checked == 8423
    result.update(
        execution=625, latestMain=MAIN, preIntegrationHead=HEAD, upstreamAlreadyAncestor=True,
        normalMergeResult="Already up to date; no artificial merge.",
        runtimeHashesVerified=checked, frozenInputsVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterOccurrencesVerified=occurrences,
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=prior["baselineMetadataExceptions"],
        baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
        exactMembershipAccounted=True, currentCounts=actual_counts,
        publishedIssue60Additions=114, acceptedUnpublishedIssue60Additions=["凱"],
        separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
        remainingIssue60Acceptance=1114, sixEarlierPlacementsCountedAsIssue60Accepted=False,
        requiredAllMappedPairs=1, directedLinksVerified=2, directWordExclusionPairs=4,
        pinnedStrokeGeometryExactlyRegenerated=True, scopedHan=han, fontProvenanceReverified=True,
        runtimePublished=False,
        limits="Mechanical source/baseline/link/reading/hash/font provenance audit, not fresh linguistic/native review. Original reviewer/native limitations retained.",
    )
    save(L / "combined-source-audit-625.json", result)
    print("Combined source audit passed; all8423 runtime hashes and exact membership verified.")


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
        with (L / f"{name}-625.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-625.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-088-reconciliation.json")
    visual = load(V / "batch-088-visual-reconciliation-624.json")
    assert text["textualReviewClosed"] and text["findings"] == []
    assert text["actionableRemainingTeachingFindings"] == 0
    assert text["consequentialUnresolvedTeachingFindings"] == 0
    assert visual["findings"] == [] and visual["serialReviewerProcessesExited"]
    assert visual["eachReviewerImagesDecoded"] == 11 and visual["allImageViewsSerial"]
    assert not visual["entireOriginalClaudeToolRunSerial"]
    for name, expected in text["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    reports = []
    previous = None
    for label, process in text["processes"].items():
        assert process["actualModels"] == [
            "claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
        assert process["exitCode"] == 0 and process["allAssignedRangesReturned"]
        assert sha(V / process["report"]) == process["reportSha256"]
        assert sha(V / f"batch-088-initial-{label}.jsonl") == process["rawExecutionSha256"]
        execution = load(V / process["execution"])
        assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
        if previous is not None:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
        reports.append(process)
    correction = visual["claudeSerialTextCorrection"]
    timeline = [
        ("claude", visual["processes"]["claude"]),
        ("claude-serial-text", correction),
        ("gpt", visual["processes"]["gpt"]),
    ]
    previous = None
    for label, process in timeline:
        assert process["exitCode"] == 0 and process["allAssignedResourcesSuccessfullyReturned"]
        assert process["sessionId"] == text["processes"]["gpt" if label == "gpt" else "claude"]["sessionId"]
        assert process["actualModels"] == [
            "gpt-6.1-sol" if label == "gpt" else "claude-opus-5.5"]
        assert not process["unfinishedTools"] and not process["missingResources"]
        prefix = V / f"batch-088-visual-624-{label}"
        assert sha(prefix.with_suffix(".md")) == process["reportSha256"]
        assert hashlib.sha256(gzip.decompress(
            prefix.with_suffix(".jsonl.gz").read_bytes())).hexdigest() == process["rawSha256"]
        if label == "claude":
            assert len(process["observedToolOverlaps"]) == 1
        else:
            assert not process["observedToolOverlaps"]
        if previous is not None:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    assert correction["serialTextCorrectionOnly"] and len(correction["toolCalls"]) == 2
    receipts_verified = 0
    for number in [623, 624]:
        for row in load(S / f"execution-{number}.json")["receipts"]:
            path = R / row["archive"]
            assert sha(path) == row["archiveSha256"], path
            data = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
            assert hashlib.sha256(data).hexdigest() == row["sourceSha256"], path
            receipts_verified += 1
    native = load(S / "execution-623.json")
    execution = native["executionReceipt"]
    assert execution["passed"] and execution["terminalSuccessCases"] == 2
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    route = native["nativeRoute"]
    assert {k: route[k] for k in ["archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "archiveRequests": 1, "importedKanji": 1111, "importedWords": 5067, "n1Cards": 120, "problems": 0}
    assert route["contentVersion"] == VERSION and route["acceptedReadingParserEpoch"] == 1
    assert route["quizOnKeys"] == ["がい"] and route["quizKunKeys"] == []
    assert route["touchInjectedReferenceStrokes"] == 12
    assert route["completeArticleProjections"] == 2
    assert route["mappedReciprocalPairs"] == 1 and route["directedLinkTransitions"] == 2
    for pool in ["N1", "All"]:
        choices = route["productionBuilderN1AndAllExactChoices"][pool]
        assert choices["availableCuratedCount"] == 3 and choices["fallbackOptions"] == 0
        assert {o["kanji"] for o in choices["options"]} == set("凱凡凸凹")
    assert not git("diff", text["reviewedTeachingSnapshot"], HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", PRODUCTION, APP, "--", "core/src/main", "app/src/main",
                   "gradle.properties", root=A)
    return {
        "initialReviewReports": reports, "nativeTerminalCaseStatuses": [0, 0],
        "archiveReceiptsReverified": receipts_verified, "newNativeOrReviewerRuns": 0,
        "nativeRuntimeMatchesCurrentCombinedTree": True, "nativeRoute": route,
        "nativeEvidence": "docs/n1-sources/execution-623.json",
        "visualEvidence": "docs/n1-reviews/batch-088-visual-reconciliation-624.json",
        "inheritedSourceTextLimits": text["limits"],
        "inheritedVisualLimits": visual["limits"], "visualDispositions": visual["dispositions"],
        "claudeTextOverlapPreserved": True, "sameSessionSerialCorrectionReverified": True,
        "rerunDisposition": "Current main already included; teaching/runtime/app production/font bytes unchanged. Existing native and original dependent visuals remain applicable; no new concern established.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-625.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-625.txt").read_text().strip() == "0 error(s)"
    assert VERSION in (L / "manifest-625.txt").read_text()
    vocabulary = (L / "vocabulary-625.txt").read_text().strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-625.json")["exitCode"] == 0
    assert (L / "host-exit-625.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-625.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-625.txt").read_text().strip())
    ended = datetime.fromisoformat((L / "host-end-625.txt").read_text().strip())
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
    source = load(L / "combined-source-audit-625.json")
    inheritance = inherited()
    budget = ast.literal_eval((L / "budget-625.txt").read_text())
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    assert not D.exists()
    D.mkdir()
    receipts = []
    paths = [
        *(L / name for name in ["starting-state-625.json", "combined-source-audit-625.json", "merge-625.txt",
          "python-tests-625.txt", "validate-625.txt", "manifest-625.txt", "vocabulary-625.txt", "budget-625.txt",
          "host-625.txt", "host-exit-625.txt", "host-command-625.json", "host-start-625.txt", "host-end-625.txt",
          "runner-ancestry-625.json"]),
        *(L / f"{name}-exit-625.json" for name in ["python-tests", "validate", "manifest", "vocabulary", "budget"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-088-combined-host-625.ps1",
        C / "post-batch-088-combined-625.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
        A / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "RealContentTest.kt",
        A / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "PublishableContentFixture.kt",
        A / "app" / "src" / "test" / "java" / "io" / "github" / "stopcran" / "kanji" / "core" / "RareHanTest.kt",
    ]
    for path in paths:
        target = D / (path.name + ".gz" if path.suffix == ".txt" else path.name)
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "sha256": sha(target),
                         "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 625, "batch": "088", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-625.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "normalMerge": True,
        "upstreamAlreadyAncestor": True, "mergeResult": "Already up to date.", "newMergeCommit": False,
        "conflicts": [], "substantiveTeachingConflictEdits": [], "batchTeachingUnchanged": True,
        "runtimeBytesUnchanged": True, "sourceAudit": source, "pythonTestsPassed": int(match[1]),
        "validatorErrors": 0, "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary,
        "manifestFresh": True, "contentVersion": VERSION, "localBudget": budget, "hostSuites": suites,
        "hostChecksFresh": True, "hostTestsExecuted": 4, "androidHead": APP,
        "productionAndroidBytesUnchanged": True, "inheritedAcceptance": inheritance, "receipts": receipts,
        "runtimeAccepted": True, "runtimePublished": False, "publishedAdditions": 114,
        "remainingAdditions": 1114, "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "diagnostics": [
            "First record attempt stopped before any archive/ledger mutation: inherited623 gzip receipts omit losslessGzip, unlike624. Corrected receipt decoding to use the actual .gz archive suffix; both archived-byte and decompressed source hashes remain mandatory. No source receipt changed or acceptance bypassed."
        ],
        "limits": "Local combined-tree acceptance only, not publication or fresh linguistic/native review. Existing vocabulary pilot2122/2431 is consistency, not full coverage. Original source/process/read-depth/denial/OOM/downscale/pool/font/MLKit/phone limitations and optional dispositions preserved. Physical phone/general release/whole set outstanding.",
    }
    save(S / "execution-625.json", evidence)
    path = S / "batch-088-progress.json"
    ledger = load(path)
    ledger["preCombined625State"] = {
        k: ledger.get(k) for k in ["status", "nextAction", "reviewClosed", "runtimeAccepted", "runtimePublished"]}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True,
                  runtimePublished=False, combinedAcceptance="docs/n1-sources/execution-625.json", nextAction=NEXT)
    save(path, ledger)
    body = (
        f"Batch088 checkpoint625: **combined current-main acceptance passed locally; publication next**. "
        f"Fresh main `{MAIN}` already ancestors reviewed local `{HEAD}`; normal non-rewriting merge returned "
        "'Already up to date'. No artificial merge, conflict or teaching/runtime edit.\n\n"
        f"Fresh {match[1]} Python tests, validator0errors, vocabulary consistency (`{vocabulary}`), "
        "regenerated fresh manifest, frozen inputs/decompressed dictionary hashes,25complete lexical families/"
        "6raw character records, original985kanji/4942words/985strokes with recorded exceptions, exact membership, "
        "all4reading dispositions, one reciprocal pair/two directions, four direct guards, pinned12-stroke "
        "regeneration and all27Han/font provenance passed. All8423runtime hashes/"
        f"version`{VERSION}` unchanged;1111kanji/5067words/120N1labels/125named members. "
        "Fresh actual-sibling RealContentTest3+RareHanTest1, zero skips/errors/failures, explicitJDK17/SDK, "
        "oneworker/in-processKotlin/existingapproved2GiBHOSTinit. TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
        "not latestappmain; no app/guest heap change.\n\n"
        "Original620 blind ClaudeOpus5.5/GPT6.1Sol and624 dependent original-session visuals reverified, NOT rerun. "
        "Claude initial2TEXTview overlap preserved with same-session2strictlyserialtext correction; "
        "all11PNGviews serial, GPT13serialcalls after actual exit. Native623 two terminalcase0 and fullarchive"
        "e445d826 productionContentSyncONCE/zeroProblems/acceptedepoch1 remain applicable to unchangedruntime. "
        "Onlyonがい, explicitkun[], rawガイ/カイ+かちどき/やわらぐ/order intact. ActualN1/All production "
        "victorysong;triumph versus凡/凸/凹,3curatedavailable/zero fallback; not futurecustompool certification. "
        "All27Han/fourCompose families visible including几/豈/鬨; botharticles/SystemBack/offline/12injected"
        "strokes/practice-recallgiveup. Contact sheets downscaled; fallback face unidentified; "
        "112Paintrecycledhashes NOT112viewedPNGs; injectedtrace/giveup NOT humanhandwriting/MLKit/phone. "
        "Original reports/evidence/limitations preserved.\n\n"
        f"Local budget:{budget['entries']:,}entries/{budget['retainedBytes']:,}retained/"
        f"{budget['inflatedBytes']:,}inflated/{budget['localZipBytes']:,}compressed bytes. "
        "Original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath guards unchanged. "
        "Evidence:`docs/n1-sources/execution-625.json`, `docs/n1-reviews/batch-088-combined-acceptance-625`.\n\n"
        "**Next bounded checkpoint: freshmain recheck, normal signed owner fast-forward publication, "
        "exact remoteSHA/terminalgreenCI/EVERYimmutablepublicZIP runtime hash and original budgets, "
        "durable publication/verifiedowner issue receipt BEFORE089.** No push/089 here. "
        "Published114/1228;1114remaining unchanged. Compatiblef9b59a2+ required; "
        "physicalphone/generalrelease/whole-set outstanding; project incomplete. "
        "Live parent19008 ancestry/session verified, runner.lock untouched; no optionalhistoricalsessionhelper "
        "or actualnewpermissiondenial.\n"
    )
    (L / "issue-body-625.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance and lossless evidence archived; ready for signed LOCAL checkpoint.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-625.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["sha256"]
        raw = (R / row["archive"]).read_bytes()
        if row["losslessGzip"]:
            raw = gzip.decompress(raw)
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    receipt = load(L / "issue-verified-625.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (L / "issue-body-625.txt").read_bytes().decode("utf-8")
    before = load(L / "progress-before-625.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 624 and p["batch"] == "088"
    row = {
        "schemaVersion": 1, "execution": 625, "checkpoint": 625, "batch": "088",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-625.json", "evidenceSha256": sha(S / "execution-625.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "upstreamAlreadyAncestor": True,
        "runtimeHashesVerified": 8423, "contentVersion": VERSION,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "freshHostTestsPassed": 4, "hostSkips": 0,
        "runtimeAccepted": True, "runtimePublished": False, "runtimeBytesUnchanged": True,
        "newNativeOrReviewerRuns": 0, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 114, "remainingAdditions": 1114, "lastPublishedCommit": MAIN,
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "issueUpdate": receipt["html_url"], "ownerIssueAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(L / "issue-verified-625.json"), "nextAction": NEXT, "blocker": None,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p.update(checkpoint=625, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution625CoordinatorCheckpoint"] = row
    p["batch088CombinedAcceptanceCheckpoint"] = row
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(L / "checkpoint-verification-625.json", row)
    print(f"Checkpoint625 persisted at signed {saved}; full history preserved. SAME088 publication next; no089.")


if __name__ == "__main__":
    {"start": start, "audit": audit, "checks": checks, "record": record, "finish": finish}[sys.argv[1]]()
