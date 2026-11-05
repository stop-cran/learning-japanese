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
assert progress["checkpoint"] == 385 and progress["batch"] == "062"
assert progress["activeExecution"]["execution"] == 386
before = load(control / "execution-386-progress-before.json")
receipt = load(control / "batch-062-native-attempt-1-execution.json")
postrun = load(control / "execution-386-postrun-verification.json")
assert receipt["nativeExecuted"] and receipt["passed"] and receipt["failure"] is None
assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
assert receipt["prelaunch"]["connections"] == []
assert receipt["parentEmulatorPid"] == 17500 and receipt["qemuPid"] == 24596
assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
assert postrun["ownedProcessesRemaining"] == 0 and "emulator-5580" not in postrun["devices"]
assert "emulator-5556" in receipt["prelaunch"]["devices"] and "emulator-5556" in postrun["devices"]
assert postrun["contentStatus"] == postrun["androidStatus"] == []
assert postrun["contentHead"] == progress["execution386StartingState"]["startingHead"]
preparation = load(root / "docs" / "n1-sources" / "batch-062-native-preparation.json")
compiled = load(root / "docs" / "n1-sources" / "execution-385.json")
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

source = control / "artifacts" / "batch-062-native-attempt-1"
destination = root / "docs" / "n1-reviews" / "batch-062-native" / "attempt-1"
assert not destination.exists()
destination.mkdir()
expected_files = set(receipt["artifacts"]) | {
    "N1Batch062NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
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
assert "Time: 96.065" in raw and "OK (2 tests)" in raw
assert not re.search(r"INSTRUMENTATION_STATUS_CODE: -[234]", raw)
names = [
    ("N1Batch062GlyphTest", "salaryLookalikesAndPersonFallbackAcrossFourProductionFamilies"),
    ("N1Batch062ArticleTest", "fullSingleImportOfflineSalaryTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
]
for _, name in names:
    assert raw.count(f"INSTRUMENTATION_STATUS: test={name}") == 2
route = load(destination / "n1-062-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1
assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1074, 5032, 94, 0, 1]
assert route["contentSnapshot"] == preparation["contentSnapshot"]
assert route["contentVersion"] == "545c56b5d4b4e8ef"
assert route["fullOnyomi"] == ["ホウ"] and route["fullKunyomi"] == []
assert route["quizOnKeys"] == ["ほう"] and route["quizKunKeys"] == []
for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
            "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
            "drawingGradeRecordedOnNext", "offline"):
    assert route[key] is True, key
assert route["touchInjectedReferenceStrokes"] == 10 and route["phoneEvidence"] is False
raster = load(destination / "n1-062-font-raster.json")
assert raster["individualGlyphProbes"] == 44 and raster["wholeWordRasterProbes"] == 4
assert len(raster["rows"]) == 48
assert {row["character"] for row in raster["rows"] if "character" in row} == set("俸棒奉借付人亻木給糸合")
assert {row["word"] for row in raster["rows"] if "word" in row} == {"俸給"}
fonts = {"Gothic", "Mincho", "Textbook", "Brush"}
assert {row["font"] for row in raster["rows"]} == fonts
for font in fonts:
    glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
    assert len(glyphs) == 11 and all(row["hasGlyph"] for row in glyphs)
    assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 11
    words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
    assert len(words) == 1 and all(row["renderedCharactersNonblank"] == 2 for row in words)
direct_images = [
    "n1-062-font-pairs.png", "n1-062-selection.png",
    "n1-062-salary-components.png", "n1-062-pay-forwardlink.png",
    "n1-062-kanji-no-kun-and-annual-reading.png", "n1-062-kanji-on-reading.png",
    "n1-062-salary-receiving-example.png", "n1-062-salary-increase-example.png",
    "n1-062-curated-On-question.png", "n1-062-curated-On-feedback.png",
    "n1-062-drawing-feedback.png", "n1-062-meaning-feedback.png",
]
assert all((destination / name).is_file() for name in direct_images)
distinct_direct_images = len({sha(destination / name) for name in direct_images})
assert distinct_direct_images == 10
png_count = sum("dimensions" in entry for entry in artifacts)
assert png_count == 37
receipts_dir = destination.parent / "execution-receipts"
assert not receipts_dir.exists()
receipts_dir.mkdir()
for path in (
    control / "start-386.py", control / "run-386-native.ps1", Path(__file__),
    control / "execution-386-postrun-verification.json",
):
    target = receipts_dir / path.name
    shutil.copyfile(path, target)
    assert sha(target) == sha(path)
    artifacts.append({"path": str(target.relative_to(root)), "bytes": target.stat().st_size, "sha256": sha(target)})
index_path = destination.parent / "execution-386-artifact-index.json"
assert not index_path.exists()
save(index_path, {
    "schemaVersion": 1, "execution": 386, "batch": "062", "attempt": 1,
    "files": artifacts, "sourcePngCount": png_count,
    "directCoordinatorImageRequests": direct_images, "distinctDirectImageHashes": distinct_direct_images,
    "limits": "Twelve direct coordinator image requests represent ten distinct images: reading/no-kun and receiving/increase pairs have identical bytes. Not every captured image or independent visual acceptance. Hashes establish bytes, not readability.",
})
next_action = (
    "SAME062 signed native-assertions checkpoint386. BOTH named native cases PASSED terminal0/no skips/"
    "96.065s on owned read-onlyAPI35 emulator-5580 parent17500/QEMU24596, stopped emukill0; "
    "separate postrun verified bothPIDs absent/dedicatedworktrees clean/unrelatedemulator5556 still present. "
    "Read docs/n1-sources/execution-386.json and batch-062-native/execution-386-artifact-index.json/attempt-1. "
    "ProductionContentSyncONCE exact fulle157d58c envelope1074kanji5032words94N1/"
    "545c56b5d4b4e8ef/problems0/epoch1; Lite+Full fullホウ/emptykun, curatedホウ/[], normalizedほう/no-kun. "
    "BOTHPairs俸-俸給/給-俸給 inFOURdirections/SystemBack/offline/meaning/"
    "solecuratedOnGoodpersistentgrade/no-kunlog/tentouch-reference-strokes/ungradedtrace/recallmiss/"
    "persistedDrawAgain ALLpassed. 44singlePaint+4wholewordprobes/fourproductionfontrows passed; "
    "37sourcePNGs archived/12coordinatorDirectImageRequests/10distinctImageHashes. Actual俸棒奉借付人亻木給糸合/俸給 "
    "readable and distinguishable in fourfontrows/no blankboxes onAPI35; actual亻 fallback readable, face notidentified. "
    "Paragraph kana wraps without lost text; readingtables explicitly horizontally scrollable and clipped "
    "offscreen cells not fulltable visualreads. Drawing handwritingmodel unavailable: reference-touch shape "
    "trace/recallmiss, NOTMLKit or correcthumanrecall. OtherPNGs notcoordinator-inspected; independentvisualacceptance "
    "pending. NEXTboundedgate: reuse ORIGINAL Claude1d12b838-18c9-407a-b065-fc6e8fe44480 and "
    "GPT38b783dc-e2cf-4226-8786-e207effbde13 sessions SERIALly for bounded dependent visuals of same "
    "unchanged38ab6072 teaching/exact nativeevidence; actual modelcatalog/help identity/read-onlyview "
    "configuration/onecallperresponse/tooloverlap audit/terminalexit+archive BEFOREsecondlaunch. "
    "No new blindinitials or accepted384Android3+1/native386 rerun absent new concern. Preserve original "
    "reports/382textualclosure/originalClaude062-P1/P2 process noncompliance; supervised dependent lexical "
    "remediation is NOTretroactive strictinitialacceptance. Then latestmain normalnonrewriting integration/"
    "allcombined source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normal signing/ownerfastforward/"
    "publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFOREdelivery "
    "or063. Original383permissiondenial and049HOST512MiBOOM remainhistorical; qualifiedhost-only1GiBinit "
    "unchanged. Actualpermissiondenial/signingwait: preserveexactcommand/error, report/yield; no retry/workaround. "
    "No061rerun/063/secondrunner/concurrentheavywork/supervisorchanges. PreserveFULLlivehistory. "
    "Published88/1228,1140remain/89necessarysupportwords; localdraft89/90NOTdelivered; compatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)
now = datetime.now(timezone.utc).isoformat()
record = {
    "schemaVersion": 1, "execution": 386, "batch": "062",
    "status": "native-assertions-passed-pending-independent-visual",
    "recordedAt": now, "startingHead": progress["execution386StartingState"]["startingHead"],
    "scope": progress["execution386StartingState"]["scope"],
    "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
    "nativeExecution": receipt,
    "terminalCases": [{"class": cls, "test": name, "status": 0} for cls, name in names],
    "durationSeconds": 96.065, "failedCases": 0, "skippedCases": 0,
    "nativeRawLog": str((destination / "instrumentation.txt").relative_to(root)),
    "rawLogSha256": sha(destination / "instrumentation.txt"),
    "productionImportEvidence": route,
    "reciprocalPairs": [["俸", "俸給"], ["給", "俸給"]],
    "directedReciprocalTransitions": 4,
    "glyphEvidence": {
        "individualPaintProbes": 44, "wholeWordRasterProbes": 4, "productionComposeRows": 4,
        "directCoordinatorImageRequests": direct_images, "distinctDirectImageHashes": distinct_direct_images,
        "observation": "Four production font rows show readable distinct俸棒奉借付人亻木給糸合/俸給 without blank/replacement boxes. Actual人/亻 remain distinguishable;亻 uses readable shared fallback, face unidentified. N1 selection shows94cards. Curated question/feedback showsホウ as sole keyed answer, matching persistent-grade and no-kun assertions. Both salary Japanese examples with kana/English and object/increase explanation display readably. Both linked components, long-vowel guidance and employment/monthly/income distinctions display readably. Reused給 forwardlink is visible. Paragraph kana wraps within available width without text loss. Reading tables explicitly instruct sideways scrolling and have horizontally clipped offscreen cells; kanji-on-reading/no-kun images show the same viewport shifted right, clipping the reading column while showing the complete linked example and no-kun/ねんぽう guidance. Not complete table visual reads. Drawing shows ten numbered reference strokes/matching touch trace/practice-only/handwriting-model-unavailable qualification.",
        "limits": "Twelve direct image requests, ten distinct image hashes; reading/no-kun and receiving/increase image pairs are byte-identical. Remaining PNGs not coordinator-inspected. Actual fallback face not identified. Not independent visual approval or physical-phone evidence; raster hashes alone do not prove readability. No claim that all table columns are simultaneously visible.",
    },
    "artifactIndex": str(index_path.relative_to(root)), "artifactIndexSha256": sha(index_path),
    "sourcePngCount": png_count, "postrunVerification": postrun,
    "accepted384AndroidRetainedWithoutRerun": True,
    "original385ArtifactsAndOriginalReportHashesReverified": True,
    "originalReviewerSessionsForLaterDependentVisualConfirmation": compiled["originalReviewerSessionsForLaterDependentVisualConfirmation"],
    "runtimeEditsMade": False, "harnessEditsAfterExecution": False,
    "nativeExecuted": True, "nativeAssertionsPassed": True,
    "nativeAcceptance": False, "independentVisualAcceptance": False,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "publishedAdditions": 88, "remainingAdditions": 1140,
    "nextAction": next_action,
    "limits": "Native assertions passed with separate cleanup inventory; independent visual/batch acceptance and phone acceptance pending. Unique disposable source/syntheticHEAD/full production archive import; due-state fixture/reference-touch trace/recallmiss not learning efficacy/human recall/MLKit evidence. No teaching or runtime changes/reviewer/publication/063. Original Claude062-P1/P2 process noncompliance and bounded confirmation limits remain; strict historical process acceptance not claimed. Original383 permission denial and049 host-only heap qualification preserved. Overall project incomplete.",
}
record_path = root / "docs" / "n1-sources" / "execution-386.json"
assert not record_path.exists()
save(record_path, record)
batch_path = root / "docs" / "n1-sources" / "batch-062-progress.json"
batch = load(batch_path)
batch["status"] = record["status"]
batch["nativeExecutionCheckpoint"] = "execution-386.json"
batch["nativeAssertionEvidence"] = record["artifactIndex"]
batch["nextAction"] = next_action
save(batch_path, batch)
progress["execution386StartingState"]["status"] = record["status"]
checkpoint = {
    "schemaVersion": 1, "execution": 386, "checkpoint": 386, "batch": "062", "status": record["status"],
    "record": str(record_path.relative_to(root)), "recordedAt": now,
    "terminalCases": record["terminalCases"], "durationSeconds": 96.065,
    "nativeAssertionsPassed": True, "independentVisualAcceptance": False,
    "sourcePngCount": png_count, "directCoordinatorImageRequests": len(direct_images),
    "distinctDirectImageHashes": distinct_direct_images,
    "ownedHelperStopped": True, "ownedQemuStopped": True,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "nextAction": next_action, "publishedAdditions": 88, "remainingAdditions": 1140,
}
progress["execution386CoordinatorCheckpoint"] = checkpoint
progress["batch062NativeExecutionCheckpoint"] = checkpoint
progress.update(checkpoint=386, status="continue", stage="batch-062-native-passed-pending-independent-visual",
                nextAction=next_action, blocker=None)
mutable = {"checkpoint", "status", "stage", "nextAction", "blocker", "activeExecution"}
for key, value in before.items():
    if key not in mutable:
        assert progress[key] == value, key
save(progress_path, progress)
print(json.dumps({
    "checkpoint": 386, "status": progress["status"], "nativeAssertionsPassed": True,
    "archivedFiles": len(artifacts), "sourcePngCount": png_count,
    "directCoordinatorImageRequests": len(direct_images), "distinctDirectImageHashes": distinct_direct_images,
    "fullHistoricalProgressPreserved": True,
}, indent=2))
