"""Bounded combined-tree acceptance under the live parent runner's lock."""
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
L = C / "logs" / "093e51d3-f820-418a-81a4-d23c4fbab3f1"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-093-combined-acceptance-674"
HEAD = "9066dd9a55d024bcf22a19ff55e9c9627128e991"
MAIN = "fe9e1a37acddae69a3b131bdf2ea01f9ca8cd2f4"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "27663944c7217a19e7de2f363e1b31a5f13452b6"
VERSION = "bf4cc85592bb9727"
CHAR, WORD = "\u5211", "\u5211\u4e8b"
STAGE = "batch-093-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME093 bounded normal signed owner fast-forward publication and exact public acceptance next; "
    "no094 until verified delivery. Read docs/n1-sources/execution-674.json and "
    "docs/n1-reviews/batch-093-combined-acceptance-674. Fresh origin/main fe9e1a37 already "
    "ancestor of reviewed9066dd9a; normal nonrewriting merge Already up to date; no substantive "
    "teaching or runtime change. Fresh full Python/validator/vocabulary consistency/regenerated "
    "manifest/budget/source membership/full baseline/all180families/eightcharacterrecords/"
    "allrawreadings/onlyonKei-nokun/TWOallmappedpairs-FOURdirections-ONEactivatedbaselinepair/"
    "fourDIRECTpoliceguards/pinnedSIXstrokes/46Han-fontprovenance/all8436runtimehashes and "
    "sibling RealContentTestTHREE+RareHanTestONE zero skips recorded. Original669 blind "
    "Claude/GPT textual reviews,672native and673 original-session serial dependent visual "
    "confirmations inherited with COMPLETE reports, corrections, optional dispositions and "
    "readlimits, NOT rerun/newblindcredit/independentupstream/equalcomprehension. Native672 "
    "TWOterminalcase0/noskips/fullarchive324b0bd9 through productionContentSyncONCE/"
    "1116kanji5070words125N1zeroProblems/versionbf4cc85592bb9727/RoomreadingEpoch1; "
    "onlyonKei persistedGoodDone/nokun/fullLiteagreement; N1+All all3curatedwrongcards/"
    "zerofallback/twoallmappedpairs/fourdirections/SystemBack/offline. All46Han across "
    "FIVEComposepanels/FOURproductionfonts readable including fallback U+4E85/U+5202/U+5F61. "
    "Eachreviewer32of63originalPNGsviewed/31notseparatelyviewed/25distinctsourcehashes; "
    "toolresizing/exactduplicates and fulltext/native-scrollassertion dependence retained. "
    "184individual+12wholewordPaintprobes NOT196viewedPNGs/identifiedfallbackface. "
    "Injectedtrace/recallgiveup NOT humanhandwriting/successfulMLKit/phone; actualUI "
    "modelunavailable/shapeonly. Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOTlatestappmain. Freshmain/exactsignedheads/whollyclean before publication; if main "
    "advanced normalmerge/reconcile/regenerate/revalidate ACTUALcombinedtree and independently "
    "review substantive teaching changes. Normal ownerstop-cran token ONLY publicationchild, "
    "no global auth switch; normal fastforward, exactremoteSHA, terminalgreen relevantCI, "
    "EVERYimmutablepublicZIP runtimeentryhash/manifest equality/original18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath guards; persist authored/"
    "reviewed/integrated/publishedSHAs and verifiedownerissue60 receipt before094. No forcepush/"
    "amend/signingbypass/heapguardincrease/productionappchange/redundantnative/reviewer. "
    "Parent19008 ownsrunner.lock: verify liveancestry/decodedlauncher/exactcurrentrunnersession/"
    "checkpoint/signedheads/whollyclean; NEVERchildacquire/delete/unlock. Approvedcontrol/"
    "committedsources/frozenworkspaceinputs only, no optional historicalsessionhelpers. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Published119/1228 "
    "and1109remaining unchanged pending delivery; compatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding, projectincomplete. No094/secondrunner."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".674.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
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
    progress = load(C / "progress.json")
    assert (progress["checkpoint"], progress["batch"], progress["status"]) == (673, "093", "continue")
    return ancestry


def start():
    ancestry = context()
    clean(R, HEAD)
    assert not (L / "progress-before-674.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-674.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["batch093VisualAcceptanceCheckpoint"]["savedCommit"] == HEAD
    state = {
        "execution": 674, "batch": "093", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME093 combined-current-main acceptance and normally signed LOCAL evidence only; publication next, no094/newnative/reviewer.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete issue and final673 directly inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial scalar printing hit cp1252 after successful full parse; UTF-8 bounded output recovered."},
        "runnerLockRole": {"parentPid": 19008, "session": L.name, "ancestry": ancestry,
                           "parentLockTouched": False},
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-674.json", state)
    progress = load(C / "progress.json")
    progress["execution674StartingState"] = state
    progress.update(stage="batch-093-combined-main-acceptance-in-progress",
                    nextAction=state["scope"], blocker=None)
    save(C / "progress.json", progress)
    before = load(L / "progress-before-674.json")
    assert all(progress[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    print("SAME093 combined acceptance scope persisted; original history preserved; parent lock untouched.")


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
    result = batch_audit(R, "093")
    ledger, prior = load(S / "batch-093-progress.json"), load(S / "batch-093-draft-audit.json")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(gzip.decompress(jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    packets = []
    for index, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        expected = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt.gz" if index == 0 else "comparison-full-family-reading.txt.gz"
        compact = gzip.decompress((S / f"batch-093-{suffix}").read_bytes())
        assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact.decode("utf-8") + "</JMdict>")] == [
            canonical(e) for e in ET.fromstring(expected)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(S / packet["xml"]),
                        "freshFrozenExtractionMatches": True, "completeCompactSemanticEquality": True})
    assert sum(p["families"] for p in packets) == 180
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    occurrences = 0
    for name in ["batch-093-kanjidic2.xml", "batch-093-comparison-kanjidic2.xml"]:
        for row in ET.parse(S / name).getroot().findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            occurrences += 1
    assert occurrences == 8
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
    assert len(published) == 119 and chars - old == published | separate | nonmembers | {CHAR}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    current_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert current_counts == {"kanji": 1116, "words": 5070, "n1Labels": 125, "namedSourceMembersPresent": 130}
    word_name = f"words/{WORD}.md"
    assert {f"words/{p.name}" for p in (R / "words").glob("*.md")
            if CHAR in metadata(R, f"words/{p.name}")["kanji"]} == {word_name}
    assert metadata(R, word_name)["jlpt"] == 3 and metadata(R, word_name)["reading"] == "\u3051\u3044\u3058"
    pairs = {(c, row["article"]) for row in ledger["supportMappings"]
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {
        (CHAR, word_name), ("\u4e8b", word_name)}
    for c, word in pairs:
        assert f"(../{word})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
        assert f"(../kanji/{c}.md)" in (R / word).read_text(encoding="utf-8")
    guards = {tuple(sorted(pair)) for row in ledger["wordQuizAudit"]["directExclusions"] for pair in row["newPairs"]}
    police = ["\u8b66\u5b98", "\u8b66\u5bdf", "\u5de1\u67fb", "\u304a\u307e\u308f\u308a\u3055\u3093"]
    assert guards == {tuple(sorted((WORD, p))) for p in police}
    assert metadata(R, word_name)["quiz_exclusions"] == police
    assert WORD in metadata(R, "words/\u63a2\u5075.md")["quiz_exclusions"]
    assert not [c for c in chars if c != CHAR and CHAR in metadata(R, f"kanji/{c}.md").get("distractors", [])]
    stroke = load(S / "batch-093-stroke-evidence.json")
    svg = (S / "batch-093-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    assert stroke["dictionaryStrokeCount"] == stroke["sourceStrokePaths"] == 6
    font = load(S / "batch-093-draft-font-audit.json")
    text = "".join((R / n).read_text(encoding="utf-8") for n in font["completeArticleScope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert han == font["actualHan"] and len(han) == 46
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
    assert checked == 8436
    result.update(execution=674, latestMain=MAIN, upstreamAlreadyAncestor=True,
                  runtimeHashesVerified=checked, frozenInputHashesVerified=len(snapshot["inputs"]),
                  decompressedDictionaryHashesVerified=2, packets=packets,
                  completeRawCharacterRecordsVerified=occurrences,
                  originalBaselineMetadataAndStrokesPreserved=counts,
                  baselineMetadataExceptions=prior["baselineMetadataExceptions"],
                  baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
                  exactMembershipAccounted=True, currentCounts=current_counts,
                  publishedIssue60Additions=119, acceptedUnpublishedIssue60Additions=[CHAR],
                  separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
                  requiredAllMappedPairs=2, directedLinksVerified=4, newDirectWordExclusionPairs=4,
                  pinnedStrokeGeometryExactlyRegenerated=True, scopedHan=han, fontProvenanceReverified=True)
    save(L / "combined-source-audit-674.json", result)
    print("Combined sources/baseline/links/readings/fonts/membership and all8436 runtime hashes passed.")


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
        with (L / f"{name}-674.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-674.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-093-reconciliation.json")
    visual = load(V / "batch-093-visual-reconciliation-673.json")
    native = load(S / "execution-672.json")
    assert text["textualReviewClosed"]
    assert text["actionableRemainingTeachingFindings"] == text["consequentialUnresolvedTeachingFindings"] == 0
    assert not text["findings"]
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedInScopeClaims"] == 0
    assert not visual["findings"] and visual["serialReviewerProcessesExited"] and visual["allToolViewsSerial"]
    for record, dependent in [(text, False), (visual, True)]:
        previous = None
        for label, process in record["processes"].items():
            assert process["actualModels"] == ["claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
            assert process["exitCode"] == 0 and not process["observedToolOverlaps"]
            if dependent:
                assert process["dependentOriginalSession"] and not process["newBlindInitialReviewCredit"]
                assert len(process["toolCalls"]) == 34 and process["allAssignedResourcesSuccessfullyReturned"]
                assert process["sessionId"] == text["processes"][label]["sessionId"]
                assert sha(V / f"batch-093-visual-673-{label}.md") == process["reportSha256"]
                raw = gzip.decompress((V / f"batch-093-visual-673-{label}.jsonl.gz").read_bytes())
                assert hashlib.sha256(raw).hexdigest() == process["rawSha256"]
                for first, second in zip(process["toolCalls"], process["toolCalls"][1:]):
                    assert first["completedAt"] <= second["startedAt"]
            else:
                assert process["allAssignedRangesReturned"] and process["firstCallExactFullPacketReturned"]
                assert sha(V / process["report"]) == process["reportSha256"]
                assert sha(V / f"batch-093-initial-{label}.jsonl") == process["rawExecutionSha256"]
            if previous:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
            previous = process["completedAt"]
    verified = 0
    for number in [669, 670, 671, 672, 673]:
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
    instrumentation = (V / "batch-093-native" / "execution-672" / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert instrumentation.count("INSTRUMENTATION_STATUS_CODE: 0") == 2
    assert "OK (2 tests)" in instrumentation and "FAILURES" not in instrumentation
    assert {k: route[k] for k in ["archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "archiveRequests": 1, "importedKanji": 1116, "importedWords": 5070, "n1Cards": 125, "problems": 0}
    assert route["contentVersion"] == VERSION and route["acceptedReadingParserEpoch"] == 1
    assert route["fullOnyomi"] == ["\u30b1\u30a4"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["\u3051\u3044"] and route["quizKunKeys"] == []
    assert route["liteQuizOnyomi"] == ["\u30b1\u30a4"] and route["liteQuizKunyomi"] == []
    assert route["onlyOnKeiNoKunPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 6 and route["directWordGuardCount"] == 4
    assert route["inboundTanteiGuardPreserved"]
    assert route["mappedReciprocalPairs"] == 2 and route["directedLinkTransitions"] == 4
    assert route["activatedBaselinePairs"] == 1 and route["completeArticleProjections"] == 3
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
        "initialReviewRecord": "docs/n1-reviews/batch-093-reconciliation.json",
        "initialModels": text["initialModels"], "initialReportsAndSerialProcessEvidenceReverified": True,
        "visualReviewRecord": "docs/n1-reviews/batch-093-visual-reconciliation-673.json",
        "nativeRecord": "docs/n1-sources/execution-672.json", "nativeRoute": route,
        "nativeTerminalCaseStatuses": [0, 0], "receiptHashesReverified": verified,
        "nativeRuntimeMatchesCurrentCombinedTree": True, "newNativeOrReviewerRuns": 0,
        "originalLimits": {"textual669": text["limits"], "native672": native["visualInspection"]["limits"],
                           "visual673": visual["limits"]},
        "dispositions": visual["dispositions"],
        "rerunDisposition": "No new concern; reviewed runtime, production app and fonts unchanged. Evidence inherited within original scope, NOT fresh linguistic review or native run.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-674.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-674.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    assert VERSION in (L / "manifest-674.txt").read_text(encoding="utf-8")
    vocabulary = (L / "vocabulary-674.txt").read_text(encoding="utf-8").strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-674.json")["exitCode"] == 0
    assert (L / "host-exit-674.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-674.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-674.txt").read_text(encoding="utf-8-sig").strip())
    ended = datetime.fromisoformat((L / "host-end-674.txt").read_text(encoding="utf-8-sig").strip())
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
    source, inheritance = load(L / "combined-source-audit-674.json"), inherited()
    budget = ast.literal_eval((L / "budget-674.txt").read_text(encoding="utf-8"))
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    assert not D.exists()
    D.mkdir()
    receipts = []
    paths = [
        *(L / name for name in ["starting-state-674.json", "combined-source-audit-674.json", "merge-674.txt",
          "python-tests-674.txt", "validate-674.txt", "manifest-674.txt", "vocabulary-674.txt", "budget-674.txt",
          "host-674.txt", "host-exit-674.txt", "host-command-674.json", "host-start-674.txt", "host-end-674.txt"]),
        *(L / f"{name}-exit-674.json" for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-093-host-674.ps1",
        C / "post-batch-093-674.ps1", C / "batch-065-host-integration-heap.init.gradle",
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
        "schemaVersion": 1, "execution": 674, "batch": "093", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-674.json"), "combinedContentHead": HEAD,
        "latestMainIntegrated": MAIN, "normalMerge": True, "mergeResult": "Already up to date.",
        "newMergeCommit": False, "conflicts": [], "substantiveTeachingConflictEdits": [],
        "runtimeBytesUnchanged": True, "sourceAudit": source, "pythonTestsPassed": int(match[1]),
        "validatorErrors": 0, "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary,
        "manifestFresh": True, "contentVersion": VERSION, "localBudget": budget, "hostSuites": suites,
        "hostChecksFresh": True, "hostTestsExecuted": 4, "androidHead": APP,
        "unchangedProductionAndroid": PRODUCTION, "qualifiedTestOnlyAndroid": True,
        "inheritedAcceptance": inheritance, "receipts": receipts, "runtimeAccepted": True,
        "runtimePublished": False, "publishedAdditions": 119, "remainingAdditions": 1109,
        "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Local combined-tree acceptance only, not public delivery or fresh native/linguistic review. Vocabulary2122/2431 pilot consistency not full coverage. Original source/read/fallbackface/Paintprobe/injectedtrace/no successfulMLKit/phone limitations retained, including32of63originalPNGs/31notseparatelyviewed/fulltext-native-scroll dependence. Qualified test-only Android not latestappmain. CI/publicZIP/publication/physicalphone/generalrelease/whole-set remain outstanding.",
    }
    save(S / "execution-674.json", evidence)
    path = S / "batch-093-progress.json"
    ledger = load(path)
    ledger["preCombined674State"] = {
        k: ledger.get(k) for k in ["status", "nextAction", "reviewClosed", "runtimeAccepted",
                                  "runtimePublished", "pendingGates", "limits"]}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True,
                  runtimePublished=False, combinedAcceptance="docs/n1-sources/execution-674.json", nextAction=NEXT)
    ledger["pendingGates"] = [
        "Fresh-main recheck before normal signed owner fast-forward publication; merge/reconcile/regenerate/revalidate and independently review substantive teaching changes if main advances.",
        "Exact remote SHA, terminal green relevant CI, EVERY immutable public ZIP runtime entry/hash, manifest equality and unchanged entry/compressed/inflated/retained/per-file/path/media budgets; durable publication ledger and verified owner issue receipt before094.",
        "Physical-phone/general-release and whole-set acceptance remain explicitly outstanding.",
    ]
    ledger["limits"] = [
        "Local combined-tree acceptance passed674. Original669two-family textual,672native and673dependent visual evidence inherited, NOT rerun or new blind credit. No public delivery claimed.",
        *inheritance["originalLimits"]["visual673"],
        "Fresh combined674tests/source/baseline/hash/fontprovenance checks do not certify new linguistic comprehension. All original textual669/native672 source/read/process limitations retained in execution674.",
    ]
    ledger["nativeAcceptance"] = "docs/n1-sources/execution-672.json"
    ledger["visualAcceptance"] = "docs/n1-reviews/batch-093-visual-reconciliation-673.json"
    ledger["combinedHostAcceptance"] = {"evidence": "docs/n1-sources/execution-674.json", "tests": 4, "skipped": 0}
    save(path, ledger)
    body = (
        "**Batch093 checkpoint674: combined current-main acceptance passed locally; publication next.** "
        f"Fresh main `{MAIN}` is already an ancestor of reviewed `{HEAD}`; normal non-rewriting merge "
        "returned Already up to date. No teaching/runtime edit or substantive conflict.\n\n"
        f"Fresh {match[1]} Python tests, validator0 errors, vocabulary consistency "
        f"(`{vocabulary}`), regenerated manifest/version `{VERSION}` and all8,436 payload hashes passed. "
        "Frozen input/decompressed dictionary hashes,180complete lexical families/eight raw character records, "
        "original985kanji/4,942words/985strokes with recorded narrow exceptions, exact membership, "
        "full raw onケイ/emptykun/explicit[ケイ]/[], onlyけいoffered, TWOall-mapped pairs/FOURdirections/"
        "ONEactivated baseline刑/刑事pair, FOURdirect police-label guards preserving inbound探偵, "
        "pinnedSIXstroke regeneration and46Han font provenance passed. Actual1,116kanji/5,070words/"
        "125N1labels/130named-source members. Existing N3刑事 identity/reading/title/level preserved; "
        "only component link/four safeguards; 事 reciprocal-navigation only; no new support word. "
        "Wholewordでか is not constituentkun; publicギョウ remains outside frozen metadata.\n\n"
        "Fresh actual-sibling RealContentTestTHREE and RareHanTestONE passed, zero skips/errors/failures. "
        "Explicit JDK17/SDK/one worker/in-process Kotlin/existing approved2GiB HOST-only init; no guest/app "
        "heap or guard change. Qualified TEST-ONLY Android `1c1b7bf4` retains production `f9b59a2`, "
        "NOT latest appmain.\n\n"
        "Original two-family textual669 reviews and original-session serial visual673 confirmations "
        "reverified, NOT rerun/new blind credit/independent upstream retrieval/equal comprehension. "
        "Native672 TWOterminal cases0/no skips: fullarchive324b0bd9 through productionContentSyncONCE, "
        "1,116kanji/5,070words/125N1/zeroProblems/currentversion/RoomreadingEpoch1. N1+All exactthree "
        "curatedwrongcards/no fallback; onlyonけい persistedGood/Done/nokun/fullLiteagreement, "
        "drawing/articles/SystemBack/offline passed. All46Han including fallback亅/刂/彡 readable "
        "in FIVEComposepanels/FOURproductionfonts. Eachreviewer32of63originalPNGs viewed,31not "
        "separatelyviewed/25distinctsourcehashes; toolresizing/exactduplicates/fulltext-native-scroll "
        "dependence retained.184individual+12wholewordPaintprobes NOT196viewedPNGs/identifiedfallbackface. "
        "Injectedtrace/recallgiveup NOT humanhandwriting/successfulMLKit/phone; UIexplicitly "
        "modelunavailable/shapeonly. All original source/read/phone limits and optional dispositions retained.\n\n"
        f"Localbudget: {budget['entries']:,}entries / {budget['retainedBytes']:,}retained / "
        f"{budget['inflatedBytes']:,}inflated / {budget['localZipBytes']:,}compressed bytes. "
        "Original18,000entries/42MiBcompressed/80MiBinflated/56MiBretained/per-file/media/path guards "
        "unchanged. Evidence: `docs/n1-sources/execution-674.json` and "
        "`docs/n1-reviews/batch-093-combined-acceptance-674`.\n\n"
        "**Next bounded checkpoint: fresh-main recheck, normal signed owner fast-forward publication, "
        "exactremoteSHA/terminalgreenCI/EVERYimmutablepublicZIP runtimehash/budget, durablepublication/"
        "verifiedownerissue before094.** No push or nextbatch here. Published119/1,228;1,109remaining "
        "unchanged. Compatiblef9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
        "Liveparent19008/session/decodedlauncher verified; runner.lock untouched. "
        "No optional historical-sessionhelper access or new permission denial.\n"
    )
    (L / "issue-body-674.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance and lossless evidence archived; ready for normal signed LOCAL checkpoint.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-674.json")
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["sha256"]
        raw = gzip.decompress(path.read_bytes()) if row["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    receipt = load(L / "issue-verified-674.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (L / "issue-body-674.txt").read_bytes().decode("utf-8")
    before, progress = load(L / "progress-before-674.json"), load(C / "progress.json")
    row = {
        "schemaVersion": 1, "execution": 674, "checkpoint": 674, "batch": "093",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-674.json", "evidenceSha256": sha(S / "execution-674.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "runtimeHashesVerified": 8436,
        "contentVersion": VERSION, "pythonTestsPassed": evidence["pythonTestsPassed"],
        "freshHostTestsPassed": 4, "hostSkips": 0, "runtimeAccepted": True, "runtimePublished": False,
        "runtimeBytesUnchanged": True, "freshNativeOrReviewerRuns": 0,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 119, "remainingAdditions": 1109, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    progress["execution674StartingState"]["status"] = "signed-local-combined-acceptance-checkpoint-complete"
    progress["execution674CoordinatorCheckpoint"] = row
    progress["batch093CombinedAcceptanceCheckpoint"] = row
    progress.update(checkpoint=674, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[k] == value for k, value in before.items() if k not in allowed)
    save(C / "progress.json", progress)
    actual = load(C / "progress.json")
    assert all(actual[k] == value for k, value in before.items() if k not in allowed)
    save(L / "checkpoint-674.json", row)
    print(json.dumps({"checkpoint": 674, "commit": saved, "status": "continue", "issue": receipt["html_url"]}))


if __name__ == "__main__":
    {"start": start, "checks": checks, "audit": audit, "record": record, "finish": finish}[sys.argv[1]]()
