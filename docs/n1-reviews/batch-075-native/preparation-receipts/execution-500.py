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
L = C / "logs" / "f607f7dd-9981-4610-8f5c-bcbe1d67a19d"
V = R / "docs" / "n1-reviews" / "batch-075-native"
S = R / "docs" / "n1-sources"
HEAD = "fba1a8868b82cd93d7bfaeae1080f5642bd92730"
REVIEWED = "f5b70805d4a4a99d27036c71701277f1b8fc8b00"
ANDROID = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PRIOR = C / "artifacts" / "batch-074-native-attempt-3" / "N1Batch074NativeTest.kt"
FIXTURE = V / "N1Batch075NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-075-fba1a886-envelope.zip"
APK = C / "artifacts" / "n1-batch-075-native-test.apk"
LIMITS = (
    "Preparation/compilation only; no native execution, PNG inspection or visual acceptance. "
    "Static projections and offsets do not establish visibility/readability. Raster hashes do not "
    "identify fallback faces. Reference-touch trace is not human handwriting/MLKit evidence. "
    "Inherited accepted074 evidence and fresh499 HOST3+1 remain distinct. No HOST heap init for "
    "native, guest/app heap changes, guard changes, teaching edits, reviewers or publication. "
    "Original Claude initial eight multi-tool responses/thirty overlapping starts and false serial "
    "claim remain preserved; later serial confirmation is not retroactive compliance. "
    "Physical-phone/general-release/whole-set acceptance remains outstanding."
)
NEXT = (
    "SAME075 execute compiled control\\artifacts\\n1-batch-075-native-test.apk ONLY after fresh "
    "device/5580/5581 local+remote connection/PID ownership inspection. Read docs\\n1-sources\\"
    "execution-500.json and batch-075-native-preparation.json. Established read-only API35 "
    "N3_Acceptance_20261029 emulator-5580, hostGPU/Vulkan-disabled2048MiB/two-core flags; record actual "
    "owned parent/QEMU and stop only owned helper. Batch0405584override NOT inherited. No HOST-only"
    "2GiBinit for native; no heap/guard increases. Both N1Batch075GlyphTest and N1Batch075ArticleTest "
    "require terminal0, zero skips and actual PNG inspection; preparation is not acceptance. Full "
    "signedfba1a886 Git archive via production ContentSync ONCE:1087kanji5044words107N1, "
    "version2759d7b13c89eb8f,problems0,epoch1. Full+Lite rawテン/デン andふみ/のり source order; "
    "curatedテン/デン+emptykun, actualてん/でん each Good/Done2correct, no kun key/log. Complete"
    "典/香典, four reused component passages, six olderkanji changed navigation passages, all12"
    "mappedpairs24directedlinks including unchanged型, selection/meaning/readings/eight-stroke"
    "reference-touch/ungradedtrace/recallAgain/articles/SystemBack/offline.117scopedHan across4"
    "productionfamilies in five bounded panels plus focused奠/亅/厂/艹+lookalikes panel; six"
    "wholewordrasters per family. Cmapabsence NOTglyphfailure; hashes NOTreadability/fallbackface. "
    "Then two SERIAL different-family original-session visual confirmations where possible. "
    "Fresh499HOST3+1 retained; no redundant rerun. Preserve originalClaude8multi-toolresponses/"
    "30overlappingstarts/false serial claim and later actuallyserial confirmation separately. "
    "No teaching changes/publication/076 this checkpoint. Later currentmainnormalmerge/revalidation/"
    "normalsigning/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets/ownerissue60receipt "
    "remain. No unreviewedpush/signingretry/permissionworkaround/authoragents/secondrunner. "
    "Preserve FULLlivehistory, source recipes, originalreports/faileddiagnostics and reviewedbaseline"
    "虎/猿/丘/山exceptions. Published101/1228,remaining1127; necessarysupportsNOTN1vocabulary. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
    "Overall project incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".execution500.tmp")
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
    assert (p["checkpoint"], p["status"], p["batch"]) == (499, "continue", "075")
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    unchanged()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert embedded["checkpoint"] == 499
    assert not (L / "execution-500-before-progress.json").exists()
    save(L / "execution-500-before-progress.json", p)
    p["execution500StartingState"] = {
        "execution": 500, "batch": "075", "startingHead": HEAD, "androidHead": ANDROID,
        "scope": "SAME075 bounded full signed Git archive native fixture preparation/compilation and normally signed local evidence checkpoint only; no device/reviewer/publication/076/second runner.",
        "status": "native-preparation-in-progress", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and embedded checkpoint parsed before implementation; operative contract, final499 checkpoint and complete approved issue inspected directly. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
    }
    p["stage"] = "batch-075-native-preparation-in-progress"
    save(C / "progress.json", p)
    print("SAME075 preparation scope saved; complete live history retained.")


def prepare():
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    unchanged()
    assert not V.exists() and not ARCHIVE.exists() and not APK.exists()
    m = load(R / "manifest.json")
    counts = {
        "kanji": sum(n.startswith("kanji/") for n in m["files"]),
        "words": sum(n.startswith("words/") for n in m["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (R / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1087, "words": 5044, "n1": 107}
    assert m["contentVersion"] == "2759d7b13c89eb8f"
    ledger = load(S / "batch-075-progress.json")
    audit = load(S / "batch-075-draft-audit.json")
    helper = R / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    selected = ast.Module(body=[n for n in parsed.body if isinstance(n, ast.FunctionDef)
                               and n.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(selected, str(helper), "exec"), namespace)
    names = audit["actualAuthoredHanFonts"]["articles"] + ["kanji/型.md"]
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

    def display(document, slug, complete=False, component=False):
        projected = documents[document]
        line(f"await({quote(projected[0][1])})")
        section_name, table_cell = None, 0
        for index, (kind, value) in enumerate(projected[1:], 1):
            if kind == "heading":
                section_name = value
                if complete or (component and value == "How the kanji combine"):
                    line(f"section({quote(value)})")
                continue
            if not complete and not (component and section_name == "How the kanji combine"):
                continue
            if kind == "table":
                table_cell += 1
                if table_cell <= 3 or table_cell % 3 == 2:
                    continue
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
        chosen = next((v for v in candidates if v[0] == preferred), candidates[0])
        section_name, raw = chosen
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        text = namespace["plain"](" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_500" + raw[link.end():]
        offset = namespace["plain"](" ".join(marked.splitlines())).index("N1_LINK_TARGET_500")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("典")')
    line('click("reference texts; rules; ceremony")')
    display("kanji/典.md", "kanji", complete=True)
    for word in ("典型", "古典", "百科事典", "辞典", "香典"):
        document = f"words/{word}.md"
        forward = follow("kanji/典.md", word, document, word + "-forward")
        display(document, word, complete=word == "香典", component=word != "香典")
        reverse = follow(document, "典", "kanji/典.md", word + "-reverse")
        line('section("Readings")')
        line(f'show(readingExample("デン"), {quote(word + "-kanji-backlink")})')
        back_to(reverse, word + "-system-back-to-word")
        for char, mapped_word in ledger["allMappedReciprocalPairs"]:
            if mapped_word != document or char == "典":
                continue
            component = follow(document, char, f"kanji/{char}.md", word + "-" + char)
            counterpart = follow(f"kanji/{char}.md", word, document, char + "-counterpart")
            line('section("How the kanji combine")')
            line(f"show(articleBullet({quote(component['renderedText'])}), {quote(word + '-' + char + '-component-backlink')})")
            back_to(counterpart, word + "-" + char + "-system-back-to-component")
            back_to(component, word + "-" + char + "-system-back-from-component")
        back_to(forward, word + "-system-back-to-kanji")
    assert len(offsets) == 24
    assert {(i["document"], i["destination"]) for i in offsets} == {
        (i["from"], i["to"]) for i in ledger["directedLinks"]
    }

    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("074", "075"), ("exemptionLookalikesAndIsolatedRadicalAcrossFourProductionFamilies",
                        "referenceTextsLookalikesAndFourFallbacksAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineExemptionFiveReciprocalPairsBothReadingsDrawingAndSystemBack",
         "fullSingleImportOfflineReferenceTextsTwelveReciprocalPairsTwoOnReadingsDrawingAndSystemBack"),
        ("4078c7d42e6bc2173c555e73d0bd39fb5d69eb08", HEAD), ("4078c7d4", HEAD[:8]),
        ("c507eceeb764bc3f", m["contentVersion"]), ("1086", "1087"), ("5043", "5044"),
        ("106, n1.size", "107, n1.size"), ("N1 · 106 cards", "N1 · 107 cards"),
        ("exemption", "referenceTexts"), ("免", "典"),
        ("exempt; be spared", "reference texts; rules; ceremony"),
        ('listOf("メン")', 'listOf("テン", "デン")'),
        ('listOf("まぬか.れる", "まぬが.れる")', 'listOf("ふみ", "のり")'),
        ('listOf("まぬが.れる")', 'emptyList<String>()'),
        ('listOf("めん")', 'listOf("てん", "でん")'),
        ('listOf("まぬがれる")', 'emptyList<String>()'),
        ('((kind == ReadingKind.On && key == "めん") || (kind == ReadingKind.Kun && key == "まぬがれる"))',
         '(kind == ReadingKind.On && key in setOf("てん", "でん"))'),
        ("典 meaning and curated on and kun due; valid alternate まぬか.れる retained but not offered.",
         "典 meaning and two curated on keys due; raw source-only ふみ/のり retained but no kun keys."),
        ("bothCuratedKindsPersistedGoodNoAlternateAndDone", "bothCuratedOnKeysPersistedGoodNoKunAndDone"),
        ('.put("mappedReciprocalPairs", 5).put("directedLinkTransitions", 10)',
         '.put("mappedReciprocalPairs", 12).put("directedLinkTransitions", 24)'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    begin = text.index("            val answeredKinds =")
    end = text.index("            rule.waitUntil(30_000) { (model(\"kreading:\") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }", begin)
    text = text[:begin] + '''            val answeredKeys = mutableSetOf<String>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("典", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue("Unexpected offered key $key", key in setOf("てん", "でん"))
                assertTrue("Duplicate target key $key", answeredKeys.add(key))
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-$key-question")
                click(question.question.options.single { it.key == key }.label)
                await("Correct! — on'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-$key-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "典" &&
                        log.mode == ReadingKind.On.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("てん", "でん"), answeredKeys)
''' + text[end:]
    text = text.replace('it.mode == ReadingKind.Kun.mode.name && it.reading == "まぬかれる"',
                        "it.mode == ReadingKind.Kun.mode.name")
    text = text.replace('capture("curated-both-done")', 'capture("curated-two-on-done")')
    glyphs = audit["actualAuthoredHanFonts"]["characters"]
    assert len(glyphs) == 117 and {"典", "奠", "亅", "厂", "艹", "具", "曲", "共"} <= set(glyphs)
    words = ["典型", "古典", "百科事典", "辞典", "香典", "香奠"]
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("典 具 曲 共 奠 亅 厂 艹 八 " + " ".join(words))
    text = text.replace("import androidx.core.content.res.ResourcesCompat",
                        "import androidx.core.content.res.ResourcesCompat\nimport androidx.compose.runtime.mutableStateOf")
    begin = text.index("        val text =")
    end = text.index("        val typefaces =", begin)
    text = text[:begin] + f'''        val pages = listOf({", ".join(quote(p) for p in pages)})
        val page = mutableStateOf(0)
        rule.setContent {{
            MaterialTheme {{
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {{
                    Text("Batch 075: reference texts / look-alikes / fallback")
                    Text("Panel ${{page.value + 1}} / ${{pages.size}}")
                    fonts.forEach {{ font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }}
                    Text("Inspect all 117 scoped Han; focused 奠/亅/厂/艹 and 典/具/曲/共. Fallback families may coincide.", fontSize = 16.sp)
                }}
            }}
        }}
''' + text[end:]
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
                  "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)',
                  "for (word in listOf(" + ", ".join(quote(w) for w in words) + "))", text, count=1)
    text = text.replace("assertEquals(184, rows.length())", "assertEquals(492, rows.length())")
    begin = text.index('        rule.waitForIdle()\n        rule.onAllNodesWithText(text)')
    end = text.index('        File(context.getExternalFilesDir(null), "n1-075-font-raster.json")', begin)
    text = text[:begin] + '''        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-075-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
''' + text[end:]
    text = text.replace('.put("individualGlyphProbes", 172).put("wholeWordRasterProbes", 12)',
                        '.put("individualGlyphProbes", 468).put("wholeWordRasterProbes", 24).put("panels", 6)')
    text = re.sub(r'\.put\("limits", "Native Paint probes[^"]+"\)',
                  '.put("limits", "117 scoped authored Han including 奠/亅/厂/艹, four production families, six bounded Compose panels and 24 whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")', text)
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("074", "免", "まぬ", "メン", "めん", "exemption", "answeredKinds", "免税", "儿"):
        assert stale not in text, stale
    for item in selectors:
        assert quote(item["target"]) in text
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-075/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.namelist()
        prefix = "n1-batch-075/"
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
    assert verified == 8352
    V.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = V / "fixture-from-074-attempt-3.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(PRIOR), tofile=str(FIXTURE.relative_to(R)), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 500, "batch": "075", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED, "androidSnapshot": ANDROID,
        "contentVersion": m["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": str(PRIOR), "priorHarnessSha256": sha(PRIOR),
        "staticProjectionHelper": str(helper.relative_to(R)), "staticProjectionHelperSha256": sha(helper),
        "fixtureDiff": str(diff.relative_to(R)), "fixtureDiffSha256": sha(diff),
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(b)}
                         for n, b in documents.items()],
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 2, "changedReusedPassages": 10,
        "unchangedMappedArticle": "kanji/型.md: mapped reciprocal link only",
        "mappedReciprocalPairs": 12, "mappedDirectedTransitions": 24,
        "plannedNativePaintProbes": 468, "plannedWholeWordRasterProbes": 24,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "fullReadings": {"on": ["テン", "デン"], "kun": ["ふみ", "のり"]},
        "curatedReadings": {"on": ["テン", "デン"], "kun": []},
        "normalizedQuizKeys": {"on": ["てん", "でん"], "kun": []},
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": LIMITS, "nextAction": NEXT,
    }
    save(C / "batch-075-native-fixture-verification.json", record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries",
                     "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print("Static selectors:", len(selectors), "; directed links:", len(offsets))


def archive():
    unchanged()
    preparation = load(C / "batch-075-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    ledger = load(S / "batch-075-progress.json")
    assert {(i["from"], i["to"]) for i in ledger["directedLinks"]} == {
        (i["document"], i["destination"]) for i in preparation["staticLinkedOffsets"]
    }
    authored_files = load(S / "batch-075-draft-audit.json")["actualAuthoredHanFonts"]["articles"]
    actual_han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                                      "".join((R / n).read_text(encoding="utf-8") for n in authored_files))))
    assert actual_han == preparation["plannedGlyphs"]
    raw_log = L / "native-compile.txt"
    text = raw_log.read_text(encoding="utf-8-sig")
    assert (L / "native-compile-exit.txt").read_text().strip() == "0" and "BUILD SUCCESSFUL" in text
    methods = ("referenceTextsLookalikesAndFourFallbacksAcrossFourProductionFamilies",
               "fullSingleImportOfflineReferenceTextsTwelveReciprocalPairsTwoOnReadingsDrawingAndSystemBack")
    with zipfile.ZipFile(APK) as z:
        assert hashlib.sha256(z.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [z.read(n) for n in z.namelist() if re.fullmatch(r"classes\d*\.dex", n)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch075{kind}Test;".encode() in b for b in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch074{kind}Test;".encode() not in b for b in dex)
        for method in methods:
            assert any(method.encode() in b for b in dex), method
    (V / "compile.txt").write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")
    (V / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    receipts = V / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-500.py")
    shutil.copyfile(C / "run-500-native-compile.ps1", receipts / "run-500-native-compile.ps1")
    save(S / "batch-075-native-preparation.json", preparation)
    inherited = load(S / "execution-499.json")
    for item in inherited["tests"]:
        assert sha(R / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 2759d7b13c89eb8f")):
        source = L / f"{name}-500.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = V / f"{name}.txt"
        target.write_text("\n".join(line.rstrip() for line in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(R)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 500, "batch": "075", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(C / "progress.json")["execution500StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-075-native-preparation.json",
        "preparationSha256": sha(S / "batch-075-native-preparation.json"),
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
            "old074DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "staticSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 2, "changedReusedPassages": 10,
            "readingLabelsAndExplanations": 4, "mappedReciprocalPairs": 12, "mappedDirectedTransitions": 24,
            "staticOnlyNotActualVisualCoverage": True, "exactLedgerDirectedLinksAndPairsVerified": True,
            "completeActualAuthoredHanReinventoried": True,
        },
        "accepted499AndroidRetainedWithoutRerun": True, "inheritedArchivedXmlHashesReverified": True,
        "textualReconciliationSha256": sha(R / "docs" / "n1-reviews" / "batch-075-reconciliation.json"),
        "originalClaudeConcurrencyBreachPreserved": True,
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 101, "remainingAdditions": 1127, "nextAction": NEXT, "limits": LIMITS,
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(R)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(V.rglob("*")) + [S / "batch-075-native-preparation.json"] if path.is_file()
    ]
    save(S / "execution-500.json", record)
    print("Exact packaged archive, both cases, inherited Android XML and cleanup verified.")


def checkpoint():
    unchanged()
    record = load(S / "execution-500.json")
    for item in record["artifacts"]:
        path = R / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    p = load(C / "progress.json")
    before = load(L / "execution-500-before-progress.json")
    assert all(p[k] == value for k, value in before.items() if k != "stage")
    assert set(p) == set(before) | {"execution500StartingState"}
    receipt = {
        "execution": 500, "checkpoint": 500, "batch": "075", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-500.json",
        "recordSha256": sha(S / "execution-500.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=500, status="continue", stage="batch-075-native-compiled-pending-execution",
             nextAction=NEXT, blocker=None)
    p["execution500StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    p["batch075NativePreparationCheckpoint"] = receipt
    p["execution500CoordinatorCheckpoint"] = receipt
    p["activeExecution"] = receipt
    save(C / "progress.json", p)
    save(L / "checkpoint-500.json", receipt)
    (L / "issue-500-body.txt").write_text(
        f"Batch 075 native-preparation checkpoint **500** saved locally at `{receipt['savedCommit']}` "
        "(normal signature G); no runtime publication.\n\n"
        "The exact full signed `fba1a886` Git archive (version `2759d7b13c89eb8f`, 1,087 kanji / "
        "5,044 words / 107 N1 cards) preserves all 8,352 runtime hashes and original publishing budgets. "
        "Both named cases and exact archive verified inside the serially compiled APK; temporary Android "
        "source/assets removed and dedicated worktree clean. No HOST heap init, guest/app heap or guard "
        "change. Teaching/manifest unchanged; fresh499 HOST3+1 retained without rerun.\n\n"
        "Static selectors prepare complete 典/香典, four reused component paragraphs, six changed older "
        "kanji navigation passages, and all 12 mapped reciprocal pairs/24 directions (unchanged 型 included). "
        "Full/Lite preserve raw テン/デン and ふみ/のり in source order; curated テン/デン plus empty kun, "
        "both actual てん/でん answers persisted Good/Done2correct and no kun log are asserted. Eight-stroke "
        "reference-touch trace/recall, 117 actual scoped Han across four production families, six bounded "
        "Compose panels including focused 奠/亅/厂/艹 and 典/具/曲/共, and 24 whole-word rasters are "
        "prepared, **not executed**. Cmap absence is not glyph failure; hashes/static selectors are not "
        "readability, fallback-face or phone evidence. Original Claude initial concurrency/false serial "
        "claim remains disclosed; later serial confirmation does not rewrite it.\n\n"
        "Next: fresh device/5580/5581 ownership inspection; owned read-only API35 helper; both terminal "
        "native statuses 0/no skips and actual PNG inspection, then two serial different-family visual "
        "confirmations. Current-main integration/validation/signing/owner fast-forward/CI/immutable public "
        "ZIP gates remain. **101/1,228 additions published; 1,127 remain.** Necessary supports are not an "
        "N1 vocabulary deck. Compatible Android `f9b59a2`+ required; physical-phone/general-release/whole-set "
        "acceptance outstanding. Status `continue`; batch076 not started.",
        encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("checkpoint", "savedCommit", "status", "nativeExecuted")}, indent=2))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "archive": archive, "checkpoint": checkpoint}[sys.argv[1]]()
