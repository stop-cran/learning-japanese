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
L = C / "logs" / "a2ca0fc4-f3c8-43e0-9b34-cea693b5c919"
HEAD = "324b0bd95ba8c255d7f0bead0b3f7ba771fccacc"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "27663944c7217a19e7de2f363e1b31a5f13452b6"
VERSION = "bf4cc85592bb9727"
WORK = C / "batch-093-native-671"
FIXTURE = WORK / "N1Batch093NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-092-native" / "N1Batch092NativeTest.kt"
UTILITY = C / "prepare-batch-085-native.py"
ARCHIVE = C / "artifacts" / "n1-batch-093-324b0bd9-envelope.zip"
VERIFICATION = C / "batch-093-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-093-native"
BEFORE = L / "progress-before-671.json"
NEXT = (
    "SAME093 execute compiled native fixture and inspect actual PNGs next; preparation671 is NOT native acceptance. "
    "Read execution-671.json and control/batch-093-native-fixture-verification.json. Require BOTH "
    "N1Batch093GlyphTest and N1Batch093ArticleTest terminal per-case0/no skips. Exact full archive324b0bd9/"
    "versionbf4cc85592bb9727/8436 runtime hashes through productionContentSync ONCE:1116kanji/5070words/"
    "125N1/zeroProblems/acceptedRoomversion+readingepoch1. Inspect all46Han across FOURproductionfont "
    "families/systemfallback, especially U+4E85/U+5202/U+5F61;184individual+12wholewordPaint probes/"
    "FIVE bounded Compose panels. Cmap/hasGlyph/rasterhashes NOT legibility/fallbackface evidence. "
    "N1/All productionchoices exactly criminal punishment vs 乃/凹/凸, all3curatedwrongcards/no fallback. "
    "ONLY onけい offered/persistedGood/Done, NO kun keys; full/Lite raw onケイ/emptykun, "
    "explicit[ケイ]/[] retained. Whole-wordでか NOT constituentkun; outside-freezeギョウ distinguished. "
    "SIX pinned strokes injectedtrace/recall/persistence; THREE complete article projections, "
    "TWO allmapped reciprocalpairs/FOUR directions, ONE activatedbaseline刑/刑事 pair "
    "(NOT事/刑事); SystemBack/offline/N1selection/meaning/reading/drawing. ReusedN3刑事 identity/"
    "reading/title/level/inbound探偵guard preserved; componentlink/four DIRECT police-label guards only. "
    "事 reciprocal navigation only. Original GPT bookkeeping correction remains explicit. "
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
    "perfile-media-safepath/ownerissue gates remain. Published119/1228,1109remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No094 or runtimepublication."
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
    temp = C / "progress.671.tmp"
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
    assert count == 8436
    review = load(R / "docs" / "n1-reviews" / "batch-093-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        670, "continue", "fresh-android-passed-awaiting-native", "093")
    runner, role = load(C / "runner.json"), load(L / "native-runner-role.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    assert role["parentAncestryVerified"] and role["launcherCommandMatches"] and not role["parentLockAccessAttempted"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 670 and checkpoint["execution670CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution671StartingState"] = {
        "execution": 671, "batch": "093", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME093 full native fixture/archive preparation and compilation, normally signed LOCAL evidence; yield before native execution/visual review/publication/094.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final670 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry/session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "devicePreflight": "adb devices empty; no listeners on 5580 through 5590. Recheck fresh ownership immediately before later native launch.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-093-native-preparation-in-progress"
    state["nextAction"] = state["execution671StartingState"]["scope"]
    persist(state)
    print("Starting671 persisted; full live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(UTILITY) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", UTILITY)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-093-draft-font-audit.json")
    names = audit["completeArticleScope"]
    assert names == ["kanji/刑.md", "words/刑事.md", "kanji/事.md"]
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_671" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_671")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("刑")')
    line('click("criminal punishment")')
    display("kanji/刑.md", "kanji")
    forward = follow("kanji/刑.md", "刑事", "words/刑事.md", "Common words", "keiji-forward")
    display("words/刑事.md", "keiji")
    reverse = follow("words/刑事.md", "刑", "kanji/刑.md", "How the kanji combine", "keiji-kei-reverse")
    line('section("Readings")')
    line('show(readingExample("ケイ"), "kei-kanji-backlink")')
    back_to(reverse, "kei-system-back-to-word")
    to_ji = follow("words/刑事.md", "事", "kanji/事.md", "How the kanji combine", "keiji-ji-reverse")
    display("kanji/事.md", "ji")
    from_ji = follow("kanji/事.md", "刑事", "words/刑事.md", "Common words", "ji-keiji-forward")
    line('section("Meaning")')
    line('capture("ji-keiji-backlink")')
    back_to(from_ji, "ji-system-back-to-kanji")
    back_to(to_ji, "ji-system-back-to-word")
    back_to(forward, "keiji-system-back-to-kei")
    plan = load(R / "docs" / "n1-sources" / "batch-093-progress.json")["proposedDirectedLinkPlan"]
    assert {(x["document"], x["destination"]) for x in offsets} == {(x["from"], x["to"]) for x in plan}
    assert len(offsets) == 4
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "N1_BATCH_093_ARTICLE_PROJECTION\n" + text[end:]
    begin = text.index("        val importedMow =")
    end = text.index("        val now =", begin)
    text = text[:begin] + '''        val importedDetective = requireNotNull(runBlocking { app.db.content().word(source.id, "刑事") })
        assertEquals(listOf("警官", "警察", "巡査", "おまわりさん"), importedDetective.quizExclusions.splitSep())
        assertEquals("けいじ", importedDetective.reading)
        assertEquals(3, importedDetective.jlpt)
        assertEquals("police detective; criminal matters", importedDetective.title)
        val detective = requireNotNull(runBlocking { app.db.content().word(source.id, "探偵") })
        assertTrue("Existing inbound detective guard", "刑事" in detective.quizExclusions.splitSep())
        val policeGuards = JSONArray()
        for (id in importedDetective.quizExclusions.splitSep()) {
            val guard = requireNotNull(runBlocking { app.db.content().word(source.id, id) })
            assertNotEquals("Unusable direct guard", guard.word, importedDetective.word)
            policeGuards.put(JSONObject().put("word", guard.word).put("title", guard.title))
        }
''' + text[end:]
    replacements = [
        ("N1Batch092", "N1Batch093"), ("disposable092", "disposable093"), ("n1-092", "n1-093"),
        ("Batch 092", "Batch 093"), ("n1-batch-092-62c6d3e2-envelope.zip", ARCHIVE.name),
        ("62c6d3e29b87d89a2027bcb3d063081de23c4320", HEAD), ("8445a5717d080dcc", VERSION),
        ("1115, updated.kanji", "1116, updated.kanji"), ("124, n1.size", "125, n1.size"),
        ("N1 · 124 cards", "N1 · 125 cards"),
        ("mowLookalikesAndScopedHan", "punishmentLookalikesAndScopedHan"),
        ("fullSingleImportOfflineMowReusedN3ReciprocalPairOneKunNoOnFourStrokesAndSystemBack",
         "fullSingleImportOfflinePunishmentReusedN3TwoReciprocalPairsOneOnNoKunSixStrokesAndSystemBack"),
        ("val mow =", "val punishment ="), ("mow.", "punishment."), ("importedMow.", "importedDetective."),
        ('"刈"', '"刑"'), ("mow; reap", "criminal punishment"),
        ('listOf("ガイ", "カイ")', 'listOf("ケイ")'),
        ('listOf("か.る")', 'emptyList<String>()'),
        ('assertEquals(emptyList<String>(), punishment.quizOnyomi?.splitSep())',
         'assertEquals(listOf("ケイ"), punishment.quizOnyomi?.splitSep())'),
        ('assertEquals(emptyList<String>(), punishment.toReadingCard().quizKeys(ReadingKind.On))',
         'assertEquals(listOf("けい"), punishment.toReadingCard().quizKeys(ReadingKind.On))'),
        ('assertEquals(listOf("かる"), punishment.toReadingCard().quizKeys(ReadingKind.Kun))',
         'assertEquals(emptyList<String>(), punishment.toReadingCard().quizKeys(ReadingKind.Kun))'),
        ('assertEquals(emptyList<String>(), card.quizOnyomi?.splitSep())',
         'assertEquals(listOf("ケイ"), card.quizOnyomi?.splitSep())'),
        ("kind == ReadingKind.Kun", "kind == ReadingKind.On"),
        ("assertEquals(ReadingKind.Kun, question.question.kind)", "assertEquals(ReadingKind.On, question.question.kind)"),
        ("it.mode == ReadingKind.Kun.mode.name", "it.mode == ReadingKind.On.mode.name"),
        ('key == "かる"', 'key == "けい"'), ('setOf("かる")', 'setOf("けい")'),
        ('put("mappedReciprocalPairs", 1)', 'put("mappedReciprocalPairs", 2)'),
        ('put("directedLinkTransitions", 2)', 'put("directedLinkTransitions", 4)'),
        ('put("completeArticleProjections", 2)', 'put("completeArticleProjections", 3)'),
        ('put("changedReusedArticles", 1)', 'put("changedReusedArticles", 2)'),
        ("assertEquals(4, strokes.length())", "assertEquals(6, strokes.length())"),
        ('hasContentDescription("4 strokes drawn"', 'hasContentDescription("6 strokes drawn"'),
        ("kotlin.random.Random(662)", "kotlin.random.Random(671)"),
        ('put("onlyKunKaruNoOnPersistedGoodAndDone", true)', 'put("onlyOnKeiNoKunPersistedGoodAndDone", true)'),
        ('capture("curated-one-kun-no-on-done")', 'capture("curated-one-on-no-kun-done")'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = text.replace('.put("directWordGuardCount", importedDetective.quizExclusions.splitSep().size)',
                        '.put("directWordGuardCount", importedDetective.quizExclusions.splitSep().size)\n'
                        '            .put("directPoliceLabelGuards", policeGuards).put("inboundTanteiGuardPreserved", true)')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; only 刑 meaning and onけい due, no kun keys. Full raw ケイ/emptykun and explicit curation retained. Two historical good 刑 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    glyphs = audit["actualHan"]
    assert len(glyphs) == 46 and all(g in glyphs for g in ["亅", "刂", "彡"])
    pages = [" ".join(glyphs[i:i + 12]) for i in range(0, len(glyphs), 12)]
    pages.append("刑 形 型 刀 刂 彡 土 事 亅 乃 凹 凸 刑事 刑罰 刑法")
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", 'for (word in listOf("刑事", "刑罰", "刑法"))', text, count=1)
    text = text.replace("mow / look-alikes / scoped Han", "punishment / look-alikes / scoped Han")
    text = text.replace("all 16 scoped Han; focused 刈/切/刀/刂/乃/凹/凸",
                        "all 46 scoped Han; focused 刑/形/型/刀/刂/彡/事/亅/乃/凹/凸")
    text = text.replace("16 actual scoped Han; 刂 absent from all three bundled cmaps",
                        "46 actual scoped Han; 亅/刂/彡 absent from all three bundled cmaps")
    text = text.replace("three bounded Compose panels and four whole-word rasters",
                        "five bounded Compose panels and twelve whole-word rasters")
    text = text.replace("assertEquals(68, rows.length())", "assertEquals(196, rows.length())")
    text = text.replace('put("individualGlyphProbes", 64)', 'put("individualGlyphProbes", 184)')
    text = text.replace('put("wholeWordRasterProbes", 4).put("panels", 3)',
                        'put("wholeWordRasterProbes", 12).put("panels", 5)')
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ["092", "mow.", "importedMow", "ガイ", "カイ", "かる", "刈", "刈除", "ReadingKind.Kun, question", "onlyKun"]:
        assert stale not in text, stale
    text = text.replace("N1_BATCH_093_ARTICLE_PROJECTION", "\n".join(lines))
    assert all(quote(item["target"]) in text for item in selectors)
    assert text.count('assertEquals(listOf("ケイ"),') == 4
    assert 'assertEquals(listOf("けい"), punishment.toReadingCard().quizKeys(ReadingKind.On))' in text
    assert 'assertEquals(emptyList<String>(), punishment.toReadingCard().quizKeys(ReadingKind.Kun))' in text
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["亅", "刂", "彡"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1116, "words": 5070, "n1": 125}
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-093/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-093/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-093/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-093/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8436 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-092.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 671, "batch": "093", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "androidSnapshot": APP, "productionBaseline": PROD, "contentVersion": VERSION, "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "durableUtilityRecipe": str(UTILITY), "durableUtilityRecipeSha256": sha(UTILITY),
        "fixtureDiff": str(diff), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 3, "changedReusedScope": ["words/刑事.md", "kanji/事.md"],
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4, "activatedBaselinePairs": 1,
        "plannedGlyphs": glyphs, "plannedWholeWords": ["刑事", "刑罰", "刑法"], "plannedComposePanels": pages,
        "plannedNativePaintProbes": 184, "plannedWholeWordRasterProbes": 12, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ケイ"], "kun": []}, "curatedReadings": {"on": ["ケイ"], "kun": []},
        "normalizedQuizKeys": {"on": ["けい"], "kun": []}, "directWordExclusionPairs": 4,
        "pendingCmapAbsences": ["亅", "刂", "彡"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1/All choices required; three curated wrong cards available, no fallback needed. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. Original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    wrapper = (C / "run-662-native-compile.ps1").read_text(encoding="utf-8-sig")
    for old, new in [
        ("031a6444-1ac9-421a-ac49-dd154997a82b", L.name), ("661", "670"), ("092", "093")
    ]:
        assert old in wrapper
        wrapper = wrapper.replace(old, new)
    (C / "run-671-native-compile.ps1").write_text(wrapper, encoding="utf-8")
    print("Prepared frozen093 fixture and full archive; all8436 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-093-native-test.apk"
    app = C / "artifacts" / "n1-batch-093-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch093GlyphTest", "N1Batch093ArticleTest",
                     "fullSingleImportOfflinePunishmentReusedN3TwoReciprocalPairsOneOnNoKunSixStrokesAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-671-native-compile.ps1", VERIFICATION, UTILITY,
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
        "schemaVersion": 1, "execution": 671, "batch": "093", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution671StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8436, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 119, "remainingAdditions": 1109, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; retained as evidence, not source whitespace changes.",
    }
    save(R / "docs" / "n1-sources" / "execution-671.json", evidence)
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-093-native/", "docs/n1-sources/execution-671.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-093-native-671-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-093-native-671-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-671.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 670 and state["stage"] == "batch-093-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 671, "checkpoint": 671, "batch": "093",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-671.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8436,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 119, "remainingAdditions": 1109, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=671, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution671CoordinatorCheckpoint"] = checkpoint
    state["batch093NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    assert all(load(C / "progress.json")[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-671-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 671, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
