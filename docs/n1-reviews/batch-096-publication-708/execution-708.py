"""Publish the already accepted batch 096; preserve the parent launcher lock."""
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
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "81f6cfe2-6ac2-4955-93d7-c0a9deec5dc6"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-096-publication-708"
HEAD = "831e4f3a9f827e3a4be49119943617dfc04a1f17"
MAIN = "4c2416e4c5925e6910b32215412bb1b795f60524"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
VERSION = "54645b95fe8e939c"
MEMBER = "\u525b"
BEFORE = L / "progress-before-708.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(path.suffix + ".708.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (707, "096", "continue")
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


def acceptance_helper():
    path = C / "accept-batch-096-combined-707.py"
    assert sha(path) == "eb92f4f4d65820418b34a491b9e4e868aa37dbbd4fe517fe31f273efc9ba9965"
    spec = importlib.util.spec_from_file_location("accepted707", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime():
    result = acceptance_helper().runtime()
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", "b26bcf9b328872b1575cf89e187973fea0a32a31", HEAD,
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
    assert checkpoint["execution707CoordinatorCheckpoint"] == p["execution707CoordinatorCheckpoint"]
    state = {
        "execution": 708, "batch": "096", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME096 owner fast-forward publication, terminal CI/public ZIP/verified owner issue, then yield before097.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed. Operative contract, complete approved issue and final707 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "runtime": runtime(), "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers accessed.",
    }
    save(L / "starting-state-708.json", state)
    p["execution708StartingState"] = state
    p.update(stage="batch-096-owner-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    assert all(p[k] == v for k, v in load(BEFORE).items() if k not in {"stage", "nextAction", "blocker"})
    print("SAME096 publication starting state persisted; exact clean signed heads and live parent verified.")


def gate():
    context(HEAD)
    current = runtime()
    accepted = load(S / "execution-707.json")
    assert accepted == load(V / "batch-096-combined-acceptance-707.json")
    assert accepted["runtimeAccepted"] and not accepted["runtimePublished"]
    assert accepted["reviewClosed"] == [MEMBER] and accepted["published"] == []
    assert accepted["actionableRemainingFindings"] == accepted["consequentialUnresolvedInScopeClaims"] == 0
    assert accepted["checks"]["pythonTests"] == 372
    assert accepted["checks"]["validatorErrors"] == 0 and accepted["checks"]["manifestFresh"]
    assert accepted["checks"]["androidTestsTotal"] == 4 and accepted["checks"]["androidSkipped"] == 0
    for row in accepted["checks"]["androidTests"]:
        suite = ET.parse(V / "batch-096-combined-acceptance-707" / Path(row["path"]).name).getroot()
        assert all(suite.attrib[k] == "0" for k in ("skipped", "failures", "errors"))
        assert len(suite.findall("testcase")) == int(suite.attrib["tests"])
    receipts = 0
    for row in accepted["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
        receipts += 1
    inherited = acceptance_helper().inherited()
    assert inherited["native705EqualsCombinedManifest"]
    result = {"execution": 708, "batch": "096", "acceptedSignedCheckpoint": HEAD,
              "acceptedRecord": "docs/n1-sources/execution-707.json",
              "runtime": current, "acceptanceReceiptHashesReverified": receipts,
              "inheritedAcceptance": inherited, "freshReviewerNativeHostRuns": 0}
    save(L / "prepublication-gate-708.json", result)
    print(f"All acceptance gates reverified; {receipts} combined receipts and 8444 runtime hashes.")


def verify(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-096-{phase}-ci.json"
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
    save(L / f"archive-download-{phase}-708.json",
         {"commit": head, "url": url, "exitCode": result.returncode,
          "stdout": result.stdout, "stderr": result.stderr})
    result.check_returncode()
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
        head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def public(phase, head):
    context(head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-096-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8444 and archive["manifestEqual"]
    assert all(archive[k] for k in (
        "allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-096-publication.json").exists()
    accepted = load(S / "execution-707.json")
    counts = dict(accepted["sourceAudit"]["currentCounts"])
    assert (counts["kanji"], counts["words"], counts["n1Labels"], counts["namedSourceMembersPresent"]) == (
        1119, 5072, 128, 133)
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=123, remainingAdditions=1105,
                  batchNewNecessarySupportWords=1, projectNewNecessarySupportWords=123,
                  batchChangedReusedArticles=0, allMappedReciprocalPairs=1, mappedDirectedLinks=2,
                  activatedBaselinePairs=0, separateExceptionPreserved="\u5996",
                  separateEarlierLevelSourceMembers=list("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50"),
                  earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    publication = {
        "schemaVersion": 1, "execution": 708, "batch": "096", "membership": [MEMBER],
        "status": "published-verified-bounded-owner-testing", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "baseCommit": MAIN, "authoredSnapshot": accepted["authoredTeachingSnapshot"],
        "initialReviewedTeachingSnapshot": accepted["authoredTeachingSnapshot"],
        "reviewedSnapshot": accepted["reviewedSnapshot"],
        "combinedTestedSnapshot": accepted["combinedTestedSnapshot"],
        "latestMainIntegrated": MAIN, "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): load(BEFORE)[f"execution{n}CoordinatorCheckpoint"]["savedCommit"]
                      for n in range(700, 708)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-096-reconciliation.json",
        "renderedRecord": "../n1-reviews/batch-096-rendered-reconciliation-706.json",
        "combinedAcceptanceRecord": "execution-707.json", "nativeRecord": "execution-705.json",
        "validation": accepted["sourceAudit"], "pythonTestsPassed": 372,
        "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2, "newReviewNativeHostRuns": 0,
        "ci": ci, "immutablePublicArchive": archive, "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP, "latestAppMainClaimed": False,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "limits": {"combined": accepted["limits"], "inherited": accepted["inheritedAcceptance"]["originalLimits"]},
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": "Verify terminal evidence CI/exact public ZIP/owner issue60; yield before097.",
    }
    save(S / "batch-096-publication.json", publication)
    ledger = load(S / "batch-096-progress.json")
    ledger["prePublication708State"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=[MEMBER], publishedAdditions=123,
                  remainingAdditions=1105, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-096-publication.json", nextAction=publication["nextAction"],
                  pendingGates=["Terminal evidence CI/public ZIP/verified owner issue; physical-phone/general-release and whole-set outstanding."])
    save(S / "batch-096-progress.json", ledger)
    save(S / "execution-708.json", {
        "schemaVersion": 1, "execution": 708, "batch": "096", "status": publication["status"],
        "startingState": load(L / "starting-state-708.json"), "publicationRecord": "batch-096-publication.json",
        "acceptedCommit": HEAD, "runtimeBytesUnchanged": True, "runtimeAccepted": True,
        "runtimePublished": True, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "newReviewerNativeHostRuns": 0, "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    })
    D.mkdir()
    for path in [Path(__file__), C / "publish-708.ps1", C / "verify-batch-002-publication.py",
                 L / "starting-state-708.json", L / "prepublication-gate-708.json",
                 L / "archive-download-accepted-708.json",
                 C / "artifacts" / "batch-096-accepted-ci.json",
                 C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json"]:
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["execution708AcceptedPublication"] = copy.deepcopy(publication)
    p.update(stage="batch-096-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    save(C / "progress.json", p)
    runtime()
    print("Accepted delivery verified; source/publication ledgers ready for signed terminal evidence.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-096-publication.json")
    body = f"""Batch **096 ({MEMBER})** is published and verified for bounded owner testing, with ONE necessary new support **剛健 (ごうけん)**, no inferred vocabulary level and no changed reused articles. ONE all-mapped reciprocal pair/TWO directions/ZERO activated baseline pairs; all12 direct word guards retained. Existing identities, primary readings, easier levels, titles and exclusions preserved.

Authored/initial reviewed `{publication['authoredSnapshot']}`; reviewed/combined-tested `{publication['combinedTestedSnapshot']}`. Original702 serial independent **claude-opus-5.5 / gpt-6.1-sol** initials and own-session supplements cover102 distinct complete families; initial missing final-label packet corrected by explicit supplements, not relabelled blind coverage. Original706 dependent rendered confirmations retained, NOT new blind credit. Each36serialviews/22complete textchunks+14decodedPNG, no overlap/unfinished/missingread. Fourfontpanels/all28Han+tencontactsheets/all37other captures inspected; reduced/resized images and exact fallback-face limitations preserved. No actionable defect or consequential unresolved in-scope claim.

Freshmain `{MAIN}` was already an ancestor; ZERO incoming teaching/runtime changes, no merge/conflict/review/native rerun required. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Normal owner-scoped fast-forwards, global romanko-ms unchanged. Combined707 **372Python tests**, validator0errors, vocabulary consistency(**2122/2431 pilot**, NOT fullcoverage), regenerated manifest, frozen sources/fullbaseline/exactmembership/allreadings/pinnedstrokes/fonts/allmappedlinks/all8444runtimehashes/originalbudgets passed. Fresh707 **3RealContentTest+1RareHanTest** passed without skips/failures/errors; unchanged-tree checks inherited, NOT rerun708.

Full sole **[ゴウ]/[]** retained in source order; explicit curated **[ゴウ]/[]** yields only **ごう**, no kunyomi. Supplemental コウ, native descriptive glosses and names not inserted into frozen metadata or called invalid. Modern-shape mnemonic not historical etymology. 剛健 supports robust body/spirit; masculine association is not a male-only subject/grammar restriction.

Native705 exact fullarchive through production **ContentSync ONCE**: **1119kanji/5072words/128N1,zeroProblems/acceptedRoomreadingEpoch1/version `{VERSION}`**, two terminalcase0/no skips. N1 selection, meaning/onlyonごう/noKunGood+Done, ONEpair/TWOdirections/article/SystemBack/offline/teninjectedstrokes and fourfontpanels retained. Unchanged current manifest/every8444runtimehash matches native705; no changed-manifest import claim. Actual defaultN1剛 vs剖/削/儒 is TWOcurated+ONEfallback, not allthreecurated. Bounded **64kanji** choices/**1536twelve-directwordguard** records CLEAN; **untested seeds/pools/all-other-word-option semantics UNVERIFIED**, not universal quiz safety.

Qualified TESTONLY Android `{APP}` preserves productionf9b59a2, NOT latestappmain. Emulator/injectedtraces/recallgiveup are **NOT physicalphone/humanhandwriting/successfulMLKit evidence**. All source/read/phone/native/rendered limitations retained. No new reviewer/native/host708.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both immutable publicZIPs preserve **all8444runtimehashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB/perfile/media/safepath guards, contributor evidence excluded.

Published **123/1228additions;1105remain**. Collection **1119kanji/5072words/128N1labels/133named-source members plus separate妖**. Six separately placed source保/案/派/第/策/結 retain earlierN2levels, not issue60accepted additions; no duplication/relevel. Necessarysupportarticles123project-wide, **NOT an N1vocabularydeck**.

Durable `docs/n1-sources/batch-096-publication.json`, `execution-708.json` and original702/705/706/707 evidence. Historical pending flags preserved with scoped discharge, not erased. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; oldclients ignore curation. **Physicalphone/generalrelease/whole-set acceptance outstanding; project incomplete**. Parent19008 retainsrunner.lock: no childacquisition/deletion/unlock/readprobe; no optionalhistoricalsessionhelper or actualnewdenial. Checkpoint708 continues and yields before097; no nextbatch/secondrunner.
"""
    path = C / "batch-096-publication-comment.txt"
    assert not path.exists()
    path.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-708.json",
         {"head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(path)})


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-096-publication-issue-receipt.json")
    remote = json.loads(output(["gh", "api",
        f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"]))
    body = (C / "batch-096-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["id"] == remote["id"] and receipt["body"] == remote["body"] == body
    assert output(["gh", "api", "user", "--jq", ".login"]) == "romanko-ms"
    assert not (S / "batch-097-progress.json").exists()
    ledger = load(S / "batch-096-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == [MEMBER]
    publication = load(S / "batch-096-publication.json")
    next_action = (
        f"Batch096 accepted/published/verified at {head}; yield before097. Next coordinator ONE bounded097 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "decodedlauncher/exactsession. Parent19008 retainsrunner.lock: no childacquire/delete/unlock/readprobe. "
        "Approvedcontrol/committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/"
        "report/yield actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/"
        "usefulness/baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/non-skippedAndroid/native/"
        "combinedmain/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchanged18000entries/"
        "42MiBcompressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published123/1228;1105acceptance-remainder;1119kanji5072words128N1labels133namedmembers+separate妖; "
        "123necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.096剛/necessary剛健/initialb26bcf9b/"
        "textual702/native705/rendered706/combined707/publication708/version54645b95fe8e939c/8444runtimehashes; "
        "372Python/fresh707host4/inheritednative705two/accepted+terminalCI+ZIP/ownerissueverified. No newreview/native/"
        "host708. Exactnative705ContentSyncONCE1119kanji5072words128N1/zeroProblems/epoch1/unchangedmanifest; "
        "64boundedkanji/1536twelvewordguards CLEAN; untestedseeds/pools/allotherwordoptionsemanticsUNVERIFIED. "
        "Fullrawゴウ/[]/sourceorder/curation[ゴウ]/[];onlyごう/noKunGood+Done. Supplementalコウ/glosses/names "
        "notinvalid/notnewfrozenmetadata. ONEallmappedpair/TWOdirections/ZEROactivatedbaselinepairs/nochangedreuse. "
        "Fourfontpanels/all28Han/tencontactsheets/all37othercaptures/native705routes/rendered706inherited; "
        "contactsheetreductions/toolresizes/fallbackface/readlimits retained. DefaultN1剖削儒two curated onefallback. "
        "Original702initialmissingfinal-labelpacket completedbybothown-sessionsupplements;NOTfreshblindcredit. "
        "InjectedtraceNOThumanhandwriting/no successfulMLKit/no exhaustivepoolsemantics. QualifiedTESTONLY"
        "Android1c1b7bf4 retainsproductionf9b59a2,NOTlatestappmain;compatiblef9b59a2+required. "
        "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No097started/authoragents/"
        "concurrentheavywork/secondrunner/signingretry/guardincrease.")
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextAction=next_action)
    save(C / "batch-096-publication-checkpoint.json", publication)
    save(L / "batch-096-publication-checkpoint.json", publication)
    before, p = load(BEFORE), load(C / "progress.json")
    p["execution708StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 708, "checkpoint": 708, "batch": "096",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8444,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-096-published-verified-before-097",
        "publishedAdditions": 123, "remainingAdditions": 1105, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution708CoordinatorCheckpoint"] = verification
    p["batch096PublicationCheckpoint"] = publication
    p["batch096PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-096-publication-comment.txt"), "verified": True}
    p.update(checkpoint=708, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1105, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = (
        "Remaining1105 issue60 source-bounded additions not review-closed/published; six separately placed "
        "earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. "
        "All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain.")
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "coordinator-checkpoint-708.json", verification)
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
