import importlib.util
import json
import shutil
import subprocess
import sys

from pathlib import Path

spec = importlib.util.spec_from_file_location("acceptance437", Path(__file__).with_name("execution-437.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
C, R, S, L, D = m.C, m.R, m.S, m.L, m.D
load, save, sha, git, now = m.load, m.save, m.sha, m.git, m.now


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-067-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == m.VERSION and archive["verifiedRuntimeHashes"] == 8329
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    m.unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    audit = load(S / "batch-067-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 437, "batch": "067", "membership": ["僧"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": m.BASE, "authoredSnapshot": m.TEACHING, "reviewedTeachingSnapshot": m.TEACHING,
        "textualClosureSnapshot": "f1e5b99ab586ef63cf074c05a825a987ce0b3210",
        "visualClosureSnapshot": m.START, "latestMainIntegrated": audit["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-067-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-067-visual-reconciliation.json",
        "validation": audit, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 94, "remainingAdditions": 1134,
            "currentKanji": 1079, "currentWords": 5037, "n1Labelled": 99, "namedSourceMembersPresent": 98,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
            "projectNewNecessarySupportWords": 95, "batchChangedReusedArticles": 1,
            "requiredReciprocalPairs": 1, "activatedBaselinePairs": 0, "directedComparisonLinks": 2,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": audit["limits"],
        "nextAction": "Verify terminal evidence commit/CI/public ZIP/ownerissue60; checkpoint and yield before068.",
    }
    assert not (S / "batch-067-publication.json").exists()
    save(S / "batch-067-publication.json", publication)
    ledger = load(S / "batch-067-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: ledger[key] for key in ("status", "nextAction", "limits")}
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=94, remainingAdditions=1134, publishedCommit=head,
        publicationRecord="batch-067-publication.json", acceptanceRecord="batch-067-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=publication["limits"],
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-067-progress.json", ledger)
    execution = load(S / "execution-437.json")
    execution.update(status=publication["status"], publicationRecord="batch-067-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-437.json", execution)
    for path in (C / "artifacts" / "batch-067-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json"):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-067-accepted-publication-verified-pending-terminal-evidence"
    p["execution437AcceptedPush"] = {"commit": head, "ciAndArchiveVerified": True}
    save(C / "progress.json", p)
    print("Accepted remote/greenCI/public8329hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-067-publication.json")
    text = f"""Batch **067 (僧)** is published and verified for **bounded owner testing**. Adds necessary support **僧侶 (そうりょ)** and the reused **坊さん** comparison link; not an N1 vocabulary expansion.

Authored/reviewed teaching `{m.TEACHING}`, textual closure `{publication['textualClosureSnapshot']}`, bounded visual closure `{m.START}`. Fresh main `{publication['latestMainIntegrated']}` already ancestral; no substantive teaching/tools changed. Normally signed accepted/integrated publication `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Normal owner-scoped fast-forward; global romanko-ms unchanged.

Fresh combined gates: **368 Python tests**, validator, vocabulary consistency (**2,122/2,431 pilot prompts**, not complete coverage), regenerated fresh manifest; exact frozen inputs/**113 full-family mechanical re-extractions**, six raw character records, exact **94 additions**, baseline **985 kanji/4,942 words/985 strokes** with only preserved reviewed exceptions, source readings/order/curation, **one mapped reciprocal pair/two directions plus both 僧侶–坊さん comparison directions**, reproduced13-stroke pinned geometry, affected Han cmaps and original archive budgets. No 侶 card yet: its retained word metadata activates a future pair. Mechanical hashes do not establish linguistic comprehension.

Blind initial families **claude-opus-5.5 / gpt-6.1-sol** reviewed the same signed snapshot/three teaching scopes/three facets. Original-session dependent visual confirmations returned **23 source PNGs per family/46 actual900x2000 payloads from37capture names**. Reviewer processes and all image calls serial. **Claude's original overlap of two small operational-receipt reads remains disclosed/noncompliant (`processAndCoverageAccepted=false`)**; original-session bounded serial repair completed before GPT. Original reports unchanged; not an all-internal-reads-serial execution. No actionable teaching/rendering defect established. Original source/retrieval/read-depth limits and optional decisions retained; unseen viewport/table regions and actual fallback faces unverified. Actual N1 meaning options visibly wrong for僧 but differ from authored増/値/倍: **authored-choice native presentation not certified**.

Accepted **433 fresh Android3 RealContentTest+1 RareHanTest/no skips** and **435 two native terminalcase0/138.141s** independently reverified, not rerun. Exact full archive productionContentSync **once**: **1,079kanji/5,037words/99N1**, problems0, `{m.VERSION}`, epoch1. Full+Liteソウ/emptyKun; normalizedそう Good persisted/noKunLog; mapped links/comparison routes/three complete articles/SystemBack/offline/N1selection/meaning/13reference-touch strokes/ungradedtrace/recallmiss/persistedDrawAgain. Four production rows readable/distinguishable for僧増値倍人亻曽侶/僧侶/坊さん. Not MLKit, successful human recall, ownerprogress, fallback-face identification or phone evidence.

Historical permission denials/HOST OOMs retained; qualified **HOST-only2GiB** init NEVER used in native. No app/guest heap, production guard, permissions or app code changed. No redundant reviewers/Gradle/native runs.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable public ZIPs verify every8,329 runtime hash**, manifest `{m.VERSION}`. Terminal **{archive['zipEntries']:,}entries /{archive['compressedBytes']:,}compressed /{archive['inflatedBytes']:,}inflated /{archive['retainedBytes']:,}retained bytes** pass unchanged18,000entries/42MiB/80MiB/56MiB; contributor evidence excluded.

Published **94/1,228 additions;1,134 remain**. Current **1,079kanji/5,037words/99N1-labelled/98named-source members plus separate妖**. Project95 necessary support additions are **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required. **Physical-phone/general-release/whole-set acceptance outstanding**. Durable `docs/n1-sources/batch-067-publication.json`, `batch-067-acceptance-audit.json`, `execution-437.json` and original source/review/native records retained. Checkpoint437 saves `continue` and yields **before068**; no next batch or second runner.
"""
    path = C / "execution-437-issue-body.txt"
    assert not path.exists()
    path.write_text(text, encoding="utf-8")
    print("Exact terminal owner issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(L / "before-progress-execution437.json")
    receipt = load(C / "execution-437-issue-receipt.json")
    expected = (C / "execution-437-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == expected.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-068-progress.json").exists()
    publication = load(S / "batch-067-publication.json")
    next_action = (
        f"Batch067 accepted/published/verified at {head}; yield before068. Read complete request/final checkpoint/scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/freshmain, then ONE evidence-bounded068 source preparation below15 from exact remaining rows. "
        "Preserve exact source/baseline identities/levels/fullreading order/exclusions and documented虎/猿/丘/山 guards. "
        "Inspect complete applicable dictionary families, necessary support, practical curated reading rows, activated+allmapped reciprocal pairs, "
        "pinned strokes and every new Han font disposition. Two serial blind different-family initial reviewers, one active/serial internal tools, "
        "bounded original-session confirmations; applicable non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/every immutableZIPhash/originalbudgets. "
        "No unreviewed push/authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. New denial preserve/report/yield. "
        "Public94/1228,1134remain;1079kanji5037words99N1labels98namedmembers plus妖;95support additions NOTN1vocabulary. "
        "Preserve067originalClaude two-small-receipt overlap/processAndCoverageAccepted=false and accepted serialrepair; do not rewrite as fullyserial. "
        + publication["limits"] + " Overallproject incomplete."
    )
    publication.update(
        finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
        terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
        nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=437, status="continue", stage="batch-067-published-verified-before-068",
             lastPublishedCommit=head, remainingAdditions=1134, blocker=None, nextAction=next_action)
    p["batch067PublicationCheckpoint"] = publication
    p["execution437StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1134source-bounded additions not authored/review-closed/published; later batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 437, "checkpoint": 437, "batch": "067",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 368, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8329,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "visualProcessExceptionAndSerialRepairPreserved": True,
        "publishedAdditions": 94, "remainingAdditions": 1134, "phoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "verifiedAt": now(),
    }
    save(C / "execution-437-final-verification.json", result)
    save(C / "batch-067-publication-checkpoint.json", publication)
    p["execution437CoordinatorCheckpoint"] = {**result, "status": "continue", "nextAction": next_action}
    p["batch067PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
