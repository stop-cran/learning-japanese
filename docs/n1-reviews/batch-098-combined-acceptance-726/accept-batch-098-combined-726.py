"""Bounded combined-tree acceptance; the live launcher retains runner.lock."""
import ast
import base64
import contextlib
import gzip
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
L = C / "logs" / "f0ae3615-c944-4c7b-ab43-0e04e37c678f"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
HEAD = "844c3df127d94e369f48725805000632e46b6e68"
MAIN = "69af99e5d7bf34b093959d90dddc7d59fe6393b5"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "0cbdc2723b0433f2"
STAGE = "batch-098-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME098 publication only next. Read docs/n1-sources/execution-726.json and "
    "docs/n1-reviews/batch-098-combined-acceptance-726.json at signed LOCAL "
    "review-closed checkpoint. Fresh main69af99e5 already ancestor; normal merge "
    "Already up to date, ZERO incoming/runtime/teaching changes. All8449 runtime "
    "hashes/version0cbdc2723b0433f2 equal native724 full archivecefedeb6: "
    "productionContentSync ONCE/1121kanji5073words130N1/zeroProblems/Roomepoch1/"
    "TWOterminalcase0/noskips. Native724 and original-session725 rendered "
    "confirmations inherited, NOT fresh native/phone/newblindcredit. Fresh726 "
    "fullPython/validate/manifest/vocabulary/budget/frozensources/fullbaseline/"
    "allreadings/pinnedstrokes/TWOallmappedpairsFOURdirections/ONEactivatedbaseline/"
    "fontprovenance and FOURAndroidRealContentTHREE+RareHanONE/noskips passed. "
    "Complete剤 and exact reused洗剤:28/洗:38 reviewed; no new support word. "
    "Onlyonざい/Good/Done1of1/NOkun; fullザイスイセイandかるけず.る retained "
    "with explicit[ザイ]/[]. ONEpreserved洗剤せっけんwordguard/NONEnew. "
    "ActualN1 choices剤 vs剛/冶/刑: ONEcurated/TWOfallbacks, NOT済/則. "
    "Bounded64kanji/128word records CLEAN, unrestricted/future/custom "
    "semantic safety UNVERIFIED, no whole-pool certification. Both original "
    "reviewers25serialviews/23PNG each; THREEfourfontpanels/all19Han, "
    "12contactsheets45routes+8originalresolutionroutes;48PNGs NOT48original "
    "views. 刂/氵 visible, exactfallbackfaceunidentified; tool resizing retained. "
    "TENinjectedstrokes/trace+giveuprecall NOT humanhandwriting/MLKit/phone. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. "
    "Fetch latestoriginmain before publication; if advanced, nonrewritingmerge/"
    "surgicalreconciliation/derivedregeneration/revalidate actualcombinedtree/"
    "independent changedteaching review/native-scope reassessment. Then normal "
    "signing/scoped stop-cran ownerfastforward/noauthswitch/noforcepush/noamend/"
    "terminalgreenCI/EVERYimmutablepublicZIP runtimeentryhash/manifest equality/"
    "unchanged18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue/durablepublication ledgers "
    "BEFORE099. Local acceptance NOT publicdelivery. Published124/1228, "
    "1104remaining unchanged until delivery verified. Parent15692 ownsrunner.lock: "
    "verifyliveancestry/currentrunnersession/signedheads/whollyclean; "
    "NOchildacquire/delete/unlock/readprobe. Approvedcontrol/committedpackets/"
    "frozeninputs only; no optionalhistoricalsessionhelper. Original722denial/"
    "approvedrecovery preserved. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. Physicalphone/generalrelease/whole-set "
    "outstanding. No099/runtimepublication/secondrunner."
)
sys.path.insert(0, str(R / "tools"))


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data):
    temporary = p.with_suffix(p.suffix + ".726.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == data
    temporary.replace(p)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(root), *args],
        encoding="utf-8").strip()


def context(head=HEAD):
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (15692, L.name, "running")
    script = f"""
$id={os.getpid()};$chain=@()
while($id -gt 0 -and $chain.Count -lt 12){{
 $p=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(!$p){{break}}
 $chain+=@{{pid=[int]$p.ProcessId;parent=[int]$p.ParentProcessId;name=$p.Name;command=$p.CommandLine}}
 if($id -eq 15692){{break}}
 $id=$p.ParentProcessId
}}
$chain|ConvertTo-Json -Depth 4 -Compress
"""
    chain = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert chain[-1]["pid"] == 15692
    assert any(p["name"].lower() == "copilot.exe" and L.name in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["batch"], state["status"]) == (725, "098", "continue")
    assert git("rev-parse", "origin/main") == MAIN
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)
    return {
        "parentPid": 15692, "session": L.name, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
    }


def runtime():
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    count = 0
    for kind, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                actual = sha(R / name) if kind in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == digest, name
                count += 1
    assert (count, manifest["contentVersion"]) == (8449, VERSION)
    return {"runtimeHashesVerified": count, "contentVersion": VERSION,
            "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True,
            "runtimeChanged": False}


def start():
    role = context()
    before = L / "progress-before-726.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    state = load(C / "progress.json")
    assert checkpoint["batch098RenderedConfirmationCheckpoint"] == state["batch098RenderedConfirmationCheckpoint"]
    assert git("merge-base", MAIN, HEAD) == MAIN
    assert not git("diff", HEAD + "...origin/main", "--name-only")
    starting = {
        "execution": 726, "batch": "098", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME098 combined-current-main acceptance and signed LOCAL review-closed checkpoint; publication next, no099.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, entire approved issue and final725 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed packets/frozen workspace inputs only; no optional historical-session helper accessed.",
        "integration": {"result": "Already up to date; fresh origin/main is an ancestor.",
                        "newIncomingPaths": [], "overlappingTeaching": [], "mergeCommitNeeded": False},
    }
    save(L / "starting-state-726.json", starting)
    state["execution726StartingState"] = starting
    state.update(stage="batch-098-combined-main-acceptance-in-progress",
                 nextAction=starting["scope"], blocker=None)
    save(C / "progress.json", state)
    assert all(state[k] == v for k, v in load(before).items() if k not in {"stage", "nextAction", "blocker"})
    print("Combined098 starting scope persisted; clean signed heads/live parent verified.")


def audit():
    context()
    helper = C / "batch-098-draft-719.py"
    original = S / "batch-098-draft-recipe.py"
    def audit_tree(path):
        return ast.dump(next(n for n in ast.parse(path.read_text(encoding="utf-8")).body
                             if isinstance(n, ast.FunctionDef) and n.name == "audit"))
    assert audit_tree(helper) == audit_tree(original)
    spec = importlib.util.spec_from_file_location("source_bound_098_audit", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    captured = {}
    module.identity = context

    def capture(path, value):
        assert path.parent == S and path.name in {
            "batch-098-draft-audit.json", "batch-098-draft-font-audit.json",
            "batch-098-draft-stroke-audit.json"}
        captured[path.name] = value

    module.save = capture
    with (L / "source-audit-726.txt").open("w", encoding="utf-8") as output:
        with contextlib.redirect_stdout(output):
            module.audit()
    result = captured["batch-098-draft-audit.json"]
    assert result["currentCounts"] == {"kanji": 1121, "words": 5073, "n1Labels": 130,
                                      "namedSourceMembersPresent": 135}
    assert result["allMappedReciprocalPairs"] == 2 and result["directedLinksVerified"] == 4
    result.update(execution=726, stage=STAGE, combinedContentHead=HEAD, integratedMain=MAIN,
                  mainAlreadyAncestor=True, incomingRuntimeChanges=[], runtime=runtime(),
                  reviewClosed=["\u5264"], draftOnlyAdditions=[], runtimeAccepted=True,
                  pendingNativeFallbackLabels=[], inheritedNativeFallbackVisible=["\u5202", "\u6c35"],
                  auditRecipe="docs/n1-sources/batch-098-draft-recipe.py",
                  auditRecipeSha256=sha(original), durableAuditHelperSha256=sha(helper),
                  recipeDiagnostic="Initial full-helper byte guard correctly stopped audit: durable719 helper contains previously recorded freeze/history guard fixes absent from original archived recipe. Exact audit-function AST matches original. Only unchanged audit executed with current726 identity guard/capture-only outputs. All five Python commands already passed; not redundantly rerun.",
                  auditReuse="Unchanged source-bound audit with current726 identity guard and capture-only output; original draft evidence not overwritten.",
                  limits="Fresh mechanical source/baseline/reading/stroke/link/font provenance audit; inherited native724/rendered725, not new linguistic/native/phone evidence.")
    save(L / "combined-source-audit-726.json", result)
    save(L / "combined-font-provenance-726.json", captured["batch-098-draft-font-audit.json"])
    save(L / "combined-stroke-provenance-726.json", captured["batch-098-draft-stroke-audit.json"])
    print("Frozen sources/baseline/all mapped links/readings/strokes/font provenance and8449 hashes passed.")


def checks():
    context()
    for name, arguments in [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]), ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]:
        command = [sys.executable, "-X", "utf8", "-B", *arguments]
        with (L / f"{name}-726.txt").open("w", encoding="utf-8") as output:
            completed = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-726.json", {"command": command, "exitCode": completed.returncode})
        assert completed.returncode == 0, name
        print(name, "passed", flush=True)
    audit()


def inherited():
    textual = load(V / "batch-098-reconciliation.json")
    rendered = load(V / "batch-098-visual-reconciliation-725.json")
    native = load(S / "execution-724.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["actionableRemainingTextualFindingGroups"] == textual["consequentialUnresolvedTeachingClaims"] == 0
    assert rendered["actionableRemainingFindings"] == rendered["consequentialUnresolvedInScopeClaims"] == 0
    assert not rendered["findings"] and not rendered["teachingChanged"]
    assert rendered["sampledLivePoolSemanticAcceptance"] == "CLEAN"
    assert rendered["unrestrictedLivePoolSemanticAcceptance"] == "UNVERIFIED"
    assert rendered["serialReviewerProcessesExited"] and rendered["allToolViewsSerial"]
    assert rendered["allAssignedResourcesReturned"] and rendered["eachReviewerImagesDecoded"] == 23
    for name, digest in textual["reviewedRuntimeHashes"].items():
        assert sha(R / name) == digest
    for record in [textual, rendered]:
        previous = None
        for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
            process = record["processes"][label]
            assert process["actualModels"] == [model] and process["exitCode"] == 0
            if previous:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
            previous = process["completedAt"]
            if record is textual:
                assert process["allAssignedRangesReturned"] and not process["observedToolOverlaps"]
                assert process["exactFullPacketReturnedInFirstCall"]
                assert sha(V / process["report"]) == process["reportSha256"]
                assert sha(V / f"batch-098-initial-{label}.jsonl") == process["rawExecutionSha256"]
            else:
                assert process["sessionId"] == textual["processes"][label]["sessionId"]
                assert len(process["toolCalls"]) == 25
                prior = None
                for call in process["toolCalls"]:
                    assert call["name"] == "view" and call["success"]
                    if prior:
                        assert datetime.fromisoformat(prior) <= datetime.fromisoformat(call["startedAt"])
                    prior = call["completedAt"]
    receipts = 0
    for row in load(R / native["artifactIndex"]):
        assert sha(R / row["path"]) == row["sha256"]
        receipts += 1
    for row in load(S / "execution-725.json")["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
        receipts += 1
    assert native["terminalPerCaseStatus"] == [
        {"class": "io.github.stopcran.kanji.ui.N1Batch098GlyphTest",
         "test": "agentLookalikesAndScopedHanAcrossFourProductionFamilies", "status": 0},
        {"class": "io.github.stopcran.kanji.ui.N1Batch098ArticleTest",
         "test": "fullSingleImportOfflineAgentReusedSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack",
         "status": 0},
    ] and native["nativeTestsSkipped"] == 0
    assert native["fullArchiveImportedOnce"]
    assert (native["importedKanji"], native["importedWords"], native["n1Cards"],
            native["problems"], native["acceptedReadingParserEpoch"]) == (1121, 5073, 130, 0, 1)
    route = load(R / native["routeEvidence"])
    assert (route["archiveRequests"], route["importedKanji"], route["importedWords"],
            route["n1Cards"], route["problems"], route["acceptedReadingParserEpoch"]) == (1, 1121, 5073, 130, 0, 1)
    assert route["offline"] and route["reciprocalLinkAndSystemBack"] and route["drawingTraceThenRecall"]
    assert len(route["productionBuilderN1AndAllExactChoices"]) == 64
    assert len(route["directGuardBuilderChecks"]) == 128
    assert not git("diff", native["contentSnapshot"], HEAD, "--", "manifest.json")
    assert not git("diff", "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", APP,
                   "--", "core/src/main", "app/src/main", "gradle.properties", root=A)
    frozen = load(R / native["archiveBudgetEvidence"])
    path = Path(frozen["archive"])
    assert path.is_relative_to(C) and sha(path) == native["archiveSha256"]
    with zipfile.ZipFile(path) as archive:
        manifests = [n for n in archive.namelist() if n.endswith("/manifest.json")]
        assert len(manifests) == 1
        prefix = manifests[0][:-len("manifest.json")]
        manifest = load(R / "manifest.json")
        assert json.loads(archive.read(manifests[0])) == manifest
        verified = 0
        for kind, entries in manifest.items():
            if isinstance(entries, dict):
                for name, digest in entries.items():
                    raw, local = archive.read(prefix + name), (R / name).read_bytes()
                    if kind not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                        raw, local = raw.replace(b"\r\n", b"\n"), local.replace(b"\r\n", b"\n")
                    assert hashlib.sha256(raw).hexdigest() == digest and raw == local, name
                    verified += 1
        assert verified == 8449
    return {
        "initialRecord": "docs/n1-reviews/batch-098-reconciliation.json",
        "nativeRecord": "docs/n1-sources/execution-724.json",
        "renderedRecord": "docs/n1-reviews/batch-098-visual-reconciliation-725.json",
        "receiptHashesReverified": receipts, "originalTeachingAndStrokesUnchanged": True,
        "native724EqualsCombinedManifest": True, "nativeArchiveRuntimeHashesReverified": verified,
        "nativeArchiveSha256": native["archiveSha256"], "newNativeRuns": 0, "newReviewers": 0,
        "originalLimits": {"textual": textual["limits"], "native": native["limits"], "rendered": rendered["limits"]},
        "incomingTeachingReview": "Not needed: ZERO incoming changes; fresh main already ancestor.",
        "changedNativeScope": "None: exact full manifest and every imported payload identical; inherited native724, not a new import.",
    }


def record():
    context()
    tests = (L / "python-tests-726.txt").read_text(encoding="utf-8")
    total = int(re.search(r"^Ran (\d+) tests in ", tests, re.M)[1])
    assert total >= 372 and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-726.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    vocabulary = (L / "vocabulary-726.txt").read_text(encoding="utf-8").strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-726.json")["exitCode"] == 0
    assert (L / "host-exit-726.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-726.txt").read_text(encoding="utf-8-sig")
    begin = datetime.fromisoformat((L / "host-start-726.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((L / "host-end-726.txt").read_text(encoding="utf-8-sig").strip())
    suites = []
    for module, task, cls, expected in [
        ("core", "test", "RealContentTest", {
            "parsesRealContentRepoWhenPresent", "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
            "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent"}),
        ("app", "testDebugUnitTest", "RareHanTest", {"contentRareCharactersAreCoveredByBundledFont"}),
    ]:
        path = A / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{cls}.xml"
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == len(expected)
        assert all(xml.attrib[k] == "0" for k in ("skipped", "errors", "failures"))
        assert {x.attrib["name"] for x in xml.findall("testcase")} == expected
        assert not any(xml.findall(".//" + name) for name in ("skipped", "failure", "error"))
        assert begin <= datetime.fromisoformat(xml.attrib["timestamp"]).astimezone(timezone.utc) <= end
        assert path.stat().st_mtime >= begin.timestamp()
        suites.append({"path": str(path), "sha256": sha(path), "suite": xml.attrib,
                       "cases": [x.attrib for x in xml.findall("testcase")]})
    assert all((A / module / ".." / ".." / "learning-japanese").resolve() == R for module in ("app", "core"))
    budget = ast.literal_eval((L / "budget-726.txt").read_text(encoding="utf-8"))
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    assert budget["entries"] <= MAX_ENTRIES and budget["retainedBytes"] <= MAX_RETAINED
    assert budget["inflatedBytes"] <= MAX_INFLATED and budget["localZipBytes"] <= MAX_COMPRESSED
    inheritance = inherited()
    source = load(L / "combined-source-audit-726.json")
    directory = V / "batch-098-combined-acceptance-726"
    assert not directory.exists()
    directory.mkdir()
    paths = [
        *(L / f"{name}-726.txt" for name in ["python-tests", "validate", "manifest", "vocabulary", "budget",
                                             "host", "host-exit", "host-start", "host-end", "source-audit"]),
        *(L / f"{name}-exit-726.json" for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]),
        *(L / f"{name}-726.json" for name in ["starting-state", "combined-source-audit",
                                              "combined-font-provenance", "combined-stroke-provenance", "host-command"]),
        *(Path(row["path"]) for row in suites),
        Path(__file__), C / "run-batch-098-host-726.ps1", C / "post-batch-098-combined-726.ps1",
        C / "batch-065-host-integration-heap.init.gradle", C / "authoring-artifact-path-notes.txt",
        C / "runner-lock-role-notes.txt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        A / "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    ]
    receipts = []
    for path in paths:
        raw = path.read_bytes()
        compressed = path.suffix == ".txt"
        target = directory / (path.name + (".gz" if compressed else ""))
        assert not target.exists()
        target.write_bytes(gzip.compress(raw, mtime=0) if compressed else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "archiveSha256": sha(target), "losslessGzip": compressed})
    evidence = {
        "schemaVersion": 1, "execution": 726, "batch": "098", "status": STAGE,
        "startingState": load(L / "starting-state-726.json"),
        "authoredTeachingSnapshot": "233d3add2b90fcb98f9706b8901aa936fc6e56e7",
        "reviewedSnapshot": HEAD, "combinedTestedSnapshot": HEAD, "integratedMain": MAIN,
        "mainAlreadyAncestor": True, "incomingChanges": [], "substantiveTeachingChanged": False,
        "runtime": runtime(), "checks": {
            "pythonTests": total, "validatorErrors": 0, "manifestFresh": True, "vocabulary": vocabulary,
            "originalArchiveBudgets": budget, "androidTests": suites, "androidTestsTotal": 4,
            "androidSkipped": 0, "freshAndroidExecution": True, "actualResolvedContentRoot": str(R),
            "gradleExitCode": 0},
        "sourceAudit": source, "inheritedAcceptance": inheritance, "receipts": receipts,
        "reviewClosed": ["\u5264"], "published": [], "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "runtimeAccepted": True,
        "runtimeAcceptanceScope": "Local bounded owner-testing acceptance, not public delivery/general release.",
        "runtimePublished": False, "newReviewers": 0, "newNativeRuns": 0,
        "qualifiedTestOnlyAndroid": APP, "unchangedProductionAndroid": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "latestAppMainClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "publishedAdditions": 124, "remainingAdditions": 1104, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "receiptSchemaDiagnostic": "First record attempt stopped before writing evidence: native724 stores terminal cases as named class/test/status objects, not a bare integer list used by older716. Exact two named cases/status0 now checked directly; no native rerun, gate relaxation or original receipt modification.",
        "limits": [
            "Native724 and original-session725 confirmations inherited, not freshly rerun or new blind credit.",
            "Bounded64kanji/128preserved-directguard records CLEAN, unrestricted/future pools UNVERIFIED.",
            "Resized reviewer images and contact sheets; exact fallback face unidentified. Injected tracing/give-up not human handwriting/MLKit.",
            "Physical-phone/general-release and whole-set acceptance outstanding.",
            "No incoming changes; no new changed-teaching review/native run required. Reassess if main advances.",
            "Public CI/immutable ZIP/normal owner fast-forward/verified publication issue remain pending.",
        ],
    }
    save(S / "execution-726.json", evidence)
    save(V / "batch-098-combined-acceptance-726.json", evidence)
    ledger = load(S / "batch-098-progress.json")
    ledger["preCombinedAcceptanceLimits"] = ledger["limits"]
    ledger.update(status=STAGE, reviewClosed=["\u5264"], published=[], runtimeAccepted=True,
                  nextAction=NEXT, limits=evidence["limits"])
    ledger["combinedAcceptance726"] = {
        "evidence": "docs/n1-sources/execution-726.json",
        "reviewRecord": "docs/n1-reviews/batch-098-combined-acceptance-726.json",
        "runtimeAccepted": True, "runtimePublished": False, "contentVersion": VERSION,
        "mainAlreadyAncestor": True, "incomingChanges": [], "native724StillExact": True,
        "freshPythonTests": total, "freshAndroidTests": 4, "freshAndroidSkipped": 0,
        "historicalLimitDisposition": "Earlier pending/draft limits preserved as historical; superseded only for bounded local acceptance."}
    ledger["pendingGates"] = [
        "Fresh main check; nonrewriting merge/reconcile/regenerate/revalidate and independent changed-teaching/native scope reassessment if advanced.",
        "Normal signed owner fast-forward, terminal-green CI, EVERY immutable public ZIP entry/hash under original guards, verified owner issue and durable publication checkpoint before099."]
    save(S / "batch-098-progress.json", ledger)
    print("Combined local bounded acceptance archived; no runtime changes or publication.")


def issue():
    evidence = load(S / "execution-726.json")
    budget = evidence["checks"]["originalArchiveBudgets"]
    body = (
        "Batch098 / checkpoint726: **combined-current-main acceptance complete locally; not yet published**.\n\n"
        "Fresh `origin/main` remains `69af99e5`, already ancestor of signed `844c3df1`; normal "
        "non-rewriting merge returned Already up to date, zero incoming teaching/runtime changes. "
        "All8,449 runtime hashes/version`0cbdc2723b0433f2` equal native724's full archive. Its production "
        "ContentSync ONCE/1121kanji/5073words/130N1/zeroProblems/Room epoch1 and two terminal native "
        "case successes remain inherited, not newly rerun.\n\n"
        f"Fresh combined checks passed:{evidence['checks']['pythonTests']} Python tests, validator0 errors, "
        "regenerated manifest unchanged, vocabulary consistency2122/2431 pilot prompts (not complete "
        "coverage), full frozen dictionaries/baseline/readings/strokes/all-mapped links/font provenance "
        "and four non-skipped Android cases (RealContentTest3, RareHanTest1). "
        f"Local archive:{budget['entries']} entries/{budget['localZipBytes']} compressed/"
        f"{budget['inflatedBytes']} inflated/{budget['retainedBytes']} retained bytes, unchanged guards. "
        "Qualified TESTONLY Android`1c1b7bf4` retains production`f9b59a2`, not latest app main.\n\n"
        "\u5264 is locally review-closed with exact reused\u6d17\u5264:28/\u6d17:38 changes; "
        "no new support word, two all-mapped pairs/four directions/one activated baseline pair. "
        "Full readings retained; only on\u3056\u3044 offered, no kun. One original direct "
        "\u6d17\u5264/\u305b\u3063\u3051\u3093 guard preserved, none new. Original serial two-family textual "
        "and dependent rendered confirmations retained. Actual N1 choices\u5264 vs\u525b/\u51b6/\u5211 "
        "(one curated, two fallback). Bounded64/128 quiz samples CLEAN, unrestricted/future pools "
        "UNVERIFIED. Each original reviewer25serialviews/23PNG, three font panels/all19Han, "
        "12contact sheets/45routes and eight additional route views; not48original-resolution "
        "views. Resizing, exact fallback-face and injected-drawing limits retained.\n\n"
        "Evidence:`docs/n1-sources/execution-726.json` and "
        "`docs/n1-reviews/batch-098-combined-acceptance-726.json` in signed local checkpoint. "
        "**Next:** fresh-main check, normal authorized owner fast-forward, terminal-green CI and every "
        "immutable public ZIP runtime hash/budget check, then publication ledgers/checkpoint before099. "
        "Published coverage stays124/1228,1104 remaining until delivery verified. Phone/general-release/"
        "whole-set acceptance outstanding. Parent lock untouched; no historical-session helper access "
        "or new permission denial. Original722 denial/approved recovery preserved.\n"
    )
    (C / "batch-098-combined-726-issue-body.txt").write_text(body, encoding="utf-8")


def finalize():
    head = git("rev-parse", "HEAD")
    context(head=head)
    assert git("rev-parse", "HEAD^") == HEAD
    evidence = load(S / "execution-726.json")
    expected = {r["archive"] for r in evidence["receipts"]} | {
        "docs/n1-sources/execution-726.json", "docs/n1-reviews/batch-098-combined-acceptance-726.json",
        "docs/n1-sources/batch-098-progress.json"}
    assert set(git("diff", "--name-only", HEAD, "HEAD").splitlines()) == expected
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    prefix = "batch-098-combined-726-issue-"
    receipt, posted = load(C / (prefix + "receipt.json")), load(C / (prefix + "posted.json"))
    body = (C / (prefix + "body.txt")).read_bytes().decode("utf-8-sig")
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = load(C / "progress.json"), load(L / "progress-before-726.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 726, "checkpoint": 726, "batch": "098",
        "savedCommit": head, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-726.json",
        "reviewRecord": "docs/n1-reviews/batch-098-combined-acceptance-726.json",
        "authoredTeachingSnapshot": evidence["authoredTeachingSnapshot"],
        "reviewedSnapshot": HEAD, "combinedTestedSnapshot": HEAD, "integratedMain": MAIN,
        "mainAlreadyAncestor": True, "incomingChanges": [], **runtime(),
        "reviewClosed": ["\u5264"], "published": [], "runtimeAccepted": True,
        "runtimeAcceptanceScope": evidence["runtimeAcceptanceScope"], "runtimePublished": False,
        "freshPythonTests": evidence["checks"]["pythonTests"], "freshAndroidTests": 4,
        "freshAndroidSkipped": 0, "newNativeRuns": 0, "newReviewers": 0,
        "native724StillExact": True, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 124, "remainingAdditions": 1104, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
        "checkpointHelper": str(Path(__file__)), "checkpointHelperSha256": sha(Path(__file__)),
        "nextAction": NEXT,
    }
    state.update(checkpoint=726, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution726CoordinatorCheckpoint"] = checkpoint
    state["batch098CombinedAcceptanceCheckpoint"] = checkpoint
    save(C / "progress.json", state)
    reread = load(C / "progress.json")
    assert all(reread[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-726.json", checkpoint)
    print("Checkpoint726 persisted; all", len(before), "original historical root values preserved.")
    print(head, receipt["html_url"])


if __name__ == "__main__":
    {"start": start, "checks": checks, "audit": audit, "preflight": context,
     "record": record, "issue": issue, "finalize": finalize}[sys.argv[1]]()
