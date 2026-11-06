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
SOURCE = CONTROL / "artifacts" / "batch-076-native-attempt-1"
DESTINATION = CONTENT / "docs" / "n1-reviews" / "batch-076-native" / "attempt-1"
RECEIPTS = DESTINATION.parent / "execution-receipts"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


execution = load(SOURCE / "execution.json")
route = load(SOURCE / "n1-076-article-route.json")
fonts = load(SOURCE / "n1-076-font-raster.json")
preparation = load(CONTENT / "docs" / "n1-sources" / "batch-076-native-preparation.json")
fixture = SOURCE / "N1Batch076NativeTest.kt"
assert digest(fixture) == preparation["fixtureSha256"]
assert execution["passed"] and execution["failure"] is None
assert execution["terminalSuccessCases"] == 2
assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
assert execution["stopAdbExitCode"] == 0
assert execution["parentEmulatorPid"] == 27628 and execution["qemuPid"] == 29744
assert all(case["status"] == 0 for case in execution["terminalCases"])
raw = (SOURCE / "instrumentation.txt").read_text(encoding="utf-8-sig")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$", raw, re.M) == ["1", "0", "1", "0"]
assert "OK (2 tests)" in raw and "INSTRUMENTATION_CODE: -1" in raw
assert "skipped" not in raw.lower() and "FAILURES" not in raw
for key, value in {
    "contentSnapshot": preparation["contentSnapshot"],
    "contentVersion": "8bd0a375668bee11",
    "archiveRequests": 1,
    "importedKanji": 1088,
    "importedWords": 5045,
    "n1Cards": 108,
    "problems": 0,
    "acceptedReadingParserEpoch": 1,
    "fullOnyomi": ["ケン"],
    "fullKunyomi": ["か.ねる", "-か.ねる"],
    "quizOnKeys": ["けん"],
    "quizKunKeys": ["かねる"],
    "liteQuizOnyomi": ["ケン"],
    "liteQuizKunyomi": ["か.ねる"],
    "fullProjectionOnyomi": ["ケン"],
    "fullProjectionKunyomi": ["か.ねる", "-か.ねる"],
    "fullProjectionQuizOnyomi": ["ケン"],
    "fullProjectionQuizKunyomi": ["か.ねる"],
    "mappedReciprocalPairs": 3,
    "directedLinkTransitions": 6,
    "touchInjectedReferenceStrokes": 10,
    "bothCuratedKindsPersistedGoodNoDuplicateSuffixAndDone": True,
    "meaningQuestionAndFeedback": True,
    "reciprocalLinkAndSystemBack": True,
    "drawingTraceThenRecall": True,
    "drawingGradeRecordedOnNext": True,
    "offline": True,
    "phoneEvidence": False,
    "passed": True,
}.items():
    assert route[key] == value, (key, route[key], value)
assert fonts["individualGlyphProbes"] == 164
assert fonts["wholeWordRasterProbes"] == 8 and fonts["panels"] == 3
assert len(fonts["rows"]) == 172
assert collections.Counter(row["font"] for row in fonts["rows"]) == {
    "Gothic": 43, "Mincho": 43, "Textbook": 43, "Brush": 43,
}
glyph_rows = [row for row in fonts["rows"] if "character" in row]
assert {row["character"] for row in glyph_rows} == set(preparation["plannedGlyphs"])
assert all(row["hasGlyph"] for row in glyph_rows)
for family in ["Gothic", "Mincho", "Textbook", "Brush"]:
    family_rows = [row for row in glyph_rows if row["font"] == family]
    assert len({row["nativePaintRasterSha256"] for row in family_rows}) == 41
    words = [row for row in fonts["rows"] if row["font"] == family and "word" in row]
    assert {row["word"] for row in words} == {"兼任", "兼ねる"}
    assert all(row["renderedCharactersNonblank"] == len(row["word"]) for row in words)
text = fixture.read_text(encoding="utf-8")
steps = set(re.findall(r'^\s*capture\("([^"]+)"\)', text, re.M))
steps.update(re.findall(r'^\s*show\(.+, "([^"]+)"\)$', text, re.M))
steps = {step for step in steps if "$" not in step}
steps.update(f"curated-{kind}-{stage}" for kind in ["On", "Kun"] for stage in ["question", "feedback"])
steps.update(f"font-panel-{index}" for index in range(1, 4))
expected_images = {f"n1-076-{step}.png" for step in steps}
actual_images = {path.name for path in SOURCE.glob("*.png")}
assert expected_images == actual_images, (expected_images - actual_images, actual_images - expected_images)
for path in SOURCE.glob("*.png"):
    with Image.open(path) as image:
        image.verify()
viewed = load(CONTROL / "execution-509-viewed.json")
assert set(viewed) <= actual_images
assert {f"n1-076-font-panel-{index}.png" for index in range(1, 4)} <= set(viewed)
assert len(viewed) == len(set(viewed))
assert not DESTINATION.exists(), "Refusing to overwrite archived evidence"
DESTINATION.mkdir(parents=True)
for path in SOURCE.iterdir():
    if path.is_file():
        shutil.copy2(path, DESTINATION / path.name)
RECEIPTS.mkdir(exist_ok=True)
for name in ["execution-509.py", "run-509-native.ps1", "run-509-native-expanded.ps1", "execution-509-viewed.json"]:
    shutil.copy2(CONTROL / name, RECEIPTS / name)

next_action = (
    "SAME076 two SERIAL different-family independent visual confirmations next, reusing original "
    "sessions Claude c756ba32-4429-4032-a560-5398a8a951ea and GPT d4d10d28-2c99-4d72-b5ed-a736b65621a0 "
    "where possible. Confirm current actual catalog/model identity and supported read-only tools; "
    "one reviewer process at a time, serial internal tools, no nested/parallel tasks; preserve actual exit "
    "and full report/events before next. No native rerun absent new concern, no publication/077. "
    "Read docs\\n1-sources\\execution-509.json and docs\\n1-reviews\\batch-076-native\\attempt-1. "
    "Both named native cases terminal0, zero skips; actual full signedb89b3336 archive production "
    "ContentSync ONCE:1088kanji5045words108N1,version8bd0a375668bee11,problems0,epoch1. "
    "Full+Lite rawケン andか.ねる/-か.ねる source order; curatedケン/か.ねる, actualけん/かねる "
    "each Good/Done2correct without duplicate suffix question/log. Complete兼/兼任, exact changed "
    "兼ねる two linked paragraphs and任 bullet, all3mappedpairs6directions; selection/meaning/readings/"
    "ten-stroke reference-touch/ungradedtrace/recallAgain/articles/SystemBack/offline. "
    "41scopedHan across4productionfamilies in two bounded panels plus focused兼/典/具/曲/八/人/亻 "
    "and兼任/兼ねる panel; two wholewordrasters per family. Coordinator sample and actual PNG counts "
    "are recorded, NOT independent visual acceptance. Cmapabsence NOTglyphfailure; hashes NOT "
    "readability/fallbackface. Table labels/examples captured separately after horizontal scrolling. "
    "Reference-injected drawing NOT humanhandwriting/MLKit evidence; model unavailable offline. "
    "Owned emulator5580 parent27628/QEMU29744 stopped; shared5556 untouched; actual post-stop "
    "ownership evidence retained, not blanket allconnectionsabsence. Fresh507HOST3+1 retained; "
    "no redundant rerun. Later currentmainnormalmerge/revalidation/normalsigning/ownerfastforward/"
    "greenCI/EVERYimmutableZIPhash/originalbudgets/ownerissue60receipt remain. No teachingchanges/"
    "unreviewedpush/signingretry/permissionworkaround/heaporguardchanges/authoragents/secondrunner. "
    "Preserve FULLlivehistory, source recipes, originalreports and reviewedbaseline虎/猿/丘/山exceptions. "
    "Published102/1228,remaining1126; necessarysupportsNOTN1vocabulary. CompatibleAndroidf9b59a2+ "
    "required; physicalphone/generalrelease/whole-set outstanding. Overall project incomplete."
)
record = {
    "schemaVersion": 1,
    "execution": 509,
    "checkpoint": 509,
    "batch": "076",
    "status": "native-passed-awaiting-independent-visual-confirmation",
    "startingHead": "b8a999695d67981e270e7a4fea559b712b26cf9b",
    "reviewedTeachingSnapshot": "08d63143e0495940d7cccee4c1808282a533c522",
    "recordedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "authorization": load(CONTROL / "progress.json")["execution509StartingState"]["authorization"],
    "originMainFreshFetch": subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=CONTENT, text=True).strip(),
    "nativeExecution": execution,
    "postStopOwnership": load(SOURCE / "post-stop-ownership.json"),
    "nativeAssertionsReverified": True,
    "nativeSkippedCases": 0,
    "routeEvidence": route,
    "pngCount": len(actual_images),
    "pngSetMatchesEveryFixtureCapture": True,
    "glyphEvidence": {
        "authoredHan": 41,
        "families": 4,
        "individualGlyphProbes": 164,
        "wholeWordRasterProbes": 8,
        "totalRows": 172,
        "panels": 3,
        "coordinatorViewedAllThreeActualPanels": True,
        "observed": "No blank/replacement glyph or collapsed look-alike established in the three inspected panels; 人/亻 and focused contrasts visible. Typeface differences are not defects.",
        "limits": "Paint hasGlyph and raster hashes do not identify fallback faces or prove readability. PNG inspection is emulator-only, not phone/native-speaker approval.",
    },
    "coordinatorVisualInspection": {
        "reviewer": "Coordinator, actual model gpt-6.1-sol; NOT independent",
        "viewToolActualOriginalPngs": viewed,
        "viewedCount": len(viewed),
        "notViewedCount": len(actual_images) - len(viewed),
        "noActionableDefectEstablishedInViewedSample": True,
        "tableScrollQualification": "Example-column captures can leave reading labels partly offscreen after horizontal scrolling. Separate label captures exist; no claim every column is simultaneously visible.",
        "drawingQualification": "Ten touch-injected reference strokes; ungraded trace and recall Again. Handwriting model unavailable offline, as displayed; no human handwriting or MLKit evidence.",
        "limits": "Bounded actual PNG sample, not all captures. Independent visual review and physical-phone acceptance remain outstanding.",
    },
    "accepted507HostCasesRetainedWithoutRerun": 4,
    "accepted507HostSkips": 0,
    "runtimeEditsMade": False,
    "reviewersLaunched": 0,
    "independentVisualAcceptance": False,
    "publicationAttempted": False,
    "runtimePublished": False,
    "publishedAdditions": 102,
    "remainingAdditions": 1126,
    "nextAction": next_action,
    "limits": "Native two-case pass is not batch publication or independent visual acceptance. No guest/app heap change, guard change, app edit, phone test, reviewer or next batch. Whole project incomplete.",
}
artifacts = []
for directory in [DESTINATION, RECEIPTS]:
    for path in sorted(directory.iterdir()):
        if path.is_file():
            row = {"path": str(path.relative_to(CONTENT)), "bytes": path.stat().st_size, "sha256": digest(path)}
            if path.suffix == ".png":
                with Image.open(path) as image:
                    row["dimensions"] = list(image.size)
                row["coordinatorViewed"] = path.name in viewed
            artifacts.append(row)
record["artifacts"] = artifacts
record_path = CONTENT / "docs" / "n1-sources" / "execution-509.json"
assert not record_path.exists()
save(record_path, record)
print(json.dumps({
    "status": record["status"], "nativeCases": 2, "skips": 0,
    "pngs": len(actual_images), "coordinatorViewed": len(viewed),
    "archivedArtifacts": len(artifacts), "recordSha256": digest(record_path),
}, ensure_ascii=False))
