"""Batch091 combined acceptance under the live parent launcher's lock."""
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
L = C / "logs" / "bf2bf78f-2a42-401f-8d4b-e4c00a084073"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-091-combined-acceptance-656"
HEAD = "27c1019a6dc9849061cddac2959560308fadc525"
MAIN = "7100a3873282b54515b9ef130766e77cf151a47b"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "bfe65483a821fc13"
STAGE = "batch-091-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME091 only: read docs/n1-sources/execution-656.json and "
    "docs/n1-reviews/batch-091-combined-acceptance-656. Combined current-main acceptance "
    "passed at signed27c1019a against freshly fetched main7100a387, already an ancestor; "
    "normal nonrewriting merge Already up to date, no substantive teaching change. "
    "Fresh fullPython/validator/vocabulary consistency/regenerated manifest/budget/"
    "frozen source/full baseline/exact membership/all5readings/one curatedkunha/noon/"
    "one allmappedpair/two directions/five directwordguards/pinned3strokes/current20Han/"
    "inherited21Han fontprovenance/"
    "all8432runtimehashes and sibling RealContentTest3+RareHanTest1 zero skips recorded. "
    "Original647 two-family blind textual reviews and corrections,653 mnemonic confirmations, "
    "654 revised fullarchive ContentSyncONCE/one terminalcase0/zeroProblems/Roomepoch1/"
    "versionbfe65483a821fc13/1114kanji5070words123N1 and655 serial original-session "
    "NEW native paragraph PNG confirmations inherited NOT rerun. GlyphTest650 evidence "
    "retained, not a fresh654/656 glyph test. V1 resolved; GPT initial non-discovery and "
    "rejected Claude651 internal overlap retained. All original source/read/process/native/"
    "fontface/Paintprobe/injectedtrace/no successfulMLKit/phone limits remain. "
    "Qualified test-onlyAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. "
    "Next bounded checkpoint normal signed owner fastforward publication and exact public "
    "acceptance: recheck fresh main, normally merge/reconcile/regenerate/revalidate if advanced; "
    "independently review substantive teaching changes. No amend/forcepush/signing bypass/"
    "global auth switch. Ownerstop-cran token only in publication child; verify exact remoteSHA/"
    "terminal green relevantCI/EVERY immutable GitHubZIP runtime entryhash and manifest equality/"
    "unchanged18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath guards. "
    "Persist authored/reviewed/integrated/publishedSHAs, ledgers and verifiedownerissue60 "
    "receipt before092. Published117/1228,1111remaining unchanged until verified delivery. "
    "Physicalphone/generalrelease/whole-set outstanding. Parent19008 ownsrunner.lock: "
    "verify live ancestry/decodedlauncher/exact currentrunnersession/checkpoint/signedheads/"
    "whollyclean; NEVER childacquire/delete/unlock. Approvedcontrol/committed evidence/frozen "
    "workspaceinputs only, no optionalhistoricalsessionhelpers. Preserve/report/yield actual "
    "newdenial/signinghang/uncertainownership. No092/newrunner or redundant native/reviewer."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".656.tmp")
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
    return ancestry


def start():
    ancestry = context()
    clean(R, HEAD)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (655, "091", "continue")
    assert p["stage"] == "revised-rendering-confirmed-awaiting-combined-current-main-acceptance"
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution655CoordinatorCheckpoint"]["savedCommit"] == HEAD
    assert not (L / "progress-before-656.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-656.json")
    state = {
        "execution": 656, "batch": "091", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME091 combined-current-main acceptance and signed LOCAL evidence checkpoint; publication next, no092/newnative/reviewer.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete issue and final655 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": {"parentPid": 19008, "session": L.name, "ancestry": ancestry,
                           "parentLockTouched": False},
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-656.json", state)
    p["execution656StartingState"] = state
    p.update(stage="batch-091-combined-main-acceptance-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-656.json")
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    print("Starting scope persisted; complete historical root values preserved; parent lock untouched.")


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
    result = batch_audit(R, "091")
    ledger, prior = load(S / "batch-091-progress.json"), load(S / "batch-091-draft-audit.json")
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
    assert sum(p["families"] for p in packets) == 78
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    occurrences = 0
    for name in ["batch-091-kanjidic2.xml", "batch-091-comparison-kanjidic2.xml"]:
        for row in ET.parse(S / name).getroot().findall("character"):
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
    published = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    chars = {path.stem for path in (R / "kanji").glob("*.md")}
    separate, nonmembers, target = set("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50"), set("\u574a\u7684\u8ab0\u8eab\u962a"), "\u5203"
    assert len(published) == 117 and chars - old == published | separate | nonmembers | {target}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    actual_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert actual_counts == {"kanji": 1114, "words": 5070, "n1Labels": 123, "namedSourceMembersPresent": 128}
    assert {f"words/{p.name}" for p in (R / "words").glob("*.md")
            if target in metadata(R, f"words/{p.name}")["kanji"]} == {f"words/{target}.md"}
    assert "jlpt" not in metadata(R, f"words/{target}.md")
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(all_pairs) == 1
    for c, word in all_pairs:
        assert f"(../{word})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
        assert f"(../kanji/{c}.md)" in (R / word).read_text(encoding="utf-8")
    guards = {tuple(sorted((row["word"], other)))
              for row in ledger["wordQuizAudit"]["directExclusions"] for other in row["exclude"]}
    assert len(guards) == 5
    assert not [c for c in chars if c != target and target in metadata(R, f"kanji/{c}.md").get("distractors", [])]
    stroke = load(S / "batch-091-stroke-evidence.json")
    svg = (S / "batch-091-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / f"{target}.json") == convert(target, svg.decode("utf-8"))
    assert stroke["dictionaryStrokeCount"] == stroke["sourceStrokePaths"] == 3
    font = load(S / "batch-091-reviewed-font-audit-647.json")
    text = "".join((R / n).read_text(encoding="utf-8") for n in font["scope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert set(font["actualHan"]) - set(han) == {"\u4e36"}
    assert set(han) <= set(font["actualHan"]) and len(han) == 20
    for row in font["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path) == row["sha256"]
        with TTFont(path) as face:
            cmap = face.getBestCmap()
        assert {c: ord(c) in cmap for c in font["actualHan"]} == row["actualPresence"]
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
    assert checked == 8432
    result.update(execution=656, latestMain=MAIN, upstreamAlreadyAncestor=True,
                  runtimeHashesVerified=checked, frozenInputHashesVerified=len(snapshot["inputs"]),
                  decompressedDictionaryHashesVerified=2, packets=packets,
                  completeRawCharacterRecordsVerified=occurrences,
                  originalBaselineMetadataAndStrokesPreserved=counts,
                  baselineMetadataExceptions=prior["baselineMetadataExceptions"],
                  baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
                  exactMembershipAccounted=True, currentCounts=actual_counts,
                  publishedIssue60Additions=117, acceptedUnpublishedIssue60Additions=[target],
                  separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
                  requiredAllMappedPairs=1, directedLinksVerified=2, directWordExclusionPairs=5,
                  pinnedStrokeGeometryExactlyRegenerated=True, scopedHan=han, fontProvenanceReverified=True,
                  inheritedFontScopeHan=font["actualHan"], removedHanSince647=["\u4e36"],
                  auditDiagnostic="First656 audit incorrectly expected unchanged647 Han membership. Reviewed653 mnemonic removes literal U+4E36; exact current20 is a subset of inherited/native650 scope21. No new glyph or teaching defect; original647/650 receipts preserved.")
    save(L / "combined-source-audit-656.json", result)
    print("Combined source/baseline/link/reading/font/membership audit passed; all8432 runtime hashes verified.")


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
        with (L / f"{name}-656.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-656.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-091-reconciliation.json")
    mnemonic = load(V / "batch-091-mnemonic-reconciliation-653.json")
    rendered = load(V / "batch-091-rendered-reconciliation-655.json")
    assert text["textualReviewClosed"]
    assert text["actionableRemainingTeachingFindings"] == text["consequentialUnresolvedTeachingFindings"] == 0
    assert all(f["status"] in {"resolved", "withdrawn", "optional"} for f in text["findings"])
    previous = None
    for label, process in text["processes"].items():
        assert process["actualModels"] == ["claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
        assert process["exitCode"] == 0 and not process["observedToolOverlaps"]
        assert process["allAssignedRangesReturned"]
        assert sha(V / process["report"]) == process["reportSha256"]
        assert sha(V / f"batch-091-initial-{label}.jsonl") == process["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    assert all(row["status"] == "resolved" for row in mnemonic["reconciliation"])
    assert rendered["findings"] == [] and all(row["status"] == "resolved" for row in rendered["reconciliation"])
    previous = None
    for process in rendered["dependentOriginalSessionConfirmations"]:
        assert process["acceptedExecution"] and process["exitCode"] == 0
        assert not process["observedToolOverlaps"] and not process["unfinishedTools"]
        assert len(process["actualDecodedImageReturns"]) == 1 and len(process["toolCalls"]) == 3
        assert not process["newBlindInitialReviewCredit"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    verified = 0
    for number in [650, 653, 654, 655]:
        evidence = load(S / f"execution-{number}.json")
        for row in evidence.get("artifacts", []) + evidence.get("receipts", []):
            path = R / (row.get("archive") or row["path"])
            assert sha(path) == (row.get("archiveSha256") or row["sha256"]), path
            if row.get("sourceSha256"):
                raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
                assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"], path
            verified += 1
    native = load(S / "execution-654.json")
    execution, route = native["executionReceipt"], native["nativeRoute"]
    assert execution["passed"] and execution["terminalSuccessCases"] == 1
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    assert {k: route[k] for k in ["archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "archiveRequests": 1, "importedKanji": 1114, "importedWords": 5070, "n1Cards": 123, "problems": 0}
    assert route["contentVersion"] == VERSION and route["acceptedReadingParserEpoch"] == 1
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["\u306f"]
    assert route["onlyKunHaNoOnPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 3 and route["directWordGuardCount"] == 5
    assert route["mappedReciprocalPairs"] == 1 and route["directedLinkTransitions"] == 2
    assert route["reciprocalLinkAndSystemBack"] and route["extraForefrontTransition"] and route["offline"]
    for pool in ["N1", "All"]:
        choices = route["productionBuilderN1AndAllExactChoices"][pool]
        assert choices["availableCuratedCount"] == 3 and choices["fallbackOptions"] == 0
        assert {o["kanji"] for o in choices["options"]} == set("\u5203\u4e43\u51f9\u51f8")
    for snapshot in [mnemonic["reviewedSnapshot"], rendered["reviewedSnapshot"], route["contentSnapshot"]]:
        assert not git("diff", snapshot, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for name in ["words/\u5203.md", "strokes/\u5203.json"]:
        assert sha(R / name) == text["reviewedRuntimeHashes"][name]
    assert not git("diff", PRODUCTION, APP, "--", "core/src/main", "app/src/main", "gradle.properties", root=A)
    return {
        "initialReviewRecord": "docs/n1-reviews/batch-091-reconciliation.json",
        "initialModels": text["initialModels"], "initialReportsReverified": True,
        "mnemonicRecord": "docs/n1-reviews/batch-091-mnemonic-reconciliation-653.json",
        "renderedRecord": "docs/n1-reviews/batch-091-rendered-reconciliation-655.json",
        "nativeRecord": "docs/n1-sources/execution-654.json", "nativeRoute": route,
        "nativeTerminalCaseStatuses": [0], "glyph650TerminalCaseStatuses": [0, 0],
        "receiptHashesReverified": verified, "V1": "resolved",
        "nativeRuntimeMatchesCurrentCombinedTree": True, "newNativeOrReviewerRuns": 0,
        "fontEvidence": "Inherit650 original21Han/fourComposefonts; exact current20Han subset after653 removes literal U+4E36. GlyphTest NOT rerun654/656.",
        "originalLimits": {"textual647": text["limits"], "mnemonic653": mnemonic["limits"],
                           "native650": load(S / "execution-650.json")["visualInspection"]["limits"],
                           "native654": native["visualInspection"]["limits"], "rendered655": rendered["limits"]},
        "priorProcessViolationPreserved": "Claude651 overlapping tools rejected; later serial confirmation is not retroactive repair.",
        "rerunDisposition": "No new concern; reviewed runtime, production app and fonts unchanged. Existing source/linguistic/native/rendered evidence inherited within its exact recorded scope, not fresh review.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-656.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-656.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    assert VERSION in (L / "manifest-656.txt").read_text(encoding="utf-8")
    vocabulary = (L / "vocabulary-656.txt").read_text(encoding="utf-8").strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-656.json")["exitCode"] == 0
    assert (L / "host-exit-656.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-656.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-656.txt").read_text(encoding="utf-8-sig").strip())
    ended = datetime.fromisoformat((L / "host-end-656.txt").read_text(encoding="utf-8-sig").strip())
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
    source, inheritance = load(L / "combined-source-audit-656.json"), inherited()
    budget = ast.literal_eval((L / "budget-656.txt").read_text(encoding="utf-8"))
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    assert not D.exists()
    D.mkdir()
    receipts = []
    paths = [
        *(L / name for name in ["starting-state-656.json", "combined-source-audit-656.json", "merge-656.txt",
          "python-tests-656.txt", "validate-656.txt", "manifest-656.txt", "vocabulary-656.txt", "budget-656.txt",
          "host-656.txt", "host-exit-656.txt", "host-command-656.json", "host-start-656.txt", "host-end-656.txt"]),
        *(L / f"{name}-exit-656.json" for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-091-host-656.ps1",
        C / "post-batch-091-656.ps1", C / "batch-065-host-integration-heap.init.gradle",
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
        "schemaVersion": 1, "execution": 656, "batch": "091", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-656.json"), "combinedContentHead": HEAD,
        "latestMainIntegrated": MAIN, "normalMerge": True, "mergeResult": "Already up to date.",
        "newMergeCommit": False, "conflicts": [], "substantiveTeachingConflictEdits": [],
        "runtimeBytesUnchanged": True, "sourceAudit": source, "pythonTestsPassed": int(match[1]),
        "validatorErrors": 0, "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary,
        "manifestFresh": True, "contentVersion": VERSION, "localBudget": budget, "hostSuites": suites,
        "hostChecksFresh": True, "hostTestsExecuted": 4, "androidHead": APP,
        "unchangedProductionAndroid": PRODUCTION, "qualifiedTestOnlyAndroid": True,
        "inheritedAcceptance": inheritance, "receipts": receipts, "runtimeAccepted": True,
        "runtimePublished": False, "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Local combined-tree acceptance only, not public delivery or fresh native/linguistic review. Vocabulary2122/2431 pilot consistency not full coverage. Original source/read/process/fontface/Paintprobe/injectedtrace/no successfulMLKit/phone limitations retained; current glyph20 subset of prior21. Qualified test-only Android not latestappmain. CI/publicZIP/publication/physicalphone/generalrelease/whole-set remain outstanding.",
    }
    save(S / "execution-656.json", evidence)
    path = S / "batch-091-progress.json"
    ledger = load(path)
    ledger["preCombined656State"] = {
        k: ledger.get(k) for k in ["status", "nextAction", "reviewClosed", "runtimeAccepted", "runtimePublished"]}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True,
                  runtimePublished=False, combinedAcceptance="docs/n1-sources/execution-656.json", nextAction=NEXT)
    save(path, ledger)
    body = (
        "**Batch 091 checkpoint 656: combined current-main acceptance passed locally; publication next.** "
        f"Fresh main `{MAIN}` is already an ancestor of reviewed `{HEAD}`; normal non-rewriting merge "
        "returned Already up to date. No teaching/runtime edit or substantive conflict.\n\n"
        f"Fresh {match[1]} Python tests, validator 0 errors, vocabulary consistency "
        f"(`{vocabulary}`), regenerated manifest/version `{VERSION}` and all 8,432 payload hashes passed. "
        "Frozen input and decompressed dictionary hashes, 78 complete lexical families/5 raw character records, "
        "original 985 kanji/4,942 words/985 strokes with recorded narrow exceptions, exact membership, "
        "all five raw readings, only kun は/no on, one all-mapped pair/two links, five direct word guards, "
        "pinned three-stroke regeneration and font provenance passed. Actual 1,114 kanji/5,070 words/"
        "123 N1 labels/128 named-source members. First audit caught a stale scope expectation: the reviewed "
        "653 mnemonic removed literal 丶, leaving 20 current Han covered by the inherited 21-Han native/font "
        "scope; original evidence preserved, no new glyph defect.\n\n"
        "Fresh actual-sibling RealContentTest THREE and RareHanTest ONE passed, zero skips/errors/failures. "
        "Explicit JDK17/SDK/one worker/in-process Kotlin/existing approved 2GiB HOST-only init; no guest/app "
        "heap or guard change. Qualified TEST-ONLY Android `1c1b7bf4` retains production `f9b59a2`, "
        "NOT latest app main.\n\n"
        "Original two-family textual review/corrections, mnemonic653 and serial original-session "
        "rendered655 confirmations reverified, NOT rerun. V1 resolved; GPT initial non-discovery and "
        "rejected Claude651 internal overlap retained. Native654 imported full archive fe3ec10b through "
        "production ContentSync ONCE: one terminal case0/no skips/zero problems/Room epoch1/current version. "
        "GlyphTest NOT rerun654/656; inherit650 exact21-Han/four-font evidence. All original source/read/"
        "native/font-face/Paint-probe/injected-trace/no successful-MLKit limits remain. Not physical-phone "
        "or native-speaker certification.\n\n"
        f"Local budget: {budget['entries']:,} entries / {budget['retainedBytes']:,} retained / "
        f"{budget['inflatedBytes']:,} inflated / {budget['localZipBytes']:,} compressed bytes. "
        "Original 18,000-entry/42MiB compressed/80MiB inflated/56MiB retained and per-file/media/path guards "
        "unchanged. Evidence: `docs/n1-sources/execution-656.json` and "
        "`docs/n1-reviews/batch-091-combined-acceptance-656`.\n\n"
        "**Next bounded checkpoint: fresh-main recheck, normal signed owner fast-forward publication, "
        "exact remote SHA, terminal green CI and EVERY immutable public ZIP runtime hash/budget, durable "
        "publication and owner issue receipt before batch092.** No push or next batch here. "
        "Published117/1,228; 1,111 remaining unchanged. Compatible f9b59a2+ required; physical-phone/"
        "general-release/whole-set acceptance outstanding. Live parent19008/session/decoded launcher "
        "verified; runner.lock untouched. No optional historical-session helper or new permission denial.\n"
    )
    (L / "issue-body-656.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance and lossless evidence archived; ready for normal signed LOCAL checkpoint.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-656.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["sha256"]
        raw = (R / row["archive"]).read_bytes()
        if row["losslessGzip"]:
            raw = gzip.decompress(raw)
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    receipt = load(L / "issue-verified-656.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (L / "issue-body-656.txt").read_text(encoding="utf-8")
    before, p = load(L / "progress-before-656.json"), load(C / "progress.json")
    assert p["checkpoint"] == 655 and p["batch"] == "091"
    row = {
        "schemaVersion": 1, "execution": 656, "checkpoint": 656, "batch": "091",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-656.json", "evidenceSha256": sha(S / "execution-656.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "runtimeHashesVerified": 8432,
        "contentVersion": VERSION, "pythonTestsPassed": evidence["pythonTestsPassed"],
        "freshHostTestsPassed": 4, "hostSkips": 0, "runtimeAccepted": True, "runtimePublished": False,
        "runtimeBytesUnchanged": True, "freshNativeOrReviewerRuns": 0, "V1": "resolved",
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 117, "remainingAdditions": 1111, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    p["execution656StartingState"]["status"] = "signed-local-combined-acceptance-checkpoint-complete"
    p["execution656CoordinatorCheckpoint"] = row
    p["batch091CombinedAcceptanceCheckpoint"] = row
    p.update(checkpoint=656, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in allowed)
    save(C / "progress.json", p)
    actual = load(C / "progress.json")
    assert all(actual[k] == value for k, value in before.items() if k not in allowed)
    save(L / "checkpoint-656.json", row)
    print(json.dumps({"checkpoint": 656, "commit": saved, "status": "continue", "issue": receipt["html_url"]}))


if __name__ == "__main__":
    {"start": start, "checks": checks, "audit": audit, "record": record, "finish": finish}[sys.argv[1]]()
