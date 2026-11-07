"""Bounded combined-tree acceptance; the live parent owns runner.lock."""
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
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
L = C / "logs" / "f99e439b-a5bf-4a02-b480-83487f5d40e4"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-092-combined-acceptance-665"
HEAD = "c6767ac962fb647004940ab20d49126bd3ee6643"
MAIN = "2186eda1bf306c7cc16c1ceca80d273dd893a0bd"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "6246dc622f7139c2a0e16d2e03847d6494391fae"
VERSION = "8445a5717d080dcc"
CHAR, WORD = "\u5208", "\u5208\u308b"
STAGE = "batch-092-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME092 normal signed owner fast-forward publication and exact public acceptance next; no093 "
    "until verified delivery. Read docs/n1-sources/execution-665.json and "
    "docs/n1-reviews/batch-092-combined-acceptance-665. Combined acceptance passed at signed "
    "c6767ac9 against freshly fetched main2186eda1 already an ancestor; normal nonrewriting "
    "merge Already up to date, no substantive teaching/runtime change. Fresh fullPython/"
    "validator/vocabulary consistency/regenerated manifest/budget/frozen source/full baseline/"
    "exact membership/all3rawreadings/onlykunKaru-noon/one allmappedbaselinepair/two directions/"
    "one new directwordguard preserving original/pinned4strokes/16Han-fontprovenance/"
    "all8434runtimehashes and sibling RealContentTest3+RareHanTest1 zero skips recorded. "
    "Initial660 independent Claude/GPT textual reviews and664 original-session serial "
    "dependent visual confirmations inherited with complete reports and limits, NOT rerun "
    "or newblindcredit. Native663 TWOterminalcase0/noskips/fullarchive62c6d3e2 through "
    "productionContentSyncONCE/1115kanji5070words124N1zeroProblems/version8445a5717d080dcc/"
    "acceptedRoomepoch1, onlykunKaru persistedGoodDone/noon/fullLite rawsourceorder, "
    "N1+All all3curatedwrongcards/zerofallback/fourpinnedstrokes/onepair/twodirections/"
    "SystemBack/offline inherited NOT rerun. All16Han across3actualComposepanels/4productionfonts "
    "readable inclU+5202;25of42PNGsviewed/17notseparatelyviewed; toolresized900x2000, "
    "wordbodyheadingnotseparatelypictured and original source/read limits retained. "
    "64individual+4wholewordPaint probes NOT68viewedPNGs/identifiedfallbackface. "
    "Injectedtrace/recallgiveup NOT humanhandwriting/successfulMLKit/phone; actualUI "
    "modelunavailable/shapeonly. Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOTlatestappmain. Freshmain/exactsignedheads/whollyclean recheck before publication; "
    "if main advanced normalmerge/reconcile/regenerate/revalidate actualcombinedtree and "
    "independentlyreview substantiveteachingchanges. No amend/forcepush/signingbypass/"
    "globalauthswitch/heapguardincrease/productionappchange. Ownerstop-cran token ONLY "
    "publicationchild, verify exactremoteSHA/terminalgreen relevantCI/EVERY immutable "
    "GitHubZIP runtimeentryhash/manifest equality/original18000entries42MiBcompressed/"
    "80MiBinflated56MiBretained/perfile-media-safepath guards. Persist authored/reviewed/"
    "integrated/publishedSHAs/ledgers/verifiedownerissue60 receipt before093. "
    "Published118/1228,1110remaining unchanged until verified delivery. "
    "Physicalphone/generalrelease/whole-set outstanding, projectincomplete. "
    "Parent19008 ownsrunner.lock: verify liveancestry/decodedlauncher/exactcurrentrunnersession/"
    "checkpoint/signedheads/whollyclean; NEVERchildacquire/delete/unlock. "
    "Approvedcontrol/committed evidence/frozenworkspaceinputs only, no optionalhistoricalsession "
    "helpers. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "No093/newrunner/redundantnative/reviewer."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data, ensure_ascii=True):
    temporary = path.with_suffix(path.suffix + ".665.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(data, ensure_ascii=ensure_ascii, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == data
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
    script = r"""
$ids=@();$p=$PID;$owned=$false
while($p -gt 0){
    $r=Get-CimInstance Win32_Process -Filter "ProcessId=$p"
    if(-not $r){break}
    $ids+=$r.ProcessId
    if($r.ProcessId -eq 19008){
        $command=$r.CommandLine
        if($command -match '-EncodedCommand ([A-Za-z0-9+/=]+)'){
            $command=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
        }
        $owned=$command.Contains('C:\Users\stop-\n1-kanji-workspace\control\runner.ps1')
        break
    }
    $p=$r.ParentProcessId
}
@{ids=$ids;owned=$owned}|ConvertTo-Json
"""
    ancestry = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert ancestry["owned"] and 19008 in ancestry["ids"]
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (664, "092", "continue")
    return ancestry


def start():
    ancestry = context()
    clean(R, HEAD)
    assert not (L / "progress-before-665.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-665.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["batch092VisualAcceptanceCheckpoint"]["savedCommit"] == HEAD
    state = {
        "execution": 665, "batch": "092", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME092 combined-current-main acceptance and normally signed LOCAL evidence; publication next, no093/newnative/reviewer.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and final checkpoint parsed; operative contract, entire approved issue and final664 directly inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial scalar output hit cp1252 after successful full parse; later UTF-8 bounded output succeeded."},
        "runnerLockRole": {"parentPid": 19008, "session": L.name, "ancestry": ancestry,
                           "parentLockTouched": False},
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-665.json", state)
    p = load(C / "progress.json")
    p["execution665StartingState"] = state
    p.update(stage="batch-092-combined-main-acceptance-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-665.json")
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    print("SAME092 starting scope persisted; original history preserved; parent lock untouched.")


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
    result = batch_audit(R, "092")
    ledger, prior = load(S / "batch-092-progress.json"), load(S / "batch-092-draft-audit.json")
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
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(S / packet["xml"])})
    assert sum(p["families"] for p in packets) == 75
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    occurrences = 0
    for name in ["batch-092-kanjidic2.xml", "batch-092-comparison-kanjidic2.xml"]:
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
    published = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    chars = {path.stem for path in (R / "kanji").glob("*.md")}
    separate, nonmembers = set("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50"), set("\u574a\u7684\u8ab0\u8eab\u962a")
    assert len(published) == 118 and chars - old == published | separate | nonmembers | {CHAR}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    current_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert current_counts == {"kanji": 1115, "words": 5070, "n1Labels": 124, "namedSourceMembersPresent": 129}
    word_name = f"words/{WORD}.md"
    assert {f"words/{p.name}" for p in (R / "words").glob("*.md")
            if CHAR in metadata(R, f"words/{p.name}")["kanji"]} == {word_name}
    assert metadata(R, word_name)["jlpt"] == 3 and metadata(R, word_name)["reading"] == "\u304b\u308b"
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {(CHAR, word_name)}
    for c, word in all_pairs:
        assert f"(../{word})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
        assert f"(../kanji/{c}.md)" in (R / word).read_text(encoding="utf-8")
    guards = {tuple(sorted(pair)) for row in ledger["wordQuizAudit"]["directExclusions"] for pair in row["newPairs"]}
    assert guards == {tuple(sorted((WORD, "\u53ce\u7a6b")))}
    assert metadata(R, word_name)["quiz_exclusions"] == ["\u5207\u308b", "\u53ce\u7a6b"]
    for inbound in ["\u5243\u308b", "\u53d6\u308a\u5165\u308c\u308b"]:
        assert WORD in metadata(R, f"words/{inbound}.md")["quiz_exclusions"]
    assert not [c for c in chars if c != CHAR and CHAR in metadata(R, f"kanji/{c}.md").get("distractors", [])]
    assert len(metadata(R, "kanji/\u5207.md")["distractors"]) == 3
    stroke = load(S / "batch-092-stroke-evidence.json")
    svg = (S / "batch-092-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    assert stroke["dictionaryStrokeCount"] == stroke["sourceStrokePaths"] == 4
    font = load(S / "batch-092-draft-font-audit.json")
    text = "".join((R / n).read_text(encoding="utf-8") for n in font["completeArticleScope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert han == font["actualHan"] and len(han) == 16
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
    assert checked == 8434
    result.update(execution=665, latestMain=MAIN, upstreamAlreadyAncestor=True,
                  runtimeHashesVerified=checked, frozenInputHashesVerified=len(snapshot["inputs"]),
                  decompressedDictionaryHashesVerified=2, packets=packets,
                  completeRawCharacterRecordsVerified=occurrences,
                  originalBaselineMetadataAndStrokesPreserved=counts,
                  baselineMetadataExceptions=prior["baselineMetadataExceptions"],
                  baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
                  exactMembershipAccounted=True, currentCounts=current_counts,
                  publishedIssue60Additions=118, acceptedUnpublishedIssue60Additions=[CHAR],
                  separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
                  requiredAllMappedPairs=1, directedLinksVerified=2, newDirectWordExclusionPairs=1,
                  pinnedStrokeGeometryExactlyRegenerated=True, scopedHan=han, fontProvenanceReverified=True)
    save(L / "combined-source-audit-665.json", result)
    print("Combined sources/baseline/links/readings/fonts/membership and all8434 runtime hashes passed.")


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
        with (L / f"{name}-665.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-665.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-092-reconciliation.json")
    visual = load(V / "batch-092-visual-reconciliation-664.json")
    native = load(S / "execution-663.json")
    assert text["textualReviewClosed"]
    assert text["actionableRemainingTeachingFindings"] == text["consequentialUnresolvedTeachingFindings"] == 0
    assert not text["findings"]
    previous = None
    for label, process in text["processes"].items():
        assert process["actualModels"] == ["claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
        assert process["exitCode"] == 0 and not process["observedToolOverlaps"]
        assert process["allAssignedRangesReturned"] and process["firstCallExactFullPacketReturned"]
        assert sha(V / process["report"]) == process["reportSha256"]
        assert sha(V / f"batch-092-initial-{label}.jsonl") == process["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedInScopeClaims"] == 0
    assert not visual["findings"] and visual["serialReviewerProcessesExited"] and visual["allToolViewsSerial"]
    previous = None
    for label, process in visual["processes"].items():
        assert process["actualModels"] == ["claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
        assert process["exitCode"] == 0 and process["dependentOriginalSession"]
        assert not process["newBlindInitialReviewCredit"] and len(process["toolCalls"]) == 27
        calls = process["toolCalls"]
        for first, second in zip(calls, calls[1:]):
            assert first["completedAt"] <= second["startedAt"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    verified = 0
    for number in [660, 661, 662, 663, 664]:
        evidence = load(S / f"execution-{number}.json")
        for row in evidence.get("artifacts", []) + evidence.get("receipts", []):
            path = R / (row.get("archive") or row["path"])
            assert sha(path) == (row.get("archiveSha256") or row["sha256"]), path
            if row.get("sourceSha256"):
                raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
                assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"], path
            verified += 1
    execution, route = native["executionReceipt"], native["nativeRoute"]
    assert execution["passed"] and execution["terminalSuccessCases"] == 2
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    assert {k: route[k] for k in ["archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "archiveRequests": 1, "importedKanji": 1115, "importedWords": 5070, "n1Cards": 124, "problems": 0}
    assert route["contentVersion"] == VERSION and route["acceptedReadingParserEpoch"] == 1
    assert route["fullOnyomi"] == ["\u30ac\u30a4", "\u30ab\u30a4"] and route["fullKunyomi"] == ["\u304b.\u308b"]
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["\u304b\u308b"]
    assert route["liteQuizOnyomi"] == [] and route["liteQuizKunyomi"] == ["\u304b.\u308b"]
    assert route["onlyKunKaruNoOnPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 4 and route["directWordGuardCount"] == 2
    assert route["mappedReciprocalPairs"] == 1 and route["directedLinkTransitions"] == 2
    assert route["reciprocalLinkAndSystemBack"] and route["offline"]
    for pool in ["N1", "All"]:
        choices = route["productionBuilderN1AndAllExactChoices"][pool]
        assert choices["availableCuratedCount"] == 3 and choices["fallbackOptions"] == 0
        assert {o["kanji"] for o in choices["options"]} == {CHAR, "\u4e43", "\u51f9", "\u51f8"}
    for snapshot in [TEACHING, visual["evidenceSnapshot"], route["contentSnapshot"]]:
        assert not git("diff", snapshot, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for name, expected in text["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    assert not git("diff", PRODUCTION, APP, "--", "core/src/main", "app/src/main", "gradle.properties", root=A)
    return {
        "initialReviewRecord": "docs/n1-reviews/batch-092-reconciliation.json",
        "initialModels": text["initialModels"], "initialReportsAndSerialProcessEvidenceReverified": True,
        "visualReviewRecord": "docs/n1-reviews/batch-092-visual-reconciliation-664.json",
        "nativeRecord": "docs/n1-sources/execution-663.json", "nativeRoute": route,
        "nativeTerminalCaseStatuses": [0, 0], "receiptHashesReverified": verified,
        "nativeRuntimeMatchesCurrentCombinedTree": True, "newNativeOrReviewerRuns": 0,
        "originalLimits": {"textual660": text["limits"], "native663": native["visualInspection"]["limits"],
                           "visual664": visual["limits"]},
        "rerunDisposition": "No new concern; reviewed runtime, production app and fonts unchanged. Inherited source/linguistic/native/rendered evidence within its exact recorded scope, NOT fresh review or native run.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-665.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-665.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    assert VERSION in (L / "manifest-665.txt").read_text(encoding="utf-8")
    vocabulary = (L / "vocabulary-665.txt").read_text(encoding="utf-8").strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-665.json")["exitCode"] == 0
    assert (L / "host-exit-665.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-665.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-665.txt").read_text(encoding="utf-8-sig").strip())
    ended = datetime.fromisoformat((L / "host-end-665.txt").read_text(encoding="utf-8-sig").strip())
    suites = []
    for module, task, names in [
        ("core", "test", {"parsesRealContentRepoWhenPresent",
                         "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
                         "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent"}),
        ("app", "testDebugUnitTest", {"contentRareCharactersAreCoveredByBundledFont"}),
    ]:
        cls = "RealContentTest" if module == "core" else "RareHanTest"
        path = A / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{cls}.xml"
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
    source, inheritance = load(L / "combined-source-audit-665.json"), inherited()
    budget = ast.literal_eval((L / "budget-665.txt").read_text(encoding="utf-8"))
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    assert not D.exists()
    D.mkdir()
    receipts = []
    paths = [
        *(L / name for name in ["starting-state-665.json", "combined-source-audit-665.json", "merge-665.txt",
          "python-tests-665.txt", "validate-665.txt", "manifest-665.txt", "vocabulary-665.txt", "budget-665.txt",
          "host-665.txt", "host-exit-665.txt", "host-command-665.json", "host-start-665.txt", "host-end-665.txt"]),
        *(L / f"{name}-exit-665.json" for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-092-host-665.ps1",
        C / "post-batch-092-665.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
        A / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "RealContentTest.kt",
        A / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "PublishableContentFixture.kt",
        A / "app" / "src" / "test" / "java" / "io" / "github" / "stopcran" / "kanji" / "core" / "RareHanTest.kt",
    ]
    for path in paths:
        target = D / (path.name + ".gz" if path.suffix == ".txt" else path.name)
        assert not target.exists(), target
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "sha256": sha(target), "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 665, "batch": "092", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-665.json"), "combinedContentHead": HEAD,
        "latestMainIntegrated": MAIN, "normalMerge": True, "mergeResult": "Already up to date.",
        "newMergeCommit": False, "conflicts": [], "substantiveTeachingConflictEdits": [],
        "runtimeBytesUnchanged": True, "sourceAudit": source, "pythonTestsPassed": int(match[1]),
        "validatorErrors": 0, "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary,
        "manifestFresh": True, "contentVersion": VERSION, "localBudget": budget, "hostSuites": suites,
        "hostChecksFresh": True, "hostTestsExecuted": 4, "androidHead": APP,
        "unchangedProductionAndroid": PRODUCTION, "qualifiedTestOnlyAndroid": True,
        "inheritedAcceptance": inheritance, "receipts": receipts, "runtimeAccepted": True,
        "runtimePublished": False, "publishedAdditions": 118, "remainingAdditions": 1110,
        "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Local combined-tree acceptance only, not public delivery or fresh native/linguistic review. Vocabulary2122/2431 pilot consistency not full coverage. All original source/read/fontface/Paintprobe/injectedtrace/no successfulMLKit/phone limitations retained. Qualified test-only Android not latestappmain. CI/publicZIP/publication/physicalphone/generalrelease/whole-set remain outstanding.",
    }
    save(S / "execution-665.json", evidence)
    path = S / "batch-092-progress.json"
    ledger = load(path)
    ledger["preCombined665State"] = {
        k: ledger.get(k) for k in ["status", "nextAction", "reviewClosed", "runtimeAccepted",
                                  "runtimePublished", "pendingGates", "limits"]}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True,
                  runtimePublished=False, combinedAcceptance="docs/n1-sources/execution-665.json", nextAction=NEXT)
    ledger["pendingGates"] = [
        "Fresh-main recheck before normal signed owner fast-forward publication; merge/reconcile/regenerate/revalidate and independently review substantive teaching changes if main advances.",
        "Exact remote SHA, terminal green relevant CI, EVERY immutable public ZIP runtime entry/hash, manifest equality and unchanged entry/compressed/inflated/retained/per-file/path/media budgets; durable publication ledger and verified owner issue receipt before093.",
        "Physical-phone/general-release and whole-set acceptance remain explicitly outstanding.",
    ]
    ledger["limits"][0] = "Local combined-tree acceptance passed665; original two-family textual660/native663/dependent visual664 evidence inherited, NOT rerun. No public delivery claimed."
    ledger["limits"][4] = "Tested N1 and All production pools each provide all three curated wrong labels without fallback; not every custom pool or older client. One new direct word guard preserves the original exclusion."
    ledger["limits"][5] = "All16 scopedHan readable in three Compose panels/four production fonts;25of42 PNGs inspected,17 not separately viewed.64individual+4wholewordPaint probes are not68 viewed PNGs or identified fallbackface. Tool resized900x2000; word body heading not separately pictured. Injectedtrace/recallgiveup is not humanhandwriting/successfulMLKit/phone."
    ledger["nativeAcceptance"] = "docs/n1-sources/execution-663.json"
    ledger["visualAcceptance"] = "docs/n1-reviews/batch-092-visual-reconciliation-664.json"
    ledger["combinedHostAcceptance"] = {"evidence": "docs/n1-sources/execution-665.json",
                                        "tests": 4, "skipped": 0}
    save(path, ledger, ensure_ascii=False)
    body = (
        "**Batch 092 checkpoint 665: combined current-main acceptance passed locally; publication next.** "
        f"Fresh main `{MAIN}` is already an ancestor of reviewed `{HEAD}`; normal non-rewriting merge "
        "returned Already up to date. No teaching/runtime edit or substantive conflict.\n\n"
        f"Fresh {match[1]} Python tests, validator 0 errors, vocabulary consistency "
        f"(`{vocabulary}`), regenerated manifest/version `{VERSION}` and all 8,434 payload hashes passed. "
        "Frozen input/decompressed dictionary hashes, 75 complete lexical families/six raw character records, "
        "original 985 kanji/4,942 words/985 strokes with recorded narrow exceptions, exact membership, "
        "all three raw readings, only kun かる/no on, one all-mapped baseline pair/two links, "
        "one new direct word guard preserving original 切る, pinned four-stroke regeneration and "
        "all16-Han font provenance passed. Actual 1,115 kanji/5,070 words/124 N1 labels/"
        "129 named-source members. Existing N3 刈る identity/reading/title/level preserved; no new support.\n\n"
        "Fresh actual-sibling RealContentTest THREE and RareHanTest ONE passed, zero skips/errors/failures. "
        "Explicit JDK17/SDK/one worker/in-process Kotlin/existing approved 2GiB HOST-only init; no guest/app "
        "heap or guard change. Qualified TEST-ONLY Android `1c1b7bf4` retains production `f9b59a2`, "
        "NOT latest app main.\n\n"
        "Original two-family textual660 reviews and original-session serial visual664 confirmations "
        "reverified, NOT rerun or new blind credit. Native663 TWO terminal cases0/no skips: full archive "
        "62c6d3e2 through production ContentSync ONCE, 1,115 kanji/5,070 words/124 N1/zero problems/"
        "current version/Room epoch1. N1 and All exact three curated wrong cards/no fallback, only kun "
        "かる persisted Good/Done/no on/raw full+Lite order, drawing/articles/SystemBack/offline passed. "
        "All16 Han including fallback 刂 readable in three Compose panels/four production fonts. "
        "25 of42 original PNGs viewed,17 not separately viewed; tool resized900x2000; word body heading "
        "not separately pictured remains explicit reviewer limit. 64 individual+4 wholeword Paint probes "
        "are NOT68 viewed PNGs or identified fallback face. Injected trace/recall give-up is NOT human "
        "handwriting/successful MLKit/physical phone; UI explicitly reports model unavailable/shape-only. "
        "All original source/read/phone limits retained.\n\n"
        f"Local budget: {budget['entries']:,} entries / {budget['retainedBytes']:,} retained / "
        f"{budget['inflatedBytes']:,} inflated / {budget['localZipBytes']:,} compressed bytes. "
        "Original18,000-entry/42MiB compressed/80MiB inflated/56MiB retained and per-file/media/path guards "
        "unchanged. Evidence: `docs/n1-sources/execution-665.json` and "
        "`docs/n1-reviews/batch-092-combined-acceptance-665`.\n\n"
        "**Next bounded checkpoint: fresh-main recheck, normal signed owner fast-forward publication, "
        "exact remote SHA, terminal green CI and EVERY immutable public ZIP runtime hash/budget, durable "
        "publication and owner issue receipt before batch093.** No push or next batch here. "
        "Published118/1,228;1,110 remaining unchanged. Compatible f9b59a2+ required; physical-phone/"
        "general-release/whole-set acceptance outstanding. Live parent19008/session/decoded launcher "
        "verified; runner.lock untouched. No optional historical-session helper or new permission denial.\n"
    )
    (L / "issue-body-665.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance and lossless evidence archived; ready for normal signed LOCAL checkpoint.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-665.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["sha256"]
        raw = (R / row["archive"]).read_bytes()
        if row["losslessGzip"]:
            raw = gzip.decompress(raw)
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    receipt = load(L / "issue-verified-665.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (L / "issue-body-665.txt").read_bytes().decode("utf-8")
    before, p = load(L / "progress-before-665.json"), load(C / "progress.json")
    row = {
        "schemaVersion": 1, "execution": 665, "checkpoint": 665, "batch": "092",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-665.json", "evidenceSha256": sha(S / "execution-665.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "runtimeHashesVerified": 8434,
        "contentVersion": VERSION, "pythonTestsPassed": evidence["pythonTestsPassed"],
        "freshHostTestsPassed": 4, "hostSkips": 0, "runtimeAccepted": True, "runtimePublished": False,
        "runtimeBytesUnchanged": True, "freshNativeOrReviewerRuns": 0,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 118, "remainingAdditions": 1110, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    p["execution665StartingState"]["status"] = "signed-local-combined-acceptance-checkpoint-complete"
    p["execution665CoordinatorCheckpoint"] = row
    p["batch092CombinedAcceptanceCheckpoint"] = row
    p.update(checkpoint=665, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in allowed)
    save(C / "progress.json", p)
    actual = load(C / "progress.json")
    assert all(actual[k] == value for k, value in before.items() if k not in allowed)
    save(L / "checkpoint-665.json", row)
    print(json.dumps({"checkpoint": 665, "commit": saved, "status": "continue", "issue": receipt["html_url"]}))


if __name__ == "__main__":
    {"start": start, "checks": checks, "audit": audit, "record": record, "finish": finish}[sys.argv[1]]()
