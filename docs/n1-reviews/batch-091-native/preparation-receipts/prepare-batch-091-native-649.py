import copy
import difflib
import gzip
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "734088c1-c57b-4b51-9ff4-c0fe2a71fe83"
HEAD = "f6b2ee397b4e2998abcef6fd747b25d6178b1fa3"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "c2a59d5c1cd4ac8040156a6c067bd9d565d59116"
VERSION = "cb3c857f3614485d"
WORK = C / "batch-091-native-649"
FIXTURE = WORK / "N1Batch091NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-090-native" / "N1Batch090NativeTest.kt"
ONE_KIND = R / "docs" / "n1-reviews" / "batch-089-native" / "N1Batch089NativeTest.kt"
UTILITY = C / "prepare-batch-085-native.py"
ARCHIVE = C / "artifacts" / "n1-batch-091-f6b2ee39-envelope.zip"
VERIFICATION = C / "batch-091-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-091-native"
BEFORE = L / "progress-before-649.json"
NEXT = (
    "SAME091 execute compiled native fixture and inspect PNGs; preparation649 is NOT native acceptance. "
    "Read execution-649.json and control/batch-091-native-fixture-verification.json. Require BOTH "
    "N1Batch091GlyphTest and N1Batch091ArticleTest terminal per-case0/no skips. Exact full archivef6b2ee39/"
    "versioncb3c857f3614485d/8432runtimehashes through productionContentSync ONCE:1114kanji/5070words/"
    "123N1/zeroProblems/acceptedRoomversion+readingepoch1. Inspect all21Han across FOURproductionfont "
    "families/systemfallback, especially U+4E36;84individual+4wholewordPaint probes and3Composepanels. "
    "Cmap/hasGlyph/rasterhashes NOT legibility/fallbackface evidence. N1/All productionchoices exactly "
    "blade;cuttingedge vs 乃/凹/凸, all3curatedwrongcards/no fallback. ONLY kunは offered/persistedGood/Done, "
    "NO on keys; full/Lite raw onジン,ニン and kunは,やいば,き.る/sourceorder retained. Recognition "
    "on/yaiba not sourceonly/uniformlyrare; kiru sourceonly/no fabricatedspelling. THREEpinnedstrokes "
    "injectedtrace/recall/persistence; BOTHcompletearticles/ONEallmappedpair/TWOdirections, "
    "先端foregroundroute/SystemBack/offline/N1selection/meaning/reading/drawing. FIVE directwordguards "
    "including先端; physicalpartnoun/neutraltranslations/shapemnemonic/physical-vs-figurativeEnglishcontrast. "
    "Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581ownership "
    "immediately before ownedreadonlyAPI35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/"
    "2048MiB/2cores; stop only ownedhelper. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, "
    "NOT latestappmain. Originaltwofamilytextualreview/limits inherited; reuse originalsessions for serial "
    "dependentvisualconfirmation, no newblindcredit. Parent19008 retains runner.lock; verifyliveancestry/"
    "session/checkpoint/exactsignedheads/whollyclean, NOchildreacquisition/delete/unlock. Approvedcontrol/"
    "committedpackets only, NOT optionalhistoricalsessionrecipes. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. All originalsource/baseline/link/reading/twofamily/native/currentmain"
    "normalmerge/changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIPruntimehash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/ownerissue gates remain. Published117/1228,1111remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No092 or runtimepublication."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root), str(root)
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)


def persist(state):
    temp = C / "progress.649.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest and manifest["contentVersion"] == VERSION
    count = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                path = R.joinpath(*name.split("/"))
                actual = sha(path) if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(path)
                assert actual == digest, name
                count += 1
    assert count == 8432
    review = load(R / "docs" / "n1-reviews" / "batch-091-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        648, "continue", "fresh-android-passed-awaiting-native", "091")
    runner, role = load(C / "runner.json"), load(L / "native-runner-role.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    assert role["parentAncestryVerified"] and role["launcherCommandMatches"] and not role["parentLockAccessAttempted"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 648 and checkpoint["execution648CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution649StartingState"] = {
        "execution": 649, "batch": "091", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME091 full native fixture/archive preparation and compilation, normally signed LOCAL evidence; yield before native execution/visual review/publication/092.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final648 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry/session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-091-native-preparation-in-progress"
    state["nextAction"] = state["execution649StartingState"]["scope"]
    persist(state)
    print("Starting649 persisted; full live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(UTILITY) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", UTILITY)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-091-reviewed-font-audit-647.json")
    names = audit["scope"]
    assert names == ["kanji/刃.md", "words/刃.md"]
    docs = {name: blocks(R.joinpath(*name.split("/"))) for name in names + ["words/先端.md"]}
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def show(document, kind, value, step):
        assert sum(v == value for k, v in docs[document]
                   if (k == "table") == (kind == "table") and k != "heading") == 1, (document, value)
        selector = "readingExample" if kind == "table" else "articleBullet"
        line(f"show({selector}({quote(value)}), {quote(step)})")
        selectors.append({"document": document, "kind": kind, "target": value, "step": step})

    def display(document, slug):
        line(f"await({quote(docs[document][0][1])})")
        cell = 0
        for index, (kind, value) in enumerate(docs[document][1:], 1):
            if kind == "heading":
                line(f"section({quote(value)})")
            elif kind == "table":
                cell += 1
                if cell > 3 and cell % 3 != 2:
                    show(document, kind, value, f"{slug}-{index:02}")
            else:
                show(document, kind, value, f"{slug}-{index:02}")

    def follow(document, label, destination, section, step):
        body = R.joinpath(*document.split("/")).read_text(encoding="utf-8").split("---", 2)[2]
        sections = re.split(r"^## (.+)\n", body, flags=re.M)
        candidates = []
        for index in range(1, len(sections), 2):
            if sections[index] == section:
                for part in re.split(r"\n\s*\n|\n(?=- )", sections[index + 1].strip()):
                    for match in re.finditer(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", part):
                        if (R / document).parent.joinpath(match[1]).resolve() == (R / destination).resolve():
                            candidates.append(part.removeprefix("- "))
        assert len(candidates) == 1, (document, label, candidates)
        raw = candidates[0]
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        rendered = plain(" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_649" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_649")
        assert rendered[offset:].startswith(label)
        line(f"section({quote(section)})")
        show(document, "paragraph", rendered, step)
        line(f"inline(await(articleBullet({quote(rendered)})), {quote(label)}, {offset})")
        line('await("Article contents")')
        item = {"document": document, "destination": destination, "label": label,
                "section": section, "renderedText": rendered, "offset": offset}
        offsets.append(item)
        return item

    def back_to(item, step):
        line("back()")
        line(f"await(articleBullet({quote(item['renderedText'])})).assertIsDisplayed()")
        line(f"section({quote(item['section'])})")
        line(f"capture({quote(step)})")

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("刃")')
    line('click("blade; cutting edge")')
    display("kanji/刃.md", "kanji")
    forward = follow("kanji/刃.md", "刃", "words/刃.md", "Common words", "blade-forward")
    display("words/刃.md", "blade")
    reverse = follow("words/刃.md", "刃", "kanji/刃.md", "How the kanji combine", "blade-reverse")
    line('section("Readings")')
    line('show(readingExample("は"), "blade-kanji-backlink")')
    back_to(reverse, "blade-system-back-to-word")
    forefront = follow("words/刃.md", "先端", "words/先端.md", "Distinctive meaning", "forefront-forward")
    line(f"await({quote(docs['words/先端.md'][0][1])})")
    line('capture("forefront-destination")')
    back_to(forefront, "forefront-system-back-to-word")
    back_to(forward, "blade-system-back-to-kanji")
    plan = load(R / "docs" / "n1-sources" / "batch-091-progress.json")["proposedDirectedLinkPlan"]
    mapped = [x for x in offsets if x["destination"] != "words/先端.md"]
    assert {(x["document"], x["destination"]) for x in mapped} == {(x["from"], x["to"]) for x in plan}
    assert len(mapped) == 2 and len(offsets) == 3
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "N1_BATCH_091_ARTICLE_PROJECTION\n" + text[end:]
    begin = text.index("            val answeredKinds =")
    end = text.index('            back()\n            await("Meaning quiz")', begin)
    single = ONE_KIND.read_text(encoding="utf-8")
    left = single.index("            val answeredKeys =")
    right = single.index('            back()\n            await("Meaning quiz")', left)
    single = single[left:right].replace("凶", "刃").replace("きょう", "は")
    single = single.replace("ReadingKind.On, question.question.kind", "ReadingKind.Kun, question.question.kind")
    single = single.replace("it.mode == ReadingKind.On.mode.name", "it.mode == ReadingKind.Kun.mode.name")
    single = single.replace("curated-one-on-no-kun-done", "curated-one-kun-no-on-done")
    text = text[:begin] + single + text[end:]
    begin = text.index('        val importedSword =')
    end = text.index('        val now =', begin)
    text = text[:begin] + '''        val importedBlade = requireNotNull(runBlocking { app.db.content().word(source.id, "刃") })
        assertEquals(listOf("刀", "日本刀", "端", "縁", "先端"), importedBlade.quizExclusions.splitSep())
        assertEquals("は", importedBlade.reading)
        assertNull(importedBlade.jlpt)
''' + text[end:]
    replacements = [
        ("N1Batch090", "N1Batch091"), ("disposable090", "disposable091"), ("n1-090", "n1-091"),
        ("Batch 090", "Batch 091"), ("n1-batch-090-40bc5a55-envelope.zip", ARCHIVE.name),
        ("40bc5a5533bce9f9a1fcb460fd220110fb30dade", HEAD), ("ceee0f79a6d394df", VERSION),
        ("1113, updated.kanji", "1114, updated.kanji"), ("5069, updated.words", "5070, updated.words"),
        ("122, n1.size", "123, n1.size"), ("N1 · 122 cards", "N1 · 123 cards"),
        ("swordLookalikesAndScopedHan", "bladeLookalikesAndScopedHan"),
        ("fullSingleImportOfflineSwordFiveReciprocalPairsBothReadingKindsDrawingAndSystemBack",
         "fullSingleImportOfflineBladeReciprocalPairOneKunNoOnDrawingForefrontAndSystemBack"),
        ("val sword =", "val blade ="), ("sword.", "blade."), ("importedSword.", "importedBlade."),
        ('"刀"', '"刃"'), ("sword; blade", "blade; cutting edge"),
        ('listOf("トウ"), blade.onyomi.splitSep()', 'listOf("ジン", "ニン"), blade.onyomi.splitSep()'),
        ('listOf("トウ"), card.onyomi.splitSep()', 'listOf("ジン", "ニン"), card.onyomi.splitSep()'),
        ('listOf("かたな", "そり")', 'listOf("は", "やいば", "き.る")'),
        ('listOf("トウ"), blade.quizOnyomi?', 'emptyList<String>(), blade.quizOnyomi?'),
        ('listOf("トウ"), card.quizOnyomi?', 'emptyList<String>(), card.quizOnyomi?'),
        ('listOf("かたな")', 'listOf("は")'),
        ('listOf("とう"), blade.toReadingCard().quizKeys(ReadingKind.On)',
         'emptyList<String>(), blade.toReadingCard().quizKeys(ReadingKind.On)'),
        ('put("mappedReciprocalPairs", 5).put("directedLinkTransitions", 10)',
         'put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2).put("extraForefrontTransition", true)'),
        ('put("changedReusedArticles", 4)', 'put("changedReusedArticles", 0)'),
        ("assertEquals(2, strokes.length())", "assertEquals(3, strokes.length())"),
        ('hasContentDescription("2 strokes drawn"', 'hasContentDescription("3 strokes drawn"'),
        ("kotlin.random.Random(640)", "kotlin.random.Random(649)"),
        ('(kind == ReadingKind.On && key == "とう" || kind == ReadingKind.Kun && key == "かたな")',
         '(kind == ReadingKind.Kun && key == "は")'),
        ('put("bothCuratedKindsPersistedGoodAndDone", true)', 'put("onlyKunHaNoOnPersistedGoodAndDone", true)'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = text.replace('assertEquals(listOf("刃", "日本刀", "端", "縁", "先端"), importedBlade.quizExclusions.splitSep())',
                        'assertEquals(listOf("刀", "日本刀", "端", "縁", "先端"), importedBlade.quizExclusions.splitSep())')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; only 刃 meaning and kunは due, no on keys. All five raw readings retained. Two historical good 刃 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    glyphs = audit["actualHan"]
    assert len(glyphs) == 21 and "丶" in glyphs
    pages = [" ".join(glyphs[:12]), " ".join(glyphs[12:]), "刃 刀 丶 乃 凹 凸 丁 包 先 端 刃物"]
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", 'for (word in listOf("刃物"))', text, count=1)
    text = text.replace("sword / look-alikes / scoped Han", "blade / look-alikes / scoped Han")
    text = text.replace("all 18 scoped Han; focused 刀/力/乃/凹/凸 and 日本刀",
                        "all 21 scoped Han; focused 刃/刀/丶/乃/凹/凸 and 先/端")
    text = text.replace("18 actual scoped Han; all main-font cmaps cover these, native readability still requires inspection",
                        "21 actual scoped Han; 丶 absent from all three bundled cmaps requires actual system fallback inspection")
    text = text.replace("assertEquals(76, rows.length())", "assertEquals(88, rows.length())")
    text = text.replace('put("individualGlyphProbes", 72)', 'put("individualGlyphProbes", 84)')
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ["090", "089", "sword.", "importedSword", "そり", "トウ", "凶", "きょう", "repeat(2)"]:
        assert stale not in text, stale
    text = text.replace("N1_BATCH_091_ARTICLE_PROJECTION", "\n".join(lines))
    assert all(quote(item["target"]) in text for item in selectors)
    assert text.count('listOf("ジン", "ニン")') == 2
    assert text.count('listOf("は", "やいば", "き.る")') == 2
    assert 'assertEquals(emptyList<String>(), blade.toReadingCard().quizKeys(ReadingKind.On))' in text
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["丶"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1114, "words": 5070, "n1": 123}
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-091/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-091/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-091/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-091/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8432 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-090.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 649, "batch": "091", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "androidSnapshot": APP, "productionBaseline": PROD, "contentVersion": VERSION, "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "oneReadingKindHarness": ONE_KIND.relative_to(R).as_posix(), "oneReadingKindHarnessSha256": sha(ONE_KIND),
        "durableUtilityRecipe": str(UTILITY), "durableUtilityRecipeSha256": sha(UTILITY),
        "fixtureDiff": str(diff), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 2, "changedReusedScope": [],
        "mappedReciprocalPairs": 1, "mappedDirectedTransitions": 2, "extraForefrontTransition": True,
        "plannedGlyphs": glyphs, "plannedWholeWords": ["刃物"], "plannedComposePanels": pages,
        "plannedNativePaintProbes": 84, "plannedWholeWordRasterProbes": 4, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ジン", "ニン"], "kun": ["は", "やいば", "き.る"]},
        "curatedReadings": {"on": [], "kun": ["は"]},
        "normalizedQuizKeys": {"on": [], "kun": ["は"]}, "directWordExclusionPairs": 5,
        "pendingCmapAbsences": ["丶"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1/All choices required; three curated wrong cards available, no fallback needed. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. Original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen091 fixture and full archive; all8432 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-091-native-test.apk"
    app = C / "artifacts" / "n1-batch-091-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch091GlyphTest", "N1Batch091ArticleTest",
                     "fullSingleImportOfflineBladeReciprocalPairOneKunNoOnDrawingForefrontAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-649-native-compile.ps1", VERIFICATION, UTILITY,
               L / "native-runner-role.json", C / "runner-lock-role-notes.txt",
               C / "authoring-artifact-path-notes.txt",
               *[L / n for n in ["native-compile-command.json", "native-compile-start.txt",
                                 "native-compile-end.txt", "native-compile-exit.txt"]]]
    provenance = []
    for source in sources:
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    zipped = receipts / "native-compile.txt.gz"
    zipped.write_bytes(gzip.compress((L / "native-compile.txt").read_bytes(), mtime=0))
    assert gzip.decompress(zipped.read_bytes()) == (L / "native-compile.txt").read_bytes()
    provenance.append({"archive": zipped.relative_to(R).as_posix(), "sha256": sha(zipped),
                       "sourceSha256": sha(L / "native-compile.txt"), "losslessGzipVerified": True})
    evidence = {
        "schemaVersion": 1, "execution": 649, "batch": "091", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution649StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8432, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; retained as evidence, not source whitespace changes.",
    }
    save(R / "docs" / "n1-sources" / "execution-649.json", evidence)
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-091-native/", "docs/n1-sources/execution-649.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-091-native-649-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-091-native-649-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-649.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 648 and state["stage"] == "batch-091-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 649, "checkpoint": 649, "batch": "091",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-649.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8432,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=649, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution649CoordinatorCheckpoint"] = checkpoint
    state["batch091NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    assert all(load(C / "progress.json")[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-649-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 649, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
