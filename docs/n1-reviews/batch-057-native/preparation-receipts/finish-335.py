import difflib
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
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-057-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "d9712bf9a2c03f3fae51c2f751481a05affbc0f9"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd,
                                   encoding="utf-8").strip()


next_action = (
    "SAME057 normally signed compiled native-preparation checkpoint335. NEXT bounded gate: "
    "execute frozen control/artifacts/n1-batch-057-native-test.apk with N1Batch057GlyphTest and "
    "N1Batch057ArticleTest against exact complete signedd9712bf9 envelope; read "
    "docs/n1-sources/execution-335.json and batch-057-native-preparation.json. "
    "Fresh adb/device and ALL local/remote5580-5581 connection/PID ownership immediately before "
    "known read-only N3_Acceptance_20261029 API35 hostGPU Vulkan-disabled helper at explicit "
    "emulator-5580; use full SDK emulator flags -port5580 -read-only -no-snapshot -no-window "
    "-no-audio -gpu host -feature -Vulkan -memory2048 -cores2. Record actual owned parent/QEMU "
    "and stop ONLY owned helper. 040 alternate-port exception NOT inherited. No production/content/"
    "font/guest-app-heap/archive-guard changes. Full archive through productionContentSyncONCE "
    "with1069kanji5028words89N1/47f11f7f539a1d55/problems0/epoch1; Lite+Full orderedキ/"
    "くわだ.てる,たくら.む and curatedキ/くわだ.てる, normalizedき/くわだてる; excludeたくらむ "
    "as a wrong option. Require BOTH terminalcase0/no skips/rawlogs/actual direct PNG inspection "
    "of企全危休人止業/企業/企てる in four production font rows, new企てる and reused企業 "
    "articles/two reciprocal pairs/four directions/SystemBack/offline/meaning/BOTHcuratedGood "
    "persistent grades/six touch-reference strokes/ungraded trace/recall miss/persistedDrawAgain. "
    "28 singlePaint+8 fullword probes planned; complete-word bitmap measured, not fixed256px. "
    "54 complete-article static selectors/32 article capture steps audited, NOT native acceptance. "
    "Rasterhashes not readability/fallback-face identification; offline reference/recallmiss not MLKit "
    "or correct human recall. Accepted334 Android3+1 retained without rerun absent new concern. "
    "After nativePASS use ORIGINAL two different-family reviewer sessions SERIALly for bounded "
    "dependent visuals, not new blind initials. Preserve original aef958a3 blind reports, Claude52 "
    "internal overlaps/noncompliance and bounded confirmation limits; strict original process "
    "contract not accepted. Then latestmain normal nonrewriting integration/allcombined "
    "source-baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/original "
    "18000entries42MiBcompressed80MiBinflated56MiBretained budgets/normal signing/ownerfastforward/"
    "publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 "
    "BEFOREdelivery or058. Actual permission denial/signing wait: preserve exact command/error, "
    "report/yield; no retry/workaround. No056rerun/058/secondrunner/concurrentheavywork/"
    "supervisor changes. Preserve FULL live history. Published83/1228,1145remaining; compatible"
    "Androidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding."
)


def verify_artifacts(record):
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


if sys.argv[1:] == ["refresh-archive"]:
    assert git("rev-parse", "HEAD") == HEAD
    preparation_path = SOURCES / "batch-057-native-preparation.json"
    preparation = load(preparation_path)
    record_path = SOURCES / "execution-335.json"
    record = load(record_path)
    prior = ROOT / preparation["reusedAcceptedHarness"]
    fixture = Path(preparation["fixture"])
    assert sha(prior) == preparation["reusedAcceptedHarnessSha256"]
    assert sha(fixture) == preparation["fixtureSha256"]
    diff_path = ROOT / preparation["fixtureDiff"]
    diff_path.write_text("".join(difflib.unified_diff(
        prior.read_text(encoding="utf-8").splitlines(keepends=True),
        fixture.read_text(encoding="utf-8").splitlines(keepends=True),
        fromfile=prior.relative_to(ROOT).as_posix(), tofile=fixture.relative_to(ROOT).as_posix(),
        n=0)), encoding="utf-8")
    for name in ("prepare-335-native.py", "finish-335.py"):
        shutil.copyfile(CONTROL / name, FOLDER / "preparation-receipts" / name)
    correction = (
        "Initial staged diff --check rejected whitespace-only CONTEXT lines in the standard "
        "unified-diff evidence before git commit/signing was invoked. Regenerated the same "
        "fixture diff with zero context; no fixture/archive/APK/runtime change, test rerun "
        "or signing retry. Generator and preparation receipts updated consistently."
    )
    preparation["fixtureDiffSha256"] = sha(diff_path)
    preparation["evidenceArchivalCorrection"] = correction
    save(preparation_path, preparation)
    record["evidenceArchivalCorrection"] = correction
    record["preparationSha256"] = sha(preparation_path)
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        item.update(bytes=path.stat().st_size, sha256=sha(path))
    verify_artifacts(record)
    save(record_path, record)
    print("Zero-context diff evidence and all dependent hashes refreshed; fixture/APK unchanged.")
    sys.exit(0)


if sys.argv[1:] == ["checkpoint"]:
    record = load(SOURCES / "execution-335.json")
    verify_artifacts(record)
    saved_head = git("rev-parse", "HEAD")
    assert saved_head != HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 334
    checkpoint = {
        "schemaVersion": 1, "execution": 335, "batch": "057",
        "status": record["status"], "record": "docs/n1-sources/execution-335.json",
        "savedCommit": saved_head, "signature": "G",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": record["scope"], "compilation": record["compilation"],
        "staticSelectors": 54, "articleCaptureSteps": 32,
        "contentVersion": record["contentVersion"],
        "nativeExecuted": False, "nativeAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "nextAction": next_action,
        "publishedAdditions": 83, "remainingAdditions": 1145,
    }
    progress["checkpoint"] = 335
    progress["status"] = "continue"
    progress["stage"] = "batch-057-native-compiled-pending-execution"
    progress["blocker"] = None
    progress["nextAction"] = next_action
    progress["execution335StartingState"]["status"] = "completed-bounded-native-preparation-checkpoint"
    progress["execution335CoordinatorCheckpoint"] = checkpoint
    progress["batch057NativePreparationCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", progress)
    save(CONTROL / "execution-335-checkpoint.json", checkpoint)
    body = (
        f"Batch **057 / 企**: native fixture prepared and compiled, saved in normally signed "
        f"local checkpoint `{saved_head}` (execution335). **Not published; native execution is next.**\n\n"
        "The exact full `d9712bf9` Git archive preserves all **8,300 runtime hashes**, "
        "**8,322 ZIP entries**, and the existing byte budgets; manifest remains "
        "`47f11f7f539a1d55` (1,069 kanji / 5,028 words / 89 N1 cards). "
        "The compiled APK contains both new test classes and that exact archive. "
        "54 article selectors and 32 article capture steps were statically audited, including "
        "both support articles, reciprocal links, curation, six-stroke drawing and System Back. "
        "28 glyph / eight complete-word raster probes are prepared, not executed. "
        "The three-character word bitmap uses measured width; old fixtures remain unchanged.\n\n"
        "Compilation succeeded (59s; one worker, no parallel heavy work). Temporary Android "
        "source/asset removed and dedicated worktrees clean. Accepted execution334 Android "
        "3+1 results retained without rerun. Original review/process limitations remain explicit. "
        "Next: fresh device/5580–5581 ownership check, supported native execution requiring "
        "both terminal case0 results and direct PNG inspection, then serial original-session "
        "visual confirmations and combined-main publication gates. **83/1,228 additions "
        "published; 1,145 remain.** No new runtime delivery, phone/general-release acceptance "
        "or whole-project completion claimed. Compatible Android `f9b59a2` or later required."
    )
    (CONTROL / "execution-335-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps({"checkpoint": 335, "savedCommit": saved_head,
                      "signature": "G", "status": "continue",
                      "nextGate": "same057-native-execution"}, indent=2))
    sys.exit(0)

assert not sys.argv[1:]
assert git("rev-parse", "HEAD") == HEAD
assert not git("diff", "--name-only")
assert not git("status", "--porcelain", cwd=ANDROID)
preparation = load(CONTROL / "batch-057-native-fixture-verification.json")
fixture = Path(preparation["fixture"])
assert sha(fixture) == preparation["fixtureSha256"]
assert sha(Path(preparation["archive"])) == preparation["archiveSha256"]
apk = CONTROL / "artifacts" / "n1-batch-057-native-test.apk"
with zipfile.ZipFile(apk) as package:
    asset = package.read("assets/n1-batch-057-d9712bf9-envelope.zip")
    assert hashlib.sha256(asset).hexdigest() == preparation["archiveSha256"]
    dex = [package.read(name) for name in package.namelist()
           if name.startswith("classes") and name.endswith(".dex")]
    for kind in ("Glyph", "Article"):
        current = f"Lio/github/stopcran/kanji/ui/N1Batch057{kind}Test;".encode()
        assert any(current in blob for blob in dex), current
        for prefix in ("N1Batch056", "N1Batch056Retry1", "N1Batch056Retry2"):
            obsolete = f"Lio/github/stopcran/kanji/ui/{prefix}{kind}Test;".encode()
            assert all(obsolete not in blob for blob in dex), obsolete
    for method in (
        "planningLookalikesAndSupportWordsAcrossFourProductionFamilies",
        "fullSingleImportOfflinePlanningArticlesMeaningBothCuratedReadingsDrawingAndSystemBack",
    ):
        assert any(method.encode() in blob for blob in dex), method
raw_log = CONTROL / "logs" / "execution-335-native-compile.txt"
compile_text = raw_log.read_text(encoding="utf-8-sig")
assert "BUILD SUCCESSFUL in 59s" in compile_text
assert "56 actionable tasks: 9 executed, 47 up-to-date" in compile_text
assert (CONTROL / "logs" / "execution-335-native-compile-exit.txt").read_text().strip() == "0"
archived_log = FOLDER / "compile.txt"
assert not archived_log.exists()
archived_log.write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n",
                        encoding="utf-8")
receipts = FOLDER / "preparation-receipts"
receipts.mkdir()
for name in ("prepare-335-native.py", "run-335-native-compile.ps1", "finish-335.py"):
    shutil.copyfile(CONTROL / name, receipts / name)
for relative in (
    r"app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch057NativeTest.kt",
    r"app\src\androidTest\assets\n1-batch-057-d9712bf9-envelope.zip",
):
    assert not (ANDROID / relative).exists()
checks = []
for name, expected in (("validate", "0 error(s)"), ("manifest", "version 47f11f7f539a1d55")):
    path = CONTROL / "logs" / f"execution-335-{name}.txt"
    assert expected in path.read_text(encoding="utf-8-sig")
    checks.append({"check": name, "exitCode": 0, "log": str(path), "sha256": sha(path)})
assert len(preparation["staticMarkdownSelectors"]) == 54
assert preparation["captureSteps"] == 32
compilation = {
    "status": "compiled-not-executed", "exitCode": 0,
    "result": "BUILD SUCCESSFUL in59s;56 tasks:9 executed,47 up-to-date",
    "log": str(archived_log.relative_to(ROOT)), "logSha256": sha(archived_log),
    "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
    "normalization": "Archive UTF-8 LF/trailing-whitespace normalization only; complete raw log retained.",
    "launcher": str(receipts.relative_to(ROOT) / "run-335-native-compile.ps1"),
    "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
    "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
    "packagedExactFullArchiveVerified": True,
    "bothBatch057ClassDescriptorsAndMethodsPresent": True,
    "oldBatch056ClassDescriptorsAbsent": True,
    "temporaryAndroidSourceAndAssetRemoved": True, "androidWhollyClean": True,
    "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
    "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
    "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
}
preparation["status"] = "native-compiled-pending-execution"
preparation["compilation"] = compilation
preparation["checks"] = checks
preparation["nextAction"] = next_action
preparation_path = SOURCES / "batch-057-native-preparation.json"
save(preparation_path, preparation)
artifact_paths = sorted(path for path in FOLDER.rglob("*") if path.is_file()) + [preparation_path]
record = {
    "schemaVersion": 1, "execution": 335, "batch": "057",
    "status": "native-compiled-pending-execution", "startingHead": HEAD,
    "scope": "SAME057 exact-full-archive supported-native fixture preparation, serial compilation and signed durable checkpoint only. No native launch, reviewer, runtime publication,058 or second runner.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
    "preparation": str(preparation_path.relative_to(ROOT)),
    "preparationSha256": sha(preparation_path),
    "contentVersion": preparation["contentVersion"],
    "fixture": preparation["fixture"], "fixtureSha256": preparation["fixtureSha256"],
    "archive": preparation["archive"], "archiveSha256": preparation["archiveSha256"],
    "compilation": compilation, "checks": checks,
    "artifacts": [{"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                   "sha256": sha(path)} for path in artifact_paths],
    "selectorAudit": {
        "completeArticleSelectors": 54, "articleCaptureSteps": 32,
        "method": "All article-route show/await/section/inline calls classified against three complete current articles. Static Markdown subset projection checked against actual production Markdown parser, not a native-tree or visibility claim.",
        "originalHarness": preparation["reusedAcceptedHarness"],
        "originalHarnessSha256": preparation["reusedAcceptedHarnessSha256"],
    },
    "accepted334AndroidRetainedWithoutRerun": True,
    "originalInitialReportHashesUnchanged": preparation["originalInitialReportHashesUnchanged"],
    "precompileInspectionCorrection": preparation["precompileInspectionCorrection"],
    "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
    "independentVisualAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
    "publishedAdditions": 83, "remainingAdditions": 1145,
    "nextAction": next_action, "limits": preparation["limits"],
}
verify_artifacts(record)
save(SOURCES / "execution-335.json", record)
batch_path = SOURCES / "batch-057-progress.json"
batch = load(batch_path)
batch["status"] = record["status"]
batch["nextAction"] = next_action
batch["nativePreparation"] = "batch-057-native-preparation.json"
batch["execution335Record"] = "execution-335.json"
save(batch_path, batch)
print(json.dumps({"status": record["status"], "compilation": compilation,
                  "archivedArtifacts": len(record["artifacts"]), "checks": checks}, indent=2))
