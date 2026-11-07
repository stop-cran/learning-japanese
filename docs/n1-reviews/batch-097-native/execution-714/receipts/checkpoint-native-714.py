import copy
import gzip
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "d0490dbe-b3a1-40f6-a8a1-7cfc0f16a6cf"
HEAD = "1069a0463dcb497682f8336064f6cb3897b3388b"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
N = C / "artifacts" / "batch-097-native-attempt-714"
I = C / "batch-097-native-inspection-714"
D = R / "docs" / "n1-reviews" / "batch-097-native" / "execution-714"
E = R / "docs" / "n1-sources" / "execution-714.json"
STAGE = "batch-097-native-executed-awaiting-rendered-confirmations"
NEXT = (
    "SAME097 serial bounded rendered confirmations in ORIGINAL reviewer sessions next: "
    "Claude 3a0b6dd8-6212-4ceb-a430-3127aac6969e THEN GPT 9f31594c-f091-4d47-9276-12249f0c848d. "
    "Read docs/n1-sources/execution-714.json and docs/n1-reviews/batch-097-native/execution-714/. "
    "BOTH native cases terminal0/no skips; full archive83e5c090/versiona066afceaf1f447a/"
    "8447hashes through productionContentSync ONCE:1120kanji/5073words/129N1/zeroProblems/Roomepoch1. "
    "Coordinator inspected all55PNG: THREEfourfontpanels/all20Han plus52routecaptures via13contactsheets; "
    "no actionable visual defect established, visible U+5202 fallback; exact fallback face unidentified. "
    "Actual default N1 options: sword/double-edgedblade vs dissect/splitopen, sturdy/unyieldingstrength and mosquito. "
    "TWO curated wrongcards available; ONE productionfallback captured (mosquito), NOT則N2. "
    "Inspect exact64 imported builder records/16seeds/N1+All+boundedcustom+randomN1subset "
    "and512 FOUR directwordguard checks from剣つるぎ/All+custom/bothdirections/bothtargetorientations. "
    "27 unique sampled builder labels include矛/spear/polearm (different weapon, not sword); "
    "plus蚊/mosquito in actualUI. Samples are NOT whole-pool semantic certification. "
    "BOTHonけん/kunつるぎ offered/persistedGood/Done; full/Lite rawケン/[つるぎ] and explicitケン/[つるぎ] retained. "
    "TEN injectedstrokes/trace+giveuprecall/persistence; TWO complete articleprojections剣/剣つるぎ, "
    "exact reused真剣component/真commonword changes, THREE allmapped reciprocalpairs/SIXdirections/"
    "ONEactivatedbaselinepair/SystemBack/offline/N1selection. "
    "Original-session followups are dependent confirmations, NOT newblindcredit. OwnedAPI35 emulator5580/"
    "parent4544/qemu3552 stopped; no owner/shared devices/heaps/guards changed, no phone/"
    "humanhandwriting/MLKit acceptance. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOT latestappmain; fresh712 JVM4/no skips retained. All original source/baseline/link/reading/"
    "twofamily/native/currentmainnonrewritingmerge/changedteachingreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPentryhash/unchanged18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue gates remain. "
    "Parent19008 retainsrunner.lock: verifyliveancestry/session/signedheads/whollyclean, NOchildacquire/"
    "delete/unlock/readprobe. Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Published123/1228,1105remaining "
    "unchanged; physicalphone/generalrelease/whole-set outstanding. No098/runtimepublication/secondrunner."
)


def load(path):
    return json.loads(path.read_bytes())


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain", "--untracked-files=all")


def runtime():
    path = C / "prepare-batch-097-native-713.py"
    frozen = load(R / "docs" / "n1-sources" / "execution-713.json")
    recipe = next(x for x in frozen["provenance"] if x.get("source") == str(path))
    assert sha(path) == recipe["sha256"]
    spec = importlib.util.spec_from_file_location("prepared097", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.runtime()


def persist(state):
    temp = C / "progress.714.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")


def collect():
    clean()
    assert not D.exists() and not E.exists()
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 713 and progress["stage"] == "batch-097-native-execution-in-progress"
    receipt = load(C / "batch-097-native-attempt-714-execution.json")
    route = load(N / "n1-097-article-route.json")
    raster = load(N / "n1-097-font-raster.json")
    frozen = load(R / "docs" / "n1-sources" / "execution-713.json")
    verification = frozen["fixtureVerification"]
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert not any(receipt[k] for k in ["parentLockTouched", "guestOrAppHeapChanged", "guardsChanged"])
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"],
            route["acceptedReadingParserEpoch"]) == (1120, 5073, 129, 0, 1)
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"],
            route["completeArticleProjections"], route["activatedBaselinePairs"],
            route["changedReusedArticles"]) == (3, 6, 2, 1, 2)
    assert route["bothKenAndTsurugiPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 10 and route["drawingGradeRecordedOnNext"]
    assert route["actualN1CuratedAvailable"] == 2 and route["actualN1FallbackOptions"] == 1
    assert len(route["directGuardBuilderChecks"]) == 512
    for row in route["directGuardBuilderChecks"]:
        assert len(row["options"]) == 4
        assert sum(o["word"] == row["target"] for o in row["options"]) == 1
        assert not any(o["word"] == row["excluded"] for o in row["options"])
    pools = route["productionBuilderN1AndAllExactChoices"]
    assert len(pools) == 64
    for name in ["N1", "All", "boundedCustom", "randomN1Subset"]:
        rows = [r for r in pools if r["pool"] == name]
        assert sorted(r["seed"] for r in rows) == list(range(16))
        for row in rows:
            assert len(row["options"]) == len({o["title"] for o in row["options"]}) == 4
            assert sum(o["kanji"] == "\u5263" for o in row["options"]) == 1
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (80, 8, 3)
    assert len(raster["rows"]) == 88
    log = (N / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0\s*$", log, re.MULTILINE)) == 2
    assert "OK (2 tests)" in log
    assert not re.search(r"STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED|assumptionFailure|ignored", log)
    for path, digest in [(verification["archive"], verification["archiveSha256"]),
                         (verification["fixture"], verification["fixtureSha256"]),
                         (frozen["appApk"]["path"], frozen["appApk"]["sha256"]),
                         (frozen["testApk"]["path"], frozen["testApk"]["sha256"])]:
        assert sha(Path(path)) == digest
    manifest = runtime()
    with zipfile.ZipFile(verification["archive"]) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) == verification["zipEntries"] < 18000
        assert Path(verification["archive"]).stat().st_size < 42 * 1024**2
        assert sum(item.file_size for item in archive.infolist()) == verification["inflatedBytes"] < 80 * 1024**2
        entry = next(n for n in names if n.endswith("/manifest.json"))
        prefix = entry[:-len("manifest.json")]
        assert json.loads(archive.read(entry)) == manifest
        count = 0
        retained = archive.getinfo(entry).file_size
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, digest in entries.items():
                data = archive.read(prefix + name)
                retained += len(data)
                local = R.joinpath(*name.split("/")).read_bytes()
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                if not binary:
                    data, local = data.replace(b"\r\n", b"\n"), local.replace(b"\r\n", b"\n")
                assert data == local and hashlib.sha256(data).hexdigest() == digest, name
                count += 1
        assert count == 8447 and retained == verification["retainedBytes"] < 56 * 1024**2
    D.mkdir()
    for source in sorted(N.iterdir()):
        assert source.is_file()
        if source.suffix == ".txt":
            archived = D / (source.name + ".gz")
            archived.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(archived.read_bytes()) == source.read_bytes()
        else:
            shutil.copyfile(source, D / source.name)
            assert sha(source) == sha(D / source.name)
    shutil.copytree(I, D / "contact-sheets")
    assert len(list(D.glob("*.png"))) == 55
    recipes = D / "receipts"
    recipes.mkdir()
    for source in [Path(__file__), C / "start-execution-714.py", C / "preflight-714.ps1",
                   C / "run-714-native.ps1", C / "inspect-batch-097-native-714.py",
                   L / "preflight-714.json", C / "runner-lock-role-notes.txt",
                   C / "authoring-artifact-path-notes.txt"]:
        shutil.copyfile(source, recipes / source.name)
    unique = sorted({json.dumps(o, ensure_ascii=False, sort_keys=True) for row in pools for o in row["options"]})
    assert len(unique) == 27
    visual = {
        "snapshot": verification["contentSnapshot"],
        "reviewedTeachingSnapshot": verification["reviewedTeachingSnapshot"],
        "reviewer": "Coordinator, GPT-6.1 Sol (gpt-6.1-sol)",
        "scope": "Native rendered inspection, not a new independent linguistic/source review.",
        "inspectedOriginalPngCount": 55,
        "fontPanelsInspectedAtOriginalResolution": [f"n1-097-font-panel-{i}.png" for i in range(1, 4)],
        "routeCapturesInspectedViaContactSheets": 52,
        "contactSheetsInspected": [f"contact-sheets/sheet-{i:02d}.png" for i in range(1, 14)],
        "additionalOriginalResolutionReads": [
            "n1-097-selection.png", "n1-097-meaning-question.png", "n1-097-meaning-feedback.png",
            "n1-097-kanji-01.png", "n1-097-kanji-09.png", "n1-097-kanji-17.png",
            "n1-097-tsurugi-02.png", "n1-097-tsurugi-07.png", "n1-097-tsurugi-09.png",
            "n1-097-shin-forward.png", "n1-097-shinken-reverse.png",
            "n1-097-curated-\u3051\u3093-question.png", "n1-097-curated-\u3051\u3093-feedback.png",
            "n1-097-curated-\u3064\u308b\u304e-question.png", "n1-097-curated-\u3064\u308b\u304e-feedback.png",
            "n1-097-curated-on-kun-done.png", "n1-097-drawing-trace.png",
            "n1-097-drawing-feedback.png", "n1-097-drawing-recall-feedback.png",
        ],
        "verdict": "No actionable visual defect established in these captures; original-session confirmations and bounded semantic adjudication remain.",
        "glyphs": "All20 scoped Han readable across Gothic/Mincho/Textbook/Brush; sword and look-alikes distinguishable. Cmap-absent U+5202 visibly renders without blank/tofu across four families. Exact fallback face not identified. Both whole-word examples visible in panel3.",
        "articles": "Two complete article projections and the exact two reused changes covered. Japanese/examples/translations and links readable. Reading table needs advertised horizontal scroll; right-scrolled captures expose full example text, with expected left-column clipping. Later captures cover vertically clipped paragraphs.",
        "quiz": "Actual N1 UI has sword/double-edged blade vs dissect/split open, sturdy/unyielding strength and mosquito. Mosquito is the single actual fallback, not N2 rule/follow a model. These are semantically distinct. All64 builder records read; 27 unique sampled labels include spear/polearm, another weapon, not a synonym for sword. Original-session semantic confirmation remains; not unrestricted pool certification.",
        "sampledBuilderDistinctOptions": [json.loads(o) for o in unique],
        "actualDefaultMeaningOptions": route["exactDefaultMeaningOptions"],
        "reading": "Both on and kun question/feedback captures readable and correct; Done2/2. Full/Lite raw and explicit curated lists retained; both normalized keys persisted Good.",
        "drawing": "Injected ten-stroke reference trace and shape-only feedback visible; recall give-up displays reference and persists grade on Next. Offline model-unavailable state is explicit. No human-handwriting/MLKit acceptance.",
        "newConsequentialUnresolvedVisualClaims": [],
        "limits": [
            "API35 emulator at default fontScale1 only; physical phone/general-release acceptance outstanding.",
            "hasGlyph/nonblank/raster hashes alone are not legibility/fallback-face evidence; actual panels inspected.",
            "No new blind reviewers or independent rendered confirmations in execution714.",
            "64kanji/512word builder checks are bounded seed/pool samples, not exhaustive random-pool safety.",
            "Four direct guards prove those pairs absent, not semantic safety of every other word option.",
            "Original two-family textual review is inherited; changed reused scope only, not a fresh full review of reused articles.",
        ],
    }
    save(D / "coordinator-visual-inspection.json", visual)
    index = [{"path": f.relative_to(R).as_posix(), "sha256": sha(f)}
             for f in sorted(D.rglob("*")) if f.is_file()]
    save(D / "artifact-index.json", index)
    evidence = {
        "schemaVersion": 1, "execution": 714, "batch": "097", "status": STAGE,
        "startingState": copy.deepcopy(progress["execution714StartingState"]),
        "contentSnapshot": verification["contentSnapshot"],
        "reviewedTeachingSnapshot": verification["reviewedTeachingSnapshot"],
        "androidHead": APP, "productionBaseline": verification["productionBaseline"],
        "qualifiedTestOnlyAndroid": True, "latestAppMainClaimed": False,
        "fixtureSha256": verification["fixtureSha256"], "archiveSha256": verification["archiveSha256"],
        "appApk": frozen["appApk"], "testApk": frozen["testApk"],
        "contentVersion": manifest["contentVersion"], "runtimeHashesVerifiedAgain": count,
        "exactArchiveAndLocalRuntimeBytesEqual": True, "archiveGuardsUnchanged": True,
        "archiveBudgetEvidence": "docs/n1-sources/execution-713.json",
        "nativeExecution": receipt, "nativeTestsPassed": 2, "nativeTestsSkipped": 0,
        "terminalPerCaseStatus": [0, 0], "fullArchiveImportedOnce": True,
        "importedKanji": 1120, "importedWords": 5073, "n1Cards": 129, "problems": 0,
        "acceptedReadingParserEpoch": 1, "kanjiBuilderChecks": 64,
        "newDirectWordGuardBuilderChecks": 512, "newDirectWordGuardPairs": 4,
        "allMappedReciprocalPairs": 3, "directedLinkTransitions": 6,
        "activatedBaselinePairs": 1, "completeArticleProjections": 2, "changedReusedArticles": 2,
        "individualGlyphProbes": 80, "wholeWordRasterProbes": 8, "fontPanels": 3,
        "originalPngCaptures": 55, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED",
        "nativeExecutionAndCoordinatorVisualInspection": "passed",
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "runtimeChanged": False, "independentReviewersLaunched": 0, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "publishedAdditions": 123, "remainingAdditions": 1105,
        "lastPublishedCommit": progress["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "routeEvidence": (D / "n1-097-article-route.json").relative_to(R).as_posix(),
        "fontEvidence": (D / "n1-097-font-raster.json").relative_to(R).as_posix(),
        "visualInspection": (D / "coordinator-visual-inspection.json").relative_to(R).as_posix(),
        "artifactIndex": (D / "artifact-index.json").relative_to(R).as_posix(),
        "limits": visual["limits"], "nextAction": NEXT,
        "diagnostics": [
            "Full request loaded/decoded before acting; initial console output failed under cp1252, corrected to UTF-8.",
            "Initial guessed acceptance filename absent; read actual article-route.json from file inventory instead.",
            "First evidence collection stopped before writes at a provenance field-name mismatch; corrected against the actual pinned preparation record.",
            "All raw text logs archived as deterministic lossless gzip.",
        ],
    }
    save(E, evidence)
    path = R / "docs" / "n1-sources" / "batch-097-progress.json"
    packet = load(path)
    assert not packet["runtimeAccepted"] and not packet["runtimePublished"]
    packet.update(status=STAGE, nextAction=NEXT)
    packet["pendingGates"][0] = "Native execution714 passed; serial original-session rendered confirmations and evidence-based semantic adjudication of actual N1/All/custom/random choices remain."
    packet["androidAcceptance"]["nativeAcceptance"] = "execution714-passed-awaiting-original-session-rendered-confirmations"
    packet["nativeExecution714"] = {
        "evidence": "docs/n1-sources/execution-714.json", "status": STAGE,
        "terminalPerCaseStatus": [0, 0], "testsSkipped": 0, "coordinatorInspectedPngCount": 55,
        "fullArchiveImportedOnce": True, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED", "runtimeAccepted": False, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier native-pending fields remain historical; this additive record supersedes native execution/visual state only, not independent review/publication.",
    }
    save(path, packet)
    subprocess.run(["git", "-C", str(R), "diff", "--check"], check=True)
    print("Verified native receipts/all55PNGs archived; runtime untouched.")


def checkpoint():
    progress = load(C / "progress.json")
    original = load(L / "checkpoint-full.json")
    assert original["checkpoint"] == 713 and progress["checkpoint"] == 713
    head = git(R, "rev-parse", "HEAD")
    assert git(R, "rev-parse", "HEAD^") == HEAD
    clean(head)
    assert not git(R, "diff", HEAD, head, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    paths = git(R, "diff", "--name-only", HEAD, head).splitlines()
    assert all(n.startswith(("docs/n1-reviews/batch-097-native/execution-714/",
                             "docs/n1-sources/execution-714.json", "docs/n1-sources/batch-097-progress.json")) for n in paths)
    posted = load(C / "batch-097-native-714-issue-receipt.json")
    assert posted["user"]["login"] == "stop-cran"
    assert posted["body"] == (C / "batch-097-native-714-issue-body.txt").read_bytes().decode("utf-8-sig")
    for item in load(D / "artifact-index.json"):
        assert sha(R.joinpath(*item["path"].split("/"))) == item["sha256"]
    runtime()
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[k] == v for k, v in original.items() if k not in mutable)
    record = {
        "schemaVersion": 1, "execution": 714, "checkpoint": 714, "batch": "097",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "evidence": "docs/n1-sources/execution-714.json",
        "nativeTestsPassed": 2, "terminalPerCaseStatus": [0, 0], "testsSkipped": 0,
        "coordinatorInspectedPngCount": 55, "fullArchiveImportedOnce": True,
        "runtimeHashesVerifiedAgain": 8447, "kanjiBuilderChecks": 64,
        "directWordGuardBuilderChecks": 512, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED", "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "ownedEmulatorStopped": True, "serial": "emulator-5580", "parentEmulatorPid": 4544, "qemuPid": 3552,
        "publishedAdditions": 123, "remainingAdditions": 1105, "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": posted["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(original),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=714, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    progress["execution714CoordinatorCheckpoint"] = record
    progress["batch097NativeExecutionCheckpoint"] = copy.deepcopy(record)
    persist(progress)
    saved = load(C / "progress.json")
    assert all(saved[k] == v for k, v in original.items() if k not in mutable)
    save(L / "checkpoint-714-verification.json", record)
    print(json.dumps({"checkpoint": 714, "savedCommit": head, "historyPreserved": True,
                      "issueUpdate": posted["html_url"]}, indent=2))


if __name__ == "__main__":
    {"collect": collect, "checkpoint": checkpoint}[sys.argv[1]]()
