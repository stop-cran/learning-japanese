import copy
import datetime
import gzip
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import zipfile

CONTROL = pathlib.Path(__file__).parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
SESSION = "7fa5bfa8-7e4f-4d49-9084-40fb301b94f5"
LOGS = CONTROL / "logs" / SESSION
NATIVE = CONTROL / "artifacts" / "batch-094-native-attempt-682"
DEST = ROOT / "docs" / "n1-reviews" / "batch-094-native" / "execution-682"
EVIDENCE = ROOT / "docs" / "n1-sources" / "execution-682.json"
STAGE = "native-executed-awaiting-rendered-confirmations"
NEXT = (
    "SAME094 serial bounded rendered confirmations in ORIGINAL reviewer sessions next: "
    "Claudeedf22897-9f87-4a3b-b20f-4c2fd839013a and GPT65fd64ff-aae2-40af-927e-bf19b52fecb6. "
    "Read docs/n1-sources/execution-682.json and docs/n1-reviews/batch-094-native/execution-682/. "
    "BOTH native cases terminal0/no skips on exact frozen fullarchive18ad4bed/versioneeae47753a460f72/"
    "8438hashes through productionContentSync ONCE;1117kanji/5070words/126N1/zeroProblems/Roomepoch1. "
    "All85PNG inspected by coordinator:5fourfontpanels/all41Han and80route captures through20contact sheets; "
    "no established visual defect, including actual visible U+5202/U+65AB/U+6C35/U+961D fallback. "
    "This is NOT independent rendered confirmation or whole-pool semantic certification. "
    "DefaultN1 actual options削/shave;sharpen;pare,刑/criminalpunishment,弐/twoformalnumeral,乏/scarce;lacking. "
    "N1 has only刑 curated;前N5/判N3 excluded, two productionfallbacks. Inspect exact64 builder pools/"
    "16seeds/N1+All+boundedcustom+randomN1subset and384three-directguard checks/bothdirections/"
    "bothtargetorientations/All+custom. All64+384records retained; do not turn guard absence into full "
    "semantic safety. In particular evaluate observed削る vs縮める 'shorten;reduce;shrink' as a "
    "pending hypothesis, not a confirmed defect or waived limitation. Onlyさく/けずる offered and "
    "persistedGood/Done; fullrawreadings retained;9injectedstrokes/trace+giveuprecall/persistence; "
    "4complete articles/3allmapped reciprocalpairs/6directions/2activatedbaselinepairs/SystemBack/offline. "
    "Original-session followups are dependent confirmations, NOT newblind credit. Exact API35emulator5580/"
    "parent12944/qemu7668 stopped; no owner/shared devices touched, heaps/guards unchanged, no phone/"
    "humanhandwriting/MLKit acceptance. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOT latestappmain. Fresh680 JVM3RealContent+1RareHan remain inherited without skips. "
    "Keep all original source/baseline/link/reading/twofamily/native/currentmainnormalmerge/"
    "changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIPruntimehash/18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue gates. Parent19008 retainsrunner.lock: verify live "
    "ancestry/session/signedheads/cleanstate, NOchildacquire/delete/unlock. Approvedcontrol/committed "
    "packets only, NO optionalhistoricalsessionrecipes. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. Published120/1228,1108remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No095/runtimepublication/secondrunner."
)


def load(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, encoding="utf-8").strip()


def change_root(path, changes, additions):
    raw = path.read_bytes().decode("utf-8")
    before = json.loads(raw)
    newline = "\r\n" if "\r\n" in raw else "\n"
    decoder = json.JSONDecoder()
    for key, value in changes.items():
        match = re.search(r'^  "' + re.escape(key) + r'": ', raw, re.MULTILINE)
        assert match, key
        _, end = decoder.raw_decode(raw, match.end())
        raw = raw[:match.end()] + json.dumps(value, ensure_ascii=False, indent=2).replace("\n", newline) + raw[end:]
    assert not set(additions) & set(before)
    if additions:
        end = raw.rfind("}")
        extra = json.dumps(additions, ensure_ascii=False, indent=2)[1:-1].strip("\n")
        raw = raw[:end].rstrip() + "," + newline + extra.replace("\n", newline) + newline + raw[end:]
    after = json.loads(raw)
    assert all(after[k] == v for k, v in before.items() if k not in changes)
    path.write_bytes(raw.encode("utf-8"))
    assert load(path) == after


def prepare():
    assert git(ROOT, "rev-parse", "HEAD") == "bf3e09d6e55f64125edd3b08dd4e37df0ffdb5d4"
    assert git(ANDROID, "rev-parse", "HEAD") == "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
    for root in [ROOT, ANDROID]:
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain", "--untracked-files=all")
    assert not DEST.exists() and not EVIDENCE.exists()
    compiled = load(ROOT / "docs" / "n1-sources" / "execution-681.json")
    frozen = compiled["fixtureVerification"]
    receipt = load(CONTROL / "batch-094-native-attempt-682-execution.json")
    route = load(NATIVE / "n1-094-article-route.json")
    raster = load(NATIVE / "n1-094-font-raster.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert not receipt["parentLockTouched"] and not receipt["guardsChanged"] and not receipt["guestOrAppHeapChanged"]
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"],
            route["acceptedReadingParserEpoch"]) == (1117, 5070, 126, 0, 1)
    assert len(route["directGuardBuilderChecks"]) == 384
    assert len(route["productionBuilderN1AndAllExactChoices"]) == 64
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"],
            route["completeArticleProjections"], route["activatedBaselinePairs"]) == (3, 6, 4, 2)
    assert route["onlySakuAndKezuruBothKindsPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 9 and route["drawingGradeRecordedOnNext"]
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (164, 12, 5)
    log = (NATIVE / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0\s*$", log, re.MULTILINE)) == 2
    assert "OK (2 tests)" in log
    for path, digest in [(frozen["archive"], frozen["archiveSha256"]),
                         (frozen["fixture"], frozen["fixtureSha256"]),
                         (compiled["testApk"]["path"], compiled["testApk"]["sha256"]),
                         (compiled["appApk"]["path"], compiled["appApk"]["sha256"])]:
        assert sha(pathlib.Path(path)) == digest
    sys.path.insert(0, str(ROOT / "tools"))
    from build_manifest import build_manifest
    manifest = load(ROOT / "manifest.json")
    assert build_manifest(ROOT) == manifest
    verified = 0
    with zipfile.ZipFile(frozen["archive"]) as archive:
        name = next(n for n in archive.namelist() if n.endswith("/manifest.json"))
        prefix = name[:-len("manifest.json")]
        assert archive.read(name) == (ROOT / "manifest.json").read_bytes()
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, digest in entries.items():
                data = archive.read(prefix + name)
                assert data == (ROOT / pathlib.PurePosixPath(name)).read_bytes(), name
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                verified += 1
    assert verified == 8438
    DEST.mkdir()
    artifacts = []
    for source in sorted(NATIVE.iterdir()):
        assert source.is_file()
        destination = DEST / source.name
        shutil.copyfile(source, destination)
        assert sha(source) == sha(destination)
        artifacts.append({"path": destination.relative_to(ROOT).as_posix(), "sha256": sha(destination)})
    inspection = CONTROL / "batch-094-native-inspection-682"
    sheets = DEST / "contact-sheets"
    sheets.mkdir()
    for source in sorted(inspection.iterdir()):
        shutil.copyfile(source, sheets / source.name)
    assert len(list(DEST.glob("*.png"))) == 85
    assert len(list(sheets.glob("*.png"))) == 20
    recipes = DEST / "receipts"
    recipes.mkdir()
    for source in [
        pathlib.Path(__file__), CONTROL / "start-execution-682.py",
        CONTROL / "run-682-native.ps1", CONTROL / "inspect-batch-094-native-682.py",
        CONTROL / "batch-094-native-attempt-682-execution.json",
    ]:
        shutil.copyfile(source, recipes / source.name)
    visual = {
        "snapshot": frozen["contentSnapshot"],
        "reviewedTeachingSnapshot": frozen["reviewedTeachingSnapshot"],
        "reviewer": "Coordinator, GPT-6.1 Sol (gpt-6.1-sol)",
        "scope": "Native visual inspection only; inherited textual source/review evidence not rebranded as fresh linguistic review.",
        "inspectedOriginalPngCount": 85,
        "fontPanelsInspectedAtOriginalResolution": [f"n1-094-font-panel-{i}.png" for i in range(1, 6)],
        "routeCapturesInspectedViaContactSheets": 80,
        "contactSheetsInspected": [f"contact-sheets/sheet-{i:02d}.png" for i in range(1, 21)],
        "additionalOriginalResolutionReads": [
            "n1-094-selection.png", "n1-094-meaning-question.png",
            "n1-094-curated-さく-question.png", "n1-094-curated-けずる-question.png",
            "n1-094-kanji-17.png", "n1-094-jo-26.png", "n1-094-drawing-feedback.png",
        ],
        "verdict": "No actionable visual defect established in these captures; dependent original-session rendered confirmations remain required.",
        "glyphs": "All41 scoped Han readable in Gothic/Mincho/Textbook/Brush panels; 削/消/肖, 刀/刂, 斫, 氵, 阜/阝 and 前/判/刑 distinguishable. Cmap-absent 刂/斫/氵/阝 visibly render without tofu or blank replacement. Matching fallback shapes across families acceptable; exact fallback font face not identified.",
        "articles": "Four complete projections covered by visible selectors and captures. Wrapped Japanese/English and source links readable. Reading tables intentionally scroll horizontally with an explicit instruction; left/right captures together expose complete rows. Left-column clipping in right-scrolled captures is expected, not missing metadata.",
        "quiz": "Actual N1 UI shows exactly 削/shave;sharpen;pare, 刑/criminal punishment, 弐/two(formal numeral), 乏/scarce;lacking. Only刑 is available curated; two fallback choices are visibly wrong for削. All64 builder records preserved; whole-pool semantics still subject to original-session confirmation.",
        "reading": "Visible question/feedback captures show only けずる and サク; two correct answers and Done. Recognition readings はつる/そぐ remain in feedback/body, not extra question keys.",
        "drawing": "Nine-stroke trace and feedback visible, with injected reference path; recall give-up displays reference and persists grade on Next. Offline model unavailable message visible. This does not certify human handwriting or MLKit.",
        "newConsequentialUnresolvedVisualClaims": [],
        "pendingHypotheses": [
            "384 direct-guard assertions prove the three specified pairs are absent, NOT semantic correctness of every other option. Observed All/JpToEn 削る vs 縮める 'shorten; reduce; shrink' deserves bounded evidence-based original-session adjudication; no new defect or automatic all-pairs expansion asserted."
        ],
        "limits": [
            "API35 emulator at default tested font scale only; physical phone/general release outstanding.",
            "Raster hashes/hasGlyph/nonblank checks alone do not prove legibility or exact fallback face; actual five panels inspected.",
            "No new blind reviewers launched and no independent rendered confirmation yet.",
            "64 kanji and384 word builder records are bounded seed/pool samples, not exhaustive random-pool safety.",
        ],
    }
    save(DEST / "coordinator-visual-inspection.json", visual)
    save(DEST / "artifact-index.json", artifacts)
    evidence = {
        "schemaVersion": 1, "execution": 682, "batch": "094", "status": STAGE,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "startingState": load(CONTROL / "progress.json")["execution682StartingState"],
        "contentSnapshot": frozen["contentSnapshot"], "reviewedTeachingSnapshot": frozen["reviewedTeachingSnapshot"],
        "androidHead": frozen["androidSnapshot"], "productionBaseline": frozen["productionBaseline"],
        "qualifiedTestOnlyAndroid": True, "latestAppMainClaimed": False,
        "fixtureSha256": frozen["fixtureSha256"], "archiveSha256": frozen["archiveSha256"],
        "appApk": compiled["appApk"], "testApk": compiled["testApk"],
        "contentVersion": route["contentVersion"], "runtimeHashesVerifiedAgain": 8438,
        "archiveGuardsUnchanged": True, "archiveBudgetEvidence": "docs/n1-sources/execution-681.json",
        "nativeExecution": receipt,
        "nativeTestsPassed": 2, "nativeTestsSkipped": 0, "terminalPerCaseStatus": [0, 0],
        "fullArchiveImportedOnce": True, "importedKanji": 1117, "importedWords": 5070,
        "n1Cards": 126, "problems": 0, "acceptedReadingParserEpoch": 1,
        "routeEvidence": "docs/n1-reviews/batch-094-native/execution-682/n1-094-article-route.json",
        "fontEvidence": "docs/n1-reviews/batch-094-native/execution-682/n1-094-font-raster.json",
        "visualInspection": "docs/n1-reviews/batch-094-native/execution-682/coordinator-visual-inspection.json",
        "artifactIndex": "docs/n1-reviews/batch-094-native/execution-682/artifact-index.json",
        "kanjiBuilderChecks": 64, "newDirectWordGuardBuilderChecks": 384,
        "newDirectWordGuardPairs": 3, "allMappedReciprocalPairs": 3, "directedLinkTransitions": 6,
        "activatedBaselinePairs": 2, "completeArticleProjections": 4,
        "individualGlyphProbes": 164, "wholeWordRasterProbes": 12,
        "fontPanels": 5, "originalPngCaptures": 85,
        "independentRenderedConfirmations": "pending", "livePoolSemanticAcceptance": "UNVERIFIED",
        "nativeExecutionAndCoordinatorVisualInspection": "passed",
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "runtimeChanged": False, "independentReviewersLaunched": 0,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": "48765e20846e1d6769c6ddc35146f6ce58deab57",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": visual["limits"], "pendingHypotheses": visual["pendingHypotheses"], "nextAction": NEXT,
        "diagnostics": [
            "Two read-only inspection probes corrected locally: Python console cp1252 could not print Japanese, then a summary probe attempted a slice on manifest files dict. No source/artifact write or permission denial resulted.",
            "Initial guessed batch-094.json path did not exist; used actual batch-094-progress/source-evidence records. Not missing mandatory evidence or permission denial.",
            "First archival precondition compared raw text hashes rather than the repository's defined CRLF-normalized hashes and stopped before writes. Confirmed exact ZIP/local bytes equal, reused build_manifest for current freshness and applied existing per-section binary/text hash contract to all8438 entries; no source/archive/manifest bytes changed."
        ],
    }
    save(EVIDENCE, evidence)
    for relative in ["docs/n1-sources/batch-094-progress.json", "docs/n1-reviews/batch-094-reconciliation.json"]:
        path = ROOT / relative
        before = load(path)
        changes = {"status": STAGE, "nextAction": NEXT}
        if "pendingGates" in before:
            changes["pendingGates"] = [
                "Serial bounded original-session rendered confirmations and evidence-based semantic adjudication of actual N1/All/custom/random choices; native execution682 passed, not final runtime acceptance.",
                *before["pendingGates"][1:],
            ]
        if "androidAcceptance" in before:
            android = copy.deepcopy(before["androidAcceptance"])
            android["nativeAcceptance"] = "execution682-passed-awaiting-original-session-rendered-confirmations"
            changes["androidAcceptance"] = android
        change_root(path, changes, {"nativeExecution682": {
            "evidence": "docs/n1-sources/execution-682.json", "status": STAGE,
            "terminalPerCaseStatus": [0, 0], "testsSkipped": 0,
            "coordinatorInspectedPngCount": 85, "fullArchiveImportedOnce": True,
            "independentRenderedConfirmations": "pending", "livePoolSemanticAcceptance": "UNVERIFIED",
            "runtimeAccepted": False, "runtimePublished": False,
        }})
        assert not load(path)["runtimeAccepted"] and not load(path)["runtimePublished"]
    subprocess.run(["git", "-C", str(ROOT), "diff", "--check"], check=True)
    print("Native evidence and exact original PNGs archived; no runtime content changed.")


def checkpoint():
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    before = load(LOGS / "progress-before-682.json")
    assert progress["checkpoint"] == 681 and progress["stage"] == "batch-094-native-execution-in-progress"
    head = git(ROOT, "rev-parse", "HEAD")
    assert head != "bf3e09d6e55f64125edd3b08dd4e37df0ffdb5d4"
    assert git(ROOT, "log", "-1", "--format=%G?") == "G"
    for root in [ROOT, ANDROID]:
        assert not git(root, "status", "--porcelain", "--untracked-files=all")
    posted = load(CONTROL / "batch-094-native-682-issue-receipt.json")
    body = (CONTROL / "batch-094-native-682-issue-body.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    runtime = git(ROOT, "diff", "bf3e09d6e55f64125edd3b08dd4e37df0ffdb5d4", "HEAD", "--",
                  "kanji", "words", "strokes", "articles", "manifest.json")
    assert not runtime
    fields = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[key] == value for key, value in before.items() if key not in fields)
    record = {
        "schemaVersion": 1, "execution": 682, "checkpoint": 682, "batch": "094",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "evidence": "docs/n1-sources/execution-682.json", "nativeTestsPassed": 2,
        "terminalPerCaseStatus": [0, 0], "testsSkipped": 0, "coordinatorInspectedPngCount": 85,
        "fullArchiveImportedOnce": True, "runtimeHashesVerifiedAgain": 8438,
        "kanjiBuilderChecks": 64, "directWordGuardBuilderChecks": 384,
        "independentRenderedConfirmations": "pending", "livePoolSemanticAcceptance": "UNVERIFIED",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "ownedEmulatorStopped": True, "serial": "emulator-5580", "parentEmulatorPid": 12944, "qemuPid": 7668,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": "48765e20846e1d6769c6ddc35146f6ce58deab57",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": posted["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    progress.update(checkpoint=682, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    progress["execution682CoordinatorCheckpoint"] = record
    progress["batch094NativeExecutionCheckpoint"] = copy.deepcopy(record)
    save(progress_path, progress)
    saved = load(progress_path)
    assert all(saved[key] == value for key, value in before.items() if key not in fields)
    save(LOGS / "checkpoint-682-verification.json", record)
    print(json.dumps({"checkpoint": 682, "savedCommit": head, "historyPreserved": True,
                      "issueUpdate": posted["html_url"]}, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "checkpoint": checkpoint}[sys.argv[1]]()
