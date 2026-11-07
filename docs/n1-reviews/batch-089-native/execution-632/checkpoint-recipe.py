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
L = C / "logs" / "ce211b43-0321-466f-a781-8c467468605d"
HEAD = "dfcdb7a0f5da5191d49762cad82fc1c7816d3201"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
BEFORE = L / "progress-before-632.json"
ATTEMPT = C / "artifacts" / "batch-089-native-attempt-632"
NEXT = (
    "SAME089 serial dependent visual confirmations in ORIGINAL Claude "
    "a56b5dcb-9fed-4785-848e-41708f65598f then ORIGINAL GPT "
    "3286add7-2824-4df6-933a-c8bba3890927. Actual CLI catalog/tool support; "
    "one read-only reviewer at a time; wait for actual exit and preserve complete reports/limits. "
    "No new blind initial credit; original GPT redundant/truncated-tail read limits remain. "
    "Read docs/n1-sources/execution-632.json and archived actual PNGs/visual-inspection plus original textual reports. "
    "Teaching4b84608b unchanged. Full archive72614eda through productionContentSync ONCE: "
    "1112kanji/5068words/121N1/zeroProblems/acceptedVersionc6562f11cb371053/readingEpoch1. "
    "Both native cases terminal0/no skips. Fourfont Compose panels cover all23Han especially U+4E42/U+51F5; "
    "92individual+4wholewordPaint probes are hashes, NOT separately viewed PaintPNGs or identified fallbackface. "
    "Actual N1/All target illfortune;evil versus 凡commonplace;mediocre, 凸convex;protruding, 凹concave;sunken "
    "allthreeavailable/no fallback. Singlequeuedonkeyきょう Good/done; rawkun[]/explicitquizkun[]. "
    "Fourstroke injectedtrace/recall/persistence, BOTHarticleprojections plus ONLYchanged作navigationline, "
    "twomappedpairs/fourdirections/onedirect収穫wordguard/SystemBack/offline. "
    "Agriculturalnoun/verypooryield not harvestverb/necessaryzeroyield/famine/badwork; compound-specific作crop/yield. "
    "Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. QualifiedTESTONLYAndroid1c1b7bf4 retains "
    "productionf9b59a2, NOT latestappmain. Parent19008 ownsrunner.lock: verify liveancestry/session/checkpoint/"
    "exactsignedheads/whollycleanworktrees; NOchildreacquisition/delete/unlock. "
    "Approvedcontrol/committedsources only, not optionalhistoricalsessionrecipes. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Alloriginalsource/baseline/link/reading/"
    "twofamily/native/currentmainnormalmerge/changedteachingindependentreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalCI/EVERYimmutablepublicZIPruntimehash/original18000entries42MiBcompressed/"
    "80MiBinflated56MiBretained/perfile-media-safepath/ownerissue gates remain. "
    "No090/runtimepublication/productionappchange/heaporguardincrease. Published115/1228,1113remaining unchanged; "
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
    assert manifest["contentVersion"] == "c6562f11cb371053"
    preparation = load(C / "batch-089-native-fixture-verification.json")
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
    assert count == 8426
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "archiveManifestEqual": True}


def persist(state):
    path = C / "progress.632.tmp"
    assert not path.exists()
    save(path, state)
    assert load(path) == state
    path.replace(C / "progress.json")


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        631, "continue", "native-prepared-compiled-not-executed", "089")
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["execution631CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    verified = runtime()
    assert not BEFORE.exists()
    save(BEFORE, state)
    source = C / "run-623-native.ps1"
    wrapper = source.read_text(encoding="utf-8-sig")
    for old, new in [
        ("a94bf768-d6d1-49db-8115-f65f5edd7bc2", L.name),
        ("1cb4f21bd6b412898dd229cab5dfe04a3abe9157", HEAD),
        ("623", "632"), ("622", "631"), ("088", "089"),
    ]:
        assert old in wrapper
        wrapper = wrapper.replace(old, new)
    output = C / "run-632-native.ps1"
    assert not output.exists()
    output.write_text(wrapper, encoding="utf-8")
    state["execution632StartingState"] = {
        "execution": 632, "batch": "089", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME089 compiled native execution and actual PNG inspection; signed LOCAL evidence only. No reviewer/publication/090.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete issue and final631 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry/session verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed source packets only; no historical session recipe access.",
        "runtime": verified, "actualNewPermissionDenials": [],
        "wrapperProvenance": {"template": str(source), "templateSha256": sha(source),
                              "generated": str(output), "generatedSha256": sha(output),
                              "changes": "Only session, exact signed coordinator head, execution623->632/preparation622->631/batch088->089."},
    }
    state["stage"] = "batch-089-native-execution-in-progress"
    persist(state)
    print("632 starting state persisted; all 8426 current/archive hashes verified; generated wrapper frozen.")


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
    result = load(C / "batch-089-native-attempt-632-execution.json")
    assert result["passed"] and result["terminalSuccessCases"] == 2 and result["adbExitCode"] == 0
    assert result["ownedHelperStopped"] and result["ownedQemuStopped"]
    assert not result["parentLockTouched"] and not result["guestOrAppHeapChanged"] and not result["guardsChanged"]
    route = load(ATTEMPT / "n1-089-article-route.json")
    assert (route["archiveRequests"], route["importedKanji"], route["importedWords"], route["n1Cards"],
            route["problems"], route["acceptedReadingParserEpoch"]) == (1, 1112, 5068, 121, 0, 1)
    assert route["passed"] and route["offline"]
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"], route["directWordGuardCount"],
            route["completeArticleProjections"], route["touchInjectedReferenceStrokes"]) == (2, 4, 1, 2, 4)
    glyph = load(ATTEMPT / "n1-089-font-raster.json")
    assert (glyph["individualGlyphProbes"], glyph["wholeWordRasterProbes"], glyph["panels"]) == (92, 4, 3)
    assert len(glyph["rows"]) == 96
    inspection = load(C / "batch-089-native-632-visual-inspection.json")
    assert inspection["allOriginalScreenshotsInspected"] and inspection["actualComposeFontPanelsViewed"] == 3
    folder = R / "docs" / "n1-reviews" / "batch-089-native" / "execution-632"
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
    for name, target in [("run-632-native.ps1", "run-632-native.ps1"),
                         (Path(__file__).name, "checkpoint-recipe.py"),
                         ("batch-089-native-632-visual-inspection.json", "visual-inspection.json")]:
        shutil.copyfile(C / name, folder / target)
        receipts.append({"source": str(C / name), "archive": (folder / target).relative_to(R).as_posix(),
                         "sourceSha256": sha(C / name), "archiveSha256": sha(folder / target)})
    evidence = {
        "schemaVersion": 1, "execution": 632, "batch": "089",
        "status": "native-passed-coordinator-inspected-awaiting-independent-visual-confirmations",
        "contentTestedHead": result["contentSnapshot"], "coordinatorStartingHead": HEAD,
        "androidTestedHead": APP, "teachingSnapshot": "4b84608b5ca8889d45a176667975524f6645bd8d",
        "qualifiedAppBaseline": "TESTONLY1c1b7bf4 retains unchanged productionf9b59a2; not latest app main.",
        "startingState": load(C / "progress.json")["execution632StartingState"],
        "executionReceipt": result, "nativeRoute": route, "glyphProbeSummary": {
            "individual": 92, "wholeWord": 4, "actualComposePanelsViewed": 3,
            "separatePaintPngsViewed": 0, "fallbackFontFaceIdentified": False},
        "visualInspection": inspection, "runtime": verified, "receipts": receipts,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "independentReviewersLaunched": 0, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "publishedAdditions": 115, "remainingAdditions": 1113, "nextAction": NEXT,
        "limits": ["Native emulator plus coordinator visual evidence only; original-session dependent independent visual confirmations still required.",
                   "Injected trace/give-up is not human handwriting, MLKit recognition success or phone acceptance.",
                   "Paint bitmaps recycled; 96 hash probes not 96 separately inspected PNGs.",
                   "Original GPT redundant/truncated-tail read limitations and all original source/reviewer/process/denial/OOM/current-main/publication limitations and unchanged production guards remain."],
    }
    save(R / "docs" / "n1-sources" / "execution-632.json", evidence)
    print("Collected verified native/visual evidence; no runtime content edited.")


def finish():
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD
    clean(saved)
    evidence = load(R / "docs" / "n1-sources" / "execution-632.json")
    for receipt in evidence["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    verified = runtime()
    receipt = load(C / "batch-089-native-632-issue-receipt.json")
    body = (C / "batch-089-native-632-issue-body.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    state, before = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 631 and state["stage"] == "batch-089-native-execution-in-progress"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 632, "checkpoint": 632, "batch": "089",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmations",
        "evidence": "docs/n1-sources/execution-632.json", "runtime": verified,
        "nativeCases": 2, "terminalCaseSuccesses": 2, "skips": 0,
        "screenshotsActuallyInspected": evidence["visualInspection"]["screenshotsActuallyInspected"],
        "actualComposeFontPanelsViewed": 3, "nativePaintHashProbes": 96, "separatePaintPngsViewed": 0,
        "independentVisualConfirmationsComplete": False, "runtimeAccepted": False,
        "runtimeChanged": False, "runtimePublished": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "ownedHelperStopped": True, "ownedQemuStopped": True,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 115, "remainingAdditions": 1113,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update({"checkpoint": 632, "status": "continue", "stage": checkpoint["stage"],
                  "nextAction": NEXT, "blocker": None})
    state["execution632CoordinatorCheckpoint"] = checkpoint
    state["batch089NativeExecutionCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    final = load(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert final[key] == value, key
    save(L / "checkpoint-final-632.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    {"start": start, "sheets": sheets, "collect": collect, "finish": finish}[sys.argv[1]]()
