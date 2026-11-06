import hashlib
import gzip
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
LOGS = CONTROL / "logs" / "0990b8e3-abc9-4197-8e29-b72c996ca602"
HEAD = "7fb6c46374f2464648130f2473fabcb9137bb7d4"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 524 and progress["batch"] == "078"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not (LOGS / "progress-before-525.json").exists()
    save(LOGS / "progress-before-525.json", progress)
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    record = {
        "execution": 525, "batch": "078", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME078 bounded native fixture preparation and compile only; no emulator, reviewer, publication,079 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, final524 and complete issue directly inspected. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
        "manifestSha256": sha(ROOT / "manifest.json"),
        "contentVersion": load(ROOT / "manifest.json")["contentVersion"],
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "preparing-native-fixture",
    }
    progress["execution525StartingState"] = record
    progress["stage"] = "native-fixture-preparation-in-progress"
    save(CONTROL / "progress.json", progress)
    save(LOGS / "starting-state.json", record)
    print("Execution525 starting state persisted; all prior history retained.")


NEXT = (
    "SAME078 bounded native execution/inspection checkpoint ONLY, then persist/yield; "
    "no publication,079 or second runner. Native fixture and test APK compiled successfully "
    "at signed local checkpoint525. Read docs\\n1-sources\\execution-525.json and "
    "batch-078-native-fixture-verification.json; source fixture/diff/compile/helper receipts "
    "are committed under docs\\n1-reviews\\batch-078-native. Use frozen full signed "
    "7fb6c463 archive n1-batch-078-7fb6c463-envelope.zip and matching "
    "control\\artifacts\\n1-batch-078-native-test.apk; verify their recorded hashes first. "
    "Do not recompile or rerun HOST3+1 without a new concern. Fresh device/5580/5581/PID "
    "ownership inspection BEFORE approved read-only API35 N3_Acceptance_20261029 emulator "
    "launch; batch0405584override was batch-specific. Same host GPU/-Vulkan/2048MiB/"
    "2core flags, explicit actual serial, JDK17/SDK, one heavy process. Stop only owned "
    "helper. Native fixture imports entire archive through production ContentSync ONCE "
    "(no preflight parse), asserts1090kanji5046words110N1/version8e06edf2b0857b26/"
    "zeroProblems/acceptedepoch and Full+Lite full/curatedジョウ,emptykun,soleじょうkey. "
    "Require terminal case status0 for BOTH N1Batch078GlyphTest and "
    "N1Batch078ArticleTest, no skips. Verify all27actualHan across fourproductionfonts, "
    "especially exact冖/几fallback and 冗/元/兄/見,108individual+4wholewordrasters/"
    "threeComposepanels. Inspect actualPNGs; hashes/cmap absence are not readability. "
    "Exercise complete冗 and reused冗談 including corrected literal-negative/rejection "
    "qualification, changed談 common-word passage, all2mappedpairs4directions, "
    "selection/meaning/soleonreading/emptykun/fourstroketracethenrecall/systemBack/offline. "
    "Touch injected reference tracing and give-up recall are not handwriting recognition "
    "or physicalphone evidence. Preserve exact attempt logs/PNGs/provenance, cleanup, "
    "normal signed LOCAL evidence, checkpoint/yield. Later two serial original-family "
    "visual confirmations ClaudeOpus5.5/GPT6.1Sol; no overlap/heavywork concurrently. "
    "Textual closure523 and fresh HOST3+1 zero-skips524 remain valid, no new teaching. "
    "8360runtimehashes/localfullarchive8382entries/originalbudgets pass; no "
    "guest/appheap/archiveguard changes, HOST-only2GiBinit NEVER enters native builds. "
    "Use committed source packets/approvedcontrolinputs/durablecontrolhelpers, not "
    "optional historical session-state recipes. Preserve FULL history and actual "
    "denials/OOM/review/read-depth/phone limitations. Later currentmain non-rewriting "
    "integration/revalidation/normal signing/ownerfastforward/greenCI/EVERYimmutableZIP"
    "hash/originalbudgets/verifiedownerissue60 still mandatory. No unreviewedpush/"
    "authoragents/secondrunner/signingretry/permissionworkaround. Preserve/report/yield "
    "on actualnewdenials. Published104/1228,remaining1124; local105th addition "
    "textuallyclosednotpublished, ZEROnew078wordarticle. CompatibleAndroidf9b59a2+; "
    "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def record():
    starting = load(LOGS / "starting-state.json")
    fixture = load(CONTROL / "batch-078-native-fixture-verification.json")
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", cwd=ANDROID)
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert sha(ROOT / "manifest.json") == starting["manifestSha256"]
    prefix = "native-compile-attempt-2"
    assert (LOGS / f"{prefix}-exit.txt").read_text().strip() == "0"
    build_result = next(line for line in (LOGS / f"{prefix}.txt").read_text().splitlines()
                        if line.startswith("BUILD SUCCESSFUL"))
    assert "0 error(s)" in (LOGS / "validate.txt").read_text()
    assert sha(Path(fixture["fixture"])) == fixture["fixtureSha256"]
    assert sha(Path(fixture["archive"])) == fixture["archiveSha256"]
    apk = CONTROL / "artifacts" / "n1-batch-078-native-test.apk"
    with zipfile.ZipFile(apk) as archive:
        asset = "assets/n1-batch-078-7fb6c463-envelope.zip"
        assert hashlib.sha256(archive.read(asset)).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch078GlyphTest", "N1Batch078ArticleTest",
                     "redundancyLookalikesAndCoverTableFallbacksAcrossFourProductionFamilies",
                     "fullSingleImportOfflineRedundancyTwoReciprocalPairsSoleOnReadingDrawingAndSystemBack"):
            assert name.encode() in dex, name
    folder = ROOT / "docs" / "n1-reviews" / "batch-078-native"
    receipts = folder / "preparation-receipts"
    receipts.mkdir()
    copied = []
    for source in (CONTROL / "prepare-batch-078-native.py",
                   CONTROL / "run-525-native-compile.ps1",
                   CONTROL / "preserve-525-preparation-attempt-1.py", Path(__file__)):
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        copied.append({"path": str(target.relative_to(ROOT)), "sha256": sha(target)})
    for source_name, target_name in (
        (f"{prefix}.txt", "compile.txt"), (f"{prefix}-start.txt", "compile-start.txt"),
        (f"{prefix}-end.txt", "compile-end.txt"), (f"{prefix}-exit.txt", "compile-exit.txt"),
        ("validate.txt", "validate.txt"), ("manifest.txt", "manifest.txt"),
    ):
        source, target = LOGS / source_name, folder / target_name
        if target_name == "compile.txt":
            raw_archive = folder / "compile-raw.txt.gz"
            raw_archive.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(raw_archive.read_bytes()) == source.read_bytes()
            target.write_text("\n".join(line.rstrip() for line in source.read_text().splitlines()) + "\n", encoding="utf-8")
            copied.append({"path": str(raw_archive.relative_to(ROOT)), "sha256": sha(raw_archive),
                           "decompressedSha256": sha(source)})
        else:
            shutil.copyfile(source, target)
            assert sha(source) == sha(target)
        copied.append({"path": str(target.relative_to(ROOT)), "sha256": sha(target)})
    frozen = ROOT / "docs" / "n1-sources" / "batch-078-native-fixture-verification.json"
    shutil.copyfile(CONTROL / "batch-078-native-fixture-verification.json", frozen)
    value = {
        **starting, "schemaVersion": 1, "checkpoint": 525,
        "status": "continue", "stage": "native-fixture-compiled-awaiting-execution",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "fixtureVerification": str(frozen.relative_to(ROOT)),
        "fixtureVerificationSha256": sha(frozen),
        "nativePreparation": fixture,
        "compile": {
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process",
            "attempt": 2, "exitCode": 0, "buildResult": build_result,
            "startedAt": (LOGS / f"{prefix}-start.txt").read_text().strip(),
            "endedAt": (LOGS / f"{prefix}-end.txt").read_text().strip(),
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
            "oneWorker": True, "parallel": False, "hostOnlyHeapInitUsed": False,
            "productionOrGuestHeapChanged": False, "archiveGuardsChanged": False,
            "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
            "apkContainsExactFrozenArchive": True, "bothClassesAndMethodsInDex": True,
            "temporarySourceAndAssetRemoved": True, "androidWorktreeClean": True,
            "warnings": "Three pre-existing SOFT_INPUT_ADJUST_RESIZE deprecations in CounterFlowTest, GrammarAnswerFlowTest and WordAnswerFlowTest; no batch078 compiler warning.",
        },
        "archivedReceipts": copied, "originalLogsPreservedByteForByteInRawGzip": True,
        "normalizedLogDifference": "compile.txt strips trailing whitespace only; exact original in compile-raw.txt.gz.",
        "priorPreparationAttempt": {
            "directory": "docs/n1-reviews/batch-078-native/preparation-attempt-1",
            "status": "compiled-successfully-not-executed-superseded",
            "reason": "Static comparison with production Markdown.kt found indented English translation bullets incorrectly joined to Japanese examples by the inherited projection. Revised fixture splits the real nodes and adds separate visibility assertions; frozen runtime archive unchanged.",
            "apk": str(CONTROL / "artifacts" / "n1-batch-078-native-test-attempt-1.apk"),
            "apkSha256": "4dc6f6cc18f1cfc5b3f118c2b987674635ebe6b4398d2ace8f4027b5391f6848",
        },
        "validatorErrors": 0, "manifestFresh": True, "manifestBytesUnchanged": True,
        "runtimeUnchanged": True, "runtimePublished": False,
        "nativeExecuted": False, "deviceOrEmulatorInspected": False,
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "publishedAdditions": 104, "remainingAdditions": 1124,
        "lastPublishedCommit": "d7170f11e271a8de47bd2fd152e7196b96bff189",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "limits": "Preparation and native test APK compilation ONLY. No native case run, device/port inspection, PNG inspection, independent visual review, phone or publication acceptance. 524 fresh HOST three+one results inherited without rerun; historical source/review/process/denial/OOM/read-depth limits unchanged.",
    }
    save(ROOT / "docs" / "n1-sources" / "execution-525.json", value)
    print(json.dumps({"status": value["stage"], "apkSha256": sha(apk),
                      "archiveBytesVerifiedInsideApk": True, "receipts": len(copied)}, indent=2))


def checkpoint():
    current = load(CONTROL / "progress.json")
    original = load(LOGS / "progress-before-525.json")
    assert current["checkpoint"] == 524 and current["batch"] == "078"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    evidence_path = ROOT / "docs" / "n1-sources" / "execution-525.json"
    evidence = load(evidence_path)
    receipt = load(LOGS / "issue-response.json")
    body = (LOGS / "issue-body.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    assert "issues/60#issuecomment-" in receipt["html_url"]
    assert sha(ROOT / "manifest.json") == evidence["manifestSha256"]
    result = {
        "schemaVersion": 1, "execution": 525, "checkpoint": 525, "batch": "078",
        "savedCommit": signed, "signature": "G", "status": "continue",
        "stage": "native-fixture-compiled-awaiting-execution",
        "dedicatedWorktreesClean": True, "runtimePublished": False,
        "record": str(evidence_path.relative_to(ROOT)), "recordSha256": sha(evidence_path),
        "compileExitCode": 0, "nativeCasesExecuted": 0, "nativeExecuted": False,
        "fixtureSha256": evidence["nativePreparation"]["fixtureSha256"],
        "archiveSha256": evidence["nativePreparation"]["archiveSha256"],
        "testApkSha256": evidence["compile"]["apkSha256"],
        "runtimePayloadHashesVerified": 8360, "zipEntries": 8382,
        "contentVersion": evidence["contentVersion"], "manifestBytesUnchanged": True,
        "publishedAdditions": 104, "remainingAdditions": 1124,
        "lastPublishedCommit": evidence["lastPublishedCommit"], "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False,
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "originalRootKeyCountCompared": len(original),
        "changedRootFields": ["checkpoint", "stage", "nextAction"],
    }
    current["checkpoint"] = 525
    current["stage"] = result["stage"]
    current["nextAction"] = NEXT
    current["execution525StartingState"]["status"] = "signed-local-native-compile-checkpoint-complete"
    current["execution525CoordinatorCheckpoint"] = result
    current["batch078NativePreparationCheckpoint"] = result
    for key, value in original.items():
        if key not in result["changedRootFields"]:
            assert current[key] == value, key
    save(CONTROL / "progress.json", current)
    saved = load(CONTROL / "progress.json")
    for key, value in original.items():
        if key not in result["changedRootFields"]:
            assert saved[key] == value, key
    assert saved["checkpoint"] == 525 and saved["status"] == "continue"
    save(LOGS / "checkpoint-525.json", result)
    print(json.dumps({"savedCommit": signed, "checkpoint": 525, "status": saved["status"],
                      "historyRootKeysPreserved": len(original), "issueUpdate": receipt["html_url"]}))


if __name__ == "__main__":
    {"start": start, "record": record, "checkpoint": checkpoint}[sys.argv[1] if len(sys.argv) > 1 else "start"]()
