import hashlib
import json
import re
import shutil
import struct
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
progress_path = control / "progress.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


progress = load(progress_path)
assert progress["checkpoint"] == 356 and progress["batch"] == "059"
before = json.loads(json.dumps(progress))
receipt = load(control / "batch-059-native-attempt-1-execution.json")
postrun = load(control / "execution-357-postrun-verification.json")
assert receipt["nativeExecuted"] and receipt["passed"] and receipt["failure"] is None
assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
assert receipt["prelaunch"]["connections"] == []
assert receipt["parentEmulatorPid"] == 21032 and receipt["qemuPid"] == 17756
assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
assert postrun["ownedProcessesRemaining"] == 0 and "emulator-5580" not in postrun["devices"]
assert "emulator-5556" in receipt["prelaunch"]["devices"] and "emulator-5556" in postrun["devices"]
assert postrun["contentStatus"] == postrun["androidStatus"] == []
assert postrun["contentHead"] == progress["execution357StartingState"]["startingHead"]
preparation = load(root / "docs" / "n1-sources" / "batch-059-native-preparation.json")
compiled = load(root / "docs" / "n1-sources" / "execution-356.json")
assert postrun["androidHead"] == preparation["androidSnapshot"]
for path, expected in (
    (preparation["archive"], preparation["archiveSha256"]),
    (preparation["fixture"], preparation["fixtureSha256"]),
    (receipt["testApk"], receipt["testApkSha256"]),
    (receipt["appApk"], receipt["appApkSha256"]),
):
    assert sha(Path(path)) == expected, path
for entry in compiled["artifacts"]:
    assert sha(root / entry["path"]) == entry["sha256"], entry["path"]
for relative, expected in compiled["originalInitialReportHashesUnchanged"].items():
    assert sha(root / relative) == expected, relative

source = control / "artifacts" / "batch-059-native-attempt-1"
destination = root / "docs" / "n1-reviews" / "batch-059-native" / "attempt-1"
assert not destination.exists()
destination.mkdir()
expected_files = set(receipt["artifacts"]) | {
    "N1Batch059NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
    "emulator-stdout.txt", "execution.json", "instrumentation.txt",
}
assert {path.name for path in source.iterdir()} == expected_files
artifacts = []
for path in sorted(source.iterdir()):
    assert path.is_file()
    target = destination / path.name
    shutil.copyfile(path, target)
    assert sha(target) == sha(path)
    entry = {"path": str(target.relative_to(root)), "bytes": target.stat().st_size, "sha256": sha(target)}
    if target.suffix == ".png":
        data = target.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        entry["dimensions"] = list(struct.unpack(">II", data[16:24]))
    artifacts.append(entry)
raw = (destination / "instrumentation.txt").read_text(encoding="utf-8-sig")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
assert "Time: 101.725" in raw and "OK (2 tests)" in raw
assert not re.search(r"INSTRUMENTATION_STATUS_CODE: -[234]", raw)
for name in (
    "benefitsLookalikesAndTwoFallbackRadicalsAcrossFourProductionFamilies",
    "fullSingleImportOfflineBenefitsTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
):
    assert raw.count(f"INSTRUMENTATION_STATUS: test={name}") == 2
route = load(destination / "n1-059-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1
assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1071, 5030, 91, 0, 1]
assert route["contentSnapshot"] == preparation["contentSnapshot"]
assert route["contentVersion"] == "1f1ad78479e9c1f4"
assert route["fullOnyomi"] == ["キョウ", "コウ"] and route["fullKunyomi"] == ["う.ける"]
assert route["quizOnKeys"] == ["きょう"] and route["quizKunKeys"] == []
for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
            "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
            "drawingGradeRecordedOnNext", "offline"):
    assert route[key] is True, key
assert route["touchInjectedReferenceStrokes"] == 8 and route["phoneEvidence"] is False
raster = load(destination / "n1-059-font-raster.json")
assert raster["individualGlyphProbes"] == 36 and raster["wholeWordRasterProbes"] == 4
assert len(raster["rows"]) == 40
assert {row["character"] for row in raster["rows"] if "character" in row} == set("享京厚高亠厂子口受")
assert {row["word"] for row in raster["rows"] if "word" in row} == {"享受"}
assert {row["font"] for row in raster["rows"]} == {"Gothic", "Mincho", "Textbook", "Brush"}
direct_images = [
    "n1-059-font-pairs.png", "n1-059-word-components-readings.png",
    "n1-059-drawing-feedback.png", "n1-059-kanji-lookalikes-fallback.png",
    "n1-059-curated-On-question.png", "n1-059-curated-On-feedback.png",
    "n1-059-selection.png", "n1-059-word-meaning-attachment.png",
    "n1-059-receiving-forwardlink.png", "n1-059-word-backlink-benefits.png",
    "n1-059-meaning-question.png",
]
for name in direct_images:
    assert (destination / name).is_file()
png_count = sum("dimensions" in entry for entry in artifacts)
assert png_count == 35
receipts_dir = destination.parent / "execution-receipts"
assert not receipts_dir.exists()
receipts_dir.mkdir()
for path in (
    control / "start-357.py", control / "run-357-native.ps1", Path(__file__),
    control / "execution-357-postrun-verification.json",
):
    target = receipts_dir / path.name
    shutil.copyfile(path, target)
    assert sha(target) == sha(path)
    artifacts.append({"path": str(target.relative_to(root)), "bytes": target.stat().st_size, "sha256": sha(target)})
index_path = destination.parent / "execution-357-artifact-index.json"
assert not index_path.exists()
save(index_path, {
    "schemaVersion": 1, "execution": 357, "batch": "059", "attempt": 1,
    "files": artifacts, "sourcePngCount": png_count,
    "directCoordinatorImageRequests": direct_images,
    "limits": "Eleven actual direct coordinator image inspections, not every captured image or independent visual acceptance. Hashes establish bytes, not readability.",
})
next_action = (
    "SAME059 signed native-assertions checkpoint357. BOTH named native cases PASSED terminal0/no skips/"
    "101.725s on owned read-onlyAPI35 emulator-5580 parent21032/QEMU17756, stopped emukill0; "
    "separate postrun verified bothPIDs absent/dedicatedworktrees clean/unrelatedemulator5556 still present. "
    "Read docs/n1-sources/execution-357.json and batch-059-native/execution-357-artifact-index.json/attempt-1. "
    "ProductionContentSyncONCE exact full911431da envelope1071kanji5030words91N1/"
    "1f1ad78479e9c1f4/problems0/epoch1; Lite+Full full orderedキョウコウ/う.ける, curatedキョウ/[], "
    "normalizedきょう/no-kun. BOTHpairs享-享受/受-享受 inFOURdirections/SystemBack/offline/meaning/"
    "solecuratedOnGoodpersistentgrade/no-kunlog/eighttouch-reference-strokes/ungradedtrace/recallmiss/"
    "persistedDrawAgain ALLpassed. 36singlePaint+4wholewordprobes/fourproductionfontrows passed; "
    "35sourcePNGs archived/11coordinatorDirectImageReads. Actual享京厚高 distinct, 亠厂子口受/享受 "
    "readable in fourfontrows/no blankboxes onAPI35; actual亠厂 fallback readable, face notidentified. "
    "Paragraph kana wraps without lost text; readingtables explicitly horizontally scrollable and "
    "examplecell captures are not fulltable visualreads. Drawing handwritingmodel unavailable: "
    "reference-touch shape trace/recallmiss, NOTMLKit or correcthumanrecall. OtherPNGs notcoordinator-inspected; "
    "independentvisualacceptance pending. NEXTboundedgate: reuse ORIGINAL Claude57374784-d547-43db-a93d-6d3bc5f93f30 "
    "and GPT345c7cb4-b120-41ce-b1ed-425003c6f4a5 sessions SERIALly for bounded dependent visuals of same "
    "unchanged769293c8 teaching/exact nativeevidence; actual modelcatalog/help identity/read-onlyview "
    "configuration/onecallperresponse/tooloverlap audit/terminalexit+archive BEFOREsecondlaunch. "
    "No new blindinitials or accepted355Android3+1/native357 rerun absent new concern. Preserve "
    "original reports/353textualclosure/historicalClaudeconfirmationoverlap noncompliance; boundedremediation "
    "NOTretroactive strictacceptance. Then latestmain normalnonrewriting integration/allcombined "
    "source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normal signing/ownerfastforward/"
    "publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 "
    "BEFOREdelivery or060. Original354permissiondenial and049HOST512MiBOOM remainhistorical; "
    "qualifiedhost-only1GiBinit unchanged. Actualpermissiondenial/signingwait: preserveexactcommand/error, "
    "report/yield; no retry/workaround. No058rerun/060/secondrunner/concurrentheavywork/supervisorchanges. "
    "PreserveFULLlivehistory. Published85/1228,1143remain; compatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)
now = datetime.now(timezone.utc).isoformat()
record = {
    "schemaVersion": 1, "execution": 357, "batch": "059",
    "status": "native-assertions-passed-pending-independent-visual",
    "recordedAt": now, "startingHead": progress["execution357StartingState"]["startingHead"],
    "scope": progress["execution357StartingState"]["scope"],
    "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
    "nativeExecution": receipt,
    "terminalCases": [
        {"class": "N1Batch059ArticleTest", "test": "fullSingleImportOfflineBenefitsTwoReciprocalPairsOnOnlyDrawingAndSystemBack", "status": 0},
        {"class": "N1Batch059GlyphTest", "test": "benefitsLookalikesAndTwoFallbackRadicalsAcrossFourProductionFamilies", "status": 0},
    ],
    "durationSeconds": 101.725, "failedCases": 0, "skippedCases": 0,
    "nativeRawLog": str((destination / "instrumentation.txt").relative_to(root)),
    "rawLogSha256": sha(destination / "instrumentation.txt"),
    "productionImportEvidence": route,
    "reciprocalPairs": [["享", "享受"], ["受", "享受"]],
    "directedReciprocalTransitions": 4,
    "glyphEvidence": {
        "individualPaintProbes": 36, "wholeWordRasterProbes": 4, "productionComposeRows": 4,
        "directCoordinatorImageRequests": direct_images,
        "observation": "Four production font rows show distinct readable享京厚高 and readable actual亠厂子口受/享受, no blank/replacement boxes. Actual亠/厂 fallbacks remain readable across rows; their face is not identified. N1 selection shows91cards. Curated question/feedback showsキョウ as sole keyed answer, matching persistent-grade and no-kun assertions; feedback retains full lookupキョウ/コウ/うける. Word meaning, both original example sentences, readings/attachment, both linked components, receiving/enjoyment boundaries and homophone display readably. Paragraph kana wraps within available width without text loss. Reused受 forwardlink and享 backlink are visible. Reading tables explicitly instruct sideways scrolling and have horizontally clipped offscreen cells; these screenshots do not prove a complete table was visible at once. Drawing shows eight numbered reference strokes/matching touch trace/practice-only/handwriting-model-unavailable qualification.",
        "limits": "Eleven direct coordinator image inspections only; remaining PNGs not coordinator-inspected. Actual fallback face not identified. Not independent visual approval or physical-phone evidence; native raster hashes alone do not prove readability. No claim that all table columns are simultaneously visible.",
    },
    "artifactIndex": str(index_path.relative_to(root)), "artifactIndexSha256": sha(index_path),
    "sourcePngCount": png_count, "postrunVerification": postrun,
    "accepted355AndroidRetainedWithoutRerun": True,
    "original356ArtifactsAndOriginalReportHashesReverified": True,
    "runtimeEditsMade": False, "harnessEditsAfterExecution": False,
    "nativeExecuted": True, "nativeAssertionsPassed": True,
    "nativeAcceptance": False, "independentVisualAcceptance": False,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "publishedAdditions": 85, "remainingAdditions": 1143,
    "nextAction": next_action,
    "limits": "Native assertions passed with separate cleanup inventory; independent visual/batch acceptance and phone acceptance pending. Unique disposable source/syntheticHEAD/full production archive import; due-state fixture/reference-touch trace/recallmiss not learning efficacy/human recall/MLKit evidence. No teaching or runtime changes/reviewer/publication/060. Original Claude confirmation overlap/noncompliance and bounded confirmation limits remain; strict historical process acceptance not claimed. Original354 permission denial and049 host-only heap qualification preserved. Overall project incomplete.",
}
record_path = root / "docs" / "n1-sources" / "execution-357.json"
assert not record_path.exists()
save(record_path, record)
batch_path = root / "docs" / "n1-sources" / "batch-059-progress.json"
batch = load(batch_path)
batch["status"] = record["status"]
batch["nativeExecutionCheckpoint"] = "execution-357.json"
batch["nativeAssertionEvidence"] = record["artifactIndex"]
batch["nextAction"] = next_action
save(batch_path, batch)
progress["execution357StartingState"]["status"] = record["status"]
checkpoint = {
    "schemaVersion": 1, "execution": 357, "batch": "059", "status": record["status"],
    "record": str(record_path.relative_to(root)), "recordedAt": now,
    "terminalCases": record["terminalCases"], "durationSeconds": 101.725,
    "nativeAssertionsPassed": True, "independentVisualAcceptance": False,
    "sourcePngCount": png_count, "directCoordinatorImageReads": len(direct_images),
    "ownedHelperStopped": True, "ownedQemuStopped": True,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "nextAction": next_action, "publishedAdditions": 85, "remainingAdditions": 1143,
}
progress["execution357CoordinatorCheckpoint"] = checkpoint
progress["batch059NativeExecutionCheckpoint"] = checkpoint
progress.update(checkpoint=357, status="continue", stage="batch-059-native-passed-pending-independent-visual",
                nextAction=next_action, blocker=None)
for key, value in before.items():
    if key not in {"checkpoint", "status", "stage", "nextAction", "blocker", "execution357StartingState"}:
        assert progress[key] == value, key
save(progress_path, progress)
print(json.dumps({
    "checkpoint": 357, "status": progress["status"], "nativeAssertionsPassed": True,
    "archivedFiles": len(artifacts), "sourcePngCount": png_count,
    "directCoordinatorImageReads": len(direct_images),
    "fullHistoricalProgressPreserved": True,
}, indent=2))
