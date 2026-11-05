import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).parent
ROOT = CONTROL.parent / "learning-japanese"
LOG = CONTROL / r"logs\e636affe-bea9-4c9b-a92c-a27fe3fa479c"
HEAD = "3618d604582809ed25b0414fccf7c4e8b2e4dd0d"
FOLDER = ROOT / r"docs\n1-reviews\batch-072-native"
RECORD = ROOT / r"docs\n1-sources\execution-477.json"
DIRECT = """font-pairs kanji-01 kanji-03 kanji-09 kanji-11 kanji-20
word-new-02 word-new-07 word-new-09 word-reused-06
word-new-system-back-word-kanji word-new-system-back-kanji-word word-reused-kanji-backlink
selection meaning-question meaning-feedback curated-On-question curated-On-feedback
curated-Kun-question curated-Kun-feedback curated-both-done
drawing-trace drawing-feedback drawing-recall-feedback""".split()
NEXT = (
    "SAME072: native477 BOTH named cases terminal0/no skips in100.843s; read docs\\n1-sources\\execution-477.json "
    "and batch-072-native\\execution-477-artifact-index.json. Full signed92f3c2ef Git envelope via production "
    "ContentSync ONCE:1084kanji5042words104N1/version900e3a2130afc56b/problems0/epoch1. Full+Lite rawジュウ "
    "andあ.てる/み.たす retained; curatedジュウ/あ.てる, normalizedじゅう/あてる; BOTH Good logs/Done2correct/"
    "noみたす question or log. Complete new充/充てる projections, exact reused拡充 component paragraph, "
    "all3reading labels/explanations,2reciprocalpairs/4directions/SystemBack/offline/N1selection/meaning/"
    "sixreference-touchstrokes/ungradedtrace/recallAgain pass. 204singlePaint+8wordRaster probes cover51Han "
    "including isolated亠/儿/厶 across4productionfamilies. 44originalPNGs/24unique byte streams directly "
    "coordinator-inspected;20duplicates hash-mapped, not fresh visual reads. Left/right table screenshots "
    "jointly retain labels/examples; right-offset first-column clipping with explicit scroll hint is inherited. "
    "Owned12224/QEMU9228 stopped; preexisting5556 unchanged; sharedADB9520 reconnect/OS TIME_WAIT not listeners. "
    "NEXT original Claude0e0fbc27-0aba-4217-94a6-74ad8bb21070 THEN GPTe304bb20-e8fe-4113-b7cb-fb09097cf343 "
    "SERIAL dependent visual confirmations on bounded PNG/route/fixture/source packets; record actual coverage, "
    "not new blind initial reviews. Do not rerun passing native or475HOST3+1 absent new concern. "
    "No host heap init/native heap/guard changes; raster hashes do not identify fallback face; injected trace "
    "not human handwriting/MLKit. Then freshmain nonrewriting integration/allcombinedvalidation/normalsigning/"
    "ownerfastforward/publicSHA/greenCI/everyimmutablepublicZIPruntimehash/originalbudgets/ownerissue60 BEFORE "
    "delivery or073. No secondrunner/supervisor edits/signingretry/permissionworkaround. Published98/1228,"
    "remaining1130;99published supports NOTN1vocabulary. CompatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set acceptance outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == data


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


if sys.argv[1] == "start":
    request = LOG / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    checkpoint = json.loads(text.split(marker, 1)[1])
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == checkpoint["checkpoint"] == 476
    assert progress["status"] == "continue" and progress["batch"] == "072"
    before = LOG / "execution-477-before-progress.json"
    assert not before.exists()
    shutil.copyfile(CONTROL / "progress.json", before)
    state = {
        "execution": 477, "batch": "072", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME072 compiled exact-full-archive native execution and coordinator visual inspection only; no reviewer/publication/073/second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and embedded checkpoint parsed; operative contract, complete approved issue and final476 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "status": "native-execution-starting",
    }
    progress["execution477StartingState"] = state
    progress["stage"] = "batch-072-native-executing"
    save(LOG / "execution-477-start.json", state)
    save(CONTROL / "progress.json", progress)
    source = (CONTROL / "run-469-native.ps1").read_text(encoding="utf-8-sig")
    replacements = {
        "071": "072",
        "469": "477",
        "execution-468.json": "execution-476.json",
        "9c0614c566d8051a85423ff05e477da6c57b293f": HEAD,
        "57d9bb43-0896-4d4b-ba85-096c439d6e4c": "e636affe-bea9-4c9b-a92c-a27fe3fa479c",
    }
    for old, new in replacements.items():
        assert old in source, old
        source = source.replace(old, new)
    runner = CONTROL / "run-477-native.ps1"
    assert not runner.exists()
    runner.write_text(source, encoding="utf-8")
    assert "071" not in source and "469" not in source and "execution-476.json" in source
    print(json.dumps(state, ensure_ascii=False, indent=2))

elif sys.argv[1] == "archive":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    receipt = load(CONTROL / "batch-072-native-attempt-1-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert receipt["prelaunch"]["connections"] == []
    assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
    source = CONTROL / r"artifacts\batch-072-native-attempt-1"
    raw = (source / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "OK (2 tests)" in raw and "Time: 100.843" in raw
    expected_cases = {
        ("io.github.stopcran.kanji.ui.N1Batch072GlyphTest",
         "allotmentLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies"),
        ("io.github.stopcran.kanji.ui.N1Batch072ArticleTest",
         "fullSingleImportOfflineAllotmentTwoReciprocalPairsBothReadingsDrawingAndSystemBack"),
    }
    assert {(c["class"], c["test"]) for c in receipt["terminalCases"]} == expected_cases
    assert all(c["status"] == 0 for c in receipt["terminalCases"])
    compiled = load(ROOT / r"docs\n1-sources\execution-476.json")
    prep = load(ROOT / r"docs\n1-sources\batch-072-native-preparation.json")
    for entry in compiled["artifacts"]:
        assert sha(ROOT / entry["path"]) == entry["sha256"]
    for field in ("archive", "fixture"):
        assert sha(Path(prep[field])) == prep[field + "Sha256"] == receipt[field + "Sha256"]
    for field in ("testApk", "appApk"):
        assert sha(Path(receipt[field])) == receipt[field + "Sha256"]
    route = load(source / "n1-072-article-route.json")
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems",
                              "acceptedReadingParserEpoch", "archiveRequests")] == [1084, 5042, 104, 0, 1, 1]
    assert route["contentVersion"] == prep["contentVersion"] and route["contentSnapshot"] == prep["contentSnapshot"]
    assert route["fullOnyomi"] == route["fullProjectionOnyomi"] == ["ジュウ"]
    assert route["fullKunyomi"] == route["fullProjectionKunyomi"] == ["あ.てる", "み.たす"]
    assert route["quizOnKeys"] == ["じゅう"] and route["quizKunKeys"] == ["あてる"]
    assert route["liteQuizOnyomi"] == route["fullProjectionQuizOnyomi"] == ["ジュウ"]
    assert route["liteQuizKunyomi"] == route["fullProjectionQuizKunyomi"] == ["あ.てる"]
    for key in ("passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "bothCuratedKindsPersistedGoodNoMitasuAndDone", "drawingTraceThenRecall",
                "drawingGradeRecordedOnNext", "offline"):
        assert route[key] is True, key
    assert route["touchInjectedReferenceStrokes"] == 6 and route["phoneEvidence"] is False
    raster = load(source / "n1-072-font-raster.json")
    assert raster["individualGlyphProbes"] == 204 and raster["wholeWordRasterProbes"] == 8
    assert len(raster["rows"]) == 212
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        rows = [r for r in raster["rows"] if r["font"] == font]
        glyphs = [r for r in rows if "character" in r]
        assert {r["character"] for r in glyphs} == set(prep["plannedGlyphs"])
        assert all(r["hasGlyph"] for r in glyphs)
        assert len({r["nativePaintRasterSha256"] for r in glyphs}) == 51
        words = [r for r in rows if "word" in r]
        assert {r["word"] for r in words} == {"充てる", "拡充"}
        assert all(r["renderedCharactersNonblank"] == len(r["word"]) for r in words)
    post = load(LOG / "execution-477-postrun.json")
    assert post["contentHead"] == HEAD and post["contentStatus"] == post["androidStatus"] == []
    assert post["ownedProcessesRemaining"] == 0
    assert post["devices"] == receipt["prelaunch"]["devices"]
    assert post["preexistingEmulators"] == receipt["preexistingEmulators"] == post["remainingEmulators"]
    assert not any(c["State"] == 2 for c in post["connections"])
    pngs = sorted(source.glob("*.png"))
    groups = {}
    for path in pngs:
        groups.setdefault(sha(path), []).append(path.name)
    inspected = [f"n1-072-{step}.png" for step in DIRECT]
    assert len(pngs) == 44 and len(groups) == len(inspected) == 24
    assert {sha(source / name) for name in inspected} == set(groups)
    destination = FOLDER / "attempt-1"
    assert not destination.exists()
    shutil.copytree(source, destination)
    receipts = FOLDER / "execution-receipts"
    assert not receipts.exists()
    receipts.mkdir()
    for path in (Path(__file__), CONTROL / "run-477-native.ps1", LOG / "execution-477-postrun.json"):
        shutil.copyfile(path, receipts / path.name)
    files = []
    for base in (destination, receipts):
        for path in sorted(base.iterdir()):
            files.append({"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)})
    index = FOLDER / "execution-477-artifact-index.json"
    save(index, {
        "execution": 477, "batch": "072", "files": files, "sourcePngCount": len(pngs),
        "directCoordinatorImageRequests": inspected,
        "pngHashGroups": [{"sha256": h, "names": names, "directlyInspectedRepresentative":
                          next(n for n in names if n in inspected)} for h, names in sorted(groups.items())],
        "limits": "24 unique-byte native PNGs directly inspected;20 exact duplicates hash-mapped, not fresh reads. Coordinator inspection, not independent review or physical phone.",
    })
    progress = load(CONTROL / "progress.json")
    record = {
        "schemaVersion": 1, "execution": 477, "checkpoint": 477, "batch": "072",
        "status": "native-passed-awaiting-independent-visual-confirmation", "startingHead": HEAD,
        "reviewedTeachingSnapshot": compiled["reviewedTeachingSnapshot"],
        "authorization": progress["execution477StartingState"]["authorization"],
        "nativeExecution": receipt, "route": route,
        "artifactIndex": str(index.relative_to(ROOT)), "artifactIndexSha256": sha(index),
        "visualInspection": {
            "directUniqueByteImages": 24, "duplicateImagesHashMapped": 20,
            "productionFamilies": 4, "individualGlyphProbes": 204, "wholeWordRasterProbes": 8,
            "observations": "All four production rows legible;充/允/元/兄/先 distinguishable, isolated亠/儿/厶 nonblank. Complete new prose and changed reused paragraph visible across captures. Table at right offset clips left labels; left captures and explicit sideways-scroll hint preserve access. Both curated questions, feedback,2/2Done, meaning, selection, reciprocal Back and six-stroke reference/recall captures inspected.",
        },
        "inheritedHostAndroid475NotRerun": True, "nativeAcceptance": True,
        "independentVisualAcceptance": False, "runtimePublished": False,
        "phoneEvidence": False, "publishedAdditions": 98, "remainingAdditions": 1130,
        "postrun": post, "nextAction": NEXT,
        "limits": "Emulator not phone; raster hashes do not identify fallback face. Reference-coordinate touch injection is not human handwriting/MLKit. Offline first-use handwriting model unavailable as disclosed by app. Not independent visual approval/current-main/CI/public ZIP/whole-set acceptance. No runtime edits.",
    }
    save(RECORD, record)
    print(f"Archived {len(files)} artifacts, {len(pngs)} PNGs, {len(groups)} unique visual streams.")

elif sys.argv[1] == "checkpoint":
    record = load(RECORD)
    for item in load(ROOT / record["artifactIndex"])["files"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    assert not git("diff", record["reviewedTeachingSnapshot"], "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert not git("status", "--porcelain")
    commit = git("rev-parse", "HEAD")
    assert commit != HEAD and git("log", "-1", "--format=%G?") == "G"
    progress = load(CONTROL / "progress.json")
    before = load(LOG / "execution-477-before-progress.json")
    for key, value in before.items():
        if key not in {"stage"}:
            assert progress[key] == value, key
    checkpoint = {
        "execution": 477, "checkpoint": 477, "batch": "072", "status": "continue",
        "savedCommit": commit, "signature": "G", "record": str(RECORD.relative_to(ROOT)),
        "recordSha256": sha(RECORD), "runtimePublished": False, "nativeExecuted": True,
        "nativeAcceptance": True, "independentVisualAcceptance": False, "nextAction": NEXT,
        "publishedAdditions": 98, "remainingAdditions": 1130, "allOriginalHistoricalRootKeysPreserved": True,
    }
    progress.update(checkpoint=477, status="continue", stage="batch-072-native-passed-pending-visual-confirmation",
                    nextAction=NEXT, blocker=None)
    progress["execution477StartingState"]["status"] = "signed-native-acceptance-checkpoint-complete"
    progress["execution477CoordinatorCheckpoint"] = checkpoint
    progress["batch072NativeCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", progress)
    save(LOG / "execution-477-final-checkpoint.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))
