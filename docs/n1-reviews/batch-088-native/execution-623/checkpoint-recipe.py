import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "a94bf768-d6d1-49db-8115-f65f5edd7bc2"
HEAD = "1cb4f21bd6b412898dd229cab5dfe04a3abe9157"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
BEFORE = L / "progress-before-623.json"
ATTEMPT = C / "artifacts" / "batch-088-native-attempt-623"
NEXT = (
    "SAME088 serial dependent visual confirmations in ORIGINAL Claude915d0745-fc54-49b0-99cf-49762fb5e16f "
    "then ORIGINAL GPT11925f67-211b-497f-9d75-3d2802c178ab; actual CLI catalog/tool support, one read-only "
    "reviewer at a time, wait for actual exit and preserve complete reports/limits. No new blind initial credit. "
    "Read docs/n1-sources/execution-623.json, archived actual PNGs/visual-inspection and original textual reports. "
    "Teaching42077c31 unchanged. Native full archivee445d826 through productionContentSyncONCE, "
    "1111kanji/5067words/120N1/zeroProblems/acceptedVersionafff40af0e155dbe/readingEpoch1. "
    "Both native cases terminal0/no skips. Fourfont Compose panels cover all27Han especially U+51E0/U+8C48/U+9B28; "
    "108individual+4wholewordPaint probes are hashes, NOT separately viewed PaintPNGs or identified fallbackface. "
    "Actual N1/All target victorysong;triumph versus 凡commonplace;mediocre, 凸convex;protruding, 凹concave;sunken "
    "requires no fallback. Singlequeuedonkeyがい Good/done; explicitkun[], rawfourreadings/order preserved. "
    "Twelvestroke injectedtrace/recall/persistence, BOTHarticleprojections, onemappedpair/twodirections/"
    "fourdirectguards/SystemBack/offline. Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "Parent19008 ownsrunner.lock: verify liveancestry/session/checkpoint/exactsignedheads/whollycleanworktrees; "
    "NOchildreacquisition/delete/unlock. Approvedcontrol/committedsources only, not optionalhistoricalsessionrecipes. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Alloriginalsource/baseline/link/reading/"
    "twofamily/native/currentmainnormalmerge/changedteachingindependentreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalCI/EVERYimmutablepublicZIPruntimehash/original18000entries42MiBcompressed/"
    "80MiBinflated56MiBretained/perfile-media-safepath/ownerissue gates remain. No089/runtimepublication/"
    "productionappchange/heaporguardincrease. Published114/1228,1114remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding; projectincomplete."
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
    assert manifest["contentVersion"] == "afff40af0e155dbe"
    preparation = load(C / "batch-088-native-fixture-verification.json")
    assert sha(Path(preparation["archive"])) == preparation["archiveSha256"]
    count = 0
    with zipfile.ZipFile(preparation["archive"]) as archive:
        prefix = next(name[:-len("manifest.json")] for name in archive.namelist() if name.endswith("manifest.json"))
        assert json.loads(archive.read(prefix + "manifest.json")) == manifest
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, expected in entries.items():
                path = R.joinpath(*name.split("/"))
                media = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert (sha(path) if media else sha256(path)) == expected, name
                data = archive.read(prefix + name)
                if not media:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == expected, name
                count += 1
    assert count == 8423
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "archiveManifestEqual": True}


def persist(state):
    path = C / "progress.623.tmp"
    assert not path.exists()
    save(path, state)
    assert load(path) == state
    path.replace(C / "progress.json")


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        622, "continue", "native-prepared-compiled-not-executed", "088")
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["execution622CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    verified = runtime()
    assert not BEFORE.exists()
    save(BEFORE, state)
    source = C / "run-614-native.ps1"
    wrapper = source.read_text(encoding="utf-8-sig")
    for old, new in [
        ("be17e4ac-5fa9-424a-8243-595b899ce914", L.name),
        ("243e504acfccddb7760e4108b6cd0dce2f0bfd9a", HEAD),
        ("614", "623"), ("613", "622"), ("087", "088"),
    ]:
        assert old in wrapper
        wrapper = wrapper.replace(old, new)
    output = C / "run-623-native.ps1"
    assert not output.exists()
    output.write_text(wrapper, encoding="utf-8")
    state["execution623StartingState"] = {
        "execution": 623, "batch": "088", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME088 compiled native execution and actual PNG inspection; signed LOCAL evidence only. No reviewer/publication/089.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete issue and final622 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry/session verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed source packets only; no historical session recipe access.",
        "runtime": verified, "actualNewPermissionDenials": [],
        "wrapperProvenance": {"template": str(source), "templateSha256": sha(source),
                              "generated": str(output), "generatedSha256": sha(output),
                              "changes": "Only session, exact signed coordinator head, execution614->623/preparation613->622/batch087->088."},
    }
    state["stage"] = "batch-088-native-execution-in-progress"
    persist(state)
    print("623 starting state persisted; all 8423 current/archive hashes verified; generated wrapper frozen.")


def sheets():
    from PIL import Image, ImageDraw
    folder = ATTEMPT / "inspection"
    assert not folder.exists()
    folder.mkdir()
    files = sorted(ATTEMPT.glob("*.png"))
    assert files
    mapping = []
    for offset in range(0, len(files), 6):
        sheet = Image.new("RGB", (1500, 2260), "white")
        draw = ImageDraw.Draw(sheet)
        originals = []
        for position, path in enumerate(files[offset:offset + 6]):
            x, y = (position % 3) * 500, (position // 3) * 1130
            with Image.open(path) as image:
                image = image.convert("RGB")
                image.thumbnail((500, 1100))
                sheet.paste(image, (x, y + 30))
            draw.text((x + 4, y + 4), f"{offset + position + 1}: {path.name}", fill="black")
            originals.append({"original": path.name, "sha256": sha(path), "position": position})
        path = folder / f"contact-{offset // 6 + 1:02}.png"
        sheet.save(path)
        mapping.append({"sheet": path.name, "sha256": sha(path), "originals": originals})
    save(folder / "contact-map.json", mapping)
    print(f"{len(files)} original PNGs; {len(mapping)} contact sheets.")


def collect():
    clean()
    verified = runtime()
    result = load(C / "batch-088-native-attempt-623-execution.json")
    assert result["passed"] and result["terminalSuccessCases"] == 2 and result["adbExitCode"] == 0
    assert result["ownedHelperStopped"] and result["ownedQemuStopped"]
    assert not result["parentLockTouched"] and not result["guestOrAppHeapChanged"] and not result["guardsChanged"]
    route = load(ATTEMPT / "n1-088-article-route.json")
    assert (route["archiveRequests"], route["importedKanji"], route["importedWords"], route["n1Cards"],
            route["problems"], route["acceptedReadingParserEpoch"]) == (1, 1111, 5067, 120, 0, 1)
    assert route["passed"] and route["offline"]
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"], route["directWordGuardCount"],
            route["completeArticleProjections"], route["touchInjectedReferenceStrokes"]) == (1, 2, 4, 2, 12)
    glyph = load(ATTEMPT / "n1-088-font-raster.json")
    assert (glyph["individualGlyphProbes"], glyph["wholeWordRasterProbes"], glyph["panels"]) == (108, 4, 3)
    assert len(glyph["rows"]) == 112
    inspection = load(C / "batch-088-native-623-visual-inspection.json")
    assert inspection["allOriginalScreenshotsInspected"] and inspection["actualComposeFontPanelsViewed"] == 3
    folder = R / "docs" / "n1-reviews" / "batch-088-native" / "execution-623"
    assert not folder.exists()
    folder.mkdir()
    receipts = []
    for path in sorted(ATTEMPT.rglob("*")):
        if not path.is_file():
            continue
        destination = folder / path.relative_to(ATTEMPT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".txt":
            destination = destination.with_suffix(".txt.gz")
            destination.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            assert gzip.decompress(destination.read_bytes()) == path.read_bytes()
        else:
            shutil.copyfile(path, destination)
            assert sha(path) == sha(destination)
        receipts.append({"source": str(path), "archive": destination.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "archiveSha256": sha(destination)})
    for name, target in [("run-623-native.ps1", "run-623-native.ps1"),
                         (Path(__file__).name, "checkpoint-recipe.py"),
                         ("batch-088-native-623-visual-inspection.json", "visual-inspection.json")]:
        shutil.copyfile(C / name, folder / target)
        receipts.append({"source": str(C / name), "archive": (folder / target).relative_to(R).as_posix(),
                         "sourceSha256": sha(C / name), "archiveSha256": sha(folder / target)})
    evidence = {
        "schemaVersion": 1, "execution": 623, "batch": "088",
        "status": "native-passed-coordinator-inspected-awaiting-independent-visual-confirmations",
        "contentTestedHead": result["contentSnapshot"], "coordinatorStartingHead": HEAD,
        "androidTestedHead": APP, "teachingSnapshot": "42077c31b4462081eb6b2c171a907c7cae47192d",
        "qualifiedAppBaseline": "TESTONLY1c1b7bf4 retains unchanged productionf9b59a2; not latest app main.",
        "startingState": load(C / "progress.json")["execution623StartingState"],
        "executionReceipt": result, "nativeRoute": route, "glyphProbeSummary": {
            "individual": 108, "wholeWord": 4, "actualComposePanelsViewed": 3,
            "separatePaintPngsViewed": 0, "fallbackFontFaceIdentified": False},
        "visualInspection": inspection, "runtime": verified, "receipts": receipts,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "independentReviewersLaunched": 0, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "publishedAdditions": 114, "remainingAdditions": 1114, "nextAction": NEXT,
        "limits": ["Native emulator plus coordinator visual evidence only; original-session dependent independent visual confirmations still required.",
                   "Injected trace/give-up is not human handwriting, MLKit recognition success or phone acceptance.",
                   "Paint bitmaps recycled; 112 hash probes not 112 separately inspected PNGs.",
                   "All original source/reviewer/process/denial/OOM/current-main/publication limitations and unchanged production guards remain."],
    }
    save(R / "docs" / "n1-sources" / "execution-623.json", evidence)
    print("Collected verified native/visual evidence; no runtime content edited.")


def finish():
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD
    clean(saved)
    evidence = load(R / "docs" / "n1-sources" / "execution-623.json")
    for receipt in evidence["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    verified = runtime()
    receipt = load(C / "batch-088-native-623-issue-receipt.json")
    body = (C / "batch-088-native-623-issue-body.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    state, before = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 622 and state["stage"] == "batch-088-native-execution-in-progress"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 623, "checkpoint": 623, "batch": "088",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmations",
        "evidence": "docs/n1-sources/execution-623.json", "runtime": verified,
        "nativeCases": 2, "terminalCaseSuccesses": 2, "skips": 0,
        "screenshotsActuallyInspected": evidence["visualInspection"]["screenshotsActuallyInspected"],
        "actualComposeFontPanelsViewed": 3, "nativePaintHashProbes": 112, "separatePaintPngsViewed": 0,
        "independentVisualConfirmationsComplete": False, "runtimeAccepted": False,
        "runtimeChanged": False, "runtimePublished": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "ownedHelperStopped": True, "ownedQemuStopped": True,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 114, "remainingAdditions": 1114,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update({"checkpoint": 623, "status": "continue", "stage": checkpoint["stage"],
                  "nextAction": NEXT, "blocker": None})
    state["execution623CoordinatorCheckpoint"] = checkpoint
    state["batch088NativeExecutionCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    final = load(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert final[key] == value, key
    save(L / "checkpoint-final-623.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


def refresh_inspection():
    folder = R / "docs" / "n1-reviews" / "batch-088-native" / "execution-623"
    evidence_path = R / "docs" / "n1-sources" / "execution-623.json"
    evidence = load(evidence_path)
    evidence["visualInspection"] = load(C / "batch-088-native-623-visual-inspection.json")
    for source, target in [(C / "batch-088-native-623-visual-inspection.json", folder / "visual-inspection.json"),
                           (Path(__file__).resolve(), folder / "checkpoint-recipe.py")]:
        shutil.copyfile(source, target)
        receipt = next(item for item in evidence["receipts"] if item["archive"] == target.relative_to(R).as_posix())
        receipt.update({"sourceSha256": sha(source), "archiveSha256": sha(target)})
    save(evidence_path, evidence)
    print("Inspection filenames corrected; source/archived observations, helper and receipt hashes synchronized.")


if __name__ == "__main__":
    {"start": start, "sheets": sheets, "collect": collect, "finish": finish,
     "refresh-inspection": refresh_inspection}[sys.argv[1]]()
