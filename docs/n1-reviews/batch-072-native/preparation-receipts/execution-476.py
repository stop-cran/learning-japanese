import ast
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

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOG = CONTROL / "logs" / "e31a72e6-5f90-44dd-a490-fac5f89fb805"
HEAD = "92f3c2ef6edbeb8dd7b6e7f37227cab8a3e20891"
REVIEWED = "5544e65205879a67b9fc7a127bb6ef4a15152069"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-072-native"
SOURCES = ROOT / "docs" / "n1-sources"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-071-native" / "N1Batch071NativeTest.kt"
FIXTURE = FOLDER / "N1Batch072NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-072-92f3c2ef-envelope.zip"
APK = CONTROL / "artifacts" / "n1-batch-072-native-test.apk"
NEXT = (
    "SAME072: execute compiled control\\artifacts\\n1-batch-072-native-test.apk "
    "N1Batch072GlyphTest and N1Batch072ArticleTest with exact signed92f3c2ef full Git archive. "
    "Read docs\\n1-sources\\execution-476.json and batch-072-native-preparation.json. "
    "Fresh adb/device and5580/5581 local/remote connection/PID ownership immediately before "
    "read-only N3_Acceptance_20261029 emulator-5580 launch: -port5580 -read-only -no-snapshot "
    "-no-window -no-audio -gpu host -feature -Vulkan -memory2048 -cores2. Record helper parent/QEMU; "
    "stop only owned helper. Batch040 routing override NOT inherited. No HOST heap init/native heap/guard changes. "
    "Require ContentSync ONCE:1084kanji5042words104N1/version900e3a2130afc56b/problems0/epoch1; "
    "Full+Lite rawジュウ andあ.てる/み.たす, curatedジュウ/あ.てる and normalizedじゅう/あてる; "
    "noみたす question/log, BOTH kinds persistedGood/Done2correct. All three reading labels/explanations, "
    "complete new充/充てる projections and exact reused拡充 component paragraph, two reciprocal pairs/four "
    "directions/SystemBack/offline/N1selection/meaning/six reference-touch strokes/ungradedtrace/recallAgain. "
    "All actual authoredHan plus isolated亠/儿/厶 across four production families, actual PNG inspection; "
    "terminalstatus0 for BOTH cases, zero skips. Static selectors/raster hashes are not readability/fallback-face "
    "or phone evidence; reference trace is not human handwriting/MLKit. Fresh475Android3+1 inherited; "
    "do not rerun HOST Gradle absent new concern. After native pass original Claude0e0fbc27-0aba-4217-94a6-74ad8bb21070 "
    "THEN GPTe304bb20-e8fe-4113-b7cb-fb09097cf343 SERIAL dependent visual confirmations on bounded packets. "
    "Then freshmain nonrewriting integration/allcombinedvalidation/normalsigning/ownerfastforward/publicSHA/"
    "greenCI/everyimmutablepublicZIPruntimehash/originalbudgets/ownerissue60 BEFOREdelivery or073. "
    "No secondrunner/supervisor edits/signingretry/permissionworkaround. Published98/1228,remaining1130; "
    "99published necessary supports NOTN1vocabulary. Androidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set acceptance outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def unchanged():
    assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", cwd=ANDROID)


def quote(text):
    return json.dumps(text, ensure_ascii=False).replace("$", "\\$")


mode = sys.argv[1]
if mode == "start":
    p = load(CONTROL / "progress.json")
    assert p["checkpoint"] == 475 and p["status"] == "continue" and p["batch"] == "072"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    unchanged()
    request = (LOG / "request.txt").read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["checkpoint"] == 475
    save(LOG / "execution-476-before-progress.json", p)
    p["execution476StartingState"] = {
        "execution": 476, "batch": "072", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME072 exact full signed Git archive native fixture preparation/compilation and normally signed local evidence checkpoint only; no native/reviewer/publication/073/second runner.",
        "authorization": {
            "requestSha256": sha(LOG / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete approved issue and complete final475 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
        "androidHead": git("rev-parse", "HEAD", cwd=ANDROID),
    }
    p["stage"] = "batch-072-native-preparation-in-progress"
    save(CONTROL / "progress.json", p)
    print("Starting native-preparation scope persisted; complete live history retained.")
elif mode == "prepare":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    unchanged()
    assert not FOLDER.exists() and not ARCHIVE.exists() and not APK.exists()
    manifest = load(ROOT / "manifest.json")
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
        "words": sum(n.startswith("words/") for n in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (ROOT / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1084, "words": 5042, "n1": 104}
    assert manifest["contentVersion"] == "900e3a2130afc56b"
    helper = ROOT / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    functions = ast.Module(body=[n for n in parsed.body if isinstance(n, ast.FunctionDef)
                                and n.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(functions, str(helper), "exec"), namespace)
    names = ["kanji/充.md", "words/充てる.md", "words/拡充.md"]
    documents = {n: namespace["blocks"](ROOT / n) for n in names}
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def display(document, slug, complete=True):
        projected = documents[document]
        line(f"await({quote(projected[0][1])})")
        table_cell = 0
        section_name = None
        for index, (kind, value) in enumerate(projected[1:], 1):
            if kind == "heading":
                section_name = value
                if complete or value == "How the kanji combine":
                    line(f"section({quote(value)})")
                continue
            if not complete and section_name != "How the kanji combine":
                continue
            if kind == "table":
                table_cell += 1
                if table_cell <= 3 or table_cell % 3 == 2:
                    continue
            qualifier = "readingExample" if kind == "table" else "articleBullet"
            candidates = [(k, v) for k, v in projected if v == value and
                          ((k == "table") if kind == "table" else (k not in ("table", "heading")))]
            assert len(candidates) == 1, (document, value)
            step = f"{slug}-{index:02}"
            line(f"show({qualifier}({quote(value)}), {quote(step)})")
            selectors.append({"document": document, "kind": kind, "target": value, "step": step})

    def follow(document, label, destination, section_name):
        body = (ROOT / document).read_text(encoding="utf-8")
        section_body = body.split("## " + section_name + "\n", 1)[1].split("\n## ", 1)[0]
        raw_parts = re.split(r"\n\s*\n|\n(?=- )", section_body.strip())
        raw = next(part.removeprefix("- ") for part in raw_parts if f"[{label}](" in part)
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        assert (ROOT / document).parent.joinpath(link[1]).resolve() == (ROOT / destination).resolve()
        text = namespace["plain"](" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_476" + raw[link.end():]
        offset = namespace["plain"](" ".join(marked.splitlines())).index("N1_LINK_TARGET_476")
        assert text[offset:].startswith(label)
        line(f"section({quote(section_name)})")
        line(f"inline(await(articleBullet({quote(text)})), {quote(label)}, {offset})")
        offsets.append({"document": document, "destination": destination, "label": label,
                        "renderedText": text, "offset": offset})

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("充")')
    line('click("allot; fill")')
    display("kanji/充.md", "kanji")
    for word, slug, complete in (("充てる", "word-new", True), ("拡充", "word-reused", False)):
        follow("kanji/充.md", word, f"words/{word}.md", "Common words")
        display(f"words/{word}.md", slug, complete)
        follow(f"words/{word}.md", "充", "kanji/充.md", "How the kanji combine")
        line('await("Article contents")')
        line('section("Readings")')
        line(f'show(readingExample("拡充 かくじゅう — expansion; strengthening"), "{slug}-kanji-backlink")')
        for item, section_name, step in (
            (offsets[-1], "How the kanji combine", f"{slug}-system-back-word-kanji"),
            (offsets[-2], "Common words", f"{slug}-system-back-kanji-word"),
        ):
            line("back()")
            line(f"await(articleBullet({quote(item['renderedText'])})).assertIsDisplayed()")
            line(f"section({quote(section_name)})")
            line(f"capture({quote(step)})")

    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("071", "072"),
        ("permissionLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies",
         "allotmentLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies"),
        ("fullSingleImportOfflinePermissionReciprocalPairOnOnlyDrawingAndSystemBack",
         "fullSingleImportOfflineAllotmentTwoReciprocalPairsBothReadingsDrawingAndSystemBack"),
        ("f6ff96a109f3e7b6a67f41e6b9ee214962c9a39f", HEAD), ("f6ff96a1", HEAD[:8]),
        ("05002d6e68a4eb89", manifest["contentVersion"]),
        ("1083", "1084"), ("5041", "5042"), ("103, n1.size", "104, n1.size"),
        ("N1 · 103 cards", "N1 · 104 cards"),
        ("permit; sincerity", "allot; fill"), ("permission", "allotment"), ("允", "充"),
        ("イン", "ジュウ"), ("いん", "じゅう"),
        ("4, strokes.length()", "6, strokes.length()"), ("4 strokes drawn", "6 strokes drawn"),
        ('listOf("じょう", "まこと.に", "ゆるす")', 'listOf("あ.てる", "み.たす")'),
        ('emptyList<String>(), allotment.quizKunyomi?.splitSep()', 'listOf("あ.てる"), allotment.quizKunyomi?.splitSep()'),
        ('emptyList<String>(), card.quizKunyomi?.splitSep()', 'listOf("あ.てる"), card.quizKunyomi?.splitSep()'),
        ('emptyList<String>(), allotment.toReadingCard().quizKeys(ReadingKind.Kun)',
         'listOf("あてる"), allotment.toReadingCard().quizKeys(ReadingKind.Kun)'),
        ('(kind == ReadingKind.On && key == "じゅう")',
         '((kind == ReadingKind.On && key == "じゅう") || (kind == ReadingKind.Kun && key == "あてる"))'),
        ("repeat(1) {", "repeat(2) {"),
        ('assertEquals(ReadingKind.On, question.question.kind)\n                val key = "じゅう"',
         'val key = if (question.question.kind == ReadingKind.On) "じゅう" else "あてる"\n'
         '                assertNotEquals("みたす", question.question.correctKey)'),
        ("setOf(ReadingKind.On), answeredKinds", "setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds"),
        ("1, done.answered", "2, done.answered"), ("1, done.correct", "2, done.correct"),
        ('it.kanji == "充" && it.mode == ReadingKind.Kun.mode.name }',
         'it.kanji == "充" && it.mode == ReadingKind.Kun.mode.name && it.reading == "みたす" }'),
        ('capture("curated-on-only-done")', 'capture("curated-both-done")'),
        ('"soleCuratedOnPersistedGoodNoKunAndDone"', '"bothCuratedKindsPersistedGoodNoMitasuAndDone"'),
        ("sole curated on key due; explicit no-kun with full source kun retained",
         "both curated on/kun keys due; source-only み.たす retained but not offered"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    actual_han = load(SOURCES / "batch-072-draft-audit.json")["actualAuthoredHanFonts"]["characters"]
    glyphs = list(dict.fromkeys(list("充允元兄先亠儿厶口土拡当満") + actual_han))
    words = ["充てる", "拡充"]
    text = re.sub(r'val text = "[^"]+"', "val text = " + quote(" ".join(glyphs + words)), text, count=1)
    text = re.sub(r'Text\("Batch 072:[^"]+"\)',
                  'Text("Batch 072: allotment / look-alikes / isolated radicals")', text)
    text = re.sub(r'Text\("Inspect [^\n]+fontSize = 18.sp\)',
                  'Text("Inspect 充/允/元/兄/先 and isolated 亠/儿/厶. Compare 拡/当/満 and both whole words. Fallback families may coincide.", fontSize = 18.sp)', text)
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
                  "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)',
                  'for (word in listOf("充てる", "拡充"))', text, count=1)
    text = text.replace("assertEquals(112, rows.length())", f"assertEquals({4 * (len(glyphs) + len(words))}, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 108).put("wholeWordRasterProbes", 4)',
                        f'.put("individualGlyphProbes", {4 * len(glyphs)}).put("wholeWordRasterProbes", 8)')
    text = re.sub(r'\.put\("limits", "Native Paint probes[^"]+"\)',
                  '.put("limits", "Native Paint probes cover actual authored Han and isolated 亠/儿/厶; eight whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")', text)
    start = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
    text = text[:start] + "\n".join(lines) + "\n" + text[end:]
    for item in selectors:
        assert quote(item["target"]) in text
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("071", "允可", "まこと.に", "ゆるす", "soleCurated", "on-only", "4 strokes", "イン"):
        assert stale not in text, stale
    assert len(offsets) == 4 and len({(i["document"], i["destination"]) for i in offsets}) == 4
    assert 'listOf("あ.てる", "み.たす"), allotment.kunyomi.splitSep()' in text
    assert 'listOf("あ.てる", "み.たす"), card.kunyomi.splitSep()' in text
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-072/",
                    f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.namelist()
        prefix = "n1-batch-072/"
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith(prefix) and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = z.read(prefix + "manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=ROOT)
        assert json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, mapping in manifest.items():
            if not isinstance(mapping, dict):
                continue
            for name, expected in mapping.items():
                data = z.read(prefix + name)
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected, name
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in z.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    assert verified == 8344
    FOLDER.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-071.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(PRIOR.relative_to(ROOT)), tofile=str(FIXTURE.relative_to(ROOT)), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 476, "batch": "072", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "androidSnapshot": git("rev-parse", "HEAD", cwd=ANDROID),
        "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": str(PRIOR.relative_to(ROOT)), "priorHarnessSha256": sha(PRIOR),
        "staticProjectionHelper": str(helper.relative_to(ROOT)), "staticProjectionHelperSha256": sha(helper),
        "fixtureDiff": str(diff.relative_to(ROOT)), "fixtureDiffSha256": sha(diff),
        "articleFiles": [{"path": n, "sha256": sha(ROOT / n), "projectedTextBlocks": len(b),
                          "scope": "exact changed component paragraph only" if n == "words/拡充.md" else "complete projection"}
                         for n, b in documents.items()],
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 2, "changedReusedPassages": 1,
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
        "plannedNativePaintProbes": 4 * len(glyphs), "plannedWholeWordRasterProbes": 8,
        "plannedGlyphs": glyphs, "plannedWholeWords": words,
        "fullReadings": {"on": ["ジュウ"], "kun": ["あ.てる", "み.たす"]},
        "curatedReadings": {"on": ["ジュウ"], "kun": ["あ.てる"]},
        "normalizedQuizKeys": {"on": ["じゅう"], "kun": ["あてる"]},
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": "Static preparation/compilation only; not native, font/visual, phone or publication acceptance. Complete new prose and all three reading label/example selectors; repeated table type labels not separately asserted. Exact changed reused component paragraph, not a fresh full review of unchanged reused prose. Full Git archive through ContentSync ONCE, unchanged guest/app heap/guards. Raster hashes do not identify fallback face or readability. Reference tracing is not human handwriting/MLKit. No teaching edits.",
        "nextAction": NEXT,
    }
    save(CONTROL / "batch-072-native-fixture-verification.json", record)
    print(json.dumps({k: record[k] for k in (
        "status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes",
        "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print("Unique article selectors:", len(selectors), "; directed links:", len(offsets))
elif mode == "archive":
    unchanged()
    preparation = load(CONTROL / "batch-072-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    raw_log = LOG / "native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (LOG / "native-compile-exit.txt").read_text().strip() == "0" and "BUILD SUCCESSFUL" in compile_text
    with zipfile.ZipFile(APK) as z:
        assert hashlib.sha256(z.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [z.read(n) for n in z.namelist() if re.fullmatch(r"classes\d*\.dex", n)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch072{kind}Test;".encode() in b for b in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch071{kind}Test;".encode() not in b for b in dex)
        for method in ("allotmentLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies",
                       "fullSingleImportOfflineAllotmentTwoReciprocalPairsBothReadingsDrawingAndSystemBack"):
            assert any(method.encode() in b for b in dex)
    (FOLDER / "compile.txt").write_text("\n".join(l.rstrip() for l in compile_text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-476.py")
    shutil.copyfile(CONTROL / "run-476-native-compile.ps1", receipts / "run-476-native-compile.ps1")
    save(SOURCES / "batch-072-native-preparation.json", preparation)
    inherited = load(SOURCES / "execution-475.json")
    for item in inherited["tests"]:
        assert sha(ROOT / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    reports = {}
    for family in ("claude", "gpt"):
        path = ROOT / "docs" / "n1-reviews" / f"batch-072-initial-{family}.md"
        assert git("diff", HEAD, "--", str(path.relative_to(ROOT))) == ""
        reports[family] = {"report": str(path.relative_to(ROOT)), "sha256": sha(path)}
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 900e3a2130afc56b")):
        source = LOG / f"{name}.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = FOLDER / f"{name}.txt"
        target.write_text("\n".join(l.rstrip() for l in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(ROOT)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 476, "batch": "072", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(CONTROL / "progress.json")["execution476StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-072-native-preparation.json",
        "preparationSha256": sha(SOURCES / "batch-072-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "exitCode": 0, "status": "compiled-not-executed",
            "result": re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0),
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "log": str((FOLDER / "compile.txt").relative_to(ROOT)), "logSha256": sha(FOLDER / "compile.txt"),
            "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "apk": str(APK), "apkSha256": sha(APK), "apkBytes": APK.stat().st_size,
            "packagedExactFullArchiveVerified": True, "bothClassesAndMethodsVerified": True,
            "old071DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "completeArticleSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 2, "changedReusedPassages": 1,
            "readingLabelsAndExplanations": 3, "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
        },
        "accepted475AndroidRetainedWithoutRerun": True, "inheritedArchivedXmlHashesReverified": True,
        "originalReportsUnchanged": reports, "runtimeEditsMade": False, "nativeExecuted": False,
        "nativeAcceptance": False, "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 98, "remainingAdditions": 1130,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    record["artifacts"] = [
        {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)}
        for p in sorted(FOLDER.rglob("*")) + [SOURCES / "batch-072-native-preparation.json"] if p.is_file()
    ]
    save(SOURCES / "execution-476.json", record)
    print("Exact packaged archive, both cases, inherited Android and reports verified.")
elif mode == "checkpoint":
    unchanged()
    record = load(SOURCES / "execution-476.json")
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    p = load(CONTROL / "progress.json")
    before = load(LOG / "execution-476-before-progress.json")
    assert all(p[k] == v for k, v in before.items() if k != "stage")
    assert set(p) == set(before) | {"execution476StartingState"}
    checkpoint = {
        "execution": 476, "checkpoint": 476, "batch": "072", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-476.json",
        "recordSha256": sha(SOURCES / "execution-476.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=476, status="continue", stage="batch-072-native-compiled-pending-execution",
             nextAction=NEXT, blocker=None)
    p["execution476StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    p["batch072NativePreparationCheckpoint"] = checkpoint
    p["execution476CoordinatorCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", p)
    save(LOG / "execution-476-checkpoint.json", checkpoint)
    (LOG / "issue-body.txt").write_text(
        f"Batch 072 native-preparation checkpoint **476** saved locally at `{checkpoint['savedCommit']}` "
        "(normal signature G); no runtime publication.\n\n"
        "Exact full signed `92f3c2ef` Git archive (version `900e3a2130afc56b`, 1,084 kanji / "
        "5,042 words / 104 N1 cards) preserves all 8,344 runtime hashes and original publishing budgets. "
        "Both cases and the exact archive are verified inside the serially compiled APK; temporary Android "
        "source/assets removed and dedicated worktree clean. No HOST heap init or guest/app heap/guard change. "
        "Teaching/manifest unchanged; validator passes.\n\n"
        f"{record['selectorAudit']['completeArticleSelectors']} static unique article selectors prepare complete "
        "充/充てる projections, all three reading labels/explanations and the exact reused 拡充 component "
        "paragraph; two mapped reciprocal pairs/four directed transitions and System Back. Both Full/Lite retain "
        "ジュウ and あ.てる/み.たす; quiz selects ジュウ/あ.てる only, with both-kind completion, persisted grades "
        "and no みたす question/log assertions. Six-stroke touch trace/recall and all actual authored Han including "
        "isolated 亠/儿/厶 across four production families are prepared, not executed. Native/visual readability, "
        "fallback-face identity and phone acceptance are not claimed. Fresh475 Android3+1 and original reports "
        "hash-reverified without redundant HOST Gradle/reviews.\n\n"
        "Next: fresh device/5580/5581 ownership check, owned read-only API35 helper, both terminal native case "
        "statuses 0/no skips and actual PNG inspection; then original Claude/GPT serial dependent visual "
        "confirmation. Current-main validation/signing/owner fast-forward/CI/immutable public ZIP gates remain. "
        "**98/1,228 additions published; 1,130 remain; 99 published necessary supports are not N1 vocabulary.** "
        "Compatible Android `f9b59a2`+ required; physical-phone/general-release/whole-set acceptance outstanding. "
        "Checkpoint status `continue`; batch073 not started.",
        encoding="utf-8")
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))
else:
    raise ValueError(mode)
