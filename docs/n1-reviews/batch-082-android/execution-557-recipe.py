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
LOG = CONTROL / "logs" / "38e9f6b1-840f-4b96-a789-8f4cd8f6448c"
PROGRESS = CONTROL / "progress.json"
ARCHIVE = CONTENT / "docs" / "n1-reviews" / "batch-082-android"
EVIDENCE = CONTENT / "docs" / "n1-sources" / "execution-557.json"
INIT = CONTROL / "batch-065-host-integration-heap.init.gradle"
HEAD = "e6e0eda2d365dda0a69752c6ab6acd5c2e83868e"
TEACHING = "b6bcc8f144cd781917abdb2ca510f663d1339a56"
ANDROID_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TESTS = [
    ("core", "test", "RealContentTest", {
        "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
        "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent",
        "parsesRealContentRepoWhenPresent",
    }),
    ("app", "testDebugUnitTest", "RareHanTest", {
        "contentRareCharactersAreCoveredByBundledFont",
    }),
]
NEXT = (
    "SAME082 blocked on fresh HOST RealContentTest.parsesRealContentRepoWhenPresent: Java heap OOM "
    "at RealContentTest.kt:119 with approved2GiB host init, both full3-case run and isolated1-case retry. "
    "Read execution-557.json and preserved batch-082-android attempt1/attempt2 XML/logs before action. "
    "Two other RealContentTest cases and RareHanTest passed fresh/non-skipped; required full-corpus "
    "case remains failed, not accepted. Investigate separately scoped Android test-harness prerequisite: "
    "the test walks ALL contributor docs (measured1,675,657,862bytes/10,582files) although production "
    "archives export-ignore these; mixed production-archive case passed. Do not delete/move evidence, "
    "omit runtime content, silently edit Android, increase approved host/guest heap or archiveguards, "
    "or repeat the failed command without a justified scoped remedy. Preserve all original reports/"
    "source/process/read-depth/denial/OOM limits and full progress history. No native fixture/device/"
    "reviewer/integration/publication or083 until host gate resolved. All31Han/fourfont native checks, "
    "including pending 冫/氵/辶/隹, terminal0 cases and two-family visual confirmations remain required; "
    "later combinedmain/normal signing/ownerfastforward/greenCI/everyZIPhash/originalbudgets unchanged. "
    "Textual closure b6bcc8f1 retained. Approved workspace source/control helpers only. "
    "Published108/1228,remaining1120; physicalphone/generalrelease/whole-set outstanding. "
    "CompatibleAndroidf9b59a2+ required; no second runner."
)
sys.path.insert(0, str(CONTENT / "tools"))
from build_manifest import build_manifest


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".557.tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), "--no-pager", *args],
                                   text=True, encoding="utf-8").strip()


def runtime():
    manifest = read(CONTENT / "manifest.json")
    assert build_manifest(CONTENT) == manifest
    count = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert count == 8372, count
    return {"manifestSha256": sha(CONTENT / "manifest.json"),
            "contentVersion": manifest["contentVersion"], "runtimeManifestHashesVerified": count}


def begin():
    progress = read(PROGRESS)
    assert progress["checkpoint"] == 556 and progress["batch"] == "082"
    for root, expected in [(CONTENT, HEAD), (ANDROID, ANDROID_HEAD)]:
        assert not git(root, "status", "--porcelain")
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
    assert sha(INIT) == "438159ae22b313e8196a0bc011f72a3b17300146b219c5ffcc779c540a64be24"
    raw = (LOG / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution556CoordinatorCheckpoint"]["savedCommit"] == HEAD
    write(LOG / "progress-before-557.json", progress)
    state = {
        "schemaVersion": 1, "execution": 557, "batch": "082",
        "startingHead": HEAD, "teachingSnapshot": TEACHING, "androidHead": ANDROID_HEAD,
        "freshOriginMain": git(CONTENT, "rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME082 fresh HOST RealContentTest3+RareHanTest1, signed LOCAL evidence; yield before native/visual/integration/publication/083.",
        "authorization": {
            "requestSha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and embedded checkpoint parsed; operative contract, complete issue and final556 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "durableHelper": str(Path(__file__)), "optionalHistoricalHelpersAccessed": False,
            "actualNewPermissionDenials": [],
        },
        "qualifiedHostInit": {
            "path": str(INIT), "sha256": sha(INIT), "coreHostMaxHeap": "2g",
            "source": "docs/n1-sources/execution-549.json",
            "original049512MiBOomAnd0651GiBOomPreserved": True,
            "guestProductionHeapOrArchiveGuardsChanged": False, "neverForNative": True,
        },
        "environment": {
            "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
        },
        "fixtureResolution": [], "preexistingReportsNotFreshAcceptance": [], **runtime(),
    }
    for module, task, name, _ in TESTS:
        resolved = (ANDROID / module / ".." / ".." / "learning-japanese").resolve()
        assert resolved == CONTENT
        state["fixtureResolution"].append({"workingDirectory": str(ANDROID / module),
            "relativeRoot": r"..\..\learning-japanese", "resolvedRoot": str(resolved)})
        report = ANDROID / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{name}.xml"
        state["preexistingReportsNotFreshAcceptance"].append({
            "path": str(report), "sha256": sha(report) if report.exists() else None})
    write(LOG / "starting-state-557.json", state)
    progress["execution557StartingState"] = state
    progress["stage"] = "fresh-host-android-checks-running"
    progress["nextAction"] = "SAME082 verify fresh HOST RealContentTest3+RareHanTest1; preserve signed LOCAL evidence then yield."
    write(PROGRESS, progress)
    print(json.dumps({"stage": progress["stage"], **runtime()}))


def collect():
    state = read(LOG / "starting-state-557.json")
    assert int((LOG / "android-exit.txt").read_text(encoding="utf-8-sig").strip()) == 0
    start = datetime.fromisoformat((LOG / "android-start.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((LOG / "android-end.txt").read_text(encoding="utf-8-sig").strip())
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    tests = []
    specifications = [
        (LOG / "android-attempt-1" / "TEST-io.github.stopcran.kanji.core.RealContentTest.xml",
         TESTS[0][3], 1, LOG / "android-attempt-1", "attempt-1"),
        (LOG / "android-attempt-2" / "TEST-io.github.stopcran.kanji.core.RealContentTest.xml",
         {"parsesRealContentRepoWhenPresent"}, 1, LOG / "android-attempt-2", "attempt-2"),
        (ANDROID / "app" / "build" / "test-results" / "testDebugUnitTest" /
         "TEST-io.github.stopcran.kanji.core.RareHanTest.xml",
         TESTS[1][3], 0, LOG, "rare-only"),
    ]
    for source, cases, failures, attempt_log, label in specifications:
        xml = ET.parse(source).getroot()
        assert int(xml.attrib["tests"]) == len(cases)
        assert all(int(xml.attrib[k]) == 0 for k in ("skipped", "errors"))
        assert int(xml.attrib["failures"]) == failures
        assert {c.attrib["name"] for c in xml.findall("testcase")} == cases
        timestamp = datetime.fromisoformat(xml.attrib["timestamp"].replace("Z", "+00:00"))
        attempt_start = datetime.fromisoformat((attempt_log / "android-start.txt").read_text(encoding="utf-8-sig").strip())
        attempt_end = datetime.fromisoformat((attempt_log / "android-end.txt").read_text(encoding="utf-8-sig").strip())
        assert attempt_start <= timestamp <= attempt_end
        if failures:
            failure = xml.find("testcase/failure")
            assert failure is not None and "OutOfMemoryError" in failure.attrib["type"]
            assert "RealContentTest.kt:119" in failure.text
        target = ARCHIVE / label / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        tests.append({**xml.attrib, "caseNames": sorted(cases), "sourcePath": str(source),
                      "archivedPath": target.relative_to(CONTENT).as_posix(),
                      "sha256": sha(source), "freshTimestampVerified": True,
                      "attempt": label, "caseResults": [
                          {"name": c.attrib["name"], "passed": c.find("failure") is None}
                          for c in xml.findall("testcase")]})
    provenance = []
    for directory, label in [(LOG / "android-attempt-1", "attempt-1"),
                             (LOG / "android-attempt-2", "attempt-2"), (LOG, "rare-only")]:
        for name in ("android-command.txt", "android-start.txt", "android-end.txt", "android-exit.txt", "android.txt"):
            source = directory / name
            target = ARCHIVE / label / name
            shutil.copyfile(source, target)
            assert sha(source) == sha(target)
            provenance.append({"path": str(source),
                "archivedPath": target.relative_to(CONTENT).as_posix(), "sha256": sha(source)})
    current = runtime()
    assert current["manifestSha256"] == state["manifestSha256"]
    assert not git(ANDROID, "status", "--porcelain")
    assert git(CONTENT, "rev-parse", "HEAD") == HEAD
    log = (LOG / "android.txt").read_text(encoding="utf-8-sig")
    assert "BUILD SUCCESSFUL" in log
    state.update({
        "status": "blocked", "stage": "blocked-fresh-android-host-heap",
        "actualStart": start.isoformat(), "completedAt": end.isoformat(), "exitCode": 0,
        "tests": tests, "distinctNamedCasesExecuted": 4, "distinctNamedCasesPassed": 3,
        "failedNamedCase": "parsesRealContentRepoWhenPresent",
        "failedAttempts": 2, "freshAndroidGatePassed": False,
        "rawAndArchivedProvenance": provenance,
        "logsAndXmlCopiedByteForByte": True,
        "command": (LOG / "android-command.txt").read_text(encoding="utf-8-sig").strip(),
        "oneWorker": True, "parallel": False, "rerunTasks": True, "inProcessCompiler": True,
        "buildResult": next(line for line in log.splitlines() if "BUILD SUCCESSFUL" in line),
        **current, "runtimeUnchanged": True, "noAndroidSourceChanges": True,
        "freshNativeOrVisualAcceptanceClaimed": False, "runtimePublished": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "nextAction": NEXT,
        "blocker": "Required full-corpus RealContentTest OOM at unchanged approved 2GiB, including isolated retry; no safe in-scope content remedy established. RareHanTest and other two real-content cases passed. Android harness prerequisite needs scoped resolution.",
        "heapInvestigation": {
            "readOnlyDocsFileCount": 10582, "readOnlyDocsBytes": 1675657862,
            "testBehavior": "RealContentTest.kt:117-119 reads ALL files except .git into a byte map, including contributor docs; at119 passes that map to ContentParser.",
            "evidenceBoundary": "Observed host OOM, not proof of production or native OOM. Contributor docs are export-ignored from runtime ZIP; completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent passed.",
            "isolationRetry": "Same approved2GiB, same whole input, failed method only; independently reproduced OOM. No further full-corpus retry.",
            "noHeapGuardOrSourceChanges": True,
        },
        "whitespaceDisposition": "docs/n1-reviews/batch-082-android/whitespace-disposition.json",
        "limits": "Fresh HOST three distinct passing cases and one failing full-corpus case across two attempts, zero skips; NOT Android gate acceptance. No native rendering/fallback/drawing/visual, phone, publication or whole-set acceptance. No emulator/device launched, changed or inspected. Historical failures and original review limits preserved.",
        "diagnostics": [
            "Initial console summary hit cp1252 UnicodeEncodeError after complete request load/checkpoint parse; final checkpoint subsequently read directly. No task mutation preceded it.",
            "Broad control file-name listing was oversized; narrowed to approved workspace helper execution-549.py and its committed evidence. No historical session helper accessed or new denial.",
        ],
        "helper": str(Path(__file__)), "helperSha256": sha(Path(__file__)),
        "runnerHelper": str(CONTROL / "run-557-android.ps1"),
        "runnerHelperSha256": sha(CONTROL / "run-557-android.ps1"),
    })
    implementations = [
        ANDROID / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "RealContentTest.kt",
        ANDROID / "app" / "src" / "test" / "java" / "io" / "github" / "stopcran" / "kanji" / "core" / "RareHanTest.kt", INIT,
    ]
    state["testImplementationsAndHostInit"] = [{"path": str(p), "sha256": sha(p)} for p in implementations]
    for source, target in [(Path(__file__), "execution-557-recipe.py"),
                           (CONTROL / "run-557-android.ps1", "run-557-android.ps1"),
                           (INIT, INIT.name)]:
        shutil.copyfile(source, ARCHIVE / target)
        assert sha(source) == sha(ARCHIVE / target)
    write(EVIDENCE, state)
    print(json.dumps({"status": state["status"], "distinctPassingCases": 3,
                      "fullCorpusOomAttempts": 2, **current}))


def finish():
    state = read(EVIDENCE)
    head = git(CONTENT, "rev-parse", "HEAD")
    assert head != HEAD and git(CONTENT, "log", "-1", "--format=%G?") == "G"
    assert not git(CONTENT, "status", "--porcelain")
    assert not git(ANDROID, "status", "--porcelain")
    receipt = read(LOG / "issue-receipt.json")
    normalize = lambda s: s.replace("\r\n", "\n").strip()
    assert receipt["user"]["login"] == "stop-cran"
    assert normalize(receipt["body"]) == normalize((LOG / "issue-update.txt").read_text(encoding="utf-8-sig"))
    assert runtime()["manifestSha256"] == state["manifestSha256"]
    progress = read(PROGRESS)
    original = read(LOG / "progress-before-557.json")
    assert progress["checkpoint"] == 556
    checkpoint = {
        "schemaVersion": 1, "execution": 557, "checkpoint": 557, "batch": "082",
        "savedCommit": head, "signature": "G", "teachingSnapshot": TEACHING,
        "status": "blocked", "stage": "blocked-fresh-android-host-heap",
        "evidence": EVIDENCE.relative_to(CONTENT).as_posix(),
        "distinctNamedCasesExecuted": 4, "distinctNamedCasesPassed": 3,
        "failedNamedCase": "parsesRealContentRepoWhenPresent", "failedAttempts": 2,
        "skipped": 0, "errors": 0, "freshAndroidGatePassed": False,
        "freshRuntimeHashesVerified": 8372, "runtimeUnchanged": True,
        "runtimePublished": False, "freshNativeOrVisualAcceptanceClaimed": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": "1f317f0762513720709ab0ca215f19ff021ca596",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": NEXT, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "dedicatedWorktreesClean": True,
    }
    checkpoint["blocker"] = state["blocker"]
    progress.update({"checkpoint": 557, "status": "blocked", "stage": checkpoint["stage"],
                     "nextAction": NEXT, "blocker": state["blocker"], "execution557CoordinatorCheckpoint": checkpoint})
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[k] == v for k, v in original.items() if k not in allowed)
    checkpoint["allOriginalHistoricalRootValuesPreservedExactly"] = True
    checkpoint["originalRootKeysCompared"] = len(original)
    write(PROGRESS, progress)
    reread = read(PROGRESS)
    assert all(reread[k] == v for k, v in original.items() if k not in allowed)
    write(LOG / "batch-082-android-checkpoint.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))


{"begin": begin, "collect": collect, "finish": finish}[sys.argv[1]]()
