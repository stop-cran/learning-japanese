import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
LOG = C / "logs" / "45e618f9-8a01-4bfc-99e2-7739bc2bf9f0"
HEAD = "f6f9b9425b483ed98950c67c35610caaccd6c786"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
ATTEMPT = C / "artifacts" / "batch-085-native-attempt-596"
DEST = R / "docs" / "n1-reviews" / "batch-085-native" / "attempt-596"
NEXT = (
    "SAME085 serial ORIGINAL-family dependent VISUAL confirmations NEXT; persist/yield before integration/publication or086. "
    "Read docs/n1-sources/execution-596.json and docs/n1-reviews/batch-085-native/attempt-596 "
    "(87 original PNGs,15 labelled full-frame sheets,index,raw terminal results,route/raster JSON,coordinator visual report). "
    "Reuse ClaudeOpus5.5 session58040cfc-7f07-4bd0-bb1e-18ba6bf9c793 then GPT6.1Sol "
    "session7e74aba9-d92a-4615-b858-c68100c7dfdb serially; ownoriginalfindings/exactdiff/nativeprovenance/"
    "boundedPNGpacket, actualmodels/read-depth/toolresults/process-exits, at most ONEreviewer/no snapshot edits. "
    "Same initialteachinga7512a5e plus exact reviewed effort exclusion29a53380, unchanged runtime/archive1d2e3290/"
    "version0c514711ae8d3212/8413hashes; Q1resolved/othersoptional and all original review limits preserved. "
    "Both named085nativecases terminal0/no skips passed596: productionContentSyncONCE1108kanji5063words117N1/"
    "zeroProblems/acceptedRoomepoch1, Full/Lite full sourceonギョウ/kunこ.る,こ.らす,こご.らす,こご.らせる,こご.る retained; "
    "curatedonギョウ/kunこ.る,こ.らす=>ぎょう/こる BOTHkindspersistedGood/done; こ.らす shares normalizedこる, "
    "NOTindependentqueuedmastery. Exact default4N1/Allbuilder凝准冗凹/no padding and actualN1meaningUI; "
    "fourcompletearticleprojections+changed固bullet only/fourpairs/eightdirections/SystemBack/offline/N1selection/"
    "16injectedreference strokes/trace/recall/persistence. All39Han/fourfamilies/156individual+12wholewordrasters/"
    "threeComposepanels legible in coordinator inspection of all87 full-frame scaled sheets+eight originals "
    "individually, NOT87fullresolutionreads/independentvisualclosure/fallbackfaceidentity. Horizontal table "
    "auto-scroll shows target cells, not every column simultaneously. Offline model unavailable; injectedtrace/"
    "giveup NOThumanhandwriting/MLKit/phone. OwnedreadonlyAPI35serial5580 parent30032/qemu24604 stopped. "
    "Parent19008runner.lock NEVER opened/acquired/deleted/unlocked. Any justified future native retry needs "
    "fresh localANDremote5580/5581 includingTimeWait/device/PIDs/liveparentancestry/checkpoint/exactsignedheads/"
    "whollycleanworktrees; no alternateport without authorization/shareddeviceinterference/heapguardincrease. "
    "HOST4passed594/compile595 need no repetition absent change. Later fresh latestmainnormalmerge/surgical "
    "reconciliation/substantiveteachingreview/combinedPython-validator-vocabulary-manifest-membership-baseline-links/"
    "original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepaths/normalsigning/"
    "ownerfastforward/terminalCI/EVERYimmutablepublicZIPruntimehash/verifiedownerissue60 BEFORE086. "
    "Approvedcontrol/committed sources only; no optional historicalsessionhelpers. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. Published111/1228,1117remaining/latestpublished97a16b00 unchanged; "
    "085 not delivered/finallyaccepted. Physicalphone/generalrelease/whole-set outstanding, projectincomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], text=True).strip()


def clean(root, head):
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "log", "-1", "--format=%G?") == "G"
    assert not git(root, "status", "--porcelain")


def record():
    clean(R, HEAD)
    clean(A, APP)
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["stage"]) == (595, "batch-085-native-execution-in-progress")
    receipt = load(ATTEMPT / "execution.json")
    assert receipt == load(C / "batch-085-native-attempt-596-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert receipt["prelaunch"]["connections"] == []
    assert not any(receipt[key] for key in ("parentLockTouched", "guestOrAppHeapChanged", "guardsChanged"))
    raw = (ATTEMPT / "instrumentation.txt").read_text(encoding="utf-8-sig")
    cases, fields = [], {}
    for line in raw.splitlines():
        if line.startswith("INSTRUMENTATION_STATUS: "):
            name, value = line.removeprefix("INSTRUMENTATION_STATUS: ").split("=", 1)
            fields[name] = value
        elif line.startswith("INSTRUMENTATION_STATUS_CODE: "):
            code = int(line.split(": ", 1)[1])
            if code != 1:
                cases.append({"class": fields["class"], "test": fields["test"], "status": code})
            fields = {}
    assert len(cases) == 2 and all(case["status"] == 0 for case in cases) and "OK (2 tests)" in raw
    assert {case["class"] for case in cases} == {
        "io.github.stopcran.kanji.ui.N1Batch085ArticleTest", "io.github.stopcran.kanji.ui.N1Batch085GlyphTest"}
    route = load(ATTEMPT / "n1-085-article-route.json")
    for key, value in {
        "contentVersion": "0c514711ae8d3212", "archiveRequests": 1, "importedKanji": 1108,
        "importedWords": 5063, "problems": 0, "n1Cards": 117, "acceptedReadingParserEpoch": 1,
        "fullOnyomi": ["ギョウ"], "fullKunyomi": ["こ.る", "こ.らす", "こご.らす", "こご.らせる", "こご.る"],
        "quizOnKeys": ["ぎょう"], "quizKunKeys": ["こる"],
        "liteQuizOnyomi": ["ギョウ"], "liteQuizKunyomi": ["こ.る", "こ.らす"],
        "mappedReciprocalPairs": 4, "directedLinkTransitions": 8, "completeArticleProjections": 4,
        "changedReusedBullets": 1, "bothCuratedKindsPersistedGoodAndDone": True,
        "touchInjectedReferenceStrokes": 16, "drawingTraceThenRecall": True,
        "drawingGradeRecordedOnNext": True, "offline": True, "passed": True, "phoneEvidence": False,
    }.items():
        assert route[key] == value, key
    assert route["fullProjectionOnyomi"] == route["fullOnyomi"]
    assert route["fullProjectionKunyomi"] == route["fullKunyomi"]
    assert route["fullProjectionQuizOnyomi"] == route["liteQuizOnyomi"]
    assert route["fullProjectionQuizKunyomi"] == route["liteQuizKunyomi"]
    options = {"凝": "congeal; become absorbed", "准": "quasi-; associate rank",
               "冗": "superfluous; redundant", "凹": "concave; sunken"}
    for scope in ("N1", "All"):
        pool = route["productionBuilderN1AndAllExactChoices"][scope]
        assert pool["allThreeCuratedAvailable"] and pool["defaultFourNoPadding"]
        assert {entry["kanji"]: entry["title"] for entry in pool["options"]} == options
    assert {entry["kanji"]: entry["title"] for entry in route["exactDefaultMeaningOptions"]} == options
    raster = load(ATTEMPT / "n1-085-font-raster.json")
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (156, 12, 3)
    assert len(raster["rows"]) == 168
    preparation = load(C / "batch-085-native-fixture-verification.json")
    assert {row["character"] for row in raster["rows"] if "character" in row} == set(preparation["plannedGlyphs"])
    assert {row["font"] for row in raster["rows"]} == {"Gothic", "Mincho", "Textbook", "Brush"}
    assert len(list(ATTEMPT.glob("*.png"))) == 87
    sheets = load(ATTEMPT / "inspection" / "index.json")
    assert len(sheets) == 15
    assert sorted(name for sheet in sheets for name in sheet["originals"]) == sorted(p.name for p in ATTEMPT.glob("*.png"))
    DEST.mkdir(exist_ok=False)
    index = []
    for path in sorted(ATTEMPT.rglob("*")):
        if not path.is_file():
            continue
        destination = DEST / path.relative_to(ATTEMPT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        zipped = path.suffix == ".txt"
        if zipped:
            destination = destination.with_suffix(destination.suffix + ".gz")
            destination.write_bytes(gzip.compress(data, mtime=0))
            assert gzip.decompress(destination.read_bytes()) == data
        else:
            shutil.copyfile(path, destination)
        index.append({"source": str(path), "archive": destination.relative_to(R).as_posix(),
                      "sourceSha256": sha(path), "sha256": sha(destination), "losslessGzipVerified": zipped})
    provenance = []
    for name in ("execution-596-preflight.py", "run-596-native.ps1", "execution-596-contact-sheets.py",
                 "execution-596-record.py", "execution-596-visual-inspection.txt", "execution-596-start.json"):
        source = C / name
        destination = DEST / name
        shutil.copyfile(source, destination)
        provenance.append({"source": str(source), "archive": destination.relative_to(R).as_posix(), "sha256": sha(source)})
    index_path = DEST / "artifact-index.json"
    save(index_path, index)
    native = {
        "execution": 596, "status": "native-passed-awaiting-original-family-visual-confirmation",
        "nativeAcceptancePassed": True, "independentVisualConfirmation": "outstanding",
        "runtimeAccepted": False, "runtimePublished": False,
        "caseResults": cases, "nativeSkips": 0, "route": route, "executionReceipt": receipt,
        "glyphProbeCounts": {"actualHan": 39, "individual": 156, "wholeWord": 12, "fontFamilies": 4, "panels": 3},
        "artifactIndex": index_path.relative_to(R).as_posix(), "artifactIndexSha256": sha(index_path),
        "originalPngCount": 87, "contactSheetCount": 15,
        "coordinatorVisualReport": (DEST / "execution-596-visual-inspection.txt").relative_to(R).as_posix(),
        "coordinatorInspection": "All87 in15 labelled full-frame scaled sheets; eight originals individually, including allthree font panels. Not87 full-resolution reads or independent closure.",
        "phoneEvidence": False, "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "limits": [
            "Injected reference strokes and recall give-up are not human handwriting/MLKit recognition; offline model unavailable.",
            "Exact default four choices covered for N1/All production builder and N1 UI; All UI and larger/custom/random/padded/partial pools not tested.",
            "Fallback-face identity not established by readability or raster hashes; default fixture sizes/scale only.",
            "Selectedこ.らす shares normalizedこる withこ.る, not independent queued mastery; full source-only readings retained.",
            "Table horizontal auto-scroll reveals target cells, not all columns simultaneously.",
            "Complete four new article projections plus changed固bullet only, not a fresh review of unchanged固body.",
            "Full archive is a frozen local envelope, not immutable public ZIP acceptance or publication.",
        ],
        "nextAction": NEXT,
    }
    evidence = {
        "schemaVersion": 1, "execution": 596, "batch": "085",
        "startingState": state["execution596StartingState"],
        "contentSnapshot": preparation["contentSnapshot"],
        "initialTeachingSnapshot": "a7512a5e6ce6d04b271099de834e431436363c3d",
        "reviewConfirmedCorrectionHead": "29a533800ed0d45e6269991d4a19e3b134057d6a",
        "androidHead": APP, "productionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "nativeAcceptance": native, "provenance": provenance,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "independentReviewersLaunched": 0, "actualNewPermissionDenials": [],
        "publishedAdditions": 111, "remainingAdditions": 1117, "lastPublishedCommit": state["lastPublishedCommit"],
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    }
    save(R / "docs" / "n1-sources" / "execution-596.json", evidence)
    path = R / "docs" / "n1-reviews" / "batch-085-reconciliation.json"
    original = path.read_text(encoding="utf-8")
    old = json.loads(original)
    assert "nativeAcceptance596" not in old
    original = original.replace('"status": "' + old["status"] + '"', '"status": "' + native["status"] + '"', 1)
    addition = json.dumps({"nativeAcceptance596": native}, ensure_ascii=True, indent=2)[2:-2]
    path.write_text(original.rstrip()[:-1].rstrip() + ",\n" + addition + "\n}\n", encoding="utf-8")
    current = load(path)
    assert all(current[key] == value for key, value in old.items() if key != "status")
    print("Both terminal cases0/zero skips and all route invariants verified; 87 PNGs/15 sheets/qualified report archived; runtime unchanged.")


def checkpoint():
    state = load(C / "progress.json")
    before = load(LOG / "progress-before-596.json")
    assert state["checkpoint"] == 595 and state["stage"] == "batch-085-native-execution-in-progress"
    saved = git(R, "rev-parse", "HEAD")
    clean(R, saved)
    clean(A, APP)
    assert not git(R, "diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    summary = {
        "schemaVersion": 1, "execution": 596, "checkpoint": 596, "batch": "085",
        "status": "continue", "stage": "native-passed-awaiting-original-family-visual-confirmation",
        "savedCommit": saved, "signature": "G", "evidence": "docs/n1-sources/execution-596.json",
        "androidHead": APP, "nativePassedCases": 2, "nativeSkips": 0, "originalPngCount": 87,
        "coordinatorPngInspection": "all87 in15 full-frame scaled contact sheets plus eight originals individually",
        "independentVisualConfirmation": "outstanding", "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "publishedAdditions": 111, "remainingAdditions": 1117,
        "lastPublishedCommit": state["lastPublishedCommit"], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "nextAction": NEXT,
    }
    state.update({"checkpoint": 596, "status": "continue", "stage": summary["stage"], "nextAction": NEXT, "blocker": None})
    state["execution596CoordinatorCheckpoint"] = summary
    state["batch085NativeCheckpoint"] = summary
    for key, value in before.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert state[key] == value, key
    temp = C / "progress.596.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")
    save(LOG / "checkpoint-596.json", summary)
    body = (
        f"Batch085 SAME checkpoint596: frozen native acceptance passed; signed LOCAL evidence `{saved}` (not published content). "
        "Both named N1Batch085ArticleTest/GlyphTest cases ended terminal status0, zero skips. "
        "Full git envelope imported ONCE through production ContentSync:1108kanji/5063words/117N1, zero problems, "
        "version0c514711ae8d3212, accepted Room parser epoch1. Full/Lite readings preserved; both curated reading kinds "
        "offered and persisted Good/done (onぎょう/kunこる; selectedこ.らす sharesこる, not independent mastery). "
        "Exact default N1/All production-builder choices and N1 meaning UI, four complete new article projections/"
        "changed固bullet, four reciprocal pairs/eight directions/SystemBack/offline/selection/16-reference-stroke "
        "trace-to-recall/persistence passed. All39 Han/four families/156individual+12wholeword probes/three Compose panels "
        "inspected:87 preserved PNGs in15 labelled full-frame scaled sheets plus eight originals individually; no blank/"
        "replacement/materially misleading glyph observed. Fallback-face identity not claimed; scrollable table target cells "
        "shown, not all columns simultaneously. Owned readonly API35 emulator5580 parent30032/qemu24604 stopped; "
        "no shared-device, production, heap/guard or parent-lock changes. Injected tracing/recall give-up is NOT "
        "human handwriting/MLKit/phone acceptance; offline model unavailable. "
        "Evidence:docs/n1-sources/execution-596.json and docs/n1-reviews/batch-085-native/attempt-596. "
        "Next:serial original-family dependent visual confirmations, then checkpoint before combined-main "
        "integration/publication. No reviewer launched here. Original textual findings/limits retained. "
        "Published111/1228,1117remaining unchanged;085 not delivered/finallyaccepted. Physicalphone/generalrelease/"
        "whole-set acceptance outstanding; no086."
    )
    (C / "execution-596-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps({"checkpoint": 596, "signedCommit": saved, "status": "continue"}))


def finalize():
    state = load(C / "progress.json")
    before = load(LOG / "progress-before-596.json")
    assert state["checkpoint"] == 596 and state["status"] == "continue"
    receipt_path = C / "execution-596-issue-verified.json"
    issue = load(receipt_path)
    body = (C / "execution-596-issue-body.txt").read_bytes().decode("utf-8").rstrip()
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    for name in ("execution596CoordinatorCheckpoint", "batch085NativeCheckpoint"):
        state[name]["issueUpdate"] = issue["html_url"]
        state[name]["ownerAuthorAndBodyVerified"] = True
        state[name]["issueReceiptSha256"] = sha(receipt_path)
    clean(R, state["execution596CoordinatorCheckpoint"]["savedCommit"])
    clean(A, APP)
    assert not git(R, "diff", HEAD, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for key, value in before.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert state[key] == value, key
    evidence = load(R / "docs" / "n1-sources" / "execution-596.json")
    for entry in load(R / evidence["nativeAcceptance"]["artifactIndex"]) + evidence["provenance"]:
        assert sha(R / entry["archive"]) == entry["sha256"]
    temp = C / "progress.596.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")
    save(LOG / "checkpoint-596.json", state["execution596CoordinatorCheckpoint"])
    save(LOG / "checkpoint-596-final-verification.json", {
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "signedCleanContentHead": state["execution596CoordinatorCheckpoint"]["savedCommit"],
        "signedCleanAndroidHead": APP, "runtimeBytesUnchanged": True, "allArchivedHashesVerified": True,
        "issueAuthorAndBodyVerified": True, "issueUpdate": issue["html_url"],
    })
    print("Checkpoint596 verified: all historical values preserved, signed clean worktrees, unchanged runtime, every archived hash, exact owner issue body.")


{"record": record, "checkpoint": checkpoint, "finalize": finalize}[sys.argv[1]]()
