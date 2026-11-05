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
assert p["checkpoint"] == 368 and p["batch"] == "060"
head = git("rev-parse", "HEAD")
assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
assert not git("diff", "ea1dac1a6fd2c452db9cf602442e1f287ff95c67", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
audit = load(s / "batch-060-acceptance-audit.json")
limits = audit["limits"]
if mode in {"pending", "terminal-pending"}:
    phase = "accepted" if mode == "pending" else "terminal"
    p["activeExecution"].update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                               recordedAt=datetime.now().astimezone().isoformat())
    p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
    p.update(stage=f"batch-060-{phase}-pending-owner-push-ci-public-archive",
             nextAction=f"SAME060 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no061.")
elif mode in {"records", "finish"}:
    phase = "accepted" if mode == "records" else "terminal"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(c / "artifacts" / f"batch-060-{phase}-ci.json")
    archive = load(c / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "dbf047f0c2e6cd56"
    assert archive["verifiedRuntimeHashes"] == 8309
    assert all(archive[k] for k in ["manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert hashlib.sha256((c / "artifacts" / f"content-{head[:7]}.zip").read_bytes()).hexdigest() == archive["sha256"]
    if mode == "records":
        assert not (s / "batch-060-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 369, "batch": "060",
            "status": "published-verified-bounded-owner-testing", "membership": ["亭"],
            "baseCommit": audit["baseCommit"],
            "authoredSnapshot": p["batch060DraftCheckpoint"]["savedCommit"],
            "initialReviewedTeachingSnapshot": "ea1dac1a6fd2c452db9cf602442e1f287ff95c67",
            "reviewedTeachingSnapshot": "ea1dac1a6fd2c452db9cf602442e1f287ff95c67",
            "textualClosureSnapshot": p["batch060TextualReviewCheckpoint"]["savedCommit"],
            "freshAndroidSnapshot": p["batch060AndroidCheckpoint"]["savedCommit"],
            "nativePreparationSnapshot": p["batch060NativePreparationCheckpoint"]["savedCommit"],
            "nativeEvidenceSnapshot": p["batch060NativeExecutionCheckpoint"]["savedCommit"],
            "visualClosureSnapshot": p["batch060NativeVisualCheckpoint"]["savedCommit"],
            "latestMainIntegrated": audit["latestMainIntegrated"],
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-060-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-060-native-acceptance.json",
            "strictInitialProcessContractAccepted": False,
            "strictFirstConfirmationProcessContractAccepted": False,
            "strictHistoricalProcessContractAccepted": False,
            "supervisedLexicalRemediationAccepted": True,
            "strictVisualProcessContractAccepted": True,
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {"batchPublishedAdditions": 1, "projectPublishedAdditions": 87,
                       "remainingAdditions": 1141, "currentKanji": 1072, "currentWords": 5031,
                       "n1Labelled": 92, "namedSourceMembersPresent": 91,
                       "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
                       "projectNewNecessarySupportWords": 89, "batchChangedReusedArticles": 2,
                       "requiredReciprocalPairs": 2, "activatedBaselinePairs": 0},
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before061.",
        }
        save(s / "batch-060-publication.json", publication)
        ledger = load(s / "batch-060-progress.json")
        ledger["prePublicationCheckpoint"] = {
            k: ledger[k] for k in ["status", "nextAction", "limits", "pendingGates"] if k in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=87, remainingAdditions=1141, publishedCommit=head,
                      publicationRecord="batch-060-publication.json", acceptanceRecord="batch-060-acceptance-audit.json",
                      pendingGates=[], nativeVisualRecord="../n1-reviews/batch-060-native-acceptance.json",
                      nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(s / "batch-060-progress.json", ledger)
        execution = load(s / "execution-369.json")
        execution.update(status=publication["status"], publicationRecord="batch-060-publication.json",
                         publishedAdditions=87, remainingAdditions=1141,
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        save(s / "execution-369.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8309)
        p.update(stage="batch-060-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    else:
        publication = load(s / "batch-060-publication.json")
        receipt = load(c / "batch-060-publication-issue-receipt.json")
        body = (c / "batch-060-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch060 accepted/published/verified at {head}; yield before061. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded061 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]/丘[坂,山]/"
            "山[川,出,木]reviewedguards. Inspect full applicable dictionary families/necessarysupport/curatedreadings/all "
            "activated and reciprocal pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one "
            "active reviewer/serial internaltools and justified original-session confirmations. Applicable fresh non-skipped"
            "Android/native/combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public87/1228;1141remaining;1072kanji/5031words/92N1labels/91namedmembers plus separate妖;89necessarysupportword"
            "additions. " + limits +
            " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch060PublicationCheckpoint"] = publication
        p.update(checkpoint=369, status="continue", stage="batch-060-published-verified-before-061",
                 lastPublishedCommit=head, remainingAdditions=1141, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME060 signed current-main acceptance/terminal verified;368Python/reverified365Android4/367native2/allsourcebaseline/readings/twopairs/strokes/fonts;greenCI8309publichashes/ownerissue. OriginalClaude060-P1/P2 historicalnoncompliance explicit. No061 or secondrunner.")
        p["execution369CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["execution369StartingState"]["status"] = "bounded-publication-checkpoint-complete"
        p["unmetAcceptanceGates"][0] = "Remaining1141source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(c / "batch-060-publication-checkpoint.json", publication)
else:
    raise ValueError(mode)
allowed = {"activeExecution", "stage", "nextAction", "batch060PublicationCheckpoint", "checkpoint",
           "status", "lastPublishedCommit", "remainingAdditions", "blocker",
           "execution369CoordinatorCheckpoint", "unmetAcceptanceGates", "execution369StartingState"}
assert all(p[k] == v for k, v in before.items() if k not in allowed)
save(c / "progress.json", p)
print(p["checkpoint"], p["stage"])
