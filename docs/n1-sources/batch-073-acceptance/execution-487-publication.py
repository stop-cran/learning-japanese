"""Bounded batch073 current-main acceptance; no teaching changes."""
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
L = C / "logs" / "f731909f-8502-409e-b026-42caadd3a030"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-073-acceptance"
BASE = "960f66b516d2c750d774813688b5dca62b3e8c32"
START = "0d292ad627db18772e5424c833426f5c247f0bf0"
TEACHING = "c8c2a0ba7dfc794feac5362fcfefa41e8d33ee5a"
VERSION = "1d8a4ee1a97c6bb5"
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
    temporary = path.with_suffix(path.suffix + ".execution487.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now().astimezone().isoformat()


def git(*args, tree=R):
    return subprocess.check_output(["git", "--no-pager", "-c", "core.quotepath=false", *args],
                                   cwd=tree, text=True, encoding="utf-8").strip()


def unchanged():
    assert git("branch", "--show-current") == "content/n1-kanji"
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", tree=A) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", tree=A)
    subprocess.run(["git", "merge-base", "--is-ancestor", git("rev-parse", "origin/main"), "HEAD"],
                   cwd=R, check=True)


def prepare():
    unchanged()
    assert git("rev-parse", "HEAD") == START
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 486 and p["status"] == "continue"
    save(L / "before-progress-execution487.json", p)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 486
    p["execution487StartingState"] = {
        "execution": 487, "batch": "073", "startingHead": START, "recordedAt": now(),
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "scope": "SAME073 fresh current-main combined acceptance and normally signed checkpoint, with bounded owner-testing publication if all gates complete. No teaching/reviewer/native/Android rerun/074/second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete approved issue and complete final486 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "status": "combined-tree-acceptance-in-progress",
    }
    p["stage"] = "batch-073-current-main-combined-validation"
    save(C / "progress.json", p)
    print("Starting scope persisted; complete live history preserved.")


def source_audit():
    unchanged()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == row["sha256"], name
    for name, section in (("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                          ("n1-implementation-JMdict_e.gz", "jmdict")):
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    ledger = load(S / "batch-073-progress.json")
    result = audit(R, "073")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison"):
        selection = load(S / f"batch-073-{kind}-selection.json")
        spellings = set(selection.get("requestedSpellings", []))
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("克" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else any(k.text in spellings for k in e.findall("k_ele/keb") + e.findall("r_ele/reb")))]
        name = "batch-073-jmdict.xml" if kind == "lexical" else "batch-073-comparison-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        dispositions = [i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [22, 7] and len(distinct) == 25
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-073-kanjidic2.xml").getroot()

    def normalized(element):
        element = copy.deepcopy(element)
        for node in element.iter():
            if node.text is not None and not node.text.strip():
                node.text = None
            node.tail = None
        return ET.tostring(element)

    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 8
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-072-acceptance-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 73
        assert not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 73:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 100 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[81] == "克"
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
    assert sum(maps.values()) == 8346
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert pairs == {("克", "words/克服.md"), ("服", "words/克服.md")}
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-073-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-0514b-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "克.json") == convert("克", svg.decode("utf-8"))
    assert sha(R / "strokes" / "克.json") == geometry["targetSha256"]
    draft = load(S / "batch-073-draft-audit.json")
    articles = draft["actualAuthoredHanFonts"]["articles"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == draft["actualAuthoredHanFonts"]["characters"] and len(han) == 27
    fonts = []
    for row in draft["actualAuthoredHanFonts"]["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["missing"] == ["儿"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1085, "words": 5042, "n1Labelled": 105, "namedSourceMembersPresent": 104}
    result.update(
        execution=487, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=25,
        dictionaryFamilyOccurrences=29, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=8, runtimePayloadHashesVerified=8346, manifestMaps=maps,
        allMappedReciprocalPairs=2, mappedDirectedLinks=4, unavailableDeclaredComponents=[],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        nativeComparisonHanCount=27, generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-073-acceptance-source-audit.json", result)
    print("25families/29occurrences/8rawrecords/baseline/100localadditions/8346hashes/2pairs/geometry/cmaps/budgets passed.")


def validate():
    receipts = []
    target = L / "execution-487-validation-receipts.json"
    assert not target.exists()
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-487-{name}.txt"
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
    textual = load(V / "batch-073-reconciliation.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["allInitialInternalToolsSerial"]
    processes = list(textual["processes"].values())
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert not row["observedToolOverlaps"] and row["multiToolResponseCount"] == 0
        assert row["actualModels"] == [row["requestedModel"]]
        for field, digest in (("report", "reportSha256"), ("execution", "executionSha256"), ("coverage", "coverageSha256")):
            assert sha(V / row[field]) == row[digest]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
    assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
    visual = load(V / "batch-073-visual-reconciliation.json")
    record486 = load(S / "execution-486.json")
    assert sha(V / "batch-073-visual-reconciliation.json") == record486["reconciliationSha256"]
    assert visual["allReviewerProcessesSerialAndExited"] and visual["acceptedRepairAndGPTInternalCallsSerial"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert not visual["allHistoricalInternalCallsSerial"]
    assert visual["processDeviation"]["status"] == "resolved"
    visual_processes = list(record486["reviews"].values())
    for name, row in record486["reviews"].items():
        assert row["exitCode"] == 0 and row["verifiedReturnedImages"] == 18
        assert row["processAndCoverageAccepted"] == (name != "claude")
        if name != "claude":
            assert row["toolOverlapStarts"] == row["multiToolResponses"] == 0
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    for first, second in zip(visual_processes, visual_processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    android = load(S / "execution-483.json")
    assert android["exitCode"] == 0
    for row in android["tests"]:
        path = R / row["archivedPath"]
        assert sha(path) == row["sha256"]
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(int(xml.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
        assert xml.attrib["timestamp"] == row["timestamp"]
    assert [row["tests"] for row in android["tests"]] == [3, 1]
    for row in android["fixtureResolution"]:
        assert Path(row["resolvedRoot"]).resolve() == R.resolve()
    for row in android["rawProvenance"] + android["testImplementationsAndHostInit"]:
        assert sha(Path(row["path"])) == row["sha256"]
    native = load(S / "execution-485.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    artifact_index = load(R / native["artifactIndex"])
    for row in artifact_index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            assert hashlib.sha256(gzip.decompress((R / row["rawGzipPath"]).read_bytes())).hexdigest() == row["originalSha256"]
    raw = V / "batch-073-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-073-native" / "attempt-1" / "n1-073-article-route.json")
    assert route == native["route"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1085, 5042, 105, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["fullOnyomi"] == ["コク"] and route["fullKunyomi"] == ["か.つ"]
    assert route["quizOnKeys"] == ["こく"] and route["quizKunKeys"] == []
    assert route["soleCuratedOnPersistedGoodNoKunAndDone"]
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(L / "execution-487-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-487-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    result = load(S / "batch-073-acceptance-source-audit.json")
    limits = record486["limits"] + (
        " Fresh combined vocabulary consistency is pilot2122/2431, not full coverage. Bounded owner testing only. "
        "Historical statements that later gates were pending remain historical; this acceptance closes only enumerated gates."
    )
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"),
        latestMainIntegrated=git("rev-parse", "origin/main"),
        normalMergeResult="Fresh main already ancestral; no substantive teaching or tool changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(artifact_index["files"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        originalInitialInternalToolsFullySerial=True, historicalVisualInternalSerialDeviationPreservedAndRepaired=True,
        textualReconciliationSha256=sha(V / "batch-073-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-073-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-483.json"), nativeEvidenceSha256=sha(S / "execution-485.json"),
        limits=limits,
    )
    save(S / "batch-073-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-487.json", {
        "schemaVersion": 1, **p["execution487StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-073-acceptance-audit.json",
        "publishedAdditions": 99, "remainingAdditions": 1129, "localReviewClosedAdditions": 100,
        "limits": limits, "nextAction": "Normal signed acceptance/owner fastforward/green CI/every immutable public ZIP hash; terminal evidence/CI/ZIP/owner issue60 then yield before074.",
    })
    p["stage"] = "batch-073-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-073-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8346
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-073-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 487, "batch": "073", "membership": ["克"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "182ddf770432e4015096767892f1181ac3122afa",
        "freshAndroidSnapshot": "5d322346c0c8bccdc36769d85f3fb23f4b5cbbee",
        "nativeEvidenceSnapshot": "27813d5ed5478935b7256a54f81f0c91d7e297f9",
        "visualClosureSnapshot": START, "latestMainIntegrated": acceptance["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-073-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-073-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 100, "remainingAdditions": 1128,
            "currentKanji": 1085, "currentWords": 5042, "n1Labelled": 105, "namedSourceMembersPresent": 104,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 0,
            "projectNewNecessarySupportWords": 100, "batchChangedReusedArticles": 2,
            "requiredReciprocalPairs": 2, "activatedBaselinePairs": 1,
        },
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/owner issue60; checkpoint and yield before074.",
    }
    assert not (S / "batch-073-publication.json").exists()
    save(S / "batch-073-publication.json", publication)
    ledger = load(S / "batch-073-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=100, remainingAdditions=1128, publishedCommit=head,
        publicationRecord="batch-073-publication.json", acceptanceRecord="batch-073-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-073-progress.json", ledger)
    execution = load(S / "execution-487.json")
    execution.update(status=publication["status"], publishedAdditions=100, remainingAdditions=1128,
                     publicationRecord="batch-073-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-487.json", execution)
    for path in (C / "artifacts" / "batch-073-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-487-accepted-push.txt", C / "verify-execution-487.ps1"):
        shutil.copyfile(path, D / path.name)
    shutil.copyfile(Path(__file__), D / "execution-487-publication.py")
    p = load(C / "progress.json")
    p["stage"] = "batch-073-accepted-publication-verified-pending-terminal-evidence"
    p["execution487AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/green CI/public8346hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-073-publication.json")
    body = f"""**Batch 073 (克) is published and verified for bounded owner testing.** Reuses existing **克服 (こくふく)** without a new word article or title: exact component link plus the narrow non-clothing example in 服. Two mapped reciprocal pairs/four directions, one activated baseline pair. No batch074 started; this is kanji scope, not an N1 vocabulary expansion.

Authored/reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`, fresh Android `{publication['freshAndroidSnapshot']}`, native evidence `{publication['nativeEvidenceSnapshot']}`, visual closure `{START}`. Fresh main `{BASE}` already ancestral: no integration teaching/tool changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not complete coverage), fresh manifest `{VERSION}`; frozen inputs and **25 distinct complete dictionary families /29 occurrences**, eight raw character records mechanically reverified. Exact **100 additions** and baseline **985kanji /4,942words /985strokes**, only preserved reviewed 虎/猿/丘/山 metadata exceptions. Full コク/か.つ retained; only コク selected, normalizedこく; nativeか.つ source-only with its own explanation. No new support/title/direct exclusion. Both mapped pairs/four directions, pinned seven-stroke geometry and all27 actual authoredHan cmaps pass. Byte/extraction checks are not linguistic comprehension.

Blind initial **claude-opus-5.5 /gpt-6.1-sol** reviews share signed teaching snapshot, all three facets, whole new克 and exact reused克服line24/服line21 passages; all19 assigned ranges,25full families/eight raw records returned. Initial reviewer processes and internal calls serial, no actionable defect. Historical enemy-submission hypothesis withdrawn against actual unchanged wording and source/register; optional 十/兄 contrast and 克明 expansion remain optional.

Original-session **dependent** visual confirmations486 retained original reports and exact returned payload/range/process evidence. Original Claude batched7text/18PNG reads,23overlap starts, despite its serial claim: **not accepted as serial**. Same-session bounded repair26singlecalls reread overlapping scope; zero overlaps. Then GPT30singlecalls, zero overlaps. All reviewer processes exited serially. Both accepted confirmations cover full521line fixture/log/route/three context files/own original report and18uniquePNG. **30source PNG /18unique streams /12duplicates**, not30fresh scenes;54actual returned900x2000payloads over original/repair/GPT from1080x2400sources. No actionable teaching/rendering defect. Optional stroke-number6/7 proximity retained as app-side polish hypothesis, no production change.

Accepted483 **RealContentTest3 +RareHanTest1, no skips**, and485 native **two named terminal-status-0 cases /82.165s**, artifact/provenance hashes reverified, not rerun. Full signed5d322346 Git envelope through production **ContentSync ONCE**: **1,085kanji /5,042words /105N1**, problems0, epoch1. Full+Lite full readings retained; sole curatedOnGood/Done1correct, no kun question/log. Complete new article projection/both reading labels/explanations, exact reused passages, two reciprocal pairs/four directions/SystemBack/offline/N1selection/actual meaning feedback/sevenreference-touch strokes/ungradedtrace/recallAgain pass. No new persisted meaning grade/human handwriting/MLKit/successful recall/model download claimed.

Four production font rows show27Han including isolated儿 and克/古/兄/元/己/勝/服 legible/distinct;108singlePaint+4wordRaster probes corroborate, not fallback-face identity/every-phone proof. Complementary table captures jointly expose labels/examples with horizontal clipping/explicit scroll hint; final source line near lower edge. Returned bytes do not prove comprehension/every pixel/viewport/gesture/physical viewing size. Actual meaning choices chrysanthemum/strange-extraordinary/overcome/vertebra-chinquapin, NOT the authored古兄元 trio or whole-pool certification. Owned emulator5580parent3704/QEMU12804 and shutdown helper stopped; preexisting5556 unchanged. Historical denials/OOMs retained; HOST-only2GiBinit NEVER nativebuilds; no app/guest heap/guard/permission/algorithm changes.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,346runtime hash**, exact manifest, safe paths/per-file limits and contributor evidence exclusion. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards.

Published **100/1,228 additions;1,128 remain**. Current **1,085kanji /5,042words /105N1-labelled /104named-source members plus separate妖**. Project100necessary supports are **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**. Durable `docs/n1-sources/batch-073-publication.json`, `batch-073-acceptance-audit.json`, `execution-487.json` and original source/review/native records retained. Exact terminal receipts in control. Checkpoint487 **continue**, yield before one bounded074source-preparation checkpoint; overall project incomplete.
"""
    path = L / "issue-487-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue body prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution487.json")
    receipt = load(L / "issue-487-verified.json")
    expected = (L / "issue-487-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    publication = load(S / "batch-073-publication.json")
    next_action = (
        f"Batch073 fully published/terminal CI/public ZIP/owner issue verified at {head}; yield before074. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/fresh main, then ONE evidence-bounded074source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every newHan font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded original-session confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on denials. "
        "Published100/1228,remaining1128;1085kanji5042words105N1labels104namedmembers plus妖;100necessarysupports NOTN1vocabulary. "
        "Inherit482initial two-family19range closure;486dependentvisual original Claude serial deviation preserved and repaired "
        "before serialGPT.18uniqueof30sourcePNG,12duplicates not freshreads/everyviewport coverage; actual returned900x2000 vs1080x2400. "
        "Inherit483Android3+1 and485native2terminal0/82.165s honestly; no redundant heavy work absentnewconcern. "
        "Preserve source/read-depth/retrieval, sidewaysviewport, fallbackface/MLKit/humanrecall, "
        "HOST-only2GiBinitNEVERnativebuilds, historicaldenials/OOMs/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=487, status="continue", stage="batch-073-published-verified-before-074",
             lastPublishedCommit=head, remainingAdditions=1128, blocker=None, nextAction=next_action)
    p["batch073PublicationCheckpoint"] = publication
    p["execution487StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1128source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 487, "checkpoint": 487, "batch": "073",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8346,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 100, "remainingAdditions": 1128, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": next_action, "status": "continue",
    }
    save(L / "execution-487-final-verification.json", result)
    save(L / "batch-073-publication-checkpoint.json", publication)
    p["execution487CoordinatorCheckpoint"] = result
    p["batch073PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({key: result[key] for key in (
        "checkpoint", "savedCommit", "issueUpdate", "publishedAdditions", "remainingAdditions",
        "allOriginalHistoricalRootKeysPreservedExactly", "wholeProjectComplete")}, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "source-audit": source_audit, "validate": validate, "evidence": evidence,
     "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
