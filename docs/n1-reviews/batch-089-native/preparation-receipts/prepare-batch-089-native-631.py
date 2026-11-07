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
L = C / "logs" / "47416279-ac73-401c-86e6-00af4522b763"
HEAD = "72614eda48aa8752d9401540d63a479467948d10"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "c6562f11cb371053"
WORK = C / "batch-089-native-631"
FIXTURE = WORK / "N1Batch089NativeTest.kt"
PRIOR = R / "docs" / "n1-reviews" / "batch-088-native" / "N1Batch088NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-089-72614eda-envelope.zip"
VERIFICATION = C / "batch-089-native-fixture-verification.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-089-native"
BEFORE = L / "progress-before-631.json"
NEXT = (
    "SAME089 execute compiled native fixture and inspect actual PNGs; preparation631 is NOT native acceptance. "
    "Read docs/n1-sources/execution-631.json and control/batch-089-native-fixture-verification.json. "
    "Require N1Batch089GlyphTest AND N1Batch089ArticleTest terminal per-case0, no skips/errors. "
    "Full git archive72614eda/versionc6562f11cb371053/8426runtimehashes through productionContentSync ONCE: "
    "1112kanji/5068words/121N1/zeroProblems/acceptedRoomversion+readingepoch1. "
    "Inspect all23scopedHan especially U+4E42/U+51F5 across fourproductionfamilies/systemfallback, "
    "92individual+4wholewordrasters and3Composepanels. Cmaps/hasGlyph/hashes are NOT legibility/face evidence. "
    "Actual N1/All production choices must be exactly illfortune;evil plus 凡commonplace;mediocre, "
    "凸convex;protruding, 凹concave;sunken; allthreeN1available/no fallback. "
    "Singlequeuedonkeyきょう persistedGood/done, rawkun[]/explicitquizkun[]; own linked凶作 row. "
    "Fourstroke injectedtrace/recall/persistence, BOTHcompletearticles plus ONLYchanged作navigationline, "
    "twoallmappedpairs/fourdirections/onedirect収穫wordguard, SystemBack/offline/N1selection/meaning/reading/drawing. "
    "Agriculturalnoun/verypooryield not harvestverb/necessaryzeroyield/famine/badwork; compound-specific作crop/yield. "
    "Injectedtrace/giveup is NOT humanhandwriting/MLKit/phone. Freshdevice/PID/local+remote5580/5581ownership "
    "immediately before ownedreadonlyAPI35 N3_Acceptance_20261029 emulator-5580 hostGPU/-Vulkan/2048MiB/2cores; "
    "stop only ownedhelper. No guest/appheap/guardincrease, productionappchange,090 or runtimepublication. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains unchangedproductionf9b59a2, not latestappmain. "
    "Original textualsnapshot4b84608b closed across Claudea56b5dcb-9fed-4785-848e-41708f65598f and "
    "GPT3286add7-2824-4df6-933a-c8bba3890927; GPT redundant/truncatedtailread limits preserved. "
    "Serial original-session dependentvisualconfirmations remain, no newblindcredit. "
    "Parent19008 ownsrunner.lock: verifyliveancestry/session/checkpoint/exactsignedheads/whollycleanworktrees; "
    "NOchildlockacquisition/delete/unlock. Approvedcontrol/committedsources only, not optionalhistoricalsessionrecipes. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Alloriginalsource/baseline/link/reading/"
    "twofamily/native/currentmainnormalmerge/changedteachingindependentreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalCI/EVERYimmutablepublicZIPruntimehash/original18000entries/42MiBcompressed/"
    "80MiBinflated/56MiBretained/perfile-media-safepath/ownerissue gates remain. "
    "Published115/1228,1113remaining unchanged; physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root), str(root)
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)


def persist(state):
    temp = C / "progress.631.tmp"
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
                actual = sha(path) if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(path)
                assert actual == digest, name
                count += 1
    assert count == 8426
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-089-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    for name, digest in reconciliation["reviewedRuntimeHashes"].items():
        assert sha(R.joinpath(*name.split("/"))) == digest, name
    return manifest


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        630, "continue", "fresh-android-passed-awaiting-native", "089")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    role = load(L / "native-runner-role.json")
    assert role["parentAncestryVerified"] and role["launcherCommandMatches"] and not role["parentLockAccessAttempted"]
    assert not BEFORE.exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 630 and checkpoint["execution630CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(BEFORE, state)
    state["execution631StartingState"] = {
        "execution": 631, "batch": "089", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME089 full native fixture/archive preparation and compilation, signed LOCAL evidence; yield before native execution/visual review/publication/090.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/JSON decoded; operative contract, complete approved issue and final630 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry and exact runner session; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-089-native-preparation-in-progress"
    state["nextAction"] = state["execution631StartingState"]["scope"]
    persist(state)
    print("Starting631 persisted; full live history retained.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert sha(PRIOR) == "ce3837f4fb70d35f4b5875de6e149cc44e02959c81985471733573e7b0036c25"
    utility = C / "prepare-batch-085-native.py"
    assert sha(utility) == "d9516213531d78dcfd25df8f9fb6057597676e1705f7d70a211021be92a28c24"
    spec = importlib.util.spec_from_file_location("native_markdown_utilities", utility)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    quote, plain, blocks = helper.quote, helper.plain, helper.blocks
    names = ["kanji/凶.md", "words/凶作.md"]
    docs = {name: blocks(R.joinpath(*name.split("/"))) for name in names + ["kanji/作.md"]}
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def show(document, kind, value, step):
        assert sum(v == value for k, v in docs[document]
                   if (k == "table") == (kind == "table") and k != "heading") == 1, (document, value)
        selector = "readingExample" if kind == "table" else "articleBullet"
        line(f"show({selector}({quote(value)}), {quote(step)})")
        selectors.append({"document": document, "kind": kind, "target": value, "step": step})

    def display(document, slug):
        line(f"await({quote(docs[document][0][1])})")
        cell = 0
        for index, (kind, value) in enumerate(docs[document][1:], 1):
            if kind == "heading":
                line(f"section({quote(value)})")
            elif kind == "table":
                cell += 1
                if cell > 3 and cell % 3 != 2:
                    show(document, kind, value, f"{slug}-{index:02}")
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
                        if (R / document).parent.joinpath(match[1]).resolve() == (R / destination).resolve():
                            candidates.append(part.removeprefix("- "))
        assert len(candidates) == 1, (document, label, candidates)
        raw = candidates[0]
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        rendered = plain(" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_631" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_631")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("凶")')
    line('click("ill fortune; evil")')
    display("kanji/凶.md", "kanji")
    forward = follow("kanji/凶.md", "凶作", "words/凶作.md", "Common words", "harvest-forward")
    display("words/凶作.md", "harvest")
    reverse = follow("words/凶作.md", "凶", "kanji/凶.md", "How the kanji combine", "harvest-reverse")
    line('section("Readings")')
    line('show(readingExample("キョウ"), "harvest-kanji-backlink")')
    back_to(reverse, "harvest-system-back-to-word")
    reused = follow("words/凶作.md", "作", "kanji/作.md", "How the kanji combine", "crop-head-forward")
    line('await("作 — make, produce")')
    reused_reverse = follow("kanji/作.md", "凶作", "words/凶作.md", "Common words", "crop-head-reverse")
    line('await("凶作 (きょうさく) — poor harvest; crop failure")')
    back_to(reused_reverse, "crop-head-system-back-to-kanji")
    back_to(reused, "crop-head-system-back-to-word")
    back_to(forward, "harvest-system-back-to-kanji")
    assert len(offsets) == 4 and len({(x["document"], x["destination"]) for x in offsets}) == 4
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    replacements = [
        ("N1Batch088", "N1Batch089"), ("disposable088", "disposable089"), ("n1-088", "n1-089"),
        ("Batch 088", "Batch 089"), ("n1-batch-088-e445d826-envelope.zip", ARCHIVE.name),
        ("e445d826118681e1df9687eb53d144eed7d66139", HEAD), ("afff40af0e155dbe", VERSION),
        ("1111, updated.kanji", "1112, updated.kanji"), ("5067, updated.words", "5068, updated.words"),
        ("120, n1.size", "121, n1.size"), ("N1 · 120 cards", "N1 · 121 cards"),
        ("triumphLookalikesAndRadicalFallbacks", "illFortuneLookalikesAndRadicalFallbacks"),
        ("fullSingleImportOfflineTriumphOneReciprocalPairOneOnKeyNoKunDrawingAndSystemBack",
         "fullSingleImportOfflineIllFortuneTwoReciprocalPairsOneOnKeyNoKunDrawingAndSystemBack"),
        ("val triumph =", "val illFortune ="), ("triumph.", "illFortune."),
        ('"凱"', '"凶"'), ("victory song; triumph", "ill fortune; evil"),
        ('listOf("ガイ", "カイ")', 'listOf("キョウ")'),
        ('listOf("かちどき", "やわらぐ")', "emptyList<String>()"),
        ('listOf("ガイ")', 'listOf("キョウ")'), ('listOf("がい")', 'listOf("きょう")'),
        ('setOf("がい")', 'setOf("きょう")'),
        ('put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2)',
         'put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)'),
        ('put("changedReusedArticles", 0)', 'put("changedReusedArticles", 1)'),
        ("assertEquals(12, strokes.length())", "assertEquals(4, strokes.length())"),
        ('hasContentDescription("12 strokes drawn"', 'hasContentDescription("4 strokes drawn"'),
        ("kotlin.random.Random(622)", "kotlin.random.Random(631)"),
        ("importedReturn", "importedHarvest"), ('"凱旋"', '"凶作"'),
        ('listOf("帰る", "帰宅", "帰り", "戻る")', 'listOf("収穫")'),
        ('"がいせん"', '"きょうさく"'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 凶 meaning and exactly onきょう due; source kun[] and explicit quizKun[] give no questions. Two historical good 凶 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    audit = load(R / "docs" / "n1-sources" / "batch-089-draft-font-audit.json")
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "".join(
        R.joinpath(*name.split("/")).read_text(encoding="utf-8") for name in names))))
    assert glyphs == audit["actualHan"] and len(glyphs) == 23
    words = ["凶作"]
    pages = [" ".join(glyphs[:12]), " ".join(glyphs[12:]), "凶 乂 凵 凡 凸 凹 作 悪 米 凶作"]
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", "for (word in listOf(" + ", ".join(map(quote, words)) + "))", text, count=1)
    text = text.replace("triumph / look-alikes / radical fallback", "ill fortune / look-alikes / radical fallback")
    text = text.replace("all 27 scoped Han; focused 凱/凡/凸/凹 and 几/豈/鬨", "all 23 scoped Han; focused 凶/凡/凸/凹 and 乂/凵")
    text = text.replace("27 actual scoped Han including exact 几/豈/鬨 fallback inspection", "23 actual scoped Han including exact 乂/凵 fallback inspection")
    text = text.replace("assertEquals(112, rows.length())", "assertEquals(96, rows.length())")
    text = text.replace('put("individualGlyphProbes", 108)', 'put("individualGlyphProbes", 92)')
    text = text.replace("assertEquals(4, meaning.options.size)",
                        "assertEquals(4, meaning.options.size)\n            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ["088", "triumph", "凱", '"がい"', "ガイ", "カイ", "かちどき", "やわらぐ", "12 strokes"]:
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    from fontTools.ttLib import TTFont
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["乂", "凵"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1112, "words": 5068, "n1": 121}
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-089/", f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-089/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-089/manifest.json")
        assert raw == (R / "manifest.json").read_bytes() and json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if isinstance(group, dict):
                for name, digest in group.items():
                    data = archive.read("n1-batch-089/" + name)
                    limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                        512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8426 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-088.diff"
    diff.write_text("".join(difflib.unified_diff(PRIOR.read_text(encoding="utf-8").splitlines(keepends=True),
        text.splitlines(keepends=True), fromfile=PRIOR.relative_to(R).as_posix(), tofile=FIXTURE.name, n=2)), encoding="utf-8")
    save(VERIFICATION, {
        "schemaVersion": 1, "execution": 631, "batch": "089", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": "4b84608b5ca8889d45a176667975524f6645bd8d",
        "androidSnapshot": APP, "productionBaseline": PROD, "contentVersion": VERSION, "expectedCounts": counts,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "durableUtilityRecipe": str(utility), "durableUtilityRecipeSha256": sha(utility),
        "fixtureDiff": str(diff), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 2, "changedReusedScope": audit["navigationOnlyReusedScope"],
        "mappedReciprocalPairs": 2, "mappedDirectedTransitions": 4,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "plannedNativePaintProbes": 92, "plannedWholeWordRasterProbes": 4, "currentFontAudit": fonts,
        "fullReadings": {"on": ["キョウ"], "kun": []}, "curatedReadings": {"on": ["キョウ"], "kun": []},
        "normalizedQuizKeys": {"on": ["きょう"], "kun": []}, "directWordExclusionPairs": 1,
        "pendingCmapAbsences": ["乂", "凵"], "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False,
        "limits": "Preparation only. Static selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Exact N1/All choices required; three curated wrong cards available, no fallback needed. Full productionContentSync ONCE. Injectedtrace/giveup not human handwriting/MLKit/phone. All original source/reviewer/denial/OOM/phone limits and production heaps/guards retained.",
    })
    print("Prepared frozen089 fixture and full archive; all8426 runtime hashes verified.")


def record():
    clean()
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(L / "native-compile-command.json")
    assert command["parentAncestryVerified"] and not command["parentLockAccessAttempted"]
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-089-native-test.apk"
    app = C / "artifacts" / "n1-batch-089-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ["N1Batch089GlyphTest", "N1Batch089ArticleTest",
                     "fullSingleImportOfflineIllFortuneTwoReciprocalPairsOneOnKeyNoKunDrawingAndSystemBack"]:
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    shutil.copytree(WORK, FOLDER)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-631-native-compile.ps1", VERIFICATION,
               C / "prepare-batch-085-native.py", L / "native-runner-role.json",
               C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt",
               *[L / n for n in ["native-compile-command.json", "native-compile-start.txt",
                                 "native-compile-end.txt", "native-compile-exit.txt"]]]
    provenance = []
    for source in sources:
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    zipped = receipts / "native-compile.txt.gz"
    with zipped.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as compressor:
            compressor.write((L / "native-compile.txt").read_bytes())
    assert gzip.decompress(zipped.read_bytes()) == (L / "native-compile.txt").read_bytes()
    provenance.append({"archive": zipped.relative_to(R).as_posix(), "sha256": sha(zipped),
                       "sourceSha256": sha(L / "native-compile.txt"), "losslessGzipVerified": True})
    save(R / "docs" / "n1-sources" / "execution-631.json", {
        "schemaVersion": 1, "execution": 631, "batch": "089", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution631StartingState"], "fixtureVerification": verification,
        "provenance": provenance, "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "compileExitCode": 0, "buildResult": "BUILD SUCCESSFUL", "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8426, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 115, "remainingAdditions": 1113, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "generatedDiffWhitespace": "Exact generated diff context includes space-prefixed blank lines; preserve as evidence, not source whitespace changes.",
        "preparationDiagnostic": "Initial pre-write stale-token assertion matched がい inside current example れいがい. Restricted the old quiz-key assertion to the quoted token. No fixture/archive was written by that failed attempt; no source, content, review, permission or acceptance gate was weakened.",
    })
    print("Compiled fixture/APK/full-envelope evidence archived for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-089-native/", "docs/n1-sources/execution-631.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-089-native-631-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-089-native-631-issue-body.txt").read_bytes().decode("utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-631.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state, original = load(C / "progress.json"), load(BEFORE)
    assert state["checkpoint"] == 630 and state["stage"] == "batch-089-native-preparation-in-progress"
    assert all(state[key] == value for key, value in original.items() if key not in {"stage", "nextAction"})
    checkpoint = {
        "schemaVersion": 1, "execution": 631, "checkpoint": 631, "batch": "089",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": "native-prepared-compiled-not-executed",
        "evidence": "docs/n1-sources/execution-631.json", "contentArchiveHead": HEAD, "androidHead": APP,
        "fixtureVerification": str(VERIFICATION), "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE),
        "testApk": evidence["testApk"], "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8426,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 115, "remainingAdditions": 1113, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=631, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution631CoordinatorCheckpoint"] = checkpoint
    state["batch089NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    persist(state)
    assert all(load(C / "progress.json")[key] == value for key, value in original.items()
               if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(L / "checkpoint-631-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 631, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
