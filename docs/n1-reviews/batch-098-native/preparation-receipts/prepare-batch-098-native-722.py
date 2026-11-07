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
L = C / "logs" / "9b6504c7-7546-4384-b402-c83f56ee5497"
HEAD = "6cca181b977144603296506cfe0b9ed744e2d193"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "233d3add2b90fcb98f9706b8901aa936fc6e56e7"
VERSION = "0cbdc2723b0433f2"
WORK = C / "batch-098-native-722"
FIXTURE = WORK / "N1Batch098NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-096-native" / "N1Batch096NativeTest.kt"
UTILITY = C / "prepare-batch-085-native.py"
ARCHIVE = C / "artifacts" / "n1-batch-098-6cca181b-envelope.zip"
VERIFICATION = C / "batch-098-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-098-native"
BEFORE = L / "progress-before-722.json"
STAGE = "batch-098-native-prepared-compiled-not-executed"
NEXT = (
    "SAME098 execute frozen compiled native fixture and inspect actual PNGs next; preparation722 is NOT native acceptance. "
    "Read docs/n1-sources/execution-722.json and control/batch-098-native-fixture-verification.json. "
    "Require BOTH N1Batch098GlyphTest and N1Batch098ArticleTest terminal per-case0/no skips. "
    "Exact full archive6cca181b/version0cbdc2723b0433f2/8449runtimehashes through productionContentSync ONCE: "
    "1121kanji/5073words/130N1/zeroProblems/acceptedRoomversion+readingepoch1. "
    "All19Han across FOUR production font families/systemfallback, especially刂/氵: "
    "76individual+8wholewordPaint probes/THREE bounded Compose panels; actual legibility/lookalike inspection required, "
    "cmap/hasGlyph/rasterhashes NOT legibility/fallbackface evidence. "
    "All productionchoices exactly medicinalpreparation;chemicalagent vs済/剛/則; actualN1 includes剛 but NOT済N3/則N2, "
    "so TWO productionfallbacks require actual semantic inspection. Inspect N1UI and16-seed N1/All/boundedcustom/randomN1subset "
    "builder records; fallbacksemanticacceptance OPEN, wider custom/random pools not certified by textualreview. "
    "Existing洗剤-せっけん directguard preserved (NO newguard):128planned importedbuilderchecks across All/custom/"
    "bothdirections/bothtargetorientations/16seeds; unchanged洗剤せんざい N2metadata. "
    "Full/Lite rawザイ/スイ/セイ andかる/けず.る retained; explicit quizザイ/[] only, "
    "ざい offered/persistedGood/Done and NO kun/sourceonly questions. TEN pinned strokes injectedtrace/recall/persistence; "
    "ONE complete articleprojection剤 plus exact reused洗剤component/洗commonword changes, "
    "TWO allmapped reciprocalpairs/FOUR directions/ONEactivatedbaselinepair; SystemBack/offline/N1selection/meaning/readings/drawing. "
    "Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581ownership immediately before "
    "ownedreadonly API35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/2048MiB/2cores; stop only ownedhelper. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Fresh721 JVM4/no skips retained. "
    "OriginalClaude d41cdccb-18bc-4302-803f-803d7bd4a007 THEN GPT33216339-ddd8-411a-8aca-b73da1a3bae7 "
    "need serial bounded rendered confirmations; no newblindcredit. Parent19008 retains runner.lock; verifyliveancestry/session/"
    "checkpoint/exactsignedheads/whollyclean, NOchildreacquisition/delete/unlock/readprobe. "
    "Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. All currentmainnonrewritingmerge/"
    "surgicalreconciliation/changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIPentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue gates remain. Published124/1228,1104remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No099/runtimepublication/secondrunner."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root), str(root)
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)


def persist(state):
    temp = C / "progress.722.tmp"
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
                actual = sha(path) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                } else sha256(path)
                assert actual == digest, name
                count += 1
    assert count == 8449
    review = load(R / "docs" / "n1-reviews" / "batch-098-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        721, "continue", "batch-098-fresh-android-passed-awaiting-native", "098"
    )
    role, runner = load(L / "preflight-722.json"), load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    assert role["decodedLauncherMatches"] and role["liveParentPid"] == 19008 and not role["lockTouched"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["checkpoint"] == 721 and checkpoint["execution721CoordinatorCheckpoint"]["savedCommit"] == HEAD
    subprocess.run(["git", "-C", str(R), "fetch", "--quiet", "origin", "main"], check=True)
    runtime()
    save(BEFORE, state)
    state["execution722StartingState"] = {
        "execution": 722, "batch": "098", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME098 full native fixture/archive preparation and compilation, normally signed LOCAL evidence; yield before native execution/visual review/publication/099.",
        "request": {
            "sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
            "characters": len(request), "lines": len(request.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final721 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-098-native-preparation-in-progress"
    state["nextAction"] = state["execution722StartingState"]["scope"]
    persist(state)
    print("Starting722 persisted; complete live history retained.")


def prepare():
    import yaml
    from fontTools.ttLib import TTFont

    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(UTILITY) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    assert sha(PRIOR) == "e55f53f31984dc2024657ea37e06f9c43e36277f6f2ab696aa14305697021c4c"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", UTILITY)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-098-draft-font-audit.json")
    names = audit["completeArticleScope"]
    assert names == ["kanji/剤.md"]
    projected = names + ["words/洗剤.md", "kanji/洗.md"]
    docs = {name: blocks(R.joinpath(*name.split("/"))) for name in projected}
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def show(document, kind, value, step, occurrence=0):
        count = sum(v == value for k, v in docs[document]
                    if (k == "table") == (kind == "table") and k != "heading")
        assert count >= 1 and 0 <= occurrence < count
        assert count == 1 or kind == "table", (document, value)
        selector = "readingExample" if kind == "table" else "articleBullet"
        extra = f", occurrence = {occurrence}, expectedCount = {count}" if count > 1 else ""
        line(f"show({selector}({quote(value)}), {quote(step)}{extra})")
        selectors.append({"document": document, "kind": kind, "target": value, "step": step,
                          "occurrence": occurrence, "expectedCount": count})

    def display(document, slug):
        line(f"await({quote(docs[document][0][1])})")
        cell = 0
        for index, (kind, value) in enumerate(docs[document][1:], 1):
            if kind == "heading":
                line(f"section({quote(value)})")
            elif kind == "table":
                cell += 1
                if cell > 3 and cell % 3 != 2:
                    occurrence = sum(k == "table" and v == value for k, v in docs[document][1:index])
                    show(document, kind, value, f"{slug}-{index:02}", occurrence)
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_722" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_722")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("剤")')
    line('click("medicinal preparation; chemical agent")')
    display("kanji/剤.md", "kanji")
    to_word = follow("kanji/剤.md", "洗剤", "words/洗剤.md", "Common words", "senzai-forward")
    line(f"await({quote(docs['words/洗剤.md'][0][1])})")
    from_word = follow("words/洗剤.md", "剤", "kanji/剤.md", "How the kanji combine", "zai-reverse")
    line('section("Readings")')
    line('show(readingExample("ザイ"), "zai-kanji-backlink")')
    back_to(from_word, "zai-system-back-to-word")
    to_sen = follow("words/洗剤.md", "洗", "kanji/洗.md", "How the kanji combine", "sen-reverse")
    line(f"await({quote(docs['kanji/洗.md'][0][1])})")
    from_sen = follow("kanji/洗.md", "洗剤", "words/洗剤.md", "Common words", "sen-forward")
    line('section("How the kanji combine")')
    line(f"show(articleBullet({quote(to_sen['renderedText'])}), \"senzai-component-return\")")
    back_to(from_sen, "sen-system-back-to-kanji")
    back_to(to_sen, "sen-system-back-to-word")
    back_to(to_word, "senzai-system-back-to-zai")
    plan = load(R / "docs" / "n1-sources" / "batch-098-progress.json")["proposedDirectedLinkPlan"]
    assert len(offsets) == 4
    assert {(x["document"], x["destination"]) for x in offsets} == {(x["from"], x["to"]) for x in plan}
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "N1_BATCH_098_ARTICLE_PROJECTION\n" + text[end:]
    card = yaml.safe_load((R / "kanji" / "剤.md").read_text(encoding="utf-8").split("---", 2)[1])
    word = yaml.safe_load((R / "words" / "洗剤.md").read_text(encoding="utf-8").split("---", 2)[1])
    assert word["quiz_exclusions"] == ["せっけん"] and word["jlpt"] == 2
    assert card["distractors"] == ["済", "剛", "則"]

    def replace(old, new):
        nonlocal text
        assert old in text, old
        text = text.replace(old, new)

    for old, new in [
        ("N1Batch096", "N1Batch098"), ("disposable096", "disposable098"), ("n1-096", "n1-098"),
        ("Batch 096", "Batch 098"), ("n1-batch-096-58129f19-envelope.zip", ARCHIVE.name),
        ("58129f197c1f88a59ebb82c02cea9e9a0220377e", HEAD), ("54645b95fe8e939c", VERSION),
        ("1119, updated.kanji", "1121, updated.kanji"), ("5072, updated.words", "5073, updated.words"),
        ("128, n1.size", "130, n1.size"), ("N1 · 128 cards", "N1 · 130 cards"),
        ("strengthLookalikesAndScopedHan", "agentLookalikesAndScopedHan"),
        ("fullSingleImportOfflineStrengthOneSupportOneReciprocalPairOneOnNoKunTenStrokesAndSystemBack",
         "fullSingleImportOfflineAgentReusedSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack"),
        ("strength", "agent"), ("Strength", "Agent"),
        ("sturdy; unyielding agent", "medicinal preparation; chemical agent"),
        ('"剛"', '"剤"'), ('listOf("削", "剖", "則")', 'listOf("済", "剛", "則")'),
        ('listOf("ゴウ")', 'listOf("ザイ", "スイ", "セイ")'),
        ('listOf("ごう")', 'listOf("ざい")'), ('"ごう"', '"ざい"'), ("onごう", "onざい"),
        ('put("mappedReciprocalPairs", 1)', 'put("mappedReciprocalPairs", 2)'),
        ('put("directedLinkTransitions", 2)', 'put("directedLinkTransitions", 4)'),
        ('put("activatedBaselinePairs", 0)', 'put("activatedBaselinePairs", 1)'),
        ('put("completeArticleProjections", 2)', 'put("completeArticleProjections", 1)'),
        ('put("changedReusedArticles", 0)', 'put("changedReusedArticles", 2)'),
        ('put("newDirectWordGuardPairs", 12)', 'put("newDirectWordGuardPairs", 0).put("preservedDirectWordGuardPairs", 1)'),
        ("assertEquals(1536, directGuardChecks.length())", "assertEquals(128, directGuardChecks.length())"),
        ("kotlin.random.Random(704)", "kotlin.random.Random(722)"),
        ("onlyOnGouNoKunPersistedGoodAndDone", "onlyOnZaiNoKunPersistedGoodAndDone"),
    ]:
        replace(old, new)
    for owner in ("agent", "card"):
        replace(f"assertEquals(emptyList<String>(), {owner}.kunyomi.splitSep())",
                f'assertEquals(listOf("かる", "けず.る"), {owner}.kunyomi.splitSep())')
        replace(f'assertEquals(listOf("ザイ", "スイ", "セイ"), {owner}.quizOnyomi?.splitSep())',
                f'assertEquals(listOf("ザイ"), {owner}.quizOnyomi?.splitSep())')
    begin = text.index("        val expectedMeanings =")
    end = text.index("        val all =", begin)
    expected, levels = {"剤": card["title"]}, {}
    for name in card["distractors"]:
        entry = yaml.safe_load((R / "kanji" / (name + ".md")).read_text(encoding="utf-8").split("---", 2)[1])
        expected[name], levels[name] = entry["title"], entry["jlpt"]
    assert levels == {"済": 3, "剛": 1, "則": 2}
    text = text[:begin] + "        val expectedMeanings = mapOf(\n" + "".join(
        f"            {quote(k)} to {quote(v)},\n" for k, v in expected.items()) + "        )\n" + text[end:]
    replace('listOf("削", "剖"), curatedIds.filter', 'listOf("剛"), curatedIds.filter')
    replace('"N1" -> 2', '"N1" -> 1')
    begin = text.index("        val importedAgent =")
    end = text.index("        for ((leftId, rightId) in guardPairs)", begin)
    text = text[:begin] + (
        '        val importedAgent = words.single { it.word == "洗剤" }\n'
        '        assertEquals(listOf("せっけん"), importedAgent.quizExclusions)\n'
        '        assertEquals("せんざい", importedAgent.reading)\n'
        '        assertEquals(2, importedAgent.jlpt)\n'
        '        val directGuardChecks = JSONArray()\n'
        '        val guardPairs = listOf("洗剤" to "せっけん")\n'
    ) + text[end:]
    replace("only 剛 meaning", "only 剤 meaning")
    replace("good 剛 meaning", "good 剤 meaning")
    replace('assertTrue(meaning.options.any { it.kanji == "削" })',
            'assertFalse(meaning.options.any { it.kanji == "済" })')
    replace('assertTrue(meaning.options.any { it.kanji == "剖" })',
            'assertTrue(meaning.options.any { it.kanji == "剛" })')
    replace('put("actualN1CuratedAvailable", 2).put("actualN1FallbackOptions", 1)',
            'put("actualN1CuratedAvailable", 1).put("actualN1FallbackOptions", 2)')
    glyphs = audit["actualHan"]
    assert len(glyphs) == 19
    pages = [" ".join(glyphs[i:i + 12]) for i in range(0, len(glyphs), 12)]
    pages.append("剤 済 剛 則 斉 刀 刂 氵 洗 洗剤 製剤 推進剤")
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", 'for (word in listOf("洗剤", "推進剤"))', text, count=1)
    replace("all 28 scoped Han; focused 剛/削/剖/則/岡/冂/山/刀/刂", "all 19 scoped Han; focused 剤/済/剛/則/斉/刀/刂/氵/洗")
    replace("28 actual scoped Han; 冂/刂 absent from all three bundled cmaps",
            "19 actual scoped Han; 刂/氵 absent from all three bundled cmaps")
    replace("four bounded Compose panels", "three bounded Compose panels")
    replace("assertEquals(120, rows.length())", "assertEquals(84, rows.length())")
    replace('put("individualGlyphProbes", 112)', 'put("individualGlyphProbes", 76)')
    replace('put("panels", 4)', 'put("panels", 3)')
    replace("private fun show(matcher: SemanticsMatcher, step: String) {",
            "private fun show(matcher: SemanticsMatcher, step: String, occurrence: Int = 0, expectedCount: Int = 1) {")
    replace("        val target = await(matcher)\n        target.performScrollTo()",
            "        rule.onAllNodes(matcher).assertCountEquals(expectedCount)\n"
            "        val target = rule.onAllNodes(matcher)[occurrence]\n        target.performScrollTo()")
    text = text.replace("N1_BATCH_098_ARTICLE_PROJECTION", "\n".join(lines))
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1 and "ContentParser.parse" not in text
    for stale in ["096", "ゴウ", "ごう", "剛健", "val strength", "importedStrength", "58129f19", "54645b95"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    assert {s["target"] for s in selectors if s["kind"] == "table"} >= {
        "ザイ", "スイ", "セイ", "かる", "けず.る", "洗剤 せんざい — detergent; cleaning agent"
    }
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["刂", "氵"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
        "words": sum(n.startswith("words/") for n in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (R / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1121, "words": 5073, "n1": 130}, counts
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-098/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-098/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-098/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-098/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8449 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-096.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2
    )), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 722, "batch": "098", "status": "prepared-not-executed",
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
        "articleFiles": [{"path": n, "sha256": sha(R.joinpath(*n.split("/"))),
                          "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 1, "changedReusedScope": audit["changedReusedScope"],
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4, "activatedBaselinePairs": 1,
        "plannedGlyphs": glyphs, "plannedWholeWords": ["洗剤", "推進剤"], "plannedComposePanels": pages,
        "plannedNativePaintProbes": 76, "plannedWholeWordRasterProbes": 8, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ザイ", "スイ", "セイ"], "kun": ["かる", "けず.る"]},
        "curatedReadings": {"on": ["ザイ"], "kun": []}, "normalizedQuizKeys": {"on": ["ざい"], "kun": []},
        "newDirectWordExclusionPairs": 0, "preservedDirectWordExclusionPairs": 1,
        "directGuardPairs": [["洗剤", "せっけん"]], "directGuardPlannedBuilderChecks": 128,
        "directGuardScopes": ["All", "boundedCustom"], "directGuardDirections": ["JpToEn", "EnToJp"],
        "directGuardBothTargetOrientations": True,
        "kanjiChoicePlannedChecks": 64, "kanjiChoicePools": ["N1", "All", "boundedCustom", "randomN1Subset"],
        "expectedAllMeaningLabels": expected,
        "n1CuratedAvailable": ["剛"], "n1MissingCurated": ["済", "則"], "n1FallbackCount": 2,
        "allCuratedAvailable": ["済", "剛", "則"], "allFallbackCount": 0,
        "fallbackSemanticAcceptance": "OPEN pending actual imported/UI options and evidence-based original-session confirmations",
        "pendingCmapAbsences": ["刂", "氵"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1 has ONE curated wrong card:剛;済N3/則N2 are excluded so TWO production fallbacks are captured, NOT assumed wrong or accepted. Wider custom/random pools need actual semantic inspection. Existing direct guard through actual builder on imported words, not learner word-session UI; no new word title/guard. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. Reused article scope is exact changed passages and required link destinations, not fresh full teaching review. Original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen098 fixture and full archive; all8449 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-098-native-test.apk"
    app = C / "artifacts" / "n1-batch-098-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch098GlyphTest", "N1Batch098ArticleTest",
                     "fullSingleImportOfflineAgentReusedSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    initial = C / "batch-098-native-722-initial-table-projection"
    initial_receipt = load(initial / "initial-fixture-verification.json")
    initial_archive = C / "artifacts" / "n1-batch-098-6cca181b-initial-table-envelope.zip"
    assert sha(initial / FIXTURE.name) == initial_receipt["fixtureSha256"]
    assert sha(initial_archive) == initial_receipt["archiveSha256"] == sha(ARCHIVE)
    shutil.copytree(initial, FOLDER / "initial-table-projection")
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [
        Path(__file__), C / "run-722-native-compile.ps1", C / "preflight-722.ps1", VERIFICATION, UTILITY,
        L / "preflight-722.json", C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt",
        *[L / n for n in ["native-compile-command.json", "native-compile-start.txt",
                          "native-compile-end.txt", "native-compile-exit.txt"]],
    ]
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
    save(R / "docs" / "n1-sources" / "execution-722.json", {
        "schemaVersion": 1, "execution": 722, "batch": "098", "status": STAGE,
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution722StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8449, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 124, "remainingAdditions": 1104, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "initialPreparationPreserved": {
            "fixture": (FOLDER / "initial-table-projection" / FIXTURE.name).relative_to(R).as_posix(),
            "fixtureSha256": initial_receipt["fixtureSha256"],
            "originalReceipt": (FOLDER / "initial-table-projection" / "initial-fixture-verification.json").relative_to(R).as_posix(),
            "archiveRelocatedTo": str(initial_archive), "archiveSha256": sha(initial_archive),
            "compiledOrExecuted": False,
            "disposition": "Before compilation, inspection found first-column-only captures insufficient to establish complete source-only table visibility. Final fixture additionally captures every example cell, including all three identical cells by checked occurrence/count. Initial receipt and fixture retained unmodified; final archive bytes identical.",
        },
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; retained as evidence, not source whitespace changes.",
        "limits": [
            "Compiled test fixture and exact full archive only; no emulator launched or native/visual/phone acceptance claimed.",
            "Exact N1 has ONE curated wrong card:剛;済N3/則N2 are outside N1. Planned assertions capture TWO production fallbacks; semantic acceptance remains open.",
            "Only committed096 harness and approved control085 Markdown utilities used; no historical session-state helper access.",
            "Fresh721 host four cases retained, not rerun or relabelled native. Both original model sessions still require bounded rendered confirmation.",
            "No runtime change, publication, next batch, production app change or lock operation.",
        ],
        "diagnostics": [
            "First in-memory preparation failed the exact level assertion:済 is preserved N3, not N1. No fixture/archive/runtime edit had been written. Corrected planned N1 availability to剛 only and TWO fallbacks; required actual semantic inspection remains open."
        ],
    })
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-098-native/", "docs/n1-sources/execution-722.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-098-native-722-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-098-native-722-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-722.json")
    for item in evidence["provenance"]:
        assert sha(R.joinpath(*item["archive"].split("/"))) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 721 and state["stage"] == "batch-098-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 722, "checkpoint": 722, "batch": "098",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-722.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8449,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 124, "remainingAdditions": 1104, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=722, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution722CoordinatorCheckpoint"] = checkpoint
    state["batch098NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    reread = load(C / "progress.json")
    assert all(reread[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-722-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 722, "savedCommit": saved, "status": "continue",
                      "stage": STAGE, "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
