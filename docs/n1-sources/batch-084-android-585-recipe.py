import copy
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CONTROL = Path(__file__).resolve().parent
CONTENT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOG = CONTROL / "logs" / "99dccb26-34f7-4d00-8f28-9487f0a6dcee"
PROGRESS = CONTROL / "progress.json"
BASELINE = LOG / "progress-before-585.json"
CONTENT_HEAD = "f218a36a42f98811284e44c458b1af4743339b80"
ANDROID_HEAD = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
NEXT_ACTION = (
    "SAME084 bounded native/visual acceptance on the unchanged textually closed teaching030b144a "
    "and qualified TESTONLY Android1c1b7bf4 atop unchanged productionf9. Fresh RealContentTest3/"
    "RareHanTest1 passed with zero skips in execution585. Inspect device/port ownership immediately "
    "before launching an owned read-only API35 N3_Acceptance_20261029 emulator with approved hostGPU/"
    "Vulkan-disabled flags, 2048MiB/two cores and explicit serial; do not interfere with shared devices. "
    "Preserve original fixtures and create bounded retry evidence; full git archive through production "
    "ContentSync ONCE, assert actual imported counts/contentVersion/problems/acceptedRoom metadata. "
    "Inspect all28 actualHan across four font families, especially凜/凛/冫/稟; cmap absence is not glyph "
    "failure. Exercise N1 selection, meaning, soleりん/kun[], 15-stroke drawing, article, SystemBack/"
    "offline routes and obtain terminal per-case0; stop only the owned emulator. No heap/archive guard "
    "increase, reduced archive, import bypass, app production change or085. Parent19008 owns runner.lock; "
    "no child acquisition/delete/unlock. Verify exact signed heads/clean worktrees/checkpoint/parent "
    "ancestry; preserve/report/yield actual new denial, signing hang or uncertain ownership. "
    "C1optional/C2withdrawn/C3defaultresolved-largerpoolunverified preserved. Later fresh latest-main "
    "normal merge, surgical reconciliation/substantive teaching review, all combined checks, normal "
    "signing, owner fast-forward, terminal CI, EVERY immutable public ZIP runtime hash, original "
    "18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safe-path guards and verified "
    "owner issue remain required. Published110/1228,1118remaining unchanged; physical phone, general "
    "release and whole-set acceptance outstanding; project incomplete."
)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], encoding="utf-8").strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value, ensure_ascii=False):
    path.write_text(json.dumps(value, ensure_ascii=ensure_ascii, indent=2) + "\n", encoding="utf-8")


def check_heads(content_head=CONTENT_HEAD):
    for root, expected in ((CONTENT, content_head), (ANDROID, ANDROID_HEAD)):
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain"), str(root)


def request_receipt():
    path = LOG / "request.txt"
    text = path.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    strings = 0

    def traverse(value):
        nonlocal strings
        if isinstance(value, str):
            strings += 1
        elif isinstance(value, dict):
            for key, item in value.items():
                traverse(key)
                traverse(item)
        elif isinstance(value, list):
            for item in value:
                traverse(item)

    traverse(checkpoint)
    return {
        "sha256": sha(path), "bytes": path.stat().st_size,
        "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "checkpointStringsTraversed": strings,
        "limits": "Entire request loaded and checkpoint traversed; operative contract, complete approved issue and final584 inspected directly. Historical middle not freshly semantically re-reviewed.",
    }


def start():
    check_heads()
    assert not BASELINE.exists(), "Starting receipt already exists; resume rather than overwrite."
    original = json.loads(PROGRESS.read_text(encoding="utf-8-sig"))
    assert original["checkpoint"] == 584 and original["batch"] == "084"
    assert original["stage"] == "textually-review-closed-awaiting-fresh-android"
    save(BASELINE, original)
    state = copy.deepcopy(original)
    state["stage"] = "fresh-host-android-checks-running"
    state["execution585StartingState"] = {
        "execution": 585, "batch": "084", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": CONTENT_HEAD, "androidHead": ANDROID_HEAD,
        "freshOriginMain": git(CONTENT, "rev-parse", "origin/main"),
        "scope": "SAME084 fresh RealContentTest3/RareHanTest1; normally signed LOCAL evidence only, yield before native/integration/publication/085.",
        "request": request_receipt(),
        "runnerRoleReceipt": str(CONTROL / "batch-084-android-585-runner-role.json"),
        "runnerLockRole": "Verified live parent19008 in child ancestry; inherited launcher protection. No lock acquisition/deletion/unlock.",
        "artifactPathPreflight": "Approved control helpers and committed source packets only; no optional historical session helper accessed.",
        "actualNewPermissionDenials": [],
        "status": "fresh-host-android-checks-running",
    }
    save(PROGRESS, state)
    persisted = json.loads(PROGRESS.read_text(encoding="utf-8"))
    assert all(persisted[k] == v for k, v in original.items() if k != "stage")
    print("Starting checkpoint recorded with every historical value preserved.")


def runtime_receipt():
    sys.path.insert(0, str(CONTENT / "tools"))
    from build_manifest import build_manifest
    path = CONTENT / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest == build_manifest(CONTENT), "Manifest not fresh."
    assert manifest["contentVersion"] == "74b87b47347b78c1"
    required = {name: digest for value in manifest.values() if isinstance(value, dict)
                for name, digest in value.items()}
    assert len(required) == 8379
    for name, digest in required.items():
        payload = CONTENT.joinpath(*name.split("/")).read_bytes()
        normalized = payload if name.startswith(("images/", "audio/", "task-audio/", "task-images/")) else payload.replace(b"\r\n", b"\n")
        assert hashlib.sha256(normalized).hexdigest() == digest, name
    baseline_manifest = subprocess.check_output(["git", "-C", str(CONTENT), "show", f"{CONTENT_HEAD}:manifest.json"])
    assert path.read_bytes().replace(b"\r\n", b"\n") == baseline_manifest.replace(b"\r\n", b"\n")
    return {"runtimePayloadHashesVerified": len(required), "manifestSha256": sha(path),
            "contentVersion": manifest["contentVersion"], "manifestFreshAndUnchanged": True}


def collect():
    check_heads()
    assert (LOG / "android-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    progress = json.loads(PROGRESS.read_text(encoding="utf-8"))
    assert progress["checkpoint"] == 584 and progress["stage"] == "fresh-host-android-checks-running"
    start_time = datetime.fromisoformat((LOG / "android-start.txt").read_text(encoding="utf-8-sig").strip())
    end_time = datetime.fromisoformat((LOG / "android-end.txt").read_text(encoding="utf-8-sig").strip())
    archive = CONTENT / "docs" / "n1-sources"
    tests = []
    reports = (
        ("core", "build/test-results/test/TEST-io.github.stopcran.kanji.core.RealContentTest.xml", 3,
         {"hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
          "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent",
          "parsesRealContentRepoWhenPresent"}),
        ("app", "build/test-results/testDebugUnitTest/TEST-io.github.stopcran.kanji.core.RareHanTest.xml", 1,
         {"contentRareCharactersAreCoveredByBundledFont"}),
    )
    for module, relative, count, expected_names in reports:
        source = ANDROID / module / Path(*relative.split("/"))
        root = ET.parse(source).getroot()
        assert int(root.attrib["tests"]) == count
        assert all(int(root.attrib[key]) == 0 for key in ("skipped", "failures", "errors"))
        case_names = {case.attrib["name"] for case in root.findall("testcase")}
        assert case_names == expected_names
        assert not any(case.find(tag) is not None for case in root.findall("testcase")
                       for tag in ("skipped", "failure", "error"))
        timestamp = datetime.fromisoformat(root.attrib["timestamp"])
        assert start_time <= timestamp <= end_time, "Stale test XML."
        assert source.stat().st_mtime >= start_time.timestamp()
        target = archive / f"batch-084-android-{module}-585.xml"
        shutil.copyfile(source, target)
        tests.append({"module": module, "class": root.attrib["name"], "tests": count,
                      "skipped": 0, "failures": 0, "errors": 0,
                      "timestamp": root.attrib["timestamp"], "caseNames": sorted(case_names),
                      "archive": target.relative_to(CONTENT).as_posix(), "sha256": sha(target)})
    assert "BUILD SUCCESSFUL" in (LOG / "android.txt").read_text(encoding="utf-8-sig")
    source_paths = (
        "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    )
    provenance = []
    for relative in source_paths:
        path = ANDROID.joinpath(*relative.split("/"))
        target = archive / f"batch-084-android-585-{path.name}.txt"
        shutil.copyfile(path, target)
        committed = subprocess.check_output(["git", "-C", str(ANDROID), "show", f"{ANDROID_HEAD}:{relative}"])
        assert path.read_bytes().replace(b"\r\n", b"\n") == committed.replace(b"\r\n", b"\n")
        provenance.append({"path": relative, "sha256": sha(path),
                           "archive": target.relative_to(CONTENT).as_posix(),
                           "exactSignedHeadSourceVerified": True})
    for module in ("core", "app"):
        assert (ANDROID / module / ".." / ".." / "learning-japanese").resolve() == CONTENT
    production_head = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    subprocess.run(["git", "-C", str(ANDROID), "merge-base", "--is-ancestor", production_head, ANDROID_HEAD], check=True)
    changed = git(ANDROID, "diff", "--name-only", production_head, ANDROID_HEAD).splitlines()
    assert all(name.startswith(("core/src/test/", "docs/", ".github/")) for name in changed)
    artifacts = {}
    for name, source in (
        ("gradle-log.txt", LOG / "android.txt"),
        ("gradle-arguments.json", LOG / "android-arguments.json"),
        ("runner-role.json", LOG / "android-runner-role.json"),
        ("host-heap.init.gradle.txt", CONTROL / "batch-065-host-integration-heap.init.gradle"),
        ("wrapper.ps1.txt", CONTROL / "run-585-android.ps1"),
        ("recipe.py", Path(__file__)),
        ("content-gitattributes.txt", CONTENT / ".gitattributes"),
    ):
        target = archive / f"batch-084-android-585-{name}"
        shutil.copyfile(source, target)
        artifacts[name] = {"archive": target.relative_to(CONTENT).as_posix(), "sha256": sha(target)}
    runtime = runtime_receipt()
    evidence = {
        "schemaVersion": 1, "execution": 585, "batch": "084",
        "status": "fresh-android-passed-awaiting-native",
        "contentTestedHead": CONTENT_HEAD, "teachingSnapshot": "030b144a6aeefc6fe77f76683219832db91bef4f",
        "androidTestedHead": ANDROID_HEAD, "unchangedProductionAndroidHead": production_head,
        "androidQualification": "Test-only publishable fixture adjustment, not latest app main or a production app change.",
        "testOnlyDeltaPaths": changed, "sourceProvenance": provenance,
        "actualResolvedContentRoot": str(CONTENT),
        "sourcePathResolution": "Both module working directories resolve ../../learning-japanese to THIS dedicated worktree; no copied/static/partial content fixture.",
        "freshRun": True, "gradleExitCode": 0,
        "startedAt": start_time.isoformat(), "completedAt": end_time.isoformat(),
        "tests": tests, "totalTests": 4, "totalSkipped": 0,
        "gradle": {"oneWorker": True, "noParallel": True, "rerunTasks": True,
                   "kotlinCompiler": "in-process", "coreTestHostHeap": "2g; existing approved host-only init script, no native/app heap changes",
                   "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
                   "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk"},
        "artifacts": artifacts, "runtime": runtime,
        "request": progress["execution585StartingState"]["request"],
        "runnerLockRole": "Live parent19008 verified in fresh wrapper ancestry; inherited protection, no child lock acquisition/delete/unlock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "newNativeOrPhoneClaimed": False, "textualReviewClosed": True,
        "textualReconciliation": "docs/n1-reviews/batch-084-reconciliation.json",
        "reconciliationSha256": sha(CONTENT / "docs" / "n1-reviews" / "batch-084-reconciliation.json"),
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": progress["lastPublishedCommit"],
        "freshOriginMain": git(CONTENT, "rev-parse", "origin/main"),
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT_ACTION,
        "limits": [
            "Fresh four-case JVM acceptance only; RareHan coverage is not native glyph legibility or fallback typeface identification.",
            "RealContentTest executes full publishable content parsing and mixed archive/legacy-reader assertions; not production Room ContentSync or native route acceptance.",
            "28 actual Han, especially凜/凛/冫/稟 across four font families, 15-stroke drawing, actual curated reading and full ContentSyncONCE/native routes/Back/offline/terminalcase0 remain pending.",
            "Textual030b144a unchanged; original C1optional/C2withdrawn/C3defaultresolved-largerpoolunverified and all original review/source/process/denial/OOM/phone limitations preserved.",
            "Fresh main106a36dd not integrated. All combined-tree/re-review/checks/signing/ownerpush/CI/everyimmutableZIPhash/originalbudgets/issue gates remain.",
            "No runtime publication, native/phone/general-release acceptance or085; published110/1228,1118remaining unchanged.",
        ],
    }
    save(archive / "execution-585.json", evidence)
    packet_path = archive / "batch-084-progress.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    packet["status"] = evidence["status"]
    packet["nextAction"] = NEXT_ACTION
    packet["androidAcceptance"] = {
        "execution": 585, "contentTestedHead": CONTENT_HEAD, "androidTestedHead": ANDROID_HEAD,
        "totalTests": 4, "totalSkipped": 0, "evidence": "docs/n1-sources/execution-585.json",
        "status": "passed", "nativeAcceptance": "pending", "runtimePublished": False,
    }
    save(packet_path, packet, ensure_ascii=True)
    print(json.dumps({"tests": tests, "runtime": runtime, "evidence": "docs/n1-sources/execution-585.json"}, ensure_ascii=False, indent=2))


def finalize():
    head = git(CONTENT, "rev-parse", "HEAD")
    assert head != CONTENT_HEAD
    check_heads(head)
    subprocess.run(["git", "-C", str(CONTENT), "merge-base", "--is-ancestor", CONTENT_HEAD, head], check=True)
    evidence = json.loads((CONTENT / "docs" / "n1-sources" / "execution-585.json").read_text(encoding="utf-8"))
    assert runtime_receipt() == evidence["runtime"]
    receipt_path = CONTROL / "batch-084-android-585-issue-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    body = (CONTROL / "batch-084-android-585-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").strip() == body.replace("\r\n", "\n").strip()
    assert head in receipt["body"]
    original = json.loads(BASELINE.read_text(encoding="utf-8"))
    state = json.loads(PROGRESS.read_text(encoding="utf-8"))
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in original.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 585, "checkpoint": 585, "batch": "084",
        "savedCommit": head, "signature": "G", "status": "continue",
        "stage": "fresh-android-passed-awaiting-native", "evidence": "docs/n1-sources/execution-585.json",
        "contentTestedHead": CONTENT_HEAD, "androidTestedHead": ANDROID_HEAD,
        "teachingSnapshot": evidence["teachingSnapshot"], "totalTests": 4, "totalSkipped": 0,
        "testCases": evidence["tests"], "runtime": evidence["runtime"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "newNativeOrPhoneClaimed": False,
        "textualReviewClosed": True, "reviewClosed": [], "published": [],
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "runnerLockRole": evidence["runnerLockRole"],
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT_ACTION, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "issueReceiptSha256": sha(receipt_path),
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "verifiedAt": datetime.now(timezone.utc).isoformat(),
    }
    state.update(checkpoint=585, status="continue", stage=checkpoint["stage"], nextAction=NEXT_ACTION, blocker=None)
    state["execution585StartingState"]["status"] = "signed-local-android-checkpoint-complete"
    state["execution585CoordinatorCheckpoint"] = checkpoint
    state["batch084AndroidCheckpoint"] = copy.deepcopy(checkpoint)
    state["batch084AndroidIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "receiptSha256": sha(receipt_path),
        "localSignedEvidenceCommit": head, "runtimePublished": False,
    }
    save(PROGRESS, state)
    persisted = json.loads(PROGRESS.read_text(encoding="utf-8"))
    assert all(persisted[k] == v for k, v in original.items() if k not in allowed)
    assert persisted["execution585CoordinatorCheckpoint"] == checkpoint
    save(LOG / "batch-084-android-checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": 585, "savedCommit": head, "status": "continue",
                      "stage": checkpoint["stage"], "tests": 4, "skipped": 0,
                      "allHistoricalValuesPreserved": True, "issueUpdate": receipt["html_url"]}, indent=2))


if __name__ == "__main__":
    actions = {"start": start, "collect": collect, "finalize": finalize}
    assert len(sys.argv) == 2 and sys.argv[1] in actions
    actions[sys.argv[1]]()
