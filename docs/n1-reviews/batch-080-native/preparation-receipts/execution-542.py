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
LOGS = CONTROL / "logs" / "19bc0831-413f-4136-b1e2-f52021deadf6"
EVIDENCE = ROOT / "docs" / "n1-sources" / "execution-542.json"
NATIVE = ROOT / "docs" / "n1-reviews" / "batch-080-native"
BASE = "0d2c9aee6de9e4f430935b38e31228db4bd47908"
NEXT = (
    "SAME080 native execution ONLY next: first freshly inspect device/port/PID ownership, "
    "then use the verified frozen native-test APK and full signed0d2c9aee envelope "
    "through production ContentSync ONCE on an owned read-only API35 emulator with "
    "original guest resources/flags, explicit serial and offline network. No build "
    "rerun absent a new concern; HOST540 three RealContentTest plus one RareHanTest "
    "and successful541 native compile retained honestly. Obtain named terminal status0 "
    "for both native cases, all30Han/four families including actual ice/water fallback "
    "labels, complete two articles, reciprocal routes/SystemBack, N1 selection/meaning, "
    "sole curated kun key, seven-stroke reference trace and recall/offline evidence. "
    "Preserve actual PNGs/JSON/runner provenance, stop only owned helper, checkpoint/yield "
    "before two serial original-family visual confirmations/current-main integration/"
    "publication/081. Full source readings/order and explicit empty on list unchanged. "
    "No HOST2GiBinit in native, guest/app heap or archiveguard change. Preserve all "
    "historical source/review/process/read-depth/lookup/denial/OOM/viewport/MLKit limits; "
    "optional historical session helpers skipped. Actual new denial or signinghang: "
    "preserve/report/yield without retry/workaround. Exactly one coordinator/at most one "
    "reviewer; no second runner. Published106/1228,remaining1122/latest079b120125a; "
    "draft107 NOT delivered. CompatibleAndroidf9b59a2+ required; physicalphone/"
    "generalrelease/whole-set outstanding. All later independent visual, combined-main "
    "checks, normal signing/owner fastforward/publicSHA/terminalgreenCI/every immutable "
    "publicZIP runtimehash/original budgets/terminal receipts/ownerissue60 gates remain."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=ROOT):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], text=True, encoding="utf-8"
    ).strip()


def preserve_history(progress, original):
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in original.items():
        if key not in allowed:
            assert progress[key] == value, key
    save(CONTROL / "progress.json", progress)
    persisted = load(CONTROL / "progress.json")
    for key, value in original.items():
        if key not in allowed:
            assert persisted[key] == value, key


def start():
    original = load(CONTROL / "progress.json")
    assert original["checkpoint"] == 541 and original["batch"] == "080"
    assert original["status"] == "continue"
    assert git("rev-parse", "HEAD") == BASE
    assert not git("status", "--porcelain", root=ANDROID)
    backup = LOGS / "progress-before-542.json"
    assert not backup.exists()
    shutil.copyfile(CONTROL / "progress.json", backup)
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):",
        1,
    )[1])
    assert checkpoint["checkpoint"] == 541
    starting = {
        "execution": 542, "batch": "080", "startingHead": BASE,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME080 finalize recovered native preparation and normal signed LOCAL checkpoint only.",
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Complete request decoded/parsed; operative contract, approved issue and final checkpoint inspected. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": str(CONTROL / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [],
    }
    save(LOGS / "starting-state-542.json", starting)
    original["execution542StartingState"] = starting
    original.update(status="continue", stage="batch-080-finalizing-recovered-native-preparation",
                    blocker=None)
    preserve_history(original, load(backup))
    print("Starting state persisted; all original historical values preserved.")


def verify():
    original = load(LOGS / "progress-before-542.json")
    recovery_path = CONTROL / "batch-080-parent-postcompile-diagnostic-recovery.json"
    recovery = load(recovery_path)
    previous_path = ROOT / "docs" / "n1-sources" / "execution-541.json"
    previous = load(previous_path)
    fixture_path = ROOT / "docs" / "n1-sources" / "batch-080-native-fixture-verification.json"
    fixture = load(fixture_path)
    assert git("rev-parse", "HEAD") == BASE
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", "--name-only") and not git("diff", "--cached", "--name-only")
    assert not git("status", "--porcelain", root=ANDROID)
    assert git("rev-parse", "HEAD", root=ANDROID) == previous["androidHead"]
    assert recovery == original["parentBatch080PostcompileRecovery"]
    assert recovery["parentToolExitCode"] == 0
    assert previous["status"] == "blocked"
    for key, hash_key in (
        ("archive", "archiveSha256"), ("fixture", "fixtureSha256"),
        ("priorHarness", "priorHarnessSha256"), ("fixtureDiff", "fixtureDiffSha256"),
        ("sourceReadingLedger", "sourceReadingLedgerSha256"),
    ):
        path = Path(fixture[key])
        assert sha(path if path.is_absolute() else ROOT / path) == fixture[hash_key], key
    for row in fixture["articleFiles"] + fixture["currentFontAudit"]:
        path = Path(row["path"])
        assert sha(path if path.is_absolute() else ROOT / path) == row["sha256"]
    for row in previous["archivedReceipts"]:
        path = ROOT / row["path"]
        assert sha(path) == row["sha256"], str(path)
        if "decompressedSha256" in row:
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == row["decompressedSha256"]
    assert sha(Path(recovery["compileRawLog"])) == recovery["compileRawLogSha256"]
    compile_result = previous["compile"]
    apk = Path(compile_result["apk"])
    assert sha(apk) == compile_result["apkSha256"] == recovery["compileResult"]["apkSha256"]
    assert apk.stat().st_size == compile_result["apkBytes"]
    assert (NATIVE / "native-compile-exit.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL in 1m 17s" in (NATIVE / "native-compile.txt").read_text()
    with zipfile.ZipFile(apk) as package:
        asset = "assets/" + Path(fixture["archive"]).name
        assert hashlib.sha256(package.read(asset)).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(package.read(n) for n in package.namelist() if n.endswith(".dex"))
        for name in (
            "N1Batch080GlyphTest", "N1Batch080ArticleTest",
            "clarityLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies",
            "fullSingleImportOfflineClarityOneReciprocalPairCuratedKunDrawingAndSystemBack",
        ):
            assert name.encode() in dex, name
    sys.path.insert(0, str(ROOT / "tools"))
    from build_manifest import build_manifest
    manifest = load(ROOT / "manifest.json")
    assert build_manifest(ROOT) == manifest
    assert sha(ROOT / "manifest.json") == previous["manifestSha256"]
    binary_sections = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    verified = 0
    with zipfile.ZipFile(fixture["archive"]) as archive:
        names = archive.namelist()
        manifest_name, = (n for n in names if n.endswith("/manifest.json") or n == "manifest.json")
        prefix = manifest_name[:-len("manifest.json")]
        assert json.loads(archive.read(manifest_name)) == manifest
        retained = len(archive.read(manifest_name))
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, expected in entries.items():
                raw = archive.read(prefix + name)
                normalized = raw if section in binary_sections else raw.replace(b"\r\n", b"\n")
                assert hashlib.sha256(normalized).hexdigest() == expected, name
                assert normalized == ((ROOT / name).read_bytes() if section in binary_sections
                                      else (ROOT / name).read_bytes().replace(b"\r\n", b"\n")), name
                retained += len(raw)
                verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert len(names) == fixture["zipEntries"] <= 18_000
        assert inflated == fixture["inflatedBytes"] <= 80 * 1024 * 1024
        assert retained == fixture["retainedBytes"] <= 56 * 1024 * 1024
        assert Path(fixture["archive"]).stat().st_size == fixture["compressedBytes"] <= 42 * 1024 * 1024
    assert verified == fixture["verifiedRuntimeHashes"] == 8366
    temporary_source = ANDROID / "app" / "src" / "androidTest" / "java" / "io" / "github" / "stopcran" / "kanji" / "ui" / "N1Batch080NativeTest.kt"
    temporary_asset = ANDROID / "app" / "src" / "androidTest" / "assets" / Path(fixture["archive"]).name
    assert not temporary_source.exists() and not temporary_asset.exists()
    receipt_folder = NATIVE / "preparation-receipts"
    shutil.copyfile(recovery_path, receipt_folder / "parent-postcompile-diagnostic-recovery.json")
    shutil.copyfile(Path(__file__), receipt_folder / Path(__file__).name)
    validation_receipts = []
    assert "0 error(s)" in (LOGS / "validate-542.txt").read_text()
    assert manifest["contentVersion"] in (LOGS / "manifest-542.txt").read_text()
    for name in ("validate-542.txt", "manifest-542.txt"):
        target = NATIVE / name
        shutil.copyfile(LOGS / name, target)
        validation_receipts.append({"path": str(target.relative_to(ROOT)), "sha256": sha(target)})
    record = {
        **load(LOGS / "starting-state-542.json"), "schemaVersion": 1,
        "checkpoint": 542, "status": "continue",
        "stage": "native-preparation-verified-awaiting-normal-signature",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "parentRecovery": recovery,
        "historicalDenialRecord": str(previous_path.relative_to(ROOT)),
        "historicalDenialRecordSha256": sha(previous_path),
        "originalDenialRecordUnmodified": True,
        "fixtureVerification": str(fixture_path.relative_to(ROOT)),
        "fixtureVerificationSha256": sha(fixture_path),
        "compiledApk": compile_result, "archiveSha256": fixture["archiveSha256"],
        "fullArchiveRuntimeHashesReverified": verified,
        "manifestFreshAndUnchanged": True, "contentVersion": manifest["contentVersion"],
        "freshContentChecks": {"validatorErrors": 0, "manifestRegeneratedUnchanged": True,
                              "receipts": validation_receipts},
        "originalArchiveBudgetsReverified": True, "temporarySourceAndAssetAbsent": True,
        "dedicatedAndroidWhollyClean": True, "trackedRuntimeUnchanged": True,
        "archivedCompileAndPreparationReceiptsReverified": len(previous["archivedReceipts"]),
        "freshHostTestsRetainedWithoutRerun": "execution540 RealContentTest3+RareHanTest1, zero skips",
        "nativeCompileRetainedWithoutRerun": "execution541 exit0 BUILD SUCCESSFUL in 1m17s",
        "helper": str(Path(__file__)), "helperSha256": sha(Path(__file__)),
        "nativeExecuted": False, "nativeCasesExecuted": 0, "reviewersLaunched": 0,
        "deviceOrEmulatorInspected": False, "nativeOrVisualAcceptanceClaimed": False,
        "runtimePublished": False, "nextBatchStarted": False,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "diagnostics": [
            "Initial console summary hit cp1252 UnicodeEncodeError only after complete request load/parse; ASCII-safe summary succeeded before mutation. No source or gate weakened."
        ],
        "limits": "Local preparation evidence only. Hash/dex/static selector verification is not native execution, readability, fallback-face, handwriting, MLKit or phone acceptance. Original blocked541 remains historical; parent recovery is separately attributed. All source/review/read-depth/process/permission/OOM/phone limitations and later gates remain.",
    }
    save(EVIDENCE, record)
    print(json.dumps({"runtimeHashes": verified, "apkSha256": sha(apk),
                      "historyRootKeys": len(original), "nativeExecuted": False}, indent=2))


def finish():
    original = load(LOGS / "progress-before-542.json")
    progress = load(CONTROL / "progress.json")
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == BASE
    assert not git("status", "--porcelain")
    assert not git("status", "--porcelain", root=ANDROID)
    assert not git("diff", BASE, "HEAD", "--", "manifest.json", "kanji", "words", "articles",
                   "strokes", "tools")
    checkpoint = {
        "schemaVersion": 1, "execution": 542, "checkpoint": 542, "batch": "080",
        "status": "continue", "stage": "signed-local-native-preparation-ready-for-device-execution",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G",
        "evidence": "docs/n1-sources/execution-542.json",
        "startingEnvelopeCommit": BASE, "runtimePublished": False, "nativeExecuted": False,
        "independentVisualAcceptance": False, "actualNewPermissionDenials": [],
        "originalHistoricalRootKeysPreserved": len(original),
        "allOriginalHistoricalValuesPreservedExactly": True,
        "dedicatedWorktreesClean": True, "trackedRuntimeUnchanged": True,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
    }
    progress.update(checkpoint=542, status="continue", stage=checkpoint["stage"],
                    nextAction=NEXT, blocker=None)
    progress["execution542CoordinatorCheckpoint"] = checkpoint
    preserve_history(progress, original)
    save(LOGS / "checkpoint-verification.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


{"start": start, "verify": verify, "finish": finish}[sys.argv[1]]()
