"""Batch070 combined-tree acceptance and bounded owner-testing publication."""
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
L = C / "logs" / "c40e5bef-8e4b-4d6c-815b-9c08f737caf0"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-070-acceptance"
BASE = "caf2eebf5d8274adbd68e67349f4d12fffedbb30"
TEACHING = "174ee1d82ddf8bd67dd72c14b411adf3d82e4aef"
START = "8d94a5b092fcc3992bbefd0467fcf1abc5a4bbf7"
VERSION = "a9867cc4b455639a"
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
    temporary = path.with_suffix(path.suffix + ".execution463.tmp")
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


def source_audit():
    unchanged()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == row["sha256"], name
    for name, section in (("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                          ("n1-implementation-JMdict_e.gz", "jmdict")):
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    ledger = load(S / "batch-070-progress.json")
    result = audit(R, "070")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison"):
        selection = load(S / f"batch-070-{kind}-selection.json")
        spellings = set(selection.get("requestedSpellings", []))
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("償" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else any(k.text in spellings for k in e.findall("k_ele/keb") + e.findall("r_ele/reb")))]
        name = "batch-070-jmdict.xml" if kind == "lexical" else "batch-070-comparison-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        dispositions = [i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [77, 13] and len(distinct) == 88
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-070-kanjidic2.xml").getroot()

    def normalized(element):
        element = copy.deepcopy(element)
        for node in element.iter():
            if node.text is not None and not node.text.strip():
                node.text = None
            node.tail = None
        return ET.tostring(element)

    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 7
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    draft = load(S / "batch-070-draft-audit.json")
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
        assert int(row["batch"]) <= 70
        assert not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 70:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 97 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[78] == "償"
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
    assert sum(maps.values()) == 8338
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert len(pairs) == 3
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-070-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-0511f-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "償.json") == convert("償", svg.decode("utf-8"))
    assert sha(R / "strokes" / "償.json") == geometry["targetSha256"]
    articles = ["kanji/償.md", "words/償う.md", "words/補償.md", "kanji/補.md", "words/補う.md"]
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
    assert actual_counts == {"kanji": 1082, "words": 5040, "n1Labelled": 102, "namedSourceMembersPresent": 101}
    result.update(
        execution=463, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=88,
        dictionaryFamilyOccurrences=90, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=7, runtimePayloadHashesVerified=8338, manifestMaps=maps,
        allMappedReciprocalPairs=3, mappedDirectedLinks=6, unavailableMappedPairs=[],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-070-acceptance-source-audit.json", result)
    print("88families/90occurrences/7rawcharacters/baseline/97additions/8338hashes/3pairs/geometry/cmaps/budgets passed.")


def validate():
    receipt_path = C / "artifacts" / "execution-463-validation-receipts.json"
    receipts = load(receipt_path) if receipt_path.exists() else []
    if any(row["exitCode"] for row in receipts):
        save(C / "artifacts" / "execution-463-original-failed-validation-receipts.json", receipts)
        receipts = [row for row in receipts if row["exitCode"] == 0]
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        if any(row["check"] == name for row in receipts):
            continue
        suffix = "-corrected" if name == "source-audit" and (L / "execution-463-source-audit.txt").exists() else ""
        path = L / f"execution-463-{name}{suffix}.txt"
        assert not path.exists(), path
        started = now()
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args],
                                    cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({"check": name, "command": ["python", "-X", "utf8", "-B", *args],
                         "startedAt": started, "completedAt": now(), "exitCode": result.returncode,
                         "log": str(path), "sha256": sha(path)})
        save(C / "artifacts" / "execution-463-validation-receipts.json", receipts)
        print(f"{name}: exit {result.returncode}", flush=True)
        if result.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(result.returncode)


def evidence():
    unchanged()
    textual = load(V / "batch-070-reconciliation.json")
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
    visual = load(V / "batch-070-visual-reconciliation.json")
    record462 = load(S / "execution-462.json")
    assert sha(V / "batch-070-visual-reconciliation.json") == record462["reconciliationSha256"]
    assert visual["allInternalCallsSerial"] and visual["allReviewerProcessesSerialAndExited"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    visual_processes = list(record462["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["verifiedReturnedImages"] == 23
        assert row["allInternalCallsSerial"] and row["processAndCoverageAccepted"]
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    android = load(S / "execution-459.json")
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
    native = load(S / "execution-461.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    artifact_index = load(R / native["artifactIndex"])
    for row in artifact_index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            assert hashlib.sha256(gzip.decompress((R / row["rawGzipPath"]).read_bytes())).hexdigest() == row["originalSha256"]
    raw = V / "batch-070-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-070-native" / "attempt-1" / "n1-070-article-route.json")
    assert route == native["nativeRouteEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1082, 5040, 102, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["quizOnKeys"] == ["しょう"] and route["quizKunKeys"] == ["つぐなう"]
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(C / "artifacts" / "execution-463-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-463-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    result = load(S / "batch-070-acceptance-source-audit.json")
    limits = record462["limits"] + (
        " Initial Claude had two overlapping140line XML reads, retained and resolved by same-session serial exact-range reread "
        "after GPT exit; no retroactive initial-compliance claim. Fresh combined vocabulary consistency is pilot2122/2431, "
        "not full coverage. Review/native source/retrieval/read-depth and historical denials/OOMs preserved. "
        "Bounded owner testing only; no app/guest heap, guard, permissions, production app or algorithm change."
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
        textualReconciliationSha256=sha(V / "batch-070-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-070-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-459.json"), nativeEvidenceSha256=sha(S / "execution-461.json"),
        coordinatorAuditCorrection="Initial comparison selector incorrectly checked only keb, missing kana-headed reb matches such as カバー. It failed closed before evidence/signing/publication. Corrected to frozen exact keb-or-reb rule; original failure log/receipts retained. Native artifact index uses files, not historical artifacts key.",
        limits=limits,
    )
    save(S / "batch-070-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py",
                 C / "verify-execution-463.ps1", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-463.json", {
        "schemaVersion": 1, **p["execution463StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-070-acceptance-audit.json",
        "publishedAdditions": 96, "remainingAdditions": 1132, "localReviewClosedAdditions": 97,
        "limits": limits, "nextAction": "Normal signed acceptance/ownerfastforward/greenCI/every immutable public ZIP hash; terminal evidence/CI/ZIP/ownerissue60 then yield before071.",
    })
    p["stage"] = "batch-070-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-070-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8338
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-070-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 463, "batch": "070", "membership": ["償"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "57aab075a61f0ac38aeb76784a6a04ddc9b8d2d8",
        "freshAndroidSnapshot": "fce81d63caba02c311d9d87ba955002ec79fc4c9",
        "nativeEvidenceSnapshot": "f05c73d26f1091e03cfcbaaba33d7dab41eca461",
        "visualClosureSnapshot": START, "latestMainIntegrated": acceptance["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-070-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-070-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 97, "remainingAdditions": 1131,
            "currentKanji": 1082, "currentWords": 5040, "n1Labelled": 102, "namedSourceMembersPresent": 101,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 2,
            "projectNewNecessarySupportWords": 98, "batchChangedReusedArticles": 2,
            "requiredReciprocalPairs": 3, "activatedBaselinePairs": 0,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/ownerissue60; checkpoint and yield before071.",
    }
    assert not (S / "batch-070-publication.json").exists()
    save(S / "batch-070-publication.json", publication)
    ledger = load(S / "batch-070-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=97, remainingAdditions=1131, publishedCommit=head,
        publicationRecord="batch-070-publication.json", acceptanceRecord="batch-070-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-070-progress.json", ledger)
    execution = load(S / "execution-463.json")
    execution.update(status=publication["status"], publicationRecord="batch-070-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-463.json", execution)
    for path in (C / "artifacts" / "batch-070-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-463-accepted-push.txt"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-070-accepted-publication-verified-pending-terminal-evidence"
    p["execution463AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/greenCI/public8338hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-070-publication.json")
    body = f"""**Batch 070 (償) is published and verified for bounded owner testing.** Adds necessary supports **償う (つぐなう), make amends / compensate for loss**, and **補償 (ほしょう), compensation for loss**, plus the narrow **補** backlink and **補う** comparison link. No batch 071 started; this is not an N1 vocabulary expansion.

Authored/reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`, fresh Android `{publication['freshAndroidSnapshot']}`, native evidence `{publication['nativeEvidenceSnapshot']}`, visual closure `{START}`. Fresh main `{publication['latestMainIntegrated']}` already ancestral: no teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not complete coverage), fresh manifest `{VERSION}`; exact frozen input hashes, **88 distinct full dictionary families /90 occurrences** mechanically re-extracted, seven raw character records, exact **97 additions**, baseline **985 kanji /4,942 words /985 strokes** with only preserved reviewed 虎/猿/丘/山 exceptions. Full readings/order and curated **ショウ /つぐな.う** preserved; **three mapped reciprocal pairs /six directed links**, reproduced pinned17-stroke geometry and actual affected Han cmaps pass. Seven direct word quiz exclusions preserved. Mechanical byte checks are not linguistic comprehension.

Blind initial **claude-opus-5.5 /gpt-6.1-sol** reviews share the frozen snapshot, complete three new articles, exact two reused changes in full context and three facets. Reviewer processes exited serially; both received all24assigned ranges including complete88distinct families/seven character records. **Original Claude had two overlapping140line XML reads**; original report/execution preserved, followed by same-session serial exact-range reread after GPT exit. This resolves the bounded process deviation, not retroactive initial compliance. No actionable teaching defect established; optional extra words/etymology/easier-deck rewrites not required.

Original-session **dependent** visual confirmations462 were serial, each37single calls/23same assigned PNGs/complete five teaching files/596line fixture/log/route. All46actual returned900x2000payloads archived separately from1080x2400sources: **23/75 source-capture scope**, not all-PNG acceptance or46independent scenes. Changed補backlink/補うcomparison visible; unchanged reused bodies rendering/context, not renewed full linguistic review. No established teaching/rendering defect. Claude cannot confidently distinguish isolated衤/礻 at resized transport; GPT distinguishes them; original100nativePaintprobes and coordinator views retained. No unanimous fine-glyph certainty, actual fallback-face identity or every-phone certification. Scroll-hinted table clipping is not established inaccessibility.

Accepted459 **RealContentTest3 +RareHanTest1, no skips**, and461 native **two terminal-status-0 cases /178.905s** reverified, not rerun. Exact signed full Git envelope through production **ContentSync once** imported **1,082 kanji /5,040 words /102N1**, problems0, epoch1. Full+Lite full/curatedショウ,つぐな.う; normalizedしょう/つぐなう and both Good grades persisted. All five article projections/three reciprocal pairs six directions plus補↔補う and補う→補償/SystemBack/offline/N1selection/actual meaning feedback/17reference-touch strokes/ungradedtrace/recallmiss/persistedDrawAgain pass. Meaning exits Back before Next, not a new persisted meaning grade. Four production font rows readable for償賞儀僧億人亻補衣衤礻甫捕手扌初複保証埋損害 and償う補償補う. No successful MLKit/human handwriting/recall or physical-phone evidence claimed.

Owned emulator5580parent17652/QEMU9972 stopped; preexisting5556 unchanged. Transient sharedADB reconnect and OS TIME_WAIT preserved; no shared process killed. Historical permission denials/HOST OOMs retained; qualified **HOST-only2GiBinit NEVER nativebuilds**. No app/guest heap, guards, permissions, production app or learning algorithms changed. Original source/retrieval/read-depth/gaiji limits and optional existing dense drawing/practice wording observations retained.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,338runtime hash** and exact manifest. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards; safe paths/per-file limits pass, contributor evidence excluded.

Published **97/1,228 additions;1,131 remain**. Current **1,082kanji /5,040words /102N1-labelled /101named-source members plus separate妖**. Project98necessary support additions are **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**. Durable `docs/n1-sources/batch-070-publication.json`, `batch-070-acceptance-audit.json`, `execution-463.json` and original source/review/native records retained. Exact terminal receipts saved in control. Checkpoint463 **continue**, yield before one bounded071source-preparation checkpoint; overall project incomplete.
"""
    path = C / "execution-463-issue-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution463.json")
    receipt = load(C / "execution-463-issue-receipt.json")
    expected = (C / "execution-463-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-071-progress.json").exists()
    publication = load(S / "batch-070-publication.json")
    next_action = (
        f"Batch070 fully published/terminalCI/publicZIP/ownerissue verified at {head}; yield before071. "
        "NEXT fresh coordinator: read complete request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/freshmain, then ONE evidence-bounded071source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every new Han font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded original-session confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on denials. "
        "Published97/1228,remaining1131;1082kanji5040words102N1labels101namedmembers plus妖;98necessarysupports NOTN1vocabulary. "
        "Preserve458originalClaude two small overlappingXMLreads and corrective same-session serial reread afterGPTexit; "
        "allreviewerprocesses serial, no retroactive internal-compliance claim. "
        "462visual processes/internalcalls fullyserial;46actualpayloads fromsame23of75sourcecaptures, "
        "complete5files/596linefixture, exactchanged補backlink/補うcomparison; not freshblind/allPNG coverage or renewed full reused linguisticreview. "
        "Inherit459Android3+1 and461native2terminal0/178.905s honestly; no redundant heavy work absentnewconcern. "
        "Preserve source/read-depth/retrieval, sidewaysviewport, Claudeisolated衤礻transport uncertainty, fallbackface/MLKit/humanrecall, "
        "HOST-only2GiBinitNEVERnativebuilds, historicaldenials/OOMs/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=463, status="continue", stage="batch-070-published-verified-before-071",
             lastPublishedCommit=head, remainingAdditions=1131, blocker=None, nextAction=next_action)
    p["batch070PublicationCheckpoint"] = publication
    p["execution463StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1131source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 463, "checkpoint": 463, "batch": "070",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8338,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "publishedAdditions": 97, "remainingAdditions": 1131, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": next_action,
    }
    save(C / "execution-463-final-verification.json", result)
    save(C / "batch-070-publication-checkpoint.json", publication)
    p["execution463CoordinatorCheckpoint"] = {**result, "status": "continue"}
    p["batch070PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({key: result[key] for key in (
        "checkpoint", "savedCommit", "issueUpdate", "publishedAdditions", "remainingAdditions",
        "allOriginalHistoricalRootKeysPreservedExactly", "wholeProjectComplete")}, indent=2))


if __name__ == "__main__":
    {"source-audit": source_audit, "validate": validate, "evidence": evidence,
     "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
