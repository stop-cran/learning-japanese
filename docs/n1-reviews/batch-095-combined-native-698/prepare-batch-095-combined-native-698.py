"""Prepare a distinct combined-manifest import fixture; retain original evidence."""
import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "7bdaadbe-a18f-4f7d-b635-8b2dc0c28c39"
HEAD = "6a7514c1ce11c25d58d43a8195540937a13378be"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "3eebfff0fdad5e28"
WORK = C / "batch-095-combined-native-698"
ARCHIVE = C / "artifacts" / "n1-batch-095-combined-6a7514c1-envelope.zip"
FIXTURE = WORK / "N1Batch095CombinedImport698Test.kt"
VERIFY = C / "batch-095-combined-native-698-verification.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean():
    for root, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R) and manifest["contentVersion"] == VERSION
    count = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                path = R.joinpath(*name.split("/"))
                actual = sha(path) if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(path)
                assert actual == digest, name
                count += 1
    assert count == 8441
    return manifest


def start():
    clean()
    runtime()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["batch"], state["stage"]) == (
        697, "continue", "095", "combined-main-teaching-confirmed-awaiting-exact-combined-native-import")
    role = load(L / "preflight-698.json")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert role["decodedLauncherMatches"] and role["liveParentPid"] == 19008 and not role["lockTouched"]
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["execution697CoordinatorCheckpoint"] == state["execution697CoordinatorCheckpoint"]
    before = L / "progress-before-698.json"
    assert not before.exists()
    save(before, state)
    state["execution698StartingState"] = {
        "execution": 698, "batch": "095", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME095 bounded exact combined full-archive production ContentSync import, curation/direct guards/links; signed local evidence checkpoint only; no publication/096.",
        "request": {"sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
                    "characters": len(request), "lines": len(request.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, complete issue and final697 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed source/fixture evidence only; no optional historical-session helper access.",
    }
    state["stage"] = "batch-095-combined-native-import-in-progress"
    state["nextAction"] = state["execution698StartingState"]["scope"]
    temp = C / "progress.698.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")
    print("Starting698 persisted with complete live history.")


def prepare():
    clean()
    manifest = runtime()
    assert not WORK.exists() and not ARCHIVE.exists() and not VERIFY.exists()
    prior = R / "docs" / "n1-reviews" / "batch-095-native" / "N1Batch095NativeTest.kt"
    assert sha(prior) == "295e763b5b274e9ebaf09db5229a642d197b6e2a49b7dcce94cb0b21a4b7684d"
    text = prior.read_text(encoding="utf-8")
    imports = text[:text.index("private fun disposable095()")]
    body = text.split("@Test fun fullSingleImportOfflineDissectionOneNewSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack() {", 1)[1]
    body = body.split("        val now = System.currentTimeMillis()", 1)[0]
    replacements = {
        "        disposable095()": '        assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))\n'
                                  '        assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))',
        "        app = instrumentation.targetContext.applicationContext as KanjiApp":
            "        val app = instrumentation.targetContext.applicationContext as KanjiApp",
        "n1-095-${UUID.randomUUID()}": "n1-095-combined-698-${UUID.randomUUID()}",
        "cc74834756847ad23fad6a721bb0a02ca859fa99": HEAD,
        "n1-batch-095-cc748347-envelope.zip": ARCHIVE.name,
        "463619d79972e9f2": VERSION,
    }
    for old, new in replacements.items():
        assert body.count(old) == 1, old
        body = body.replace(old, new)
    suffix = '''
        val full = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "剖") })
        assertEquals(listOf("ボウ"), full.onyomi.splitSep())
        assertEquals(emptyList<String>(), full.kunyomi.splitSep())
        assertNotNull(full.quizOnyomi)
        assertNotNull(full.quizKunyomi)
        assertEquals(listOf("ボウ"), full.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), full.quizKunyomi?.splitSep())
        assertEquals(listOf("ぼう"), full.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), full.toReadingCard().quizKeys(ReadingKind.Kun))
        val word = requireNotNull(runBlocking { app.db.content().word(source.id, "解剖") })
        val kai = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "解") })
        assertTrue(full.body.contains("[解剖](../words/解剖.md)"))
        assertTrue(word.body.contains("[剖](../kanji/剖.md)"))
        assertTrue(word.body.contains("[解](../kanji/解.md)"))
        assertTrue(kai.body.contains("[解剖](../words/解剖.md)"))
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable Wi-Fi/data before import", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(full.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(full.kunyomi.splitSep()))
            .put("fullQuizOnyomi", JSONArray(requireNotNull(full.quizOnyomi).splitSep()))
            .put("fullQuizKunyomi", JSONArray(requireNotNull(full.quizKunyomi).splitSep()))
            .put("liteOnyomi", JSONArray(dissection.onyomi.splitSep()))
            .put("liteKunyomi", JSONArray(dissection.kunyomi.splitSep()))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(dissection.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(dissection.quizKunyomi).splitSep()))
            .put("quizOnKeys", JSONArray(full.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(full.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("directGuardBuilderChecks", directGuardChecks).put("productionBuilderChoices", checkedPools)
            .put("reciprocalPairs", 2).put("linkDirections", 4)
            .put("transport", "Exact full combined git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("phoneEvidence", false).put("newVisualOrRouteAcceptance", false).put("passed", true)
        File(requireNotNull(app.getExternalFilesDir(null)), "n1-095-combined-import-698.json")
            .writeText(evidence.toString(2))
    }
}
'''
    generated = imports + "class N1Batch095CombinedImport698Test {\n    @Test fun exactCombinedArchiveSingleImportCurationGuardsAndLinks() {" + body + suffix
    assert generated.count("ContentSync(app.db") == 1
    assert "ContentParser.parse" not in generated and "463619d79972e9f2" not in generated
    WORK.mkdir()
    FIXTURE.write_text(generated, encoding="utf-8")
    raw = WORK / "git-archive.zip"
    subprocess.run(["git", "-C", str(R), "archive", "--format=zip", "--prefix=learning-japanese/",
                    f"--output={raw}", HEAD], check=True)
    raw.replace(ARCHIVE)
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        archived_manifest = json.loads(archive.read("learning-japanese/manifest.json"))
        assert archived_manifest == manifest
        checked = 0
        for section, entries in manifest.items():
            if isinstance(entries, dict):
                for name, digest in entries.items():
                    data = archive.read("learning-japanese/" + name)
                    if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                        data = data.replace(b"\r\n", b"\n")
                    assert hashlib.sha256(data).hexdigest() == digest, name
                    checked += 1
        inflated = sum(i.file_size for i in archive.infolist())
        assert checked == 8441 and len(names) <= 18000
        assert inflated <= 80 * 1024**2 and ARCHIVE.stat().st_size <= 42 * 1024**2
        assert not any(n.startswith("learning-japanese/docs/") for n in names)
    save(VERIFY, {
        "execution": 698, "contentSnapshot": HEAD, "androidSnapshot": APP, "productionBaseline": PROD,
        "contentVersion": VERSION, "runtimeHashesVerified": checked,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "priorFixture": prior.relative_to(R).as_posix(), "priorFixtureSha256": sha(prior),
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE),
        "archiveBytes": ARCHIVE.stat().st_size, "archiveEntries": len(names), "inflatedBytes": inflated,
        "singleProductionImportAsserted": True, "parentLockTouched": False,
        "limits": "Local git archive, not public GitHub ZIP acceptance; no fresh glyph/route/phone evidence.",
    })
    print(json.dumps(load(VERIFY), indent=2))


def compiled():
    clean()
    runtime()
    assert (L / "native-compile-exit.txt").read_text().strip() == "0"
    verification = load(VERIFY)
    for key in ["fixture", "archive"]:
        assert sha(Path(verification[key])) == verification[key + "Sha256"]
    artifacts = {}
    for key, name in [("appApk", "n1-batch-095-combined-698-app.apk"),
                      ("testApk", "n1-batch-095-combined-698-test.apk")]:
        path = C / "artifacts" / name
        artifacts[key] = {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size}
    assert artifacts["appApk"]["sha256"] == "0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407"
    target = C / "batch-095-combined-native-698-compiled.json"
    assert not target.exists()
    save(target, {"fixtureVerification": verification, **artifacts})
    print("Combined fixture compiled; app APK unchanged; dedicated worktrees clean.")


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "compiled": compiled}[sys.argv[1]]()
