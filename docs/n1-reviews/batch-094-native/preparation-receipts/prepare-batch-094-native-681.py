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
L = C / "logs" / "d22b802a-279d-4983-8f48-57c9d81fb387"
HEAD = "18ad4bed3264a7c30e04cd60edbd85264a5b39d8"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "4089e881d605ce92c4c425d57816bc795605ded8"
VERSION = "eeae47753a460f72"
WORK = C / "batch-094-native-681"
FIXTURE = WORK / "N1Batch094NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-093-native" / "N1Batch093NativeTest.kt"
UTILITY = C / "prepare-batch-085-native.py"
ARCHIVE = C / "artifacts" / "n1-batch-094-18ad4bed-envelope.zip"
VERIFICATION = C / "batch-094-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-094-native"
BEFORE = L / "progress-before-681.json"
NEXT = (
    "SAME094 execute compiled native fixture and inspect actual PNGs next; preparation681 is NOT native acceptance. "
    "Read docs/n1-sources/execution-681.json and control/batch-094-native-fixture-verification.json. Require BOTH "
    "N1Batch094GlyphTest and N1Batch094ArticleTest terminal per-case0/no skips. Exact full archive18ad4bed/"
    "versioneeae47753a460f72/8438 runtime hashes through productionContentSync ONCE:1117kanji/5070words/"
    "126N1/zeroProblems/acceptedRoomversion+readingepoch1. Inspect all41Han across FOURproductionfont "
    "families/systemfallback, especially U+5202/U+65AB/U+6C35/U+961D;164individual+12wholewordPaint probes/"
    "FIVE bounded Compose panels. Cmap/hasGlyph/rasterhashes NOT legibility/fallbackface evidence. "
    "All productionchoices exactly shave;sharpen;pare vs 前/判/刑; actual N1 has ONLY刑 curated "
    "(前N5/判N3 excluded) plus TWO productionfallbacks. Inspect actual N1 UI and 16-seed N1/All/"
    "bounded-custom/random-subset builder records; fallback semantic acceptance remains OPEN, not waived. "
    "THREE newdirect word guards 削る/除く,削る/外す,削除/省く:actual imported full-source and "
    "bounded custom candidate pools/both directions/both target orientations/16 seeds, original exclusions retained. "
    "ONLY onさく/kunけずる offered/persistedGood/Done; full/Lite raw onサク/kunけず.る,はつ.る,そ.ぐ "
    "and explicit[サク]/[けず.る] retained. NINE pinned strokes injectedtrace/recall/persistence; "
    "FOUR complete article projections削/削る/削除/除, THREE allmapped reciprocalpairs/SIX directions, "
    "TWO activatedbaseline削 pairs; SystemBack/offline/N1selection/meaning/reading/drawing. "
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
    "perfile-media-safepath/ownerissue gates remain. Published120/1228,1108remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No095 or runtimepublication."
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
    temp = C / "progress.681.tmp"
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
    assert count == 8438
    review = load(R / "docs" / "n1-reviews" / "batch-094-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        680, "continue", "fresh-android-passed-awaiting-native", "094")
    runner, role = load(C / "runner.json"), load(L / "native-runner-role.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    assert role["parentAncestryVerified"] and role["launcherCommandMatches"] and not role["parentLockAccessAttempted"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 680 and checkpoint["execution680CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution681StartingState"] = {
        "execution": 681, "batch": "094", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME094 full native fixture/archive preparation and compilation, normally signed LOCAL evidence; yield before native execution/visual review/publication/095.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final680 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry/session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "devicePreflight": "adb devices empty; no local/remote5580/5581 connections. Recheck fresh ownership immediately before later native launch.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-094-native-preparation-in-progress"
    state["nextAction"] = state["execution681StartingState"]["scope"]
    persist(state)
    print("Starting681 persisted; full live history retained.")


def prepare():
    clean()
    resumed_preparation = WORK.exists()
    if resumed_preparation:
        assert VERIFICATION.exists() and ARCHIVE.exists()
        old = load(VERIFICATION)
        assert sha(ARCHIVE) == old["archiveSha256"] and sha(FIXTURE) == old["fixtureSha256"]
        assert not (WORK / "original-preexecution-assumptions.kt.txt").exists()
        shutil.copyfile(FIXTURE, WORK / "original-preexecution-assumptions.kt.txt")
        shutil.copyfile(VERIFICATION, WORK / "original-preexecution-verification.json")
    else:
        assert not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(UTILITY) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", UTILITY)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-094-draft-font-audit.json")
    names = audit["completeArticleScope"]
    assert names == ["kanji/削.md", "words/削る.md", "words/削除.md", "kanji/除.md"]
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_681" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_681")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("削")')
    line('click("shave; sharpen; pare")')
    display("kanji/削.md", "kanji")
    to_kezuru = follow("kanji/削.md", "削る", "words/削る.md", "Common words", "kezuru-forward")
    display("words/削る.md", "kezuru")
    from_kezuru = follow("words/削る.md", "削", "kanji/削.md", "How the kanji combine", "kezuru-reverse")
    line('section("Readings")')
    line('show(readingExample("けず.る"), "kezuru-kanji-backlink")')
    back_to(from_kezuru, "kezuru-system-back-to-word")
    back_to(to_kezuru, "kezuru-system-back-to-kanji")
    to_sakujo = follow("kanji/削.md", "削除", "words/削除.md", "Common words", "sakujo-forward")
    display("words/削除.md", "sakujo")
    from_sakujo = follow("words/削除.md", "削", "kanji/削.md", "How the kanji combine", "sakujo-saku-reverse")
    line('section("Readings")')
    line('show(readingExample("サク"), "saku-kanji-backlink")')
    back_to(from_sakujo, "saku-system-back-to-word")
    to_jo = follow("words/削除.md", "除", "kanji/除.md", "How the kanji combine", "sakujo-jo-reverse")
    display("kanji/除.md", "jo")
    from_jo = follow("kanji/除.md", "削除", "words/削除.md", "Common words", "jo-sakujo-forward")
    line('section("Meaning")')
    line('capture("jo-sakujo-backlink")')
    back_to(from_jo, "jo-system-back-to-kanji")
    back_to(to_jo, "jo-system-back-to-word")
    back_to(to_sakujo, "sakujo-system-back-to-kanji")
    plan = load(R / "docs" / "n1-sources" / "batch-094-progress.json")["proposedDirectedLinkPlan"]
    assert {(x["document"], x["destination"]) for x in offsets} == {(x["from"], x["to"]) for x in plan}
    assert len(offsets) == 6
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "N1_BATCH_094_ARTICLE_PROJECTION\n" + text[end:]
    begin = text.index("        val importedDetective =")
    end = text.index("        val now =", begin)
    text = text[:begin] + '''        val words = runBlocking { app.db.content().wordsLite(source.id) }.map { it.toCard() }
        val importedShave = words.single { it.word == "削る" }
        val importedDeletion = words.single { it.word == "削除" }
        assertEquals(listOf("切る", "減らす", "省く", "消す", "除く", "外す"), importedShave.quizExclusions)
        assertEquals(listOf("消す", "除く", "外す", "取る", "削る", "省く"), importedDeletion.quizExclusions)
        assertEquals("けずる", importedShave.reading)
        assertEquals("さくじょ", importedDeletion.reading)
        assertEquals(2, importedShave.jlpt)
        assertEquals(2, importedDeletion.jlpt)
        val directGuardChecks = JSONArray()
        val guardPairs = listOf("削る" to "除く", "削る" to "外す", "削除" to "省く")
        for ((leftId, rightId) in guardPairs) {
            val left = words.single { it.word == leftId }
            val right = words.single { it.word == rightId }
            assertTrue(right.word in left.quizExclusions)
            for ((target, excluded) in listOf(left to right, right to left)) {
                val custom = listOf(target, excluded) + words.filter {
                    it.word !in setOf(target.word, excluded.word) && it.title !in setOf(target.title, excluded.title) &&
                        it.word !in target.quizExclusions && target.word !in it.quizExclusions
                }.take(12)
                for ((poolName, pool) in listOf("All" to words, "boundedCustom" to custom)) {
                    for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
                        repeat(16) { seed ->
                            val options = WordQuizBuilder.options(target, pool, direction, kotlin.random.Random(seed))
                            assertEquals(4, options.size)
                            assertEquals(1, options.count { it.word == target.word })
                            assertFalse("Direct exclusion leaked", options.any { it.word == excluded.word })
                            directGuardChecks.put(JSONObject().put("target", target.word).put("excluded", excluded.word)
                                .put("pool", poolName).put("direction", direction.name).put("seed", seed)
                                .put("options", JSONArray().also { rows ->
                                    options.forEach { rows.put(JSONObject().put("word", it.word).put("label", it.label)) }
                                }))
                        }
                    }
                }
            }
        }
        assertEquals(384, directGuardChecks.length())
''' + text[end:]
    text = text.replace("import io.github.stopcran.kanji.core.srs.StudyMode",
                        "import io.github.stopcran.kanji.core.srs.StudyMode\n"
                        "import io.github.stopcran.kanji.core.words.WordDirection\n"
                        "import io.github.stopcran.kanji.core.words.WordQuizBuilder")
    replacements = [
        ("N1Batch093", "N1Batch094"), ("disposable093", "disposable094"), ("n1-093", "n1-094"),
        ("Batch 093", "Batch 094"), ("n1-batch-093-324b0bd9-envelope.zip", ARCHIVE.name),
        ("324b0bd95ba8c255d7f0bead0b3f7ba771fccacc", HEAD), ("bf4cc85592bb9727", VERSION),
        ("1116, updated.kanji", "1117, updated.kanji"), ("125, n1.size", "126, n1.size"),
        ("N1 · 125 cards", "N1 · 126 cards"),
        ("punishmentLookalikesAndScopedHan", "shavingLookalikesAndScopedHan"),
        ("fullSingleImportOfflinePunishmentReusedN3TwoReciprocalPairsOneOnNoKunSixStrokesAndSystemBack",
         "fullSingleImportOfflineShavingTwoReusedN2ThreeReciprocalPairsBothReadingsNineStrokesAndSystemBack"),
        ("val punishment =", "val shaving ="), ("punishment.", "shaving."),
        ("punishment / look-alikes", "shaving / look-alikes"),
        ('"刑"', '"削"'), ("criminal punishment", "shave; sharpen; pare"),
        ('listOf("乃", "凹", "凸")', 'listOf("前", "判", "刑")'),
        ('listOf("ケイ")', 'listOf("サク")'),
        ('emptyList<String>(), shaving.kunyomi.splitSep()', 'listOf("けず.る", "はつ.る", "そ.ぐ"), shaving.kunyomi.splitSep()'),
        ('emptyList<String>(), card.kunyomi.splitSep()', 'listOf("けず.る", "はつ.る", "そ.ぐ"), card.kunyomi.splitSep()'),
        ('emptyList<String>(), shaving.quizKunyomi?.splitSep()', 'listOf("けず.る"), shaving.quizKunyomi?.splitSep()'),
        ('emptyList<String>(), card.quizKunyomi?.splitSep()', 'listOf("けず.る"), card.quizKunyomi?.splitSep()'),
        ('listOf("けい")', 'listOf("さく")'),
        ('emptyList<String>(), shaving.toReadingCard().quizKeys(ReadingKind.Kun)',
         'listOf("けずる"), shaving.toReadingCard().quizKeys(ReadingKind.Kun)'),
        ('"凸" to "convex; protruding"', '"刑" to "criminal punishment"'),
        ('"乃" to "thereupon; possessive no"', '"前" to "front, before"'),
        ('"凹" to "concave; sunken"', '"判" to "judge; seal"'),
        ('it.kanji == "凹"', 'it.kanji == "判"'),
        ('(kind == ReadingKind.On && key == "けい")',
         '((kind == ReadingKind.On && key == "さく") || (kind == ReadingKind.Kun && key == "けずる"))'),
        ('put("mappedReciprocalPairs", 2)', 'put("mappedReciprocalPairs", 3)'),
        ('put("directedLinkTransitions", 4)', 'put("directedLinkTransitions", 6)'),
        ('put("activatedBaselinePairs", 1)', 'put("activatedBaselinePairs", 2)'),
        ('put("completeArticleProjections", 3)', 'put("completeArticleProjections", 4)'),
        ('put("changedReusedArticles", 2)', 'put("changedReusedArticles", 3)'),
        ("assertEquals(6, strokes.length())", "assertEquals(9, strokes.length())"),
        ('hasContentDescription("6 strokes drawn"', 'hasContentDescription("9 strokes drawn"'),
        ("kotlin.random.Random(671)", "kotlin.random.Random(681)"),
        ('put("onlyOnKeiNoKunPersistedGoodAndDone", true)', 'put("onlySakuAndKezuruBothKindsPersistedGoodAndDone", true)'),
        ('capture("curated-one-on-no-kun-done")', 'capture("curated-one-on-one-kun-done")'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = text.replace(
        '            .put("directWordGuardCount", importedDetective.quizExclusions.splitSep().size)\n'
        '            .put("directPoliceLabelGuards", policeGuards).put("inboundTanteiGuardPreserved", true)',
        '            .put("newDirectWordGuardPairs", 3).put("directGuardBuilderChecks", directGuardChecks)')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; only 削 meaning and onさく/kunけずる due. Full raw readings and explicit curation retained. Two historical good 削 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    text = text.replace("            repeat(1) {", "            repeat(2) {")
    text = text.replace("                assertEquals(ReadingKind.On, question.question.kind)\n", "")
    text = text.replace('key in setOf("けい")', 'key in setOf("さく", "けずる")')
    text = text.replace("                assertEquals(key, question.question.correctKey)",
                        '                assertEquals(if (key == "さく") ReadingKind.On else ReadingKind.Kun, question.question.kind)')
    text = text.replace('setOf("けい")', 'setOf("さく", "けずる")')
    text = text.replace("assertEquals(1, done.answered)", "assertEquals(2, done.answered)")
    text = text.replace("assertEquals(1, done.correct)", "assertEquals(2, done.correct)")
    text = text.replace("assertEquals(1, readingLogs.size)", "assertEquals(2, readingLogs.size)")
    text = text.replace("assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })",
                        "assertEquals(setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name), readingLogs.map { it.mode }.toSet())")
    begin = text.index("        val checkedPools = JSONObject()")
    end = text.index("        val words =", begin)
    text = text[:begin] + '''        assertEquals(n1.map { it.kanji }.toSet(),
            all.filter { "jlpt-n1" in it.tags.splitSep() }.map { it.kanji }.toSet())
        val curatedIds = listOf("前", "判", "刑")
        assertEquals(listOf("刑"), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(shaving, n1.single { it.kanji == "刑" }) +
            n1.filter { it.kanji !in setOf("削", "刑") }.shuffled(kotlin.random.Random(681)).take(12)
        val checkedPools = JSONArray()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all,
            "boundedCustom" to boundedCustom, "randomN1Subset" to randomSubset)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "削" }
            assertEquals(curatedIds, target.distractors)
            val available = curatedIds.filter { id -> cards.any { it.kanji == id } }
            val expectedAvailable = if (poolName == "N1" || poolName == "randomN1Subset") 1 else 3
            assertEquals(expectedAvailable, available.size)
            repeat(16) { seed ->
                val options = QuizBuilder.options(target, cards, kotlin.random.Random(seed))
                assertEquals(4, options.size)
                assertEquals(4, options.map { it.title }.toSet().size)
                assertEquals(1, options.count { it.kanji == target.kanji })
                assertTrue(options.all { option -> cards.any { it.kanji == option.kanji && it.title == option.title } })
                assertTrue(available.all { id -> options.any { it.kanji == id } })
                if (expectedAvailable == 3) assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
                checkedPools.put(JSONObject().put("pool", poolName).put("poolSize", pool.size).put("seed", seed)
                    .put("options", JSONArray().also { rows ->
                        options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                    }).put("availableCuratedCount", available.size)
                    .put("fallbackOptions", options.count { it.kanji != target.kanji && it.kanji !in available }))
            }
        }
        assertEquals(64, checkedPools.length())
''' + text[end:]
    begin = text.index("            val expectedMeanings = mapOf(", text.index("            val meaning ="))
    end = text.index('            capture("meaning-question")', begin)
    text = text[:begin] + '''            assertEquals(4, meaning.options.size)
            assertEquals(4, meaning.options.map { it.title }.toSet().size)
            assertEquals(1, meaning.options.count { it.kanji == "削" })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertEquals("criminal punishment", meaning.options.single { it.kanji == "刑" }.title)
            assertFalse(meaning.options.any { it.kanji in setOf("前", "判") })
            assertEquals("shave; sharpen; pare", meaning.options.single { it.kanji == "削" }.title)
            assertEquals(listOf("前", "判", "刑"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 1).put("actualN1FallbackOptions", 2)
                .put("meaningChoiceVisualAdjudicationRequired", true)
''' + text[end:]
    glyphs = audit["actualHan"]
    assert len(glyphs) == 41
    pages = [" ".join(glyphs[i:i + 12]) for i in range(0, len(glyphs), 12)]
    pages.append("削 消 肖 刀 刂 斫 氵 阜 阝 前 判 刑 削る 削除 削ぐ")
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", 'for (word in listOf("削る", "削除", "削ぐ"))', text, count=1)
    text = text.replace("all 46 scoped Han; focused 刑/形/型/刀/刂/彡/事/亅/乃/凹/凸",
                        "all 41 scoped Han; focused 削/消/肖/刀/刂/斫/氵/阜/阝/前/判/刑")
    text = text.replace("46 actual scoped Han; 亅/刂/彡 absent from all three bundled cmaps",
                        "41 actual scoped Han; 刂/斫/氵/阝 absent from all three bundled cmaps")
    text = text.replace("assertEquals(196, rows.length())", "assertEquals(176, rows.length())")
    text = text.replace('put("individualGlyphProbes", 184)', 'put("individualGlyphProbes", 164)')
    text = text.replace("N1_BATCH_094_ARTICLE_PROJECTION", "\n".join(lines))
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ["093", "importedDetective", "policeGuards", "けい", "ケイ", "punishment.", "乃", "凹", "凸", "亅", "彡"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    for name in ["前", "判", "刑"]:
        import yaml
        card = yaml.safe_load((R / "kanji" / (name + ".md")).read_text(encoding="utf-8").split("---", 2)[1])
        assert f'"{name}" to {quote(card["title"])}' in text, (name, card["title"])
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["刂", "斫", "氵", "阝"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1117, "words": 5070, "n1": 126}
    if not resumed_preparation:
        subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-094/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-094/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-094/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-094/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8438 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    if not resumed_preparation:
        WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-093.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 681, "batch": "094", "status": "prepared-not-executed",
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
        "completeArticleProjections": 4, "changedReusedScope": names[1:],
        "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6, "activatedBaselinePairs": 2,
        "plannedGlyphs": glyphs, "plannedWholeWords": ["削る", "削除", "削ぐ"], "plannedComposePanels": pages,
        "plannedNativePaintProbes": 164, "plannedWholeWordRasterProbes": 12, "currentFontAudit": fonts,
        "fullReadings": {"on": ["サク"], "kun": ["けず.る", "はつ.る", "そ.ぐ"]},
        "curatedReadings": {"on": ["サク"], "kun": ["けず.る"]},
        "normalizedQuizKeys": {"on": ["さく"], "kun": ["けずる"]}, "newDirectWordExclusionPairs": 3,
        "directGuardPlannedBuilderChecks": 384, "directGuardScopes": ["All", "boundedCustom"],
        "directGuardDirections": ["JpToEn", "EnToJp"], "directGuardBothTargetOrientations": True,
        "kanjiChoicePlannedChecks": 64,
        "kanjiChoicePools": ["N1", "All", "boundedCustom", "randomN1Subset"],
        "n1CuratedAvailable": ["刑"], "n1MissingCurated": ["前", "判"], "n1FallbackCount": 2,
        "allCuratedAvailable": ["前", "判", "刑"], "allFallbackCount": 0,
        "fallbackSemanticAcceptance": "OPEN pending actual imported/UI options and evidence-based original-session confirmations",
        "pendingCmapAbsences": ["刂", "斫", "氵", "阝"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. All has three curated wrong cards; exact N1 has only刑, since前N5/判N3 are excluded, so two production fallbacks are captured, NOT assumed wrong or accepted. Static first draft of fixture caught this scope mismatch before compilation; original preparation preserved. Three direct word guards tested through actual builder on imported words, not learner word-session UI. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. Original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen094 fixture and full archive; all8438 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-094-native-test.apk"
    app = C / "artifacts" / "n1-batch-094-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch094GlyphTest", "N1Batch094ArticleTest",
                     "fullSingleImportOfflineShavingTwoReusedN2ThreeReciprocalPairsBothReadingsNineStrokesAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-681-native-compile.ps1", VERIFICATION, UTILITY,
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
        "schemaVersion": 1, "execution": 681, "batch": "094", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution681StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8438, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; retained as evidence, not source whitespace changes.",
        "diagnostics": [
            "Optional Android .github/instructions directory does not exist; root instructions and DESIGN consulted. No permission denial.",
            "Only committed093 harness and approved control085 Markdown utilities used; no historical session-state helper access.",
            "First in-memory preparation assertion caught an overbroad variable rename consuming the source title; scoped variable replacements corrected before any fixture/archive write.",
            "Static generated-fixture inspection caught inherited three-curated assumption in exact N1:前N5/判N3 are outside N1. Corrected planned assertions to actual one-curated/two-fallback behavior; preserved original uncompiled preparation. No app/content change or acceptance waiver. Actual fallback labels and semantic review remain open."
        ],
    }
    save(R / "docs" / "n1-sources" / "execution-681.json", evidence)
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-094-native/", "docs/n1-sources/execution-681.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-094-native-681-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-094-native-681-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-681.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 680 and state["stage"] == "batch-094-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 681, "checkpoint": 681, "batch": "094",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-681.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8438,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=681, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution681CoordinatorCheckpoint"] = checkpoint
    state["batch094NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    assert all(load(C / "progress.json")[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-681-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 681, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
