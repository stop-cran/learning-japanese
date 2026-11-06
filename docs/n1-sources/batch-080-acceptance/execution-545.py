"""Batch 080 combined-tree acceptance and publication checkpoint."""
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
L = C / "logs" / "33aee530-af6e-4883-bc14-6cce8447a767"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-080-acceptance"
BASE = "b120125ae5cdbfe9f3bcb1b0a7ae8a61e422ec8d"
START = "ac3350642c3888ad3af8cd31ba4d2619e70da52a"
TEACHING = "3f883347e81422abce490ee633e874be55ef01ad"
VERSION = "4572f7b1d0d95059"
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
    temporary = path.with_suffix(path.suffix + ".execution545.tmp")
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
    unchanged()
    assert git("rev-parse", "HEAD") == START and git("rev-parse", "origin/main") == BASE
    assert not git("status", "--porcelain")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 544 and p["batch"] == "080" and p["status"] == "continue"
    assert "execution545StartingState" not in p
    assert not (L / "progress-before-execution-545.json").exists()
    save(L / "progress-before-execution-545.json", p)
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    json.loads(request.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p["execution545StartingState"] = {
        "execution": 545, "batch": "080", "startingHead": START, "freshOriginMain": BASE,
        "recordedAt": now(), "status": "combined-tree-acceptance-in-progress",
        "scope": "SAME080 combined-current-main acceptance/publication only; yield before081, no second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, final544, complete issue and durable path preflight inspected. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated worktrees clean; normally signed content. Fresh main already ancestral; no merge needed. Canonical repositories not accessed.",
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    p["stage"] = "batch-080-combined-tree-acceptance-in-progress"
    save(C / "progress.json", p)
    print("Starting scope persisted with complete live history.")


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
    ledger = load(S / "batch-080-progress.json")
    result = audit(R, "080")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison", "related", "hypothesis"):
        selection = load(S / f"batch-080-{kind}-selection.json")
        selected = set(selection["entryIds"])
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("冴" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else e.findtext("ent_seq") in selected)]
        name = "batch-080-jmdict.xml" if kind == "lexical" else f"batch-080-{kind}-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        if kind != "hypothesis":
            distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [16, 12, 8, 2] and len(distinct) == 35
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-080-kanjidic2.xml").getroot()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 4
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-079-acceptance-source-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 80 and not expected & set(row["membership"])
        if int(row["batch"]) < 80:
            assert row["reviewClosed"] == row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 107 and old_chars <= current
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
    assert sum(maps.values()) == 8366
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 1
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-080-stroke-evidence.json")
    svg_path = Path(geometry["input"])
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "冴.json") == convert("冴", svg.decode("utf-8"))
    font_audit = load(S / "batch-080-draft-font-audit.json")
    articles = font_audit["completeRuntimeScope"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == sorted(font_audit["actualHan"]) and len(han) == 30
    fonts = []
    for row in font_audit["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["allActualMissing"] == ["冫", "冱", "氵"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1092, "words": 5048, "n1Labelled": 112, "namedSourceMembersPresent": 111}
    result.update(
        execution=545, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        exactFrozenInitialDistinctDictionaryFamilies=len(distinct), initialDictionaryFamilyOccurrences=36,
        supplementalHypothesisFamilies=2, dictionaryPackets=packets, completeRawCharacterRecordsVerified=4,
        runtimePayloadHashesVerified=8366, manifestMaps=maps, allMappedReciprocalPairs=1,
        mappedDirectedLinks=2, actualCounts=actual_counts,
        actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Mechanical source/family/baseline/membership/readings/quiz/link/geometry/cmap/manifest/budget audit, not fresh linguistic/native review. Reviewed full dictionaries and source-only qualifications retained; cmap absence is not a glyph failure.",
    )
    save(S / "batch-080-acceptance-source-audit.json", result)
    print("Source/families/baseline/107 additions/8366 hashes/links/geometry/cmaps/budgets passed.")


def validate():
    unchanged()
    receipts = []
    target = L / "execution-545-validation-receipts.json"
    assert not target.exists()
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-545-{name}.txt"
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
    textual = load(V / "batch-080-reconciliation.json")
    assert sha(V / "batch-080-reconciliation.json") == load(S / "execution-539.json")["reconciliationSha256"]
    assert textual["textualReviewClosed"] and textual["actionableRemainingFindings"] == 0
    assert textual["consequentialUnresolvedTeachingFindings"] == 0 and not textual["findings"]
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["allInitialAndSupplementInternalToolsSerial"]
    processes = list(textual["processes"].values())
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]] and row["snapshot"] == TEACHING
        execution = load(V / row["execution"])
        assert sha(V / row["report"]) == row["reportSha256"] == execution["reportSha256"]
        assert sha(V / Path(row["report"]).with_suffix(".jsonl")) == row["rawExecutionSha256"]
        assert execution["observedToolOverlaps"] == execution["unfinishedTools"] == []
        assert execution["multiToolResponseCount"] == 0 and execution["exitCode"] == 0
        assert execution["actualModels"] == [row["requestedModel"]]
        assert load(V / row["coverage"])["allAssignedRangesReturned"]
    for first, second in zip(processes, processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    visual = load(V / "batch-080-visual-reconciliation.json")
    record544 = load(S / "execution-544.json")
    assert sha(V / "batch-080-visual-reconciliation.json") == record544["reconciliationSha256"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedScopedTeachingFindings"] == 0
    assert visual["process"]["oneReviewerFamilyActiveAtATime"]
    assert visual["process"]["allChildrenExitedBeforeNext"]
    assert visual["process"]["observedToolOverlaps"] == visual["process"]["multiToolResponses"] == 0
    visual_processes = list(record544["reviews"].values())
    assert [r["actualModels"] for r in visual_processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
    assert datetime.fromisoformat(visual_processes[0]["completedAt"]) < datetime.fromisoformat(visual_processes[1]["startedAt"])
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["serialChildProcesses"] == 28
        assert row["completePackets"] == 1 and row["distinctImages"] == 26
    for row in record544["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"], row["path"]
    android = load(S / "execution-540.json")
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
    native = load(S / "execution-543.json")
    for row in native["archivedReceipts"]:
        assert sha(R / row["path"]) == row["sha256"]
        if "compressedRaw" in row:
            assert sha(R / row["compressedRaw"]) == row["compressedRawSha256"]
            original = gzip.decompress((R / row["compressedRaw"]).read_bytes())
            assert hashlib.sha256(original).hexdigest() == row["originalSha256"]
    raw = V / "batch-080-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-080-native" / "attempt-1" / "n1-080-article-route.json")
    assert route == native["articleRoute"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1092, 5048, 112, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    for suffix, full, selected in (
        ("Onyomi", ["ゴ", "コ"], []), ("Kunyomi", ["さ.える", "こお.る", "ひ.える"], ["さ.える"])
    ):
        assert route["full" + suffix] == route["fullProjection" + suffix] == full
        assert route["fullProjectionQuiz" + suffix] == route["liteQuiz" + suffix] == selected
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["さえる"]
    assert route["soleCuratedKunPersistedGoodAndDone"] and route["meaningQuestionAndFeedback"]
    assert route["mappedReciprocalPairs"] == 1 and route["directedLinkTransitions"] == 2
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert route["touchInjectedReferenceStrokes"] == 7 and route["drawingGradeRecordedOnNext"]
    execution = native["nativeExecution"]
    assert execution["terminalSuccessCases"] == 2
    assert len(execution["terminalCases"]) == 2 and all(r["status"] == 0 for r in execution["terminalCases"])
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    index = native["imageIndex"]
    assert index["originalPngCount"] == 49 and index["distinctByteGroups"] == 26
    images = []
    for group in index["groups"]:
        for name in group["originals"]:
            assert sha(raw.parent / name) == group["sha256"]
            images.append(name)
    assert len(images) == len(set(images)) == 49
    receipts = load(L / "execution-545-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-545-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    limits = (
        "Two blind initial textual families plus original-session supplements retained:35 initial distinct families/"
        "36 occurrences,two supplementary families,four raw records,21 comparison bodies. Original Claude counting "
        "imprecision retained; no teaching edit. No consequential unresolved scoped teaching defect; conditional "
        "guards withdrawn and conservative additional guard/wording/citation polish optional. "
        "Dependent original-session ClaudeOpus5.5/GPT6.1Sol visual confirmations serial/exited:each28serialchildren/"
        "onepacket/26distinctPNGgroups covering49originals/23aliases. Source1080x2400 versus returned900x2000, "
        "not source-byte equality. Initial overstrict transport assertion and qualified recovery preserved; "
        "not a permission denial/rejected linguistic finding. Claude summary-only resources1-12 explicit. "
        "All30Han/fourproductionfamilies/readable exact冫冱氵; fallbackface not identified. Complementary "
        "horizontal table states,not allcolumns oneframe or universalUI certification. HOST5403+1/no skips "
        "and native543two namedterminal0 reverified without rerun; fullsigned0d2c9aee archive through production "
        "ContentSyncONCE1092kanji5048words112N1/zeroProblems/epoch1. Full+Lite fullゴコ/さ.えるこお.るひ.える "
        "unchanged; selectedon[]/kun[さ.える],offeredさえる/goodlog/Done1of1. Onepairtwodirections/SystemBack/"
        "offline/N1selection/actualmeaningchoices passed. Finalsemanticstree loading,not settledroute/persistenceproof. "
        "Seven injectedreferencepaths/ungradedtrace/shape-onlycomparison/giveuprecallgrade1 NOT humanhandwriting/"
        "successfulrecall/MLKitrecognition/modeldownload; offline model unavailable. 120individual+4wholewordPaint "
        "assertion/hashrecords NOT124PNGreads. Seededdisposableschedule NOTownerprogress. Owned543emulator5580 "
        "parent11976/qemu1240 stopped; owner5556 untouched. Freshvocabulary2122/2431 pilotprompts NOTfullcoverage. "
        "Historicalsource/lookup/citation/readdepth/review/process/denial/OOM/viewport/phone limitations retained. "
        "HOST-only2GiBinit NEVERnative; noapp/guestheap/archiveguard changes. CompatibleAndroidf9b59a2+ required; "
        "physicalphone/generalrelease/whole-set outstanding. Bounded owner testing only."
    )
    result = load(S / "batch-080-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh main already ancestral; no teaching/tool integration changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(native["archivedReceipts"]),
        visualArtifactHashesReverified=len(record544["artifacts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        textualReconciliationSha256=sha(V / "batch-080-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-080-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-540.json"), nativeEvidenceSha256=sha(S / "execution-543.json"),
        limits=limits,
    )
    save(S / "batch-080-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1",
                 C / "verify-execution-545.ps1", C / "post-execution-545.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-545.json", {
        "schemaVersion": 1, **p["execution545StartingState"], "recordedAt": now(),
        "status": result["status"], "acceptanceRecord": "batch-080-acceptance-audit.json",
        "publishedAdditions": 106, "remainingAdditions": 1122, "localReviewClosedAdditions": 107,
        "limits": limits, "nextAction": "Normal signed acceptance,ownerfastforward,exactgreenCI/publicZIP,terminal evidence/ownerissue60;yield before081.",
    })
    ledger = load(S / "batch-080-progress.json")
    ledger["preAcceptanceCheckpoint"] = {
        k: copy.deepcopy(ledger[k]) for k in ("status", "reviewClosed", "nextAction", "limits")}
    ledger.update(status="review-closed-combined-tree-accepted-pending-publication",
                  reviewClosed=ledger["membership"], acceptanceRecord="batch-080-acceptance-audit.json")
    for row in ledger["supportMappings"]:
        row["status"] = ledger["status"]
    save(S / "batch-080-progress.json", ledger)
    p["stage"] = "batch-080-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined-tree and inherited reviewer/HOST/native evidence accepted.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-080-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8366
    assert all(archive[k] for k in ("manifestEqual", "allPublishingBudgetsPassed",
                                  "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    acceptance = load(S / "batch-080-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 545, "batch": "080", "membership": ["冴"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "df0bab41616b2d8db5c03c2ebfc32aa213a75c80",
        "freshAndroidSnapshot": "0d2c9aee6de9e4f430935b38e31228db4bd47908",
        "nativeEnvelopeSnapshot": "0d2c9aee6de9e4f430935b38e31228db4bd47908",
        "nativeEvidenceSnapshot": "2bfc8456f33d1625509321e1e946f1402d5eb672",
        "visualClosureSnapshot": START, "latestMainIntegrated": BASE,
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-080-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-080-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 107, "remainingAdditions": 1121,
            "currentKanji": 1092, "currentWords": 5048, "n1Labelled": 112, "namedSourceMembersPresent": 111,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 106, "batchChangedReusedArticles": 0,
            "allMappedReciprocalPairs": 1, "activatedBaselinePairs": 0,
        },
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/publicZIP/ownerissue60;checkpoint and yield before081.",
    }
    assert not (S / "batch-080-publication.json").exists()
    save(S / "batch-080-publication.json", publication)
    ledger = load(S / "batch-080-progress.json")
    ledger["prePublicationCheckpoint"] = {
        k: copy.deepcopy(ledger[k]) for k in ("status", "nextAction", "nextGate", "limits") if k in ledger}
    ledger.update(status=publication["status"], published=ledger["membership"],
                  publishedAdditions=107, remainingAdditions=1121, publishedCommit=head,
                  publicationRecord="batch-080-publication.json", acceptanceRecord="batch-080-acceptance-audit.json",
                  nextAction=publication["nextAction"], nextGate="Terminal receipts/ownerissue,then yield before081.",
                  limits=publication["limits"])
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-080-progress.json", ledger)
    execution = load(S / "execution-545.json")
    execution.update(status=publication["status"], publishedAdditions=107, remainingAdditions=1121,
                     publicationRecord="batch-080-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-545.json", execution)
    for path in (C / "artifacts" / "batch-080-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-545-accepted-push.txt"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-080-accepted-publication-verified-pending-terminal-evidence"
    p["execution545AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted publication verified; terminal durable records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-080-publication.json")
    body = f"""**Batch 080 (冴) is published and verified for bounded owner testing**, with necessary **冴える (さえる)**. Full metadata stays **ゴ, コ /さ.える, こお.る, ひ.える** in source order; explicit on practice **[]**, sole selected kun **さ.える**, offered **さえる**. All five dispositions remain visible, including rare recognition-only 冴寒 and qualified source-only rows. No inferred word JLPT level or unrelated reused teaching edits.

Authored/reviewed `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`; HOST/native full-envelope `{publication['nativeEnvelopeSnapshot']}`; native evidence `{publication['nativeEvidenceSnapshot']}`; visual closure `{START}`. Fresh main `{BASE}` already ancestral: no teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined checks: **372 Python tests/no skips**, validator, vocabulary (**2,122/2,431 reviewed pilot prompts**, not full coverage), manifest `{VERSION}`, five frozen inputs/two decompressed dictionaries, **35 initial distinct JMdict families/36 occurrences plus two supplementary families**, four complete raw character records, baseline **985kanji/4,942words/985strokes** with documented exceptions, exact **107 additions**, all readings/quiz safeguards/**one reciprocal pair/two directions**, pinned seven-stroke geometry, all30 scoped Han cmaps, **8,366 runtime hashes** and original budgets.

Two blind textual families **claude-opus-5.5 /gpt-6.1-sol**, original-session supplements and dependent visual confirmations retained; no actionable/consequential unresolved scoped teaching defect. Conditional guard hypotheses withdrawn; additional はっきり guard/wording/citation polish optional, no teaching edit. Visual reviewers ran serially: **28 host-dispatched serial children each**, same complete packet plus **26 distinct PNG groups covering49 originals/23 byte aliases**, zero-tool final report, all exits before next family. Original1080x2400 versus returned900x2000 payloads separately retained. Claude final synthesis uses own compressed summary for resources1-12, not live original pixels. Initial overstrict raw-byte-equality assertion and qualified transport recovery preserved, not permission denial or rejected linguistic evidence. Complete reports/observations/process/source/read-depth limits retained; not native-speaker certification.

Accepted HOST540 **RealContentTest3 +RareHanTest1/no skips** and native543 **two named terminal-status-0 cases** reverified, not rerun. Full signed0d2c9aee archive through production **ContentSync ONCE**: **1,092kanji/5,048words/112N1/zeroProblems/epoch1**. Full/Lite full and curated readings agree; sole new kun good log/**Done1of1**, N1selection/actualmeaningfeedback/onepair/twodirections/SystemBack/offline passed. All30Han/fourproductionfamilies/exact冫冱氵 readable in bounded captures; fallbackface unknown. Complementary horizontal table states, not allcolumns oneframe. Final semanticstree loading, not settledroute/persistenceproof. Seven injectedreferencepaths/ungradedtrace/shape-onlycomparison/giveuprecallgrade1 NOT humanhandwriting/successfulrecall/MLKitrecognition/modeldownload; offline model unavailable. 120individual+4wholewordPaint assertions NOT124PNGreads; seeded disposable schedule not owner progress. Owned5580parent11976/qemu1240 stopped; owner5556 untouched. HOST-only2GiBinit NEVERnative; no app/guestheap/guard changes.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs preserve every8,366runtime hash**, exactmanifest/safepaths/per-filelimits/contributor-evidence exclusion. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']}entries/{archive['compressedBytes']}compressed/{archive['inflatedBytes']}inflated/{archive['retainedBytes']}retained bytes**, unchanged **18,000entries/42compressed/80inflated/56retained MiB** guards.

Published **107/1,228 additions;1,121 remain**. Current **1,092kanji/5,048words/112N1labels/111named-source members plus separate妖**; **106 necessary support additions, not an N1 vocabulary deck**. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required. **Physical-phone/general-release/whole-set acceptance outstanding.**

Durable `docs/n1-sources/batch-080-publication.json`, `batch-080-acceptance-audit.json`, `execution-545.json` and authoring notes preserve exact review/source/native/process/denial/OOM/viewport/phone limitations. Checkpoint545 continue; yield before one bounded081 source-preparation checkpoint. Durablecontrol/committedpackets/approvedinputs only; optional historical session recipes skipped, no new denial, no081 or secondrunner. Overall project incomplete.
"""
    path = L / "issue-545-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact owner issue publication body prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "progress-before-execution-545.json")
    receipt = load(L / "issue-545-verified.json")
    expected = (L / "issue-545-body.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == expected
    assert not (S / "batch-081-progress.json").exists()
    publication = load(S / "batch-080-publication.json")
    next_action = (
        f"Batch080 published/terminalgreenCI/everypublicZIPhash/ownerissue verified at {head}; yield before081. "
        "NEXT freshcoordinator read entire request/finalcheckpoint/scopedlivekeys and preserve FULLhistory. "
        "Verify dedicatedclean signedheads/freshmain,then ONE evidence-bounded081 SOURCE-PREPARATION checkpoint "
        "below15 from exactremaining frozenrows ONLY,no runtime draft/latergates in sourcecheckpoint. "
        "Use committedsourcepackets/approvedworkspaceinputs/durablecontrolhelpers,NOT optional historicalsessionrecipes. "
        "Preserve source/baseline identities/levels/readings/order/exclusions and documented虎/猿/丘/山/冗談 exceptions; "
        "inspect complete applicablefamilies/actualnecessarysupport/everyreadingdisposition/curatedrow/"
        "allactivated+reciprocalpairs/pinnedstrokes/allnewHanfonts. Later twoSERIALblinddifferentfamilyreviews/"
        "serialinternaltools/boundedoriginalconfirmations/nonskippedAndroid/native/currentmain/normalsigning/"
        "ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets mandatory. No unreviewedpush/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield actualnewdenials. "
        "Published107/1228,remaining1121;1092kanji5048words112N1labels111namedmembers plus separate妖;106necessarysupports "
        "NOT N1vocabulary. Inherit539textualclosure/noedit/35initialdistinctfamilies36occurrences+2supplementary/"
        "4rawrecords/21comparisonbodies,540HOST3+1noskips,543native2terminal0,544dependentvisualclosure each28serialchildren/"
        "onepacket26distinctPNGgroups49originals23aliases900x2000returned1080x2400source;Claude summary-only1-12 explicit. "
        "Initial overstrict transportassertion/recovery preserved,notpermissiondenial/rejectedlinguisticreview. "
        "All30Han/fourfamilies/readable冫冱氵/fallbackface unknown;complementaryhorizontaltable notallcolumnsoneframe. "
        "Fullsigned0d2c9aee productionContentSyncONCE1092kanji5048words112N1/problems0/epoch1. "
        "Full+Lite fullゴコ/さ.えるこお.るひ.える unchanged;selectedon[]/kun[さ.える],offeredさえる/goodlog/Done1of1. "
        "Actualmeaningfeedback/1pair2directions/SystemBack/offline/N1selection. Seveninjectedreferencepaths/ungradedtrace/"
        "shapeonly/giveuprecallgrade1 NOT humanhandwriting/successfulrecall/MLKit/download;120+4Paintrecords NOT124PNGreads. "
        "Finaltree transientloading NOT loadedpersistenceproof;seededdisposableschedule NOTownerprogress. "
        "Owned5435580parent11976qemu1240 stopped,owner5556 untouched. Preserve all originalsource/review/process/denial/"
        "OOM/lookup/citation/readdepth/viewport/phone limits and FULLlivehistory. HOST-only2GiBinit NEVERnative;"
        "noapp/guestheap/guardchanges. CompatibleAndroidf9b59a2+ required;physicalphone/generalrelease/whole-set outstanding. "
        "Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=545, status="continue", stage="batch-080-published-verified-before-081",
             lastPublishedCommit=head, remainingAdditions=1121, blocker=None, nextAction=next_action)
    p["batch080PublicationCheckpoint"] = publication
    p["execution545StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1121 source-bounded additions not authored/review-closed/published;later batches retain all original source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 545, "checkpoint": 545, "batch": "080",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8366,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "originalRootKeyCountCompared": len(original),
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 107, "remainingAdditions": 1121, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "verifiedAt": now(), "nextAction": next_action, "status": "continue",
    }
    save(L / "execution-545-final-verification.json", result)
    save(L / "batch-080-publication-checkpoint.json", publication)
    p["execution545CoordinatorCheckpoint"] = result
    p["batch080PublicationIssueReceipt"] = {
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
