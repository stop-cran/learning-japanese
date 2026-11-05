import copy
import gzip
import hashlib
import importlib.util
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
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
L = C / "logs" / "b6a6a3f0-ba8b-42d3-af0d-4b1504bf7824"
D = S / "batch-067-acceptance"
BASE = "f0b318eb058efa8081db770f12aa15963af7ff79"
START = "6034d0f228681eac3a33dcd4c0cc27338df2bf4d"
TEACHING = "5cb2ea4bc804ac218b17d5c583d4fba95e60971c"
VERSION = "68c767f176e68882"
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
    temporary = path.with_suffix(path.suffix + ".execution437.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, tree=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", *args],
        cwd=tree, text=True, encoding="utf-8").strip()


def now():
    return datetime.now().astimezone().isoformat()


def unchanged():
    assert git("branch", "--show-current") == "content/n1-kanji"
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", tree=A) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", tree=A)
    subprocess.run(["git", "merge-base", "--is-ancestor", git("rev-parse", "origin/main"), "HEAD"],
                   cwd=R, check=True)


def start():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 436 and git("rev-parse", "HEAD") == START
    assert not git("status", "--porcelain")
    unchanged()
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == p["checkpoint"]
    assert not (L / "before-progress-execution437.json").exists()
    save(L / "before-progress-execution437.json", p)
    p["execution437StartingState"] = {
        "execution": 437, "batch": "067", "startingHead": START,
        "scope": "SAME067 latest-main combined acceptance, normal signed owner fast-forward publication, exact CI/public ZIP acceptance and durable checkpoint; no068, duplicate reviewers/Android/native or second runner.",
        "status": "combined-acceptance-started",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final436 and complete approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
        },
        "originMain": git("rev-parse", "origin/main"), "recordedAt": now(),
    }
    p["stage"] = "batch-067-combined-current-main-acceptance"
    p["nextAction"] = p["execution437StartingState"]["scope"]
    save(C / "progress.json", p)
    print("Execution437 starting scope saved; complete live history preserved.")


def source_audit():
    unchanged()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == row["sha256"], name
    for name, section in (("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
                          ("n1-implementation-JMdict_e.gz", "jmdict")):
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    ledger = load(S / "batch-067-progress.json")
    result = audit(R, "067")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    groups = {"lexical": [], "comparison": []}
    comparisons = set(load(S / "batch-067-comparison-selection.json")["selectionSpellings"])
    for entry in ET.fromstring(gzip.decompress(dictionary)).findall("entry"):
        forms = {e.text for e in entry.findall("k_ele/keb") + entry.findall("r_ele/reb")}
        kind = "lexical" if any("僧" in form for form in forms) else "comparison" if forms & comparisons else None
        if kind:
            groups[kind].append(entry.findtext("ent_seq"))
    packets = []
    for kind, ids in groups.items():
        name = "batch-067-jmdict.xml" if kind == "lexical" else "batch-067-comparison-jmdict.xml"
        assert load(S / f"batch-067-{kind}-selection.json")["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert set(ids) == {i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]}
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [106, 7]
    raw_source = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    raw_packet = ET.parse(S / "batch-067-kanjidic2.xml").getroot()
    raw_characters = raw_packet.findall("character")
    assert len(raw_characters) == 6
    source_by_char = {e.findtext("literal"): e for e in raw_source.findall("character")}
    def normalized(element):
        element = copy.deepcopy(element)
        ET.indent(element, space="  ")
        return ET.tostring(element, encoding="unicode").strip()
    assert all(normalized(e) == normalized(source_by_char[e.findtext("literal")]) for e in raw_characters)
    assert normalized(raw_packet.find("header")) == normalized(raw_source.find("header"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-067-draft-audit.json")["explicitInheritedMetadataExceptions"]
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
    original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
    expected = set(load(C / "progress.json")["publicationCheckpoint"]["pilotMembership"])
    for path in sorted(S.glob("batch-*-progress.json")):
        row = load(path)
        if int(row["batch"]) <= 67:
            assert not expected & set(row["membership"])
            assert row["reviewClosed"] == row["membership"]
            if int(row["batch"]) < 67:
                assert row["published"] == row["membership"]
            expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - original == expected and len(expected) == 94 and original <= current
    index = {row["kanji"]: row for row in load(S / "source-index.json")}
    for char in expected:
        meta = metadata(R, f"kanji/{char}.md")
        for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
            assert meta[field] == index[char]["metadata"][field], (char, field)
        assert meta["jlpt"] == 1
        stroke = load(R / "strokes" / f"{char}.json")
        assert stroke["kanji"] == char and stroke["strokeCount"] == len(stroke["strokes"]) == meta["strokes"]
        assert stroke["sourceRevision"] == snapshot["kanjivg"]["revision"]
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[75] == "僧"
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
    assert sum(maps.values()) == 8329
    assert "(../kanji/僧.md)" in (R / "words" / "僧侶.md").read_text(encoding="utf-8")
    assert "(../words/僧侶.md)" in (R / "kanji" / "僧.md").read_text(encoding="utf-8")
    assert "(坊さん.md)" in (R / "words" / "僧侶.md").read_text(encoding="utf-8")
    assert "(僧侶.md)" in (R / "words" / "坊さん.md").read_text(encoding="utf-8")
    assert not (R / "kanji" / "侶.md").exists()
    geometry = load(S / "batch-067-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-050e7-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "僧.json") == convert("僧", svg.decode("utf-8"))
    assert sha(R / "strokes" / "僧.json") == geometry["targetSha256"]
    articles = ["kanji/僧.md", "words/僧侶.md", "words/坊さん.md"]
    han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                               "\n".join((R / name).read_text(encoding="utf-8") for name in articles))))
    fonts = []
    for row in load(S / "font-coverage.json")["fonts"]:
        path = A / row["path"]
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [char for char in han if ord(char) not in font.getBestCmap()]
        fonts.append({"path": row["path"], "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1079, "words": 5037, "n1Labelled": 99, "namedSourceMembersPresent": 98}
    result.update(
        execution=437, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDictionaryFamilies=113,
        dictionaryPackets=packets, completeRawCharacterRecordsVerified=6,
        runtimePayloadHashesVerified=8329, manifestMaps=maps,
        allMappedReciprocalPairs=1, mappedDirectedLinks=2, directedComparisonLinks=2,
        unavailableMappedPairs=load(S / "batch-067-draft-audit.json")["unavailableMappedPairs"],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-067-acceptance-source-audit.json", result)
    print("Frozen sources/113families/baseline/94additions/8329hashes/1pair+2comparisondirections/geometry/cmaps/budgets passed.")


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
        path = L / f"execution-437-{name}.txt"
        assert not path.exists(), path
        started = now()
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args],
                                    cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({
            "check": name, "command": ["python", "-X", "utf8", "-B", *args],
            "startedAt": started, "completedAt": now(), "exitCode": result.returncode,
            "log": str(path), "sha256": sha(path),
        })
        save(C / "artifacts" / "execution-437-validation-receipts.json", receipts)
        print(f"{name}: exit {result.returncode}", flush=True)
        if result.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(result.returncode)


def evidence():
    unchanged()
    textual = load(V / "batch-067-reconciliation.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    processes = list(textual["processes"].values())
    assert [row["requestedModel"] for row in processes] == ["claude-opus-5.5", "gpt-6.1-sol"]
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"] and not row["observedToolOverlaps"]
        assert row["actualModels"] == [row["requestedModel"]] and row["snapshot"] == TEACHING
        for field, digest in (("report", "reportSha256"), ("execution", "executionSha256"), ("coverage", "coverageSha256")):
            assert sha(V / row[field]) == row[digest]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
    assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
    visual = load(V / "batch-067-visual-reconciliation.json")
    record436 = load(S / "execution-436.json")
    assert sha(V / "batch-067-visual-reconciliation.json") == record436["reconciliationSha256"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert visual["allReviewerProcessesSerialAndExited"] and visual["allImageReadsSerial"]
    assert not visual["allInternalReadsSerial"] and not record436["allInternalReadsSerial"]
    reviews = list(record436["reviews"].values())
    for row in reviews:
        assert row["exitCode"] == 0 and row["returnedImages"] == 23
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    assert not reviews[0]["processAndCoverageAccepted"]
    assert reviews[0]["boundedConfirmationAcceptedWithDisclosedRepair"]
    assert reviews[1]["processAndCoverageAccepted"]
    repair = record436["repair"]
    assert repair["serialRepairAccepted"] and not repair["observedToolOverlaps"]
    assert sha(C / "batch-067-visual-claude-serial-repair.jsonl") == repair["rawExecutionSha256"]
    assert datetime.fromisoformat(reviews[0]["completedAt"]) < datetime.fromisoformat(repair["startedAt"])
    assert datetime.fromisoformat(repair["completedAt"]) < datetime.fromisoformat(reviews[1]["startedAt"])
    android = load(S / "execution-433.json")
    assert android["exitCode"] == 0
    for row in android["tests"]:
        path = R / row["archivedPath"]
        assert sha(path) == row["sha256"]
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(int(xml.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
        assert xml.attrib["timestamp"] == row["timestamp"] and Path(row["fixtureRoot"]).resolve() == R.resolve()
    assert [row["tests"] for row in android["tests"]] == [3, 1]
    for row in android["rawProvenance"] + android["testImplementationsAndHostInit"]:
        assert sha(Path(row["path"])) == row["sha256"]
    native = load(S / "execution-435.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    index = load(R / native["artifactIndex"])
    for row in index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
    raw = V / "batch-067-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-067-native" / "attempt-1" / "n1-067-article-route.json")
    assert route == native["nativeRouteEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1079, 5037, 99, 0]
    assert route["acceptedReadingParserEpoch"] == 1 and route["quizOnKeys"] == ["そう"] and route["quizKunKeys"] == []
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(C / "artifacts" / "execution-437-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    summary = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                        (L / "execution-437-python-tests.txt").read_text(encoding="utf-8"))
    assert summary and int(summary[1]) == 368
    result = load(S / "batch-067-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"),
        latestMainIntegrated=git("rev-parse", "origin/main"),
        normalMergeResult="Already up to date; no substantive teaching or tool changes.",
        pythonTests={"passed": 368, "failures": 0, "errors": 0}, validationReceipts=receipts,
        acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(index["files"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        visualProcessExceptionPreserved=True, allInternalReviewerReadsSerial=False,
        textualReconciliationSha256=sha(V / "batch-067-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-067-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-433.json"), nativeEvidenceSha256=sha(S / "execution-435.json"),
        limits=(
            "Bounded owner-testing only; physical-phone/general-release/whole-set outstanding. Compatible Androidf9b59a2+ required. "
            "Original two-family textual reports, source/retrieval/read-depth/lookup limits and optional decisions retained. "
            "Original-session visual confirmations:23 source PNGs per family/46 actual900x2000 payloads from37capture names. "
            "Reviewer processes and all image reads serial. Claude original two-small-receipt overlap remains noncompliant "
            "processAndCoverageAccepted=false; same-session serial repair accepted before GPT. Not an all-internal-reads-serial execution. "
            "No established actionable defect; unseen viewport/table regions and actual fallback faces unverified. "
            "Actual N1 meaning choices visibly wrong for僧 but differ from authored増/値/倍, whose native presentation is NOT certified. "
            "Accepted433 HOST Android3+1 and435 native2terminal0/138.141s independently reverified, not rerun. "
            "Exact full archive productionContentSyncONCE1079kanji5037words99N1/problems0/epoch1; normalizedそう Good/noKunLog, "
            "one mapped pair/two directions and both僧侶-坊さん comparison directions, full3articles/SystemBack/offline/N1selection/meaning/"
            "13reference-touch strokes/ungradedtrace/recallmiss/persistedDrawAgain. Not MLKit, human successful recall, ownerprogress or phone evidence. "
            "Four readable production font rows do not identify fallback face or every-phone readability. "
            "Historical permission denials/HOST OOMs retained; qualified HOST-only2GiB init NEVER used in native. "
            "No production, app/guest heap, guard or permission changes. Latestmain ancestral and runtime/tools unchanged; "
            "no duplicate reviewer/Android/native required. Vocabulary pilot gaps retained, not repaired or counted complete. "
            "One new necessary support word in067;95 project support additions are not an N1 vocabulary deck. "
            "No 侶 card exists; its future addition must activate the preserved metadata pair."
        ),
    )
    save(S / "batch-067-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    shutil.copyfile(Path(__file__), D / Path(__file__).name)
    p = load(C / "progress.json")
    save(S / "execution-437.json", {
        "schemaVersion": 1, **p["execution437StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-067-acceptance-audit.json",
        "publishedAdditions": 93, "remainingAdditions": 1135, "localDraftAdditions": 94,
        "limits": result["limits"], "nextAction": "Normal signed acceptance/ownerfastforward/greenCI/every immutable ZIP hash; terminal evidence/CI/ZIP/ownerissue60 then yield before068.",
    })
    p["stage"] = "batch-067-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and exact inherited evidence archived; publication pending.")


if __name__ == "__main__":
    {"start": start, "source-audit": source_audit, "validate": validate, "evidence": evidence}[sys.argv[1]]()
