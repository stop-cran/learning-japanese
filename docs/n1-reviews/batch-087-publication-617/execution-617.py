"""Publish accepted batch087 under the live launcher's existing protection."""
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
D = V / "batch-087-publication-617"
L = C / "logs" / "28fb2b49-f5ad-4fc4-a962-4a55c06934eb"
HEAD = "3ca10c377d6f802a0f9e9d0788f37a8c22a6e1dd"
MAIN = "6eaa018dcbcabe57d9e22ddf6b07c6b8ee2dfea6"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "f6391022356073dd3e53437be30885f9a09857d9"
VERSION = "eb3a9413cccd4f57"
BEFORE = L / "progress-before-617.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".617.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (616, "087", "continue")
    return ids


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8420
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
    assert embedded["checkpoint"] == 616
    state = {
        "execution": 617, "batch": "087", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME087 accepted signed owner fast-forward publication, exact CI/public ZIP/owner issue verification; yield before088. No new reviewer/native/HOST absent change.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, entire approved issue and final616 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry and exact runner session verified; no child acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers, committed source/review packets and frozen workspace inputs only. No optional historical-session artifact accessed.",
        "ancestryPids": ids, "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-617.json", state)
    p = load(C / "progress.json")
    p["execution617StartingState"] = state
    p.update(stage="batch-087-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    evidence = load(S / "execution-616.json")
    assert sha(S / "execution-616.json") == p["execution616CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"], path
    for report in evidence["inheritedAcceptance"]["reviewReports"]:
        assert report["exitCode"] == 0
        assert sha(R / report["report"]) == report["reportSha256"]
    assert evidence["inheritedAcceptance"]["nativeTerminalCaseStatuses"] == [0, 0]
    review = load(V / "batch-087-reconciliation.json")
    assert review["actionableRemainingTeachingFindings"] == 0
    assert review["consequentialUnresolvedTeachingFindings"] == 0
    visual = load(V / "batch-087-visual-reconciliation-615.json")
    assert visual["status"] == "dependent-visual-review-closed-awaiting-combined-acceptance"
    assert not visual["findings"]
    assert load(S / "batch-087-progress.json")["reviewClosed"] == ["凪"]
    runtime()
    save(L / "prepublication-gate-617.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G",
        "runtimeHashesVerified": 8420, "combinedReceiptsVerified": len(evidence["receipts"]),
        "reviewReportsVerified": 4, "nativeTerminalCasesVerified": 2,
        "parentLockTouched": False, "newReviewerNativeHostRuns": 0,
    })
    print("Starting scope persisted; signed acceptance, review receipts and all8420 runtime hashes verified.")


def public(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-087-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8420 and archive["manifestEqual"]
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
    ci_path = C / "artifacts" / f"batch-087-{phase}-ci.json"
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
    assert not D.exists() and not (S / "batch-087-publication.json").exists()
    D.mkdir()
    p = load(C / "progress.json")
    before = load(BEFORE)
    evidence = load(S / "execution-616.json")
    ledger_path = S / "batch-087-progress.json"
    ledger = load(ledger_path)
    counts = dict(evidence["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=114, remainingAdditions=1114,
                  batchNewNecessarySupportWords=2, projectNewNecessarySupportWords=117,
                  batchChangedReusedArticles=0, allMappedReciprocalPairs=2, mappedDirectedLinks=4,
                  activatedBaselinePairs=0, separateExceptionPreserved="妖",
                  separateEarlierLevelSourceMembers=evidence["sourceAudit"]["separateEarlierLevelSourceMembers"],
                  earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (
        1110, 5066, 119, 124)
    limits = {
        "combined": evidence["limits"],
        "sourceText": evidence["inheritedAcceptance"]["inheritedSourceTextLimits"],
        "visual": evidence["inheritedAcceptance"]["inheritedVisualLimits"],
        "visualDispositions": evidence["inheritedAcceptance"]["visualDispositions"],
        "clarification": "Historical pending gates are historical; combined acceptance616, accepted CI/archive617 and terminal receipts discharge them only within their recorded scope. Every linguistic/process/denial/OOM/read-depth/downscale/font/pool/MLKit/phone limitation remains.",
    }
    publication = {
        "schemaVersion": 1, "execution": 617, "batch": "087", "membership": ["凪"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": TEACHING, "initialReviewedTeachingSnapshot": TEACHING,
        "reviewedTeachingSnapshot": TEACHING, "combinedContentHead": evidence["combinedContentHead"],
        "latestMainIntegrated": MAIN, "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"]
                      for n in range(609, 617)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-087-reconciliation.json",
        "visualRecord": "../n1-reviews/batch-087-visual-reconciliation-615.json",
        "combinedAcceptanceRecord": "execution-616.json", "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits, "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before088.",
    }
    save(S / "batch-087-publication.json", publication)
    ledger["prePublicationCheckpoint617"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["凪"], publishedAdditions=114,
                  remainingAdditions=1114, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-087-publication.json",
                  pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
                  nextAction=publication["nextAction"], publicationClarification=limits["clarification"])
    save(ledger_path, ledger)
    for name in ["batch-087-reconciliation.json", "batch-087-visual-reconciliation-615.json"]:
        path = V / name
        review = load(path)
        review["prePublicationState617"] = {k: copy.deepcopy(review[k]) for k in
                                           ("status", "runtimePublished", "limits") if k in review}
        review.update(status=publication["status"], runtimePublished=True,
                      publicationRecord="../n1-sources/batch-087-publication.json",
                      publicationClarification=limits["clarification"])
        save(path, review)
    receipts = []
    for name, args in [("validate", ["tools\\validate.py"]),
                       ("manifest", ["tools\\build_manifest.py"]),
                       ("budget", ["tools\\check_content_budget.py"])]:
        path = D / f"{name}-617.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args], cwd=R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    execution = {
        "schemaVersion": 1, "execution": 617, "batch": "087", "status": publication["status"],
        "startingState": p["execution617StartingState"], "publicationRecord": "batch-087-publication.json",
        "acceptedCommit": HEAD, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-616.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "newReviewNativeHostRuns": 0, "limits": limits,
        "terminalLocalValidation": receipts, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    save(S / "execution-617.json", execution)
    for path in [L / "prepublication-gate-617.json", L / "starting-state-617.json",
                 C / "artifacts" / "batch-087-accepted-ci.json",
                 C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json",
                 C / "verify-batch-002-publication.py", C / "publish-617.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-087-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution617AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Public accepted delivery verified; durable publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-087-publication.json")
    body = f"""Batch **087 (凪)** is published and verified for bounded owner testing, with necessary native support **凪 (なぎ), calm at sea; lull**, and **凪ぐ (なぐ), become calm (wind/sea)**. Two mapped reciprocal pairs/four directions, seven direct word guards, no changed reused articles or inferred vocabulary levels.

Authored/independently reviewed teaching `{TEACHING}`; textual closure `{publication['snapshots']['611']}`; native evidence `{publication['snapshots']['614']}`; original-session visual closure `{publication['snapshots']['615']}`. Main `{MAIN}` was already an ancestor; normal nonrewriting merge Already up to date, no teaching change. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global account unchanged.

Original blind **Claude Opus5.5 / GPT6.1Sol** initial reviews and serial dependent original-session visuals retained, not new blind credit. Identical146190byte/2830line packet included25 completeJMdictfamilies,5 rawcharacters and16 completearticlebodies including3new; assigned ranges returned, not proof of equivalent comprehension. Each original reviewer decoded12PNG images in14 serial viewcalls; ten downscaled contact sheets cover55 captures and two separately full-size Compose font panels. No actionable scoped teaching defect remains; optional screenshot/transition/practice-wording observations remain optional.

Combined-tree **372Python tests**, validator0errors, vocabulary consistency (pilot2122/2431, not full coverage), fresh manifest, exact source/baseline/membership, two readings/two pairs/four directions/seven guards/pinned six strokes/font provenance passed. Fresh616 **3RealContentTest+1RareHanTest** passed without skips/failures/errors. No reviewer/HOST/native rerun617. Inherited614 **two named native terminalcase0** used full git archive404f507d through productionContentSync **ONCE**,1110kanji/5066words/119N1,zeroProblems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged combined runtime.

Both rawkun entries/order **なぎ / な.ぐ** retained and both keys **なぎ / なぐ** scheduled Good/done; explicit on[] creates no onquestion. Modern weather凪ぐ/gu-ending conjugation remains separate from feelings和ぐ and classical forms. N1 has only凡/凹 curated available, not N4風; pictured default fallback **yuzu citrus** is unambiguous. Seed613chestnut and Allwind/style are supplied productionJSON only, not separate pictures or universal future/custom-pool certification. Native N1 selection/meaning/readings/sixstroke drawing/allthree articles/SystemBack/offline covered within the recorded scope.

All21scopedHan, especially几 U+51E0, readable in fourproduction Compose selections; exact systemfallbackface unknown. **84+8 recycled Paint hashes are NOT92exported/viewedPNGs**. Six injectedtrace strokes/recallgiveup are **not humanhandwriting/successful recall/MLKit/phone evidence**. Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, not latestappmain. No heap/guard increase or productionapp change.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable publicZIPs preserve **all8420runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus perfile/media/safepath guards; contributor evidence excluded.

Published **114/1228additions;1114remain**. Collection **1110kanji/5066words/119N1labels/124named-source members plus separate妖**. Six separate earlierN2source members保/案/派/第/策/結 are preserved, not issue60accepted additions; do not duplicate/relevel. This batch adds2necessarysupportarticles,117project-wide, **not an N1vocabularydeck**.

Durable evidence: `docs/n1-sources/batch-087-publication.json`, `execution-617.json`, original611textual/612HOST/613fixture/614native/615visual/616combined records. Every original source/lookup/process/denial/OOM/readdepth/downscale/font/pool/phone qualification retained. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock, no child lock or optional historical-session helper access. Checkpoint617 persists continue and yields before088; no nextbatch/secondrunner.
"""
    target = C / "batch-087-publication-comment.txt"
    assert not target.exists()
    target.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-617.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-087-publication-issue-receipt.json")
    remote = json.loads(output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-087-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-088-progress.json").exists()
    ledger = load(S / "batch-087-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == ["凪"]
    publication = load(S / "batch-087-publication.json")
    next_action = (
        f"Batch087 accepted/published/verified at{head}; yield before088. Next coordinator ONE bounded088 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue and preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "exactsession. Parent19008 retainsrunner.lock: no child acquire/delete/unlock. Approvedcontrolhelpers/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield "
        "actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/"
        "baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "two serialblinddifferentfamilies/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normal signing/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/original18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published114/1228;1114acceptance-remainder;1110kanji5066words119N1labels124namedmembers+separate妖; "
        "117necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.087initialf6391022/611textual/612HOST/"
        "613fixture/614native/615visual/616combined/accepted3ca10c37/versioneb3a9413cccd4f57/8420hashes; "
        "372Python/fresh616HOST4/inherited614native2/original615visuals/accepted+terminalCI+ZIP/ownerissueverified. "
        "No freshreview/native/HOST617. FullContentSyncONCE1110kanji5066words119N1/zeroProblems/epoch1/"
        "versionmatchescombined. Bothrawkunなぎ/な.ぐorder retained and keysなぎ/なぐ scheduledGood/done, "
        "expliciton[]. Modernweather凪ぐ versus feelings和ぐ/classicalforms separate. Twopairs/fourdirections/"
        "sevendirectguards; all21Han/fourComposefonts incl几readable; exactfallbackfaceunknown and contact"
        "sheetsdownscaled. DefaultN1yuzupictured; seeded613chestnut/AllwindJSONonly, not universalpoolcertification. "
        "Paint84+8recycledhashes NOT92exportedPNGs. Sixinjectedtrace/recallgiveup NOT humanhandwriting/MLKit/"
        "phone. QualifiedTESTONLYAndroid1c1b7bf4 retainsproductionf9b59a2, notlatestappmain. Alloriginal source/"
        "process/denial/OOM/readdepth/downscale/native/pool/phone limits andoptionaldispositions preserved in "
        "docs/n1-sources/batch-087-publication.json and execution-616.json. Physicalphone/generalrelease/"
        "whole-setoutstanding; projectincomplete. No088started/authoragents/concurrentheavywork/secondrunner/"
        "signingretry/guardincrease."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       nextAction=next_action)
    save(C / "batch-087-publication-checkpoint.json", publication)
    save(L / "batch-087-publication-checkpoint.json", publication)
    before = load(BEFORE)
    p = load(C / "progress.json")
    p["execution617StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 617, "checkpoint": 617, "batch": "087",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8420,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-087-published-verified-before-088",
        "publishedAdditions": 114, "remainingAdditions": 1114, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution617CoordinatorCheckpoint"] = verification
    p["batch087PublicationCheckpoint"] = publication
    p["batch087PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-087-publication-comment.txt"), "verified": True}
    p.update(checkpoint=617, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1114, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1114 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-verification-617.json", verification)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({k: v for k, v in verification.items() if k != "nextAction"}, indent=2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "start":
        start()
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
