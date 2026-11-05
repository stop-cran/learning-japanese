"""Batch071 combined-tree acceptance and bounded owner-testing publication."""
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
L = C / "logs" / "bdbde220-4688-441a-8c2b-ad3ee5e73cc9"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-071-acceptance"
BASE = "e8874e6871b4e7e3410093e41422764597b9853e"
TEACHING = "1dc352148065c47d6d3a33206c62f3b877e678f6"
START = "3910febb861b6be55c1a5e1e58cf899d34693a41"
VERSION = "05002d6e68a4eb89"
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
    temporary = path.with_suffix(path.suffix + ".execution471.tmp")
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
    assert p["checkpoint"] == 470 and p["status"] == "continue"
    assert not (L / "before-progress-execution471.json").exists()
    save(L / "before-progress-execution471.json", p)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 470
    p["execution471StartingState"] = {
        "execution": 471, "batch": "071", "startingHead": START, "recordedAt": now(),
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "scope": "SAME071 current-main integration and combined validation, normal signed reviewed owner-testing publication, exact immutable ZIP and CI verification; checkpoint before072. No teaching/reviewer/native/Android rerun/second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete approved issue and complete final470 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "status": "combined-tree-acceptance-in-progress",
    }
    p["stage"] = "batch-071-current-main-combined-validation"
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
    ledger = load(S / "batch-071-progress.json")
    result = audit(R, "071")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison"):
        selection = load(S / f"batch-071-{kind}-selection.json")
        spellings = set(selection.get("requestedSpellings", []))
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("允" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else any(k.text in spellings for k in e.findall("k_ele/keb") + e.findall("r_ele/reb")))]
        name = "batch-071-jmdict.xml" if kind == "lexical" else "batch-071-comparison-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        dispositions = [i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [5, 19] and len(distinct) == 23
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-071-kanjidic2.xml").getroot()

    def normalized(element):
        element = copy.deepcopy(element)
        for node in element.iter():
            if node.text is not None and not node.text.strip():
                node.text = None
            node.tail = None
        return ET.tostring(element)

    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 6
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-070-acceptance-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 71
        assert not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 71:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 98 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[79] == "允"
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
    assert sum(maps.values()) == 8341
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {("允", "words/允可.md")}
    assert not (R / "kanji" / "可.md").exists()
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-071-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-05141-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "允.json") == convert("允", svg.decode("utf-8"))
    assert sha(R / "strokes" / "允.json") == geometry["targetSha256"]
    draft = load(S / "batch-071-draft-audit.json")
    articles = draft["actualAuthoredHanFonts"]["articles"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == draft["actualAuthoredHanFonts"]["characters"] and len(han) == 25
    fonts = []
    for row in draft["actualAuthoredHanFonts"]["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["missing"] == ["儿", "厶"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1083, "words": 5041, "n1Labelled": 103, "namedSourceMembersPresent": 102}
    result.update(
        execution=471, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=23,
        dictionaryFamilyOccurrences=24, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=6, runtimePayloadHashesVerified=8341, manifestMaps=maps,
        allMappedReciprocalPairs=1, mappedDirectedLinks=2,
        unavailableDeclaredComponents=["可; retained metadata, no nonexistent-card link"],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        nativeComparisonHanCount=27, generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test. Authored25Han and native27Han are separate scopes.",
    )
    save(S / "batch-071-acceptance-source-audit.json", result)
    print("23families/24occurrences/6rawcharacters/baseline/98additions/8341hashes/1pair/geometry/cmaps/budgets passed.")


def validate():
    receipts = []
    target = C / "artifacts" / "execution-471-validation-receipts.json"
    assert not target.exists()
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-471-{name}.txt"
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
    textual = load(V / "batch-071-reconciliation.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["processDeviation"]["status"] == "resolved"
    processes = list(textual["processes"].values())
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]]
        for field, digest in (("report", "reportSha256"), ("execution", "executionSha256"), ("coverage", "coverageSha256")):
            assert sha(V / row[field]) == row[digest]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
    assert processes[0]["observedToolOverlaps"] and all(not row["observedToolOverlaps"] for row in processes[1:])
    for first, second in zip(processes, processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    visual = load(V / "batch-071-visual-reconciliation.json")
    record470 = load(S / "execution-470.json")
    assert sha(V / "batch-071-visual-reconciliation.json") == record470["reconciliationSha256"]
    assert visual["allInternalCallsSerial"] and visual["allReviewerProcessesSerialAndExited"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    visual_processes = list(record470["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["verifiedReturnedImages"] == 22
        assert row["allInternalCallsSerial"] and row["processAndCoverageAccepted"]
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    android = load(S / "execution-467.json")
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
    native = load(S / "execution-469.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    artifact_index = load(R / native["artifactIndex"])
    for row in artifact_index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            assert hashlib.sha256(gzip.decompress((R / row["rawGzipPath"]).read_bytes())).hexdigest() == row["originalSha256"]
    raw = V / "batch-071-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-071-native" / "attempt-1" / "n1-071-article-route.json")
    assert route == native["nativeRouteEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1083, 5041, 103, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["quizOnKeys"] == ["いん"] and route["quizKunKeys"] == []
    assert route["fullKunyomi"] == ["じょう", "まこと.に", "ゆるす"]
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(C / "artifacts" / "execution-471-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-471-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    result = load(S / "batch-071-acceptance-source-audit.json")
    limits = record470["limits"] + (
        " Initial Claude overlapping guidance reads and same-session serial corrective reread retained; no retroactive compliance claim. "
        "Fresh combined vocabulary consistency is pilot2122/2431, not full coverage. Bounded owner testing only. "
        "Current-main mechanical acceptance does not remove physical-phone/general-release/whole-set limitations."
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
        originalInitialInternalToolsFullySerial=False, correctiveSerialRereadVerified=True,
        textualReconciliationSha256=sha(V / "batch-071-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-071-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-467.json"), nativeEvidenceSha256=sha(S / "execution-469.json"),
        limits=limits,
    )
    save(S / "batch-071-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py",
                 C / "verify-execution-471.ps1", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-471.json", {
        "schemaVersion": 1, **p["execution471StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-071-acceptance-audit.json",
        "publishedAdditions": 97, "remainingAdditions": 1131, "localReviewClosedAdditions": 98,
        "limits": limits, "nextAction": "Normal signed acceptance/ownerfastforward/greenCI/every immutable public ZIP hash; terminal evidence/CI/ZIP/ownerissue60 then yield before072.",
    })
    p["stage"] = "batch-071-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-071-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8341
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-071-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 471, "batch": "071", "membership": ["允"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "8eb0c1ea9934e6ea7fed3abb7fbb9bdbed45736e",
        "freshAndroidSnapshot": "f6ff96a109f3e7b6a67f41e6b9ee214962c9a39f",
        "nativeEvidenceSnapshot": "43016306901a1111e309e7081e90db258cbc5f2d",
        "visualClosureSnapshot": START, "latestMainIntegrated": acceptance["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-071-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-071-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 98, "remainingAdditions": 1130,
            "currentKanji": 1083, "currentWords": 5041, "n1Labelled": 103, "namedSourceMembersPresent": 102,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 99, "batchChangedReusedArticles": 0,
            "requiredReciprocalPairs": 1, "activatedBaselinePairs": 0,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/ownerissue60; checkpoint and yield before072.",
    }
    assert not (S / "batch-071-publication.json").exists()
    save(S / "batch-071-publication.json", publication)
    ledger = load(S / "batch-071-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=98, remainingAdditions=1130, publishedCommit=head,
        publicationRecord="batch-071-publication.json", acceptanceRecord="batch-071-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-071-progress.json", ledger)
    execution = load(S / "execution-471.json")
    execution.update(status=publication["status"], publicationRecord="batch-071-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-471.json", execution)
    for path in (C / "artifacts" / "batch-071-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-471-accepted-push.txt"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-071-accepted-publication-verified-pending-terminal-evidence"
    p["execution471AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/greenCI/public8341hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-071-publication.json")
    body = f"""**Batch 071 (允) is published and verified for bounded owner testing.** Adds necessary support **允可 (いんか), permission; assent**, with one reciprocal pair/two directed links. No batch 072 started; this is not an N1 vocabulary expansion.

Authored/reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`, fresh Android `{publication['freshAndroidSnapshot']}`, native evidence `{publication['nativeEvidenceSnapshot']}`, visual closure `{START}`. Fresh main `{publication['latestMainIntegrated']}` already ancestral: no teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not complete coverage), fresh manifest `{VERSION}`; frozen input hashes, **23 distinct full dictionary families /24 occurrences** mechanically re-extracted, six raw character records, exact **98 additions**, baseline **985 kanji /4,942 words /985 strokes** with only preserved reviewed 虎/猿/丘/山 exceptions. Full イン /じょう /まこと.に /ゆるす order retained; only イン selected, explicit quizKunyomi empty. All four explanations, thirteen direct word guards, one mapped reciprocal pair/two directions, pinned four-stroke geometry and actual authored25Han cmaps pass. 可 remains declared but has no kanji card or broken link. Mechanical byte checks are not linguistic comprehension.

Blind initial **claude-opus-5.5 /gpt-6.1-sol** reviews share the frozen snapshot and complete two new articles/three facets. Reviewer processes exited serially. Original Claude issued two overlapping guidance reads; report/execution preserved and same-session serial exact-range reread after GPT exit resolves that bounded deviation, not retroactive initial compliance. No actionable teaching defect established; optional historical/provenance/idiom expansion remains optional.

Original-session **dependent** visual confirmations470 exited serially, each33single calls/22same assigned PNGs/complete two articles/fixture/log/route. All44actual returned900x2000payloads archived separately from1080x2400sources: **22 unique source byte-streams /40 archived files**;18duplicates are not fresh scenes. GPT reported word-03 as a strip but read the full construction in word-02. Archived word-03 is full900x2000/844812bytes, identical for both reviewers; coordinator directly saw the complete passage. Returned bytes do not prove every pixel perceived. No actionable teaching/rendering defect established.

Accepted467 **RealContentTest3 +RareHanTest1, no skips**, and469 native **two terminal-status-0 cases /112.22s**, provenance and artifact hashes reverified, not rerun. Exact signed full Git envelope through production **ContentSync once** imported **1,083 kanji /5,041 words /103N1**, problems0, epoch1. Full+Lite full readings retained; sole normalizedいん Good grade/noKunLog/Done1correct. Both article projections/four reading explanations/reciprocal pair/SystemBack/offline/N1selection/actual meaning feedback/fourreference-touch strokes/ungradedtrace/recallmiss/persistedDrawAgain pass. Meaning exits Back before Next, not a new persisted meaning grade.

Four production font rows visibly distinguish native27Han+允可 including isolated儿/厶/口/土 and公/先;108singlePaint+4word probes corroborate nonblankness/distinct rasters, not every-phone readability or actual fallback-face identity. Complementary left/right table captures jointly expose all four reading labels/explanations with horizontal clipping/explicit scrollhint; not every viewport/gesture/bodyH1 certification. Actual meaning choicescamphortree/chestnut/hawkfalcon, NOT authored元兄去 trio or whole-pool certification. No MLKit/human handwriting/recall/successful model download or phone evidence claimed.

Owned emulator5580parent412/QEMU19604 stopped; preexisting5556 unchanged. Historical denials/HOST OOMs retained; qualified **HOST-only2GiBinit NEVER nativebuilds**. No app/guest heap, guard, permission, production app or algorithm change. Original source/retrieval/read-depth and optional limitations retained.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,341runtime hash** and exact manifest. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards; safe paths/per-file limits pass, contributor evidence excluded.

Published **98/1,228 additions;1,130 remain**. Current **1,083kanji /5,041words /103N1-labelled /102named-source members plus separate妖**. Project99necessary support additions are **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**. Durable `docs/n1-sources/batch-071-publication.json`, `batch-071-acceptance-audit.json`, `execution-471.json` and original source/review/native records retained. Exact terminal receipts saved in control. Checkpoint471 **continue**, yield before one bounded072source-preparation checkpoint; overall project incomplete.
"""
    path = C / "execution-471-issue-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution471.json")
    receipt = load(C / "execution-471-issue-receipt.json")
    expected = (C / "execution-471-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-072-progress.json").exists()
    publication = load(S / "batch-071-publication.json")
    next_action = (
        f"Batch071 fully published/terminalCI/publicZIP/ownerissue verified at {head}; yield before072. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/freshmain, then ONE evidence-bounded072source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every new Han font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded original-session confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on denials. "
        "Published98/1228,remaining1130;1083kanji5041words103N1labels102namedmembers plus妖;99necessarysupports NOTN1vocabulary. "
        "Preserve466originalClaude overlappingguidancereads/corrective same-session serialreread afterGPTexit; "
        "allreviewerprocesses serial, no retroactive internal-compliance claim. "
        "470visual processes/internalcalls fullyserial;44actualpayloads fromsame22uniqueof40sourcecaptures, "
        "complete2files/fixture/log/route; not freshblind/allviewport coverage. GPTword03perceivedstrip/fullpayload844812bytes "
        "and completeword02reading retained; complete bytes not everypixelperception. "
        "Inherit467Android3+1 and469native2terminal0/112.22s honestly; no redundant heavy work absentnewconcern. "
        "Preserve source/read-depth/retrieval, sidewaysviewport, fallbackface/MLKit/humanrecall, "
        "HOST-only2GiBinitNEVERnativebuilds, historicaldenials/OOMs/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=471, status="continue", stage="batch-071-published-verified-before-072",
             lastPublishedCommit=head, remainingAdditions=1130, blocker=None, nextAction=next_action)
    p["batch071PublicationCheckpoint"] = publication
    p["execution471StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1130source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 471, "checkpoint": 471, "batch": "071",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8341,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "publishedAdditions": 98, "remainingAdditions": 1130, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": next_action,
    }
    save(C / "execution-471-final-verification.json", result)
    save(C / "batch-071-publication-checkpoint.json", publication)
    p["execution471CoordinatorCheckpoint"] = {**result, "status": "continue"}
    p["batch071PublicationIssueReceipt"] = {
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
