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
LOG = CONTROL / "logs" / "b3d5c3f1-09e3-4e38-8c71-a8957ba293dc"
HEAD = "f6ff96a109f3e7b6a67f41e6b9ee214962c9a39f"
REVIEWED = "1dc352148065c47d6d3a33206c62f3b877e678f6"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-071-native"
SOURCES = ROOT / "docs" / "n1-sources"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-070-native" / "N1Batch070NativeTest.kt"
FIXTURE = FOLDER / "N1Batch071NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-071-f6ff96a1-envelope.zip"
APK = CONTROL / "artifacts" / "n1-batch-071-native-test.apk"
NEXT = (
    "SAME071: execute compiled control\\artifacts\\n1-batch-071-native-test.apk "
    "N1Batch071GlyphTest and N1Batch071ArticleTest using exact signed f6ff96a1 full Git envelope. "
    "Read docs\\n1-sources\\execution-468.json and batch-071-native-preparation.json. "
    "Fresh adb/device and5580/5581 local/remote connection/PID ownership immediately before "
    "read-only N3_Acceptance_20261029 emulator-5580 launch with established API35 flags "
    "-port5580 -read-only -no-snapshot -no-window -no-audio -gpu host -feature -Vulkan "
    "-memory2048 -cores2. Record helper parent/QEMU identities; stop only owned helper. "
    "Batch040 routing override not inherited. No HOST heap init/native guest or app heap/guard changes. "
    "Require ContentSync ONCE:1083kanji5041words103N1/version05002d6e68a4eb89/problems0/epoch1; "
    "Full+Lite fullイン andじょう/まこと.に/ゆるす; sole curatedイン/normalizedいん, explicit empty quizKunyomi. "
    "Terminal status0 for BOTH cases, no skips and actual PNG inspection; actual25Han including "
    "isolated儿/厶 and口/土 plus公/先 and允可 across four production families, two complete article projections, "
    "all four reading labels/explanations, one mapped reciprocal pair/two directions, System Back/"
    "offline/N1selection/meaning/soleOn/persistedGood/noKunLog/Done1correct/"
    "fourreference-stroke touch/ungradedtrace/recallmiss/persistedDrawAgain. "
    "Static selectors/raster hashes are not readability, fallback-face or phone evidence. "
    "Reference trace is not human handwriting/MLKit. Fresh467Android3+1 inherited; "
    "no redundant HOST Gradle absent new concern. After native pass original "
    "Claude43cc8b39-2d2e-4d29-a274-d582d2ac4e02 and GPT08e79180-ae38-4be2-bc8c-cd2f83041ab0 "
    "SERIAL dependent visual confirmations using supported read-only tools and bounded packets. "
    "Then current-main nonrewriting integration/all validation/normal signing/owner fastforward/"
    "greenCI/every immutable public ZIP runtime hash/original budgets/ownerissue60 receipt "
    "before publication or072. No second runner/supervisor edits/permission bypass/signing workaround. "
    "Published97/1228,remaining1131;071 local is not delivered. Compatible Androidf9b59a2+ required; "
    "physical-phone/general-release/whole-set acceptance outstanding."
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
    assert p["checkpoint"] == 467 and p["status"] == "continue" and p["batch"] == "071"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    unchanged()
    request = (LOG / "request.txt").read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["checkpoint"] == 467
    save(LOG / "execution-468-before-progress.json", p)
    p["execution468StartingState"] = {
        "execution": 468, "batch": "071", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME071 exact full signed Git archive native fixture preparation/compilation and normally signed local evidence checkpoint only; no native/reviewer/publication/072/second runner.",
        "authorization": {
            "requestSha256": sha(LOG / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete approved issue and complete final467 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial console root-key output hit cp1252 after successful parse; repeated bounded UTF8 inspection, no state changed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
        "androidHead": git("rev-parse", "HEAD", cwd=ANDROID),
    }
    p["stage"] = "batch-071-native-preparation-in-progress"
    save(CONTROL / "progress.json", p)
    print("Starting native-preparation scope persisted; complete live history retained.")
elif mode in ("prepare", "prepare-refresh"):
    assert git("rev-parse", "HEAD") == HEAD
    expected_status = "" if mode == "prepare" else "?? docs/n1-reviews/batch-071-native/"
    assert git("status", "--porcelain") == expected_status
    unchanged()
    assert not APK.exists()
    if mode == "prepare":
        assert not FOLDER.exists() and not ARCHIVE.exists()
    else:
        initial = load(CONTROL / "batch-071-native-fixture-verification.json")
        assert sha(FIXTURE) == initial["fixtureSha256"] and sha(ARCHIVE) == initial["archiveSha256"]
        assert not (LOG / "native-compile.txt").exists()
        shutil.copyfile(FIXTURE, LOG / "precompile-original-N1Batch071NativeTest.kt")
        save(LOG / "precompile-original-preparation.json", initial)
    manifest = load(ROOT / "manifest.json")
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
        "words": sum(n.startswith("words/") for n in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (ROOT / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1083, "words": 5041, "n1": 103}
    assert manifest["contentVersion"] == "05002d6e68a4eb89"
    helper = ROOT / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    functions = ast.Module(body=[n for n in parsed.body if isinstance(n, ast.FunctionDef)
                                and n.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(functions, str(helper), "exec"), namespace)
    names = ["kanji/允.md", "words/允可.md"]
    documents = {n: namespace["blocks"](ROOT / n) for n in names}
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def display(document, slug):
        projected = documents[document]
        line(f"await({quote(projected[0][1])})")
        table_cell = 0
        for index, (kind, value) in enumerate(projected[1:], 1):
            if kind == "heading":
                line(f"section({quote(value)})")
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
        raw = next(part.removeprefix("- ") for part in raw_parts
                   if f"[{label}](" in part)
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        assert (ROOT / document).parent.joinpath(link[1]).resolve() == (ROOT / destination).resolve()
        text = namespace["plain"](" ".join(raw.splitlines()))
        marker = "N1_LINK_TARGET_468"
        marked = raw[:link.start()] + marker + raw[link.end():]
        offset = namespace["plain"](" ".join(marked.splitlines())).index(marker)
        assert text[offset:].startswith(label)
        line(f"section({quote(section_name)})")
        line(f"inline(await(articleBullet({quote(text)})), {quote(label)}, {offset})")
        offsets.append({"document": document, "destination": destination, "label": label,
                        "renderedText": text, "offset": offset})

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("允")')
    line('click("permit; sincerity")')
    display("kanji/允.md", "kanji")
    follow("kanji/允.md", "允可", "words/允可.md", "Common words")
    display("words/允可.md", "word")
    follow("words/允可.md", "允", "kanji/允.md", "How the kanji combine")
    line('await("Article contents")')
    line('section("Readings")')
    line('show(readingExample("允可 いんか — permission; assent"), "word-new-kanji-backlink")')
    for item, section_name, step in (
        (offsets[1], "How the kanji combine", "system-back-word-kanji"),
        (offsets[0], "Common words", "system-back-kanji-word"),
    ):
        line("back()")
        line(f"await(articleBullet({quote(item['renderedText'])})).assertIsDisplayed()")
        line(f"section({quote(section_name)})")
        line(f"capture({quote(step)})")
    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("070", "071"),
        ("recompenseLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
         "permissionLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineRecompenseThreeReciprocalPairsBothReadingsDrawingAndSystemBack",
         "fullSingleImportOfflinePermissionReciprocalPairOnOnlyDrawingAndSystemBack"),
        ("fce81d63caba02c311d9d87ba955002ec79fc4c9", HEAD), ("fce81d63", HEAD[:8]),
        ("a9867cc4b455639a", manifest["contentVersion"]),
        ("1082", "1083"), ("5040", "5041"), ("102, n1.size", "103, n1.size"),
        ("N1 · 102 cards", "N1 · 103 cards"),
        ("recompense; make amends", "permit; sincerity"),
        ("recompense", "permission"), ("償", "允"),
        ("ショウ", "イン"), ("しょう", "いん"),
        ("17, strokes.length()", "4, strokes.length()"), ("17 strokes drawn", "4 strokes drawn"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    actual_han = load(SOURCES / "batch-071-draft-audit.json")["actualAuthoredHanFonts"]["characters"]
    assert len(actual_han) == 25
    glyphs = list(dict.fromkeys(list("允元兄去公先許儿厶口土可") + actual_han))
    words = ["允可"]
    text = re.sub(r'val text = "[^"]+"', "val text = " + quote(" ".join(glyphs + words)), text, count=1)
    text = re.sub(r'Text\("Batch 071:[^"]+"\)',
                  'Text("Batch 071: permission / look-alikes / isolated radicals")', text)
    text = re.sub(r'Text\("Inspect [^\n]+fontSize = 18.sp\)',
                  'Text("Inspect 允/元/兄/去 and standalone 儿/厶. Compare 公/先, 口/土 and the whole word 允可. Fallback families may coincide.", fontSize = 18.sp)', text)
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
                  "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)', 'for (word in listOf("允可"))', text, count=1)
    text = text.replace("assertEquals(100, rows.length())", f"assertEquals({4 * (len(glyphs) + 1)}, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 88).put("wholeWordRasterProbes", 12)',
                        f'.put("individualGlyphProbes", {4 * len(glyphs)}).put("wholeWordRasterProbes", 4)')
    text = re.sub(r'\.put\("limits", "Native single-character[^"]+"\)',
                  '.put("limits", "Native Paint probes for all authored Han plus 公/先 including actual isolated 儿/厶 and 口/土; four whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")', text)
    for owner in ("permission", "card"):
        text = text.replace(f'listOf("つぐな.う"), {owner}.kunyomi.splitSep()',
                            f'listOf("じょう", "まこと.に", "ゆるす"), {owner}.kunyomi.splitSep()')
        text = text.replace(f'listOf("つぐな.う"), {owner}.quizKunyomi?.splitSep()',
                            f'emptyList<String>(), {owner}.quizKunyomi?.splitSep()')
    text = text.replace('listOf("つぐなう"), permission.toReadingCard().quizKeys(ReadingKind.Kun)',
                        'emptyList<String>(), permission.toReadingCard().quizKeys(ReadingKind.Kun)')
    text = text.replace('((kind == ReadingKind.On && key == "いん") || (kind == ReadingKind.Kun && key == "つぐなう"))',
                        '(kind == ReadingKind.On && key == "いん")')
    text = text.replace('repeat(2) {', 'repeat(1) {')
    text = text.replace('val key = if (question.question.kind == ReadingKind.On) "いん" else "つぐなう"',
                        'assertEquals(ReadingKind.On, question.question.kind)\n                val key = "いん"')
    text = text.replace('assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)',
                        '''assertEquals(setOf(ReadingKind.On), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "允" && it.mode == ReadingKind.Kun.mode.name }
            })
            capture("curated-on-only-done")''')
    text = text.replace("both curated on/kun keys due", "sole curated on key due; explicit no-kun with full source kun retained")
    text = text.replace('"bothCuratedKindsAndPersistedGrades"', '"soleCuratedOnPersistedGoodNoKunAndDone"')
    text = text.replace('.put("transport", "Exact full git envelope', '''.put("liteQuizOnyomi", JSONArray(requireNotNull(permission.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(permission.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope''')
    text = text.replace('val strokes = JSONObject(requireNotNull(card.strokesJson))', '''evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson))''')
    start = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
    text = text[:start] + "\n".join(lines) + "\n" + text[end:]
    for selector in selectors:
        assert quote(selector["target"]) in text, selector
    for link in offsets:
        assert quote(link["renderedText"]) in text, link
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("070", "償", "つぐな", "ショウ", "bothCurated", "permission; make amends", "17 strokes"):
        assert stale not in text, stale
    assert 'listOf("じょう", "まこと.に", "ゆるす"), permission.kunyomi.splitSep()' in text
    assert 'listOf("じょう", "まこと.に", "ゆるす"), card.kunyomi.splitSep()' in text
    assert len(offsets) == 2 and {(v["document"], v["destination"]) for v in offsets} == {
        ("kanji/允.md", "words/允可.md"), ("words/允可.md", "kanji/允.md")}
    if not ARCHIVE.exists():
        subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-071/",
                        f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.namelist()
        prefix = "n1-batch-071/"
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
    assert verified == 8341
    FOLDER.mkdir(exist_ok=mode == "prepare-refresh")
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-070.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(PRIOR.relative_to(ROOT)), tofile=str(FIXTURE.relative_to(ROOT)), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 468, "batch": "071", "status": "prepared-not-executed",
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
        "articleFiles": [{"path": n, "sha256": sha(ROOT / n), "projectedTextBlocks": len(b)} for n, b in documents.items()],
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 2, "mappedReciprocalPairs": 1, "mappedDirectedTransitions": 2,
        "plannedNativePaintProbes": 4 * len(glyphs), "plannedWholeWordRasterProbes": 4,
        "plannedGlyphs": glyphs, "plannedWholeWords": words,
        "fullReadings": {"on": ["イン"], "kun": ["じょう", "まこと.に", "ゆるす"]},
        "curatedReadings": {"on": ["イン"], "kun": []},
        "normalizedQuizKeys": {"on": ["いん"], "kun": []},
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "preCompilationCorrection": "First static preparation safety check caught two stale 償 disclosure mentions before any output. Subsequent complete fixture inspection caught inherited global kana substitution touching source-derived 承認しょうにん selector. Original uncompiled fixture/record preserved in execution468 log; insert generated source projections AFTER harness substitutions and assert every source-derived selector and linked paragraph remains exact. No teaching change, build/native failure or acceptance inferred.",
        "limits": "Static preparation/compilation only; not native, font/visual, phone or publication acceptance. Complete prose and all four reading label/example selectors; repeated table type labels not separately asserted. Full Git archive through ContentSync ONCE, unchanged guest/app heap/guards. Raster hashes do not identify fallback face or readability. Reference tracing is not human handwriting/MLKit. No teaching edits.",
        "nextAction": NEXT,
    }
    save(CONTROL / "batch-071-native-fixture-verification.json", record)
    print(json.dumps({k: record[k] for k in (
        "status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes",
        "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print("Unique article selectors:", len(selectors), "; directed links:", len(offsets))
elif mode == "archive":
    unchanged()
    preparation = load(CONTROL / "batch-071-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    raw_log = LOG / "native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (LOG / "native-compile-exit.txt").read_text().strip() == "0" and "BUILD SUCCESSFUL" in compile_text
    with zipfile.ZipFile(APK) as z:
        assert hashlib.sha256(z.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [z.read(n) for n in z.namelist() if re.fullmatch(r"classes\d*\.dex", n)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch071{kind}Test;".encode() in b for b in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch070{kind}Test;".encode() not in b for b in dex)
        for method in ("permissionLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies",
                       "fullSingleImportOfflinePermissionReciprocalPairOnOnlyDrawingAndSystemBack"):
            assert any(method.encode() in b for b in dex)
    (FOLDER / "compile.txt").write_text("\n".join(l.rstrip() for l in compile_text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-468.py")
    shutil.copyfile(CONTROL / "run-468-native-compile.ps1", receipts / "run-468-native-compile.ps1")
    save(SOURCES / "batch-071-native-preparation.json", preparation)
    inherited = load(SOURCES / "execution-467.json")
    for item in inherited["tests"]:
        assert sha(ROOT / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-071-reconciliation.json")
    reports = {}
    for key, process in reconciliation["processes"].items():
        path = ROOT / "docs" / "n1-reviews" / process["report"]
        assert sha(path) == process["reportSha256"]
        reports[key] = {"report": process["report"], "sha256": sha(path)}
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 05002d6e68a4eb89")):
        source = LOG / f"{name}.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = FOLDER / f"{name}.txt"
        target.write_text("\n".join(l.rstrip() for l in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(ROOT)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 468, "batch": "071", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(CONTROL / "progress.json")["execution468StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-071-native-preparation.json",
        "preparationSha256": sha(SOURCES / "batch-071-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "exitCode": 0, "status": "compiled-not-executed",
            "result": re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0),
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "log": str((FOLDER / "compile.txt").relative_to(ROOT)), "logSha256": sha(FOLDER / "compile.txt"),
            "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "apk": str(APK), "apkSha256": sha(APK), "apkBytes": APK.stat().st_size,
            "packagedExactFullArchiveVerified": True, "bothClassesAndMethodsVerified": True,
            "old070DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "completeArticleSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 2, "readingLabelsAndExplanations": 4,
            "mappedReciprocalPairs": 1, "mappedDirectedTransitions": 2,
        },
        "accepted467AndroidRetainedWithoutRerun": True, "inheritedArchivedXmlHashesReverified": True,
        "originalReportsUnchanged": reports, "runtimeEditsMade": False, "nativeExecuted": False,
        "nativeAcceptance": False, "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 97, "remainingAdditions": 1131,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    record["artifacts"] = [
        {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)}
        for p in sorted(FOLDER.rglob("*")) + [SOURCES / "batch-071-native-preparation.json"] if p.is_file()
    ]
    save(SOURCES / "execution-468.json", record)
    print("Exact packaged archive, both cases, inherited Android and reports verified.")
elif mode == "checkpoint":
    unchanged()
    record = load(SOURCES / "execution-468.json")
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    p = load(CONTROL / "progress.json")
    before = load(LOG / "execution-468-before-progress.json")
    assert all(p[k] == v for k, v in before.items() if k != "stage")
    assert set(p) == set(before) | {"execution468StartingState"}
    checkpoint = {
        "execution": 468, "checkpoint": 468, "batch": "071", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-468.json",
        "recordSha256": sha(SOURCES / "execution-468.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=468, status="continue", stage="batch-071-native-compiled-pending-execution",
             nextAction=NEXT, blocker=None)
    p["execution468StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    p["batch071NativePreparationCheckpoint"] = checkpoint
    p["execution468CoordinatorCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", p)
    save(LOG / "execution-468-checkpoint.json", checkpoint)
    (LOG / "issue-body.txt").write_text(
        f"Batch 071 native-preparation checkpoint **468** saved locally at `{checkpoint['savedCommit']}` "
        "(normal signature G); no runtime publication.\n\n"
        "The exact full signed `f6ff96a1` Git archive (version `05002d6e68a4eb89`, 1,083 kanji / "
        "5,041 words / 103 N1 cards) preserves all 8,341 runtime hashes and original publishing budgets. "
        "Both cases and the exact archive are verified inside the serially compiled APK; temporary Android "
        "source/assets removed and dedicated worktree clean. No HOST-only heap init or guest/app heap/guard "
        "change. Teaching/manifest unchanged; validator passes.\n\n"
        f"{record['selectorAudit']['completeArticleSelectors']} static unique article selectors prepare two "
        "complete projections (允 and 允可), all four reading labels/explanations and the mapped reciprocal "
        "pair/both directions. Full source イン and じょう/まこと.に/ゆるす remain in both Full/Lite, "
        "with sole curated イン/いん and explicit empty quizKunyomi; completion/no-kun-log assertions, "
        f"four-stroke trace/recall, {load(SOURCES / 'batch-071-native-preparation.json')['plannedNativePaintProbes']} glyph "
        "and four word raster probes are prepared, including isolated 儿/厶 fallback and all actual authored Han. "
        "These are **not executed**; native/visual readability, fallback-face identity and phone acceptance "
        "are not claimed. Fresh467 Android3+1 and original reports are hash-reverified without redundant "
        "HOST runs. Historical evidence preserved.\n\n"
        "**Next:** separate native execution with fresh device/port/PID ownership, original-session serial "
        "visual confirmations, then combined-main/signing/CI/exact immutable public-ZIP gates before "
        "publication or072. Published coverage remains **97/1,228 additions; 1,131 remain**. Compatible "
        "Android `f9b59a2+` required; physical-phone/general-release and whole-set acceptance outstanding.\n",
        encoding="utf-8")
    print("Signed local checkpoint468 saved with complete live history.")
else:
    raise ValueError(mode)
