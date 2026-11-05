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

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOG = CONTROL / "logs" / "4383793a-1c9c-496f-aa83-12f55e8a91a6"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-068-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "7ca40a695d8e01f4176f4afcca91b1e4d2d6c0b0"
REVIEWED = "80f5f424729d8832cdc9ecb8491b59559d921cd3"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-067-native" / "N1Batch067NativeTest.kt"
FIXTURE = FOLDER / "N1Batch068NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-068-7ca40a69-envelope.zip"
APK = CONTROL / "artifacts" / "n1-batch-068-native-test.apk"
PAIRS = [("儀式", "式"), ("礼儀", "礼"), ("行儀", "行"), ("お辞儀", "辞")]
GLYPHS = list("儀義億優倍人亻式礼辞行亍弋彳礻")
WORDS = [word for word, _ in PAIRS]
NEXT = (
    "SAME068: execute compiled control\\artifacts\\n1-batch-068-native-test.apk cases "
    "N1Batch068GlyphTest and N1Batch068ArticleTest using the exact full signed7ca40a69 Git envelope. "
    "Read docs\\n1-sources\\execution-443.json and batch-068-native-preparation.json. "
    "Fresh adb/device and5580/5581 local/remote connection/PID ownership immediately before "
    "launching read-only N3_Acceptance_20261029 API35 emulator-5580 with established flags "
    "-port5580 -read-only -no-snapshot -no-window -no-audio -gpu host -feature -Vulkan "
    "-memory2048 -cores2. Record owned parent/QEMU and stop only owned helper. Batch040 routing "
    "exception not inherited. No HOST heap init in native; guest/app heaps/fonts/guards unchanged. "
    "Require production ContentSync ONCE:1080kanji5037words100N1/versionddef65b637fe2f85/"
    "problems0/epoch1; Lite+Full full and curatedギ/emptyKun, normalizedぎ/noKun. Both terminal "
    "case status0/no skips, raw logs, direct PNG inspection:儀義億優倍人亻式礼辞行亍弋彳礻 and "
    "four mapped words across four production families, complete nine article projections including "
    "all eight changed reused passages/revised私儀 note; eight reciprocal pairs in16directions, "
    "SystemBack/offline/N1selection/meaning/soleOnGood/persistedgrade/15reference-stroke touch/"
    "ungradedtrace/recallmiss/persistedDrawAgain. Full article projection is native rendering scope, "
    "not fresh linguistic re-review of unchanged baseline prose. Static selectors/raster hashes "
    "do not establish viewport readability/fallback face. Reference trace is not human handwriting/MLKit. "
    "Fresh442Android3+1 inherited without redundant HOST Gradle. After nativePASS original "
    "Claude79971d7f-dd53-46bf-8249-df9d0c122c12 and GPT4b8ed210-be92-4627-8679-44e8622067dd "
    "SERIAL dependent visual confirmations with actual supported CLI/read-only tools and bounded "
    "image packets; preserve read-depth/source limits. Then latest-main nonrewriting integration/"
    "all validation/normal signing/ownerfastforward/greenCI/exactimmutablepublicZIP hashes+budgets/"
    "ownerissue60 before publication or069. Preserve historical permission/signing/memory failures, "
    "no workaround/guard increase/second runner/supervisor edits. Full live history preserved. "
    "Published94/1228,remaining1134;068local not delivered. CompatibleAndroidf9b59a2+ required; "
    "phone/general-release/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def unchanged():
    assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", cwd=ANDROID)


def quote(text):
    return json.dumps(text, ensure_ascii=False).replace("$", "\\$")


mode = sys.argv[1]
if mode == "prepare":
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    status = git("status", "--porcelain")
    assert not status or status == "?? docs/n1-reviews/batch-068-native/"
    unchanged()
    assert not APK.exists()
    if FOLDER.exists():
        previous = load(CONTROL / "batch-068-native-fixture-verification.json")
        assert sha(FIXTURE) == previous["fixtureSha256"] and sha(ARCHIVE) == previous["archiveSha256"]
        assert {p.name for p in FOLDER.iterdir()} == {"N1Batch068NativeTest.kt", "fixture-from-067.diff"}
    save(LOG / "execution-443-before-progress.json", load(CONTROL / "progress.json"))
    manifest = load(ROOT / "manifest.json")
    assert manifest["contentVersion"] == "ddef65b637fe2f85"
    counts = {
        "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
        "words": sum(name.startswith("words/") for name in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (ROOT / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1080, "words": 5037, "n1": 100}
    helper = ROOT / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    functions = ast.Module(body=[node for node in parsed.body if isinstance(node, ast.FunctionDef)
                                and node.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(functions, str(helper), "exec"), namespace)
    names = ["kanji/儀.md"] + [f"words/{word}.md" for word, _ in PAIRS] + [
        f"kanji/{kanji}.md" for _, kanji in PAIRS]
    documents = {name: namespace["blocks"](ROOT / name) for name in names}
    lines, selectors, transitions, linked_offsets = [], [], [], []

    def line(value):
        lines.append("            " + value)

    def display(document, slug):
        projected = documents[document]
        assert projected[0][0] == "heading"
        line(f"await({quote(projected[0][1])})")
        table_cell = 0
        for index, (kind, value) in enumerate(projected[1:], 1):
            if kind == "heading":
                line(f"section({quote(value)})")
                continue
            if kind == "table":
                table_cell += 1
                if table_cell % 3 != 0 or value == "Typical words":
                    continue
            qualifier = "readingExample" if kind == "table" else "articleBullet"
            candidates = [(k, v) for k, v in projected if v == value and
                          ((k == "table") if kind == "table" else (k != "table" and k != "heading"))]
            assert len(candidates) == 1, (document, value)
            step = f"{slug}-{index:02}"
            line(f"show({qualifier}({quote(value)}), {quote(step)})")
            selectors.append({"document": document, "kind": kind, "target": value, "step": step})

    def follow(document, label, destination, kind):
        body = (ROOT / document).read_text(encoding="utf-8")
        section_name = "How the kanji combine" if document.startswith("words/") else "Common words"
        section_body = body.split("## " + section_name + "\n", 1)[1].split("\n## ", 1)[0]
        links = re.findall(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", section_body)
        import posixpath
        destinations = {posixpath.normpath(posixpath.join(posixpath.dirname(document), link))
                        for link in links if not link.startswith("https://")}
        assert destinations == {destination}, (document, label, destinations, destination)
        blocks = []
        label_pattern = r"(?<![\u3400-\u9fff])" + re.escape(label) + r"(?![\u3400-\u9fff])"
        current_section = None
        for block_kind, value in documents[document]:
            if block_kind == "heading":
                current_section = value
            elif current_section == section_name and re.search(label_pattern, value) and block_kind == kind:
                blocks.append((block_kind, value))
        assert len(blocks) == 1, (document, label, blocks)
        raw_paragraphs = re.split(r"\n\s*\n|\n(?=- )", section_body.strip())
        raw = next(part.removeprefix("- ") for part in raw_paragraphs
                   if namespace["plain"](" ".join(part.removeprefix("- ").splitlines())) == blocks[0][1])
        prefix = raw[:raw.index("[" + label + "](")]
        offset = len(namespace["plain"](" ".join(prefix.splitlines())))
        assert blocks[0][1][offset:].startswith(label), (document, label, offset)
        line(f"inline(await(articleBullet({quote(blocks[0][1])})), {quote(label)}, {offset})")
        transitions.append([document, destination])
        linked_offsets.append({"document": document, "destination": destination, "label": label,
                               "renderedText": blocks[0][1], "offset": offset})
        return blocks[0][1]

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("儀")')
    line('click("ceremony; formal conduct")')
    display("kanji/儀.md", "kanji")
    for index, (word, component) in enumerate(PAIRS, 1):
        word_path, component_path = f"words/{word}.md", f"kanji/{component}.md"
        line('section("Common words")')
        follow("kanji/儀.md", word, word_path, "paragraph")
        display(word_path, f"word{index}")
        line('section("How the kanji combine")')
        follow(word_path, "儀", "kanji/儀.md", "paragraph")
        line('await("Article contents")')
        line('section("Readings")')
        reading = next(value for kind, value in documents["kanji/儀.md"]
                       if kind == "table" and "儀式" in value)
        line(f"show(readingExample({quote(reading)}), \"word{index}-new-kanji-backlink\")")
        line("back()")
        line('section("How the kanji combine")')
        changed = follow(word_path, component, component_path, "paragraph")
        display(component_path, f"component{index}")
        line('section("Common words")')
        follow(component_path, word, word_path, "paragraph")
        line(f"await({quote(documents[word_path][0][1])})")
        line('section("How the kanji combine")')
        line(f"show(articleBullet({quote(changed)}), \"word{index}-legacy-backlink\")")
        line("back()")
        line('await("Common words")')
        line(f'capture("system-back-component{index}")')
        line("back()")
        line('await("How the kanji combine")')
        line(f'capture("system-back-word{index}-component")')
        line("back()")
        line('await("Common words")')
        line(f'capture("system-back-kanji-word{index}")')
    assert len(transitions) == 16 and len({tuple(pair) for pair in transitions}) == 16
    route = "\n".join(lines) + "\n"
    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("067", "068"),
        ("buddhistClergyLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
         "ceremonyLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineBuddhistClergyReciprocalComparisonOnOnlyDrawingAndSystemBack",
         "fullSingleImportOfflineCeremonyEightReciprocalPairsOnOnlyDrawingAndSystemBack"),
        ("a45ce3014661487bf16977260daa5ca23e001663", HEAD), ("a45ce301", HEAD[:8]),
        ("68c767f176e68882", manifest["contentVersion"]),
        ("1079", "1080"), ("99, n1.size", "100, n1.size"), ("N1 · 99 cards", "N1 · 100 cards"),
        ("clergy", "ceremony"), ("僧", "儀"), ("ソウ", "ギ"), ("そう", "ぎ"),
        ("Buddhist monk; priest", "ceremony; formal conduct"),
        ("13, strokes.length()", "15, strokes.length()"), ("13 strokes drawn", "15 strokes drawn"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    start = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
    text = text[:start] + route + text[end:]
    text = text.replace("private fun inline(node: SemanticsNodeInteraction, label: String)",
                        "private fun inline(node: SemanticsNodeInteraction, label: String, offset: Int)")
    text = text.replace("        val offset = text.indexOf(label)\n        assertTrue(\"Missing $label in $text\", offset >= 0)",
                        '        assertTrue("Wrong linked offset $offset for $label in $text", offset >= 0 && text.substring(offset).startsWith(label))')
    text = re.sub(r'val text = "[^"]+"', "val text = " + quote(" ".join(GLYPHS + WORDS)), text, count=1)
    text = text.replace("Batch 068: Buddhist ceremony / look-alikes / radical variants",
                        "Batch 068: ceremony / look-alikes / radical variants")
    text = text.replace("fontSize = 24.sp, lineHeight = 34.sp", "fontSize = 18.sp, lineHeight = 26.sp")
    text = re.sub(r'Text\("Compare [^\n]+fontSize = 18.sp\)',
                  'Text("Inspect 儀 versus 義/億/優/倍, 人 versus 亻, all four mapped words and actual fallback components 亍/弋/彳/礻. Fallback families may coincide.", fontSize = 18.sp)', text)
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)', "for (char in listOf(" +
                  ", ".join(quote(char) for char in GLYPHS) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)', "for (word in listOf(" +
                  ", ".join(quote(word) for word in WORDS) + "))", text, count=1)
    text = text.replace("assertEquals(40, rows.length())", "assertEquals(76, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 32).put("wholeWordRasterProbes", 8)',
                        '.put("individualGlyphProbes", 60).put("wholeWordRasterProbes", 16)')
    text = re.sub(r'\.put\("limits", "Thirty-two[^"]+"\)',
                  '.put("limits", "Sixty single-character native Paint probes including 人/亻 and actual fallback components 亍/弋/彳/礻, sixteen whole-word nonblank raster probes and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")', text)
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for obsolete in ("067", "僧", "ソウ", "そう", "clergy", "13 strokes"):
        assert obsolete not in text, (obsolete, [value for value in text.splitlines() if obsolete in value])
    assert text.count('listOf("ギ")') == 4
    if not ARCHIVE.exists():
        subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-068/",
                        f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
    with zipfile.ZipFile(ARCHIVE) as zipped:
        entries = zipped.namelist()
        prefix = "n1-batch-068/"
        assert len(entries) == len(set(entries)) and len(entries) <= 18000
        assert all(name.startswith(prefix) and "\\" not in name and ".." not in name.split("/")
                   for name in entries)
        raw_manifest = zipped.read(prefix + "manifest.json")
        assert raw_manifest == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=ROOT)
        assert json.loads(raw_manifest) == manifest
        retained, verified = len(raw_manifest), 0
        binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        for section, mapping in manifest.items():
            if not isinstance(mapping, dict):
                continue
            for name, expected in mapping.items():
                data = zipped.read(prefix + name)
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit, name
                normalized = data if section in binary else data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(normalized).hexdigest() == expected, name
                retained += len(data)
                verified += 1
        inflated = sum(info.file_size for info in zipped.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in name or "/tools/" in name for name in entries)
    assert verified == 8331
    FOLDER.mkdir(exist_ok=True)
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-067.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)),
        encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 443, "batch": "068",
        "status": "static-native-preparation-verified-not-executed",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "androidSnapshot": git("rev-parse", "HEAD", cwd=ANDROID),
        "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated,
        "retainedBytes": retained, "verifiedRuntimeHashes": verified, "manifestEqual": True,
        "safePathsPerFileAndOriginalPublishingBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "reusedAcceptedHarness": str(PRIOR.relative_to(ROOT)), "reusedAcceptedHarnessSha256": sha(PRIOR),
        "staticProjectionHelper": str(helper.relative_to(ROOT)), "staticProjectionHelperSha256": sha(helper),
        "fixtureDiff": str(diff.relative_to(ROOT)), "fixtureDiffSha256": sha(diff),
        "articleFiles": [{"path": name, "sha256": sha(ROOT / name), "projectedTextBlocks": len(blocks)}
                         for name, blocks in documents.items()],
        "staticMarkdownSelectors": selectors, "articleRouteTransitions": transitions,
        "staticLinkedOffsets": linked_offsets,
        "completeArticleProjections": 9, "mappedReciprocalPairs": 8, "directedTransitions": 16,
        "plannedArticleCaptureSteps": len(selectors) + 20,
        "plannedNativePaintProbes": 60, "plannedWholeWordRasterProbes": 16,
        "plannedGlyphs": GLYPHS, "plannedWholeWords": WORDS,
        "fullReadings": {"on": ["ギ"], "kun": []}, "curatedReadings": {"on": ["ギ"], "kun": []},
        "normalizedQuizKeys": {"on": ["ぎ"], "kun": []},
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "accepted442AndroidRetainedWithoutRerun": True, "nativeExecuted": False,
        "independentVisualAcceptance": False, "phoneEvidence": False,
        "publicationAttempted": False, "runtimeEdited": False, "hostTestInitScriptUsed": False,
        "projectionQualification": "Nine article block projections cover every prose block and table example cell with section navigation and exact kind-qualified unique selectors. Table reading/type labels are not separately asserted. Static projection is not native semantics/viewport/readability acceptance or fresh linguistic review of unchanged baseline prose. Eight mapped reciprocal pairs require sixteen directed link touches at exact source-derived offsets and System Back.",
        "limits": "Preparation/compilation only. Full Git archive and production ContentSync ONCE; no reduced fixture, guest/app heap change or guard increase. Sixty glyph/sixteen word raster probes and fifteen-stroke reference trace/recall prepared, not executed. Raster hashes do not identify fallback face or readability. Reference tracing is not human handwriting or MLKit evidence. Native/visual/physical-phone/current-main/publication/whole-set gates outstanding.",
        "nextAction": NEXT,
    }
    save(CONTROL / "batch-068-native-fixture-verification.json", record)
    print(json.dumps({key: record[key] for key in ("status", "expectedCounts", "zipEntries",
          "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print(f"Static article selectors: {len(selectors)}; sixteen directed transitions.")
elif mode == "archive":
    unchanged()
    preparation = load(CONTROL / "batch-068-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    linked_offsets = []
    quoted = r'("(?:\\.|[^"\\])*")'
    for match in re.finditer(r"inline\(await\(articleBullet\(" + quoted +
                             r"\)\), " + quoted + r", (\d+)\)", FIXTURE.read_text(encoding="utf-8")):
        rendered, label, offset = json.loads(match[1]), json.loads(match[2]), int(match[3])
        assert rendered[offset:].startswith(label)
        document, destination = preparation["articleRouteTransitions"][len(linked_offsets)]
        linked_offsets.append({"document": document, "destination": destination, "label": label,
                               "renderedText": rendered, "offset": offset})
    assert len(linked_offsets) == 16
    preparation["staticLinkedOffsets"] = linked_offsets
    preparation["projectionQualification"] = (
        "Nine article block projections cover every prose block and table example cell with section "
        "navigation and exact kind-qualified unique selectors. Table reading/type labels are not "
        "separately asserted. Static projection is not native semantics/viewport/readability acceptance "
        "or fresh linguistic review of unchanged baseline prose. Eight mapped reciprocal pairs require "
        "sixteen directed link touches at exact source-derived offsets and System Back."
    )
    preparation["preCompilationHarnessCorrections"] = (
        "Static authoring assertions rejected unscoped same-label links and duplicate reading labels. "
        "Final selectors are section/kind qualified. Source-derived exact linked-text offsets replace "
        "the inherited first-substring shortcut, which could target unlinked 御辞儀 before [辞]/[儀]. "
        "Changed-passage Back checks use the actual formation paragraph, not a meaning substring. "
        "All corrections preceded the single successful compile; no production defect or native pass inferred."
    )
    save(CONTROL / "batch-068-native-fixture-verification.json", preparation)
    raw_log = LOG / "native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (LOG / "native-compile-exit.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in compile_text
    with zipfile.ZipFile(APK) as package:
        assert hashlib.sha256(package.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist() if re.fullmatch(r"classes\d*\.dex", name)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch068{kind}Test;".encode() in blob for blob in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch067{kind}Test;".encode() not in blob for blob in dex)
        for method in ("ceremonyLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
                       "fullSingleImportOfflineCeremonyEightReciprocalPairsOnOnlyDrawingAndSystemBack"):
            assert any(method.encode() in blob for blob in dex)
    (FOLDER / "compile.txt").write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    assert gzip.decompress((FOLDER / "compile-raw.txt.gz").read_bytes()) == raw_log.read_bytes()
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir(exist_ok=True)
    shutil.copyfile(Path(__file__), receipts / "execution-443.py")
    shutil.copyfile(CONTROL / "run-443-native-compile.ps1", receipts / "run-443-native-compile.ps1")
    save(SOURCES / "batch-068-native-preparation.json", preparation)
    inherited = load(SOURCES / "execution-442.json")
    for item in inherited["tests"]:
        assert sha(ROOT / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-068-reconciliation.json")
    reports = {}
    for key, process in reconciliation["processes"].items():
        path = ROOT / "docs" / "n1-reviews" / process["report"]
        assert sha(path) == process["reportSha256"]
        reports[key] = {"report": process["report"], "sha256": sha(path)}
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version ddef65b637fe2f85")):
        source = LOG / f"{name}.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = FOLDER / f"{name}.txt"
        target.write_text("\n".join(line.rstrip() for line in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(ROOT)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 443, "batch": "068", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(CONTROL / "progress.json")["execution443StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-068-native-preparation.json",
        "preparationSha256": sha(SOURCES / "batch-068-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "exitCode": 0, "status": "compiled-not-executed",
            "result": re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0),
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "log": str((FOLDER / "compile.txt").relative_to(ROOT)), "logSha256": sha(FOLDER / "compile.txt"),
            "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "apk": str(APK), "apkSha256": sha(APK), "apkBytes": APK.stat().st_size,
            "packagedExactFullArchiveVerified": True, "bothClassesAndMethodsVerified": True,
            "old067DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "completeArticleSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 9, "mappedReciprocalPairs": 8, "directedTransitions": 16,
            "method": preparation["projectionQualification"],
        },
        "accepted442AndroidRetainedWithoutRerun": True, "inherited442ArchivedXmlHashesReverified": True,
        "originalReportsUnchanged": reports, "runtimeEditsMade": False, "nativeExecuted": False,
        "nativeAcceptance": False, "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 94, "remainingAdditions": 1134,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(FOLDER.rglob("*")) + [SOURCES / "batch-068-native-preparation.json"] if path.is_file()
    ]
    save(SOURCES / "execution-443.json", record)
    print("Exact packaged archive, two classes/methods, inherited Android and all original reports verified.")
elif mode == "checkpoint":
    unchanged()
    record = load(SOURCES / "execution-443.json")
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    progress = load(CONTROL / "progress.json")
    before = load(LOG / "execution-443-before-progress.json")
    assert progress == before
    checkpoint = {
        "execution": 443, "checkpoint": 443, "batch": "068", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-443.json",
        "recordSha256": sha(SOURCES / "execution-443.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalKeysPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=443, status="continue", stage="batch-068-native-compiled-pending-execution",
                    nextAction=NEXT, blocker=None)
    progress["execution443StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    progress["batch068NativePreparationCheckpoint"] = checkpoint
    progress["execution443CoordinatorCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", progress)
    save(LOG / "execution-443-checkpoint.json", checkpoint)
    (LOG / "issue-body.txt").write_text(
        f"Batch 068 native-preparation checkpoint **443** saved locally at `{checkpoint['savedCommit']}` "
        "(normal signature G); no runtime publication.\n\n"
        "The exact full `7ca40a69` Git archive (version `ddef65b637fe2f85`, 1,080 kanji / 5,037 words / "
        "100 N1 cards) preserves all 8,331 runtime hashes and original publishing budgets. The fixture "
        "compiles serially with one worker, no HOST-only heap init and unchanged guest/app heaps/guards. "
        "Both cases and the exact archive are verified inside the APK; temporary Android source/assets "
        "were removed and its worktree is clean. Teaching and manifest are unchanged; validator passes.\n\n"
        f"{record['selectorAudit']['completeArticleSelectors']} static unique article selectors prepare nine "
        "complete article projections (not fresh linguistic review of unchanged baseline prose), all eight "
        "changed reused passages, revised 私儀 note and eight reciprocal pairs in sixteen directions. "
        "Sole curated ギ/no kun, fifteen-stroke trace/recall, 60 glyph and 16 word raster probes include "
        "儀/義/億/優/倍, 人/亻 and actual fallback components 亍/弋/彳/礻. These are **prepared, not executed**. "
        "Native readability, fallback-face identity and visual/phone acceptance are not claimed. Fresh442 "
        "Android3+1 and all original reports are hash-reverified without redundant reruns; historical "
        "permission/memory/signing evidence remains preserved.\n\n"
        "**Next:** separate native execution with fresh device/port/PID ownership, original-session serial "
        "visual confirmations, then combined-main/signing/CI/exact immutable public-ZIP gates before "
        "publication or069. Published coverage remains **94/1,228 additions; 1,134 remain**. Compatible "
        "Android `f9b59a2+` required; physical-phone/general-release and whole-set acceptance outstanding.\n",
        encoding="utf-8")
    print("Signed local checkpoint443 saved with complete live history.")
else:
    raise ValueError(mode)
