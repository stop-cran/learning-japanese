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
L = C / "logs" / "f0a40c46-f4cd-4679-80a6-3dbb3e18fc0e"
HEAD = "404f507d5f9d3abe4e8bdc5e72bd41ea5607c521"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "eb3a9413cccd4f57"
WORK = C / "batch-087-native-613"
FIXTURE = WORK / "N1Batch087NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-086-native" / "N1Batch086NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-087-404f507d-envelope.zip"
VERIFICATION = C / "batch-087-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-087-native"
BEFORE = L / "progress-before-613.json"
NEXT = (
    "SAME087 execute compiled native fixture and inspect actual PNGs; preparation613 is NOT native acceptance. "
    "Read docs/n1-sources/execution-613.json and control/batch-087-native-fixture-verification.json. "
    "Verify signed content archive404f507d/versioneb3a9413cccd4f57/8420runtimehashes and frozen fixture/app/testAPK hashes. "
    "Require BOTH N1Batch087GlyphTest and N1Batch087ArticleTest terminalcase0, no skips/errors. "
    "Full git archive through productionContentSyncONCE:1110kanji/5066words/119N1/zeroProblems/acceptedRoomepoch1. "
    "All21Han especially U+51E0 across fourproductionfamilies/systemfallback; 84individual+8wholewordrasters and2Composepanels "
    "require actual PNG inspection, not cmap/hasGlyph/hash certification. N1 has only凡/凹 curated, N4風 excluded; "
    "All has風/凡/凹. Actual seed613 and default N1 fallback meaning labels need semantic adjudication. "
    "Both queuedkunkeysなぎ/なぐ persistedGood/done, expliciton[] noquestions; rawkunなぎ/な.ぐ order retained. "
    "Sixstroke injectedtrace/recall/persistence, allthree newarticleprojections, tworeciprocalpairs/fourdirections, "
    "seven directwordguards, SystemBack/offline/N1selection/meaning/reading/drawing. Injectedtrace/giveup is NOT "
    "humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581 ownership immediately before ownedreadonlyAPI35 "
    "N3_Acceptance_20261029 emulator-5580, hostGPU/-Vulkan/2048MiB/2cores/explicitserial; stop only ownedhelper. "
    "No guest/appheap/guard increase, productionappchange,088 or runtimepublication. QualifiedTESTONLYAndroid1c1b7bf4 "
    "retains unchangedproductionf9b59a2, not latestappmain. Original textualsnapshotf6391022 closed across Claude2308e256-e5c9-494d-8e53-805f94ff6314 "
    "and GPTd08a2c70-c89c-4b1f-a38c-311b6245ad29; serial dependentvisualconfirmations remain, no newblindcredit. "
    "Modernweather凪ぐ versus feelings和ぐ/classicalforms preserved. Parent19008 ownsrunner.lock; verifyliveancestry/session/"
    "checkpoint/exactsignedheads/whollycleanworktrees; NOchildlockacquisition/delete/unlock. Approvedcontrol/committedsources "
    "only, not optionalhistoricalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Alloriginalsource/baseline/link/reading/twofamily/native/currentmainnormalmerge/changedteachingindependentreview/"
    "combinedchecks/normalsigning/ownerfastforward/terminalCI/EVERYimmutablepublicZIPruntimehash/original18000entries/"
    "42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath/ownerissue gates remain. "
    "Published113/1228,1115remaining unchanged; physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root), str(root)
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)


def persist(state):
    temp = C / "progress.613.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    m = load(R / "manifest.json")
    assert build_manifest(R) == m and m["contentVersion"] == VERSION
    count = 0
    for section, entries in m.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                p = R.joinpath(*name.split("/"))
                actual = sha(p) if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(p)
                assert actual == digest, name
                count += 1
    assert count == 8420
    rec = load(R / "docs" / "n1-reviews" / "batch-087-reconciliation.json")
    assert rec["textualReviewClosed"]
    for name, digest in rec["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return m


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        612, "continue", "fresh-android-passed-awaiting-native", "087")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    role = load(L / "native-runner-role.json")
    assert role["parentAncestryVerified"] and role["launcherCommandMatches"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["execution612CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution613StartingState"] = {
        "execution": 613, "batch": "087", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME087 full native fixture/archive preparation and compilation, signed LOCAL evidence; yield before execution/visual review/publication/088.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete approved issue and final612 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry and exact runner session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-087-native-preparation-in-progress"
    persist(state)
    print("Starting613 persisted; full live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    m = runtime()
    assert sha(PRIOR) == "6724db90edee1c1bb35f6d3fc2f8dd20a5b0fc00d548b37bb276c26e21e420ae"
    utility = C / "prepare-batch-085-native.py"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", utility)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    names = ["kanji/凪.md", "words/凪.md", "words/凪ぐ.md"]
    docs = {name: blocks(R.joinpath(*name.split("/"))) for name in names}
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
        body = (R.joinpath(*document.split("/"))).read_text(encoding="utf-8").split("---", 2)[2]
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_613" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_613")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("凪")')
    line('click("calm seas; lull")')
    display("kanji/凪.md", "kanji")
    for word, slug in [("凪", "noun"), ("凪ぐ", "verb")]:
        forward = follow("kanji/凪.md", word, f"words/{word}.md", "Common words", slug + "-forward")
        display(f"words/{word}.md", slug)
        reverse = follow(f"words/{word}.md", "凪", "kanji/凪.md", "How the kanji combine", slug + "-reverse")
        line('section("Readings")')
        line(f'show(readingExample("なぎ"), "{slug}-kanji-backlink")')
        back_to(reverse, slug + "-system-back-to-word")
        back_to(forward, slug + "-system-back-to-kanji")
    assert len(offsets) == 4 and len({(x["document"], x["destination"]) for x in offsets}) == 4
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    begin = text.index("        val importedLegend = ")
    end = text.index("        val now = ", begin)
    text = text[:begin] + """        val importedNoun = requireNotNull(runBlocking { app.db.content().word(source.id, "凪") })
        val importedVerb = requireNotNull(runBlocking { app.db.content().word(source.id, "凪ぐ") })
        assertEquals(listOf("穏やか", "静か"), importedNoun.quizExclusions.splitSep())
        assertEquals(listOf("静まる", "止む", "落ち着く", "穏やか", "静か"), importedVerb.quizExclusions.splitSep())
        assertEquals("なぎ", importedNoun.reading)
        assertEquals("なぐ", importedVerb.reading)
        assertNull(importedNoun.jlpt)
        assertNull(importedVerb.jlpt)
""" + text[end:]
    replacements = [
        ("N1Batch086", "N1Batch087"), ("disposable086", "disposable087"),
        ("n1-086", "n1-087"), ("Batch 086", "Batch 087"),
        ("n1-batch-086-6667318d-envelope.zip", ARCHIVE.name),
        ("6667318d9d5bdf8ec8c899db64395e2955612432", HEAD),
        ("86e8cb13aa72ecd0", VERSION), ("1109, updated.kanji", "1110, updated.kanji"),
        ("5064, updated.words", "5066, updated.words"), ("118, n1.size", "119, n1.size"),
        ("N1 · 118 cards", "N1 · 119 cards"),
        ("commonplaceLookalikesAndRadicalFallbacks", "calmSeaLookalikesAndRadicalFallbacks"),
        ("fullSingleImportOfflineCommonplaceSevenReciprocalPairsTwoOnKeysNoKunDrawingAndSystemBack",
         "fullSingleImportOfflineCalmSeaTwoReciprocalPairsTwoKunKeysNoOnDrawingAndSystemBack"),
        ("val commonplace =", "val calmSea ="), ("commonplace.", "calmSea."),
        ('"凡"', '"凪"'), ("commonplace; mediocre", "calm seas; lull"),
        ('listOf("丸", "九", "凹")', 'listOf("風", "凡", "凹")'),
        ('"丸" to "round; circle"', '"風" to "wind; style"'),
        ('"九" to "nine"', '"凡" to "commonplace; mediocre"'),
        ('setOf("凪", "凹")', 'setOf("凪", "凡", "凹")'),
        ('listOf("ボン", "ハン")', 'emptyList<String>()'),
        ('listOf("およ.そ", "おうよ.そ", "すべ.て")', 'listOf("なぎ", "な.ぐ")'),
        ('listOf("ぼん", "はん")', 'emptyList<String>()'),
        ('emptyList<String>(), calmSea.quizKunyomi', 'listOf("なぎ", "な.ぐ"), calmSea.quizKunyomi'),
        ('emptyList<String>(), calmSea.toReadingCard().quizKeys(ReadingKind.Kun)',
         'listOf("なぎ", "なぐ"), calmSea.toReadingCard().quizKeys(ReadingKind.Kun)'),
        ('emptyList<String>(), card.quizKunyomi', 'listOf("なぎ", "な.ぐ"), card.quizKunyomi'),
        ('setOf("ぼん", "はん")', 'setOf("なぎ", "なぐ")'),
        ("kind == ReadingKind.On && key", "kind == ReadingKind.Kun && key"),
        ("assertEquals(ReadingKind.On, question.question.kind)", "assertEquals(ReadingKind.Kun, question.question.kind)"),
        ("assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })",
         "assertTrue(readingLogs.all { it.mode == ReadingKind.Kun.mode.name })"),
        ("curated-two-on-no-kun-done", "curated-two-kun-no-on-done"),
        ("bothCuratedOnKeysPersistedGoodAndDone", "bothCuratedKunKeysPersistedGoodAndDone"),
        ('put("mappedReciprocalPairs", 7).put("directedLinkTransitions", 14)',
         'put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)'),
        ('put("completeArticleProjections", 2).put("changedReusedArticles", 6)',
         'put("completeArticleProjections", 3).put("changedReusedArticles", 0)'),
        ("assertEquals(3, strokes.length())", "assertEquals(6, strokes.length())"),
        ('hasContentDescription("3 strokes drawn"', 'hasContentDescription("6 strokes drawn"'),
        ("kotlin.random.Random(604)", "kotlin.random.Random(613)"),
        ('importedLegend.quizExclusions.splitSep().size',
         'importedNoun.quizExclusions.splitSep().size + importedVerb.quizExclusions.splitSep().size'),
        ("assertEquals(2, options.count", "assertEquals(1, options.count"),
        ("assertEquals(2, meaning.options.count", "assertEquals(1, meaning.options.count"),
        ('put("actualN1CuratedAvailable", 1).put("actualN1FallbackOptions", 2)',
         'put("actualN1CuratedAvailable", 2).put("actualN1FallbackOptions", 1)'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 凪 meaning and exactly kunなぎ/なぐ due; explicit on[] gives no questions. Two historical good 凪 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    audit = load(R / "docs" / "n1-sources" / "batch-087-draft-font-audit.json")
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "".join(
        R.joinpath(*n.split("/")).read_text(encoding="utf-8") for n in names))))
    assert glyphs == audit["actualHan"] and len(glyphs) == 21
    words = ["凪", "凪ぐ"]
    pages = [" ".join(glyphs), "凪 風 止 几 凡 凹 凪ぐ 朝凪 夕凪"]
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", "for (word in listOf(" + ", ".join(map(quote, words)) + "))", text, count=1)
    text = text.replace("commonplace / look-alikes / radical fallback", "calm seas / look-alikes / radical fallback")
    text = text.replace("all 31 scoped Han; focused 凡/丸/九/凹, 丶/几", "all 21 scoped Han; focused 凪/風/止/凡/凹, 几")
    text = text.replace("31 actual scoped Han including exact 丶/几 fallback inspection", "21 actual scoped Han including exact 几 fallback inspection")
    text = text.replace("assertEquals(140, rows.length())", "assertEquals(92, rows.length())")
    text = text.replace('put("individualGlyphProbes", 124).put("wholeWordRasterProbes", 16).put("panels", 3)',
                        'put("individualGlyphProbes", 84).put("wholeWordRasterProbes", 8).put("panels", 2)')
    text = text.replace("three bounded Compose panels and sixteen whole-word rasters", "two bounded Compose panels and eight whole-word rasters")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ["086", "commonplace.", "calmSea;", "ぼん", "はん", "およ", "おうよ", "すべ", "凡例", "importedLegend"]:
        assert stale not in text, stale
    assert all(quote(x["target"]) in text for x in selectors)
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        p = Path(entry["path"])
        assert sha(p) == entry["sha256"]
        with TTFont(p) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["几"]
        fonts.append({"path": str(p), "sha256": sha(p), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in m["files"]),
              "words": sum(n.startswith("words/") for n in m["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1110, "words": 5066, "n1": 119}
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-087/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-087/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = z.read("n1-batch-087/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == m
        retained, verified = len(raw), 0
        for section, group in m.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = z.read("n1-batch-087/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(i.file_size for i in z.infolist())
        assert verified == 8420 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-086.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 613, "batch": "087", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": "f6391022356073dd3e53437be30885f9a09857d9",
        "androidSnapshot": APP, "productionBaseline": PROD, "contentVersion": VERSION, "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "durableUtilityRecipe": str(utility), "durableUtilityRecipeSha256": sha(utility),
        "fixtureDiff": str(diff), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 3, "changedReusedScope": {}, "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "plannedNativePaintProbes": 84, "plannedWholeWordRasterProbes": 8, "currentFontAudit": fonts,
        "fullReadings": {"on": [], "kun": ["なぎ", "な.ぐ"]}, "curatedReadings": {"on": [], "kun": ["なぎ", "な.ぐ"]},
        "normalizedQuizKeys": {"on": [], "kun": ["なぎ", "なぐ"]}, "directWordExclusionPairs": 7,
        "pendingCmapAbsences": ["几"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Actual N1 default/seed613 fallback choices require adjudication. Full productionContentSyncONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. All original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    }
    save(VERIFICATION, record)
    print(json.dumps({k: record[k] for k in ["status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes"]}))


def record():
    clean()
    runtime()
    v = load(VERIFICATION)
    assert sha(FIXTURE) == v["fixtureSha256"] and sha(ARCHIVE) == v["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-087-native-test.apk"
    app = C / "artifacts" / "n1-batch-087-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as z:
        assert hashlib.sha256(z.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(z.read(n) for n in z.namelist() if n.endswith(".dex"))
        for name in ["N1Batch087GlyphTest", "N1Batch087ArticleTest",
                     "fullSingleImportOfflineCalmSeaTwoReciprocalPairsTwoKunKeysNoOnDrawingAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-613-native-compile.ps1", VERIFICATION,
               C / "prepare-batch-085-native.py", L / "native-runner-role.json",
               C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt",
               *[L / n for n in ["native-compile-command.json", "native-compile-start.txt",
                                 "native-compile-end.txt", "native-compile-exit.txt"]]]
    provenance = []
    for source in sources:
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    zipped = receipts / "native-compile.txt.gz"
    with zipped.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as compressor:
            compressor.write((L / "native-compile.txt").read_bytes())
    assert gzip.decompress(zipped.read_bytes()) == (L / "native-compile.txt").read_bytes()
    provenance.append({"archive": zipped.relative_to(R).as_posix(), "sha256": sha(zipped),
                       "sourceSha256": sha(L / "native-compile.txt"), "losslessGzipVerified": True})
    save(R / "docs" / "n1-sources" / "execution-613.json", {
        "schemaVersion": 1, "execution": 613, "batch": "087", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution613StartingState"], "fixtureVerification": v,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8420, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 113, "remainingAdditions": 1115, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; preserve as evidence, not source whitespace changes.",
    })
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-087-native/", "docs/n1-sources/execution-613.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-087-native-613-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-087-native-613-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-613.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 612 and state["stage"] == "batch-087-native-preparation-in-progress"
    assert all(state[k] == v for k, v in original.items() if k != "stage")
    checkpoint = {
        "schemaVersion": 1, "execution": 613, "checkpoint": 613, "batch": "087",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-613.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8420,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 113, "remainingAdditions": 1115, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=613, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution613CoordinatorCheckpoint"] = checkpoint
    state["batch087NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    assert all(load(C / "progress.json")[k] == v for k, v in original.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-613-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 613, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
