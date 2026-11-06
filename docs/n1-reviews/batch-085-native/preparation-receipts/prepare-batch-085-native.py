import copy
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
LOG = C / "logs" / "2b41f559-c2ff-4dc8-a17f-1897c402ca8d"
HEAD = "1d2e329035789b160e495a7518d64183f799233e"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "0c514711ae8d3212"
PRIOR = R / "docs" / "n1-reviews" / "batch-083-native-corrected" / "N1Batch083CorrectedNativeTest.kt"
WORK = C / "batch-085-native-595"
FIXTURE = WORK / "N1Batch085NativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-085-1d2e3290-envelope.zip"
VERIFICATION = C / "batch-085-native-fixture-verification.json"
BEFORE = LOG / "progress-before-595.json"
FOLDER = R / "docs" / "n1-reviews" / "batch-085-native"
NEXT = (
    "SAME085 execute newly compiled frozen native fixture and inspect actual PNGs next; "
    "read execution-595.json and batch-085-native-fixture-verification.json. Verify exact "
    "signed full archive1d2e3290/version0c514711ae8d3212/8413runtimehashes, frozen085 "
    "app/testAPK and fixture hashes. Qualified TESTONLY Android1c1b7bf4 atop unchanged "
    "productionf9b59a2; fresh HOST4 zero-skips passed594; preparation595 is NOT native "
    "acceptance. Require terminalcase0 BOTH N1Batch085GlyphTest and N1Batch085ArticleTest, "
    "no skips/errors. Full productionContentSyncONCE,1108kanji/5063words/117N1/"
    "zeroProblems/version/acceptedRoomepoch1. Full metadata onギョウ/kunこ.る,こ.らす,"
    "こご.らす,こご.らせる,こご.る unchanged; curated onギョウ/kunこ.る,こ.らす "
    "yields exactlyぎょう/こる (こ.らす shares normalizedこる, not independent queued "
    "mastery), both kinds offered/persistedGood/done. All39Han (original37 plus努力 "
    "from reviewedQ1guard)/fourproductionfamilies/156individual+12wholewordrasters/"
    "3Composepanels especially冫/隹 require direct "
    "PNGlegibility/lookalike inspection; cmap/hasGlyph/hashes not readability/fallbackface. "
    "Complete凝/凝固/凝る/凝らす article projections plus changed固bullet only, "
    "fourreciprocalpairs/eightdirections, SystemBack/offline/N1selection/meaning/"
    "bothreadingkinds/16stroke injectedtrace/recall/persistence. Injectedtrace/giveup "
    "NOT humanhandwriting/MLKit/phone. Fresh device/PID/local+remote5580/5581 including "
    "TimeWait ownership immediately before ownedreadonly API35N3_Acceptance_20261029 "
    "emulator-5580 launch; hostGPU/-Vulkan/2048MiB/2cores/explicitserial, stop only "
    "ownedhelper. No shareddevice interference, alternateport without authorization, "
    "app/guestheap/guard increase, productionappchange or086. Parent19008 ownsrunner.lock; "
    "verify liveancestry/session/checkpoint/exactsignedheads/whollycleanworktrees; "
    "NOchildlockacquisition/delete/unlock. Approvedcontrol/committedsources only. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Original "
    "twofamilytextualreviews/limits/Q1resolved/othersoptional preserved; dependent "
    "serialtwofamilyvisualconfirmation remains. Later currentmainnormalmerge/surgical "
    "reconciliation/changedteachingreview/combinedchecks/normalsigning/ownerfastforward/"
    "terminalCI/EVERYimmutablepublicZIPruntimehash/original18000entries/42MiBcompressed/"
    "80MiBinflated/56MiBretained/perfile-media-safepathguards/verifiedownerissue remain. "
    "Published111/1228,1117remaining unchanged; physicalphone/generalrelease/whole-set "
    "outstanding, projectincomplete. No086."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root), str(root)


def update(state):
    temp = C / "progress.595.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    value = load(R / "manifest.json")
    assert value == build_manifest(R) and value["contentVersion"] == VERSION
    assert sum(len(v) for v in value.values() if isinstance(v, dict)) == 8413
    return value


def start():
    clean(R, HEAD)
    clean(A, APP)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 594 and state["batch"] == "085"
    assert state["stage"] == "fresh-android-passed-awaiting-native"
    assert state["status"] == "continue" and not BEFORE.exists()
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == LOG.name and runner["status"] == "running"
    role = load(C / "batch-085-native-595-runner-role.json")
    assert any(p["pid"] == 19008 for p in role)
    request = (LOG / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 594
    runtime()
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)
    shutil.copyfile(C / "progress.json", BEFORE)
    state["execution595StartingState"] = {
        "execution": 595, "batch": "085", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME085 full archive/native fixture preparation and compilation, signed LOCAL evidence; yield before native execution/reviewer/integration/publication/086.",
        "request": {"sha256": sha(LOG / "request.txt"), "bytes": (LOG / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, complete issue and final594 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live parent19008 ancestry; child never acquires/deletes/unlocks parent lock.",
        "runnerRoleReceipt": str(C / "batch-085-native-595-runner-role.json"),
        "artifactPathPreflight": "Approved workspace inputs, committed source packets and new reusable control helpers only; optional historical session helpers not accessed.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-085-native-preparation-in-progress"
    state["nextAction"] = state["execution595StartingState"]["scope"]
    update(state)
    print("Starting scope persisted with complete live history.")


def quote(text):
    return json.dumps(text, ensure_ascii=False).replace("$", "\\$")


def plain(text):
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text).replace("**", "")
    return re.sub(r"\*([^\s*](?:[^*]*[^\s*])?)\*", r"\1", text)


def blocks(path):
    body = path.read_text(encoding="utf-8").split("---\n", 2)[2]
    result, paragraph = [], []

    def flush():
        if paragraph:
            result.append(("paragraph", plain(" ".join(paragraph))))
            paragraph.clear()

    for value in body.splitlines() + [""]:
        if not value.strip():
            flush()
        elif value.startswith("#"):
            flush()
            result.append(("heading", value.lstrip("#").strip()))
        elif value.startswith("|"):
            flush()
            cells = value.strip("|").split("|")
            if not all(re.fullmatch(r"\s*-+\s*", cell) for cell in cells):
                result.extend(("table", plain(cell.strip())) for cell in cells)
        elif re.match(r"^\s*[-*+]\s+", value):
            flush()
            paragraph.append(re.sub(r"^\s*[-*+]\s+", "", value))
        else:
            paragraph.append(value.strip())
    return result


def prepare():
    from fontTools.ttLib import TTFont
    clean(R, HEAD)
    clean(A, APP)
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    reconciliation = load(R / "docs" / "n1-reviews" / "batch-085-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    for name, digest in reconciliation["reviewedRuntimeHashes"].items():
        assert sha(R / name) == digest, name
    audit = load(R / "docs" / "n1-sources" / "batch-085-draft-font-audit.json")
    names = audit["completeNewArticleScope"]
    assert names == ["kanji/凝.md", "words/凝固.md", "words/凝る.md", "words/凝らす.md"]
    changed = audit["changedReusedScope"]
    assert list(changed) == ["kanji/固.md"]
    docs = {name: blocks(R / name) for name in names + list(changed)}
    lines, selectors, offsets = [], [], []

    def line(value):
        lines.append("            " + value)

    def show(document, kind, value, step):
        qualifier = "readingExample" if kind == "table" else "articleBullet"
        assert sum(v == value for k, v in docs[document]
                   if (k == "table") == (kind == "table") and k != "heading") == 1, (document, value)
        line(f"show({qualifier}({quote(value)}), {quote(step)})")
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
        sections = re.split(r"^## (.+)\n", (R / document).read_text(encoding="utf-8").split("---", 2)[2], flags=re.M)
        candidates = []
        for i in range(1, len(sections), 2):
            if sections[i] != section:
                continue
            for part in re.split(r"\n\s*\n|\n(?=- )", sections[i + 1].strip()):
                for link in re.finditer(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", part):
                    if (R / document).parent.joinpath(link[1]).resolve() == (R / destination).resolve():
                        candidates.append((part.removeprefix("- "), link[1]))
        assert len(candidates) == 1, (document, label, candidates)
        raw, _ = candidates[0]
        link = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", raw)
        rendered = plain(" ".join(raw.splitlines()))
        marked = raw[:link.start()] + "N1_LINK_TARGET_595" + raw[link.end():]
        offset = plain(" ".join(marked.splitlines())).index("N1_LINK_TARGET_595")
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
    line('rule.onNode(hasSetTextAction()).performTextReplacement("凝")')
    line('click("congeal; become absorbed")')
    display("kanji/凝.md", "kanji")
    for word, slug in [("凝固", "solidify"), ("凝る", "absorbed"), ("凝らす", "effort")]:
        forward = follow("kanji/凝.md", word, f"words/{word}.md", "Common words", slug + "-forward")
        display(f"words/{word}.md", slug)
        if word == "凝固":
            solid = follow("words/凝固.md", "固", "kanji/固.md", "How the kanji combine", "solid-kanji")
            line('await("固 — firm; harden")')
            reverse_solid = follow("kanji/固.md", "凝固", "words/凝固.md", "Common words", "solid-changed-bullet")
            line(f"await({quote(docs['words/凝固.md'][0][1])})")
            back_to(reverse_solid, "solid-back-to-reused-kanji")
            back_to(solid, "solid-back-to-word")
        reverse = follow(f"words/{word}.md", "凝", "kanji/凝.md", "How the kanji combine", slug + "-reverse")
        line('section("Readings")')
        line(f'show(readingExample("ギョウ"), "{slug}-kanji-backlink")')
        back_to(reverse, slug + "-system-back-to-word")
        back_to(forward, slug + "-system-back-to-kanji")
    assert len(offsets) == 8
    assert len({(i["document"], i["destination"]) for i in offsets}) == 8
    text = PRIOR.read_text(encoding="utf-8")
    begin = text.index('            click("Browse all kanji")')
    end = text.index('            back()\n            await("Search kanji, meaning or reading")', begin)
    text = text[:begin] + "\n".join(lines) + "\n" + text[end:]
    replacements = [
        ("N1Batch083Corrected", "N1Batch085"), ("disposable083Corrected", "disposable085"),
        ("n1-083-corrected", "n1-085"), ("Batch 083", "Batch 085"),
        ("n1-batch-083-corrected-867fe8be-envelope.zip", ARCHIVE.name),
        ("867fe8bef228145ef0a6e48690941b0a0aa50336", HEAD),
        ("6dfe6a1e287ce5df", VERSION), ("1095, updated.kanji", "1108, updated.kanji"),
        ("5052, updated.words", "5063, updated.words"), ("115, n1.size", "117, n1.size"),
        ("N1 · 115 cards", "N1 · 117 cards"), ('"凌"', '"凝"'),
        ("endurance", "concentration"), ("EnduranceTwoReciprocalPairs", "ConcentrationFourReciprocalPairs"),
        ("endure; surpass", "congeal; become absorbed"),
        ('listOf("准", "冶", "冴")', 'listOf("准", "冗", "凹")'),
        ('"冶" to "smelt; work metals"', '"冗" to "superfluous; redundant"'),
        ('"冴" to "clear; sharp-minded"', '"凹" to "concave; sunken"'),
        ('listOf("リョウ")', 'listOf("ギョウ")'), ('"りょう"', '"ぎょう"'),
        ('"しのぐ"', '"こる"'),
        ('put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)',
         'put("mappedReciprocalPairs", 4).put("directedLinkTransitions", 8)'),
        ('put("completeArticleProjections", 3)',
         'put("completeArticleProjections", 4).put("changedReusedBullets", 1)'),
        ("assertEquals(10, strokes.length())", "assertEquals(16, strokes.length())"),
        ('hasContentDescription("10 strokes drawn"', 'hasContentDescription("16 strokes drawn"'),
        ("kotlin.random.Random(577)", "kotlin.random.Random(595)"),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    for target in ("concentration", "card"):
        text = text.replace(f'listOf("しの.ぐ"), {target}.kunyomi.splitSep()',
                            f'listOf("こ.る", "こ.らす", "こご.らす", "こご.らせる", "こご.る"), {target}.kunyomi.splitSep()')
        text = text.replace(f'listOf("しの.ぐ"), {target}.quizKunyomi?.splitSep()',
                            f'listOf("こ.る", "こ.らす"), {target}.quizKunyomi?.splitSep()')
    text = text.replace('setOf("ぎょう", "しのぐ")', 'setOf("ぎょう", "こる")')
    text = re.sub(r'\.put\("fixture", "Other N1 meanings/readings postponed;[^\n]+',
                  '.put("fixture", "Other N1 meanings/readings postponed; 凝 meaning and curated onぎょう/kunこる due. Selectedこ.らす shares normalizedこる, not independent queued mastery. Two historical good 凝 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")',
                  text, count=1)
    original_glyphs = audit["actualHan"]
    assert len(original_glyphs) == 37
    actual = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "".join(
        (R / name).read_text(encoding="utf-8") for name in names) + "".join(changed.values()))))
    assert set(actual) - set(original_glyphs) == set("努力")
    assert not set(original_glyphs) - set(actual)
    glyphs = actual
    assert len(glyphs) == 39
    fonts = []
    for entry in audit["fonts"]:
        path = Path(entry["path"])
        assert sha(path) == entry["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == entry["allActualMissing"] == ["冫", "隹"]
        fonts.append({"path": str(path), "sha256": sha(path), "missingCurrentScopedHan": missing})
    words = ["凝固", "凝る", "凝らす"]
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("凝 疑 准 冗 凹 冫 隹 凍 固 硬 凝固 凝る 凝らす")
    text = re.sub(r"val pages = listOf\([^\n]+\)", "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)", "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    text = re.sub(r"for \(word in listOf\([^\n]+\)", "for (word in listOf(" + ", ".join(map(quote, words)) + "))", text, count=1)
    text = text.replace("all 30 scoped Han; focused 凌/陵/准/冶/冴/次, 冫/夌/阝/隹",
                        "all 39 scoped Han; focused 凝/疑/准/冗/凹, 冫/隹")
    text = text.replace("30 actual scoped Han including exact 冫/夌/阝/隹 fallback inspection",
                        "39 actual scoped Han including exact 冫/隹 fallback inspection")
    text = text.replace("assertEquals(128, rows.length())", "assertEquals(168, rows.length())")
    text = text.replace('put("individualGlyphProbes", 120).put("wholeWordRasterProbes", 8)',
                        'put("individualGlyphProbes", 156).put("wholeWordRasterProbes", 12)')
    text = text.replace("eight whole-word rasters", "twelve whole-word rasters")
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    for stale in ("083", "凌", "しの", "リョウ", "りょう", "endurance", "Endurance", "夌", "阝"):
        assert stale not in text, stale
    assert all(quote(item["target"]) in text for item in selectors)
    assert 'listOf("こる"), concentration.toReadingCard().quizKeys(ReadingKind.Kun)' in text
    counts = {"kanji": sum(n.startswith("kanji/") for n in manifest["files"]),
              "words": sum(n.startswith("words/") for n in manifest["files"]),
              "n1": sum(re.search(r"^jlpt: 1$", p.read_text(encoding="utf-8"), re.M) is not None
                        for p in (R / "kanji").glob("*.md"))}
    assert counts == {"kanji": 1108, "words": 5063, "n1": 117}
    expected_titles = {"凝": "congeal; become absorbed", "准": "quasi-; associate rank",
                       "冗": "superfluous; redundant", "凹": "concave; sunken"}
    for char, title in expected_titles.items():
        assert re.search(r"^title: " + re.escape(title) + r"$", (R / "kanji" / f"{char}.md").read_text(encoding="utf-8"), re.M)
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-085/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith("n1-batch-085/") and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read("n1-batch-085/manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=R)
        assert json.loads(raw) == manifest
        retained, verified = len(raw), 0
        for section, mapping in manifest.items():
            if not isinstance(mapping, dict):
                continue
            for name, expected in mapping.items():
                data = archive.read("n1-batch-085/" + name)
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in archive.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024 and verified == 8413
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    WORK.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-from-corrected-083.diff"
    diff.write_text("".join(difflib.unified_diff(
        PRIOR.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=PRIOR.relative_to(R).as_posix(), tofile="docs/n1-reviews/batch-085-native/" + FIXTURE.name, n=2)), encoding="utf-8")
    record = {
        "schemaVersion": 1, "execution": 595, "batch": "085", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "reviewedTeachingSnapshot": reconciliation["originalTeachingSnapshot"],
        "reviewConfirmedCorrectionHead": "29a533800ed0d45e6269991d4a19e3b134057d6a",
        "androidSnapshot": APP, "productionBaseline": PROD, "contentVersion": VERSION,
        "expectedCounts": counts, "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE),
        "zipEntries": len(entries), "compressedBytes": ARCHIVE.stat().st_size,
        "inflatedBytes": inflated, "retainedBytes": retained, "verifiedRuntimeHashes": verified,
        "manifestEqual": True, "originalBudgetsPassed": True,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": PRIOR.relative_to(R).as_posix(), "priorHarnessSha256": sha(PRIOR),
        "fixtureDiff": str(diff), "fixtureDiffSha256": sha(diff),
        "staticMarkdownSelectors": selectors, "staticLinkedOffsets": offsets,
        "articleFiles": [{"path": n, "sha256": sha(R / n), "projectedTextBlocks": len(docs[n])} for n in names],
        "completeArticleProjections": 4, "changedReusedScope": changed,
        "mappedReciprocalPairs": 4, "mappedDirectedTransitions": 8,
        "plannedGlyphs": glyphs, "plannedWholeWords": words, "plannedComposePanels": pages,
        "plannedNativePaintProbes": 156, "plannedWholeWordRasterProbes": 12, "currentFontAudit": fonts,
        "fontScopeReconciliation": "Original draft audit37 preserved. Reviewed Q1 exclusion adds努力 in metadata; current full raw scope39 includes both, with no removal. Initial preparation assertion caught this before any fixture/archive was written.",
        "countReconciliation": "Measured current manifest1108kanji/5063words/117N1, rather than extrapolating old084native1096/5053. Static preflight caught the outdated assumption before any fixture/archive was written; require current whole envelope counts from actual production import. N1 published additions remain111; no extra target additions inferred from unrelated totals.",
        "fullReadings": {"on": ["ギョウ"], "kun": ["こ.る", "こ.らす", "こご.らす", "こご.らせる", "こご.る"]},
        "curatedReadings": {"on": ["ギョウ"], "kun": ["こ.る", "こ.らす"]},
        "normalizedQuizKeys": {"on": ["ぎょう"], "kun": ["こる"]},
        "sharedStemLimit": "Selected こ.らす shares normalizedこる withこ.る; not independent queued mastery.",
        "pendingCmapAbsences": ["冫", "隹"], "exactMeaningOptions": expected_titles,
        "plannedSerial": "emulator-5580", "plannedPorts": [5580, 5581],
        "nativeExecuted": False, "phoneEvidence": False, "hostTestInitScriptUsed": False,
        "limits": "Preparation only. Static Markdown selectors/offsets/cmaps/hashes are not native visibility/legibility/fallback-face evidence. Four new complete projections plus changed固bullet only; unchanged固article not claimed freshly reviewed. ProductionContentSyncONCE; reference tracing/giveup not human handwriting/MLKit/phone. All original source/reviewer/denial/OOM/phone limits and production heaps/guards preserved.",
    }
    save(VERIFICATION, record)
    print(json.dumps({k: record[k] for k in ("status", "expectedCounts", "zipEntries", "verifiedRuntimeHashes",
                                             "compressedBytes", "inflatedBytes", "retainedBytes")}))


def record():
    clean(R, HEAD)
    clean(A, APP)
    runtime()
    verification = load(VERIFICATION)
    assert sha(FIXTURE) == verification["fixtureSha256"] and sha(ARCHIVE) == verification["archiveSha256"]
    assert (LOG / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    command = load(LOG / "native-compile-command.json")
    assert command["parentAncestryVerified"] and not command["parentLockAccessAttempted"]
    assert not command["hostOnlyHeapInitUsed"]
    assert "BUILD SUCCESSFUL" in (LOG / "native-compile.txt").read_text(encoding="utf-8-sig")
    apk = C / "artifacts" / "n1-batch-085-native-test.apk"
    app = C / "artifacts" / "n1-batch-085-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch085GlyphTest", "N1Batch085ArticleTest",
                     "fullSingleImportOfflineConcentrationFourReciprocalPairsCuratedOnAndKunDrawingAndSystemBack"):
            assert name.encode() in dex, name
    assert not FOLDER.exists()
    FOLDER.mkdir()
    for path in WORK.iterdir():
        shutil.copyfile(path, FOLDER / path.name)
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir()
    sources = [Path(__file__), C / "run-595-native-compile.ps1", VERIFICATION,
               C / "batch-085-native-595-runner-role.json", C / "runner-lock-role-notes.txt",
               C / "authoring-artifact-path-notes.txt",
               *[LOG / n for n in ("native-compile-command.json", "native-compile-start.txt",
                                   "native-compile-end.txt", "native-compile-exit.txt")]]
    provenance = []
    for source in sources:
        target = receipts / source.name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    zipped = receipts / "native-compile.txt.gz"
    with zipped.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as compressor:
            compressor.write((LOG / "native-compile.txt").read_bytes())
    assert gzip.decompress(zipped.read_bytes()) == (LOG / "native-compile.txt").read_bytes()
    provenance.append({"archive": zipped.relative_to(R).as_posix(), "sha256": sha(zipped),
                       "sourceSha256": sha(LOG / "native-compile.txt"), "losslessGzipVerified": True})
    save(R / "docs" / "n1-sources" / "execution-595.json", {
        "schemaVersion": 1, "execution": 595, "batch": "085", "status": "native-prepared-compiled-not-executed",
        "contentSnapshot": HEAD, "androidHead": APP, "productionBaseline": PROD,
        "startingState": load(C / "progress.json")["execution595StartingState"],
        "fixtureVerification": verification, "provenance": provenance,
        "committedFixture": (FOLDER / FIXTURE.name).relative_to(R).as_posix(),
        "testApk": {"path": str(apk), "sha256": sha(apk)},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "buildResult": "BUILD SUCCESSFUL", "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "runtimeManifestHashesVerified": 8413, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "hostChecksRerun": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 111, "remainingAdditions": 1117, "nextAction": NEXT,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    })
    print("Preparation and exact compiled artifact evidence archived; ready for normal signed LOCAL commit.")


def finish():
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    clean(A, APP)
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(n.startswith(("docs/n1-reviews/batch-085-native/", "docs/n1-sources/execution-595.json"))
               for n in git("diff", "--name-only", HEAD, saved).splitlines())
    runtime()
    issue = load(C / "batch-085-native-595-issue-receipt.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-085-native-595-issue-body.txt").read_text(encoding="utf-8-sig")
    evidence = load(R / "docs" / "n1-sources" / "execution-595.json")
    for item in evidence["provenance"]:
        assert sha(R / item["archive"]) == item["sha256"]
    state = load(C / "progress.json")
    original = load(BEFORE)
    assert state["checkpoint"] == 594 and state["stage"] == "batch-085-native-preparation-in-progress"
    for key, value in original.items():
        if key not in {"stage", "nextAction"}:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 595, "checkpoint": 595, "batch": "085",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "native-prepared-compiled-not-executed", "evidence": "docs/n1-sources/execution-595.json",
        "contentArchiveHead": HEAD, "androidHead": APP, "fixtureVerification": str(VERIFICATION),
        "archiveSha256": sha(ARCHIVE), "fixtureSha256": sha(FIXTURE), "testApk": evidence["testApk"],
        "appApk": evidence["appApk"], "runtimeManifestHashesVerified": 8413,
        "contentVersion": VERSION, "compileExitCode": 0, "nativeOrVisualExecuted": False,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeAccepted": False, "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False, "publishedAdditions": 111,
        "remainingAdditions": 1117, "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(C / "batch-085-native-595-issue-receipt.json"),
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update(checkpoint=595, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    state["execution595CoordinatorCheckpoint"] = checkpoint
    state["batch085NativePreparationCheckpoint"] = copy.deepcopy(checkpoint)
    update(state)
    persisted = load(C / "progress.json")
    assert all(persisted[k] == v for k, v in original.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(LOG / "checkpoint-595-final-verification.json", checkpoint)
    print(json.dumps({"checkpoint": 595, "savedCommit": saved, "status": "continue",
                      "stage": checkpoint["stage"], "issueUpdate": issue["html_url"]}))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
