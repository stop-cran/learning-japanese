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
D = S / "batch-063-acceptance"
TEACHING = "ddad655f71c06e7cb2c749de18596863a800a73d"
VERSION = "c19b742b7e6320a7"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, data):
    temporary = p.with_suffix(p.suffix + ".execution398.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(p)


def git(*args, tree=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree,
                                   text=True, encoding="utf-8").strip()


def verified_archive(phase, head):
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-063-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8317
    assert all(archive[k] for k in ("manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    return ci, archive


def records(p, head, audit):
    ci, archive = verified_archive("accepted", head)
    assert not (S / "batch-063-publication.json").exists()
    publication = {
        "schemaVersion": 1, "execution": 398, "batch": "063",
        "status": "published-verified-bounded-owner-testing", "membership": ["倣"],
        "baseCommit": audit["baseCommit"],
        "authoredSnapshot": p["batch063DraftCheckpoint"]["savedCommit"],
        "initialReviewedTeachingSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": p["batch063ReconciliationCheckpoint"]["savedCommit"],
        "freshAndroidSnapshot": p["batch063AndroidAcceptanceCheckpoint"]["savedCommit"],
        "nativePreparationSnapshot": p["batch063NativePreparationCheckpoint"]["savedCommit"],
        "nativeEvidenceSnapshot": p["batch063NativeExecutionCheckpoint"]["savedCommit"],
        "visualClosureSnapshot": p["batch063NativeVisualCheckpoint"]["savedCommit"],
        "latestMainIntegrated": audit["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-063-reconciliation.json",
        "nativeRecord": "../n1-reviews/batch-063-native-acceptance.json",
        "strictInitialProcessContractAccepted": False, "strictHistoricalProcessContractAccepted": False,
        "prospectiveSupervisedRemediationAccepted": True,
        "validation": audit, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 90, "remainingAdditions": 1138,
            "currentKanji": 1075, "currentWords": 5033, "n1Labelled": 95,
            "namedSourceMembersPresent": 94, "separateExceptionPreserved": "妖",
            "batchNewNecessarySupportWords": 1, "projectNewNecessarySupportWords": 91,
            "batchChangedReusedArticles": 1, "requiredReciprocalPairs": 2, "activatedBaselinePairs": 1,
        },
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "limits": audit["limits"], "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before064.",
    }
    save(S / "batch-063-publication.json", publication)
    ledger = load(S / "batch-063-progress.json")
    ledger["prePublicationCheckpoint"] = {
        k: copy.deepcopy(ledger[k]) for k in ("status", "nextAction", "limits", "fontDisposition", "supportMappings")
    }
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=90, remainingAdditions=1138, publishedCommit=head,
        publicationRecord="batch-063-publication.json", acceptanceRecord="batch-063-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=audit["limits"],
        fontDisposition={**ledger["fontDisposition"], "pending": "Physical-phone/general-release acceptance outstanding.",
                         "acceptedEvidence": "docs/n1-reviews/batch-063-native-acceptance.json"},
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-063-progress.json", ledger)
    execution = load(S / "execution-398.json")
    execution.update(
        status=publication["status"], publicationRecord="batch-063-publication.json",
        publishedAdditions=90, remainingAdditions=1138,
        publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]},
    )
    save(S / "execution-398.json", execution)
    for path in (
        C / "artifacts" / "batch-063-accepted-ci.json",
        C / "artifacts" / f"content-{head[:7]}-acceptance.json",
        C / "verify-batch-002-publication.py", C / "verify-batch-063-publication.ps1",
        C / "push-batch-060.ps1", Path(__file__),
    ):
        assert not (D / path.name).exists()
        shutil.copyfile(path, D / path.name)
    receipts = []
    for name, args in (
        ("validate", ["tools\\validate.py"]), ("manifest", ["tools\\build_manifest.py"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = D / f"execution-398-terminal-{name}.txt"
        assert not path.exists()
        with path.open("wb") as stream:
            process = subprocess.run([sys.executable, "-X", "utf8", "-B", *args],
                                     cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({"command": ["python", "-X", "utf8", "-B", *args], "exitCode": process.returncode,
                         "log": path.relative_to(R).as_posix(), "sha256": sha(path)})
        assert process.returncode == 0, path
    save(S / "batch-063-terminal-validation.json", receipts)
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                               acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8317)
    p.update(stage="batch-063-accepted-publication-verified-pending-terminal-receipts",
             nextAction=publication["nextAction"])


def comment(p, head):
    ci, archive = verified_archive("terminal", head)
    publication = load(S / "batch-063-publication.json")
    text = f"""Batch **063 (倣)** is published and verified for bounded owner testing, with necessary support **模倣** and the reviewed component link in existing 倣う.

Authored/reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`; visual closure `{publication['visualClosureSnapshot']}`. Fresh main `{publication['latestMainIntegrated']}` was already ancestral after a normal merge. Normally signed accepted/integrated publication `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global GitHub identity unchanged.

Fresh combined-tree checks: **368 Python tests**, validator, vocabulary consistency (existing pilot coverage 2122/2431, not repaired or claimed complete), manifest freshness, frozen-source/35-family mechanical re-extraction, exact addition membership, baseline metadata/readings/levels/exclusions/strokes, both reading dispositions, **two reciprocal pairs/four links** including the activated baseline pair, generated ten-stroke geometry and actual font cmaps. Accepted fresh Android **3 RealContentTest + 1 RareHanTest**, no skips, and **two native terminal-0 cases** independently reverified without reruns. Single full production ContentSync import: 1075 kanji/5033 words/95 N1 labels, zero problems, parser epoch1.

Meaning, both curated ホウ/なら.う (normalized ほう/ならう), both pairs/four native transitions, System Back/offline, reference-touch drawing/recall miss/persisted Draw Again retained. Meaning feedback Back BEFORE Next is not a newly persisted grade; both OnGood and KunGood and DrawAgain are separately asserted. Both original model families' dependent visual confirmations retained; no actionable teaching finding. Historical Claude **063-P1** remains noncompliant: two serial supervised lexical confirmations are **not retroactive strict initial-process acceptance**. Optional wrapping/spacing/chip/drawing wording are not content defects or authorized app work. Each visual reviewer inspected25PNGnames/20distinct source hashes, not25independent scenes. Full reading rows visible in kanji-meaning; shifted on-reading clips leftlabels. Four font rows include readable/distinguishable actual亻/傚 and倣/放; actual fallback face/other font scales/unseen pixels remain unverified. Emulator evidence is not physical-phone, MLKit or successful human recall evidence.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) are green. Both immutable GitHub ZIPs preserve **all 8,317 runtime hashes** and manifest `{VERSION}`; terminal ZIP **{archive['zipEntries']:,} entries / {archive['compressedBytes']:,} compressed / {archive['inflatedBytes']:,} inflated / {archive['retainedBytes']:,} retained bytes**, within unchanged 18,000-entry/42-MiB/80-MiB/56-MiB guards. Contributor evidence excluded.

Published **90/1,228 additions; 1,138 remain**. Current collection: **1,075 kanji, 5,033 words, 95 N1-labelled cards, 94 named-source members plus separate 妖**. This batch adds one necessary support word; 91 project-wide, **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** is required; old clients ignore curation. Physical-phone/general-release and whole-set acceptance remain **outstanding**. Original393 denial/parent exact recovery and qualified host-only heap history retained. Durable evidence: `docs/n1-sources/batch-063-publication.json`, `batch-063-acceptance-audit.json`, `execution-398.json`, original source/review/native records. Checkpoint398 persists `continue` and yields before064; no064/second runner started.
"""
    target = C / "batch-063-publication-comment.txt"
    assert not target.exists()
    target.write_text(text, encoding="utf-8")
    print("Prepared exact terminal publication issue update.")


def finish(p, head):
    ci, archive = verified_archive("terminal", head)
    publication = load(S / "batch-063-publication.json")
    receipt = load(C / "batch-063-publication-issue-receipt.json")
    body = (C / "batch-063-publication-comment.txt").read_text(encoding="utf-8-sig")
    assert receipt["user"]["login"] == "stop-cran" and head in body
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    assert remote["user"]["login"] == "stop-cran" and remote["body"] == receipt["body"]
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    app = C.parent / "kanji-cards-android"
    assert not git("status", "--porcelain", tree=app)
    assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not (S / "batch-064-progress.json").exists()
    for row in load(S / "batch-063-terminal-validation.json"):
        assert row["exitCode"] == 0 and sha(R / row["log"]) == row["sha256"]
    ledger = load(S / "batch-063-progress.json")
    assert ledger["published"] == ledger["reviewClosed"] == ledger["membership"] == ["倣"]
    publication.update(
        finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
        terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False,
    )
    next_action = (
        f"Batch063 accepted/published/verified at {head}; yield before064. Fresh coordinator read complete authorized "
        "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed heads/"
        "latestmain, then ONE risk/evidence-bounded064 below15 from exact remaining frozen source rows. Preserve "
        "baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]/丘[坂,山]/"
        "山[川,出,木]reviewedguards. Inspect full applicable dictionary families/necessarysupport/curatedreadings/"
        "allactivated+reciprocalpairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one "
        "active reviewer/serial internaltools and justified original-session confirmations. Applicable fresh non-skipped"
        "Android/native/combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
        "Public90/1228;1138remaining;1075kanji/5033words/95N1labels/94namedmembers plus separate妖;91necessarysupportword"
        "additions. " + publication["limits"] +
        " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
    )
    publication["nextAction"] = next_action
    p["batch063PublicationCheckpoint"] = publication
    p.update(
        checkpoint=398, status="continue", stage="batch-063-published-verified-before-064",
        lastPublishedCommit=head, remainingAdditions=1138, blocker=None, nextAction=next_action,
    )
    p["activeExecution"].update(
        status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
        recordedAt=datetime.now().astimezone().isoformat(),
        result="SAME063 signed combined-tree acceptance and terminal publication verified;368Python/reverified394Android4/396native2/allsourcebaseline/readings/twopairs/strokes/fonts;greenCI8317publichashes/ownerissue. HistoricalClaude063-P1 explicit, supervised remediation not retroactive strictacceptance. No064/secondrunner.",
    )
    p["execution398CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
    p["execution398StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1138source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
    original = load(C / "execution-398-starting-progress.json")
    allowed = {"activeExecution", "stage", "nextAction", "checkpoint", "status",
               "lastPublishedCommit", "remainingAdditions", "blocker", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    verification = {
        "schemaVersion": 1, "execution": 398, "checkpoint": 398, "batch": "063",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingAndRuntimeUnchanged": True,
        "freshPythonTestsPassed": 368, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8317,
        "originalArchiveGuardsUnchanged": True, "allOriginalHistoricalKeysPreservedExactly": True,
        "oldTopLevelKeys": len(original), "currentTopLevelKeys": len(p),
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "globalIdentityUnchanged": True, "publishedAdditions": 90, "remainingAdditions": 1138,
        "strictInitialProcessContractAccepted": False, "strictHistoricalProcessContractAccepted": False,
        "prospectiveSupervisedRemediationAccepted": True, "phoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": datetime.now().astimezone().isoformat(),
    }
    assert not (C / "execution-398-final-verification.json").exists()
    save(C / "execution-398-final-verification.json", verification)
    save(C / "batch-063-publication-checkpoint.json", publication)
    for key in ("activeExecution", "execution398CoordinatorCheckpoint", "batch063PublicationCheckpoint"):
        p[key]["verification"] = copy.deepcopy(verification)
    print(json.dumps(verification, ensure_ascii=False, indent=2))


def main():
    mode = sys.argv[1]
    p = load(C / "progress.json")
    before = copy.deepcopy(p)
    assert p["checkpoint"] == 397 and p["batch"] == "063"
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    audit = load(S / "batch-063-acceptance-audit.json")
    if mode == "records":
        records(p, head, audit)
    elif mode == "comment":
        comment(p, head)
    elif mode == "finish":
        finish(p, head)
    else:
        raise ValueError(mode)
    allowed = {"activeExecution", "stage", "nextAction", "batch063PublicationCheckpoint", "checkpoint",
               "status", "lastPublishedCommit", "remainingAdditions", "blocker",
               "execution398CoordinatorCheckpoint", "unmetAcceptanceGates", "execution398StartingState"}
    assert all(p[k] == value for k, value in before.items() if k not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(p["checkpoint"], p["stage"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
