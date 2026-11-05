import copy
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
S = R / "docs" / "n1-sources"
D = S / "batch-061-acceptance"
TEACHING = "2567f5e7b3888f2df3ed560f618341266b471902"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution378.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree,
                                   text=True, encoding="utf-8").strip()


def verified_archive(phase, head):
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-061-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "d01d660cc41262fe"
    assert archive["verifiedRuntimeHashes"] == 8311
    assert all(archive[k] for k in ("manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    return ci, archive


def main():
    mode = sys.argv[1]
    p = load(C / "progress.json")
    before = copy.deepcopy(p)
    assert p["checkpoint"] == 377 and p["batch"] == "061"
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    audit = load(S / "batch-061-acceptance-audit.json")
    limits = audit["limits"]
    if mode in {"pending", "terminal-pending"}:
        phase = "accepted" if mode == "pending" else "terminal"
        p["activeExecution"].update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                                   recordedAt=datetime.now().astimezone().isoformat())
        p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
        p.update(stage=f"batch-061-{phase}-pending-owner-push-ci-public-archive",
                 nextAction=f"SAME061 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no062.")
    elif mode == "records":
        ci, archive = verified_archive("accepted", head)
        assert not (S / "batch-061-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 378, "batch": "061",
            "status": "published-verified-bounded-owner-testing", "membership": ["俳"],
            "baseCommit": audit["baseCommit"],
            "authoredSnapshot": p["batch061DraftCheckpoint"]["savedCommit"],
            "initialReviewedTeachingSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
            "textualClosureSnapshot": p["batch061TextualClosureCheckpoint"]["savedCommit"],
            "freshAndroidSnapshot": p["batch061AndroidArchivalCheckpoint"]["savedCommit"],
            "nativePreparationSnapshot": p["batch061NativePreparationCheckpoint"]["savedCommit"],
            "nativeEvidenceSnapshot": p["batch061NativeExecutionCheckpoint"]["savedCommit"],
            "visualClosureSnapshot": p["batch061NativeVisualCheckpoint"]["savedCommit"],
            "latestMainIntegrated": audit["latestMainIntegrated"],
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-061-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-061-native-acceptance.json",
            "strictInitialProcessContractAccepted": False,
            "strictDependentProcessContractAccepted": True,
            "strictFirstVisualProcessContractAccepted": False,
            "strictHistoricalProcessContractAccepted": False,
            "prospectiveSupervisedVisualRemediationAccepted": True,
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {
                "batchPublishedAdditions": 1, "projectPublishedAdditions": 88,
                "remainingAdditions": 1140, "currentKanji": 1073, "currentWords": 5031,
                "n1Labelled": 93, "namedSourceMembersPresent": 92,
                "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 0,
                "projectNewNecessarySupportWords": 89, "batchChangedReusedArticles": 3,
                "requiredReciprocalPairs": 3, "activatedBaselinePairs": 2,
            },
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before062.",
        }
        save(S / "batch-061-publication.json", publication)
        ledger = load(S / "batch-061-progress.json")
        ledger["prePublicationCheckpoint"] = {
            key: ledger[key] for key in ("status", "nextAction", "limits", "pendingGates") if key in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=88, remainingAdditions=1140, publishedCommit=head,
                      publicationRecord="batch-061-publication.json", acceptanceRecord="batch-061-acceptance-audit.json",
                      pendingGates=[], nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(S / "batch-061-progress.json", ledger)
        execution = load(S / "execution-378.json")
        execution.update(status=publication["status"], publicationRecord="batch-061-publication.json",
                         publishedAdditions=88, remainingAdditions=1140,
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        save(S / "execution-378.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8311)
        p.update(stage="batch-061-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    elif mode == "finish":
        ci, archive = verified_archive("terminal", head)
        publication = load(S / "batch-061-publication.json")
        receipt = load(C / "batch-061-publication-issue-receipt.json")
        body = (C / "batch-061-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch061 accepted/published/verified at {head}; yield before062. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded062 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]/丘[坂,山]/"
            "山[川,出,木]reviewedguards. Inspect full applicable dictionary families/necessarysupport/curatedreadings/all "
            "activated and reciprocal pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one "
            "active reviewer/serial internaltools and justified original-session confirmations. Applicable fresh non-skipped"
            "Android/native/combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public88/1228;1140remaining;1073kanji/5031words/93N1labels/92namedmembers plus separate妖;89necessarysupportword"
            "additions. " + limits +
            " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch061PublicationCheckpoint"] = publication
        p.update(checkpoint=378, status="continue", stage="batch-061-published-verified-before-062",
                 lastPublishedCommit=head, remainingAdditions=1140, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME061 signed combined-tree acceptance and terminal publication verified;368Python/reverified374Android4/376native2/allsourcebaseline/readings/threepairs/strokes/fonts;greenCI8311publichashes/ownerissue. HistoricalClaude061-P1/P2/P3 explicit, prospective remediation not retroactive strictacceptance. No062 or secondrunner.")
        p["execution378CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["execution378StartingState"]["status"] = "bounded-publication-checkpoint-complete"
        p["unmetAcceptanceGates"][0] = "Remaining1140source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(C / "batch-061-publication-checkpoint.json", publication)
    else:
        raise ValueError(mode)
    allowed = {"activeExecution", "stage", "nextAction", "batch061PublicationCheckpoint", "checkpoint",
               "status", "lastPublishedCommit", "remainingAdditions", "blocker",
               "execution378CoordinatorCheckpoint", "unmetAcceptanceGates", "execution378StartingState"}
    assert all(p[k] == value for k, value in before.items() if k not in allowed)
    save(C / "progress.json", p)
    print(p["checkpoint"], p["stage"])


if __name__ == "__main__":
    main()
