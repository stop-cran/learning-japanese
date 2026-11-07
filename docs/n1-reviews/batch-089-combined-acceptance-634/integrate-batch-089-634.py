"""Batch089 combined-tree acceptance; the live parent owns runner.lock."""
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
L = C / "logs" / "1541ec7f-54e5-4694-b61c-6a3844f61509"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = V / "batch-089-combined-acceptance-634"
HEAD = "6a7e18f11311d172c11043cb010611b16007c723"
MAIN = "703ebf5fba412aefdc516ea18b36658d227631d1"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "c6562f11cb371053"
STAGE = "batch-089-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME089 normal signed owner fast-forward publication and exact public acceptance next; NO090. "
    "Read docs/n1-sources/execution-634.json and docs/n1-reviews/batch-089-combined-acceptance-634. "
    "Fresh origin/main703ebf5f already ancestor of reviewed6a7e18f1; normal nonrewriting merge "
    "Already up to date; no substantive teaching/runtime change. Fresh fullPython/validator/"
    "vocabulary consistency/manifestfreshness/budget/source/fullbaseline/exactmembership/onefullreading/"
    "twoallmappedpairs/fourdirections/onedirectguard/pinnedfourstrokes/23Hanfontprovenance and "
    "actual sibling RealContentTest3+RareHanTest1 zero skips required and recorded in634. "
    "8426runtimehashes/versionc6562f11cb371053;1112kanji5068words121N1labels126namedmembers. "
    "Original629 blind ClaudeOpus5.5/GPT6.1Sol,632native bothterminalcase0 and633 original-session "
    "dependentvisuals reverified NOT rerun. Original GPT redundant/truncatedtail reads retained. "
    "Fullarchive72614eda productionContentSyncONCE/zeroProblems/Roomepoch1; soleonきょうGood/done, "
    "rawkun[]/explicitquizkun[]. Actual N1/All options illfortune;evil versus凡/凸/凹 all3available/"
    "zerofallback; not futurecustompool certification. Bothnewarticles and ONLYchanged作navigationline/"
    "SystemBack/offline/fourinjectedstrokes/trace-recallgiveup, NOT humanhandwriting/MLKit/phone. "
    "All23Han/fourComposefonts including乂/凵 visible; fallbackfaceunknown;96Painthashprobes NOT "
    "separatelyviewedPNGs; contact sheets downscaled. Agriculturalnoun/verypooryield notharvestverb/"
    "necessaryzeroyield/famine/badwork; compound-specific作crop/yield. TESTONLYAndroid1c1b7bf4 retains "
    "unchangedproductionf9b59a2, NOTlatestappmain. Beforepush fetchfreshmain; ifadvanced normallymerge/"
    "reconcile/regenerate/revalidate and independentlyreview substantive teaching. Normalsigning/"
    "ownerstop-cran processscopedtoken/normalfastforward only; noamend/forcepush/globalauthswitch. "
    "Verify exactremoteSHA/terminalgreen relevantCI/EVERYruntimeentryhash and manifestequality in EXACT"
    "immutableGitHubZIP/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-"
    "safepathguards. Persist authored/reviewed/integrated/publishedSHAs/ledgers/counts/verifiedownerissue60 "
    "BEFORE090. Published115/1228,1113remaining/latestpublic703ebf5f unchanged until verifieddelivery. "
    "Physicalphone/generalrelease/whole-set outstanding; projectincomplete. Keep original source/"
    "review/process/denial/OOM/readdepth/downscale/pool/font/phone limits and optionaldispositions. "
    "Parent19008 ownsrunner.lock; verify liveancestry/currentrunnersession/checkpoint/exactsignedheads/"
    "whollycleanworktrees; NEVERchildacquire/delete/unlock. Approvedcontrol/committedsources/"
    "frozenworkspaceinputs only, no optionalhistoricalsessionhelpers. Preserve/report/yield actual"
    "newdenial/signinghang/uncertainownership. No090/newnative/reviewer absent new concern, production"
    "appchange, heap/guardincrease or unreviewedpush."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".634.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == value
    tmp.replace(path)


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
        633, "089", "continue", "visual-review-closed-awaiting-combined-acceptance")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["execution633CoordinatorCheckpoint"]["checkpoint"] == 633
    assert not (L / "progress-before-634.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-634.json")
    state = {
        "execution": 634, "batch": "089", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME089 combined current-main acceptance and signed LOCAL evidence only; no publication/090 or new native/reviewer absent changed teaching/new concern.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete approved issue and final633 directly inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial parsed-state print hit cp1252 after successful full parse; direct final range read successfully."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact current runner session verified; no child lock acquisition/delete/unlock.",
        "ancestryPids": ids,
        "artifactPathPreflight": "Approved control helpers, frozen workspace inputs and committed source/review evidence only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-634.json", state)
    p["execution634StartingState"] = state
    p.update(stage="batch-089-combined-main-integration-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-634.json")
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
    result = batch_audit(R, "089")
    ledger = load(S / "batch-089-progress.json")
    prior = load(S / "batch-089-draft-audit.json")
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
    assert sum(p["families"] for p in packets) == 73
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    occurrences = 0
    for name in ["batch-089-kanjidic2.xml", "batch-089-comparison-kanjidic2.xml"]:
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
    assert len(published) == 115 and chars - old == published | separate | nonmembers | {"凶"}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    actual_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert actual_counts == {"kanji": 1112, "words": 5068, "n1Labels": 121,
                             "namedSourceMembersPresent": 126}
    assert {f"words/{p.name}" for p in (R / "words").glob("*.md")
            if "凶" in metadata(R, f"words/{p.name}")["kanji"]} == {"words/凶作.md"}
    assert "jlpt" not in metadata(R, "words/凶作.md")
    assert ledger["allMappedReciprocalPairs"] == [["凶", "words/凶作.md"], ["作", "words/凶作.md"]]
    for char, word in ledger["allMappedReciprocalPairs"]:
        assert f"(../{word})" in (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../kanji/{char}.md)" in (R / word).read_text(encoding="utf-8")
    guards = {tuple(sorted((row["word"], other)))
              for row in ledger["wordQuizAudit"]["directExclusions"] for other in row["exclude"]}
    assert guards == {tuple(sorted(("凶作", "収穫")))}
    stroke = load(S / "batch-089-stroke-evidence.json")
    svg = (S / "batch-089-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "凶.json") == convert("凶", svg.decode("utf-8"))
    assert stroke["dictionaryStrokeCount"] == stroke["sourceStrokePaths"] == 4
    font = load(S / "batch-089-draft-font-audit.json")
    text = "".join((R / n).read_text(encoding="utf-8") for n in font["completeNewArticleScope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert han == font["actualHan"] and len(han) == 23
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
    assert checked == 8426
    result.update(
        execution=634, latestMain=MAIN, preIntegrationHead=HEAD, upstreamAlreadyAncestor=True,
        runtimeHashesVerified=checked, frozenInputsVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterOccurrencesVerified=occurrences,
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=prior["baselineMetadataExceptions"],
        baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
        exactMembershipAccounted=True, currentCounts=actual_counts,
        publishedIssue60Additions=115, acceptedUnpublishedIssue60Additions=["凶"],
        separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
        remainingIssue60Acceptance=1113, sixEarlierPlacementsCountedAsIssue60Accepted=False,
        requiredAllMappedPairs=2, directedLinksVerified=4, directWordExclusionPairs=1,
        pinnedStrokeGeometryExactlyRegenerated=True, scopedHan=han, fontProvenanceReverified=True,
        runtimePublished=False,
        limits="Mechanical source/baseline/link/reading/hash/font provenance audit, not fresh linguistic/native review. Original reviewer/native limitations retained.",
    )
    save(L / "combined-source-audit-634.json", result)
    print("Combined source audit passed; all8426 runtime hashes and exact membership verified.")


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
        with (L / f"{name}-634.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-634.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-089-reconciliation.json")
    visual = load(V / "batch-089-visual-reconciliation-633.json")
    assert text["textualReviewClosed"] and text["findings"] == []
    assert text["actionableRemainingTeachingFindings"] == 0
    assert text["consequentialUnresolvedTeachingFindings"] == 0
    assert visual["findings"] == [] and visual["serialReviewerProcessesExited"]
    assert visual["eachReviewerImagesDecoded"] == 11 and visual["allToolViewsSerial"]
    for name, expected in text["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    previous = None
    for label, process in text["processes"].items():
        assert process["actualModels"] == [
            "claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
        assert process["exitCode"] == 0 and process["allAssignedRangesReturned"]
        assert not process["observedToolOverlaps"]
        assert sha(V / process["report"]) == process["reportSha256"]
        assert sha(V / f"batch-089-initial-{label}.jsonl") == process["rawExecutionSha256"]
        if previous is not None:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    previous = None
    for label, process in visual["processes"].items():
        assert process["exitCode"] == 0 and process["allAssignedResourcesSuccessfullyReturned"]
        assert process["sessionId"] == text["processes"][label]["sessionId"]
        assert process["actualModels"] == [
            "gpt-6.1-sol" if label == "gpt" else "claude-opus-5.5"]
        assert not process["unfinishedTools"] and not process["missingResources"]
        assert not process["observedToolOverlaps"] and len(process["toolCalls"]) == 13
        prefix = V / f"batch-089-visual-633-{label}"
        assert sha(prefix.with_suffix(".md")) == process["reportSha256"]
        assert hashlib.sha256(gzip.decompress(
            prefix.with_suffix(".jsonl.gz").read_bytes())).hexdigest() == process["rawSha256"]
        if previous is not None:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    receipts_verified = 0
    for number in [632, 633]:
        for row in load(S / f"execution-{number}.json")["receipts"]:
            path = R / row["archive"]
            assert sha(path) == row["archiveSha256"], path
            data = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
            assert hashlib.sha256(data).hexdigest() == row["sourceSha256"], path
            receipts_verified += 1
    native = load(S / "execution-632.json")
    execution = native["executionReceipt"]
    assert execution["passed"] and execution["terminalSuccessCases"] == 2
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    route = native["nativeRoute"]
    assert {k: route[k] for k in ["archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "archiveRequests": 1, "importedKanji": 1112, "importedWords": 5068, "n1Cards": 121, "problems": 0}
    assert route["contentVersion"] == VERSION and route["acceptedReadingParserEpoch"] == 1
    assert route["quizOnKeys"] == ["きょう"] and route["quizKunKeys"] == []
    assert route["touchInjectedReferenceStrokes"] == 4 and route["completeArticleProjections"] == 2
    assert route["mappedReciprocalPairs"] == 2 and route["directedLinkTransitions"] == 4
    for pool in ["N1", "All"]:
        choices = route["productionBuilderN1AndAllExactChoices"][pool]
        assert choices["availableCuratedCount"] == 3 and choices["fallbackOptions"] == 0
        assert {o["kanji"] for o in choices["options"]} == set("凶凡凸凹")
    assert not git("diff", text["reviewedTeachingSnapshot"], HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", PRODUCTION, APP, "--", "core/src/main", "app/src/main",
                   "gradle.properties", root=A)
    return {
        "initialReviewReports": text["processes"], "nativeTerminalCaseStatuses": [0, 0],
        "archiveReceiptsReverified": receipts_verified, "newNativeOrReviewerRuns": 0,
        "nativeRuntimeMatchesCurrentCombinedTree": True, "nativeRoute": route,
        "nativeEvidence": "docs/n1-sources/execution-632.json",
        "visualEvidence": "docs/n1-reviews/batch-089-visual-reconciliation-633.json",
        "inheritedSourceTextLimits": text["limits"], "inheritedVisualLimits": visual["limits"],
        "visualDispositions": visual["dispositions"],
        "rerunDisposition": "Current main already included; teaching/runtime/app production/font bytes unchanged. Existing native and original dependent visuals remain applicable; no new concern established.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-634.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-634.txt").read_text().strip() == "0 error(s)"
    assert VERSION in (L / "manifest-634.txt").read_text()
    vocabulary = (L / "vocabulary-634.txt").read_text().strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-634.json")["exitCode"] == 0
    assert (L / "host-exit-634.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-634.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-634.txt").read_text().strip())
    ended = datetime.fromisoformat((L / "host-end-634.txt").read_text().strip())
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
    source = load(L / "combined-source-audit-634.json")
    inheritance = inherited()
    budget = ast.literal_eval((L / "budget-634.txt").read_text())
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    assert not D.exists()
    D.mkdir()
    receipts = []
    paths = [
        *(L / name for name in ["starting-state-634.json", "combined-source-audit-634.json", "merge-634.txt",
          "python-tests-634.txt", "validate-634.txt", "manifest-634.txt", "vocabulary-634.txt", "budget-634.txt",
          "host-634.txt", "host-exit-634.txt", "host-command-634.json", "host-start-634.txt", "host-end-634.txt",
          "runner-ancestry-634.json"]),
        *(L / f"{name}-exit-634.json" for name in ["python-tests", "validate", "manifest", "vocabulary", "budget"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-089-combined-host-634.ps1",
        C / "post-batch-089-combined-634.ps1", C / "batch-065-host-integration-heap.init.gradle",
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
        "schemaVersion": 1, "execution": 634, "batch": "089", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-634.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "normalMerge": True,
        "upstreamAlreadyAncestor": True, "mergeResult": "Already up to date.", "newMergeCommit": False,
        "conflicts": [], "substantiveTeachingConflictEdits": [], "batchTeachingUnchanged": True,
        "runtimeBytesUnchanged": True, "sourceAudit": source, "pythonTestsPassed": int(match[1]),
        "validatorErrors": 0, "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary,
        "manifestFresh": True, "contentVersion": VERSION, "localBudget": budget, "hostSuites": suites,
        "hostChecksFresh": True, "hostTestsExecuted": 4, "androidHead": APP,
        "productionAndroidBytesUnchanged": True, "inheritedAcceptance": inheritance, "receipts": receipts,
        "runtimeAccepted": True, "runtimePublished": False, "publishedAdditions": 115,
        "remainingAdditions": 1113, "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Local combined-tree acceptance only, not publication or fresh linguistic/native review. Existing vocabulary pilot2122/2431 is consistency, not full coverage. Original source/process/read-depth/denial/OOM/downscale/pool/font/MLKit/phone limitations and optional dispositions preserved. Physical phone/general release/whole set outstanding.",
    }
    save(S / "execution-634.json", evidence)
    path = S / "batch-089-progress.json"
    ledger = load(path)
    ledger["preCombined634State"] = {
        k: ledger.get(k) for k in ["status", "nextAction", "reviewClosed", "runtimeAccepted", "runtimePublished"]}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True,
                  runtimePublished=False, combinedAcceptance="docs/n1-sources/execution-634.json", nextAction=NEXT)
    save(path, ledger)
    body = (
        "**Batch089 checkpoint634: combined current-main acceptance passed locally; publication next.** "
        f"Fresh main `{MAIN}` already ancestors reviewed `{HEAD}`; normal non-rewriting merge returned "
        "'Already up to date'. No conflict, artificial merge or teaching/runtime edit.\n\n"
        f"Fresh {match[1]} Python tests, validator0errors, vocabulary consistency (`{vocabulary}`), "
        "regenerated manifest, all8426runtimehashes/version`c6562f11cb371053`, frozeninputs/decompressed"
        "dictionaryhashes/73completelexicalfamilies/6rawcharacters, original985kanji4942words985strokes "
        "with recorded exceptions, exactmembership, soleキョウ reading/explicitkun[], twoallmappedpairs/"
        "fourdirections/onedirect収穫guard, regenerated pinnedfourstrokes and23Han/font provenance passed. "
        "Actual1112kanji5068words121N1labels126namedmembers. Fresh actual-sibling RealContentTest3+"
        "RareHanTest1 passed, zero skips/errors/failures; explicitJDK17/SDK/oneworker/in-processKotlin/"
        "existingapproved2GiBHOSTinit. TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, notlatestappmain; "
        "no app/guestheap change.\n\n"
        "Original629 blind ClaudeOpus5.5/GPT6.1Sol and633 dependent original-session visuals reverified, "
        "NOT rerun; original GPT redundant/truncatedtailreads retained. Native632 bothterminalcase0/"
        "fullarchive72614eda productionContentSyncONCE/zeroProblems/acceptedepoch1 unchanged. Singleon"
        "きょうGood/done/rawkun[]/explicitquizkun[]. ActualN1/All options illfortune;evil versus凡/凸/凹/"
        "all3curatedavailable/zerofallback, notfuturecustompool certification. Botharticles and ONLYchanged"
        "作navigationline/SystemBack/offline/fourinjectedstrokes/trace-recallgiveup. All23Han/fourCompose"
        "fonts including乂/凵 visible; contact sheets downscaled, fallbackfaceunidentified,96Painthashes "
        "NOT96viewedPNGs. Not humanhandwriting/MLKit/phone. Agriculturalnoun/verypooryield, notharvestverb/"
        "necessaryzeroyield/famine/badwork; compound-specific作crop/yield. Original limitations retained.\n\n"
        f"Local budget: {budget['entries']:,}entries/{budget['retainedBytes']:,}retained/"
        f"{budget['inflatedBytes']:,}inflated/{budget['localZipBytes']:,}compressed bytes. "
        "Original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath guards "
        "unchanged. Evidence:`docs/n1-sources/execution-634.json` and "
        "`docs/n1-reviews/batch-089-combined-acceptance-634`.\n\n"
        "**Next bounded checkpoint: freshmain recheck, normal signed owner fast-forward publication, "
        "exactremoteSHA/terminalgreenCI/EVERYimmutablepublicZIP runtimehash and originalbudgets, durable"
        "publication and verifiedownerissue receipt BEFORE090.** No push/090 here. Published115/1228, "
        "1113remaining unchanged. Compatiblef9b59a2+ required; physicalphone/generalrelease/whole-set "
        "outstanding; projectincomplete. Liveparent19008 ancestry/session verified; runner.lock untouched. "
        "No optionalhistoricalsessionhelper or actualnewpermissiondenial.\n"
    )
    (L / "issue-body-634.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance and lossless evidence archived; ready for signed LOCAL checkpoint.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-634.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["sha256"]
        raw = (R / row["archive"]).read_bytes()
        if row["losslessGzip"]:
            raw = gzip.decompress(raw)
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    receipt = load(L / "issue-verified-634.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (L / "issue-body-634.txt").read_bytes().decode("utf-8")
    before = load(L / "progress-before-634.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 633 and p["batch"] == "089"
    row = {
        "schemaVersion": 1, "execution": 634, "checkpoint": 634, "batch": "089",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-634.json", "evidenceSha256": sha(S / "execution-634.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "upstreamAlreadyAncestor": True,
        "runtimeHashesVerified": 8426, "contentVersion": VERSION,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "freshHostTestsPassed": 4, "hostSkips": 0,
        "runtimeAccepted": True, "runtimePublished": False, "runtimeBytesUnchanged": True,
        "newNativeOrReviewerRuns": 0, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 115, "remainingAdditions": 1113, "lastPublishedCommit": MAIN,
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "issueUpdate": receipt["html_url"], "ownerIssueAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(L / "issue-verified-634.json"), "nextAction": NEXT, "blocker": None,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p.update(checkpoint=634, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution634CoordinatorCheckpoint"] = row
    p["batch089CombinedAcceptanceCheckpoint"] = row
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(L / "checkpoint-verification-634.json", row)
    print(f"Checkpoint634 persisted at signed {saved}; full history preserved. SAME089 publication next; no090.")


if __name__ == "__main__":
    {"start": start, "audit": audit, "checks": checks, "record": record, "finish": finish}[sys.argv[1]]()
