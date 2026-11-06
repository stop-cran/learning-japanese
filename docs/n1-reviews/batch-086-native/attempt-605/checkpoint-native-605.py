import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
LOG = C / "logs" / "bde9f84b-987b-4ebc-98f6-97e1f8e4e49b"
HEAD = "e1077c7715de31b3cca989d8329bae375ab9cbbd"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
FOLDER = R / "docs" / "n1-reviews" / "batch-086-native" / "attempt-605"
NEXT = (
    "SAME086 dependent visual confirmations using original Claude3008102f-fcab-48aa-8298-7bf950377cc3 "
    "and GPT60bd24a1-86d7-476d-a371-9af354cab393 sessions, serial read-only one at a time with actual exit/model/range evidence. "
    "Read docs/n1-sources/execution-605.json, batch-086-native/attempt-605/visual-inspection.json, all19 indexed sheets/original76PNGs, "
    "original reports/reconciliation and exact fixture. Native605 BOTH cases terminal0, no skips/errors; full archive6667318d "
    "productionContentSync ONCE/1109kanji/5064words/118N1/zeroProblems/version86e8cb13aa72ecd0/acceptedRoomepoch1. "
    "All31Han fourfamilies legible in three directly inspected panels including systemfallback dots丶/几; "
    "124individual+16wholeword automatedrasters are hashes/nonblank probes, not separately saved PNGs or exact fallback-face identification. "
    "Coordinator inspected all76 native captures via19labelled sheets, plus threefontpanels/meaningquestion/legend02 at original size; "
    "no actionable visual defect established. Original textual reviews unchanged at f59c65fd; supplemental visuals are dependent NOT newblindcredit. "
    "Actual default N1 meaning labels concave;sunken/quasi-;associate rank/commonplace;mediocre/beast;animal; "
    "builderseed604 N1 labels concave;sunken/commonplace;mediocre/mosquito/pavilion;restaurant building; "
    "N1 has only凹 curated plus twofallbacks, All has丸/九/凹. Judge displayed semantic alternatives, not arbitrarypool safety. "
    "Both queuedkeysぼん/はん persistedGood/done, kun[] noquestions/logs; allfive rawreadings/order retained; "
    "rawおうよ.そ modern usage explicitly UNVERIFIED source-only. Three-stroke injectedtrace/giveuprecall/persistedgrade "
    "NOT humanhandwriting/MLKit/phone. Sevenreciprocalpairs/fourteendirections inclaliases/reused平/例/全, "
    "eight directwordguards, two complete newarticle projections/six changedreused passages, SystemBack/offline. "
    "Owned emulator-5580 parent23060/qemu25336 stopped and adbempty; do not relaunch merely for same evidence. "
    "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, not latest appmain; noheap/guardincrease/appchange. "
    "Parent19008 owns runner.lock; verifyliveancestry/session/checkpoint/exactsignedheads/whollycleanworktrees; "
    "NOchild reacquire/delete/unlock. Approvedcontrol/committedsources only; preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "After dependentvisualclosure, original currentmain normalmerge/surgicalreconciliation/changedteachingreview/combinedchecks/normal signing/"
    "ownerfastforward/terminalCI/EVERYimmutablepublicZIP runtimehash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue gates remain. Published112/1228,1116remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding, project incomplete. No087 or publication in next bounded visual checkpoint."
)


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def update(value):
    target = C / "progress.605.tmp"
    assert not target.exists()
    save(target, value)
    assert load(target) == value
    target.replace(C / "progress.json")


def start():
    state = load(C / "progress.json")
    assert state["checkpoint"] == 604 and state["status"] == "continue"
    assert state["batch"] == "086" and state["stage"] == "native-prepared-compiled-not-executed"
    for root, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == LOG.name and runner["status"] == "running"
    before = LOG / "progress-before-605.json"
    assert not before.exists()
    request = LOG / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    parsed = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["checkpoint"] == 604
    shutil.copyfile(C / "progress.json", before)
    state["execution605StartingState"] = {
        "execution": 605, "batch": "086", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "scope": "SAME086 frozen native execution, direct visual inspection and signed LOCAL evidence; no publication/reviewer/087.",
        "request": {"sha256": sha(request), "bytes": request.stat().st_size, "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/parsed; operative contract, complete issue and final604 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial display hit cp1252 after successful parse."},
        "runnerLockRole": "Live parent19008 ancestry verified; child does not reacquire/delete/unlock parent runner.lock.",
        "artifactPathPreflight": "Approved workspace inputs/committed evidence/control helpers only; no optional historical-session recipe access.",
        "actualNewPermissionDenials": []
    }
    state["stage"] = "batch-086-native-execution-in-progress"
    update(state)
    print("SAME086 starting state saved; historical root values retained.")


def verify_runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == "86e8cb13aa72ecd0"
    count = 0
    binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    for kind, group in manifest.items():
        if isinstance(group, dict):
            for name, digest in group.items():
                data = (R / name).read_bytes()
                if kind not in binary:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == digest, name
                count += 1
    assert count == 8416
    fixture = load(C / "batch-086-native-fixture-verification.json")
    archive = Path(fixture["archive"])
    assert sha(archive) == fixture["archiveSha256"]
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        root = next(n[:-len("manifest.json")] for n in names if n.endswith("/manifest.json"))
        assert z.read(root + "manifest.json") == (R / "manifest.json").read_bytes()
        for kind, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = z.read(root + name)
                    if kind not in binary:
                        data = data.replace(b"\r\n", b"\n")
                    assert hashlib.sha256(data).hexdigest() == digest, name
    return {"contentVersion": manifest["contentVersion"], "manifestSha256": sha(R / "manifest.json"),
            "runtimePayloadHashesVerified": count, "archivePayloadHashesVerified": count,
            "manifestFresh": True, "runtimeBytesUnchanged": True}


def prepare():
    state = load(C / "progress.json")
    assert state["checkpoint"] == 604 and state["stage"] == "batch-086-native-execution-in-progress"
    receipt = load(C / "batch-086-native-attempt-605-execution.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    source = C / "artifacts" / "batch-086-native-attempt-605"
    route = load(source / "n1-086-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1 and route["problems"] == 0
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"]) == (1109, 5064, 118)
    assert route["acceptedReadingParserEpoch"] == 1 and route["directWordGuardCount"] == 8
    assert route["quizOnKeys"] == ["ぼん", "はん"] and route["quizKunKeys"] == []
    assert route["bothCuratedOnKeysPersistedGoodAndDone"] and route["touchInjectedReferenceStrokes"] == 3
    rasters = load(source / "n1-086-font-raster.json")
    assert len(rasters["rows"]) == 140 and rasters["individualGlyphProbes"] == 124
    assert rasters["wholeWordRasterProbes"] == 16 and rasters["panels"] == 3
    runtime = verify_runtime()
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    assert not FOLDER.exists()
    shutil.copytree(source, FOLDER)
    sheets = C / "artifacts" / "batch-086-native-sheets-605"
    shutil.copytree(sheets, FOLDER / "sheets")
    for name in ["run-605-native.ps1", "checkpoint-native-605.py", "make-native-605-sheets.py"]:
        shutil.copyfile(C / name, FOLDER / name)
    visual = {
        "snapshot": {"nativeContentArchive": receipt["contentSnapshot"], "teaching": "f59c65fde644ed36958d74495da59a66c1d82570",
                     "coordinatorHead": HEAD, "uncommittedTeachingIncluded": False},
        "scope": "Coordinator GPT-6.1 Sol native visual inspection, not independent review: all76 screenshots through19 labelled full-frame sheets; original-size threefontpanels, meaningquestion and legend02.",
        "verdicts": {
            "nativeVisualScopedCoverage": "CLEAN",
            "nativeVisualComprehensibility": "CLEAN",
            "freshIndependentLinguisticCorrectness": "UNVERIFIED",
            "rawSourceOnlyおうよ.そModernUsage": "UNVERIFIED"
        },
        "findings": [],
        "optional": "None established within native visual scope.",
        "limits": [
            "Supplemental coordinator inspection does not replace the required two-family dependent visual confirmations.",
            "Original textual reviews and their evidence/qualifications remain unchanged; no fresh broad linguistic certification.",
            "All76 original screenshots viewed through19 half-size contact sheets; only named originals also opened at original resolution.",
            "Reading tables scroll horizontally as instructed; intentionally scrolled captures clip left columns, while other captures preserve them. Scroll viewports do not prove all content visible simultaneously.",
            "Four production-family panels show all31 Han and whole-word forms. 140 paint raster probes have JSON hashes, not separately saved images. Exact system fallback font face not identified.",
            "ReadonlyAPI35 emulator, not physical phone. Injected reference-stroke tracing and give-up recall do not certify human handwriting or MLKit.",
            "Shown/default and recordedseed604 N1 meaning alternatives adjudicated; not all possible fallback choices, arbitrary pools or learning effectiveness."
        ],
        "observations": [
            "Threefontpanels: 31 scoped Han legible across Gothic/Mincho/Textbook/Brush, no blank/replacement boxes or materially misleading forms. Exact丶/几 visible and distinct from凡/丸/九/凹; systemfallback may share appearance across families.",
            "平凡/凡例/凡そ/凡て word forms readable across families. Current-shape mnemonic dot/frame is visually consistent without asserting etymology.",
            "All native article captures inspected: new凡 and凡例 projections plus six changed reused passages/linked routes. Paragraph wrapping, kana, translations and source-only/spelling cautions readable; no actionable visual omission established.",
            "Sevenreciprocalpairs/fourteendirections and SystemBack asserted by fixture and supported by captured destinations; offline defaultnetwork none.",
            "Default N1 quiz displays concave;sunken, quasi-;associate rank, commonplace;mediocre, beast;animal. Only commonplace;mediocre fits凡; recordedbuilderN1 mosquito/pavilion alternatives also do not fit. N1 pool has one available curatedwronganswer plus twofallbacks, All uses丸/九/凹.",
            "Reading queue showsハン andボン, each accepted Correct with persistedGood and terminal2of2; curation excludes kun questions, but feedback intentionally retains full rawmetadata readings with source-only caveat in article.",
            "Three-stroke trace resembles凡; positive shape-only tracing feedback and reveal/give-up recall shown. Terminal progress asserts drawinggrade persistence; offline handwritingmodel unavailable is stated, not concealed.",
            "N1 selection shows118 cards; no owner/shared devices existed at prelaunch. Only owned23060/25336 helper launched and stopped."
        ],
        "sheetIndex": load(sheets / "index.json"),
        "independentVisualConfirmations": "pending",
        "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding"
    }
    save(FOLDER / "visual-inspection.json", visual)
    inventory = {str(p.relative_to(R)).replace("\\", "/"): sha(p) for p in sorted(FOLDER.rglob("*")) if p.is_file()}
    save(FOLDER / "artifact-hashes.json", inventory)
    evidence = {
        "schemaVersion": 1, "execution": 605, "batch": "086",
        "status": "native-passed-coordinator-visual-inspected-awaiting-dependent-confirmations",
        "contentSnapshot": receipt["contentSnapshot"], "teachingSnapshot": visual["snapshot"]["teaching"],
        "androidHead": APP, "productionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "androidQualification": "TESTONLY sibling head; unchanged production; not latest app main.",
        "startingState": state["execution605StartingState"], "nativeExecution": receipt,
        "productionImportAndRoutes": route, "runtimeVerification": runtime,
        "visualInspection": str((FOLDER / "visual-inspection.json").relative_to(R)).replace("\\", "/"),
        "archiveInventory": str((FOLDER / "artifact-hashes.json").relative_to(R)).replace("\\", "/"),
        "nativePerCaseTerminalStatus": [0, 0], "nativeSkips": 0, "nativeFailures": 0,
        "fullArchiveProductionContentSyncCalls": 1, "originalBudgetGuardsUnchanged": True,
        "textualReviewClosed": True, "independentVisualConfirmations": "pending", "runtimeAccepted": False,
        "runtimePublished": False, "runtimeChanged": False, "newIndependentReviewers": 0,
        "diagnostics": ["Initial coordinator runtime-byte checks used raw SHA for all working-tree/ZIP groups and each stopped on CRLF curriculum/grammar.json before creating evidence. Corrected both to repository-standard CRLF normalization for text groups, byte-exact binary groups, matching build_manifest/production parser and execution604. Entire ZIP itself remains byte-exact SHA verified; no runtime content changed."],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "publishedAdditions": 112, "remainingAdditions": 1116,
        "lastPublishedCommit": state["lastPublishedCommit"], "nextAction": NEXT
    }
    save(R / "docs" / "n1-sources" / "execution-605.json", evidence)
    print("Native evidence prepared:76 PNGs/19 sheets, both terminal0,8416 current+archive hashes verified.")


def finish():
    state = load(C / "progress.json")
    before = load(LOG / "progress-before-605.json")
    assert state["checkpoint"] == 604 and state["stage"] == "batch-086-native-execution-in-progress"
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "HEAD", root=A) == APP
    runtime = verify_runtime()
    for name, digest in load(FOLDER / "artifact-hashes.json").items():
        assert sha(R / name) == digest, name
        assert hashlib.sha256(subprocess.check_output(["git", "-C", str(R), "show", f"HEAD:{name}"])).hexdigest() == digest
    issue = load(C / "batch-086-native-605-issue-receipt.json")
    body = (C / "batch-086-native-605-issue-body.txt").read_text(encoding="utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    checkpoint = {
        "schemaVersion": 1, "execution": 605, "checkpoint": 605, "batch": "086",
        "savedCommit": head, "signature": "G", "status": "continue",
        "stage": "native-passed-awaiting-dependent-visual-confirmations",
        "evidence": "docs/n1-sources/execution-605.json", "dedicatedWorktreesClean": True,
        "nativeTerminalCaseStatuses": [0, 0], "nativeSkipped": 0, "nativeFailures": 0,
        "allNativeCapturesCoordinatorInspected": 76, "labelledSheets": 19,
        "all31ScopedHanFourFamiliesInspected": True, "independentVisualConfirmations": "pending",
        "runtimeVerification": runtime, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "ownedEmulator": {"serial": "emulator-5580", "parentPid": 23060, "qemuPid": 25336, "bothStopped": True},
        "textualReviewClosed": True, "newIndependentReviewers": 0,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalHelpersAccessed": False,
        "publishedAdditions": 112, "remainingAdditions": 1116, "lastPublishedCommit": state["lastPublishedCommit"],
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(C / "batch-086-native-605-issue-receipt.json"),
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "verifiedAt": datetime.now(timezone.utc).isoformat(), "nextAction": NEXT
    }
    state["execution605StartingState"]["status"] = "signed-local-native-checkpoint-complete"
    state["execution605CoordinatorCheckpoint"] = checkpoint
    state["batch086NativeExecutionCheckpoint"] = checkpoint
    state.update(checkpoint=605, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for k, v in before.items():
        if k not in allowed:
            assert state[k] == v, k
    update(state)
    saved = load(C / "progress.json")
    assert saved == state
    save(LOG / "final-verification-605.json", checkpoint)
    print(json.dumps({k: checkpoint[k] for k in ["checkpoint", "savedCommit", "stage", "issueUpdate", "originalRootKeysCompared"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "finish": finish}[sys.argv[1]]()
