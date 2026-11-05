"""Batch 069 combined acceptance and bounded owner-testing publication."""
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
L = C / "logs" / "236aecb0-3566-46f3-921d-9979858eb059"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-069-acceptance"
START = "33d1a4118634ab4fcb95d120ee9b4e4fe4eb7b34"
BASE = "f9e0511fa6bf2b4f280110b591d813c630da6566"
TEACHING = "f5061bcdf101f8eba5729b21f222b57821df9a38"
VERSION = "83ed94552dd1a9ce"
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
    temporary = path.with_suffix(path.suffix + ".execution455.tmp")
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
    p = load(C / "progress.json")
    assert p["checkpoint"] == 454 and p["batch"] == "069"
    assert git("rev-parse", "HEAD") == START and not git("status", "--porcelain")
    unchanged()
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 454 and embedded["batch"] == "069"
    assert not (L / "before-progress-execution455.json").exists()
    save(L / "before-progress-execution455.json", p)
    p["execution455StartingState"] = {
        "execution": 455, "batch": "069", "startingHead": START, "recordedAt": now(),
        "scope": "SAME069 fresh-main combined acceptance, normally signed owner fast-forward publication, terminal CI/exact immutable public ZIP/owner issue receipts and durable checkpoint only. No070, reviewers, Android/native rerun or second runner.",
        "status": "combined-acceptance-started",
        "freshOriginMain": git("rev-parse", "origin/main"),
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final454 checkpoint and complete approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
    }
    p.update(stage="batch-069-combined-current-main-acceptance",
             nextAction=p["execution455StartingState"]["scope"])
    save(C / "progress.json", p)
    print("Execution455 started; complete live history preserved.")


def source_audit():
    unchanged()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == row["sha256"], name
    for name, section in (("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                          ("n1-implementation-JMdict_e.gz", "jmdict")):
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    ledger = load(S / "batch-069-progress.json")
    result = audit(R, "069")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets = []
    distinct = set()
    for kind in ("lexical", "comparison"):
        selection = load(S / f"batch-069-{kind}-selection.json")
        spellings = set(selection.get("requestedSpellings", []))
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if any(("儒" in k.text if kind == "lexical" else k.text in spellings)
                      for k in e.findall("k_ele/keb"))]
        name = "batch-069-jmdict.xml" if kind == "lexical" else "batch-069-comparison-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        dispositions = [i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [32, 11] and len(distinct) == 41
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-069-kanjidic2.xml").getroot()

    def normalized(element):
        element = copy.deepcopy(element)
        for node in element.iter():
            if node.text is not None and not node.text.strip():
                node.text = None
            node.tail = None
        return ET.tostring(element)

    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 9
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    draft = load(S / "batch-069-draft-audit.json")
    exceptions = {name: {"quiz_exclusions": value}
                  for name, value in draft["explicitInheritedMetadataExceptions"].items()}
    exceptions.update({name: {"distractors": value}
                       for name, value in draft["inheritedKanjiDistractorException"].items()})
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
        assert int(row["batch"]) <= 69, "Next batch unexpectedly started"
        assert not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 69:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 96 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[77] == "儒"
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
    assert sum(maps.values()) == 8334
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert pairs == {("儒", "words/儒教.md"), ("教", "words/儒教.md")}
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-069-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-05112-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "儒.json") == convert("儒", svg.decode("utf-8"))
    assert sha(R / "strokes" / "儒.json") == geometry["targetSha256"]
    articles = ["kanji/儒.md", "words/儒教.md", "kanji/教.md"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    fonts = []
    for row in draft["actualAuthoredHanFonts"]["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1081, "words": 5038, "n1Labelled": 101, "namedSourceMembersPresent": 100}
    result.update(
        execution=455, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=41,
        dictionaryFamilyOccurrences=43, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=9, runtimePayloadHashesVerified=8334, manifestMaps=maps,
        allMappedReciprocalPairs=2, mappedDirectedLinks=4, unavailableMappedPairs=[],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-069-acceptance-source-audit.json", result)
    print("41distinct families/43occurrences/9rawcharacters/baseline/96additions/8334hashes/2pairs/geometry/cmaps/budgets passed.")


def validate():
    receipts = []
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-455-{name}.txt"
        assert not path.exists(), path
        started = now()
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args],
                                    cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({"check": name, "command": ["python", "-X", "utf8", "-B", *args],
                         "startedAt": started, "completedAt": now(), "exitCode": result.returncode,
                         "log": str(path), "sha256": sha(path)})
        save(C / "artifacts" / "execution-455-validation-receipts.json", receipts)
        print(f"{name}: exit {result.returncode}", flush=True)
        if result.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(result.returncode)


def evidence():
    unchanged()
    textual = load(V / "batch-069-reconciliation.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["allInitialInternalToolsSerial"] and textual["serialReviewerProcessesVerified"]
    processes = list(textual["processes"].values())
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]] and not row["observedToolOverlaps"]
        for field, digest in (("report", "reportSha256"), ("execution", "executionSha256"), ("coverage", "coverageSha256")):
            assert sha(V / row[field]) == row[digest]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
    assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
    visual = load(V / "batch-069-visual-reconciliation.json")
    record454 = load(S / "execution-454.json")
    assert sha(V / "batch-069-visual-reconciliation.json") == record454["reconciliationSha256"]
    assert visual["allInternalCallsSerial"] and visual["allReviewerProcessesSerialAndExited"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    visual_processes = list(record454["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["verifiedReturnedImages"] == 16
        assert row["allInternalCallsSerial"] and row["processAndCoverageAccepted"]
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    android = load(S / "execution-451.json")
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
    native = load(S / "execution-453.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    artifact_index = load(R / native["artifactIndex"])
    for row in artifact_index["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            assert hashlib.sha256(gzip.decompress((R / row["rawGzipPath"]).read_bytes())).hexdigest() == row["originalSha256"]
    raw = V / "batch-069-native" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-069-native" / "n1-069-article-route.json")
    assert route == native["nativeRouteEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1081, 5038, 101, 0]
    assert route["acceptedReadingParserEpoch"] == 1 and route["quizOnKeys"] == ["じゅ"] and route["quizKunKeys"] == []
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(C / "artifacts" / "execution-455-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-455-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    result = load(S / "batch-069-acceptance-source-audit.json")
    limits = (
        "Bounded owner testing, not general release. Dependent16/46successfulcapture confirmation; "
        "32returned900x2000payloads from16same1080x2400sources, not32independent scenes/all-PNG/physical-size acceptance. "
        "Exact changed教backlink covered; unchanged教body rendering/context, not renewed full linguistic review. "
        "Sideways clipping with explicit scroll hint does not establish inaccessible content or certify every offset; "
        "儒 final source-note pixels unseen. Actual meaning choices differ from authored儀/僧/優, whose native presentation is not certified. "
        "Drawing reference-touch/ungradedtrace/recallmiss/persistedAgain, not MLKit/human handwriting/successful recall; actual fallback faces unverified. "
        "Original frozen-XML/public-source retrieval/read-depth/gaiji limits retained. Vocabulary pilot gaps not repaired or counted complete. "
        "Original native attempt1timeout and attempt2ownershipabort preserved; separate retry adds destination-title await only. "
        "Historical permission denials/HOST OOMs retained; HOST-only2GiBinit NEVER nativebuilds. "
        "No app/guest heap, production guard, permissions, app code or learning algorithm changes. "
        "Androidf9b59a2+ required; physical-phone/general-release/whole-set acceptance outstanding."
    )
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"),
        latestMainIntegrated=git("rev-parse", "origin/main"),
        normalMergeResult="Fresh main already ancestral; no substantive teaching or tool changes.",
        pythonTests={"passed": int(tests[1]), "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(artifact_index["artifacts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        allInitialAndVisualReviewerInternalCallsSerial=True,
        textualReconciliationSha256=sha(V / "batch-069-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-069-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-451.json"), nativeEvidenceSha256=sha(S / "execution-453.json"),
        limits=limits,
    )
    save(S / "batch-069-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py",
                 C / "verify-execution-455.ps1", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-455.json", {
        "schemaVersion": 1, **p["execution455StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-069-acceptance-audit.json",
        "publishedAdditions": 95, "remainingAdditions": 1133, "localReviewClosedAdditions": 96,
        "limits": limits, "nextAction": "Normal signed acceptance/ownerfastforward/greenCI/every immutable public ZIP hash; terminal evidence/CI/ZIP/ownerissue60 then yield before070.",
    })
    p["stage"] = "batch-069-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-069-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8334
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-069-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 455, "batch": "069", "membership": ["儒"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "00bd022997bf82a85f07614161332f47457613c3",
        "freshAndroidSnapshot": "e245739783dbc2ebe33ee164b8cfa718d670551b",
        "nativeEvidenceSnapshot": "41390d7019b58dd8be521388865164d706b2b34d",
        "visualClosureSnapshot": START, "latestMainIntegrated": acceptance["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-069-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-069-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 96, "remainingAdditions": 1132,
            "currentKanji": 1081, "currentWords": 5038, "n1Labelled": 101, "namedSourceMembersPresent": 100,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 96, "batchChangedReusedArticles": 1,
            "requiredReciprocalPairs": 2, "activatedBaselinePairs": 0,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/ownerissue60; checkpoint and yield before070.",
    }
    assert not (S / "batch-069-publication.json").exists()
    save(S / "batch-069-publication.json", publication)
    ledger = load(S / "batch-069-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=96, remainingAdditions=1132, publishedCommit=head,
        publicationRecord="batch-069-publication.json", acceptanceRecord="batch-069-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-069-progress.json", ledger)
    execution = load(S / "execution-455.json")
    execution.update(status=publication["status"], publicationRecord="batch-069-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-455.json", execution)
    for path in (C / "artifacts" / "batch-069-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-455-accepted-push.txt"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-069-accepted-publication-verified-pending-terminal-evidence"
    p["execution455AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/greenCI/public8334hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-069-publication.json")
    body = f"""**Batch 069 (儒) is published and verified for bounded owner testing.** Adds necessary support **儒教 (じゅきょう), Confucianism**, and the narrow **教** backlink. No batch 070 started; this is not an N1 vocabulary expansion.

Authored/reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`, fresh Android `{publication['freshAndroidSnapshot']}`, native evidence `{publication['nativeEvidenceSnapshot']}`, visual closure `{START}`. Fresh main `{publication['latestMainIntegrated']}` already ancestral: normal integration changed no teaching/tools. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Both owner-scoped normal fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not complete coverage), fresh manifest `{VERSION}`; exact frozen input hashes, **41 distinct full dictionary families /43 occurrences** mechanically re-extracted, nine raw character records, exact **96 additions**, baseline **985 kanji /4,942 words /985 strokes** with only preserved reviewed 虎/猿/丘/山 exceptions. Full readings/order/sole curated ジュ and empty kun preserved; **two mapped reciprocal pairs /four directed links**, reproduced pinned16-stroke geometry and actual affected Han cmaps pass. Mechanical bytes are not linguistic comprehension.

Blind initial **claude-opus-5.5 /gpt-6.1-sol** reviews share the same frozen snapshot/complete new儒 and儒教/exact changed教 passage/three facets. Both processes exited serially; internal calls serial and all19assigned ranges returned, including complete41distinct families/nine character records. No actionable defect established; optional scholar-word expansion not necessary. Original reports, source/retrieval/read-depth limits and independent versus supplied evidence preserved.

Original-session **dependent** visual confirmations454 were serial, each28single calls/16same assigned PNGs/complete three teaching files/529line retry fixture/log/route. All32actual returned900x2000payloads archived separately from1080x2400sources: **16/46 successful capture scope**, not all-PNG acceptance or32independent scenes. Added教backlink visible; unchanged教body rendering/context, not renewed full linguistic review. No established teaching/rendering defect. Sideways table clipping has an explicit hint/complementary offsets; 儒 final source-note pixels, every offset and actual fallback faces remain unverified. Optional dense drawing numbers are existing app polish, not a content defect.

Accepted451 **RealContentTest3 +RareHanTest1, no skips**, and453 native **two terminal-status-0 cases /158.188s** reverified, not rerun. Full signed Git envelope through production **ContentSync once** imported **1,081 kanji /5,038 words /101N1**, problems0, epoch1. Full+Liteジュ/emptyKun; normalizedじゅ Good persisted/noKunLog. Three complete article prose/example projections32selectors, both reciprocal pairs/four directions/SystemBack/offline/N1selection/actual meaning feedback/16reference-touch strokes/ungradedtrace/recallmiss/persistedDrawAgain. Meaning feedback exits Back before Next, not a newly persisted meaning grade. Four production font rows readable/distinguishable for儒需儀僧優人亻教攴攵子考校木 and儒教. Actual meaning options differ from authored儀/僧/優; authored-choice native presentation not certified. No MLKit/human handwriting/successful human recall or phone claim.

Original native attempt1timeout preserved, including failing Article status-2. Separate retry adds only explicit destination-title await after asynchronous SystemBack, with unchanged production/content/guards/heaps/assertions. Attempt2 aborted before launch on actual adb SYN_SENT connection; later fresh ownership check clear, attempt3 passed. Owned helpers stopped; preexisting emulator unchanged. Historical permission denials/HOST OOMs retained; qualified **HOST-only2GiBinit NEVER nativebuilds**. No app/guest heap, guards, permissions, app code or learning algorithm changed.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,334runtime hash** and exact manifest. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards; safe paths/per-file limits pass, contributor evidence excluded.

Published **96/1,228 additions;1,132 remain**. Current **1,081kanji /5,038words /101N1-labelled /100named-source members plus separate妖**. Project96necessary support additions are **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**. Durable `docs/n1-sources/batch-069-publication.json`, `batch-069-acceptance-audit.json`, `execution-455.json` and original source/review/native records retained. Exact terminal receipts saved in control. Checkpoint455 **continue**, yield before one bounded070source-preparation checkpoint; overall project incomplete.
"""
    path = C / "execution-455-issue-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution455.json")
    receipt = load(C / "execution-455-issue-receipt.json")
    expected = (C / "execution-455-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-070-progress.json").exists()
    publication = load(S / "batch-069-publication.json")
    next_action = (
        f"Batch069 fully published/terminalCI/publicZIP/ownerissue verified at {head}; yield before070. "
        "NEXT fresh coordinator: read complete request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/freshmain, then ONE evidence-bounded070source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every new Han font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded original-session confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on denials. "
        "Published96/1228,remaining1132;1081kanji5038words101N1labels100namedmembers plus妖;96necessarysupport additions NOTN1vocabulary. "
        "Preserve069original native timeout/ownershipabort and separately compiled destination-await retry; no production defect established. "
        "450textual and454visual processes/internalcalls fullyserial;45432actualpayloads fromsame16of46successfulcaptures, "
        "complete3files/529linefixture, exactchanged教backlink; not freshblind/allPNG coverage or renewed full教linguisticreview. "
        "Inherit451Android3+1 and453native2terminal0/158.188s honestly; no redundant heavy work absentnewconcern. "
        "Preserve source/read-depth/retrieval, sidewaysviewport/unseen儒source-note, authored-choice/fallback-face/MLKit/humanrecall, "
        "HOST-only2GiBinitNEVERnativebuilds, historicaldenials/OOMs/pushfailures/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=455, status="continue", stage="batch-069-published-verified-before-070",
             lastPublishedCommit=head, remainingAdditions=1132, blocker=None, nextAction=next_action)
    p["batch069PublicationCheckpoint"] = publication
    p["execution455StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1132source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 455, "checkpoint": 455, "batch": "069",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8334,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "publishedAdditions": 96, "remainingAdditions": 1132, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": next_action,
    }
    save(C / "execution-455-final-verification.json", result)
    save(C / "batch-069-publication-checkpoint.json", publication)
    p["execution455CoordinatorCheckpoint"] = {**result, "status": "continue"}
    p["batch069PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({key: result[key] for key in (
        "checkpoint", "savedCommit", "issueUpdate", "publishedAdditions", "remainingAdditions",
        "allOriginalHistoricalRootKeysPreservedExactly", "wholeProjectComplete")}, indent=2))


if __name__ == "__main__":
    {"start": start, "source-audit": source_audit, "validate": validate, "evidence": evidence,
     "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
