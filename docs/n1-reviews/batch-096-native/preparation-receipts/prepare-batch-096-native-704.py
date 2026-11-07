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
L = C / "logs" / "110fd75c-c109-4887-a762-9abe26b9f6f7"
HEAD = "58129f197c1f88a59ebb82c02cea9e9a0220377e"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "b26bcf9b328872b1575cf89e187973fea0a32a31"
VERSION = "54645b95fe8e939c"
WORK = C / "batch-096-native-704"
FIXTURE = WORK / "N1Batch096NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-095-native" / "N1Batch095NativeTest.kt"
UTILITY = C / "prepare-batch-085-native.py"
ARCHIVE = C / "artifacts" / "n1-batch-096-58129f19-envelope.zip"
VERIFICATION = C / "batch-096-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-096-native"
BEFORE = L / "progress-before-704.json"
NEXT = (
    "SAME096 execute frozen compiled native fixture and inspect actual PNGs next; preparation704 is NOT native acceptance. "
    "Read docs/n1-sources/execution-704.json and control/batch-096-native-fixture-verification.json. "
    "Require BOTH N1Batch096GlyphTest and N1Batch096ArticleTest terminal per-case0/no skips. "
    "Exact full archive58129f19/version54645b95fe8e939c/8444runtimehashes through productionContentSync ONCE: "
    "1119kanji/5072words/128N1/zeroProblems/acceptedRoomversion+readingepoch1. "
    "Inspect all28Han across FOUR production font families/systemfallback, especially冂/刂; "
    "112individual+8wholewordPaint probes/FOUR bounded Compose panels. Cmap/hasGlyph/rasterhashes NOT legibility/fallbackface evidence. "
    "All productionchoices exactly sturdy;unyielding strength vs削/剖/則; actual N1 includes削/剖 but NOT則N2, "
    "so ONE productionfallback requires actual semantic inspection. Inspect N1 UI and16-seed N1/All/boundedcustom/randomN1subset "
    "builder records; fallbacksemanticacceptance OPEN, wider custom/random pools not certified by textual review. "
    "TWELVE directwordguards from剛健 full imported word pool/custom/bothdirections/bothtargetorientations/16seeds "
    "(1536 planned builder checks). ONLYonごう/noKun offered/persistedGood/Done; full/Lite rawゴウ/[] and explicitゴウ/[] retained. "
    "TEN pinned strokes injectedtrace/recall/persistence; TWO complete articleprojections剛/剛健, "
    "ONE allmapped reciprocalpair/TWO directions, zeroactivatedbaselinepairs; SystemBack/offline/N1selection/meaning/reading/drawing. "
    "Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581ownership immediately before "
    "ownedreadonlyAPI35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/2048MiB/2cores; stop only ownedhelper. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Fresh703 JVM4/no skips retained. "
    "OriginalClaude de7596b6-1f69-43e0-b297-c3e600fa712a THEN GPT ca536738-97f2-4841-b985-321ce12b37c1 need serial bounded "
    "rendered confirmations, no newblindcredit. Parent19008 retains runner.lock; verifyliveancestry/session/checkpoint/exactsignedheads/"
    "whollyclean, NOchildreacquisition/delete/unlock/readprobe. Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. All currentmainnonrewritingmerge/surgicalreconciliation/"
    "changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPentryhash/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue gates remain. "
    "Published122/1228,1106remaining unchanged; physicalphone/generalrelease/whole-set outstanding. No097/runtimepublication/secondrunner."
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
    temp = C / "progress.704.tmp"
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
    assert count == 8444
    review = load(R / "docs" / "n1-reviews" / "batch-096-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        703, "continue", "batch-096-fresh-android-passed-awaiting-native", "096")
    role, runner = load(L / "preflight-704.json"), load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    assert role["decodedLauncherMatches"] and role["liveParentPid"] == 19008 and not role["lockTouched"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 703 and checkpoint["execution703CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution704StartingState"] = {
        "execution": 704, "batch": "096", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME096 full native fixture/archive preparation and compilation, normally signed LOCAL evidence; yield before native execution/visual review/publication/097.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final703 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-096-native-preparation-in-progress"
    state["nextAction"] = state["execution704StartingState"]["scope"]
    persist(state)
    print("Starting704 persisted; complete live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(UTILITY) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    assert sha(PRIOR) == "295e763b5b274e9ebaf09db5229a642d197b6e2a49b7dcce94cb0b21a4b7684d"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", UTILITY)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-096-draft-font-audit.json")
    names = audit["completeArticleScope"]
    assert names == ["kanji/剛.md", "words/剛健.md"]
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
                        if R.joinpath(*document.split("/")).parent.joinpath(match[1]).resolve() == R.joinpath(*destination.split("/")).resolve():
                            candidates.append(part.removeprefix("- "))
        assert len(candidates) == 1, (document, label, candidates)
        raw = candidates[0]
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        rendered = plain(" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_704" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_704")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("剛")')
    line('click("sturdy; unyielding strength")')
    display("kanji/剛.md", "kanji")
    to_word = follow("kanji/剛.md", "剛健", "words/剛健.md", "Common words", "gouken-forward")
    display("words/剛健.md", "gouken")
    from_word = follow("words/剛健.md", "剛", "kanji/剛.md", "How the kanji combine", "gou-reverse")
    line('section("Readings")')
    line('show(readingExample("ゴウ"), "gou-kanji-backlink")')
    back_to(from_word, "gou-system-back-to-word")
    back_to(to_word, "gouken-system-back-to-kanji")
    plan = load(R / "docs" / "n1-sources" / "batch-096-progress.json")["proposedDirectedLinkPlan"]
    assert len(offsets) == 2
    assert {(x["document"], x["destination"]) for x in offsets} == {(x["from"], x["to"]) for x in plan}
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "N1_BATCH_096_ARTICLE_PROJECTION\n" + text[end:]
    import yaml
    card = yaml.safe_load((R / "kanji" / "剛.md").read_text(encoding="utf-8").split("---", 2)[1])
    word = yaml.safe_load((R / "words" / "剛健.md").read_text(encoding="utf-8").split("---", 2)[1])
    exclusions = word["quiz_exclusions"]
    assert len(exclusions) == 12 and card["distractors"] == ["削", "剖", "則"]
    for old, new in [
        ("N1Batch095", "N1Batch096"), ("disposable095", "disposable096"), ("n1-095", "n1-096"),
        ("Batch 095", "Batch 096"), ("n1-batch-095-cc748347-envelope.zip", ARCHIVE.name),
        ("cc74834756847ad23fad6a721bb0a02ca859fa99", HEAD), ("463619d79972e9f2", VERSION),
        ("1118, updated.kanji", "1119, updated.kanji"), ("5071, updated.words", "5072, updated.words"),
        ("127, n1.size", "128, n1.size"), ("N1 · 127 cards", "N1 · 128 cards"),
        ("dissectionLookalikesAndScopedHan", "strengthLookalikesAndScopedHan"),
        ("fullSingleImportOfflineDissectionOneNewSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack",
         "fullSingleImportOfflineStrengthOneSupportOneReciprocalPairOneOnNoKunTenStrokesAndSystemBack"),
        ("dissection", "strength"), ("Dissection", "Strength"), ("dissect; split open", "sturdy; unyielding strength"),
        ('"剖"', '"剛"'), ('listOf("部", "倍", "副")', 'listOf("削", "剖", "則")'),
        ('listOf("ボウ")', 'listOf("ゴウ")'), ('listOf("ぼう")', 'listOf("ごう")'),
        ('"ぼう"', '"ごう"'), ("onぼう", "onごう"),
        ('put("mappedReciprocalPairs", 2)', 'put("mappedReciprocalPairs", 1)'),
        ('put("directedLinkTransitions", 4)', 'put("directedLinkTransitions", 2)'),
        ('put("completeArticleProjections", 3)', 'put("completeArticleProjections", 2)'),
        ('put("changedReusedArticles", 1)', 'put("changedReusedArticles", 0)'),
        ('put("newDirectWordGuardPairs", 3)', 'put("newDirectWordGuardPairs", 12)'),
        ("assertEquals(384, directGuardChecks.length())", "assertEquals(1536, directGuardChecks.length())"),
        ("kotlin.random.Random(693)", "kotlin.random.Random(704)"),
        ("onlyOnBouNoKunPersistedGoodAndDone", "onlyOnGouNoKunPersistedGoodAndDone"),
    ]:
        assert old in text, old
        text = text.replace(old, new)
    begin = text.index("        val expectedMeanings =")
    end = text.index("        val all =", begin)
    expected = {"剛": card["title"]}
    levels = {}
    for name in card["distractors"]:
        entry = yaml.safe_load((R / "kanji" / (name + ".md")).read_text(encoding="utf-8").split("---", 2)[1])
        expected[name] = entry["title"]
        levels[name] = entry["jlpt"]
    assert levels == {"削": 1, "剖": 1, "則": 2}
    text = text[:begin] + "        val expectedMeanings = mapOf(\n" + "".join(
        f"            {quote(k)} to {quote(v)},\n" for k, v in expected.items()) + "        )\n" + text[end:]
    text = text.replace('assertEquals(emptyList<String>(), curatedIds.filter { id -> n1.any { it.kanji == id } })',
                        'assertEquals(listOf("削", "剖"), curatedIds.filter { id -> n1.any { it.kanji == id } })')
    text = text.replace('val expectedAvailable = if (poolName == "N1" || poolName == "randomN1Subset") 0 else 3',
                        'val expectedAvailable = when (poolName) {\n'
                        '                "N1" -> 2\n'
                        '                "All", "boundedCustom" -> 3\n'
                        '                else -> curatedIds.count { id -> randomSubset.any { it.kanji == id } }\n'
                        '            }')
    begin = text.index("        val importedStrength =")
    end = text.index("        for ((leftId, rightId) in guardPairs)", begin)
    text = text[:begin] + (
        '        val importedStrength = words.single { it.word == "剛健" }\n'
        f'        assertEquals(listOf({", ".join(map(quote, exclusions))}), importedStrength.quizExclusions)\n'
        '        assertEquals("ごうけん", importedStrength.reading)\n'
        '        assertNull(importedStrength.jlpt)\n'
        '        val directGuardChecks = JSONArray()\n'
        '        val guardPairs = listOf(' + ", ".join(f'"剛健" to {quote(w)}' for w in exclusions) + ')\n'
    ) + text[end:]
    text = text.replace('assertFalse(meaning.options.any { it.kanji in setOf("部", "倍", "副") })',
                        'assertTrue(meaning.options.any { it.kanji == "削" })\n'
                        '            assertTrue(meaning.options.any { it.kanji == "剖" })\n'
                        '            assertFalse(meaning.options.any { it.kanji == "則" })')
    text = text.replace('put("actualN1CuratedAvailable", 0).put("actualN1FallbackOptions", 3)',
                        'put("actualN1CuratedAvailable", 2).put("actualN1FallbackOptions", 1)')
    text = text.replace("only 剖 meaning", "only 剛 meaning").replace("good 剖 meaning", "good 剛 meaning")
    glyphs = audit["actualHan"]
    assert len(glyphs) == 28
    pages = [" ".join(glyphs[i:i + 12]) for i in range(0, len(glyphs), 12)]
    pages.append("剛 削 剖 則 岡 冂 山 刀 刂 剛健 剛性 剛毛")
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", 'for (word in listOf("剛健", "質実剛健"))', text, count=1)
    text = text.replace("all 32 scoped Han; focused 剖/部/倍/副/立/口/刀/刂/亻/阝/解",
                        "all 28 scoped Han; focused 剛/削/剖/則/岡/冂/山/刀/刂")
    text = text.replace("32 actual scoped Han; 亻/刂/阝 absent from all three bundled cmaps",
                        "28 actual scoped Han; 冂/刂 absent from all three bundled cmaps")
    text = text.replace("assertEquals(136, rows.length())", "assertEquals(120, rows.length())")
    text = text.replace('put("individualGlyphProbes", 128)', 'put("individualGlyphProbes", 112)')
    text = text.replace("N1_BATCH_096_ARTICLE_PROJECTION", "\n".join(lines))
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1 and "ContentParser.parse" not in text
    for stale in ["095", "ボウ", "ぼう", "解剖", "部", "倍", "副", "dissection", "cc748347", "463619d7"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["冂", "刂"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1119, "words": 5072, "n1": 128}, counts
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-096/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-096/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-096/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-096/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8444 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-095.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 704, "batch": "096", "status": "prepared-not-executed",
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
        "completeArticleProjections": 2, "changedReusedScope": [],
        "mappedReciprocalPairs": 1, "mappedDirectedTransitions": 2, "activatedBaselinePairs": 0,
        "plannedGlyphs": glyphs, "plannedWholeWords": ["剛健", "質実剛健"], "plannedComposePanels": pages,
        "plannedNativePaintProbes": 112, "plannedWholeWordRasterProbes": 8, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ゴウ"], "kun": []}, "curatedReadings": {"on": ["ゴウ"], "kun": []},
        "normalizedQuizKeys": {"on": ["ごう"], "kun": []}, "newDirectWordExclusionPairs": 12,
        "directGuardPairs": [["剛健", w] for w in exclusions], "directGuardPlannedBuilderChecks": 1536,
        "directGuardScopes": ["All", "boundedCustom"], "directGuardDirections": ["JpToEn", "EnToJp"],
        "directGuardBothTargetOrientations": True,
        "kanjiChoicePlannedChecks": 64, "kanjiChoicePools": ["N1", "All", "boundedCustom", "randomN1Subset"],
        "n1CuratedAvailable": ["削", "剖"], "n1MissingCurated": ["則"], "n1FallbackCount": 1,
        "allCuratedAvailable": ["削", "剖", "則"], "allFallbackCount": 0,
        "fallbackSemanticAcceptance": "OPEN pending actual imported/UI options and evidence-based original-session confirmations",
        "pendingCmapAbsences": ["冂", "刂"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1 has TWO curated wrong cards;則N2 is excluded so ONE production fallback is captured, NOT assumed wrong or accepted. Wider custom/random pools need actual semantic inspection. Twelve direct guards through actual builder on imported words, not learner word-session UI. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. Original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen096 fixture and full archive; all8444 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-096-native-test.apk"
    app = C / "artifacts" / "n1-batch-096-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch096GlyphTest", "N1Batch096ArticleTest",
                     "fullSingleImportOfflineStrengthOneSupportOneReciprocalPairOneOnNoKunTenStrokesAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-704-native-compile.ps1", C / "preflight-704.ps1", VERIFICATION, UTILITY,
               L / "preflight-704.json", C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt",
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
        "schemaVersion": 1, "execution": 704, "batch": "096", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution704StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8444, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 122, "remainingAdditions": 1106, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; retained as evidence, not source whitespace changes.",
        "diagnostics": [
            "Exact N1 has TWO curated wrong cards:削/剖;則N2 is outside N1. Planned assertions capture ONE production fallback; actual semantic acceptance remains open.",
            "Only committed095 harness and approved control085 Markdown utilities used; no historical session-state helper access.",
            "Initial console inspection needed explicit UTF-8 after a cp1252 print failure; entire request had already loaded/decoded. No permission denial or checkpoint loss.",
            "First in-memory preparation rejected the valid new distractor label dissect; split open as if stale prior content. Narrowed the stale-token assertion; no fixture/archive had been written and no content or gate changed.",
            "Native execution and fresh device/port ownership checks deliberately deferred to next bounded checkpoint; no emulator launched."
        ],
    }
    save(R / "docs" / "n1-sources" / "execution-704.json", evidence)
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-096-native/", "docs/n1-sources/execution-704.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-096-native-704-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-096-native-704-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-704.json")
    for item in evidence["provenance"]:
        assert sha(R.joinpath(*item["archive"].split("/"))) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 703 and state["stage"] == "batch-096-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 704, "checkpoint": 704, "batch": "096",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-704.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8444,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 122, "remainingAdditions": 1106, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=704, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution704CoordinatorCheckpoint"] = checkpoint
    state["batch096NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    reread = load(C / "progress.json")
    assert all(reread[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-704-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 704, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
