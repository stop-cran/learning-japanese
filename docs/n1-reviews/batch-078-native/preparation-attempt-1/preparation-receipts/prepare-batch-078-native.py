import ast
import difflib
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from fontTools.ttLib import TTFont

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
HEAD = "7fb6c46374f2464648130f2473fabcb9137bb7d4"
REVIEWED = "02b9634acda285bd60d00884479dee2a29ccb6e2"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-078-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-077-native" / "N1Batch077NativeTest.kt"
FIXTURE = FOLDER / "N1Batch078NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-078-7fb6c463-envelope.zip"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def quote(text):
    return json.dumps(text, ensure_ascii=False).replace("$", "\\$")


assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
assert not FOLDER.exists() and not ARCHIVE.exists()
progress = load(CONTROL / "progress.json")
assert progress["checkpoint"] == 524 and progress["batch"] == "078"
assert progress["batch078TextualReview"]["textualReviewClosed"] == ["冗"]
manifest = load(ROOT / "manifest.json")
assert manifest["contentVersion"] == "8e06edf2b0857b26"
ledger = load(ROOT / "docs" / "n1-sources" / "batch-078-progress.json")
audit = load(ROOT / "docs" / "n1-sources" / "batch-078-draft-audit.json")
assert ledger["sourceReadingOrder"] == {"onyomi": ["ジョウ"], "kunyomi": []}
assert [(i["reading"], i["selected"]) for i in ledger["readingDispositions"]] == [("ジョウ", True)]
projection = ROOT / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
parsed = ast.parse(projection.read_text(encoding="utf-8"))
functions = ast.Module(body=[node for node in parsed.body if isinstance(node, ast.FunctionDef)
                            and node.name in ("plain", "blocks")], type_ignores=[])
namespace = {"re": re}
exec(compile(functions, str(projection), "exec"), namespace)
names = audit["actualAuthoredHanFonts"]["articles"]
documents = {name: namespace["blocks"](ROOT / name) for name in names}
lines, selectors, offsets = [], [], []


def line(value):
    lines.append("            " + value)


def show(document, index, kind, value, slug):
    qualifier = "readingExample" if kind == "table" else "articleBullet"
    assert sum(v == value for k, v in documents[document]
               if (k == "table") == (kind == "table") and k != "heading") == 1
    step = f"{slug}-{index:02}"
    line(f"show({qualifier}({quote(value)}), {quote(step)})")
    selectors.append({"document": document, "kind": kind, "target": value, "step": step})


def display(document, slug):
    line(f"await({quote(documents[document][0][1])})")
    table_cell = 0
    for index, (kind, value) in enumerate(documents[document][1:], 1):
        if kind == "heading":
            line(f"section({quote(value)})")
        elif kind == "table":
            table_cell += 1
            if table_cell > 3 and table_cell % 3 != 2:
                show(document, index, kind, value, slug)
        else:
            show(document, index, kind, value, slug)


def follow(document, label, destination, slug):
    body = (ROOT / document).read_text(encoding="utf-8")
    sections = re.split(r"^## (.+)\n", body.split("---", 2)[2], flags=re.M)
    candidates = []
    for i in range(1, len(sections), 2):
        for part in re.split(r"\n\s*\n|\n(?=- )", sections[i + 1].strip()):
            for link in re.finditer(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", part):
                if (ROOT / document).parent.joinpath(link[1]).resolve() == (ROOT / destination).resolve():
                    candidates.append((sections[i], part.removeprefix("- ")))
    preferred = "Common words" if document.startswith("kanji/") else "How the kanji combine"
    section_name, raw = next((v for v in candidates if v[0] == preferred), candidates[0])
    link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
    text = namespace["plain"](" ".join(raw.splitlines()))
    marked = raw[:link.start()] + "N1_LINK_TARGET_525" + raw[link.end():]
    offset = namespace["plain"](" ".join(marked.splitlines())).index("N1_LINK_TARGET_525")
    assert text[offset:].startswith(label)
    line(f"section({quote(section_name)})")
    show(document, len(selectors), "paragraph", text, slug)
    line(f"inline(await(articleBullet({quote(text)})), {quote(label)}, {offset})")
    line('await("Article contents")')
    item = {"document": document, "destination": destination, "label": label,
            "section": section_name, "renderedText": text, "offset": offset}
    offsets.append(item)
    return item


def back_to(item, step):
    line("back()")
    line(f"await(articleBullet({quote(item['renderedText'])})).assertIsDisplayed()")
    line(f"section({quote(item['section'])})")
    line(f"capture({quote(step)})")


line('click("Browse all kanji")')
line('rule.onNode(hasSetTextAction()).performTextReplacement("冗")')
line('click("superfluous; redundant")')
display("kanji/冗.md", "kanji")
forward = follow("kanji/冗.md", "冗談", "words/冗談.md", "冗談-forward")
display("words/冗談.md", "冗談")
reverse = follow("words/冗談.md", "冗", "kanji/冗.md", "冗談-reverse")
line('section("Readings")')
line('show(readingExample("ジョウ"), "冗談-kanji-backlink")')
back_to(reverse, "冗談-system-back-to-word")
component = follow("words/冗談.md", "談", "kanji/談.md", "冗談-談")
line(f"await({quote(documents['kanji/談.md'][0][1])})")
counterpart = follow("kanji/談.md", "冗談", "words/冗談.md", "談-counterpart")
line('section("How the kanji combine")')
line(f"show(articleBullet({quote(component['renderedText'])}), \"冗談-談-component-backlink\")")
back_to(counterpart, "冗談-談-system-back-to-component")
back_to(component, "冗談-談-system-back-from-component")
back_to(forward, "冗談-system-back-to-kanji")
assert len(offsets) == 4
assert {(i["document"], i["destination"]) for i in offsets} == {
    pair for char, word in ledger["allMappedReciprocalPairs"]
    for pair in ((f"kanji/{char}.md", word), (word, f"kanji/{char}.md"))}

text = PRIOR.read_text(encoding="utf-8")
replacements = [
    ("077", "078"),
    ("bravingRiskLookalikesAndRadicalFallbacksAcrossFourProductionFamilies",
     "redundancyLookalikesAndCoverTableFallbacksAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineBravingRiskThreeReciprocalPairsBothReadingsDrawingAndSystemBack",
     "fullSingleImportOfflineRedundancyTwoReciprocalPairsSoleOnReadingDrawingAndSystemBack"),
    ("46dff1466ac9f3cf64b54e197c05088414939896", HEAD), ("46dff146", HEAD[:8]),
    ("2944928c13e2165a", manifest["contentVersion"]),
    ("1089", "1090"), ("109, n1.size", "110, n1.size"), ("N1 · 109 cards", "N1 · 110 cards"),
    ("bravingRisk", "redundancy"), ('"冒"', '"冗"'),
    ("brave danger; venture", "superfluous; redundant"),
    ('listOf("ボウ")', 'listOf("ジョウ")'),
    ('listOf("おか.す")', 'emptyList<String>()'),
    ('listOf("ぼう")', 'listOf("じょう")'),
    ('listOf("おかす")', 'emptyList<String>()'),
    ('"ぼう"', '"じょう"'),
    ('"Other N1 meanings/readings postponed; 冒 meaning and both complete curated readings due. Two historical good 冒 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress."',
     '"Other N1 meanings/readings postponed; 冗 meaning and sole curated on key じょう due; full and curated kun lists explicitly empty. Two historical good 冗 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress."'),
    ("bothCuratedKindsPersistedGoodAndDone", "soleCuratedOnPersistedGoodAndDoneNoKun"),
    ("assertEquals(9, strokes.length())", "assertEquals(4, strokes.length())"),
    ('"9 strokes drawn"', '"4 strokes drawn"'),
    ('.put("mappedReciprocalPairs", 3).put("directedLinkTransitions", 6)',
     '.put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)'),
    ('if (card.kanji == "冗" && ((kind == ReadingKind.On && key == "じょう") || (kind == ReadingKind.Kun && key == "おかす")))',
     'if (card.kanji == "冗" && kind == ReadingKind.On && key == "じょう")'),
    ("repeat(2) {", "repeat(1) {"),
    ('val key = if (question.question.kind == ReadingKind.On) "じょう" else "おかす"',
     'assertEquals(ReadingKind.On, question.question.kind)\n                val key = "じょう"'),
    ("assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)",
     "assertEquals(setOf(ReadingKind.On), answeredKinds)"),
    ("assertEquals(2, done.answered)", "assertEquals(1, done.answered)"),
    ("assertEquals(2, done.correct)", "assertEquals(1, done.correct)"),
    ("assertEquals(2, readingLogs.size)", "assertEquals(1, readingLogs.size)"),
    ('assertEquals(setOf("じょう", "おかす"), readingLogs.map { it.reading }.toSet())',
     'assertEquals(setOf("じょう"), readingLogs.map { it.reading }.toSet())\n'
     '            assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })'),
    ('capture("curated-both-done")', 'capture("curated-sole-on-done")'),
]
for old, new in replacements:
    assert old in text, old
    text = text.replace(old, new)
begin = text.index('            click("Browse all kanji")')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                              "".join((ROOT / n).read_text(encoding="utf-8") for n in names))))
assert glyphs == audit["actualAuthoredHanFonts"]["characters"] and len(glyphs) == 27
fonts = []
for prior_font in audit["actualAuthoredHanFonts"]["fonts"]:
    font_path = Path(prior_font["path"])
    assert sha(font_path) == prior_font["sha256"]
    with TTFont(font_path) as font:
        missing = [char for char in glyphs if ord(char) not in font.getBestCmap()]
    assert missing == ["冖", "几"]
    fonts.append({"path": str(font_path), "sha256": sha(font_path), "missingCurrentScopedHan": missing})
words = ["冗談"]
pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
pages.append("冗 冖 几 元 兄 見 口 目 冗談 冗長 冗長性 談")
text = re.sub(r'val pages = listOf\([^\n]+\)', "val pages = listOf(" + ", ".join(quote(p) for p in pages) + ")", text, count=1)
text = text.replace("Batch 078: braving risk / look-alikes / radical fallback",
                    "Batch 078: redundancy / look-alikes / cover and table fallback")
text = text.replace("Inspect all 39 scoped Han; focused 冒/日/目/官, 冂 and 阜/阝. Fallback families may coincide.",
                    "Inspect all 27 scoped Han; focused 冗/元/兄/見, 冖 and 几. Fallback families may coincide.")
text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
              "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
text = re.sub(r'for \(word in listOf\([^\n]+\)\)',
              "for (word in listOf(" + ", ".join(quote(w) for w in words) + "))", text, count=1)
text = text.replace("assertEquals(164, rows.length())", "assertEquals(112, rows.length())")
text = text.replace('.put("individualGlyphProbes", 156).put("wholeWordRasterProbes", 8)',
                    '.put("individualGlyphProbes", 108).put("wholeWordRasterProbes", 4)')
text = text.replace("39 scoped Han including metadata-only 攻 and pending 冂/阝 fallback inspection,",
                    "27 actual scoped Han including exact 冖/几 fallback inspection,")
text = text.replace("three bounded Compose panels and eight whole-word rasters.",
                    "three bounded Compose panels and four whole-word rasters.")
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for stale in ("077", "冒", "険", "ボウ", "ぼう", "おかす", "おか.す", "bravingRisk", "39 scoped", "9 strokes", "bothCurated"):
    assert stale not in text, stale
counts = {
    "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
    "words": sum(n.startswith("words/") for n in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1090, "words": 5046, "n1": 110}
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-078/",
                f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(ARCHIVE) as archive:
    entries = archive.namelist()
    prefix = "n1-batch-078/"
    assert len(entries) == len(set(entries)) <= 18000
    assert all(n.startswith(prefix) and "\\" not in n and ".." not in n.split("/") for n in entries)
    raw = archive.read(prefix + "manifest.json")
    assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=ROOT)
    assert json.loads(raw) == manifest
    retained, verified = len(raw), 0
    for section, mapping in manifest.items():
        if not isinstance(mapping, dict):
            continue
        for name, expected in mapping.items():
            data = archive.read(prefix + name)
            limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                     512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
            assert len(data) <= limit
            binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
            assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected, name
            retained += len(data)
            verified += 1
    inflated = sum(i.file_size for i in archive.infolist())
    assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
    assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
    assert not any("/docs/" in n or "/tools/" in n for n in entries)
assert verified == 8360
FOLDER.mkdir()
FIXTURE.write_text(text, encoding="utf-8")
diff = FOLDER / "fixture-from-077.diff"
diff.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=str(PRIOR.relative_to(ROOT)), tofile=str(FIXTURE.relative_to(ROOT)), n=0)), encoding="utf-8")
record = {
    "schemaVersion": 1, "execution": 525, "batch": "078", "status": "prepared-not-executed",
    "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED,
    "androidSnapshot": git("rev-parse", "HEAD", cwd=ANDROID),
    "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
    "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
    "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
    "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
    "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
    "priorHarness": str(PRIOR.relative_to(ROOT)), "priorHarnessSha256": sha(PRIOR),
    "staticProjectionHelper": str(projection.relative_to(ROOT)), "staticProjectionHelperSha256": sha(projection),
    "fixtureDiff": str(diff.relative_to(ROOT)), "fixtureDiffSha256": sha(diff),
    "articleFiles": [{"path": n, "sha256": sha(ROOT / n), "projectedTextBlocks": len(b)}
                     for n, b in documents.items()],
    "sourceReadingLedger": "docs/n1-sources/batch-078-progress.json",
    "sourceReadingLedgerSha256": sha(ROOT / "docs" / "n1-sources" / "batch-078-progress.json"),
    "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
    "completeArticleProjections": 2, "changedReusedPassages": 1,
    "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
    "plannedNativePaintProbes": 108, "plannedWholeWordRasterProbes": 4,
    "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
    "currentFontAudit": fonts,
    "fullReadings": {"on": ["ジョウ"], "kun": []},
    "curatedReadings": {"on": ["ジョウ"], "kun": []},
    "normalizedQuizKeys": {"on": ["じょう"], "kun": []},
    "pendingCmapAbsences": ["冖", "几"],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
    "limits": "Preparation only until compilation is verified; not native rendering, PNG/visual, handwriting, phone or publication acceptance. No duplicate parser preflight; production ContentSync once. Static offsets/hashes are not visibility, readability or fallback-face proof. HOST-only2GiBinit NEVER enters native builds; no app/guest heap/archiveguard changes. Fresh port/device/PID ownership inspection required before later launch. Historical limitations retained.",
}
(CONTROL / "batch-078-native-fixture-verification.json").write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: record[key] for key in ("status", "expectedCounts", "zipEntries",
                 "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
print("Static selectors:", len(selectors), "; directed links:", len(offsets))
