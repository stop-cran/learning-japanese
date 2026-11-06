from pathlib import Path
import datetime
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys

C = Path(__file__).parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
HEAD = "8a4a70e70d51487ae0c58979e8166b2186a6ee91"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
ATTEMPT = C / "artifacts" / "batch-084-native-retry1-attempt-587"
DEST = R / "docs" / "n1-reviews" / "batch-084-native-retry1" / "attempt-587"
LOG = C / "logs" / "beea3b0e-c8ab-47ae-b801-f7e33fa093ae"
NEXT = (
    "SAME084 serial ORIGINAL-family dependent VISUAL confirmations NEXT, then persist/yield before integration/publication or085. "
    "Read docs/n1-sources/execution-587.json and docs/n1-reviews/batch-084-native-retry1/attempt-587 "
    "(all42 original PNGs, seven labelled contact sheets, raw terminal results, route/raster JSON, coordinator visual report). "
    "Reuse ClaudeOpus5.5 session45e7798c-3f2b-45f4-85ce-5f00db7cc847 then GPT6.1Sol "
    "sessionaa972b37-2d13-4edc-8636-f2896ef9c3ad sequentially, same frozen unchanged teaching030b144a/"
    "runtime53b6819b/version74b87b47347b78c1, ownoriginalfindings/exactdiff/nativeprovenance/boundedPNGpacket; "
    "actual models/read-depth/tool results/process exits required, at most one reviewer and no snapshot edits. "
    "No new blind initial review or native rerun absent changed passage/new concern. Both Retry1 native named cases "
    "terminal0/no skips passed587: full git envelope via productionContentSyncONCE1096kanji5053words116N1/"
    "zeroProblems/epoch1; Full/Lite full sourceリン/きびし.い retained, curatedリン/kun[], soleりん persisted good/done; "
    "exact ordinary default4 N1 AND All productionbuilder凜/准/冗/凹 actuallabels/no padding, actualN1meaningUI; "
    "onepair/twodirections/twocompletearticles/SystemBack/offline/selection/15injectedreference strokes/"
    "trace/recall/persistence. 28Han/112individual+8wholeword/fourfonts/threeComposepanels legible in "
    "coordinator PNG inspection; all42 viewed in scaled full-frame contact sheets plus seven originals "
    "at full resolution, not42fullresolution reads nor independentvisualclosure. Fallbackface not identified. "
    "Injectedreference/giveup and offlineMLKit unavailable NOT humanrecognition/physicalphone. "
    "OwnedAPI35readonlyhostGPU/-Vulkan/2048MiB2cores/serial5580 parent26288qemu10468 stoppedonlyownedhelper; "
    "parent19008runner.lock never acquired/deleted/unlocked, initialread sharingviolation preserved as role diagnostic. "
    "Any justified future native retry needs fresh localANDremote5580/5581 includingTimeWait/device/PIDs/"
    "liveparentancestry/checkpoint/signedheads/whollycleanworktrees; no alternateport without routing authorization/"
    "shareddeviceinterference/heapguard increases. FreshHOST4passed585/compile586 need no repetition absent change. "
    "Original586fixture/APK/selector correction and all historical reports remain immutable. "
    "C1optional/C2withdrawn/C3defaultresolved-largerpoolunverified preserved. Later fresh latest-main "
    "normalmerge/surgicalreconciliation/substantiveteachingreview/combinedPython-validator-vocabulary-manifest/"
    "membership-baseline-link-original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepaths/"
    "normalsigning/ownerfastforward/terminalCI/EVERYimmutablepublicZIPhash/verifiedownerissue60 required BEFORE085. "
    "Approvedcontrol/committed sources only, no optional historical-session recipes; preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. Published110/1228,1118remaining/latestpublished73b19c3e unchanged; "
    "084 not published or finally accepted. Physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)

def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), "--no-pager", *args], text=True).strip()

def clean(root, head):
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "log", "-1", "--format=%G?") == "G"
    assert not git(root, "status", "--porcelain")

def record():
    clean(R, HEAD)
    clean(A, APP)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 586 and p["stage"] == "batch-084-native-execution-in-progress"
    save(LOG / "progress-before-587-final.json", p)
    receipt = load(ATTEMPT / "execution.json")
    assert receipt == load(C / "batch-084-native-retry1-attempt-587-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert not any(receipt[key] for key in ("parentLockTouched", "guestOrAppHeapChanged", "guardsChanged"))
    assert receipt["prelaunch"]["connections"] == []
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
    assert [case["class"] for case in cases] == [
        "io.github.stopcran.kanji.ui.N1Batch084Retry1GlyphTest",
        "io.github.stopcran.kanji.ui.N1Batch084Retry1ArticleTest"]
    assert all(case["status"] == 0 for case in cases) and "OK (2 tests)" in raw
    route = load(ATTEMPT / "n1-084-article-route.json")
    for key, value in {
        "contentVersion": "74b87b47347b78c1", "archiveRequests": 1, "importedKanji": 1096,
        "importedWords": 5053, "problems": 0, "n1Cards": 116, "acceptedReadingParserEpoch": 1,
        "fullOnyomi": ["リン"], "fullKunyomi": ["きびし.い"], "quizOnKeys": ["りん"], "quizKunKeys": [],
        "mappedReciprocalPairs": 1, "directedLinkTransitions": 2, "completeArticleProjections": 2,
        "soleCuratedOnPersistedGoodAndDone": True, "touchInjectedReferenceStrokes": 15,
        "drawingTraceThenRecall": True, "drawingGradeRecordedOnNext": True, "offline": True,
    }.items():
        assert route[key] == value, key
    for scope in ("N1", "All"):
        choices = route["productionBuilderN1AndAllExactChoices"][scope]
        assert choices["allThreeCuratedAvailable"] and choices["defaultFourNoPadding"]
        assert {entry["kanji"]: entry["title"] for entry in choices["options"]} == {
            "凜": "dignified; bracing cold", "准": "quasi-; associate rank",
            "冗": "superfluous; redundant", "凹": "concave; sunken"}
    raster = load(ATTEMPT / "n1-084-font-raster.json")
    assert (raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (112, 8, 3)
    assert len(raster["rows"]) == 120
    assert len(list(ATTEMPT.glob("*.png"))) == 42
    DEST.mkdir(exist_ok=False)
    index = []
    for path in sorted(ATTEMPT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ATTEMPT)
        destination = DEST / relative
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
    for name in ("execution-587-preflight.py", "run-587-native.ps1", "execution-587-contact-sheets.py",
                 "execution-587-record.py", "execution-587-visual-inspection.txt", "execution-587-start.json"):
        source = C / name
        destination = DEST / name
        shutil.copyfile(source, destination)
        provenance.append({"source": str(source), "archive": destination.relative_to(R).as_posix(), "sha256": sha(source)})
    index_path = DEST / "artifact-index.json"
    save(index_path, index)
    native = {
        "execution": 587, "status": "native-passed-awaiting-original-family-visual-confirmation",
        "nativeAcceptancePassed": True, "independentVisualConfirmation": "outstanding",
        "runtimeAccepted": False, "runtimePublished": False,
        "caseResults": cases, "nativeSkips": 0, "route": route, "executionReceipt": receipt,
        "glyphProbeCounts": {"actualHan": 28, "individual": 112, "wholeWord": 8, "fontFamilies": 4, "panels": 3},
        "artifactIndex": index_path.relative_to(R).as_posix(), "artifactIndexSha256": sha(index_path),
        "originalPngCount": 42, "contactSheetCount": 7,
        "coordinatorVisualReport": (DEST / "execution-587-visual-inspection.txt").relative_to(R).as_posix(),
        "coordinatorInspection": "All42 at labelled scaled full-frame sheets; seven originals at full resolution, including allthree fontpanels. Not42 full-resolution reads or independent closure.",
        "phoneEvidence": False, "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "limits": [
            "Injected reference strokes and recall give-up are not human handwriting/MLKit recognition.",
            "Offline handwriting model unavailable; shape-only tracing exercised honestly.",
            "Exact default four choices covered for N1 and All production builder; All UI and larger/custom/random/padded/partial pools not tested.",
            "Fallback-face identity not established by readability or raster hashes.",
            "Full source-only kun retained in reference/feedback metadata, not offered as a reading question.",
            "Initial preflight counted only manifest files, failed before changes; corrected to all canonical manifest sections and then verified8379 hashes.",
            "Initial runner.lock read sharing violation preserved; parent role/ancestry verified and no lock mutation/acquisition.",
        ],
        "nextAction": NEXT,
    }
    evidence = {
        "schemaVersion": 1, "execution": 587, "batch": "084",
        "startingState": p["execution587StartingState"], "contentSnapshot": "53b6819b22787a2517cd0ad14aa855d357cbc70a",
        "teachingSnapshot": "030b144a6aeefc6fe77f76683219832db91bef4f", "androidHead": APP,
        "productionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "nativeAcceptance": native, "provenance": provenance,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "publishedAdditions": 110, "remainingAdditions": 1118, "lastPublishedCommit": p["lastPublishedCommit"],
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    }
    save(R / "docs" / "n1-sources" / "execution-587.json", evidence)
    reconciliation_path = R / "docs" / "n1-reviews" / "batch-084-reconciliation.json"
    original = reconciliation_path.read_text(encoding="utf-8")
    reconciliation = json.loads(original)
    original = original.replace(
        '"status": "' + reconciliation["status"] + '"',
        '"status": "' + native["status"] + '"', 1)
    addition = json.dumps({"nativeAcceptance587": native}, ensure_ascii=True, indent=2)[2:-2]
    reconciliation_path.write_text(original.rstrip()[:-1].rstrip() + ",\n" + addition + "\n}\n", encoding="utf-8")
    print("Native receipts, all42 PNGs, seven sheets and qualified visual report archived; runtime unchanged.")

def checkpoint():
    p = load(C / "progress.json")
    before = load(LOG / "progress-before-587-final.json")
    assert p == before
    saved = git(R, "rev-parse", "HEAD")
    clean(R, saved)
    clean(A, APP)
    assert not git(R, "diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git(R, "log", "-1", "--format=%G?") == "G"
    summary = {
        "schemaVersion": 1, "execution": 587, "checkpoint": 587, "batch": "084", "status": "continue",
        "stage": "native-passed-awaiting-original-family-visual-confirmation", "savedCommit": saved, "signature": "G",
        "evidence": "docs/n1-sources/execution-587.json", "androidHead": APP, "nativePassedCases": 2, "nativeSkips": 0,
        "originalPngCount": 42, "coordinatorPngInspection": "all42 contact-sheet frames plus seven full-resolution originals",
        "independentVisualConfirmation": "outstanding", "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": p["lastPublishedCommit"], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "dedicatedWorktreesClean": True, "allOriginalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before), "nextAction": NEXT,
    }
    p.update({"checkpoint": 587, "status": "continue", "stage": summary["stage"], "nextAction": NEXT, "blocker": None})
    p["execution587CoordinatorCheckpoint"] = summary
    p["batch084NativeCheckpoint"] = summary
    for key, value in before.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert p[key] == value, key
    temporary = C / "progress.587.tmp"
    assert not temporary.exists()
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")
    save(LOG / "checkpoint-587.json", summary)
    body = (
        f"Batch084 SAME checkpoint587: fresh frozen Retry1 native acceptance passed, preserved at signed LOCAL `{saved}` "
        "(not published content). Both named instrumentation cases ended status0, no skips. Full git envelope imported "
        "ONCE through production ContentSync:1096kanji/5053words/116N1, zero problems, version74b87b47347b78c1, accepted parser epoch1. "
        "Exact default N1/All four meaning choices, sole curated onりん/kun[], complete reciprocal articles/SystemBack/offline/"
        "selection/15-reference-stroke trace/recall/persistence passed. All28 scoped Han/fourfamilies/112individual+8wholeword "
        "rasters/threeComposepanels inspected: all42 preserved PNGs in full-frame scaled sheets plus seven originals at full resolution; "
        "no blank/replacement/materially misleading glyph observed. Fallback font identity not claimed. "
        "Owned readonly API35 emulator5580 parent26288/qemu10468 stopped; no shareddevice, heap/guard or parent-lock changes. "
        "Touch-injected tracing/recall give-up is NOT human handwriting/MLKit/phone acceptance; offline model unavailable. "
        "Evidence:docs/n1-sources/execution-587.json and docs/n1-reviews/batch-084-native-retry1/attempt-587. "
        "Next:serial original-family dependent visual confirmation, then checkpoint before combined-main integration/publication. "
        "Original textual findings and larger/custom/random/padded/partial option-pool limits retained. "
        "Published110/1228,1118remaining unchanged;084 not delivered. Physicalphone/generalrelease/whole-set outstanding; no085."
    )
    (C / "execution-587-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps({"checkpoint": 587, "signedCommit": saved, "status": "continue"}))

def repair_reconciliation():
    path = R / "docs" / "n1-reviews" / "batch-084-reconciliation.json"
    original = subprocess.check_output(
        ["git", "-C", str(R), "show", HEAD + ":docs/n1-reviews/batch-084-reconciliation.json"]
    ).decode("utf-8").replace("\r\n", "\n")
    evidence_path = R / "docs" / "n1-sources" / "execution-587.json"
    evidence = load(evidence_path)
    native = evidence["nativeAcceptance"]
    old = json.loads(original)
    original = original.replace('"status": "' + old["status"] + '"', '"status": "' + native["status"] + '"', 1)
    addition = json.dumps({"nativeAcceptance587": native}, ensure_ascii=True, indent=2)[2:-2]
    path.write_text(original.rstrip()[:-1].rstrip() + ",\n" + addition + "\n}\n", encoding="utf-8")
    current = load(path)
    assert all(current[key] == value for key, value in old.items() if key != "status")
    source = C / "execution-587-record.py"
    destination = DEST / source.name
    shutil.copyfile(source, destination)
    for entry in evidence["provenance"]:
        if entry["source"] == str(source):
            entry["sha256"] = sha(source)
    evidence["serializationDiagnostic"] = "Preserved original reconciliation bytes/values except status plus added native key; initial generated serialization escaped existing Unicode, corrected before commit."
    save(evidence_path, evidence)
    print("Original reconciliation formatting/history preserved; added native evidence only.")

if __name__ == "__main__":
    {"record": record, "checkpoint": checkpoint, "repair-reconciliation": repair_reconciliation}[sys.argv[1]]()
