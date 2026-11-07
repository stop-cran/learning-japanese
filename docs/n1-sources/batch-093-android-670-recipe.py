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
L = C / "logs" / "6b227f64-839d-4b9f-a771-c90acdcf0d7c"
S = R / "docs" / "n1-sources"
HEAD = "fd260cf4a204c6874251cfb3ed9b0d78eb89e538"
TEACHING = "27663944c7217a19e7de2f363e1b31a5f13452b6"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PREFIX = "batch-093-android-670-"
NEXT = (
    "SAME093 bounded native/visual preparation and acceptance on unchanged textually closed "
    "teaching27663944. Fresh670 sibling RealContentTest THREE and RareHanTest ONE passed "
    "with zero skips. Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d "
    "retains productionf9b59a2, not latest app main. Inspect fresh device/port ownership; "
    "use an owned read-only API35 N3_Acceptance_20261029 emulator with approved hostGPU/"
    "Vulkan-disabled flags, 2048MiB/two cores and explicit serial; stop only owned helper. "
    "Preserve old fixtures. Full git archive through production ContentSync ONCE with actual "
    "imported counts/contentVersion/problems/acceptedRoom assertions and terminal per-case0; "
    "no reduced archive/import bypass/guest or app heap/guard increase. Inspect all46 scopedHan "
    "especially U+4E85/U+5202/U+5F61 across FOUR productionfont families/systemfallback; cmap "
    "absence is not glyphfailure. Exercise actualN1/All productionchoices, meaning, onlyon "
    "U+3051 U+3044/nokun keys, SIX pinned drawingstrokes, articles/SystemBack/offline and four "
    "direct police-label guards. Full rawケイ/emptykun retained; explicit[ケイ]/[] selects "
    "onlyけい through own linked existing N3刑事 row. Special whole-wordでか and outside-freeze "
    "ギョウ remain distinguished. One new刑card, no new support word; reused N3刑事 preserves "
    "identity/reading/title/level/inbound探偵guard and adds componentlink/four DIRECT guards only; "
    "事 adds reciprocal navigation only. Two allmapped pairs/four directions, one activated "
    "baseline刑/刑事 pair (not事/刑事); original GPT bookkeeping correction remains explicit. "
    "Original twofamily textualreview remains; reuse original sessions for dependentvisuals, "
    "no newblindcredit. Parent19008 retains runner.lock; NO child reacquisition/delete/unlock. "
    "Keep exactsignedheads/checkpoint/whollyclean/liveparent checks; preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. Approved controlhelpers/committedpackets/"
    "frozeninputs only, not optional historicalsessionrecipes. All original source/baseline/"
    "link/reading/twofamily/native/currentmain-normalmerge/substantiveteachingreview/combinedchecks/"
    "normal-signing/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original"
    "18000entries42MiBcompressed80MiBinflated56MiBretained/media/path/ownerissue gates remain. "
    "Published119/1228 and1109 acceptanceremainder unchanged; physicalphone/generalrelease/"
    "whole-set outstanding. No094, reviewer or runtimepublication in next bounded gate."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    target = C / "progress.670.tmp"
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
    assert count == 8436
    review = load(R / "docs" / "n1-reviews" / "batch-093-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    assert not git(R, "diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"runtimePayloadHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "manifestFreshAndUnchanged": True}


def start():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["stage"], p["status"]) == (
        669, "093", "textually-review-closed-awaiting-fresh-android", "continue")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert any(x["pid"] == 19008 and x["launcherCommandMatches"]
               for x in load(L / "android-runner-role.json"))
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    frozen = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert frozen["checkpoint"] == 669
    assert frozen["execution669CoordinatorCheckpoint"]["savedCommit"] == HEAD
    baseline = L / "progress-before-670.json"
    assert not baseline.exists(), "Existing receipt must not be overwritten."
    checked = runtime()
    save(baseline, p)
    p["stage"] = "fresh-host-android-checks-running"
    p["execution670StartingState"] = {
        "execution": 670, "batch": "093", "startingHead": HEAD, "androidHead": ANDROID,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME093 four fresh JVM cases and normally signed LOCAL evidence only; no native/reviewer/publication/094.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete issue and final669 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry and exact session; no child lock operation.",
        "artifactPathPreflight": "Approved workspace inputs, committed packets and durable control helpers only.",
        "runtime": checked, "status": "fresh-host-android-checks-running", "actualNewPermissionDenials": [],
    }
    persist(p)
    print("Starting670 persisted; full prior history preserved.")


def collect():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["stage"]) == (669, "fresh-host-android-checks-running")
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
        (C / "run-670-android.ps1", "wrapper.ps1.txt"), (Path(__file__), "recipe.py"),
    ):
        archive(source, suffix)
    e = {
        "schemaVersion": 1, "execution": 670, "batch": "093", "status": "fresh-android-passed-awaiting-native",
        "contentTestedHead": HEAD, "teachingSnapshot": TEACHING,
        "androidTestedHead": ANDROID, "unchangedProductionAndroidHead": PRODUCTION,
        "androidQualification": "TESTONLY publishable fixture adjustment, not latest app main or production change.",
        "testOnlyDeltaPaths": changed, "actualResolvedContentRoot": str(R), "sourceProvenance": provenance,
        "tests": tests, "totalTests": 4, "totalSkipped": 0, "freshRun": True, "gradleExitCode": 0,
        "startedAt": begin.isoformat(), "completedAt": end.isoformat(), "artifacts": artifacts, "runtime": checked,
        "request": p["execution670StartingState"]["request"],
        "gradle": {"oneWorker": True, "noParallel": True, "rerunTasks": True, "kotlinCompiler": "in-process",
                   "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
                   "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
                   "coreHostHeap": "Existing approved 2g host-only init script; guest/app heap unchanged."},
        "textualReviewClosed": True, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newNativeOrPhoneClaimed": False, "publishedAdditions": 119, "remainingAdditions": 1109,
        "lastPublishedCommit": p["lastPublishedCommit"], "wholeProjectComplete": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding", "nextAction": NEXT,
        "limits": ["Four fresh JVM cases only; native glyph/four-font/ContentSync/route and phone evidence not supplied.",
                   "All original textual review limitations and native/current-main/publication gates remain.",
                   "Parent launcher ancestry verified without touching runner.lock."],
    }
    save(S / "execution-670.json", e)
    packet = load(S / "batch-093-progress.json")
    packet.update(status=e["status"], nextAction=NEXT)
    packet["androidAcceptance"] = {
        "execution": 670, "status": "passed", "evidence": "docs/n1-sources/execution-670.json",
        "totalTests": 4, "totalSkipped": 0, "nativeAcceptance": "pending", "runtimePublished": False,
    }
    save(S / "batch-093-progress.json", packet)
    print(json.dumps({"tests": tests, "runtime": checked}, indent=2))


def post():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    assert all(x.startswith("docs/n1-sources/") for x in git(R, "diff", "--name-only", HEAD, head).splitlines())
    e = load(S / "execution-670.json")
    body = (
        f"Batch 093 (刑): **fresh Android host gate passed; not published**. Normally signed local evidence "
        f"`{head}`; tested content `{HEAD}`.\n\n"
        "Fresh RealContentTest **3 cases** and RareHanTest **1 case** passed with **zero skips, failures or errors**. "
        "Exact XML, signed-head sources, publishable fixture, Gradle log/arguments, live launcher ancestry "
        "and durable recipes are indexed by `docs/n1-sources/execution-670.json`. Both module paths resolve "
        "to the dedicated N1 content tree. Qualified TESTONLY Android `1c1b7bf4` is atop unchanged production "
        "`f9b59a2`, not latest app main or a production change. One worker, in-process Kotlin and existing "
        "approved 2-GiB host-test heap; no guest/app heap or archive-guard change.\n\n"
        f"All **8,436 runtime hashes** and manifest freshness reverified; contentVersion "
        f"`{e['runtime']['contentVersion']}`, teaching/runtime bytes unchanged. JVM evidence is not native glyph/"
        "phone acceptance. Next: SAME093 native/visual gate, all 46 scoped Han/four fonts, especially 亅/刂/彡; "
        "actual N1/All production choices and four direct police guards, only on けい/no kun keys, "
        "six-stroke drawing, articles/Back/offline, full production ContentSync once with terminal per-case 0. "
        "Original two-family textual closure, full ケイ/empty kun metadata, conservative explicit [ケイ]/[] "
        "selection and whole-word でか/outside-freeze ギョウ distinctions remain unchanged. No new support "
        "word; N3 刑事 preserves identity/primary reading/title/level/inbound 探偵 guard, adding only a "
        "component link/four direct guards; 事 adds reciprocal navigation. Two mapped pairs/four directions, "
        "one activated baseline 刑/刑事 pair; original report bookkeeping correction remains explicit.\n\n"
        "Current-main integration, combined checks, normal signing, owner fast-forward push, terminal CI, "
        "every immutable ZIP runtime hash and original budgets remain mandatory. Published **119/1,228; "
        "1,109 remaining**, unchanged. Physical-phone/general-release/whole-set acceptance outstanding. "
        "Checkpoint670 continues SAME093; no094, native/reviewer run or runtime push. Parent launcher retains "
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
    e = load(S / "execution-670.json")
    assert runtime() == e["runtime"]
    for record in e["artifacts"]:
        assert sha(R.joinpath(*record["archive"].split("/"))) == record["sha256"]
    receipt = load(C / (PREFIX + "issue-receipt.json"))
    assert receipt["user"]["login"] == "stop-cran" and head in receipt["body"]
    assert receipt["body"] == load(C / (PREFIX + "issue-payload.json"))["body"]
    baseline = load(L / "progress-before-670.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in baseline.items() if k not in allowed)
    checkpoint = {**e, "checkpoint": 670, "status": "continue", "stage": e["status"],
                  "savedCommit": head, "signature": "G", "dedicatedWorktreesClean": True,
                  "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
                  "allOriginalHistoricalValuesPreserved": True, "originalRootKeysCompared": len(baseline),
                  "evidence": "docs/n1-sources/execution-670.json"}
    p.update(checkpoint=670, status="continue", stage=e["status"], nextAction=NEXT, blocker=None)
    p["execution670StartingState"]["status"] = "signed-local-android-checkpoint-complete"
    p["execution670CoordinatorCheckpoint"] = checkpoint
    p["batch093AndroidCheckpoint"] = copy.deepcopy(checkpoint)
    p["batch093AndroidIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": hashlib.sha256(receipt["body"].encode("utf-8")).hexdigest(), "verified": True,
    }
    persist(p)
    assert all(load(C / "progress.json")[k] == v for k, v in baseline.items() if k not in allowed)
    save(L / "batch-093-android-checkpoint.json", checkpoint)
    print(json.dumps({"checkpoint": 670, "savedCommit": head, "tests": 4, "skipped": 0,
                      "status": "continue", "allHistoricalValuesPreserved": True,
                      "issueUpdate": receipt["html_url"]}, indent=2))


if __name__ == "__main__":
    {"start": start, "collect": collect, "post": post, "finalize": finalize}[sys.argv[1]]()
