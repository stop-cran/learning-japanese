import hashlib
import gzip
import json
import re
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
LOG = CONTROL / r"logs\7d577d59-f228-461b-b5b9-1c723f44a5a7"
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / r"docs\n1-reviews\batch-067-native"
RECORD = ROOT / r"docs\n1-sources\execution-435.json"
HEAD = "923eb205bae2fafe146145a06955b8467c5c14cd"
IMAGES = [
    "n1-067-font-pairs.png",
    "n1-067-kanji-on-reading.png",
    "n1-067-clergy-reading-allocation.png",
    "n1-067-bousan-changed-comparison.png",
    "n1-067-curated-On-question.png",
    "n1-067-drawing-feedback.png",
    "n1-067-bousan-directions-example.png",
    "n1-067-meaning-feedback.png",
]
NEXT = (
    "SAME067 native checkpoint435: both named Glyph/Article cases terminal0/no skips/"
    "138.141s. Read docs\\n1-sources\\execution-435.json and batch-067-native\\"
    "execution-435-artifact-index.json; all original PNGs/raw logs archived, eight direct "
    "coordinator images inspected, not complete-PNG acceptance. Exact full signed a45ce301 "
    "Git envelope imported through production ContentSync ONCE:1079kanji5037words99N1/"
    "68c767f176e68882/problems0/epoch1. Full+Liteソウ/emptyKun; sole normalizedそう "
    "Good persisted/noKunLog. One mapped僧-僧侶 reciprocal pair and both僧侶-坊さん comparison "
    "directions, complete3article semantics/SystemBack/offline/N1selection/meaning/"
    "13reference-stroke touch/ungradedtrace/recallmiss/persistedDrawAgain.32singlePaint+"
    "8wholewordraster probes pass; four production rows visibly readable僧増値倍人亻曽侶/"
    "僧侶/坊さん. Article text wraps legibly; first-column left edge clipped at current "
    "horizontal reading-table offset with explicit scroll hint. No fallback-face identity/"
    "MLKit/humanhandwriting/physicalphone acceptance. Owned parent14572/QEMU15716 stopped; "
    "preexistingemulator5556 unchanged, clean worktrees, no owned PIDs/listeners; postrun "
    "OS TIME_WAIT preserved. Next bounded checkpoint: ORIGINAL "
    "Claude0d237a1b-fdf8-4ea8-8c5d-03aa6a6d86a0 then "
    "GPTab7f642d-37b9-4069-8a9c-4fc5e6bc071a SERIAL bounded dependent visual confirmations "
    "using actual supported CLI/read-only controls/scoped control access. Record actual "
    "returned image/read-depth/source limits, not fresh blind reviews. Do not rerun passed "
    "native or accepted433Android3+1 absentnewconcern; qualified HOST-only heap init NEVER "
    "native builds. Preserve original denials/OOMs/432 textual closure/reports and full "
    "livehistory. Then freshlatestmain nonrewriting integration/allcombined source-"
    "baseline-reading-link-font-stroke/Python/vocab/validator/freshmanifest/original "
    "18000entries42MiBcompressed80MiBinflated56MiBretained budgets/normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/"
    "ownerissue60 BEFOREdelivery or068. Permissiondenial/signingwait: preserve exact "
    "command/error and yield; no workaround, secondrunner, concurrentheavywork or "
    "supervisorchanges. Published93/1228,1135remain/latest066f0b318eb; local067 NOTdelivered. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
    "Overallproject incomplete."
)


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
    compiled = load(ROOT / r"docs\n1-sources\execution-434.json")
    for relative, expected in compiled["originalReportHashesUnchanged"].items():
        assert sha(ROOT / relative) == expected
    android = CONTROL.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", cwd=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", cwd=android)
    print(f"Verified {len(index['files'])} evidence hashes; runtime and original reports unchanged.")


if sys.argv[1] == "start":
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 434 and progress["batch"] == "067"
    assert not (LOG / "execution-435-before-progress.json").exists()
    save(LOG / "execution-435-before-progress.json", progress)
    request = LOG / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    checkpoint = json.loads(text.split(marker, 1)[1])
    assert checkpoint["checkpoint"] == 434
    start = {
        "execution": 435, "batch": "067",
        "startingHead": "923eb205bae2fafe146145a06955b8467c5c14cd",
        "scope": "SAME067 compiled native execution, evidence archival, direct bounded PNG inspection and normally signed local checkpoint only. No reviewer, publication,068 or second runner.",
        "status": "native-execution-in-progress",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "authorization": {
            "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and full embedded checkpoint parsed. Operative contract, complete final434 and approved issue inspected directly; historical middle parsed, not freshly semantically re-reviewed."
        }
    }
    save(LOG / "execution-435-start.json", start)
    progress["execution435StartingState"] = start
    progress["stage"] = "batch-067-native-execution-in-progress"
    progress["nextAction"] = start["scope"]
    save(CONTROL / "progress.json", progress)
    print("Starting state persisted with complete prior history preserved.")
elif sys.argv[1] == "archive":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    receipt = load(CONTROL / "batch-067-native-attempt-1-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert receipt["prelaunch"]["connections"] == []
    assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
    source = CONTROL / r"artifacts\batch-067-native-attempt-1"
    raw = (source / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "OK (2 tests)" in raw and "Time: 138.141" in raw
    for kind, method in (
        ("Glyph", "buddhistClergyLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
        ("Article", "fullSingleImportOfflineBuddhistClergyReciprocalComparisonOnOnlyDrawingAndSystemBack"),
    ):
        assert raw.count(f"INSTRUMENTATION_STATUS: class=io.github.stopcran.kanji.ui.N1Batch067{kind}Test") == 2
        assert raw.count(f"INSTRUMENTATION_STATUS: test={method}") == 2
    compiled = load(ROOT / r"docs\n1-sources\execution-434.json")
    for item in compiled["artifacts"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    for name in ("fixture", "archive"):
        assert sha(Path(compiled[name])) == compiled[f"{name}Sha256"]
    for name in ("testApk", "appApk"):
        assert sha(Path(receipt[name])) == receipt[f"{name}Sha256"]
    route = load(source / "n1-067-article-route.json")
    assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems",
                                  "acceptedReadingParserEpoch", "archiveRequests")] == [1079, 5037, 99, 0, 1, 1]
    assert route["contentVersion"] == "68c767f176e68882"
    assert route["contentSnapshot"] == compiled["startingHead"]
    assert route["fullOnyomi"] == ["ソウ"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["そう"] and route["quizKunKeys"] == []
    for key in ("passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
                "drawingGradeRecordedOnNext", "offline"):
        assert route[key] is True, key
    assert route["touchInjectedReferenceStrokes"] == 13 and route["phoneEvidence"] is False
    raster = load(source / "n1-067-font-raster.json")
    assert raster["individualGlyphProbes"] == 32 and raster["wholeWordRasterProbes"] == 8
    assert len(raster["rows"]) == 40
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
        assert {row["character"] for row in glyphs} == set("僧増値倍人亻曽侶")
        assert all(row["hasGlyph"] for row in glyphs)
        assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 8
        words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
        assert {row["word"] for row in words} == {"僧侶", "坊さん"}
        assert all(row["renderedCharactersNonblank"] == len(row["word"]) for row in words)
    postrun = load(LOG / "execution-435-postrun-verification.json")
    assert postrun["contentHead"] == HEAD and postrun["contentStatus"] == [] and postrun["androidStatus"] == []
    assert postrun["ownedProcessesRemaining"] == 0
    assert postrun["devices"] == receipt["prelaunch"]["devices"]
    assert postrun["preexistingProcesses"] == receipt["preexistingEmulators"]
    assert all(connection["State"] == 11 and connection["OwningProcess"] == 0
               for connection in postrun["connections"])
    destination = FOLDER / "attempt-1"
    assert not destination.exists()
    expected = set(receipt["artifacts"]) | {
        "N1Batch067NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
        "emulator-stdout.txt", "execution.json", "instrumentation.txt",
    }
    assert {path.name for path in source.iterdir()} == expected
    assert set(IMAGES) <= expected
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
    for path in (
        CONTROL / "run-435-native.ps1", CONTROL / "execution-435.py",
        LOG / "execution-435-start.json", LOG / "execution-435-postrun-verification.json",
    ):
        copy(path, receipts / path.name)
    png_count = sum("dimensions" in entry for entry in artifacts)
    assert png_count == len([name for name in expected if name.endswith(".png")])
    index_path = FOLDER / "execution-435-artifact-index.json"
    save(index_path, {
        "schemaVersion": 1, "execution": 435, "batch": "067", "attempt": 1,
        "files": artifacts, "sourcePngCount": png_count, "directCoordinatorImageRequests": IMAGES,
        "limits": f"Eight direct coordinator PNG inspections. Other{png_count - 8} archived PNGs not visually inspected by coordinator. Hashes/assertions do not establish complete readability or independent visual acceptance.",
    })
    limits = (
        "Native emulator assertions plus eight direct coordinator PNG inspections only. "
        "Synthetic unique source/HEAD, full production import once with unchanged guards/heaps/fonts. "
        "No owner progress, complete-PNG/independent visual/physical-phone acceptance, fallback-face "
        "identity, MLKit or human recall. Textual432/Android433 inherited unchanged, not rerun. "
        "Historical permission denials/HOST OOMs retained. Latest-main publication and whole-set "
        "acceptance outstanding."
    )
    record = {
        "schemaVersion": 1, "execution": 435, "checkpoint": 435, "batch": "067",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingHead": HEAD, "reviewedTeachingSnapshot": compiled["reviewedTeachingSnapshot"],
        "authorization": load(LOG / "execution-435-start.json")["authorization"],
        "scope": load(LOG / "execution-435-start.json")["scope"],
        "nativeExecution": receipt, "nativeRouteEvidence": route,
        "artifactIndex": str(index_path.relative_to(ROOT)), "artifactIndexSha256": sha(index_path),
        "sourcePngCount": png_count, "directCoordinatorImageRequests": IMAGES,
        "visualObservations": (
            "All eight characters and both words are readable in four production font rows; "
            "坊さん wraps without missing characters. 僧/増 left components and 値/倍 right "
            "components are distinguishable; 人/亻 and standalone 曽/侶 visible. Actual fallback "
            "face not identified. Clergy reading allocation, singular/plural boundary, register "
            "comparison and 坊さん directions example wrap legibly with visible links. The "
            "horizontally scrolled reading table clips the first-column left edge; explicit "
            "scroll hint, linked 僧侶 example and nearby full ソウ explanation remain visible. "
            "On question shows ソウ with three distinct alternatives; meaning feedback marks "
            "Buddhist monk/priest correct. Drawing feedback visibly has 13 numbered reference "
            "strokes, ungraded practice and model-unavailable qualification. This was touch-"
            "injected reference geometry, not human handwriting or MLKit acceptance. "
            f"Other{png_count - 8} PNGs not directly inspected."
        ),
        "independentPostrunVerification": postrun,
        "sharedResourceQualification": "Preexisting emulator5556 and exact processes10668/18200 unchanged. Owned parent14572/QEMU15716 absent; no listeners. OS PID0 TIME_WAIT preserved, not killed or claimed empty ports.",
        "nativeAcceptance": True, "independentVisualAcceptance": False, "phoneEvidence": False,
        "accepted433AndroidRetainedWithoutRerun": True, "runtimeEditsMade": False,
        "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 93, "remainingAdditions": 1135, "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None, "recordedAt": datetime.now(timezone.utc).isoformat(),
        "limits": limits,
    }
    save(RECORD, record)
    batch_path = ROOT / r"docs\n1-sources\batch-067-progress.json"
    batch = load(batch_path)
    batch["status"] = record["status"]
    batch["nextAction"] = NEXT
    batch["limits"] = limits
    batch["nativeExecutionCheckpoint"] = {
        "execution": 435, "record": "execution-435.json", "terminalSuccessCases": 2,
        "nativePassed": True, "independentPostrunVerification": True,
        "independentVisualAcceptance": False, "publicationAttempted": False, "limits": limits,
    }
    save(batch_path, batch)
    verify(record)
    print(f"Archived both passing cases and {png_count} PNGs; next gate is original-session visual confirmation.")
elif sys.argv[1] == "checkpoint":
    record = load(RECORD)
    verify(record)
    signed_head = git("rev-parse", "HEAD")
    assert signed_head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    before = load(LOG / "execution-435-before-progress.json")
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    assert progress["checkpoint"] == 434 and progress["batch"] == "067"
    summary = {
        "execution": 435, "checkpoint": 435, "batch": "067", "savedCommit": signed_head,
        "signature": "G", "record": r"docs\n1-sources\execution-435.json",
        "recordSha256": sha(RECORD), "status": "continue", "nativePassed": True,
        "terminalSuccessCases": 2, "independentPostrunVerification": True,
        "independentVisualAcceptance": False, "runtimePublished": False,
        "allOriginalHistoricalKeysPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=435, status="continue",
                    stage="batch-067-native-passed-awaiting-independent-visual-confirmation",
                    nextAction=NEXT, blocker=None)
    progress["execution435StartingState"]["status"] = "signed-native-execution-checkpoint-complete"
    progress["batch067NativeExecutionCheckpoint"] = summary
    progress["execution435CoordinatorCheckpoint"] = summary
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    temporary = LOG / "execution-435-progress.tmp"
    save(temporary, progress)
    temporary.replace(progress_path)
    save(LOG / "execution-435-checkpoint.json", summary)
    body = (
        f"Batch 067 native checkpoint **435** saved locally at signed `{signed_head}`; runtime publication has not occurred.\n\n"
        "Both named glyph/article cases returned terminal **0**, no skips, in **138.141 s**. "
        "The exact full `a45ce301` Git envelope imported once through production ContentSync: "
        "**1,079 kanji / 5,037 words / 99 N1**, version `68c767f176e68882`, zero problems, parser epoch1. "
        "Full/Lite ソウ and empty kun preserved; sole curated `そう` Good grade persisted with no kun log. "
        "The 僧–僧侶 reciprocal pair and both 僧侶–坊さん comparison directions, complete three-article "
        "semantics, offline/System Back/N1 selection/meaning, thirteen reference touch strokes, "
        "ungraded trace and persisted drawing miss pass.\n\n"
        f"**32 individual glyph / 8 whole-word raster probes** pass; **{record['sourcePngCount']} original PNGs** "
        "archived, **eight directly inspected**. Four production rows visibly distinguish 僧/増/値/倍 and "
        "render 人/亻/曽/侶/僧侶/坊さん. Article examples and comparisons wrap legibly. The horizontally "
        "scrolled reading-table capture clips its first-column edge, retaining the explicit scroll hint "
        "and linked example. No complete-PNG/independent visual/physical-phone acceptance, fallback-face "
        "identity, MLKit or human handwriting is inferred.\n\n"
        "Owned emulator parent14572/QEMU15716 stopped; independent postrun verifies no owned PIDs/listeners, "
        "unchanged emulator5556/processes and clean worktrees. OS TIME_WAIT preserved. Accepted433 Android3+1 "
        "and432 textual closure inherited without rerun; historical permission/HOST OOM evidence retained. "
        "HOST-only memory init was not used for native work.\n\n"
        "**Next:** original Claude/GPT sessions, serial bounded dependent visual confirmation, then latest-main "
        "integration and all publication gates. No reviewers, push or batch068 here. "
        "**93/1,228 published; 1,135 remaining.** Compatible Android `f9b59a2`+ required; "
        "phone/general-release/whole-set acceptance outstanding."
    )
    (LOG / "issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key != "nextAction"}, indent=2))
elif sys.argv[1] == "normalize":
    record = load(RECORD)
    verify(record)
    source = CONTROL / r"artifacts\batch-067-native-attempt-1"
    destination = FOLDER / "attempt-1"
    normalizations = []
    for path in sorted(source.glob("*.txt")):
        raw = path.read_bytes()
        archive = destination / (path.name + ".raw.gz")
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        text = raw.decode("utf-8-sig")
        normalized = "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"
        target = destination / path.name
        target.write_text(normalized, encoding="utf-8", newline="\n")
        normalizations.append({
            "readablePath": str(target.relative_to(ROOT)),
            "originalSha256": sha(path),
            "readableSha256": sha(target),
            "rawArchivePath": str(archive.relative_to(ROOT)),
            "rawArchiveSha256": sha(archive),
        })
    helper_copy = FOLDER / r"execution-receipts\execution-435.py"
    shutil.copyfile(Path(__file__), helper_copy)
    index_path = ROOT / record["artifactIndex"]
    index = load(index_path)
    entries = []
    for path in sorted([*destination.iterdir(), *(FOLDER / "execution-receipts").iterdir()]):
        assert path.is_file()
        entry = {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)}
        if path.suffix == ".png":
            entry["dimensions"] = list(struct.unpack(">II", path.read_bytes()[16:24]))
        entries.append(entry)
    index["files"] = entries
    index["logNormalization"] = normalizations
    index["logNormalizationReason"] = (
        "Staged whitespace check identified trailing spaces/blank EOF in raw adb/emulator logs. "
        "Readable UTF-8 LF copies remove trailing whitespace; deterministic gzip retains every "
        "original text-log byte. Original attempt and original helper remain in control. No native rerun."
    )
    save(index_path, index)
    record["artifactIndexSha256"] = sha(index_path)
    record["artifactNormalization"] = index["logNormalizationReason"]
    save(RECORD, record)
    verify(record)
    print("Readable logs normalized; original raw bytes preserved and verified in gzip.")
elif sys.argv[1] == "verify":
    verify(load(RECORD))
else:
    raise ValueError(sys.argv[1])
