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
L = C / "logs" / "285e1858-47ae-41c1-a157-6cc962fcb72f"
HEAD = "40bc5a5533bce9f9a1fcb460fd220110fb30dade"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "ceee0f79a6d394df"
WORK = C / "batch-090-native-640"
FIXTURE = WORK / "N1Batch090NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-089-native" / "N1Batch089NativeTest.kt"
TWO_KINDS = R / "docs" / "n1-reviews" / "batch-085-native" / "N1Batch085NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-090-40bc5a55-envelope.zip"
VERIFICATION = C / "batch-090-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-090-native"
BEFORE = L / "progress-before-640.json"
NEXT = (
    "SAME090 execute compiled native fixture and inspect actual PNGs next; preparation640 is NOT native acceptance. "
    "Read docs/n1-sources/execution-640.json and control/batch-090-native-fixture-verification.json. "
    "Require N1Batch090GlyphTest AND N1Batch090ArticleTest terminal per-case0, no skips/errors. "
    "Full git archive40bc5a55/versionceee0f79a6d394df/8429runtimehashes through productionContentSync ONCE: "
    "1113kanji/5069words/122N1/zeroProblems/acceptedRoomversion+readingepoch1. "
    "Inspect all18scopedHan across fourproductionfamilies/systemfallback; 72individual+4wholewordPaint probes "
    "and3Composepanels. Maincmapcoverage/hasGlyph/hashes are NOT native legibility or fallback-face evidence. "
    "N1/All production choices exactly 刀sword;blade, 乃thereupon;possessiveno, 凹concave;sunken, 凸convex;protruding; "
    "allthreecuratedwrongcardsavailable/no fallback. Exactly onとう and kunかたな offered/persistedGood/done, "
    "NOそり; allrawトウ/かたな/そり retained in sourceorder in full/LiteRoom. "
    "Twostroke injectedtrace/recall/persistence, BOTHcompletearticles andONLYfourchangedreusedpassages, "
    "fiveallmappedpairs/tendirections/onedirect日本刀-to-刀guard; preserve existing刀N3/剃刀N2/鋭いguard. "
    "N1selection/meaning/readings/drawing/articles/SystemBack/offline. TraditionalJapaneseSwordnoun, "
    "neutralmuseum/photosentences, lexical日本modifier+sword, bothにほんとう/にっぽんとう without "
    "frequencyranking/universalsoundchange/shape rule; sourceonlyそりnotallocatedfromjukujikunrazor. "
    "Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581ownership "
    "immediately before ownedreadonlyAPI35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/2048MiB/2cores; "
    "stop only ownedhelper. No guest/appheap/guardincrease, productionappchange,091 or runtimepublication. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "Original textualsnapshote044e953 closed across Claude63fa1d59-4733-497f-bc2d-b6202471619d "
    "and GPTf0995652-508c-4921-a3dd-08e89e67eb46; alloriginalreview/readlimitationspreserved. "
    "Serial original-session dependentvisualconfirmations remain, no newblindcredit. "
    "Parent19008 ownsrunner.lock: verifyliveancestry/session/checkpoint/exactsignedheads/whollycleanworktrees; "
    "NOchildreacquisition/delete/unlock. Approvedcontrol/committedsources only, NOT optionalhistoricalsessionrecipes. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Alloriginalsource/baseline/link/reading/"
    "twofamily/native/currentmainnormalmerge/changedteachingindependentreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalCI/EVERYimmutablepublicZIPruntimehash/original18000entries42MiBcompressed/"
    "80MiBinflated56MiBretained/perfile-media-safepath/ownerissue gates remain. "
    "Published116/1228,1112remaining unchanged; physicalphone/generalrelease/whole-set outstanding; projectincomplete."
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
    temp = C / "progress.640.tmp"
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
    assert count == 8429
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-090-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    for name, digest in reconciliation["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        639, "continue", "fresh-android-passed-awaiting-native", "090")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    role = load(L / "native-runner-role.json")
    assert role["parentAncestryVerified"] and not role["parentLockAccessAttempted"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 639 and checkpoint["execution639CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution640StartingState"] = {
        "execution": 640, "batch": "090", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME090 full native fixture/archive preparation and compilation, signed LOCAL evidence; yield before native execution/visual review/publication/091.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete approved issue and final639 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry and exact runner session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-090-native-preparation-in-progress"
    state["nextAction"] = state["execution640StartingState"]["scope"]
    persist(state)
    print("Starting640 persisted; full live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    utility = C / "prepare-batch-085-native.py"
    assert sha(utility) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", utility)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-090-draft-font-audit.json")
    names = audit["completeNewArticleScope"]
    reused = [item["article"] for item in audit["exactReusedChangedPassagesIncluded"]]
    assert names == ["kanji/刀.md", "words/日本刀.md"] and len(reused) == 4
    docs = {name: blocks(R.joinpath(*name.split("/"))) for name in names + reused}
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_640" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_640")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("刀")')
    line('click("sword; blade")')
    display("kanji/刀.md", "kanji")
    forward = follow("kanji/刀.md", "日本刀", "words/日本刀.md", "Common words", "japanese-sword-forward")
    display("words/日本刀.md", "japanese-sword")
    reverse = follow("words/日本刀.md", "刀", "kanji/刀.md", "How the kanji combine", "japanese-sword-reverse")
    line('section("Readings")')
    line('show(readingExample("トウ"), "japanese-sword-kanji-backlink")')
    back_to(reverse, "japanese-sword-system-back-to-word")
    for char, slug in [("日", "country-first"), ("本", "country-second")]:
        other = follow("words/日本刀.md", char, f"kanji/{char}.md", "How the kanji combine", f"{slug}-forward")
        other_reverse = follow(f"kanji/{char}.md", "日本刀", "words/日本刀.md", "Common words", f"{slug}-reverse")
        line(f"await({quote(docs['words/日本刀.md'][0][1])})")
        back_to(other_reverse, f"{slug}-system-back-to-kanji")
        back_to(other, f"{slug}-system-back-to-word")
    back_to(forward, "japanese-sword-system-back-to-kanji")
    for word, slug in [("刀", "katana"), ("剃刀", "razor")]:
        word_forward = follow("kanji/刀.md", word, f"words/{word}.md", "Common words", f"{slug}-forward")
        line(f"await({quote(docs[f'words/{word}.md'][0][1])})")
        word_reverse = follow(f"words/{word}.md", "刀", "kanji/刀.md", "How the kanji combine", f"{slug}-reverse")
        line('section("Readings")')
        line('show(readingExample("かたな"), ' + quote(f"{slug}-kanji-backlink") + ")")
        back_to(word_reverse, f"{slug}-system-back-to-word")
        back_to(word_forward, f"{slug}-system-back-to-kanji")
    plan = load(R / "docs" / "n1-sources" / "batch-090-progress.json")["proposedDirectedLinkPlan"]
    assert {(x["document"], x["destination"]) for x in offsets} == {(x["from"], x["to"]) for x in plan}
    assert len(offsets) == 10
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    begin = text.index("            val answeredKeys =")
    end = text.index('            back()\n            await("Meaning quiz")', begin)
    both = TWO_KINDS.read_text(encoding="utf-8")
    both_begin = both.index("            val answeredKinds =")
    both_end = both.index('            back()\n            await("Meaning quiz")', both_begin)
    both = both[both_begin:both_end].replace("凝", "刀").replace("ぎょう", "とう").replace("こる", "かたな")
    both = both.replace('assertEquals(key, question.question.correctKey)',
                        'assertEquals(key, question.question.correctKey)\n                assertNotEquals("そり", key)')
    both = both.replace('capture("curated-on-kun-done")',
                        'assertEquals(setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name), readingLogs.map { it.mode }.toSet())\n            capture("curated-on-kun-done")')
    text = text[:begin] + both + text[end:]
    replacements = [
        ("N1Batch089", "N1Batch090"), ("disposable089", "disposable090"), ("n1-089", "n1-090"),
        ("Batch 089", "Batch 090"), ("n1-batch-089-72614eda-envelope.zip", ARCHIVE.name),
        ("72614eda48aa8752d9401540d63a479467948d10", HEAD), ("c6562f11cb371053", VERSION),
        ("1112, updated.kanji", "1113, updated.kanji"), ("5068, updated.words", "5069, updated.words"),
        ("121, n1.size", "122, n1.size"), ("N1 · 121 cards", "N1 · 122 cards"),
        ("illFortuneLookalikesAndRadicalFallbacks", "swordLookalikesAndScopedHan"),
        ("fullSingleImportOfflineIllFortuneTwoReciprocalPairsOneOnKeyNoKunDrawingAndSystemBack",
         "fullSingleImportOfflineSwordFiveReciprocalPairsBothReadingKindsDrawingAndSystemBack"),
        ("val illFortune =", "val sword ="), ("illFortune.", "sword."),
        ('"凶"', '"刀"'), ("ill fortune; evil", "sword; blade"),
        ('listOf("凡", "凸", "凹")', 'listOf("乃", "凹", "凸")'),
        ('"凡" to "commonplace; mediocre"', '"乃" to "thereupon; possessive no"'),
        ('listOf("キョウ")', 'listOf("トウ")'), ('listOf("きょう")', 'listOf("とう")'),
        ('put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)',
         'put("mappedReciprocalPairs", 5).put("directedLinkTransitions", 10)'),
        ('put("changedReusedArticles", 1)', 'put("changedReusedArticles", 4)'),
        ("assertEquals(4, strokes.length())", "assertEquals(2, strokes.length())"),
        ('hasContentDescription("4 strokes drawn"', 'hasContentDescription("2 strokes drawn"'),
        ("kotlin.random.Random(631)", "kotlin.random.Random(640)"),
        ("importedHarvest", "importedSword"), ('"凶作"', '"日本刀"'),
        ('listOf("収穫")', 'listOf("刀")'), ('"きょうさく"', '"にほんとう"'),
        ('kind == ReadingKind.On && key in setOf("きょう")',
         '(kind == ReadingKind.On && key == "とう" || kind == ReadingKind.Kun && key == "かたな")'),
        ('put("singleCuratedOnKeyPersistedGoodAndDone", true)', 'put("bothCuratedKindsPersistedGoodAndDone", true)'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    for owner in ["sword", "card"]:
        text = text.replace(f'assertEquals(emptyList<String>(), {owner}.kunyomi.splitSep())',
                            f'assertEquals(listOf("かたな", "そり"), {owner}.kunyomi.splitSep())')
        text = text.replace(f'assertEquals(emptyList<String>(), {owner}.quizKunyomi?.splitSep())',
                            f'assertEquals(listOf("かたな"), {owner}.quizKunyomi?.splitSep())')
    text = text.replace('assertEquals(emptyList<String>(), sword.toReadingCard().quizKeys(ReadingKind.Kun))',
                        'assertEquals(listOf("かたな"), sword.toReadingCard().quizKeys(ReadingKind.Kun))')
    text = text.replace('assertNull(importedSword.jlpt)', '''assertNull(importedSword.jlpt)
        assertEquals(3, requireNotNull(runBlocking { app.db.content().word(source.id, "刀") }).jlpt)
        val importedRazor = requireNotNull(runBlocking { app.db.content().word(source.id, "剃刀") })
        assertEquals(2, importedRazor.jlpt)
        assertEquals(listOf("鋭い"), importedRazor.quizExclusions.splitSep())''')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 刀 meaning and exactly onとう/kunかたな due, source-onlyそり excluded without erasing raw metadata. Two historical good 刀 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    glyphs = audit["actualHan"]
    assert len(glyphs) == 18
    words = ["日本刀"]
    pages = [" ".join(glyphs[:12]), " ".join(glyphs[12:]), "刀 力 乃 凹 凸 丁 包 剃 日本刀"]
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", "for (word in listOf(" + ", ".join(map(quote, words)) + "))", text, count=1)
    text = text.replace("ill fortune / look-alikes / radical fallback", "sword / look-alikes / scoped Han")
    text = text.replace("all 23 scoped Han; focused 凶/凡/凸/凹 and 乂/凵", "all 18 scoped Han; focused 刀/力/乃/凹/凸 and 日本刀")
    text = text.replace("23 actual scoped Han including exact 乂/凵 fallback inspection", "18 actual scoped Han; all main-font cmaps cover these, native readability still requires inspection")
    text = text.replace("assertEquals(96, rows.length())", "assertEquals(76, rows.length())")
    text = text.replace('put("individualGlyphProbes", 92)', 'put("individualGlyphProbes", 72)')
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ["089", "illFortune", "凶", "凡", "キョウ", "きょう", "乂", "凵", "singleCuratedOnKey", "repeat(1)"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    assert 'listOf("かたな", "そり"), sword.kunyomi.splitSep()' in text
    assert 'listOf("かたな", "そり"), card.kunyomi.splitSep()' in text
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == []
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1113, "words": 5069, "n1": 122}
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-090/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-090/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-090/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-090/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8429 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-089.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 640, "batch": "090", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": "e044e953133548dd37fdf1dba449de2f4ee7575f",
        "androidSnapshot": APP, "productionBaseline": PROD, "contentVersion": VERSION, "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "bothReadingKindsHarness": TWO_KINDS.relative_to(R).as_posix(), "bothReadingKindsHarnessSha256": sha(TWO_KINDS),
        "durableUtilityRecipe": str(utility), "durableUtilityRecipeSha256": sha(utility),
        "fixtureDiff": str(diff), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 2, "changedReusedScope": audit["exactReusedChangedPassagesIncluded"],
        "mappedReciprocalPairs": 5, "mappedDirectedTransitions": 10,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "plannedNativePaintProbes": 72, "plannedWholeWordRasterProbes": 4, "currentFontAudit": fonts,
        "fullReadings": {"on": ["トウ"], "kun": ["かたな", "そり"]},
        "curatedReadings": {"on": ["トウ"], "kun": ["かたな"]},
        "normalizedQuizKeys": {"on": ["とう"], "kun": ["かたな"]}, "directWordExclusionPairs": 1,
        "pendingCmapAbsences": [], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1/All choices required; three curated wrong cards available, no fallback needed. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. All original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen090 fixture and full archive; all8429 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-090-native-test.apk"
    app = C / "artifacts" / "n1-batch-090-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch090GlyphTest", "N1Batch090ArticleTest",
                     "fullSingleImportOfflineSwordFiveReciprocalPairsBothReadingKindsDrawingAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-640-native-compile.ps1", VERIFICATION,
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
    zipped.write_bytes(gzip.compress((L / "native-compile.txt").read_bytes(), mtime=0))
    assert gzip.decompress(zipped.read_bytes()) == (L / "native-compile.txt").read_bytes()
    provenance.append({"archive": zipped.relative_to(R).as_posix(), "sha256": sha(zipped),
                       "sourceSha256": sha(L / "native-compile.txt"), "losslessGzipVerified": True})
    evidence = {
        "schemaVersion": 1, "execution": 640, "batch": "090", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution640StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8429, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 116, "remainingAdditions": 1112, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; preserve as evidence, not source whitespace changes.",
    }
    save(R / "docs" / "n1-sources" / "execution-640.json", evidence)
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-090-native/", "docs/n1-sources/execution-640.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-090-native-640-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-090-native-640-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-640.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 639 and state["stage"] == "batch-090-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 640, "checkpoint": 640, "batch": "090",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-640.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8429,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 116, "remainingAdditions": 1112, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=640, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution640CoordinatorCheckpoint"] = checkpoint
    state["batch090NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    assert all(load(C / "progress.json")[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-640-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 640, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
