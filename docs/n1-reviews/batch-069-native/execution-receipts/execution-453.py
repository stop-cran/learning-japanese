import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CONTROL = Path(__file__).parent
CONTENT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
PROGRESS = CONTROL / "progress.json"
REQUEST = CONTROL / "logs" / "6a71d700-ec79-4e62-9644-4f790eff7082" / "request.txt"
TARGET = CONTENT / "docs" / "n1-reviews" / "batch-069-native"
SOURCE = CONTROL / "artifacts" / "batch-069-native-attempt-1"
HEAD = "e60c35c6536bdae22e18d3bba8aa4649b90a460d"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], timeout=30, encoding="utf-8").strip()


def start():
    raw = REQUEST.read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(PROGRESS)
    assert p["checkpoint"] == embedded["checkpoint"] == 452 and p["batch"] == "069"
    assert "execution453StartingState" not in p
    assert git(CONTENT, "rev-parse", "HEAD") == HEAD and not git(CONTENT, "status", "--porcelain")
    assert git(ANDROID, "rev-parse", "HEAD") == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git(ANDROID, "status", "--porcelain")
    state = {
        "execution": 453, "batch": "069", "startingHead": HEAD,
        "scope": "SAME069 compiled native execution, evidence archival, direct bounded PNG inspection and normally signed local checkpoint only. No reviewer/publication/070/second runner.",
        "status": "executing-native-checkpoint", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "authorization": {
            "requestSha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final452 checkpoint, approved issue and current native preparations inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "originMainFreshFetch": git(CONTENT, "rev-parse", "origin/main"),
    }
    save(CONTROL / "execution-453-start.json", state)
    p["execution453StartingState"] = state
    p["stage"] = "batch-069-native-execution-in-progress"
    save(PROGRESS, p)
    print(json.dumps(state, ensure_ascii=False, indent=2))


def archive():
    execution = load(SOURCE / "execution.json")
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    route = load(SOURCE / "n1-069-article-route.json")
    assert route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"]) == (1081, 5038, 101)
    assert route["contentVersion"] == "83ed94552dd1a9ce" and route["problems"] == 0
    assert route["fullOnyomi"] == ["ジュ"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["じゅ"] and route["quizKunKeys"] == []
    assert route["acceptedReadingParserEpoch"] == 1
    if execution["passed"]:
        assert execution["terminalSuccessCases"] == 2 and route["passed"]
        for key in ["reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                    "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
                    "drawingGradeRecordedOnNext", "offline"]:
            assert route[key]
        assert route["touchInjectedReferenceStrokes"] == 16
        target = TARGET
    else:
        assert execution["terminalSuccessCases"] == 1 and not route["passed"]
        target = TARGET / "attempt-1-failed"
        target.mkdir()
    rows = load(SOURCE / "n1-069-font-raster.json")
    assert len(rows["rows"]) == 60 and rows["individualGlyphProbes"] == 56 and rows["wholeWordRasterProbes"] == 4
    indexed = []
    for original in sorted(SOURCE.iterdir()):
        if not original.is_file():
            continue
        dest = target / original.name
        if original.suffix == ".txt":
            raw = original.read_bytes()
            normalized = "\n".join(line.rstrip() for line in raw.decode("utf-8-sig").splitlines()).rstrip() + "\n"
            assert not dest.exists()
            dest.write_text(normalized, encoding="utf-8", newline="\n")
            gz = target / (original.name + ".raw.gz")
            assert not gz.exists()
            gz.write_bytes(gzip.compress(raw, mtime=0))
            entry = {"path": str(dest.relative_to(CONTENT)), "sourcePath": str(original),
                     "originalBytes": len(raw), "originalSha256": sha(original),
                     "sha256": sha(dest), "bytes": dest.stat().st_size,
                     "rawGzipPath": str(gz.relative_to(CONTENT)), "rawGzipSha256": sha(gz)}
        else:
            if dest.exists():
                assert sha(dest) == sha(original), f"Refusing overwrite: {dest}"
            else:
                shutil.copyfile(original, dest)
            entry = {"path": str(dest.relative_to(CONTENT)), "sourcePath": str(original),
                     "sha256": sha(dest), "bytes": dest.stat().st_size}
        indexed.append(entry)
    receipts = target / "execution-receipts"
    receipts.mkdir(exist_ok=True)
    for name in ["run-453-native.ps1", "execution-453.py", "execution-453-start.json"]:
        shutil.copyfile(CONTROL / name, receipts / name)
    index = target / "execution-453-artifact-index.json"
    save(index, {"execution": 453, "batch": "069", "artifacts": indexed,
                 "normalization": "Readable text copies use UTF-8 LF and trim trailing whitespace. Deterministic gzip preserves original text bytes. PNG/JSON/fixture bytes copied unchanged. Original attempt retained in control."})
    print(json.dumps({"index": str(index), "sha256": sha(index),
                      "sourceFiles": len(indexed), "pngs": len(list(SOURCE.glob("*.png")))}, indent=2))


def checks():
    results = []
    for name, tool in [("validate-453", "validate.py"), ("manifest-453", "build_manifest.py")]:
        run = subprocess.run([sys.executable, "-B", str(CONTENT / "tools" / tool)],
                             cwd=CONTENT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        path = TARGET / (name + ".txt")
        path.write_bytes(run.stdout)
        results.append({"check": name, "exitCode": run.returncode,
                        "path": str(path.relative_to(CONTENT)), "sha256": sha(path)})
        if run.returncode:
            save(CONTROL / "execution-453-checks.json", results)
            raise RuntimeError(f"{name} failed: {run.stdout.decode('utf-8', errors='replace')}")
    assert not git(CONTENT, "diff", "--name-only", "--", "manifest.json")
    save(CONTROL / "execution-453-checks.json", results)
    print(json.dumps(results, indent=2))


NEXT = (
    "SAME069 native checkpoint453 PASSED retry1: both Glyph and Article terminal0/no skips/158.188s. "
    "Read docs\\n1-sources\\execution-453.json and batch-069-native\\execution-453-artifact-index.json. "
    "46 successful PNGs/raw logs archived; ten successful images requested/directly inspected "
    "(font bytes identical to directly readable attempt1 image), not all46 or independent visual acceptance. "
    "Original attempt1 retained under attempt-1-failed: Glyph0, Article-2 timeout at section after asynchronous "
    "SystemBack. Separately named retry adds explicit destination top-bar await before scrolling; "
    "unchanged production/content/guards/heaps/assertions. Attempt2 aborted before launch on actual adb9520 "
    "SYN_SENT to5581; exact receipt retained. Later fresh ownership inspection was clear; attempt3 passed. "
    "Full signede2457397 Git envelope via production ContentSync ONCE:1081kanji5038words101N1/"
    "83ed94552dd1a9ce/problems0/epoch1; Full+Liteジュ/emptyKun; normalizedじゅ Good persisted/noKunLog. "
    "Three complete article prose/example projections32selectors, two reciprocal pairs/four directions, "
    "SystemBack/offline/N1selection/meaning/16reference-stroke touch/ungradedtrace/recallmiss/persistedDrawAgain. "
    "56singlePaint+4wholeword probes; readable 儒需儀僧優人亻教攴攵子考校木 and儒教 across fourproduction rows. "
    "Reading-table firstcolumn clips at selected horizontal offset; scrollhint/fullジュ explanation visible. "
    "No fallback-face identity/humanhandwriting/MLKit/phone evidence. Owned parent28908/QEMU27816 and "
    "original28244/27576 stopped; preexisting5556 unchanged; Android clean. "
    "NEXT BOUNDED CHECKPOINT: ORIGINAL Claude78cf2390-1187-4593-ba60-ebe562f1a49a then "
    "GPTe683a0f6-66de-4049-ae70-eb508e0866ee SERIAL dependent visual confirmations, actual supported "
    "CLI/read-only tools and bounded packets, frozen signed checkpoint. Assign new儒/儒教 and changed教 reciprocal "
    "passage; unchanged教 full rendering scope is not fresh linguistic review. Record actual image/read/source "
    "limits, not blind initial or all46PNG coverage. Do not rerun passed native or accepted451Android3+1 absent "
    "newconcern; no native HOST heapinit. Preserve original textual reviews and all historical keys. "
    "Then freshlatestmain nonrewriting integration/allcombined source-baseline-reading-link-font-stroke/Python/"
    "vocab/validator/freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained budgets/"
    "normal signing/ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/ownerissue60 "
    "BEFOREdelivery or070. No secondrunner/supervisorchanges/permissionbypass/signingworkaround. "
    "Published95/1228,remaining1133/latest068f9e0511f; local069 NOTdelivered. CompatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def record():
    state = load(CONTROL / "execution-453-start.json")
    execution = load(SOURCE / "execution.json")
    assert execution["passed"] and execution["terminalSuccessCases"] == 2
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    host = load(CONTROL / "execution-453-retry-postrun-host.json")
    assert host["ownedProcesses"] == []
    assert all(c["OwningProcess"] == 0 and c["State"] == 11 for c in host["connections"])
    assert [(p["ProcessId"], p["CommandLine"]) for p in host["preexistingProcesses"]] == [
        (p["ProcessId"], p["CommandLine"]) for p in execution["preexistingEmulators"]]
    assert git(CONTENT, "rev-parse", "HEAD") == HEAD and not git(ANDROID, "status", "--porcelain")
    assert git(ANDROID, "rev-parse", "HEAD") == execution["androidSnapshot"]
    receipts = TARGET / "execution-receipts"
    for name in ["run-453-native.ps1", "run-453-native-retry1.ps1", "run-453-compile-retry1.ps1",
                 "execution-453.py", "execution-453-start.json", "execution-453-postrun-host.json",
                 "execution-453-final-host.json", "execution-453-retry-postrun-host.json",
                 "batch-069-native-retry1-compilation.json", "batch-069-native-attempt-2-execution.json"]:
        shutil.copyfile(CONTROL / name, receipts / name)
    raw_compile = (CONTROL / "artifacts" / "batch-069-native-retry1-compile" / "compile.txt").read_bytes()
    (TARGET / "retry1-compile-raw.txt.gz").write_bytes(gzip.compress(raw_compile, mtime=0))
    (TARGET / "retry1-compile.txt").write_text(
        "\n".join(line.rstrip() for line in raw_compile.decode("utf-8-sig").splitlines()).rstrip() + "\n",
        encoding="utf-8", newline="\n")
    diff = subprocess.run(["git", "--no-pager", "diff", "--no-index",
                           str(TARGET / "N1Batch069NativeTest.kt"),
                           str(TARGET / "N1Batch069NativeRetry1Test.kt")],
                          cwd=CONTENT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    assert diff.returncode == 1
    (TARGET / "retry1-fixture.diff").write_text(
        "\n".join(line.rstrip() for line in diff.stdout.decode("utf-8").splitlines()) + "\n",
        encoding="utf-8", newline="\n")
    (TARGET / "retry1-fixture.diff.raw.gz").write_bytes(gzip.compress(diff.stdout, mtime=0))
    for index in [TARGET / "execution-453-artifact-index.json",
                  TARGET / "attempt-1-failed" / "execution-453-artifact-index.json"]:
        for entry in load(index)["artifacts"]:
            assert sha(CONTENT / entry["path"]) == entry["sha256"]
            if "rawGzipPath" in entry:
                assert hashlib.sha256(gzip.decompress((CONTENT / entry["rawGzipPath"]).read_bytes())).hexdigest() == entry["originalSha256"]
    assert sha(SOURCE / "n1-069-font-pairs.png") == sha(
        CONTROL / "artifacts" / "batch-069-native-attempt-1" / "n1-069-font-pairs.png")
    image_names = ["font-pairs", "word1-07", "component1-23", "drawing-feedback", "curated-On-question",
                   "kanji-11", "kanji-17", "meaning-feedback", "drawing-recall-feedback", "selection"]
    report = {
        "schemaVersion": 1, "execution": 453, "checkpoint": 453, "batch": "069",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingHead": HEAD, "reviewedTeachingSnapshot": "f5061bcdf101f8eba5729b21f222b57821df9a38",
        "scope": state["scope"], "authorization": state["authorization"],
        "originMainFreshFetch": state["originMainFreshFetch"],
        "nativeExecution": execution, "nativeRouteEvidence": load(SOURCE / "n1-069-article-route.json"),
        "failedOriginalAttempt": {
            "receipt": "docs\\n1-reviews\\batch-069-native\\attempt-1-failed\\execution.json",
            "artifactIndex": "docs\\n1-reviews\\batch-069-native\\attempt-1-failed\\execution-453-artifact-index.json",
            "glyphCaseTerminalStatus": 0, "articleCaseTerminalStatus": -2, "passed": False,
            "pngCount": 21,
            "diagnosis": "After System Back at original line289, section() scrolled the prior article before the asynchronous return completed. Final tree shows destination word at bottom with no Article contents mounted; timeout at original line290. A destination-specific top-bar await before any scroll fixed the separately compiled retry. No production defect established.",
        },
        "abortedRetryPrelaunch": {
            "receipt": "docs\\n1-reviews\\batch-069-native\\execution-receipts\\batch-069-native-attempt-2-execution.json",
            "nativeExecuted": False, "reason": "Actual adb server PID9520 SYN_SENT to remote5581. No helper launched or process killed. Later fresh check clear; attempt3 independently rechecked ownership before launch.",
        },
        "retryFixture": {
            **load(CONTROL / "batch-069-native-retry1-compilation.json"),
            "diff": "docs\\n1-reviews\\batch-069-native\\retry1-fixture.diff",
            "diffNormalization": "Readable diff trims trailing whitespace (including blank context markers); deterministic raw gzip preserves original exact git diff bytes.",
            "change": "Separate retry classes plus one destination-title await after actual System Back. Same archive, application, source/content and every import/quiz/drawing/link assertion.",
            "packagedExactFullArchiveVerified": True, "bothClassesAndMethodsVerified": True,
            "originalAnd068DescriptorsAbsent": True,
            "compilation": "BUILD SUCCESSFUL in 1m 11s; one worker, in-process Kotlin, explicit verified JDK17/SDK. No HOST heap init.",
        },
        "artifactIndex": "docs\\n1-reviews\\batch-069-native\\execution-453-artifact-index.json",
        "artifactIndexSha256": sha(TARGET / "execution-453-artifact-index.json"),
        "sourcePngCount": 46, "originalFailedAttemptPngCount": 21,
        "directCoordinatorImageRequests": [f"n1-069-{name}.png" for name in image_names],
        "additionalOriginalAttemptImageRequests": ["n1-069-font-pairs.png", "n1-069-word1-new-kanji-backlink.png"],
        "fontImageIdentity": {
            "sameBytesInBothExecutedAttempts": True, "sha256": sha(SOURCE / "n1-069-font-pairs.png"),
            "dimensions": [1080, 2400],
            "inspection": "Original attempt font image returned fully visible; retry request displayed an anomalous thin preview. Exact equality and dimensions rechecked, not assumed a blank runtime capture. Original readable bytes show all four production rows.",
        },
        "visualObservations": (
            "儒/需 differ by 亻; 儀/僧/優 right-hand shapes are distinguishable; 人 and standalone亻, 教/攴/攵/子/考/校/木 "
            "and 儒教 are readable in all four production rows. Gothic/Mincho/Brush wrap 教 of final 儒教 onto next line; "
            "Textbook keeps that word together. No blank/replacement glyph established. Word formation shows both "
            "linked component labels with readable wrapped explanatory prose; changed 教 Common words backlink visible. "
            "Reading table at captured horizontal offset clips reading column left edge with scroll hint; full ジュ and "
            "no-kun explanation visible below. Reading choiceジュ and three distinct alternatives are visible; "
            "meaning feedback selects Confucian/Confucian scholar. Drawing shows16numbered reference strokes, ungraded "
            "trace and unavailable handwriting-model qualification; recall-miss screen shows blank attempt and reference. "
            "N1 selection displays101cards. Other36successful PNGs not directly inspected."
        ),
        "nativeCoverage": {
            "completeArticleProjections": 3, "proseAndExampleSelectors": 32,
            "reciprocalPairs": 2, "directedTransitions": 4,
            "singleCharacterPaintProbes": 56, "wholeWordRasterProbes": 4,
            "limits": "Three complete prose/table-example projections, not assertions of every table reading/type label, viewport readability or fresh linguistic review of unchanged 教. Ten successful image requests, not all46. Raster hashes do not identify fallback face.",
        },
        "postrunHost": host, "checks": load(CONTROL / "execution-453-checks.json"),
        "nativeAcceptance": True, "independentVisualAcceptance": False, "phoneEvidence": False,
        "accepted451AndroidRetainedWithoutRerun": True, "runtimeEditsMade": False,
        "reviewersLaunched": 0, "publicationAttempted": False, "publishedAdditions": 95,
        "remainingAdditions": 1133, "wholeProjectComplete": False, "nextAction": NEXT,
        "blocker": None, "recordedAt": datetime.now(timezone.utc).isoformat(),
        "limits": "Emulator assertions and bounded direct PNG inspection only. Full production import ONCE per executed attempt, synthetic unique source/HEAD, unchanged guards/heaps/fonts. No owner progress, complete-PNG/independent-visual/physical-phone acceptance, fallback-face identity, MLKit or human recall. Textual450/Android451 inherited unchanged. Latest-main publication and whole-set acceptance outstanding.",
    }
    all_files = []
    for path in sorted(TARGET.rglob("*")):
        if path.is_file():
            all_files.append({"path": str(path.relative_to(CONTENT)), "bytes": path.stat().st_size, "sha256": sha(path)})
    report["artifacts"] = all_files
    save(CONTENT / "docs" / "n1-sources" / "execution-453.json", report)
    p = load(PROGRESS)
    assert p["checkpoint"] == 452
    p["stage"] = "batch-069-native-passed-pending-signed-checkpoint"
    p["execution453StartingState"]["status"] = "native-passed-evidence-prepared"
    p["nextAction"] = NEXT
    save(PROGRESS, p)
    print("Native pass, failed original, prelaunch interruption, retry and all artifact hashes recorded.")


def checkpoint():
    report_path = CONTENT / "docs" / "n1-sources" / "execution-453.json"
    report = load(report_path)
    commit = git(CONTENT, "rev-parse", "HEAD")
    assert git(CONTENT, "log", "-1", "--format=%G?") == "G"
    assert git(CONTENT, "rev-parse", "HEAD^") == HEAD
    assert not git(CONTENT, "status", "--porcelain")
    assert not git(ANDROID, "status", "--porcelain")
    for entry in report["artifacts"]:
        assert sha(CONTENT / entry["path"]) == entry["sha256"]
    p = load(PROGRESS)
    assert p["checkpoint"] == 452 and p["batch"] == "069"
    prior = dict(p)
    p["checkpoint"] = 453
    p["status"] = "continue"
    p["stage"] = "batch-069-native-passed-awaiting-independent-visual-confirmation"
    p["nextAction"] = NEXT
    p["blocker"] = None
    p["execution453StartingState"]["status"] = "signed-native-checkpoint-complete"
    p["batch069NativeExecutionCheckpoint"] = {
        "checkpoint": 453, "execution": 453, "batch": "069", "signedLocalCommit": commit,
        "signature": "G", "record": str(report_path.relative_to(CONTENT)), "recordSha256": sha(report_path),
        "nativeAcceptance": True, "independentVisualAcceptance": False, "phoneEvidence": False,
        "publishedAdditions": 95, "remainingAdditions": 1133, "publicationAttempted": False, "nextAction": NEXT,
    }
    p["execution453CoordinatorCheckpoint"] = p["batch069NativeExecutionCheckpoint"]
    save(PROGRESS, p)
    reloaded = load(PROGRESS)
    assert reloaded["checkpoint"] == 453 and reloaded["status"] == "continue"
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker", "execution453StartingState"}
    for key, value in prior.items():
        if key not in mutable:
            assert reloaded[key] == value, f"Historical key changed: {key}"
    print(json.dumps({"checkpoint": 453, "status": "continue", "signedLocalCommit": commit,
                      "recordSha256": sha(report_path), "allHistoricalKeysPreserved": True}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "retry1":
        SOURCE = CONTROL / "artifacts" / "batch-069-native-attempt-3"
    {"start": start, "archive": archive, "checks": checks, "record": record, "checkpoint": checkpoint}[sys.argv[1]]()
