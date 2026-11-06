import difflib
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
LOG = C / "logs" / "0a43f5a9-526e-48b3-a031-45f5abcd9a2f"
HEAD = "867fe8bef228145ef0a6e48690941b0a0aa50336"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "6dfe6a1e287ce5df"
FOLDER = R / "docs" / "n1-reviews" / "batch-083-native-corrected"
FIXTURE = FOLDER / "N1Batch083CorrectedNativeTest.kt"
ARCHIVE = C / "artifacts" / "n1-batch-083-corrected-867fe8be-envelope.zip"
VERIFICATION = C / "batch-083-corrected-native-fixture-verification.json"
BEFORE = LOG / "progress-before-577.json"
EVIDENCE = R / "docs" / "n1-sources" / "execution-577.json"
NEXT = (
    "SAME083 corrected native execution and direct PNG inspection NEXT, then persist/yield; "
    "no publication/084. Read execution-577.json and corrected-native fixture verification. "
    "Use NEW corrected frozen archive867fe8be/version6dfe6a1e287ce5df/8376hashes, "
    "N1Batch083CorrectedGlyphTest and N1Batch083CorrectedArticleTest, corrected577app/testAPKs "
    "with exact hashes; original573/574attempt/fixtures/APKs/reports immutable. Fresh HOST4 "
    "no-skips and corrected test compilation passed; do not repeat absent new concern. "
    "SignedAndroid1c1b7bf4/G TEST-ONLY harness atop unchangedproductionf9; HOSTinit NEVER native. "
    "Require terminal0 BOTH named corrected cases/no skips/no-2/-3. ProductionContentSyncONCE/"
    "1095kanji5052words115N1/zeroProblems/acceptedepoch1; exact imported N1 AND All "
    "QuizBuilder default4 IDs+titles凌/准/冶/冴 all3curatedavailable/no padding, plus actual "
    "N1UI meaning/feedback; no selectedpool expansion/level/algorithm/assertion weakening. "
    "Full/Lite source+curated onリョウ/kunしの.ぐ and independently persisted soleりょう/しのぐ. "
    "Updated30Han incl冴/120individual+8wholeword/fourfonts/Paint/directComposePNG/"
    "lookalikes凌陵准冶冴次/冫夌阝隹; complete3articles/two reciprocalpairs/fourdirections/"
    "SystemBack/offline/selection/bothreadings/tenstroketrace/recall/persistence retained. "
    "Injectedtrace/giveup NOT humanrecognition/MLKit/phone. FreshlocalANDremote5580/5581 "
    "inclTimeWait/devices/PIDs/liveparentancestry immediately before ownedreadonlyAVD "
    "N3_Acceptance_20261029 API35/hostGPU/-Vulkan/2048MiB2cores explicitserialemulator-5580; "
    "no alternateport/shareddevice interference, owned-only cleanup. One heavy process, "
    "explicitJDK17+SDK/unchangedheaps/guards. Original serial two-family dependent VISUAL "
    "confirmations still required BEFORE latest-main normalmerge/combinedPython/validator/"
    "vocabulary/manifest/exact17guards/baseline/link/membership/originalbudgets/normal "
    "signedownerfastforward/exactremote/terminalgreenCI/EVERYimmutableZIPhash/verifiedownerissue60 "
    "BEFORE084. Textual083-NATIVE-574-CHOICE resolved by originalClaudeOpus5.5+GPT6.1Sol; "
    "runtime remains partiallyresolved/outstanding. 冴える excel-at/skillfulness retained, "
    "actualclear;sharp-minded wrong for凌; no universal synonym-disjointness/random/custom/"
    "padded/partial/larger/reversepool safety. All inherited gates and original limitations "
    "retained in evidence577/576/575/574. Parent19008 runner.lock untouched; approvedcontrol"
    "helpers/committedsources only/nooptionalhistoricalsessionhelpers. Preserve/report/yield "
    "actualnewdenial/signinghang. Published109/1228,remaining1119/latestpublic21a5cb1328aadd"
    "437139a6b850f07298a2e2985d unchanged;083notdelivered. Physicalphone/generalrelease/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def update(p):
    tmp = C / "progress.577.tmp"
    assert not tmp.exists()
    save(tmp, p)
    assert load(tmp) == p
    tmp.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8376
    return manifest


def start():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 576 and p["status"] == "continue" and p["batch"] == "083"
    clean(R, HEAD)
    clean(A, APP)
    runtime()
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)
    request = (LOG / "request.txt").read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(request.split(marker, 1)[1])["checkpoint"] == 576
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    state = {
        "execution": 577, "batch": "083", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME083 corrected affected HOST and separately named full signed archive/native-fixture/APK preparation only, normally signed LOCAL evidence checkpoint; no emulator/native/reviewer/publication/084.",
        "request": {"sha256": sha(LOG / "request.txt"), "characters": len(request),
                    "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint parsed; operative contract, complete issue and final576 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 verified in coordinator ancestry; child never opens, reacquires, deletes or unlocks runner.lock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    p["execution577StartingState"] = state
    p["stage"] = "batch-083-corrected-host-native-preparation-in-progress"
    p["nextAction"] = state["scope"]
    update(p)
    save(C / "execution-577-start.json", state)
    print("Starting scope persisted; original live history preserved.")


def prepare():
    from fontTools.ttLib import TTFont
    clean(R, HEAD)
    clean(A, APP)
    assert not FOLDER.exists() and not ARCHIVE.exists() and not VERIFICATION.exists()
    manifest = runtime()
    assert not git("diff", "7cc896f488ae5315046453777aae6768b9ff18e8", HEAD,
                   "--", "kanji", "words", "articles", "strokes", "manifest.json")
    reconciliation = load(R / "docs/n1-reviews/batch-083-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    assert reconciliation["choiceConfirmation"]["status"] == "corrected-choice-textually-confirmed-awaiting-fresh-host-native"
    old = load(C / "batch-083-native-fixture-verification.json")
    prior = Path(old["fixture"])
    assert sha(prior) == old["fixtureSha256"]
    assert sha(Path(old["archive"])) == old["archiveSha256"]
    text = prior.read_text(encoding="utf-8")
    for before, after in [
        ("N1Batch083GlyphTest", "N1Batch083CorrectedGlyphTest"),
        ("N1Batch083ArticleTest", "N1Batch083CorrectedArticleTest"),
        ("disposable083", "disposable083Corrected"),
        ("n1-083", "n1-083-corrected"),
        (old["contentSnapshot"], HEAD), (old["contentVersion"], VERSION),
        (Path(old["archive"]).name, ARCHIVE.name),
        ('listOf("准", "冶", "次")', 'listOf("准", "冶", "冴")'),
        ('"次" to "next"', '"冴" to "clear; sharp-minded"'),
        ("all 29 scoped Han", "all 30 scoped Han"),
        ("29 actual scoped Han", "30 actual scoped Han"),
        ("凌/陵/准/冶/次", "凌/陵/准/冶/冴/次"),
        ("assertEquals(124, rows.length())", "assertEquals(128, rows.length())"),
        ('put("individualGlyphProbes", 116)', 'put("individualGlyphProbes", 120)'),
    ]:
        assert before in text, before
        text = text.replace(before, after)
    text = text.replace("import io.github.stopcran.kanji.core.reading.ReadingKind",
                        "import io.github.stopcran.kanji.core.quiz.QuizBuilder\n"
                        "import io.github.stopcran.kanji.core.quiz.QuizCard\n"
                        "import io.github.stopcran.kanji.core.reading.ReadingKind")
    names = [entry["path"] for entry in old["articleFiles"]]
    glyphs = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "".join(
        (R / name).read_text(encoding="utf-8") for name in names))))
    assert len(glyphs) == 30 and set(glyphs) == set(old["plannedGlyphs"]) | {"冴"}
    quote = lambda s: json.dumps(s, ensure_ascii=False).replace("$", "\\$")
    pages = [" ".join(glyphs[i:i + 24]) for i in range(0, len(glyphs), 24)]
    pages.append("凌 陵 准 冶 冴 次 冫 夌 阝 隹 凌ぐ 凌駕")
    text = re.sub(r"val pages = listOf\([^\n]+\)",
                  "val pages = listOf(" + ", ".join(map(quote, pages)) + ")", text, count=1)
    text = re.sub(r"for \(char in listOf\([^\n]+\)",
                  "for (char in listOf(" + ", ".join(map(quote, glyphs)) + "))", text, count=1)
    # Keep every existing article selector and route assertion, including unchanged 次 prose.
    for selector in old["staticMarkdownSelectors"]:
        assert quote(selector["target"]) in text
    insertion = '''        val expectedMeanings = mapOf(
            "凌" to "endure; surpass", "准" to "quasi-; associate rank",
            "冶" to "smelt; work metals", "冴" to "clear; sharp-minded",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "凌" }
            assertEquals(listOf("准", "冶", "冴"), target.distractors)
            assertEquals(expectedMeanings, cards.filter { it.kanji in expectedMeanings }.associate { it.kanji to it.title })
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(577))
            assertEquals(4, options.size)
            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("allThreeCuratedAvailable", true).put("defaultFourNoPadding", true))
        }
'''
    needle = '        val now = System.currentTimeMillis()'
    assert text.count(needle) == 1
    text = text.replace(needle, insertion + needle)
    text = text.replace('.put("transport", "Exact full git envelope',
                        '.put("productionBuilderN1AndAllExactChoices", checkedPools)\n'
                        '            .put("transport", "Exact full git envelope')
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    assert text.count('assertEquals(listOf("准", "冶", "冴")') == 4
    assert "repeat(2)" in text and "assertEquals(2, readingLogs.size)" in text
    fonts = []
    for item in old["currentFontAudit"]:
        path = Path(item["path"])
        assert sha(path) == item["sha256"]
        with TTFont(path) as font:
            missing = [g for g in glyphs if ord(g) not in font.getBestCmap()]
        assert missing == ["冫", "夌", "阝", "隹"]
        fonts.append(dict(item, missingCurrentScopedHan=missing))
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-083-corrected/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    prefix = "n1-batch-083-corrected/"
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.namelist()
        assert len(entries) == len(set(entries)) <= 18000
        assert all(n.startswith(prefix) and "\\" not in n and ".." not in n.split("/") for n in entries)
        raw = archive.read(prefix + "manifest.json")
        assert raw == subprocess.check_output(["git", "show", f"{HEAD}:manifest.json"], cwd=R)
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
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected
                retained += len(data)
                verified += 1
        inflated = sum(i.file_size for i in archive.infolist())
        assert retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in entries)
    assert verified == 8376
    FOLDER.mkdir()
    FIXTURE.write_text(text, encoding="utf-8")
    diff = FOLDER / "fixture-from-original-083.diff"
    diff.write_text("".join(difflib.unified_diff(
        prior.read_text(encoding="utf-8").splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=prior.relative_to(R).as_posix(), tofile=FIXTURE.relative_to(R).as_posix(), n=3)), encoding="utf-8")
    record = dict(old)
    record.update({
        "execution": 577, "status": "corrected-prepared-not-executed", "contentSnapshot": HEAD,
        "reviewedTeachingSnapshot": "7cc896f488ae5315046453777aae6768b9ff18e8", "contentVersion": VERSION,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(entries),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "verifiedRuntimeHashes": verified, "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorHarness": prior.relative_to(R).as_posix(), "priorHarnessSha256": sha(prior),
        "fixtureDiff": diff.relative_to(R).as_posix(), "fixtureDiffSha256": sha(diff),
        "articleFiles": [dict(item, sha256=sha(R / item["path"])) for item in old["articleFiles"]],
        "plannedGlyphs": glyphs, "plannedComposePanels": pages, "plannedNativePaintProbes": 120,
        "currentFontAudit": fonts,
        "exactMeaningOptions": {"凌": "endure; surpass", "准": "quasi-; associate rank",
                                "冶": "smelt; work metals", "冴": "clear; sharp-minded"},
        "meaningScope": "Production QuizBuilder on complete imported N1 and All, default4/all three curated available/no padding; additionally actual N1 UI options/feedback. Not random/custom/padded/partial/larger/reverse-pool safety.",
        "originalAttemptPreserved": True,
    })
    save(VERIFICATION, record)
    print(f"Corrected fixture prepared: {verified} hashes, {len(glyphs)} Han; native NOT executed.")


def record():
    clean(A, APP)
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runtime()
    fixture = load(VERIFICATION)
    assert sha(FIXTURE) == fixture["fixtureSha256"] and sha(ARCHIVE) == fixture["archiveSha256"]
    assert (LOG / "host-exit-577.txt").read_text().strip() == "0"
    assert (LOG / "corrected-native-compile-exit-577.txt").read_text().strip() == "0"
    command = load(LOG / "corrected-native-compile-command-577.json")
    assert command["hostOnlyHeapInitUsed"] is False
    assert command["arguments"] == [":app:assembleDebugAndroidTest", "--no-daemon", "--no-parallel", "--max-workers=1",
                                     "-Pkotlin.compiler.execution.strategy=in-process"]
    host = load(LOG / "host-command-577.json")
    assert host["exactSiblingContent"] == str(R) and host["hostOnlyHeapInit"] is True
    assert host["nativeHeapInit"] is False
    assert "--rerun-tasks" in host["arguments"]
    xml_paths = [
        A / "core/build/test-results/test/TEST-io.github.stopcran.kanji.core.RealContentTest.xml",
        A / "app/build/test-results/testDebugUnitTest/TEST-io.github.stopcran.kanji.core.RareHanTest.xml",
    ]
    suites = []
    for path, count in zip(xml_paths, [3, 1]):
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == count
        assert all(int(xml.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
        assert len(xml.findall("testcase")) == count and not xml.findall(".//skipped")
        suites.append({"path": str(path), "sha256": sha(path), "suite": xml.attrib,
                       "cases": [node.attrib for node in xml.findall("testcase")]})
    assert datetime.fromisoformat((LOG / "host-end-577.txt").read_text().strip()) < datetime.fromisoformat(
        (LOG / "corrected-native-compile-start-577.txt").read_text().strip())
    assert (A / "core/../../learning-japanese").resolve() == R
    assert (A / "app/../../learning-japanese").resolve() == R
    apk = C / "artifacts/n1-batch-083-corrected-577-native-test.apk"
    app = C / "artifacts/n1-batch-083-corrected-577-native-app.apk"
    assert sha(app) == command["baselineAppSha256"]
    with zipfile.ZipFile(apk) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == fixture["archiveSha256"]
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        for name in ("N1Batch083CorrectedGlyphTest", "N1Batch083CorrectedArticleTest",
                     "enduranceLookalikesAndRadicalFallbacksAcrossFourProductionFamilies",
                     "fullSingleImportOfflineEnduranceTwoReciprocalPairsCuratedOnAndKunDrawingAndSystemBack"):
            assert name.encode() in dex, name
    receipts = FOLDER / "preparation-receipts"
    assert not receipts.exists()
    receipts.mkdir()
    provenance = []
    sources = [
        Path(__file__), C / "run-577-host.ps1", C / "run-577-native-compile.ps1",
        C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt", VERIFICATION,
        C / "batch-065-host-integration-heap.init.gradle", *xml_paths,
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        A / "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
        *[LOG / name for name in (
            "runner-ancestry-577.json", "host-command-577.json", "host-start-577.txt", "host-end-577.txt", "host-exit-577.txt",
            "corrected-native-compile-command-577.json", "corrected-native-compile-start-577.txt",
            "corrected-native-compile-end-577.txt", "corrected-native-compile-exit-577.txt")],
    ]
    for source in sources:
        target = receipts / source.name
        assert not target.exists()
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    for name in ("host-577.txt", "corrected-native-compile-577.txt"):
        source = LOG / name
        target = receipts / (name + ".gz")
        with target.open("wb") as stream:
            with gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as zipped:
                zipped.write(source.read_bytes())
        assert gzip.decompress(target.read_bytes()) == source.read_bytes()
        provenance.append({"source": str(source), "sourceSha256": sha(source),
                           "archive": target.relative_to(R).as_posix(), "sha256": sha(target),
                           "losslessGzipVerified": True})
    result = next(line for line in (LOG / "corrected-native-compile-577.txt").read_text().splitlines()
                  if line.startswith("BUILD SUCCESSFUL"))
    host_result = next(line for line in (LOG / "host-577.txt").read_text().splitlines()
                       if line.startswith("BUILD SUCCESSFUL"))
    old = load(R / "docs/n1-sources/execution-573.json")
    for key in ("testApk", "appApk"):
        assert sha(Path(old[key]["path"])) == old[key]["sha256"]
    save(EVIDENCE, {
        "schemaVersion": 1, "execution": 577, "batch": "083",
        "status": "corrected-host-passed-native-prepared-compiled-not-executed",
        "startingState": load(C / "execution-577-start.json"),
        "contentSnapshot": HEAD, "teachingSnapshot": "7cc896f488ae5315046453777aae6768b9ff18e8",
        "androidHead": APP, "productionBaseline": PROD, "fixtureVerification": fixture,
        "hostResult": host_result, "hostExitCode": 0, "hostSuites": suites,
        "hostCases": 4, "hostSkips": 0, "freshHostRerunTasks": True,
        "actualSiblingContent": str(R), "bothModuleRelativeRootsResolvedExactly": True,
        "hostOnlyHeapInitUsed": True, "nativeHeapInitUsed": False,
        "buildResult": result, "compileExitCode": 0,
        "testApk": {"path": str(apk), "sha256": sha(apk), "embeddedArchiveHashVerified": True,
                    "bothCorrectedNamedCasesInDex": True},
        "appApk": {"path": str(app), "sha256": sha(app), "unchangedProductionBuild": True},
        "provenance": provenance, "original573And574ArtifactsUnchanged": True,
        "runtimeManifestHashesVerified": 8376, "runtimeChanged": False,
        "runtimePublished": False, "runtimeAccepted": False, "nativeOrVisualExecuted": False,
        "reviewersLaunched": 0, "nextBatchStarted": False,
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "diagnostics": [
            "Preparation prerequisite lookup adjusted to actual root textualReviewClosed and choiceConfirmation.status before prepare ran. No generated source/archive existed at that point; no failed build/test, permission denial or gate substitution.",
        ],
        "nextGate": NEXT,
        "inheritedNextGate": load(R / "docs/n1-sources/execution-576.json")["confirmation"],
        "limits": fixture["limits"] + " N1 and All exact production-builder assertions are prepared, not executed; only actual N1 UI session is assigned. No All UI/custom/random/padded/partial/larger/reverse-pool safety claim.",
    })
    print(f"{host_result}; 4 cases, no skips. {result}; corrected APK hashes verified, native NOT executed.")


def finish():
    clean(A, APP)
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("merge-base", HEAD, "HEAD") == HEAD
    runtime()
    evidence = load(EVIDENCE)
    assert not evidence["nativeOrVisualExecuted"] and not evidence["runtimePublished"]
    p = load(C / "progress.json")
    assert p["checkpoint"] == 576 and p["batch"] == "083"
    before = load(BEFORE)
    for key, value in before.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert p[key] == value, key
    summary = {
        "schemaVersion": 1, "execution": 577, "checkpoint": 577, "batch": "083",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": "corrected-host-passed-native-prepared-compiled-awaiting-execution",
        "evidence": EVIDENCE.relative_to(R).as_posix(), "contentSnapshot": HEAD,
        "androidHead": APP, "contentVersion": VERSION, "runtimeManifestHashesVerified": 8376,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "freshHostCasesPassed": 4, "hostSkips": 0, "correctedFixtureCompiled": True,
        "nativeOrVisualExecuted": False, "reviewersLaunched": 0,
        "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "dedicatedWorktreesClean": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    for key in ("checkpoint", "status", "stage", "nextAction"):
        p[key] = summary[key]
    p["blocker"] = None
    assert "execution577CoordinatorCheckpoint" not in p
    p["execution577CoordinatorCheckpoint"] = summary
    p["batch083CorrectedNativePreparationCheckpoint"] = summary
    update(p)
    save(C / "execution-577-checkpoint.json", summary)
    print("Checkpoint577 persisted; full historical values preserved, both dedicated worktrees clean.")


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record, "finish": finish}[sys.argv[1]]()
