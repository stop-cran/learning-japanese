import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime

from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual", C / "review-batch-083-visual.py")
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)
R, A, V, N, LOG = x.R, x.A, x.V, x.N, x.LOG
load, save, sha, git = x.load, x.save, x.sha, x.git
E = R / "docs" / "n1-sources" / "execution-579.json"
STAGE = "corrected-native-and-original-family-visual-accepted-awaiting-combined-main"
NEXT = (
    "SAME083 latest-main normal integration and combined-tree acceptance NEXT, then persist/yield "
    "before publication if needed; no084. Read signed execution-579.json, batch-083-visual-reconciliation.json "
    "and original578/577/576/575/574 evidence. Both original ClaudeOpus5.5 and GPT6.1Sol serially "
    "confirmed unchanged teaching7cc896f4/evidence2f24c5c4 via complete same source packet and31 "
    "distinct original PNGs representing56captures; actual models/66child exits/oneviewperresource verified. "
    "All30Han/fourfamilies/two wholewords, actualN1meaning/readings/drawing/articles/Back visually accepted "
    "within captured scope. Word-body headings aboveMeaning not directly captured; full source and native "
    "heading-existence assertions supplied, appbar/readings/wholewordpanels visible, no established rendering "
    "defect; not full heading pixel certification. Finaltree loading capture not settled UI evidence; "
    "cleanup-timing hypothesis unverified. Source1080x2400 returned900x2000; no full-resolution/fallback-face/"
    "equalretained-context certification. 083-NATIVE-574-CHOICE resolved textual+native+boundedvisual, "
    "actualclear;sharp-minded wrong for凌 despite genuine冴skill/excel-at secondary senses; no universal "
    "synonym-disjointness/AllUI/custom/random/padded/partial/larger/reversepool safety. Original574failure "
    "and reports immutable. Fresh577HOST4noskips/compile and578both correctednativecases terminal0, "
    "productionContentSyncONCE1095kanji5052words115N1/version6dfe6a1e287ce5df/zeroProblems/epoch1, "
    "N1ANDAll default4 exact凌/准/冶/冴 IDs+titles/all3available/no padding, Full/Lite/rawcuration and "
    "independentlypersisted soleりょう/しのぐ inherited, not rerun absent actual change/newconcern. "
    "Ten injectedreference strokes/giveuprecall/gradeonNext NOT humanrecognition/MLKit/phone; "
    "offline handwritingmodel unavailable honest. SignedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9. "
    "Require freshorigin/main normalnonrewritingmerge, combinedPythonunittest/validate/vocabulary/"
    "manifestfreshness/exact8376hashes-or-accountedmergedchanges/baseline/link/membership/exact17guards/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretained budgets and applicable non-skipped "
    "Android checks for actual combinedtree; substantive changedteaching independentboundedrereview. "
    "Then normal signedownerfastforward/exactremote/terminalgreenCI/EVERYimmutableZIPhash/"
    "verifiedownerissue60 BEFORE084. Do not publish unreviewed teaching. Parent19008runner.lock "
    "untouched; approvedcontrolhelpers/committedsources only/nooptionalhistoricalsessionhelpers. "
    "Preserve/report/yield actualnewdenial/signinghang. No native rerun now; if truly needed fresh "
    "localANDremote5580/5581 inclTimeWait/devices/PIDs/liveparentancestry, ownedreadonlyAPI35hostGPU/"
    "-Vulkan/2048MiB2cores/explicitserial5580/noalternateport/no shareddeviceinterference/unchangedheaps/"
    "guards/ownedonlycleanup; one heavy process. All inherited source/reviewer/readdepth/process/OOM/"
    "denial/viewport limitations retained. Published109/1228,remaining1119/latestpublic21a5cb1328aadd437139a6b850f07298a2e2985d "
    "unchanged;083 not delivered. Physicalphone/generalrelease/whole-set outstanding."
)


def process_audit():
    f = x.frozen()
    processes = {}
    previous = None
    for family, (model, session) in x.SESSIONS.items():
        prefix = f"batch-083-visual-{family}"
        row = load(V / (prefix + "-execution.json"))
        assert row["processAndCoverageAccepted"] and row["completePacketReturned"]
        assert row["actualModels"] == [model] and row["sessionId"] == session
        assert row["distinctImagePayloadsVerified"] == 31 and len(row["turns"]) == 33
        assert sha(V / (prefix + ".md")) == row["reportSha256"]
        assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(row["startedAt"])
        previous = row["completedAt"]
        for i, turn in enumerate(row["turns"]):
            assert turn["singleResourceAccepted"] and turn["exitCode"] == 0
            if i:
                assert datetime.fromisoformat(row["turns"][i-1]["completedAt"]) < datetime.fromisoformat(turn["startedAt"])
            if "imagePayload" in turn:
                assert sha(R / turn["imagePayload"]["returnedPayloadCopy"]) == turn["imagePayload"]["sha256"]
        events = [json.loads(s) for s in Path(row["rawExecutionLocation"]).read_text(
            encoding="utf-8-sig").splitlines() if s.strip()]
        active, overlaps, calls = set(), [], 0
        for event in events:
            data = event.get("data", {})
            if event["type"] == "tool.execution_start":
                if active:
                    overlaps.append(data["toolCallId"])
                active.add(data["toolCallId"])
                calls += 1
                assert data["toolName"] == "view"
            elif event["type"] == "tool.execution_complete":
                active.remove(data["toolCallId"])
                assert data["success"]
        assert not active and not overlaps and calls == 32
        processes[family] = {
            **{k: row[k] for k in ["requestedModel", "actualModels", "sessionId", "startedAt",
                                  "completedAt", "reportSha256", "rawExecutionSha256"]},
            "execution": prefix + "-execution.json", "report": prefix + ".md",
            "observations": prefix + "-observations.md", "verifiedChildExits": 33,
            "compactionEventTypes": sorted({e["type"] for e in events if "compact" in e["type"]}),
            "sourceDimensions": sorted({tuple(t["imagePayload"]["sourceDimensions"])
                                        for t in row["turns"] if "imagePayload" in t}),
            "returnedDimensions": sorted({tuple(t["imagePayload"]["returnedDimensions"])
                                          for t in row["turns"] if "imagePayload" in t}),
        }
    return f, processes


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    from audit_n1_batch import audit

    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest == json.loads(git(R, "show", f"{x.HEAD}:manifest.json"))
    audit_result = audit(R, "083")
    return {"manifestFresh": True, "runtimeBytesUnchanged": True, "batchAudit": audit_result}


def record():
    f, processes = process_audit()
    verification = runtime()
    native = load(R / "docs" / "n1-sources" / "execution-578.json")
    assert native["nativeAcceptance"]["nativeAcceptancePassed"]
    assert len(native["nativeAcceptance"]["independentlyParsedTerminalCases"]) == 2
    assert all(c["status"] == 0 for c in native["nativeAcceptance"]["independentlyParsedTerminalCases"])
    limits = [
        "Dependent original-session visual confirmations, not new blind initial/source reviews or reviewer-executed native tests. Both original blind reports and choice confirmations retained; all inherited exact-source/citation/lookup/reading/denial/OOM/process limits remain.",
        "Both families received complete same packet and31 direct original-path image payloads serially;56captures include25 exact-byte aliases, not56 independent reads. Source1080x2400 returned900x2000; no original-resolution or equal comprehension/retained-context claim. Complete per-turn observations retained.",
        "Word-body headings/readings aboveMeaning not directly shown in captured frames. Full source reviewed; native fixture awaits exact headings at308/340 without assertIsDisplayed/capture of heading. Appbar titles, linked kana and wholewordpanels readable. No established rendering failure, but do not claim every heading directly visually confirmed.",
        "Finaltree contains loading/All0 state, not settled-screen acceptance. Both reports note this; Claude's likely-cleanup-timing hypothesis not established: fixture dumps tree in finally before scenario.close. Stable selection PNG and earlier assertions/route prove bounded exercised state, not finaltree timing/cause.",
        "Claude's opening074 label is an unsupported transcription typo; actualfinding083-NATIVE-574-CHOICE throughout reports/source/receipts. Original report preserved verbatim; no new074 finding or altered historical report.",
        "Claude's shared-fallback shorthand supported only as appearance consistency; no fallback-face identification from raster/cmap/pixels. All30Han/fourfamilies and two wholewords readable; finehook/inline detail limited by resized view. Prior all40font inspection inherited.",
        "Full default-four productionQuizBuilder N1 andAll asserted in578; actualN1UI labels independently inspected here. AllUI/custom/padded/partial/larger/reverse/random pools uncertified. 冴skill/excel-at secondary sense retained; actualclear/sharp-minded label wrong for凌, not universally disjoint families.",
        "Fresh577HOST4no-skips/compile and578two correctednative terminal0cases inherited, not rerun; TESTONLYAndroid1c1b7bf4 atop unchangedproductionf9, notlatestappmain. FullContentSyncONCE/8376hashes/1095kanji5052words115N1/version6dfe6a1e287ce5df/zeroProblems/epoch1, Full/Lite/soleりょうしのぐ/persistence supplied execution, not pixelsalone.",
        "Two mapped reciprocalpairs/fourdirections, SystemBack/offline and source/persistence depend on supplied fixture/route/terminal, not screenshots alone. Filename forward can capture originating kanji, not prove a word destination.",
        "Ten reference-injectedtouchstrokes/shapeonlyfeedback/giveuprecall/gradeonNext not humanhandwriting/successfulrecall/MLKit/modeldownload/phone. Offline unavailablemodel shown honestly; transient downloading notice not success.",
        "Current-main integration/combined tests/normal signedownerpush/remoteCI/exactimmutableZIP and publication outstanding; physicalphone/generalrelease/whole-set acceptance outstanding. No newHOST/native/media/algorithm/otherbatch, optional historical helper or parentlock access.",
    ]
    verdicts = {
        name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
               "boundedVisualComprehensibility": "CLEAN", "limits": "Captured scope; see coverage limits."}
        for name in ["kanji/凌.md", "words/凌ぐ.md", "words/凌駕.md"]
    }
    reconciliation = {
        "schemaVersion": 1, "execution": 579, "batch": "083", "status": STAGE,
        "evidenceHead": x.HEAD, "reviewedTeachingSnapshot": x.TEACHING,
        "nativeArchiveSnapshot": "867fe8bef228145ef0a6e48690941b0a0aa50336",
        "contentVersion": "6dfe6a1e287ce5df", "processes": processes,
        "process": {"oneReviewerFamilyActiveAtATime": True, "hostDispatchedChildrenPerFamily": 33,
                    "sourcePacketsPerFamily": 1, "distinctPngsPerFamily": 31,
                    "allChildrenExitedBeforeNext": True, "firstReportArchivedBeforeSecondLaunch": True,
                    "availableTools": ["view"], "observedToolOverlaps": 0, "unfinishedTools": 0,
                    "sameTaskSourceImages": True, "otherReportOrCoordinatorVerdictSupplied": False,
                    "runtimeEditsDuringReviews": False},
        "coverage": {"originalPngs": 56, "distinctPngGroupsPerFamily": 31, "byteAliases": 25,
                     "completePacketReturnedBothFamilies": True,
                     "packetBytes": f["packetBytes"], "packetLines": f["packetLines"],
                     "originalAndReturnedPayloadsPreserved": True,
                     "sourceByteIdenticalReturnedImages": 0,
                     "all30HanAcrossFourFamiliesAndBothWholewordsInspected": True,
                     "wordBodyHeadingPixelsConfirmed": False},
        "verdicts": verdicts, "findings": [], "actionableRemainingFindings": 0,
        "consequentialUnresolvedScopedClaims": 0,
        "reconciliation": [
            {"id": "083-NATIVE-574-CHOICE", "status": "resolved",
             "scope": "Textual576/native578/boundedvisual579 defaultfour completeN1ANDAll builder and actualN1UI only.",
             "evidence": "Corrected次N3→冴N1; both original textual confirmations, fresh578two terminal0/native exactIDs+titles and579actualquestion/feedback PNG reads; original574failure immutable.",
             "confidence": "High within exact tested configuration; all other pools excluded."},
            {"claim": "30Han and two wholewords/fourfonts, three article bodies across scroll states, actual quizzes/routes/drawing readable.",
             "status": "resolved", "scope": "Bounded returned pixels plus supplied native assertions; word-body heading pixels/fine-detail limits remain."},
            {"claim": "Final All0 tree proves settled UI regression or cleanup cause.",
             "status": "unresolved", "scope": "Timing/cause not established, not a demonstrated defect. Do not certify settled state from tree; actual PNGs and assertions separate."},
            {"claim": "Every word heading directly captured.", "status": "withdrawn",
             "scope": "Full source/native node existence, appbar and linked readings supplied; no directbodyheadingcapture; no demonstrated learning defect."},
            {"claim": "Shared glyph/raster indicates specific fallbackface; reportopening074 identifies a newfinding.",
             "status": "withdrawn", "scope": "Consistency only; unsupported shorthand/transcription, original reports retained."},
            {"claim": "Weather wording/extra defy-slight gloss, unchanged冴N1fallback/paddedpool observations, wrappedkana/transientmodel/shapegrade UI wording.",
             "status": "optional", "scope": "No demonstrated new scoped learning defect; no legacy or app edits."},
            {"claim": "Phone/generalrelease/recognition/unrestrictedpool and combinedpublication acceptance.",
             "status": "unresolved", "scope": "Explicitly outstanding or outside bounded assertion; no waiver."},
        ],
        "modelContributionComparison": {
            "shared": "AllthreearticlesCLEAN and boundedchoice/runtime/rendering closure; both distinguish finalloadingtree/stills-versus-route/faceidentity/MLKit/phone limits anywhere in observations/final.",
            "claudeOnlyVerifiedUseful": "Explicit uncaptured word-bodyheading limit; preserved as coveragequalification, not demonstrated teaching/rendering defect. Detailed optional whitespace/UI notes, not required fixes. Cleanup timing hypothesis unsupported.",
            "gptOnlyVerifiedUseful": "No unique actionable defect; concise timing/filename and suppliedexecution caveats overlap Claude observations.",
            "limits": "Compared complete reports and all observations, including optional/limits. Actual returnedranges do not prove equal comprehension or retained context; no model ranking.",
        },
        "independentVisualInspectionComplete": True, "independentVisualAcceptance": True,
        "runtimeAccepted": True, "runtimePublished": False, "teachingChanges": [],
        "newHostOrNativeRuns": 0, "nextBatchStarted": False, "limits": limits, "nextAction": NEXT,
    }
    save(V / "batch-083-visual-reconciliation.json", reconciliation)
    path = V / "batch-083-reconciliation.json"
    ledger = load(path)
    ledger["preVisual579Status"] = {k: ledger.get(k) for k in
                                 ["status", "runtimeAccepted", "runtimePublished", "limits"]}
    ledger.update(status=STAGE, runtimeAccepted=True, runtimePublished=False,
                  independentVisualAcceptance=True,
                  visualConfirmation="batch-083-visual-reconciliation.json")
    save(path, ledger)
    path = R / "docs" / "n1-sources" / "batch-083-progress.json"
    ledger = load(path)
    ledger["preVisual579AcceptanceState"] = {k: ledger.get(k) for k in
                                          ["status", "reviewClosed", "runtimeAccepted", "nextAction", "limits"]}
    ledger.update(status=STAGE, reviewClosed=["凌"], runtimeAccepted=True,
                  independentVisualAcceptance=True, published=[],
                  visualEvidence="docs/n1-reviews/batch-083-visual-reconciliation.json",
                  nextAction=NEXT, visualLimits=limits)
    save(path, ledger)
    receipts = V / "batch-083-visual-recipes"
    receipts.mkdir(exist_ok=False)
    for path in [Path(__file__), C / "review-batch-083-visual.py",
                 C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt"]:
        shutil.copyfile(path, receipts / path.name)
    save(E, {
        "schemaVersion": 1, "execution": 579, "batch": "083", "status": "continue", "stage": STAGE,
        "startingState": load(C / "progress.json")["execution579StartingState"],
        "evidenceHead": x.HEAD, "reviewedTeachingSnapshot": x.TEACHING,
        "reconciliation": "docs/n1-reviews/batch-083-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-083-visual-reconciliation.json"),
        "processes": processes, "independentVisualAcceptance": True, "runtimeAccepted": True,
        "runtimePublished": False, "resolvedFinding": "083-NATIVE-574-CHOICE bounded defaultfour",
        "newHostOrNativeRuns": 0, **verification,
        "publishedAdditions": 109, "remainingAdditions": 1119, "lastPublishedCommit": x.BASE,
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "limits": limits,
        "recipeReceipts": [{"path": str(path.relative_to(R)), "sha256": sha(path)}
                           for path in sorted(receipts.iterdir())],
    })
    print("Both complete original-family visual confirmations reconciled; publication remains gated.")


def checkpoint():
    before = load(LOG / "progress-before-579.json")
    p = load(C / "progress.json")
    signed = git(R, "rev-parse", "HEAD")
    assert git(R, "rev-parse", "HEAD^") == x.HEAD and git(R, "log", "-1", "--format=%G?") == "G"
    assert not git(R, "status", "--porcelain") and not git(A, "status", "--porcelain")
    assert git(A, "rev-parse", "HEAD") == x.APP
    assert not git(R, "diff", x.HEAD, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    receipt = load(C / "batch-083-visual-579-issue-verified.json")
    body = (C / "batch-083-visual-579-issue.txt").read_text(encoding="utf-8")
    norm = lambda s: s.replace("\r\n", "\n").rstrip()
    assert receipt["user"]["login"] == "stop-cran" and norm(body) == norm(receipt["body"])
    assert signed in body
    ev = load(E)
    for row in ev["recipeReceipts"]:
        assert sha(R / row["path"]) == row["sha256"]
    cp = {
        "schemaVersion": 1, "execution": 579, "checkpoint": 579, "batch": "083",
        "savedCommit": signed, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-579.json", "evidenceSha256": sha(E),
        "independentVisualAcceptance": True, "runtimeAccepted": True, "runtimePublished": False,
        "runtimeBytesUnchanged": True, "serialReviewerChildren": 66, "allChildrenExitedZero": True,
        "sourcePacketsPerFamily": 1, "distinctPngGroupsPerFamily": 31, "originalPngs": 56,
        "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"], "newHostOrNativeRuns": 0,
        "resolvedFinding": "083-NATIVE-574-CHOICE bounded defaultfour",
        "dedicatedWorktreesClean": True, "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": x.BASE, "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p.update({k: cp[k] for k in ["checkpoint", "status", "stage", "nextAction", "blocker"]})
    p["execution579CoordinatorCheckpoint"] = cp
    p["batch083CorrectedVisualAcceptance"] = cp.copy()
    p["batch083CorrectedVisualIssueReceipt"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "localSignedEvidenceCommit": signed,
        "runtimePublished": False, "globalAccountUnchanged": True,
        "receiptSha256": sha(C / "batch-083-visual-579-issue-verified.json"),
        "normalization": "GitHub CRLF normalized to LF; terminal whitespace trimmed only.",
    }
    permitted = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert before.keys() <= p.keys()
    assert all(p[k] == value for k, value in before.items() if k not in permitted)
    x.persist(p)
    persisted = load(C / "progress.json")
    assert all(persisted[k] == value for k, value in before.items() if k not in permitted)
    changed = git(R, "diff-tree", "--no-commit-id", "--name-only", "-r", signed).splitlines()
    for name in changed:
        blob = subprocess.check_output(["git", "-C", str(R), "show", f"{signed}:{name}"])
        assert blob == (R / name).read_bytes(), name
    save(LOG / "execution-579-final-verification.json", {
        **cp, "committedEvidenceFilesByteVerified": len(changed),
        "runtimeVerification": runtime(), "issueReceiptSha256": sha(C / "batch-083-visual-579-issue-verified.json"),
    })
    print(f"Signed checkpoint579 verified; {len(before)} historical root values preserved; {receipt['html_url']}")


def seal():
    verification = runtime()
    ev = load(E)
    receipts = V / "batch-083-visual-recipes"
    for path in [LOG / "visual-579-validate.txt", LOG / "visual-579-manifest.txt",
                 Path(__file__), C / "post-579-issue.ps1"]:
        shutil.copyfile(path, receipts / path.name)
    assert "0 error(s)" in (LOG / "visual-579-validate.txt").read_text(encoding="utf-8")
    staged = git(R, "diff", "--cached", "--name-only").splitlines()
    assert staged and all(name.startswith(("docs/n1-reviews/batch-083-visual-",
                                         "docs/n1-reviews/batch-083-reconciliation.json",
                                         "docs/n1-sources/batch-083-progress.json",
                                         "docs/n1-sources/execution-579.json")) for name in staged)
    result = subprocess.run(["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check"],
                            capture_output=True, encoding="utf-8")
    assert result.returncode in (0, 2)
    warnings = [line for line in result.stdout.splitlines() if line.startswith("docs/")]
    allowed = {"batch-083-visual-source-packet.txt", "batch-083-visual-gpt-observations.md",
               "batch-083-visual-claude-observations.md",
               "batch-083-visual-copilot-help-execution-579.txt",
               "batch-083-visual-copilot-model-catalog-execution-579.txt"}
    assert all(line.split(":")[0].split("/")[-1] in allowed for line in warnings), result.stdout
    assert all(": trailing whitespace." in line or ": new blank line at EOF." in line
               for line in warnings), result.stdout
    save(V / "batch-083-visual-whitespace-disposition.json", {
        "execution": 579, "checkExitCode": result.returncode, "originalOutput": result.stdout,
        "warningCount": len(warnings),
        "decision": "Preserve exact reviewed line-numbered source packet/CLI capture whitespace and original reviewer observations. No runtime or authored code whitespace exception.",
        "initialSealDiagnostic": "Initial seal stopped on original Claude observation423 containing a two-space blank line. Added this exact original-report file to evidence-only dispositions; no report byte changed, denial or validation failure.",
    })
    ev.update(**verification, runtimeHashesVerified=8376, validatorErrors=0,
              recipeReceipts=[{"path": str(path.relative_to(R)), "sha256": sha(path)}
                              for path in sorted(receipts.iterdir())],
              whitespaceDisposition="docs/n1-reviews/batch-083-visual-whitespace-disposition.json")
    save(E, ev)
    print("Validation receipts and exact original-report whitespace disposition sealed.")


if __name__ == "__main__":
    {"record": record, "checkpoint": checkpoint, "seal": seal}[sys.argv[1]]()
