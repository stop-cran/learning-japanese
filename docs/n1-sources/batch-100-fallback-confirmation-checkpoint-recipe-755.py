"""Preserve original-session fallback confirmations and the next bounded checkpoint."""
import copy
import gzip
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("fallback_confirmation", C / "confirm-batch-100-755.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
HEAD, APP, MAIN = review.HEAD, review.review.APP, review.review.MAIN
load, sha, git, now, save = review.load, review.sha, review.git, review.now, review.save
NEXT = (
    "SAME100 checkpoint755 original-session fallback exact-diff confirmations COMPLETE on signed8a55290e; "
    "read docs/n1-sources/execution-755.json and docs/n1-reviews/batch-100-fallback-confirmation-755-reconciliation.json. "
    "Claude4975f494/claude-opus-5.5 then GPTc9e3c7f4/gpt-6.1-sol exited0, one full155372byte/4510line view each, "
    "zero internal overlaps. N753-fallback-establish RESOLVED semantically: both confirmed new創/樹 directguard "
    "and all23sampledlabel decisions from ten full families/23rawrecords/64projectedchoice rows. "
    "NOT changed-manifest enforcement/native/rendered acceptance; no fresh blind-review credit or185/137family reread. "
    "Original750 findings/history preserved. New754 source decision locations off by1 are qualified in755 "
    "reconciliation; original754 evidence unchanged. NEXT bounded fresh HOST3+1 ONLY at qualified signedAndroid"
    "bf30cdead8515739bc0e671d57a54b9a3109dd46: RealContentTest3+RareHanTest1, require fresh XML4tests0failures/"
    "errors/skips against THIS signed content runtime606c836e4be33ba9, then signed local evidence checkpoint/yield. "
    "Verified JDK17/SDK paths, one worker/no parallel/quoted inprocessKotlin/unchanged2gHOST; no heavywork overlap. "
    "Then prepare actual full git archive/new named productionContentSyncONCE fixture/APKs for changed payload; "
    "old752/753 archive/APKs/native2case0 historical only. All8453runtimehashes, exact manifest/version, "
    "full archive/path/media/budget guards mandatory. Native11directpairs bothorientations/NONTRANSITIVE"
    "neighborchecks/preservedwordguards/actualN1-All-custom builderpoolchoices, N1 TWOcurated剣倹 plus fallback "
    "because験N4; no fallbackmask/relevel/universalrandomsafety claim. Selectedソウ/つく.る persistedgood/done, "
    "12drawingstrokes/trace/recall, fiveallmappedpairs/tendirections/oneactivatedbaselinepair/threeexactreused"
    "changes/article/reference/systemBack/offline;21Han(allmetadata incl樹)/fourproductionfontfamilies and actual"
    "PNG semantic/readability acceptance with SERIAL original-family rendered confirmations remain. Require "
    "both namedterminalcase0/no skips; fresh owneddevice/ports(includingremoteTimeWait)/PID/readonlyAVD/"
    "fingerprint/192m before launch, stop only owned helper. Cmap presence not readability; absence not glyphfailure/"
    "fallbackfaceproof. Sixfullreadings/order preserved; sourceonlyショウ/けず.しける allocationUNVERIFIED/unselected. "
    "Conservative創/初 not provenhistoricallivefailure/universalsynonym. No legacy樹/設/初 edits; eleven guards "
    "direct/symmetric/NONTRANSITIVE, no neighborclique. Reused創作N2/作るN5 metadata and13/5wordguards unchanged. "
    "All currentmainnonrewritingintegration/changedteachingreview/actualcombinedchecks/normalsigning/"
    "ownerfastforward/exactremoteSHA/terminalgreenCI/EVERYimmutableZIPmanifesthash/18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia/verifiedownerissue gates remain. "
    "No unreviewedpush/101/authoragent/concurrentheavywork/secondrunner/signingretry/guardincrease. "
    "Verify whollyclean exactsignedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. "
    "Parent5920 ownsrunner.lock: no childacquire/delete/unlock/readprobe. Approvedcontrol/committedsource/"
    "frozeninputs only, not optionalhistoricalsessionrecipes; preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Published126/1228,1102acceptanceremainder,lastpublished716c6101 unchanged; "
    "sixearlierN2placements保案派第策結 remain separate, neverduplicate/relevel. "
    "Physicalphone/generalrelease/whole-set outstanding; batch NOTreviewclosed/published/projectincomplete."
)


def new(path, value):
    assert not path.exists(), path
    save(path, value)


def archive(source, destination):
    assert not destination.exists(), destination
    raw = source.read_bytes()
    destination.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(destination.read_bytes()) == raw
    return {"archive": destination.name, "rawBytes": len(raw), "rawSha256": sha(source),
            "archiveSha256": sha(destination), "lossless": True}


def record():
    review.frozen(whole=True)
    confirmations = {}
    storage = []
    for label, model in review.review.MODELS.items():
        prefix = f"batch-100-confirmation-755-{label}"
        record = load(C / (prefix + "-execution.json"))
        assert record["snapshot"] == HEAD
        assert record["actualModels"] == [model] and record["usageCurrentModel"] == model
        assert record["sessionId"] == review.review.SESSIONS[label]
        assert record["exitCode"] == 0 and record["reviewerProcessExitVerified"]
        assert review.absent(record["launcherPid"])
        assert record["allAssignedRangesReturned"] and not record["observedToolOverlaps"]
        assert not record["unfinishedTools"] and record["multiToolResponseCount"] == 0
        assert len(record["toolCalls"]) == 1 and record["availableTools"] == ["view"]
        call = record["toolCalls"][0]
        assert call["success"] and call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
        for suffix in [".md", "-execution.json", "-stderr.txt", "-prompt.txt", "-usage.json"]:
            destination = V / (prefix + suffix)
            assert not destination.exists()
            shutil.copyfile(C / (prefix + suffix), destination)
        storage.append(archive(C / (prefix + ".jsonl"), V / (prefix + ".jsonl.gz")))
        confirmations[label] = {k: record[k] for k in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
            "snapshot", "reportSha256", "rawExecutionSha256", "allAssignedRangesReturned"]}
        confirmations[label].update(
            report=prefix + ".md", execution=prefix + "-execution.json",
            rawExecution=prefix + ".jsonl.gz", internalToolCalls=1, observedToolOverlaps=0,
            processExitVerified=True, fullPacketReturned=True)
    assert confirmations["claude"]["completedAt"] < confirmations["gpt"]["startedAt"]
    storage.append(archive(review.PACKET, V / "batch-100-confirmation-755-packet.txt.gz"))
    for kind in ["help", "config-help"]:
        storage.append(archive(L / f"copilot-{kind}-755.txt", V / f"batch-100-cli-{kind}-execution-755.txt.gz"))
    new(V / "batch-100-confirmation-755-lossless-storage.json", storage)
    for source, target in [
        (L / "confirmation-755-provenance.json", V / "batch-100-confirmation-755-provenance.json"),
        (L / "preflight-755.json", V / "batch-100-confirmation-755-runner-role.json"),
        (C / "confirm-batch-100-755.py", S / "batch-100-fallback-confirmation-recipe-755.py"),
        (C / "checkpoint-755.py", S / "batch-100-fallback-confirmation-checkpoint-recipe-755.py"),
        (C / "preflight-755.ps1", V / "batch-100-fallback-confirmation-preflight-755.ps1.txt"),
        (C / "post-batch-100-confirmation-755.ps1", V / "batch-100-fallback-confirmation-issue-recipe-755.ps1.txt"),
    ]:
        assert not target.exists()
        shutil.copyfile(source, target)
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    payloads = {name: value for entries in manifest.values() if isinstance(entries, dict)
                for name, value in entries.items()}
    assert len(payloads) == 8453 and manifest["contentVersion"] == "606c836e4be33ba9"
    assert (R / "manifest.json").read_bytes() == subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", f"{HEAD}:manifest.json"])
    reconciliation = {
        "schemaVersion": 1, "execution": 755, "batch": "100", "snapshot": HEAD,
        "beforeCorrection": review.BEFORE,
        "finding": "N753-fallback-establish", "status": "resolved",
        "statusScope": "Semantic source/diff correction resolved; enforcement/native/rendered acceptance pending, not full batch closure.",
        "severityBeforeCorrection": "Major", "facet": "correctness/quiz ambiguity",
        "locations": ["kanji/創.md:14", "kanji/創.md:36", "kanji/創.md:50", "kanji/樹.md:3", "kanji/樹.md:22"],
        "evidence": "Actual753defaultN1 and seed10 establish option; full1330410樹立 and1398640創立 establishment/founding,1307550 establishment spelling scope and full raw創/樹 meanings. Both original model families independently confirmed exact branch overlap from same bounded follow-up evidence.",
        "remedy": "Only append樹 to new創 metadata; eleven direct symmetric NONTRANSITIVE pairs, no inferred neighbors or legacy edit. No removal of meanings, releveling or fallback masking.",
        "confidence": "High for semantic overlap; new-payload runtime enforcement UNVERIFIED.",
        "confirmations": confirmations,
        "verdicts": {
            unit: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
            for unit in ["kanji/創.md", "words/創作.md:30", "words/作る.md:36", "kanji/作.md:45"]
        },
        "guardSemantics": "CLEAN", "changedManifestEnforcement": "UNVERIFIED",
        "sampledLabels": 23, "projectedChoiceRows": 64, "completeSupplementFamilies": 10,
        "completeRawCharacterRecords": 23, "bothReviewersAgreeNoOtherActionableSampledAmbiguity": True,
        "limits": [
            "Original-session dependent confirmation, not new blind review or fresh185/137family semantic reread. Exact returned bytes establish access, not equal comprehension or native-speaker certification.",
            "Route is coordinator key projection: scalars/default options/all64choice rows, no repeated pool memberships or5984 mechanical guard-check records. Full original gzip and its SHA retained.",
            "No new upstream lookup, Git/hash verification by reviewers, actual image pixels or runtime execution. Sample safety is not all-pairs/future random-pool safety.",
            "Both reviewers' statement about symmetric effect refers to the approved mechanism, not independently tested changed-manifest enforcement.",
            "Source-onlyショウ/けず.しける remains explicitlyUNVERIFIED/unselected; full readings/order and selectedソウ/つく.る unchanged.",
        ],
        "optional": {
            "documentationLineReferences": "Claude noted off-by-one locations in immutable754decisions. Exclusion is創14 not15; establishment is創36/50 not35/49; 樹立 is樹22 not21. Correct locations recorded here; original historical evidence preserved.",
            "previousO1ToO4": "Remain optional; no teaching edit required or made.",
        },
        "inheritedDispositions": {"F1": "resolved", "C1-establish": "resolved", "H1-initial": "resolved as conservative safeguard, not proven historical live failure", "H1-wound": "withdrawn"},
        "preparationDiagnostics": [
            "Initial checkpoint comparison stopped on equivalent recordedAt offsets(+01:00/+00:00); explicit datetime comparison confirmed same instant, every other754field equal. Live historical values never rewritten.",
            "Unlaunched first packet included full9MB route. Preserved original packet gzip/prompts/provenance under control; no reviewer launched on it. Revised packet155372bytes/4510lines projects actual scalar/options evidence, all64rows retained. Neither original native evidence nor guard assertions changed.",
        ],
        "runtimeChangedThisExecution": False, "manifestChangedThisExecution": False,
        "runtimeHashesVerified": 8453, "contentVersion": manifest["contentVersion"],
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "independentRenderedReviewClosed": False, "runtimeAccepted": False,
        "reviewClosed": [], "published": [], "nextAction": NEXT,
    }
    new(V / "batch-100-fallback-confirmation-755-reconciliation.json", reconciliation)
    old = load(V / "batch-100-reconciliation.json")
    assert "fallbackConfirmation755" not in old
    old["fallbackConfirmation755"] = reconciliation
    save(V / "batch-100-reconciliation.json", old)
    ledger = load(S / "batch-100-progress.json")
    assert ledger["reviewClosed"] == ledger["published"] == []
    ledger["statusBefore755"] = ledger["status"]
    ledger.update(
        status="fallback-textual-confirmations-complete-awaiting-fresh-android",
        textualAcceptanceComplete=True, runtimeChangedThisExecution=False,
        fallbackConfirmation755="docs/n1-reviews/batch-100-fallback-confirmation-755-reconciliation.json",
        nextAction=NEXT)
    ledger["limitsBefore755"] = ledger["limits"]
    ledger["limits"] = list(ledger["limits"])
    ledger["limits"][0] = "Original750 and fallback755 original-family textual confirmations complete on identified snapshots. Batch NOT review-closed. Fresh changed-tree HOST/native/font/rendered and publication pending."
    ledger["limits"][5] = "Five all-mapped pairs/ten directions/one activated baseline pair, three exact reused changes. Eleven direct symmetric nontransitive guards textually confirmed, changed-tree live-pool acceptance pending."
    save(S / "batch-100-progress.json", ledger)
    new(S / "execution-755.json", {
        "schemaVersion": 1, "execution": 755, "batch": "100",
        "stage": "fallback-textual-confirmations-complete-awaiting-fresh-android",
        "startingState": load(C / "progress.json")["execution755StartingState"],
        "snapshot": HEAD, "qualifiedAndroidHead": APP, "freshOriginMain": MAIN,
        "confirmations": confirmations,
        "reconciliation": "docs/n1-reviews/batch-100-fallback-confirmation-755-reconciliation.json",
        "finding": "N753-fallback-establish", "findingStatus": "resolved semantically; enforcement pending",
        "runtimeHashesVerified": 8453, "contentVersion": manifest["contentVersion"],
        "runtimeChanged": False, "manifestChanged": False,
        "inheritedChecks754": "52focusedPython/validator/manifest/budget/vocabulary/baseline/link audits retained, not newly executed for docs-only confirmation evidence.",
        "freshAndroidOrNativeClaimed": False, "independentRenderedReviewClosed": False,
        "runtimeAccepted": False, "runtimePublished": False, "reviewClosed": [], "published": [],
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": NEXT,
    })
    print("Both serial original-family confirmations archived and reconciled; changed-runtime enforcement still pending.")


def finish():
    p = load(C / "progress.json")
    before = load(L / "progress-before-755.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (754, "100", "continue")
    runner = load(C / "runner.json")
    assert (runner["status"], runner["sessionId"], runner["pid"]) == ("running", L.name, 5920)
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP and git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    assert not git("diff", HEAD, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    comment = load(L / "issue-755-reread.json")
    body = (C / "batch-100-confirmation-755-issue-body.txt").read_bytes().decode("utf-8")
    assert comment["user"]["login"] == "stop-cran" and comment["body"] == body and head in body
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for k, v in before.items():
        if k not in changed:
            assert p[k] == v, k
    record = {
        "schemaVersion": 1, "execution": 755, "checkpoint": 755, "batch": "100", "status": "continue",
        "stage": "batch-100-fallback-confirmations-complete-awaiting-fresh-host",
        "recordedAt": now(), "savedCommit": head, "signature": "G", "qualifiedAndroidHead": APP,
        "evidence": "docs/n1-sources/execution-755.json",
        "issueUpdate": comment["html_url"], "ownerIssueAuthorAndExactBodyVerified": True,
        "finding": "N753-fallback-establish", "findingStatus": "resolved semantically; enforcement pending",
        "originalSessionConfirmations": 2, "actualModels": list(review.review.MODELS.values()),
        "serialReviewerProcessExitsVerified": True, "internalToolOverlaps": 0,
        "completePacketReturnedEach": True, "packetBytes": 155372, "packetLines": 4510,
        "runtimeHashesVerified": 8453, "contentVersion": "606c836e4be33ba9",
        "runtimeChanged": False, "manifestChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False, "independentRenderedReviewClosed": False,
        "reviewClosed": [], "published": [], "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": f"SAME100 signed LOCAL evidenceHEAD{head}, qualifiedAndroid{APP}. " + NEXT,
        "inherited754NextActionPreserved": before["nextAction"],
        "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
    }
    after = copy.deepcopy(p)
    assert "execution755CoordinatorCheckpoint" not in after
    after["execution755CoordinatorCheckpoint"] = record
    after.update(checkpoint=755, status="continue", stage=record["stage"], nextAction=record["nextAction"], blocker=None)
    for k, v in before.items():
        if k not in changed:
            assert after[k] == v, k
    new(L / "checkpoint-755-summary.json", record)
    assert load(C / "progress.json") == p
    save(C / "progress.json", after)
    assert load(C / "progress.json") == after
    print(json.dumps({"checkpoint": 755, "status": "continue", "savedCommit": head,
                      "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True}))


if __name__ == "__main__":
    {"record": record, "finish": finish}[sys.argv[1]]()
