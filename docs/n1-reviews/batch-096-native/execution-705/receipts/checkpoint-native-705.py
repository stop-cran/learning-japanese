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
import zipfile

C = pathlib.Path(__file__).parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
SESSION = "4061f75b-8dc5-4ba3-affb-1d74572f9afa"
L = C / "logs" / SESSION
HEAD = "81845e0477a157e90551abf39e7bb132e6d2919e"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
N = C / "artifacts" / "batch-096-native-attempt-705"
I = C / "batch-096-native-inspection-705"
D = R / "docs" / "n1-reviews" / "batch-096-native" / "execution-705"
E = R / "docs" / "n1-sources" / "execution-705.json"
STAGE = "native-executed-awaiting-rendered-confirmations"
NEXT = (
    "SAME096 serial bounded rendered confirmations in ORIGINAL reviewer sessions next: "
    "Claude de7596b6-1f69-43e0-b297-c3e600fa712a THEN GPT ca536738-97f2-4841-b985-321ce12b37c1. "
    "Read docs/n1-sources/execution-705.json and docs/n1-reviews/batch-096-native/execution-705/. "
    "BOTH native cases terminal0/no skips; full archive58129f19/version54645b95fe8e939c/"
    "8444hashes through productionContentSync ONCE:1119kanji/5072words/128N1/zeroProblems/Roomepoch1. "
    "Coordinator inspected all41PNG: FOURfourfontpanels/all28Han and37routecaptures via10contactsheets; "
    "no actionable visual defect established, visible U+5182/U+5202 fallback; exact fallback face unidentified. "
    "Actual default N1 options: strength vs dissect/split open, shave/sharpen/pare and Confucian/scholar. "
    "TWO curated wrongcards available; ONE productionfallback captured. Inspect exact64 imported builder "
    "records/16seeds/N1+All+boundedcustom+randomN1subset and1536 TWELVE directwordguard checks "
    "from剛健/All+custom/bothdirections/bothtargetorientations. Samples are NOT whole-pool semantic certification. "
    "Onlyonごう/noKun offered/persistedGood/Done; full/Lite rawゴウ/[] and explicitゴウ/[] retained. "
    "TEN injectedstrokes/trace+giveuprecall/persistence; TWO complete articleprojections剛/剛健, "
    "ONE allmapped reciprocalpair/TWOdirections/zeroactivatedbaselinepairs/SystemBack/offline/N1selection. "
    "Original-session followups are dependent confirmations, NOT newblindcredit. OwnedAPI35 emulator5580/"
    "parent12020/qemu21048 stopped; no owner/shared devices/heaps/guards changed, no phone/"
    "humanhandwriting/MLKit acceptance. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOT latestappmain; fresh703 JVM4/no skips retained. All original source/baseline/link/reading/"
    "twofamily/native/currentmainnonrewritingmerge/changedteachingreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPentryhash/unchanged18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue gates remain. "
    "Parent19008 retainsrunner.lock: verifyliveancestry/session/signedheads/whollyclean, NOchildacquire/"
    "delete/unlock/readprobe. Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Published122/1228,1106remaining "
    "unchanged; physicalphone/generalrelease/whole-set outstanding. No097/runtimepublication/secondrunner."
)


def load(p):
    return json.loads(p.read_bytes())


def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(root), *args],
        encoding="utf-8").strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain", "--untracked-files=all")


def runtime():
    p = C / "prepare-batch-096-native-704.py"
    assert sha(p) == "852e7fbff2679218855c894fec338d22cedf28a6a9e28ba4a8ebc64cd4dea820"
    spec = importlib.util.spec_from_file_location("prepared096", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.runtime()


def persist(p):
    temp = C / "progress.705.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")


def prepare():
    clean()
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    _, checkpoint = text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)
    embedded = json.loads(checkpoint)
    assert embedded["checkpoint"] == 704 and embedded["batch"] == "096"
    p = load(C / "progress.json")
    assert p["checkpoint"] == 704 and p["status"] == "continue"
    save(L / "progress-before-705.json", p)
    preflight = (C / "preflight-704.ps1").read_text(encoding="utf-8-sig")
    preflight = preflight.replace("110fd75c-c109-4887-a762-9abe26b9f6f7", SESSION).replace("704", "705")
    (C / "preflight-705.ps1").write_text(preflight, encoding="utf-8")
    subprocess.run(["pwsh", "-NoProfile", "-File", str(C / "preflight-705.ps1")], check=True)
    start = {
        "execution": 705, "batch": "096", "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "startedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "SAME096 frozen compiled native execution and coordinator visual inspection; signed LOCAL evidence only. No rendered reviewer/publication/097.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, entire approved issue and final704 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": load(L / "preflight-705.json"),
        "artifactPathPreflight": "Approved control helpers, committed packets and approved frozen inputs only; no optional historical-session recipes accessed.",
        "runtime": runtime(), "actualNewPermissionDenials": [],
    }
    p["execution705StartingState"] = start
    p["stage"] = "batch-096-native-execution-in-progress"
    p["nextAction"] = "SAME096 execute frozen compiled fixture, inspect native outputs, preserve signed LOCAL evidence and checkpoint. All prior acceptance/publication gates remain."
    persist(p)
    wrapper = (C / "run-694-native.ps1").read_text(encoding="utf-8-sig")
    replacements = {
        "6538b1ef-d7d4-465b-bd47-d66aa8a6ea9f": SESSION,
        "694": "705", "693": "704", "095": "096",
        "95be0577bea120a757bccd190625499b01e94a63": HEAD,
    }
    for old, new in replacements.items():
        assert old in wrapper
        wrapper = wrapper.replace(old, new)
    (C / "run-705-native.ps1").write_text(wrapper, encoding="utf-8")
    print("Starting state persisted; exact runtime manifest and source hashes verified.")


def collect():
    clean()
    assert not D.exists() and not E.exists()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 704 and p["stage"] == "batch-096-native-execution-in-progress"
    receipt = load(C / "batch-096-native-attempt-705-execution.json")
    route = load(N / "n1-096-article-route.json")
    raster = load(N / "n1-096-font-raster.json")
    frozen = load(R / "docs" / "n1-sources" / "execution-704.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert not any(receipt[k] for k in ["parentLockTouched", "guestOrAppHeapChanged", "guardsChanged"])
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"],
            route["acceptedReadingParserEpoch"]) == (1119, 5072, 128, 0, 1)
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"],
            route["completeArticleProjections"], route["activatedBaselinePairs"]) == (1, 2, 2, 0)
    assert route["onlyOnGouNoKunPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 10 and route["drawingGradeRecordedOnNext"]
    assert route["actualN1CuratedAvailable"] == 2 and route["actualN1FallbackOptions"] == 1
    assert len(route["directGuardBuilderChecks"]) == 1536
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
            assert sum(o["kanji"] == "剛" for o in row["options"]) == 1
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (112, 8, 4)
    assert len(raster["rows"]) == 120
    log = (N / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0\s*$", log, re.MULTILINE)) == 2
    assert "OK (2 tests)" in log
    assert not re.search(r"STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED|assumptionFailure|ignored", log)
    verification = frozen["fixtureVerification"]
    for path, digest in [(verification["archive"], verification["archiveSha256"]),
                         (verification["fixture"], verification["fixtureSha256"]),
                         (frozen["appApk"]["path"], frozen["appApk"]["sha256"]),
                         (frozen["testApk"]["path"], frozen["testApk"]["sha256"])]:
        assert sha(pathlib.Path(path)) == digest
    manifest = runtime()
    with zipfile.ZipFile(verification["archive"]) as z:
        names = z.namelist()
        entry = next(n for n in names if n.endswith("/manifest.json"))
        prefix = entry[:-len("manifest.json")]
        assert json.loads(z.read(entry)) == manifest
        count = 0
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, digest in entries.items():
                data = z.read(prefix + name)
                local = R.joinpath(*name.split("/")).read_bytes()
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                if not binary:
                    data, local = data.replace(b"\r\n", b"\n"), local.replace(b"\r\n", b"\n")
                assert data == local and hashlib.sha256(data).hexdigest() == digest, name
                count += 1
        assert count == 8444
    D.mkdir()
    for source in sorted(N.iterdir()):
        assert source.is_file()
        if source.suffix == ".txt":
            data = source.read_bytes()
            archived = D / (source.name + ".gz")
            archived.write_bytes(gzip.compress(data, mtime=0))
            assert gzip.decompress(archived.read_bytes()) == data
        else:
            shutil.copyfile(source, D / source.name)
            assert sha(source) == sha(D / source.name)
    shutil.copytree(I, D / "contact-sheets")
    assert len(list(D.glob("*.png"))) == 41 and len(list((D / "contact-sheets").glob("*.png"))) == 10
    recipes = D / "receipts"
    recipes.mkdir()
    for source in [pathlib.Path(__file__), C / "preflight-705.ps1", C / "run-705-native.ps1",
                   C / "inspect-batch-096-native-705.py", L / "preflight-705.json",
                   C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt"]:
        shutil.copyfile(source, recipes / source.name)
    visual = {
        "snapshot": verification["contentSnapshot"],
        "reviewedTeachingSnapshot": verification["reviewedTeachingSnapshot"],
        "reviewer": "Coordinator, GPT-6.1 Sol (gpt-6.1-sol)",
        "scope": "Native visual inspection only; inherited textual source/review evidence not rebranded as fresh linguistic review.",
        "inspectedOriginalPngCount": 41,
        "fontPanelsInspectedAtOriginalResolution": [f"n1-096-font-panel-{i}.png" for i in range(1, 5)],
        "routeCapturesInspectedViaContactSheets": 37,
        "contactSheetsInspected": [f"contact-sheets/sheet-{i:02d}.png" for i in range(1, 11)],
        "additionalOriginalResolutionReads": ["n1-096-meaning-question.png", "n1-096-selection.png"],
        "verdict": "No actionable visual defect established in these captures; original-session rendered confirmations and bounded semantic adjudication remain required.",
        "glyphs": "All28 scoped Han readable across Gothic/Mincho/Textbook/Brush; 剛/削/剖/則/岡/冂/山/刀/刂 distinguishable. Cmap-absent 冂/刂 visibly render without tofu or blanks. Exact fallback font face not identified. All focused compounds remain visible in panel4.",
        "articles": "Two complete projections covered by visible selectors/captures. Japanese, translations, component boundaries and source references readable. Reading table explicitly instructs sideways scrolling; left/right captures expose the entire row. Left-column clipping in right-scrolled captures is expected; viewport clipping of other paragraphs is covered by subsequent captures.",
        "quiz": "Actual N1 UI shows 剛/sturdy; unyielding strength, 剖/dissect; split open, 削/shave; sharpen; pare, 儒/Confucian; Confucian scholar. One actual fallback is 儒, not 則N2. These displayed alternatives are semantically distinct. All64 builder records preserved; their 27 unique sampled labels include 克/overcome, related to strength but not a synonym for sturdy/unyielding strength. Final bounded original-session confirmation pending, not unrestricted pool certification.",
        "reading": "Visible question and feedback show only onゴウ; Done records1/1 correct. No kun questions; full frozen and explicit quiz lists retainゴウ/[] in full/Lite projections.",
        "drawing": "Ten-stroke injected reference trace and feedback visible; recall give-up displays reference and persists grade on Next. Offline model-unavailable feedback visible. Not human handwriting or MLKit acceptance.",
        "newConsequentialUnresolvedVisualClaims": [],
        "limits": [
            "API35 emulator at tested default font scale only; physical phone/general release outstanding.",
            "hasGlyph/nonblank/raster hashes alone are not legibility or exact fallback-face evidence; actual four panels inspected.",
            "No new blind reviewers or independent rendered confirmations in this checkpoint.",
            "64kanji/1536word builder records are bounded seed/pool samples, not exhaustive random-pool safety.",
            "Direct-guard success proves the twelve specified pairs are absent, not semantic safety of every other option.",
        ],
    }
    save(D / "coordinator-visual-inspection.json", visual)
    index = [{"path": f.relative_to(R).as_posix(), "sha256": sha(f)}
             for f in sorted(D.rglob("*")) if f.is_file()]
    save(D / "artifact-index.json", index)
    start = copy.deepcopy(p["execution705StartingState"])
    start["runtime"] = {"contentVersion": manifest["contentVersion"], "runtimeHashesVerified": count,
                        "manifestSha256": sha(R / "manifest.json")}
    evidence = {
        "schemaVersion": 1, "execution": 705, "batch": "096", "status": STAGE,
        "startingState": start, "contentSnapshot": verification["contentSnapshot"],
        "reviewedTeachingSnapshot": verification["reviewedTeachingSnapshot"],
        "androidHead": APP, "productionBaseline": verification["productionBaseline"],
        "qualifiedTestOnlyAndroid": True, "latestAppMainClaimed": False,
        "fixtureSha256": verification["fixtureSha256"], "archiveSha256": verification["archiveSha256"],
        "appApk": frozen["appApk"], "testApk": frozen["testApk"], "contentVersion": manifest["contentVersion"],
        "runtimeHashesVerifiedAgain": count, "exactArchiveAndLocalRuntimeBytesEqual": True,
        "archiveGuardsUnchanged": True, "archiveBudgetEvidence": "docs/n1-sources/execution-704.json",
        "nativeExecution": receipt, "nativeTestsPassed": 2, "nativeTestsSkipped": 0,
        "terminalPerCaseStatus": [0, 0], "fullArchiveImportedOnce": True,
        "importedKanji": 1119, "importedWords": 5072, "n1Cards": 128, "problems": 0,
        "acceptedReadingParserEpoch": 1, "kanjiBuilderChecks": 64,
        "newDirectWordGuardBuilderChecks": 1536, "newDirectWordGuardPairs": 12,
        "allMappedReciprocalPairs": 1, "directedLinkTransitions": 2,
        "activatedBaselinePairs": 0, "completeArticleProjections": 2,
        "individualGlyphProbes": 112, "wholeWordRasterProbes": 8, "fontPanels": 4,
        "originalPngCaptures": 41, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED",
        "nativeExecutionAndCoordinatorVisualInspection": "passed",
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "runtimeChanged": False, "independentReviewersLaunched": 0, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 122, "remainingAdditions": 1106,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "routeEvidence": (D / "n1-096-article-route.json").relative_to(R).as_posix(),
        "fontEvidence": (D / "n1-096-font-raster.json").relative_to(R).as_posix(),
        "visualInspection": (D / "coordinator-visual-inspection.json").relative_to(R).as_posix(),
        "artifactIndex": (D / "artifact-index.json").relative_to(R).as_posix(),
        "limits": visual["limits"], "nextAction": NEXT,
        "diagnostics": [
            "Initial console inspection failed to print Japanese under cp1252 after entire request was loaded and checkpoint parsed; no required input missing.",
            "Out-of-range reads were corrected to actual file bounds; no permission denial.",
            "All raw text logs archived as deterministic lossless gzip to preserve original whitespace.",
        ],
    }
    save(E, evidence)
    path = R / "docs" / "n1-sources" / "batch-096-progress.json"
    packet = load(path)
    assert not packet["runtimeAccepted"] and not packet["runtimePublished"]
    packet.update(status=STAGE, nextAction=NEXT)
    packet["pendingGates"][0] = "Native execution705 passed; serial bounded original-session rendered confirmations and evidence-based semantic adjudication of actual N1/All/custom/random choices remain."
    packet["androidAcceptance"]["nativeAcceptance"] = "execution705-passed-awaiting-original-session-rendered-confirmations"
    packet["nativeExecution705"] = {
        "evidence": "docs/n1-sources/execution-705.json", "status": STAGE,
        "terminalPerCaseStatus": [0, 0], "testsSkipped": 0, "coordinatorInspectedPngCount": 41,
        "fullArchiveImportedOnce": True, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED", "runtimeAccepted": False, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier native-pending fields/limits remain historical; this additive record supersedes native execution/visual state only, not independent review or publication.",
    }
    save(path, packet)
    subprocess.run(["git", "-C", str(R), "diff", "--check"], check=True)
    print("Collected verified native receipts and all41PNGs; runtime untouched.")


def checkpoint():
    p = load(C / "progress.json")
    original = load(L / "progress-before-705.json")
    assert p["checkpoint"] == 704 and p["stage"] == "batch-096-native-execution-in-progress"
    head = git(R, "rev-parse", "HEAD")
    assert git(R, "rev-parse", "HEAD^") == HEAD
    clean(head)
    assert not git(R, "diff", HEAD, head, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    paths = git(R, "diff", "--name-only", HEAD, head).splitlines()
    assert all(n.startswith(("docs/n1-reviews/batch-096-native/execution-705/",
                             "docs/n1-sources/execution-705.json", "docs/n1-sources/batch-096-progress.json")) for n in paths)
    posted = load(C / "batch-096-native-705-issue-receipt.json")
    assert posted["user"]["login"] == "stop-cran"
    assert posted["body"] == (C / "batch-096-native-705-issue-body.txt").read_text(encoding="utf-8-sig")
    for item in load(D / "artifact-index.json"):
        assert sha(R.joinpath(*item["path"].split("/"))) == item["sha256"]
    runtime()
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in mutable)
    record = {
        "schemaVersion": 1, "execution": 705, "checkpoint": 705, "batch": "096",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "evidence": "docs/n1-sources/execution-705.json",
        "nativeTestsPassed": 2, "terminalPerCaseStatus": [0, 0], "testsSkipped": 0,
        "coordinatorInspectedPngCount": 41, "fullArchiveImportedOnce": True,
        "runtimeHashesVerifiedAgain": 8444, "kanjiBuilderChecks": 64,
        "directWordGuardBuilderChecks": 1536, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED", "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "ownedEmulatorStopped": True, "serial": "emulator-5580", "parentEmulatorPid": 12020, "qemuPid": 21048,
        "publishedAdditions": 122, "remainingAdditions": 1106, "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": posted["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(original),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    p.update(checkpoint=705, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution705CoordinatorCheckpoint"] = record
    p["batch096NativeExecutionCheckpoint"] = copy.deepcopy(record)
    persist(p)
    saved = load(C / "progress.json")
    assert all(saved[k] == v for k, v in original.items() if k not in mutable)
    save(L / "checkpoint-705-verification.json", record)
    print(json.dumps({"checkpoint": 705, "savedCommit": head, "historyPreserved": True,
                      "issueUpdate": posted["html_url"]}, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "collect": collect, "checkpoint": checkpoint}[sys.argv[1]]()
