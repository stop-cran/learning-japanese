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
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-066-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "175fdf3f1605f231e27a9de19a7c18c4a02cb20d"
NEXT = (
    "SAME066 signed compiled native-preparation checkpoint426. Execute "
    "control\\artifacts\\n1-batch-066-native-test.apk using N1Batch066GlyphTest and "
    "N1Batch066ArticleTest against exact full signed175fdf3f Git envelope. Read "
    "docs\\n1-sources\\execution-426.json and batch-066-native-preparation.json. "
    "Fresh adb inventory and local/remote5580-5581 connection/PID ownership immediately "
    "before known read-only N3_Acceptance_20261029 API35 hostGPU Vulkan-disabled "
    "emulator-5580 (-port5580 -read-only -no-snapshot -no-window -no-audio -gpu host "
    "-feature -Vulkan -memory2048 -cores2). Record owned parent/QEMU and stop ONLY owned "
    "helper;040 alternate-port exception not inherited. Keep guest/app heaps, font code "
    "and archive guards unchanged. Full archive through productionContentSyncONCE: "
    "1078kanji5036words98N1/a9ecc100b6c1335c/problems0/epoch1; full and curatedリョウ/"
    "emptyKun in Lite+Full; normalizedりょう, no Kun log. Require BOTH actual terminal "
    "case0/no skips/raw logs/direct PNG inspection of僚療像値人亻疒同口/同僚 in four "
    "production rows.36singlePaint+4word-raster probes planned;54staticselectors/"
    "32articlecaptures do not establish native semantics/readability. Both mapped pairs "
    "僚-同僚/同-同僚 in4directions, complete3articles/SystemBack/offline/N1selection/"
    "meaning/solecuratedOnGood/persistedgrade/14reference-stroke touch/ungradedtrace/"
    "recallmiss/persistedDrawAgain. Raster hashes do not identify fallback faces or "
    "certify readability; trace/recall miss is not MLKit or human handwriting evidence. "
    "Accepted425 freshAndroid3+1 inherited without redundant Gradle; HOST-only2GiB "
    "init NEVER for native builds. All historical denials/HOST OOM evidence retained. "
    "After nativePASS use ORIGINAL Claude9db759dd-1a9d-4c7f-b3ab-049af5686bc4 and "
    "GPT81338bd1-836a-4b79-9fc6-69d90c5d00ab sessions SERIALly for bounded dependent "
    "visual confirmations with actual supported CLI/read-only tool controls and scoped "
    "control access; record exact returned images/read-depth/source limits, not fresh "
    "blind reviews. Then freshlatestmain nonrewriting integration/allcombined "
    "source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normal "
    "signing/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/"
    "ownerissue60 BEFOREdelivery or067. Permissiondenial or signingwait: preserve exact "
    "command/error and yield; no workaround. No secondrunner/concurrentheavywork/"
    "supervisorchanges. PreserveFULLlivehistory. Published92/1228,1136remain/latest065 "
    "44645f54; local066 NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/"
    "generalrelease/whole-set outstanding. Overallproject incomplete."
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
    preparation = load(CONTROL / "batch-066-native-fixture-verification.json")
    apk = CONTROL / "artifacts" / "n1-batch-066-native-test.apk"
    with zipfile.ZipFile(apk) as package:
        assert hashlib.sha256(package.read("assets/n1-batch-066-175fdf3f-envelope.zip")).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist() if re.fullmatch(r"classes\d*\.dex", name)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch066{kind}Test;".encode() in blob for blob in dex)
            for old in ("064", "065"):
                assert all(f"Lio/github/stopcran/kanji/ui/N1Batch{old}{kind}Test;".encode() not in blob for blob in dex)
        for method in (
            "colleagueLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
            "fullSingleImportOfflineColleagueTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
        ):
            assert any(method.encode() in blob for blob in dex)
    raw_log = CONTROL / "logs" / "execution-426-native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (CONTROL / "logs" / "execution-426-native-compile-exit.txt").read_text().strip() == "0"
    assert not (FOLDER / "compile.txt").exists()
    (FOLDER / "compile.txt").write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    assert gzip.decompress((FOLDER / "compile-raw.txt.gz").read_bytes()) == raw_log.read_bytes()
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    for name in ("start-426.py", "prepare-426-native.py", "run-426-native-compile.ps1", "finish-426.py"):
        shutil.copyfile(CONTROL / name, receipts / name)
    save(SOURCES / "batch-066-native-preparation.json", preparation)
    assert not (ANDROID / "app" / "src" / "androidTest" / "java" / "io" / "github" / "stopcran" / "kanji" / "ui" / "N1Batch066NativeTest.kt").exists()
    assert not (ANDROID / "app" / "src" / "androidTest" / "assets" / "n1-batch-066-175fdf3f-envelope.zip").exists()
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version a9ecc100b6c1335c")):
        path = CONTROL / "logs" / f"execution-426-{name}.txt"
        assert expected in path.read_text(encoding="utf-8-sig")
        destination = FOLDER / f"{name}.txt"
        destination.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(destination.relative_to(ROOT)), "sha256": sha(destination)})
    assert len(preparation["staticMarkdownSelectors"]) == 54
    assert preparation["captureSteps"] == 32 and len(preparation["articleRouteTransitions"]) == 4
    source = Path(preparation["fixture"]).read_text(encoding="utf-8")
    assert source.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in source
    assert 'assertEquals(14, strokes.length())' in source
    inherited = load(SOURCES / "execution-425.json")
    for item in inherited["tests"]:
        assert sha(ROOT / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-066-reconciliation.json")
    reports = {}
    for process in reconciliation["processes"].values():
        path = ROOT / "docs" / "n1-reviews" / process["report"]
        assert sha(path) == process["reportSha256"]
        reports[path.relative_to(ROOT).as_posix()] = sha(path)
    record = {
        "schemaVersion": 1, "execution": 426, "batch": "066",
        "status": "native-compiled-pending-execution", "startingHead": HEAD,
        "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
        "scope": load(CONTROL / "execution-426-start.json")["scope"],
        "authorization": load(CONTROL / "execution-426-start.json")["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-066-native-preparation.json",
        "preparationSha256": sha(SOURCES / "batch-066-native-preparation.json"),
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
            "bothBatch066ClassDescriptorsAndMethodsPresent": True, "oldBatch064And065ClassDescriptorsAbsent": True,
            "temporaryAndroidSourceAndAssetRemoved": True, "androidWhollyClean": True,
            "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks,
        "fixture": preparation["fixture"], "fixtureSha256": preparation["fixtureSha256"],
        "archive": preparation["archive"], "archiveSha256": preparation["archiveSha256"],
        "selectorAudit": {"completeArticleSelectors": 54, "articleCaptureSteps": 32,
                          "reciprocalPairs": 2, "directedReciprocalTransitions": 4,
                          "method": preparation["projectionQualification"]},
        "accepted425AndroidRetainedWithoutRerun": True,
        "inherited425ArchivedXmlHashesReverified": True,
        "originalReportHashesUnchanged": reports,
        "originalReviewerSessionsForLaterDependentVisualConfirmation": [
            {"family": family, "sessionId": process["sessionId"], "requestedModel": process["requestedModel"]}
            for family, process in reconciliation["processes"].items()
        ],
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 92, "remainingAdditions": 1136,
        "generatorCorrectionBeforeFixtureEmission": "First static destination assertion saw the external dictionary citation labelled 同僚 as a second article destination. Restricted article-route audit to relative links; original failure occurred before archive/fixture emission and did not change teaching.",
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(FOLDER.rglob("*")) + [SOURCES / "batch-066-native-preparation.json"] if path.is_file()
    ]
    verify(record)
    save(SOURCES / "execution-426.json", record)
    print("Exact APK archive/classes verified; inherited Android XML and original reports unchanged.")
elif mode == "checkpoint":
    record = load(SOURCES / "execution-426.json")
    verify(record)
    assert not git("status", "--porcelain")
    commit = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    before = load(CONTROL / "execution-426-before-progress.json")
    assert progress["checkpoint"] == 425 and progress["batch"] == "066"
    for key, value in before.items():
        if key != "stage":
            assert progress[key] == value, key
    checkpoint = {
        "execution": 426, "checkpoint": 426, "batch": "066", "savedCommit": commit, "signature": "G",
        "record": "docs\\n1-sources\\execution-426.json", "recordSha256": sha(SOURCES / "execution-426.json"),
        "status": "continue", "runtimePublished": False, "nativeExecuted": False,
        "allOriginalHistoricalKeysPreservedExactly": True, "dedicatedWorktreesClean": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=426, status="continue", stage="batch-066-native-compiled-pending-execution",
                    nextAction=NEXT, blocker=None)
    progress["execution426StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    progress["batch066NativePreparationCheckpoint"] = checkpoint
    progress["execution426CoordinatorCheckpoint"] = checkpoint
    save(progress_path, progress)
    save(CONTROL / "execution-426-checkpoint.json", checkpoint)
    (CONTROL / "execution-426-issue-body.txt").write_text(
        f"Batch 066 native-preparation checkpoint **426** saved locally at `{commit}` (normal signature G); no runtime publication.\n\n"
        "The exact full `175fdf3f` Git archive (version `a9ecc100b6c1335c`, 1,078 kanji / 5,036 words / 98 N1 cards) "
        "passes all 8,326 runtime hashes and original budgets (8,348 entries). The fixture compiles with one worker, "
        "without HOST-only heap init; its APK contains the exact archive and both selected cases. Temporary Android "
        "source/assets were removed and its worktree is clean. Validator passes; the manifest is unchanged.\n\n"
        "54 static article selectors, 32 article captures and four directed routes cover both mapped reciprocal pairs "
        "(僚–同僚 and 同–同僚). Sole curated リョウ and fourteen-stroke trace/recall are planned, not executed. "
        "36 glyph and four whole-word raster probes include standalone 亻/疒; no native/visual/phone acceptance "
        "is claimed. Fresh checkpoint-425 Android evidence and both original review reports remain unchanged. "
        "All historical permission/memory failures remain retained; guest/app heaps and production guards are unchanged.\n\n"
        "**Next:** separate native execution with fresh device/port ownership, then original-session serial visual confirmations "
        "and combined-main/signing/CI/immutable-public-ZIP gates before publication or 067. Published coverage remains "
        "**92/1,228 additions; 1,136 remain**. Compatible Android `f9b59a2+` is required; physical-phone/general-release "
        "and whole-set acceptance remain outstanding.\n", encoding="utf-8")
    print("Signed local checkpoint426 persisted with full live history and next native gate.")
else:
    raise ValueError(mode)
