import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "842472e9-0ae8-4380-bb52-9eb67dfc1d57"
S = R / "docs" / "n1-sources"
HEAD = "75918e23e665a167fa41f0c06a02513851b841e5"
TEACHING = "70dfe3344d167e5152a3685b09689d73fa1cdab1"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
RUNNING = "batch-099-fresh-host-android-checks-running"
STAGE = "batch-099-fresh-android-passed-awaiting-native"
PREFIX = "batch-099-android-731-"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).rstrip("\r\n")


def heads(content=HEAD, clean=True):
    for root, expected in ((R, content), (A, ANDROID)):
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        if clean:
            assert not git(root, "status", "--porcelain=v1", "--untracked-files=all")


def persist(p):
    target = C / "progress.731.tmp"
    assert not target.exists()
    save(target, p)
    assert load(target) == p
    target.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == "5408632b5aa1382c"
    count = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                path = R.joinpath(*name.split("/"))
                actual = sha(path) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                } else sha256(path)
                assert actual == digest, name
                count += 1
    assert count == 8451
    review = load(R / "docs" / "n1-reviews" / "batch-099-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    assert not git(R, "diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"runtimePayloadHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "manifestFreshAndUnchanged": True}


def next_action():
    previous = load(L / "progress-before-731.json")["nextAction"]
    return (
        "SAME099 native/visual preparation and acceptance next on unchanged textually closed signed70dfe334. "
        "Fresh731 sibling RealContentTest THREE and RareHanTest ONE passed, zero skips/failures/errors; "
        "host JVM acceptance ONLY, not native or full batch acceptance. "
        "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain. "
        "Run fresh " + previous.split("Then fresh ", 1)[1]
    )


def start():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (
        730, "099", "continue", "batch-099-textual-review-closed-awaiting-android-native"
    )
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (15692, L.name, "running")
    role = load(L / "android-runner-role.json")
    assert role["liveParentPid"] == 15692 and not role["lockTouched"]
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    frozen = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert frozen["checkpoint"] == 730
    assert frozen["execution730CoordinatorCheckpoint"]["savedCommit"] == HEAD
    assert not (L / "progress-before-731.json").exists()
    subprocess.run(["git", "-C", str(R), "fetch", "--quiet", "origin", "main"], check=True)
    checked = runtime()
    save(L / "progress-before-731.json", p)
    p["stage"] = RUNNING
    p["execution731StartingState"] = {
        "execution": 731, "batch": "099", "startingHead": HEAD, "androidHead": ANDROID,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME099 four fresh JVM cases and normally signed LOCAL evidence only; no native/reviewer/publication/100.",
        "request": {
            "sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete approved issue and final730 directly inspected. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved control helpers, committed packets and frozen inputs only; no optional historical-session recipes accessed.",
        "runtime": checked, "status": "fresh-host-android-checks-running",
        "actualNewPermissionDenials": [],
    }
    persist(p)
    print("Starting731 persisted; all original history preserved.", flush=True)


def collect():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["stage"]) == (730, RUNNING)
    assert (L / "android-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    begin = datetime.fromisoformat((L / "android-start.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((L / "android-end.txt").read_text(encoding="utf-8-sig").strip())
    assert "BUILD SUCCESSFUL" in (L / "android.txt").read_text(encoding="utf-8-sig")
    checked = runtime()
    artifacts = []

    def archive(source, suffix):
        target = S / (PREFIX + suffix)
        assert not target.exists()
        shutil.copyfile(source, target)
        record = {"archive": target.relative_to(R).as_posix(), "sha256": sha(target)}
        artifacts.append(record)
        return record

    tests = []
    for module, task, cls, names in (
        ("core", "test", "RealContentTest", {
            "parsesRealContentRepoWhenPresent", "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
            "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent",
        }),
        ("app", "testDebugUnitTest", "RareHanTest", {"contentRareCharactersAreCoveredByBundledFont"}),
    ):
        source = A / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{cls}.xml"
        xml = ET.parse(source).getroot()
        assert int(xml.attrib["tests"]) == len(names)
        assert all(int(xml.attrib[k]) == 0 for k in ("skipped", "failures", "errors"))
        assert {x.attrib["name"] for x in xml.findall("testcase")} == names
        assert not any(x.find(t) is not None for x in xml.findall("testcase") for t in ("skipped", "failure", "error"))
        assert begin <= datetime.fromisoformat(xml.attrib["timestamp"]) <= end
        assert source.stat().st_mtime >= begin.timestamp()
        tests.append({**archive(source, module + ".xml"), "module": module, "class": xml.attrib["name"],
                      "tests": len(names), "skipped": 0, "failures": 0, "errors": 0,
                      "caseNames": sorted(names), "timestamp": xml.attrib["timestamp"]})
    provenance = []
    for name in (
        "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    ):
        source = A.joinpath(*name.split("/"))
        committed = subprocess.check_output(["git", "-C", str(A), "show", f"{ANDROID}:{name}"])
        assert source.read_bytes().replace(b"\r\n", b"\n") == committed.replace(b"\r\n", b"\n")
        provenance.append({**archive(source, source.name + ".txt"), "path": name,
                           "exactSignedHeadSourceVerified": True})
    for module in ("app", "core"):
        assert (A / module / ".." / ".." / "learning-japanese").resolve() == R
    subprocess.run(["git", "-C", str(A), "merge-base", "--is-ancestor", PRODUCTION, ANDROID], check=True)
    changed = git(A, "diff", "--name-only", PRODUCTION, ANDROID).splitlines()
    assert all(x.startswith(("core/src/test/", "docs/", ".github/")) for x in changed)
    raw = (L / "android.txt").read_bytes()
    target = S / (PREFIX + "gradle-log.txt.gz")
    assert not target.exists()
    target.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(target.read_bytes()) == raw
    artifacts.append({"archive": target.relative_to(R).as_posix(), "sha256": sha(target),
                      "uncompressedSha256": hashlib.sha256(raw).hexdigest()})
    for source, suffix in (
        (L / "android-arguments.json", "gradle-arguments.json"),
        (L / "android-runner-role.json", "runner-role.json"),
        (C / "batch-065-host-integration-heap.init.gradle", "host-heap.init.gradle.txt"),
        (C / "run-731-android.ps1", "wrapper.ps1.txt"), (Path(__file__), "recipe.py"),
    ):
        archive(source, suffix)
    e = {
        "schemaVersion": 1, "execution": 731, "batch": "099", "status": STAGE,
        "contentTestedHead": HEAD, "teachingSnapshot": TEACHING, "androidTestedHead": ANDROID,
        "unchangedProductionAndroidHead": PRODUCTION,
        "androidQualification": "TESTONLY publishable fixture adjustment, not latest app main or production change.",
        "testOnlyDeltaPaths": changed, "actualResolvedContentRoot": str(R), "sourceProvenance": provenance,
        "tests": tests, "totalTests": 4, "totalSkipped": 0, "freshRun": True, "gradleExitCode": 0,
        "startedAt": begin.isoformat(), "completedAt": end.isoformat(), "artifacts": artifacts, "runtime": checked,
        "startingState": p["execution731StartingState"],
        "gradle": {"oneWorker": True, "noParallel": True, "rerunTasks": True, "kotlinCompiler": "in-process",
                   "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
                   "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
                   "coreHostHeap": "Existing approved 2g host-only init script; guest/app heap unchanged."},
        "textualReviewClosed": True, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newNativeOrPhoneClaimed": False, "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": p["lastPublishedCommit"], "wholeProjectComplete": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding", "nextAction": next_action(),
        "limits": [
            "Four fresh JVM cases only; native glyph/four-font/ContentSync/route and phone evidence not supplied.",
            "Original two-family textual review and all limitations remain, not new blind review credit.",
            "All native/current-main/publication gates remain. No runtime content change or publication.",
        ],
    }
    save(S / "execution-731.json", e)
    packet_path = S / "batch-099-progress.json"
    packet = load(packet_path)
    assert packet["status"] == "batch-099-textual-review-closed-awaiting-android-native"
    assert packet["reviewClosed"] == packet["published"] == []
    assert packet["pendingGates"][0] == "Fresh non-skipped THREE RealContentTest/ONE RareHanTest against actual sibling."
    packet.update(status=STAGE, nextAction=e["nextAction"], pendingGates=packet["pendingGates"][1:])
    packet["limits"] = [s.replace(
        "Fresh non-skipped Android/native/four-font/all-Han/rendered review including",
        "Fresh four-case non-skipped JVM gate passed; native/four-font/all-Han/rendered review including",
    ) for s in packet["limits"]]
    assert "androidAcceptance" not in packet
    packet["androidAcceptance"] = {
        "execution": 731, "status": "passed", "evidence": "docs/n1-sources/execution-731.json",
        "totalTests": 4, "totalSkipped": 0, "nativeAcceptance": "pending", "runtimePublished": False,
    }
    save(packet_path, packet)
    expected = {record["archive"] for record in artifacts} | {
        "docs/n1-sources/execution-731.json", "docs/n1-sources/batch-099-progress.json",
    }
    assert {line[3:] for line in git(R, "status", "--porcelain=v1", "--untracked-files=all").splitlines()} == expected
    subprocess.run(["git", "-C", str(R), "diff", "--check"], check=True)
    print(json.dumps({"tests": tests, "runtime": checked}, indent=2))


def finish():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    assert all(x.startswith("docs/n1-sources/") for x in git(R, "diff", "--name-only", HEAD, head).splitlines())
    e = load(S / "execution-731.json")
    assert runtime() == e["runtime"]
    for record in e["artifacts"]:
        assert sha(R.joinpath(*record["archive"].split("/"))) == record["sha256"]
    posted = load(L / "issue-731-reread.json")
    body = (C / "batch-099-android-731-issue-body.txt").read_bytes().decode("utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    original = load(L / "progress-before-731.json")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["stage"]) == (730, "099", RUNNING)
    checkpoint = {
        "schemaVersion": 1, "execution": 731, "checkpoint": 731, "batch": "099", "status": "continue",
        "stage": STAGE, "savedCommit": head, "signature": "G", "contentTestedHead": HEAD,
        "teachingSnapshot": TEACHING, "androidHead": ANDROID,
        "evidence": "docs/n1-sources/execution-731.json", "issueUpdate": posted["html_url"],
        "ownerIssueAuthorAndBodyVerified": True, "totalTests": 4, "totalSkipped": 0,
        "failures": 0, "errors": 0, "freshRun": True, "dedicatedWorktreesClean": True,
        "runtimeBytesUnchanged": True, "runtimeAccepted": False, "runtimePublished": False,
        "textualReviewClosed": True, "reviewClosed": [], "published": [],
        "publishedAdditions": 125, "remainingAdditions": 1103, "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "allRuntimePayloadHashesVerified": 8451, "contentVersion": e["runtime"]["contentVersion"],
        "nextAction": e["nextAction"], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True,
    }
    p.update(checkpoint=731, status="continue", stage=STAGE, nextAction=e["nextAction"], blocker=None)
    p["execution731StartingState"]["status"] = "signed-local-host-android-checkpoint-complete"
    p["execution731CoordinatorCheckpoint"] = checkpoint
    p["batch099AndroidCheckpoint"] = copy.deepcopy(checkpoint)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    persist(p)
    save(L / "checkpoint-731.json", checkpoint)
    assert load(C / "progress.json") == p
    print(json.dumps(checkpoint, indent=2))


if __name__ == "__main__":
    {"start": start, "collect": collect, "finish": finish}[sys.argv[1]]()
