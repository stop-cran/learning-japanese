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
L = C / "logs" / "e18b3bce-9dbb-464d-8dbc-bc6c53b6bec5"
HEAD = "17a4bbb997c1940dc802cf4e97599c560009e4a7"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "70dfe3344d167e5152a3685b09689d73fa1cdab1"
VERSION = "5408632b5aa1382c"
WORK = C / "batch-099-native-732"
FIXTURE = WORK / "N1Batch099NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-098-native" / "N1Batch098NativeTest.kt"
UTILITY = C / "prepare-batch-085-native.py"
ARCHIVE = C / "artifacts" / "n1-batch-099-17a4bbb9-envelope.zip"
VERIFICATION = C / "batch-099-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-099-native"
BEFORE = L / "progress-before-732.json"
STAGE = "batch-099-native-prepared-compiled-not-executed"
NEXT = (
    "SAME099 execute frozen compiled native fixture and inspect actual PNGs next; preparation732 is NOT native acceptance. "
    "Read docs/n1-sources/execution-732.json and control/batch-099-native-fixture-verification.json. "
    "Require BOTH N1Batch099GlyphTest and N1Batch099ArticleTest terminal per-case0/no skips. "
    "Exact full archive17a4bbb9/version5408632b5aa1382c/8451runtimehashes through productionContentSync ONCE: "
    "1122kanji/5073words/131N1/zeroProblems/acceptedRoomversion+readingepoch1. "
    "All12Han across FOUR production font families/systemfallback, especially刂/older剩: "
    "48individual+8wholewordPaint probes/TWO bounded Compose panels; actual legibility/lookalike inspection required, "
    "cmap/hasGlyph/rasterhashes NOT legibility/fallbackface evidence. "
    "All productionchoices exactly remainder;surplusamount vs乗/剣/則; actualN1 includes剣 but NOT乗N3/則N2, "
    "so TWO productionfallbacks require actual semantic inspection. Inspect N1UI and16-seed N1/All/boundedcustom/randomN1subset "
    "builder records; fallbacksemanticacceptance OPEN, wider custom/random pools not certified by textualreview. "
    "Existing過剰 SEVEN directguards preserved (NO newguard):896planned importedbuilderchecks across All/custom/"
    "bothdirections/bothtargetorientations/16seeds; unchanged過剰かじょう N2metadata. "
    "Full/Lite rawジョウ andあまつさえ/あま.り/あま.る retained; explicit quizジョウ/[] only, "
    "じょう offered/persistedGood/Done and NO kun/sourceonly questions. ELEVEN pinned strokes injectedtrace/recall/persistence; "
    "ONE complete articleprojection剰 plus exact reused過剰component/過commonword changes, "
    "TWO allmapped reciprocalpairs/FOUR directions/ONEactivatedbaselinepair; SystemBack/offline/N1selection/meaning/readings/drawing. "
    "Injectedtrace/giveup NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581ownership immediately before "
    "ownedreadonly API35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/2048MiB/2cores; stop only ownedhelper. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Fresh731 JVM4/no skips retained. "
    "OriginalClaude2ac79fdb-83fc-485d-8f64-6c5d7b473973 THEN GPT240faa46-7797-4c93-998e-af5db5677c98 "
    "need serial bounded rendered confirmations; no newblindcredit. Parent15692 retains runner.lock; verifyliveancestry/session/"
    "checkpoint/exactsignedheads/whollyclean, NOchildreacquisition/delete/unlock/readprobe. "
    "Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. All currentmainnonrewritingmerge/"
    "surgicalreconciliation/changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIPentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue gates remain. Published125/1228,1103remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No100/runtimepublication/secondrunner."
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
    original = load(BEFORE)
    for key, value in original.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert state[key] == value, key
    temp = C / "progress.732.tmp"
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
    assert count == 8451
    review = load(R / "docs" / "n1-reviews" / "batch-099-reconciliation.json")
    assert review["textualReviewClosed"] and review["reviewedTeachingSnapshot"] == TEACHING
    for name, digest in review["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        731, "continue", "batch-099-fresh-android-passed-awaiting-native", "099"
    )
    role, runner = load(L / "preflight-732.json"), load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (15692, "running", L.name)
    assert role["decodedLauncherMatches"] and role["liveParentPid"] == 15692 and not role["lockTouched"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["checkpoint"] == 731 and checkpoint["execution731CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution732StartingState"] = {
        "execution": 732, "batch": "099", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME099 full native fixture/archive preparation and compilation, normally signed LOCAL evidence; yield before native execution/visual review/publication/100.",
        "request": {
            "sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
            "characters": len(request), "lines": len(request.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final731 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-099-native-preparation-in-progress"
    state["nextAction"] = state["execution732StartingState"]["scope"]
    persist(state)
    print("Starting732 persisted; complete live history retained.")


def prepare():
    import yaml
    from fontTools.ttLib import TTFont

    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", UTILITY)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    audit = load(R / "docs" / "n1-sources" / "batch-099-draft-font-audit.json")
    names = audit["completeArticleScope"]
    assert names == ["kanji/剰.md"]
    projected = names + ["words/過剰.md", "kanji/過.md"]
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_732" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_732")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("剰")')
    line('click("remainder; surplus amount")')
    display("kanji/剰.md", "kanji")
    to_word = follow("kanji/剰.md", "過剰", "words/過剰.md", "Common words", "kajo-forward")
    line(f"await({quote(docs['words/過剰.md'][0][1])})")
    from_word = follow("words/過剰.md", "剰", "kanji/剰.md", "How the kanji combine", "jo-reverse")
    line('section("Readings")')
    line('show(readingExample("ジョウ"), "jo-kanji-backlink")')
    back_to(from_word, "jo-system-back-to-word")
    to_ka = follow("words/過剰.md", "過", "kanji/過.md", "How the kanji combine", "ka-reverse")
    line(f"await({quote(docs['kanji/過.md'][0][1])})")
    from_ka = follow("kanji/過.md", "過剰", "words/過剰.md", "Common words", "ka-forward")
    line('section("How the kanji combine")')
    line(f"show(articleBullet({quote(to_ka['renderedText'])}), \"kajo-component-return\")")
    back_to(from_ka, "ka-system-back-to-kanji")
    back_to(to_ka, "ka-system-back-to-word")
    back_to(to_word, "kajo-system-back-to-jo")
    plan = load(R / "docs" / "n1-sources" / "batch-099-progress.json")["proposedDirectedLinkPlan"]
    assert len(offsets) == 4
    assert {(x["document"], x["destination"]) for x in offsets} == {(x["from"], x["to"]) for x in plan}
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "N1_BATCH_099_ARTICLE_PROJECTION\n" + text[end:]
    card = yaml.safe_load((R / "kanji" / "剰.md").read_text(encoding="utf-8").split("---", 2)[1])
    word = yaml.safe_load((R / "words" / "過剰.md").read_text(encoding="utf-8").split("---", 2)[1])
    assert word["quiz_exclusions"] == ["余分", "超過", "オーバー", "あまり", "あんまり", "余る", "余裕"]
    assert word["jlpt"] == 2 and card["distractors"] == ["乗", "剣", "則"]

    def replace(old, new):
        nonlocal text
        assert old in text, old
        text = text.replace(old, new)

    for old, new in [
        ("N1Batch098", "N1Batch099"), ("disposable098", "disposable099"), ("n1-098", "n1-099"),
        ("Batch 098", "Batch 099"), ("n1-batch-098-6cca181b-envelope.zip", ARCHIVE.name),
        ("6cca181b977144603296506cfe0b9ed744e2d193", HEAD), ("0cbdc2723b0433f2", VERSION),
        ("1121, updated.kanji", "1122, updated.kanji"), ("130, n1.size", "131, n1.size"),
        ("N1 · 130 cards", "N1 · 131 cards"), ("agentLookalikesAndScopedHan", "surplusLookalikesAndScopedHan"),
        ("fullSingleImportOfflineAgentReusedSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack",
         "fullSingleImportOfflineSurplusReusedSupportTwoReciprocalPairsOneOnNoKunElevenStrokesAndSystemBack"),
        ("agent", "surplus"), ("Agent", "Surplus"),
        ("medicinal preparation; chemical surplus", "remainder; surplus amount"),
        ('"剤"', '"剰"'), ('listOf("済", "剛", "則")', 'listOf("乗", "剣", "則")'),
        ('listOf("ザイ", "スイ", "セイ")', 'listOf("ジョウ")'),
        ('listOf("かる", "けず.る")', 'listOf("あまつさえ", "あま.り", "あま.る")'),
        ('listOf("ザイ")', 'listOf("ジョウ")'), ('listOf("ざい")', 'listOf("じょう")'),
        ('"ざい"', '"じょう"'), ("onざい", "onじょう"),
        ('put("preservedDirectWordGuardPairs", 1)', 'put("preservedDirectWordGuardPairs", 7)'),
        ("assertEquals(128, directGuardChecks.length())", "assertEquals(896, directGuardChecks.length())"),
        ("kotlin.random.Random(722)", "kotlin.random.Random(732)"),
        ("onlyOnZaiNoKunPersistedGoodAndDone", "onlyOnJouNoKunPersistedGoodAndDone"),
        ("assertEquals(10, strokes.length())", "assertEquals(11, strokes.length())"),
        ('"10 strokes drawn"', '"11 strokes drawn"'),
    ]:
        replace(old, new)
    begin = text.index("        val expectedMeanings =")
    end = text.index("        val all =", begin)
    expected, levels = {"剰": card["title"]}, {}
    for name in card["distractors"]:
        entry = yaml.safe_load((R / "kanji" / (name + ".md")).read_text(encoding="utf-8").split("---", 2)[1])
        expected[name], levels[name] = entry["title"], entry["jlpt"]
    assert levels == {"乗": 3, "剣": 1, "則": 2}, levels
    text = text[:begin] + "        val expectedMeanings = mapOf(\n" + "".join(
        f"            {quote(k)} to {quote(v)},\n" for k, v in expected.items()) + "        )\n" + text[end:]
    replace('listOf("剛"), curatedIds.filter', 'listOf("剣"), curatedIds.filter')
    begin = text.index("        val importedSurplus =")
    end = text.index("        for ((leftId, rightId) in guardPairs)", begin)
    text = text[:begin] + (
        '        val importedSurplus = words.single { it.word == "過剰" }\n'
        f'        assertEquals(listOf({", ".join(map(quote, word["quiz_exclusions"]))}), importedSurplus.quizExclusions)\n'
        '        assertEquals("かじょう", importedSurplus.reading)\n'
        '        assertEquals(2, importedSurplus.jlpt)\n'
        '        val directGuardChecks = JSONArray()\n'
        '        val guardPairs = importedSurplus.quizExclusions.map { "過剰" to it }\n'
    ) + text[end:]
    replace("only 剤 meaning", "only 剰 meaning")
    replace("good 剤 meaning", "good 剰 meaning")
    replace('assertFalse(meaning.options.any { it.kanji == "済" })',
            'assertFalse(meaning.options.any { it.kanji == "乗" })')
    replace('assertTrue(meaning.options.any { it.kanji == "剛" })',
            'assertTrue(meaning.options.any { it.kanji == "剣" })')
    glyphs = audit["actualHan"]
    assert len(glyphs) == 12
    pages = [" ".join(glyphs), "剰 剩 乗 余 剣 則 刀 刂 過 過剰 剰え"]
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", 'for (word in listOf("過剰", "剰え"))', text, count=1)
    replace("all 19 scoped Han; focused 剤/済/剛/則/斉/刀/刂/氵/洗", "all 12 scoped Han; focused 剰/剩/乗/余/剣/則/刀/刂/過")
    replace("19 actual scoped Han; 刂/氵 absent from all three bundled cmaps",
            "12 actual scoped Han; 刂/older剩 absent from all three bundled cmaps")
    replace("three bounded Compose panels", "two bounded Compose panels")
    replace("assertEquals(84, rows.length())", "assertEquals(56, rows.length())")
    replace('put("individualGlyphProbes", 76)', 'put("individualGlyphProbes", 48)')
    replace('put("panels", 3)', 'put("panels", 2)')
    text = text.replace("N1_BATCH_099_ARTICLE_PROJECTION", "\n".join(lines))
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1 and "ContentParser.parse" not in text
    for stale in ["098", "ザイ", "ざい", "洗剤", "剤", "剛", "済", "6cca181b", "0cbdc272"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    assert {s["target"] for s in selectors if s["kind"] == "table"} >= {
        "ジョウ", "あまつさえ", "あま.り", "あま.る", "過剰 かじょう — excess; too much"
    }
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["刂", "剩"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
        "words": sum(n.startswith("words/") for n in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (R / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1122, "words": 5073, "n1": 131}, counts
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-099/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-099/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-099/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-099/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8451 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-098.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2
    )), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 732, "batch": "099", "status": "prepared-not-executed",
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
        "plannedGlyphs": glyphs, "plannedWholeWords": ["過剰", "剰え"], "plannedComposePanels": pages,
        "plannedNativePaintProbes": 48, "plannedWholeWordRasterProbes": 8, "currentFontAudit": fonts,
        "fullReadings": {"on": ["ジョウ"], "kun": ["あまつさえ", "あま.り", "あま.る"]},
        "curatedReadings": {"on": ["ジョウ"], "kun": []}, "normalizedQuizKeys": {"on": ["じょう"], "kun": []},
        "newDirectWordExclusionPairs": 0, "preservedDirectWordExclusionPairs": 7,
        "directGuardPairs": [["過剰", x] for x in word["quiz_exclusions"]], "directGuardPlannedBuilderChecks": 896,
        "directGuardScopes": ["All", "boundedCustom"], "directGuardDirections": ["JpToEn", "EnToJp"],
        "directGuardBothTargetOrientations": True,
        "kanjiChoicePlannedChecks": 64, "kanjiChoicePools": ["N1", "All", "boundedCustom", "randomN1Subset"],
        "expectedAllMeaningLabels": expected,
        "n1CuratedAvailable": ["剣"], "n1MissingCurated": ["乗", "則"], "n1FallbackCount": 2,
        "allCuratedAvailable": ["乗", "剣", "則"], "allFallbackCount": 0,
        "fallbackSemanticAcceptance": "OPEN pending actual imported/UI options and evidence-based original-session confirmations",
        "pendingCmapAbsences": ["刂", "剩"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1 has ONE curated wrong card:剣;乗N3/則N2 are excluded so TWO production fallbacks are captured, NOT assumed wrong or accepted. Wider custom/random pools need actual semantic inspection, including surplus-overlap余/過 and sharedジョウ乗 wrong-option protection. Existing seven direct guards through actual builder on imported words, not learner word-session UI; no new word title/guard. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. Reused article scope is exact changed passages and required link destinations, not fresh full teaching review. Original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen099 fixture and full archive; all8451 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and command["launcherCommandMatches"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-099-native-test.apk"
    app = C / "artifacts" / "n1-batch-099-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch099GlyphTest", "N1Batch099ArticleTest",
                     "fullSingleImportOfflineSurplusReusedSupportTwoReciprocalPairsOneOnNoKunElevenStrokesAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [
        Path(__file__), C / "run-732-native-compile.ps1", C / "preflight-732.ps1", VERIFICATION, UTILITY,
        L / "preflight-732.json", C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt",
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
    save(R / "docs" / "n1-sources" / "execution-732.json", {
        "schemaVersion": 1, "execution": 732, "batch": "099", "status": STAGE,
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution732StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8451, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 125, "remainingAdditions": 1103, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; retained as evidence, not source whitespace changes.",
        "limits": [
            "Compiled test fixture and exact full archive only; no emulator launched or native/visual/phone acceptance claimed.",
            "Exact N1 has ONE curated wrong card:剣;乗N3/則N2 are outside N1. Planned assertions capture TWO production fallbacks; semantic acceptance remains open.",
            "Only committed098 harness and approved control085 Markdown utilities used; no historical session-state helper access.",
            "Fresh731 host four cases retained, not rerun or relabelled native. Both original model sessions still require bounded rendered confirmation.",
            "No runtime change, publication, next batch, production app change or lock operation.",
        ],
        "diagnostics": [
            "First in-memory preparation failed exact level assertion: 乗 is preserved N3, not N4. No fixture/archive/runtime edit had been written. Corrected planned level; N1 availability remains 剣 only with TWO fallbacks. Original failed console output retained."
        ],
    })
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-099-native/", "docs/n1-sources/execution-732.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(L / "issue-732-reread.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-099-native-732-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-732.json")
    for item in evidence["provenance"]:
        assert sha(R.joinpath(*item["archive"].split("/"))) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 731 and state["stage"] == "batch-099-native-preparation-in-progress"
    checkpoint = {
        "schemaVersion": 1, "execution": 732, "checkpoint": 732, "batch": "099",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-732.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8451,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 125, "remainingAdditions": 1103, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=732, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution732CoordinatorCheckpoint"] = checkpoint
    state["batch099NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    reread = load(C / "progress.json")
    assert all(reread[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-732-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 732, "savedCommit": saved, "status": "continue",
                      "stage": STAGE, "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
