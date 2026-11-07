import hashlib
import copy
import gzip
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "2be12432-54ac-4d75-82ab-630ff0541205"
HEAD = "4a652e4e6ca3c28a7d24e9720cf278347ab85f2e"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
N = C / "artifacts" / "batch-098-native-attempt-724"
I = C / "batch-098-native-inspection-724"
D = R / "docs" / "n1-reviews" / "batch-098-native" / "execution-724"
E = R / "docs" / "n1-sources" / "execution-724.json"
STAGE = "batch-098-native-executed-awaiting-rendered-confirmations"
NEXT = (
    "SAME098 serial bounded rendered confirmations in ORIGINAL reviewer sessions next: "
    "Claude d41cdccb-18bc-4302-803f-803d7bd4a007 THEN GPT 33216339-ddd8-411a-8aca-b73da1a3bae7. "
    "Read docs/n1-sources/execution-724.json and docs/n1-reviews/batch-098-native/execution-724/. "
    "BOTH native cases terminal0/no skips; full frozen archivecefedeb6/version0cbdc2723b0433f2/"
    "8449hashes through productionContentSync ONCE:1121kanji/5073words/130N1/zeroProblems/Roomepoch1. "
    "Coordinator inspected all48PNG: THREEfourfontpanels/all19Han plus45routecaptures via12contactsheets "
    "and eight original-resolution route reads; no actionable visual defect established. "
    "Visible U+5202/U+6C35 system fallback, exact fallback face unidentified. "
    "Actual default N1 options: medicinalpreparation/chemicalagent vs sturdy/unyieldingstrength, "
    "smelt/workmetals and criminalpunishment. ONE curated wrongcard available(剛); TWO actual "
    "productionfallbacks(冶/刑), NOT済N3/則N2. "
    "Inspect64 imported kanjibuilder records/16seeds/N1+All+boundedcustom+randomN1subset "
    "and128 preserved ONE directwordguard checks 洗剤/せっけん through All+custom/"
    "bothdirections/bothtargetorientations. 35 unique sampled kanji labels plus actualUI冶; "
    "samples NOT whole-pool semantic certification. Only onざい offered/persistedGood/Done1of1, "
    "NO kun; full/Lite rawザイ/スイ/セイ andかる/けず.る retained with explicit[ザイ]/[]. "
    "TEN injectedstrokes/trace+giveuprecall/persistence; ONE complete new剤 articleprojection "
    "plus exact reused洗剤component/洗commonword changes, TWO allmapped reciprocalpairs/"
    "FOURdirections/ONEactivatedbaselinepair/SystemBack/offline/N1selection. "
    "Original-session followups are dependent confirmations, NOT newblindcredit. "
    "OwnedAPI35 emulator5580/parent260/qemu16588 stopped; no owner/shared devices/heaps/guards changed, "
    "no phone/humanhandwriting/MLKit acceptance. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOT latestappmain; fresh721 JVM4/noskips and720 textual closure retained without rerun. "
    "All original source/baseline/link/reading/twofamily/native/currentmainnonrewritingmerge/"
    "changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIPentryhash/unchanged18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue gates remain BEFORE099. "
    "Parent15692 retainsrunner.lock: verifyliveancestry/session/signedheads/whollyclean, "
    "NOchildacquire/delete/unlock/readprobe. Approvedcontrol/committedpackets only; "
    "no optionalhistoricalsessionhelper. Original722denial and approvedrecovery preserved. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Published124/1228,1104remaining unchanged;098NOTdelivered. Physicalphone/generalrelease/whole-set "
    "outstanding. No099/runtimepublication/secondrunner."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).rstrip("\r\n")


def persist(p):
    before = load(L / "progress-before-724.json")
    for key, value in before.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert p[key] == value, key
    target = C / "progress.724.tmp"
    assert not target.exists()
    save(target, p)
    assert load(target) == p
    target.replace(C / "progress.json")


def start():
    for root, head in ((R, HEAD), (A, ANDROID)):
        assert git(root, "rev-parse", "HEAD") == head
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain=v1", "--untracked-files=all")
    assert git(R, "config", "--get", "commit.gpgsign") == "true"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (
        723, "098", "continue", "batch-098-native-preparation-signed-awaiting-native"
    )
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["execution723CoordinatorCheckpoint"] == p["execution723CoordinatorCheckpoint"]
    role = load(L / "preflight-724.json")
    runner = load(C / "runner.json")
    assert runner["sessionId"] == L.name and runner["pid"] == role["liveParentPid"]
    assert runner["status"] == "running" and not role["lockTouched"]
    assert not (L / "progress-before-724.json").exists()
    save(L / "progress-before-724.json", p)
    p["execution724StartingState"] = {
        "execution": 724, "batch": "098", "startingHead": HEAD, "androidHead": ANDROID,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME098 owned native execution and normally signed LOCAL evidence checkpoint; no reviewer, publication,099 or second runner.",
        "request": {
            "sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, complete approved issue and final checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved workspace inputs, committed source/review evidence and durable control helpers only; no optional historical-session helper access.",
        "actualNewPermissionDenials": [],
    }
    p["stage"] = "batch-098-native-execution-in-progress"
    persist(p)
    print("Starting724 persisted; all original historical root values preserved.")


def clean(head=HEAD):
    for root, expected in ((R, head), (A, ANDROID)):
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain=v1", "--untracked-files=all")


def verify_runtime(archive_path, expected):
    manifest = load(R / "manifest.json")
    assert manifest["contentVersion"] == "0cbdc2723b0433f2"
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) == expected["zipEntries"] <= 18000
        assert archive_path.stat().st_size == expected["compressedBytes"] <= 42 * 1024**2
        assert sum(i.file_size for i in archive.infolist()) == expected["inflatedBytes"] <= 80 * 1024**2
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
                if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                    data, local = data.replace(b"\r\n", b"\n"), local.replace(b"\r\n", b"\n")
                assert data == local and hashlib.sha256(data).hexdigest() == digest, name
                count += 1
        assert count == 8449
        assert retained == expected["retainedBytes"] <= 56 * 1024**2
    return count


def collect():
    clean()
    assert not D.exists() and not E.exists()
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 723 and progress["stage"] == "batch-098-native-execution-in-progress"
    receipt = load(C / "batch-098-native-attempt-724-execution.json")
    route = load(N / "n1-098-article-route.json")
    raster = load(N / "n1-098-font-raster.json")
    frozen = load(R / "docs" / "n1-sources" / "execution-723.json")
    verification = load(C / "batch-098-native-fixture-verification.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert not any(receipt[k] for k in ["parentLockTouched", "guestOrAppHeapChanged", "guardsChanged"])
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"],
            route["acceptedReadingParserEpoch"]) == (1121, 5073, 130, 0, 1)
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"],
            route["completeArticleProjections"], route["activatedBaselinePairs"],
            route["changedReusedArticles"]) == (2, 4, 1, 1, 2)
    assert route["onlyOnZaiNoKunPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 10 and route["drawingGradeRecordedOnNext"]
    assert route["actualN1CuratedAvailable"] == 1 and route["actualN1FallbackOptions"] == 2
    assert route["quizOnKeys"] == ["ざい"] and route["quizKunKeys"] == []
    for prefix in ("", "fullProjection"):
        on = route["fullOnyomi" if not prefix else prefix + "Onyomi"]
        kun = route["fullKunyomi" if not prefix else prefix + "Kunyomi"]
        assert on == ["ザイ", "スイ", "セイ"] and kun == ["かる", "けず.る"]
    assert route["liteQuizOnyomi"] == route["fullProjectionQuizOnyomi"] == ["ザイ"]
    assert route["liteQuizKunyomi"] == route["fullProjectionQuizKunyomi"] == []
    guards = route["directGuardBuilderChecks"]
    assert len(guards) == 128
    assert {(r["target"], r["excluded"]) for r in guards} == {("洗剤", "せっけん"), ("せっけん", "洗剤")}
    for row in guards:
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
            assert sum(o["kanji"] == "剤" for o in row["options"]) == 1
    actual = route["exactDefaultMeaningOptions"]
    assert {o["kanji"] for o in actual} == {"剤", "剛", "冶", "刑"}
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (76, 8, 3)
    assert len(raster["rows"]) == 84 and raster["fontScale"] == 1
    assert all(r.get("hasGlyph", True) for r in raster["rows"])
    log = (N / "instrumentation.txt").read_text(encoding="utf-8-sig")
    records = re.split(r"INSTRUMENTATION_STATUS_CODE: ", log)
    terminals = []
    for index in range(len(records) - 1):
        if records[index + 1].startswith("0"):
            cls = re.findall(r"^INSTRUMENTATION_STATUS: class=(.+)\s*$", records[index], re.MULTILINE)[-1].strip()
            test = re.findall(r"^INSTRUMENTATION_STATUS: test=(.+)\s*$", records[index], re.MULTILINE)[-1].strip()
            terminals.append({"class": cls, "test": test, "status": 0})
    assert {(t["class"], t["test"]) for t in terminals} == {
        ("io.github.stopcran.kanji.ui.N1Batch098GlyphTest", "agentLookalikesAndScopedHanAcrossFourProductionFamilies"),
        ("io.github.stopcran.kanji.ui.N1Batch098ArticleTest",
         "fullSingleImportOfflineAgentReusedSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack"),
    }
    assert len(terminals) == 2 and "OK (2 tests)" in log
    assert not re.search(r"STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED|assumptionFailure|ignored", log)
    for path, digest in [(verification["archive"], verification["archiveSha256"]),
                         (verification["fixture"], verification["fixtureSha256"]),
                         (frozen["appApk"]["path"], frozen["appApk"]["sha256"]),
                         (frozen["testApk"]["path"], frozen["testApk"]["sha256"])]:
        assert sha(Path(path)) == digest
    count = verify_runtime(Path(verification["archive"]), verification)
    assert len(list(N.glob("*.png"))) == 48
    assert len(list(I.glob("sheet-*.png"))) == 12
    assert sum(len(s["sources"]) for s in load(I / "index.json")) == 45
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
    recipes = D / "receipts"
    recipes.mkdir()
    for source in [Path(__file__), C / "preflight-724.ps1", C / "run-724-native.ps1",
                   C / "inspect-batch-098-native-724.py", L / "preflight-724.json",
                   C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt"]:
        shutil.copyfile(source, recipes / source.name)
    unique = sorted({json.dumps(o, ensure_ascii=False, sort_keys=True) for row in pools for o in row["options"]})
    assert len(unique) == 35
    visual = {
        "snapshot": verification["contentSnapshot"],
        "reviewedTeachingSnapshot": verification["reviewedTeachingSnapshot"],
        "reviewer": "Coordinator, GPT-6.1 Sol (gpt-6.1-sol)",
        "scope": "Native rendered inspection, not a new independent linguistic/source review.",
        "inspectedOriginalPngCount": 48,
        "fontPanelsInspectedAtOriginalResolution": [f"n1-098-font-panel-{i}.png" for i in range(1, 4)],
        "routeCapturesInspectedViaContactSheets": 45,
        "contactSheetsInspected": [f"contact-sheets/sheet-{i:02d}.png" for i in range(1, 13)],
        "additionalOriginalResolutionReads": [
            "n1-098-meaning-question.png", "n1-098-selection.png", "n1-098-kanji-11.png",
            "n1-098-kanji-20.png", "n1-098-kanji-36.png",
            "n1-098-curated-ざい-question.png", "n1-098-curated-ざい-feedback.png",
            "n1-098-drawing-feedback.png",
        ],
        "verdict": "No actionable visual defect established in these captures; original-session confirmations and independent sampled-choice semantic adjudication remain.",
        "glyphs": "All19 scoped Han readable across Gothic/Mincho/Textbook/Brush; 剤/済/剛/則 and radical variants distinguishable. Cmap-absent U+5202/U+6C35 visibly render without blank/tofu across four families. Exact fallback face not identified. Textbook wraps final 剤 of 推進剤 onto the next line in font panel3 without clipping; other panels and whole-word rasters retain the characters.",
        "articles": "One complete new 剤 article projection and exact two reused navigation changes covered. Japanese/examples/translations and links readable. Reading table needs advertised horizontal scroll; right-scrolled captures expose full example text, with expected left-column clipping. Later captures cover vertically clipped paragraphs. No fresh full teaching review of reused articles is claimed.",
        "quiz": "Actual N1 UI has medicinal preparation/chemical agent vs sturdy/unyielding strength, smelt/work metals and criminal punishment. Only 剛 is available curated; 冶/刑 are the two actual fallbacks, not N3済/N2則. These shown meanings are semantically distinct. All64 builder records read;35 unique sampled labels contain no established alternate correct meaning for 剤. Additional actualUI冶 is preserved. Original-session independent semantic confirmation remains; not unrestricted pool certification.",
        "sampledBuilderDistinctOptions": [json.loads(o) for o in unique],
        "actualDefaultMeaningOptions": actual,
        "reading": "Only onざい offered, readable question/feedback and Done1/1; no kun offered. Full/Lite raw readings retained while explicit[ザイ]/[] transported. Sole normalized key persisted Good; feedback's full reference readings are not additional offered keys.",
        "drawing": "Injected ten-stroke reference trace and shape-only feedback visible; recall give-up displays reference and persists grade on Next. Offline model-unavailable state is explicit. No human-handwriting/MLKit acceptance.",
        "newConsequentialUnresolvedVisualClaims": [],
        "limits": [
            "API35 emulator/default fontScale1 only; physical phone/general-release acceptance outstanding.",
            "hasGlyph/nonblank/raster hashes alone are not legibility/fallback-face evidence; actual panels inspected.",
            "No new blind reviewers or independent rendered confirmations in execution724.",
            "64kanji/128word builder checks are bounded seed/pool samples, not exhaustive random-pool safety.",
            "One preserved direct guard proves that pair absent, not semantic safety of every other word option.",
            "Original two-family textual review inherited; exact changed reused passages only, not a fresh full review of reused articles.",
            "Original722 denial and approved parent recovery remain separate historical records; no new denial or policy change.",
        ],
    }
    save(D / "coordinator-visual-inspection.json", visual)
    index = [{"path": f.relative_to(R).as_posix(), "sha256": sha(f)}
             for f in sorted(D.rglob("*")) if f.is_file()]
    save(D / "artifact-index.json", index)
    evidence = {
        "schemaVersion": 1, "execution": 724, "batch": "098", "status": STAGE,
        "startingState": copy.deepcopy(progress["execution724StartingState"]),
        "contentSnapshot": verification["contentSnapshot"],
        "reviewedTeachingSnapshot": verification["reviewedTeachingSnapshot"],
        "androidHead": ANDROID, "productionBaseline": verification["productionBaseline"],
        "qualifiedTestOnlyAndroid": True, "latestAppMainClaimed": False,
        "fixtureSha256": verification["fixtureSha256"], "archiveSha256": verification["archiveSha256"],
        "appApk": frozen["appApk"], "testApk": frozen["testApk"],
        "contentVersion": route["contentVersion"], "runtimeHashesVerifiedAgain": count,
        "exactArchiveAndLocalRuntimeBytesEqual": True, "archiveGuardsUnchanged": True,
        "archiveBudgetEvidence": "docs/n1-reviews/batch-098-native/preparation-receipts/batch-098-native-fixture-verification.json",
        "nativeExecution": receipt, "nativeTestsPassed": 2, "nativeTestsSkipped": 0,
        "terminalPerCaseStatus": terminals, "fullArchiveImportedOnce": True,
        "importedKanji": 1121, "importedWords": 5073, "n1Cards": 130, "problems": 0,
        "acceptedReadingParserEpoch": 1, "kanjiBuilderChecks": 64,
        "preservedDirectWordGuardBuilderChecks": 128, "preservedDirectWordGuardPairs": 1,
        "newDirectWordGuardPairs": 0, "allMappedReciprocalPairs": 2, "directedLinkTransitions": 4,
        "activatedBaselinePairs": 1, "completeArticleProjections": 1, "changedReusedArticles": 2,
        "individualGlyphProbes": 76, "wholeWordRasterProbes": 8, "fontPanels": 3,
        "originalPngCaptures": 48, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED",
        "nativeExecutionAndCoordinatorVisualInspection": "passed",
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "runtimeChanged": False, "independentReviewersLaunched": 0, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "publishedAdditions": 124, "remainingAdditions": 1104,
        "lastPublishedCommit": progress["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "routeEvidence": (D / "n1-098-article-route.json").relative_to(R).as_posix(),
        "fontEvidence": (D / "n1-098-font-raster.json").relative_to(R).as_posix(),
        "visualInspection": (D / "coordinator-visual-inspection.json").relative_to(R).as_posix(),
        "artifactIndex": (D / "artifact-index.json").relative_to(R).as_posix(),
        "limits": visual["limits"], "nextAction": NEXT,
        "diagnostics": [
            "Initial console checkpoint summary failed under cp1252; corrected to UTF-8 before parsing full request checkpoint.",
            "Preserved compiled fixture/APKs used unchanged, no redundant compilation or host tests.",
            "All raw text logs archived as deterministic lossless gzip.",
        ],
    }
    save(E, evidence)
    path = R / "docs" / "n1-sources" / "batch-098-progress.json"
    packet = load(path)
    assert not packet["runtimeAccepted"] and not packet["runtimePublished"]
    packet.update(status=STAGE, nextAction=NEXT)
    packet["pendingGates"][0] = "Native execution724 passed; serial original-session rendered confirmations and evidence-based semantic adjudication of actual N1/All/custom/random choices remain."
    packet["androidAcceptance"]["nativeAcceptance"] = "execution724-passed-awaiting-original-session-rendered-confirmations"
    packet["nativeExecution724"] = {
        "evidence": "docs/n1-sources/execution-724.json", "status": STAGE,
        "terminalPerCaseStatus": [0, 0], "testsSkipped": 0, "coordinatorInspectedPngCount": 48,
        "fullArchiveImportedOnce": True, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED", "runtimeAccepted": False, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier native-pending fields remain historical; this additive record supersedes native execution/visual state only, not independent review/publication.",
    }
    save(path, packet)
    subprocess.run(["git", "-C", str(R), "diff", "--check"], check=True)
    print("Verified native receipts/all48PNGs archived; runtime untouched.")


def checkpoint():
    progress = load(C / "progress.json")
    original = load(L / "progress-before-724.json")
    assert progress["checkpoint"] == original["checkpoint"] == 723
    head = git(R, "rev-parse", "HEAD")
    assert git(R, "rev-parse", "HEAD^") == HEAD
    clean(head)
    assert not git(R, "diff", HEAD, head, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    paths = git(R, "-c", "core.quotepath=false", "diff", "--name-only", HEAD, head).splitlines()
    assert all(n.startswith(("docs/n1-reviews/batch-098-native/execution-724/",
                             "docs/n1-sources/execution-724.json", "docs/n1-sources/batch-098-progress.json")) for n in paths)
    posted = load(C / "batch-098-native-724-issue-receipt.json")
    assert posted["user"]["login"] == "stop-cran"
    assert posted["body"] == (C / "batch-098-native-724-issue-body.txt").read_text(encoding="utf-8-sig")
    for item in load(D / "artifact-index.json"):
        assert sha(R.joinpath(*item["path"].split("/"))) == item["sha256"]
    verification = load(C / "batch-098-native-fixture-verification.json")
    verify_runtime(Path(verification["archive"]), verification)
    receipt = load(C / "batch-098-native-attempt-724-execution.json")
    record = {
        "schemaVersion": 1, "execution": 724, "checkpoint": 724, "batch": "098",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "evidence": "docs/n1-sources/execution-724.json",
        "nativeTestsPassed": 2, "terminalPerCaseStatus": [0, 0], "testsSkipped": 0,
        "coordinatorInspectedPngCount": 48, "fullArchiveImportedOnce": True,
        "runtimeHashesVerifiedAgain": 8449, "kanjiBuilderChecks": 64,
        "preservedDirectWordGuardBuilderChecks": 128, "independentRenderedConfirmations": "pending",
        "livePoolSemanticAcceptance": "UNVERIFIED", "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "ownedEmulatorStopped": True, "serial": receipt["serial"],
        "parentEmulatorPid": receipt["parentEmulatorPid"], "qemuPid": receipt["qemuPid"],
        "publishedAdditions": 124, "remainingAdditions": 1104, "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": posted["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(original),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
        "checkpointHelper": str(Path(__file__)), "checkpointHelperSha256": sha(Path(__file__)),
    }
    progress.update(checkpoint=724, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    progress["execution724CoordinatorCheckpoint"] = record
    progress["batch098NativeExecutionCheckpoint"] = copy.deepcopy(record)
    persist(progress)
    saved = load(C / "progress.json")
    assert saved["execution724CoordinatorCheckpoint"] == record
    save(L / "checkpoint-724-verification.json", record)
    print(json.dumps({"checkpoint": 724, "savedCommit": head, "historyPreserved": True,
                      "issueUpdate": posted["html_url"]}, indent=2))


if __name__ == "__main__":
    {"start": start, "collect": collect, "checkpoint": checkpoint}[sys.argv[1]]()
