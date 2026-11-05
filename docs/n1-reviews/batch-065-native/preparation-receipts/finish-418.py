import gzip
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
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-065-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "ee672744235275d321b4bfb33a6efe0286444594"
NEXT = (
    "SAME065 signed compiled native-preparation checkpoint418. Next bounded checkpoint: "
    "execute control/artifacts/n1-batch-065-native-test.apk using N1Batch065GlyphTest and "
    "N1Batch065ArticleTest against exact full signedee672744 Git envelope. Read "
    "docs/n1-sources/execution-418.json and batch-065-native-preparation.json. Fresh actual "
    "adb inventory and local/remote5580-5581 connection/PID ownership immediately before "
    "known read-only N3_Acceptance_20261029 API35 hostGPU Vulkan-disabled emulator-5580 "
    "(-port5580 -read-only -no-snapshot -no-window -no-audio -gpu host -feature -Vulkan "
    "-memory2048 -cores2). Record owned parent/QEMU and stop ONLY owned helper;040 alternate "
    "port exception not inherited. Use unchanged guest/app heaps, production font code and "
    "archive guards. Full archive through productionContentSyncONCE:1077kanji5036words97N1/"
    "6a940651167e0e94/problems0/epoch1; ordered fullケン/[つま.しい,つづまやか] "
    "and curatedケン/つま.しい in Lite+Full; normalizedけん/つましい, no source-only "
    "つづまやか log. Require BOTH actual terminalcase0/no skips/rawlogs/direct PNG inspection "
    "of倹儉険験値人亻阝馬約糸勺/倹約/倹しい in four production rows.48 singlePaint "
    "and8word-raster probes planned;86 static article selectors/49captures are not "
    "native semantics/readability acceptance. All3mapped pairs倹-倹約/約-倹約/倹-倹しい "
    "in6directions and倹約-倹しい comparison in2directions; complete4articles/SystemBack/"
    "offline/N1selection/meaning/bothcuratedGoodgrades/10reference-stroke touch/ungraded "
    "trace/recallmiss/persistedDrawAgain. Raster hashes do not establish readable glyphs "
    "or fallback-face identity; trace/recall miss not MLKit or human recall. Accepted417 "
    "qualifiedfreshAndroid3+1 retained without redundant rerun. Future same-full-repo HOST "
    "gates use qualifiedbatch-065-host-integration-heap.init.gradle2GiB; NEVER for native "
    "builds; preserve original416permissiondenial/actual1GiBOOM/prior049512MiBfailure "
    "and exact failed/successlogs/XML/init. After nativePASS use ORIGINAL Claude "
    "9555ba9e-42a2-497b-b221-dff6587e98e0 and GPT491afc55-0d7d-42d1-aef9-3d2f6681b28b "
    "sessions SERIALly for bounded dependent visual confirmation with scoped--add-dir "
    "control and process/preflight checks; retain honest image/read-depth/source/citation "
    "limits and45c275e7teaching/ae36905btextualclosure. Then freshlatestmain nonrewriting "
    "integration/allcombined source-baseline-reading-link-font-stroke/Python/vocab/validator/"
    "freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/"
    "normal signing/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIP"
    "runtimehash/terminalreceipts/ownerissue60 BEFOREdelivery or066. Actualpermissiondenial "
    "or signingwait: preserve exact command/error, report/yield; no retry/workaround. No "
    "secondrunner/concurrentheavywork/supervisorchanges. PreserveFULLlivehistory. Published "
    "91/1228,1137remain/latest0640fe60920; localdraft92 NOTdelivered. CompatibleAndroidf9b59a2+ "
    "required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
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
    assert not git("diff", record["reviewedTeachingSnapshot"], "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for name, expected in record["originalReportHashesUnchanged"].items():
        assert sha(ROOT / name) == expected


mode = sys.argv[1] if sys.argv[1:] else "archive"
if mode == "archive":
    assert git("rev-parse", "HEAD") == HEAD
    assert git("diff", "--name-only") == "docs/n1-authoring-notes.md"
    preparation = load(CONTROL / "batch-065-native-fixture-verification.json")
    apk = CONTROL / "artifacts" / "n1-batch-065-native-test.apk"
    with zipfile.ZipFile(apk) as package:
        assert hashlib.sha256(package.read("assets/n1-batch-065-ee672744-envelope.zip")).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist() if re.fullmatch(r"classes\d*\.dex", name)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch065{kind}Test;".encode() in blob for blob in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch064{kind}Test;".encode() not in blob for blob in dex)
        for method in (
            "frugalityLookalikesOlderFormAndRadicalsAcrossFourProductionFamilies",
            "fullSingleImportOfflineFrugalityThreePairsBothCuratedReadingsDrawingAndSystemBack",
        ):
            assert any(method.encode() in blob for blob in dex)
    raw_log = CONTROL / "logs" / "execution-418-native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (CONTROL / "logs" / "execution-418-native-compile-exit.txt").read_text().strip() == "0"
    assert not (FOLDER / "compile.txt").exists()
    (FOLDER / "compile.txt").write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    assert gzip.decompress((FOLDER / "compile-raw.txt.gz").read_bytes()) == raw_log.read_bytes()
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    for name in ("start-418.py", "prepare-418-native.py", "run-418-native-compile.ps1", "finish-418.py"):
        shutil.copyfile(CONTROL / name, receipts / name)
    save(SOURCES / "batch-065-native-preparation.json", preparation)
    for name in ("N1Batch065NativeTest.kt",):
        assert not (ANDROID / "app" / "src" / "androidTest" / "java" / "io" / "github" / "stopcran" / "kanji" / "ui" / name).exists()
    assert not (ANDROID / "app" / "src" / "androidTest" / "assets" / "n1-batch-065-ee672744-envelope.zip").exists()
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 6a940651167e0e94")):
        path = CONTROL / "logs" / f"execution-418-{name}.txt"
        assert expected in path.read_text(encoding="utf-8-sig")
        checks.append({"check": name, "exitCode": 0, "log": str(path), "sha256": sha(path)})
    assert len(preparation["staticMarkdownSelectors"]) == 86
    assert preparation["captureSteps"] == 49 and len(preparation["articleRouteTransitions"]) == 8
    source = Path(preparation["fixture"]).read_text(encoding="utf-8")
    assert source.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in source
    assert 'repeat(2)' in source and 'assertEquals(10, strokes.length())' in source
    inherited = load(SOURCES / "execution-417.json")
    for item in inherited["archivedArtifacts"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-065-reconciliation.json")
    reports = {}
    for process in reconciliation["processes"].values():
        path = ROOT / "docs" / "n1-reviews" / process["report"]
        assert sha(path) == process["reportSha256"]
        reports[path.relative_to(ROOT).as_posix()] = sha(path)
    record = {
        "schemaVersion": 1, "execution": 418, "batch": "065",
        "status": "native-compiled-pending-execution", "startingHead": HEAD,
        "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
        "scope": load(CONTROL / "execution-418-start.json")["scope"],
        "authorization": load(CONTROL / "execution-418-start.json")["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "preparation": "docs\\n1-sources\\batch-065-native-preparation.json",
        "preparationSha256": sha(SOURCES / "batch-065-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "status": "compiled-not-executed", "exitCode": 0,
            "result": re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0),
            "tasks": re.search(r"\d+ actionable tasks: .+", compile_text).group(0),
            "log": str((FOLDER / "compile.txt").relative_to(ROOT)), "logSha256": sha(FOLDER / "compile.txt"),
            "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "rawLogArchive": str((FOLDER / "compile-raw.txt.gz").relative_to(ROOT)),
            "normalization": "Readable log is UTF-8 LF with trailing line whitespace removed; deterministic gzip retains exact raw bytes.",
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
            "packagedExactFullArchiveVerified": True,
            "bothBatch065ClassDescriptorsAndMethodsPresent": True, "oldBatch064ClassDescriptorsAbsent": True,
            "temporaryAndroidSourceAndAssetRemoved": True, "androidWhollyClean": True,
            "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks,
        "fixture": preparation["fixture"], "fixtureSha256": preparation["fixtureSha256"],
        "archive": preparation["archive"], "archiveSha256": preparation["archiveSha256"],
        "selectorAudit": {"completeArticleSelectors": 86, "articleCaptureSteps": 49,
                          "reciprocalPairs": 3, "directedReciprocalTransitions": 6,
                          "comparisonPairs": 1, "directedComparisonTransitions": 2,
                          "method": preparation["projectionQualification"]},
        "accepted417AndroidRetainedWithoutRerun": True,
        "inherited417EvidenceHashesReverified": True,
        "originalReportHashesUnchanged": reports,
        "originalReviewerSessionsForLaterDependentVisualConfirmation": [
            {"family": family, "sessionId": reconciliation["processes"][f"initial-{family}"]["sessionId"],
             "requestedModel": reconciliation["processes"][f"initial-{family}"]["requestedModel"]}
            for family in ("claude", "gpt")
        ],
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 91, "remainingAdditions": 1137,
        "generatorCorrectionsBeforeFixtureEmission": [
            "Adjusted title replacement to follow generic variable rename.",
            "Restricted obsolete reading token check to quoted key; ordinary polite examples contain てい.",
        ],
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    paths = sorted(FOLDER.rglob("*")) + [SOURCES / "batch-065-native-preparation.json"]
    record["artifacts"] = [{"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)}
                           for path in paths if path.is_file()]
    verify(record)
    save(SOURCES / "execution-418.json", record)
    print("Exact APK archive/classes verified; original Android evidence and all four reports unchanged.")
elif mode == "checkpoint":
    record = load(SOURCES / "execution-418.json")
    verify(record)
    assert not git("status", "--porcelain")
    commit = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    before = load(CONTROL / "execution-418-before-progress.json")
    assert progress["checkpoint"] == 417 and progress["batch"] == "065"
    for key, value in before.items():
        if key != "stage":
            assert progress[key] == value, key
    checkpoint = {
        "execution": 418, "checkpoint": 418, "batch": "065", "savedCommit": commit, "signature": "G",
        "record": "docs\\n1-sources\\execution-418.json", "recordSha256": sha(SOURCES / "execution-418.json"),
        "status": "continue", "runtimePublished": False, "nativeExecuted": False,
        "allOriginalHistoricalKeysPreservedExactly": True, "dedicatedWorktreesClean": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=418, status="continue", stage="batch-065-native-compiled-pending-execution",
                    nextAction=NEXT, blocker=None)
    progress["execution418StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    progress["batch065NativePreparationCheckpoint"] = checkpoint
    progress["execution418CoordinatorCheckpoint"] = checkpoint
    save(progress_path, progress)
    save(CONTROL / "execution-418-checkpoint.json", checkpoint)
    (CONTROL / "execution-418-issue-body.txt").write_text(
        f"Batch 065 native-preparation checkpoint **418** saved locally at `{commit}` (normal signature G); no runtime publication.\n\n"
        "The exact full `ee672744` Git envelope (version `6a940651167e0e94`, 1,077 kanji / 5,036 words / 97 N1 cards) "
        "passes all 8,324 runtime hashes and original budgets (8,346 entries). The fixture compiles with one worker, "
        "without HOST-only heap init; the APK contains the exact archive and both selected cases. Android temporary paths "
        "were removed and its worktree is clean. Validator passes and the manifest is unchanged.\n\n"
        "86 static article selectors, 49 captures and eight directed routes cover all three mapped reciprocal pairs plus "
        "the 倹約/倹しい comparison. Both curated readings and ten-stroke trace/recall are planned, not executed. "
        "48 glyph and eight word-raster probes are prepared; no native/visual/phone acceptance is claimed. "
        "Accepted checkpoint-417 Android evidence and all four original reports remain unchanged, including the original "
        "permission denial, 1-GiB HOST OOM, prior 512-MiB failure and separately qualified HOST-only 2-GiB retry. "
        "Guest/app heaps and production guards are unchanged.\n\n"
        "**Next:** separate native execution with fresh device/port ownership, then original-session serial visual confirmations "
        "and combined-main/signing/CI/immutable-public-ZIP publication gates before 066. Published coverage remains "
        "**91/1,228 additions; 1,137 remain**. Compatible Android `f9b59a2+` is required; physical-phone/general-release "
        "and whole-set acceptance remain outstanding.\n", encoding="utf-8")
    print("Signed local checkpoint418 persisted with full live history and next native gate.")
elif mode == "receipt":
    receipt = load(CONTROL / "execution-418-issue-receipt.json")
    assert receipt["author"] == "stop-cran" and receipt["bodyVerified"] is True
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 418
    progress["batch065NativePreparationIssueReceipt"] = receipt
    save(CONTROL / "progress.json", progress)
    verify(load(SOURCES / "execution-418.json"))
    assert not git("status", "--porcelain")
    print("Owner issue author/body verified; final checkpoint418 and both clean worktrees verified.")
else:
    raise ValueError(mode)
