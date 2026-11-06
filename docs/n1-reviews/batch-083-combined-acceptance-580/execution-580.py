import hashlib
import gzip
import json
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
LOG = C / "logs" / "94a69f58-a6ed-411f-b1bc-90b6e47ccb68"
HEAD = "a70c9deb565e696772342675c2a9c99b09967e8a"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
MAIN = "21a5cb1328aadd437139a6b850f07298a2e2985d"
BEFORE = LOG / "progress-before-580.json"
STAGE = "batch-083-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME083 normally signed owner fast-forward publication and public acceptance NEXT; no084 before "
    "verified delivery. Read signed execution-580.json and combined source/HOST receipts. Fresh origin/main "
    "21a5cb1328aadd437139a6b850f07298a2e2985d normal merge was already up to date; all reviewed runtime "
    "bytes unchanged at version6dfe6a1e287ce5df/8376hashes. Combined372Python tests, validate0errors, "
    "vocabulary consistency, manifest freshness/budgets, baseline985/4942/985 with inherited narrow "
    "exceptions, exact membership109published plus accepted-unpublished凌,17directguards/twopairs/"
    "tworeadings/pinnedstrokes/frozenpacket re-extraction passed. Fresh actual-sibling HOST RealContentTest3 "
    "and RareHanTest1 passed with no skips/errors/failures under signed TESTONLYAndroid1c1b7bf4 atop "
    "unchangedproductionf9; one worker/inherited host-only init, no native heap/guard increase or lock access. "
    "Both original initial/choice/visual reports and corrected578 two terminal0 native cases/artifacts "
    "reverified, not rerun; original574failure immutable and all579limitations retained. No changed teaching "
    "or new concern requiring fresh independent/native review. Before push freshly fetch main; if it advanced "
    "normal merge/reconcile/regenerate/combined revalidation and bounded independent review of any substantive "
    "changed teaching. Owner stop-cran token ONLY publication child, verify identity, normal signing/noamend/"
    "noforce/globalaccountunchanged. Then verify exact remoteSHA/terminalgreen relevantCI/EVERY runtime "
    "hash and manifest in EXACT immutableGitHubZIP plus original18000entries/42MiBcompressed/80MiBinflated/"
    "56MiBretained/perfile/media/pathguards. Prior local native archive verified but NOT public delivery. "
    "Persist authored/reviewed/integrated/published SHAs, ledgers/counts and verifiedownerissue60 before084. "
    "Published remains109/1228,remaining1119/latestpublic21a5cb1328aadd437139a6b850f07298a2e2985d; "
    "083NOTdelivered. Physicalphone/generalrelease/whole-set outstanding. All source/reviewer/process/"
    "readdepth/viewport/fallback/MLKit/OOM/denial/AllUI/custom/random/padded/partial/larger/reversepool "
    "limitations inherited unchanged from579; injectedtrace/giveup NOT humanrecognition/MLKit/phone. "
    "Parent19008 ownsrunner.lock throughout child lifetime; never reacquire/delete/unlock. Approvedcontrol "
    "helpers and committedsources only; nooptionalhistoricalsessionhelpers. Preserve/report/yield actualnew "
    "denial/signinghang or uncertainownership, noworkaround."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "log", "-1", "--format=%G?") == "G"
    assert not git(root, "status", "--porcelain")


def persist(value):
    temporary = C / "progress.580.tmp"
    assert not temporary.exists()
    save(temporary, value)
    assert load(temporary) == value
    temporary.replace(C / "progress.json")


def start():
    clean(R, HEAD)
    clean(A, APP)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 579 and p["batch"] == "083" and p["status"] == "continue"
    assert git(R, "rev-parse", "origin/main") == MAIN
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    text = (LOG / "request.txt").read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 579
    state = {
        "execution": 580, "batch": "083", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME083 latest-main integration and combined-tree automated acceptance; local signed evidence checkpoint before publication; no084, reviewer or native rerun absent change.",
        "request": {
            "sha256": sha(LOG / "request.txt"), "characters": len(text),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Complete request loaded and checkpoint decoded; operative contract, full approved issue and final579 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": "Live parent19008 verified in coordinator ancestry; child never opens/acquires/deletes/unlocks runner.lock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    save(LOG / "starting-state-580.json", state)
    p["execution580StartingState"] = state
    p["stage"] = "batch-083-combined-main-acceptance-in-progress"
    p["nextAction"] = state["scope"]
    persist(p)
    before = load(BEFORE)
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction"})
    print("Execution580 starting scope persisted; complete historical progress preserved.")


def canonical(element):
    return (element.tag, element.attrib, (element.text or "").strip(),
            [canonical(child) for child in element])


def audit():
    clean(R, HEAD)
    clean(A, APP)
    assert git(R, "rev-parse", "origin/main") == MAIN
    assert not git(R, "diff", "7cc896f488ae5315046453777aae6768b9ff18e8", HEAD,
                   "--", "kanji", "words", "articles", "strokes", "manifest.json")
    subprocess.run(["git", "merge-base", "--is-ancestor", MAIN, HEAD], cwd=R, check=True)
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from generate_strokes import convert

    folder = R / "docs" / "n1-sources"
    result = batch_audit(R, "083")
    ledger = load(folder / "batch-083-progress.json")
    assert ledger["reviewClosed"] == ["凌"] and ledger["published"] == []
    freeze = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in freeze["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"], name
    dictionaries = {}
    for name, field in [("n1-implementation-JMdict_e.gz", "jmdict"),
                        ("n1-planning-kanjidic2.xml.gz", "kanjidic2")]:
        raw = gzip.decompress((C / "inputs" / name).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == freeze[field]["xmlSha256"]
        dictionaries[field] = ET.fromstring(raw)
    families = {e.findtext("ent_seq"): e for e in dictionaries["jmdict"].findall("entry")}
    packets = []
    for packet in ledger["dictionaryPackets"] + [
            {"selection": "batch-083-choice-selection.json", "xml": "batch-083-choice-jmdict.xml"}]:
        selection = load(folder / packet["selection"])
        ids = selection["entryIds"]
        selected = ET.Element("JMdict")
        for identity in ids:
            selected.append(families[identity])
        ET.indent(selected, space="  ")
        expected = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
        assert (folder / packet["xml"]).read_bytes() == expected
        packets.append({"path": packet["xml"], "families": len(ids),
                        "sha256": sha(folder / packet["xml"]), "freshExtractionMatches": True})
    kd = dictionaries["kanjidic2"]
    records = {e.findtext("literal"): e for e in kd.findall("character")}
    characters = 0
    for name in ["batch-083-kanjidic2.xml", "batch-083-support-kanjidic2.xml",
                 "batch-083-choice-kanjidic2.xml"]:
        selected = ET.parse(folder / name).getroot()
        assert canonical(selected.find("header")) == canonical(kd.find("header"))
        for record in selected.findall("character"):
            assert canonical(record) == canonical(records[record.findtext("literal")])
            characters += 1
    baseline = load(folder / "baseline-inventory.json")
    old_audit = load(folder / "batch-083-draft-audit.json")
    exceptions = old_audit["baselineMetadataExceptions"]
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = old_audit["baselineKanjiDistractorException"][name]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in folder.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(name).stem for name in baseline["files"] if name.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(folder / "community-list-20261102.json")
    assert len(published) == 109 and current - old == published | {"凌"}
    assert len(current) == 1095 and len(current & set(named)) == 114
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    assert sum(metadata(R, f"kanji/{p.name}")["jlpt"] == 1 for p in (R / "kanji").glob("*.md")) == 115
    assert len(list((R / "words").glob("*.md"))) == 5052
    pairs = {(c, row["article"]) for row in ledger["supportMappings"]
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {
        ("凌", "words/凌ぐ.md"), ("凌", "words/凌駕.md")}
    declared = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                if "凌" in metadata(R, f"words/{p.name}")["kanji"]}
    assert declared == {"words/凌ぐ.md", "words/凌駕.md"}
    guards = set()
    for row in ledger["wordQuizAudit"]["directExclusions"]:
        assert metadata(R, f"words/{row['word']}.md")["quiz_exclusions"] == row["exclude"]
        guards.update(tuple(sorted((row["word"], other))) for other in row["exclude"])
    assert len(guards) == 17
    source = load(folder / "batch-083-stroke-evidence.json")
    svg = Path(source["input"]).read_bytes()
    assert hashlib.sha256(svg).hexdigest() == source["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == source["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(
        b"\r\n", b"\n")).hexdigest() == source["converterNormalizedSha256"]
    assert load(R / "strokes" / "凌.json") == convert("凌", svg.decode("utf-8"))
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R) and manifest["contentVersion"] == "6dfe6a1e287ce5df"
    binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    verified = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                assert (sha(R / name) if section in binary else sha256(R / name)) == expected, name
                verified += 1
    assert verified == 8376
    preparation = load(folder / "execution-577.json")["fixtureVerification"]
    archive = Path(preparation["archive"])
    assert sha(archive) == preparation["archiveSha256"]
    with zipfile.ZipFile(archive) as z:
        root = z.namelist()[0].split("/")[0] + "/"
        assert json.loads(z.read(root + "manifest.json")) == manifest
        for section, entries in manifest.items():
            if isinstance(entries, dict):
                for name, expected in entries.items():
                    payload = z.read(root + name)
                    if section not in binary:
                        payload = payload.replace(b"\r\n", b"\n")
                    assert hashlib.sha256(payload).hexdigest() == expected, name
        assert len(z.infolist()) == 8398 < 18000 and archive.stat().st_size < 42 * 1024**2
        assert sum(i.file_size for i in z.infolist()) == preparation["inflatedBytes"] < 80 * 1024**2
        assert preparation["retainedBytes"] < 56 * 1024**2
    result.update(
        execution=580, integration={"latestMain": MAIN, "combinedHead": HEAD,
                                   "normalMergeResult": "Already up to date.", "teachingChanged": False},
        frozenInputsVerified=5, decompressedDictionaryHashesVerified=2,
        freshPacketExtractions=packets, completeRawCharacterOccurrencesVerified=characters,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException=old_audit["baselineKanjiDistractorException"],
        exactMembershipPreserved=True, publishedAdditions=109, acceptedUnpublishedAdditions=["凌"],
        requiredAllMappedPairs=2, activatedBaselinePairs=0, directWordExclusionPairs=17,
        runtimeHashesVerified=verified, pinnedStrokeGeometryExactlyRegenerated=True,
        acceptedNativeArchive={"path": str(archive), "sha256": sha(archive),
                              "everyRuntimeHashVerified": verified, "manifestEqualToCombinedTree": True,
                              "entries": 8398, "compressedBytes": archive.stat().st_size,
                              "inflatedBytes": preparation["inflatedBytes"],
                              "retainedBytes": preparation["retainedBytes"],
                              "publicImmutableZip": False},
        freshLinguisticReviewClaimed=False, runtimePublished=False,
        limits="Fresh mechanical source/baseline/reading/link/guard/stroke/archive audit, not fresh linguistic or native review. Prior independent source and corrected native/visual evidence retained; exact public immutable ZIP remains required.",
    )
    save(LOG / "combined-source-audit-580.json", result)
    print("Combined source audit passed: baseline985/4942/985,17guards,2pairs,8376runtimehashes; four frozen lexical packets and12 raw character occurrences reverified.")


def inherited_acceptance():
    folder = R / "docs" / "n1-reviews"
    initial = load(folder / "batch-083-reconciliation.json")
    visual = load(folder / "batch-083-visual-reconciliation.json")
    assert initial["textualReviewClosed"] and initial["runtimeAccepted"]
    assert visual["independentVisualAcceptance"] and visual["actionableRemainingFindings"] == 0
    reports = []
    for kind in ["initial", "choice", "visual"]:
        previous = None
        for family, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
            stem = f"batch-083-{kind}-{family}"
            row = load(folder / f"{stem}-execution.json")
            assert row["actualModels"] == [model] and row["exitCode"] == 0
            assert sha(folder / f"{stem}.md") == row["reportSha256"]
            raw = C / f"{stem}.jsonl"
            assert sha(raw) == row["rawExecutionSha256"]
            if previous:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(row["startedAt"])
            previous = row["completedAt"]
            if kind == "visual":
                assert len(row["turns"]) == 33 and row["completePacketReturned"]
                for i, turn in enumerate(row["turns"]):
                    assert turn["singleResourceAccepted"] and turn["exitCode"] == 0
                    if i:
                        assert datetime.fromisoformat(row["turns"][i-1]["completedAt"]) < datetime.fromisoformat(turn["startedAt"])
                    if "imagePayload" in turn:
                        image = turn["imagePayload"]
                        assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                        resource = Path(turn["resource"])
                        assert resource.is_relative_to(R)
                        assert sha(resource) == image["sourceSha256"]
            reports.append({"kind": kind, "family": family, "model": model,
                            "sessionId": row["sessionId"], "report": f"{stem}.md",
                            "reportSha256": row["reportSha256"], "rawExecutionSha256": sha(raw),
                            "exitCode": 0, "reverifiedNotRerun": True})
    native = load(R / "docs" / "n1-sources" / "execution-578.json")["nativeAcceptance"]
    assert native["nativeAcceptancePassed"]
    cases = native["independentlyParsedTerminalCases"]
    assert len(cases) == 2 and all(case["status"] == 0 for case in cases)
    index = R / native["artifactIndex"]
    assert sha(index) == native["artifactIndexSha256"]
    artifacts = load(index)
    for row in artifacts:
        path = R / row["archive"]
        assert sha(path) == row["sha256"]
        raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzipVerified") else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
        assert path.stat().st_size == row["bytes"]
    return {"reviewReports": reports, "nativeTerminalCases": cases,
            "correctedNativeArtifactHashesReverified": len(artifacts),
            "nativeAndIndependentVisualRerun": False,
            "inheritedLimits": visual["limits"]}


def record():
    clean(R, HEAD)
    clean(A, APP)
    result = load(LOG / "combined-source-audit-580.json")
    assert result["runtimeHashesVerified"] == 8376
    assert (LOG / "python-tests-exit-580.txt").read_text().strip() == "0"
    tests = (LOG / "python-tests-580.txt").read_text(encoding="utf-8-sig")
    assert "Ran 372 tests" in tests and tests.rstrip().endswith("OK") and "FAILED" not in tests
    assert (LOG / "validate-580.txt").read_text().strip() == "0 error(s)"
    assert "6dfe6a1e287ce5df" in (LOG / "manifest-580.txt").read_text()
    assert (LOG / "vocabulary-580.txt").read_text().strip() == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    assert (LOG / "host-exit-580.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in (LOG / "host-580.txt").read_text(encoding="utf-8-sig")
    host_start = datetime.fromisoformat((LOG / "host-start-580.txt").read_text().strip())
    suites = []
    for relative, count in [
            ("core\\build\\test-results\\test\\TEST-io.github.stopcran.kanji.core.RealContentTest.xml", 3),
            ("app\\build\\test-results\\testDebugUnitTest\\TEST-io.github.stopcran.kanji.core.RareHanTest.xml", 1)]:
        path = A / relative
        xml = ET.parse(path).getroot()
        assert xml.attrib["tests"] == str(count)
        assert all(xml.attrib[key] == "0" for key in ["skipped", "errors", "failures"])
        assert len(xml.findall("testcase")) == count
        assert not xml.findall(".//skipped") and not xml.findall(".//failure") and not xml.findall(".//error")
        assert datetime.fromisoformat(xml.attrib["timestamp"]).astimezone(timezone.utc) >= host_start.astimezone(timezone.utc)
        suites.append({"path": str(path), "sha256": sha(path), "suite": xml.attrib,
                       "cases": [case.attrib for case in xml.findall("testcase")]})
    inherited = inherited_acceptance()
    assert not git(A, "diff", "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", APP,
                   "--", "app/src/main", "core/src/main", "gradle.properties")
    receipts = R / "docs" / "n1-reviews" / "batch-083-combined-acceptance-580"
    assert not receipts.exists()
    receipts.mkdir()
    archives = []
    for path in [
            *(LOG / name for name in [
                "python-tests-580.txt", "python-tests-exit-580.txt", "validate-580.txt",
                "manifest-580.txt", "vocabulary-580.txt", "budget-580.txt", "batch-audit-580.txt",
                "combined-source-audit-580.json", "host-580.txt", "host-exit-580.txt",
                "host-command-580.json", "host-start-580.txt", "host-end-580.txt",
                "runner-ancestry-580.json"]),
            *(Path(suite["path"]) for suite in suites),
            Path(__file__), C / "run-580-host.ps1", C / "batch-065-host-integration-heap.init.gradle",
            C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt"]:
        target = receipts / (path.name + ".gz" if path.suffix == ".txt" else path.name)
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        archives.append({"source": str(path), "archive": str(target.relative_to(R)),
                         "sourceSha256": sha(path), "sha256": sha(target),
                         "bytes": len(raw), "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 580, "batch": "083", "status": "continue",
        "stage": STAGE, "startingState": load(LOG / "starting-state-580.json"),
        "combinedContentHead": HEAD, "freshOriginMain": MAIN,
        "normalMergeResult": "Already up to date.", "substantiveTeachingChanges": [],
        "sourceAudit": result, "pythonTests": {"executed": 372, "passed": True},
        "validatorErrors": 0, "manifestFresh": True, "vocabularyConsistencyPassed": True,
        "budgetOutput": (LOG / "budget-580.txt").read_text().strip(),
        "hostSuites": suites, "hostChecksFresh": True, "hostTestsExecuted": 4,
        "androidHead": APP, "androidProductionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "productionAndroidBytesUnchanged": True, "inheritedAcceptance": inherited,
        "receipts": archives, "runtimeAccepted": True, "runtimePublished": False,
        "runtimeBytesUnchanged": True, "newNativeOrReviewerRuns": 0,
        "publishedAdditions": 109, "remainingAdditions": 1119, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "inheritedNextAction579": load(R / "docs" / "n1-sources" / "execution-579.json")["nextAction"],
        "nextAction": NEXT,
        "limits": "Combined-tree mechanical/HOST acceptance, not public delivery or fresh linguistic/native review. Original initial/choice/visual reports and failed574/corrected578 evidence preserved. All579 source/process/readdepth/viewport/fallback/MLKit/OOM/denial and pool-scope limitations remain; phone/general-release/whole-set outstanding.",
    }
    save(R / "docs" / "n1-sources" / "execution-580.json", evidence)
    for path in [R / "docs" / "n1-sources" / "batch-083-progress.json",
                 R / "docs" / "n1-reviews" / "batch-083-reconciliation.json"]:
        ledger = load(path)
        ledger["preCombined580Status"] = ledger["status"]
        ledger.update(status=STAGE, runtimeAccepted=True, runtimePublished=False,
                      combinedAcceptance="docs/n1-sources/execution-580.json")
        save(path, ledger)
    print("Combined acceptance evidence and lossless receipts persisted; ready for normal signed local checkpoint.")


def finish():
    clean(A, APP)
    saved = git(R, "rev-parse", "HEAD")
    clean(R, saved)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    assert not git(R, "diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    before = load(BEFORE)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 579 and p["batch"] == "083"
    evidence_path = R / "docs" / "n1-sources" / "execution-580.json"
    row = {
        "schemaVersion": 1, "execution": 580, "checkpoint": 580, "batch": "083",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-580.json", "evidenceSha256": sha(evidence_path),
        "combinedContentHead": HEAD, "latestMain": MAIN, "normalMergeResult": "Already up to date.",
        "pythonTestsPassed": 372, "freshHostTestsPassed": 4, "hostSkips": 0,
        "runtimeHashesVerified": 8376, "directWordExclusionPairs": 17,
        "originalBaselinePreserved": True, "runtimeBytesUnchanged": True,
        "runtimeAccepted": True, "runtimePublished": False, "newNativeOrReviewerRuns": 0,
        "publishedAdditions": 109, "remainingAdditions": 1119, "lastPublishedCommit": MAIN,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    receipt = load(C / "batch-083-combined-580-issue-verified.json")
    body = (C / "batch-083-combined-580-issue.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
    row["issueUpdate"] = receipt["html_url"]
    row["ownerIssueAuthorAndBodyVerified"] = True
    p.update(checkpoint=580, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution580CoordinatorCheckpoint"] = row
    p["batch083CombinedAcceptance"] = row
    p["batch083CombinedIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "localSignedEvidenceCommit": saved, "runtimePublished": False,
        "receiptSha256": sha(C / "batch-083-combined-580-issue-verified.json"),
        "globalAccountUnchanged": True,
    }
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[key] == value for key, value in before.items() if key not in changed)
    persist(p)
    assert load(C / "progress.json") == p
    save(LOG / "checkpoint-verification-580.json", row)
    print(f"Checkpoint580 persisted at signed {saved}; every original historical root value preserved. Batch083 unpublished; next owner-publication gate.")


def finalize_recipes():
    path = R / "docs" / "n1-sources" / "execution-580.json"
    evidence = load(path)
    folder = R / "docs" / "n1-reviews" / "batch-083-combined-acceptance-580"
    for source in [Path(__file__), C / "post-580-issue.ps1"]:
        target = folder / source.name
        target.write_bytes(source.read_bytes())
        row = {"source": str(source), "archive": str(target.relative_to(R)),
               "sourceSha256": sha(source), "sha256": sha(target),
               "bytes": source.stat().st_size, "losslessGzip": False}
        evidence["receipts"] = [r for r in evidence["receipts"] if r["source"] != str(source)] + [row]
    evidence["coordinatorReceiptDiagnostics"] = [
        "Local receipt verification initially compared aware XML timestamps with a naive value; corrected to compare UTC instants. No test rerun or result mutation.",
        "Initial native artifact check treated index bytes as decompressed bytes. Inspection confirmed bytes records stored archive length; corrected stored length and independently verified decompressed source SHA. Original index unchanged.",
    ]
    save(path, evidence)
    print("Final durable control recipes and receipt diagnostics archived.")


if __name__ == "__main__":
    {"start": start, "audit": audit, "record": record, "finish": finish,
     "finalize-recipes": finalize_recipes}[sys.argv[1]]()
