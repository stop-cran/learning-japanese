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

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
HEAD = "d5c5f744b8750d3dfa16d59fe2d9dd86cfb74bf8"
AH = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
REQUEST = C / "logs" / "24afdbfd-9b14-494a-93c2-6cef4da85979" / "request.txt"
BEFORE = C / "execution-565-progress-before.json"
ATTEMPT = C / "artifacts" / "batch-082-corrected-native-attempt-565"
FOLDER = R / "docs" / "n1-reviews" / "batch-082-native-corrected"
EVIDENCE = R / "docs" / "n1-sources" / "execution-565.json"
NEXT = (
    "SAME082 corrected-runtime two SERIAL original-family dependent VISUAL confirmations NEXT, "
    "then persist/yield before integration/publication/083. Read signed execution565 evidence, "
    "actual corrected PNGs/image-index/coordinator inspection under "
    "docs/n1-reviews/batch-082-native-corrected. Reuse ClaudeOpus5.5 "
    "session1c5aebb9-9903-4567-a88a-5da4b472781d then GPT6.1Sol "
    "sessionfd9a447c-6e9f-4874-a043-4851de97c996; one active reviewer maximum, actual model/"
    "process/read-return evidence and complete original reports, no frozen snapshot edits. "
    "Corrected d82e7fefe3898a70 native both named cases terminal0/no skips; exact default meaning "
    "options 准/冴/冶/隼 and exact titles/no倣/no fallback asserted in production question. "
    "Full production ContentSync ONCE1094kanji5050words114N1/zeroProblems/acceptedepoch1; "
    "Full+Lite soleジュン/kun[] and soleじゅん key. All34Han/fourfamilies136individual+4wholeword "
    "rasters/3Composepanels including冴/冶/隼 and冫/氵/辶/隹. Complete准/准教授 plus exact教bullet/"
    "助教授successor paragraph;2mappedpairs4directions+comparison2directions/SystemBack/offline/"
    "N1selection/meaning/singleon/10stroke injectedtrace then giveuprecall. NOT humanmemory/"
    "recognition/MLKitdownload/phone evidence. Source082-V1 resolved9ce870d1; independent visual "
    "acceptance remains false until both original-family confirmations reconciled. Preserve "
    "old559/560/561 uncorrected receipts and all original source/lookup/citation/readdepth/denial/"
    "OOM/process/viewport/fallback/MLKit limits; rarity of准える not disproof. Defaultfour N1/All "
    "with allvalidcandidates only; custom/partial/larger/future pools not certified. "
    "Inherit563HOST3+1+5/no skips and564compile honestly; no redundant HOST/native/blindinitial "
    "rerun absent new concern. Qualified TEST-ONLY Android1c1b7bf4/G preserves productionf9b59a2, "
    "not latestappmain. HOST-only2g init NEVERnative; no app/guestheap/guard increase. "
    "AFTER acceptance latestmain/nonrewritingintegration/combinedPython368/validator/vocabulary/"
    "freshmanifest/exact虎猿/baseline/link/membership/original18000entries42MiBcompressed80MiBinflated"
    "56MiBretainedguards/normal signedownerfastforward/remoteSHA/terminalgreenCI/EVERYimmutableZIP"
    "hash/verifiedownerissue60 mandatory before083. Published108/1228,remaining1120,lastPublished"
    "1f317f0762513720709ab0ca215f19ff021ca596;082NOTdelivered. Phone/generalrelease/whole-set"
    "outstanding. Full live history, approved workspace/committed sources/controlhelpers only; "
    "no optionalhistoricalsessionrecipe access. Onecoordinator/no secondrunner. Actualnewdenial/"
    "signinghang preserve/report/yield withoutworkaround."
)


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def now():
    return datetime.now(timezone.utc).isoformat()


def runtime():
    m = load(R / "manifest.json")
    assert m["contentVersion"] == "d82e7fefe3898a70"
    count = 0
    for section, entries in m.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            raw = (R / name).read_bytes()
            if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                raw = raw.replace(b"\r\n", b"\n")
            assert hashlib.sha256(raw).hexdigest() == digest, name
            count += 1
    assert count == 8372
    return {"contentVersion": m["contentVersion"], "runtimeHashesVerified": count,
            "manifestSha256": sha(R / "manifest.json")}


def start():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 564 and p["status"] == "continue" and p["batch"] == "082"
    assert not BEFORE.exists()
    text = REQUEST.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 564
    for root, head in [(R, HEAD), (A, AH)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    save(BEFORE, p)
    state = {
        "execution": 565, "batch": "082", "startedAt": now(),
        "startingHead": HEAD, "androidHead": AH,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME082 corrected native execution and actual PNG inspection only; no reviewer, integration/publication/083 or second runner.",
        "authorization": {"requestSha256": sha(REQUEST), "bytes": REQUEST.stat().st_size,
                          "characters": len(text), "lines": len(text.splitlines()),
                          "completeFileLoadedAndCheckpointParsed": True,
                          "limits": "Entire request loaded and checkpoint decoded; operative contract, complete issue and final564 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "artifactPathPreflight": str(C / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "dedicatedWorktreesInitiallyClean": True, **runtime(),
        "status": "corrected-native-execution-in-progress"
    }
    p["execution565StartingState"] = state
    p["stage"] = "batch-082-corrected-native-execution-in-progress"
    p["nextAction"] = state["scope"]
    save(C / "progress.json", p)
    save(C / "execution-565-start.json", state)
    print("Complete request parsed; starting scope persisted with full live history.")


def sheets():
    from PIL import Image, ImageDraw
    out = C / "artifacts" / "batch-082-corrected-inspection-565"
    out.mkdir(exist_ok=True)
    groups = defaultdict(list)
    for path in sorted(ATTEMPT.glob("*.png")):
        groups[sha(path)].append(path)
    reps = [paths[0] for paths in groups.values()]
    for i in range(0, len(reps), 6):
        batch = reps[i:i + 6]
        sheet = Image.new("RGB", (1080, 1100 * ((len(batch) + 1) // 2)), "white")
        draw = ImageDraw.Draw(sheet)
        for j, path in enumerate(batch):
            image = Image.open(path).convert("RGB")
            image.thumbnail((540, 1040))
            x, y = j % 2 * 540, j // 2 * 1100
            sheet.paste(image, (x, y + 40))
            draw.text((x + 4, y + 4), path.name.removeprefix("n1-082-corrected-"), fill="black")
        sheet.save(out / f"contact-{i // 6 + 1:02}.png")
    print(json.dumps({"pngs": sum(map(len, groups.values())), "groups": len(groups),
                      "sheets": len(list(out.glob("*.png"))) }))


def record():
    from PIL import Image
    state = load(C / "execution-565-start.json")
    native = load(C / "batch-082-corrected-native-attempt-565-execution.json")
    prep = load(R / "docs" / "n1-sources" / "batch-082-corrected-native-fixture-verification.json")
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == AH and not git("status", "--porcelain", root=A)
    assert native["passed"] and native["failure"] is None and native["adbExitCode"] == 0
    expected_cases = {
        ("N1Batch082CorrectedGlyphTest", "associateRankLookalikesAndRadicalFallbacksAcrossFourProductionFamilies", 0),
        ("N1Batch082CorrectedArticleTest", "fullSingleImportOfflineAssociateRankReciprocalAndComparisonLinksCuratedOnDrawingAndSystemBack", 0),
    }
    assert native["terminalSuccessCases"] == len(native["terminalCases"]) == 2
    assert {(c["class"].split(".")[-1], c["test"], c["status"]) for c in native["terminalCases"]} == expected_cases
    assert native["ownedHelperStopped"] and native["ownedQemuStopped"] and native["stopAdbExitCode"] == 0
    assert (native["parentEmulatorPid"], native["qemuPid"]) == (25860, 12960)
    assert not native["preexistingEmulators"] and not native["prelaunch"]["connections"]
    assert not any(native[k] for k in ("hostHeapInitUsed", "guestOrAppHeapChanged", "guardsChanged"))
    raw_log = (ATTEMPT / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert "OK (2 tests)" in raw_log and "INSTRUMENTATION_STATUS_CODE: -3" not in raw_log
    for key in ("testApk", "appApk"):
        assert sha(Path(native[key])) == native[key + "Sha256"]
    assert sha(Path(prep["fixture"])) == prep["fixtureSha256"] == native["fixtureSha256"]
    assert sha(Path(prep["priorFixture"])) == prep["priorFixtureSha256"]
    assert sha(Path(prep["priorArchive"])) == prep["priorArchiveSha256"]
    with zipfile.ZipFile(native["testApk"]) as apk:
        assert apk.read("assets/" + Path(prep["archive"]).name) == Path(prep["archive"]).read_bytes()
    route = load(ATTEMPT / "n1-082-corrected-article-route.json")
    raster = load(ATTEMPT / "n1-082-corrected-font-raster.json")
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"]) == (1094, 5050, 114, 0)
    assert route["acceptedReadingParserEpoch"] == 1 and not route["phoneEvidence"]
    assert route["contentSnapshot"] == prep["contentSnapshot"] == "e108bbeb0fcd4fda3837d955a652f662f72fdac1"
    assert route["contentVersion"] == prep["contentVersion"] == "d82e7fefe3898a70"
    expected_options = {"准": "quasi-; associate rank", "冴": "clear; sharp-minded",
                        "冶": "smelt; work metals", "隼": "falcon"}
    assert len(route["exactDefaultMeaningOptions"]) == 4
    assert {v["kanji"]: v["title"] for v in route["exactDefaultMeaningOptions"]} == expected_options
    assert route["exactCuratedChoicesWithoutFallback"]
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
    assert (len(raster["rows"]), raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (140, 136, 4, 3)
    assert raster["fontScale"] == 1 and raster["sdk"] == 35
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        rows = [r for r in raster["rows"] if r["font"] == font]
        assert len(rows) == 35
        glyphs = [r for r in rows if "character" in r]
        assert {r["character"] for r in glyphs} == set(prep["plannedGlyphs"])
        assert all(r["hasGlyph"] for r in glyphs)
        assert len({r["nativePaintRasterSha256"] for r in glyphs}) == 34
        words = [r for r in rows if "word" in r]
        assert len(words) == 1 and words[0]["word"] == "准教授" and words[0]["renderedCharactersNonblank"] == 3
    groups = defaultdict(list)
    for path in sorted(ATTEMPT.glob("*.png")):
        assert Image.open(path).size == (1080, 2400)
        groups[sha(path)].append(path.name)
    assert sum(map(len, groups.values())) == 51 and len(groups) == 28
    manifest = load(R / "manifest.json")
    assert runtime() == {k: state[k] for k in ("contentVersion", "runtimeHashesVerified", "manifestSha256")}
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    assert build_manifest(R) == manifest
    with zipfile.ZipFile(prep["archive"]) as archive:
        assert sha(Path(prep["archive"])) == prep["archiveSha256"] == native["archiveSha256"]
        manifest_name, = (n for n in archive.namelist() if n.endswith("/manifest.json"))
        raw_manifest = archive.read(manifest_name)
        assert raw_manifest == (R / "manifest.json").read_bytes()
        prefix = manifest_name[:-len("manifest.json")]
        retained, verified = len(raw_manifest), 0
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, digest in entries.items():
                raw = archive.read(prefix + name)
                current = (R / name).read_bytes()
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                normalized = raw if binary else raw.replace(b"\r\n", b"\n")
                assert normalized == (current if binary else current.replace(b"\r\n", b"\n")), name
                assert hashlib.sha256(normalized).hexdigest() == digest, name
                retained += len(raw)
                verified += 1
        assert verified == 8372
        assert len(archive.infolist()) == prep["zipEntries"] == 8394
        assert len(archive.infolist()) <= 18000
        assert Path(prep["archive"]).stat().st_size == prep["compressedBytes"] <= 42 * 1024**2
        assert sum(i.file_size for i in archive.infolist()) == prep["inflatedBytes"] <= 80 * 1024**2
        assert retained == prep["retainedBytes"] <= 56 * 1024**2
    target = FOLDER / "attempt-565"
    assert not target.exists()
    shutil.copytree(ATTEMPT, target)
    artifacts = []
    for path in sorted(target.iterdir()):
        assert sha(path) == sha(ATTEMPT / path.name)
        row = {"path": path.relative_to(R).as_posix(), "sha256": sha(path), "bytes": path.stat().st_size}
        if path.suffix == ".txt":
            raw = path.read_bytes()
            compressed = path.with_suffix(".raw.txt.gz")
            compressed.write_bytes(gzip.compress(raw, mtime=0))
            assert gzip.decompress(compressed.read_bytes()) == raw
            readable = "\n".join(line.rstrip() for line in raw.decode("utf-8-sig").splitlines()).rstrip() + "\n"
            path.write_text(readable, encoding="utf-8")
            row.update(originalSha256=row["sha256"], sha256=sha(path), bytes=path.stat().st_size,
                       compressedRaw=compressed.relative_to(R).as_posix(), compressedRawSha256=sha(compressed),
                       normalization="Readable UTF-8/no BOM with trailing whitespace removed; exact original bytes in gzip.")
        artifacts.append(row)
    recipes = FOLDER / "execution-565-receipts"
    recipes.mkdir()
    for path in (Path(__file__), C / "run-565-native.ps1", C / "post-565-issue.ps1"):
        shutil.copyfile(path, recipes / path.name)
        artifacts.append({"path": (recipes / path.name).relative_to(R).as_posix(), "sha256": sha(path)})
    sheets_path = C / "artifacts" / "batch-082-corrected-inspection-565"
    shutil.copytree(sheets_path, FOLDER / "inspection-execution-565")
    visual = {
        "snapshot": HEAD, "correctedTeachingSnapshot": "9ce870d190d5c519d65ed20b118de64371350c0c",
        "contentVersion": route["contentVersion"],
        "reviewer": "Coordinator GPT-6.1 Sol (gpt-6.1-sol), NOT independent two-family visual confirmation",
        "method": "51 original1080x2400 PNGs grouped into28 exact-byte groups. All28 representatives inspected in five labelled contact sheets; originals thumbnailed468x1040 inside sheets. Three original Compose font panels and original meaning question/feedback additionally viewed directly. Viewer fits large images: direct returns900x2000, sheets may be downscaled further. Not51 separate full-resolution reads.",
        "scope": "Corrected actual meaning choices/feedback; complete准/准教授 text across scroll states, exact教common-word bullet and助教授successor paragraph; six link directions/SystemBack, N1selection, reading/drawing;34Han/fourfamilies.",
        "coordinatorDisplayResult": "No actionable blank/replacement glyph, misleading look-alike, truncation of the corrected four choice labels or article rendering defect established in inspected scope. Independent changed-runtime visual acceptance outstanding.",
        "glyphInspection": {
            "characters": prep["plannedGlyphs"], "families": ["Gothic", "Mincho", "Textbook", "Brush"],
            "directlyViewedPanels": [f"n1-082-corrected-font-panel-{i}.png" for i in range(1, 4)],
            "fallbackScope": ["冫", "氵", "辶", "隹"],
            "observations": "All34 scoped Han and准教授 are readable in actual panels. New冴/冶 differ by right牙/台, 隼 includes lower十 versus隹. 准/準 distinguishable by two/three left marks and lower十; 冫/氵,辶,隹 are visible standalone shapes. Typefaces differ; exact fallback face not identified."
        },
        "meaningInspection": "Original question and feedback show clear; sharp-minded / quasi-; associate rank / falcon / smelt; work metals, all four untruncated. Only quasi-; associate rank selected as correct. Production question model asserts exact准/冴/冶/隼. No imitate option or tag fallback in this bounded run.",
        "articleInspection": "Complete new text visible collectively across scroll states. Reading labels/type/example use horizontal table states, not all columns simultaneously. Rank definitions/examples/notes/source attribution visible; exact教common-word bullet and助教授successor paragraph readable. SystemBack returns to actual source articles.",
        "sessionInspection": "N1selected114cards; meaning correct, soleジュン key correct and1/1 completed. Guided10stroke trace and giveup recall feedback visible. Model unavailable/shape-only fallback explicitly shown.",
        "findings": [], "independentVisualAcceptance": False, "phoneAcceptance": False,
        "limits": [
            "Coordinator contact-sheet/direct-view inspection is not independent two-family closure, native-speaker certification, human learning evidence or physical-phone usability acceptance.",
            "Original1080x2400 images preserved. Direct viewer return900x2000 and further-downscaled contact sheets are not full-resolution reads;28representatives cover51 byte-grouped captures.",
            "140 Paint records mean136 individual probes plus4 whole-word rasters, not140 PNGs or proof of a specific system fallback face.",
            "Article scroll/table states collectively expose text; not every line/column is simultaneously visible.",
            "Injected reference tracing, shape-only offline grading and giveup recall are not handwriting recognizer accuracy, successful MLKit download or human memory evidence.",
            "Disposable synthetic source/settings/progress on API35 emulator; no owner progress or other device modified.",
            "Exact default four-choice N1 pool with all candidates present only; custom/partial/larger/future pools are not certified.",
            "All original source/reviewer/citation/lookup/read-depth/permission/OOM/process/viewport/fallback/MLKit limits remain. Old uncorrected reports remain historical; rare准える is not invalidated.",
            "No new blind initial review, independent visual review, integration, publication, CI, immutable GitHub ZIP, phone/general-release or whole-set acceptance claimed."
        ]
    }
    index = {
        "originalPngCount": 51, "distinctByteGroups": 28, "originalDimensions": [1080, 2400],
        "inspectionMethod": visual["method"],
        "groups": [{"sha256": digest, "contactSheetRepresentative": names[0], "originals": names}
                   for digest, names in groups.items()],
        "contactSheets": [{"file": p.name, "sha256": sha(p)} for p in sorted(sheets_path.glob("*.png"))]
    }
    save(FOLDER / "visual-inspection-execution-565.json", visual)
    save(FOLDER / "image-index-execution-565.json", index)
    ev = {
        **state, "schemaVersion": 1, "checkpoint": 565, "status": "continue",
        "stage": "batch-082-corrected-native-passed-awaiting-independent-visual-confirmations",
        "completedAt": now(), "nativeExecution": native, "articleRoute": route,
        "nativeRasterRecords": {"rows": 140, "individualGlyphProbes": 136, "wholeWordRasterProbes": 4,
                               "panels": 3, "path": (target / "n1-082-corrected-font-raster.json").relative_to(R).as_posix(),
                               "sha256": sha(target / "n1-082-corrected-font-raster.json")},
        "visualInspection": visual, "imageIndex": index, "archivedReceipts": artifacts,
        "rawAttemptAndOriginalPngBytesPreserved": True,
        "priorUncorrectedFixtureAndArchivePreserved": True,
        "productionSingleArchiveImport": True, "exactRuntimeHashesVerified": verified,
        "originalArchiveBudgetsReverified": True, "runtimeBytesUnchanged": True,
        "freshNativeAcceptance": True, "independentVisualAcceptance": False, "runtimePublished": False,
        "independentVisualReviewersLaunched": 0, "sourceLevelFinding082V1": "resolved",
        "overallRuntimeAcceptance": "UNVERIFIED pending independent corrected-pixel confirmations",
        "inheritedFreshHostGate": "execution563 corrected3+1+5/no skips, not rerun",
        "inheritedNativeCompile": "execution564 exact frozen app/test APKs, no compile rerun or HOST-only heap init",
        "qualifiedAndroidHead": AH, "originalProductionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "otherOwnerDevices": "Fresh device list/preexisting emulator inventory empty. Owned5580 parent25860/QEMU12960 only; both stopped.",
        "manifestFresh": True, "manifestBytesUnchanged": True,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": state["freshOriginMain"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "diagnostics": ["Initial complete checkpoint console print hit cp1252 UnicodeEncodeError only after full load/parse; final checkpoint subsequently read directly. No permission denial or artifact loss."],
        "nextAction": NEXT, "limits": visual["limits"]
    }
    save(EVIDENCE, ev)
    ledger_path = R / "docs" / "n1-sources" / "batch-082-progress.json"
    ledger = load(ledger_path)
    assert "preCorrectedNative565AcceptanceState" not in ledger
    ledger["preCorrectedNative565AcceptanceState"] = {
        k: ledger[k] for k in ("status", "nextAction", "limits", "fontDisposition", "nativeEvidence",
                              "independentVisualAcceptance", "nativeExecutionCases") if k in ledger
    }
    ledger.update(status=ev["stage"], nextAction=NEXT, limits=visual["limits"],
                  fontDisposition="Fresh565 corrected34Han/fourfamilies readable in3 actual Compose panels including冴/冶/隼 and冫/氵/辶/隹 in coordinator inspection; independent changed-runtime two-family visual closure/phone outstanding.",
                  nativeEvidence=EVIDENCE.relative_to(R).as_posix(), nativeExecutionCases=2,
                  independentVisualAcceptance=False)
    save(ledger_path, ledger)
    print("Corrected native evidence archived:2 terminal-zero cases;51PNG/28groups;8372runtime hashes.")


def verify():
    ev = load(EVIDENCE)
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    prefix = "docs/n1-reviews/batch-082-native-corrected/"
    assert staged and all(p.startswith(prefix) or p in {
        "docs/n1-sources/execution-565.json", "docs/n1-sources/batch-082-progress.json"} for p in staged)
    for row in ev["archivedReceipts"]:
        assert sha(R / row["path"]) == row["sha256"], row["path"]
        if "compressedRaw" in row:
            compressed = R / row["compressedRaw"]
            assert sha(compressed) == row["compressedRawSha256"]
            assert hashlib.sha256(gzip.decompress(compressed.read_bytes())).hexdigest() == row["originalSha256"]
    for row in ev["imageIndex"]["groups"]:
        for name in row["originals"]:
            assert sha(FOLDER / "attempt-565" / name) == row["sha256"]
    for row in ev["imageIndex"]["contactSheets"]:
        assert sha(FOLDER / "inspection-execution-565" / row["file"]) == row["sha256"]
    for path in staged:
        assert subprocess.check_output(["git", "show", ":" + path], cwd=R) == (R / path).read_bytes(), path
        if path.endswith(".json"):
            load(R / path)
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=R, check=True)
    assert runtime()["manifestSha256"] == ev["manifestSha256"]
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("status", "--porcelain", root=A)
    print(json.dumps({"stagedFiles": len(staged), "allIndexBytesExact": True, "runtimeUnchanged": True}))


def checkpoint():
    before, p, ev = load(BEFORE), load(C / "progress.json"), load(EVIDENCE)
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=A)
    assert not git("diff", HEAD, signed, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert runtime()["manifestSha256"] == ev["manifestSha256"]
    receipt = load(C / "execution-565-issue-receipt.json")
    body = (C / "execution-565-issue-body.txt").read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").strip() == body and signed in body
    result = {
        "schemaVersion": 1, "execution": 565, "checkpoint": 565, "batch": "082",
        "savedCommit": signed, "signature": "G", "status": "continue", "stage": ev["stage"],
        "evidence": EVIDENCE.relative_to(R).as_posix(), "evidenceSha256": sha(EVIDENCE),
        **runtime(), "qualifiedAndroidHead": AH,
        "freshNativeAcceptance": True, "nativeCasesExecuted": 2, "terminalZeroCases": 2, "skips": 0,
        "serial": ev["nativeExecution"]["serial"], "parentEmulatorPid": 25860, "qemuPid": 12960,
        "ownedHelperStopped": True, "ownedQemuStopped": True,
        "originalPngs": 51, "distinctPngGroups": 28, "coordinatorInspectionContactSheets": 5,
        "fontPanelsDirectlyViewed": 3, "meaningQuestionAndFeedbackDirectlyViewed": True,
        "individualGlyphProbes": 136, "wholeWordRasterProbes": 4,
        "exactCorrectedFourMeaningOptions": True, "independentVisualAcceptance": False,
        "runtimePublished": False, "runtimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None
    }
    p.update({k: result[k] for k in ("checkpoint", "status", "stage", "nextAction", "blocker")})
    p["execution565StartingState"]["status"] = "signed-local-corrected-native-checkpoint-complete"
    p["execution565CoordinatorCheckpoint"] = result
    p["batch082CorrectedNativeAcceptance"] = result.copy()
    changed = [key for key, value in before.items() if p.get(key) != value]
    assert not set(changed) - {"checkpoint", "status", "stage", "nextAction", "blocker"}, changed
    assert before.keys() <= p.keys()
    result.update(originalRootKeysCompared=len(before),
                  allOriginalHistoricalRootKeysPreservedExactly=True, changedRootFields=changed)
    temporary = C / "execution-565-progress.tmp.json"
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")
    save(C / "execution-565-final-verification.json", result)
    print(json.dumps({k: result[k] for k in ("checkpoint", "savedCommit", "status", "issueUpdate",
                                             "originalRootKeysCompared")}))


if __name__ == "__main__":
    {"start": start, "sheets": sheets, "record": record, "verify": verify,
     "checkpoint": checkpoint}[sys.argv[1]]()
