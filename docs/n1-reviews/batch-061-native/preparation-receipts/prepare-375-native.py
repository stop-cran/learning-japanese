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
HEAD = "f891cb1e0b43c4fefcb31da16f28f3159b49aea4"
REVIEWED = "2567f5e7b3888f2df3ed560f618341266b471902"
APP_HEAD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-061-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-060-native" / "N1Batch060NativeTest.kt"
FIXTURE = FOLDER / "N1Batch061NativeTest.kt"


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
assert progress["checkpoint"] == 374 and progress["execution375StartingState"]["execution"] == 375
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1073, "words": 5031, "n1": 93}, counts
assert manifest["contentVersion"] == "d01d660cc41262fe"
initial_reports = {
    f"docs/n1-reviews/batch-061-initial-{family}.md":
        sha(ROOT / "docs" / "n1-reviews" / f"batch-061-initial-{family}.md")
    for family in ("claude", "gpt")
}
prior_hash = sha(PRIOR)
text = PRIOR.read_text(encoding="utf-8")
glyphs = ["俳", "非", "悲", "借", "優", "人", "亻", "昔", "心", "句", "憂"]
for old, new in (
    ("060", "061"),
    ("pavilionLookalikesAndThreeFallbackComponentsAcrossFourProductionFamilies",
     "haikuActorLookalikesAndPersonFallbackAcrossFourProductionFamilies"),
    ("fullSingleImportOfflinePavilionTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
     "fullSingleImportOfflineHaikuActorThreeReciprocalPairsOnOnlyDrawingAndSystemBack"),
    ("99d8ace026aaf5cf76b4adada34b14e969d10d4e", HEAD),
    ("99d8ace0", HEAD[:8]), ("dbf047f0c2e6cd56", manifest["contentVersion"]),
    ("1072", "1073"), ("92, n1.size", "93, n1.size"), ("N1 · 92 cards", "N1 · 93 cards"),
    ('"亭 停 京 享 高 亠 亻 冖 丁 小 子 口 料 料亭"', '"俳 非 悲 借 優 人 亻 昔 心 句 憂 俳句 俳優"'),
    ('listOf("亭", "停", "京", "享", "高", "亠", "亻", "冖", "丁", "小", "子", "口", "料")',
     'listOf("俳", "非", "悲", "借", "優", "人", "亻", "昔", "心", "句", "憂")'),
    ('listOf("料亭")', 'listOf("俳句", "俳優")'),
    ("Batch 061: pavilion / look-alikes / fallback components",
     "Batch 061: haiku and actor / look-alikes / person fallback"),
    ("Compare 亭 with 停, 京, 享 and 高. Inspect actual 亠, 亻 and 冖 fallback glyphs, 丁 versus 小 and 子 bases, and both 料亭 components. Shared fallback need not give four different designs.",
     "Compare 俳 with 非, 悲, 借 and 優. Inspect actual 人 versus 亻, 非 versus 昔, 心 and 憂, and both words 俳句 and 俳優. Shared fallback need not give four different designs."),
    ("assertEquals(56, rows.length())", "assertEquals(52, rows.length())"),
    ('.put("individualGlyphProbes", 52).put("wholeWordRasterProbes", 4)',
     '.put("individualGlyphProbes", 44).put("wholeWordRasterProbes", 8)'),
    ("Fifty-two single-character native Paint probes including actual 亠, 亻 and 冖, four complete-word nonblank raster probes and four production Compose rows; actual 亭/停/京/享/高/亠/亻/冖/丁/小/子/口/料/料亭 readability requires separate visual inspection.",
     "Forty-four single-character native Paint probes including actual 人 and 亻, eight complete-word nonblank raster probes and four production Compose rows; actual 俳/非/悲/借/優/人/亻/昔/心/句/憂/俳句/俳優 readability requires separate visual inspection."),
    ("val pavilion", "val performer"), ("pavilion.", "performer."),
    ('"亭"', '"俳"'),
    ("pavilion; restaurant building", "haiku; actor"),
    ('listOf("テイ", "チン")', 'listOf("ハイ")'),
    ('listOf("テイ")', 'listOf("ハイ")'),
    ('"てい"', '"はい"'),
    ('assertFalse(question.question.options.any { it.key in setOf("ちん") })',
     'assertFalse(question.question.options.any { it.key.isBlank() })'),
    ("亭 meaning and sole curated on key due", "俳 meaning and sole curated on key due"),
    ("Two historical good 亭 meaning logs", "Two historical good 俳 meaning logs"),
    ("assertEquals(9, strokes.length())", "assertEquals(10, strokes.length())"),
    ("9 strokes drawn", "10 strokes drawn"),
):
    assert old in text, old
    text = text.replace(old, new)
start = text.index('            await("no. 8)"')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = '''            await("no. 9)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("俳 connects two useful vocabulary families", "kanji-meaning")
            show("Modern-shape mnemonic:", "kanji-mnemonic")
            section("Readings")
            show(readingExample("俳句 はいく — haiku; 俳優 はいゆう — actor; actress"), "kanji-on-reading")
            show("The source metadata lists no kun reading.", "kanji-no-kun")
            section("Notes")
            show(articleBullet("The right-hand 非 does not make these words mean \\"not a poem\\" or \\"not an actor.\\" A visible component is not a word-by-word translation rule."), "kanji-component-boundary")
            show(articleBullet("悲 has 非 above 心, rather than a person-shaped component on the left. 借 shares 亻 but has 昔 on the right, not 非."), "kanji-lookalikes")
            show(articleBullet("In 俳優, 優 also has a performer-related use; translating it as \\"gentle\\" does not explain the occupation."), "kanji-performer-boundary")
            show(articleBullet("The traditional Japanese haiku pattern concerns Japanese sound units, not seventeen English syllables. The linked 俳句 article explains the form and its qualifications."), "kanji-mora-boundary")
            section("Common words")
            inline(await(articleBullet("俳句 はいく — haiku, a short poetic form")), "俳句")
            await("俳句 (はいく) - haiku")
            section("Meaning")
            show("Free-form and nonseasonal haiku also exist", "haiku-form-qualification")
            show(articleBullet("春の俳句を作りました。 (はるのはいくをつくりました。) - I composed a spring haiku."), "haiku-composing-example")
            show(articleBullet("この俳句には春の季語が入っています。 (このはいくにははるのきごがはいっています。) - This haiku contains a spring seasonal word."), "haiku-season-example")
            show("A mora is a timing unit", "haiku-mora-definition")
            section("How the kanji combine")
            show("The on readings combine as はい + く.", "haiku-components")
            inline(await("The on readings combine as はい + く.", substring = true), "俳")
            await("Article contents")
            section("Readings")
            show("The source metadata lists no kun reading.", "haiku-backlink")
            back()
            await("The on readings combine as はい + く.", substring = true).assertIsDisplayed()
            capture("system-back-haiku")
            section("Synonyms and antonyms")
            show("names a person rather than a poem.", "haiku-comparison")
            section("Distinctive meaning")
            show("Do not define every haiku as seventeen English syllables", "haiku-distinctive")
            back()
            await("Common words")
            inline(await(articleBullet("俳優 はいゆう — actor; actress")), "俳優")
            await("俳優 (はいゆう) - actor")
            section("Meaning")
            show("the word is not inherently restricted to men.", "actor-gender-boundary")
            show(articleBullet("彼女は映画で活躍する俳優です。 (かのじょはえいがでかつやくするはいゆうです。) - She is an actor active in films."), "actor-film-example")
            show(articleBullet("子どものころから俳優になりたかったです。 (こどものころからはいゆうになりたかったです。) - I have wanted to become an actor since childhood."), "actor-childhood-example")
            show("好きな俳優 (すきなはいゆう)", "actor-noun-attachment")
            section("How the kanji combine")
            show("The on-readings are ハイ + ユウ.", "actor-components")
            inline(await("contributes an entertainer or performer in this compound.", substring = true), "俳")
            await("Article contents")
            section("Readings")
            show("The source metadata lists no kun reading.", "actor-backlink")
            back()
            await("The on-readings are ハイ + ユウ.", substring = true).assertIsDisplayed()
            capture("system-back-actor-performer")
            inline(await("also has an actor-related use here", substring = true), "優")
            await("Article contents")
            section("Common words")
            show(articleBullet("俳優 はいゆう — actor"), "superior-forwardlink")
            inline(await(articleBullet("俳優 はいゆう — actor")), "俳優")
            await("俳優 (はいゆう) - actor")
            section("Distinctive meaning")
            show("not automatically a football player or music-playback device", "superior-forwardlink-actor")
            back()
            await("Common words")
            capture("system-back-superior")
            back()
            await("The on-readings are ハイ + ユウ.", substring = true).assertIsDisplayed()
            capture("system-back-actor-superior")
            section("Synonyms and antonyms")
            show("the occupations are not synonyms.", "actor-occupation-boundary")
            section("Distinctive meaning")
            show("It does not by itself say whether the person is famous", "actor-status-boundary")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for obsolete in ("060", "料亭", "亭", "テイ", "チン", '"てい"', "99d8ace0"):
    assert obsolete not in text, obsolete
documents = {name: blocks(ROOT / name) for name in
             ("kanji/俳.md", "words/俳句.md", "words/俳優.md", "kanji/優.md")}
stack, selectors, controls, transitions = ["kanji/俳.md"], [], [], []
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
assert stack == ["kanji/俳.md"]
assert len(transitions) == len(set(tuple(pair) for pair in transitions)) == 6
accepted = json.loads((ROOT / "docs" / "n1-sources" / "execution-374.json").read_text(encoding="utf-8"))
for item in accepted["archivedArtifacts"]:
    assert sha(ROOT / item["path"]) == item["sha256"]
for test in accepted["recovery"]["tests"]:
    assert test["failures"] == test["errors"] == test["skipped"] == 0
archive = CONTROL / "artifacts" / "n1-batch-061-f891cb1e-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-061/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-061/"
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
diff_path = FOLDER / "fixture-from-060.diff"
diff_path.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)),
    encoding="utf-8")
assert sha(PRIOR) == prior_hash
for name, expected in initial_reports.items():
    assert sha(ROOT / name) == expected
record = {
    "schemaVersion": 1, "execution": 375, "batch": "061",
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
    "plannedNativePaintProbes": 44, "plannedWholeWordRasterProbes": 8,
    "plannedGlyphs": glyphs, "plannedWholeWords": ["俳句", "俳優"],
    "fullReadings": {"on": ["ハイ"], "kun": []},
    "curatedReadings": {"on": ["ハイ"], "kun": []},
    "normalizedQuizKeys": {"on": ["はい"], "kun": []},
    "reciprocalPairs": [["俳", "俳句"], ["俳", "俳優"], ["優", "俳優"]],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted374AndroidRetainedWithoutRerun": True,
    "nativeExecuted": False, "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "limits": "Static fixture/archive preparation, not native execution, readability, independent visual, phone or publication acceptance. Article selectors use a bounded Markdown projection, not a native semantics tree. Exact full Git envelope; production ContentSync called ONCE with unchanged guards. All three reciprocal pairs include reused優. Actual人/亻 readability remains pending until native execution and direct visual inspection. Raster hashes do not identify fallback faces or certify readability. Touch-reference trace and recall miss do not prove MLKit recognition or correct human recall. Accepted374 Android3+1 retained; original373 permission denial/049 host-only heap qualification unchanged. Original Claude061-P1/P2 process noncompliance remains historical; dependent lexical remediation is not retroactive strict initial acceptance. Fresh5580/5581 ownership check mandatory before later launch;040 exception not inherited. No emulator/reviewer/publication/062/second runner. Published87/1228,1141remain; compatibleAndroidf9b59a2+ required; phone/generalrelease/whole-set outstanding.",
}
save(CONTROL / "batch-061-native-fixture-verification.json", record)
print(json.dumps({key: record[key] for key in
                  ("status", "contentVersion", "expectedCounts", "archiveSha256", "zipEntries",
                   "compressedBytes", "inflatedBytes", "retainedBytes", "verifiedRuntimeHashes",
                   "fixtureSha256", "captureSteps")}, indent=2))
print("Article selectors:", len(selectors), "Directed reciprocal transitions:", len(transitions))
