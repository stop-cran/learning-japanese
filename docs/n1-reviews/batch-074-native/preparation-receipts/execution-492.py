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
L = C / "logs" / "cb9dd289-9629-4ee7-a229-14ac174ee87b"
V = R / "docs" / "n1-reviews" / "batch-074-native"
S = R / "docs" / "n1-sources"
HEAD = "4078c7d42e6bc2173c555e73d0bd39fb5d69eb08"
REVIEWED = "75fbfc7dc734c7ff5d9771fbd5103afd3f3fdc1c"
ANDROID = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PRIOR = R / "docs" / "n1-reviews" / "batch-073-native" / "N1Batch073NativeTest.kt"
FIXTURE = V / "N1Batch074NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-074-4078c7d4-envelope.zip"
APK = C / "artifacts" / "n1-batch-074-native-test.apk"
LIMITS = (
    "Fixture preparation and compilation only, not native execution or visual acceptance. "
    "Complete projected new kanji/word and changed reused component passages plus the new 許 common-word "
    "example; unchanged 税 visited only for its mapped reciprocal link. Static offsets/selectors do not "
    "prove every character is visible. Raster hashes do not identify fallback faces or establish readability. "
    "Reference-touch trace is not human handwriting/MLKit evidence. Emulator is not physical-phone evidence. "
    "No HOST heap init, guest/app heap changes, relaxed guards, teaching changes or publication."
)
NEXT = (
    "SAME074 execute compiled control\\artifacts\\n1-batch-074-native-test.apk, "
    "N1Batch074GlyphTest and N1Batch074ArticleTest, exact signed4078c7d4 full Git archive. "
    "Read docs\\n1-sources\\execution-492.json and batch-074-native-preparation.json. "
    "Fresh adb/device and5580/5581 local/remote connection/PID ownership immediately before read-only "
    "N3_Acceptance_20261029 emulator-5580 launch with established hostGPU/Vulkan-disabled2048MiB/two-core "
    "flags. Record actual owned parent/QEMU; stop only owned helper. Batch040 override NOT inherited; "
    "HOST-only2GiB init NEVER for native. Full production ContentSync ONCE must import1086kanji5043words"
    "106N1/versionc507eceeb764bc3f/problems0/epoch1. Full+Lite rawメン/まぬか.れる/まぬが.れる "
    "source order, curatedメン/まぬが.れる, normalizedめん/まぬがれる; both actual offered kinds "
    "persistGood/Done2correct, no excludedまぬかれる key/log. Both pronunciations valid, no rarity claim. "
    "Complete new免/免れる projection, reused免許N3/免税N2 component passages and許 example; "
    "all5reciprocalpairs10directions/SystemBack/offline/N1selection/meaning/eightreference-touchstrokes/"
    "ungradedtrace/recallAgain. All43actual authoredHan including isolated儿 across4productionfamilies "
    "and3whole-wordrasters; require terminal0 for BOTH cases, zero skips and actualPNGinspection. "
    "Static selectors/rasterhashes are not fullviewport readability/fallback-face/phone evidence. "
    "Fresh491HOST3+1 inherited; do not rerun absentnewconcern. Then original "
    "Claudeaf76d4d5-df98-409c-a302-d8d9fd63f45d THEN GPTc7f3d66f-c4ff-479b-82cb-957c2f7913ec "
    "SERIAL dependent visual confirmations; original Claude initial ONE concurrent兄/元 read remains "
    "disclosed. No publication before native/font/currentmainmerge/revalidation/normalsigning/"
    "ownerfastforward/greenCI/EVERYimmutablepublicZIPruntimehash/originalbudgets/ownerissue60receipt. "
    "No signingretry/permissionworkaround/unreviewedpush/075/secondrunner. Preserve FULLlivehistory/"
    "originalsource recipe/baselineexceptions/fullreadingorder/historicalfailures/limits. "
    "Published100/1228,remaining1128;100necessarypublishedsupports NOTN1vocabulary. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".execution492.tmp")
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
    assert p["checkpoint"] == 491 and p["status"] == "continue" and p["batch"] == "074"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    unchanged()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert embedded["checkpoint"] == 491
    assert not (L / "execution-492-before-progress.json").exists()
    save(L / "execution-492-before-progress.json", p)
    p["execution492StartingState"] = {
        "execution": 492, "batch": "074", "startingHead": HEAD, "androidHead": ANDROID,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME074 bounded full signed Git archive native fixture preparation/compilation and normally signed local evidence checkpoint only; no native/reviewer/publication/075/second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, entire approved issue and final491 inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
    }
    p["stage"] = "batch-074-native-preparation-in-progress"
    save(C / "progress.json", p)
    print("SAME074 preparation scope saved; complete live history retained.")


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
    assert counts == {"kanji": 1086, "words": 5043, "n1": 106}
    assert m["contentVersion"] == "c507eceeb764bc3f"
    helper = R / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    selected = ast.Module(body=[n for n in parsed.body if isinstance(n, ast.FunctionDef)
                               and n.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(selected, str(helper), "exec"), namespace)
    names = ("kanji/免.md", "words/免れる.md", "words/免許.md", "words/免税.md", "kanji/許.md", "kanji/税.md")
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

    def display(document, slug, scope):
        projected = documents[document]
        line(f"await({quote(projected[0][1])})")
        section_name, table_cell = None, 0
        for index, (kind, value) in enumerate(projected[1:], 1):
            if kind == "heading":
                section_name = value
                if scope == "complete" or (scope == "component" and value == "How the kanji combine"):
                    line(f"section({quote(value)})")
                continue
            if scope == "component" and section_name != "How the kanji combine":
                continue
            if scope == "license-example":
                if section_name != "Common words" or not value.startswith("免許 "):
                    continue
                line('section("Common words")')
            if kind == "table":
                table_cell += 1
                if table_cell <= 3 or table_cell % 3 == 2:
                    continue
            show(document, index, kind, value, slug)

    def follow(document, label, destination, section_name):
        body = (R / document).read_text(encoding="utf-8")
        section_body = body.split("## " + section_name + "\n", 1)[1].split("\n## ", 1)[0]
        parts = re.split(r"\n\s*\n|\n(?=- )", section_body.strip())
        raw = next(part.removeprefix("- ") for part in parts if f"[{label}](" in part)
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        assert (R / document).parent.joinpath(link[1]).resolve() == (R / destination).resolve()
        text = namespace["plain"](" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_492" + raw[link.end():]
        offset = namespace["plain"](" ".join(marked.splitlines())).index("N1_LINK_TARGET_492")
        assert text[offset:].startswith(label)
        line(f"section({quote(section_name)})")
        line(f"inline(await(articleBullet({quote(text)})), {quote(label)}, {offset})")
        line('await("Article contents")')
        item = {"document": document, "destination": destination, "label": label,
                "renderedText": text, "offset": offset}
        offsets.append(item)
        return item

    def back_to(item, section_name, step):
        line("back()")
        line(f"await(articleBullet({quote(item['renderedText'])})).assertIsDisplayed()")
        line(f"section({quote(section_name)})")
        line(f"capture({quote(step)})")

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("免")')
    line('click("exempt; be spared")')
    display("kanji/免.md", "kanji", "complete")
    for word, extra in (("免れる", None), ("免許", "許"), ("免税", "税")):
        document = f"words/{word}.md"
        forward = follow("kanji/免.md", word, document, "Common words")
        display(document, word, "complete" if word == "免れる" else "component")
        reverse = follow(document, "免", "kanji/免.md", "How the kanji combine")
        line('section("Readings")')
        line(f'show(readingExample("まぬが.れる"), {quote(word + "-kanji-backlink")})')
        back_to(reverse, "How the kanji combine", word + "-system-back-to-word")
        if extra:
            component = follow(document, extra, f"kanji/{extra}.md", "How the kanji combine")
            if extra == "許":
                display("kanji/許.md", "permit-example", "license-example")
            counterpart = follow(f"kanji/{extra}.md", word, document, "Common words")
            line('section("How the kanji combine")')
            line(f"show(articleBullet({quote(reverse['renderedText'])}), {quote(word + '-component-backlink')})")
            back_to(counterpart, "Common words", word + "-system-back-to-component")
            back_to(component, "How the kanji combine", word + "-system-back-from-component")
        back_to(forward, "Common words", word + "-system-back-to-kanji")

    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("073", "074"),
        ("overcomeLookalikesAndIsolatedRadicalAcrossFourProductionFamilies",
         "exemptionLookalikesAndIsolatedRadicalAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineOvercomeTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
         "fullSingleImportOfflineExemptionFiveReciprocalPairsBothReadingsDrawingAndSystemBack"),
        ("5d322346c0c8bccdc36769d85f3fb23f4b5cbbee", HEAD), ("5d322346", HEAD[:8]),
        ("1d8a4ee1a97c6bb5", m["contentVersion"]), ("1085", "1086"), ("5042", "5043"),
        ("105, n1.size", "106, n1.size"), ("N1 · 105 cards", "N1 · 106 cards"),
        ("overcome", "exemption"), ("克", "免"),
        ('"exemption"', '"exempt; be spared"'),
        ("コク", "メン"), ("こく", "めん"),
        ('listOf("か.つ")', 'listOf("まぬか.れる", "まぬが.れる")'),
        ('emptyList<String>(), exemption.quizKunyomi?.splitSep()', 'listOf("まぬが.れる"), exemption.quizKunyomi?.splitSep()'),
        ('emptyList<String>(), card.quizKunyomi?.splitSep()', 'listOf("まぬが.れる"), card.quizKunyomi?.splitSep()'),
        ('emptyList<String>(), exemption.toReadingCard().quizKeys(ReadingKind.Kun)', 'listOf("まぬがれる"), exemption.toReadingCard().quizKeys(ReadingKind.Kun)'),
        ('(kind == ReadingKind.On && key == "めん")',
         '((kind == ReadingKind.On && key == "めん") || (kind == ReadingKind.Kun && key == "まぬがれる"))'),
        ("repeat(1) {", "repeat(2) {"),
        ('assertEquals(ReadingKind.On, question.question.kind)\n                val key = "めん"',
         'val key = if (question.question.kind == ReadingKind.On) "めん" else "まぬがれる"\n                assertNotEquals("まぬかれる", question.question.correctKey)'),
        ("setOf(ReadingKind.On), answeredKinds", "setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds"),
        ("1, done.answered", "2, done.answered"), ("1, done.correct", "2, done.correct"),
        ('it.mode == ReadingKind.Kun.mode.name }\n            })\n            capture("curated-on-only-done")',
         'it.mode == ReadingKind.Kun.mode.name && it.reading == "まぬかれる" }\n            })\n            capture("curated-both-done")'),
        ('"soleCuratedOnPersistedGoodNoKunAndDone"', '"bothCuratedKindsPersistedGoodNoAlternateAndDone"'),
        ("sole curated on key due; raw か.つ retained but explicit empty quiz kun",
         "curated on and kun due; valid alternate まぬか.れる retained but not offered"),
        ("7, strokes.length()", "8, strokes.length()"), ("7 strokes drawn", "8 strokes drawn"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    glyphs = load(S / "batch-074-draft-audit.json")["actualAuthoredHanFonts"]["characters"]
    assert len(glyphs) == 43 and {"免", "先", "兄", "元", "儿", "税", "許"} <= set(glyphs)
    words = ["免れる", "免許", "免税"]
    text = re.sub(r'val text = "[^"]+"', "val text = " + quote(" ".join(glyphs + words)), text, count=1)
    text = re.sub(r'Text\("Batch 074:[^"]+"\)',
                  'Text("Batch 074: exemption / look-alikes / isolated radical")', text)
    text = re.sub(r'Text\("Inspect [^\n]+fontSize = 18.sp\)',
                  'Text("Inspect 免/兄/元/先, isolated 儿 and 許/税; all authored Han, 免れる/免許/免税. Fallback families may coincide.", fontSize = 18.sp)', text)
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
                  "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)',
                  "for (word in listOf(" + ", ".join(quote(w) for w in words) + "))", text, count=1)
    text = text.replace("assertEquals(112, rows.length())", "assertEquals(184, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 108).put("wholeWordRasterProbes", 4)',
                        '.put("individualGlyphProbes", 172).put("wholeWordRasterProbes", 12)')
    text = re.sub(r'\.put\("limits", "Native Paint probes[^"]+"\)',
                  '.put("limits", "Native Paint probes cover all43 actual authored Han including isolated 儿; twelve whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")', text)
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    text = text.replace('evidence.put("reciprocalLinkAndSystemBack", true)',
                        'evidence.put("reciprocalLinkAndSystemBack", true)\n'
                        '                .put("mappedReciprocalPairs", 5).put("directedLinkTransitions", 10)')
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("073", "克", "か.つ", "こく", "コク", "overcome", "OnOnly", "7 strokes", "NoKun"):
        assert stale not in text, stale
    assert len(offsets) == 10 and len({(i["document"], i["destination"]) for i in offsets}) == 10
    assert sum(i["document"] == "kanji/許.md" for i in selectors) == 1
    for item in selectors:
        assert quote(item["target"]) in text
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-074/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.namelist()
        prefix = "n1-batch-074/"
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
    assert verified == 8349
    V.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = V / "fixture-from-073.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(PRIOR.relative_to(R)), tofile=str(FIXTURE.relative_to(R)), n=0)), encoding="utf-8")
    scopes = dict(zip(names, ("complete projection", "complete projection",
                             "changed component paragraph", "changed component paragraph",
                             "new common-word example", "unchanged reciprocal link only")))
    record = {
        "schemaVersion": 1, "execution": 492, "batch": "074", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED, "androidSnapshot": ANDROID,
        "contentVersion": m["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": str(PRIOR.relative_to(R)), "priorHarnessSha256": sha(PRIOR),
        "staticProjectionHelper": str(helper.relative_to(R)), "staticProjectionHelperSha256": sha(helper),
        "fixtureDiff": str(diff.relative_to(R)), "fixtureDiffSha256": sha(diff),
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(b), "scope": scopes[n]}
                         for n, b in documents.items()],
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 2, "changedReusedPassages": 3,
        "mappedReciprocalPairs": 5, "mappedDirectedTransitions": 10,
        "plannedNativePaintProbes": 172, "plannedWholeWordRasterProbes": 12,
        "plannedGlyphs": glyphs, "plannedWholeWords": words,
        "fullReadings": {"on": ["メン"], "kun": ["まぬか.れる", "まぬが.れる"]},
        "curatedReadings": {"on": ["メン"], "kun": ["まぬが.れる"]},
        "normalizedQuizKeys": {"on": ["めん"], "kun": ["まぬがれる"]},
        "excludedValidAlternateKey": "まぬかれる",
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": LIMITS, "nextAction": NEXT,
    }
    save(C / "batch-074-native-fixture-verification.json", record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries",
                     "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print("Unique article selectors:", len(selectors), "; directed links:", len(offsets))


def archive():
    unchanged()
    preparation = load(C / "batch-074-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    ledger = load(S / "batch-074-progress.json")
    expected_links = {(item["from"], item["to"]) for item in ledger["directedLinks"]}
    actual_links = {(item["document"], item["destination"]) for item in preparation["staticLinkedOffsets"]}
    assert expected_links == actual_links and len(actual_links) == 10
    expected_pairs = {(f"kanji/{char}.md", word) for char, word in ledger["allMappedReciprocalPairs"]}
    assert expected_pairs == {(a, b) for a, b in actual_links if a.startswith("kanji/")}
    authored_files = ("kanji/免.md", "words/免れる.md", "words/免許.md", "words/免税.md", "kanji/許.md")
    actual_han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                                      "".join((R / n).read_text(encoding="utf-8") for n in authored_files))))
    assert actual_han == preparation["plannedGlyphs"]
    raw_log = L / "native-compile.txt"
    text = raw_log.read_text(encoding="utf-8-sig")
    assert (L / "native-compile-exit.txt").read_text().strip() == "0" and "BUILD SUCCESSFUL" in text
    methods = ("exemptionLookalikesAndIsolatedRadicalAcrossFourProductionFamilies",
               "fullSingleImportOfflineExemptionFiveReciprocalPairsBothReadingsDrawingAndSystemBack")
    with zipfile.ZipFile(APK) as z:
        assert hashlib.sha256(z.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [z.read(n) for n in z.namelist() if re.fullmatch(r"classes\d*\.dex", n)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch074{kind}Test;".encode() in b for b in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch073{kind}Test;".encode() not in b for b in dex)
        for method in methods:
            assert any(method.encode() in b for b in dex), method
    (V / "compile.txt").write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")
    (V / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    receipts = V / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-492.py")
    shutil.copyfile(C / "run-492-native-compile.ps1", receipts / "run-492-native-compile.ps1")
    save(S / "batch-074-native-preparation.json", preparation)
    inherited = load(S / "execution-491.json")
    for item in inherited["tests"]:
        assert sha(R / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version c507eceeb764bc3f")):
        source = L / f"{name}.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = V / f"{name}.txt"
        target.write_text("\n".join(line.rstrip() for line in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(R)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 492, "batch": "074", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(C / "progress.json")["execution492StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-074-native-preparation.json",
        "preparationSha256": sha(S / "batch-074-native-preparation.json"),
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
            "old073DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "uniqueSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 2, "changedReusedPassages": 3,
            "readingLabelsAndExplanations": 3, "mappedReciprocalPairs": 5, "mappedDirectedTransitions": 10,
            "staticOnlyNotActualVisualCoverage": True,
            "exactLedgerDirectedLinksAndPairsVerified": True,
            "completeActualAuthoredHanReinventoried": True,
        },
        "accepted491AndroidRetainedWithoutRerun": True, "inheritedArchivedXmlHashesReverified": True,
        "textualReconciliationSha256": sha(R / "docs" / "n1-reviews" / "batch-074-reconciliation.json"),
        "originalClaudeSingleConcurrentSmallReadPreserved": True,
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 100, "remainingAdditions": 1128, "nextAction": NEXT, "limits": LIMITS,
        "resolvedPreparationDiagnostic": "One read-only console mapping probe used Windows cp1252 implicitly and failed Unicode decoding. Repeated with explicit UTF8 succeeded; original tool diagnostic retained. No source/fixture change, lost work or permission bypass.",
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(R)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(V.rglob("*")) + [S / "batch-074-native-preparation.json"] if path.is_file()
    ]
    save(S / "execution-492.json", record)
    print("Exact packaged archive, both cases, inherited Android XML and cleanup verified.")


def checkpoint():
    unchanged()
    record = load(S / "execution-492.json")
    for item in record["artifacts"]:
        path = R / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    p = load(C / "progress.json")
    before = load(L / "execution-492-before-progress.json")
    assert all(p[k] == value for k, value in before.items() if k != "stage")
    assert set(p) == set(before) | {"execution492StartingState"}
    receipt = {
        "execution": 492, "checkpoint": 492, "batch": "074", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-492.json",
        "recordSha256": sha(S / "execution-492.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=492, status="continue", stage="batch-074-native-compiled-pending-execution",
             nextAction=NEXT, blocker=None)
    p["execution492StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    p["batch074NativePreparationCheckpoint"] = receipt
    p["execution492CoordinatorCheckpoint"] = receipt
    p["activeExecution"] = receipt
    save(C / "progress.json", p)
    save(L / "checkpoint-492.json", receipt)
    (L / "issue-body.txt").write_text(
        f"Batch 074 native-preparation checkpoint **492** saved locally at `{receipt['savedCommit']}` "
        "(normal signature G); no runtime publication.\n\n"
        "Exact full signed `4078c7d4` Git archive (version `c507eceeb764bc3f`, 1,086 kanji / "
        "5,043 words / 106 N1 cards) preserves all 8,349 runtime hashes and original publishing budgets. "
        "Both named cases and the exact archive are verified inside the serially compiled APK; temporary "
        "Android source/assets removed and dedicated worktree clean. No HOST heap init, guest/app heap "
        "or guard change. Teaching/manifest unchanged.\n\n"
        "Static selectors prepare complete new 免 / 免れる projections, all three raw reading rows, "
        "the valid alternate まぬかれる, reused 免許/免税 component passages and the 許 common-word example. "
        "Five reciprocal pairs/ten directed transitions include the unchanged 税 link. Full/Lite retain "
        "メン / まぬか.れる / まぬが.れる in source order; both curated メン / まぬが.れる keys, "
        "persisted Good/Done2correct and no alternate-key log are asserted. Eight-stroke reference-touch "
        "trace/recall, 43 actual authored Han including isolated 儿 across four production families, and "
        "three whole-word rasters per family are prepared, not executed. Native/visual readability, "
        "fallback-face identity and phone acceptance are not claimed. Fresh491 Android3+1 retained "
        "without redundant HOST Gradle. Original Claude initial single concurrent small-file read remains disclosed.\n\n"
        "Next: fresh device/5580/5581 ownership check, owned read-only API35 helper, both terminal native "
        "case statuses 0/no skips and actual PNG inspection; then original Claude/GPT serial dependent "
        "visual confirmations. Current-main validation/signing/owner fast-forward/CI/immutable public ZIP "
        "gates remain. **100/1,228 additions published; 1,128 remain; 100 published necessary supports "
        "are not N1 vocabulary.** Compatible Android `f9b59a2`+ required; physical-phone/general-release/"
        "whole-set acceptance outstanding. Checkpoint status `continue`; batch075 not started.",
        encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "archive": archive, "checkpoint": checkpoint}[sys.argv[1]]()
