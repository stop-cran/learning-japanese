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
LOG = C / "logs" / "304b2e80-115b-491d-957c-a2ae713f67a3"
HEAD = "cab46bf2e9c68cc3c7bf03479922a1ef89696bcb"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
BEFORE = C / "artifacts" / "execution-574-progress-before.json"
ATTEMPT = C / "artifacts" / "batch-083-native-attempt-574"
FOLDER = R / "docs" / "n1-reviews" / "batch-083-native" / "attempt-574"
EVIDENCE = R / "docs" / "n1-sources" / "execution-574.json"
NEXT = (
    "SAME083 corrective source/quiz-choice checkpoint next; no084/publication. Read execution-574.json "
    "and immutable batch-083-native/attempt-574 receipts FIRST. Actual native glyph case terminal0, "
    "article case terminal-2 at exact meaning-options assertion: expected 凌/准/冶/次, actual "
    "准/凌/冶/麟. 次 is preserved N3 and absent from N1 quiz pool. Production QuizViewModel "
    "filters all by selected stack before QuizBuilder maps curated distractors, then fills from "
    "random same-pool candidates. This is a content/fixture curation assumption, NOT evidence of "
    "an app regression or an ambiguous answer in this draw. Do not weaken the assertion, enlarge "
    "the selected pool, change 次's easier level, seed padding, alter quiz algorithms or approve "
    "random fallback as the reviewed set. Source-verify a defensibly wrong N1 third distractor "
    "using complete applicable frozen families/actual article, inspect ordinary secondary senses, "
    "audit both N1 and all-stack options and every affected direct guard, make smallest content "
    "correction with manifest/validator and normally signed LOCAL freeze. Preserve original initial "
    "reviews and obtain bounded changed-choice confirmations from original serial Claude/GPT "
    "sessions in batch-083-reconciliation.json, with actual diff/source evidence, then refresh "
    "affected HOST/full archive/native fixture/APK acceptance on corrected snapshot. Original "
    "failed fixture/APKs/archive/reports/attempt remain immutable. No fresh compile/HOST/initial "
    "review was done in574. Full import ONCE1095/5052/115/a9faafdd68af3230/zeroProblems/epoch1 "
    "and two reciprocal pairs/four directions/three complete article routes actually reached; "
    "reading quiz, meaning feedback, drawing and final persistence NOT reached. Six PNGs directly "
    "inspected (threefontpanels and kanji21/endure05/surpass12), all46 saved; do not claim all46 "
    "inspected. All29Han/fourfonts116individual+8wholeword Paint and glyph case passed, actual "
    "fallback panels readable; not phone/native-speaker/fallback-face identity certification. "
    "Need BOTH corrected named terminal0/no skips/no-2/-3 and direct changed PNG inspection, "
    "original serial two-family dependent visual confirmation BEFORE latest-main combined checks, "
    "normally signed integration/ownerfastforward/exactremote/terminalgreenCI/EVERYimmutableZIP"
    "hash/budgets/ownerissue60. Parent19008 lock lifetime remains untouched; fresh localANDremote"
    "5580/5581 includingTimeWait/device/PID/ancestry ownership before any retry, unchanged readonly"
    "AVD/API35/hostGPU/-Vulkan/2048MiB2cores, owned-only cleanup. Prior owned4820/qemu6592 "
    "stopped. Approved control helpers/committed evidence only; preserve/report/yield actual "
    "new denial/signinghang. Published109/1228,remaining1119/latestpublic21a5cb1328aadd437139a6b850"
    "f07298a2e2985d unchanged;083 not delivered. Physicalphone/generalrelease/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "log", "-1", "--format=%G?") == "G"
    assert not git(root, "status", "--porcelain")


def update(p):
    temporary = C / "progress.574.tmp"
    assert not temporary.exists()
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")


def inputs():
    e = load(R / "docs" / "n1-sources" / "execution-573.json")
    f = e["fixtureVerification"]
    for key in ("testApk", "appApk"):
        assert sha(Path(e[key]["path"])) == e[key]["sha256"]
    for key in ("fixture", "archive"):
        assert sha(Path(f[key])) == f[key + "Sha256"]
    assert f == load(C / "batch-083-native-fixture-verification.json")
    assert not git(A, "diff", e["productionBaseline"], APP, "--",
                   "app/src/main", "core/src/main", "gradle.properties")
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest["contentVersion"] == "a9faafdd68af3230"
    with zipfile.ZipFile(f["archive"]) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) == 8398
        prefix = names[0].split("/")[0] + "/"
        assert json.loads(archive.read(prefix + "manifest.json")) == manifest
        verified = 0
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, expected in entries.items():
                data = archive.read(prefix + name)
                if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == expected, name
                verified += 1
        assert verified == 8376
    with zipfile.ZipFile(e["testApk"]["path"]) as archive:
        assert hashlib.sha256(archive.read("assets/" + Path(f["archive"]).name)).hexdigest() == f["archiveSha256"]
    return e


def start():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 573 and p["status"] == "continue" and p["batch"] == "083"
    assert not BEFORE.exists()
    clean(R, HEAD)
    clean(A, APP)
    inputs()
    request = LOG / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 573
    shutil.copyfile(C / "progress.json", BEFORE)
    state = {
        "execution": 574, "batch": "083", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "scope": "SAME083 frozen native execution and direct PNG inspection, signed LOCAL evidence checkpoint; no reviewer/integration/publication/084.",
        "request": {"sha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Operative contract, full approved issue and final checkpoint inspected directly; historical middle loaded/parsed, not freshly semantically re-reviewed."},
        "runtimeManifestHashesVerified": 8376,
        "runnerLockRole": "Live parent PID19008 verified as coordinator ancestor; child never opens/reacquires/deletes/unlocks runner.lock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    p["execution574StartingState"] = state
    p["stage"] = "batch-083-native-execution-in-progress"
    p["nextAction"] = state["scope"]
    update(p)
    save(C / "execution-574-start.json", state)
    print("SAME083 starting scope persisted; 8376 archive hashes and frozen APKs verified.")


def record():
    clean(R, HEAD)
    clean(A, APP)
    prior = inputs()
    receipt = load(C / "batch-083-native-attempt-574-execution.json")
    assert receipt["nativeExecuted"] and not receipt["passed"]
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"] and receipt["stopAdbExitCode"] == 0
    assert not any(receipt[k] for k in ("parentLockTouched", "guestOrAppHeapChanged", "guardsChanged", "hostHeapInitUsed"))
    raw = (ATTEMPT / "instrumentation.txt").read_text(encoding="utf-8-sig")
    cases = []
    fields = {}
    for line in raw.splitlines():
        if line.startswith("INSTRUMENTATION_STATUS: "):
            name, value = line.removeprefix("INSTRUMENTATION_STATUS: ").split("=", 1)
            fields[name] = value
        elif line.startswith("INSTRUMENTATION_STATUS_CODE: "):
            code = int(line.split(": ", 1)[1])
            if code != 1:
                cases.append({"class": fields["class"], "test": fields["test"], "status": code})
            fields = {}
    assert cases == [
        {"class": "io.github.stopcran.kanji.ui.N1Batch083ArticleTest",
         "test": "fullSingleImportOfflineEnduranceTwoReciprocalPairsCuratedOnAndKunDrawingAndSystemBack", "status": -2},
        {"class": "io.github.stopcran.kanji.ui.N1Batch083GlyphTest",
         "test": "enduranceLookalikesAndRadicalFallbacksAcrossFourProductionFamilies", "status": 0},
    ]
    assert "Tests run: 2,  Failures: 1" in raw
    route = load(ATTEMPT / "n1-083-article-route.json")
    assert route["archiveRequests"] == 1 and route["importedKanji"] == 1095
    assert route["importedWords"] == 5052 and route["n1Cards"] == 115 and route["problems"] == 0
    assert route["contentVersion"] == "a9faafdd68af3230" and route["acceptedReadingParserEpoch"] == 1
    assert route["reciprocalLinkAndSystemBack"] and route["mappedReciprocalPairs"] == 2
    assert route["directedLinkTransitions"] == 4 and route["completeArticleProjections"] == 3
    assert route["quizOnKeys"] == ["りょう"] and route["quizKunKeys"] == ["しのぐ"]
    assert not route["passed"]
    raster = load(ATTEMPT / "n1-083-font-raster.json")
    glyphs = [r for r in raster["rows"] if "character" in r]
    words = [r for r in raster["rows"] if "word" in r]
    assert len(glyphs) == 116 and len(words) == 8
    assert {r["character"] for r in glyphs} == set(prior["fixtureVerification"]["plannedGlyphs"])
    assert all(r["hasGlyph"] for r in glyphs)
    assert all(r["renderedCharactersNonblank"] == len(r["word"]) for r in words)
    for font in {r["font"] for r in glyphs}:
        assert len({r["nativePaintRasterSha256"] for r in glyphs if r["font"] == font}) == 29
    pngs = sorted(ATTEMPT.glob("*.png"))
    assert len(pngs) == 46
    inspected = ["n1-083-font-panel-1.png", "n1-083-font-panel-2.png", "n1-083-font-panel-3.png",
                 "n1-083-kanji-21.png", "n1-083-endure-word-05.png", "n1-083-surpass-word-12.png"]
    assert all((ATTEMPT / n).exists() for n in inspected)
    assert not FOLDER.exists()
    shutil.copytree(ATTEMPT, FOLDER)
    source_folder = FOLDER / "provenance"
    source_folder.mkdir()
    sources = [Path(__file__), C / "run-574-native.ps1", C / "runner-lock-role-notes.txt",
               C / "authoring-artifact-path-notes.txt"]
    source_code = [
        A / "app" / "src" / "main" / "java" / "io" / "github" / "stopcran" / "kanji" / "ui" / "QuizViewModel.kt",
        A / "core" / "src" / "main" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "quiz" / "QuizBuilder.kt",
        R / "kanji" / "次.md",
    ]
    sources += source_code
    provenance = []
    for source in sources:
        target = source_folder / source.name
        shutil.copyfile(source, target)
        provenance.append({"source": str(source), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    index = [{"path": item.relative_to(FOLDER).as_posix(), "sha256": sha(item), "bytes": item.stat().st_size}
             for item in sorted(FOLDER.rglob("*")) if item.is_file()]
    save(FOLDER / "artifact-index.json", index)
    evidence = {
        "schemaVersion": 1, "execution": 574, "batch": "083",
        "status": "native-failed-exact-n1-choice-gate-correction-required",
        "startingState": load(C / "execution-574-start.json"),
        "contentSnapshot": prior["contentSnapshot"], "teachingSnapshot": prior["teachingSnapshot"],
        "coordinatorHead": HEAD, "androidHead": APP, "productionBaseline": prior["productionBaseline"],
        "nativeReceipt": receipt, "independentlyParsedTerminalCases": cases,
        "nativeAcceptancePassed": False, "nativeCases": 2, "passedCases": 1, "failedCases": 1,
        "skippedCases": 0, "nativeAdbExitCode": receipt["adbExitCode"],
        "adbZeroDoesNotMeanTestSuccess": True, "productionImportAndCompletedRouteEvidence": route,
        "glyphProbes": {"individual": 116, "wholeWord": 8, "fonts": 4, "distinctHan": 29,
                        "allIndividualHasGlyph": True, "distinctIndividualRasterHashesWithinEachFont": True},
        "directPngInspection": {
            "reviewer": "Coordinator GPT-6.1 Sol (gpt-6.1-sol)", "independentReviewer": False,
            "files": inspected, "savedPngCount": 46, "notDirectlyInspectedPngCount": 40,
            "observation": "All 29 Han across all four family panels and both whole words are visibly nonblank and distinguishable on this API35 render. 凌/陵/准/冶/次 remain distinguishable; 冫/夌/阝/隹 fallback glyphs readable, some fallback shapes coincide across families. Three inspected article frames have readable scoped notes, conjugation/transitivity and rare-spelling guidance; long surrounding content may extend beyond the viewport.",
            "limits": "Only six listed PNGs directly inspected. Not all article screenshots, independent two-family visual confirmation, physical-phone readability, fallback-face identity or native-speaker certification.",
        },
        "finding": {
            "id": "083-NATIVE-574-CHOICE", "severity": "minor", "facet": "scoped coverage / live quiz curation",
            "status": "unresolved", "confidence": "high", "publicationBlocking": True,
            "file": "kanji/凌.md:13",
            "claim": "次 is N3, absent from the N1 option pool. Three configured distractors therefore do not yield the required exact reviewed N1 option set.",
            "expectedOptions": {"凌": "endure; surpass", "准": "quasi-; associate rank", "冶": "smelt; work metals", "次": "next"},
            "actualOptions": {"准": "quasi-; associate rank", "凌": "endure; surpass", "冶": "smelt; work metals", "麟": "qilin; mythical animal"},
            "evidence": [
                "Attempt instrumentation names article test with terminal -2 at N1Batch083NativeTest.kt:365, and prints exact expected/actual maps.",
                "kanji/次.md:4 preserves jlpt3.",
                "QuizViewModel.kt:91-97 filters cards with inStack(stack) and creates quizCards from that selected pool; ask at164-166 passes quizCards to QuizBuilder.",
                "QuizBuilder.kt:16-28 resolves curated distractors only inside supplied pool, then fills from shuffled same-pool cards.",
            ],
            "impact": "Only two reviewed curated distractors participate in N1; third is random fallback. This draw's 麟 label is not demonstrated semantically ambiguous, but it does not satisfy the exact reviewed-set acceptance gate.",
            "remedy": "Source-verify and review an appropriate N1 third distractor, preserving 次's easier level and app algorithms; update affected guards/fixture and rerun corrected snapshot gates. Do not simply weaken assertion or enlarge pool.",
            "scope": "Content/fixture authoring assumption exposed by unchanged production behavior, not an established app regression.",
        },
        "notReached": ["meaning feedback", "live curated on/kun questions and persisted logs",
                       "full card reading projection assertion", "10-stroke tracing", "recall drawing",
                       "final offline and persistence assertions"],
        "artifacts": FOLDER.relative_to(R).as_posix(), "artifactIndexSha256": sha(FOLDER / "artifact-index.json"),
        "provenance": provenance, "runtimeManifestHashesVerified": 8376, "runtimeChanged": False,
        "runtimePublished": False, "runtimeAccepted": False, "hostChecksRerun": False,
        "independentReviewersLaunched": 0, "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": "21a5cb1328aadd437139a6b850f07298a2e2985d",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "limits": "Native attempt failed overall. Glyph case terminal0 is not full batch acceptance. Original source/reviewer/read-depth/OOM/fallback/MLKit/phone/publication limits retained. No teaching or production changes, no repeated HOST checks/reviews, no new denial. Original fixture/APKs/archive/reports retained unchanged.",
        "nextGate": NEXT,
    }
    save(EVIDENCE, evidence)
    print("Failed native gate and exact root cause archived; glyph pass/partial route distinguished.")


def finish():
    clean(A, APP)
    assert git(R, "log", "-1", "--format=%G?") == "G"
    assert not git(R, "status", "--porcelain")
    assert not git(R, "diff", HEAD, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    inputs()
    evidence = load(EVIDENCE)
    assert not evidence["nativeAcceptancePassed"] and evidence["finding"]["status"] == "unresolved"
    p = load(C / "progress.json")
    before = load(BEFORE)
    assert p["checkpoint"] == 573 and p["batch"] == "083"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert p[key] == value, key
    summary = {
        "schemaVersion": 1, "execution": 574, "checkpoint": 574, "batch": "083",
        "savedCommit": git(R, "rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": "native-failed-exact-n1-choice-correction-required",
        "evidence": EVIDENCE.relative_to(R).as_posix(), "contentSnapshot": evidence["contentSnapshot"],
        "androidHead": APP, "nativeExecuted": True, "nativeAcceptancePassed": False,
        "nativeTerminalCases": evidence["independentlyParsedTerminalCases"],
        "newFinding": evidence["finding"], "directPngInspection": evidence["directPngInspection"],
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "hostChecksRerun": False, "independentReviewersLaunched": 0,
        "publishedAdditions": 109, "remainingAdditions": 1119, "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "ownedEmulatorStopped": True, "parentLockTouched": False, "dedicatedWorktreesClean": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    for key in ("checkpoint", "status", "stage", "nextAction"):
        p[key] = summary[key]
    p["blocker"] = None
    p["execution574CoordinatorCheckpoint"] = summary
    p["batch083NativeFailedChoiceCheckpoint"] = summary
    update(p)
    save(C / "execution-574-checkpoint.json", summary)
    print("Checkpoint574 continue: same083 source-verified corrective choice next; both worktrees clean.")


if __name__ == "__main__":
    {"start": start, "inputs": inputs, "record": record, "finish": finish}[sys.argv[1]]()
