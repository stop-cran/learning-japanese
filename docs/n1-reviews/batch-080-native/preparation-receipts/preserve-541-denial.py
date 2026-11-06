import gzip
import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
LOGS = CONTROL / "logs" / "593f89b0-4aa4-4f11-bcd4-d94ebc4f2dea"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-080-native"
DENIED_COMMAND = (
    "git --no-pager status --short; Get-Content "
    "..\\control\\logs\\593f89b0-4aa4-4f11-bcd4-d94ebc4f2dea\\native-compile.txt "
    "| Select-String -SimpleMatch 'warning:','e:','w:' | Select-Object -First 12"
)
DENIAL = (
    "Permission denied because no interactive user response was available. "
    "Retry in an interactive session so the user can approve it, or try an "
    "alternative that does not require this permission."
)
NEXT = (
    "SAME080: actual new tool denial after successful native fixture compile. "
    "Preserved docs/n1-sources/execution-541.json, all fixture/compile receipts, "
    "full signed0d2c9aee archive and n1-batch-080-native-test.apk. No denied "
    "operation retried or alternative used to obtain its result. Resolve scoped "
    "authorization/disposition for the compound status/compile-diagnostic command, "
    "then resume SAME080 bounded native-preparation evidence finalization and "
    "normal signed LOCAL checkpoint only before any device/native execution. "
    "No signing attempted, no push/reviewer/device/emulator/081/second runner. "
    "All native/PNG/two serial original-family visual/current-main integration/"
    "publication acceptance gates remain. Fresh540HOST3+1 inherited honestly. "
    "Full runtime/manifest unchanged; full live history and all source/review/"
    "read-depth/process/permission/OOM/phone limitations retained. Optional "
    "historical session-state helpers not accessed. Preserve/report/yield actual "
    "new denial; signinghang stop/yield without retry. Published106/1228,remaining1122; "
    "compatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preserve():
    original = load(LOGS / "progress-before-541.json")
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == original["checkpoint"] == 540
    starting = load(LOGS / "starting-state-541.json")
    fixture_path = CONTROL / "batch-080-native-fixture-verification.json"
    fixture = load(fixture_path)
    assert (LOGS / "native-compile-exit.txt").read_text().strip() == "0"
    assert sha(Path(fixture["fixture"])) == fixture["fixtureSha256"]
    assert sha(Path(fixture["archive"])) == fixture["archiveSha256"]
    assert sha(ROOT / "manifest.json") == starting["manifestSha256"]
    assert "0 error(s)" in (LOGS / "validate.txt").read_text()
    apk = CONTROL / "artifacts" / "n1-batch-080-native-test.apk"
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read(
            "assets/n1-batch-080-0d2c9aee-envelope.zip")).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch080GlyphTest", "N1Batch080ArticleTest",
                     "clarityLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies",
                     "fullSingleImportOfflineClarityOneReciprocalPairCuratedKunDrawingAndSystemBack"):
            assert name.encode() in dex, name
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    copied = []
    for source in (CONTROL / "execution-541.py", CONTROL / "run-541-native-compile.ps1", Path(__file__)):
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
    frozen = ROOT / "docs" / "n1-sources" / fixture_path.name
    shutil.copyfile(fixture_path, frozen)
    record = {
        **starting, "schemaVersion": 1, "execution": 541, "checkpoint": 541,
        "status": "blocked", "stage": "blocked-permission-after-native-fixture-compile",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "savedCommit": starting["startingHead"], "newCommitCreated": False,
        "uncommittedEvidence": [str(FOLDER.relative_to(ROOT)), str(frozen.relative_to(ROOT)),
                                "docs/n1-sources/execution-541.json"],
        "deniedCommand": DENIED_COMMAND, "actualToolDenial": DENIAL,
        "denialScope": "Compound repository status / compile-log diagnostics; tool returned no command results. No component inferred to be individually denied or permitted.",
        "deniedOperationRetried": False, "permissionWorkaroundAttempted": False,
        "postDenialTaskImplementationContinued": False,
        "postDenialOperations": "Evidence/checkpoint preservation and authorized owner issue reporting only; no substitute status or warning query.",
        "nativePreparation": fixture,
        "compile": {
            "exitCode": 0, "buildResult": "BUILD SUCCESSFUL in 1m 17s",
            "oneWorker": True, "parallel": False, "hostOnlyHeapInitUsed": False,
            "productionOrGuestHeapChanged": False, "archiveGuardsChanged": False,
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process",
            "startedAt": (LOGS / "native-compile-start.txt").read_text().strip(),
            "endedAt": (LOGS / "native-compile-end.txt").read_text().strip(),
            "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
            "apkContainsExactFrozenArchive": True, "bothClassesAndMethodsInDex": True,
            "temporarySourceAndAssetCleanupVerifiedBeforeDenial": True,
        },
        "archivedReceipts": copied, "originalCompileBytesPreservedInGzip": True,
        "normalizedLogDifference": "Readable compile log strips trailing whitespace only.",
        "validatorErrors": 0, "manifestFresh": True, "manifestBytesUnchanged": True,
        "runtimeUnchangedBeforeDenial": True, "androidCleanVerifiedBeforeDenial": True,
        "finalGitStatusNotObtained": True, "signingAttempted": False,
        "runtimePublished": False, "nativeCasesExecuted": 0, "nativeExecuted": False,
        "deviceOrEmulatorInspected": False, "reviewersLaunched": 0, "nextBatchStarted": False,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "actualNewPermissionDenials": [{"command": DENIED_COMMAND, "response": DENIAL}],
        "diagnostics": [
            "Initial console request summary hit cp1252 UnicodeEncodeError after complete load/parse; ASCII-safe summary then succeeded before mutation.",
            "Broad control listing oversized; subsequent discovery narrowed without reading optional historical session-state helpers.",
            "Static stale-fixture guard falsely matched legitimate ごかん; narrowed it to exact stale quoted reading labels before creating archive/fixture. Original failed attempts were pre-write."
        ],
        "limits": "Fixture prepared/compiled only, not native/visual/phone/publication acceptance. No signed evidence freeze yet. Fresh540 HOST3+1 inherited without rerun; all earlier evidence limits remain. Final diagnostic command denied and not retried; preserving/reporting/yielding.",
    }
    save(ROOT / "docs" / "n1-sources" / "execution-541.json", record)
    checkpoint = {
        **{k: record[k] for k in (
            "schemaVersion", "execution", "checkpoint", "status", "stage", "savedCommit",
            "newCommitCreated", "uncommittedEvidence", "actualNewPermissionDenials",
            "deniedOperationRetried", "permissionWorkaroundAttempted", "signingAttempted",
            "runtimePublished", "nativeExecuted", "nativeCasesExecuted",
            "publishedAdditions", "remainingAdditions", "lastPublishedCommit",
            "physicalPhoneAcceptance", "generalReleaseAcceptance", "wholeProjectComplete",
            "optionalHistoricalHelpersAccessed", "nextAction")},
        "batch": "080", "evidence": "docs/n1-sources/execution-541.json",
        "compileExitCode": 0, "testApkSha256": sha(apk),
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "originalRootKeyCountCompared": len(original),
    }
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    progress.update(checkpoint=541, status="blocked", stage=record["stage"], nextAction=NEXT,
                    blocker={"kind": "permission", "command": DENIED_COMMAND, "response": DENIAL})
    progress["execution541CoordinatorCheckpoint"] = checkpoint
    for key, value in original.items():
        if key not in allowed:
            assert progress[key] == value, key
    save(CONTROL / "progress.json", progress)
    check = load(CONTROL / "progress.json")
    for key, value in original.items():
        if key not in allowed:
            assert check[key] == value, key
    save(LOGS / "checkpoint-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 541, "status": "blocked", "apkSha256": sha(apk),
                      "historyRootKeysPreserved": len(original)}, indent=2))


def receipt():
    response = load(LOGS / "issue-response.json")
    expected = (LOGS / "issue-body.txt").read_text(encoding="utf-8")
    assert response["user"]["login"] == "stop-cran"
    assert response["body"].replace("\r\n", "\n").rstrip() == expected.rstrip()
    assert "issues/60#issuecomment-" in response["html_url"]
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 541 and progress["status"] == "blocked"
    progress["execution541CoordinatorCheckpoint"]["issueUpdate"] = response["html_url"]
    progress["execution541CoordinatorCheckpoint"]["ownerAuthorAndBodyVerified"] = True
    save(CONTROL / "progress.json", progress)
    save(LOGS / "checkpoint-verification.json", progress["execution541CoordinatorCheckpoint"])
    print(response["html_url"])


{"preserve": preserve, "receipt": receipt}[sys.argv[1]]()
