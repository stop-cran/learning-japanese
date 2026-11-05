import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-059-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "911431dad205cf031e1df9f561a47748c060439b"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
SESSION = "d1def87c-01fa-4af8-b997-5b4c5a67c656"
NEXT = (
    "SAME059 signed compiled native-preparation checkpoint356. NEXT bounded gate: execute "
    "control/artifacts/n1-batch-059-native-test.apk with N1Batch059GlyphTest and "
    "N1Batch059ArticleTest against exact full signed911431da Git envelope; read "
    "docs/n1-sources/execution-356.json and batch-059-native-preparation.json. "
    "Fresh adb/device and all local/remote5580-5581 connection/PID ownership immediately before "
    "known read-only N3_Acceptance_20261029 API35 hostGPU Vulkan-disabled helper at explicit "
    "emulator-5580; full SDK emulator flags -port5580 -read-only -no-snapshot -no-window "
    "-no-audio -gpu host -feature -Vulkan -memory2048 -cores2. Record actual owned parent/QEMU; "
    "stop ONLY owned helper. 040 alternate-port exception NOT inherited. No production/content/"
    "font/guest-app-heap/archive-guard changes. Full archive through productionContentSyncONCE "
    "with1071kanji5030words91N1/1f1ad78479e9c1f4/problems0/epoch1; Lite+Full full ordered "
    "キョウコウ/う.ける and curatedキョウ/[]; normalizedきょう/no-kun. BOTH terminalcase0/"
    "no skips/rawlogs/direct PNG inspection of享京厚高亠厂子口受/享受 in four production font "
    "rows; actual亠厂 fallback pending. New享受 article plus changed受 reciprocal entry; "
    "BOTH pairs享-享受/受-享受 in FOUR directions/SystemBack/offline/meaning/sole curatedOn "
    "Good persistent grade/no-kun log/eight touch-reference strokes/ungraded trace/recall miss/"
    "persistedDrawAgain. 36 singlePaint+4 fullword probes planned;44 complete-article static "
    "selectors/26 article capture steps audited, NOT native acceptance. Rasterhashes not "
    "readability/fallback-face identification; offline reference/recallmiss not MLKit or "
    "correct human recall. Accepted355 freshAndroid3+1 retained without rerun absent new concern. "
    "After nativePASS use ORIGINAL two different-family reviewer sessions SERIALly for bounded "
    "dependent visuals, not new blind initials: Claude57374784-d547-43db-a93d-6d3bc5f93f30/"
    "GPT345c7cb4-b120-41ce-b1ed-425003c6f4a5. Preserve original initial reports and353 textual "
    "closure on769293c8; historical Claude first-confirmation overlap remains noncompliance; "
    "one-call bounded remediation is NOT retroactive strict acceptance. Then latestmain "
    "normal nonrewriting integration/allcombined source-baseline-reading-link-font-stroke/Python/"
    "vocab/validator/freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained "
    "budgets/normal signing/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIP"
    "runtimehash/terminalreceipts/ownerissue60 BEFOREdelivery or060. Original354 permission "
    "denial and049HOST512MiBOOM remain historical; qualified host-only1GiB init unchanged. "
    "Actual permission denial/signing wait: preserve exact command/error, report/yield; no retry/"
    "workaround. No058rerun/060/secondrunner/concurrentheavywork/supervisor changes. Preserve FULL "
    "live history. Published85/1228,1143remain; compatibleAndroidf9b59a2+ required; "
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
    preparation = load(CONTROL / "batch-059-native-fixture-verification.json")
    assert sha(Path(preparation["fixture"])) == preparation["fixtureSha256"]
    assert sha(Path(preparation["archive"])) == preparation["archiveSha256"]
    apk = CONTROL / "artifacts" / "n1-batch-059-native-test.apk"
    with zipfile.ZipFile(apk) as package:
        asset = package.read("assets/n1-batch-059-911431da-envelope.zip")
        assert hashlib.sha256(asset).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist()
               if name.startswith("classes") and name.endswith(".dex")]
        for kind in ("Glyph", "Article"):
            current = f"Lio/github/stopcran/kanji/ui/N1Batch059{kind}Test;".encode()
            assert any(current in blob for blob in dex), current
            obsolete = f"Lio/github/stopcran/kanji/ui/N1Batch058{kind}Test;".encode()
            assert all(obsolete not in blob for blob in dex), obsolete
        for method in (
            "benefitsLookalikesAndTwoFallbackRadicalsAcrossFourProductionFamilies",
            "fullSingleImportOfflineBenefitsTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
        ):
            assert any(method.encode() in blob for blob in dex), method
    raw_log = CONTROL / "logs" / "execution-356-native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert "BUILD SUCCESSFUL in 1m 5s" in compile_text
    assert "56 actionable tasks: 9 executed, 47 up-to-date" in compile_text
    assert (CONTROL / "logs" / "execution-356-native-compile-exit.txt").read_text().strip() == "0"
    archived_log = FOLDER / "compile.txt"
    assert not archived_log.exists()
    archived_log.write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n",
                            encoding="utf-8")
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    for name in ("start-356.py", "prepare-356-native.py", "run-356-native-compile.ps1", "finish-356.py"):
        shutil.copyfile(CONTROL / name, receipts / name)
    for relative in (
        r"app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch059NativeTest.kt",
        r"app\src\androidTest\assets\n1-batch-059-911431da-envelope.zip",
    ):
        assert not (ANDROID / relative).exists()
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 1f1ad78479e9c1f4")):
        path = CONTROL / "logs" / f"execution-356-{name}.txt"
        assert expected in path.read_text(encoding="utf-8-sig")
        checks.append({"check": name, "exitCode": 0, "log": str(path), "sha256": sha(path)})
    assert len(preparation["staticMarkdownSelectors"]) == 44
    assert preparation["captureSteps"] == 26
    assert len(preparation["articleRouteTransitions"]) == 4
    compilation = {
        "status": "compiled-not-executed", "exitCode": 0,
        "result": "BUILD SUCCESSFUL in1m5s;56 tasks:9 executed,47 up-to-date",
        "log": str(archived_log.relative_to(ROOT)), "logSha256": sha(archived_log),
        "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
        "normalization": "Archive UTF-8 LF/trailing-whitespace normalization only; complete raw log retained.",
        "launcher": str(receipts.relative_to(ROOT) / "run-356-native-compile.ps1"),
        "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
        "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
        "packagedExactFullArchiveVerified": True, "bothBatch059ClassDescriptorsAndMethodsPresent": True,
        "oldBatch058ClassDescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
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
    preparation_path = SOURCES / "batch-059-native-preparation.json"
    assert not preparation_path.exists()
    save(preparation_path, preparation)
    artifact_paths = sorted(path for path in FOLDER.rglob("*") if path.is_file()) + [preparation_path]
    record = {
        "schemaVersion": 1, "execution": 356, "batch": "059", "status": preparation["status"],
        "startingHead": HEAD,
        "scope": load(CONTROL / "progress.json")["execution356StartingState"]["scope"],
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
            "completeArticleSelectors": 44, "articleCaptureSteps": 26,
            "method": preparation["projectionQualification"],
            "originalHarness": preparation["reusedAcceptedHarness"],
            "originalHarnessSha256": preparation["reusedAcceptedHarnessSha256"],
            "reciprocalPairs": 2, "directedTransitions": 4,
        },
        "accepted355AndroidRetainedWithoutRerun": True,
        "originalInitialReportHashesUnchanged": preparation["originalInitialReportHashesUnchanged"],
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 85, "remainingAdditions": 1143,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    verify(record)
    save(SOURCES / "execution-356.json", record)
    batch_path = SOURCES / "batch-059-progress.json"
    batch = load(batch_path)
    batch.update(status="native-compiled-pending-execution",
                 nativePreparation="batch-059-native-preparation.json",
                 nativePreparationCheckpoint="execution-356.json", nextAction=NEXT)
    save(batch_path, batch)
    print(json.dumps({"status": record["status"], "artifacts": len(record["artifacts"]),
                      "apkSha256": compilation["apkSha256"], "runtimeUnchanged": True,
                      "nativeExecuted": False}, indent=2))
else:
    assert sys.argv[1:] in (["checkpoint"], ["close"])
    record = load(SOURCES / "execution-356.json")
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
        assert progress["checkpoint"] == 355
        checkpoint = {
            "schemaVersion": 1, "execution": 356, "batch": "059", "status": record["status"],
            "record": "docs/n1-sources/execution-356.json", "savedCommit": saved_head,
            "signature": "G", "recordedAt": datetime.now(timezone.utc).isoformat(),
            "scope": record["scope"], "compilation": record["compilation"],
            "staticSelectors": 44, "articleCaptureSteps": 26, "reciprocalPairs": 2,
            "directedReciprocalTransitions": 4, "contentVersion": record["contentVersion"],
            "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
            "publicationAttempted": False, "nextAction": NEXT,
            "publishedAdditions": 85, "remainingAdditions": 1143,
        }
        progress.update(checkpoint=356, status="continue",
                        stage="batch-059-native-compiled-pending-execution",
                        blocker=None, nextAction=NEXT)
        progress["execution356StartingState"]["status"] = "completed-bounded-native-preparation-checkpoint"
        progress["execution356CoordinatorCheckpoint"] = checkpoint
        progress["batch059NativePreparationCheckpoint"] = checkpoint
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-356-checkpoint.json", checkpoint)
        body = (
            f"Batch **059 / 享**: exact-full-archive native fixture prepared and compiled in "
            f"normally signed local checkpoint `{saved_head}` (execution356). **Not published; "
            "native execution remains next.**\n\n"
            "The complete `911431da` Git envelope preserves all **8,306 runtime hashes / "
            "8,328 ZIP entries** and existing byte budgets. Content version remains "
            "`1f1ad78479e9c1f4`: **1,071 kanji / 5,030 words / 91 N1 cards**. Both current "
            "test classes and the exact archive were verified inside the APK. Prepared "
            "coverage includes **キョウ / no kun**, full ordered metadata, both **享/享受 "
            "and 受/享受** pairs in four directions, System Back, offline routes, meaning, "
            "persisted on-reading feedback and eight-stroke drawing. **44 static selectors / "
            "26 article capture steps**, 36 glyph probes including actual **亠/厂**, and "
            "four word probes are prepared—not native or fallback-readability acceptance.\n\n"
            "Compilation passed (1m5s; one worker, serial). Temporary Android source/assets "
            "were removed; worktrees are clean. Execution355's fresh Android 3+1 results were "
            "retained without rerun. Original354 permission denial, qualified host-only heap "
            "evidence and historical reviewer noncompliance remain explicit; bounded "
            "remediation does not retroactively establish strict compliance. Next: fresh "
            "device/5580–5581 ownership check, both terminal native case0 results and direct "
            "PNG inspection, then original-session serial visual confirmation and combined-main "
            "publication gates. **85/1,228 additions published; 1,143 remain.** No new runtime "
            "delivery, physical-phone/general-release or whole-set acceptance claimed. "
            "Compatible Android `f9b59a2+` required."
        )
        (CONTROL / "execution-356-issue-body.txt").write_text(body + "\n", encoding="utf-8")
        print(json.dumps({"checkpoint": 356, "savedCommit": saved_head, "status": "continue",
                          "historicalRecordsCompared": compared, "nextGate": "same059-native-execution"}, indent=2))
    else:
        assert progress["checkpoint"] == 356 and progress["status"] == "continue"
        assert progress["execution356CoordinatorCheckpoint"]["savedCommit"] == saved_head
        receipt = load(CONTROL / "execution-356-issue-receipt.json")
        assert receipt["author"] == "stop-cran" and receipt["identityVerified"]
        assert receipt["bodySha256"] == sha(CONTROL / "execution-356-issue-body.txt")
        assert receipt["runtimePublished"] is False
        verification = {
            "schemaVersion": 1, "execution": 356, "checkpoint": 356, "batch": "059",
            "status": "continue", "savedCommit": saved_head, "signature": "G",
            "changedPaths": git("diff-tree", "--no-commit-id", "--name-only", "-r", saved_head).splitlines(),
            "worktreesClean": True, "runtimeUnchanged": True,
            "committedArtifactHashesVerified": len(record["artifacts"]),
            "fullHistoricalProgressPreserved": True, "historicalRecordsCompared": compared,
            "compiledNativeFixture": True, "exactFullArchivePackaged": True,
            "staticArticleSelectors": 44, "articleCaptureSteps": 26,
            "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
            "issueUpdate": receipt["url"], "ownerAuthorAndBodyVerified": True,
            "globalIdentityUnchanged": receipt["globalIdentityUnchanged"],
            "runtimePublished": False, "wholeProjectComplete": False,
            "recordedAt": datetime.now(timezone.utc).isoformat(),
        }
        progress["execution356CoordinatorCheckpoint"].update(
            issueUpdate=receipt["url"],
            issueReceipt="control/execution-356-issue-receipt.json", verification=verification,
        )
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-356-verification.json", verification)
        print(json.dumps(verification, ensure_ascii=False, indent=2))
