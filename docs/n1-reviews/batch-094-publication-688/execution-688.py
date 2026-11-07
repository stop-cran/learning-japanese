"""Publish accepted batch094 with exact public acceptance under the parent lock."""
import base64
import copy
import gzip
import hashlib
import importlib.util
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
L = C / "logs" / "c93f70f4-3e4b-4cac-b23d-233b55050746"
D = V / "batch-094-publication-688"
HEAD = "7dc89d688e935a57104175a675a18832afd42f60"
MAIN = "48765e20846e1d6769c6ddc35146f6ce58deab57"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
INITIAL = "d1e986ec1a8c162beeaf4ae452a94be4c7b8b598"
CORRECTED = "b85d7a4d40225ad829891c1c7fe3b31f8cd31afe"
VERSION = "74b7e886a1afbd46"
MEMBER = "\u524a"
BEFORE = L / "progress-before-688.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(path.suffix + ".688.tmp")
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


def context(head):
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
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (687, "094", "continue")
    clean(A, APP)
    clean(R, head)
    return {"parentPid": 19008, "session": L.name, "decodedLauncherMatches": True,
            "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
            "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain]}


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8438
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                data = (R / name).read_bytes()
                if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == digest, name


def start():
    role = context(HEAD)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("merge-base", MAIN, HEAD) == MAIN
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution687CoordinatorCheckpoint"] == p["execution687CoordinatorCheckpoint"]
    state = {
        "execution": 688, "batch": "094", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME094 owner fast-forward publication, terminal CI, exact public ZIP and verified ownerissue; yield before095. No redundant reviewer/native/host.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete issue and final687 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers accessed.",
    }
    save(L / "starting-state-688.json", state)
    p["execution688StartingState"] = state
    p.update(stage="batch-094-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    assert all(p[k] == v for k, v in load(BEFORE).items() if k not in {"stage", "nextAction", "blocker"})
    gate()


def gate():
    context(HEAD)
    e = load(S / "execution-687.json")
    assert e["runtimeAccepted"] and not e["runtimePublished"]
    assert (e["pythonTestsPassed"], e["validatorErrors"], e["hostTestsExecuted"], e["hostTestsSkipped"]) == (372, 0, 4, 0)
    assert e["hostChecksFresh"] and e["manifestFresh"] and e["vocabularyConsistencyPassed"]
    for row in e["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    for row in e["hostSuites"]:
        suite = row["suite"]
        assert all(suite[k] == "0" for k in ("skipped", "failures", "errors"))
        assert len(row["cases"]) == int(suite["tests"])
    spec = importlib.util.spec_from_file_location("accepted687", C / "accept-batch-094-687.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    inherited = module.inherited()
    assert inherited == e["inheritedAcceptance"]
    review = load(V / "batch-094-combined-reconciliation-687.json")
    assert review["runtimeAccepted"] and all(
        value == "CLEAN" for verdict in review["verdicts"].values() for value in verdict.values())
    assert all(f["status"] == "resolved" for f in review["reconciliation"])
    assert load(S / "batch-094-progress.json")["reviewClosed"] == [MEMBER]
    runtime()
    save(L / "prepublication-gate-688.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G", "runtimeHashesVerified": 8438,
        "combinedReceiptsVerified": len(e["receipts"]), "inheritedAcceptance": inherited,
        "parentLockTouched": False, "newReviewerNativeHostRuns": 0})
    print("Signed acceptance, full inherited review/native receipts and all8438 runtime hashes verified.")


def public(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-094-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8438 and archive["manifestEqual"]
    assert all(archive[k] for k in ["allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (18000, 42*1024**2, 80*1024**2, 56*1024**2)
    return ci, archive


def verify(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-094-{phase}-ci.json"
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
    save(L / f"archive-download-{phase}-688.json", {"commit": head, "url": url,
        "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
        head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-094-publication.json").exists()
    D.mkdir()
    p, before = load(C / "progress.json"), load(BEFORE)
    e = load(S / "execution-687.json")
    ledger = load(S / "batch-094-progress.json")
    counts = dict(e["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=121, remainingAdditions=1107,
        namedSourceMembersPresent=131, batchNewNecessarySupportWords=0, projectNewNecessarySupportWords=121,
        batchChangedReusedArticles=3, allMappedReciprocalPairs=3, mappedDirectedLinks=6,
        activatedBaselinePairs=2, separateExceptionPreserved="\u5996",
        separateEarlierLevelSourceMembers=list("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50"),
        earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert (counts["kanji"], counts["words"], counts["n1Labels"]) == (1117,5070,126)
    limits = {"combined": e["limits"], "inherited": e["inheritedAcceptance"]["originalLimits"],
        "clarification": "Historical pending flags retained, not erased: combined687 and accepted/terminal688 discharge only their recorded scope. All source/read/native/font/injectedtrace/MLKit/pool/phone limitations remain."}
    publication = {
        "schemaVersion": 1, "execution": 688, "batch": "094", "membership": [MEMBER],
        "status": "published-verified-bounded-owner-testing", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": ledger["baseCommit"], "authoredSnapshot": INITIAL,
        "initialReviewedTeachingSnapshot": INITIAL, "reviewedTeachingSnapshot": CORRECTED,
        "combinedContentHead": e["combinedContentHead"], "latestMainIntegrated": MAIN,
        "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"] for n in range(676,688)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-094-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-094-rendered-reconciliation-683.json",
        "correctionRecord": "../n1-reviews/batch-094-correction-reconciliation-686.json",
        "nativeRecords": ["execution-682.json", "execution-686.json"], "combinedAcceptanceRecord": "execution-687.json",
        "validation": e["sourceAudit"], "pythonTestsPassed": 372, "hostTestsReverified": 4,
        "nativeTerminalCasesReverified": 3, "newReviewNativeHostRuns": 0, "ci": ci,
        "immutablePublicArchive": archive, "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP, "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits, "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before095."}
    save(S / "batch-094-publication.json", publication)
    ledger["prePublicationCheckpoint688"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=121,
        remainingAdditions=1107, publishedCommit=HEAD, runtimePublished=True, publicationRecord="batch-094-publication.json",
        pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
        nextAction=publication["nextAction"], publicationClarification=limits["clarification"])
    save(S / "batch-094-progress.json", ledger)
    receipts = []
    for name, tool in [("validate","tools\\validate.py"),("manifest","tools\\build_manifest.py"),("budget","tools\\check_content_budget.py")]:
        path = D / f"{name}-688.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable,"-X","utf8","-B",tool],cwd=R,stdout=stream,stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path":path.relative_to(R).as_posix(),"sha256":sha(path),"exitCode":0})
    save(S / "execution-688.json", {
        "schemaVersion":1,"execution":688,"batch":"094","status":publication["status"],
        "startingState":p["execution688StartingState"],"publicationRecord":"batch-094-publication.json",
        "acceptedCommit":HEAD,"counts":counts,"ci":ci,"immutablePublicArchive":archive,
        "inheritedAcceptanceRecord":"execution-687.json","runtimeBytesUnchanged":True,"runtimePublished":True,
        "parentLockTouched":False,"optionalHistoricalSessionHelpersAccessed":False,"actualNewPermissionDenials":[],
        "newReviewNativeHostRuns":0,"limits":limits,"terminalLocalValidation":receipts,
        "physicalPhoneAcceptance":"outstanding","generalReleaseAcceptance":"outstanding",
        "wholeProjectComplete":False,"nextBatchStarted":False})
    for path in [L/"prepublication-gate-688.json",L/"starting-state-688.json",
        L/"archive-download-accepted-688.json",C/"artifacts/batch-094-accepted-ci.json",
        C/"artifacts"/f"content-{HEAD[:7]}-acceptance.json",C/"verify-batch-002-publication.py",
        C/"publish-688.ps1",Path(__file__)]:
        shutil.copyfile(path,D/path.name)
    runtime()
    p.update(stage="batch-094-accepted-published-awaiting-terminal-evidence",nextAction=publication["nextAction"])
    p["execution688AcceptedPublication"]=copy.deepcopy(publication)
    save(C/"progress.json",p)
    print("Accepted delivery verified; publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal",head)
    publication=load(S/"batch-094-publication.json")
    body=f"""Batch **094 ({MEMBER})** is published and verified for bounded owner testing. Existing N2 **削る (けずる)** and **削除 (さくじょ)** reused; no new support word. Three all-mapped reciprocal pairs/six directions, TWO newly activated baseline pairs; 除 receives navigation only. Identities, primary readings, N2 levels, titles and original exclusions retained. Three source-supported direct guards plus subsequently observed **削る/縮める** guard are resolved; direct exclusions are not transitive cliques.

Authored/initial reviewed `{INITIAL}`; corrected reviewed metadata `{CORRECTED}`. Initial678 blind serial two-family reviews actually **Claude Opus5.5 / GPT6.1Sol**, same frozen snapshot;679 original-session corrections,683 dependent rendered confirmations and685 direct-pair confirmations retained, NOT new blind review credit. Original683 Claude overlapping-tool execution remains **REJECTED**, followed by accepted serial repair; no process relabeling. Original full reports, optional polish, supplied-source and actual read/visual limitations remain.

Combined687 content `{publication['combinedContentHead']}`, freshmain `{MAIN}` already ancestral: no teaching merge or runtime change. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards, global account unchanged. Combined687 **372Python tests**, validator0errors, vocabulary consistency(pilot2122/2431, NOTfullcoverage), manifest/budget/frozen sources/full baseline/exact membership/all readings/three mapped pairs/six directions/two activated pairs/pinnedNINEstrokes/font provenance/all8438runtimehashes passed. Fresh687 **3RealContentTest+1RareHanTest** passed without skips/failures/errors; no new reviewer/native/host688.

Full raw **サク / けず.る・はつ.る・そ.ぐ** preserved in source order; explicit curated **[サク]/[けず.る]**, only **さく/けずる** offered/persistedGood+Done. はつる andそぐ are retained recognition readings, NOT declared obsolete or invalid. Per-sense kana flags kept distinct; no invented frequency/etymology or unnecessary support.

Inherited682 native routes/85captures/four productionfont selections/41visibleHan and original-session683 rendered confirmations preserved. Cmapabsences刂/斫/氵/阝 are not glyph failures. Added metadata-only縮 makes42rawHan; bundled cmaps verified, no new visible-glyph claim. Reduced contact sheets/tool resizes/read limitations and unspecified exact fallbackface remain explicit.

Corrected native686 imported exact full archive through production **ContentSync ONCE**: **1117kanji/5070words/126N1,zeroProblems/acceptedRoomreadingEpoch1/version `{VERSION}`**; terminalcase0/no skips. **128productionWordQuizBuilder** direct削る/縮める checks covered BOTHtargetorientations/BOTHdirections/All+boundedcustom/16seeds. Earlier682 TWOterminalcase0 and384boundedguardrecords/selection/meaning/reading/drawing/articles/reciprocalnavigation/SystemBack/offline inherited; old682 import is NOT relabeled corrected686. No exhaustive random-pool semantic certification.

Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, NOTlatestappmain. API35emulator/injectedtrace/recallgiveup is **NOT physicalphone/humanhandwriting/successfulMLKit evidence**. All original native/font/shape-grading limits remain.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable publicZIPs preserve **all8438runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB and perfile/media/safepath guards; contributor evidence excluded.

Published **121/1228additions;1107remain**. Collection **1117kanji/5070words/126N1labels/131named-source members plus separate妖**. Six separately placed earlierN2 source members保/案/派/第/策/結 preserved, not issue60accepted additions; do not duplicate/relevel. Necessarysupportarticles remain121project-wide, **NOT an N1vocabularydeck**.

Durable evidence: `docs/n1-sources/batch-094-publication.json`, `execution-688.json`, original678/679textual,682native,683rendered,685/686correction and687combined records. Historical pending flags preserved with scoped discharge, not erased. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock: no child lock or optional historical-session helper access. Checkpoint688 persists continue and yields before095; no nextbatch/secondrunner.
"""
    target=C/"batch-094-publication-comment.txt"
    assert not target.exists()
    target.write_text(body,encoding="utf-8")
    save(L/"terminal-publication-688.json",{"head":head,"ci":ci,"archive":archive,"issueBodySha256":sha(target)})


def finish(head):
    ci,archive=public("terminal",head)
    receipt=load(C/"batch-094-publication-issue-receipt.json")
    remote=json.loads(output(["gh","api",f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body=(C/"batch-094-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"]==remote["user"]["login"]=="stop-cran"
    assert receipt["body"]==remote["body"]==body
    assert output(["gh","api","user","--jq",".login"])=="romanko-ms"
    assert not (S/"batch-095-progress.json").exists()
    ledger=load(S/"batch-094-progress.json")
    assert ledger["membership"]==ledger["reviewClosed"]==ledger["published"]==[MEMBER]
    publication=load(S/"batch-094-publication.json")
    next_action=(
        f"Batch094 accepted/published/verified at {head}; yield before095. Next coordinator ONE bounded095 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent19008 retainsrunner.lock: no childacquire/delete/unlock. Approvedcontrol/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield actual"
        "newdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/baseline/"
        "fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/two serialblind"
        "differentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published121/1228;1107acceptance-remainder;1117kanji5070words126N1labels131namedmembers+separate妖; "
        "121necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.094initiald1e986ec/textual678+679/"
        "native682/rendered683/correction685+686/combined687/accepted7dc89d68/version74b7e886a1afbd46/"
        "8438runtimehashes;372Python/fresh687host4/inheritednative682two+686one/accepted+terminalCI+ZIP/"
        "ownerissueverified. No freshreview/native/host688. OriginalClaude/GPTreports/optionalpolish/sourceandread"
        "limits retained. Original683ClaudeoverlapREJECTED; serialrepairaccepted, never relabeloriginal. "
        "Corrected686ContentSyncONCE1117kanji5070words126N1/zeroProblems/epoch1/versionmatchescombined; "
        "128productionWordQuizBuilderdirect削る-縮めるchecks,bothorientations/directions/All+custom/16seeds. "
        "Fullrawサク/けず.る,はつ.る,そ.ぐ/sourceorder/curation[サク]/[けず.る]retained;onlyさく/けずるGood+Done. "
        "Recognitionはつる/そぐnotobsolete/invalid. THREEallmappedpairs/SIXdirections/TWOactivatedbaselinepairs, "
        "existing削る/削除N2identity/primaryreading/title/originalguards preserved;navigationonly除. "
        "85unchangedcaptures/41visibleHan/fourfonts/682routes/683rendered inherited;42rawHanincludesmetadataonly縮. "
        "Cmapabsences刂斫氵阝NOTglyphfailure;contactsheetreductions/toolresizes/fallbackface/readlimits retained. "
        "InjectedtraceNOThumanhandwriting/no successfulMLKit/no exhaustivepoolsemantics. QualifiedTESTONLY"
        "Android1c1b7bf4 retainsproductionf9b59a2, NOTlatestappmain;compatiblef9b59a2+required. "
        "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No095started/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head,remoteMainVerified=head,terminalCi=ci,
        terminalImmutablePublicArchive=archive,issueUpdate=receipt["html_url"],nextAction=next_action)
    save(C/"batch-094-publication-checkpoint.json",publication)
    save(L/"batch-094-publication-checkpoint.json",publication)
    before,p=load(BEFORE),load(C/"progress.json")
    p["execution688StartingState"]["status"]="bounded-publication-checkpoint-complete"
    verification={
        "schemaVersion":1,"execution":688,"checkpoint":688,"batch":"094","savedCommit":head,"signature":"G",
        "remoteMainVerified":head,"acceptedCommit":HEAD,"acceptedCi":publication["ci"]["databaseId"],
        "terminalCi":ci["databaseId"],"bothImmutablePublicArchivesVerified":True,"runtimeHashesPerArchive":8438,
        "reviewedRuntimeBytesUnchanged":True,"dedicatedWorktreesClean":True,
        "allOriginalHistoricalRootValuesPreservedExactly":True,"originalRootKeysCompared":len(before),
        "ownerIssueAuthorAndBodyVerified":True,"issueUpdate":receipt["html_url"],"globalIdentityUnchanged":True,
        "parentLockTouched":False,"optionalHistoricalSessionHelpersAccessed":False,"actualNewPermissionDenials":[],
        "status":"continue","stage":"batch-094-published-verified-before-095","publishedAdditions":121,
        "remainingAdditions":1107,"lastPublishedCommit":head,"nextAction":next_action,"blocker":None,
        "physicalPhoneAcceptance":"outstanding","generalReleaseAcceptance":"outstanding",
        "wholeProjectComplete":False,"nextBatchStarted":False}
    p["execution688CoordinatorCheckpoint"]=verification
    p["batch094PublicationCheckpoint"]=publication
    p["batch094PublicationIssueReceipt"]={"id":receipt["id"],"url":receipt["html_url"],"author":"stop-cran",
        "bodySha256":sha(C/"batch-094-publication-comment.txt"),"verified":True}
    p.update(checkpoint=688,status="continue",stage=verification["stage"],lastPublishedCommit=head,
        remainingAdditions=1107,blocker=None,nextAction=next_action)
    p["unmetAcceptanceGates"]=copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0]="Remaining1107 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed={"checkpoint","status","stage","lastPublishedCommit","remainingAdditions","blocker","nextAction","unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k]==v for k,v in before.items() if k not in allowed)
    save(L/"coordinator-checkpoint-688.json",verification)
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
