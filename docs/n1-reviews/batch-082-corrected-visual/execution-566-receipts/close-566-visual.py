import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("execution", C / "execution-566.py")
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)
R, A, N, V, WORK, E = x.R, x.A, x.N, x.V, x.WORK, x.E
load, save, sha, git, now = x.load, x.save, x.sha, x.git, x.now


def audit_processes():
    x.frozen()
    previous = None
    process = {}
    for family in ["claude", "gpt"]:
        prefix = f"batch-082-visual-{family}"
        row = load(V / (prefix + "-execution.json"))
        assert row["processAndCoverageAccepted"] and row["completePacketReturned"]
        assert row["actualModels"] == [x.v.SESSIONS[family][0]]
        assert row["sessionId"] == x.v.SESSIONS[family][1]
        assert row["distinctImagePayloadsVerified"] == 28 and len(row["turns"]) == 30
        assert sha(V / (prefix + ".md")) == row["reportSha256"]
        assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(row["startedAt"])
        previous = row["completedAt"]
        for i, t in enumerate(row["turns"]):
            assert t["singleResourceAccepted"] and t["exitCode"] == 0
            if i:
                assert datetime.fromisoformat(row["turns"][i-1]["completedAt"]) < datetime.fromisoformat(t["startedAt"])
            if "imagePayload" in t:
                assert sha(R / t["imagePayload"]["returnedPayloadCopy"]) == t["imagePayload"]["sha256"]
        events = [json.loads(s) for s in Path(row["rawExecutionLocation"]).read_text(
            encoding="utf-8-sig").splitlines() if s.strip()]
        process[family] = {
            **{k: row[k] for k in ["requestedModel", "actualModels", "sessionId", "startedAt",
                                  "completedAt", "reportSha256", "rawExecutionSha256"]},
            "execution": prefix + "-execution.json", "report": prefix + ".md",
            "observations": prefix + "-observations.md",
            "compactionEventTypes": sorted({e["type"] for e in events if "compact" in e["type"]}),
            "sourceDimensions": sorted({tuple(t["imagePayload"]["sourceDimensions"])
                                        for t in row["turns"] if "imagePayload" in t}),
            "returnedDimensions": sorted({tuple(t["imagePayload"]["returnedDimensions"])
                                          for t in row["turns"] if "imagePayload" in t}),
        }
    return process


def validate():
    x.frozen()
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from build_manifest import build_manifest
    result = audit(R, "082")
    assert load(R / "manifest.json") == build_manifest(R)
    assert load(R / "manifest.json") == json.loads(git("show", f"{x.HEAD}:manifest.json"))
    save(WORK / "mechanical-verification.json", {"batchAudit": result, **x.runtime()})
    print("Exact manifest, 8372 runtime hashes and complete batch mechanical audit verified.")


def record():
    processes = audit_processes()
    validate()
    native = load(N / "attempt-565" / "execution.json")
    pngs = [name for name in native["artifacts"] if name.endswith(".png")]
    assert len(native["artifacts"]) == 54 and len(pngs) == 51
    assert set(pngs) == {p.name for p in (N / "attempt-565").glob("*.png")}
    assert native["passed"] and native["terminalSuccessCases"] == 2
    assert all(c["status"] == 0 for c in native["terminalCases"])
    verdicts = {
        name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
               "boundedVisualComprehensibility": "CLEAN"}
        for name in ["kanji/准.md", "words/准教授.md", "kanji/教.md:39 added bullet",
                     "words/助教授.md:15-18 successor paragraph/link"]
    }
    limits = [
        "Dependent original-session visual confirmations, not new blind initial linguistic reviews, fresh dictionary retrieval or reviewer-executed native tests. Original textual/source findings and all historical denial/OOM/citation/lookup/reading/process limitations remain.",
        "Both families received complete source packet and28 direct original-path image payloads serially;51 captures include23 byte aliases, not51 independent reviewer reads. Source1080x2400 returned900x2000, not original-resolution bytes or comprehension certification.",
        "Claude final report discloses resources1-6 summarized out of retained context; GPT resources1-14 likewise. Complete original per-turn observations preserved. No equal live-context depth claim.",
        "Exact default-four N1 question accepted. All-stack candidate availability/source reasoning is inherited, not a separately captured All quiz. Custom/partial/larger/future pools including prior準hypothesis remain uncertified.",
        "Rare准える imitation remains recognized; ordinary standalonefrequency/learnerimpact unproven, not invalidated. Historical contrary initial calibrations retained, not resolved by voting.",
        "All34Han/fourfamilies and whole准教授 visible across threeComposepanels.136individual+4wholewordPaint assertions are not140 PNG reads or fallback-face identification. Fine inline radical/stroke detail limited at returned size; prior all40 evidence inherited.",
        "Complete articles readable collectively across vertical/table horizontal states, not all columns simultaneously. Six linkdirections/SystemBack/offline/import/persistence depend additionally on supplied fixture/route/terminal, not stills alone.",
        "563HOST3+1+5/no skips/564compile/565two corrected native terminal0 cases inherited, not rerun here. QualifiedTESTONLYAndroid1c1b7bf4 preserves productionf9b59a2, not latestappmain; no heap/guard increase.",
        "Disposable API35read-only emulator and injected reference trace/shape-only/giveup recall are not humanhandwriting/memory/MLKitrecognition/modeldownload/phone/native-speaker/learningeffectiveness evidence.",
        "Combined-current-main integration, fullPython/vocabulary/budget/finalmanifest audits, normal signedownerfastforward, remoteSHA/CI/exactimmutableZIP and publication outstanding. Physicalphone/generalrelease/whole-set acceptance remains outstanding.",
        "No new runtime edit, HOST/native run, optionalhistoricalsessionhelper access, actual new permission denial, publication,083 or secondrunner.",
    ]
    reconciliation = {
        "schemaVersion": 1, "execution": 566, "batch": "082", "status": x.STAGE,
        "evidenceHead": x.HEAD, "reviewedTeachingSnapshot": x.TEACHING,
        "nativeArchiveSnapshot": "e108bbeb0fcd4fda3837d955a652f662f72fdac1",
        "contentVersion": "d82e7fefe3898a70",
        "reviewType": "Dependent original-session changed-runtime visual confirmations; original two-family blind initials and source-correction confirmations retained.",
        "processes": processes,
        "process": {
            "oneReviewerFamilyActiveAtATime": True, "hostDispatchedChildrenPerFamily": 30,
            "sourcePacketsPerFamily": 1, "distinctPngsPerFamily": 28,
            "zeroToolFinalReportTurnsPerFamily": 1, "allChildrenExitedBeforeNext": True,
            "firstFamilyReportAndEvidenceArchivedBeforeSecondLaunch": True,
            "availableTools": ["view"], "observedToolOverlaps": 0, "unfinishedTools": 0,
            "commonTaskAndSourceAccess": True, "otherReportOrCoordinatorVerdictSupplied": False,
            "runtimeEditsDuringReviews": False,
        },
        "coverage": {
            "originalPngs": 51, "distinctByteGroupsPerFamily": 28, "byteAliasCaptures": 23,
            "completePacketReturnedBothFamilies": True, "originalAndReturnedPayloadsPreserved": True,
            "sourceByteIdenticalReturnedImages": 0,
            "claudeReadDepth": "All29resources directly returned serially. Final report discloses resources1-6 summarized out of context; original observations retained.",
            "gptReadDepth": "All29resources directly returned serially. Final report discloses resources1-14 summarized out of context; original observations retained.",
        },
        "verdicts": verdicts, "findings": [],
        "actionableRemainingFindings": 0, "consequentialUnresolvedScopedClaims": 0,
        "reconciliation": [
            {"id": "082-V1", "status": "resolved", "facets": ["runtime quiz correctness", "coverage"],
             "severity": "Original moderate-if-confirmed calibration retained in561; corrected source availability defect and bounded runtime now closed.",
             "location": "kanji/准.md:13",
             "evidence": "Actual source correction9ce870d1, both original source-confirmations562, fresh correctedHOST563/native565 exactfour assertions and new566question/feedback PNG reads.",
             "reason": "Actual four complete labels map to准/冴/冶/隼 and no imitate/倣/tagfallback. Existing complete source families support distinctness; both original reviewers now agree bounded closure. No old pixels substituted or linguistic rarity used as disproof.",
             "confidence": "High for exact default-four configuration; excluded pools remain uncertified."},
            {"claim": "Both scoped new articles and two reused changes readable with corrected glyphs.",
             "status": "resolved", "scope": "All34Han/fourfamilies/whole准教授, complete articles across scrolling, exact教bullet/助教授successor paragraph. Not physical-phone or fallback-face certification."},
            {"claim": "Claude resource1/final53PNG-versus51capture discrepancy.",
             "status": "withdrawn", "scope": "Coordinator counted exact original execution.json:54artifact filenames=51PNG+3nonPNG(routeJSON/treeTXT/rasterJSON); actual51PNGfiles and28hashgroups. Reviewer arithmetic unsupported; original report preserved verbatim, not rewritten. This did not omit an image or change learning evidence."},
            {"claim": "word-forward-13 filename proves a准教授 destination.",
             "status": "withdrawn", "scope": "Both reviewers' observations correctly identify actual准 article; filename alone not navigation evidence. Actual fixture/route/assertions supply transitions. No false destination inferred."},
            {"claim": "Shared raster hashes prove a particular fallback face.",
             "status": "withdrawn", "scope": "Claude resource1 used stronger shared-fallback shorthand; final reports correctly bound it to consistency, not face identification. No teaching or production font edit."},
            {"claim": "Inline fine radical detail, extra compounds/readings examples, optional Notes for new distractors, unlinked授, wrappedkana and transient model/loading UX.",
             "status": "optional", "scope": "No demonstrated learning defect. Large panels distinguishradicals, table scrolling signposted,授card absent; no invented support/UXfix."},
            {"claim": "Humanrecall/recognition/MLKitdownload/phone/generalrelease and arbitrary pool safety.",
             "status": "unresolved", "scope": "Explicitly outside this bounded acceptance, not claimed; currentpublication/whole-set gates retained."},
        ],
        "modelContributionComparison": {
            "shared": "AllfouritemsCLEAN; no scoped actionable defect. Both independently inspected corrected labels/glyphs/articles and closed own082-V1 runtime claim. Both noted filename-versus-visiblearticle and stills-versus-route limits anywhere in report/observations.",
            "claudeOnlyVerifiedUseful": "Detailed fine-inline-radical and optional expansion notes, largely inherited; no unique actionable defect.53PNG arithmetic claim unsupported and corrected by exact receipt count.",
            "gptOnlyVerifiedUseful": "No unique verified actionable defect. Explicit final filename caution overlaps Claude's per-turn note, not a unique discovery.",
            "limits": "Compared full final reports and all per-turn observations/findings/optional/limits. Different compressed-history ranges preclude equal retained-context claims; no model ranking.",
        },
        "independentVisualInspectionComplete": True, "independentVisualAcceptance": True,
        "fontInspectionAccepted": True, "runtimeAccepted": True, "runtimePublished": False,
        "teachingChanges": [], "newHostOrNativeRuns": 0, "nextBatchStarted": False,
        "limits": limits, "nextAction": x.NEXT,
    }
    save(V / "reconciliation.json", reconciliation)
    ledger_path = R / "docs" / "n1-sources" / "batch-082-progress.json"
    ledger = load(ledger_path)
    ledger["preCorrectedVisual566AcceptanceState"] = {
        k: ledger[k] for k in ["status", "reviewClosed", "runtimeAccepted",
                              "independentVisualAcceptance", "nextAction", "limits", "fontDisposition"]
    }
    ledger.update(
        status=x.STAGE, reviewClosed=["准"], runtimeAccepted=True,
        independentVisualInspectionComplete=True, independentVisualAcceptance=True,
        correctedTeachingSnapshot=x.TEACHING,
        correctedVisualEvidence="docs/n1-reviews/batch-082-corrected-visual/reconciliation.json",
        unresolvedRuntimeClaims=[], nextAction=x.NEXT, limits=limits,
        fontDisposition="Both original families directly received corrected threeComposepanels:34Han/fourfamilies+whole准教授 distinguishable; fineinline/resized/fallback-face limits retained. No physicalphone claim.",
    )
    save(ledger_path, ledger)
    receipts = V / "execution-566-receipts"
    receipts.mkdir(exist_ok=False)
    for path in [Path(__file__), C / "execution-566.py", C / "review-batch-082-visual.py",
                 C / "post-566-issue.ps1", WORK / "validate.txt", WORK / "manifest.txt",
                 WORK / "mechanical-verification.json"]:
        shutil.copyfile(path, receipts / path.name)
    save(E, {
        **load(WORK / "starting-state.json"), "schemaVersion": 1, "checkpoint": 566,
        "status": "continue", "stage": x.STAGE, "completedAt": now(),
        "reconciliation": "docs/n1-reviews/batch-082-corrected-visual/reconciliation.json",
        "reconciliationSha256": sha(V / "reconciliation.json"),
        "processes": processes, "independentVisualAcceptance": True,
        "resolvedRuntimeFinding": "082-V1 exact default-four configuration",
        "runtimeAccepted": True, "runtimePublished": False, "runtimeBytesUnchanged": True,
        "newHostOrNativeRuns": 0, "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": load(WORK / "progress-before.json")["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "validatorErrors": 0, "manifestFresh": True,
        **load(WORK / "mechanical-verification.json"),
        "validationReceipts": [{"path": p.relative_to(R).as_posix(), "sha256": sha(p)}
                               for p in sorted(receipts.iterdir())],
        "nextAction": x.NEXT, "limits": limits,
    })
    print("Both complete corrected visual reports and bounded082-V1 resolution recorded.")


def checkpoint():
    before = load(WORK / "progress-before.json")
    p = load(C / "progress.json")
    ev = load(E)
    signed = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == x.HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "HEAD", root=A) == x.AH
    assert not git("diff", x.HEAD, "HEAD", "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    receipt = load(WORK / "issue-receipt.json")
    body = (WORK / "issue-body.txt").read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").strip() == body and signed in body
    for row in ev["validationReceipts"]:
        assert sha(R / row["path"]) == row["sha256"]
    result = {
        "schemaVersion": 1, "execution": 566, "checkpoint": 566, "batch": "082",
        "savedCommit": signed, "signature": "G", "status": "continue", "stage": x.STAGE,
        "evidence": E.relative_to(R).as_posix(), "evidenceSha256": sha(E), **x.runtime(),
        "reviewedTeachingSnapshot": x.TEACHING, "qualifiedAndroidHead": x.AH,
        "independentVisualAcceptance": True, "runtimeAccepted": True,
        "runtimePublished": False, "runtimeBytesUnchanged": True,
        "resolvedRuntimeFinding": "082-V1 bounded default-four scope only",
        "serialReviewerChildren": 60, "allChildrenExitedZero": True,
        "sourcePacketsPerFamily": 1, "distinctPngGroupsPerFamily": 28, "originalPngs": 51,
        "actualModels": [x.v.SESSIONS[f][0] for f in ["claude", "gpt"]],
        "dedicatedWorktreesClean": True, "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "newHostOrNativeRuns": 0, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": x.NEXT, "blocker": None,
    }
    p.update({k: result[k] for k in ("checkpoint", "status", "stage", "nextAction", "blocker")})
    p["execution566StartingState"]["status"] = "signed-local-corrected-visual-checkpoint-complete"
    p["execution566CoordinatorCheckpoint"] = result
    p["batch082CorrectedVisualAcceptance"] = result.copy()
    changed = [key for key, value in before.items() if p.get(key) != value]
    assert not set(changed) - {"checkpoint", "status", "stage", "nextAction", "blocker"}, changed
    assert before.keys() <= p.keys()
    result.update(originalRootKeysCompared=len(before),
                  allOriginalHistoricalRootKeysPreservedExactly=True, changedRootFields=changed)
    temporary = WORK / "progress.tmp.json"
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")
    persisted = load(C / "progress.json")
    assert all(persisted[k] == value for k, value in before.items() if k not in changed)
    save(WORK / "final-verification.json", result)
    print(json.dumps({k: result[k] for k in ("checkpoint", "savedCommit", "status", "issueUpdate",
                                             "originalRootKeysCompared")}))


def seal():
    x.frozen()
    validate()
    check = subprocess.run(
        ["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check"],
        capture_output=True, encoding="utf-8")
    assert check.returncode in (0, 2)
    headers = [line for line in check.stdout.splitlines() if line.startswith("docs/")]
    allowed = {
        "batch-082-visual-gpt-observations.md", "batch-082-visual-gpt.md",
        "batch-082-visual-source-packet.txt", "cli-catalog-execution-566.txt",
    }
    assert all(line.split(":")[0].split("/")[-1] in allowed for line in headers)
    assert all(": trailing whitespace." in line or ": new blank line at EOF." in line
               for line in headers)
    save(V / "whitespace-disposition.json", {
        "execution": 566, "checkExitCode": check.returncode, "originalOutput": check.stdout,
        "warningCount": len(headers),
        "decision": "Preserve exact complete reviewer report/observations Markdown hard linebreak, reviewed line-numbered packet blank rows and CLI catalog terminal blank line. No runtime/authored-code whitespace warning, report rewriting or production lint exception."
    })
    staged = git("diff", "--cached", "--name-only").splitlines()
    assert staged and all(name.startswith("docs/") for name in staged)
    assert not git("diff", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    ev = load(E)
    receipts = V / "execution-566-receipts"
    for path in [Path(__file__), C / "execution-566.py", C / "review-batch-082-visual.py",
                 C / "post-566-issue.ps1", WORK / "validate.txt", WORK / "manifest.txt",
                 WORK / "mechanical-verification.json"]:
        shutil.copyfile(path, receipts / path.name)
    ev.update(
        validationReceipts=[{"path": p.relative_to(R).as_posix(), "sha256": sha(p)}
                            for p in sorted(receipts.iterdir())],
        whitespaceDisposition="docs/n1-reviews/batch-082-corrected-visual/whitespace-disposition.json",
        **load(WORK / "mechanical-verification.json"),
    )
    save(E, ev)
    print("Signed-checkpoint evidence sealed; only unchanged verbatim-evidence whitespace preserved.")


if __name__ == "__main__":
    {"audit": audit_processes, "validate": validate, "record": record,
     "seal": seal, "checkpoint": checkpoint}[sys.argv[1]]()
