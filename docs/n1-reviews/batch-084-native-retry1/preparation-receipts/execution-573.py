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
LOG = C / "logs" / "f5677e86-368f-4fb6-bd10-d95054b95439"
HEAD = "d5dd7e9e04aa45af0befeb3fd9a9044488fc7a0a"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "4b8bfcc4bc4fff4c73185a8cc6c27d4cb5736efc"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
FOLDER = R / "docs" / "n1-reviews" / "batch-083-native"
PRIOR = R / "docs" / "n1-reviews" / "batch-082-native-corrected" / "N1Batch082CorrectedNativeTest.kt"
FIXTURE = FOLDER / "N1Batch083NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-083-d5dd7e9e-envelope.zip"
VERIFICATION = C / "batch-083-native-fixture-verification.json"
BEFORE = C / "artifacts" / "execution-573-progress-before.json"
EVIDENCE = R / "docs" / "n1-sources" / "execution-573.json"
NEXT = (
    "SAME083 bounded native execution and direct PNG inspection next, then persist/yield. "
    "Read docs/n1-sources/execution-573.json and batch-083-native-fixture-verification.json. "
    "Verify signed d5dd7e9e full archive, fixture and frozen083 app/test APK hashes. "
    "No redundant compile/HOST/initial textual reviews absent new concern. Exact signed "
    "Android1c1b7bf4 TEST-ONLY harness atop unchanged productionf9; HOSTinit NEVER for native. "
    "Fresh local AND remote5580/5581 port ownership includingTimeWait, adbdevices/PIDs and "
    "live parent ancestry immediately before owned readonly N3_Acceptance_20261029 API35 "
    "emulator-5580 launch: hostGPU/-Vulkan/2048MiB/2core, explicitadbserial, one heavy "
    "process, stop only owned helper. No alternate port or shared-device interference. "
    "Require named terminal0/no skips/no-2/-3 BOTH N1Batch083GlyphTest and "
    "N1Batch083ArticleTest; full productionContentSyncONCE/1095kanji5052words115N1/"
    "a9faafdd68af3230/zeroProblems/acceptedepoch. Full+Lite onリョウ/kunしの.ぐ "
    "and curated same; onlyりょう/しのぐ offered and independently persisted. "
    "All29Han/fourfonts/Paint/directPNG/legibility/lookalikes including冫/夌/阝/隹, "
    "116individual+8wholewordrasters/3panels; complete凌/凌ぐ/凌駕, two reciprocal "
    "pairs/four directions, selection/meaning/exact准冶次 options/bothcuratedreadings/"
    "tenstroke trace/recall/SystemBack/offline/persistence. Injected tracing and giveup "
    "are not handwriting/MLKit/phone evidence. Preserve attempts/artifacts/cleanup. "
    "Original serial two-family dependent visual confirmations required before current-main "
    "integration; original sessions/models in083 reconciliation. Preserve source/reviewer/"
    "process/read-depth/viewport/fallback/MLKit/OOM/denial limits and all historical values. "
    "Then current combined-main Python/validator/vocabulary/manifest/exact reviewed quizguards/"
    "original archivebudgets, normally signed integration/ownerfastforward/exactremote/"
    "terminalgreenCI/EVERYimmutableZIPhash/terminalreceipts/ownerissue60 BEFORE084. "
    "Live parent owns runner.lock; children never acquire/delete/unlock it. Approved control "
    "helpers/committed sources only, no optional historicalsessionhelpers. Published109/1228,"
    "remaining1119/latestpublic21a5cb1328aadd437139a6b850f07298a2e2985d unchanged;083 not delivered. "
    "Physicalphone/generalrelease/whole-set outstanding. Preserve/report/yield actual new "
    "denial or signinghang without workaround."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    data = load(R / "manifest.json")
    assert data == build_manifest(R)
    assert data["contentVersion"] == "a9faafdd68af3230"
    assert sum(len(v) for v in data.values() if isinstance(v, dict)) == 8376
    return data


def update(p):
    temporary = C / "progress.573.tmp"
    assert not temporary.exists()
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")


def start():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 572 and p["status"] == "continue" and p["batch"] == "083"
    assert not BEFORE.exists()
    clean(R, HEAD)
    clean(A, APP)
    runtime()
    assert not git("diff", PRODUCTION, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)
    text = (LOG / "request.txt").read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 572
    shutil.copyfile(C / "progress.json", BEFORE)
    state = {
        "execution": 573, "batch": "083", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME083 native fixture/full archive preparation and compilation, normally signed LOCAL checkpoint only; no emulator/native execution/reviewer/integration/publication/084.",
        "request": {"sha256": sha(LOG / "request.txt"), "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Operative contract, complete issue and final checkpoint inspected directly; historical middle loaded/parsed, not freshly semantically re-reviewed."},
        "runtimeManifestHashesVerified": 8376,
        "runnerLockRole": "Verified live runner PID19008 is execution ancestor; no lock open/reacquire/delete/unlock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    p["execution573StartingState"] = state
    p["stage"] = "batch-083-native-preparation-in-progress"
    p["nextAction"] = state["scope"]
    update(p)
    save(C / "execution-573-start.json", state)
    print("Starting scope persisted with complete live history.")


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
    clean(R, HEAD)
    clean(A, APP)
    assert not FOLDER.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert not git("diff", TEACHING, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-083-reconciliation.json")
    assert reconciliation["textualReviewClosed"] and not reconciliation["actionableRemainingFindings"]
    audit = load(R / "docs" / "n1-sources" / "batch-083-draft-font-audit.json")
    names = audit["completeNewArticleScope"]
    assert names == ["kanji/凌.md", "words/凌ぐ.md", "words/凌駕.md"]
    assert not audit["changedReusedScope"]
    assert all(sha(R / name) == expected for name, expected in audit["articleHashes"].items())
    documents = {name: blocks(R / name) for name in names}
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

    def follow(document, label, destination, slug, preferred):
        body = (R / document).read_text(encoding="utf-8")
        sections = re.split(r"^## (.+)\n", body.split("---", 2)[2], flags=re.M)
        candidates = []
        for i in range(1, len(sections), 2):
            for part in re.split(r"\n\s*\n|\n(?=- )", sections[i + 1].strip()):
                for link in re.finditer(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", part):
                    if (R / document).parent.joinpath(link[1]).resolve() == (R / destination).resolve():
                        candidates.append((sections[i], part.removeprefix("- ")))
        section_name, raw = next(v for v in candidates if v[0] == preferred)
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        text = plain(" ".join(part.strip() for part in raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_573" + raw[link.end():]
        offset = plain(" ".join(part.strip() for part in marked.splitlines())).index("N1_LINK_TARGET_573")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("凌")')
    line('click("endure; surpass")')
    display("kanji/凌.md", "kanji")
    for word, slug in [("凌ぐ", "endure-word"), ("凌駕", "surpass-word")]:
        forward = follow("kanji/凌.md", word, f"words/{word}.md", slug + "-forward", "Common words")
        display(f"words/{word}.md", slug)
        reverse = follow(f"words/{word}.md", "凌", "kanji/凌.md", slug + "-reverse", "How the kanji combine")
        line('section("Readings")')
        line(f'show(readingExample("リョウ"), "{slug}-kanji-backlink")')
        back_to(reverse, slug + "-system-back-to-word")
        back_to(forward, slug + "-system-back-to-kanji")
    assert len(offsets) == 4
    assert {(i["document"], i["destination"]) for i in offsets} == {
        ("kanji/凌.md", "words/凌ぐ.md"), ("words/凌ぐ.md", "kanji/凌.md"),
        ("kanji/凌.md", "words/凌駕.md"), ("words/凌駕.md", "kanji/凌.md")}
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "            N1_ARTICLE_ROUTE_573\n" + text[end:]
    replacements = [
        ("n1-batch-082-corrected-e108bbeb-envelope.zip", ARCHIVE.name),
        ("082Corrected", "083"), ("082-corrected", "083"), ("Batch 082 corrected", "Batch 083"),
        ("associateRank", "endurance"), ("AssociateRankReciprocalAndComparisonLinksCuratedOn", "EnduranceTwoReciprocalPairsCuratedOnAndKun"),
        ("associate rank / look-alikes / radical fallback", "endurance / look-alikes / radical fallback"),
        ("e108bbeb0fcd4fda3837d955a652f662f72fdac1", HEAD),
        ("d82e7fefe3898a70", manifest["contentVersion"]),
        ("1094, updated.kanji", "1095, updated.kanji"), ("5050, updated.words", "5052, updated.words"),
        ("114, n1.size", "115, n1.size"), ("N1 · 114 cards", "N1 · 115 cards"),
        ('"准"', '"凌"'), ("quasi-; associate rank", "endure; surpass"),
        ('listOf("ジュン")', 'listOf("リョウ")'), ('"じゅん"', '"りょう"'),
        ("repeat(1)", "repeat(2)"), ("assertEquals(1, done.answered)", "assertEquals(2, done.answered)"),
        ("assertEquals(1, done.correct)", "assertEquals(2, done.correct)"),
        ("assertEquals(1, readingLogs.size)", "assertEquals(2, readingLogs.size)"),
        ('setOf("りょう"), readingLogs', 'setOf("りょう", "しのぐ"), readingLogs'),
        ("assertEquals(setOf(ReadingKind.On), answeredKinds)", "assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)"),
        ('capture("curated-on-done")', 'capture("curated-on-kun-done")'),
        ('put("soleCuratedOnPersistedGoodAndDone", true)', 'put("bothCuratedKindsPersistedGoodAndDone", true)'),
        ('.put("comparisonPairs", 1).put("comparisonLinkTransitions", 2)', '.put("completeArticleProjections", 3)'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = text.replace('listOf("冴", "冶", "隼")', 'listOf("准", "冶", "次")')
    text = re.sub(r'            val expectedMeanings = mapOf\([\s\S]*?\n            \)',
                  '            val expectedMeanings = mapOf(\n'
                  '                "凌" to "endure; surpass",\n'
                  '                "准" to "quasi-; associate rank",\n'
                  '                "冶" to "smelt; work metals",\n'
                  '                "次" to "next",\n            )', text, count=1)
    text = text.replace('            assertFalse(meaning.options.any { it.kanji == "倣" })\n', "")
    text = text.replace("assertEquals(emptyList<String>(), endurance.kunyomi.splitSep())",
                        'assertEquals(listOf("しの.ぐ"), endurance.kunyomi.splitSep())')
    text = text.replace("assertEquals(emptyList<String>(), endurance.quizKunyomi?.splitSep())",
                        'assertEquals(listOf("しの.ぐ"), endurance.quizKunyomi?.splitSep())')
    text = text.replace("assertEquals(emptyList<String>(), endurance.toReadingCard().quizKeys(ReadingKind.Kun))",
                        'assertEquals(listOf("しのぐ"), endurance.toReadingCard().quizKeys(ReadingKind.Kun))')
    text = text.replace("assertEquals(emptyList<String>(), card.kunyomi.splitSep())",
                        'assertEquals(listOf("しの.ぐ"), card.kunyomi.splitSep())')
    text = text.replace("assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())",
                        'assertEquals(listOf("しの.ぐ"), card.quizKunyomi?.splitSep())')
    text = text.replace('card.kanji == "凌" && kind == ReadingKind.On && key == "りょう"',
                        'card.kanji == "凌" && key == (if (kind == ReadingKind.On) "りょう" else "しのぐ")')
    text = text.replace('                assertEquals(ReadingKind.On, question.question.kind)\n'
                        '                val key = "りょう"',
                        '                val key = if (question.question.kind == ReadingKind.On) "りょう" else "しのぐ"')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 凌 meaning and curated onりょう/kunしのぐ due. Two historical good 凌 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    text = text.replace("            N1_ARTICLE_ROUTE_573", "\n".join(lines))
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "".join(
        (R / name).read_text(encoding="utf-8") for name in names))))
    assert glyphs == audit["actualHan"] and len(glyphs) == 29
    fonts = []
    for item in audit["fonts"]:
        path = Path(item["path"])
        assert sha(path) == item["sha256"]
        with TTFont(path) as font:
            missing = [c for c in glyphs if ord(c) not in font.getBestCmap()]
        assert missing == item["allActualMissing"] == ["冫", "夌", "阝", "隹"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    words = ["凌ぐ", "凌駕"]
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("凌 陵 准 冶 次 冫 夌 阝 隹 凌ぐ 凌駕")
    text = re.sub(r"val pages = listOf\([^\n]+\)",
                  "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)",
                  "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)",
                  "for (word in listOf(" + ", ".join(map(quote, words)) + "))", text, count=1)
    text = text.replace("34 scoped Han; focused 准/冴/冶/隼/準, 冫/氵/辶/隹",
                        "29 scoped Han; focused 凌/陵/准/冶/次, 冫/夌/阝/隹")
    text = text.replace("assertEquals(140, rows.length())", "assertEquals(124, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 136).put("wholeWordRasterProbes", 4)',
                        '.put("individualGlyphProbes", 116).put("wholeWordRasterProbes", 8)')
    text = text.replace("34 actual scoped Han including exact 冫/氵/辶/隹 fallback inspection",
                        "29 actual scoped Han including exact 冫/夌/阝/隹 fallback inspection")
    text = text.replace("four whole-word rasters", "eight whole-word rasters")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("082", "准教授", "ジュン", "じゅん", "associateRank", "AssociateRank",
                  "34 scoped", "氵", "辶", "emptyList<String>()", "sole curated", "Source and quiz kun lists empty"):
        assert stale not in text, stale
    assert 'listOf("リョウ"), endurance.quizOnyomi?.splitSep()' in text
    assert 'listOf("しの.ぐ"), endurance.quizKunyomi?.splitSep()' in text
    assert "repeat(2)" in text and 'assertEquals(2, readingLogs.size)' in text
    assert all(quote(item["target"]) in text for item in selectors)
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1095, "words": 5052, "n1": 115}
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-083/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        prefix = "n1-batch-083/"
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith(prefix) and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read(prefix + "manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=R)
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
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in archive.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    assert verified == 8376
    FOLDER.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-corrected-082.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.relative_to(R).as_posix(), n=2)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 573, "batch": "083", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": TEACHING, "androidSnapshot": APP,
        "productionBaseline": PRODUCTION, "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "fixtureDiff": diff.relative_to(R).as_posix(), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(documents[n])} for n in names],
        "completeArticleProjections": 3, "changedReusedPassages": 0,
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "plannedNativePaintProbes": 116, "plannedWholeWordRasterProbes": 8, "currentFontAudit": fonts,
        "fullReadings": {"on": ["リョウ"], "kun": ["しの.ぐ"]},
        "curatedReadings": {"on": ["リョウ"], "kun": ["しの.ぐ"]},
        "normalizedQuizKeys": {"on": ["りょう"], "kun": ["しのぐ"]},
        "pendingCmapAbsences": ["冫", "夌", "阝", "隹"],
        "exactMeaningOptions": {"凌": "endure; surpass", "准": "quasi-; associate rank",
                                "冶": "smelt; work metals", "次": "next"},
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": "Preparation only. Static Markdown selectors/offsets and cmap checks are not native visibility/legibility/fallback-face evidence. Full archive through production ContentSync once. Injected reference tracing and giveup recall are not handwriting recognition/MLKit/physical-phone acceptance. Fresh local AND remote port ownership including TimeWait required immediately before launch. No production/guest heap/archiveguard changes. All historical limitations retained."
    }
    save(VERIFICATION, record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes",
                                             "compressedBytes", "inflatedBytes", "retainedBytes")}))


def record():
    clean(A, APP)
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runtime()
    fixture = load(VERIFICATION)
    assert sha(FIXTURE) == fixture["fixtureSha256"] and sha(ARCHIVE) == fixture["archiveSha256"]
    assert (LOG / "native-compile-exit.txt").read_text().strip() == "0"
    command = load(LOG / "native-compile-command.json")
    assert command["hostOnlyHeapInitUsed"] is False
    assert command["arguments"] == [":app:assembleDebugAndroidTest", "--no-daemon", "--no-parallel", "--max-workers=1",
                                     "-Pkotlin.compiler.execution.strategy=in-process"]
    result = next(v for v in (LOG / "native-compile.txt").read_text().splitlines() if v.startswith("BUILD SUCCESSFUL"))
    apk = C / "artifacts" / "n1-batch-083-native-test.apk"
    app = C / "artifacts" / "n1-batch-083-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch083GlyphTest", "N1Batch083ArticleTest",
                     "enduranceLookalikesAndRadicalFallbacksAcrossFourProductionFamilies",
                     "fullSingleImportOfflineEnduranceTwoReciprocalPairsCuratedOnAndKunDrawingAndSystemBack"):
            assert name.encode() in dex, name
    receipts = FOLDER / "preparation-receipts"
    assert not receipts.exists()
    receipts.mkdir()
    provenance = []
    for source in [Path(__file__), C / "run-573-native-compile.ps1", C / "runner-lock-role-notes.txt",
                   C / "authoring-artifact-path-notes.txt", VERIFICATION,
                   *[LOG / n for n in ("native-compile-command.json", "native-compile-start.txt",
                                       "native-compile-end.txt", "native-compile-exit.txt")]]:
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    raw_log = LOG / "native-compile.txt"
    compressed_log = receipts / "native-compile-raw.txt.gz"
    with compressed_log.open("wb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, mtime=0) as zipped:
            zipped.write(raw_log.read_bytes())
    assert gzip.decompress(compressed_log.read_bytes()) == raw_log.read_bytes()
    provenance.append({"source": str(raw_log), "sourceSha256": sha(raw_log),
                       "archive": compressed_log.relative_to(R).as_posix(), "sha256": sha(compressed_log),
                       "losslessGzipVerified": True})
    save(EVIDENCE, {
        "schemaVersion": 1, "execution": 573, "batch": "083", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "teachingSnapshot": TEACHING, "androidHead": APP, "productionBaseline": PRODUCTION,
        "startingState": load(C / "execution-573-start.json"), "fixtureVerification": fixture,
        "buildResult": result, "compileExitCode": 0, "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "provenance": provenance, "runtimeManifestHashesVerified": 8376,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "hostChecksRerun": False, "nativeOrVisualExecuted": False,
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "diagnostics": [
            "Optional guessed app/ui/Markdown.kt path absent; located actual MarkdownView.kt before selector verification. No permission denial or missing mandatory artifact.",
            "First preparation static-selector assertion rejected template substitutions reaching the new article route. Stopped before writing fixture/archive; isolated template adaptation from literal current article projections, then rechecked every selector and offset.",
        ],
        "nextGate": NEXT,
        "inheritedNextGate": load(R / "docs" / "n1-sources" / "execution-572.json")["nextGate"],
        "limits": fixture["limits"],
    })
    print(result)
    print("APK assets/DEX/frozen bytes and production app equality verified; no native execution.")


def finish():
    clean(A, APP)
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("merge-base", HEAD, "HEAD") == HEAD
    runtime()
    evidence = load(EVIDENCE)
    assert not evidence["nativeOrVisualExecuted"] and not evidence["runtimePublished"]
    p = load(C / "progress.json")
    assert p["checkpoint"] == 572 and p["batch"] == "083"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    before = load(BEFORE)
    for key, value in before.items():
        if key not in allowed:
            assert p[key] == value, key
    summary = {
        "schemaVersion": 1, "execution": 573, "checkpoint": 573, "batch": "083",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": "native-prepared-compiled-awaiting-execution", "evidence": EVIDENCE.relative_to(R).as_posix(),
        "contentSnapshot": HEAD, "androidHead": APP, "runtimeManifestHashesVerified": 8376,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "nativeOrVisualExecuted": False, "hostChecksRerun": False,
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "dedicatedWorktreesClean": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    for key in ("checkpoint", "status", "stage", "nextAction"):
        p[key] = summary[key]
    p["blocker"] = None
    p["execution573CoordinatorCheckpoint"] = summary
    p["batch083NativePreparationCheckpoint"] = summary
    update(p)
    save(C / "execution-573-checkpoint.json", summary)
    print("Checkpoint573 persisted; full historical values preserved, both worktrees clean.")


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
