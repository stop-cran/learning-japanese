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
LOG = CONTROL / "logs" / "4142c13f-de80-456f-93b8-d96894d3a217"
PROGRESS = CONTROL / "progress.json"
BASELINE = LOG / "progress-before-594.json"
CONTENT_HEAD = "29a533800ed0d45e6269991d4a19e3b134057d6a"
ANDROID_HEAD = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PREFIX = "batch-085-android-594-"
NEXT_ACTION = (
    "SAME085 bounded native/visual acceptance on textually closed teaching a7512a5e plus "
    "review-confirmed Q1 direct exclusion at 29a53380, qualified TESTONLY Android1c1b7bf4 "
    "atop unchanged productionf9b59a2. Execution594 fresh RealContentTest THREE and RareHanTest "
    "ONE passed, zero skips. Inspect live device/port ownership immediately before an owned "
    "read-only API35 N3_Acceptance_20261029 emulator with approved hostGPU/Vulkan-disabled flags, "
    "2048MiB/two cores and explicit serial; do not interfere with shared devices. Preserve old "
    "fixtures and create bounded retry evidence. Full git archive through production ContentSync "
    "ONCE; assert actual imported counts/contentVersion/problems/acceptedRoom metadata. Inspect "
    "all37 actualHan across four production font families/system fallback, especially U+51AB/U+96B9; "
    "cmap absence is not glyph failure. Exercise N1 selection, meaning, actual curated reading "
    "keys \u304e\u3087\u3046/\u3053\u308b (selected \u3053.\u3089\u3059 shares the \u3053\u308b stem, "
    "not independent queued mastery),16stroke drawing, all articles/four reciprocal pairs/eight "
    "directions, SystemBack/offline routes and terminal per-case0. No reduced archive, import "
    "bypass, guest/app heap or archive guard increase, production app change or086. "
    "Parent19008 owns runner.lock throughout child lifetime: NOchild acquisition/delete/unlock. "
    "Keep exact signed-head/checkpoint/wholly-clean-worktree/live-parent-ancestry checks; "
    "preserve/report/yield actual new denial, signing hang or uncertain ownership. "
    "All original source/baseline/link/readings/two-family review limitations and Q1resolved/"
    "other optional dispositions preserved. Later current-main normal merge, surgical reconciliation/"
    "changed-teaching independent review, combined checks, normal signing, owner fast-forward push, "
    "terminal CI, EVERY immutable public ZIP runtime hash, original18000entries/42MiBcompressed/"
    "80MiBinflated/56MiBretained/perfile-media-safe-path guards and verified owner issue remain. "
    "Published111/1228,1117remaining unchanged; physicalphone/generalrelease/whole-set outstanding; "
    "project incomplete. No086."
)


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value, ensure_ascii=True):
    path.write_text(json.dumps(value, ensure_ascii=ensure_ascii, indent=2) + "\n", encoding="utf-8")


def check_heads(content_head=CONTENT_HEAD):
    for root, expected in ((CONTENT, content_head), (ANDROID, ANDROID_HEAD)):
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain"), str(root)


def start():
    check_heads()
    assert not BASELINE.exists(), "Existing start receipt: resume, do not overwrite."
    original = json.loads(PROGRESS.read_text(encoding="utf-8-sig"))
    assert original["checkpoint"] == 593 and original["batch"] == "085"
    assert original["stage"] == "textually-review-closed-awaiting-fresh-android"
    role_path = CONTROL / "batch-085-android-594-runner-role.json"
    role = json.loads(role_path.read_text(encoding="utf-8-sig"))
    assert any(p["pid"] == 19008 and r"n1-kanji-workspace\control\runner.ps1" in p["command"] for p in role)
    request_path = LOG / "request.txt"
    request = request_path.read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert parsed["checkpoint"] == 593
    save(BASELINE, original)
    state = copy.deepcopy(original)
    state["stage"] = "fresh-host-android-checks-running"
    state["execution594StartingState"] = {
        "execution": 594, "batch": "085", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": CONTENT_HEAD, "androidHead": ANDROID_HEAD,
        "freshOriginMain": git(CONTENT, "rev-parse", "origin/main"),
        "scope": "SAME085 fresh RealContentTest3/RareHanTest1, signed LOCAL evidence; yield before native/reviewer/integration/publication/086.",
        "request": {"sha256": sha(request_path), "bytes": request_path.stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "checkpointStringsTraversed": 47611,
                    "limits": "Entire request loaded, checkpoint decoded and nested strings traversed. Operative contract, complete issue and final593 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerRoleReceipt": str(role_path),
        "runnerLockRole": "Verified live parent19008 ancestry; child inherits launcher protection and does not acquire/delete/unlock runner.lock.",
        "artifactPathPreflight": "Approved workspace inputs, committed source packets and new reusable control helpers only; optional historical session helpers not accessed.",
        "actualNewPermissionDenials": [], "status": "fresh-host-android-checks-running",
    }
    save(PROGRESS, state)
    persisted = json.loads(PROGRESS.read_text(encoding="utf-8"))
    assert all(persisted[k] == v for k, v in original.items() if k != "stage")
    print("Starting state persisted; all original historical values preserved.")


def runtime_receipt():
    sys.path.insert(0, str(CONTENT / "tools"))
    from build_manifest import build_manifest
    path = CONTENT / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest == build_manifest(CONTENT), "Manifest not fresh."
    assert manifest["contentVersion"] == "0c514711ae8d3212"
    required = {name: digest for value in manifest.values() if isinstance(value, dict)
                for name, digest in value.items()}
    assert len(required) == 8413
    for name, digest in required.items():
        payload = CONTENT.joinpath(*name.split("/")).read_bytes()
        normalized = payload if name.startswith(("images/", "audio/", "task-audio/", "task-images/")) else payload.replace(b"\r\n", b"\n")
        assert hashlib.sha256(normalized).hexdigest() == digest, name
    committed = subprocess.check_output(["git", "-C", str(CONTENT), "show", f"{CONTENT_HEAD}:manifest.json"])
    assert path.read_bytes().replace(b"\r\n", b"\n") == committed.replace(b"\r\n", b"\n")
    return {"runtimePayloadHashesVerified": len(required), "manifestSha256": sha(path),
            "contentVersion": manifest["contentVersion"], "manifestFreshAndUnchanged": True}


def collect():
    check_heads()
    assert (LOG / "android-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    progress = json.loads(PROGRESS.read_text(encoding="utf-8"))
    assert progress["checkpoint"] == 593 and progress["stage"] == "fresh-host-android-checks-running"
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
    for module, relative, count, names in reports:
        source = ANDROID / module / Path(*relative.split("/"))
        root = ET.parse(source).getroot()
        assert int(root.attrib["tests"]) == count
        assert all(int(root.attrib[k]) == 0 for k in ("skipped", "failures", "errors"))
        assert {case.attrib["name"] for case in root.findall("testcase")} == names
        assert not any(case.find(tag) is not None for case in root.findall("testcase")
                       for tag in ("skipped", "failure", "error"))
        timestamp = datetime.fromisoformat(root.attrib["timestamp"])
        assert start_time <= timestamp <= end_time and source.stat().st_mtime >= start_time.timestamp(), "Stale XML."
        target = archive / f"{PREFIX}{module}.xml"
        shutil.copyfile(source, target)
        tests.append({"module": module, "class": root.attrib["name"], "tests": count, "skipped": 0,
                      "failures": 0, "errors": 0, "timestamp": root.attrib["timestamp"],
                      "caseNames": sorted(names), "archive": target.relative_to(CONTENT).as_posix(), "sha256": sha(target)})
    assert "BUILD SUCCESSFUL" in (LOG / "android.txt").read_text(encoding="utf-8-sig")
    provenance = []
    for relative in (
        "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    ):
        path = ANDROID.joinpath(*relative.split("/"))
        target = archive / f"{PREFIX}{path.name}.txt"
        shutil.copyfile(path, target)
        committed = subprocess.check_output(["git", "-C", str(ANDROID), "show", f"{ANDROID_HEAD}:{relative}"])
        assert path.read_bytes().replace(b"\r\n", b"\n") == committed.replace(b"\r\n", b"\n")
        provenance.append({"path": relative, "sha256": sha(path), "archive": target.relative_to(CONTENT).as_posix(),
                           "exactSignedHeadSourceVerified": True})
    for module in ("core", "app"):
        assert (ANDROID / module / ".." / ".." / "learning-japanese").resolve() == CONTENT
    subprocess.run(["git", "-C", str(ANDROID), "merge-base", "--is-ancestor", PRODUCTION_HEAD, ANDROID_HEAD], check=True)
    changed = git(ANDROID, "diff", "--name-only", PRODUCTION_HEAD, ANDROID_HEAD).splitlines()
    assert all(name.startswith(("core/src/test/", "docs/", ".github/")) for name in changed)
    artifacts = {}
    for name, source in (
        ("gradle-log.txt", LOG / "android.txt"), ("gradle-arguments.json", LOG / "android-arguments.json"),
        ("runner-role.json", LOG / "android-runner-role.json"),
        ("host-heap.init.gradle.txt", CONTROL / "batch-065-host-integration-heap.init.gradle"),
        ("wrapper.ps1.txt", CONTROL / "run-594-android.ps1"), ("recipe.py", Path(__file__)),
        ("content-gitattributes.txt", CONTENT / ".gitattributes"),
    ):
        target = archive / f"{PREFIX}{name}"
        shutil.copyfile(source, target)
        artifacts[name] = {"archive": target.relative_to(CONTENT).as_posix(), "sha256": sha(target)}
    evidence = {
        "schemaVersion": 1, "execution": 594, "batch": "085", "status": "fresh-android-passed-awaiting-native",
        "contentTestedHead": CONTENT_HEAD, "teachingSnapshot": "a7512a5e6ce6d04b271099de834e431436363c3d",
        "reviewConfirmedCorrectionHead": CONTENT_HEAD, "androidTestedHead": ANDROID_HEAD,
        "unchangedProductionAndroidHead": PRODUCTION_HEAD,
        "androidQualification": "Test-only publishable fixture adjustment, not latest app main or a production app change.",
        "testOnlyDeltaPaths": changed, "sourceProvenance": provenance,
        "actualResolvedContentRoot": str(CONTENT),
        "sourcePathResolution": "Both module working directories resolve ../../learning-japanese to THIS dedicated content tree; full publishable manifest fixture, not partial/static/copied content.",
        "freshRun": True, "gradleExitCode": 0, "startedAt": start_time.isoformat(), "completedAt": end_time.isoformat(),
        "tests": tests, "totalTests": 4, "totalSkipped": 0,
        "gradle": {"oneWorker": True, "noParallel": True, "rerunTasks": True, "kotlinCompiler": "in-process",
                   "coreTestHostHeap": "2g; existing approved host-only init script, no guest/app heap change",
                   "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
                   "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk"},
        "artifacts": artifacts, "runtime": runtime_receipt(),
        "request": progress["execution594StartingState"]["request"],
        "runnerLockRole": progress["execution594StartingState"]["runnerLockRole"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False, "newNativeOrPhoneClaimed": False,
        "textualReviewClosed": True, "textualReconciliation": "docs/n1-reviews/batch-085-reconciliation.json",
        "reconciliationSha256": sha(CONTENT / "docs" / "n1-reviews" / "batch-085-reconciliation.json"),
        "publishedAdditions": 111, "remainingAdditions": 1117, "lastPublishedCommit": progress["lastPublishedCommit"],
        "freshOriginMain": git(CONTENT, "rev-parse", "origin/main"),
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT_ACTION,
        "limits": [
            "Four fresh non-skipped JVM tests only, not native glyph legibility/system fallback or phone acceptance.",
            "RealContentTest parses full publishable content and mixed/legacy archives; not production Room ContentSync/native route acceptance.",
            "37 Han across four fonts, especially U+51AB/U+96B9, 16-stroke drawing, curated reading/native routes/Back/offline and terminal case0 remain pending.",
            "Original two-family textual evidence/limits and Q1resolved/other optional dispositions preserved; no fresh independent reviewer.",
            "Current-main integration, combined checks, signing, owner push, CI, every immutable ZIP runtime hash and original budgets remain required.",
            "No runtime push, native/phone/general-release/whole-set acceptance or086; published111/1228,1117remaining unchanged.",
        ],
    }
    save(archive / "execution-594.json", evidence)
    packet_path = archive / "batch-085-progress.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    packet.update(status=evidence["status"], nextAction=NEXT_ACTION)
    packet["androidAcceptance"] = {
        "execution": 594, "contentTestedHead": CONTENT_HEAD, "androidTestedHead": ANDROID_HEAD,
        "totalTests": 4, "totalSkipped": 0, "evidence": "docs/n1-sources/execution-594.json",
        "status": "passed", "nativeAcceptance": "pending", "runtimePublished": False,
    }
    save(packet_path, packet, ensure_ascii=False)
    print(json.dumps({"tests": tests, "runtime": evidence["runtime"]}, indent=2))


def finalize():
    head = git(CONTENT, "rev-parse", "HEAD")
    assert head != CONTENT_HEAD
    check_heads(head)
    assert git(CONTENT, "rev-parse", "HEAD^") == CONTENT_HEAD
    assert not git(CONTENT, "diff", "--name-only", CONTENT_HEAD, head, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")
    evidence = json.loads((CONTENT / "docs" / "n1-sources" / "execution-594.json").read_text(encoding="utf-8"))
    assert runtime_receipt() == evidence["runtime"]
    for record in evidence["tests"] + evidence["sourceProvenance"] + list(evidence["artifacts"].values()):
        assert sha(CONTENT.joinpath(*record["archive"].split("/"))) == record["sha256"]
    receipt_path = CONTROL / "batch-085-android-594-issue-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    body = (CONTROL / "batch-085-android-594-issue-body.txt").read_text(encoding="utf-8-sig")
    assert receipt["user"]["login"] == "stop-cran" and head in receipt["body"]
    assert receipt["body"].replace("\r\n", "\n").strip() == body.replace("\r\n", "\n").strip()
    original = json.loads(BASELINE.read_text(encoding="utf-8"))
    state = json.loads(PROGRESS.read_text(encoding="utf-8"))
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in original.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 594, "checkpoint": 594, "batch": "085",
        "savedCommit": head, "signature": "G", "status": "continue", "stage": evidence["status"],
        "evidence": "docs/n1-sources/execution-594.json", "contentTestedHead": CONTENT_HEAD,
        "androidTestedHead": ANDROID_HEAD, "teachingSnapshot": evidence["teachingSnapshot"],
        "totalTests": 4, "totalSkipped": 0, "testCases": evidence["tests"], "runtime": evidence["runtime"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "newNativeOrPhoneClaimed": False, "textualReviewClosed": True,
        "reviewClosed": [], "published": [], "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "runnerLockRole": evidence["runnerLockRole"], "publishedAdditions": 111, "remainingAdditions": 1117,
        "lastPublishedCommit": original["lastPublishedCommit"], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT_ACTION, "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(receipt_path), "originalRootKeysCompared": len(original),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "verifiedAt": datetime.now(timezone.utc).isoformat(),
    }
    state.update(checkpoint=594, status="continue", stage=evidence["status"], nextAction=NEXT_ACTION, blocker=None)
    state["execution594StartingState"]["status"] = "signed-local-android-checkpoint-complete"
    state["execution594CoordinatorCheckpoint"] = checkpoint
    state["batch085AndroidCheckpoint"] = copy.deepcopy(checkpoint)
    save(PROGRESS, state)
    persisted = json.loads(PROGRESS.read_text(encoding="utf-8"))
    assert all(persisted[k] == v for k, v in original.items() if k not in allowed)
    assert persisted["execution594CoordinatorCheckpoint"] == checkpoint
    save(LOG / "batch-085-android-checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": 594, "savedCommit": head, "status": "continue", "stage": evidence["status"],
                      "tests": 4, "skipped": 0, "allHistoricalValuesPreserved": True,
                      "issueUpdate": receipt["html_url"]}, indent=2))


if __name__ == "__main__":
    actions = {"start": start, "collect": collect, "finalize": finalize}
    assert len(sys.argv) == 2 and sys.argv[1] in actions
    actions[sys.argv[1]]()
