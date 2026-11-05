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
before = load(control / "execution-396-progress-before.json")
assert progress["checkpoint"] == 395 and progress["batch"] == "063"
assert progress["activeExecution"]["execution"] == 396
receipt = load(control / "batch-063-native-attempt-1-execution.json")
postrun = load(control / "execution-396-postrun-verification.json")
assert receipt["nativeExecuted"] and receipt["passed"] and receipt["failure"] is None
assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
assert receipt["prelaunch"]["connections"] == []
assert receipt["parentEmulatorPid"] == 26180 and receipt["qemuPid"] == 4200
assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
assert postrun["ownedProcessesRemaining"] == 0 and "emulator-5580" not in postrun["devices"]
assert "emulator-5556" in receipt["prelaunch"]["devices"] and "emulator-5556" in postrun["devices"]
assert postrun["contentStatus"] == postrun["androidStatus"] == []
assert postrun["contentHead"] == progress["execution396StartingState"]["startingHead"]
assert not any(item["State"] == 2 for item in postrun["connections"])
preparation = load(root / "docs" / "n1-sources" / "batch-063-native-preparation.json")
compiled = load(root / "docs" / "n1-sources" / "execution-395.json")
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

source = control / "artifacts" / "batch-063-native-attempt-1"
destination = root / "docs" / "n1-reviews" / "batch-063-native" / "attempt-1"
assert not destination.exists()
destination.mkdir()
expected_files = set(receipt["artifacts"]) | {
    "N1Batch063NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
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
assert "Time: 114.805" in raw and "OK (2 tests)" in raw
names = [
    ("N1Batch063GlyphTest", "imitationLookalikesAndPersonFallbackAcrossFourProductionFamilies"),
    ("N1Batch063ArticleTest", "fullSingleImportOfflineImitationTwoReciprocalPairsBothReadingsDrawingAndSystemBack"),
]
for cls, name in names:
    assert raw.count(f"INSTRUMENTATION_STATUS: test={name}") == 2
    assert raw.count(f"INSTRUMENTATION_STATUS: class=io.github.stopcran.kanji.ui.{cls}") == 2
route = load(destination / "n1-063-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1
assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1075, 5033, 95, 0, 1]
assert route["contentSnapshot"] == preparation["contentSnapshot"]
assert route["contentVersion"] == "c19b742b7e6320a7"
assert route["fullOnyomi"] == ["ホウ"] and route["fullKunyomi"] == ["なら.う"]
assert route["quizOnKeys"] == ["ほう"] and route["quizKunKeys"] == ["ならう"]
for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
            "bothCuratedReadingsAndPersistedGoodGrades", "drawingTraceThenRecall",
            "drawingGradeRecordedOnNext", "offline"):
    assert route[key] is True, key
assert route["touchInjectedReferenceStrokes"] == 10 and route["phoneEvidence"] is False
raster = load(destination / "n1-063-font-raster.json")
assert raster["individualGlyphProbes"] == 44 and raster["wholeWordRasterProbes"] == 8
assert len(raster["rows"]) == 52
assert {row["character"] for row in raster["rows"] if "character" in row} == set("倣放方付人亻模木傚習攵")
assert {row["word"] for row in raster["rows"] if "word" in row} == {"模倣", "倣う"}
fonts = {"Gothic", "Mincho", "Textbook", "Brush"}
assert {row["font"] for row in raster["rows"]} == fonts
for font in fonts:
    glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
    assert len(glyphs) == 11 and all(row["hasGlyph"] for row in glyphs)
    assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 11
    words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
    assert len(words) == 2 and all(row["renderedCharactersNonblank"] == 2 for row in words)
direct_images = [
    "n1-063-font-pairs.png", "n1-063-selection.png",
    "n1-063-imitation-components.png", "n1-063-follow-learning-contrast.png",
    "n1-063-curated-Kun-feedback.png", "n1-063-curated-On-feedback.png",
    "n1-063-drawing-feedback.png", "n1-063-kanji-on-reading.png",
    "n1-063-kanji-kun-reading.png", "n1-063-follow-model-particle.png",
    "n1-063-imitation-work-example.png", "n1-063-imitation-backlink.png",
    "n1-063-follow-backlink.png", "n1-063-meaning-feedback.png",
]
assert all((destination / name).is_file() for name in direct_images)
distinct_direct_images = len({sha(destination / name) for name in direct_images})
png_count = sum("dimensions" in entry for entry in artifacts)
assert png_count == 45
receipts_dir = destination.parent / "execution-receipts"
assert not receipts_dir.exists()
receipts_dir.mkdir()
for path in (
    control / "start-396.py", control / "run-396-native.ps1", Path(__file__),
    control / "execution-396-postrun-verification.json",
):
    target = receipts_dir / path.name
    shutil.copyfile(path, target)
    assert sha(target) == sha(path)
    artifacts.append({"path": str(target.relative_to(root)), "bytes": target.stat().st_size, "sha256": sha(target)})
index_path = destination.parent / "execution-396-artifact-index.json"
assert not index_path.exists()
save(index_path, {
    "schemaVersion": 1, "execution": 396, "batch": "063", "attempt": 1,
    "files": artifacts, "sourcePngCount": png_count,
    "directCoordinatorImageRequests": direct_images, "distinctDirectImageHashes": distinct_direct_images,
    "limits": "Fourteen direct coordinator image requests; on/kun reading images have identical bytes. Not every captured image or independent visual acceptance. Hashes establish bytes, not readability.",
})
next_action = (
    "SAME063 signed native-assertions checkpoint396. BOTH named native cases PASSED terminal0/no skips/"
    "114.805s on owned read-onlyAPI35 emulator-5580 parent26180/QEMU4200, stopped emukill0; "
    "separate postrun verified bothPIDs absent/dedicatedworktrees clean/unrelatedemulator5556 still present. "
    "Postrun residual TCP SYN_SENT/TIME_WAIT recorded, no listeners; do not touch unrelated adbPID9520. "
    "Read docs/n1-sources/execution-396.json and batch-063-native/execution-396-artifact-index.json/attempt-1. "
    "ProductionContentSyncONCE exact full53ecd117 envelope1075kanji5033words95N1/"
    "c19b742b7e6320a7/problems0/epoch1; Lite+Full fullホウ/なら.う, both curated subsets, normalizedほう/ならう. "
    "BOTHPairs倣-模倣/倣-倣う inFOURdirections/SystemBack/offline/meaning/BOTHcuratedOnKunGoodpersistentgrades/"
    "tentouch-reference-strokes/ungradedtrace/recallmiss/persistedDrawAgain ALLpassed. "
    "44singlePaint+8wholewordprobes/fourproductionfontrows passed;45sourcePNGs archived/"
    f"14coordinatorDirectImageRequests/{distinct_direct_images}distinctImageHashes. "
    "Actual倣放方付人亻模木傚習攵/模倣/倣う readable and distinguishable in fourfontrows/no blankboxes onAPI35; "
    "actual亻/reused傚 fallback readable, actualfaces notidentified. Kana paragraphs wrap without lost text; "
    "readingtables explicitly sideways-scrollable and offscreen first-column cells NOT fulltable visualreads. "
    "On/kunreading images byte-identical. Drawing handwritingmodel unavailable: reference-touch shape trace/"
    "recallmiss NOTMLKit or correcthumanrecall. OtherPNGs notcoordinator-inspected; independentvisualacceptance pending. "
    "NEXTboundedgate: reuse ORIGINAL Claude80bc3198-c572-419d-b7a1-2df6ec8475c5 and "
    "GPT65373d23-fce9-455e-a51f-5bd7c89b5d17 sessions SERIALly for bounded dependent visuals of unchanged "
    "ddad655f teaching/exact nativeevidence; actual modelcatalog/help identity/read-onlyview configuration/"
    "onecallperresponse/tooloverlap audit/terminalexit+archive BEFOREsecondlaunch. "
    "No new blindinitials or accepted394Android3+1/native396 rerun absent new concern. Preserve originalreports/"
    "392textualclosure/originalClaude063-P1 one overlappingtwo-view response; superviseddependentlexical "
    "remediation NOTretroactive strictinitialacceptance. Then latestmain normalnonrewriting integration/"
    "allcombined source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normal signing/ownerfastforward/"
    "publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFOREdelivery "
    "or064. Original393permissiondenial and049HOST512MiBOOM remainhistorical; qualifiedhost-only1GiBinit unchanged. "
    "Actualpermissiondenial/signingwait: preserveexactcommand/error, report/yield; no retry/workaround. "
    "No062rerun/064/secondrunner/concurrentheavywork/supervisorchanges. PreserveFULLlivehistory. "
    "Published89/1228,1139remain; localdraft90 NOTdelivered; compatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)
now = datetime.now(timezone.utc).isoformat()
record = {
    "schemaVersion": 1, "execution": 396, "batch": "063",
    "status": "native-assertions-passed-pending-independent-visual",
    "recordedAt": now, "startingHead": progress["execution396StartingState"]["startingHead"],
    "scope": progress["execution396StartingState"]["scope"],
    "authorization": progress["execution396StartingState"]["authorization"],
    "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
    "nativeExecution": receipt,
    "terminalCases": [{"class": cls, "test": name, "status": 0} for cls, name in names],
    "durationSeconds": 114.805, "failedCases": 0, "skippedCases": 0,
    "nativeRawLog": str((destination / "instrumentation.txt").relative_to(root)),
    "rawLogSha256": sha(destination / "instrumentation.txt"),
    "productionImportEvidence": route,
    "reciprocalPairs": [["倣", "模倣"], ["倣", "倣う"]],
    "directedReciprocalTransitions": 4,
    "glyphEvidence": {
        "individualPaintProbes": 44, "wholeWordRasterProbes": 8, "productionComposeRows": 4,
        "directCoordinatorImageRequests": direct_images, "distinctDirectImageHashes": distinct_direct_images,
        "observation": "Four production font rows show readable distinct倣放方付人亻模木傚習攵/模倣/倣う without blank/replacement boxes. Actual人/亻 and reused rare傚 readable; shared fallback styles need not differ, actualfaces unidentified. N1 selection shows95cards. Both curated feedbacks show sole keyedホウ/ならう and persistentGood assertions passed. Actual模倣 transitiveを and倣う modelに examples, kana/English, modern-shape-not-history and習う contrast are readable. Inline kana may wrap at word boundaries without text loss. Readingtable explicitly instructs sideways scrolling; shifted viewport clips first-column initial characters while complete linked examples are readable. On/kunreading captures identical bytes, not separate viewport coverage. Drawing shows ten numbered strokes/matching touchtrace/practice-only/handwritingmodel unavailable. Not all captured PNGs inspected.",
        "limits": "Fourteen direct image requests; counts of distinct bytes are not additional reads. Native emulator, not phone or independent review. No fallback-face identification or claim all table columns simultaneously visible. Shape trace/recallmiss not MLKit or correct human recall.",
    },
    "artifactIndex": str(index_path.relative_to(root)), "artifactIndexSha256": sha(index_path),
    "sourcePngCount": png_count, "postrunVerification": postrun,
    "accepted394AndroidRetainedWithoutRerun": True,
    "original395ArtifactsAndOriginalReportHashesReverified": True,
    "originalReviewerSessionsForLaterDependentVisualConfirmation": compiled["originalReviewerSessionsForLaterDependentVisualConfirmation"],
    "runtimeEditsMade": False, "harnessEditsAfterExecution": False,
    "nativeExecuted": True, "nativeAssertionsPassed": True,
    "nativeAcceptance": False, "independentVisualAcceptance": False,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "publishedAdditions": 89, "remainingAdditions": 1139,
    "nextAction": next_action,
    "limits": "Native assertions passed; independent visual/batch acceptance and phone acceptance pending. Unique disposable source/syntheticHEAD/full production archive import; due-state fixture/reference-touch trace/recallmiss not learning efficacy/human recall/MLKit evidence. No teaching or runtime changes/reviewer/publication/064. Original Claude063-P1 process noncompliance and bounded confirmation limits remain; strict historical process acceptance not claimed. Original393 permission denial and049 host-only heap qualification preserved. Postrun residual SYN_SENT/TIME_WAIT retained, no helper listeners; no unrelated process touched. Overall project incomplete.",
}
record_path = root / "docs" / "n1-sources" / "execution-396.json"
assert not record_path.exists()
save(record_path, record)
batch_path = root / "docs" / "n1-sources" / "batch-063-progress.json"
batch = load(batch_path)
batch["status"] = record["status"]
batch["nativeExecutionCheckpoint"] = "execution-396.json"
batch["nativeAssertionEvidence"] = record["artifactIndex"]
batch["nextAction"] = next_action
save(batch_path, batch)
progress["execution396StartingState"]["status"] = record["status"]
checkpoint = {
    "schemaVersion": 1, "execution": 396, "checkpoint": 396, "batch": "063", "status": record["status"],
    "record": str(record_path.relative_to(root)), "recordedAt": now,
    "terminalCases": record["terminalCases"], "durationSeconds": 114.805,
    "nativeAssertionsPassed": True, "independentVisualAcceptance": False,
    "sourcePngCount": png_count, "directCoordinatorImageRequests": len(direct_images),
    "distinctDirectImageHashes": distinct_direct_images,
    "ownedHelperStopped": True, "ownedQemuStopped": True,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "nextAction": next_action, "publishedAdditions": 89, "remainingAdditions": 1139,
}
progress["execution396CoordinatorCheckpoint"] = checkpoint
progress["batch063NativeExecutionCheckpoint"] = checkpoint
progress.update(checkpoint=396, status="continue", stage="batch-063-native-passed-pending-independent-visual",
                nextAction=next_action, blocker=None)
mutable = {"checkpoint", "status", "stage", "nextAction", "blocker", "activeExecution"}
for key, value in before.items():
    if key not in mutable:
        assert progress[key] == value, key
save(progress_path, progress)
print(json.dumps({
    "checkpoint": 396, "status": progress["status"], "nativeAssertionsPassed": True,
    "archivedFiles": len(artifacts), "sourcePngCount": png_count,
    "directCoordinatorImageRequests": len(direct_images), "distinctDirectImageHashes": distinct_direct_images,
    "fullHistoricalProgressPreserved": True,
}, indent=2))
