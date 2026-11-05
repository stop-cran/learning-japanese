import hashlib
import gzip
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CONTROL = Path(__file__).parent
CONTENT = CONTROL.parent / "learning-japanese"
PROGRESS = CONTROL / "progress.json"
REQUEST = CONTROL / "logs" / "7ef4e40e-1096-43b8-87ae-47bcd6ef36e2" / "request.txt"


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def start():
    raw = REQUEST.read_bytes()
    text = raw.decode("utf-8-sig")
    json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = json.loads(PROGRESS.read_text(encoding="utf-8-sig"))
    assert p["checkpoint"] == 443 and p["batch"] == "068"
    assert "execution444StartingState" not in p
    state = {
        "execution": 444,
        "batch": "068",
        "startingHead": "9fe550d130e559720d1991314635dda0849bc442",
        "scope": "SAME068 compiled native execution, evidence archival, direct bounded PNG inspection and normally signed local checkpoint only. No reviewer/publication/069/second runner.",
        "status": "executing-native-checkpoint",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "authorization": {
            "requestSha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "characters": len(text),
            "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and complete embedded checkpoint parsed; operative contract, final443 checkpoint and complete approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
    }
    save(CONTROL / "execution-444-start.json", state)
    p["execution444StartingState"] = state
    p["stage"] = "batch-068-native-execution-in-progress"
    save(PROGRESS, p)
    print(json.dumps(state, ensure_ascii=False, indent=2))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive():
    source = CONTROL / "artifacts" / "batch-068-native-attempt-1"
    target = CONTENT / "docs" / "n1-reviews" / "batch-068-native"
    execution = json.loads((source / "execution.json").read_text(encoding="utf-8-sig"))
    assert execution["passed"] and execution["terminalSuccessCases"] == 2
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    route = json.loads((source / "n1-068-article-route.json").read_text(encoding="utf-8"))
    assert route["passed"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"]) == (1080, 5037, 100)
    assert route["contentVersion"] == "ddef65b637fe2f85" and route["problems"] == 0
    assert route["fullOnyomi"] == ["ギ"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["ぎ"] and route["quizKunKeys"] == []
    assert route["acceptedReadingParserEpoch"] == 1
    for key in ["reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
                "drawingGradeRecordedOnNext", "offline"]:
        assert route[key]
    assert route["touchInjectedReferenceStrokes"] == 15
    rows = json.loads((source / "n1-068-font-raster.json").read_text(encoding="utf-8"))
    assert len(rows["rows"]) == 76
    assert rows["individualGlyphProbes"] == 60 and rows["wholeWordRasterProbes"] == 16
    indexed = []
    for original in sorted(source.iterdir()):
        if not original.is_file():
            continue
        dest = target / original.name
        if original.suffix == ".txt":
            raw = original.read_bytes()
            normalized = "\n".join(line.rstrip() for line in raw.decode("utf-8-sig").splitlines()).rstrip() + "\n"
            dest.write_text(normalized, encoding="utf-8", newline="\n")
            gz = target / (original.name + ".raw.gz")
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
    shutil.copyfile(CONTROL / "run-444-native.ps1", receipts / "run-444-native.ps1")
    shutil.copyfile(Path(__file__), receipts / "execution-444.py")
    index = target / "execution-444-artifact-index.json"
    save(index, {"execution": 444, "batch": "068", "artifacts": indexed,
                 "normalization": "Readable text copies use UTF-8 LF and trim trailing whitespace. Deterministic gzip preserves original text bytes. PNG/JSON/fixture bytes copied unchanged. Original attempt retained in control."})
    print(json.dumps({"index": str(index), "sha256": sha(index),
                      "sourceFiles": len(indexed), "pngs": len(list(source.glob("*.png")))}, indent=2))


def postrun():
    def git(directory, *args):
        return subprocess.check_output(["git", "-C", str(directory), *args], timeout=30, encoding="utf-8").strip()
    android = CONTENT.parent / "kanji-cards-android"
    data = {
        "contentHead": git(CONTENT, "rev-parse", "HEAD"),
        "contentStatus": git(CONTENT, "status", "--porcelain").splitlines(),
        "androidHead": git(android, "rev-parse", "HEAD"),
        "androidStatus": git(android, "status", "--porcelain").splitlines(),
        "recordedAt": datetime.now(timezone.utc).isoformat(),
    }
    save(CONTROL / "execution-444-postrun-git.json", data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def checks():
    folder = CONTENT / "docs" / "n1-reviews" / "batch-068-native"
    results = []
    for name, tool in [("validate-444", "validate.py"), ("manifest-444", "build_manifest.py")]:
        run = subprocess.run([sys.executable, "-B", str(CONTENT / "tools" / tool)],
                             cwd=CONTENT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        path = folder / (name + ".txt")
        path.write_bytes(run.stdout)
        results.append({"check": name, "exitCode": run.returncode,
                        "path": str(path.relative_to(CONTENT)), "sha256": sha(path)})
        if run.returncode:
            save(CONTROL / "execution-444-checks.json", results)
            raise RuntimeError(f"{name} failed: {run.stdout.decode('utf-8', errors='replace')}")
    assert not subprocess.check_output(["git", "diff", "--name-only", "--", "manifest.json"], cwd=CONTENT)
    save(CONTROL / "execution-444-checks.json", results)
    print(json.dumps(results, indent=2))


NEXT = (
    "SAME068 native checkpoint444: Glyph and Article cases terminal0/no skips/272.859s. "
    "Read docs\\n1-sources\\execution-444.json and batch-068-native\\execution-444-artifact-index.json; "
    "127 original PNGs/raw logs archived, sixteen direct coordinator PNGs inspected, NOT complete-PNG acceptance. "
    "Exact full signed7ca40a69 Git envelope through production ContentSync ONCE:1080kanji5037words100N1/"
    "ddef65b637fe2f85/problems0/epoch1. Full+Liteギ/emptyKun; sole normalizedぎ Good persisted/noKunLog. "
    "Nine complete article prose/example projections98selectors, all eight changed reused passages/revised私儀 note, "
    "eight mapped reciprocal pairs16directions/SystemBack/offline/N1selection/meaning/"
    "15reference-stroke touch/ungradedtrace/recallmiss/persistedDrawAgain. "
    "60singlePaint+16wholewordraster probes pass; four production rows visibly readable "
    "儀義億優倍人亻式礼辞行亍弋彳礻/儀式/礼儀/行儀/お辞儀. "
    "First-column left edge clipped at captured horizontal reading-table offset with explicit scroll hint; "
    "linked examples and explanatory paragraphs legible. No fallback-face identity/MLKit/humanhandwriting/physicalphone acceptance. "
    "Owned parent19472/QEMU13316 stopped; preexistingemulator5556 unchanged; no owned PIDs or port connections. "
    "Next bounded checkpoint: ORIGINAL Claude79971d7f-dd53-46bf-8249-df9d0c122c12 then "
    "GPT4b8ed210-be92-4627-8679-44e8622067dd SERIAL bounded dependent visual confirmations using actual "
    "supported CLI/read-only controls and bounded native image packets. Record actual image/read-depth/source limits, "
    "not fresh blind reviews or all127PNG coverage. All eight reused changed passages should be assigned explicitly. "
    "Do not rerun passed native or accepted442Android3+1 absentnewconcern; qualified HOST-only heap init NEVER native builds. "
    "Preserve textual441 closure/original reports/permissiondenials/OOMs and full livehistory. "
    "Then freshlatestmain nonrewriting integration/allcombined source-baseline-reading-link-font-stroke/Python/vocab/"
    "validator/freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained budgets/normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/everyimmutablepublicZIPruntimehash/ownerissue60 BEFOREdelivery or069. "
    "Permissiondenial/signingwait: preserve exact command/error and yield; no workaround, secondrunner, "
    "concurrentheavywork or supervisorchanges. Published94/1228,remaining1134/latest06772f99d82; local068 NOTdelivered. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def record():
    target = CONTENT / "docs" / "n1-reviews" / "batch-068-native"
    source = CONTROL / "artifacts" / "batch-068-native-attempt-1"
    start_state = json.loads((CONTROL / "execution-444-start.json").read_text(encoding="utf-8"))
    host = json.loads((CONTROL / "execution-444-postrun-host.json").read_text(encoding="utf-8-sig"))
    git = json.loads((CONTROL / "execution-444-postrun-git.json").read_text(encoding="utf-8"))
    assert host["ownedProcesses"] == [] and host["connections"] == []
    assert git["contentHead"] == start_state["startingHead"] and git["androidStatus"] == []
    assert all(line.startswith("?? docs/n1-reviews/batch-068-native/") for line in git["contentStatus"])
    execution = json.loads((source / "execution.json").read_text(encoding="utf-8"))
    assert [(p["ProcessId"], p["CommandLine"]) for p in host["preexistingProcesses"]] == [
        (p["ProcessId"], p["CommandLine"]) for p in execution["preexistingEmulators"]]
    for name in ["execution-444-postrun-host.json", "execution-444-postrun-git.json", "execution-444-start.json"]:
        shutil.copyfile(CONTROL / name, target / "execution-receipts" / name)
    shutil.copyfile(Path(__file__), target / "execution-receipts" / "execution-444.py")
    index = target / "execution-444-artifact-index.json"
    entries = json.loads(index.read_text(encoding="utf-8"))["artifacts"]
    for entry in entries:
        assert sha(CONTENT / entry["path"]) == entry["sha256"]
        if "rawGzipPath" in entry:
            assert hashlib.sha256(gzip.decompress((CONTENT / entry["rawGzipPath"]).read_bytes())).hexdigest() == entry["originalSha256"]
    images = [
        "font-pairs", "kanji-19", "kanji-11", "drawing-recall-feedback",
        "word1-06", "word2-07", "word3-07", "word4-07",
        "component1-16", "component2-20", "component3-30", "component4-19",
        "curated-On-question", "drawing-feedback", "meaning-feedback", "selection",
    ]
    record_data = {
        "schemaVersion": 1, "execution": 444, "checkpoint": 444, "batch": "068",
        "status": "native-passed-awaiting-independent-visual-confirmation",
        "startingHead": start_state["startingHead"],
        "reviewedTeachingSnapshot": "80f5f424729d8832cdc9ecb8491b59559d921cd3",
        "authorization": start_state["authorization"], "scope": start_state["scope"],
        "nativeExecution": execution,
        "nativeRouteEvidence": json.loads((source / "n1-068-article-route.json").read_text(encoding="utf-8")),
        "artifactIndex": str(index.relative_to(CONTENT)), "artifactIndexSha256": sha(index),
        "sourcePngCount": 127,
        "directCoordinatorImageRequests": [f"n1-068-{name}.png" for name in images],
        "visualObservations": (
            "All fifteen glyphs and four words are readable in four production font rows; Textbook wraps 礻 "
            "and the words without missing characters. 儀/義 differ by 亻; 億/優/倍 have distinguishable right halves. "
            "人/亻 and actual fallback components 亍/弋/彳/礻 are visible, with イ-like and ネ-like conventional component forms. "
            "Actual fallback face not identified. Revised 私儀 formal-self-reference note and globe/ceremony boundary "
            "wrap legibly. All four word formation paragraphs show both component links; the four legacy Common words "
            "additions show their compound links. Eight changed reused passages directly imaged, not a fresh linguistic "
            "review of unchanged baseline prose. Horizontally scrolled reading tables clip first-column left edges "
            "at these captured offsets; explicit scroll hints, linked examples and nearby full ギ explanation remain visible. "
            "On question has ギ and three distinct alternatives; meaning feedback marks ceremony/formal conduct correct. "
            "Drawing practice has fifteen numbered reference strokes, ungraded practice and model-unavailable qualification. "
            "Recall-miss screen shows blank attempt and numbered reference. This was touch-injected reference geometry, "
            "not human handwriting or MLKit acceptance. N1 selection displays100cards. Other111PNGs not directly inspected."
        ),
        "nativeCoverage": {
            "completeArticleProjections": 9, "proseAndExampleSelectors": 98,
            "changedReusedPassages": 8, "reciprocalPairs": 8, "directedTransitions": 16,
            "singleCharacterPaintProbes": 60, "wholeWordRasterProbes": 16,
            "limits": "Nine source-derived complete prose/table-example projections, not separate assertions of every table reading/type label, viewport readability, or fresh linguistic review. Sixteen direct PNGs, not all127. Raster hashes do not identify fallback face."
        },
        "independentPostrunVerification": {"git": git, "host": host},
        "operationalInterruption": {
            "stoppedReadOnlyProbeShells": [5, 6, 7],
            "details": "Three postrun read-only shell probes returned no output and remained running; stopped their exact tool-owned process trees. No signing command, permission denial or native failure. A later fresh bounded probe completed and saved actual cleanup/worktree/device evidence. No cause established; no policy/configuration/heap changes."
        },
        "checks": json.loads((CONTROL / "execution-444-checks.json").read_text(encoding="utf-8")),
        "nativeAcceptance": True, "independentVisualAcceptance": False, "phoneEvidence": False,
        "accepted442AndroidRetainedWithoutRerun": True, "runtimeEditsMade": False,
        "reviewersLaunched": 0, "publicationAttempted": False, "publishedAdditions": 94,
        "remainingAdditions": 1134, "wholeProjectComplete": False, "nextAction": NEXT,
        "blocker": None, "recordedAt": datetime.now(timezone.utc).isoformat(),
        "limits": "Native emulator assertions plus sixteen direct coordinator PNG inspections only. Synthetic unique source/HEAD, full production import once with unchanged guards/heaps/fonts. No owner progress, complete-PNG/independent visual/physical-phone acceptance, fallback-face identity, MLKit or human recall. Textual441/Android442 inherited unchanged, not rerun. Latest-main publication and whole-set acceptance outstanding.",
    }
    save(CONTENT / "docs" / "n1-sources" / "execution-444.json", record_data)
    p = json.loads(PROGRESS.read_text(encoding="utf-8-sig"))
    assert p["checkpoint"] == 443
    p["stage"] = "batch-068-native-passed-pending-signed-checkpoint"
    p["execution444StartingState"]["status"] = "native-passed-evidence-prepared"
    p["nextAction"] = NEXT
    save(PROGRESS, p)
    print("Record written; native and all archived hashes verified. No publication.")


if __name__ == "__main__":
    {"start": start, "archive": archive, "postrun": postrun, "checks": checks, "record": record}[sys.argv[1]]()
