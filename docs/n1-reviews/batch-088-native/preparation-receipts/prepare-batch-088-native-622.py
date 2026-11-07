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
L = C / "logs" / "c4ddd25a-3e57-43c1-8fc2-df82b6733b6c"
HEAD = "e445d826118681e1df9687eb53d144eed7d66139"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "afff40af0e155dbe"
WORK = C / "batch-088-native-622"
FIXTURE = WORK / "N1Batch088NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-087-native" / "N1Batch087NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-088-e445d826-envelope.zip"
VERIFICATION = C / "batch-088-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-088-native"
BEFORE = L / "progress-before-622.json"
NEXT = (
    "SAME088 execute compiled native fixture and inspect actual PNGs; preparation622 is NOT native acceptance. "
    "Read docs/n1-sources/execution-622.json and control/batch-088-native-fixture-verification.json. "
    "Require N1Batch088GlyphTest AND N1Batch088ArticleTest terminal per-case0, no skips/errors. "
    "Frozen full git archivee445d826/versionafff40af0e155dbe/8423runtimehashes through productionContentSync ONCE: "
    "1111kanji/5067words/120N1/zeroProblems/acceptedRoomversion+readingepoch1. "
    "Inspect all27scopedHan especially U+51E0/U+8C48/U+9B28 across fourproductionfamilies/systemfallback, "
    "108individual+4wholewordrasters and3Composepanels. Cmaps/hasGlyph/hashes are NOT legibility/face evidence. "
    "Actual N1/All production choices must be exactly target victorysong;triumph plus 凡commonplace;mediocre, "
    "凸convex;protruding, 凹concave;sunken, all3N1available/no fallback. "
    "Onequeuedonkeyがい persistedGood/done, explicitkun[] and source-onlyカイ/かちどき/やわらぐ unoffered; "
    "allrawreadings/order retained. Twelvestroke injectedtrace/recall/persistence, BOTHcompletearticles, "
    "onemappedpair/twodirections/fourdirectwordguards, SystemBack/offline/N1selection/meaning/reading/drawing. "
    "Injectedtrace/giveup is NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581 ownership "
    "immediately before ownedreadonlyAPI35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/2048MiB/2cores; "
    "stop only ownedhelper. No guest/appheap/guardincrease, productionappchange,089 or runtimepublication. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains unchangedproductionf9b59a2, not latestappmain. "
    "Original textualsnapshot42077c31 closed across Claude915d0745-fc54-49b0-99cf-49762fb5e16f and "
    "GPT11925f67-211b-497f-9d75-3d2802c178ab; serial original-session dependentvisualconfirmations remain, "
    "no newblindcredit. Parent19008 ownsrunner.lock: verifyliveancestry/session/checkpoint/exactsignedheads/"
    "whollycleanworktrees; NOchildlockacquisition/delete/unlock. Approvedcontrol/committedsources only, "
    "not optionalhistoricalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Alloriginalsource/baseline/link/reading/twofamily/native/currentmainnormalmerge/changedteachingindependentreview/"
    "combinedchecks/normalsigning/ownerfastforward/terminalCI/EVERYimmutablepublicZIPruntimehash/original18000entries/"
    "42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath/ownerissue gates remain. "
    "Published114/1228,1114remaining unchanged; physicalphone/generalrelease/whole-set outstanding; projectincomplete."
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
        assert not git("status", "--porcelain", root=root), str(root)
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)


def persist(state):
    temp = C / "progress.622.tmp"
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
    assert count == 8423
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-088-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    for name, digest in reconciliation["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        621, "continue", "fresh-android-passed-awaiting-native", "088")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    role = load(L / "native-runner-role.json")
    assert role["parentAncestryVerified"] and role["launcherCommandMatches"] and not role["parentLockAccessAttempted"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 621 and checkpoint["execution621CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution622StartingState"] = {
        "execution": 622, "batch": "088", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME088 full native fixture/archive preparation and compilation, signed LOCAL evidence; yield before native execution/visual review/publication/089.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete approved issue and final621 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry and exact runner session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-088-native-preparation-in-progress"
    state["nextAction"] = state["execution622StartingState"]["scope"]
    persist(state)
    print("Starting622 persisted; full live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(PRIOR) == "e1db2217f7d756c6c9d46455aef274e38e0cba57c92d3f40288aa7e9e1eeacd4"
    utility = C / "prepare-batch-085-native.py"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", utility)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    names = ["kanji/凱.md", "words/凱旋.md"]
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_622" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_622")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("凱")')
    line('click("victory song; triumph")')
    display("kanji/凱.md", "kanji")
    forward = follow("kanji/凱.md", "凱旋", "words/凱旋.md", "Common words", "return-forward")
    display("words/凱旋.md", "return")
    reverse = follow("words/凱旋.md", "凱", "kanji/凱.md", "How the kanji combine", "return-reverse")
    line('section("Readings")')
    line('show(readingExample("ガイ"), "return-kanji-backlink")')
    back_to(reverse, "return-system-back-to-word")
    back_to(forward, "return-system-back-to-kanji")
    assert len(offsets) == 2 and len({(x["document"], x["destination"]) for x in offsets}) == 2
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    begin = text.index("        val importedNoun = ")
    end = text.index("        val now = ", begin)
    text = text[:begin] + """        val importedReturn = requireNotNull(runBlocking { app.db.content().word(source.id, "凱旋") })
        assertEquals(listOf("帰る", "帰宅", "帰り", "戻る"), importedReturn.quizExclusions.splitSep())
        assertEquals("がいせん", importedReturn.reading)
        assertNull(importedReturn.jlpt)
""" + text[end:]
    begin = text.index('            if (poolName == "All") {')
    end = text.index("            checkedPools.put(", begin)
    text = text[:begin] + """            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            assertEquals(3, cards.count { it.kanji in target.distractors })
""" + text[end:]
    replacements = [
        ("N1Batch087", "N1Batch088"), ("disposable087", "disposable088"),
        ("n1-087", "n1-088"), ("Batch 087", "Batch 088"),
        ("n1-batch-087-404f507d-envelope.zip", ARCHIVE.name),
        ("404f507d5f9d3abe4e8bdc5e72bd41ea5607c521", HEAD),
        ("eb3a9413cccd4f57", VERSION), ("1110, updated.kanji", "1111, updated.kanji"),
        ("5066, updated.words", "5067, updated.words"), ("119, n1.size", "120, n1.size"),
        ("N1 · 119 cards", "N1 · 120 cards"),
        ("calmSeaLookalikesAndRadicalFallbacks", "triumphLookalikesAndRadicalFallbacks"),
        ("fullSingleImportOfflineCalmSeaTwoReciprocalPairsTwoKunKeysNoOnDrawingAndSystemBack",
         "fullSingleImportOfflineTriumphOneReciprocalPairOneOnKeyNoKunDrawingAndSystemBack"),
        ("val calmSea =", "val triumph ="), ("calmSea.", "triumph."),
        ('"凪"', '"凱"'), ("calm seas; lull", "victory song; triumph"),
        ('listOf("風", "凡", "凹")', 'listOf("凡", "凸", "凹")'),
        ('"風" to "wind; style"', '"凸" to "convex; protruding"'),
        ('emptyList<String>(), triumph.onyomi', 'listOf("ガイ", "カイ"), triumph.onyomi'),
        ('listOf("なぎ", "な.ぐ"), triumph.kunyomi', 'listOf("かちどき", "やわらぐ"), triumph.kunyomi'),
        ('emptyList<String>(), triumph.quizOnyomi', 'listOf("ガイ"), triumph.quizOnyomi'),
        ('listOf("なぎ", "な.ぐ"), triumph.quizKunyomi', 'emptyList<String>(), triumph.quizKunyomi'),
        ('emptyList<String>(), triumph.toReadingCard().quizKeys(ReadingKind.On)',
         'listOf("がい"), triumph.toReadingCard().quizKeys(ReadingKind.On)'),
        ('listOf("なぎ", "なぐ"), triumph.toReadingCard().quizKeys(ReadingKind.Kun)',
         'emptyList<String>(), triumph.toReadingCard().quizKeys(ReadingKind.Kun)'),
        ('emptyList<String>(), card.onyomi', 'listOf("ガイ", "カイ"), card.onyomi'),
        ('listOf("なぎ", "な.ぐ"), card.kunyomi', 'listOf("かちどき", "やわらぐ"), card.kunyomi'),
        ('emptyList<String>(), card.quizOnyomi', 'listOf("ガイ"), card.quizOnyomi'),
        ('listOf("なぎ", "な.ぐ"), card.quizKunyomi', 'emptyList<String>(), card.quizKunyomi'),
        ('setOf("なぎ", "なぐ")', 'setOf("がい")'),
        ("kind == ReadingKind.Kun && key", "kind == ReadingKind.On && key"),
        ("assertEquals(ReadingKind.Kun, question.question.kind)", "assertEquals(ReadingKind.On, question.question.kind)"),
        ("assertTrue(readingLogs.all { it.mode == ReadingKind.Kun.mode.name })",
         "assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })"),
        ("curated-two-kun-no-on-done", "curated-one-on-no-kun-done"),
        ("bothCuratedKunKeysPersistedGoodAndDone", "singleCuratedOnKeyPersistedGoodAndDone"),
        ('put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)',
         'put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2)'),
        ('put("completeArticleProjections", 3)', 'put("completeArticleProjections", 2)'),
        ("assertEquals(6, strokes.length())", "assertEquals(12, strokes.length())"),
        ('hasContentDescription("6 strokes drawn"', 'hasContentDescription("12 strokes drawn"'),
        ("kotlin.random.Random(613)", "kotlin.random.Random(622)"),
        ("importedNoun.quizExclusions.splitSep().size + importedVerb.quizExclusions.splitSep().size",
         "importedReturn.quizExclusions.splitSep().size"),
        ("assertEquals(1, meaning.options.count", "assertEquals(0, meaning.options.count"),
        ('put("actualN1CuratedAvailable", 2).put("actualN1FallbackOptions", 1)',
         'put("actualN1CuratedAvailable", 3).put("actualN1FallbackOptions", 0)'),
        ("repeat(2) {", "repeat(1) {"),
        ("assertEquals(2, done.answered)", "assertEquals(1, done.answered)"),
        ("assertEquals(2, done.correct)", "assertEquals(1, done.correct)"),
        ("assertEquals(2, readingLogs.size)", "assertEquals(1, readingLogs.size)"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 凱 meaning and exactly onがい due; explicit kun[] and unselectedカイ give no questions. Two historical good 凱 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    audit = load(R / "docs" / "n1-sources" / "batch-088-draft-font-audit.json")
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "".join(
        R.joinpath(*name.split("/")).read_text(encoding="utf-8") for name in names))))
    assert glyphs == audit["actualHan"] and len(glyphs) == 27
    words = ["凱旋"]
    pages = [" ".join(glyphs[:14]), " ".join(glyphs[14:]), "凱 几 豈 山 豆 鬨 凡 凸 凹 勝 歌 旋 凱旋"]
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", "for (word in listOf(" + ", ".join(map(quote, words)) + "))", text, count=1)
    text = text.replace("calm seas / look-alikes / radical fallback", "triumph / look-alikes / radical fallback")
    text = text.replace("all 21 scoped Han; focused 凪/風/止/凡/凹, 几", "all 27 scoped Han; focused 凱/凡/凸/凹 and 几/豈/鬨")
    text = text.replace("21 actual scoped Han including exact 几 fallback inspection", "27 actual scoped Han including exact 几/豈/鬨 fallback inspection")
    text = text.replace("assertEquals(92, rows.length())", "assertEquals(112, rows.length())")
    text = text.replace('put("individualGlyphProbes", 84).put("wholeWordRasterProbes", 8).put("panels", 2)',
                        'put("individualGlyphProbes", 108).put("wholeWordRasterProbes", 4).put("panels", 3)')
    text = text.replace("two bounded Compose panels and eight whole-word rasters", "three bounded Compose panels and four whole-word rasters")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ["087", "calmSea", "凪", "なぎ", "なぐ", "な.ぐ", "importedNoun", "importedVerb", "bothCuratedKun"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["几", "豈", "鬨"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1111, "words": 5067, "n1": 120}
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-088/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-088/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-088/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-088/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8423 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-087.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 622, "batch": "088", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": "42077c31b4462081eb6b2c171a907c7cae47192d",
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
        "completeArticleProjections": 2, "changedReusedScope": {}, "mappedReciprocalPairs": 1, "mappedDirectedTransitions": 2,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "plannedNativePaintProbes": 108, "plannedWholeWordRasterProbes": 4, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ガイ", "カイ"], "kun": ["かちどき", "やわらぐ"]},
        "curatedReadings": {"on": ["ガイ"], "kun": []}, "normalizedQuizKeys": {"on": ["がい"], "kun": []},
        "directWordExclusionPairs": 4, "pendingCmapAbsences": ["几", "豈", "鬨"],
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581], "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1/All choices required; three curated wrong cards available, no fallback needed. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. All original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    }
    save(VERIFICATION, record)
    print(json.dumps({key: record[key] for key in ["status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes"]}))


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-088-native-test.apk"
    app = C / "artifacts" / "n1-batch-088-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch088GlyphTest", "N1Batch088ArticleTest",
                     "fullSingleImportOfflineTriumphOneReciprocalPairOneOnKeyNoKunDrawingAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-622-native-compile.ps1", VERIFICATION,
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
    save(R / "docs" / "n1-sources" / "execution-622.json", {
        "schemaVersion": 1, "execution": 622, "batch": "088", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution622StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8423, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 114, "remainingAdditions": 1114, "nextAction": NEXT,
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
    assert all(n.startswith(("docs/n1-reviews/batch-088-native/", "docs/n1-sources/execution-622.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-088-native-622-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-088-native-622-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-622.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 621 and state["stage"] == "batch-088-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 622, "checkpoint": 622, "batch": "088",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-622.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8423,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 114, "remainingAdditions": 1114, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=622, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution622CoordinatorCheckpoint"] = checkpoint
    state["batch088NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    assert all(load(C / "progress.json")[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-622-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 622, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
