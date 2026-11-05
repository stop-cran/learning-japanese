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
HEAD = "911431dad205cf031e1df9f561a47748c060439b"
REVIEWED = "769293c824dc41abb9386e76c4dd5f8c676e48e0"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-059-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-058-native" / "N1Batch058NativeTest.kt"
FIXTURE = FOLDER / "N1Batch059NativeTest.kt"


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
assert progress["checkpoint"] == 355 and progress["execution356StartingState"]["execution"] == 356
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1071, "words": 5030, "n1": 91}
assert manifest["contentVersion"] == "1f1ad78479e9c1f4"
initial_reports = {
    f"docs/n1-reviews/batch-059-initial-{family}.md":
        sha(ROOT / "docs" / "n1-reviews" / f"batch-059-initial-{family}.md")
    for family in ("claude", "gpt")
}
prior_hash = sha(PRIOR)
text = PRIOR.read_text(encoding="utf-8")
for old, new in (
    ("058", "059"),
    ("hillLookalikesRadicalAndSupportWordsAcrossFourProductionFamilies",
     "benefitsLookalikesAndTwoFallbackRadicalsAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineHillThreeReciprocalPairsBothCuratedReadingsDrawingAndSystemBack",
     "fullSingleImportOfflineBenefitsTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
    ("00491dddddaa65467b0f7ad474689e054a00f5f4", HEAD),
    ("00491ddd", HEAD[:8]), ("5e8f3e7e39ea187a", manifest["contentVersion"]),
    ("1070", "1071"), ("5029", "5030"), ("90, n1.size", "91, n1.size"),
    ("N1 · 90 cards", "N1 · 91 cards"),
    ('"丘 兵 近 共 一 砂 山 丘 砂丘"', '"享 京 厚 高 亠 厂 子 口 受 享受"'),
    ('listOf("丘", "兵", "近", "共", "一", "砂", "山")',
     'listOf("享", "京", "厚", "高", "亠", "厂", "子", "口", "受")'),
    ('listOf("丘", "砂丘")', 'listOf("享受")'),
    ("Batch 059: hill / look-alikes / radical / support",
     "Batch 059: benefits / look-alikes / fallback radicals"),
    ("Compare 丘 with 兵, 近 and 共; inspect radical 一, both components of 砂丘 and contextual 山. Shared fallback need not give four different designs.",
     "Compare 享 with 京, 厚 and 高. Inspect actual 亠 and 厂 fallback glyphs, 子 versus 小-shaped bases and both 享受 components. Shared fallback need not give four different designs."),
    ("assertEquals(36, rows.length())", "assertEquals(40, rows.length())"),
    ('.put("individualGlyphProbes", 28).put("wholeWordRasterProbes", 8)',
     '.put("individualGlyphProbes", 36).put("wholeWordRasterProbes", 4)'),
    ("Twenty-eight single-character native Paint probes, eight complete-word nonblank raster probes and four production Compose rows; actual 丘/兵/近/共/一/砂/山/丘/砂丘 readability requires separate visual inspection.",
     "Thirty-six single-character native Paint probes including actual 亠 and 厂, four complete-word nonblank raster probes and four production Compose rows; actual 享/京/厚/高/亠/厂/子/口/受/享受 readability requires separate visual inspection."),
    ("val hill", "val benefits"), ("hill.", "benefits."),
    ('"丘"', '"享"'), ("hill; knoll", "enjoy; receive benefits"),
    ('listOf("キュウ")', 'listOf("キョウ", "コウ")'),
    ('listOf("おか")', 'listOf("う.ける")'),
    ('"きゅう"', '"きょう"'),
    ("丘 meaning and both curated keys due. Two historical good 丘 meaning logs",
     "享 meaning and sole curated on key due; explicit no-kun. Two historical good 享 meaning logs"),
    ("assertEquals(5, strokes.length())", "assertEquals(8, strokes.length())"),
    ("5 strokes drawn", "8 strokes drawn"),
    ('"bothCuratedQuestionsAndPersistedGrades"', '"soleCuratedOnQuestionAndPersistedGradeNoKun"'),
):
    assert old in text, old
    text = text.replace(old, new)
text = text.replace('assertEquals(listOf("キョウ", "コウ"), benefits.quizOnyomi?.splitSep())',
                    'assertEquals(listOf("キョウ"), benefits.quizOnyomi?.splitSep())')
text = text.replace('assertEquals(listOf("う.ける"), benefits.quizKunyomi?.splitSep())',
                    'assertEquals(emptyList<String>(), benefits.quizKunyomi?.splitSep())')
text = text.replace('assertEquals(listOf("う.ける"), benefits.toReadingCard().quizKeys(ReadingKind.Kun))',
                    'assertEquals(emptyList<String>(), benefits.toReadingCard().quizKeys(ReadingKind.Kun))')
text = text.replace('assertEquals(listOf("キョウ", "コウ"), card.quizOnyomi?.splitSep())',
                    'assertEquals(listOf("キョウ"), card.quizOnyomi?.splitSep())')
text = text.replace('assertEquals(listOf("う.ける"), card.quizKunyomi?.splitSep())',
                    'assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())')
text = text.replace('((kind == ReadingKind.On && key == "きょう") || (kind == ReadingKind.Kun && key == "おか"))',
                    '(kind == ReadingKind.On && key == "きょう")')
start = text.index('            await("no. 1)"')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = '''            await("no. 8)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("享 connects receiving something", "kanji-meaning")
            show("Modern-shape mnemonic, not etymology", "kanji-mnemonic")
            section("Readings")
            show(readingExample("享受 きょうじゅ - enjoyment of benefits or rights"), "kanji-on-reading")
            show(readingExample("Source-only lookup reading here; no suitable modern word example was established in the inspected dictionary families."), "kanji-source-only-on")
            show(readingExample("享ける うける - receive (recognition spelling); 生を享ける せいをうける, \\"be born\\""), "kanji-recognition-kun")
            show("Practice selects キョウ.", "kanji-curation")
            show("享ける is an attested spelling", "kanji-recognition-boundaries")
            section("Notes")
            show(articleBullet("Distinguish 京, \\"capital\\": its bottom is 小-shaped, whereas 享 ends in 子. 厚 has a 厂 overhang and a 日-shaped box above 子; 享 instead starts with 亠 above 口."), "kanji-lookalikes-fallback")
            show(articleBullet("受 is the broader receiving/undergoing character. Learn the whole word and spelling rather than substituting either character mechanically."), "kanji-receiving-boundary")
            show(articleBullet("享年 names age at death, not someone's current age or a general wish for a long life."), "kanji-age-boundary")
            section("Common words")
            inline(await(articleBullet("享受 きょうじゅ - enjoyment of benefits or rights")), "享受")
            await("享受 (きょうじゅ) - enjoyment of benefits or rights")
            section("Meaning")
            show("享受 means receiving something as one's own", "word-meaning-attachment")
            show(articleBullet("私たちは自由を享受しています。 (わたしたちはじゆうをきょうじゅしています。) - We enjoy freedom."), "word-freedom-example")
            show(articleBullet("私たちは科学技術の恩恵を享受しています。 (わたしたちはかがくぎじゅつのおんけいをきょうじゅしています。) - We enjoy the benefits of science and technology."), "word-benefits-example")
            show("Useful forms include", "word-forms")
            section("How the kanji combine")
            show("Their related meanings reinforce", "word-components-readings")
            inline(await("Their related meanings reinforce", substring = true), "享")
            await("Article contents")
            section("Readings")
            show("Practice selects キョウ.", "word-backlink-benefits")
            back()
            await("Their related meanings reinforce", substring = true).assertIsDisplayed()
            capture("system-back-word-benefits")
            inline(await("Their related meanings reinforce", substring = true), "受")
            await("Article contents")
            section("Common words")
            show(articleBullet("享受 きょうじゅ — enjoyment of benefits or rights"), "receiving-forwardlink")
            inline(await(articleBullet("享受 きょうじゅ — enjoyment of benefits or rights")), "享受")
            await("享受 (きょうじゅ) - enjoyment of benefits or rights")
            section("Distinctive meaning")
            show("rather than merely playing or feeling happy", "receiving-forwardlink-word")
            back()
            await("Common words")
            capture("system-back-receiving")
            back()
            await("Their related meanings reinforce", substring = true).assertIsDisplayed()
            capture("system-back-word-receiving")
            section("Synonyms and antonyms")
            show("Neither is freely interchangeable", "word-enjoying-receiving-boundaries")
            show("not a single antonym", "word-benefit-contrast")
            section("Distinctive meaning")
            show("rather than merely playing or feeling happy", "word-recreation-boundary")
            show("Do not confuse it with 教授", "word-homophone")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
text = text.replace("            repeat(2) {", "            repeat(1) {")
old = '                val key = if (question.question.kind == ReadingKind.On) "きょう" else "おか"'
assert old in text
text = text.replace(old, '''                assertEquals(ReadingKind.On, question.question.kind)
                val key = "きょう"
                assertFalse(question.question.options.any { it.key in setOf("こう", "うける") })''')
text = text.replace("assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)",
                    '''assertEquals(setOf(ReadingKind.On), answeredKinds)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "享" && it.mode == ReadingKind.Kun.mode.name }
            })''')
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
assert not any(old in text for old in ("058", "丘", "砂", "おか", "キュウ", "hill", "00491ddd", "both curated"))
assert text.count('assertEquals(emptyList<String>(),') == 3
documents = {name: blocks(ROOT / name) for name in
             ("kanji/享.md", "words/享受.md", "kanji/受.md")}
stack, selectors, controls, transitions = ["kanji/享.md"], [], [], []
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
assert stack == ["kanji/享.md"]
assert len(transitions) == 4 and len(set(tuple(pair) for pair in transitions)) == 4
accepted = json.loads((ROOT / "docs" / "n1-sources" / "execution-355.json").read_text(encoding="utf-8"))
for item in accepted["archivedArtifacts"]:
    assert sha(ROOT / item["path"]) == item["sha256"]
for test in accepted["recovery"]["tests"]:
    assert test["failures"] == test["errors"] == test["skipped"] == 0
archive = CONTROL / "artifacts" / "n1-batch-059-911431da-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-059/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-059/"
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
diff_path = FOLDER / "fixture-from-058.diff"
diff_path.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)),
    encoding="utf-8")
assert sha(PRIOR) == prior_hash
for name, expected in initial_reports.items():
    assert sha(ROOT / name) == expected
record = {
    "schemaVersion": 1, "execution": 356, "batch": "059",
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
    "plannedNativePaintProbes": 36, "plannedWholeWordRasterProbes": 4,
    "plannedGlyphs": ["享", "京", "厚", "高", "亠", "厂", "子", "口", "受"],
    "plannedWholeWords": ["享受"],
    "fullReadings": {"on": ["キョウ", "コウ"], "kun": ["う.ける"]},
    "curatedReadings": {"on": ["キョウ"], "kun": []},
    "normalizedQuizKeys": {"on": ["きょう"], "kun": []},
    "reciprocalPairs": [["享", "享受"], ["受", "享受"]],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted355AndroidRetainedWithoutRerun": True,
    "nativeExecuted": False, "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "limits": "Static fixture/archive preparation, not native execution, readability, independent visual, phone or publication acceptance. Article selectors use a bounded Markdown projection, not a native semantics tree. Exact full Git envelope; production ContentSync called ONCE with unchanged guards. Both reciprocal pairs include reused受. Actual亠/厂 fallback remains pending until native execution and direct visual inspection. Raster hashes do not identify fallback faces or certify readability. Touch-reference trace and recall miss do not prove MLKit recognition or correct human recall. Accepted355 Android3+1 retained; original354 permission denial/049 host-only heap qualification unchanged. Historical Claude first-confirmation overlap remains noncompliance; bounded remediation is not retroactive strict acceptance. Fresh5580/5581 ownership check mandatory before later launch;040 exception not inherited. No emulator/reviewer/publication/060/second runner. Published85/1228,1143remain; compatibleAndroidf9b59a2+ required; phone/generalrelease/whole-set outstanding.",
}
save(CONTROL / "batch-059-native-fixture-verification.json", record)
print(json.dumps({key: record[key] for key in
                  ("status", "contentVersion", "expectedCounts", "archiveSha256", "zipEntries",
                   "compressedBytes", "inflatedBytes", "retainedBytes", "verifiedRuntimeHashes",
                   "fixtureSha256", "captureSteps")}, ensure_ascii=False, indent=2))
print("Unique article selectors:", len(selectors), "Directed reciprocal transitions:", len(transitions))
