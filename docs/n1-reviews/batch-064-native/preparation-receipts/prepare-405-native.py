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
HEAD = "bf6204e5b4e4c64f340dcd8db65b2924b869cc45"
REVIEWED = "ff6eb7893344b806bf517ebd41bf19089bed5021"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-064-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-063-native" / "N1Batch063NativeTest.kt"


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
assert progress["checkpoint"] == 404 and progress["execution405StartingState"]["execution"] == 405
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1076, "words": 5034, "n1": 96}, counts
assert manifest["contentVersion"] == "ae05977ba66f42f5"
reports = {f"docs/n1-reviews/batch-064-initial-{family}.md":
           sha(ROOT / "docs" / "n1-reviews" / f"batch-064-initial-{family}.md")
           for family in ("claude", "gpt")}
text = PRIOR.read_text(encoding="utf-8")
for old, new in (
    ("063", "064"),
    ("imitationLookalikesAndPersonFallbackAcrossFourProductionFamilies",
     "investigationLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineImitationTwoReciprocalPairsBothReadingsDrawingAndSystemBack",
     "fullSingleImportOfflineInvestigationTwoPairsComparisonOnOnlyDrawingAndSystemBack"),
    ("53ecd11711804be900ca95f9f1018942910aecec", HEAD),
    ("53ecd117", HEAD[:8]), ("c19b742b7e6320a7", manifest["contentVersion"]),
    ("1075", "1076"), ("5033", "5034"), ("95, n1.size", "96, n1.size"),
    ("N1 · 95 cards", "N1 · 96 cards"),
    ('"倣 放 方 付 人 亻 模 木 傚 習 攵 模倣 倣う"', '"偵 貞 停 低 値 人 亻 探 手 扌 探偵 刑事"'),
    ('listOf("倣", "放", "方", "付", "人", "亻", "模", "木", "傚", "習", "攵")',
     'listOf("偵", "貞", "停", "低", "値", "人", "亻", "探", "手", "扌")'),
    ('listOf("模倣", "倣う")', 'listOf("探偵", "刑事")'),
    ("Batch 064: imitation / look-alikes / person fallback",
     "Batch 064: investigation / look-alikes / radical variants"),
    ("Compare 倣 with 放, 方 and 付. Inspect 人 versus 亻, 模 with 木, reused rare 傚 and 習, and both words 模倣 and 倣う. Shared fallback need not give four different designs.",
     "Compare 偵 with 貞, 停, 低 and 値. Inspect 人 versus 亻, 手 versus 扌 in 探, and both words 探偵 and 刑事. Shared fallback need not give four different designs."),
    ("assertEquals(52, rows.length())", "assertEquals(48, rows.length())"),
    ('.put("individualGlyphProbes", 44)', '.put("individualGlyphProbes", 40)'),
    ("Forty-four single-character native Paint probes including actual 人 and 亻, eight complete-word nonblank raster probes and four production Compose rows; actual 倣/放/方/付/人/亻/模/木/傚/習/攵/模倣/倣う readability requires separate visual inspection.",
     "Forty single-character native Paint probes including actual 人/亻 and 手/扌, eight complete-word nonblank raster probes and four production Compose rows; actual 偵/貞/停/低/値/人/亻/探/手/扌/探偵/刑事 readability requires separate visual inspection."),
    ("imitate; emulate", "spy; covert investigation"), ("imitation", "investigation"),
    ('"倣"', '"偵"'), ('"ホウ"', '"テイ"'), ('"ほう"', '"てい"'),
    ("倣 meaning and both curated on/kun keys due. Two historical good 倣 meaning logs",
     "偵 meaning and sole curated on key due; explicit no-kun. Two historical good 偵 meaning logs"),
    ("assertEquals(10, strokes.length())", "assertEquals(11, strokes.length())"),
    ('"10 strokes drawn"', '"11 strokes drawn"'),
    ("bothCuratedReadingsAndPersistedGoodGrades", "soleCuratedOnQuestionAndPersistedGradeNoKun"),
):
    assert old in text, old
    text = text.replace(old, new)
for owner in ("investigation", "card"):
    for field in ("kunyomi.splitSep()", "quizKunyomi?.splitSep()"):
        old = f'assertEquals(listOf("なら.う"), {owner}.{field})'
        assert old in text, old
        text = text.replace(old, f"assertEquals(emptyList<String>(), {owner}.{field})")
text = text.replace('assertEquals(listOf("ならう"), investigation.toReadingCard().quizKeys(ReadingKind.Kun))',
                    "assertEquals(emptyList<String>(), investigation.toReadingCard().quizKeys(ReadingKind.Kun))")
text = text.replace('((kind == ReadingKind.On && key == "てい") || (kind == ReadingKind.Kun && key == "ならう"))',
                    '(kind == ReadingKind.On && key == "てい")')
text = text.replace("repeat(2) {", "repeat(1) {")
text = text.replace('                val key = if (question.question.kind == ReadingKind.On) "てい" else "ならう"',
                    '                assertEquals(ReadingKind.On, question.question.kind)\n                val key = "てい"')
text = text.replace(
    "            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)",
    """            assertEquals(setOf(ReadingKind.On), answeredKinds)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "偵" && it.mode == ReadingKind.Kun.mode.name }
            })""")
start = text.index('            await("no. 9)"')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = r'''            await("no. 9)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("偵 concerns finding out hidden information", "kanji-meaning")
            show("Learn 偵 through compounds", "kanji-compound-boundary")
            show("Modern-shape mnemonic:", "kanji-mnemonic")
            show("etymology or an explanation based on 貞's meaning.", "kanji-origin-boundary")
            section("Readings")
            show(readingExample("探偵 たんてい — detective; investigator"), "kanji-on-reading")
            show("No kun reading is supplied", "kanji-no-kun")
            section("Notes")
            show(articleBullet("A 探偵 may be a private investigator; 刑事 けいじ specifically names a police detective in its person sense. The shared English word \"detective\" does not make these identical job labels."), "kanji-role-contrast")
            show(articleBullet("停, \"halt; stopping,\" shares 亻 and テイ but has a different right side, with a roof-like top and a long lower hook."), "kanji-stop-lookalike")
            show(articleBullet("低, \"low,\" and 値, \"value; price,\" also share 亻. Compare the entire right side, not just the radical or a boxed outline."), "kanji-other-lookalikes")
            section("Common words")
            show(articleBullet("探偵小説 たんていしょうせつ — detective story"), "kanji-detective-story")
            show(articleBullet("偵察 ていさつ — scouting; reconnaissance"), "kanji-reconnaissance")
            inline(await(articleBullet("探偵 たんてい — detective; investigator")), "探偵")
            await("探偵 (たんてい) - detective; secret investigation")
            section("Meaning")
            show("私立探偵 (しりつたんてい)", "detective-role")
            show(articleBullet("探偵に調査を頼みました。 (たんていにちょうさをたのみました。) - I asked a detective to carry out an investigation."), "detective-request-example")
            show(articleBullet("探偵小説を読むのが好きです。 (たんていしょうせつをよむのがすきです。) - I like reading detective stories."), "detective-fiction-example")
            show("In the first example, に marks the person asked", "detective-particles-and-activity")
            show("including the transitive する form 探偵する.", "detective-suru-boundary")
            section("How the kanji combine")
            show("The on readings are タン + テイ: たんてい.", "detective-components")
            inline(await("contributes searching or probing", substring = true), "偵")
            await("Article contents")
            section("Readings")
            show(readingExample("探偵 たんてい — detective; investigator"), "detective-backlink")
            back()
            await("contributes searching or probing", substring = true).assertIsDisplayed()
            capture("system-back-detective")
            inline(await("contributes searching or probing", substring = true), "探")
            await("探 — search")
            await("no. 64)", substring = true).performScrollTo().assertIsDisplayed()
            capture("search-radical")
            section("Meaning and origin")
            show("Searching does not itself say that the thing has been found.", "search-meaning")
            show("imagine the hand-side 扌 searching", "search-mnemonic")
            section("Readings")
            show("The examples select the two kun readings", "search-on-boundary")
            show(readingExample("探す さがす — look for; seek"), "search-reading-sagasu")
            show(readingExample("探る さぐる — feel around; investigate"), "search-reading-saguru")
            section("Notes")
            show("this is a spelling tendency, not an absolute separation.", "search-spelling-boundary")
            show("Their right sides are different:", "search-lookalikes")
            section("Common words")
            show(articleBullet("探す さがす — search for"), "search-common-sagasu")
            show(articleBullet("探る さぐる — feel around for; probe"), "search-common-saguru")
            inline(await(articleBullet("探偵 たんてい — detective; investigator (探 is タン here)")), "探偵")
            await("探偵 (たんてい) - detective; secret investigation")
            section("How the kanji combine")
            show("The on readings are タン + テイ: たんてい.", "search-backlink")
            back()
            await(articleBullet("探偵 たんてい — detective; investigator (探 is タン here)")).assertIsDisplayed()
            capture("system-back-search")
            back()
            await("contributes searching or probing", substring = true).assertIsDisplayed()
            section("Synonyms and antonyms")
            show("not a rule that every occurrence of 探偵 excludes police.", "detective-police-boundary")
            show("None of these three by itself names the detective.", "detective-other-words")
            show("There is no single useful antonym", "detective-antonym-boundary")
            inline(await("not a rule that every occurrence of 探偵 excludes police.", substring = true), "刑事")
            await("刑事 (けいじ) - police detective; criminal matters")
            section("Meaning")
            show("刑事 has two related uses:", "police-two-senses")
            show(articleBullet("刑事が目撃者に話を聞いています。 (けいじがもくげきしゃにはなしをきいています。) - A detective is talking to a witness."), "police-witness-example")
            show(articleBullet("これは刑事事件です。 (これはけいじじけんです。) - This is a criminal case."), "police-criminal-case-example")
            show("it does not mean \"a detective's incident.\"", "police-legal-boundary")
            section("How the kanji combine")
            show("刑 contributes criminal punishment", "police-components")
            section("Distinctive meaning")
            show("Neither use means \"criminal\" as a noun naming the person", "police-criminal-person-boundary")
            section("Synonyms and antonyms")
            show("it is not an opposite kind of police officer.", "police-role-comparison")
            inline(await("it is not an opposite kind of police officer.", substring = true), "探偵")
            await("探偵 (たんてい) - detective; secret investigation")
            section("Synonyms and antonyms")
            show("not a rule that every occurrence of 探偵 excludes police.", "police-comparison-backlink")
            back()
            await("it is not an opposite kind of police officer.", substring = true).assertIsDisplayed()
            capture("system-back-police")
            back()
            await("not a rule that every occurrence of 探偵 excludes police.", substring = true).assertIsDisplayed()
            section("Distinctive meaning")
            show("English \"detective\" can describe a police officer", "detective-role-summary")
            show("The compound alone does not say that an investigation succeeds.", "detective-success-boundary")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for obsolete in ("063", "倣", "模倣", "なら", "ホウ", "ほう", "imitation", "53ecd117", "1075", "5033", "bothCurated"):
    assert obsolete not in text, obsolete
assert text.count('assertEquals(emptyList<String>(),') == 5
assert text.count("repeat(1)") == 1 and "repeat(2)" not in text
documents = {name: blocks(ROOT / name) for name in (
    "kanji/偵.md", "words/探偵.md", "kanji/探.md", "words/刑事.md")}
stack, selectors, controls, transitions = ["kanji/偵.md"], [], [], []
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
        assert line.strip() == "back()" or re.fullmatch(r'\s*capture\("[^"]+"\)', line), line
        if line.strip() == "back()":
            assert len(stack) > 1
            stack.pop()
        continue
    target = target.replace('\\"', '"')
    if target == "Article contents":
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
        assert destination in documents, destination
        transitions.append([document, destination])
        stack.append(destination)
assert stack == ["kanji/偵.md"]
expected_transitions = {
    ("kanji/偵.md", "words/探偵.md"), ("words/探偵.md", "kanji/偵.md"),
    ("words/探偵.md", "kanji/探.md"), ("kanji/探.md", "words/探偵.md"),
    ("words/探偵.md", "words/刑事.md"), ("words/刑事.md", "words/探偵.md"),
}
assert len(transitions) == 6 and {tuple(pair) for pair in transitions} == expected_transitions
accepted = json.loads((ROOT / "docs" / "n1-sources" / "execution-404.json").read_text(encoding="utf-8"))
for item in accepted["archivedArtifacts"]:
    assert sha(ROOT / item["path"]) == item["sha256"]
for test in accepted["recovery"]["tests"]:
    assert test["failures"] == test["errors"] == test["skipped"] == 0
archive = CONTROL / "artifacts" / "n1-batch-064-bf6204e5-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-064/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-064/"
    assert len(names) == len(set(names)) and len(names) <= 18000
    assert all(name.startswith(prefix) and "\\" not in name
               and ".." not in PurePosixPath(name).parts and not PurePosixPath(name).is_absolute()
               for name in names)
    manifest_bytes = zipped.read(prefix + "manifest.json")
    assert manifest_bytes == git("show", f"{HEAD}:manifest.json")
    assert json.loads(manifest_bytes) == manifest
    assert manifest["schemaVersion"] == 1
    assert (manifest["baseLanguage"], manifest["targetLanguage"]) == ("en", "ja")
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
fixture = FOLDER / "N1Batch064NativeTest.kt"
fixture.write_text(text, encoding="utf-8")
diff = FOLDER / "fixture-from-063.diff"
diff.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=fixture.relative_to(ROOT).as_posix(), n=0)), encoding="utf-8")
for name, expected in reports.items():
    assert sha(ROOT / name) == expected
record = {
    "schemaVersion": 1, "execution": 405, "batch": "064",
    "status": "static-native-preparation-verified-not-executed",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
    "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED,
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
    "plannedNativePaintProbes": 40, "plannedWholeWordRasterProbes": 8,
    "plannedGlyphs": ["偵", "貞", "停", "低", "値", "人", "亻", "探", "手", "扌"],
    "plannedWholeWords": ["探偵", "刑事"],
    "fullReadings": {"on": ["テイ"], "kun": []},
    "curatedReadings": {"on": ["テイ"], "kun": []},
    "normalizedQuizKeys": {"on": ["てい"], "kun": []},
    "reciprocalPairs": [["偵", "探偵"], ["探", "探偵"]],
    "comparisonPair": ["刑事", "探偵"],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted404AndroidRetainedWithoutRerun": True, "nativeExecuted": False,
    "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "projectionQualification": "Bounded heading/paragraph/bullet/table projection reused from accepted063 and checked against production core/markdown/Markdown.kt; these four articles use its supported subset. Static selectors are not a native semantics tree or readability acceptance.",
    "limits": "Preparation only. Exact full Git envelope; production ContentSync called ONCE with unchanged guards. Both mapped pairs in four directions and comparison pair in both directions, sole curated on-reading/no-kun, eleven touch-reference strokes/ungraded trace and recall miss are planned, not executed. Paint hashes do not identify fallback faces or certify readability. Touch trace/recall miss do not prove MLKit recognition or correct human recall. Fresh5580/5581 ownership check mandatory before later native launch;040 exception not inherited. Accepted404 freshAndroid3+1 retained; original403 permission denial and049 host-only heap qualification unchanged. Original initial reviews and lookup/read-depth/citation qualifications preserved. No native/reviewer/runtime publication/065/second runner. Published90/1228,1138remain; compatibleAndroidf9b59a2+ required; phone/generalrelease/whole-set outstanding.",
}
(CONTROL / "batch-064-native-fixture-verification.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: record[key] for key in ("status", "contentVersion", "expectedCounts",
                 "archiveSha256", "zipEntries", "compressedBytes", "inflatedBytes",
                 "retainedBytes", "verifiedRuntimeHashes", "fixtureSha256", "captureSteps")}, indent=2))
print("Article selectors:", len(selectors), "Directed transitions:", len(transitions))
