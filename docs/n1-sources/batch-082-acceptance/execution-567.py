"""Batch 082 combined-tree publication and durable checkpoint operations."""
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
L = C / "logs" / "9268395b-a2ea-4c82-9bc8-b75caf647988"
S = R / "docs" / "n1-sources"
D = S / "batch-082-acceptance"
START = "394a3eb441b56684e212b6758d9e82855d69db36"
BASE = "1f317f0762513720709ab0ca215f19ff021ca596"
TEACHING = "9ce870d190d5c519d65ed20b118de64371350c0c"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "d82e7fefe3898a70"
sys.path.insert(0, str(R / "tools"))
from build_manifest import build_manifest
from audit_n1_batch import audit
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract
from generate_strokes import convert
from fontTools.ttLib import TTFont


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_suffix(p.suffix + ".567.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(p)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, tree=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree,
                                   text=True, encoding="utf-8").strip()


def now():
    return datetime.now().astimezone().isoformat()


def unchanged():
    assert git("branch", "--show-current") == "content/n1-kanji"
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", tree=A) == ANDROID
    assert not git("status", "--porcelain", tree=A)
    assert load(R / "manifest.json") == build_manifest(R)
    assert load(R / "manifest.json")["contentVersion"] == VERSION


def start():
    unchanged()
    assert git("rev-parse", "HEAD") == START
    assert git("rev-parse", "origin/main") == BASE
    assert not git("status", "--porcelain")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 566 and p["batch"] == "082"
    assert "execution567StartingState" not in p
    save(L / "progress-before-execution-567.json", p)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution566CoordinatorCheckpoint"]["savedCommit"] == START
    state = {
        "execution": 567, "batch": "082", "startingHead": START, "freshOriginMain": BASE,
        "androidHead": ANDROID, "startedAt": now(),
        "scope": "SAME082 combined-current-main acceptance and authorized owner-testing publication; yield before083. No new reviewer/native run absent substantive change.",
        "authorization": {
            "requestSha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed; operative contract, complete issue and final566 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": str(C / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "dedicatedWorktreesInitiallyClean": True,
        "status": "combined-tree-acceptance-in-progress",
    }
    p["execution567StartingState"] = state
    p.update(stage="batch-082-combined-tree-acceptance-in-progress", blocker=None,
             nextAction="SAME082 validate combined current main, normally sign/publish accepted content, verify remote/CI/every immutable ZIP hash; persist/yield before083.")
    save(C / "progress.json", p)
    save(L / "starting-state-567.json", state)
    print("Starting scope persisted with complete live history.")


def checks():
    unchanged()
    D.mkdir(parents=True, exist_ok=True)
    commands = [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
        ("batch-audit", ["tools\\audit_n1_batch.py", "--batch", "082"]),
    ]
    receipts = []
    for name, args in commands:
        target = D / f"execution-567-{name}.txt"
        assert not target.exists(), target
        with target.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args], cwd=R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({"command": ["python", "-X", "utf8", "-B", *args],
                         "exitCode": result.returncode, "log": target.relative_to(R).as_posix(),
                         "sha256": sha(target)})
        save(L / "checks-567.json", receipts)
        print(name, result.returncode, flush=True)
        assert result.returncode == 0, target
    checks_done()


def checks_done():
    receipts = load(L / "checks-567.json")
    assert len(receipts) == 6 and all(r["exitCode"] == 0 for r in receipts)
    assert all(sha(R / r["log"]) == r["sha256"] for r in receipts)
    assert "Ran 372 tests" in (D / "execution-567-python-tests.txt").read_text(encoding="utf-8")
    assert "OK" in (D / "execution-567-python-tests.txt").read_text(encoding="utf-8")
    assert (D / "execution-567-vocabulary.txt").read_text(encoding="utf-8").strip() == (
        "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot")
    unchanged()
    save(S / "batch-082-terminal-validation.json", receipts)


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
    ledger = load(S / "batch-082-progress.json")
    result = audit(R, "082")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for packet in ledger["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        if "lexical" in packet["selection"]:
            assert ids == [e.findtext("ent_seq") for e in full.findall("entry")
                           if any("准" in k.text for k in e.findall("k_ele/keb"))]
        assert (S / packet["xml"]).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        distinct.update(ids)
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(S / packet["xml"])})
    assert [r["families"] for r in packets] == [22, 11, 4] and len(distinct) == 36
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-082-kanjidic2.xml").getroot()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 7
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == git("show", f"{BASE}:{name}") + "\n"
    exceptions = load(S / "batch-081-acceptance-source-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 82 and not expected & set(row["membership"])
        if int(row["batch"]) < 82:
            assert row["reviewClosed"] == row["published"] == row["membership"]
        else:
            assert row["reviewClosed"] == row["membership"] == ["准"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 109 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and expected <= set(named)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    manifest = load(R / "manifest.json")
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8372
    pairs = {(c, r["article"]) for r in ledger["supportMappings"]
             for c in metadata(R, r["article"])["kanji"] if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 2
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and metadata(R, name)["reading"] in body
    for name, target in [("words/准教授.md", "助教授"), ("words/助教授.md", "准教授")]:
        assert f"({target}.md)" in (R / name).read_text(encoding="utf-8")
    assert metadata(R, "words/准教授.md")["quiz_exclusions"] == ["助教授"]
    geometry = load(S / "batch-082-stroke-evidence.json")
    svg_path = Path(geometry["input"])
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "准.json") == convert("准", svg.decode("utf-8"))
    font_audit = load(S / "batch-082-choice-correction-audit.json")
    font = load(S / "batch-082-draft-font-audit.json")
    han = font_audit["fontScope"]["actualHan"]
    assert len(han) == 34 and set(han) == set(font["actualHan"]) | set("冴冶隼")
    fonts = []
    for row in font["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as face:
            cmap = face.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "missing": [c for c in han if ord(c) not in cmap]})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, f"kanji/{p.name}")["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1094, "words": 5050, "n1Labelled": 114, "namedSourceMembersPresent": 113}
    result.update(
        execution=567, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        exactFrozenDistinctDictionaryFamilies=len(distinct), dictionaryFamilyOccurrences=37,
        dictionaryPackets=packets, completeRawCharacterRecordsVerified=7, runtimePayloadHashesVerified=8372,
        allMappedReciprocalPairs=2, mappedDirectedLinks=4, comparisonDirectedLinks=2,
        actualCounts=actual_counts, generatedGeometryReproducedExactly=True, fontCmaps=fonts,
        currentChoiceCorrectionAuditSha256=sha(S / "batch-082-choice-correction-audit.json"),
        freshLinguisticReviewClaimed=False,
        limits="Mechanical source/family/baseline/membership/readings/quiz/link/geometry/cmap/manifest audit, not fresh linguistic/native review. Original source-only and lookup limitations retained; cmap absence is not a glyph failure.",
    )
    save(S / "batch-082-acceptance-source-audit.json", result)
    print("Source/families/baseline/109 additions/8372 hashes/two pairs/six directions/geometry/cmaps passed.")


def evidence():
    unchanged()
    checks_done()
    v = R / "docs" / "n1-reviews"
    textual = load(v / "batch-082-reconciliation.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["actionableRemainingFindings"] == textual["consequentialUnresolvedTeachingFindings"] == 0
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["allInitialInternalToolsSerial"]
    for row in textual["processes"].values():
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]]
        assert sha(v / row["report"]) == row["reportSha256"]
        assert sha((v / row["report"]).with_suffix(".jsonl")) == row["rawExecutionSha256"]
        execution = load(v / row["execution"])
        assert execution["observedToolOverlaps"] == execution["unfinishedTools"] == []
        assert load(v / row["coverage"])["allAssignedRangesReturned"]
    initial = list(textual["processes"].values())
    assert datetime.fromisoformat(initial[0]["completedAt"]) < datetime.fromisoformat(initial[1]["startedAt"])
    choice = load(v / "batch-082-choice-reconciliation.json")
    assert choice["correctedSnapshot"] == TEACHING
    confirmations = [r for r in choice["processes"] if r["proposalApplied"]]
    assert [r["actualModels"] for r in confirmations] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
    for row in choice["processes"]:
        assert row["processAccepted"] and row["actualProcessExited"] and row["exitCode"] == 0
        assert sha(v / row["report"]) == row["reportSha256"]
        assert sha(v / row["raw"]) == row["rawSha256"]
    for one, two in zip(choice["processes"], choice["processes"][1:]):
        assert datetime.fromisoformat(one["completedAt"]) < datetime.fromisoformat(two["startedAt"])
    record = load(S / "execution-566.json")
    visual_path = R / record["reconciliation"]
    assert sha(visual_path) == record["reconciliationSha256"]
    visual = load(visual_path)
    assert visual["independentVisualAcceptance"] and visual["runtimeAccepted"]
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedScopedClaims"] == 0
    assert not visual["findings"] and visual["process"]["oneReviewerFamilyActiveAtATime"]
    assert visual["process"]["allChildrenExitedBeforeNext"]
    visual_processes = list(record["processes"].values())
    for row in visual_processes:
        folder = visual_path.parent
        execution = load(folder / row["execution"])
        assert execution["exitCode"] == 0 and len(execution["turns"]) == 30
        assert execution["completePacketReturned"] and execution["distinctImagePayloadsVerified"] == 28
        assert execution["observedToolOverlaps"] == execution["unfinishedTools"] == []
        assert sha(folder / row["report"]) == row["reportSha256"] == execution["reportSha256"]
        assert sha(Path(execution["rawExecutionLocation"])) == row["rawExecutionSha256"]
        for turn in execution["turns"]:
            assert turn["exitCode"] == 0 and turn["singleResourceAccepted"]
            assert turn["actualModels"] == [row["requestedModel"]]
            if "imagePayload" in turn:
                image = turn["imagePayload"]
                assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                assert sha(Path(turn["resource"])) == image["sourceSha256"]
                assert image["sourceDimensions"] == [1080, 2400]
                assert image["returnedDimensions"] == [900, 2000]
        for one, two in zip(execution["turns"], execution["turns"][1:]):
            assert datetime.fromisoformat(one["completedAt"]) < datetime.fromisoformat(two["startedAt"])
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    host = load(S / "execution-563.json")
    assert host["actualGradleExit"] == 0 and host["qualifiedAndroidHead"] == ANDROID
    assert host["fixtureRoot"] == str(R) and host["runtimeBytesUnchanged"]
    for row in host["artifacts"]:
        assert sha(R / row["archivedPath"]) == row["sha256"]
    for row in host["tests"]:
        path = R / "docs" / "n1-reviews" / "batch-082-android" / "corrected-host-563" / (row["name"].split(".")[-1] + ".xml")
        assert sha(path) == row["sha256"]
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(int(xml.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
    assert sum(r["tests"] for r in host["tests"]) == 9
    native = load(S / "execution-565.json")
    assert native["qualifiedAndroidHead"] == ANDROID and native["contentVersion"] == VERSION
    for row in native["archivedReceipts"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "compressedRaw" in row:
            assert sha(R / row["compressedRaw"]) == row["compressedRawSha256"]
            assert hashlib.sha256(gzip.decompress((R / row["compressedRaw"]).read_bytes())).hexdigest() == row["originalSha256"]
    route = native["articleRoute"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1094, 5050, 114, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["quizOnKeys"] == ["じゅん"] and route["quizKunKeys"] == []
    assert route["fullOnyomi"] == route["fullProjectionOnyomi"] == ["ジュン"]
    assert route["fullProjectionQuizOnyomi"] == route["liteQuizOnyomi"] == ["ジュン"]
    assert route["fullKunyomi"] == route["fullProjectionKunyomi"] == route["fullProjectionQuizKunyomi"] == route["liteQuizKunyomi"] == []
    assert {r["kanji"]: r["title"] for r in route["exactDefaultMeaningOptions"]} == {
        "准": "quasi-; associate rank", "冴": "clear; sharp-minded", "冶": "smelt; work metals", "隼": "falcon"}
    assert route["exactCuratedChoicesWithoutFallback"] and route["soleCuratedOnPersistedGoodAndDone"]
    assert route["directedLinkTransitions"] == 4 and route["comparisonLinkTransitions"] == 2
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert route["touchInjectedReferenceStrokes"] == 10 and route["drawingGradeRecordedOnNext"]
    execution = native["nativeExecution"]
    assert execution["terminalSuccessCases"] == 2
    assert len(execution["terminalCases"]) == 2 and all(r["status"] == 0 for r in execution["terminalCases"])
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    raw = v / "batch-082-native-corrected" / "attempt-565" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8-sig"), re.M) == ["1", "0", "1", "0"]
    assert native["imageIndex"]["originalPngCount"] == 51 and native["imageIndex"]["distinctByteGroups"] == 28
    result = load(S / "batch-082-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh main already ancestral; no teaching/tool integration changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=load(L / "checks-567.json"), acceptedHostCasesReverified=9,
        acceptedNativeTerminalCasesReverified=2, newHostNativeOrReviewerRun=False,
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        sourceLevelFinding082V1="resolved at9ce870d1; exact default-four configuration confirmed by corrected HOST/native and both original families.",
        textualReconciliationSha256=sha(v / "batch-082-reconciliation.json"),
        choiceReconciliationSha256=sha(v / "batch-082-choice-reconciliation.json"),
        visualAcceptanceSha256=sha(visual_path), androidEvidenceSha256=sha(S / "execution-563.json"),
        nativeEvidenceSha256=sha(S / "execution-565.json"),
        limits=record["limits"],
        diagnostics=[
            "All six actual gates passed initially. Receipt assertion corrected from stale checkpoint368 to observed372 tests without rerunning successful suite.",
            "Audit-only assumption of bilateral word exclusions corrected: repository exclusions are symmetric direct pairs when declared on either endpoint; only new准教授 declares助教授. No runtime change.",
        ],
    )
    save(S / "batch-082-acceptance-audit.json", result)
    p = load(C / "progress.json")
    save(S / "execution-567.json", {
        "schemaVersion": 1, **p["execution567StartingState"], "recordedAt": now(),
        "status": result["status"], "acceptanceRecord": "batch-082-acceptance-audit.json",
        "publishedAdditions": 108, "remainingAdditions": 1120, "localReviewClosedAdditions": 109,
        "limits": result["limits"], "nextAction": "Normal signed acceptance/ownerfastforward,exactgreenCI/publicZIP,terminal evidence/ownerissue60;yield before083.",
    })
    ledger = load(S / "batch-082-progress.json")
    ledger["preAcceptanceCheckpoint"] = {
        k: copy.deepcopy(ledger[k]) for k in ("status", "reviewClosed", "nextAction", "limits")}
    ledger.update(status="review-closed-combined-tree-accepted-pending-publication",
                  runtimeAccepted=True, acceptanceRecord="batch-082-acceptance-audit.json")
    for row in ledger["supportMappings"]:
        row["status"] = ledger["status"]
    save(S / "batch-082-progress.json", ledger)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p["stage"] = "batch-082-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined-tree and inherited reviewer/HOST/native evidence accepted.")


if __name__ == "__main__":
    {"start": start, "checks": checks, "checks-done": checks_done,
     "source-audit": source_audit, "evidence": evidence}[sys.argv[1]]()
