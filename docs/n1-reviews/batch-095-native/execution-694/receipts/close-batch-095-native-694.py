import copy
import datetime
import gzip
import hashlib
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys

CONTROL = pathlib.Path(__file__).parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
SESSION = "6538b1ef-d7d4-465b-bd47-d66aa8a6ea9f"
LOGS = CONTROL / "logs" / SESSION
NATIVE = CONTROL / "artifacts" / "batch-095-native-attempt-694"
INSPECTION = CONTROL / "batch-095-native-inspection-694"
DEST = ROOT / "docs" / "n1-reviews" / "batch-095-native" / "execution-694"
EVIDENCE = ROOT / "docs" / "n1-sources" / "execution-694.json"
HEAD = "95be0577bea120a757bccd190625499b01e94a63"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
STAGE = "native-executed-awaiting-rendered-confirmations"
NEXT = (
    "SAME095 serial bounded rendered confirmations in ORIGINAL reviewer sessions next: "
    "Claude ede78c28-e889-47b5-be0b-21533da61551 THEN GPT ee7498e0-d3ad-46bf-bbc9-82761892cab0. "
    "Read docs/n1-sources/execution-694.json and docs/n1-reviews/batch-095-native/execution-694/. "
    "BOTH native cases terminal0/no skips; exact fullarchivecc748347/version463619d79972e9f2/"
    "8441hashes through productionContentSync ONCE:1118kanji/5071words/127N1/zeroProblems/Roomepoch1. "
    "Coordinator inspected all60PNG: FOURfourfontpanels/all32Han and56routecaptures via14contactsheets; "
    "no actionable visual defect established, visible U+4EBB/U+5202/U+961D fallback. "
    "Actual default N1 options:剖/dissect;split open,冒/brave danger;venture,刈/mow;reap,企/plan;undertake. "
    "N1 has ZERO curated wrongcards since部N3/倍N2/副N2 excluded; THREE productionfallbacks preserved. "
    "Inspect exact64 imported builder records/16seeds/N1+All+boundedcustom+randomN1subset and384 "
    "THREE directwordguards解剖/分析,解剖/分解,解剖/検査/bothdirections/bothtargetorientations/"
    "All+custom. All64+384records preserved, NOT whole-pool semantic certification. "
    "Onlyonぼう/noKun offered/persistedGood/Done; full/Lite rawボウ/[] and explicitボウ/[] retained. "
    "TEN injectedstrokes/trace+giveuprecall/persistence; THREE complete articleprojections剖/解剖/解, "
    "TWO allmapped reciprocalpairs/FOURdirections/zeroactivatedbaselinepairs/SystemBack/offline/N1selection. "
    "Original-session followups are dependent confirmations, NOT newblindcredit. Exact ownedAPI35 "
    "emulator5580/parent5536/qemu14252 stopped; no owner/shared devices/heaps/guards changed, "
    "no phone/humanhandwriting/MLKit acceptance. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOT latestappmain; fresh692 JVM4/no skips retained. All original source/baseline/link/reading/"
    "twofamily/native/currentmainnonrewritingmerge/changedteachingreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPentryhash/unchanged18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue gates remain. "
    "Parent19008 retainsrunner.lock: verifyliveancestry/session/signedheads/whollyclean, "
    "NOchildacquire/delete/unlock. Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper "
    "access. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. FreshoriginMain "
    "da374717 advances lastpublished d6a26190; integrate later, NOT accepted here. "
    "Published121/1228,1107remaining unchanged; physicalphone/generalrelease/whole-set outstanding. "
    "No096/runtimepublication/secondrunner."
)


def load(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   text=True, encoding="utf-8").strip()


def runtime():
    recipe = CONTROL / "prepare-batch-095-native-693.py"
    assert sha(recipe) == "37e0104c5321f192f57fc1987c0d399972102a8ca278eea37100d8bf460dbbab"
    spec = importlib.util.spec_from_file_location("prepared095", recipe)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return helper.runtime()


def persist(state):
    temporary = CONTROL / "progress.694.tmp"
    assert not temporary.exists()
    save(temporary, state)
    assert load(temporary) == state
    temporary.replace(CONTROL / "progress.json")


def packet_fields():
    path = ROOT / "docs" / "n1-sources" / "batch-095-progress.json"
    current = load(path)
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{HEAD}:docs/n1-sources/batch-095-progress.json"])
    text = original.decode("utf-8")
    decoder = json.JSONDecoder()
    for key in ["status", "nextAction", "pendingGates", "androidAcceptance"]:
        match = re.search(r'^  "' + key + r'": ', text, re.MULTILINE)
        assert match
        _, end = decoder.raw_decode(text, match.end())
        value = json.dumps(current[key], ensure_ascii=False, indent=2).replace("\n", "\n  ")
        text = text[:match.end()] + value + text[end:]
    end = text.rfind("}")
    extra = json.dumps({"nativeExecution694": current["nativeExecution694"]}, ensure_ascii=False, indent=2)[1:-1]
    text = text[:end].rstrip() + "," + extra + "\n" + text[end:]
    assert json.loads(text) == current
    path.write_bytes(text.encode("utf-8"))


def prepare():
    for root, expected in [(ROOT, HEAD), (ANDROID, APP)]:
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain", "--untracked-files=all")
    assert not DEST.exists() and not EVIDENCE.exists()
    compiled = load(ROOT / "docs" / "n1-sources" / "execution-693.json")
    frozen = compiled["fixtureVerification"]
    receipt = load(CONTROL / "batch-095-native-attempt-694-execution.json")
    route = load(NATIVE / "n1-095-article-route.json")
    raster = load(NATIVE / "n1-095-font-raster.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert not receipt["parentLockTouched"] and not receipt["guardsChanged"] and not receipt["guestOrAppHeapChanged"]
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"],
            route["acceptedReadingParserEpoch"]) == (1118, 5071, 127, 0, 1)
    assert len(route["directGuardBuilderChecks"]) == 384
    for row in route["directGuardBuilderChecks"]:
        assert len(row["options"]) == 4
        assert sum(o["word"] == row["target"] for o in row["options"]) == 1
        assert not any(o["word"] == row["excluded"] for o in row["options"])
    pools = route["productionBuilderN1AndAllExactChoices"]
    assert len(pools) == 64
    for pool in ["N1", "All", "boundedCustom", "randomN1Subset"]:
        rows = [r for r in pools if r["pool"] == pool]
        assert sorted(r["seed"] for r in rows) == list(range(16))
        for row in rows:
            assert len(row["options"]) == len({o["title"] for o in row["options"]}) == 4
            assert sum(o["kanji"] == "剖" for o in row["options"]) == 1
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"],
            route["completeArticleProjections"], route["activatedBaselinePairs"]) == (2, 4, 3, 0)
    assert route["onlyOnBouNoKunPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 10 and route["drawingGradeRecordedOnNext"]
    assert route["actualN1CuratedAvailable"] == 0 and route["actualN1FallbackOptions"] == 3
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (128, 8, 4)
    assert len(raster["rows"]) == 136
    log = (NATIVE / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0\s*$", log, re.MULTILINE)) == 2
    assert "OK (2 tests)" in log
    assert not re.search(r"STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED|assumptionFailure|ignored", log)
    for path, digest in [(frozen["archive"], frozen["archiveSha256"]),
                         (frozen["fixture"], frozen["fixtureSha256"]),
                         (compiled["testApk"]["path"], compiled["testApk"]["sha256"]),
                         (compiled["appApk"]["path"], compiled["appApk"]["sha256"])]:
        assert sha(pathlib.Path(path)) == digest
    runtime()
    verified = load(LOGS / "runtime-694.json")
    assert verified["runtimeHashesVerified"] == 8441 and verified["exactArchiveAndLocalBytesEqual"]
    assert verified["archiveSha256"] == frozen["archiveSha256"]
    DEST.mkdir()
    for source in sorted(NATIVE.iterdir()):
        assert source.is_file()
        if source.name in {"adb-operations.txt", "emulator-stdout.txt"}:
            data = source.read_bytes()
            archived = DEST / (source.name + ".gz")
            archived.write_bytes(gzip.compress(data, mtime=0))
            assert gzip.decompress(archived.read_bytes()) == data
        else:
            shutil.copyfile(source, DEST / source.name)
            assert sha(source) == sha(DEST / source.name)
    sheets = DEST / "contact-sheets"
    shutil.copytree(INSPECTION, sheets)
    assert len(list(DEST.glob("*.png"))) == 60 and len(list(sheets.glob("*.png"))) == 14
    recipes = DEST / "receipts"
    recipes.mkdir()
    for source in [pathlib.Path(__file__), CONTROL / "start-execution-694.py",
                   CONTROL / "preflight-694.ps1", CONTROL / "run-694-native.ps1",
                   CONTROL / "inspect-batch-095-native-694.py",
                   LOGS / "preflight-694.json", LOGS / "runtime-694.json",
                   CONTROL / "runner-lock-role-notes.txt", CONTROL / "authoring-artifact-path-notes.txt"]:
        shutil.copyfile(source, recipes / source.name)
    visual = {
        "snapshot": frozen["contentSnapshot"],
        "reviewedTeachingSnapshot": frozen["reviewedTeachingSnapshot"],
        "reviewer": "Coordinator, GPT-6.1 Sol (gpt-6.1-sol)",
        "scope": "Native visual inspection only; inherited textual source/review evidence not rebranded as fresh linguistic review.",
        "inspectedOriginalPngCount": 60,
        "fontPanelsInspectedAtOriginalResolution": [f"n1-095-font-panel-{i}.png" for i in range(1, 5)],
        "routeCapturesInspectedViaContactSheets": 56,
        "contactSheetsInspected": [f"contact-sheets/sheet-{i:02d}.png" for i in range(1, 15)],
        "additionalOriginalResolutionReads": ["n1-095-meaning-question.png", "n1-095-selection.png"],
        "verdict": "No actionable visual defect established in these captures; original-session rendered confirmations and bounded semantic adjudication remain required.",
        "glyphs": "All32 scoped Han readable across Gothic/Mincho/Textbook/Brush; 剖/部/倍/副 and 刀/刂/亻/阝/解 distinguishable. Cmap-absent 亻/刂/阝 visibly render without tofu or blanks. Exact fallback font face not identified. Textbook 解剖学 wraps before 学 on panel4; all characters remain visible.",
        "articles": "Three complete projections covered by visible selectors/captures. Japanese, translations, component boundaries and source references readable. Reading tables explicitly instruct sideways scrolling; left/right captures expose the rows. Left-column clipping in right-scrolled captures is expected; viewport clipping of other paragraphs is covered by subsequent captures.",
        "quiz": "Actual N1 UI shows 剖/dissect; split open, 冒/brave danger; venture, 刈/mow; reap, 企/plan; undertake. All three default fallback meanings are distinct from dissect/split open; mowing/reaping is not dissection. All64 builder records preserved; related blade/shaving meanings among sampled alternatives do not by themselves establish synonyms for dissect/split open. Final bounded original-session semantic confirmation pending.",
        "reading": "Visible question and feedback show only onボウ; Done records1/1 correct. No kun questions; full frozen and explicit quiz lists retainボウ/[] in full/Lite projections.",
        "drawing": "Ten-stroke injected reference trace and feedback visible; recall give-up displays reference and persists grade on Next. Offline model-unavailable message visible. Not human handwriting or MLKit acceptance.",
        "newConsequentialUnresolvedVisualClaims": [],
        "pendingHypotheses": [],
        "limits": [
            "API35 emulator at tested default font scale only; physical phone/general release outstanding.",
            "hasGlyph/nonblank/raster hashes alone are not legibility or exact fallback-face evidence; actual four panels inspected.",
            "No new blind reviewers or independent rendered confirmations in this checkpoint.",
            "64kanji/384word builder records are bounded seed/pool samples, not exhaustive random-pool safety.",
            "Direct-guard success proves the three specified pairs are absent, not semantic safety of every other option.",
        ],
    }
    save(DEST / "coordinator-visual-inspection.json", visual)
    artifact_index = [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p)}
                      for p in sorted(DEST.rglob("*")) if p.is_file()]
    save(DEST / "artifact-index.json", artifact_index)
    evidence = {
        "schemaVersion": 1, "execution": 694, "batch": "095", "status": STAGE,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "startingState": load(CONTROL / "progress.json")["execution694StartingState"],
        "contentSnapshot": frozen["contentSnapshot"], "reviewedTeachingSnapshot": frozen["reviewedTeachingSnapshot"],
        "androidHead": APP, "productionBaseline": frozen["productionBaseline"],
        "qualifiedTestOnlyAndroid": True, "latestAppMainClaimed": False,
        "fixtureSha256": frozen["fixtureSha256"], "archiveSha256": frozen["archiveSha256"],
        "appApk": compiled["appApk"], "testApk": compiled["testApk"],
        "contentVersion": route["contentVersion"], "runtimeHashesVerifiedAgain": 8441,
        "archiveGuardsUnchanged": True, "archiveBudgetEvidence": "docs/n1-sources/execution-693.json",
        "nativeExecution": receipt, "nativeTestsPassed": 2, "nativeTestsSkipped": 0,
        "terminalPerCaseStatus": [0, 0], "fullArchiveImportedOnce": True,
        "importedKanji": 1118, "importedWords": 5071, "n1Cards": 127,
        "problems": 0, "acceptedReadingParserEpoch": 1,
        "routeEvidence": "docs/n1-reviews/batch-095-native/execution-694/n1-095-article-route.json",
        "fontEvidence": "docs/n1-reviews/batch-095-native/execution-694/n1-095-font-raster.json",
        "visualInspection": "docs/n1-reviews/batch-095-native/execution-694/coordinator-visual-inspection.json",
        "artifactIndex": "docs/n1-reviews/batch-095-native/execution-694/artifact-index.json",
        "kanjiBuilderChecks": 64, "newDirectWordGuardBuilderChecks": 384, "newDirectWordGuardPairs": 3,
        "allMappedReciprocalPairs": 2, "directedLinkTransitions": 4,
        "activatedBaselinePairs": 0, "completeArticleProjections": 3,
        "individualGlyphProbes": 128, "wholeWordRasterProbes": 8, "fontPanels": 4,
        "originalPngCaptures": 60, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED",
        "nativeExecutionAndCoordinatorVisualInspection": "passed",
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "runtimeChanged": False, "independentReviewersLaunched": 0,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 121, "remainingAdditions": 1107,
        "lastPublishedCommit": "d6a261903f269d6223afc067815b02c595da41a3",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": visual["limits"], "pendingHypotheses": [], "nextAction": NEXT,
        "diagnostics": [
            "Initial console summary needed explicit UTF8 after cp1252 could not print Japanese. Entire request had already been read/decoded; no permission denial or artifact loss.",
            "One evidence read requested beyond EOF; corrected to actual627-line range. No required evidence missing.",
            "Historical textual reconciliation remains immutable at execution691; active native disposition is this additive record and current batch packet, not fresh blind-review credit.",
            "Staged whitespace check rejected untouched raw adb/emulator logs before signing began. Archived those two logs as verified lossless gzip, preserving original bytes in control; no test result or raw content normalized.",
        ],
    }
    save(EVIDENCE, evidence)
    path = ROOT / "docs" / "n1-sources" / "batch-095-progress.json"
    packet = load(path)
    assert not packet["runtimeAccepted"] and not packet["runtimePublished"]
    packet.update(status=STAGE, nextAction=NEXT)
    packet["pendingGates"][0] = (
        "Native execution694 passed; serial bounded original-session rendered confirmations and "
        "evidence-based semantic adjudication of actual N1/All/custom/random choices remain."
    )
    packet["androidAcceptance"]["nativeAcceptance"] = "execution694-passed-awaiting-original-session-rendered-confirmations"
    assert "nativeExecution694" not in packet
    packet["nativeExecution694"] = {
        "evidence": "docs/n1-sources/execution-694.json", "status": STAGE,
        "terminalPerCaseStatus": [0, 0], "testsSkipped": 0, "coordinatorInspectedPngCount": 60,
        "fullArchiveImportedOnce": True, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED", "runtimeAccepted": False, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier native-pending fields/limits are historical; this record supersedes execution/native visual state only, not independent review or publication.",
    }
    save(path, packet)
    packet_fields()
    subprocess.run(["git", "-C", str(ROOT), "diff", "--check"], check=True)
    print("Native evidence and exact original PNGs archived; no runtime content changed.")


def checkpoint():
    progress = load(CONTROL / "progress.json")
    original = load(LOGS / "progress-before-694.json")
    assert progress["checkpoint"] == 693 and progress["stage"] == "batch-095-native-execution-in-progress"
    head = git(ROOT, "rev-parse", "HEAD")
    assert git(ROOT, "rev-parse", "HEAD^") == HEAD and git(ROOT, "log", "-1", "--format=%G?") == "G"
    for root in [ROOT, ANDROID]:
        assert not git(root, "status", "--porcelain", "--untracked-files=all")
    assert git(ANDROID, "rev-parse", "HEAD") == APP
    assert not git(ROOT, "diff", HEAD, "HEAD", "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    assert all(p.startswith(("docs/n1-reviews/batch-095-native/execution-694/",
                             "docs/n1-sources/execution-694.json", "docs/n1-sources/batch-095-progress.json"))
               for p in git(ROOT, "diff", "--name-only", HEAD, "HEAD").splitlines())
    posted = load(CONTROL / "batch-095-native-694-issue-receipt.json")
    assert posted["user"]["login"] == "stop-cran"
    assert posted["body"] == (CONTROL / "batch-095-native-694-issue-body.txt").read_bytes().decode("utf-8-sig")
    for item in load(DEST / "artifact-index.json"):
        assert sha(ROOT.joinpath(*item["path"].split("/"))) == item["sha256"]
    runtime()
    fields = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[key] == value for key, value in original.items() if key not in fields)
    record = {
        "schemaVersion": 1, "execution": 694, "checkpoint": 694, "batch": "095",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "evidence": "docs/n1-sources/execution-694.json", "nativeTestsPassed": 2,
        "terminalPerCaseStatus": [0, 0], "testsSkipped": 0, "coordinatorInspectedPngCount": 60,
        "fullArchiveImportedOnce": True, "runtimeHashesVerifiedAgain": 8441,
        "kanjiBuilderChecks": 64, "directWordGuardBuilderChecks": 384,
        "independentRenderedConfirmations": "pending", "livePoolSemanticAcceptance": "UNVERIFIED",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "ownedEmulatorStopped": True, "serial": "emulator-5580", "parentEmulatorPid": 5536, "qemuPid": 14252,
        "publishedAdditions": 121, "remainingAdditions": 1107, "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": posted["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    progress.update(checkpoint=694, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    progress["execution694CoordinatorCheckpoint"] = record
    progress["batch095NativeExecutionCheckpoint"] = copy.deepcopy(record)
    persist(progress)
    saved = load(CONTROL / "progress.json")
    assert all(saved[key] == value for key, value in original.items() if key not in fields)
    save(LOGS / "checkpoint-694-verification.json", record)
    print(json.dumps({"checkpoint": 694, "savedCommit": head, "historyPreserved": True,
                      "issueUpdate": posted["html_url"]}, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "checkpoint": checkpoint, "packet-fields": packet_fields}[sys.argv[1]]()
