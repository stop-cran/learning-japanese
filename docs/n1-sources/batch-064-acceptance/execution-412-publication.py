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
D = S / "batch-064-acceptance"
START = "0e85e2e2f1e83dcba5dd7ea3c1d504245d154384"
BASE = "d00bf868466437d39b0330a383de8448686b502d"
TEACHING = "ff6eb7893344b806bf517ebd41bf19089bed5021"
VERSION = "ae05977ba66f42f5"
REQUEST = C / "logs" / "840882c8-0104-4371-a6b5-6f8d8decbefe" / "request.txt"
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
    temporary = path.with_suffix(path.suffix + ".execution412.tmp")
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


def start():
    text = REQUEST.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert embedded["checkpoint"] == p["checkpoint"] == 411 and p["batch"] == "064"
    assert git("rev-parse", "HEAD") == START and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not (C / "execution-412-starting-progress.json").exists()
    unchanged()
    save(C / "execution-412-starting-progress.json", p)
    record = {
        "execution": 412, "batch": "064", "startingHead": START, "recordedAt": now(),
        "status": "starting-combined-main-acceptance",
        "scope": "SAME064 combined-main acceptance and bounded owner-testing publication; no065, duplicate accepted Android/native/reviewer run or second runner absent a new substantive concern.",
        "authorization": {
            "requestSha256": sha(REQUEST), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete checkpoint parsed; operative contract, final411 and approved issue inspected directly. Historical middle not freshly semantically re-reviewed.",
        },
        "integratedMain": git("rev-parse", "origin/main"),
        "mergeDisposition": "Fetched main already ancestral; normal merge to confirm. No new substantive teaching delta.",
    }
    p["activeExecution"] = record
    p["execution412StartingState"] = copy.deepcopy(record)
    p["stage"] = "batch-064-combined-main-acceptance"
    save(C / "progress.json", p)
    print("Execution412 starting scope saved, preserving full live history.")


def source_audit():
    spec = importlib.util.spec_from_file_location("frozen399", C / "execution-399.py")
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    snapshot = source.inputs()
    ledger = load(S / "batch-064-progress.json")
    result = audit(R, "064")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    packets = []
    for kind, ids in source.groups(dictionary).items():
        name = "batch-064-jmdict.xml" if kind == "lexical" else "batch-064-comparison-jmdict.xml"
        assert load(S / f"batch-064-{kind}-selection.json")["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert set(ids) == {i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]}
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert sum(p["families"] for p in packets) == 33
    assert (S / "batch-064-kanjidic2.xml").read_bytes() == source.raw_metadata()
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
            expected = {**row["metadata"], **exceptions.get(name, {})}
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == row["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
    expected = set(load(C / "progress.json")["publicationCheckpoint"]["pilotMembership"])
    for path in sorted(S.glob("batch-*-progress.json")):
        row = load(path)
        if int(row["batch"]) <= 64:
            assert not expected & set(row["membership"])
            assert row["reviewClosed"] == row["membership"]
            if int(row["batch"]) < 64:
                assert row["published"] == row["membership"]
            expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - original == expected and len(expected) == 91 and original <= current
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[65] == "偵"
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
    assert sum(maps.values()) == 8320
    assert ledger["allMappedReciprocalPairs"] == [["偵", "words/探偵.md"], ["探", "words/探偵.md"]]
    for char, word in ledger["allMappedReciprocalPairs"]:
        assert f"(../kanji/{char}.md)" in (R / word).read_text(encoding="utf-8")
        assert f"(../{word})" in (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
    assert "[探偵](探偵.md)" in (R / "words" / "刑事.md").read_text(encoding="utf-8")
    assert "[刑事](刑事.md)" in (R / "words" / "探偵.md").read_text(encoding="utf-8")
    assert "jlpt" not in metadata(R, "words/探偵.md")
    geometry = load(S / "batch-064-stroke-evidence.json")
    svg = (C / "inputs" / "n1-05075-70a0b7ae.svg").read_bytes()
    assert sha(C / "inputs" / "n1-05075-70a0b7ae.svg") == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert source.digest((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    assert load(R / "strokes" / "偵.json") == convert("偵", svg.decode("utf-8"))
    assert sha(R / "strokes" / "偵.json") == geometry["targetSha256"]
    articles = ["kanji/偵.md", "words/探偵.md", "kanji/探.md", "words/刑事.md"]
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
        execution=412, status="combined-source-audit-pending-evidence-reverification",
        exactLocalAdditionMembership=sorted(expected), baselineMetadataAndStrokesChecked=counts,
        explicitInheritedMetadataExceptions=exceptions, newBaselineMetadataExceptions=[],
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        exactFrozenDictionaryFamilies=33, dictionaryPackets=packets,
        runtimePayloadHashesVerified=8320, manifestMaps=maps,
        allMappedReciprocalPairs=2, mappedDirectedLinks=4, comparisonRouteBothDirections=True,
        actualCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                      "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
                      "namedSourceMembersPresent": len(current & set(named))},
        actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical frozen-family/source/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test. Historical evidence retained.",
    )
    assert result["actualCounts"] == {"kanji": 1076, "words": 5034, "n1Labelled": 96, "namedSourceMembersPresent": 95}
    save(S / "batch-064-acceptance-source-audit.json", result)
    print("Frozen sources,33families,baseline,91exact additions,8320hashes,two pairs,comparison,geometry/fonts/budget passed.")


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
        path = C / "logs" / f"execution-412-{name}.txt"
        assert not path.exists(), path
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args],
                                    cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        row = {"check": name, "command": ["python", "-X", "utf8", "-B", *args],
               "exitCode": result.returncode, "log": str(path), "sha256": sha(path)}
        receipts.append(row)
        print(json.dumps(row), flush=True)
        if result.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(result.returncode)
    save(C / "artifacts" / "execution-412-validation-receipts.json", receipts)


def evidence():
    reconciliation = load(V / "batch-064-reconciliation.json")
    assert reconciliation["textualReviewClosed"] and reconciliation["reviewClosed"]
    assert all(row["status"] == "resolved" for row in reconciliation["findings"])
    assert sha(V / reconciliation["originalInitialReview"]) == reconciliation["originalInitialReviewSha256"]
    initial = load(V / reconciliation["originalInitialReview"])
    assert initial["strictInitialProcessContractAccepted"]
    rows = initial["reviewProcesses"]
    assert [row["model"] for row in rows] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert datetime.fromisoformat(rows[0]["completedAt"]) < datetime.fromisoformat(rows[1]["startedAt"])
    for row in rows:
        prefix = "batch-064-" + row["label"]
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
        assert not row["observedInternalOverlaps"] and not row["multiToolResponses"] and not row["failedCalls"]
        for suffix, field in ((".md", "reportSha256"), ("-execution.json", "executionRecordSha256"),
                              ("-coverage.json", "coverageRecordSha256")):
            assert sha(V / (prefix + suffix)) == row[field]
        assert sha(C / (prefix + ".jsonl")) == row["rawExecutionSha256"]
    for row in reconciliation["confirmationProcesses"]:
        assert row["exitCode"] == 0 and row["allRequiredTextReturned"]
        assert not row["observedToolOverlaps"] and not row["multiToolResponses"]
        assert sha(V / row["report"]) == row["reportSha256"]
        assert sha(V / row["executionRecord"]) == row["executionRecordSha256"]
        assert sha(C / Path(row["report"]).with_suffix(".jsonl").name) == row["rawExecutionSha256"]
    visual = load(V / "batch-064-native-visual-411-acceptance.json")
    assert visual["independentVisualAcceptance"] and not visual["actionableNewContentFindings"]
    assert visual["exactOriginalReviewerPathAccessRecovered"] and visual["serialExitsAndFirstArchiveBeforeSecondLaunch"]
    execution411 = load(S / "execution-411.json")
    assert sha(R / execution411["acceptanceRecord"]) == execution411["acceptanceRecordSha256"]
    for row in execution411["archivedArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    visuals = [load(R / name) for name in visual["reviewerRecords"]]
    for row, original in zip(visuals, rows):
        assert row["exitCode"] == 0 and row["actualModels"] == [original["model"]]
        assert row["sessionId"] == original["sessionId"]
        assert not row["observedToolOverlaps"] and not row["multiToolResponses"] and not row["unfinishedTools"]
        assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
        assert max(row["requestsPerAssistantResponse"]) == 1
        for call in row["toolCalls"]:
            assert call["success"]
            if "imagePayload" in call:
                image = call["imagePayload"]
                assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
    assert datetime.fromisoformat(visuals[0]["completedAt"]) < datetime.fromisoformat(visuals[1]["startedAt"])
    for prefix, row in visual["historical408409410Preserved"].items():
        assert sha(V / (prefix + ".md")) == row["reportSha256"]
        assert sha(V / (prefix + "-execution.json")) == row["executionSha256"]
        assert sha(C / (prefix + ".jsonl")) == row["rawSha256"]
        assert not row["strictAcceptance"]
    android = load(S / "execution-404.json")
    for row in android["archivedArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    for row in android["provenance"]:
        assert sha(Path(row["path"])) == row["sha256"]
    for row in android["recovery"]["tests"]:
        archived = V / "batch-064-android" / Path(row["artifactPath"]).name
        assert sha(archived) == row["sha256"]
        xml = ET.parse(archived).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(int(xml.attrib[key]) == 0 for key in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
        assert xml.attrib["timestamp"] == row["timestamp"] and Path(row["fixtureRoot"]).resolve() == R.resolve()
    assert [row["tests"] for row in android["recovery"]["tests"]] == [3, 1]
    native = load(S / "execution-406.json")
    recovery = load(S / "execution-407.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"] == recovery["artifactIndexSha256"]
    index = load(R / native["artifactIndex"])
    for row in index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
    for row in recovery["recoveryArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    raw = V / "batch-064-native" / "attempt-1" / "instrumentation.txt"
    assert sha(raw) == recovery["rawLogSha256"]
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$", raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-064-native" / "attempt-1" / "n1-064-article-route.json")
    assert route == recovery["actualRouteReceipt"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1076, 5034, 96, 0]
    assert route["acceptedReadingParserEpoch"] == 1 and route["quizOnKeys"] == ["てい"] and route["quizKunKeys"] == []
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    audit_record = load(S / "batch-064-acceptance-source-audit.json")
    receipts = load(C / "artifacts" / "execution-412-validation-receipts.json")
    for row in receipts:
        assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
    output = (C / "logs" / "execution-412-python-tests.txt").read_text(encoding="utf-8")
    summary = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)", output)
    assert summary
    count = int(summary[1])
    assert count == 368
    limits = (
        "Bounded owner-testing only; physical-phone/general-release/whole-set acceptance outstanding. Compatible Androidf9b59a2+ required. "
        "Original blind40145/44calls/30assignedranges each, zerooverlaps; source/read-depth/citation limits retained. "
        "Original402dependent link-only correction6calls each, not blind reviews. Source399/400 linguistic inspection retained; "
        "fresh41233families mechanically re-extracted, not newly linguistically reviewed. "
        "Historical408/409/410 visual/path failures remain strictly unaccepted; authorized scoped411 access/dependent closure is not retroactive acceptance. "
        "Claude41110calls/6freshimages plus retained408pixels; GPT41141calls/28images, serial/nooverlap/onecallperresponse. "
        "Kun-dash claim withdrawn (sole on row; dash is gloss punctuation), everyparagraph/footer narrowed; clipping/unseen pixels/actual fallbackface unverified. "
        "Source1080x2400/model900x2000 images separately retained. Native406single full productionContentSync/two terminalcase0, "
        "allmapped4transitions/comparison/SystemBack/offline/soleOnGood/noKun/11injectedreference strokes/recallmiss/persistedDrawAgain; "
        "meaningBack beforeNext is not newly persisted meaninggrade. Synthetic source/queues/history not ownerprogress, MLKit or humanrecall/phone evidence. "
        "Font160pilot render/all40 targets inherited, not freshly rerun. Fourfontrowspy/investigation/lookalikes readable/distinguishable; fallbackfaceunknown. "
        "403/406denials and exact parent404/407recovery preserved. Actual407nonempty remote5581connection NOT allportsfree; future fresh fullportguard required. "
        "Qualified049HOST512MiBOOM/HOSTonly1GiB init unchanged; no guest/appheap/archiveguard changes. "
        "Latestmain already ancestral and runtime/tools equal accepted teaching; no substantive merge concern requiring duplicate Android/native/reviewer work. "
        "Existing vocabulary pilot coverage gaps retained, not repaired or counted as complete. N1 support words are not an N1 vocabulary deck."
    )
    audit_record.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=git("rev-parse", "origin/main"),
        normalMergeResult="Already up to date; no conflicts or substantive teaching changes.",
        pythonTests={"passed": count, "failures": 0, "errors": 0}, validationReceipts=receipts,
        acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, strictInitialProcessContractAccepted=True,
        strictHistorical408409410VisualAcceptance=False, dependent411VisualAcceptance=True,
        nativeArtifactHashesReverified=len(index["files"]), reviewedRuntimeAndToolsUnchanged=True,
        textualReconciliationSha256=sha(V / "batch-064-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-064-native-visual-411-acceptance.json"),
        androidEvidenceSha256=sha(S / "execution-404.json"),
        nativeEvidenceSha256=sha(S / "execution-406.json"), nativeRecoverySha256=sha(S / "execution-407.json"),
        limits=limits,
    )
    save(S / "batch-064-acceptance-audit.json", audit_record)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    shutil.copyfile(Path(__file__), D / Path(__file__).name)
    p = load(C / "progress.json")
    save(S / "execution-412.json", {
        "schemaVersion": 1, **p["execution412StartingState"],
        "status": "combined-tree-locally-accepted-pending-publication",
        "acceptanceRecord": "batch-064-acceptance-audit.json", "publishedAdditions": 90,
        "remainingAdditions": 1138, "localDraftAdditions": 91, "limits": limits,
        "nextAction": "Normal signed acceptance, owner fastforward, greenCI/every immutable publicZIPhash; terminal evidence commit and final receipts/ownerissue60 before counting064 delivery; no065.",
    })
    p["activeExecution"].update(status="combined-tree-accepted-pending-normal-signing", pythonTests=count)
    p["stage"] = "batch-064-combined-tree-accepted-pending-normal-signing"
    save(C / "progress.json", p)
    unchanged()
    print(f"Combined acceptance saved: Python{count}; Android4/native2/68artifact hashes reverified, no reruns. Publication pending.")


def verified(phase, recovery_record=False):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-064-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION and archive["verifiedRuntimeHashes"] == 8320
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    assert git("log", "-1", "--format=%G?") == "G"
    dirty = git("status", "--porcelain")
    if recovery_record:
        assert dirty == "?? docs/n1-sources/batch-064-publication.json"
    else:
        assert not dirty
    unchanged()
    return head, ci, archive


def publication_records():
    head, ci, archive = verified("accepted", recovery_record=(S / "batch-064-publication.json").exists())
    p = load(C / "progress.json")
    audit_record = load(S / "batch-064-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 412, "batch": "064", "membership": ["偵"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": "400ba5ea60299cf4b77f6f9ffbf66cae8f061db3",
        "reviewedTeachingSnapshot": TEACHING, "textualClosureSnapshot": "94fcbbe3426f9a957a1131dee97b7f1ff2381f3f",
        "visualClosureSnapshot": START, "latestMainIntegrated": audit_record["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no signing bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-064-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-064-native-visual-411-acceptance.json",
        "validation": audit_record, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 91, "remainingAdditions": 1137,
            "currentKanji": 1076, "currentWords": 5034, "n1Labelled": 96, "namedSourceMembersPresent": 95,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 92, "batchChangedReusedArticles": 2,
            "requiredReciprocalPairs": 2, "activatedBaselinePairs": 0,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": audit_record["limits"],
        "nextAction": "Verify terminal evidence commit/CI/publicZIP/ownerissue60; checkpoint and yield before065.",
    }
    path = S / "batch-064-publication.json"
    if path.exists():
        saved = load(path)
        assert saved["acceptedCommit"] == head and saved["ci"] == ci and saved["immutablePublicArchive"] == archive
        publication = saved
    else:
        save(path, publication)
    ledger = load(S / "batch-064-progress.json")
    ledger["prePublicationCheckpoint"] = {key: copy.deepcopy(ledger[key])
                                         for key in ("status", "nextAction", "limits")}
    ledger.update(status=publication["status"], published=ledger["membership"],
                  publishedAdditions=91, remainingAdditions=1137, publishedCommit=head,
                  publicationRecord="batch-064-publication.json", acceptanceRecord="batch-064-acceptance-audit.json",
                  pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"])
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-064-progress.json", ledger)
    execution = load(S / "execution-412.json")
    execution.update(status=publication["status"], publicationRecord="batch-064-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-412.json", execution)
    for path in (C / "artifacts" / "batch-064-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 C / "verify-batch-064-publication.ps1", C / "verify-batch-002-publication.py",
                 C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-evidence",
                               acceptedCommit=head, ciRun=ci["databaseId"])
    p["stage"] = "batch-064-accepted-publication-verified-pending-terminal-evidence"
    save(C / "progress.json", p)
    print("Accepted main/greenCI/public8320hashes verified; terminal publication records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-064-publication.json")
    text = f"""Batch **064 (偵)** is published and verified for **bounded owner testing**, with necessary support **探偵**, its existing 探 common-word link and the link-only 刑事 comparison correction.

Authored snapshot `{publication['authoredSnapshot']}`, reviewed teaching `{TEACHING}`, textual closure `{publication['textualClosureSnapshot']}`, scoped dependent visual closure `{START}`. Fresh latest main `{publication['latestMainIntegrated']}` was already ancestral: normal merge, no substantive teaching conflict. Normally signed accepted/integrated publication `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global identity unchanged.

Fresh combined-tree checks: **368 Python tests**, validator, vocabulary consistency (existing pilot gaps explicitly outstanding), manifest freshness, frozen source bytes and **33 full-family mechanical re-extractions**, exact **91 local additions**, baseline metadata/readings/levels/exclusions/strokes with only preserved reviewed exceptions, sole テイ disposition/explicit no-kun, **two mapped reciprocal pairs/four links** including existing 探/探偵, both 刑事 comparison directions, pinned eleven-stroke conversion and all affected Han font cmaps. No fresh linguistic certification is claimed from mechanical checks.

Accepted **404 Android 3 RealContentTest + 1 RareHanTest, no skips**, **406 two native per-case terminal-0 results** and **407 exact cleanup recovery** independently reverified without reruns; runtime/tools are unchanged from accepted teaching. Full production ContentSync imported the complete archive **once**: **1,076 kanji / 5,034 words / 96 N1 cards**, zero problems, parser epoch1 and manifest `{VERSION}`. N1 selection, meaning feedback, sole curated on reading with persisted OnGood/no-kun, both mapped routes plus comparison routes/System Back/offline, eleven reference-touch strokes and recall miss/persisted DrawAgain retained. Meaning Back **before Next** is not a newly persisted grade; injected/synthetic progress is not owner history, MLKit or successful human recall evidence.

Both blind initials used different actual families (**claude-opus-5.5 / gpt-6.1-sol**) on one frozen draft: 45/44 calls, 30 assigned ranges each, no internal overlaps. **064-N1** is resolved by the exact link-only correction and both original-session confirmations. Historical **408/409/410 failures remain unaccepted**. User-authorized scoped411 `--add-dir control` restored each ORIGINAL reviewer's exact task read; serial dependent visual closure is not retroactive acceptance. Claude411 inspected six fresh images plus retained408 evidence; GPT411 inspected28. The claimed kun-cell dash is **withdrawn** (sole on row; gloss punctuation), universal paragraph/footer visibility is **narrowed**, not certified. Clipped/unseen pixels and actual fallback face remain unverified; source1080x2400/model900x2000 images preserved. The four font rows show readable, distinguishable 偵/貞/停/低/値/人/亻/探/手/扌; all40-target pilot evidence is inherited honestly.

Original403/406 denials and exact parent recoveries are preserved.407 found a nonempty remote5581 connection, **not all ports free**; future native launches require fresh full local+remote port ownership checks. Qualified historical049 HOST-only heap/OOM evidence is unchanged; no guest/app heap, archive guards or permissions changed.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) are green. **Both immutable public ZIPs verify all 8,320 runtime hashes** and equal manifest `{VERSION}`. Terminal archive: **{archive['zipEntries']:,} entries / {archive['compressedBytes']:,} compressed / {archive['inflatedBytes']:,} inflated / {archive['retainedBytes']:,} retained bytes**; unchanged18,000-entry/42-MiB/80-MiB/56-MiB guards pass; contributor evidence excluded.

Published **91/1,228 additions; 1,137 remain**. Current **1,076 kanji / 5,034 words / 96 N1-labelled / 95 named-source members plus separate 妖**. One necessary support word this batch;92 project-wide, **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; physical-phone/general-release/whole-set acceptance **outstanding**. Durable evidence: `docs/n1-sources/batch-064-publication.json`, `batch-064-acceptance-audit.json`, `execution-412.json`, original source/review/native records. Checkpoint412 persists `continue` and yields before065; no065/second runner started.
"""
    path = C / "batch-064-publication-comment.txt"
    assert not path.exists()
    path.write_text(text, encoding="utf-8")
    print("Exact verified terminal issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(C / "execution-412-starting-progress.json")
    receipt = load(C / "batch-064-publication-issue-receipt.json")
    body = (C / "batch-064-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-065-progress.json").exists()
    publication = load(S / "batch-064-publication.json")
    next_action = (
        f"Batch064 accepted/published/verified at {head}; fresh coordinator yield before065. Read complete request/finalcheckpoint and scoped live keys, preserve FULL live history. Verify dedicated clean signed heads/latestmain, then ONE risk/evidence-bounded065 below15 from exact remaining frozen source rows. Preserve baseline identities/levels/fullreadings/order/exclusions and reviewed虎[酔っ払い]/猿[馬鹿]/丘[坂,山]/山[川,出,木]guards. Inspect full applicable dictionary families/necessarysupport/curatedreadings/allactivated+reciprocalpairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one active reviewer/onecallperresponse/serialinternaltools, scoped --add-dir control path preflight and originalcwd/read-only tools; bounded original-session confirmations only as needed. Applicable fresh non-skippedAndroid/native/currentmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
        "Public91/1228,1137remain;1076kanji/5034words/96N1labels/95namedmembers plus separate妖;92necessarysupportword additions, NOTN1vocabulary. "
        + publication["limits"] +
        " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. New denial preserve/report/yield. Overall task incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=412, status="continue", stage="batch-064-published-verified-before-065",
             lastPublishedCommit=head, remainingAdditions=1137, blocker=None, nextAction=next_action)
    p["batch064PublicationCheckpoint"] = publication
    p["activeExecution"].update(status="bounded-publication-checkpoint-complete", savedCommit=head,
                               issueUpdate=receipt["html_url"], recordedAt=now())
    p["execution412CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
    p["execution412StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1137source-bounded additions not authored/review-closed/published; later batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
    allowed = {"activeExecution", "checkpoint", "status", "stage", "lastPublishedCommit",
               "remainingAdditions", "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 412, "checkpoint": 412, "batch": "064",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 368, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8320,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "publishedAdditions": 91, "remainingAdditions": 1137,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "verifiedAt": now(),
    }
    save(C / "execution-412-final-verification.json", result)
    save(C / "batch-064-publication-checkpoint.json", publication)
    p["execution412CoordinatorCheckpoint"]["verification"] = result
    save(C / "progress.json", p)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"start": start, "source-audit": source_audit, "validate": validate,
     "evidence": evidence, "publication-records": publication_records,
     "comment": comment, "finish": finish}[sys.argv[1]]()
