"""Publish only accepted batch086; the live parent retains runner.lock."""
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
V = R / "docs" / "n1-reviews"
D = V / "batch-086-publication-608"
L = C / "logs" / "cff4a59b-fb9d-4223-b295-c82b20a532ec"
HEAD = "6bb780671a8418a3def2e27e1e5c4531e9a074ab"
MAIN = "f001846c194b20b13b9deb797d70e04a34025d93"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
TEACHING = "f59c65fde644ed36958d74495da59a66c1d82570"
VERSION = "86e8cb13aa72ecd0"
BEFORE = L / "progress-before-608.json"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value, ascii=True):
    temp = path.with_suffix(path.suffix + ".608.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(value, ensure_ascii=ascii, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


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
    assert (p["checkpoint"], p["batch"], p["status"]) == (607, "086", "continue")
    return ids


def runtime():
    from build_manifest import build_manifest
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == VERSION
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8416
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
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
    assert embedded["checkpoint"] == 607
    state = {
        "execution": 608, "batch": "086", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME086 signed owner fast-forward publication and exact public CI/ZIP/issue acceptance; yield before087. No new reviewer/native/HOST absent change.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, entire approved issue and final607 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial scalar output hit cp1252; bounded UTF-8 reread succeeded."},
        "runnerLockRole": "Live parent19008 ancestry/session verified; no child opens/acquires/deletes/unlocks runner.lock.",
        "artifactPathPreflight": "Approved control helpers, committed source/review evidence and frozen workspace inputs only. No optional historical-session artifact accessed.",
        "ancestryPids": ids, "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-608.json", state)
    p = load(C / "progress.json")
    p["execution608StartingState"] = state
    p.update(stage="batch-086-publication-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    evidence = load(S / "execution-607.json")
    assert sha(S / "execution-607.json") == p["execution607CoordinatorCheckpoint"]["evidenceSha256"]
    assert evidence["runtimeAccepted"] and not evidence["runtimePublished"]
    assert evidence["pythonTestsPassed"] == 372 and evidence["validatorErrors"] == 0
    assert evidence["hostTestsExecuted"] == 4 and evidence["hostChecksFresh"]
    for receipt in evidence["receipts"]:
        path = R / receipt["archive"]
        assert sha(path) == receipt["sha256"], path
        data = gzip.decompress(path.read_bytes()) if receipt["losslessGzip"] else path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == receipt["sourceSha256"], path
    for report in evidence["inheritedAcceptance"]["reviewReports"]:
        path = Path(report["report"])
        if not str(path).startswith("docs"):
            path = Path("docs") / "n1-reviews" / path
        assert report["exitCode"] == 0
        assert sha(R / path) == report["reportSha256"]
    assert evidence["inheritedAcceptance"]["nativeTerminalCaseStatuses"] == [0, 0]
    for name, key in [
        ("batch-086-reconciliation.json", "actionableRemainingTeachingFindings"),
        ("batch-086-visual-606-reconciliation.json", "actionableRemainingFindings"),
    ]:
        assert load(V / name)[key] == 0
    assert load(S / "batch-086-progress.json")["reviewClosed"] == ["凡"]
    runtime()
    save(L / "prepublication-gate-608.json", {
        "acceptedHead": HEAD, "freshMain": MAIN, "signature": "G",
        "runtimeHashesVerified": 8416, "combinedReceiptsVerified": len(evidence["receipts"]),
        "reviewReportsVerified": 4, "nativeTerminalCasesVerified": 2,
        "parentLockTouched": False, "newReviewerNativeHostRuns": 0,
    })
    print("Starting scope saved; exact signed acceptance and all8416 runtime hashes reverified.")


def public(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci = load(C / "artifacts" / f"batch-086-{phase}-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    assert archive["commit"] == head and archive["contentVersion"] == VERSION
    assert archive["verifiedRuntimeHashes"] == 8416 and archive["manifestEqual"]
    assert all(archive[k] for k in [
        "allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"])
    assert sha(C / "artifacts" / f"content-{head[:7]}.zip") == archive["sha256"]
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    return ci, archive


def verify(phase, head):
    context()
    clean(R, head)
    runtime()
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    ci_path = C / "artifacts" / f"batch-086-{phase}-ci.json"
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


def records():
    ci, archive = public("accepted", HEAD)
    assert not D.exists() and not (S / "batch-086-publication.json").exists()
    D.mkdir()
    p = load(C / "progress.json")
    before = load(BEFORE)
    evidence = load(S / "execution-607.json")
    ledger_path = S / "batch-086-progress.json"
    ledger = load(ledger_path)
    counts = dict(evidence["sourceAudit"]["currentCounts"])
    counts.update(batchPublishedAdditions=1, projectPublishedAdditions=113, remainingAdditions=1115,
                  batchNewNecessarySupportWords=1, projectNewNecessarySupportWords=115,
                  batchChangedReusedArticles=6, allMappedReciprocalPairs=7, mappedDirectedLinks=14,
                  activatedBaselinePairs=1, separateExceptionPreserved="妖",
                  separateEarlierLevelSourceMembers=evidence["earlierLevelSourceMemberDisposition"],
                  earlierPlacementsCountedAsIssue60AcceptedBatches=False)
    assert counts["kanji"] == 1109 and counts["words"] == 5064
    assert counts["n1Labels"] == 118 and counts["namedSourceMembersPresent"] == 123
    limits = {
        "combined": evidence["limits"],
        "sourceText": evidence["inheritedAcceptance"]["inheritedSourceTextLimits"],
        "nativeVisualDispositions": evidence["inheritedAcceptance"]["inheritedNativeVisualDispositions"],
        "additionalCombinedLimits": evidence["inheritedAcceptance"].get("limits", []),
    }
    publication = {
        "schemaVersion": 1, "execution": 608, "batch": "086", "membership": ["凡"],
        "status": "published-verified-bounded-owner-testing",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": ledger["baseCommit"],
        "authoredSnapshot": TEACHING, "initialReviewedTeachingSnapshot": TEACHING,
        "reviewedTeachingSnapshot": TEACHING,
        "combinedContentHead": evidence["combinedContentHead"], "latestMainIntegrated": MAIN,
        "acceptedCommit": HEAD, "integratedCommit": HEAD, "publishedCommit": HEAD,
        "snapshots": {str(n): before[f"execution{n}CoordinatorCheckpoint"]["savedCommit"]
                      for n in range(600, 608)},
        "normalSignatureStatus": "G; normal owner-scoped fast-forward; no bypass/amendment/force push.",
        "reviewRecord": "../n1-reviews/batch-086-reconciliation.json",
        "visualRecord": "../n1-reviews/batch-086-visual-606-reconciliation.json",
        "combinedAcceptanceRecord": "execution-607.json", "validation": evidence["sourceAudit"],
        "pythonTestsPassed": 372, "hostTestsReverified": 4, "nativeTerminalCasesReverified": 2,
        "newReviewNativeHostRuns": 0, "ci": ci, "immutablePublicArchive": archive,
        "counts": counts, "contentVersion": VERSION,
        "compatibleClient": "Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection.",
        "qualifiedAndroidHead": APP,
        "publicationIdentity": "stop-cran; process-scoped token only; global romanko-ms unchanged.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": limits,
        "publicationClarification": "Historical pending integration/publication gates fulfilled for accepted commit here; terminal evidence CI/archive follow separately. Every original source, review, native, process and phone qualification retained; no fresh native/reviewer/HOST run.",
        "nextAction": "Verify terminal evidence CI/exact public ZIP/ownerissue60; yield before087.",
    }
    save(S / "batch-086-publication.json", publication)
    ledger["prePublicationCheckpoint608"] = copy.deepcopy(ledger)
    ledger.update(status=publication["status"], published=["凡"], publishedAdditions=113,
                  remainingAdditions=1115, publishedCommit=HEAD, runtimePublished=True,
                  publicationRecord="batch-086-publication.json",
                  pendingGates=["Physical-phone/general-release and whole-set acceptance outstanding."],
                  nextAction=publication["nextAction"], publicationClarification=publication["publicationClarification"])
    for row in ledger.get("supportMappings", []):
        row["status"] = publication["status"]
    save(ledger_path, ledger, ascii=False)
    for name in ["batch-086-reconciliation.json", "batch-086-visual-606-reconciliation.json"]:
        path = V / name
        review = load(path)
        review["prePublicationState608"] = {k: copy.deepcopy(review[k]) for k in
                                           ("status", "runtimePublished", "limits") if k in review}
        review.update(status=publication["status"], runtimePublished=True,
                      publicationRecord="../n1-sources/batch-086-publication.json",
                      publicationClarification=publication["publicationClarification"])
        save(path, review, ascii="visual" in name)
    receipts = []
    for name, args in [("validate", ["tools\\validate.py"]),
                       ("manifest", ["tools\\build_manifest.py"]),
                       ("budget", ["tools\\check_content_budget.py"])]:
        path = D / f"{name}-608.txt"
        with path.open("wb") as stream:
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", *args], cwd=R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        receipts.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path), "exitCode": 0})
    execution = {
        "schemaVersion": 1, "execution": 608, "batch": "086", "status": publication["status"],
        "startingState": p["execution608StartingState"], "publicationRecord": "batch-086-publication.json",
        "acceptedCommit": HEAD, "counts": counts, "ci": ci, "immutablePublicArchive": archive,
        "inheritedAcceptanceRecord": "execution-607.json", "runtimeBytesUnchanged": True,
        "runtimePublished": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newReviewNativeHostRuns": 0, "limits": limits, "terminalLocalValidation": receipts,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    save(S / "execution-608.json", execution)
    for path in [L / "prepublication-gate-608.json", L / "starting-state-608.json",
                 C / "artifacts" / "batch-086-accepted-ci.json",
                 C / "artifacts" / f"content-{HEAD[:7]}-acceptance.json",
                 C / "verify-batch-002-publication.py", C / "publish-608.ps1", Path(__file__)]:
        shutil.copyfile(path, D / path.name)
    runtime()
    p.update(stage="batch-086-accepted-published-awaiting-terminal-evidence", nextAction=publication["nextAction"])
    p["execution608AcceptedPublication"] = copy.deepcopy(publication)
    save(C / "progress.json", p)
    print("Accepted public delivery verified; durable ledgers and terminal local validation saved.")


def comment(head):
    ci, archive = public("terminal", head)
    publication = load(S / "batch-086-publication.json")
    body = f"""Batch **086 (凡)** is published and verified for bounded owner testing, with necessary support **凡例 (はんれい), explanatory notes; legend**. Reviewed reuse/recognition/navigation passages cover 平凡, およそ, 全て and baseline 平/例/全. Seven mapped reciprocal pairs/fourteen directions; one activated baseline pair; eight direct word guards.

Authored and independently reviewed teaching `{TEACHING}`; textual closure `{publication['snapshots']['602']}`; native evidence `{publication['snapshots']['605']}`; original-family visual closure `{publication['snapshots']['606']}`. Fresh main `{MAIN}` was already an ancestor; normal merge Already up to date, no synthetic merge/conflict/teaching change. Normally signed accepted publication `{HEAD}`; terminal evidence/remote main `{head}`. Both owner-scoped pushes are normal fast-forwards; global account unchanged.

Independent blind **Claude Opus5.5 / GPT6.1Sol** textual reviews and serial dependent original-session visuals retained; no new blind-review credit. All assigned initial packet ranges returned, including71 complete JMdict families,7 raw characters,28 full article bodies. Each original reviewer viewed24 images for visual confirmation. Exact returned images are downscaled (1080x2456→879x2000 and1080x2400→900x2000), not nativepixel independent inspection; original reports and failed first source-byte assertion retained. No actionable scoped teaching defect remains; optional points remain optional.

Combined-tree **372 Python tests**, validator0errors, vocabulary consistency, fresh manifest, source/baseline/exact membership, allfive reading dispositions, seven reciprocal pairs/fourteen directions, eight direct guards and pinned three-stroke regeneration passed; fresh **3 RealContentTest + 1 RareHanTest** passed without skips/failures/errors in607. No reviewer/HOST/native rerun here. Inherited605 **two named native terminal-status0 cases** used production ContentSync full archive **ONCE**,1109kanji/5064words/118N1,zero problems/acceptedRoomparserEpoch1/version `{VERSION}`, matching unchanged combined runtime.

Full/Lite preserve allfive raw readings/order; curated ボン/ハン schedules only **ぼん/はん**, explicit kun[]. Raw **おうよ.そ remains UNVERIFIED source-only**, not silently normalized or asserted modern usage. 凡そ is usually kana; 凡て is rare kanji spelling, not a rare kana pronunciation. Native N1 selection/meaning/readings/drawing/article/SystemBack/offline and31Han/fourfonts incl丶/几 covered within recorded captures. Exact fallback face unknown. N1 meaning pool had only凹 curated available plus **two fallback choices**: observed labels and seeded604 choices safe, not arbitrary/custom/randompool certification. Three injectedtrace strokes/recallgiveup are **not human handwriting, successful recall, MLKit or phone evidence**. Qualified TEST-ONLY Android `{APP}` preserves productionf9b59a2, not latestappmain. No heap/guard increase.

Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) green. Both exact immutable public ZIPs preserve **all8416 runtime hashes** and manifest `{VERSION}`. Terminal **{archive['zipEntries']}entries / {archive['compressedBytes']}compressed / {archive['inflatedBytes']}inflated / {archive['retainedBytes']}retained bytes** passes unchanged18000entries/42MiB/80MiB/56MiB plus per-file/media/safe-path guards; contributor evidence excluded.

Published **113/1228 additions;1115 remain**. Collection **1109kanji/5064words/118N1-labelled/123named-source members plus separate妖**. Six separate public-main source members 保/案/派/第/策/結 retain earlier N2 levels, **not counted as issue60 accepted additions**; do not duplicate/relevel. This batch adds1 necessary support article;115project-wide, **not an N1 vocabulary deck**.

Durable evidence: `docs/n1-sources/batch-086-publication.json`, `execution-608.json`, original602textual/603HOST/604fixture/605native/606visual/607combined records. Every original source/lookup/process/readdepth/downscale/fallbackface/pool/phone qualification retained. Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** required; old clients ignore curation. **Physical-phone/general-release/whole-set acceptance outstanding; project incomplete**. Parent19008 retains runner.lock; no child lock or optional historical-session helper access. Checkpoint608 persists continue and yields before087; no next batch or second runner.
"""
    target = C / "batch-086-publication-comment.txt"
    assert not target.exists()
    target.write_text(body, encoding="utf-8")
    save(L / "terminal-publication-608.json", {
        "head": head, "ci": ci, "archive": archive, "issueBodySha256": sha(target)})
    print("Terminal CI/archive verified; exact owner issue body prepared.")


def finish(head):
    ci, archive = public("terminal", head)
    receipt = load(C / "batch-086-publication-issue-receipt.json")
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        encoding="utf-8"))
    body = (C / "batch-086-publication-comment.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == remote["user"]["login"] == "stop-cran"
    assert receipt["body"] == remote["body"] == body
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], encoding="utf-8").strip() == "romanko-ms"
    assert not (S / "batch-087-progress.json").exists()
    ledger = load(S / "batch-086-progress.json")
    assert ledger["membership"] == ledger["reviewClosed"] == ledger["published"] == ["凡"]
    publication = load(S / "batch-086-publication.json")
    next_action = (
        f"Batch086 accepted/published/verified at{head}; yield before087. Next coordinator ONE bounded087 "
        "source-preparation checkpoint from remaining frozen rows below15. Read entire request/finalcheckpoint/"
        "approvedissue and preserve FULLlivehistory. Verify whollyclean signedheads/freshmain/liveparentancestry/"
        "session. Parent19008 retainsrunner.lock: no child acquire/delete/unlock. Approvedcontrolhelpers/"
        "committedsourcepackets/frozeninputs only; no optional historicalsessionrecipes. Preserve/report/yield "
        "actualnewdenial/signinghang/uncertainownership. All original fullfamily/readingallocation/usefulness/"
        "baseline/fullmetadata/curation/directguards/allmapped+activatedlinks/pinnedstrokes/newHanfonts/"
        "two serialblinddifferentfamilies/originalsessionconfirmation/non-skippedAndroid/native/combinedmain/"
        "normal signing/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/original18000entries42MiB"
        "compressed80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gates remain. "
        "Published113/1228;1115acceptance-remainder;1109kanji5064words118N1labels123namedmembers+separate妖; "
        "115necessarysupportsNOTN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
        "not issue60accepted additions; do not duplicate/relevel.086initialf59c65fd/textual207816fa/"
        "HOST6667318d/fixturee1077c77/native81238670/visualf23dae44/accepted6bb78067/"
        "version86e8cb13aa72ecd0/8416hashes;372Python/fresh607HOST4/inherited605native2/"
        "original606visuals/accepted+terminalCI+ZIP/ownerissueverified. No freshreview/native/HOST here. "
        "Native fullContentSyncONCE1109kanji5064words118N1/zeroProblems/epoch1/versionmatches combined. "
        "Allfive raw readings/order retained; only on keysぼん/はん queued, kun[]. Rawおうよ.そ modern "
        "usage remains UNVERIFIED source-only, not normalized/assertedmodernusage. Recognition凡そ "
        "usuallykana and凡て rareKANJI spelling do not make kana pronunciation rare. Sevenpairs14directions/"
        "eightdirectguards; all31Han/fourfonts incl丶几 readable; exactfallbackfaceunknown and images "
        "toolresized, NOT nativepixel independentinspection. N1meaning only凹curated plusTWOfallbacks; "
        "boundedobservedlabels/seeded604safe, not arbitrarypool certification. Threeinjectedtrace/"
        "recallgiveup NOT humanhandwriting/MLKit/phone. QualifiedTESTONLYAndroid1c1b7bf4 retainsproduction"
        "f9b59a2, notlatestappmain. Alloriginal source/process/readdepth/downscale/native/pool/phone "
        "limits andoptionaldispositions preserved in docs/n1-sources/batch-086-publication.json and "
        "execution-607.json. Physicalphone/generalrelease/whole-setoutstanding; projectincomplete. "
        "No087started/authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease."
    )
    publication.update(finalPublishedCommit=head, remoteMainVerified=head, terminalCi=ci,
                       terminalImmutablePublicArchive=archive, issueUpdate=receipt["html_url"],
                       nextAction=next_action)
    save(C / "batch-086-publication-checkpoint.json", publication)
    save(L / "batch-086-publication-checkpoint.json", publication)
    before = load(BEFORE)
    p = load(C / "progress.json")
    p["execution608StartingState"]["status"] = "bounded-publication-checkpoint-complete"
    verification = {
        "schemaVersion": 1, "execution": 608, "checkpoint": 608, "batch": "086",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head, "acceptedCommit": HEAD,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": ci["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8416,
        "reviewedRuntimeBytesUnchanged": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["html_url"],
        "globalIdentityUnchanged": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-086-published-verified-before-087",
        "publishedAdditions": 113, "remainingAdditions": 1115, "lastPublishedCommit": head,
        "nextAction": next_action, "blocker": None, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    p["execution608CoordinatorCheckpoint"] = verification
    p["batch086PublicationCheckpoint"] = publication
    p["batch086PublicationIssueReceipt"] = {
        "id": receipt["id"], "url": receipt["html_url"], "author": "stop-cran",
        "bodySha256": sha(C / "batch-086-publication-comment.txt"), "verified": True}
    p.update(checkpoint=608, status="continue", stage=verification["stage"],
             lastPublishedCommit=head, remainingAdditions=1115, blocker=None, nextAction=next_action)
    p["unmetAcceptanceGates"] = copy.deepcopy(before["unmetAcceptanceGates"])
    p["unmetAcceptanceGates"][0] = "Remaining1115 issue60 source-bounded additions not review-closed/published; six separately placed earlier-level source members require accounted dispositions, not duplicates or issue60 acceptance credit. All original source/review/baseline/reading/link/font/Android/native/currentmain/CI/publicZIP gates remain."
    allowed = {"checkpoint", "status", "stage", "lastPublishedCommit", "remainingAdditions",
               "blocker", "nextAction", "unmetAcceptanceGates"}
    assert before.keys() <= p.keys()
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-verification-608.json", verification)
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
