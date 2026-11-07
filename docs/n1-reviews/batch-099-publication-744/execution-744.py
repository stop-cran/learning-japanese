"""Publish accepted batch 099 without touching the parent-owned runner lock."""
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
L = C / "logs" / "cf779820-280a-4e99-a787-a7395b8150af"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-099-publication-744"
HEAD = "93576e000175a2fcef04130ee6184769c4dd73f8"
MAIN = "2d3a3fa022d48aca6ea8a2ac629bd7ee66b85f9f"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
VERSION = "39eb4a86902c6dec"
MEMBER = "\u5270"
BEFORE = L / "progress-before-744.json"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data, replace=False):
    assert replace or not p.exists(), p
    temp = p.with_suffix(p.suffix + ".744.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    os.replace(temp, p)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def output(args, root=R):
    return subprocess.check_output(args, cwd=root, encoding="utf-8").strip()


def git(*args, root=R):
    return output(["git", "--no-pager", "-C", str(root), *args])


def context(head=HEAD, clean=True):
    assert not os.environ.get("GH_TOKEN")
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
    assert any(p["name"].lower() == "copilot.exe" and L.name in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["batch"], state["status"]) == (743, "099", "continue")
    for root, expected in ((R, head), (A, APP)):
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if clean or root == A:
            assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    return {
        "parentPid": 5920, "session": L.name, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
    }


def helper():
    p = C / "accept-batch-099-combined-743.py"
    assert sha(p) == "8bb69c9b6deb3eca6c8f52afcd0acad94cbb77f40fb061e3ddb32ee08ea16c86"
    spec = importlib.util.spec_from_file_location("accepted743", p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime():
    result = helper().runtime()
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return result


def start():
    role = context()
    assert git("rev-parse", "origin/main") == MAIN
    assert git("merge-base", MAIN, HEAD) == MAIN
    state = load(C / "progress.json")
    assert state == load(L / "checkpoint-full.json")
    save(BEFORE, state)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    a, b = embedded["execution743CoordinatorCheckpoint"], state["execution743CoordinatorCheckpoint"]
    assert a.keys() == b.keys()
    assert all(v == b[k] for k, v in a.items() if k != "recordedAt")
    assert datetime.fromisoformat(a["recordedAt"]) == datetime.fromisoformat(b["recordedAt"])
    record = {
        "execution": 744, "batch": "099", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME099 owner publication, exact remote/terminal CI/public ZIP/verified owner issue and durable checkpoint; yield before100.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and embedded checkpoint parsed; operative contract, entire approved issue and final743 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session recipes accessed.",
        "diagnostics": ["Initial request display hit cp1252 UnicodeEncodeError after successful complete decode/parse; ASCII/UTF-8 serialization used thereafter."],
    }
    save(L / "starting-state-744.json", record)
    after = copy.deepcopy(state)
    after["execution744StartingState"] = record
    after.update(stage="batch-099-owner-publication-in-progress", nextAction=record["scope"], blocker=None)
    assert all(after[k] == v for k, v in state.items() if k not in {"stage", "nextAction", "blocker"})
    assert load(C / "progress.json") == state
    save(C / "progress.json", after, replace=True)
    print("SAME099 publication started; signed clean heads and live launcher verified; full history preserved.", flush=True)


def gate():
    context()
    accepted = load(S / "execution-743.json")
    assert accepted == load(V / "batch-099-combined-acceptance-743.json")
    assert accepted["runtimeAccepted"] and not accepted["runtimePublished"]
    assert accepted["reviewClosed"] == [MEMBER] and not accepted["published"]
    assert accepted["actionableRemainingFindings"] == accepted["consequentialUnresolvedInScopeClaims"] == 0
    assert accepted["checks"]["pythonTests"] == 377
    assert accepted["checks"]["validatorErrors"] == 0 and accepted["checks"]["manifestFresh"]
    for row in accepted["receipts"]:
        p = R / row["archive"]
        assert sha(p) == row["archiveSha256"]
        raw = gzip.decompress(p.read_bytes()) if row.get("losslessGzip") else p.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    inherited = helper().inherit()
    assert inherited["hostTests"] == 6 and inherited["nativeTerminalCaseSuccesses"] == 2
    save(L / "prepublication-gate-744.json", {
        "execution": 744, "acceptedSignedCheckpoint": HEAD, "runtime": runtime(),
        "acceptanceReceiptHashesReverified": len(accepted["receipts"]),
        "inheritedAcceptance": inherited, "freshReviewerNativeHostRuns": 0,
    })
    print("Combined/source/review/host/native receipts and all8451 runtime hashes verified.", flush=True)


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
    save(L / f"{phase}-ci-744.json", ci)
    p = C / "artifacts" / f"content-{head[:7]}.zip"
    assert not p.exists()
    url = f"https://codeload.github.com/stop-cran/learning-japanese/legacy.zip/{head}"
    result = subprocess.run(["curl.exe", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "180", url, "--output", str(p)], capture_output=True, text=True)
    save(L / f"archive-download-{phase}-744.json", {
        "commit": head, "url": url, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    verifier = C / "verify-batch-002-publication.py"
    assert sha(verifier) == "8d07dcdb04eefa2bef9f1fb66f9a47e0f3711f9328eb15c9da13606ed8b42a6d"
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(verifier), head, str(p),
                    str(L / f"{phase}-archive-744.json")], check=True)
    public(phase, head)


def public(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci, archive = load(L / f"{phase}-ci-744.json"), load(L / f"{phase}-archive-744.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8451 and archive["manifestEqual"]
    assert all(archive[k] for k in ("allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    sys.path.insert(0, str(R / "tools"))
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def records():
    ci, archive = public("accepted", HEAD)
    accepted = load(S / "execution-743.json")
    counts = dict(accepted["sourceAudit"]["currentCounts"])
    assert (counts["kanji"], counts["words"], counts["n1Labels"]) == (1122, 5073, 131)
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=126, remainingAdditions=1102,
                  batchNewNecessarySupportWords=0, projectNewNecessarySupportWords=124,
                  batchChangedReusedArticles=2, allMappedReciprocalPairs=2,
                  mappedDirectedLinks=4, activatedBaselinePairs=1)
    publication = {
        "schemaVersion": 1, "execution": 744, "batch": "099", "membership": [MEMBER],
        "status": "published-verified-bounded-compatible-client-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": accepted["sourceAudit"]["baseCommit"],
        "authoredSnapshot": accepted["authoredTeachingSnapshot"], "reviewedSnapshot": accepted["reviewedSnapshot"],
        "combinedTestedSnapshot": accepted["combinedTestedSnapshot"], "latestMainIntegrated": MAIN,
        "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-099-reconciliation.json",
        "dependentGuardRenderedRecord": "../n1-reviews/batch-099-guard-742-reconciliation.json",
        "combinedAcceptanceRecord": "execution-743.json", "nativeRecord": "execution-741.json",
        "validation": accepted["sourceAudit"], "pythonTestsPassed": 377,
        "hostTestsReverified": 6, "nativeTerminalCasesReverified": 2, "newReviewNativeHostRuns": 0,
        "ci": ci, "immutablePublicArchive": archive, "counts": counts, "contentVersion": VERSION,
        "qualifiedAndroidHead": APP,
        "compatibleClient": "Approved Android #132/main2edbf366 guard plus #125 curated readings required. Old clients ignore these metadata fields; not universal synonym detection.",
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "limits": accepted["limits"], "original733734Retroaccepted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": "Verify terminal evidence CI/public ZIP/owner issue; checkpoint and yield before100.",
    }
    save(S / "batch-099-publication.json", publication)
    ledger = load(S / "batch-099-progress.json")
    ledger["prePublication744State"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=126,
                  remainingAdditions=1102, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-099-publication.json", nextAction=publication["nextAction"],
                  pendingGates=["Terminal evidence CI/public ZIP/verified owner issue; physical-phone/general-release and whole-set outstanding."])
    save(S / "batch-099-progress.json", ledger, replace=True)
    save(S / "execution-744.json", {
        "schemaVersion": 1, "execution": 744, "batch": "099", "status": publication["status"],
        "startingState": load(L / "starting-state-744.json"), "publicationRecord": "batch-099-publication.json",
        "acceptedCommit": HEAD, "runtimeBytesUnchanged": True, "runtimeAccepted": True,
        "runtimePublished": True, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "newReviewerNativeHostRuns": 0, "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "original733734Retroaccepted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    })
    assert not D.exists()
    D.mkdir()
    for p in (Path(__file__), C / "publish-744.ps1", C / "verify-batch-002-publication.py",
              L / "starting-state-744.json", L / "prepublication-gate-744.json",
              L / "archive-download-accepted-744.json", L / "accepted-ci-744.json",
              L / "accepted-archive-744.json"):
        shutil.copyfile(p, D / p.name)
    state = load(C / "progress.json")
    state["execution744AcceptedPublication"] = copy.deepcopy(publication)
    state.update(stage="batch-099-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    save(C / "progress.json", state, replace=True)
    runtime()
    print("Accepted delivery verified; publication ledgers ready for signed terminal evidence.", flush=True)


def comment(head):
    ci, archive = public("terminal", head)
    p = load(S / "batch-099-publication.json")
    body = f"""Batch **099 ({MEMBER})** is published and verified for bounded compatible-client owner testing. No new support article: existing **過剰 (かじょう)** retains its N2 identity, title, primary reading and seven original exclusions. TWO all-mapped pairs/FOUR link directions/ONE activated baseline pair; reused teaching changes limited to 過剰:25 and 過:41.

Authored `{p['authoredSnapshot']}`; reviewed `{p['reviewedSnapshot']}`; combined-tested `{p['combinedTestedSnapshot']}`. Original serial blind **claude-opus-5.5 / gpt-6.1-sol** reviews and necessary original-session742 dependent guard/rendered confirmations retained. Each742 reviewer: actual exit0,14 successful tool calls, zero overlaps; two original font panels plus10contact sheets/39thumbnails, NOT41 full-resolution route reads. No consequential in-scope defect remains. Original733/734 evidence, Claude's false serial claim/nine overlaps/max9 active tools and original packet byte-comparisonfalse are preserved, NOT retroaccepted. Supplementary742 audit: all2784 substantive lines exact/in order, blank-line normalization only.

Full metadata **ジョウ; あまつさえ/あま.り/あま.る** preserved in source order. Explicit **[ジョウ]/[]** offers only **じょう**, no kun. Recognition/search-only/dated spelling qualifications remain; no invented 剰る collocation. Supported **quiz_exclusions:[冗]** preserves the evidenced surplus/redundancy overlap without distorting titles. This is a direct symmetric nontransitive guard, NOT universal synonym detection/exhaustive pool certification. **stop-cran/kanji-cards-android#132** (published main `2edbf366a4a6fce594b2a6580bfc4252b98d3f6d`) plus curated-reading **stop-cran/kanji-cards-android#125** is required; old clients ignore both fields. Qualified Android `{APP}` carries approved guard and schema-only bridges, NOT unrelated latest-app behavior.

Fresh main `{MAIN}` remains an ancestor; ZERO incoming/runtime/teaching changes. Signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Normal stop-cran process-scoped fast-forwards; global romanko-ms unchanged. Combined743 **377 Python tests**, validator0errors, manifest, vocabulary consistency(**2122/2431 pilot**, not complete coverage), frozen sources/fullbaseline/exactmembership/allreadings/pinnedstrokes/fonts/allmappedlinks/originalbudgets passed. HOST740 six non-skipped cases and native741 TWO terminalcase0 inherited and reverified, NOT rerun744. Native production **ContentSync ONCE**: **1122kanji/5073words/131N1,zeroProblems,both accepted parser epochs1**, version `{VERSION}`; **224kanjiguard checks/64actual surplus choices/896preservedwordguards**, with pool membership/order. Curated reading, eleven injected reference strokes, N1 selection/meaning/drawing/articles/links/SystemBack/offline/four-font checks retained. Injection/give-up is NOT human handwriting/successfulMLKit/phone evidence; actual fallback font face unidentified and unsampled/custom pools remain unverified.

Accepted CI [{p['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{p['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. BOTH immutable publicZIPs preserve **all8451 runtime hashes** and manifest. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB/perfile/media/safepath guards; contributor evidence excluded.

Published **126/1228additions;1102remain**. Collection **1122kanji/5073words/131N1labels/{p['counts']['namedSourceMembersPresent']}named-source members plus separate妖**. Six separately placed source保/案/派/第/策/結 retain earlierN2levels, not issue60accepted additions; no duplication/relevel. Necessarysupportarticles124project-wide, NOT an N1 vocabulary deck.

Durable `docs/n1-sources/batch-099-publication.json`, `execution-744.json` and original source/textual/HOST740/native741/rendered742/combined743 records. Historical pending flags preserved with scoped discharge. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent5920 retainsrunner.lock: no childacquisition/deletion/unlock/readprobe; no optional historicalsessionhelper or actualnewdenial. Checkpoint744 continues and yields before100; no nextbatch/secondrunner.
"""
    pth = C / "batch-099-publication-comment.txt"
    assert not pth.exists()
    pth.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-744.json",
         {"head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(pth)})


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(L / "issue-744-reread.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-099-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["id"] == remote["id"] and receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-100-progress.json").exists()
    ledger = load(S / "batch-099-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == [MEMBER]
    publication = load(S / "batch-099-publication.json")
    next_action = (
        f"Batch099 accepted/published/verified at {head}; yield before100. Next coordinator ONE bounded100 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent5920 retainsrunner.lock: no childacquire/delete/unlock/readprobe. "
        "Approvedcontrol/committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/"
        "report/yield actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/"
        "usefulness/baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/"
        "combinedmain/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries/"
        "42MiBcompressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published126/1228;1102acceptance-remainder;1122kanji5073words131N1labels136namedmembers+separate妖; "
        "124necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.099剰/no new support/exact reused過剰:25and過:41/"
        "authored70dfe334/originaltextualreview/HOST740/native741/dependentguardrendered742/combined743/"
        "publication744/version39eb4a86902c6dec/8451runtimehashes;377Python/HOST6/native2/"
        "accepted+terminalCI+ZIP/ownerissueverified. No newreview/native/host744. Exactnative741ContentSyncONCE/"
        "zeroProblems/bothacceptedepochs1/unchangedmanifest;224kanjiguards/64surpluschoices/"
        "896preservedwordguards/capturedpoolmembershiporder. Fullrawジョウ/あまつさえあま.りあま.る/"
        "sourceorder/explicit[ジョウ]/[];onlyじょう/NOkun. TWOallmappedpairs/FOURdirections/ONEactivatedbaselinepair/"
        "sevenpreservedwordguards/ELEVENinjectedstrokes. Supportedquiz_exclusions:[冗] direct symmetricnontransitive "
        "guard; compatibleAndroid#132 main2edbf366 plus#125 required; oldclientsignore. QualifiedsignedAndroid"
        "bf30cdead8515739bc0e671d57a54b9a3109dd46 approvedguard+schemaonlybridges,NOTunrelatedlatestappmain. "
        "Original742each14serialcalls/zerooverlaps/actualexits/twooriginalfontpanels12Han+10sheets39thumbnails, "
        "NOT41originalresolutionreads; no newblindcredit. Original733734/falseserialclaim/nineoverlaps/max9/"
        "strictpacketbytecomparisonfalse preservedNOTretroaccepted;2784nonblanklinesexactinorder. "
        "Actualfallbackfaceunknown/injectedtraceNOThumanhandwriting/no successfulMLKit/no exhaustivepoolsemantics. "
        "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No100started/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextAction=next_action)
    save(C / "batch-099-publication-checkpoint.json", publication)
    save(L / "batch-099-publication-checkpoint.json", publication)
    before, state = load(BEFORE), load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 744, "checkpoint": 744, "batch": "099",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8451,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-099-published-verified-before-100",
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    state["execution744CoordinatorCheckpoint"] = checkpoint
    state["batch099PublicationCheckpoint"] = publication
    state["batch099PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-099-publication-comment.txt"), "verified": True}
    state.update(checkpoint=744, status="continue", stage=checkpoint["stage"],
                 lastPublishedCommit=head, remainingAdditions=1102, blocker=None, nextAction=next_action)
    state["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    state["unmetAcceptanceGates"][0] = (
        "Remaining1102 issue60 source-bounded additions not review-closed/published; six separately placed "
        "earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. "
        "All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain.")
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= state.keys()
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    assert load(C / "progress.json")["checkpoint"] == 743
    save(C / "progress.json", state, replace=True)
    verified = load(C / "progress.json")
    assert verified == state
    assert all(verified[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-744.json", checkpoint)
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
