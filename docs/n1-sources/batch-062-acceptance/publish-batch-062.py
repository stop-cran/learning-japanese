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
D = S / "batch-062-acceptance"
TEACHING = "38ab6072d2041325142c54cf54be5d126928eb31"
VERSION = "545c56b5d4b4e8ef"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution388.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree,
                                   text=True, encoding="utf-8").strip()


def verified_archive(phase, head):
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-062-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8314
    assert all(archive[k] for k in ("manifestEqual", "allPublishingBudgetsPassed",
                                   "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    return ci, archive


def records(p, head, audit):
    ci, archive = verified_archive("accepted", head)
    assert not (S / "batch-062-publication.json").exists()
    publication = {
        "schemaVersion": 1, "execution": 388, "batch": "062",
        "status": "published-verified-bounded-owner-testing", "membership": ["俸"],
        "baseCommit": audit["baseCommit"],
        "authoredSnapshot": p["batch062DraftCheckpoint"]["savedCommit"],
        "initialReviewedTeachingSnapshot": TEACHING, "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": p["batch062TextualReviewCheckpoint"]["savedCommit"],
        "freshAndroidSnapshot": p["batch062AndroidArchivalCheckpoint"]["savedCommit"],
        "nativePreparationSnapshot": p["batch062NativePreparationCheckpoint"]["savedCommit"],
        "nativeEvidenceSnapshot": p["batch062NativeExecutionCheckpoint"]["savedCommit"],
        "visualClosureSnapshot": p["batch062NativeVisualCheckpoint"]["savedCommit"],
        "latestMainIntegrated": audit["latestMainIntegrated"],
        "acceptedCommit": head, "integratedCommit": head, "publishedCommit": head,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward, no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-062-reconciliation.json",
        "nativeRecord": "../n1-reviews/batch-062-native-acceptance.json",
        "strictInitialProcessContractAccepted": False, "strictHistoricalProcessContractAccepted": False,
        "prospectiveSupervisedRemediationAccepted": True,
        "validation": audit, "ci": ci, "immutablePublicArchive": archive,
        "counts": {
            "batchPublishedAdditions": 1, "projectPublishedAdditions": 89, "remainingAdditions": 1139,
            "currentKanji": 1074, "currentWords": 5032, "n1Labelled": 94,
            "namedSourceMembersPresent": 93, "separateExceptionPreserved": "妖",
            "batchNewNecessarySupportWords": 1, "projectNewNecessarySupportWords": 90,
            "batchChangedReusedArticles": 1, "requiredReciprocalPairs": 2, "activatedBaselinePairs": 0,
        },
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "limits": audit["limits"], "nextAction": "Verify terminalCI/publicZIP/ownerissue60; yield before063.",
    }
    save(S / "batch-062-publication.json", publication)
    ledger = load(S / "batch-062-progress.json")
    ledger["prePublicationCheckpoint"] = {
        key: copy.deepcopy(ledger[key]) for key in ("status", "nextAction", "limits", "fontDisposition", "supportMappings")
    }
    ledger.update(
        status=publication["status"], published=ledger["membership"],
        publishedAdditions=89, remainingAdditions=1139, publishedCommit=head,
        publicationRecord="batch-062-publication.json", acceptanceRecord="batch-062-acceptance-audit.json",
        pendingGates=[], nextAction=publication["nextAction"], limits=audit["limits"],
        fontDisposition={**ledger["fontDisposition"], "pending": "Physical-phone/general-release acceptance outstanding.",
                         "acceptedEvidence": "docs/n1-reviews/batch-062-native-acceptance.json"},
    )
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(S / "batch-062-progress.json", ledger)
    execution = load(S / "execution-388.json")
    execution.update(
        status=publication["status"], publicationRecord="batch-062-publication.json",
        publishedAdditions=89, remainingAdditions=1139,
        publication={"acceptedCommit": head, "ciRun": ci["databaseId"], "counts": publication["counts"]},
    )
    save(S / "execution-388.json", execution)
    for path in (
        C / "artifacts" / "batch-062-accepted-ci.json",
        C / "artifacts" / f"content-{head[:7]}-acceptance.json",
        C / "verify-batch-002-publication.py", C / "verify-batch-062-publication.ps1",
        C / "push-batch-060.ps1", Path(__file__),
    ):
        assert not (D / path.name).exists()
        shutil.copyfile(path, D / path.name)
    receipts = []
    for name, arguments in (
        ("validate", ["tools\\validate.py"]), ("manifest", ["tools\\build_manifest.py"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = D / f"execution-388-terminal-{name}.txt"
        assert not path.exists()
        with path.open("wb") as stream:
            process = subprocess.run([sys.executable, "-X", "utf8", "-B", *arguments],
                                     cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({"command": ["python", "-X", "utf8", "-B", *arguments],
                         "exitCode": process.returncode, "log": path.relative_to(R).as_posix(), "sha256": sha(path)})
        assert process.returncode == 0, path
    save(S / "batch-062-terminal-validation.json", receipts)
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    p["activeExecution"].update(status="accepted-publication-verified-pending-terminal-receipts",
                               acceptedCommit=head, ciRun=ci["databaseId"], verifiedRuntimeHashes=8314)
    p.update(stage="batch-062-accepted-publication-verified-pending-terminal-receipts",
             nextAction=publication["nextAction"])


def comment(p, head):
    ci, archive = verified_archive("terminal", head)
    publication = load(S / "batch-062-publication.json")
    text = f"""Batch **062 (俸)** is published and verified for bounded owner testing, with necessary support **俸給** and one reviewed link in 給.

Authored/reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`; visual closure `{publication['visualClosureSnapshot']}`. Fresh main `{publication['latestMainIntegrated']}` was already ancestral after a normal merge. Normally signed accepted/integrated publication `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global GitHub identity unchanged.

Fresh combined-tree checks: **368 Python tests**, validator, vocabulary consistency (existing pilot coverage 2122/2431, not repaired or claimed complete), manifest freshness, frozen-source/42-family mechanical re-extraction, exact addition membership, baseline metadata/readings/levels/exclusions/strokes, one reading disposition, **two reciprocal pairs/four links**, generated ten-stroke geometry and actual font cmaps. Accepted fresh Android **3 RealContentTest + 1 RareHanTest**, no skips, and **two native terminal-0 cases** independently reverified without reruns. Single full production ContentSync import: 1074 kanji/5032 words/94 N1 labels, zero problems, parser epoch1.

Meaning, sole curated ホウ/no-kun, both pairs/four native transitions, System Back/offline, reference-touch drawing/recall-miss/persisted Draw Again retained. Meaning feedback Back BEFORE Next is not a newly persisted grade; OnGood and DrawAgain are separately asserted. Both original model families' dependent visual confirmations retained; no actionable teaching finding. Historical Claude **062-P1/P2** remain explicit: supervised remediation is **not retroactive strict initial-process acceptance**. Five optional suggestions not adopted. Four font rows readable/distinguishable; unseen pixels/horizontal table crops and actual fallback face remain unverified. Emulator evidence is not physical-phone, MLKit or successful human recall evidence.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) are green. Both immutable GitHub ZIPs preserve **all 8,314 runtime hashes** and manifest `{VERSION}`; terminal ZIP **{archive['zipEntries']:,} entries / {archive['compressedBytes']:,} compressed / {archive['inflatedBytes']:,} inflated / {archive['retainedBytes']:,} retained bytes**, within unchanged 18,000-entry/42-MiB/80-MiB/56-MiB guards. Contributor evidence excluded.

Published **89/1,228 additions; 1,139 remain**. Current collection: **1,074 kanji, 5,032 words, 94 N1-labelled cards, 93 named-source members plus separate 妖**. This batch adds one necessary support word; 90 project-wide, **not an N1 vocabulary deck**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** is required; old clients ignore curation. Physical-phone/general-release and whole-set acceptance remain **outstanding**. Original383 denial/parent exact recovery and qualified host-only heap history retained. Durable evidence: `docs/n1-sources/batch-062-publication.json`, `batch-062-acceptance-audit.json`, `execution-388.json`, original source/review/native records. Checkpoint388 persists `continue` and yields before063; no063/second runner started.
"""
    target = C / "batch-062-publication-comment.txt"
    assert not target.exists()
    target.write_text(text, encoding="utf-8")
    print("Prepared exact terminal publication issue update.")


def finish(p, head):
    ci, archive = verified_archive("terminal", head)
    publication = load(S / "batch-062-publication.json")
    receipt = load(C / "batch-062-publication-issue-receipt.json")
    body = (C / "batch-062-publication-comment.txt").read_text(encoding="utf-8-sig")
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
    assert not (S / "batch-063-progress.json").exists()
    for row in load(S / "batch-062-terminal-validation.json"):
        assert row["exitCode"] == 0 and sha(R / row["log"]) == row["sha256"]
    ledger = load(S / "batch-062-progress.json")
    assert ledger["published"] == ledger["reviewClosed"] == ledger["membership"] == ["俸"]
    publication.update(
        finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
        terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"], nextBatchStarted=False,
    )
    next_action = (
        f"Batch062 accepted/published/verified at {head}; yield before063. Fresh coordinator read complete authorized "
        "request/finalcheckpoint and scoped live keys; preserve FULL live history. Verify dedicated clean signed heads/"
        "latestmain, then ONE risk/evidence-bounded063 below15 from exact remaining frozen source rows. Preserve "
        "baseline identities/levels/fullreadings/order/exclusions and exact虎[酔っ払い]/猿[馬鹿]/丘[坂,山]/"
        "山[川,出,木]reviewedguards. Inspect full applicable dictionary families/necessarysupport/curatedreadings/"
        "allactivated+reciprocalpairs/pinnedstrokes/allnewHanfonts. Two serialblind different-family initials, one "
        "active reviewer/serial internaltools and justified original-session confirmations. Applicable fresh non-skipped"
        "Android/native/combinedmain/normalsigning/ownerfastforward/greenCI/everyimmutablepublicZIPhash/unchangedbudgets. "
        "Public89/1228;1139remaining;1074kanji/5032words/94N1labels/93namedmembers plus separate妖;90necessarysupportword"
        "additions. " + publication["limits"] +
        " No authoragents/concurrentheavywork/secondrunner/signingretry/permissionworkaround. Overalltask incomplete."
    )
    publication["nextAction"] = next_action
    p["batch062PublicationCheckpoint"] = publication
    p.update(
        checkpoint=388, status="continue", stage="batch-062-published-verified-before-063",
        lastPublishedCommit=head, remainingAdditions=1139, blocker=None, nextAction=next_action,
    )
    p["activeExecution"].update(
        status=publication["status"], savedCommit=head, issueUpdate=receipt["html_url"],
        recordedAt=datetime.now().astimezone().isoformat(),
        result="SAME062 signed combined-tree acceptance and terminal publication verified;368Python/reverified384Android4/386native2/allsourcebaseline/readings/twopairs/strokes/fonts;greenCI8314publichashes/ownerissue. HistoricalClaude062-P1/P2 explicit, prospective remediation not retroactive strictacceptance. No063/secondrunner.",
    )
    p["execution388CoordinatorCheckpoint"] = copy.deepcopy(p["activeExecution"])
    p["execution388StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    p["unmetAcceptanceGates"][0] = "Remaining1139source-bounded additions not authored/review-closed/published; subsequent batches require all source/review/reading/link/baseline/font/Android/currentmain/CI/publicZIP gates."
    original = load(C / "execution-388-starting-progress.json")
    allowed = {"activeExecution", "stage", "nextAction", "checkpoint", "status",
               "lastPublishedCommit", "remainingAdditions", "blocker", "unmetAcceptanceGates"}
    assert original.keys() <= p.keys()
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    verification = {
        "schemaVersion": 1, "execution": 388, "checkpoint": 388, "batch": "062",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingAndRuntimeUnchanged": True,
        "freshPythonTestsPassed": 368, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8314,
        "originalArchiveGuardsUnchanged": True, "allOriginalHistoricalKeysPreservedExactly": True,
        "oldTopLevelKeys": len(original), "currentTopLevelKeys": len(p),
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "globalIdentityUnchanged": True, "publishedAdditions": 89, "remainingAdditions": 1139,
        "strictInitialProcessContractAccepted": False, "strictHistoricalProcessContractAccepted": False,
        "prospectiveSupervisedRemediationAccepted": True, "phoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": datetime.now().astimezone().isoformat(),
    }
    assert not (C / "execution-388-final-verification.json").exists()
    save(C / "execution-388-final-verification.json", verification)
    save(C / "batch-062-publication-checkpoint.json", publication)
    for key in ("activeExecution", "execution388CoordinatorCheckpoint", "batch062PublicationCheckpoint"):
        p[key]["verification"] = copy.deepcopy(verification)
    print(json.dumps(verification, ensure_ascii=False, indent=2))


def main():
    mode = sys.argv[1]
    p = load(C / "progress.json")
    before = copy.deepcopy(p)
    assert p["checkpoint"] == 387 and p["batch"] == "062"
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    audit = load(S / "batch-062-acceptance-audit.json")
    if mode in {"pending", "terminal-pending"}:
        phase = "accepted" if mode == "pending" else "terminal"
        p["activeExecution"].update(
            status=f"{phase}-signed-pending-owner-push-ci-public-archive",
            recordedAt=datetime.now().astimezone().isoformat(),
        )
        p["activeExecution"]["acceptedCommit" if phase == "accepted" else "terminalPushedCommit"] = head
        p.update(stage=f"batch-062-{phase}-pending-owner-push-ci-public-archive",
                 nextAction=f"SAME062 verify remote before repeating push; finish {phase}CI/publicZIP/ownerissue60, no063.")
    elif mode == "records":
        records(p, head, audit)
    elif mode == "comment":
        comment(p, head)
    elif mode == "finish":
        finish(p, head)
    else:
        raise ValueError(mode)
    allowed = {"activeExecution", "stage", "nextAction", "batch062PublicationCheckpoint", "checkpoint",
               "status", "lastPublishedCommit", "remainingAdditions", "blocker",
               "execution388CoordinatorCheckpoint", "unmetAcceptanceGates", "execution388StartingState"}
    assert all(p[k] == value for k, value in before.items() if k not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(p["checkpoint"], p["stage"])


if __name__ == "__main__":
    main()
