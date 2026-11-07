"""Reconcile confirmed text and preserve the bounded local checkpoint."""
import ast
import gzip
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("confirmation", C / "confirm-batch-100-750.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
HEAD, INITIAL, APP, MAIN = review.HEAD, review.INITIAL, review.APP, review.MAIN
load, save, sha, git = review.load, review.save, review.sha, review.git
NEXT = (
    "SAME100 fresh qualified Android HOST verification only at signed bf30cdead8515739bc0e671d57a54b9a3109dd46: "
    "RealContentTest three cases plus RareHanTest one case, inspect non-skipped XML against THIS content tree, "
    "preserve exact reports/provenance and normally signed local evidence, then yield. "
    "Textual initial reviews and TWO SERIAL original-session changed-passage confirmations are COMPLETE on "
    "signed44b5c4ee; do not rerun textual reviews or call whole batch review-closed. "
    "Claude4975f494/claude-opus-5.5 and GPTc9e3c7f4/gpt-6.1-sol confirmed F1/C1-establish/H1-initial "
    "resolved and H1-wound withdrawn; original coverage disagreement and all original reports/read limits remain. "
    "The創/初 pair is an evidence-supported conservative direct safeguard, not a proven historical live-quiz "
    "failure or universal synonym. Ten direct symmetric NONTRANSITIVE guards; no legacy設/初 edits. "
    "Six full readings/order and selectedソウ/つく.る preserved; source-onlyショウ/けず.しける allocation "
    "UNVERIFIED, explicitly qualified/unselected. Reused創作N2/作るN5 metadata and13/5 original guards, "
    "five all-mapped pairs/ten directions/one activated baseline pair/three exact reused changes retained. "
    "Use explicit JDK17/SDK paths, one Gradle worker and quoted in-process Kotlin argument, unchanged2g; "
    "no reviewer/native/Gradle overlap. Later productionContentSyncONCE/native N1-All/meaning/curatedreading/"
    "drawing/article/Back/offline/four-font/all-Han/rendered acceptance, combinedcurrentmain checks, "
    "normal signing/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry/"
    "42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia/verifiedownerissue gates remain mandatory. "
    "No unreviewedpush/101/authoragent/secondrunner/signingretry/guardincrease. Verify whollyclean signedheads/"
    "freshmain/liveparentancestry/decodedlauncher/exactsession. Parent5920 ownsrunner.lock: no childacquire/"
    "delete/unlock/readprobe. Approvedcontrol/committedsource/frozeninputs only, not optional historicalsession"
    "recipes; preserve/report/yield actualnewdenial/signinghang/uncertainownership. Published126/1228,"
    "1102acceptanceremainder unchanged; six earlierN2placements保案派第策結 remain separate, never duplicate/"
    "relevel. Physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def archive(source, target):
    assert not target.exists(), target
    raw = source.read_bytes()
    target.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(target.read_bytes()) == raw
    return {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(source),
            "archiveSha256": sha(target), "lossless": True}


def record():
    review.frozen(whole=True)
    processes = {}
    storage = []
    for label, model in review.MODELS.items():
        prefix = f"batch-100-confirmation-750-{label}"
        execution = load(C / (prefix + "-execution.json"))
        assert execution["snapshot"] == HEAD
        assert execution["sessionId"] == review.SESSIONS[label]
        assert execution["actualModels"] == [model] and execution["usageCurrentModel"] == model
        assert execution["exitCode"] == 0 and execution["reviewerProcessExitVerified"]
        assert review.absent(execution["launcherPid"])
        assert execution["allAssignedRangesReturned"] and not execution["observedToolOverlaps"]
        assert not execution["unfinishedTools"] and execution["multiToolResponseCount"] == 0
        assert execution["availableTools"] == ["view"] and len(execution["toolCalls"]) == 1
        call = execution["toolCalls"][0]
        assert call["success"] and call["exactRequestedTextContainedInResult"]
        assert not call["truncationMarker"]
        for suffix in [".md", "-execution.json", "-stderr.txt", "-prompt.txt", "-usage.json"]:
            destination = V / (prefix + suffix)
            assert not destination.exists()
            shutil.copyfile(C / (prefix + suffix), destination)
        storage.append(archive(C / (prefix + ".jsonl"), V / (prefix + ".jsonl.gz")))
        processes[label] = {k: execution[k] for k in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
            "snapshot", "reportSha256", "rawExecutionSha256", "allAssignedRangesReturned"]}
        processes[label].update(
            report=prefix + ".md", execution=prefix + "-execution.json",
            rawExecution=prefix + ".jsonl.gz", internalToolCalls=1, observedToolOverlaps=0,
            processExitVerified=True, fullPacketReturned=True)
    assert processes["claude"]["completedAt"] < processes["gpt"]["startedAt"]
    storage.append(archive(review.PACKET, V / "batch-100-confirmation-750-packet.txt.gz"))
    for kind in ["help", "config-help"]:
        storage.append(archive(L / f"copilot-{kind}-750.txt",
                               V / f"batch-100-cli-{kind}-execution-750.txt.gz"))
    save(V / "batch-100-confirmation-750-lossless-storage.json", storage)
    shutil.copyfile(L / "confirmation-750-provenance.json",
                    V / "batch-100-confirmation-750-provenance.json")
    shutil.copyfile(L / "preflight-750.json", V / "batch-100-confirmation-750-runner-role.json")
    reconciliation = load(V / "batch-100-reconciliation.json")
    assert reconciliation["status"] == "author-corrected-awaiting-original-session-confirmations"
    assert not reconciliation["textualAcceptanceComplete"]
    reconciliation.update(
        status="textual-confirmations-complete-awaiting-fresh-android",
        textualAcceptanceComplete=True, runtimeChangedThisExecution=False,
        correctedTeachingSnapshot=HEAD, confirmationExecution=750,
        confirmations=processes, unresolvedTextualFindings=[],
        confirmationReadDepthLimits=(
            "Both original sessions returned the exact full134314-byte/3535-line packet in one serial "
            "view call; zero internal overlaps and previous process exit verified. Fresh scope: six "
            "current article bodies,12supplement+4original lexical family occurrences,15raw character "
            "records, exact diffs and original source blocks. Initial153-family review is inherited, "
            "not freshly repeated. Byte access is not equal comprehension, native-speaker certification "
            "or independent upstream retrieval. GPT did not re-adjudicate details of Claude-only "
            "optionalO1-O4; their original optional dispositions remain."),
        coordinatorConfirmationAdjudication={
            "F1": "Resolved: exact1398640/1398490 and Daijisen support both short qualified examples. Historical GPT initial coverage CLEAN/Claude NEEDS FIX disagreement preserved, not rebranded consensus.",
            "C1-establish": "Resolved: actual設establish branch overlaps expressly taught創establishment; full source/actual unchanged card support direct guard, not universal synonymy.",
            "H1-initial": "Resolved as conservative direct safeguard with moderate confidence from actualinitial/beginning versusstart/genesis branches. Not counted as a proven historical quiz failure; not based on topic, substring or transitivity.",
            "H1-wound": "Withdrawn: no kanji/傷.md; word namespace does not create that quiz candidate.",
            "reportQualifications": "Claude's remark that over-excluding costs little is NOT adopted as a general authoring rule or sole pair justification. Both reviewers supply exact branch/source overlap. Claude's summary orders wordguard counts ambiguously; preserved metadata/audit establish創作13and作る5.",
        },
        nextAction=NEXT)
    for verdict in reconciliation["verdicts"].values():
        verdict["correctness"] = "CLEAN"
        verdict["scopedCoverage"] = "CLEAN"
        verdict["textComprehensibility"] = "CLEAN"
        if "quizPoolAcceptance" in verdict:
            verdict["quizPoolAcceptance"] = "UNVERIFIED runtime gate; textual direct-guard semantics confirmed, not live N1/All/custom acceptance"
    for finding in reconciliation["findings"]:
        if finding["id"] in {"F1", "C1-establish", "H1-initial"}:
            assert finding["status"] == "partially resolved"
            finding["statusBefore750"] = finding["status"]
            finding["status"] = "resolved"
            finding["confirmation750"] = reconciliation["coordinatorConfirmationAdjudication"][finding["id"]]
            finding["confirmingModels"] = list(review.MODELS.values())
        else:
            assert finding["id"] == "H1-wound" and finding["status"] == "withdrawn"
    save(V / "batch-100-reconciliation.json", reconciliation)
    ledger = load(S / "batch-100-progress.json")
    assert ledger["reviewClosed"] == ledger["published"] == []
    ledger.update(
        status="textual-confirmations-complete-awaiting-fresh-android",
        textualAcceptanceComplete=True, confirmationSnapshot=HEAD,
        confirmationEvidence="docs/n1-reviews/batch-100-reconciliation.json",
        runtimeChangedThisExecution=False, nextAction=NEXT)
    ledger["limits"][0] = "Initial and both original-session changed-passage textual reviews complete; batch NOT review-closed. Fresh qualifiedAndroid/native/font/rendered acceptance and publication pending."
    ledger["limits"][5] = "Five all-mapped pairs/ten directions/one activated baseline pair, three exact reused changes. Ten direct symmetric nontransitive kanji guards textually confirmed; live-pool acceptance pending."
    save(S / "batch-100-progress.json", ledger)
    print("Both original-session confirmations reconciled; textual acceptance complete, full batch acceptance pending.")


def seal():
    review.frozen()
    checks = {}
    test_count = None
    for label in ["tests", "validate", "manifest", "budget", "vocabulary", "audit", "whitespace"]:
        path = L / f"{label}-750.txt"
        text = path.read_text(encoding="utf-8-sig")
        if label == "tests":
            match = re.search(r"Ran (\d+) tests", text)
            assert match and "\nOK" in text
            test_count = int(match[1])
        elif label == "validate":
            assert text.strip() == "0 error(s)"
        elif label == "manifest":
            assert "8453 files" in text and "82b45827a5bb4ae3" in text
        elif label == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        elif label == "vocabulary":
            assert "2122/2431 reviewed prompts; stage=pilot" in text
        elif label == "audit":
            audit = json.loads(text)
            assert audit["manifestFresh"] and audit["dictionaryFamilies"] == 163
            assert audit["readingDispositions"] == 6 and audit["curatedOfferedKeys"] == 2
            assert audit["exactBaseRuntimePreservedOutsideRecordedChanges"]
        else:
            assert not text.strip()
        checks[label] = archive(path, V / f"batch-100-confirmation-{label}-750.txt.gz")
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    payloads = {name: value for entries in manifest.values() if isinstance(entries, dict)
                for name, value in entries.items()}
    assert len(payloads) == 8453
    assert (R / "manifest.json").read_bytes() == subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", f"{HEAD}:manifest.json"])
    save(V / "batch-100-confirmation-runtime-preservation-750.json", {
        "snapshot": HEAD, "contentVersion": "82b45827a5bb4ae3", "runtimeHashesVerified": 8453,
        "runtimeDiffSinceCorrectedFreeze": [], "manifestBytesUnchanged": True,
        "hashMethod": "Exact production build_manifest(root) equality, with canonical text-newline normalization and original binary bytes.",
        "sourceAudit": audit, "limits": "Mechanical preservation, not fresh native or phone acceptance.",
    })
    for source, target in [
        (C / "confirm-batch-100-750.py", S / "batch-100-confirmation-recipe-750.py"),
        (C / "checkpoint-750.py", S / "batch-100-confirmation-checkpoint-recipe-750.py"),
        (C / "preflight-750.ps1", V / "batch-100-confirmation-preflight-750.ps1.txt"),
        (C / "checks-batch-100-750.ps1", V / "batch-100-confirmation-checks-750.ps1.txt"),
        (C / "post-batch-100-confirmation-750.ps1", V / "batch-100-confirmation-issue-recipe-750.ps1.txt"),
    ]:
        shutil.copyfile(source, target)
    reconciliation = load(V / "batch-100-reconciliation.json")
    save(S / "execution-750.json", {
        "schemaVersion": 1, "execution": 750, "batch": "100", "stage": reconciliation["status"],
        "correctedTeachingSnapshot": HEAD, "originalTeachingSnapshot": INITIAL,
        "androidSignedHead": APP, "freshOriginMain": MAIN,
        "startingState": load(C / "progress.json")["execution750StartingState"],
        "confirmations": reconciliation["confirmations"],
        "reconciliation": "docs/n1-reviews/batch-100-reconciliation.json",
        "checks": checks, "pythonTestsPassed": test_count, "validatorErrors": 0, "localBudget": budget,
        "contentVersion": "82b45827a5bb4ae3", "runtimeHashesVerified": 8453,
        "runtimeChangedThisExecution": False, "runtimePublished": False,
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "resolvedFindings": ["F1", "C1-establish", "H1-initial"],
        "withdrawnHypotheses": ["H1-wound"], "unresolvedTextualFindings": [],
        "reviewClosed": [], "published": [], "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": NEXT,
    })
    print("Textual confirmation evidence sealed; every runtime payload and manifest preserved.")


def signed_identity():
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD and not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP and git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    assert not review.absent(5920)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (749, "100", "continue")
    changes = git("-c", "core.quotepath=false", "diff", "--name-only", HEAD, "HEAD").splitlines()
    assert changes and all(n.startswith("docs/n1-reviews/batch-100-confirmation") or
                           n.startswith("docs/n1-reviews/batch-100-cli-") or n in {
                               "docs/n1-reviews/batch-100-reconciliation.json",
                               "docs/n1-sources/batch-100-progress.json",
                               "docs/n1-sources/execution-750.json",
                               "docs/n1-sources/batch-100-confirmation-recipe-750.py",
                               "docs/n1-sources/batch-100-confirmation-checkpoint-recipe-750.py",
                           } for n in changes)
    return head


def issue():
    head = signed_identity()
    target = C / "batch-100-confirmation-750-issue.txt"
    assert not target.exists()
    target.write_text(
        "Batch100: **both original-session changed-passage confirmations complete; textual acceptance only**.\n\n"
        f"Normally signed local evidence `{head}` preserves corrected teaching `{HEAD}` unchanged. "
        "Original Claude Opus5.5 session4975f494 and GPT-6.1 Sol sessionc9e3c7f4 ran serially, "
        "with exact actual models, process exit before next reviewer, view-only tools and zero internal "
        "tool overlap verified. Each returned the same complete134314-byte/3535-line correction "
        "packet: six current article bodies,12supplement+4original lexical family occurrences,15raw "
        "character records, exact initial-to-corrected/reused diffs and original public source "
        "blocks. Full original reports, raw JSONL, prompts, usage and source/read/process limits "
        "preserved losslessly. Initial153-family evidence is inherited, not a new full reread; "
        "byte access is not equal comprehension or independent upstream retrieval.\n\n"
        "F1 founding/formal-wound examples and C1-establish direct創/設 guard resolved. "
        "H1-initial direct創/初 guard confirmed as a reasonable conservative safeguard from "
        "actualinitial/beginning versusstart/genesis branches, not a proven prior live-quiz "
        "failure or universal synonym. H1-wound remains withdrawn: no kanji/傷.md; word article "
        "is another quiz namespace. Historical initial coverage disagreement and optionalO1-O4 "
        "preserved. Both reviewers now report correctness/scopedcoverage/textcomprehensibility "
        "CLEAN for revised創 and each exact three reused changes; no new actionable regression. "
        "This does not certify native fonts, rendered phone UI or live N1/All/custom pools.\n\n"
        "All six readings/order, two selected keys, source-onlyショウ/けず.しける explicitly "
        "UNVERIFIED/unselected, reused創作N2/作るN5 metadata and13/5 guards, five mapped "
        "pairs/ten directions/one activated baseline pair/ten direct symmetric NONTRANSITIVE "
        "guards remain unchanged. Focused source/format tests, validator0errors, regenerated "
        "manifest equality, all8453runtime hashes, source/reading/link/baseline audits and "
        "unchanged archive budgets verified; contentVersion82b45827a5bb4ae3. Vocabulary "
        "consistency retains existing2122/2431pilot scope.\n\n"
        "Evidence: docs/n1-sources/execution-750.json; docs/n1-reviews/batch-100-reconciliation.json "
        "and complete confirmation reports/process/source captures. No Android/native execution, "
        "publication, batch101 or second runner. Parent5920/exact session/decoded launcher "
        "verified; runner.lock untouched; approved workspace artifacts only; no new permission "
        "denial. Next SAME100 fresh qualifiedAndroidbf30cdead non-skipped RealContentTest3/"
        "RareHanTest1, then all original native/rendered/combined-main/signing/owner-push/"
        "terminalCI/exactimmutableZIP/runtimehash/budget gates. Batch NOT fully review-closed. "
        "Published coverage **126/1228;1102 acceptance remainder** unchanged. Physical-phone/"
        "general-release/whole-set acceptance outstanding; project incomplete.\n",
        encoding="utf-8")
    (L / "signed-head-750.txt").write_text(head + "\n", encoding="ascii")
    print("Signed clean local checkpoint verified; owner issue body prepared.")


def finish():
    head = signed_identity()
    data = load(L / "issue-750-verified.json")
    assert data["user"]["login"] == "stop-cran"
    assert data["body"] == (C / "batch-100-confirmation-750-issue.txt").read_bytes().decode("utf-8")
    assert head in data["body"]
    before, p = load(L / "progress-before-750.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    evidence = load(S / "execution-750.json")
    state = {
        "schemaVersion": 1, "execution": 750, "checkpoint": 750, "batch": "100",
        "savedCommit": head, "signature": "G", "correctedTeachingSnapshot": HEAD,
        "originalTeachingSnapshot": INITIAL, "freshOriginMain": MAIN, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-750.json",
        "reconciliation": "docs/n1-reviews/batch-100-reconciliation.json",
        "contentVersion": "82b45827a5bb4ae3", "initialReviewsComplete": True,
        "textualAcceptanceComplete": True, "runtimeDrafted": ["創"], "reviewClosed": [], "published": [],
        "runtimeChangedThisExecution": False, "runtimePublished": False,
        "independentReviewersLaunchedThisExecution": 2, "confirmationProcesses": evidence["confirmations"],
        "models": list(review.MODELS.values()), "serialReviewerProcessesVerified": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "resolvedFindings": ["F1", "C1-establish", "H1-initial"], "withdrawnHypotheses": ["H1-wound"],
        "unresolvedTextualFindings": [], "freshAndroidOrNativeClaimed": False,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "validatorErrors": 0,
        "runtimeHashesVerified": 8453, "publishedAdditions": 126, "remainingAdditions": 1102,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": data["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-100-textual-confirmations-complete-awaiting-fresh-android",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
    }
    p["execution750CoordinatorCheckpoint"] = state
    p["execution750StartingState"]["status"] = "signed-local-textual-confirmation-checkpoint-complete"
    p.update(checkpoint=750, status="continue", stage=state["stage"], batch="100",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    assert persisted == p
    assert all(persisted[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-750-final-verification.json", state)
    print(json.dumps({k: state[k] for k in ["checkpoint", "savedCommit", "status", "stage",
                                         "issueUpdate", "originalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"record": record, "seal": seal, "issue": issue, "finish": finish}[sys.argv[1]]()
