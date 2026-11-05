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
LOG = CONTROL / r"logs\586c174d-f7ef-4f03-a1d0-e2020c7b3ee6"
HEAD = "79b3ced488f35f70a1062064a8d4e66af79fc980"
FOLDER = ROOT / r"docs\n1-reviews\batch-073-native"
RECORD = ROOT / r"docs\n1-sources\execution-485.json"
DIRECT = """font-pairs kanji-01 kanji-03 kanji-09 kanji-11 kanji-17
word-reused-07 clothing-reused-03 word-kanji-backlink
selection meaning-question meaning-feedback curated-On-question curated-On-feedback
curated-on-only-done drawing-trace drawing-feedback drawing-recall-feedback""".split()
NEXT = (
    "SAME073: native485 BOTH named cases terminal0/no skips in82.165s; read docs\\n1-sources\\execution-485.json "
    "and batch-073-native\\execution-485-artifact-index.json. Full signed5d322346 Git envelope through "
    "production ContentSync ONCE:1085kanji5042words105N1/version1d8a4ee1a97c6bb5/problems0/epoch1. "
    "Full+Lite rawコク/か.つ retained; curatedコク/[], normalizedこく/[]; sole on Good log/Done1correct/"
    "no kun question or log. Complete new克 projection asserted, both metadata reading labels/explanations, "
    "exact reused克服 component paragraph and服 sentence,2reciprocalpairs/4directions/SystemBack/offline/"
    "N1selection/meaning/sevenreference-touchstrokes/ungradedtrace/recallAgain pass.108singlePaint+4wordRaster "
    "probes cover27actualHan including isolated儿 across4productionfamilies.30originalPNGs/18unique byte "
    "streams directly coordinator-inspected;12duplicates hash-mapped, not fresh visual reads. Left/right "
    "table captures jointly retain labels/examples; horizontal clipping and explicit scroll hint inherited. "
    "Final source-link line partly below frame in notes capture; complete projection/selector is not "
    "every-character screenshot evidence. Owned3704/QEMU12804 and delayed emulator shutdown helper28476 "
    "exited; preexisting5556 unchanged; sharedADB9520 reconnect/OS TIME_WAIT not listeners. "
    "NEXT original Claude482a74cb-d8a4-47d5-8e7d-1451bbdfc13b THEN GPT427eb11f-e4a8-43eb-9677-eb03d1065cfe "
    "SERIAL dependent visual confirmations on bounded PNG/route/fixture/source packets; record actual "
    "coverage, not new blind initial reviews. Do not rerun passing native or483HOST3+1 absent new concern. "
    "No HOST heap init/native heap/guard changes; raster hashes do not identify fallback face; injected "
    "trace not human handwriting/MLKit. Then freshmain nonrewriting integration/allcombinedvalidation/"
    "normalsigning/ownerfastforward/publicSHA/greenCI/everyimmutablepublicZIPruntimehash/originalbudgets/"
    "ownerissue60 BEFORE delivery or074. No secondrunner/supervisor edits/signingretry/permissionworkaround. "
    "Published99/1228,remaining1129;100published necessary supports NOTN1vocabulary. CompatibleAndroidf9b59a2+ "
    "required; physicalphone/generalrelease/whole-set acceptance outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".485.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == data
    temporary.replace(path)


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
    assert progress["checkpoint"] == checkpoint["checkpoint"] == 484
    assert progress["status"] == "continue" and progress["batch"] == "073"
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    before = LOG / "execution-485-before-progress.json"
    assert not before.exists()
    shutil.copyfile(CONTROL / "progress.json", before)
    state = {
        "execution": 485, "batch": "073", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME073 compiled exact-full-archive native execution and coordinator visual inspection only; no reviewer/publication/074/second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and embedded checkpoint parsed; operative contract, complete approved issue and complete final484 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
        "status": "native-execution-starting",
    }
    progress["execution485StartingState"] = state
    progress["stage"] = "batch-073-native-executing"
    save(LOG / "execution-485-start.json", state)
    save(CONTROL / "progress.json", progress)
    source = (CONTROL / "run-477-native.ps1").read_text(encoding="utf-8-sig")
    replacements = {
        "072": "073",
        "477": "485",
        "execution-476.json": "execution-484.json",
        "3618d604582809ed25b0414fccf7c4e8b2e4dd0d": HEAD,
        "e636affe-bea9-4c9b-a92c-a27fe3fa479c": "586c174d-f7ef-4f03-a1d0-e2020c7b3ee6",
    }
    for old, new in replacements.items():
        assert old in source, old
        source = source.replace(old, new)
    runner = CONTROL / "run-485-native.ps1"
    assert not runner.exists()
    runner.write_text(source, encoding="utf-8")
    assert "072" not in source and "477" not in source and "execution-484.json" in source
    print(json.dumps(state, ensure_ascii=False, indent=2))
elif sys.argv[1] == "archive":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    receipt = load(CONTROL / "batch-073-native-attempt-1-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert receipt["prelaunch"]["connections"] == []
    assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
    source = CONTROL / r"artifacts\batch-073-native-attempt-1"
    raw = (source / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "OK (2 tests)" in raw and "Time: 82.165" in raw
    expected_cases = {
        ("io.github.stopcran.kanji.ui.N1Batch073GlyphTest",
         "overcomeLookalikesAndIsolatedRadicalAcrossFourProductionFamilies"),
        ("io.github.stopcran.kanji.ui.N1Batch073ArticleTest",
         "fullSingleImportOfflineOvercomeTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
    }
    assert {(c["class"], c["test"]) for c in receipt["terminalCases"]} == expected_cases
    assert all(c["status"] == 0 for c in receipt["terminalCases"])
    compiled = load(ROOT / r"docs\n1-sources\execution-484.json")
    prep = load(ROOT / r"docs\n1-sources\batch-073-native-preparation.json")
    for entry in compiled["artifacts"]:
        assert sha(ROOT / entry["path"]) == entry["sha256"]
    for field in ("archive", "fixture"):
        assert sha(Path(prep[field])) == prep[field + "Sha256"] == receipt[field + "Sha256"]
    for field in ("testApk", "appApk"):
        assert sha(Path(receipt[field])) == receipt[field + "Sha256"]
    route = load(source / "n1-073-article-route.json")
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems",
                              "acceptedReadingParserEpoch", "archiveRequests")] == [1085, 5042, 105, 0, 1, 1]
    assert route["contentVersion"] == prep["contentVersion"] and route["contentSnapshot"] == prep["contentSnapshot"]
    assert route["fullOnyomi"] == route["fullProjectionOnyomi"] == ["コク"]
    assert route["fullKunyomi"] == route["fullProjectionKunyomi"] == ["か.つ"]
    assert route["quizOnKeys"] == ["こく"] and route["quizKunKeys"] == []
    assert route["liteQuizOnyomi"] == route["fullProjectionQuizOnyomi"] == ["コク"]
    assert route["liteQuizKunyomi"] == route["fullProjectionQuizKunyomi"] == []
    for key in ("passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedOnPersistedGoodNoKunAndDone", "drawingTraceThenRecall",
                "drawingGradeRecordedOnNext", "offline"):
        assert route[key] is True, key
    assert route["touchInjectedReferenceStrokes"] == 7 and route["phoneEvidence"] is False
    raster = load(source / "n1-073-font-raster.json")
    assert raster["individualGlyphProbes"] == 108 and raster["wholeWordRasterProbes"] == 4
    assert len(raster["rows"]) == 112
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        rows = [r for r in raster["rows"] if r["font"] == font]
        glyphs = [r for r in rows if "character" in r]
        assert {r["character"] for r in glyphs} == set(prep["plannedGlyphs"])
        assert all(r["hasGlyph"] for r in glyphs)
        assert len({r["nativePaintRasterSha256"] for r in glyphs}) == 27
        words = [r for r in rows if "word" in r]
        assert {r["word"] for r in words} == {"克服"}
        assert all(r["renderedCharactersNonblank"] == len(r["word"]) for r in words)
    post = load(LOG / "execution-485-postrun-final.json")
    assert post["contentHead"] == HEAD and post["contentStatus"] == post["androidStatus"] == []
    assert post["ownedProcessesRemaining"] == 0
    assert post["devices"] == receipt["prelaunch"]["devices"]
    assert post["remainingEmulators"] == receipt["preexistingEmulators"]
    assert not any(c["State"] == 2 for c in post["connections"])
    pngs = sorted(source.glob("*.png"))
    groups = {}
    for path in pngs:
        groups.setdefault(sha(path), []).append(path.name)
    inspected = [f"n1-073-{step}.png" for step in DIRECT]
    assert len(pngs) == 30 and len(groups) == len(inspected) == 18
    assert {sha(source / name) for name in inspected} == set(groups)
    destination = FOLDER / "attempt-1"
    assert not destination.exists()
    shutil.copytree(source, destination)
    receipts = FOLDER / "execution-receipts"
    assert not receipts.exists()
    receipts.mkdir()
    for path in (Path(__file__), CONTROL / "run-485-native.ps1",
                 LOG / "execution-485-postrun.json", LOG / "execution-485-postrun-final.json"):
        shutil.copyfile(path, receipts / path.name)
    files = []
    for base in (destination, receipts):
        for path in sorted(base.iterdir()):
            files.append({"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)})
    index = FOLDER / "execution-485-artifact-index.json"
    save(index, {
        "execution": 485, "batch": "073", "files": files, "sourcePngCount": len(pngs),
        "directCoordinatorImageRequests": inspected,
        "pngHashGroups": [{"sha256": h, "names": names, "directlyInspectedRepresentative":
                          next(n for n in names if n in inspected)} for h, names in sorted(groups.items())],
        "limits": "18 unique-byte native PNGs directly inspected;12 exact duplicates hash-mapped, not fresh reads. Coordinator inspection, not independent review or physical phone.",
    })
    progress = load(CONTROL / "progress.json")
    record = {
        "schemaVersion": 1, "execution": 485, "checkpoint": 485, "batch": "073",
        "status": "native-passed-awaiting-independent-visual-confirmation", "startingHead": HEAD,
        "reviewedTeachingSnapshot": compiled["reviewedTeachingSnapshot"],
        "authorization": progress["execution485StartingState"]["authorization"],
        "nativeExecution": receipt, "route": route,
        "artifactIndex": str(index.relative_to(ROOT)), "artifactIndexSha256": sha(index),
        "visualInspection": {
            "directUniqueByteImages": 18, "duplicateImagesHashMapped": 12,
            "productionFamilies": 4, "individualGlyphProbes": 108, "wholeWordRasterProbes": 4,
            "observations": "All four production rows legible;克/古/兄/元 distinguishable; isolated儿 and all27 authored Han nonblank. Main new teaching prose and both changed reused passages legible. Reading labels and examples jointly accessible in left/right captures with explicit sideways-scroll hint; horizontal clipping inherited. Source-link final line partly below notes frame; complete projection/selector assertion is not every-character visibility in a screenshot. Sole on question/feedback/1of1Done, meaning, selection, reciprocal Back and seven-stroke reference/recall inspected.",
        },
        "inheritedHostAndroid483NotRerun": True, "nativeAcceptance": True,
        "independentVisualAcceptance": False, "runtimePublished": False,
        "phoneEvidence": False, "publishedAdditions": 99, "remainingAdditions": 1129,
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
    assert git("rev-parse", "HEAD^") == HEAD
    progress = load(CONTROL / "progress.json")
    before = load(LOG / "execution-485-before-progress.json")
    for key, value in before.items():
        if key != "stage":
            assert progress[key] == value, key
    checkpoint = {
        "execution": 485, "checkpoint": 485, "batch": "073", "status": "continue",
        "savedCommit": commit, "signature": "G", "record": str(RECORD.relative_to(ROOT)),
        "recordSha256": sha(RECORD), "runtimePublished": False, "nativeExecuted": True,
        "nativeAcceptance": True, "independentVisualAcceptance": False, "nextAction": NEXT,
        "publishedAdditions": 99, "remainingAdditions": 1129, "allOriginalHistoricalRootKeysPreserved": True,
    }
    progress.update(checkpoint=485, status="continue", stage="batch-073-native-passed-pending-visual-confirmation",
                    nextAction=NEXT, blocker=None)
    progress["execution485StartingState"]["status"] = "signed-native-acceptance-checkpoint-complete"
    progress["execution485CoordinatorCheckpoint"] = checkpoint
    progress["batch073NativeCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", progress)
    save(LOG / "execution-485-final-checkpoint.json", checkpoint)
    body = (
        f"Batch **073 (克)**: native checkpoint **485** saved locally at signed `{commit}`; "
        "**not published**. Both named emulator cases returned terminal status `0` with no skips "
        "(82.165 s), importing the complete signed `5d322346` archive through production ContentSync once: "
        "1,085 kanji / 5,042 words / 105 N1, version `1d8a4ee1a97c6bb5`, zero problems, parser epoch 1.\n\n"
        "Full/Lite preserve raw `コク / か.つ`; curated `コク / []` yields only `こく`, persisted Good, "
        "1/1 correct and no kun question/log. N1 selection, meaning, the new article, both changed reused "
        "passages, two reciprocal pairs/four directions, system Back, offline routes, seven reference-touch "
        "strokes, ungraded trace and recall Again passed. All 27 authored Han (including isolated 儿) "
        "were probed across four production families, plus four 克服 rasters. Coordinator inspected "
        "18 unique PNG byte streams from 30 captures; 12 duplicates are hash-mapped, not fresh reads. "
        "Left/right table captures jointly expose the content with the inherited scroll hint; the final "
        "source-link line is partly below the notes frame. These are not physical-phone, fallback-face "
        "identification or human-handwriting/MLKit results.\n\n"
        "Owned emulator-5580 parent 3704 / QEMU 12804 and its delayed shutdown helper exited; pre-existing "
        "emulator-5556 unchanged. No guest/app heap or guard changes. Fresh checkpoint483 HOST Android "
        "3+1 results inherited without rerun. Evidence: `docs/n1-sources/execution-485.json` and "
        "`docs/n1-reviews/batch-073-native/execution-485-artifact-index.json`.\n\n"
        "**Next:** original Claude then GPT serial dependent visual confirmations, followed by current-main "
        "integration/validation, normal signing and publication/CI/immutable-ZIP gates. No batch074 started. "
        "**Published remains 99/1,228 additions; 1,129 remain**, with 100 necessary published support articles "
        "(not an N1 vocabulary deck). Compatible Android `f9b59a2+` required; physical-phone, general-release "
        "and whole-set acceptance remain outstanding."
    )
    (LOG / "issue-485-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))
else:
    raise SystemExit("Unsupported stage")
