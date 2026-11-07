import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "a4804907-57eb-4b63-854a-98f9c36f310d"
S = R / "docs" / "n1-sources"
HEAD = "6cb6b78defaccf57c57b790b514eafba98b2503d"
TEACHING = "4089e881d605ce92c4c425d57816bc795605ded8"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PREFIX = "batch-094-android-680-"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def heads(content=HEAD):
    for root, expected in ((R, content), (A, ANDROID)):
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain=v1", "--untracked-files=all"), str(root)


def persist(p):
    target = C / "progress.680.tmp"
    assert not target.exists()
    save(target, p)
    assert load(target) == p
    target.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
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
    assert count == 8438
    review = load(R / "docs" / "n1-reviews" / "batch-094-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    assert not git(R, "diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"runtimePayloadHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "manifestFreshAndUnchanged": True}


def next_action():
    return (
        "SAME094 bounded native/visual preparation and acceptance next on unchanged textually closed "
        "signed4089e881. Fresh680 sibling RealContentTest THREE and RareHanTest ONE passed, zero skips. "
        "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest app main. "
        "Run fresh " + load(L / "progress-before-680.json")["nextAction"].split("Then fresh ", 1)[1]
    )


def update_packet(e):
    path = S / "batch-094-progress.json"
    original = subprocess.check_output(
        ["git", "-C", str(R), "show", f"{HEAD}:docs/n1-sources/batch-094-progress.json"]
    ).decode("utf-8")
    packet = json.loads(original)
    limits = [
        value.replace("as do fresh non-skippedAndroid/RareHan, ", "as do ")
        for value in packet["limits"]
    ]
    updates = {
        "status": e["status"], "nextAction": e["nextAction"], "limits": limits,
        "pendingGates": packet["pendingGates"][1:],
    }
    assert packet["pendingGates"][0] == (
        "Fresh non-skipped THREE RealContentTest cases/ONE RareHanTest against actual sibling content.")
    for key, value in updates.items():
        match = re.search(r'^  "' + re.escape(key) + r'": ', original, re.MULTILINE)
        assert match, key
        _, end = json.JSONDecoder().raw_decode(original[match.end():])
        encoded = json.dumps(value, ensure_ascii=False, indent=2).replace("\n", "\n  ")
        original = original[:match.end()] + encoded + original[match.end() + end:]
    acceptance = {
        "execution": 680, "status": "passed", "evidence": "docs/n1-sources/execution-680.json",
        "totalTests": 4, "totalSkipped": 0, "nativeAcceptance": "pending", "runtimePublished": False,
    }
    assert "androidAcceptance" not in packet
    addition = json.dumps(acceptance, indent=2).replace("\n", "\n  ")
    original = original.rstrip()
    assert original.endswith("}")
    original = original[:-1].rstrip() + ',\n  "androidAcceptance": ' + addition + "\n}\n"
    expected = {**packet, **updates, "androidAcceptance": acceptance}
    assert json.loads(original) == expected
    path.write_bytes(original.encode("utf-8"))


def start():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (
        679, "094", "continue", "batch-094-textual-review-closed-awaiting-android-native")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    role = load(L / "android-runner-role.json")
    assert role["liveParentPid"] == 19008 and not role["lockTouched"]
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    frozen = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert frozen["checkpoint"] == 679
    assert frozen["execution679CoordinatorCheckpoint"]["savedCommit"] == HEAD
    baseline = L / "progress-before-680.json"
    assert not baseline.exists(), "Existing receipt must not be overwritten"
    checked = runtime()
    save(baseline, p)
    p["stage"] = "batch-094-fresh-host-android-checks-running"
    p["execution680StartingState"] = {
        "execution": 680, "batch": "094", "startingHead": HEAD, "androidHead": ANDROID,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME094 four fresh JVM cases and normally signed LOCAL evidence only; no native/reviewer/publication/095.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete issue and final679 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "artifactPathPreflight": "Approved control helpers, committed packets and frozen inputs only.",
        "runtime": checked, "status": "fresh-host-android-checks-running", "actualNewPermissionDenials": [],
        "diagnostics": ["Stopped own initial unbounded ancestry probe after verbose output; replaced by bounded verified launcher preflight. No lock operation or permission denial."],
    }
    persist(p)
    print("Starting680 persisted; all original history preserved.")


def collect():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["stage"]) == (679, "batch-094-fresh-host-android-checks-running")
    assert (L / "android-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    begin = datetime.fromisoformat((L / "android-start.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((L / "android-end.txt").read_text(encoding="utf-8-sig").strip())
    assert "BUILD SUCCESSFUL" in (L / "android.txt").read_text(encoding="utf-8-sig")
    checked = runtime()
    artifacts = []

    def archive(source, suffix):
        target = S / (PREFIX + suffix)
        assert not target.exists(), str(target)
        shutil.copyfile(source, target)
        record = {"archive": target.relative_to(R).as_posix(), "sha256": sha(target)}
        artifacts.append(record)
        return record

    tests = []
    for module, task, cls, names in (
        ("core", "test", "RealContentTest", {
            "parsesRealContentRepoWhenPresent", "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
            "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent"}),
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
    for source, suffix in (
        (L / "android.txt", "gradle-log.txt"), (L / "android-arguments.json", "gradle-arguments.json"),
        (L / "android-runner-role.json", "runner-role.json"),
        (C / "batch-065-host-integration-heap.init.gradle", "host-heap.init.gradle.txt"),
        (C / "run-680-android.ps1", "wrapper.ps1.txt"), (Path(__file__), "recipe.py"),
    ):
        archive(source, suffix)
    e = {
        "schemaVersion": 1, "execution": 680, "batch": "094", "status": "fresh-android-passed-awaiting-native",
        "contentTestedHead": HEAD, "teachingSnapshot": TEACHING,
        "androidTestedHead": ANDROID, "unchangedProductionAndroidHead": PRODUCTION,
        "androidQualification": "TESTONLY publishable fixture adjustment, not latest app main or production change.",
        "testOnlyDeltaPaths": changed, "actualResolvedContentRoot": str(R), "sourceProvenance": provenance,
        "tests": tests, "totalTests": 4, "totalSkipped": 0, "freshRun": True, "gradleExitCode": 0,
        "startedAt": begin.isoformat(), "completedAt": end.isoformat(), "artifacts": artifacts, "runtime": checked,
        "startingState": p["execution680StartingState"],
        "gradle": {"oneWorker": True, "noParallel": True, "rerunTasks": True, "kotlinCompiler": "in-process",
                   "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
                   "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
                   "coreHostHeap": "Existing approved 2g host-only init script; guest/app heap unchanged."},
        "textualReviewClosed": True, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newNativeOrPhoneClaimed": False, "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": p["lastPublishedCommit"], "wholeProjectComplete": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding", "nextAction": next_action(),
        "limits": ["Four fresh JVM cases only; native glyph/four-font/ContentSync/route and phone evidence not supplied.",
                   "Both original-model textual confirmations and all original review limitations retained, not new blind credit.",
                   "All native/current-main/publication gates remain. No runtime content change or publication."],
    }
    save(S / "execution-680.json", e)
    update_packet(e)
    print(json.dumps({"tests": tests, "runtime": checked}, indent=2))


def post():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    assert all(x.startswith("docs/n1-sources/") for x in git(R, "diff", "--name-only", HEAD, head).splitlines())
    e = load(S / "execution-680.json")
    body = (
        f"Batch 094 (\u524a): **fresh Android host gate passed; not published**. Normally signed local "
        f"evidence `{head}`; tested content `{HEAD}`, textually reviewed teaching `{TEACHING}`.\n\n"
        "Fresh RealContentTest **3 cases** and RareHanTest **1 case** passed with **zero skips, failures or errors**. "
        "Exact XML, signed-head sources, publishable fixture, Gradle log/arguments, live launcher ancestry "
        "and durable recipes are indexed by `docs/n1-sources/execution-680.json`. Both module paths resolve "
        "to the dedicated N1 content tree. Qualified TESTONLY Android `1c1b7bf4` retains production "
        "`f9b59a2`, not latest app main or a production change. One worker, in-process Kotlin and existing "
        "approved 2-GiB host-test heap; no guest/app heap, font production or archive-guard change.\n\n"
        f"All **8,438 runtime hashes** and manifest freshness reverified; contentVersion "
        f"`{e['runtime']['contentVersion']}`; teaching/runtime bytes unchanged. Both original model-session "
        "textual confirmations and all three direct word guards remain preserved, not new blind credit. "
        "JVM evidence is not native glyph/live-choice/phone acceptance. Next: SAME094 native/visual gate, "
        "all 41 scoped Han/four fonts (cmap absence of \u5202/\u65ab/\u6c35/\u961d is not glyph failure); "
        "actual N1/All production choices and three direct guards, only \u3055\u304f/\u3051\u305a\u308b "
        "reading keys, nine-stroke drawing, complete \u524a/\u524a\u308b/\u524a\u9664 and reciprocal "
        "\u9664 articles, System Back/offline, full production ContentSync once with terminal per-case 0. "
        "Both original reviewers still need bounded rendered confirmations.\n\n"
        "Current-main integration, combined checks, normal signing, owner fast-forward push, terminal CI, "
        "every immutable ZIP runtime hash and original budgets remain mandatory. Published **120/1,228; "
        "1,108 remaining**, unchanged. Physical-phone/general-release/whole-set acceptance outstanding. "
        "Checkpoint680 continues SAME094; no095, native/reviewer run or runtime push. Parent launcher retains "
        "runner.lock untouched; no optional historical helper access or new permission denial."
    )
    payload = C / (PREFIX + "issue-payload.json")
    receipt = C / (PREFIX + "issue-receipt.json")
    assert not payload.exists() and not receipt.exists()
    save(payload, {"body": body})
    env = os.environ.copy()
    env["GH_TOKEN"] = subprocess.check_output(["gh", "auth", "token", "--user", "stop-cran"], text=True).strip()
    try:
        assert env["GH_TOKEN"]
        assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], env=env, text=True).strip() == "stop-cran"
        posted = json.loads(subprocess.check_output(
            ["gh", "api", "repos/stop-cran/learning-japanese/issues/60/comments", "--method", "POST",
             "--input", str(payload)], env=env, text=True, encoding="utf-8"))
        save(C / (PREFIX + "issue-posted.json"), posted)
        verified = json.loads(subprocess.check_output(
            ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{posted['id']}"],
            env=env, text=True, encoding="utf-8"))
        assert verified["user"]["login"] == "stop-cran" and verified["body"] == body
        save(receipt, verified)
        print(verified["html_url"])
    finally:
        env.pop("GH_TOKEN", None)


def finalize():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    e = load(S / "execution-680.json")
    assert runtime() == e["runtime"]
    for record in e["artifacts"]:
        assert sha(R.joinpath(*record["archive"].split("/"))) == record["sha256"]
    receipt = load(C / (PREFIX + "issue-receipt.json"))
    assert receipt["user"]["login"] == "stop-cran" and head in receipt["body"]
    assert receipt["body"] == load(C / (PREFIX + "issue-payload.json"))["body"]
    baseline = load(L / "progress-before-680.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in baseline.items() if k not in allowed)
    checkpoint = {**e, "checkpoint": 680, "status": "continue", "stage": e["status"],
                  "savedCommit": head, "signature": "G", "dedicatedWorktreesClean": True,
                  "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
                  "allOriginalHistoricalValuesPreserved": True, "originalRootKeysCompared": len(baseline),
                  "evidence": "docs/n1-sources/execution-680.json"}
    p.update(checkpoint=680, status="continue", stage=e["status"], nextAction=e["nextAction"], blocker=None)
    p["execution680StartingState"]["status"] = "signed-local-android-checkpoint-complete"
    p["execution680CoordinatorCheckpoint"] = checkpoint
    p["batch094AndroidCheckpoint"] = copy.deepcopy(checkpoint)
    p["batch094AndroidIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": hashlib.sha256(receipt["body"].encode("utf-8")).hexdigest(), "verified": True,
    }
    persist(p)
    assert all(load(C / "progress.json")[k] == v for k, v in baseline.items() if k not in allowed)
    save(L / "batch-094-android-checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": 680, "savedCommit": head, "tests": 4, "skipped": 0,
                      "status": "continue", "allHistoricalValuesPreserved": True,
                      "issueUpdate": receipt["html_url"]}, indent=2))


if __name__ == "__main__":
    {"start": start, "collect": collect, "post": post, "finalize": finalize}[sys.argv[1]]()
