import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).parent
ROOT = CONTROL.parent / "learning-japanese"
LOG = CONTROL / r"logs\14b9bff6-920d-4009-95a8-ba742c6ab75a"
HEAD = "3011ad0b302bf39e64be158fadb69ee5fc075c15"
FOLDER = ROOT / r"docs\n1-reviews\batch-074-native"
RECORD = ROOT / r"docs\n1-sources\execution-493.json"
DIRECT = """curated-both-done curated-Kun-feedback curated-Kun-question
curated-On-feedback curated-On-question drawing-feedback drawing-recall-feedback
drawing-trace font-pairs kanji-01 kanji-03 kanji-09 kanji-11 kanji-20
meaning-feedback meaning-question permit-example-18 selection
免れる-02 免れる-07 免れる-09 免れる-12 免税-07 免税-kanji-backlink
免税-system-back-to-component 免税-system-back-to-kanji 免許-07
免許-component-backlink 免許-kanji-backlink 免許-system-back-from-component
免許-system-back-to-component 免許-system-back-to-kanji""".split()
NEXT = (
    "SAME074: native493 attempt3 BOTH named cases terminal0/no skips in128.836s; "
    "read docs\\n1-sources\\execution-493.json and batch-074-native\\execution-493-artifact-index.json. "
    "Complete signed4078c7d4 Git archive through production ContentSync ONCE:1086kanji5043words106N1/"
    "versionc507eceeb764bc3f/problems0/epoch1. Full+Lite rawメン/まぬか.れる/まぬが.れる "
    "source order retained; curatedメン/まぬが.れる => めん/まぬがれる, both actual offered kinds "
    "Good/Done2correct/no alternateまぬかれる key or log. Both pronunciations valid, no rarity claim. "
    "Complete免/免れる projection, reused免許N3/免税N2 component passages and許 example, all5pairs/"
    "10directions/SystemBack/offline/N1selection/meaning/eightreference-touchstrokes/ungradedtrace/"
    "recallAgain pass.172singlePaint+12wordrasters cover43actualHan including isolated儿 across4families. "
    "57originalPNGs/32unique byte streams directly coordinator-inspected;25duplicates hash-mapped, "
    "not fresh visual reads. Left/right table captures jointly expose reading labels/examples with "
    "inherited horizontal scroll hint. Newword final dictionary source-link line below notes screenshot; "
    "complete projection/selector is not every-character viewport evidence. Attempt1 both cases passed "
    "130.644s but inherited ASCII-only retrieval lost27Unicode-namedPNGs; original preserved. "
    "Attempt2 refused own shutdown TIME_WAIT/sharedADB SynSent prelaunch, no native; preserved. "
    "Attempt3 waited180s for natural release, unchanged ownership gate/ports/fixture/APKs/assertions/"
    "heaps/guards and Unicode-letter filename retrieval; all57PNGs retrieved. "
    "Owned30460/QEMU11920 exited, preexisting5556 unchanged; no listener, only sharedADB9520 reconnect/"
    "OS TIME_WAIT. NEXT original Claudeaf76d4d5-df98-409c-a302-d8d9fd63f45d THEN "
    "GPTc7f3d66f-c4ff-479b-82cb-957c2f7913ec SERIAL dependent visual confirmations on bounded "
    "PNG/route/fixture/source packets; do not claim new blind initial reviews. Original Claude initial "
    "ONE concurrent兄/元 read remains disclosed. Do not rerun passing native or491HOST3+1 absentnewconcern. "
    "Keep Unicode retrieval for future native scripts; reference injection is not human handwriting/"
    "MLKit, emulator not physicalphone, raster hashes do not identify fallback face. "
    "Then freshmain nonrewriting integration/allcombinedvalidation/normalsigning/ownerfastforward/"
    "publicSHA/greenCI/EVERYimmutablepublicZIPruntimehash/originalbudgets/ownerissue60 BEFORE delivery "
    "or075. No secondrunner/supervisor edits/signingretry/permissionworkaround/unreviewedpush. "
    "Preserve FULLlivehistory/source recipe/baselineexceptions/fullreadingorder/historicalfailures/"
    "limits. Published100/1228,remaining1128;100necessarypublishedsupports NOTN1vocabulary. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set acceptance outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    temp = path.with_suffix(path.suffix + ".493.tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    temp.replace(path)


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


if sys.argv[1] == "start":
    request = LOG / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    snapshot = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == snapshot["checkpoint"] == 492
    assert progress["batch"] == "074" and progress["status"] == "continue"
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    shutil.copyfile(CONTROL / "progress.json", LOG / "execution-493-before-progress.json")
    state = {
        "execution": 493, "batch": "074", "startingHead": HEAD,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME074 compiled full-archive native execution and coordinator visual inspection; no reviewer/publication/075/second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, entire approved issue and final492 inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed. Initial full-acquisition console print failed cp1252 after successful parse; diagnostic retained.",
        },
        "status": "native-execution-starting",
    }
    progress["execution493StartingState"] = state
    progress["stage"] = "batch-074-native-executing"
    save(LOG / "execution-493-start.json", state)
    save(CONTROL / "progress.json", progress)
    source = (ROOT / r"docs\n1-reviews\batch-073-native\execution-receipts\run-485-native.ps1").read_text(encoding="utf-8-sig")
    for old, new in {
        "073": "074", "485": "493", "execution-484.json": "execution-492.json",
        "79b3ced488f35f70a1062064a8d4e66af79fc980": HEAD,
        "586c174d-f7ef-4f03-a1d0-e2020c7b3ee6": "14b9bff6-920d-4009-95a8-ba742c6ab75a",
    }.items():
        assert old in source, old
        source = source.replace(old, new)
    target = CONTROL / "run-493-native.ps1"
    assert not target.exists()
    target.write_text(source, encoding="utf-8")
    print(json.dumps(state, ensure_ascii=False, indent=2))
elif sys.argv[1] == "repair-capture":
    receipt = load(CONTROL / "batch-074-native-attempt-1-execution.json")
    assert receipt["passed"] and receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"]
    source = (CONTROL / "run-493-native.ps1").read_text(encoding="utf-8-sig")
    assert "attempt-1" in source and "attempt=1;" in source
    assert "^n1-074-[a-zA-Z0-9-]+" in source
    source = source.replace("attempt-1", "attempt-2").replace("attempt=1;", "attempt=2;")
    source = source.replace("^n1-074-[a-zA-Z0-9-]+", r"^n1-074-[\p{L}\p{N}-]+")
    target = CONTROL / "run-493-native-attempt-2.ps1"
    assert not target.exists()
    target.write_text(source, encoding="utf-8")
    repair = {
        "execution": 493, "batch": "074", "attempt1NativeCasesPassed": 2,
        "attempt1Preserved": True,
        "defect": "Inherited ASCII-only artifact filename filter omitted Unicode-named new-word/reused-word and system-Back PNGs. Both native cases passed, but those screenshots were not retrieved before the owned disposable helper stopped.",
        "remedy": "Preserve complete original attempt; repeat identical frozen native fixture with Unicode letter/number filename retrieval. No teaching/assertion/archive/heap/guard changes.",
        "permissionDenial": False,
        "retryScriptSha256": sha(target),
    }
    save(LOG / "execution-493-capture-repair.json", repair)
    progress = load(CONTROL / "progress.json")
    progress["execution493CaptureRepair"] = repair
    save(CONTROL / "progress.json", progress)
    print(json.dumps(repair, indent=2))
elif sys.argv[1] == "prepare-after-port-release":
    receipt = load(CONTROL / "batch-074-native-attempt-2-execution.json")
    assert not receipt["nativeExecuted"]
    assert receipt["failure"] == "5580/5581 occupied; no helper launched."
    assert {c["OwningProcess"] for c in receipt["prelaunch"]["connections"]} == {0, 9520}
    source = (CONTROL / "run-493-native-attempt-2.ps1").read_text(encoding="utf-8-sig")
    source = source.replace("attempt-2", "attempt-3").replace("attempt=2;", "attempt=3;")
    target = CONTROL / "run-493-native-attempt-3.ps1"
    assert not target.exists()
    target.write_text(source, encoding="utf-8")
    print("Prepared same ownership-gated Unicode retrieval runner; no policy or port change.")
elif sys.argv[1] == "archive":
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    prep = load(ROOT / r"docs\n1-sources\batch-074-native-preparation.json")
    compiled = load(ROOT / r"docs\n1-sources\execution-492.json")
    for item in compiled["artifacts"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    for key in ("archive", "fixture"):
        assert sha(Path(prep[key])) == prep[key + "Sha256"]
    expected_cases = {
        ("io.github.stopcran.kanji.ui.N1Batch074GlyphTest",
         "exemptionLookalikesAndIsolatedRadicalAcrossFourProductionFamilies"),
        ("io.github.stopcran.kanji.ui.N1Batch074ArticleTest",
         "fullSingleImportOfflineExemptionFiveReciprocalPairsBothReadingsDrawingAndSystemBack"),
    }
    receipts = [load(CONTROL / f"batch-074-native-attempt-{i}-execution.json") for i in (1, 2, 3)]
    for i, receipt in zip((1, 3), (receipts[0], receipts[2])):
        assert receipt["passed"] and receipt["nativeExecuted"] and receipt["failure"] is None
        assert receipt["terminalSuccessCases"] == 2 and receipt["adbExitCode"] == 0
        assert {(r["class"], r["test"]) for r in receipt["terminalCases"]} == expected_cases
        assert all(r["status"] == 0 for r in receipt["terminalCases"])
        assert receipt["prelaunch"]["connections"] == []
        assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"]
        assert receipt["stopAdbExitCode"] == 0
        assert receipt["heapGrowth"] == "192m" and receipt["heapSize"] == "576m"
        for key in ("testApk", "appApk"):
            assert sha(Path(receipt[key])) == receipt[key + "Sha256"]
        original = CONTROL / rf"artifacts\batch-074-native-attempt-{i}"
        raw = (original / "instrumentation.txt").read_text(encoding="utf-8-sig")
        assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (.+)$", raw, re.M) == ["1", "0", "1", "0"]
        assert "OK (2 tests)" in raw
    assert not receipts[1]["nativeExecuted"] and not receipts[1]["passed"]
    assert receipts[1]["failure"] == "5580/5581 occupied; no helper launched."
    source = CONTROL / r"artifacts\batch-074-native-attempt-3"
    route = load(source / "n1-074-article-route.json")
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems",
                              "acceptedReadingParserEpoch", "archiveRequests")] == [1086, 5043, 106, 0, 1, 1]
    assert route["contentVersion"] == prep["contentVersion"]
    assert route["contentSnapshot"] == prep["contentSnapshot"]
    assert route["fullOnyomi"] == route["fullProjectionOnyomi"] == ["メン"]
    assert route["fullKunyomi"] == route["fullProjectionKunyomi"] == ["まぬか.れる", "まぬが.れる"]
    assert route["quizOnKeys"] == ["めん"] and route["quizKunKeys"] == ["まぬがれる"]
    assert route["liteQuizOnyomi"] == route["fullProjectionQuizOnyomi"] == ["メン"]
    assert route["liteQuizKunyomi"] == route["fullProjectionQuizKunyomi"] == ["まぬが.れる"]
    assert route["mappedReciprocalPairs"] == 5 and route["directedLinkTransitions"] == 10
    for key in ("passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "bothCuratedKindsPersistedGoodNoAlternateAndDone", "drawingTraceThenRecall",
                "drawingGradeRecordedOnNext", "offline"):
        assert route[key] is True, key
    assert route["touchInjectedReferenceStrokes"] == 8 and route["phoneEvidence"] is False
    raster = load(source / "n1-074-font-raster.json")
    assert raster["individualGlyphProbes"] == 172 and raster["wholeWordRasterProbes"] == 12
    assert len(raster["rows"]) == 184
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        rows = [r for r in raster["rows"] if r["font"] == font]
        glyphs = [r for r in rows if "character" in r]
        assert {r["character"] for r in glyphs} == set(prep["plannedGlyphs"])
        assert all(r["hasGlyph"] for r in glyphs)
        assert len({r["nativePaintRasterSha256"] for r in glyphs}) == 43
        words = [r for r in rows if "word" in r]
        assert {r["word"] for r in words} == set(prep["plannedWholeWords"])
        assert all(r["renderedCharactersNonblank"] == len(r["word"]) for r in words)
    post = load(LOG / "execution-493-postrun-final.json")
    assert post["contentHead"] == HEAD and post["contentStatus"] == post["androidStatus"] == []
    assert post["androidHead"] == prep["androidSnapshot"]
    assert post["devices"] == receipts[2]["prelaunch"]["devices"]
    assert post["emulators"] == receipts[2]["preexistingEmulators"]
    assert not any(c["State"] == 2 for c in post["connections"])
    assert all(c["OwningProcess"] in (0, 9520) for c in post["connections"])
    pngs = sorted(source.glob("*.png"))
    groups = {}
    for path in pngs:
        groups.setdefault(sha(path), []).append(path.name)
    inspected = [f"n1-074-{step}.png" for step in DIRECT]
    assert len(pngs) == 57 and len(groups) == len(inspected) == 32
    assert {sha(source / name) for name in inspected} == set(groups)
    expected_literal_steps = set(re.findall(
        r'(?:show\([^\n]+|capture\()"([^"\n]+)"\)', Path(prep["fixture"]).read_text(encoding="utf-8")
    ))
    expected_steps = {
        step.replace("${question.question.kind}", kind)
        for step in expected_literal_steps for kind in ("On", "Kun")
    }
    expected_steps.add("font-pairs")
    assert {f"n1-074-{step}.png" for step in expected_steps} == {path.name for path in pngs}
    for i in (1, 2, 3):
        destination = FOLDER / f"attempt-{i}"
        assert not destination.exists()
        shutil.copytree(CONTROL / rf"artifacts\batch-074-native-attempt-{i}", destination)
    execution_receipts = FOLDER / "execution-receipts"
    assert not execution_receipts.exists()
    execution_receipts.mkdir()
    for path in (Path(__file__), CONTROL / "run-493-native.ps1",
                 CONTROL / "run-493-native-attempt-2.ps1", CONTROL / "run-493-native-attempt-3.ps1",
                 LOG / "execution-493-capture-repair.json", LOG / "execution-493-post-stop-ownership.json",
                 LOG / "execution-493-postrun-final.json"):
        shutil.copyfile(path, execution_receipts / path.name)
    files = []
    for base in (FOLDER / "attempt-1", FOLDER / "attempt-2", FOLDER / "attempt-3", execution_receipts):
        for path in sorted(base.iterdir()):
            files.append({"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)})
    index = FOLDER / "execution-493-artifact-index.json"
    save(index, {
        "execution": 493, "batch": "074", "files": files, "acceptedAttempt": 3,
        "acceptedAttemptPngCount": 57, "directCoordinatorImageRequests": inspected,
        "pngHashGroups": [
            {"sha256": h, "names": names, "directlyInspectedRepresentative": next(n for n in names if n in inspected)}
            for h, names in sorted(groups.items())
        ],
        "originalAttempt1PngCount": 30,
        "limits": "Attempt3:32 unique-byte native PNGs directly inspected;25 exact duplicates hash-mapped, not fresh image reads. Attempt1's18 unique streams also inspected separately. Coordinator inspection, not independent review or physical phone.",
    })
    progress = load(CONTROL / "progress.json")
    save(RECORD, {
        "schemaVersion": 1, "execution": 493, "checkpoint": 493, "batch": "074",
        "status": "native-passed-awaiting-independent-visual-confirmation", "startingHead": HEAD,
        "reviewedTeachingSnapshot": compiled["reviewedTeachingSnapshot"],
        "authorization": progress["execution493StartingState"]["authorization"],
        "nativeExecution": receipts[2], "preservedAttempt1": receipts[0], "preservedAttempt2": receipts[1],
        "captureRepair": load(LOG / "execution-493-capture-repair.json"),
        "route": route, "artifactIndex": str(index.relative_to(ROOT)), "artifactIndexSha256": sha(index),
        "visualInspection": {
            "directUniqueByteImages": 32, "duplicateImagesHashMapped": 25,
            "productionFamilies": 4, "individualGlyphProbes": 172, "wholeWordRasterProbes": 12,
            "observations": "All four production rows legible;免/兄/元/先 distinguishable, isolated儿 and all43 authoredHan nonblank; whole免れる/免許/免税 legible. New免/免れる teaching and changed免許/免税 component passages plus許 common-word example inspected. Left/right reading-table captures jointly expose labels/examples, with inherited horizontal scroll hint. Newword's final dictionary source-link line below notes frame; complete projection/selector is not every-character screenshot visibility. Both actual on/kun questions, feedback,2of2Done, meaning, selection, all5pairs10directions and Back, eight-stroke reference/trace/recall inspected.",
        },
        "hostAndroid491NotRerun": True, "nativeAcceptance": True,
        "independentVisualAcceptance": False, "runtimePublished": False,
        "phoneEvidence": False, "publishedAdditions": 100, "remainingAdditions": 1128,
        "postrun": post, "nextAction": NEXT,
        "limits": "Emulator not phone; raster hashes do not identify fallback face. Reference-coordinate touch injection is not human handwriting/MLKit. Offline first-use handwriting model unavailable as disclosed by app. Not independent visual approval/current-main/CI/public ZIP/whole-set acceptance. No runtime edits, guest/app heap changes, HOST heap init or guard changes. Original Claude initial one concurrent small兄/元 read remains disclosed.",
    })
    print(f"Archived {len(files)} artifacts; accepted57PNGs/32unique directly inspected streams.")
elif sys.argv[1] == "checkpoint":
    record = load(RECORD)
    for item in load(ROOT / record["artifactIndex"])["files"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    assert not git("diff", record["reviewedTeachingSnapshot"], "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert not git("status", "--porcelain")
    commit = git("rev-parse", "HEAD")
    assert commit != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD
    progress = load(CONTROL / "progress.json")
    before = load(LOG / "execution-493-before-progress.json")
    for key, value in before.items():
        if key != "stage":
            assert progress[key] == value, key
    checkpoint = {
        "execution": 493, "checkpoint": 493, "batch": "074", "status": "continue",
        "savedCommit": commit, "signature": "G", "record": str(RECORD.relative_to(ROOT)),
        "recordSha256": sha(RECORD), "runtimePublished": False, "nativeExecuted": True,
        "nativeAcceptance": True, "independentVisualAcceptance": False, "nextAction": NEXT,
        "publishedAdditions": 100, "remainingAdditions": 1128, "allOriginalHistoricalRootKeysPreserved": True,
    }
    progress.update(checkpoint=493, status="continue", stage="batch-074-native-passed-pending-visual-confirmation",
                    nextAction=NEXT, blocker=None)
    progress["execution493StartingState"]["status"] = "signed-native-acceptance-checkpoint-complete"
    progress["execution493CoordinatorCheckpoint"] = checkpoint
    progress["batch074NativeCheckpoint"] = checkpoint
    save(CONTROL / "progress.json", progress)
    save(LOG / "execution-493-final-checkpoint.json", checkpoint)
    body = (
        f"Batch **074 (免)**: native checkpoint **493** saved locally at signed `{commit}`; **not published**. "
        "Both named API35 emulator cases returned terminal status `0`, zero skips (128.836s), importing "
        "the complete signed `4078c7d4` archive through production ContentSync **once**: "
        "1,086 kanji / 5,043 words / 106 N1, version `c507eceeb764bc3f`, zero problems, parser epoch1.\n\n"
        "Full/Lite preserve raw `メン / まぬか.れる / まぬが.れる` in source order; curation offers "
        "`めん / まぬがれる`, both actual kinds persisted Good, 2/2 correct, no excluded-alternate key/log. "
        "Both pronunciations remain valid. New免/免れる, reused免許/免税 component passages and許 example, "
        "five reciprocal pairs/ten directions, system Back, offline routes, N1 selection/meaning, eight "
        "reference-touch strokes, ungraded trace and recall Again passed. All43 authoredHan including "
        "isolated儿 were probed across four production families, plus twelve whole-word rasters. "
        "Coordinator inspected32 unique PNG byte streams from57 captures;25 duplicates hash-mapped, "
        "not fresh reads. Horizontal tables retain the scroll hint; the newword's last source-link line "
        "is below its notes capture. This is not physical-phone, fallback-face or human-handwriting/MLKit evidence.\n\n"
        "Original attempt1 passed both cases (130.644s), but an inherited ASCII-only retrieval filter "
        "omitted27 Unicode-named PNGs. Original evidence retained; Unicode filename retrieval corrected. "
        "Attempt2 safely refused prelaunch while own shutdown TIME_WAIT/sharedADB reconnect remained; "
        "no native run. After180s natural release, attempt3 passed with identical frozen APKs/archive/"
        "assertions and all57 PNGs retrieved. No port, ownership-gate, guest/app heap, HOST-init or guard "
        "changes. Owned parent30460/QEMU11920 exited; existing emulator5556 unchanged. "
        "Evidence: `docs/n1-sources/execution-493.json` and "
        "`docs/n1-reviews/batch-074-native/execution-493-artifact-index.json`.\n\n"
        "**Next:** original Claude then GPT serial dependent visual confirmations, then current-main "
        "integration/validation, signing/publication/CI/immutable-ZIP gates. Original Claude's single "
        "concurrent small read remains disclosed. No batch075 started. **Published remains100/1,228; "
        "1,128 remain**, with100 necessary published supports (not N1 vocabulary). Compatible Android "
        "`f9b59a2+` required; physical-phone/general-release/whole-set acceptance outstanding."
    )
    (LOG / "issue-493-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))
else:
    raise SystemExit("Unsupported stage")
