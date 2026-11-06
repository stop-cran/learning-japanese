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
LOG = C / "logs" / "95c5e51d-d0cc-4f42-9024-d155d9489619"
HEAD = "53b6819b22787a2517cd0ad14aa855d357cbc70a"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
TEACHING = "030b144a6aeefc6fe77f76683219832db91bef4f"
VERSION = "74b87b47347b78c1"
FOLDER = R / "docs" / "n1-reviews" / "batch-084-native-retry1"
FIXTURE = FOLDER / "N1Batch084Retry1NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-083-native-corrected" / "N1Batch083CorrectedNativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-084-53b6819b-envelope.zip"
VERIFICATION = C / "batch-084-native-retry1-fixture-verification.json"
BEFORE = LOG / "progress-before-586.json"
EVIDENCE = R / "docs" / "n1-sources" / "execution-586.json"
NEXT = (
    "SAME084 native execution and direct PNG inspection on the newly compiled frozen "
    "batch084 fixture next, then persist/yield before dependent two-family visual "
    "confirmation, latest-main integration/publication or085. Read execution-586.json "
    "and batch-084-native-retry1-fixture-verification.json. Verify signed content53b6819b "
    "archive/version74b87b47347b78c1/8379runtimehashes, frozen084app/testAPK and fixture "
    "hashes; qualified TESTONLY Android1c1b7bf4 atop unchanged productionf9. "
    "Fresh HOST4 zero-skips passed585; native fixture compiled586, neither is native "
    "acceptance. Require terminalcase0 BOTH N1Batch084Retry1GlyphTest and N1Batch084Retry1ArticleTest, "
    "no skips/errors. Full git envelope via production ContentSync ONCE, actual "
    "1096kanji/5053words/116N1, zeroProblems/version/Roomepoch1; full source "
    "onリン/kunきびし.い preserved, curated onリン/kun[], soleりん offered/persisted "
    "and done. Exact default N1 and All meaning options凜/准/冗/凹 with actual titles. "
    "All28 actualHan/fourfamilies/112individual+8wholewordrasters/3Composepanels, "
    "especially凜/凛/冫/稟, require PNG legibility/lookalike inspection; missingcmap "
    "and hashes do not establish readability/fallbackface. Complete凜kanji/word "
    "article projections, one reciprocalpair/twodirections, SystemBack/offline/"
    "N1selection/meaning/soleon/15stroke trace/recall/persistence. Injected tracing/"
    "giveup NOT humanhandwriting/MLKit/phone. Fresh device/PID/local+remote5580/5581 "
    "includingTimeWait ownership immediately before approved ownedreadonly API35 "
    "N3_Acceptance_20261029 emulator-5580 launch; hostGPU/-Vulkan/2048MiB/2cores, "
    "explicit serial, stop only owned helper. No shareddevice interference, "
    "alternateport without routing authorization, app/guestheap or guard increases. "
    "Parent19008 owns runner.lock; verify live ancestry/session/checkpoint/signedheads/"
    "cleanworktrees, no child lock acquisition/delete/unlock. Approvedcontrol/committed "
    "sources only; preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Textual030b144a closed; C1optional/C2withdrawn/C3defaultresolved-largerpoolunverified "
    "and all original evidence/limits retained. Original serial two-family dependent "
    "visual confirmation remains required. Later fresh latest-main normalmerge/"
    "surgicalreconciliation/substantiveteachingreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalCI/EVERYimmutablepublicZIPhash/original18000entries/"
    "42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepathguards/"
    "verifiedownerissue60 remain. Published110/1228,1118remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding, projectincomplete. No085."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def update(data):
    temp = C / "progress.586.tmp"
    assert not temp.exists()
    save(temp, data)
    assert load(temp) == data
    temp.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == VERSION
    count = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert count == 8379
    return manifest


def start():
    data = load(C / "progress.json")
    assert data["checkpoint"] == 585 and data["status"] == "continue" and data["batch"] == "084"
    assert data["stage"] == "fresh-android-passed-awaiting-native"
    clean(R, HEAD)
    clean(A, APP)
    runtime()
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)
    request = (LOG / "request.txt").read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    checkpoint = json.loads(request.split(marker, 1)[1])
    assert checkpoint["checkpoint"] == 585 and checkpoint["batch"] == "084"
    traversed = 0
    stack = [checkpoint]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
        elif isinstance(value, str):
            traversed += 1
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    state = {
        "execution": 586, "batch": "084", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME084 full archive/native fixture preparation and compilation, normally signed LOCAL checkpoint; no native execution, reviewer, latest-main integration, publication or085.",
        "request": {"sha256": sha(LOG / "request.txt"), "bytes": (LOG / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True, "checkpointStringsTraversed": traversed,
                    "limits": "Entire request read and checkpoint traversed. Operative contract, complete issue and final585 inspected directly; historical middle not freshly semantically re-reviewed."},
        "runnerLockRole": "Live runner19008 verified in coordinator ancestry; child never acquires/deletes/unlocks parent lock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    data["execution586StartingState"] = state
    data["stage"] = "batch-084-native-preparation-in-progress"
    data["nextAction"] = state["scope"]
    update(data)
    save(C / "execution-586-start.json", state)
    print("Starting scope persisted; full live history preserved.")


def prepare():
    from fontTools.ttLib import TTFont
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", "HEAD")
    assert set(git("ls-files", "--others", "--exclude-standard").splitlines()) == {
        "docs/n1-reviews/batch-084-native/N1Batch084NativeTest.kt",
        "docs/n1-reviews/batch-084-native/fixture-from-corrected-083.diff",
    }
    clean(A, APP)
    assert not FOLDER.exists() and not VERIFICATION.exists()
    original = load(C / "batch-084-native-fixture-verification.json")
    assert sha(Path(original["fixture"])) == original["fixtureSha256"]
    assert sha(ARCHIVE) == original["archiveSha256"]
    manifest = runtime()
    assert not git("diff", TEACHING, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-084-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    assert reconciliation["actionableRemainingTeachingFindings"] == 0
    audit = load(R / "docs" / "n1-sources" / "batch-084-draft-font-audit.json")
    names = audit["completeNewArticleScope"]
    assert names == ["kanji/凜.md", "words/凜.md"] and not audit["changedReusedScope"]
    assert all(sha(R / name) == expected for name, expected in audit["articleHashes"].items())
    spec = importlib.util.spec_from_file_location("approved_573_projection", C / "execution-573.py")
    projection = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(projection)
    original_plain = projection.plain

    def plain(value):
        value = original_plain(value)
        return re.sub(r"\*([^\s*](?:[^*]*[^\s*])?)\*", r"\1", value)

    projection.plain = plain
    documents = {name: projection.blocks(R / name) for name in names}
    quote = projection.quote
    assert plain("*taru adjective*") == "taru adjective"
    assert plain("**bold**") == "bold" and plain("x * y") == "x * y"
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def show(document, kind, value, step):
        qualifier = "readingExample" if kind == "table" else "articleBullet"
        assert sum(v == value for k, v in documents[document]
                   if (k == "table") == (kind == "table") and k != "heading") == 1
        line(f"show({qualifier}({quote(value)}), {quote(step)})")
        selectors.append({"document": document, "kind": kind, "target": value, "step": step})

    def display(document, slug):
        line(f"await({quote(documents[document][0][1])})")
        cell = 0
        for index, (kind, value) in enumerate(documents[document][1:], 1):
            if kind == "heading":
                line(f"section({quote(value)})")
            elif kind == "table":
                cell += 1
                if cell > 3 and cell % 3 != 2:
                    show(document, kind, value, f"{slug}-{index:02}")
            else:
                show(document, kind, value, f"{slug}-{index:02}")

    def follow(document, destination, preferred, step):
        body = (R / document).read_text(encoding="utf-8").split("---", 2)[2]
        sections = re.split(r"^## (.+)\n", body, flags=re.M)
        candidates = []
        for i in range(1, len(sections), 2):
            for part in re.split(r"\n\s*\n|\n(?=- )", sections[i + 1].strip()):
                for link in re.finditer(r"\[凜\]\(([^)]+)\)", part):
                    if (R / document).parent.joinpath(link[1]).resolve() == (R / destination).resolve():
                        candidates.append((sections[i], part.removeprefix("- ")))
        section_name, raw = next(v for v in candidates if v[0] == preferred)
        link = re.search(r"\[凜\]\(([^)]+)\)", raw)
        rendered = plain(" ".join(part.strip() for part in raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_586" + raw[link.end():]
        offset = plain(" ".join(part.strip() for part in marked.splitlines())).index("N1_LINK_TARGET_586")
        assert rendered[offset:].startswith("凜")
        line(f"section({quote(section_name)})")
        show(document, "paragraph", rendered, step)
        line(f"inline(await(articleBullet({quote(rendered)})), \"凜\", {offset})")
        line('await("Article contents")')
        item = {"document": document, "destination": destination, "label": "凜",
                "section": section_name, "renderedText": rendered, "offset": offset}
        offsets.append(item)
        return item

    def back_to(item, step):
        line("back()")
        line(f"await(articleBullet({quote(item['renderedText'])})).assertIsDisplayed()")
        line(f"section({quote(item['section'])})")
        line(f"capture({quote(step)})")

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("凜")')
    line('click("dignified; bracing cold")')
    display("kanji/凜.md", "kanji")
    forward = follow("kanji/凜.md", "words/凜.md", "Common words", "word-forward")
    display("words/凜.md", "word")
    reverse = follow("words/凜.md", "kanji/凜.md", "How the kanji combine", "word-reverse")
    line('section("Readings")')
    line('show(readingExample("リン"), "word-kanji-backlink")')
    back_to(reverse, "word-system-back-to-word")
    back_to(forward, "word-system-back-to-kanji")
    assert len(offsets) == 2
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "            N1_ARTICLE_ROUTE_586\n" + text[end:]
    replacements = [
        ("N1Batch083Corrected", "N1Batch084Retry1"), ("disposable083Corrected", "disposable084"),
        ("n1-083-corrected", "n1-084"), ("Batch 083", "Batch 084"),
        ("enduranceLookalikes", "dignifiedLookalikes"),
        ("fullSingleImportOfflineEnduranceTwoReciprocalPairsCuratedOnAndKunDrawingAndSystemBack",
         "fullSingleImportOfflineDignifiedReciprocalPairSoleOnDrawingAndSystemBack"),
        ("n1-batch-083-corrected-867fe8be-envelope.zip", ARCHIVE.name),
        ("867fe8bef228145ef0a6e48690941b0a0aa50336", HEAD),
        ("6dfe6a1e287ce5df", VERSION), ("1095, updated.kanji", "1096, updated.kanji"),
        ("5052, updated.words", "5053, updated.words"), ("115, n1.size", "116, n1.size"),
        ("N1 · 115 cards", "N1 · 116 cards"), ('"凌"', '"凜"'),
        ("endure; surpass", "dignified; bracing cold"), ("endurance", "dignified"),
        ('listOf("准", "冶", "冴")', 'listOf("准", "冗", "凹")'),
        ('"冶" to "smelt; work metals"', '"冗" to "superfluous; redundant"'),
        ('"冴" to "clear; sharp-minded"', '"凹" to "concave; sunken"'),
        ('listOf("リョウ")', 'listOf("リン")'), ('"りょう"', '"りん"'),
        ('listOf("しの.ぐ")', 'listOf("きびし.い")'),
        ("repeat(2)", "repeat(1)"),
        ("assertEquals(2, done.answered)", "assertEquals(1, done.answered)"),
        ("assertEquals(2, done.correct)", "assertEquals(1, done.correct)"),
        ("assertEquals(2, readingLogs.size)", "assertEquals(1, readingLogs.size)"),
        ('setOf("りん", "しのぐ"), readingLogs', 'setOf("りん"), readingLogs'),
        ("assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)",
         "assertEquals(setOf(ReadingKind.On), answeredKinds)"),
        ('capture("curated-on-kun-done")', 'capture("curated-on-done")'),
        ('put("bothCuratedKindsPersistedGoodAndDone", true)', 'put("soleCuratedOnPersistedGoodAndDone", true)'),
        ('put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)',
         'put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2)'),
        ('put("completeArticleProjections", 3)', 'put("completeArticleProjections", 2)'),
        ("assertEquals(10, strokes.length())", "assertEquals(15, strokes.length())"),
        ('hasContentDescription("10 strokes drawn"', 'hasContentDescription("15 strokes drawn"'),
        ("kotlin.random.Random(577)", "kotlin.random.Random(586)"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    for target in ("dignified", "card"):
        text = text.replace(f'assertEquals(listOf("きびし.い"), {target}.quizKunyomi?.splitSep())',
                            f"assertEquals(emptyList<String>(), {target}.quizKunyomi?.splitSep())")
    text = text.replace('assertEquals(listOf("しのぐ"), dignified.toReadingCard().quizKeys(ReadingKind.Kun))',
                        'assertEquals(emptyList<String>(), dignified.toReadingCard().quizKeys(ReadingKind.Kun))')
    text = text.replace('card.kanji == "凜" && key == (if (kind == ReadingKind.On) "りん" else "しのぐ")',
                        'card.kanji == "凜" && kind == ReadingKind.On && key == "りん"')
    text = text.replace('val key = if (question.question.kind == ReadingKind.On) "りん" else "しのぐ"',
                        'assertEquals(ReadingKind.On, question.question.kind)\n                val key = "りん"')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 凜 meaning and sole curated onりん due, kun[] source-onlyきびし.い not queued. Two historical good 凜 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    text = text.replace("            N1_ARTICLE_ROUTE_586", "\n".join(lines))
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "".join(
        (R / name).read_text(encoding="utf-8") for name in names))))
    assert glyphs == audit["actualHan"] and len(glyphs) == 28
    fonts = []
    for item in audit["fonts"]:
        path = Path(item["path"])
        assert sha(path) == item["sha256"]
        with TTFont(path) as font:
            missing = [char for char in glyphs if ord(char) not in font.getBestCmap()]
        assert missing == item["allActualMissing"] == ["冫", "凛", "凜", "稟"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    words = ["凜とした", "凛とした"]
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("凜 凛 冫 稟 禾 示 准 冗 凹 凜とした 凛とした")
    text = re.sub(r"val pages = listOf\([^\n]+\)",
                  "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)",
                  "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)",
                  "for (word in listOf(" + ", ".join(map(quote, words)) + "))", text, count=1)
    text = text.replace("endurance / look-alikes / radical fallback", "dignified bearing / variant / radical fallback")
    text = text.replace("all 30 scoped Han; focused 凌/陵/准/冶/冴/次, 冫/夌/阝/隹",
                        "all 28 scoped Han; focused 凜/凛/冫/稟 and 禾/示, 准/冗/凹")
    text = text.replace("assertEquals(128, rows.length())", "assertEquals(120, rows.length())")
    text = text.replace('put("individualGlyphProbes", 120).put("wholeWordRasterProbes", 8)',
                        'put("individualGlyphProbes", 112).put("wholeWordRasterProbes", 8)')
    # Both variant expressions are rendered in each of four production families.
    text = text.replace("30 actual scoped Han including exact 冫/夌/阝/隹 fallback inspection",
                        "28 actual scoped Han including exact 凜/凛/冫/稟 fallback inspection")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("083", "凌", "しの", "リョウ", "りょう", "endurance", "夌", "阝", "隹"):
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    assert 'assertEquals(emptyList<String>(), dignified.quizKunyomi?.splitSep())' in text
    assert 'assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())' in text
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1096, "words": 5053, "n1": 116}
    expected_titles = {"凜": "dignified; bracing cold", "准": "quasi-; associate rank",
                       "冗": "superfluous; redundant", "凹": "concave; sunken"}
    for char, title in expected_titles.items():
        assert re.search(r"^title: " + re.escape(title) + r"$", (R / "kanji" / f"{char}.md").read_text(encoding="utf-8"), re.M)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        prefix = "n1-batch-084/"
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith(prefix) and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read(prefix + "manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=R)
        assert json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, mapping in manifest.items():
            if not isinstance(mapping, dict):
                continue
            for name, expected in mapping.items():
                data = archive.read(prefix + name)
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in archive.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    assert verified == 8379
    FOLDER.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-corrected-083.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.relative_to(R).as_posix(), n=2)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 586, "batch": "084", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": TEACHING, "androidSnapshot": APP,
        "productionBaseline": PROD, "contentVersion": VERSION, "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "fixtureDiff": diff.relative_to(R).as_posix(), "fixtureDiffSha256": sha(diff),
        "projectionHelper": str(C / "execution-573.py"), "projectionHelperSha256": sha(C / "execution-573.py"),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(documents[n])} for n in names],
        "completeArticleProjections": 2, "changedReusedPassages": 0,
        "mappedReciprocalPairs": 1, "mappedDirectedTransitions": 2,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "plannedNativePaintProbes": 112, "plannedWholeWordRasterProbes": 8, "currentFontAudit": fonts,
        "fullReadings": {"on": ["リン"], "kun": ["きびし.い"]},
        "curatedReadings": {"on": ["リン"], "kun": []},
        "normalizedQuizKeys": {"on": ["りん"], "kun": []},
        "pendingCmapAbsences": ["冫", "凛", "凜", "稟"],
        "exactMeaningOptions": expected_titles, "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "originalAttempt": original,
        "retryReason": "Post-compile source inspection found the old projection helper retained single emphasis delimiters around taru adjective, unlike production Markdown.parseInline. No native case ran. Preserve original fixture, compile log and APK; correct only generated static selector rendering and use separately named Retry1 classes/APK/log.",
        "limits": "Preparation only. Static Markdown selectors/offsets/cmaps/bytes do not establish native visibility, legibility or fallback face. Full archive through production ContentSync ONCE. Reference tracing/giveup are not human handwriting/MLKit/phone. All source/reviewer/process/denial/OOM/phone limits and original production heaps/guards preserved."
    }
    save(VERIFICATION, record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes",
                                             "compressedBytes", "inflatedBytes", "retainedBytes")}))


def record():
    clean(A, APP)
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runtime()
    fixture = load(VERIFICATION)
    assert sha(FIXTURE) == fixture["fixtureSha256"] and sha(ARCHIVE) == fixture["archiveSha256"]
    original_fixture = Path(fixture["originalAttempt"]["fixture"])
    original_text = original_fixture.read_text(encoding="utf-8")
    retry_text = FIXTURE.read_text(encoding="utf-8")
    assert original_text.replace("N1Batch084", "N1Batch084Retry1").replace(
        "*taru adjective*", "taru adjective") == retry_text
    assert "*taru adjective*" not in retry_text
    assert retry_text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in retry_text
    assert (LOG / "native-retry1-compile-exit.txt").read_text().strip() == "0"
    command = load(LOG / "native-retry1-compile-command.json")
    assert not command["hostOnlyHeapInitUsed"] and not command["parentLockAccessAttempted"]
    assert command["arguments"] == [":app:assembleDebugAndroidTest", "--no-daemon", "--no-parallel", "--max-workers=1",
                                     "-Pkotlin.compiler.execution.strategy=in-process"]
    result = next(v for v in (LOG / "native-retry1-compile.txt").read_text().splitlines() if v.startswith("BUILD SUCCESSFUL"))
    apk = C / "artifacts" / "n1-batch-084-native-retry1-test.apk"
    app = C / "artifacts" / "n1-batch-084-native-retry1-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch084Retry1GlyphTest", "N1Batch084Retry1ArticleTest", "dignifiedLookalikesAndRadicalFallbacksAcrossFourProductionFamilies",
                     "fullSingleImportOfflineDignifiedReciprocalPairSoleOnDrawingAndSystemBack"):
            assert name.encode() in dex, name
    receipts = FOLDER / "preparation-receipts"
    assert not receipts.exists()
    receipts.mkdir()
    provenance = []
    for source in [Path(__file__), C / "execution-573.py", C / "run-586-native-compile.ps1",
                   C / "run-586-native-compile-original.ps1",
                   C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt", VERIFICATION,
                   C / "batch-084-native-fixture-verification.json",
                   *[LOG / n for n in ("native-compile-command.json", "native-compile-start.txt",
                                       "native-compile-end.txt", "native-compile-exit.txt",
                                       "native-retry1-compile-command.json", "native-retry1-compile-start.txt",
                                       "native-retry1-compile-end.txt", "native-retry1-compile-exit.txt")]]:
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    for name in ("native-compile.txt", "native-retry1-compile.txt"):
        raw_log = LOG / name
        zipped_log = receipts / (name + ".gz")
        with zipped_log.open("wb") as output:
            with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as zipped:
                zipped.write(raw_log.read_bytes())
        assert gzip.decompress(zipped_log.read_bytes()) == raw_log.read_bytes()
        provenance.append({"source": str(raw_log), "sourceSha256": sha(raw_log),
                           "archive": zipped_log.relative_to(R).as_posix(), "sha256": sha(zipped_log), "losslessGzipVerified": True})
    save(EVIDENCE, {
        "schemaVersion": 1, "execution": 586, "batch": "084", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "teachingSnapshot": TEACHING, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "execution-586-start.json"), "fixtureVerification": fixture,
        "buildResult": result, "compileExitCode": 0, "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "provenance": provenance, "runtimeManifestHashesVerified": 8379,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "hostChecksRerun": False, "nativeOrVisualExecuted": False,
        "diagnostics": [
            "Initial static title audit caught assumed concave label; actual concave; sunken retained before writing original fixture/archive.",
            fixture["retryReason"],
        ],
        "originalCompileLog": {"path": str(LOG / "native-compile.txt"), "sha256": sha(LOG / "native-compile.txt")},
        "originalTestApk": {"path": str(C / "artifacts" / "n1-batch-084-native-test.apk"),
                            "sha256": sha(C / "artifacts" / "n1-batch-084-native-test.apk")},
        "retryDiffVerified": "Original fixture preserved; Retry1 differs only in independently named classes and one rendered emphasis selector. Both compilations succeeded; neither executed natively.",
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "nextGate": NEXT, "inheritedNextGate": load(R / "docs" / "n1-sources" / "execution-585.json")["nextAction"],
        "limits": fixture["limits"],
    })
    print(result)
    print("Frozen APK assets/DEX and unchanged production APK verified; no native execution.")


def finish():
    clean(A, APP)
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("merge-base", HEAD, "HEAD") == HEAD
    runtime()
    issue = load(C / "batch-084-native-preparation-586-issue-verified.json")
    payload = load(C / "batch-084-native-preparation-586-issue-payload.json")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == payload["body"]
    data, before = load(C / "progress.json"), load(BEFORE)
    assert data["checkpoint"] == 585 and data["batch"] == "084"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert data[key] == value, key
    summary = {
        "schemaVersion": 1, "execution": 586, "checkpoint": 586, "batch": "084",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": "native-prepared-compiled-awaiting-execution", "evidence": EVIDENCE.relative_to(R).as_posix(),
        "contentSnapshot": HEAD, "androidHead": APP, "runtimeManifestHashesVerified": 8379,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "nativeOrVisualExecuted": False, "hostChecksRerun": False,
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "dedicatedWorktreesClean": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(C / "batch-084-native-preparation-586-issue-verified.json"),
    }
    for key in ("checkpoint", "status", "stage", "nextAction"):
        data[key] = summary[key]
    data["blocker"] = None
    data["execution586CoordinatorCheckpoint"] = summary
    data["batch084NativePreparationCheckpoint"] = summary
    data["batch084NativePreparationIssueReceipt"] = {
        "url": issue["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": issue["id"], "receiptSha256": summary["issueReceiptSha256"],
        "localSignedEvidenceCommit": summary["savedCommit"], "runtimePublished": False,
    }
    update(data)
    save(LOG / "batch-084-native-preparation-checkpoint.json", summary)
    print("Checkpoint586 persisted; full original history preserved, both worktrees clean.")


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
