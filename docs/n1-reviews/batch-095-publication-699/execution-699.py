"""Close and publish batch095 without changing reviewed runtime bytes."""
import base64
import copy
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
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "afb82923-4607-46b7-99ce-dfb05842a9c4"
D = V / "batch-095-publication-699"
HEAD = "0de3e8c3bbdad1e1deb041a6051e536ba42a6911"
MAIN = "da374717b6f8a53430c9583e9b5371004e1f7719"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
INITIAL = "8c4e16500d57749f90f08c196fbb8980981967a6"
VERSION = "3eebfff0fdad5e28"
MEMBER = "\u5256"
BEFORE = L / "progress-before-699.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(path.suffix + ".699.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    temp.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(args, root=R):
    return subprocess.check_output(args, cwd=root, encoding="utf-8").strip()


def git(*args, root=R):
    return output(["git", "--no-pager", "-C", str(root), *args])


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)


def context(head, require_clean=True):
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
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
    chain = json.loads(output(["pwsh", "-NoProfile", "-NonInteractive", "-Command", script]))
    assert chain[-1]["pid"] == 19008
    assert any(p["name"].lower() == "copilot.exe" and L.name in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    launcher = (C / "runner.ps1").read_text(encoding="utf-8-sig")
    assert "$lock.Dispose()" in launcher
    assert "'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None'" in launcher
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (698, "095", "continue")
    clean(A, APP)
    if require_clean:
        clean(R, head)
    else:
        assert git("rev-parse", "HEAD") == head and git("log", "-1", "--format=%G?") == "G"
    return {
        "parentPid": 19008, "session": L.name, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"),
        "parentLockAcquiredOrModified": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
        "diagnostic": "Initial read-only Get-Content runner.lock probe returned a Windows sharing violation. No content was read, no acquisition/deletion/unlock/retry occurred. Live ancestry and unchanged launcher verified instead; this was not a permission denial.",
    }


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8441
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", "d5a6823c70583ab5c64a63a863993b9577466937", HEAD,
                   "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                data = (R / name).read_bytes()
                if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == digest, name
    return manifest


def start():
    role = context(HEAD)
    assert git("rev-parse", "origin/main") == MAIN and git("merge-base", MAIN, HEAD) == MAIN
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution698CoordinatorCheckpoint"] == p["execution698CoordinatorCheckpoint"]
    state = {
        "execution": 699, "batch": "095", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME095 signed reviewclosure, owner fast-forward publication, terminal CI/public ZIP/verified ownerissue; yield before096.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and embedded checkpoint parsed. Operative contract, complete issue and final698 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers accessed.",
    }
    save(L / "starting-state-699.json", state)
    p["execution699StartingState"] = state
    p.update(stage="batch-095-reviewclosure-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    assert all(p[k] == v for k, v in load(BEFORE).items() if k not in {"stage", "nextAction", "blocker"})
    print("Starting state persisted; exact clean signed heads and live parent verified.")


def gate():
    context(HEAD)
    runtime()
    spec = importlib.util.spec_from_file_location("integrate696", C / "integrate-batch-095-696.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    inherited = module.inherited()
    receipts = 0
    for n in [695, 696, 697, 698]:
        for row in load(S / f"execution-{n}.json")["receipts"]:
            path = R / row["archive"]
            assert sha(path) == row["archiveSha256"], path
            raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"], path
            receipts += 1
    automated = load(S / "execution-696.json")
    assert (automated["pythonTestsPassed"], automated["validatorErrors"],
            automated["hostTestsExecuted"], automated["hostTestsSkipped"]) == (372, 0, 4, 0)
    assert automated["manifestFresh"] and automated["vocabularyConsistencyPassed"]
    for row in automated["hostSuites"]:
        suite = row["suite"]
        assert all(suite[k] == "0" for k in ("skipped", "failures", "errors"))
        path = V / "batch-095-combined-integration-696" / Path(row["path"]).name
        assert sha(path) == row["sha256"]
        actual = ET.parse(path).getroot()
        assert len(actual.findall("testcase")) == int(suite["tests"])
    changed = load(V / "batch-095-combined-teaching-reconciliation-697.json")
    assert not changed["findings"]
    assert all(v == "CLEAN" for verdict in changed["facetVerdicts"].values() for v in verdict.values())
    assert all(x["status"] in {"optional", "resolved", "withdrawn"} for x in changed["reconciliation"])
    assert [row["actualModel"] for row in changed["reviewers"]] == ["claude-opus-5.5", "gpt-6.1-sol"]
    for row in changed["reviewers"]:
        assert row["exitCode"] == 0 and row["processExitedVerified"] and row["allSixCommonTextChunksReturned"]
        assert not row["internalToolOverlaps"] and not row["unfinishedTools"]
    confirmation = load(S / "execution-697.json")
    assert confirmation["atMostOneActiveReviewerVerified"] and confirmation["strictSerialToolExecutionAccepted"]
    assert confirmation["actionableRemainingFindings"] == confirmation["consequentialUnresolvedInScopeClaims"] == 0
    native = load(V / "batch-095-combined-native-698" / "acceptance.json")
    assert native["exactCombinedNativeImport"] == "passed"
    assert (native["terminalSuccessCases"], native["skipped"]) == (1, 0)
    imported = native["imported"]
    assert (imported["contentVersion"], imported["archiveRequests"], imported["importedKanji"],
            imported["importedWords"], imported["n1Cards"], imported["problems"],
            imported["acceptedReadingParserEpoch"]) == (VERSION, 1, 1118, 5071, 127, 0, 1)
    assert imported["quizOnKeys"] == ["\u307c\u3046"] and imported["quizKunKeys"] == []
    assert native["directGuardBuilderChecks"] == 384 and native["meaningPoolBuilderChecks"] == 64
    assert (imported["reciprocalPairs"], imported["linkDirections"]) == (2, 4)
    acceptance = {
        "schemaVersion": 1, "execution": 699, "batch": "095", "contentSnapshot": HEAD,
        "combinedMerge": automated["combinedContentHead"], "latestMainIntegrated": MAIN,
        "contentVersion": VERSION, "runtimeHashesVerified": 8441,
        "originalTeachingSnapshot": INITIAL, "reviewClosed": [MEMBER],
        "runtimeAccepted": True, "runtimePublished": False,
        "combinedReceiptHashesReverified": receipts, "inheritedAcceptance": inherited,
        "automatedRecord": "docs/n1-sources/execution-696.json",
        "changedTeachingRecord": "docs/n1-reviews/batch-095-combined-teaching-reconciliation-697.json",
        "exactCombinedNativeRecord": "docs/n1-reviews/batch-095-combined-native-698/acceptance.json",
        "pendingFlagDisposition": "Historical pending flags remain immutable. Confirmations697 discharge696 changed-teaching gate; exact import698 discharges696/697 import gate; this record closes bounded runtime acceptance. Publication still requires exact remote CI/public ZIP.",
        "pythonTestsPassed": 372, "hostTestsExecuted": 4, "hostTestsSkipped": 0,
        "nativeTerminalCases": {"inherited694": 2, "exactCombined698": 1},
        "newReviewerNativeHostRuns": 0,
        "limits": {
            "inherited": inherited["originalLimits"], "changedTeaching": confirmation["limits"],
            "combinedNative": load(S / "execution-698.json")["limits"],
            "clarification": "No new blind review/native/host run. Original Claude695 overlap stays REJECTED, accepted minimal serial repair separate. Untested quiz seeds/pools UNVERIFIED; no physical-phone, human-handwriting, successful MLKit, general-release or whole-set acceptance.",
        },
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    save(L / "prepublication-gate-699.json", acceptance)
    print(f"Review, native and combined automated gates verified; {receipts} archived receipts and8441runtimehashes.")
    return acceptance


def local_checks():
    results = []
    for name, arguments in [
        ("validate", ["tools\\validate.py"]), ("manifest", ["tools\\build_manifest.py"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]:
        path = L / f"{name}-699.txt"
        assert not path.exists()
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *arguments],
                                    cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        results.append({"path": path.name, "sha256": sha(path), "exitCode": 0})
    runtime()
    return results


def accept():
    accepted = gate()
    assert not D.exists() and not (S / "batch-095-acceptance-699.json").exists()
    checks = local_checks()
    D.mkdir()
    accepted["terminalLocalChecks"] = checks
    save(S / "batch-095-acceptance-699.json", accepted)
    ledger = load(S / "batch-095-progress.json")
    ledger["preReviewClosure699State"] = copy.deepcopy(ledger)
    ledger.update(status="review-closed-combined-accepted-awaiting-publication",
                  reviewClosed=[MEMBER], runtimeAccepted=True,
                  acceptanceRecord="batch-095-acceptance-699.json",
                  pendingGates=["Owner fast-forward; terminal green CI; every immutable public ZIP runtime hash/budget; verified ownerissue before096."],
                  nextAction="SAME095 owner fast-forward publication and exact public acceptance; yield before096.")
    save(S / "batch-095-progress.json", ledger)
    for path in [Path(__file__), C / "publish-699.ps1", C / "verify-batch-002-publication.py",
                 L / "starting-state-699.json", L / "prepublication-gate-699.json"]:
        shutil.copyfile(path, D / path.name)
    for check in checks:
        shutil.copyfile(L / check["path"], D / check["path"])
    save(S / "execution-699.json", {
        "schemaVersion": 1, "execution": 699, "batch": "095",
        "status": "review-closed-combined-accepted-awaiting-publication",
        "startingState": load(L / "starting-state-699.json"),
        "acceptanceRecord": "batch-095-acceptance-699.json",
        "runtimeBytesUnchanged": True, "runtimeAccepted": True, "runtimePublished": False,
        "newReviewerNativeHostRuns": 0, "actualNewPermissionDenials": [],
        "parentLockAcquiredOrModified": False, "optionalHistoricalSessionHelpersAccessed": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    })
    runtime()
    print("Bounded acceptance closed; reviewclosed ledger and local evidence ready for normal signing.")


def verify(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-095-{phase}-ci.json"
    assert not ci_path.exists()
    runs = json.loads(output(["gh", "run", "list", "--repo", "stop-cran/learning-japanese",
        "--commit", head, "--workflow", "Validate content", "--limit", "5",
        "--json", "databaseId,status,conclusion,headSha"]))
    assert runs and runs[0]["headSha"] == head, "Exact CI not available; preserve pending checkpoint"
    subprocess.run(["gh", "run", "watch", str(runs[0]["databaseId"]), "--repo",
        "stop-cran/learning-japanese", "--exit-status", "--interval", "10"], check=True)
    save(ci_path, json.loads(output(["gh", "run", "view", str(runs[0]["databaseId"]), "--repo",
        "stop-cran/learning-japanese", "--json", "databaseId,status,conclusion,headSha,workflowName,jobs"])))
    path = C / "artifacts" / f"content-{head[:7]}.zip"
    assert not path.exists()
    url = f"https://codeload.github.com/stop-cran/learning-japanese/legacy.zip/{head}"
    result = subprocess.run(["curl.exe", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "180", url, "--output", str(path)], capture_output=True, text=True)
    save(L / f"archive-download-{phase}-699.json", {
        "commit": head, "url": url, "exitCode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
        head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def public(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-095-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8441 and archive["manifestEqual"]
    assert all(archive[k] for k in ["allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (18000, 42*1024**2, 80*1024**2, 56*1024**2)
    return ci, archive


def records(head):
    ci, archive = public("accepted", head)
    assert not (S / "batch-095-publication.json").exists()
    automated = load(S / "execution-696.json")
    counts = dict(automated["sourceAudit"]["currentCounts"])
    from audit_n1_pilot import metadata
    chars = {p.stem for p in (R / "kanji").glob("*.md")}
    named = set(load(S / "community-list-20261102.json"))
    assert len(chars & named) == 132
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=122, remainingAdditions=1106,
        namedSourceMembersPresent=132, batchNewNecessarySupportWords=1,
        projectNewNecessarySupportWords=122, batchChangedReusedArticles=1,
        allMappedReciprocalPairs=2, mappedDirectedLinks=4, activatedBaselinePairs=0,
        separateExceptionPreserved="\u5996", separateEarlierLevelSourceMembers=list("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50"),
        earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"]) == (1118, 5071, 127)
    p, before = load(C / "progress.json"), load(BEFORE)
    publication = {
        "schemaVersion": 1, "execution": 699, "batch": "095", "membership": [MEMBER],
        "status": "published-verified-bounded-owner-testing", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": load(S / "batch-095-progress.json")["baseCommit"],
        "authoredSnapshot": INITIAL, "initialReviewedTeachingSnapshot": INITIAL,
        "reviewedTeachingSnapshot": INITIAL, "combinedContentHead": automated["combinedContentHead"],
        "latestMainIntegrated": MAIN, "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"] for n in range(689, 699)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-095-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-095-rendered-reconciliation-695.json",
        "incomingTeachingRecord": "../n1-reviews/batch-095-combined-teaching-reconciliation-697.json",
        "nativeRecords": ["execution-694.json", "execution-698.json"],
        "combinedAcceptanceRecord": "batch-095-acceptance-699.json",
        "validation": automated["sourceAudit"], "pythonTestsPassed": 372,
        "hostTestsReverified": 4, "nativeTerminalCasesReverified": 3,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "limits": load(S / "batch-095-acceptance-699.json")["limits"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before096.",
    }
    save(S / "batch-095-publication.json", publication)
    ledger = load(S / "batch-095-progress.json")
    ledger["prePublication699State"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=122,
        remainingAdditions=1106, publishedCommit=head, runtimePublished=True,
        publicationRecord="batch-095-publication.json", nextAction=publication["nextAction"],
        pendingGates=["Terminal evidence CI/public ZIP/verified ownerissue; physical-phone/general-release and whole-set outstanding."])
    save(S / "batch-095-progress.json", ledger)
    evidence = load(S / "execution-699.json")
    evidence.update(status=publication["status"], publicationRecord="batch-095-publication.json",
        acceptedCommit=head, counts=counts, ci=ci, immutablePublicArchive=archive,
        runtimePublished=True)
    save(S / "execution-699.json", evidence)
    for path in [L / "archive-download-accepted-699.json",
                 C / "artifacts" / "batch-095-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json"]:
        shutil.copyfile(path, D / path.name)
    p["execution699AcceptedPublication"] = copy.deepcopy(publication)
    p.update(stage="batch-095-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    save(C / "progress.json", p)
    runtime()
    print("Accepted delivery verified; publication ledgers prepared for terminal evidence commit.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-095-publication.json")
    accepted = publication["acceptedCommit"]
    body = f"""Batch **095 ({MEMBER})** is published and verified for bounded owner testing, with ONE necessary new support **解剖 (かいぼう)** and navigation-only addition to existing 解. No vocabulary level inferred from the kanji. TWO all-mapped reciprocal pairs/FOUR directions, zero activated baseline pairs; three direct wordguards 解剖↔分析/分解/検査 retained. Existing identities, primary readings, easier levels, titles and original exclusions preserved.

Authored/initial reviewed `{INITIAL}`. Blind691 same-snapshot independent serial reviews actually **claude-opus-5.5 / gpt-6.1-sol**; original-session695 dependent rendered confirmations and697 incoming-main confirmations retained, NOT new blind credit. OriginalClaude695 overlapping-panel execution remains **REJECTED**, separate smallest serial repair accepted. Optional suggestions, complete reports, actual source/read/visual/process limits preserved; no actionable finding or consequential unresolved in-scope claim. Eleven incoming main articles independently confirmed by both original sessions on frozen6c945042; no etymology consensus invented, partial Kotobank/Daijisen evidence limits explicit.

Combined merge `{publication['combinedContentHead']}`, incomingmain `{MAIN}`. Normally signed accepted publication `{accepted}`; terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards; global romanko-ms unchanged. Combined696 **372Python tests**, validator0errors, vocabulary consistency(**2122/2431 pilot**, NOTfullcoverage), manifest/budget/frozen sources/full baseline/exact membership/all readings/pinnedstrokes/fonts/allmappedlinks/all8441runtimehashes passed. Fresh696 **3RealContentTest+1RareHanTest** passed without skips/failures/errors; these unchanged-tree checks are inherited, NOT rerun699.

Full raw **[ボウ]/[]** and explicit curated **[ボウ]/[]** retained in source order. Only **ぼう**, no kunyomi offered/persistedGood+Done. Other dictionaries' ホウ is not called invalid; no metadata/source substitution. Modern-shape mnemonic not historical etymology. Necessary support distinguishes physical dissection/autopsy from figurative analysis, not every examination.

Inherited694 API35 native routes/fonts/60originalPNG/all32Han/fourfonts, original-session695 rendered confirmations and two terminalcase0 retained. Bounded **64kanji** choices and **384directguard** checks inspected; untested seeds/pools remain **UNVERIFIED**. Exact NEW combined698 full archive through production **ContentSync ONCE**: **1118kanji/5071words/127N1,zeroProblems/acceptedRoomreadingEpoch1/version `{VERSION}`**; one terminalcase0/no skips, three direct guards/384checks/64meaningpoolchecks/TWOreciprocalpairs/FOURdirections pass. Old694 archive/version is not relabeled combined698; localarchive is not publicZIP. Owned emulator stopped, unchanged guards/heaps.

Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, NOTlatestappmain. Emulator/injectedtraces/recallgiveup are **NOT physicalphone/humanhandwriting/successfulMLKit evidence**. Exact fallback face, tool resizing/contactsheet and original source/read limitations remain. No new reviewer/native/host699.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both immutable publicZIPs preserve **all8441runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB/perfile/media/safepath guards, contributor evidence excluded.

Published **122/1228additions;1106remain**. Collection **1118kanji/5071words/127N1labels/132named-source members plus separate妖**. Six separately placed source保/案/派/第/策/結 retain earlierN2levels, not issue60accepted additions; no duplication/relevel. Necessarysupportarticles122project-wide, **NOT an N1vocabularydeck**.

Durable `docs/n1-sources/batch-095-acceptance-699.json`, `batch-095-publication.json`, `execution-699.json` and original691/694/695/696/697/698 evidence. Historical pending flags preserved with scoped discharge, not erased. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock: no childacquisition/deletion/unlock, no optional historical-session helper access. Initial readonly lock probe sharing violation recorded, no retry. Checkpoint699 continues and yields before096; no nextbatch/secondrunner.
"""
    path = C / "batch-095-publication-comment.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-699.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(path)})


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-095-publication-issue-receipt.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-095-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-096-progress.json").exists()
    ledger = load(S / "batch-095-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == [MEMBER]
    publication = load(S / "batch-095-publication.json")
    next_action = (
        f"Batch095 accepted/published/verified at {head}; yield before096. Next coordinator ONE bounded096 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent19008 retainsrunner.lock: no childacquire/delete/unlock or readprobe. "
        "Approvedcontrol/committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/"
        "report/yield actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/"
        "usefulness/baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/"
        "combinedmain/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries"
        "42MiBcompressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published122/1228;1106acceptance-remainder;1118kanji5071words127N1labels132namedmembers+separate妖; "
        "122necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.095剖/necessary解剖/initial8c4e1650/"
        "textual691/native694/rendered695/combined696/incomingteaching697/exactimport698/acceptance699/"
        f"accepted{publication['acceptedCommit']}/version3eebfff0fdad5e28/8441runtimehashes;372Python/"
        "fresh696host4/inheritednative694two+698one/accepted+terminalCI+ZIP/ownerissueverified. No new review/native/"
        "host699. OriginalClaude695overlapREJECTED; serialrepairaccepted, never relabeloriginal. "
        "NEWexactcombined698ContentSyncONCE1118kanji5071words127N1/zeroProblems/epoch1/versionmatchescombined; "
        "384productionWordQuizBuilderdirectguards解剖-分析/分解/検査, bothorientations/directions/All+custom/16seeds. "
        "Fullrawボウ/[]/sourceorder/curation[ボウ]/[]retained;onlyぼう/noKunGood+Done. Otherdictionaryホウnotinvalid/"
        "notnewfrozenmetadata. TWOallmappedpairs/FOURdirections/ZEROactivatedbaselinepairs;existing解navigationonly. "
        "60unchangedcaptures/32Han/fourfonts/694routes/695rendered inherited;contactsheetreductions/toolresizes/"
        "fallbackface/readlimits retained. Elevenincomingmainarticlesconfirmed697bybothoriginalsessions;partial"
        "Kotobank/Daijisenlimits and unresolvedultimate柚etymology attribution preserved;notuniversalconsensus. "
        "InjectedtraceNOThumanhandwriting/no successfulMLKit/no exhaustivepoolsemantics. QualifiedTESTONLY"
        "Android1c1b7bf4 retainsproductionf9b59a2, NOTlatestappmain;compatiblef9b59a2+required. "
        "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No096started/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
        terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextAction=next_action)
    save(C / "batch-095-publication-checkpoint.json", publication)
    save(L / "batch-095-publication-checkpoint.json", publication)
    before, p = load(BEFORE), load(C / "progress.json")
    p["execution699StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 699, "checkpoint": 699, "batch": "095",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "acceptedCommit": publication["acceptedCommit"], "acceptedCi": publication["ci"]["databaseId"],
        "terminalCi": ci["databaseId"], "bothImmutablePublicArchivesVerified": True,
        "runtimeHashesPerArchive": 8441, "reviewedRuntimeBytesUnchanged": True,
        "dedicatedWorktreesClean": True, "allOriginalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before), "ownerIssueAuthorAndBodyVerified": True,
        "issueUpdate": receipt["html_url"], "globalIdentityUnchanged": True,
        "parentLockAcquiredOrModified": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-095-published-verified-before-096", "publishedAdditions": 122,
        "remainingAdditions": 1106, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution699CoordinatorCheckpoint"] = verification
    p["batch095PublicationCheckpoint"] = publication
    p["batch095PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-095-publication-comment.txt"), "verified": True}
    p.update(checkpoint=699, status="continue", stage=verification["stage"],
        lastPublishedCommit=head, remainingAdditions=1106, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = (
        "Remaining1106 issue60 source-bounded additions not review-closed/published; six separately placed "
        "earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. "
        "All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain.")
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions", "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "coordinator-checkpoint-699.json", verification)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({k: v for k, v in verification.items() if k != "nextAction"}, indent=2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "start":
        start()
    elif mode == "gate":
        gate()
    elif mode == "accept":
        accept()
    elif mode == "context":
        context(sys.argv[2])
    elif mode == "verify":
        verify(sys.argv[2], sys.argv[3])
    elif mode == "records":
        records(sys.argv[2])
    elif mode == "comment":
        comment(sys.argv[2])
    elif mode == "finish":
        finish(sys.argv[2])
