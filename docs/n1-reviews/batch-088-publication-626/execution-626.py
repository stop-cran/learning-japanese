"""Publish the already accepted batch088; never acquire the parent runner lock."""
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
L = C / "logs" / "0f42e870-4004-452c-989d-df67ea9dabb1"
D = V / "batch-088-publication-626"
HEAD = "77a1a79b8c1baf9a1145929aeb49cce1d27e4f41"
MAIN = "8a36f8cd81c0e35c330079881cac1a1f3a771e26"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "42077c31b4462081eb6b2c171a907c7cae47192d"
VERSION = "afff40af0e155dbe"
BEFORE = L / "progress-before-626.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".626.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (625, "088", "continue")
    return ids


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8423
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")


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
    assert embedded["checkpoint"] == 625
    state = {
        "execution": 626, "batch": "088", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME088 normal owner fast-forward publication, exact CI/public ZIP/owner issue verification; yield before089. No new reviewer/native/host absent change.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed; operative contract, entire approved issue and final625 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact current session verified; no child acquisition/delete/unlock.",
        "ancestryPids": ids,
        "artifactPathPreflight": "Approved control helpers, committed source/review packets and frozen workspace inputs only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-626.json", state)
    p = load(C / "progress.json")
    p["execution626StartingState"] = state
    p.update(stage="batch-088-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    gate()


def gate():
    context()
    clean(R, HEAD)
    p = load(C / "progress.json")
    evidence = load(S / "execution-625.json")
    assert sha(S / "execution-625.json") == p["execution625CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"], path
    for report in evidence["inheritedAcceptance"]["initialReviewReports"]:
        assert report["exitCode"] == 0 and report["allAssignedRangesReturned"]
        assert sha(V / report["report"]) == report["reportSha256"]
        execution = load(V / report["execution"])
        assert execution["rawExecutionSha256"] == report["rawExecutionSha256"]
        assert execution["actualModels"] == report["actualModels"]
        assert sha(V / report["execution"].replace("-execution.json", ".jsonl")) == report["rawExecutionSha256"]
    assert evidence["inheritedAcceptance"]["nativeTerminalCaseStatuses"] == [0, 0]
    review = load(V / "batch-088-reconciliation.json")
    assert review["actionableRemainingTeachingFindings"] == 0
    assert review["consequentialUnresolvedTeachingFindings"] == 0
    visual = load(V / "batch-088-visual-reconciliation-624.json")
    assert visual["status"] == "dependent-visual-review-closed-awaiting-combined-acceptance"
    assert not visual["findings"] and visual["serialReviewerProcessesExited"]
    assert load(S / "batch-088-progress.json")["reviewClosed"] == ["凱"]
    runtime()
    save(L / "prepublication-gate-626.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G",
        "runtimeHashesVerified": 8423, "combinedReceiptsVerified": len(evidence["receipts"]),
        "initialReportsAndExecutionHashesVerified": 2, "nativeTerminalCasesVerified": 2,
        "inheritedAcceptance": evidence["inheritedAcceptance"],
        "parentLockTouched": False, "newReviewerNativeHostRuns": 0,
    })
    print("Starting scope persisted; signed acceptance, source/review receipts and all8423 runtime hashes verified.")


def public(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-088-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8423 and archive["manifestEqual"]
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
    ci_path = C / "artifacts" / f"batch-088-{phase}-ci.json"
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
    path = C / "artifacts" / f"content-{head[:7]}.zip"
    assert not path.exists(), path
    subprocess.run(["curl.exe", "--fail", "--location", "--silent", "--show-error",
                    f"https://api.github.com/repos/stop-cran/learning-japanese/zipball/{head}",
                    "--output", str(path)], check=True)
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
                    head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-088-publication.json").exists()
    D.mkdir()
    p = load(C / "progress.json")
    before = load(BEFORE)
    evidence = load(S / "execution-625.json")
    ledger_path = S / "batch-088-progress.json"
    ledger = load(ledger_path)
    previous = load(S / "batch-087-publication.json")
    counts = dict(evidence["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=115, remainingAdditions=1113,
                  batchNewNecessarySupportWords=1,
                  projectNewNecessarySupportWords=previous["counts"]["projectNewNecessarySupportWords"] + 1,
                  batchChangedReusedArticles=0, allMappedReciprocalPairs=1, mappedDirectedLinks=2,
                  activatedBaselinePairs=0, separateExceptionPreserved="妖",
                  separateEarlierLevelSourceMembers=evidence["sourceAudit"]["separateEarlierLevelSourceMembers"],
                  earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (
        1111, 5067, 120, 125)
    limits = {
        "combined": evidence["limits"],
        "sourceText": evidence["inheritedAcceptance"]["inheritedSourceTextLimits"],
        "visual": evidence["inheritedAcceptance"]["inheritedVisualLimits"],
        "visualDispositions": evidence["inheritedAcceptance"]["visualDispositions"],
        "clarification": "Historical pending gates remain historical, not erased: combined625 and accepted/terminal626 receipts discharge only their recorded scope. Original source/process/denial/OOM/read-depth/downscale/font/pool/MLKit/phone limitations and optional dispositions remain.",
    }
    publication = {
        "schemaVersion": 1, "execution": 626, "batch": "088", "membership": ["凱"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": TEACHING, "initialReviewedTeachingSnapshot": TEACHING,
        "reviewedTeachingSnapshot": TEACHING, "combinedContentHead": evidence["combinedContentHead"],
        "latestMainIntegrated": MAIN, "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"]
                      for n in range(618, 626)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-088-reconciliation.json",
        "visualRecord": "../n1-reviews/batch-088-visual-reconciliation-624.json",
        "combinedAcceptanceRecord": "execution-625.json", "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits, "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before089.",
    }
    save(S / "batch-088-publication.json", publication)
    ledger["prePublicationCheckpoint626"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["凱"], publishedAdditions=115,
                  remainingAdditions=1113, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-088-publication.json",
                  pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
                  nextAction=publication["nextAction"], publicationClarification=limits["clarification"])
    save(ledger_path, ledger)
    for name in ["batch-088-reconciliation.json", "batch-088-visual-reconciliation-624.json"]:
        path = V / name
        review = load(path)
        review["prePublicationState626"] = {k: copy.deepcopy(review[k]) for k in
                                           ("status", "runtimeAccepted", "runtimePublished", "limits") if k in review}
        review.update(status=publication["status"], runtimePublished=True,
                      publicationRecord="../n1-sources/batch-088-publication.json",
                      publicationClarification=limits["clarification"])
        save(path, review)
    receipts = []
    for name, args in [("validate", ["tools\\validate.py"]),
                       ("manifest", ["tools\\build_manifest.py"]),
                       ("budget", ["tools\\check_content_budget.py"])]:
        path = D / f"{name}-626.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args], cwd=R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    execution = {
        "schemaVersion": 1, "execution": 626, "batch": "088", "status": publication["status"],
        "startingState": p["execution626StartingState"], "publicationRecord": "batch-088-publication.json",
        "acceptedCommit": HEAD, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-625.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "newReviewNativeHostRuns": 0, "limits": limits,
        "diagnostics": [
            "Initial prepublication check stopped before any push: helper mistakenly compared rawExecutionSha256 with the structured execution.json bytes. Verified it against the actual committed raw .jsonl and checked the structured model/hash fields separately; no evidence or acceptance gate changed."
        ],
        "terminalLocalValidation": receipts, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    save(S / "execution-626.json", execution)
    for path in [L / "prepublication-gate-626.json", L / "starting-state-626.json",
                 C / "artifacts" / "batch-088-accepted-ci.json",
                 C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json",
                 C / "verify-batch-002-publication.py", C / "publish-626.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-088-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution626AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Public accepted delivery verified; durable publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-088-publication.json")
    body = f"""Batch **088 (凱)** is published and verified for bounded owner testing, with necessary support **凱旋 (がいせん), triumphant return**. One mapped reciprocal pair/two directions, four direct word guards, no changed reused articles or inferred vocabulary level.

Authored/independently reviewed teaching `{TEACHING}`; textual closure `{publication['snapshots']['620']}`; native evidence `{publication['snapshots']['623']}`; original-session visual closure `{publication['snapshots']['624']}`. Main `{MAIN}` was already an ancestor; normal nonrewriting merge Already up to date, no teaching change. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global account unchanged.

Original blind **Claude Opus5.5 / GPT6.1Sol** initial reviews and serial dependent original-session visuals retained, not new blind credit. Identical141101byte/2665line packet included25 completeJMdictfamilies,6 rawcharacters and14 completearticlebodies including2new; assigned ranges returned, not proof of equivalent comprehension. Each original reviewer decoded11PNG images: eight downscaled contact sheets cover46captures and three original font panels. Claude's original first two TEXT views overlapped; complete deviation retained and corrected through two strictly serial same-session text rereads. All imageviews serial; GPT13serialcalls after actual Claudeexit. No actionable scoped teaching defect remains; original optional wording/wrapping/table observations remain optional.

Combined-tree **372Python tests**, validator0errors, vocabulary consistency (pilot2122/2431, not full coverage), fresh manifest, exact source/baseline/membership, allfour readings/one pair/two directions/four guards/pinned12strokes/font provenance passed. Fresh625 **3RealContentTest+1RareHanTest** passed without skips/failures/errors. No reviewer/host/native rerun626. Inherited623 **two named native terminalcase0** used full git archivee445d826 through productionContentSync **ONCE**,1111kanji/5067words/120N1,zeroProblems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged combined runtime.

All rawon **ガイ / カイ** and undottedkun **かちどき / やわらぐ**, including order, retained. Only **がい** scheduled Good/done; explicitkun[] and unselectedカイ create no questions. Source-only characterdictionary meanings are not fabricated ordinary modern wordspellings. Actual N1 and All production choices **victory song; triumph** versus **凡 commonplace; mediocre / 凸 convex; protruding / 凹 concave; sunken**, all3curatedavailable/zero fallback; All receipt is JSON, not a separately pictured All question or universal future/custom-pool certification. Native N1 selection/meaning/reading/drawing/both articles/SystemBack/offline covered within the recorded scope.

All27scopedHan, especially几/豈/鬨, readable in fourproduction Compose selections; exact systemfallbackface unknown. **108individual+4wholeword recycled Paint hashes are NOT112exported/viewedPNGs**. Twelve injectedtrace strokes/recallgiveup are **not humanhandwriting/successful recall/MLKit/phone evidence**. Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, not latestappmain. No heap/guard increase or productionapp change.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable publicZIPs preserve **all8423runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus perfile/media/safepath guards; contributor evidence excluded.

Published **115/1228additions;1113remain**. Collection **1111kanji/5067words/120N1labels/125named-source members plus separate妖**. Six separate earlierN2source members保/案/派/第/策/結 are preserved, not issue60accepted additions; do not duplicate/relevel. This batch adds1necessarysupportarticle,118project-wide, **not an N1vocabularydeck**.

Durable evidence: `docs/n1-sources/batch-088-publication.json`, `execution-626.json`, original620textual/621host/622fixture/623native/624visual/625combined records. Every original source/lookup/process/denial/OOM/readdepth/downscale/font/pool/phone qualification retained. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock, no child lock or optional historical-session helper access. Checkpoint626 persists continue and yields before089; no nextbatch/secondrunner.
"""
    target = C / "batch-088-publication-comment.txt"
    assert not target.exists()
    target.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-626.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-088-publication-issue-receipt.json")
    remote = json.loads(output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-088-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-089-progress.json").exists()
    ledger = load(S / "batch-088-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == ["凱"]
    publication = load(S / "batch-088-publication.json")
    next_action = (
        f"Batch088 accepted/published/verified at{head}; yield before089. Next coordinator ONE bounded089 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue and preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "exactsession. Parent19008 retainsrunner.lock: no child acquire/delete/unlock. Approvedcontrolhelpers/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield "
        "actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/"
        "baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "two serialblinddifferentfamilies/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normal signing/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/original18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published115/1228;1113acceptance-remainder;1111kanji5067words120N1labels125namedmembers+separate妖; "
        "118necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.088initial42077c31/620textual/621host/"
        "622fixture/623native/624visual/625combined/accepted77a1a79b/versionafff40af0e155dbe/8423hashes; "
        "372Python/fresh625host4/inherited623native2/original624visuals/accepted+terminalCI+ZIP/ownerissueverified. "
        "No freshreview/native/host626. FullContentSyncONCE1111kanji5067words120N1/zeroProblems/epoch1/"
        "versionmatchescombined. Rawガイ/カイ+かちどき/やわらぐorder preserved, onlyがいscheduledGood/done, "
        "explicitkun[]; sourceonly glosses NOT ordinarymodernspellings. Onepair/twodirections/fourdirectguards; "
        "N1/All productionall3curatedzeroFallback 凡/凸/凹 versus victorysong;triumph; AllJSONnotpictured. "
        "All27Han/fourComposefonts incl几豈鬨readable; exactfallbackfaceunknown and contactsheetsdownscaled. "
        "Paint108+4recycledhashes NOT112exportedPNGs. Twelveinjectedtrace/recallgiveup NOThumanhandwriting/"
        "MLKit/phone. Claudeinitial2TEXTviewoverlap PRESERVED withsamesessionserial2textcorrection; "
        "all11PNGserial/GPT13serialcalls afterClaudeexit; notnewblindcredit. QualifiedTESTONLYAndroid1c1b7bf4 "
        "retainsproductionf9b59a2, notlatestappmain. Alloriginal source/process/denial/OOM/readdepth/downscale/"
        "native/pool/phone limits andoptionaldispositions preserved in docs/n1-sources/batch-088-publication.json "
        "and execution-625.json. Physicalphone/generalrelease/whole-setoutstanding; projectincomplete. "
        "No089started/authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       nextAction=next_action)
    save(C / "batch-088-publication-checkpoint.json", publication)
    save(L / "batch-088-publication-checkpoint.json", publication)
    before = load(BEFORE)
    p = load(C / "progress.json")
    p["execution626StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 626, "checkpoint": 626, "batch": "088",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8423,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-088-published-verified-before-089",
        "publishedAdditions": 115, "remainingAdditions": 1113, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution626CoordinatorCheckpoint"] = verification
    p["batch088PublicationCheckpoint"] = publication
    p["batch088PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-088-publication-comment.txt"), "verified": True}
    p.update(checkpoint=626, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1113, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1113 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-verification-626.json", verification)
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
