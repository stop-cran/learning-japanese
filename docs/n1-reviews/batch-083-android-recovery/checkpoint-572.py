import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

CONTROL = pathlib.Path(__file__).resolve().parent
CONTENT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
PROGRESS = CONTROL / "progress.json"
BEFORE = CONTROL / "artifacts" / "execution-572-progress-before.json"
START_HEAD = "c3ebb45896b3637ad784ba33d89e8fff3356925a"
APP_HEAD = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PUBLIC_HEAD = "21a5cb1328aadd437139a6b850f07298a2e2985d"
ARCHIVE = CONTENT / "docs" / "n1-reviews" / "batch-083-android-recovery"
EVIDENCE = CONTENT / "docs" / "n1-sources" / "execution-572.json"
SUMMARY = CONTROL / "execution-572-checkpoint.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), "--no-pager", *args], encoding="utf-8"
    ).strip()


def signed_clean(root, head):
    require(git(root, "rev-parse", "HEAD") == head, "Unexpected signed HEAD")
    require(git(root, "log", "-1", "--format=%G?") == "G", "Signature not good")
    require(not git(root, "status", "--porcelain"), "Worktree is not wholly clean")


def runtime():
    manifest = CONTENT / "manifest.json"
    require(digest(manifest) == "e7840539ab7b0eca155f21b02e0932b35d42b3246199fe634b749c86751daab9",
            "Frozen manifest changed")
    data = load(manifest)
    require(data["contentVersion"] == "a9faafdd68af3230", "Unexpected content version")
    sys.path.insert(0, str(CONTENT / "tools"))
    from build_manifest import build_manifest
    require(build_manifest(CONTENT) == data, "Runtime manifest differs from current generated payload")
    count = sum(len(value) for value in data.values() if isinstance(value, dict))
    require(count == 8376, "Unexpected runtime count")
    return count


def update_progress(data):
    temporary = PROGRESS.with_suffix(".572.tmp")
    require(not temporary.exists(), "Unexpected checkpoint temporary")
    save(temporary, data)
    require(load(temporary) == data, "Checkpoint serialization changed values")
    temporary.replace(PROGRESS)


def history_preserved(data):
    before = load(BEFORE)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            require(key in data and data[key] == value, "Historical value changed: " + key)
    return len(before)


def start():
    require(not BEFORE.exists(), "Starting snapshot already exists")
    state = load(PROGRESS)
    require(state["checkpoint"] == 571 and state["status"] == "continue"
            and state["batch"] == "083", "Unexpected starting checkpoint")
    signed_clean(CONTENT, START_HEAD)
    signed_clean(ANDROID, APP_HEAD)
    require(git(CONTENT, "rev-parse", "origin/main") == PUBLIC_HEAD, "Remote reference changed")
    count = runtime()
    request = CONTROL / "logs" / "6971e4cb-5513-46e4-bb41-c6aea1fb5a81" / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):",
        1,
    )[1])
    shutil.copyfile(PROGRESS, BEFORE)
    state["execution572StartingState"] = {
        "execution": 572, "batch": "083", "startingHead": START_HEAD,
        "androidHead": APP_HEAD, "freshOriginMain": PUBLIC_HEAD,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "Archive and normally sign LOCAL recovered HOST evidence only; yield before native.",
        "request": {"sha256": digest(request), "bytes": request.stat().st_size,
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Operative contract, complete issue and final checkpoint inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runtimeManifestHashesVerified": count,
        "runnerLockRole": "Live parent runner owns lock; this child never opens, reacquires, deletes or unlocks it.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-083-archiving-recovered-android-evidence"
    state["nextAction"] = "SAME083 verify/archive parent recovery receipts, exact XML/logs/arguments/helpers/qualification, normally sign LOCAL evidence, then yield before native. No HOST rerun, reviewer, integration, publication or084."
    update_progress(state)
    print("Starting state persisted; signed heads and 8376 runtime hashes verified.")


def archive():
    state = load(PROGRESS)
    require(state["checkpoint"] == 571 and "execution572StartingState" in state, "Start first")
    signed_clean(CONTENT, START_HEAD)
    signed_clean(ANDROID, APP_HEAD)
    require(not ARCHIVE.exists() and not EVIDENCE.exists(), "Do not overwrite evidence")
    receipt = load(CONTROL / "batch-083-parent-android-recovery.json")
    disposition = load(CONTROL / "batch-083-parent-lock-disposition.json")
    checkpoint_receipt = json.loads(json.dumps(state["parentBatch083AndroidRecovery"]))
    comparable_receipt = json.loads(json.dumps(receipt))
    for comparison in (checkpoint_receipt, comparable_receipt):
        for test in comparison["tests"]:
            test["timestamp"] = datetime.fromisoformat(
                test["timestamp"].replace("Z", "+00:00")
            ).isoformat()
    require(comparable_receipt == checkpoint_receipt, "Recovery receipt differs from checkpoint")
    require(disposition == state["parentExecution571LockDisposition"], "Disposition differs from checkpoint")
    require(receipt["localContentHead"] == START_HEAD and receipt["androidHead"] == APP_HEAD
            and receipt["exitCode"] == 0 and receipt["oneWorker"] and not receipt["parallel"]
            and receipt["rerunTasks"], "Recovery execution attribution mismatch")
    run = CONTROL / "artifacts" / "batch-083-parent-lock-recovery"
    started = datetime.fromisoformat((run / "start.txt").read_text().strip())
    ended = datetime.fromisoformat((run / "end.txt").read_text().strip())
    require((run / "exit.txt").read_text().strip() == "0", "Actual run exit not zero")
    log = (run / "gradle.txt").read_text(encoding="utf-8-sig")
    require("BUILD SUCCESSFUL in 3m 19s" in log
            and "41 actionable tasks: 41 executed" in log, "Incomplete successful build log")
    arguments = load(run / "arguments.json")
    require(arguments == [
        ":core:test", "--tests", "io.github.stopcran.kanji.core.RealContentTest",
        ":app:testDebugUnitTest", "--tests", "io.github.stopcran.kanji.core.RareHanTest",
        "--no-daemon", "--no-parallel", "--max-workers=1", "--rerun-tasks",
        "-Pkotlin.compiler.execution.strategy=in-process", "--init-script",
        str(CONTROL / "batch-065-host-integration-heap.init.gradle"),
    ], "Unexpected Gradle selection or resource arguments")
    expected_cases = [
        ["hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
         "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent",
         "parsesRealContentRepoWhenPresent"],
        ["contentRareCharactersAreCoveredByBundledFont"],
    ]
    require(len(receipt["tests"]) == 2, "Unexpected suites")
    for test, names in zip(receipt["tests"], expected_cases):
        require(test["fixtureRoot"] == str(CONTENT), "Incorrect fixture root")
        for field in ("artifactPath", "sourcePath"):
            require(digest(pathlib.Path(test[field])) == test["sha256"], "XML source/copy mismatch")
        suite = ET.parse(test["artifactPath"]).getroot()
        require(int(suite.attrib["tests"]) == len(names)
                and all(int(suite.attrib[k]) == 0 for k in ("failures", "errors", "skipped")),
                "Failed, skipped or missing tests")
        require([case.attrib["name"] for case in suite.findall("testcase")] == names
                and test["caseNames"] == names, "Named cases mismatch")
        timestamp = datetime.fromisoformat(suite.attrib["timestamp"].replace("Z", "+00:00"))
        require(started <= timestamp <= ended, "Stale XML timestamp")
    for item in disposition["provenance"]:
        require(digest(pathlib.Path(item["path"])) == item["sha256"], "Parent provenance changed")
    original = load(CONTENT / "docs" / "n1-sources" / "execution-571.json")
    for item in original["provenance"]:
        require(digest(CONTENT.joinpath(*item["archive"].split("/"))) == item["sha256"],
                "Original failed-attempt evidence changed")
    init = CONTROL / "batch-065-host-integration-heap.init.gradle"
    require(digest(init) == "438159ae22b313e8196a0bc011f72a3b17300146b219c5ffcc779c540a64be24",
            "Approved HOST qualification changed")
    files = [
        CONTROL / "batch-083-parent-android-recovery.json",
        CONTROL / "batch-083-parent-lock-disposition.json",
        CONTROL / "runner-lock-role-notes.txt",
        CONTROL / "authoring-artifact-path-notes.txt",
        CONTROL / "run-571-parent-android.ps1",
        CONTROL / "verify-parent-android.ps1",
        CONTROL / "recover-571-parent.ps1",
        CONTROL / "checkpoint-571.py", pathlib.Path(__file__), init,
        *(run / name for name in ("arguments.json", "start.txt", "end.txt", "exit.txt", "gradle.txt")),
        *(pathlib.Path(test["artifactPath"]) for test in receipt["tests"]),
    ]
    ARCHIVE.mkdir()
    provenance = []
    for source in files:
        destination = ARCHIVE / source.name
        require(not destination.exists(), "Archive filename collision")
        shutil.copyfile(source, destination)
        require(digest(source) == digest(destination), "Archive differs from source")
        provenance.append({"source": str(source), "archive": destination.relative_to(CONTENT).as_posix(),
                           "sha256": digest(destination)})
    evidence = {
        "schemaVersion": 1, "execution": 572, "batch": "083",
        "status": "recovered-host-android-passed-local-evidence-only",
        "contentTestedCommit": START_HEAD, "androidHead": APP_HEAD,
        "teachingSnapshot": "4b8bfcc4bc4fff4c73185a8cc6c27d4cb5736efc",
        "textualReviewClosure": "677c9864340303be42a4bd77aa21d5229167ddb8",
        "startingState": state["execution572StartingState"],
        "parentRecovery": receipt, "parentLockDisposition": disposition,
        "provenance": provenance, "freshTests": 4, "freshFailures": 0, "freshSkips": 0,
        "xmlSourceCopiesNamedCasesAndFreshnessVerified": True,
        "original571EvidenceUnchangedAndZeroTestsNotRetroaccepted": True,
        "runtimeManifestHashesVerified": runtime(), "runtimeChanged": False,
        "manifestUnchanged": True, "hostChecksRerunByThisExecution": False,
        "diagnostics": [
            "Initial helper verification incorrectly compared raw CRLF text hashes; stopped before starting-state/archive writes. Corrected to reuse repository build_manifest for all nine runtime maps, preserving canonical text normalization and binary hashes. No runtime edits.",
            "Two read-only inspection snippets hit console/default-encoding or dictionary-slice errors; original files and all evidence preserved. Explicit UTF-8/ASCII-safe output used afterward.",
            "Parent PowerShell checkpoint serialized the first XML UTC fraction .210Z as .21Z; exact difference inspected. Comparison normalizes timestamp representation only; original receipt/XML/checkpoint bytes preserved.",
        ],
        "nativeOrVisualExecuted": False, "runtimePublished": False, "runtimeAccepted": False,
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "nextGate": load(BEFORE)["nextAction"],
        "limits": "HOST recovery evidence only. Parent-only scripts archived verbatim as historical evidence, NOT child recipes. No parent-lock access, new reviewer, native/font legibility, device, visual, integration, CI, immutable ZIP or publication acceptance. Original source/review/read-depth/viewport/OOM/denial/MLKit limits and all production/guest heap/archive guards remain. Whole project incomplete.",
    }
    save(EVIDENCE, evidence)
    history_preserved(state)
    print("Archived parent recovery, exact four passing named cases and original evidence; no tests rerun.")


def finish():
    state = load(PROGRESS)
    require(state["checkpoint"] == 571, "Checkpoint already advanced")
    head = git(CONTENT, "rev-parse", "HEAD")
    signed_clean(CONTENT, head)
    signed_clean(ANDROID, APP_HEAD)
    require(git(CONTENT, "rev-parse", "HEAD^") == START_HEAD, "Unexpected commit parent")
    changed = git(CONTENT, "diff", "--name-only", START_HEAD, head).splitlines()
    require(changed and all(p.startswith("docs/n1-reviews/batch-083-android-recovery/")
                            or p == "docs/n1-sources/execution-572.json" for p in changed),
            "Evidence commit contains out-of-scope changes")
    evidence = load(EVIDENCE)
    for item in evidence["provenance"]:
        require(digest(CONTENT.joinpath(*item["archive"].split("/"))) == item["sha256"],
                "Archived bytes changed")
    count = runtime()
    next_action = (
        "SAME083 recovered HOST gate signed/archived; do NOT rerun HOST or initial textual reviews absent new concern. "
        "Read docs/n1-sources/execution-572.json and original570/571 evidence; parent-only recovery scripts are historical, never child wrappers. "
        "NEXT bounded native preparation/checkpoint against exact signed Android1c1b7bf4 test-only harness atop frozen productionf9, full git archive through productionContentSyncONCE. "
        "All29Han/fourfonts/Paint/directPNG/legibility/lookalikes/selection/meaning/curatedreadings/drawing/articles/reciprocallinks/SystemBack/offline/persistence required; "
        "fresh local AND remote portownership includingTimeWait, explicitadbserial, ownedreadonlyAVD5580/5581 only; actual named terminal0 everycase/noskips/no-2/-3. HOSTinit NEVER for native. "
        "Original serial two-family dependent visual confirmations before current-main integration. "
        "Preserve complete parent nextAction in execution572 evidence.nextGate and every original acceptance/source/reviewer/process/read-depth/viewport/fallback/MLKit/OOM/denial limit. "
        "Current combined-main Python/validator/vocabulary/manifest/exact reviewed quizguards/original archive budgets, normally signed integration/ownerfastforward/exactremote/terminalgreenCI/everyimmutableZIPhash/terminalreceipts/ownerissue60 BEFORE084. "
        "Live runner owns runner.lock; children must NOT acquire/delete/unlock it. Approved control helpers and committed source packets only; no optional historicalsessionhelpers. "
        "Published109/1228,remaining1119/latestpublic21a5cb1328aadd437139a6b850f07298a2e2985d unchanged;083 not delivered. Physicalphone/generalrelease/whole-set outstanding."
    )
    checkpoint = {
        "schemaVersion": 1, "execution": 572, "checkpoint": 572, "batch": "083",
        "savedCommit": head, "signature": "G", "status": "continue",
        "stage": "recovered-host-android-signed-awaiting-native",
        "evidence": EVIDENCE.relative_to(CONTENT).as_posix(),
        "contentTestedCommit": START_HEAD, "androidHead": APP_HEAD,
        "freshTests": 4, "failures": 0, "skipped": 0, "freshAndroidAccepted": True,
        "hostChecksRerunByThisExecution": False, "runtimeManifestHashesVerified": count,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "nativeOrVisualExecuted": False, "nativeFontPending": ["\u51ab", "\u590c", "\u961d", "\u96b9"],
        "publishedAdditions": 109, "remainingAdditions": 1119, "lastPublishedCommit": PUBLIC_HEAD,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": next_action, "dedicatedWorktreesClean": True,
    }
    checkpoint["originalRootKeysCompared"] = history_preserved(state)
    checkpoint["allOriginalHistoricalRootValuesPreservedExactly"] = True
    state.update(checkpoint=572, status="continue", stage=checkpoint["stage"],
                 nextAction=next_action, blocker=None)
    state["execution572CoordinatorCheckpoint"] = checkpoint
    state["batch083RecoveredAndroidCheckpoint"] = checkpoint
    history_preserved(state)
    save(SUMMARY, checkpoint)
    update_progress(state)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    {"start": start, "archive": archive, "finish": finish}[sys.argv[1]]()
