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
L = C / "logs" / "49dac17d-7012-48cb-b241-ce67cb94bf4e"
HEAD = "cc74834756847ad23fad6a721bb0a02ca859fa99"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "8c4e16500d57749f90f08c196fbb8980981967a6"
VERSION = "463619d79972e9f2"
WORK = C / "batch-095-native-693"
FIXTURE = WORK / "N1Batch095NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-094-native" / "N1Batch094NativeTest.kt"
READING_PRIOR = R / "docs" / "n1-reviews" / "batch-093-native" / "N1Batch093NativeTest.kt"
UTILITY = C / "prepare-batch-085-native.py"
ARCHIVE = C / "artifacts" / "n1-batch-095-cc748347-envelope.zip"
VERIFICATION = C / "batch-095-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-095-native"
BEFORE = L / "progress-before-693.json"
NEXT = (
    "SAME095 execute frozen compiled native fixture and inspect actual PNGs next; preparation693 is NOT native acceptance. "
    "Read docs/n1-sources/execution-693.json and control/batch-095-native-fixture-verification.json. "
    "Require BOTH N1Batch095GlyphTest and N1Batch095ArticleTest terminal per-case0/no skips. "
    "Exact full archivecc748347/version463619d79972e9f2/8441runtimehashes through productionContentSync ONCE: "
    "1118kanji/5071words/127N1/zeroProblems/acceptedRoomversion+readingepoch1. "
    "Inspect all32Han across FOURproductionfont families/systemfallback, especially亻/刂/阝; "
    "128individual+8wholewordPaint probes/FOUR bounded Compose panels. Cmap/hasGlyph/rasterhashes NOT legibility/fallbackface evidence. "
    "All productionchoices exactly dissect;split open vs部/倍/副; actual N1 has NONE of those curated "
    "(部N3/倍N2/副N2 excluded), so THREE productionfallbacks require actual semantic inspection. "
    "Inspect N1 UI and16-seed N1/All/boundedcustom/randomN1subset builder records; fallbacksemanticacceptance OPEN. "
    "THREE directwordguards解剖/分析,解剖/分解,解剖/検査 through imported fullsource/custom/bothdirections/"
    "bothtargetorientations/16seeds. ONLYonぼう/noKun offered/persistedGood/Done; full/Lite rawボウ/[] and explicitボウ/[] retained. "
    "TEN pinned strokes injectedtrace/recall/persistence; THREE complete articleprojections剖/解剖/解, "
    "TWO allmapped reciprocalpairs/FOUR directions, zeroactivatedbaselinepairs; SystemBack/offline/N1selection/meaning/reading/drawing. "
    "Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581ownership immediately before "
    "ownedreadonlyAPI35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/2048MiB/2cores; stop only ownedhelper. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Fresh692 JVM4/no skips retained. "
    "OriginalClaude ede78c28-e889-47b5-be0b-21533da61551 THEN GPT ee7498e0-d3ad-46bf-bbc9-82761892cab0 need serial bounded rendered confirmations, "
    "no newblindcredit. Parent19008 retains runner.lock; verifyliveancestry/session/checkpoint/exactsignedheads/whollyclean, "
    "NOchildreacquisition/delete/unlock. Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper access. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. FreshoriginMain da374717 now advances publishedd6a26190; "
    "later nonrewritingmerge/surgicalreconciliation/changedteachingreview/combinedchecks/normalsigning/ownerfastforward/"
    "terminalgreenCI/EVERYimmutablepublicZIPentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue gates remain. Published121/1228,1107remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No096, runtimepublication or secondrunner."
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
    temp = C / "progress.693.tmp"
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
    assert count == 8441
    review = load(R / "docs" / "n1-reviews" / "batch-095-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        692, "continue", "fresh-android-passed-awaiting-native", "095")
    role, runner = load(L / "preflight-693.json"), load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    assert role["decodedLauncherMatches"] and role["liveParentPid"] == 19008 and not role["lockTouched"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 692 and checkpoint["execution692CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution693StartingState"] = {
        "execution": 693, "batch": "095", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME095 full native fixture/archive preparation and compilation, normally signed LOCAL evidence; yield before native execution/visual review/publication/096.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final692 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-095-native-preparation-in-progress"
    state["nextAction"] = state["execution693StartingState"]["scope"]
    persist(state)
    print("Starting693 persisted; full live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(UTILITY) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", UTILITY)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-095-draft-font-audit.json")
    names = audit["completeArticleScope"]
    assert names == ["kanji/剖.md", "words/解剖.md", "kanji/解.md"]
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_693" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_693")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("剖")')
    line('click("dissect; split open")')
    display("kanji/剖.md", "kanji")
    to_word = follow("kanji/剖.md", "解剖", "words/解剖.md", "Common words", "kaibou-forward")
    display("words/解剖.md", "kaibou")
    from_word = follow("words/解剖.md", "剖", "kanji/剖.md", "How the kanji combine", "bou-reverse")
    line('section("Readings")')
    line('show(readingExample("ボウ"), "bou-kanji-backlink")')
    back_to(from_word, "bou-system-back-to-word")
    to_kai = follow("words/解剖.md", "解", "kanji/解.md", "How the kanji combine", "kai-reverse")
    display("kanji/解.md", "kai")
    from_kai = follow("kanji/解.md", "解剖", "words/解剖.md", "Common words", "kai-kaibou-forward")
    line('section("Meaning")')
    line('capture("kai-kaibou-backlink")')
    back_to(from_kai, "kai-system-back-to-kanji")
    back_to(to_kai, "kai-system-back-to-word")
    back_to(to_word, "kaibou-system-back-to-kanji")
    plan = load(R / "docs" / "n1-sources" / "batch-095-progress.json")["proposedDirectedLinkPlan"]
    assert len(offsets) == 4
    assert {(x["document"], x["destination"]) for x in offsets} == {(x["from"], x["to"]) for x in plan}
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "N1_BATCH_095_ARTICLE_PROJECTION\n" + text[end:]
    begin = text.index("        val importedShave =")
    end = text.index("        val directGuardChecks =", begin)
    text = text[:begin] + '''        val importedDissection = words.single { it.word == "解剖" }
        assertEquals(listOf("分析", "分解", "検査"), importedDissection.quizExclusions)
        assertEquals("かいぼう", importedDissection.reading)
        assertNull(importedDissection.jlpt)
''' + text[end:]
    text = text.replace('listOf("削る" to "除く", "削る" to "外す", "削除" to "省く")',
                        'listOf("解剖" to "分析", "解剖" to "分解", "解剖" to "検査")')
    reading = READING_PRIOR.read_text(encoding="utf-8")
    begin = text.index("            val answeredKeys =")
    end = text.index('            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))', begin)
    rb = reading.index("            val answeredKeys =")
    re_ = reading.index('            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))', rb)
    text = text[:begin] + reading[rb:re_] + text[end:]
    for old, new in [
        ("N1Batch094", "N1Batch095"), ("disposable094", "disposable095"), ("n1-094", "n1-095"),
        ("Batch 094", "Batch 095"), ("n1-batch-094-18ad4bed-envelope.zip", ARCHIVE.name),
        ("18ad4bed3264a7c30e04cd60edbd85264a5b39d8", HEAD), ("eeae47753a460f72", VERSION),
        ("1117, updated.kanji", "1118, updated.kanji"), ("5070, updated.words", "5071, updated.words"),
        ("126, n1.size", "127, n1.size"), ("N1 · 126 cards", "N1 · 127 cards"),
        ("shavingLookalikesAndScopedHan", "dissectionLookalikesAndScopedHan"),
        ("fullSingleImportOfflineShavingTwoReusedN2ThreeReciprocalPairsBothReadingsNineStrokesAndSystemBack",
         "fullSingleImportOfflineDissectionOneNewSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack"),
        ("val shaving =", "val dissection ="), ("shaving.", "dissection."),
        ("shaving / look-alikes", "dissection / look-alikes"),
        ('"削"', '"剖"'), ("shave; sharpen; pare", "dissect; split open"),
        ('listOf("前", "判", "刑")', 'listOf("部", "倍", "副")'),
        ('listOf("サク")', 'listOf("ボウ")'),
        ('listOf("けず.る", "はつ.る", "そ.ぐ")', 'emptyList<String>()'),
        ('listOf("けず.る")', 'emptyList<String>()'),
        ('listOf("さく")', 'listOf("ぼう")'),
        ('listOf("けずる")', 'emptyList<String>()'),
        ('"刑" to "criminal punishment"', '"副" to "vice-; secondary"'),
        ('"前" to "front, before"', '"部" to "section; department"'),
        ('"判" to "judge; seal"', '"倍" to "multiple; double"'),
        ('(kind == ReadingKind.On && key == "さく") || (kind == ReadingKind.Kun && key == "けずる")',
         'kind == ReadingKind.On && key == "ぼう"'),
        ('put("mappedReciprocalPairs", 3)', 'put("mappedReciprocalPairs", 2)'),
        ('put("directedLinkTransitions", 6)', 'put("directedLinkTransitions", 4)'),
        ('put("activatedBaselinePairs", 2)', 'put("activatedBaselinePairs", 0)'),
        ('put("completeArticleProjections", 4)', 'put("completeArticleProjections", 3)'),
        ('put("changedReusedArticles", 3)', 'put("changedReusedArticles", 1)'),
        ("assertEquals(9, strokes.length())", "assertEquals(10, strokes.length())"),
        ('hasContentDescription("9 strokes drawn"', 'hasContentDescription("10 strokes drawn"'),
        ("kotlin.random.Random(681)", "kotlin.random.Random(693)"),
        ('put("onlySakuAndKezuruBothKindsPersistedGoodAndDone", true)', 'put("onlyOnBouNoKunPersistedGoodAndDone", true)'),
        ('"刑"', '"剖"'), ('"けい"', '"ぼう"'),
    ]:
        assert old in text, old
        text = text.replace(old, new)
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; only 剖 meaning and onぼう due; no kun keys. Full raw readings and explicit curation retained. Two historical good 剖 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    begin = text.index("        assertEquals(listOf(",
                       text.index('        val curatedIds ='))
    end = text.index("        val checkedPools =", begin)
    text = text[:begin] + '''        assertEquals(emptyList<String>(), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(dissection) +
            n1.filter { it.kanji != "剖" }.shuffled(kotlin.random.Random(693)).take(15)
''' + text[end:]
    text = text.replace('if (poolName == "N1" || poolName == "randomN1Subset") 1 else 3',
                        'if (poolName == "N1" || poolName == "randomN1Subset") 0 else 3')
    begin = text.index('            assertEquals("criminal punishment", meaning.options')
    end = text.index('            for (option in meaning.options)', begin)
    text = text[:begin] + '''            assertFalse(meaning.options.any { it.kanji in setOf("部", "倍", "副") })
            assertEquals("dissect; split open", meaning.options.single { it.kanji == "剖" }.title)
            assertEquals(listOf("部", "倍", "副"), meaning.card.distractors.splitSep())
''' + text[end:]
    text = text.replace('put("actualN1CuratedAvailable", 1).put("actualN1FallbackOptions", 2)',
                        'put("actualN1CuratedAvailable", 0).put("actualN1FallbackOptions", 3)')
    glyphs = audit["actualHan"]
    assert len(glyphs) == 32
    pages = [" ".join(glyphs[i:i + 12]) for i in range(0, len(glyphs), 12)]
    pages.append("剖 部 倍 副 立 口 刀 刂 亻 阝 解 解剖 解剖学")
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", 'for (word in listOf("解剖", "解剖学"))', text, count=1)
    text = text.replace("all 41 scoped Han; focused 削/消/肖/刀/刂/斫/氵/阜/阝/前/判/刑",
                        "all 32 scoped Han; focused 剖/部/倍/副/立/口/刀/刂/亻/阝/解")
    text = text.replace("41 actual scoped Han; 刂/斫/氵/阝 absent from all three bundled cmaps",
                        "32 actual scoped Han; 亻/刂/阝 absent from all three bundled cmaps")
    text = text.replace("five bounded Compose panels and twelve whole-word rasters",
                        "four bounded Compose panels and eight whole-word rasters")
    text = text.replace("assertEquals(176, rows.length())", "assertEquals(136, rows.length())")
    text = text.replace('put("individualGlyphProbes", 164).put("wholeWordRasterProbes", 12).put("panels", 5)',
                        'put("individualGlyphProbes", 128).put("wholeWordRasterProbes", 8).put("panels", 4)')
    text = text.replace("N1_BATCH_095_ARTICLE_PROJECTION", "\n".join(lines))
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ["093", "094", "importedShave", "importedDeletion", "けい", "ケイ", "さく", "けずる", "削", "criminal punishment"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    import yaml
    for name in ["部", "倍", "副"]:
        card = yaml.safe_load((R / "kanji" / (name + ".md")).read_text(encoding="utf-8").split("---", 2)[1])
        assert f'"{name}" to {quote(card["title"])}' in text
        assert card["jlpt"] != 1
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["亻", "刂", "阝"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1118, "words": 5071, "n1": 127}, counts
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-095/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-095/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-095/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-095/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8441 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-094.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 693, "batch": "095", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "androidSnapshot": APP, "productionBaseline": PROD, "contentVersion": VERSION, "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "oneReadingPriorHarness": READING_PRIOR.relative_to(R).as_posix(), "oneReadingPriorHarnessSha256": sha(READING_PRIOR),
        "durableUtilityRecipe": str(UTILITY), "durableUtilityRecipeSha256": sha(UTILITY),
        "fixtureDiff": str(diff), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R.joinpath(*n.split("/"))), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 3, "changedReusedScope": ["kanji/解.md:39"],
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4, "activatedBaselinePairs": 0,
        "plannedGlyphs": glyphs, "plannedWholeWords": ["解剖", "解剖学"], "plannedComposePanels": pages,
        "plannedNativePaintProbes": 128, "plannedWholeWordRasterProbes": 8, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ボウ"], "kun": []}, "curatedReadings": {"on": ["ボウ"], "kun": []},
        "normalizedQuizKeys": {"on": ["ぼう"], "kun": []}, "newDirectWordExclusionPairs": 3,
        "directGuardPlannedBuilderChecks": 384, "directGuardScopes": ["All", "boundedCustom"],
        "directGuardDirections": ["JpToEn", "EnToJp"], "directGuardBothTargetOrientations": True,
        "kanjiChoicePlannedChecks": 64, "kanjiChoicePools": ["N1", "All", "boundedCustom", "randomN1Subset"],
        "n1CuratedAvailable": [], "n1MissingCurated": ["部", "倍", "副"], "n1FallbackCount": 3,
        "allCuratedAvailable": ["部", "倍", "副"], "allFallbackCount": 0,
        "fallbackSemanticAcceptance": "OPEN pending actual imported/UI options and evidence-based original-session confirmations",
        "pendingCmapAbsences": ["亻", "刂", "阝"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. All has three curated wrong cards; exact N1 has none since部N3/倍N2/副N2 are excluded, so three production fallbacks are captured, NOT assumed wrong or accepted. Three direct word guards tested through actual builder on imported words, not learner word-session UI. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. Original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen095 fixture and full archive; all8441 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-095-native-test.apk"
    app = C / "artifacts" / "n1-batch-095-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch095GlyphTest", "N1Batch095ArticleTest",
                     "fullSingleImportOfflineDissectionOneNewSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-693-native-compile.ps1", C / "preflight-693.ps1", VERIFICATION, UTILITY,
               L / "preflight-693.json", C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt",
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
        "schemaVersion": 1, "execution": 693, "batch": "095", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution693StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8441, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 121, "remainingAdditions": 1107, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; retained as evidence, not source whitespace changes.",
        "diagnostics": [
            "Exact N1 has zero curated wrong cards:部N3/倍N2/副N2 are outside N1. Planned assertions capture three production fallbacks; actual semantic acceptance remains open.",
            "Only committed093/094 harnesses and approved control085 Markdown utilities used; no historical session-state helper access.",
            "Initial console inspection needed explicit UTF-8 after a cp1252 print failure; entire request had already loaded/decoded. No permission denial or checkpoint loss.",
            "First in-memory preparation stopped on an unnecessary stale-token replacement assertion before writing fixture/archive; removed that no-op requirement and reran preparation successfully.",
            "Native execution and fresh device/port ownership checks deliberately deferred to next bounded checkpoint; no emulator launched."
        ],
    }
    save(R / "docs" / "n1-sources" / "execution-693.json", evidence)
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-095-native/", "docs/n1-sources/execution-693.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-095-native-693-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-095-native-693-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-693.json")
    for item in evidence["provenance"]:
        assert sha(R.joinpath(*item["archive"].split("/"))) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 692 and state["stage"] == "batch-095-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 693, "checkpoint": 693, "batch": "095",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-693.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8441,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 121, "remainingAdditions": 1107, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=693, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution693CoordinatorCheckpoint"] = checkpoint
    state["batch095NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    reread = load(C / "progress.json")
    assert all(reread[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-693-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 693, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
