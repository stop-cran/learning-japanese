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
HEAD = "e157d58c5bdb9fc2d58d7043fdf0429d36f5c040"
REVIEWED = "38ab6072d2041325142c54cf54be5d126928eb31"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-062-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-061-native" / "N1Batch061NativeTest.kt"
FIXTURE = FOLDER / "N1Batch062NativeTest.kt"


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
            paragraph.append(line[2:])
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
assert progress["checkpoint"] == 384 and progress["execution385StartingState"]["execution"] == 385
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1074, "words": 5032, "n1": 94}, counts
assert manifest["contentVersion"] == "545c56b5d4b4e8ef"
initial_reports = {
    f"docs/n1-reviews/batch-062-initial-{family}.md":
        sha(ROOT / "docs" / "n1-reviews" / f"batch-062-initial-{family}.md")
    for family in ("claude", "gpt")
}
prior_hash = sha(PRIOR)
text = PRIOR.read_text(encoding="utf-8")
glyphs = ["俸", "棒", "奉", "借", "付", "人", "亻", "木", "給", "糸", "合"]
for old, new in (
    ("061", "062"),
    ("haikuActorLookalikesAndPersonFallbackAcrossFourProductionFamilies",
     "salaryLookalikesAndPersonFallbackAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineHaikuActorThreeReciprocalPairsOnOnlyDrawingAndSystemBack",
     "fullSingleImportOfflineSalaryTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
    ("f891cb1e0b43c4fefcb31da16f28f3159b49aea4", HEAD),
    ("f891cb1e", HEAD[:8]), ("d01d660cc41262fe", manifest["contentVersion"]),
    ("1073", "1074"), ("5031", "5032"),
    ("93, n1.size", "94, n1.size"), ("N1 · 93 cards", "N1 · 94 cards"),
    ('"俳 非 悲 借 優 人 亻 昔 心 句 憂 俳句 俳優"', '"俸 棒 奉 借 付 人 亻 木 給 糸 合 俸給"'),
    ('listOf("俳", "非", "悲", "借", "優", "人", "亻", "昔", "心", "句", "憂")',
     'listOf("俸", "棒", "奉", "借", "付", "人", "亻", "木", "給", "糸", "合")'),
    ('listOf("俳句", "俳優")', 'listOf("俸給")'),
    ("Batch 062: haiku and actor / look-alikes / person fallback",
     "Batch 062: salary / look-alikes / person fallback"),
    ("Compare 俳 with 非, 悲, 借 and 優. Inspect actual 人 versus 亻, 非 versus 昔, 心 and 憂, and both words 俳句 and 俳優. Shared fallback need not give four different designs.",
     "Compare 俸 with 棒, 奉, 借 and 付. Inspect actual 人 versus 亻, 木 versus 亻, 給 with 糸 and 合, and both characters in 俸給. Shared fallback need not give four different designs."),
    ("assertEquals(52, rows.length())", "assertEquals(48, rows.length())"),
    ('.put("individualGlyphProbes", 44).put("wholeWordRasterProbes", 8)',
     '.put("individualGlyphProbes", 44).put("wholeWordRasterProbes", 4)'),
    ("Forty-four single-character native Paint probes including actual 人 and 亻, eight complete-word nonblank raster probes and four production Compose rows; actual 俳/非/悲/借/優/人/亻/昔/心/句/憂/俳句/俳優 readability requires separate visual inspection.",
     "Forty-four single-character native Paint probes including actual 人 and 亻, four complete-word nonblank raster probes and four production Compose rows; actual 俸/棒/奉/借/付/人/亻/木/給/糸/合/俸給 readability requires separate visual inspection."),
    ("performer", "salary"),
    ('"俳"', '"俸"'),
    ("haiku; actor", "salary; stipend"),
    ('listOf("ハイ")', 'listOf("ホウ")'),
    ('"はい"', '"ほう"'),
    ("俳 meaning and sole curated on key due", "俸 meaning and sole curated on key due"),
    ("Two historical good 俳 meaning logs", "Two historical good 俸 meaning logs"),
):
    assert old in text, old
    text = text.replace(old, new)
start = text.index('            await("no. 9)"')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = '''            await("no. 9)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("俸 concerns salary or a stipend", "kanji-meaning")
            show("but is not restricted to government employment.", "kanji-employment-boundary")
            show("Modern-shape mnemonic:", "kanji-mnemonic")
            section("Readings")
            show(readingExample("俸給 ほうきゅう — salary; pay"), "kanji-on-reading")
            show("pronounced ぽう, not ぼう", "kanji-no-kun-and-annual-reading")
            section("Notes")
            show(articleBullet("棒, \\"rod; stick,\\" has 木 on the left instead of 亻. Write 年俸 for annual salary; JMdict marks 年棒 as irregular kanji usage."), "kanji-spelling-boundary")
            show(articleBullet("借, \\"borrow; rent,\\" and 付, \\"attach,\\" share 亻 but have different right sides. Neither names a salary."), "kanji-lookalikes")
            show(articleBullet("年俸 specifies an annual basis or a year's salary, not necessarily a single yearly payment. The word alone does not establish a payment schedule."), "kanji-payment-schedule")
            show(articleBullet("Historical 俸禄 ほうろく means a retainer's stipend. That historical use does not make modern 俸給 a payment in rice."), "kanji-historical-boundary")
            section("Common words")
            show(articleBullet("年俸 ねんぽう — annual salary"), "kanji-annual-compound")
            show(articleBullet("減俸 げんぽう — salary reduction"), "kanji-reduction-compound")
            inline(await(articleBullet("俸給 ほうきゅう — salary; pay, especially for public employees")), "俸給")
            await("俸給 (ほうきゅう) — salary; pay")
            section("Meaning")
            show("It is not a government-only synonym of salary.", "salary-employment-boundary")
            show(articleBullet("俸給を受け取っています。 (ほうきゅうをうけとっています。) — I receive a salary."), "salary-receiving-example")
            show(articleBullet("俸給が上がりました。 (ほうきゅうがあがりました。) — My salary went up."), "salary-increase-example")
            show("The second reports an increase, not a change of occupation.", "salary-example-explanation")
            section("How the kanji combine")
            show("Keep both long vowels.", "salary-components")
            inline(await("The on readings are ホウ + キュウ: ほうきゅう.", substring = true), "俸")
            await("Article contents")
            section("Readings")
            show("pronounced ぽう, not ぼう", "salary-backlink")
            back()
            await("Keep both long vowels.", substring = true).assertIsDisplayed()
            capture("system-back-salary-stipend")
            inline(await("The on readings are ホウ + キュウ: ほうきゅう.", substring = true), "給")
            await("Article contents")
            section("Common words")
            show(articleBullet("俸給 ほうきゅう — salary; pay, especially for public employees"), "pay-forwardlink")
            inline(await(articleBullet("俸給 ほうきゅう — salary; pay, especially for public employees")), "俸給")
            await("俸給 (ほうきゅう) — salary; pay")
            section("Distinctive meaning")
            show("not as a rule forbidding its use for company employees.", "pay-forwardlink-salary")
            back()
            await("Common words")
            capture("system-back-pay")
            back()
            await("Keep both long vowels.", substring = true).assertIsDisplayed()
            capture("system-back-salary-pay")
            section("Synonyms and antonyms")
            show("overlap this employment-pay sense.", "salary-synonyms")
            show("specifies a monthly salary.", "salary-monthly-boundary")
            show("sources other than employment.", "salary-income-boundary")
            section("Distinctive meaning")
            show("not as a rule forbidding its use for company employees.", "salary-employment-guide")
            show("The word alone does not tell you the payment interval", "salary-document-boundary")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for obsolete in ("061", "俳", "俳句", "俳優", "ハイ", '"はい"', "f891cb1e", "1073", "5031"):
    assert obsolete not in text, obsolete
documents = {name: blocks(ROOT / name) for name in
             ("kanji/俸.md", "words/俸給.md", "kanji/給.md")}
stack, selectors, controls, transitions = ["kanji/俸.md"], [], [], []
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
assert stack == ["kanji/俸.md"]
assert len(transitions) == len(set(tuple(pair) for pair in transitions)) == 4
accepted = json.loads((ROOT / "docs" / "n1-sources" / "execution-384.json").read_text(encoding="utf-8"))
for item in accepted["archivedArtifacts"]:
    assert sha(ROOT / item["path"]) == item["sha256"]
for test in accepted["recovery"]["tests"]:
    assert test["failures"] == test["errors"] == test["skipped"] == 0
archive = CONTROL / "artifacts" / "n1-batch-062-e157d58c-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-062/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-062/"
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
diff_path = FOLDER / "fixture-from-061.diff"
diff_path.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)),
    encoding="utf-8")
assert sha(PRIOR) == prior_hash
for name, expected in initial_reports.items():
    assert sha(ROOT / name) == expected
record = {
    "schemaVersion": 1, "execution": 385, "batch": "062",
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
    "plannedNativePaintProbes": 44, "plannedWholeWordRasterProbes": 4,
    "plannedGlyphs": glyphs, "plannedWholeWords": ["俸給"],
    "fullReadings": {"on": ["ホウ"], "kun": []},
    "curatedReadings": {"on": ["ホウ"], "kun": []},
    "normalizedQuizKeys": {"on": ["ほう"], "kun": []},
    "reciprocalPairs": [["俸", "俸給"], ["給", "俸給"]],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted384AndroidRetainedWithoutRerun": True,
    "nativeExecuted": False, "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "limits": "Static fixture/archive preparation, not native execution, readability, independent visual, phone or publication acceptance. Article selectors use a bounded Markdown projection, not a native semantics tree. Exact full Git envelope; production ContentSync called ONCE with unchanged guards. Both reciprocal pairs include reused給. Actual人/亻 readability remains pending until native execution and direct visual inspection. Raster hashes do not identify fallback faces or certify readability. Touch-reference trace and recall miss do not prove MLKit recognition or correct human recall. Accepted384 Android3+1 retained; original383 permission denial/049 host-only heap qualification unchanged. Original Claude062-P1/P2 process noncompliance remains historical; dependent lexical remediation is not retroactive strict initial acceptance. Fresh5580/5581 ownership check mandatory before later launch;040 exception not inherited. No emulator/reviewer/publication/063/second runner. Published88/1228,1140remain; compatibleAndroidf9b59a2+ required; phone/generalrelease/whole-set outstanding.",
}
save(CONTROL / "batch-062-native-fixture-verification.json", record)
print(json.dumps({key: record[key] for key in
                  ("status", "contentVersion", "expectedCounts", "archiveSha256", "zipEntries",
                   "compressedBytes", "inflatedBytes", "retainedBytes", "verifiedRuntimeHashes",
                   "fixtureSha256", "captureSteps")}, indent=2))
print("Article selectors:", len(selectors), "Directed reciprocal transitions:", len(transitions))
