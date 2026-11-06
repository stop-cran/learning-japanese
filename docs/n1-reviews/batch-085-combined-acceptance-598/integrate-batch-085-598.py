"""Bounded combined-tree acceptance; runner.lock remains owned by the parent."""
import gzip
import ast
import hashlib
import json
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
L = C / "logs" / "4e19ca44-0f2d-4721-996a-8f32a6f5d943"
S = R / "docs" / "n1-sources"
HEAD = "40eb5dcee006ef142721fcd9c9e923c616f6a89e"
MAIN = "97a16b0027b05c0528d78971dd3b17cce17d8056"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "0c514711ae8d3212"
STAGE = "batch-085-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME085 normal signed owner fast-forward PUBLICATION and exact public acceptance NEXT; no086. "
    "Read signed execution-598.json, combined acceptance receipts, original593 textual/two-family reports, "
    "594 HOST4, compiled595,596 two terminalcase0 native and597 original-family visual confirmations. "
    "Fresh origin/main97a16b00 was already an ancestor of reviewed local40eb5dce; normal merge returned "
    "Already up to date, no artificial merge/rewrite/conflict/substantive teaching edit. Same reviewed "
    "a7512a5e plus29a53380 effort guard/envelope1d2e3290/version0c514711ae8d3212/8413runtimehashes. "
    "Fresh598 combined372Python/validate0/vocabulary/freshmanifest/frozeninput+decompressedhashes/"
    "threefulllexicalpacketreextractions/fourrawcharacterrecords/original985kanji4942words985strokes "
    "with recordedexceptions/exactmembership/fourreciprocalpairs-eightdirections/sixreadings-curation/"
    "exact32directguards/pinned16stroke regeneration/originalbudgets passed. Fresh sibling HOST "
    "RealContentTest3+RareHanTest1 zero skips/errors/failures, one worker/in-processKotlin/explicitJDK17SDK/"
    "unchanged approved2GiBHOSTinit; exact signedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9, "
    "not latestappmain. No new native/reviewer run absent actualchange/newconcern. Original two model "
    "families actualClaudeOpus5.5/GPT6.1Sol sessions/reports/serialexits/archives/imagepayloads and112native "
    "artifacts reverified, NOT rerun. Native ContentSyncONCE version/counts match current unchanged "
    "runtime1108kanji5063words117N1/zeroProblems/acceptedRoomparserEpoch1. Curatedonギョウ/"
    "kunこ.る,こ.らす yields exactlyぎょう/こる BOTHkindspersistedGood/done; selectedこ.らす shares "
    "normalizedこる NOT independentqueuedmastery.39Han/fourfonts/threewholewords, allscopedarticles/"
    "changed固bullet, fourpairs/eightdirections/offline/SystemBack/defaultfourchoices inherited within "
    "capturedscope; AllUI/custom/padded/partial/larger/random pools uncertified.16referenceINJECTED "
    "strokes/trace/recallgiveup/gradepersistence NOT humanhandwriting/MLKit/phone; offline model unavailable. "
    "Before push freshly fetch main; if advanced normallymerge/reconcile/regenerate/revalidate actual "
    "combinedtree, bounded independentrereview of substantivechangedteaching. Ownerstop-cran token ONLY "
    "publicationchild, verifyidentity/globalaccountunchanged/normal signing/noamend/noforce. Verify exact "
    "remoteSHA/terminalgreen relevantCI/EVERYruntimehash+manifest in EXACTimmutableGitHubZIP and original "
    "18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepathguards. Preserve all "
    "authored/reviewed/integrated/publishedSHAs/counts/source+review+publication ledgers/verifiedownerissue60 "
    "BEFORE086. Published111/1228,remaining1117/latestpublic97a16b00 unchanged;085notdelivered. Six separate "
    "earlierN2sourceplacements保案派第策結 remain earlierlevels, NOT acceptedissue60batches; no duplication. "
    "All original source/lookup/readdepth/process/compaction/downscale/fallbackface/bodyfine-stroke/"
    "pool/phone limits andQ1resolved/otheroptional dispositions preserved. Physicalphone/generalrelease/"
    "whole-setoutstanding; projectincomplete. Parent19008 runner.lock liveowned throughout; verify "
    "ancestry/session/checkpoint/exactsignedheads/whollycleanworktrees; never reacquire/delete/unlock. "
    "Approvedcontrol/committedsources only/nooptionalhistoricalsessionhelpers. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. No086."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value, ascii=True):
    temporary = path.with_suffix(path.suffix + ".598.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=ascii, indent=2) + "\n", encoding="utf-8")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (597, "085", "continue")
    assert not (L / "progress-before-598.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-598.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 597
    state = {
        "execution": 598, "batch": "085", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME085 normal latest-main integration and combined-tree acceptance; signed LOCAL checkpoint before owner publication. No086 or new reviewer/native absent a changed substantive passage or new concern.",
        "request": {
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "characters": len(text),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, complete approved issue and final597 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial tail print hit cp1252; final checkpoint subsequently read with UTF-8.",
        },
        "runnerLockRole": "Live parent19008 verified in coordinator ancestry and decoded launcher command; no child opens/acquires/deletes/unlocks runner.lock.",
        "artifactPathPreflight": "Approved workspace inputs/control helpers and committed source/review packets only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-598.json", state)
    p["execution598StartingState"] = state
    p.update(stage="batch-085-combined-main-integration-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    old = load(L / "progress-before-598.json")
    assert all(p[k] == v for k, v in old.items() if k not in {"stage", "nextAction", "blocker"})
    print("Starting scope saved; complete live history preserved.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from generate_strokes import convert

    context()
    clean(R, HEAD)
    assert git("merge-base", MAIN, HEAD) == MAIN
    assert not git("diff", HEAD, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    result = batch_audit(R, "085")
    ledger = load(S / "batch-085-progress.json")
    assert ledger["baseCommit"] == MAIN
    assert ledger["reviewClosed"] == ["凝"] and ledger["published"] == []
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd_raw = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(gzip.decompress(dictionary)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd_raw).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    packets = []
    for packet in ledger["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        expected = extract(dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / packet["xml"]).read_bytes()
        packets.append({"path": packet["xml"], "families": len(ids),
                        "freshFrozenExtractionMatches": True, "sha256": sha(S / packet["xml"])})
    assert len(packets) == 3 and sum(row["families"] for row in packets) == 110
    kd = ET.fromstring(kd_raw)
    records = {row.findtext("literal"): row for row in kd.findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    occurrences = 0
    for name in ["batch-085-kanjidic2.xml", "batch-085-comparison-kanjidic2.xml"]:
        packet = ET.parse(S / name).getroot()
        assert canonical(packet.find("header")) == canonical(kd.find("header"))
        for row in packet.findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            occurrences += 1
    assert occurrences == 4
    baseline = load(S / "baseline-inventory.json")
    prior = load(S / "batch-085-draft-audit.json")
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
    separate = set("保案派第策結")
    nonmembers = set("坊的誰身阪")
    assert len(published) == 111 and chars - old == published | separate | nonmembers | {"凝"}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    actual_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert actual_counts == {"kanji": 1108, "words": 5063, "n1Labels": 117,
                             "namedSourceMembersPresent": 122}
    pairs = {(c, row["article"]) for row in ledger["supportMappings"]
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(row) for row in ledger["allMappedReciprocalPairs"]} and len(pairs) == 4
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    assert {f"words/{path.name}" for path in (R / "words").glob("*.md")
            if "凝" in metadata(R, f"words/{path.name}")["kanji"]} == {row["article"] for row in ledger["supportMappings"]}
    guards = {tuple(sorted((row["word"], other)))
              for row in ledger["wordQuizAudit"]["directExclusions"] for other in row["exclude"]}
    assert len(guards) == 32
    stroke = load(S / "batch-085-stroke-evidence.json")
    svg = (S / "batch-085-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "凝.json") == convert("凝", svg.decode("utf-8"))
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
    assert checked == 8413
    result.update(
        execution=598, latestMain=MAIN, preIntegrationHead=HEAD,
        upstreamAlreadyAncestor=True, normalMergeResult="Already up to date; no artificial merge commit.",
        runtimeHashesVerified=checked, frozenInputsVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterOccurrencesVerified=occurrences,
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=prior["baselineMetadataExceptions"],
        baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
        exactMembershipAccounted=True, currentCounts=actual_counts,
        publishedIssue60Additions=111, acceptedUnpublishedIssue60Additions=["凝"],
        separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
        remainingIssue60Acceptance=1117, sixEarlierPlacementsCountedAsIssue60Accepted=False,
        requiredAllMappedPairs=len(pairs), directWordExclusionPairs=len(guards),
        pinnedStrokeGeometryExactlyRegenerated=True, runtimePublished=False,
        limits="Mechanical source/baseline/link/reading/hash audit, not a fresh linguistic review or native run. Original reviewer/native qualifications retained.",
    )
    save(L / "combined-source-audit-598.json", result)
    print("Combined source audit passed; all8413 runtime hashes and exact membership verified.")


def checks():
    context()
    clean(R, HEAD)
    commands = [
        ("python-tests", [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", [sys.executable, "-B", "tools\\validate.py"]),
        ("manifest", [sys.executable, "-B", "tools\\build_manifest.py"]),
        ("vocabulary", [sys.executable, "-B", "tools\\grammar_vocabulary.py", "check"]),
        ("budget", [sys.executable, "-B", "tools\\check_content_budget.py"]),
    ]
    for name, command in commands:
        with (L / f"{name}-598.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT,
                                    env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
        save(L / f"{name}-exit-598.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    folder = R / "docs" / "n1-reviews"
    text = load(folder / "batch-085-reconciliation.json")
    visual = load(folder / "batch-085-visual-reconciliation.json")
    assert text["textualReviewClosed"]
    assert text["actionableRemainingTeachingFindings"] == 0
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedScopedClaims"] == 0
    assert load(S / "execution-597.json")["independentVisualAcceptance"]
    reports = []
    for group in [text["processes"], visual["processes"]]:
        previous = None
        for label, process in group.items():
            row = load(folder / process["execution"])
            model = "claude-opus-5.5" if "claude" in label else "gpt-6.1-sol"
            assert row["actualModels"] == [model] and row["exitCode"] == 0
            assert sha(folder / process["report"]) == process["reportSha256"]
            if previous is not None:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(row["startedAt"])
            previous = row["completedAt"]
            if "rawArchive" in process:
                assert sha(folder / process["rawArchive"]) == process["rawArchiveSha256"]
                turns = row["turns"]
                assert len(turns) == 25
                assert len(gzip.decompress((folder / process["rawArchive"]).read_bytes()).splitlines()) > 25
                for index, turn in enumerate(turns):
                    assert turn["exitCode"] == 0
                    if turn["resource"] is not None:
                        assert turn["singleResourceAccepted"]
                    else:
                        assert index == 24 and turn["toolCalls"] == 0
                    if index:
                        assert datetime.fromisoformat(turns[index - 1]["completedAt"]) < datetime.fromisoformat(turn["startedAt"])
                    if "imagePayload" in turn:
                        image = turn["imagePayload"]
                        assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                        source = Path(turn["resource"])
                        assert source.is_relative_to(R) and sha(source) == image["sourceSha256"]
            else:
                assert sha(folder / f"batch-085-{label}.jsonl") == process["rawExecutionSha256"]
                assert not row["observedToolOverlaps"] and not row["unfinishedTools"]
            reports.append({
                "report": process["report"], "reportSha256": process["reportSha256"],
                "actualModels": [model], "sessionId": row["sessionId"],
                "exitCode": 0, "serialTimingReverified": True, "rerun": False,
            })
    native = load(S / "execution-596.json")["nativeAcceptance"]
    assert native["nativeAcceptancePassed"] and native["nativeSkips"] == 0
    assert len(native["caseResults"]) == 2 and all(r["status"] == 0 for r in native["caseResults"])
    assert native["route"]["contentVersion"] == VERSION
    assert {k: native["route"][k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "importedKanji": 1108, "importedWords": 5063, "n1Cards": 117, "problems": 0}
    index = R / native["artifactIndex"]
    assert sha(index) == native["artifactIndexSha256"]
    artifacts = load(index)
    assert len(artifacts) == 112
    for row in artifacts:
        path = R / row["archive"]
        assert sha(path) == row["sha256"], path
        raw = gzip.decompress(path.read_bytes()) if row["losslessGzipVerified"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"], path
    return {
        "reviewReports": reports, "nativeTerminalCases": native["caseResults"],
        "nativeArtifactHashesReverified": len(artifacts), "newNativeOrReviewerRuns": 0,
        "nativeContentVersion": VERSION, "nativeRuntimeMatchesCurrentCombinedTree": True,
        "inheritedLimits": visual["limits"],
        "rerunDisposition": "Fresh main already included; runtime, source, app production bytes, N1 pool, curated choices, readings, articles and strokes unchanged since accepted native/visual evidence. Fresh actual-combined HOST4 passed. No new native concern or substantive teaching change established; no repeated native/reviewer run.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-598.txt").read_text(encoding="utf-8-sig")
    assert re.search(r"^Ran 372 tests in ", tests, re.M) and re.search(r"^OK$", tests, re.M)
    assert not re.search(r"^FAILED", tests, re.M)
    assert (L / "validate-598.txt").read_text().strip() == "0 error(s)"
    assert VERSION in (L / "manifest-598.txt").read_text()
    assert (L / "vocabulary-598.txt").read_text().strip() == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-598.json")["exitCode"] == 0
    assert (L / "host-exit-598.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-598.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-598.txt").read_text().strip())
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
    source = load(L / "combined-source-audit-598.json")
    assert source["runtimeHashesVerified"] == 8413
    inheritance = inherited()
    budget = ast.literal_eval((L / "budget-598.txt").read_text())
    target_folder = R / "docs" / "n1-reviews" / "batch-085-combined-acceptance-598"
    assert not target_folder.exists()
    target_folder.mkdir()
    receipts = []
    for path in [
        *(L / name for name in [
            "starting-state-598.json", "combined-source-audit-598.json",
            "python-tests-598.txt", "validate-598.txt", "manifest-598.txt", "vocabulary-598.txt",
            "budget-598.txt", "host-598.txt", "host-exit-598.txt", "host-command-598.json",
            "host-start-598.txt", "host-end-598.txt", "runner-ancestry-598.json"]),
        *(L / f"{name}-exit-598.json" for name in ["python-tests", "validate", "manifest", "vocabulary", "budget"]),
        *(Path(row["path"]) for row in suites),
        Path(__file__), C / "run-batch-085-combined-host-598.ps1",
        C / "post-batch-085-combined-598.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
    ]:
        target = target_folder / (path.name + ".gz" if path.suffix == ".txt" else path.name)
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        receipts.append({"source": str(path), "archive": str(target.relative_to(R)),
                         "sourceSha256": sha(path), "sha256": sha(target),
                         "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 598, "batch": "085", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-598.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN,
        "normalMerge": True, "upstreamAlreadyAncestor": True, "mergeResult": "Already up to date.",
        "newMergeCommit": False, "conflicts": [], "substantiveTeachingConflictEdits": [],
        "batchTeachingUnchanged": True, "runtimeBytesUnchanged": True,
        "sourceAudit": source, "pythonTestsPassed": 372, "validatorErrors": 0,
        "vocabularyConsistencyPassed": True, "manifestFresh": True, "contentVersion": VERSION,
        "localBudget": budget, "hostSuites": suites, "hostChecksFresh": True, "hostTestsExecuted": 4,
        "androidHead": APP, "productionAndroidBytesUnchanged": True,
        "inheritedAcceptance": inheritance, "receipts": receipts,
        "runtimeAccepted": True, "runtimePublished": False,
        "publishedAdditions": 111, "remainingAdditions": 1117, "lastPublishedCommit": MAIN,
        "earlierLevelSourceMemberDisposition": source["separateEarlierLevelSourceMembers"],
        "earlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "diagnostics": [
            "Initial helper selected validate_grammar_vocabulary.py, a library with no command-line entry point; exit0 with empty output was not accepted as vocabulary evidence. Replaced with actual CI grammar_vocabulary.py check and verified exact expected coverage output. No gate relaxed or full-suite rerun needed.",
            "A read-only schema inspection omitted explicit UTF-8 and hit Windows cp1252 decoding; repeated that bounded inspection with UTF-8, no permission denial or state change.",
            "Initial inherited-evidence verifier assumed every visual turn had a resource acceptance field. It stopped before any repository writes on the terminal no-tool report turn. Corrected to require24 resource-accepted turns plus the final null-resource/zero-tool turn, retaining every exit/model/timing/image hash check.",
        ],
        "limits": "Combined-tree source/mechanical/fresh HOST acceptance, not public delivery or fresh linguistic/native review. Original593/594/595/596/597 source/process/read-depth/downscale/fallbackface/MLKit/phone/pool qualifications retained. Physical phone/general release/whole-set outstanding.",
    }
    save(S / "execution-598.json", evidence)
    ledger = load(S / "batch-085-progress.json")
    ledger["preCombined598State"] = {
        key: ledger.get(key) for key in ["status", "nextAction", "runtimeAccepted", "runtimePublished"]}
    ledger.update(status=STAGE, runtimeAccepted=True, runtimePublished=False,
                  combinedAcceptance="docs/n1-sources/execution-598.json", nextAction=NEXT)
    save(S / "batch-085-progress.json", ledger, ascii=False)
    body = (
        f"Batch085 checkpoint598: **latest-main integration and combined-tree acceptance passed locally; publication is next**. "
        f"Fresh public main {MAIN} is already an ancestor of reviewed local {HEAD}; normal non-rewriting merge returned "
        "'Already up to date'. No artificial merge, conflict resolution, teaching edit or repeated native/reviewer run.\n\n"
        f"Same reviewed kanji, three necessary support articles and bounded reused bullet; version {VERSION}, "
        "all8,413 runtime hashes verified,1,108kanji/5,063words/117N1labels/122named members. "
        "Fresh372Python tests, validator0errors, actual CI vocabulary consistency, regenerated fresh manifest, "
        "frozen inputs/decompression/three full lexical packet re-extractions/four raw character records, "
        "original985kanji/4942words/985strokes with recorded exceptions, exact membership, all six reading dispositions, "
        "four reciprocal pairs/eight directions,32direct guards and pinned16stroke regeneration passed. "
        f"Local budget: {budget['entries']:,}entries; {budget['retainedBytes']:,}retained, "
        f"{budget['inflatedBytes']:,}inflated, {budget['localZipBytes']:,}compressed bytes. "
        "Original18,000entries/42MiBcompressed/80MiBinflated/56MiBretained/per-file/media/safe-path guards unchanged.\n\n"
        "Fresh actual-sibling Android RealContentTest3 and RareHanTest1 executed with zero skips/errors/failures; "
        "BUILD SUCCESSFUL,41tasks executed. Exact signed TESTONLYAndroid1c1b7bf4 atop unchanged productionf9b59a2 "
        "(not latest app main), explicitJDK17/SDK/oneworker/in-processKotlin/unchanged approved2GiBHOSTinit. "
        "No app/guest heap or production app change. Original two-family textual/confirmation and dependent visual "
        "reports, actualClaudeOpus5.5/GPT6.1Sol models/sessions/serial exits/hashes/returned image payloads and112native "
        "artifacts reverified, NOT rerun. Two native terminalcase0 results remain current: productionContentSyncONCE "
        "same version/counts/zeroProblems/acceptedRoomparserEpoch1;39Han/fourfonts/threewholewords, allscopedarticles/"
        "changedbullet/fourpairs/eightdirections/SystemBack/offline/defaultfourchoices within captured scope. "
        "Three selected raw readings yield only two scheduled keys; shared-stem selection is not independent mastery. "
        "Injected16reference strokes/trace/recallgiveup are not human handwriting/MLKit/phone evidence. All original "
        "source/lookup/read-depth/compaction/downscale/fallbackface/pool/device limitations and optional dispositions retained.\n\n"
        "Evidence: docs/n1-sources/execution-598.json and docs/n1-reviews/batch-085-combined-acceptance-598 "
        "(lossless outputs, fresh non-skipped XML and durable control recipes). "
        "**Next bounded checkpoint: fresh-main recheck, normal signed owner fast-forward publication, exact remoteSHA/"
        "terminalgreenCI/EVERY immutable public ZIP runtime hash and unchanged budgets, durable publication/verified "
        "owner issue receipt before086.** No push or086 here. Published111/1228;1117remaining unchanged; "
        "six separate earlier N2 source placements are not accepted issue60 batches. Physical-phone/general-release/"
        "whole-set acceptance remains outstanding; project incomplete. Live parent19008 verified in ancestry; child "
        "never opens/reacquires/deletes/unlocks runner.lock. Approved workspace/control/committed evidence only; "
        "no optional historical-session artifact or actual new permission denial.\n"
    )
    (L / "issue-body-598.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance and lossless receipts recorded; ready for normal signed LOCAL checkpoint.")


def seal():
    path = S / "batch-085-progress.json"
    ledger = load(path)
    before = json.loads(git("show", f"{HEAD}:docs/n1-sources/batch-085-progress.json"))
    assert {k for k in before if before[k] != ledger[k]} == {"status", "nextAction"}
    assert ledger["preCombined598State"] == {
        key: before.get(key) for key in ["status", "nextAction", "runtimeAccepted", "runtimePublished"]}
    save(path, ledger, ascii=False)
    path = S / "execution-598.json"
    evidence = load(path)
    for row in evidence["receipts"]:
        if row["source"] == str(Path(__file__)):
            (R / row["archive"]).write_bytes(Path(__file__).read_bytes())
            row["sourceSha256"] = row["sha256"] = sha(Path(__file__))
    save(path, evidence)
    print("Final helper archived; original ledger Unicode formatting and historical values preserved.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-598.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["sha256"]
    receipt = load(L / "issue-verified-598.json")
    body = (L / "issue-body-598.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    before = load(L / "progress-before-598.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 597 and p["batch"] == "085"
    row = {
        "schemaVersion": 1, "execution": 598, "checkpoint": 598, "batch": "085",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-598.json", "evidenceSha256": sha(S / "execution-598.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "upstreamAlreadyAncestor": True,
        "runtimeHashesVerified": 8413, "contentVersion": VERSION, "pythonTestsPassed": 372,
        "freshHostTestsPassed": 4, "hostSkips": 0, "runtimeAccepted": True, "runtimePublished": False,
        "runtimeBytesUnchanged": True, "newNativeOrReviewerRuns": 0,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 111, "remainingAdditions": 1117, "lastPublishedCommit": MAIN,
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "issueUpdate": receipt["html_url"], "ownerIssueAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(L / "issue-verified-598.json"),
        "nextAction": NEXT, "blocker": None, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p.update(checkpoint=598, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution598CoordinatorCheckpoint"] = row
    p["batch085CombinedAcceptanceCheckpoint"] = row
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(L / "checkpoint-verification-598.json", row)
    print(f"Checkpoint598 persisted at signed {saved}; all historical root values preserved. SAME085 publication next; no086.")


if __name__ == "__main__":
    {"start": start, "audit": audit, "checks": checks, "record": record,
     "seal": seal, "finish": finish}[sys.argv[1]]()
