"""Bounded batch 079 acceptance, publication and durable checkpoint."""
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
L = C / "logs" / "d2164d7e-cfd0-4e75-b0a2-a93e8f2235ed"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-079-acceptance"
BASE = "2a6777503de6c23c2ac5582b0265dd68d224f44c"
START = "5a706e6521c2b7e04f0ce2d526724dd45dbe660d"
TEACHING = "0f7f20e93b1e20cbc9943011e9ac69b20f75086e"
VERSION = "a01eb85b17601ac0"
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
    temporary = path.with_suffix(path.suffix + ".execution536.tmp")
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


def start():
    unchanged()
    assert git("rev-parse", "HEAD") == START and git("rev-parse", "origin/main") == BASE
    assert not git("status", "--porcelain")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 535 and p["batch"] == "079" and p["status"] == "continue"
    assert "execution536StartingState" not in p
    save(L / "progress-before-execution-536.json", p)
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p["execution536StartingState"] = {
        "execution": 536, "batch": "079", "startingHead": START, "freshOriginMain": BASE,
        "recordedAt": now(), "status": "combined-tree-acceptance-in-progress",
        "scope": "SAME079 combined-current-main acceptance/publication only, then yield; no080 or second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, final535, complete issue and durable path preflight directly inspected. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated worktrees clean; normal signatures G. Fresh main already ancestral; no merge needed. Canonical repositories not accessed.",
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    p["stage"] = "batch-079-combined-tree-acceptance-in-progress"
    save(C / "progress.json", p)
    print("Starting scope saved; full history preserved.")


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
    ledger = load(S / "batch-079-progress.json")
    result = audit(R, "079")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison", "related"):
        selection = load(S / f"batch-079-{kind}-selection.json")
        selected = set(selection["entryIds"])
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("冠" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else e.findtext("ent_seq") in selected)]
        name = "batch-079-jmdict.xml" if kind == "lexical" else f"batch-079-{kind}-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [158, 18, 1] and len(distinct) == 177
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-079-kanjidic2.xml").getroot()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 5
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-078-acceptance-source-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 79 and not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 79:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 106 and old_chars <= current
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
    assert sum(maps.values()) == 8363
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 3
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-079-stroke-evidence.json")
    svg_path = Path(geometry["input"])
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "冠.json") == convert("冠", svg.decode("utf-8"))
    font_audit = load(S / "batch-079-draft-font-audit.json")
    articles = font_audit["completeRuntimeScope"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == sorted(font_audit["actualHan"]) and len(han) == 35
    fonts = []
    for row in font_audit["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["allActualMissing"] == ["冖", "宀"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1091, "words": 5047, "n1Labelled": 111, "namedSourceMembersPresent": 110}
    result.update(
        execution=536, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        exactFrozenDistinctDictionaryFamilies=len(distinct), dictionaryFamilyOccurrences=177,
        dictionaryPackets=packets, completeRawCharacterRecordsVerified=5,
        runtimePayloadHashesVerified=8363, manifestMaps=maps, allMappedReciprocalPairs=3,
        mappedDirectedLinks=6, actualCounts=actual_counts,
        actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Mechanical source/family/baseline/membership/readings/quiz/link/geometry/cmap/manifest/budget audit, not fresh linguistic or native review. Comparison/related selections retained from reviewed committed packets.",
    )
    save(S / "batch-079-acceptance-source-audit.json", result)
    print("177families/5rawrecords/baseline/106additions/8363hashes/3pairs/geometry/cmaps/budgets passed.")


def validate():
    unchanged()
    receipts = []
    target = L / "execution-536-validation-receipts.json"
    assert not target.exists()
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-536-{name}.txt"
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
    textual = load(V / "batch-079-reconciliation.json")
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
    visual = load(V / "batch-079-visual-reconciliation.json")
    record535 = load(S / "execution-535.json")
    assert sha(V / "batch-079-visual-reconciliation.json") == record535["reconciliationSha256"]
    assert visual["processReconciliation"]["bothAcceptedExecutionsInternallySerial"]
    assert not visual["findings"] and visual["actionableRemainingFindings"] == 0
    assert visual["consequentialUnresolvedScopedTeachingClaims"] == 0
    assert record535["bothAcceptedOriginalFamilyExecutionsSerialAndExited"]
    assert record535["bothAcceptedVisualExecutionsInternallySerial"]
    visual_processes = list(record535["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["imagePayloadsVerified"] == 29
        assert row["completeSourcePacketReturned"]
        assert row["observedToolOverlaps"] == row["multiToolResponses"] == 0
    assert [r["actualModels"] for r in visual_processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    for row in record535["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    android = load(S / "execution-532.json")
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
        assert sha(R / row["archivedPath"]) == row["sha256"]
    for row in android["testImplementationsAndHostInit"]:
        assert sha(Path(row["path"])) == row["sha256"]
    native = load(S / "execution-534.json")
    for row in native["archivedReceipts"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "originalBytesPreservedIn" in row:
            original = gzip.decompress((R / row["originalBytesPreservedIn"]).read_bytes())
            assert original
    raw = V / "batch-079-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-079-native" / "attempt-1" / "n1-079-article-route.json")
    assert route == native["articleRoute"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1091, 5047, 111, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    for suffix, values in (("Onyomi", ["カン"]), ("Kunyomi", ["かんむり"])):
        assert route["full" + suffix] == route["fullProjection" + suffix] == values
        assert route["fullProjectionQuiz" + suffix] == route["liteQuiz" + suffix] == values
    assert route["quizOnKeys"] == ["かん"] and route["quizKunKeys"] == ["かんむり"]
    assert route["bothCuratedKindsPersistedGoodAndDone"]
    assert route["mappedReciprocalPairs"] == 3 and route["directedLinkTransitions"] == 6
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert route["touchInjectedReferenceStrokes"] == 9 and route["drawingGradeRecordedOnNext"]
    execution = native["nativeExecution"]
    assert execution["terminalSuccessCases"] == 2
    assert len(execution["terminalCases"]) == 2 and all(r["status"] == 0 for r in execution["terminalCases"])
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    receipts = load(L / "execution-536-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-536-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    limits = (
        "Two blind initial textual model families and original-session confirmations retained; "
        "177 complete families/five raw records, N2 and bottle-closure naming evidence gaps resolved, no teaching edits. "
        "Dependent visual ClaudeOpus5.5/GPT6.1Sol accepted serial/exited, each29uniquePNGgroups/57originals/28aliases; "
        "original1080x2400 versus returned900x2000. Rejected Claude25overlaps/two multitoool responses remains rejected; "
        "finite31turn serial replay accepted, resources1-17 ownsummary/live18-30 explicit. "
        "All35Han/fourfamilies/exact冖宀 readable in bounded captures, actual fallbackface unknown. "
        "Complementary horizontal reading-table states, not allcolumns oneframe. "
        "HOST5323+1/no skips/native534two namedterminal0 reverified without rerun. Fullsigned3fdc0bf9 archive "
        "productionContentSyncONCE1091kanji5047words111N1/problems0/epoch1. Bothカンかんむり/rawFullLite/keysかんかんむり "
        "new grade3 logs/Done2of2, threepairs/sixdirections/SystemBack/offline. Actualmeaningchoices exempt/superfluous/frugal "
        "NOT full authored冗完守 trio; no newlypersisted meaninggrade claim. Nine injectedreferencepaths/ungradedtrace/"
        "shape-onlycomparison/giveuprecallgrade1 NOT humanhandwriting/successfulrecall/MLKit/modeldownload. "
        "140individual+8wholeword Paint assertion/hashrecords NOT148PNGreads. Finaltree transientloading "
        "NOT loadedpersistenceproof. Freshvocabulary2122/2431 pilotprompts NOT fullcoverage. Historicalsource/review/"
        "process/denial/OOM/readdepth/lookup/phone limits and reviewedbaseline exceptions preserved. HOST-only2GiBinit "
        "NEVER native; no production/guestheap/guard/permission/algorithm changes. CompatibleAndroidf9b59a2+ required; "
        "physicalphone/generalrelease/whole-set outstanding. Boundedowner testing only."
    )
    result = load(S / "batch-079-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh main already ancestral; no teaching/tool integration changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(native["archivedReceipts"]),
        visualArtifactHashesReverified=len(record535["artifacts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        rejectedOriginalClaudeVisualProcessPreserved=True,
        textualReconciliationSha256=sha(V / "batch-079-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-079-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-532.json"), nativeEvidenceSha256=sha(S / "execution-534.json"),
        limits=limits,
    )
    save(S / "batch-079-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1",
                 C / "verify-execution-536.ps1", C / "post-execution-536.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-536.json", {
        "schemaVersion": 1, **p["execution536StartingState"], "recordedAt": now(),
        "status": result["status"], "acceptanceRecord": "batch-079-acceptance-audit.json",
        "publishedAdditions": 105, "remainingAdditions": 1123, "localReviewClosedAdditions": 106,
        "limits": limits, "nextAction": "Normal signed acceptance, ownerfastforward, exactgreenCI/publicZIP, terminalevidence/ownerissue60; yield before080.",
    })
    p["stage"] = "batch-079-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined-tree and inherited reviewer/HOST/native evidence accepted.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-079-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8363
    assert all(archive[k] for k in ("manifestEqual", "allPublishingBudgetsPassed",
                                  "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-079-acceptance-audit.json")
    p = load(C / "progress.json")
    publication = {
        "schemaVersion": 1, "execution": 536, "batch": "079", "membership": ["冠"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "084d5301d175189d6e83aa77666ae495abed6f47",
        "freshAndroidSnapshot": "3fdc0bf952e299060b5a07ac372bb6d926595a4c",
        "nativeEnvelopeSnapshot": "3fdc0bf952e299060b5a07ac372bb6d926595a4c",
        "nativeEvidenceSnapshot": "dcfcbb43b30b63beef3f689d3ebae4e412c9120c",
        "visualClosureSnapshot": START, "latestMainIntegrated": BASE,
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-079-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-079-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 106, "remainingAdditions": 1122,
            "currentKanji": 1091, "currentWords": 5047, "n1Labelled": 111, "namedSourceMembersPresent": 110,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 105, "batchChangedReusedArticles": 2,
            "allMappedReciprocalPairs": 3, "activatedBaselinePairs": 1,
        },
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/publicZIP/ownerissue60; checkpoint and yield before080.",
    }
    assert not (S / "batch-079-publication.json").exists()
    save(S / "batch-079-publication.json", publication)
    ledger = load(S / "batch-079-progress.json")
    ledger["prePublicationCheckpoint"] = {
        k: copy.deepcopy(ledger[k]) for k in ("status", "nextAction", "nextGate", "limits") if k in ledger}
    ledger.update(status=publication["status"], published=ledger["membership"],
                  publishedAdditions=106, remainingAdditions=1122, publishedCommit=head,
                  publicationRecord="batch-079-publication.json", acceptanceRecord="batch-079-acceptance-audit.json",
                  nextAction=publication["nextAction"], nextGate="Terminalreceipts/ownerissue, then yield before080.",
                  limits=publication["limits"])
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-079-progress.json", ledger)
    execution = load(S / "execution-536.json")
    execution.update(status=publication["status"], publishedAdditions=106, remainingAdditions=1122,
                     publicationRecord="batch-079-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-536.json", execution)
    for path in (C / "artifacts" / "batch-079-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-536-accepted-push.txt"):
        shutil.copyfile(path, D / path.name)
    p["stage"] = "batch-079-accepted-publication-verified-pending-terminal-evidence"
    p["execution536AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted publication verified; terminal durable records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-079-publication.json")
    acceptance = publication["validation"]
    body = f"""**Batch 079 (冠) is published and verified for bounded owner testing**, with necessary **王冠 (おうかん)** and reused **冠 (かんむり)**. Both full/curated readings カン /かんむり retain source order; offered keys かん /かんむり. Existing 冠 N2 identity/primary reading/eight exclusions preserved; new 王冠 has no inferred vocabulary level. Three mapped reciprocal pairs/six directions include older 王.

Authored/reviewed `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`; fresh HOST/native envelope `{publication['nativeEnvelopeSnapshot']}`; native evidence `{publication['nativeEvidenceSnapshot']}`; visual closure `{START}`. Fresh main `{BASE}` already ancestral, no teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Owner-scoped normal fast-forwards; global romanko-ms unchanged.

Fresh combined checks: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not full coverage), manifest `{VERSION}`, five frozen inputs/two decompressed dictionaries, **177 complete distinct JMdict families** (158 lexical/18 comparison/one related), five complete raw character records, original **985kanji/4,942words/985strokes** baseline and documented exceptions, exact **106 additions**, all reading dispositions/quiz mappings/three pairs, nine-stroke pinned geometry, all35 scoped Han cmaps, **8,363 runtime hashes** and original budgets.

Two blind initial model families **claude-opus-5.5 /gpt-6.1-sol** and original-session confirmations retained; source gaps 079-C1/G1 resolved by exact N2:363 and Daijisen bottle-cap naming evidence, no teaching errors/edits. Dependent visual confirmations accepted serial/exited: same packet plus **29uniquePNGgroups/57originals/28aliases each**, original1080x2400 versus returned900x2000. Initial Claude visual execution remains rejected (25overlaps/two multitoolresponses); one finite31turn serial replay accepted, resources1-17 ownsummary/live18-30 explicit. GPT subsequently serial. All four assigned teaching scopes CLEAN within bounded facets; no consequential unresolved teaching defect. Full original reports/returned payloads/process/read-depth limits retained, not native-speaker certification.

Accepted HOST532 **RealContentTest3 +RareHanTest1/no skips** and native534 **two named terminal-status-0 cases** reverified, not rerun. Production **ContentSync ONCE**, full signed3fdc0bf9 archive: **1,091kanji/5,047words/111N1/problems0/epoch1**. Full/Lite raw/curated readings agree; two new grade3 reading logs/Done2of2, threepairs/sixdirections/SystemBack/offline/N1selection. All35Han/fourproductionfamilies/exact冖宀 readable in bounded captures; fallbackface unknown. Horizontal reading-table states are complementary, not allcolumns in oneframe. Actual meaning choices exempt/superfluous/frugal NOT all authored冗完守; no newlypersisted meaninggrade claim. Nine injectedreferencepaths/ungradedtrace/shape-onlycomparison/giveuprecallgrade1 NOT humanhandwriting/successfulrecall/MLKit/modeldownload. 140individual+8wholeword nativePaint assertion/hashrecords NOT148PNGreads; terminaltree transientloading NOT loadedpersistenceproof. Owned5580parent2004/qemu6712 stopped; shared5556 untouched. HOST-only2GiBinit NEVER native; original source/review/denial/OOM/baseline limits preserved.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs preserve every8,363runtime hash**, exactmanifest/safepaths/per-filelimits/contributor-evidence exclusion. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']}entries/{archive['compressedBytes']}compressed/{archive['inflatedBytes']}inflated/{archive['retainedBytes']}retained bytes**, unchanged **18,000entries/42compressed/80inflated/56retained MiB** guards.

Published **106/1,228 additions;1,122 remain**. Current **1,091kanji/5,047words/111N1labels/110named-source members plus separate妖**; **105 necessary support additions, not N1 vocabulary expansion**. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required. **Physical-phone/general-release/whole-set acceptance outstanding.**

Durable `docs/n1-sources/batch-079-publication.json`, `batch-079-acceptance-audit.json`, `execution-536.json`, updated authoring notes and original evidence retained. Checkpoint536 continue, yield before one bounded080 source-preparation checkpoint. Optional historical session recipes not accessed, no new permission denial, no080 or secondrunner. Overall project incomplete.
"""
    path = L / "issue-536-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact owner issue publication body prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "progress-before-execution-536.json")
    receipt = load(L / "issue-536-verified.json")
    expected = (L / "issue-536-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n") == expected.replace("\r\n", "\n")
    assert not (S / "batch-080-progress.json").exists()
    publication = load(S / "batch-079-publication.json")
    next_action = (
        f"Batch079 published/terminalgreenCI/everypublicZIPhash/ownerissue verified at {head}; yield before080. "
        "NEXT freshcoordinator read entire request/finalcheckpoint/scopedlivekeys and preserve FULLhistory. "
        "Verify dedicatedclean signedheads/freshmain, then ONE evidence-bounded080 SOURCE-PREPARATION checkpoint below15 "
        "from exactremaining frozen rows ONLY, no runtime draft/latergates in sourcecheckpoint. "
        "Use committedsourcepackets/approvedworkspaceinputs/durablecontrolhelpers, NOT optional historicalsession recipes. "
        "Preserve fullsource/baseline identities/levels/readings/order/exclusions and documented虎/猿/丘/山/冗談 exceptions; "
        "inspect complete applicablefamilies/actualnecessarysupport/everyreadingdisposition/curatedrow/"
        "allactivated+reciprocalpairs/pinnedstrokes/allnewHanfonts. Later twoSERIALblinddifferentfamilyreviews/"
        "serialinternaltools/boundedoriginalconfirmations/nonskippedAndroid/native/currentmain/normalsigning/"
        "ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets mandatory. No unreviewedpush/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield actualnewdenials. "
        "Published106/1228,remaining1122;1091kanji5047words111N1labels110namedmembers plus separate妖;105necessarysupports "
        "NOT N1vocabulary. Inherit531textualclosure/noedit/N2:363/bottlecapnaming,532HOST3+1noskips,534native2terminal0,"
        "535boundedvisualclosure with rejectedClaude25overlaps preserved and finite31serialturnreplay accepted/"
        "ownsummary1-17live18-30; GPTserial. Each29uniquePNGgroups/57originals/28aliases,900x2000returned vs1080x2400source. "
        "All35Han/fourfamilies/exact冖宀 readable/fallbackface unknown; complementaryhorizontalreadingtable "
        "notallcolumnsoneframe. Meaningexempt/superfluous/frugal NOT authoredfull冗完守/no newmeaninggradeclaim. "
        "Bothreadinggrade3/Done2of2,3pairs6directions/offline/SystemBack. Nineinjectedreferencepaths/ungradedtrace/"
        "shapeonly/giveuprecallgrade1 NOT humanhandwriting/successfulrecall/MLKit/download;140+8Paintrecords NOT148PNGreads. "
        "Finaltreetransientloading NOT loadedpersistenceproof. Preserve all originalsource/review/process/denial/OOM/"
        "lookup/readdepth/phone limits and FULLlivehistory. HOST-only2GiBinit NEVERnative; noapp/guestheap/guardchanges. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=536, status="continue", stage="batch-079-published-verified-before-080",
             lastPublishedCommit=head, remainingAdditions=1122, blocker=None, nextAction=next_action)
    p["batch079PublicationCheckpoint"] = publication
    p["execution536StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1122 source-bounded additions not authored/review-closed/published; later batches retain all original source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 536, "checkpoint": 536, "batch": "079",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8363,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "originalRootKeyCountCompared": len(original),
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 106, "remainingAdditions": 1122, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "verifiedAt": now(), "nextAction": next_action, "status": "continue",
    }
    save(L / "execution-536-final-verification.json", result)
    save(L / "batch-079-publication-checkpoint.json", publication)
    p["execution536CoordinatorCheckpoint"] = result
    p["batch079PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({k: result[k] for k in ("checkpoint", "savedCommit", "issueUpdate",
          "publishedAdditions", "remainingAdditions", "allOriginalHistoricalRootKeysPreservedExactly",
          "wholeProjectComplete")}, indent=2))


if __name__ == "__main__":
    {"start": start, "validate": validate, "source-audit": source_audit, "evidence": evidence,
     "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
