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
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-060-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "99d8ace026aaf5cf76b4adada34b14e969d10d4e"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
SESSION = "8327db1a-6be4-4e90-9f27-d86089e17e4e"
NEXT = (
    "SAME060 signed compiled native-preparation checkpoint366. NEXT bounded gate: execute "
    "control/artifacts/n1-batch-060-native-test.apk using N1Batch060GlyphTest and "
    "N1Batch060ArticleTest against exact full signed99d8ace0 Git envelope; read "
    "docs/n1-sources/execution-366.json and batch-060-native-preparation.json. "
    "Fresh adb/device and all local/remote5580-5581 connection/PID ownership immediately before "
    "known read-only N3_Acceptance_20261029 API35 hostGPU Vulkan-disabled helper at explicit "
    "emulator-5580; full SDK emulator flags -port5580 -read-only -no-snapshot -no-window "
    "-no-audio -gpu host -feature -Vulkan -memory2048 -cores2. Record actual owned parent/QEMU; "
    "stop ONLY owned helper. 040 alternate-port exception NOT inherited. No production/content/"
    "font/guest-app-heap/archive-guard changes. Full archive through productionContentSyncONCE "
    "with1072kanji5031words92N1/dbf047f0c2e6cd56/problems0/epoch1; Lite+Full full ordered "
    "テイチン/emptykun and curatedテイ/[]; normalizedてい/no-kun. BOTH terminalcase0/"
    "no skips/rawlogs/direct PNG inspection of亭停京享高亠亻冖丁小子口料/料亭 in four production font "
    "rows; actual亠亻冖 fallback pending. New料亭 article plus changed料 reciprocal entry; "
    "BOTH pairs亭-料亭/料-料亭 in FOUR directions/SystemBack/offline/meaning/sole curatedOn "
    "Good persistent grade/no-kun log/nine touch-reference strokes/ungraded trace/recall miss/"
    "persistedDrawAgain. 52 singlePaint+4 fullword probes planned;45 complete-article static "
    "selectors/27 article capture steps audited, NOT native acceptance. Rasterhashes not "
    "readability/fallback-face identification; offline reference/recallmiss not MLKit or "
    "correct human recall. Accepted365 freshAndroid3+1 retained without rerun absent new concern. "
    "After nativePASS use ORIGINAL two different-family reviewer sessions SERIALly for bounded "
    "dependent visuals, not new blind initials; actual session IDs preserved in execution366. "
    "Preserve original initial reports and363 textual closure on ea1dac1a; original Claude060-P1/P2 "
    "process noncompliance remains historical; supervised dependent lexical remediation is NOT "
    "retroactive strict initial acceptance. Then latestmain normal nonrewriting integration/"
    "allcombined source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/"
    "terminalreceipts/ownerissue60 BEFOREdelivery or061. Original364 permission denial and"
    "049HOST512MiBOOM remain historical; qualified host-only1GiB init unchanged. "
    "Actual permission denial/signing wait: preserve exact command/error, report/yield; no retry/"
    "workaround. No059rerun/061/secondrunner/concurrentheavywork/supervisor changes. Preserve FULL "
    "live history. Published86/1228,1142remain; compatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overall project incomplete."
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd,
                                   encoding="utf-8").strip()


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


if not sys.argv[1:]:
    assert git("rev-parse", "HEAD") == HEAD
    assert git("diff", "--name-only") == "docs/n1-authoring-notes.md"
    preparation = load(CONTROL / "batch-060-native-fixture-verification.json")
    assert sha(Path(preparation["fixture"])) == preparation["fixtureSha256"]
    assert sha(Path(preparation["archive"])) == preparation["archiveSha256"]
    apk = CONTROL / "artifacts" / "n1-batch-060-native-test.apk"
    with zipfile.ZipFile(apk) as package:
        asset = package.read("assets/n1-batch-060-99d8ace0-envelope.zip")
        assert hashlib.sha256(asset).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist()
               if name.startswith("classes") and name.endswith(".dex")]
        for kind in ("Glyph", "Article"):
            current = f"Lio/github/stopcran/kanji/ui/N1Batch060{kind}Test;".encode()
            assert any(current in blob for blob in dex), current
            obsolete = f"Lio/github/stopcran/kanji/ui/N1Batch059{kind}Test;".encode()
            assert all(obsolete not in blob for blob in dex), obsolete
        for method in (
            "pavilionLookalikesAndThreeFallbackComponentsAcrossFourProductionFamilies",
            "fullSingleImportOfflinePavilionTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
        ):
            assert any(method.encode() in blob for blob in dex), method
    raw_log = CONTROL / "logs" / "execution-366-native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert "BUILD SUCCESSFUL in 56s" in compile_text
    assert "56 actionable tasks: 9 executed, 47 up-to-date" in compile_text
    assert (CONTROL / "logs" / "execution-366-native-compile-exit.txt").read_text().strip() == "0"
    archived_log = FOLDER / "compile.txt"
    assert not archived_log.exists()
    archived_log.write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n",
                            encoding="utf-8")
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    for name in ("start-366.py", "prepare-366-native.py", "run-366-native-compile.ps1", "finish-366.py"):
        shutil.copyfile(CONTROL / name, receipts / name)
    for relative in (
        r"app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch060NativeTest.kt",
        r"app\src\androidTest\assets\n1-batch-060-99d8ace0-envelope.zip",
    ):
        assert not (ANDROID / relative).exists()
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version dbf047f0c2e6cd56")):
        path = CONTROL / "logs" / f"execution-366-{name}.txt"
        assert expected in path.read_text(encoding="utf-8-sig")
        checks.append({"check": name, "exitCode": 0, "log": str(path), "sha256": sha(path)})
    assert len(preparation["staticMarkdownSelectors"]) == 45
    assert preparation["captureSteps"] == 27
    assert len(preparation["articleRouteTransitions"]) == 4
    source = Path(preparation["fixture"]).read_text(encoding="utf-8")
    glyphs = re.findall(r'"([^"]+)"', re.search(r'for \(char in listOf\((.*?)\)\)', source).group(1))
    assert glyphs == preparation["plannedGlyphs"] and len(set(glyphs)) == 13
    assert source.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in source
    compilation = {
        "status": "compiled-not-executed", "exitCode": 0,
        "result": "BUILD SUCCESSFUL in56s;56 tasks:9 executed,47 up-to-date",
        "log": str(archived_log.relative_to(ROOT)), "logSha256": sha(archived_log),
        "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
        "normalization": "Archive UTF-8 LF/trailing-whitespace normalization only; complete raw log retained.",
        "launcher": str(receipts.relative_to(ROOT) / "run-366-native-compile.ps1"),
        "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
        "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
        "packagedExactFullArchiveVerified": True, "bothBatch060ClassDescriptorsAndMethodsPresent": True,
        "oldBatch059ClassDescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
        "androidWhollyClean": True,
        "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
        "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
        "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
    }
    preparation.update(
        status="native-compiled-pending-execution", compilation=compilation, checks=checks,
        nextAction=NEXT,
        projectionQualification="Bounded plain-text heading/paragraph/bullet/table projection inspected against current production core/markdown/Markdown.kt; these three articles use its supported subset. This is not a native semantics-tree assertion.",
    )
    preparation_path = SOURCES / "batch-060-native-preparation.json"
    assert not preparation_path.exists()
    save(preparation_path, preparation)
    artifact_paths = sorted(path for path in FOLDER.rglob("*") if path.is_file()) + [preparation_path]
    sessions = []
    for family in ("claude", "gpt"):
        process = load(CONTROL / f"batch-060-initial-{family}-process.json")
        sessions.append({"family": family, "sessionId": process["sessionId"],
                         "requestedModel": process["requestedModel"],
                         "identityEvidence": "docs/n1-reviews/batch-060-initial-review-checkpoint.json"})
    record = {
        "schemaVersion": 1, "execution": 366, "batch": "060", "status": preparation["status"],
        "startingHead": HEAD,
        "scope": load(CONTROL / "progress.json")["execution366StartingState"]["scope"],
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
            "completeArticleSelectors": 45, "articleCaptureSteps": 27,
            "method": preparation["projectionQualification"],
            "originalHarness": preparation["reusedAcceptedHarness"],
            "originalHarnessSha256": preparation["reusedAcceptedHarnessSha256"],
            "reciprocalPairs": 2, "directedTransitions": 4,
        },
        "accepted365AndroidRetainedWithoutRerun": True,
        "originalReviewerSessionsForLaterDependentVisualConfirmation": sessions,
        "originalInitialReportHashesUnchanged": preparation["originalInitialReportHashesUnchanged"],
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 86, "remainingAdditions": 1142,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    verify(record)
    save(SOURCES / "execution-366.json", record)
    batch_path = SOURCES / "batch-060-progress.json"
    batch = load(batch_path)
    batch.update(status="native-compiled-pending-execution",
                 nativePreparation="batch-060-native-preparation.json",
                 nativePreparationCheckpoint="execution-366.json", nextAction=NEXT)
    save(batch_path, batch)
    print(json.dumps({"status": record["status"], "artifacts": len(record["artifacts"]),
                      "apkSha256": compilation["apkSha256"], "runtimeUnchanged": True,
                      "nativeExecuted": False}, indent=2))
else:
    assert sys.argv[1:] in (["checkpoint"], ["close"])
    record = load(SOURCES / "execution-366.json")
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
    compared = 0
    for key, value in original.items():
        if key not in allowed:
            assert progress[key] == value, key
            compared += 1
    if sys.argv[1:] == ["checkpoint"]:
        assert progress["checkpoint"] == 365
        checkpoint = {
            "schemaVersion": 1, "execution": 366, "batch": "060", "status": record["status"],
            "record": "docs/n1-sources/execution-366.json", "savedCommit": saved_head,
            "signature": "G", "recordedAt": datetime.now(timezone.utc).isoformat(),
            "scope": record["scope"], "compilation": record["compilation"],
            "staticSelectors": 45, "articleCaptureSteps": 27, "reciprocalPairs": 2,
            "directedReciprocalTransitions": 4, "contentVersion": record["contentVersion"],
            "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
            "publicationAttempted": False, "nextAction": NEXT,
            "publishedAdditions": 86, "remainingAdditions": 1142,
        }
        progress.update(checkpoint=366, status="continue",
                        stage="batch-060-native-compiled-pending-execution",
                        blocker=None, nextAction=NEXT)
        progress["execution366StartingState"]["status"] = "completed-bounded-native-preparation-checkpoint"
        progress["execution366CoordinatorCheckpoint"] = checkpoint
        progress["batch060NativePreparationCheckpoint"] = checkpoint
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-366-checkpoint.json", checkpoint)
        body = (
            f"Batch **060 / 亭**: exact-full-archive native fixture prepared and compiled in "
            f"normally signed local checkpoint `{saved_head}` (execution366). **Not published; "
            "native execution remains next.**\n\n"
            "The complete `99d8ace0` Git envelope preserves all **8,309 runtime hashes / "
            "8,331 ZIP entries** and existing byte budgets. Content version remains "
            "`dbf047f0c2e6cd56`: **1,072 kanji / 5,031 words / 92 N1 cards**. Both current "
            "test classes and the exact archive were verified inside the APK. Prepared "
            "coverage includes **テイ / no kun**, full ordered metadata, both **亭/料亭 "
            "and 料/料亭** pairs in four directions, System Back, offline routes, meaning, "
            "persisted on-reading feedback and nine-stroke drawing. **45 static selectors / "
            "27 article capture steps**, 52 glyph probes including actual **亠/亻/冖**, and "
            "four word probes are prepared—not native or fallback-readability acceptance.\n\n"
            "Compilation passed (56s; one worker, serial). Temporary Android source/assets "
            "were removed; worktrees are clean. Execution365's fresh Android 3+1 results were "
            "retained without rerun. Original364 permission denial, qualified host-only heap "
            "evidence and original Claude060-P1/P2 noncompliance remain explicit; supervised "
            "dependent lexical remediation does not retroactively establish strict initial "
            "compliance. Next: fresh device/5580–5581 ownership check, both terminal native "
            "case0 results and direct PNG inspection, then original-session serial visual "
            "confirmation and combined-main publication gates. **86/1,228 additions published; "
            "1,142 remain.** No new runtime delivery, physical-phone/general-release or "
            "whole-set acceptance claimed. Compatible Android `f9b59a2+` required."
        )
        (CONTROL / "execution-366-issue-body.txt").write_text(body + "\n", encoding="utf-8")
        print(json.dumps({"checkpoint": 366, "savedCommit": saved_head, "status": "continue",
                          "historicalRecordsCompared": compared, "nextGate": "same060-native-execution"}, indent=2))
    else:
        assert progress["checkpoint"] == 366 and progress["status"] == "continue"
        assert progress["execution366CoordinatorCheckpoint"]["savedCommit"] == saved_head
        receipt = load(CONTROL / "execution-366-issue-receipt.json")
        assert receipt["author"] == "stop-cran" and receipt["identityVerified"]
        assert receipt["bodySha256"] == sha(CONTROL / "execution-366-issue-body.txt")
        assert receipt["runtimePublished"] is False
        verification = {
            "schemaVersion": 1, "execution": 366, "checkpoint": 366, "batch": "060",
            "status": "continue", "savedCommit": saved_head, "signature": "G",
            "changedPaths": git("diff-tree", "--no-commit-id", "--name-only", "-r", saved_head).splitlines(),
            "worktreesClean": True, "runtimeUnchanged": True,
            "committedArtifactHashesVerified": len(record["artifacts"]),
            "fullHistoricalProgressPreserved": True, "historicalRecordsCompared": compared,
            "compiledNativeFixture": True, "exactFullArchivePackaged": True,
            "staticArticleSelectors": 45, "articleCaptureSteps": 27,
            "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
            "issueUpdate": receipt["url"], "ownerAuthorAndBodyVerified": True,
            "globalIdentityUnchanged": receipt["globalIdentityUnchanged"],
            "runtimePublished": False, "wholeProjectComplete": False,
            "recordedAt": datetime.now(timezone.utc).isoformat(),
        }
        progress["execution366CoordinatorCheckpoint"].update(
            issueUpdate=receipt["url"],
            issueReceipt="control/execution-366-issue-receipt.json", verification=verification,
        )
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-366-verification.json", verification)
        print(json.dumps(verification, ensure_ascii=True, indent=2))
