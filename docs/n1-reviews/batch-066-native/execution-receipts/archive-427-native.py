import hashlib
import json
import re
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / r"docs\n1-reviews\batch-066-native"
HEAD = "428a9ecf96af91c0022f9f88892b2f8265d4cdf1"
RECORD = ROOT / r"docs\n1-sources\execution-427.json"
NEXT = (
    "SAME066 native checkpoint427: both named Glyph/Article cases terminal0/no skips/"
    "93.971s. Read docs\\n1-sources\\execution-427.json and batch-066-native\\"
    "execution-427-artifact-index.json; 41 original PNGs/raw logs archived, eight direct "
    "coordinator images inspected, not complete-PNG acceptance. Exact full signed175fdf3f "
    "Git envelope imported through production ContentSync ONCE:1078kanji5036words98N1/"
    "a9ecc100b6c1335c/problems0/epoch1. Full+Liteリョウ/emptyKun; sole normalizedりょう "
    "Good persisted/noKunLog. Both mapped pairs僚-同僚/同-同僚 in4directions, complete3"
    "article semantics/SystemBack/offline/N1selection/meaning/14reference-stroke touch/"
    "ungradedtrace/recallmiss/persistedDrawAgain.36singlePaint+4wordraster probes pass; "
    "four production rows visibly readable僚療像値人亻疒同口/同僚. Article/table examples "
    "wrap legibly; first-column left edge clipped at current horizontal table offset "
    "with explicit scroll hint. No fallback-face identification/MLKit/humanhandwriting/"
    "physicalphone acceptance. Owned parent4276/QEMU25352 stopped; preexistingemulator5556 "
    "unchanged, clean worktrees, no owned PIDs/listeners; postrun OS TIME_WAIT preserved. "
    "Next bounded checkpoint: ORIGINAL Claude9db759dd-1a9d-4c7f-b3ab-049af5686bc4 then "
    "GPT81338bd1-836a-4b79-9fc6-69d90c5d00ab SERIAL bounded dependent visual confirmations "
    "using actual supported CLI/read-only controls/scoped control access. Record actual "
    "returned image/read-depth/source limits, not new blind reviews. Do not rerun passed "
    "native or accepted425 Android3+1 absentnewconcern; qualified HOST2GiB init NEVER "
    "native builds. Preserve original denials/OOMs/424 textual closure/reports and full "
    "livehistory. Then freshlatestmain nonrewriting integration/allcombined source-"
    "baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/original "
    "18000entries42MiBcompressed80MiBinflated56MiBretained budgets/normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/"
    "ownerissue60 BEFOREdelivery or067. Permissiondenial/signingwait: preserve exact "
    "command/error and yield; no workaround, secondrunner, concurrentheavywork or "
    "supervisorchanges. Published92/1228,1136remain/latest06544645f54; local066 "
    "NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/"
    "whole-set outstanding. Overallproject incomplete."
)
IMAGES = [
    "n1-066-font-pairs.png",
    "n1-066-coworker-rank-boundary.png",
    "n1-066-same-attachment.png",
    "n1-066-kanji-on-reading.png",
    "n1-066-curated-On-question.png",
    "n1-066-drawing-feedback.png",
    "n1-066-coworker-consult-example.png",
    "n1-066-meaning-feedback.png",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd, encoding="utf-8").strip()


def verify(record):
    index = load(ROOT / record["artifactIndex"])
    assert sha(ROOT / record["artifactIndex"]) == record["artifactIndexSha256"]
    for entry in index["files"]:
        path = ROOT / entry["path"]
        assert sha(path) == entry["sha256"] and path.stat().st_size == entry["bytes"], path
    assert not git("diff", record["reviewedTeachingSnapshot"], "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")
    compiled = load(ROOT / r"docs\n1-sources\execution-426.json")
    for relative, expected in compiled["originalReportHashesUnchanged"].items():
        assert sha(ROOT / relative) == expected
    android = CONTROL.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", cwd=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", cwd=android)
    print(f"Verified {len(index['files'])} evidence hashes; runtime and original reports unchanged.")


mode = sys.argv[1] if len(sys.argv) > 1 else "archive"
if mode == "archive":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    receipt = load(CONTROL / "batch-066-native-attempt-1-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert receipt["prelaunch"]["connections"] == []
    assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
    source = CONTROL / r"artifacts\batch-066-native-attempt-1"
    raw = (source / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "OK (2 tests)" in raw and "Time: 93.971" in raw
    for kind, method in (
        ("Glyph", "colleagueLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
        ("Article", "fullSingleImportOfflineColleagueTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
    ):
        assert raw.count(f"INSTRUMENTATION_STATUS: class=io.github.stopcran.kanji.ui.N1Batch066{kind}Test") == 2
        assert raw.count(f"INSTRUMENTATION_STATUS: test={method}") == 2
    compiled = load(ROOT / r"docs\n1-sources\execution-426.json")
    for item in compiled["artifacts"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    for name in ("fixture", "archive"):
        assert sha(Path(compiled[name])) == compiled[f"{name}Sha256"]
    for name in ("testApk", "appApk"):
        assert sha(Path(receipt[name])) == receipt[f"{name}Sha256"]
    route = load(source / "n1-066-article-route.json")
    assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems",
                                  "acceptedReadingParserEpoch", "archiveRequests")] == [1078, 5036, 98, 0, 1, 1]
    assert route["contentVersion"] == "a9ecc100b6c1335c"
    assert route["contentSnapshot"] == compiled["startingHead"]
    assert route["fullOnyomi"] == ["リョウ"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["りょう"] and route["quizKunKeys"] == []
    for key in ("passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
                "drawingGradeRecordedOnNext", "offline"):
        assert route[key] is True, key
    assert route["touchInjectedReferenceStrokes"] == 14 and route["phoneEvidence"] is False
    raster = load(source / "n1-066-font-raster.json")
    assert raster["individualGlyphProbes"] == 36 and raster["wholeWordRasterProbes"] == 4
    assert len(raster["rows"]) == 40
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
        assert {row["character"] for row in glyphs} == set("僚療像値人亻疒同口")
        assert all(row["hasGlyph"] for row in glyphs)
        assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 9
        words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
        assert len(words) == 1 and words[0]["word"] == "同僚"
        assert words[0]["renderedCharactersNonblank"] == 2
    postrun = load(CONTROL / "execution-427-postrun-verification.json")
    assert postrun["contentHead"] == HEAD and postrun["contentStatus"] == [] and postrun["androidStatus"] == []
    assert postrun["ownedProcessesRemaining"] == 0
    assert postrun["devices"] == receipt["prelaunch"]["devices"]
    assert all(connection["State"] == 11 and connection["OwningProcess"] == 0
               for connection in postrun["connections"])
    destination = FOLDER / "attempt-1"
    assert not destination.exists()
    destination.mkdir()
    expected = set(receipt["artifacts"]) | {
        "N1Batch066NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
        "emulator-stdout.txt", "execution.json", "instrumentation.txt",
    }
    assert {path.name for path in source.iterdir()} == expected
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
    for name in ("run-427-native.ps1", "start-427.py", "archive-427-native.py",
                 "execution-427-start.json", "execution-427-postrun-verification.json"):
        copy(CONTROL / name, receipts / name)
    png_count = sum("dimensions" in entry for entry in artifacts)
    assert png_count == 41, png_count
    assert set(IMAGES) <= {path.name for path in source.iterdir()}
    index_path = FOLDER / "execution-427-artifact-index.json"
    save(index_path, {
        "schemaVersion": 1, "execution": 427, "batch": "066", "attempt": 1,
        "files": artifacts, "sourcePngCount": png_count, "directCoordinatorImageRequests": IMAGES,
        "limits": "Eight direct coordinator PNG inspections. Other33 archived PNGs not visually inspected by coordinator. Hashes/assertions do not establish complete readability or independent visual acceptance.",
    })
    record = {
        "schemaVersion": 1, "execution": 427, "checkpoint": 427, "batch": "066",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingHead": HEAD, "reviewedTeachingSnapshot": compiled["reviewedTeachingSnapshot"],
        "authorization": load(CONTROL / "execution-427-start.json")["authorization"],
        "scope": load(CONTROL / "execution-427-start.json")["scope"],
        "nativeExecution": receipt, "nativeRouteEvidence": route,
        "artifactIndex": str(index_path.relative_to(ROOT)), "artifactIndexSha256": sha(index_path),
        "sourcePngCount": png_count, "directCoordinatorImageRequests": IMAGES,
        "visualObservations": (
            "All nine characters and 同僚 are readable and distinguishable in all four production font rows. "
            "Standalone 亻 and 疒 render consistently across styles; actual fallback faces not identified. "
            "僚/療 have distinct person/illness left components; 像/値 right components remain distinct. "
            "Coworker examples, consulted-person に, plural/context explanation, rank qualification, "
            "component links and 同じ direct attachment note wrap legibly. The current horizontally scrolled "
            "reading tables clip the first-column left edge; explicit sideways-scroll hint and linked examples "
            "remain visible. On question shows リョウ and three distinct alternatives; meaning feedback marks "
            "colleague correct. Drawing feedback visibly has 14 numbered reference strokes, ungraded practice "
            "and model-unavailable qualification. This was touch-injected reference geometry, not human "
            "handwriting or MLKit acceptance. Other33 PNGs not directly inspected."
        ),
        "independentPostrunVerification": postrun,
        "sharedResourceQualification": "Preexisting emulator5556 inventory unchanged. Owned parent4276/QEMU25352 absent; no listeners. OS PID0 TIME_WAIT preserved, not killed or claimed empty ports.",
        "nativeAcceptance": True, "independentVisualAcceptance": False, "phoneEvidence": False,
        "accepted425AndroidRetainedWithoutRerun": True, "runtimeEditsMade": False,
        "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 92, "remainingAdditions": 1136, "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None, "recordedAt": datetime.now(timezone.utc).isoformat(),
        "limits": "Native emulator assertions plus eight direct coordinator PNG inspections only. Synthetic unique source/HEAD, full production import once with unchanged guards/heaps/fonts. No owner progress, complete-PNG/independent visual/physical-phone acceptance, fallback-face identification, MLKit or human recall. Textual424/Android425 inherited unchanged, not rerun. Historical permission denials/HOST OOMs retained. Latest-main publication and whole-set acceptance outstanding.",
    }
    save(RECORD, record)
    batch_path = ROOT / r"docs\n1-sources\batch-066-progress.json"
    batch = load(batch_path)
    batch["status"] = record["status"]
    batch["nativeExecutionCheckpoint"] = {
        "execution": 427, "record": "execution-427.json", "terminalSuccessCases": 2,
        "nativePassed": True, "independentPostrunVerification": True,
        "independentVisualAcceptance": False, "publicationAttempted": False, "limits": record["limits"],
    }
    save(batch_path, batch)
    verify(record)
    print(f"Archived both passing cases and {png_count} PNGs; next gate is original-session visual confirmation.")
elif mode == "checkpoint":
    record = load(RECORD)
    verify(record)
    signed_head = git("rev-parse", "HEAD")
    assert signed_head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    before = load(CONTROL / "execution-427-before-progress.json")
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    assert progress["checkpoint"] == 426 and progress["batch"] == "066"
    summary = {
        "execution": 427, "checkpoint": 427, "batch": "066", "savedCommit": signed_head,
        "signature": "G", "record": r"docs\n1-sources\execution-427.json",
        "recordSha256": sha(RECORD), "status": "continue", "nativePassed": True,
        "terminalSuccessCases": 2, "independentPostrunVerification": True,
        "independentVisualAcceptance": False, "runtimePublished": False,
        "allOriginalHistoricalKeysPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=427, status="continue",
                    stage="batch-066-native-passed-awaiting-independent-visual-confirmation",
                    nextAction=NEXT, blocker=None)
    progress["execution427StartingState"]["status"] = "signed-native-execution-checkpoint-complete"
    progress["batch066NativeExecutionCheckpoint"] = summary
    progress["execution427CoordinatorCheckpoint"] = summary
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    temporary = CONTROL / "execution-427-progress.tmp"
    save(temporary, progress)
    temporary.replace(progress_path)
    save(CONTROL / "execution-427-checkpoint.json", summary)
    body = (
        f"Batch 066 native checkpoint **427** saved locally at signed `{signed_head}`; runtime publication has not occurred.\n\n"
        "Both named glyph/article cases returned terminal **0**, no skips, in **93.971 s**. "
        "The exact full `175fdf3f` Git envelope imported once through production ContentSync: "
        "**1,078 kanji / 5,036 words / 98 N1**, version `a9ecc100b6c1335c`, zero problems, parser epoch1. "
        "Full/Lite リョウ and empty kun preserved; sole curated `りょう` Good grade persisted with no kun log. "
        "Both mapped pairs (four directions), complete three-article semantics, offline/System Back/N1 selection/"
        "meaning, fourteen reference touch strokes, ungraded trace and persisted drawing miss pass.\n\n"
        "**36 individual glyph / 4 whole-word raster probes** pass; **41 original PNGs** archived, "
        "**eight directly inspected**. Four production rows visibly distinguish 僚/療/像/値 and render "
        "人/亻/疒/同/口/同僚. Example/attachment/rank text wraps legibly. Horizontally scrolled reading tables "
        "clip the first-column edge in those captures, retaining the explicit scroll hint and linked examples. "
        "No complete-PNG/independent visual/physical-phone acceptance, fallback-face identification, MLKit or human handwriting is inferred.\n\n"
        "Owned emulator parent4276/QEMU25352 stopped; independent postrun verifies no owned PIDs/listeners, "
        "unchanged emulator5556 and clean worktrees. OS TIME_WAIT preserved. Accepted425 Android3+1 and "
        "424 textual closure inherited without rerun; historical permission/HOST OOM evidence retained. "
        "HOST-only memory init was not used for native work.\n\n"
        "**Next:** original Claude/GPT sessions, serial bounded dependent visual confirmation, then latest-main "
        "integration and all publication gates. No reviewers, push or batch067 here. "
        "**92/1,228 published; 1,136 remaining.** Compatible Android `f9b59a2`+ required; "
        "phone/general-release/whole-set acceptance outstanding."
    )
    (CONTROL / "execution-427-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
else:
    raise ValueError(mode)
