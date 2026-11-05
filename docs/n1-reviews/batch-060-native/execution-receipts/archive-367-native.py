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
assert progress["checkpoint"] == 366 and progress["batch"] == "060"
assert progress["activeExecution"]["execution"] == 367
before = json.loads(json.dumps(progress))
receipt = load(control / "batch-060-native-attempt-1-execution.json")
postrun = load(control / "execution-367-postrun-verification.json")
assert receipt["nativeExecuted"] and receipt["passed"] and receipt["failure"] is None
assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
assert receipt["prelaunch"]["connections"] == []
assert receipt["parentEmulatorPid"] == 11792 and receipt["qemuPid"] == 25572
assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
assert postrun["ownedProcessesRemaining"] == 0 and "emulator-5580" not in postrun["devices"]
assert "emulator-5556" in receipt["prelaunch"]["devices"] and "emulator-5556" in postrun["devices"]
assert postrun["contentStatus"] == postrun["androidStatus"] == []
assert postrun["contentHead"] == progress["execution367StartingState"]["startingHead"]
preparation = load(root / "docs" / "n1-sources" / "batch-060-native-preparation.json")
compiled = load(root / "docs" / "n1-sources" / "execution-366.json")
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

source = control / "artifacts" / "batch-060-native-attempt-1"
destination = root / "docs" / "n1-reviews" / "batch-060-native" / "attempt-1"
assert not destination.exists()
destination.mkdir()
expected_files = set(receipt["artifacts"]) | {
    "N1Batch060NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
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
assert "Time: 88.09" in raw and "OK (2 tests)" in raw
assert not re.search(r"INSTRUMENTATION_STATUS_CODE: -[234]", raw)
for name in (
    "pavilionLookalikesAndThreeFallbackComponentsAcrossFourProductionFamilies",
    "fullSingleImportOfflinePavilionTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
):
    assert raw.count(f"INSTRUMENTATION_STATUS: test={name}") == 2
route = load(destination / "n1-060-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1
assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1072, 5031, 92, 0, 1]
assert route["contentSnapshot"] == preparation["contentSnapshot"]
assert route["contentVersion"] == "dbf047f0c2e6cd56"
assert route["fullOnyomi"] == ["テイ", "チン"] and route["fullKunyomi"] == []
assert route["quizOnKeys"] == ["てい"] and route["quizKunKeys"] == []
for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
            "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
            "drawingGradeRecordedOnNext", "offline"):
    assert route[key] is True, key
assert route["touchInjectedReferenceStrokes"] == 9 and route["phoneEvidence"] is False
raster = load(destination / "n1-060-font-raster.json")
assert raster["individualGlyphProbes"] == 52 and raster["wholeWordRasterProbes"] == 4
assert len(raster["rows"]) == 56
assert {row["character"] for row in raster["rows"] if "character" in row} == set("亭停京享高亠亻冖丁小子口料")
assert {row["word"] for row in raster["rows"] if "word" in row} == {"料亭"}
fonts = {"Gothic", "Mincho", "Textbook", "Brush"}
assert {row["font"] for row in raster["rows"]} == fonts
for font in fonts:
    glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
    assert len(glyphs) == 13 and all(row["hasGlyph"] for row in glyphs)
    assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 13
    words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
    assert len(words) == 1 and words[0]["renderedCharactersNonblank"] == 2
direct_images = [
    "n1-060-font-pairs.png", "n1-060-kanji-mnemonic.png",
    "n1-060-word-components-readings.png", "n1-060-materials-forwardlink.png",
    "n1-060-curated-On-feedback.png", "n1-060-drawing-feedback.png",
    "n1-060-selection.png", "n1-060-curated-On-question.png",
    "n1-060-word-meaning-qualification.png", "n1-060-word-backlink-pavilion.png",
    "n1-060-kanji-lower-lookalikes.png",
]
for name in direct_images:
    assert (destination / name).is_file()
png_count = sum("dimensions" in entry for entry in artifacts)
assert png_count == 36
receipts_dir = destination.parent / "execution-receipts"
assert not receipts_dir.exists()
receipts_dir.mkdir()
for path in (
    control / "start-367.py", control / "run-367-native.ps1", Path(__file__),
    control / "execution-367-postrun-verification.json",
):
    target = receipts_dir / path.name
    shutil.copyfile(path, target)
    assert sha(target) == sha(path)
    artifacts.append({"path": str(target.relative_to(root)), "bytes": target.stat().st_size, "sha256": sha(target)})
index_path = destination.parent / "execution-367-artifact-index.json"
assert not index_path.exists()
save(index_path, {
    "schemaVersion": 1, "execution": 367, "batch": "060", "attempt": 1,
    "files": artifacts, "sourcePngCount": png_count,
    "directCoordinatorImageRequests": direct_images,
    "limits": "Eleven actual direct coordinator image inspections, not every captured image or independent visual acceptance. Hashes establish bytes, not readability.",
})
next_action = (
    "SAME060 signed native-assertions checkpoint367. BOTH named native cases PASSED terminal0/no skips/"
    "88.09s on owned read-onlyAPI35 emulator-5580 parent11792/QEMU25572, stopped emukill0; "
    "separate postrun verified bothPIDs absent/dedicatedworktrees clean/unrelatedemulator5556 still present. "
    "Read docs/n1-sources/execution-367.json and batch-060-native/execution-367-artifact-index.json/attempt-1. "
    "ProductionContentSyncONCE exact full99d8ace0 envelope1072kanji5031words92N1/"
    "dbf047f0c2e6cd56/problems0/epoch1; Lite+Full full orderedテイチン/emptykun, curatedテイ/[], "
    "normalizedてい/no-kun. BOTHpairs亭-料亭/料-料亭 inFOURdirections/SystemBack/offline/meaning/"
    "solecuratedOnGoodpersistentgrade/no-kunlog/ninetouch-reference-strokes/ungradedtrace/recallmiss/"
    "persistedDrawAgain ALLpassed. 52singlePaint+4wholewordprobes/fourproductionfontrows passed; "
    "36sourcePNGs archived/11coordinatorDirectImageReads. Actual亭停京享高 distinct, "
    "亠亻冖丁小子口料/料亭 readable in fourfontrows/no blankboxes onAPI35; "
    "actual亠亻冖 fallback readable, face notidentified. Paragraph kana wraps without lost text; "
    "readingtables explicitly horizontally scrollable and clipped offscreen cells not fulltable visualreads. "
    "Drawing handwritingmodel unavailable: reference-touch shape trace/recallmiss, NOTMLKit or correcthumanrecall. "
    "OtherPNGs notcoordinator-inspected; independentvisualacceptance pending. NEXTboundedgate: reuse ORIGINAL "
    "Claude34dbb43d-2a7f-4fa9-9e45-00c50c1281a1 and GPT8130aa10-a2af-44b9-80ca-28fb1662eb6c sessions "
    "SERIALly for bounded dependent visuals of same unchangedea1dac1a teaching/exact nativeevidence; "
    "actual modelcatalog/help identity/read-onlyview configuration/onecallperresponse/tooloverlap audit/"
    "terminalexit+archive BEFOREsecondlaunch. No new blindinitials or accepted365Android3+1/native367 rerun "
    "absent new concern. Preserve original reports/363textualclosure/originalClaude060-P1/P2 process "
    "noncompliance; supervised dependent lexical remediation is NOTretroactive strictinitialacceptance. "
    "Then latestmain normalnonrewriting integration/allcombined source-baseline-reading-link-font-stroke/"
    "Python/vocab/validator/freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/"
    "normal signing/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/"
    "terminalreceipts/ownerissue60 BEFOREdelivery or061. Original364permissiondenial and049HOST512MiBOOM "
    "remainhistorical; qualifiedhost-only1GiBinit unchanged. Actualpermissiondenial/signingwait: "
    "preserveexactcommand/error, report/yield; no retry/workaround. No059rerun/061/secondrunner/"
    "concurrentheavywork/supervisorchanges. PreserveFULLlivehistory. Published86/1228,1142remain; "
    "compatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)
now = datetime.now(timezone.utc).isoformat()
record = {
    "schemaVersion": 1, "execution": 367, "batch": "060",
    "status": "native-assertions-passed-pending-independent-visual",
    "recordedAt": now, "startingHead": progress["execution367StartingState"]["startingHead"],
    "scope": progress["execution367StartingState"]["scope"],
    "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
    "nativeExecution": receipt,
    "terminalCases": [
        {"class": "N1Batch060ArticleTest", "test": "fullSingleImportOfflinePavilionTwoReciprocalPairsOnOnlyDrawingAndSystemBack", "status": 0},
        {"class": "N1Batch060GlyphTest", "test": "pavilionLookalikesAndThreeFallbackComponentsAcrossFourProductionFamilies", "status": 0},
    ],
    "durationSeconds": 88.09, "failedCases": 0, "skippedCases": 0,
    "nativeRawLog": str((destination / "instrumentation.txt").relative_to(root)),
    "rawLogSha256": sha(destination / "instrumentation.txt"),
    "productionImportEvidence": route,
    "reciprocalPairs": [["亭", "料亭"], ["料", "料亭"]],
    "directedReciprocalTransitions": 4,
    "glyphEvidence": {
        "individualPaintProbes": 52, "wholeWordRasterProbes": 4, "productionComposeRows": 4,
        "directCoordinatorImageRequests": direct_images,
        "observation": "Four production font rows show distinct readable亭停京享高 and readable actual亠亻冖丁小子口料/料亭, no blank/replacement boxes. Actual亠/亻/冖 fallback components remain readable across rows; their face is not identified. N1 selection shows92cards. Curated question/feedback showsテイ as sole keyed answer, matching persistent-grade and no-kun assertions; feedback retains full lookupテイ/チン. Word meaning, both original example sentences, food/place attachment, both linked components, restaurant/eatery/inn boundaries and kanji mnemonic/lookalike prose display readably. Paragraph kana wraps within available width without text loss. Reused料 forwardlink and亭 backlink are visible. Reading tables explicitly instruct sideways scrolling and have horizontally clipped offscreen cells; these screenshots do not prove a complete table was visible at once. Drawing shows nine numbered reference strokes/matching touch trace/practice-only/handwriting-model-unavailable qualification.",
        "limits": "Eleven direct coordinator image inspections only; remaining PNGs not coordinator-inspected. Actual fallback face not identified. Not independent visual approval or physical-phone evidence; native raster hashes alone do not prove readability. No claim that all table columns are simultaneously visible.",
    },
    "artifactIndex": str(index_path.relative_to(root)), "artifactIndexSha256": sha(index_path),
    "sourcePngCount": png_count, "postrunVerification": postrun,
    "accepted365AndroidRetainedWithoutRerun": True,
    "original366ArtifactsAndOriginalReportHashesReverified": True,
    "runtimeEditsMade": False, "harnessEditsAfterExecution": False,
    "nativeExecuted": True, "nativeAssertionsPassed": True,
    "nativeAcceptance": False, "independentVisualAcceptance": False,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "publishedAdditions": 86, "remainingAdditions": 1142,
    "nextAction": next_action,
    "limits": "Native assertions passed with separate cleanup inventory; independent visual/batch acceptance and phone acceptance pending. Unique disposable source/syntheticHEAD/full production archive import; due-state fixture/reference-touch trace/recallmiss not learning efficacy/human recall/MLKit evidence. No teaching or runtime changes/reviewer/publication/061. Original Claude060-P1/P2 process noncompliance and bounded confirmation limits remain; strict historical process acceptance not claimed. Original364 permission denial and049 host-only heap qualification preserved. Overall project incomplete.",
}
record_path = root / "docs" / "n1-sources" / "execution-367.json"
assert not record_path.exists()
save(record_path, record)
batch_path = root / "docs" / "n1-sources" / "batch-060-progress.json"
batch = load(batch_path)
batch["status"] = record["status"]
batch["nativeExecutionCheckpoint"] = "execution-367.json"
batch["nativeAssertionEvidence"] = record["artifactIndex"]
batch["nextAction"] = next_action
save(batch_path, batch)
progress["execution367StartingState"]["status"] = record["status"]
checkpoint = {
    "schemaVersion": 1, "execution": 367, "batch": "060", "status": record["status"],
    "record": str(record_path.relative_to(root)), "recordedAt": now,
    "terminalCases": record["terminalCases"], "durationSeconds": 88.09,
    "nativeAssertionsPassed": True, "independentVisualAcceptance": False,
    "sourcePngCount": png_count, "directCoordinatorImageReads": len(direct_images),
    "ownedHelperStopped": True, "ownedQemuStopped": True,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "nextAction": next_action, "publishedAdditions": 86, "remainingAdditions": 1142,
}
progress["execution367CoordinatorCheckpoint"] = checkpoint
progress["batch060NativeExecutionCheckpoint"] = checkpoint
progress.update(checkpoint=367, status="continue", stage="batch-060-native-passed-pending-independent-visual",
                nextAction=next_action, blocker=None)
for key, value in before.items():
    if key not in {"checkpoint", "status", "stage", "nextAction", "blocker", "execution367StartingState", "activeExecution"}:
        assert progress[key] == value, key
save(progress_path, progress)
print(json.dumps({
    "checkpoint": 367, "status": progress["status"], "nativeAssertionsPassed": True,
    "archivedFiles": len(artifacts), "sourcePngCount": png_count,
    "directCoordinatorImageReads": len(direct_images),
    "fullHistoricalProgressPreserved": True,
}, indent=2))
