import gzip
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual725", C / "review-batch-098-visual-725.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, L = review.R, review.A, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
STAGE = "batch-098-dependent-rendered-review-closed-awaiting-combined-acceptance"
NEXT = (
    "SAME098 bounded fresh-current-main integration and actual combined-tree acceptance next; no099. "
    "Read docs/n1-sources/execution-725.json and docs/n1-reviews/batch-098-visual-reconciliation-725.json. "
    "Original Claude d41cdccb THEN GPT33216339 dependent rendered confirmations CLOSED on unchanged "
    "teaching233d3add/evidence7e03dede. Actualclaude-opus-5.5 then gpt-6.1-sol; "
    "each25strictlyserialviewcalls/23decodedPNGviews/exit0/nooverlap/allassignedtextreturned/"
    "processactuallyexitedbeforenext. NOTnewblindcredit/independentupstream/equalcomprehension. "
    "Complete剤 and exact reused洗剤:28component/洗:38commonword changes retain inheritedtextual "
    "correctness/coverage and boundedrenderedcomprehensibility. Both full originalreports, "
    "actualresource/image/model/process evidence and optionaldispositions retained. "
    "THREEfourfontpanels/all19Han plus12mappedcontactsheets covering45routecaptures and8additional "
    "originalresolutionrouteviews perreviewer;48originalcaptures NOT48separatelyviewedoriginals. "
    "Toolresizes/exactduplicates retained. U+5202刂/U+6C35氵 visible and distinguishable; "
    "fallbackfaceunidentified/84Paintprobes NOT84viewedPNGs. Readingtable intentionally scrollable; "
    "complete剤 projected; top/firstexample reused洗剤 notcaptured/notnewlyrenderedapproved. "
    "ActualN1 options剤medicinalpreparationchemicalagent vs剛sturdy/冶smelt/刑criminalpunishment: "
    "ONEcuratedwrongcard剛/TWOfallbacks冶刑, NOT済N3/則N2. Both assessed64kanjibuilder samples/"
    "16seeds/N1+All+custom+randomN1subset/35distinctrecordedlabelspluspictured冶 and128preserved "
    "DIRECT洗剤せっけんwordguard questions/bothorientations/directions/All+custom: noalternate "
    "defensibleanswer established. SampledsemanticacceptanceCLEAN ONLYtestedconfigs; wider/future "
    "pools/薬overlap UNVERIFIED, notuniversalcertification. Onlyonざい/persistedGood/Done1of1/NOkun; "
    "rawザイスイセイandかるけず.る/sourceorder/explicit[ザイ]/[]retained/FullLiteagreement. "
    "TENpinnedstrokes/injectedtrace/recallgiveup/shapeonlymodelunavailable NOT humanhandwriting/"
    "MLKit/phone. TWOallmappedpairs剤洗剤AND洗洗剤/FOURdirections/ONEactivatedbaseline剤洗剤/"
    "SystemBack/offline/N1selection. Fresh721JVM4noskips and724nativeTWOterminalcase0noskips retained/"
    "no725rerun/fullarchivecefedeb6 productionContentSyncONCE/1121kanji5073words130N1zeroProblems/"
    "version0cbdc2723b0433f2/RoomreadingEpoch1/owned5580stopped. QualifiedTESTONLYAndroid1c1b7bf4 "
    "retains productionf9b59a2, NOTlatestappmain. Recheck freshmain/exactsignedheads/whollyclean/"
    "source-membership/fullbaselinepreservation/links/readings/guards/stroke-fontdispositions; "
    "normalnonrewritingoriginmainmerge/regeneratemanifestifchanged/independentreviewofchangedteaching. "
    "Required fullPython/vocabularyconsistency/manifestfreshness/budget/audits/applicablenonskipped "
    "Android on ACTUALcombinedtree before normallysignedreviewclosedacceptance. Then ownernormal "
    "fastforward/terminalgreenCI/EVERYimmutablepublicZIPentryhash/unchanged18000entries42MiBcompressed/"
    "80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue gates BEFORE099. "
    "Parent15692 retainsrunner.lock: verifyliveancestry/currentrunnersession/decodedlauncher/"
    "checkpoint/exactsignedheads/whollyclean; NOchildreacquire/delete/unlock/readprobe. "
    "Approvedcontrol/committedsources only, NOToptionalhistoricalsessionrecipes. Original722denial/"
    "approvedrecovery preserved. Preserve/report/yieldactualnewdenial/signinghang/uncertainownership. "
    "Published124/1228,1104remaining unchanged;098NOTdelivered. Physicalphone/generalrelease/whole-set "
    "outstanding. No099/runtimepublication/secondrunner."
)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for kind, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            path = R.joinpath(*name.split("/"))
            actual = sha(path) if kind in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"
            } else sha256(path)
            assert actual == digest, name
            count += 1
    assert count == 8449 and manifest["contentVersion"] == "0cbdc2723b0433f2"
    assert not git("diff", review.TEACHING, "HEAD", "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"runtimeHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True,
            "teachingAndAllRuntimeBytesUnchanged": True}


def exited(pid):
    subprocess.run(["pwsh", "-NoProfile", "-Command",
                    f"if(Get-Process -Id {pid} -ErrorAction SilentlyContinue){{exit 1}}"], check=True)


def archive():
    review.frozen()
    adjudication = load(C / "batch-098-visual-725-adjudication.json")
    assert adjudication["actionableRemainingFindings"] == 0
    assert adjudication["consequentialUnresolvedInScopeClaims"] == 0
    target = V / "batch-098-visual-reconciliation-725.json"
    assert not target.exists()
    records = {label: load(C / f"batch-098-visual-725-{label}-execution.json")
               for label in review.SESSIONS}
    for label, record in records.items():
        prefix = C / f"batch-098-visual-725-{label}"
        model, session = review.SESSIONS[label]
        assert record["actualModels"] == [model] and record["usageCurrentModel"] == model
        assert record["sessionId"] == session and record["exitCode"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert record["allAssignedResourcesSuccessfullyReturned"]
        assert record["exactlyOneViewPerToolBearingMessage"]
        assert len(record["toolCalls"]) == 25 and len(record["actualDecodedImageReturns"]) == 23
        assert all(call["name"] == "view" and call["success"] for call in record["toolCalls"])
        assert sha(prefix.with_suffix(".jsonl")) == record["rawSha256"]
        assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
        exited(record["launcherPid"])
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    assert all(a["returnedSha256"] == b["returnedSha256"] for a, b in zip(
        records["claude"]["actualDecodedImageReturns"], records["gpt"]["actualDecodedImageReturns"]))
    checked = runtime()
    receipts = []
    sources = [
        Path(__file__), C / "review-batch-098-visual-725.py", C / "preflight-725.ps1",
        review.PACKET, C / "batch-098-visual-725-inputs.json",
        C / "batch-098-visual-cli-help-725.txt", C / "batch-098-visual-cli-config-725.txt",
        C / "batch-098-visual-725-adjudication.json",
        C / "post-batch-098-visual-725.ps1", C / "batch-098-visual-725-issue-body.txt",
    ]
    for label in review.SESSIONS:
        prefix = C / f"batch-098-visual-725-{label}"
        sources.extend(prefix.with_suffix(suffix) for suffix in [
            ".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"])
        sources.append(C / (prefix.name + "-execution.json"))
        raw = prefix.with_suffix(".jsonl")
        archived = V / (raw.name + ".gz")
        assert not archived.exists()
        archived.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archived.read_bytes()) == raw.read_bytes()
        receipts.append({"source": str(raw), "archive": archived.relative_to(R).as_posix(),
                         "sourceSha256": sha(raw), "archiveSha256": sha(archived),
                         "losslessGzip": True})
    for source in sources:
        archived = V / source.name
        assert not archived.exists()
        shutil.copyfile(source, archived)
        assert sha(source) == sha(archived)
        receipts.append({"source": str(source), "archive": archived.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(archived)})
    groups = {}
    for image in load(C / "batch-098-visual-725-inputs.json")["images"]:
        groups.setdefault(image["sha256"], []).append(image["path"])
    reconciliation = {
        **adjudication, "status": STAGE,
        "evidenceSnapshot": review.HEAD, "teachingSnapshot": review.TEACHING,
        "originalInitialReviewsPreserved": True, "newBlindInitialReviewCredit": False,
        "processes": records, "serialReviewerProcessesExited": True,
        "eachOriginalReportPreservedBeforeNextLaunch": True,
        "eachReviewerImagesDecoded": 23, "eachReviewerViewCalls": 25,
        "allAssignedResourcesReturned": True, "allToolViewsSerial": True,
        "sameActualReturnedImageHashesAcrossReviewers": True,
        "distinctAssignedSourceImageHashes": len(groups),
        "exactDuplicateSourceGroups": [paths for paths in groups.values() if len(paths) > 1],
        "runtime": checked, "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "sampledLivePoolSemanticAcceptance": "CLEAN",
        "unrestrictedLivePoolSemanticAcceptance": "UNVERIFIED",
        "nextAction": NEXT,
    }
    save(target, reconciliation)
    save(R / "docs" / "n1-sources" / "execution-725.json", {
        "schemaVersion": 1, "execution": 725, "batch": "098", "status": STAGE,
        "startingState": load(C / "progress.json")["execution725StartingState"],
        "snapshot": review.HEAD, "teachingSnapshot": review.TEACHING,
        "runtime": checked, "reconciliation": target.relative_to(R).as_posix(),
        "receipts": receipts, "originalSessionReviewersLaunched": 2,
        "dependentRenderedConfirmation": "closed", "newBlindInitialReviewCredit": False,
        "sampledLivePoolSemanticAcceptance": "CLEAN",
        "unrestrictedLivePoolSemanticAcceptance": "UNVERIFIED",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 124, "remainingAdditions": 1104,
        "lastPublishedCommit": load(C / "progress.json")["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "rawEvidenceWhitespace": {
            "disposition": "Retain exact supplied packet including Git diff context spaces and exact CLI captures. Other authored evidence checked separately.",
            "paths": [
                "docs/n1-reviews/batch-098-visual-725-packet.txt",
                "docs/n1-reviews/batch-098-visual-cli-help-725.txt",
                "docs/n1-reviews/batch-098-visual-cli-config-725.txt",
            ],
        },
        "nextAction": NEXT,
    })
    print("Both complete dependent reports archived; 8449 unchanged runtime hashes verified.")


def finalize():
    review.ownership()
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == review.HEAD and git("log", "-1", "--format=%G?") == "G"
    for root, expected in ((R, saved), (A, review.ANDROID)):
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)
    changed = git("-c", "core.quotepath=false", "diff", "--name-only", review.HEAD, saved).splitlines()
    assert changed and all(name.startswith(("docs/n1-reviews/", "docs/n1-sources/")) for name in changed)
    receipt = load(C / "batch-098-visual-725-issue-receipt.json")
    body = (C / "batch-098-visual-725-issue-body.txt").read_bytes().decode("utf-8-sig")
    body += f"\nSigned LOCAL evidence checkpoint: {saved} (signature G). Not published.\n"
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    assert saved[:12] in body and "#60" in body
    checked = runtime()
    before = load(L / "progress-before-725.json")
    state = load(C / "progress.json")
    assert state["checkpoint"] == 724 and state["batch"] == "098"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 725, "checkpoint": 725,
        "batch": "098", "status": "continue", "stage": STAGE,
        "savedCommit": saved, "signature": "G", "evidence": "docs/n1-sources/execution-725.json",
        "dependentRenderedConfirmations": "closed", "originalReviewerProcessesExited": True,
        "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "eachReviewerViewCalls": 25, "eachReviewerDecodedImageViews": 23,
        "newBlindInitialReviewCredit": False, "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False,
        "runtimeHashesVerifiedAgain": checked["runtimeHashesVerified"],
        "sampledLivePoolSemanticAcceptance": "CLEAN",
        "unrestrictedLivePoolSemanticAcceptance": "UNVERIFIED",
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 124, "remainingAdditions": 1104,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    state["execution725CoordinatorCheckpoint"] = checkpoint
    state["batch098RenderedConfirmationCheckpoint"] = checkpoint
    state.update(checkpoint=725, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    temporary = C / "progress.725.tmp"
    assert not temporary.exists()
    save(temporary, state)
    assert load(temporary) == state
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    temporary.replace(C / "progress.json")
    save(L / "checkpoint-725-verification.json", checkpoint)
    print("Checkpoint725 persisted; full historical root comparison passed;", saved, receipt["html_url"])


if __name__ == "__main__":
    if sys.argv[1] == "archive":
        archive()
    elif sys.argv[1] == "finalize":
        finalize()
    else:
        raise ValueError(sys.argv[1])
