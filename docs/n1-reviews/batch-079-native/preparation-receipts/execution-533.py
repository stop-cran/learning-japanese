import gzip
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
LOGS = CONTROL / "logs" / "b4870a38-0a79-4c37-971e-c696d37e2e33"
HEAD = "3fdc0bf952e299060b5a07ac372bb6d926595a4c"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-079-native"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


NEXT = (
    "SAME079 bounded native execution/actual PNG inspection checkpoint ONLY, then persist/yield; "
    "no publication,080 or second runner. Read docs\\n1-sources\\execution-533.json and "
    "batch-079-native-fixture-verification.json. Verify frozen full signed3fdc0bf9 archive "
    "control\\artifacts\\n1-batch-079-3fdc0bf9-envelope.zip and matching "
    "n1-batch-079-native-test.apk hashes before use; no recompile or HOST3+1 rerun absent new concern. "
    "Fresh device/5580/5581/PID ownership inspection BEFORE approved read-only API35 "
    "N3_Acceptance_20261029 emulator launch; batch0405584override was batch-specific. "
    "Same hostGPU/-Vulkan/2048MiB/2core flags, explicit actual serial, JDK17/SDK, "
    "one heavy process; stop only owned helper. Require terminal case status0/no skips "
    "for BOTH N1Batch079GlyphTest and N1Batch079ArticleTest. Production ContentSync "
    "imports entire signed Git archive ONCE, no duplicate preflight parse:1091kanji5047words"
    "111N1/contentVersiona01eb85b17601ac0/zeroProblems/acceptedepoch, "
    "Full+Lite full/curatedカン,かんむり and offeredかん/かんむり. "
    "Inspect all35Han across fourproductionfamilies, exact冖/宀fallback and冠/冗/完/守/元/寸, "
    "140individual+8wholewordrasters and threeComposepanels. Cmap absence/hashes "
    "are not readability. Actual complete冠/王冠 articles, reused冠 word and changed王 "
    "passage, threepairs/sixdirections, N1selection/meaning/bothreadings/ninestroke "
    "trace then recall/systemBack/offline. Injected reference tracing/giveup recall "
    "are not handwriting recognition or physicalphone. Preserve all attempts/PNGs/"
    "provenance/cleanup, normal signed LOCAL evidence and yield. Later two serial "
    "original-family visual confirmations ClaudeOpus5.5/GPT6.1Sol remain required. "
    "Textual closure084d5301 and fresh532 HOST3+1/no skips inherited honestly. "
    "177distinctfamilies/fiverawrecords and all original review/read-depth/lookup/process "
    "limits retained; no teaching changes. Use committed packets/approvedcontrolinputs/"
    "durablecontrolhelpers; optional historicalsession recipes NOT required. "
    "Preserve FULL live history/source/review/denial/OOM/phone limits and baseline "
    "exceptions; HOST-only2GiBinit NEVER enters native builds, no app/guestheap/archive"
    "guard increase. Later currentmain non-rewriting integration/revalidation/normal"
    "signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets/verified "
    "ownerissue60 mandatory. No unreviewedpush/authoragents/concurrentheavywork/"
    "secondrunner/signingretry/permissionworkaround; preserve/report/yield actualnewdenials. "
    "Published105/1228,remaining1123; local106thaddition textuallyclosednotpublished. "
    "CompatibleAndroidf9b59a2+; physicalphone/generalrelease/whole-set outstanding. "
    "Overallproject incomplete."
)


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 532 and progress["batch"] == "079"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not (LOGS / "progress-before-533.json").exists()
    save(LOGS / "progress-before-533.json", progress)
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution532CoordinatorCheckpoint"]["checkpoint"] == 532
    record = {
        "execution": 533, "batch": "079", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME079 native fixture preparation and compile ONLY; no device/emulator/reviewer/publication/080 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and complete checkpoint parsed before implementation; operative contract, final532 and complete issue directly inspected. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
        "manifestSha256": sha(ROOT / "manifest.json"),
        "contentVersion": load(ROOT / "manifest.json")["contentVersion"],
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "preparing-native-fixture",
    }
    progress["execution533StartingState"] = record
    progress["stage"] = "native-fixture-preparation-in-progress"
    save(CONTROL / "progress.json", progress)
    save(LOGS / "starting-state.json", record)
    print("Starting state persisted; complete live history retained.")


def record():
    starting = load(LOGS / "starting-state.json")
    fixture = load(CONTROL / "batch-079-native-fixture-verification.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("status", "--porcelain", cwd=ANDROID)
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert sha(ROOT / "manifest.json") == starting["manifestSha256"]
    assert (LOGS / "native-compile-exit.txt").read_text().strip() == "0"
    result = next(line for line in (LOGS / "native-compile.txt").read_text().splitlines()
                  if line.startswith("BUILD SUCCESSFUL"))
    assert "0 error(s)" in (LOGS / "validate.txt").read_text()
    assert sha(Path(fixture["fixture"])) == fixture["fixtureSha256"]
    assert sha(Path(fixture["archive"])) == fixture["archiveSha256"]
    apk = CONTROL / "artifacts" / "n1-batch-079-native-test.apk"
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read(
            "assets/n1-batch-079-3fdc0bf9-envelope.zip")).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch079GlyphTest", "N1Batch079ArticleTest",
                     "crownLookalikesAndCoverRoofFallbacksAcrossFourProductionFamilies",
                     "fullSingleImportOfflineCrownThreeReciprocalPairsBothReadingsDrawingAndSystemBack"):
            assert name.encode() in dex, name
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    copied = []
    for source in (CONTROL / "prepare-batch-079-native.py",
                   CONTROL / "run-533-native-compile.ps1", Path(__file__)):
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        copied.append({"path": str(target.relative_to(ROOT)), "sha256": sha(target)})
    for name in ("native-compile.txt", "native-compile-start.txt", "native-compile-end.txt",
                 "native-compile-exit.txt", "validate.txt", "manifest.txt"):
        source = LOGS / name
        target = FOLDER / name
        if name == "native-compile.txt":
            raw = FOLDER / "native-compile-raw.txt.gz"
            raw.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(raw.read_bytes()) == source.read_bytes()
            target.write_text("\n".join(line.rstrip() for line in source.read_text().splitlines()) + "\n",
                              encoding="utf-8")
            copied.append({"path": str(raw.relative_to(ROOT)), "sha256": sha(raw),
                           "decompressedSha256": sha(source)})
        else:
            shutil.copyfile(source, target)
            assert sha(source) == sha(target)
        copied.append({"path": str(target.relative_to(ROOT)), "sha256": sha(target)})
    frozen = ROOT / "docs" / "n1-sources" / "batch-079-native-fixture-verification.json"
    shutil.copyfile(CONTROL / frozen.name, frozen)
    evidence = {
        **starting, "schemaVersion": 1, "checkpoint": 533, "status": "continue",
        "stage": "native-fixture-compiled-awaiting-execution",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "nativePreparation": fixture, "fixtureVerification": str(frozen.relative_to(ROOT)),
        "fixtureVerificationSha256": sha(frozen),
        "compile": {
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process",
            "exitCode": 0, "buildResult": result,
            "startedAt": (LOGS / "native-compile-start.txt").read_text().strip(),
            "endedAt": (LOGS / "native-compile-end.txt").read_text().strip(),
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
            "oneWorker": True, "parallel": False, "hostOnlyHeapInitUsed": False,
            "productionOrGuestHeapChanged": False, "archiveGuardsChanged": False,
            "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
            "apkContainsExactFrozenArchive": True, "bothClassesAndMethodsInDex": True,
            "temporarySourceAndAssetRemoved": True, "androidWorktreeClean": True,
        },
        "archivedReceipts": copied, "originalCompileLogPreservedByteForByteInGzip": True,
        "normalizedLogDifference": "Readable compile log strips trailing whitespace only; original compressed bytes retained.",
        "validatorErrors": 0, "manifestFresh": True, "manifestBytesUnchanged": True,
        "runtimeUnchanged": True, "runtimePublished": False,
        "nativeExecuted": False, "deviceOrEmulatorInspected": False,
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "publishedAdditions": 105, "remainingAdditions": 1123,
        "lastPublishedCommit": "2a6777503de6c23c2ac5582b0265dd68d224f44c",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "limits": "Preparation and native test APK compilation only. No native cases, device/port/PID or PNG inspection, independent visual review, phone or publication acceptance. Fresh532 HOST3+1 inherited without rerun; all original source/review/read-depth/process/denial/OOM/phone limitations retained.",
    }
    save(ROOT / "docs" / "n1-sources" / "execution-533.json", evidence)
    print(json.dumps({"stage": evidence["stage"], "apkSha256": sha(apk),
                      "exactArchiveInsideApk": True, "receipts": len(copied)}, indent=2))


def checkpoint():
    progress = load(CONTROL / "progress.json")
    original = load(LOGS / "progress-before-533.json")
    assert progress["checkpoint"] == 532 and progress["batch"] == "079"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    evidence = load(ROOT / "docs" / "n1-sources" / "execution-533.json")
    receipt = load(LOGS / "issue-response.json")
    body = (LOGS / "issue-body.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    assert "issues/60#issuecomment-" in receipt["html_url"]
    assert sha(ROOT / "manifest.json") == evidence["manifestSha256"]
    result = {
        "schemaVersion": 1, "execution": 533, "checkpoint": 533, "batch": "079",
        "savedCommit": signed, "signature": "G", "status": "continue",
        "stage": "native-fixture-compiled-awaiting-execution",
        "evidence": "docs/n1-sources/execution-533.json",
        "evidenceSha256": sha(ROOT / "docs" / "n1-sources" / "execution-533.json"),
        "compileExitCode": 0, "nativeCasesExecuted": 0, "nativeExecuted": False,
        "fixtureSha256": evidence["nativePreparation"]["fixtureSha256"],
        "archiveSha256": evidence["nativePreparation"]["archiveSha256"],
        "testApkSha256": evidence["compile"]["apkSha256"],
        "runtimePayloadHashesVerified": 8363,
        "zipEntries": evidence["nativePreparation"]["zipEntries"],
        "contentVersion": evidence["contentVersion"], "runtimeBytesUnchanged": True,
        "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 105, "remainingAdditions": 1123,
        "lastPublishedCommit": evidence["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "originalRootKeyCountCompared": len(original),
        "changedRootFields": ["checkpoint", "status", "stage", "nextAction", "blocker"],
    }
    progress.update(checkpoint=533, status="continue", stage=result["stage"],
                    nextAction=NEXT, blocker=None)
    progress["execution533CoordinatorCheckpoint"] = result
    progress["batch079NativePreparation"] = result
    allowed = set(result["changedRootFields"])
    for key, value in original.items():
        if key not in allowed:
            assert progress[key] == value, key
    save(CONTROL / "progress.json", progress)
    check = load(CONTROL / "progress.json")
    for key, value in original.items():
        if key not in allowed:
            assert check[key] == value, key
    save(LOGS / "checkpoint-verification.json", result)
    print(json.dumps({"checkpoint": 533, "savedCommit": signed, "status": "continue",
                      "historyKeysPreserved": len(original), "issueUpdate": receipt["html_url"]}, indent=2))


{"start": start, "record": record, "checkpoint": checkpoint}[sys.argv[1]]()
