import hashlib
import json
import re
import shutil
import struct
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONTROL = Path(__file__).parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
HEAD = "9c0614c566d8051a85423ff05e477da6c57b293f"
FOLDER = ROOT / r"docs\n1-reviews\batch-071-native"
RECORD = ROOT / r"docs\n1-sources\execution-469.json"
DIRECT_IMAGES = [
    "font-pairs", "kanji-01", "kanji-09", "kanji-11", "kanji-20", "kanji-24",
    "word-02", "word-07", "word-new-kanji-backlink", "curated-On-question",
    "curated-On-feedback", "curated-on-only-done", "selection", "meaning-question",
    "meaning-feedback", "drawing-trace", "drawing-feedback", "drawing-recall-feedback",
    "kanji-03", "word-03", "system-back-kanji-word", "system-back-word-kanji",
]
DIRECT_IMAGES = [f"n1-071-{name}.png" for name in DIRECT_IMAGES]
NEXT = (
    "SAME071: native checkpoint469 passed BOTH named cases terminal0/no skips in112.22s. "
    "Read docs\\n1-sources\\execution-469.json and batch-071-native\\execution-469-artifact-index.json. "
    "Exact signed f6ff96a1 full Git envelope through ContentSync ONCE:1083kanji5041words103N1/"
    "version05002d6e68a4eb89/problems0/epoch1. Full+Lite fullイン andじょう/まこと.に/ゆるす "
    "preserved; sole curatedイン/normalizedいん, explicit empty quizKunyomi, Good on grade "
    "persisted/noKunLog/Done1correct. Two complete article projections/all four reading "
    "labels+explanations/one mapped reciprocal pair two directions/SystemBack/offline/N1selection/"
    "meaning/fourreference-touch-strokes/ungradedtrace/recallmiss/persistedDrawAgain pass. "
    "108singlePaint+4wordRaster probes cover actual27distinctHan including isolated儿/厶/口/土 "
    "and公/先 across four production families, not stale25. 40originalPNGs archived; "
    "22unique-byte images directly coordinator-inspected and18duplicates hash-mapped, not18fresh "
    "visual reads. Four production rows visibly readable/distinct; horizontal table scroll "
    "clips first-column left edge at rightmost offset, explicit scroll hint retained; left and "
    "right captures jointly preserve labels/explanations. Owned parent412/QEMU19604 stopped; "
    "preexisting5556 unchanged; sharedADB9520 reconnect/OS TIME_WAIT preserved, no listener. "
    "Next bounded checkpoint original Claude43cc8b39-2d2e-4d29-a274-d582d2ac4e02 THEN "
    "GPT08e79180-ae38-4be2-bc8c-cd2f83041ab0 SERIAL dependent visual confirmations with supported "
    "read-only tools and bounded PNG/route/fixture/source packets. Record actual read/image coverage "
    "and limits; not new blind initial reviews. No rerun passing native or467Android3+1 absent "
    "new concern. Qualified inherited HOST-only2GiB init NEVER native; original heaps/guards unchanged. "
    "Then freshlatestmain nonrewriting integration/allcombinedvalidation/normalsigning/ownerfastforward/"
    "publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash+originalbudgets/ownerissue60 "
    "BEFOREdelivery or072. No secondrunner/supervisor edits/permission bypass/signing workaround. "
    "Published97/1228,remaining1131;071 local NOTdelivered. CompatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set acceptance outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == data


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd, encoding="utf-8").strip()


def verify(record):
    index = ROOT / record["artifactIndex"]
    assert sha(index) == record["artifactIndexSha256"]
    for entry in load(index)["files"]:
        path = ROOT / entry["path"]
        assert sha(path) == entry["sha256"] and path.stat().st_size == entry["bytes"], path
    assert not git("diff", record["reviewedTeachingSnapshot"], "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")
    compiled = load(ROOT / r"docs\n1-sources\execution-468.json")
    for entry in compiled["originalReportsUnchanged"].values():
        assert sha(ROOT / r"docs\n1-reviews" / entry["report"]) == entry["sha256"]
    assert git("rev-parse", "HEAD", cwd=ANDROID) == record["nativeExecution"]["androidSnapshot"]
    assert not git("status", "--porcelain", cwd=ANDROID)
    print(f"Verified {len(load(index)['files'])} evidence hashes and unchanged runtime/original reports.")


mode = sys.argv[1]
if mode == "archive":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    receipt = load(CONTROL / "batch-071-native-attempt-1-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert receipt["prelaunch"]["connections"] == []
    assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
    source = CONTROL / r"artifacts\batch-071-native-attempt-1"
    raw = (source / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "OK (2 tests)" in raw and "Time: 112.22" in raw
    expected_cases = {
        ("io.github.stopcran.kanji.ui.N1Batch071GlyphTest",
         "permissionLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies"),
        ("io.github.stopcran.kanji.ui.N1Batch071ArticleTest",
         "fullSingleImportOfflinePermissionReciprocalPairOnOnlyDrawingAndSystemBack"),
    }
    assert {(case["class"], case["test"]) for case in receipt["terminalCases"]} == expected_cases
    assert all(case["status"] == 0 for case in receipt["terminalCases"])
    compiled = load(ROOT / r"docs\n1-sources\execution-468.json")
    prep = load(ROOT / r"docs\n1-sources\batch-071-native-preparation.json")
    for entry in compiled["artifacts"]:
        assert sha(ROOT / entry["path"]) == entry["sha256"]
    assert sha(Path(prep["archive"])) == prep["archiveSha256"] == receipt["archiveSha256"]
    assert sha(Path(prep["fixture"])) == prep["fixtureSha256"] == receipt["fixtureSha256"]
    for name in ("testApk", "appApk"):
        assert sha(Path(receipt[name])) == receipt[f"{name}Sha256"]
    route = load(source / "n1-071-article-route.json")
    assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems",
                                  "acceptedReadingParserEpoch", "archiveRequests")] == [1083, 5041, 103, 0, 1, 1]
    assert route["contentVersion"] == prep["contentVersion"]
    assert route["contentSnapshot"] == prep["contentSnapshot"]
    assert route["fullOnyomi"] == route["fullProjectionOnyomi"] == ["イン"]
    assert route["fullKunyomi"] == route["fullProjectionKunyomi"] == ["じょう", "まこと.に", "ゆるす"]
    assert route["quizOnKeys"] == ["いん"] and route["quizKunKeys"] == []
    assert route["liteQuizOnyomi"] == route["fullProjectionQuizOnyomi"] == ["イン"]
    assert route["liteQuizKunyomi"] == route["fullProjectionQuizKunyomi"] == []
    for key in ("passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedOnPersistedGoodNoKunAndDone", "drawingTraceThenRecall",
                "drawingGradeRecordedOnNext", "offline"):
        assert route[key] is True, key
    assert route["touchInjectedReferenceStrokes"] == 4 and route["phoneEvidence"] is False
    raster = load(source / "n1-071-font-raster.json")
    assert raster["individualGlyphProbes"] == 108 and raster["wholeWordRasterProbes"] == 4
    assert len(raster["rows"]) == 112
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
        assert {row["character"] for row in glyphs} == set(prep["plannedGlyphs"])
        assert all(row["hasGlyph"] for row in glyphs)
        assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 27
        words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
        assert {row["word"] for row in words} == {"允可"}
        assert all(row["renderedCharactersNonblank"] == 2 for row in words)
    postrun = load(CONTROL / "execution-469-postrun-verification.json")
    assert postrun["contentHead"] == HEAD and postrun["contentStatus"] == [] and postrun["androidStatus"] == []
    assert postrun["ownedProcessesRemaining"] == 0
    assert postrun["devices"] == receipt["prelaunch"]["devices"]
    assert postrun["preexistingEmulators"] == receipt["preexistingEmulators"]
    assert not any(connection["State"] == 2 for connection in postrun["connections"])
    assert all(owner["Name"] == "adb.exe" for owner in postrun["connectionOwners"])
    destination = FOLDER / "attempt-1"
    assert not destination.exists()
    expected = set(receipt["artifacts"]) | {
        "N1Batch071NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
        "emulator-stdout.txt", "execution.json", "instrumentation.txt",
    }
    assert {path.name for path in source.iterdir()} == expected
    pngs = sorted(source.glob("*.png"))
    assert len(pngs) == 40
    groups = {}
    for path in pngs:
        groups.setdefault(sha(path), []).append(path.name)
    assert len(groups) == 22
    assert len(DIRECT_IMAGES) == 22
    assert {sha(source / name) for name in DIRECT_IMAGES} == set(groups)
    destination.mkdir()
    artifacts = []

    def copy(path, target):
        shutil.copyfile(path, target)
        assert sha(path) == sha(target)
        entry = {"path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": sha(target)}
        if target.suffix == ".png":
            data = target.read_bytes()
            assert data[:8] == b"\x89PNG\r\n\x1a\n"
            entry["dimensions"] = list(struct.unpack(">II", data[16:24]))
        artifacts.append(entry)

    for path in sorted(source.iterdir()):
        assert path.is_file()
        copy(path, destination / path.name)
    receipts = FOLDER / "execution-receipts"
    assert not receipts.exists()
    receipts.mkdir()
    for name in ("run-469-native.ps1", "archive-469-native.py", "execution-469-postrun-verification.json"):
        copy(CONTROL / name, receipts / name)
    index_path = FOLDER / "execution-469-artifact-index.json"
    save(index_path, {
        "schemaVersion": 1, "execution": 469, "batch": "071", "attempt": 1,
        "files": artifacts, "sourcePngCount": 40, "directCoordinatorImageRequests": DIRECT_IMAGES,
        "pngHashGroups": [{"sha256": key, "names": names,
                           "directlyInspectedRepresentative": next(name for name in names if name in DIRECT_IMAGES)}
                          for key, names in sorted(groups.items())],
        "limits": "22 directly inspected native PNGs cover all22 unique image byte streams; other18 files are exact duplicates, not additional fresh visual reads. This is coordinator inspection, not independent review or physical-phone evidence.",
    })
    progress = load(CONTROL / "progress.json")
    record = {
        "schemaVersion": 1, "execution": 469, "checkpoint": 469, "batch": "071",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingHead": HEAD, "reviewedTeachingSnapshot": compiled["reviewedTeachingSnapshot"],
        "authorization": progress["execution469StartingState"]["authorization"],
        "scope": progress["execution469StartingState"]["scope"],
        "nativeExecution": receipt, "nativeRouteEvidence": route,
        "artifactIndex": str(index_path.relative_to(ROOT)), "artifactIndexSha256": sha(index_path),
        "sourcePngCount": 40, "uniquePngByteStreams": 22, "directCoordinatorImageRequests": DIRECT_IMAGES,
        "visualObservations": (
            "All27 distinct Han and whole word允可 visibly readable in four production font rows. "
            "允 has upper厶 above儿; 元/兄/去 have different tops/bottoms, 公/先 also distinct. "
            "Standalone儿/厶 and口/土 render nonblank without replacement boxes; fallback face not identified. "
            "Both articles' paragraphs, historical example允可を得る, formal/older-register warnings, "
            "ordinary-permission contrast and component explanation wrap legibly with linked anchors. "
            "Left-aligned reading capture shows fullイン/じょう/まこと.に/ゆるす labels; rightward "
            "table captures show complete historical/classical/character-dictionary explanations while "
            "clipping first-column left edges. Explicit sideways-scroll hint remains. This is combined "
            "left/right evidence, not all columns simultaneously readable. Bottomゆるす explanation "
            "visible completely inkanji-20. Meaning choices camphor tree/chestnut/hawk;falcon are distinct "
            "from permit;sincerity; feedback marks the intended answer. On question showsイン/ハン/ケン/リン "
            "and correctイン feedback; Done says1 of1 correct. N1 selection says103cards. "
            "Drawing trace shows four numbered strokes; touch-injected reference geometry produces "
            "ungraded practice with model-unavailable qualification. Recall miss has blank drawing and "
            "four-stroke reference. This is not human handwriting/MLKit or phone acceptance. "
            "System Back captures return to the expected articles."
        ),
        "glyphCountCorrection": "Actual fixture/plannedGlyphs contain27 distinct Han, not stale25 in the inherited nextAction. 27x4=108 individual probes plus4 whole-word probes; no scope or gate reduction.",
        "postrunVerification": postrun,
        "nativeAcceptance": True, "independentVisualAcceptance": False, "phoneEvidence": False,
        "accepted467AndroidRetainedWithoutRerun": True, "runtimeEditsMade": False,
        "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 97, "remainingAdditions": 1131, "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None, "recordedAt": datetime.now().astimezone().isoformat(),
        "limits": "Native emulator assertions plus22 direct coordinator PNG inspections and18 byte-identical duplicate mappings only. Synthetic unique source/HEAD, full production import once with unchanged guards/heaps/fonts. No owner progress, independent visual/physical-phone acceptance, fallback-face identification, MLKit or human recall. Textual466/Android467 inherited unchanged, not rerun. Historical permission denials/HOST OOMs retained. Latest-main publication and whole-set acceptance outstanding.",
    }
    assert not RECORD.exists()
    save(RECORD, record)
    batch_path = ROOT / r"docs\n1-sources\batch-071-progress.json"
    batch = load(batch_path)
    batch["status"] = record["status"]
    batch["nextAction"] = NEXT
    batch["nativeExecutionCheckpoint"] = {
        "execution": 469, "record": "execution-469.json", "terminalSuccessCases": 2,
        "nativePassed": True, "postrunVerification": True,
        "independentVisualAcceptance": False, "publicationAttempted": False, "limits": record["limits"],
    }
    save(batch_path, batch)
    verify(record)
    print("Archived both passing cases and40 PNGs (22 unique byte streams directly inspected).")
elif mode == "verify":
    verify(load(RECORD))
elif mode == "checkpoint":
    record = load(RECORD)
    verify(record)
    signed_head = git("rev-parse", "HEAD")
    assert signed_head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    before = json.loads(json.dumps(progress))
    assert progress["checkpoint"] == 468 and progress["batch"] == "071"
    summary = {
        "execution": 469, "checkpoint": 469, "batch": "071", "savedCommit": signed_head,
        "signature": "G", "record": r"docs\n1-sources\execution-469.json",
        "recordSha256": sha(RECORD), "status": "continue", "nativePassed": True,
        "terminalSuccessCases": 2, "postrunVerification": True,
        "sourcePngCount": 40, "directlyInspectedUniquePngs": 22,
        "independentVisualAcceptance": False, "runtimePublished": False,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=469, status="continue",
                    stage="batch-071-native-passed-awaiting-independent-visual-confirmation",
                    nextAction=NEXT, blocker=None)
    progress["execution469StartingState"]["status"] = "signed-native-execution-checkpoint-complete"
    progress["batch071NativeExecutionCheckpoint"] = summary
    progress["execution469CoordinatorCheckpoint"] = summary
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker", "execution469StartingState"}:
        assert progress[key] == before[key], key
    temporary = CONTROL / "execution-469-progress.tmp"
    save(temporary, progress)
    temporary.replace(progress_path)
    save(CONTROL / "execution-469-checkpoint.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
else:
    raise ValueError(mode)
