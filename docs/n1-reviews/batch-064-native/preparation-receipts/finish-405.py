import hashlib
import json
import os
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
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-064-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "bf6204e5b4e4c64f340dcd8db65b2924b869cc45"
REVIEWED = "ff6eb7893344b806bf517ebd41bf19089bed5021"
SESSION = "90f1816e-9dd2-4f59-ba6b-106bfdc45098"
NEXT = (
    "SAME064 signed compiled native-preparation checkpoint405. NEXT bounded gate: execute "
    "control/artifacts/n1-batch-064-native-test.apk using N1Batch064GlyphTest and "
    "N1Batch064ArticleTest against exact full signedbf6204e5 Git envelope; read "
    "docs/n1-sources/execution-405.json and batch-064-native-preparation.json. "
    "Fresh adb/device and all local/remote5580-5581 connection/PID ownership immediately before "
    "known read-only N3_Acceptance_20261029 API35 hostGPU Vulkan-disabled helper at explicit "
    "emulator-5580; full SDK emulator flags -port5580 -read-only -no-snapshot -no-window "
    "-no-audio -gpu host -feature -Vulkan -memory2048 -cores2. Record actual owned parent/QEMU; "
    "stop ONLY owned helper. 040 alternate-port exception NOT inherited. No production/content/"
    "font/guest-app-heap/archive-guard changes. Full archive through productionContentSyncONCE "
    "with1076kanji5034words96N1/ae05977ba66f42f5/problems0/epoch1; Lite+Full full ordered "
    "テイ/emptykun and both explicit curated subsets; sole normalizedてい/noKunLog. "
    "BOTH terminalcase0/no skips/rawlogs/direct PNG inspection of偵貞停低値人亻探手扌/"
    "探偵/刑事 in four production font rows; actual亻/扌 fallback pending. "
    "BOTH mapped reciprocal pairs偵-探偵/探-探偵 in FOUR directions and "
    "刑事-探偵 comparison in BOTH directions/SystemBack/offline/meaning/sole curatedOn "
    "Good persistent grade/eleven touch-reference strokes/ungraded trace/recall miss/"
    "persistedDrawAgain. 40 singlePaint+8 fullword probes planned;79 complete-article "
    "static selectors/46 article capture steps audited, NOT native acceptance. "
    "Rasterhashes not readability/fallback-face identification; offline reference/recallmiss "
    "not MLKit or correct human recall. Accepted404 freshAndroid3+1 retained without rerun "
    "absent new concern. After nativePASS use ORIGINAL Claude28a561c9-9201-40a9-a3a1-c9e37c6d168a "
    "and GPT1d30e91b-c5ed-4bd0-8d74-2177b9fbb0d7 sessions SERIALly for bounded dependent visuals, "
    "not new blind initials. Preserve original reports,402textual closure and process/lookup/"
    "citation/read-depth qualifications onff6eb789. Then latestmain normal nonrewriting "
    "integration/allcombined source-baseline-reading-link-font-stroke/Python/vocab/validator/"
    "freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/"
    "normal signing/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/"
    "terminalreceipts/ownerissue60 BEFOREdelivery or065. Original403permissiondenial and049"
    "HOST512MiBOOM remain historical; qualifiedhost-only1GiBinit unchanged. Actualpermission"
    "denial/signingwait: preserveexactcommand/error, report/yield; no retry/workaround. "
    "No063rerun/065/secondrunner/concurrentheavywork/supervisorchanges. PreserveFULLlivehistory. "
    "Published90/1228,1138remain; localdraft91 NOTdelivered. CompatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd, encoding="utf-8").strip()


def verify(record):
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"], path
    for name in ("fixture", "archive"):
        assert sha(Path(record[name])) == record[f"{name}Sha256"]
    assert sha(Path(record["compilation"]["apk"])) == record["compilation"]["apkSha256"]
    assert not git("status", "--porcelain", cwd=ANDROID)
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for name, expected in record["originalInitialReportHashesUnchanged"].items():
        assert sha(ROOT / name) == expected


mode = sys.argv[1] if sys.argv[1:] else "archive"
if mode == "archive":
    assert git("rev-parse", "HEAD") == HEAD
    assert git("diff", "--name-only") == "docs/n1-authoring-notes.md"
    preparation = load(CONTROL / "batch-064-native-fixture-verification.json")
    apk = CONTROL / "artifacts" / "n1-batch-064-native-test.apk"
    with zipfile.ZipFile(apk) as package:
        asset = package.read("assets/n1-batch-064-bf6204e5-envelope.zip")
        assert hashlib.sha256(asset).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist()
               if name.startswith("classes") and name.endswith(".dex")]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch064{kind}Test;".encode() in blob for blob in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch063{kind}Test;".encode() not in blob for blob in dex)
        for method in (
            "investigationLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
            "fullSingleImportOfflineInvestigationTwoPairsComparisonOnOnlyDrawingAndSystemBack",
        ):
            assert any(method.encode() in blob for blob in dex), method
    raw_log = CONTROL / "logs" / "execution-405-native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (CONTROL / "logs" / "execution-405-native-compile-exit.txt").read_text().strip() == "0"
    result = re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0)
    tasks = re.search(r"\d+ actionable tasks: .+", compile_text).group(0)
    archived_log = FOLDER / "compile.txt"
    assert not archived_log.exists()
    archived_log.write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n", encoding="utf-8")
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    for name in ("start-405.py", "prepare-405-native.py", "run-405-native-compile.ps1", "finish-405.py"):
        shutil.copyfile(CONTROL / name, receipts / name)
    for relative in (
        r"app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch064NativeTest.kt",
        r"app\src\androidTest\assets\n1-batch-064-bf6204e5-envelope.zip",
    ):
        assert not (ANDROID / relative).exists()
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version ae05977ba66f42f5")):
        path = CONTROL / "logs" / f"execution-405-{name}.txt"
        assert expected in path.read_text(encoding="utf-8-sig")
        checks.append({"check": name, "exitCode": 0, "log": str(path), "sha256": sha(path)})
    assert len(preparation["staticMarkdownSelectors"]) == 79
    assert preparation["captureSteps"] == 46 and len(preparation["articleRouteTransitions"]) == 6
    source = Path(preparation["fixture"]).read_text(encoding="utf-8")
    glyphs = re.findall(r'"([^"]+)"', re.search(r'for \(char in listOf\((.*?)\)\)', source).group(1))
    assert glyphs == preparation["plannedGlyphs"] and len(set(glyphs)) == 10
    assert source.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in source
    assert source.count("assertEquals(emptyList<String>(),") == 5
    assert "repeat(1)" in source and "repeat(2)" not in source
    assert "assertEquals(11, strokes.length())" in source and '"11 strokes drawn"' in source
    assert 'it.kanji == "偵" && it.mode == ReadingKind.Kun.mode.name' in source
    compilation = {
        "status": "compiled-not-executed", "exitCode": 0, "result": result, "tasks": tasks,
        "log": str(archived_log.relative_to(ROOT)), "logSha256": sha(archived_log),
        "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
        "normalization": "Archive UTF-8 LF/trailing-whitespace normalization only; complete raw log retained.",
        "launcher": str(receipts.relative_to(ROOT) / "run-405-native-compile.ps1"),
        "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
        "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
        "packagedExactFullArchiveVerified": True, "bothBatch064ClassDescriptorsAndMethodsPresent": True,
        "oldBatch063ClassDescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
        "androidWhollyClean": True,
        "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
        "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
        "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
    }
    preparation.update(status="native-compiled-pending-execution", compilation=compilation,
                       checks=checks, nextAction=NEXT)
    preparation_path = SOURCES / "batch-064-native-preparation.json"
    assert not preparation_path.exists()
    save(preparation_path, preparation)
    initial = load(ROOT / "docs" / "n1-reviews" / "batch-064-initial-review-checkpoint.json")
    sessions = [
        {"family": item["label"].removeprefix("initial-"), "sessionId": item["sessionId"],
         "requestedModel": item["model"], "identityEvidence": "docs/n1-reviews/batch-064-initial-review-checkpoint.json"}
        for item in initial["reviewProcesses"]
    ]
    assert len(sessions) == 2
    artifact_paths = sorted(path for path in FOLDER.rglob("*") if path.is_file()) + [preparation_path]
    record = {
        "schemaVersion": 1, "execution": 405, "batch": "064", "status": preparation["status"],
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "scope": load(CONTROL / "progress.json")["execution405StartingState"]["scope"],
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "requestSha256": sha(CONTROL / "logs" / SESSION / "request.txt"),
        "preparation": str(preparation_path.relative_to(ROOT)), "preparationSha256": sha(preparation_path),
        "contentVersion": preparation["contentVersion"], "compilation": compilation, "checks": checks,
        **{key: preparation[key] for key in ("fixture", "fixtureSha256", "archive", "archiveSha256")},
        "artifacts": [{"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                       "sha256": sha(path)} for path in artifact_paths],
        "selectorAudit": {
            "completeArticleSelectors": 79, "articleCaptureSteps": 46,
            "method": preparation["projectionQualification"],
            "reciprocalPairs": 2, "directedReciprocalTransitions": 4,
            "comparisonPairs": 1, "directedComparisonTransitions": 2,
        },
        "accepted404AndroidRetainedWithoutRerun": True,
        "originalReviewerSessionsForLaterDependentVisualConfirmation": sessions,
        "originalInitialReportHashesUnchanged": preparation["originalInitialReportHashesUnchanged"],
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 90, "remainingAdditions": 1138,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    verify(record)
    save(SOURCES / "execution-405.json", record)
    batch_path = SOURCES / "batch-064-progress.json"
    batch = load(batch_path)
    batch.update(status="native-compiled-pending-execution",
                 nativePreparation="batch-064-native-preparation.json",
                 nativePreparationCheckpoint="execution-405.json", nextAction=NEXT)
    save(batch_path, batch)
    print(json.dumps({"status": record["status"], "artifacts": len(record["artifacts"]),
                      "apkSha256": compilation["apkSha256"], "runtimeUnchanged": True,
                      "nativeExecuted": False}, indent=2))
elif mode in ("checkpoint", "close"):
    record = load(SOURCES / "execution-405.json")
    verify(record)
    saved_head = git("rev-parse", "HEAD")
    assert saved_head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    for item in record["artifacts"]:
        committed = subprocess.check_output(["git", "show", f"{saved_head}:{Path(item['path']).as_posix()}"], cwd=ROOT)
        assert hashlib.sha256(committed).hexdigest() == item["sha256"]
    progress = load(CONTROL / "progress.json")
    original = load(CONTROL / "logs" / SESSION / "checkpoint-full.json")
    compared = 0
    for key, value in original.items():
        if key not in {"checkpoint", "status", "stage", "blocker", "nextAction"}:
            assert progress[key] == value, key
            compared += 1
    if mode == "checkpoint":
        assert progress["checkpoint"] == 404
        checkpoint = {
            "execution": 405, "checkpoint": 405, "batch": "064", "status": record["status"],
            "record": "docs/n1-sources/execution-405.json", "savedCommit": saved_head, "signature": "G",
            "recordedAt": datetime.now(timezone.utc).isoformat(), "scope": record["scope"],
            "compilation": record["compilation"], "staticSelectors": 79, "articleCaptureSteps": 46,
            "reciprocalPairs": 2, "directedReciprocalTransitions": 4,
            "comparisonPairs": 1, "directedComparisonTransitions": 2,
            "contentVersion": record["contentVersion"], "nativeExecuted": False,
            "nativeAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
            "nextAction": NEXT, "publishedAdditions": 90, "remainingAdditions": 1138,
        }
        progress.update(checkpoint=405, status="continue", stage="batch-064-native-compiled-pending-execution",
                        blocker=None, nextAction=NEXT)
        progress["execution405StartingState"]["status"] = "completed-bounded-native-preparation-checkpoint"
        progress["execution405CoordinatorCheckpoint"] = checkpoint
        progress["batch064NativePreparationCheckpoint"] = checkpoint
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-405-checkpoint.json", checkpoint)
        body = (
            f"Batch **064 / 偵**: full-archive native fixture prepared and compiled in normally "
            f"signed local checkpoint `{saved_head}` (execution405). **Not published; native "
            "execution remains next.**\n\n"
            "The complete `bf6204e5` Git envelope preserves all **8,320 runtime hashes / "
            "8,342 ZIP entries** and existing byte budgets. Content version remains "
            "`ae05977ba66f42f5`: **1,076 kanji / 5,034 words / 96 N1 cards**. Both current "
            "test classes and the exact archive were verified inside the APK. Prepared "
            "coverage includes **テイ / empty kun**, Lite/Full metadata and the sole "
            "normalized **てい** key, both **偵/探偵 and 探/探偵** pairs in four directions, "
            "the **刑事/探偵** comparison in both directions, System Back, offline routes, "
            "meaning, persisted on-reading grade and eleven-stroke drawing. "
            "**79 static selectors / 46 article capture steps**, 40 glyph probes including "
            "actual **人/亻 and 手/扌**, eight word probes for **探偵/刑事** and four "
            "production font rows are prepared—not native or fallback-readability acceptance.\n\n"
            "Temporary Android source/assets were removed; worktrees are clean. Execution404's "
            "fresh Android 3+1 acceptance retained without rerun. Original403 permission denial, "
            "parent exact-command recovery, qualified host-only heap evidence and all original "
            "review/source/read-depth qualifications remain distinct. Next: fresh device/"
            "5580–5581 ownership check, both terminal native case0 results and direct PNG "
            "inspection, then original-session serial visual confirmation and combined-main "
            "publication gates. **90/1,228 additions published; 1,138 remain.** No new runtime "
            "delivery, physical-phone/general-release or whole-set acceptance claimed. "
            "Compatible Android `f9b59a2+` required."
        )
        (CONTROL / "execution-405-issue-body.txt").write_text(body + "\n", encoding="utf-8")
        print(json.dumps({"checkpoint": 405, "savedCommit": saved_head, "status": "continue",
                          "historicalRecordsCompared": compared, "nextGate": "same064-native-execution"}, indent=2))
    else:
        assert progress["checkpoint"] == 405 and progress["status"] == "continue"
        assert progress["execution405CoordinatorCheckpoint"]["savedCommit"] == saved_head
        receipt = load(CONTROL / "execution-405-issue-receipt.json")
        assert receipt["author"] == "stop-cran" and receipt["bodyVerified"]
        assert receipt["bodySha256"] == sha(CONTROL / "execution-405-issue-body.txt")
        assert receipt["runtimePublished"] is False
        verification = {
            "execution": 405, "checkpoint": 405, "batch": "064", "status": "continue",
            "savedCommit": saved_head, "signature": "G",
            "changedPaths": git("diff-tree", "--no-commit-id", "--name-only", "-r", saved_head).splitlines(),
            "worktreesClean": True, "runtimeUnchanged": True,
            "committedArtifactHashesVerified": len(record["artifacts"]),
            "fullHistoricalProgressPreserved": True, "historicalRecordsCompared": compared,
            "compiledNativeFixture": True, "exactFullArchivePackaged": True,
            "staticArticleSelectors": 79, "articleCaptureSteps": 46,
            "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
            "issueUpdate": receipt["url"], "ownerAuthorAndBodyVerified": True,
            "globalIdentityUnchanged": receipt["globalIdentityUnchanged"],
            "runtimePublished": False, "wholeProjectComplete": False,
            "recordedAt": datetime.now(timezone.utc).isoformat(),
        }
        progress["execution405CoordinatorCheckpoint"].update(issueUpdate=receipt["url"], verification=verification)
        progress["batch064NativePreparationCheckpoint"] = progress["execution405CoordinatorCheckpoint"]
        progress["batch064NativePreparationIssueReceipt"] = receipt
        save(CONTROL / "progress.json", progress)
        save(CONTROL / "execution-405-verification.json", verification)
        print(json.dumps(verification, ensure_ascii=True, indent=2))
elif mode == "post":
    body_path = CONTROL / "execution-405-issue-body.txt"
    body = body_path.read_text(encoding="utf-8").rstrip("\n")
    receipt_path = CONTROL / "execution-405-issue-receipt.json"
    assert not receipt_path.exists()
    global_before = subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip()
    assert global_before == "romanko-ms"
    child_env = os.environ.copy()
    token = subprocess.check_output(["gh", "auth", "token", "--user", "stop-cran"], text=True).strip()
    child_env["GH_TOKEN"] = token
    try:
        identity = subprocess.check_output(["gh", "api", "user", "--jq", ".login"], env=child_env, text=True).strip()
        assert identity == "stop-cran"
        response = subprocess.run(
            ["gh", "api", "--method", "POST", "repos/stop-cran/learning-japanese/issues/60/comments", "--input", "-"],
            input=json.dumps({"body": body}), env=child_env, text=True, encoding="utf-8",
            capture_output=True, check=True)
        posted = json.loads(response.stdout)
        checked = json.loads(subprocess.check_output(
            ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{posted['id']}"],
            env=child_env, encoding="utf-8"))
        assert checked["body"] == body and checked["user"]["login"] == "stop-cran"
    finally:
        child_env.pop("GH_TOKEN", None)
        token = None
    global_after = subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip()
    assert global_after == global_before
    receipt = {
        "url": checked["html_url"], "commentId": checked["id"], "author": checked["user"]["login"],
        "bodyVerified": True, "bodySha256": sha(body_path), "localCommit": git("rev-parse", "HEAD"),
        "globalIdentityUnchanged": True, "runtimePublished": False,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
    }
    save(receipt_path, receipt)
    print(json.dumps(receipt, indent=2))
else:
    raise ValueError(f"Unknown mode: {mode}")
