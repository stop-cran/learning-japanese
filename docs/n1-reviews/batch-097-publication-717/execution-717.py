"""Publish accepted batch 097 without touching the parent-owned runner lock."""
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
L = C / "logs" / "8c0dff4a-cc00-4534-b947-79f1591f52f3"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-097-publication-717"
HEAD = "80df466127028d7081f40bee164fb7ac18a9cc58"
MAIN = "1b00a924a007f32da36894ea92b05f675436e60d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "a066afceaf1f447a"
MEMBER = "\u5263"
BEFORE = L / "progress-before-717.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(path.suffix + ".717.tmp")
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


def context(head, clean=True):
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
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (716, "097", "continue")
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if clean or root == A:
            assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)
    return {
        "parentPid": 19008, "session": L.name, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
    }


def accepted_helper():
    path = C / "accept-batch-097-combined-716.py"
    assert sha(path) == "d086a578aebd9a623fdbac1114f01d5481a6b278ea074ce9dc71e2388c73ad5e"
    spec = importlib.util.spec_from_file_location("accepted716", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime():
    result = accepted_helper().runtime()
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", "1fa1ac69b88383ef424c0a69d34020ccca83c313", HEAD,
                   "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return result


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
    assert checkpoint["execution716CoordinatorCheckpoint"] == p["execution716CoordinatorCheckpoint"]
    state = {
        "execution": 717, "batch": "097", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME097 owner fast-forward publication, terminal CI/public ZIP/verified owner issue, then yield before098.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed. Operative contract, complete approved issue and final716 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers accessed.",
        "diagnostics": ["Two initial display probes hit Windows console/default-file cp1252 decoding; corrected with explicit UTF-8. No permission denial or source-byte change."],
    }
    save(L / "starting-state-717.json", state)
    p["execution717StartingState"] = state
    p.update(stage="batch-097-owner-publication-in-progress", nextAction=state["scope"], blocker=None)
    assert all(p[k] == v for k, v in load(BEFORE).items() if k not in {"stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    print("SAME097 publication starting state persisted; exact clean signed heads and live parent verified.")


def gate():
    context(HEAD)
    current = runtime()
    accepted = load(S / "execution-716.json")
    assert accepted == load(V / "batch-097-combined-acceptance-716.json")
    assert accepted["runtimeAccepted"] and not accepted["runtimePublished"]
    assert accepted["reviewClosed"] == [MEMBER] and accepted["published"] == []
    assert accepted["actionableRemainingFindings"] == accepted["consequentialUnresolvedInScopeClaims"] == 0
    assert accepted["checks"]["pythonTests"] == 372
    assert accepted["checks"]["validatorErrors"] == 0 and accepted["checks"]["manifestFresh"]
    assert accepted["checks"]["androidTestsTotal"] == 4 and accepted["checks"]["androidSkipped"] == 0
    for row in accepted["checks"]["androidTests"]:
        suite = ET.parse(V / "batch-097-combined-acceptance-716" / Path(row["path"]).name).getroot()
        assert all(suite.attrib[k] == "0" for k in ("skipped", "failures", "errors"))
        assert len(suite.findall("testcase")) == int(suite.attrib["tests"])
    for row in accepted["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    inherited = accepted_helper().inherited()
    assert inherited["native714EqualsCombinedManifest"]
    result = {"execution": 717, "batch": "097", "acceptedSignedCheckpoint": HEAD,
              "acceptedRecord": "docs/n1-sources/execution-716.json", "runtime": current,
              "acceptanceReceiptHashesReverified": len(accepted["receipts"]),
              "inheritedAcceptance": inherited, "freshReviewerNativeHostRuns": 0}
    save(L / "prepublication-gate-717.json", result)
    print(f"Acceptance gates reverified; {len(accepted['receipts'])} combined receipts and 8447 runtime hashes.")


def verify(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-097-{phase}-ci.json"
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
    save(L / f"archive-download-{phase}-717.json",
         {"commit": head, "url": url, "exitCode": result.returncode,
          "stdout": result.stdout, "stderr": result.stderr})
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
    ci = load(C / "artifacts" / f"batch-097-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8447 and archive["manifestEqual"]
    assert all(archive[k] for k in (
        "allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-097-publication.json").exists()
    accepted = load(S / "execution-716.json")
    counts = dict(accepted["sourceAudit"]["currentCounts"])
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (
        1120, 5073, 129, 134)
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=124, remainingAdditions=1104,
                  batchNewNecessarySupportWords=1, projectNewNecessarySupportWords=124,
                  batchChangedReusedArticles=2, allMappedReciprocalPairs=3, mappedDirectedLinks=6,
                  activatedBaselinePairs=1, separateExceptionPreserved="\u5996",
                  separateEarlierLevelSourceMembers=list("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50"),
                  earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    publication = {
        "schemaVersion": 1, "execution": 717, "batch": "097", "membership": [MEMBER],
        "status": "published-verified-bounded-owner-testing", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": MAIN, "authoredSnapshot": accepted["authoredTeachingSnapshot"],
        "reviewedSnapshot": accepted["reviewedSnapshot"], "combinedTestedSnapshot": accepted["combinedTestedSnapshot"],
        "latestMainIntegrated": MAIN, "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): load(BEFORE)[f"execution{n}CoordinatorCheckpoint"]["savedCommit"]
                      for n in range(709, 717)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-097-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-097-rendered/execution-715/reconciliation.json",
        "combinedAcceptanceRecord": "execution-716.json", "nativeRecord": "execution-714.json",
        "validation": accepted["sourceAudit"], "pythonTestsPassed": 372,
        "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2, "newReviewNativeHostRuns": 0,
        "ci": ci, "immutablePublicArchive": archive, "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP, "latestAppMainClaimed": False,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "limits": {"combined": accepted["limits"], "inherited": accepted["inheritedAcceptance"]["originalLimits"]},
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": "Verify terminal evidence CI/exact public ZIP/owner issue60; yield before098.",
    }
    save(S / "batch-097-publication.json", publication)
    ledger = load(S / "batch-097-progress.json")
    ledger["prePublication717State"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=124,
                  remainingAdditions=1104, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-097-publication.json", nextAction=publication["nextAction"],
                  pendingGates=["Terminal evidence CI/public ZIP/verified owner issue; physical-phone/general-release and whole-set outstanding."])
    save(S / "batch-097-progress.json", ledger)
    save(S / "execution-717.json", {
        "schemaVersion": 1, "execution": 717, "batch": "097", "status": publication["status"],
        "startingState": load(L / "starting-state-717.json"), "publicationRecord": "batch-097-publication.json",
        "acceptedCommit": HEAD, "runtimeBytesUnchanged": True, "runtimeAccepted": True,
        "runtimePublished": True, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "newReviewerNativeHostRuns": 0, "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    })
    D.mkdir()
    for path in [Path(__file__), C / "publish-717.ps1", C / "verify-batch-002-publication.py",
                 L / "starting-state-717.json", L / "prepublication-gate-717.json",
                 L / "archive-download-accepted-717.json", C / "artifacts" / "batch-097-accepted-ci.json",
                 C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json"]:
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["execution717AcceptedPublication"] = copy.deepcopy(publication)
    p.update(stage="batch-097-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    save(C / "progress.json", p)
    runtime()
    print("Accepted delivery verified; source/publication ledgers ready for signed terminal evidence.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-097-publication.json")
    body = f"""Batch **097 ({MEMBER})** is published and verified for bounded owner testing, with ONE necessary new support **剣 (つるぎ)**, no inferred vocabulary level, and TWO navigation-only reused changes (**真剣 / 真**). THREE all-mapped pairs/SIX directions/ONE activated baseline pair/FOUR direct word guards retained. Stable identities, full metadata/readings, easier levels and original exclusions preserved.

Authored `{publication['authoredSnapshot']}`; reviewed/combined-tested `{publication['combinedTestedSnapshot']}`. Original711 serial blind **claude-opus-5.5 / gpt-6.1-sol** initials covered the same137-family packet and exact reused diffs, independently. Original715 dependent rendered confirmations accepted: **36 turns/34 serial single-resource views/32 images/zero overlaps**. Original Claude29-overlap attempt preserved and NOT accepted. Resized images and exact fallback-face limitations retained. No actionable defect or consequential unresolved in-scope claim.

Freshmain `{MAIN}` already ancestor: ZERO incoming teaching/runtime changes. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Normal stop-cran process-scoped fast-forwards; global romanko-ms unchanged. Combined716 **372 Python tests**, validator0errors, vocabulary consistency(**2122/2431 pilot**, NOT fullcoverage), manifest, frozen sources/fullbaseline/exactmembership/allreadings/pinnedstrokes/fonts/allmappedlinks/all8447runtimehashes/originalbudgets passed. Fresh716 **3RealContentTest+1RareHanTest** passed without skips/failures/errors; unchanged-tree evidence inherited, NOT rerun717.

Full source **[ケン]/[つるぎ]** retained in order and explicitly selected; both **けん/つるぎ Good+Done** verified. Useful真剣しんけん support retains N3 and originalまじめ guard. Standaloneけん recognized without transferring its restricted senses toつるぎ. Sword especially double-edged, not an absolute taxonomy; modern-shape mnemonic not historical etymology. Canonical刀18 retained, visible刂 explained.

Native714 exact fullarchive through production **ContentSync ONCE**: **1120kanji/5073words/129N1,zeroProblems/acceptedRoomreadingEpoch1/version `{VERSION}`**, BOTH terminalcase0/no skips. N1 selection, meaning/reading/drawing, THREEpairs/SIXdirections/article/SystemBack/offline/teninjectedstrokes and fourfontpanels retained. Unchanged manifest/every8447runtimehash matches native714; no changed-manifest import claim. Bounded **64kanji** choices/**512four-directwordguard** records CLEAN; **wider custom/random/legacy semantics UNVERIFIED**, not universal quiz safety.

Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, NOT latestappmain. Emulator/injectedtraces/recallgiveup are **NOT physicalphone/humanhandwriting/successfulMLKit evidence**. 刂 visible; exact fallbackface unidentified. No new reviewer/native/host717. All historical source/read/native/rendered limitations retained.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both immutable publicZIPs preserve **all8447runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB/perfile/media/safepath guards, contributor evidence excluded.

Published **124/1228additions;1104remain**. Collection **1120kanji/5073words/129N1labels/134named-source members plus separate妖**. Six separately placed source保/案/派/第/策/結 retain earlierN2levels, not issue60accepted additions; no duplication/relevel. Necessarysupportarticles124project-wide, **NOT an N1vocabularydeck**.

Durable `docs/n1-sources/batch-097-publication.json`, `execution-717.json` and original711/714/715/716 evidence. Historical pending flags preserved with scoped discharge. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock: no childacquisition/deletion/unlock/readprobe; no optionalhistoricalsessionhelper or actualnewdenial. Checkpoint717 continues and yields before098; no nextbatch/secondrunner.
"""
    path = C / "batch-097-publication-comment.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-717.json",
         {"head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(path)})


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-097-publication-issue-receipt.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-097-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["id"] == remote["id"] and receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-098-progress.json").exists()
    ledger = load(S / "batch-097-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == [MEMBER]
    publication = load(S / "batch-097-publication.json")
    next_action = (
        f"Batch097 accepted/published/verified at {head}; yield before098. Next coordinator ONE bounded098 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent19008 retainsrunner.lock: no childacquire/delete/unlock/readprobe. "
        "Approvedcontrol/committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/"
        "report/yield actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/"
        "usefulness/baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/"
        "combinedmain/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries/"
        "42MiBcompressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published124/1228;1104acceptance-remainder;1120kanji5073words129N1labels134namedmembers+separate妖; "
        "124necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.097剣/necessary剣つるぎ/two navigation-only "
        "reused真剣and真/initial1fa1ac69/textual711/native714/rendered715/combined716/publication717/"
        "versiona066afceaf1f447a/8447runtimehashes;372Python/fresh716host4/inheritednative714two/"
        "accepted+terminalCI+ZIP/ownerissueverified. No newreview/native/host717. Exactnative714ContentSyncONCE"
        "1120kanji5073words129N1/zeroProblems/epoch1/unchangedmanifest;64boundedkanji/512fourwordguards CLEAN; "
        "widercustom/random/legacysemanticsUNVERIFIED,notwholepoolcertification. Fullrawケン/つるぎ/"
        "sourceorder/explicitcuration/bothけんつるぎGoodDone;けん-onlysensesnottransferredtoつるぎ. "
        "THREEallmappedpairs/SIXdirections/ONEactivatedbaselinepair/FOURwordguards/TENinjectedstrokes. "
        "Original715resourcegated36turns34views32imageszerooverlaps accepted; initialClaude29overlap "
        "attempt NOT accepted. Resizedimages/fallback刂visible/exactfaceunidentified/readlimits retained. "
        "InjectedtraceNOThumanhandwriting/no successfulMLKit/no exhaustivepoolsemantics. QualifiedTESTONLY"
        "Android1c1b7bf4 retainsproductionf9b59a2,NOTlatestappmain;compatiblef9b59a2+required. "
        "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No098started/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextAction=next_action)
    save(C / "batch-097-publication-checkpoint.json", publication)
    save(L / "batch-097-publication-checkpoint.json", publication)
    before, p = load(BEFORE), load(C / "progress.json")
    p["execution717StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 717, "checkpoint": 717, "batch": "097",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8447,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-097-published-verified-before-098",
        "publishedAdditions": 124, "remainingAdditions": 1104, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution717CoordinatorCheckpoint"] = verification
    p["batch097PublicationCheckpoint"] = publication
    p["batch097PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-097-publication-comment.txt"), "verified": True}
    p.update(checkpoint=717, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1104, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = (
        "Remaining1104 issue60 source-bounded additions not review-closed/published; six separately placed "
        "earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. "
        "All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain.")
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "coordinator-checkpoint-717.json", verification)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({k: v for k, v in verification.items() if k != "nextAction"}, indent=2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "start":
        start()
    elif mode == "gate":
        gate()
    elif mode == "context":
        context(sys.argv[2])
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
