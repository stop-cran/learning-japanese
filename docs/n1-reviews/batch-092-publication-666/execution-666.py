"""Publish the accepted batch092; the live launcher retains its lock."""
import copy
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "568dca5b-ba61-4799-87db-7d07b4f7e079"
D = V / "batch-092-publication-666"
HEAD = "948a29a4306fd4adbea734942d2ce68e6d8d7355"
MAIN = "2186eda1bf306c7cc16c1ceca80d273dd893a0bd"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "6246dc622f7139c2a0e16d2e03847d6494391fae"
VERSION = "8445a5717d080dcc"
MEMBER = "\u5208"
BEFORE = L / "progress-before-666.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".666.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
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


def context():
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    script = r"""
$ids=@();$p=$PID;$owned=$false
while($p -gt 0){
    $r=Get-CimInstance Win32_Process -Filter "ProcessId=$p"
    if(-not $r){break}
    $ids+=$r.ProcessId
    if($r.ProcessId -eq 19008){
        $command=$r.CommandLine
        if($command -match '-EncodedCommand ([A-Za-z0-9+/=]+)'){
            $command=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
        }
        $owned=$command.Contains('C:\Users\stop-\n1-kanji-workspace\control\runner.ps1')
        break
    }
    $p=$r.ParentProcessId
}
@{ids=$ids;owned=$owned}|ConvertTo-Json
"""
    ancestry = json.loads(output(["pwsh", "-NoProfile", "-NonInteractive", "-Command", script]))
    assert ancestry["owned"] and 19008 in ancestry["ids"], ancestry
    clean(A, APP)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (665, "092", "continue")
    return ancestry


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8434
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert not git("diff", HEAD, "--", "tools")
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            data = (R / name).read_bytes()
            if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                data = data.replace(b"\r\n", b"\n")
            assert hashlib.sha256(data).hexdigest() == digest, name


def start():
    ancestry = context()
    clean(R, HEAD)
    assert git("rev-parse", "origin/main") == MAIN
    subprocess.run(["git", "merge-base", "--is-ancestor", MAIN, HEAD], cwd=R, check=True)
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["execution665CoordinatorCheckpoint"]["checkpoint"] == 665
    state = {
        "execution": 666, "batch": "092", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME092 owner fast-forward publication, terminal CI, exact public ZIP and verified ownerissue; yield before093. No redundant reviewer/native/host.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and embedded checkpoint parsed; operative contract, complete issue and final665 directly inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial scalar output hit cp1252 after successful parse; bounded UTF-8 output succeeded."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact session verified; no child acquisition/delete/unlock.",
        "ancestry": ancestry,
        "artifactPathPreflight": "Approved control helpers/inputs and committed source/review evidence only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-666.json", state)
    p = load(C / "progress.json")
    p["execution666StartingState"] = state
    p.update(stage="batch-092-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    gate()


def gate():
    context()
    clean(R, HEAD)
    evidence = load(S / "execution-665.json")
    p = load(C / "progress.json")
    assert sha(S / "execution-665.json") == p["execution665CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"], path
    review = load(V / "batch-092-reconciliation.json")
    assert review["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert review["actionableRemainingTeachingFindings"] == 0
    assert review["consequentialUnresolvedTeachingFindings"] == 0
    for report in review["processes"].values():
        assert report["exitCode"] == 0 and report["allAssignedRangesReturned"]
        assert report["observedToolOverlaps"] == 0
        assert sha(V / report["report"]) == report["reportSha256"]
        assert sha(V / report["execution"].replace("-execution.json", ".jsonl")) == report["rawExecutionSha256"]
    inherited = evidence["inheritedAcceptance"]
    assert inherited["nativeTerminalCaseStatuses"] == [0, 0]
    assert inherited["nativeRuntimeMatchesCurrentCombinedTree"]
    route = inherited["nativeRoute"]
    assert (route["contentVersion"], route["archiveRequests"], route["importedKanji"],
            route["importedWords"], route["problems"], route["acceptedReadingParserEpoch"]) == (
        VERSION, 1, 1115, 5070, 0, 1)
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["\u304b\u308b"]
    visual = load(V / "batch-092-visual-reconciliation-664.json")
    assert visual["serialReviewerProcessesExited"] and visual["allToolViewsSerial"]
    assert visual["allAssignedResourcesReturned"] and visual["eachReviewerImagesDecoded"] == 25
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedInScopeClaims"] == 0
    for family, row in visual["processes"].items():
        assert row["exitCode"] == 0 and not row["observedToolOverlaps"] and not row["unfinishedTools"]
        assert sha(V / f"batch-092-visual-664-{family}.md") == row["reportSha256"]
    assert load(S / "batch-092-progress.json")["reviewClosed"] == [MEMBER]
    runtime()
    save(L / "prepublication-gate-666.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G",
        "runtimeHashesVerified": 8434, "combinedReceiptsVerified": len(evidence["receipts"]),
        "initialReportsAndExecutionHashesVerified": 2, "nativeTerminalCasesVerified": 2,
        "inheritedAcceptance": inherited, "parentLockTouched": False, "newReviewerNativeHostRuns": 0,
    })
    print("Starting scope persisted; signed acceptance, source/review receipts and all8434 runtime hashes verified.")


def public(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-092-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8434 and archive["manifestEqual"]
    assert all(archive[k] for k in [
        "allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def verify(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-092-{phase}-ci.json"
    assert not ci_path.exists(), ci_path
    runs = json.loads(output(["gh", "run", "list", "--repo", "stop-cran/learning-japanese",
        "--commit", head, "--workflow", "Validate content", "--limit", "5",
        "--json", "databaseId,status,conclusion,headSha"]))
    assert runs and runs[0]["headSha"] == head, "Exact CI not available; preserve pending checkpoint"
    run = runs[0]
    subprocess.run(["gh", "run", "watch", str(run["databaseId"]), "--repo",
                    "stop-cran/learning-japanese", "--exit-status", "--interval", "10"], check=True)
    ci = json.loads(output(["gh", "run", "view", str(run["databaseId"]), "--repo",
        "stop-cran/learning-japanese", "--json", "databaseId,status,conclusion,headSha,workflowName,jobs"]))
    save(ci_path, ci)
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    path = C / "artifacts" / f"content-{head[:7]}.zip"
    assert not path.exists(), path
    url = f"https://codeload.github.com/stop-cran/learning-japanese/legacy.zip/{head}"
    result = subprocess.run(["curl.exe", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "180", url, "--output", str(path)], capture_output=True, text=True)
    save(L / f"archive-download-{phase}-666.json", {
        "commit": head, "url": url, "exitCode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
        head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-092-publication.json").exists()
    D.mkdir()
    p, before = load(C / "progress.json"), load(BEFORE)
    evidence = load(S / "execution-665.json")
    ledger_path = S / "batch-092-progress.json"
    ledger = load(ledger_path)
    previous = load(S / "batch-091-publication.json")
    counts = dict(evidence["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=119, remainingAdditions=1109,
        batchNewNecessarySupportWords=0,
        projectNewNecessarySupportWords=previous["counts"]["projectNewNecessarySupportWords"],
        batchChangedReusedArticles=1, allMappedReciprocalPairs=1, mappedDirectedLinks=2,
        activatedBaselinePairs=1, separateExceptionPreserved="\u5996",
        separateEarlierLevelSourceMembers=evidence["sourceAudit"]["separateEarlierLevelSourceMembers"],
        earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (1115, 5070, 124, 129)
    limits = {
        "combined": evidence["limits"],
        "inherited": evidence["inheritedAcceptance"]["originalLimits"],
        "clarification": "Historical pending flags preserved, not erased: combined665 and accepted/terminal666 receipts discharge only their recorded scope. All source/read/native/font/Paintprobe/injectedtrace/MLKit/phone limitations remain.",
    }
    publication = {
        "schemaVersion": 1, "execution": 666, "batch": "092", "membership": [MEMBER],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": before["execution659CoordinatorCheckpoint"]["savedCommit"],
        "initialReviewedTeachingSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "combinedContentHead": evidence["combinedContentHead"], "latestMainIntegrated": MAIN,
        "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"] for n in range(658, 666)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-092-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-092-visual-reconciliation-664.json",
        "nativeRecord": "execution-663.json", "combinedAcceptanceRecord": "execution-665.json",
        "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits, "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before093.",
    }
    save(S / "batch-092-publication.json", publication)
    ledger["prePublicationCheckpoint666"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=119,
        remainingAdditions=1109, publishedCommit=HEAD, runtimePublished=True,
        publicationRecord="batch-092-publication.json",
        pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
        nextAction=publication["nextAction"], publicationClarification=limits["clarification"])
    save(ledger_path, ledger)
    receipts = []
    for name, tool in [("validate", "tools\\validate.py"), ("manifest", "tools\\build_manifest.py"),
                       ("budget", "tools\\check_content_budget.py")]:
        path = D / f"{name}-666.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", tool], cwd=R,
                stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    save(S / "execution-666.json", {
        "schemaVersion": 1, "execution": 666, "batch": "092", "status": publication["status"],
        "startingState": p["execution666StartingState"], "publicationRecord": "batch-092-publication.json",
        "acceptedCommit": HEAD, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-665.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "newReviewNativeHostRuns": 0, "limits": limits,
        "terminalLocalValidation": receipts, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False})
    for path in [L / "prepublication-gate-666.json", L / "starting-state-666.json",
        L / "archive-download-accepted-666.json", C / "artifacts" / "batch-092-accepted-ci.json",
        C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json", C / "verify-batch-002-publication.py",
        C / "publish-666.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-092-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution666AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Accepted delivery verified; durable publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-092-publication.json")
    body = f"""Batch **092 ({MEMBER})** is published and verified for bounded owner testing. Existing N3 support **{MEMBER}\u308b (\u304b\u308b), mow; shear** was reused: one activated baseline/all-mapped reciprocal pair, two directions. No new support word; original \u5207\u308b exclusion retained and direct \u53ce\u7a6b exclusion added for overlapping answer labels. No vocabulary releveling.

Authored and independently reviewed teaching `{TEACHING}` unchanged. Two serial blind textual660 reviews: actual **Claude Opus5.5 / GPT6.1Sol**, each same full162352byte/3624line packet,75complete dictionary families,6rawcharacters and13completearticles via one full-file view; exact access is not equal comprehension or independent upstream retrieval. Both complete original reports, optional polish and limits retained; no mandatory finding or teaching correction. Original-session serial dependent rendered664 confirmations are NOT new blind review credit: each27serialviews/25decodedoriginalPNGs,22distinctsourceimages, exit0/nooverlap.

Combined665 head `{publication['combinedContentHead']}`, freshmain `{MAIN}` already ancestral, no substantive merge. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped normal fast-forwards; global account unchanged. Combined665 **372Python tests**, validator0errors, vocabulary consistency(pilot2122/2431, not full coverage), fresh manifest/budget/frozen sources/full baseline/exact membership/all3rawreadings/onepair/twodirections/directguards/pinned4strokes/16Han fontprovenance/all8434runtimehashes passed. Fresh665 **3RealContentTest+1RareHanTest** passed without skips/failures/errors. No reviewer/host/native rerun666.

Full raw **\u30ac\u30a4/\u30ab\u30a4; \u304b.\u308b** source order retained in full/Lite projections. Only selected **\u304b\u308b**, with own linked existing article, scheduled; on prompts explicitly empty. Both \u5208\u9664 (\u304c\u3044\u3058\u3087/\u304b\u3044\u3058\u3087) recognized/unselected, no invented obsolete/frequency ranking. Cutting growing things versus all harvesting explained; shape-only mnemonic not history, canonical\u5200 radical18 versus visible\u5202.

Inherited663 fullarchive62c6d3e2 through production **ContentSync ONCE**:1115kanji/5070words/124N1,zeroProblems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged runtime; **TWO terminalcase0/no skips**. N1 selection/meaning/onlykun\u304b\u308bGood+Done/noonkey/fourinjectedreference strokes/recallgiveup/both complete article projections/two reciprocal transitions/SystemBack/offline covered within recorded scope. N1/All production choices use \u4e43/\u51f9/\u51f8, all3curatedavailable/zero fallback; not future/custom-pool certification.

All16scopedHan in3actualComposepanels/4productionfontselections readable including fallbackU+5202\u5202. Reviewed25of42PNGs,17notseparatelyviewed; toolresized1080x2400to900x2000, wordbodyheadingnotseparatelypictured and complementary horizontallyscrolled table limits retained. 64individual+4wholewordPaint probes are NOT68viewedPNGs or identifiedfallbackface. Injectedtrace/recallgiveup is **not humanhandwriting/successfulMLKit/physical-phone evidence**; actualUI says modelunavailable/shape-onlygrading. Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, NOTlatestappmain. API35emulator is not phone acceptance.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable publicZIPs preserve **all8434runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus perfile/media/safepath guards; contributor evidence excluded.

Published **119/1228additions;1109remain**. Collection **1115kanji/5070words/124N1labels/129named-source members plus separate\u5996**. Six separately placed earlierN2source members\u4fdd/\u6848/\u6d3e/\u7b2c/\u7b56/\u7d50 preserved, not issue60accepted additions; do not duplicate/relevel. Necessarysupportarticles remain121project-wide, **not an N1vocabularydeck**.

Durable evidence: `docs/n1-sources/batch-092-publication.json`, `execution-666.json`, original660textual/663native/664rendered/665combined records. All original source/lookup/readdepth/font/Paintprobe/MLKit/phone limitations retained. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock, no child lock or optional historical-session helper access. Checkpoint666 persists continue and yields before093; no nextbatch/secondrunner.
"""
    target = C / "batch-092-publication-comment.txt"
    assert not target.exists()
    target.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-666.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-092-publication-issue-receipt.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-092-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-093-progress.json").exists()
    ledger = load(S / "batch-092-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == [MEMBER]
    publication = load(S / "batch-092-publication.json")
    next_action = (
        f"Batch092 accepted/published/verified at {head}; yield before093. Next coordinator ONE bounded093 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent19008 retainsrunner.lock: no childacquire/delete/unlock. Approvedcontrol/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield actual"
        "newdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/baseline/"
        "fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/two serialblind"
        "differentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published119/1228;1109acceptance-remainder;1115kanji5070words124N1labels129namedmembers+separate妖; "
        "121necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.092teaching6246dc62/textual660/native663/"
        "rendered664/combined665/accepted948a29a4/version8445a5717d080dcc/8434runtimehashes; "
        "372Python/fresh665host4/inherited663native2/accepted+terminalCI+ZIP/ownerissueverified. "
        "No freshreview/native/host666. OriginalClaude/GPT reports/optionalpolish/sourceandreadlimits retained. "
        "FullContentSyncONCE1115kanji5070words124N1/zeroProblems/epoch1/versionmatchescombined. "
        "Fullrawガイカイ/か.る sourceorderretained; onlykunかるGood+Done,noon;both刈除readingsrecognizedunselected. "
        "Oneallmappedbaselinepair/twodirections/original切るguard+newdirect収穫guard; no supportaddition/relevel. "
        "All16Han/3Composepanels/4productionfonts inclfallback刂readable;25of42PNGsviewed/17notseparatelyviewed/"
        "resized900x2000/wordbodyheadingnotseparatelypictured. 64individual+4wholewordPaintprobesNOT68PNGs/"
        "fallbackfaceunknown/injectedtraceNOT humanhandwriting/no successfulMLKit. QualifiedTESTONLYAndroid"
        "1c1b7bf4 retainsproductionf9b59a2, NOTlatestappmain. All original source/read/native/font/pool/phone"
        "qualifications remain in publication666 and execution665. Physicalphone/generalrelease/whole-set"
        "outstanding; projectincomplete. No093started/authoragents/concurrentheavywork/secondrunner/"
        "signingretry/guardincrease."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
        terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextAction=next_action)
    save(C / "batch-092-publication-checkpoint.json", publication)
    save(L / "batch-092-publication-checkpoint.json", publication)
    before, p = load(BEFORE), load(C / "progress.json")
    p["execution666StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 666, "checkpoint": 666, "batch": "092",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8434,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-092-published-verified-before-093",
        "publishedAdditions": 119, "remainingAdditions": 1109, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution666CoordinatorCheckpoint"] = verification
    p["batch092PublicationCheckpoint"] = publication
    p["batch092PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-092-publication-comment.txt"), "verified": True}
    p.update(checkpoint=666, status="continue", stage=verification["stage"],
        lastPublishedCommit=head, remainingAdditions=1109, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1109 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "coordinator-checkpoint-666.json", verification)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({k: v for k, v in verification.items() if k != "nextAction"}, indent=2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "start":
        start()
    elif mode == "gate":
        gate()
    elif mode == "verify":
        verify(sys.argv[2], sys.argv[3])
    elif mode == "records":
        records()
    elif mode == "comment":
        comment(sys.argv[2])
    elif mode == "finish":
        finish(sys.argv[2])
    else:
        raise ValueError(mode)
