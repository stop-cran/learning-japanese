import copy
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
s = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))


def save(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=r, text=True, encoding="utf-8").strip()


mode = sys.argv[1]
p = load(c / "progress.json")
before = copy.deepcopy(p)
assert p["checkpoint"] == 358 and p["batch"] == "059"
head = git("rev-parse", "HEAD")
assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
assert not git("diff", "f074f1116460c112a61687f587bbda7b2b91b0cb", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
audit = load(s / "batch-059-acceptance-audit.json")
limits = audit["limits"]
if mode in {"pending", "terminal-pending"}:
    phase = "accepted" if mode == "pending" else "terminal"
    p["activeExecution"].update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                               recordedAt=datetime.now().astimezone().isoformat())
    p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
    p.update(stage=f"batch-059-{phase}-pending-owner-push-ci-public-archive",
             nextAction=f"SAME059 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no060.")
elif mode in {"records", "finish"}:
    phase = "accepted" if mode == "records" else "terminal"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(c / "artifacts" / f"batch-059-{phase}-ci.json")
    archive = load(c / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "1f1ad78479e9c1f4"
    assert archive["verifiedRuntimeHashes"] == 8306
    assert all(archive[k] for k in ["manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert hashlib.sha256((c / "artifacts" / f"content-{head[:7]}.zip").read_bytes()).hexdigest() == archive["sha256"]
    if mode == "records":
        assert not (s / "batch-059-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 359, "batch": "059",
            "status": "published-verified-bounded-owner-testing", "membership": ["享"],
            "baseCommit": "633f60022b4c42d5f3a6fa83f85465c39729cedd",
            "authoredSnapshot": p["batch059DraftCheckpoint"]["savedCommit"],
            "initialReviewedTeachingSnapshot": "9c79f7dbabcc2309891d2b4ab5ed87d53c8bbb98",
            "reviewedTeachingSnapshot": "769293c824dc41abb9386e76c4dd5f8c676e48e0",
            "textualClosureSnapshot": p["batch059TextualReconciliationCheckpoint"]["savedCommit"],
            "freshAndroidSnapshot": p["execution355CoordinatorCheckpoint"]["savedCommit"],
            "nativePreparationSnapshot": p["batch059NativePreparationCheckpoint"]["savedCommit"],
            "nativeEvidenceSnapshot": p["batch059NativeExecutionCheckpoint"]["savedCommit"],
            "visualClosureSnapshot": "f074f1116460c112a61687f587bbda7b2b91b0cb",
            "latestMainIntegrated": audit["latestMainIntegrated"],
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-059-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-059-native-acceptance.json",
            "strictInitialProcessContractAccepted": True,
            "strictFirstConfirmationProcessContractAccepted": False,
            "strictHistoricalProcessContractAccepted": False, "strictVisualProcessContractAccepted": True,
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {"batchPublishedAdditions": 1, "projectPublishedAdditions": 86,
                       "remainingAdditions": 1142, "currentKanji": 1071, "currentWords": 5030,
                       "n1Labelled": 91, "namedSourceMembersPresent": 90,
                       "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
                       "projectNewNecessarySupportWords": 88, "batchChangedReusedSupportArticles": 1,
                       "requiredReciprocalPairs": 2, "activatedBaselinePairs": 0},
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before060.",
        }
        assert all(publication[k] for k in [
            "authoredSnapshot", "textualClosureSnapshot", "freshAndroidSnapshot",
            "nativePreparationSnapshot", "nativeEvidenceSnapshot"])
        save(s / "batch-059-publication.json", publication)
        ledger = load(s / "batch-059-progress.json")
        ledger["prePublicationCheckpoint"] = {
            k: ledger[k] for k in ["status", "nextAction", "limits", "pendingGates"] if k in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=86, remainingAdditions=1142, publishedCommit=head,
                      publicationRecord="batch-059-publication.json", acceptanceRecord="batch-059-acceptance-audit.json",
                      pendingGates=[], nativeVisualRecord="../n1-reviews/batch-059-native-acceptance.json",
                      nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(s / "batch-059-progress.json", ledger)
        execution = load(s / "execution-359.json")
        execution.update(status=publication["status"], publicationRecord="batch-059-publication.json",
                         publishedAdditions=86, remainingAdditions=1142,
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        execution["checkpointHelperCorrection"] = {
            "firstRecordsAttempt": "KeyError: batch059ReconciliationCheckpoint; no publication ledger or progress written.",
            "correction": "Read exact existing keys; use batch059TextualReconciliationCheckpoint and execution355CoordinatorCheckpoint. No review/runtime/test/publication evidence changed or repeated.",
        }
        save(s / "execution-359.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8306)
        p.update(stage="batch-059-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    else:
        publication = load(s / "batch-059-publication.json")
        receipt = load(c / "batch-059-publication-issue-receipt.json")
        body = (c / "batch-059-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch059 accepted/published/verified at {head}; yield before060. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded060 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]/丘[坂,山]/"
            "山[川,出,木]reviewedguards. Inspect full applicable dictionary families/necessarysupport/curatedreadings/all "
            "activated and reciprocal pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one "
            "active reviewer/serial internaltools and justified original-session confirmations. Applicable fresh non-skipped"
            "Android/native/combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public86/1228;1142remaining;1071kanji/5030words/91N1labels/90namedmembers plus separate妖;88necessarysupportword"
            "additions. " + limits +
            " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch059PublicationCheckpoint"] = publication
        p.update(checkpoint=359, status="continue", stage="batch-059-published-verified-before-060",
                 lastPublishedCommit=head, remainingAdditions=1142, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME059 signed current-main acceptance/terminal verified;368Python/reverified355Android4/357native2/allsourcebaseline/readings/twopairs/strokes/fonts;greenCI8306publichashes/ownerissue. Original Claude confirmation noncompliance remains explicit. No060 or secondrunner.")
        p["execution359CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["execution359StartingState"]["status"] = "bounded-publication-checkpoint-complete"
        p["unmetAcceptanceGates"][0] = "Remaining1142source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(c / "batch-059-publication-checkpoint.json", publication)
else:
    raise ValueError(mode)
allowed = {"activeExecution", "stage", "nextAction", "batch059PublicationCheckpoint", "checkpoint",
           "status", "lastPublishedCommit", "remainingAdditions", "blocker",
           "execution359CoordinatorCheckpoint", "unmetAcceptanceGates", "execution359StartingState"}
assert all(p[k] == v for k, v in before.items() if k not in allowed)
save(c / "progress.json", p)
print(p["checkpoint"], p["stage"])
