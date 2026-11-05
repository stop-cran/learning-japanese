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
L = C / "logs" / "dd4c948a-ffde-4b61-907b-cc20b11ef6d3"
V = R / "docs" / "n1-reviews" / "batch-073-native"
S = R / "docs" / "n1-sources"
HEAD = "5d322346c0c8bccdc36769d85f3fb23f4b5cbbee"
REVIEWED = "c8c2a0ba7dfc794feac5362fcfefa41e8d33ee5a"
ANDROID = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
PRIOR = R / "docs" / "n1-reviews" / "batch-072-native" / "N1Batch072NativeTest.kt"
FIXTURE = V / "N1Batch073NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-073-5d322346-envelope.zip"
APK = C / "artifacts" / "n1-batch-073-native-test.apk"
NEXT = (
    "SAME073 execute compiled control\\artifacts\\n1-batch-073-native-test.apk "
    "N1Batch073GlyphTest and N1Batch073ArticleTest using exact signed5d322346 full Git archive. "
    "Read docs\\n1-sources\\execution-484.json and batch-073-native-preparation.json. "
    "Fresh adb/device and5580/5581 local/remote connection/PID ownership immediately before "
    "read-only N3_Acceptance_20261029 emulator-5580 launch with established host GPU/Vulkan-disabled "
    "2048MiB/two-core flags. Record actual owned parent/QEMU and stop only owned helper. "
    "Batch040 routing override NOT inherited; HOST heap init NEVER for native; no guest/app heap/guard changes. "
    "Require ContentSync ONCE:1085kanji5042words105N1/version1d8a4ee1a97c6bb5/problems0/epoch1; "
    "Full+Lite rawコク/か.つ, curatedコク/[] and normalizedこく/[]; no kun question/log; sole on persistedGood/Done1correct. "
    "Complete new克 projection including both reading labels/explanations, exact reused克服 component paragraph "
    "and服 sentence, two reciprocal pairs/four directions/SystemBack/offline/N1selection/meaning/"
    "seven reference-touch strokes/ungradedtrace/recallAgain. All27 actual authoredHan including isolated儿 "
    "across four production families, four whole-word rasters and actual PNG inspection; terminal0 for BOTH "
    "cases/no skips. Static selectors/raster hashes are not readability/fallback-face or phone evidence; "
    "reference trace is not human handwriting/MLKit. Fresh483 HOST Android3+1 inherited; do not rerun absent "
    "new concern. Then original Claude482a74cb-d8a4-47d5-8e7d-1451bbdfc13b THEN "
    "GPT427eb11f-e4a8-43eb-9677-eb03d1065cfe SERIAL dependent visual confirmations. "
    "No publication before native/font/current-main validation, normal signing, owner fast-forward, green CI, "
    "every immutable public ZIP runtime hash/original budgets and owner issue60 receipt. No074 or second runner. "
    "Published99/1228,remaining1129;100 published necessary supports are not N1 vocabulary. Compatible "
    "Androidf9b59a2+ required; physical-phone/general-release/whole-set acceptance remains outstanding."
)
LIMITS = (
    "Static native preparation/compilation only, not execution, readability, fallback-face identification, "
    "independent visual, physical-phone or publication acceptance. Complete new 克 projection and both "
    "reading labels/explanations; repeated table type labels not individually asserted. Exact changed "
    "reused 克服 component paragraph and 服 sentence only, not fresh full review of unchanged reused prose. "
    "Full signed Git archive through production ContentSync ONCE; no HOST heap init, guest/app heap or "
    "archive guard changes. Reference touch trace is not human handwriting/MLKit. No teaching edits."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".execution484.tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)
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
    assert p["checkpoint"] == 483 and p["status"] == "continue" and p["batch"] == "073"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    unchanged()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = load_request(request)
    assert embedded["checkpoint"] == 483
    assert not (L / "execution-484-before-progress.json").exists()
    save(L / "execution-484-before-progress.json", p)
    p["execution484StartingState"] = {
        "execution": 484, "batch": "073", "startingHead": HEAD, "androidHead": ANDROID,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME073 bounded exact full signed Git archive native fixture preparation/compilation and normally signed local evidence checkpoint only; no native/reviewer/publication/074/second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete approved issue and complete final483 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "freshlyFetchedOriginMain": git("rev-parse", "origin/main"),
    }
    p["stage"] = "batch-073-native-preparation-in-progress"
    save(C / "progress.json", p)
    print("SAME073 native-preparation scope persisted; complete live history retained.")


def load_request(text):
    return json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])


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
    assert counts == {"kanji": 1085, "words": 5042, "n1": 105}
    assert m["contentVersion"] == "1d8a4ee1a97c6bb5"
    helper = R / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    selected = ast.Module(body=[n for n in parsed.body if isinstance(n, ast.FunctionDef)
                               and n.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(selected, str(helper), "exec"), namespace)
    documents = {n: namespace["blocks"](R / n) for n in ("kanji/克.md", "words/克服.md", "kanji/服.md")}
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
                if scope == "complete" or value == "How the kanji combine":
                    line(f"section({quote(value)})")
                continue
            if scope == "component" and section_name != "How the kanji combine":
                continue
            if scope == "sentence":
                if 'In 克服 こくふく, "overcoming; surmounting,"' not in value:
                    continue
                line('section("Meaning and origin")')
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
        marked = raw[:link.start()] + "N1_LINK_TARGET_484" + raw[link.end():]
        offset = namespace["plain"](" ".join(marked.splitlines())).index("N1_LINK_TARGET_484")
        assert text[offset:].startswith(label)
        line(f"section({quote(section_name)})")
        line(f"inline(await(articleBullet({quote(text)})), {quote(label)}, {offset})")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("克")')
    line('click("overcome")')
    display("kanji/克.md", "kanji", "complete")
    forward = follow("kanji/克.md", "克服", "words/克服.md", "Common words")
    display("words/克服.md", "word-reused", "component")
    reverse = follow("words/克服.md", "克", "kanji/克.md", "How the kanji combine")
    line('await("Article contents")')
    line('section("Readings")')
    line('show(readingExample("克服 こくふく — overcoming; surmounting"), "word-kanji-backlink")')
    back_to(reverse, "How the kanji combine", "system-back-word-kanji")
    clothing = follow("words/克服.md", "服", "kanji/服.md", "How the kanji combine")
    display("kanji/服.md", "clothing-reused", "sentence")
    clothing_reverse = follow("kanji/服.md", "克服", "words/克服.md", "Meaning and origin")
    line('await("Article contents")')
    line('section("How the kanji combine")')
    line(f"show(articleBullet({quote(reverse['renderedText'])}), \"clothing-word-backlink\")")
    back_to(clothing_reverse, "Meaning and origin", "system-back-clothing-word")
    back_to(clothing, "How the kanji combine", "system-back-word-clothing")
    back_to(forward, "Common words", "system-back-kanji-word")
    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("072", "073"),
        ("allotmentLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies",
         "overcomeLookalikesAndIsolatedRadicalAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineAllotmentTwoReciprocalPairsBothReadingsDrawingAndSystemBack",
         "fullSingleImportOfflineOvercomeTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
        ("92f3c2ef6edbeb8dd7b6e7f37227cab8a3e20891", HEAD), ("92f3c2ef", HEAD[:8]),
        ("900e3a2130afc56b", m["contentVersion"]), ("1084", "1085"),
        ("104, n1.size", "105, n1.size"), ("N1 · 104 cards", "N1 · 105 cards"),
        ("allot; fill", "overcome"), ("allotment", "overcome"), ("充", "克"),
        ("ジュウ", "コク"), ("じゅう", "こく"),
        ('listOf("あ.てる", "み.たす")', 'listOf("か.つ")'),
        ('listOf("あ.てる"), overcome.quizKunyomi?.splitSep()', 'emptyList<String>(), overcome.quizKunyomi?.splitSep()'),
        ('listOf("あ.てる"), card.quizKunyomi?.splitSep()', 'emptyList<String>(), card.quizKunyomi?.splitSep()'),
        ('listOf("あてる"), overcome.toReadingCard().quizKeys(ReadingKind.Kun)', 'emptyList<String>(), overcome.toReadingCard().quizKeys(ReadingKind.Kun)'),
        ('((kind == ReadingKind.On && key == "こく") || (kind == ReadingKind.Kun && key == "あてる"))',
         '(kind == ReadingKind.On && key == "こく")'),
        ("repeat(2) {", "repeat(1) {"),
        ('val key = if (question.question.kind == ReadingKind.On) "こく" else "あてる"\n                assertNotEquals("みたす", question.question.correctKey)',
         'assertEquals(ReadingKind.On, question.question.kind)\n                val key = "こく"'),
        ("setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds", "setOf(ReadingKind.On), answeredKinds"),
        ("2, done.answered", "1, done.answered"), ("2, done.correct", "1, done.correct"),
        (' && it.reading == "みたす"', ''),
        ('capture("curated-both-done")', 'capture("curated-on-only-done")'),
        ('"bothCuratedKindsPersistedGoodNoMitasuAndDone"', '"soleCuratedOnPersistedGoodNoKunAndDone"'),
        ("both curated on/kun keys due; source-only み.たす retained but not offered",
         "sole curated on key due; raw か.つ retained but explicit empty quiz kun"),
        ("6, strokes.length()", "7, strokes.length()"), ("6 strokes drawn", "7 strokes drawn"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    glyphs = load(S / "batch-073-draft-audit.json")["actualAuthoredHanFonts"]["characters"]
    assert len(glyphs) == 27 and {"克", "古", "兄", "元", "儿", "己", "服", "勝"} <= set(glyphs)
    text = re.sub(r'val text = "[^"]+"', "val text = " + quote(" ".join(glyphs + ["克服"])), text, count=1)
    text = re.sub(r'Text\("Batch 073:[^"]+"\)',
                  'Text("Batch 073: overcome / look-alikes / isolated radical")', text)
    text = re.sub(r'Text\("Inspect [^\n]+fontSize = 18.sp\)',
                  'Text("Inspect 克/古/兄/元, isolated 儿 and 己/勝/服; all authored Han and 克服. Fallback families may coincide.", fontSize = 18.sp)', text)
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)',
                  "for (char in listOf(" + ", ".join(quote(c) for c in glyphs) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)', 'for (word in listOf("克服"))', text, count=1)
    text = text.replace("assertEquals(212, rows.length())", "assertEquals(112, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 204).put("wholeWordRasterProbes", 8)',
                        '.put("individualGlyphProbes", 108).put("wholeWordRasterProbes", 4)')
    text = re.sub(r'\.put\("limits", "Native Paint probes[^"]+"\)',
                  '.put("limits", "Native Paint probes cover all27 actual authored Han including isolated 儿; four whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")', text)
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("072", "充", "拡", "あてる", "みたす", "あ.てる", "み.たす", "allot", "BothReadings", "6 strokes"):
        assert stale not in text, stale
    assert len(offsets) == 4 and len({(i["document"], i["destination"]) for i in offsets}) == 4
    assert sum(i["document"] == "kanji/服.md" for i in selectors) == 1
    assert sum(i["document"] == "words/克服.md" for i in selectors) == 1
    for item in selectors:
        assert quote(item["target"]) in text
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-073/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        entries = z.namelist()
        prefix = "n1-batch-073/"
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
    assert verified == 8346
    V.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = V / "fixture-from-072.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=str(PRIOR.relative_to(R)), tofile=str(FIXTURE.relative_to(R)), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 484, "batch": "073", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED, "androidSnapshot": ANDROID,
        "contentVersion": m["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": str(PRIOR.relative_to(R)), "priorHarnessSha256": sha(PRIOR),
        "staticProjectionHelper": str(helper.relative_to(R)), "staticProjectionHelperSha256": sha(helper),
        "fixtureDiff": str(diff.relative_to(R)), "fixtureDiffSha256": sha(diff),
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(b),
                          "scope": "complete projection" if n == "kanji/克.md" else
                          "exact changed component paragraph" if n == "words/克服.md" else "exact new sentence"}
                         for n, b in documents.items()],
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "completeArticleProjections": 1, "changedReusedPassages": 2,
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
        "plannedNativePaintProbes": 108, "plannedWholeWordRasterProbes": 4,
        "plannedGlyphs": glyphs, "plannedWholeWords": ["克服"],
        "fullReadings": {"on": ["コク"], "kun": ["か.つ"]},
        "curatedReadings": {"on": ["コク"], "kun": []},
        "normalizedQuizKeys": {"on": ["こく"], "kun": []},
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": LIMITS, "nextAction": NEXT,
    }
    save(C / "batch-073-native-fixture-verification.json", record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries",
                     "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print("Unique article selectors:", len(selectors), "; directed links:", len(offsets))


def archive():
    unchanged()
    preparation = load(C / "batch-073-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    raw_log = L / "native-compile.txt"
    text = raw_log.read_text(encoding="utf-8-sig")
    assert (L / "native-compile-exit.txt").read_text().strip() == "0" and "BUILD SUCCESSFUL" in text
    with zipfile.ZipFile(APK) as z:
        assert hashlib.sha256(z.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [z.read(n) for n in z.namelist() if re.fullmatch(r"classes\d*\.dex", n)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch073{kind}Test;".encode() in b for b in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch072{kind}Test;".encode() not in b for b in dex)
        for method in ("overcomeLookalikesAndIsolatedRadicalAcrossFourProductionFamilies",
                       "fullSingleImportOfflineOvercomeTwoReciprocalPairsOnOnlyDrawingAndSystemBack"):
            assert any(method.encode() in b for b in dex)
    (V / "compile.txt").write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")
    (V / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    receipts = V / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-484.py")
    shutil.copyfile(C / "run-484-native-compile.ps1", receipts / "run-484-native-compile.ps1")
    save(S / "batch-073-native-preparation.json", preparation)
    inherited = load(S / "execution-483.json")
    for item in inherited["tests"]:
        assert sha(R / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    reports = {}
    for family in ("claude", "gpt"):
        path = R / "docs" / "n1-reviews" / f"batch-073-initial-{family}.md"
        assert not git("diff", HEAD, "--", str(path.relative_to(R)))
        reports[family] = {"report": str(path.relative_to(R)), "sha256": sha(path)}
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 1d8a4ee1a97c6bb5")):
        source = L / f"{name}.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = V / f"{name}.txt"
        target.write_text("\n".join(line.rstrip() for line in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(R)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 484, "batch": "073", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(C / "progress.json")["execution484StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-073-native-preparation.json",
        "preparationSha256": sha(S / "batch-073-native-preparation.json"),
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
            "old072DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "completeArticleSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 1, "changedReusedPassages": 2,
            "readingLabelsAndExplanations": 2, "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
            "clothingSentenceWithinExistingParagraph": True,
        },
        "accepted483AndroidRetainedWithoutRerun": True, "inheritedArchivedXmlHashesReverified": True,
        "originalReportsUnchanged": reports, "runtimeEditsMade": False, "nativeExecuted": False,
        "nativeAcceptance": False, "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 99, "remainingAdditions": 1129,
        "nextAction": NEXT, "limits": LIMITS,
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(R)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(V.rglob("*")) + [S / "batch-073-native-preparation.json"] if path.is_file()
    ]
    save(S / "execution-484.json", record)
    print("Exact packaged archive, both cases, inherited Android and reports verified.")


def checkpoint():
    unchanged()
    record = load(S / "execution-484.json")
    for item in record["artifacts"]:
        path = R / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    p = load(C / "progress.json")
    before = load(L / "execution-484-before-progress.json")
    assert all(p[k] == value for k, value in before.items() if k != "stage")
    assert set(p) == set(before) | {"execution484StartingState"}
    receipt = {
        "execution": 484, "checkpoint": 484, "batch": "073", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-484.json",
        "recordSha256": sha(S / "execution-484.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootKeysPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=484, status="continue", stage="batch-073-native-compiled-pending-execution",
             nextAction=NEXT, blocker=None)
    p["execution484StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    p["batch073NativePreparationCheckpoint"] = receipt
    p["execution484CoordinatorCheckpoint"] = receipt
    p["activeExecution"] = receipt
    save(C / "progress.json", p)
    save(L / "checkpoint-484.json", receipt)
    (L / "issue-body.txt").write_text(
        f"Batch 073 native-preparation checkpoint **484** saved locally at `{receipt['savedCommit']}` "
        "(normal signature G); no runtime publication.\n\n"
        "Exact full signed `5d322346` Git archive (version `1d8a4ee1a97c6bb5`, 1,085 kanji / "
        "5,042 words / 105 N1 cards) preserves all 8,346 runtime hashes and original publishing budgets. "
        "Both cases and the exact archive are verified inside the serially compiled APK; temporary Android "
        "source/assets removed and dedicated worktree clean. No HOST heap init or guest/app heap/guard change. "
        "Teaching/manifest unchanged; validator passes.\n\n"
        "14 static unique article selectors prepare the complete new 克 projection, both reading "
        "labels/explanations, exact reused 克服 component paragraph and new 服 sentence within its existing "
        "paragraph; two mapped reciprocal pairs/four directed transitions and System Back. Both Full/Lite "
        "retain コク/か.つ; quiz selects コク only (explicit empty kun), with sole-key completion, persisted "
        "Good and no kun question/log assertions. Seven-stroke reference-touch trace/recall and all 27 "
        "actual authored Han including isolated 儿 across four production families are prepared, not executed. "
        "Native/visual readability, fallback-face identity and phone acceptance are not claimed. Fresh483 "
        "Android3+1 and original reports hash-reverified without redundant HOST Gradle/reviews.\n\n"
        "Next: fresh device/5580/5581 ownership check, owned read-only API35 helper, both terminal native "
        "case statuses 0/no skips and actual PNG inspection; then original Claude/GPT serial dependent visual "
        "confirmation. Current-main validation/signing/owner fast-forward/CI/immutable public ZIP gates remain. "
        "**99/1,228 additions published; 1,129 remain; 100 published necessary supports are not N1 vocabulary.** "
        "Compatible Android `f9b59a2`+ required; physical-phone/general-release/whole-set acceptance outstanding. "
        "Checkpoint status `continue`; batch074 not started.",
        encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "archive": archive, "checkpoint": checkpoint}[sys.argv[1]]()
