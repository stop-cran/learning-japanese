"""Publish accepted batch 089 under the live parent runner's lock."""
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
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
L = C / "logs" / "59921a8c-a9b8-42f1-8718-5f2831af7054"
D = V / "batch-089-publication-635"
HEAD = "6e972c1a148abf4dc918f6dd86ba1a8b524ce8b9"
MAIN = "703ebf5fba412aefdc516ea18b36658d227631d1"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "4b84608b5ca8889d45a176667975524f6645bd8d"
VERSION = "c6562f11cb371053"
BEFORE = L / "progress-before-635.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".635.tmp")
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
    command = (
        "$ids=@();$p=$PID;for($i=0;$i -lt 12 -and $p;$i++){"
        '$r=Get-CimInstance Win32_Process -Filter "ProcessId=$p";'
        "if(-not $r){break};$ids+=$r.ProcessId;$p=$r.ParentProcessId};"
        "ConvertTo-Json -InputObject $ids"
    )
    ids = json.loads(output(["pwsh", "-NoProfile", "-NonInteractive", "-Command", command]))
    assert 19008 in ids, ids
    clean(A, APP)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (634, "089", "continue")
    return ids


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8426
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert not git("diff", HEAD, "--", "tools")


def start():
    ids = context()
    clean(R, HEAD)
    assert git("rev-parse", "origin/main") == MAIN
    subprocess.run(["git", "merge-base", "--is-ancestor", MAIN, HEAD], cwd=R, check=True)
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 634
    state = {
        "execution": 635, "batch": "089", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME089 normal owner fast-forward publication and exact CI/public ZIP/owner issue verification; yield before090. No new reviewer/native/host absent change.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete approved issue and final634 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact current session verified; no child acquisition/delete/unlock.",
        "ancestryPids": ids,
        "artifactPathPreflight": "Approved control helpers, committed source/review packets and frozen workspace inputs only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-635.json", state)
    p = load(C / "progress.json")
    p["execution635StartingState"] = state
    p.update(stage="batch-089-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    gate()


def gate():
    context()
    clean(R, HEAD)
    p = load(C / "progress.json")
    evidence = load(S / "execution-634.json")
    assert sha(S / "execution-634.json") == p["execution634CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"], path
    reports = evidence["inheritedAcceptance"]["initialReviewReports"]
    assert {m for r in reports.values() for m in r["actualModels"]} == {
        "claude-opus-5.5", "gpt-6.1-sol"}
    for report in reports.values():
        assert report["exitCode"] == 0 and report["allAssignedRangesReturned"]
        assert sha(V / report["report"]) == report["reportSha256"]
        execution = load(V / report["execution"])
        assert execution["rawExecutionSha256"] == report["rawExecutionSha256"]
        assert execution["actualModels"] == report["actualModels"]
        raw = V / report["execution"].replace("-execution.json", ".jsonl")
        assert sha(raw) == report["rawExecutionSha256"]
    assert evidence["inheritedAcceptance"]["nativeTerminalCaseStatuses"] == [0, 0]
    review = load(V / "batch-089-reconciliation.json")
    assert review["actionableRemainingTeachingFindings"] == 0
    assert review["consequentialUnresolvedTeachingFindings"] == 0
    visual = load(V / "batch-089-visual-reconciliation-633.json")
    assert visual["status"] == "dependent-visual-review-closed-awaiting-combined-acceptance"
    assert not visual["findings"] and visual["serialReviewerProcessesExited"]
    assert evidence["inheritedAcceptance"]["visualEvidence"] == (
        "docs/n1-reviews/batch-089-visual-reconciliation-633.json")
    assert load(S / "batch-089-progress.json")["reviewClosed"] == ["凶"]
    runtime()
    save(L / "prepublication-gate-635.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G",
        "runtimeHashesVerified": 8426, "combinedReceiptsVerified": len(evidence["receipts"]),
        "initialReportsAndExecutionHashesVerified": 2, "nativeTerminalCasesVerified": 2,
        "inheritedAcceptance": evidence["inheritedAcceptance"],
        "parentLockTouched": False, "newReviewerNativeHostRuns": 0,
    })
    print("Starting scope persisted; signed acceptance, source/review receipts and all8426 runtime hashes verified.")


def public(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-089-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8426 and archive["manifestEqual"]
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
    ci_path = C / "artifacts" / f"batch-089-{phase}-ci.json"
    assert not ci_path.exists(), ci_path
    runs = json.loads(output(
        ["gh", "run", "list", "--repo", "stop-cran/learning-japanese", "--commit", head,
         "--workflow", "Validate content", "--limit", "5", "--json",
         "databaseId,status,conclusion,headSha"]))
    assert runs and runs[0]["headSha"] == head, "Exact CI not available; preserve pending checkpoint"
    run = runs[0]
    subprocess.run(["gh", "run", "watch", str(run["databaseId"]), "--repo",
                    "stop-cran/learning-japanese", "--exit-status", "--interval", "10"], check=True)
    ci = json.loads(output(
        ["gh", "run", "view", str(run["databaseId"]), "--repo", "stop-cran/learning-japanese",
         "--json", "databaseId,status,conclusion,headSha,workflowName,jobs"]))
    save(ci_path, ci)
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    download(phase, head, f"https://api.github.com/repos/stop-cran/learning-japanese/zipball/{head}")


def download(phase, head, url):
    context()
    clean(R, head)
    runtime()
    ci = load(C / "artifacts" / f"batch-089-{phase}-ci.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    path = C / "artifacts" / f"content-{head[:7]}.zip"
    assert not path.exists(), path
    result = subprocess.run(["curl.exe", "--fail", "--location", "--silent", "--show-error",
                             "--max-time", "180", url, "--output", str(path)],
                            capture_output=True, text=True)
    save(L / f"archive-download-{phase}-635.json", {
        "commit": head, "url": url, "exitCode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr,
        "earlierAttempt": "Accepted-head API zipball returned HTTP504/curl22 after greenCI; no archive accepted. Direct GitHub codeload retry uses the same immutable commit, not different source bytes or relaxed guards."
        if phase == "accepted" else None,
    })
    result.check_returncode()
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
                    head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-089-publication.json").exists()
    D.mkdir()
    p = load(C / "progress.json")
    before = load(BEFORE)
    evidence = load(S / "execution-634.json")
    ledger_path = S / "batch-089-progress.json"
    ledger = load(ledger_path)
    previous = load(S / "batch-088-publication.json")
    counts = dict(evidence["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=116, remainingAdditions=1112,
                  batchNewNecessarySupportWords=1,
                  projectNewNecessarySupportWords=previous["counts"]["projectNewNecessarySupportWords"] + 1,
                  batchChangedReusedArticles=1, allMappedReciprocalPairs=2, mappedDirectedLinks=4,
                  activatedBaselinePairs=0, separateExceptionPreserved="妖",
                  separateEarlierLevelSourceMembers=evidence["sourceAudit"]["separateEarlierLevelSourceMembers"],
                  earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (
        1112, 5068, 121, 126)
    limits = {
        "combined": evidence["limits"],
        "sourceText": evidence["inheritedAcceptance"]["inheritedSourceTextLimits"],
        "visual": evidence["inheritedAcceptance"]["inheritedVisualLimits"],
        "visualDispositions": evidence["inheritedAcceptance"]["visualDispositions"],
        "clarification": "Historical pending gates remain historical, not erased: combined634 and accepted/terminal635 receipts discharge only their recorded scope. Original source/process/denial/OOM/read-depth/downscale/font/pool/MLKit/phone limitations and optional dispositions remain.",
    }
    publication = {
        "schemaVersion": 1, "execution": 635, "batch": "089", "membership": ["凶"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": TEACHING, "initialReviewedTeachingSnapshot": TEACHING,
        "reviewedTeachingSnapshot": TEACHING, "combinedContentHead": evidence["combinedContentHead"],
        "latestMainIntegrated": MAIN, "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"]
                      for n in range(627, 635)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-089-reconciliation.json",
        "visualRecord": "../n1-reviews/batch-089-visual-reconciliation-633.json",
        "combinedAcceptanceRecord": "execution-634.json", "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits, "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before090.",
    }
    save(S / "batch-089-publication.json", publication)
    ledger["prePublicationCheckpoint635"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["凶"], publishedAdditions=116,
                  remainingAdditions=1112, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-089-publication.json",
                  pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
                  nextAction=publication["nextAction"], publicationClarification=limits["clarification"])
    save(ledger_path, ledger)
    for name in ["batch-089-reconciliation.json", "batch-089-visual-reconciliation-633.json"]:
        path = V / name
        review = load(path)
        review["prePublicationState635"] = {k: copy.deepcopy(review[k]) for k in
                                           ("status", "runtimeAccepted", "runtimePublished", "limits") if k in review}
        review.update(status=publication["status"], runtimePublished=True,
                      publicationRecord="../n1-sources/batch-089-publication.json",
                      publicationClarification=limits["clarification"])
        save(path, review)
    receipts = []
    for name, tool in [("validate", "tools\\validate.py"), ("manifest", "tools\\build_manifest.py"),
                       ("budget", "tools\\check_content_budget.py")]:
        path = D / f"{name}-635.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", tool], cwd=R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    execution = {
        "schemaVersion": 1, "execution": 635, "batch": "089", "status": publication["status"],
        "startingState": p["execution635StartingState"], "publicationRecord": "batch-089-publication.json",
        "acceptedCommit": HEAD, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-634.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "newReviewNativeHostRuns": 0, "limits": limits,
        "diagnostics": [
            "Initial prepublication check stopped before any push on visual633's historical runtimeAcceptedForPublication=false, which correctly preceded combined634. Checked visual closure and its explicit linkage from accepted634 instead; retained the historical633 flag and every acceptance gate.",
            "Accepted-head API zipball download returned HTTP504/curl22 after greenCI. Preserved failure and used direct GitHub codeload for the same immutable commit; every runtimehash/manifest/guard still verified."
        ],
        "terminalLocalValidation": receipts, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    save(S / "execution-635.json", execution)
    for path in [L / "prepublication-gate-635.json", L / "starting-state-635.json",
                 L / "archive-download-accepted-635.json",
                 C / "artifacts" / "batch-089-accepted-ci.json",
                 C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json",
                 C / "verify-batch-002-publication.py", C / "publish-635.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-089-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution635AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Public accepted delivery verified; durable publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-089-publication.json")
    body = f"""Batch **089 (凶)** is published and verified for bounded owner testing, with necessary support **凶作 (きょうさく), crop failure** and the additive **作** navigation line only. Two all-mapped reciprocal pairs/four directions, one direct word guard, no activated baseline pair or inferred vocabulary level.

Authored/independently reviewed teaching `{TEACHING}`; textual closure `{publication['snapshots']['629']}`; native evidence `{publication['snapshots']['632']}`; original-session visual closure `{publication['snapshots']['633']}`. Main `{MAIN}` was already an ancestor; normal nonrewriting merge Already up to date, no teaching change. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global account unchanged.

Original blind **Claude Opus5.5 / GPT6.1Sol** initial reviews and serial dependent original-session visuals retained, not new blind credit. Identical173695byte/3568line packet included73completeJMdictfamilies,6rawcharacters and14completearticlebodies including2new and1changedreused. Both firstcalls returned the exact full packet; bytes do not prove equal comprehension. GPT's three redundant overlapping serialtailreads/two truncatedtailresponses remain recorded; no missing assigned range or parallel tools. Each original reviewer decoded11PNGs: eight downscaled contact sheets cover43captures and three original font panels. No actionable scoped teaching defect remains; original strongerword/crop-sense/crimeweapon/wrapping/table suggestions remain optional.

Combined-tree **372Python tests**, validator0errors, vocabulary consistency (pilot2122/2431, not full coverage), fresh manifest, exact source/baseline/membership, sole reading/two pairs/four directions/one guard/pinned4strokes/font provenance passed. Fresh634 **3RealContentTest+1RareHanTest** passed without skips/failures/errors. No reviewer/host/native rerun635. Inherited632 **two named native terminalcase0** used full git archive72614eda through productionContentSync **ONCE**,1112kanji/5068words/121N1,zeroProblems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged combined runtime.

Sole raw/selected on **キョウ** retained; rawkun[]/explicitquizkun[] create no kunquestions. Only **きょう** scheduled Good/done. 凶作 is an agriculturalnoun/verypooryield, not the harvestverb, necessarilyzeroyield/famine or badwork; 作 contributes compound-specific crop/yield. Actual N1 and All production choices **ill fortune; evil** versus **凡 commonplace; mediocre / 凸 convex; protruding / 凹 concave; sunken**, all3curatedavailable/zero fallback; All receipt is JSON, not a separately pictured All question or universal future/custom-pool certification. Native N1 selection/meaning/reading/drawing/both complete new articles/onlychanged作navigationline/SystemBack/offline covered within the recorded scope.

All23scopedHan, especially乂/凵, readable in fourproduction Compose selections; exact systemfallbackface unknown. **96recycled Paint hashes are NOT96exported/viewedPNGs**; contact sheets downscaled. Four injectedtrace strokes/recallgiveup are **not humanhandwriting/successful recall/MLKit/phone evidence**. Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, not latestappmain. No heap/guard increase or productionapp change.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable publicZIPs preserve **all8426runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus perfile/media/safepath guards; contributor evidence excluded.

Published **116/1228additions;1112remain**. Collection **1112kanji/5068words/121N1labels/126named-source members plus separate妖**. Six separate earlierN2source members保/案/派/第/策/結 are preserved, not issue60accepted additions; do not duplicate/relevel. This batch adds1necessarysupportarticle,119project-wide, **not an N1vocabularydeck**.

Durable evidence: `docs/n1-sources/batch-089-publication.json`, `execution-635.json`, original629textual/630host/631fixture/632native/633visual/634combined records. Every original source/lookup/process/denial/OOM/readdepth/downscale/font/pool/phone qualification retained. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock, no child lock or optional historical-session helper access. Checkpoint635 persists continue and yields before090; no nextbatch/secondrunner.
"""
    target = C / "batch-089-publication-comment.txt"
    assert not target.exists()
    target.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-635.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-089-publication-issue-receipt.json")
    remote = json.loads(output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-089-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-090-progress.json").exists()
    ledger = load(S / "batch-089-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == ["凶"]
    publication = load(S / "batch-089-publication.json")
    next_action = (
        f"Batch089 accepted/published/verified at{head}; yield before090. Next coordinator ONE bounded090 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue and preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "exactsession. Parent19008 retainsrunner.lock: no child acquire/delete/unlock. Approvedcontrolhelpers/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield "
        "actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/"
        "baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "two serialblinddifferentfamilies/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normal signing/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/original18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published116/1228;1112acceptance-remainder;1112kanji5068words121N1labels126namedmembers+separate妖; "
        "119necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.089initial4b84608b/629textual/630host/"
        "631fixture/632native/633visual/634combined/accepted6e972c1a/versionc6562f11cb371053/8426hashes; "
        "372Python/fresh634host4/inherited632native2/original633visuals/accepted+terminalCI+ZIP/ownerissueverified. "
        "No freshreview/native/host635. FullContentSyncONCE1112kanji5068words121N1/zeroProblems/epoch1/"
        "versionmatchescombined. Sole raw/selectedキョウ/きょうGood/done, rawkun[]/explicitquizkun[]. "
        "Agriculturalnoun/verypooryield notharvestverb/necessaryzeroyield/famine/badwork; compound-specific作crop/yield. "
        "Twoallmappedpairs/fourdirections/onedirectguard; N1/All productionall3curatedzeroFallback "
        "凡/凸/凹 versus illfortune;evil; AllJSONnotpictured. All23Han/fourComposefonts incl乂凵readable; "
        "exactfallbackfaceunknown/contactsheetsdownscaled;96recycledPainthashes NOT96exportedPNGs. "
        "Fourinjectedtrace/recallgiveup NOThumanhandwriting/MLKit/phone. OriginalGPT redundantserialtailreads/"
        "two truncatedresponses retained; fullfirstread not equalcomprehension; no missingassignedscope. "
        "QualifiedTESTONLYAndroid1c1b7bf4 retainsproductionf9b59a2, notlatestappmain. Alloriginal source/"
        "process/denial/OOM/readdepth/downscale/native/pool/phone limits andoptionaldispositions preserved "
        "in docs/n1-sources/batch-089-publication.json and execution-634.json. Physicalphone/generalrelease/"
        "whole-setoutstanding; projectincomplete. No090started/authoragents/concurrentheavywork/secondrunner/"
        "signingretry/guardincrease."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       nextAction=next_action)
    save(C / "batch-089-publication-checkpoint.json", publication)
    save(L / "batch-089-publication-checkpoint.json", publication)
    before = load(BEFORE)
    p = load(C / "progress.json")
    p["execution635StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 635, "checkpoint": 635, "batch": "089",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8426,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-089-published-verified-before-090",
        "publishedAdditions": 116, "remainingAdditions": 1112, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution635CoordinatorCheckpoint"] = verification
    p["batch089PublicationCheckpoint"] = publication
    p["batch089PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-089-publication-comment.txt"), "verified": True}
    p.update(checkpoint=635, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1112, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1112 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-verification-635.json", verification)
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
    elif mode == "download":
        download(sys.argv[2], sys.argv[3], sys.argv[4])
    elif mode == "comment":
        comment(sys.argv[2])
    elif mode == "finish":
        finish(sys.argv[2])
    else:
        raise ValueError(mode)
