"""Publish only accepted batch090; the live launcher retains runner.lock."""
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
L = C / "logs" / "6fc9a750-fe67-4502-b364-cc379749aa8c"
D = V / "batch-090-publication-644"
HEAD = "dd91f984c1f8299752a909911b192c846b8d5429"
MAIN = "ebfd48dc911f32be0eeb9426db2f2d35a9084044"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "e044e953133548dd37fdf1dba449de2f4ee7575f"
VERSION = "ceee0f79a6d394df"
BEFORE = L / "progress-before-644.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".644.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (643, "090", "continue")
    return ancestry


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8429
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert not git("diff", HEAD, "--", "tools")


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
    assert embedded["checkpoint"] == 643
    state = {
        "execution": 644, "batch": "090", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME090 owner fast-forward publication, terminal CI, exact public ZIP and verified ownerissue; yield before091. No new reviewer/native/host absent change.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and embedded checkpoint parsed; operative contract, complete issue and final643 directly inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial display hit cp1252 encoding; final checkpoint subsequently read directly."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact session verified; no child acquisition/delete/unlock.",
        "ancestry": ancestry,
        "artifactPathPreflight": "Approved control helpers/inputs and committed source/review evidence only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-644.json", state)
    p = load(C / "progress.json")
    p["execution644StartingState"] = state
    p.update(stage="batch-090-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    gate()


def gate():
    context()
    clean(R, HEAD)
    evidence = load(S / "execution-643.json")
    p = load(C / "progress.json")
    assert sha(S / "execution-643.json") == p["execution643CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"], path
    reports = evidence["inheritedAcceptance"]["initialReviewReports"]
    assert {m for r in reports.values() for m in r["actualModels"]} == {"claude-opus-5.5", "gpt-6.1-sol"}
    for report in reports.values():
        assert report["exitCode"] == 0 and report["allAssignedRangesReturned"]
        assert sha(V / report["report"]) == report["reportSha256"]
        execution = load(V / report["execution"])
        assert execution["rawExecutionSha256"] == report["rawExecutionSha256"]
        assert execution["actualModels"] == report["actualModels"]
        assert sha(V / report["execution"].replace("-execution.json", ".jsonl")) == report["rawExecutionSha256"]
    assert evidence["inheritedAcceptance"]["nativeTerminalCaseStatuses"] == [0, 0]
    assert evidence["inheritedAcceptance"]["nativeRuntimeMatchesCurrentCombinedTree"]
    review = load(V / "batch-090-reconciliation.json")
    assert review["actionableRemainingTeachingFindings"] == 0
    assert review["consequentialUnresolvedTeachingFindings"] == 0
    visual = load(V / "batch-090-visual-reconciliation-642.json")
    assert visual["status"] == "dependent-visual-review-closed-awaiting-combined-acceptance"
    assert not visual["findings"] and visual["serialReviewerProcessesExited"]
    assert evidence["inheritedAcceptance"]["visualEvidence"] == "docs/n1-reviews/batch-090-visual-reconciliation-642.json"
    assert load(S / "batch-090-progress.json")["reviewClosed"] == ["刀"]
    runtime()
    save(L / "prepublication-gate-644.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G",
        "runtimeHashesVerified": 8429, "combinedReceiptsVerified": len(evidence["receipts"]),
        "initialReportsAndExecutionHashesVerified": 2, "nativeTerminalCasesVerified": 2,
        "inheritedAcceptance": evidence["inheritedAcceptance"],
        "parentLockTouched": False, "newReviewerNativeHostRuns": 0,
    })
    print("Starting scope persisted; signed acceptance, source/review receipts and all8429 runtime hashes verified.")


def public(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-090-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8429 and archive["manifestEqual"]
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
    ci_path = C / "artifacts" / f"batch-090-{phase}-ci.json"
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
    save(L / f"archive-download-{phase}-644.json", {
        "commit": head, "url": url, "exitCode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
        head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-090-publication.json").exists()
    D.mkdir()
    p, before = load(C / "progress.json"), load(BEFORE)
    evidence = load(S / "execution-643.json")
    ledger_path = S / "batch-090-progress.json"
    ledger = load(ledger_path)
    previous = load(S / "batch-089-publication.json")
    counts = dict(evidence["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=117, remainingAdditions=1111,
        batchNewNecessarySupportWords=1,
        projectNewNecessarySupportWords=previous["counts"]["projectNewNecessarySupportWords"] + 1,
        batchChangedReusedArticles=4, allMappedReciprocalPairs=5, mappedDirectedLinks=10,
        activatedBaselinePairs=2, separateExceptionPreserved="妖",
        separateEarlierLevelSourceMembers=evidence["sourceAudit"]["separateEarlierLevelSourceMembers"],
        earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (1113, 5069, 122, 127)
    limits = {
        "combined": evidence["limits"],
        "sourceText": evidence["inheritedAcceptance"]["inheritedSourceTextLimits"],
        "visual": evidence["inheritedAcceptance"]["inheritedVisualLimits"],
        "visualDispositions": evidence["inheritedAcceptance"]["visualDispositions"],
        "clarification": "Historical pending flags preserved, not erased: combined643 and accepted/terminal644 receipts discharge only their recorded scope. Every original source/process/denial/OOM/read-depth/downscale/font/pool/MLKit/phone qualification and optional disposition remains.",
    }
    publication = {
        "schemaVersion": 1, "execution": 644, "batch": "090", "membership": ["刀"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": TEACHING, "initialReviewedTeachingSnapshot": TEACHING,
        "reviewedTeachingSnapshot": TEACHING, "combinedContentHead": evidence["combinedContentHead"],
        "latestMainIntegrated": MAIN, "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"] for n in range(636, 644)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-090-reconciliation.json",
        "visualRecord": "../n1-reviews/batch-090-visual-reconciliation-642.json",
        "combinedAcceptanceRecord": "execution-643.json", "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits, "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before091.",
    }
    save(S / "batch-090-publication.json", publication)
    ledger["prePublicationCheckpoint644"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["刀"], publishedAdditions=117,
        remainingAdditions=1111, publishedCommit=HEAD, runtimePublished=True,
        publicationRecord="batch-090-publication.json",
        pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
        nextAction=publication["nextAction"], publicationClarification=limits["clarification"])
    save(ledger_path, ledger)
    for name in ["batch-090-reconciliation.json", "batch-090-visual-reconciliation-642.json"]:
        path = V / name
        review = load(path)
        review["prePublicationState644"] = {k: copy.deepcopy(review[k]) for k in
            ("status", "runtimeAccepted", "runtimePublished", "limits") if k in review}
        review.update(status=publication["status"], runtimePublished=True,
            publicationRecord="../n1-sources/batch-090-publication.json",
            publicationClarification=limits["clarification"])
        save(path, review)
    receipts = []
    for name, tool in [("validate", "tools\\validate.py"), ("manifest", "tools\\build_manifest.py"),
                       ("budget", "tools\\check_content_budget.py")]:
        path = D / f"{name}-644.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", tool], cwd=R,
                stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    save(S / "execution-644.json", {
        "schemaVersion": 1, "execution": 644, "batch": "090", "status": publication["status"],
        "startingState": p["execution644StartingState"], "publicationRecord": "batch-090-publication.json",
        "acceptedCommit": HEAD, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-643.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "newReviewNativeHostRuns": 0, "limits": limits,
        "terminalLocalValidation": receipts, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False})
    for path in [L / "prepublication-gate-644.json", L / "starting-state-644.json",
        L / "archive-download-accepted-644.json", C / "artifacts" / "batch-090-accepted-ci.json",
        C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json", C / "verify-batch-002-publication.py",
        C / "publish-644.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-090-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution644AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Accepted delivery verified; durable publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-090-publication.json")
    body = f"""Batch **090 (刀)** is published and verified for bounded owner testing, with necessary support **日本刀 (にほんとう), Japanese sword**. Four changed reused navigation passages only (日/本/刀/剃刀), five all-mapped reciprocal pairs/ten directions, two activated baseline pairs and one direct 日本刀–刀 word guard. Existing 刀 N3, 剃刀 N2 and 鋭い guard preserved; no inferred vocabulary level.

Authored/two-family independently reviewed teaching `{TEACHING}`; textual638/native641/original-session visual642/combined643 evidence retained. Main `{MAIN}` was already an ancestor; normal nonrewriting merge Already up to date, no teaching change. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global account unchanged.

Original blind **Claude Opus5.5 / GPT6.1Sol** initial reviews and serial dependent original-session visuals retained, not new blind credit. Both initial packets returned completely; hashes establish bytes, not equal comprehension. Both complete new articles and only four changed reused passages are review-closed. Each original visual reviewer decoded14PNGs (11contact sheets covering64captures plus3font panels); Claude used compacted same-session notes for first4sheets. Original read/provenance limits and downscaling preserved; no actionable scoped finding remains.

Combined643 **372Python tests**, validator0errors, vocabulary consistency (pilot2122/2431, not full coverage), fresh manifest, exact source/baseline/membership/all3readings/5pairs10directions/1guard/pinned2strokes/18Han provenance passed. Fresh643 **3RealContentTest+1RareHanTest** passed without skips/failures/errors. No reviewer/host/native rerun644. Inherited641 two named native terminalcase0 used fullarchive40bc5a55 through productionContentSync **ONCE**,1113kanji/5069words/122N1,zeroProblems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged combined runtime.

Raw **トウ/かたな/そり** retained in full/Lite sourceorder; only selected **とう/かたな** scheduled Good/2of2done with own linked rows. Source-onlyそり excluded without invented allocation from jukujikun剃刀. 日本刀 is a traditionalJapaneseSword noun; neutral museum/photo sentences, lexical日本modifier+sword, bothにほんとう/にっぽんとう without frequency ranking or universal sound-change/shape rule. Actual N1 and All choices **刀 sword; blade** versus **乃 thereupon; possessive no / 凹 concave; sunken / 凸 convex; protruding**, all3curatedavailable/zero fallback; not future/custom-pool certification.

Native N1 selection/meaning/curatedreading/twostroke injectedtrace/recallgiveup/both complete articles/changed reused passages/5pairs10directions/oneguard/SystemBack/offline covered within recorded scope. All18Han readable/distinguishable in fourproductionComposefonts, including刀 versus力. Fallbackface unknown; **76Paint hash probes are NOT76separately viewedPNGs**; contact sheets downscaled. Injectedtrace/giveup is **not humanhandwriting/successful recall/offlineMLKit/phone evidence**. Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, not latestappmain. First641 escaping failure before device launch remains historical, not permissiondenial/lockrecovery. No heap/guard increase or productionapp change.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable publicZIPs preserve **all8429runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus perfile/media/safepath guards; contributor evidence excluded.

Published **117/1228additions;1111remain**. Collection **1113kanji/5069words/122N1labels/127named-source members plus separate妖**. Six separate earlierN2source members保/案/派/第/策/結 remain preserved, not issue60accepted additions; do not duplicate/relevel. This batch adds1necessarysupportarticle,120project-wide, **not an N1vocabularydeck**.

Durable evidence: `docs/n1-sources/batch-090-publication.json`, `execution-644.json`, original638textual/639host/640fixture/641native/642visual/643combined records. All original source/lookup/process/denial/OOM/readdepth/downscale/font/pool/phone limitations and optional dispositions retained. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock, no child lock or optional historical-session helper access. Checkpoint644 persists continue and yields before091; no nextbatch/secondrunner.
"""
    target = C / "batch-090-publication-comment.txt"
    assert not target.exists()
    target.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-644.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-090-publication-issue-receipt.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-090-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-091-progress.json").exists()
    ledger = load(S / "batch-090-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == ["刀"]
    publication = load(S / "batch-090-publication.json")
    next_action = (
        f"Batch090 accepted/published/verified at{head}; yield before091. Next coordinator ONE bounded091 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "exactsession. Parent19008 retainsrunner.lock: no childacquire/delete/unlock. Approvedcontrolhelpers/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield "
        "actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/"
        "baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "two serialblinddifferentfamilies/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/original18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published117/1228;1111acceptance-remainder;1113kanji5069words122N1labels127namedmembers+separate妖; "
        "120necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.090initiale044e953/638textual/639host/"
        "640fixture/641native/642visual/643combined/accepteddd91f984/versionceee0f79a6d394df/8429hashes; "
        "372Python/fresh643host4/inherited641native2/original642visuals/accepted+terminalCI+ZIP/ownerissueverified. "
        "No freshreview/native/host644. FullContentSyncONCE1113kanji5069words122N1/zeroProblems/epoch1/"
        "versionmatchescombined. Rawトウ/かたな/そり in fullLitesourceorder; only selectedとう/かたな "
        "Good/2of2done; sourceonlyそり excluded without invented jukujikun剃刀allocation. "
        "TraditionalJapaneseSwordnoun/neutralmuseumphotos/日本modifier+sword/bothにほんとうにっぽんとう "
        "withoutfrequencyranking/universalsoundchange/shape rule. Bothnewarticles/only4changedreused/"
        "5pairs10directions/2activatedbaselinepairs/1direct日本刀-刀guard; existing刀N3/剃刀N2/鋭いguard "
        "preserved. N1/All productionall3curatedzeroFallback乃/凹/凸 versus sword;blade; notfuturecustompools. "
        "All18Han/fourComposefonts incl刀versus力readable; fallbackfaceunknown/contactsheetsdownscaled; "
        "76Painthashes NOT76separatelyviewedPNGs. Twoinjectedtrace/recallgiveup NOThumanhandwriting/MLKit/phone. "
        "OriginalClaude first4visualsheets used compacted same-session notes; not equalfreshreadclaim. "
        "QualifiedTESTONLYAndroid1c1b7bf4 retainsproductionf9b59a2, notlatestappmain. First641wrapperfailure "
        "beforedevicelaunch remains historical, notdenial/lockrecovery. Every original source/process/denial/"
        "OOM/readdepth/downscale/native/pool/phone qualification andoptionaldisposition preserved in "
        "docs/n1-sources/batch-090-publication.json and execution-643.json. Physicalphone/generalrelease/"
        "whole-setoutstanding; projectincomplete. No091started/authoragents/concurrentheavywork/secondrunner/"
        "signingretry/guardincrease."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
        terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextAction=next_action)
    save(C / "batch-090-publication-checkpoint.json", publication)
    save(L / "batch-090-publication-checkpoint.json", publication)
    before, p = load(BEFORE), load(C / "progress.json")
    p["execution644StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 644, "checkpoint": 644, "batch": "090",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8429,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-090-published-verified-before-091",
        "publishedAdditions": 117, "remainingAdditions": 1111, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution644CoordinatorCheckpoint"] = verification
    p["batch090PublicationCheckpoint"] = publication
    p["batch090PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-090-publication-comment.txt"), "verified": True}
    p.update(checkpoint=644, status="continue", stage=verification["stage"],
        lastPublishedCommit=head, remainingAdditions=1111, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1111 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-verification-644.json", verification)
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
