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
LOG = CONTROL / "logs" / "483d3eeb-91f9-428c-881e-418300821fd9"
PROGRESS = CONTROL / "progress.json"
EVIDENCE = CONTENT / "docs" / "n1-sources" / "execution-549.json"
ARCHIVE = CONTENT / "docs" / "n1-reviews" / "batch-081-android"
INIT = CONTROL / "batch-065-host-integration-heap.init.gradle"
START_HEAD = "cbf4db9a98cfb47c780f9d7f1d43349c62dc189e"
TEACHING = "b7bf953d137251f179a57128bb84bd70a37737c8"
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
    "SAME081 bounded native fixture preparation/compile ONLY, persist/yield before "
    "device/emulator/reviewer/integration/publication/082; no second runner. "
    "Read execution-549.json, batch081 source/draft/font audits and textual reconciliation. "
    "Fresh HOST RealContentTest THREE and RareHanTest ONE passed with zero skips against "
    "THIS dedicated sibling/content tree; no rerun absent new concern. Prepare full signed "
    "Git archive through production ContentSync ONCE, no duplicate parse; assert actual "
    "imported counts/version/problems and Full+Lite full/curated raw readings, selected "
    "on key for 冶 and explicit empty kun list. Preserve full ヤ/い.る order and qualified "
    "source-only い.る; no invented 冶る or ジ allocation. Require seven-stroke drawing, "
    "actual N1 selection/meaning/curated-reading/articles/systemBack/offline, all29 actualHan "
    "and four production font families including pending 冫/氵 fallback labels; cmap absence "
    "is not glyph failure. HOST-only2GiBinit NEVER enters native builds; no app/guest heap "
    "or archiveguard change. Fresh device/port/PID ownership immediately before later approved "
    "read-onlyAPI35 launch; earlier5584override was batch-specific; stop only owned helper. "
    "Later terminal0 each native case, actualPNG inspection/two serial original-family visual "
    "confirmations, combined-current-main checks/non-rewriting integration/normal signing/"
    "ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets mandatory. Preserve "
    "textual closure on b7bf953d, complete original reports/process/read-depth/source limits, "
    "all baseline exceptions and FULL progress history. Approved workspace inputs/committed "
    "packets/durable control helpers only; optional historical session recipes skipped. "
    "Actual new denial or signinghang: preserve/report/yield without retry/workaround. "
    "Published107/1228,remaining1121; physicalphone/generalrelease/whole-set outstanding. "
    "CompatibleAndroidf9b59a2+ required; no unreviewed push or next batch."
)
sys.path.insert(0, str(CONTENT / "tools"))
from build_manifest import build_manifest


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".549.tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), "--no-pager", *args],
                                   text=True, encoding="utf-8").strip()


def runtime():
    manifest = read(CONTENT / "manifest.json")
    assert build_manifest(CONTENT) == manifest, "Manifest/runtime hash mismatch"
    count = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert count == 8369, count
    return {"manifestSha256": sha(CONTENT / "manifest.json"),
            "contentVersion": manifest["contentVersion"], "runtimeManifestHashesVerified": count}


def begin():
    original = read(PROGRESS)
    assert original["checkpoint"] == 548 and original["batch"] == "081"
    for root, head in [(CONTENT, START_HEAD), (ANDROID, ANDROID_HEAD)]:
        assert not git(root, "status", "--porcelain")
        assert git(root, "rev-parse", "HEAD") == head
        assert git(root, "log", "-1", "--format=%G?") == "G"
    assert sha(INIT) == "438159ae22b313e8196a0bc011f72a3b17300146b219c5ffcc779c540a64be24"
    raw = (LOG / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution548CoordinatorCheckpoint"]["savedCommit"] == START_HEAD
    write(LOG / "progress-before-549.json", original)
    state = {
        "schemaVersion": 1, "execution": 549, "batch": "081",
        "startingHead": START_HEAD, "teachingSnapshot": TEACHING, "androidHead": ANDROID_HEAD,
        "freshOriginMain": git(CONTENT, "rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME081 fresh HOST RealContentTest3+RareHanTest1, signed LOCAL evidence; yield before native/visual/integration/publication/082.",
        "authorization": {
            "requestSha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and embedded checkpoint parsed; operative contract, complete approved issue and final548 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "durableHelper": str(Path(__file__)), "optionalHistoricalHelpersAccessed": False,
            "actualNewPermissionDenials": [],
        },
        "qualifiedHostInit": {
            "path": str(INIT), "sha256": sha(INIT), "coreHostMaxHeap": "2g",
            "source": "docs/n1-sources/execution-540.json",
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
    write(LOG / "starting-state-549.json", state)
    original["execution549StartingState"] = state
    original["stage"] = "fresh-host-android-checks-running"
    original["nextAction"] = "SAME081 run/verify fresh HOST RealContentTest3+RareHanTest1; preserve signed LOCAL evidence, then yield before native/publication/082."
    write(PROGRESS, original)
    print(json.dumps({"stage": original["stage"], **runtime()}))


def collect():
    state = read(LOG / "starting-state-549.json")
    assert int((LOG / "android-exit.txt").read_text(encoding="utf-8-sig").strip()) == 0
    start = datetime.fromisoformat((LOG / "android-start.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((LOG / "android-end.txt").read_text(encoding="utf-8-sig").strip())
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    tests = []
    for module, task, name, cases in TESTS:
        source = ANDROID / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{name}.xml"
        xml = ET.parse(source).getroot()
        assert int(xml.attrib["tests"]) == len(cases)
        assert all(int(xml.attrib[k]) == 0 for k in ("skipped", "failures", "errors"))
        assert {c.attrib["name"] for c in xml.findall("testcase")} == cases
        timestamp = datetime.fromisoformat(xml.attrib["timestamp"].replace("Z", "+00:00"))
        assert start <= timestamp <= end and source.stat().st_mtime >= start.timestamp()
        assert all(c.find(tag) is None for c in xml.findall("testcase")
                   for tag in ("skipped", "failure", "error"))
        shutil.copyfile(source, ARCHIVE / source.name)
        assert sha(source) == sha(ARCHIVE / source.name)
        tests.append({**xml.attrib, "caseNames": sorted(cases), "sourcePath": str(source),
                      "archivedPath": (ARCHIVE / source.name).relative_to(CONTENT).as_posix(),
                      "sha256": sha(source), "freshTimestampAndMtimeVerified": True})
    provenance = []
    for name in ("android-command.txt", "android-start.txt", "android-end.txt", "android-exit.txt", "android.txt"):
        source = LOG / name
        shutil.copyfile(source, ARCHIVE / name)
        assert sha(source) == sha(ARCHIVE / name)
        provenance.append({"path": str(source),
            "archivedPath": (ARCHIVE / name).relative_to(CONTENT).as_posix(), "sha256": sha(source)})
    current = runtime()
    assert current["manifestSha256"] == state["manifestSha256"]
    assert not git(ANDROID, "status", "--porcelain")
    assert git(CONTENT, "rev-parse", "HEAD") == START_HEAD
    assert git(ANDROID, "rev-parse", "HEAD") == ANDROID_HEAD
    log = (LOG / "android.txt").read_text(encoding="utf-8-sig")
    assert "BUILD SUCCESSFUL" in log
    state.update({
        "status": "continue", "stage": "fresh-android-passed-awaiting-normal-signature",
        "actualStart": start.isoformat(), "completedAt": end.isoformat(), "exitCode": 0,
        "tests": tests, "exactNamedCasesVerified": 4, "rawAndArchivedProvenance": provenance,
        "logsAndXmlCopiedByteForByte": True,
        "command": (LOG / "android-command.txt").read_text(encoding="utf-8-sig").strip(),
        "oneWorker": True, "parallel": False, "rerunTasks": True, "inProcessCompiler": True,
        "buildResult": next(line for line in log.splitlines() if "BUILD SUCCESSFUL" in line),
        **current, "runtimeUnchanged": True, "noAndroidSourceChanges": True,
        "freshNativeOrVisualAcceptanceClaimed": False, "runtimePublished": False,
        "publishedAdditions": 107, "remainingAdditions": 1121,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "nextAction": NEXT,
        "limits": "Fresh HOST JVM3+1 only; not native rendering/fallback/drawing/visual, phone, publication or whole-set acceptance. No emulator/device launched, changed or inspected. Historical failures and original review limits preserved.",
        "diagnostics": [
            "Initial console summary hit cp1252 UnicodeEncodeError only after complete request load/checkpoint parse; final checkpoint subsequently read directly. No task mutation preceded it.",
            "Guessed prior batch080 provenance.json did not exist; authoritative committed execution-540.json and approved control helpers supplied the required precedent. No permission denial or missing mandatory input.",
        ],
        "helper": str(Path(__file__)), "helperSha256": sha(Path(__file__)),
        "runnerHelper": str(CONTROL / "run-549-android.ps1"),
        "runnerHelperSha256": sha(CONTROL / "run-549-android.ps1"),
    })
    implementations = [
        ANDROID / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "RealContentTest.kt",
        ANDROID / "app" / "src" / "test" / "java" / "io" / "github" / "stopcran" / "kanji" / "core" / "RareHanTest.kt", INIT,
    ]
    state["testImplementationsAndHostInit"] = [{"path": str(p), "sha256": sha(p)} for p in implementations]
    for source, target in [(Path(__file__), "execution-549-recipe.py"),
                           (CONTROL / "run-549-android.ps1", "run-549-android.ps1"),
                           (INIT, INIT.name)]:
        shutil.copyfile(source, ARCHIVE / target)
        assert sha(source) == sha(ARCHIVE / target)
    write(EVIDENCE, state)
    print(json.dumps({"buildResult": state["buildResult"], "cases": 4,
                      "runtimeHashesVerified": current["runtimeManifestHashesVerified"]}))


def finish():
    state = read(EVIDENCE)
    head = git(CONTENT, "rev-parse", "HEAD")
    assert git(CONTENT, "log", "-1", "--format=%G?") == "G"
    assert not git(CONTENT, "status", "--porcelain")
    assert not git(ANDROID, "status", "--porcelain")
    receipt = read(LOG / "issue-receipt.json")
    normalize = lambda s: s.replace("\r\n", "\n").strip()
    assert receipt["user"]["login"] == "stop-cran"
    assert normalize(receipt["body"]) == normalize((LOG / "issue-update.txt").read_text(encoding="utf-8-sig"))
    original = read(LOG / "progress-before-549.json")
    live = read(PROGRESS)
    assert live["checkpoint"] == 548
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(live[k] == v for k, v in original.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 549, "checkpoint": 549, "batch": "081",
        "savedCommit": head, "signature": "G", "status": "continue",
        "stage": "fresh-android-passed-awaiting-native-preparation", "teachingSnapshot": TEACHING,
        "evidence": EVIDENCE.relative_to(CONTENT).as_posix(), "exactNamedCasesVerified": 4,
        "tests": [{k: x[k] for k in ("name", "tests", "skipped", "failures", "errors")} for x in state["tests"]],
        "runtimeHashesReverified": runtime()["runtimeManifestHashesVerified"],
        "manifestUnchanged": True, "dedicatedWorktreesClean": True,
        "freshNativeOrVisualAcceptanceClaimed": False, "runtimePublished": False,
        "runtimeAccepted": False, "publishedAdditions": 107, "remainingAdditions": 1121,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(original), "nextAction": NEXT,
        "verifiedAt": datetime.now(timezone.utc).isoformat(),
    }
    live.update({"checkpoint": 549, "status": "continue", "stage": checkpoint["stage"],
                 "nextAction": NEXT, "blocker": None, "execution549CoordinatorCheckpoint": checkpoint})
    live["execution549StartingState"]["status"] = "signed-local-host-android-checkpoint-complete"
    live["batch081AndroidIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "receiptSha256": sha(LOG / "issue-receipt.json"),
        "localSignedAndroidCommit": head, "runtimePublished": False,
        "normalization": "GitHub CRLF normalized to LF; otherwise exact after terminal whitespace trim.",
    }
    write(PROGRESS, live)
    final = read(PROGRESS)
    assert all(final[k] == v for k, v in original.items() if k not in allowed)
    write(LOG / "checkpoint-549-verification.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


{"begin": begin, "collect": collect, "finish": finish}[sys.argv[1]]()
