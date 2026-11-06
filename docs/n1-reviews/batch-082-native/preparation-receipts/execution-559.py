import difflib
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


CONTROL = Path(__file__).resolve().parent
spec = spec_from_file_location("n1_native_preparation_550", CONTROL / "execution-550.py")
prior = module_from_spec(spec)
spec.loader.exec_module(prior)
blocks, plain, quote = prior.blocks, prior.plain, prior.quote
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOGS = CONTROL / "logs" / "342070a3-d57f-4923-a4eb-030ef93ca108"
HEAD = "4f5812bc7f33e7996214661e7dbf5f8e765df849"
REVIEWED = "b6bcc8f144cd781917abdb2ca510f663d1339a56"
ANDROID_HEAD = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-082-native"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-081-native" / "N1Batch081NativeTest.kt"
FIXTURE = FOLDER / "N1Batch082NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-082-4f5812bc-envelope.zip"
VERIFICATION = CONTROL / "batch-082-native-fixture-verification.json"
BEFORE = CONTROL / "execution-559-progress-before.json"
NEXT = (
    "SAME082 native execution and actual PNG inspection next, then persist/yield. "
    "Read docs/n1-sources/execution-559.json and batch-082-native-fixture-verification.json. "
    "Verify frozen4f5812bc full archive, fixture and n1-batch-082-native-test.apk hashes; "
    "no redundant compile/HOST/blind initial review absent new concern. Qualified TEST-ONLY "
    "Android1c1b7bf4/G preserves productionf9b59a2; not latest app main or literal old HEAD. "
    "Fresh device/5580/5581/PID ownership immediately BEFORE approved read-only API35 "
    "N3_Acceptance_20261029 launch; batch0405584 override was batch-specific. "
    "HostGPU/-Vulkan/2048MiB/2core, explicit actual serial/JDK17/SDK, one heavy process, "
    "stop only owned helper. Require terminal status0/no skips for BOTH "
    "N1Batch082GlyphTest and N1Batch082ArticleTest. Full signed Git archive through "
    "production ContentSync ONCE:1094kanji5050words114N1/version0739a82c9699f031/"
    "zeroProblems/acceptedepoch. Full+Lite onジュン and emptykun; quizOnジュン/quizKun[]; "
    "onlyじゅん offered. All31Han/fourproductionfamilies including 冫/氵/辶/隹 fallback, "
    "124individual+4wholewordrasters/threeComposepanels. Complete准/准教授 plus exact "
    "教bullet and 助教授successor-link paragraph; twomappedpairs/fourdirections plus "
    "comparisonpair/twodirections; N1selection/meaning/singlecuratedon/tenstroke trace "
    "then recall/SystemBack/offline. Injected tracing and giveup recall are not handwriting "
    "recognition/MLKit/phone acceptance. Retain all attempts/PNGs/provenance/cleanup. "
    "Later serial original-family dependent visual confirmations required: ClaudeOpus5.5 "
    "session1c5aebb9-9903-4567-a88a-5da4b472781d then GPT6.1Sol "
    "sessionfd9a447c-6e9f-4874-a043-4851de97c996. Textual closureb6bcc8f1 and "
    "recovered558 HOST3+1+5/no skips inherited honestly. Preserve all original557OOMs/"
    "denials/source/process/read-depth/citation/viewport/fallback/MLKit limits. "
    "HOST-only2g init NEVER enters native builds; no app/guestheap/archiveguard increase. "
    "Then latest-main integration, combined Python368/validator/vocabulary/manifest/"
    "exact虎猿/originalbudgets, normal signed owner fastforward publication/remoteSHA/"
    "terminalgreenCI/EVERYimmutableZIPhash/verified ownerissue60 before083. "
    "Published108/1228,remaining1120,lastPublished1f317f0762513720709ab0ca215f19ff021ca596; "
    "082 not delivered. Physicalphone/generalrelease/whole-set outstanding. "
    "One coordinator/one reviewer maximum, no second runner. Full live history preserved; "
    "approved workspace/control helpers only. Preserve/report/yield on actual new denial "
    "or signinghang without workaround."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def now():
    return datetime.now(timezone.utc).isoformat()


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 558 and progress["batch"] == "082"
    assert not BEFORE.exists()
    for root, head in [(ROOT, HEAD), (ANDROID, ANDROID_HEAD)]:
        assert git("rev-parse", "HEAD", cwd=root) == head
        assert git("log", "-1", "--format=%G?", cwd=root) == "G"
        assert not git("status", "--porcelain", cwd=root)
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = load_request(text)
    assert embedded["checkpoint"] == 558
    save(BEFORE, progress)
    state = {
        "schemaVersion": 1, "execution": 559, "batch": "082", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID_HEAD, "teachingSnapshot": REVIEWED,
        "scope": "SAME082 full native fixture preparation and compilation only; no device/emulator/reviewer/integration/publication/083 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded before task mutation; operative contract, complete issue and final558 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."
        },
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "helper": str(Path(__file__)), "optionalHistoricalHelpersAccessed": False,
            "actualNewPermissionDenials": []
        },
        "freshOriginMain": git("rev-parse", "origin/main"),
        "manifestSha256": sha(ROOT / "manifest.json"),
        "contentVersion": load(ROOT / "manifest.json")["contentVersion"],
        "status": "preparing-native-fixture"
    }
    progress["execution559StartingState"] = state
    progress["stage"] = "batch-082-native-fixture-preparation-in-progress"
    progress["nextAction"] = state["scope"]
    save(CONTROL / "progress.json", progress)
    save(CONTROL / "execution-559-start.json", state)
    print("Starting scope persisted; all live history retained.")


def load_request(text):
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    return json.loads(text.split(marker, 1)[1])


def prepare():
    from fontTools.ttLib import TTFont

    assert git("rev-parse", "HEAD") == HEAD and not git("diff", "--name-only")
    assert not git("status", "--porcelain", cwd=ANDROID)
    assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    refreshing = VERIFICATION.exists()
    if refreshing:
        previous = load(VERIFICATION)
        assert sha(FIXTURE) == previous["fixtureSha256"]
        assert sha(ARCHIVE) == previous["archiveSha256"]
        assert not (LOGS / "native-compile-start.txt").exists()
    else:
        assert not FOLDER.exists() and not ARCHIVE.exists()
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-082-reconciliation.json")
    assert reconciliation["textualReviewClosed"] and not reconciliation["actionableRemainingFindings"]
    assert reconciliation["reviewedTeachingSnapshot"] == REVIEWED
    manifest = load(ROOT / "manifest.json")
    assert manifest["contentVersion"] == "0739a82c9699f031"
    ledger_path = ROOT / "docs" / "n1-sources" / "batch-082-progress.json"
    ledger = load(ledger_path)
    audit = load(ROOT / "docs" / "n1-sources" / "batch-082-draft-font-audit.json")
    assert ledger["sourceReadingOrder"] == {"onyomi": ["ジュン"], "kunyomi": []}
    assert [(i["reading"], i["selected"]) for i in ledger["readingDispositions"]] == [("ジュン", True)]
    names = audit["completeNewArticleScope"]
    assert all(sha(ROOT / name) == expected for name, expected in audit["articleHashes"].items())
    documents = {name: blocks(ROOT / name) for name in [*names, "kanji/教.md", "words/助教授.md"]}
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def show(document, index, kind, value, slug):
        qualifier = "readingExample" if kind == "table" else "articleBullet"
        assert sum(v == value for k, v in documents[document]
                   if (k == "table") == (kind == "table") and k != "heading") == 1
        step = f"{slug}-{index:02}"
        line(f"show({qualifier}({quote(value)}), {quote(step)})")
        selectors.append({"document": document, "kind": kind, "target": value, "step": step})

    def display(document, slug):
        line(f"await({quote(documents[document][0][1])})")
        table_cell = 0
        for index, (kind, value) in enumerate(documents[document][1:], 1):
            if kind == "heading":
                line(f"section({quote(value)})")
            elif kind == "table":
                table_cell += 1
                if table_cell > 3 and table_cell % 3 != 2:
                    show(document, index, kind, value, slug)
            else:
                show(document, index, kind, value, slug)

    def follow(document, label, destination, slug, preferred):
        body = (ROOT / document).read_text(encoding="utf-8")
        sections = re.split(r"^## (.+)\n", body.split("---", 2)[2], flags=re.M)
        candidates = []
        for i in range(1, len(sections), 2):
            for part in re.split(r"\n\s*\n|\n(?=- )", sections[i + 1].strip()):
                for link in re.finditer(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", part):
                    if (ROOT / document).parent.joinpath(link[1]).resolve() == (ROOT / destination).resolve():
                        candidates.append((sections[i], part.removeprefix("- ")))
        section_name, raw = next(v for v in candidates if v[0] == preferred)
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        text = plain(" ".join(part.strip() for part in raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_559" + raw[link.end():]
        offset = plain(" ".join(part.strip() for part in marked.splitlines())).index("N1_LINK_TARGET_559")
        assert text[offset:].startswith(label)
        line(f"section({quote(section_name)})")
        show(document, len(selectors), "paragraph", text, slug)
        line(f"inline(await(articleBullet({quote(text)})), {quote(label)}, {offset})")
        line('await("Article contents")')
        item = {"document": document, "destination": destination, "label": label,
                "section": section_name, "renderedText": text, "offset": offset}
        offsets.append(item)
        return item

    def back_to(item, step):
        line("back()")
        line(f"await(articleBullet({quote(item['renderedText'])})).assertIsDisplayed()")
        line(f"section({quote(item['section'])})")
        line(f"capture({quote(step)})")

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("准")')
    line('click("quasi-; associate rank")')
    display("kanji/准.md", "kanji")
    forward = follow("kanji/准.md", "准教授", "words/准教授.md", "word-forward", "Common words")
    display("words/准教授.md", "word")
    reverse = follow("words/准教授.md", "准", "kanji/准.md", "word-reverse", "How the kanji combine")
    line('section("Readings")')
    line('show(readingExample("ジュン"), "kanji-backlink")')
    back_to(reverse, "system-back-to-word")
    teach = follow("words/准教授.md", "教", "kanji/教.md", "teach-forward", "How the kanji combine")
    line('await("教 — teach, instruct")')
    back_teach = follow("kanji/教.md", "准教授", "words/准教授.md", "teach-reverse", "Common words")
    line('await("准教授 (じゅんきょうじゅ) — associate professor")')
    back_to(back_teach, "system-back-to-teach")
    back_to(teach, "system-back-to-word-from-teach")
    former = follow("words/准教授.md", "助教授", "words/助教授.md", "former-forward", "Synonyms and antonyms")
    line('await("助教授 (じょきょうじゅ) - associate professor (former Japanese title)")')
    successor = follow("words/助教授.md", "准教授", "words/准教授.md", "successor-reverse", "Meaning")
    line('await("准教授 (じゅんきょうじゅ) — associate professor")')
    back_to(successor, "system-back-to-former-title")
    back_to(former, "system-back-to-current-title")
    back_to(forward, "system-back-to-kanji")
    required = {
        ("kanji/准.md", "words/准教授.md"), ("words/准教授.md", "kanji/准.md"),
        ("kanji/教.md", "words/准教授.md"), ("words/准教授.md", "kanji/教.md"),
        ("words/准教授.md", "words/助教授.md"), ("words/助教授.md", "words/准教授.md")
    }
    assert len(offsets) == 6 and {(i["document"], i["destination"]) for i in offsets} == required
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    replacements = [
        ("081", "082"),
        ("smeltingLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies",
         "associateRankLookalikesAndRadicalFallbacksAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineSmeltingTwoReciprocalPairsCuratedOnDrawingAndSystemBack",
         "fullSingleImportOfflineAssociateRankReciprocalAndComparisonLinksCuratedOnDrawingAndSystemBack"),
        ("95a87783e4be501c4b2b788d6906f6cc76b3c751", HEAD),
        ("95a87783", HEAD[:8]), ("f1dd5d8b9d2ff535", manifest["contentVersion"]),
        ("1093", "1094"), ("5049", "5050"), ("113, n1.size", "114, n1.size"),
        ("N1 · 113 cards", "N1 · 114 cards"), ("smelting", "associateRank"),
        ('"冶"', '"准"'), ("smelt; work metals", "quasi-; associate rank"),
        ('listOf("ヤ")', 'listOf("ジュン")'), ('listOf("い.る")', "emptyList<String>()"),
        ('"や"', '"じゅん"'),
        ('assertEquals(7, strokes.length())', 'assertEquals(10, strokes.length())'),
        ('"7 strokes drawn"', '"10 strokes drawn"'),
        ('.put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)',
         '.put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)\n'
         '                .put("comparisonPairs", 1).put("comparisonLinkTransitions", 2)')
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 准 meaning and sole curated on key じゅん due. Source and quiz kun lists empty. Two historical good 准 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "".join(
        (ROOT / name).read_text(encoding="utf-8") for name in names) +
        "".join(audit["changedReusedScope"].values()))))
    assert glyphs == audit["actualHan"] and len(glyphs) == 31
    fonts = []
    for prior_font in audit["fonts"]:
        path = Path(prior_font["path"])
        assert sha(path) == prior_font["sha256"]
        with TTFont(path) as font:
            missing = [c for c in glyphs if ord(c) not in font.getBestCmap()]
        assert missing == prior_font["allActualMissing"] == ["冫", "氵", "辶", "隹"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    words = ["准教授"]
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("准 準 集 進 難 冫 氵 辶 隹 准教授")
    text = re.sub(r'val pages = listOf\([^\n]+\)',
                  "val pages = listOf(" + ", ".join(quote(p) for p in pages) + ")", text, count=1)
    text = text.replace("associateRank / look-alikes / ice and water fallback",
                        "associate rank / look-alikes / radical fallback")
    text = text.replace("Inspect all 29 scoped Han; focused 冶/治/台/始, 冫/氵. Fallback families may coincide.",
                        "Inspect all 31 scoped Han; focused 准/準/集/進/難, 冫/氵/辶/隹. Fallback families may coincide.")
    text = re.sub(r'for \(char in listOf\([^\n]+\)',
                  "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)',
                  "for (word in listOf(" + ", ".join(quote(w) for w in words) + "))", text, count=1)
    text = text.replace("assertEquals(120, rows.length())", "assertEquals(128, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 116)', '.put("individualGlyphProbes", 124)')
    text = text.replace("29 actual scoped Han including exact 冫/氵 fallback inspection",
                        "31 actual scoped Han including exact 冫/氵/辶/隹 fallback inspection")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("081", "冶", "冶金", "ヤ", "い.る", "smelting", "Smelting", "29 scoped",
                  "gold-forward", "gold-reverse", "7 strokes drawn", "val associate rank"):
        assert stale not in text, stale
    for required_text in (
        'assertEquals(listOf("じゅん"), associateRank.toReadingCard().quizKeys(ReadingKind.On))',
        'assertEquals(emptyList<String>(), associateRank.toReadingCard().quizKeys(ReadingKind.Kun))',
        'assertEquals(listOf("ジュン"), card.quizOnyomi?.splitSep())',
        'assertEquals(emptyList<String>(), card.kunyomi.splitSep())',
        'assertEquals(10, strokes.length())',
        'setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name)'
    ):
        assert required_text in text, required_text
    for selector in selectors:
        assert quote(selector["target"]) in text, selector
    for offset in offsets:
        assert quote(offset["renderedText"]) in text, offset
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
        "words": sum(n.startswith("words/") for n in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (ROOT / "kanji").glob("*.md"))
    }
    assert counts == {"kanji": 1094, "words": 5050, "n1": 114}
    if not refreshing:
        subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-082/",
                        f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        prefix = "n1-batch-082/"
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith(prefix) and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read(prefix + "manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=ROOT)
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
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected, name
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in archive.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    assert verified == 8372
    FOLDER.mkdir(exist_ok=True)
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-081.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(PRIOR.relative_to(ROOT)), tofile=str(FIXTURE.relative_to(ROOT)), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 559, "batch": "082", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED, "androidSnapshot": ANDROID_HEAD,
        "productionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "qualifiedAndroidDelta": "TEST-ONLY loader recovery; production unchanged, see execution-558.json.",
        "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": str(PRIOR.relative_to(ROOT)), "priorHarnessSha256": sha(PRIOR),
        "fixtureDiff": str(diff.relative_to(ROOT)), "fixtureDiffSha256": sha(diff),
        "staticProjection": "Durable Markdown subset checked against production Markdown.kt; selectors/offsets are not native visibility.",
        "articleFiles": [{"path": n, "sha256": sha(ROOT / n), "projectedTextBlocks": len(documents[n])} for n in names],
        "changedReusedScope": audit["changedReusedScope"],
        "sourceReadingLedger": str(ledger_path.relative_to(ROOT)), "sourceReadingLedgerSha256": sha(ledger_path),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 2, "changedReusedPassages": 2,
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
        "comparisonPairs": 1, "comparisonDirectedTransitions": 2,
        "plannedNativePaintProbes": 124, "plannedWholeWordRasterProbes": 4,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "currentFontAudit": fonts, "fullReadings": {"on": ["ジュン"], "kun": []},
        "curatedReadings": {"on": ["ジュン"], "kun": []},
        "normalizedQuizKeys": {"on": ["じゅん"], "kun": []},
        "pendingCmapAbsences": ["冫", "氵", "辶", "隹"],
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": "Preparation only; no native rendering, visual, handwriting, phone or publication acceptance. No duplicate parser preflight; production ContentSync once. Static projections/hashes are not visibility/readability/fallback-face evidence. HOST-only2g init NEVER enters native builds; no app/guest heap/archive guard changes. Fresh port/device/PID ownership inspection mandatory immediately before launch. Historical limitations retained."
    }
    save(VERIFICATION, record)
    print(json.dumps({key: record[key] for key in ("status", "expectedCounts", "zipEntries",
                     "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))


def record():
    starting = load(CONTROL / "execution-559-start.json")
    fixture = load(VERIFICATION)
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain", cwd=ANDROID)
    assert git("rev-parse", "HEAD", cwd=ANDROID) == ANDROID_HEAD
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert sha(ROOT / "manifest.json") == starting["manifestSha256"]
    assert (LOGS / "native-compile-exit.txt").read_text().strip() == "0"
    result = next(line for line in (LOGS / "native-compile.txt").read_text().splitlines()
                  if line.startswith("BUILD SUCCESSFUL"))
    assert "0 error(s)" in (LOGS / "validate.txt").read_text()
    assert sha(FIXTURE) == fixture["fixtureSha256"]
    assert sha(ARCHIVE) == fixture["archiveSha256"]
    args = load(LOGS / "native-compile-arguments.json")
    assert args == [":app:assembleDebugAndroidTest", "--no-daemon", "--no-parallel", "--max-workers=1",
                    "-Pkotlin.compiler.execution.strategy=in-process"]
    apk = CONTROL / "artifacts" / "n1-batch-082-native-test.apk"
    app = CONTROL / "artifacts" / "n1-batch-082-native-app.apk"
    assert sha(app) == "0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407"
    assert sha(ANDROID / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk") == sha(app)
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/n1-batch-082-4f5812bc-envelope.zip")).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch082GlyphTest", "N1Batch082ArticleTest",
                     "associateRankLookalikesAndRadicalFallbacksAcrossFourProductionFamilies",
                     "fullSingleImportOfflineAssociateRankReciprocalAndComparisonLinksCuratedOnDrawingAndSystemBack"):
            assert name.encode() in dex, name
    manifest = load(ROOT / "manifest.json")
    with zipfile.ZipFile(ARCHIVE) as archive:
        verified = 0
        for section, mapping in manifest.items():
            if not isinstance(mapping, dict):
                continue
            for name, expected in mapping.items():
                data = (ROOT / name).read_bytes()
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected
                assert archive.read("n1-batch-082/" + name).replace(b"\r\n", b"\n") == data.replace(b"\r\n", b"\n")
                verified += 1
    assert verified == 8372
    text = FIXTURE.read_text(encoding="utf-8")
    for selector in fixture["staticMarkdownSelectors"]:
        assert quote(selector["target"]) in text, selector
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    receipts = FOLDER / "preparation-receipts"
    assert not receipts.exists()
    receipts.mkdir()
    copied = []
    for source in (Path(__file__), CONTROL / "execution-550.py",
                   CONTROL / "run-559-native-compile.ps1", CONTROL / "post-559-issue.ps1"):
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        copied.append({"path": target.relative_to(ROOT).as_posix(), "sha256": sha(target)})
    for name in ("native-compile.txt", "native-compile-start.txt", "native-compile-end.txt",
                 "native-compile-exit.txt", "native-compile-arguments.json", "validate.txt", "manifest.txt"):
        source = LOGS / name
        target = FOLDER / name
        if name == "native-compile.txt":
            raw = FOLDER / "native-compile-raw.txt.gz"
            raw.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(raw.read_bytes()) == source.read_bytes()
            target.write_text("\n".join(line.rstrip() for line in source.read_text().splitlines()) + "\n", encoding="utf-8")
            copied.append({"path": raw.relative_to(ROOT).as_posix(), "sha256": sha(raw),
                           "decompressedSha256": sha(source)})
        else:
            target.write_text(source.read_text(encoding="utf-8-sig"), encoding="utf-8")
        copied.append({"path": target.relative_to(ROOT).as_posix(), "sha256": sha(target),
                       "sourceSha256": sha(source), "textNormalization": "UTF-8 without BOM; readable compile log strips trailing whitespace. Raw compile bytes preserved separately."})
    frozen = ROOT / "docs" / "n1-sources" / VERIFICATION.name
    shutil.copyfile(VERIFICATION, frozen)
    evidence = {
        **starting, "schemaVersion": 1, "checkpoint": 559, "status": "continue",
        "stage": "batch-082-native-fixture-compiled-awaiting-execution", "completedAt": now(),
        "nativePreparation": fixture, "fixtureVerification": frozen.relative_to(ROOT).as_posix(),
        "fixtureVerificationSha256": sha(frozen),
        "compile": {
            "arguments": args, "exitCode": 0, "buildResult": result,
            "startedAt": (LOGS / "native-compile-start.txt").read_text().strip(),
            "endedAt": (LOGS / "native-compile-end.txt").read_text().strip(),
            "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
            "oneWorker": True, "parallel": False, "hostOnlyHeapInitUsed": False,
            "productionOrGuestHeapChanged": False, "archiveGuardsChanged": False,
            "apk": str(apk), "apkSha256": sha(apk), "apkBytes": apk.stat().st_size,
            "appApk": str(app), "appApkSha256": sha(app),
            "appApkProvenance": "Unchanged production f9b59a2 debug APK, hash pinned by accepted batch081 native receipt/run-551-native.ps1. Test-only qualified1c1b7bf4 does not modify production or build configuration.",
            "apkContainsExactFrozenArchive": True, "bothClassesAndMethodsInDex": True,
            "temporarySourceAndAssetRemoved": True, "androidWorktreeClean": True
        },
        "archivedReceipts": copied, "originalCompileLogPreservedByteForByteInGzip": True,
        "inheritedHostGate": "docs/n1-sources/execution-558.json: fresh non-skipped RealContent3/RareHan1/loaderRegression5; not rerun.",
        "textualClosure": "docs/n1-reviews/batch-082-reconciliation.json",
        "validatorErrors": 0, "manifestFresh": True, "manifestBytesUnchanged": True,
        "runtimeHashesReverified": verified, "runtimeUnchanged": True, "runtimePublished": False,
        "nativeExecuted": False, "deviceOrEmulatorInspected": False,
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": starting["freshOriginMain"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "limits": "Native fixture preparation and compilation only; no native case, device, PNG/visual, handwriting, phone, publication or whole-set acceptance. Original source/reviewer/read-depth/process/denial/OOM/citation/viewport/fallback/MLKit limits retained. Host-only2g init never used.",
        "diagnostics": [
            "Initial console summary hit cp1252 UnicodeEncodeError after complete request load/checkpoint parse; final checkpoint subsequently read directly. No task mutation preceded it.",
            "Initial guessed Markdown content-package path absent; actual core/markdown/Markdown.kt then read. No access denial or missing mandatory input.",
            "Precompile projection assertion caught indentation in wrapped list links; normalized continuation lines exactly as production Markdown does.",
            "Precompile actual diff inspection caught broad identifier substitution also changing associate rank prose. Corrected identifier-only migration, regenerated unexecuted fixture/diff and added exact-selector preservation assertions before compile. No content source edit, native attempt or false acceptance."
        ]
    }
    save(ROOT / "docs" / "n1-sources" / "execution-559.json", evidence)
    print(json.dumps({"stage": evidence["stage"], "apkSha256": sha(apk),
                      "archiveInsideApkExact": True, "receipts": len(copied)}, indent=2))


def verify():
    ev = load(ROOT / "docs" / "n1-sources" / "execution-559.json")
    expected = {"docs/n1-sources/execution-559.json", ev["fixtureVerification"],
                "docs/n1-reviews/batch-082-native/N1Batch082NativeTest.kt",
                "docs/n1-reviews/batch-082-native/fixture-from-081.diff"}
    for entry in ev["archivedReceipts"]:
        expected.add(entry["path"])
        assert sha(ROOT / entry["path"]) == entry["sha256"]
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    assert staged == expected, (staged - expected, expected - staged)
    for path in staged:
        indexed = subprocess.check_output(["git", "show", ":" + path], cwd=ROOT)
        assert indexed == (ROOT / path).read_bytes(), path
        if path.endswith(".json"):
            load(ROOT / path)
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
    assert sha(ROOT / "manifest.json") == ev["manifestSha256"]
    print(json.dumps({"stagedFiles": len(staged), "allIndexBytesExact": True,
                      "runtimeUnchanged": True}, indent=2))


def checkpoint():
    progress, original = load(CONTROL / "progress.json"), load(BEFORE)
    assert progress["checkpoint"] == 558 and progress["batch"] == "082"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD", cwd=ANDROID) == ANDROID_HEAD
    assert not git("diff", HEAD, signed, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    ev = load(ROOT / "docs" / "n1-sources" / "execution-559.json")
    receipt = load(CONTROL / "execution-559-issue-response.json")
    body = (CONTROL / "execution-559-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.rstrip()
    assert signed in receipt["body"] and "issues/60#issuecomment-" in receipt["html_url"]
    assert sha(ROOT / "manifest.json") == ev["manifestSha256"]
    for entry in ev["archivedReceipts"]:
        assert sha(ROOT / entry["path"]) == entry["sha256"]
    result = {
        "schemaVersion": 1, "execution": 559, "checkpoint": 559, "batch": "082",
        "savedCommit": signed, "signature": "G", "status": "continue", "stage": ev["stage"],
        "evidence": "docs/n1-sources/execution-559.json", "qualifiedAndroidHead": ANDROID_HEAD,
        "compileExitCode": 0, "nativeCasesExecuted": 0, "nativeExecuted": False,
        "fixtureSha256": ev["nativePreparation"]["fixtureSha256"],
        "archiveSha256": ev["nativePreparation"]["archiveSha256"],
        "testApkSha256": ev["compile"]["apkSha256"], "appApkSha256": ev["compile"]["appApkSha256"],
        "runtimePayloadHashesVerified": 8372, "contentVersion": ev["contentVersion"],
        "runtimeBytesUnchanged": True, "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(original),
        "changedRootFields": ["checkpoint", "status", "stage", "nextAction", "blocker"]
    }
    allowed = set(result["changedRootFields"])
    for key, value in original.items():
        assert key in allowed or progress[key] == value, key
    progress.update(checkpoint=559, status="continue", stage=result["stage"], nextAction=NEXT, blocker=None)
    progress["execution559CoordinatorCheckpoint"] = result
    progress["batch082NativePreparation"] = result
    progress["execution559StartingState"]["status"] = "signed-local-native-preparation-checkpoint-complete"
    temporary = CONTROL / "execution-559-progress.tmp.json"
    save(temporary, progress)
    written = load(temporary)
    for key, value in original.items():
        assert key in allowed or written[key] == value, key
    assert written["execution559CoordinatorCheckpoint"] == result
    temporary.replace(CONTROL / "progress.json")
    save(CONTROL / "execution-559-final-verification.json", result)
    print(json.dumps({"checkpoint": 559, "savedCommit": signed, "status": "continue",
                      "historyKeysPreserved": len(original), "issueUpdate": receipt["html_url"]}, indent=2))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "verify": verify, "checkpoint": checkpoint}[sys.argv[1]]()
