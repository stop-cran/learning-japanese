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
D = S / "batch-066-acceptance"
L = C / "logs" / "4c99dde2-9bea-4e53-9990-f88882257dbb"
BASE = "44645f54b3fadb4b792b91c12a895ebf9f495d4e"
START = "f43e6ea06e480406292a618db564e963dd1e1701"
TEACHING = "6c23db00d2d14ec6d0a3537a1ef72b273e3d55e7"
VERSION = "a9ecc100b6c1335c"
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
    temporary = path.with_suffix(path.suffix + ".execution429.tmp")
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
    assert p["checkpoint"] == 428 and git("rev-parse", "HEAD") == START
    assert not git("status", "--porcelain")
    unchanged()
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == p["checkpoint"]
    assert not (L / "before-progress-execution429.json").exists()
    save(L / "before-progress-execution429.json", p)
    p["execution429StartingState"] = {
        "execution": 429, "batch": "066", "startingHead": START,
        "scope": "SAME066 latest-main combined acceptance, normal signed owner fast-forward publication, exact CI/public ZIP acceptance and durable checkpoint; no067, duplicate reviewers/Android/native or second runner.",
        "status": "combined-acceptance-started",
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final428 and complete approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
        },
        "originMain": git("rev-parse", "origin/main"), "recordedAt": now(),
    }
    p["stage"] = "batch-066-combined-current-main-acceptance"
    p["nextAction"] = p["execution429StartingState"]["scope"]
    save(C / "progress.json", p)
    print("Execution429 starting scope saved; complete live history preserved.")


def source_audit():
    unchanged()
    spec = importlib.util.spec_from_file_location("source422", C / "execution-422.py")
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    snapshot = source.inputs()
    ledger = load(S / "batch-066-progress.json")
    result = audit(R, "066")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    packets = []
    for kind, ids in source.groups(dictionary).items():
        name = "batch-066-jmdict.xml" if kind == "lexical" else "batch-066-comparison-jmdict.xml"
        assert load(S / f"batch-066-{kind}-selection.json")["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert set(ids) == {i for row in ledger[f"{kind}Dispositions"] for i in row["entries"]}
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert sum(row["families"] for row in packets) == 47
    assert (S / "batch-066-kanjidic2.xml").read_bytes() == source.raw_metadata()
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
        if int(row["batch"]) <= 66:
            assert not expected & set(row["membership"])
            assert row["reviewClosed"] == row["membership"]
            if int(row["batch"]) < 66:
                assert row["published"] == row["membership"]
            expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - original == expected and len(expected) == 93 and original <= current
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
    assert len(named) == len(set(named)) == 1232 and named[74] == "僚"
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
    assert sum(maps.values()) == 8326
    pairs = [("僚", "words/同僚.md"), ("同", "words/同僚.md")]
    for char, word in pairs:
        assert f"(../kanji/{char}.md)" in (R / word).read_text(encoding="utf-8")
        assert f"(../{word})" in (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
    geometry = load(S / "batch-066-stroke-evidence.json")
    svg_path = C / "inputs" / "n1-050da-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "僚.json") == convert("僚", svg.decode("utf-8"))
    assert sha(R / "strokes" / "僚.json") == geometry["targetSha256"]
    articles = ["kanji/僚.md", "words/同僚.md", "kanji/同.md"]
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
    assert actual_counts == {"kanji": 1078, "words": 5036, "n1Labelled": 98, "namedSourceMembersPresent": 97}
    result.update(
        execution=429, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDictionaryFamilies=47,
        dictionaryPackets=packets, runtimePayloadHashesVerified=8326, manifestMaps=maps,
        allMappedReciprocalPairs=2, mappedDirectedLinks=4, actualCounts=actual_counts,
        actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test.",
    )
    save(S / "batch-066-acceptance-source-audit.json", result)
    print("Frozen sources/47families/baseline/93additions/8326hashes/2pairs/geometry/cmaps/budgets passed.")


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
        path = L / f"execution-429-{name}.txt"
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
        save(C / "artifacts" / "execution-429-validation-receipts.json", receipts)
        print(f"{name}: exit {result.returncode}", flush=True)
        if result.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(result.returncode)


def evidence():
    unchanged()
    textual = load(V / "batch-066-reconciliation.json")
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
    visual = load(V / "batch-066-visual-reconciliation.json")
    record428 = load(S / "execution-428.json")
    assert sha(V / "batch-066-visual-reconciliation.json") == record428["reconciliationSha256"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert visual["allReviewerProcessesSerialAndExited"] and visual["allInternalReadsSerial"]
    reviews = list(record428["reviews"].values())
    for row in reviews:
        assert row["exitCode"] == 0 and row["processAndCoverageAccepted"] and row["returnedImages"] == 19
        assert sha(R / row["report"]) == row["reportSha256"]
        assert sha(R / row["execution"]) == row["executionSha256"]
    assert datetime.fromisoformat(reviews[0]["completedAt"]) < datetime.fromisoformat(reviews[1]["startedAt"])
    android = load(S / "execution-425.json")
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
    native = load(S / "execution-427.json")
    assert sha(R / native["artifactIndex"]) == native["artifactIndexSha256"]
    index = load(R / native["artifactIndex"])
    for row in index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
    raw = V / "batch-066-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-066-native" / "attempt-1" / "n1-066-article-route.json")
    assert route == native["nativeRouteEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1078, 5036, 98, 0]
    assert route["acceptedReadingParserEpoch"] == 1 and route["quizOnKeys"] == ["りょう"] and route["quizKunKeys"] == []
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(C / "artifacts" / "execution-429-validation-receipts.json")
    assert len(receipts) == 6 and all(row["exitCode"] == 0 for row in receipts)
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    summary = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                        (L / "execution-429-python-tests.txt").read_text(encoding="utf-8"))
    assert summary and int(summary[1]) == 368
    result = load(S / "batch-066-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"),
        latestMainIntegrated=git("rev-parse", "origin/main"),
        normalMergeResult="Already up to date; no substantive teaching or tool changes.",
        pythonTests={"passed": 368, "failures": 0, "errors": 0}, validationReceipts=receipts,
        acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(index["files"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        textualReconciliationSha256=sha(V / "batch-066-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-066-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-425.json"), nativeEvidenceSha256=sha(S / "execution-427.json"),
        limits=(
            "Bounded owner-testing only; physical-phone/general-release/whole-set outstanding. Compatible Androidf9b59a2+ required. "
            "Original two-family textual reports, source/lookup/read-depth/gaiji limits and optional decisions retained. "
            "Both original-session visual confirmations serial:19 distinct scenes each/38 actual returned900x2000payloads, not41distinct captures. "
            "No established actionable defect; unseen viewport/table regions and actual fallback faces unverified. "
            "Claude same-sans Mincho description withdrawn; original fallback inference corrected. Actual meaning choices were wrong for僚 "
            "but differ from authored療/像/値, whose native presentation is NOT certified. "
            "Accepted425 HOST Android3+1 and427 native2terminal0/93.971s independently reverified, not rerun. "
            "Exact full archive productionContentSyncONCE1078kanji5036words98N1/problems0/epoch1; sole normalizedりょう Good/noKunLog, "
            "two mapped pairs/four directions, full3articles/SystemBack/offline/N1selection/meaning/14reference-touch strokes/ungradedtrace/"
            "recallmiss/persistedDrawAgain. Not MLKit, human successful recall, ownerprogress or phone evidence. "
            "Four readable production font rows do not identify fallback face or every-phone readability. "
            "Original permission denials/HOST512MiB+1GiB OOMs retained; qualified HOST-only2GiB init NEVER used in native. "
            "No production, app/guest heap, guard or permission changes. Latestmain ancestral and runtime/tools unchanged; "
            "no duplicate reviewer/Android/native required. Vocabulary pilot gaps retained, not repaired or counted complete. "
            "Zero new support words in066;94 project additions are necessary supports, not an N1 vocabulary deck."
        ),
    )
    save(S / "batch-066-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    shutil.copyfile(Path(__file__), D / Path(__file__).name)
    p = load(C / "progress.json")
    save(S / "execution-429.json", {
        "schemaVersion": 1, **p["execution429StartingState"], "status": result["status"],
        "acceptanceRecord": "batch-066-acceptance-audit.json",
        "publishedAdditions": 92, "remainingAdditions": 1136, "localDraftAdditions": 93,
        "limits": result["limits"], "nextAction": "Normal signed acceptance/ownerfastforward/greenCI/every immutable ZIP hash; terminal evidence/CI/ZIP/ownerissue60 then yield before067.",
    })
    p["stage"] = "batch-066-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and exact inherited evidence archived; publication pending.")


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-066-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION and archive["verifiedRuntimeHashes"] == 8326
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    audit_record = load(S / "batch-066-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 429, "batch": "066", "membership": ["僚"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": "4c0a3b6f28b99984cc5cd245c763852e204d8e7f",
        "visualClosureSnapshot": START, "latestMainIntegrated": audit_record["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-066-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-066-visual-reconciliation.json",
        "validation": audit_record, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 93, "remainingAdditions": 1135,
            "currentKanji": 1078, "currentWords": 5036, "n1Labelled": 98, "namedSourceMembersPresent": 97,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 0,
            "projectNewNecessarySupportWords": 94, "batchChangedReusedArticles": 2,
            "requiredReciprocalPairs": 2, "activatedBaselinePairs": 1,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": audit_record["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/ownerissue60; checkpoint and yield before067.",
    }
    assert not (S / "batch-066-publication.json").exists()
    save(S / "batch-066-publication.json", publication)
    ledger = load(S / "batch-066-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=93, remainingAdditions=1135, publishedCommit=head,
        publicationRecord="batch-066-publication.json", acceptanceRecord="batch-066-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-066-progress.json", ledger)
    execution = load(S / "execution-429.json")
    execution.update(status=publication["status"], publicationRecord="batch-066-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-429.json", execution)
    for path in (C / "artifacts" / "batch-066-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 C / "verify-batch-066-publication.ps1", C / "verify-batch-002-publication.py",
                 C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-066-accepted-publication-verified-pending-terminal-evidence"
    p["execution429AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/greenCI/public8326hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-066-publication.json")
    text = f"""Batch **066 (僚)** is published and verified for **bounded owner testing**. Reuses existing **同僚** with a component link and **同** with a common-word backlink; **zero new support articles**.

Authored/reviewed teaching `{TEACHING}`, textual closure `{publication['textualClosureSnapshot']}`, bounded visual closure `{START}`. Fresh main `{publication['latestMainIntegrated']}` already ancestral; no substantive teaching/tools changed. Normally signed accepted/integrated publication `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Normal owner-scoped fast-forward, global romanko-ms unchanged.

Fresh combined gates: **368 Python tests**, validator, vocabulary consistency (**2,122/2,431 pilot prompts**, not complete coverage), regenerated fresh manifest; exact frozen inputs/**47 full-family mechanical re-extractions**, exact **93 additions**, baseline **985 kanji/4,942 words/985 strokes** with only preserved reviewed exceptions, source readings/order/curation, **two mapped reciprocal pairs/four directed links** including the activated baseline pair, reproduced14-stroke pinned geometry, affected Han cmaps and original archive budgets. Mechanical hashes do not establish linguistic comprehension.

Both blind initial families (**claude-opus-5.5 / gpt-6.1-sol**) reviewed the same signed snapshot/three teaching scopes/three facets. Both original-session visual confirmations were fully serial, **19 distinct scenes per family /38 actual900x2000 image payloads** from41 source capture names; original reports/source/read-depth/lookup limits retained. No actionable defect established. Claude's same-sans Mincho description is withdrawn; actual fallback faces remain unidentified. Its original no-filler inference is corrected: observed N1 meaning options differ from authored 療/像/値 and are visibly wrong for僚; **native presentation of those authored choices is not certified**. Unseen viewport/table regions and whole-row simultaneous visibility remain unverified.

Accepted **425 fresh Android3 RealContentTest+1 RareHanTest/no skips** and **427 two native terminalcase0/93.971s** independently reverified, not rerun. Exact full archive through productionContentSync **once**: **1,078kanji/5,036words/98N1**, problems0, `{VERSION}`, epoch1. Full+Liteリョウ/emptyKun; sole normalizedりょう Good persisted/noKunLog; both mapped pairs/four directions, three complete article semantics/SystemBack/offline/N1selection/meaning/14reference-touch strokes/ungradedtrace/recallmiss/persistedDrawAgain. Four production rows readable/distinguishable for僚療像値人亻疒同口/同僚. Not MLKit, successful human recall, ownerprogress, fallback-face identification or phone evidence.

Historical denials and HOST512MiB/1GiB OOMs preserved; qualified **HOST-only2GiB** init NEVER used in native. No app/guest heap, production guard, permissions or app code changed. Owned427helpers stopped; unrelated shared emulator preserved. No redundant reviewers/Gradle/native runs.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,326 runtime hash** and manifest `{VERSION}`. Terminal **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes** pass unchanged18,000entries/42MiB/80MiB/56MiB; contributor evidence excluded.

Published **93/1,228 additions;1,135 remain**. Current **1,078kanji/5,036words/98N1-labelled/97named-source members plus separate妖**. Project94 necessary support additions are **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required. **Physical-phone/general-release/whole-set acceptance outstanding**. Durable `docs/n1-sources/batch-066-publication.json`, `batch-066-acceptance-audit.json`, `execution-429.json` and original source/review/native records retained. Checkpoint429 saves `continue` and yields **before067**; no next batch or second runner.
"""
    path = C / "execution-429-issue-body.txt"
    assert not path.exists()
    path.write_text(text, encoding="utf-8")
    print("Exact terminal owner issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution429.json")
    receipt = load(C / "execution-429-issue-receipt.json")
    expected = (C / "execution-429-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-067-progress.json").exists()
    publication = load(S / "batch-066-publication.json")
    next_action = (
        f"Batch066 accepted/published/verified at {head}; yield before067. Read complete request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/freshmain, then ONE evidence-bounded067 source preparation below15 from exact remaining rows. "
        "Preserve exact source/baseline identities/levels/fullreading order/exclusions and documented虎/猿/丘/山 guards. "
        "Inspect complete applicable dictionary families, necessary support, practical curated reading rows, activated+allmapped reciprocal pairs, "
        "pinned strokes and every new Han font disposition. Two serial blind different-family initial reviewers, one active/serial internal tools, "
        "bounded original-session confirmations; applicable non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/every immutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. New denial preserve/report/yield. "
        "Public93/1228,1135remain;1078kanji5036words98N1labels97namedmembers plus妖;94support additions NOTN1vocabulary. "
        + publication["limits"] + " Overallproject incomplete."
    )
    publication.update(
        finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
        terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
        nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=429, status="continue", stage="batch-066-published-verified-before-067",
             lastPublishedCommit=head, remainingAdditions=1135, blocker=None, nextAction=next_action)
    p["batch066PublicationCheckpoint"] = publication
    p["execution429StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1135source-bounded additions not authored/review-closed/published; later batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 429, "checkpoint": 429, "batch": "066",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 368, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8326,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "publishedAdditions": 93, "remainingAdditions": 1135, "phoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "verifiedAt": now(),
    }
    save(C / "execution-429-final-verification.json", result)
    save(C / "batch-066-publication-checkpoint.json", publication)
    p["execution429CoordinatorCheckpoint"] = {**result, "status": "continue", "nextAction": next_action}
    p["batch066PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"start": start, "source-audit": source_audit, "validate": validate,
     "evidence": evidence, "records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
