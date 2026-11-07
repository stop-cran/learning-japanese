import copy
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "ec5e6e3f-0cb4-47c8-850d-3b276eba0562"
HEAD = "3a31f5eecbe403b81cb0c0bce9a467025feaef89"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SOURCE = C / "artifacts" / "batch-091-native-attempt-650"
DEST = R / "docs" / "n1-reviews" / "batch-091-native" / "execution-650"
EVIDENCE = R / "docs" / "n1-sources" / "execution-650.json"
NEXT = (
    "SAME091 serial dependent visual confirmations in ORIGINAL Claude session "
    "075924f2-f60b-4ae0-bf3f-341db3dfbd74 then ORIGINAL GPT session "
    "8da57d75-100b-4996-acf7-f52b0b446472. Read docs/n1-sources/execution-650.json, "
    "actual archived PNGs/visual-inspection and original textual reports/limitations. "
    "Use actual CLI catalog/tool support; one read-only reviewer at a time, wait for "
    "actual process exit and preserve complete reports. No new blind initial credit. "
    "Teaching c2a59d5c unchanged. Both native cases terminal per-case0/no skips; full "
    "archive f6b2ee39 through production ContentSync ONCE:1114kanji/5070words/123N1/"
    "zeroProblems/contentVersion cb3c857f3614485d/acceptedRoom readingEpoch1. "
    "All21 scopedHan readable in THREE actual Compose panels across FOUR productionfont "
    "selections, especially fallback U+4E36;84individual+4wholewordPaint probes are NOT "
    "separately viewed PNGs or identified fallbackface. Coordinator viewed26 original "
    "PNGs; all50 captures preserved, no claim of separate fresh inspection of remaining24. "
    "N1/All production choices exactly blade;cuttingedge vs 乃/凹/凸, all3curatedwrongcards/"
    "no fallback. ONLY kunは offered/persistedGood/Done, NOon keys; raw onジン,ニン and "
    "kunは,やいば,き.る retained in sourceorder in full/Lite. Recognized on/yaiba not "
    "sourceonly/uniformlyrare; kiru sourceonly/no fabricatedspelling. THREE pinned drawing "
    "strokes injectedtrace/recall/persistence; BOTH complete articles/ONE mappedpair/TWO "
    "directions/先端forefront/SystemBack/offline/N1selection/meaning/reading/drawing. "
    "FIVE directwordguards including先端; physicalpartnoun/neutraltranslations/shapemnemonic/"
    "physical-vs-figurativeEnglishcontrast. Injectedtrace/giveup NOT humanhandwriting/"
    "MLKit/phone. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latest "
    "appmain. Owned5580 helper29800/qemu17136 stopped. Parent19008 retains runner.lock; "
    "verify liveancestry/session/checkpoint/exactsignedheads/whollyclean, NO child "
    "reacquisition/delete/unlock. Approvedcontrol/committedpackets only, NOT optional "
    "historicalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. All originalsource/baseline/link/reading/twofamily/native/"
    "currentmainnormalmerge/changedteachingreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPruntimehash/original "
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/"
    "ownerissue gates remain. Published117/1228,1111remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No092/runtimepublication."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def verify_heads(content_head, require_clean):
    for root, expected in [(R, content_head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if require_clean:
            assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    assert not git("diff", "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", APP,
                   "--", "app/src/main", "core/src/main", "gradle.properties", root=A)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    assert manifest["contentVersion"] == "cb3c857f3614485d"
    preparation = load(C / "batch-091-native-fixture-verification.json")
    archive_path = Path(preparation["archive"])
    assert sha(archive_path) == preparation["archiveSha256"]
    count = 0
    with zipfile.ZipFile(archive_path) as archive:
        prefix = next(name[:-len("manifest.json")] for name in archive.namelist()
                      if name.endswith("manifest.json"))
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
    assert count == 8432
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "archiveManifestEqual": True,
            "manifestFreshAndUnchanged": True}


def prepare():
    verify_heads(HEAD, True)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["stage"]) == (
        649, "091", "batch-091-native-execution-in-progress")
    receipt = load(SOURCE / "execution.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"]
    raw = (SOURCE / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert raw.count("INSTRUMENTATION_STATUS_CODE: 0") == 2
    assert "OK (2 tests)" in raw
    route = load(SOURCE / "n1-091-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"],
            route["problems"], route["acceptedReadingParserEpoch"]) == (1114, 5070, 123, 0, 1)
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["は"]
    assert route["fullOnyomi"] == ["ジン", "ニン"]
    assert route["fullKunyomi"] == ["は", "やいば", "き.る"]
    raster = load(SOURCE / "n1-091-font-raster.json")
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"],
            raster["panels"]) == (84, 4, 3)
    assert len(raster["rows"]) == 88
    pngs = sorted(SOURCE.glob("*.png"))
    assert len(pngs) == 50
    inspected = [
        "font-panel-1", "font-panel-2", "font-panel-3",
        "kanji-01", "kanji-04", "kanji-09", "kanji-11", "kanji-24", "kanji-26",
        "blade-02", "blade-07", "blade-09", "forefront-destination",
        "meaning-question", "meaning-feedback", "curated-は-question",
        "curated-は-feedback", "curated-one-kun-no-on-done", "drawing-trace",
        "drawing-feedback", "drawing-recall-feedback", "selection",
        "blade-kanji-backlink", "blade-system-back-to-kanji",
        "blade-system-back-to-word", "forefront-system-back-to-word",
    ]
    assert len(inspected) == 26
    visual = {
        "snapshot": "c2a59d5c1cd4ac8040156a6c067bd9d565d59116",
        "archiveSnapshot": receipt["contentSnapshot"],
        "reviewer": "Coordinator, actual GPT-6.1 Sol (gpt-6.1-sol); not independent review",
        "scope": "Native rendered content, all 21 scoped Han in four font selections, meaning/reading/drawing and article routes.",
        "inspectedOriginalPngs": [
            {"file": f"n1-091-{name}.png", "sha256": sha(SOURCE / f"n1-091-{name}.png")}
            for name in inspected
        ],
        "capturedPngs": 50,
        "individuallyInspectedPngs": 26,
        "notSeparatelyInspectedPngs": 24,
        "glyphDisposition": "All 21 scoped Han readable/distinguishable in the three original Compose panels across Gothic/Mincho/Textbook/Brush. U+4E36 is visible as a short diagonal mark in every selection, not a replacement box; bundled cmap absence with successful native display supports usable system fallback, not identification of its face. 刃/刀/乃/凹/凸 and 先/端 remain distinguishable; 刃物 legible.",
        "articleDisposition": "Both complete new articles covered by complementary original views and passing native selector/scroll assertions. Readings table is horizontally scrollable as instructed; left/right views complement one another, not simultaneous full-column visibility. Physical/figurative distinction, recognition/source-only qualification, Japanese translations, modern-shape mnemonic and links remain readable.",
        "quizDisposition": "Exactly one defensible blade/cutting-edge answer versus three visible curated wrong labels. Only kun は offered; correct feedback and 1/1 Done visible. Full raw readings displayed in feedback are not extra offered keys.",
        "routeDisposition": "Forward/backlink/System Back and 先端 destination/return visible; N1 selection and offline persistence asserted.",
        "drawingDisposition": "Three pinned strokes visible. Injected trace followed by recall give-up and persistence passed; model-unavailable/shape-only grading is explicitly shown. Not human handwriting or successful MLKit recognition.",
        "findings": [],
        "limits": [
            "Not a fresh linguistic/source review or two-family dependent visual closure.",
            "Remaining 24 PNGs preserved but not separately visually inspected by this coordinator.",
            "84 individual and four whole-word Paint probes are not separately inspected PNGs.",
            "No physical phone, latest app-main, native-speaker or measured-learning acceptance.",
        ],
    }
    assert not DEST.exists() and not EVIDENCE.exists()
    DEST.mkdir()
    artifacts = []
    for source in sorted(SOURCE.iterdir()):
        assert source.is_file()
        target = DEST / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        artifacts.append({"path": target.relative_to(R).as_posix(), "sha256": sha(target),
                          "bytes": target.stat().st_size})
    for source in [C / "prepare-native-execution-650.py",
                   C / "close-native-execution-650.py", C / "run-650-native.ps1"]:
        target = DEST / source.name
        shutil.copyfile(source, target)
        artifacts.append({"path": target.relative_to(R).as_posix(), "sha256": sha(target),
                          "bytes": target.stat().st_size})
    save(DEST / "visual-inspection.json", visual)
    artifacts.append({"path": (DEST / "visual-inspection.json").relative_to(R).as_posix(),
                      "sha256": sha(DEST / "visual-inspection.json")})
    evidence = {
        "schemaVersion": 1, "execution": 650, "batch": "091",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingState": p["execution650StartingState"],
        "executionReceipt": receipt, "nativeRoute": route,
        "visualInspection": visual, "runtime": runtime(), "artifacts": artifacts,
        "textualReviewClosed": True, "independentVisualConfirmation": "pending",
        "originalReviewSessions": {
            "claude-opus-5.5": "075924f2-f60b-4ae0-bf3f-341db3dfbd74",
            "gpt-6.1-sol": "8da57d75-100b-4996-acf7-f52b0b446472",
        },
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "independentReviewersLaunched": 0,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT,
    }
    save(EVIDENCE, evidence)
    print("Both terminal cases and 8432 current/archive hashes verified; 50 PNGs preserved, 26 viewed.")


def finalize():
    saved = git("rev-parse", "HEAD")
    verify_heads(saved, True)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "strokes", "articles", "manifest.json")
    evidence = load(EVIDENCE)
    for artifact in evidence["artifacts"]:
        assert sha(R.joinpath(*artifact["path"].split("/"))) == artifact["sha256"]
    issue = load(C / "batch-091-native-650-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    before = load(L / "progress-before-650.json")
    p = load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 650, "checkpoint": 650, "batch": "091",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmation",
        "evidence": "docs/n1-sources/execution-650.json",
        "contentArchiveHead": "f6b2ee397b4e2998abcef6fd747b25d6178b1fa3",
        "reviewedTeachingSnapshot": "c2a59d5c1cd4ac8040156a6c067bd9d565d59116",
        "androidHead": APP, "terminalSuccessCases": 2, "skipped": 0,
        "nativeExecuted": True, "nativeCasesPassed": True,
        "coordinatorViewedPngs": 26, "capturedPngs": 50,
        "scopedHanInspected": 21, "productionFontSelections": 4,
        "runtimeHashesVerified": 8432, "contentVersion": "cb3c857f3614485d",
        "ownedHelperStopped": True, "ownedQemuStopped": True,
        "independentVisualConfirmation": "pending", "independentReviewersLaunched": 0,
        "dedicatedWorktreesClean": True, "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT, "issueUpdate": issue["html_url"],
        "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p.update(checkpoint=650, status="continue", stage=checkpoint["stage"],
             nextAction=NEXT, blocker=None)
    p["execution650CoordinatorCheckpoint"] = checkpoint
    p["batch091NativeAcceptanceCheckpoint"] = copy.deepcopy(checkpoint)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert p[key] == value, key
    temp = C / "progress.650.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")
    save(L / "native-650-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 650, "savedCommit": saved, "issue": issue["html_url"],
                      "historicalRootValuesPreserved": len(before), "status": "continue"}))


if __name__ == "__main__":
    {"prepare": prepare, "finalize": finalize}[sys.argv[1]]()
