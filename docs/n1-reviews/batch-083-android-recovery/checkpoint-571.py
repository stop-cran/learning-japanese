from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
CONTROL = Path(r"C:\Users\stop-\n1-kanji-workspace\control")
CONTENT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOG = CONTROL / "logs" / "bb3b3736-672b-44f7-b9a6-8be9048f0c84"
PROGRESS = CONTROL / "progress.json"
HEAD = "677c9864340303be42a4bd77aa21d5229167ddb8"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
ARCHIVE = CONTENT / "docs" / "n1-reviews" / "batch-083-android"
INIT = CONTROL / "batch-065-host-integration-heap.init.gradle"
NEXT = (
    "SAME083 fresh Android gate passed3RealContentTest+1RareHanTest, zero failures/errors/skips, "
    "against THIS content tree and signedAndroid1c1b7bf4 publishable-content harness with unchanged "
    "approved2GiBHOSTinit. NEXT bounded coordinator prepare exact full runtime native fixture using "
    "productionContentSync ONCE, preserve source/hash/provenance, all29Han/fourfonts with native "
    "冫/夌/阝/隹 pending, actual selection/meaning/curatedreading/drawing/article/systemBack/offline "
    "and terminal per-case0 plus two-family visual confirmation. Inspect current port/device ownership "
    "before launch; do not assume historical batch040 routing override applies. No heap/guard increase, "
    "no contributor-doc traversal, no app production edits, no optional historicalsessionhelper access. "
    "Current clean signedAndroid1c1b7bf4, not oldf9b59a2. Textual closure677c9864 retained; native/visual/"
    "currentmain/integration/normal signing/ownerfastforward/CI/exactimmutableZIP acceptance still "
    "required before publication or084. Preserve full historical source/review/process/denial/OOM/"
    "read-depth/viewport limits. Published109/1228,remaining1119 unchanged; compatibleAPKf9b59a2+; "
    "physicalphone/generalrelease/whole-set outstanding. No second runner."
)
BLOCKED_NEXT = (
    "SAME083 fresh Android gate NOT executed. Execution571 wrapper copied a historical parent-runner "
    "exclusive runner.lock check, but current supervisor PID9004 already owns that lock. The initial "
    "File.Open failed with a Windows sharing violation before Gradle, without reading/changing lock "
    "contents or launching tests. Preserve exact diagnostic and wrapper; do not retry/unlock/stop/"
    "change supervisor or its policies. Parent must disposition this unnecessary child acquisition "
    "before the next coordinator runs unchanged3RealContentTest+1RareHanTest with signedAndroid"
    "1c1b7bf4, verifiedJDK17/SDK/oneworker/approved2GiBHOSTinit. No new source/reviewer/test "
    "permission denial established; this is a runner-resource conflict and an overbroad wrapper "
    "preflight, not a missing mandatory input. All textual review/source/history preserved. "
    "Do not access historical session helpers. No native/visual/integration/publication/084; "
    "all original acceptance gates, heap/archiveguards remain. Published109/1228,remaining1119; "
    "physicalphone/generalrelease/whole-set outstanding."
)
CASES = [
    ("core", "test", "RealContentTest", {
        "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
        "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent",
        "parsesRealContentRepoWhenPresent",
    }),
    ("app", "testDebugUnitTest", "RareHanTest", {
        "contentRareCharactersAreCoveredByBundledFont",
    }),
]


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".571.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), "--no-pager", *args], text=True, encoding="utf-8"
    ).strip()


def runtime():
    sys.path.insert(0, str(CONTENT / "tools"))
    from build_manifest import build_manifest
    manifest = read(CONTENT / "manifest.json")
    assert build_manifest(CONTENT) == manifest
    count = sum(len(value) for value in manifest.values() if isinstance(value, dict))
    assert count == 8376, count
    return {
        "manifestSha256": sha(CONTENT / "manifest.json"),
        "contentVersion": manifest["contentVersion"],
        "runtimeManifestHashesVerified": count,
    }


def historical_check(progress, baseline, allowed):
    assert set(baseline) <= set(progress)
    for key, value in baseline.items():
        if key not in allowed:
            assert progress[key] == value, key
    return len(baseline)


def begin():
    baseline_path = LOG / "progress-before-571.json"
    assert not baseline_path.exists(), "Do not replace an execution baseline"
    progress = read(PROGRESS)
    assert progress["checkpoint"] == 570 and progress["batch"] == "083"
    assert progress["stage"] == "textually-review-closed-awaiting-fresh-android"
    for root, expected in ((CONTENT, HEAD), (ANDROID, APP)):
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain")
    assert sha(INIT) == "438159ae22b313e8196a0bc011f72a3b17300146b219c5ffcc779c540a64be24"
    raw = (LOG / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):",
        1,
    )[1])
    assert checkpoint["execution570CoordinatorCheckpoint"]["savedCommit"] == HEAD
    write(baseline_path, progress)
    state = {
        "execution": 571, "batch": "083",
        "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": git(CONTENT, "rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME083 fresh Android RealContentTest3+RareHanTest1, signed LOCAL evidence only; yield before native/visual/integration/publication/084.",
        "authorization": {
            "requestSha256": sha(LOG / "request.txt"),
            "bytes": len(raw), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, full approved issue and final checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "durableHelper": str(Path(__file__)),
            "optionalHistoricalSessionHelpersAccessed": False,
            "actualNewPermissionDenials": [],
        },
        "qualifiedHostInit": {
            "path": str(INIT), "sha256": sha(INIT), "coreTestMaxHeap": "2g",
            "unchangedFromAcceptedBatch082": True,
            "productionGuestHeapOrArchiveGuardsChanged": False,
            "neverForNative": True,
        },
        "fixtureRoots": [],
        **runtime(),
    }
    for module, _, _, _ in CASES:
        root = (ANDROID / module / ".." / ".." / "learning-japanese").resolve()
        assert root == CONTENT
        state["fixtureRoots"].append({"module": module, "resolvedRoot": str(root)})
    write(LOG / "starting-state-571.json", state)
    progress["execution571StartingState"] = state
    progress["stage"] = "fresh-host-android-checks-running"
    progress["nextAction"] = "SAME083 run fresh non-skipped RealContentTest3+RareHanTest1; preserve signed local evidence, then yield before native."
    historical_check(progress, read(baseline_path), {"stage", "nextAction"})
    write(PROGRESS, progress)
    print(json.dumps({"stage": progress["stage"], **runtime()}))


def collect():
    state = read(LOG / "starting-state-571.json")
    assert git(CONTENT, "rev-parse", "HEAD") == HEAD
    assert git(ANDROID, "rev-parse", "HEAD") == APP
    assert not git(CONTENT, "status", "--porcelain")
    assert not git(ANDROID, "status", "--porcelain")
    assert int((LOG / "android-exit.txt").read_text().strip()) == 0
    start = datetime.fromisoformat((LOG / "android-start.txt").read_text().strip())
    end = datetime.fromisoformat((LOG / "android-end.txt").read_text().strip())
    log = (LOG / "android.txt").read_text(encoding="utf-8-sig")
    assert "BUILD SUCCESSFUL" in log
    assert "UP-TO-DATE" not in log and "FROM-CACHE" not in log
    assert start >= datetime.fromisoformat(state["startedAt"])
    ARCHIVE.mkdir(parents=True, exist_ok=False)
    tests = []
    for module, task, name, expected in CASES:
        source = ANDROID / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{name}.xml"
        suite = ET.parse(source).getroot()
        assert int(suite.attrib["tests"]) == len(expected)
        assert all(int(suite.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
        cases = suite.findall("testcase")
        assert {case.attrib["name"] for case in cases} == expected
        assert all(not list(case) for case in cases)
        timestamp = datetime.fromisoformat(suite.attrib["timestamp"].removesuffix("Z")).replace(tzinfo=timezone.utc)
        assert start <= timestamp <= end
        destination = ARCHIVE / source.name
        shutil.copyfile(source, destination)
        assert sha(source) == sha(destination)
        tests.append({
            "class": suite.attrib["name"], "tests": len(expected),
            "failures": 0, "errors": 0, "skipped": 0,
            "caseNames": sorted(expected), "timestamp": suite.attrib["timestamp"],
            "source": str(source), "archive": destination.relative_to(CONTENT).as_posix(),
            "sha256": sha(destination), "fixtureRoot": str(CONTENT),
        })
    provenance = []
    for source, name in [
        (LOG / "android.txt", "gradle.txt"),
        (LOG / "android-arguments.json", "arguments.json"),
        (LOG / "android-start.txt", "start.txt"),
        (LOG / "android-end.txt", "end.txt"),
        (LOG / "android-exit.txt", "exit.txt"),
        (CONTROL / "run-571-android.ps1", "run-571-android.ps1"),
        (Path(__file__), "checkpoint-571.py"),
        (INIT, INIT.name),
        (ANDROID / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "PublishableContentFixture.kt", "PublishableContentFixture.kt"),
    ]:
        target = ARCHIVE / name
        shutil.copyfile(source, target)
        provenance.append({"source": str(source), "archive": target.relative_to(CONTENT).as_posix(), "sha256": sha(target)})
    assert runtime()["manifestSha256"] == state["manifestSha256"]
    evidence = {
        "schemaVersion": 1, "execution": 571, "batch": "083",
        "status": "fresh-android-passed-awaiting-native",
        "contentTestedCommit": HEAD, "teachingSnapshot": "4b8bfcc4bc4fff4c73185a8cc6c27d4cb5736efc",
        "androidHead": APP, "androidSignature": git(ANDROID, "log", "-1", "--format=%G?"),
        "freshOriginMain": state["freshOriginMain"],
        "start": start.isoformat(), "end": end.isoformat(), "actualExitCode": 0,
        "buildResult": next(line.strip() for line in log.splitlines() if "BUILD SUCCESSFUL" in line),
        "tasks": next(line.strip() for line in log.splitlines() if "actionable tasks:" in line),
        "oneWorker": True, "parallel": False, "rerunTasks": True,
        "testCount": 4, "failuresErrorsSkips": 0,
        "tests": tests, "provenance": provenance,
        "hostInit": state["qualifiedHostInit"],
        "fixtureSelection": "Pinned signed1c1b7bf4 PublishableContentFixture, NUL-delimited Git export-ignore selection with fail-closed manifest dependency checks; same sibling content root in core/app.",
        "runtimeUnchanged": True, **runtime(),
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "runtimePublished": False, "newNativeOrPhysicalPhoneClaimed": False,
        "nextAction": NEXT,
        "limits": "Fresh JVM corpus/rare-codepoint gate only. RareHanTest is not glyph-legibility evidence. All29Han/fourfonts native/visual checks including 冫/夌/阝/隹 remain pending, as do native routes/drawing, current-main integration, signed owner publication, CI and exact immutable ZIP acceptance. Physical-phone/general-release/whole-set acceptance outstanding. All prior source/review/process/denial/OOM/read-depth/viewport limits and original heap/archive guards preserved.",
    }
    write(CONTENT / "docs" / "n1-sources" / "execution-571.json", evidence)
    print(json.dumps({"testCount": 4, "failuresErrorsSkips": 0, "status": evidence["status"]}))


def blocked():
    state = read(LOG / "starting-state-571.json")
    assert git(CONTENT, "rev-parse", "HEAD") == HEAD
    assert not git(CONTENT, "status", "--porcelain")
    assert not git(ANDROID, "status", "--porcelain")
    assert not (LOG / "android-start.txt").exists()
    assert not (LOG / "android-exit.txt").exists()
    diagnostic = {
        "execution": 571,
        "attempt": "powershell run-571-android.ps1",
        "shellId": "batch083-android-571",
        "exitCode": 1,
        "statement": "$lock = [IO.File]::Open((Join-Path $control 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')",
        "exception": "MethodInvocationException, line5: Exception calling Open with 4 arguments: The process cannot access the file 'C:\\Users\\stop-\\n1-kanji-workspace\\control\\runner.lock' because it is being used by another process.",
        "classification": "Windows sharing violation on supervisor-owned resource; not a missing source packet, content defect, failed test, or established access-policy denial.",
        "cause": "Coordinator incorrectly reused a historical parent-runner exclusion check inside the already-running supervisor child.",
        "supervisorObserved": read(CONTROL / "runner.json"),
        "supervisorLockImplementation": "control/runner.ps1:115 opens runner.lock with FileShare.None",
        "gradleStarted": False,
        "testsRun": 0,
        "attempts": 1,
        "retriedUnlockedOrBypassed": False,
        "supervisorEditedOrStopped": False,
        "disposition": "Preserve/report/yield; parent disposition required before another child wrapper execution.",
    }
    ARCHIVE.mkdir(parents=True, exist_ok=False)
    write(ARCHIVE / "execution-571-sharing-violation.json", diagnostic)
    provenance = []
    for source, name in [
        (CONTROL / "run-571-android.ps1", "run-571-android.ps1"),
        (Path(__file__), "checkpoint-571.py"),
        (ARCHIVE / "execution-571-sharing-violation.json", "execution-571-sharing-violation.json"),
    ]:
        target = ARCHIVE / name
        if source != target:
            shutil.copyfile(source, target)
        provenance.append({"source": str(source), "archive": target.relative_to(CONTENT).as_posix(), "sha256": sha(target)})
    evidence = {
        "schemaVersion": 1, "execution": 571, "batch": "083",
        "status": "blocked-supervisor-lock-before-android",
        "contentTestedCommit": None, "preservedContentCommit": HEAD,
        "teachingSnapshot": "4b8bfcc4bc4fff4c73185a8cc6c27d4cb5736efc",
        "androidHead": APP, "androidSignature": "G",
        "freshOriginMain": state["freshOriginMain"],
        "startingState": state,
        "actualAttemptExitCode": 1, "gradleStarted": False,
        "testCount": 0, "tests": [], "provenance": provenance,
        "diagnostic": diagnostic,
        "runtimeUnchanged": True, **runtime(),
        "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "actualNewResourceAccessFailures": [diagnostic["exception"]],
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "runtimePublished": False, "newAndroidNativeOrPhysicalPhoneClaimed": False,
        "nextAction": BLOCKED_NEXT,
        "limits": "Fresh Android gate remains unperformed, not passed/failed/skipped. Native/font/visual/current-main/integration/CI/immutableZIP/phone/generalrelease/whole-set remain unaccepted. No runtime, app, lock, supervisor, policy or heap/archiveguard changes.",
    }
    assert evidence["manifestSha256"] == state["manifestSha256"]
    write(CONTENT / "docs" / "n1-sources" / "execution-571.json", evidence)
    print(json.dumps({"status": evidence["status"], "testsRun": 0, "runtimeChanged": False}))


def finish():
    evidence = read(CONTENT / "docs" / "n1-sources" / "execution-571.json")
    saved = git(CONTENT, "rev-parse", "HEAD")
    assert git(CONTENT, "log", "-1", "--format=%G?") == "G"
    assert git(CONTENT, "rev-parse", "HEAD^") == HEAD
    assert not git(CONTENT, "status", "--porcelain")
    assert not git(ANDROID, "status", "--porcelain")
    changed = git(CONTENT, "diff", "--name-only", HEAD, saved).splitlines()
    assert changed and all(name.startswith(("docs/n1-reviews/batch-083-android/", "docs/n1-sources/execution-571.json")) for name in changed)
    for entry in evidence["tests"] + evidence["provenance"]:
        assert sha(CONTENT / entry["archive"]) == entry["sha256"]
    receipt = read(LOG / "issue-receipt.json")
    body = (CONTROL / "issue-update-571.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").strip() == body.strip()
    assert saved in body
    progress = read(PROGRESS)
    baseline = read(LOG / "progress-before-571.json")
    assert progress["checkpoint"] == 570
    is_blocked = evidence["status"] == "blocked-supervisor-lock-before-android"
    check = {
        "schemaVersion": 1, "execution": 571, "checkpoint": 571, "batch": "083",
        "savedCommit": saved, "signature": "G",
        "status": "blocked" if is_blocked else "continue", "stage": evidence["status"],
        "evidence": "docs/n1-sources/execution-571.json",
        "androidHead": APP, "contentTestedCommit": evidence["contentTestedCommit"],
        "preservedContentCommit": HEAD,
        "freshTests": evidence["testCount"],
        "freshAndroidAccepted": not is_blocked,
        "runtimeManifestHashesVerified": 8376,
        "runtimePublished": False, "runtimeAccepted": False,
        "nativeFontPending": ["冫", "夌", "阝", "隹"],
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": baseline["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": evidence["nextAction"], "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "dedicatedWorktreesClean": True,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    progress.update(
        checkpoint=571, status=check["status"], stage=evidence["status"],
        nextAction=evidence["nextAction"],
        blocker={
            "kind": "supervisor-resource-sharing-conflict",
            "path": str(CONTROL / "runner.lock"),
            "gradleStarted": False,
            "testsRun": 0,
            "preservedEvidence": "docs/n1-sources/execution-571.json",
            "reason": "Child wrapper attempted parent-only exclusive runner.lock acquisition; supervisor already owns lock. No retry or lock/policy change; yield for parent disposition.",
        } if is_blocked else None,
    )
    progress["execution571CoordinatorCheckpoint"] = check
    progress["batch083AndroidCheckpoint"] = check.copy()
    count = historical_check(progress, baseline, {"checkpoint", "status", "stage", "nextAction", "blocker"})
    check["originalRootKeysCompared"] = count
    check["allOriginalHistoricalRootValuesPreservedExactly"] = True
    progress["execution571StartingState"]["status"] = (
        "signed-local-resource-conflict-checkpoint-complete" if is_blocked else
        "signed-local-android-checkpoint-complete"
    )
    write(PROGRESS, progress)
    reread = read(PROGRESS)
    historical_check(reread, baseline, {"checkpoint", "status", "stage", "nextAction", "blocker"})
    assert runtime()["manifestSha256"] == read(LOG / "starting-state-571.json")["manifestSha256"]
    write(LOG / "checkpoint-571.json", check)
    print(json.dumps(check, ensure_ascii=False, indent=2))


def verify_blocked():
    progress = read(PROGRESS)
    assert progress["checkpoint"] == 571 and progress["status"] == "blocked"
    for key in ("execution571CoordinatorCheckpoint", "batch083AndroidCheckpoint"):
        assert progress[key]["freshTests"] == 0
        progress[key]["contentTestedCommit"] = None
        progress[key]["preservedContentCommit"] = HEAD
    historical_check(
        progress, read(LOG / "progress-before-571.json"),
        {"checkpoint", "status", "stage", "nextAction", "blocker"},
    )
    write(PROGRESS, progress)
    write(LOG / "checkpoint-571.json", progress["execution571CoordinatorCheckpoint"])
    assert not git(CONTENT, "status", "--porcelain")
    assert not git(ANDROID, "status", "--porcelain")
    assert git(CONTENT, "log", "-1", "--format=%G?") == "G"
    assert not (LOG / "android-start.txt").exists()
    assert not (LOG / "android-exit.txt").exists()
    print("Blocked checkpoint571 verified: no tests run, signed local evidence, clean worktrees, full historical values preserved.")


{"begin": begin, "collect": collect, "blocked": blocked, "finish": finish,
 "verify-blocked": verify_blocked}[sys.argv[1]]()
