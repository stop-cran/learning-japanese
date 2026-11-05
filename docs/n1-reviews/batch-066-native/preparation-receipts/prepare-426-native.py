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
HEAD = "175fdf3f1605f231e27a9de19a7c18c4a02cb20d"
REVIEWED = "6c23db00d2d14ec6d0a3537a1ef72b273e3d55e7"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-066-native"
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
assert progress["checkpoint"] == 425 and progress["execution426StartingState"]["execution"] == 426
assert not FOLDER.exists()
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
counts = {
    "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
    "words": sum(name.startswith("words/") for name in manifest["files"]),
    "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
              for p in (ROOT / "kanji").glob("*.md")),
}
assert counts == {"kanji": 1078, "words": 5036, "n1": 98}, counts
assert manifest["contentVersion"] == "a9ecc100b6c1335c"
reports = {f"docs/n1-reviews/batch-066-initial-{family}.md":
           sha(ROOT / "docs" / "n1-reviews" / f"batch-066-initial-{family}.md")
           for family in ("claude", "gpt")}
text = PRIOR.read_text(encoding="utf-8")
replacements = (
    ("064", "066"),
    ("investigationLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
     "colleagueLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
    ("fullSingleImportOfflineInvestigationTwoPairsComparisonOnOnlyDrawingAndSystemBack",
     "fullSingleImportOfflineColleagueTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
    ("bf6204e5b4e4c64f340dcd8db65b2924b869cc45", HEAD), ("bf6204e5", HEAD[:8]),
    ("ae05977ba66f42f5", manifest["contentVersion"]),
    ("1076", "1078"), ("5034", "5036"), ("96, n1.size", "98, n1.size"),
    ("N1 · 96 cards", "N1 · 98 cards"),
    ('"偵 貞 停 低 値 人 亻 探 手 扌 探偵 刑事"', '"僚 療 像 値 人 亻 疒 同 口 同僚"'),
    ('listOf("偵", "貞", "停", "低", "値", "人", "亻", "探", "手", "扌")',
     'listOf("僚", "療", "像", "値", "人", "亻", "疒", "同", "口")'),
    ('listOf("探偵", "刑事")', 'listOf("同僚")'),
    ("Batch 066: investigation / look-alikes / radical variants",
     "Batch 066: colleague / look-alikes / radical variants"),
    ("Compare 偵 with 貞, 停, 低 and 値. Inspect 人 versus 亻, 手 versus 扌 in 探, and both words 探偵 and 刑事. Shared fallback need not give four different designs.",
     "Compare 僚 with 療, 像 and 値. Inspect 人 versus 亻 and the illness frame 疒; also inspect 同, 口 and the word 同僚. Shared fallback need not give four different designs."),
    ("assertEquals(48, rows.length())", "assertEquals(40, rows.length())"),
    ('.put("individualGlyphProbes", 40).put("wholeWordRasterProbes", 8)',
     '.put("individualGlyphProbes", 36).put("wholeWordRasterProbes", 4)'),
    ("Forty single-character native Paint probes including actual 人/亻 and 手/扌, eight complete-word nonblank raster probes and four production Compose rows; actual 偵/貞/停/低/値/人/亻/探/手/扌/探偵/刑事 readability requires separate visual inspection.",
     "Thirty-six single-character native Paint probes including actual 人/亻 and standalone 疒, four complete-word nonblank raster probes and four production Compose rows; actual 僚/療/像/値/人/亻/疒/同/口/同僚 readability requires separate visual inspection."),
    ("investigation", "colleague"), ('"偵"', '"僚"'),
    ('listOf("テイ")', 'listOf("リョウ")'), ('listOf("てい")', 'listOf("りょう")'),
    ('key == "てい"', 'key == "りょう"'), ('val key = "てい"', 'val key = "りょう"'),
    ('"spy; covert colleague"', '"colleague"'),
    ('assertEquals(11, strokes.length())', 'assertEquals(14, strokes.length())'),
    ('"11 strokes drawn"', '"14 strokes drawn"'),
    ("Other N1 meanings/readings postponed; 偵 meaning and sole curated on key due; explicit no-kun. Two historical good 偵 meaning logs unlock drawing.",
     "Other N1 meanings/readings postponed; 僚 meaning and sole curated on key due; explicit no-kun. Two historical good 僚 meaning logs unlock drawing."),
)
for old, new in replacements:
    assert old in text, old
    text = text.replace(old, new)
start = text.index('            click("Browse all kanji")')
end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
route = r'''            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("僚")
            click("colleague")
            await("Article contents")
            await("as 亻, no. 9)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("僚 concerns a colleague or associate sharing work or a role", "kanji-meaning")
            show("It also appears with an official sense", "kanji-official-sense")
            show("Modern-shape mnemonic, not etymology:", "kanji-mnemonic")
            section("Readings")
            show(readingExample("同僚 どうりょう — coworker; colleague"), "kanji-on-reading")
            section("Notes")
            show(articleBullet("同僚 identifies a work relationship, not necessarily a personal friendship. Do not derive a rigid equal-rank requirement from 同."), "kanji-role-boundary")
            show(articleBullet("療 shares the elaborate right-hand shape but has the illness frame 疒 and concerns treatment or healing, not a colleague."), "kanji-healing-lookalike")
            show(articleBullet("像 and 値 also have 亻 on the left; inspect the different right-hand components rather than relying on the radical alone."), "kanji-other-lookalikes")
            section("Common words")
            show(articleBullet("官僚 かんりょう — bureaucrat; government official"), "kanji-common-official")
            inline(await(articleBullet("同僚 どうりょう — coworker; colleague")), "同僚")
            await("同僚 (どうりょう) - coworker; colleague")
            section("Meaning")
            show("同僚 is a noun for a coworker or colleague.", "coworker-meaning")
            show(articleBullet("同僚と昼ご飯を食べました。 (どうりょうとひるごはんをたべました。) - I had lunch with a colleague."), "coworker-lunch-example")
            show(articleBullet("困ったときは同僚に相談します。 (こまったときはどうりょうにそうだんします。) - When I have a problem, I consult a coworker."), "coworker-consult-example")
            show("The second example uses に for the person consulted.", "coworker-particle-plural")
            section("How the kanji combine")
            show("The on readings ドウ + リョウ give どうりょう.", "coworker-reading-allocation")
            inline(await("contributes sameness or sharing", substring = true), "僚")
            await("Article contents")
            section("Readings")
            show(readingExample("同僚 どうりょう — coworker; colleague"), "coworker-colleague-backlink")
            back()
            await("contributes sameness or sharing", substring = true).assertIsDisplayed()
            capture("system-back-coworker-colleague")
            inline(await("contributes sameness or sharing", substring = true), "同")
            await("同 — same, equal")
            await("Key (radical):", substring = true).performScrollTo().assertIsDisplayed()
            capture("same-radical")
            section("Meaning and origin")
            show("同 conveys sameness, equality, or agreement.", "same-meaning")
            show("Modern-shape mnemonic:", "same-mnemonic")
            section("Readings")
            show(readingExample("同時 どうじ — same time; 同意 どうい — agreement"), "same-on-reading")
            show(readingExample("同じ おなじ — same"), "same-kun-reading")
            section("Notes")
            show("Before an ordinary noun, use 同じ directly:", "same-attachment")
            show("Distinguish the outer frame", "same-lookalikes")
            section("Common words")
            show(articleBullet("同じ おなじ — same"), "same-common-same")
            show(articleBullet("同時 どうじ — same time; 同時に どうじに — simultaneously"), "same-common-time")
            show(articleBullet("同意 どうい — agreement; consent"), "same-common-agreement")
            inline(await(articleBullet("同僚 どうりょう — coworker; colleague")), "同僚")
            await("同僚 (どうりょう) - coworker; colleague")
            section("How the kanji combine")
            show("The on readings ドウ + リョウ give どうりょう.", "same-coworker-backlink")
            back()
            await(articleBullet("同僚 どうりょう — coworker; colleague")).assertIsDisplayed()
            capture("system-back-same-coworker")
            back()
            await("contributes sameness or sharing", substring = true).assertIsDisplayed()
            section("Synonyms and antonyms")
            show("仲間 (なかま) is a companion or member of the same group more broadly.", "coworker-companion-boundary")
            show("友人 (ゆうじん) is a friend", "coworker-friend-boundary")
            show("上司 (じょうし)", "coworker-superior-boundary")
            section("Distinctive meaning")
            show("同僚 presents someone as a fellow worker.", "coworker-rank-boundary")
            back()
            await("Common words")
'''
text = text[:start] + route + text[end:]
assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
assert "ContentParser.parse" not in text
for obsolete in ("064", "偵", "探偵", "刑事", "テイ", '"てい"', "investigation", "Comparison"):
    assert obsolete not in text, obsolete
assert text.count('listOf("リョウ")') == 4
assert 'assertEquals(14, strokes.length())' in text
documents = {name: blocks(ROOT / name) for name in ("kanji/僚.md", "words/同僚.md", "kanji/同.md")}
stack, selectors, controls, transitions = ["kanji/僚.md"], [], [], []
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
        elif line.strip() in ('click("Browse all kanji")', 'click("colleague")') or "performTextReplacement" in line:
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
        destinations = {posixpath.normpath(posixpath.join(posixpath.dirname(document), link))
                        for link in links if not link.startswith("https://")}
        assert len(destinations) == 1, (document, label, destinations)
        destination = destinations.pop()
        assert destination in documents
        transitions.append([document, destination])
        stack.append(destination)
assert stack == ["kanji/僚.md"]
expected_transitions = {
    ("kanji/僚.md", "words/同僚.md"), ("words/同僚.md", "kanji/僚.md"),
    ("words/同僚.md", "kanji/同.md"), ("kanji/同.md", "words/同僚.md"),
}
assert len(transitions) == 4 and {tuple(pair) for pair in transitions} == expected_transitions
archive = CONTROL / "artifacts" / "n1-batch-066-175fdf3f-envelope.zip"
assert not archive.exists()
subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-066/",
                f"--output={archive}", HEAD], cwd=ROOT, check=True)
with zipfile.ZipFile(archive) as zipped:
    names = zipped.namelist()
    prefix = "n1-batch-066/"
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
assert verified == 8326
FOLDER.mkdir()
fixture = FOLDER / "N1Batch066NativeTest.kt"
fixture.write_text(text, encoding="utf-8")
diff = FOLDER / "fixture-from-064.diff"
diff.write_text("".join(difflib.unified_diff(
    PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
    fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=fixture.relative_to(ROOT).as_posix(), n=0)), encoding="utf-8")
record = {
    "schemaVersion": 1, "execution": 426, "batch": "066",
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
    "plannedNativePaintProbes": 36, "plannedWholeWordRasterProbes": 4,
    "plannedGlyphs": ["僚", "療", "像", "値", "人", "亻", "疒", "同", "口"],
    "plannedWholeWords": ["同僚"],
    "fullReadings": {"on": ["リョウ"], "kun": []},
    "curatedReadings": {"on": ["リョウ"], "kun": []},
    "normalizedQuizKeys": {"on": ["りょう"], "kun": []},
    "reciprocalPairs": [["僚", "同僚"], ["同", "同僚"]],
    "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
    "accepted425AndroidRetainedWithoutRerun": True, "nativeExecuted": False,
    "independentVisualAcceptance": False, "phoneEvidence": False,
    "publicationAttempted": False, "runtimeEdited": False,
    "projectionQualification": "Bounded heading/paragraph/bullet/table projection reused from accepted064/065. Static selectors establish matching text and link destinations, not native semantics, viewport readability or visual acceptance.",
    "hostTestInitScriptUsed": False,
    "limits": "Preparation only. Exact full Git envelope and production ContentSync ONCE with unchanged guards. Both mapped pairs in four directions, complete three articles, selection/meaning/sole curated On/no Kun/14-stroke trace and recall planned, not executed. Paint hashes do not establish readable glyphs or fallback-face identity. Reference trace/recall miss do not establish human handwriting or MLKit recognition. Fresh device/port ownership required before separate native execution. Historical permission failures and HOST-only memory qualification remain intact; HOST init not for native builds. No native/reviewer/publication/067/second runner. Published92/1228,1136remain; phone/general-release/whole-set outstanding.",
}
(CONTROL / "batch-066-native-fixture-verification.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: record[key] for key in ("status", "contentVersion", "expectedCounts",
                 "archiveSha256", "zipEntries", "compressedBytes", "inflatedBytes",
                 "retainedBytes", "verifiedRuntimeHashes", "fixtureSha256", "captureSteps")}, indent=2))
print("Article selectors:", len(selectors), "Directed transitions:", len(transitions))
