"""Publish the accepted batch093 without acquiring the launcher's lock."""
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
L = C / "logs" / "d627db19-0f4d-4d9b-af29-cbaff0c9f89e"
D = V / "batch-093-publication-675"
HEAD = "713e047f4d81809fafbe0e1a5b0ad742d1315b2b"
MAIN = "fe9e1a37acddae69a3b131bdf2ea01f9ca8cd2f4"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "27663944c7217a19e7de2f363e1b31a5f13452b6"
VERSION = "bf4cc85592bb9727"
MEMBER = "\u5211"
BEFORE = L / "progress-before-675.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".675.tmp")
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


def context(head):
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    command = r"""
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
    ancestry = json.loads(output(["pwsh", "-NoProfile", "-NonInteractive", "-Command", command]))
    assert ancestry["owned"] and 19008 in ancestry["ids"]
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (674, "093", "continue")
    clean(A, APP)
    clean(R, head)
    return ancestry


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8436
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert not git("diff", HEAD, "--", "tools")
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                data = (R / name).read_bytes()
                if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == digest, name


def start():
    ancestry = context(HEAD)
    assert git("rev-parse", "origin/main") == MAIN
    subprocess.run(["git", "merge-base", "--is-ancestor", MAIN, HEAD], cwd=R, check=True)
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution674CoordinatorCheckpoint"]["savedCommit"] == HEAD
    state = {
        "execution": 675, "batch": "093", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME093 owner fast-forward publication, terminal CI, exact public ZIP and verified ownerissue; yield before094. No redundant reviewer/native/host.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete issue and final674 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and exact session verified; no child acquisition/delete/unlock.",
        "ancestry": ancestry, "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-675.json", state)
    p = load(C / "progress.json")
    p["execution675StartingState"] = state
    p.update(stage="batch-093-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    gate()


def gate():
    context(HEAD)
    e = load(S / "execution-674.json")
    p = load(C / "progress.json")
    assert sha(S / "execution-674.json") == p["execution674CoordinatorCheckpoint"]["evidenceSha256"]
    assert e["runtimeAccepted"] and not e["runtimePublished"]
    assert e["pythonTestsPassed"] == 372 and e["validatorErrors"] == 0
    assert e["hostTestsExecuted"] == 4 and e["hostChecksFresh"]
    for receipt in e["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"]
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"]
    review = load(V / "batch-093-reconciliation.json")
    assert review["initialModels"] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert review["actionableRemainingTeachingFindings"] == review["consequentialUnresolvedTeachingFindings"] == 0
    for row in review["processes"].values():
        assert row["exitCode"] == 0 and row["allAssignedRangesReturned"] and not row["observedToolOverlaps"]
        assert sha(V / row["report"]) == row["reportSha256"]
        assert sha(V / row["execution"].replace("-execution.json", ".jsonl")) == row["rawExecutionSha256"]
    inherited = e["inheritedAcceptance"]
    assert inherited["nativeTerminalCaseStatuses"] == [0, 0] and inherited["nativeRuntimeMatchesCurrentCombinedTree"]
    route = inherited["nativeRoute"]
    assert (route["contentVersion"], route["archiveRequests"], route["importedKanji"],
            route["importedWords"], route["problems"], route["acceptedReadingParserEpoch"]) == (
        VERSION, 1, 1116, 5070, 0, 1)
    assert route["quizOnKeys"] == ["\u3051\u3044"] and route["quizKunKeys"] == []
    visual = load(V / "batch-093-visual-reconciliation-673.json")
    assert visual["serialReviewerProcessesExited"] and visual["allToolViewsSerial"] and visual["allAssignedResourcesReturned"]
    assert visual["eachReviewerImagesDecoded"] == 32
    assert visual["actionableRemainingFindings"] == visual["consequentialUnresolvedInScopeClaims"] == 0
    for family, row in visual["processes"].items():
        assert row["exitCode"] == 0 and not row["observedToolOverlaps"] and not row["unfinishedTools"]
        assert sha(V / f"batch-093-visual-673-{family}.md") == row["reportSha256"]
    assert load(S / "batch-093-progress.json")["reviewClosed"] == [MEMBER]
    runtime()
    save(L / "prepublication-gate-675.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G", "runtimeHashesVerified": 8436,
        "combinedReceiptsVerified": len(e["receipts"]), "initialReportsAndExecutionHashesVerified": 2,
        "nativeTerminalCasesVerified": 2, "inheritedAcceptance": inherited,
        "parentLockTouched": False, "newReviewerNativeHostRuns": 0})
    print("Signed acceptance, complete review receipts and all8436 runtime hashes verified; starting scope persisted.")


def public(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-093-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8436 and archive["manifestEqual"]
    assert all(archive[k] for k in ["allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (18000, 42*1024**2, 80*1024**2, 56*1024**2)
    return ci, archive


def verify(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-093-{phase}-ci.json"
    assert not ci_path.exists()
    runs = json.loads(output(["gh", "run", "list", "--repo", "stop-cran/learning-japanese",
        "--commit", head, "--workflow", "Validate content", "--limit", "5", "--json", "databaseId,status,conclusion,headSha"]))
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
    save(L / f"archive-download-{phase}-675.json", {"commit": head, "url": url,
        "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
        head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-093-publication.json").exists()
    D.mkdir()
    p, before = load(C / "progress.json"), load(BEFORE)
    e = load(S / "execution-674.json")
    ledger = load(S / "batch-093-progress.json")
    counts = dict(e["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=120, remainingAdditions=1108,
        batchNewNecessarySupportWords=0, projectNewNecessarySupportWords=121,
        batchChangedReusedArticles=2, allMappedReciprocalPairs=2, mappedDirectedLinks=4,
        activatedBaselinePairs=1, separateExceptionPreserved="\u5996",
        separateEarlierLevelSourceMembers=e["sourceAudit"]["separateEarlierLevelSourceMembers"],
        earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (1116,5070,125,130)
    limits = {"combined": e["limits"], "inherited": e["inheritedAcceptance"]["originalLimits"],
        "clarification": "Historical pending flags preserved, not erased: combined674 and accepted/terminal675 discharge only their recorded scope. All source/read/native/font/Paintprobe/injectedtrace/MLKit/phone limitations remain."}
    publication = {
        "schemaVersion": 1, "execution": 675, "batch": "093", "membership": [MEMBER],
        "status": "published-verified-bounded-owner-testing", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": ledger["baseCommit"], "authoredSnapshot": TEACHING,
        "initialReviewedTeachingSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "combinedContentHead": e["combinedContentHead"], "latestMainIntegrated": MAIN,
        "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"] for n in range(667,675)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-093-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-093-visual-reconciliation-673.json",
        "nativeRecord": "execution-672.json", "combinedAcceptanceRecord": "execution-674.json",
        "validation": e["sourceAudit"], "pythonTestsPassed": 372, "hostTestsReverified": 4,
        "nativeTerminalCasesReverified": 2, "newReviewNativeHostRuns": 0, "ci": ci,
        "immutablePublicArchive": archive, "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP, "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits, "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before094."}
    save(S / "batch-093-publication.json", publication)
    ledger["prePublicationCheckpoint675"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=120,
        remainingAdditions=1108, publishedCommit=HEAD, runtimePublished=True, publicationRecord="batch-093-publication.json",
        pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
        nextAction=publication["nextAction"], publicationClarification=limits["clarification"])
    save(S / "batch-093-progress.json", ledger)
    receipts = []
    for name, tool in [("validate","tools\\validate.py"),("manifest","tools\\build_manifest.py"),("budget","tools\\check_content_budget.py")]:
        path = D / f"{name}-675.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable,"-X","utf8","-B",tool],cwd=R,stdout=stream,stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path":path.relative_to(R).as_posix(),"sha256":sha(path),"exitCode":0})
    save(S / "execution-675.json", {
        "schemaVersion":1,"execution":675,"batch":"093","status":publication["status"],
        "startingState":p["execution675StartingState"],"publicationRecord":"batch-093-publication.json",
        "acceptedCommit":HEAD,"counts":counts,"ci":ci,"immutablePublicArchive":archive,
        "inheritedAcceptanceRecord":"execution-674.json","runtimeBytesUnchanged":True,"runtimePublished":True,
        "parentLockTouched":False,"optionalHistoricalSessionHelpersAccessed":False,"actualNewPermissionDenials":[],
        "newReviewNativeHostRuns":0,"limits":limits,"terminalLocalValidation":receipts,
        "physicalPhoneAcceptance":"outstanding","generalReleaseAcceptance":"outstanding",
        "wholeProjectComplete":False,"nextBatchStarted":False})
    for path in [L/"prepublication-gate-675.json",L/"starting-state-675.json",
        L/"archive-download-accepted-675.json",C/"artifacts/batch-093-accepted-ci.json",
        C/"artifacts"/f"content-{HEAD[:7]}-acceptance.json",C/"verify-batch-002-publication.py",
        C/"publish-675.ps1",Path(__file__)]:
        shutil.copyfile(path,D/path.name)
    runtime()
    p.update(stage="batch-093-accepted-published-awaiting-terminal-evidence",nextAction=publication["nextAction"])
    p["execution675AcceptedPublication"]=copy.deepcopy(publication)
    save(C/"progress.json",p)
    print("Accepted delivery verified; publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal",head)
    publication=load(S/"batch-093-publication.json")
    body=f"""Batch **093 ({MEMBER})** is published and verified for bounded owner testing. Existing N3 **刑事 (けいじ), police detective** reused; no new support word. Two all-mapped reciprocal pairs/four directions, only ONE newly activated baseline pair (刑/刑事, not 事/刑事). Original identity/reading/title/N3/inbound探偵 guard retained. Four DIRECT police-label exclusions added; 事 receives reciprocal navigation only.

Authored/reviewed teaching `{TEACHING}` unchanged. Two serial blind textual669 reviews, actual **Claude Opus5.5 / GPT6.1Sol**, each received the same222131byte/5392line packet,180complete dictionary families/eight rawcharacters/15completearticles. Exact full packet returned in each initial view; redundant tail reads, GPT truncation/recovery, unequal manual tally depth and original GPT link-accounting correction preserved. No equal-comprehension or independent upstream retrieval claim. Complete original reports/optional dispositions retained. Original-session serial dependent rendered673 confirmations are NOT new blind review credit: each34serialviews/32decodedoriginalPNGs,25distinctsourcehashes, exit0/nooverlap.

Combined674 head `{publication['combinedContentHead']}`, freshmain `{MAIN}` already ancestral, no substantive merge. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped normal fast-forwards; global account unchanged. Combined674 **372Python tests**, validator0errors, vocabulary consistency(pilot2122/2431, NOTfullcoverage), manifest/budget/frozen sources/full baseline/exact membership/allrawreadings/TWOallmappedpairs-FOURdirections-ONEactivatedbaselinepair/fourdirectguards/pinnedSIXstrokes/46Han fontprovenance/all8436runtimehashes passed. Fresh674 **3RealContentTest+1RareHanTest** passed without skips/failures/errors. No reviewer/host/native rerun675.

Full raw **ケイ/emptykun**, explicit[ケイ]/[] retained in full/Lite. Only on **けい** scheduled, linked existing article, persistedGood/1of1Done/noKun. Whole-wordでか NOT constituentkun; publicギョウ outsidefreeze. Criminal punishment versus pictured乃/凹/凸: all3curatedavailable/zero fallback in N1/All production pools; broadercustompools/文/oldclients NOT universally certified. Modern-shape mnemonic not historical origin.

Inherited672 fullarchive324b0bd9 through production **ContentSync ONCE**:1116kanji/5070words/125N1,zeroProblems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged runtime; **TWO terminalcase0/no skips**. N1 selection/meaning/onlyonけい/six injected reference strokes/recallgiveup/allthree complete article projections/four reciprocal transitions/SystemBack/offline covered within recorded scope.

All46scopedHan inFIVEactualComposepanels/FOURproductionfontselections readable including fallback亅/刂/彡. Each reviewer viewed32of63originalPNGs;31notseparatelyviewed, tool resizes/exactduplicates and complementary horizontallyscrolled table/fulltext/native-scrollassertion dependence retained. 184individual+12wholewordPaint probes are NOT196viewedPNGs or identifiedfallbackface. Injectedtrace/recallgiveup is **NOT humanhandwriting/successfulMLKit/physical-phone evidence**; actualUI says modelunavailable/shape-onlygrading. Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, NOTlatestappmain. API35emulator is not phone acceptance.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable publicZIPs preserve **all8436runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus perfile/media/safepath guards; contributor evidence excluded.

Published **120/1228additions;1108remain**. Collection **1116kanji/5070words/125N1labels/130named-source members plus separate妖**. Six separately placed earlierN2source members保/案/派/第/策/結 preserved, not issue60accepted additions; do not duplicate/relevel. Necessarysupportarticles remain121project-wide, **NOT an N1vocabularydeck**.

Durable evidence: `docs/n1-sources/batch-093-publication.json`, `execution-675.json`, original669textual/672native/673rendered/674combined records. All original source/lookup/readdepth/font/Paintprobe/MLKit/phone limitations retained, not erased by historical pending flags. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock, no child lock or optional historical-session helper access. Checkpoint675 persists continue and yields before094; no nextbatch/secondrunner.
"""
    target=C/"batch-093-publication-comment.txt"
    assert not target.exists()
    target.write_text(body,encoding="utf-8")
    save(L/"terminal-publication-675.json",{"head":head,"ci":ci,"archive":archive,"issueBodySha256":sha(target)})


def finish(head):
    ci,archive=public("terminal",head)
    receipt=load(C/"batch-093-publication-issue-receipt.json")
    remote=json.loads(output(["gh","api",f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body=(C/"batch-093-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"]==remote["user"]["login"]=="stop-cran"
    assert receipt["body"]==remote["body"]==body
    assert output(["gh","api","user","--jq",".login"])=="romanko-ms"
    assert not (S/"batch-094-progress.json").exists()
    ledger=load(S/"batch-093-progress.json")
    assert ledger["membership"]==ledger["reviewClosed"]==ledger["published"]==[MEMBER]
    publication=load(S/"batch-093-publication.json")
    next_action=(
        f"Batch093 accepted/published/verified at {head}; yield before094. Next coordinator ONE bounded094 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent19008 retainsrunner.lock: no childacquire/delete/unlock. Approvedcontrol/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield actual"
        "newdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/baseline/"
        "fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/two serialblind"
        "differentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published120/1228;1108acceptance-remainder;1116kanji5070words125N1labels130namedmembers+separate妖; "
        "121necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.093teaching27663944/textual669/native672/"
        "rendered673/combined674/accepted713e047f/versionbf4cc85592bb9727/8436runtimehashes; "
        "372Python/fresh674host4/inherited672native2/accepted+terminalCI+ZIP/ownerissueverified. "
        "No freshreview/native/host675. OriginalClaude/GPT reports/optionalpolish/sourceandreadlimits retained. "
        "FullContentSyncONCE1116kanji5070words125N1/zeroProblems/epoch1/versionmatchescombined. "
        "Fullrawケイ/emptykun/explicit[ケイ]/[]retained;onlyonけいGood+Done,noKun;でかwholewordNOTkun/publicギョウoutsidefreeze. "
        "TWOallmappedpairs/FOURdirections/ONEactivatedbaseline刑-刑事pairNOT事-刑事;originalGPTaccountingcorrection "
        "retained.刑事N3identity/reading/title/level/inbound探偵guard preserved;fourDIRECTpoliceguards/navigationonly事. "
        "All46Han/FIVEComposepanels/FOURproductionfonts inclfallback亅刂彡readable;32of63PNGsviewed/"
        "31notseparatelyviewed/25distinctsourcehashes/toolresizes/exactduplicates/fulltext-native-scroll dependence. "
        "184individual+12wholewordPaintprobesNOT196PNGs/fallbackfaceunknown/injectedtraceNOThumanhandwriting/"
        "no successfulMLKit. QualifiedTESTONLYAndroid1c1b7bf4 retainsproductionf9b59a2, NOTlatestappmain. "
        "All original source/read/native/font/pool/phone qualifications remain in publication675/execution674. "
        "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No094started/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head,remoteMainVerified=head,terminalCi=ci,
        terminalImmutablePublicArchive=archive,issueUpdate=receipt["html_url"],nextAction=next_action)
    save(C/"batch-093-publication-checkpoint.json",publication)
    save(L/"batch-093-publication-checkpoint.json",publication)
    before,p=load(BEFORE),load(C/"progress.json")
    p["execution675StartingState"]["status"]="bounded-publication-checkpoint-complete"
    verification={
        "schemaVersion":1,"execution":675,"checkpoint":675,"batch":"093","savedCommit":head,"signature":"G",
        "remoteMainVerified":head,"acceptedCommit":HEAD,"acceptedCi":publication["ci"]["databaseId"],
        "terminalCi":ci["databaseId"],"bothImmutablePublicArchivesVerified":True,"runtimeHashesPerArchive":8436,
        "reviewedRuntimeBytesUnchanged":True,"dedicatedWorktreesClean":True,
        "allOriginalHistoricalRootValuesPreservedExactly":True,"originalRootKeysCompared":len(before),
        "ownerIssueAuthorAndBodyVerified":True,"issueUpdate":receipt["html_url"],"globalIdentityUnchanged":True,
        "parentLockTouched":False,"optionalHistoricalSessionHelpersAccessed":False,"actualNewPermissionDenials":[],
        "status":"continue","stage":"batch-093-published-verified-before-094","publishedAdditions":120,
        "remainingAdditions":1108,"lastPublishedCommit":head,"nextAction":next_action,"blocker":None,
        "physicalPhoneAcceptance":"outstanding","generalReleaseAcceptance":"outstanding",
        "wholeProjectComplete":False,"nextBatchStarted":False}
    p["execution675CoordinatorCheckpoint"]=verification
    p["batch093PublicationCheckpoint"]=publication
    p["batch093PublicationIssueReceipt"]={"id":receipt["id"],"url":receipt["html_url"],"author":"stop-cran",
        "bodySha256":sha(C/"batch-093-publication-comment.txt"),"verified":True}
    p.update(checkpoint=675,status="continue",stage=verification["stage"],lastPublishedCommit=head,
        remainingAdditions=1108,blocker=None,nextAction=next_action)
    p["unmetAcceptanceGates"]=copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0]="Remaining1108 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed={"checkpoint","status","stage","lastPublishedCommit","remainingAdditions","blocker","nextAction","unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k]==v for k,v in before.items() if k not in allowed)
    save(L/"coordinator-checkpoint-675.json",verification)
    save(C/"progress.json",p)
    assert load(C/"progress.json")==p
    print(json.dumps({k:v for k,v in verification.items() if k!="nextAction"},indent=2))


if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="start": start()
    elif mode=="gate": gate()
    elif mode=="context": context(sys.argv[2])
    elif mode=="verify": verify(sys.argv[2],sys.argv[3])
    elif mode=="records": records()
    elif mode=="comment": comment(sys.argv[2])
    elif mode=="finish": finish(sys.argv[2])
    else: raise ValueError(mode)
