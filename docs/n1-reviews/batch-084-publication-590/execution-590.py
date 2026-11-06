"""Batch 084 publication checkpoint; the live parent retains runner.lock."""
import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
D = R / "docs" / "n1-reviews" / "batch-084-publication-590"
L = C / "logs" / "f2ec9d32-d497-4f17-80e8-e775b928f778"
ACCEPTED = "859116da55b84a38a0ca9c4ca210255b7c9772eb"
MAIN = "106a36dd9617a0d0826a512da82ee1ed9bf9e34d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "030b144a6aeefc6fe77f76683219832db91bef4f"
VERSION = "8c3fa3ee6f2b1ebc"
BEFORE = L / "progress-before-590.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value, ascii=True):
    temporary = path.with_suffix(path.suffix + ".590.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=ascii, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8408
    assert not git("diff", ACCEPTED, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", TEACHING, "--", "kanji/凜.md", "words/凜.md", "strokes/凜.json")
    return manifest


def start():
    clean(R, ACCEPTED)
    clean(A, APP)
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running" and runner["sessionId"] == L.name
    assert git("rev-parse", "origin/main") == MAIN
    subprocess.run(["git", "merge-base", "--is-ancestor", MAIN, ACCEPTED], cwd=R, check=True)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 589 and p["batch"] == "084" and p["status"] == "continue"
    if not BEFORE.exists():
        shutil.copyfile(C / "progress.json", BEFORE)
    else:
        original = load(BEFORE)
        assert original["checkpoint"] == 589 and original["batch"] == "084"
        assert p["execution590StartingState"] == load(L / "starting-state-590.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 589
    state = {
        "execution": 590, "batch": "084", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": ACCEPTED, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME084 signed owner publication, exact public CI/ZIP and durable ledgers/checkpoint only; no085 or fresh reviewer/native/HOST absent change.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire file loaded and checkpoint decoded; operative contract, complete approved issue and final589 inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial tail display hit local cp1252 encoding; final checkpoint subsequently read directly in full."},
        "runnerLockRole": "Live parent19008 verified in coordinator ancestry; no child lock open/acquisition/delete/unlock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    if (L / "starting-state-590.json").exists():
        state = load(L / "starting-state-590.json")
    else:
        save(L / "starting-state-590.json", state)
    p["execution590StartingState"] = state
    p.update(stage="batch-084-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    evidence = load(S / "execution-589.json")
    assert sha(S / "execution-589.json") == p["execution589CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"], path
    for report in evidence["inheritedAcceptance"]["reviewReports"]:
        assert report["exitCode"] == 0 and report["serialTimingReverified"]
        assert sha(R / "docs" / "n1-reviews" / report["report"]) == report["reportSha256"]
    assert all(case["status"] == 0 for case in evidence["inheritedAcceptance"]["nativeTerminalCases"])
    assert load(S / "batch-084-progress.json")["reviewClosed"] == ["凜"]
    for name, key in (
        ("batch-084-reconciliation.json", "actionableRemainingTeachingFindings"),
        ("batch-084-visual-reconciliation.json", "actionableRemainingFindings"),
    ):
        assert load(R / "docs" / "n1-reviews" / name)[key] == 0
    runtime()
    save(L / "prepublication-gate-590.json", {
        "acceptedHead": ACCEPTED, "freshMain": MAIN, "signature": "G",
        "everyRuntimeHashAndManifestReverified": 8408,
        "evidence589ReceiptsReverified": len(evidence["receipts"]),
        "reviewReportsReverified": 8, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "parentLockTouched": False,
        "diagnostic": "First local preflight stopped on an incorrect helper field name before push. Corrected to the actual textual actionableRemainingTeachingFindings and visual actionableRemainingFindings fields; both zero. No acceptance gate relaxed.",
    })
    print("Starting scope persisted; signed acceptance receipts and all8408 runtime hashes reverified.")


def public(phase, head):
    clean(R, head)
    clean(A, APP)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-084-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8408 and archive["manifestEqual"]
    assert all(archive[k] for k in ("allPublishingBudgetsPassed", "contributorEvidenceExcluded",
                                   "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    return ci, archive


def records():
    ci, archive = public("accepted", ACCEPTED)
    assert not (S / "batch-084-publication.json").exists() and not D.exists()
    D.mkdir()
    p = load(C / "progress.json")
    before = load(BEFORE)
    evidence = load(S / "execution-589.json")
    ledger = load(S / "batch-084-progress.json")
    manifest = runtime()
    kanji = list((R / "kanji").glob("*.md"))
    named = set(load(C / "inputs" / "n1-kanji-source-20261102.json"))
    counts = {
        "batchPublishedAdditions": 1, "projectPublishedAdditions": 111, "remainingAdditions": 1117,
        "currentKanji": len(kanji), "currentWords": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum("jlpt: 1\n" in x.read_text(encoding="utf-8") for x in kanji),
        "namedSourceMembersPresent": len(named & {x.stem for x in kanji}),
        "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 1,
        "projectNewNecessarySupportWords": 111, "batchChangedReusedArticles": 0,
        "allMappedReciprocalPairs": 1, "mappedDirectedLinks": 2, "activatedBaselinePairs": 0,
        "separateEarlierLevelSourceMembers": evidence["earlierLevelSourceMemberDisposition"],
        "earlierPlacementsCountedAsIssue60AcceptedBatches": False,
    }
    assert len(named) == 1232 and counts["namedSourceMembersPresent"] == 121
    assert counts["currentKanji"] == 1107 and counts["currentWords"] == 5060 and counts["n1Labelled"] == 116
    publication = {
        "schemaVersion": 1, "execution": 590, "batch": "084", "membership": ["凜"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": TEACHING, "initialReviewedTeachingSnapshot": TEACHING,
        "reviewedTeachingSnapshot": TEACHING,
        "textualClosureSnapshot": before["execution584CoordinatorCheckpoint"]["savedCommit"],
        "freshAndroidSnapshot": before["execution585CoordinatorCheckpoint"]["savedCommit"],
        "nativeEnvelopeSnapshot": before["execution586CoordinatorCheckpoint"]["savedCommit"],
        "nativeEvidenceSnapshot": before["execution587CoordinatorCheckpoint"]["savedCommit"],
        "visualClosureSnapshot": before["execution588CoordinatorCheckpoint"]["savedCommit"],
        "combinedContentHead": evidence["combinedContentHead"], "latestMainIntegrated": MAIN,
        "acceptedCommit": ACCEPTED, "integratedCommit": ACCEPTED, "publishedCommit": ACCEPTED,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-084-reconciliation.json",
        "visualRecord": "../n1-reviews/batch-084-visual-reconciliation.json",
        "combinedAcceptanceRecord": "execution-589.json", "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": manifest["contentVersion"],
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": evidence["inheritedAcceptance"]["inheritedLimits"],
        "publicationClarification": "Historical pending combined-main/publication checks are now verified here. All linguistic/process/native/read-depth/pool/phone limitations retained. Native import remains premerge version74b87b47347b78c1, not a combined-version native import; fresh combined HOST4 accepted.",
        "nextAction": "Verify terminal evidence commit CI/exact public ZIP/ownerissue60; yield before085.",
    }
    save(S / "batch-084-publication.json", publication)
    ledger["prePublicationCheckpoint590"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["凜"], publishedAdditions=111,
                  remainingAdditions=1117, publishedCommit=ACCEPTED, runtimePublished=True,
                  publicationRecord="batch-084-publication.json", pendingGates=[],
                  nextAction=publication["nextAction"])
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    ledger["publicationClarification"] = publication["publicationClarification"]
    save(S / "batch-084-progress.json", ledger)
    review_path = R / "docs" / "n1-reviews" / "batch-084-reconciliation.json"
    review = load(review_path)
    review["prePublicationState590"] = {k: copy.deepcopy(review[k]) for k in ("status", "runtimePublished", "limits")}
    review.update(status=publication["status"], runtimePublished=True,
                  publicationRecord="../n1-sources/batch-084-publication.json",
                  publicationClarification=publication["publicationClarification"])
    save(review_path, review, ascii=False)
    execution = {
        "schemaVersion": 1, "execution": 590, "batch": "084", "status": publication["status"],
        "startingState": p["execution590StartingState"], "publicationRecord": "batch-084-publication.json",
        "acceptedCommit": ACCEPTED, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-589.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newReviewNativeHostRuns": 0, "limits": publication["limits"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    receipts = []
    for name, args in (
        ("validate", ["tools\\validate.py"]), ("manifest", ["tools\\build_manifest.py"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = D / f"{name}-590.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args], cwd=R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    execution["terminalLocalValidation"] = receipts
    save(S / "execution-590.json", execution)
    for path in [L / "prepublication-gate-590.json", L / "starting-state-590.json",
                 C / "artifacts" / "batch-084-accepted-ci.json",
                 C / "artifacts" / f"content-{ACCEPTED[:7]}-acceptance.json",
                 C / "verify-batch-002-publication.py", C / "verify-590-publication.ps1",
                 C / "publish-590.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-084-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution590AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Accepted public delivery verified; durable publication ledgers and local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-084-publication.json")
    text = f"""Batch **084 (凜)** is published and verified for bounded owner testing, with necessary support **凜 (りん)**. One reciprocal pair/two directions; no reused article changed.

Authored and reviewed teaching `{TEACHING}`; textual closure `{publication['textualClosureSnapshot']}`; visual closure `{publication['visualClosureSnapshot']}`. Normal latest-main merge `{publication['combinedContentHead']}` integrated `{MAIN}`; generated manifest was the only conflict. Reviewed batch bytes and all29 incoming runtime additions/43 changed public-main files preserved exactly. Normally signed accepted publication `{ACCEPTED}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global account unchanged.

Both blind initial families **Claude Opus5.5 / GPT6.1Sol**, original-session textual confirmations, serial visual confirmations and native-pixel detail addenda retained. No actionable scoped teaching finding. C1 spelling-priority note optional, C2 extra word-guard hypothesis withdrawn, C3 default-four concern resolved; larger/custom/random/partial/padded/reverse pools remain unverified. Default N1/All builder exact IDs and labels 凜/准/冗/凹 supplied; actual N1 UI inspected, not All UI or universal quiz safety.

Combined-tree **372 Python tests**, validator0errors, vocabulary consistency, fresh manifest, frozen-source/31-family re-extraction, original985kanji/4942words/985strokes with inherited narrow exceptions, membership, both metadata dispositions, sole curatedリン/kun[],20direct guards, pinned15-stroke geometry and fresh combined **3 RealContentTest + 1 RareHanTest** passed without skips/failures/errors. No new reviewer/HOST/native run here. Inherited587 **two native terminal-status0 cases** accepted: production ContentSync full archive once,1096kanji/5053words/116N1,zero problems/epoch1/version74b87b47347b78c1; Full/Lite fullリン/きびし.い retained, onlyりん offered and persistedGood. **Native import was premerge, not combined-version native import**. Combined HOST4 imported actual combined archive; disjoint lower-level main changes left N1 pool/routes/readings/strokes unchanged. Qualified TEST-ONLY Android `{APP}` preserves production f9b59a2, not latest app main.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable public ZIPs preserve **all8408 runtime hashes**, manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus per-file/media/path guards; contributor evidence excluded.

Published **111/1228 additions;1117 remain**. Collection **1107kanji/5060words/116N1-labelled/121named-source members plus separate妖**. Six separate public-main source members 保/案/派/第/策/結 retain earlier N2 levels and are **not counted as issue60 accepted additions**; do not duplicate them. This batch adds one necessary support article;111project-wide, **not an N1 vocabulary deck**.

All original source/lookup/process/read-depth/denial/OOM/native/pool limits retained in `execution-589.json` and `batch-084-publication.json`. Both visual families received25 distinct original PNGs representing42captures;1080x2400 fullframes returned900x2000. Lossless632x760 native-pixel crop resolved panel凜禾-bottom/凛示-bottom recognition; no every-fine-stroke/smaller-body/otherdensity/fallback-face/physical-phone certification. All28Han/fourfamilies recognized within captured scope. Onepair/articles/SystemBack/offline/selection supplied by fixtures/terminal as well as pixels. Fifteen injected reference strokes, trace/giveup recall and persisted grade are **not human handwriting/MLKit recognition/model download/phone evidence**. Source-only kun in reference/feedback and optional grade/download wording are not established content or prerequisite defects.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; old clients ignore curation. **Physical-phone/general-release/whole-set acceptance outstanding**. Parent19008 retains runner.lock; no child lock or optional historical-session helper access. Checkpoint590 persists `continue` and yields before085; no next batch or second runner.

Durable evidence: `docs/n1-sources/batch-084-publication.json`, `execution-590.json`, original584textual/585HOST/586fixture/587native/588visual/589combined records.
"""
    target = C / "batch-084-publication-comment.txt"
    assert not target.exists()
    target.write_text(text, encoding="utf-8")
    save(L / "terminal-publication-590.json", {"head": head, "ci": ci, "archive": archive,
                                             "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; exact owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-084-publication-issue-receipt.json")
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        encoding="utf-8"))
    text = (C / "batch-084-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"]
    assert text.replace("\r\n", "\n").rstrip() == remote["body"].replace("\r\n", "\n").rstrip()
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], encoding="utf-8").strip() == "romanko-ms"
    assert not (S / "batch-085-progress.json").exists()
    ledger = load(S / "batch-084-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == ["凜"]
    publication = load(S / "batch-084-publication.json")
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"])
    next_action = (
        f"Batch084 accepted/published/verified at{head}; yield before085. Next coordinator ONE bounded085 "
        "source-preparation checkpoint from exact remaining frozen rows below15. Read fullrequest/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify dedicated whollyclean signedheads/freshmain/liveparent "
        "ancestry/session. Parent19008 retainsrunner.lock: no child acquire/delete/unlock. Approvedcontrolhelpers/"
        "committedsourcepackets/frozeninputs only, no optional historicalsessionrecipes. Preserve/report/yield "
        "actualnewdenial/signinghang/uncertainownership; no workaround. All original fullfamily/readingallocation/"
        "usefulness/baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "two serialblinddifferentfamilies/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normal signing/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/original18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published111/1228;1117acceptance-remainder;1107kanji5060words116N1labels121namedmembers+separate妖; "
        "111necessarysupportsNOTN1vocabulary. Six separate main source members保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel, account dispositions in later membership audits. "
        "084unchanged030b144ateaching, combined40305851+106a36dd version8c3fa3ee6f2b1ebc/8408hashes;372Python/"
        "fresh589HOST4/inherited587native2/original588visuals plus detail/accepted+terminalCI+ZIP/ownerissueverified. "
        "No freshreview/native/HOST reruns here. Native import remains PREMERGE74b87b47347b78c1/1096kanji5053words"
        "116N1/zeroProblems/epoch1; not combinednativeimport. CombinedHOST4 imports actualfullcombined; disjoint"
        "lowerlevelpublicmain leftN1pool/routes unchanged. C1optional/C2withdrawn/C3defaultresolved largerpools"
        "unverified. Historical pending publication/combinedchecks now verified; all other source/process/readdepth/"
        "denial/OOM/viewport/fallbackface/bodyfine-stroke/MLKit/pool limitations retained: "
        + " ".join(publication["limits"])
        + " CompatibleAndroidf9b59a2+required. Physicalphone/generalrelease/whole-setoutstanding; projectincomplete. "
        "No085started, authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease."
    )
    publication["nextAction"] = next_action
    save(C / "batch-084-publication-checkpoint.json", publication)
    save(L / "batch-084-publication-checkpoint.json", publication)
    p = load(C / "progress.json")
    before = load(BEFORE)
    p["execution590StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 590, "checkpoint": 590, "batch": "084",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": ACCEPTED,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8408,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-084-published-verified-before-085",
        "publishedAdditions": 111, "remainingAdditions": 1117, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution590CoordinatorCheckpoint"] = verification
    p["batch084PublicationCheckpoint"] = publication
    p["batch084PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-084-publication-comment.txt"), "verified": True}
    p.update(checkpoint=590, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1117, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1117 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-verification-590.json", verification)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({k: v for k, v in verification.items() if k != "nextAction"}, indent=2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "start":
        start()
    elif mode == "records":
        records()
    elif mode == "comment":
        comment(sys.argv[2])
    elif mode == "finish":
        finish(sys.argv[2])
    else:
        raise ValueError(mode)
