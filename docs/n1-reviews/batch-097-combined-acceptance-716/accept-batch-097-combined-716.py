"""Verify combined batch 097; the live parent retains its runner lock."""
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
L = C / "logs" / "7461f3b6-f096-49a1-a62b-d3f6a400807e"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
HEAD = "833eacbe1e6554bdb727b43135350d1f9b7dd65a"
MAIN = "1b00a924a007f32da36894ea92b05f675436e60d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "a066afceaf1f447a"
STAGE = "batch-097-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME097 publication only next. Read docs/n1-sources/execution-716.json and "
    "docs/n1-reviews/batch-097-combined-acceptance-716.json at the normally signed "
    "LOCAL review-closed checkpoint. Fresh main1b00a924 already ancestor; normal "
    "merge Already up to date, ZERO incoming/runtime/teaching changes. All8447 "
    "runtime hashes/versiona066afceaf1f447a match native714 full archive83e5c090: "
    "productionContentSync ONCE/1120kanji5073words129N1/zeroProblems/Roomepoch1/"
    "BOTH terminalcase0/no skips. Inherited native714/original715 dependent "
    "rendered confirmations NOT fresh native/phone evidence. Fresh716 full Python/"
    "validate/manifest/vocabulary/budget/frozen-source/baseline/readings/stroke/"
    "allmappedlinks/font-provenance plus FOUR Android RealContentTHREE+RareHanONE "
    "no skips passed. TWO serial blind initials711 actualClaudeOpus5.5 then "
    "GPT6.1Sol; original-session715 resource-gated36turns/34views/32images/"
    "zerooverlaps accepted, initialClaude29overlap attempt NOT accepted. "
    "Bothけん/つるぎGood/Done, THREEpairs/SIXdirections/ONEactivatedbaselinepair/"
    "FOURwordguards/TENinjectedstrokes/Back-offline preserved. "
    "Bounded64kanji512wordguard samples CLEAN; widercustom/random/legacy "
    "semantic safety UNVERIFIED, no whole-pool certification. 刂 visible but "
    "exact fallbackface unidentified; image resizing limits retained. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "Fetch latestoriginmain before publication; if advanced, nonrewriting "
    "merge/surgicalreconciliation/derivedregeneration/revalidate actualcombinedtree/"
    "independent changedteaching review/native-scope reassessment. Then normal "
    "signing/scoped stop-cran ownerfastforward/noauthswitch/noforcepush/noamend/"
    "terminalgreenCI/EVERY immutablepublicZIP runtimeentryhash/manifest equality/"
    "unchanged18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue/durablepublication ledgers. "
    "Local acceptance NOT publicdelivery. Published123/1228,1105remaining "
    "unchanged until all gates pass. Parent19008 retainsrunner.lock: verify "
    "liveancestry/session/signedheads/whollyclean, NOchildlockoperation. "
    "Approvedcontrol/committedpackets/frozeninputs only, no optionalhistorical "
    "sessionhelpers. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Physicalphone/generalrelease/whole-set outstanding; "
    "no humanhandwriting/MLKit/native-speaker acceptance. No098/secondrunner."
)
sys.path.insert(0, str(R / "tools"))


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data):
    temporary = p.with_suffix(p.suffix + ".716.tmp")
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


def context(clean=True, head=HEAD):
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    script = f"""
$id={os.getpid()};$chain=@()
while($id -gt 0 -and $chain.Count -lt 12){{
 $p=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(!$p){{break}}
 $chain+=@{{pid=[int]$p.ProcessId;parent=[int]$p.ParentProcessId;name=$p.Name;command=$p.CommandLine}}
 if($id -eq 19008){{break}}
 $id=$p.ParentProcessId
}}
$chain|ConvertTo-Json -Depth 4 -Compress
"""
    chain = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert chain[-1]["pid"] == 19008
    assert any(p["name"].lower() == "copilot.exe" and L.name in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (715, "097", "continue")
    assert git("rev-parse", "origin/main") == MAIN
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if clean or root == A:
            assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)
    return {
        "parentPid": 19008, "session": L.name, "decodedLauncherMatches": True,
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
    assert (count, manifest["contentVersion"]) == (8447, VERSION)
    return {"runtimeHashesVerified": count, "contentVersion": VERSION,
            "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True,
            "runtimeChanged": False}


def start():
    role = context()
    before = L / "progress-before-716.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    state = load(C / "progress.json")
    assert checkpoint["batch097RenderedConfirmationCheckpoint"] == state["batch097RenderedConfirmationCheckpoint"]
    assert git("merge-base", MAIN, HEAD) == MAIN
    assert not git("diff", HEAD + "...origin/main", "--name-only")
    starting = {
        "execution": 716, "batch": "097", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME097 combined-current-main acceptance and signed LOCAL review-closed checkpoint; publication next, no098.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, entire approved issue and final715 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed packets/frozen workspace inputs only; no optional historical-session helper accessed.",
        "integration": {"result": "Already up to date; current origin/main is an ancestor.",
                        "newIncomingPaths": [], "overlappingTeaching": [], "mergeCommitNeeded": False},
    }
    save(L / "starting-state-716.json", starting)
    state["execution716StartingState"] = starting
    state.update(stage="batch-097-combined-main-acceptance-in-progress",
                 nextAction=starting["scope"], blocker=None)
    save(C / "progress.json", state)
    assert all(state[k] == v for k, v in load(before).items() if k not in {"stage", "nextAction", "blocker"})
    print("Combined097 starting state persisted; exact clean signed heads/live parent verified.")


def audit():
    context()
    helper = C / "batch-097-draft-710.py"
    assert helper.read_bytes() == (S / "batch-097-draft-recipe.py").read_bytes()
    spec = importlib.util.spec_from_file_location("source_bound_097_audit", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    captured = {}
    module.identity = context
    def capture(path, value):
        assert path.parent == S and path.name in {
            "batch-097-draft-audit.json", "batch-097-draft-font-audit.json",
            "batch-097-draft-stroke-audit.json"}
        captured[path.name] = value
    module.save = capture
    with (L / "source-audit-716.txt").open("w", encoding="utf-8") as output:
        with contextlib.redirect_stdout(output):
            module.audit()
    result = captured["batch-097-draft-audit.json"]
    assert result["currentCounts"] == {"kanji": 1120, "words": 5073, "n1Labels": 129,
                                      "namedSourceMembersPresent": 134}
    assert result["allMappedReciprocalPairs"] == 3 and result["directedLinksVerified"] == 6
    assert result["allRuntimePayloadHashesVerified"] == 8447
    result.update(execution=716, stage=STAGE, combinedContentHead=HEAD, integratedMain=MAIN,
                  mainAlreadyAncestor=True, incomingRuntimeChanges=[], runtime=runtime(),
                  reviewClosed=["\u5263"], draftOnlyAdditions=[], runtimeAccepted=True,
                  pendingNativeFallbackLabels=[], inheritedNativeFallbackVisible=["\u5202"],
                  auditRecipe="docs/n1-sources/batch-097-draft-recipe.py",
                  auditRecipeSha256=sha(helper),
                  auditReuse="Unchanged source-bound audit with current716 identity guard and capture-only output; no historical draft evidence overwritten.",
                  limits="Fresh mechanical source/baseline/reading/stroke/link/font provenance audit; inherited native714/rendered715, not new linguistic/native/phone evidence.")
    save(L / "combined-source-audit-716.json", result)
    print("Frozen sources/baseline/all mapped links/strokes/font provenance and8447 hashes passed.")


def checks():
    context()
    for name, arguments in [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]), ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]:
        command = [sys.executable, "-X", "utf8", "-B", *arguments]
        with (L / f"{name}-716.txt").open("w", encoding="utf-8") as output:
            completed = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-716.json", {"command": command, "exitCode": completed.returncode})
        assert completed.returncode == 0, name
        print(name, "passed", flush=True)
    audit()


def inherited():
    textual = load(V / "batch-097-reconciliation.json")
    rendered = load(V / "batch-097-rendered" / "execution-715" / "reconciliation.json")
    native = load(S / "execution-714.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert textual["actionableRemainingTextualFindingGroups"] == textual["consequentialUnresolvedTeachingClaims"] == 0
    assert rendered["renderedConfirmationsClosed"] and not rendered["findings"]
    assert rendered["boundedSemanticAcceptance"] == "CLEAN"
    assert rendered["wholePoolSemanticAcceptance"] == "UNVERIFIED"
    assert rendered["acceptedToolOverlaps"] == 0 and not rendered["nonconformingAttempt"]["accepted"]
    for name, digest in textual["reviewedRuntimeHashes"].items():
        assert sha(R / name) == digest
    previous = None
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        process = textual["processes"][label]
        assert process["actualModels"] == [model] and process["exitCode"] == 0
        assert process["allAssignedRangesReturned"] and not process["observedToolOverlaps"]
        assert process["exactFullPacketReturnedInOneCall"]
        assert sha(V / process["report"]) == process["reportSha256"]
        assert sha(V / f"batch-097-initial-{label}.jsonl") == process["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    receipt_count = 0
    for index in [
        V / "batch-097-native" / "execution-714" / "artifact-index.json",
        V / "batch-097-rendered" / "execution-715" / "artifact-index.json",
    ]:
        for row in load(index):
            assert sha(R / row["path"]) == row["sha256"], row["path"]
            receipt_count += 1
    previous = None
    turns = calls = 0
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        summary = load(V / "batch-097-rendered" / "execution-715" / "resource-gated" / f"{label}-summary.json")
        assert summary["acceptedExecution"] and summary["model"] == model
        assert summary["sessionId"] == textual["processes"][label]["sessionId"]
        for turn in summary["turns"]:
            assert turn["actualModels"] == [model] and turn["exitCode"] == 0
            assert len(turn["toolCalls"]) <= 1
            if previous:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(turn["startedAt"])
            previous = turn["completedAt"]
            for call in turn["toolCalls"]:
                assert call["name"] == "view" and call["success"]
                calls += 1
            turns += 1
    assert (turns, calls) == (36, 34)
    assert native["terminalPerCaseStatus"] == [0, 0] and native["nativeTestsSkipped"] == 0
    assert native["fullArchiveImportedOnce"]
    assert (native["importedKanji"], native["importedWords"], native["n1Cards"],
            native["problems"], native["acceptedReadingParserEpoch"]) == (1120, 5073, 129, 0, 1)
    route = load(R / native["routeEvidence"])
    assert (route["archiveRequests"], route["importedKanji"], route["importedWords"],
            route["n1Cards"], route["problems"], route["acceptedReadingParserEpoch"]) == (1, 1120, 5073, 129, 0, 1)
    assert route["offline"] and route["reciprocalLinkAndSystemBack"] and route["drawingTraceThenRecall"]
    assert len(route["productionBuilderN1AndAllExactChoices"]) == 64
    assert len(route["directGuardBuilderChecks"]) == 512
    assert not git("diff", native["contentSnapshot"], HEAD, "--", "manifest.json")
    assert not git("diff", "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", APP,
                   "--", "core/src/main", "app/src/main", "gradle.properties", root=A)
    frozen = load(S / "execution-713.json")["fixtureVerification"]
    path = Path(frozen["archive"])
    assert path.is_relative_to(C) and sha(path) == frozen["archiveSha256"]
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
                    raw = archive.read(prefix + name)
                    local = (R / name).read_bytes()
                    if kind not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                        raw, local = raw.replace(b"\r\n", b"\n"), local.replace(b"\r\n", b"\n")
                    assert hashlib.sha256(raw).hexdigest() == digest and raw == local, name
                    verified += 1
        assert verified == 8447
    return {
        "initialRecord": "docs/n1-reviews/batch-097-reconciliation.json",
        "nativeRecord": "docs/n1-sources/execution-714.json",
        "renderedRecord": "docs/n1-reviews/batch-097-rendered/execution-715/reconciliation.json",
        "receiptHashesReverified": receipt_count, "originalTeachingAndStrokesUnchanged": True,
        "acceptedRenderedTurnsReverified": turns, "acceptedSingleResourceViewCallsReverified": calls,
        "native714EqualsCombinedManifest": True, "nativeArchiveRuntimeHashesReverified": verified,
        "nativeArchiveSha256": frozen["archiveSha256"], "newNativeRuns": 0, "newReviewers": 0,
        "originalLimits": {"textual": textual["limits"], "native": native["limits"], "rendered": rendered["limits"]},
        "incomingTeachingReview": "Not needed: ZERO incoming changes; current main already an ancestor.",
        "changedNativeScope": "None: exact full manifest and every imported payload identical; inherited native714, not a new import.",
    }


def record():
    context()
    tests = (L / "python-tests-716.txt").read_text(encoding="utf-8")
    total = int(re.search(r"^Ran (\d+) tests in ", tests, re.M)[1])
    assert total >= 372 and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-716.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    vocabulary = (L / "vocabulary-716.txt").read_text(encoding="utf-8").strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-716.json")["exitCode"] == 0
    assert (L / "host-exit-716.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-716.txt").read_text(encoding="utf-8-sig")
    begin = datetime.fromisoformat((L / "host-start-716.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((L / "host-end-716.txt").read_text(encoding="utf-8-sig").strip())
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
    budget = ast.literal_eval((L / "budget-716.txt").read_text(encoding="utf-8"))
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    assert budget["entries"] <= MAX_ENTRIES and budget["retainedBytes"] <= MAX_RETAINED
    assert budget["inflatedBytes"] <= MAX_INFLATED and budget["localZipBytes"] <= MAX_COMPRESSED
    inheritance = inherited()
    source = load(L / "combined-source-audit-716.json")
    directory = V / "batch-097-combined-acceptance-716"
    assert not directory.exists()
    directory.mkdir()
    paths = [
        *(L / f"{name}-716.txt" for name in ["python-tests", "validate", "manifest", "vocabulary", "budget",
                                             "host", "host-exit", "host-start", "host-end", "source-audit"]),
        *(L / f"{name}-exit-716.json" for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]),
        L / "starting-state-716.json", L / "combined-source-audit-716.json", L / "host-command-716.json",
        *(Path(row["path"]) for row in suites),
        Path(__file__), C / "run-batch-097-host-716.ps1", C / "post-batch-097-combined-716.ps1",
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
        "schemaVersion": 1, "execution": 716, "batch": "097", "status": STAGE,
        "startingState": load(L / "starting-state-716.json"),
        "authoredTeachingSnapshot": "1fa1ac69b88383ef424c0a69d34020ccca83c313",
        "reviewedSnapshot": HEAD, "combinedTestedSnapshot": HEAD, "integratedMain": MAIN,
        "mainAlreadyAncestor": True, "incomingChanges": [], "substantiveTeachingChanged": False,
        "runtime": runtime(), "checks": {
            "pythonTests": total, "validatorErrors": 0, "manifestFresh": True, "vocabulary": vocabulary,
            "originalArchiveBudgets": budget, "androidTests": suites, "androidTestsTotal": 4,
            "androidSkipped": 0, "freshAndroidExecution": True, "actualResolvedContentRoot": str(R),
            "gradleExitCode": 0},
        "sourceAudit": source, "inheritedAcceptance": inheritance, "receipts": receipts,
        "reviewClosed": ["\u5263"], "published": [], "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "runtimeAccepted": True,
        "runtimeAcceptanceScope": "Local bounded owner-testing acceptance, not public delivery/general release.",
        "runtimePublished": False, "newReviewers": 0, "newNativeRuns": 0,
        "qualifiedTestOnlyAndroid": APP, "unchangedProductionAndroid": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "latestAppMainClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "publishedAdditions": 123, "remainingAdditions": 1105, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": [
            "Native714 and original-session715 confirmations inherited, not freshly rerun or new blind credit.",
            "Bounded64kanji/512directguard records CLEAN, wider custom/random/legacy pools UNVERIFIED, not whole-pool certification.",
            "Resized reviewer images; exact fallback face unidentified. Injected tracing/give-up not human handwriting/MLKit.",
            "Physical-phone/general-release and whole-set acceptance outstanding.",
            "No incoming changes; no new changed-teaching review/native run required. Reassess if main advances.",
            "Public CI/immutable ZIP/normal owner fast-forward/verified publication issue remain pending.",
        ],
    }
    save(S / "execution-716.json", evidence)
    save(V / "batch-097-combined-acceptance-716.json", evidence)
    ledger = load(S / "batch-097-progress.json")
    ledger.update(status=STAGE, reviewClosed=["\u5263"], published=[], nextAction=NEXT)
    ledger["combinedAcceptance716"] = {
        "evidence": "docs/n1-sources/execution-716.json",
        "reviewRecord": "docs/n1-reviews/batch-097-combined-acceptance-716.json",
        "runtimeAccepted": True, "runtimePublished": False, "contentVersion": VERSION,
        "mainAlreadyAncestor": True, "incomingChanges": [], "native714StillExact": True,
        "freshPythonTests": total, "freshAndroidTests": 4, "freshAndroidSkipped": 0,
        "historicalLimitDisposition": "Earlier pending/draft limits retained as historical, superseded only for local acceptance."}
    ledger["pendingGates"] = [
        "Fresh main check; nonrewriting merge/reconcile/regenerate/revalidate and independent changed-teaching/native scope reassessment if advanced.",
        "Normal signed owner fast-forward, terminal-green CI, EVERY immutable public ZIP entry/hash under original guards, verified owner issue and durable publication checkpoint before098."]
    save(S / "batch-097-progress.json", ledger)
    print("Combined local bounded acceptance archived; no runtime changes or publication.")


def issue():
    evidence = load(S / "execution-716.json")
    budget = evidence["checks"]["originalArchiveBudgets"]
    body = (
        "Batch097 / checkpoint716: **combined-current-main acceptance complete locally; not yet published**.\n\n"
        "Fresh `origin/main` remains `1b00a924`, already an ancestor of signed `833eacbe`; normal "
        "non-rewriting merge returned Already up to date, zero incoming teaching/runtime changes. "
        "All8,447 runtime hashes/version`a066afceaf1f447a` equal native714's full archive. Its production "
        "ContentSync ONCE/1120kanji/5073words/129N1/zeroProblems/Room epoch1 and two terminal native "
        "case successes remain inherited, not newly rerun.\n\n"
        f"Fresh combined checks passed:{evidence['checks']['pythonTests']} Python tests, validator0 errors, "
        "regenerated manifest unchanged, vocabulary consistency2122/2431 pilot prompts (not complete "
        "coverage), full frozen dictionaries/baseline/readings/strokes/all-mapped links/font provenance "
        "and four non-skipped Android cases (RealContentTest3, RareHanTest1). "
        f"Local archive:{budget['entries']} entries/{budget['localZipBytes']} compressed/"
        f"{budget['inflatedBytes']} inflated/{budget['retainedBytes']} retained bytes, unchanged guards. "
        "Qualified TESTONLY Android`1c1b7bf4` retains production`f9b59a2`, not latest app main.\n\n"
        "\u5263 and necessary\u5263\u3064\u308b\u304e support are locally review-closed, with both\u3051\u3093/\u3064\u308b\u304e, "
        "two exact reused navigation changes, three all-mapped pairs/six directions/one activated baseline "
        "pair and four direct word guards. Original serial two-family textual and dependent resource-gated "
        "rendered confirmations retained; nonconforming29-overlap attempt remains rejected. Bounded64/512 "
        "quiz samples CLEAN, wider custom/random/legacy pools UNVERIFIED. Resized-image, fallback-face, "
        "injected-drawing and physical-phone limits remain explicit.\n\n"
        "Evidence:`docs/n1-sources/execution-716.json` and "
        "`docs/n1-reviews/batch-097-combined-acceptance-716.json` in the signed local checkpoint. "
        "**Next:** fresh-main check, normal authorized owner fast-forward, terminal-green CI and every "
        "immutable public ZIP runtime hash/budget check, then publication ledgers/checkpoint before098. "
        "Published coverage stays123/1228,1105 remaining until delivery verified. Phone/general-release/"
        "whole-set acceptance outstanding. Parent lock untouched; no historical-session helper access "
        "or new permission denial.\n"
    )
    (C / "batch-097-combined-716-issue-body.txt").write_text(body, encoding="utf-8")


def finalize():
    head = git("rev-parse", "HEAD")
    context(head=head)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-716.json")
    expected = {r["archive"] for r in evidence["receipts"]} | {
        "docs/n1-sources/execution-716.json", "docs/n1-reviews/batch-097-combined-acceptance-716.json",
        "docs/n1-sources/batch-097-progress.json"}
    assert set(git("diff", "--name-only", HEAD, "HEAD").splitlines()) == expected
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    prefix = "batch-097-combined-716-issue-"
    receipt, posted = load(C / (prefix + "receipt.json")), load(C / (prefix + "posted.json"))
    body = (C / (prefix + "body.txt")).read_bytes().decode("utf-8-sig")
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = load(C / "progress.json"), load(L / "progress-before-716.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 716, "checkpoint": 716, "batch": "097",
        "savedCommit": head, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-716.json",
        "reviewRecord": "docs/n1-reviews/batch-097-combined-acceptance-716.json",
        "authoredTeachingSnapshot": evidence["authoredTeachingSnapshot"],
        "reviewedSnapshot": HEAD, "combinedTestedSnapshot": HEAD, "integratedMain": MAIN,
        "mainAlreadyAncestor": True, "incomingChanges": [], **runtime(),
        "reviewClosed": ["\u5263"], "published": [], "runtimeAccepted": True,
        "runtimeAcceptanceScope": evidence["runtimeAcceptanceScope"], "runtimePublished": False,
        "freshPythonTests": evidence["checks"]["pythonTests"], "freshAndroidTests": 4,
        "freshAndroidSkipped": 0, "newNativeRuns": 0, "newReviewers": 0,
        "native714StillExact": True, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 123, "remainingAdditions": 1105, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
        "checkpointHelper": str(Path(__file__)), "checkpointHelperSha256": sha(Path(__file__)),
        "nextAction": NEXT,
    }
    state.update(checkpoint=716, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution716CoordinatorCheckpoint"] = checkpoint
    state["batch097CombinedAcceptanceCheckpoint"] = checkpoint
    save(C / "progress.json", state)
    reread = load(C / "progress.json")
    assert all(reread[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-716.json", checkpoint)
    print("Checkpoint716 persisted; all", len(before), "original historical root values preserved.")
    print(head, receipt["html_url"])


if __name__ == "__main__":
    {"start": start, "checks": checks, "preflight": context,
     "record": record, "issue": issue, "finalize": finalize}[sys.argv[1]]()
