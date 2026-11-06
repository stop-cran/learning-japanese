import difflib
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
LOG = C / "logs" / "fe815daf-5f4a-4994-870d-ac724c6ea5cf"
BEFORE = C / "execution-564-progress-before.json"
HEAD = "e108bbeb0fcd4fda3837d955a652f662f72fdac1"
ANDROID_HEAD = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "d82e7fefe3898a70"
FOLDER = R / "docs" / "n1-reviews" / "batch-082-native-corrected"
FIXTURE = FOLDER / "N1Batch082CorrectedNativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-082-corrected-e108bbeb-envelope.zip"
VERIFICATION = C / "batch-082-corrected-native-fixture-verification.json"
EVIDENCE = R / "docs" / "n1-sources" / "execution-564.json"
sys.path.insert(0, str(R / "tools"))
from build_manifest import build_manifest


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def now():
    return datetime.now(timezone.utc).isoformat()


def runtime():
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == VERSION
    count = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert count == 8372
    return {"contentVersion": VERSION, "runtimeHashesVerified": count,
            "manifestSha256": sha(R / "manifest.json")}


def start():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 563 and p["status"] == "continue" and p["batch"] == "082"
    assert not BEFORE.exists()
    for root, head in [(R, HEAD), (A, ANDROID_HEAD)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    request = LOG / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 563
    save(BEFORE, p)
    state = {
        "execution": 564, "batch": "082", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID_HEAD,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME082 corrected full native archive/fixture preparation and compile only; no native execution, device launch, reviewer, publication or083.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, complete issue and final563 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."
        },
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "dedicatedWorktreesInitiallyClean": True, **runtime(),
        "status": "corrected-native-preparation-in-progress"
    }
    p["execution564StartingState"] = state
    p["stage"] = "batch-082-corrected-native-preparation-in-progress"
    p["nextAction"] = state["scope"]
    save(C / "progress.json", p)
    save(C / "execution-564-start.json", state)
    print("Starting scope persisted; complete live history preserved.")


def prepare():
    from fontTools.ttLib import TTFont

    assert git("rev-parse", "HEAD") == HEAD
    assert not git("status", "--porcelain", root=A)
    assert not FIXTURE.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    previous = load(R / "docs" / "n1-sources" / "batch-082-native-fixture-verification.json")
    old_fixture = Path(previous["fixture"])
    old_archive = Path(previous["archive"])
    assert sha(old_fixture) == previous["fixtureSha256"]
    assert sha(old_archive) == previous["archiveSha256"]
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-082-choice-reconciliation.json")
    assert reconciliation["correctedSnapshot"] == "9ce870d190d5c519d65ed20b118de64371350c0c"
    assert reconciliation["currentRuntimeVerdict"] == "UNVERIFIED"
    assert not git("diff", reconciliation["correctedSnapshot"], HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")
    audit = load(R / "docs" / "n1-sources" / "batch-082-choice-correction-audit.json")
    glyphs = audit["fontScope"]["actualHan"]
    assert len(glyphs) == 34 and glyphs == sorted(set(glyphs))
    assert audit["fontScope"]["newComparedWithPreviousScope"] == ["冴", "冶", "隼"]
    fonts = []
    for item in audit["fontScope"]["fonts"]:
        path = Path(item["path"])
        assert sha(path) == item["sha256"]
        with TTFont(path) as font:
            missing = [c for c in glyphs if ord(c) not in font.getBestCmap()]
        assert missing == item["allActualMissing"] == ["冫", "氵", "辶", "隹"]
        fonts.append({**item, "missingCurrentScopedHan": missing})
    text = old_fixture.read_text(encoding="utf-8")
    original = text
    replacements = [
        ("disposable082", "disposable082Corrected"),
        ("N1Batch082GlyphTest", "N1Batch082CorrectedGlyphTest"),
        ("N1Batch082ArticleTest", "N1Batch082CorrectedArticleTest"),
        (previous["contentSnapshot"], HEAD),
        ("n1-batch-082-4f5812bc-envelope.zip", ARCHIVE.name),
        (previous["contentVersion"], VERSION),
        ('"n1-082-', '"n1-082-corrected-'),
        ("Batch 082: associate rank", "Batch 082 corrected: associate rank"),
        ("31 scoped Han", "34 scoped Han"),
        ("31 actual scoped Han", "34 actual scoped Han"),
        ("focused 准/準/集/進/難", "focused 准/冴/冶/隼/準"),
        ("assertEquals(128, rows.length())", "assertEquals(140, rows.length())"),
        ('.put("individualGlyphProbes", 124)', '.put("individualGlyphProbes", 136)'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("准 冴 冶 隼 準 冫 氵 辶 隹 准教授")
    text, count = re.subn(r"val pages = listOf\([^\n]+\)",
                         "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    assert count == 1
    text, count = re.subn(r"for \(char in listOf\([^\n]+\)",
                         "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    assert count == 1
    old_question = '            assertEquals("准", (quiz.ui as QuizUi.Question).card.kanji)\n'
    assert text.count(old_question) == 1
    question = """            val meaning = quiz.ui as QuizUi.Question
            assertEquals("准", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "准" to "quasi-; associate rank",
                "冴" to "clear; sharp-minded",
                "冶" to "smelt; work metals",
                "隼" to "falcon",
            )
            assertEquals(4, meaning.options.size)
            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })
            assertFalse(meaning.options.any { it.kanji == "倣" })
            assertEquals(listOf("冴", "冶", "隼"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("exactCuratedChoicesWithoutFallback", true)
"""
    text = text.replace(old_question, question)
    for anchor in [
        '        assertEquals(listOf("ジュン"), associateRank.onyomi.splitSep())',
        '            assertEquals(listOf("ジュン"), card.onyomi.splitSep())',
    ]:
        assert text.count(anchor) == 1
        name = "associateRank" if "associateRank" in anchor else "card"
        indent = anchor[:len(anchor) - len(anchor.lstrip())]
        text = text.replace(anchor, indent + f'assertEquals(listOf("冴", "冶", "隼"), {name}.distractors.splitSep())\n' + anchor)
    for selector in previous["staticMarkdownSelectors"]:
        assert quote(selector["target"]) in text, selector
    for offset in previous["staticLinkedOffsets"]:
        assert quote(offset["renderedText"]) in text, offset
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    assert "0739a82c9699f031" not in text and "n1-batch-082-4f5812bc" not in text
    assert all(v in text for v in (
        "assertEquals(1094, updated.kanji)", "assertEquals(5050, updated.words)",
        "assertEquals(114, n1.size)", "assertEquals(10, strokes.length())",
        "assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)",
        'assertEquals(listOf("じゅん"), associateRank.toReadingCard().quizKeys(ReadingKind.On))',
        'assertEquals(emptyList<String>(), associateRank.toReadingCard().quizKeys(ReadingKind.Kun))',
        '.put("directedLinkTransitions", 4)', '.put("comparisonLinkTransitions", 2)',
    ))
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-082-corrected/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    manifest = load(R / "manifest.json")
    with zipfile.ZipFile(ARCHIVE) as archive:
        prefix = "n1-batch-082-corrected/"
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith(prefix) and "\\" not in n and ".." not in n.split("/") for n in entries)
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
        raw = archive.read(prefix + "manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=R)
        assert json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, mapping in manifest.items():
            if not isinstance(mapping, dict):
                continue
            for name, expected in mapping.items():
                data = archive.read(prefix + name)
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected, name
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in archive.infolist())
    assert verified == 8372
    assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
    assert inflated <= 80 * 1024 * 1024 and retained <= 56 * 1024 * 1024
    FOLDER.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-uncorrected-082.diff"
    diff.write_text("".join(difflib.unified_diff(
        original.splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=old_fixture.relative_to(R).as_posix(), tofile=FIXTURE.relative_to(R).as_posix(), n=0)),
        encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 564, "batch": "082", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "correctedTeachingSnapshot": reconciliation["correctedSnapshot"],
        "androidSnapshot": ANDROID_HEAD, "contentVersion": VERSION,
        "productionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "expectedCounts": {"kanji": 1094, "words": 5050, "n1": 114},
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE),
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "fixtureDiff": diff.relative_to(R).as_posix(), "fixtureDiffSha256": sha(diff),
        "priorFixture": str(old_fixture), "priorFixtureSha256": sha(old_fixture),
        "priorArchive": str(old_archive), "priorArchiveSha256": sha(old_archive),
        "priorArtifactsPreserved": True,
        "zipEntries": len(entries), "compressedBytes": ARCHIVE.stat().st_size,
        "inflatedBytes": inflated, "retainedBytes": retained, "verifiedRuntimeHashes": verified,
        "manifestEqual": True, "originalBudgetsPassed": True,
        "plannedGlyphs": glyphs, "plannedNativePaintProbes": 136,
        "plannedWholeWords": ["准教授"], "plannedWholeWordRasterProbes": 4,
        "plannedComposePanels": pages, "currentFontAudit": fonts,
        "staticMarkdownSelectors": previous["staticMarkdownSelectors"],
        "staticLinkedOffsets": previous["staticLinkedOffsets"],
        "completeArticleProjections": 2, "changedReusedPassages": 2,
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
        "comparisonPairs": 1, "comparisonDirectedTransitions": 2,
        "expectedMeaningOptions": {"准": "quasi-; associate rank", "冴": "clear; sharp-minded",
                                   "冶": "smelt; work metals", "隼": "falcon"},
        "fullReadings": {"on": ["ジュン"], "kun": []},
        "curatedReadings": {"on": ["ジュン"], "kun": []},
        "normalizedQuizKeys": {"on": ["じゅん"], "kun": []},
        "nativeClassNames": ["N1Batch082CorrectedGlyphTest", "N1Batch082CorrectedArticleTest"],
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": "Preparation only. Static selectors and hashes do not prove native visibility/readability/fallback faces. Corrected runtime requires fresh two-case terminal0, PNG inspection and both original-family dependent visual confirmations. No HOST2g init, app/guest heap change or guard relaxation. Device/port/PID ownership must be inspected immediately before any later launch. Original source/reviewer/denial/OOM/process/viewport/fallback/MLKit limits retained."
    }
    save(VERIFICATION, record)
    print(json.dumps({k: record[k] for k in ("status", "zipEntries", "verifiedRuntimeHashes",
                                             "compressedBytes", "inflatedBytes", "retainedBytes")}))


def record():
    state, prep = load(C / "execution-564-start.json"), load(VERIFICATION)
    assert not git("status", "--porcelain", root=A)
    assert git("rev-parse", "HEAD", root=A) == ANDROID_HEAD
    assert sha(FIXTURE) == prep["fixtureSha256"] and sha(ARCHIVE) == prep["archiveSha256"]
    assert sha(Path(prep["priorFixture"])) == prep["priorFixtureSha256"]
    assert sha(Path(prep["priorArchive"])) == prep["priorArchiveSha256"]
    assert (LOG / "native-compile-exit.txt").read_text().strip() == "0"
    raw_log = (LOG / "native-compile.txt").read_bytes()
    build = next(line for line in raw_log.decode("utf-8-sig").splitlines() if line.startswith("BUILD SUCCESSFUL"))
    apk = C / "artifacts" / "n1-batch-082-corrected-564-native-test.apk"
    app = C / "artifacts" / "n1-batch-082-corrected-564-native-app.apk"
    assert sha(app) == "0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407"
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in prep["nativeClassNames"]:
            assert name.encode() in dex
    artifacts = []
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    for source in [Path(__file__), C / "run-564-native-compile.ps1", VERIFICATION]:
        target = receipts / source.name
        shutil.copyfile(source, target)
        artifacts.append({"path": target.relative_to(R).as_posix(), "sha256": sha(target)})
    for source in sorted(LOG.glob("native-compile*.txt")):
        target = receipts / source.name
        if source.name == "native-compile.txt":
            raw = receipts / "native-compile-raw.txt.gz"
            raw.write_bytes(gzip.compress(raw_log, mtime=0))
            assert gzip.decompress(raw.read_bytes()) == raw_log
            artifacts.append({"path": raw.relative_to(R).as_posix(), "sha256": sha(raw),
                              "decompressedSha256": sha(source)})
            target.write_text("\n".join(line.rstrip() for line in raw_log.decode("utf-8-sig").splitlines()) + "\n",
                              encoding="utf-8")
        else:
            target.write_text(source.read_text(encoding="utf-8-sig"), encoding="utf-8")
        artifacts.append({"path": target.relative_to(R).as_posix(), "sha256": sha(target),
                          "sourceSha256": sha(source)})
    command = load(LOG / "native-compile-command.json")
    save(receipts / "native-compile-command.json", command)
    artifacts.append({"path": (receipts / "native-compile-command.json").relative_to(R).as_posix(),
                      "sha256": sha(receipts / "native-compile-command.json")})
    frozen = R / "docs" / "n1-sources" / VERIFICATION.name
    shutil.copyfile(VERIFICATION, frozen)
    next_action = (
        "SAME082 corrected native execution and actual PNG inspection NEXT, then persist/yield. "
        "Read execution-564.json and batch-082-corrected-native-fixture-verification.json. "
        "Use ONLY corrected signed e108bbeb archive/versiond82e7fefe3898a70, corrected fixture and "
        "corrected-564 test/app APKs with exact recorded hashes; do not reuse old559/560/561 acceptance. "
        "No redundant HOST/compile/blind initial review absent new concern. Fresh device/5580/5581/PID "
        "ownership immediately before any launch; old batch0405584 exception was batch-specific. "
        "Approved API35 N3_Acceptance_20261029 read-only/no-snapshot/no-window/no-audio/hostGPU/-Vulkan/"
        "2048MiB2cores; explicit actual serial, stop only owned helper. Qualified TEST-ONLY Android "
        "1c1b7bf4/G preserves productionf9b59a2, HOST-only2g init NEVER native. Require both "
        "N1Batch082CorrectedGlyphTest and N1Batch082CorrectedArticleTest terminal0/no skips. "
        "Production ContentSync ONCE1094kanji5050words114N1/versiond82e7fefe3898a70/zeroProblems/"
        "acceptedepoch1. Actual four meaning options exactly准/冴/冶/隼 and exact titles, no倣/tagfallback; "
        "Full+Lite curatedonジュン/kun[] and soleじゅん key. All34Han/fourfamilies136individual+4wholeword"
        "rasters/3Composepanels including new冴/冶/隼 plus冫/氵/辶/隹; inspect actual PNGs. Complete"
        "准/准教授 plus exact教bullet/助教授successor paragraph; 2mappedpairs4directions+comparison2directions;"
        "N1selection/meaning/singleon/10stroke trace then recall/SystemBack/offline. Injected trace/giveup "
        "NOT humanrecall/recognition/MLKit/phone. Then serial original-family dependent changed-runtime "
        "visual confirmations ClaudeOpus5.5 session1c5aebb9-9903-4567-a88a-5da4b472781d then GPT6.1Sol "
        "sessionfd9a447c-6e9f-4874-a043-4851de97c996. 082-V1 source fix confirmed at9ce870d1; runtime "
        "remainsUNVERIFIED until fresh acceptance. Defaultfour N1/All allvalidcandidates only; custom/"
        "partial/larger/futurepools not certified. Rare准える imitation recognized; ordinary standalone "
        "frequency/learnerimpact unproven, not invalidated. Preserve ALL original source/lookup/citation/"
        "readdepth/denial/OOM/process/viewport/fallback/MLKit limits. AFTER acceptance latestmain/"
        "nonrewritingintegration/combinedPython368/validator/vocabulary/manifest/exact虎猿/baseline/link/"
        "membership/original18000entries42MiBcompressed80MiBinflated56MiBretainedguards/normal signedowner"
        "fastforward/remoteSHA/terminalgreenCI/EVERYimmutableZIPhash/verifiedownerissue60 before083. "
        "Published108/1228,remaining1120,lastPublished1f317f0762513720709ab0ca215f19ff021ca596;082NOTdelivered. "
        "Phone/generalrelease/whole-setoutstanding. Full live history, approved workspace/committed source/"
        "controlhelpers only; no optionalhistoricalsessionrecipe access. Onecoordinator/oneactive reviewer/"
        "no secondrunner. Actualnewdenial/signinghang preserve/report/yield withoutworkaround."
    )
    evidence = {
        **state, "schemaVersion": 1, "checkpoint": 564, "status": "continue",
        "stage": "batch-082-corrected-native-compiled-awaiting-execution", "completedAt": now(),
        "nativePreparation": prep, "fixtureVerification": frozen.relative_to(R).as_posix(),
        "fixtureVerificationSha256": sha(frozen), "archivedReceipts": artifacts,
        "compile": {**command, "exitCode": 0, "buildResult": build, "apk": str(apk),
                    "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
                    "appApk": str(app), "appApkSha256": sha(app),
                    "apkContainsExactFrozenArchive": True, "bothClassesInDex": True,
                    "temporarySourceAndAssetRemoved": True, "androidWorktreeClean": True,
                    "productionOrGuestHeapChanged": False, "archiveGuardsChanged": False,
                    "hostOnlyHeapInitUsed": False},
        "inheritedHostGate": "execution563 corrected runtime HOST3+1+5 zero failures/errors/skips; not rerun.",
        "textualClosure": "docs/n1-reviews/batch-082-choice-reconciliation.json",
        **runtime(), "runtimeBytesUnchanged": True, "runtimePublished": False,
        "freshNativeAcceptance": False, "independentVisualAcceptance": False,
        "nativeCasesExecuted": 0, "deviceOrEmulatorInspected": False,
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": state["freshOriginMain"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": next_action,
        "limits": "Compile/preparation only; no fresh native/pixel/visual/phone acceptance. Old fixtures and archives preserved unchanged. All original source/reviewer/read-depth/citation/lookup/denial/OOM/process/viewport/fallback/MLKit limits retained.",
        "diagnostics": [
            "First final-checkpoint console output hit cp1252 UnicodeEncodeError after full file load/parse; bounded UTF-8 output then succeeded.",
            "Two guessed contributor file paths were absent; actual committed paths found and read. No permission denial or missing mandatory evidence."
        ]
    }
    save(EVIDENCE, evidence)
    print(json.dumps({"stage": evidence["stage"], "testApkSha256": sha(apk),
                      "runtime": runtime()}, ensure_ascii=True))


def refresh_diff():
    prep, ev = load(VERIFICATION), load(EVIDENCE)
    assert sha(FIXTURE) == prep["fixtureSha256"]
    prior = Path(prep["priorFixture"])
    assert sha(prior) == prep["priorFixtureSha256"]
    diff = R / prep["fixtureDiff"]
    diff.write_text("".join(difflib.unified_diff(
        prior.read_text(encoding="utf-8").splitlines(keepends=True),
        FIXTURE.read_text(encoding="utf-8").splitlines(keepends=True),
        fromfile=prior.relative_to(R).as_posix(), tofile=FIXTURE.relative_to(R).as_posix(), n=0)),
        encoding="utf-8")
    prep["fixtureDiffSha256"] = sha(diff)
    save(VERIFICATION, prep)
    for path in [R / ev["fixtureVerification"],
                 FOLDER / "preparation-receipts" / VERIFICATION.name]:
        shutil.copyfile(VERIFICATION, path)
    shutil.copyfile(Path(__file__), FOLDER / "preparation-receipts" / Path(__file__).name)
    ev["nativePreparation"] = prep
    ev["fixtureVerificationSha256"] = sha(R / ev["fixtureVerification"])
    for item in ev["archivedReceipts"]:
        item["sha256"] = sha(R / item["path"])
    ev["diagnostics"].append(
        "Staged whitespace check flagged unified-diff blank context prefixes, not Kotlin whitespace. Regenerated the evidence-only diff with zero context and refreshed its exact hashes; frozen fixture/archive/APKs unchanged.")
    save(EVIDENCE, ev)


def checkpoint():
    p, before, ev = load(C / "progress.json"), load(BEFORE), load(EVIDENCE)
    saved = git("rev-parse", "HEAD")
    assert saved != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=A)
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert runtime()["manifestSha256"] == ev["manifestSha256"]
    receipt = load(C / "execution-564-issue-receipt.json")
    body = (C / "execution-564-issue-body.txt").read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").strip() == body and saved in body
    result = {
        "schemaVersion": 1, "execution": 564, "checkpoint": 564, "batch": "082",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": ev["stage"],
        "evidence": EVIDENCE.relative_to(R).as_posix(), "evidenceSha256": sha(EVIDENCE),
        **runtime(), "qualifiedAndroidHead": ANDROID_HEAD,
        "compileExitCode": 0, "freshNativeAcceptance": False, "independentVisualAcceptance": False,
        "nativeCasesExecuted": 0, "runtimeBytesUnchanged": True, "runtimePublished": False,
        "testApkSha256": ev["compile"]["apkSha256"],
        "archiveSha256": ev["nativePreparation"]["archiveSha256"],
        "fixtureSha256": ev["nativePreparation"]["fixtureSha256"],
        "priorFixtureAndArchivePreserved": True, "dedicatedWorktreesClean": True,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": ev["nextAction"], "blocker": None
    }
    p.update({k: result[k] for k in ["checkpoint", "status", "stage", "nextAction", "blocker"]})
    p["execution564StartingState"]["status"] = "signed-local-corrected-native-compile-checkpoint-complete"
    p["execution564CoordinatorCheckpoint"] = result
    p["batch082CorrectedNativePreparation"] = result.copy()
    changed = [key for key, value in before.items() if p.get(key) != value]
    assert not set(changed) - {"checkpoint", "status", "stage", "nextAction", "blocker"}, changed
    assert before.keys() <= p.keys()
    result.update(originalRootKeysCompared=len(before),
                  allOriginalHistoricalRootKeysPreservedExactly=True, changedRootFields=changed)
    temporary = C / "execution-564-progress.tmp.json"
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")
    save(C / "execution-564-final-verification.json", result)
    print(json.dumps({k: result[k] for k in ("checkpoint", "savedCommit", "status", "issueUpdate",
                                             "originalRootKeysCompared")}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record,
     "refresh-diff": refresh_diff, "checkpoint": checkpoint}[sys.argv[1]]()
