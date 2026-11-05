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
HEAD = "27a65d2fa6e711d4e23f17c2c485f044d3aef848"
FOLDER = ROOT / r"docs\n1-reviews\batch-070-native"
RECORD = ROOT / r"docs\n1-sources\execution-461.json"
IMAGES = [
    "n1-070-font-pairs.png", "n1-070-kanji-11.png", "n1-070-word1-04.png",
    "n1-070-word2-09.png", "n1-070-comparison-11.png", "n1-070-component1-19.png",
    "n1-070-curated-On-question.png", "n1-070-curated-Kun-question.png",
    "n1-070-drawing-feedback.png", "n1-070-meaning-feedback.png",
]
NEXT = (
    "SAME070: native checkpoint461 passed BOTH named cases terminal0/no skips in178.905s. "
    "Read docs\\n1-sources\\execution-461.json and batch-070-native\\execution-461-artifact-index.json. "
    "Exact signed fce81d63 full Git envelope through ContentSync ONCE:1082kanji5040words102N1/"
    "versiona9867cc4b455639a/problems0/epoch1; Full+Lite full/curatedショウ,つぐな.う;"
    "normalizedしょう,つぐなう and both Good grades persisted. All five article projections/"
    "three mapped reciprocal pairs six directions plus補-補う reciprocal and補う-to補償 comparison/"
    "SystemBack/offline/N1selection/meaning/17reference-touch-strokes/ungradedtrace/recallmiss/"
    "persistedDrawAgain pass. 88singlePaint+12wordRaster probes/75originalPNGs archived; "
    "ten direct coordinator PNG inspections only, not complete-PNG/independent/phone acceptance. "
    "Four production rows readable償賞儀僧億人亻補衣衤礻甫捕手扌初複保証埋損害 and償う補償補う; "
    "reading table left edge clipped at current horizontal offset with explicit scroll hint. "
    "Owned parent17652/QEMU9972 stopped, unchanged preexisting5556 and clean worktrees; "
    "transient sharedADB9520 reconnect and OS TIME_WAIT preserved, no shared process killed. "
    "Next bounded checkpoint ORIGINAL Claude5ace375a-4747-4cb8-be76-486c1a778e45 THEN "
    "GPT5424a79d-80be-4124-ba8b-fb09e2be95c2 SERIAL bounded dependent visual confirmations "
    "using supported CLI/read-only controls and actual PNGs/route/fixture/source excerpts. "
    "Record actual returned image/read coverage and limits; not new blind initial reviews. "
    "Do not rerun passing native or459Android3+1 absent new concern. Qualified HOST2GiB init "
    "NEVER native; original heaps/guards unchanged. Then freshlatestmain nonrewriting integration/"
    "allcombined validation/normal signing/ownerfastforward/publicSHA/terminalgreenCI/"
    "everyimmutablepublicZIPruntimehash+originalbudgets/ownerissue60 BEFOREdelivery or071. "
    "No secondrunner/supervisor edits/permission bypass/signing workaround. Published96/1228,"
    "remaining1132;070 local NOTdelivered. CompatibleAndroidf9b59a2+ required; "
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
    compiled = load(ROOT / r"docs\n1-sources\execution-460.json")
    for entry in compiled["originalReportsUnchanged"].values():
        assert sha(ROOT / r"docs\n1-reviews" / entry["report"]) == entry["sha256"]
    android = CONTROL.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", cwd=android) == record["nativeExecution"]["androidSnapshot"]
    assert not git("status", "--porcelain", cwd=android)
    print(f"Verified {len(load(index)['files'])} evidence hashes and unchanged runtime/original reports.")


mode = sys.argv[1]
if mode == "archive":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    receipt = load(CONTROL / "batch-070-native-attempt-1-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert receipt["prelaunch"]["connections"] == []
    assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
    source = CONTROL / r"artifacts\batch-070-native-attempt-1"
    raw = (source / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "OK (2 tests)" in raw and "Time: 178.905" in raw
    for kind, method in (
        ("Article", "fullSingleImportOfflineRecompenseThreeReciprocalPairsBothReadingsDrawingAndSystemBack"),
        ("Glyph", "recompenseLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
    ):
        assert raw.count(f"INSTRUMENTATION_STATUS: class=io.github.stopcran.kanji.ui.N1Batch070{kind}Test") == 2
        assert raw.count(f"INSTRUMENTATION_STATUS: test={method}") == 2
    compiled = load(ROOT / r"docs\n1-sources\execution-460.json")
    prep = load(ROOT / r"docs\n1-sources\batch-070-native-preparation.json")
    for entry in compiled["artifacts"]:
        assert sha(ROOT / entry["path"]) == entry["sha256"]
    assert sha(Path(prep["archive"])) == prep["archiveSha256"] == receipt["archiveSha256"]
    assert sha(Path(prep["fixture"])) == prep["fixtureSha256"] == receipt["fixtureSha256"]
    for name in ("testApk", "appApk"):
        assert sha(Path(receipt[name])) == receipt[f"{name}Sha256"]
    route = load(source / "n1-070-article-route.json")
    assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems",
                                  "acceptedReadingParserEpoch", "archiveRequests")] == [1082, 5040, 102, 0, 1, 1]
    assert route["contentVersion"] == prep["contentVersion"]
    assert route["contentSnapshot"] == prep["contentSnapshot"]
    assert route["fullOnyomi"] == ["ショウ"] and route["fullKunyomi"] == ["つぐな.う"]
    assert route["quizOnKeys"] == ["しょう"] and route["quizKunKeys"] == ["つぐなう"]
    for key in ("passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "bothCuratedKindsAndPersistedGrades", "drawingTraceThenRecall",
                "drawingGradeRecordedOnNext", "offline"):
        assert route[key] is True, key
    assert route["touchInjectedReferenceStrokes"] == 17 and route["phoneEvidence"] is False
    raster = load(source / "n1-070-font-raster.json")
    assert raster["individualGlyphProbes"] == 88 and raster["wholeWordRasterProbes"] == 12
    assert len(raster["rows"]) == 100
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
        assert {row["character"] for row in glyphs} == set(prep["plannedGlyphs"])
        assert all(row["hasGlyph"] for row in glyphs)
        assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 22
        words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
        assert {row["word"] for row in words} == set(prep["plannedWholeWords"])
        assert all(row["renderedCharactersNonblank"] == len(row["word"]) for row in words)
    postrun = load(CONTROL / "execution-461-postrun-verification.json")
    observation = load(CONTROL / "execution-461-postrun-connection-observation.json")
    assert postrun["contentHead"] == HEAD and postrun["contentStatus"] == [] and postrun["androidStatus"] == []
    assert postrun["ownedProcessesRemaining"] == 0
    assert postrun["devices"] == receipt["prelaunch"]["devices"]
    assert not any(c["State"] == 2 for c in postrun["connections"])
    assert observation["observedRemainingConnectionOwner"]["Name"] == "adb.exe"
    assert all(c["State"] == 11 and c["OwningProcess"] == 0 for c in observation["connections"])
    destination = FOLDER / "attempt-1"
    assert not destination.exists()
    destination.mkdir()
    expected = set(receipt["artifacts"]) | {
        "N1Batch070NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt",
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
    for name in ("run-461-native.ps1", "start-461.py", "archive-461-native.py",
                 "execution-461-postrun-verification.json", "execution-461-postrun-connection-observation.json"):
        copy(CONTROL / name, receipts / name)
    png_count = sum("dimensions" in entry for entry in artifacts)
    assert png_count == 75
    assert set(IMAGES) <= {path.name for path in source.iterdir()}
    index_path = FOLDER / "execution-461-artifact-index.json"
    save(index_path, {
        "schemaVersion": 1, "execution": 461, "batch": "070", "attempt": 1,
        "files": artifacts, "sourcePngCount": png_count, "directCoordinatorImageRequests": IMAGES,
        "limits": "Ten direct coordinator PNG inspections. Other65 archived PNGs not visually inspected by coordinator. Hashes/assertions do not establish complete readability or independent visual acceptance.",
    })
    progress = load(CONTROL / "progress.json")
    record = {
        "schemaVersion": 1, "execution": 461, "checkpoint": 461, "batch": "070",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingHead": HEAD, "reviewedTeachingSnapshot": compiled["reviewedTeachingSnapshot"],
        "authorization": progress["execution461StartingState"]["authorization"],
        "scope": progress["execution461StartingState"]["scope"],
        "nativeExecution": receipt, "nativeRouteEvidence": route,
        "artifactIndex": str(index_path.relative_to(ROOT)), "artifactIndexSha256": sha(index_path),
        "sourcePngCount": png_count, "directCoordinatorImageRequests": IMAGES,
        "visualObservations": (
            "All22 individual characters and all3 whole words visibly readable in four production font rows. "
            "償 versus 賞 has the extra person-side component; 儀/僧/億 right-hand shapes differ. "
            "人/standalone亻 and 衣/衤/礻, 甫, 捕/手/扌, 初/複 and remaining comparison characters render "
            "without blank/replacement boxes; actual fallback faces not identified. New 償う examples/forms "
            "and 補償 scope/comparison paragraphs wrap legibly; new 補 backlink and changed 補う comparison "
            "are visible with target links. At the captured horizontal table offset the first-column left edge "
            "is clipped, with explicit sideways-scroll hint and linked examples retained. On/Kun questions "
            "show distinct readable choices including ショウ/つぐなう; meaning feedback marks recompense "
            "correct. Drawing feedback visibly has17 numbered reference strokes, ungraded practice and "
            "model-unavailable qualification. This was touch-injected reference geometry, not human "
            "handwriting or MLKit acceptance. Other65 PNGs not directly inspected."
        ),
        "postrunVerification": postrun, "postrunConnectionObservation": observation,
        "sharedResourceQualification": "Preexisting emulator5556 inventory unchanged. Owned parent17652/QEMU9972 absent; no listeners. Transient sharedADB9520 reconnect and OS PID0 TIME_WAIT preserved; shared ADB server not killed, ports not falsely claimed empty.",
        "nativeAcceptance": True, "independentVisualAcceptance": False, "phoneEvidence": False,
        "accepted459AndroidRetainedWithoutRerun": True, "runtimeEditsMade": False,
        "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 96, "remainingAdditions": 1132, "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None, "recordedAt": datetime.now().astimezone().isoformat(),
        "limits": "Native emulator assertions plus ten direct coordinator PNG inspections only. Synthetic unique source/HEAD, full production import once with unchanged guards/heaps/fonts. No owner progress, complete-PNG/independent visual/physical-phone acceptance, fallback-face identification, MLKit or human recall. Textual458/Android459 inherited unchanged, not rerun. Historical permission denials/HOST OOMs retained. Latest-main publication and whole-set acceptance outstanding.",
    }
    assert not RECORD.exists()
    save(RECORD, record)
    batch_path = ROOT / r"docs\n1-sources\batch-070-progress.json"
    batch = load(batch_path)
    batch["status"] = record["status"]
    batch["nextAction"] = NEXT
    batch["nativeExecutionCheckpoint"] = {
        "execution": 461, "record": "execution-461.json", "terminalSuccessCases": 2,
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
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    before = json.loads(json.dumps(progress))
    assert progress["checkpoint"] == 460 and progress["batch"] == "070"
    summary = {
        "execution": 461, "checkpoint": 461, "batch": "070", "savedCommit": signed_head,
        "signature": "G", "record": r"docs\n1-sources\execution-461.json",
        "recordSha256": sha(RECORD), "status": "continue", "nativePassed": True,
        "terminalSuccessCases": 2, "independentPostrunVerification": True,
        "independentVisualAcceptance": False, "runtimePublished": False,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=461, status="continue",
                    stage="batch-070-native-passed-awaiting-independent-visual-confirmation",
                    nextAction=NEXT, blocker=None)
    progress["execution461StartingState"]["status"] = "signed-native-execution-checkpoint-complete"
    progress["batch070NativeExecutionCheckpoint"] = summary
    progress["execution461CoordinatorCheckpoint"] = summary
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker", "execution461StartingState"}:
        assert progress[key] == before[key], key
    temporary = CONTROL / "execution-461-progress.tmp"
    save(temporary, progress)
    temporary.replace(progress_path)
    save(CONTROL / "execution-461-checkpoint.json", summary)
    body = (
        f"Batch 070 native checkpoint **461** saved locally at signed `{signed_head}`; runtime publication has not occurred.\n\n"
        "Both named glyph/article cases returned terminal **0**, no skips, in **178.905 s**. "
        "The exact full `fce81d63` Git envelope imported once through production ContentSync: "
        "**1,082 kanji / 5,040 words / 102 N1**, version `a9867cc4b455639a`, zero problems, parser epoch1. "
        "Full/Lite ショウ and つぐな.う preserved; curated `しょう`/`つぐなう` Good grades persisted. "
        "Three mapped pairs (six directions), 補/補う reciprocal and 補う→補償 comparison, five article projections, "
        "offline/System Back/N1 selection/meaning, seventeen reference touch strokes, ungraded trace and persisted drawing miss pass.\n\n"
        "**88 individual glyph / 12 whole-word raster probes** pass; **75 original PNGs** archived, "
        "**ten directly inspected**. Four production rows visibly distinguish 償/賞/儀/僧/億 and render "
        "人/亻/補/衣/衤/礻/甫/捕/手/扌/初/複/保/証/埋/損/害 plus 償う/補償/補う. "
        "Changed passages and examples wrap legibly. Horizontally scrolled reading tables clip the first-column edge "
        "in those captures, retaining the explicit scroll hint and linked examples. "
        "No complete-PNG/independent visual/physical-phone acceptance, fallback-face identification, MLKit or human handwriting is inferred.\n\n"
        "Owned emulator parent17652/QEMU9972 stopped; postrun verifies no owned PIDs/listeners, unchanged emulator5556 "
        "and clean worktrees. Transient sharedADB9520 reconnect and OS TIME_WAIT preserved without killing shared processes. "
        "Accepted459 Android3+1 and458 textual closure inherited without rerun; historical permission/HOST OOM evidence retained. "
        "HOST-only memory init was not used for native work.\n\n"
        "**Next:** original Claude/GPT sessions, serial bounded dependent visual confirmation, then latest-main integration "
        "and all publication gates. No reviewers, push or batch071 here. "
        "**96/1,228 published; 1,132 remaining.** Compatible Android `f9b59a2`+ required; "
        "phone/general-release/whole-set acceptance outstanding."
    )
    (CONTROL / "execution-461-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
else:
    raise ValueError(mode)
