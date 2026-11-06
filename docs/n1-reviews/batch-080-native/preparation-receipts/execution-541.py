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
LOGS = CONTROL / "logs" / "593f89b0-4aa4-4f11-bcd4-d94ebc4f2dea"
HEAD = "0d2c9aee6de9e4f430935b38e31228db4bd47908"
REVIEWED = "3f883347e81422abce490ee633e874be55ef01ad"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-080-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-079-native" / "N1Batch079NativeTest.kt"
FIXTURE = FOLDER / "N1Batch080NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-080-0d2c9aee-envelope.zip"
VERIFICATION = CONTROL / "batch-080-native-fixture-verification.json"
NEXT = (
    "SAME080 bounded native execution/actual PNG inspection ONLY, then persist/yield; "
    "no publication/081/reviewer/second runner. Read docs/n1-sources/execution-541.json "
    "and batch-080-native-fixture-verification.json; verify frozen full signed0d2c9aee "
    "archive and n1-batch-080-native-test.apk hashes before use. No recompile or HOST3+1 "
    "rerun absent new concern. Fresh device/5580/5581/PID ownership BEFORE approved "
    "read-only API35 N3_Acceptance_20261029 launch; batch0405584override was batch-specific. "
    "Same hostGPU/-Vulkan/2048MiB/2core, explicit actual serial, JDK17/SDK, one heavy "
    "process; stop only owned helper. Require terminal status0/no skips for BOTH "
    "N1Batch080GlyphTest and N1Batch080ArticleTest. Production ContentSync imports "
    "entire signed Git archive ONCE, no duplicate parse:1092kanji5048words112N1/"
    "contentVersion4572f7b1d0d95059/zeroProblems/acceptedepoch. Full+Lite retain "
    "onゴ,コ and kunさ.える,こお.る,ひ.える in order, explicit empty quizOnyomi "
    "and quizKunyomiさ.える; no offered on key, sole offered kunさえる. "
    "Inspect all30Han/fourproductionfamilies, exact冫/冱/氵fallback and "
    "冴/次/汗/河/牙,120individual+4wholewordrasters/threeComposepanels. "
    "Actual complete冴/冴える articles, onepair/twodirections, N1selection/meaning/"
    "singlecuratedkun/sevenstroke trace then recall/systemBack/offline. Injected "
    "reference tracing/giveup recall are not handwriting recognition or phone. "
    "Preserve attempts/PNGs/provenance/cleanup, normally signed LOCAL evidence, yield. "
    "Later two serial original-family visual confirmations ClaudeOpus5.5/GPT6.1Sol "
    "required, original sessions a3b94466-63e4-4403-a67d-3249751e5a1b and "
    "27fb4006-7e5d-4d5c-aabb-c8316fb8f334. Textual closure3f883347 and fresh540 "
    "HOST3+1/no skips inherited honestly. All source/review/read-depth/process/"
    "denial/OOM/phone limitations and baseline exceptions retained. Approved workspace/"
    "committed packets/durablecontrolhelpers only, no optional historicalsession recipes. "
    "Preserve FULL live history. HOST-only2GiBinit NEVER enters native builds; no "
    "app/guestheap/archiveguard increase. Later currentmain non-rewriting integration/"
    "revalidation/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/"
    "originalbudgets/verified ownerissue60 mandatory. No unreviewedpush; signinghang "
    "stop/yield no retry; preserve/report/yield actualnewdenial. Published106/1228,"
    "remaining1122; local107thaddition textuallyclosednotpublished. CompatibleAndroid"
    "f9b59a2+; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 540 and progress["batch"] == "080"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not (LOGS / "progress-before-541.json").exists()
    save(LOGS / "progress-before-541.json", progress)
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 540
    record = {
        "schemaVersion": 1, "execution": 541, "batch": "080", "startingHead": HEAD,
        "androidHead": git("rev-parse", "HEAD", cwd=ANDROID),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME080 native fixture preparation/compile ONLY; no device/emulator/reviewer/integration/publication/081 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and embedded checkpoint parsed; operative contract, complete issue and final540 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "freshOriginMain": git("rev-parse", "origin/main"),
        "manifestSha256": sha(ROOT / "manifest.json"),
        "contentVersion": load(ROOT / "manifest.json")["contentVersion"],
        "artifactPathPreflight": str(CONTROL / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "preparing-native-fixture",
    }
    progress["execution541StartingState"] = record
    progress["stage"] = "native-fixture-preparation-in-progress"
    save(CONTROL / "progress.json", progress)
    save(LOGS / "starting-state-541.json", record)
    print("Starting scope persisted with full live history.")


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


def prepare():
    from fontTools.ttLib import TTFont

    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert not FOLDER.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 540 and progress["batch"] == "080"
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-080-reconciliation.json")
    assert reconciliation["textualReviewClosed"] and not reconciliation["actionableRemainingFindings"]
    assert reconciliation["reviewedTeachingSnapshot"] == REVIEWED
    manifest = load(ROOT / "manifest.json")
    assert manifest["contentVersion"] == "4572f7b1d0d95059"
    ledger_path = ROOT / "docs" / "n1-sources" / "batch-080-progress.json"
    ledger = load(ledger_path)
    audit = load(ROOT / "docs" / "n1-sources" / "batch-080-draft-font-audit.json")
    assert ledger["sourceReadingOrder"] == {
        "onyomi": ["ゴ", "コ"], "kunyomi": ["さ.える", "こお.る", "ひ.える"]}
    assert [(i["reading"], i["selected"]) for i in ledger["readingDispositions"]] == [
        ("ゴ", False), ("コ", False), ("さ.える", True), ("こお.る", False), ("ひ.える", False)]
    names = audit["completeRuntimeScope"]
    assert all(sha(ROOT / name) == audit["articleHashes"][name] for name in names)
    documents = {name: blocks(ROOT / name) for name in names}
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_541" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_541")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("冴")')
    line('click("clear; sharp-minded")')
    display("kanji/冴.md", "kanji")
    forward = follow("kanji/冴.md", "冴える", "words/冴える.md", "word-forward")
    display("words/冴える.md", "word")
    reverse = follow("words/冴える.md", "冴", "kanji/冴.md", "word-reverse")
    line('section("Readings")')
    line('show(readingExample("さ.える"), "kanji-backlink")')
    back_to(reverse, "system-back-to-word")
    back_to(forward, "system-back-to-kanji")
    assert len(offsets) == 2
    assert {(i["document"], i["destination"]) for i in offsets} == {
        pair for char, word in ledger["allMappedReciprocalPairs"]
        for pair in ((f"kanji/{char}.md", word), (word, f"kanji/{char}.md"))}

    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    replacements = [
        ("079", "080"),
        ("crownLookalikesAndCoverRoofFallbacksAcrossFourProductionFamilies",
         "clarityLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineCrownThreeReciprocalPairsBothReadingsDrawingAndSystemBack",
         "fullSingleImportOfflineClarityOneReciprocalPairCuratedKunDrawingAndSystemBack"),
        ("3fdc0bf952e299060b5a07ac372bb6d926595a4c", HEAD),
        ("3fdc0bf9", HEAD[:8]), ("a01eb85b17601ac0", manifest["contentVersion"]),
        ("1091", "1092"), ("5047", "5048"), ("111, n1.size", "112, n1.size"),
        ("N1 · 111 cards", "N1 · 112 cards"),
        ("crown", "clarity"), ('"冠"', '"冴"'),
        ("clarity; peerless", "clear; sharp-minded"),
        ('listOf("カン")', 'listOf("ゴ", "コ")'),
        ('listOf("かんむり")', 'listOf("さ.える", "こお.る", "ひ.える")'),
        ('listOf("かん")', 'emptyList<String>()'),
        ('"かんむり"', '"さえる"'), ('"かん"', '"NO_ON_KEY"'),
        ('repeat(2) {', 'repeat(1) {'),
        ("assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)",
         "assertEquals(setOf(ReadingKind.Kun), answeredKinds)"),
        ("assertEquals(2, done.answered)", "assertEquals(1, done.answered)"),
        ("assertEquals(2, done.correct)", "assertEquals(1, done.correct)"),
        ("assertEquals(2, readingLogs.size)", "assertEquals(1, readingLogs.size)"),
        ('assertEquals(setOf("NO_ON_KEY", "さえる"), readingLogs.map { it.reading }.toSet())',
         'assertEquals(setOf("さえる"), readingLogs.map { it.reading }.toSet())'),
        ("curated-both-done", "curated-kun-done"),
        ('assertEquals(9, strokes.length())', 'assertEquals(7, strokes.length())'),
        ('"9 strokes drawn"', '"7 strokes drawn"'),
        ('.put("mappedReciprocalPairs", 3).put("directedLinkTransitions", 6)',
         '.put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2)'),
        ('"bothCuratedKindsPersistedGoodAndDone"', '"soleCuratedKunPersistedGoodAndDone"'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    for card in ("clarity", "card"):
        text = text.replace(
            f'assertEquals(listOf("ゴ", "コ"), {card}.quizOnyomi?.splitSep())',
            f'assertEquals(emptyList<String>(), {card}.quizOnyomi?.splitSep())')
        text = text.replace(
            f'assertEquals(listOf("さ.える", "こお.る", "ひ.える"), {card}.quizKunyomi?.splitSep())',
            f'assertEquals(listOf("さ.える"), {card}.quizKunyomi?.splitSep())')
    text = text.replace(
        'assertEquals(listOf("さ.える", "こお.る", "ひ.える"), clarity.toReadingCard().quizKeys(ReadingKind.Kun))',
        'assertEquals(listOf("さえる"), clarity.toReadingCard().quizKeys(ReadingKind.Kun))')
    text = text.replace(
        'val key = if (question.question.kind == ReadingKind.On) "NO_ON_KEY" else "さえる"',
        'assertEquals(ReadingKind.Kun, question.question.kind)\n                val key = "さえる"')
    text = text.replace(
        'if (card.kanji == "冴" && ((kind == ReadingKind.On && key == "NO_ON_KEY") || (kind == ReadingKind.Kun && key == "さえる")))',
        'if (card.kanji == "冴" && kind == ReadingKind.Kun && key == "さえる")')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 冴 meaning and sole curated kun key さえる due. Explicit empty on list. Two historical good 冴 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                                  "".join((ROOT / n).read_text(encoding="utf-8") for n in names))))
    assert glyphs == audit["actualHan"] and len(glyphs) == 30
    fonts = []
    for prior_font in audit["fonts"]:
        path = Path(prior_font["path"])
        assert sha(path) == prior_font["sha256"]
        with TTFont(path) as font:
            missing = [c for c in glyphs if ord(c) not in font.getBestCmap()]
        assert missing == prior_font["allActualMissing"] == ["冫", "冱", "氵"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    words = ["冴える"]
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("冴 次 汗 河 冫 氵 冱 牙 冴える 冱える 冴寒 頭 目 眠 冷 凍")
    text = re.sub(r'val pages = listOf\([^\n]+\)',
                  "val pages = listOf(" + ", ".join(quote(p) for p in pages) + ")", text, count=1)
    text = text.replace("Batch 080: clarity / look-alikes / cover and roof fallback",
                        "Batch 080: clarity / look-alikes / ice and water fallback")
    text = text.replace(
        "Inspect all 35 scoped Han; focused 冠/冗/完/守/元/寸, 冖 and 宀. Fallback families may coincide.",
        "Inspect all 30 scoped Han; focused 冴/次/汗/河/牙, 冫/冱/氵. Fallback families may coincide.")
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
                  "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)',
                  "for (word in listOf(" + ", ".join(quote(w) for w in words) + "))", text, count=1)
    text = text.replace("assertEquals(148, rows.length())", "assertEquals(124, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 140).put("wholeWordRasterProbes", 8)',
                        '.put("individualGlyphProbes", 120).put("wholeWordRasterProbes", 4)')
    text = text.replace(
        "35 actual scoped Han including exact 冖/宀 fallback inspection, four production families, three bounded Compose panels and eight whole-word rasters.",
        "30 actual scoped Han including exact 冫/冱/氵 fallback inspection, four production families, three bounded Compose panels and four whole-word rasters.")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("079", "冠", '"かん"', "かんむり", "カン", "NO_ON_KEY", "35 scoped", "冖", "宀", "peerless"):
        assert stale not in text, (stale, [row for row in text.splitlines() if stale in row])
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
        "words": sum(n.startswith("words/") for n in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (ROOT / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1092, "words": 5048, "n1": 112}
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-080/",
                    f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        prefix = "n1-batch-080/"
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
    assert verified == 8366
    FOLDER.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-079.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(PRIOR.relative_to(ROOT)), tofile=str(FIXTURE.relative_to(ROOT)), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 541, "batch": "080", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "androidSnapshot": git("rev-parse", "HEAD", cwd=ANDROID),
        "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": str(PRIOR.relative_to(ROOT)), "priorHarnessSha256": sha(PRIOR),
        "staticProjection": "Durable helper subset follows production Markdown.kt paragraph/table/list rules. Static selectors/offsets are not native visibility.",
        "fixtureDiff": str(diff.relative_to(ROOT)), "fixtureDiffSha256": sha(diff),
        "articleFiles": [{"path": n, "sha256": sha(ROOT / n), "projectedTextBlocks": len(b)}
                         for n, b in documents.items()],
        "sourceReadingLedger": str(ledger_path.relative_to(ROOT)), "sourceReadingLedgerSha256": sha(ledger_path),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 2, "changedReusedPassages": 0,
        "mappedReciprocalPairs": 1, "mappedDirectedTransitions": 2,
        "plannedNativePaintProbes": 120, "plannedWholeWordRasterProbes": 4,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "currentFontAudit": fonts,
        "fullReadings": {"on": ["ゴ", "コ"], "kun": ["さ.える", "こお.る", "ひ.える"]},
        "curatedReadings": {"on": [], "kun": ["さ.える"]},
        "normalizedQuizKeys": {"on": [], "kun": ["さえる"]},
        "pendingCmapAbsences": ["冫", "冱", "氵"],
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": "Preparation only until compile verified; no native rendering, PNG/visual, handwriting, phone or publication acceptance. No duplicate parser preflight; production ContentSync once. Static projections/hashes are not visibility/readability/fallback-face proof. HOST-only2GiBinit NEVER enters native builds; no app/guestheap/archiveguard changes. Fresh port/device/PID ownership inspection required before later launch. Historical limitations retained.",
    }
    save(VERIFICATION, record)
    print(json.dumps({key: record[key] for key in ("status", "expectedCounts", "zipEntries",
                     "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))


def record():
    starting = load(LOGS / "starting-state-541.json")
    fixture = load(VERIFICATION)
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain", cwd=ANDROID)
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert sha(ROOT / "manifest.json") == starting["manifestSha256"]
    assert (LOGS / "native-compile-exit.txt").read_text().strip() == "0"
    result = next(line for line in (LOGS / "native-compile.txt").read_text().splitlines()
                  if line.startswith("BUILD SUCCESSFUL"))
    assert "0 error(s)" in (LOGS / "validate.txt").read_text()
    assert sha(Path(fixture["fixture"])) == fixture["fixtureSha256"]
    assert sha(Path(fixture["archive"])) == fixture["archiveSha256"]
    apk = CONTROL / "artifacts" / "n1-batch-080-native-test.apk"
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/n1-batch-080-0d2c9aee-envelope.zip")).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch080GlyphTest", "N1Batch080ArticleTest",
                     "clarityLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies",
                     "fullSingleImportOfflineClarityOneReciprocalPairCuratedKunDrawingAndSystemBack"):
            assert name.encode() in dex, name
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    copied = []
    for source in (Path(__file__), CONTROL / "run-541-native-compile.ps1"):
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        copied.append({"path": str(target.relative_to(ROOT)), "sha256": sha(target)})
    for name in ("native-compile.txt", "native-compile-start.txt", "native-compile-end.txt",
                 "native-compile-exit.txt", "validate.txt", "manifest.txt"):
        source = LOGS / name
        target = FOLDER / name
        if name == "native-compile.txt":
            raw = FOLDER / "native-compile-raw.txt.gz"
            raw.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(raw.read_bytes()) == source.read_bytes()
            target.write_text("\n".join(line.rstrip() for line in source.read_text().splitlines()) + "\n",
                              encoding="utf-8")
            copied.append({"path": str(raw.relative_to(ROOT)), "sha256": sha(raw),
                           "decompressedSha256": sha(source)})
        else:
            shutil.copyfile(source, target)
            assert sha(source) == sha(target)
        copied.append({"path": str(target.relative_to(ROOT)), "sha256": sha(target)})
    frozen = ROOT / "docs" / "n1-sources" / VERIFICATION.name
    shutil.copyfile(VERIFICATION, frozen)
    evidence = {
        **starting, "schemaVersion": 1, "checkpoint": 541, "status": "continue",
        "stage": "native-fixture-compiled-awaiting-execution",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "nativePreparation": fixture, "fixtureVerification": str(frozen.relative_to(ROOT)),
        "fixtureVerificationSha256": sha(frozen),
        "compile": {
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 -Pkotlin.compiler.execution.strategy=in-process",
            "exitCode": 0, "buildResult": result,
            "startedAt": (LOGS / "native-compile-start.txt").read_text().strip(),
            "endedAt": (LOGS / "native-compile-end.txt").read_text().strip(),
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
            "oneWorker": True, "parallel": False, "hostOnlyHeapInitUsed": False,
            "productionOrGuestHeapChanged": False, "archiveGuardsChanged": False,
            "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
            "apkContainsExactFrozenArchive": True, "bothClassesAndMethodsInDex": True,
            "temporarySourceAndAssetRemoved": True, "androidWorktreeClean": True,
        },
        "archivedReceipts": copied, "originalCompileLogPreservedByteForByteInGzip": True,
        "normalizedLogDifference": "Readable compile log strips trailing whitespace only; original compressed bytes retained.",
        "validatorErrors": 0, "manifestFresh": True, "manifestBytesUnchanged": True,
        "runtimeUnchanged": True, "runtimePublished": False, "nativeExecuted": False,
        "deviceOrEmulatorInspected": False, "reviewersLaunched": 0, "nextBatchStarted": False,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": starting["freshOriginMain"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "limits": "Preparation/native test APK compile only. No native case/device/PNG/visual/phone/publication acceptance. Fresh540 HOST3+1 inherited without rerun; original source/review/read-depth/process/denial/OOM/phone limitations retained.",
        "diagnostics": [
            "Initial request summary print hit cp1252 UnicodeEncodeError after full load/parse; ASCII-safe summary succeeded before mutation.",
            "Broad control filename listing produced oversized output; narrowed subsequent discovery; no historical session-state helper accessed."
        ],
    }
    save(ROOT / "docs" / "n1-sources" / "execution-541.json", evidence)
    print(json.dumps({"stage": evidence["stage"], "apkSha256": sha(apk),
                      "exactArchiveInsideApk": True, "receipts": len(copied)}, indent=2))


def checkpoint():
    progress = load(CONTROL / "progress.json")
    original = load(LOGS / "progress-before-541.json")
    assert progress["checkpoint"] == 540 and progress["batch"] == "080"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    evidence = load(ROOT / "docs" / "n1-sources" / "execution-541.json")
    receipt = load(LOGS / "issue-response.json")
    body = (LOGS / "issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.rstrip()
    assert "issues/60#issuecomment-" in receipt["html_url"]
    assert sha(ROOT / "manifest.json") == evidence["manifestSha256"]
    result = {
        "schemaVersion": 1, "execution": 541, "checkpoint": 541, "batch": "080",
        "savedCommit": signed, "signature": "G", "status": "continue",
        "stage": "native-fixture-compiled-awaiting-execution",
        "evidence": "docs/n1-sources/execution-541.json",
        "compileExitCode": 0, "nativeCasesExecuted": 0, "nativeExecuted": False,
        "fixtureSha256": evidence["nativePreparation"]["fixtureSha256"],
        "archiveSha256": evidence["nativePreparation"]["archiveSha256"],
        "testApkSha256": evidence["compile"]["apkSha256"],
        "runtimePayloadHashesVerified": 8366, "contentVersion": evidence["contentVersion"],
        "runtimeBytesUnchanged": True, "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "originalRootKeyCountCompared": len(original),
        "changedRootFields": ["checkpoint", "status", "stage", "nextAction", "blocker"],
    }
    progress.update(checkpoint=541, status="continue", stage=result["stage"], nextAction=NEXT, blocker=None)
    progress["execution541CoordinatorCheckpoint"] = result
    progress["batch080NativePreparation"] = result
    allowed = set(result["changedRootFields"])
    for key, value in original.items():
        if key not in allowed:
            assert progress[key] == value, key
    save(CONTROL / "progress.json", progress)
    check = load(CONTROL / "progress.json")
    for key, value in original.items():
        if key not in allowed:
            assert check[key] == value, key
    save(LOGS / "checkpoint-verification.json", result)
    print(json.dumps({"checkpoint": 541, "savedCommit": signed, "status": "continue",
                      "historyKeysPreserved": len(original), "issueUpdate": receipt["html_url"]}, indent=2))


{"start": start, "prepare": prepare, "record": record, "checkpoint": checkpoint}[sys.argv[1]]()
