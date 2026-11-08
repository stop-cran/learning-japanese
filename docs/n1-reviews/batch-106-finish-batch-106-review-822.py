"""Verify and checkpoint textual review without claiming runtime acceptance."""
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
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "4656604b-eebf-4190-bcb5-d2e6ae5ddd3e"
HEAD = "5fe224b5c611e8ca0c7c5a1fcbd5ea4a025e606a"
MAIN = "0c582f18b31f65a5e1a908d92e37dde3d34f81ee"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
spec = importlib.util.spec_from_file_location("current_review", C / "review-batch-106-822.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
load, save, sha, git = module.review.load, module.review.save, module.review.sha, module.review.git
NEXT = (
    "SAME106 qualified signed Androidbf30cdead HOST+finite semantic actual options, including "
    "non-skipped RealContentTest three cases/RareHanTest one, word BOTH directions and kanji "
    "defaultN1/All/custom/reduced pools; inspect exact displayed labels/secondary senses/"
    "fallbacks and preserved weak 勅/訓 hypothesis. Textual reviews on SAME signed5fe224b "
    "are complete with actual claude-opus-5.5 and gpt-6.1-sol; no teaching changed, no "
    "established actionable textual defect or consequential unresolved positive teaching "
    "claim. Preserve original full reports/model/process/read limits and optional/explicit "
    "unresolved nonblocking hypothesis dispositions; do not force withdrawal or add a "
    "guard from unproved hypothesis. No changed-passage confirmation needed absent edits. "
    "This checkpoint does NOT execute Android/native or publish. All later fresh native "
    "ContentSyncONCE/N1/All/meaning/curatedreading/drawing/articles/Back/offline/allfourfont/"
    "defaultsystem/wholeword/radical/lookalike/rendered gates remain mandatory, then combined "
    "currentmain/fullPython/vocabulary/baseline-membership-links/manifest/perfilemedia-safepaths/"
    "unchanged18000entries42MiBcompressed80MiBinflated56MiBretained/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/verifiedownerissue. "
    "Full original source820/draft821 acceptance/reading/quiz/link/font/baseline gates and "
    "historical limitations retained EXACT in execution822Inherited821Gates and before822 "
    "snapshot, not new822 runs/retroaccepted. Full[チョク]/[いまし.める,みことのり], selected"
    "[チョク]/[], keyちょく versus displayチョク; modern writtenいまし.めるUNVERIFIED; documented"
    "みことのり outsideJoyoREADINGlistNOTfrequency/invalidity; one necessary勅令 support "
    "NOinferredwordlevel, sovereigngeneral+Meijilegalform, TWOdirectkanjiguards令命/"
    "SIXdirectwordguards命令命じる命ずる法法律規則/symmetricNONTRANSITIVE; "
    "TWOmappedpairsFOURdirectionsZEROactivatedbaselinepairs/ONEexact令lineonlybaselinebodychange. "
    "Verifywhollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. "
    "Parent13320ownsrunner.lock:NOchildacquire/delete/unlock/readprobe; approvedcontrol/"
    "committedsource/frozeninputs only,nooptionalhistoricalsessionrecipes. Preserve/report/"
    "yield actualnewdenial/signinghang/uncertainownership. Published132/1228,1096remainder "
    "unchanged; no107/secondrunner/unreviewedpush/authoragents/concurrentheavywork/"
    "signingretry/guardincrease. CompatibleAndroid125+132 required; oldclientsignore; "
    "qualifiedsignedbf30cdead8515739bc0e671d57a54b9a3109dd46 guard+schemaonlyNOTlatestmain. "
    "Sixseparatelyplaced保案派第策結retainN2/noacceptedcredit/noduplicate/relevel. "
    "Native-speaker/equalcomprehension/fallbackface/originalpixels/everyrequestretention/"
    "phone/effectiveness remainUNVERIFIED. Physicalphone/generalrelease/whole-setoutstanding; "
    "projectincomplete. Next bounded HOST checkpoint only; no native/publication/107 in that checkpoint."
)


def audit():
    module.frozen()
    provenance = load(V / "batch-106-review-dictionary-provenance.json")
    assert sha(module.review.PACKET) == provenance["packetSha256"]
    assert gzip.decompress((V / "batch-106-initial-packet.txt.gz").read_bytes()) == module.review.PACKET.read_bytes()
    for row in provenance["sources"]:
        assert sha(Path(row["path"])) == row["sha256"]
    executions = {}
    for label, model in module.review.MODELS.items():
        prefix = "batch-106-initial-" + label
        execution = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert execution["actualModels"] == [model] and execution["usageCurrentModel"] == model
        assert execution["exitCode"] == 0 and module.review.absent(execution["launcherPid"])
        assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
        assert execution["multiToolResponseCount"] == 0 and coverage["allAssignedRangesReturned"]
        assert len(execution["toolCalls"]) == 1 and execution["availableTools"] == ["view"]
        call = execution["toolCalls"][0]
        assert call["name"] == "view" and call["success"] and call["exactRequestedTextContainedInResult"]
        assert not call["truncationMarker"] and sha(V / (prefix + ".md")) == execution["reportSha256"]
        raw = V / (prefix + ".jsonl")
        archive = V / (prefix + ".jsonl.gz")
        raw_bytes = raw.read_bytes() if raw.exists() else gzip.decompress(archive.read_bytes())
        assert hashlib.sha256(raw_bytes).hexdigest() == execution["rawExecutionSha256"]
        executions[label] = execution
    assert executions["claude"]["completedAt"] < executions["gpt"]["startedAt"]
    assert executions["claude"]["toolCalls"][0]["returnedSha256"] == executions["gpt"]["toolCalls"][0]["returnedSha256"]
    reconciliation = load(V / "batch-106-reconciliation.json")
    assert not reconciliation["establishedActionableFindings"]
    assert not reconciliation["consequentialUnresolvedTextualClaims"]
    assert not reconciliation["teachingChangesAfterReview"]
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    manifest = load(R / "manifest.json")
    assert manifest == json.loads(git("show", HEAD + ":manifest.json"))
    baseline = json.loads(git("show", MAIN + ":manifest.json"))
    new = set(manifest["files"]) - set(baseline["files"])
    changed = {name for name in baseline["files"] if manifest["files"][name] != baseline["files"][name]}
    assert new == {"kanji/勅.md", "words/勅令.md", "strokes/勅.json"}
    assert changed == {"kanji/令.md"}
    summary = {
        "snapshot": HEAD, "actualModels": [e["actualModels"][0] for e in executions.values()],
        "serialProcessExitVerified": True, "completeReturnedPackets": 2, "toolCallsPerReviewer": 1,
        "internalToolOverlaps": 0, "packetSourceHashesPreserved": True,
        "publishedBaselineManifestEntries": len(baseline["files"]),
        "runtimeChangesRelativeToPublishedBase": sorted(new | changed),
        "runtimeAndManifestUnchangedSinceDraft": True, "teachingChanged": False,
        "actualAndroidNativeOrPhoneAcceptance": False,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return executions, summary


def prepare():
    executions, summary = audit()
    for label, execution in executions.items():
        raw = V / f"batch-106-initial-{label}.jsonl"
        archive = raw.with_name(raw.name + ".gz")
        assert not archive.exists()
        archive.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw.read_bytes()
        raw.unlink()
    save(V / "batch-106-initial-executions-822.json", {
        "snapshot": HEAD, "initialExecutions": executions, "audit": summary,
        "limits": "Complete returned bytes and process/model evidence are not comprehension certification.",
    })
    ledger = load(S / "batch-106-progress.json")
    assert ledger["status"] == "local-unreviewed-runtime-draft"
    ledger.update(
        status="textually-reconciled-awaiting-qualified-host-and-native-acceptance",
        textualReviewClosed=["勅"], reviewClosed=[], published=[],
        independentInitialReviewSnapshot=HEAD,
        independentInitialModels=list(module.review.MODELS.values()),
        textualReconciliation="../n1-reviews/batch-106-reconciliation.json",
        textualReviewExecution=822, teachingChangedAfterInitialReview=False, nextAction=NEXT,
        limits="Both new articles and exact令line are textually reconciled without teaching edits. Full reviewClosed stays empty pending qualified host/finite semantic/native/rendered acceptance. Weak訓fallback hypothesis retained, not an established defect. No publication or phone claim; all historical limits and acceptance gates preserved.")
    save(S / "batch-106-progress.json", ledger)
    for name in ["review-batch-106-822.py", "finish-batch-106-review-822.py",
                 "preflight-822.ps1", "checks-batch-106-review-822.ps1", "issue-batch-106-review-822.ps1"]:
        shutil.copyfile(C / name, V / ("batch-106-" + name))
    shutil.copyfile(L / "preflight-822.json", V / "batch-106-runner-role-822.json")


def package():
    audit()
    for name in ["review-batch-106-822.py", "finish-batch-106-review-822.py",
                 "preflight-822.ps1", "checks-batch-106-review-822.ps1", "issue-batch-106-review-822.ps1"]:
        shutil.copyfile(C / name, V / ("batch-106-" + name))
    logs = {}
    for name in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                 "vocabulary", "review-audit", "whitespace"]:
        raw = L / f"{name}-822.txt"
        archive = V / f"batch-106-{name}-822.txt.gz"
        assert raw.exists() and not archive.exists()
        archive.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw.read_bytes()
        logs[name] = {"archive": archive.name, "rawBytes": raw.stat().st_size,
                      "rawSha256": sha(raw), "archiveSha256": sha(archive)}
    for name in ["help", "config-help"]:
        raw = V / f"batch-106-cli-{name}-execution-822.txt"
        archive = raw.with_name(raw.name + ".gz")
        assert not archive.exists()
        archive.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw.read_bytes()
        raw.unlink()
    failed_audit = L / "review-audit-822-attempt1.txt"
    failed_archive = V / "batch-106-review-audit-822-attempt1.txt.gz"
    assert failed_audit.exists() and not failed_archive.exists()
    failed_archive.write_bytes(gzip.compress(failed_audit.read_bytes(), mtime=0))
    assert gzip.decompress(failed_archive.read_bytes()) == failed_audit.read_bytes()
    save(V / "batch-106-execution-822.json", {
        "schemaVersion": 1, "execution": 822, "batch": "106", "snapshot": HEAD,
        "status": "textually-reconciled-unchanged-not-published",
        "reconciliation": "batch-106-reconciliation.json", "validation": logs,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalHelpersAccessed": False, "runtimeChangedThisExecution": False,
        "runtimePublished": False, "publishedAdditions": 132, "remainingAdditions": 1096,
        "nextAction": NEXT, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "diagnostic": load(C / "progress.json")["execution822StartingState"]["diagnostic"],
        "auditDiagnostic": "Post-validation review audit stopped because generic git helper stripped the initial porcelain status space on the first modified ledger row. Corrected status decoding to preserve exact columns, then reran only failed audit and whitespace; prior passing checks were not repeated. Original failed log preserved losslessly; no runtime/permission/gate change.",
        "limits": "Textual and mechanical checkpoint only; no qualified Android/finite live semantic/native/font/rendered/phone acceptance.",
    })


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert not git("diff", HEAD, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", repo=A) == APP and not git("status", "--porcelain", repo=A)
    issue = load(L / "issue-receipt-822.json")
    assert issue["verified"] and issue["author"] == "stop-cran" and issue["localCommit"] == head
    original = load(L / "progress-before-822.json")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (821, "106", "continue")
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in original.items() if k not in changed)
    p["execution822Inherited821Gates"] = {
        "checkpoint": 821, "nextAction": original["nextAction"],
        "invariant": "Preserve exact inherited gates and limitations; textual822 does not rerun or retroaccept them.",
    }
    p.update(checkpoint=822, status="continue",
             stage="batch-106-textually-reconciled-awaiting-qualified-host",
             nextAction=NEXT, blocker=None)
    p["batch106TextualReviewIssueReceipt"] = issue
    p["execution822CoordinatorCheckpoint"] = {
        "schemaVersion": 1, "execution": 822, "checkpoint": 822, "batch": "106",
        "status": "continue", "stage": p["stage"], "savedCommit": head, "signature": "G",
        "reviewSnapshot": HEAD, "publishedBase": MAIN, "androidSignedHead": APP,
        "membership": ["勅"], "sourceRows": [117],
        "initialExecutions": load(V / "batch-106-initial-executions-822.json"),
        "textualReconciliation": "docs/n1-reviews/batch-106-reconciliation.json",
        "evidence": "docs/n1-reviews/batch-106-execution-822.json",
        "textualReviewClosed": ["勅"], "reviewClosed": [], "published": [],
        "consequentialUnresolvedTextualClaims": [], "teachingChanged": False,
        "nonblockingHypotheses": ["Actual later fallback-label assessment must retain weak勅/訓 concern; no mandatory guard established."],
        "runtimeChangedThisExecution": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "actualBuilderChecked": False,
        "nativeDrawingAccepted": False, "renderedAcceptance": False,
        "publishedAdditions": 132, "remainingAdditions": 1096, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False,
        "finalRunnerPreflight": load(L / "preflight-822-final.json"),
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreserved": True,
        "originalRootKeysCompared": len(original), "issueUpdate": issue["url"],
        "ownerIssueAuthorAndBodyVerified": True, "nextAction": NEXT,
        "limits": "Textual checkpoint complete without teaching edits; full batch reviewClosed empty pending host/finite live semantic/native/rendered gates. No publication or project-completion claim.",
    }
    assert all(p[k] == value for k, value in original.items() if k not in changed)
    module.atomic(C / "progress.json", p)
    check = load(C / "progress.json")
    assert check == p and all(check[k] == value for k, value in original.items() if k not in changed)
    save(L / "checkpoint-verification-822.json", {
        "checkpoint": 822, "originalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "changedRootFields": sorted(changed),
        "savedCommit": head, "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "ownerIssueAuthorAndBodyVerified": True, "status": "continue",
    })
    print("Checkpoint822 saved; original historical root values preserved exactly.")


if __name__ == "__main__":
    {"audit": audit, "prepare": prepare, "package": package, "checkpoint": checkpoint}[sys.argv[1]]()
