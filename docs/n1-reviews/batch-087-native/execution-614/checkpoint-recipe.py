import copy
import gzip
import hashlib
import json
import subprocess
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "be17e4ac-5fa9-424a-8243-595b899ce914"
HEAD = "243e504acfccddb7760e4108b6cd0dce2f0bfd9a"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
BEFORE = L / "progress-before-614.json"
ATTEMPT = C / "artifacts" / "batch-087-native-attempt-614"
NEXT = (
    "SAME087 serial dependent visual confirmations using ORIGINAL Claude session2308e256-e5c9-494d-8e53-805f94ff6314 "
    "then ORIGINAL GPT sessiond08a2c70-c89c-4b1f-a38c-311b6245ad29, actual installed CLI catalog/tool support and "
    "one active read-only reviewer at a time; wait for process exit and preserve complete actual reports/limits. "
    "No new blind initial-review credit. Read docs/n1-sources/execution-614.json and docs/n1-reviews/batch-087-native/"
    "execution-614/visual-inspection.json, original reports/reconciliation and actual PNGs. Teaching f6391022 unchanged. "
    "Both compiled087 native cases terminal0/no skips, full archive404f507d through productionContentSyncONCE "
    "1110kanji/5066words/119N1/zeroProblems/versioneb3a9413cccd4f57/acceptedepoch1. All21Han especially U+51E0 "
    "actually visible in fourfamily Compose panels; 84+8 Paint hash probes are NOT separately exported/viewed PNGs. "
    "55 actual screenshots inspected via ten full-frame contact sheets plus full-size font panels; original captures preserved. "
    "Actual N1 default fallback柚 yuzu citrus and seed613栗 chestnut unambiguous beside凹/凡; N4風 excluded, All includes風. "
    "Both queuedkunkeysなぎ/なぐ Good/done, expliciton[], sixstroke injectedtrace/recall/Again, all3articleprojections/"
    "twopairs/fourdirections/sevendirectguards/SystemBack/offline. OwnedreadonlyAPI35 emulator5580 parent22056/qemu6448 "
    "stopped and no devices afterward. Injectedtrace/giveup not humanhandwriting/MLKit/phone. QualifiedTESTONLYAndroid1c1b7bf4 "
    "retains productionf9b59a2, not latest app main. Keep modernweather凪ぐ versus feelings和ぐ/classicalforms separate. "
    "Parent19008 ownsrunner.lock; verify live ancestry/session/exactcheckpoint/signedheads/whollycleanworktrees; "
    "NOchildreacquisition/delete/unlock. Approvedcontrol/committedsources only, no optionalhistoricalsessionhelpers. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Alloriginalsource/baseline/link/reading/twofamily/"
    "native/currentmainnormalmerge/changedteachingindependentreview/combinedchecks/normalsigning/ownerfastforward/"
    "terminalCI/EVERYimmutablepublicZIPruntimehash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/ownerissue gates remain. No088/publication/productionappchange/heaporguardincrease. "
    "Published113/1228,1115remaining unchanged; physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    assert manifest["contentVersion"] == "eb3a9413cccd4f57"
    count = 0
    with zipfile.ZipFile(load(C / "batch-087-native-fixture-verification.json")["archive"]) as archive:
        names = archive.namelist()
        prefix = next(name[:-len("manifest.json")] for name in names if name.endswith("manifest.json"))
        assert json.loads(archive.read(prefix + "manifest.json")) == manifest
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, expected in entries.items():
                path = R.joinpath(*name.split("/"))
                actual = sha(path) if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(path)
                assert actual == expected, name
                data = archive.read(prefix + name)
                if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == expected, name
                count += 1
    assert count == 8420
    return {"runtimeHashesVerified": count, "manifestSha256": sha(R / "manifest.json"),
            "contentVersion": manifest["contentVersion"], "archiveManifestEqual": True}


def persist(state):
    path = C / "progress.614.tmp"
    assert not path.exists()
    save(path, state)
    assert load(path) == state
    path.replace(C / "progress.json")


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        613, "continue", "native-prepared-compiled-not-executed", "087")
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["execution613CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert not BEFORE.exists()
    verified = runtime()
    save(BEFORE, state)
    state["execution614StartingState"] = {
        "execution": 614, "batch": "087", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME087 compiled native execution and actual image inspection; signed LOCAL evidence/checkpoint only. No reviewer/publication/088.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Full request loaded and checkpoint JSON decoded; operative contract, approved issue and final613 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Committed source packets and approved control artifacts only; optional historical session helpers not accessed.",
        "runtime": verified, "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-087-native-execution-in-progress"
    persist(state)
    print("Starting614 persisted with full historical state; 8420 current and frozen-archive hashes verified.")


def sheets():
    from PIL import Image, ImageDraw
    folder = ATTEMPT / "inspection"
    assert not folder.exists()
    folder.mkdir()
    files = sorted(ATTEMPT.glob("*.png"))
    assert len(files) == 55
    mapping = []
    for offset in range(0, len(files), 6):
        selected = files[offset:offset + 6]
        sheet = Image.new("RGB", (1500, 2260), "white")
        draw = ImageDraw.Draw(sheet)
        rows = []
        for position, path in enumerate(selected):
            x = (position % 3) * 500
            y = (position // 3) * 1130
            with Image.open(path) as image:
                image = image.convert("RGB")
                image.thumbnail((500, 1100))
                sheet.paste(image, (x, y + 30))
            draw.text((x + 4, y + 4), f"{offset + position + 1}: {path.name}", fill="black")
            rows.append({"original": path.name, "sha256": sha(path), "position": position})
        path = folder / f"contact-{offset // 6 + 1:02}.png"
        sheet.save(path)
        mapping.append({"sheet": path.name, "sha256": sha(path), "originals": rows})
    save(folder / "contact-map.json", mapping)
    print("55 original screenshots retained; 10 contact sheets generated for actual inspection.")


def collect():
    clean()
    verified = runtime()
    result = load(C / "batch-087-native-attempt-614-execution.json")
    assert result["passed"] and result["terminalSuccessCases"] == 2 and result["adbExitCode"] == 0
    assert result["ownedHelperStopped"] and result["ownedQemuStopped"]
    assert not result["parentLockTouched"] and not result["guestOrAppHeapChanged"] and not result["guardsChanged"]
    route = load(ATTEMPT / "n1-087-article-route.json")
    assert (route["archiveRequests"], route["importedKanji"], route["importedWords"], route["n1Cards"],
            route["problems"], route["acceptedReadingParserEpoch"]) == (1, 1110, 5066, 119, 0, 1)
    assert route["passed"] and route["offline"] and route["bothCuratedKunKeysPersistedGoodAndDone"]
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"], route["directWordGuardCount"],
            route["completeArticleProjections"], route["touchInjectedReferenceStrokes"]) == (2, 4, 7, 3, 6)
    glyph = load(ATTEMPT / "n1-087-font-raster.json")
    assert (glyph["individualGlyphProbes"], glyph["wholeWordRasterProbes"], glyph["panels"]) == (84, 8, 2)
    assert len(glyph["rows"]) == 92
    raw = (ATTEMPT / "instrumentation.txt").read_text(encoding="utf-8-sig")
    for name in ["N1Batch087ArticleTest", "N1Batch087GlyphTest"]:
        assert name in raw
    assert raw.count("INSTRUMENTATION_STATUS_CODE: 0") == 2 and "OK (2 tests)" in raw
    folder = R / "docs" / "n1-reviews" / "batch-087-native" / "execution-614"
    assert not folder.exists()
    folder.mkdir()
    receipts = []
    for path in sorted(ATTEMPT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ATTEMPT)
        destination = folder / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".txt":
            destination = destination.with_suffix(".txt.gz")
            data = path.read_bytes()
            destination.write_bytes(gzip.compress(data, mtime=0))
            assert gzip.decompress(destination.read_bytes()) == data
        else:
            shutil.copyfile(path, destination)
            assert sha(path) == sha(destination)
        receipts.append({"source": str(path), "archive": destination.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "archiveSha256": sha(destination)})
    for name, destination in [
        ("run-614-native.ps1", "run-614-native.ps1"),
        ("batch-087-native-614.py", "checkpoint-recipe.py"),
        ("batch-087-native-614-visual-inspection.json", "visual-inspection.json"),
    ]:
        shutil.copyfile(C / name, folder / destination)
        receipts.append({"source": str(C / name), "archive": (folder / destination).relative_to(R).as_posix(),
                         "sourceSha256": sha(C / name), "archiveSha256": sha(folder / destination)})
    inspection = load(C / "batch-087-native-614-visual-inspection.json")
    evidence = {
        "schemaVersion": 1, "execution": 614, "batch": "087",
        "status": "native-passed-coordinator-inspected-awaiting-independent-visual-confirmations",
        "contentTestedHead": result["contentSnapshot"], "coordinatorStartingHead": HEAD, "androidTestedHead": APP,
        "teachingSnapshot": "f6391022356073dd3e53437be30885f9a09857d9",
        "qualifiedAppBaseline": "TESTONLY Android1c1b7bf4 retains unchanged productionf9b59a2; not latest app main.",
        "startingState": load(C / "progress.json")["execution614StartingState"],
        "executionReceipt": result, "nativeRoute": route,
        "glyphProbes": {"individual": 84, "wholeWord": 8, "rows": 92, "actualComposePanelsViewed": 2},
        "visualInspection": inspection, "receipts": receipts, "runtime": verified,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "textualReviewClosed": True, "independentVisualConfirmationsComplete": False,
        "newIndependentReviewersLaunched": 0, "newPhoneClaimed": False,
        "publishedAdditions": 113, "remainingAdditions": 1115,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False, "nextAction": NEXT,
    }
    save(R / "docs" / "n1-sources" / "execution-614.json", evidence)
    save(C / "batch-087-native-614-evidence.json", evidence)
    print("Native614 receipts, 55 originals, contact sheets and bounded inspection archived; runtime unchanged.")


def finalize():
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD
    clean(saved)
    evidence = load(R / "docs" / "n1-sources" / "execution-614.json")
    for receipt in evidence["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    verified = runtime()
    receipt = load(C / "batch-087-native-614-issue-receipt.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (C / "batch-087-native-614-issue-body.txt").read_text(encoding="utf-8")
    state = load(C / "progress.json")
    before = load(BEFORE)
    assert state["checkpoint"] == 613 and state["stage"] == "batch-087-native-execution-in-progress"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 614, "checkpoint": 614, "batch": "087",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmations",
        "evidence": "docs/n1-sources/execution-614.json", "runtime": verified,
        "nativeCases": 2, "terminalCaseSuccesses": 2, "skips": 0,
        "screenshotsActuallyInspected": 55, "actualComposeFontPanelsViewed": 2,
        "nativePaintHashProbes": 92, "separatePaintPngsViewed": 0,
        "independentVisualConfirmationsComplete": False, "runtimeAccepted": False,
        "runtimeChanged": False, "runtimePublished": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "ownedHelperStopped": True, "ownedQemuStopped": True,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 113, "remainingAdditions": 1115,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update({"checkpoint": 614, "status": "continue", "stage": checkpoint["stage"],
                  "nextAction": NEXT, "blocker": None})
    state["execution614CoordinatorCheckpoint"] = checkpoint
    state["batch087NativeExecutionCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    final = load(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert final[key] == value, key
    save(L / "checkpoint-final-614.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    {"start": start, "sheets": sheets, "collect": collect, "finalize": finalize}[sys.argv[1]]()
