import difflib
import hashlib
import json
import posixpath
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
HEAD = "ee672744235275d321b4bfb33a6efe0286444594"
REVIEWED = "45c275e7"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-065-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-064-native" / "N1Batch064NativeTest.kt"


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(text):
    return re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text).replace("**", "")


def blocks(path):
    body = path.read_text(encoding="utf-8").split("---\n", 2)[2]
    result, paragraph = [], []

    def flush():
        if paragraph:
            result.append(("paragraph", plain(" ".join(paragraph))))
            paragraph.clear()

    for line in body.splitlines() + [""]:
        if not line:
            flush()
        elif line.startswith("#"):
            flush()
            result.append(("heading", line.lstrip("#").strip()))
        elif line.startswith("|"):
            flush()
            cells = line.strip("|").split("|")
            if not all(re.fullmatch(r"\s*-+\s*", cell) for cell in cells):
                result.extend(("table", plain(cell.strip())) for cell in cells)
        elif line.startswith("- "):
            flush()
            paragraph.append(line[2:])
        else:
            paragraph.append(line.strip())
    return result


assert git("rev-parse", "HEAD").decode().strip() == HEAD
assert git("log", "-1", "--format=%G?").decode().strip() == "G"
assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
assert git("rev-parse", "HEAD", cwd=ANDROID).decode().strip() == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
progress = json.loads((CONTROL / "progress.json").read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == 417 and progress["execution418StartingState"]["execution"] == 418
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1077, "words": 5036, "n1": 97}, counts
assert manifest["contentVersion"] == "6a940651167e0e94"
reports = {f"docs/n1-reviews/batch-065-initial-{family}.md":
           sha(ROOT / "docs" / "n1-reviews" / f"batch-065-initial-{family}.md")
           for family in ("claude", "gpt")}
text = PRIOR.read_text(encoding="utf-8")
replacements = (
    ("064", "065"),
    ("investigationLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
     "frugalityLookalikesOlderFormAndRadicalsAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineInvestigationTwoPairsComparisonOnOnlyDrawingAndSystemBack",
     "fullSingleImportOfflineFrugalityThreePairsBothCuratedReadingsDrawingAndSystemBack"),
    ("bf6204e5b4e4c64f340dcd8db65b2924b869cc45", HEAD), ("bf6204e5", HEAD[:8]),
    ("ae05977ba66f42f5", manifest["contentVersion"]),
    ("1076", "1077"), ("5034", "5036"), ("96, n1.size", "97, n1.size"),
    ("N1 · 96 cards", "N1 · 97 cards"),
    ('"偵 貞 停 低 値 人 亻 探 手 扌 探偵 刑事"', '"倹 儉 険 験 値 人 亻 阝 馬 約 糸 勺 倹約 倹しい"'),
    ('listOf("偵", "貞", "停", "低", "値", "人", "亻", "探", "手", "扌")',
     'listOf("倹", "儉", "険", "験", "値", "人", "亻", "阝", "馬", "約", "糸", "勺")'),
    ('listOf("探偵", "刑事")', 'listOf("倹約", "倹しい")'),
    ("Batch 065: investigation / look-alikes / radical variants",
     "Batch 065: thrift / look-alikes / older form / radicals"),
    ("Compare 偵 with 貞, 停, 低 and 値. Inspect 人 versus 亻, 手 versus 扌 in 探, and both words 探偵 and 刑事. Shared fallback need not give four different designs.",
     "Compare 倹 with 儉, 険, 験 and 値; inspect 人/亻, 阝, 馬 and 約 with 糸/勺. Read 倹約 and 倹しい. Shared fallback need not give four different designs."),
    ("assertEquals(48, rows.length())", "assertEquals(56, rows.length())"),
    ('.put("individualGlyphProbes", 40)', '.put("individualGlyphProbes", 48)'),
    ("Forty single-character native Paint probes including actual 人/亻 and 手/扌, eight complete-word nonblank raster probes and four production Compose rows; actual 偵/貞/停/低/値/人/亻/探/手/扌/探偵/刑事 readability requires separate visual inspection.",
     "Forty-eight single-character native Paint probes including older 儉 and actual 人/亻/阝/馬/糸/勺, eight complete-word nonblank raster probes and four production Compose rows; actual 倹/儉/険/験/値/人/亻/阝/馬/約/糸/勺/倹約/倹しい readability requires separate visual inspection."),
    ("investigation", "frugality"), ('"偵"', '"倹"'),
    ('listOf("テイ")', 'listOf("ケン")'), ('listOf("てい")', 'listOf("けん")'),
    ('key == "てい"', 'key == "けん"'),
    ('"spy; covert frugality"', '"frugal; thrifty"'),
    ("repeat(1)", "repeat(2)"),
    ('                assertEquals(ReadingKind.On, question.question.kind)\n                val key = "てい"',
     '                val key = if (question.question.kind == ReadingKind.On) "けん" else "つましい"'),
    ("assertEquals(setOf(ReadingKind.On), answeredKinds)", "assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)"),
    ('assertEquals(11, strokes.length())', 'assertEquals(10, strokes.length())'),
    ('"11 strokes drawn"', '"10 strokes drawn"'),
    ('soleCuratedOnQuestionAndPersistedGradeNoKun', 'bothCuratedReadingsAndPersistedGrades'),
    ("Other N1 meanings/readings postponed; 偵 meaning and sole curated on key due; explicit no-kun. Two historical good 偵 meaning logs unlock drawing.",
     "Other N1 meanings/readings postponed; 倹 meaning and both curated reading keys due. Full source-only つづまやか retained, not offered. Two historical good 倹 meaning logs unlock drawing."),
)
for old, new in replacements:
    assert old in text, old
    text = text.replace(old, new)
for owner in ("frugality", "card"):
    text = text.replace(f'assertEquals(emptyList<String>(), {owner}.kunyomi.splitSep())',
                        f'assertEquals(listOf("つま.しい", "つづまやか"), {owner}.kunyomi.splitSep())')
    text = text.replace(f'assertEquals(emptyList<String>(), {owner}.quizKunyomi?.splitSep())',
                        f'assertEquals(listOf("つま.しい"), {owner}.quizKunyomi?.splitSep())')
text = text.replace('assertEquals(emptyList<String>(), frugality.toReadingCard().quizKeys(ReadingKind.Kun))',
                    'assertEquals(listOf("つましい"), frugality.toReadingCard().quizKeys(ReadingKind.Kun))')
text = text.replace('(kind == ReadingKind.On && key == "けん")',
                    '((kind == ReadingKind.On && key == "けん") || (kind == ReadingKind.Kun && key == "つましい"))')
text = text.replace('it.kanji == "倹" && it.mode == ReadingKind.Kun.mode.name }',
                    'it.kanji == "倹" && it.mode == ReadingKind.Kun.mode.name && it.reading == "つづまやか" }')
start = text.index('            click("Browse all kanji")')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = r'''            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("倹")
            click("frugal; thrifty")
            await("Article contents")
            await("as left-hand 亻", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("倹 concerns thrift", "kanji-meaning")
            show("Modern-shape mnemonic, not etymology:", "kanji-mnemonic")
            section("Readings")
            show(readingExample("倹約 けんやく — thrift; frugality"), "kanji-on-reading")
            show(readingExample("倹しい つましい — frugal; modest in one's living; usually written in kana"), "kanji-kun-reading")
            show(readingExample("source-only character-dictionary reading associated with frugality or restraint; no verified practical word spelled with 倹 is supplied here"), "kanji-source-only")
            show("The full source lists and their order are retained.", "kanji-curation-boundary")
            section("Notes")
            show("Compare the similar right-hand shapes", "kanji-lookalikes")
            show("倹しい is つましい, not つつましい.", "kanji-pronunciation-boundary")
            show("The older form of 倹 is 儉", "kanji-older-form")
            section("Common words")
            show(articleBullet("倹約家 (けんやくか) — a thrifty person"), "kanji-frugal-person")
            inline(await(articleBullet("倹約 けんやく — thrift; frugality")), "倹約")
            await("倹約 (けんやく) — thrift; frugality")
            section("Meaning")
            show("倹約 means avoiding wasteful spending", "thrift-meaning")
            show(articleBullet("小遣いを倹約しています。 (こづかいをけんやくしています。) — I am economizing on my spending money."), "thrift-verb-example")
            show(articleBullet("倹約な生活を送っています。 (けんやくなせいかつをおくっています。) — I lead a frugal life."), "thrift-adjective-example")
            show("With する, the expenditure being reduced takes を.", "thrift-attachment")
            section("How the kanji combine")
            show("The on readings combine as ケン + ヤク: けんやく.", "thrift-reading-allocation")
            inline(await("contributes reduction or restraint here.", substring = true), "倹")
            await("Article contents")
            section("Readings")
            show(readingExample("倹約 けんやく — thrift; frugality"), "thrift-person-backlink")
            back()
            await("contributes reduction or restraint here.", substring = true).assertIsDisplayed()
            capture("system-back-thrift-person")
            inline(await("contributes reduction or restraint here.", substring = true), "約")
            await("Article contents")
            await("Key (radical):", substring = true).performScrollTo().assertIsDisplayed()
            capture("agreement-radical")
            section("Meaning and origin")
            show("約 has two particularly useful jobs", "agreement-two-uses")
            show("This recalls the promise meaning only", "agreement-mnemonic")
            section("Readings")
            show(readingExample("約束 やくそく — promise; 予約 よやく — reservation"), "agreement-on-reading")
            show(readingExample("約 やく — approximately"), "agreement-approximate-reading")
            show("The source's kun readings remain", "agreement-source-boundary")
            section("Notes")
            show("約束を守る", "agreement-promise-example")
            show("Identify 約 by its relatively simple 勺", "agreement-lookalikes")
            section("Common words")
            show(articleBullet("約束 やくそく — promise; arrangement"), "agreement-common-promise")
            show(articleBullet("予約 よやく — reservation; booking"), "agreement-common-reservation")
            show(articleBullet("約 やく — about; approximately, before a quantity"), "agreement-common-approximation")
            inline(await(articleBullet("倹約 けんやく — thrift; frugality")), "倹約")
            await("倹約 (けんやく) — thrift; frugality")
            section("How the kanji combine")
            show("The on readings combine as ケン + ヤク: けんやく.", "thrift-agreement-backlink")
            back()
            await(articleBullet("倹約 けんやく — thrift; frugality")).assertIsDisplayed()
            capture("system-back-agreement")
            back()
            await("contributes reduction or restraint here.", substring = true).assertIsDisplayed()
            section("Synonyms and antonyms")
            show("節約 also readily describes saving electricity or time", "thrift-conservation-boundary")
            show("spending less does not guarantee that the difference is saved.", "thrift-saving-boundary")
            section("Distinctive meaning")
            show("倹約 does not inherently call someone a miser.", "thrift-stinginess-boundary")
            show("neither is an unrestricted replacement for the other.", "thrift-economy-boundary")
            inline(await("describes frugal or modest living as an い-adjective.", substring = true), "倹しい")
            await("倹しい (つましい) — frugal; modest in one's living")
            section("Meaning")
            show("つましい describes living without extravagance", "modest-meaning-spelling")
            show(articleBullet("二人はつましい暮らしをしています。 (ふたりはつましいくらしをしています。) — The two of them lead a modest life."), "modest-living-example")
            show(articleBullet("私たちの生活はつましいですが、満足しています。 (わたしたちのせいかつはつましいですが、まんぞくしています。) — Our life is modest, but we are content."), "modest-content-example")
            show("It is an い-adjective:", "modest-attachment")
            section("How the kanji combine")
            show("supplies つま, with しい as the written ending", "modest-reading-boundary")
            show("JMdict also recognizes 約しい", "modest-spelling-flag")
            inline(await("supplies つま, with しい as the written ending", substring = true), "倹")
            await("Article contents")
            section("Common words")
            inline(await(articleBullet("倹しい つましい — frugal; modest in one's living; usually written つましい")), "倹しい")
            await("倹しい (つましい) — frugal; modest in one's living")
            section("How the kanji combine")
            show("supplies つま, with しい as the written ending", "modest-person-backlink")
            back()
            await(articleBullet("倹しい つましい — frugal; modest in one's living; usually written つましい")).assertIsDisplayed()
            capture("system-back-person-modest")
            back()
            await("supplies つま, with しい as the written ending", substring = true).assertIsDisplayed()
            section("Synonyms and antonyms")
            show("Compare 倹約する", "modest-thrift-contrast")
            show("Do not manufacture a strict behavior-versus-lifestyle split", "modest-pronunciation-overlap")
            inline(await("Compare 倹約する", substring = true), "倹約")
            await("倹約 (けんやく) — thrift; frugality")
            section("Meaning")
            show("With する, the expenditure being reduced takes を.", "modest-thrift-backlink")
            back()
            await("Compare 倹約する", substring = true).assertIsDisplayed()
            capture("system-back-modest-thrift")
            section("Distinctive meaning")
            show("つましい does not itself say", "modest-judgment-boundary")
            show("Nor does つましい mean", "modest-simple-boundary")
            back()
            await("describes frugal or modest living as an い-adjective.", substring = true).assertIsDisplayed()
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for obsolete in ("064", "偵", "探偵", "刑事", "テイ", '"てい"', "investigation", "soleCurated", "no-kun"):
    assert obsolete not in text, obsolete
assert text.count('listOf("つま.しい", "つづまやか")') == 2
assert text.count('listOf("つま.しい")') == 2
assert 'repeat(2)' in text and '"つづまやか" }' in text
documents = {name: blocks(ROOT / name) for name in (
    "kanji/倹.md", "words/倹約.md", "kanji/約.md", "words/倹しい.md")}
stack, selectors, controls, transitions = ["kanji/倹.md"], [], [], []
quoted = r'"((?:\\.|[^"\\])*)"'
for number, line in enumerate(route.splitlines(), 1):
    document = stack[-1]
    shown = re.search(r'show\((?:(readingExample|articleBullet)\()?' + quoted + r'\)?, "([^"]+)"\)', line)
    section = re.search(r'section\("([^"]+)"\)', line)
    awaited = re.search(r'await\((?:(readingExample|articleBullet)\()?' + quoted + r'(?:, substring = (true|false))?', line)
    if shown:
        qualifier, target, step = shown.groups()
        operation, substring = "show", qualifier is None
    elif section:
        qualifier, target, step = "heading", section.group(1), None
        operation, substring = "section", False
    elif awaited:
        qualifier, target, sub = awaited.groups()
        operation, substring, step = "await", sub == "true", None
    else:
        if line.strip() == "back()":
            assert len(stack) > 1
            stack.pop()
        elif re.fullmatch(r'\s*capture\("[^"]+"\)', line):
            pass
        elif line.strip() in ('click("Browse all kanji")', 'click("frugal; thrifty")') or "performTextReplacement" in line:
            pass
        else:
            raise AssertionError(line)
        continue
    target = target.replace('\\"', '"')
    if target in ("Article contents", "Common words") and operation == "await":
        controls.append({"routeLine": number, "target": target})
    else:
        matches = [(kind, value) for kind, value in documents[document]
                   if (target in value if substring else target == value)
                   and (qualifier != "heading" or kind == "heading")
                   and (qualifier != "readingExample" or kind == "table")
                   and (qualifier != "articleBullet" or kind != "table")]
        assert len(matches) == 1, (number, document, target, matches)
        selectors.append({"routeLine": number, "document": document, "operation": operation,
                          "target": target, "substring": substring, "qualifier": qualifier,
                          "step": step, "matches": matches})
    if "inline(await" in line:
        label = re.search(r', "([^"]+)"\)$', line).group(1)
        links = re.findall(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", (ROOT / document).read_text(encoding="utf-8"))
        destinations = {posixpath.normpath(posixpath.join(posixpath.dirname(document), link)) for link in links}
        assert len(destinations) == 1, (document, label, destinations)
        destination = destinations.pop()
        assert destination in documents
        transitions.append([document, destination])
        stack.append(destination)
assert stack == ["kanji/倹.md"]
expected_transitions = {
    ("kanji/倹.md", "words/倹約.md"), ("words/倹約.md", "kanji/倹.md"),
    ("words/倹約.md", "kanji/約.md"), ("kanji/約.md", "words/倹約.md"),
    ("words/倹約.md", "words/倹しい.md"), ("words/倹しい.md", "words/倹約.md"),
    ("words/倹しい.md", "kanji/倹.md"), ("kanji/倹.md", "words/倹しい.md"),
}
assert len(transitions) == 8 and {tuple(pair) for pair in transitions} == expected_transitions
archive = CONTROL / "artifacts" / "n1-batch-065-ee672744-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-065/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-065/"
    assert len(names) == len(set(names)) and len(names) <= 18000
    assert all(name.startswith(prefix) and "\\" not in name
               and ".." not in PurePosixPath(name).parts and not PurePosixPath(name).is_absolute()
               for name in names)
    manifest_bytes = zipped.read(prefix + "manifest.json")
    assert manifest_bytes == git("show", f"{HEAD}:manifest.json")
    assert json.loads(manifest_bytes) == manifest
    assert (manifest["schemaVersion"], manifest["baseLanguage"], manifest["targetLanguage"]) == (1, "en", "ja")
    retained, verified = len(manifest_bytes), 0
    binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, expected in entries.items():
            data = zipped.read(prefix + name)
            limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                     512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
            assert len(data) <= limit, name
            normalized = data if section in binary else data.replace(b"\r\n", b"\n")
            assert hashlib.sha256(normalized).hexdigest() == expected, name
            retained += len(data)
            verified += 1
    inflated = sum(info.file_size for info in zipped.infolist())
    assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
    assert archive.stat().st_size <= 42 * 1024 * 1024
    assert not any("/docs/" in name or "/tools/" in name for name in names)
assert verified == sum(len(value) for value in manifest.values() if isinstance(value, dict))
FOLDER.mkdir()
fixture = FOLDER / "N1Batch065NativeTest.kt"
fixture.write_text(text, encoding="utf-8")
diff = FOLDER / "fixture-from-064.diff"
diff.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=fixture.relative_to(ROOT).as_posix(), n=0)), encoding="utf-8")
record = {
    "schemaVersion": 1, "execution": 418, "batch": "065",
    "status": "static-native-preparation-verified-not-executed",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
    "contentSnapshot": HEAD, "reviewedTeachingSnapshot": git("rev-parse", REVIEWED).decode().strip(),
    "androidSnapshot": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
    "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
    "archive": str(archive), "archiveSha256": sha(archive), "zipEntries": len(names),
    "compressedBytes": archive.stat().st_size, "inflatedBytes": inflated,
    "retainedBytes": retained, "verifiedRuntimeHashes": verified, "manifestEqual": True,
    "safePathsPerFileAndOriginalPublishingBudgetsPassed": True,
    "fixture": str(fixture), "fixtureSha256": sha(fixture),
    "reusedAcceptedHarness": str(PRIOR.relative_to(ROOT)), "reusedAcceptedHarnessSha256": sha(PRIOR),
    "fixtureDiff": str(diff.relative_to(ROOT)), "fixtureDiffSha256": sha(diff),
    "originalInitialReportHashesUnchanged": reports,
    "articleFiles": [{"path": name, "sha256": sha(ROOT / name), "projectedTextBlocks": len(items)}
                     for name, items in documents.items()],
    "staticMarkdownSelectors": selectors, "renderedNavigationControls": controls,
    "articleRouteTransitions": transitions,
    "captureSteps": len(re.findall(r'(?:show\([^\n]+, |capture\()"([^"]+)"\)', route)),
    "plannedNativePaintProbes": 48, "plannedWholeWordRasterProbes": 8,
    "plannedGlyphs": ["倹", "儉", "険", "験", "値", "人", "亻", "阝", "馬", "約", "糸", "勺"],
    "plannedWholeWords": ["倹約", "倹しい"],
    "fullReadings": {"on": ["ケン"], "kun": ["つま.しい", "つづまやか"]},
    "curatedReadings": {"on": ["ケン"], "kun": ["つま.しい"]},
    "normalizedQuizKeys": {"on": ["けん"], "kun": ["つましい"]},
    "reciprocalPairs": [["倹", "倹約"], ["約", "倹約"], ["倹", "倹しい"]],
    "comparisonPair": ["倹約", "倹しい"],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted417AndroidRetainedWithoutRerun": True, "nativeExecuted": False,
    "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "projectionQualification": "Bounded heading/paragraph/bullet/table projection reused from accepted064. Static selectors establish matching text and link destinations, not native semantics, viewport readability or visual acceptance.",
    "hostTestInitScriptUsed": False,
    "limits": "Preparation only. Full Git envelope and production ContentSync ONCE with unchanged guards. All three mapped pairs in six directions plus support comparison in both directions planned, not executed. Full readings retained; source-only つづまやか not offered. Paint hashes do not establish readable glyphs or fallback-face identity. Reference trace/recall miss do not establish human handwriting or MLKit recognition. Fresh device/port ownership required before separate native execution. Original416 denial, actual1GiB HOST OOM, original049512MiB failure and qualified HOST-only2GiB retry preserved; HOST init not for native builds. No native/reviewer/publication/066/second runner. Published91/1228,1137remain; phone/general-release/whole-set outstanding.",
}
(CONTROL / "batch-065-native-fixture-verification.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: record[key] for key in ("status", "contentVersion", "expectedCounts",
                 "archiveSha256", "zipEntries", "compressedBytes", "inflatedBytes",
                 "retainedBytes", "verifiedRuntimeHashes", "fixtureSha256", "captureSteps")}, indent=2))
print("Article selectors:", len(selectors), "Directed transitions:", len(transitions))
