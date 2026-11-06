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
HEAD = "3fdc0bf952e299060b5a07ac372bb6d926595a4c"
REVIEWED = "084d5301d175189d6e83aa77666ae495abed6f47"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-079-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-077-native" / "N1Batch077NativeTest.kt"
FIXTURE = FOLDER / "N1Batch079NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-079-3fdc0bf9-envelope.zip"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def quote(text):
    return json.dumps(text, ensure_ascii=False).replace("$", "\\$")


def plain(text):
    return re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text).replace("**", "")


def blocks(path):
    body = path.read_text(encoding="utf-8").split("---\n", 2)[2]
    result, paragraph = [], []

    def flush():
        if paragraph:
            result.append(("paragraph", plain(" ".join(paragraph))))
            paragraph.clear()

    for value in body.splitlines() + [""]:
        if not value.strip():
            flush()
        elif value.startswith("#"):
            flush()
            result.append(("heading", value.lstrip("#").strip()))
        elif value.startswith("|"):
            flush()
            cells = value.strip("|").split("|")
            if not all(re.fullmatch(r"\s*-+\s*", cell) for cell in cells):
                result.extend(("table", plain(cell.strip())) for cell in cells)
        elif re.match(r"^\s*[-*+]\s+", value):
            flush()
            paragraph.append(re.sub(r"^\s*[-*+]\s+", "", value))
        else:
            paragraph.append(value.strip())
    return result


assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
assert not FOLDER.exists() and not ARCHIVE.exists()
progress = load(CONTROL / "progress.json")
assert progress["checkpoint"] == 532 and progress["batch"] == "079"
assert progress["batch079TextualReview"]["savedCommit"] == REVIEWED
manifest = load(ROOT / "manifest.json")
assert manifest["contentVersion"] == "a01eb85b17601ac0"
ledger = load(ROOT / "docs" / "n1-sources" / "batch-079-progress.json")
audit = load(ROOT / "docs" / "n1-sources" / "batch-079-draft-font-audit.json")
assert ledger["sourceReadingOrder"] == {"onyomi": ["カン"], "kunyomi": ["かんむり"]}
assert [(i["reading"], i["selected"]) for i in ledger["readingDispositions"]] == [
    ("カン", True), ("かんむり", True)]
names = audit["completeRuntimeScope"]
assert all(sha(ROOT / name) == audit["articleHashes"][name] for name in names)
documents = {name: blocks(ROOT / name) for name in names}
assert ("paragraph", "王様は金の冠をかぶっていました。 (おうさまはきんのかんむりをかぶっていました。) - The king was wearing a gold crown.") in documents["words/冠.md"]
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
    assert candidates, (document, label, destination)
    section_name, raw = next((v for v in candidates if v[0] == preferred), candidates[0])
    link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
    text = plain(" ".join(raw.splitlines()))
    marked = raw[:link.start()] + "N1_LINK_TARGET_533" + raw[link.end():]
    offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_533")
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
line('rule.onNode(hasSetTextAction()).performTextReplacement("冠")')
line('click("crown; peerless")')
display("kanji/冠.md", "kanji")
forward = follow("kanji/冠.md", "冠", "words/冠.md", "冠-forward")
display("words/冠.md", "冠")
reverse = follow("words/冠.md", "kanji", "kanji/冠.md", "冠-reverse")
line('section("Readings")')
line('show(readingExample("かんむり"), "冠-kanji-backlink")')
back_to(reverse, "冠-system-back-to-word")
back_to(forward, "冠-system-back-to-kanji")
forward = follow("kanji/冠.md", "王冠", "words/王冠.md", "王冠-forward")
display("words/王冠.md", "王冠")
reverse = follow("words/王冠.md", "冠", "kanji/冠.md", "王冠-reverse")
line('section("Readings")')
line('show(readingExample("カン"), "王冠-kanji-backlink")')
back_to(reverse, "王冠-system-back-to-word")
component = follow("words/王冠.md", "王", "kanji/王.md", "王冠-王")
line(f"await({quote(documents['kanji/王.md'][0][1])})")
counterpart = follow("kanji/王.md", "王冠", "words/王冠.md", "王-counterpart")
line('section("How the kanji combine")')
line(f"show(articleBullet({quote(component['renderedText'])}), \"王冠-王-component-backlink\")")
back_to(counterpart, "王冠-王-system-back-to-component")
back_to(component, "王冠-王-system-back-from-component")
back_to(forward, "王冠-system-back-to-kanji")
assert len(offsets) == 6
assert {(i["document"], i["destination"]) for i in offsets} == {
    pair for char, word in ledger["allMappedReciprocalPairs"]
    for pair in ((f"kanji/{char}.md", word), (word, f"kanji/{char}.md"))}

text = PRIOR.read_text(encoding="utf-8")
replacements = [
    ("077", "079"),
    ("bravingRiskLookalikesAndRadicalFallbacksAcrossFourProductionFamilies",
     "crownLookalikesAndCoverRoofFallbacksAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineBravingRiskThreeReciprocalPairsBothReadingsDrawingAndSystemBack",
     "fullSingleImportOfflineCrownThreeReciprocalPairsBothReadingsDrawingAndSystemBack"),
    ("46dff1466ac9f3cf64b54e197c05088414939896", HEAD), ("46dff146", HEAD[:8]),
    ("2944928c13e2165a", manifest["contentVersion"]),
    ("1089", "1091"), ("5046", "5047"), ("109, n1.size", "111, n1.size"),
    ("N1 · 109 cards", "N1 · 111 cards"),
    ("bravingRisk", "crown"), ('"冒"', '"冠"'),
    ("brave danger; venture", "crown; peerless"),
    ('listOf("ボウ")', 'listOf("カン")'), ('listOf("おか.す")', 'listOf("かんむり")'),
    ('listOf("ぼう")', 'listOf("かん")'), ('listOf("おかす")', 'listOf("かんむり")'),
    ('"ぼう"', '"かん"'), ('"おかす"', '"かんむり"'),
    ('"Other N1 meanings/readings postponed; 冒 meaning and both complete curated readings due. Two historical good 冒 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress."',
     '"Other N1 meanings/readings postponed; 冠 meaning and both complete curated keys かん/かんむり due. Two historical good 冠 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress."'),
]
for old, new in replacements:
    assert old in text, old
    text = text.replace(old, new)
begin = text.index('            click("Browse all kanji")')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                              "".join((ROOT / n).read_text(encoding="utf-8") for n in names))))
assert glyphs == audit["actualHan"] and len(glyphs) == 35
fonts = []
for prior_font in audit["fonts"]:
    font_path = Path(prior_font["path"])
    assert sha(font_path) == prior_font["sha256"]
    with TTFont(font_path) as font:
        missing = [char for char in glyphs if ord(char) not in font.getBestCmap()]
    assert missing == prior_font["allActualMissing"] == ["冖", "宀"]
    fonts.append({"path": str(font_path), "sha256": sha(font_path), "missingCurrentScopedHan": missing})
words = ["冠", "王冠"]
pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
pages.append("冠 冗 完 守 冖 宀 元 寸 王 王冠 冠たる 世界 帽子 蓋 栓")
text = re.sub(r'val pages = listOf\([^\n]+\)', "val pages = listOf(" + ", ".join(quote(p) for p in pages) + ")", text, count=1)
text = text.replace("Batch 079: braving risk / look-alikes / radical fallback",
                    "Batch 079: crown / look-alikes / cover and roof fallback")
text = text.replace("Inspect all 39 scoped Han; focused 冒/日/目/官, 冂 and 阜/阝. Fallback families may coincide.",
                    "Inspect all 35 scoped Han; focused 冠/冗/完/守/元/寸, 冖 and 宀. Fallback families may coincide.")
text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
              "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
text = re.sub(r'for \(word in listOf\([^\n]+\)\)',
              "for (word in listOf(" + ", ".join(quote(w) for w in words) + "))", text, count=1)
text = text.replace("assertEquals(164, rows.length())", "assertEquals(148, rows.length())")
text = text.replace('.put("individualGlyphProbes", 156)', '.put("individualGlyphProbes", 140)')
text = text.replace("39 scoped Han including metadata-only 攻 and pending 冂/阝 fallback inspection,",
                    "35 actual scoped Han including exact 冖/宀 fallback inspection,")
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for stale in ("077", "冒", "険", '"ボウ"', '"ぼう"', "おかす", "おか.す", "bravingRisk", "39 scoped", "冂", "阝"):
    assert stale not in text, (stale, [row for row in text.splitlines() if stale in row])
counts = {
    "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
    "words": sum(n.startswith("words/") for n in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1091, "words": 5047, "n1": 111}
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-079/",
                f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(ARCHIVE) as archive:
    entries = archive.namelist()
    prefix = "n1-batch-079/"
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
assert verified == 8363
FOLDER.mkdir()
FIXTURE.write_text(text, encoding="utf-8")
diff = FOLDER / "fixture-from-077.diff"
diff.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=str(PRIOR.relative_to(ROOT)), tofile=str(FIXTURE.relative_to(ROOT)), n=0)), encoding="utf-8")
record = {
    "schemaVersion": 1, "execution": 533, "batch": "079", "status": "prepared-not-executed",
    "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED,
    "androidSnapshot": git("rev-parse", "HEAD", cwd=ANDROID),
    "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
    "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
    "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
    "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
    "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
    "priorHarness": str(PRIOR.relative_to(ROOT)), "priorHarnessSha256": sha(PRIOR),
    "staticProjection": "Durable local helper; scoped subset follows production Markdown.kt paragraph/table/list rules, including indented continuation and translation bullets. Offsets and projections are not native visibility.",
    "productionMarkdownPath": str(ANDROID / "core" / "src" / "main" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "markdown" / "Markdown.kt"),
    "fixtureDiff": str(diff.relative_to(ROOT)), "fixtureDiffSha256": sha(diff),
    "articleFiles": [{"path": n, "sha256": sha(ROOT / n), "projectedTextBlocks": len(b)}
                     for n, b in documents.items()],
    "sourceReadingLedger": "docs/n1-sources/batch-079-progress.json",
    "sourceReadingLedgerSha256": sha(ROOT / "docs" / "n1-sources" / "batch-079-progress.json"),
    "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
    "completeArticleProjections": 3, "changedReusedPassages": 1,
    "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6,
    "plannedNativePaintProbes": 140, "plannedWholeWordRasterProbes": 8,
    "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
    "currentFontAudit": fonts,
    "fullReadings": {"on": ["カン"], "kun": ["かんむり"]},
    "curatedReadings": {"on": ["カン"], "kun": ["かんむり"]},
    "normalizedQuizKeys": {"on": ["かん"], "kun": ["かんむり"]},
    "pendingCmapAbsences": ["冖", "宀"],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
    "limits": "Preparation only until compilation is verified; not native rendering, PNG/visual, handwriting, phone or publication acceptance. No duplicate parser preflight; production ContentSync once. Static offsets/hashes are not visibility/readability/fallback-face proof. HOST-only2GiBinit NEVER enters native builds; no app/guest heap/archiveguard changes. Fresh port/device/PID ownership inspection required before later launch. Historical limitations retained.",
}
(CONTROL / "batch-079-native-fixture-verification.json").write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: record[key] for key in ("status", "expectedCounts", "zipEntries",
                 "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
print("Static selectors:", len(selectors), "; directed links:", len(offsets))
