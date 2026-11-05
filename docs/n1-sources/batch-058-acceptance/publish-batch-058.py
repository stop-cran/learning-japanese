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
assert p["checkpoint"] == 348 and p["batch"] == "058"
head = git("rev-parse", "HEAD")
assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
assert not git("diff", "378f4ba3b19cb81e46a0f9a6839e36998390fca9", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
audit = load(s / "batch-058-acceptance-audit.json")
limits = audit["limits"]
if mode in {"pending", "terminal-pending"}:
    phase = "accepted" if mode == "pending" else "terminal"
    p["activeExecution"].update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                               recordedAt=datetime.now().astimezone().isoformat())
    p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
    p.update(stage=f"batch-058-{phase}-pending-owner-push-ci-public-archive",
             nextAction=f"SAME058 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no059.")
elif mode in {"records", "finish"}:
    phase = "accepted" if mode == "records" else "terminal"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(c / "artifacts" / f"batch-058-{phase}-ci.json")
    archive = load(c / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "5e8f3e7e39ea187a"
    assert archive["verifiedRuntimeHashes"] == 8303
    assert all(archive[k] for k in ["manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert hashlib.sha256((c / "artifacts" / f"content-{head[:7]}.zip").read_bytes()).hexdigest() == archive["sha256"]
    if mode == "records":
        assert not (s / "batch-058-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 349, "batch": "058",
            "status": "published-verified-bounded-owner-testing", "membership": ["丘"],
            "baseCommit": "c064f0c749bdc93bc1f86dbd01cec19212991bd7",
            "authoredSnapshot": p["batch058DraftCheckpoint"]["savedCommit"],
            "reviewedTeachingSnapshot": "58b53fd31b6d55baba32c049fba62ac739feb004",
            "textualClosureSnapshot": p["batch058ReconciliationCheckpoint"]["savedCommit"],
            "freshAndroidSnapshot": p["batch058AndroidCheckpoint"]["savedCommit"],
            "nativePreparationSnapshot": p["batch058NativePreparationCheckpoint"]["savedCommit"],
            "nativeEvidenceSnapshot": p["batch058NativeExecutionCheckpoint"]["savedCommit"],
            "visualClosureSnapshot": "378f4ba3b19cb81e46a0f9a6839e36998390fca9",
            "latestMainIntegrated": audit["latestMainIntegrated"],
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-058-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-058-native-acceptance.json",
            "strictInitialProcessContractAccepted": False, "strictVisualProcessContractAccepted": True,
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {"batchPublishedAdditions": 1, "projectPublishedAdditions": 85,
                       "remainingAdditions": 1143, "currentKanji": 1070, "currentWords": 5029,
                       "n1Labelled": 90, "namedSourceMembersPresent": 89,
                       "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
                       "projectNewNecessarySupportWords": 87, "batchChangedReusedSupportArticles": 3,
                       "requiredReciprocalPairs": 3, "activatedBaselinePairs": 1},
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before059.",
        }
        save(s / "batch-058-publication.json", publication)
        ledger = load(s / "batch-058-progress.json")
        ledger["prePublicationCheckpoint"] = {
            k: ledger[k] for k in ["status", "nextAction", "limits", "pendingGates"] if k in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=85, remainingAdditions=1143, publishedCommit=head,
                      publicationRecord="batch-058-publication.json", acceptanceRecord="batch-058-acceptance-audit.json",
                      pendingGates=[], nativeVisualRecord="../n1-reviews/batch-058-native-acceptance.json",
                      nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(s / "batch-058-progress.json", ledger)
        execution = load(s / "execution-349.json")
        execution.update(status=publication["status"], publicationRecord="batch-058-publication.json",
                         publishedAdditions=85, remainingAdditions=1143,
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        save(s / "execution-349.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8303)
        p.update(stage="batch-058-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    else:
        publication = load(s / "batch-058-publication.json")
        receipt = load(c / "batch-058-publication-issue-receipt.json")
        body = (c / "batch-058-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch058 accepted/published/verified at {head}; yield before059. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded059 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]/丘[坂,山]/"
            "山[川,出,木]reviewedguards. Inspect full applicable dictionary families/necessarysupport/curatedreadings/all "
            "activated and reciprocal pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one "
            "active reviewer/serial internaltools and justified original-session confirmations. Applicable fresh non-skipped"
            "Android/native/combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public85/1228;1143remaining;1070kanji/5029words/90N1labels/89namedmembers plus separate妖;87necessarysupportword"
            "additions. " + limits +
            " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch058PublicationCheckpoint"] = publication
        p.update(checkpoint=349, status="continue", stage="batch-058-published-verified-before-059",
                 lastPublishedCommit=head, remainingAdditions=1143, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME058 signed current-main acceptance/terminal verified;368Python/reverified345Android4/347native2/allsourcebaseline/readings/threepairs/strokes/fonts;greenCI8303publichashes/ownerissue. Original initial process noncompliance remains explicit. No059 or secondrunner.")
        p["execution349CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["execution349StartingState"]["status"] = "bounded-publication-checkpoint-complete"
        p["unmetAcceptanceGates"][0] = "Remaining1143source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(c / "batch-058-publication-checkpoint.json", publication)
else:
    raise ValueError(mode)
allowed = {"activeExecution", "stage", "nextAction", "batch058PublicationCheckpoint", "checkpoint",
           "status", "lastPublishedCommit", "remainingAdditions", "blocker",
           "execution349CoordinatorCheckpoint", "unmetAcceptanceGates", "execution349StartingState"}
assert all(p[k] == v for k, v in before.items() if k not in allowed)
save(c / "progress.json", p)
print(p["checkpoint"], p["stage"])
