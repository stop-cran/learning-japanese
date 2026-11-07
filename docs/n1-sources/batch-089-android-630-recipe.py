import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "90a27eb2-4ab1-4d8a-874b-533203017b0d"
S = R / "docs" / "n1-sources"
HEAD = "c9b92a7f18d457d623d2cdc7bff2fdd91a2bef10"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PREFIX = "batch-089-android-630-"


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


def persist(progress):
    target = C / "progress.630.tmp"
    assert not target.exists()
    save(target, progress)
    assert load(target) == progress
    target.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    count = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                path = R.joinpath(*name.split("/"))
                digest = sha(path) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                } else sha256(path)
                assert digest == expected, name
                count += 1
    assert count == 8426
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-089-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    for name, digest in reconciliation["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    assert not git(R, "diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"runtimePayloadHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "manifestFreshAndUnchanged": True}


def start():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["stage"], p["status"]) == (
        629, "089", "textually-review-closed-awaiting-fresh-android", "continue")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert any(x["pid"] == 19008 and x["launcherCommandMatches"]
               for x in load(L / "android-runner-role.json"))
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    frozen = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert frozen["checkpoint"] == 629
    assert frozen["execution629CoordinatorCheckpoint"]["savedCommit"] == HEAD
    baseline = L / "progress-before-630.json"
    assert not baseline.exists(), "Existing receipt must not be overwritten."
    checked = runtime()
    save(baseline, p)
    p["stage"] = "fresh-host-android-checks-running"
    p["execution630StartingState"] = {
        "execution": 630, "batch": "089", "startingHead": HEAD, "androidHead": ANDROID,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME089 four fresh JVM cases and normally signed LOCAL evidence only; no native/reviewer/publication/090.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete issue and final629 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry and exact session; no child lock operation.",
        "artifactPathPreflight": "Approved workspace inputs, committed packets and durable control helpers only.",
        "runtime": checked, "status": "fresh-host-android-checks-running",
        "actualNewPermissionDenials": [],
    }
    persist(p)
    print("Starting630 persisted; full prior history preserved.")


def collect():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["stage"]) == (629, "fresh-host-android-checks-running")
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
            "parsesRealContentRepoWhenPresent",
            "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
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
        (C / "run-630-android.ps1", "wrapper.ps1.txt"), (Path(__file__), "recipe.py"),
    ):
        archive(source, suffix)
    next_action = (
        "SAME089 bounded native/visual acceptance on unchanged textually closed teaching4b84608b. "
        "Execution630 fresh sibling RealContentTest THREE and RareHanTest ONE passed with zero skips. "
        "Qualified TESTONLY Android1c1b7bf4 atop unchanged productionf9b59a2 is not latest app main. "
        "Inspect fresh device/port ownership; use an owned read-only API35 N3_Acceptance_20261029 emulator "
        "with approved hostGPU/Vulkan-disabled flags, 2048MiB/two cores and explicit serial; stop only owned helper. "
        "Preserve old fixtures. Full git archive through production ContentSync ONCE with actual imported counts/"
        "contentVersion/problems/acceptedRoom assertions and terminal per-case0; no reduced archive, import bypass "
        "or guest/app heap/guard increase. Inspect all23 scopedHan especially U+4E42/U+51F5 across four production "
        "font families/system fallback; cmap absence is not glyph failure. Exercise actual N1/All production "
        "choices despite allthree curatedwrongcards being N1-available, meaning, singlequeuedkey U+304D U+3087 U+3046, "
        "fourstroke drawing, both new articles/SystemBack/offline routes, two allmappedpairs/four directions "
        "and one direct wordguard. Sole raw/selected on U+30AD U+30E7 U+30A6, rawkun[]/explicitquizkun[]; own "
        "linked U+51F6 U+4F5C row, noun/agriculturalverypooryield not harvestverb/necessaryzeroyield/famine/badwork, "
        "compound-specific modifier+head U+4F5C crop/yield. Original two-family textual review and its GPT "
        "redundant/truncated-tailread limitations remain; reuse original sessions for dependent visuals, no new "
        "blind credit. Parent19008 owns runner.lock; NO child reacquisition/delete/unlock. Keep exact signed-head/"
        "checkpoint/wholly-clean-worktree/live-parent checks; preserve/report/yield actual new denial, signinghang "
        "or uncertainownership. Approved control helpers/committed packets/frozen inputs only, not optional "
        "historical session recipes. All original source/baseline/link/reading/twofamily/native/currentmain-normalmerge/"
        "changed-teaching-independent-review/combinedchecks/normal-signing/owner-fastforward/terminalCI/"
        "EVERYimmutableZIPentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/media/safepath/"
        "ownerissue gates remain. Published115/1228,1113remaining unchanged; physicalphone/generalrelease/whole-set "
        "outstanding. No090, reviewer or runtime publication in next bounded gate."
    )
    e = {
        "schemaVersion": 1, "execution": 630, "batch": "089", "status": "fresh-android-passed-awaiting-native",
        "contentTestedHead": HEAD, "teachingSnapshot": "4b84608b5ca8889d45a176667975524f6645bd8d",
        "androidTestedHead": ANDROID, "unchangedProductionAndroidHead": PRODUCTION,
        "androidQualification": "TESTONLY publishable fixture adjustment, not latest app main or production change.",
        "testOnlyDeltaPaths": changed, "actualResolvedContentRoot": str(R), "sourceProvenance": provenance,
        "tests": tests, "totalTests": 4, "totalSkipped": 0, "freshRun": True, "gradleExitCode": 0,
        "startedAt": begin.isoformat(), "completedAt": end.isoformat(), "artifacts": artifacts, "runtime": checked,
        "request": p["execution630StartingState"]["request"],
        "gradle": {"oneWorker": True, "noParallel": True, "rerunTasks": True, "kotlinCompiler": "in-process",
                   "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
                   "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
                   "coreHostHeap": "Existing approved 2g host-only init script; guest/app heap unchanged."},
        "textualReviewClosed": True, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newNativeOrPhoneClaimed": False, "publishedAdditions": 115, "remainingAdditions": 1113,
        "lastPublishedCommit": p["lastPublishedCommit"], "wholeProjectComplete": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding", "nextAction": next_action,
        "limits": ["Four fresh JVM cases only; native glyph/four-font/ContentSync/route and phone evidence not supplied.",
                   "All original textual review limitations and native/current-main/publication gates remain.",
                   "Parent launcher ancestry verified without touching runner.lock."],
    }
    save(S / "execution-630.json", e)
    packet = load(S / "batch-089-progress.json")
    packet.update(status=e["status"], nextAction=next_action)
    packet["androidAcceptance"] = {"execution": 630, "status": "passed", "evidence": "docs/n1-sources/execution-630.json",
                                   "totalTests": 4, "totalSkipped": 0, "nativeAcceptance": "pending", "runtimePublished": False}
    save(S / "batch-089-progress.json", packet, ensure_ascii=False)
    print(json.dumps({"tests": tests, "runtime": checked}, indent=2))


def post():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    assert all(x.startswith("docs/n1-sources/") for x in git(R, "diff", "--name-only", HEAD, head).splitlines())
    receipt = C / (PREFIX + "issue-receipt.json")
    assert not receipt.exists()
    e = load(S / "execution-630.json")
    body = (
        f"Batch 089 (凶): **fresh Android host gate passed; not published**. Normally signed local evidence "
        f"`{head}`; tested content `{HEAD}`.\n\n"
        "Fresh RealContentTest **3 cases** and RareHanTest **1 case** passed with **zero skips, failures or errors**. "
        "Exact XML, signed-head sources, publishable fixture, Gradle log/arguments, live launcher ancestry "
        "and durable recipes are indexed by `docs/n1-sources/execution-630.json`. Both module paths resolve "
        "to the dedicated N1 content tree. Qualified TESTONLY Android `1c1b7bf4` is atop unchanged production "
        "`f9b59a2`, not latest app main or a production change. One worker, in-process Kotlin and existing "
        "approved 2-GiB host-test heap; no guest/app heap or archive-guard change.\n\n"
        f"All **8,426 runtime hashes** and manifest freshness reverified; contentVersion "
        f"`{e['runtime']['contentVersion']}`, teaching/runtime bytes unchanged. JVM evidence is not native glyph/"
        "phone acceptance. Next: SAME089 native/visual gate, all 23 scoped Han/four fonts/system fallback "
        "(especially 乂/凵), actual N1/All production choices, single queued きょう, four-stroke drawing, "
        "both new articles/Back/offline and full production ContentSync once with terminal per-case 0. "
        "Original two-family textual review, redundant/truncated GPT tail-read limitation, and source "
        "qualifications remain unchanged.\n\n"
        "Current-main integration, combined checks, normal signing, owner fast-forward push, terminal CI, "
        "every immutable ZIP runtime hash and original budgets remain mandatory. Published **115/1,228; "
        "1,113 remaining**, unchanged. Physical-phone/general-release/whole-set acceptance outstanding. "
        "Checkpoint630 continues SAME089; no090, native/reviewer run or runtime push. Parent launcher retains "
        "runner.lock untouched; no optional historical helper access or new permission denial."
    )
    save(C / (PREFIX + "issue-payload.json"), {"body": body})
    env = os.environ.copy()
    env["GH_TOKEN"] = subprocess.check_output(["gh", "auth", "token", "--user", "stop-cran"], text=True).strip()
    try:
        assert env["GH_TOKEN"]
        assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], env=env, text=True).strip() == "stop-cran"
        posted = json.loads(subprocess.check_output(
            ["gh", "api", "repos/stop-cran/learning-japanese/issues/60/comments", "--method", "POST",
             "--input", str(C / (PREFIX + "issue-payload.json"))], env=env, text=True, encoding="utf-8"))
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
    e = load(S / "execution-630.json")
    assert runtime() == e["runtime"]
    for record in e["artifacts"]:
        assert sha(R.joinpath(*record["archive"].split("/"))) == record["sha256"]
    receipt = load(C / (PREFIX + "issue-receipt.json"))
    assert receipt["user"]["login"] == "stop-cran" and head in receipt["body"]
    assert receipt["body"] == load(C / (PREFIX + "issue-payload.json"))["body"]
    baseline = load(L / "progress-before-630.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in baseline.items() if k not in allowed)
    checkpoint = {**e, "checkpoint": 630, "status": "continue", "stage": e["status"],
                  "savedCommit": head, "signature": "G", "dedicatedWorktreesClean": True,
                  "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
                  "allOriginalHistoricalValuesPreserved": True, "originalRootKeysCompared": len(baseline),
                  "evidence": "docs/n1-sources/execution-630.json"}
    p.update(checkpoint=630, status="continue", stage=e["status"], nextAction=e["nextAction"], blocker=None)
    p["execution630StartingState"]["status"] = "signed-local-android-checkpoint-complete"
    p["execution630CoordinatorCheckpoint"] = checkpoint
    p["batch089AndroidCheckpoint"] = copy.deepcopy(checkpoint)
    persist(p)
    assert all(load(C / "progress.json")[k] == v for k, v in baseline.items() if k not in allowed)
    save(L / "batch-089-android-checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": 630, "savedCommit": head, "tests": 4, "skipped": 0,
                      "status": "continue", "allHistoricalValuesPreserved": True,
                      "issueUpdate": receipt["html_url"]}, indent=2))


if __name__ == "__main__":
    {"start": start, "collect": collect, "post": post, "finalize": finalize}[sys.argv[1]]()
