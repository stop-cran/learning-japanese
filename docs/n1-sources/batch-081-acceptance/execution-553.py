"""Bounded batch 081 combined-tree acceptance and publication."""
import copy
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "ecff7653-5e6e-4424-8cb2-a4825995bdb4"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-081-acceptance"
BASE = "a7b119ed36adf7a3a92bba03700bc1c51f812bef"
START = "a7e2eb07025fe0ee74195be468b844588a12ea73"
TEACHING = "b7bf953d137251f179a57128bb84bd70a37737c8"
VERSION = "f1dd5d8b9d2ff535"
sys.path.insert(0, str(R / "tools"))
from audit_n1_batch import audit, base_file
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256
from check_content_budget import archive_names, check
from extract_n1_jmdict import extract
from fontTools.ttLib import TTFont
from generate_strokes import convert


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".execution553.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now().astimezone().isoformat()


def git(*args, tree=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", *args],
        cwd=tree, text=True, encoding="utf-8").strip()


def unchanged():
    assert git("branch", "--show-current") == "content/n1-kanji"
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", tree=A) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", tree=A)
    subprocess.run(["git", "merge-base", "--is-ancestor", git("rev-parse", "origin/main"), "HEAD"],
                   cwd=R, check=True)


def start():
    unchanged()
    assert git("rev-parse", "HEAD") == START and git("rev-parse", "origin/main") == BASE
    assert not git("status", "--porcelain")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 552 and p["batch"] == "081" and p["status"] == "continue"
    assert "execution553StartingState" not in p
    assert not (L / "progress-before-execution-553.json").exists()
    save(L / "progress-before-execution-553.json", p)
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p["execution553StartingState"] = {
        "execution": 553, "batch": "081", "startingHead": START, "freshOriginMain": BASE,
        "startedAt": now(), "status": "combined-tree-acceptance-in-progress",
        "scope": "SAME081 combined-current-main acceptance and authorized owner-testing publication only; no082 or second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, complete issue and final552 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated worktrees clean, normally signed; freshly fetched main already ancestral. No canonical repositories accessed.",
        "artifactPathPreflight": str(C / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "diagnostics": ["Initial console output hit cp1252 only after complete request load/checkpoint parse; final checkpoint subsequently read directly. No permission denial."],
    }
    p["stage"] = "batch-081-combined-tree-acceptance-in-progress"
    save(C / "progress.json", p)
    print("Starting scope persisted; complete live history preserved.")


def normalized(element):
    element = copy.deepcopy(element)
    for node in element.iter():
        if node.text is not None and not node.text.strip():
            node.text = None
        node.tail = None
    return ET.tostring(element)


def source_audit():
    unchanged()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == row["sha256"], name
    for name, section in (("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                          ("n1-implementation-JMdict_e.gz", "jmdict")):
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    ledger = load(S / "batch-081-progress.json")
    result = audit(R, "081")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison"):
        selection = load(S / f"batch-081-{kind}-selection.json")
        selected = set(selection["entryIds"])
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("冶" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else e.findtext("ent_seq") in selected)]
        name = "batch-081-jmdict.xml" if kind == "lexical" else "batch-081-comparison-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [15, 10] and len(distinct) == 24
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-081-kanjidic2.xml").getroot()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 5
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-080-acceptance-source-audit.json")["explicitInheritedMetadataExceptions"]
    baseline = load(S / "baseline-inventory.json")["files"]
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, row in baseline.items():
        kind = name.split("/")[0]
        if kind in ("kanji", "words"):
            assert metadata(R, name) == {**row["metadata"], **exceptions.get(name, {})}, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == row["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    old_chars = {Path(p).stem for p in baseline if p.startswith("kanji/")}
    expected = set(load(C / "progress.json")["publicationCheckpoint"]["pilotMembership"])
    for path in sorted(S.glob("batch-*-progress.json")):
        row = load(path)
        assert int(row["batch"]) <= 81 and not expected & set(row["membership"])
        if int(row["batch"]) < 81:
            assert row["reviewClosed"] == row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 108 and old_chars <= current
    index = {row["kanji"]: row for row in load(S / "source-index.json")}
    for char in expected:
        meta = metadata(R, f"kanji/{char}.md")
        for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
            assert meta[field] == index[char]["metadata"][field], (char, field)
        stroke = load(R / "strokes" / f"{char}.json")
        assert meta["jlpt"] == 1 and stroke["kanji"] == char
        assert stroke["strokeCount"] == len(stroke["strokes"]) == meta["strokes"]
        assert stroke["sourceRevision"] == snapshot["kanjivg"]["revision"]
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232
    assert expected <= set(named) and metadata(R, "kanji/妖.md")["jlpt"] == 1
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R) and manifest["contentVersion"] == VERSION
    maps = {}
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == digest, name
            maps[section] = len(entries)
    assert sum(maps.values()) == 8369
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 2
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-081-stroke-evidence.json")
    svg_path = Path(geometry["input"])
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "冶.json") == convert("冶", svg.decode("utf-8"))
    font_audit = load(S / "batch-081-draft-font-audit.json")
    scope_text = "".join((R / name).read_text(encoding="utf-8") for name in font_audit["completeNewArticleScope"])
    scope_text += "".join(font_audit["changedReusedScope"].values())
    han = sorted(set(c for c in scope_text if 0x2E80 <= ord(c) <= 0x2FDF
                     or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                     or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == sorted(font_audit["actualHan"]) and len(han) == 29
    fonts = []
    for row in font_audit["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["allActualMissing"] == ["冫", "氵"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1093, "words": 5049, "n1Labelled": 113, "namedSourceMembersPresent": 112}
    result.update(
        execution=553, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        exactFrozenDistinctDictionaryFamilies=len(distinct), dictionaryFamilyOccurrences=25,
        dictionaryPackets=packets, completeRawCharacterRecordsVerified=5,
        runtimePayloadHashesVerified=8369, manifestMaps=maps, allMappedReciprocalPairs=2,
        mappedDirectedLinks=4, actualCounts=actual_counts,
        actualHanFontCmaps={"characters": han, "fonts": fonts, "scope": font_audit["completeNewArticleScope"],
                           "changedReusedScope": font_audit["changedReusedScope"]},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Mechanical source/family/baseline/membership/readings/quiz/link/geometry/cmap/manifest/budget audit, not fresh linguistic/native review. Original source-only and lookup limitations retained; cmap absence is not a glyph failure.",
    )
    save(S / "batch-081-acceptance-source-audit.json", result)
    print("Source/families/baseline/108 additions/8369 hashes/two pairs/geometry/cmaps/budgets passed.")


def validate():
    unchanged()
    receipts = []
    target = L / "execution-553-validation-receipts.json"
    assert not target.exists()
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-553-{name}.txt"
        assert not path.exists()
        started = now()
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args],
                                    cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({"check": name, "command": ["python", "-X", "utf8", "-B", *args],
                         "startedAt": started, "completedAt": now(), "exitCode": result.returncode,
                         "log": str(path), "sha256": sha(path)})
        save(target, receipts)
        print(f"{name}: exit {result.returncode}", flush=True)
        if result.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(result.returncode)


def evidence():
    unchanged()
    textual = load(V / "batch-081-reconciliation.json")
    assert sha(V / "batch-081-reconciliation.json") == load(S / "execution-548.json")["reconciliationSha256"]
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["actionableRemainingFindings"] == textual["consequentialUnresolvedTeachingFindings"] == 0
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["allInitialInternalToolsSerial"]
    processes = list(textual["processes"].values())
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]] and row["snapshot"] == TEACHING
        execution = load(V / row["execution"])
        assert sha(V / row["report"]) == row["reportSha256"] == execution["reportSha256"]
        assert sha(V / Path(row["report"]).with_suffix(".jsonl")) == row["rawExecutionSha256"]
        assert execution["observedToolOverlaps"] == execution["unfinishedTools"] == []
        assert execution["multiToolResponseCount"] == 0 and execution["exitCode"] == 0
        assert execution["actualModels"] == [row["requestedModel"]]
        assert load(V / row["coverage"])["allAssignedRangesReturned"]
    assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
    visual = load(V / "batch-081-visual-reconciliation.json")
    record552 = load(S / "execution-552.json")
    assert sha(V / "batch-081-visual-reconciliation.json") == record552["reconciliationSha256"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedScopedTeachingFindings"] == 0
    assert visual["process"]["oneReviewerFamilyActiveAtATime"] and visual["process"]["allChildrenExitedBeforeNext"]
    assert visual["process"]["observedToolOverlaps"] == visual["process"]["unfinishedTools"] == 0
    visual_processes = list(record552["processes"].values())
    assert [r["actualModels"] for r in visual_processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    for row in visual_processes:
        execution = load(V / row["execution"])
        assert execution["exitCode"] == 0 and len(execution["turns"]) == 27
        assert execution["completePacketReturned"] and execution["distinctImagePayloadsVerified"] == 25
        assert execution["observedToolOverlaps"] == execution["unfinishedTools"] == []
        assert sha(V / row["report"]) == row["reportSha256"] == execution["reportSha256"]
        assert sha(Path(execution["rawExecutionLocation"])) == row["rawExecutionSha256"]
        turns = execution["turns"]
        for turn in turns:
            assert turn["exitCode"] == 0 and turn["singleResourceAccepted"]
            assert turn["actualModels"] == [row["requestedModel"]]
            if "imagePayload" in turn:
                image = turn["imagePayload"]
                assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                assert sha(Path(turn["resource"])) == image["sourceSha256"]
                assert image["sourceDimensions"] == [1080, 2400] and image["returnedDimensions"] == [900, 2000]
        for first, second in zip(turns, turns[1:]):
            assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    android = load(S / "execution-549.json")
    assert android["exitCode"] == 0
    for row in android["tests"]:
        path = R / row["archivedPath"]
        assert sha(path) == row["sha256"]
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == int(row["tests"])
        assert all(int(xml.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
        assert xml.attrib["timestamp"] == row["timestamp"]
    assert [int(row["tests"]) for row in android["tests"]] == [3, 1]
    for row in android["fixtureResolution"]:
        assert Path(row["resolvedRoot"]).resolve() == R.resolve()
    for row in android["rawAndArchivedProvenance"]:
        assert sha(R / row["archivedPath"]) == row["sha256"]
    for row in android["testImplementationsAndHostInit"]:
        assert sha(Path(row["path"])) == row["sha256"]
    native = load(S / "execution-551.json")
    for row in native["archivedReceipts"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "compressedRaw" in row:
            assert sha(R / row["compressedRaw"]) == row["compressedRawSha256"]
            original = gzip.decompress((R / row["compressedRaw"]).read_bytes())
            assert hashlib.sha256(original).hexdigest() == row["originalSha256"]
    raw = V / "batch-081-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(raw.parent / "n1-081-article-route.json")
    assert route == native["articleRoute"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1093, 5049, 113, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    for suffix, full, selected in (("Onyomi", ["ヤ"], ["ヤ"]), ("Kunyomi", ["い.る"], [])):
        assert route["full" + suffix] == route["fullProjection" + suffix] == full
        assert route["fullProjectionQuiz" + suffix] == route["liteQuiz" + suffix] == selected
    assert route["quizOnKeys"] == ["や"] and route["quizKunKeys"] == []
    assert route["soleCuratedOnPersistedGoodAndDone"] and route["meaningQuestionAndFeedback"]
    assert route["mappedReciprocalPairs"] == 2 and route["directedLinkTransitions"] == 4
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert route["touchInjectedReferenceStrokes"] == 7 and route["drawingGradeRecordedOnNext"]
    execution = native["nativeExecution"]
    assert execution["terminalSuccessCases"] == 2
    assert len(execution["terminalCases"]) == 2 and all(r["status"] == 0 for r in execution["terminalCases"])
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    index = native["imageIndex"]
    assert index["originalPngCount"] == 45 and index["distinctByteGroups"] == 25
    images = []
    for group in index["groups"]:
        for name in group["originals"]:
            assert sha(raw.parent / name) == group["sha256"]
            images.append(name)
    assert len(images) == len(set(images)) == 45
    receipts = load(L / "execution-553-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-553-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    limits = [
        "Two blind textual families on unchanged b7bf953d, same complete packet:24 distinct families/25 occurrences,five raw records,nine comparison bodies. Supplied coordinator upstream observations, not reviewer independent retrieval; encyclopedia/Nipponica truncation and image-dependent etymology limits retained.",
        "No consequential unresolved scoped teaching defect. Conditional溶 fallback concern and five wording/comparison/citation suggestions optional. Three curated wrong choices治/台/始 textually reviewed, NOT the captured random meaning alternatives; no every-pool certification.",
        "Original ClaudeOpus5.5/GPT6.1Sol visual confirmations each27 serial children/one packet/25 distinct PNG groups covering45 originals/20 aliases; all exits before next. Original1080x2400 versus returned900x2000 preserved, not source-byte equality. Claude compressed-history resource26 disclosure and all original reports/observations unchanged.",
        "All29Han/fourproductionfamilies/readable冫/氵; faint prose冫 optional. Fallback face unknown; complementary horizontal table states are not all columns in one frame. 116individual+4wholewordPaint assertions are not120PNGreads.",
        "Accepted HOST549RealContentTest3+RareHanTest1/no skips,550compile and551both named native terminal0 reverified without rerun because exact runtime/tools/Android unchanged. Full signed95a87783archive through productionContentSyncONCE1093kanji5049words113N1/zeroProblems/epoch1.",
        "Full/Lite fullヤ/い.る preserved; selectedonヤ/kun[],soleやgoodlog/Done1of1. Two pairs/four directions/SystemBack/offline/N1selection/actualmeaningfeedback. Seven injectedreferencepaths/ungradedtrace/shape-only/giveuprecallgrade1 NOT humanhandwriting/successfulrecall/MLKitrecognition/modeldownload; offline model unavailable. Finalsemanticstree transientloading NOT settledroute/persistenceproof. Disposable synthetic source/seeds NOTownerprogress.",
        "Owned551emulator5580parent18020/qemu28948 stopped; owner5556 untouched. HOST-only2GiBinit NEVERnative; no app/guestheap/archiveguard changes. Original source/lookup/citation/readdepth/review/process/denial/OOM/viewport/phone/baseline limitations retained.",
        "Fresh vocabulary2122/2431 reviewed pilot prompts NOTfullcoverage. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Bounded owner testing only.",
    ]
    result = load(S / "batch-081-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh main already ancestral; no teaching/tool integration changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(native["archivedReceipts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        textualReconciliationSha256=sha(V / "batch-081-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-081-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-549.json"), nativeEvidenceSha256=sha(S / "execution-551.json"),
        limits=limits,
    )
    save(S / "batch-081-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1",
                 C / "verify-execution-553.ps1", C / "post-execution-553.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-553.json", {
        "schemaVersion": 1, **p["execution553StartingState"], "recordedAt": now(),
        "status": result["status"], "acceptanceRecord": "batch-081-acceptance-audit.json",
        "publishedAdditions": 107, "remainingAdditions": 1121, "localReviewClosedAdditions": 108,
        "limits": limits, "nextAction": "Normal signed acceptance,ownerfastforward,exactgreenCI/publicZIP,terminal evidence/ownerissue60;yield before082.",
    })
    ledger = load(S / "batch-081-progress.json")
    ledger["preAcceptanceCheckpoint"] = {
        k: copy.deepcopy(ledger[k]) for k in ("status", "reviewClosed", "nextAction", "limits")}
    ledger.update(status="review-closed-combined-tree-accepted-pending-publication",
                  reviewClosed=ledger["membership"], runtimeAccepted=True,
                  acceptanceRecord="batch-081-acceptance-audit.json")
    for row in ledger["supportMappings"]:
        row["status"] = ledger["status"]
    save(S / "batch-081-progress.json", ledger)
    p["stage"] = "batch-081-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined-tree and inherited reviewer/HOST/native evidence accepted.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-081-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8369
    assert all(archive[k] for k in ("manifestEqual", "allPublishingBudgetsPassed",
                                  "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-081-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 553, "batch": "081", "membership": ["冶"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "cbf4db9a98cfb47c780f9d7f1d43349c62dc189e",
        "freshAndroidSnapshot": "95a87783e4be501c4b2b788d6906f6cc76b3c751",
        "nativeEnvelopeSnapshot": "95a87783e4be501c4b2b788d6906f6cc76b3c751",
        "nativeEvidenceSnapshot": "824045ee9eefca3c7ee883a7b7687d72a52d4f96",
        "visualClosureSnapshot": START, "latestMainIntegrated": BASE,
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-081-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-081-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 108, "remainingAdditions": 1120,
            "currentKanji": 1093, "currentWords": 5049, "n1Labelled": 113, "namedSourceMembersPresent": 112,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 107, "batchChangedReusedArticles": 1,
            "allMappedReciprocalPairs": 2, "activatedBaselinePairs": 0,
        },
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/publicZIP/ownerissue60;checkpoint and yield before082.",
    }
    assert not (S / "batch-081-publication.json").exists()
    save(S / "batch-081-publication.json", publication)
    ledger = load(S / "batch-081-progress.json")
    ledger["prePublicationCheckpoint"] = {
        k: copy.deepcopy(ledger[k]) for k in ("status", "nextAction", "nextGate", "limits") if k in ledger}
    ledger.update(status=publication["status"], published=ledger["membership"],
                  publishedAdditions=108, remainingAdditions=1120, publishedCommit=head,
                  publicationRecord="batch-081-publication.json", acceptanceRecord="batch-081-acceptance-audit.json",
                  nextAction=publication["nextAction"], nextGate="Terminal receipts/ownerissue,then yield before082.",
                  limits=publication["limits"], runtimePublished=True, runtimeAccepted=True)
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-081-progress.json", ledger)
    execution = load(S / "execution-553.json")
    execution.update(status=publication["status"], publishedAdditions=108, remainingAdditions=1120,
                     publicationRecord="batch-081-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-553.json", execution)
    for path in (C / "artifacts" / "batch-081-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-553-accepted-push.txt"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-081-accepted-publication-verified-pending-terminal-evidence"
    p["execution553AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted publication verified; terminal durable records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-081-publication.json")
    body = f"""**Batch 081 (冶) is published and verified for bounded owner testing**, with necessary **冶金 (やきん, metallurgy)** and only one reciprocal bullet added to existing 金. Full metadata **ヤ /い.る** stays in source order; selected on **ヤ**, explicit kun **[]**, sole offered key **や**. Qualified source-only い.る does not invent an ordinary 冶る or extract ジ from whole-word 鍛冶かじ. No inferred word JLPT level.

Authored/reviewed `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`; HOST/native full-envelope `{publication['nativeEnvelopeSnapshot']}`; native evidence `{publication['nativeEvidenceSnapshot']}`; visual closure `{START}`. Fresh main `{BASE}` already ancestral: no teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined checks: **372 Python tests/no skips**, validator, vocabulary (**2,122/2,431 reviewed pilot prompts**, not full coverage), fresh manifest `{VERSION}`, five frozen inputs/two decompressed dictionaries, **24 distinct complete JMdict families/25 occurrences**, five complete raw character records, baseline **985kanji/4,942words/985strokes** with documented exceptions, exact **108 additions**, readings/quiz safeguards/**two reciprocal pairs/four directions**, pinned seven-stroke geometry, all29 scoped Han cmaps, **8,369 runtime hashes** and original budgets.

Original blind textual reviews **claude-opus-5.5 /gpt-6.1-sol** and dependent original-session visual confirmations preserved; no actionable/consequential unresolved scoped teaching defect. Conditional溶 fallback concern and five wording/comparison/citation suggestions optional; no teaching edit. Visual reviewers serial: **27 host-dispatched children each**, one common complete packet plus **25 distinct PNG groups covering45 originals/20 aliases**, then zero-tool final report; all children exit before next family. Original1080x2400 and returned900x2000 payloads separately retained. Claude resource26 compressed-history disclosure and original reports/observations preserved; no fresh-source/equal-comprehension or original-resolution-byte claim.

Accepted HOST549 **RealContentTest3+RareHanTest1/no skips**,550compile and native551 **two named terminal-status-0 cases** reverified, not rerun. Full signed95a87783archive through production **ContentSync ONCE**: **1,093kanji/5,049words/113N1/zeroProblems/epoch1**. Full/Lite full and curated readings agree; sole new on good log/**Done1of1**, N1selection/actualmeaningfeedback/twopairs/fourdirections/SystemBack/offline pass. Captured wrong meaning labels were two(formal numeral),chrysanthemum,moreover/also—not curated治/台/始; curated trio retains textual review, not captured-use or every-pool certification.

All29Han/fourproductionfamilies/exact冫/氵 readable in bounded captures; faint prose冫 optional, fallbackface unknown. Complementary horizontal table states, not allcolumns oneframe. Finalsemanticstree loading, not settledroute/persistenceproof. Seven injectedreferencepaths/ungradedtrace/shape-only/giveuprecallgrade1 NOT humanhandwriting/successfulrecall/MLKitrecognition/modeldownload; offline model unavailable. 116individual+4wholewordPaint assertions NOT120PNGreads; seeded synthetic source/schedule not ownerprogress. Owned5580parent18020/qemu28948 stopped; owner5556 untouched. HOST-only2GiBinit NEVERnative; no app/guestheap/guard changes.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs preserve every8,369runtime hash**, exactmanifest/safepaths/per-filelimits/contributor-evidence exclusion. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']}entries/{archive['compressedBytes']}compressed/{archive['inflatedBytes']}inflated/{archive['retainedBytes']}retained bytes**, unchanged **18,000entries/42compressed/80inflated/56retained MiB** guards.

Published **108/1,228 additions;1,120 remain**. Current **1,093kanji/5,049words/113N1labels/112named-source members plus separate妖**; **107 necessary support additions, not an N1 vocabulary deck**. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required. **Physical-phone/general-release/whole-set acceptance outstanding.**

Durable `docs/n1-sources/batch-081-publication.json`, `batch-081-acceptance-audit.json`, `execution-553.json` and authoring notes preserve exact review/source/native/process/denial/OOM/viewport/phone limitations. Checkpoint553 continue; yield before one bounded082 source-preparation checkpoint. Durablecontrol/committedpackets/approvedinputs only; optional historical session recipes skipped, no new denial, no082 or secondrunner. Full live history preserved; overall project incomplete.
"""
    path = L / "issue-553-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact owner issue publication body prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "progress-before-execution-553.json")
    receipt = load(L / "issue-553-verified.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (L / "issue-553-body.txt").read_bytes().decode("utf-8")
    assert not (S / "batch-082-progress.json").exists()
    publication = load(S / "batch-081-publication.json")
    next_action = (
        f"Batch081 published/terminalgreenCI/everypublicZIPhash/ownerissue verified at {head}; yield before082. "
        "NEXT freshcoordinator read entire request/finalcheckpoint/scopedlivekeys and preserve FULLhistory. "
        "Verify dedicatedclean signedheads/freshmain,then ONE evidence-bounded082 SOURCE-PREPARATION checkpoint "
        "below15 from exactremaining frozenrows ONLY,no runtime draft/latergates in sourcecheckpoint. "
        "Use committedsourcepackets/approvedworkspaceinputs/durablecontrolhelpers,NOT optional historicalsessionrecipes. "
        "Preserve source/baseline identities/levels/readings/order/exclusions and documented虎/猿/丘/山/冗談 exceptions; "
        "inspect complete applicablefamilies/actualnecessarysupport/everyreadingdisposition/curatedrow/"
        "allactivated+reciprocalpairs/pinnedstrokes/allnewHanfonts. Later twoSERIALblinddifferentfamilyreviews/"
        "serialinternaltools/boundedoriginalconfirmations/nonskippedAndroid/native/currentmain/normalsigning/"
        "ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets mandatory. No unreviewedpush/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield actualnewdenials. "
        "Published108/1228,remaining1120;1093kanji5049words113N1labels112namedmembers plus separate妖;107necessarysupports "
        "NOT N1vocabulary. Inherit548textualclosure/b7bf953d/noedit/24distinctfamilies25occurrences/5rawrecords/9comparisonbodies,"
        "549HOST3+1noskips,550compile,551native2terminal0,552dependentvisualclosure each27serialchildren/"
        "onepacket25distinctPNGgroups45originals20aliases900x2000returned1080x2400source;Claude resource26summary explicit. "
        "All29Han/fourfamilies/readable冫/氵/fallbackface unknown;faintprose冫optional;complementaryhorizontaltable "
        "notallcolumnsoneframe. Fullsigned95a87783 productionContentSyncONCE1093kanji5049words113N1/problems0/epoch1. "
        "Full+Lite fullヤ/い.る unchanged;selectedonヤ/kun[],offeredや/goodlog/Done1of1. "
        "Actualmeaningfeedback/2pairs4directions/SystemBack/offline/N1selection. Curated治/台/始 textualreview "
        "NOT capturedrandommeaningtrio(twoformal/chrysanthemum/moreover);noeverypoolclaim. "
        "Seveninjectedreferencepaths/ungradedtrace/shapeonly/giveuprecallgrade1 NOT humanhandwriting/successfulrecall/"
        "MLKit/download;116+4Paintrecords NOT120PNGreads. Finaltree transientloading NOT loadedpersistenceproof;"
        "seededdisposablesource/schedule NOTownerprogress. Owned5515580parent18020qemu28948 stopped,owner5556 untouched. "
        "Preserve all originalsource/review/process/denial/OOM/lookup/citation/readdepth/viewport/phone limits and FULLlivehistory. "
        "HOST-only2GiBinit NEVERnative;noapp/guestheap/guardchanges. CompatibleAndroidf9b59a2+ required;"
        "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=553, status="continue", stage="batch-081-published-verified-before-082",
             lastPublishedCommit=head, remainingAdditions=1120, blocker=None, nextAction=next_action)
    assert "batch081PublicationCheckpoint" not in p
    p["batch081PublicationCheckpoint"] = publication
    p["execution553StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1120 source-bounded additions not authored/review-closed/published;later batches retain all original source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 553, "checkpoint": 553, "batch": "081",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8369,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "originalRootKeyCountCompared": len(original),
        "changedRootFields": sorted(k for k in original if p[k] != original[k]),
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 108, "remainingAdditions": 1120, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "verifiedAt": now(), "nextAction": next_action, "status": "continue",
    }
    save(L / "execution-553-final-verification.json", result)
    save(L / "batch-081-publication-checkpoint.json", publication)
    p["execution553CoordinatorCheckpoint"] = result
    p["batch081PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({k: result[k] for k in ("checkpoint", "savedCommit", "issueUpdate",
          "publishedAdditions", "remainingAdditions", "allOriginalHistoricalRootKeysPreservedExactly",
          "wholeProjectComplete")}, indent=2))


if __name__ == "__main__":
    {"start": start, "source-audit": source_audit, "validate": validate, "evidence": evidence,
     "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
