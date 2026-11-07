"""Publish accepted batch 101 under the live parent launcher's lock."""
import base64
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
L = C / "logs" / "1948f3d5-ecf0-44ba-80c4-7a39c33ca265"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-101-publication-771"
HEAD = "17ddb4da1f102552d3307c0c19227d9545ed7f27"
MAIN = "ba1a7f467a2431523e3131d4f259c1d3260c93af"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
VERSION = "6e9b74967e21fc3c"
MEMBER = "\u529f"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data, replace=False):
    assert replace or not p.exists(), p
    temp = p.with_suffix(p.suffix + ".771.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    os.replace(temp, p)
    assert load(p) == data


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def output(args, root=R):
    return subprocess.check_output(args, cwd=root, encoding="utf-8").strip()


def git(*args, root=R):
    return output(["git", "--no-pager", "-C", str(root), *args])


def context(head=HEAD, clean=True):
    assert not os.environ.get("GH_TOKEN") and not os.environ.get("GITHUB_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (5920, "running", L.name)
    script = f"""
$id={os.getpid()};$chain=@()
while($id -gt 0 -and $chain.Count -lt 12){{
 $p=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(!$p){{break}}
 $chain+=@{{pid=[int]$p.ProcessId;parent=[int]$p.ParentProcessId;name=$p.Name;command=$p.CommandLine}}
 if($id -eq 5920){{break}}
 $id=$p.ParentProcessId
}}
$chain|ConvertTo-Json -Depth 4 -Compress
"""
    chain = json.loads(output(["pwsh", "-NoProfile", "-NonInteractive", "-Command", script]))
    assert chain[-1]["pid"] == 5920
    assert any(p["name"].lower() == "copilot.exe" and f"--session-id {L.name}" in p["command"]
               for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert f"& {C / 'runner.ps1'}" in base64.b64decode(encoded).decode("utf-16-le")
    launcher_hash = sha(C / "runner.ps1")
    assert launcher_hash == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["batch"], state["status"]) == (770, "101", "continue")
    for root, expected in ((R, head), (A, APP)):
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if clean or root == A:
            assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    return {"parentPid": 5920, "session": L.name, "decodedLauncherMatches": True,
            "launcherSha256": launcher_hash, "parentLockTouched": False,
            "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain]}


def helper():
    p = C / "accept-batch-101-combined-770.py"
    assert sha(p) == "0674155d14613ad05537205209ce8eafe9770e6c51ebf844f600d5a616ff908b"
    spec = importlib.util.spec_from_file_location("accepted770", p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime():
    result = helper().runtime()
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return result


def start():
    role = context()
    state = load(C / "progress.json")
    assert state == load(L / "checkpoint-full.json")
    assert git("rev-parse", "origin/main") == MAIN and git("merge-base", MAIN, HEAD) == MAIN
    save(L / "progress-before-771.json", state)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    a, b = embedded["execution770CoordinatorCheckpoint"], state["execution770CoordinatorCheckpoint"]
    assert a.keys() == b.keys()
    assert all(v == b[k] for k, v in a.items() if k != "recordedAt")
    assert datetime.fromisoformat(a["recordedAt"]) == datetime.fromisoformat(b["recordedAt"])
    record = {
        "execution": 771, "batch": "101", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME101 owner publication, exact remote/terminal CI/public ZIP/verified owner issue and durable checkpoint; yield before102.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request decoded and complete checkpoint parsed; operative contract, entire approved issue and final770 inspected directly. Historical middle parsed, not freshly semantically rereviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session recipes accessed.",
    }
    save(L / "starting-state-771.json", record)
    state["execution771StartingState"] = record
    state.update(stage="batch-101-owner-publication-in-progress", nextAction=record["scope"], blocker=None)
    save(C / "progress.json", state, replace=True)
    print("SAME101 publication started; clean signed heads/live launcher verified; full history preserved.")


def gate():
    context()
    accepted = load(S / "execution-770.json")
    assert accepted == load(V / "batch-101-combined-acceptance-770.json")
    assert accepted["runtimeAccepted"] and not accepted["runtimePublished"]
    assert accepted["reviewClosed"] == [MEMBER] and not accepted["published"]
    assert accepted["actionableRemainingFindings"] == accepted["consequentialUnresolvedUnqualifiedTeachingClaims"] == 0
    assert accepted["checks"]["pythonTests"] == 377
    assert accepted["checks"]["validatorErrors"] == 0 and accepted["checks"]["manifestFresh"]
    for row in accepted["receipts"]:
        p = R / row["archive"]
        assert sha(p) == row["archiveSha256"]
        raw = gzip.decompress(p.read_bytes()) if row.get("losslessGzip") else p.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    inherited = helper().inherit()
    assert inherited["hostTests"] == 5 and inherited["nativeTerminalCaseSuccesses"] == 2
    save(L / "prepublication-gate-771.json", {
        "execution": 771, "acceptedSignedCheckpoint": HEAD, "runtime": runtime(),
        "acceptanceReceiptHashesReverified": len(accepted["receipts"]),
        "inheritedAcceptance": inherited, "freshReviewerNativeHostRuns": 0})
    print("Acceptance/source/review/HOST/native receipts and all8455 runtime hashes verified.")


def verify(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    runs = json.loads(output(["gh", "run", "list", "--repo", "stop-cran/learning-japanese",
        "--commit", head, "--workflow", "Validate content", "--limit", "5",
        "--json", "databaseId,status,conclusion,headSha"]))
    assert runs and runs[0]["headSha"] == head, "Exact CI not available; preserve pending checkpoint"
    subprocess.run(["gh", "run", "watch", str(runs[0]["databaseId"]), "--repo",
        "stop-cran/learning-japanese", "--exit-status", "--interval", "10"], check=True)
    ci = json.loads(output(["gh", "run", "view", str(runs[0]["databaseId"]), "--repo",
        "stop-cran/learning-japanese", "--json", "databaseId,status,conclusion,headSha,workflowName,jobs"]))
    save(L / f"{phase}-ci-771.json", ci)
    p = C / "artifacts" / f"content-{head[:7]}.zip"
    assert not p.exists(), p
    url = f"https://codeload.github.com/stop-cran/learning-japanese/legacy.zip/{head}"
    result = subprocess.run(["curl.exe", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "180", url, "--output", str(p)], capture_output=True, text=True)
    save(L / f"archive-download-{phase}-771.json", {
        "commit": head, "url": url, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    verifier = C / "verify-batch-002-publication.py"
    assert sha(verifier) == "8d07dcdb04eefa2bef9f1fb66f9a47e0f3711f9328eb15c9da13606ed8b42a6d"
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(verifier), head, str(p),
                    str(L / f"{phase}-archive-771.json")], check=True)
    public(phase, head)


def public(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci, archive = load(L / f"{phase}-ci-771.json"), load(L / f"{phase}-archive-771.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8455 and archive["manifestEqual"]
    assert all(archive[k] for k in ("allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    sys.path.insert(0, str(R / "tools"))
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def records():
    ci, archive = public("accepted", HEAD)
    accepted = load(S / "execution-770.json")
    counts = dict(accepted["sourceAudit"]["currentCounts"])
    assert (counts["kanji"], counts["words"], counts["n1Labels"]) == (1124, 5073, 133)
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=128, remainingAdditions=1100,
                  batchNewNecessarySupportWords=0, projectNewNecessarySupportWords=124,
                  batchChangedReusedArticles=3, allMappedReciprocalPairs=4,
                  mappedDirectedLinks=8, activatedBaselinePairs=2)
    initial = load(V / "batch-101-reconciliation.json")
    publication = {
        "schemaVersion": 1, "execution": 771, "batch": "101", "membership": [MEMBER],
        "status": "published-verified-bounded-compatible-client-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": accepted["sourceAudit"]["baseCommit"],
        "authoredSnapshot": initial["originalTeachingSnapshot"],
        "reviewedSnapshot": initial["originalTeachingSnapshot"],
        "combinedTestedSnapshot": accepted["combinedTestedSnapshot"], "latestMainIntegrated": MAIN,
        "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-101-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-101-rendered-769/reconciliation.json",
        "combinedAcceptanceRecord": "execution-770.json", "nativeRecord": "execution-768.json",
        "validation": accepted["sourceAudit"], "pythonTestsPassed": 377,
        "hostTestsReverified": 5, "nativeTerminalCasesReverified": 2, "newReviewNativeHostRuns": 0,
        "ci": ci, "immutablePublicArchive": archive, "counts": counts, "contentVersion": VERSION,
        "qualifiedAndroidHead": APP,
        "compatibleClient": "Approved Android #132/main2edbf366 guard plus #125 curated readings required. Old clients ignore these metadata fields; not universal synonym detection.",
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "limits": accepted["limits"], "historicalPendingFlagsPreserved": True,
        "pendingPublicationGateDisposition": "Accepted commit CI and exact public ZIP verified; terminal evidence/issue/checkpoint still pending.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": "Verify terminal evidence CI/public ZIP/owner issue; checkpoint and yield before102.",
    }
    save(S / "batch-101-publication.json", publication)
    ledger = load(S / "batch-101-progress.json")
    ledger["prePublication771State"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=128,
                  remainingAdditions=1100, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-101-publication.json", nextAction=publication["nextAction"],
                  pendingGates=["Terminal evidence CI/public ZIP/verified owner issue; physical-phone/general-release and whole-set outstanding."])
    save(S / "batch-101-progress.json", ledger, replace=True)
    save(S / "execution-771.json", {
        "schemaVersion": 1, "execution": 771, "batch": "101", "status": publication["status"],
        "startingState": load(L / "starting-state-771.json"), "publicationRecord": "batch-101-publication.json",
        "acceptedCommit": HEAD, "runtimeBytesUnchanged": True, "runtimeAccepted": True,
        "runtimePublished": True, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "newReviewerNativeHostRuns": 0, "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False})
    assert not D.exists()
    D.mkdir()
    for p in (Path(__file__), C / "publish-771.ps1", C / "verify-batch-002-publication.py",
              L / "starting-state-771.json", L / "prepublication-gate-771.json",
              L / "archive-download-accepted-771.json", L / "accepted-ci-771.json",
              L / "accepted-archive-771.json"):
        shutil.copyfile(p, D / (p.name + (".txt" if p.suffix == ".ps1" else "")))
    state = load(C / "progress.json")
    state["execution771AcceptedPublication"] = copy.deepcopy(publication)
    state.update(stage="batch-101-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    save(C / "progress.json", state, replace=True)
    runtime()
    print("Accepted delivery verified; publication ledgers ready for signed terminal evidence.")


def comment(head):
    ci, archive = public("terminal", head)
    p = load(S / "batch-101-publication.json")
    body = f"""Batch **101 ({MEMBER})** is published and verified for bounded compatible-client owner testing. No new support article or vocabulary level: existing **功績 (こうせき), N2** and **成功 (せいこう), N3** retain their identities/readings/levels. FOUR all-mapped pairs/EIGHT link directions/TWO activated baseline pairs; THREE exact reused navigation changes; FIVE pinned generated strokes.

Authored/reviewed `{p['reviewedSnapshot']}`; combined-tested `{p['combinedTestedSnapshot']}`; signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Original serial blind **claude-opus-5.5 / gpt-6.1-sol** and original-session769 rendered confirmations retained. No new reviewer/HOST/native run771 or new blind credit. Each rendered reviewer received26 assigned PNGs, not34 individually viewed originals; mapped contact sheets, resizing/duplicate/read-depth limits remain. No actionable defect or consequential unresolved unqualified changed-teaching claim remains.

All raw readings/order **コウ・ク; いさお** preserved. Curated **[コウ]/[]** offers **こう** only; persistedGood/Done1of1 in native768. **ク** is not exclusively/mainly religious; **いさお** is a dated lexical noun, not merely nanori. THIRTEEN supported direct symmetric NONTRANSITIVE kanji guards, not synonym cliques. Actual default N1 wrong choices: ONE curated **刀 (sword; blade)** and TWO fallbacks **松 (pine tree)/梨 (pear tree)**; **加 stays N3, 幼 stays N2**. Native64 production choices/25 labels are bounded accepted samples, NOT universal future-pool semantic certification. Unchanged功績sevenwordguards preserved; six unsupplied legacy titles remain **UNVERIFIED outside exact navigation-only scope**.896mechanical wordguard checks are not complete semantic certification.

Fresh main `{MAIN}` remains an ancestor; ZERO incoming/runtime/teaching changes. Normal stop-cran process-scoped fast-forwards; global romanko-ms unchanged. Combined770 **377 Python tests**, validator0errors, regenerated manifest, vocabulary consistency(**2122/2431 pilot**, not complete coverage), frozen sources/fullbaseline/exactmembership/allreadings/pinnedstrokes/fonts/allmappedlinks/originalbudgets passed. HOST766 FIVE non-skipped cases and native768 TWO terminalcase0 successes inherited/reverified, NOT rerun771. Native fullarchive production **ContentSync ONCE**: **1124kanji/5073words/133N1,zeroProblems,both accepted parser epochs1**, version `{VERSION}`; **2912direct guards/2496NONTRANSITIVEneighbor checks/896preservedwordguards/64actual production-builder choices/25sampledlabels**. Actual N1 selection/meaning/curated reading/five-stroke drawing/articles/links/SystemBack/offline/19Han across four font families retained. Injected strokes/seeded due/shape-only drawing with model unavailable are NOT successful MLKit/human mastery/phone evidence. Cmap/raster evidence alone is not readability; original-session rendered confirmation limits remain.

Accepted CI [{p['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{p['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. BOTH immutable publicZIPs preserve **all8455 runtime hashes** and manifest. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB/perfile/media/safepath guards; contributor evidence excluded.

Published **128/1228additions;1100remain**. Collection **1124kanji/5073words/133N1labels/138named-source members plus separate妖**. Six separately placed source保/案/派/第/策/結 retain earlierN2levels, not issue60accepted additions; no duplication/relevel. Necessarysupportarticles124project-wide, NOT an N1 vocabulary deck. Compatible **stop-cran/kanji-cards-android#132** plus **stop-cran/kanji-cards-android#125** required; old clients ignore guards/curation. Qualified Android `{APP}` carries approved guard and schema-only bridges, NOT unrelated latest-app behavior.

Durable `docs/n1-sources/batch-101-publication.json`, `execution-771.json`, textual765/HOST766/native768/rendered769/combined770 records. Historical pending flags preserved with scoped discharge; all original evidence/permission/process limitations retained. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent5920 retainsrunner.lock: no childacquisition/deletion/unlock/readprobe; no optional historicalsessionhelper or actualnewdenial. Checkpoint771 continues and yields before102; no nextbatch/secondrunner.
"""
    path = C / "batch-101-publication-comment.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-771.json",
         {"head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(path)})


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(L / "issue-771-reread.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-101-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["id"] == remote["id"] and receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-102-progress.json").exists()
    ledger = load(S / "batch-101-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == [MEMBER]
    publication = load(S / "batch-101-publication.json")
    next_action = (
        f"Batch101 accepted/published/verified at {head}; yield before102. Next coordinator ONE bounded102 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent5920 retainsrunner.lock: NOchildacquire/delete/unlock/readprobe. "
        "Approvedcontrol/committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/"
        "report/yield actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/"
        "usefulness/baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/"
        "combinedmain/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries/"
        "42MiBcompressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published128/1228;1100acceptance-remainder;1124kanji5073words133N1labels138namedmembers+separate妖; "
        "124necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.101功/no new support/threeexactreusednavigationchanges/"
        "fullコウクいさおsourceorder/[コウ]/[]/onlyこう/クnotexclusivelymainlyreligious/いさおdatedlexicalnounNOTjustnanori. "
        "功績N2/成功N3 unchanged;sevenlegacy功績wordguards preserved, sixunsuppliedlegacytitles explicitlyUNVERIFIED "
        "outside exactnavigation-only scope,896mechanicalchecks NOTcomplete semanticcertification. FOURallmappedpairs/"
        "EIGHTdirections/TWOactivatedbaselinepairs/FIVEpinnedstrokes/THIRTEENdirectsymmetricNONTRANSITIVEkanjiguards. "
        "N1ONEcurated刀plusTWOfallbacks松梨;加N3幼N2 unchanged/no mask/relevel/futurepoolguarantee. "
        "HOST766fivecases/noskips/native768TWOterminalcase0/ContentSyncONCE1124kanji5073words133N1zeroProblems/"
        "bothepochs1/2912directguards2496neighbors896wordguards64builderchoices25labels. Original-session769 "
        "26assignedPNGseach/8mappedcontactsheets+15standaloneoriginals+3panels NOT34separatelyviewedoriginals/"
        "image resizing/readdepth/duplicate limits retained/NOTfreshblind;19Han/fourfonts/injectedstrokesseededdueshapeonly "
        "modelunavailable NOTMLKithumanmasteryphone. CompatibleAndroid#132 main2edbf366 plus#125 required; oldclientsignore. "
        "QualifiedsignedAndroidbf30cdead8515739bc0e671d57a54b9a3109dd46 approvedguard+schemaonlybridges NOTunrelatedlatestmain. "
        "Combined770377Python/version6e9b74967e21fc3c/8455runtimehashes/accepted+terminalCI+ZIP/ownerissueverified771; "
        "no newreviewnativehost771. Historical evidence/process/permission/OOM/source-only/pending limitations preserved, "
        "no retroacceptance. Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No102started/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       pendingPublicationGateDisposition="Terminal CI/public ZIP/owner issue verified; bounded owner-testing delivery closed, not phone/general release.",
                       nextAction=next_action)
    save(C / "batch-101-publication-checkpoint.json", publication)
    save(L / "batch-101-publication-checkpoint.json", publication)
    before, state = load(L / "progress-before-771.json"), load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 771, "checkpoint": 771, "batch": "101",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8455,
        "contentVersion": VERSION, "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-101-published-verified-before-102",
        "publishedAdditions": 128, "remainingAdditions": 1100, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False}
    state["execution771CoordinatorCheckpoint"] = checkpoint
    state["batch101PublicationCheckpoint"] = publication
    state["batch101PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-101-publication-comment.txt"), "verified": True}
    state.update(checkpoint=771, status="continue", stage=checkpoint["stage"],
                 lastPublishedCommit=head, remainingAdditions=1100, blocker=None, nextAction=next_action)
    state["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    state["unmetAcceptanceGates"][0] = (
        "Remaining1100 issue60 source-bounded additions not review-closed/published; six separately placed "
        "earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. "
        "All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain.")
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= state.keys()
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    assert load(C / "progress.json")["checkpoint"] == 770
    save(C / "progress.json", state, replace=True)
    verified = load(C / "progress.json")
    assert verified == state
    assert all(verified[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-771.json", checkpoint)
    print(json.dumps({k: v for k, v in checkpoint.items() if k != "nextAction"}, indent=2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "context":
        context(sys.argv[2])
    elif mode == "verify":
        verify(sys.argv[2], sys.argv[3])
    elif mode in {"comment", "finish"}:
        globals()[mode](sys.argv[2])
    else:
        {"start": start, "gate": gate, "records": records}[mode]()
