import copy
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
D = S / "batch-065-acceptance"
BASE = "0fe60920ee7e2de1504edb44e673aa370d928a17"
START = "848a25e006cfb3287c73326bf50bf3d941087e94"
TEACHING = "45c275e7c041d8486705ab860a31f34e51ac7a70"
VERSION = "6a940651167e0e94"
SESSION = C / "logs" / "a4f4add2-997d-4e20-af30-f73f041d209c"
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".execution421.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


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


def source_audit():
    unchanged()
    spec = importlib.util.spec_from_file_location("frozen413", C / "execution-413.py")
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    snapshot = source.inputs()
    ledger = load(S / "batch-065-progress.json")
    result = audit(R, "065")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    packets = []
    for kind, ids in source.groups(dictionary).items():
        name = "batch-065-jmdict.xml" if kind == "lexical" else "batch-065-comparison-jmdict.xml"
        assert load(S / f"batch-065-{kind}-selection.json")["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert set(ids) == {i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]}
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert sum(p["families"] for p in packets) == 24
    assert (S / "batch-065-kanjidic2.xml").read_bytes() == source.raw_metadata()
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = {
        "words/虎.md": {"quiz_exclusions": ["酔っ払い"]},
        "words/猿.md": {"quiz_exclusions": ["馬鹿"]},
        "words/丘.md": {"quiz_exclusions": ["坂", "山"]},
        "kanji/山.md": {"distractors": ["川", "出", "木"]},
    }
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
        if int(row["batch"]) <= 65:
            assert not expected & set(row["membership"])
            assert row["reviewClosed"] == row["membership"]
            if int(row["batch"]) < 65:
                assert row["published"] == row["membership"]
            expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - original == expected and len(expected) == 92 and original <= current
    index = {r["kanji"]: r for r in load(S / "source-index.json")}
    for char in expected:
        meta = metadata(R, f"kanji/{char}.md")
        for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
            assert meta[field] == index[char]["metadata"][field], (char, field)
        assert meta["jlpt"] == 1
        stroke = load(R / "strokes" / f"{char}.json")
        assert stroke["kanji"] == char and stroke["strokeCount"] == meta["strokes"]
        assert stroke["sourceRevision"] == snapshot["kanjivg"]["revision"]
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[61] == "倹"
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R) and manifest["contentVersion"] == VERSION
    maps = {}
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                } else sha256(R / name)
                assert actual == digest, name
            maps[section] = len(entries)
    assert sum(maps.values()) == 8324
    assert ledger["allMappedReciprocalPairs"] == [
        ["倹", "words/倹約.md"], ["倹", "words/倹しい.md"], ["約", "words/倹約.md"]]
    for char, word in ledger["allMappedReciprocalPairs"]:
        assert f"(../kanji/{char}.md)" in (R / word).read_text(encoding="utf-8")
        assert f"(../{word})" in (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
    for one, other in (("倹約", "倹しい"), ("倹しい", "倹約")):
        assert f"[{other}]({other}.md)" in (R / "words" / f"{one}.md").read_text(encoding="utf-8")
    actual_exclusions = {}
    for word in ("倹約", "倹しい"):
        meta = metadata(R, f"words/{word}.md")
        assert "jlpt" not in meta
        actual_exclusions[word] = meta["quiz_exclusions"]
    assert actual_exclusions["倹しい"] == ["節約", "経済", "地味", "けち", "謙虚"]
    assert actual_exclusions["倹約"] == ["節約", "経済", "倹しい", "けち"]
    geometry = load(S / "batch-065-stroke-evidence.json")
    svg = (C / "inputs" / "n1-05039-70a0b7ae.svg").read_bytes()
    assert sha(C / "inputs" / "n1-05039-70a0b7ae.svg") == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "倹.json") == convert("倹", svg.decode("utf-8"))
    assert sha(R / "strokes" / "倹.json") == geometry["targetSha256"]
    articles = ["kanji/倹.md", "words/倹約.md", "words/倹しい.md", "kanji/約.md"]
    han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",
                               "\n".join((R / name).read_text(encoding="utf-8") for name in articles))))
    fonts = []
    for row in load(S / "font-coverage.json")["fonts"]:
        path = A / row["path"]
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [char for char in han if ord(char) not in font.getBestCmap()]
        fonts.append({"path": row["path"], "sha256": row["sha256"], "missing": missing})
    result.update(
        execution=421, status="combined-source-audit-pending-evidence-reverification",
        exactLocalAdditionMembership=sorted(expected), baselineMetadataAndStrokesChecked=counts,
        explicitInheritedMetadataExceptions=exceptions, newBaselineMetadataExceptions=[],
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        exactFrozenDictionaryFamilies=24, dictionaryPackets=packets,
        runtimePayloadHashesVerified=8324, manifestMaps=maps,
        allMappedReciprocalPairs=3, mappedDirectedLinks=6, comparisonRouteBothDirections=True,
        actualWordExclusions=actual_exclusions,
        actualCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                      "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
                      "namedSourceMembersPresent": len(current & set(named))},
        actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical frozen-family/source/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test. Historical evidence retained.",
    )
    assert result["actualCounts"] == {"kanji": 1077, "words": 5036, "n1Labelled": 97, "namedSourceMembersPresent": 96}
    save(S / "batch-065-acceptance-source-audit.json", result)
    print("Frozen sources,24families,baseline,92exact additions,8324hashes,three pairs,comparison,geometry/fonts/budget passed.")


def validate(resume=False):
    receipts = load(C / "artifacts" / "execution-421-validation-receipts.json") if resume else []
    for name, args in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        if resume and any(row["check"] == name and row["exitCode"] == 0 for row in receipts):
            continue
        suffix = "-attempt-2" if resume and name == "source-audit" else ""
        path = SESSION / f"execution-421-{name}{suffix}.txt"
        assert not path.exists(), path
        started = now()
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args],
                                    cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        row = {"check": name, "command": ["python", "-X", "utf8", "-B", *args],
               "startedAt": started, "completedAt": now(), "exitCode": result.returncode,
               "log": str(path), "sha256": sha(path)}
        receipts.append(row)
        save(C / "artifacts" / "execution-421-validation-receipts.json", receipts)
        print(json.dumps(row), flush=True)
        if result.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(result.returncode)


def evidence():
    unchanged()
    reconciliation = load(V / "batch-065-reconciliation.json")
    assert reconciliation["textualReviewClosed"]
    assert all(row["status"] == "resolved" for row in reconciliation["findings"])
    processes = list(reconciliation["processes"].values())
    for row in processes:
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"] and not row["observedToolOverlaps"]
        assert row["actualModels"] == [row["requestedModel"]]
        for field, digest in (("report", "reportSha256"), ("execution", "executionSha256"), ("coverage", "coverageSha256")):
            assert sha(V / row[field]) == row[digest]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
    assert [row["requestedModel"] for row in processes[:2]] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert all(datetime.fromisoformat(one["completedAt"]) < datetime.fromisoformat(two["startedAt"])
               for one, two in zip(processes, processes[1:]))
    visual = load(V / "batch-065-visual-reconciliation.json")
    record420 = load(S / "execution-420.json")
    assert sha(V / "batch-065-visual-reconciliation.json") == record420["reconciliationSha256"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert visual["allReviewerProcessesSerialAndExited"] and not visual["allOriginalInternalReadsSerial"]
    assert visual["processDisposition"]["status"] == "partially resolved"
    reviews = list(record420["reviews"].values())
    for row in reviews:
        assert row["exitCode"] == 0
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    assert not reviews[0]["processAndCoverageAccepted"] and reviews[0]["overlaps"] == 2
    assert all(row["processAndCoverageAccepted"] and row["overlaps"] == 0 for row in reviews[1:])
    assert all(datetime.fromisoformat(one["completedAt"]) < datetime.fromisoformat(two["startedAt"])
               for one, two in zip(reviews, reviews[1:]))
    android = load(S / "execution-417.json")
    for row in android["archivedArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    for row in android["provenance"]:
        assert sha(Path(row["path"])) == row["sha256"]
    for row in android["recovery"]["tests"]:
        archived = V / "batch-065-android" / Path(row["artifactPath"]).name
        assert sha(archived) == row["sha256"]
        xml = ET.parse(archived).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(int(xml.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
        assert xml.attrib["timestamp"] == row["timestamp"] and Path(row["fixtureRoot"]).resolve() == R.resolve()
    assert [row["tests"] for row in android["recovery"]["tests"]] == [3, 1]
    native = load(S / "execution-419.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    index = load(R / native["artifactIndex"])
    for row in index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
    raw = V / "batch-065-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$", raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-065-native" / "attempt-1" / "n1-065-article-route.json")
    assert route == native["nativeRouteEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1077, 5036, 97, 0]
    assert route["acceptedReadingParserEpoch"] == 1 and route["quizOnKeys"] == ["けん"] and route["quizKunKeys"] == ["つましい"]
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    all_receipts = load(C / "artifacts" / "execution-421-validation-receipts.json")
    receipts = [row for row in all_receipts if row["exitCode"] == 0]
    failures = [row for row in all_receipts if row["exitCode"] != 0]
    assert len(receipts) == 6 and len(failures) == 1
    assert failures[0]["check"] == "source-audit"
    for row in all_receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    summary = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                        (SESSION / "execution-421-python-tests.txt").read_text(encoding="utf-8"))
    assert summary and int(summary[1]) == 368
    limits = (
        "Bounded owner-testing only; physical-phone/general-release/whole-set acceptance outstanding. Compatible Androidf9b59a2+ required. "
        "Original two-family blind textual reviews and source/read-depth/citation limits retained; C1 conservative modest-living/attitude display guard resolved, "
        "original GPT disagreement retained; C2 frequency-neutral spelling clarification confirmed. No new linguistic certification from24mechanical family re-extractions. "
        "Original Claude420 internal two-tool overlaps remain NONCONFORMANT; exact four affected resources freshly serially reconfirmed in original-session5call recovery, "
        "not retroactive process acceptance. GPT42044calls serial; reviewer processes exited serially. Thirty distinct bounded images per family;62returned900x2000payloads "
        "versus1080x2400sources are access evidence, not comprehension. Unseen article/table regions and actual fallbackface remain unverified. "
        "Accepted417fresh Android3+1/no skips and419native two terminalcase0/148.883s independently reverified, not rerun. Full productionContentSyncONCE "
        "1077kanji/5036words/97N1/zero problems/epoch1; full and curated on/kun, persisted Good grades/no source-only log, three mapped pairs in six directions "
        "and two support comparisons/SystemBack/offline/meaning/N1selection/10reference-touch strokes/ungradedtrace/recallmiss/persistedDrawAgain. "
        "Synthetic queues/source/history are not ownerprogress, MLKit or successful humanrecall. Readable fourfontrows do not identify fallbackface or everyphone. "
        "Original416permission denial/actual1GiB HOST OOM and049512MiBfailure remain; qualified HOST-only2GiB init is NOT for native/guest/app heaps. "
        "No archiveguard/permission/runtime changes. Owned419helpers stopped; preexisting5556 retained; sharedADB SYN probes and TIME_WAIT not emptyports. "
        "Latestmain already ancestral, runtime/tools equal accepted teaching; no new concern requiring duplicate Android/native/reviewer runs. "
        "Vocabulary pilot coverage gaps retained, not repaired or counted complete. Supporting words are not an N1 vocabulary deck."
    )
    result = load(S / "batch-065-acceptance-source-audit.json")
    result.update(status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
                  integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=git("rev-parse", "origin/main"),
                  normalMergeResult="Already up to date; no conflicts or substantive teaching changes.",
                  pythonTests={"passed": 368, "failures": 0, "errors": 0}, validationReceipts=receipts,
                  preservedFailedAuditReceipts=failures,
                  auditCorrection="Current wordQuizAudit direct-exclusion list lagged already-reviewed C1 teaching. Exact current 謙虚 guard/rationale synchronized; no teaching/manifest changed. Original failure preserved, exact audit rerun passed.",
                  acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
                  acceptedAndroidNativeReviewerRerun=False, originalClaudeVisualTurnSerial=False,
                  affectedVisualResourcesSeriallyReconfirmed=True, boundedDependentVisualAcceptance=True,
                  nativeArtifactHashesReverified=len(index["files"]), reviewedRuntimeAndToolsUnchanged=True,
                  textualReconciliationSha256=sha(V / "batch-065-reconciliation.json"),
                  visualAcceptanceSha256=sha(V / "batch-065-visual-reconciliation.json"),
                  androidEvidenceSha256=sha(S / "execution-417.json"),
                  nativeEvidenceSha256=sha(S / "execution-419.json"), limits=limits)
    save(S / "batch-065-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in all_receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    shutil.copyfile(Path(__file__), D / Path(__file__).name)
    p = load(C / "progress.json")
    save(S / "execution-421.json", {
        "schemaVersion": 1, **p["execution421StartingState"],
        "status": result["status"], "acceptanceRecord": "batch-065-acceptance-audit.json",
        "publishedAdditions": 91, "remainingAdditions": 1137, "localDraftAdditions": 92,
        "limits": limits, "nextAction": "Normal signed acceptance, owner fastforward, greenCI/every immutable publicZIPhash; terminal evidence commit and final receipts/ownerissue60 before counting065 delivery; no066."
    })
    p["stage"] = "batch-065-combined-tree-accepted-pending-normal-signing"
    save(C / "progress.json", p)
    print("Combined acceptance archived; publication pending.")


if __name__ == "__main__":
    {"source-audit": source_audit, "validate": validate,
     "resume-validation": lambda: validate(True), "evidence": evidence}[sys.argv[1]]()
