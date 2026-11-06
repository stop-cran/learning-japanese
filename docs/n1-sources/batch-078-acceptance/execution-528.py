"""Bounded batch 078 combined-tree acceptance and publication receipts."""
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
L = C / "logs" / "e32e73a1-af39-408c-a925-70af94d75384"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-078-acceptance"
BASE = "d7170f11e271a8de47bd2fd152e7196b96bff189"
START = "70a28b861eb57f8b765f2ac57d660360fb6ac13a"
TEACHING = "02b9634acda285bd60d00884479dee2a29ccb6e2"
VERSION = "8e06edf2b0857b26"
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
    temporary = path.with_suffix(path.suffix + ".execution528.tmp")
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


def start():
    unchanged()
    assert git("rev-parse", "HEAD") == START
    assert git("rev-parse", "origin/main") == BASE
    assert not git("status", "--porcelain")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 527 and p["status"] == "continue" and p["batch"] == "078"
    assert "execution528StartingState" not in p
    save(L / "progress-before-execution-528.json", p)
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p["execution528StartingState"] = {
        "execution": 528, "batch": "078", "startingHead": START, "freshOriginMain": BASE,
        "recordedAt": now(), "status": "combined-tree-acceptance-in-progress",
        "scope": "SAME078 combined-current-main acceptance and authorized publication if every gate passes; no079, redundant reviewer/native/HOST run or second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, final527, complete approved issue and durable path preflight directly inspected. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated worktrees clean; signed content70a28b86 and Androidf9b59a2. Fresh main d7170f11 already ancestral; no merge or teaching reconciliation needed. Canonical repositories not accessed.",
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    p["stage"] = "batch-078-combined-tree-acceptance-in-progress"
    save(C / "progress.json", p)
    print("Starting scope persisted with complete prior progress preserved.")


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
    ledger = load(S / "batch-078-progress.json")
    result = audit(R, "078")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison", "related"):
        selection = load(S / f"batch-078-{kind}-selection.json")
        selected = set(selection["entryIds"])
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("冗" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else e.findtext("ent_seq") in selected)]
        name = "batch-078-jmdict.xml" if kind == "lexical" else f"batch-078-{kind}-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [47, 26, 6] and len(distinct) == 78
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-078-kanjidic2.xml").getroot()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 6
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-077-acceptance-source-audit.json")["explicitInheritedMetadataExceptions"]
    exceptions["words/冗談.md"] = {"quiz_exclusions": ["ユーモア"]}
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
        assert int(row["batch"]) <= 78 and not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 78:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 105 and old_chars <= current
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
    assert sum(maps.values()) == 8360
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 2
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    draft = load(S / "batch-078-draft-audit.json")
    geometry = draft["geometry"]
    svg_path = Path(geometry["input"])
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "冗.json") == convert("冗", svg.decode("utf-8"))
    assert sha(R / "strokes" / "冗.json") == geometry["targetSha256"]
    font_audit = draft["actualAuthoredHanFonts"]
    articles = font_audit["articles"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == sorted(font_audit["characters"]) and len(han) == 27
    fonts = []
    for row in font_audit["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["missingActualDraftHan"] == ["冖", "几"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1090, "words": 5046, "n1Labelled": 110, "namedSourceMembersPresent": 109}
    result.update(
        execution=528, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newReviewedBaselineMetadataSafeguard={"words/冗談.md": exceptions["words/冗談.md"]},
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        exactFrozenDistinctDictionaryFamilies=len(distinct), dictionaryFamilyOccurrences=79,
        dictionaryPackets=packets, completeRawCharacterRecordsVerified=6,
        runtimePayloadHashesVerified=8360, manifestMaps=maps, allMappedReciprocalPairs=2,
        mappedDirectedLinks=4, unavailableDeclaredComponents=[], actualCounts=actual_counts,
        actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Mechanical source/family/baseline/membership/readings/quiz/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native run. Comparison/related membership retained from reviewed committed selections.",
    )
    save(S / "batch-078-acceptance-source-audit.json", result)
    print("78families/6rawrecords/baseline/105localadditions/8360hashes/2pairs/geometry/cmaps/budgets passed.")


def evidence():
    unchanged()
    textual = load(V / "batch-078-reconciliation.json")
    assert textual["textualReviewClosed"] and textual["actionableRemainingFindings"] == 0
    assert textual["consequentialUnresolvedTeachingFindings"] == 0
    assert all(row["status"] == "resolved" for row in textual["findings"])
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["allInitialInternalToolsSerial"]
    assert textual["allConfirmationInternalToolsSerial"]
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
    visual = load(V / "batch-078-visual-reconciliation.json")
    record527 = load(S / "execution-527.json")
    assert sha(V / "batch-078-visual-reconciliation.json") == record527["reconciliationSha256"]
    assert visual["serialProcessesAndCompleteArchiveBeforeNextLaunch"]
    assert visual["eachReviewerInternallySerial"] and not visual["findings"]
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedScopedTeachingFindings"] == 0
    assert [visual[k] for k in ("originalCaptures", "eachReviewerDistinctPngs", "exactByteAliases")] == [43, 24, 19]
    assert record527["bothOriginalSessionProcessesSerialAndExited"]
    assert record527["bothVisualExecutionsInternallySerial"]
    visual_processes = list(record527["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["imagePayloadsVerified"] == 24
        assert row["completeSourcePacketReturned"]
        assert row["observedToolOverlaps"] == row["multiToolResponses"] == 0
    assert [r["actualModels"] for r in visual_processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
    for first, second in zip(visual_processes, visual_processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    for row in record527["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    android = load(S / "execution-524.json")
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
        assert sha(Path(row["path"])) == row["sha256"]
        assert sha(R / row["archivedPath"]) == row["sha256"]
    for row in android["testImplementationsAndHostInit"]:
        assert sha(Path(row["path"])) == row["sha256"]
    native = load(S / "execution-526.json")
    for row in native["archivedArtifacts"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"]
        if "decompressedSha256" in row:
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == row["decompressedSha256"]
    raw = V / "batch-078-native" / "attempt-1" / "instrumentation.txt.gz"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      gzip.decompress(raw.read_bytes()).decode("utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-078-native" / "attempt-1" / "n1-078-article-route.json")
    assert route == native["articleRoute"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1090, 5046, 110, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["fullOnyomi"] == route["fullProjectionQuizOnyomi"] == route["liteQuizOnyomi"] == ["ジョウ"]
    assert route["fullKunyomi"] == route["fullProjectionQuizKunyomi"] == route["liteQuizKunyomi"] == []
    assert route["quizOnKeys"] == ["じょう"] and route["quizKunKeys"] == []
    assert route["soleCuratedOnPersistedGoodAndDoneNoKun"]
    assert route["mappedReciprocalPairs"] == 2 and route["directedLinkTransitions"] == 4
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert route["touchInjectedReferenceStrokes"] == 4
    execution = native["nativeExecution"]
    assert execution["terminalSuccessCases"] == 2
    assert len(execution["terminalCases"]) == 2 and all(r["status"] == 0 for r in execution["terminalCases"])
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    receipts = load(L / "execution-528-validation-receipts.json")
    latest = {row["check"]: row for row in receipts}
    assert len(latest) == 6 and all(row["exitCode"] == 0 for row in latest.values())
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-528-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    limits = (
        "Two blind initial textual families plus original-session dependent visual confirmations retained, "
        "not fresh upstream retrieval/native-speaker certification. All reviewer processes/internal tools serial/exited. "
        "Each visual reviewer received24uniquePNGgroups/43originals/19exact-bytealiases; "
        "source1080x2400/toolreturned900x2000 preserved. All27Han/fourproductionfamilies/focused冖几冗元兄見口目/"
        "wholeword冗談 readable in bounded captures; fallbackface/phone unknown. "
        "078-C1resolved: literal polite negative versus conversational rejection; unsupported polite-remedy extension withdrawn. "
        "Optional glossary/citation/stroke-label and transientloadingtree observations retained. "
        "HOST5243+1/no skips/native526two namedterminal0 retained, hashes/provenance reverified, not rerun. "
        "Full signed7fb6c463archive productionContentSyncONCE1090kanji5046words110N1/problems0/epoch1. "
        "Full+Liteジョウ/emptykun; soleじょうGood/Done1of1; all2mappedpairs4directions/SystemBack/offline. "
        "Actual meaning choices were stackmates NOT authored元兄見; no newlypersisted meaninggrade claimed. "
        "Four reference-touchstrokes/ungradedtrace/giveuprecallAgain NOT humanhandwriting/successfulrecall/MLKit/download. "
        "Fresh vocabulary consistency2122/2431 reviewedpilotprompts, not full coverage. "
        "Historicalsource/review/process/denial/OOM/lookup/readdepthlimitations and reviewed虎/猿/丘/山exceptions remain. "
        "New reviewed冗談/ユーモア directguard additive; ZEROnew078wordarticle. "
        "HOST-only2GiBinit NEVER enters native; no runtime/app/tool/heap/guard/permission/algorithm changes or079. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Bounded owner testing only."
    )
    result = load(S / "batch-078-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh main already ancestral; no substantive teaching/tool integration changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(native["archivedArtifacts"]),
        visualArtifactHashesReverified=len(record527["artifacts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        historicalProcessDeviationsPreserved=True,
        textualReconciliationSha256=sha(V / "batch-078-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-078-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-524.json"), nativeEvidenceSha256=sha(S / "execution-526.json"),
        limits=limits,
    )
    save(S / "batch-078-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1",
                 C / "verify-execution-528.ps1", C / "post-execution-528.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-528.json", {
        "schemaVersion": 1, **p["execution528StartingState"], "recordedAt": now(),
        "status": result["status"], "acceptanceRecord": "batch-078-acceptance-audit.json",
        "publishedAdditions": 104, "remainingAdditions": 1124, "localReviewClosedAdditions": 105,
        "limits": limits, "nextAction": "Normal signed acceptance, owner fast-forward, exact green CI/public ZIP then terminal evidence/owner issue60; yield before079.",
    })
    p["stage"] = "batch-078-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined-tree and inherited review/Android/native evidence accepted and archived.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-078-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8360
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-078-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 528, "batch": "078", "membership": ["冗"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": "3fcd4d838a2d5579f9fe72e4875aab2dedcb2d8d",
        "reviewedTeachingSnapshot": TEACHING, "textualClosureSnapshot": TEACHING,
        "freshAndroidSnapshot": "7fb6c46374f2464648130f2473fabcb9137bb7d4",
        "nativeEnvelopeSnapshot": "7fb6c46374f2464648130f2473fabcb9137bb7d4",
        "nativeEvidenceSnapshot": "9ed58b037d40d7506ec9dc14ea4ee2ecb7f110f3",
        "visualClosureSnapshot": START, "latestMainIntegrated": BASE,
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-078-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-078-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 105, "remainingAdditions": 1123,
            "currentKanji": 1090, "currentWords": 5046, "n1Labelled": 110, "namedSourceMembersPresent": 109,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 0,
            "projectNewNecessarySupportWords": 104, "batchChangedReusedArticles": 2,
            "allMappedReciprocalPairs": 2, "activatedBaselinePairs": 1,
        },
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/owner issue60; checkpoint and yield before079.",
    }
    assert not (S / "batch-078-publication.json").exists()
    save(S / "batch-078-publication.json", publication)
    ledger = load(S / "batch-078-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "nextGate", "limits", "remainingGates")
        if key in ledger}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=105, remainingAdditions=1123, publishedCommit=head,
        publicationRecord="batch-078-publication.json", acceptanceRecord="batch-078-acceptance-audit.json",
        remainingGates="Terminal evidence publication/CI/public ZIP/owner issue update; physicalphone/generalrelease/whole-set outstanding.",
        nextAction=publication["nextAction"], nextGate="Terminal publication receipts and owner issue update, then yield before079.",
        limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-078-progress.json", ledger)
    execution = load(S / "execution-528.json")
    execution.update(status=publication["status"], publishedAdditions=105, remainingAdditions=1123,
                     publicationRecord="batch-078-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-528.json", execution)
    for path in (C / "artifacts" / "batch-078-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-528-accepted-push.txt", Path(__file__)):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-078-accepted-publication-verified-pending-terminal-evidence"
    p["execution528AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/green CI/public8360hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-078-publication.json")
    body = f"""**Batch 078 (冗) is published and verified for bounded owner testing.** Existing **冗談 (じょうだん)** supplies the sole **ジョウ** reading; its N3 vocabulary level and primary reading are preserved. **Zero new word articles.** Both mapped reciprocal pairs /four directions (including older 談) and the activated baseline pair are complete. Additive direct 冗談/ユーモア quiz safeguard preserves prior guards without treating them as transitive.

Authored `{publication['authoredSnapshot']}`; textually corrected/review-closed `{TEACHING}`; fresh Android/native envelope `{publication['nativeEnvelopeSnapshot']}`; native evidence `{publication['nativeEvidenceSnapshot']}`; visual closure `{START}`. Fresh main `{BASE}` already ancestral: no substantive teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not full coverage), fresh manifest `{VERSION}`, five frozen inputs and **78 distinct complete JMdict families /79 occurrences** (47 lexical/26 comparison/6 related), six raw character records. Exact **105 additions** and original **985kanji /4,942words /985strokes** baseline preserved with recorded reviewed metadata exceptions. Sole reading disposition, pinned four-stroke geometry, both mapped pairs/four directions, all27actual scoped Han cmaps and **8,360 runtime hashes** reverified. Raw/full/curated **ジョウ**, empty kun, offered **じょう** retain source order.

Blind initial **claude-opus-5.5 /gpt-6.1-sol**, same frozen snapshot and complete source packet, covered new 冗, complete reused 冗談 and changed 談 passage across all three facets. All initial/confirmation processes/internal reads serial. Minor **078-C1 resolved**: qualify literal polite negative and separately document conversational 冗談じゃない rejection. Unsupported extension of colloquial evidence to a polite remedy withdrawn. No consequential unresolved scoped teaching defect; optional suggestions retained.

Dependent original-session visual527 confirmations: both processes exited serially, internally serial, each complete common source/fixture packet plus **24uniquePNGgroups /43originals /19exact-bytealiases**. Actual model-visible payloads **900x2000**, NOT original1080x2400; returned bytes preserved. All27Han/four production families/focused冖几冗元兄見口目/wholeword冗談 readable in bounded captures. No actionable teaching/rendering defect established. Actual fallback face unknown; physical-phone rendering unverified. Optional glossary/citation/stroke-label observations and final transient loading-tree limitations preserved. Hashes/access do not prove comprehension or every viewport.

Accepted524 **RealContentTest3 +RareHanTest1, no skips**, and526 native attempt1 **two named terminal-status-0 cases**, hashes/provenance reverified, not rerun. Production **ContentSync ONCE** imports complete signed7fb6c463 envelope: **1,090kanji /5,046words /110N1**, problems0, epoch1. Full/Lite raw and curatedジョウ/emptykun agree; soleじょう persistsGood/Done1of1. All2mappedpairs4directions/SystemBack/offline/N1selection/meaningfeedback/four reference-touch strokes/ungradedtrace then give-up recallAgain pass. Actual meaning choices were stackmates, NOT newly exercised authored元兄見; **no newly persisted meaning grade claimed**. No human handwriting/MLKit/successful recall/model download/reviewer gestures or restart durability claimed. Owned5580parent27716/QEMU11132 stopped; shared5556 untouched. Historical denials/failures/OOMs retained; HOST-only2GiBinit NEVER used for native; no production/guest heap, guard, permission or algorithm changes.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,360runtime hash**, exact manifest, safe paths/per-file limits and contributor evidence exclusion. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']}entries /{archive['compressedBytes']}compressed /{archive['inflatedBytes']}inflated /{archive['retainedBytes']}retained bytes**, all original **18,000entries /42compressed /80inflated /56retained MiB** guards unchanged.

Published **105/1,228 additions;1,123 remain**. Current **1,090kanji /5,046words /110N1-labelled /109named-source members plus separate妖**. The104necessary support articles are **not N1 vocabulary expansion**. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**.

Durable `docs/n1-sources/batch-078-publication.json`, `batch-078-acceptance-audit.json`, `execution-528.json`, updated authoring notes and complete original source/review/native records retained. Exact terminal receipts in control. Checkpoint528 **continue**; yield before one bounded079source-preparation checkpoint. Overall project incomplete.
"""
    path = L / "issue-528-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue body prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "progress-before-execution-528.json")
    assert original["checkpoint"] == 527
    receipt = load(L / "issue-528-verified.json")
    expected_body = (L / "issue-528-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected_body.replace("\r\n", "\n").rstrip()
    publication = load(S / "batch-078-publication.json")
    next_action = (
        f"Batch078 fully published/terminal CI/public ZIP/owner issue verified at {head}; yield before079. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/fresh main, then ONE evidence-bounded079source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Use committed source packets and approved workspace inputs; reusable helpers belong in control. "
        "Optional prior-session recipes are NOT required evidence; do not request/access historical session-state paths. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 plus冗談 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every newHan font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewedpush/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on actualnewdenials. "
        "Published105/1228,remaining1123;1090kanji5046words110N1labels109namedmembers plus妖;104necessarysupports NOTN1vocabulary. "
        "Inherit523textualclosure078-C1resolved/unsupportedpoliteremedywithdrawn,524HOST3+1zeroskips,526native2terminal0,"
        "527boundedvisualclosure; no redundantheavywork absentnewconcern. Each visualreviewer24uniquePNGgroups/43originals/"
        "19exact-bytealiases;900x2000returned vs1080x2400source;all27Han/fourfamilies/冗談 readable,fallbackface unknown. "
        "Actualmeaningstackmates NOT authored元兄見; no newlypersisted meaninggrade claimed. Fourreference-touchstrokes/"
        "ungradedtrace/giveuprecallAgain NOT humanhandwriting/successfulrecall/MLKit. SoleじょうGood/Done1,emptykun. "
        "Preserve all originalsource/review/process/denial/OOM/lookup/readdepth/loadingtree/phone limits and FULLlivehistory. "
        "HOST-only2GiBinit NEVER enters nativebuilds; no app/guestheap/archiveguard changes. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=528, status="continue", stage="batch-078-published-verified-before-079",
             lastPublishedCommit=head, remainingAdditions=1123, blocker=None, nextAction=next_action)
    p["batch078PublicationCheckpoint"] = publication
    p["execution528StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1123source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 528, "checkpoint": 528, "batch": "078",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8360,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "originalRootKeyCountCompared": len(original),
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 105, "remainingAdditions": 1123, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "verifiedAt": now(), "nextAction": next_action, "status": "continue",
    }
    save(L / "execution-528-final-verification.json", result)
    save(L / "batch-078-publication-checkpoint.json", publication)
    p["execution528CoordinatorCheckpoint"] = result
    p["batch078PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({key: result[key] for key in (
        "checkpoint", "savedCommit", "issueUpdate", "publishedAdditions", "remainingAdditions",
        "allOriginalHistoricalRootKeysPreservedExactly", "wholeProjectComplete")}, indent=2))


def validate():
    unchanged()
    assert git("rev-parse", "HEAD") == START
    target = L / "execution-528-validation-receipts.json"
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
        path = L / f"execution-528-{name}{suffix}.txt"
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


if __name__ == "__main__":
    {"start": start, "validate": validate, "source-audit": source_audit, "evidence": evidence,
     "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
