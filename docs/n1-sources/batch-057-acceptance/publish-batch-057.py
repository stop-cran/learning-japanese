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
assert p["checkpoint"] == 338 and p["batch"] == "057"
head = git("rev-parse", "HEAD")
assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
assert not git("diff", "4aa811b55df37e07d93ec3aaf0d97a0f386881c7", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
audit = load(s / "batch-057-acceptance-audit.json")
limits = audit["limits"]
if mode in {"pending", "terminal-pending"}:
    phase = "accepted" if mode == "pending" else "terminal"
    p["activeExecution"].update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                               recordedAt=datetime.now().astimezone().isoformat())
    p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
    p.update(stage=f"batch-057-{phase}-pending-owner-push-ci-public-archive",
             nextAction=f"SAME057 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no058.")
elif mode in {"records", "finish"}:
    phase = "accepted" if mode == "records" else "terminal"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(c / "artifacts" / f"batch-057-{phase}-ci.json")
    archive = load(c / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "47f11f7f539a1d55"
    assert archive["verifiedRuntimeHashes"] == 8300
    assert all(archive[k] for k in ["manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert hashlib.sha256((c / "artifacts" / f"content-{head[:7]}.zip").read_bytes()).hexdigest() == archive["sha256"]
    if mode == "records":
        assert not (s / "batch-057-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 339, "batch": "057",
            "status": "published-verified-bounded-owner-testing", "membership": ["企"],
            "baseCommit": "e8dc74eba6a783552f069593c6fc1d3849986293",
            "authoredSnapshot": "aef958a3bccd96044d0af50e2da74b1b8cfe20da",
            "reviewedTeachingSnapshot": "acc397033503a38aa88506fc3ad966761793db72",
            "textualClosureSnapshot": "acc397033503a38aa88506fc3ad966761793db72",
            "freshAndroidSnapshot": "d9712bf9a2c03f3fae51c2f751481a05affbc0f9",
            "nativePreparationSnapshot": "6dfc42dd3129b7f4efea4caf537931b5a7348c32",
            "nativeEvidenceSnapshot": "4d460d10add0b9c88d6514837e2806b1d9946c3a",
            "visualClosureSnapshot": "4aa811b55df37e07d93ec3aaf0d97a0f386881c7",
            "latestMainIntegrated": audit["latestMainIntegrated"],
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-057-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-057-native-acceptance.json",
            "strictInitialProcessContractAccepted": False, "strictVisualProcessContractAccepted": False,
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {"batchPublishedAdditions": 1, "projectPublishedAdditions": 84,
                       "remainingAdditions": 1144, "currentKanji": 1069, "currentWords": 5028,
                       "n1Labelled": 89, "namedSourceMembersPresent": 88,
                       "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
                       "projectNewNecessarySupportWords": 86, "batchChangedReusedSupportArticles": 1,
                       "requiredReciprocalPairs": 2, "activatedBaselinePairs": 1},
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before058.",
        }
        save(s / "batch-057-publication.json", publication)
        ledger = load(s / "batch-057-progress.json")
        ledger["prePublicationCheckpoint"] = {
            k: ledger[k] for k in ["status", "nextAction", "limits", "pendingGates"] if k in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=84, remainingAdditions=1144, publishedCommit=head,
                      publicationRecord="batch-057-publication.json", acceptanceRecord="batch-057-acceptance-audit.json",
                      pendingGates=[], nativeVisualRecord="../n1-reviews/batch-057-native-acceptance.json",
                      nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(s / "batch-057-progress.json", ledger)
        execution = load(s / "execution-339.json")
        execution.update(status=publication["status"], publicationRecord="batch-057-publication.json",
                         publishedAdditions=84, remainingAdditions=1144,
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        save(s / "execution-339.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8300)
        p.update(stage="batch-057-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    else:
        publication = load(s / "batch-057-publication.json")
        receipt = load(c / "batch-057-publication-issue-receipt.json")
        body = (c / "batch-057-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch057 accepted/published/verified at {head}; yield before058. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded058 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]guards. "
            "Inspect full applicable dictionary families/necessarysupport/curatedreadings/all activated and reciprocal "
            "pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one active reviewer/serial "
            "internaltools and justified original-session confirmations. Applicable fresh non-skippedAndroid/native/"
            "combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public84/1228;1144remaining;1069kanji/5028words/89N1labels/88namedmembers plus separate妖. "
            + limits + " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch057PublicationCheckpoint"] = publication
        p.update(checkpoint=339, status="continue", stage="batch-057-published-verified-before-058",
                 lastPublishedCommit=head, remainingAdditions=1144, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME057 signed current-main acceptance/terminal verified;368Python/reverified334Android4/336native2/allsourcebaseline/readings/links/strokes/fonts;greenCI8300publichashes/ownerissue. Original process noncompliance remains explicit. No058 or secondrunner.")
        p["execution339CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["unmetAcceptanceGates"][0] = "Remaining1144source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(c / "batch-057-publication-checkpoint.json", publication)
else:
    raise ValueError(mode)
allowed = {"activeExecution", "stage", "nextAction", "batch057PublicationCheckpoint", "checkpoint",
           "status", "lastPublishedCommit", "remainingAdditions", "blocker",
           "execution339CoordinatorCheckpoint", "unmetAcceptanceGates"}
assert all(p[k] == v for k, v in before.items() if k not in allowed)
save(c / "progress.json", p)
print(p["checkpoint"], p["stage"])
