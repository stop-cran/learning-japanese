import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual084", C / "review-batch-084-visual.py")
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)
R, A, V, LOG = x.R, x.A, x.V, x.LOG
E = R / "docs" / "n1-sources" / "execution-588.json"
STAGE = "native-and-original-family-visual-accepted-awaiting-combined-main"
NEXT = (
    "SAME084 fresh latest-main normal integration and combined-tree acceptance NEXT, then bounded "
    "authorized publication only when all gates pass; no085 until remote acceptance/checkpoint. "
    "Read signed execution-588.json and batch-084-visual-reconciliation.json, preserving original584 "
    "textual,585HOST4,586compile/fixture,587native and588complete visual reports/addenda. "
    "Both ORIGINAL ClaudeOpus5.5 session45e7798c-3f2b-45f4-85ce-5f00db7cc847 and GPT6.1Sol "
    "sessionaa972b37-2d13-4edc-8636-f2896ef9c3ad confirmed unchanged teaching030b144a/runtime53b6819b/"
    "version74b87b47347b78c1, complete commonpacket and25 distinct original PNGs representing42captures; "
    "54 serial child exits plus two serial original-native-pixel detail addenda verified. "
    "All28Han/fourfamilies/twospellings and actualN1meaning/soleon/drawing/articles/Back readable "
    "within captured scope. Main900x2000payloads downscaled from1080x2400; lossless632x760 crop "
    "disambiguates native-panel凜禾-bottom/凛示-bottom for both; no originalfullframe-resolution/"
    "everyfine-stroke/bodytextmicroscopic/otherdensity/physicalphone/fallbackface certification. "
    "Claude remaining smaller-body/phone uncertainty outside exactcrop is explicitly retained, not "
    "universal glyph failure or unqualified全sizegreen. Source-onlykun in reference/feedback retained "
    "with no kunquestion; feedbackqualifier/grade/downloadwording observations optional and app-level, "
    "no prerequisite defect established. C1optional/C2withdrawn/C3defaultresolved-largerpoolunverified "
    "unchanged. FreshHOST4passed585/no skips; bothRetry1native terminalcase0/no skips passed587: "
    "productionContentSync fullgitONCE1096kanji5053words116N1/zeroProblems/version74b87b47347b78c1/"
    "acceptedepoch1; Full/Lite fullリン/きびし.い retained, curatedリン/kun[], soleりん persistedgood/done; "
    "default4N1ANDAll exact凜/准/冗/凹 IDs+actuallabels/allthreecuratedavailable/nopadding; actualN1UI, "
    "not AllUI/custom/padded/partial/larger/reversepool safety. Onepair/twodirections/twocompletearticles/"
    "SystemBack/offline/selection/15reference-injectedstrokes/trace/giveuprecall/gradepersisted, NOT "
    "humanhandwriting/MLKitrecognition/modeldownload/phone. QualifiedTESTONLYAndroid1c1b7bf4 atop "
    "unchangedproductionf9; no freshHOST/native rerun absent changedruntime/newconcern. "
    "Require freshorigin/main nonrewritingmerge/surgicalreconciliation, independently review substantive "
    "changedteaching, regenerate manifest and combinedPythonunittest/validate/vocabulary/freshness/"
    "membership-baseline-links/exact8379hashes-or-accountedmergechanges/budgets and applicable "
    "non-skippedAndroid on actualcombinedtree. Original18000entries/42MiBcompressed/80MiBinflated/"
    "56MiBretained/perfile-media-safepath guards unchanged. Then normal signedownerfastforward/"
    "exactremote/terminalgreenCI/EVERYimmutablepublicZIPentryhash/verifiedownerissue60 BEFORE085. "
    "No unreviewedpush. Parent19008 runner.lock untouched; liveancestry/session/checkpoint/signedheads/"
    "whollycleanworktrees verified. Approvedcontrol/committedsources only, no optionalhistoricalsession "
    "recipes; preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "If justifiedfuture native needed, freshly inspect bothlocalANDremote5580/5581 inclTimeWait/"
    "devices/PIDs immediately before approvedownedreadonlyAPI35N3_Acceptance_20261029 emulator5580/"
    "hostGPU/-Vulkan/2048MiB2cores; no alternateport without routingauthorization/shareddeviceinterference/"
    "heapguardincrease; stoponlyownedhelper. Originaldenials/OOM/source/readdepth/process/reviewlimits "
    "remain. Published110/1228,1118remaining/latestpublic73b19c3e unchanged;084 localreviewclosed "
    "notpublished/finallyaccepted. Physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def audit_processes():
    freeze = x.frozen()
    result = {}
    previous = None
    for kind in ["visual", "visual-detail"]:
        for family, (model, session) in x.SESSIONS.items():
            prefix = f"batch-084-{kind}-{family}"
            row = x.load(V / (prefix + "-execution.json"))
            assert row["processAndCoverageAccepted"] and row["actualModels"] == [model]
            assert row["sessionId"] == session and row["exitCode"] == 0
            assert x.sha(V / (prefix + ".md")) == row["reportSha256"]
            raw = Path(row["rawExecutionLocation"])
            assert x.sha(raw) == row["rawExecutionSha256"]
            if previous:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(row["startedAt"])
            previous = row["completedAt"]
            events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
            active = set()
            calls = 0
            for event in events:
                data = event.get("data", {})
                if event["type"] == "tool.execution_start":
                    assert not active and data["toolName"] == "view"
                    active.add(data["toolCallId"])
                    calls += 1
                elif event["type"] == "tool.execution_complete":
                    assert data["success"] and data["toolCallId"] in active
                    active.remove(data["toolCallId"])
            assert not active and calls == (26 if kind == "visual" else 1)
            if kind == "visual":
                assert len(row["turns"]) == 27 and row["completePacketReturned"]
                assert row["distinctImagePayloadsVerified"] == 25
                for i, turn in enumerate(row["turns"]):
                    assert turn["exitCode"] == 0 and turn["singleResourceAccepted"]
                    if i:
                        assert datetime.fromisoformat(row["turns"][i-1]["completedAt"]) < datetime.fromisoformat(turn["startedAt"])
                    if "imagePayload" in turn:
                        assert x.sha(R / turn["imagePayload"]["returnedPayloadCopy"]) == turn["imagePayload"]["sha256"]
            else:
                assert row["originalPixelEquivalentReturned"]
                assert row["returnedDimensions"] == [632, 760]
                assert x.sha(V / (prefix + "-returned.png")) == row["returnedPayloadSha256"]
            result[f"{kind}-{family}"] = {
                **{key: row[key] for key in ["actualModels", "sessionId", "startedAt", "completedAt",
                                            "reportSha256", "rawExecutionSha256"]},
                "report": prefix + ".md", "execution": prefix + "-execution.json",
                "verifiedChildExits": 27 if kind == "visual" else 1,
                "successfulSerialViews": calls,
                "compactionEventTypes": sorted({e["type"] for e in events if "compact" in e["type"]}),
            }
    return freeze, result


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    from audit_n1_batch import audit

    manifest = x.load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest == json.loads(x.git(R, "show", f"{x.CONTENT}:manifest.json"))
    assert not x.git(R, "diff", x.HEAD, "--", "kanji", "words", "articles",
                     "strokes", "manifest.json", "tools")
    return {
        "runtimeBytesUnchanged": True, "manifestFresh": True,
        "contentVersion": manifest["contentVersion"], "runtimeHashesVerifiedAtPreparation": 8379,
        "batchAudit": audit(R, "084"),
    }


def record():
    freeze, processes = audit_processes()
    verification = runtime()
    native = x.load(R / "docs" / "n1-sources" / "execution-587.json")["nativeAcceptance"]
    assert native["nativeAcceptancePassed"] and native["nativeSkips"] == 0
    assert len(native["caseResults"]) == 2 and all(row["status"] == 0 for row in native["caseResults"])
    limits = [
        "Dependent original-session visual confirmations plus focused native-pixel addenda, not new blind/source reviews or reviewer-executed native tests. Original initial/confirmation reports and historical source/lookup/read-depth/denial/OOM/process limitations retained.",
        "Each family received complete same packet and25 direct original-path image payloads representing42captures by exact-byte aliases; not42 separate independent reads. Source1080x2400 returned900x2000. All56 child exits and54 successful views audited serially; bytes/receipt counts are not comprehension certification.",
        "Lossless sourcepanel3 crop632x760 returned at original pixel dimensions/equivalent RGBA, no resampling/enlargement. Both original families resolved captured-panel凜/凛 recognition. Claude retains smaller-body/otherdensity/phone/everyfine-stroke uncertainty; do not convert this into full-scale/bodyfont certification or erase that distinction. No demonstrated misleading glyph; bounded recognition sufficient, not every stroke at every scale.",
        "Claude says no native-font evidence on a device: read as no physical-device evidence; actual Android native emulator renders and two native cases are separately proven. Fallback-like appearance/raster convergence does not identify a face. Fine stroke-number labels and険/鷹 details limited in downscaled fullframes; all28 recognized, not stroke-by-stroke certification.",
        "Both article bodies collectively visible across scroll states, horizontal reading-table cells and wordwrap retained. Scroll snapshots do not show every heading simultaneously or every microscopic bottom-component detail. Route captures and exact-byte aliases not independent second captures/transitions.",
        "Claude optional source-onlykun in feedback summary/trace grading wording/transient download notice overlap GPT resource observations or final limits; no unique required content fix. Full source metadata remains reference material; source-only kun not offered. App mechanisms unchanged.",
        "Original C1 spellingpriority optional preference retained, C2涼しい hypothesis withdrawn, C3 defaultresolved while larger/custom/random/padded/partial/reverse exposure remains unverified. AllUI not exercised; default N1 andAll builder IDs/titles asserted, actual N1UI visually inspected.",
        "FreshHOST4zero-skips585/compile586/native587two terminal0 cases inherited, not rerun. TESTONLYAndroid1c1b7bf4 atop unchangedproductionf9. FullContentSyncONCE/1096kanji5053words116N1/zeroProblems/epoch1 and Full/Lite/readings/persistedgood are supplied execution evidence, not pixelsalone.",
        "One reciprocalpair/twodirections/SystemBack/offline and persistence rely on native fixture/route/terminal, not screenshotsalone. Synthetic disposable source and seeded meaning logs are not owner progress; no drawing state preseeded.",
        "15 injected reference strokes, shape-only feedback, recall give-up and saved grade are not human handwriting/MLKitrecognition/modeldownload/phone. Offline unavailablemodel disclosed; pending download status not success.",
        "Latest-main integration/combined tests/normal signedownerpush/remoteCI/EVERY immutable publicZIP hash and originalarchiveguards remain required. Physicalphone/generalrelease/whole-set outstanding. No nextbatch, newHOST/native, optional historical-session artifact or parentlock access.",
    ]
    verdicts = {
        name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
               "renderedComprehensibility": "CLEAN", "limits": "Bounded captured recognition and legibility, not all scales/devices/fine strokes."}
        for name in ["kanji/凜.md", "words/凜.md"]
    }
    reconciliation = {
        "schemaVersion": 1, "execution": 588, "batch": "084", "status": STAGE,
        "evidenceHead": x.HEAD, "teachingSnapshot": x.TEACHING, "contentSnapshot": x.CONTENT,
        "contentVersion": "74b87b47347b78c1", "processes": processes,
        "process": {
            "oneReviewerFamilyActiveAtATime": True, "all56ChildrenExitedZero": True,
            "firstOriginalReportArchivedBeforeSecondLaunch": True,
            "sameTaskSourceImages": True, "otherReportOrCoordinatorVerdictSupplied": False,
            "availableTools": ["view"], "observedToolOverlaps": 0, "unfinishedTools": 0,
            "runtimeEditsDuringReviews": False,
        },
        "coverage": {
            "packetBytes": freeze["packetBytes"], "packetLines": freeze["packetLines"],
            "completePacketReturnedBothFamilies": True, "originalPngs": 42,
            "distinctOriginalPngsPerFamily": 25, "exactByteAliases": 17,
            "mainSourceDimensions": [1080, 2400], "mainReturnedDimensions": [900, 2000],
            "detailNativePixelCropDimensions": [632, 760], "detailOriginalPixelsReturnedBothFamilies": True,
            "all28HanAcrossFourFamiliesRecognizable": True,
            "capturedPanelVariantDistinctionResolvedBoth": True,
            "allSmallerBodyTextFineStrokesOrPhysicalPhoneCertified": False,
        },
        "verdicts": verdicts, "findings": [], "actionableRemainingFindings": 0,
        "consequentialUnresolvedScopedClaims": 0,
        "reconciliation": [
            {"claim": "Captured-panel凜/凛 distinction uncertain after full-frame downscaling.",
             "status": "resolved", "confidence": "Claude moderately high; GPT high.",
             "evidence": "Exact original-pixel crop with native dimensions/equivalent returnedRGBA, both original addenda identify禾-versus示 bottoms; no collapse/blank. Smallerbody/otherdevice certification remains excluded."},
            {"claim": "All scales/body-font fine strokes/phone fallbackface.",
             "status": "unresolved", "scope": "Not claimed or required as universal certification. Claude's broader qualification retained; actual captured shapes recognized, no established defect."},
            {"claim": "Reading feedback fullsourcekun/grade wording/transient model-download text.",
             "status": "optional", "scope": "Existing app-level observations, no new content defect or prerequisite established; not altered."},
            {"id": "084-C1", "status": "optional", "scope": "Original historical newspaper-priority preference, no teaching change."},
            {"id": "084-C2", "status": "withdrawn", "scope": "No demonstrated displayed-label ambiguity requiring exclusion."},
            {"id": "084-C3", "status": "partially resolved",
             "scope": "Defaultfour N1/All builder and actualN1UI resolved; larger/custom/random/partial/padded/reverse pools unverified."},
            {"claim": "Phone/generalrelease/recognition/unrestrictedpools and combinedpublication acceptance.",
             "status": "unresolved", "scope": "Explicitly outstanding/outside bounded assertions, no waiver."},
        ],
        "modelContributionComparison": {
            "shared": "Both complete reports/observations establish bounded twoarticleCLEAN, no actionable defect, defaultchoices/sourcekun/wordwrap/route-versus-pixels/MLKit/phone/publication distinctions.",
            "claudeOnlyVerifiedUseful": "Explicit fine-bottom/downscale uncertainty prompted native-pixel crop; resolved for panelrecognition by both addenda. Not a discovered teaching defect or general model benchmark.",
            "gptOnlyVerifiedUseful": "No unique actionable defect. Feedback sourcekun and pendingdownload cautions occur in GPT observations, so not credited as Claude-only discoveries.",
            "unsupportedOrQualified": "Specific sharedfallbackface not identified; both qualify. Claude blanket no native-font/device evidence limited to no physicalphone; actual emulator native frames exist. Everyfine-stroke/allscale/bodyfont certification not supplied.",
            "limits": "Complete reports and per-resource observations compared including optional/limits, no model ranking/equal retained comprehension claim.",
        },
        "independentVisualAcceptance": True, "runtimeAccepted": True,
        "runtimeAcceptanceScope": "Local bounded content/native/rendered acceptance, not combined-main/publication/general release.",
        "runtimePublished": False, "teachingChanges": [], "newHostOrNativeRuns": 0,
        "nextBatchStarted": False, "limits": limits, "nextAction": NEXT,
    }
    x.save(V / "batch-084-visual-reconciliation.json", reconciliation)
    path = V / "batch-084-reconciliation.json"
    ledger = x.load(path)
    ledger["preVisual588AcceptanceState"] = {
        key: ledger.get(key) for key in ["status", "runtimeAccepted", "runtimePublished", "limits"]}
    ledger.update(status=STAGE, runtimeAccepted=True, runtimePublished=False,
                  independentVisualAcceptance=True, visualConfirmation="batch-084-visual-reconciliation.json")
    x.save(path, ledger)
    path = R / "docs" / "n1-sources" / "batch-084-progress.json"
    ledger = x.load(path)
    ledger["preVisual588AcceptanceState"] = {
        key: ledger.get(key) for key in ["status", "reviewClosed", "runtimeAccepted", "nextAction", "limits"]}
    ledger.update(status=STAGE, reviewClosed=["凜"], runtimeAccepted=True,
                  independentVisualAcceptance=True, published=[],
                  visualEvidence="docs/n1-reviews/batch-084-visual-reconciliation.json",
                  nextAction=NEXT, visualLimits=limits)
    path.write_text(json.dumps(ledger, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    receipts = V / "batch-084-visual-recipes"
    receipts.mkdir(exist_ok=False)
    for path in [Path(__file__), C / "review-batch-084-visual.py",
                 C / "confirm-batch-084-glyph-detail.py", C / "post-batch-084-visual-588.ps1"]:
        shutil.copyfile(path, receipts / path.name)
    x.save(E, {
        "schemaVersion": 1, "execution": 588, "batch": "084", "status": "continue", "stage": STAGE,
        "startingState": x.load(C / "progress.json")["execution588StartingState"],
        "teachingSnapshot": x.TEACHING, "contentSnapshot": x.CONTENT,
        "reconciliation": "docs/n1-reviews/batch-084-visual-reconciliation.json",
        "reconciliationSha256": x.sha(V / "batch-084-visual-reconciliation.json"),
        "processes": processes, "independentVisualAcceptance": True, "runtimeAccepted": True,
        "runtimePublished": False, "newHostOrNativeRuns": 0, **verification,
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": "73b19c3eafb75721add6c8e333a1c3bef9e960d7",
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "limits": limits,
    })
    print("Both complete visual reports/addenda reconciled; local gate closed, publication remains gated.")


def seal():
    verification = runtime()
    assert "0 error(s)" in (LOG / "visual-588-validate.txt").read_text(encoding="utf-8")
    receipts = V / "batch-084-visual-recipes"
    for path in [LOG / "visual-588-validate.txt", LOG / "visual-588-manifest.txt"]:
        shutil.copyfile(path, receipts / path.name)
    checked = subprocess.run(["git", "--no-pager", "-C", str(R), "diff", "--check"],
                             capture_output=True, encoding="utf-8")
    assert checked.returncode == 0, checked.stdout
    staged = x.git(R, "diff", "--cached", "--name-only").splitlines()
    assert staged and all(name.startswith((
        "docs/n1-reviews/batch-084-visual-", "docs/n1-reviews/batch-084-reconciliation.json",
        "docs/n1-sources/batch-084-progress.json", "docs/n1-sources/execution-588.json"))
        for name in staged)
    checked = subprocess.run(["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check"],
                             capture_output=True, encoding="utf-8")
    warnings = [line for line in checked.stdout.splitlines() if line.startswith("docs/")]
    allowed = {
        "batch-084-visual-source-packet.txt", "batch-084-visual-claude-observations.md",
        "batch-084-visual-gpt-observations.md", "batch-084-visual-copilot-help-execution-588.txt",
        "batch-084-visual-copilot-model-catalog-execution-588.txt",
    }
    assert checked.returncode in (0, 2)
    assert all(line.split(":")[0].split("/")[-1] in allowed for line in warnings), checked.stdout
    assert all(": trailing whitespace." in line or ": new blank line at EOF." in line
               for line in warnings), checked.stdout
    x.save(V / "batch-084-visual-whitespace-disposition.json", {
        "execution": 588, "checkExitCode": checked.returncode, "originalOutput": checked.stdout,
        "warningCount": len(warnings),
        "decision": "Preserve exact line-numbered supplied packet, CLI captures and original observations; no authored runtime/code whitespace exception.",
    })
    evidence = x.load(E)
    evidence.update(**verification, validatorErrors=0,
                    recipeReceipts=[{"path": str(path.relative_to(R)), "sha256": x.sha(path)}
                                    for path in sorted(receipts.iterdir())],
                    whitespaceDisposition="docs/n1-reviews/batch-084-visual-whitespace-disposition.json")
    x.save(E, evidence)
    print("Validation, unchanged runtime and complete evidence receipts sealed.")


def issue_body():
    signed = x.git(R, "rev-parse", "HEAD")
    assert x.git(R, "rev-parse", "HEAD^") == x.HEAD
    assert x.git(R, "log", "-1", "--format=%G?") == "G"
    assert not x.git(R, "status", "--porcelain")
    body = (
        f"Batch 084 checkpoint 588: local two-family dependent visual acceptance saved at signed `{signed}` "
        "(not pushed or counted as delivered).\n\n"
        "Original Claude Opus 5.5 and GPT-6.1 Sol sessions each inspected the same complete packet and 25 "
        "distinct native PNGs representing all 42 captures. Both original reports and observations are preserved. "
        "A lossless original-pixel crop and two serial addenda resolve panel-size 凜/凛 distinguishability; "
        "56 child processes exited 0 with serial read-only tools. No actionable teaching defect remains within "
        "the captured scope. Smaller-body fine detail/other densities and physical-phone behavior are not certified. "
        "No teaching/runtime changes or new native/host run. Earlier two native cases and four non-skipped host "
        "cases remain inherited, not rerun.\n\n"
        "C1 optional spelling-priority note, C2 withdrawn and C3 default-resolved/larger-pool-unverified stay "
        "unchanged. Feedback source-only reading/grade wording observations remain optional app-level notes, "
        "not changes in this content task. Injected tracing and unavailable offline handwriting model are not "
        "human recognition or phone acceptance.\n\n"
        "Next: SAME084 latest-main normal integration and combined-tree acceptance, then authorized publication "
        "only after normal signing, owner fast-forward, terminal CI, every immutable ZIP runtime hash and "
        "unchanged archive/path/media budgets. No085 yet. Published remains **110/1,228; 1,118 remaining**. "
        "Physical-phone/general-release and whole-set acceptance remain outstanding; the project is incomplete.\n\n"
        "Evidence: `docs/n1-sources/execution-588.json` and "
        "`docs/n1-reviews/batch-084-visual-reconciliation.json`. Parent launcher retains runner.lock; "
        "no child acquisition/deletion/unlock, no optional historical-session helper access and no new denial."
    )
    target = C / "batch-084-visual-588-issue.txt"
    assert not target.exists()
    target.write_text(body + "\n", encoding="utf-8")
    print(signed)


def checkpoint():
    before = x.load(LOG / "progress-before-588.json")
    progress = x.load(C / "progress.json")
    signed = x.git(R, "rev-parse", "HEAD")
    assert x.git(R, "rev-parse", "HEAD^") == x.HEAD
    for root in [R, A]:
        assert x.git(root, "log", "-1", "--format=%G?") == "G"
        assert not x.git(root, "status", "--porcelain", "--untracked-files=all")
    assert x.git(A, "rev-parse", "HEAD") == x.APP
    evidence = x.load(E)
    for row in evidence["recipeReceipts"]:
        assert x.sha(R / row["path"]) == row["sha256"]
    receipt = x.load(C / "batch-084-visual-588-issue-verified.json")
    body = (C / "batch-084-visual-588-issue.txt").read_text(encoding="utf-8")
    norm = lambda text: text.replace("\r\n", "\n").rstrip()
    assert receipt["user"]["login"] == "stop-cran" and norm(body) == norm(receipt["body"])
    assert signed in body
    cp = {
        "schemaVersion": 1, "execution": 588, "checkpoint": 588, "batch": "084",
        "savedCommit": signed, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-588.json", "evidenceSha256": x.sha(E),
        "independentVisualAcceptance": True, "runtimeAccepted": True, "runtimePublished": False,
        "runtimeBytesUnchanged": True, "serialReviewerChildren": 56, "allChildrenExitedZero": True,
        "sourcePacketsPerFamily": 1, "distinctPngGroupsPerFamily": 25, "originalPngs": 42,
        "nativePixelDetailAddenda": 2, "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "newHostOrNativeRuns": 0, "dedicatedWorktreesClean": True,
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": "73b19c3eafb75721add6c8e333a1c3bef9e960d7",
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    progress.update({key: cp[key] for key in ["checkpoint", "status", "stage", "nextAction", "blocker"]})
    progress["execution588CoordinatorCheckpoint"] = cp
    progress["batch084VisualAcceptanceCheckpoint"] = cp.copy()
    progress["batch084VisualIssueReceipt588"] = {
        "url": receipt["html_url"], "author": "stop-cran", "bodyVerified": True,
        "commentId": receipt["id"], "localSignedEvidenceCommit": signed, "runtimePublished": False,
        "receiptSha256": x.sha(C / "batch-084-visual-588-issue-verified.json"),
        "globalAccountUnchanged": True,
    }
    permitted = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert before.keys() <= progress.keys()
    assert all(progress[key] == value for key, value in before.items() if key not in permitted)
    x.persist(progress)
    persisted = x.load(C / "progress.json")
    assert all(persisted[key] == value for key, value in before.items() if key not in permitted)
    changed = x.git(R, "diff-tree", "--no-commit-id", "--name-only", "-r", signed).splitlines()
    for name in changed:
        blob = subprocess.check_output(["git", "-C", str(R), "show", f"{signed}:{name}"])
        assert blob == (R / name).read_bytes().replace(b"\r\n", b"\n") if not name.endswith(".png") else blob == (R / name).read_bytes()
    x.save(LOG / "execution-588-final-verification.json", {
        **cp, "committedEvidenceFilesByteVerified": len(changed),
        "runtimeVerification": runtime(),
    })
    print(f"Signed checkpoint588 verified; {len(before)} historical root values preserved; {receipt['html_url']}")


if __name__ == "__main__":
    {"record": record, "seal": seal, "issue-body": issue_body, "checkpoint": checkpoint}[sys.argv[1]]()
