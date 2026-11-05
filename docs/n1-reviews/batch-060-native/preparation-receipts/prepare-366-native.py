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
HEAD = "99d8ace026aaf5cf76b4adada34b14e969d10d4e"
REVIEWED = "ea1dac1a6fd2c452db9cf602442e1f287ff95c67"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-060-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-059-native" / "N1Batch059NativeTest.kt"
FIXTURE = FOLDER / "N1Batch060NativeTest.kt"


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
assert progress["checkpoint"] == 365 and progress["execution366StartingState"]["execution"] == 366
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1072, "words": 5031, "n1": 92}, counts
assert manifest["contentVersion"] == "dbf047f0c2e6cd56"
initial_reports = {
    f"docs/n1-reviews/batch-060-initial-{family}.md":
        sha(ROOT / "docs" / "n1-reviews" / f"batch-060-initial-{family}.md")
    for family in ("claude", "gpt")
}
prior_hash = sha(PRIOR)
text = PRIOR.read_text(encoding="utf-8")
for old, new in (
    ("059", "060"),
    ("benefitsLookalikesAndTwoFallbackRadicalsAcrossFourProductionFamilies",
     "pavilionLookalikesAndThreeFallbackComponentsAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineBenefitsTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
     "fullSingleImportOfflinePavilionTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
    ("911431dad205cf031e1df9f561a47748c060439b", HEAD),
    ("911431da", HEAD[:8]), ("1f1ad78479e9c1f4", manifest["contentVersion"]),
    ("1071", "1072"), ("5030", "5031"), ("91, n1.size", "92, n1.size"),
    ("N1 · 91 cards", "N1 · 92 cards"),
    ('"享 京 厚 高 亠 厂 子 口 受 享受"', '"亭 停 京 享 高 亠 亻 冖 丁 小 子 口 料 料亭"'),
    ('listOf("享", "京", "厚", "高", "亠", "厂", "子", "口", "受")',
     'listOf("亭", "停", "京", "享", "高", "亠", "亻", "冖", "丁", "小", "子", "口", "料")'),
    ('listOf("享受")', 'listOf("料亭")'),
    ("Batch 060: benefits / look-alikes / fallback radicals",
     "Batch 060: pavilion / look-alikes / fallback components"),
    ("Compare 享 with 京, 厚 and 高. Inspect actual 亠 and 厂 fallback glyphs, 子 versus 小-shaped bases and both 享受 components. Shared fallback need not give four different designs.",
     "Compare 亭 with 停, 京, 享 and 高. Inspect actual 亠, 亻 and 冖 fallback glyphs, 丁 versus 小 and 子 bases, and both 料亭 components. Shared fallback need not give four different designs."),
    ("assertEquals(40, rows.length())", "assertEquals(56, rows.length())"),
    ('.put("individualGlyphProbes", 36).put("wholeWordRasterProbes", 4)',
     '.put("individualGlyphProbes", 52).put("wholeWordRasterProbes", 4)'),
    ("Thirty-six single-character native Paint probes including actual 亠 and 厂, four complete-word nonblank raster probes and four production Compose rows; actual 享/京/厚/高/亠/厂/子/口/受/享受 readability requires separate visual inspection.",
     "Fifty-two single-character native Paint probes including actual 亠, 亻 and 冖, four complete-word nonblank raster probes and four production Compose rows; actual 亭/停/京/享/高/亠/亻/冖/丁/小/子/口/料/料亭 readability requires separate visual inspection."),
    ("val benefits", "val pavilion"), ("benefits.", "pavilion."),
    ('it.kanji == "享"', 'it.kanji == "亭"'),
    ('card.kanji == "享"', 'card.kanji == "亭"'),
    ('"jlpt-n1", "享",', '"jlpt-n1", "亭",'),
    ('performTextReplacement("享")', 'performTextReplacement("亭")'),
    ('assertEquals("享",', 'assertEquals("亭",'),
    ('kanjiCard(source.id, "享")', 'kanjiCard(source.id, "亭")'),
    ('log.kanji == "享"', 'log.kanji == "亭"'),
    ("enjoy; receive benefits", "pavilion; restaurant building"),
    ('listOf("キョウ", "コウ")', 'listOf("テイ", "チン")'),
    ('listOf("う.ける")', 'emptyList<String>()'),
    ('listOf("キョウ")', 'listOf("テイ")'),
    ('"きょう"', '"てい"'),
    ('setOf("こう", "うける")', 'setOf("ちん")'),
    ("享 meaning and sole curated on key due", "亭 meaning and sole curated on key due"),
    ("Two historical good 享 meaning logs", "Two historical good 亭 meaning logs"),
    ("assertEquals(8, strokes.length())", "assertEquals(9, strokes.length())"),
    ("8 strokes drawn", "9 strokes drawn"),
):
    assert old in text, old
    text = text.replace(old, new)
start = text.index('            await("no. 8)"')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = '''            await("no. 8)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("亭 can refer to a pavilion", "kanji-meaning")
            show("Modern-shape mnemonic, not etymology", "kanji-mnemonic")
            section("Readings")
            show(readingExample("料亭 りょうてい - traditional Japanese restaurant, especially an upscale one"), "kanji-on-reading")
            show(readingExample("亭 ちん - a small pavilion for viewing or resting, for example in a garden; recognition example"), "kanji-recognition-on")
            show("Practice selects テイ.", "kanji-curation")
            show("Those suffix senses use てい", "kanji-suffix-boundary")
            section("Notes")
            show(articleBullet("停, \\"halt; stopping,\\" adds the person-shaped 亻 on the left of 亭. A restaurant or pavilion is not the stopping action."), "kanji-person-lookalike")
            show(articleBullet("京, \\"capital,\\" ends in 小, and 享, \\"enjoy; receive benefits,\\" ends in 子. 亭 instead has the covered 丁-shaped lower part."), "kanji-lower-lookalikes")
            show(articleBullet("料亭 is not the lodging word 旅館 りょかん. Nor does every restaurant use 亭 in its name."), "kanji-lodging-boundary")
            section("Common words")
            inline(await(articleBullet("料亭 りょうてい - traditional Japanese restaurant, especially an upscale one")), "料亭")
            await("料亭 (りょうてい) — traditional Japanese restaurant")
            section("Meaning")
            show("料亭 is a traditional Japanese restaurant", "word-meaning-qualification")
            show(articleBullet("昨夜、料亭で食事をしました。（さくや、りょうていで しょくじを しました。）— Last night, I had a meal at a traditional Japanese restaurant."), "word-meal-example")
            show(articleBullet("この料亭の料理はおいしいです。（この りょうていの りょうりは おいしいです。）— The food at this traditional Japanese restaurant is delicious."), "word-food-example")
            show("Use で for eating there", "word-place-particle")
            section("How the kanji combine")
            show("Read it as a modifier-plus-place compound", "word-components-readings")
            inline(await("Read it as a modifier-plus-place compound", substring = true), "亭")
            await("Article contents")
            section("Readings")
            show("Practice selects テイ.", "word-backlink-pavilion")
            back()
            await("Read it as a modifier-plus-place compound", substring = true).assertIsDisplayed()
            capture("system-back-word-pavilion")
            inline(await("Read it as a modifier-plus-place compound", substring = true), "料")
            await("Article contents")
            section("Common words")
            show(articleBullet("料亭 りょうてい — traditional Japanese restaurant, especially an upscale one"), "materials-forwardlink")
            inline(await(articleBullet("料亭 りょうてい — traditional Japanese restaurant, especially an upscale one")), "料亭")
            await("料亭 (りょうてい) — traditional Japanese restaurant")
            section("Distinctive meaning")
            show("not as the general word for Japanese food", "materials-forwardlink-word")
            back()
            await("Common words")
            capture("system-back-materials")
            back()
            await("Read it as a modifier-plus-place compound", substring = true).assertIsDisplayed()
            capture("system-back-word-materials")
            section("Synonyms and antonyms")
            show(articleBullet("レストラン is a broader restaurant word, especially associated with Western-style dining; the actual cuisine and naming vary."), "word-broader-restaurant")
            show(articleBullet("食堂 しょくどう can mean a dining hall or cafeteria, or an ordinary eatery. That is a different emphasis from 料亭, not a rule that their possible referents can never overlap."), "word-eatery-overlap")
            show(articleBullet("旅館 りょかん names a traditional Japanese inn: overnight lodging rather than the restaurant category. An inn may serve meals without making the two words synonyms."), "word-inn-boundary")
            show(articleBullet("There is no direct antonym."), "word-antonym-boundary")
            section("Distinctive meaning")
            show("not as the general word for Japanese food", "word-facilities-boundary")
            show("The different spelling 涼亭", "word-homophone")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
assert not any(old in text for old in ("059", "享受", "受ける", "キョウ", "コウ", "うける", "benefits.", "911431da", "きょう"))
glyph_list = re.search(r'for \(char in listOf\((.*?)\)\)', text).group(1)
glyphs = re.findall(r'"([^"]+)"', glyph_list)
assert glyphs == ["亭", "停", "京", "享", "高", "亠", "亻", "冖", "丁", "小", "子", "口", "料"]
assert len(glyphs) == len(set(glyphs)) == 13
documents = {name: blocks(ROOT / name) for name in ("kanji/亭.md", "words/料亭.md", "kanji/料.md")}
stack, selectors, controls, transitions = ["kanji/亭.md"], [], [], []
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
assert stack == ["kanji/亭.md"]
assert len(transitions) == len(set(tuple(pair) for pair in transitions)) == 4
accepted = json.loads((ROOT / "docs" / "n1-sources" / "execution-365.json").read_text(encoding="utf-8"))
for item in accepted["archivedArtifacts"]:
    assert sha(ROOT / item["path"]) == item["sha256"]
for test in accepted["recovery"]["tests"]:
    assert test["failures"] == test["errors"] == test["skipped"] == 0
archive = CONTROL / "artifacts" / "n1-batch-060-99d8ace0-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-060/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-060/"
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
diff_path = FOLDER / "fixture-from-059.diff"
diff_path.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)),
    encoding="utf-8")
assert sha(PRIOR) == prior_hash
for name, expected in initial_reports.items():
    assert sha(ROOT / name) == expected
record = {
    "schemaVersion": 1, "execution": 366, "batch": "060",
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
    "plannedNativePaintProbes": 52, "plannedWholeWordRasterProbes": 4,
    "plannedGlyphs": ["亭", "停", "京", "享", "高", "亠", "亻", "冖", "丁", "小", "子", "口", "料"],
    "plannedWholeWords": ["料亭"],
    "fullReadings": {"on": ["テイ", "チン"], "kun": []},
    "curatedReadings": {"on": ["テイ"], "kun": []},
    "normalizedQuizKeys": {"on": ["てい"], "kun": []},
    "reciprocalPairs": [["亭", "料亭"], ["料", "料亭"]],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted365AndroidRetainedWithoutRerun": True,
    "nativeExecuted": False, "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "limits": "Static fixture/archive preparation, not native execution, readability, independent visual, phone or publication acceptance. Article selectors use a bounded Markdown projection, not a native semantics tree. Exact full Git envelope; production ContentSync called ONCE with unchanged guards. Both reciprocal pairs include reused料. Actual亠/亻/冖 fallback remains pending until native execution and direct visual inspection. Raster hashes do not identify fallback faces or certify readability. Touch-reference trace and recall miss do not prove MLKit recognition or correct human recall. Accepted365 Android3+1 retained; original364 permission denial/049 host-only heap qualification unchanged. Original Claude060-P1/P2 process noncompliance remains historical; dependent lexical remediation is not retroactive strict initial acceptance. Fresh5580/5581 ownership check mandatory before later launch;040 exception not inherited. No emulator/reviewer/publication/061/second runner. Published86/1228,1142remain; compatibleAndroidf9b59a2+ required; phone/generalrelease/whole-set outstanding.",
}
save(CONTROL / "batch-060-native-fixture-verification.json", record)
print(json.dumps({key: record[key] for key in
                  ("status", "contentVersion", "expectedCounts", "archiveSha256", "zipEntries",
                   "compressedBytes", "inflatedBytes", "retainedBytes", "verifiedRuntimeHashes",
                   "fixtureSha256", "captureSteps")}, indent=2))
print("Unique article selectors:", len(selectors), "Directed reciprocal transitions:", len(transitions))
