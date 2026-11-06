"""Batch075 combined-tree acceptance and bounded publication evidence."""
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
L = C / "logs" / "cc9cd17c-c350-4a21-b8aa-b7ef5e02d0f3"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-075-acceptance"
BASE = "1446bed45489d6d1e30944e2070ea888a33b83e1"
START = "3a9be3dea9c3e335a32a297a95c40e14e4d50de3"
TEACHING = "f5b70805d4a4a99d27036c71701277f1b8fc8b00"
VERSION = "2759d7b13c89eb8f"
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
    temporary = path.with_suffix(path.suffix + ".execution503.tmp")
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
    ledger = load(S / "batch-075-progress.json")
    result = audit(R, "075")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    for kind in ("lexical", "comparison"):
        selection = load(S / f"batch-075-{kind}-selection.json")
        spellings = set(selection.get("requestedSpellings", []))
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("典" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else any(k.text in spellings for k in e.findall("k_ele/keb") + e.findall("r_ele/reb")))]
        name = "batch-075-jmdict.xml" if kind == "lexical" else "batch-075-comparison-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        key = "lexicalDispositions" if kind == "lexical" else "comparisonDispositions"
        dispositions = [i for row in ledger[key] for i in row["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [174, 24]
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-075-kanjidic2.xml").getroot()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 12
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-074-acceptance-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 75 and not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 75:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 102 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[83] == "典"
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
    assert sum(maps.values()) == 8352
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 12
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    geometry = load(S / "batch-075-stroke-evidence.json")
    svg_path = Path(geometry["path"])
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "典.json") == convert("典", svg.decode("utf-8"))
    assert sha(R / "strokes" / "典.json") == geometry["targetSha256"]
    draft = load(S / "batch-075-draft-audit.json")["actualAuthoredHanFonts"]
    articles = draft["articles"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == draft["characters"] and len(han) == 117
    fonts = []
    for row in draft["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["missingActualDraftHan"] == ["亅", "厂", "奠", "艹"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1087, "words": 5044, "n1Labelled": 107, "namedSourceMembersPresent": 106}
    result.update(
        execution=503, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=len(distinct),
        dictionaryFamilyOccurrences=198, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=12, runtimePayloadHashesVerified=8352, manifestMaps=maps,
        allMappedReciprocalPairs=12, mappedDirectedLinks=24, unavailableDeclaredComponents=[],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-075-acceptance-source-audit.json", result)
    print(f"{len(distinct)}families/198occurrences/12rawrecords/baseline/102localadditions/8352hashes/12pairs/geometry/cmaps/budgets passed.")


def validate():
    unchanged()
    assert git("rev-parse", "HEAD") == START
    target = L / "execution-503-validation-receipts.json"
    assert not target.exists()
    receipts = []
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = L / f"execution-503-{name}.txt"
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
    textual = load(V / "batch-075-reconciliation.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert textual["serialReviewerProcessesVerified"] and textual["claudeBoundedConfirmationInternalToolsSerial"]
    assert not textual["allInitialInternalToolsSerial"]
    processes = list(textual["processes"].values())
    for name, row in textual["processes"].items():
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert row["actualModels"] == [row["requestedModel"]]
        for field in ("report", "execution", "coverage"):
            assert sha(V / row[field]) == row[field + "Sha256"]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
        if name != "initial-claude":
            assert row["observedToolOverlapCount"] == row["multiToolResponseCount"] == 0
        else:
            assert row["observedToolOverlapCount"] == 30 and row["multiToolResponseCount"] == 8
    for first, second in zip(processes, processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    visual = load(V / "batch-075-visual-reconciliation.json")
    record502 = load(S / "execution-502.json")
    assert sha(V / "batch-075-visual-reconciliation.json") == record502["reconciliationSha256"]
    assert visual["allFourReviewerProcessesSerialAndExited"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert not visual["allVisualExecutionsInternallySerial"]
    visual_processes = list(record502["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    for first, second in zip(visual_processes, visual_processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    assert visual["payloadAccounting"]["gptCombinedCertifiedSourceImages"] == 51
    assert visual["payloadAccounting"]["gptFreshRecoveryImages"] == 24
    android = load(S / "execution-499.json")
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
    native = load(S / "execution-501.json")
    for row in native["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    raw = V / "batch-075-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-075-native" / "attempt-1" / "n1-075-article-route.json")
    assert route == native["routeEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1087, 5044, 107, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["fullOnyomi"] == ["テン", "デン"] and route["fullKunyomi"] == ["ふみ", "のり"]
    assert route["quizOnKeys"] == ["てん", "でん"] and route["quizKunKeys"] == []
    assert route["bothCuratedOnKeysPersistedGoodNoKunAndDone"]
    assert route["mappedReciprocalPairs"] == 12 and route["directedLinkTransitions"] == 24
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(L / "execution-503-validation-receipts.json")
    assert len(receipts) == 6 and all(r["exitCode"] == 0 for r in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-503-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    result = load(S / "batch-075-acceptance-source-audit.json")
    limits = record502["limits"] + (
        " Fresh combined vocabulary consistency is pilot2122/2431, not full coverage. Bounded owner testing only. "
        "Historical pending-gate statements remain historical; this acceptance closes only enumerated gates."
    )
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh main already ancestral; no substantive teaching or tool changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(native["artifacts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        historicalProcessDeviationsPreserved=True,
        textualReconciliationSha256=sha(V / "batch-075-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-075-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-499.json"), nativeEvidenceSha256=sha(S / "execution-501.json"),
        limits=limits,
    )
    save(S / "batch-075-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-503.json", {
        "schemaVersion": 1, **p["execution503StartingState"], "recordedAt": now(),
        "status": result["status"], "acceptanceRecord": "batch-075-acceptance-audit.json",
        "publishedAdditions": 101, "remainingAdditions": 1127, "localReviewClosedAdditions": 102,
        "limits": limits, "nextAction": "Normal signed acceptance, owner fast-forward, exact green CI/public ZIP then terminal evidence/owner issue60; yield before076.",
    })
    p["stage"] = "batch-075-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


if __name__ == "__main__":
    {"validate": validate, "source-audit": source_audit, "evidence": evidence}[sys.argv[1]]()
