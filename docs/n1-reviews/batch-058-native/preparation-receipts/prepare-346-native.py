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
HEAD = "00491dddddaa65467b0f7ad474689e054a00f5f4"
REVIEWED = "58b53fd31b6d55baba32c049fba62ac739feb004"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-058-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-057-native" / "N1Batch057NativeTest.kt"
FIXTURE = FOLDER / "N1Batch058NativeTest.kt"


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
            result.append(("bullet", plain(line[2:])))
        elif result and result[-1][0] == "bullet" and line.startswith("  "):
            result[-1] = ("bullet", result[-1][1] + " " + plain(line.strip()))
        else:
            paragraph.append(line.strip())
    return result


assert git("rev-parse", "HEAD").decode().strip() == HEAD
assert git("log", "-1", "--format=%G?").decode().strip() == "G"
assert not git("status", "--porcelain")
assert not git("status", "--porcelain", cwd=ANDROID)
assert git("rev-parse", "HEAD", cwd=ANDROID).decode().strip() == APP_HEAD
assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
progress = json.loads((CONTROL / "progress.json").read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == 345 and progress["execution346StartingState"]["execution"] == 346
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1070, "words": 5029, "n1": 90}
prior_hash = sha(PRIOR)
initial_reports = {
    f"docs/n1-reviews/batch-058-initial-{family}.md":
        sha(ROOT / "docs" / "n1-reviews" / f"batch-058-initial-{family}.md")
    for family in ("claude", "gpt")
}
text = PRIOR.read_text(encoding="utf-8")
for old, new in (
    ("057", "058"),
    ("planningLookalikesAndSupportWordsAcrossFourProductionFamilies",
     "hillLookalikesRadicalAndSupportWordsAcrossFourProductionFamilies"),
    ("fullSingleImportOfflinePlanningArticlesMeaningBothCuratedReadingsDrawingAndSystemBack",
     "fullSingleImportOfflineHillThreeReciprocalPairsBothCuratedReadingsDrawingAndSystemBack"),
    ("d9712bf9a2c03f3fae51c2f751481a05affbc0f9", HEAD),
    ("d9712bf9", HEAD[:8]), ("47f11f7f539a1d55", manifest["contentVersion"]),
    ("1069", "1070"), ("5028", "5029"), ("89, n1.size", "90, n1.size"),
    ("N1 · 89 cards", "N1 · 90 cards"), ("planning", "hill"),
    ('"企 全 危 休 人 止 業 企業 企てる"', '"丘 兵 近 共 一 砂 山 丘 砂丘"'),
    ('listOf("企", "全", "危", "休", "人", "止", "業")',
     'listOf("丘", "兵", "近", "共", "一", "砂", "山")'),
    ('listOf("企業", "企てる")', 'listOf("丘", "砂丘")'),
    ("Batch 058: hill / look-alikes / support", "Batch 058: hill / look-alikes / radical / support"),
    ("Compare 企 with 全, 危 and 休; inspect radical 人, lower 止 and both support words. Shared fallback need not give four different designs.",
     "Compare 丘 with 兵, 近 and 共; inspect radical 一, both components of 砂丘 and contextual 山. Shared fallback need not give four different designs."),
    ("actual 企/全/危/休/人/止/業/企業/企てる readability",
     "actual 丘/兵/近/共/一/砂/山/丘/砂丘 readability"),
    ('"企"', '"丘"'), ("plan; undertake", "hill; knoll"),
    ('listOf("キ")', 'listOf("キュウ")'),
    ('listOf("くわだ.てる", "たくら.む")', 'listOf("おか")'),
    ('listOf("くわだ.てる")', 'listOf("おか")'),
    ('"き"', '"きゅう"'), ('"くわだてる"', '"おか"'),
    ("企 meaning and both curated keys due. Two historical good 企 meaning logs",
     "丘 meaning and both curated keys due. Two historical good 丘 meaning logs"),
    ("assertEquals(6, strokes.length())", "assertEquals(5, strokes.length())"),
    ("6 strokes drawn", "5 strokes drawn"),
):
    assert old in text, old
    text = text.replace(old, new)
old = '                assertFalse(question.question.options.any { it.key == "たくらむ" })'
assert old in text
text = text.replace(old, '                assertEquals(1, question.question.options.count { it.key == key })')
start = text.index('            await("no. 9)"')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = '''            await("no. 1)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("丘 means a hill or knoll", "kanji-meaning")
            show("Modern-shape mnemonic", "kanji-mnemonic")
            section("Readings")
            show(readingExample("砂丘 さきゅう - sand dune"), "kanji-on-reading")
            show(readingExample("丘 おか - hill; rising ground"), "kanji-kun-reading")
            show("Both sourced readings", "kanji-curation")
            section("Notes")
            show(articleBullet("山 means mountain and can also describe a hill in context. 坂 focuses on a slope or inclined road; it can be part of a hill."), "kanji-landform-boundaries")
            show("岡 is another dictionary spelling", "kanji-spelling-names")
            show("Distinguish the five-stroke", "kanji-lookalike")
            section("Common words")
            inline(await(articleBullet("丘 おか - hill; rising ground")), "丘")
            await("丘 (おか)", substring = true)
            section("Meaning")
            show("丘 is a hill or raised area", "hill-word-meaning")
            show(articleBullet("丘の上に小さな家があります。 (おかのうえにちいさないえがあります。) - There is a small house on the hill."), "hill-house-example")
            show(articleBullet("あの丘に登ると、海が見えます。 (あのおかにのぼると、うみがみえます。) - If you climb that hill, you can see the sea."), "hill-climb-example")
            show("The first example locates", "hill-example-roles")
            section("How the kanji combine")
            show("represents the whole native noun", "hill-native-component")
            inline(await("represents the whole native noun", substring = true), "丘")
            await("Article contents")
            section("Meaning and origin")
            show("Modern-shape mnemonic", "hill-backlink-kanji")
            back()
            await("represents the whole native noun", substring = true).assertIsDisplayed()
            capture("system-back-hill")
            section("Synonyms and antonyms")
            show("universal numerical height boundary", "hill-comparisons")
            section("Distinctive meaning")
            show("not height as an abstract measurement", "hill-height-boundary")
            back()
            await("Common words")
            inline(await(articleBullet("砂丘 さきゅう - sand dune")), "砂丘")
            await("砂丘 (さきゅう) - sand dune")
            section("Meaning")
            show("a raised accumulation of sand formed by wind", "dune-meaning")
            show(articleBullet("砂丘を歩きました。 (さきゅうをあるきました。) - We walked across the sand dunes."), "dune-walk-example")
            show(articleBullet("砂丘の上から海が見えます。 (さきゅうのうえからうみがみえます。) - You can see the sea from the top of the dune."), "dune-view-example")
            show("を marks the area traversed", "dune-particles-number")
            section("How the kanji combine")
            show("modifier-plus-head combination", "dune-components-readings")
            inline(await("modifier-plus-head combination", substring = true), "丘")
            await("Article contents")
            section("Readings")
            show("Both sourced readings", "dune-backlink-hill")
            back()
            await("modifier-plus-head combination", substring = true).assertIsDisplayed()
            capture("system-back-dune-hill")
            inline(await("modifier-plus-head combination", substring = true), "砂")
            await("Article contents")
            section("Meaning and origin")
            show("砂 names sand", "dune-backlink-sand")
            section("Common words")
            inline(await(articleBullet("砂丘 さきゅう - sand dune")), "砂丘")
            await("砂丘 (さきゅう) - sand dune")
            section("Distinctive meaning")
            show("not any patch or grain of sand", "sand-forwardlink-dune")
            back()
            await("Common words")
            capture("system-back-sand")
            back()
            await("modifier-plus-head combination", substring = true).assertIsDisplayed()
            capture("system-back-dune-sand")
            show("JMdict also lists しゃきゅう", "dune-alternatives")
            section("Synonyms and antonyms")
            show("not exact synonyms or a set of antonyms", "dune-geography-boundaries")
            section("Distinctive meaning")
            show("not any patch or grain of sand", "dune-material-boundary")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
assert not any(old in text for old in ("057", "企", "くわだ", "たくら", "planning", "d9712bf9"))
documents = {name: blocks(ROOT / name) for name in
             ("kanji/丘.md", "words/丘.md", "words/砂丘.md", "kanji/砂.md")}
stack, selectors, controls, transitions = ["kanji/丘.md"], [], [], []
for number, line in enumerate(route.splitlines(), 1):
    document = stack[-1]
    shown = re.search(r'show\((?:(readingExample|articleBullet)\()?"([^"]+)"\)?, "([^"]+)"\)', line)
    section = re.search(r'section\("([^"]+)"\)', line)
    awaited = re.search(r'await\((?:(readingExample|articleBullet)\()?"([^"]+)"(?:, substring = (true|false))?', line)
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
assert stack == ["kanji/丘.md"]
assert len(transitions) == 6 and len(set(tuple(pair) for pair in transitions)) == 6
android = progress["batch058AndroidCheckpoint"]
assert android["execution"] == 345
for item in android["archivedArtifacts"]:
    assert sha(ROOT / item["path"]) == item["sha256"]
for test in android["freshParentRecovery"]["tests"]:
    assert test["failures"] == test["errors"] == test["skipped"] == 0
archive = CONTROL / "artifacts" / "n1-batch-058-00491ddd-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-058/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-058/"
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
FIXTURE.write_text(text, encoding="utf-8")
diff_path = FOLDER / "fixture-from-057.diff"
diff_path.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)),
    encoding="utf-8")
assert sha(PRIOR) == prior_hash
for name, expected in initial_reports.items():
    assert sha(ROOT / name) == expected
record = {
    "schemaVersion": 1, "execution": 346, "batch": "058",
    "status": "static-native-preparation-verified-not-executed",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
    "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED, "androidSnapshot": APP_HEAD,
    "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
    "archive": str(archive), "archiveSha256": sha(archive), "zipEntries": len(names),
    "compressedBytes": archive.stat().st_size, "inflatedBytes": inflated,
    "retainedBytes": retained, "verifiedRuntimeHashes": verified, "manifestEqual": True,
    "safePathsPerFileAndOriginalPublishingBudgetsPassed": True,
    "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
    "reusedAcceptedHarness": str(PRIOR.relative_to(ROOT)),
    "reusedAcceptedHarnessSha256": prior_hash,
    "fixtureDiff": str(diff_path.relative_to(ROOT)), "fixtureDiffSha256": sha(diff_path),
    "originalInitialReportHashesUnchanged": initial_reports,
    "articleFiles": [{"path": name, "sha256": sha(ROOT / name),
                      "projectedTextBlocks": len(items)} for name, items in documents.items()],
    "staticMarkdownSelectors": selectors, "renderedNavigationControls": controls,
    "articleRouteTransitions": transitions,
    "captureSteps": len(re.findall(r'(?:show\([^\n]+, |capture\()"([^"]+)"\)', route)),
    "plannedNativePaintProbes": 28, "plannedWholeWordRasterProbes": 8,
    "plannedGlyphs": ["丘", "兵", "近", "共", "一", "砂", "山"],
    "plannedWholeWords": ["丘", "砂丘"],
    "fullReadings": {"on": ["キュウ"], "kun": ["おか"]},
    "curatedReadings": {"on": ["キュウ"], "kun": ["おか"]},
    "normalizedQuizKeys": {"on": ["きゅう"], "kun": ["おか"]},
    "reciprocalPairs": [["丘", "丘"], ["丘", "砂丘"], ["砂", "砂丘"]],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted345AndroidRetainedWithoutRerun": True,
    "nativeExecuted": False, "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "limits": "Static fixture/archive preparation, not native execution, visibility, readability, independent visual, phone or publication acceptance. Every article-route selector resolves to one block in the bounded static Markdown projection, not a native semantics tree. Entire Git export envelope retained; production ContentSync called ONCE, no duplicate parse/reduced archive, production/font/guest-app-heap/archive-guard changes. All three reciprocal pairs include reused砂. Raster hashes do not identify fallback faces or certify readability. Touch-reference trace and recall miss do not prove MLKit recognition or correct human recall. Accepted345 Android3+1 retained; original344 permission denial and049 host-only heap qualification unchanged. InitialClaude3 overlaps/noncompliance and bounded remediation are not retroactive strict acceptance. Fresh5580/5581 ownership check mandatory before later launch;040 exception not inherited. No emulator/reviewer/publication/059/second runner. Published84/1228,1144remain; compatibleAndroidf9b59a2+ required; phone/generalrelease/whole-set outstanding.",
}
save(CONTROL / "batch-058-native-fixture-verification.json", record)
print(json.dumps({key: record[key] for key in
                  ("status", "contentVersion", "expectedCounts", "archiveSha256", "zipEntries",
                   "compressedBytes", "inflatedBytes", "retainedBytes", "verifiedRuntimeHashes",
                   "fixtureSha256", "captureSteps")}, ensure_ascii=False, indent=2))
print("Unique article selectors:", len(selectors), "Directed reciprocal transitions:", len(transitions))
