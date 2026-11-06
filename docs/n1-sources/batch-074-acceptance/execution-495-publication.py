"""Batch074 bounded combined acceptance and publication checkpoint."""
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
L = C / "logs" / "7f1d6bb7-19b0-4ddd-babf-835888ae694c"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-074-acceptance"
BASE = "4e4173513e33061e35abf19d25be499c57b06978"
START = "56732dce1b278c4ce4e8f4ad53bfc65c043a84ee"
TEACHING = "75fbfc7dc734c7ff5d9771fbd5103afd3f3fdc1c"
VERSION = "c507eceeb764bc3f"
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
    temporary = path.with_suffix(path.suffix + ".execution495.tmp")
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
    assert p["checkpoint"] == 494 and p["status"] == "continue"
    save(L / "before-progress-execution495.json", p)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 494
    p["execution495StartingState"] = {
        "execution": 495, "batch": "074", "startingHead": START, "recordedAt": now(),
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "scope": "SAME074 fresh current-main combined acceptance, normal signed commits, owner fast-forward publication and exact CI/public ZIP acceptance. No teaching/reviewer/native/HOST rerun/075/second runner.",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, entire approved issue and complete final494 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "status": "combined-tree-acceptance-in-progress",
    }
    p["stage"] = "batch-074-current-main-combined-validation"
    save(C / "progress.json", p)
    print("495 starting scope persisted; complete live history preserved.")


def source_audit():
    unchanged()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == row["sha256"], name
    for name, section in (("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                          ("n1-implementation-JMdict_e.gz", "jmdict")):
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    ledger = load(S / "batch-074-progress.json")
    result = audit(R, "074")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison", "support-comparison"):
        selection = load(S / f"batch-074-{kind}-selection.json")
        spellings = set(selection.get("requestedSpellings", []))
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("免" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else any(k.text in spellings for k in e.findall("k_ele/keb") + e.findall("r_ele/reb")))]
        name = "batch-074-jmdict.xml" if kind == "lexical" else f"batch-074-{kind}-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        key = {"lexical": "lexicalDispositions", "comparison": "comparisonDispositions",
               "support-comparison": "supportComparisonDispositions"}[kind]
        dispositions = [i for row in ledger[key] for i in row["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [173, 8, 5] and len(distinct) == 182
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-074-kanjidic2.xml").getroot()

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
    exceptions = load(S / "batch-073-acceptance-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 74
        assert not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 74:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 101 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[82] == "免"
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
    assert sum(maps.values()) == 8349
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 5
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-074-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-0514d-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "免.json") == convert("免", svg.decode("utf-8"))
    assert sha(R / "strokes" / "免.json") == geometry["targetSha256"]
    draft = load(S / "batch-074-draft-audit.json")
    articles = draft["actualAuthoredHanFonts"]["articles"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == draft["actualAuthoredHanFonts"]["characters"] and len(han) == 43
    fonts = []
    for row in draft["actualAuthoredHanFonts"]["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["missingActualDraftHan"] == ["儿"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1086, "words": 5043, "n1Labelled": 106, "namedSourceMembersPresent": 105}
    result.update(
        execution=495, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=182,
        dictionaryFamilyOccurrences=186, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=8, runtimePayloadHashesVerified=8349, manifestMaps=maps,
        allMappedReciprocalPairs=5, mappedDirectedLinks=10, unavailableDeclaredComponents=[],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-074-acceptance-source-audit.json", result)
    print("182families/186occurrences/8rawrecords/baseline/101localadditions/8349hashes/5pairs/geometry/cmaps/budgets passed.")


def validate():
    receipts = []
    target = L / "execution-495-validation-receipts.json"
    assert not target.exists()
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-495-{name}.txt"
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


def continue_validation():
    target = L / "execution-495-validation-receipts.json"
    receipts = load(target)
    assert len(receipts) == 5 and receipts[-1]["exitCode"] == 1
    assert "KeyError: 'missing'" in Path(receipts[-1]["log"]).read_text(encoding="utf-8")
    for name, args in (
        ("source-audit-corrected", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-495-{name}.txt"
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
    textual = load(V / "batch-074-reconciliation.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["bothConfirmationInternalToolsSerial"]
    assert not textual["allInitialInternalToolsSerial"]
    processes = list(textual["processes"].values())
    for name, row in textual["processes"].items():
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]]
        assert sha(V / row["report"]) == row["reportSha256"]
        execution = load(V / row["execution"])
        assert execution["reportSha256"] == row["reportSha256"]
        assert execution["rawExecutionSha256"] == row["rawExecutionSha256"]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
        assert (V / row["coverage"]).is_file()
        if name != "initial-claude":
            assert not row["observedToolOverlaps"] and row["multiToolResponseCount"] == 0
        else:
            assert len(row["observedToolOverlaps"]) == row["multiToolResponseCount"] == 1
    for first, second in zip(processes, processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    visual = load(V / "batch-074-visual-reconciliation.json")
    record494 = load(S / "execution-494.json")
    assert sha(V / "batch-074-visual-reconciliation.json") == record494["reconciliationSha256"]
    assert visual["allReviewerProcessesSerialAndExited"] and visual["bothVisualExecutionsInternallySerial"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert not visual["allHistoricalInternalCallsSerial"]
    visual_processes = list(record494["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["verifiedReturnedImages"] == 32
        assert row["processAndCoverageAccepted"]
        assert row["toolOverlapStarts"] == row["multiToolResponses"] == 0
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    android = load(S / "execution-491.json")
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
    native = load(S / "execution-493.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    artifact_index = load(R / native["artifactIndex"])
    for row in artifact_index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "rawGzipPath" in row:
            assert sha(R / row["rawGzipPath"]) == row["rawGzipSha256"]
            assert hashlib.sha256(gzip.decompress((R / row["rawGzipPath"]).read_bytes())).hexdigest() == row["originalSha256"]
    raw = V / "batch-074-native" / "attempt-3" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-074-native" / "attempt-3" / "n1-074-article-route.json")
    assert route == native["route"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1086, 5043, 106, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["fullOnyomi"] == ["メン"] and route["fullKunyomi"] == ["まぬか.れる", "まぬが.れる"]
    assert route["quizOnKeys"] == ["めん"] and route["quizKunKeys"] == ["まぬがれる"]
    assert route["bothCuratedKindsPersistedGoodNoAlternateAndDone"]
    assert route["mappedReciprocalPairs"] == 5 and route["directedLinkTransitions"] == 10
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(L / "execution-495-validation-receipts.json")
    assert len(receipts) == 7
    assert [r["exitCode"] for r in receipts] == [0, 0, 0, 0, 1, 0, 0]
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-495-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    result = load(S / "batch-074-acceptance-source-audit.json")
    limits = record494["limits"] + (
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
        originalInitialInternalToolsFullySerial=False, initialSingleSmallReadOverlapPreserved=True,
        laterOriginalSessionConfirmationsInternallySerial=True,
        helperCorrection="Initial audit used previous batch font key missing; actual074 key missingActualDraftHan. Original failed log preserved; corrected audit passes without runtime edits.",
        textualReconciliationSha256=sha(V / "batch-074-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-074-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-491.json"), nativeEvidenceSha256=sha(S / "execution-493.json"),
        limits=limits,
    )
    save(S / "batch-074-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-495.json", {
        "schemaVersion": 1, **p["execution495StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-074-acceptance-audit.json",
        "publishedAdditions": 100, "remainingAdditions": 1128, "localReviewClosedAdditions": 101,
        "limits": limits, "nextAction": "Normal signed acceptance/owner fastforward/green CI/every immutable public ZIP hash; terminal evidence/CI/ZIP/owner issue60 then yield before075.",
    })
    p["stage"] = "batch-074-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-074-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8349
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-074-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 495, "batch": "074", "membership": ["免"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "7ac69f1adde82ccffd3767379f6fdc2ed549c20b",
        "freshAndroidSnapshot": "4078c7d42e6bc2173c555e73d0bd39fb5d69eb08",
        "nativeEvidenceSnapshot": "564561b6ef566d6117fd9c70e41f12158589fc7e",
        "visualClosureSnapshot": START, "latestMainIntegrated": acceptance["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-074-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-074-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 101, "remainingAdditions": 1127,
            "currentKanji": 1086, "currentWords": 5043, "n1Labelled": 106, "namedSourceMembersPresent": 105,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 101, "batchChangedReusedArticles": 3,
            "requiredReciprocalPairs": 5, "activatedBaselinePairs": 2,
        },
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/owner issue60; checkpoint and yield before075.",
    }
    assert not (S / "batch-074-publication.json").exists()
    save(S / "batch-074-publication.json", publication)
    ledger = load(S / "batch-074-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=101, remainingAdditions=1127, publishedCommit=head,
        publicationRecord="batch-074-publication.json", acceptanceRecord="batch-074-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-074-progress.json", ledger)
    execution = load(S / "execution-495.json")
    execution.update(status=publication["status"], publishedAdditions=101, remainingAdditions=1127,
                     publicationRecord="batch-074-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-495.json", execution)
    for path in (C / "artifacts" / "batch-074-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-495-accepted-push.txt", C / "verify-execution-495.ps1"):
        shutil.copyfile(path, D / path.name)
    shutil.copyfile(Path(__file__), D / "execution-495-publication.py")
    p = load(C / "progress.json")
    p["stage"] = "batch-074-accepted-publication-verified-pending-terminal-evidence"
    p["execution495AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/green CI/public8349hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-074-publication.json")
    body = f"""**Batch 074 (免) is published and verified for bounded owner testing.** Adds the necessary support **免れる (まぬがれる)**; links existing **免許 (N3)** and **免税 (N2)** without changing their identities/metadata, plus the narrow 許 example. Five mapped reciprocal pairs/ten directions, two activated baseline pairs; three direct new-word quiz exclusions. No batch075 started; this is kanji scope, not an N1 vocabulary expansion.

Authored/reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`, fresh Android `{publication['freshAndroidSnapshot']}`, native evidence `{publication['nativeEvidenceSnapshot']}`, visual closure `{START}`. Fresh main `{BASE}` already ancestral: no integration teaching/tool changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not complete coverage), fresh manifest `{VERSION}`; frozen inputs and **182 distinct complete dictionary families /186 occurrences**, eight raw character records mechanically reverified. Exact **101 additions** and baseline **985kanji /4,942words /985strokes**, only preserved reviewed 虎/猿/丘/山 metadata exceptions. Full メン/まぬか.れる/まぬが.れる source order retained; curated メン/まぬが.れる => めん/まぬがれる. **Both native pronunciations are valid**; exclusion of the alternate prevents duplicate variant questions, not a rarity/incorrectness claim. Every metadata reading has its own disposition. All five mapped pairs/ten directions, pinned eight-stroke geometry and all43 authoredHan cmaps pass. Original helper font-field KeyError preserved; corrected to actual074 schema, no runtime changes.

Blind initial **claude-opus-5.5 /gpt-6.1-sol** reviews share signed teaching snapshot, all three facets, whole new免/免れる and exact reused免許line25/免税line26/許line38 passages; all26 assigned ranges returned to both. Complete family/raw-character packets available. No actionable defect. Initial reviewer processes exited serially; original Claude had **one concurrent small 兄/元 read**, disclosed and preserved. Both bounded original-session textual confirmations and both visual confirmations use serial internal tools; no claim that later passes erase the historical overlap. Optional extra comparisons/dismissal pattern/source pointer remain optional.

Dependent original-session visual confirmations494: original Claude then GPT; both entire595line fixture/log/route/five context files/own reports and32uniquePNG returned. **57original PNG /32unique streams /25duplicates**, not57fresh scenes;64actual returned900x2000payloads from1080x2400sources. Allfive scoped surfaces/allthree facets CLEAN. Complementary horizontally scrolled tables jointly expose allthree labels/examples/variant qualifications; newword source link clipped in09, fully visible in12. All43Han including isolated儿 and免/兄/元/先/許/税 readable across four production families, plus three whole words;172singlePaint+12word probes are not fallback-face identity/every-phone evidence. No new blind initial review, teaching/app edits or speculative fallback attribution.

Accepted491 **RealContentTest3 +RareHanTest1, no skips**, and493 native attempt3 **two named terminal-status-0 cases /128.836s**, full artifact/provenance hashes reverified, not rerun. Full signed4078c7d4 Git envelope through production **ContentSync ONCE**: **1,086kanji /5,043words /106N1**, problems0, epoch1. Full+Lite raw/curated lists retained; both actual curated kinds persistGood/Done2correct, no excluded alternate key/log. Complete new article projections/exact reused passages/fivepairs/tendirections/SystemBack/offline/N1selection/actual meaning feedback/eightreference-touch strokes/ungradedtrace/recallAgain pass. Supplied runtime assertions/static screenshots are not reviewer gestures, everyviewport proof, new persisted meaning grade, human handwriting/MLKit/successful recall/model download evidence.

Historical493attempt1 native cases passed but ASCII-only retrieval omitted27Unicode-named PNGs; original preserved. Attempt2 refused own shutdown TIME_WAIT/sharedADB SynSent prelaunch; no native. Attempt3 waited180s for natural release with identical ports/ownership gates/fixture/assertions/heaps/guards and Unicode-letter filename retrieval; all57PNGs retrieved. Owned5580parent30460/QEMU11920 exited, preexisting5556 unchanged. All historical denials/OOMs/limits retained; HOST-only2GiBinit NEVER nativebuilds, no guest/app heap/guard/permission/algorithm changes.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,349runtime hash**, exact manifest, safe paths/per-file limits and contributor evidence exclusion. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards.

Published **101/1,228 additions;1,127 remain**. Current **1,086kanji /5,043words /106N1-labelled /105named-source members plus separate妖**. Project101necessary supports are **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**. Durable `docs/n1-sources/batch-074-publication.json`, `batch-074-acceptance-audit.json`, `execution-495.json` and original source/review/native records retained. Exact terminal receipts in control. Checkpoint495 **continue**, yield before one bounded075source-preparation checkpoint; overall project incomplete.
"""
    path = L / "issue-495-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue body prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution495.json")
    receipt = load(L / "issue-495-verified.json")
    expected = (L / "issue-495-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    publication = load(S / "batch-074-publication.json")
    next_action = (
        f"Batch074 fully published/terminal CI/public ZIP/owner issue verified at {head}; yield before075. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/fresh main, then ONE evidence-bounded075source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every newHan font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded original-session confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on denials. "
        "Published101/1228,remaining1127;1086kanji5043words106N1labels105namedmembers plus妖;101necessarysupports NOTN1vocabulary. "
        "Inherit490initial two-family26range closure and494dependentvisual32uniqueof57sourcePNG/25duplicates honestly; "
        "original initialClaude ONE concurrent兄/元 read preserved, subsequent original-session confirmations internallyserial. "
        "Actual returned900x2000 vs1080x2400, not everyviewport/fallbackface/phone proof. "
        "Inherit491Android3+1 and493native2terminal0/128.836s; no redundant heavy work absentnewconcern. "
        "Keep Unicode-letter filename retrieval for future native scripts;493attempt1captureloss/attempt2ownershiprefusal/attempt3accepted "
        "all preserved. Bothまぬかれる/まぬがれる valid, quiz variantselection notrarityclaim. "
        "Preserve source/read-depth/retrieval, sidewaysviewport, fallbackface/MLKit/humanrecall, "
        "HOST-only2GiBinitNEVERnativebuilds, historicaldenials/OOMs/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=495, status="continue", stage="batch-074-published-verified-before-075",
             lastPublishedCommit=head, remainingAdditions=1127, blocker=None, nextAction=next_action)
    p["batch074PublicationCheckpoint"] = publication
    p["execution495StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1127source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 495, "checkpoint": 495, "batch": "074",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8349,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 101, "remainingAdditions": 1127, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": next_action, "status": "continue",
    }
    save(L / "execution-495-final-verification.json", result)
    save(L / "batch-074-publication-checkpoint.json", publication)
    p["execution495CoordinatorCheckpoint"] = result
    p["batch074PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({key: result[key] for key in (
        "checkpoint", "savedCommit", "issueUpdate", "publishedAdditions", "remainingAdditions",
        "allOriginalHistoricalRootKeysPreservedExactly", "wholeProjectComplete")}, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "source-audit": source_audit, "validate": validate,
     "continue-validation": continue_validation, "evidence": evidence,
     "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
