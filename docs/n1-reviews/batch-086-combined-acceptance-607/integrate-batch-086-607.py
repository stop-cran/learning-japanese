"""Combined-tree checkpoint; the live launcher owns runner.lock throughout."""
import ast
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
L = C / "logs" / "ed3499c0-6a0d-4ef9-82b6-fa2f03f3c1a9"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
HEAD = "f23dae44b7c044087f1fe7d31176c4c1534f6e94"
MAIN = "f001846c194b20b13b9deb797d70e04a34025d93"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "86e8cb13aa72ecd0"
STAGE = "batch-086-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME086 normal signed owner fast-forward PUBLICATION and exact public acceptance next; NO087. "
    "Read docs/n1-sources/execution-607.json and batch-086-combined-acceptance-607 receipts. "
    "Fresh origin/main f001846c already ancestor of signed reviewed f23dae44; normal merge Already up to date, "
    "no conflict, substantive teaching edit or artificial merge. Fresh combined full Python/validate/vocabulary/"
    "manifest/budget/source/baseline/membership/reading/alias/seven reciprocal pairs-fourteen directions/"
    "eight direct guards/pinned three-stroke regeneration and non-skipped RealContentTest3+RareHanTest1 "
    "passed on actual sibling content. All8416 runtime hashes/version86e8cb13aa72ecd0 unchanged; "
    "1109kanji/5064words/118N1labels/123namedsource members. Original602 blind ClaudeOpus5.5/GPT6.1Sol "
    "and606 dependent original-session visuals/605 native two terminalcase0 retained and reverified, NOT "
    "rerun. ProductionContentSyncONCE/zeroProblems/Roomepoch1; only on keysぼん/はん scheduled, kun[]; "
    "allfive raw readings/order retained. Rawおうよ.そ modern usage remains UNVERIFIED source-only, "
    "not normalized or asserted modern usage. All31Han/fourfonts incl丶/几 readable; exactfallbackface "
    "unknown; images toolresized, not nativepixel independentinspection. N1 meaning only凹 curated available "
    "plus TWO fallbacks; bounded observed Englishlabels and seeded604 choices safe, not arbitrarypool "
    "certification. Three injectedtrace strokes/recallgiveup NOT human handwriting/MLKit/phone. Qualified "
    "TESTONLY Android1c1b7bf4 retains productionf9b59a2, not latestappmain; no guest/app heap/guard change. "
    "Before push freshly fetch main; if advanced normallymerge/reconcile/regenerate/revalidate actual "
    "combinedtree and independently rereview substantivechangedteaching. Ownerstop-cran token ONLY "
    "publicationchild, verifyidentity/globalaccountunchanged/normal signing/noamend/noforce. Verify exact "
    "remoteSHA/terminalgreen relevantCI/EVERYruntimehash+manifest in EXACTimmutableGitHubZIP and original "
    "18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepathguards. Preserve all "
    "authored/reviewed/integrated/publishedSHAs/counts/source+review+publication ledgers/verifiedownerissue60 "
    "BEFORE087. Published112/1228,remaining1116/latestpublicf001846c unchanged until verifiedpublication; "
    "086notdelivered. Six separate earlierN2sourceplacements保案派第策結 remain earlierlevels, NOT "
    "acceptedissue60batches; no duplication. Original source/review/process/denial/OOM/readdepth/downscale/"
    "fallbackface/pool/phone limits and optional dispositions preserved. Physicalphone/generalrelease/"
    "whole-setoutstanding; projectincomplete. Parent19008 runner.lock liveowned throughout; verify "
    "ancestry/session/checkpoint/exactsignedheads/whollycleanworktrees; never reacquire/delete/unlock. "
    "Approvedcontrol/committedsources only/nooptionalhistoricalsessionhelpers. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. No087 or unreviewed push."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".607.tmp")
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
    assert not git("status", "--porcelain", root=root)


def context():
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)


def start():
    context()
    clean(R, HEAD)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (606, "086", "continue")
    assert not (L / "progress-before-607.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-607.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 606
    state = {
        "execution": 607, "batch": "086", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME086 current-main integration and combined-tree validation; signed LOCAL checkpoint only. No087/publication/new native or reviewer absent changed teaching or new concern.",
        "request": {
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "characters": len(text),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, entire approved issue and final606 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial scalar print hit cp1252; bounded UTF-8 reread succeeded.",
        },
        "runnerLockRole": "Live parent19008 ancestry/session verified; no child opens/acquires/deletes/unlocks runner.lock.",
        "artifactPathPreflight": "Approved workspace inputs/control helpers and committed source/review evidence only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-607.json", state)
    p["execution607StartingState"] = state
    p.update(stage="batch-086-combined-main-integration-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-607.json")
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    print("Starting scope persisted with complete live history.")


def audit():
    from audit_n1_batch import audit as batch_audit, lexical_pair
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from generate_strokes import convert

    context()
    clean(R, HEAD)
    assert git("merge-base", MAIN, HEAD) == MAIN
    result = batch_audit(R, "086")
    ledger = load(S / "batch-086-progress.json")
    assert ledger["baseCommit"] == MAIN and ledger["published"] == []
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(gzip.decompress(jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    packets, families = [], {}
    for packet in ledger["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        expected = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / packet["xml"]).read_bytes()
        packets.append({"path": packet["xml"], "families": len(ids),
                        "freshFrozenExtractionMatches": True, "sha256": sha(S / packet["xml"])})
        families.update({e.findtext("ent_seq"): e for e in ET.fromstring(expected).findall("entry")})
    assert len(packets) == 3 and len(families) == 71
    for row in ledger["recognitionAliasMappings"]:
        assert any(lexical_pair(families[i], row["spelling"], row["primaryReading"])
                   for i in row["entryIds"])
        text = (R / row["article"]).read_text(encoding="utf-8")
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        assert row["spelling"] in plain and row["primaryReading"] in plain
        assert "(../kanji/凡.md)" in text
        if row["spelling"] == "凡て":
            spelling = next(k for k in families["1595730"].findall("k_ele")
                            if k.findtext("keb") == "凡て")
            assert spelling.findtext("ke_inf") == "rarely used kanji form"
            assert "rare kanji spelling" in plain
    assert not any(e.text == "おうよそ" for e in ET.fromstring(gzip.decompress(jm)).iter("reb"))
    kd_root = ET.fromstring(kd)
    records = {e.findtext("literal"): e for e in kd_root.findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    occurrences = 0
    for name in ["batch-086-kanjidic2.xml", "batch-086-comparison-kanjidic2.xml"]:
        packet = ET.parse(S / name).getroot()
        assert canonical(packet.find("header")) == canonical(kd_root.find("header"))
        for row in packet.findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            occurrences += 1
    assert occurrences == 7
    baseline = load(S / "baseline-inventory.json")
    prior = load(S / "batch-086-draft-audit.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(info["metadata"])
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
    assert len(published) == 112 and chars - old == published | separate | nonmembers | {"凡"}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    actual_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert actual_counts == {"kanji": 1109, "words": 5064, "n1Labels": 118,
                             "namedSourceMembersPresent": 123}
    mappings = ledger["supportMappings"] + ledger["recognitionAliasMappings"]
    pairs = {(c, row["article"]) for row in mappings
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").exists()}
    pairs.update(("凡", row["article"]) for row in ledger["recognitionAliasMappings"])
    assert pairs == {tuple(row) for row in ledger["allMappedReciprocalPairs"]} and len(pairs) == 7
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    assert {f"words/{path.name}" for path in (R / "words").glob("*.md")
            if "凡" in metadata(R, f"words/{path.name}")["kanji"]} == {
                row["article"] for row in ledger["supportMappings"]}
    guards = {tuple(sorted((row["word"], other)))
              for row in ledger["wordQuizAudit"]["directExclusions"] for other in row["exclude"]}
    assert len(guards) == 8 and "jlpt" not in metadata(R, "words/凡例.md")
    stroke = load(S / "batch-086-stroke-evidence.json")
    svg = (S / "batch-086-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "凡.json") == convert("凡", svg.decode("utf-8"))
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
    assert checked == 8416
    result.update(
        execution=607, latestMain=MAIN, preIntegrationHead=HEAD, upstreamAlreadyAncestor=True,
        normalMergeResult="Already up to date; no artificial merge commit.",
        runtimeHashesVerified=checked, frozenInputsVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterOccurrencesVerified=occurrences,
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=prior["baselineMetadataExceptions"],
        baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
        exactMembershipAccounted=True, currentCounts=actual_counts,
        publishedIssue60Additions=112, acceptedUnpublishedIssue60Additions=["凡"],
        separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
        remainingIssue60Acceptance=1116, sixEarlierPlacementsCountedAsIssue60Accepted=False,
        requiredAllMappedPairs=len(pairs), directedLinksVerified=14, recognitionAliasesVerified=2,
        directWordExclusionPairs=len(guards), pinnedStrokeGeometryExactlyRegenerated=True,
        runtimePublished=False,
        limits="Mechanical source/baseline/link/reading/hash audit, not a fresh linguistic review or native run. Original reviewer/native qualifications retained.",
    )
    save(L / "combined-source-audit-607.json", result)
    print("Combined source audit passed; all8416 runtime hashes and exact membership verified.")


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
        command = [sys.executable, "-B", *args]
        with (L / f"{name}-607.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT,
                                    env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        save(L / f"{name}-exit-607.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-086-reconciliation.json")
    visual = load(V / "batch-086-visual-606-reconciliation.json")
    assert text["textualReviewClosed"] and text["actionableRemainingTeachingFindings"] == 0
    assert text["consequentialUnresolvedTeachingFindings"] == 0
    assert visual["dependentVisualConfirmationClosed"] and visual["actionableRemainingFindings"] == 0
    assert visual["consequentialUnresolvedTeachingClaims"] == 0
    reports = []
    image_hashes = {}
    for group, prefix in [(text["processes"], "initial"), (visual["processes"], "visual-606")]:
        previous = None
        for label, process in group.items():
            assert process["actualModels"] == [
                "claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
            assert process["exitCode"] == 0
            report = V / f"batch-086-{prefix}-{label}.md"
            assert sha(report) == process["reportSha256"]
            execution = load(V / f"batch-086-{prefix}-{label}-execution.json")
            assert execution["actualModels"] == process["actualModels"]
            assert execution["sessionId"] == process["sessionId"] and execution["exitCode"] == 0
            assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
            if prefix == "initial":
                assert sha(V / f"batch-086-initial-{label}.jsonl") == process["rawExecutionSha256"]
                assert process["allAssignedRangesReturned"]
            else:
                coverage = load(V / f"batch-086-visual-606-{label}-coverage.json")
                archive = R / coverage["losslessRawArchive"]
                assert sha(archive) == coverage["losslessRawArchiveSha256"]
                raw = gzip.decompress(archive.read_bytes())
                assert len(raw) == coverage["rawOriginalBytes"]
                assert hashlib.sha256(raw).hexdigest() == process["rawExecutionSha256"]
                assert execution["actualDistinctImageViews"] == 24
                assert execution["completePacketReturned"] and execution["originalReportReturnedCompletely"]
                assert not execution["missingRequiredImages"] and not execution["missingPacketLines"]
                images = coverage["actualImageReturns"]
                assert len(images) == 24 and coverage["all24ImagePayloadsDecodedAndDimensionsVerified"]
                for image in images:
                    source = Path(image["path"])
                    assert source.is_relative_to(R) and sha(source) == image["sourceImageSha256"]
                image_hashes[label] = [row["actualReturnedImageSha256"] for row in images]
            if previous is not None:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
            previous = process["completedAt"]
            reports.append({"report": report.relative_to(R).as_posix(), **process, "rerun": False})
    assert image_hashes["claude"] == image_hashes["gpt"]
    native = load(S / "execution-605.json")
    assert native["nativePerCaseTerminalStatus"] == [0, 0]
    assert native["nativeSkips"] == native["nativeFailures"] == 0
    assert native["fullArchiveProductionContentSyncCalls"] == 1
    assert native["nativeExecution"]["passed"] and native["nativeExecution"]["ownedHelperStopped"]
    assert native["runtimeVerification"]["contentVersion"] == VERSION
    route = native["productionImportAndRoutes"]
    assert {k: route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "importedKanji": 1109, "importedWords": 5064, "n1Cards": 118, "problems": 0}
    assert route["contentVersion"] == VERSION and route["acceptedReadingParserEpoch"] == 1
    inventory = load(R / native["archiveInventory"])
    assert len(inventory) == 108
    for name, expected in inventory.items():
        assert sha(R / name) == expected, name
    assert load(S / "execution-606.json")["runtimeVerification"]["contentVersion"] == VERSION
    assert not git("diff", text["reviewedTeachingSnapshot"], HEAD, "--",
                   "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    return {
        "reviewReports": reports, "nativeTerminalCaseStatuses": [0, 0],
        "newNativeOrReviewerRuns": 0, "nativeContentVersion": VERSION,
        "nativeArtifactHashesReverified": len(inventory),
        "allFourRawReviewExecutionHashesReverified": True,
        "all24ReturnedImagePayloadHashReceiptsMatchBetweenModels": True,
        "nativeRuntimeMatchesCurrentCombinedTree": True,
        "nativeEvidence": "docs/n1-sources/execution-605.json",
        "nativeEvidenceSha256": sha(S / "execution-605.json"),
        "visualEvidence": "docs/n1-reviews/batch-086-visual-606-reconciliation.json",
        "visualEvidenceSha256": sha(V / "batch-086-visual-606-reconciliation.json"),
        "inheritedSourceTextLimits": text["limits"],
        "inheritedNativeVisualDispositions": visual["dispositions"],
        "rerunDisposition": "Fresh main already included; runtime, source, app production, pools, readings, articles and strokes unchanged since accepted605/606 evidence. Fresh combined HOST4 required; no new native concern or substantive teaching change established.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-607.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M)
    assert not re.search(r"^FAILED|skipped=", tests, re.M)
    assert (L / "validate-607.txt").read_text().strip() == "0 error(s)"
    assert VERSION in (L / "manifest-607.txt").read_text()
    assert (L / "vocabulary-607.txt").read_text().strip() == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-607.json")["exitCode"] == 0
    assert (L / "host-exit-607.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-607.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-607.txt").read_text().strip())
    suites = []
    for relative, expected in [
        ("core\\build\\test-results\\test\\TEST-io.github.stopcran.kanji.core.RealContentTest.xml", 3),
        ("app\\build\\test-results\\testDebugUnitTest\\TEST-io.github.stopcran.kanji.core.RareHanTest.xml", 1),
    ]:
        path = A / relative
        xml = ET.parse(path).getroot()
        assert xml.attrib["tests"] == str(expected)
        assert all(xml.attrib[key] == "0" for key in ["skipped", "errors", "failures"])
        assert len(xml.findall("testcase")) == expected
        assert not any(xml.findall(".//" + name) for name in ["skipped", "failure", "error"])
        assert datetime.fromisoformat(xml.attrib["timestamp"]).astimezone(timezone.utc) >= started.astimezone(timezone.utc)
        suites.append({"path": str(path), "sha256": sha(path), "suite": xml.attrib,
                       "cases": [case.attrib for case in xml.findall("testcase")]})
    assert not git("diff", "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", APP,
                   "--", "app/src/main", "core/src/main", "gradle.properties", root=A)
    source = load(L / "combined-source-audit-607.json")
    assert source["runtimeHashesVerified"] == 8416
    inheritance = inherited()
    budget = ast.literal_eval((L / "budget-607.txt").read_text())
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    target_folder = V / "batch-086-combined-acceptance-607"
    assert not target_folder.exists()
    target_folder.mkdir()
    receipts = []
    for path in [
        *(L / name for name in [
            "starting-state-607.json", "combined-source-audit-607.json", "merge-607.txt",
            "python-tests-607.txt", "validate-607.txt", "manifest-607.txt", "vocabulary-607.txt",
            "budget-607.txt", "host-607.txt", "host-exit-607.txt", "host-command-607.json",
            "host-start-607.txt", "host-end-607.txt", "runner-ancestry-607.json"]),
        *(L / f"{name}-exit-607.json" for name in ["python-tests", "validate", "manifest", "vocabulary", "budget"]),
        *(Path(row["path"]) for row in suites),
        Path(__file__), C / "run-batch-086-combined-host-607.ps1",
        C / "post-batch-086-combined-607.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
    ]:
        target = target_folder / (path.name + ".gz" if path.suffix == ".txt" else path.name)
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "sha256": sha(target),
                         "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 607, "batch": "086", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-607.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN,
        "normalMerge": True, "upstreamAlreadyAncestor": True, "mergeResult": "Already up to date.",
        "newMergeCommit": False, "conflicts": [], "substantiveTeachingConflictEdits": [],
        "batchTeachingUnchanged": True, "runtimeBytesUnchanged": True,
        "sourceAudit": source, "pythonTestsPassed": int(match[1]), "validatorErrors": 0,
        "vocabularyConsistencyPassed": True, "manifestFresh": True, "contentVersion": VERSION,
        "localBudget": budget, "hostSuites": suites, "hostChecksFresh": True, "hostTestsExecuted": 4,
        "androidHead": APP, "productionAndroidBytesUnchanged": True,
        "inheritedAcceptance": inheritance, "receipts": receipts,
        "runtimeAccepted": True, "runtimePublished": False,
        "publishedAdditions": 112, "remainingAdditions": 1116, "lastPublishedCommit": MAIN,
        "earlierLevelSourceMemberDisposition": source["separateEarlierLevelSourceMembers"],
        "earlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Combined-tree source/mechanical/fresh HOST acceptance, not public delivery or fresh linguistic/native review. Original602/603/604/605/606 source/process/read-depth/downscale/fallbackface/MLKit/phone/pool qualifications retained. Rawおうよ.そ modern use UNVERIFIED source-only. Physical phone/general release/whole-set outstanding.",
    }
    save(S / "execution-607.json", evidence)
    ledger = load(S / "batch-086-progress.json")
    ledger["preCombined607State"] = {
        key: ledger.get(key) for key in ["status", "nextAction", "reviewClosed", "runtimeAccepted", "runtimePublished"]}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True,
                  runtimePublished=False, combinedAcceptance="docs/n1-sources/execution-607.json", nextAction=NEXT)
    (S / "batch-086-progress.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    body = (
        f"Batch086 checkpoint607: **current-main integration and combined-tree acceptance passed locally; publication next**. "
        f"Fresh origin/main `{MAIN}` is already an ancestor of reviewed local `{HEAD}`; normal non-rewriting merge "
        "returned 'Already up to date'. No artificial merge, conflict resolution or substantive teaching edit.\n\n"
        f"Fresh {match[1]} Python tests, validator0errors, actual CI vocabulary consistency, regenerated fresh manifest, "
        "frozen inputs/decompression/three full lexical packet re-extractions (71families)/seven raw character records, "
        "original985kanji/4942words/985strokes with recorded exceptions, exact membership, allfive reading dispositions, "
        "two recognition aliases, seven reciprocal pairs/fourteen directions, eight direct guards and pinnedthree-stroke "
        f"regeneration passed. All8,416 runtime hashes/version`{VERSION}` verified; 1,109kanji/5,064words/118N1labels/"
        "123named members. Fresh actual-sibling Android RealContentTest3 and RareHanTest1, zero skips/errors/failures; "
        "oneworker/in-processKotlin/explicitJDK17+SDK/unchanged approved2GiBHOSTinit. Exact signed TESTONLYAndroid1c1b7bf4 "
        "atop unchanged productionf9b59a2, not latest app main; no production app/guest heap change.\n\n"
        "Original602 two blind families (ClaudeOpus5.5/GPT6.1Sol),605 two terminalcase0 native and606 dependent "
        "original-session visuals retained/reverified, NOT rerun. Same full productionContentSyncONCE/version/counts/"
        "zeroProblems/Roomepoch1; onlyぼん/はん scheduled, kun[]. Allfive raw readings/order retained; "
        "rawおうよ.そ modern usage remains UNVERIFIED source-only. All31Han/fourfamilies incl丶/几 readable; "
        "exact fallback face unknown and image-tool resizing disclosed. N1 meaning has only凹 curated available "
        "plus TWO fallbacks; bounded observed/seeded choices not arbitrary-pool certification. Three injectedtrace/"
        "recallgiveup strokes are not human handwriting/MLKit/phone evidence. All original source/process/read-depth/"
        "denial/OOM/downscale/pool/device limits and optional dispositions preserved.\n\n"
        f"Local budget: {budget['entries']:,}entries, {budget['retainedBytes']:,}retained, "
        f"{budget['inflatedBytes']:,}inflated, {budget['localZipBytes']:,}compressed bytes; original18,000entries/"
        "42MiBcompressed/80MiBinflated/56MiBretained/per-file/media/safe-path guards unchanged. Evidence: "
        "`docs/n1-sources/execution-607.json`, `docs/n1-reviews/batch-086-combined-acceptance-607`.\n\n"
        "**Next bounded checkpoint: fresh-main recheck, normal signed owner fast-forward publication, exact remoteSHA/"
        "terminalgreenCI/EVERY immutable public ZIP runtime hash and unchanged budgets, durable publication/verified "
        "owner issue receipt before087.** No push or087 here. Published112/1228;1116remaining unchanged; six separate "
        "earlier N2 source placements are not accepted issue60 batches. Compatiblef9b59a2+ required for ownertesting; "
        "physical-phone/general-release/whole-set acceptance remains outstanding; project incomplete. "
        "Live parent19008 ancestry verified; child never opens/reacquires/deletes/unlocks runner.lock. "
        "Approved workspace/control/committed evidence only; no optional historicalsession artifact or new denial.\n"
    )
    (L / "issue-body-607.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance, lossless receipts and current ledger recorded for signed LOCAL checkpoint.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-607.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["sha256"]
    receipt = load(L / "issue-verified-607.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (L / "issue-body-607.txt").read_text(encoding="utf-8")
    before = load(L / "progress-before-607.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 606 and p["batch"] == "086"
    row = {
        "schemaVersion": 1, "execution": 607, "checkpoint": 607, "batch": "086",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-607.json", "evidenceSha256": sha(S / "execution-607.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "upstreamAlreadyAncestor": True,
        "runtimeHashesVerified": 8416, "contentVersion": VERSION,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "freshHostTestsPassed": 4, "hostSkips": 0,
        "runtimeAccepted": True, "runtimePublished": False, "runtimeBytesUnchanged": True,
        "newNativeOrReviewerRuns": 0, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 112, "remainingAdditions": 1116, "lastPublishedCommit": MAIN,
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "issueUpdate": receipt["html_url"], "ownerIssueAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(L / "issue-verified-607.json"),
        "nextAction": NEXT, "blocker": None, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p.update(checkpoint=607, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution607CoordinatorCheckpoint"] = row
    p["batch086CombinedAcceptanceCheckpoint"] = row
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(L / "checkpoint-verification-607.json", row)
    print(f"Checkpoint607 persisted at signed {saved}; full historical values preserved. SAME086 publication next; no087.")


if __name__ == "__main__":
    {"start": start, "audit": audit, "checks": checks, "record": record, "finish": finish}[sys.argv[1]]()
