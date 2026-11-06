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
C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "804f9a11-6513-4c96-9998-4f8dafd1314f"
S = R / "docs" / "n1-sources"
HEAD = "f201260b35361afefeffa05c5df66bfeb3209395"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
SNAPSHOT = "f6391022356073dd3e53437be30885f9a09857d9"
PREFIX = "batch-087-android-612-"
NEXT = (
    "SAME087 bounded native/visual acceptance on unchanged textually closed teaching "
    "f6391022356073dd3e53437be30885f9a09857d9. Execution612 fresh sibling "
    "RealContentTest THREE and RareHanTest ONE passed, zero skips. Qualified TESTONLY "
    "Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d atop unchanged productionf9b59a2 "
    "is not latest app main. Inspect actual live device/port ownership before an owned "
    "read-only API35 N3_Acceptance_20261029 emulator; approved hostGPU/Vulkan-disabled "
    "flags, 2048MiB/two cores, explicit serial, stop only owned helper. Preserve prior "
    "fixtures; full git archive through production ContentSync ONCE with actual counts/"
    "contentVersion/problems/acceptedRoom assertions and terminal per-case0. Inspect "
    "all21 scoped Han especially U+51E0 across four production font families/system "
    "fallback; cmap absence is not glyph failure. Exercise N1 selection, actual N1 "
    "fallback choices (N4 U+98A8 excluded; All pool differs), meaning, both queued "
    "kunkeys\u306a\u304e/\u306a\u3050, six-stroke drawing, all three new articles, "
    "SystemBack/offline routes, two mapped pairs/four link directions and seven direct "
    "word guards. Both rawkun entries/order retained; explicit on[]. Modern weather "
    "\u51ea\u3050 versus feelings\u548c\u3050/classical forms remain separate. Retain "
    "both original different-family review sessions for dependent visuals, no new "
    "blind credit. No reduced archive/import bypass/guest or app heap/guard increase, "
    "production app change,088 or runtime publication in next bounded gate. "
    "Parent19008 owns runner.lock throughout child lifetime: no child acquisition/"
    "delete/unlock. Keep exact signed-head/checkpoint/wholly-clean-worktree/live-parent "
    "ancestry checks; preserve/report/yield actual new denial, signing hang or uncertain "
    "ownership. Use approved control helpers/committed source packets/frozen workspace "
    "inputs, not optional historical session recipes. All original source/baseline/"
    "link/reading/twofamily/native/currentmain-normalmerge/changed-teaching-independent "
    "review/combinedchecks/normal-signing/owner-fastforward/terminalCI/EVERYimmutableZIP "
    "entryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/media/"
    "safepath/ownerissue gates remain. Published113/1228,1115remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding; project incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value, ensure_ascii=True):
    path.write_text(json.dumps(value, ensure_ascii=ensure_ascii, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def heads(content=HEAD):
    for root, expected in ((R, content), (A, ANDROID)):
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain"), str(root)


def persist(value):
    temporary = C / "progress.612.tmp"
    assert not temporary.exists()
    save(temporary, value)
    assert load(temporary) == value
    temporary.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    assert manifest["contentVersion"] == "eb3a9413cccd4f57"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                path = R.joinpath(*name.split("/"))
                digest = sha(path) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                } else sha256(path)
                assert digest == expected, name
                checked += 1
    assert checked == 8420
    rec = load(R / "docs" / "n1-reviews" / "batch-087-reconciliation.json")
    assert rec["textualReviewClosed"]
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == expected
    assert not git(R, "diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"runtimePayloadHashesVerified": checked, "manifestSha256": sha(R / "manifest.json"),
            "contentVersion": manifest["contentVersion"], "manifestFreshAndUnchanged": True}


def start():
    heads()
    baseline = L / "progress-before-612.json"
    assert not baseline.exists(), "Existing receipt; resume without overwriting."
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (
        611, "087", "continue", "textually-review-closed-awaiting-fresh-android")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert any(x["pid"] == 19008 and x["launcherCommandMatches"] for x in load(L / "android-runner-role.json"))
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["checkpoint"] == 611
    assert parsed["execution611FinalVerification"]["savedCommit"] == HEAD
    save(baseline, p)
    state = copy.deepcopy(p)
    state["stage"] = "fresh-host-android-checks-running"
    state["execution612StartingState"] = {
        "execution": 612, "batch": "087", "startingHead": HEAD, "androidHead": ANDROID,
        "startedAt": datetime.now(timezone.utc).isoformat(), "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "scope": "SAME087 four fresh JVM cases, signed LOCAL evidence and checkpoint only; no native/reviewer/publication/088.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(request),
                    "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire file loaded/JSON decoded; operative contract, complete approved issue and final611 inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry and exact runner session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "status": "fresh-host-android-checks-running", "actualNewPermissionDenials": [],
        "diagnostics": ["Initial request diagnostic hit console UnicodeEncodeError after full load/JSON parse; repeated using ASCII-safe output, no permission denial or changed input."],
    }
    persist(state)
    assert all(load(C / "progress.json")[k] == v for k, v in p.items() if k != "stage")
    print("Starting612 state saved with full historical values preserved.")


def collect():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["stage"]) == (611, "fresh-host-android-checks-running")
    assert (L / "android-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    start_time = datetime.fromisoformat((L / "android-start.txt").read_text(encoding="utf-8-sig").strip())
    end_time = datetime.fromisoformat((L / "android-end.txt").read_text(encoding="utf-8-sig").strip())
    tests = []
    for module, task, cls, names in (
        ("core", "test", "RealContentTest", {"parsesRealContentRepoWhenPresent",
         "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
         "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent"}),
        ("app", "testDebugUnitTest", "RareHanTest", {"contentRareCharactersAreCoveredByBundledFont"}),
    ):
        source = A / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{cls}.xml"
        xml = ET.parse(source).getroot()
        assert int(xml.attrib["tests"]) == len(names)
        assert all(int(xml.attrib[k]) == 0 for k in ("skipped", "failures", "errors"))
        assert {x.attrib["name"] for x in xml.findall("testcase")} == names
        assert not any(x.find(tag) is not None for x in xml.findall("testcase") for tag in ("skipped", "failure", "error"))
        assert start_time <= datetime.fromisoformat(xml.attrib["timestamp"]) <= end_time
        assert source.stat().st_mtime >= start_time.timestamp()
        target = S / f"{PREFIX}{module}.xml"
        shutil.copyfile(source, target)
        tests.append({"module": module, "class": xml.attrib["name"], "tests": len(names), "skipped": 0,
                      "failures": 0, "errors": 0, "timestamp": xml.attrib["timestamp"], "caseNames": sorted(names),
                      "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    assert "BUILD SUCCESSFUL" in (L / "android.txt").read_text(encoding="utf-8-sig")
    provenance = []
    for name in (
        "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    ):
        source = A.joinpath(*name.split("/"))
        committed = subprocess.check_output(["git", "-C", str(A), "show", f"{ANDROID}:{name}"])
        assert source.read_bytes().replace(b"\r\n", b"\n") == committed.replace(b"\r\n", b"\n")
        target = S / f"{PREFIX}{source.name}.txt"
        shutil.copyfile(source, target)
        provenance.append({"path": name, "archive": target.relative_to(R).as_posix(),
                           "sha256": sha(target), "exactSignedHeadSourceVerified": True})
    for module in ("app", "core"):
        assert (A / module / ".." / ".." / "learning-japanese").resolve() == R
    subprocess.run(["git", "-C", str(A), "merge-base", "--is-ancestor", PRODUCTION, ANDROID], check=True)
    changed = git(A, "diff", "--name-only", PRODUCTION, ANDROID).splitlines()
    assert all(x.startswith(("core/src/test/", "docs/", ".github/")) for x in changed)
    artifacts = []
    for name, source in (
        ("gradle-log.txt", L / "android.txt"), ("gradle-arguments.json", L / "android-arguments.json"),
        ("runner-role.json", L / "android-runner-role.json"),
        ("host-heap.init.gradle.txt", C / "batch-065-host-integration-heap.init.gradle"),
        ("wrapper.ps1.txt", C / "run-612-android.ps1"), ("recipe.py", Path(__file__)),
    ):
        target = S / f"{PREFIX}{name}"
        shutil.copyfile(source, target)
        artifacts.append({"archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    evidence = {
        "schemaVersion": 1, "execution": 612, "batch": "087", "status": "fresh-android-passed-awaiting-native",
        "contentTestedHead": HEAD, "teachingSnapshot": SNAPSHOT, "androidTestedHead": ANDROID,
        "unchangedProductionAndroidHead": PRODUCTION, "testOnlyDeltaPaths": changed,
        "androidQualification": "TESTONLY publishable fixture adjustment atop unchanged production, not latest app main.",
        "actualResolvedContentRoot": str(R), "sourceProvenance": provenance,
        "sourcePathResolution": "Both module ../../learning-japanese paths resolve to this tree; full current publishable fixture, not partial/static content.",
        "freshRun": True, "gradleExitCode": 0, "startedAt": start_time.isoformat(), "completedAt": end_time.isoformat(),
        "tests": tests, "totalTests": 4, "totalSkipped": 0, "artifacts": artifacts, "runtime": runtime(),
        "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
        "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
        "gradle": {"oneWorker": True, "noParallel": True, "rerunTasks": True, "kotlinCompiler": "in-process",
                   "coreHostHeap": "Existing approved 2g host-only init script; no guest/app heap change."},
        "request": p["execution612StartingState"]["request"],
        "runnerLockRole": p["execution612StartingState"]["runnerLockRole"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "textualReconciliation": "docs/n1-reviews/batch-087-reconciliation.json",
        "reconciliationSha256": sha(R / "docs" / "n1-reviews" / "batch-087-reconciliation.json"),
        "textualReviewClosed": True, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "newNativeOrPhoneClaimed": False, "publishedAdditions": 113, "remainingAdditions": 1115,
        "lastPublishedCommit": p["lastPublishedCommit"], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT,
        "limits": ["Four fresh non-skipped JVM cases only, not native glyph/phone evidence.",
                   "Full current publishable parser/mixed/legacy fixtures do not establish Room ContentSync/native route acceptance.",
                   "All21 scoped Han/fourfont/systemfallback, production N1 fallback, reading/drawing/article/Back/offline gates pending.",
                   "Original textual review/source qualifications unchanged. No reviewer or native run in execution612.",
                   "Current-main integration/combinedchecks/normal signing/owner push/terminal CI/every immutable ZIP hash/original guards pending."],
    }
    save(S / "execution-612.json", evidence)
    packet = load(S / "batch-087-progress.json")
    packet.update(status=evidence["status"], nextAction=NEXT)
    packet["androidAcceptance"] = {"execution": 612, "contentTestedHead": HEAD, "androidTestedHead": ANDROID,
        "totalTests": 4, "totalSkipped": 0, "evidence": "docs/n1-sources/execution-612.json",
        "status": "passed", "nativeAcceptance": "pending", "runtimePublished": False}
    save(S / "batch-087-progress.json", packet, ensure_ascii=False)
    print(json.dumps({"tests": tests, "runtime": evidence["runtime"]}, indent=2))


def finalize():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert head != HEAD and git(R, "rev-parse", "HEAD^") == HEAD
    changed = git(R, "diff", "--name-only", HEAD, head).splitlines()
    assert changed and all(x.startswith("docs/n1-sources/") for x in changed)
    e = load(S / "execution-612.json")
    assert runtime() == e["runtime"]
    for record in e["tests"] + e["sourceProvenance"] + e["artifacts"]:
        assert sha(R.joinpath(*record["archive"].split("/"))) == record["sha256"]
    assert sha(R / "docs" / "n1-reviews" / "batch-087-reconciliation.json") == e["reconciliationSha256"]
    receipt = load(C / f"{PREFIX}issue-receipt.json")
    body = (C / f"{PREFIX}issue-body.txt").read_text(encoding="utf-8-sig")
    assert receipt["user"]["login"] == "stop-cran" and head in receipt["body"]
    assert receipt["body"].replace("\r\n", "\n").strip() == body.replace("\r\n", "\n").strip()
    original = load(L / "progress-before-612.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    checkpoint = {
        **{k: e[k] for k in ("schemaVersion", "execution", "batch", "status", "contentTestedHead", "androidTestedHead",
           "teachingSnapshot", "totalTests", "totalSkipped", "runtime", "textualReviewClosed", "runtimeChanged",
           "runtimeAccepted", "runtimePublished", "newNativeOrPhoneClaimed", "publishedAdditions", "remainingAdditions",
           "lastPublishedCommit", "physicalPhoneAcceptance", "generalReleaseAcceptance", "wholeProjectComplete",
           "nextBatchStarted", "parentLockTouched", "optionalHistoricalSessionHelpersAccessed", "actualNewPermissionDenials")},
        "checkpoint": 612, "savedCommit": head, "signature": "G", "stage": e["status"],
        "evidence": "docs/n1-sources/execution-612.json", "dedicatedWorktreesClean": True,
        "reviewClosed": [], "published": [], "nextAction": NEXT, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(original),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "verifiedAt": datetime.now(timezone.utc).isoformat(),
    }
    p.update(checkpoint=612, status="continue", stage=e["status"], nextAction=NEXT, blocker=None)
    p["execution612StartingState"]["status"] = "signed-local-android-checkpoint-complete"
    p["execution612CoordinatorCheckpoint"] = checkpoint
    p["batch087AndroidCheckpoint"] = copy.deepcopy(checkpoint)
    persist(p)
    assert all(load(C / "progress.json")[k] == v for k, v in original.items() if k not in allowed)
    save(L / "batch-087-android-checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": 612, "savedCommit": head, "tests": 4, "skipped": 0,
                      "status": "continue", "allHistoricalValuesPreserved": True, "issueUpdate": receipt["html_url"]}, indent=2))


if __name__ == "__main__":
    {"start": start, "collect": collect, "finalize": finalize}[sys.argv[1]]()
