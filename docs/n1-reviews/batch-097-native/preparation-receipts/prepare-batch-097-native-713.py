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
L = C / "logs" / "5d45db9d-513d-4000-8dc6-525d23565294"
HEAD = "83e5c0901a2d080e33b3583da7e0271a6aa329a0"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "1fa1ac69b88383ef424c0a69d34020ccca83c313"
VERSION = "a066afceaf1f447a"
WORK = C / "batch-097-native-713"
FIXTURE = WORK / "N1Batch097NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-096-native" / "N1Batch096NativeTest.kt"
UTILITY = C / "prepare-batch-085-native.py"
ARCHIVE = C / "artifacts" / "n1-batch-097-83e5c090-envelope.zip"
VERIFICATION = C / "batch-097-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-097-native"
BEFORE = L / "progress-before-713.json"
NEXT = (
    "SAME097 execute frozen compiled native fixture and inspect actual PNGs next; preparation713 is NOT native acceptance. "
    "Read docs/n1-sources/execution-713.json and control/batch-097-native-fixture-verification.json. "
    "Require BOTH N1Batch097GlyphTest and N1Batch097ArticleTest terminal per-case0/no skips. "
    "Exact full archive83e5c090/versiona066afceaf1f447a/8447runtimehashes through productionContentSync ONCE: "
    "1120kanji/5073words/129N1/zeroProblems/acceptedRoomversion+readingepoch1. "
    "Inspect all20Han across FOUR production font families/systemfallback, especially刂; "
    "80individual+8wholewordPaint probes/THREE bounded Compose panels. Cmap/hasGlyph/rasterhashes NOT legibility/fallbackface evidence. "
    "All productionchoices exactly sword;double-edgedblade vs剛/剖/則; actual N1 includes剛/剖 but NOT則N2, "
    "so ONE productionfallback requires actual semantic inspection. Inspect N1 UI and16-seed N1/All/boundedcustom/randomN1subset "
    "builder records; fallbacksemanticacceptance OPEN, wider custom/random pools not certified by textual review. "
    "FOUR directwordguards from剣つるぎ full imported word pool/custom/bothdirections/bothtargetorientations/16seeds "
    "(512 planned builder checks). BOTHonけん/kunつるぎ offered/persistedGood/Done; full/Lite rawケン/[つるぎ] "
    "and explicitケン/[つるぎ] retained. TEN pinned strokes injectedtrace/recall/persistence; "
    "TWO complete articleprojections剣/剣つるぎ plus exact reused真剣component and真commonword changes; "
    "THREE allmapped reciprocalpairs/SIX directions/ONEactivatedbaselinepair; SystemBack/offline/N1selection/meaning/readings/drawing. "
    "Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581ownership immediately before "
    "ownedreadonlyAPI35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/2048MiB/2cores; stop only ownedhelper. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Fresh712 JVM4/no skips retained. "
    "OriginalClaude3a0b6dd8-6212-4ceb-a430-3127aac6969e THEN GPT9f31594c-f091-4d47-9276-12249f0c848d need serial bounded "
    "rendered confirmations, no newblindcredit. Parent19008 retains runner.lock; verifyliveancestry/session/checkpoint/exactsignedheads/"
    "whollyclean, NOchildreacquisition/delete/unlock/readprobe. Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. All currentmainnonrewritingmerge/surgicalreconciliation/"
    "changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPentryhash/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue gates remain. "
    "Published123/1228,1105remaining unchanged; physicalphone/generalrelease/whole-set outstanding. No098/runtimepublication/secondrunner."
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
    temp = C / "progress.713.tmp"
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
    assert count == 8447
    review = load(R / "docs" / "n1-reviews" / "batch-097-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        712, "continue", "batch-097-fresh-android-passed-awaiting-native", "097")
    role, runner = load(L / "preflight-713.json"), load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    assert role["decodedLauncherMatches"] and role["liveParentPid"] == 19008 and not role["lockTouched"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 712 and checkpoint["execution712CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution713StartingState"] = {
        "execution": 713, "batch": "097", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME097 full native fixture/archive preparation and compilation, normally signed LOCAL evidence; yield before native execution/visual review/publication/098.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final712 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-097-native-preparation-in-progress"
    state["nextAction"] = state["execution713StartingState"]["scope"]
    persist(state)
    print("Starting713 persisted; complete live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(UTILITY) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    assert sha(PRIOR) == "e55f53f31984dc2024657ea37e06f9c43e36277f6f2ab696aa14305697021c4c"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", UTILITY)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-097-draft-font-audit.json")
    names = audit["completeArticleScope"]
    assert names == ["kanji/剣.md", "words/剣.md"]
    projected = names + ["words/真剣.md", "kanji/真.md"]
    docs = {name: blocks(R.joinpath(*name.split("/"))) for name in projected}
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
                        if R.joinpath(*document.split("/")).parent.joinpath(match[1]).resolve() == R.joinpath(*destination.split("/")).resolve():
                            candidates.append(part.removeprefix("- "))
        assert len(candidates) == 1, (document, label, candidates)
        raw = candidates[0]
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        rendered = plain(" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_713" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_713")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("剣")')
    line('click("sword; double-edged blade")')
    display("kanji/剣.md", "kanji")
    to_word = follow("kanji/剣.md", "剣", "words/剣.md", "Common words", "tsurugi-forward")
    display("words/剣.md", "tsurugi")
    from_word = follow("words/剣.md", "剣", "kanji/剣.md", "How the kanji combine", "tsurugi-reverse")
    line('section("Readings")')
    line('show(readingExample("つるぎ"), "tsurugi-kanji-backlink")')
    back_to(from_word, "tsurugi-system-back-to-word")
    back_to(to_word, "tsurugi-system-back-to-kanji")
    to_shinken = follow("kanji/剣.md", "真剣", "words/真剣.md", "Common words", "shinken-forward")
    from_shinken = follow("words/真剣.md", "剣", "kanji/剣.md", "How the kanji combine", "shinken-reverse")
    line('section("Readings")')
    line('show(readingExample("ケン"), "shinken-kanji-backlink")')
    back_to(from_shinken, "shinken-system-back-from-ken")
    to_shin = follow("words/真剣.md", "真", "kanji/真.md", "How the kanji combine", "shin-reverse")
    from_shin = follow("kanji/真.md", "真剣", "words/真剣.md", "Common words", "shin-forward")
    line('section("How the kanji combine")')
    line(f"show(articleBullet({quote(to_shin['renderedText'])}), \"shinken-component-return\")")
    back_to(from_shin, "shin-system-back-to-kanji")
    back_to(to_shin, "shin-system-back-to-word")
    back_to(to_shinken, "shinken-system-back-to-ken")
    plan = load(R / "docs" / "n1-sources" / "batch-097-progress.json")["proposedDirectedLinkPlan"]
    assert len(offsets) == 6
    assert {(x["document"], x["destination"]) for x in offsets} == {(x["from"], x["to"]) for x in plan}
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "N1_BATCH_097_ARTICLE_PROJECTION\n" + text[end:]
    import yaml
    card = yaml.safe_load((R / "kanji" / "剣.md").read_text(encoding="utf-8").split("---", 2)[1])
    word = yaml.safe_load((R / "words" / "剣.md").read_text(encoding="utf-8").split("---", 2)[1])
    exclusions = word["quiz_exclusions"]
    assert exclusions == ["刀", "日本刀", "刃", "真剣"] and card["distractors"] == ["剛", "剖", "則"]

    def replace(old, new):
        nonlocal text
        assert old in text, old
        text = text.replace(old, new)

    for old, new in [
        ("N1Batch096", "N1Batch097"), ("disposable096", "disposable097"), ("n1-096", "n1-097"),
        ("Batch 096", "Batch 097"), ("n1-batch-096-58129f19-envelope.zip", ARCHIVE.name),
        ("58129f197c1f88a59ebb82c02cea9e9a0220377e", HEAD), ("54645b95fe8e939c", VERSION),
        ("1119, updated.kanji", "1120, updated.kanji"), ("5072, updated.words", "5073, updated.words"),
        ("128, n1.size", "129, n1.size"), ("N1 · 128 cards", "N1 · 129 cards"),
        ("strengthLookalikesAndScopedHan", "swordLookalikesAndScopedHan"),
        ("fullSingleImportOfflineStrengthOneSupportOneReciprocalPairOneOnNoKunTenStrokesAndSystemBack",
         "fullSingleImportOfflineSwordOneSupportThreeReciprocalPairsBothReadingsTenStrokesAndSystemBack"),
        ("strength", "sword"), ("Strength", "Sword"), ("sturdy; unyielding sword", "sword; double-edged blade"),
        ('"剛"', '"剣"'), ('listOf("削", "剖", "則")', 'listOf("剛", "剖", "則")'),
        ('listOf("ゴウ")', 'listOf("ケン")'), ('listOf("ごう")', 'listOf("けん")'),
        ('"ごう"', '"けん"'), ("onごう", "onけん"),
        ('put("mappedReciprocalPairs", 1)', 'put("mappedReciprocalPairs", 3)'),
        ('put("directedLinkTransitions", 2)', 'put("directedLinkTransitions", 6)'),
        ('put("activatedBaselinePairs", 0)', 'put("activatedBaselinePairs", 1)'),
        ('put("changedReusedArticles", 0)', 'put("changedReusedArticles", 2)'),
        ('put("newDirectWordGuardPairs", 12)', 'put("newDirectWordGuardPairs", 4)'),
        ("assertEquals(1536, directGuardChecks.length())", "assertEquals(512, directGuardChecks.length())"),
        ("kotlin.random.Random(704)", "kotlin.random.Random(713)"),
        ("onlyOnGouNoKunPersistedGoodAndDone", "bothKenAndTsurugiPersistedGoodAndDone"),
    ]:
        replace(old, new)
    replace('assertEquals(emptyList<String>(), sword.kunyomi.splitSep())',
            'assertEquals(listOf("つるぎ"), sword.kunyomi.splitSep())')
    replace('assertEquals(emptyList<String>(), sword.quizKunyomi?.splitSep())',
            'assertEquals(listOf("つるぎ"), sword.quizKunyomi?.splitSep())')
    replace('assertEquals(emptyList<String>(), sword.toReadingCard().quizKeys(ReadingKind.Kun))',
            'assertEquals(listOf("つるぎ"), sword.toReadingCard().quizKeys(ReadingKind.Kun))')
    replace('assertEquals(emptyList<String>(), card.kunyomi.splitSep())',
            'assertEquals(listOf("つるぎ"), card.kunyomi.splitSep())')
    replace('assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())',
            'assertEquals(listOf("つるぎ"), card.quizKunyomi?.splitSep())')
    begin = text.index("        val expectedMeanings =")
    end = text.index("        val all =", begin)
    expected, levels = {"剣": card["title"]}, {}
    for name in card["distractors"]:
        entry = yaml.safe_load((R / "kanji" / (name + ".md")).read_text(encoding="utf-8").split("---", 2)[1])
        expected[name], levels[name] = entry["title"], entry["jlpt"]
    assert levels == {"剛": 1, "剖": 1, "則": 2}
    text = text[:begin] + "        val expectedMeanings = mapOf(\n" + "".join(
        f"            {quote(k)} to {quote(v)},\n" for k, v in expected.items()) + "        )\n" + text[end:]
    replace('listOf("削", "剖"), curatedIds.filter', 'listOf("剛", "剖"), curatedIds.filter')
    begin = text.index("        val importedSword =")
    end = text.index("        for ((leftId, rightId) in guardPairs)", begin)
    text = text[:begin] + (
        '        val importedSword = words.single { it.word == "剣" }\n'
        f'        assertEquals(listOf({", ".join(map(quote, exclusions))}), importedSword.quizExclusions)\n'
        '        assertEquals("つるぎ", importedSword.reading)\n'
        '        assertNull(importedSword.jlpt)\n'
        '        val directGuardChecks = JSONArray()\n'
        '        val guardPairs = listOf(' + ", ".join(f'"剣" to {quote(w)}' for w in exclusions) + ')\n'
    ) + text[end:]
    replace('(kind == ReadingKind.On && key == "けん")',
            '((kind == ReadingKind.On && key == "けん") || (kind == ReadingKind.Kun && key == "つるぎ"))')
    replace("only 剛 meaning", "only 剣 meaning")
    replace("good 剛 meaning", "good 剣 meaning")
    replace("and onけん due; no kun keys.", "and onけん/kunつるぎ due.")
    replace('assertTrue(meaning.options.any { it.kanji == "削" })',
            'assertTrue(meaning.options.any { it.kanji == "剛" })')
    replace("            repeat(1) {", "            repeat(2) {")
    replace("                assertEquals(ReadingKind.On, question.question.kind)\n"
            "                val key = question.question.correctKey\n"
            '                assertTrue(key in setOf("けん"))',
            '                val key = if (question.question.kind == ReadingKind.On) "けん" else "つるぎ"')
    replace('assertEquals(setOf("けん"), answeredKeys)', 'assertEquals(setOf("けん", "つるぎ"), answeredKeys)')
    for field in ["done.answered", "done.correct", "readingLogs.size"]:
        replace(f"assertEquals(1, {field})", f"assertEquals(2, {field})")
    replace('assertEquals(setOf("けん"), readingLogs.map { it.reading }.toSet())',
            'assertEquals(setOf("けん", "つるぎ"), readingLogs.map { it.reading }.toSet())')
    replace("assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })",
            'assertEquals(setOf(ReadingKind.On.mode.name to "けん", ReadingKind.Kun.mode.name to "つるぎ"),\n'
            "                readingLogs.map { it.mode to it.reading }.toSet())")
    replace('capture("curated-one-on-no-kun-done")', 'capture("curated-on-kun-done")')
    glyphs = audit["actualHan"]
    assert len(glyphs) == 20
    pages = [" ".join(glyphs[i:i + 12]) for i in range(0, len(glyphs), 12)]
    pages.append("剣 剛 剖 則 刀 刂 刃 口 真 真剣 剣道")
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", 'for (word in listOf("真剣", "剣道"))', text, count=1)
    replace("all 28 scoped Han; focused 剛/削/剖/則/岡/冂/山/刀/刂", "all 20 scoped Han; focused 剣/剛/剖/則/刀/刂/刃/口/真")
    replace("28 actual scoped Han; 冂/刂 absent from all three bundled cmaps", "20 actual scoped Han; 刂 absent from all three bundled cmaps")
    replace("four bounded Compose panels", "three bounded Compose panels")
    replace("assertEquals(120, rows.length())", "assertEquals(88, rows.length())")
    replace('put("individualGlyphProbes", 112)', 'put("individualGlyphProbes", 80)')
    replace('put("panels", 4)', 'put("panels", 3)')
    text = text.replace("N1_BATCH_097_ARTICLE_PROJECTION", "\n".join(lines))
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1 and "ContentParser.parse" not in text
    for stale in ["096", "ゴウ", "ごう", "剛健", "削", "val strength", "importedStrength", "NoKun", "58129f19", "54645b95"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["刂"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1120, "words": 5073, "n1": 129}, counts
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-097/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-097/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-097/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-097/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8447 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-096.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 713, "batch": "097", "status": "prepared-not-executed",
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
        "articleFiles": [{"path": n, "sha256": sha(R.joinpath(*n.split("/"))), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 2, "changedReusedScope": audit["changedReusedScope"],
        "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6, "activatedBaselinePairs": 1,
        "plannedGlyphs": glyphs, "plannedWholeWords": ["真剣", "剣道"], "plannedComposePanels": pages,
        "plannedNativePaintProbes": 80, "plannedWholeWordRasterProbes": 8, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ケン"], "kun": ["つるぎ"]}, "curatedReadings": {"on": ["ケン"], "kun": ["つるぎ"]},
        "normalizedQuizKeys": {"on": ["けん"], "kun": ["つるぎ"]}, "newDirectWordExclusionPairs": 4,
        "directGuardPairs": [["剣", w] for w in exclusions], "directGuardPlannedBuilderChecks": 512,
        "directGuardScopes": ["All", "boundedCustom"], "directGuardDirections": ["JpToEn", "EnToJp"],
        "directGuardBothTargetOrientations": True,
        "kanjiChoicePlannedChecks": 64, "kanjiChoicePools": ["N1", "All", "boundedCustom", "randomN1Subset"],
        "n1CuratedAvailable": ["剛", "剖"], "n1MissingCurated": ["則"], "n1FallbackCount": 1,
        "allCuratedAvailable": ["剛", "剖", "則"], "allFallbackCount": 0,
        "fallbackSemanticAcceptance": "OPEN pending actual imported/UI options and evidence-based original-session confirmations",
        "pendingCmapAbsences": ["刂"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1 has TWO curated wrong cards;則N2 is excluded so ONE production fallback is captured, NOT assumed wrong or accepted. Wider custom/random pools need actual semantic inspection. Four direct guards through actual builder on imported words, not learner word-session UI. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. Reused article scope is exact changed passages and required link destinations, not fresh full teaching review. Original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen097 fixture and full archive; all8447 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-097-native-test.apk"
    app = C / "artifacts" / "n1-batch-097-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch097GlyphTest", "N1Batch097ArticleTest",
                     "fullSingleImportOfflineSwordOneSupportThreeReciprocalPairsBothReadingsTenStrokesAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-713-native-compile.ps1", C / "preflight-713.ps1", VERIFICATION, UTILITY,
               L / "preflight-713.json", C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt",
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
        "schemaVersion": 1, "execution": 713, "batch": "097", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution713StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8447, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 123, "remainingAdditions": 1105, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; retained as evidence, not source whitespace changes.",
        "limits": [
            "Compiled test fixture and exact full archive only; no emulator launched or native/visual/phone acceptance claimed.",
            "Exact N1 has TWO curated wrong cards:剛/剖;則N2 is outside N1. Planned assertions capture ONE production fallback; semantic acceptance remains open.",
            "Only committed096 harness and approved control085 Markdown utilities used; no historical session-state helper access.",
            "Fresh712 host four cases retained, not rerun or relabelled native. Both original model sessions still require bounded rendered confirmation.",
            "No runtime change, publication, next batch, production app change or lock operation."
        ],
        "diagnostics": [
            "First in-memory preparation rejected the legitimate distractor word strength as stale old fixture text. Narrowed to old variable names; no fixture/archive or runtime edit had been written."
        ],
    }
    save(R / "docs" / "n1-sources" / "execution-713.json", evidence)
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-097-native/", "docs/n1-sources/execution-713.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-097-native-713-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-097-native-713-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-713.json")
    for item in evidence["provenance"]:
        assert sha(R.joinpath(*item["archive"].split("/"))) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 712 and state["stage"] == "batch-097-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 713, "checkpoint": 713, "batch": "097",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "batch-097-native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-713.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8447,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 123, "remainingAdditions": 1105, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=713, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution713CoordinatorCheckpoint"] = checkpoint
    state["batch097NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    reread = load(C / "progress.json")
    assert all(reread[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-713-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 713, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
