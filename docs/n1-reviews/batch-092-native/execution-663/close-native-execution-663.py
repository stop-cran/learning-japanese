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
L = C / "logs" / "ebddfa2a-d55d-4245-a060-b0008ff34f6a"
HEAD = "e29406823d0dab6be1bc3ff78eea0d0af711b680"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "6246dc622f7139c2a0e16d2e03847d6494391fae"
SOURCE = C / "artifacts" / "batch-092-native-attempt-663"
DEST = R / "docs" / "n1-reviews" / "batch-092-native" / "execution-663"
EVIDENCE = R / "docs" / "n1-sources" / "execution-663.json"
NEXT = (
    "SAME092 serial dependent visual confirmations in ORIGINAL Claude session "
    "2f27854e-184a-4f54-8d7d-962197573318 then ORIGINAL GPT session "
    "4ff2dfd7-8eed-456f-8f4d-4acd64d2a820. Read docs/n1-sources/execution-663.json, "
    "archived actual PNGs/visual-inspection and original textual reports/limits. "
    "Use actual CLI catalog/tool support; one read-only reviewer at a time, wait for "
    "actual process exit and preserve complete reports. No new blind initial credit. "
    "Teaching6246dc62 unchanged. BOTH native cases terminal per-case0/no skips; full "
    "archive62c6d3e2 through productionContentSync ONCE:1115kanji/5070words/124N1/"
    "zeroProblems/contentVersion8445a5717d080dcc/acceptedRoom readingEpoch1. "
    "All16 scopedHan readable in THREE actualCompose panels across FOURproductionfont "
    "selections, especially fallbackU+5202;64individual+4wholewordPaint probes NOT "
    "separately viewed PNGs or identified fallbackface. Coordinator viewed25original "
    "PNGs; all42captured preserved, remaining17 not separately viewed. N1/All production "
    "choices exactly mow;reap vs 乃/凹/凸, all3curatedwrongcards/no fallback. ONLY kunかる "
    "offered/persistedGood/Done, NOon keys; raw onガイ,カイ and kunか.る sourceorder "
    "retained in full/Lite. Both刈除readings recognized/unselected, not sourceonly/obsolete. "
    "FOURpinnedstrokes injectedtrace/recall/persistence; BOTHcompletearticles/ONEallmapped"
    "baselinepair/TWOdirections/SystemBack/offline/N1selection/meaning/reading/drawing. "
    "ReusedN3刈る identity/reading/title/level/original切るguard preserved; componentlink "
    "and direct収穫guard only. Shapeonlymnemonic/刀-visible刂 distinction. Injectedtrace/"
    "giveup NOT humanhandwriting/MLKit/phone; actualUI shows modelunavailable/shapeonly. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "Owned5580helper25788/qemu4008 stopped. Parent19008 retains runner.lock; verifylive"
    "ancestry/session/checkpoint/exactsignedheads/whollyclean, NOchild reacquisition/"
    "delete/unlock. Approvedcontrol/committedpackets only, NOT optionalhistoricalsession"
    "recipes. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "All originalsource/baseline/link/reading/twofamily/native/currentmainnormalmerge/"
    "changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIPruntimehash/original18000entries42MiBcompressed80MiBinflated"
    "56MiBretained/perfile-media-safepath/ownerissue gates remain. Published118/1228,"
    "1110remaining unchanged; physicalphone/generalrelease/whole-set outstanding. "
    "No093/runtimepublication."
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
    assert manifest["contentVersion"] == "8445a5717d080dcc"
    preparation = load(C / "batch-092-native-fixture-verification.json")
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
    assert count == 8434
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "archiveManifestEqual": True,
            "manifestFreshAndUnchanged": True}


def prepare():
    verify_heads(HEAD, True)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["stage"]) == (
        662, "092", "batch-092-native-execution-in-progress")
    receipt = load(SOURCE / "execution.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"]
    raw = (SOURCE / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert raw.count("INSTRUMENTATION_STATUS_CODE: 0") == 2
    assert "OK (2 tests)" in raw
    assert "N1Batch092GlyphTest" in raw and "N1Batch092ArticleTest" in raw
    route = load(SOURCE / "n1-092-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"],
            route["problems"], route["acceptedReadingParserEpoch"]) == (1115, 5070, 124, 0, 1)
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["かる"]
    assert route["fullOnyomi"] == ["ガイ", "カイ"]
    assert route["fullKunyomi"] == ["か.る"]
    assert route["mappedReciprocalPairs"] == route["activatedBaselinePairs"] == 1
    assert route["directedLinkTransitions"] == route["completeArticleProjections"] == 2
    assert route["touchInjectedReferenceStrokes"] == 4
    raster = load(SOURCE / "n1-092-font-raster.json")
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"],
            raster["panels"]) == (64, 4, 3)
    assert len(raster["rows"]) == 68
    pngs = sorted(SOURCE.glob("*.png"))
    assert len(pngs) == 42
    inspected = [
        "font-panel-1", "font-panel-2", "font-panel-3",
        "kanji-01", "kanji-03", "kanji-09", "kanji-11", "kanji-20",
        "karu-02", "karu-04", "karu-07",
        "selection", "meaning-question", "meaning-feedback",
        "curated-かる-question", "curated-かる-feedback", "curated-one-kun-no-on-done",
        "drawing-trace", "drawing-feedback", "drawing-recall-feedback",
        "karu-forward", "karu-kanji-backlink", "karu-reverse",
        "karu-system-back-to-kanji", "karu-system-back-to-word",
    ]
    assert len(inspected) == 25
    visual = {
        "snapshot": TEACHING,
        "archiveSnapshot": receipt["contentSnapshot"],
        "reviewer": "Coordinator, actual GPT-6.1 Sol (gpt-6.1-sol); not independent review",
        "scope": "Native rendered content, all 16 scoped Han in four font selections, meaning/reading/drawing and both complete article routes.",
        "inspectedOriginalPngs": [
            {"file": f"n1-092-{name}.png", "sha256": sha(SOURCE / f"n1-092-{name}.png")}
            for name in inspected
        ],
        "capturedPngs": 42,
        "individuallyInspectedPngs": 25,
        "notSeparatelyInspectedPngs": 17,
        "glyphDisposition": "All 16 scoped Han readable/distinguishable in three original Compose panels across Gothic/Mincho/Textbook/Brush. U+5202 is visible as two upright strokes with the right hook, not a replacement box; absence from all three bundled cmaps plus actual native display supports usable system fallback, not identification of its face. 刈/切/刀/刂/乃/凹/凸 remain distinguishable; 刈除 legible across all four selections.",
        "articleDisposition": "Complementary original views and passing native selector/scroll assertions cover both complete articles. Readings table is horizontally scrollable as instructed; left/right views complement one another, not simultaneous full-column visibility. Both 刈除 readings remain recognized/unselected without obsolete/source-only claims. Cutting-versus-harvesting boundaries, shape-only mnemonic and canonical刀/visible刂 distinction, kana, translations and reciprocal links remain readable.",
        "quizDisposition": "Exactly one defensible mow/reap answer versus three visible curated wrong labels. Only kun かる offered; correct feedback and 1/1 Done visible. Full raw readings displayed in feedback are not extra offered keys.",
        "routeDisposition": "Forward/backlink/System Back views visible; one all-mapped/baseline pair and two directions. N1 selection and offline persistence asserted.",
        "drawingDisposition": "Four pinned strokes visible. Injected trace followed by recall give-up and persistence passed; model-unavailable/shape-only grading explicitly shown. Not human handwriting or successful MLKit recognition.",
        "findings": [],
        "limits": [
            "Not a fresh linguistic/source review or two-family dependent visual closure.",
            "Remaining 17 PNGs preserved but not separately visually inspected by this coordinator.",
            "64 individual and four whole-word Paint probes are not separately inspected PNGs.",
            "No physical phone, latest app-main, native-speaker or measured-learning acceptance.",
        ],
    }
    checked_runtime = runtime()
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
    for source in [C / "checkpoint-663.py", Path(__file__), C / "run-663-native.ps1"]:
        target = DEST / source.name
        shutil.copyfile(source, target)
        artifacts.append({"path": target.relative_to(R).as_posix(), "sha256": sha(target),
                          "bytes": target.stat().st_size})
    save(DEST / "visual-inspection.json", visual)
    artifacts.append({"path": (DEST / "visual-inspection.json").relative_to(R).as_posix(),
                      "sha256": sha(DEST / "visual-inspection.json")})
    review = load(R / "docs" / "n1-reviews" / "batch-092-reconciliation.json")
    evidence = {
        "schemaVersion": 1, "execution": 663, "batch": "092",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "rawOutputWhitespace": {
            "disposition": "Retain exact adb/emulator output bytes and hashes, including emitted trailing spaces/final blank lines; check generated evidence separately from raw logs.",
            "paths": [(DEST / "adb-operations.txt").relative_to(R).as_posix()],
        },
        "startingState": p["execution663StartingState"],
        "executionReceipt": receipt, "nativeRoute": route,
        "visualInspection": visual, "runtime": checked_runtime, "artifacts": artifacts,
        "textualReviewClosed": True, "independentVisualConfirmation": "pending",
        "originalReviewSessions": {
            model: review["processes"][key]["sessionId"]
            for model, key in [("claude-opus-5.5", "claude"), ("gpt-6.1-sol", "gpt")]
        },
        "freshOriginMain": git("rev-parse", "origin/main"),
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "independentReviewersLaunched": 0,
        "publishedAdditions": 118, "remainingAdditions": 1110,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT,
    }
    save(EVIDENCE, evidence)
    print("Both terminal cases and 8434 current/archive hashes verified; 42 PNGs preserved, 25 viewed.")


def finalize():
    saved = git("rev-parse", "HEAD")
    verify_heads(saved, True)
    assert git("rev-parse", "HEAD^") == HEAD
    changed = git("diff", "--name-only", HEAD, saved).splitlines()
    assert all(name.startswith(("docs/n1-reviews/batch-092-native/execution-663/",
                                "docs/n1-sources/execution-663.json")) for name in changed)
    evidence = load(EVIDENCE)
    for artifact in evidence["artifacts"]:
        assert sha(R.joinpath(*artifact["path"].split("/"))) == artifact["sha256"]
    issue = load(C / "batch-092-native-663-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    before = load(L / "progress-before-663.json")
    p = load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 663, "checkpoint": 663, "batch": "092",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmation",
        "evidence": "docs/n1-sources/execution-663.json",
        "contentArchiveHead": evidence["executionReceipt"]["contentSnapshot"],
        "reviewedTeachingSnapshot": TEACHING, "androidHead": APP,
        "terminalSuccessCases": 2, "skipped": 0,
        "nativeExecuted": True, "nativeCasesPassed": True,
        "coordinatorViewedPngs": 25, "capturedPngs": 42,
        "scopedHanInspected": 16, "productionFontSelections": 4,
        "runtimeHashesVerified": 8434, "contentVersion": "8445a5717d080dcc",
        "ownedHelperStopped": True, "ownedQemuStopped": True,
        "independentVisualConfirmation": "pending", "independentReviewersLaunched": 0,
        "dedicatedWorktreesClean": True, "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 118, "remainingAdditions": 1110,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT, "issueUpdate": issue["html_url"],
        "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    assert (p["checkpoint"], p["batch"], p["stage"]) == (
        662, "092", "batch-092-native-execution-in-progress")
    p.update(checkpoint=663, status="continue", stage=checkpoint["stage"],
             nextAction=NEXT, blocker=None)
    assert "execution663CoordinatorCheckpoint" not in p
    p["execution663CoordinatorCheckpoint"] = checkpoint
    p["batch092NativeAcceptanceCheckpoint"] = copy.deepcopy(checkpoint)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert p[key] == value, key
    temp = C / "progress.663.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")
    save(L / "native-663-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 663, "savedCommit": saved, "issue": issue["html_url"],
                      "historicalRootValuesPreserved": len(before), "status": "continue"}))


if __name__ == "__main__":
    {"prepare": prepare, "finalize": finalize}[sys.argv[1]]()
