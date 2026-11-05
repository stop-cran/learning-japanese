import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-058-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "00491dddddaa65467b0f7ad474689e054a00f5f4"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
SESSION = "c7400859-db52-41fe-9405-edf18a31274e"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd,
                                   encoding="utf-8").strip()


NEXT = (
    "SAME058 signed compiled native-preparation checkpoint346. NEXT bounded gate: execute "
    "control/artifacts/n1-batch-058-native-test.apk with N1Batch058GlyphTest and "
    "N1Batch058ArticleTest against exact full signed00491ddd Git envelope; read "
    "docs/n1-sources/execution-346.json and batch-058-native-preparation.json. "
    "Fresh adb/device and all local/remote5580-5581 connection/PID ownership immediately before "
    "known read-only N3_Acceptance_20261029 API35 hostGPU Vulkan-disabled helper at explicit "
    "emulator-5580; full SDK emulator flags -port5580 -read-only -no-snapshot -no-window "
    "-no-audio -gpu host -feature -Vulkan -memory2048 -cores2. Record actual owned parent/QEMU; "
    "stop ONLY owned helper. 040 alternate-port exception NOT inherited. No production/content/"
    "font/guest-app-heap/archive-guard changes. Full archive through productionContentSyncONCE "
    "with1070kanji5029words90N1/5e8f3e7e39ea187a/problems0/epoch1; Lite+Full full and curated "
    "キュウ/おか, normalizedきゅう/おか. BOTH terminalcase0/no skips/rawlogs/direct PNG inspection "
    "of丘兵近共一砂山/丘/砂丘 in four production font rows; new砂丘 and reused丘 articles plus "
    "changed砂 reciprocal entry; all THREE pairs丘-丘/丘-砂丘/砂-砂丘 in SIX directions/"
    "SystemBack/offline/meaning/BOTHcuratedGood persistent grades/five touch-reference strokes/"
    "ungraded trace/recall miss/persistedDrawAgain. 28 singlePaint+8 fullword probes planned; "
    "60 complete-article static selectors/32 article capture steps audited, NOT native acceptance. "
    "Exact full砂丘 heading avoids duplicate source-footer substring. Rasterhashes not readability/"
    "fallback-face identification; offline reference/recallmiss not MLKit or correct human recall. "
    "Accepted345 freshAndroid3+1 retained without rerun absent new concern. After nativePASS "
    "use ORIGINAL two different-family reviewer sessions SERIALly for bounded dependent visuals, "
    "not new blind initials. Preserve original58b53fd3 reports/initialClaude3overlaps/historical "
    "noncompliance; bounded remediation is NOT retroactive strict acceptance. Then latestmain "
    "normal nonrewriting integration/allcombined source-baseline-reading-link-font-stroke/Python/"
    "vocab/validator/freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained "
    "budgets/normal signing/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIP"
    "runtimehash/terminalreceipts/ownerissue60 BEFOREdelivery or059. Original344 permission "
    "denial and049HOST512MiBOOM remain historical; qualified host-only1GiB init unchanged. "
    "Actual permission denial/signing wait: preserve exact command/error, report/yield; no retry/"
    "workaround. No057rerun/059/secondrunner/concurrentheavywork/supervisor changes. Preserve FULL "
    "live history. Published84/1228,1144remain; compatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overall project incomplete."
)


def verify(record):
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"], path
        assert sha(path) == item["sha256"], path
    for name in ("fixture", "archive"):
        assert sha(Path(record[name])) == record[f"{name}Sha256"]
    assert sha(Path(record["compilation"]["apk"])) == record["compilation"]["apkSha256"]
    assert not git("status", "--porcelain", cwd=ANDROID)
    assert git("rev-parse", "HEAD", cwd=ANDROID) == APP_HEAD
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for name, expected in record["originalInitialReportHashesUnchanged"].items():
        assert sha(ROOT / name) == expected


if sys.argv[1:] in (["checkpoint"], ["close"]):
    record = load(SOURCES / "execution-346.json")
    verify(record)
    saved_head = git("rev-parse", "HEAD")
    assert saved_head != HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    for item in record["artifacts"]:
        committed = subprocess.check_output(
            ["git", "show", f"{saved_head}:{Path(item['path']).as_posix()}"], cwd=ROOT)
        assert hashlib.sha256(committed).hexdigest() == item["sha256"]
    progress = load(CONTROL / "progress.json")
    original = load(CONTROL / "logs" / SESSION / "checkpoint-full.json")
    allowed = {"checkpoint", "status", "stage", "blocker", "nextAction"}
    for key, value in original.items():
        if key not in allowed:
            assert progress[key] == value, key
    if sys.argv[1:] == ["checkpoint"]:
        assert progress["checkpoint"] == 345
        checkpoint = {
            "schemaVersion": 1, "execution": 346, "batch": "058", "status": record["status"],
            "record": "docs/n1-sources/execution-346.json", "savedCommit": saved_head,
            "signature": "G", "recordedAt": datetime.now(timezone.utc).isoformat(),
            "scope": record["scope"], "compilation": record["compilation"],
            "staticSelectors": 60, "articleCaptureSteps": 32, "reciprocalPairs": 3,
            "directedReciprocalTransitions": 6, "contentVersion": record["contentVersion"],
            "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
            "publicationAttempted": False, "nextAction": NEXT,
            "publishedAdditions": 84, "remainingAdditions": 1144,
        }
        progress.update(checkpoint=346, status="continue",
                        stage="batch-058-native-compiled-pending-execution",
                        blocker=None, nextAction=NEXT)
        progress["execution346StartingState"]["status"] = "completed-bounded-native-preparation-checkpoint"
        progress["execution346CoordinatorCheckpoint"] = checkpoint
        progress["batch058NativePreparationCheckpoint"] = checkpoint
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-346-checkpoint.json", checkpoint)
        body = (
            f"Batch **058 / 丘**: full-archive native fixture prepared and compiled in normally "
            f"signed local checkpoint `{saved_head}` (execution346). **Not published; native "
            "execution remains next.**\n\n"
            "The exact full `00491ddd` Git envelope preserves all **8,303 runtime hashes**, "
            "**8,325 ZIP entries** and the existing byte budgets. Manifest remains "
            "`5e8f3e7e39ea187a`: **1,070 kanji / 5,029 words / 90 N1 cards**. Both test "
            "classes and the exact archive were verified inside the compiled APK. The fixture "
            "covers both curated readings, new 砂丘 and reused 丘 articles, the changed 砂 "
            "entry and **all three reciprocal pairs / six link directions**, System Back, "
            "offline routes, meaning and five-stroke drawing. **60 selectors / 32 article "
            "capture steps**, 28 glyph probes and eight complete-word probes are prepared, "
            "not native acceptance. Static preflight caught an ambiguous 砂丘 heading/footer "
            "substring; the fixture now selects the exact complete heading.\n\n"
            "Compilation passed (one minute; one worker, no parallel heavy work). Temporary "
            "Android source/asset were removed; dedicated worktrees are clean. Execution345's "
            "fresh Android 3+1 results were retained without rerun. Original344 permission "
            "denial, qualified host-only heap evidence and initial reviewer process limitations "
            "remain explicit. Next: fresh device/5580–5581 ownership check, native execution "
            "with both terminal case0 results and direct PNG inspection, then original-session "
            "serial visual confirmation and combined-main publication gates. **84/1,228 "
            "additions published; 1,144 remain.** No new runtime delivery, physical-phone/"
            "general-release or whole-set acceptance claimed. Compatible Android `f9b59a2+` required."
        )
        (CONTROL / "execution-346-issue-body.txt").write_text(body + "\n", encoding="utf-8")
        print(json.dumps({"checkpoint": 346, "savedCommit": saved_head, "status": "continue",
                          "nextGate": "same058-native-execution"}, indent=2))
    else:
        assert progress["checkpoint"] == 346 and progress["status"] == "continue"
        assert progress["execution346CoordinatorCheckpoint"]["savedCommit"] == saved_head
        receipt = load(CONTROL / "execution-346-issue-receipt.json")
        assert receipt["author"] == "stop-cran" and receipt["identityVerified"]
        assert receipt["bodySha256"] == sha(CONTROL / "execution-346-issue-body.txt")
        assert receipt["runtimePublished"] is False
        verification = {
            "execution": 346, "checkpoint": 346, "batch": "058",
            "savedCommit": saved_head, "signature": "G", "dedicatedWorktreesClean": True,
            "runtimeUnchanged": True, "compiledApkHashVerified": True,
            "exactArchiveHashVerified": True, "archivedArtifactHashesVerified": len(record["artifacts"]),
            "historicalRootKeysPreserved": len(original), "liveRootKeys": len(progress),
            "nativePerformed": False, "runtimePublished": False,
            "publishedAdditions": 84, "remainingAdditions": 1144, "wholeProjectComplete": False,
            "issueUpdate": receipt["url"], "verifiedAt": datetime.now(timezone.utc).isoformat(),
        }
        for key in ("execution346CoordinatorCheckpoint", "batch058NativePreparationCheckpoint"):
            progress[key].update(issueUpdate=receipt["url"],
                                 issueReceipt="control/execution-346-issue-receipt.json",
                                 verification=verification, checkpointedAt=verification["verifiedAt"])
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-346-final-verification.json", verification)
        assert load(CONTROL / "progress.json")["batch058NativePreparationCheckpoint"]["savedCommit"] == saved_head
        print(json.dumps(verification, ensure_ascii=False, indent=2))
    sys.exit(0)

assert not sys.argv[1:]
assert git("rev-parse", "HEAD") == HEAD
assert git("diff", "--name-only") == "docs/n1-authoring-notes.md"
preparation = load(CONTROL / "batch-058-native-fixture-verification.json")
assert sha(Path(preparation["fixture"])) == preparation["fixtureSha256"]
assert sha(Path(preparation["archive"])) == preparation["archiveSha256"]
apk = CONTROL / "artifacts" / "n1-batch-058-native-test.apk"
with zipfile.ZipFile(apk) as package:
    asset = package.read("assets/n1-batch-058-00491ddd-envelope.zip")
    assert hashlib.sha256(asset).hexdigest() == preparation["archiveSha256"]
    dex = [package.read(name) for name in package.namelist()
           if name.startswith("classes") and name.endswith(".dex")]
    for kind in ("Glyph", "Article"):
        current = f"Lio/github/stopcran/kanji/ui/N1Batch058{kind}Test;".encode()
        assert any(current in blob for blob in dex), current
        obsolete = f"Lio/github/stopcran/kanji/ui/N1Batch057{kind}Test;".encode()
        assert all(obsolete not in blob for blob in dex), obsolete
    for method in (
        "hillLookalikesRadicalAndSupportWordsAcrossFourProductionFamilies",
        "fullSingleImportOfflineHillThreeReciprocalPairsBothCuratedReadingsDrawingAndSystemBack",
    ):
        assert any(method.encode() in blob for blob in dex), method
raw_log = CONTROL / "logs" / "execution-346-native-compile.txt"
compile_text = raw_log.read_text(encoding="utf-8-sig")
assert "BUILD SUCCESSFUL in 1m" in compile_text
assert "56 actionable tasks: 9 executed, 47 up-to-date" in compile_text
assert (CONTROL / "logs" / "execution-346-native-compile-exit.txt").read_text().strip() == "0"
archived_log = FOLDER / "compile.txt"
assert not archived_log.exists()
archived_log.write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n",
                        encoding="utf-8")
receipts = FOLDER / "preparation-receipts"
receipts.mkdir()
for name in ("start-346.py", "prepare-346-native.py", "run-346-native-compile.ps1", "finish-346.py"):
    shutil.copyfile(CONTROL / name, receipts / name)
for relative in (
    r"app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch058NativeTest.kt",
    r"app\src\androidTest\assets\n1-batch-058-00491ddd-envelope.zip",
):
    assert not (ANDROID / relative).exists()
checks = []
for name, expected in (("validate", "0 error(s)"), ("manifest", "version 5e8f3e7e39ea187a")):
    path = CONTROL / "logs" / f"execution-346-{name}.txt"
    assert expected in path.read_text(encoding="utf-8-sig")
    checks.append({"check": name, "exitCode": 0, "log": str(path), "sha256": sha(path)})
assert len(preparation["staticMarkdownSelectors"]) == 60
assert preparation["captureSteps"] == 32
assert len(preparation["articleRouteTransitions"]) == 6
compilation = {
    "status": "compiled-not-executed", "exitCode": 0,
    "result": "BUILD SUCCESSFUL in1m;56 tasks:9 executed,47 up-to-date",
    "log": str(archived_log.relative_to(ROOT)), "logSha256": sha(archived_log),
    "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
    "normalization": "Archive UTF-8 LF/trailing-whitespace normalization only; complete raw log retained.",
    "launcher": str(receipts.relative_to(ROOT) / "run-346-native-compile.ps1"),
    "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
    "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
    "packagedExactFullArchiveVerified": True, "bothBatch058ClassDescriptorsAndMethodsPresent": True,
    "oldBatch057ClassDescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
    "androidWhollyClean": True,
    "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
    "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
    "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
}
preparation.update(
    status="native-compiled-pending-execution", compilation=compilation, checks=checks,
    nextAction=NEXT,
    precompileSelectorCorrection="First static preflight stopped before fixture/archive creation: partial砂丘 (さきゅう) matched both heading and source footer. Both article-entry awaits now select the exact complete砂丘 (さきゅう) - sand dune heading. Repeated static audit resolved all60selectors against four complete articles; no native run/failure, archive overwrite, teaching edit or signing attempt occurred.",
    projectionQualification="Bounded plain-text heading/paragraph/bullet/table projection inspected against current production core/markdown/Markdown.kt; these four articles use its supported subset. This is not a native semantics-tree assertion.",
)
preparation_path = SOURCES / "batch-058-native-preparation.json"
save(preparation_path, preparation)
artifact_paths = sorted(path for path in FOLDER.rglob("*") if path.is_file()) + [preparation_path]
record = {
    "schemaVersion": 1, "execution": 346, "batch": "058", "status": preparation["status"],
    "startingHead": HEAD,
    "scope": "SAME058 exact-full-archive supported-native fixture preparation, serial compilation and signed durable checkpoint only. No native launch, reviewer, runtime publication,059 or second runner.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
    "requestSha256": sha(CONTROL / "logs" / SESSION / "request.txt"),
    "preparation": str(preparation_path.relative_to(ROOT)), "preparationSha256": sha(preparation_path),
    "contentVersion": preparation["contentVersion"],
    "fixture": preparation["fixture"], "fixtureSha256": preparation["fixtureSha256"],
    "archive": preparation["archive"], "archiveSha256": preparation["archiveSha256"],
    "compilation": compilation, "checks": checks,
    "artifacts": [{"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                   "sha256": sha(path)} for path in artifact_paths],
    "selectorAudit": {
        "completeArticleSelectors": 60, "articleCaptureSteps": 32,
        "method": preparation["projectionQualification"],
        "originalHarness": preparation["reusedAcceptedHarness"],
        "originalHarnessSha256": preparation["reusedAcceptedHarnessSha256"],
        "reciprocalPairs": 3, "directedTransitions": 6,
    },
    "precompileSelectorCorrection": preparation["precompileSelectorCorrection"],
    "accepted345AndroidRetainedWithoutRerun": True,
    "originalInitialReportHashesUnchanged": preparation["originalInitialReportHashesUnchanged"],
    "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
    "independentVisualAcceptance": False, "reviewersLaunched": 0,
    "publicationAttempted": False, "publishedAdditions": 84, "remainingAdditions": 1144,
    "nextAction": NEXT, "limits": preparation["limits"],
}
verify(record)
save(SOURCES / "execution-346.json", record)
batch_path = SOURCES / "batch-058-progress.json"
batch = load(batch_path)
batch.update(status="native-compiled-pending-execution",
             nativePreparation="batch-058-native-preparation.json",
             nativePreparationCheckpoint="execution-346.json", nextAction=NEXT)
save(batch_path, batch)
print(json.dumps({"status": record["status"], "artifacts": len(record["artifacts"]),
                  "apkSha256": compilation["apkSha256"], "runtimeUnchanged": True,
                  "nativeExecuted": False}, indent=2))
