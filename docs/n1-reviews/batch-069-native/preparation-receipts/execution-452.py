import ast
import difflib
import gzip
import hashlib
import json
import posixpath
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
LOG = CONTROL / "logs" / "dfb82b02-41bb-44fc-9ac5-da2c28f6208d"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-069-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "e245739783dbc2ebe33ee164b8cfa718d670551b"
REVIEWED = "f5061bcdf101f8eba5729b21f222b57821df9a38"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-068-native" / "N1Batch068NativeTest.kt"
FIXTURE = FOLDER / "N1Batch069NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-069-e2457397-envelope.zip"
APK = CONTROL / "artifacts" / "n1-batch-069-native-test.apk"
GLYPHS = list("儒需儀僧優人亻教攴攵子考校木")
WORDS = ["儒教"]
NEXT = (
    "SAME069: execute compiled control\\artifacts\\n1-batch-069-native-test.apk "
    "N1Batch069GlyphTest and N1Batch069ArticleTest with exact signed e2457397 full Git envelope. "
    "Read docs\\n1-sources\\execution-452.json and batch-069-native-preparation.json. "
    "Fresh adb/device and5580/5581 local/remote connection/PID ownership immediately before "
    "read-only N3_Acceptance_20261029 emulator-5580 launch with established API35 flags "
    "-port5580 -read-only -no-snapshot -no-window -no-audio -gpu host -feature -Vulkan "
    "-memory2048 -cores2. Record helper parent/QEMU identities; stop only owned helper. "
    "Batch040 routing override not inherited. No HOST heap init/native guest or app heap/guard changes. "
    "Require ContentSync ONCE:1081kanji5038words101N1/version83ed94552dd1a9ce/problems0/epoch1; "
    "Full+Lite full/curatedジュ,emptyKun; normalizedじゅ,noKun. Terminal status0 for BOTH cases, "
    "no skips and actual PNG inspection; 儒/需/儀/僧/優/人/standalone亻/教/攴/攵/子/考/校/木 "
    "and 儒教 across four production families, three complete article projections, two reciprocal "
    "pairs/four directions, System Back/offline/N1selection/meaning/soleOnGood/persistedgrade/"
    "16reference-stroke touch/ungradedtrace/recallmiss/persistedDrawAgain. Static selectors/raster "
    "hashes are not readability, fallback-face or phone evidence. Full unchanged 教 projection is "
    "rendering scope, not fresh linguistic review. Reference trace is not human handwriting/MLKit. "
    "Fresh451Android3+1 inherited; no redundant HOST Gradle absent new concern. After native pass "
    "original Claude78cf2390-1187-4593-ba60-ebe562f1a49a and GPTe683a0f6-66de-4049-ae70-eb508e0866ee "
    "SERIAL dependent visual confirmations using actual supported CLI/read-only tools and bounded "
    "packets. Then current-main nonrewriting integration/all validation/normal signing/owner fastforward/"
    "greenCI/exactimmutablepublicZIP hashes+budgets/ownerissue60 receipt before publication or070. "
    "No second runner/supervisor edits/permission bypass/signing workaround. Published95/1228,remaining1133; "
    "069 local is not delivered. Compatible Androidf9b59a2+ required; physical-phone/general-release/"
    "whole-set acceptance outstanding."
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
    assert not git("status", "--porcelain")
    unchanged()
    assert not FOLDER.exists() and not ARCHIVE.exists() and not APK.exists()
    manifest = load(ROOT / "manifest.json")
    assert manifest["contentVersion"] == "83ed94552dd1a9ce"
    counts = {
        "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
        "words": sum(name.startswith("words/") for name in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (ROOT / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1081, "words": 5038, "n1": 101}, counts
    helper = ROOT / "docs" / "n1-reviews" / "batch-066-native" / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(helper.read_text(encoding="utf-8"))
    functions = ast.Module(body=[node for node in parsed.body if isinstance(node, ast.FunctionDef)
                                and node.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(functions, str(helper), "exec"), namespace)
    names = ["kanji/儒.md", "words/儒教.md", "kanji/教.md"]
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
        destinations = {posixpath.normpath(posixpath.join(posixpath.dirname(document), link))
                        for link in links if not link.startswith("https://")}
        assert destinations == {destination}, (document, label, destinations, destination)
        matching = []
        label_pattern = r"(?<![\u3400-\u9fff])" + re.escape(label) + r"(?![\u3400-\u9fff])"
        current_section = None
        for block_kind, value in documents[document]:
            if block_kind == "heading":
                current_section = value
            elif current_section == section_name and re.search(label_pattern, value) and block_kind == kind:
                matching.append(value)
        assert len(matching) == 1, (document, label, matching)
        raw_paragraphs = re.split(r"\n\s*\n|\n(?=- )", section_body.strip())
        raw = next(part.removeprefix("- ") for part in raw_paragraphs
                   if namespace["plain"](" ".join(part.removeprefix("- ").splitlines())) == matching[0])
        link = re.search(r"\[" + re.escape(label) + r"\]\([^)]+\)", raw)
        assert link is not None
        marker = "N1_LINK_TARGET_452"
        assert marker not in raw
        marked = raw[:link.start()] + marker + raw[link.end():]
        offset = namespace["plain"](" ".join(marked.splitlines())).index(marker)
        assert matching[0][offset:].startswith(label), (document, label, offset)
        line(f"inline(await(articleBullet({quote(matching[0])})), {quote(label)}, {offset})")
        transitions.append([document, destination])
        linked_offsets.append({"document": document, "destination": destination, "label": label,
                               "renderedText": matching[0], "offset": offset})
        return matching[0]

    line('click("Browse all kanji")')
    line('rule.onNode(hasSetTextAction()).performTextReplacement("儒")')
    line('click("Confucian; Confucian scholar")')
    display("kanji/儒.md", "kanji")
    line('section("Common words")')
    follow("kanji/儒.md", "儒教", "words/儒教.md", "paragraph")
    display("words/儒教.md", "word1")
    line('section("How the kanji combine")')
    follow("words/儒教.md", "儒", "kanji/儒.md", "paragraph")
    line('await("Article contents")')
    line('section("Readings")')
    reading = next(value for kind, value in documents["kanji/儒.md"] if kind == "table" and "儒教" in value)
    line(f"show(readingExample({quote(reading)}), \"word1-new-kanji-backlink\")")
    line("back()")
    line('section("How the kanji combine")')
    changed = follow("words/儒教.md", "教", "kanji/教.md", "paragraph")
    display("kanji/教.md", "component1")
    line('section("Common words")')
    follow("kanji/教.md", "儒教", "words/儒教.md", "paragraph")
    line(f"await({quote(documents['words/儒教.md'][0][1])})")
    line('section("How the kanji combine")')
    line(f"show(articleBullet({quote(changed)}), \"word1-legacy-backlink\")")
    line("back()")
    line('await("Common words")')
    line('capture("system-back-component1")')
    line("back()")
    line('await("How the kanji combine")')
    line('capture("system-back-word1-component")')
    line("back()")
    line('await("Common words")')
    line('capture("system-back-kanji-word1")')
    assert len(transitions) == len({tuple(pair) for pair in transitions}) == 4
    route = "\n".join(lines) + "\n"
    text = PRIOR.read_text(encoding="utf-8")
    replacements = [
        ("068", "069"),
        ("ceremonyLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
         "confucianLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineCeremonyEightReciprocalPairsOnOnlyDrawingAndSystemBack",
         "fullSingleImportOfflineConfucianTwoReciprocalPairsOnOnlyDrawingAndSystemBack"),
        ("7ca40a695d8e01f4176f4afcca91b1e4d2d6c0b0", HEAD), ("7ca40a69", HEAD[:8]),
        ("ddef65b637fe2f85", manifest["contentVersion"]),
        ("1080", "1081"), ("5037", "5038"),
        ("100, n1.size", "101, n1.size"), ("N1 · 100 cards", "N1 · 101 cards"),
        ("ceremony", "confucian"), ("儀", "儒"), ("ギ", "ジュ"), ("ぎ", "じゅ"),
        ("confucian; formal conduct", "Confucian; Confucian scholar"),
        ("15, strokes.length()", "16, strokes.length()"), ("15 strokes drawn", "16 strokes drawn"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    start = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
    text = text[:start] + route + text[end:]
    text = re.sub(r'val text = "[^"]+"', "val text = " + quote(" ".join(GLYPHS + WORDS)), text, count=1)
    text = text.replace("Batch 069: confucian / look-alikes / radical variants",
                        "Batch 069: Confucian / look-alikes / radical variants")
    text = re.sub(r'Text\("Inspect [^\n]+fontSize = 18.sp\)',
                  'Text("Inspect 儒 versus 需/儀/僧/優, 人 versus standalone 亻, 儒教 and 教 with 子/攴/攵 plus 考/校/木. Fallback families may coincide.", fontSize = 18.sp)', text)
    text = re.sub(r'for \(char in listOf\([^\n]+\)\)', "for (char in listOf(" +
                  ", ".join(quote(char) for char in GLYPHS) + "))", text, count=1)
    text = re.sub(r'for \(word in listOf\([^\n]+\)\)', 'for (word in listOf("儒教"))', text, count=1)
    text = text.replace("assertEquals(76, rows.length())", "assertEquals(60, rows.length())")
    text = text.replace('.put("individualGlyphProbes", 60).put("wholeWordRasterProbes", 16)',
                        '.put("individualGlyphProbes", 56).put("wholeWordRasterProbes", 4)')
    text = re.sub(r'\.put\("limits", "Sixty[^"]+"\)',
                  '.put("limits", "Fifty-six single-character native Paint probes including 人/standalone亻 and actual 攴/攵, four whole-word nonblank raster probes and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")', text)
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text and "068" not in text and "ギ" not in text
    assert text.count('listOf("ジュ")') == 4
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-069/",
                    f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
    with zipfile.ZipFile(ARCHIVE) as zipped:
        entries = zipped.namelist()
        prefix = "n1-batch-069/"
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
    assert verified == 8334
    FOLDER.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-068.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)),
        encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 452, "batch": "069",
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
        "completeArticleProjections": 3, "mappedReciprocalPairs": 2, "directedTransitions": 4,
        "plannedArticleCaptureSteps": len(selectors) + 5,
        "plannedNativePaintProbes": 56, "plannedWholeWordRasterProbes": 4,
        "plannedGlyphs": GLYPHS, "plannedWholeWords": WORDS,
        "fullReadings": {"on": ["ジュ"], "kun": []}, "curatedReadings": {"on": ["ジュ"], "kun": []},
        "normalizedQuizKeys": {"on": ["じゅ"], "kun": []},
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "accepted451AndroidRetainedWithoutRerun": True, "nativeExecuted": False,
        "independentVisualAcceptance": False, "phoneEvidence": False,
        "publicationAttempted": False, "runtimeEdited": False, "hostTestInitScriptUsed": False,
        "projectionQualification": "Three complete article block projections cover every prose block and table example cell with section navigation and exact kind-qualified unique selectors. Table reading/type labels not separately asserted. Static projection is not native semantics/viewport/readability acceptance or fresh linguistic review of unchanged 教 prose. Two mapped reciprocal pairs require four directed link touches at exact source-derived offsets and System Back.",
        "preCompilationHarnessCorrection": "First static preparation rejected inherited prefix-only offset calculation for a linked 教 beginning a wrapped Markdown line: splitlines omitted the boundary space. Exact full-paragraph sentinel projection now preserves the actual renderer space and verifies each final label offset. Failed preparation wrote no fixture/archive; no production defect or native pass inferred.",
        "limits": "Preparation/compilation only. Full Git archive and production ContentSync ONCE; no reduced fixture, guest/app heap change or guard increase. Fifty-six glyph/four word raster probes and sixteen-stroke reference trace/recall prepared, not executed. Raster hashes do not identify fallback face or readability. Reference tracing is not human handwriting or MLKit evidence. Native/visual/physical-phone/current-main/publication/whole-set gates outstanding.",
        "nextAction": NEXT,
    }
    save(CONTROL / "batch-069-native-fixture-verification.json", record)
    print(json.dumps({key: record[key] for key in ("status", "expectedCounts", "zipEntries",
          "verifiedRuntimeHashes", "compressedBytes", "inflatedBytes", "retainedBytes")}, indent=2))
    print(f"Static article selectors: {len(selectors)}; four directed transitions.")
elif mode == "archive":
    unchanged()
    preparation = load(CONTROL / "batch-069-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"] and sha(ARCHIVE) == preparation["archiveSha256"]
    raw_log = LOG / "native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (LOG / "native-compile-exit.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in compile_text
    with zipfile.ZipFile(APK) as package:
        assert hashlib.sha256(package.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist() if re.fullmatch(r"classes\d*\.dex", name)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch069{kind}Test;".encode() in blob for blob in dex)
            assert all(f"Lio/github/stopcran/kanji/ui/N1Batch068{kind}Test;".encode() not in blob for blob in dex)
        for method in ("confucianLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
                       "fullSingleImportOfflineConfucianTwoReciprocalPairsOnOnlyDrawingAndSystemBack"):
            assert any(method.encode() in blob for blob in dex)
    (FOLDER / "compile.txt").write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    assert gzip.decompress((FOLDER / "compile-raw.txt.gz").read_bytes()) == raw_log.read_bytes()
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-452.py")
    shutil.copyfile(CONTROL / "run-452-native-compile.ps1", receipts / "run-452-native-compile.ps1")
    save(SOURCES / "batch-069-native-preparation.json", preparation)
    inherited = load(SOURCES / "execution-451.json")
    for item in inherited["tests"]:
        assert sha(ROOT / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-069-reconciliation.json")
    reports = {}
    for key, process in reconciliation["processes"].items():
        path = ROOT / "docs" / "n1-reviews" / process["report"]
        assert sha(path) == process["reportSha256"]
        reports[key] = {"report": process["report"], "sha256": sha(path)}
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 83ed94552dd1a9ce")):
        source = LOG / f"{name}.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = FOLDER / f"{name}.txt"
        target.write_text("\n".join(line.rstrip() for line in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(ROOT)), "sha256": sha(target)})
    record = {
        "schemaVersion": 1, "execution": 452, "batch": "069", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": REVIEWED,
        "authorization": load(CONTROL / "progress.json")["execution452StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-069-native-preparation.json",
        "preparationSha256": sha(SOURCES / "batch-069-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "exitCode": 0, "status": "compiled-not-executed",
            "result": re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0),
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "log": str((FOLDER / "compile.txt").relative_to(ROOT)), "logSha256": sha(FOLDER / "compile.txt"),
            "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "apk": str(APK), "apkSha256": sha(APK), "apkBytes": APK.stat().st_size,
            "packagedExactFullArchiveVerified": True, "bothClassesAndMethodsVerified": True,
            "old068DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixtureSha256": sha(FIXTURE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "completeArticleSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 3, "mappedReciprocalPairs": 2, "directedTransitions": 4,
            "method": preparation["projectionQualification"],
        },
        "accepted451AndroidRetainedWithoutRerun": True, "inherited451ArchivedXmlHashesReverified": True,
        "originalReportsUnchanged": reports, "runtimeEditsMade": False, "nativeExecuted": False,
        "nativeAcceptance": False, "independentVisualAcceptance": False, "reviewersLaunched": 0,
        "publicationAttempted": False, "publishedAdditions": 95, "remainingAdditions": 1133,
        "nextAction": NEXT, "limits": preparation["limits"],
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(FOLDER.rglob("*")) + [SOURCES / "batch-069-native-preparation.json"] if path.is_file()
    ]
    save(SOURCES / "execution-452.json", record)
    print("Exact packaged archive, both cases, inherited Android and original reports verified.")
elif mode == "checkpoint":
    unchanged()
    record = load(SOURCES / "execution-452.json")
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    progress = load(CONTROL / "progress.json")
    before = load(LOG / "execution-452-before-progress.json")
    assert all(progress[key] == value for key, value in before.items() if key != "stage")
    assert set(progress) == set(before) | {"execution452StartingState"}
    checkpoint = {
        "execution": 452, "checkpoint": 452, "batch": "069", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-452.json",
        "recordSha256": sha(SOURCES / "execution-452.json"), "status": "continue",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalKeysPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=452, status="continue", stage="batch-069-native-compiled-pending-execution",
                    nextAction=NEXT, blocker=None)
    progress["execution452StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    progress["batch069NativePreparationCheckpoint"] = checkpoint
    progress["execution452CoordinatorCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", progress)
    save(LOG / "execution-452-checkpoint.json", checkpoint)
    (LOG / "issue-body.txt").write_text(
        f"Batch 069 native-preparation checkpoint **452** saved locally at `{checkpoint['savedCommit']}` "
        "(normal signature G); no runtime publication.\n\n"
        "The exact full signed `e2457397` Git archive (version `83ed94552dd1a9ce`, 1,081 kanji / "
        "5,038 words / 101 N1 cards) preserves all 8,334 runtime hashes and original publishing budgets. "
        "Both cases and the exact archive are verified inside the serially compiled APK; temporary Android "
        "source/assets removed and dedicated worktree clean. No HOST-only heap init or guest/app heap/guard "
        "change. Teaching/manifest unchanged; validator passes.\n\n"
        f"{record['selectorAudit']['completeArticleSelectors']} static unique article selectors prepare three "
        "complete projections (儒, 儒教 and 教; unchanged 教 prose is rendering scope, not fresh linguistic review), "
        "two reciprocal pairs in four directions, sole curated ジュ/no kun, sixteen-stroke trace/recall, "
        "56 glyph and four word raster probes. Glyphs include 儒/需/儀/僧/優/人/standalone亻/教/攴/攵/子/考/校/木. "
        "These are **prepared, not executed**; native/visual readability, fallback-face identity and phone "
        "acceptance are not claimed. Fresh451 Android3+1 and original reports are hash-reverified without "
        "redundant HOST runs. Historical permission/memory/signing evidence preserved.\n\n"
        "**Next:** separate native execution with fresh device/port/PID ownership, original-session serial "
        "visual confirmations, then combined-main/signing/CI/exact immutable public-ZIP gates before "
        "publication or070. Published coverage remains **95/1,228 additions; 1,133 remain**. Compatible "
        "Android `f9b59a2+` required; physical-phone/general-release and whole-set acceptance outstanding.\n",
        encoding="utf-8")
    print("Signed local checkpoint452 saved with complete live history.")
else:
    raise ValueError(mode)
