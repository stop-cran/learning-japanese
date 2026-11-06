import collections
import datetime
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image


CONTROL = Path(__file__).resolve().parent
CONTENT = CONTROL.parent / "learning-japanese"
SOURCE = CONTROL / "artifacts" / "batch-075-native-attempt-1"
DESTINATION = CONTENT / "docs" / "n1-reviews" / "batch-075-native" / "attempt-1"
RECEIPTS = DESTINATION.parent / "execution-receipts"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


execution = load(SOURCE / "execution.json")
route = load(SOURCE / "n1-075-article-route.json")
fonts = load(SOURCE / "n1-075-font-raster.json")
preparation = load(CONTENT / "docs" / "n1-sources" / "batch-075-native-preparation.json")
fixture = SOURCE / "N1Batch075NativeTest.kt"
assert digest(fixture) == preparation["fixtureSha256"]
assert execution["passed"] and execution["failure"] is None
assert execution["terminalSuccessCases"] == 2
assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
assert execution["stopAdbExitCode"] == 0
assert execution["parentEmulatorPid"] == 24028 and execution["qemuPid"] == 30848
assert all(case["status"] == 0 for case in execution["terminalCases"])
raw = (SOURCE / "instrumentation.txt").read_text(encoding="utf-8-sig")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$", raw, re.M) == ["1", "0", "1", "0"]
assert "OK (2 tests)" in raw and "INSTRUMENTATION_CODE: -1" in raw
assert "skipped" not in raw.lower() and "FAILURES" not in raw
for key, value in {
    "contentSnapshot": preparation["contentSnapshot"],
    "contentVersion": "2759d7b13c89eb8f",
    "archiveRequests": 1,
    "importedKanji": 1087,
    "importedWords": 5044,
    "n1Cards": 107,
    "problems": 0,
    "acceptedReadingParserEpoch": 1,
    "fullOnyomi": ["テン", "デン"],
    "fullKunyomi": ["ふみ", "のり"],
    "quizOnKeys": ["てん", "でん"],
    "quizKunKeys": [],
    "liteQuizOnyomi": ["テン", "デン"],
    "liteQuizKunyomi": [],
    "fullProjectionOnyomi": ["テン", "デン"],
    "fullProjectionKunyomi": ["ふみ", "のり"],
    "fullProjectionQuizOnyomi": ["テン", "デン"],
    "fullProjectionQuizKunyomi": [],
    "mappedReciprocalPairs": 12,
    "directedLinkTransitions": 24,
    "touchInjectedReferenceStrokes": 8,
    "bothCuratedOnKeysPersistedGoodNoKunAndDone": True,
    "meaningQuestionAndFeedback": True,
    "reciprocalLinkAndSystemBack": True,
    "drawingTraceThenRecall": True,
    "drawingGradeRecordedOnNext": True,
    "offline": True,
    "phoneEvidence": False,
    "passed": True,
}.items():
    assert route[key] == value, (key, route[key], value)
assert fonts["individualGlyphProbes"] == 468
assert fonts["wholeWordRasterProbes"] == 24 and fonts["panels"] == 6
assert len(fonts["rows"]) == 492
assert collections.Counter(row["font"] for row in fonts["rows"]) == {
    "Gothic": 123, "Mincho": 123, "Textbook": 123, "Brush": 123,
}
glyph_rows = [row for row in fonts["rows"] if "character" in row]
assert len({row["character"] for row in glyph_rows}) == 117
assert all(row["hasGlyph"] for row in glyph_rows)
for family in ["Gothic", "Mincho", "Textbook", "Brush"]:
    family_rows = [row for row in glyph_rows if row["font"] == family]
    assert len({row["nativePaintRasterSha256"] for row in family_rows}) == 117
    words = [row for row in fonts["rows"] if row["font"] == family and "word" in row]
    assert {row["word"] for row in words} == {"典型", "古典", "百科事典", "辞典", "香典", "香奠"}
    assert all(row["renderedCharactersNonblank"] == len(row["word"]) for row in words)
text = fixture.read_text(encoding="utf-8")
steps = set(re.findall(r'^\s*capture\("([^"]+)"\)', text, re.M))
steps.update(re.findall(r'^\s*show\(.+, "([^"]+)"\)$', text, re.M))
steps = {step for step in steps if "$" not in step}
steps.update(f"curated-{key}-{stage}" for key in ["てん", "でん"] for stage in ["question", "feedback"])
steps.update(f"font-panel-{index}" for index in range(1, 7))
expected_images = {f"n1-075-{step}.png" for step in steps}
actual_images = {path.name for path in SOURCE.glob("*.png")}
assert expected_images == actual_images, (expected_images - actual_images, actual_images - expected_images)
assert len(actual_images) == 111
for path in SOURCE.glob("*.png"):
    with Image.open(path) as image:
        image.verify()
assert not DESTINATION.exists(), "Refusing to overwrite archived evidence"
DESTINATION.mkdir(parents=True)
for path in SOURCE.iterdir():
    if path.is_file():
        shutil.copy2(path, DESTINATION / path.name)
RECEIPTS.mkdir(exist_ok=True)
for name in ["execution-501.py", "run-501-native.ps1"]:
    shutil.copy2(CONTROL / name, RECEIPTS / name)

viewed = [f"n1-075-font-panel-{index}.png" for index in range(1, 7)] + [
    "n1-075-kanji-20.png",
    "n1-075-香典-08.png",
    "n1-075-curated-てん-question.png",
    "n1-075-curated-でん-feedback.png",
    "n1-075-curated-two-on-done.png",
    "n1-075-drawing-trace.png",
    "n1-075-drawing-feedback.png",
    "n1-075-drawing-recall-feedback.png",
    "n1-075-selection.png",
    "n1-075-meaning-feedback.png",
    "n1-075-curated-てん-feedback.png",
    "n1-075-curated-でん-question.png",
    "n1-075-kanji-11.png",
    "n1-075-kanji-17.png",
    "n1-075-香典-03.png",
    "n1-075-百科事典-07.png",
    "n1-075-古典-古-system-back-to-component.png",
    "n1-075-辞典-辞-component-backlink.png",
    "n1-075-香典-香-system-back-to-component.png",
]
assert len(viewed) == len(set(viewed)) == 25
assert set(viewed) <= actual_images
next_action = (
    "SAME075 two SERIAL different-family independent visual confirmations next, reusing original sessions "
    "where possible; no native rerun absent new concern, no publication/076 this checkpoint. "
    "Frozen signed native evidence at docs\\n1-sources\\execution-501.json and "
    "docs\\n1-reviews\\batch-075-native\\attempt-1; 111 actual PNGs, both named terminal0/zero skips. "
    "Use original Claude9fa0573b-2a16-4020-95ca-b6db67263344 and GPTf8bb1a1f-8f2e-469d-a486-7874e1b6f3da "
    "where available, confirm actual current model catalog/identity and supported read-only tools. "
    "One reviewer PROCESS at a time; each reviewer ONE resource/tool call per response, no nested/parallel tools; "
    "verify process exit and archive original report/events before next. Same frozen teachingf5b70805, "
    "native archivefba1a886 version2759d7b13c89eb8f, Androidf9b59a2. Complete典/香典, "
    "four changed reused component passages, six olderkanji navigation edits, all12mappedpairs24directions "
    "including unchanged型, full rawテン/デン andふみ/のり source order with curatedテン/デン+emptykun, "
    "actualてん/でん two correct/Done/noKunLog, eight-stroke reference-touch/ungradedtrace/recallAgain, "
    "selection/meaning/articles/SystemBack/offline. All117 scopedHan across four production families "
    "in five panels plus focused奠/亅/厂/艹+lookalikes/sixwholewords panel. "
    "Coordinator actually viewed25/111 PNGs including all6fontpanels, not full screenshot review or "
    "independent acceptance. Table examples can be horizontally shifted (reading labels separately captured); "
    "assess actual targets, not entire adjacent screens. Paint/cmap/hash evidence NOT readability/fallback-face identity. "
    "Drawing is reference-injected, not human handwriting/MLKit; model unavailable offline. "
    "Owned emulator5580 parent24028/QEMU30848 stopped, shared5556/10668/18200 unchanged; "
    "post-stop residual TCP states preserved, no blanket claim all connections absent. "
    "Fresh499HOST3+1 retained; no redundant rerun. OriginalClaude8multi-toolresponses/"
    "30overlappingstarts/false serial claim preserved; later actualserial confirmation not retroactive compliance. "
    "Then evidence-based visual reconciliation; later currentmainnormalmerge/revalidation/normalsigning/"
    "ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets/ownerissue60receipt remain. "
    "No teaching changes/unreviewedpush/signingretry/permissionworkaround/heaporguardchanges/"
    "authoragents/secondrunner. Preserve FULLlivehistory, originalreports/faileddiagnostics and "
    "reviewedbaseline虎/猿/丘/山exceptions plus inheritedaccepted074 evidence honestly. "
    "Published101/1228,remaining1127; necessarysupportsNOTN1vocabulary. CompatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overall project incomplete."
)
record = {
    "schemaVersion": 1,
    "execution": 501,
    "checkpoint": 501,
    "batch": "075",
    "status": "native-passed-awaiting-independent-visual-confirmation",
    "startingHead": "1ae9135616852380db2cf1d7cc5a369da5ab7d3e",
    "reviewedTeachingSnapshot": "f5b70805d4a4a99d27036c71701277f1b8fc8b00",
    "recordedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "authorization": load(CONTROL / "progress.json")["execution501StartingState"]["authorization"],
    "originMainFreshFetch": subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=CONTENT, text=True).strip(),
    "nativeExecution": execution,
    "postStopOwnership": load(SOURCE / "post-stop-ownership.json"),
    "nativeAssertionsReverified": True,
    "evidenceRecipeDiagnostic": "Initial capture-set audit mistakenly treated two Kotlin $key interpolation templates as literal filenames; failed before copying evidence. Recipe excludes interpolation templates and separately enumerates all four actual reading captures. This was not a native failure or changed fixture.",
    "nativeSkippedCases": 0,
    "routeEvidence": route,
    "pngCount": 111,
    "pngSetMatchesEveryFixtureCapture": True,
    "glyphEvidence": {
        "authoredHan": 117,
        "families": 4,
        "individualGlyphProbes": 468,
        "wholeWordRasterProbes": 24,
        "totalRows": 492,
        "panels": 6,
        "coordinatorViewedAllSixActualPanels": True,
        "observed": "No blank/replacement glyph or collapsed look-alike established in the six inspected panels; four fallback targets remain visible. Different shapes/weights are not defects.",
        "limits": "Paint hasGlyph and raster hashes do not identify fallback faces or prove readability. PNG inspection is emulator-only, not phone/native-speaker approval.",
    },
    "coordinatorVisualInspection": {
        "reviewer": "Coordinator, actual model gpt-6.1-sol; NOT independent",
        "viewToolActualOriginalPngs": viewed,
        "viewedCount": 25,
        "notViewedCount": 86,
        "noActionableDefectEstablishedInViewedSample": True,
        "tableScrollQualification": "Example-column captures can leave reading labels partly offscreen after horizontal scrolling. Separate label captures exist; no claim every column is simultaneously visible.",
        "drawingQualification": "Eight touch-injected reference strokes; ungraded trace and recall Again. Handwriting model unavailable offline, as displayed; no human handwriting or MLKit evidence.",
        "limits": "25 actual PNGs inspected, not all111. Independent visual review and physical-phone acceptance remain outstanding.",
    },
    "accepted499HostCasesRetainedWithoutRerun": 4,
    "accepted499HostSkips": 0,
    "inheritedAccepted074NotFreshlyRecertified": True,
    "originalClaudeConcurrencyBreachPreserved": True,
    "runtimeEditsMade": False,
    "reviewersLaunched": 0,
    "independentVisualAcceptance": False,
    "publicationAttempted": False,
    "runtimePublished": False,
    "publishedAdditions": 101,
    "remainingAdditions": 1127,
    "nextAction": next_action,
    "limits": "Native two-case pass is not batch publication or completed independent visual acceptance. No guest/app heap change, guard change, app edit, phone test, reviewer or next batch. Whole project incomplete.",
}
artifacts = []
for directory in [DESTINATION, RECEIPTS]:
    for path in sorted(directory.iterdir()):
        if path.is_file():
            row = {
                "path": str(path.relative_to(CONTENT)),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
            if path.suffix == ".png":
                with Image.open(path) as image:
                    row["dimensions"] = list(image.size)
                row["coordinatorViewed"] = path.name in viewed
            artifacts.append(row)
record["artifacts"] = artifacts
record_path = CONTENT / "docs" / "n1-sources" / "execution-501.json"
assert not record_path.exists()
save(record_path, record)
print(json.dumps({
    "status": record["status"], "nativeCases": 2, "skips": 0,
    "pngs": 111, "coordinatorViewed": 25, "archivedArtifacts": len(artifacts),
    "recordSha256": digest(record_path),
}, ensure_ascii=False))
