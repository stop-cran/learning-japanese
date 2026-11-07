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
L = C / "logs" / "6eb76a67-baeb-4c82-9712-085c7f41f102"
HEAD = "540d36f717189b2ac7b34bebeba1414ff3ff53c6"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
BEFORE = L / "progress-before-641.json"
ATTEMPT = C / "artifacts" / "batch-090-native-attempt-641"
RETRY = C / "artifacts" / "batch-090-native-attempt-641-retry1"
NEXT = (
    "SAME090 serial dependent visual confirmations in ORIGINAL Claude "
    "63fa1d59-4733-497f-bc2d-b6202471619d then ORIGINAL GPT "
    "f0995652-508c-4921-a3dd-08e89e67eb46. Read docs/n1-sources/execution-641.json, "
    "archived actual PNGs/visual-inspection and original textual reports/limitations. "
    "Use actual CLI catalog/tool support, one read-only reviewer at a time, wait for actual exit "
    "and preserve complete reports. No new blind initial credit. Teachinge044e953 unchanged. "
    "Full archive40bc5a55 through productionContentSync ONCE:1113kanji/5069words/122N1/"
    "zeroProblems/acceptedVersionceee0f79a6d394df/readingEpoch1. Both native cases terminal0/no skips. "
    "All18Han in fourproductionfont selections inspected in3Composepanels;72individual+4wholewordPaint "
    "hash probes NOT separately inspected PaintPNGs or identified fallbackface. Exactly 刀sword;blade "
    "versus乃thereupon;possessiveno/凹concave;sunken/凸convex;protruding in actualN1 and productionAll;"
    "allthreeavailable/no fallback. Exactly onとう/kunかたな Good/done;rawトウ/かたな/そり retained "
    "in full/Lite sourceorder;sourceonlyそり excluded without invented jukujikunrazor allocation. "
    "Twostroke injectedtrace/recall/persistence,BOTHcompletearticles,ONLYfourchangedreusedpassages,"
    "fivemappedpairs/tendirections/onedirect日本刀-to-刀guard/SystemBack/offline. "
    "Existing刀N3/剃刀N2/鋭いguard preserved. TraditionalJapaneseSwordnoun,neutralmuseum/photosentences,"
    "lexical日本modifier+sword,bothにほんとう/にっぽんとう without frequencyranking/universalsoundchange/"
    "shape rule. Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. QualifiedTESTONLYAndroid1c1b7bf4 "
    "retains productionf9b59a2,NOT latestappmain. Owned5580helper26660/qemu17716 stopped. "
    "First641wrapper escaping failure before device launch preserved;corrected literalverification "
    "retry1 proved live parent ancestry/session/decodedlauncher,NOT permissiondenial or lockrecovery. "
    "Parent19008 ownsrunner.lock: verify liveancestry/session/checkpoint/exactsignedheads/"
    "whollycleanworktrees;NOchildreacquisition/delete/unlock. Approvedcontrol/committedsources only,"
    "not optionalhistoricalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Alloriginalsource/baseline/link/reading/twofamily/native/currentmainnormalmerge/"
    "changedteachingindependentreview/combinedchecks/normalsigning/ownerfastforward/terminalCI/"
    "EVERYimmutablepublicZIPruntimehash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/ownerissue gates remain. No091/runtimepublication/productionappchange/"
    "heaporguardincrease. Published116/1228,1112remaining unchanged;physicalphone/generalrelease/"
    "whole-set outstanding;projectincomplete."
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
    assert manifest["contentVersion"] == "ceee0f79a6d394df"
    preparation = load(C / "batch-090-native-fixture-verification.json")
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
    assert count == 8429
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "archiveManifestEqual": True}


def persist(state):
    path = C / "progress.641.tmp"
    assert not path.exists()
    save(path, state)
    assert load(path) == state
    path.replace(C / "progress.json")


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        640, "continue", "native-prepared-compiled-not-executed", "090")
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["execution640CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    verified = runtime()
    assert not BEFORE.exists()
    save(BEFORE, state)
    source = C / "run-632-native.ps1"
    wrapper = source.read_text(encoding="utf-8-sig")
    for old, new in [
        ("ce211b43-0321-466f-a781-8c467468605d", L.name),
        ("dfcdb7a0f5da5191d49762cad82fc1c7816d3201", HEAD),
        ("632", "641"), ("631", "640"), ("089", "090"),
    ]:
        assert old in wrapper
        wrapper = wrapper.replace(old, new)
    anchor = "    $result.parentAncestry = $ancestry"
    assert wrapper.count(anchor) == 1
    wrapper = wrapper.replace(anchor, r"""    $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$($runner.pid)"
    $encoded = [regex]::Match($parent.CommandLine, '-EncodedCommand\\s+(\\S+)')
    if (-not $encoded.Success -or [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded.Groups[1].Value)) -notlike "*$control\\runner.ps1*") {
        throw 'Launcher command ownership uncertain; no lock access attempted.'
    }
    $result.launcherCommandMatches = $true
""" + anchor)
    output = C / "run-641-native.ps1"
    assert not output.exists()
    output.write_text(wrapper, encoding="utf-8")
    state["execution641StartingState"] = {
        "execution": 641, "batch": "090", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME090 compiled native execution and actual PNG inspection; signed LOCAL evidence only. No reviewer/publication/091.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete issue and final640 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry/session/launcher command required by child wrapper; no lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed source packets only; no historical session recipe access.",
        "runtime": verified, "actualNewPermissionDenials": [],
        "wrapperProvenance": {"template": str(source), "templateSha256": sha(source),
                              "generated": str(output), "generatedSha256": sha(output),
                              "changes": "Session, exact signed coordinator head, execution632->641/preparation631->640/batch089->090; require decoded parent launcher command."},
    }
    state["stage"] = "batch-090-native-execution-in-progress"
    persist(state)
    print("641 starting state persisted; all 8429 current/archive hashes verified; generated wrapper frozen.")


def retry():
    clean()
    state = load(C / "progress.json")
    assert state["checkpoint"] == 640 and state["stage"] == "batch-090-native-execution-in-progress"
    original = C / "run-641-native.ps1"
    result = load(C / "batch-090-native-attempt-641-execution.json")
    assert result["failure"] == "Launcher command ownership uncertain; no lock access attempted."
    assert not result["nativeExecuted"] and not result["parentLockTouched"]
    wrapper = original.read_text(encoding="utf-8")
    bad_regex = r"'-EncodedCommand\\s+(\\S+)'"
    bad_path = r'"*$control\\runner.ps1*"'
    assert wrapper.count(bad_regex) == wrapper.count(bad_path) == 1
    wrapper = wrapper.replace(bad_regex, r"'-EncodedCommand\s+(\S+)'")
    wrapper = wrapper.replace(bad_path, r'"*$control\runner.ps1*"')
    wrapper = wrapper.replace("batch-090-native-attempt-641", "batch-090-native-attempt-641-retry1")
    target = C / "run-641-native-retry1.ps1"
    assert not target.exists()
    target.write_text(wrapper, encoding="utf-8")
    state["execution641WrapperDiagnostic"] = {
        "originalWrapper": str(original), "originalSha256": sha(original),
        "originalReceipt": str(C / "batch-090-native-attempt-641-execution.json"),
        "failure": result["failure"], "nativeExecuted": False,
        "rootCause": "Generated PowerShell regex and expected path were double-escaped. Python raw string retained the extra backslashes. Check failed before device inspection, not an actual denial or evidence of another owner.",
        "readOnlyConfirmation": "Independent literal single-backslash regex decoded live PID19008 launcher and matched exact authorized control runner.ps1; runner session and live ancestry were already valid.",
        "retryWrapper": str(target), "retrySha256": sha(target),
        "disposition": "Preserve first attempt unchanged. New attempt re-runs every signed-head, clean-state, checkpoint, live-parent/session/decoded-command, hash, fresh device/port and acceptance check with corrected literal escaping. No lock access or ownership assumption.",
    }
    persist(state)
    print("Original wrapper/receipt preserved; retry1 corrects escaping and retains all ownership checks.")


def sheets():
    from PIL import Image, ImageDraw

    attempt = C / "artifacts" / "batch-090-native-attempt-641-retry1"
    folder = attempt / "inspection"
    assert not folder.exists()
    folder.mkdir()
    files = sorted(attempt.glob("*.png"))
    assert len(files) == 64
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
    state = load(C / "progress.json")
    result = load(C / "batch-090-native-attempt-641-retry1-execution.json")
    assert result["passed"] and result["terminalSuccessCases"] == 2 and result["adbExitCode"] == 0
    assert result["ownedHelperStopped"] and result["ownedQemuStopped"] and result["launcherCommandMatches"]
    assert not result["parentLockTouched"] and not result["guestOrAppHeapChanged"] and not result["guardsChanged"]
    raw = (RETRY / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert raw.count("INSTRUMENTATION_STATUS_CODE: 0") == 2 and "OK (2 tests)" in raw
    for bad in ["INSTRUMENTATION_STATUS_CODE: -2", "INSTRUMENTATION_STATUS_CODE: -3",
                "INSTRUMENTATION_STATUS_CODE: -4", "INSTRUMENTATION_FAILED", "FAILURES"]:
        assert bad not in raw
    route = load(RETRY / "n1-090-article-route.json")
    assert (route["archiveRequests"], route["importedKanji"], route["importedWords"], route["n1Cards"],
            route["problems"], route["acceptedReadingParserEpoch"]) == (1, 1113, 5069, 122, 0, 1)
    assert route["passed"] and route["offline"]
    assert route["contentVersion"] == verified["contentVersion"]
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"], route["directWordGuardCount"],
            route["completeArticleProjections"], route["touchInjectedReferenceStrokes"],
            route["changedReusedArticles"]) == (5, 10, 1, 2, 2, 4)
    assert route["bothCuratedKindsPersistedGoodAndDone"]
    for key in ["quizOnKeys", "quizKunKeys"]:
        assert route[key] == {"quizOnKeys": ["とう"], "quizKunKeys": ["かたな"]}[key]
    for pool in route["productionBuilderN1AndAllExactChoices"].values():
        assert pool["availableCuratedCount"] == 3 and pool["fallbackOptions"] == 0
        assert {o["kanji"]: o["title"] for o in pool["options"]} == {
            "刀": "sword; blade", "乃": "thereupon; possessive no",
            "凹": "concave; sunken", "凸": "convex; protruding",
        }
    glyph = load(RETRY / "n1-090-font-raster.json")
    assert (glyph["individualGlyphProbes"], glyph["wholeWordRasterProbes"], glyph["panels"]) == (72, 4, 3)
    assert len(glyph["rows"]) == 76
    inspection = load(C / "batch-090-native-641-visual-inspection.json")
    assert inspection["allOriginalScreenshotsInspected"] and inspection["actualComposeFontPanelsViewed"] == 3
    folder = R / "docs" / "n1-reviews" / "batch-090-native" / "execution-641"
    assert not folder.exists()
    folder.mkdir()
    receipts = []
    for source_folder, destination_folder in [(ATTEMPT, folder / "first-attempt"), (RETRY, folder / "retry1")]:
        for path in sorted(source_folder.rglob("*")):
            if not path.is_file():
                continue
            destination = destination_folder / path.relative_to(source_folder)
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
    for name, target in [("run-641-native.ps1", "run-641-native.ps1"),
                         ("run-641-native-retry1.ps1", "run-641-native-retry1.ps1"),
                         (Path(__file__).name, "checkpoint-recipe.py"),
                         ("batch-090-native-641-visual-inspection.json", "visual-inspection.json")]:
        shutil.copyfile(C / name, folder / target)
        receipts.append({"source": str(C / name), "archive": (folder / target).relative_to(R).as_posix(),
                         "sourceSha256": sha(C / name), "archiveSha256": sha(folder / target)})
    evidence = {
        "schemaVersion": 1, "execution": 641, "batch": "090",
        "status": "native-passed-coordinator-inspected-awaiting-independent-visual-confirmations",
        "contentTestedHead": result["contentSnapshot"], "coordinatorStartingHead": HEAD,
        "androidTestedHead": APP, "teachingSnapshot": "e044e953133548dd37fdf1dba449de2f4ee7575f",
        "qualifiedAppBaseline": "TESTONLY1c1b7bf4 retains unchanged productionf9b59a2; not latest app main.",
        "startingState": state["execution641StartingState"],
        "firstAttemptDiagnostic": state["execution641WrapperDiagnostic"],
        "executionReceipt": result, "nativeRoute": route,
        "glyphProbeSummary": {"individual": 72, "wholeWord": 4, "actualComposePanelsViewed": 3,
                              "separatePaintPngsViewed": 0, "fallbackFontFaceIdentified": False},
        "visualInspection": inspection, "runtime": verified, "receipts": receipts,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "independentReviewersLaunched": 0, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "publishedAdditions": 116, "remainingAdditions": 1112, "nextAction": NEXT,
        "limits": [
            "Native emulator and coordinator visual evidence only; original-session dependent independent visual confirmations still required.",
            "Injected trace/give-up is not human handwriting, MLKit recognition success or phone acceptance.",
            "76 Paint hash probes are not76 separately inspected PNGs; no fallback-face identification.",
            "Original two-family textual reports and all original source/reviewer/process/denial/OOM/current-main/publication/phone limitations and unchanged production guards remain.",
        ],
    }
    save(R / "docs" / "n1-sources" / "execution-641.json", evidence)
    print("Collected verified native/visual evidence and preserved first attempt; no runtime content edited.")


def finish():
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD
    clean(saved)
    evidence = load(R / "docs" / "n1-sources" / "execution-641.json")
    for receipt in evidence["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    verified = runtime()
    receipt = load(C / "batch-090-native-641-issue-receipt.json")
    body = (C / "batch-090-native-641-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    state, before = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 640 and state["stage"] == "batch-090-native-execution-in-progress"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 641, "checkpoint": 641, "batch": "090",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmations",
        "evidence": "docs/n1-sources/execution-641.json", "runtime": verified,
        "nativeCases": 2, "terminalCaseSuccesses": 2, "skips": 0,
        "screenshotsActuallyInspected": 64, "contactSheetsViewed": 11,
        "actualComposeFontPanelsViewed": 3, "nativePaintHashProbes": 76, "separatePaintPngsViewed": 0,
        "independentVisualConfirmationsComplete": False, "runtimeAccepted": False,
        "runtimeChanged": False, "runtimePublished": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "ownedHelperStopped": True, "ownedQemuStopped": True,
        "firstAttemptPreserved": True, "correctedLiteralOwnershipChecksPassed": True,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 116, "remainingAdditions": 1112,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update({"checkpoint": 641, "status": "continue", "stage": checkpoint["stage"],
                  "nextAction": NEXT, "blocker": None})
    state["execution641CoordinatorCheckpoint"] = checkpoint
    state["batch090NativeExecutionCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    final = load(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert final[key] == value, key
    save(L / "checkpoint-final-641.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    {"start": start, "retry": retry, "sheets": sheets, "collect": collect, "finish": finish}[sys.argv[1]]()
