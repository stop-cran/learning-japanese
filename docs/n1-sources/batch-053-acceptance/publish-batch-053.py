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
assert p["checkpoint"] == 295 and p["batch"] == "053"
head = git("rev-parse", "HEAD")
assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
assert not git("diff", "3e37ebdac9af2880ceaa810ca34a7588d8c1d602", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
audit = load(s / "batch-053-acceptance-audit.json")
limits = audit["limits"]
if mode in {"pending", "terminal-pending"}:
    phase = "accepted" if mode == "pending" else "terminal"
    active = copy.deepcopy(p["execution296StartingState"])
    active.update(status=f"{phase}-signed-pending-owner-push-ci-public-archive",
                  recordedAt=datetime.now().astimezone().isoformat())
    active["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
    p["activeExecution"] = active
    p.update(stage=f"batch-053-{phase}-pending-owner-push-ci-public-archive",
             nextAction=f"SAME053 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no054.")
elif mode in {"records", "finish"}:
    phase = "accepted" if mode == "records" else "terminal"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(c / "artifacts" / f"batch-053-{phase}-ci.json")
    archive = load(c / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == "ba2d74eac9ea12e1"
    assert archive["verifiedRuntimeHashes"] == 8287
    assert all(archive[k] for k in ["manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert hashlib.sha256((c / "artifacts" / f"content-{head[:7]}.zip").read_bytes()).hexdigest() == archive["sha256"]
    if mode == "records":
        assert not (s / "batch-053-publication.json").exists()
        publication = {
            "schemaVersion": 1, "execution": 296, "batch": "053",
            "status": "published-verified-bounded-owner-testing", "membership": ["丙"],
            "baseCommit": "e16c95b3edc55975b7a2c7985bf730425baa2f83",
            "authoredSnapshot": "3e37ebdac9af2880ceaa810ca34a7588d8c1d602",
            "reviewedTeachingSnapshot": "3e37ebdac9af2880ceaa810ca34a7588d8c1d602",
            "textualClosureSnapshot": "0ec559e24f5895b2818fbaaf88cbb698ba750e99",
            "freshAndroidSnapshot": "93c55a2c17bd61123e2a5bacf1ff47a5c2ad48cf",
            "nativePreparationSnapshot": "c3880ee222728c1209e988b0d0b6d6563c1bfc38",
            "visualClosureSnapshot": "5564579c9778c1ed55f77f81dbbdfce118a03241",
            "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
            "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
            "reviewRecord": "../n1-reviews/batch-053-reconciliation.json",
            "nativeRecord": "../n1-reviews/batch-053-native-acceptance.json",
            "validation": audit, "ci": ci, "immutablePublicArchive": archive,
            "counts": {"batchPublishedAdditions": 1, "projectPublishedAdditions": 80,
                       "remainingAdditions": 1148, "currentKanji": 1065, "currentWords": 5023,
                       "n1Labelled": 85, "namedSourceMembersPresent": 84,
                       "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 2,
                       "projectNewNecessarySupportWords": 81, "batchChangedReusedSupportArticles": 0,
                       "requiredReciprocalPairs": 2, "activatedBaselinePairs": 0},
            "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
            "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
            "limits": limits, "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before054.",
        }
        save(s / "batch-053-publication.json", publication)
        ledger = load(s / "batch-053-progress.json")
        ledger["prePublicationCheckpoint"] = {
            k: ledger[k] for k in ["status", "nextAction", "limits", "pendingQualification"] if k in ledger}
        ledger.update(status=publication["status"], published=ledger["membership"],
                      publishedAdditions=80, remainingAdditions=1148, publishedCommit=head,
                      publicationRecord="batch-053-publication.json", acceptanceRecord="batch-053-acceptance-audit.json",
                      pendingQualification=[], nextAction=publication["nextAction"], limits=limits)
        for row in ledger["supportMappings"]:
            row["status"] = publication["status"]
        save(s / "batch-053-progress.json", ledger)
        execution = load(s / "execution-296.json")
        execution.update(status=publication["status"], publicationRecord="batch-053-publication.json",
                         publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
        save(s / "execution-296.json", execution)
        p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                                   acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8287)
        p.update(stage="batch-053-accepted-publication-verified-pending-terminal-receipts",
                 nextAction=publication["nextAction"])
    else:
        publication = load(s / "batch-053-publication.json")
        receipt = load(c / "batch-053-publication-issue-receipt.json")
        body = (c / "batch-053-publication-comment.txt").read_text(encoding="utf-8-sig")
        assert receipt["user"]["login"] == "stop-cran" and head in body
        assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
        publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                           terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False)
        next_action = (
            f"Batch053 accepted/published/verified at {head}; yield before054. Fresh coordinator read complete authorized "
            "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed "
            "heads/latestmain, then ONE risk/evidence-bounded054 below15 from exact remaining frozen source rows. "
            "Preserve baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]guards. "
            "Inspect full applicable dictionary families/necessarysupport/curatedreadings/all activated and reciprocal "
            "pairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one active reviewer/serial "
            "internaltools and justified original-session confirmations. Applicable fresh non-skippedAndroid/native/"
            "combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
            "Public80/1228;1148remaining;1065kanji/5023words/85N1labels/84namedmembers plus separate妖. "
            + limits + " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
        )
        publication["nextAction"] = next_action
        p["batch053PublicationCheckpoint"] = publication
        p.update(checkpoint=296, status="continue", stage="batch-053-published-verified-before-054",
                 lastPublishedCommit=head, remainingAdditions=1148, blocker=None, nextAction=next_action)
        p["activeExecution"].update(
            status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
            recordedAt=datetime.now().astimezone().isoformat(),
            result="SAME053 signed acceptance/terminal verified;368Python/reverified292Android4/native2/fullsourcebaseline/readings/links/strokes/fonts;greenCI8287publichashes/ownerissue. No054 or secondrunner.")
        p["execution296CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
        p["unmetAcceptanceGates"][0] = "Remaining1148source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
        save(c / "batch-053-publication-checkpoint.json", publication)
else:
    raise ValueError(mode)
allowed = {"activeExecution", "stage", "nextAction", "batch053PublicationCheckpoint", "checkpoint",
           "status", "lastPublishedCommit", "remainingAdditions", "blocker",
           "execution296CoordinatorCheckpoint", "unmetAcceptanceGates"}
assert all(p[k] == v for k, v in before.items() if k not in allowed)
save(c / "progress.json", p)
print(p["checkpoint"], p["stage"])
