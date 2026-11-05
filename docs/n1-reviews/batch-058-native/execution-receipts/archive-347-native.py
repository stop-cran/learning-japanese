import hashlib
import json
import re
import shutil
import struct
import subprocess
from datetime import datetime
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
assert progress["checkpoint"] == 346 and progress["batch"] == "058"
before = json.loads(json.dumps(progress))
receipt = load(control / "batch-058-native-attempt-1-execution.json")
postrun = load(control / "execution-347-postrun-verification.json")
assert receipt["nativeExecuted"] and receipt["passed"] and receipt["failure"] is None
assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
assert receipt["prelaunch"]["connections"] == []
assert receipt["parentEmulatorPid"] == 25124 and receipt["qemuPid"] == 19420
assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
assert postrun["ownedProcessesRemaining"] == 0 and "emulator-5580" not in postrun["devices"]
assert "emulator-5556" in postrun["devices"]
assert postrun["contentStatus"] == postrun["androidStatus"] == []
assert postrun["contentHead"] == progress["execution347StartingState"]["startingHead"]
preparation = load(root / "docs" / "n1-sources" / "batch-058-native-preparation.json")
compiled = load(root / "docs" / "n1-sources" / "execution-346.json")
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

source = control / "artifacts" / "batch-058-native-attempt-1"
destination = root / "docs" / "n1-reviews" / "batch-058-native" / "attempt-1"
assert not destination.exists()
destination.mkdir()
expected_files = set(receipt["artifacts"]) | {
    "N1Batch058NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
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
assert "Time: 102.361" in raw and "OK (2 tests)" in raw
assert not re.search(r"INSTRUMENTATION_STATUS_CODE: -[234]", raw)
for name in (
    "hillLookalikesRadicalAndSupportWordsAcrossFourProductionFamilies",
    "fullSingleImportOfflineHillThreeReciprocalPairsBothCuratedReadingsDrawingAndSystemBack",
):
    assert raw.count(f"INSTRUMENTATION_STATUS: test={name}") == 2
route = load(destination / "n1-058-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1
assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1070, 5029, 90, 0, 1]
assert route["contentSnapshot"] == preparation["contentSnapshot"]
assert route["contentVersion"] == "5e8f3e7e39ea187a"
assert route["fullOnyomi"] == ["キュウ"] and route["fullKunyomi"] == ["おか"]
assert route["quizOnKeys"] == ["きゅう"] and route["quizKunKeys"] == ["おか"]
for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
            "bothCuratedQuestionsAndPersistedGrades", "drawingTraceThenRecall",
            "drawingGradeRecordedOnNext", "offline"):
    assert route[key] is True, key
assert route["touchInjectedReferenceStrokes"] == 5 and route["phoneEvidence"] is False
raster = load(destination / "n1-058-font-raster.json")
assert raster["individualGlyphProbes"] == 28 and raster["wholeWordRasterProbes"] == 8
assert len(raster["rows"]) == 36
assert {row["character"] for row in raster["rows"] if "character" in row} == set("丘兵近共一砂山")
assert {row["word"] for row in raster["rows"] if "word" in row} == {"丘", "砂丘"}
assert {row["font"] for row in raster["rows"]} == {"Gothic", "Mincho", "Textbook", "Brush"}
direct_images = [
    "n1-058-font-pairs.png", "n1-058-drawing-feedback.png",
    "n1-058-dune-components-readings.png", "n1-058-hill-house-example.png",
    "n1-058-selection.png", "n1-058-curated-On-question.png",
    "n1-058-curated-On-feedback.png", "n1-058-curated-Kun-question.png",
    "n1-058-curated-Kun-feedback.png", "n1-058-sand-forwardlink-dune.png",
]
for name in direct_images:
    assert (destination / name).is_file()
png_count = sum("dimensions" in entry for entry in artifacts)
assert png_count == len([name for name in receipt["artifacts"] if name.endswith(".png")])
receipts_dir = destination.parent / "execution-receipts"
assert not receipts_dir.exists()
receipts_dir.mkdir()
for path in (
    control / "run-347-native.ps1", Path(__file__),
    control / "execution-347-postrun-verification.json",
):
    target = receipts_dir / path.name
    shutil.copyfile(path, target)
    assert sha(target) == sha(path)
    artifacts.append({"path": str(target.relative_to(root)), "bytes": target.stat().st_size, "sha256": sha(target)})
index_path = destination.parent / "execution-347-artifact-index.json"
assert not index_path.exists()
save(index_path, {
    "schemaVersion": 1, "execution": 347, "batch": "058", "attempt": 1,
    "files": artifacts, "sourcePngCount": png_count,
    "directCoordinatorImageRequests": direct_images,
    "limits": "Ten actual direct coordinator image inspections, not every captured image or independent visual acceptance. Hashes establish bytes, not readability.",
})
next_action = (
    "SAME058 signed native-assertions checkpoint347. BOTH named native cases PASSED terminal0/no skips/"
    "102.361s on owned read-onlyAPI35 emulator-5580 parent25124/QEMU19420, killed emukill0; "
    "separate postrun verified bothPIDs absent/dedicatedworktrees clean/unrelatedemulator5556 unchanged. "
    "Read docs/n1-sources/execution-347.json and batch-058-native/execution-347-artifact-index.json/"
    "attempt-1. ProductionContentSyncONCE exact full00491ddd envelope1070kanji5029words90N1/"
    "5e8f3e7e39ea187a/problems0/epoch1; full+Liteキュウ/おか and curatedきゅう/おか; "
    "allTHREEpairs丘-丘/丘-砂丘/砂-砂丘 inSIXdirections/SystemBack/offline/meaning/BOTHcuratedGood "
    "persistentgrades/five touch-reference strokes/ungradedtrace/recallmiss/persistedDrawAgain ALLpassed. "
    f"28singlePaint+8wholewordprobes/fourproductionfontrows passed; {png_count}sourcePNGs archived, "
    "10coordinatorDirectImageReads(fontpairs/drawingfeedback/dunecomponents/hillhouse/selection/"
    "bothcuratedquestions+feedback/sandforwardlink). Actual丘兵近共 distinct and一砂山/丘/砂丘 readable "
    "in fourfontrows/no blankboxes onAPI35. Duneさきゅう wraps within paragraph without clipping; "
    "fallbackface notidentified. Drawing explicitly handwritingmodel unavailable: reference-touch "
    "shape trace/recallmiss, NOTMLKit or correcthumanrecall. OtherPNGs notcoordinator-inspected; "
    "independentvisualacceptance pending. NEXTboundedgate: reuse ORIGINAL Claude527ad6ad-8f36-4c08-8a38-96d2cbf333ee "
    "and GPT843ee44f-696c-4254-b7b3-7d3fe8c0cfa6 sessions SERIALly for bounded dependent visuals of same "
    "unchanged58b53fd3 teaching/exact nativeevidence; actual modelcatalog/help identity/read-onlyview "
    "configuration/onecallperresponse/tooloverlap audit/terminalexit+archive BEFOREsecondlaunch. "
    "No new blindinitials or accepted345Android3+1/native347 rerun absent new concern. Preserve "
    "original58b53fd3 reports/initialClaude3overlaps/historicalnoncompliance; boundedremediation NOT "
    "retroactive strictacceptance. Then latestmain normalnonrewriting integration/allcombined "
    "source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normal signing/ownerfastforward/"
    "publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 "
    "BEFOREdelivery or059. Original344permissiondenial and049HOST512MiBOOM remainhistorical; "
    "qualifiedhost-only1GiBinit unchanged. Actualpermissiondenial/signingwait: preserveexactcommand/error, "
    "report/yield; no retry/workaround. No057rerun/059/secondrunner/concurrentheavywork/supervisorchanges. "
    "PreserveFULLlivehistory. Published84/1228,1144remain; compatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)
now = datetime.now().astimezone().isoformat()
record = {
    "schemaVersion": 1, "execution": 347, "batch": "058",
    "status": "native-assertions-passed-pending-independent-visual",
    "recordedAt": now, "startingHead": progress["execution347StartingState"]["startingHead"],
    "scope": progress["execution347StartingState"]["scope"],
    "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
    "nativeExecution": receipt,
    "terminalCases": [
        {"class": "N1Batch058GlyphTest", "test": "hillLookalikesRadicalAndSupportWordsAcrossFourProductionFamilies", "status": 0},
        {"class": "N1Batch058ArticleTest", "test": "fullSingleImportOfflineHillThreeReciprocalPairsBothCuratedReadingsDrawingAndSystemBack", "status": 0},
    ],
    "durationSeconds": 102.361, "failedCases": 0, "skippedCases": 0,
    "nativeRawLog": str((destination / "instrumentation.txt").relative_to(root)),
    "rawLogSha256": sha(destination / "instrumentation.txt"),
    "productionImportEvidence": route,
    "reciprocalPairs": [["丘", "丘"], ["丘", "砂丘"], ["砂", "砂丘"]],
    "directedReciprocalTransitions": 6,
    "glyphEvidence": {
        "individualPaintProbes": 28, "wholeWordRasterProbes": 8, "productionComposeRows": 4,
        "directCoordinatorImageRequests": direct_images,
        "observation": "Four production font rows show distinct readable丘兵近共 and readable一砂山/丘/砂丘, no blank/replacement boxes. N1 selection shows90cards. Both curated questions/feedback displayキュウ andおか as sole keyed answers, matching successful persistent-grade assertions. Reused丘 image shows both examples/kana/English and component link; new砂丘 image shows both component links, readings/alternatives and geographical boundaries. さきゅう wraps inside paragraph without clipping. Sand-forwardlink route returns砂丘. Drawing feedback shows five numbered reference strokes/matching touch trace/practice-only/handwriting-model-unavailable qualification.",
        "limits": "Ten direct coordinator image inspections only; remaining PNGs not coordinator-inspected. Actual fallback face not identified. Not independent visual approval or physical-phone evidence; native raster hashes alone do not prove readability.",
    },
    "artifactIndex": str(index_path.relative_to(root)), "artifactIndexSha256": sha(index_path),
    "sourcePngCount": png_count, "postrunVerification": postrun,
    "accepted345AndroidRetainedWithoutRerun": True,
    "original346ArtifactsAndOriginalReportHashesReverified": True,
    "runtimeEditsMade": False, "harnessEditsAfterExecution": False,
    "nativeExecuted": True, "nativeAssertionsPassed": True,
    "nativeAcceptance": False, "independentVisualAcceptance": False,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "publishedAdditions": 84, "remainingAdditions": 1144,
    "nextAction": next_action,
    "limits": "Native assertions passed with separate cleanup inventory; independent visual/batch acceptance and phone acceptance pending. Unique disposable source/syntheticHEAD/full production archive import; due-state fixture/reference-touch trace/recallmiss not learning efficacy/human recall/MLKit evidence. No teaching or runtime changes/reviewer/publication/059. Original Claude3 overlaps/noncompliance and bounded confirmation limits remain; strict original process acceptance not claimed. Original344 permission denial and049 host-only heap qualification preserved. Overall project incomplete.",
}
record_path = root / "docs" / "n1-sources" / "execution-347.json"
assert not record_path.exists()
save(record_path, record)
batch_path = root / "docs" / "n1-sources" / "batch-058-progress.json"
batch = load(batch_path)
batch["status"] = record["status"]
batch["nativeExecutionCheckpoint"] = "execution-347.json"
batch["nativeAssertionEvidence"] = record["artifactIndex"]
batch["nextAction"] = next_action
save(batch_path, batch)
state = {
    **progress["execution347StartingState"], "status": record["status"],
    "record": str(record_path.relative_to(root)), "recordedAt": now,
}
progress["execution347StartingState"] = state
checkpoint = {
    "execution": 347, "batch": "058", "status": record["status"],
    "record": str(record_path.relative_to(root)),
    "startingHead": record["startingHead"], "savedCommit": None,
    "nativeAssertionsPassed": True, "independentVisualAcceptance": False,
    "sourcePngCount": png_count, "coordinatorDirectImages": len(direct_images),
    "postrunVerifiedClean": True, "nextAction": next_action, "checkpointedAt": now,
}
progress.update({
    "checkpoint": 347, "status": "continue",
    "stage": "batch-058-native-passed-pending-independent-visual",
    "blocker": None, "nextAction": next_action, "activeExecution": state,
    "execution347CoordinatorCheckpoint": checkpoint,
    "batch058NativeExecutionCheckpoint": checkpoint,
})
mutable = {"checkpoint", "status", "stage", "blocker", "nextAction", "activeExecution", "execution347StartingState"}
for key in before.keys() - mutable:
    assert progress[key] == before[key], key
save(progress_path, progress)
print(json.dumps({
    "record": str(record_path), "archivedFiles": len(artifacts), "sourcePngCount": png_count,
    "directImageCount": len(direct_images), "checkpoint": 347, "status": progress["status"],
    "historicalRootKeysPreserved": len(before.keys() - mutable),
}, ensure_ascii=False, indent=2))
