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
D = R / "docs" / "n1-reviews" / "batch-083-publication-581"
L = C / "logs" / "db6cb356-7698-4014-a72c-fafa11be1d7c"
ACCEPTED = "bbe7cb954260d96dbf44c526783aaff184f25bf4"
MAIN = "21a5cb1328aadd437139a6b850f07298a2e2985d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "7cc896f488ae5315046453777aae6768b9ff18e8"
VERSION = "6dfe6a1e287ce5df"
BEFORE = L / "progress-before-581.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".581.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
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
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8376
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    return manifest


def start():
    clean(R, ACCEPTED)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    subprocess.run(["git", "merge-base", "--is-ancestor", MAIN, ACCEPTED], cwd=R, check=True)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 580 and p["batch"] == "083" and p["status"] == "continue"
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 580
    state = {
        "execution": 581, "batch": "083", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": ACCEPTED, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME083 accepted signed owner publication, exact public CI/ZIP and durable ledgers/checkpoint only; no084 or new reviews/native absent change.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, complete approved issue and final580 inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live launcher19008 verified in ancestry; parent owns lock throughout child lifetime; no child lock access.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-581.json", state)
    p["execution581StartingState"] = state
    p["stage"] = "batch-083-publication-in-progress"
    p["nextAction"] = state["scope"]
    save(C / "progress.json", p)
    evidence = load(S / "execution-580.json")
    assert sha(S / "execution-580.json") == p["execution580CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTests"]["executed"] == 372 and evidence["pythonTests"]["passed"]
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        raw = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt["sourceSha256"], path
    for report in evidence["inheritedAcceptance"]["reviewReports"]:
        assert report["exitCode"] == 0
        assert sha(R / "docs" / "n1-reviews" / report["report"]) == report["reportSha256"]
    assert all(case["status"] == 0 for case in evidence["inheritedAcceptance"]["nativeTerminalCases"])
    assert load(S / "batch-083-progress.json")["reviewClosed"] == ["凌"]
    assert load(R / "docs" / "n1-reviews" / "batch-083-reconciliation.json")["actionableRemainingFindings"] == 0
    runtime()
    save(L / "prepublication-gate-581.json", {
        "acceptedHead": ACCEPTED, "freshMain": MAIN, "signature": "G",
        "everyRuntimeHashAndManifestReverified": 8376, "evidence580ReceiptsReverified": len(evidence["receipts"]),
        "reviewReportsReverified": 6, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "parentLockTouched": False,
    })
    print("Starting scope persisted; signed acceptance receipts and all runtime hashes reverified.")


def public(phase, head):
    clean(R, head)
    clean(A, APP)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-083-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8376 and archive["manifestEqual"]
    assert all(archive[k] for k in ("allPublishingBudgetsPassed", "contributorEvidenceExcluded",
                                   "perFileLimitsAndSafePathsPassed"))
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    return ci, archive


def records():
    ci, archive = public("accepted", ACCEPTED)
    assert not (S / "batch-083-publication.json").exists()
    assert not D.exists()
    D.mkdir()
    p = load(C / "progress.json")
    before = load(BEFORE)
    evidence = load(S / "execution-580.json")
    ledger = load(S / "batch-083-progress.json")
    manifest = runtime()
    kanji = list((R / "kanji").glob("*.md"))
    counts = {
        "batchPublishedAdditions": 1, "projectPublishedAdditions": 110, "remainingAdditions": 1118,
        "currentKanji": len(kanji), "currentWords": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum("jlpt: 1\n" in x.read_text(encoding="utf-8") for x in kanji),
        "namedSourceMembersPresent": 114, "separateExceptionPreserved": "妖",
        "batchNewNecessarySupportWords": 2, "projectNewNecessarySupportWords": 110,
        "batchChangedReusedArticles": 0, "allMappedReciprocalPairs": 2,
        "mappedDirectedLinks": 4, "activatedBaselinePairs": 0,
    }
    assert counts["currentKanji"] == 1095 and counts["currentWords"] == 5052 and counts["n1Labelled"] == 115
    named = set(load(C / "inputs" / "n1-kanji-source-20261102.json"))
    assert len(named) == 1232 and len(named & {x.stem for x in kanji}) == 114
    publication = {
        "schemaVersion": 1, "execution": 581, "batch": "083", "membership": ["凌"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": MAIN,
        "authoredSnapshot": before["batch083RuntimeDraft"]["savedCommit"],
        "initialReviewedTeachingSnapshot": "4b8bfcc4bc4fff4c73185a8cc6c27d4cb5736efc",
        "reviewedTeachingSnapshot": TEACHING,
        "correctedTextualSnapshot": before["execution576CoordinatorCheckpoint"]["savedCommit"],
        "freshAndroidSnapshot": before["execution577CoordinatorCheckpoint"]["savedCommit"],
        "nativeEnvelopeSnapshot": "867fe8bef228145ef0a6e48690941b0a0aa50336",
        "nativeEvidenceSnapshot": before["execution578CoordinatorCheckpoint"]["savedCommit"],
        "visualClosureSnapshot": before["execution579CoordinatorCheckpoint"]["savedCommit"],
        "latestMainIntegrated": MAIN, "acceptedCommit": ACCEPTED,
        "integratedCommit": ACCEPTED, "publishedCommit": ACCEPTED,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-083-reconciliation.json",
        "visualRecord": "../n1-reviews/batch-083-visual-reconciliation.json",
        "combinedAcceptanceRecord": "execution-580.json",
        "validation": evidence["sourceAudit"], "pythonTestsPassed": 372,
        "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive, "counts": counts,
        "contentVersion": manifest["contentVersion"],
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": evidence["inheritedAcceptance"]["inheritedLimits"],
        "publicationClarification": "The previously outstanding publication/combined checks in historical limitations are now verified by this record; all linguistic/process/native/read-depth/phone limitations remain unchanged.",
        "nextAction": "Verify terminal evidence commit CI/exact public ZIP/ownerissue60; yield before084.",
    }
    save(S / "batch-083-publication.json", publication)
    ledger["prePublicationCheckpoint581"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["凌"], publishedAdditions=110,
                  remainingAdditions=1118, publishedCommit=ACCEPTED, runtimePublished=True,
                  publicationRecord="batch-083-publication.json", pendingGates=[],
                  nextAction=publication["nextAction"])
    save(S / "batch-083-progress.json", ledger)
    execution = {
        "schemaVersion": 1, "execution": 581, "batch": "083", "status": publication["status"],
        "startingState": p["execution581StartingState"], "publicationRecord": "batch-083-publication.json",
        "acceptedCommit": ACCEPTED, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-580.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newReviewNativeHostRuns": 0, "limits": publication["limits"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    save(S / "execution-581.json", execution)
    for path in [L / "prepublication-gate-581.json", L / "starting-state-581.json",
                 C / "artifacts" / "batch-083-accepted-ci.json",
                 C / "artifacts" / f"content-{ACCEPTED[:7]}-acceptance.json",
                 C / "verify-batch-002-publication.py", C / "verify-581-publication.ps1",
                 C / "publish-581.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    assert runtime()["contentVersion"] == VERSION
    p["stage"] = "batch-083-accepted-published-awaiting-terminal-evidence"
    p["nextAction"] = publication["nextAction"]
    p["execution581AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Accepted public delivery verified; durable publication ledgers prepared.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-083-publication.json")
    text = f"""Batch **083 (凌)** is published and verified for bounded owner testing, with necessary support articles **凌ぐ (しのぐ)** and **凌駕 (りょうが)**. No reused article changed.

Authored/initial-reviewed snapshot `{publication['initialReviewedTeachingSnapshot']}`; corrected teaching `{TEACHING}`; corrected textual closure `{publication['correctedTextualSnapshot']}`; visual closure `{publication['visualClosureSnapshot']}`. Fresh main `{MAIN}` remained ancestral; normally signed accepted/integrated publication `{ACCEPTED}`, terminal evidence/remote main `{head}`. Owner `stop-cran` normal fast-forward pushes; global account unchanged.

Both independent initial model families **Claude Opus5.5 / GPT6.1Sol** and their serial original-session choice/visual confirmations retained. **083-NATIVE-574-CHOICE** is resolved by corrected production defaults `[准, 冶, 冴]`, exact N1/All default-four assertions and corrected native/visual evidence; original failed574 receipts remain immutable. 冴's genuine skill/excel-at secondary sense is preserved: actual displayed clear/sharp-minded is wrong for 凌, not a universal disjointness rule or certification of custom/random/partial/padded/larger/reverse pools.

Combined-tree **372 Python tests**, validator0errors, vocabulary consistency, fresh manifest, frozen-source re-extraction, original985kanji/4942words/985strokes with explicit inherited narrow exceptions, exact membership, both metadata/curated readings, **two reciprocal pairs/four directions**,17direct word guards and pinned ten-stroke geometry passed. Fresh580 actual-sibling **3 RealContentTest + 1 RareHanTest**, no skips/errors/failures, and corrected578 **two terminal-status0 native cases** reverified, not rerun. Full production ContentSync once:1095kanji/5052words/115N1, zero problems, parser epoch1; both curated りょう/しのぐ persisted independently. Qualified TEST-ONLY Android `{APP}` preserves production `f9b59a2`; not latest app main.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) are green. Both exact immutable public GitHub ZIPs preserve **all8376 runtime hashes** and manifest `{VERSION}`. Terminal archive **{archive['zipEntries']} entries / {archive['compressedBytes']} compressed / {archive['inflatedBytes']} inflated / {archive['retainedBytes']} retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus per-file/media/path guards; contributor evidence excluded.

Published **110/1228 additions;1118 remain**. Collection **1095kanji/5052words/115N1-labelled**,114 named-source members plus separate妖. This batch adds2necessary support words;110project-wide, **not an N1 vocabulary deck**.

All source/reviewer/process/citation/lookup/read-depth/OOM/denial/viewport/font/pool/MLKit limitations remain in `execution-580.json`, original reports and `batch-083-publication.json`. Both visual families received31distinct original-path payloads representing56captures/25byte aliases; returned900x2000 from1080x2400, not original-resolution/equal-retained-context or fallback-face certification. Word-body headings aboveMeaning were not directly captured; source and heading-existence assertions supplied, appbar/readings/wholewords visible. Finaltree is loading state, not settledUI acceptance; cleanup-timing hypothesis unverified. All30Han/fourfamilies readable within inspected scope; prior40fallback targets inherited. SystemBack/offline/links depend additionally on fixture/terminal evidence. Ten injectedreference strokes/shape-only feedback/giveup recall/grade-on-Next are **not human handwriting/successful recall/MLKit download/phone evidence**.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; old clients ignore curation. **Physical-phone/general-release/whole-set acceptance outstanding**. Parent19008 retains runner.lock; no child lock access or historical session helper access. Checkpoint581 persists `continue` and yields before084; no next batch or second runner.

Durable records: `docs/n1-sources/batch-083-publication.json`, `execution-581.json`, original source/review/failed574/corrected578/579/580 receipts.
"""
    target = C / "batch-083-publication-comment.txt"
    assert not target.exists()
    target.write_text(text, encoding="utf-8")
    save(L / "terminal-publication-581.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal public CI/archive verified; exact owner issue body prepared.")


def finalize_records():
    ledger = load(S / "batch-083-progress.json")
    assert ledger["published"] == ["凌"]
    named = set(load(C / "inputs" / "n1-kanji-source-20261102.json"))
    assert len(named) == 1232 and len(named & {x.stem for x in (R / "kanji").glob("*.md")}) == 114
    review_path = R / "docs" / "n1-reviews" / "batch-083-reconciliation.json"
    review = load(review_path)
    review["prePublicationState581"] = {
        k: copy.deepcopy(review[k]) for k in ("status", "runtimePublished", "limits")
    }
    review.update(status="published-verified-bounded-owner-testing", runtimePublished=True,
                  publicationRecord="../n1-sources/batch-083-publication.json")
    review["publicationClarification"] = (
        "Publication is verified by execution581; historical scoped review/native/read-depth limitations and "
        "original complete reports remain unchanged. This is not a fresh linguistic review.")
    save(review_path, review)
    for row in ledger["supportMappings"]:
        row["status"] = "published-verified-bounded-owner-testing"
    ledger["fontDisposition"] = (
        "Corrected578 native and579 original-family visual evidence accepted for all30Han/fourfamilies "
        "within inspected scope; fallback-face/original-resolution/unseen headings/phone limits retained. "
        "See execution-580.json and batch-083-publication.json; physical-phone acceptance outstanding.")
    ledger["choiceCorrection"]["status"] = "resolved-textual-native-bounded-visual-published"
    ledger["choiceCorrection"]["runtimeAcceptance"] = (
        "Corrected578 two terminal0 cases and579 serial original-family visual confirmations accepted; "
        "original failed574 immutable. Exact default-four N1/All scope only.")
    ledger["choiceCorrection"]["confirmation"]["status"] = "resolved"
    ledger["choiceCorrection"]["confirmation"]["nativeEvidence"] = "execution-578.json"
    ledger["choiceCorrection"]["confirmation"]["visualEvidence"] = "execution-579.json"
    save(S / "batch-083-progress.json", ledger)
    receipts = []
    for name in ["validate", "manifest", "budget"]:
        source = L / f"{name}-581.txt"
        target = D / source.name
        assert not target.exists()
        shutil.copyfile(source, target)
        receipts.append({"path": target.relative_to(R).as_posix(), "sha256": sha(target),
                         "exitCode": 0, "runtimeManifestUnchanged": True})
    execution = load(S / "execution-581.json")
    execution["terminalLocalValidation"] = receipts
    execution["diagnostics"] = [
        "Published ledgers preserve entire prePublicationCheckpoint581 and prior nested receipts as historical; "
        "current support/font/choice dispositions explicitly updated to verified acceptance.",
    ]
    save(S / "execution-581.json", execution)
    shutil.copyfile(Path(__file__), D / Path(__file__).name)
    runtime()
    print("Current dispositions and terminal local validation archived; historical receipts unchanged.")


def finish(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-083-publication.json")
    receipt = load(C / "batch-083-publication-issue-receipt.json")
    text = (C / "batch-083-publication-comment.txt").read_text(encoding="utf-8")
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        encoding="utf-8"))
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"]
    assert text.replace("\r\n", "\n").rstrip() == remote["body"].replace("\r\n", "\n").rstrip()
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"],
                                   encoding="utf-8").strip() == "romanko-ms"
    ledger = load(S / "batch-083-progress.json")
    assert ledger["published"] == ledger["reviewClosed"] == ledger["membership"] == ["凌"]
    assert not (S / "batch-084-progress.json").exists()
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"])
    inherited = " ".join(publication["limits"])
    next_action = (
        f"Batch083 accepted/published/verified at{head}; yield before084. Next fresh coordinator execute ONE "
        "risk/evidence-bounded084 source-preparation checkpoint from exact remaining frozen source rows, below15; "
        "do not reopen accepted083 or access optional historical session helpers. Read complete authorizedrequest/"
        "finalcheckpoint/fullapprovedissue; preserve FULLlivehistory. Fresh dedicated signed cleanheads/main and "
        "liveparent ancestry; parent19008 retainsrunner.lock, children never reacquire/delete/unlock. "
        "Use approvedcontrolhelpers/committedsources/frozeninputs; preserve/report/yield actualnew denial/signinghang/"
        "uncertainownership, noworkaround. All original fullfamily/readingallocation/usefulness/baseline/fullmetadata/"
        "curatedkeys/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/two serialblindfamilies/"
        "originalsessionreconciliation/non-skippedAndroid/native/combinedmain/normalsigning/ownerfastforward/"
        "terminalgreenCI/EVERYimmutablepublicZIPhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
        "perfilemediasafepaths/verifiedownerissue gates apply. Published110/1228;1118remaining;1095kanji5052words"
        "115N1labels114namedmembers+separate妖;110necessarysupportsNOTN1vocabulary. "
        "083 correctedchoice/readings/twopairs/tenstrokes accepted;372Python/fresh580HOST4/corrected578native2/"
        "originalfamilyvisuals/accepted+terminalCI8376publichashesverified, not rerun. "
        "Publication/currentmain items formerly outstanding in historical limits now verified; ALL other limits: "
        + inherited + " Physicalphone/generalrelease/whole-set outstanding; projectincomplete; no084started."
    )
    publication["nextAction"] = next_action
    save(C / "batch-083-publication-checkpoint.json", publication)
    save(L / "batch-083-publication-checkpoint.json", publication)
    p = load(C / "progress.json")
    before = load(BEFORE)
    p["execution581StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 581, "checkpoint": 581, "batch": "083",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "acceptedCommit": ACCEPTED, "acceptedCi": publication["ci"]["databaseId"],
        "terminalCi": ci["databaseId"], "bothImmutablePublicArchivesVerified": True,
        "runtimeHashesPerArchive": 8376, "reviewedRuntimeBytesUnchanged": True,
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-083-published-verified-before-084",
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": head, "nextAction": next_action, "blocker": None,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution581CoordinatorCheckpoint"] = verification
    p["batch083PublicationCheckpoint"] = publication
    p["batch083PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-083-publication-comment.txt"), "verified": True}
    p.update(checkpoint=581, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1118, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1118 source-bounded additions not authored/review-closed/published;later batches retain all original source/review/reading/link/baseline/font/Android/native/currentmain/CI/publicZIP gates."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-verification-581.json", verification)
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
    elif mode == "finalize-records":
        finalize_records()
    elif mode == "finish":
        finish(sys.argv[2])
    else:
        raise ValueError(mode)
