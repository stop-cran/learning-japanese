"""Bounded combined-main checkpoint; the live launcher owns runner.lock."""
import gzip
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "60ad0d56-a96f-42e1-a1f6-8cf1b979a255"
HEAD = "42ca66e9ff00ab495ded6cdd6051643f1c1673f8"
MAIN = "106a36dd9617a0d0826a512da82ee1ed9bf9e34d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
MERGED = "40305851ec490c698e31277d5d67386e34272bb8"
STAGE = "batch-084-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME084 bounded normal signed owner fast-forward PUBLICATION and exact public acceptance NEXT; "
    "no085 before delivery/checkpoint. Read signed execution-589.json and combined acceptance receipts. "
    "Normal nonrewriting merge40305851 has parents42ca66e9 and latestmain106a36dd; only generated "
    "manifest conflicted and was regenerated. Exact disjoint union: reviewed凜kanji/word/15stroke bytes "
    "UNCHANGED, publicmain29runtime additions+43link-only changes retained byte-for-byte; no "
    "substantive conflict resolution/new teaching authored. Combined version8c3fa3ee6f2b1ebc/"
    "8408runtimehashes/1107kanji5060words116N1/121namedmembers. Separate main11kanji includes "
    "six frozenN1members保案派第策結 placedN2 and five nonmembers; retain earlier levels, no duplicates, "
    "NOT six issue60accepted batches, issue60published110/1228 and1118acceptance-remainder unchanged. "
    "Fresh combined372Python/validate0/vocabulary/freshmanifest/budgets/source-frozen-reextraction/"
    "original985kanji4942words985strokes-with-recordedexceptions/membership/onepair20directguards/"
    "allreadings/pinnedstrokes/hash checks passed. Fresh actual-sibling HOSTRealContentTest3/"
    "RareHanTest1 no skips/failures/errors on signedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9; "
    "one worker/inherited HOSTONLYinit, no nativeheap/archiveguard increase/parentlock access. "
    "Original584blind/source+confirmation and588originalvisual/detail families ClaudeOpus5.5/GPT6.1Sol "
    "reports/models/serialexits/hashes and587two terminal0 native cases/allartifacts reverified NOT rerun. "
    "Native fullContentSyncONCE remains premergeversion74b87b47347b78c1/1096kanji5053words116N1; "
    "NOT combinedversion nativeimport. Runtime union changed only unrelated public lower-level content; "
    "N1pool/three curated choices/凜readings/articles/strokes unchanged, freshHOST imports combinedfull "
    "archive. No new native concern established; inherited glyph/routes/Back/offline/drawing bounded. "
    "Before push freshly fetch main; if advanced normallymerge/reconcile/regenerate/revalidate actual "
    "combinedtree, bounded independentreview of substantive changedteaching. Ownerstop-cran token "
    "ONLYpublicationchild; verifyidentity, normal signing/noamend/noforce/globalaccountunchanged. "
    "Verify exact remoteSHA/terminalgreen relevantCI/EVERYruntimehash+manifest in EXACTimmutableGitHubZIP "
    "and original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepathguards. "
    "Preserve authored/reviewed/integrated/publishedSHAs, counts/earlierplacements/evidence in ledgers "
    "and verifiedownerissue60 BEFORE085. No unreviewedpush. All source/denial/OOM/process/readdepth/"
    "downscale/fallbackface/bodyfine-stroke/MLKit/phone/AllUI-larger-custom-random-partial-padded-reversepool "
    "limitations from588 retained. Injectedtrace/giveup NOT humanrecognition/MLKit/phone. Physicalphone/"
    "generalrelease/whole-set outstanding, projectincomplete. Parent19008 runner.lock liveowned throughout; "
    "verify ancestry/session/checkpoint/exactsignedheads/whollycleanworktrees, never reacquire/delete/unlock. "
    "Approvedcontrol/committedsources only, no optional historicalsessionhelpers. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. No085."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value, ascii=True):
    temporary = path.with_suffix(path.suffix + ".589.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=ascii, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def start():
    for root, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    assert git("rev-parse", "origin/main") == MAIN
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 588 and progress["status"] == "continue"
    assert progress["batch"] == "084"
    before = L / "progress-before-589.json"
    assert not before.exists()
    save(before, progress)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 588
    state = {
        "execution": 589, "batch": "084", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME084 normal latest-main integration and combined-tree acceptance; signed LOCAL checkpoint before owner publication. No085, new reviewer or native run absent a changed substantive passage or new concern.",
        "request": {
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, full approved issue and final588 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": "Live parent19008 verified in coordinator ancestry; no child lock open/acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/control helpers and committed source/review packets only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-589.json", state)
    progress["execution589StartingState"] = state
    progress.update(stage="batch-084-combined-main-integration-in-progress",
                    nextAction=state["scope"], blocker=None)
    save(C / "progress.json", progress)
    old = load(before)
    assert all(progress[k] == v for k, v in old.items()
               if k not in {"stage", "nextAction", "blocker"})
    print("Starting integration scope persisted; complete live history preserved.")


def canonical(element):
    return (element.tag, element.attrib, (element.text or "").strip(),
            [canonical(child) for child in element])


def audit():
    sys.path.insert(0, str(R / "tools"))
    import audit_n1_batch
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from generate_strokes import convert

    folder = R / "docs" / "n1-sources"
    base = load(folder / "batch-084-membership.json")["baseCommit"]
    frozen = json.loads(git("show", f"{HEAD}:manifest.json"))
    upstream = json.loads(git("show", f"{MAIN}:manifest.json"))
    common = json.loads(git("show", f"{base}:manifest.json"))
    current = load(R / "manifest.json")
    assert current == build_manifest(R)

    def payload(manifest):
        return {(section, name): value
                for section, entries in manifest.items() if isinstance(entries, dict)
                for name, value in entries.items()}

    old, ours, theirs, actual = map(payload, (common, frozen, upstream, current))
    ours_changed = {key for key in old.keys() | ours.keys() if old.get(key) != ours.get(key)}
    theirs_changed = {key for key in old.keys() | theirs.keys() if old.get(key) != theirs.get(key)}
    assert not ours_changed & theirs_changed
    assert not old.keys() - ours.keys() and not old.keys() - theirs.keys()
    expected = dict(old)
    expected.update({key: ours[key] for key in ours_changed})
    expected.update({key: theirs[key] for key in theirs_changed})
    assert actual == expected
    assert len(ours_changed) == 3 and len(actual) == 8408
    original_delta = audit_n1_batch.runtime_delta

    def integrated_delta(before, after, additions, changed):
        # The unchanged strict auditor checks the frozen batch delta separately.
        original_delta(before, frozen, additions, changed)
        assert payload(after) == expected

    audit_n1_batch.runtime_delta = integrated_delta
    try:
        result = audit_n1_batch.audit(R, "084")
    finally:
        audit_n1_batch.runtime_delta = original_delta
    result["exactBaseRuntimePreservedOutsideRecordedChanges"] = False
    result["exactBaseRuntimePreservedOutsideBatchAndEnumeratedMainChanges"] = True
    result["integrationAdapter"] = (
        "Original strict runtime_delta checked base->frozen reviewed batch; then exact disjoint "
        "three-way runtime union checked base+batch+fresh main->actual generated combined manifest. "
        "All remaining original audit_n1_batch checks ran unchanged against the actual combined tree."
    )
    result["mainRuntimeAdditions"] = sorted(key[1] for key in theirs.keys() - old.keys())
    result["mainRuntimeChanges"] = sorted(key[1] for key in old.keys() & theirs.keys()
                                          if old[key] != theirs[key])
    assert len(result["mainRuntimeAdditions"]) == 29
    assert len(result["mainRuntimeChanges"]) == 43
    for section, name in theirs_changed:
        raw = subprocess.check_output(["git", "show", f"{MAIN}:{name}"], cwd=R)
        assert (R / name).read_bytes().replace(b"\r\n", b"\n") == raw.replace(b"\r\n", b"\n")
    assert not git("diff", HEAD, "--", "tools", "kanji/凜.md", "words/凜.md", "strokes/凜.json")
    freeze = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in freeze["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == info["sha256"]
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    assert hashlib.sha256(gzip.decompress(dictionary)).hexdigest() == freeze["jmdict"]["xmlSha256"]
    kd_raw = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(kd_raw).hexdigest() == freeze["kanjidic2"]["xmlSha256"]
    ledger = load(folder / "batch-084-progress.json")
    assert ledger["reviewClosed"] == ["凜"] and ledger["published"] == []
    packets = []
    for packet in ledger["dictionaryPackets"]:
        ids = load(folder / packet["selection"])["entryIds"]
        extracted = extract(dictionary, freeze["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert (folder / packet["xml"]).read_bytes() == extracted
        packets.append({"path": packet["xml"], "families": len(ids),
                        "freshFrozenExtractionMatches": True})
    kd = ET.fromstring(kd_raw)
    records = {row.findtext("literal"): row for row in kd.findall("character")}
    occurrences = 0
    for path in folder.glob("batch-084*kanjidic2.xml"):
        packet = ET.parse(path).getroot()
        assert canonical(packet.find("header")) == canonical(kd.find("header"))
        for row in packet.findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            occurrences += 1
    baseline = load(folder / "baseline-inventory.json")
    prior = load(folder / "batch-084-draft-audit.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            target = dict(info["metadata"])
            if name in prior["baselineMetadataExceptions"]:
                target["quiz_exclusions"] = prior["baselineMetadataExceptions"][name]
            if name in prior["baselineKanjiDistractorException"]:
                target["distractors"] = prior["baselineKanjiDistractorException"][name]
            assert metadata(R, name) == target, name
            counts[kind] += 1
        elif kind == "strokes":
            assert hashlib.sha256((R / name).read_bytes()).hexdigest() == info["sha256"]
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in folder.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    previous = {Path(name).stem for name in baseline["files"] if name.startswith("kanji/")}
    chars = {path.stem for path in (R / "kanji").glob("*.md")}
    supplement = load(R / "docs" / "n3-n2-supplement-sources.json")
    incoming = {row["kanji"] for row in supplement["cards"]}
    earlier = set(supplement["n1Coordination"]["sourceMembersPlacedN2"])
    assert len(published) == 110 and len(incoming) == 11 and len(earlier) == 6
    assert chars - previous == published | {"凜"} | incoming
    named = set(load(C / "inputs" / "n1-kanji-source-20261102.json"))
    assert incoming & named == earlier and earlier == set("保案派第策結")
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 2 for char in earlier)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    actual_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & named),
    }
    assert actual_counts == {"kanji": 1107, "words": 5060, "n1Labels": 116,
                             "namedSourceMembersPresent": 121}
    pairs = {(char, row["article"]) for row in ledger["supportMappings"]
             for char in metadata(R, row["article"])["kanji"]
             if (R / "kanji" / (char + ".md")).exists()}
    assert pairs == {tuple(pair) for pair in ledger["allMappedReciprocalPairs"]}
    assert pairs == {("凜", "words/凜.md")}
    declared = {f"words/{path.name}" for path in (R / "words").glob("*.md")
                if "凜" in metadata(R, f"words/{path.name}")["kanji"]}
    assert declared == {"words/凜.md"}
    guards = {tuple(sorted((row["word"], other)))
              for row in ledger["wordQuizAudit"]["directExclusions"] for other in row["exclude"]}
    assert len(guards) == 20
    stroke = load(folder / "batch-084-stroke-evidence.json")
    svg = (folder / "batch-084-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(
        b"\r\n", b"\n")).hexdigest() == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "凜.json") == convert("凜", svg.decode("utf-8"))
    binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    for (section, name), expected_hash in actual.items():
        measured = (hashlib.sha256((R / name).read_bytes()).hexdigest()
                    if section in binary else sha256(R / name))
        assert measured == expected_hash, name
    result.update(
        execution=589, latestMain=MAIN, preIntegrationHead=HEAD,
        manifestFresh=True, runtimeHashesVerified=len(actual),
        frozenInputsVerified=len(freeze["inputs"]), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterOccurrencesVerified=occurrences,
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=prior["baselineMetadataExceptions"],
        baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
        exactMembershipAccounted=True, currentCounts=actual_counts,
        publishedIssue60Additions=110, acceptedUnpublishedIssue60Additions=["凜"],
        separateEarlierLevelSourceMembers=sorted(earlier), separateNonmemberAdditions=sorted(incoming - named),
        remainingIssue60Acceptance=1118, sixEarlierPlacementsCountedAsIssue60Accepted=False,
        requiredAllMappedPairs=len(pairs), directWordExclusionPairs=len(guards),
        pinnedStrokeGeometryExactlyRegenerated=True, runtimePublished=False,
        limits="Mechanical combined-union/source/baseline/link/reading/hash audit, not a new linguistic review. Incoming main teaching is byte-identical to public main, not independently re-reviewed here; six earlier placements are not accepted issue60 batches. Original native envelope has old total/version and is not a native import of this combined version.",
    )
    save(L / "combined-source-audit-589.json", result)
    print("Combined exact-union/source audit passed;8408 hashes,1107kanji/5060words/116N1, six separate earlier placements accounted.")


def inherited():
    folder = R / "docs" / "n1-reviews"
    text = load(folder / "batch-084-reconciliation.json")
    visual = load(folder / "batch-084-visual-reconciliation.json")
    assert text["textualReviewClosed"] and visual["independentVisualAcceptance"]
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedScopedClaims"] == 0
    reports = []
    for group in [text["processes"], visual["processes"]]:
        previous = None
        for label, process in group.items():
            path = folder / process["execution"]
            row = load(path)
            model = "claude-opus-5.5" if "claude" in label else "gpt-6.1-sol"
            assert row["actualModels"] == process["actualModels"] == [model]
            assert row["exitCode"] == 0
            assert sha(folder / process["report"]) == process["reportSha256"]
            raw = C / f"batch-084-{label}.jsonl"
            assert sha(raw) == process["rawExecutionSha256"]
            if previous is not None:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(row["startedAt"])
            previous = row["completedAt"]
            for index, turn in enumerate(row.get("turns", [])):
                assert turn["exitCode"] == 0 and turn["singleResourceAccepted"]
                if index:
                    assert datetime.fromisoformat(row["turns"][index - 1]["completedAt"]) < datetime.fromisoformat(turn["startedAt"])
                if "imagePayload" in turn:
                    image = turn["imagePayload"]
                    assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                    source = Path(turn["resource"])
                    assert source.is_relative_to(R) and sha(source) == image["sourceSha256"]
            reports.append({"report": process["report"], "reportSha256": process["reportSha256"],
                            "actualModels": [model], "sessionId": row["sessionId"],
                            "exitCode": 0, "serialTimingReverified": True, "rerun": False})
    native = load(R / "docs" / "n1-sources" / "execution-587.json")["nativeAcceptance"]
    assert native["nativeAcceptancePassed"] and native["nativeSkips"] == 0
    assert len(native["caseResults"]) == 2 and all(r["status"] == 0 for r in native["caseResults"])
    index = R / native["artifactIndex"]
    assert sha(index) == native["artifactIndexSha256"]
    artifacts = load(index)
    for row in artifacts:
        path = R / row["archive"]
        assert sha(path) == row["sha256"], path
        raw = gzip.decompress(path.read_bytes()) if row["losslessGzipVerified"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    return {
        "reviewReports": reports, "nativeTerminalCases": native["caseResults"],
        "nativeArtifactHashesReverified": len(artifacts), "newNativeOrReviewerRuns": 0,
        "premergeNativeContentVersion": native["route"]["contentVersion"],
        "premergeNativeCounts": {k: native["route"][k] for k in ["importedKanji", "importedWords", "n1Cards"]},
        "combinedVersionNativeImportClaimed": False, "inheritedLimits": visual["limits"],
        "rerunDisposition": "Public-main changes are disjoint, lower-level cards/links. Batch teaching, readings, three curated labels, N1 pool and routes unchanged; fresh actual-combined full-archive HOST checks pass. No new native concern established. Inherited emulator import totals/version remain premerge, not certified as combined-version native import.",
    }


def record():
    clean(R, MERGED)
    clean(A, APP)
    assert git("show", "-s", "--format=%P", MERGED) == f"{HEAD} {MAIN}"
    assert git("rev-parse", "origin/main") == MAIN
    tests = (L / "python-tests-589.txt").read_text(encoding="utf-8-sig")
    assert (L / "python-tests-exit-589.txt").read_text().strip() == "0"
    assert re.search(r"^Ran 372 tests in ", tests, re.M) and re.search(r"^OK$", tests, re.M)
    assert not re.search(r"^FAILED", tests, re.M)
    assert (L / "validate-589.txt").read_text().strip() == "0 error(s)"
    assert "8c3fa3ee6f2b1ebc" in (L / "manifest-fresh-589.txt").read_text()
    assert (L / "vocabulary-589.txt").read_text().strip() == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    assert (L / "host-exit-589.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-589.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-589.txt").read_text().strip())
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
    source = load(L / "combined-source-audit-589.json")
    assert source["runtimeHashesVerified"] == 8408
    inheritance = inherited()
    target_folder = R / "docs" / "n1-reviews" / "batch-084-combined-acceptance-589"
    assert not target_folder.exists()
    target_folder.mkdir()
    receipts = []
    for path in [
        *(L / name for name in [
            "starting-state-589.json", "combined-source-audit-589.json", "python-tests-589.txt",
            "python-tests-exit-589.txt", "validate-589.txt", "manifest-589.txt",
            "manifest-fresh-589.txt", "vocabulary-589.txt", "budget-589.txt",
            "host-589.txt", "host-exit-589.txt", "host-command-589.json",
            "host-start-589.txt", "host-end-589.txt", "runner-ancestry-589.json"]),
        *(Path(row["path"]) for row in suites),
        Path(__file__), C / "run-batch-084-combined-host-589.ps1",
        C / "post-batch-084-combined-589.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
    ]:
        target = target_folder / (path.name + ".gz" if path.suffix == ".txt" else path.name)
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        receipts.append({"source": str(path), "archive": str(target.relative_to(R)),
                         "sourceSha256": sha(path), "sha256": sha(target),
                         "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 589, "batch": "084", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-589.json"),
        "combinedContentHead": MERGED, "latestMainIntegrated": MAIN,
        "mergeParents": [HEAD, MAIN], "normalMerge": True,
        "conflicts": ["manifest.json"], "resolution": "Regenerated actual combined manifest; no stale-side selection.",
        "substantiveTeachingConflictEdits": [], "batchTeachingUnchanged": True,
        "sourceAudit": source, "pythonTestsPassed": 372, "validatorErrors": 0,
        "vocabularyConsistencyPassed": True, "manifestFresh": True,
        "budgetOutput": (L / "budget-589.txt").read_text().strip(),
        "hostSuites": suites, "hostChecksFresh": True, "hostTestsExecuted": 4,
        "androidHead": APP, "productionAndroidBytesUnchanged": True,
        "inheritedAcceptance": inheritance, "receipts": receipts,
        "runtimeAccepted": True, "runtimePublished": False,
        "runtimeBytesChangedOnlyByEnumeratedPublicMainUnion": True,
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": "73b19c3eafb75721add6c8e333a1c3bef9e960d7",
        "earlierLevelSourceMemberDisposition": source["separateEarlierLevelSourceMembers"],
        "earlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Combined-tree source/mechanical/HOST acceptance, not public delivery, fresh linguistic/native review, or combined-version native import. Incoming public-main teaching preserved byte-for-byte, not independently re-reviewed here. All original584/585/586/587/588 source/process/read-depth/downscale/fallbackface/MLKit/phone/pool qualifications retained. Physical phone/general release/whole-set outstanding.",
    }
    save(R / "docs" / "n1-sources" / "execution-589.json", evidence)
    for path in [R / "docs" / "n1-sources" / "batch-084-progress.json",
                 R / "docs" / "n1-reviews" / "batch-084-reconciliation.json"]:
        value = load(path)
        value["preCombined589Status"] = value["status"]
        value.update(status=STAGE, runtimeAccepted=True, runtimePublished=False,
                     combinedAcceptance="docs/n1-sources/execution-589.json")
        save(path, value, ascii=path.name != "batch-084-reconciliation.json")
    print("Combined acceptance and lossless receipts recorded; ready for normal signed LOCAL evidence checkpoint.")


def finish():
    clean(A, APP)
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == MERGED
    assert not git("diff", MERGED, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    before = load(L / "progress-before-589.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 588 and progress["batch"] == "084"
    receipt = load(C / "batch-084-combined-589-issue-verified.json")
    body = (C / "batch-084-combined-589-issue.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
    row = {
        "schemaVersion": 1, "execution": 589, "checkpoint": 589, "batch": "084",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-589.json",
        "evidenceSha256": sha(R / "docs" / "n1-sources" / "execution-589.json"),
        "combinedContentHead": MERGED, "latestMainIntegrated": MAIN,
        "runtimeHashesVerified": 8408, "contentVersion": "8c3fa3ee6f2b1ebc",
        "pythonTestsPassed": 372, "freshHostTestsPassed": 4, "hostSkips": 0,
        "runtimeAccepted": True, "runtimePublished": False, "newNativeOrReviewerRuns": 0,
        "separateEarlierPlacementsCountedAsIssue60Accepted": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": "73b19c3eafb75721add6c8e333a1c3bef9e960d7",
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "issueUpdate": receipt["html_url"], "ownerIssueAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(C / "batch-084-combined-589-issue-verified.json"),
        "nextAction": NEXT, "blocker": None,
        "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    progress.update(checkpoint=589, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    progress["execution589CoordinatorCheckpoint"] = row
    progress["batch084CombinedAcceptanceCheckpoint"] = row
    progress["batch084CombinedIssueReceipt589"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "localSignedEvidenceCommit": saved, "runtimePublished": False,
        "receiptSha256": row["issueReceiptSha256"], "globalAccountUnchanged": True,
    }
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[key] == value for key, value in before.items() if key not in changed)
    save(C / "progress.json", progress)
    assert load(C / "progress.json") == progress
    save(L / "checkpoint-verification-589.json", row)
    print(f"Checkpoint589 persisted at signed {saved}; all historical root values preserved. SAME084 publication next, no085.")


def finalize_recipes():
    path = R / "docs" / "n1-sources" / "execution-589.json"
    evidence = load(path)
    for row in evidence["receipts"]:
        if row["source"] == str(Path(__file__)):
            (R / row["archive"]).write_bytes(Path(__file__).read_bytes())
            row["sourceSha256"] = row["sha256"] = sha(Path(__file__))
    save(path, evidence)
    path = R / "docs" / "n1-reviews" / "batch-084-reconciliation.json"
    save(path, load(path), ascii=False)
    for name in ["docs/n1-reviews/batch-084-reconciliation.json",
                 "docs/n1-sources/batch-084-progress.json"]:
        before = json.loads(git("show", f"{MERGED}:{name}"))
        after = load(R / name)
        assert all(before[k] == after[k] for k in before if k != "status")
    print("Final control recipe archived; original ledger Unicode formatting and historical values preserved.")


if __name__ == "__main__":
    {"start": start, "audit": audit, "record": record, "finish": finish,
     "finalize-recipes": finalize_recipes}[sys.argv[1]]()
