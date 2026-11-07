import copy
import gzip
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual673", C / "review-batch-093-visual-673.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
review = module.review
R, A, V, L = review.R, review.A, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
STAGE = "dependent-visual-review-closed-awaiting-combined-acceptance"
NEXT = (
    "SAME093 bounded fresh-current-main integration and actual combined-tree acceptance next; no094. "
    "Read docs/n1-sources/execution-673.json and docs/n1-reviews/batch-093-visual-reconciliation-673.json. "
    "Original Claude c8c0a762 then GPT feee7268 dependent visual confirmations CLOSED on unchanged "
    "teaching27663944/evidence66aea026. Actualclaude-opus-5.5 then gpt-6.1-sol; "
    "each34strictlyserialviewcalls/32decodedoriginalPNGviews, exit0/nooverlap/allassignedtextreturned/"
    "processactuallyexitedbeforenext. No newblindinitialcredit, independentupstreamclaim or "
    "equalcomprehensionclaim. Complete刑/reusedN3刑事 and added事:37 retain inheritedtextual "
    "correctness/coverage and boundedrenderedcomprehensibility; completeoriginalreports, optional "
    "dispositions and readlimits retained.32of63originalPNGsviewed/31notseparatelyviewed; actualtool "
    "image resizes and exactduplicates recorded. All46Han/FIVEComposepanels/FOURproductionfonts, "
    "especiallyfallback亅刂彡, readable;184individual+12wholewordPaintprobes NOT196viewedPNGs "
    "or identifiedfallbackface. Complementaryhorizontalscrolledreadingtable and allthreearticle "
    "projections rely on actualviews plus suppliedfulltext/native-scrollassertions. "
    "Onlyonけいoffered/persistedGood/1of1Done/NOkunkeys/fullLiteagreement, rawケイ/emptykun "
    "and explicit[ケイ]/[]retained; wholewordでか NOTconstituentkun, publicギョウoutsidefreeze. "
    "刑事N3identity/reading/title/level/inbound探偵guard preserved; componentlink/fourDIRECT "
    "policelabelguards only;事reciprocalnavigation only. TWOallmappedpairs/FOURdirections/"
    "ONEactivatedbaseline刑/刑事pair(NOT事/刑事); originalGPTaccountingcorrection remains. "
    "PicturedN1/suppliedAll choices criminalpunishment vs乃/凹/凸 all3available/zerofallback; "
    "broadercustompools/文/oldclients NOTuniversallycertified. Inherited672native TWOterminalcase0/"
    "noskips/fullarchive324b0bd9 productionContentSyncONCE/1116kanji5070words125N1zeroProblems/"
    "versionbf4cc85592bb9727/acceptedRoomreadingEpoch1. SIXpinnedstrokes/injectedtrace/recallgiveup "
    "NOThumanhandwriting/successfulMLKit/phone; actualUIexplicitlymodelunavailable/shapeonly. "
    "SystemBack/offline/N1selection/meaning/reading/drawing suppliednativeassertions retained. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. No fresh673 "
    "Android/nativeclaim; owned672helpersstopped. Recheck freshmain/exactsignedheads/whollyclean/"
    "source-membership/fullbaselinepreservation/links/readings/guards/stroke-fontdispositions; "
    "normalnonrewritingoriginmainmerge, regeneratederivedmanifestifchanged, independentlyrereview "
    "substantiveteachingchanges. Required fullPython/vocabularyconsistency/manifestfreshness/budget/"
    "audits/applicablenonskippedAndroid on ACTUALcombinedtree before normallysignedreviewclosed "
    "acceptance. Then normalownerfastforward/terminalgreenCI/EVERYimmutablepublicZIP runtimeentryhash/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/ownerissue "
    "gates. No publicationuntilprerequisitespass; no094/forcepush/amend/guardheapincrease/"
    "productionappchange. Parent19008 retainsrunner.lock: verifyliveancestry/currentrunnersession/"
    "decodedlauncher/checkpoint/exactsignedheads/whollyclean; NOchildreacquire/delete/unlock. "
    "Approvedcontrol/committedsources only, NOToptionalhistoricalsessionrecipes. Preserve/report/"
    "yieldactualnewdenial/signinghang/uncertainownership. Published119/1228,1109remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    verified = {}
    for kind, section in manifest.items():
        if isinstance(section, dict):
            for name, expected in section.items():
                if isinstance(expected, str) and len(expected) == 64:
                    path = R.joinpath(*name.split("/"))
                    actual = sha(path) if kind in {
                        "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                    } else sha256(path)
                    assert actual == expected, name
                    verified[name] = actual
    assert len(verified) == 8436
    assert manifest["contentVersion"] == "bf4cc85592bb9727"
    assert not git("diff", review.TEACHING, "HEAD", "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {
        "runtimeHashesVerified": len(verified), "contentVersion": manifest["contentVersion"],
        "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True,
        "teachingAndAllRuntimeBytesUnchanged": True,
    }


def archive():
    review.frozen()
    target = V / "batch-093-visual-reconciliation-673.json"
    assert not target.exists()
    adjudication = load(C / "batch-093-visual-673-adjudication.json")
    assert adjudication["actionableRemainingFindings"] == 0
    assert adjudication["consequentialUnresolvedInScopeClaims"] == 0
    records = {label: load(C / f"batch-093-visual-673-{label}-execution.json")
               for label in review.SESSIONS}
    message_audit = {}
    for label, record in records.items():
        prefix = C / f"batch-093-visual-673-{label}"
        model, session = review.SESSIONS[label]
        assert record["actualModels"] == [model] and record["usageCurrentModel"] == model
        assert record["sessionId"] == session and record["exitCode"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert record["allAssignedResourcesSuccessfullyReturned"]
        assert len(record["toolCalls"]) == 34
        assert all(item["name"] == "view" and item["success"] for item in record["toolCalls"])
        assert len(record["actualDecodedImageReturns"]) == 32
        assert sha(prefix.with_suffix(".jsonl")) == record["rawSha256"]
        assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
        events = [
            json.loads(line)
            for line in prefix.with_suffix(".jsonl").read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        counts = [
            len(event["data"]["toolRequests"])
            for event in events
            if event["type"] == "assistant.message" and event["data"].get("toolRequests")
        ]
        assert len(counts) == 34 and set(counts) == {1}
        message_audit[label] = {
            "toolBearingAssistantMessages": len(counts),
            "exactlyOneViewPerToolBearingMessage": True,
            "source": prefix.with_suffix(".jsonl").name,
        }
        assert review.absent(record["launcherPid"])
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    assert all(a["returnedSha256"] == b["returnedSha256"] for a, b in zip(
        records["claude"]["actualDecodedImageReturns"], records["gpt"]["actualDecodedImageReturns"]))
    checked = runtime()
    receipts = []
    sources = [
        Path(__file__), C / "review-batch-093-visual-673.py", review.PACKET,
        C / "batch-093-visual-673-inputs.json", C / "post-batch-093-visual-673.ps1",
        C / "batch-093-visual-cli-help-673.txt", C / "batch-093-visual-cli-config-673.txt",
        C / "batch-093-visual-673-adjudication.json", C / "batch-093-visual-673-issue-summary.txt",
    ]
    for label in review.SESSIONS:
        prefix = C / f"batch-093-visual-673-{label}"
        sources.extend(prefix.with_suffix(suffix) for suffix in [
            ".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"])
        sources.append(C / (prefix.name + "-execution.json"))
        raw = prefix.with_suffix(".jsonl")
        archived = V / (raw.name + ".gz")
        assert not archived.exists()
        archived.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archived.read_bytes()) == raw.read_bytes()
        receipts.append({
            "source": str(raw), "archive": archived.relative_to(R).as_posix(),
            "sourceSha256": sha(raw), "archiveSha256": sha(archived), "losslessGzip": True,
        })
    for source in sources:
        archived = V / source.name
        assert not archived.exists()
        shutil.copyfile(source, archived)
        assert sha(source) == sha(archived)
        receipts.append({
            "source": str(source), "archive": archived.relative_to(R).as_posix(),
            "sourceSha256": sha(source), "archiveSha256": sha(archived),
        })
    inputs = load(C / "batch-093-visual-673-inputs.json")
    groups = {}
    for image in inputs["images"]:
        groups.setdefault(image["sha256"], []).append(image["path"])
    reconciliation = {
        "schemaVersion": 1, "execution": 673, "batch": "093", "status": STAGE,
        "evidenceSnapshot": review.HEAD, "teachingSnapshot": review.TEACHING,
        "teachingChanged": False, "originalInitialReviewsPreserved": True,
        "newBlindInitialReviewCredit": False, "processes": records,
        "serialReviewerProcessesExited": True, "allToolViewsSerial": True,
        "assistantMessageToolGrouping": message_audit,
        "eachOriginalReportPreservedBeforeNextLaunch": True,
        "eachReviewerImagesDecoded": 32, "distinctSourceImageHashes": len(groups),
        "remainingUnassignedPngs": 31, "allAssignedResourcesReturned": True,
        "sameActualReturnedImageHashesAcrossReviewers": True,
        "exactDuplicateSourceGroups": [paths for paths in groups.values() if len(paths) > 1],
        "actualReturnedImageDimensions": sorted({
            tuple(item["returnedDimensions"])
            for record in records.values() for item in record["actualDecodedImageReturns"]
        }),
        "runtime": checked, "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "baseRecipe": {"path": module.BASE.relative_to(R).as_posix(), "sha256": sha(module.BASE)},
        "nextAction": NEXT,
        **adjudication,
    }
    save(target, reconciliation)
    save(R / "docs" / "n1-sources" / "execution-673.json", {
        "schemaVersion": 1, "execution": 673, "batch": "093", "status": STAGE,
        "startingState": load(C / "progress.json")["execution673StartingState"],
        "snapshot": review.HEAD, "teachingSnapshot": review.TEACHING,
        "runtime": checked, "reconciliation": target.relative_to(R).as_posix(), "receipts": receipts,
        "independentReviewersLaunched": 2, "dependentVisualConfirmation": "closed",
        "newBlindInitialReviewCredit": False, "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 119, "remainingAdditions": 1109,
        "lastPublishedCommit": load(C / "progress.json")["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "rawEvidenceWhitespace": {
            "disposition": "Retain exact supplied reviewer packet, including Git diff context lines containing a single space, and exact CLI catalog output including any emitted final blank line. Their archived hashes equal actual supplied/captured evidence. Check other generated evidence separately.",
            "paths": [
                "docs/n1-reviews/batch-093-visual-673-packet.txt",
                "docs/n1-reviews/batch-093-visual-cli-config-673.txt",
            ],
        },
    })
    print("Both complete reports and lossless raw events archived; 8436 unchanged runtime hashes verified.")


def finalize():
    review.ownership()
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == review.HEAD and git("log", "-1", "--format=%G?") == "G"
    for root, expected in [(R, saved), (A, review.ANDROID)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    changed = git("-c", "core.quotepath=false", "diff", "--name-only", review.HEAD, saved).splitlines()
    assert all(path.startswith("docs/n1-reviews/") or path == "docs/n1-sources/execution-673.json"
               for path in changed)
    checked = runtime()
    evidence = load(R / "docs" / "n1-sources" / "execution-673.json")
    for receipt in evidence["receipts"]:
        path = R.joinpath(*receipt["archive"].split("/"))
        assert sha(path) == receipt["archiveSha256"]
        if receipt.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == receipt["sourceSha256"]
    body = (C / "batch-093-visual-673-issue-body.txt").read_bytes().decode("utf-8-sig")
    posted, issue = [load(C / f"batch-093-visual-673-issue-{name}.json")
                     for name in ["posted", "receipt"]]
    assert posted["id"] == issue["id"] and posted["body"] == issue["body"] == body
    assert issue["user"]["login"] == "stop-cran"
    before = load(L / "progress-before-673.json")
    state = load(C / "progress.json")
    assert state["checkpoint"] == 672 and state["batch"] == "093"
    reconciliation = load(V / "batch-093-visual-reconciliation-673.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 673, "checkpoint": 673, "batch": "093",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-673.json",
        "reconciliation": "docs/n1-reviews/batch-093-visual-reconciliation-673.json",
        "reviewedTeachingSnapshot": review.TEACHING, "androidHead": review.ANDROID,
        "dependentVisualConfirmation": "closed", "independentReviewersLaunched": 2,
        "serialReviewerProcessesExited": True, "allToolViewsSerial": True,
        "eachReviewerDecodedImageViews": 32,
        "distinctSourceImageHashes": reconciliation["distinctSourceImageHashes"],
        "remainingUnassignedPngs": 31, "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "actionableRemainingFindings": 0, "runtime": checked,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "newBlindInitialReviewCredit": False,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 119, "remainingAdditions": 1109,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    assert "execution673CoordinatorCheckpoint" not in state
    state.update(checkpoint=673, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution673CoordinatorCheckpoint"] = checkpoint
    state["batch093VisualAcceptanceCheckpoint"] = copy.deepcopy(checkpoint)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    temp = C / "progress.673.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")
    save(L / "visual-673-final-verification.json", checkpoint)
    print(json.dumps({
        "checkpoint": 673, "savedCommit": saved, "issue": issue["html_url"],
        "historicalRootValuesPreserved": len(before), "status": "continue",
    }))


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
