"""Publish the accepted batch 098; runner.lock remains owned by the launcher."""
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
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
L = C / "logs" / "e1f08e94-7602-4e44-aad4-001aff4173c5"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-098-publication-727"
HEAD = "7c71a8ccf1413972e0acc55ff1e969f06a354799"
MAIN = "69af99e5d7bf34b093959d90dddc7d59fe6393b5"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "0cbdc2723b0433f2"
MEMBER = "\u5264"
BEFORE = L / "progress-before-727.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(path.suffix + ".727.tmp")
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


def context(head=HEAD, clean=True):
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (15692, "running", L.name)
    script = f"""
$id={os.getpid()};$chain=@()
while($id -gt 0 -and $chain.Count -lt 12){{
 $p=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(!$p){{break}}
 $chain+=@{{pid=[int]$p.ProcessId;parent=[int]$p.ParentProcessId;name=$p.Name;command=$p.CommandLine}}
 if($id -eq 15692){{break}}
 $id=$p.ParentProcessId
}}
$chain|ConvertTo-Json -Depth 4 -Compress
"""
    chain = json.loads(output(["pwsh", "-NoProfile", "-NonInteractive", "-Command", script]))
    assert chain[-1]["pid"] == 15692
    assert any(p["name"].lower() == "copilot.exe" and L.name in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["batch"], state["status"]) == (726, "098", "continue")
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if clean or root == A:
            assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)
    return {
        "parentPid": 15692, "session": L.name, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
    }


def acceptance_helper():
    path = C / "accept-batch-098-combined-726.py"
    assert sha(path) == "ddbb07ffcfb73002c9c062c05b01df4bb7fcb1ad290bf58cd2e0fb4fd9fbdfe8"
    spec = importlib.util.spec_from_file_location("accepted726", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime():
    result = acceptance_helper().runtime()
    assert not git("diff", "233d3add2b90fcb98f9706b8901aa936fc6e56e7", "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return result


def start():
    role = context()
    assert git("rev-parse", "origin/main") == MAIN
    assert git("merge-base", MAIN, HEAD) == MAIN
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    state = load(C / "progress.json")
    assert checkpoint["execution726CoordinatorCheckpoint"] == state["execution726CoordinatorCheckpoint"]
    record = {
        "execution": 727, "batch": "098", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME098 owner publication, terminal CI/public ZIP/verified owner issue, then yield before099.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed. Operative contract, complete approved issue and final726 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers accessed.",
        "diagnostics": ["Initial progress display encountered Windows cp1252 UnicodeEncodeError only; explicit UTF-8/ASCII serialization used. No permission denial or source-byte change."],
    }
    save(L / "starting-state-727.json", record)
    state["execution727StartingState"] = record
    state.update(stage="batch-098-owner-publication-in-progress", nextAction=record["scope"], blocker=None)
    assert all(state[k] == v for k, v in load(BEFORE).items() if k not in {"stage", "nextAction", "blocker"})
    save(C / "progress.json", state)
    print("SAME098 starting state persisted; exact clean signed heads and live parent verified.")


def gate():
    context()
    accepted = load(S / "execution-726.json")
    assert accepted == load(V / "batch-098-combined-acceptance-726.json")
    assert accepted["runtimeAccepted"] and not accepted["runtimePublished"]
    assert accepted["reviewClosed"] == [MEMBER] and not accepted["published"]
    assert accepted["actionableRemainingFindings"] == accepted["consequentialUnresolvedInScopeClaims"] == 0
    checks = accepted["checks"]
    assert checks["pythonTests"] == 372 and checks["validatorErrors"] == 0 and checks["manifestFresh"]
    assert checks["androidTestsTotal"] == 4 and checks["androidSkipped"] == 0
    for row in checks["androidTests"]:
        suite = ET.parse(V / "batch-098-combined-acceptance-726" / Path(row["path"]).name).getroot()
        assert all(suite.attrib[k] == "0" for k in ("skipped", "failures", "errors"))
        assert len(suite.findall("testcase")) == int(suite.attrib["tests"])
    for row in accepted["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    inherited = acceptance_helper().inherited()
    assert inherited["native724EqualsCombinedManifest"]
    save(L / "prepublication-gate-727.json", {
        "execution": 727, "batch": "098", "acceptedSignedCheckpoint": HEAD,
        "runtime": runtime(), "acceptanceReceiptHashesReverified": len(accepted["receipts"]),
        "inheritedAcceptance": inherited, "freshReviewerNativeHostRuns": 0,
    })
    print("Combined receipts, original reviews/native acceptance and all8449 runtime hashes reverified.")


def verify(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-098-{phase}-ci.json"
    assert not ci_path.exists()
    runs = json.loads(output(["gh", "run", "list", "--repo", "stop-cran/learning-japanese",
        "--commit", head, "--workflow", "Validate content", "--limit", "5",
        "--json", "databaseId,status,conclusion,headSha"]))
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
    save(L / f"archive-download-{phase}-727.json",
         {"commit": head, "url": url, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    verifier = C / "verify-batch-002-publication.py"
    assert sha(verifier) == "8d07dcdb04eefa2bef9f1fb66f9a47e0f3711f9328eb15c9da13606ed8b42a6d"
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(verifier),
        head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def public(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-098-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8449 and archive["manifestEqual"]
    assert all(archive[k] for k in (
        "allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-098-publication.json").exists()
    accepted = load(S / "execution-726.json")
    counts = dict(accepted["sourceAudit"]["currentCounts"])
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (
        1121, 5073, 130, 135)
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=125, remainingAdditions=1103,
                  batchNewNecessarySupportWords=0, projectNewNecessarySupportWords=124,
                  batchChangedReusedArticles=2, allMappedReciprocalPairs=2, mappedDirectedLinks=4,
                  activatedBaselinePairs=1, separateExceptionPreserved="\u5996",
                  separateEarlierLevelSourceMembers=list("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50"),
                  earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    publication = {
        "schemaVersion": 1, "execution": 727, "batch": "098", "membership": [MEMBER],
        "status": "published-verified-bounded-owner-testing", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": MAIN, "authoredSnapshot": accepted["authoredTeachingSnapshot"],
        "reviewedSnapshot": accepted["reviewedSnapshot"], "combinedTestedSnapshot": accepted["combinedTestedSnapshot"],
        "latestMainIntegrated": MAIN, "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): load(BEFORE)[f"execution{n}CoordinatorCheckpoint"]["savedCommit"]
                      for n in range(718, 727)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-098-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-098-visual-reconciliation-725.json",
        "combinedAcceptanceRecord": "execution-726.json", "nativeRecord": "execution-724.json",
        "validation": accepted["sourceAudit"], "pythonTestsPassed": 372,
        "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2, "newReviewNativeHostRuns": 0,
        "ci": ci, "immutablePublicArchive": archive, "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP, "latestAppMainClaimed": False,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "limits": {"combined": accepted["limits"], "inherited": accepted["inheritedAcceptance"]["originalLimits"]},
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": "Verify terminal evidence CI/exact public ZIP/owner issue60; yield before099.",
    }
    save(S / "batch-098-publication.json", publication)
    ledger = load(S / "batch-098-progress.json")
    ledger["prePublication727State"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=125,
                  remainingAdditions=1103, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-098-publication.json", nextAction=publication["nextAction"],
                  pendingGates=["Terminal evidence CI/public ZIP/verified owner issue; physical-phone/general-release and whole-set outstanding."])
    save(S / "batch-098-progress.json", ledger)
    save(S / "execution-727.json", {
        "schemaVersion": 1, "execution": 727, "batch": "098", "status": publication["status"],
        "startingState": load(L / "starting-state-727.json"), "publicationRecord": "batch-098-publication.json",
        "acceptedCommit": HEAD, "runtimeBytesUnchanged": True, "runtimeAccepted": True,
        "runtimePublished": True, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "newReviewerNativeHostRuns": 0, "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    })
    D.mkdir()
    for path in [Path(__file__), C / "publish-727.ps1", C / "verify-batch-002-publication.py",
                 L / "starting-state-727.json", L / "prepublication-gate-727.json",
                 L / "archive-download-accepted-727.json", C / "artifacts" / "batch-098-accepted-ci.json",
                 C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json"]:
        shutil.copyfile(path, D / path.name)
    state = load(C / "progress.json")
    state["execution727AcceptedPublication"] = copy.deepcopy(publication)
    state.update(stage="batch-098-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    save(C / "progress.json", state)
    runtime()
    print("Accepted delivery verified; publication ledgers ready for signed terminal evidence.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-098-publication.json")
    body = f"""Batch **098 ({MEMBER})** is published and verified for bounded owner testing. No new support article: existing **洗剤 (せんざい)** retains its N2 identity, primary reading and original せっけん exclusion. Exact reused changes: 洗剤:28 and 洗:38. TWO all-mapped pairs/FOUR link directions/ONE activated baseline pair; no new word guard.

Authored `{publication['authoredSnapshot']}`; reviewed/combined-tested `{publication['combinedTestedSnapshot']}`. Original serial blind **claude-opus-5.5 / gpt-6.1-sol** textual reviews and dependent original-session725 rendered confirmations retained; no actionable defect or consequential unresolved in-scope claim. Each rendered reviewer25 serial views/23 PNGs: three four-font panels/all19Han,12contact sheets/45routes and8 additional route views. These are NOT48 original-resolution image inspections; resizing/read limits and unidentified exact fallback face remain.

Full metadata **ザイ/スイ/セイ;かる/けず.る** preserved in source order; explicit **[ザイ]/[]** offers only **ざい**, verified Good/Done1of1, no kun. Source-only alternatives are not silently dropped or given invented lexical examples. Actual N1 meaning choices **剤 vs 剛/冶/刑**: one curated/two fallback, not済/則. Bounded64kanji/128preserved-directguard records CLEAN; **unrestricted/future/custom semantics UNVERIFIED**, not whole-pool certification.

Fresh main `{MAIN}` remains an ancestor, zero incoming/runtime/teaching changes. Signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Normal stop-cran process-scoped fast-forwards; global romanko-ms unchanged. Combined726 **372 Python tests**, validator0errors, manifest, vocabulary consistency(**2122/2431 pilot**, not full coverage), frozen sources/fullbaseline/exactmembership/allreadings/pinnedstrokes/fonts/allmappedlinks/originalbudgets passed. Fresh726 **RealContentTest3+RareHanTest1**, no skips/failures/errors; these unchanged-tree checks inherited, NOT rerun727.

Native724 full archive through production **ContentSync ONCE**: **1121kanji/5073words/130N1,zeroProblems/acceptedRoomreadingEpoch1/version `{VERSION}`**, TWO terminalcase0/no skips. Exact manifest and all8449runtimehashes still match. N1 selection, meaning/reading/drawing, links/articles/SystemBack/offline and four-font evidence retained. TEN injected strokes/trace+give-up recall are NOT human handwriting/successfulMLKit/phone evidence. 刂/氵 visible; exactfallbackface unidentified. Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, NOT latestappmain. No new reviewer/native/host727. Original722 denial/approved recovery remains historical and unmodified.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. BOTH immutable publicZIPs preserve **all8449 runtime hashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB/perfile/media/safepath guards; contributor evidence excluded.

Published **125/1228additions;1103remain**. Collection **1121kanji/5073words/130N1labels/135named-source members plus separate妖**. Six separately placed source保/案/派/第/策/結 retain earlierN2levels, not issue60accepted additions; no duplication/relevel. Necessarysupportarticles124project-wide, NOT an N1 vocabulary deck.

Durable `docs/n1-sources/batch-098-publication.json`, `execution-727.json` and original textual/native724/rendered725/combined726 evidence. Historical pending flags preserved with scoped discharge. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; old clients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent15692 retainsrunner.lock: no childacquisition/deletion/unlock/readprobe; no optionalhistoricalsessionhelper or actualnewdenial. Checkpoint727 continues and yields before099; no nextbatch/secondrunner.
"""
    path = C / "batch-098-publication-comment.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-727.json",
         {"head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(path)})


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-098-publication-issue-receipt.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-098-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["id"] == remote["id"] and receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-099-progress.json").exists()
    ledger = load(S / "batch-098-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == [MEMBER]
    publication = load(S / "batch-098-publication.json")
    next_action = (
        f"Batch098 accepted/published/verified at {head}; yield before099. Next coordinator ONE bounded099 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent15692 retainsrunner.lock: no childacquire/delete/unlock/readprobe. "
        "Approvedcontrol/committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/"
        "report/yield actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/"
        "usefulness/baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/"
        "combinedmain/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries/"
        "42MiBcompressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published125/1228;1103acceptance-remainder;1121kanji5073words130N1labels135namedmembers+separate妖; "
        "124necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.098剤/no new support/exact reused洗剤:28and洗:38/"
        "authored233d3add/textualreview/native724/rendered725/combined726/publication727/"
        "version0cbdc2723b0433f2/8449runtimehashes;372Python/fresh726host4/inheritednative724two/"
        "accepted+terminalCI+ZIP/ownerissueverified. No newreview/native/host727. Exactnative724ContentSyncONCE/"
        "zeroProblems/epoch1/unchangedmanifest;64boundedkanji/128onepreservedwordguard CLEAN; "
        "widercustom/random/legacysemanticsUNVERIFIED,notwholepoolcertification. Fullrawザイスイセイ/"
        "かるけず.る/sourceorder/explicit[ザイ]/[];onlyざいGoodDone1of1/NOkun. "
        "TWOallmappedpairs/FOURdirections/ONEactivatedbaselinepair/NOnewwordguards/TENinjectedstrokes. "
        "Original725each25serialviews23PNG/threefourfontpanels19Han/12contactsheets45routes+8routeviews; "
        "48PNGs NOT48originalresolutionviews. Resizedimages/fallback刂氵visible/exactfaceunidentified/readlimits "
        "retained. InjectedtraceNOThumanhandwriting/no successfulMLKit/no exhaustivepoolsemantics. "
        "QualifiedTESTONLYAndroid1c1b7bf4 retainsproductionf9b59a2,NOTlatestappmain;compatiblef9b59a2+required. "
        "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. Original722denial and approved "
        "recovery preserved. No099started/authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextAction=next_action)
    save(C / "batch-098-publication-checkpoint.json", publication)
    save(L / "batch-098-publication-checkpoint.json", publication)
    before, state = load(BEFORE), load(C / "progress.json")
    state["execution727StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    checkpoint = {
        "schemaVersion": 1, "execution": 727, "checkpoint": 727, "batch": "098",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8449,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-098-published-verified-before-099",
        "publishedAdditions": 125, "remainingAdditions": 1103, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    state["execution727CoordinatorCheckpoint"] = checkpoint
    state["batch098PublicationCheckpoint"] = publication
    state["batch098PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-098-publication-comment.txt"), "verified": True}
    state.update(checkpoint=727, status="continue", stage=checkpoint["stage"],
                 lastPublishedCommit=head, remainingAdditions=1103, blocker=None, nextAction=next_action)
    state["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    state["unmetAcceptanceGates"][0] = (
        "Remaining1103 issue60 source-bounded additions not review-closed/published; six separately placed "
        "earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. "
        "All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain.")
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= state.keys()
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    save(L / "coordinator-checkpoint-727.json", checkpoint)
    save(C / "progress.json", state)
    assert load(C / "progress.json") == state
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
