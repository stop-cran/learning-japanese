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
assert p["checkpoint"] == 304 and p["batch"] == "054"
head = git("rev-parse", "HEAD")
assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
assert not git("diff", "ffe45e9fc6eba82e4e0e6c3f53608d916a791eba", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
audit = load(s / "batch-054-acceptance-audit.json")
limits = audit["limits"]
if mode in {"pending", "terminal-pending"}:
    phase = "accepted" if mode == "pending" else "terminal"
    p["activeExecution"].update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                               recordedAt=datetime.now().astimezone().isoformat())
    p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
    p.update(stage=f"batch-054-{phase}-pending-owner-push-ci-public-archive",
             nextAction=f"SAME054 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no055.")
elif mode in {"records", "finish"}:
    phase = "accepted" if mode == "records" else "terminal"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(c / "artifacts" / f"batch-054-{phase}-ci.json")
    archive = load(c / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "8846e9a9dc29d24c"
    assert archive["verifiedRuntimeHashes"] == 8290
    assert all(archive[k] for k in ["manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert hashlib.sha256((c / "artifacts" / f"content-{head[:7]}.zip").read_bytes()).hexdigest() == archive["sha256"]
    if mode == "records":
        assert not (s / "batch-054-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 305, "batch": "054",
            "status": "published-verified-bounded-owner-testing", "membership": ["且"],
            "baseCommit": "672266d5fffae425e608cdfa5a631ac147d1d08c",
            "authoredSnapshot": "4fb51498f6912169499456031380ce2353373397",
            "reviewedTeachingSnapshot": "4fb51498f6912169499456031380ce2353373397",
            "textualClosureSnapshot": "2500120842f5ed6db9382dc0f6848b7811487623",
            "freshAndroidSnapshot": "b957500752f3f62f5228706db9f1ea6d4a17d0ed",
            "nativePreparationSnapshot": "9b48eb9e657c69c2dac785f1a91e20312c9604b8",
            "nativeExecutionSnapshot": "73593c32886b12443c6da65b9b6c2e393ba01ace",
            "visualClosureSnapshot": "0fe8e4f8c0804fe41a26bd1ee4f6fc9b0a9c2fa0",
            "latestMainIntegrated": audit["latestMainIntegrated"],
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-054-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-054-native-acceptance.json",
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {"batchPublishedAdditions": 1, "projectPublishedAdditions": 81,
                       "remainingAdditions": 1147, "currentKanji": 1066, "currentWords": 5024,
                       "n1Labelled": 86, "namedSourceMembersPresent": 85,
                       "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
                       "projectNewNecessarySupportWords": 82, "batchChangedReusedSupportArticles": 0,
                       "requiredReciprocalPairs": 1, "activatedBaselinePairs": 0},
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before055.",
        }
        save(s / "batch-054-publication.json", publication)
        ledger = load(s / "batch-054-progress.json")
        ledger["prePublicationCheckpoint"] = {
            k: ledger[k] for k in ["status", "nextAction", "limits"] if k in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=81, remainingAdditions=1147, publishedCommit=head,
                      publicationRecord="batch-054-publication.json", acceptanceRecord="batch-054-acceptance-audit.json",
                      nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(s / "batch-054-progress.json", ledger)
        execution = load(s / "execution-305.json")
        execution.update(status=publication["status"], publicationRecord="batch-054-publication.json",
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        save(s / "execution-305.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8290)
        p.update(stage="batch-054-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    else:
        publication = load(s / "batch-054-publication.json")
        receipt = load(c / "batch-054-publication-issue-receipt.json")
        body = (c / "batch-054-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch054 accepted/published/verified at {head}; yield before055. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded055 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]guards. "
            "Inspect full applicable dictionary families/necessarysupport/curatedreadings/all activated and reciprocal "
            "pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one active reviewer/serial "
            "internaltools and justified original-session confirmations. Applicable fresh non-skippedAndroid/native/"
            "combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public81/1228;1147remaining;1066kanji/5024words/86N1labels/85namedmembers plus separate妖. "
            + limits + " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch054PublicationCheckpoint"] = publication
        p.update(checkpoint=305, status="continue", stage="batch-054-published-verified-before-055",
                 lastPublishedCommit=head, remainingAdditions=1147, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME054 signed current-main acceptance/terminal verified;368Python/reverified301Android4/native2/fullsourcebaseline/readings/links/strokes/fonts;greenCI8290publichashes/ownerissue. No055 or secondrunner.")
        p["execution305CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["unmetAcceptanceGates"][0] = "Remaining1147source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(c / "batch-054-publication-checkpoint.json", publication)
else:
    raise ValueError(mode)
allowed = {"activeExecution", "stage", "nextAction", "batch054PublicationCheckpoint", "checkpoint",
           "status", "lastPublishedCommit", "remainingAdditions", "blocker",
           "execution305CoordinatorCheckpoint", "unmetAcceptanceGates"}
assert all(p[k] == v for k, v in before.items() if k not in allowed)
save(c / "progress.json", p)
print(p["checkpoint"], p["stage"])
