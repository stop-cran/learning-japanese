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
assert p["checkpoint"] == 328 and p["batch"] == "056"
head = git("rev-parse", "HEAD")
assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
assert not git("diff", "7f465a9dff08c9365ce6a32300280d8428fa979f", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
audit = load(s / "batch-056-acceptance-audit.json")
limits = audit["limits"]
if mode in {"pending", "terminal-pending"}:
    phase = "accepted" if mode == "pending" else "terminal"
    p["activeExecution"].update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                               recordedAt=datetime.now().astimezone().isoformat())
    p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
    p.update(stage=f"batch-056-{phase}-pending-owner-push-ci-public-archive",
             nextAction=f"SAME056 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no057.")
elif mode in {"records", "finish"}:
    phase = "accepted" if mode == "records" else "terminal"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(c / "artifacts" / f"batch-056-{phase}-ci.json")
    archive = load(c / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "cb85043f73a606f3"
    assert archive["verifiedRuntimeHashes"] == 8297
    assert all(archive[k] for k in ["manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert hashlib.sha256((c / "artifacts" / f"content-{head[:7]}.zip").read_bytes()).hexdigest() == archive["sha256"]
    if mode == "records":
        assert not (s / "batch-056-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 329, "batch": "056",
            "status": "published-verified-bounded-owner-testing", "membership": ["乏"],
            "baseCommit": "9b5e9fd9f596801eb78078ab14e4c4b35973479d",
            "authoredSnapshot": "4dba935415312d39b1c2defdc05b938d37fe21f0",
            "reviewedTeachingSnapshot": "4dba935415312d39b1c2defdc05b938d37fe21f0",
            "textualClosureSnapshot": "f1461f249d6654a67ea58388a6f4c897f5d8cb3b",
            "freshAndroidSnapshot": "fddfae3526b27d1deea8aabdb202b9a9168f0214",
            "nativePreparationSnapshot": "1a71f2be30dfcd4a1eb296ff068febdf09ce8b47",
            "nativeEvidenceSnapshot": "6283ee5e6b90598cf92516ee6abf7cfa91d08e68",
            "visualClosureSnapshot": "7f465a9dff08c9365ce6a32300280d8428fa979f",
            "latestMainIntegrated": audit["latestMainIntegrated"],
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-056-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-056-native-acceptance.json",
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {"batchPublishedAdditions": 1, "projectPublishedAdditions": 83,
                       "remainingAdditions": 1145, "currentKanji": 1068, "currentWords": 5027,
                       "n1Labelled": 88, "namedSourceMembersPresent": 87,
                       "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 2,
                       "projectNewNecessarySupportWords": 85, "batchChangedReusedSupportArticles": 0,
                       "requiredReciprocalPairs": 2, "activatedBaselinePairs": 0},
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before057.",
        }
        save(s / "batch-056-publication.json", publication)
        ledger = load(s / "batch-056-progress.json")
        ledger["prePublicationCheckpoint"] = {
            k: ledger[k] for k in ["status", "nextAction", "limits", "pendingGates"] if k in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=83, remainingAdditions=1145, publishedCommit=head,
                      publicationRecord="batch-056-publication.json", acceptanceRecord="batch-056-acceptance-audit.json",
                      pendingGates=[], nativeVisualRecord="../n1-reviews/batch-056-native-acceptance.json",
                      nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(s / "batch-056-progress.json", ledger)
        execution = load(s / "execution-329.json")
        execution.update(status=publication["status"], publicationRecord="batch-056-publication.json",
                         publishedAdditions=83, remainingAdditions=1145,
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        save(s / "execution-329.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8297)
        p.update(stage="batch-056-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    else:
        publication = load(s / "batch-056-publication.json")
        receipt = load(c / "batch-056-publication-issue-receipt.json")
        body = (c / "batch-056-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch056 accepted/published/verified at {head}; yield before057. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded057 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]guards. "
            "Inspect full applicable dictionary families/necessarysupport/curatedreadings/all activated and reciprocal "
            "pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one active reviewer/serial "
            "internaltools and justified original-session confirmations. Applicable fresh non-skippedAndroid/native/"
            "combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public83/1228;1145remaining;1068kanji/5027words/88N1labels/87namedmembers plus separate妖. "
            + limits + " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch056PublicationCheckpoint"] = publication
        p.update(checkpoint=329, status="continue", stage="batch-056-published-verified-before-057",
                 lastPublishedCommit=head, remainingAdditions=1145, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME056 signed current-main acceptance/terminal verified;368Python/reverified320Android4/326native2/allsourcebaseline/readings/links/strokes/fonts;greenCI8297publichashes/ownerissue. No057 or secondrunner.")
        p["execution329CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["unmetAcceptanceGates"][0] = "Remaining1145source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(c / "batch-056-publication-checkpoint.json", publication)
else:
    raise ValueError(mode)
allowed = {"activeExecution", "stage", "nextAction", "batch056PublicationCheckpoint", "checkpoint",
           "status", "lastPublishedCommit", "remainingAdditions", "blocker",
           "execution329CoordinatorCheckpoint", "unmetAcceptanceGates"}
assert all(p[k] == v for k, v in before.items() if k not in allowed)
save(c / "progress.json", p)
print(p["checkpoint"], p["stage"])
