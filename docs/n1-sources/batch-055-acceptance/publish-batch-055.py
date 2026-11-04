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
assert p["checkpoint"] == 314 and p["batch"] == "055"
head = git("rev-parse", "HEAD")
assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
assert not git("diff", "9361f6129024a65699081cd1a62b589929e3fd60", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
audit = load(s / "batch-055-acceptance-audit.json")
limits = audit["limits"]
if mode in {"pending", "terminal-pending"}:
    phase = "accepted" if mode == "pending" else "terminal"
    p["activeExecution"].update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                               recordedAt=datetime.now().astimezone().isoformat())
    p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
    p.update(stage=f"batch-055-{phase}-pending-owner-push-ci-public-archive",
             nextAction=f"SAME055 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no056.")
elif mode in {"records", "finish"}:
    phase = "accepted" if mode == "records" else "terminal"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(c / "artifacts" / f"batch-055-{phase}-ci.json")
    archive = load(c / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "66fa8fda924b856d"
    assert archive["verifiedRuntimeHashes"] == 8293
    assert all(archive[k] for k in ["manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert hashlib.sha256((c / "artifacts" / f"content-{head[:7]}.zip").read_bytes()).hexdigest() == archive["sha256"]
    if mode == "records":
        assert not (s / "batch-055-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 315, "batch": "055",
            "status": "published-verified-bounded-owner-testing", "membership": ["丞"],
            "baseCommit": "c2004b726e5086f811a8ef238d78da3c0285dd54",
            "authoredSnapshot": "a532c4d436726e6eeb46ff78cc3dc1a039d6f19e",
            "reviewedTeachingSnapshot": "a532c4d436726e6eeb46ff78cc3dc1a039d6f19e",
            "textualClosureSnapshot": "8bce74a0497867b0f10c348e25486b80b3913772",
            "freshAndroidSnapshot": "b342cff4c070a799fd4bee9f46ea4ff22a7d3eaa",
            "nativePreparationSnapshot": "f1493a3a3f37f7545ac27fe5a8fbf258c8418af9",
            "nativeEvidenceSnapshot": "c4fc279c44541b3d99ddaa56ca5d1ce0452e9026",
            "visualClosureSnapshot": "9361f6129024a65699081cd1a62b589929e3fd60",
            "latestMainIntegrated": audit["latestMainIntegrated"],
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-055-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-055-native-acceptance.json",
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {"batchPublishedAdditions": 1, "projectPublishedAdditions": 82,
                       "remainingAdditions": 1146, "currentKanji": 1067, "currentWords": 5025,
                       "n1Labelled": 87, "namedSourceMembersPresent": 86,
                       "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
                       "projectNewNecessarySupportWords": 83, "batchChangedReusedSupportArticles": 0,
                       "requiredReciprocalPairs": 1, "activatedBaselinePairs": 0},
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before056.",
        }
        save(s / "batch-055-publication.json", publication)
        ledger = load(s / "batch-055-progress.json")
        ledger["prePublicationCheckpoint"] = {
            k: ledger[k] for k in ["status", "nextAction", "limits", "pendingGates"] if k in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=82, remainingAdditions=1146, publishedCommit=head,
                      publicationRecord="batch-055-publication.json", acceptanceRecord="batch-055-acceptance-audit.json",
                      pendingGates=[], nativeVisualRecord="../n1-reviews/batch-055-native-acceptance.json",
                      nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(s / "batch-055-progress.json", ledger)
        execution = load(s / "execution-315.json")
        execution.update(status=publication["status"], publicationRecord="batch-055-publication.json",
                         publishedAdditions=82, remainingAdditions=1146,
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        save(s / "execution-315.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8293)
        p.update(stage="batch-055-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    else:
        publication = load(s / "batch-055-publication.json")
        receipt = load(c / "batch-055-publication-issue-receipt.json")
        body = (c / "batch-055-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch055 accepted/published/verified at {head}; yield before056. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded056 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]guards. "
            "Inspect full applicable dictionary families/necessarysupport/curatedreadings/all activated and reciprocal "
            "pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one active reviewer/serial "
            "internaltools and justified original-session confirmations. Applicable fresh non-skippedAndroid/native/"
            "combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public82/1228;1146remaining;1067kanji/5025words/87N1labels/86namedmembers plus separate妖. "
            + limits + " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch055PublicationCheckpoint"] = publication
        p.update(checkpoint=315, status="continue", stage="batch-055-published-verified-before-056",
                 lastPublishedCommit=head, remainingAdditions=1146, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME055 signed current-main acceptance/terminal verified;368Python/reverified310Android4/312native2/allsourcebaseline/readings/links/strokes/fonts;greenCI8293publichashes/ownerissue. No056 or secondrunner.")
        p["execution315CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["unmetAcceptanceGates"][0] = "Remaining1146source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(c / "batch-055-publication-checkpoint.json", publication)
else:
    raise ValueError(mode)
allowed = {"activeExecution", "stage", "nextAction", "batch055PublicationCheckpoint", "checkpoint",
           "status", "lastPublishedCommit", "remainingAdditions", "blocker",
           "execution315CoordinatorCheckpoint", "unmetAcceptanceGates"}
assert all(p[k] == v for k, v in before.items() if k not in allowed)
save(c / "progress.json", p)
print(p["checkpoint"], p["stage"])
