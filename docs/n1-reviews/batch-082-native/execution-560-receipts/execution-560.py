import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOGS = CONTROL / "logs" / "9914ebfb-0fd5-44b7-b7c5-fde05c66a683"
HEAD = "35f7e9944c74a9d7a00e3beb1f96625fbf85a622"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-082-native"
ATTEMPT = CONTROL / "artifacts" / "batch-082-native-attempt-1"
BEFORE = CONTROL / "execution-560-progress-before.json"
NEXT = (
    "SAME082 two SERIAL original-family dependent VISUAL confirmations next, then persist/yield "
    "before integration/publication/083. Read signed execution560 native evidence and actual original "
    "PNGs/image index/visual inspection under docs/n1-reviews/batch-082-native. Reuse ClaudeOpus5.5 "
    "session1c5aebb9-9903-4567-a88a-5da4b472781d then GPT6.1Sol "
    "sessionfd9a447c-6e9f-4874-a043-4851de97c996 where possible; actual catalog/model/process "
    "evidence and complete original reports required. At most ONE active reviewer, no edits to "
    "frozen snapshot during review. Native TWO named cases terminal0/noskips, full signed4f5812bc "
    "production ContentSync ONCE1094kanji5050words114N1/version0739a82c9699f031/zeroProblems/"
    "epoch1; Full+Lite onジュン/kun[]/quizOnジュン/quizKun[]/soleじゅん. All31Han/fourfamilies "
    "including冫/氵/辶/隹,124individual+4wholeword Paint probes/threeComposepanels. Complete准/"
    "准教授 and exact教bullet/助教授successor paragraph;twomappedpairs+comparisonpair/sixdirections/"
    "SystemBack/offline/N1selection/meaning/singlecuratedon/tenstroke injected trace/giveuprecall. "
    "Reference injection and giveup NOT handwriting recognition/human recall/MLKit/phone acceptance. "
    "Inherit textual closureb6bcc8f1 and recovered558HOST3+1+5/no skips/559compile honestly; no "
    "redundant HOST/native/blindinitial rerun absent new concern. Qualified TEST-ONLY Android1c1b7bf4/G "
    "preserves productionf9b59a2; not latestappmain. Preserve557OOMs/all source/lookup/citation/readdepth/"
    "process/denial/viewport/fallback/MLKit limits and FULL live history. HOSTonly2g init NEVER native; "
    "no app/guestheap/archiveguard increase. Later latest-main integration, combined Python368/"
    "validator/vocabulary/manifest/exact虎猿/originalbudgets, normal signed owner fastforward "
    "publication/remoteSHA/terminalgreenCI/EVERYimmutableZIPhash/verifiedownerissue60 mandatory "
    "before083. Published108/1228,remaining1120,lastPublished1f317f0762513720709ab0ca215f19ff021ca596; "
    "082 not delivered. Physicalphone/generalrelease/whole-set outstanding. One coordinator, no "
    "second runner. Approved workspace/control helpers only; optional historical session recipes "
    "skipped. Preserve/report/yield on actual new denial or signinghang without workaround."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def start():
    original = load(CONTROL / "progress.json")
    assert original["checkpoint"] == 559 and original["batch"] == "082"
    assert not BEFORE.exists()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    state = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert state["checkpoint"] == 559
    save(BEFORE, original)
    starting = {
        "execution": 560, "batch": "082", "startingHead": HEAD,
        "androidHead": git("rev-parse", "HEAD", cwd=ANDROID),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME082 native execution and actual PNG inspection; no reviewer/integration/publication/083 or second runner.",
        "authorization": {"requestSha256": sha(request), "bytes": request.stat().st_size,
                          "characters": len(text), "lines": len(text.splitlines()),
                          "completeFileLoadedAndCheckpointParsed": True,
                          "limits": "Entire request loaded and checkpoint decoded; operative contract, complete issue and final559 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "artifactPathPreflight": str(CONTROL / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "freshOriginMain": git("rev-parse", "origin/main"),
        "manifestSha256": sha(ROOT / "manifest.json"),
        "status": "native-execution-preparing",
    }
    original["execution560StartingState"] = starting
    original["stage"] = "batch-082-native-execution-in-progress"
    original["nextAction"] = starting["scope"]
    save(CONTROL / "progress.json", original)
    save(CONTROL / "execution-560-start.json", starting)
    print("Starting native scope persisted; complete request parsed and live history retained.")


def sheets():
    from PIL import Image, ImageDraw

    output = CONTROL / "artifacts" / "batch-082-native-inspection"
    output.mkdir(exist_ok=True)
    groups = defaultdict(list)
    for path in sorted(ATTEMPT.glob("*.png")):
        groups[sha(path)].append(path)
    representatives = [paths[0] for paths in groups.values()]
    for i in range(0, len(representatives), 6):
        batch = representatives[i:i + 6]
        sheet = Image.new("RGB", (1080, 1100 * ((len(batch) + 1) // 2)), "white")
        draw = ImageDraw.Draw(sheet)
        for j, path in enumerate(batch):
            image = Image.open(path).convert("RGB")
            image.thumbnail((540, 1040))
            x, y = j % 2 * 540, j // 2 * 1100
            sheet.paste(image, (x, y + 40))
            draw.text((x + 4, y + 4), path.name.removeprefix("n1-082-"), fill="black")
        path = output / f"contact-{i // 6 + 1:02}.png"
        if path.exists():
            import io
            data = io.BytesIO()
            sheet.save(data, format="PNG")
            assert data.getvalue() == path.read_bytes()
        else:
            sheet.save(path)
    print(f"{sum(map(len, groups.values()))} original PNGs; {len(groups)} byte groups.")


def record():
    starting = load(CONTROL / "execution-560-start.json")
    native = load(CONTROL / "batch-082-native-attempt-1-execution.json")
    preparation = load(ROOT / "docs" / "n1-sources" / "batch-082-native-fixture-verification.json")
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", cwd=ANDROID) == starting["androidHead"]
    assert not git("status", "--porcelain", cwd=ANDROID)
    assert native["passed"] and native["failure"] is None and native["adbExitCode"] == 0
    expected_cases = {
        ("N1Batch082GlyphTest", "associateRankLookalikesAndRadicalFallbacksAcrossFourProductionFamilies", 0),
        ("N1Batch082ArticleTest", "fullSingleImportOfflineAssociateRankReciprocalAndComparisonLinksCuratedOnDrawingAndSystemBack", 0),
    }
    assert native["terminalSuccessCases"] == 2 and len(native["terminalCases"]) == 2
    assert {(c["class"].split(".")[-1], c["test"], c["status"]) for c in native["terminalCases"]} == expected_cases
    assert native["ownedHelperStopped"] and native["ownedQemuStopped"] and native["stopAdbExitCode"] == 0
    assert (native["parentEmulatorPid"], native["qemuPid"]) == (5996, 27284)
    assert not native["preexistingEmulators"] and not native["prelaunch"]["connections"]
    assert not any(native[k] for k in ("hostHeapInitUsed", "guestOrAppHeapChanged", "guardsChanged"))
    for key in ("testApk", "appApk"):
        assert sha(Path(native[key])) == native[key + "Sha256"]
    assert sha(Path(preparation["fixture"])) == preparation["fixtureSha256"] == native["fixtureSha256"]
    route = load(ATTEMPT / "n1-082-article-route.json")
    raster = load(ATTEMPT / "n1-082-font-raster.json")
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"]) == (1094, 5050, 114, 0)
    assert route["acceptedReadingParserEpoch"] == 1 and not route["phoneEvidence"]
    assert route["contentSnapshot"] == preparation["contentSnapshot"]
    assert route["contentVersion"] == preparation["contentVersion"] == "0739a82c9699f031"
    for key in ("fullOnyomi", "fullProjectionOnyomi", "liteQuizOnyomi", "fullProjectionQuizOnyomi"):
        assert route[key] == ["ジュン"]
    for key in ("fullKunyomi", "fullProjectionKunyomi", "quizKunKeys", "liteQuizKunyomi", "fullProjectionQuizKunyomi"):
        assert route[key] == []
    assert route["quizOnKeys"] == ["じゅん"]
    assert route["touchInjectedReferenceStrokes"] == 10
    assert (route["mappedReciprocalPairs"], route["directedLinkTransitions"], route["comparisonPairs"], route["comparisonLinkTransitions"]) == (2, 4, 1, 2)
    for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedOnPersistedGoodAndDone", "drawingTraceThenRecall", "drawingGradeRecordedOnNext"):
        assert route[key], key
    assert (len(raster["rows"]), raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (128, 124, 4, 3)
    assert raster["fontScale"] == 1 and raster["sdk"] == 35
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        rows = [r for r in raster["rows"] if r["font"] == font]
        assert len(rows) == 32
        glyphs = [r for r in rows if "character" in r]
        assert {r["character"] for r in glyphs} == set(preparation["plannedGlyphs"])
        assert all(r["hasGlyph"] for r in glyphs)
        assert len({r["nativePaintRasterSha256"] for r in glyphs}) == 31
        words = [r for r in rows if "word" in r]
        assert len(words) == 1 and words[0]["word"] == "准教授" and words[0]["renderedCharactersNonblank"] == 3
    groups = defaultdict(list)
    for path in sorted(ATTEMPT.glob("*.png")):
        groups[sha(path)].append(path.name)
    assert sum(map(len, groups.values())) == 51 and len(groups) == 28
    sheets()
    inspection_root = CONTROL / "artifacts" / "batch-082-native-inspection"
    visual = {
        "snapshot": HEAD, "reviewedTeachingSnapshot": "b6bcc8f144cd781917abdb2ca510f663d1339a56",
        "reviewer": "Coordinator; GPT-6.1 Sol (gpt-6.1-sol); not independent two-family visual confirmation",
        "method": "All 51 original PNGs grouped into 28 byte-identical groups; all 28 representatives inspected through five labeled contact sheets. Each 1080x2400 original thumbnailed to 468x1040 (43.33% linear resolution); three original font panels additionally viewed directly. No claim of 51 separate full-resolution reads.",
        "scope": "准 and complete准教授 article; exact added教 bullet and助教授 successor paragraph; six link directions/system Back, selection, meaning/reading feedback and drawing flow; all31 scoped Han/four production font families.",
        "coordinatorDisplayResult": "No actionable clipping, replacement-box, blank glyph or misleading look-alike established in inspected scope. Independently dependent visual review remains outstanding.",
        "glyphInspection": {
            "characters": preparation["plannedGlyphs"], "families": ["Gothic", "Mincho", "Textbook", "Brush"],
            "composePanelsDirectlyViewed": [f"n1-082-font-panel-{i}.png" for i in range(1, 4)],
            "fallbackScope": ["冫", "氵", "辶", "隹"],
            "observations": "All scoped glyphs and准教授 readable in the actual panels. 冫 has two marks versus氵 three; 辶 and隹 show identifiable standalone shapes; 准/準 distinguishable by water marks and lower十, 集/進/難 remain distinct. System-fallback typeface can coincide across bundled choices; no exact fallback face identified."
        },
        "articleInspection": "Complete new text collectively visible over scroll positions. Reading labels/type and example are visible across horizontal table states; no single-frame all-column claim. 准教授 examples/translations, rank distinctions and source notes visible. Changed教 common-word link and助教授 successor passage readable; System Back returns to actual source articles.",
        "sessionInspection": "N1 selection shows114cards. 准 meaning question/feedback; soleジュン on-reading answered and 1/1 completed. Ten-stroke guided trace then give-up recall feedback present; model unavailable and shape-only fallback explicitly visible.",
        "findings": [],
        "independentVisualAcceptance": False, "phoneAcceptance": False,
        "limits": [
            "Coordinator contact-sheet inspection is not independent two-family visual closure, native-speaker certification or measured phone usability.",
            "128 Paint records are124 individual probes plus4 whole-word rasters, not128 PNGs or proof of a specific fallback font face.",
            "Scroll states collectively show article/table text; not every line/column is simultaneously visible.",
            "Offline handwriting model unavailable. Reference-path injected tracing and give-up recall do not test recognizer accuracy or human memory.",
            "Synthetic disposable source/settings/progress fixture; no real owner progress modified. API35 emulator, not physical phone.",
            "All original source/review/citation/lookup/read-depth/process/permission/OOM/viewport/MLKit limitations retained; no publication or whole-set acceptance."
        ]
    }
    index = {
        "originalPngCount": 51, "distinctByteGroups": 28, "inspectionMethod": visual["method"],
        "groups": [{"sha256": digest, "contactSheetRepresentative": names[0], "originals": names}
                   for digest, names in groups.items()],
        "contactSheets": [{"file": p.name, "sha256": sha(p)} for p in sorted(inspection_root.glob("*.png"))],
    }
    manifest = load(ROOT / "manifest.json")
    assert sha(ROOT / "manifest.json") == starting["manifestSha256"]
    verified = 0
    with zipfile.ZipFile(preparation["archive"]) as archive:
        assert sha(Path(preparation["archive"])) == preparation["archiveSha256"] == native["archiveSha256"]
        manifest_name, = (n for n in archive.namelist() if n.endswith("/manifest.json"))
        raw_manifest = archive.read(manifest_name)
        prefix = manifest_name[:-len("manifest.json")]
        assert raw_manifest == (ROOT / "manifest.json").read_bytes()
        retained = len(raw_manifest)
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, expected in entries.items():
                raw, current = archive.read(prefix + name), (ROOT / name).read_bytes()
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                normalized = raw if binary else raw.replace(b"\r\n", b"\n")
                assert normalized == (current if binary else current.replace(b"\r\n", b"\n")), name
                assert hashlib.sha256(normalized).hexdigest() == expected, name
                verified += 1
                retained += len(raw)
        assert verified == 8372
        assert len(archive.infolist()) == preparation["zipEntries"] == 8394
        assert len(archive.infolist()) <= 18000
        assert Path(preparation["archive"]).stat().st_size == preparation["compressedBytes"] <= 42 * 1024**2
        assert sum(i.file_size for i in archive.infolist()) == preparation["inflatedBytes"] <= 80 * 1024**2
        assert retained == preparation["retainedBytes"] <= 56 * 1024**2
    target = FOLDER / "attempt-1"
    assert not target.exists()
    shutil.copytree(ATTEMPT, target)
    copied = []
    for path in sorted(target.iterdir()):
        assert sha(path) == sha(ATTEMPT / path.name)
        row = {"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "bytes": path.stat().st_size}
        if path.suffix == ".txt":
            raw = path.read_bytes()
            compressed = path.with_suffix(".raw.txt.gz")
            compressed.write_bytes(gzip.compress(raw, mtime=0))
            assert gzip.decompress(compressed.read_bytes()) == raw
            readable = "\n".join(line.rstrip() for line in raw.decode("utf-8-sig").splitlines()).rstrip() + "\n"
            path.write_text(readable, encoding="utf-8")
            row.update(originalSha256=row["sha256"], sha256=sha(path), bytes=path.stat().st_size,
                       compressedRaw=compressed.relative_to(ROOT).as_posix(), compressedRawSha256=sha(compressed),
                       normalization="Readable UTF-8/no BOM with trailing whitespace removed; original bytes in gzip.")
        copied.append(row)
    receipts = FOLDER / "execution-560-receipts"
    receipts.mkdir()
    for path in (Path(__file__), CONTROL / "run-560-native.ps1", CONTROL / "post-560-issue.ps1"):
        shutil.copyfile(path, receipts / path.name)
        copied.append({"path": (receipts / path.name).relative_to(ROOT).as_posix(), "sha256": sha(path)})
    inspection = FOLDER / "inspection-execution-560"
    shutil.copytree(inspection_root, inspection)
    save(FOLDER / "visual-inspection-execution-560.json", visual)
    save(FOLDER / "image-index-execution-560.json", index)
    assert "0 error(s)" in (LOGS / "validate-560.txt").read_text(encoding="utf-8-sig")
    for name in ("validate-560.txt", "manifest-560.txt"):
        text = (LOGS / name).read_text(encoding="utf-8-sig")
        (FOLDER / name).write_text("\n".join(l.rstrip() for l in text.splitlines()).rstrip() + "\n", encoding="utf-8")
    evidence = {
        **starting, "schemaVersion": 1, "checkpoint": 560, "status": "continue",
        "stage": "batch-082-native-passed-awaiting-independent-visual-confirmations",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "nativeExecution": native, "articleRoute": route,
        "nativeRasterRecords": {"rows": 128, "individualGlyphProbes": 124, "wholeWordRasterProbes": 4,
                               "panels": 3, "path": (target / "n1-082-font-raster.json").relative_to(ROOT).as_posix(),
                               "sha256": sha(target / "n1-082-font-raster.json")},
        "visualInspection": visual, "imageIndex": index, "archivedReceipts": copied,
        "rawAttemptsAndOriginalPngBytesPreserved": True,
        "productionSingleArchiveImport": True, "exactRuntimeHashesVerified": verified,
        "originalArchiveBudgetsReverified": True, "runtimeUnchanged": True,
        "runtimePublished": False, "independentVisualReviewersLaunched": 0,
        "contentVersion": route["contentVersion"],
        "inheritedTextualReview": "b6bcc8f144cd781917abdb2ca510f663d1339a56",
        "inheritedFreshHostChecks": "execution558 recovered non-skipped RealContent3/RareHan1/loaderRegression5; original557OOM evidence preserved, not reclassified or rerun.",
        "inheritedNativeCompile": "execution559 frozen native test/app APKs; no redundant compile or HOST-only heap init.",
        "qualifiedAndroidHead": starting["androidHead"],
        "originalReviewerSessions": {"claude-opus-5.5": "1c5aebb9-9903-4567-a88a-5da4b472781d",
                                     "gpt-6.1-sol": "fd9a447c-6e9f-4874-a043-4851de97c996"},
        "otherOwnerDevices": "Fresh device list and preexisting emulator inventory empty. No other owner device modified; every mutation targets owned5580, stopped after checks.",
        "validatorErrors": 0, "manifestFresh": True, "manifestBytesUnchanged": True,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": starting["freshOriginMain"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT, "limits": visual["limits"],
    }
    save(ROOT / "docs" / "n1-sources" / "execution-560.json", evidence)
    ledger_path = ROOT / "docs" / "n1-sources" / "batch-082-progress.json"
    ledger = load(ledger_path)
    assert "preNative560AcceptanceState" not in ledger
    ledger["preNative560AcceptanceState"] = {
        k: ledger[k] for k in ("status", "nextAction", "limits", "fontDisposition") if k in ledger
    }
    ledger.update(
        status=evidence["stage"], nextAction=NEXT, limits=visual["limits"],
        fontDisposition="Fresh560 native31Han/fourfamilies/three original Compose panels including 冫/氵/辶/隹 readable in coordinator inspection; independent two-family visual closure/phone outstanding.",
        nativeEvidence="docs/n1-sources/execution-560.json",
        nativeExecutionCases=2, independentVisualAcceptance=False,
    )
    save(ledger_path, ledger)
    print("Native evidence archived: 2 terminal-zero cases; 51 PNGs/28 groups; 8372 runtime hashes.")


def normalize_receipts():
    path = ROOT / "docs" / "n1-sources" / "execution-560.json"
    evidence = load(path)
    for row in evidence["archivedReceipts"]:
        if "compressedRaw" not in row:
            continue
        receipt = ROOT / row["path"]
        text = receipt.read_text(encoding="utf-8")
        receipt.write_text(text.rstrip() + "\n", encoding="utf-8")
        row.update(sha256=sha(receipt), bytes=receipt.stat().st_size)
    helper = FOLDER / "execution-560-receipts" / Path(__file__).name
    shutil.copyfile(Path(__file__), helper)
    for row in evidence["archivedReceipts"]:
        if row["path"] == helper.relative_to(ROOT).as_posix():
            row["sha256"] = sha(helper)
    evidence["diagnostics"] = [
        "First staged whitespace check caught an extra blank line at EOF in readable adb receipt. Removed it and updated hashes/recipe; exact original receipt bytes remain preserved in gzip. No runtime/native rerun or acceptance change."
    ]
    save(path, evidence)


def verify():
    ev = load(ROOT / "docs" / "n1-sources" / "execution-560.json")
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    prefix = "docs/n1-reviews/batch-082-native/"
    assert all(p.startswith(prefix) or p in {"docs/n1-sources/execution-560.json", "docs/n1-sources/batch-082-progress.json"} for p in staged)
    for row in ev["archivedReceipts"]:
        assert sha(ROOT / row["path"]) == row["sha256"], row["path"]
        if "compressedRaw" in row:
            compressed = ROOT / row["compressedRaw"]
            assert sha(compressed) == row["compressedRawSha256"]
            assert hashlib.sha256(gzip.decompress(compressed.read_bytes())).hexdigest() == row["originalSha256"]
    for row in ev["imageIndex"]["groups"]:
        for name in row["originals"]:
            assert sha(FOLDER / "attempt-1" / name) == row["sha256"]
    for path in staged:
        assert subprocess.check_output(["git", "show", ":" + path], cwd=ROOT) == (ROOT / path).read_bytes(), path
        if path.endswith(".json"):
            load(ROOT / path)
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
    assert sha(ROOT / "manifest.json") == ev["manifestSha256"]
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("status", "--porcelain", cwd=ANDROID)
    print(json.dumps({"stagedFiles": len(staged), "allIndexBytesExact": True, "runtimeUnchanged": True}))


def checkpoint():
    original, progress = load(BEFORE), load(CONTROL / "progress.json")
    evidence = load(ROOT / "docs" / "n1-sources" / "execution-560.json")
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    receipt = load(CONTROL / "execution-560-issue-response.json")
    body = (CONTROL / "execution-560-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.rstrip()
    assert signed in receipt["body"] and "issues/60#issuecomment-" in receipt["html_url"]
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in original.items():
        assert key in allowed or progress[key] == value, key
    result = {
        "schemaVersion": 1, "execution": 560, "checkpoint": 560, "batch": "082",
        "savedCommit": signed, "signature": "G", "status": "continue", "stage": evidence["stage"],
        "evidence": "docs/n1-sources/execution-560.json",
        "qualifiedAndroidHead": evidence["qualifiedAndroidHead"],
        "nativeCasesExecuted": 2, "terminalZeroCases": 2, "skips": 0,
        "serial": evidence["nativeExecution"]["serial"], "parentEmulatorPid": 5996, "qemuPid": 27284,
        "ownedHelperStopped": True, "ownedQemuStopped": True,
        "runtimePayloadHashesVerified": 8372, "contentVersion": evidence["contentVersion"],
        "originalPngs": 51, "distinctPngGroups": 28, "coordinatorInspectionContactSheets": 5,
        "fontPanelsDirectlyViewed": 3, "nativePaintProbes": 128,
        "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "runtimeBytesUnchanged": True, "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None, "allOriginalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(original), "changedRootFields": sorted(allowed),
    }
    progress.update(checkpoint=560, status="continue", stage=evidence["stage"], nextAction=NEXT, blocker=None)
    progress["execution560StartingState"]["status"] = "signed-local-native-checkpoint-complete"
    progress["execution560CoordinatorCheckpoint"] = result
    progress["batch082NativeAcceptance"] = result
    temporary = CONTROL / "execution-560-progress.tmp.json"
    save(temporary, progress)
    written = load(temporary)
    for key, value in original.items():
        assert key in allowed or written[key] == value, key
    temporary.replace(CONTROL / "progress.json")
    save(CONTROL / "execution-560-final-verification.json", result)
    print(json.dumps({"checkpoint": 560, "status": "continue", "savedCommit": signed,
                      "historyKeysPreserved": len(original), "issueUpdate": receipt["html_url"]}))


if __name__ == "__main__":
    {"start": start, "sheets": sheets, "record": record, "normalize": normalize_receipts,
     "verify": verify, "checkpoint": checkpoint}[sys.argv[1]]()
