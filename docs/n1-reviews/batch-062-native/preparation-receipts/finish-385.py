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
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-062-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "e157d58c5bdb9fc2d58d7043fdf0429d36f5c040"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
SESSION = "147e9f3a-8b42-4837-9b15-839df356dd9c"
NEXT = (
    "SAME062 signed compiled native-preparation checkpoint385. NEXT bounded gate: execute "
    "control/artifacts/n1-batch-062-native-test.apk using N1Batch062GlyphTest and "
    "N1Batch062ArticleTest against exact full signede157d58c Git envelope; read "
    "docs/n1-sources/execution-385.json and batch-062-native-preparation.json. "
    "Fresh adb/device and all local/remote5580-5581 connection/PID ownership immediately before "
    "known read-only N3_Acceptance_20261029 API35 hostGPU Vulkan-disabled helper at explicit "
    "emulator-5580; full SDK emulator flags -port5580 -read-only -no-snapshot -no-window "
    "-no-audio -gpu host -feature -Vulkan -memory2048 -cores2. Record actual owned parent/QEMU; "
    "stop ONLY owned helper. 040 alternate-port exception NOT inherited. No production/content/"
    "font/guest-app-heap/archive-guard changes. Full archive through productionContentSyncONCE "
    "with1074kanji5032words94N1/545c56b5d4b4e8ef/problems0/epoch1; Lite+Full full ordered "
    "ホウ/emptykun and curatedホウ/[]; normalizedほう/no-kun. BOTH terminalcase0/no skips/"
    "rawlogs/direct PNG inspection of俸棒奉借付人亻木給糸合/俸給 in four production font "
    "rows; actual亻 fallback pending. BOTH reciprocal pairs俸-俸給/給-俸給 in FOUR directions/"
    "SystemBack/offline/meaning/sole curatedOn Good persistent grade/no-kun log/ten "
    "touch-reference strokes/ungraded trace/recall miss/persistedDrawAgain. "
    "44 singlePaint+4 fullword probes planned;46 complete-article static selectors/"
    "28 article capture steps audited, NOT native acceptance. Rasterhashes not readability/"
    "fallback-face identification; offline reference/recallmiss not MLKit or correct human "
    "recall. Accepted384 freshAndroid3+1 retained without rerun absent new concern. After "
    "nativePASS use ORIGINAL two different-family reviewer sessions SERIALly for bounded "
    "dependent visuals, not new blind initials; actual session IDs preserved in execution385. "
    "Preserve original initial reports and382 textual closure on38ab6072; original Claude062-P1/P2 "
    "process noncompliance remains historical; supervised dependent lexical remediation is NOT "
    "retroactive strict initial acceptance. Then latestmain normal nonrewriting integration/"
    "allcombined source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/"
    "terminalreceipts/ownerissue60 BEFOREdelivery or063. Original383 permission denial and"
    "049HOST512MiBOOM remain historical; qualified host-only1GiB init unchanged. Actual "
    "permission denial/signing wait: preserve exact command/error, report/yield; no retry/"
    "workaround. No061rerun/063/secondrunner/concurrentheavywork/supervisor changes. Preserve "
    "FULL live history. Published88/1228,1140remain/89necessarysupportwords; localdraft89/90"
    "NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set "
    "outstanding. Overall project incomplete."
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
    preparation = load(CONTROL / "batch-062-native-fixture-verification.json")
    for name in ("fixture", "archive"):
        assert sha(Path(preparation[name])) == preparation[f"{name}Sha256"]
    apk = CONTROL / "artifacts" / "n1-batch-062-native-test.apk"
    with zipfile.ZipFile(apk) as package:
        asset = package.read("assets/n1-batch-062-e157d58c-envelope.zip")
        assert hashlib.sha256(asset).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist()
               if name.startswith("classes") and name.endswith(".dex")]
        for kind in ("Glyph", "Article"):
            current = f"Lio/github/stopcran/kanji/ui/N1Batch062{kind}Test;".encode()
            assert any(current in blob for blob in dex), current
            obsolete = f"Lio/github/stopcran/kanji/ui/N1Batch061{kind}Test;".encode()
            assert all(obsolete not in blob for blob in dex), obsolete
        for method in (
            "salaryLookalikesAndPersonFallbackAcrossFourProductionFamilies",
            "fullSingleImportOfflineSalaryTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
        ):
            assert any(method.encode() in blob for blob in dex), method
    raw_log = CONTROL / "logs" / "execution-385-native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    result = re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0)
    tasks = re.search(r"56 actionable tasks: 9 executed, 47 up-to-date", compile_text).group(0)
    assert (CONTROL / "logs" / "execution-385-native-compile-exit.txt").read_text().strip() == "0"
    archived_log = FOLDER / "compile.txt"
    assert not archived_log.exists()
    archived_log.write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n",
                            encoding="utf-8")
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    for name in ("start-385.py", "prepare-385-native.py", "run-385-native-compile.ps1", "finish-385.py"):
        shutil.copyfile(CONTROL / name, receipts / name)
    for relative in (
        r"app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch062NativeTest.kt",
        r"app\src\androidTest\assets\n1-batch-062-e157d58c-envelope.zip",
    ):
        assert not (ANDROID / relative).exists()
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 545c56b5d4b4e8ef")):
        path = CONTROL / "logs" / f"execution-385-{name}.txt"
        assert expected in path.read_text(encoding="utf-8-sig")
        checks.append({"check": name, "exitCode": 0, "log": str(path), "sha256": sha(path)})
    assert len(preparation["staticMarkdownSelectors"]) == 46
    assert preparation["captureSteps"] == 28
    assert len(preparation["articleRouteTransitions"]) == 4
    source = Path(preparation["fixture"]).read_text(encoding="utf-8")
    glyphs = re.findall(r'"([^"]+)"', re.search(r'for \(char in listOf\((.*?)\)\)', source).group(1))
    assert glyphs == preparation["plannedGlyphs"] and len(set(glyphs)) == 11
    assert source.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in source
    compilation = {
        "status": "compiled-not-executed", "exitCode": 0,
        "result": result, "tasks": tasks,
        "log": str(archived_log.relative_to(ROOT)), "logSha256": sha(archived_log),
        "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
        "normalization": "Archive UTF-8 LF/trailing-whitespace normalization only; complete raw log retained.",
        "launcher": str(receipts.relative_to(ROOT) / "run-385-native-compile.ps1"),
        "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
        "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
        "packagedExactFullArchiveVerified": True, "bothBatch062ClassDescriptorsAndMethodsPresent": True,
        "oldBatch061ClassDescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
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
    preparation_path = SOURCES / "batch-062-native-preparation.json"
    assert not preparation_path.exists()
    save(preparation_path, preparation)
    artifact_paths = sorted(path for path in FOLDER.rglob("*") if path.is_file()) + [preparation_path]
    initial = load(ROOT / "docs" / "n1-reviews" / "batch-062-initial-review-checkpoint.json")
    sessions = [
        {"family": item["label"].removeprefix("initial-"), "sessionId": item["sessionId"],
         "requestedModel": item["model"],
         "identityEvidence": "docs/n1-reviews/batch-062-initial-review-checkpoint.json"}
        for item in initial["reviewProcesses"]
    ]
    assert len(sessions) == 2
    record = {
        "schemaVersion": 1, "execution": 385, "batch": "062", "status": preparation["status"],
        "startingHead": HEAD,
        "reviewedTeachingSnapshot": "38ab6072d2041325142c54cf54be5d126928eb31",
        "scope": load(CONTROL / "progress.json")["execution385StartingState"]["scope"],
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
            "completeArticleSelectors": 46, "articleCaptureSteps": 28,
            "method": preparation["projectionQualification"],
            "originalHarness": preparation["reusedAcceptedHarness"],
            "originalHarnessSha256": preparation["reusedAcceptedHarnessSha256"],
            "reciprocalPairs": 2, "directedTransitions": 4,
        },
        "accepted384AndroidRetainedWithoutRerun": True,
        "originalReviewerSessionsForLaterDependentVisualConfirmation": sessions,
        "originalInitialReportHashesUnchanged": preparation["originalInitialReportHashesUnchanged"],
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 88, "remainingAdditions": 1140,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    verify(record)
    save(SOURCES / "execution-385.json", record)
    batch_path = SOURCES / "batch-062-progress.json"
    batch = load(batch_path)
    batch.update(status="native-compiled-pending-execution",
                 nativePreparation="batch-062-native-preparation.json",
                 nativePreparationCheckpoint="execution-385.json", nextAction=NEXT)
    save(batch_path, batch)
    print(json.dumps({"status": record["status"], "artifacts": len(record["artifacts"]),
                      "apkSha256": compilation["apkSha256"], "runtimeUnchanged": True,
                      "nativeExecuted": False}, indent=2))
else:
    assert sys.argv[1:] in (["checkpoint"], ["close"])
    record = load(SOURCES / "execution-385.json")
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
        assert progress["checkpoint"] == 384
        checkpoint = {
            "schemaVersion": 1, "execution": 385, "checkpoint": 385, "batch": "062",
            "status": record["status"], "record": "docs/n1-sources/execution-385.json",
            "savedCommit": saved_head, "signature": "G",
            "recordedAt": datetime.now(timezone.utc).isoformat(),
            "scope": record["scope"], "compilation": record["compilation"],
            "staticSelectors": 46, "articleCaptureSteps": 28, "reciprocalPairs": 2,
            "directedReciprocalTransitions": 4, "contentVersion": record["contentVersion"],
            "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
            "publicationAttempted": False, "nextAction": NEXT,
            "publishedAdditions": 88, "remainingAdditions": 1140,
        }
        progress.update(checkpoint=385, status="continue",
                        stage="batch-062-native-compiled-pending-execution",
                        blocker=None, nextAction=NEXT)
        progress["execution385StartingState"]["status"] = "completed-bounded-native-preparation-checkpoint"
        progress["execution385CoordinatorCheckpoint"] = checkpoint
        progress["batch062NativePreparationCheckpoint"] = checkpoint
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-385-checkpoint.json", checkpoint)
        body = (
            f"Batch **062 / 俸**: exact-full-archive native fixture prepared and compiled in "
            f"normally signed local checkpoint `{saved_head}` (execution385). **Not published; "
            "native execution remains next.**\n\n"
            "The complete `e157d58c` Git envelope preserves all **8,314 runtime hashes / "
            "8,336 ZIP entries** and existing byte budgets. Content version remains "
            "`545c56b5d4b4e8ef`: **1,074 kanji / 5,032 words / 94 N1 cards**. Both current "
            "test classes and the exact archive were verified inside the APK. Prepared "
            "coverage includes **ホウ / no kun**, full ordered metadata, both "
            "**俸/俸給 and 給/俸給** pairs in four directions, System Back, offline routes, "
            "meaning, persisted on-reading feedback and ten-stroke drawing. "
            "**46 static selectors / 28 article capture steps**, 44 glyph probes including "
            "actual **人/亻**, four word probes for **俸給** and four production font rows "
            "are prepared—not native or fallback-readability acceptance.\n\n"
            "Temporary Android source/assets were removed; worktrees are clean. Execution384's "
            "fresh Android 3+1 results were retained without rerun. Original383 permission "
            "denial, qualified host-only heap evidence and original Claude062-P1/P2 "
            "noncompliance remain explicit; supervised dependent lexical remediation does "
            "not retroactively establish strict initial compliance. Next: fresh device/"
            "5580–5581 ownership check, both terminal native case0 results and direct PNG "
            "inspection, then original-session serial visual confirmation and combined-main "
            "publication gates. **88/1,228 additions published; 1,140 remain.** No new runtime "
            "delivery, physical-phone/general-release or whole-set acceptance claimed. "
            "Compatible Android `f9b59a2+` required."
        )
        (CONTROL / "execution-385-issue-body.txt").write_text(body + "\n", encoding="utf-8")
        print(json.dumps({"checkpoint": 385, "savedCommit": saved_head, "status": "continue",
                          "historicalRecordsCompared": compared, "nextGate": "same062-native-execution"}, indent=2))
    else:
        assert progress["checkpoint"] == 385 and progress["status"] == "continue"
        assert progress["execution385CoordinatorCheckpoint"]["savedCommit"] == saved_head
        receipt = load(CONTROL / "execution-385-issue-receipt.json")
        assert receipt["author"] == "stop-cran" and receipt["identityVerified"]
        assert receipt["bodySha256"] == sha(CONTROL / "execution-385-issue-body.txt")
        assert receipt["runtimePublished"] is False
        verification = {
            "schemaVersion": 1, "execution": 385, "checkpoint": 385, "batch": "062",
            "status": "continue", "savedCommit": saved_head, "signature": "G",
            "changedPaths": git("diff-tree", "--no-commit-id", "--name-only", "-r", saved_head).splitlines(),
            "worktreesClean": True, "runtimeUnchanged": True,
            "committedArtifactHashesVerified": len(record["artifacts"]),
            "fullHistoricalProgressPreserved": True, "historicalRecordsCompared": compared,
            "compiledNativeFixture": True, "exactFullArchivePackaged": True,
            "staticArticleSelectors": 46, "articleCaptureSteps": 28,
            "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
            "issueUpdate": receipt["url"], "ownerAuthorAndBodyVerified": True,
            "globalIdentityUnchanged": receipt["globalIdentityUnchanged"],
            "runtimePublished": False, "wholeProjectComplete": False,
            "recordedAt": datetime.now(timezone.utc).isoformat(),
        }
        progress["execution385CoordinatorCheckpoint"].update(
            issueUpdate=receipt["url"],
            issueReceipt="control/execution-385-issue-receipt.json", verification=verification,
        )
        progress["batch062NativePreparationCheckpoint"] = progress["execution385CoordinatorCheckpoint"]
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-385-verification.json", verification)
        print(json.dumps(verification, ensure_ascii=True, indent=2))
