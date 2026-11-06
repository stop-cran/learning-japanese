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
SOURCE = CONTROL / "artifacts" / "batch-077-native-attempt-1"
DESTINATION = CONTENT / "docs" / "n1-reviews" / "batch-077-native" / "attempt-1"
RECEIPTS = DESTINATION.parent / "execution-receipts"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


execution = load(SOURCE / "execution.json")
route = load(SOURCE / "n1-077-article-route.json")
fonts = load(SOURCE / "n1-077-font-raster.json")
preparation = load(CONTENT / "docs" / "n1-sources" / "batch-077-native-preparation.json")
fixture = SOURCE / "N1Batch077NativeTest.kt"
assert digest(fixture) == preparation["fixtureSha256"]
assert execution["passed"] and execution["failure"] is None
assert execution["terminalSuccessCases"] == 2
assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
assert execution["stopAdbExitCode"] == 0
assert execution["parentEmulatorPid"] == 27684 and execution["qemuPid"] == 23940
assert all(case["status"] == 0 for case in execution["terminalCases"])
raw = (SOURCE / "instrumentation.txt").read_text(encoding="utf-8-sig")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$", raw, re.M) == ["1", "0", "1", "0"]
assert "OK (2 tests)" in raw and "INSTRUMENTATION_CODE: -1" in raw
assert "skipped" not in raw.lower() and "FAILURES" not in raw
for key, value in {
    "contentSnapshot": preparation["contentSnapshot"],
    "contentVersion": "2944928c13e2165a",
    "archiveRequests": 1,
    "importedKanji": 1089,
    "importedWords": 5046,
    "n1Cards": 109,
    "problems": 0,
    "acceptedReadingParserEpoch": 1,
    "fullOnyomi": ["ボウ"],
    "fullKunyomi": ["おか.す"],
    "quizOnKeys": ["ぼう"],
    "quizKunKeys": ["おかす"],
    "liteQuizOnyomi": ["ボウ"],
    "liteQuizKunyomi": ["おか.す"],
    "fullProjectionOnyomi": ["ボウ"],
    "fullProjectionKunyomi": ["おか.す"],
    "fullProjectionQuizOnyomi": ["ボウ"],
    "fullProjectionQuizKunyomi": ["おか.す"],
    "mappedReciprocalPairs": 3,
    "directedLinkTransitions": 6,
    "touchInjectedReferenceStrokes": 9,
    "bothCuratedKindsPersistedGoodAndDone": True,
    "meaningQuestionAndFeedback": True,
    "reciprocalLinkAndSystemBack": True,
    "drawingTraceThenRecall": True,
    "drawingGradeRecordedOnNext": True,
    "offline": True,
    "phoneEvidence": False,
    "passed": True,
}.items():
    assert route[key] == value, (key, route[key], value)
assert fonts["individualGlyphProbes"] == 156
assert fonts["wholeWordRasterProbes"] == 8 and fonts["panels"] == 3
assert len(fonts["rows"]) == 164
assert collections.Counter(row["font"] for row in fonts["rows"]) == {
    "Gothic": 41, "Mincho": 41, "Textbook": 41, "Brush": 41,
}
glyph_rows = [row for row in fonts["rows"] if "character" in row]
assert {row["character"] for row in glyph_rows} == set(preparation["plannedGlyphs"])
assert all(row["hasGlyph"] for row in glyph_rows)
for family in ["Gothic", "Mincho", "Textbook", "Brush"]:
    family_rows = [row for row in glyph_rows if row["font"] == family]
    assert len({row["nativePaintRasterSha256"] for row in family_rows}) == 39
    words = [row for row in fonts["rows"] if row["font"] == family and "word" in row]
    assert {row["word"] for row in words} == {"冒険", "冒す"}
    assert all(row["renderedCharactersNonblank"] == len(row["word"]) for row in words)
text = fixture.read_text(encoding="utf-8")
steps = set(re.findall(r'^\s*capture\("([^"]+)"\)', text, re.M))
steps.update(re.findall(r'^\s*show\(.+, "([^"]+)"\)$', text, re.M))
steps = {step for step in steps if "$" not in step}
steps.update(f"curated-{kind}-{stage}" for kind in ["On", "Kun"] for stage in ["question", "feedback"])
steps.update(f"font-panel-{index}" for index in range(1, 4))
actual_images = {path.name for path in SOURCE.glob("*.png")}
assert {f"n1-077-{step}.png" for step in steps} == actual_images
assert len(actual_images) == 54
for path in SOURCE.glob("*.png"):
    with Image.open(path) as image:
        image.verify()
viewed = load(CONTROL / "execution-518-viewed.json")
assert set(viewed) <= actual_images and len(viewed) == len(set(viewed)) == 26
assert {f"n1-077-font-panel-{index}.png" for index in range(1, 4)} <= set(viewed)
post_stop = load(SOURCE / "post-stop-ownership.json")
assert not post_stop["ownedProcesses"]
assert "emulator-5580" not in post_stop["devices"]
assert "emulator-5556" in post_stop["devices"]
assert {row["ProcessId"] for row in post_stop["sharedEmulators"]} == {10668, 18200}
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=CONTENT, text=True).strip()
assert not DESTINATION.exists(), "Refusing to overwrite archived evidence"
DESTINATION.mkdir(parents=True)
for path in SOURCE.iterdir():
    if path.is_file():
        shutil.copy2(path, DESTINATION / path.name)
RECEIPTS.mkdir(exist_ok=True)
for name in ["execution-518.py", "run-518-native.ps1", "run-518-native-expanded.ps1", "execution-518-viewed.json", "start-518.py"]:
    shutil.copy2(CONTROL / name, RECEIPTS / name)
next_action = (
    "SAME077 two SERIAL different-family independent visual confirmations next, reusing original "
    "sessions Claude b8120704-feb3-4c48-83bd-db5328d32017 and GPT 897b738d-bc44-412f-ab06-3e680bfbf0ba "
    "where possible. Confirm actual current catalog/model identity and supported read-only tools. "
    "One reviewer process at a time, serial internal tools, no nested/parallel tasks; preserve actual "
    "process exit/full reports/events before the next. Read docs\\n1-sources\\execution-518.json and "
    "docs\\n1-reviews\\batch-077-native\\attempt-1; no native rerun absent new concern, no publication/078. "
    "Both named077native cases terminal0, zero skips; full signed46dff146 archive via production "
    "ContentSync ONCE:1089kanji5046words109N1,version2944928c13e2165a,problems0,epoch1. "
    "Full/Lite raw and curatedボウ/おか.す; actualぼう/おかす each Good/Done2correct without duplicate "
    "question/log. Complete冒/冒す, changed冒険 component paragraph and険 meaning paragraph, "
    "all3mappedpairs6directions; selection/meaning/readings/nine-stroke reference-touch/ungradedtrace/"
    "recallAgain/articles/SystemBack/offline. All39rawscopedHan across4productionfamilies in two bounded "
    "panels plus focused冒/日/目/官/冂/阜/阝/険/犯/侵 and冒険/冒す;156single/8wordrasters. "
    "Historical38 retained: metadata-only攻 makes39. Coordinator inspected26of54originalPNGs including "
    "all3fontpanels and actual冂/阝 facts; no actionable defect established in that sample, NOT "
    "independent visual acceptance. CmapabsenceNOTglyphfailure; hashesNOTreadability/fallbackface. "
    "Table labels/examples captured separately with horizontal scrolling. Reference-touchNOThuman"
    "handwriting/MLKit; model unavailable offline. Owned5580parent27684/QEMU23940 stopped; shared5556 "
    "untouched; post-stop residualclosingconnections recorded, not claimed absent. Fresh516HOST3+1 "
    "retained without redundant rerun; HOST-only2GiBinit NEVER enters native. Later currentmainnormal"
    "merge/revalidation/normalsigning/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets/"
    "ownerissue60receipt remain. No teachingchanges/unreviewedpush/signingretry/permissionworkaround/"
    "heaporguardchanges/authoragents/secondrunner. Preserve FULLlivehistory, allsource/review/process/"
    "denial/OOM/failedlookup/readdepthlimitations and reviewedbaseline虎/猿/丘/山exceptions. Published103/"
    "1228,remaining1125; necessarysupportsNOTN1vocabulary. CompatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-set outstanding. Overall project incomplete."
)
record = {
    "schemaVersion": 1, "execution": 518, "checkpoint": 518, "batch": "077",
    "status": "native-passed-awaiting-independent-visual-confirmation",
    "startingHead": "594710e8e902b9450001bb0de79e44c1384419d4",
    "reviewedTeachingSnapshot": "02877a257d6b265625e637e6a304fc8440ddd337",
    "recordedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "authorization": load(CONTROL / "progress.json")["execution518StartingState"]["authorization"],
    "originMainFreshFetch": subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=CONTENT, text=True).strip(),
    "nativeExecution": execution, "postStopOwnership": post_stop,
    "nativeAssertionsReverified": True, "nativeSkippedCases": 0, "routeEvidence": route,
    "pngCount": len(actual_images), "pngSetMatchesEveryFixtureCapture": True,
    "glyphEvidence": {
        "currentRawScopedHan": 39, "historicalDraftHan": 38,
        "inventoryReconciliation": "Reviewed metadata-only 攻 exclusion adds the39th raw Han; historical audits retained.",
        "families": 4, "individualGlyphProbes": 156, "wholeWordRasterProbes": 8, "totalRows": 164, "panels": 3,
        "coordinatorViewedAllThreeActualPanels": True,
        "observed": "No blank/replacement glyph or collapsed look-alike established in three actual panels. 冂/阝 are visible in all four families and actual article facts; 冒/日/目/官/阜/険/犯/侵 remain distinguishable. Typeface differences are not defects.",
        "limits": "Paint hasGlyph and raster hashes do not identify fallback faces or prove readability. PNG inspection is emulator-only, not phone/native-speaker approval.",
    },
    "coordinatorVisualInspection": {
        "reviewer": "Coordinator, actual model gpt-6.1-sol; NOT independent",
        "viewToolActualOriginalPngs": viewed, "viewedCount": len(viewed),
        "notViewedCount": len(actual_images) - len(viewed),
        "noActionableDefectEstablishedInViewedSample": True,
        "tableScrollQualification": "Example-column captures leave reading labels partly offscreen after horizontal scrolling. Separate label captures exist; no claim all columns are simultaneously visible.",
        "drawingQualification": "Nine touch-injected reference strokes; ungraded trace and recall Again. Handwriting model unavailable offline as displayed; no human handwriting or MLKit evidence.",
        "limits": "Bounded actual PNG sample, not all54. Independent visual review and physical-phone acceptance remain outstanding.",
    },
    "accepted516HostCasesRetainedWithoutRerun": 4, "accepted516HostSkips": 0,
    "runtimeEditsMade": False, "runtimeBytesAndRegeneratedManifestUnchanged": True,
    "reviewersLaunched": 0, "independentVisualAcceptance": False,
    "publicationAttempted": False, "runtimePublished": False,
    "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
    "publishedAdditions": 103, "remainingAdditions": 1125, "nextAction": next_action,
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
record_path = CONTENT / "docs" / "n1-sources" / "execution-518.json"
assert not record_path.exists()
record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": record["status"], "nativeCases": 2, "skips": 0, "pngs": len(actual_images),
    "coordinatorViewed": len(viewed), "archivedArtifacts": len(artifacts), "recordSha256": digest(record_path),
}))
