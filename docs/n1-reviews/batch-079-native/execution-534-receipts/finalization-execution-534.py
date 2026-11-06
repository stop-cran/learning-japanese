import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOGS = CONTROL / "logs" / "7019b461-4e10-4de2-b113-4e400347cc06"
HEAD = "7b40b263ec555cf8b5996a224f6c730b714a5ecc"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-079-native"
ATTEMPT = CONTROL / "artifacts" / "batch-079-native-attempt-1"
NEXT = (
    "SAME079 bounded two SERIAL original-family independent VISUAL confirmations ONLY, "
    "then persist/yield; no publication,080 or second runner. Read docs\\n1-sources\\execution-534.json, "
    "docs\\n1-reviews\\batch-079-native\\visual-inspection-execution-534.json and preserved attempt-1 "
    "native PNGs/receipts. Fresh534 native TWO cases terminal0/no skips on owned read-only "
    "API35 emulator-5580 parent2004/qemu6712, both stopped; owner5556 untouched. "
    "Production ContentSync full signed3fdc0bf9 archive ONCE:1091kanji5047words111N1/"
    "contentVersiona01eb85b17601ac0/zeroProblems/acceptedepoch1; Full+Lite full and curated "
    "カン,かんむり, offeredかん/かんむり; threepairs/sixdirections, complete冠/王冠/reused冠 "
    "and changed王 passage, N1selection/meaning/bothreadings/ninestroke trace then giveuprecall/"
    "systemBack/offline all native asserted. 57originalPNG/29distinctbytegroups directly "
    "coordinator-inspected; all35Han in fourproductionfamilies and exact冖/宀 distinct in "
    "threeactualComposepanels.140individual+8wholeword nativePaint ASSERTION/hash records, "
    "not148separatePNGvisualreads; referencebitmaps recycled. Horizontal table navigation "
    "shows both complete reading examples over different states; no single-frameallcolumns "
    "claim. Offline handwritingmodel unavailable, injected reference trace/shape-only "
    "comparison/giveuprecall NOT handwritingrecognition/humanmemory/physicalphone. "
    "Required visual reviewers use original ClaudeOpus5.5/GPT6.1Sol sessions where possible; "
    "inspect actual PNGs/route evidence, retain actualmodels/readlimits/process exit, at mostONE "
    "active reviewer and no snapshot edits. Freeze new evidence at recorded signed local HEAD; "
    "textualclosure084d5301 and fresh532 HOST3+1 inherited honestly, no rerun absentnewconcern. "
    "All177distinctfamilies/fiverawrecords/source/review/read-depth/process/denial/OOM/phone "
    "limits and baseline exceptions retained. Durablecontrolhelpers and committedpackets/"
    "approvedinputs ONLY; optional historicalsession recipes NOT required. "
    "HOST-only2GiBinit NEVER native; no app/guestheap/archiveguard change. Later currentmain "
    "non-rewritingintegration/revalidation/normalsigning/ownerfastforward/greenCI/"
    "EVERYimmutableZIPhash/originalbudgets/verifiedownerissue60 mandatory. "
    "No unreviewedpush/authoragents/concurrentheavywork/secondrunner/signingretry/"
    "permissionworkaround; preserve/report/yield actualnewdenials. "
    "Published105/1228,remaining1123; local106thaddition textuallyclosednativepassednotpublished. "
    "CompatibleAndroidf9b59a2+; physicalphone/generalrelease/whole-set outstanding. "
    "Overallproject incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 533 and progress["batch"] == "079"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    assert not (LOGS / "progress-before-534.json").exists()
    save(LOGS / "progress-before-534.json", progress)
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 533
    record = {
        "execution": 534, "batch": "079", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME079 bounded native execution and actual PNG inspection ONLY; no reviewer, publication,080 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and complete checkpoint parsed before implementation; operative contract, final533 and complete issue directly inspected. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
        "manifestSha256": sha(ROOT / "manifest.json"),
        "contentVersion": load(ROOT / "manifest.json")["contentVersion"],
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "executing-native-fixture",
    }
    progress["execution534StartingState"] = record
    progress["stage"] = "native-execution-in-progress"
    save(CONTROL / "progress.json", progress)
    save(LOGS / "starting-state.json", record)
    print("Starting native scope persisted; full live history retained.")


def record():
    starting = load(LOGS / "starting-state.json")
    native = load(CONTROL / "batch-079-native-attempt-1-execution.json")
    visual = load(CONTROL / "batch-079-native-visual-inspection.json")
    assert native["passed"] and native["failure"] is None
    assert native["terminalSuccessCases"] == 2 and len(native["terminalCases"]) == 2
    assert {case["class"].split(".")[-1] for case in native["terminalCases"]} == {
        "N1Batch079GlyphTest", "N1Batch079ArticleTest"}
    assert native["ownedHelperStopped"] and native["ownedQemuStopped"]
    assert not git("status", "--porcelain", cwd=ANDROID)
    assert git("rev-parse", "HEAD") == HEAD
    assert sha(ROOT / "manifest.json") == starting["manifestSha256"]
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    route = load(ATTEMPT / "n1-079-article-route.json")
    raster = load(ATTEMPT / "n1-079-font-raster.json")
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"]) == (
        1091, 5047, 111, 0)
    assert route["contentVersion"] == starting["contentVersion"]
    assert route["acceptedReadingParserEpoch"] == 1
    for key in ("fullOnyomi", "liteQuizOnyomi", "fullProjectionOnyomi", "fullProjectionQuizOnyomi"):
        assert route[key] == ["カン"], key
    for key in ("fullKunyomi", "liteQuizKunyomi", "fullProjectionKunyomi", "fullProjectionQuizKunyomi"):
        assert route[key] == ["かんむり"], key
    assert route["quizOnKeys"] == ["かん"] and route["quizKunKeys"] == ["かんむり"]
    assert route["touchInjectedReferenceStrokes"] == 9
    assert route["mappedReciprocalPairs"] == 3 and route["directedLinkTransitions"] == 6
    assert all(route[key] for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                                     "bothCuratedKindsPersistedGoodAndDone", "drawingTraceThenRecall",
                                     "drawingGradeRecordedOnNext"))
    assert len(raster["rows"]) == 148 and raster["individualGlyphProbes"] == 140
    assert raster["wholeWordRasterProbes"] == 8 and raster["panels"] == 3
    groups = defaultdict(list)
    for path in sorted(ATTEMPT.glob("*.png")):
        groups[sha(path)].append(path.name)
    assert sum(map(len, groups.values())) == 57 and len(groups) == 29
    assert set(visual["inspectedRepresentatives"]) == {names[0] for names in groups.values()}
    index = {
        "originalPngCount": 57, "distinctByteGroups": 29,
        "inspectionMethod": visual["method"],
        "groups": [{"sha256": digest, "directlyViewedRepresentative": names[0],
                    "originals": names} for digest, names in groups.items()],
    }
    save(CONTROL / "batch-079-native-image-index.json", index)
    preparation = load(ROOT / "docs" / "n1-sources" / "batch-079-native-fixture-verification.json")
    manifest = load(ROOT / "manifest.json")
    with zipfile.ZipFile(preparation["archive"]) as archive:
        assert sha(Path(preparation["archive"])) == native["archiveSha256"]
        names = archive.namelist()
        prefix = names[0]
        assert prefix.endswith("/")
        assert archive.read(prefix + "manifest.json") == (ROOT / "manifest.json").read_bytes()
        verified = 0
        for section, mapping in manifest.items():
            if not isinstance(mapping, dict):
                continue
            binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
            for relative, expected in mapping.items():
                archived = archive.read(prefix + relative)
                current = (ROOT / Path(relative)).read_bytes()
                if not binary:
                    archived = archived.replace(b"\r\n", b"\n")
                    current = current.replace(b"\r\n", b"\n")
                assert hashlib.sha256(archived).hexdigest() == expected, relative
                assert hashlib.sha256(current).hexdigest() == expected, relative
                verified += 1
    assert verified == 8363
    target = FOLDER / "attempt-1"
    assert not target.exists()
    shutil.copytree(ATTEMPT, target)
    copied = []
    for path in sorted(ATTEMPT.iterdir()):
        if path.is_file():
            destination = target / path.name
            assert sha(path) == sha(destination)
            copied.append({"path": str(destination.relative_to(ROOT)),
                           "sha256": sha(destination), "bytes": destination.stat().st_size})
    receipts = FOLDER / "execution-534-receipts"
    receipts.mkdir()
    for path in (Path(__file__), CONTROL / "run-534-native.ps1"):
        destination = receipts / path.name
        shutil.copyfile(path, destination)
        assert sha(path) == sha(destination)
        copied.append({"path": str(destination.relative_to(ROOT)), "sha256": sha(destination)})
    shutil.copyfile(CONTROL / "batch-079-native-visual-inspection.json",
                    FOLDER / "visual-inspection-execution-534.json")
    shutil.copyfile(CONTROL / "batch-079-native-image-index.json", FOLDER / "image-index-execution-534.json")
    evidence = {
        **starting, "schemaVersion": 1, "checkpoint": 534, "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmations",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "nativeExecution": native, "articleRoute": route,
        "nativeRasterRecords": {"rows": 148, "individualGlyphProbes": 140, "wholeWordRasterProbes": 8,
                               "panels": 3, "path": str((target / "n1-079-font-raster.json").relative_to(ROOT)),
                               "sha256": sha(target / "n1-079-font-raster.json")},
        "visualInspection": visual, "imageIndex": index,
        "archivedReceipts": copied, "rawAttemptsAndOriginalPngBytesPreserved": True,
        "productionSingleArchiveImport": True, "exactRuntimeHashesVerified": 8363,
        "runtimeUnchanged": True, "runtimePublished": False, "independentVisualReviewersLaunched": 0,
        "inheritedTextualReview": "084d5301d175189d6e83aa77666ae495abed6f47",
        "inheritedFreshHostChecks": "execution532: RealContentTest THREE + RareHanTest ONE, no skips",
        "publishedAdditions": 105, "remainingAdditions": 1123,
        "lastPublishedCommit": "2a6777503de6c23c2ac5582b0265dd68d224f44c",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "limits": visual["limits"],
    }
    save(ROOT / "docs" / "n1-sources" / "execution-534.json", evidence)
    print(json.dumps({"stage": evidence["stage"], "terminalCases": 2, "originalPNGs": 57,
                      "visuallyInspectedDistinctPNGs": 29, "archivedFiles": len(copied),
                      "runtimeHashesVerified": 8363}, indent=2))


def checkpoint():
    progress = load(CONTROL / "progress.json")
    original = load(LOGS / "progress-before-534.json")
    assert progress["checkpoint"] == 533 and progress["batch"] == "079"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    evidence = load(ROOT / "docs" / "n1-sources" / "execution-534.json")
    receipt = load(LOGS / "issue-response.json")
    body = (LOGS / "issue-body.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    assert "issues/60#issuecomment-" in receipt["html_url"]
    assert sha(ROOT / "manifest.json") == evidence["manifestSha256"]
    result = {
        "schemaVersion": 1, "execution": 534, "checkpoint": 534, "batch": "079",
        "savedCommit": signed, "signature": "G", "status": "continue",
        "stage": evidence["stage"], "evidence": "docs/n1-sources/execution-534.json",
        "evidenceSha256": sha(ROOT / "docs" / "n1-sources" / "execution-534.json"),
        "nativeCasesExecuted": 2, "terminalSuccessCases": 2, "skipped": 0,
        "nativePassed": True, "emulatorSerial": "emulator-5580", "parentEmulatorPid": 2004,
        "qemuPid": 6712, "ownedHelperAndQemuStopped": True, "otherOwnerEmulatorUntouched": True,
        "originalPngCount": 57, "distinctPngGroupsDirectlyInspected": 29,
        "scopeGlyphs": 35, "productionFontFamilies": 4, "actualComposePanels": 3,
        "individualNativePaintAssertions": 140, "wholeWordNativePaintAssertions": 8,
        "independentVisualReviewersLaunched": 0,
        "runtimePayloadHashesVerified": 8363, "contentVersion": evidence["contentVersion"],
        "runtimeBytesUnchanged": True, "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 105, "remainingAdditions": 1123,
        "lastPublishedCommit": evidence["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextAction": NEXT,
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "originalRootKeyCountCompared": len(original),
        "changedRootFields": ["checkpoint", "status", "stage", "nextAction", "blocker"],
    }
    progress.update(checkpoint=534, status="continue", stage=evidence["stage"], nextAction=NEXT, blocker=None)
    progress["execution534CoordinatorCheckpoint"] = result
    progress["batch079Native"] = result
    allowed = set(result["changedRootFields"])
    for key, value in original.items():
        if key not in allowed:
            assert progress[key] == value, key
    save(CONTROL / "progress.json", progress)
    saved = load(CONTROL / "progress.json")
    for key, value in original.items():
        if key not in allowed:
            assert saved[key] == value, key
    save(LOGS / "coordinator-checkpoint-534.json", result)
    print(json.dumps({"checkpoint": 534, "status": "continue", "savedCommit": signed,
                      "historicalRootKeysPreserved": len(original), "issueUpdate": receipt["html_url"]}, indent=2))


def validate_record():
    evidence_path = ROOT / "docs" / "n1-sources" / "execution-534.json"
    evidence = load(evidence_path)
    assert "0 error(s)" in (LOGS / "validate.txt").read_text()
    assert sha(ROOT / "manifest.json") == evidence["manifestSha256"]
    for name in ("validate.txt", "manifest.txt"):
        source = LOGS / name
        target = FOLDER / ("execution-534-" + name)
        assert not target.exists()
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        evidence["archivedReceipts"].append({"path": str(target.relative_to(ROOT)), "sha256": sha(target)})
    evidence["validatorErrors"] = 0
    evidence["manifestFresh"] = True
    evidence["manifestBytesUnchanged"] = True
    save(evidence_path, evidence)
    print("Fresh validator/manifest receipts saved; runtime bytes unchanged.")


def issue_body():
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    body = (
        "Batch 079 native execution checkpoint 534: **both native cases passed**, terminal status 0 "
        "for N1Batch079GlyphTest and N1Batch079ArticleTest, no skips. Evidence is saved in normally "
        f"signed LOCAL commit `{git('rev-parse', 'HEAD')}` (`docs/n1-sources/execution-534.json`). "
        "This is not content publication.\n\n"
        "The frozen complete signed 3fdc0bf9 archive was imported through production ContentSync "
        "once: 1,091 kanji, 5,047 words, 111 N1 labels, zero problems, contentVersion "
        "`a01eb85b17601ac0`, accepted reading epoch 1. Full and Lite projections retained the "
        "full/curated カン and かんむり, with offered keys かん and かんむり. Actual N1 selection, "
        "meaning, both reading kinds/persisted good logs, complete 冠/王冠/reused 冠 articles, changed "
        "王 passage, three reciprocal pairs/six directions, system Back, nine-stroke reference "
        "trace then give-up recall and offline routes passed.\n\n"
        "All 57 original PNGs and raw attempt receipts are preserved; the coordinator directly "
        "inspected all 29 distinct byte groups. Three actual Compose panels show all 35 scoped "
        "Han in Gothic/Mincho/Textbook/Brush, including distinct 冖 versus 宀 and 冠/冗/完/守/元/寸. "
        "The 140 individual + 8 whole-word Paint results are assertion/hash records, not 148 "
        "separate visual PNG reads. No scoped blank, replacement box or materially misleading "
        "glyph was established. Complete reading examples are readable using the existing "
        "horizontal table navigation, not all columns in one frame.\n\n"
        "Read-only API35 helper emulator-5580 (parent PID 2004, QEMU 6712), host GPU with Vulkan "
        "disabled, 2048 MiB/two cores, was verified responsive and stopped; owner emulator-5556 "
        "was untouched. No app/guest heap or archive guard changed. Offline handwriting-model "
        "unavailability is explicit: injected reference paths, shape-only comparison and give-up "
        "recall are not handwriting-model recognition, human memory or physical-phone evidence.\n\n"
        "Fresh content validation/manifest passed with unchanged runtime bytes and 8,363 verified "
        "runtime hashes; previous host 3+1 and textual review are inherited honestly, not rerun. "
        "Required serial original-family independent visual confirmations are the next SAME079 "
        "bounded checkpoint; current-main integration/revalidation, signed owner fast-forward, "
        "CI and every immutable ZIP hash/budget remain later gates. No reviewer, next batch or "
        "second runner launched. Only approved workspace inputs/committed packets/durable control "
        "helpers were used; no historical helper access or new permission denial.\n\n"
        "**Published remains 105/1,228; 1,123 additions remain.** The local 106th addition is "
        "textually closed/native-passed but unpublished. Compatible Android f9b59a2+ is required; "
        "physical-phone, general-release and whole-set acceptance remain outstanding. "
        "Overall project incomplete; checkpoint status `continue`."
    )
    assert not (LOGS / "issue-body.txt").exists()
    (LOGS / "issue-body.txt").write_text(body, encoding="utf-8")
    print("Owner issue checkpoint body prepared.")


def normalize_logs():
    evidence_path = ROOT / "docs" / "n1-sources" / "execution-534.json"
    evidence = load(evidence_path)
    dispositions = []
    for name in ("adb-operations.txt", "emulator-stdout.txt"):
        original = ATTEMPT / name
        target = FOLDER / "attempt-1" / name
        assert sha(original) == sha(target)
        raw = target.with_suffix(".raw.txt.gz")
        assert not raw.exists()
        raw.write_bytes(gzip.compress(original.read_bytes(), mtime=0))
        assert gzip.decompress(raw.read_bytes()) == original.read_bytes()
        text = original.read_text(encoding="utf-8-sig")
        target.write_text("\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n",
                          encoding="utf-8")
        for entry in evidence["archivedReceipts"]:
            if entry["path"] == str(target.relative_to(ROOT)):
                entry.update(sha256=sha(target), bytes=target.stat().st_size,
                             originalBytesPreservedIn=str(raw.relative_to(ROOT)))
        evidence["archivedReceipts"].append({
            "path": str(raw.relative_to(ROOT)), "sha256": sha(raw),
            "decompressedSha256": sha(original), "bytes": raw.stat().st_size})
        dispositions.append({
            "file": str(target.relative_to(ROOT)), "originalSha256": sha(original),
            "normalizedSha256": sha(target), "rawGzip": str(raw.relative_to(ROOT)),
            "decision": "Strip trailing whitespace and extra blank EOF only in readable Git log; exact original bytes retained in deterministic gzip and approved control attempt.",
        })
    evidence["logWhitespaceDispositions"] = dispositions
    evidence["allOriginalLogBytesPreserved"] = True
    for source, name in ((Path(__file__), "finalization-execution-534.py"),
                         (CONTROL / "post-execution-534.ps1", "post-execution-534.ps1")):
        destination = FOLDER / "execution-534-receipts" / name
        assert not destination.exists()
        shutil.copyfile(source, destination)
        assert sha(source) == sha(destination)
        evidence["archivedReceipts"].append({
            "path": str(destination.relative_to(ROOT)), "sha256": sha(destination)})
    save(evidence_path, evidence)
    print("Readable log whitespace normalized; exact originals retained in gzip.")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
