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
HEAD = "46dff1466ac9f3cf64b54e197c05088414939896"
REVIEWED = "02877a257d6b265625e637e6a304fc8440ddd337"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-077-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-076-native" / "N1Batch076NativeTest.kt"
FIXTURE = FOLDER / "N1Batch077NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-077-46dff146-envelope.zip"


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
assert progress["checkpoint"] == 516 and progress["batch"] == "077"
manifest = load(ROOT / "manifest.json")
assert manifest["contentVersion"] == "2944928c13e2165a"
ledger = load(ROOT / "docs" / "n1-sources" / "batch-077-progress.json")
audit = load(ROOT / "docs" / "n1-sources" / "batch-077-draft-audit.json")
assert ledger["sourceReadingOrder"] == {"onyomi": ["ボウ"], "kunyomi": ["おか.す"]}
assert [(i["reading"], i["selected"]) for i in ledger["readingDispositions"]] == [
    ("ボウ", True), ("おか.す", True)]
assert progress["batch077TextualReviewCheckpoint"]["textualReviewClosed"]
helper = ROOT / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
parsed = ast.parse(helper.read_text(encoding="utf-8"))
functions = ast.Module(body=[node for node in parsed.body if isinstance(node, ast.FunctionDef)
                            and node.name in ("plain", "blocks")], type_ignores=[])
namespace = {"re": re}
exec(compile(functions, str(helper), "exec"), namespace)
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
    marked = raw[:link.start()] + "N1_LINK_TARGET_517" + raw[link.end():]
    offset = namespace["plain"](" ".join(marked.splitlines())).index("N1_LINK_TARGET_517")
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
line('rule.onNode(hasSetTextAction()).performTextReplacement("冒")')
line('click("brave danger; venture")')
display("kanji/冒.md", "kanji")
for word in ("冒す", "冒険"):
    document = f"words/{word}.md"
    forward = follow("kanji/冒.md", word, document, word + "-forward")
    if word == "冒す":
        display(document, word)
    else:
        line(f"await({quote(documents[document][0][1])})")
        line('section("How the kanji combine")')
        index = next(i for i, block in enumerate(documents[document])
                     if block == ("heading", "How the kanji combine"))
        kind, value = documents[document][index + 1]
        show(document, index + 1, kind, value, word)
    reverse = follow(document, "冒", "kanji/冒.md", word + "-reverse")
    line('section("Readings")')
    line(f'show(readingExample("ボウ"), {quote(word + "-kanji-backlink")})')
    back_to(reverse, word + "-system-back-to-word")
    for char, mapped_word in ledger["allMappedReciprocalPairs"]:
        if mapped_word != document or char == "冒":
            continue
        assert char == "険"
        component = follow(document, char, f"kanji/{char}.md", word + "-" + char)
        kind, value = documents["kanji/険.md"][1]
        show("kanji/険.md", 1, kind, value, "険-fallback")
        counterpart = follow("kanji/険.md", word, document, "険-counterpart")
        line('section("How the kanji combine")')
        line(f"show(articleBullet({quote(component['renderedText'])}), {quote(word + '-険-component-backlink')})")
        back_to(counterpart, word + "-険-system-back-to-component")
        back_to(component, word + "-険-system-back-from-component")
    back_to(forward, word + "-system-back-to-kanji")
assert len(offsets) == 6
assert {(i["document"], i["destination"]) for i in offsets} == {
    pair for char, word in ledger["allMappedReciprocalPairs"]
    for pair in ((f"kanji/{char}.md", word), (word, f"kanji/{char}.md"))}
text = PRIOR.read_text(encoding="utf-8")
replacements = [
    ("076", "077"),
    ("concurrentRolesLookalikesAndPersonFallbackAcrossFourProductionFamilies",
     "bravingRiskLookalikesAndRadicalFallbacksAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineConcurrentRolesThreeReciprocalPairsBothReadingsDrawingAndSystemBack",
     "fullSingleImportOfflineBravingRiskThreeReciprocalPairsBothReadingsDrawingAndSystemBack"),
    ("b89b333682fa5bfb4123ea8f4a74c2cc59935a7c", HEAD), ("b89b3336", HEAD[:8]),
    ("8bd0a375668bee11", manifest["contentVersion"]),
    ("1088", "1089"), ("5045", "5046"),
    ("108, n1.size", "109, n1.size"), ("N1 · 108 cards", "N1 · 109 cards"),
    ("concurrentRoles", "bravingRisk"), ('"兼"', '"冒"'),
    ("combine; concurrent roles", "brave danger; venture"),
    ('listOf("ケン")', 'listOf("ボウ")'),
    ('listOf("か.ねる", "-か.ねる")', 'listOf("おか.す")'),
    ('listOf("か.ねる")', 'listOf("おか.す")'),
    ('listOf("けん")', 'listOf("ぼう")'), ('listOf("かねる")', 'listOf("おかす")'),
    ('"けん"', '"ぼう"'), ('"かねる"', '"おかす"'),
    ('"Other N1 meanings/readings postponed; 兼 meaning and curated on/kun due; valid suffix -か.ねる retained but not selected separately; one かねる key. Two historical good 兼 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress."',
     '"Other N1 meanings/readings postponed; 冒 meaning and both complete curated readings due. Two historical good 冒 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress."'),
    ("bothCuratedKindsPersistedGoodNoDuplicateSuffixAndDone", "bothCuratedKindsPersistedGoodAndDone"),
    ("assertEquals(10, strokes.length())", "assertEquals(9, strokes.length())"),
    ('"10 strokes drawn"', '"9 strokes drawn"'),
]
for old, new in replacements:
    assert old in text, old
    text = text.replace(old, new)
begin = text.index('            click("Browse all kanji")')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                              "".join((ROOT / n).read_text(encoding="utf-8") for n in names))))
assert set(glyphs) == set(audit["actualAuthoredHanFonts"]["characters"]) | {"攻"} and len(glyphs) == 39
fonts = []
for prior_font in audit["actualAuthoredHanFonts"]["fonts"]:
    font_path = Path(prior_font["path"])
    assert sha(font_path) == prior_font["sha256"]
    with TTFont(font_path) as font:
        missing = [char for char in glyphs if ord(char) not in font.getBestCmap()]
    assert missing == ["冂", "阝"]
    fonts.append({"path": str(font_path), "sha256": sha(font_path), "missingCurrentScopedHan": missing})
words = ["冒険", "冒す"]
pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
pages.append("冒 日 目 官 冂 阜 阝 険 犯 侵 " + " ".join(words))
text = re.sub(r'val pages = listOf\([^\n]+\)', "val pages = listOf(" + ", ".join(quote(p) for p in pages) + ")", text, count=1)
text = text.replace("Batch 077: concurrent roles / look-alikes / fallback",
                    "Batch 077: braving risk / look-alikes / radical fallback")
text = text.replace("Inspect all 41 scoped Han; focused 兼/典/具/曲/八 and 人/亻. Fallback families may coincide.",
                    "Inspect all 39 scoped Han; focused 冒/日/目/官, 冂 and 阜/阝. Fallback families may coincide.")
text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
              "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
text = re.sub(r'for \(word in listOf\([^\n]+\)\)',
              "for (word in listOf(" + ", ".join(quote(w) for w in words) + "))", text, count=1)
text = text.replace("assertEquals(172, rows.length())", "assertEquals(164, rows.length())")
text = text.replace('.put("individualGlyphProbes", 164)', '.put("individualGlyphProbes", 156)')
text = text.replace("41 scoped authored Han including pre-existing 亻,",
                    "39 scoped Han including metadata-only 攻 and pending 冂/阝 fallback inspection,")
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for stale in ("076", "かねる", "か.ねる", 'listOf("ケン")', "兼", "concurrentRoles", "suffix", "41 scoped", "10 strokes"):
    assert stale not in text, stale
counts = {
    "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
    "words": sum(n.startswith("words/") for n in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1089, "words": 5046, "n1": 109}
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-077/",
                f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(ARCHIVE) as archive:
    entries = archive.namelist()
    prefix = "n1-batch-077/"
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
assert verified == 8358
FOLDER.mkdir()
FIXTURE.write_text(text, encoding="utf-8")
diff = FOLDER / "fixture-from-076.diff"
diff.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=str(PRIOR.relative_to(ROOT)), tofile=str(FIXTURE.relative_to(ROOT)), n=0)), encoding="utf-8")
record = {
    "schemaVersion": 1, "execution": 517, "batch": "077", "status": "prepared-not-executed",
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
    "articleFiles": [{"path": n, "sha256": sha(ROOT / n), "projectedTextBlocks": len(b)}
                     for n, b in documents.items()],
    "sourceReadingLedger": "docs/n1-sources/batch-077-progress.json",
    "sourceReadingLedgerSha256": sha(ROOT / "docs" / "n1-sources" / "batch-077-progress.json"),
    "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
    "completeArticleProjections": 2, "changedReusedPassages": 2,
    "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6,
    "plannedNativePaintProbes": 156, "plannedWholeWordRasterProbes": 8,
    "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
    "currentFontAudit": fonts,
    "inventoryReconciliation": "Historical draft had 38 Han; reviewed metadata adds 攻 in the new direct quiz exclusion. Cover all39 raw scoped Han, including that metadata-only character. Historical audits remain unchanged.",
    "fullReadings": {"on": ["ボウ"], "kun": ["おか.す"]},
    "curatedReadings": {"on": ["ボウ"], "kun": ["おか.す"]},
    "normalizedQuizKeys": {"on": ["ぼう"], "kun": ["おかす"]},
    "pendingCmapAbsences": ["冂", "阝"],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
    "limits": "Preparation only until compilation is verified; not native rendering, PNG/visual, handwriting, phone or publication acceptance. No duplicate parser preflight; production ContentSync once. Static offsets/hashes are not visibility, readability or fallback-face proof. HOST-only2GiBinit NEVER enters native builds; no app/guest heap/archiveguard changes. Historical limitations retained.",
}
(CONTROL / "batch-077-native-fixture-verification.json").write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: record[key] for key in ("status", "expectedCounts", "zipEntries",
                 "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
print("Static selectors:", len(selectors), "; directed links:", len(offsets))
