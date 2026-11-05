import difflib
import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
HEAD = "53ecd11711804be900ca95f9f1018942910aecec"
REVIEWED = "ddad655f71c06e7cb2c749de18596863a800a73d"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-063-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-062-native" / "N1Batch062NativeTest.kt"


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
assert progress["checkpoint"] == 394 and progress["execution395StartingState"]["execution"] == 395
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1075, "words": 5033, "n1": 95}, counts
assert manifest["contentVersion"] == "c19b742b7e6320a7"
reports = {f"docs/n1-reviews/batch-063-initial-{family}.md":
           sha(ROOT / "docs" / "n1-reviews" / f"batch-063-initial-{family}.md")
           for family in ("claude", "gpt")}
text = PRIOR.read_text(encoding="utf-8")
for old, new in (
    ("062", "063"), ("salaryLookalikesAndPersonFallbackAcrossFourProductionFamilies",
                    "imitationLookalikesAndPersonFallbackAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineSalaryTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
     "fullSingleImportOfflineImitationTwoReciprocalPairsBothReadingsDrawingAndSystemBack"),
    ("e157d58c5bdb9fc2d58d7043fdf0429d36f5c040", HEAD),
    ("e157d58c", HEAD[:8]), ("545c56b5d4b4e8ef", manifest["contentVersion"]),
    ("1074", "1075"), ("5032", "5033"), ("94, n1.size", "95, n1.size"),
    ("N1 · 94 cards", "N1 · 95 cards"),
    ('"俸 棒 奉 借 付 人 亻 木 給 糸 合 俸給"', '"倣 放 方 付 人 亻 模 木 傚 習 攵 模倣 倣う"'),
    ('listOf("俸", "棒", "奉", "借", "付", "人", "亻", "木", "給", "糸", "合")',
     'listOf("倣", "放", "方", "付", "人", "亻", "模", "木", "傚", "習", "攵")'),
    ('listOf("俸給")', 'listOf("模倣", "倣う")'),
    ("Batch 063: salary / look-alikes / person fallback",
     "Batch 063: imitation / look-alikes / person fallback"),
    ("Compare 俸 with 棒, 奉, 借 and 付. Inspect actual 人 versus 亻, 木 versus 亻, 給 with 糸 and 合, and both characters in 俸給. Shared fallback need not give four different designs.",
     "Compare 倣 with 放, 方 and 付. Inspect 人 versus 亻, 模 with 木, reused rare 傚 and 習, and both words 模倣 and 倣う. Shared fallback need not give four different designs."),
    ("assertEquals(48, rows.length())", "assertEquals(52, rows.length())"),
    ('.put("individualGlyphProbes", 44).put("wholeWordRasterProbes", 4)',
     '.put("individualGlyphProbes", 44).put("wholeWordRasterProbes", 8)'),
    ("Forty-four single-character native Paint probes including actual 人 and 亻, four complete-word nonblank raster probes and four production Compose rows; actual 俸/棒/奉/借/付/人/亻/木/給/糸/合/俸給 readability requires separate visual inspection.",
     "Forty-four single-character native Paint probes including actual 人 and 亻, eight complete-word nonblank raster probes and four production Compose rows; actual 倣/放/方/付/人/亻/模/木/傚/習/攵/模倣/倣う readability requires separate visual inspection."),
    ("salary; stipend", "imitate; emulate"), ("salary", "imitation"), ('"俸"', '"倣"'),
):
    assert old in text, old
    text = text.replace(old, new)
for owner in ("imitation", "card"):
    for field in ("kunyomi.splitSep()", "quizKunyomi?.splitSep()"):
        old = f"assertEquals(emptyList<String>(), {owner}.{field})"
        assert old in text, old
        text = text.replace(old, f'assertEquals(listOf("なら.う"), {owner}.{field})')
text = text.replace(
    "assertEquals(emptyList<String>(), imitation.toReadingCard().quizKeys(ReadingKind.Kun))",
    'assertEquals(listOf("ならう"), imitation.toReadingCard().quizKeys(ReadingKind.Kun))')
text = text.replace('(kind == ReadingKind.On && key == "ほう")',
                    '((kind == ReadingKind.On && key == "ほう") || (kind == ReadingKind.Kun && key == "ならう"))')
text = text.replace("俸 meaning and sole curated on key due; explicit no-kun. Two historical good 俸 meaning logs",
                    "倣 meaning and both curated on/kun keys due. Two historical good 倣 meaning logs")
text = text.replace("repeat(1) {", "repeat(2) {")
text = text.replace('                assertEquals(ReadingKind.On, question.question.kind)\n                val key = "ほう"',
                    '                val key = if (question.question.kind == ReadingKind.On) "ほう" else "ならう"')
old = '''            assertEquals(setOf(ReadingKind.On), answeredKinds)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "倣" && it.mode == ReadingKind.Kun.mode.name }
            })'''
assert old in text
text = text.replace(old, "            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)")
text = text.replace("soleCuratedOnQuestionAndPersistedGradeNoKun", "bothCuratedReadingsAndPersistedGoodGrades")
start = text.index('            await("no. 9)"')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = '''            await("no. 9)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("倣 concerns imitating or following an existing model.", "kanji-meaning")
            show("The model need not be a teacher giving lessons.", "kanji-model-boundary")
            show("Modern-shape mnemonic:", "kanji-mnemonic")
            show("or a claim that 放's", "kanji-origin-boundary")
            section("Readings")
            show(readingExample("模倣 もほう — imitation; copying"), "kanji-on-reading")
            show(readingExample("倣う ならう — imitate; follow an example"), "kanji-kun-reading")
            show("In 倣う, 倣 writes なら and う is okurigana.", "kanji-kana-boundary")
            section("Notes")
            show(articleBullet("倣う marks the model with に: 前例に倣う, \\"follow a precedent.\\" 習う, also ならう, concerns learning under instruction: 先生にピアノを習う (せんせいにピアノをならう), \\"take piano lessons from a teacher.\\" The skill takes を; the shared sound does not make these words interchangeable."), "kanji-particle-contrast")
            show(articleBullet("放, \\"release,\\" lacks the left-hand 亻. 方, \\"direction, method,\\" is only part of 放, not the whole right side of 倣."), "kanji-lookalikes")
            show(articleBullet("付, \\"attach,\\" shares 亻 but has a different right side. Keep the entire shape in view rather than identifying a kanji by its radical alone."), "kanji-radical-boundary")
            section("Common words")
            show(articleBullet("前例に倣う ぜんれいにならう — follow a precedent"), "kanji-precedent")
            inline(await(articleBullet("模倣 もほう — imitation; copying")), "模倣")
            await("模倣 (もほう) - imitation; copying")
            section("Meaning")
            show("模倣する is a transitive verb: the model being imitated takes を.", "imitation-transitivity")
            show(articleBullet("子供は大人の話し方を模倣します。 (こどもはおとなのはなしかたをもほうします。) - Children imitate adults' ways of speaking."), "imitation-speech-example")
            show(articleBullet("この絵は、有名な作品を模倣したものです。 (このえは、ゆうめいなさくひんをもほうしたものです。) - This picture is an imitation of a famous work."), "imitation-work-example")
            show("Forms include 模倣します, 模倣しない and 模倣して.", "imitation-forms")
            section("How the kanji combine")
            show("The on readings here are モ + ホウ: もほう.", "imitation-components")
            inline(await("模 contributes modeling or copying, and 倣 imitation.", substring = true), "倣")
            await("Article contents")
            section("Readings")
            show(readingExample("模倣 もほう — imitation; copying"), "imitation-backlink")
            back()
            await("The on readings here are モ + ホウ: もほう.", substring = true).assertIsDisplayed()
            capture("system-back-imitation")
            section("Synonyms and antonyms")
            show("do not transfer that construction to 模倣する.", "imitation-particle-contrast")
            show("copying a sheet or file is not necessarily", "imitation-copy-boundary")
            section("Distinctive meaning")
            show("Two people can look alike without either copying the other.", "imitation-resemblance")
            show("do not translate every occurrence as fraud or plagiarism.", "imitation-judgment")
            back()
            await("Common words")
            inline(await(articleBullet("倣う ならう — follow a model or precedent")), "倣う")
            await("倣う (ならう) - imitate; follow an example")
            section("Meaning")
            show("Use に for the model:", "follow-model-particle")
            show(articleBullet("先輩のやり方に倣いました。 (せんぱいのやりかたにならいました。) - I followed my senior colleague's way of doing it."), "follow-colleague-example")
            show(articleBullet("前例に倣って、この方法を使います。 (ぜんれいにならって、このほうほうをつかいます。) - Following the precedent, we will use this method."), "follow-precedent-example")
            show("Its forms include 倣います, 倣わない, 倣って and 倣った.", "follow-godan-forms")
            show("does not justify mechanically using を.", "follow-transitivity-boundary")
            section("How the kanji combine")
            show("傚う and 慣らう are marked rare spellings", "follow-spelling-boundary")
            inline(await("writes なら, followed by う.", substring = true), "倣")
            await("Article contents")
            section("Readings")
            show(readingExample("倣う ならう — imitate; follow an example"), "follow-backlink")
            back()
            await("writes なら, followed by う.", substring = true).assertIsDisplayed()
            capture("system-back-follow")
            section("Synonyms and antonyms")
            show("倣う specifically brings a model or example into view.", "follow-synonyms")
            section("Distinctive meaning")
            show("習う, also ならう, means learning under instruction.", "follow-learning-contrast")
            show("does not make the two written identities interchangeable.", "follow-identity-boundary")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for obsolete in ("062", "俸", "俸給", "salary", "soleCurated", "e157d58c", "1074", "5032"):
    assert obsolete not in text, obsolete
assert text.count('assertEquals(listOf("なら.う"),') == 4
assert text.count("repeat(2)") == 1
documents = {name: blocks(ROOT / name) for name in ("kanji/倣.md", "words/模倣.md", "words/倣う.md")}
stack, selectors, controls, transitions = ["kanji/倣.md"], [], [], []
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
        destination = f"words/{label}.md" if document.startswith("kanji/") else f"kanji/{label}.md"
        assert f"../{destination}" in (ROOT / document).read_text(encoding="utf-8")
        transitions.append([document, destination])
        stack.append(destination)
assert stack == ["kanji/倣.md"]
assert len(transitions) == len(set(tuple(pair) for pair in transitions)) == 4
accepted = json.loads((ROOT / "docs" / "n1-sources" / "execution-394.json").read_text(encoding="utf-8"))
for item in accepted["archivedArtifacts"]:
    assert sha(ROOT / item["path"]) == item["sha256"]
for test in accepted["recovery"]["tests"]:
    assert test["failures"] == test["errors"] == test["skipped"] == 0
archive = CONTROL / "artifacts" / "n1-batch-063-53ecd117-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-063/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-063/"
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
fixture = FOLDER / "N1Batch063NativeTest.kt"
fixture.write_text(text, encoding="utf-8")
diff = FOLDER / "fixture-from-062.diff"
diff.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=fixture.relative_to(ROOT).as_posix(), n=0)), encoding="utf-8")
for name, expected in reports.items():
    assert sha(ROOT / name) == expected
record = {
    "schemaVersion": 1, "execution": 395, "batch": "063",
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
    "plannedNativePaintProbes": 44, "plannedWholeWordRasterProbes": 8,
    "plannedGlyphs": ["倣", "放", "方", "付", "人", "亻", "模", "木", "傚", "習", "攵"],
    "plannedWholeWords": ["模倣", "倣う"],
    "fullReadings": {"on": ["ホウ"], "kun": ["なら.う"]},
    "curatedReadings": {"on": ["ホウ"], "kun": ["なら.う"]},
    "normalizedQuizKeys": {"on": ["ほう"], "kun": ["ならう"]},
    "reciprocalPairs": [["倣", "模倣"], ["倣", "倣う"]],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted394AndroidRetainedWithoutRerun": True, "nativeExecuted": False,
    "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "projectionQualification": "Bounded heading/paragraph/bullet/table projection inspected against current production core/markdown/Markdown.kt; these three articles use its supported subset. Static selectors are not a native semantics tree or readability acceptance.",
    "limits": "Preparation only. Exact full Git envelope; production ContentSync called ONCE with unchanged guards. Both reciprocal pairs in four directions, both curated reading kinds, ten touch-reference strokes/ungraded trace and recall miss are planned, not executed. Paint hashes do not identify fallback faces or certify readability. Touch trace/recall miss do not prove MLKit recognition or correct human recall. Fresh5580/5581 ownership check mandatory before later native launch;040 exception not inherited. Accepted394 Android3+1 retained; original393 permission denial and049 host-only heap qualification unchanged. Original Claude063-P1 overlapping views remain noncompliant; dependent lexical remediation is not retroactive strict initial-process acceptance. No native/reviewer/publication/064/second runner. Published89/1228,1139remain; compatibleAndroidf9b59a2+ required; phone/generalrelease/whole-set outstanding.",
}
(CONTROL / "batch-063-native-fixture-verification.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: record[key] for key in ("status", "contentVersion", "expectedCounts",
                 "archiveSha256", "zipEntries", "compressedBytes", "inflatedBytes",
                 "retainedBytes", "verifiedRuntimeHashes", "fixtureSha256", "captureSteps")}, indent=2))
print("Article selectors:", len(selectors), "Directed transitions:", len(transitions))
