"""Reconcile both original-session confirmations and persist textual-only closure."""
import copy
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("correction094", C / "correct-batch-094-679.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R, A, S, V, L = m.R, m.A, m.S, m.V, m.L
load, save, sha, git = m.load, m.save, m.sha, m.git
STAGE = "batch-094-textual-review-closed-awaiting-android-native"
NEXT = (
    "SAME094 fresh Android checkpoint next; textual closure ONLY at revised signed4089e881. "
    "Three direct guards削る/除く,削る/外す,削除/省く are applied and both ORIGINAL "
    "Claudeedf22897-9f87-4a3b-b20f-4c2fd839013a and GPT65fd64ff-aae2-40af-927e-bf19b52fecb6 "
    "confirmed serially without remaining actionable textual defects. No newblind credit. "
    "Run fresh non-skipped THREE RealContentTest and ONE RareHanTest against THIS sibling; "
    "qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Use explicit "
    "JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot and "
    "ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, oneGradleworker "
    "and quoted '-Pkotlin.compiler.execution.strategy=in-process'; inspect terminal test reports "
    "and actual sibling path, no skip assumptions. Then fresh fullarchive productionContentSync "
    "ONCE/native N1/All production choices and THREE new direct guards, onlyさく/けずる reading "
    "questions, nine-stroke drawing, complete削/削る/削除 and reciprocal除 articles, SystemBack/"
    "offline/all41Han/fourfonts with fresh safe port/device ownership checks; 刂/斫/氵/阝 cmap "
    "absence is NOT glyph failure. Preserve exact fixture/hash and actual terminalcase0; no "
    "heap/archiveguard increase, preflight doubleparse or shared-device interference. Original "
    "reviewer sessions then need bounded rendered confirmations; current textual review is "
    "not native/phone or live-pool acceptance. All original combined-current-main/nonrewriting "
    "merge/changedteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/EVERY"
    "immutableZIPmanifestentryhash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/"
    "media/path/verifiedownerissue gates remain. Parent19008 retains runner.lock throughout child "
    "lifetime: NO child acquire/delete/unlock. Approved control/committed packets/frozen inputs "
    "only; no optional historical-session helper access. Preserve/report/yield actual new denial, "
    "signing hang or uncertain ownership. Published120/1228 and1108acceptanceremainder unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No095, unreviewedpush or secondrunner."
)


def records():
    staging = C / "batch-094-confirmation-679"
    freeze = load(C / "batch-094-confirmation-freeze-679.json")
    previous, result = None, {}
    for label, model in m.MODELS.items():
        prefix = f"batch-094-confirm-679-{label}"
        rec = load(staging / (prefix + "-execution.json"))
        coverage = load(staging / (prefix + "-coverage.json"))
        assert rec["exitCode"] == 0 and rec["actualModels"] == [model]
        assert rec["usageCurrentModel"] == model
        assert rec["snapshot"] == freeze["snapshot"] and rec["sessionId"] == m.SESSIONS[label]
        assert "--resume" in rec["command"] and "--session-id" not in rec["command"]
        assert rec["availableTools"] == ["view"] and "--available-tools=view" in rec["command"]
        assert not rec["unfinishedTools"] and not rec["observedToolOverlaps"]
        assert rec["multiToolResponseCount"] == 0 and coverage["allAssignedRangesReturned"]
        assert len(rec["toolCalls"]) == 1
        call = rec["toolCalls"][0]
        packet = C / f"batch-094-confirm-{label}-packet-679.txt"
        assert call["name"] == "view" and call["success"]
        assert call["arguments"] == {"path": str(packet), "forceReadLargeFiles": True}
        assert call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
        assert sha(staging / (prefix + ".md")) == rec["reportSha256"]
        assert sha(staging / (prefix + ".jsonl")) == rec["rawExecutionSha256"]
        assert subprocess.run(["pwsh", "-NoProfile", "-Command",
            f"if (Get-Process -Id {rec['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
            capture_output=True).returncode == 0
        assert not previous or previous < rec["startedAt"]
        previous = rec["completedAt"]
        result[label] = {
            **{k: rec[k] for k in ["launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
                                   "requestedModel", "actualModels", "snapshot", "reportSha256",
                                   "rawExecutionSha256"]},
            "report": prefix + ".md", "execution": prefix + "-execution.json",
            "coverage": prefix + "-coverage.json",
            "packet": packet.name, "packetSha256": sha(packet),
            "packetBytes": packet.stat().st_size,
            "packetLines": len(packet.read_text(encoding="utf-8").splitlines()),
            "allAssignedRangesReturned": True, "toolCalls": 1,
            "observedToolOverlaps": 0, "exactFullPacketReturnedInOneCall": True,
            "originalSessionResumed": True, "newBlindReviewCredit": False,
            "limits": "Actual full returned packet and process exit verified, not comprehension certification, fresh121family review or native acceptance. Usage metrics are cumulative original-session totals.",
        }
    return freeze, result


def prepare():
    m.identity(clean=True)
    freeze, confirmed = records()
    assert git("rev-parse", "HEAD") == freeze["snapshot"]
    for name, value in freeze["runtimeHashes"].items():
        assert sha(R / name) == value
    before_rec = load(V / "batch-094-reconciliation.json")
    archived = V / "batch-094-reconciliation-before-correction-678.json"
    assert not archived.exists()
    shutil.copyfile(V / "batch-094-reconciliation.json", archived)
    staging = C / "batch-094-confirmation-679"
    for label in m.MODELS:
        prefix = f"batch-094-confirm-679-{label}"
        for suffix in [".md", ".jsonl", "-execution.json", "-coverage.json", "-stderr.txt"]:
            src, dst = staging / (prefix + suffix), V / (prefix + suffix)
            assert not dst.exists()
            shutil.copyfile(src, dst)
        for kind in ["packet", "prompt"]:
            path = C / f"batch-094-confirm-{label}-{kind}-679.txt"
            shutil.copyfile(path, V / path.name)
    rec = copy.deepcopy(before_rec)
    rec.update(execution=679, status=STAGE, reviewedTeachingSnapshot=freeze["snapshot"],
               teachingChangedAfterInitialReviews=True, articleBodiesChangedAfterInitialReviews=False,
               confirmations=confirmed, textualReviewClosed=True,
               actionableRemainingFindingGroups=0, actionableRemainingDirectPairs=0,
               consequentialUnresolvedTeachingClaims=0, newDirectWordExclusionPairsApplied=3,
               acceptedDirectWordExclusionPairsPending=0, reviewedRuntimeHashes=freeze["runtimeHashes"],
               contentVersion=load(R / "manifest.json")["contentVersion"], nextAction=NEXT)
    rec["initialReviewStatePreserved"] = archived.name
    finding = rec["findings"][0]
    assert finding["id"] == "094-word-direct-guards" and finding["status"] == "unresolved"
    finding.update(status="resolved", remediationApplied=True, resolvedSnapshot=freeze["snapshot"],
                   confirmationEvidence={k: v["report"] for k, v in confirmed.items()})
    for pair in finding["pairs"]:
        pair["status"] = "resolved"
    for name in ["words/削る.md", "words/削除.md"]:
        rec["verdicts"][name]["correctness"] = "CLEAN"
        rec["verdicts"][name]["scope"] = "Complete original review carried forward with three direct additive guards confirmed; no prose change. Bounded textual review only."
    rec["confirmationAdjudication"] = {
        "status": "resolved",
        "decision": "All three exact guards implement source-supported pairwise ambiguity safeguards. Both original reviewers find no associated regression; closure rests on exact declarations, complete applicable senses, displayed labels and direct-pair contract, not model votes.",
        "claudeReassessment": "Original low-risk削除/省く hypothesis resolved; original broad statement that guards covered real overlaps partly withdrawn. Added削る/除く and削る/外す accepted. This is post-fix confirmation, not original blind discovery.",
        "optional": "All prior wording/example/polish items remain optional and untouched; no manufactured additional defect.",
        "contributionAccounting": "削除/省く observation remains shared because Claude mentioned it as a hypothesis. GPT unique established useful initial findings are削る/除く and削る/外す only. No generalized model ranking.",
    }
    rec["mechanicalBatchAudit"] = load(S / "batch-094-correction-audit-679.json")
    rec["previousCompleteSourceBaselineFontStrokeAudit"] = "docs/n1-sources/batch-094-draft-audit.json"
    rec["correctionCompleteAudit"] = "docs/n1-sources/batch-094-correction-audit-679.json"
    rec["correctionChecks"] = load(S / "batch-094-correction-freeze-679.json")["checks"]
    rec["limits"] = [
        "TEXTUAL closure only on revised signed4089e881; runtimeAccepted/runtimePublished remain false. All three source-supported direct guards applied and both original-session confirmations complete; no remaining actionable textual defect or consequential unresolved teaching claim.",
        "Initial two-family blind review at d1e986ec retained unchanged. These are bounded follow-ups in original sessions, not newblind reviews or a fresh121family inspection. Exact full packets returned through one serial view call each; actual models/process exits verified. Returned bytes do not prove comprehension.",
        "Confirmation packets contain each own original report, exactdiff, seven complete current articles, five complete applicable frozen families and two complete committed public extracts. Public evidence is supplied extraction, not independent upstream retrieval. Initial Weblioへずる/footer and中止target limitations remain historical, not newly verified.",
        "Only two word-header exclusion lists and generatedmanifest changed. Bodies, stableidentities, primaryreadings, titles, N2levels, originalexclusions/order, fullsource readings/order, explicitcuration, links and strokegeometry preserved.",
        "Fullbaseline985kanji/4942words/985strokes audited with original exceptions plus onlythree newdirectpairs. Frozeninputs/fullfamilyextractions/tenrawrecords/threeallmappedpairs/sixdirections/twoactivatedpairs/fourreadings/twokeys/ninepaths/all41Han/fontcmaps and8438payloadhashes verified mechanically, not linguistic/native certification.",
        "LiveN1/All/custom/randompool choices and actualthreeguards remain original native gates, as do fresh non-skippedAndroid/RareHan, fullarchiveContentSyncONCE, drawing/reading/articles/SystemBack/offline/fourfonts and both original-session rendered confirmations. Cmapabsence of刂/斫/氵/阝 is NOT glyphfailure.",
        "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain; compatiblef9b59a2+ required. Physicalphone/generalrelease/whole-set outstanding.",
        "Published120/1228 and1108acceptanceremainder unchanged. Earlierlevel保案派第策結 and separate妖 retained. No095, unreviewedpush, secondrunner, parentlocktouch or optionalhistorical-sessionhelperaccess.",
        "All original combined-main/nonrewritingmerge/changedteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/unchangedbudgets/media/path/verifiedownerissue gates remain.",
    ]
    save(V / "batch-094-reconciliation.json", rec)
    p = load(S / "batch-094-progress.json")
    p.update(status=STAGE, textualReviewClosed=True, reviewedTeachingSnapshot=freeze["snapshot"],
             nextAction=NEXT, limits=rec["limits"])
    p["textualReview"].update(snapshot=freeze["snapshot"], textualReviewClosed=True,
                              teachingChanged=True, acceptedUnresolvedDirectQuizPairs=[],
                              resolvedDirectQuizPairs=[pair["words"] for pair in finding["pairs"]],
                              confirmations=confirmed, reconciliationSha256=sha(V / "batch-094-reconciliation.json"))
    p["quizSafeguardCorrection679"].update(status="resolved-original-session-confirmations-complete",
                                          revisedSnapshot=freeze["snapshot"])
    for row in p["wordQuizAudit"]["directExclusions"]:
        row["status"] = "confirmed-original-sessions"
    p["pendingGates"] = p["pendingGates"][1:]
    assert p["reviewClosed"] == p["published"] == []
    assert not p["runtimeAccepted"] and not p["runtimePublished"]
    save(S / "batch-094-progress.json", p)
    for src, dst in [
        (Path(__file__), V / "close-batch-094-textual-679.py"),
        (C / "correct-batch-094-679.py", V / "confirm-batch-094-original-sessions-679.py"),
    ]:
        shutil.copyfile(src, dst)
    save(S / "execution-679.json", {
        "schemaVersion": 1, "execution": 679, "batch": "094", "stage": STAGE,
        "initialTeachingSnapshot": m.INITIAL, "revisedTeachingSnapshot": freeze["snapshot"],
        "previousEvidenceCheckpoint": m.HEAD,
        "startingState": load(C / "progress.json")["execution679StartingState"],
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "findingsResolved": 1, "directQuizPairsResolved": 3,
        "originalSessionConfirmations": confirmed,
        "audit": "docs/n1-sources/batch-094-correction-audit-679.json",
        "checks": rec["correctionChecks"], "focusedTestsPassed": 43, "validatorErrors": 0,
        "reconciliation": "docs/n1-reviews/batch-094-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-094-reconciliation.json"),
        "contentVersion": rec["contentVersion"], "allRuntimePayloadHashesVerified": 8438,
        "articleBodiesChanged": False, "freshAndroidOrNativeClaimed": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "publishedAdditions": 120, "remainingAdditions": 1108, "wholeProjectComplete": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "limits": rec["limits"],
    })
    assert not git("diff", freeze["snapshot"], "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    print("Both original confirmations archived and textual-only closure reconciled.")


def verify():
    m.identity(clean=True)
    freeze, confirmed = records()
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == freeze["snapshot"]
    assert not git("diff", freeze["snapshot"], head, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for name, value in freeze["runtimeHashes"].items():
        assert sha(R / name) == value
    rec = load(V / "batch-094-reconciliation.json")
    evidence = load(S / "execution-679.json")
    assert evidence["reconciliationSha256"] == sha(V / "batch-094-reconciliation.json")
    assert rec["textualReviewClosed"] and not rec["runtimeAccepted"] and not rec["runtimePublished"]
    assert rec["actionableRemainingDirectPairs"] == 0 and rec["actionableRemainingFindingGroups"] == 0
    for row in evidence["checks"].values():
        assert sha(R / row["path"]) == row["sha256"]
    assert m.build_manifest(R) == load(R / "manifest.json")
    m.batch_audit(R, "094")
    return head, freeze, confirmed


def seal():
    head, freeze, confirmed = verify()
    p = load(C / "progress.json")
    original = load(L / "progress-before-679.json")
    assert p["checkpoint"] == 678 and p["batch"] == "094"
    cp = {
        "schemaVersion": 1, "execution": 679, "checkpoint": 679, "batch": "094",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": m.INITIAL, "reviewedTeachingSnapshot": freeze["snapshot"],
        "lastPublishedCommit": p["lastPublishedCommit"], "evidence": "docs/n1-sources/execution-679.json",
        "sourcePacket": "docs/n1-sources/batch-094-progress.json",
        "reconciliation": "docs/n1-reviews/batch-094-reconciliation.json",
        "textualReviewClosed": True, "runtimeDrafted": ["削"], "reviewClosed": [], "published": [],
        "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": list(m.MODELS.values()), "originalSessionConfirmations": 2,
        "serialReviewerExitAndScopeReverified": True, "bothConfirmationFullPacketsReturned": True,
        "acceptedUnresolvedFindingGroups": 0, "acceptedUnresolvedDirectQuizPairs": 0,
        "newDirectWordExclusionPairsApplied": 3, "articleBodiesChanged": False,
        "contentVersion": load(R / "manifest.json")["contentVersion"],
        "completeDictionaryFamilies": 121, "familyOccurrences": 125,
        "confirmationCompleteApplicableFamilies": 5, "completeRawCharacterRecords": 10,
        "metadataReadings": 4, "curatedOfferedKeys": 2, "newSupportArticles": 0,
        "reusedSupportArticles": 2, "changedReusedArticles": 3,
        "allMappedReciprocalPairs": 3, "directedLinksVerified": 6, "activatedBaselinePairs": 2,
        "generatedStrokePaths": 9, "actualHanCount": 41,
        "pendingNativeFallbackLabels": ["刂", "斫", "氵", "阝"],
        "allRuntimePayloadHashesVerified": 8438, "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=679, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution679CoordinatorCheckpoint"] = cp
    p["batch094TextualClosureCheckpoint"] = copy.deepcopy(cp)
    p["execution679StartingState"]["status"] = "signed-local-textual-closure-checkpoint-complete"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-094-textual-679-seal.json", cp)
    save(L / "checkpoint-679.json", cp)
    body = (
        f"Batch 094: three source-backed direct quiz safeguards applied and TEXTUAL review closed "
        f"at normally signed LOCAL checkpoint 679 `{head}` (signature G); revised teaching "
        f"`{freeze['snapshot']}`. NOT native acceptance or publication.\n\n"
        "Only append 除く and 外す to 削る's original exclusion list, and 省く to 削除's list. "
        "All original exclusions/order, titles, N2 levels, identities, primary readings and complete "
        "article bodies preserved. Full サク and けず.る/はつ.る/そ.ぐ remain in source order; "
        "explicit [サク]/[けず.る] offers only さく/けずる. No new support words, geometry or link changes.\n\n"
        "Original Claude Opus 5.5 (claude-opus-5.5, edf22897-9f87-4a3b-b20f-4c2fd839013a) then "
        "GPT-6.1 Sol (gpt-6.1-sol, 65fd64ff-aae2-40af-927e-bf19b52fecb6) resumed SERIAL read-only "
        "CLI confirmations on the same signed revised snapshot. Each read its own original report, "
        "exact diff, seven complete articles, five complete applicable JMdict families, two committed "
        "public extracts and pairwise quiz contract in exactly ONE full view call. Actual models, "
        "exact full returned packets, no overlap/truncation/unfinished tools and actual process exit "
        "before next launch verified. Reports/executions/packets/provenance retained in docs/n1-reviews. "
        "These are original-session bounded confirmations, NOT new blind reviews, fresh121family "
        "inspection, independent upstream retrieval or comprehension certification.\n\n"
        "All three direct pairs resolved; no actionable textual defect or consequential unresolved "
        "teaching claim remains. Correctness/scoped coverage/text comprehensibility CLEAN in bounded "
        "scope for complete 削/削る/削除 and added 除 navigation passage. Claude retracted the prior "
        "broad guard-coverage claim in part; its 削除/省く low-risk hypothesis resolves. That observation "
        "remains SHARED, not uniquely GPT; GPT uniquely established the other two initial missing "
        "pairs. Optional polish remains optional. Closure follows exact sources/labels/pair contract, "
        "not votes; production live pools are not certified.\n\n"
        "Fresh validator0, regenerated manifest eeae47753a460f72,43 focused tests, vocabulary consistency "
        "and unchanged budgets passed. Complete baseline985kanji/4942words/985strokes preserved with "
        "documented prior exceptions plus these three additive guards. Five frozen input hashes, "
        "full applicable dictionary extractions, tenrawrecords, fourreadingdispositions/twokeys, "
        "threeallmappedpairs/sixdirections/twoactivatedpairs, ninepinnedpaths, all41Han/fontcmaps "
        "and8438runtimepayloadhashes mechanically verified. Local archive8460entries/"
        "30270285compressed/44601491inflated/44333153retained bytes, below original guards.\n\n"
        "Next SAME094: fresh THREE RealContentTest/ONE RareHanTest with no skips against actual sibling, "
        "then fullarchive productionContentSyncONCE/native N1/All production choices/three directguards/"
        "onlyさく,けずる/ninestroke drawing/articles/SystemBack/offline/all41Han/fourfonts and original-session "
        "rendered confirmations. 刂/斫/氵/阝 cmap absence is NOT glyphfailure. Qualified TESTONLY "
        "Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. No new Android/native claim here. "
        "All original combined-main/nonrewritingmerge/reviewchangedteaching/checks/normalsigning/"
        "ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/unchangedbudgets/media/path/"
        "verifiedownerissue gates remain.\n\n"
        "Published120/1228 and1108acceptanceremainder unchanged; lastpublishedmain48765e20846e1d6769c6ddc35146f6ce58deab57. "
        "Compatiblef9b59a2+ client required; physicalphone/generalrelease/whole-set explicitly outstanding. "
        "Dedicated worktrees clean; no095, unreviewedpush or secondrunner. Parent19008 retainsrunner.lock "
        "untouched; no childacquire/delete/unlock, optional historical-session helper access or actualnewdenial. "
        "progress.json preserves complete history with statuscontinue."
    )
    (C / "batch-094-textual-679-issue-body.txt").write_text(body, encoding="utf-8")
    print("Signed textual-only checkpoint679 sealed; complete history preserved:", head)


def final():
    head, freeze, confirmed = verify()
    body = C / "batch-094-textual-679-issue-body.txt"
    posted = load(C / "batch-094-textual-679-issue-posted.json")
    actual = load(C / "batch-094-textual-679-issue-reread.json")
    assert actual["id"] == posted["id"] and actual["user"]["login"] == "stop-cran"
    assert actual["body"].encode("utf-8") == body.read_bytes()
    receipt = {"id": actual["id"], "url": actual["html_url"], "author": "stop-cran",
               "bodySha256": sha(body), "verified": True, "comparison": "Exact UTF-8 bytes."}
    p, before = load(C / "progress.json"), load(L / "progress-before-679.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (679, "094", "continue", STAGE)
    assert p["nextAction"] == NEXT and p["blocker"] is None
    assert p["lastPublishedCommit"] == before["lastPublishedCommit"] and p["remainingAdditions"] == 1108
    for key in ["execution679CoordinatorCheckpoint", "batch094TextualClosureCheckpoint"]:
        assert p[key]["savedCommit"] == head
        p[key].update(issueUpdate=receipt["url"], ownerIssueAuthorAndBodyVerified=True)
    p["batch094TextualClosureIssueReceipt"] = receipt
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(C / "batch-094-textual-679-issue-receipt.json", receipt)
    save(L / "checkpoint-679.json", p["execution679CoordinatorCheckpoint"])
    save(C / "batch-094-textual-679-final-verification.json", p["execution679CoordinatorCheckpoint"])
    print("Verified signed clean checkpoint679; historical root values preserved:", len(before), receipt["url"])


if __name__ == "__main__":
    import sys
    {"prepare": prepare, "seal": seal, "final": final}[sys.argv[1]]()
