"""Publish accepted batch091 without acquiring the parent launcher's lock."""
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
L = C / "logs" / "12849885-f3b9-470f-b0bc-cc287a1905b5"
D = V / "batch-091-publication-657"
HEAD = "38e30de845e0a9c0d49be599ba8c14ef323e7353"
MAIN = "7100a3873282b54515b9ef130766e77cf151a47b"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "fe3ec10b34e5b26fd286d7a79b33b6b6a03afda6"
VERSION = "bfe65483a821fc13"
BEFORE = L / "progress-before-657.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".657.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (656, "091", "continue")
    return ancestry


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8432
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
    assert embedded["execution656CoordinatorCheckpoint"]["checkpoint"] == 656
    state = {
        "execution": 657, "batch": "091", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME091 owner fast-forward publication, terminal CI, exact public ZIP and verified ownerissue; yield before092. No redundant reviewer/native/host.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and embedded checkpoint parsed; operative contract, complete issue and final656 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact session verified; no child acquisition/delete/unlock.",
        "ancestry": ancestry,
        "artifactPathPreflight": "Approved control helpers/inputs and committed source/review evidence only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-657.json", state)
    p = load(C / "progress.json")
    p["execution657StartingState"] = state
    p.update(stage="batch-091-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    gate()


def gate():
    context()
    clean(R, HEAD)
    evidence = load(S / "execution-656.json")
    p = load(C / "progress.json")
    assert sha(S / "execution-656.json") == p["execution656CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"], path
    review = load(V / "batch-091-reconciliation.json")
    assert review["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    for report in review["processes"].values():
        assert report["exitCode"] == 0 and report["allAssignedRangesReturned"]
        assert report["observedToolOverlaps"] == 0
        assert sha(V / report["report"]) == report["reportSha256"]
        assert sha(V / report["execution"].replace("-execution.json", ".jsonl")) == report["rawExecutionSha256"]
    assert evidence["inheritedAcceptance"]["nativeTerminalCaseStatuses"] == [0]
    assert evidence["inheritedAcceptance"]["glyph650TerminalCaseStatuses"] == [0, 0]
    assert evidence["inheritedAcceptance"]["nativeRuntimeMatchesCurrentCombinedTree"]
    assert evidence["inheritedAcceptance"]["V1"] == "resolved"
    visual = load(V / "batch-091-rendered-reconciliation-655.json")
    confirmations = visual["dependentOriginalSessionConfirmations"]
    assert len(confirmations) == 2
    assert {m for r in confirmations for m in r["actualModels"]} == {"claude-opus-5.5", "gpt-6.1-sol"}
    for row in confirmations:
        assert row["exitCode"] == 0 and row["acceptedExecution"]
        assert not row["observedToolOverlaps"] and not row["unfinishedTools"]
    assert load(S / "batch-091-progress.json")["reviewClosed"] == ["刃"]
    runtime()
    save(L / "prepublication-gate-657.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G",
        "runtimeHashesVerified": 8432, "combinedReceiptsVerified": len(evidence["receipts"]),
        "initialReportsAndExecutionHashesVerified": 2, "nativeTerminalCasesVerified": 1,
        "glyph650CasesInherited": 2, "inheritedAcceptance": evidence["inheritedAcceptance"],
        "parentLockTouched": False, "newReviewerNativeHostRuns": 0,
    })
    print("Starting scope persisted; signed acceptance, source/review receipts and all8432 runtime hashes verified.")


def public(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-091-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8432 and archive["manifestEqual"]
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
    ci_path = C / "artifacts" / f"batch-091-{phase}-ci.json"
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
    save(L / f"archive-download-{phase}-657.json", {
        "commit": head, "url": url, "exitCode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
        head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-091-publication.json").exists()
    D.mkdir()
    p, before = load(C / "progress.json"), load(BEFORE)
    evidence = load(S / "execution-656.json")
    ledger_path = S / "batch-091-progress.json"
    ledger = load(ledger_path)
    previous = load(S / "batch-090-publication.json")
    counts = dict(evidence["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=118, remainingAdditions=1110,
        batchNewNecessarySupportWords=1,
        projectNewNecessarySupportWords=previous["counts"]["projectNewNecessarySupportWords"] + 1,
        batchChangedReusedArticles=0, allMappedReciprocalPairs=1, mappedDirectedLinks=2,
        activatedBaselinePairs=0, separateExceptionPreserved="妖",
        separateEarlierLevelSourceMembers=evidence["sourceAudit"]["separateEarlierLevelSourceMembers"],
        earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (1114, 5070, 123, 128)
    limits = {
        "combined": evidence["limits"],
        "inherited": evidence["inheritedAcceptance"]["originalLimits"],
        "processViolation": evidence["inheritedAcceptance"]["priorProcessViolationPreserved"],
        "clarification": "Historical pending flags preserved, not erased: combined656 and accepted/terminal657 receipts discharge only their recorded scope. All source/read/process/native/font/Paintprobe/injectedtrace/MLKit/phone limitations remain. V1 text resolved653, revised native654 and dependent rendered655 confirmed; no retroactive repair of rejected Claude651 overlap.",
    }
    publication = {
        "schemaVersion": 1, "execution": 657, "batch": "091", "membership": ["刃"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": before["execution646CoordinatorCheckpoint"]["savedCommit"],
        "initialReviewedTeachingSnapshot": load(V / "batch-091-reconciliation.json")["originalTeachingSnapshot"],
        "reviewedTeachingSnapshot": TEACHING, "combinedContentHead": evidence["combinedContentHead"],
        "latestMainIntegrated": MAIN, "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"] for n in range(645, 657)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-091-reconciliation.json",
        "mnemonicRecord": "../n1-reviews/batch-091-mnemonic-reconciliation-653.json",
        "renderedRecord": "../n1-reviews/batch-091-rendered-reconciliation-655.json",
        "nativeRecord": "execution-654.json", "combinedAcceptanceRecord": "execution-656.json",
        "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 1,
        "glyph650CasesInherited": 2, "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits, "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before092.",
    }
    save(S / "batch-091-publication.json", publication)
    ledger["prePublicationCheckpoint657"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["刃"], publishedAdditions=118,
        remainingAdditions=1110, publishedCommit=HEAD, runtimePublished=True,
        publicationRecord="batch-091-publication.json",
        pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
        nextAction=publication["nextAction"], publicationClarification=limits["clarification"])
    save(ledger_path, ledger)
    receipts = []
    for name, tool in [("validate", "tools\\validate.py"), ("manifest", "tools\\build_manifest.py"),
                       ("budget", "tools\\check_content_budget.py")]:
        path = D / f"{name}-657.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", tool], cwd=R,
                stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    save(S / "execution-657.json", {
        "schemaVersion": 1, "execution": 657, "batch": "091", "status": publication["status"],
        "startingState": p["execution657StartingState"], "publicationRecord": "batch-091-publication.json",
        "acceptedCommit": HEAD, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-656.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "newReviewNativeHostRuns": 0, "limits": limits,
        "terminalLocalValidation": receipts, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False})
    for path in [L / "prepublication-gate-657.json", L / "starting-state-657.json",
        L / "archive-download-accepted-657.json", C / "artifacts" / "batch-091-accepted-ci.json",
        C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json", C / "verify-batch-002-publication.py",
        C / "publish-657.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-091-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution657AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Accepted delivery verified; durable publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-091-publication.json")
    body = f"""Batch **091 (刃)** is published and verified for bounded owner testing, with necessary support **刃 (は), blade/cutting edge**. One all-mapped reciprocal pair/two directions, no changed reused articles or activated baseline pairs; all five direct word guards retained, including the reviewed English-label precaution with 先端. No inferred vocabulary level.

Initial authored/two-family blind teaching `{publication['initialReviewedTeachingSnapshot']}`; textual647 guard correction, mnemonic653 confirmation, revised native654 and serial original-session rendered655 evidence retained. Current reviewed runtime `{TEACHING}` / version `{VERSION}`; combined656 head `{publication['combinedContentHead']}`. Main `{MAIN}` was already ancestral; no new substantive merge. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global account unchanged.

Original blind **Claude Opus5.5 / GPT6.1Sol** reviews covered both complete new articles,78full dictionary families and5rawcharacters. Each initial reviewer received the same full packet via one serial view; access is not equal comprehension. Claude's minor English-label guard finding resolved; GPT's initial non-discovery remains historical. V1 mnemonic text resolved653 and NEW revised-version native paragraph independently confirmed in the original sessions655 with serial tools. These are dependent confirmations, not new blind review credit. Rejected **Claude651 internal tool overlap** is preserved, not retroactively repaired.

Combined656 **372Python tests**, validator0errors, vocabulary consistency (pilot2122/2431, not full coverage), fresh manifest, frozen sources/full baseline/exact membership/all5readings/onepair/twodirections/fivedirectguards/pinned3strokes/current20Han subset of inherited21Han fontprovenance passed. Fresh656 **3RealContentTest+1RareHanTest** passed without skips/failures/errors. No reviewer/host/native rerun657.

Full raw **ジン/ニン; は/やいば/き.る** source order retained in full/Lite projections. Only selected **は**, with its own linked article, is scheduled; on prompts explicitly empty. Recognition readings remain qualified; source-onlyき.る does not become an invented ordinary spelling. The physical cutting edge is not automatically a whole knife or the figurative forefront. Shape mnemonic explicitly nonhistorical and font-qualified.

Inherited654 fullarchive through production **ContentSync ONCE**:1114kanji/5070words/123N1,zeroProblems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged runtime; **one terminalcase0/no skips**. N1 selection/meaning/onlykunはGood+Done/3injectedreference strokes/recallgiveup/persistedDrawAgain/both complete articles/two reciprocal transitions/先端 contrast/SystemBack/offline covered within recorded scope. N1/All production choices use 乃/凹/凸, all3curatedavailable/zero fallback; not future/custom-pool certification.

GlyphTest **NOT rerun654/656/657**: inherit650 original21Han/fourComposefonts and exact recorded limits, current20Han subset. Fallbackface unknown; Paint hash probes are not separately inspected PNGs. Revised654 coordinator viewed one of47new captures; original655 reviewers each decoded the NEW paragraph PNG, not all47. Injectedtrace/giveup is **not humanhandwriting/successfulMLKit/physical-phone evidence**. Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, NOTlatestappmain; API35 emulator is not phone acceptance.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable publicZIPs preserve **all8432runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus perfile/media/safepath guards; contributor evidence excluded.

Published **118/1228additions;1110remain**. Collection **1114kanji/5070words/123N1labels/128named-source members plus separate妖**. Six separately placed earlierN2source members保/案/派/第/策/結 remain preserved, not issue60accepted additions; do not duplicate/relevel. This batch adds1necessarysupportarticle,121project-wide, **not an N1vocabularydeck**.

Durable evidence: `docs/n1-sources/batch-091-publication.json`, `execution-657.json`, original647textual/650glyph/653mnemonic/654native/655rendered/656combined records. All original source/lookup/process/readdepth/font/Paintprobe/MLKit/phone limitations remain. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock, no child lock or optional historical-session helper access. Checkpoint657 persists continue and yields before092; no nextbatch/secondrunner.
"""
    target = C / "batch-091-publication-comment.txt"
    assert not target.exists()
    target.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-657.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-091-publication-issue-receipt.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-091-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-092-progress.json").exists()
    ledger = load(S / "batch-091-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == ["刃"]
    publication = load(S / "batch-091-publication.json")
    next_action = (
        f"Batch091 accepted/published/verified at {head}; yield before092. Next coordinator ONE bounded092 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent19008 retainsrunner.lock: no childacquire/delete/unlock. Approvedcontrol/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield actual"
        "newdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/baseline/"
        "fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/two serialblind"
        "differentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published118/1228;1110acceptance-remainder;1114kanji5070words123N1labels128namedmembers+separate妖; "
        "121necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.091initial77e8735b/textual647/mnemonic653/"
        "native654/rendered655/combined656/accepted38e30de8/versionbfe65483a821fc13/8432runtimehashes; "
        "372Python/fresh656host4/inherited654native1/650glyph2/accepted+terminalCI+ZIP/ownerissueverified. "
        "No freshreview/native/host657. V1 textresolved653/currentnative654/originalsessionPNG655 serialconfirmation. "
        "GPTinitialnondiscovery and rejectedClaude651overlap preserved, not retroactivelyrepaired. FullContentSyncONCE"
        "1114kanji5070words123N1/zeroProblems/epoch1/versionmatchescombined. Fullrawジンニン/はやいばき.る "
        "retained; onlykunはGood+Done, no on/sourceonlykey; oneallmappedpair/twodirections/fivedirectguards. "
        "Current20Han subset inherited65021; GlyphTestNOT rerun654656657; actualfallbackfaceunknown/Paintprobes"
        "NOTseparatePNGs/oneparagraphPNGperreviewer655notall47newcaptures/injectedtraceNOT humanhandwriting/"
        "no successfulMLKit. QualifiedTESTONLYAndroid1c1b7bf4 retainsproductionf9b59a2, NOTlatestappmain. "
        "All original source/read/process/native/font/pool/phone qualifications remain in publication657 and "
        "execution656. Physicalphone/generalrelease/whole-setoutstanding; projectincomplete. "
        "No092started/authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
        terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextAction=next_action)
    save(C / "batch-091-publication-checkpoint.json", publication)
    save(L / "batch-091-publication-checkpoint.json", publication)
    before, p = load(BEFORE), load(C / "progress.json")
    p["execution657StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 657, "checkpoint": 657, "batch": "091",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8432,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-091-published-verified-before-092",
        "publishedAdditions": 118, "remainingAdditions": 1110, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution657CoordinatorCheckpoint"] = verification
    p["batch091PublicationCheckpoint"] = publication
    p["batch091PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-091-publication-comment.txt"), "verified": True}
    p.update(checkpoint=657, status="continue", stage=verification["stage"],
        lastPublishedCommit=head, remainingAdditions=1110, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1110 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "coordinator-checkpoint-657.json", verification)
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
