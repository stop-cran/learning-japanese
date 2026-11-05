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
assert progress["checkpoint"] == 375 and progress["batch"] == "061"
assert progress["activeExecution"]["execution"] == 376
before = load(control / "execution-376-progress-before.json")
receipt = load(control / "batch-061-native-attempt-1-execution.json")
postrun = load(control / "execution-376-postrun-verification.json")
assert receipt["nativeExecuted"] and receipt["passed"] and receipt["failure"] is None
assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
assert receipt["prelaunch"]["connections"] == []
assert receipt["parentEmulatorPid"] == 1528 and receipt["qemuPid"] == 11340
assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
assert postrun["ownedProcessesRemaining"] == 0 and "emulator-5580" not in postrun["devices"]
assert "emulator-5556" in receipt["prelaunch"]["devices"] and "emulator-5556" in postrun["devices"]
assert postrun["contentStatus"] == postrun["androidStatus"] == []
assert postrun["contentHead"] == progress["execution376StartingState"]["startingHead"]
preparation = load(root / "docs" / "n1-sources" / "batch-061-native-preparation.json")
compiled = load(root / "docs" / "n1-sources" / "execution-375.json")
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

source = control / "artifacts" / "batch-061-native-attempt-1"
destination = root / "docs" / "n1-reviews" / "batch-061-native" / "attempt-1"
assert not destination.exists()
destination.mkdir()
expected_files = set(receipt["artifacts"]) | {
    "N1Batch061NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
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
assert "Time: 108.92" in raw and "OK (2 tests)" in raw
assert not re.search(r"INSTRUMENTATION_STATUS_CODE: -[234]", raw)
names = [
    ("N1Batch061GlyphTest", "haikuActorLookalikesAndPersonFallbackAcrossFourProductionFamilies"),
    ("N1Batch061ArticleTest", "fullSingleImportOfflineHaikuActorThreeReciprocalPairsOnOnlyDrawingAndSystemBack"),
]
for _, name in names:
    assert raw.count(f"INSTRUMENTATION_STATUS: test={name}") == 2
route = load(destination / "n1-061-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1
assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1073, 5031, 93, 0, 1]
assert route["contentSnapshot"] == preparation["contentSnapshot"]
assert route["contentVersion"] == "d01d660cc41262fe"
assert route["fullOnyomi"] == ["ハイ"] and route["fullKunyomi"] == []
assert route["quizOnKeys"] == ["はい"] and route["quizKunKeys"] == []
for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
            "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
            "drawingGradeRecordedOnNext", "offline"):
    assert route[key] is True, key
assert route["touchInjectedReferenceStrokes"] == 10 and route["phoneEvidence"] is False
raster = load(destination / "n1-061-font-raster.json")
assert raster["individualGlyphProbes"] == 44 and raster["wholeWordRasterProbes"] == 8
assert len(raster["rows"]) == 52
assert {row["character"] for row in raster["rows"] if "character" in row} == set("俳非悲借優人亻昔心句憂")
assert {row["word"] for row in raster["rows"] if "word" in row} == {"俳句", "俳優"}
fonts = {"Gothic", "Mincho", "Textbook", "Brush"}
assert {row["font"] for row in raster["rows"]} == fonts
for font in fonts:
    glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
    assert len(glyphs) == 11 and all(row["hasGlyph"] for row in glyphs)
    assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 11
    words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
    assert len(words) == 2 and all(row["renderedCharactersNonblank"] == 2 for row in words)
direct_images = [
    "n1-061-font-pairs.png", "n1-061-haiku-form-qualification.png",
    "n1-061-actor-components.png", "n1-061-superior-forwardlink.png",
    "n1-061-curated-On-feedback.png", "n1-061-drawing-feedback.png",
    "n1-061-selection.png", "n1-061-kanji-on-reading.png",
    "n1-061-haiku-backlink.png", "n1-061-actor-gender-boundary.png",
    "n1-061-kanji-lookalikes.png", "n1-061-curated-On-question.png",
]
assert all((destination / name).is_file() for name in direct_images)
png_count = sum("dimensions" in entry for entry in artifacts)
assert png_count == 40
receipts_dir = destination.parent / "execution-receipts"
assert not receipts_dir.exists()
receipts_dir.mkdir()
for path in (
    control / "start-376.py", control / "run-376-native.ps1", Path(__file__),
    control / "execution-376-postrun-verification.json",
):
    target = receipts_dir / path.name
    shutil.copyfile(path, target)
    assert sha(target) == sha(path)
    artifacts.append({"path": str(target.relative_to(root)), "bytes": target.stat().st_size, "sha256": sha(target)})
index_path = destination.parent / "execution-376-artifact-index.json"
assert not index_path.exists()
save(index_path, {
    "schemaVersion": 1, "execution": 376, "batch": "061", "attempt": 1,
    "files": artifacts, "sourcePngCount": png_count,
    "directCoordinatorImageRequests": direct_images,
    "limits": "Twelve actual direct coordinator image inspections, not every captured image or independent visual acceptance. Hashes establish bytes, not readability.",
})
next_action = (
    "SAME061 signed native-assertions checkpoint376. BOTH named native cases PASSED terminal0/no skips/"
    "108.92s on owned read-onlyAPI35 emulator-5580 parent1528/QEMU11340, stopped emukill0; "
    "separate postrun verified bothPIDs absent/dedicatedworktrees clean/unrelatedemulator5556 still present. "
    "Read docs/n1-sources/execution-376.json and batch-061-native/execution-376-artifact-index.json/attempt-1. "
    "ProductionContentSyncONCE exact fullf891cb1e envelope1073kanji5031words93N1/"
    "d01d660cc41262fe/problems0/epoch1; Lite+Full fullハイ/emptykun, curatedハイ/[], normalizedはい/no-kun. "
    "ALLTHREEpairs俳-俳句/俳-俳優/優-俳優 inSIXdirections/SystemBack/offline/meaning/"
    "solecuratedOnGoodpersistentgrade/no-kunlog/tentouch-reference-strokes/ungradedtrace/recallmiss/"
    "persistedDrawAgain ALLpassed. 44singlePaint+8wholewordprobes/fourproductionfontrows passed; "
    "40sourcePNGs archived/12coordinatorDirectImageReads. Actual俳非悲借優人亻昔心句憂/俳句/俳優 "
    "readable and distinguishable in fourfontrows/no blankboxes onAPI35; actual亻 fallback readable, face notidentified. "
    "Paragraph kana wraps without lost text; readingtables explicitly horizontally scrollable and clipped "
    "offscreen cells not fulltable visualreads. Drawing handwritingmodel unavailable: reference-touch shape "
    "trace/recallmiss, NOTMLKit or correcthumanrecall. OtherPNGs notcoordinator-inspected; independentvisualacceptance "
    "pending. NEXTboundedgate: reuse ORIGINAL Claude537a357b-564b-433a-897c-1285b08defb2 and "
    "GPT89aec53d-9f60-44ad-9cd7-f859fe24d8fd sessions SERIALly for bounded dependent visuals of same "
    "unchanged2567f5e7 teaching/exact nativeevidence; actual modelcatalog/help identity/read-onlyview "
    "configuration/onecallperresponse/tooloverlap audit/terminalexit+archive BEFOREsecondlaunch. "
    "No new blindinitials or accepted374Android3+1/native376 rerun absent new concern. Preserve original "
    "reports/372textualclosure/originalClaude061-P1/P2 process noncompliance; supervised dependent lexical "
    "remediation is NOTretroactive strictinitialacceptance. Then latestmain normalnonrewriting integration/"
    "allcombined source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normal signing/ownerfastforward/"
    "publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFOREdelivery "
    "or062. Original373permissiondenial and049HOST512MiBOOM remainhistorical; qualifiedhost-only1GiBinit "
    "unchanged. Actualpermissiondenial/signingwait: preserveexactcommand/error, report/yield; no retry/workaround. "
    "No060rerun/062/secondrunner/concurrentheavywork/supervisorchanges. PreserveFULLlivehistory. "
    "Published87/1228,1141remain; compatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set "
    "outstanding. Overallproject incomplete."
)
now = datetime.now(timezone.utc).isoformat()
record = {
    "schemaVersion": 1, "execution": 376, "batch": "061",
    "status": "native-assertions-passed-pending-independent-visual",
    "recordedAt": now, "startingHead": progress["execution376StartingState"]["startingHead"],
    "scope": progress["execution376StartingState"]["scope"],
    "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
    "nativeExecution": receipt,
    "terminalCases": [{"class": cls, "test": name, "status": 0} for cls, name in names],
    "durationSeconds": 108.92, "failedCases": 0, "skippedCases": 0,
    "nativeRawLog": str((destination / "instrumentation.txt").relative_to(root)),
    "rawLogSha256": sha(destination / "instrumentation.txt"),
    "productionImportEvidence": route,
    "reciprocalPairs": [["俳", "俳句"], ["俳", "俳優"], ["優", "俳優"]],
    "directedReciprocalTransitions": 6,
    "glyphEvidence": {
        "individualPaintProbes": 44, "wholeWordRasterProbes": 8, "productionComposeRows": 4,
        "directCoordinatorImageRequests": direct_images,
        "observation": "Four production font rows show readable distinct俳非悲借優人亻昔心句憂/俳句/俳優 without blank/replacement boxes. Actual人/亻 remain distinguishable;亻 uses readable shared fallback, face unidentified. N1 selection shows93cards. Curated question/feedback showsハイ as sole keyed answer, matching persistent-grade and no-kun assertions. Haiku's qualified traditional form, both Japanese examples, mora timing explanation and haiku components display readably. Actor gender boundary, both example sentences, noun attachment and both linked components display readably. Reused優 forwardlink and俳 backlink are visible. Paragraph kana wraps within available width without text loss. Reading tables explicitly instruct sideways scrolling and have horizontally clipped offscreen cells; the kanji-on-reading image is shifted right and clips the reading column, while haiku-backlink exposesハイ but clips the right example text. These are not complete table visual reads. Drawing shows ten numbered reference strokes/matching touch trace/practice-only/handwriting-model-unavailable qualification.",
        "limits": "Twelve direct coordinator image inspections only; remaining PNGs not coordinator-inspected. Actual fallback face not identified. Not independent visual approval or physical-phone evidence; native raster hashes alone do not prove readability. No claim that all table columns are simultaneously visible.",
    },
    "artifactIndex": str(index_path.relative_to(root)), "artifactIndexSha256": sha(index_path),
    "sourcePngCount": png_count, "postrunVerification": postrun,
    "accepted374AndroidRetainedWithoutRerun": True,
    "original375ArtifactsAndOriginalReportHashesReverified": True,
    "runtimeEditsMade": False, "harnessEditsAfterExecution": False,
    "nativeExecuted": True, "nativeAssertionsPassed": True,
    "nativeAcceptance": False, "independentVisualAcceptance": False,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "publishedAdditions": 87, "remainingAdditions": 1141,
    "nextAction": next_action,
    "limits": "Native assertions passed with separate cleanup inventory; independent visual/batch acceptance and phone acceptance pending. Unique disposable source/syntheticHEAD/full production archive import; due-state fixture/reference-touch trace/recallmiss not learning efficacy/human recall/MLKit evidence. No teaching or runtime changes/reviewer/publication/062. Original Claude061-P1/P2 process noncompliance and bounded confirmation limits remain; strict historical process acceptance not claimed. Original373 permission denial and049 host-only heap qualification preserved. Overall project incomplete.",
}
record_path = root / "docs" / "n1-sources" / "execution-376.json"
assert not record_path.exists()
save(record_path, record)
batch_path = root / "docs" / "n1-sources" / "batch-061-progress.json"
batch = load(batch_path)
batch["status"] = record["status"]
batch["nativeExecutionCheckpoint"] = "execution-376.json"
batch["nativeAssertionEvidence"] = record["artifactIndex"]
batch["nextAction"] = next_action
save(batch_path, batch)
progress["execution376StartingState"]["status"] = record["status"]
checkpoint = {
    "schemaVersion": 1, "execution": 376, "checkpoint": 376, "batch": "061", "status": record["status"],
    "record": str(record_path.relative_to(root)), "recordedAt": now,
    "terminalCases": record["terminalCases"], "durationSeconds": 108.92,
    "nativeAssertionsPassed": True, "independentVisualAcceptance": False,
    "sourcePngCount": png_count, "directCoordinatorImageReads": len(direct_images),
    "ownedHelperStopped": True, "ownedQemuStopped": True,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "nextAction": next_action, "publishedAdditions": 87, "remainingAdditions": 1141,
}
progress["execution376CoordinatorCheckpoint"] = checkpoint
progress["batch061NativeExecutionCheckpoint"] = checkpoint
progress.update(checkpoint=376, status="continue", stage="batch-061-native-passed-pending-independent-visual",
                nextAction=next_action, blocker=None)
mutable = {"checkpoint", "status", "stage", "nextAction", "blocker", "activeExecution"}
for key, value in before.items():
    if key not in mutable:
        assert progress[key] == value, key
save(progress_path, progress)
print(json.dumps({
    "checkpoint": 376, "status": progress["status"], "nativeAssertionsPassed": True,
    "archivedFiles": len(artifacts), "sourcePngCount": png_count,
    "directCoordinatorImageReads": len(direct_images),
    "fullHistoricalProgressPreserved": True,
}, indent=2))
