"""Batch076 bounded combined-tree acceptance and publication receipts."""
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
L = C / "logs" / "39b94cca-10bb-41ef-a9ac-40ec0bcca842"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-076-acceptance"
BASE = "1ee375280d2b778fa66046627f1b19c3bcb55eec"
START = "9be50c7670ac411c9c4e8670c6a7a9b4708af0ff"
TEACHING = "08d63143e0495940d7cccee4c1808282a533c522"
VERSION = "8bd0a375668bee11"
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
    temporary = path.with_suffix(path.suffix + ".execution511.tmp")
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
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", tree=A) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", tree=A)
    subprocess.run(["git", "merge-base", "--is-ancestor", git("rev-parse", "origin/main"), "HEAD"],
                   cwd=R, check=True)


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
    ledger = load(S / "batch-076-progress.json")
    result = audit(R, "076")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison"):
        selection = load(S / f"batch-076-{kind}-selection.json")
        spellings = {"勤める", "務める", "就任", "掛け持ち", "専任"}
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("兼" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else any(k.text in spellings for k in e.findall("k_ele/keb")))]
        name = "batch-076-jmdict.xml" if kind == "lexical" else "batch-076-comparison-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [70, 5] and len(distinct) == 75
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-076-kanjidic2.xml").getroot()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 5
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-075-acceptance-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 76 and not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 76:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 103 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[84] == "兼"
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
    assert sum(maps.values()) == 8355
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 3
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-076-stroke-evidence.json")
    svg_path = Path(geometry["input"])
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "兼.json") == convert("兼", svg.decode("utf-8"))
    assert sha(R / "strokes" / "兼.json") == geometry["targetSha256"]
    draft = load(S / "batch-076-draft-audit.json")["actualAuthoredHanFonts"]
    articles = draft["articles"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == draft["characters"] and len(han) == 41
    fonts = []
    for row in draft["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["missingActualDraftHan"] == ["亻"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1088, "words": 5045, "n1Labelled": 108, "namedSourceMembersPresent": 107}
    result.update(
        execution=511, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=len(distinct),
        dictionaryFamilyOccurrences=75, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=5, runtimePayloadHashesVerified=8355, manifestMaps=maps,
        allMappedReciprocalPairs=3, mappedDirectedLinks=6, unavailableDeclaredComponents=[],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/quiz/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-076-acceptance-source-audit.json", result)
    print("75families/5rawrecords/baseline/103localadditions/8355hashes/3pairs/geometry/cmaps/budgets passed.")


def validate():
    unchanged()
    assert git("rev-parse", "HEAD") == START
    target = L / "execution-511-validation-receipts.json"
    receipts = load(target) if target.exists() else []
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        previous = [row for row in receipts if row["check"] == name]
        if previous and previous[-1]["exitCode"] == 0:
            print(f"{name}: retained verified successful receipt", flush=True)
            continue
        suffix = f"-retry{len(previous)}" if previous else ""
        path = L / f"execution-511-{name}{suffix}.txt"
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
    textual = load(V / "batch-076-reconciliation.json")
    assert textual["textualReviewClosed"] and textual["actionableRemainingFindings"] == 0
    assert textual["consequentialUnresolvedTeachingFindings"] == 0
    assert all(row["status"] == "resolved" for row in textual["findings"])
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["allInitialInternalToolsSerial"]
    processes = list(textual["processes"].values())
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]]
        for field in ("report", "execution", "coverage"):
            assert sha(V / row[field]) == row[field + "Sha256"]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
        assert row["observedToolOverlapCount"] == row["multiToolResponseCount"] == 0
    for first, second in zip(processes, processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    visual = load(V / "batch-076-visual-reconciliation.json")
    record510 = load(S / "execution-510.json")
    assert sha(V / "batch-076-visual-reconciliation.json") == record510["reconciliationSha256"]
    assert visual["allThreeReviewerProcessesSerialAndExited"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert not visual["allVisualExecutionsInternallySerial"]
    assert visual["claudeBoundedSerialCorrectionAndGptAccepted"]
    visual_processes = list(record510["reviews"].values())
    assert [row["processAndCoverageAccepted"] for row in visual_processes] == [False, True, True]
    for row in visual_processes:
        assert row["exitCode"] == 0
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    for first, second in zip(visual_processes, visual_processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    assert [visual[k] for k in ("sourceCaptures", "uniqueAssignedCaptures", "hashMappedDuplicateCaptures")] == [57, 34, 23]
    android = load(S / "execution-507.json")
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
    native = load(S / "execution-509.json")
    for row in native["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    raw = V / "batch-076-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-076-native" / "attempt-1" / "n1-076-article-route.json")
    assert route == native["routeEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1088, 5045, 108, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["fullOnyomi"] == ["ケン"] and route["fullKunyomi"] == ["か.ねる", "-か.ねる"]
    assert route["quizOnKeys"] == ["けん"] and route["quizKunKeys"] == ["かねる"]
    assert route["bothCuratedKindsPersistedGoodNoDuplicateSuffixAndDone"]
    assert route["mappedReciprocalPairs"] == 3 and route["directedLinkTransitions"] == 6
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(L / "execution-511-validation-receipts.json")
    latest = {row["check"]: row for row in receipts}
    assert len(latest) == 6 and all(row["exitCode"] == 0 for row in latest.values())
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-511-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    limits = record510["limits"] + (
        " Fresh combined vocabulary consistency is pilot2122/2431, not full coverage. Bounded owner testing only. "
        "Historical pending-gate statements remain historical; this acceptance closes only enumerated gates."
    )
    result = load(S / "batch-076-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh main already ancestral; no substantive teaching or tool changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        validationRecovery="Initial local acceptance recipe incorrectly expected comparison requestedSpellings, absent in this batch schema. Corrected to its documented five exact keb spellings; failed receipt retained, only failed/unrun gates rerun. No source/teaching changes.",
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(native["artifacts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        historicalProcessDeviationsPreserved=True,
        textualReconciliationSha256=sha(V / "batch-076-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-076-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-507.json"), nativeEvidenceSha256=sha(S / "execution-509.json"),
        limits=limits,
    )
    save(S / "batch-076-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-511.json", {
        "schemaVersion": 1, **p["execution511StartingState"], "recordedAt": now(),
        "status": result["status"], "acceptanceRecord": "batch-076-acceptance-audit.json",
        "publishedAdditions": 102, "remainingAdditions": 1126, "localReviewClosedAdditions": 103,
        "limits": limits, "nextAction": "Normal signed acceptance, owner fast-forward, exact green CI/public ZIP then terminal evidence/owner issue60; yield before077.",
    })
    p["stage"] = "batch-076-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-076-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8355
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-076-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 511, "batch": "076", "membership": ["兼"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": "3557596ad648e74a636196579b8e202c5ddfbfc3",
        "reviewedTeachingSnapshot": TEACHING, "textualClosureSnapshot": TEACHING,
        "freshAndroidSnapshot": "b89b333682fa5bfb4123ea8f4a74c2cc59935a7c",
        "nativeEvidenceSnapshot": "78f550ade2e27ce3c05d39f7a497c6bc0aacfb57",
        "visualClosureSnapshot": START, "latestMainIntegrated": BASE,
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-076-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-076-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 103, "remainingAdditions": 1125,
            "currentKanji": 1088, "currentWords": 5045, "n1Labelled": 108, "namedSourceMembersPresent": 107,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 103, "batchChangedReusedArticles": 2,
            "requiredReciprocalPairs": 3, "activatedBaselinePairs": 1,
        },
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/owner issue60; checkpoint and yield before077.",
    }
    assert not (S / "batch-076-publication.json").exists()
    save(S / "batch-076-publication.json", publication)
    ledger = load(S / "batch-076-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "nextGate", "limits", "remainingGates")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=103, remainingAdditions=1125, publishedCommit=head,
        publicationRecord="batch-076-publication.json", acceptanceRecord="batch-076-acceptance-audit.json",
        remainingGates="Terminal evidence publication/CI/public ZIP/owner issue update; physicalphone/generalrelease/whole-set outstanding.",
        nextAction=publication["nextAction"],
        nextGate="Terminal publication receipts and owner issue update, then yield before077.",
        limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-076-progress.json", ledger)
    execution = load(S / "execution-511.json")
    execution.update(status=publication["status"], publishedAdditions=103, remainingAdditions=1125,
                     publicationRecord="batch-076-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-511.json", execution)
    for path in (C / "artifacts" / "batch-076-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-511-accepted-push.txt", C / "verify-execution-511.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-076-accepted-publication-verified-pending-terminal-evidence"
    p["execution511AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/green CI/public8355hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-076-publication.json")
    body = f"""**Batch 076 (兼) is published and verified for bounded owner testing.** Adds only necessary support **兼任 (けんにん)**, two exact navigation links in existing **兼ねる** and one Common words bullet in older **任**. **Three all-mapped reciprocal pairs /six directions**, one activated baseline pair; the new word directly excludes 兼ねる because of overlapping role senses. No inferred vocabulary level or batch077.

Authored `{publication['authoredSnapshot']}`; textually corrected/review-closed `{TEACHING}`; fresh Android `{publication['freshAndroidSnapshot']}`; native evidence `{publication['nativeEvidenceSnapshot']}`; visual closure `{START}`. Fresh main `{BASE}` already ancestral: no substantive teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not full coverage), fresh manifest `{VERSION}`, five frozen inputs and **75 distinct complete JMdict families**, five raw character records. Exact **103 additions** and original **985kanji /4,942words /985strokes** baseline preserved, only inherited reviewed 虎/猿/丘/山 metadata exceptions. All three reading dispositions, pinned ten-stroke geometry, three mapped pairs/six directions, all41actual scoped Han cmaps and **8,355 runtime hashes** reverified. Raw **ケン /か.ねる・-か.ねる** order remains; selected **ケン /か.ねる** produces **けん /かねる**. Valid kana-preferred difficulty suffix remains explained, not a duplicate mastery key. The only textual fix clarified を attachment for an additional post OR two posts joined with と.

Blind initial **claude-opus-5.5 /gpt-6.1-sol** share one frozen teaching snapshot and complete dictionary packet, both full new articles and exact changed reused passages, all three facets. All four initial/confirmation processes and internal reads serial. One minor wording finding resolved and confirmed by both original sessions; no consequential unresolved teaching defect. Supplied public observations are not reviewer upstream retrieval/native-speaker certification.

Bounded dependent visual510 confirmation covers full570line fixture/four complete articles, route/terminal evidence and **34 unique captures /57 original PNGs /23 duplicates**. All three reviewer processes exited serially. Original Claude **one response/two concurrent PNG reads/one overlap** remains preserved/noncompliant with original flagFALSE. Same-session bounded correction reread ONLY those two images serially, inheriting32; it does not erase the breach. GPT34uniquePNG/4completeTEXT returns were serial/no repeats or overlaps. All scoped surfaces/all three facets CLEAN, no actionable defect. **41Han/four production families/two words/three panels** readable; fallback-face guess withdrawn, actual face unknown. Complementary table viewports and900x2000payloads from1080x2400sources are not everypixel/gesture/everyphone certification. Extra兼ねる-to兼任 link visible, not separately native-traversed.

Accepted507 **RealContentTest3 +RareHanTest1, no skips**, and509 native attempt1 **two named terminal-status-0 cases**, no skips, hashes/provenance reverified, not rerun. Production **ContentSync ONCE** imports complete signedb89b3336 Git envelope: **1,088kanji /5,045words /108N1**, problems0, epoch1. Actualけん/かねる each persistGood/Done2correct without duplicate suffix logs. All3mappedpairs6directions/SystemBack/offline/N1selection/actual meaning feedback/ten reference-touch strokes/ungradedtrace then recallAgain pass. Supplied assertions/pixels are not reviewer gestures, a new persisted meaning grade, human handwriting/MLKit/successful recall/model download. All57PNG preserved; owned emulator5580parent27628/QEMU29744 stopped, preexisting shared5556 unchanged. Historical denials/failures/OOMs retained; no native/guest/app heap, guards, permissions, algorithms or unrelated app changes.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,355runtime hash**, exact manifest, safe paths/per-file limits and contributor evidence exclusion. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards.

Published **103/1,228 additions;1,125 remain**. Current **1,088kanji /5,045words /108N1-labelled /107named-source members plus separate妖**. The103necessary support articles are **not N1 vocabulary expansion**. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**.

Durable `docs/n1-sources/batch-076-publication.json`, `batch-076-acceptance-audit.json`, `execution-511.json`, updated authoring notes and complete original source/review/native records retained. Exact terminal receipts in control. Checkpoint511 **continue**; yield before one bounded077source-preparation checkpoint. Overall project incomplete.
"""
    path = L / "issue-511-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue body prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "checkpoint-full.json")
    assert original["checkpoint"] == 510
    receipt = load(L / "issue-511-verified.json")
    expected_body = (L / "issue-511-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected_body.replace("\r\n", "\n").rstrip()
    publication = load(S / "batch-076-publication.json")
    next_action = (
        f"Batch076 fully published/terminal CI/public ZIP/owner issue verified at {head}; yield before077. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/fresh main, then ONE evidence-bounded077source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every newHan font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on denials. "
        "Published103/1228,remaining1125;1088kanji5045words108N1labels107namedmembers plus妖;103necessarysupports NOTN1vocabulary. "
        "Inherit506textual two-family closure with076-C1resolved/bothconfirmations,507HOST3+1/no skips,"
        "509native2terminal0,510boundedvisual closure; no redundant heavy work absentnewconcern. "
        "Allthreevisualreviewerprocesses exited serially; originalClaude one response/two concurrentPNG/oneoverlap "
        "remains noncompliant/originalflagFALSE; serialtwoimage correction inherits32, not retroactive fullserial review. "
        "GPT34uniquePNG4TEXT actuallyserial/no repeats/overlaps. 57originalPNG34unique23duplicates;"
        "900x2000returned vs1080x2400source; fallbackface guess withdrawn/unknown. "
        "All41Han/fourfamilies/twowords readable; no everyviewport/fallbackface/phone proof. Extra word-to-word link visible/not separately traversed. "
        "Preserve originals/source-and-readdepthlimits/sidewaysviewport/MLKit/humanrecall/"
        "HOST-only2GiBinitNEVERnativebuilds/historicaldenials/OOMs/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=511, status="continue", stage="batch-076-published-verified-before-077",
             lastPublishedCommit=head, remainingAdditions=1125, blocker=None, nextAction=next_action)
    p["batch076PublicationCheckpoint"] = publication
    p["execution511StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1125source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 511, "checkpoint": 511, "batch": "076",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8355,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 103, "remainingAdditions": 1125, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": next_action, "status": "continue",
    }
    save(L / "execution-511-final-verification.json", result)
    save(L / "batch-076-publication-checkpoint.json", publication)
    p["execution511CoordinatorCheckpoint"] = result
    p["batch076PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({key: result[key] for key in (
        "checkpoint", "savedCommit", "issueUpdate", "publishedAdditions", "remainingAdditions",
        "allOriginalHistoricalRootKeysPreservedExactly", "wholeProjectComplete")}, indent=2))


if __name__ == "__main__":
    {"validate": validate, "source-audit": source_audit, "evidence": evidence,
     "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
