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
P = C / "progress.json"
BEFORE = C / "execution-563-progress-before.json"
OUT = C / "artifacts" / "batch-082-corrected-host-563"
DEST = R / "docs" / "n1-reviews" / "batch-082-android" / "corrected-host-563"
EVIDENCE = R / "docs" / "n1-sources" / "execution-563.json"
HEAD = "e2b1ea6325bc705c5174c41f40a944baee5f6f64"
ANDROID_HEAD = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "d82e7fefe3898a70"
sys.path.insert(0, str(R / "tools"))
from build_manifest import build_manifest


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def now():
    return datetime.now(timezone.utc).isoformat()


def runtime():
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == VERSION
    count = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert count == 8372
    return {"contentVersion": VERSION, "runtimeHashesVerified": count,
            "manifestSha256": sha(R / "manifest.json")}


def history_check(current, before, allowed):
    changed = [key for key, value in before.items() if current.get(key) != value]
    assert not set(changed) - set(allowed), changed
    assert before.keys() <= current.keys()
    return changed


def start():
    p = load(P)
    assert p["checkpoint"] == 562 and p["status"] == "continue" and p["batch"] == "082"
    assert not BEFORE.exists() and not OUT.exists()
    for root, head in [(R, HEAD), (A, ANDROID_HEAD)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    request = C / "logs" / "a38577f2-72ab-48a1-baf7-3f8d47a091f6" / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    embedded = json.loads(text.split(marker, 1)[1])
    assert embedded["checkpoint"] == 562
    save(BEFORE, p)
    state = {
        "execution": 563, "batch": "082", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID_HEAD,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME082 corrected-runtime fresh HOST 3+1+5 only, signed local evidence and checkpoint; no native, reviewer, publication or083.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, complete issue and final562 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."
        },
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "dedicatedWorktreesInitiallyClean": True, **runtime()
    }
    p["execution563StartingState"] = state
    p["stage"] = "batch-082-corrected-runtime-host-running"
    p["nextAction"] = "SAME082 fresh corrected-runtime HOST RealContent3/RareHan1/loader5; archive exact command/XML, normally sign local evidence, checkpoint/yield. No native/reviewer/publication/083."
    history_check(p, load(BEFORE), ["stage", "nextAction"])
    save(P, p)
    save(C / "execution-563-start.json", state)
    print(json.dumps(state, ensure_ascii=True))


def archive():
    p = load(P)
    state = p["execution563StartingState"]
    assert p["checkpoint"] == 562 and not EVIDENCE.exists()
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == ANDROID_HEAD
    assert not git("status", "--porcelain", root=A)
    before_runtime = {k: state[k] for k in runtime()}
    assert runtime() == before_runtime
    receipt = load(OUT / "command.json")
    assert receipt["exitCode"] == 0
    assert receipt["contentHead"] == HEAD and receipt["androidHead"] == ANDROID_HEAD
    log = (OUT / "gradle.txt").read_text(encoding="utf-8-sig")
    assert "BUILD SUCCESSFUL" in log
    start_time = datetime.fromisoformat(receipt["startedAt"])
    tests = []
    for module, task, name, expected in [
        ("core", "test", "RealContentTest", 3),
        ("core", "test", "PublishableContentFixtureTest", 5),
        ("app", "testDebugUnitTest", "RareHanTest", 1),
    ]:
        source = A / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{name}.xml"
        copied = OUT / f"{name}.xml"
        assert copied.read_bytes() == source.read_bytes()
        suite = ET.parse(copied).getroot()
        assert int(suite.attrib["tests"]) == expected
        assert all(int(suite.attrib[k]) == 0 for k in ["failures", "errors", "skipped"])
        cases = suite.findall("testcase")
        assert len(cases) == expected
        assert not any(case.find(tag) is not None for case in cases for tag in ["skipped", "failure", "error"])
        timestamp = datetime.fromisoformat(suite.attrib["timestamp"].replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        assert timestamp >= start_time
        assert (A / module / ".." / ".." / "learning-japanese").resolve() == R
        tests.append({"name": suite.attrib["name"], "tests": expected, "failures": 0,
                      "errors": 0, "skipped": 0, "timestamp": suite.attrib["timestamp"],
                      "caseNames": [case.attrib["name"] for case in cases],
                      "sourcePath": str(source), "sha256": sha(copied)})
    artifacts = []
    for source in [*sorted(OUT.iterdir()), Path(__file__), C / "run-corrected-host-563.ps1",
                   C / "batch-065-host-integration-heap.init.gradle"]:
        assert source.is_file()
        target = DEST / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        assert not target.exists()
        shutil.copyfile(source, target)
        artifacts.append({"source": str(source), "archivedPath": target.relative_to(R).as_posix(),
                          "sha256": sha(target), "bytes": target.stat().st_size})
    evidence = {
        "schemaVersion": 1, **state, "completedAt": now(),
        "status": "fresh-corrected-host-passed-local-only",
        "stage": "batch-082-corrected-host-passed-awaiting-native-preparation",
        "correctionSnapshot": "9ce870d190d5c519d65ed20b118de64371350c0c",
        "qualifiedAndroidHead": ANDROID_HEAD,
        "originalProductionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "productionUnchanged": True, "hostHeap": "2g", "hostInitNeverForNative": True,
        "hostInitSha256": sha(C / "batch-065-host-integration-heap.init.gradle"),
        "actualGradleExit": 0, "tests": tests, "namedTests": 9,
        "buildResult": "BUILD SUCCESSFUL in 3m 12s",
        "tasks": "41 actionable tasks: 41 executed",
        "failuresErrorsSkips": 0, "fixtureRoot": str(R),
        "freshHostAcceptance": True, "freshNativeAcceptance": False,
        "independentVisualAcceptance": False, "runtimeBytesUnchanged": True,
        "runtimePublished": False, "reviewersLaunched": 0,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": [
            "HOST only for corrected d82e7fefe3898a70; no fresh native/pixel/drawing/routes/offline/phone acceptance.",
            "Qualified signed test-only Android loader delta retained; no newer production app behavior, heap increase or guard relaxation.",
            "All original source/reviewer/read-depth/citation/lookup/denial/OOM/process/viewport/fallback/MLKit limits remain; old native pixels are not corrected-runtime acceptance.",
            "No new blind initial review, publication, integration, CI, immutable ZIP or whole-set acceptance claimed.",
        ],
        "diagnostics": [
            "Initial checkpoint tail print hit cp1252 UnicodeEncodeError after full request load/parse. Repeated bounded UTF-8 output succeeded; no file changes or denial.",
            "A combined tail/current-state print exceeded tool output size; narrowed to final120 request lines and selected live root fields. Full request/checkpoint already loaded and parsed."
        ],
        "artifacts": artifacts, **runtime(),
        "nextAction": load(BEFORE)["nextAction"].replace(
            "SAME082 fresh qualified Android HOST gate on corrected signed runtime d82e7fefe3898a70 next, then persist/yield.",
            "SAME082 corrected-runtime fresh HOST3+1+5 passed at execution563. NEXT bounded corrected native-fixture/archive preparation and compile only, then persist/yield. Do not rerun HOST absent a new concern."
        ).replace(
            "Fresh RealContentTest3, RareHanTest1 and PublishableContentFixtureTest5, zero skips; actual sibling checkout and XML/command receipts.",
            "Fresh RealContentTest3, RareHanTest1 and PublishableContentFixtureTest5 VERIFIED execution563, zero skips; actual sibling checkout and XML/command receipts archived at docs/n1-reviews/batch-082-android/corrected-host-563."
        )
    }
    save(EVIDENCE, evidence)
    print(json.dumps({"evidence": str(EVIDENCE), "tests": tests, "runtime": runtime()}, ensure_ascii=True))


def checkpoint():
    p = load(P)
    before = load(BEFORE)
    evidence = load(EVIDENCE)
    saved = git("rev-parse", "HEAD")
    assert saved != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=A)
    assert runtime()["manifestSha256"] == evidence["manifestSha256"]
    receipt = load(C / "execution-563-issue-receipt.json")
    body = (C / "execution-563-issue-body.txt").read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").strip() == body
    result = {
        "schemaVersion": 1, "execution": 563, "checkpoint": 563, "batch": "082",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": evidence["stage"], "evidence": EVIDENCE.relative_to(R).as_posix(),
        "evidenceSha256": sha(EVIDENCE), **runtime(),
        "freshHostAcceptance": True, "namedHostTests": 9, "failuresErrorsSkips": 0,
        "freshNativeAcceptance": False, "independentVisualAcceptance": False,
        "runtimePublished": False, "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": p["lastPublishedCommit"], "dedicatedWorktreesClean": True,
        "runtimeBytesUnchanged": True, "reviewersLaunched": 0,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": evidence["nextAction"], "blocker": None
    }
    p.update({k: result[k] for k in ["checkpoint", "status", "stage", "nextAction", "blocker"]})
    p["execution563StartingState"]["status"] = "signed-local-corrected-host-checkpoint-complete"
    p["execution563CoordinatorCheckpoint"] = result
    p["batch082CorrectedRuntimeHost"] = result.copy()
    changed = history_check(p, before, ["checkpoint", "status", "stage", "nextAction", "blocker"])
    result["originalRootKeysCompared"] = len(before)
    result["allOriginalHistoricalRootKeysPreservedExactly"] = True
    result["changedRootFields"] = changed
    save(P, p)
    assert load(P) == p
    save(C / "execution-563-final-verification.json", result)
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    {"start": start, "archive": archive, "checkpoint": checkpoint}[sys.argv[1]]()
