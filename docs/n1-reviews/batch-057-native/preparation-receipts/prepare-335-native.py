import difflib
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
HEAD = "d9712bf9a2c03f3fae51c2f751481a05affbc0f9"
REVIEWED = "acc397033503a38aa88506fc3ad966761793db72"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-057-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-056-native" / "N1Batch056Retry2NativeTest.kt"
FIXTURE = FOLDER / "N1Batch057NativeTest.kt"


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


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
refresh = sys.argv[1:] == ["--refresh"]
if refresh:
    assert not git("diff", "--name-only")
    assert git("status", "--porcelain").decode().strip() == "?? docs/n1-reviews/batch-057-native/"
    prior_preparation = load(CONTROL / "batch-057-native-fixture-verification.json")
    assert sha(FIXTURE) == prior_preparation["fixtureSha256"]
else:
    assert not git("status", "--porcelain")
assert not git("status", "--porcelain", cwd=ANDROID)
assert git("rev-parse", "HEAD", cwd=ANDROID).decode().strip() == APP_HEAD
assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
progress = load(CONTROL / "progress.json")
assert progress["checkpoint"] == 334 and progress["execution335StartingState"]["execution"] == 335
assert FOLDER.exists() == refresh
prior_hash = sha(PRIOR)
initial_reports = {
    f"docs/n1-reviews/batch-057-initial-{family}.md":
        sha(ROOT / "docs" / "n1-reviews" / f"batch-057-initial-{family}.md")
    for family in ("claude", "gpt")
}
manifest = load(ROOT / "manifest.json")
assert manifest["contentVersion"] == "47f11f7f539a1d55"
kanji_count = sum(path.startswith("kanji/") for path in manifest["files"])
word_count = sum(path.startswith("words/") for path in manifest["files"])
n1_count = sum(re.search(r"^jlpt: 1$", path.read_text(encoding="utf-8"), re.M) is not None
               for path in (ROOT / "kanji").glob("*.md"))
assert (kanji_count, word_count, n1_count) == (1069, 5028, 89)
text = PRIOR.read_text(encoding="utf-8")
for old, new in (
    ("N1Batch056Retry2", "N1Batch057"),
    ("056", "057"),
    ("scarcityLookalikesAndRadicalFamineFallbackAcrossFourProductionFamilies",
     "planningLookalikesAndSupportWordsAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineScarcityArticlesMeaningBothCuratedReadingsDrawingAndSystemBack",
     "fullSingleImportOfflinePlanningArticlesMeaningBothCuratedReadingsDrawingAndSystemBack"),
    ("fddfae3526b27d1deea8aabdb202b9a9168f0214", HEAD),
    ("fddfae35", HEAD[:8]), ("cb85043f73a606f3", manifest["contentVersion"]),
    ("1068", str(kanji_count)), ("5027", str(word_count)),
    ("88, n1.size", f"{n1_count}, n1.size"), ("N1 · 88 cards", f"N1 · {n1_count} cards"),
    ("scarcity", "planning"),
    ('"乏 久 反 乃 丿 饉 飢饉"', '"企 全 危 休 人 止 業 企業 企てる"'),
    ('listOf("乏", "久", "反", "乃", "丿", "饉", "飢")',
     'listOf("企", "全", "危", "休", "人", "止", "業")'),
    ("Batch 057: planning / look-alikes / fallback", "Batch 057: planning / look-alikes / support"),
    ("Compare 乏 with 久, 反 and 乃. Inspect radical 丿 and 饉 in 飢饉; shared fallback need not give four different designs.",
     "Compare 企 with 全, 危 and 休; inspect radical 人, lower 止 and both support words. Shared fallback need not give four different designs."),
    ('"乏"', '"企"'), ("scarce; lacking", "plan; undertake"),
    ('listOf("ボウ")', 'listOf("キ")'),
    ('listOf("とぼ.しい", "とも.しい")', 'listOf("くわだ.てる", "たくら.む")'),
    ('listOf("とぼ.しい")', 'listOf("くわだ.てる")'),
    ('"ぼう"', '"き"'), ('"とぼしい"', '"くわだてる"'), ('"ともしい"', '"たくらむ"'),
    ("乏 meaning and both curated keys due. Two historical good 乏 meaning logs",
     "企 meaning and both curated keys due. Two historical good 企 meaning logs"),
    ("assertEquals(4, strokes.length())", "assertEquals(6, strokes.length())"),
    ("4 strokes drawn", "6 strokes drawn"),
):
    assert old in text, old
    text = text.replace(old, new)
start = text.index('            val word = "飢饉"')
end = text.index("        assertEquals(32, rows.length())", start)
word_probe = text[start:end]
assert word_probe.endswith("        }\n")
word_probe = word_probe.removesuffix("        }\n")
word_probe = word_probe.replace('            val word = "飢饉"\n', "")
word_probe = word_probe.replace(
    "Bitmap.createBitmap(256, 128, Bitmap.Config.ARGB_8888)",
    "Bitmap.createBitmap(kotlin.math.ceil(paint.measureText(word)).toInt() + 16, 128, Bitmap.Config.ARGB_8888)")
word_probe = "".join("    " + line if line.strip() else line for line in word_probe.splitlines(keepends=True))
text = text[:start] + '            for (word in listOf("企業", "企てる")) {\n' + word_probe + "            }\n        }\n" + text[end:]
text = text.replace("assertEquals(32, rows.length())", "assertEquals(36, rows.length())")
text = text.replace('.put("wholeWordRasterProbes", 4)', '.put("wholeWordRasterProbes", 8)')
text = text.replace(
    "Twenty-eight single-character native Paint probes, four complete-word nonblank raster probes and four production Compose rows; actual 丿/饉/飢饉 readability requires separate visual inspection.",
    "Twenty-eight single-character native Paint probes, eight complete-word nonblank raster probes and four production Compose rows; actual 企/全/危/休/人/止/業/企業/企てる readability requires separate visual inspection.")
start = text.index('            await("no. 4)"')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = '''            await("no. 9)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("企 concerns planning", "kanji-meaning")
            show("Modern-shape mnemonic", "kanji-mnemonic")
            section("Readings")
            show(readingExample("企業 きぎょう — business enterprise; company"), "kanji-on-reading")
            show(readingExample("企てる くわだてる — plan; attempt"), "kanji-kun-reading")
            show(readingExample("企む たくらむ — scheme; often written たくらむ"), "kanji-recognition-reading")
            show("This card practices", "kanji-curation")
            section("Notes")
            show("They are not two interchangeable", "kanji-conjugation")
            show("The source indexes", "kanji-lookalike-radicals")
            show("neither has the planning meaning", "kanji-distractors")
            section("Common words")
            inline(await(articleBullet("企てる くわだてる — plan; attempt")), "企てる")
            await("企てる (くわだてる)", substring = true)
            section("Meaning")
            show("It is a transitive ichidan verb", "verb-grammar")
            show(articleBullet("新しい事業を企てています。 (あたらしいじぎょうをくわだてています。) — We are planning a new business venture."), "verb-business-example")
            show(articleBullet("彼らは何かを企てているようです。 (かれらはなにかをくわだてているようです。) — They seem to be plotting something."), "verb-plot-example")
            show("does not establish that the attempt succeeded", "verb-success-boundary")
            section("How the kanji combine")
            show("supplies くわだ", "verb-component")
            inline(await("supplies くわだ", substring = true), "企")
            await("Article contents")
            section("Meaning and origin")
            show("Modern-shape mnemonic", "verb-backlink-kanji")
            back()
            await("supplies くわだ", substring = true).assertIsDisplayed()
            capture("system-back-verb")
            section("Synonyms and antonyms")
            show("not restricted to bad intentions", "verb-register")
            show("accepting responsibility", "verb-undertake-boundary")
            section("Distinctive meaning")
            show("not the contracted form", "verb-separate-godan")
            show("archaic tiptoe sense", "verb-archaic-sense-boundary")
            back()
            await("Common words")
            inline(await(articleBullet("企業 きぎょう — business enterprise; company")), "企業")
            await("企業 (きぎょう)", substring = true)
            section("Meaning")
            show("businesses as economic organizations", "enterprise-scope")
            show(articleBullet("この企業は医療機器を作っています。 (このきぎょうはいりょうききをつくっています。) - This company makes medical equipment."), "enterprise-product-example")
            show(articleBullet("地元の企業で働きたいです。 (じもとのきぎょうではたらきたいです。) - I want to work for a local business."), "enterprise-work-example")
            show("uses で for the organization", "enterprise-particle")
            section("How the kanji combine")
            show("carries a planning or undertaking association", "enterprise-components-reading")
            inline(await("carries a planning or undertaking association", substring = true), "企")
            await("Article contents")
            section("Meaning and origin")
            show("Modern-shape mnemonic", "enterprise-backlink-kanji")
            back()
            await("carries a planning or undertaking association", substring = true).assertIsDisplayed()
            capture("system-back-enterprise")
            section("Synonyms and antonyms")
            show("overlaps strongly", "enterprise-company-overlap")
            show("production facility", "enterprise-factory-boundary")
            section("Distinctive meaning")
            show("does not inherently mean a giant corporation", "enterprise-size-boundary")
            show("not any undertaking such as a household chore", "enterprise-startup-boundary")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
assert not any(old in text for old in ("056", "scarcity", "乏", "飢", "饉", "とも", "とぼ", "ボウ", "fddfae35"))
documents = {name: blocks(ROOT / name) for name in ("kanji/企.md", "words/企てる.md", "words/企業.md")}
stack, selectors, controls = ["kanji/企.md"], [], []
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
        stack.append("kanji/企.md" if label == "企" else f"words/{label}.md")
assert stack == ["kanji/企.md"]
for article in ("企業", "企てる"):
    assert f"../words/{article}.md" in (ROOT / "kanji" / "企.md").read_text(encoding="utf-8")
    assert "../kanji/企.md" in (ROOT / "words" / f"{article}.md").read_text(encoding="utf-8")
android = progress["batch057AndroidCheckpoint"]
assert android["execution"] == 334
for test in android["tests"]:
    assert test["failures"] == test["errors"] == test["skipped"] == 0
    assert sha(ROOT / test["artifactPath"]) == test["sha256"]
archive = CONTROL / "artifacts" / "n1-batch-057-d9712bf9-envelope.zip"
if refresh:
    assert sha(archive) == prior_preparation["archiveSha256"]
else:
    assert not archive.exists()
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-057/",
                    f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-057/"
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
FOLDER.mkdir(exist_ok=refresh)
FIXTURE.write_text(text, encoding="utf-8")
diff_path = FOLDER / "fixture-from-056-retry2.diff"
diff_path.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)),
    encoding="utf-8")
assert sha(PRIOR) == prior_hash
for name, expected in initial_reports.items():
    assert sha(ROOT / name) == expected
record = {
    "schemaVersion": 1, "execution": 335, "batch": "057",
    "status": "static-native-preparation-verified-not-executed",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
    "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED, "androidSnapshot": APP_HEAD,
    "contentVersion": manifest["contentVersion"], "manifestSchemaVersion": 1,
    "baseLanguage": "en", "targetLanguage": "ja",
    "expectedCounts": {"kanji": kanji_count, "words": word_count, "n1": n1_count},
    "archive": str(archive), "archiveSha256": sha(archive),
    "zipEntries": len(names), "compressedBytes": archive.stat().st_size,
    "inflatedBytes": inflated, "retainedBytes": retained, "verifiedRuntimeHashes": verified,
    "manifestEqual": True, "safePathsPerFileAndOriginalPublishingBudgetsPassed": True,
    "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
    "reusedAcceptedHarness": str(PRIOR.relative_to(ROOT)),
    "reusedAcceptedHarnessSha256": prior_hash,
    "fixtureDiff": str(diff_path.relative_to(ROOT)), "fixtureDiffSha256": sha(diff_path),
    "originalInitialReportHashesUnchanged": initial_reports,
    "articleFiles": [{"path": name, "sha256": sha(ROOT / name),
                      "projectedTextBlocks": len(items)} for name, items in documents.items()],
    "staticMarkdownSelectors": selectors, "renderedNavigationControls": controls,
    "captureSteps": len(re.findall(r'(?:show\([^\n]+, |capture\()"([^"]+)"\)', route)),
    "plannedNativePaintProbes": 28, "plannedWholeWordRasterProbes": 8,
    "plannedGlyphs": ["企", "全", "危", "休", "人", "止", "業"],
    "plannedWholeWords": ["企業", "企てる"],
    "precompileInspectionCorrection": "Coordinator diff inspection caught that inherited fixed256px word bitmap cannot contain three full-width glyphs of企てる at96px. Allocate ceil(Paint.measureText(word))+16 before compiling; retain per-character nonblank and bounds assertions. Nested-loop indentation corrected. Original056 fixture/archive unchanged. No native run or failure occurred.",
    "fullReadings": {"on": ["キ"], "kun": ["くわだ.てる", "たくら.む"]},
    "curatedReadings": {"on": ["キ"], "kun": ["くわだ.てる"]},
    "normalizedQuizKeys": {"on": ["き"], "kun": ["くわだてる"]},
    "reciprocalPairs": [["企", "企業"], ["企", "企てる"]],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted334AndroidRetainedWithoutRerun": True,
    "nativeExecuted": False, "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "limits": "Static fixture/archive preparation, not native execution or visibility/readability/independent visual/phone/publication acceptance. Every article-route selector resolves to one block in the bounded static Markdown projection, not a fresh native semantics tree. Entire original full Git envelope retained; production ContentSync called ONCE, no duplicate parse/reduced archive, no production/font/guest-app-heap/archive-guard changes. Seven single-character probes per font and both complete support words; raster hashes do not identify fallback face or certify readability. Reference touches/recall miss do not prove MLKit recognition or human recall. Original056 failures/retry history untouched. Accepted334 Android3+1 retained without rerun; historical049 host-only Test heap qualification unchanged. Original057 blind reports, Claude52 overlaps/noncompliance and bounded confirmation limits remain immutable; strict original process contract not accepted. No native/reviewer/push/058/second runner or supervisor changes. Fresh5580/5581 ownership inspection mandatory immediately before future launch;040exception not inherited. Published83/1228,1145remaining; compatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
}
save(CONTROL / "batch-057-native-fixture-verification.json", record)
print(json.dumps({key: record[key] for key in
                  ("status", "expectedCounts", "archiveSha256", "zipEntries", "compressedBytes",
                   "inflatedBytes", "retainedBytes", "verifiedRuntimeHashes", "fixtureSha256",
                   "captureSteps")}, ensure_ascii=False, indent=2))
print("Unique article selectors:", len(selectors))
