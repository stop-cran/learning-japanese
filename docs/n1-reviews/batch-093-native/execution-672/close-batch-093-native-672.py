import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "01755ff6-fe55-417b-a9a1-0df278807936"
HEAD = "be6569bb5fae6c3ffa70a1c97514d27ce27ef8dc"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "27663944c7217a19e7de2f363e1b31a5f13452b6"
SOURCE = C / "artifacts" / "batch-093-native-attempt-672"
DEST = R / "docs" / "n1-reviews" / "batch-093-native" / "execution-672"
EVIDENCE = R / "docs" / "n1-sources" / "execution-672.json"
NEXT = (
    "SAME093 serial dependent visual confirmations in ORIGINAL Claude session "
    "c8c0a762-a31b-4dca-a1a0-bc010350ec18 then ORIGINAL GPT session "
    "feee7268-db4e-48e3-b7d6-f3568c7173b6. Read docs/n1-sources/execution-672.json, "
    "archived actual PNGs/visual-inspection and original textual reports/limits. "
    "Use actual CLI catalog/tool support; one read-only reviewer at a time, wait for "
    "actual process exit and preserve complete reports. No new blind initial credit. "
    "Teaching27663944 unchanged. BOTH native cases terminal per-case0/no skips; full "
    "archive324b0bd9 through productionContentSync ONCE:1116kanji/5070words/125N1/"
    "zeroProblems/contentVersionbf4cc85592bb9727/acceptedRoom readingEpoch1. "
    "All46 scopedHan readable in FIVE actualCompose panels across FOURproductionfont "
    "selections, especially fallbackU+4E85/U+5202/U+5F61;184individual+12wholewordPaint "
    "probes NOT separately viewed PNGs or identified fallbackface. Coordinator viewed32 "
    "original PNGs; all63captured preserved, remaining31 not separately viewed. "
    "N1/All productionchoices exactly criminal punishment vs 乃/凹/凸, all3curatedwrongcards/"
    "no fallback. ONLY onけい offered/persistedGood/Done, NOkun keys; full/Lite raw "
    "onケイ/emptykun, explicit[ケイ]/[] retained. Whole-wordでか NOT constituentkun; "
    "outside-freezeギョウ distinguished. SIXpinnedstrokes injectedtrace/recall/persistence; "
    "THREEcompletearticleprojections/TWOallmappedpairs/FOURdirections/ONEactivatedbaseline"
    "刑/刑事pair(NOT事/刑事)/SystemBack/offline/N1selection/meaning/reading/drawing. "
    "ReusedN3刑事 identity/reading/title/level/inbound探偵guard preserved; componentlink/"
    "fourDIRECTpolice-labelguards only;事 reciprocalnavigation only. Original GPT "
    "bookkeeping correction remains explicit. Injectedtrace/giveup NOT humanhandwriting/"
    "MLKit/phone; actualUI shows modelunavailable/shapeonly. QualifiedTESTONLYAndroid"
    "1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Owned5580helper5624/qemu15848 "
    "stopped. Parent19008 retains runner.lock; verifyliveancestry/session/checkpoint/"
    "exactsignedheads/whollyclean, NOchild reacquisition/delete/unlock. Approvedcontrol/"
    "committedpackets only, NOT optionalhistoricalsessionrecipes. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. All originalsource/baseline/link/"
    "reading/twofamily/native/currentmainnormalmerge/changedteachingreview/combinedchecks/"
    "normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPruntimehash/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/"
    "ownerissue gates remain. Published119/1228,1109remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No094/runtimepublication."
)
INSPECTED = [
    "font-panel-1", "font-panel-2", "font-panel-3", "font-panel-4", "font-panel-5",
    "selection", "meaning-question", "meaning-feedback",
    "curated-けい-question", "curated-けい-feedback", "curated-one-on-no-kun-done",
    "drawing-trace", "drawing-feedback", "drawing-recall-feedback",
    "kanji-09", "kanji-11", "kanji-12", "kanji-19", "kanji-20", "kanji-21",
    "keiji-02", "keiji-05", "keiji-07", "keiji-09", "keiji-11", "ji-22",
    "kanji-01", "ji-01", "kei-system-back-to-word", "ji-system-back-to-kanji",
    "ji-system-back-to-word", "keiji-system-back-to-kei",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def verify_heads(content_head, clean):
    for root, expected in [(R, content_head), (A, APP)]:
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        if clean:
            assert not git(root, "status", "--porcelain", "--untracked-files=all")
    assert not git(A, "diff", "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", APP,
                   "--", "app/src/main", "core/src/main", "gradle.properties")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    assert manifest["contentVersion"] == "bf4cc85592bb9727"
    preparation = load(C / "batch-093-native-fixture-verification.json")
    archive_path = Path(preparation["archive"])
    assert sha(archive_path) == preparation["archiveSha256"]
    count = 0
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) == 8458
        prefix = next(name[:-len("manifest.json")] for name in names if name.endswith("manifest.json"))
        assert json.loads(archive.read(prefix + "manifest.json")) == manifest
        assert archive_path.stat().st_size < 42 * 1024**2
        assert sum(info.file_size for info in archive.infolist()) == 44595396 < 80 * 1024**2
        assert preparation["retainedBytes"] == 44327058 < 56 * 1024**2
        assert len(names) < 18000
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
    assert count == 8436
    review = load(R / "docs" / "n1-reviews" / "batch-093-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "archiveManifestEqual": True,
            "manifestFreshAndUnchanged": True, "originalBudgetsPassed": True}


def prepare():
    verify_heads(HEAD, True)
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["batch"], state["stage"]) == (
        671, "093", "batch-093-native-execution-in-progress")
    receipt = load(SOURCE / "execution.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"]
    assert not receipt["parentLockTouched"] and not receipt["guestOrAppHeapChanged"] and not receipt["guardsChanged"]
    raw = (SOURCE / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0\s*$", raw, re.MULTILINE)) == 2
    assert "OK (2 tests)" in raw
    assert "N1Batch093GlyphTest" in raw and "N1Batch093ArticleTest" in raw
    assert not re.search(r"INSTRUMENTATION_STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED|assumptionFailure|ignored", raw)
    route = load(SOURCE / "n1-093-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"],
            route["problems"], route["acceptedReadingParserEpoch"]) == (1116, 5070, 125, 0, 1)
    assert route["quizOnKeys"] == ["けい"] and route["quizKunKeys"] == []
    assert route["fullOnyomi"] == ["ケイ"] and route["fullKunyomi"] == []
    assert route["mappedReciprocalPairs"] == 2 and route["activatedBaselinePairs"] == 1
    assert route["directedLinkTransitions"] == 4 and route["completeArticleProjections"] == 3
    assert route["touchInjectedReferenceStrokes"] == 6 and route["directWordGuardCount"] == 4
    for key in ["inboundTanteiGuardPreserved", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "onlyOnKeiNoKunPersistedGoodAndDone", "drawingTraceThenRecall", "drawingGradeRecordedOnNext", "offline"]:
        assert route[key], key
    expected = {"刑": "criminal punishment", "乃": "thereupon; possessive no",
                "凹": "concave; sunken", "凸": "convex; protruding"}
    for pool in route["productionBuilderN1AndAllExactChoices"].values():
        assert {item["kanji"]: item["title"] for item in pool["options"]} == expected
        assert pool["availableCuratedCount"] == 3 and pool["fallbackOptions"] == 0
    raster = load(SOURCE / "n1-093-font-raster.json")
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (184, 12, 5)
    assert len(raster["rows"]) == 196
    pngs = sorted(SOURCE.glob("*.png"))
    assert len(pngs) == 63 and len(set(INSPECTED)) == len(INSPECTED) == 32
    visual = {
        "snapshot": TEACHING, "archiveSnapshot": receipt["contentSnapshot"],
        "reviewer": "Coordinator, actual GPT-6.1 Sol (gpt-6.1-sol); not independent review",
        "scope": "Native rendered content, all 46 scoped Han in four font selections, meaning/reading/drawing and representative three-article route views.",
        "inspectedOriginalPngs": [{"file": f"n1-093-{name}.png", "sha256": sha(SOURCE / f"n1-093-{name}.png")} for name in INSPECTED],
        "capturedPngs": 63, "individuallyInspectedPngs": 32, "notSeparatelyInspectedPngs": 31,
        "glyphDisposition": "All 46 scoped Han readable and distinguishable in five original Compose panels across Gothic/Mincho/Textbook/Brush. U+4E85 shows a single hooked stem, U+5202 two upright strokes with the right hook, and U+5F61 three slanting strokes, not blank/replacement boxes. Their absence from all three bundled cmaps plus actual native display supports usable system fallback, not identification of its face. Punishment/form/mold and knife/hair/hook comparisons remain distinguishable. Three whole words render legibly across all four selections; Textbook wraps within 刑罰 in the dense comparison panel without losing a character.",
        "articleDisposition": "Viewed new article opening/mnemonic, complementary horizontally scrollable reading-table columns, wider ギョウ note, semantic/shape comparisons, whole-word でか note, reused 刑事 senses/examples/combination/boundaries and new 事 reciprocal line. Text and kana readable in inspected views. Passing native selector/scroll assertions cover all three complete article projections; 31 remaining screenshots were preserved, not separately inspected. Unchanged 事 prose is contextual, not a fresh linguistic review.",
        "quizDisposition": "Visible question has one defensible criminal-punishment answer versus three curated wrong labels. Actual N1 and All default-four builder pools have all three curated cards, zero fallback; arbitrary pool sizes remain uncertified. Only on けい offered; correct feedback and 1/1 Done visible. No kun keys. Four direct police-label safeguards and inbound 探偵 safeguard asserted.",
        "routeDisposition": "System Back return views inspected for both all-mapped pairs; four directed transitions and one activated baseline 刑/刑事 pair asserted. N1 selection and offline persistence passed; no owner progress used.",
        "drawingDisposition": "All six pinned reference strokes visible; injected trace, recall give-up and persistence passed. Model-unavailable/shape-only grading is explicitly shown. Not human handwriting or successful MLKit recognition.",
        "verdicts": {
            "kanji/刑.md": {"renderedComprehensibility": "CLEAN", "scope": "Inspected native views and all scoped glyphs; original textual verdicts inherited, not repeated."},
            "words/刑事.md": {"renderedComprehensibility": "CLEAN", "scope": "Inspected complete reused article presentation across complementary views."},
            "kanji/事.md:37": {"renderedComprehensibility": "CLEAN", "scope": "Added reciprocal line and contextual opening; unchanged article not freshly linguistically reviewed."},
        },
        "findings": [], "optional": "None established in bounded rendered scope.",
        "limits": [
            "Not a fresh linguistic/source review or two-family dependent visual closure.",
            "Remaining 31 PNGs preserved but not separately visually inspected by this coordinator.",
            "184 individual and twelve whole-word Paint probes are not separately inspected PNGs.",
            "No physical phone, latest app-main, native-speaker or measured-learning acceptance.",
        ],
    }
    checked_runtime = runtime()
    assert not DEST.exists() and not EVIDENCE.exists()
    DEST.mkdir()
    artifacts = []
    inputs = list(sorted(SOURCE.iterdir())) + [
        C / "execute-batch-093-native-672.py", Path(__file__), C / "run-672-native.ps1",
        L / "native-wrapper-provenance.json",
    ]
    for source in inputs:
        assert source.is_file()
        target = DEST / source.name
        assert not target.exists()
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        artifacts.append({"path": target.relative_to(R).as_posix(), "sha256": sha(target), "bytes": target.stat().st_size})
    save(DEST / "visual-inspection.json", visual)
    artifacts.append({"path": (DEST / "visual-inspection.json").relative_to(R).as_posix(),
                      "sha256": sha(DEST / "visual-inspection.json")})
    review = load(R / "docs" / "n1-reviews" / "batch-093-reconciliation.json")
    evidence = {
        "schemaVersion": 1, "execution": 672, "batch": "093",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingState": state["execution672StartingState"], "executionReceipt": receipt,
        "nativeRoute": route, "visualInspection": visual, "runtime": checked_runtime, "artifacts": artifacts,
        "rawOutputWhitespace": "Retain exact adb/emulator output bytes and hashes, including emitted trailing spaces/final blank lines; check authored evidence separately from raw logs.",
        "textualReviewClosed": True, "independentVisualConfirmation": "pending",
        "originalReviewSessions": {model: review["processes"][key]["sessionId"]
                                   for model, key in [("claude-opus-5.5", "claude"), ("gpt-6.1-sol", "gpt")]},
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "independentReviewersLaunched": 0,
        "publishedAdditions": 119, "remainingAdditions": 1109, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    }
    save(EVIDENCE, evidence)
    print("Both terminal cases and 8436 current/archive hashes verified; 63 PNGs preserved, 32 viewed.")


def finalize():
    saved = git(R, "rev-parse", "HEAD")
    verify_heads(saved, True)
    assert git(R, "rev-parse", "HEAD^") == HEAD
    changed = git(R, "-c", "core.quotepath=false", "diff", "--name-only", HEAD, saved).splitlines()
    assert all(name.startswith(("docs/n1-reviews/batch-093-native/execution-672/",
                                "docs/n1-sources/execution-672.json")) for name in changed)
    evidence = load(EVIDENCE)
    for artifact in evidence["artifacts"]:
        assert sha(R.joinpath(*artifact["path"].split("/"))) == artifact["sha256"]
    issue = load(C / "batch-093-native-672-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-093-native-672-issue-body.txt").read_text(encoding="utf-8")
    before = load(L / "progress-before-672.json")
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["batch"], state["stage"]) == (
        671, "093", "batch-093-native-execution-in-progress")
    checkpoint = {
        "schemaVersion": 1, "execution": 672, "checkpoint": 672, "batch": "093",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmation",
        "evidence": "docs/n1-sources/execution-672.json",
        "contentArchiveHead": evidence["executionReceipt"]["contentSnapshot"],
        "reviewedTeachingSnapshot": TEACHING, "androidHead": APP,
        "terminalSuccessCases": 2, "skipped": 0, "nativeExecuted": True, "nativeCasesPassed": True,
        "coordinatorViewedPngs": 32, "capturedPngs": 63, "scopedHanInspected": 46, "productionFontSelections": 4,
        "runtimeHashesVerified": 8436, "contentVersion": "bf4cc85592bb9727",
        "ownedHelperStopped": True, "ownedQemuStopped": True,
        "independentVisualConfirmation": "pending", "independentReviewersLaunched": 0,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 119, "remainingAdditions": 1109, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT, "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=672, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    assert "execution672CoordinatorCheckpoint" not in state and "batch093NativeAcceptanceCheckpoint" not in state
    state["execution672CoordinatorCheckpoint"] = checkpoint
    state["batch093NativeAcceptanceCheckpoint"] = copy.deepcopy(checkpoint)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    temp = C / "progress.672.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")
    save(L / "native-672-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 672, "savedCommit": saved, "issue": issue["html_url"],
                      "historicalRootValuesPreserved": len(before), "status": "continue"}))


if __name__ == "__main__":
    {"prepare": prepare, "finalize": finalize}[sys.argv[1]]()
