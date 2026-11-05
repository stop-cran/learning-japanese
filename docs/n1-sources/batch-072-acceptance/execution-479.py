"""Batch072 combined-tree acceptance and bounded owner-testing publication."""
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
L = C / "logs" / "27ce81be-208d-4df4-8ac7-92268e0adcd5"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-072-acceptance"
BASE = "05dd4cc5b97e73abeecafb51b4c50daf9c7cfa02"
TEACHING = "5544e65205879a67b9fc7a127bb6ef4a15152069"
START = "d52a90834c983a41ab44e922ae2ec119c4941528"
VERSION = "900e3a2130afc56b"
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
    temporary = path.with_suffix(path.suffix + ".execution479.tmp")
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


def prepare():
    unchanged()
    assert git("rev-parse", "HEAD") == START
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 478 and p["status"] == "continue"
    assert not (L / "before-progress-execution479.json").exists()
    save(L / "before-progress-execution479.json", p)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 478
    p["execution479StartingState"] = {
        "execution": 479, "batch": "072", "startingHead": START, "recordedAt": now(),
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "scope": "SAME072 current-main combined validation and normally signed reviewed owner-testing publication; exact immutable ZIP/CI/owner issue verification and checkpoint before073. No teaching/reviewer/native/Android rerun/second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete approved issue and final478 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "status": "combined-tree-acceptance-in-progress",
    }
    p["stage"] = "batch-072-current-main-combined-validation"
    save(C / "progress.json", p)
    print("Starting state persisted; full live history preserved.")


def source_audit():
    unchanged()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == row["sha256"], name
    for name, section in (("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                          ("n1-implementation-JMdict_e.gz", "jmdict")):
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    ledger = load(S / "batch-072-progress.json")
    result = audit(R, "072")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison", "quiz"):
        selection = load(S / f"batch-072-{kind}-selection.json")
        spellings = set(selection.get("requestedSpellings", []))
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("充" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else any(k.text in spellings for k in e.findall("k_ele/keb") + e.findall("r_ele/reb")))]
        name = "batch-072-jmdict.xml" if kind == "lexical" else f"batch-072-{kind}-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        dispositions = [i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [84, 15, 10] and len(distinct) == 101
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-072-kanjidic2.xml").getroot()

    def normalized(element):
        element = copy.deepcopy(element)
        for node in element.iter():
            if node.text is not None and not node.text.strip():
                node.text = None
            node.tail = None
        return ET.tostring(element)

    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 11
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-071-acceptance-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 72
        assert not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 72:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 99 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[80] == "充"
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
    assert sum(maps.values()) == 8344
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert pairs == {("充", "words/充てる.md"), ("充", "words/拡充.md")}
    assert not (R / "kanji" / "拡.md").exists()
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-072-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-05145-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "充.json") == convert("充", svg.decode("utf-8"))
    assert sha(R / "strokes" / "充.json") == geometry["targetSha256"]
    draft = load(S / "batch-072-draft-audit.json")
    articles = draft["actualAuthoredHanFonts"]["articles"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == draft["actualAuthoredHanFonts"]["characters"] and len(han) == 50
    fonts = []
    for row in draft["actualAuthoredHanFonts"]["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["missing"] == ["亠", "儿", "厶"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1084, "words": 5042, "n1Labelled": 104, "namedSourceMembersPresent": 103}
    result.update(
        execution=479, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=101,
        dictionaryFamilyOccurrences=109, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=11, runtimePayloadHashesVerified=8344, manifestMaps=maps,
        allMappedReciprocalPairs=2, mappedDirectedLinks=4,
        unavailableDeclaredComponents=["拡; retained metadata, no nonexistent-card link"],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        nativeComparisonHanCount=51, generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test. Authored50Han and native51Han are separate scopes.",
    )
    save(S / "batch-072-acceptance-source-audit.json", result)
    print("101families/109occurrences/11rawcharacters/baseline/99additions/8344hashes/2pairs/geometry/cmaps/budgets passed.")


def validate():
    receipts = []
    target = C / "artifacts" / "execution-479-validation-receipts.json"
    assert not target.exists()
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-479-{name}.txt"
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
    textual = load(V / "batch-072-reconciliation.json")
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
    visual = load(V / "batch-072-visual-reconciliation.json")
    record478 = load(S / "execution-478.json")
    assert sha(V / "batch-072-visual-reconciliation.json") == record478["reconciliationSha256"]
    assert visual["allInternalCallsSerial"] and visual["allReviewerProcessesSerialAndExited"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    visual_processes = list(record478["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["verifiedReturnedImages"] == 24
        assert row["allInternalCallsSerial"] and row["processAndCoverageAccepted"]
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    android = load(S / "execution-475.json")
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
    native = load(S / "execution-477.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    artifact_index = load(R / native["artifactIndex"])
    for row in artifact_index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            assert hashlib.sha256(gzip.decompress((R / row["rawGzipPath"]).read_bytes())).hexdigest() == row["originalSha256"]
    raw = V / "batch-072-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-072-native" / "attempt-1" / "n1-072-article-route.json")
    assert route == native["route"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1084, 5042, 104, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["quizOnKeys"] == ["じゅう"] and route["quizKunKeys"] == ["あてる"]
    assert route["fullKunyomi"] == ["あ.てる", "み.たす"]
    assert route["bothCuratedKindsPersistedGoodNoMitasuAndDone"]
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(C / "artifacts" / "execution-479-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-479-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    result = load(S / "batch-072-acceptance-source-audit.json")
    limits = record478["limits"] + (
        " Fresh combined vocabulary consistency is pilot2122/2431, not full coverage. Bounded owner testing only. "
        "Current-main mechanical acceptance does not remove physical-phone/general-release/whole-set limitations. "
        "Historical statements that later gates were pending remain historical; this acceptance record closes only its enumerated gates."
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
        originalInitialInternalToolsFullySerial=True,
        textualReconciliationSha256=sha(V / "batch-072-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-072-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-475.json"), nativeEvidenceSha256=sha(S / "execution-477.json"),
        limits=limits,
    )
    save(S / "batch-072-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py",
                 C / "verify-execution-479.ps1", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-479.json", {
        "schemaVersion": 1, **p["execution479StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-072-acceptance-audit.json",
        "publishedAdditions": 98, "remainingAdditions": 1130, "localReviewClosedAdditions": 99,
        "limits": limits, "nextAction": "Normal signed acceptance/ownerfastforward/greenCI/every immutable public ZIP hash; terminal evidence/CI/ZIP/ownerissue60 then yield before073.",
    })
    p["stage"] = "batch-072-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-072-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8344
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-072-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 479, "batch": "072", "membership": ["充"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "78787cb45b0387a6e774f2d634b3e0969406ce75",
        "freshAndroidSnapshot": "92f3c2ef6edbeb8dd7b6e7f37227cab8a3e20891",
        "nativeEvidenceSnapshot": "447b590e6bd8ce0a41d3ed82f2d08df6be60d972",
        "visualClosureSnapshot": START, "latestMainIntegrated": acceptance["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-072-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-072-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 99, "remainingAdditions": 1129,
            "currentKanji": 1084, "currentWords": 5042, "n1Labelled": 104, "namedSourceMembersPresent": 103,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 100, "batchChangedReusedArticles": 1,
            "requiredReciprocalPairs": 2, "activatedBaselinePairs": 1,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/ownerissue60; checkpoint and yield before073.",
    }
    assert not (S / "batch-072-publication.json").exists()
    save(S / "batch-072-publication.json", publication)
    ledger = load(S / "batch-072-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=99, remainingAdditions=1129, publishedCommit=head,
        publicationRecord="batch-072-publication.json", acceptanceRecord="batch-072-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-072-progress.json", ledger)
    execution = load(S / "execution-479.json")
    execution.update(status=publication["status"], publishedAdditions=99, remainingAdditions=1129,
                     publicationRecord="batch-072-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-479.json", execution)
    for path in (C / "artifacts" / "batch-072-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-479-accepted-push.txt"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-072-accepted-publication-verified-pending-terminal-evidence"
    p["execution479AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/greenCI/public8344hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-072-publication.json")
    body = f"""**Batch 072 (充) is published and verified for bounded owner testing.** Adds necessary support **充てる (あてる), allocate; earmark**, and the exact component link in existing **拡充 (かくじゅう)**. Two reciprocal pairs/four directions, including one activated baseline pair. No batch 073 started; this is not an N1 vocabulary expansion.

Authored/reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`, fresh Android `{publication['freshAndroidSnapshot']}`, native evidence `{publication['nativeEvidenceSnapshot']}`, visual closure `{START}`. Fresh main `{publication['latestMainIntegrated']}` already ancestral: no teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not complete coverage), fresh manifest `{VERSION}`; frozen input hashes, **101 distinct complete dictionary families /109 occurrences** mechanically re-extracted, eleven raw character records, exact **99 additions**, baseline **985 kanji /4,942 words /985 strokes** with only preserved reviewed 虎/猿/丘/山 exceptions. Full ジュウ /あ.てる /み.たす source order retained; only ジュウ /あ.てる selected. All three explanations, five direct word guards, two mapped reciprocal pairs/four directions, pinned six-stroke geometry and actual authored50Han cmaps pass. 拡 remains declared but has no kanji card or broken link. Mechanical byte checks are not linguistic comprehension.

Blind initial **claude-opus-5.5 /gpt-6.1-sol** reviews share one signed snapshot and cover both complete new articles and exact reused link passage across three facets,30 assigned ranges/26 complete applicable dictionary families/11raw character records. Reviewer processes and internal calls exited serially. No actionable teaching defect established; optional additional compound examples and 残す watchpoint did not establish a defect and were not expanded. Initial source/retrieval/read-depth limitations retained.

Original-session **dependent** visual confirmations478 exited serially, each36single calls/24same assigned PNGs/complete536line fixture/log/route/three whole context files/own original report. All48actual returned900x2000payloads archived separately from1080x2400sources: **24 unique source byte-streams /44 archived files**;20duplicates are not fresh scenes. No actionable teaching/rendering defect established. Complete returned bytes/ranges are not proof of comprehension/every pixel/viewport/gesture/physical viewing size. Coordinator EOF600/536 accounting correction preserved, not a reviewer failure or rerun.

Accepted475 **RealContentTest3 +RareHanTest1, no skips**, and477 native **two named terminal-status-0 cases /100.843s**, provenance and artifact hashes reverified, not rerun. Exact signed full Git envelope through production **ContentSync once** imported **1,084 kanji /5,042 words /104N1**, problems0, epoch1. Full+Lite full readings retained; both normalizedじゅう/あてる Good logs/Done2correct, noみたす question/log. Both complete new article projections/exact reused paragraph/all3 reading labels and explanations/two reciprocal pairs/four directions/SystemBack/offline/N1selection/actual meaning feedback/sixreference-touch strokes/ungradedtrace/recallAgain pass. No new persisted meaning grade/MLKit/human handwriting/recall/successful model download claimed.

Four production font rows visibly distinguish native51Han+2words including isolated亠/儿/厶;204singlePaint+8word probes corroborate nonblankness/distinct rasters, not every-phone readability or actual fallback-face identity. Complementary left/right table captures jointly expose all three reading labels/explanations with horizontal clipping/explicit scrollhint; not every viewport/gesture certification. Actual meaning choicesgrain-bearinghead/suspiciousuncanny/allotfill/Japanesecedar, NOT authored元兄先 trio or whole-pool certification.

Owned emulator5580parent12224/QEMU9228 stopped; preexisting5556 unchanged. Historical denials/HOST OOMs retained; qualified **HOST-only2GiBinit NEVER nativebuilds**. No app/guest heap, guard, permission, production app or algorithm change.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,344runtime hash** and exact manifest. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards; safe paths/per-file limits pass, contributor evidence excluded.

Published **99/1,228 additions;1,129 remain**. Current **1,084kanji /5,042words /104N1-labelled /103named-source members plus separate妖**. Project100necessary support additions are **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**. Durable `docs/n1-sources/batch-072-publication.json`, `batch-072-acceptance-audit.json`, `execution-479.json` and original source/review/native records retained. Exact terminal receipts saved in control. Checkpoint479 **continue**, yield before one bounded073source-preparation checkpoint; overall project incomplete.
"""
    path = C / "execution-479-issue-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution479.json")
    receipt = load(C / "execution-479-issue-receipt.json")
    expected = (C / "execution-479-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-073-progress.json").exists()
    publication = load(S / "batch-072-publication.json")
    next_action = (
        f"Batch072 fully published/terminalCI/publicZIP/ownerissue verified at {head}; yield before073. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/freshmain, then ONE evidence-bounded073source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every new Han font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded original-session confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on denials. "
        "Published99/1228,remaining1129;1084kanji5042words104N1labels103namedmembers plus妖;100necessarysupports NOTN1vocabulary. "
        "Inherit474initial two-family30range textual closure;478dependentvisual processes/internalcalls fullyserial;"
        "48actualpayloads fromsame24uniqueof44sourcecaptures,complete536linefixture/3contextfiles/log/route;"
        "20duplicates not freshreads/everyviewport coverage; EOF600/536coordinator correction retained. "
        "Inherit475Android3+1 and477native2terminal0/100.843s honestly; no redundant heavy work absentnewconcern. "
        "Preserve source/read-depth/retrieval, sidewaysviewport, fallbackface/MLKit/humanrecall, "
        "HOST-only2GiBinitNEVERnativebuilds, historicaldenials/OOMs/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=479, status="continue", stage="batch-072-published-verified-before-073",
             lastPublishedCommit=head, remainingAdditions=1129, blocker=None, nextAction=next_action)
    p["batch072PublicationCheckpoint"] = publication
    p["execution479StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1129source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 479, "checkpoint": 479, "batch": "072",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8344,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "publishedAdditions": 99, "remainingAdditions": 1129, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": next_action,
    }
    save(C / "execution-479-final-verification.json", result)
    save(C / "batch-072-publication-checkpoint.json", publication)
    p["execution479CoordinatorCheckpoint"] = {**result, "status": "continue"}
    p["batch072PublicationIssueReceipt"] = {
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
