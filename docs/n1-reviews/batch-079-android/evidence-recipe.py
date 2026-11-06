import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

CONTROL = Path(__file__).resolve().parent
CONTENT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOGS = CONTROL / "logs" / "7857506a-a446-4579-9f9f-ac206713bc8b"
PROGRESS = CONTROL / "progress.json"
BEFORE = CONTROL / "execution-532-progress-before.json"
START = CONTROL / "execution-532-start.json"
EVIDENCE = CONTENT / "docs" / "n1-sources" / "execution-532.json"
ARCHIVE = CONTENT / "docs" / "n1-reviews" / "batch-079-android"
HEAD = "084d5301d175189d6e83aa77666ae495abed6f47"
ANDROID_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
INIT = CONTROL / "batch-065-host-integration-heap.init.gradle"
SOURCES = [
    ANDROID / r"core\src\test\kotlin\io\github\stopcran\kanji\core\RealContentTest.kt",
    ANDROID / r"app\src\test\java\io\github\stopcran\kanji\core\RareHanTest.kt",
    INIT,
]
RESULTS = [
    ANDROID / r"core\build\test-results\test\TEST-io.github.stopcran.kanji.core.RealContentTest.xml",
    ANDROID / r"app\build\test-results\testDebugUnitTest\TEST-io.github.stopcran.kanji.core.RareHanTest.xml",
]
EXPECTED = [
    {"hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
     "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent",
     "parsesRealContentRepoWhenPresent"},
    {"contentRareCharactersAreCoveredByBundledFont"},
]
NEXT = (
    "SAME079 bounded native preparation/compile checkpoint ONLY, then persist/yield; "
    "no publication,080 or second runner. Read docs\\n1-sources\\execution-532.json, "
    "batch079TextualReview, batch079Draft and committed079 source/draft/reconciliation records. "
    "Fresh HOST RealContentTest THREE and RareHanTest ONE passed with zero skips against "
    "THIS dedicated sibling/content tree; do not rerun without new concern. Prepare full signed "
    "Git archive through production ContentSync ONCE, no duplicate preflight parse; assert "
    "actual imported counts/version/problems and Full+Lite full/curated raw readings and offered "
    "both reading keys for batch079. Use exact source/draft records for all35Han and exact two "
    "pending fallback labels, nine-stroke drawing, N1 selection/meaning/readings/articles/"
    "systemBack/offline and four production font families. Cmap absence is not a glyph failure. "
    "HOST-only2GiBinit NEVER enters native builds; no app/guest heap/archiveguard increase. "
    "Fresh device/port/PID ownership inspection before approved read-only API35 launch; "
    "batch0405584override was batch-specific. Stop only owned helper. Require terminal0 each "
    "native case/no skips/actual PNG inspection, then two serial original-family visual confirmations. "
    "Preserve textual closure at084d5301: two serial blind ClaudeOpus5.5/GPT6.1Sol initial reviews "
    "on0f7f20e9 and both original-session evidence confirmations;079-C1/079-G1 resolved evidence "
    "gaps, no teaching defect/change, seven optional suggestions.177distinctfamilies/fiverawrecords "
    "and all original read-depth/lookup/process limits retained. ContentVersiona01eb85b17601ac0; "
    "8363runtimehashes unchanged. Three mapped reciprocal pairs/six directions; one necessary "
    "new support article without inferred vocabulary level; preserved reused N2 identity/eightguards. "
    "Use committed packets/approvedcontrolinputs/durablecontrolhelpers; optional historicalsession "
    "recipes NOT required. Preserve FULL live history and all source/review/process/denial/OOM/phone "
    "limits and reviewed exceptions. Later currentmain non-rewriting integration/revalidation/normal "
    "signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets and verified ownerissue60 "
    "receipt remain mandatory. No unreviewedpush/authoragents/concurrentheavywork/secondrunner/"
    "signingretry/permissionworkaround. Preserve/report/yield on actualnewdenials. Published105/1228,"
    "remaining1123; local106thaddition textuallyclosednotpublished,1091kanji5047words111N1labels"
    "110namedmembers plus separate exception. CompatibleAndroidf9b59a2+ required; physicalphone/"
    "generalrelease/whole-set outstanding. Overallproject incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, encoding="utf-8").strip()


def inventory():
    return {name: sha(CONTENT / name)
            for section in load(CONTENT / "manifest.json").values() if isinstance(section, dict)
            for name in section if (CONTENT / name).is_file()}


def begin():
    assert not BEFORE.exists() and not START.exists()
    progress = load(PROGRESS)
    assert progress["checkpoint"] == 531 and progress["batch"] == "079"
    for root, head in ((CONTENT, HEAD), (ANDROID, ANDROID_HEAD)):
        assert git(root, "rev-parse", "HEAD") == head
        assert not git(root, "status", "--porcelain")
        assert git(root, "log", "-1", "--format=%G?") == "G"
    text = (LOGS / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 531
    state = {
        "execution": 532, "batch": "079", "startingHead": HEAD, "androidHead": ANDROID_HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME079 fresh HOST RealContentTest3+RareHanTest1, exact reports/provenance and normally signed local evidence; then yield. No native/review/publication/080/second runner.",
        "authorization": {
            "requestSha256": sha(LOGS / "request.txt"), "bytes": (LOGS / "request.txt").stat().st_size,
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, complete approved issue and final531 inspected directly; historical middle parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git(CONTENT, "rev-parse", "origin/main"),
        "manifestSha256": sha(CONTENT / "manifest.json"),
        "contentVersion": load(CONTENT / "manifest.json")["contentVersion"],
        "reconciliationSha256": sha(CONTENT / r"docs\n1-reviews\batch-079-reconciliation.json"),
        "testImplementationsAndHostInit": [{"path": str(p), "sha256": sha(p)} for p in SOURCES],
        "fixtureResolution": [
            {"workingDirectory": str(ANDROID / module), "relativeRoot": "..\\..\\learning-japanese",
             "resolvedRoot": str((ANDROID / module / ".." / ".." / "learning-japanese").resolve())}
            for module in ("core", "app")],
        "preexistingXmlNotFreshAcceptance": [{"path": str(p), "sha256": sha(p)} for p in RESULTS if p.exists()],
        "hostMemoryQualification": load(CONTENT / r"docs\n1-sources\execution-524.json")["hostMemoryQualification"],
        "environment": {"JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
                        "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk"},
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    assert all(row["resolvedRoot"] == str(CONTENT) for row in state["fixtureResolution"])
    assert sha(INIT) == state["hostMemoryQualification"]["qualifiedInitSha256"]
    shutil.copyfile(PROGRESS, BEFORE)
    save(START, state)
    save(CONTROL / "execution-532-runtime-before.json", inventory())
    progress["execution532StartingState"] = state
    progress["stage"] = "batch-079-fresh-android-running"
    progress["nextAction"] = "Finish SAME079 fresh HOST RealContentTest3+RareHanTest1; archive exact non-skipped XML/provenance, normal signed local evidence and yield. No native/review/publication/080."
    save(PROGRESS, progress)
    print("Starting scope persisted with full history and exact runtime baseline.")


def verify_runtime():
    assert git(ANDROID, "rev-parse", "HEAD") == ANDROID_HEAD
    assert not git(ANDROID, "status", "--porcelain")
    assert inventory() == load(CONTROL / "execution-532-runtime-before.json")
    assert sha(CONTENT / "manifest.json") == load(START)["manifestSha256"]
    assert load(START)["testImplementationsAndHostInit"] == [{"path": str(p), "sha256": sha(p)} for p in SOURCES]


def archive():
    verify_runtime()
    assert git(CONTENT, "rev-parse", "HEAD") == HEAD
    sys.path.insert(0, str(CONTENT / "tools"))
    from build_manifest import build_manifest
    assert build_manifest(CONTENT) == load(CONTENT / "manifest.json")
    assert (LOGS / "android-exit.txt").read_text().strip() == "0"
    started = datetime.fromisoformat((LOGS / "android-start.txt").read_text().strip())
    ARCHIVE.mkdir(exist_ok=False)
    tests = []
    for path, expected in zip(RESULTS, EXPECTED):
        root = ElementTree.parse(path).getroot()
        assert {case.attrib["name"] for case in root.findall("testcase")} == expected
        assert int(root.attrib["tests"]) == len(expected)
        assert all(int(root.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
        assert not any(root.findall(".//" + tag) for tag in ("skipped", "failure", "error"))
        assert datetime.fromisoformat(root.attrib["timestamp"].replace("Z", "+00:00")) >= started
        assert datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= started
        shutil.copyfile(path, ARCHIVE / path.name)
        assert sha(path) == sha(ARCHIVE / path.name)
        tests.append({**root.attrib, "caseNames": sorted(expected), "sourcePath": str(path),
                      "archivedPath": str((ARCHIVE / path.name).relative_to(CONTENT)), "sha256": sha(path)})
    provenance = []
    for name in ("android-command.txt", "android-start.txt", "android-end.txt", "android-exit.txt", "android.txt"):
        shutil.copyfile(LOGS / name, ARCHIVE / name)
        assert sha(LOGS / name) == sha(ARCHIVE / name)
        provenance.append({"path": str(LOGS / name), "archivedPath": str((ARCHIVE / name).relative_to(CONTENT)),
                           "sha256": sha(ARCHIVE / name)})
    log = (LOGS / "android.txt").read_text(encoding="utf-8-sig")
    assert "BUILD SUCCESSFUL" in log
    record = {
        **load(START), "schemaVersion": 1, "checkpoint": 532, "status": "continue",
        "stage": "fresh-android-passed-awaiting-normal-signature", "actualStart": started.isoformat(),
        "completedAt": (LOGS / "android-end.txt").read_text().strip(), "exitCode": 0,
        "tests": tests, "exactNamedCasesVerified": 4,
        "command": (LOGS / "android-command.txt").read_text().strip(),
        "oneWorker": True, "parallel": False, "rerunTasks": True, "inProcessCompiler": True,
        "coreHostMaxHeap": "2g", "hostInitNeverForNative": True,
        "buildResult": next(line for line in log.splitlines() if "BUILD SUCCESSFUL" in line),
        "rawAndArchivedProvenance": provenance, "logsAndXmlCopiedByteForByte": True,
        "runtimeManifestHashesVerified": len(inventory()), "manifestFresh": True,
        "runtimeUnchanged": True, "noAndroidSourceChanges": True,
        "freshNativeOrVisualAcceptanceClaimed": False, "runtimePublished": False,
        "publishedAdditions": 105, "remainingAdditions": 1123, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "limits": "Fresh HOST JVM3+1 only; not native rendering/fallback/drawing/visual, phone, publication or whole-set acceptance. No device/emulator launched, changed or inspected. Historical failures and original review limitations preserved.",
        "helper": str(Path(__file__)), "helperSha256": sha(Path(__file__)),
        "runnerHelper": str(CONTROL / "run-532-android.ps1"),
        "runnerHelperSha256": sha(CONTROL / "run-532-android.ps1"),
    }
    shutil.copyfile(Path(__file__), ARCHIVE / "evidence-recipe.py")
    shutil.copyfile(CONTROL / "run-532-android.ps1", ARCHIVE / "run-android.ps1")
    save(EVIDENCE, record)
    print("Four fresh exact named cases passed with zero skips; XML/logs archived.")


def finish():
    verify_runtime()
    commit = git(CONTENT, "rev-parse", "HEAD")
    assert git(CONTENT, "log", "-1", "--format=%G?") == "G"
    assert not git(CONTENT, "status", "--porcelain")
    assert git(CONTENT, "diff", HEAD, commit, "--", "manifest.json", "kanji", "words", "articles", "strokes") == ""
    receipt = load(CONTROL / "batch-079-android-issue-receipt.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (CONTROL / "batch-079-android-issue-body.txt").read_text(encoding="utf-8")
    progress, original = load(PROGRESS), load(BEFORE)
    changed = {"checkpoint", "stage", "nextAction"}
    for key, value in original.items():
        if key not in changed:
            assert progress[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 532, "checkpoint": 532, "batch": "079",
        "savedCommit": commit, "signature": "G", "status": "continue",
        "stage": "fresh-android-passed-awaiting-native-preparation",
        "evidence": "docs/n1-sources/execution-532.json", "androidHead": ANDROID_HEAD,
        "freshTests": 4, "skipped": 0, "failures": 0, "errors": 0,
        "runtimeHashesVerified": len(inventory()), "contentVersion": load(START)["contentVersion"],
        "runtimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "runtimePublished": False, "publishedAdditions": 105, "remainingAdditions": 1123,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "originalRootKeyCountCompared": len(original), "changedRootFields": sorted(changed),
        "nextAction": NEXT, "verifiedAt": datetime.now(timezone.utc).isoformat(),
    }
    progress.update(checkpoint=532, stage=checkpoint["stage"], nextAction=NEXT)
    progress["execution532CoordinatorCheckpoint"] = checkpoint
    progress["batch079Android"] = checkpoint.copy()
    save(PROGRESS, progress)
    final = load(PROGRESS)
    assert all(final[k] == v for k, v in original.items() if k not in changed)
    save(CONTROL / "execution-532-checkpoint.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))


{"begin": begin, "archive": archive, "finish": finish}[sys.argv[1]]()
