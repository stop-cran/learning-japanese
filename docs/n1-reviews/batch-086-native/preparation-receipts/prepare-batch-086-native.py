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

sys.stdout.reconfigure(encoding="utf-8")
C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
LOG = C / "logs" / "4d3581a0-2755-4b12-8e27-3fff4418c2a3"
HEAD = "6667318d9d5bdf8ec8c899db64395e2955612432"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "86e8cb13aa72ecd0"
WORK = C / "batch-086-native-604"
FIXTURE = WORK / "N1Batch086NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-086-6667318d-envelope.zip"
VERIFICATION = C / "batch-086-native-fixture-verification.json"
BEFORE = LOG / "progress-before-604.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-086-native"
PRIOR = R / "docs" / "n1-reviews" / "batch-085-native" / "N1Batch085NativeTest.kt"
SPEC = importlib.util.spec_from_file_location("prior_native_utils", C / "prepare-batch-085-native.py")
UTIL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UTIL)
quote, plain, blocks = UTIL.quote, UTIL.plain, UTIL.blocks
NEXT = (
    "SAME086 execute frozen compiled native fixture and inspect actual PNGs next; "
    "read docs/n1-sources/execution-604.json and batch-086-native-fixture-verification.json. "
    "Preparation/compilation is NOT native or visual acceptance. Exact full archive6667318d/"
    "version86e8cb13aa72ecd0/8416runtimehashes; qualified TESTONLY Android1c1b7bf4 atop "
    "unchanged productionf9b59a2, not latest app main. Require terminalcase0 BOTH "
    "N1Batch086GlyphTest and N1Batch086ArticleTest without skips/errors. Production "
    "ContentSync ONCE,1109kanji/5064words/118N1/zeroProblems/version/acceptedRoom "
    "readingepoch1. Allfive raw readings/order retained; selected onボン/ハン yields "
    "exactぼん/はん; explicitkun[] and no kun question/log. Rawおうよ.そ modern usage "
    "UNVERIFIED source-only, not normalized. All31 scopedHan/fourproductionfamilies/"
    "124individual+16wholewordrasters/3Composepanels especially丶/几 require direct "
    "PNGlegibility/lookalike inspection; cmap/hasGlyph/hashes not readability or fallback "
    "face evidence. Two complete new articles plus exact six changed reused passages, "
    "sevenreciprocalpairs/fourteendirections incl aliases and 平/例/全, eight direct "
    "word guards, SystemBack/offline/N1selection/meaning/two on keys persistedGood/done/"
    "three-stroke injectedtrace/recall/persistence. Trace injection/giveup NOT human "
    "handwriting/MLKit/phone. Fresh live device/PID/local+remote5580/5581 including "
    "TimeWait ownership immediately before owned readonly API35 N3_Acceptance_20261029 "
    "emulator-5580 launch; hostGPU/-Vulkan/2048MiB/2cores/explicitserial, stop only "
    "ownedhelper. Do not interfere with shared devices or choose another port without "
    "authorization. No app/guestheap/guard increase, production app change or087. "
    "Parent19008 owns runner.lock; verify live ancestry/session/checkpoint/exact signed "
    "heads/whollycleanworktrees; NOchild acquisition/delete/unlock. Approved control/"
    "committedsources only. Preserve/report/yield actual new denial/signing hang/"
    "uncertain ownership. Original twofamily textual reviews and limitations preserved; "
    "dependent serial twofamily visual confirmations remain, no new blind credit. Later "
    "currentmain normalmerge/surgical reconciliation/changedteaching review/combined "
    "checks/normal signing/owner fastforward/terminalCI/EVERY immutable publicZIP "
    "runtimehash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath guards/verified ownerissue remain. Published112/1228,"
    "1116remaining unchanged; physicalphone/generalrelease/whole-set outstanding, "
    "project incomplete. No087 or publication in next bounded native checkpoint."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root), str(root)


def update(state):
    temp = C / "progress.604.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    value = load(R / "manifest.json")
    assert value == build_manifest(R) and value["contentVersion"] == VERSION
    assert sum(len(v) for v in value.values() if isinstance(v, dict)) == 8416
    return value


def start():
    clean(R, HEAD)
    clean(A, APP)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 603 and state["batch"] == "086"
    assert state["stage"] == "fresh-android-passed-awaiting-native"
    assert state["status"] == "continue" and not BEFORE.exists()
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == LOG.name and runner["status"] == "running"
    role = load(LOG / "native-runner-role.json")
    assert any(p["pid"] == 19008 for p in role)
    request_path = LOG / "request.txt"
    request = request_path.read_text(encoding="utf-8-sig")
    parsed = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert parsed["checkpoint"] == 603
    runtime()
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)
    shutil.copyfile(C / "progress.json", BEFORE)
    state["execution604StartingState"] = {
        "execution": 604, "batch": "086", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME086 full archive/native fixture preparation and compilation, signed LOCAL evidence; yield before native execution/reviewer/integration/publication/087.",
        "request": {"sha256": sha(request_path), "bytes": request_path.stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded before acting; operative contract, complete issue and final603 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial display hit cp1252 encoding error after complete parse; final checkpoint read directly with view."},
        "runnerLockRole": "Verified live parent19008 ancestry and exact runner.json session; child never acquires/deletes/unlocks parent lock.",
        "runnerRoleReceipt": str(LOG / "native-runner-role.json"),
        "artifactPathPreflight": "Approved workspace inputs, committed source packets and new reusable control helpers only; optional historical session helpers not accessed.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-086-native-preparation-in-progress"
    state["nextAction"] = state["execution604StartingState"]["scope"]
    update(state)
    print("Starting scope persisted with complete live history.")


def prepare():
    from fontTools.ttLib import TTFont
    clean(R, HEAD)
    clean(A, APP)
    assert not WORK.exists() and not VERIFICATION.exists()
    manifest = runtime()
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-086-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    for name, digest in reconciliation["reviewedRuntimeHashes"].items():
        assert sha(R / name) == digest, name
    audit = load(R / "docs" / "n1-sources" / "batch-086-draft-font-audit.json")
    names = audit["completeNewArticleScope"]
    changed = [item["article"] for item in audit["changedReusedScope"]]
    docs = {name: blocks(R / name) for name in names + changed}
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def show(document, kind, value, step):
        qualifier = "readingExample" if kind == "table" else "articleBullet"
        assert sum(v == value for k, v in docs[document]
                   if (k == "table") == (kind == "table") and k != "heading") == 1, (document, value)
        line(f"show({qualifier}({quote(value)}), {quote(step)})")
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
        body = (R / document).read_text(encoding="utf-8").split("---", 2)[2]
        sections = re.split(r"^## (.+)\n", body, flags=re.M)
        candidates = []
        for i in range(1, len(sections), 2):
            if sections[i] != section:
                continue
            for part in re.split(r"\n\s*\n|\n(?=- )", sections[i + 1].strip()):
                for link in re.finditer(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", part):
                    if (R / document).parent.joinpath(link[1]).resolve() == (R / destination).resolve():
                        candidates.append(part.removeprefix("- "))
        assert len(candidates) == 1, (document, label, candidates)
        raw = candidates[0]
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        rendered = plain(" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_604" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_604")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("凡")')
    line('click("commonplace; mediocre")')
    display("kanji/凡.md", "kanji")
    for word, label, other, slug in [
        ("平凡", "平凡", "平", "ordinary"),
        ("凡例", "凡例", "例", "legend"),
        ("およそ", "およそ", None, "approximate"),
        ("全て", "全て", "全", "everything"),
    ]:
        word_path = f"words/{word}.md"
        forward = follow("kanji/凡.md", label, word_path, "Common words", slug + "-forward")
        line(f"await({quote(docs[word_path][0][1])})")
        if word == "凡例":
            display(word_path, slug)
        if other:
            component = follow(word_path, other, f"kanji/{other}.md", "How the kanji combine", slug + "-component")
            line(f"await({quote(docs[f'kanji/{other}.md'][0][1])})")
            reverse_component = follow(f"kanji/{other}.md", word, word_path, "Common words", slug + "-changed-reused")
            line(f"await({quote(docs[word_path][0][1])})")
            back_to(reverse_component, slug + "-back-to-reused-kanji")
            back_to(component, slug + "-back-to-word")
        reverse = follow(word_path, "凡", "kanji/凡.md", "How the kanji combine", slug + "-reverse")
        line('section("Readings")')
        line(f'show(readingExample("ボン"), "{slug}-kanji-backlink")')
        back_to(reverse, slug + "-system-back-to-word")
        back_to(forward, slug + "-system-back-to-kanji")
    assert len(offsets) == 14
    assert len({(i["document"], i["destination"]) for i in offsets}) == 14
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    replacements = [
        ("N1Batch085", "N1Batch086"), ("disposable085", "disposable086"),
        ("n1-085", "n1-086"), ("Batch 085", "Batch 086"),
        ("n1-batch-085-1d2e3290-envelope.zip", ARCHIVE.name),
        ("1d2e329035789b160e495a7518d64183f799233e", HEAD),
        ("0c514711ae8d3212", VERSION), ("1108, updated.kanji", "1109, updated.kanji"),
        ("5063, updated.words", "5064, updated.words"), ("117, n1.size", "118, n1.size"),
        ("N1 · 117 cards", "N1 · 118 cards"), ('"凝"', '"凡"'),
        ("concentration", "commonplace"), ("ConcentrationFourReciprocalPairsCuratedOnAndKun", "CommonplaceSevenReciprocalPairsTwoOnKeysNoKun"),
        ("congeal; become absorbed", "commonplace; mediocre"),
        ('listOf("准", "冗", "凹")', 'listOf("丸", "九", "凹")'),
        ('"准" to "quasi-; associate rank"', '"丸" to "round; circle"'),
        ('"冗" to "superfluous; redundant"', '"九" to "nine"'),
        ('listOf("ギョウ")', 'listOf("ボン", "ハン")'),
        ('listOf("こ.る", "こ.らす", "こご.らす", "こご.らせる", "こご.る")',
         'listOf("およ.そ", "おうよ.そ", "すべ.て")'),
        ('listOf("こ.る", "こ.らす")', 'emptyList<String>()'),
        ('listOf("ぎょう")', 'listOf("ぼん", "はん")'),
        ('listOf("こる")', 'emptyList<String>()'),
        ('put("mappedReciprocalPairs", 4).put("directedLinkTransitions", 8)',
         'put("mappedReciprocalPairs", 7).put("directedLinkTransitions", 14)'),
        ('put("completeArticleProjections", 4).put("changedReusedBullets", 1)',
         'put("completeArticleProjections", 2).put("changedReusedArticles", 6)'),
        ("assertEquals(16, strokes.length())", "assertEquals(3, strokes.length())"),
        ('hasContentDescription("16 strokes drawn"', 'hasContentDescription("3 strokes drawn"'),
        ("kotlin.random.Random(595)", "kotlin.random.Random(604)"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = text.replace(
        'if (card.kanji == "凡" && key == (if (kind == ReadingKind.On) "ぎょう" else "こる"))',
        'if (card.kanji == "凡" && kind == ReadingKind.On && key in setOf("ぼん", "はん"))')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 凡 meaning and exactly onぼん/はん due; explicit kun[] gives no questions. Two historical good 凡 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    text = text.replace("val answeredKinds = mutableSetOf<ReadingKind>()", "val answeredKeys = mutableSetOf<String>()")
    text = text.replace(
        'assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))\n'
        '                val key = if (question.question.kind == ReadingKind.On) "ぎょう" else "こる"',
        'assertEquals(ReadingKind.On, question.question.kind)\n'
        '                val key = question.question.correctKey\n'
        '                assertTrue(key in setOf("ぼん", "はん"))\n'
        '                assertTrue("Duplicate target reading key", answeredKeys.add(key))')
    text = text.replace("assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)",
                        'assertEquals(setOf("ぼん", "はん"), answeredKeys)')
    text = text.replace('setOf("ぎょう", "こる")', 'setOf("ぼん", "はん")')
    text = text.replace('"curated-${question.question.kind}-', '"curated-${key}-')
    text = text.replace("bothCuratedKindsPersistedGoodAndDone", "bothCuratedOnKeysPersistedGoodAndDone")
    text = text.replace('capture("curated-on-kun-done")', 'assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })\n'
                        '            capture("curated-two-on-no-kun-done")')
    guard_code = (
        '        val importedLegend = requireNotNull(runBlocking { app.db.content().word(source.id, "凡例") })\n'
        '        assertEquals(listOf("注", "説明", "解説", "メモ", "筆記", "はじめに", "概論", "鍵"), importedLegend.quizExclusions.splitSep())\n'
        '        assertEquals("はんれい", importedLegend.reading)\n'
        '        assertNull(importedLegend.jlpt)\n'
    )
    text = text.replace("        val now = System.currentTimeMillis()", guard_code + "        val now = System.currentTimeMillis()")
    text = text.replace('.put("problems", updated.problems.size)', '.put("directWordGuardCount", importedLegend.quizExclusions.splitSep().size)\n'
                        '            .put("problems", updated.problems.size)')
    text = text.replace(
        '            assertEquals(expectedMeanings, cards.filter { it.kanji in expectedMeanings }.associate { it.kanji to it.title })\n'
        '            val options = QuizBuilder.options(target, cards, kotlin.random.Random(604))\n'
        '            assertEquals(4, options.size)\n'
        '            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })',
        '            val options = QuizBuilder.options(target, cards, kotlin.random.Random(604))\n'
        '            assertEquals(4, options.size)\n'
        '            if (poolName == "All") {\n'
        '                assertEquals(expectedMeanings, options.associate { it.kanji to it.title })\n'
        '            } else {\n'
        '                assertEquals(setOf("凡", "凹"), cards.filter { it.kanji in expectedMeanings }.map { it.kanji }.toSet())\n'
        '                assertTrue(options.any { it.kanji == "凹" })\n'
        '                assertEquals(2, options.count { it.kanji !in expectedMeanings })\n'
        '            }')
    text = text.replace('.put("allThreeCuratedAvailable", true).put("defaultFourNoPadding", true)',
                        '.put("availableCuratedCount", cards.count { it.kanji in target.distractors })\n'
                        '                .put("fallbackOptions", options.count { it.kanji !in expectedMeanings })')
    text = text.replace(
        '            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })',
        '            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })\n'
        '            assertTrue(meaning.options.any { it.kanji == "凹" })\n'
        '            assertEquals(2, meaning.options.count { it.kanji !in expectedMeanings })\n'
        '            assertEquals("commonplace; mediocre", meaning.options.single { it.kanji == "凡" }.title)')
    text = text.replace('.put("exactCuratedChoicesWithoutFallback", true)',
                        '.put("actualN1CuratedAvailable", 1).put("actualN1FallbackOptions", 2)\n'
                        '                .put("meaningChoiceVisualAdjudicationRequired", true)')
    glyphs = audit["actualHan"]
    assert len(glyphs) == 31
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["丶", "几"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    words = ["平凡", "凡例", "凡そ", "凡て"]
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("凡 丸 九 凹 几 丶 平凡 凡例 凡そ 凡て")
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", "for (word in listOf(" + ", ".join(map(quote, words)) + "))", text, count=1)
    text = text.replace("all 39 scoped Han; focused 凝/疑/准/冗/凹, 冫/隹",
                        "all 31 scoped Han; focused 凡/丸/九/凹, 丶/几")
    text = text.replace("39 actual scoped Han including exact 冫/隹 fallback inspection",
                        "31 actual scoped Han including exact 丶/几 fallback inspection")
    text = text.replace("assertEquals(168, rows.length())", "assertEquals(140, rows.length())")
    text = text.replace('put("individualGlyphProbes", 156).put("wholeWordRasterProbes", 12)',
                        'put("individualGlyphProbes", 124).put("wholeWordRasterProbes", 16)')
    text = text.replace("twelve whole-word rasters", "sixteen whole-word rasters")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("085", "凝", "こご", "ギョウ", "ぎょう", "こる", "answeredKinds", "冫", "隹"):
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    expected_titles = {"凡": "commonplace; mediocre", "丸": "round; circle",
                       "九": "nine", "凹": "concave; sunken"}
    for char, title in expected_titles.items():
        assert re.search(r"^title: " + re.escape(title) + r"$", (R / "kanji" / f"{char}.md").read_text(encoding="utf-8"), re.M), (char, title)
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1109, "words": 5064, "n1": 118}
    if not ARCHIVE.exists():
        subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-086/",
                        f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-086/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-086/manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=R)
        assert json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, mapping in manifest.items():
            if not isinstance(mapping, dict):
                continue
            for name, expected in mapping.items():
                data = archive.read("n1-batch-086/" + name)
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in archive.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024 and verified == 8416
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-085.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(R).as_posix(), tofile="docs/n1-reviews/batch-086-native/" + FIXTURE.name, n=2)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 604, "batch": "086", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": reconciliation["reviewedTeachingSnapshot"],
        "androidSnapshot": APP, "productionBaseline": PROD, "contentVersion": VERSION,
        "expectedCounts": counts, "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE),
        "zipEntries": len(entries), "compressedBytes": ARCHIVE.stat().st_size,
        "inflatedBytes": inflated, "retainedBytes": retained, "verifiedRuntimeHashes": verified,
        "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "durableUtilityRecipe": str(C / "prepare-batch-085-native.py"),
        "durableUtilityRecipeSha256": sha(C / "prepare-batch-085-native.py"),
        "fixtureDiff": str(diff), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 2, "changedReusedScope": audit["changedReusedScope"],
        "mappedReciprocalPairs": 7, "mappedDirectedTransitions": 14, "directWordGuards": 8,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "plannedNativePaintProbes": 124, "plannedWholeWordRasterProbes": 16, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ボン", "ハン"], "kun": ["およ.そ", "おうよ.そ", "すべ.て"]},
        "curatedReadings": {"on": ["ボン", "ハン"], "kun": []},
        "normalizedQuizKeys": {"on": ["ぼん", "はん"], "kun": []},
        "sourceOnlyLimit": "Rawおうよ.そ modern usage remains UNVERIFIED source-only, not normalized or offered.",
        "pendingCmapAbsences": ["丶", "几"], "exactMeaningOptions": expected_titles,
        "meaningPoolQualification": "All includes all three curated choices. Exact N1 excludes easier丸(N2)/九(N5), so only凹 is available and production fills two random wrong options. Native records actual displayed labels for dependent visual adjudication; no N1 no-padding/safety certification from static curated labels. Original uncompiled template-assumption fixture/verification preserved under control batch-086-native-604-initial before correction; no production/content change.",
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": "Preparation only. Static Markdown selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Two complete new article projections plus exact six changed reused passages only; unchanged reused bodies not claimed freshly reviewed. ProductionContentSyncONCE; reference tracing/giveup not human handwriting/MLKit/phone. All original source/reviewer/denial/OOM/phone limits and production heaps/guards preserved.",
    }
    save(VERIFICATION, record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes",
                                             "compressedBytes", "inflatedBytes", "retainedBytes")}))


def record():
    clean(R, HEAD)
    clean(A, APP)
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (LOG / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(LOG / "native-compile-command.json")
    assert command["parentAncestryVerified"] and not command["parentLockAccessAttempted"]
    assert not command["hostOnlyHeapInitUsed"]
    assert "BUILD SUCCESSFUL" in (LOG / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-086-native-test.apk"
    app = C / "artifacts" / "n1-batch-086-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch086GlyphTest", "N1Batch086ArticleTest",
                     "fullSingleImportOfflineCommonplaceSevenReciprocalPairsTwoOnKeysNoKunDrawingAndSystemBack"):
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    FOLDER.mkdir()
    for path in WORK.iterdir():
        shutil.copyfile(path, FOLDER / path.name)
    original_fixture = C / "batch-086-native-604-initial"
    initial_archive = FOLDER / "initial-uncompiled-assumption"
    initial_archive.mkdir()
    for path in original_fixture.iterdir():
        shutil.copyfile(path, initial_archive / path.name)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "prepare-batch-085-native.py", C / "run-604-native-compile.ps1", VERIFICATION,
               LOG / "native-runner-role.json", C / "runner-lock-role-notes.txt",
               C / "authoring-artifact-path-notes.txt",
               *[LOG / n for n in ("native-compile-command.json", "native-compile-start.txt",
                                   "native-compile-end.txt", "native-compile-exit.txt")]]
    provenance = []
    for source in sources:
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    zipped = receipts / "native-compile.txt.gz"
    with zipped.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as compressor:
            compressor.write((LOG / "native-compile.txt").read_bytes())
    assert gzip.decompress(zipped.read_bytes()) == (LOG / "native-compile.txt").read_bytes()
    provenance.append({"archive": zipped.relative_to(R).as_posix(), "sha256": sha(zipped),
                       "sourceSha256": sha(LOG / "native-compile.txt"), "losslessGzipVerified": True})
    save(R / "docs" / "n1-sources" / "execution-604.json", {
        "schemaVersion": 1, "execution": 604, "batch": "086", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution604StartingState"],
        "fixtureVerification": verification, "provenance": provenance,
        "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "buildResult": "BUILD SUCCESSFUL", "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8416, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 112, "remainingAdditions": 1116, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    })
    print("Exact compiled artifact evidence archived; ready for normally signed LOCAL checkpoint.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    clean(A, APP)
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-086-native/", "docs/n1-sources/execution-604.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-086-native-604-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-086-native-604-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-604.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state = load(C / "progress.json")
    original = load(BEFORE)
    assert state["checkpoint"] == 603 and state["stage"] == "batch-086-native-preparation-in-progress"
    for key, value in original.items():
        if key not in {"stage", "nextAction"}:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 604, "checkpoint": 604, "batch": "086",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-prepared-compiled-not-executed", "evidence": "docs/n1-sources/execution-604.json",
        "contentArchiveHead": HEAD, "androidHead": APP, "fixtureVerification": str(VERIFICATION),
        "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE), "testApk": evidence["testApk"],
        "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8416,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False, "publishedAdditions": 112,
        "remainingAdditions": 1116, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(C / "batch-086-native-604-issue-receipt.json"),
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=604, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution604StartingState"]["status"] = "signed-local-native-preparation-checkpoint-complete"
    state["execution604CoordinatorCheckpoint"] = checkpoint
    state["batch086NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    update(state)
    persisted = load(C / "progress.json")
    assert all(persisted[k] == v for k, v in original.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(LOG / "checkpoint-604-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 604, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
