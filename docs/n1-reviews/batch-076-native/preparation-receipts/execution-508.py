import ast
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
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "3170476c-7f4a-41ac-8eba-4098c59992c0"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews" / "batch-076-native"
HEAD = "b89b333682fa5bfb4123ea8f4a74c2cc59935a7c"
REVIEWED = "08d63143e0495940d7cccee4c1808282a533c522"
ANDROID = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PRIOR = R / "docs" / "n1-reviews" / "batch-075-native" / "N1Batch075NativeTest.kt"
FIXTURE = V / "N1Batch076NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-076-b89b3336-envelope.zip"
APK = C / "artifacts" / "n1-batch-076-native-test.apk"
LIMITS = (
    "Preparation/compilation only; no emulator, native execution, PNG inspection or visual acceptance. "
    "Static projections/offsets and raster hashes do not establish visibility/readability or fallback face. "
    "Reference-touch trace is not human handwriting/MLKit evidence. Fresh507 HOST3+1 remains distinct; "
    "HOST-only2GiBinit NEVER enters native builds. No guest/app heap/archiveguard changes, teaching/app "
    "edits, reviewer or publication. Historical denials/OOMs/failed lookups/read-depth limits retained. "
    "Physical-phone/general-release/whole-set acceptance remains outstanding."
)
NEXT = (
    "SAME076 execute compiled control\\artifacts\\n1-batch-076-native-test.apk ONLY after fresh device/"
    "5580/5581 local+remote connection/PID ownership inspection. Read docs\\n1-sources\\execution-508.json "
    "and batch-076-native-preparation.json. Established read-only API35 N3_Acceptance_20261029 "
    "emulator-5580, hostGPU/Vulkan-disabled2048MiB/two-core flags; record actual owned parent/QEMU and "
    "stop only owned helper. Batch0405584override NOT inherited. No HOST-only2GiBinit for native; no heap/"
    "guard increases. Both N1Batch076GlyphTest and N1Batch076ArticleTest require terminal0, zero skips "
    "and actual PNG inspection; preparation is not acceptance. Full signedb89b3336 Git archive via "
    "production ContentSync ONCE:1088kanji5045words108N1,version8bd0a375668bee11,problems0,epoch1. "
    "Full+Lite rawケン andか.ねる/-か.ねる source order; curatedケン/か.ねる, actualけん/かねる "
    "each Good/Done2correct, no duplicate suffix question/log. Complete兼/兼任, exact changed兼ねる "
    "two linked paragraphs and任 bullet, all3mappedpairs6directions; selection/meaning/readings/"
    "ten-stroke reference-touch/ungradedtrace/recallAgain/articles/SystemBack/offline.41scopedHan "
    "across4productionfamilies in two bounded panels plus focused兼/典/具/曲/八/人/亻 and "
    "兼任/兼ねる panel; two wholewordrasters per family. Cmapabsence NOTglyphfailure; hashes NOT"
    "readability/fallbackface. Then two SERIAL different-family original-session visual confirmations "
    "where possible. Fresh507HOST3+1 retained; no redundant rerun. No teaching changes/publication/077 "
    "this checkpoint. Later currentmainnormalmerge/revalidation/normalsigning/ownerfastforward/greenCI/"
    "EVERYimmutableZIPhash/originalbudgets/ownerissue60receipt remain. No unreviewedpush/signingretry/"
    "permissionworkaround/authoragents/secondrunner. Preserve FULLlivehistory, source recipes, "
    "originalreports and reviewedbaseline虎/猿/丘/山exceptions. Published102/1228,remaining1126; "
    "necessarysupportsNOTN1vocabulary. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/"
    "whole-set outstanding. Overall project incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".execution508.tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    assert load(path) == value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd, encoding="utf-8").strip()


def unchanged():
    assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert git("rev-parse", "HEAD", cwd=A) == ANDROID
    assert not git("status", "--porcelain", cwd=A)


def quote(text):
    return json.dumps(text, ensure_ascii=False).replace("$", "\\$")


def start():
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["status"], p["batch"]) == (507, "continue", "076")
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    unchanged()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert embedded["checkpoint"] == 507
    assert not (L / "execution-508-before-progress.json").exists()
    save(L / "execution-508-before-progress.json", p)
    p["execution508StartingState"] = {
        "execution": 508, "batch": "076", "startingHead": HEAD, "androidHead": ANDROID,
        "scope": "SAME076 bounded full signed Git archive native fixture preparation/compilation and normally signed local evidence checkpoint only; no device/reviewer/publication/077/second runner.",
        "status": "native-preparation-in-progress", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, final507 checkpoint and complete approved issue inspected directly. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
    }
    p["stage"] = "batch-076-native-preparation-in-progress"
    save(C / "progress.json", p)
    print("SAME076 preparation scope saved; complete live history retained.")


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    unchanged()
    assert not V.exists() and not ARCHIVE.exists() and not APK.exists()
    m = load(R / "manifest.json")
    assert m["contentVersion"] == "8bd0a375668bee11"
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in m["files"]),
        "words": sum(n.startswith("words/") for n in m["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (R / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1088, "words": 5045, "n1": 108}
    ledger = load(S / "batch-076-progress.json")
    audit = load(S / "batch-076-draft-audit.json")
    helper = R / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    selected = ast.Module(body=[n for n in parsed.body if isinstance(n, ast.FunctionDef)
                               and n.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(selected, str(helper), "exec"), namespace)
    names = audit["actualAuthoredHanFonts"]["articles"]
    documents = {n: namespace["blocks"](R / n) for n in names}
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
        projected = documents[document]
        line(f"await({quote(projected[0][1])})")
        table_cell = 0
        for index, (kind, value) in enumerate(projected[1:], 1):
            if kind == "heading":
                line(f"section({quote(value)})")
            elif kind == "table":
                table_cell += 1
                if table_cell > 3 and table_cell % 3 != 2:
                    show(document, index, kind, value, slug)
            else:
                show(document, index, kind, value, slug)

    def follow(document, label, destination, slug):
        body = (R / document).read_text(encoding="utf-8")
        sections = re.split(r"^## (.+)\n", body.split("---", 2)[2], flags=re.M)
        candidates = []
        for i in range(1, len(sections), 2):
            for part in re.split(r"\n\s*\n|\n(?=- )", sections[i + 1].strip()):
                for link in re.finditer(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", part):
                    if (R / document).parent.joinpath(link[1]).resolve() == (R / destination).resolve():
                        candidates.append((sections[i], part.removeprefix("- ")))
        preferred = "Common words" if document.startswith("kanji/") else "How the kanji combine"
        section_name, raw = next((v for v in candidates if v[0] == preferred), candidates[0])
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        text = namespace["plain"](" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_508" + raw[link.end():]
        offset = namespace["plain"](" ".join(marked.splitlines())).index("N1_LINK_TARGET_508")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("兼")')
    line('click("combine; concurrent roles")')
    display("kanji/兼.md", "kanji")
    for word in ("兼ねる", "兼任"):
        document = f"words/{word}.md"
        forward = follow("kanji/兼.md", word, document, word + "-forward")
        if word == "兼任":
            display(document, word)
        else:
            for section_name in ("How the kanji combine", "Synonyms and antonyms"):
                line(f"section({quote(section_name)})")
                index = next(i for i, b in enumerate(documents[document]) if b == ("heading", section_name))
                kind, value = documents[document][index + 1]
                show(document, index + 1, kind, value, word)
        reverse = follow(document, "兼", "kanji/兼.md", word + "-reverse")
        line('section("Readings")')
        line(f'show(readingExample("ケン"), {quote(word + "-kanji-backlink")})')
        back_to(reverse, word + "-system-back-to-word")
        for char, mapped_word in ledger["allMappedReciprocalPairs"]:
            if mapped_word != document or char == "兼":
                continue
            component = follow(document, char, f"kanji/{char}.md", word + "-" + char)
            if char == "任":
                kind, value = documents["kanji/任.md"][1]
                show("kanji/任.md", 1, kind, value, "任-fallback")
            counterpart = follow(f"kanji/{char}.md", word, document, char + "-counterpart")
            line('section("How the kanji combine")')
            line(f"show(articleBullet({quote(component['renderedText'])}), {quote(word + '-' + char + '-component-backlink')})")
            back_to(counterpart, word + "-" + char + "-system-back-to-component")
            back_to(component, word + "-" + char + "-system-back-from-component")
        back_to(forward, word + "-system-back-to-kanji")
    assert len(offsets) == 6
    assert {(i["document"], i["destination"]) for i in offsets} == {
        (i["from"], i["to"]) for i in ledger["directedLinks"]
    }
    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("075", "076"),
        ("referenceTextsLookalikesAndFourFallbacksAcrossFourProductionFamilies",
         "concurrentRolesLookalikesAndPersonFallbackAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineReferenceTextsTwelveReciprocalPairsTwoOnReadingsDrawingAndSystemBack",
         "fullSingleImportOfflineConcurrentRolesThreeReciprocalPairsBothReadingsDrawingAndSystemBack"),
        ("fba1a8868b82cd93d7bfaeae1080f5642bd92730", HEAD), ("fba1a886", HEAD[:8]),
        ("2759d7b13c89eb8f", m["contentVersion"]), ("1087", "1088"), ("5044", "5045"),
        ("107, n1.size", "108, n1.size"), ("N1 · 107 cards", "N1 · 108 cards"),
        ("referenceTexts", "concurrentRoles"), ('"典"', '"兼"'),
        ("reference texts; rules; ceremony", "combine; concurrent roles"),
        ('listOf("テン", "デン")', 'listOf("ケン")'),
        ('listOf("ふみ", "のり")', 'listOf("か.ねる", "-か.ねる")'),
        ("emptyList<String>()", 'listOf("か.ねる")'),
        ('listOf("てん", "でん")', 'listOf("けん")'),
        ('(kind == ReadingKind.On && key in setOf("てん", "でん"))',
         '((kind == ReadingKind.On && key == "けん") || (kind == ReadingKind.Kun && key == "かねる"))'),
        ("典 meaning and two curated on keys due; raw source-only ふみ/のり retained but no kun keys.",
         "兼 meaning and curated on/kun due; valid suffix -か.ねる retained but not selected separately; one かねる key."),
        ("Two historical good 典 meaning logs", "Two historical good 兼 meaning logs"),
        ("bothCuratedOnKeysPersistedGoodNoKunAndDone", "bothCuratedKindsPersistedGoodNoDuplicateSuffixAndDone"),
        ('.put("mappedReciprocalPairs", 12).put("directedLinkTransitions", 24)',
         '.put("mappedReciprocalPairs", 3).put("directedLinkTransitions", 6)'),
        ("assertEquals(8, strokes.length())", "assertEquals(10, strokes.length())"),
        ('"8 strokes drawn"', '"10 strokes drawn"'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = text.replace('assertEquals(listOf("か.ねる"), concurrentRoles.toReadingCard().quizKeys(ReadingKind.Kun))',
                        'assertEquals(listOf("かねる"), concurrentRoles.toReadingCard().quizKeys(ReadingKind.Kun))')
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    begin = text.index("            val answeredKeys =")
    end = text.index("            rule.waitUntil(30_000) { (model(\"kreading:\") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }", begin)
    text = text[:begin] + '''            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("兼", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "けん" else "かねる"
                assertEquals(key, question.question.correctKey)
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-${question.question.kind}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (question.question.kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${question.question.kind}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "兼" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
''' + text[end:]
    begin = text.index('            assertFalse(runBlocking {', text.index("assertEquals(2, done.correct)"))
    end = text.index('            back()\n            await("Meaning quiz")', begin)
    text = text[:begin] + '''            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "兼" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("けん", "かねる"), readingLogs.map { it.reading }.toSet())
            capture("curated-both-done")
''' + text[end:]
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                                  "".join((R / n).read_text(encoding="utf-8") for n in names))))
    assert glyphs == audit["actualAuthoredHanFonts"]["characters"] and len(glyphs) == 41
    words = ["兼任", "兼ねる"]
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("兼 典 具 曲 八 人 亻 " + " ".join(words))
    text = re.sub(r'val pages = listOf\([^\n]+\)', "val pages = listOf(" + ", ".join(quote(p) for p in pages) + ")", text, count=1)
    text = text.replace("Batch 076: reference texts / look-alikes / fallback",
                        "Batch 076: concurrent roles / look-alikes / fallback")
    text = text.replace("Inspect all 117 scoped Han; focused 奠/亅/厂/艹 and 典/具/曲/共. Fallback families may coincide.",
                        "Inspect all 41 scoped Han; focused 兼/典/具/曲/八 and 人/亻. Fallback families may coincide.")
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
                  "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)',
                  "for (word in listOf(" + ", ".join(quote(w) for w in words) + "))", text, count=1)
    text = text.replace("assertEquals(492, rows.length())", "assertEquals(172, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 468).put("wholeWordRasterProbes", 24).put("panels", 6)',
                        '.put("individualGlyphProbes", 164).put("wholeWordRasterProbes", 8).put("panels", 3)')
    text = text.replace("117 scoped authored Han including 奠/亅/厂/艹, four production families, six bounded Compose panels and 24 whole-word rasters.",
                        "41 scoped authored Han including pre-existing 亻, four production families, three bounded Compose panels and eight whole-word rasters.")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("075", "ふみ", "のり", "テン", "デン", "てん", "でん", "referenceTexts", "香典", "奠", "two-on", "NoKun"):
        assert stale not in text, stale
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-076/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.namelist()
        prefix = "n1-batch-076/"
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith(prefix) and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = z.read(prefix + "manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=R)
        assert json.loads(raw) == m
        retained, verified = len(raw), 0
        for section, mapping in m.items():
            if not isinstance(mapping, dict):
                continue
            for name, expected in mapping.items():
                data = z.read(prefix + name)
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected, name
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in z.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    assert verified == 8355
    V.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = V / "fixture-from-075.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(PRIOR.relative_to(R)), tofile=str(FIXTURE.relative_to(R)), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 508, "batch": "076", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED, "androidSnapshot": ANDROID,
        "contentVersion": m["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": str(PRIOR.relative_to(R)), "priorHarnessSha256": sha(PRIOR),
        "staticProjectionHelper": str(helper.relative_to(R)), "staticProjectionHelperSha256": sha(helper),
        "fixtureDiff": str(diff.relative_to(R)), "fixtureDiffSha256": sha(diff),
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(b)}
                         for n, b in documents.items()],
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 2, "changedReusedPassages": 3,
        "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6,
        "plannedNativePaintProbes": 164, "plannedWholeWordRasterProbes": 8,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "fullReadings": {"on": ["ケン"], "kun": ["か.ねる", "-か.ねる"]},
        "curatedReadings": {"on": ["ケン"], "kun": ["か.ねる"]},
        "normalizedQuizKeys": {"on": ["けん"], "kun": ["かねる"]},
        "suffixDisposition": "Valid usual-kana suffix is retained, not source-only; same かねる key is not a second question or mastery event.",
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": LIMITS, "nextAction": NEXT,
    }
    save(C / "batch-076-native-fixture-verification.json", record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries",
                     "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print("Static selectors:", len(selectors), "; directed links:", len(offsets))


def archive():
    unchanged()
    preparation = load(C / "batch-076-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    raw_log = L / "native-compile.txt"
    text = raw_log.read_text(encoding="utf-8-sig")
    assert (L / "native-compile-exit.txt").read_text().strip() == "0" and "BUILD SUCCESSFUL" in text
    with zipfile.ZipFile(APK) as z:
        assert hashlib.sha256(z.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [z.read(n) for n in z.namelist() if re.fullmatch(r"classes\d*\.dex", n)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch076{kind}Test;".encode() in b for b in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch075{kind}Test;".encode() not in b for b in dex)
        for method in (
            "concurrentRolesLookalikesAndPersonFallbackAcrossFourProductionFamilies",
            "fullSingleImportOfflineConcurrentRolesThreeReciprocalPairsBothReadingsDrawingAndSystemBack",
        ):
            assert any(method.encode() in b for b in dex), method
    (V / "compile.txt").write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")
    (V / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    receipts = V / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-508.py")
    shutil.copyfile(C / "run-508-native-compile.ps1", receipts / "run-508-native-compile.ps1")
    save(S / "batch-076-native-preparation.json", preparation)
    inherited = load(S / "execution-507.json")
    for item in inherited["tests"]:
        assert sha(R / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 8bd0a375668bee11")):
        source = L / f"{name}-508.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = V / f"{name}.txt"
        target.write_text("\n".join(line.rstrip() for line in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(R)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 508, "batch": "076", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(C / "progress.json")["execution508StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-076-native-preparation.json",
        "preparationSha256": sha(S / "batch-076-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "exitCode": 0, "status": "compiled-not-executed",
            "startedAt": (L / "native-compile-start.txt").read_text().strip(),
            "endedAt": (L / "native-compile-end.txt").read_text().strip(),
            "result": re.search(r"BUILD SUCCESSFUL in (.+)", text).group(0),
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "log": str((V / "compile.txt").relative_to(R)), "logSha256": sha(V / "compile.txt"),
            "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "apk": str(APK), "apkSha256": sha(APK), "apkBytes": APK.stat().st_size,
            "packagedExactFullArchiveVerified": True, "bothClassesAndMethodsVerified": True,
            "old075DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "staticSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 2, "changedReusedPassages": 3,
            "readingLabelsAndExplanations": 6, "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6,
            "staticOnlyNotActualVisualCoverage": True, "exactLedgerDirectedLinksAndPairsVerified": True,
            "completeActualAuthoredHanReinventoried": True,
        },
        "accepted507AndroidRetainedWithoutRerun": True, "inheritedArchivedXmlHashesReverified": True,
        "textualReconciliationSha256": sha(R / "docs" / "n1-reviews" / "batch-076-reconciliation.json"),
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 102, "remainingAdditions": 1126, "nextAction": NEXT, "limits": LIMITS,
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(R)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(V.rglob("*")) + [S / "batch-076-native-preparation.json"] if path.is_file()
    ]
    save(S / "execution-508.json", record)
    print("Exact packaged archive, both cases, inherited Android XML and cleanup verified.")


def checkpoint():
    unchanged()
    record = load(S / "execution-508.json")
    for item in record["artifacts"]:
        path = R / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    p = load(C / "progress.json")
    before = load(L / "execution-508-before-progress.json")
    assert all(p[k] == value for k, value in before.items() if k != "stage")
    assert set(p) == set(before) | {"execution508StartingState"}
    receipt = {
        "execution": 508, "checkpoint": 508, "batch": "076", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-508.json",
        "recordSha256": sha(S / "execution-508.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=508, status="continue", stage="batch-076-native-compiled-pending-execution",
             nextAction=NEXT, blocker=None)
    p["execution508StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    p["batch076NativePreparationCheckpoint"] = receipt
    p["execution508CoordinatorCheckpoint"] = receipt
    p["activeExecution"] = receipt
    save(C / "progress.json", p)
    save(L / "checkpoint-508.json", receipt)
    (L / "issue-508-body.txt").write_text(
        f"Batch 076 native-preparation checkpoint **508** saved locally at `{receipt['savedCommit']}` "
        "(normal signature verified; **not published**). Complete signed Git archive preserved with "
        "**8,355 runtime hashes verified**, original budgets unchanged, and the instrumentation APK "
        "compiled successfully with one Gradle worker and no HOST heap init. Exact embedded archive, "
        "both new test classes/methods, six directed links/three mapped pairs, complete new articles/"
        "three changed reused passages, all three raw readings with two offered keys, ten-stroke "
        "fixture and 41-Han/four-family font scope verified statically. Temporary Android source/asset "
        "removed; dedicated worktrees clean. `docs/n1-sources/execution-508.json` and "
        "`batch-076-native-preparation.json` retain hashes/commands/limits.\n\n"
        "**No emulator, native execution, screenshot inspection or visual acceptance claimed.** "
        "Fresh checkpoint507 HOST3+1 retained without rerun. Next: fresh device/port/PID ownership "
        "inspection, approved disposable API35 native cases with terminal case0 and actual PNG "
        "inspection; then two serial different-family visual confirmations. Current-main integration/"
        "validation/signing/owner fast-forward/CI/immutable public ZIP gates remain. "
        "**102/1,228 additions published; 1,126 remain.** Necessary supports are not an N1 vocabulary "
        "deck. Compatible Android `f9b59a2`+ required; physical-phone/general-release/whole-set acceptance "
        "outstanding. Status `continue`; batch077 not started.",
        encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("checkpoint", "savedCommit", "status", "nativeExecuted")}, indent=2))


def finalize():
    p = load(C / "progress.json")
    before = load(L / "execution-508-before-progress.json")
    receipt = load(L / "issue-508-verified.json")
    record = load(S / "execution-508.json")
    assert p["checkpoint"] == 508 and p["status"] == "continue"
    assert receipt["author"] == "stop-cran" and receipt["bodyVerified"]
    assert git("rev-parse", "HEAD") == receipt["savedCommit"]
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    unchanged()
    assert sha(APK) == record["compilation"]["apkSha256"]
    for item in record["artifacts"]:
        assert sha(R / item["path"]) == item["sha256"]
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker", "activeExecution"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    assert p["lastPublishedCommit"] == before["lastPublishedCommit"]
    for key in ("batch076NativePreparationCheckpoint", "execution508CoordinatorCheckpoint", "activeExecution"):
        p[key].update(issueUpdate=receipt["url"], ownerAuthorAndBodyVerified=True)
    p["batch076NativePreparationIssueReceipt"] = receipt
    save(C / "progress.json", p)
    save(L / "checkpoint-508-full.json", p)
    final = {
        "checkpoint": 508, "status": "continue", "batch": "076", "savedCommit": receipt["savedCommit"],
        "signature": "G", "nativeFixtureCompiled": True, "exactPackagedArchiveVerified": True,
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allPriorHistoricalKeysPreserved": True, "ownerIssueReceipt": receipt["url"],
        "publishedAdditions": 102, "remainingAdditions": 1126,
    }
    save(L / "final-508-verification.json", final)
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "archive": archive,
     "checkpoint": checkpoint, "finalize": finalize}[sys.argv[1]]()
