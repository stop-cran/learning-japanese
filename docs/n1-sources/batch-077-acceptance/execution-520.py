"""Bounded batch077 combined-tree acceptance and publication checkpoint."""
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
L = C / "logs" / "bd0d00fd-cb92-446f-b0ef-63f5522ec4a7"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-077-acceptance"
BASE = "da5364e9cc72885b8fe08a4bf187e79721f595df"
START = "05a5e153314a94adaffed82d7c150e572a07577a"
TEACHING = "02877a257d6b265625e637e6a304fc8440ddd337"
VERSION = "2944928c13e2165a"
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
    temporary = path.with_suffix(path.suffix + ".execution520.tmp")
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
    assert p["checkpoint"] == 519 and p["status"] == "continue" and p["batch"] == "077"
    assert "execution520StartingState" not in p
    save(L / "progress-before-execution-520.json", p)
    request = (L / "request.txt").read_text(encoding="utf-8")
    p["execution520StartingState"] = {
        "execution": 520, "batch": "077", "startingHead": START, "freshOriginMain": BASE,
        "recordedAt": now(), "status": "combined-tree-acceptance-in-progress",
        "scope": "SAME077 combined-current-main acceptance and authorized publication if every gate passes; no next batch, reviewer/native rerun or second runner.",
        "authorization": {
            "requestSha256": sha(L / "request.txt"), "characters": len(request),
            "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and embedded checkpoint parsed; operative contract, final519 and complete approved issue inspected directly. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated content and Android clean; normally signed G heads05a5e153/f9b59a2. Fresh main da5364e9 already ancestral; no merge or teaching reconciliation needed. Canonical repositories not accessed.",
        "optionalHistoricalHelpersAccessed": False,
    }
    p["stage"] = "batch-077-combined-tree-acceptance-in-progress"
    save(C / "progress.json", p)
    print("Starting scope persisted; original full progress separately preserved.")


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
    ledger = load(S / "batch-077-progress.json")
    result = audit(R, "077")
    dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    full = ET.fromstring(gzip.decompress(dictionary))
    packets, distinct = [], set()
    comparison_ids = set(load(S / "batch-077-comparison-selection.json")["entryIds"])
    for kind in ("lexical", "comparison"):
        selection = load(S / f"batch-077-{kind}-selection.json")
        ids = [e.findtext("ent_seq") for e in full.findall("entry")
               if (any("冒" in k.text for k in e.findall("k_ele/keb")) if kind == "lexical"
                   else e.findtext("ent_seq") in comparison_ids)]
        name = "batch-077-jmdict.xml" if kind == "lexical" else "batch-077-comparison-jmdict.xml"
        assert selection["entryIds"] == ids
        assert (S / name).read_bytes() == extract(
            dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        distinct.update(ids)
        packets.append({"path": name, "families": len(ids), "sha256": sha(S / name)})
    assert [row["families"] for row in packets] == [29, 11] and len(distinct) == 40
    original = ET.fromstring(gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    packet = ET.parse(S / "batch-077-kanjidic2.xml").getroot()
    by_char = {e.findtext("literal"): e for e in original.findall("character")}
    assert len(packet.findall("character")) == 2
    assert normalized(packet.find("header")) == normalized(original.find("header"))
    assert all(normalized(e) == normalized(by_char[e.findtext("literal")]) for e in packet.findall("character"))
    for name in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"):
        assert (R / name).read_text(encoding="utf-8") == base_file(R, BASE, name)
    exceptions = load(S / "batch-076-acceptance-audit.json")["explicitInheritedMetadataExceptions"]
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
        assert int(row["batch"]) <= 77 and not expected & set(row["membership"])
        assert row["reviewClosed"] == row["membership"]
        if int(row["batch"]) < 77:
            assert row["published"] == row["membership"]
        expected.update(row["membership"])
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    assert current - old_chars == expected and len(expected) == 104 and old_chars <= current
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
    assert len(named) == len(set(named)) == 1232 and named[85] == "冒"
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
    assert sum(maps.values()) == 8358
    words = {row["article"]: metadata(R, row["article"]) for row in ledger["supportMappings"]}
    pairs = {(c, name) for name, meta in words.items() for c in meta["kanji"]
             if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 3
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        body = (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../{name})" in body and words[name]["reading"] in body
    draft = load(S / "batch-077-draft-audit.json")
    geometry = draft["geometry"]
    svg_path = Path(geometry["input"])
    svg = svg_path.read_bytes()
    assert sha(svg_path) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == geometry["converterNormalizedSha256"]
    assert load(R / "strokes" / "冒.json") == convert("冒", svg.decode("utf-8"))
    assert sha(R / "strokes" / "冒.json") == geometry["targetSha256"]
    font_audit = draft["actualAuthoredHanFonts"]
    articles = font_audit["articles"]
    han = sorted(set(c for c in "".join((R / name).read_text(encoding="utf-8") for name in articles)
                     if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                     or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    assert han == sorted(set(font_audit["characters"]) | {"攻"}) and len(han) == 39
    assert load(S / "execution-518.json")["glyphEvidence"]["currentRawScopedHan"] == len(han)
    fonts = []
    for row in font_audit["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == row["missingActualDraftHan"] == ["冂", "阝"]
        fonts.append({"path": str(path), "sha256": row["sha256"], "missing": missing})
    actual_counts = {
        "kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
        "namedSourceMembersPresent": len(current & set(named)),
    }
    assert actual_counts == {"kanji": 1089, "words": 5046, "n1Labelled": 109, "namedSourceMembersPresent": 108}
    result.update(
        execution=520, exactLocalAdditionMembership=sorted(expected),
        baselineMetadataAndStrokesChecked=counts, explicitInheritedMetadataExceptions=exceptions,
        newBaselineMetadataExceptions=[], frozenInputHashesVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, exactFrozenDistinctDictionaryFamilies=len(distinct),
        dictionaryFamilyOccurrences=40, dictionaryPackets=packets,
        completeRawCharacterRecordsVerified=2, runtimePayloadHashesVerified=8358, manifestMaps=maps,
        allMappedReciprocalPairs=3, mappedDirectedLinks=6, unavailableDeclaredComponents=[],
        actualCounts=actual_counts, actualHanFontCmaps={"articles": articles, "characters": han, "fonts": fonts},
        generatedGeometryReproducedExactly=True, budget=check(R, archive_names(R)),
        freshLinguisticReviewClaimed=False,
        limits="Fresh mechanical source/family/baseline/membership/readings/quiz/link/geometry/cmap/manifest/budget audit, not a fresh linguistic review or native test. Comparison family membership retained from reviewed committed selection, not newly semantically selected.",
    )
    save(S / "batch-077-acceptance-source-audit.json", result)
    print("40families/2rawrecords/baseline/104localadditions/8358hashes/3pairs/geometry/cmaps/budgets passed.")


def evidence():
    unchanged()
    textual = load(V / "batch-077-reconciliation.json")
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
    visual = load(V / "batch-077-visual-reconciliation.json")
    record519 = load(S / "execution-519.json")
    assert sha(V / "batch-077-visual-reconciliation.json") == record519["reconciliationSha256"]
    assert visual["bothOriginalSessionProcessesSerialAndExited"]
    assert visual["boundedIndependentVisualConfirmation"] and not visual["findings"]
    assert visual["bothVisualExecutionsInternallySerial"]
    assert [visual[k] for k in ("sourceCaptures", "uniqueAssignedCaptures", "hashMappedDuplicateCaptures")] == [54, 33, 21]
    visual_processes = list(visual["reviews"].values())
    for row in visual_processes:
        assert row["exitCode"] == 0 and row["processAndCoverageAccepted"]
        assert sha(R / row["report"]) == row["reportSha256"]
        assert (R / row["execution"]).is_file()
    for first, second in zip(visual_processes, visual_processes[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    for row in record519["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    android = load(S / "execution-516.json")
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
    native = load(S / "execution-518.json")
    for row in native["artifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    raw = V / "batch-077-native" / "attempt-1" / "instrumentation.txt"
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                      raw.read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
    route = load(V / "batch-077-native" / "attempt-1" / "n1-077-article-route.json")
    assert route == native["routeEvidence"]
    assert route["archiveRequests"] == 1 and route["contentVersion"] == VERSION
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems")] == [1089, 5046, 109, 0]
    assert route["acceptedReadingParserEpoch"] == 1
    assert route["fullOnyomi"] == route["fullProjectionQuizOnyomi"] == route["liteQuizOnyomi"] == ["ボウ"]
    assert route["fullKunyomi"] == route["fullProjectionQuizKunyomi"] == route["liteQuizKunyomi"] == ["おか.す"]
    assert route["quizOnKeys"] == ["ぼう"] and route["quizKunKeys"] == ["おかす"]
    assert route["bothCuratedKindsPersistedGoodAndDone"]
    assert route["mappedReciprocalPairs"] == 3 and route["directedLinkTransitions"] == 6
    assert route["offline"] and route["passed"] and not route["phoneEvidence"]
    assert native["nativeExecution"]["terminalSuccessCases"] == 2 and native["nativeSkippedCases"] == 0
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    receipts = load(L / "execution-520-validation-receipts.json")
    latest = {row["check"]: row for row in receipts}
    assert len(latest) == 6 and all(row["exitCode"] == 0 for row in latest.values())
    for row in receipts:
        assert sha(Path(row["log"])) == row["sha256"]
    tests = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK(?:\s|$)",
                      (L / "execution-520-python-tests.txt").read_text(encoding="utf-8"))
    assert tests and int(tests[1]) == 372
    limits = (
        "Two independent blind textual families and bounded dependent original-session visual confirmations retained, "
        "not fresh upstream retrieval/native-speaker certification. Visual processes and internal reads serial/exited; "
        "33uniquePNGgroups/54originals/21exact-bytealiases per reviewer, source1080x2400/toolreturned900x2000. "
        "All39Han/fourfamilies/twowords readable in bounded captures; fallbackface/physicalphone unknown. "
        "Original攻める safeguard disagreement, optionalおかlure hypothesis, alias/lastloadingtree limits preserved. "
        "HOST5163+1/native518two namedterminal0/zeroskips retained and hashes/provenance reverified, not rerun. "
        "ProductionContentSyncONCE full46dff146 archive1089kanji5046words109N1/problems0/epoch1; actualぼうおかすGood/Done2. "
        "Meaning actual stackmatechoices, NOT newlyexercised authored日目官; textualchoicesaudit retained. "
        "Nine reference-touchstrokes/ungradedtrace/recallAgain are NOT humanhandwriting/successfulrecall/MLKit. "
        "All3mappedpairs6directions/SystemBack/offline supplied; stills not gestures/restartdurability. "
        "Fresh vocabulary consistency2122/2431 reviewedpilotprompts, not full coverage. "
        "Historicalsource/review/process/denial/OOM/failedlookup/readdepthlimitations and reviewed虎/猿/丘/山exceptions remain. "
        "HOST-only2GiBinit NEVER enters native. No runtime/app/tool/heap/guard/permission/algorithm changes or078. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
        "Bounded owner testing only; historical pending-gate statements remain historical."
    )
    result = load(S / "batch-077-acceptance-source-audit.json")
    result.update(
        status="combined-tree-locally-accepted-pending-publication", recordedAt=now(),
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh main already ancestral; no substantive teaching or tool changes.",
        pythonTests={"passed": 372, "failures": 0, "errors": 0, "skipped": 0},
        validationReceipts=receipts, acceptedAndroidCasesReverified=4, acceptedNativeTerminalCasesReverified=2,
        validationRecovery="Initial acceptance recipe compared current39rawHan with historical38draftHan; assertion stopped. Corrected to historical38 plus reviewed metadata-only攻, matching518native and519visual inventories. Failed receipt retained; only failed/unrun gates rerun. No teaching or source changes.",
        acceptedAndroidNativeReviewerRerun=False, nativeArtifactHashesReverified=len(native["artifacts"]),
        visualArtifactHashesReverified=len(record519["artifacts"]),
        reviewedRuntimeAndToolsUnchanged=True, boundedDependentVisualAcceptance=True,
        historicalProcessDeviationsPreserved=True,
        textualReconciliationSha256=sha(V / "batch-077-reconciliation.json"),
        visualAcceptanceSha256=sha(V / "batch-077-visual-reconciliation.json"),
        androidEvidenceSha256=sha(S / "execution-516.json"), nativeEvidenceSha256=sha(S / "execution-518.json"),
        limits=limits,
    )
    save(S / "batch-077-acceptance-audit.json", result)
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "verify-batch-002-publication.py", C / "push-batch-060.ps1"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    save(S / "execution-520.json", {
        "schemaVersion": 1, **p["execution520StartingState"], "recordedAt": now(),
        "status": result["status"], "acceptanceRecord": "batch-077-acceptance-audit.json",
        "publishedAdditions": 103, "remainingAdditions": 1125, "localReviewClosedAdditions": 104,
        "limits": limits, "nextAction": "Normal signed acceptance, owner fast-forward, exact green CI/public ZIP then terminal evidence/owner issue60; yield before078.",
    })
    p["stage"] = "batch-077-combined-tree-accepted-pending-signing"
    save(C / "progress.json", p)
    print("Combined acceptance and inherited evidence archived; publication pending.")


def verified(phase, recovering_records=False):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G"
    dirty = git("status", "--porcelain")
    assert not dirty or recovering_records and dirty == "?? docs/n1-sources/batch-077-publication.json"
    ci = load(C / "artifacts" / f"batch-077-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8358
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted", recovering_records=True)
    acceptance = load(S / "batch-077-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 520, "batch": "077", "membership": ["冒"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": BASE, "authoredSnapshot": "0d6fe29033157a4417def2b503ad3d02e7cb43da",
        "reviewedTeachingSnapshot": TEACHING, "textualClosureSnapshot": TEACHING,
        "freshAndroidSnapshot": "772463c4c0f58b66482e6ee8b6d73d7a7b1a8bf7",
        "nativeEnvelopeSnapshot": "46dff1466ac9f3cf64b54e197c05088414939896",
        "nativeEvidenceSnapshot": "45191e3dcdee657fd872a8c416227480b95cbc3e",
        "visualClosureSnapshot": START, "latestMainIntegrated": BASE,
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-077-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-077-visual-reconciliation.json",
        "validation": acceptance, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 104, "remainingAdditions": 1124,
            "currentKanji": 1089, "currentWords": 5046, "n1Labelled": 109, "namedSourceMembersPresent": 108,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 104, "batchChangedReusedArticles": 2,
            "requiredReciprocalPairs": 3, "activatedBaselinePairs": 1,
        },
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": acceptance["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/owner issue60; checkpoint and yield before078.",
    }
    publication_path = S / "batch-077-publication.json"
    if publication_path.exists():
        previous = load(publication_path)
        assert {k: v for k, v in previous.items() if k != "recordedAt"} == {
            k: v for k, v in publication.items() if k != "recordedAt"}
        publication = previous
    else:
        save(publication_path, publication)
    ledger = load(S / "batch-077-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "nextGate", "limits", "remainingGates")
        if key in ledger}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=104, remainingAdditions=1124, publishedCommit=head,
        publicationRecord="batch-077-publication.json", acceptanceRecord="batch-077-acceptance-audit.json",
        remainingGates="Terminal evidence publication/CI/public ZIP/owner issue update; physicalphone/generalrelease/whole-set outstanding.",
        nextAction=publication["nextAction"],
        nextGate="Terminal publication receipts and owner issue update, then yield before078.",
        limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-077-progress.json", ledger)
    execution = load(S / "execution-520.json")
    execution.update(status=publication["status"], publishedAdditions=104, remainingAdditions=1124,
                     publicationRecord="batch-077-publication.json",
                     publicationRecipeRecovery="First records operation saved verified publication, then KeyError on absent optional remainingGates before changing ledger. Preserved original publication, verified its exact payload, and preserved only fields actually present in prePublicationCheckpoint. No content/acceptance gate changed.",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-520.json", execution)
    for path in (C / "artifacts" / "batch-077-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 L / "execution-520-accepted-push.txt", C / "verify-execution-520.ps1",
                 C / "post-execution-520.ps1", Path(__file__)):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-077-accepted-publication-verified-pending-terminal-evidence"
    p["execution520AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/green CI/public8358hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-077-publication.json")
    body = f"""**Batch 077 (冒) is published and verified for bounded owner testing.** Necessary support **冒す (おかす)** added; existing **冒険 (ぼうけん)** retains its N3 word level. Only two exact navigation changes in 冒険 and older 険. All **three mapped reciprocal pairs /six directions**, one activated baseline pair, present. No inferred vocabulary level or batch078.

Authored `{publication['authoredSnapshot']}`; textually corrected/review-closed `{TEACHING}`; fresh Android `{publication['freshAndroidSnapshot']}`; native evidence `{publication['nativeEvidenceSnapshot']}`; visual closure `{START}`. Fresh main `{BASE}` already ancestral: no substantive teaching/tool integration changes. Normally signed accepted/integrated runtime `{publication['acceptedCommit']}`, terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged.

Fresh combined gates: **372 Python tests, no skips**, validator, vocabulary consistency (**2,122/2,431 reviewed pilot prompts**, not full coverage), fresh manifest `{VERSION}`, five frozen inputs and **40 distinct complete JMdict families** (29 lexical/11 comparison), two raw character records. Exact **104 additions** and original **985kanji /4,942words /985strokes** baseline preserved, only inherited reviewed 虎/猿/丘/山 metadata exceptions. Both reading dispositions, pinned nine-stroke geometry, three mapped pairs/six directions, all39actual scoped Han cmaps and **8,358 runtime hashes** reverified. Raw and selected **ボウ /おか.す** retain source order and offer **ぼう /おかす**. An initial local acceptance-recipe assertion compared current39Han to historical38; corrected to include reviewed metadata-only攻, consistent with native/visual inventories. Failed receipt retained; only failed/unrun gates rerun; no teaching correction.

Blind initial **claude-opus-5.5 /gpt-6.1-sol** reviewed one frozen teaching snapshot, complete source packet, both full new articles and exact changed reused passages, all three facets. All four initial/confirmation processes and internal reads serial. One minor conservative direct **攻める** label safeguard resolved and confirmed by both original sessions. GPT's disagreement that the original absence was necessarily defective remains explicit; no unrestricted synonym rule or proven live defect inferred. No consequential unresolved scoped teaching defect.

Dependent original-session visual519 confirmations: both processes exited serially, internally serial, each complete common source/fixture packet plus **33uniquePNGgroups /54originals /21exact-bytealiases**. Actual model-visible payloads **900x2000**, NOT original1080x2400; returned bytes preserved. All39Han/four production families/focused冒日目官冂阜阝険犯侵 and冒険/冒す legible in bounded captures. No actionable teaching/rendering defect established. Actual fallback face unknown; physical-phone rendering unverified. Optionalおかlure hypothesis, alias and final loading-tree limits preserved. Hashes/access are not comprehension, gestures, everyviewport or phone evidence.

Accepted516 **RealContentTest3 +RareHanTest1, no skips**, and518 native attempt1 **two named terminal-status-0 cases**, no skips, hashes/provenance reverified, not rerun. Production **ContentSync ONCE** imports complete signed46dff146 Git envelope: **1,089kanji /5,046words /109N1**, problems0, epoch1. Full/Lite raw and curatedボウ/おか.す agree; actualぼう/おかす each persistGood/Done2correct without duplicate logs. All3mappedpairs6directions/SystemBack/offline/N1selection/meaningfeedback/nine reference-touch strokes/ungradedtrace then recallAgain pass. Actual meaning choices were stackmates, NOT newly exercised authored日目官; textualchoicesaudit retained. No human handwriting/MLKit/successful recall/model download/reviewer gestures or restart durability claimed. Owned5580parent27684/QEMU23940 stopped; shared5556 untouched. Historical denials/failures/OOMs retained; HOST-only2GiBinit NEVER used for native; no production/guest heap, guard, permission or algorithm changes.

Accepted [CI {publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal [CI {ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,358runtime hash**, exact manifest, safe paths/per-file limits and contributor evidence exclusion. Terminal ZIP SHA256 `{archive['sha256']}`: **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes**, within unchanged18,000entries/42MiB/80MiB/56MiB guards.

Published **104/1,228 additions;1,124 remain**. Current **1,089kanji /5,046words /109N1-labelled /108named-source members plus separate妖**. The104necessary support articles are **not N1 vocabulary expansion**. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; **physical-phone/general-release/whole-set acceptance outstanding**.

Durable `docs/n1-sources/batch-077-publication.json`, `batch-077-acceptance-audit.json`, `execution-520.json`, updated authoring notes and complete original source/review/native records retained. Exact terminal receipts in control. Checkpoint520 **continue**; yield before one bounded078source-preparation checkpoint. Overall project incomplete.
"""
    path = L / "issue-520-body.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    print("Exact terminal owner issue body prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "progress-before-execution-520.json")
    assert original["checkpoint"] == 519
    receipt = load(L / "issue-520-verified.json")
    expected_body = (L / "issue-520-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected_body.replace("\r\n", "\n").rstrip()
    publication = load(S / "batch-077-publication.json")
    next_action = (
        f"Batch077 fully published/terminal CI/public ZIP/owner issue verified at {head}; yield before078. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/fresh main, then ONE evidence-bounded078source-preparation checkpoint below15 "
        "from exact remaining source rows. No runtime draft or later gates in that source checkpoint. "
        "Use committed source packets and approved workspace inputs; reusable helpers belong in control. "
        "Optional prior-session recipes are NOT required evidence; do not request/access historical session-state paths. "
        "Preserve frozen sources/baseline identities/levels/fullreading order/exclusions and reviewed虎/猿/丘/山 exceptions; "
        "inspect complete applicable dictionary families, actual necessary support, every reading disposition/practical curated row, "
        "activated and all-mapped reciprocal pairs, pinned strokes and every newHan font disposition. "
        "Later stages retain two serial blind different-family reviewers/serial internal tools/bounded confirmations/"
        "non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Preserve/report/yield on actualnewdenials. "
        "Published104/1228,remaining1124;1089kanji5046words109N1labels108namedmembers plus妖;104necessarysupports NOTN1vocabulary. "
        "Inherit515textual two-family closure with077-C1conservative攻める safeguard resolved/bothconfirmations and originaldisagreement preserved,"
        "516HOST3+1/no skips,518native2terminal0,519boundedvisual closure; no redundant heavy work absentnewconcern. "
        "Bothvisualreviewerprocesses exited serially/internallyserial; each33uniquePNGgroups/54originals/21exact-bytealiases; "
        "900x2000returned vs1080x2400source; all39Han/fourfamilies/twowords readable, fallbackface unknown. "
        "Optionalおかlure/alias/finalloadingtree limits retained. Nine reference-touchstrokes/ungradedtrace/recallAgain "
        "NOT humanhandwriting/successfulrecall/MLKit; actualmeaningstackmates NOT authored日目官nativeexercise. "
        "Preserve originals/source-and-readdepthlimits/sidewaysviewport/MLKit/humanrecall/"
        "HOST-only2GiBinitNEVERnativebuilds/historicaldenials/OOMs/full livehistory. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       batchFinalizationComplete=True, nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=520, status="continue", stage="batch-077-published-verified-before-078",
             lastPublishedCommit=head, remainingAdditions=1124, blocker=None, nextAction=next_action)
    p["batch077PublicationCheckpoint"] = publication
    p["execution520StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1124source-bounded additions not authored/review-closed/published; later batches retain all source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 520, "checkpoint": 520, "batch": "077",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 372, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8358,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalRootKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 104, "remainingAdditions": 1124, "runtimePublished": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "verifiedAt": now(), "nextAction": next_action, "status": "continue",
    }
    save(L / "execution-520-final-verification.json", result)
    save(L / "batch-077-publication-checkpoint.json", publication)
    p["execution520CoordinatorCheckpoint"] = result
    p["batch077PublicationIssueReceipt"] = {
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
    target = L / "execution-520-validation-receipts.json"
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
        path = L / f"execution-520-{name}{suffix}.txt"
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
