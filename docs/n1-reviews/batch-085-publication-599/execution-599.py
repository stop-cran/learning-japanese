"""Publish accepted batch085; parent launcher exclusively retains runner.lock."""
import copy
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
D = R / "docs" / "n1-reviews" / "batch-085-publication-599"
L = C / "logs" / "aa18fa02-3f8c-4755-8066-08cccac53157"
HEAD = "10973c302b99840138fc1ec6e2e098d3aad3bac6"
MAIN = "97a16b0027b05c0528d78971dd3b17cce17d8056"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "a7512a5e6ce6d04b271099de834e431436363c3d"
REVIEWED = "29a533800ed0d45e6269991d4a19e3b134057d6a"
VERSION = "0c514711ae8d3212"
BEFORE = L / "progress-before-599.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value, ascii=True):
    temporary = path.with_suffix(path.suffix + ".599.tmp")
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
    assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)


def context():
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    command = (
        "$ids=@();$p=$PID;for($i=0;$i -lt 8 -and $p;$i++){"
        "$r=Get-CimInstance Win32_Process -Filter \"ProcessId=$p\";"
        "if(-not $r){break};$ids+=$r.ProcessId;$p=$r.ParentProcessId};"
        "ConvertTo-Json -InputObject $ids"
    )
    ids = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", command], encoding="utf-8"))
    assert 19008 in ids, ids
    clean(A, APP)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (598, "085", "continue")
    return ids


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8413
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", REVIEWED, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    return manifest


def start():
    ids = context()
    clean(R, HEAD)
    assert git("rev-parse", "origin/main") == MAIN
    subprocess.run(["git", "merge-base", "--is-ancestor", MAIN, HEAD], cwd=R, check=True)
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 598
    state = {
        "execution": 599, "batch": "085", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME085 normal signed owner fast-forward publication, exact public CI/ZIP, durable ledgers and checkpoint. No086; no new native/reviewer/HOST absent change.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, entire approved issue and final598 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial summary print hit cp1252; bounded direct UTF-8 reads followed."},
        "runnerLockRole": "Live parent19008 verified in ancestry/session; no child opens/acquires/deletes/unlocks runner.lock.",
        "artifactPathPreflight": "Approved workspace inputs/control helpers and committed source/review evidence only; no optional historical-session artifact accessed.",
        "ancestryPids": ids, "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-599.json", state)
    p = load(C / "progress.json")
    p["execution599StartingState"] = state
    p.update(stage="batch-085-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    evidence = load(S / "execution-598.json")
    assert sha(S / "execution-598.json") == p["execution598CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        raw = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt["sourceSha256"], path
    for report in evidence["inheritedAcceptance"]["reviewReports"]:
        assert report["exitCode"] == 0 and report["serialTimingReverified"]
        assert sha(R / "docs" / "n1-reviews" / report["report"]) == report["reportSha256"]
    assert len(evidence["inheritedAcceptance"]["nativeTerminalCases"]) == 2
    assert all(c["status"] == 0 for c in evidence["inheritedAcceptance"]["nativeTerminalCases"])
    for name, key in [
        ("batch-085-reconciliation.json", "actionableRemainingTeachingFindings"),
        ("batch-085-visual-reconciliation.json", "actionableRemainingFindings"),
    ]:
        assert load(R / "docs" / "n1-reviews" / name)[key] == 0
    assert load(S / "batch-085-progress.json")["reviewClosed"] == ["凝"]
    runtime()
    save(L / "prepublication-gate-599.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G",
        "runtimeHashesVerified": 8413, "combinedReceiptsVerified": len(evidence["receipts"]),
        "reviewReportsVerified": len(evidence["inheritedAcceptance"]["reviewReports"]),
        "nativeTerminalCasesVerified": 2, "parentLockTouched": False,
        "newReviewerNativeHostRuns": 0,
    })
    print("Starting scope saved; exact signed acceptance and all8413 runtime hashes reverified.")


def verify(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-085-{phase}-ci.json"
    assert not ci_path.exists(), ci_path
    runs = json.loads(subprocess.check_output(
        ["gh", "run", "list", "--repo", "stop-cran/learning-japanese", "--commit", head,
         "--workflow", "Validate content", "--limit", "5", "--json",
         "databaseId,status,conclusion,headSha"], encoding="utf-8"))
    assert runs and runs[0]["headSha"] == head, "Exact CI not yet available; preserve pending checkpoint"
    run = runs[0]
    subprocess.run(["gh", "run", "watch", str(run["databaseId"]), "--repo",
                    "stop-cran/learning-japanese", "--exit-status", "--interval", "10"], check=True)
    ci = json.loads(subprocess.check_output(
        ["gh", "run", "view", str(run["databaseId"]), "--repo", "stop-cran/learning-japanese",
         "--json", "databaseId,status,conclusion,headSha,workflowName,jobs"], encoding="utf-8"))
    save(ci_path, ci)
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    path = C / "artifacts" / f"content-{head[:7]}.zip"
    assert not path.exists(), path
    subprocess.run(["curl.exe", "--fail", "--location", "--silent", "--show-error",
                    f"https://api.github.com/repos/stop-cran/learning-japanese/zipball/{head}",
                    "--output", str(path)], check=True)
    subprocess.run([sys.executable, "-X", "utf8", "-B", str(C / "verify-batch-002-publication.py"),
                    head, str(path), str(path.with_name(path.stem + "-acceptance.json"))], check=True)
    public(phase, head)


def public(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-085-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8413 and archive["manifestEqual"]
    assert all(archive[k] for k in [
        "allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-085-publication.json").exists()
    D.mkdir()
    p = load(C / "progress.json")
    before = load(BEFORE)
    evidence = load(S / "execution-598.json")
    ledger_path = S / "batch-085-progress.json"
    ledger = load(ledger_path)
    named = set(load(C / "inputs" / "n1-kanji-source-20261102.json"))
    cards = list((R / "kanji").glob("*.md"))
    counts = {
        "batchPublishedAdditions": 1, "projectPublishedAdditions": 112, "remainingAdditions": 1116,
        "currentKanji": len(cards), "currentWords": len(list((R / "words").glob("*.md"))),
        "n1Labelled": sum("jlpt: 1\n" in x.read_text(encoding="utf-8") for x in cards),
        "namedSourceMembersPresent": len(named & {x.stem for x in cards}),
        "separateExceptionPreserved": "妖", "batchNewNecessarySupportWords": 3,
        "projectNewNecessarySupportWords": 114, "batchChangedReusedArticles": 1,
        "allMappedReciprocalPairs": 4, "mappedDirectedLinks": 8, "activatedBaselinePairs": 0,
        "separateEarlierLevelSourceMembers": evidence["earlierLevelSourceMemberDisposition"],
        "earlierPlacementsCountedAsIssue60AcceptedBatches": False,
    }
    assert len(named) == 1232 and counts["namedSourceMembersPresent"] == 122
    assert counts["currentKanji"] == 1108 and counts["currentWords"] == 5063 and counts["n1Labelled"] == 117
    publication = {
        "schemaVersion": 1, "execution": 599, "batch": "085", "membership": ["凝"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": TEACHING, "initialReviewedTeachingSnapshot": TEACHING,
        "reviewedTeachingSnapshot": REVIEWED,
        "textualClosureSnapshot": before["execution593CoordinatorCheckpoint"]["savedCommit"],
        "freshAndroidSnapshot": before["execution594CoordinatorCheckpoint"]["savedCommit"],
        "nativeEnvelopeSnapshot": before["execution595CoordinatorCheckpoint"]["savedCommit"],
        "nativeEvidenceSnapshot": before["execution596CoordinatorCheckpoint"]["savedCommit"],
        "visualClosureSnapshot": before["execution597CoordinatorCheckpoint"]["savedCommit"],
        "combinedContentHead": evidence["combinedContentHead"], "latestMainIntegrated": MAIN,
        "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-085-reconciliation.json",
        "visualRecord": "../n1-reviews/batch-085-visual-reconciliation.json",
        "combinedAcceptanceRecord": "execution-598.json", "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": evidence["inheritedAcceptance"]["inheritedLimits"],
        "publicationClarification": "Historical pending integration/publication checks are now verified for the accepted commit here. Terminal evidence CI/archive follow separately. All source/linguistic/process/read-depth/native/pool/phone limitations retained. Native import version matches unchanged combined runtime.",
        "nextAction": "Verify terminal evidence commit CI/exact public ZIP/ownerissue60; yield before086.",
    }
    save(S / "batch-085-publication.json", publication)
    ledger["prePublicationCheckpoint599"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["凝"], publishedAdditions=112,
                  remainingAdditions=1116, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-085-publication.json", pendingGates=[],
                  nextAction=publication["nextAction"], publicationClarification=publication["publicationClarification"])
    for row in ledger["supportMappings"]:
        row["status"] = publication["status"]
    save(ledger_path, ledger, ascii=False)
    for name in ["batch-085-reconciliation.json", "batch-085-visual-reconciliation.json"]:
        path = R / "docs" / "n1-reviews" / name
        review = load(path)
        review["prePublicationState599"] = {k: copy.deepcopy(review[k]) for k in
                                           ("status", "runtimePublished", "limits") if k in review}
        review.update(status=publication["status"], runtimePublished=True,
                      publicationRecord="../n1-sources/batch-085-publication.json",
                      publicationClarification=publication["publicationClarification"])
        save(path, review, ascii=False)
    execution = {
        "schemaVersion": 1, "execution": 599, "batch": "085", "status": publication["status"],
        "startingState": p["execution599StartingState"], "publicationRecord": "batch-085-publication.json",
        "acceptedCommit": HEAD, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-598.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newReviewNativeHostRuns": 0, "limits": publication["limits"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    receipts = []
    for name, args in [("validate", ["tools\\validate.py"]),
                       ("manifest", ["tools\\build_manifest.py"]),
                       ("budget", ["tools\\check_content_budget.py"])]:
        path = D / f"{name}-599.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args], cwd=R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    execution["terminalLocalValidation"] = receipts
    save(S / "execution-599.json", execution)
    for path in [L / "prepublication-gate-599.json", L / "starting-state-599.json",
                 C / "artifacts" / "batch-085-accepted-ci.json",
                 C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json",
                 C / "verify-batch-002-publication.py", C / "publish-599.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-085-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution599AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Accepted public delivery verified; durable ledgers and terminal local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-085-publication.json")
    body = f"""Batch **085 (凝)** is published and verified for bounded owner testing, with necessary supporting articles **凝固 (ぎょうこ), 凝る (こる), 凝らす (こらす)** and the reviewed 固 navigation bullet. Four mapped reciprocal pairs/eight directions; no activated baseline pairs.

Authored/initially reviewed `{TEACHING}`; exact reviewed effort exclusion and textual closure `{REVIEWED}`; native evidence `{publication['nativeEvidenceSnapshot']}`; original-family visual closure `{publication['visualClosureSnapshot']}`. Fresh main `{MAIN}` was already an ancestor; normal merge reported Already up to date, with no synthetic merge/conflict/teaching change. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global account unchanged.

Independent blind initial **Claude Opus5.5 / GPT6.1Sol** reviews and serial original-session confirmations retained. Q1 direct 努力 exclusion resolved by exact dictionary/title evidence and both confirmations; other polish optional. Serial original-family visual confirmations inspected the same packet,15 full-frame contact sheets plus8 focused originals per family; all50 child processes exited0. No new blind-review credit or equal fresh-read/comprehension certification. No actionable scoped teaching finding remains.

Combined-tree **372 Python tests**, validator0errors, vocabulary consistency, fresh manifest, frozen-source/decompressed hashes, three full lexical-packet re-extractions, original985kanji/4942words/985strokes with narrow recorded exceptions, exact membership, six reading dispositions,32 direct guards, pinned16-stroke geometry and fresh **3 RealContentTest + 1 RareHanTest** passed without skips/failures/errors in598. No reviewer/HOST/native rerun here. Inherited596 **two named native terminal-status0 cases**: production ContentSync full archive ONCE,1108kanji/5063words/117N1,zero problems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged combined runtime. Full/Lite retain all6 source readings in order; curated ギョウ/こ.る/こ.らす produces exactly **ぎょう/こる**, both kinds offered/persistedGood/done. Selectedこ.らす shares normalizedこる, **not independently queued mastery**.

Native evidence covers N1 selection/meaning/readings, four complete scoped article projections plus changed固bullet, fourpairs/eightdirections/SystemBack/offline and16 reference-INJECTED strokes/trace/recallgiveup/gradepersistence. Exact default four 凝/准/冗/凹 IDs/titles verified in N1/All builder and actual N1 UI; **All UI/custom/padded/partial/larger/random pools uncertified**.39 scoped Han/fourproductionfamilies/threewholewords readable within captures.87 originals represented by resized full-frame sheets plus8 focused originals; **not87 full-resolution reads**, fallback-face identity or other-device certification. Table targets scroll horizontally; not all columns simultaneously. Fine kana/underlines/Brush strokes/overlaid drawing numbers have limited detail. Injected tracing/giveup is **not human handwriting, successful recall, MLKit recognition or phone evidence**; offline handwriting model unavailable. Qualified TEST-ONLY Android `{APP}` preserves production f9b59a2, not latest app main.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable public ZIPs preserve **all8413 runtime hashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus per-file/media/safe-path guards; contributor evidence excluded.

Published **112/1228 additions;1116 remain**. Collection **1108kanji/5063words/117N1-labelled/122named-source members plus separate妖**. Six separate public-main source members 保/案/派/第/策/結 retain earlier N2 levels, **not counted as issue60 accepted additions**; do not duplicate them. This batch adds3 necessary support articles;114project-wide, **not an N1 vocabulary deck**.

All original source/lookup/process/read-depth/compaction/downscale/native/pool limitations retained in `execution-598.json` and `batch-085-publication.json`. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; old clients ignore curation. **Physical-phone/general-release/whole-set acceptance outstanding**. Parent19008 retains runner.lock; no child lock or optional historical-session helper access. Checkpoint599 persists `continue` and yields before086; no next batch or second runner.

Durable evidence: `docs/n1-sources/batch-085-publication.json`, `execution-599.json`, original593textual/594HOST/595fixture/596native/597visual/598combined records.
"""
    target = C / "batch-085-publication-comment.txt"
    assert not target.exists()
    target.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-599.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; exact owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-085-publication-issue-receipt.json")
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        encoding="utf-8"))
    body = (C / "batch-085-publication-comment.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], encoding="utf-8").strip() == "romanko-ms"
    assert not (S / "batch-086-progress.json").exists()
    ledger = load(S / "batch-085-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == ["凝"]
    publication = load(S / "batch-085-publication.json")
    next_action = (
        f"Batch085 accepted/published/verified at{head}; yield before086. Next coordinator ONE bounded086 "
        "source-preparation checkpoint from remaining frozen rows below15. Read fullrequest/finalcheckpoint/"
        "approvedissue; preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "session. Parent19008 retainsrunner.lock: no child acquire/delete/unlock. Approvedcontrolhelpers/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield "
        "actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/"
        "baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "two serialblinddifferentfamilies/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normal signing/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/original18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published112/1228;1116acceptance-remainder;1108kanji5063words117N1labels122namedmembers+separate妖; "
        "114necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.085initiala7512a5e+reviewed29a53380effortguard/"
        "envelope1d2e3290/version0c514711ae8d3212/8413hashes;372Python/fresh598HOST4/inherited596native2/"
        "original597visuals/accepted+terminalCI+ZIP/ownerissueverified. No freshreview/native/HOST here. "
        "Native fullContentSyncONCE1108kanji5063words117N1/zeroProblems/epoch1/versionmatches combined. "
        "Fullsixmetadata retained; curatedギョウ/こ.る/こ.らす yieldsぎょう/こる BOTHkindspersistedGood/done; "
        "selectedこ.らす sharesnormalizedこる NOT independentqueuedmastery. Q1resolved/othersoptional. "
        "All original source/process/readdepth/compaction/downscale/fallbackface/bodyfine-stroke/pool/MLKit/"
        "phone limits preserved; historical pending publication/combined gates now fulfilled. "
        + " ".join(publication["limits"])
        + " CompatibleAndroidf9b59a2+required. Physicalphone/generalrelease/whole-setoutstanding; projectincomplete. "
        "No086started/authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       nextAction=next_action)
    save(C / "batch-085-publication-checkpoint.json", publication)
    save(L / "batch-085-publication-checkpoint.json", publication)
    before = load(BEFORE)
    p = load(C / "progress.json")
    p["execution599StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 599, "checkpoint": 599, "batch": "085",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8413,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-085-published-verified-before-086",
        "publishedAdditions": 112, "remainingAdditions": 1116, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution599CoordinatorCheckpoint"] = verification
    p["batch085PublicationCheckpoint"] = publication
    p["batch085PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-085-publication-comment.txt"), "verified": True}
    p.update(checkpoint=599, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1116, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1116 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-verification-599.json", verification)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps({k: v for k, v in verification.items() if k != "nextAction"}, indent=2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "start":
        start()
    elif mode == "verify":
        verify(sys.argv[2], sys.argv[3])
    elif mode == "records":
        records()
    elif mode == "comment":
        comment(sys.argv[2])
    elif mode == "finish":
        finish(sys.argv[2])
    else:
        raise ValueError(mode)
