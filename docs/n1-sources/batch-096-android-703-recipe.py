import copy
import gzip
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
L = C / "logs" / "08b808d4-2614-4321-a988-409013b92036"
S = R / "docs" / "n1-sources"
HEAD = "697ebc285a3a402095ce6c04da255eed247012d8"
TEACHING = "b26bcf9b328872b1575cf89e187973fea0a32a31"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PREFIX = "batch-096-android-703-"
STAGE = "batch-096-fresh-android-passed-awaiting-native"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


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
            assert not git(root, "status", "--porcelain=v1", "--untracked-files=all"), str(root)


def persist(p):
    target = C / "progress.703.tmp"
    assert not target.exists()
    save(target, p)
    assert load(target) == p
    target.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == "54645b95fe8e939c"
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
    assert count == 8444
    review = load(R / "docs" / "n1-reviews" / "batch-096-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    assert not git(R, "diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {
        "runtimePayloadHashesVerified": count, "contentVersion": manifest["contentVersion"],
        "manifestSha256": sha(R / "manifest.json"), "manifestFreshAndUnchanged": True,
    }


def next_action():
    previous = load(L / "progress-before-703.json")["nextAction"]
    return (
        "SAME096 native/visual preparation and acceptance next on unchanged textually closed signedb26bcf9b. "
        "Fresh703 sibling RealContentTest THREE and RareHanTest ONE passed, zero skips/failures/errors; "
        "this is host JVM acceptance ONLY, not native or full batch acceptance. "
        "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain. "
        "Run fresh " + previous.split("Then fresh ", 1)[1]
    )


def update_packet(e):
    path = S / "batch-096-progress.json"
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    packet = json.loads(text)
    assert packet["status"] == "batch-096-textual-review-closed-awaiting-android-native"
    assert packet["reviewClosed"] == packet["published"] == []
    assert packet["pendingGates"][0] == (
        "Fresh non-skipped THREE RealContentTest/ONE RareHanTest against actual sibling."
    )
    updates = {
        "status": STAGE,
        "nextAction": e["nextAction"],
        "limits": [
            item.replace(
                "Fresh non-skipped Android/native/four-font/all-Han/rendered review pending.",
                "Fresh four-case non-skipped JVM gate passed; native/four-font/all-Han/rendered review pending.",
            ) for item in packet["limits"]
        ],
        "pendingGates": packet["pendingGates"][1:],
    }
    for key, value in updates.items():
        matches = list(re.finditer(r'^  "' + re.escape(key) + r'": ', text, re.MULTILINE))
        assert len(matches) == 1, key
        match = matches[0]
        _, end = json.JSONDecoder().raw_decode(text[match.end():])
        encoded = json.dumps(value, ensure_ascii=True, indent=2).replace("\n", "\n  ")
        text = text[:match.end()] + encoded + text[match.end() + end:]
    acceptance = {
        "execution": 703, "status": "passed", "evidence": "docs/n1-sources/execution-703.json",
        "totalTests": 4, "totalSkipped": 0, "nativeAcceptance": "pending", "runtimePublished": False,
    }
    assert "androidAcceptance" not in packet
    text = text.rstrip()
    assert text.endswith("}")
    text = text[:-1].rstrip() + ',\n  "androidAcceptance": ' + json.dumps(
        acceptance, indent=2
    ).replace("\n", "\n  ") + "\n}\n"
    assert json.loads(text) == {**packet, **updates, "androidAcceptance": acceptance}
    path.write_bytes(text.replace("\n", newline).encode("utf-8"))


def start():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (
        702, "096", "continue", "batch-096-textual-review-closed-awaiting-android-native"
    )
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    role = load(L / "android-runner-role.json")
    assert role["liveParentPid"] == 19008 and not role["lockTouched"]
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    frozen = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert frozen["checkpoint"] == 702
    assert frozen["execution702CoordinatorCheckpoint"]["savedCommit"] == HEAD
    baseline = L / "progress-before-703.json"
    assert not baseline.exists(), "Existing receipt must not be overwritten"
    checked = runtime()
    save(baseline, p)
    p["stage"] = "batch-096-fresh-host-android-checks-running"
    p["execution703StartingState"] = {
        "execution": 703, "batch": "096", "startingHead": HEAD, "androidHead": ANDROID,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME096 four fresh JVM cases and normally signed LOCAL evidence only; no native/reviewer/publication/097.",
        "request": {
            "sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete approved issue and final702 directly inspected. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved control helpers, committed packets and frozen inputs only; no optional historical-session recipes accessed.",
        "runtime": checked, "status": "fresh-host-android-checks-running",
        "actualNewPermissionDenials": [],
    }
    persist(p)
    print("Starting703 persisted; all original history preserved.", flush=True)


def collect():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["stage"]) == (702, "batch-096-fresh-host-android-checks-running")
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
            "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent",
        }),
        ("app", "testDebugUnitTest", "RareHanTest", {"contentRareCharactersAreCoveredByBundledFont"}),
    ):
        source = A / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{cls}.xml"
        xml = ET.parse(source).getroot()
        assert int(xml.attrib["tests"]) == len(names)
        assert all(int(xml.attrib[k]) == 0 for k in ("skipped", "failures", "errors"))
        assert {x.attrib["name"] for x in xml.findall("testcase")} == names
        assert not any(
            x.find(t) is not None for x in xml.findall("testcase") for t in ("skipped", "failure", "error")
        )
        assert begin <= datetime.fromisoformat(xml.attrib["timestamp"]) <= end
        assert source.stat().st_mtime >= begin.timestamp()
        tests.append({
            **archive(source, module + ".xml"), "module": module, "class": xml.attrib["name"],
            "tests": len(names), "skipped": 0, "failures": 0, "errors": 0,
            "caseNames": sorted(names), "timestamp": xml.attrib["timestamp"],
        })
    provenance = []
    for name in (
        "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    ):
        source = A.joinpath(*name.split("/"))
        committed = subprocess.check_output(["git", "-C", str(A), "show", f"{ANDROID}:{name}"])
        assert source.read_bytes().replace(b"\r\n", b"\n") == committed.replace(b"\r\n", b"\n")
        provenance.append({
            **archive(source, source.name + ".txt"), "path": name, "exactSignedHeadSourceVerified": True,
        })
    for module in ("app", "core"):
        assert (A / module / ".." / ".." / "learning-japanese").resolve() == R
    subprocess.run(["git", "-C", str(A), "merge-base", "--is-ancestor", PRODUCTION, ANDROID], check=True)
    changed = git(A, "diff", "--name-only", PRODUCTION, ANDROID).splitlines()
    assert all(x.startswith(("core/src/test/", "docs/", ".github/")) for x in changed)
    for source, suffix in (
        (L / "android.txt", "gradle-log.txt"), (L / "android-arguments.json", "gradle-arguments.json"),
        (L / "android-runner-role.json", "runner-role.json"),
        (C / "batch-065-host-integration-heap.init.gradle", "host-heap.init.gradle.txt"),
        (C / "run-703-android.ps1", "wrapper.ps1.txt"), (Path(__file__), "recipe.py"),
    ):
        archive(source, suffix)
    e = {
        "schemaVersion": 1, "execution": 703, "batch": "096", "status": STAGE,
        "contentTestedHead": HEAD, "teachingSnapshot": TEACHING, "androidTestedHead": ANDROID,
        "unchangedProductionAndroidHead": PRODUCTION,
        "androidQualification": "TESTONLY publishable fixture adjustment, not latest app main or production change.",
        "testOnlyDeltaPaths": changed, "actualResolvedContentRoot": str(R), "sourceProvenance": provenance,
        "tests": tests, "totalTests": 4, "totalSkipped": 0, "freshRun": True, "gradleExitCode": 0,
        "startedAt": begin.isoformat(), "completedAt": end.isoformat(), "artifacts": artifacts, "runtime": checked,
        "startingState": p["execution703StartingState"],
        "gradle": {
            "oneWorker": True, "noParallel": True, "rerunTasks": True, "kotlinCompiler": "in-process",
            "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
            "coreHostHeap": "Existing approved 2g host-only init script; guest/app heap unchanged.",
        },
        "textualReviewClosed": True, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newNativeOrPhoneClaimed": False, "publishedAdditions": 122, "remainingAdditions": 1106,
        "lastPublishedCommit": p["lastPublishedCommit"], "wholeProjectComplete": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding", "nextAction": next_action(),
        "limits": [
            "Four fresh JVM cases only; native glyph/four-font/ContentSync/route and phone evidence not supplied.",
            "Original two-family textual review and its preserved coverage supplements/limitations remain, not new blind review credit.",
            "All native/current-main/publication gates remain. No runtime content change or publication.",
        ],
    }
    save(S / "execution-703.json", e)
    update_packet(e)
    print(json.dumps({"tests": tests, "runtime": checked}, indent=2))


def complete_collection():
    heads(clean=False)
    e = load(S / "execution-703.json")
    assert not git(A, "status", "--porcelain=v1", "--untracked-files=all")
    status = git(R, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    assert all(line.startswith("?? ") for line in status)
    assert {line[3:] for line in status} == {
        record["archive"] for record in e["artifacts"]
    } | {"docs/n1-sources/execution-703.json"}
    assert e["totalTests"] == 4 and e["totalSkipped"] == 0
    assert runtime() == e["runtime"]
    for record in e["artifacts"]:
        assert sha(R.joinpath(*record["archive"].split("/"))) == record["sha256"]
    original = S / (PREFIX + "recipe.py")
    preserved = S / (PREFIX + "original-collection-recipe.py.txt")
    assert not preserved.exists()
    update_packet(e)
    shutil.copyfile(original, preserved)
    shutil.copyfile(Path(__file__), original)
    for record in e["artifacts"]:
        if record["archive"] == original.relative_to(R).as_posix():
            record["sha256"] = sha(original)
    e["artifacts"].append({"archive": preserved.relative_to(R).as_posix(), "sha256": sha(preserved)})
    e["collectionDiagnostic"] = (
        "First collection verified and archived all four fresh passing XML cases, signed sources and "
        "runtime hashes, then stopped at a fail-closed assertion expecting the prior batch's pending-gate "
        "wording. Batch096 uses 'Fresh non-skipped THREE RealContentTest/ONE RareHanTest against actual "
        "sibling.' Corrected this exact string, preserved the original recipe, reverified every existing "
        "artifact and completed the ledger update. The first collection-completion attempt also stopped "
        "at an overly broad clean-worktree assertion because collection's own known untracked receipts "
        "existed; replaced with exact accounted receipt-set validation plus clean Android/unchanged "
        "signed heads/runtime requirements. No test rerun, acceptance waiver or runtime change."
    )
    save(S / "execution-703.json", e)
    print("Collection completed; original recipe and precise assertion diagnostic preserved.")


def seal_collection():
    heads(clean=False)
    assert not git(A, "status", "--porcelain=v1", "--untracked-files=all")
    e = load(S / "execution-703.json")
    assert runtime() == e["runtime"]
    path = S / "batch-096-progress.json"
    original = subprocess.check_output([
        "git", "-C", str(R), "show", f"{HEAD}:docs/n1-sources/batch-096-progress.json",
    ])
    before, after = json.loads(original), load(path)
    assert {key for key in before if before[key] != after[key]} == {
        "status", "limits", "nextAction", "pendingGates",
    }
    assert after.keys() - before.keys() == {"androidAcceptance"}
    assert after["reviewClosed"] == after["published"] == []
    assert original.count(b"\r\n") == original.count(b"\n")
    path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert load(path) == after
    recipe = S / (PREFIX + "recipe.py")
    shutil.copyfile(Path(__file__), recipe)
    for record in e["artifacts"]:
        if record["archive"] == recipe.relative_to(R).as_posix():
            record["sha256"] = sha(recipe)
        assert sha(R.joinpath(*record["archive"].split("/"))) == record["sha256"]
    save(S / "execution-703.json", e)
    expected = {record["archive"] for record in e["artifacts"]} | {
        "docs/n1-sources/execution-703.json", "docs/n1-sources/batch-096-progress.json",
    }
    status = git(R, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    assert {line[3:] for line in status} == expected
    subprocess.run(["git", "-C", str(R), "diff", "--check"], check=True)
    print("Sealed exact receipt set; original ledger CRLF and all unaffected fields preserved.")


def compress_log():
    e = load(S / "execution-703.json")
    raw = S / (PREFIX + "gradle-log.txt")
    target = raw.with_suffix(".txt.gz")
    assert not target.exists()
    data = raw.read_bytes()
    assert data == (L / "android.txt").read_bytes()
    matches = [record for record in e["artifacts"] if record["archive"] == raw.relative_to(R).as_posix()]
    assert len(matches) == 1 and matches[0]["sha256"] == sha(raw)
    target.write_bytes(gzip.compress(data, mtime=0))
    assert gzip.decompress(target.read_bytes()) == data
    matches[0].update(
        archive=target.relative_to(R).as_posix(), sha256=sha(target),
        uncompressedSha256=hashlib.sha256(data).hexdigest(),
    )
    raw.unlink()
    e["logPackaging"] = (
        "Exact Gradle stdout/stderr archived as deterministic gzip, preserving its original trailing "
        "whitespace after staged diff --check identified it. Original raw log remains in control. "
        "No normalization or loss of execution output."
    )
    save(S / "execution-703.json", e)
    print("Compressed exact raw Gradle log without modifying its bytes.")


def post():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    assert all(x.startswith("docs/n1-sources/") for x in git(R, "diff", "--name-only", HEAD, head).splitlines())
    e = load(S / "execution-703.json")
    body = (
        f"Batch 096 (\u525b): **fresh Android host gate passed; not published**. Normally signed local "
        f"evidence `{head}`; tested content `{HEAD}`, textually reviewed teaching `{TEACHING}`.\n\n"
        "Fresh RealContentTest **3 cases** and RareHanTest **1 case** passed with **zero skips, failures or errors**. "
        "Exact XML, signed-head sources, publishable fixture, Gradle log/arguments, verified live launcher ancestry "
        "and durable control recipes are indexed by `docs/n1-sources/execution-703.json`. Both module paths resolve "
        "to the dedicated N1 content tree. Qualified TESTONLY Android `1c1b7bf4` retains production `f9b59a2`, "
        "not latest app main or a production change. One worker, in-process Kotlin and existing approved "
        "2-GiB host-test heap; no guest/app heap, production font or archive-guard change.\n\n"
        f"All **8,444 runtime hashes** and manifest freshness reverified; contentVersion "
        f"`{e['runtime']['contentVersion']}`; teaching/runtime bytes unchanged. Both independent initial textual "
        "reviews and their preserved coverage supplements remain, not new review credit. JVM evidence is not "
        "native glyph, live-choice or phone acceptance. Next: SAME096 full-archive production ContentSync "
        "ONCE/native N1-All actual choices/twelve direct guards/only \u3054\u3046/no kun/ten-stroke drawing/"
        "complete \u525b and \u525b\u5065 articles/System Back/offline/all 28 scoped Han/four fonts; "
        "\u5182/\u5202 cmap absence is NOT glyph failure. Fresh safe port/device ownership checks and "
        "terminal per-case status 0 remain required. Both original model sessions still need serial "
        "bounded rendered confirmations.\n\n"
        "Current-main integration, combined checks, normal signing, owner fast-forward push, terminal CI, "
        "every immutable ZIP runtime hash and unchanged budgets remain mandatory. Published **122/1,228; "
        "1,106 remaining**, unchanged. Physical-phone/general-release/whole-set acceptance outstanding. "
        "Checkpoint703 continues SAME096; no097, native/reviewer run or runtime push. Parent launcher retains "
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
             "--input", str(payload)], env=env, text=True, encoding="utf-8"
        ))
        save(C / (PREFIX + "issue-posted.json"), posted)
        verified = json.loads(subprocess.check_output(
            ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{posted['id']}"],
            env=env, text=True, encoding="utf-8"
        ))
        assert verified["user"]["login"] == "stop-cran" and verified["body"] == body
        save(receipt, verified)
        print(verified["html_url"])
    finally:
        env.pop("GH_TOKEN", None)


def finalize():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    changed = git(R, "diff", "--name-only", HEAD, head).splitlines()
    assert changed and all(name.startswith("docs/n1-sources/") for name in changed)
    e = load(S / "execution-703.json")
    assert runtime() == e["runtime"]
    for record in e["artifacts"]:
        assert sha(R.joinpath(*record["archive"].split("/"))) == record["sha256"]
    receipt = load(C / (PREFIX + "issue-receipt.json"))
    assert receipt["user"]["login"] == "stop-cran" and head in receipt["body"]
    assert receipt["body"] == load(C / (PREFIX + "issue-payload.json"))["body"]
    baseline = load(L / "progress-before-703.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in baseline.items() if k not in allowed)
    checkpoint = {
        **e, "checkpoint": 703, "status": "continue", "stage": STAGE,
        "savedCommit": head, "signature": "G", "dedicatedWorktreesClean": True,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "allOriginalHistoricalValuesPreserved": True, "originalRootKeysCompared": len(baseline),
        "evidence": "docs/n1-sources/execution-703.json",
    }
    p.update(checkpoint=703, status="continue", stage=STAGE, nextAction=e["nextAction"], blocker=None)
    p["execution703StartingState"]["status"] = "signed-local-android-checkpoint-complete"
    p["execution703CoordinatorCheckpoint"] = checkpoint
    p["batch096AndroidCheckpoint"] = copy.deepcopy(checkpoint)
    p["batch096AndroidIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": hashlib.sha256(receipt["body"].encode("utf-8")).hexdigest(), "verified": True,
    }
    persist(p)
    assert all(load(C / "progress.json")[k] == v for k, v in baseline.items() if k not in allowed)
    save(L / "batch-096-android-checkpoint.json", checkpoint)
    print(json.dumps({
        "checkpoint": 703, "savedCommit": head, "tests": 4, "skipped": 0, "status": "continue",
        "allHistoricalValuesPreserved": True, "issueUpdate": receipt["html_url"],
    }, indent=2))


if __name__ == "__main__":
    {
        "start": start, "collect": collect, "complete-collection": complete_collection,
        "seal": seal_collection, "compress-log": compress_log, "post": post, "finalize": finalize,
    }[sys.argv[1]]()
