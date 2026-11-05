import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

from importlib.util import module_from_spec, spec_from_file_location

C = Path(__file__).resolve().parent
spec = spec_from_file_location("acceptance421", C / "execution-421.py")
m = module_from_spec(spec)
spec.loader.exec_module(m)
R, S, V, D = m.R, m.S, m.V, m.D
load, save, sha, git, now, unchanged = m.load, m.save, m.sha, m.git, m.now, m.unchanged


def verified(phase):
    head = git("rev-parse", "HEAD")
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    ci = load(C / "artifacts" / f"batch-065-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == m.VERSION and archive["verifiedRuntimeHashes"] == 8324
    assert all(archive[key] for key in ("manifestEqual", "allPublishingBudgetsPassed",
                                       "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    unchanged()
    return head, ci, archive


def records():
    head, ci, archive = verified("accepted")
    assert head == "1f2da73c75b5fbcce044bdaa53180467d5f2db80"
    audit = load(S / "batch-065-acceptance-audit.json")
    publication = {
        "schemaVersion": 1, "execution": 421, "batch": "065", "membership": ["倹"],
        "status": "published-verified-bounded-owner-testing", "recordedAt": now(),
        "baseCommit": m.BASE, "authoredSnapshot": "5da89bd73eff6a195ee0004762e6eced2b77c15c",
        "reviewedTeachingSnapshot": m.TEACHING, "textualClosureSnapshot": "ae36905b",
        "visualClosureSnapshot": m.START, "latestMainIntegrated": audit["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no signing bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-065-reconciliation.json",
        "nativeVisualRecord": "../n1-reviews/batch-065-visual-reconciliation.json",
        "validation": audit, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 92, "remainingAdditions": 1136,
            "currentKanji": 1077, "currentWords": 5036, "n1Labelled": 97, "namedSourceMembersPresent": 96,
            "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 2,
            "projectNewNecessarySupportWords": 94, "batchChangedReusedArticles": 1,
            "requiredReciprocalPairs": 3, "activatedBaselinePairs": 0,
        },
        "compatibleClient": "Androidf9b59a2+ required; old clients ignore curation.",
        "publicationIdentity": "stop-cran process-scoped token; global romanko-ms unchanged.",
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "limits": audit["limits"],
        "nextAction": "Verify terminal evidence commit/CI/publicZIP/ownerissue60; checkpoint and yield before066.",
    }
    assert not (S / "batch-065-publication.json").exists()
    save(S / "batch-065-publication.json", publication)
    ledger = load(S / "batch-065-progress.json")
    ledger["prePublicationCheckpoint"] = {key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits")}
    ledger.update(status=publication["status"], published=ledger["membership"], publishedAdditions=92,
                  remainingAdditions=1136, publishedCommit=head, publicationRecord="batch-065-publication.json",
                  acceptanceRecord="batch-065-acceptance-audit.json", pendingGates=[],
                  nextAction=publication["nextAction"], limits=publication["limits"])
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-065-progress.json", ledger)
    execution = load(S / "execution-421.json")
    execution.update(status=publication["status"], publicationRecord="batch-065-publication.json",
                     publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]})
    save(S / "execution-421.json", execution)
    for path in (C / "artifacts" / "batch-065-accepted-ci.json",
                 C / "artifacts" / f"content-{head[:7]}-acceptance.json",
                 C / "verify-batch-065-publication.ps1", C / "verify-batch-002-publication.py",
                 C / "push-batch-060.ps1", Path(__file__)):
        shutil.copyfile(path, D / path.name)
    p = load(C / "progress.json")
    p["stage"] = "batch-065-accepted-publication-verified-pending-terminal-evidence"
    p["execution421AcceptedPush"]["ciAndArchiveVerified"] = True
    save(C / "progress.json", p)
    print("Accepted main/greenCI/public8324hashes verified; terminal records prepared.")


def comment():
    head, ci, archive = verified("terminal")
    publication = load(S / "batch-065-publication.json")
    text = f"""Batch **065 (倹)** is published and verified for **bounded owner testing**, with necessary support **倹約 / 倹しい** and the existing 約 common-word backlink.

Authored `{publication['authoredSnapshot']}`, reviewed teaching `{m.TEACHING}`, textual closure `{publication['textualClosureSnapshot']}`, bounded visual closure `{m.START}`. Fresh latest main `{publication['latestMainIntegrated']}` was already ancestral; normal merge with no substantive teaching conflict. Normally signed accepted/integrated publication `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Owner-scoped normal fast-forward pushes; global romanko-ms unchanged.

Fresh combined gates: **368 Python tests**, validator, vocabulary consistency (**2,122/2,431 pilot prompts**, not complete coverage), regenerated fresh manifest, exact frozen bytes and **24 full-family mechanical re-extractions**, exact **92 local additions**, baseline **985 kanji / 4,942 words / 985 strokes** with only preserved reviewed exceptions, all full reading order/curation, **three mapped reciprocal pairs/six directions plus two support-comparison directions**, ten-stroke pinned conversion and complete affected Han cmaps. The initial combined audit exposed a stale current C1 exclusion ledger: teaching and both confirmations already included 倹しい/謙虚. Only the ledger/rationale was synchronized; original failed audit and passing exact rerun preserved. No teaching/manifest or new linguistic decision changed.

Both blind initials used actual **claude-opus-5.5 / gpt-6.1-sol**, same snapshot/four teaching scopes/three facets. C1 is a conservative display guard, not proven live failure or lexical equivalence; original GPT disagreement and source/citation/read-depth limits remain. C2 frequency-neutral spelling clarification confirmed. Original-session bounded visual confirmations establish no actionable content/rendering defect in captured scenes. **Claude's original two internal overlaps remain NONCONFORMANT**; separate original-session five-call recovery serially reread exactly four affected resources. GPT's44calls were serial; all reviewer processes exited serially. Both saw30distinct bounded source images;62actual900x2000payloads are archived separately from1080x2400sources. Access/hash counts are not comprehension. Unseen article/table regions and actual fallbackface remain unverified.

Accepted **417 Android3 RealContentTest + 1 RareHanTest, no skips**, and **419 two native per-case terminal0 / 148.883s** independently reverified without reruns: unchanged reviewed runtime/tools, full productionContentSync imported **once**, **1,077 kanji / 5,036 words / 97 N1**, zero problems, version `{m.VERSION}`, epoch1. Full ケン/[つま.しい,つづまやか], curated ケン/つま.しい, normalizedけん/つましい, both persisted Good grades/no source-only log; meaning/N1selection, all mapped/support routes/SystemBack/offline, ten reference-touch strokes/ungradedtrace/recallmiss/persistedDrawAgain. Four font rows show readable/distinguishable 倹儉険験値人亻阝馬約糸勺/倹約/倹しい. No MLKit, successful humanrecall or phone inference.

Original416permission denial/actual1GiB HOST OOM and049512MiBfailure preserved. Qualified HOST-only2GiB init is **not** for native/guest/app heaps; no guards/permissions/production changes. Owned419helpers stopped; shared5556 and adb SYN/TIME_WAIT not touched or called empty ports.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. **Both immutable ZIPs verify every8,324 runtime hash** and equal manifest `{m.VERSION}`. Terminal archive **{archive['zipEntries']:,} entries / {archive['compressedBytes']:,} compressed / {archive['inflatedBytes']:,} inflated / {archive['retainedBytes']:,} retained bytes** passes unchanged18,000-entry/42MiB/80MiB/56MiB guards; contributor evidence excluded.

Published **92/1,228 additions; 1,136 remain**. Current **1,077 kanji / 5,036 words / 97 N1-labelled / 96 named-source members plus separate 妖**. Two necessary supports this batch,94 project-wide, **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; physical-phone/general-release/whole-set acceptance **outstanding**. Durable `docs/n1-sources/batch-065-publication.json`, `batch-065-acceptance-audit.json`, `execution-421.json` and original source/review/native records retained. Checkpoint421 saves `continue` and yields before066; no066 or second runner.
"""
    path = C / "execution-421-issue-body.txt"
    assert not path.exists()
    path.write_text(text, encoding="utf-8")
    print("Exact verified terminal issue update prepared.")


def finish():
    head, ci, archive = verified("terminal")
    p = load(C / "progress.json")
    original = load(m.SESSION / "before-progress-execution421.json")
    receipt = load(C / "execution-421-issue-receipt.json")
    body = (C / "execution-421-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["body"] == receipt["body"] and remote["user"]["login"] == "stop-cran"
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    assert not (S / "batch-066-progress.json").exists()
    publication = load(S / "batch-065-publication.json")
    next_action = (
        f"Batch065 accepted/published/verified at {head}; yield before066. Read complete request/final checkpoint and scoped live keys; preserve FULL history. "
        "Verify dedicated clean signed heads/freshmain, then ONE evidence-bounded066 source preparation below15 from exact remaining rows. "
        "Preserve source/baseline identities/levels/fullreadings/order/exclusions and documented虎/猿/丘/山 guards. "
        "Inspect full applicable dictionary families, necessarysupport/curatedreadings/allactivated+reciprocalpairs/pinnedstrokes/allnewHanfonts. "
        "Two serialblind different-family initials, one reviewer/serial internal tools/scoped control access, original-session confirmations as needed; "
        "fresh applicable non-skippedAndroid/native/currentmain/normal signing/ownerfastforward/greenCI/everyimmutableZIPhash/originalbudgets. "
        "Public92/1228,1136remain;1077kanji/5036words/97N1labels/96namedmembers plus妖;94supportword additions NOTN1vocabulary. "
        + publication["limits"] +
        " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. New denial preserve/report/yield. Overall incomplete."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       nextBatchStarted=False, nextAction=next_action)
    p.update(checkpoint=421, status="continue", stage="batch-065-published-verified-before-066",
             lastPublishedCommit=head, remainingAdditions=1136, blocker=None, nextAction=next_action)
    p["batch065PublicationCheckpoint"] = publication
    p["execution421StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1136source-bounded additions not authored/review-closed/published; later batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions", "blocker", "nextAction", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    result = {
        "schemaVersion": 1, "execution": 421, "checkpoint": 421, "batch": "065",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingRuntimeToolsUnchanged": True,
        "freshPythonTestsPassed": 368, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "runtimeHashesPerArchive": 8324,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "originalGuardsUnchanged": True,
        "allOriginalHistoricalKeysPreservedExactly": True, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "globalIdentityUnchanged": True,
        "publishedAdditions": 92, "remainingAdditions": 1136,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "verifiedAt": now(),
    }
    save(C / "execution-421-final-verification.json", result)
    save(C / "batch-065-publication-checkpoint.json", publication)
    p["execution421CoordinatorCheckpoint"] = {**result, "status": "continue", "nextAction": next_action}
    p["batch065PublicationIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "publishedCommit": head, "runtimePublished": True}
    save(C / "progress.json", p)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"records": records, "comment": comment, "finish": finish}[sys.argv[1]]()
