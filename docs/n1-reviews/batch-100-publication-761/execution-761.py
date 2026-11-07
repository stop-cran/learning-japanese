"""Publish the accepted batch 100; the live launcher retains runner.lock."""
import base64
import copy
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
L = C / "logs" / "e0b60b75-3585-4023-b843-b5965c536953"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-100-publication-761"
HEAD = "c27507c20c53c50686f463d1c337b077bac21c6c"
MAIN = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
VERSION = "606c836e4be33ba9"
MEMBER = "\u5275"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data, replace=False):
    assert replace or not p.exists(), p
    temp = p.with_suffix(p.suffix + ".761.tmp")
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
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["batch"], state["status"]) == (760, "100", "continue")
    for root, expected in ((R, head), (A, APP)):
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if clean or root == A:
            assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    return {"parentPid": 5920, "session": L.name, "decodedLauncherMatches": True,
            "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
            "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain]}


def helper():
    p = C / "accept-batch-100-combined-760.py"
    assert sha(p) == "27a76e13a48208f3aaf96d7dd0ae52675f294355f52738062a502eeb9e99d113"
    spec = importlib.util.spec_from_file_location("accepted760", p)
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
    save(L / "progress-before-761.json", state)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    a, b = embedded["execution760CoordinatorCheckpoint"], state["execution760CoordinatorCheckpoint"]
    assert a.keys() == b.keys()
    assert all(v == b[k] for k, v in a.items() if k != "recordedAt")
    assert datetime.fromisoformat(a["recordedAt"]) == datetime.fromisoformat(b["recordedAt"])
    record = {
        "execution": 761, "batch": "100", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME100 owner publication, exact remote/terminal CI/public ZIP/verified owner issue and durable checkpoint; yield before101.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request decoded and complete checkpoint parsed; operative contract, entire approved issue and final760 inspected directly. Historical middle parsed, not freshly semantically rereviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session recipes accessed.",
    }
    save(L / "starting-state-761.json", record)
    state["execution761StartingState"] = record
    state.update(stage="batch-100-owner-publication-in-progress", nextAction=record["scope"], blocker=None)
    save(C / "progress.json", state, replace=True)
    print("SAME100 publication started; clean signed heads/live launcher verified; full history preserved.")


def gate():
    context()
    accepted = load(S / "execution-760.json")
    assert accepted == load(V / "batch-100-combined-acceptance-760.json")
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
    assert inherited["hostTests"] == 4 and inherited["nativeTerminalCaseSuccesses"] == 2
    save(L / "prepublication-gate-761.json", {
        "execution": 761, "acceptedSignedCheckpoint": HEAD, "runtime": runtime(),
        "acceptanceReceiptHashesReverified": len(accepted["receipts"]),
        "inheritedAcceptance": inherited, "freshReviewerNativeHostRuns": 0})
    print("Acceptance/source/review/HOST/native receipts and all8453 runtime hashes verified.")


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
    save(L / f"{phase}-ci-761.json", ci)
    p = C / "artifacts" / f"content-{head[:7]}.zip"
    assert not p.exists(), p
    url = f"https://codeload.github.com/stop-cran/learning-japanese/legacy.zip/{head}"
    result = subprocess.run(["curl.exe", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "180", url, "--output", str(p)], capture_output=True, text=True)
    save(L / f"archive-download-{phase}-761.json", {
        "commit": head, "url": url, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    verifier = C / "verify-batch-002-publication.py"
    assert sha(verifier) == "8d07dcdb04eefa2bef9f1fb66f9a47e0f3711f9328eb15c9da13606ed8b42a6d"
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(verifier), head, str(p),
                    str(L / f"{phase}-archive-761.json")], check=True)
    public(phase, head)


def public(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci, archive = load(L / f"{phase}-ci-761.json"), load(L / f"{phase}-archive-761.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8453 and archive["manifestEqual"]
    assert all(archive[k] for k in ("allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    sys.path.insert(0, str(R / "tools"))
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def records():
    ci, archive = public("accepted", HEAD)
    accepted = load(S / "execution-760.json")
    counts = dict(accepted["sourceAudit"]["currentCounts"])
    assert (counts["kanji"], counts["words"], counts["n1Labels"]) == (1123, 5073, 132)
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=127, remainingAdditions=1101,
                  batchNewNecessarySupportWords=0, projectNewNecessarySupportWords=124,
                  batchChangedReusedArticles=3, allMappedReciprocalPairs=5,
                  mappedDirectedLinks=10, activatedBaselinePairs=1)
    initial = load(V / "batch-100-reconciliation.json")
    publication = {
        "schemaVersion": 1, "execution": 761, "batch": "100", "membership": [MEMBER],
        "status": "published-verified-bounded-compatible-client-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": accepted["sourceAudit"]["baseCommit"],
        "authoredSnapshot": initial["originalTeachingSnapshot"],
        "reviewedSnapshot": initial["correctedTeachingSnapshot"],
        "combinedTestedSnapshot": accepted["combinedTestedSnapshot"], "latestMainIntegrated": MAIN,
        "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-100-reconciliation.json",
        "semanticRecord": "../n1-reviews/batch-100-fallback-confirmation-755-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-100-rendered-759-reconciliation.json",
        "combinedAcceptanceRecord": "execution-760.json", "nativeRecord": "execution-758.json",
        "validation": accepted["sourceAudit"], "pythonTestsPassed": 377,
        "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2, "newReviewNativeHostRuns": 0,
        "ci": ci, "immutablePublicArchive": archive, "counts": counts, "contentVersion": VERSION,
        "qualifiedAndroidHead": APP,
        "compatibleClient": "Approved Android #132/main2edbf366 guard plus #125 curated readings required. Old clients ignore these metadata fields; not universal synonym detection.",
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "limits": accepted["limits"], "historicalPendingFlagsPreserved": True,
        "pendingPublicationGateDisposition": "Accepted commit CI and exact public ZIP verified; terminal evidence/issue/checkpoint still pending.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": "Verify terminal evidence CI/public ZIP/owner issue; checkpoint and yield before101.",
    }
    save(S / "batch-100-publication.json", publication)
    ledger = load(S / "batch-100-progress.json")
    ledger["prePublication761State"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=127,
                  remainingAdditions=1101, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-100-publication.json", nextAction=publication["nextAction"],
                  pendingGates=["Terminal evidence CI/public ZIP/verified owner issue; physical-phone/general-release and whole-set outstanding."])
    save(S / "batch-100-progress.json", ledger, replace=True)
    save(S / "execution-761.json", {
        "schemaVersion": 1, "execution": 761, "batch": "100", "status": publication["status"],
        "startingState": load(L / "starting-state-761.json"), "publicationRecord": "batch-100-publication.json",
        "acceptedCommit": HEAD, "runtimeBytesUnchanged": True, "runtimeAccepted": True,
        "runtimePublished": True, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "newReviewerNativeHostRuns": 0, "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False})
    assert not D.exists()
    D.mkdir()
    for p in (Path(__file__), C / "publish-761.ps1", C / "verify-batch-002-publication.py",
              L / "starting-state-761.json", L / "prepublication-gate-761.json",
              L / "preflight-761.json", L / "archive-download-accepted-761.json",
              L / "accepted-ci-761.json", L / "accepted-archive-761.json"):
        shutil.copyfile(p, D / (p.name + (".txt" if p.suffix == ".ps1" else "")))
    state = load(C / "progress.json")
    state["execution761AcceptedPublication"] = copy.deepcopy(publication)
    state.update(stage="batch-100-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    save(C / "progress.json", state, replace=True)
    runtime()
    print("Accepted delivery verified; publication ledgers ready for signed terminal evidence.")


def comment(head):
    ci, archive = public("terminal", head)
    p = load(S / "batch-100-publication.json")
    body = f"""Batch **100 ({MEMBER})** is published and verified for bounded compatible-client owner testing. No new support article: existing **創作 (そうさく), N2** and **作る (つくる), N5** retain their identities, readings, levels and 13/5 original word exclusions. FIVE all-mapped pairs/TEN link directions/ONE activated baseline pair; THREE narrowly changed reused articles; TWELVE pinned generated strokes.

Authored `{p['authoredSnapshot']}`; revised/reviewed `{p['reviewedSnapshot']}`; combined-tested `{p['combinedTestedSnapshot']}`. Original serial blind **claude-opus-5.5 / gpt-6.1-sol** reviews and necessary original-session semantic755/rendered759 confirmations retained. Each759 reviewer: actual exit0,17 serial calls/15 images, zero overlaps; exact-byte Claude coverage addendum preserved, NOT fresh blind credit. F1/C1-establish/H1-initial/N753-fallback-establish resolved; H1-wound withdrawn. Optional O1-O4/wrapping nonblocking. No consequential unresolved unqualified teaching claim remains in scope.

All SIX raw readings/order preserved: **ソウ・ショウ; つく.る・はじ.める・きず・けず.しける**. Curated **[ソウ]/[つく.る]** offers **そう/つくる** only. **ショウ/けず.しける** lexical allocation explicitly UNVERIFIED/unselected; no invented example. Recognition-only spelling qualifications remain. ELEVEN supported direct symmetric NONTRANSITIVE kanji guards; N1 has TWO eligible curated distractors **剣/倹** plus a fallback because **験 remains N4**. Default fallback **蚕 (silkworm)** confirmed; no masking/releveling/universal synonym detection or future-pool guarantee. **stop-cran/kanji-cards-android#132** (main `2edbf366a4a6fce594b2a6580bfc4252b98d3f6d`) plus curated-reading **stop-cran/kanji-cards-android#125** required; old clients ignore both metadata fields. Qualified Android `{APP}` carries approved guard and schema-only bridges, NOT unrelated latest-app behavior.

Fresh main `{MAIN}` remains an ancestor; ZERO incoming/runtime/teaching changes. Signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Normal stop-cran process-scoped fast-forwards; global romanko-ms unchanged. Combined760 **377 Python tests**, validator0errors, regenerated manifest, vocabulary consistency(**2122/2431 pilot**, not complete coverage), frozen sources/fullbaseline/exactmembership/allreadings/pinnedstrokes/fonts/allmappedlinks/originalbudgets passed. HOST756 FOUR non-skipped cases and corrected native758 TWO named terminalcase0 successes inherited/reverified, NOT rerun761. Native production **ContentSync ONCE**: **1123kanji/5073words/132N1,zeroProblems,both accepted parser epochs1**, version `{VERSION}`; **2464direct guards/1760NONTRANSITIVEneighbor checks/2304preservedwordguards/64actual production-builder choices/22sampledlabels**. N1 selection/meaning/two curated readings/drawing/articles/links/SystemBack/offline/21Han across four font families retained. Reduced contact sheets are NOT all46full-resolution PNGs; Back/offline relies on758execution. Injected strokes/seeded due/shape-only drawing are NOT successful MLKit/human mastery/phone evidence. Cmap coverage is NOT readability or fallback-face proof; actual fallback face remains unidentified.

Accepted CI [{p['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{p['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. BOTH immutable publicZIPs preserve **all8453 runtime hashes** and manifest. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB/perfile/media/safepath guards; contributor evidence excluded.

Published **127/1228additions;1101remain**. Collection **1123kanji/5073words/132N1labels/137named-source members plus separate妖**. Six separately placed source保/案/派/第/策/結 retain earlierN2levels, not issue60accepted additions; no duplication/relevel. Necessarysupportarticles124project-wide, NOT an N1 vocabulary deck.

Durable `docs/n1-sources/batch-100-publication.json`, `execution-761.json` and source/textual/HOST756/native758/rendered759/combined760 records. Historical pending flags preserved with scoped discharge; all original evidence/permission/process limitations retained. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent5920 retainsrunner.lock: no childacquisition/deletion/unlock/readprobe; no optional historicalsessionhelper or actualnewdenial. Checkpoint761 continues and yields before101; no nextbatch/secondrunner.
"""
    path = C / "batch-100-publication-comment.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-761.json",
         {"head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(path)})


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(L / "issue-761-reread.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-100-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["id"] == remote["id"] and receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-101-progress.json").exists()
    ledger = load(S / "batch-100-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == [MEMBER]
    publication = load(S / "batch-100-publication.json")
    next_action = (
        f"Batch100 accepted/published/verified at {head}; yield before101. Next coordinator ONE bounded101 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent5920 retainsrunner.lock: NOchildacquire/delete/unlock/readprobe. "
        "Approvedcontrol/committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/"
        "report/yield actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/"
        "usefulness/baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/"
        "combinedmain/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries/"
        "42MiBcompressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published127/1228;1101acceptance-remainder;1123kanji5073words132N1labels137namedmembers+separate妖; "
        "124necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.100創/no new support/threeexactreusedchanges/"
        "sixfullreadings sourceorder/[ソウ]/[つく.る]/onlyそうつくる/source-onlyショウけず.しける explicitly"
        "UNVERIFIEDunselected. 創作N2/作るN5/13and5wordguards preserved. FIVEallmappedpairs/TENdirections/"
        "ONEactivatedbaselinepair/TWELVEpinnedstrokes/ELEVENdirect symmetricNONTRANSITIVEkanjiguards. "
        "N1TWOcurated剣倹plusfallback because験N4; no mask/relevel/futurepoolguarantee. N753-fallback-establish "
        "resolved755/758/759, default蚕silkworm. HOST756fourcases/noskips/native758TWOterminalcase0/"
        "ContentSyncONCE1123kanji5073words132N1zeroProblems/bothepochs1/2464directguards1760neighbors"
        "2304wordguards64builderchoices22labels. Original-session759 each17serialcalls15imageszerooverlaps/"
        "exactbyteClaudeaddendum/NOTfreshblind;21Han/fourfonts via reducedsheets NOTall46fullPNGs/"
        "Backoffline758/injectedstrokesseededdueshapeonlyNOTMLKithumanmasteryphone/fallbackfaceunknown. "
        "CompatibleAndroid#132 main2edbf366 plus#125 required; oldclientsignore. QualifiedsignedAndroid"
        "bf30cdead8515739bc0e671d57a54b9a3109dd46 approvedguard+schemaonlybridges NOTunrelatedlatestmain. "
        "Combined760377Python/version606c836e4be33ba9/8453runtimehashes/accepted+terminalCI+ZIP/"
        "ownerissueverified761; no newreviewnativehost761. Historical evidence/process/permission/OOM/"
        "source-only/pending limitations preserved, no retroacceptance. Physicalphone/generalrelease/"
        "whole-setoutstanding;projectincomplete. No101started/authoragents/concurrentheavywork/secondrunner/"
        "signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       pendingPublicationGateDisposition="Terminal CI/public ZIP/owner issue verified; bounded owner-testing delivery closed, not phone/general release.",
                       nextAction=next_action)
    save(C / "batch-100-publication-checkpoint.json", publication)
    save(L / "batch-100-publication-checkpoint.json", publication)
    before, state = load(L / "progress-before-761.json"), load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 761, "checkpoint": 761, "batch": "100",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8453,
        "contentVersion": VERSION, "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-100-published-verified-before-101",
        "publishedAdditions": 127, "remainingAdditions": 1101, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False}
    state["execution761CoordinatorCheckpoint"] = checkpoint
    state["batch100PublicationCheckpoint"] = publication
    state["batch100PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-100-publication-comment.txt"), "verified": True}
    state.update(checkpoint=761, status="continue", stage=checkpoint["stage"],
                 lastPublishedCommit=head, remainingAdditions=1101, blocker=None, nextAction=next_action)
    state["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    state["unmetAcceptanceGates"][0] = (
        "Remaining1101 issue60 source-bounded additions not review-closed/published; six separately placed "
        "earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. "
        "All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain.")
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= state.keys()
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    assert load(C / "progress.json")["checkpoint"] == 760
    save(C / "progress.json", state, replace=True)
    verified = load(C / "progress.json")
    assert verified == state
    assert all(verified[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-761.json", checkpoint)
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
