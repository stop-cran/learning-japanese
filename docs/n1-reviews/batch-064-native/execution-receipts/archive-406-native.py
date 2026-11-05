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
before = load(control / "execution-406-progress-before.json")
assert progress["checkpoint"] == 405 and progress["batch"] == "064"
receipt = load(control / "batch-064-native-attempt-1-execution.json")
assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
assert receipt["parentEmulatorPid"] == 11024 and receipt["qemuPid"] == 14968
assert receipt["prelaunch"]["connections"] == []
assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
preparation = load(root / "docs" / "n1-sources" / "batch-064-native-preparation.json")
compiled = load(root / "docs" / "n1-sources" / "execution-405.json")
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

source = control / "artifacts" / "batch-064-native-attempt-1"
destination = root / "docs" / "n1-reviews" / "batch-064-native" / "attempt-1"
assert not destination.exists()
destination.mkdir()
expected_files = set(receipt["artifacts"]) | {
    "N1Batch064NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
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
assert "Time: 160.379" in raw and "OK (2 tests)" in raw
for cls, name in (
    ("N1Batch064GlyphTest", "investigationLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
    ("N1Batch064ArticleTest", "fullSingleImportOfflineInvestigationTwoPairsComparisonOnOnlyDrawingAndSystemBack"),
):
    assert raw.count(f"INSTRUMENTATION_STATUS: test={name}") == 2
    assert raw.count(f"INSTRUMENTATION_STATUS: class=io.github.stopcran.kanji.ui.{cls}") == 2
route = load(destination / "n1-064-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1
assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1076, 5034, 96, 0, 1]
assert route["contentSnapshot"] == preparation["contentSnapshot"]
assert route["contentVersion"] == "ae05977ba66f42f5"
assert route["fullOnyomi"] == ["テイ"] and route["fullKunyomi"] == []
assert route["quizOnKeys"] == ["てい"] and route["quizKunKeys"] == []
for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
            "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
            "drawingGradeRecordedOnNext", "offline"):
    assert route[key] is True, key
assert route["touchInjectedReferenceStrokes"] == 11 and route["phoneEvidence"] is False
raster = load(destination / "n1-064-font-raster.json")
assert raster["individualGlyphProbes"] == 40 and raster["wholeWordRasterProbes"] == 8
assert len(raster["rows"]) == 48
for font in ("Gothic", "Mincho", "Textbook", "Brush"):
    glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
    assert {row["character"] for row in glyphs} == set("偵貞停低値人亻探手扌")
    assert all(row["hasGlyph"] for row in glyphs)
    assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 10
    words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
    assert {row["word"] for row in words} == {"探偵", "刑事"}
    assert all(row["renderedCharactersNonblank"] == 2 for row in words)
images = ["n1-064-font-pairs.png", "n1-064-detective-particles-and-activity.png"]
assert all((destination / name).is_file() for name in images)
png_count = sum("dimensions" in entry for entry in artifacts)
denied_command = (
    "$ErrorActionPreference='Stop'; $record=[ordered]@{execution=406;recordedAt=[DateTimeOffset]::Now.ToString('o');"
    "contentHead=(git rev-parse HEAD);contentStatus=@(git status --porcelain);androidHead=(git -C "
    "C:\\Users\\stop-\\n1-kanji-workspace\\kanji-cards-android rev-parse HEAD);androidStatus=@(git -C "
    "C:\\Users\\stop-\\n1-kanji-workspace\\kanji-cards-android status --porcelain)}; $record.devices=(& "
    "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe devices -l | Out-String); "
    "if($LASTEXITCODE -ne 0){throw 'adb inventory failed'}; $owned=@(Get-Process -Id 11024,14968 "
    "-ErrorAction SilentlyContinue); $record.ownedProcessesRemaining=$owned.Count; "
    "$record.connections=@(Get-NetTCPConnection -ErrorAction Stop | Where-Object {$_.LocalPort -in 5580,5581 "
    "-or $_.RemotePort -in 5580,5581} | Select-Object LocalAddress,RemoteAddress,LocalPort,RemotePort,State,OwningProcess); "
    "$record | ConvertTo-Json -Depth 6 | Set-Content C:\\Users\\stop-\\n1-kanji-workspace\\control\\execution-406-postrun-verification.json "
    "-Encoding utf8NoBOM; $record | ConvertTo-Json -Depth 6"
)
next_action = (
    "Approval-capable parent should resolve EXACT execution406 denied post-native read-only dedicated-worktree/"
    "device/ownedPID11024+14968/local+remote5580-5581 verification command, preserving denial; no retry, alternative "
    "invocation, permission/configuration change or disguised execution. SAME064 only; no065 or second runner. "
    "Read docs/n1-sources/execution-406.json and batch-064-native/execution-406-artifact-index.json/attempt-1. "
    "Both named cases actually PASSED terminal0/no skips/160.379s, exact fullbf6204e5 Git envelope productionContentSyncONCE "
    "1076kanji5034words96N1/ae05977ba66f42f5/problems0/epoch1. Full+Lite orderedテイ/emptykun, "
    "explicit curated subsets and soleてい/noKunLog; both mappedpairs偵-探偵/探-探偵 fourdirections and "
    "刑事-探偵 comparison bothdirections/SystemBack/offline/meaning/soleOnGoodpersisted/elevenreference"
    "touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain passed. Owned read-only API35emulator5580 "
    "parent11024/QEMU14968 reportedly stopped by launcher emukill0; independent postrun verification DENIED, "
    "so no independent cleanup/shared-device preservation claim. 40singlePaint+8wholewordprobes passed; "
    f"{png_count}PNGs archived, only2direct coordinator image inspections. Fourproductionfontrows readable "
    "偵貞停低値人亻探手扌/探偵/刑事 without blankboxes; Textbook探偵 wraps betweencharacters; actualfallbackfaces "
    "notidentified. Detectiveparticles/activityparagraph wraps legibly; not fullarticle/screenshots inspection. "
    "Rasterhashes notreadability; drawingreference/recallmiss notMLKit/correcthumanrecall. After exact parentcleanup "
    "recovery archive it separately; do NOT rerun passed native or accepted404Android3+1 absentnewconcern. "
    "Then bounded dependent originalClaude28a561c9-9201-40a9-a3a1-c9e37c6d168a and "
    "GPT1d30e91b-c5ed-4bd0-8d74-2177b9fbb0d7 visuals SERIALly, not blindinitials. Preserve402textualclosure/"
    "originalreports/read-depth/lookup/citation/process limits. Latestmain normalnonrewriting integration/"
    "allcombinedsource-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/originalbudgets/"
    "normalsigning/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/"
    "terminalreceipts/ownerissue60 stillrequired BEFOREdelivery or065. Published90/1228,1138remain; "
    "localdraft91 NOTdelivered; compatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding."
)
now = datetime.now(timezone.utc).isoformat()
blocker = {
    "schemaVersion": 1, "execution": 406, "batch": "064", "kind": "execution-permission",
    "gate": "Independent post-native dedicated-worktree/device/owned-PID/port verification",
    "attempts": 1, "deniedCommand": denied_command,
    "message": "Permission denied because no interactive user response was available. Retry in an interactive session so the user can approve it, or try an alternative that does not require this permission.",
    "limits": "Denied before execution; exact trigger unavailable. Native cases passed and launcher records owned-helper/QEMU stopped, but independent postrun status/device/process/port verification did not execute. Not a native/test/glyph/signing failure.",
    "disposition": "Preserve/report/yield; no retry or alternate command, no permission/configuration changes.",
    "savedStartingCommit": progress["execution406StartingState"]["startingHead"],
    "safeNextAction": next_action, "recordedAt": now,
}
save(control / "execution-406-permission-blocker.json", blocker)
receipts_dir = destination.parent / "execution-receipts"
assert not receipts_dir.exists()
receipts_dir.mkdir()
for path in (control / "start-406.py", control / "run-406-native.ps1", Path(__file__),
             control / "execution-406-permission-blocker.json"):
    target = receipts_dir / path.name
    shutil.copyfile(path, target)
    assert sha(target) == sha(path)
    artifacts.append({"path": str(target.relative_to(root)), "bytes": target.stat().st_size, "sha256": sha(target)})
index_path = destination.parent / "execution-406-artifact-index.json"
save(index_path, {
    "schemaVersion": 1, "execution": 406, "batch": "064", "attempt": 1,
    "files": artifacts, "sourcePngCount": png_count, "directCoordinatorImageRequests": images,
    "limits": "Two direct coordinator image inspections only; other PNGs not visually inspected. Hashes establish bytes, not readability. Independent visual review and postrun cleanup verification pending.",
})
record = {
    "schemaVersion": 1, "execution": 406, "checkpoint": 406, "batch": "064",
    "status": "native-passed-postrun-verification-permission-blocked",
    "startingHead": progress["execution406StartingState"]["startingHead"],
    "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
    "nativeExecution": receipt, "artifactIndex": str(index_path.relative_to(root)),
    "artifactIndexSha256": sha(index_path), "sourcePngCount": png_count,
    "directCoordinatorImageRequests": images,
    "visualObservations": "Four font rows render 偵/貞/停/低/値/人/亻/探/手/扌 and both words without blank boxes. Characters remain distinguishable; Textbook wraps 探偵 between its characters. Actual fallback faces not identified. Detective particles/activity paragraph and linked components wrap legibly; the final comparison continues below the viewport. Other screenshots and complete articles not visually inspected.",
    "independentPostrunVerification": False, "independentVisualAcceptance": False,
    "accepted404AndroidRetainedWithoutRerun": True,
    "runtimeEditsMade": False, "reviewersLaunched": 0, "publicationAttempted": False,
    "blocker": blocker, "nextAction": next_action,
    "publishedAdditions": 90, "remainingAdditions": 1138,
    "wholeProjectComplete": False, "recordedAt": now,
}
save(root / "docs" / "n1-sources" / "execution-406.json", record)
batch_path = root / "docs" / "n1-sources" / "batch-064-progress.json"
batch = load(batch_path)
batch["status"] = "native-passed-postrun-verification-permission-blocked"
batch["nativeExecutionCheckpoint"] = {
    "execution": 406, "record": "execution-406.json", "terminalSuccessCases": 2,
    "nativePassed": True, "independentPostrunVerification": False,
    "independentVisualAcceptance": False, "publicationAttempted": False,
    "limits": "Launcher reports owned helper stopped; independent postrun verification command denied. Original textual closure and accepted404Android unchanged. No cleanup or full batch acceptance inferred.",
}
save(batch_path, batch)
progress.update(checkpoint=406, status="blocked", stage="batch-064-native-passed-postrun-verification-blocked",
                blocker=blocker, nextAction=next_action)
progress["execution406StartingState"]["status"] = "native-passed-postrun-verification-permission-blocked"
summary = {key: value for key, value in record.items() if key != "nativeExecution"}
summary["nativePassed"] = True
summary["terminalSuccessCases"] = 2
summary["ownedHelperAndQemuStoppedPerLauncherReceipt"] = True
progress["execution406CoordinatorCheckpoint"] = summary
progress["batch064NativeExecutionCheckpoint"] = summary
progress["activeExecution"] = summary
for key in before.keys() - {"checkpoint", "status", "stage", "blocker", "nextAction", "activeExecution"}:
    assert progress[key] == before[key], key
save(progress_path, progress)
body = (
    "Batch 064 native checks passed, but the next read-only cleanup verification was permission-denied.\n\n"
    "Both named cases returned terminal status 0 with no skips (160.379 s). The exact full signed `bf6204e5` "
    "archive went through production ContentSync once: 1,076 kanji / 5,034 words / 96 N1, "
    "`ae05977ba66f42f5`, zero problems, parser epoch 1. Sole curated `てい` / no kun, all four mapped "
    "reciprocal directions, both 刑事/探偵 comparison directions, offline/System Back/meaning, persisted "
    "reading grade, eleven reference touch strokes and persisted drawing miss passed. Forty glyph and eight "
    "whole-word raster probes passed. Two direct coordinator image inspections found the four font rows "
    "readable and the detective explanation wrapping legibly; not independent visual acceptance, ML Kit "
    "recognition or physical-phone evidence.\n\n"
    "The owned API35 helper `emulator-5580` (parent 11024 / QEMU 14968) was stopped according to the "
    "launcher receipt (`emu kill` exit 0; both PIDs absent there). The separate postrun worktree/device/"
    "PID/port verification command was denied before execution. Its exact command/error and all original "
    f"native artifacts ({png_count} PNGs) are preserved in `docs/n1-sources/execution-406.json` and "
    "`docs/n1-reviews/batch-064-native/attempt-1`; no retry, alternate command or permission changes. "
    "Independent cleanup/shared-device preservation verification remains blocked. An approval-capable "
    "parent must resolve that exact command, then resume the same batch's original-session serial visual "
    "confirmations and remaining integration/publication gates without rerunning accepted native/Android "
    "checks absent a new concern.\n\n"
    "No runtime push or batch 065. Published 90/1,228; 1,138 remain. Compatible Android `f9b59a2`+ "
    "required; physical-phone/general-release and whole-set acceptance remain outstanding."
)
(control / "execution-406-issue-body.txt").write_text(body + "\n", encoding="utf-8")
print(f"Archived {len(artifacts)} exact artifacts, {png_count} PNGs; checkpoint406 BLOCKED, history preserved.")
