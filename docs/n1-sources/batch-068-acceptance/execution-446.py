"""Batch 068 combined-tree acceptance and bounded publication receipts."""
import copy
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "988fcc90-c5bd-4b86-911c-9ed945acf352"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-068-acceptance"
START = "e312232f38f13216e7d967e00a01261525a4d9ef"
BASE = "72f99d821fa4b8b6e77b622f7f8356e5a67b2b28"
TEACHING = "80f5f424729d8832cdc9ecb8491b59559d921cd3"
VERSION = "ddef65b637fe2f85"
sys.path.insert(0, str(R / "tools"))
from audit_n1_batch import audit, base_file
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256
from check_content_budget import archive_names, check, CONTENT_FOLDERS
from extract_n1_jmdict import extract
from fontTools.ttLib import TTFont
from generate_strokes import convert


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".execution446.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


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
    assert p["checkpoint"] == 445 and p["batch"] == "068"
    assert git("rev-parse", "HEAD") == START and not git("status", "--porcelain")
    unchanged()
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["batch068VisualConfirmationCheckpoint"]["savedCommit"] == START
    assert not (L / "before-progress-execution446.json").exists()
    save(L / "before-progress-execution446.json", p)
    p["execution446StartingState"] = {
        "execution": 446, "batch": "068", "startingHead": START, "recordedAt": now(),
        "scope": "SAME068 fresh-main combined acceptance, normal signed owner fast-forward publication, CI/exact immutable ZIP receipts and durable checkpoint only. No069, reviewer/Android/native rerun or second runner.",
        "status": "combined-acceptance-started",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final445 and complete approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "freshOriginMain": git("rev-parse", "origin/main"),
    }
    p.update(stage="batch-068-combined-current-main-acceptance",
             nextAction=p["execution446StartingState"]["scope"])
    save(C / "progress.json", p)
    print("Execution446 started; complete live history preserved.")


def source_audit():
    unchanged()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == row["sha256"], name
    for name, section in (("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                          ("n1-implementation-JMdict_e.gz", "jmdict")):
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    ledger = load(S / "batch-068-progress.json")
    result = audit(R, "068")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    comparisons = set(load(S / "batch-068-comparison-selection.json")["selectionSpellings"])
    groups = {"lexical": [], "comparison": []}
    for entry in ET.fromstring(gzip.decompress(dictionary)).findall("entry"):
        forms = {e.text for e in entry.findall("k_ele/keb") + entry.findall("r_ele/reb")}
        kind = "lexical" if any("儀" in form for form in forms) else "comparison" if forms & comparisons else None
        if kind:
            groups[kind].append(entry.findtext("ent_seq"))
    packets = []
    for kind, ids in groups.items():
        name = "batch-068-jmdict.xml" if kind == "lexical" else "batch-068-comparison-jmdict.xml"
        assert load(S / f"batch-068-{kind}-selection.json")["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert set(ids) == {i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]}
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [134, 12]
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-068-kanjidic2.xml").getroot()
    def normalized(element):
        element = copy.deepcopy(element)
        ET.indent(element, space="  ")
        return ET.tostring(element, encoding="unicode").strip()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 10
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-068-draft-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 68, "Next batch unexpectedly started"
        assert not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 68:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 95 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[76] == "儀"
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
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
    assert sum(maps.values()) == 8331
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 8
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-068-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-05100-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "儀.json") == convert("儀", svg.decode("utf-8"))
    assert sha(R / "strokes" / "儀.json") == geometry["targetSha256"]
    articles = ["kanji/儀.md"] + sorted({row["article"] for row in ledger["changedReusedPassages"]})
    han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                               "\n".join((R / name).read_text(encoding="utf-8") for name in articles))))
    fonts = []
    for row in load(S / "font-coverage.json")["fonts"]:
        path = A / row["path"]
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        fonts.append({"path": row["path"], "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1080, "words": 5037, "n1Labelled": 100, "namedSourceMembersPresent": 99}
    result.update(
        execution=446, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDictionaryFamilies=146,
        dictionaryPackets=packets, completeRawCharacterRecordsVerified=10,
        runtimePayloadHashesVerified=8331, manifestMaps=maps,
        allMappedReciprocalPairs=8, mappedDirectedLinks=16, unavailableMappedPairs=[],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-068-acceptance-source-audit.json", result)
    print("Frozen146families/10rawcharacters/baseline/95additions/8331hashes/8pairs/geometry/cmaps/budgets passed.")


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
        path = L / f"execution-446-{name}.txt"
        assert not path.exists(), path
        started = now()
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args],
                                    cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({"check": name, "command": ["python", "-X", "utf8", "-B", *args],
                         "startedAt": started, "completedAt": now(), "exitCode": result.returncode,
                         "log": str(path), "sha256": sha(path)})
        save(C / "artifacts" / "execution-446-validation-receipts.json", receipts)
        print(f"{name}: exit {result.returncode}", flush=True)
        if result.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(result.returncode)


def evidence():
    unchanged()
    textual = load(V / "batch-068-reconciliation.json")
    assert textual["textualReviewClosed"] and all(row["status"] in {"resolved", "withdrawn", "optional"} for row in textual["findings"])
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    processes = list(textual["processes"].values())
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]]
        for field, digest in (("report", "reportSha256"), ("execution", "executionSha256"), ("coverage", "coverageSha256")):
            assert sha(V / row[field]) == row[digest]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
    assert all(datetime.fromisoformat(x["completedAt"]) < datetime.fromisoformat(y["startedAt"])
               for x, y in zip(processes, processes[1:]))
    assert not textual["allConfirmationInternalToolsSerial"]
    assert textual["historicalConfirmationOverlap"]["overlapMilliseconds"] == 13
    assert not processes[-1]["observedToolOverlaps"]
    visual = load(V / "batch-068-visual-reconciliation.json")
    record445 = load(S / "execution-445.json")
    assert sha(V / "batch-068-visual-reconciliation.json") == record445["reconciliationSha256"]
    assert visual["allInternalCallsSerial"] and visual["allReviewerProcessesSerialAndExited"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    for row in record445["reviews"].values():
        assert row["exitCode"] == 0 and row["verifiedReturnedImages"] == 20
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    android = load(S / "execution-442.json")
    assert android["exitCode"] == 0
    for row in android["tests"]:
        path = R / row["archivedPath"]
        assert sha(path) == row["sha256"]
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(int(xml.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
        assert xml.attrib["timestamp"] == row["timestamp"]
    for row in android["fixtureResolution"]:
        assert Path(row["resolvedRoot"]).resolve() == R.resolve()
    for row in android["rawProvenance"] + android["testImplementationsAndHostInit"]:
        assert sha(Path(row["path"])) == row["sha256"]
    assert [row["tests"] for row in android["tests"]] == [3, 1]
    native = load(S / "execution-444.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    artifact_index = load(R / native["artifactIndex"])
    for row in artifact_index["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            assert hashlib.sha256(gzip.decompress((R / row["rawGzipPath"]).read_bytes())).hexdigest() == row["originalSha256"]
    raw = V / "batch-068-native" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-068-native" / "n1-068-article-route.json")
    assert route == native["nativeRouteEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1080, 5037, 100, 0]
    assert route["acceptedReadingParserEpoch"] == 1 and route["quizOnKeys"] == ["ぎ"] and route["quizKunKeys"] == []
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(C / "artifacts" / "execution-446-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    text = (L / "execution-446-python-tests.txt").read_text(encoding="utf-8")
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)", text)
    assert tests and int(tests[1]) >= 368
    result = load(S / "batch-068-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"),
        latestMainIntegrated=git("rev-parse", "origin/main"),
        normalMergeResult="Fresh main already ancestral; no substantive teaching or tool changes.",
        pythonTests={"passed": int(tests[1]), "failures": 0, "errors": 0}, validationReceipts=receipts,
        acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(artifact_index["artifacts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        historicalTextualProcessExceptionPreserved=True, allHistoricalInternalReviewerReadsSerial=False,
        textualReconciliationSha256=sha(V / "batch-068-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-068-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-442.json"), nativeEvidenceSha256=sha(S / "execution-444.json"),
        limits=record445["limits"] + " Original441 Claude13ms textual overlap and one-call original-session repair remain preserved; initial and445internal calls serial. Actual meaning choices differ from authored億/優/倍; authored-choice native presentation not certified. Vocabulary pilot gaps retained, not repaired or counted complete. Bounded owner testing only; Androidf9b59a2+ required. No runtime, app/guest heap, guard, permission or app code changes. Historical permission denials/HOST OOMs retained; HOST-only2GiBinit NEVER nativebuilds.",
    )
    save(S / "batch-068-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    shutil.copyfile(Path(__file__), D / Path(__file__).name)
    p = load(C / "progress.json")
    save(S / "execution-446.json", {
        "schemaVersion": 1, **p["execution446StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-068-acceptance-audit.json",
        "publishedAdditions": 94, "remainingAdditions": 1134, "localDraftAdditions": 95,
        "limits": result["limits"], "nextAction": "Normal signed acceptance/ownerfastforward/greenCI/every immutable ZIP hash; terminal evidence/CI/ZIP/ownerissue60 then yield before069.",
    })
    p["stage"] = "batch-068-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-068-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8331
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-068-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 446, "batch": "068", "membership": ["儀"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": "5bfb668dae3b2acd99720d88a15e5fc2feb397ae",
        "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "c5af362d7af0ad1f0e5070169d5caae65d4d985e",
        "visualClosureSnapshot": START, "latestMainIntegrated": acceptance["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-068-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-068-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 95, "remainingAdditions": 1133,
            "currentKanji": 1080, "currentWords": 5037, "n1Labelled": 100, "namedSourceMembersPresent": 99,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 0,
            "projectNewNecessarySupportWords": 95, "batchChangedReusedArticles": 8,
            "requiredReciprocalPairs": 8, "activatedBaselinePairs": 4,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/ownerissue60; checkpoint and yield before069.",
    }
    assert not (S / "batch-068-publication.json").exists()
    save(S / "batch-068-publication.json", publication)
    ledger = load(S / "batch-068-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: ledger[key] for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=95, remainingAdditions=1133, publishedCommit=head,
        publicationRecord="batch-068-publication.json", acceptanceRecord="batch-068-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-068-progress.json", ledger)
    execution = load(S / "execution-446.json")
    execution.update(status=publication["status"], publicationRecord="batch-068-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-446.json", execution)
    for path in (C / "artifacts" / "batch-068-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-446-accepted-push.txt"):
        shutil.copyfile(path, D / path.name)
    shutil.copyfile(Path(__file__), D / Path(__file__).name)
    p = load(C / "progress.json")
    p["stage"] = "batch-068-accepted-publication-verified-pending-terminal-evidence"
    p["execution446AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/greenCI/public8331hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-068-publication.json")
    body = f"""**Batch 068 (儀) is published and verified for bounded owner testing.** No batch 069 started.

Adds one kanji and its pinned generated 15-stroke file; no new support words. Four existing support words **儀式 (ぎしき), 礼儀 (れいぎ), 行儀 (ぎょうぎ), お辞儀 (おじぎ)** plus four counterpart kanji **式・礼・行・辞** receive eight narrow reciprocal-link passages. All **eight mapped pairs / 16 directions** checked, including the four activated baseline pairs; existing identities, readings, easier levels and exclusions preserved.

Initial frozen teaching `5bfb668dae3b2acd99720d88a15e5fc2feb397ae`; suffix-scope correction reviewed at `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`, bounded visual closure `{START}`. Fresh main `{publication['latestMainIntegrated']}` already ancestral: no substantive merge or teaching/tool changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Both normal owner fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not complete coverage), fresh manifest `{VERSION}`; exact frozen input hashes and **146 full-family mechanical re-extractions**, ten raw character records; exact **95 additions**, baseline **985 kanji / 4,942 words / 985 strokes** with only preserved reviewed 虎/猿/丘/山 exceptions; source readings/order/curation, all mapped links, reproduced pinned geometry and affected Han cmaps. Mechanical hashes establish bytes, not linguistic comprehension.

Independent initial **claude-opus-5.5 / gpt-6.1-sol** reviews share the frozen snapshot, complete nine-file teaching scope and three facets. Shared minor suffix finding resolved with typical self/own-side attachment, humble nuance and sourced **私儀 (わたくしぎ)**; original-session confirmations retained. **Original441 Claude13ms overlap between own-report/diff reads remains disclosed**, followed by its one-call serial repair; not relabelled fully serial. Dependent visual confirmations445 were fully serial, each41single calls and20assigned PNGs, complete nine teaching files and696line fixture/log/route. All40actual returned900x2000payloads archived separately from1080x2400sources: **20/127 capture scope, not full-PNG acceptance**. All eight reused changed passages and revised suffix note assigned explicitly. No consequential in-scope defect remains established; optional polish not expanded.

Accepted442 fresh **RealContentTest3 + RareHanTest1, no skips**, and444 native **two terminal-status-0 cases /272.859s** reverified, not redundantly rerun. Exact full Git envelope through production **ContentSync once** imported **1,080 kanji /5,037 words /100N1**, problems0, epoch1. Full+Liteギ/emptyKun; sole normalizedぎ Good persisted/noKunLog. Nine complete article prose/example projections98selectors; all mapped links/SystemBack/offline/N1selection/actual meaning feedback/15reference-stroke touch/ungradedtrace/recallmiss/persistedDrawAgain. Four readable production font rows with 儀義億優倍人亻式礼辞行亍弋彳礻 and all four support words;60singlePaint+16wholewordraster probes. Owned emulator stopped; no owner device modified. Native API35 emulator is **not phone evidence**.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,331 runtime hash** and the exact manifest. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,} entries / {archive['compressedBytes']:,} compressed / {archive['inflatedBytes']:,} inflated / {archive['retainedBytes']:,} retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards; safe paths/per-file limits pass, contributor evidence excluded.

Published **95/1,228 additions;1,133 remain**. Current **1,080 kanji /5,037 words /100N1-labelled /99named-source members plus separate妖**. The project95 necessary support additions are **not an N1 vocabulary deck**.

**Limits:** bounded viewport checks, not all127screenshots; sideways table clipping has an explicit scroll hint, without certification of every offset. Actual meaning choices differ from authored億/優/倍, whose native presentation is not certified. No actual fallback-face identification, MLKit/human handwriting or successful human recall. Original dictionary retrieval/gaiji/read-depth limits, permission denials, HOST OOMs and textual overlap/repair retained; qualified HOST-only2GiBinit NEVER nativebuilds. No app/guest heap, production guard, permissions, app code or learning algorithm changed.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance remains outstanding**. Durable `docs/n1-sources/batch-068-publication.json`, `batch-068-acceptance-audit.json`, `execution-446.json` and original source/review/native records retained. Exact terminal CI/ZIP/issue receipts are in control artifacts. Checkpoint446 status **continue**, yield before one bounded069source-preparation checkpoint; overall project incomplete.
"""
    path = C / "execution-446-issue-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution446.json")
    receipt = load(C / "execution-446-issue-receipt.json")
    expected = (C / "execution-446-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-069-progress.json").exists()
    publication = load(S / "batch-068-publication.json")
    next_action = (
        f"Batch068 fully published/terminalCI/publicZIP/ownerissue verified at {head}; yield before069. "
        "NEXT fresh coordinator: read complete request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/freshmain, then ONE evidence-bounded069source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every new Han font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded original-session confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on denials. "
        "Published95/1228,remaining1133;1080kanji5037words100N1labels99namedmembers plus妖;95necessarysupport additions NOTN1vocabulary. "
        "Preserve068original441Claude13ms two-text-call overlap and one-call original-session repair;445allserial40actualpayloads "
        "fromsame20of127captures, complete9files/696linefixture, all8changedpassages/revised私儀note; not freshblind/allPNG coverage. "
        "Inherit442Android3+1 and444native2terminal0/272.859s honestly; no redundant heavy work absentnewconcern. "
        "Preserve source/read-depth/retrieval, sidewaysviewport, authored-choice/fallback-face/MLKit/humanrecall, "
        "HOST-only2GiBinitNEVERnativebuilds, historicaldenials/OOMs/pushfailures/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=446, status="continue", stage="batch-068-published-verified-before-069",
             lastPublishedCommit=head, remainingAdditions=1133, blocker=None, nextAction=next_action)
    p["batch068PublicationCheckpoint"] = publication
    p["execution446StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1133source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 446, "checkpoint": 446, "batch": "068",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8331,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "textualProcessExceptionAndSerialRepairPreserved": True,
        "publishedAdditions": 95, "remainingAdditions": 1133, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": next_action,
    }
    save(C / "execution-446-final-verification.json", result)
    save(C / "batch-068-publication-checkpoint.json", publication)
    p["execution446CoordinatorCheckpoint"] = {**result, "status": "continue"}
    p["batch068PublicationIssueReceipt"] = {
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
