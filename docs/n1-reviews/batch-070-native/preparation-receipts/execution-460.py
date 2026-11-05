import ast
import difflib
import gzip
import hashlib
import json
import posixpath
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
LOG = CONTROL / "logs" / "196f22b0-1fe9-4e6c-97d5-a6260db22ec1"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-070-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "fce81d63caba02c311d9d87ba955002ec79fc4c9"
REVIEWED = "174ee1d82ddf8bd67dd72c14b411adf3d82e4aef"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-069-native" / "N1Batch069NativeRetry1Test.kt"
FIXTURE = FOLDER / "N1Batch070NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-070-fce81d63-envelope.zip"
APK = CONTROL / "artifacts" / "n1-batch-070-native-test.apk"
GLYPHS = list("償賞儀僧億人亻補衣衤礻甫捕手扌初複保証埋損害")
WORDS = ["償う", "補償", "補う"]
NEXT = (
    "SAME070: execute compiled control\\artifacts\\n1-batch-070-native-test.apk "
    "N1Batch070GlyphTest and N1Batch070ArticleTest with exact signed fce81d63 full Git envelope. "
    "Read docs\\n1-sources\\execution-460.json and batch-070-native-preparation.json. "
    "Fresh adb/device and5580/5581 local/remote connection/PID ownership immediately before "
    "read-only N3_Acceptance_20261029 emulator-5580 launch with established API35 flags "
    "-port5580 -read-only -no-snapshot -no-window -no-audio -gpu host -feature -Vulkan "
    "-memory2048 -cores2. Record helper parent/QEMU identities; stop only owned helper. "
    "Batch040 routing override not inherited. No HOST heap init/native guest or app heap/guard changes. "
    "Require ContentSync ONCE:1082kanji5040words102N1/versiona9867cc4b455639a/problems0/epoch1; "
    "Full+Lite full/curatedショウ,つぐな.う; normalizedしょう,つぐなう. Terminal status0 for BOTH cases, "
    "no skips and actual PNG inspection; 償/賞/儀/僧/億/人/standalone亻/補/衣/衤/礻/甫/捕/手/扌/初/複/"
    "保/証/埋/損/害 plus 償う/補償/補う across four production families, five complete article "
    "projections, three mapped reciprocal pairs/six directions plus 補/補う reciprocal and "
    "changed補う-to補償 comparison, System Back/offline/N1selection/meaning/bothCuratedKinds/"
    "persistedgrades/17reference-stroke touch/ungradedtrace/recallmiss/persistedDrawAgain. "
    "Static selectors/raster hashes are not readability, fallback-face or phone evidence. "
    "Full reused補/補う projections are rendering scope, not fresh linguistic review of unchanged prose. "
    "Reference trace is not human handwriting/MLKit. Fresh459Android3+1 inherited; no redundant HOST "
    "Gradle absent new concern. After native pass original Claude5ace375a-4747-4cb8-be76-486c1a778e45 "
    "and GPT5424a79d-80be-4124-ba8b-fb09e2be95c2 SERIAL dependent visual confirmations using actual "
    "supported CLI/read-only tools and bounded packets. Then current-main nonrewriting integration/"
    "all validation/normal signing/owner fastforward/greenCI/exactimmutablepublicZIP hashes+budgets/"
    "ownerissue60 receipt before publication or071. No second runner/supervisor edits/permission bypass/"
    "signing workaround. Published96/1228,remaining1132;070 local is not delivered. Compatible "
    "Androidf9b59a2+ required; physical-phone/general-release/whole-set acceptance outstanding."
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
    assert p["checkpoint"] == 459 and p["status"] == "continue" and p["batch"] == "070"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    unchanged()
    request_path = LOG / "request.txt"
    request = request_path.read_text(encoding="utf-8-sig")
    json.loads(request.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    save(LOG / "execution-460-before-progress.json", p)
    p["execution460StartingState"] = {
        "execution": 460, "batch": "070", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME070 exact full archive native fixture preparation/compilation and normally signed local evidence checkpoint only; no native/reviewer/publication/071/second runner.",
        "authorization": {
            "requestSha256": sha(request_path), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, approved issue and complete final459 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed. First console inspection failed cp1252 after successful parse; repeated with UTF8, no state changed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
        "androidHead": git("rev-parse", "HEAD", cwd=ANDROID),
    }
    p["stage"] = "batch-070-native-preparation-in-progress"
    save(CONTROL / "progress.json", p)
    print("Starting scope persisted; complete historical progress retained.")
elif mode in ("prepare", "prepare-refresh"):
    assert git("rev-parse", "HEAD") == HEAD
    expected_status = "" if mode == "prepare" else "?? docs/n1-reviews/batch-070-native/"
    assert git("status", "--porcelain") == expected_status
    unchanged()
    assert not APK.exists()
    if mode == "prepare":
        assert not FOLDER.exists() and not ARCHIVE.exists()
    else:
        initial = load(CONTROL / "batch-070-native-fixture-verification.json")
        assert sha(FIXTURE) == initial["fixtureSha256"] and sha(ARCHIVE) == initial["archiveSha256"]
        assert not (LOG / "native-compile.txt").exists()
        shutil.copyfile(FIXTURE, LOG / "precompile-original-N1Batch070NativeTest.kt")
        save(LOG / "precompile-original-preparation.json", initial)
    manifest = load(ROOT / "manifest.json")
    assert manifest["contentVersion"] == "a9867cc4b455639a"
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
        "words": sum(n.startswith("words/") for n in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (ROOT / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1082, "words": 5040, "n1": 102}
    helper = ROOT / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    functions = ast.Module(body=[n for n in parsed.body if isinstance(n, ast.FunctionDef)
                                and n.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(functions, str(helper), "exec"), namespace)
    names = ["kanji/償.md", "words/償う.md", "words/補償.md", "kanji/補.md", "words/補う.md"]
    documents = {n: namespace["blocks"](ROOT / n) for n in names}
    lines, selectors, transitions, offsets = [], [], [], []

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
                if table_cell % 3 != 0 or value == "Typical words":
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
        links = re.findall(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", section_body)
        destinations = {posixpath.normpath(posixpath.join(posixpath.dirname(document), link))
                        for link in links if not link.startswith("https://")}
        assert destinations == {destination}, (document, label, destinations)
        matching, current = [], None
        pattern = r"(?<![\u3400-\u9fff])" + re.escape(label) + r"(?![\u3400-\u9fff])"
        for kind, value in documents[document]:
            if kind == "heading":
                current = value
            elif current == section_name and kind == "paragraph" and re.search(pattern, value):
                matching.append(value)
        assert len(matching) == 1, (document, label, matching)
        raw_parts = re.split(r"\n\s*\n|\n(?=- )", section_body.strip())
        raw = next(part.removeprefix("- ") for part in raw_parts
                   if namespace["plain"](" ".join(part.removeprefix("- ").splitlines())) == matching[0])
        link = re.search(r"\[" + re.escape(label) + r"\]\([^)]+\)", raw)
        marker = "N1_LINK_TARGET_460"
        marked = raw[:link.start()] + marker + raw[link.end():]
        offset = namespace["plain"](" ".join(marked.splitlines())).index(marker)
        assert matching[0][offset:].startswith(label)
        line(f"section({quote(section_name)})")
        line(f"inline(await(articleBullet({quote(matching[0])})), {quote(label)}, {offset})")
        transitions.append([document, destination])
        offsets.append({"document": document, "destination": destination, "label": label,
                        "renderedText": matching[0], "offset": offset})

    def back_to(document, section_name, step):
        restored = next(item["renderedText"] for item in reversed(offsets) if item["document"] == document)
        line("back()")
        line(f"await(articleBullet({quote(restored)})).assertIsDisplayed()")
        line(f"section({quote(section_name)})")
        line(f"capture({quote(step)})")

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("償")')
    line('click("recompense; make amends")')
    display("kanji/償.md", "kanji")
    follow("kanji/償.md", "償う", "words/償う.md", "Common words")
    display("words/償う.md", "word1")
    follow("words/償う.md", "償", "kanji/償.md", "How the kanji combine")
    line('await("Article contents")')
    line('section("Readings")')
    line('show(readingExample("償う つぐなう — make amends; compensate for loss"), "word1-new-kanji-backlink")')
    back_to("words/償う.md", "How the kanji combine", "system-back-word1-kanji")
    back_to("kanji/償.md", "Common words", "system-back-kanji-word1")
    follow("kanji/償.md", "補償", "words/補償.md", "Common words")
    display("words/補償.md", "word2")
    follow("words/補償.md", "償", "kanji/償.md", "How the kanji combine")
    line('await("Article contents")')
    line('section("Readings")')
    line('show(readingExample("補償 ほしょう — compensation for loss"), "word2-new-kanji-backlink")')
    back_to("words/補償.md", "How the kanji combine", "system-back-word2-kanji")
    follow("words/補償.md", "補", "kanji/補.md", "How the kanji combine")
    display("kanji/補.md", "component1")
    follow("kanji/補.md", "補償", "words/補償.md", "Common words")
    line('await("Article contents")')
    line('section("How the kanji combine")')
    line('capture("word2-legacy-backlink")')
    back_to("kanji/補.md", "Common words", "system-back-component1-word2")
    follow("kanji/補.md", "補う", "words/補う.md", "Common words")
    display("words/補う.md", "comparison")
    follow("words/補う.md", "補", "kanji/補.md", "How the kanji combine")
    line('await("Article contents")')
    line('section("Readings")')
    line('capture("comparison-component-backlink")')
    back_to("words/補う.md", "Distinctive meaning", "system-back-comparison-component")
    follow("words/補う.md", "補償", "words/補償.md", "Distinctive meaning")
    line('await("Article contents")')
    line('section("Distinctive meaning")')
    line('capture("comparison-compensation-target")')
    back_to("words/補う.md", "Distinctive meaning", "system-back-comparison-compensation")
    back_to("kanji/補.md", "Common words", "system-back-component1-comparison")
    back_to("words/補償.md", "How the kanji combine", "system-back-word2-component1")
    back_to("kanji/償.md", "Common words", "system-back-kanji-word2")
    assert len(transitions) == len({tuple(p) for p in transitions}) == 9
    expected_pairs = {
        ("kanji/償.md", "words/償う.md"), ("kanji/償.md", "words/補償.md"),
        ("kanji/補.md", "words/補償.md"),
    }
    for pair in expected_pairs:
        assert list(pair) in transitions and list(reversed(pair)) in transitions
    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("069", "070"), ("Retry1", ""),
        ("confucianLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
         "recompenseLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineConfucianTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
         "fullSingleImportOfflineRecompenseThreeReciprocalPairsBothReadingsDrawingAndSystemBack"),
        ("e245739783dbc2ebe33ee164b8cfa718d670551b", HEAD), ("e2457397", HEAD[:8]),
        ("83ed94552dd1a9ce", manifest["contentVersion"]),
        ("1081", "1082"), ("5038", "5040"),
        ("101, n1.size", "102, n1.size"), ("N1 · 101 cards", "N1 · 102 cards"),
        ("confucian", "recompense"), ("儒", "償"), ("ジュ", "ショウ"), ("じゅ", "しょう"),
        ("Confucian; Confucian scholar", "recompense; make amends"),
        ("16, strokes.length()", "17, strokes.length()"), ("16 strokes drawn", "17 strokes drawn"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    start = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
    text = text[:start] + "\n".join(lines) + "\n" + text[end:]
    text = re.sub(r'val text = "[^"]+"', "val text = " + quote(" ".join(GLYPHS + WORDS)), text, count=1)
    text = re.sub(r'Text\("Batch 070:[^"]+"\)', 'Text("Batch 070: recompense / look-alikes / radical variants")', text)
    text = re.sub(r'Text\("Inspect [^\n]+fontSize = 18.sp\)',
                  'Text("Inspect 償/賞 and 人/亻; 補 has 衣 as 衤, not 礻. Compare 捕/扌 and 初/複. Check all three words. Fallback families may coincide.", fontSize = 18.sp)', text)
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)', "for (char in listOf(" +
                  ", ".join(quote(c) for c in GLYPHS) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)', "for (word in listOf(" +
                  ", ".join(quote(w) for w in WORDS) + "))", text, count=1)
    text = text.replace("assertEquals(60, rows.length())", f"assertEquals({4 * (len(GLYPHS) + len(WORDS))}, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 56).put("wholeWordRasterProbes", 4)',
                        f'.put("individualGlyphProbes", {4 * len(GLYPHS)}).put("wholeWordRasterProbes", 12)')
    text = re.sub(r'\.put\("limits", "Fifty-six[^"]+"\)',
                  '.put("limits", "Native single-character Paint probes including 人/亻 and 衣/衤/礻 plus twelve whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")', text)
    for owner in ("recompense", "card"):
        text = text.replace(f"emptyList<String>(), {owner}.kunyomi.splitSep()", f'listOf("つぐな.う"), {owner}.kunyomi.splitSep()')
        text = text.replace(f"emptyList<String>(), {owner}.quizKunyomi?.splitSep()", f'listOf("つぐな.う"), {owner}.quizKunyomi?.splitSep()')
    text = text.replace('emptyList<String>(), recompense.toReadingCard().quizKeys(ReadingKind.Kun)',
                        'listOf("つぐなう"), recompense.toReadingCard().quizKeys(ReadingKind.Kun)')
    text = text.replace('(kind == ReadingKind.On && key == "しょう")',
                        '((kind == ReadingKind.On && key == "しょう") || (kind == ReadingKind.Kun && key == "つぐなう"))')
    text = text.replace('repeat(1) {', 'repeat(2) {')
    text = text.replace('                assertEquals(ReadingKind.On, question.question.kind)\n', '')
    text = text.replace('val key = "しょう"', 'val key = if (question.question.kind == ReadingKind.On) "しょう" else "つぐなう"')
    start = text.index('            assertEquals(setOf(ReadingKind.On), answeredKinds)')
    end = text.index('            back()', start)
    text = text[:start] + '            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)\n' + text[end:]
    text = text.replace("sole curated on key due; explicit no-kun", "both curated on/kun keys due")
    text = text.replace('"soleCuratedOnQuestionAndPersistedGradeNoKun"', '"bothCuratedKindsAndPersistedGrades"')
    assert "explicit no-kun" not in text and "emptyList<String>()" not in text
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text and "069" not in text and "儒" not in text
    if not ARCHIVE.exists():
        subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-070/",
                        f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.namelist()
        prefix = "n1-batch-070/"
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
                normalized = data if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(normalized).hexdigest() == expected, name
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in z.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    assert verified == 8338
    FOLDER.mkdir(exist_ok=mode == "prepare-refresh")
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-069-retry1.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 460, "batch": "070", "status": "prepared-not-executed",
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
        "staticMarkdownSelectors": selectors, "articleRouteTransitions": transitions, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 5, "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6,
        "extraDirectedTransitions": 3, "plannedNativePaintProbes": 4 * len(GLYPHS),
        "plannedWholeWordRasterProbes": 12, "plannedGlyphs": GLYPHS, "plannedWholeWords": WORDS,
        "fullReadings": {"on": ["ショウ"], "kun": ["つぐな.う"]},
        "curatedReadings": {"on": ["ショウ"], "kun": ["つぐな.う"]},
        "normalizedQuizKeys": {"on": ["しょう"], "kun": ["つぐなう"]},
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "preCompilationHarnessCorrection": "Coordinator static inspection replaced top-only Article contents waits after nested Back with exact source-derived restored paragraph visibility assertions. A lazy article can restore below its uncomposed top. Original uncompiled fixture/record preserved in execution460 log; no native failure/pass or production defect inferred.",
        "limits": "Static preparation/compilation only; not native, font/visual, phone or publication acceptance. Complete prose and table-example selectors; table labels not separately asserted. Full reused補/補う rendering does not freshly linguistically review unchanged prose. Full Git archive through ContentSync ONCE, unchanged guest/app heap/guards. Raster hashes do not identify fallback face or readability. Reference tracing is not human handwriting/MLKit.",
        "nextAction": NEXT,
    }
    save(CONTROL / "batch-070-native-fixture-verification.json", record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print("Unique article selectors:", len(selectors), "; directed links:", len(transitions))
elif mode == "archive":
    unchanged()
    preparation = load(CONTROL / "batch-070-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    raw_log = LOG / "native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (LOG / "native-compile-exit.txt").read_text().strip() == "0" and "BUILD SUCCESSFUL" in compile_text
    with zipfile.ZipFile(APK) as z:
        assert hashlib.sha256(z.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [z.read(n) for n in z.namelist() if re.fullmatch(r"classes\d*\.dex", n)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch070{kind}Test;".encode() in b for b in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch069Retry1{kind}Test;".encode() not in b for b in dex)
        for method in ("recompenseLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
                       "fullSingleImportOfflineRecompenseThreeReciprocalPairsBothReadingsDrawingAndSystemBack"):
            assert any(method.encode() in b for b in dex)
    (FOLDER / "compile.txt").write_text("\n".join(l.rstrip() for l in compile_text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-460.py")
    shutil.copyfile(CONTROL / "run-460-native-compile.ps1", receipts / "run-460-native-compile.ps1")
    save(SOURCES / "batch-070-native-preparation.json", preparation)
    inherited = load(SOURCES / "execution-459.json")
    for item in inherited["tests"]:
        assert sha(ROOT / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-070-reconciliation.json")
    reports = {}
    for key, process in reconciliation["processes"].items():
        path = ROOT / "docs" / "n1-reviews" / process["report"]
        assert sha(path) == process["reportSha256"]
        reports[key] = {"report": process["report"], "sha256": sha(path)}
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version a9867cc4b455639a")):
        source = LOG / f"{name}.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = FOLDER / f"{name}.txt"
        target.write_text("\n".join(l.rstrip() for l in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(ROOT)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 460, "batch": "070", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(CONTROL / "progress.json")["execution460StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-070-native-preparation.json",
        "preparationSha256": sha(SOURCES / "batch-070-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "exitCode": 0, "status": "compiled-not-executed",
            "result": re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0),
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "log": str((FOLDER / "compile.txt").relative_to(ROOT)), "logSha256": sha(FOLDER / "compile.txt"),
            "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "apk": str(APK), "apkSha256": sha(APK), "apkBytes": APK.stat().st_size,
            "packagedExactFullArchiveVerified": True, "bothClassesAndMethodsVerified": True,
            "old069Retry1DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "completeArticleSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 5, "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6,
            "extraDirectedTransitions": 3,
        },
        "accepted459AndroidRetainedWithoutRerun": True, "inheritedArchivedXmlHashesReverified": True,
        "originalReportsUnchanged": reports, "runtimeEditsMade": False, "nativeExecuted": False,
        "nativeAcceptance": False, "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 96, "remainingAdditions": 1132,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    record["artifacts"] = [
        {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)}
        for p in sorted(FOLDER.rglob("*")) + [SOURCES / "batch-070-native-preparation.json"] if p.is_file()
    ]
    save(SOURCES / "execution-460.json", record)
    print("Exact packaged full archive, both cases, inherited Android and reports verified.")
elif mode == "checkpoint":
    unchanged()
    record = load(SOURCES / "execution-460.json")
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    p = load(CONTROL / "progress.json")
    before = load(LOG / "execution-460-before-progress.json")
    assert all(p[k] == v for k, v in before.items() if k != "stage")
    assert set(p) == set(before) | {"execution460StartingState"}
    checkpoint = {
        "execution": 460, "checkpoint": 460, "batch": "070", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-460.json",
        "recordSha256": sha(SOURCES / "execution-460.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=460, status="continue", stage="batch-070-native-compiled-pending-execution",
             nextAction=NEXT, blocker=None)
    p["execution460StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    p["batch070NativePreparationCheckpoint"] = checkpoint
    p["execution460CoordinatorCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", p)
    save(LOG / "execution-460-checkpoint.json", checkpoint)
    (LOG / "issue-body.txt").write_text(
        f"Batch 070 native-preparation checkpoint **460** saved locally at `{checkpoint['savedCommit']}` "
        "(normal signature G); no runtime publication.\n\n"
        "The exact full signed `fce81d63` Git archive (version `a9867cc4b455639a`, 1,082 kanji / "
        "5,040 words / 102 N1 cards) preserves all 8,338 runtime hashes and original publishing budgets. "
        "Both cases and the exact archive are verified inside the serially compiled APK; temporary Android "
        "source/assets removed and dedicated worktree clean. No HOST-only heap init or guest/app heap/guard "
        "change. Teaching/manifest unchanged; validator passes.\n\n"
        f"{record['selectorAudit']['completeArticleSelectors']} static unique article selectors prepare five "
        "complete projections (償, 償う, 補償, 補, 補う; unchanged reused prose is rendering scope, not fresh "
        "linguistic review), three mapped reciprocal pairs/six directions plus the 補/補う reciprocal and "
        "changed補う-to補償 comparison. Both curated ショウ/つぐな.う keys, seventeen-stroke trace/recall, "
        "88 glyph and twelve word raster probes are prepared. These are **not executed**; native/visual "
        "readability, fallback-face identity and phone acceptance are not claimed. Fresh459 Android3+1 "
        "and original reports are hash-reverified without redundant HOST runs. Historical evidence preserved.\n\n"
        "**Next:** separate native execution with fresh device/port/PID ownership, original-session serial "
        "visual confirmations, then combined-main/signing/CI/exact immutable public-ZIP gates before "
        "publication or071. Published coverage remains **96/1,228 additions; 1,132 remain**. Compatible "
        "Android `f9b59a2+` required; physical-phone/general-release and whole-set acceptance outstanding.\n",
        encoding="utf-8")
    print("Signed local checkpoint460 saved with complete live history.")
else:
    raise ValueError(mode)
