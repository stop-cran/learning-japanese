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
FOLDER = ROOT / r"docs\n1-reviews\batch-065-native"
HEAD = "82a2c26c9d7541f93786ab3a7722d10ca557e98c"
NEXT = (
    "SAME065 native checkpoint419: both named cases actually passed terminal0/no skips/"
    "148.883s; exact full ee672744 archive through production ContentSync ONCE, "
    "1077kanji/5036words/97N1/contentVersion6a940651167e0e94/problems0/epoch1. "
    "Read docs/n1-sources/execution-419.json and batch-065-native/execution-419-artifact-index.json "
    "with exact attempt-1 PNGs/rawlogs and postrun receipts. Full/Lite ordered ケン/"
    "[つま.しい,つづまやか], curated ケン/つま.しい and normalizedけん/つましい, both "
    "persisted Good grades/no source-only log; all3mapped pairs倹-倹約/約-倹約/倹-倹しい "
    "in6directions and倹約-倹しい comparison in2directions, four complete articles/"
    "SystemBack/offline/N1selection/meaning/10reference-stroke touch/ungradedtrace/"
    "recallmiss/persistedDrawAgain.48singlePaint+8wordraster probes;60PNGs archived "
    "with4direct coordinator image inspections only. Four production font rows readable "
    "倹儉険験値人亻阝馬約糸勺/倹約/倹しい; attachment explanations and source-only "
    "table readable, first-column left edge clipped at horizontal scroll position. "
    "No fallback-face/MLKit/humanrecall/phone or complete-PNG acceptance. Owned parent21240/"
    "QEMU5416 stopped, preexistingemulator5556 retained, dedicated worktrees clean. "
    "Independent postrun has no owned processes/listeners; sharedADB9520 SYN probes and "
    "OS TIME_WAIT preserved, not claimed empty ports. Next bounded checkpoint: ORIGINAL "
    "Claude9555ba9e-42a2-497b-b221-dff6587e98e0 then GPT491afc55-0d7d-42d1-aef9-3d2f6681b28b "
    "SERIAL bounded dependent visual confirmations with scoped--add-dir control and "
    "actual CLI/catalog/process/preflight checks, honest image/read-depth/source/citation "
    "limits; do not rerun passed native or accepted417 freshAndroid3+1 absentnewconcern. "
    "Preserve45c275e7teaching/ae36905btextualclosure/original reports and qualified "
    "HOST-only2GiB init for future full-repo HOST gates, NEVER native builds; original416 "
    "denial/actual1GiBOOM/prior049512MiBfailure retained. Then freshlatestmain nonrewriting "
    "integration/allcombined source-baseline-reading-link-font-stroke/Python/vocab/"
    "validator/freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "normal signing/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIP"
    "runtimehash/terminalreceipts/ownerissue60 BEFOREdelivery or066. Actualpermissiondenial "
    "or signingwait: preserve exact command/error, report/yield; no retry/workaround. "
    "No secondrunner/concurrentheavywork/supervisorchanges; preserveFULLlivehistory. "
    "Published91/1228,1137remain/latest0640fe60920; localdraft92 NOTdelivered. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set "
    "outstanding. Overallproject incomplete."
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
    assert not git("diff", record["reviewedTeachingSnapshot"], "--", "kanji", "words", "articles", "strokes", "manifest.json")
    compiled = load(ROOT / r"docs\n1-sources\execution-418.json")
    for relative, expected in compiled["originalReportHashesUnchanged"].items():
        assert sha(ROOT / relative) == expected, relative
    android = CONTROL.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", cwd=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", cwd=android)
    print(f"Verified {len(index['files'])} evidence hashes; runtime and original reports unchanged.")


mode = sys.argv[1] if len(sys.argv) > 1 else "archive"
if mode == "archive":
    assert git("rev-parse", "HEAD") == HEAD
    receipt = load(CONTROL / "batch-065-native-attempt-1-execution.json")
    assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
    assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert receipt["prelaunch"]["connections"] == []
    assert receipt["parentEmulatorPid"] == 21240 and receipt["qemuPid"] == 5416
    assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
    source = CONTROL / r"artifacts\batch-065-native-attempt-1"
    raw = (source / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "OK (2 tests)" in raw and "Time: 148.883" in raw
    for kind, method in (
        ("Glyph", "frugalityLookalikesOlderFormAndRadicalsAcrossFourProductionFamilies"),
        ("Article", "fullSingleImportOfflineFrugalityThreePairsBothCuratedReadingsDrawingAndSystemBack"),
    ):
        assert raw.count(f"INSTRUMENTATION_STATUS: class=io.github.stopcran.kanji.ui.N1Batch065{kind}Test") == 2
        assert raw.count(f"INSTRUMENTATION_STATUS: test={method}") == 2
    compiled = load(ROOT / r"docs\n1-sources\execution-418.json")
    for item in compiled["artifacts"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    for name in ("fixture", "archive"):
        assert sha(Path(compiled[name])) == compiled[f"{name}Sha256"]
    for name in ("testApk", "appApk"):
        assert sha(Path(receipt[name])) == receipt[f"{name}Sha256"]
    route = load(source / "n1-065-article-route.json")
    assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch", "archiveRequests")] == [1077, 5036, 97, 0, 1, 1]
    assert route["contentVersion"] == "6a940651167e0e94"
    assert route["contentSnapshot"] == compiled["startingHead"]
    assert route["fullOnyomi"] == ["ケン"] and route["fullKunyomi"] == ["つま.しい", "つづまやか"]
    assert route["quizOnKeys"] == ["けん"] and route["quizKunKeys"] == ["つましい"]
    for key in ("passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback", "bothCuratedReadingsAndPersistedGrades", "drawingTraceThenRecall", "drawingGradeRecordedOnNext", "offline"):
        assert route[key] is True, key
    assert route["touchInjectedReferenceStrokes"] == 10 and route["phoneEvidence"] is False
    raster = load(source / "n1-065-font-raster.json")
    assert raster["individualGlyphProbes"] == 48 and raster["wholeWordRasterProbes"] == 8 and len(raster["rows"]) == 56
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        glyphs = [row for row in raster["rows"] if row["font"] == font and "character" in row]
        assert {row["character"] for row in glyphs} == set("倹儉険験値人亻阝馬約糸勺")
        assert all(row["hasGlyph"] for row in glyphs)
        assert len({row["nativePaintRasterSha256"] for row in glyphs}) == 12
        words = [row for row in raster["rows"] if row["font"] == font and "word" in row]
        assert {row["word"] for row in words} == {"倹約", "倹しい"}
        assert all(row["renderedCharactersNonblank"] == len(row["word"]) for row in words)
    postrun = load(CONTROL / "execution-419-postrun-verification.json")
    settlement = load(CONTROL / "execution-419-port-settlement.json")
    assert postrun["contentHead"] == HEAD and postrun["contentStatus"] == [] and postrun["androidStatus"] == []
    assert postrun["ownedProcessesRemaining"] == 0 and settlement["ownedProcessesRemaining"] == 0 and settlement["listeners"] == 0
    assert postrun["devices"] == receipt["prelaunch"]["devices"]
    assert all(connection["State"] in ("SynSent", "TimeWait") for connection in settlement["connections"])
    destination = FOLDER / "attempt-1"
    assert not destination.exists()
    destination.mkdir()
    expected_files = set(receipt["artifacts"]) | {"N1Batch065NativeTest.kt", "adb-operations.txt", "emulator-stderr.txt", "emulator-stdout.txt", "execution.json", "instrumentation.txt"}
    assert {path.name for path in source.iterdir()} == expected_files
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
    for name in ("run-419-native.ps1", "start-419.py", "archive-419-native.py", "execution-419-start.json", "execution-419-postrun-verification.json", "execution-419-port-settlement.json"):
        copy(CONTROL / name, receipts / name)
    images = ["n1-065-font-pairs.png", "n1-065-thrift-attachment.png", "n1-065-modest-attachment.png", "n1-065-kanji-source-only.png"]
    png_count = sum("dimensions" in entry for entry in artifacts)
    assert png_count == 60, png_count
    index_path = FOLDER / "execution-419-artifact-index.json"
    save(index_path, {
        "schemaVersion": 1, "execution": 419, "batch": "065", "attempt": 1, "files": artifacts,
        "sourcePngCount": png_count, "directCoordinatorImageRequests": images,
        "limits": "Four direct coordinator PNG inspections only. Other56 PNGs archived but not visually inspected. Exact bytes/hashes and native assertions do not establish complete readability or independent visual acceptance.",
    })
    record = {
        "schemaVersion": 1, "execution": 419, "checkpoint": 419, "batch": "065",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingHead": HEAD, "reviewedTeachingSnapshot": compiled["reviewedTeachingSnapshot"],
        "authorization": load(CONTROL / "execution-419-start.json")["authorization"],
        "scope": load(CONTROL / "execution-419-start.json")["scope"],
        "nativeExecution": receipt, "nativeRouteEvidence": route,
        "artifactIndex": str(index_path.relative_to(ROOT)), "artifactIndexSha256": sha(index_path),
        "sourcePngCount": png_count, "directCoordinatorImageRequests": images,
        "visualObservations": "All12 glyphs and both support words readable in four production font rows; older儉 and 倹/険/験/値 remain distinguishable. 勺 wraps to the next line in every row, but neither support word splits. Thrift and modest-living attachment paragraphs wrap legibly, including typed kana examples, translations and component links. Source-only explanation and curation warning visible and readable; current horizontal table scroll clips first-column left edge while the scroll hint remains visible. Other56 screenshots and full viewport sequence not visually inspected; fallback face not identified.",
        "independentPostrunVerification": postrun, "portSettlement": settlement,
        "sharedResourceQualification": "Preexisting emulator5556 unchanged in adb inventory. Both owned PIDs gone, no listeners. Shared adb PID9520 retains outbound SynSent probes; OS PID0 retains TimeWait. Neither touched; not a claim of entirely empty local/remote ports.",
        "nativeAcceptance": True, "independentVisualAcceptance": False, "phoneEvidence": False,
        "accepted417AndroidRetainedWithoutRerun": True, "runtimeEditsMade": False,
        "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 91, "remainingAdditions": 1137, "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None, "recordedAt": datetime.now(timezone.utc).isoformat(),
        "limits": "Native emulator assertions and four direct coordinator PNG inspections only. Synthetic unique source/HEAD, production full import once with unchanged guards/heaps/fonts. No owner progress, independent visual or physical-phone acceptance, MLKit recognition or human recall claimed. Textual reviews/417 qualified HOST checks retained, not rerun. Original416 permission denial/actual1GiB OOM/prior049512MiB history remains. Combined-main publication and whole-set acceptance outstanding.",
    }
    save(ROOT / r"docs\n1-sources\execution-419.json", record)
    batch_path = ROOT / r"docs\n1-sources\batch-065-progress.json"
    batch = load(batch_path)
    batch["status"] = record["status"]
    batch["nativeExecutionCheckpoint"] = {
        "execution": 419, "record": "execution-419.json", "terminalSuccessCases": 2,
        "nativePassed": True, "independentPostrunVerification": True,
        "independentVisualAcceptance": False, "publicationAttempted": False,
        "limits": record["limits"],
    }
    save(batch_path, batch)
    verify(record)
    print(f"Archived native result and {png_count} original PNGs; next gate is original-session visual confirmation.")
elif mode == "checkpoint":
    record = load(ROOT / r"docs\n1-sources\execution-419.json")
    verify(record)
    signed_head = git("rev-parse", "HEAD")
    assert signed_head != HEAD and git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    before = load(CONTROL / "execution-419-before-progress.json")
    progress_path = CONTROL / "progress.json"
    progress = load(progress_path)
    assert progress["checkpoint"] == 418 and progress["batch"] == "065"
    summary = {
        "execution": 419, "checkpoint": 419, "batch": "065", "savedCommit": signed_head,
        "signature": "G", "record": r"docs\n1-sources\execution-419.json",
        "recordSha256": sha(ROOT / r"docs\n1-sources\execution-419.json"),
        "status": "continue", "nativePassed": True, "terminalSuccessCases": 2,
        "independentPostrunVerification": True, "independentVisualAcceptance": False,
        "runtimePublished": False, "allOriginalHistoricalKeysPreservedExactly": True,
        "nextAction": NEXT,
    }
    progress.update(checkpoint=419, status="continue", stage="batch-065-native-passed-awaiting-independent-visual-confirmation", nextAction=NEXT, blocker=None)
    progress["execution419StartingState"]["status"] = "signed-native-execution-checkpoint-complete"
    progress["batch065NativeExecutionCheckpoint"] = summary
    progress["execution419CoordinatorCheckpoint"] = summary
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    temporary = CONTROL / "execution-419-progress.tmp"
    save(temporary, progress)
    temporary.replace(progress_path)
    save(CONTROL / "execution-419-checkpoint.json", summary)
    body = (
        f"Batch 065 native checkpoint **419** saved locally at signed `{signed_head}`; runtime publication has not occurred.\n\n"
        "Both named glyph/article cases returned terminal **0**, no skips, in **148.883 s**. Exact full `ee672744` Git archive imported once through production ContentSync: **1,077 kanji / 5,036 words / 97 N1**, version `6a940651167e0e94`, zero problems, parser epoch1. Full/Lite source readings remain; only curated `けん` / `つましい` are offered, with both Good grades persisted and no source-only log. All three mapped pairs (six directions), both support-comparison directions, four complete-article semantics, offline/System Back/meaning and ten reference touch strokes/ungraded trace/persisted drawing miss pass.\n\n"
        "**48 individual glyph / 8 whole-word raster probes** pass; **60 original PNGs** archived, only **four directly inspected** by the coordinator. Four production font rows distinguish 倹/儉/険/験/値 and render radicals and both support words; support attachment explanations and the source-only warning are legible. The horizontally scrolled table's first-column edge is clipped in that capture, with its scroll hint visible. No complete-PNG/independent visual/physical-phone acceptance, fallback-face identification, MLKit or correct human recall is inferred.\n\n"
        "Owned emulator parent21240/QEMU5416 stopped; independent postrun checks retain the preexisting emulator5556, clean worktrees and no owned PIDs/listeners. Shared adb outbound SYN probes and OS TIME_WAIT are preserved, not killed or called empty ports. Accepted417 qualified HOST3+1 and original416 denial/1GiB OOM/049512MiB history retained without rerun. HOST-only2GiB init is never for native builds.\n\n"
        "**Next:** original Claude/GPT sessions, serial bounded dependent visual confirmation, then latest-main integration and all publication gates. No reviewer, push or batch066 here. **91/1,228 published; 1,137 remaining.** Compatible Android `f9b59a2`+ required; phone/general-release/whole-set acceptance outstanding."
    )
    (CONTROL / "execution-419-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
else:
    assert mode == "verify"
    verify(load(ROOT / r"docs\n1-sources\execution-419.json"))
