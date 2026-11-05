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
LOG = CONTROL / "logs" / "beece005-3965-4ed7-a9b8-c8812b03201d"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-067-native"
SOURCES = ROOT / "docs" / "n1-sources"
HEAD = "a45ce3014661487bf16977260daa5ca23e001663"
REVIEWED = "5cb2ea4bc804ac218b17d5c583d4fba95e60971c"
PRIOR = ROOT / "docs" / "n1-reviews" / "batch-066-native" / "N1Batch066NativeTest.kt"
FIXTURE = FOLDER / "N1Batch067NativeTest.kt"
ARCHIVE = CONTROL / "artifacts" / "n1-batch-067-a45ce301-envelope.zip"
APK = CONTROL / "artifacts" / "n1-batch-067-native-test.apk"
SCOPE = (
    "SAME067 exact full Git archive native fixture preparation, serial compilation and "
    "normally signed local evidence checkpoint only. No native launch, reviewer, runtime "
    "publication,068 or second runner."
)
NEXT = (
    "SAME067: execute compiled control\\artifacts\\n1-batch-067-native-test.apk cases "
    "N1Batch067GlyphTest and N1Batch067ArticleTest against the exact full signed a45ce301 "
    "Git envelope. Read docs\\n1-sources\\execution-434.json and batch-067-native-preparation.json. "
    "Fresh adb/device and 5580/5581 local/remote connection/PID ownership immediately before "
    "launching the established read-only N3_Acceptance_20261029 API35 emulator-5580: "
    "-port5580 -read-only -no-snapshot -no-window -no-audio -gpu host -feature -Vulkan "
    "-memory2048 -cores2. Record owned parent/QEMU; stop only owned helper. Batch040 alternate "
    "routing exception is not inherited. Keep guest/app heaps, font code and archive guards "
    "unchanged; never use HOST-only heap init for native. Full production ContentSync ONCE "
    "must import1079kanji5037words99N1/contentVersion68c767f176e68882/problems0/epoch1. "
    "Check full/curatedソウ and emptyKun in Lite+Full, normalizedそう/noKun log. Require both "
    "terminal case status0/no skips, raw logs, direct PNG inspection: 僧増値倍人亻曽侶 and "
    "僧侶/坊さん across four production families, complete three articles, one mapped "
    "僧-僧侶 reciprocal pair plus both 僧侶-坊さん comparison directions, SystemBack/offline/"
    "N1selection/meaning/sole curatedOnGood/persistedgrade/13reference-stroke touch/"
    "ungradedtrace/recallmiss/persistedDrawAgain. Static selectors and raster hashes do not "
    "establish native semantics/readability/fallback-face identity; trace/recall miss is not "
    "MLKit or human handwriting evidence. Inherit fresh433Android3+1 without redundant Gradle. "
    "After nativePASS use ORIGINAL Claude0d237a1b-fdf8-4ea8-8c5d-03aa6a6d86a0 and "
    "GPTab7f642d-37b9-4069-8a9c-4fc5e6bc071a SERIALly for bounded dependent visual "
    "confirmations with actual supported CLI/read-only tools and scoped control access; "
    "record actual returned images/read-depth/source limits, not fresh blind reviews. "
    "Then combined-latest-main nonrewriting integration/all validation/normal signing/"
    "ownerfastforward/greenCI/exactimmutablepublicZIPruntimehashesandbudgets/ownerissue60 "
    "before publication or068. Preserve historical permission/signing/memory failures; "
    "no workaround, guard increase, concurrent heavy work, second runner or supervisor edits. "
    "Preserve full live history. Published93/1228,remaining1135/latest066f0b318eb;067 local "
    "not delivered. CompatibleAndroidf9b59a2+ required; phone/general-release/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def verify_runtime_unchanged():
    assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", cwd=ANDROID)


mode = sys.argv[1]
if mode == "start":
    request_path = LOG / "request.txt"
    request = request_path.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    checkpoint = json.loads(request.split(marker, 1)[1])
    assert checkpoint["checkpoint"] == 433
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 433 and progress["batch"] == "067"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    verify_runtime_unchanged()
    before = LOG / "execution-434-before-progress.json"
    assert not before.exists()
    save(before, progress)
    record = {
        "execution": 434, "batch": "067", "startingHead": HEAD,
        "androidHead": git("rev-parse", "HEAD", cwd=ANDROID),
        "originMain": git("rev-parse", "origin/main"), "scope": SCOPE,
        "status": "preparing-exact-full-archive-native-fixture",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "authorization": {
            "requestSha256": sha(request_path), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and full embedded checkpoint parsed. Operative contract, complete final433 checkpoint and approved issue inspected directly; historical middle parsed, not freshly semantically re-reviewed.",
        },
    }
    save(LOG / "execution-434-start.json", record)
    progress["execution434StartingState"] = record
    progress["stage"] = "batch-067-native-fixture-preparation-in-progress"
    save(CONTROL / "progress.json", progress)
    print("Recorded434 scope early; full live433 history preserved.")
elif mode == "prepare":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    verify_runtime_unchanged()
    assert not FOLDER.exists() and not ARCHIVE.exists() and not APK.exists()
    manifest = load(ROOT / "manifest.json")
    assert manifest["contentVersion"] == "68c767f176e68882"
    counts = {
        "kanji": sum(name.startswith("kanji/") for name in manifest["files"]),
        "words": sum(name.startswith("words/") for name in manifest["files"]),
        "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                  for p in (ROOT / "kanji").glob("*.md")),
    }
    assert counts == {"kanji": 1079, "words": 5037, "n1": 99}, counts
    text = PRIOR.read_text(encoding="utf-8")
    replacements = (
        ("066", "067"),
        ("colleagueLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
         "buddhistClergyLookalikesAndRadicalVariantsAcrossFourProductionFamilies"),
        ("fullSingleImportOfflineColleagueTwoReciprocalPairsOnOnlyDrawingAndSystemBack",
         "fullSingleImportOfflineBuddhistClergyReciprocalComparisonOnOnlyDrawingAndSystemBack"),
        ("175fdf3f1605f231e27a9de19a7c18c4a02cb20d", HEAD), ("175fdf3f", HEAD[:8]),
        ("a9ecc100b6c1335c", manifest["contentVersion"]),
        ("1078", "1079"), ("5036", "5037"), ("98, n1.size", "99, n1.size"),
        ("N1 · 98 cards", "N1 · 99 cards"),
        ('"僚 療 像 値 人 亻 疒 同 口 同僚"', '"僧 増 値 倍 人 亻 曽 侶 僧侶 坊さん"'),
        ('listOf("僚", "療", "像", "値", "人", "亻", "疒", "同", "口")',
         'listOf("僧", "増", "値", "倍", "人", "亻", "曽", "侶")'),
        ('listOf("同僚")', 'listOf("僧侶", "坊さん")'),
        ("Batch 067: colleague / look-alikes / radical variants",
         "Batch 067: Buddhist clergy / look-alikes / radical variants"),
        ("Compare 僚 with 療, 像 and 値. Inspect 人 versus 亻 and the illness frame 疒; also inspect 同, 口 and the word 同僚. Shared fallback need not give four different designs.",
         "Compare 僧 with 増, 値 and 倍. Inspect 人 versus 亻, the right-hand 曽 and the support character 侶; also inspect 僧侶 and 坊さん. Shared fallback need not give four different designs."),
        ('.put("individualGlyphProbes", 36).put("wholeWordRasterProbes", 4)',
         '.put("individualGlyphProbes", 32).put("wholeWordRasterProbes", 8)'),
        ("Thirty-six single-character native Paint probes including actual 人/亻 and standalone 疒, four complete-word nonblank raster probes and four production Compose rows; actual 僚/療/像/値/人/亻/疒/同/口/同僚 readability requires separate visual inspection.",
         "Thirty-two single-character native Paint probes including actual 人/亻 and standalone 曽/侶, eight complete-word nonblank raster probes and four production Compose rows; actual 僧/増/値/倍/人/亻/曽/侶/僧侶/坊さん readability requires separate visual inspection."),
        ("colleague", "clergy"), ('"僚"', '"僧"'),
        ('listOf("リョウ")', 'listOf("ソウ")'), ('listOf("りょう")', 'listOf("そう")'),
        ('key == "りょう"', 'key == "そう"'), ('val key = "りょう"', 'val key = "そう"'),
        ('click("clergy")', 'click("Buddhist monk; priest")'),
        ('await("clergy")', 'await("Buddhist monk; priest")'),
        ('assertEquals(14, strokes.length())', 'assertEquals(13, strokes.length())'),
        ('"14 strokes drawn"', '"13 strokes drawn"'),
        ("Other N1 meanings/readings postponed; 僚 meaning and sole curated on key due; explicit no-kun. Two historical good 僚 meaning logs unlock drawing.",
         "Other N1 meanings/readings postponed; 僧 meaning and sole curated on key due; explicit no-kun. Two historical good 僧 meaning logs unlock drawing."),
    )
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    route = r'''            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("僧")
            click("Buddhist monk; priest")
            await("Article contents")
            await("as 亻, no. 9)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("僧 usually refers to a Buddhist monk or priest.", "kanji-meaning")
            show("The visible parts are 亻", "kanji-components")
            show("Modern-shape mnemonic:", "kanji-mnemonic")
            section("Readings")
            show(readingExample("僧侶 そうりょ — Buddhist priest; monk"), "kanji-on-reading")
            show("The frozen character dictionary gives ソウ and no kun reading.", "kanji-compound-reading-boundary")
            section("Notes")
            show(articleBullet("僧 そう can also abbreviate the Buddhist community, or sangha, in religious usage. The context distinguishes this collective sense from an individual monk."), "kanji-collective-sense")
            show(articleBullet("The English gloss \"priest\" does not make 僧 a general translation for clergy of every religion. Compounds can have wider uses; learn the whole word."), "kanji-religious-scope")
            show(articleBullet("増, \"increase,\" has 土 on the left instead of 亻. 値, \"value; price,\" and 倍, \"multiple; double,\" share 亻 but have different right-hand shapes."), "kanji-lookalikes")
            section("Common words")
            show(articleBullet("高僧 こうそう — a high-ranking or highly respected Buddhist priest"), "kanji-common-high-priest")
            inline(await(articleBullet("僧侶 そうりょ — Buddhist priest; monk")), "僧侶")
            await("僧侶 (そうりょ) - Buddhist priest; monk")
            section("Meaning")
            show("僧侶 is a Buddhist priest or monk.", "clergy-meaning")
            show(articleBullet("彼は僧侶です。 (かれはそうりょです。) - He is a Buddhist priest."), "clergy-person-example")
            show(articleBullet("お寺で僧侶の話を聞きました。 (おてらでそうりょのはなしをききました。) - I listened to a Buddhist priest's talk at the temple."), "clergy-temple-example")
            section("How the kanji combine")
            show("僧 ソウ supplies the Buddhist monk or priest meaning;", "clergy-reading-allocation")
            inline(await("僧 ソウ supplies the Buddhist monk or priest meaning;", substring = true), "僧")
            await("Article contents")
            section("Readings")
            show(readingExample("僧侶 そうりょ — Buddhist priest; monk"), "clergy-kanji-backlink")
            back()
            await("僧 ソウ supplies the Buddhist monk or priest meaning;", substring = true).assertIsDisplayed()
            capture("system-back-clergy-kanji")
            section("Synonyms and antonyms")
            show("坊さん (ぼうさん), also お坊さん (おぼうさん),", "clergy-register-comparison")
            show("神父 (しんぷ), a Catholic priest,", "clergy-catholic-boundary")
            inline(await("坊さん (ぼうさん), also お坊さん (おぼうさん),", substring = true), "坊さん")
            await("坊さん (ぼうさん) - Buddhist priest; monk")
            section("Meaning")
            show("坊さん is a familiar, respectful way of referring to a Buddhist priest or monk.", "bousan-meaning")
            show(articleBullet("お寺で坊さんの話を聞きました。 (おてらでぼうさんのはなしをききました。) - I listened to a Buddhist priest's talk at the temple."), "bousan-temple-example")
            show(articleBullet("お坊さんに道を尋ねました。 (おぼうさんにみちをたずねました。) - I asked a Buddhist priest for directions."), "bousan-directions-example")
            section("How the kanji combine")
            show("坊 contributes ボウ; さん is the familiar honorific suffix, not another kanji.", "bousan-formation")
            section("Distinctive meaning")
            show("坊さん also has a familiar \"boy\" sense.", "bousan-boy-boundary")
            section("Synonyms and antonyms")
            show("僧侶 (そうりょ) is a more formal Buddhist-clergy term.", "bousan-changed-comparison")
            inline(await("僧侶 (そうりょ) is a more formal Buddhist-clergy term.", substring = true), "僧侶")
            await("僧侶 (そうりょ) - Buddhist priest; monk")
            section("How the kanji combine")
            show("僧 ソウ supplies the Buddhist monk or priest meaning;", "bousan-clergy-backlink")
            back()
            await("僧侶 (そうりょ) is a more formal Buddhist-clergy term.", substring = true).assertIsDisplayed()
            capture("system-back-bousan-clergy")
            back()
            await("坊さん (ぼうさん), also お坊さん (おぼうさん),", substring = true).assertIsDisplayed()
            capture("system-back-clergy-bousan")
            section("Distinctive meaning")
            show("Use 僧侶 for the religious person,", "clergy-person-temple-boundary")
            back()
            await("Common words")
'''
    start = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', start)
    text = text[:start] + route + text[end:]
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for obsolete in ("066", "僚", "同僚", "リョウ", "りょう", "colleague"):
        assert obsolete not in text, obsolete
    assert text.count('listOf("ソウ")') == 4
    prior_generator = PRIOR.parent / "preparation-receipts" / "prepare-426-native.py"
    parsed = ast.parse(prior_generator.read_text(encoding="utf-8"))
    reusable = ast.Module(body=[node for node in parsed.body if isinstance(node, ast.FunctionDef)
                               and node.name in ("plain", "blocks")], type_ignores=[])
    namespace = {"re": re}
    exec(compile(reusable, str(prior_generator), "exec"), namespace)
    documents = {name: namespace["blocks"](ROOT / name)
                 for name in ("kanji/僧.md", "words/僧侶.md", "words/坊さん.md")}
    stack, selectors, controls, transitions = ["kanji/僧.md"], [], [], []
    quoted = r'"((?:\\.|[^"\\])*)"'
    for number, line in enumerate(route.splitlines(), 1):
        document = stack[-1]
        shown = re.search(r'show\((?:(readingExample|articleBullet)\()?' + quoted + r'\)?, "([^"]+)"\)', line)
        section = re.search(r'section\("([^"]+)"\)', line)
        awaited = re.search(r'await\((?:(readingExample|articleBullet)\()?' + quoted + r'(?:, substring = (true|false))?', line)
        if shown:
            qualifier, target, step = shown.groups()
            operation, substring = "show", qualifier is None
        elif section:
            qualifier, target, step = "heading", section.group(1), None
            operation, substring = "section", False
        elif awaited:
            qualifier, target, sub = awaited.groups()
            operation, substring, step = "await", sub == "true", None
        else:
            if line.strip() == "back()":
                assert len(stack) > 1
                stack.pop()
            elif re.fullmatch(r'\s*capture\("[^"]+"\)', line):
                pass
            elif line.strip() in ('click("Browse all kanji")', 'click("Buddhist monk; priest")') or "performTextReplacement" in line:
                pass
            else:
                raise AssertionError(line)
            continue
        target = target.replace('\\"', '"')
        if target in ("Article contents", "Common words") and operation == "await":
            controls.append({"routeLine": number, "target": target})
        else:
            matches = [(kind, value) for kind, value in documents[document]
                       if (target in value if substring else target == value)
                       and (qualifier != "heading" or kind == "heading")
                       and (qualifier != "readingExample" or kind == "table")
                       and (qualifier != "articleBullet" or kind != "table")]
            assert len(matches) == 1, (number, document, target, matches)
            selectors.append({"routeLine": number, "document": document, "operation": operation,
                              "target": target, "substring": substring, "qualifier": qualifier,
                              "step": step, "matches": matches})
        if "inline(await" in line:
            label = re.search(r', "([^"]+)"\)$', line).group(1)
            links = re.findall(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", (ROOT / document).read_text(encoding="utf-8"))
            destinations = {posixpath.normpath(posixpath.join(posixpath.dirname(document), link))
                            for link in links if not link.startswith("https://")}
            assert len(destinations) == 1, (document, label, destinations)
            destination = destinations.pop()
            assert destination in documents
            transitions.append([document, destination])
            stack.append(destination)
    assert stack == ["kanji/僧.md"]
    expected = {("kanji/僧.md", "words/僧侶.md"), ("words/僧侶.md", "kanji/僧.md"),
                ("words/僧侶.md", "words/坊さん.md"), ("words/坊さん.md", "words/僧侶.md")}
    assert len(transitions) == 4 and {tuple(item) for item in transitions} == expected
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-067/",
                    f"--output={ARCHIVE}", HEAD], cwd=ROOT, check=True)
    with zipfile.ZipFile(ARCHIVE) as zipped:
        names = zipped.namelist()
        prefix = "n1-batch-067/"
        assert len(names) == len(set(names)) and len(names) <= 18000
        assert all(name.startswith(prefix) and "\\" not in name
                   and ".." not in name.split("/") for name in names)
        manifest_bytes = zipped.read(prefix + "manifest.json")
        assert manifest_bytes == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=ROOT)
        assert json.loads(manifest_bytes) == manifest
        assert (manifest["schemaVersion"], manifest["baseLanguage"], manifest["targetLanguage"]) == (1, "en", "ja")
        retained, verified = len(manifest_bytes), 0
        binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, expected_hash in entries.items():
                data = zipped.read(prefix + name)
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit, name
                normalized = data if section in binary else data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(normalized).hexdigest() == expected_hash, name
                retained += len(data)
                verified += 1
        inflated = sum(info.file_size for info in zipped.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in name or "/tools/" in name for name in names)
    assert verified == 8329
    FOLDER.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-066.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(ROOT).as_posix(), tofile=FIXTURE.relative_to(ROOT).as_posix(), n=0)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 434, "batch": "067",
        "status": "static-native-preparation-verified-not-executed",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "contentSnapshot": HEAD,
        "reviewedTeachingSnapshot": REVIEWED,
        "androidSnapshot": git("rev-parse", "HEAD", cwd=ANDROID),
        "contentVersion": manifest["contentVersion"], "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(names),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated,
        "retainedBytes": retained, "verifiedRuntimeHashes": verified, "manifestEqual": True,
        "safePathsPerFileAndOriginalPublishingBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "reusedAcceptedHarness": str(PRIOR.relative_to(ROOT)), "reusedAcceptedHarnessSha256": sha(PRIOR),
        "staticProjectionHelper": str(prior_generator.relative_to(ROOT)), "staticProjectionHelperSha256": sha(prior_generator),
        "fixtureDiff": str(diff.relative_to(ROOT)), "fixtureDiffSha256": sha(diff),
        "originalInitialReportHashesUnchanged": {
            f"docs/n1-reviews/batch-067-initial-{family}.md":
            sha(ROOT / "docs" / "n1-reviews" / f"batch-067-initial-{family}.md")
            for family in ("claude", "gpt")
        },
        "articleFiles": [{"path": name, "sha256": sha(ROOT / name), "projectedTextBlocks": len(items)}
                         for name, items in documents.items()],
        "staticMarkdownSelectors": selectors, "renderedNavigationControls": controls,
        "articleRouteTransitions": transitions,
        "captureSteps": len(re.findall(r'(?:show\([^\n]+, |capture\()"([^"]+)"\)', route)),
        "plannedNativePaintProbes": 32, "plannedWholeWordRasterProbes": 8,
        "plannedGlyphs": ["僧", "増", "値", "倍", "人", "亻", "曽", "侶"],
        "plannedWholeWords": ["僧侶", "坊さん"],
        "fullReadings": {"on": ["ソウ"], "kun": []}, "curatedReadings": {"on": ["ソウ"], "kun": []},
        "normalizedQuizKeys": {"on": ["そう"], "kun": []},
        "reciprocalPairs": [["僧", "僧侶"]], "comparisonPairs": [["僧侶", "坊さん"]],
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "accepted433AndroidRetainedWithoutRerun": True, "nativeExecuted": False,
        "independentVisualAcceptance": False, "phoneEvidence": False,
        "publicationAttempted": False, "runtimeEdited": False, "hostTestInitScriptUsed": False,
        "projectionQualification": "Bounded heading/paragraph/bullet/table projection reused unchanged from accepted066. Static selectors establish matching text and relative link destinations, not native semantics, viewport readability or visual acceptance.",
        "limits": "Preparation only. Exact full Git envelope and production ContentSync ONCE with unchanged guards. One mapped reciprocal pair and one comparison pair, each in both directions; complete three articles, selection/meaning/sole curated On/no Kun/13-stroke trace and recall planned, not executed. Paint hashes do not establish readable glyphs or fallback-face identity. Reference trace/recall miss do not establish human handwriting or MLKit recognition. Fresh device/port ownership required before separate native execution. Historical permission failures and HOST-only memory qualification remain intact; HOST init not for native builds. No native/reviewer/publication/068/second runner. Published93/1228,1135remain; phone/general-release/whole-set outstanding.",
    }
    save(CONTROL / "batch-067-native-fixture-verification.json", record)
    print(json.dumps({key: record[key] for key in ("status", "contentVersion", "expectedCounts",
          "archiveSha256", "zipEntries", "compressedBytes", "inflatedBytes", "retainedBytes",
          "verifiedRuntimeHashes", "fixtureSha256", "captureSteps")}, indent=2))
    print("Article selectors:", len(selectors), "Directed transitions:", len(transitions))
elif mode == "archive":
    assert git("rev-parse", "HEAD") == HEAD
    verify_runtime_unchanged()
    preparation = load(CONTROL / "batch-067-native-fixture-verification.json")
    assert sha(FIXTURE) == preparation["fixtureSha256"]
    assert sha(ARCHIVE) == preparation["archiveSha256"]
    raw_log = LOG / "native-compile.txt"
    compile_text = raw_log.read_text(encoding="utf-8-sig")
    assert (LOG / "native-compile-exit.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in compile_text
    with zipfile.ZipFile(APK) as package:
        assert hashlib.sha256(package.read("assets/" + ARCHIVE.name)).hexdigest() == preparation["archiveSha256"]
        dex = [package.read(name) for name in package.namelist() if re.fullmatch(r"classes\d*\.dex", name)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch067{kind}Test;".encode() in blob for blob in dex)
            for old in ("064", "065", "066"):
                assert all(f"Lio/github/stopcran/kanji/ui/N1Batch{old}{kind}Test;".encode() not in blob for blob in dex)
        for method in (
            "buddhistClergyLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
            "fullSingleImportOfflineBuddhistClergyReciprocalComparisonOnOnlyDrawingAndSystemBack",
        ):
            assert any(method.encode() in blob for blob in dex)
    (FOLDER / "compile.txt").write_text("\n".join(line.rstrip() for line in compile_text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    assert gzip.decompress((FOLDER / "compile-raw.txt.gz").read_bytes()) == raw_log.read_bytes()
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    shutil.copyfile(Path(__file__), receipts / "execution-434.py")
    shutil.copyfile(CONTROL / "run-434-native-compile.ps1", receipts / "run-434-native-compile.ps1")
    save(SOURCES / "batch-067-native-preparation.json", preparation)
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 68c767f176e68882")):
        source = LOG / f"{name}.txt"
        assert expected in source.read_text(encoding="utf-8-sig")
        target = FOLDER / f"{name}.txt"
        target.write_text("\n".join(line.rstrip() for line in source.read_text(encoding="utf-8-sig").splitlines()) + "\n", encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(ROOT)), "sha256": sha(target)})
    inherited = load(SOURCES / "execution-433.json")
    for item in inherited["tests"]:
        assert sha(ROOT / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == 0
    reconciliation = load(ROOT / "docs" / "n1-reviews" / "batch-067-reconciliation.json")
    reports = preparation["originalInitialReportHashesUnchanged"]
    for process in reconciliation["processes"].values():
        path = ROOT / "docs" / "n1-reviews" / process["report"]
        assert sha(path) == process["reportSha256"] == reports[path.relative_to(ROOT).as_posix()]
    record = {
        "schemaVersion": 1, "execution": 434, "batch": "067",
        "status": "native-compiled-pending-execution", "startingHead": HEAD,
        "reviewedTeachingSnapshot": REVIEWED, "scope": SCOPE,
        "authorization": load(LOG / "execution-434-start.json")["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": str((SOURCES / "batch-067-native-preparation.json").relative_to(ROOT)),
        "preparationSha256": sha(SOURCES / "batch-067-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "status": "compiled-not-executed", "exitCode": 0,
            "result": re.search(r"BUILD SUCCESSFUL in (.+)", compile_text).group(0),
            "tasks": re.search(r"\d+ actionable tasks: .+", compile_text).group(0),
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "log": str((FOLDER / "compile.txt").relative_to(ROOT)), "logSha256": sha(FOLDER / "compile.txt"),
            "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "rawLogArchive": str((FOLDER / "compile-raw.txt.gz").relative_to(ROOT)),
            "normalization": "Readable log UTF-8 LF/trailing whitespace removed; deterministic gzip retains exact raw bytes.",
            "apk": str(APK), "apkSha256": sha(APK), "apkBytes": APK.stat().st_size,
            "packagedExactFullArchiveVerified": True, "bothSelectedClassDescriptorsAndMethodsPresent": True,
            "oldBatch064065066DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False, "nativeOrEmulatorStarted": False,
            "JAVA_HOME": "C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": "C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk",
        },
        "checks": checks, "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE),
        "selectorAudit": {
            "completeArticleSelectors": len(preparation["staticMarkdownSelectors"]),
            "articleCaptureSteps": preparation["captureSteps"], "reciprocalPairs": 1,
            "comparisonPairs": 1, "directedTransitions": 4,
            "method": preparation["projectionQualification"],
        },
        "accepted433AndroidRetainedWithoutRerun": True,
        "inherited433ArchivedXmlHashesReverified": True, "originalReportHashesUnchanged": reports,
        "originalReviewerSessionsForLaterDependentVisualConfirmation": [
            {"family": family, "sessionId": process["sessionId"], "requestedModel": process["requestedModel"]}
            for family, process in reconciliation["processes"].items()
        ],
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
        "publishedAdditions": 93, "remainingAdditions": 1135, "nextAction": NEXT,
        "limits": preparation["limits"],
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(FOLDER.rglob("*")) + [SOURCES / "batch-067-native-preparation.json"] if path.is_file()
    ]
    save(SOURCES / "execution-434.json", record)
    print("Exact packaged archive/classes verified; original reviews and fresh433Android unchanged.")
elif mode == "checkpoint":
    record = load(SOURCES / "execution-434.json")
    verify_runtime_unchanged()
    for item in record["artifacts"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    assert not git("status", "--porcelain")
    commit = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G" and git("rev-parse", "HEAD^") == HEAD
    progress = load(CONTROL / "progress.json")
    before = load(LOG / "execution-434-before-progress.json")
    assert progress["checkpoint"] == 433 and progress["batch"] == "067"
    for key, value in before.items():
        if key != "stage":
            assert progress[key] == value, key
    checkpoint = {
        "execution": 434, "checkpoint": 434, "batch": "067", "savedCommit": commit, "signature": "G",
        "record": "docs\\n1-sources\\execution-434.json", "recordSha256": sha(SOURCES / "execution-434.json"),
        "status": "continue", "runtimePublished": False, "nativeExecuted": False,
        "allOriginalHistoricalKeysPreservedExactly": True, "dedicatedWorktreesClean": True,
        "nextAction": NEXT,
    }
    progress.update(checkpoint=434, status="continue", stage="batch-067-native-compiled-pending-execution",
                    nextAction=NEXT, blocker=None)
    progress["execution434StartingState"]["status"] = "signed-native-preparation-checkpoint-complete"
    progress["batch067NativePreparationCheckpoint"] = checkpoint
    progress["execution434CoordinatorCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", progress)
    save(LOG / "execution-434-checkpoint.json", checkpoint)
    (LOG / "issue-body.txt").write_text(
        f"Batch 067 native-preparation checkpoint **434** saved locally at `{commit}` (normal signature G); no runtime publication.\n\n"
        "The exact full `a45ce301` Git archive (version `68c767f176e68882`, 1,079 kanji / 5,037 words / 99 N1 cards) "
        "passes every runtime hash (8,329) and original archive budgets. "
        "The fixture compiles with one worker and no HOST-only heap init; the APK contains the exact archive "
        "and both selected cases. Temporary Android source/assets were removed; its worktree is clean. "
        "Validator passes and the manifest is unchanged.\n\n"
        f"{record['selectorAudit']['completeArticleSelectors']} static article selectors and "
        f"{record['selectorAudit']['articleCaptureSteps']} article captures are planned, with four directed routes: "
        "僧–僧侶 reciprocal links and 僧侶–坊さん comparisons. Sole curated ソウ, thirteen-stroke trace/recall, "
        "32 glyph and eight whole-word raster probes (including 亻/曽/侶) are prepared, not executed. "
        "No native/visual/phone acceptance is claimed. Fresh checkpoint-433 Android evidence and both "
        "original review reports remain unchanged. Historical permission/memory failures remain retained; "
        "guest/app heaps, production guards and teaching are unchanged.\n\n"
        "**Next:** separate native execution with fresh device/port ownership, then original-session serial "
        "visual confirmations and combined-main/signing/CI/immutable-public-ZIP gates before publication or 068. "
        "Published coverage remains **93/1,228 additions; 1,135 remain**. Compatible Android `f9b59a2+` is "
        "required; physical-phone/general-release and whole-set acceptance remain outstanding.\n", encoding="utf-8")
    print("Signed local checkpoint434 persisted; full live history preserved.")
else:
    raise ValueError(mode)
