import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
LOG = C / "logs" / "6a3968b7-ab7d-4ae3-94b2-658691ab2f77"
HEAD = "3b1f6ccb93834bb69ba53bce0c81f4d8079980a7"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
ATTEMPT = C / "artifacts" / "batch-083-corrected-native-attempt-578"
FOLDER = R / "docs" / "n1-reviews" / "batch-083-native-corrected" / "attempt-578"
BEFORE = LOG / "progress-before-578.json"
EVIDENCE = R / "docs" / "n1-sources" / "execution-578.json"
NEXT = (
    "SAME083 original-family dependent VISUAL confirmations NEXT, then persist/yield; "
    "no publication/084. Signed corrected native578 evidence in docs/n1-sources/execution-578.json "
    "and batch-083-native-corrected/attempt-578: BOTH corrected named cases terminal0/no skips/"
    "no-2/-3, productionContentSyncONCE1095kanji5052words115N1/version6dfe6a1e287ce5df/"
    "zeroProblems/acceptedepoch1; exact default4 productionQuizBuilder N1 AND All "
    "IDs+titles凌/准/冶/冴 all3curatedavailable/no padding, actualN1UI meaning/feedback; "
    "Full/Lite full+curatedリョウ/しの.ぐ and independently persisted soleりょう/しのぐ; "
    "threearticles/tworeciprocalpairs/fourdirections/SystemBack/offline/selection/"
    "teninjectedstroketrace/recall/persistence passed. Updated30Han incl冴,120individual+"
    "8wholeword/fourfonts/Paint/directComposePNG. Coordinator directly inspected19of56PNGs "
    "including all3fontpanels and changedmeaning/readings/drawing/threearticleframes/Back; "
    "not all56 nor independent confirmation. Reuse original ClaudeOpus5.5 session"
    "ce6f8ba4-518e-42b8-b0ee-bd14d3b291e9 then GPT6.1Sol session"
    "574ee3ae-411e-4a83-b00f-89b69ac61d99 serially on same signed unchanged snapshot/"
    "boundedpacket with ownoriginalfindings/exactdiff/nativeprovenance/actualPNGreads; "
    "actualmodel/readdepth/tool/process-exit evidence; no new blindinitial review absent concern. "
    "FreshHOST4/compile577 and corrected578native need no repeat absent change/newconcern. "
    "Original573/574failedattempt/fixtures/APKs/archive/reports immutable. "
    "083-NATIVE-574-CHOICE textual+boundedruntime resolved; independent visual/batch acceptance "
    "still outstanding. 冴える skill/excel-at secondary sense retained, actualclear;sharp-minded "
    "label assessed, no universal synonym-disjointness/random/custom/padded/partial/larger/"
    "reversepool or AllUI safety claim. Injectedreference+giveup NOT humanrecognition/MLKit/"
    "phone; offline handwritingmodel unavailable shown honestly. API35readonlyhostGPU/-Vulkan/"
    "2048MiB2cores/serial5580 parent20588qemu27704 owned-only stopped, parent19008runner.lock "
    "untouched. No native rerun now; any future need requires fresh localANDremote5580/5581 "
    "includingTimeWait/devices/PIDs/liveparentancestry before launch/noalternateport/"
    "shareddeviceinterference/unchangedheapsguards. After serialVISUAL confirmations require "
    "latest-main normalmerge/combinedPython/validator/vocabulary/manifest/exact17guards/"
    "baseline/link/membership/originalbudgets/normal signedownerfastforward/exactremote/"
    "terminalgreenCI/EVERYimmutableZIPhash/verifiedownerissue60 BEFORE084. Approvedcontrolhelpers/"
    "committedsources only/nooptionalhistoricalsessionhelpers. Preserve/report/yield actual"
    "newdenial/signinghang; all inherited source/reviewer/process/lookup/readdepth/viewport/"
    "fallback/MLKit/OOM/denial limitations retained. Published109/1228,remaining1119/"
    "latestpublic21a5cb1328aadd437139a6b850f07298a2e2985d unchanged;083notdelivered. "
    "Physicalphone/generalrelease/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "log", "-1", "--format=%G?") == "G"
    assert not git(root, "status", "--porcelain")


def update(p):
    tmp = C / "progress.578.tmp"
    assert not tmp.exists()
    save(tmp, p)
    assert load(tmp) == p
    tmp.replace(C / "progress.json")


def inputs():
    e = load(R / "docs" / "n1-sources" / "execution-577.json")
    f = e["fixtureVerification"]
    for key in ("testApk", "appApk"):
        assert sha(Path(e[key]["path"])) == e[key]["sha256"]
    for key in ("fixture", "archive"):
        assert sha(Path(f[key])) == f[key + "Sha256"]
    assert not git(A, "diff", e["productionBaseline"], APP, "--",
                   "app/src/main", "core/src/main", "gradle.properties")
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == "6dfe6a1e287ce5df"
    with zipfile.ZipFile(f["archive"]) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) == 8398
        prefix = names[0].split("/")[0] + "/"
        assert json.loads(archive.read(prefix + "manifest.json")) == manifest
        verified = 0
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, expected in entries.items():
                data = archive.read(prefix + name)
                if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == expected, name
                verified += 1
        assert verified == 8376
    with zipfile.ZipFile(e["testApk"]["path"]) as archive:
        assert hashlib.sha256(archive.read("assets/" + Path(f["archive"]).name)).hexdigest() == f["archiveSha256"]
    return e


def start():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 577 and p["status"] == "continue" and p["batch"] == "083"
    clean(R, HEAD)
    clean(A, APP)
    inputs()
    request = LOG / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 577
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    state = {
        "execution": 578, "batch": "083", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "scope": "SAME083 corrected frozen native execution and direct PNG inspection, signed LOCAL evidence checkpoint; no reviewer/integration/publication/084.",
        "request": {"sha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint parsed; operative contract, complete approved issue and final577 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 verified in coordinator ancestry; no child lock open/acquire/delete/unlock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    p["execution578StartingState"] = state
    p["stage"] = "batch-083-corrected-native-execution-in-progress"
    p["nextAction"] = state["scope"]
    update(p)
    save(C / "execution-578-start.json", state)
    print("Starting scope persisted; complete history and 8376 archive hashes preserved.")


def record():
    clean(R, HEAD)
    clean(A, APP)
    prior = inputs()
    receipt = load(ATTEMPT / "execution.json")
    assert receipt == load(C / "batch-083-corrected-native-attempt-578-execution.json")
    assert receipt["nativeExecuted"] and receipt["passed"] and receipt["failure"] is None
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert not any(receipt[k] for k in ("parentLockTouched", "guestOrAppHeapChanged", "guardsChanged", "hostHeapInitUsed"))
    assert receipt["prelaunch"]["connections"] == [] and receipt["preexistingEmulators"] == []
    raw = (ATTEMPT / "instrumentation.txt").read_text(encoding="utf-8-sig")
    cases = []
    fields = {}
    for line in raw.splitlines():
        if line.startswith("INSTRUMENTATION_STATUS: "):
            name, value = line.removeprefix("INSTRUMENTATION_STATUS: ").split("=", 1)
            fields[name] = value
        elif line.startswith("INSTRUMENTATION_STATUS_CODE: "):
            code = int(line.split(": ", 1)[1])
            if code != 1:
                cases.append({"class": fields["class"], "test": fields["test"], "status": code})
            fields = {}
    assert cases == [
        {"class": "io.github.stopcran.kanji.ui.N1Batch083CorrectedGlyphTest",
         "test": "enduranceLookalikesAndRadicalFallbacksAcrossFourProductionFamilies", "status": 0},
        {"class": "io.github.stopcran.kanji.ui.N1Batch083CorrectedArticleTest",
         "test": "fullSingleImportOfflineEnduranceTwoReciprocalPairsCuratedOnAndKunDrawingAndSystemBack", "status": 0},
    ]
    assert "OK (2 tests)" in raw and receipt["adbExitCode"] == 0
    route = load(ATTEMPT / "n1-083-corrected-article-route.json")
    for key, value in {
        "archiveRequests": 1, "importedKanji": 1095, "importedWords": 5052, "n1Cards": 115,
        "problems": 0, "acceptedReadingParserEpoch": 1, "contentVersion": "6dfe6a1e287ce5df",
        "reciprocalLinkAndSystemBack": True, "mappedReciprocalPairs": 2, "directedLinkTransitions": 4,
        "completeArticleProjections": 3, "passed": True, "offline": True,
        "exactCuratedChoicesWithoutFallback": True, "meaningQuestionAndFeedback": True,
        "bothCuratedKindsPersistedGoodAndDone": True, "touchInjectedReferenceStrokes": 10,
        "drawingTraceThenRecall": True, "drawingGradeRecordedOnNext": True,
    }.items():
        assert route[key] == value, key
    for key in ("fullOnyomi", "liteQuizOnyomi", "fullProjectionOnyomi", "fullProjectionQuizOnyomi"):
        assert route[key] == ["リョウ"]
    for key in ("fullKunyomi", "liteQuizKunyomi", "fullProjectionKunyomi", "fullProjectionQuizKunyomi"):
        assert route[key] == ["しの.ぐ"]
    assert route["quizOnKeys"] == ["りょう"] and route["quizKunKeys"] == ["しのぐ"]
    expected = {"凌": "endure; surpass", "准": "quasi-; associate rank",
                "冶": "smelt; work metals", "冴": "clear; sharp-minded"}
    for name, count in (("N1", 115), ("All", 1095)):
        pool = route["productionBuilderN1AndAllExactChoices"][name]
        assert pool["poolSize"] == count and pool["allThreeCuratedAvailable"] and pool["defaultFourNoPadding"]
        assert len(pool["options"]) == 4
        assert {o["kanji"]: o["title"] for o in pool["options"]} == expected
    assert len(route["exactDefaultMeaningOptions"]) == 4
    assert {o["kanji"]: o["title"] for o in route["exactDefaultMeaningOptions"]} == expected
    raster = load(ATTEMPT / "n1-083-corrected-font-raster.json")
    glyphs = [r for r in raster["rows"] if "character" in r]
    words = [r for r in raster["rows"] if "word" in r]
    assert len(glyphs) == 120 and len(words) == 8
    assert {r["character"] for r in glyphs} == set(prior["fixtureVerification"]["plannedGlyphs"])
    assert all(r["hasGlyph"] for r in glyphs)
    assert all(r["renderedCharactersNonblank"] == len(r["word"]) for r in words)
    for font in {r["font"] for r in glyphs}:
        assert len({r["nativePaintRasterSha256"] for r in glyphs if r["font"] == font}) == 30
    steps = [
        "font-panel-1", "font-panel-2", "font-panel-3", "meaning-question", "meaning-feedback",
        "curated-On-question", "curated-On-feedback", "curated-Kun-question", "curated-Kun-feedback",
        "curated-on-kun-done", "drawing-trace", "drawing-feedback", "drawing-recall-feedback",
        "selection", "kanji-21", "endure-word-05", "surpass-word-12",
        "endure-word-system-back-to-kanji", "surpass-word-system-back-to-word",
    ]
    inspected = ["n1-083-corrected-" + step + ".png" for step in steps]
    assert len(list(ATTEMPT.glob("*.png"))) == 56 and len(inspected) == 19
    assert all((ATTEMPT / name).exists() for name in inspected)
    assert not FOLDER.exists() and not EVIDENCE.exists()
    FOLDER.mkdir(parents=True)
    artifacts = []
    for source in sorted(ATTEMPT.iterdir()):
        assert source.is_file()
        compressed = source.suffix == ".txt" and source.stat().st_size > 20000
        target = FOLDER / (source.name + ".gz" if compressed else source.name)
        if compressed:
            target.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(target.read_bytes()) == source.read_bytes()
        else:
            shutil.copyfile(source, target)
        artifacts.append({"sourceName": source.name, "archive": target.relative_to(R).as_posix(),
                          "sha256": sha(target), "sourceSha256": sha(source),
                          "bytes": target.stat().st_size, "losslessGzipVerified": compressed})
    provenance_folder = FOLDER / "provenance"
    provenance_folder.mkdir()
    provenance = []
    for source in (Path(__file__), C / "run-578-native.ps1",
                   C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt"):
        target = provenance_folder / source.name
        shutil.copyfile(source, target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    save(FOLDER / "artifact-index.json", artifacts)
    inspection = {
        "reviewer": "Coordinator GPT-6.1 Sol (gpt-6.1-sol)", "independentReviewer": False,
        "files": inspected, "savedPngCount": 56, "directlyInspectedPngCount": 19,
        "notDirectlyInspectedPngCount": 37,
        "observation": "All 30 Han and both whole words visibly nonblank across four production families in three panels. 凌/陵/准/冶/冴/次 and 冫/夌/阝/隹 distinguishable at captured size; fallback forms may coincide across families. Exact four meaning labels visible with endure;surpass correct. Onリョウ and kunしのぐ questions/feedback and 2-of-2 completion legible. Ten-stroke drawing/reference feedback and giveup recall visible. Three sampled article frames and two Back frames show readable text and component/spelling guidance.",
        "limits": "Only 19 listed PNGs directly inspected, not all56 or independent two-family visual confirmation. Captured viewport is not whole-article simultaneous visibility or physical-phone/native-speaker/fallback-face identity certification. Drawing screenshot explicitly says handwriting model unavailable; injected reference tracing and giveup are not human recognition or MLKit acceptance.",
    }
    native = {
        "execution": 578, "status": "corrected-native-passed-awaiting-original-family-visual-confirmation",
        "contentSnapshot": prior["contentSnapshot"], "teachingSnapshot": prior["teachingSnapshot"],
        "contentVersion": route["contentVersion"], "androidHead": APP,
        "nativeReceipt": receipt, "independentlyParsedTerminalCases": cases,
        "nativeAcceptancePassed": True, "passedCases": 2, "failedCases": 0, "skippedCases": 0,
        "route": route, "glyphProbes": {"individual": 120, "wholeWord": 8, "fonts": 4, "distinctHan": 30,
                                       "allIndividualHasGlyph": True, "distinctIndividualRasterHashesWithinEachFont": True},
        "directPngInspection": inspection, "artifactIndex": (FOLDER / "artifact-index.json").relative_to(R).as_posix(),
        "artifactIndexSha256": sha(FOLDER / "artifact-index.json"),
        "choiceFinding": {"id": "083-NATIVE-574-CHOICE", "status": "resolved",
                          "textualDisposition": "resolved in576", "boundedRuntimeDisposition": "resolved in578",
                          "evidence": "Exact default-four ID/title sets now passed in production QuizBuilder on full imported N1 and All, and actual N1 UI question/feedback. Original574 failure remains immutable.",
                          "limits": "Independent visual confirmation and combined-tree publication acceptance remain. No All UI/custom/random/padded/partial/larger/reverse-pool safety claim."},
        "independentVisualConfirmation": "outstanding", "runtimeAccepted": False, "runtimePublished": False,
    }
    reconciliation_path = R / "docs" / "n1-reviews" / "batch-083-reconciliation.json"
    reconciliation = load(reconciliation_path)
    assert reconciliation["textualReviewClosed"] and not reconciliation["runtimeAccepted"]
    assert "correctedNativeAcceptance" not in reconciliation
    reconciliation["status"] = native["status"]
    reconciliation["correctedNativeAcceptance"] = native
    save(reconciliation_path, reconciliation)
    evidence = {
        "schemaVersion": 1, "execution": 578, "batch": "083", "status": native["status"],
        "startingState": load(C / "execution-578-start.json"),
        "contentSnapshot": prior["contentSnapshot"], "teachingSnapshot": prior["teachingSnapshot"],
        "coordinatorHead": HEAD, "androidHead": APP, "productionBaseline": prior["productionBaseline"],
        "nativeAcceptance": native, "provenance": provenance,
        "runtimeManifestHashesVerified": 8376, "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "hostChecksRerun": False, "independentReviewersLaunched": 0,
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": "21a5cb1328aadd437139a6b850f07298a2e2985d",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "inheritedNextGate577PreservedVerbatim": prior["nextGate"],
        "limits": "Bounded emulator native pass, not batch publication acceptance or independent visual confirmation. No teaching/production changes. Original573/574/575/576/577 sources/fixtures/APKs/archive/reports, reviewer/lookup/read-depth/process/OOM/denial/viewport/fallback/MLKit/phone/publication limitations retained. No HOST or compile rerun absent new concern.",
        "nextGate": NEXT,
    }
    save(EVIDENCE, evidence)
    print("Both named terminal0 cases and exact corrected choices archived; 19/56 PNGs inspected.")


def finish():
    clean(A, APP)
    assert git(R, "log", "-1", "--format=%G?") == "G"
    assert not git(R, "status", "--porcelain")
    assert not git(R, "diff", HEAD, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    inputs()
    evidence = load(EVIDENCE)
    assert evidence["nativeAcceptance"]["nativeAcceptancePassed"]
    p = load(C / "progress.json")
    before = load(BEFORE)
    assert p["checkpoint"] == 577 and p["batch"] == "083"
    for key, value in before.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert p[key] == value, key
    summary = {
        "schemaVersion": 1, "execution": 578, "checkpoint": 578, "batch": "083",
        "savedCommit": git(R, "rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": "corrected-native-passed-awaiting-original-family-visual-confirmation",
        "evidence": EVIDENCE.relative_to(R).as_posix(), "contentSnapshot": evidence["contentSnapshot"],
        "contentVersion": "6dfe6a1e287ce5df", "androidHead": APP,
        "nativeExecuted": True, "nativeAcceptancePassed": True,
        "nativeTerminalCases": evidence["nativeAcceptance"]["independentlyParsedTerminalCases"],
        "directPngInspection": evidence["nativeAcceptance"]["directPngInspection"],
        "choiceFinding": evidence["nativeAcceptance"]["choiceFinding"],
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "hostChecksRerun": False, "independentReviewersLaunched": 0,
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "ownedEmulatorStopped": True, "parentLockTouched": False, "dedicatedWorktreesClean": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    for key in ("checkpoint", "status", "stage", "nextAction"):
        p[key] = summary[key]
    p["blocker"] = None
    p["execution578CoordinatorCheckpoint"] = summary
    p["batch083CorrectedNativeCheckpoint"] = summary
    update(p)
    save(C / "execution-578-checkpoint.json", summary)
    print("Checkpoint578 continue: same083 original-family visual confirmations next; worktrees clean.")


if __name__ == "__main__":
    {"start": start, "record": record, "finish": finish}[sys.argv[1]]()
