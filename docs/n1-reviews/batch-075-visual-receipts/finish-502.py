import ast
from datetime import datetime
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

spec = importlib.util.spec_from_file_location("execution502", Path(__file__).with_name("execution-502.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
L, C, R, V, F = m.L, m.C, m.R, m.V, m.F

NEXT = (
    "SAME075 visual evidence reconciled at502; no publication/076 this checkpoint. Read "
    "docs\\n1-sources\\execution-502.json and batch-075-visual-reconciliation.json. "
    "Two-family bounded visual conclusions CLEAN for complete典/香典 and tenexact reused "
    "passages; no actionable teaching/rendering defect. Claude originalsession51uniquePNG "
    "plus actuallyserialonepacket correction; originalvisual ONE response THREE concurrent "
    "fixture reads121-480/TWOoverlaps remains noncompliant, originalflagFALSE; initial498 "
    "EIGHTmultitool/THIRTYoverlaps/false serial claim also preserved. GPT originalsession "
    "125serialcalls/101PNGreturns/50repeatedreads certified27/51only; originalpartialreport/"
    "withdrawnunsupportedobservations remain. FreshGPT isolatedsession24missingPNG onceeach "
    "actuallyvisible/26serialcalls completes inherited27+fresh24; not51freshreads or "
    "retroactive originalapproval. All4reviewerprocesses exited sequentially; actualmodels "
    "claude-opus-5.5/gpt-6.1-sol. Full743linefixture/13contextfiles/terminal+route returned "
    "tooriginalreviewers; all111originalPNG=51unique+60hashduplicates. Fullrawテン/デン,"
    "ふみ/のり order; selectedbothon/emptykun, actualてん/でん feedback+Done2correct/"
    "noKunLog, eightreference-touchstrokes/ungradedtrace/recallAgain, all12mappedpairs"
    "24directions/SystemBack/offline and fourproductionfontrows all117Han+sixwords accepted "
    "within suppliedAPI35scope; fallbackface/phone not identified. Newfrozen teachingf5b70805/"
    "nativeenvelopefba1a886 version2759d7b13c89eb8f/Androidf9b59a2 unchanged. Inherit "
    "498textual372tests/499freshHOST3+1/501native2terminal0noskips, no redundant reruns. "
    "NEXT freshfetchorigin/main/nonrewritingmergeifneeded and validate actualcombined "
    "source/membership/baseline/readings/quiz/links/fonts/strokes/Python/vocab/validator/"
    "freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained; "
    "normalsigning/authorizedownerfastforward/publicSHA/terminalgreenCI/EVERYimmutable"
    "publicZIPruntimehash+budgets/ownerissue60 BEFOREdelivery or076. Preserve FULLlivehistory/"
    "originalreports/failedarchiverdiagnostics/allhistoricaldenials and baseline虎猿丘山 "
    "exceptions. No signingretry/permissionworkaround/heaporguardchanges/authoragents/"
    "secondrunner/supervisoredits/concurrentheavywork. Published101/1228,remaining1127; "
    "local075NOTdelivered; necessarysupportsNOTN1vocabulary. CompatibleAndroidf9b59a2+ "
    "required; physicalphone/generalrelease/whole-setacceptanceoutstanding. Projectincomplete."
)
LIMITS = (
    "Dependent visual confirmations and bounded recovery, not new blind initial reviews or "
    "fresh upstream retrieval. Original lexical/optional/source limits inherited unchanged. "
    "Claude initial4988multi-toolresponses/30overlaps/false serial claim and502visual "
    "three concurrent fixture reads/twooverlaps remain noncompliant. Its subsequent "
    "single-packet serial correction does not repair earlier process history. GPT original "
    "modelreportedimage-limit/50repeatedreads/withdrawnunsupportedobservations and partial "
    "report remain; raw125successfulcalls/101binaryPNGresults do not prove modelaccess. "
    "FreshGPT24image recovery certifies only24newreads plus27inherited, not51freshreads. "
    "All4reviewerprocesses serial/exited; original reports/rawevents/ranges/payloads preserved. "
    "51unique source captures/111originalfiles;60duplicates hashmapped, not freshimages. "
    "Source1080x2400 resized900x2000; not everypixel/gesture/everyphone evidence. Tables "
    "require complementaryviews and wrapのり; unrelatedadjacent clipping is not targetdefect. "
    "Fallbackface unidentified; paint/cmap/hash evidence notreadability. No reviewerdevice "
    "execution/freshdictionary/native-speaker/MLKit/humanhandwriting/successfulrecall/model"
    "download/newpersistedmeaninggrade. HOST499/native501 not rerun; historicalfailures "
    "and baselineexceptions retained. Current-main/CI/publicZIP/physicalphone/generalrelease/"
    "whole-set acceptance remains outstanding. CompatibleAndroidf9b59a2+ required. "
    "No runtime/app edits, native/HOST rerun, publication,heap/guard changes or076."
)
SURFACES = (
    "kanji/典.md", "words/香典.md", "words/典型.md:24 link", "words/古典.md:31 link",
    "words/百科事典.md:29 link", "words/辞典.md:23 link", "kanji/古.md:38 example",
    "kanji/辞.md:37 example", "kanji/百.md:22 link only", "kanji/科.md:41 example",
    "kanji/事.md:36 example", "kanji/香.md:42 example",
)


def verify_reviews():
    frozen = m.load(V / "batch-075-visual-freeze.json")
    assert not m.git("diff", m.TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for path, digest in frozen["resourceHashes"].items():
        assert m.sha(Path(path)) == digest
    reviews = {}
    ordered = []
    prefixes = (
        "batch-075-visual-claude", "batch-075-visual-claude-confirmation",
        "batch-075-visual-gpt", "batch-075-visual-gpt-recovery",
    )
    for prefix in prefixes:
        path = V / f"{prefix}-execution.json"
        item = m.load(path)
        m.exited(item["launcherPid"], item["completedAt"])
        assert item["exitCode"] == 0
        assert item["actualModels"] == [item["requestedModel"]] == [item["usage"]["currentModel"]]
        assert item["availableTools"] == ["view"]
        report = V / f"{prefix}.md"
        assert m.sha(report) == item["reportSha256"]
        assert m.sha(Path(item["rawExecutionLocation"])) == item["rawExecutionSha256"]
        calls = item["toolCalls"]
        if isinstance(calls, list):
            assert not item["missingRequiredText"] and not item["unexpectedReadPaths"]
            assert not item["unfinishedTools"]
            for row in calls:
                assert row["name"] == "view" and row["success"]
                if "imagePayload" in row:
                    payload = row["imagePayload"]
                    assert m.sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
                    assert m.sha(Path(row["arguments"]["path"])) == payload["sourceSha256"]
                    assert payload["sourceDimensions"] == [1080, 2400]
                    assert payload["returnedDimensions"] == [900, 2000]
                else:
                    assert row["exactRequestedTextContainedInResult"]
        reviews[prefix] = {
            "report": str(report.relative_to(R)), "reportSha256": m.sha(report),
            "execution": str(path.relative_to(R)), "executionSha256": m.sha(path),
            "actualModel": item["requestedModel"], "sessionId": item["sessionId"],
            "launcherPid": item["launcherPid"], "startedAt": item["startedAt"],
            "completedAt": item["completedAt"], "exitCode": item["exitCode"],
            "toolCalls": len(calls) if isinstance(calls, list) else calls,
            "processAndCoverageAccepted": item["processAndCoverageAccepted"],
            "usageQualification": "Resumed-session usage can be cumulative, not per-pass cost.",
        }
        ordered.append(item)
    for first, second in zip(ordered, ordered[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    claude, correction, gpt, recovery = ordered
    assert claude["imagePayloadsVerified"] == 51 and not claude["processAndCoverageAccepted"]
    assert claude["multiToolResponses"] == 1 and len(claude["observedToolOverlaps"]) == 2
    assert correction["processAndCoverageAccepted"] and correction["toolCalls"] == 1
    assert gpt["mechanicalTransportCoverageComplete"] and not gpt["processAndCoverageAccepted"]
    assert gpt["imagePayloadCalls"] == 101 and len(gpt["toolCalls"]) == 125
    assert not gpt["observedToolOverlaps"] and gpt["multiToolResponses"] == 0
    assert recovery["processAndCoverageAccepted"] and recovery["imagePayloadCalls"] == 24
    assert len(recovery["toolCalls"]) == 26 and not recovery["observedToolOverlaps"]
    assert recovery["multiToolResponses"] == 0
    assert gpt["sessionId"] == m.SESSIONS["gpt"][1] != recovery["sessionId"]
    image_hashes = {}
    for item in (claude, gpt, recovery):
        for row in item["toolCalls"]:
            if "imagePayload" in row:
                source = row["arguments"]["path"]
                digest = row["imagePayload"]["sha256"]
                assert image_hashes.setdefault(source, digest) == digest
    assert set(image_hashes) == set(frozen["images"])
    return frozen, reviews


def record():
    frozen, reviews = verify_reviews()
    checks = {}
    for name in ("validate", "manifest", "budget"):
        source = L / f"{name}.txt"
        target = V / f"batch-075-visual-{name}-execution-502.txt"
        shutil.copyfile(source, target)
        checks[name] = {"path": str(target.relative_to(R)), "sha256": m.sha(target), "exitCode": 0}
    for source_name, label in (("copilot-help.txt", "help"), ("copilot-model-catalog.txt", "models")):
        target = V / f"batch-075-visual-{label}-execution-502.txt"
        target.write_text((L / source_name).read_text(encoding="utf-8-sig").rstrip() + "\n", encoding="utf-8")
    budget = ast.literal_eval((L / "budget.txt").read_text(encoding="utf-8").strip())
    assert budget == {
        "files": 8359, "entries": 8374, "retainedBytes": 44117705,
        "inflatedBytes": 44386043, "localZipBytes": 30153315, "listeningTaskMediaBytes": 5893602,
    }
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = m.load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert sum(len(section) for section in manifest.values() if isinstance(section, dict)) == 8352
    reconciliation = {
        "schemaVersion": 1, "execution": 502, "batch": "075",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": m.HEAD, "reviewedTeachingSnapshot": m.TEACHING,
        "nativeEnvelopeSnapshot": "fba1a8868b82cd93d7bfaeae1080f5642bd92730",
        "dependentNotBlind": True, "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "scope": "Two complete new articles and ten exact changed reused passages.13complete contextfiles/743linefixture/terminalinstrumentation/route read by original sessions. Unchanged型 included for12mappedpairs24directions. Original lexical/source conclusions inherited; fresh visual pixels distinguished from supplied runtime assertions.",
        "allFourReviewerProcessesSerialAndExited": True,
        "allVisualExecutionsInternallySerial": False,
        "claudeSerialCorrectionAndGptFreshRecoveryAccepted": True,
        "findings": [],
        "verdicts": {
            path: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
                   "boundedVisualComprehensibility": "CLEAN"} for path in SURFACES
        },
        "observations": [
            "Neither family established an actionable teaching/rendering defect. No teaching/app changes. Claude51pixels plus onepacket correction; GPT27certifiedpixels inherited plus24freshcontextpixels complete matched51sourcecapture scope.",
            "All117scopedHan across fourproductionfontrows and focused奠/亅/厂/艹/八/典/具/曲/共 plus sixwholewords readable. No replacementbox/blank/collapsedlookalike established. Fontfaceidentity unknown;468singlePaint+24wordprobes not readability evidence.",
            "Complementary captures jointly show allfourreadinglabels, linkedselectedwholewords and source-onlyqualifications; partialhorizontalclipping andのりwrap disclosed. Fullrawテン/デン,ふみ/のり sourceorder retained, selectedbothon/emptykun; nonselection is not incorrect/names-only.",
            "Actual onchoicesテン/メン/イン/リン andメン/デン/カン/ハン each have intended answer, feedbackCorrect and2of2Done. Actualmeaningchoicesume;Japaneseapricot/reference texts;rules;ceremony/deer/pinetree distinct. Not authored具曲共 or whole-livepool certification.",
            "香典 money-or-goods qualification, both objectをexamples with fullkana/translations, コウ+デン and rare香奠spelling-not-pronunciation distinction readable. Fourreusedwordlinks/sixolderkanjinavigationtargets readable; unchangedbroadercontext not freshlycertified.",
            "FullsignednativeGitarchive through productionContentSyncONCE1087kanji5044words107N1/problems0/version2759d7b13c89eb8f/epoch1; supplied API35bothnamedterminal0/no skips234.957s. Synthetic sourceHTTP/HEAD does not mean synthetic/reduced content.",
            "Twelve reciprocalpairs24directions/SystemBack/offline supported by supplied743linefixture/route and representativepixels, not reviewerperformedgestures. Meaning exitsbeforeNext; no newlypersistedmeaninggrade.",
            "Drawing first eightgeneratedreference touchstrokes/ungradedtrace/model-unavailablegeometry, then separate recallmiss/persistedDrawAgain. No humanhandwriting/successfulrecall/MLKit or successfulmodeldownload claim.",
        ],
        "optional": [
            {"status": "optional", "reportedBy": ["Claude"],
             "claim": "Initial辞典/事典tendencywording, pluraldictionariesforのり, optional香典返し.",
             "decision": "Retain textual498 evidence-based nonblocking dispositions; no required teaching change."},
            {"status": "optional", "reportedBy": ["Claude"],
             "claim": "Add1283090 to reused香source list; reduceのりnarrowcolumnwrap.",
             "decision": "New香典/典 cite1283090 and complementaryviews expose reading; no demonstrated teaching or targetvisibility defect."},
        ],
        "hypothesisDispositions": [
            {"status": "withdrawn", "reportedBy": ["Claude"],
             "claim": "辞source list lacks辞典entry.",
             "evidence": "Actual1595270 is present; initial mistaken1319100identity corrected by reviewer."},
            {"status": "resolved", "reportedBy": ["Claude"],
             "claim": "Visual report countedtwofixturecalls and ambiguously called importsynthetic/drawingrecallonly/nativeunpassed.",
             "evidence": "ActualTHREEconcurrentfixturecalls/TWOoverlaps; onepacket follow-up corrects count and exactproductionimport/trace-then-recall/suppliednativepass distinction. Original report unchanged; process noncompliance remains."},
            {"status": "resolved", "reportedBy": ["GPT"],
             "claim": "24missingimages and withdrawnunsupportedvisualobservations.",
             "evidence": "Originalpartialreport retainsUNVERIFIED; freshisolatedGPT24imageonceeach recovery actuallyseespixels and resolves bounded典comprehensibility. No retrospective claim original51certified."},
        ],
        "processHistory": {
            "initial498Claude": "8multi-toolresponses/30overlappingstarts/false serial claim preserved.",
            "visual502Claude": "1multi-toolresponse/3fixturecalls[121,240],[241,360],[361,480]/2overlaps; originalprocessAndCoverageAcceptedFALSE; actualPNGcallsserial. Follow-up singlepacket corrects report, not priorcompliance.",
            "visual502GPT": "125serialcalls/101binaryPNGreturns/50repeatedreads; originalreport certifies27/51only, withdrawsunsupportedobservations. Rawsuccessfulbinaryreturns do not prove visualaccess.",
            "fresh502GPTRecovery": "Freshsession26serialcalls=task+ownpartialreport+24missingPNGonceeach; no retries/overlaps; all24actualpixels certified.",
            "archiverFailure": "Originalsource-namedtarget-existsassertion on repeatedGPTimage preserved. Recovery archiver verifies repeatedpayload bytes without overwriting originalreport or earliercopies.",
            "futureBound": "Do not repeat whole51imagepacket in growing originalcontext; stop on first missing-image result and use a narrow freshcontext recovery.",
        },
        "modelContributionComparison": {
            "matchedScope": "Samefrozen51uniquesourcecaptures/teaching/nativeevidence; GPT split27inherited+24fresh, not equal freshrereaddepth.",
            "sharedEstablishedDefects": [], "uniqueVerifiedClaudeDefects": [], "uniqueVerifiedGPTDefects": [],
            "qualification": "Findings/optional/limits compared together. No findingquota/generalmodelranking. Transport/processcorrections are evidence limitations, not invented Japanese teaching defects.",
        },
        "payloadAccounting": {
            "archivedSourceCaptures": 111, "uniqueSourceCaptures": 51, "byteDuplicateSourceFiles": 60,
            "claudeCertifiedSourceImages": 51, "gptOriginalCertifiedImages": 27, "gptFreshRecoveryImages": 24,
            "gptCombinedCertifiedSourceImages": 51, "rawReturnedImageCalls": 176,
            "rawCallsBreakdown": {"claudeVisual": 51, "gptOriginalIncludingRepeats": 101, "gptFreshRecovery": 24},
            "sourceDimensions": [1080, 2400], "returnedDimensions": [900, 2000],
            "sameReturnedBytesPerSourceAcrossFamiliesAndRepeats": True,
            "rawReturnedCallsNotFreshCertifiedImageCount": True,
        },
        "reviews": reviews, "checks": checks,
        "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False,
        "inheritedEvidence": {
            "textual": "batch-075-reconciliation.json/execution498 unchanged;372Python tests retained.",
            "android": "execution499 RealContentTest3+RareHanTest1 no skips, not rerun.",
            "native": "execution501 attempt1 two namedterminal0/no skips;111sourcecaptures, not rerun.",
        },
        "limits": LIMITS, "nextAction": NEXT,
    }
    m.save(V / "batch-075-visual-reconciliation.json", reconciliation)
    result = {
        "schemaVersion": 1, "execution": 502, "checkpoint": 502, "batch": "075",
        "status": reconciliation["status"], "startingHead": m.HEAD,
        "reviewedTeachingSnapshot": m.TEACHING,
        "authorization": m.load(L / "starting-state.json")["authorization"],
        "scope": m.load(L / "starting-state.json")["scope"],
        "reviews": reviews, "reconciliation": r"docs\n1-reviews\batch-075-visual-reconciliation.json",
        "reconciliationSha256": m.sha(V / "batch-075-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allVisualExecutionsInternallySerial": False,
        "claudeSerialCorrectionAndGptFreshRecoveryAccepted": True,
        "allOriginalReportsAndTeachingUnmodified": True, "runtimeEditsMade": False,
        "nativeOrAndroidRerun": False, "publicationAttempted": False, "runtimePublished": False,
        "publishedAdditions": 101, "remainingAdditions": 1127, "phoneEvidence": False,
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None, "limits": LIMITS,
        "checks": checks, "recordedAt": m.now(),
        "checksSummary": {
            "validatorErrors": 0, "manifestFresh": True, "runtimeHashesVerified": 8352,
            "contentVersion": "2759d7b13c89eb8f", "budget": budget, "originalLimitsUnchanged": True,
        },
        "coordinatorDirectImageChecks": [
            *[f"n1-075-font-panel-{i}.png" for i in range(1, 7)],
            "n1-075-kanji-20.png", "n1-075-香典-13.png",
            "n1-075-curated-てん-question.png", "n1-075-curated-でん-question.png",
            "n1-075-meaning-question.png", "n1-075-drawing-feedback.png",
        ],
        "controllerDiagnostics": {
            "unsupportedListModelsOption": "Exit1; actualcopilothelpconfig catalog subsequently captured. Not permissiondenial.",
            "incorrectPreparationConsoleFixtureCount": "Initialconsole757 corrected to actual743; frozen task/ranges were743 throughout.",
            "originalClaudeArchiverExit1": "Concurrencyacceptanceassertion after complete originalreport/events/payload archival; not reviewerexitfailure.",
            "originalGPTArchiverExit1": "Existingpayloadcopy on repeatedimage; recovery preserves all125calls/101payloads and originalreport without overwrite.",
            "transientPidRecheck": "Later barePID check observed29528 transiently; immediate explicit inspection found it absent. Receipt rechecks compare process creation time to reviewer completion to distinguish PID reuse; no shared process changed.",
        },
        "evidenceWhitespace": {
            "initialStagedDiffCheckExitCode": 2,
            "exactDiagnostics": [
                "batch-075-visual-claude-confirmation-packet.txt:70 trailing space after numbered empty source line150",
                "batch-075-visual-claude-confirmation-packet.txt:75 trailing space after numbered empty source line155",
                "batch-075-visual-receipts/copilot-model-catalog.txt:525 raw terminal blank line",
            ],
            "disposition": "Preserve frozen reviewer packet and exact raw CLI catalog bytes; these are evidence-only, not runtime/teaching. All remaining staged files checked separately before normal signing.",
        },
    }
    m.save(R / "docs" / "n1-sources" / "execution-502.json", result)
    batch = m.load(R / "docs" / "n1-sources" / "batch-075-progress.json")
    batch.update(
        status=reconciliation["status"], nextAction=NEXT, limits=LIMITS,
        nativeAcceptanceLimits="Two terminal-zero native cases, zero skips;111source screenshots preserved. Bounded two-family visual conclusions closed at502 with original Claude concurrency and GPT partial-image/recovery limitations explicitly preserved. Phone/general-release/current-main/CI/publicarchive acceptance and publication remain outstanding; no source row counted as published.",
    )
    batch["visualReviewCheckpoint"] = {
        "execution": 502, "evidenceHead": m.HEAD, "reviewedSnapshot": m.TEACHING,
        "reconciliation": str((V / "batch-075-visual-reconciliation.json").relative_to(R)),
        "reconciliationSha256": result["reconciliationSha256"],
        "boundedIndependentVisualConfirmation": True, "runtimePublished": False,
        "allVisualExecutionsInternallySerial": False, "historicalDeviationsPreserved": True,
    }
    m.save(R / "docs" / "n1-sources" / "batch-075-progress.json", batch)
    receipts = V / "batch-075-visual-receipts"
    receipts.mkdir(exist_ok=True)
    for path in (L / "execution-502.py", Path(__file__), L / "gpt-archive-diagnostic.json",
                 L / "copilot-help.txt", L / "copilot-model-catalog.txt"):
        shutil.copyfile(path, receipts / path.name)
    shutil.copyfile(m.PRIOR, receipts / "inherited-execution-494-archiver.py")
    print("Preserved all four reports/processes,176returned imagecalls and qualified two-family visual closure.")


def checkpoint():
    progress = m.load(C / "progress.json")
    before = m.load(L / "starting-progress.json")
    assert progress["checkpoint"] == 501
    for key, value in before.items():
        if key not in {"stage", "nextAction", "execution502StartingState"}:
            assert progress[key] == value, key
    head = m.git("rev-parse", "HEAD")
    assert head != m.HEAD and m.git("log", "-1", "--format=%G?") == "G"
    assert not m.git("status", "--porcelain")
    assert not m.git("diff", m.TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    path = R / "docs" / "n1-sources" / "execution-502.json"
    receipt = {
        "execution": 502, "checkpoint": 502, "batch": "075", "status": "continue",
        "savedCommit": head, "signature": "G", "record": str(path.relative_to(R)),
        "recordSha256": m.sha(path), "runtimePublished": False,
        "boundedIndependentVisualAcceptance": True, "allReviewerProcessesSerialAndExited": True,
        "allVisualExecutionsInternallySerial": False, "historicalDeviationsPreserved": True,
        "gptFreshRecoveryMissingImages": 24, "nextAction": NEXT,
        "publishedAdditions": 101, "remainingAdditions": 1127,
        "allOriginalHistoricalRootKeysPreserved": True,
    }
    progress.update(checkpoint=502, status="continue", stage="batch-075-visual-closed-awaiting-integration",
                    nextAction=NEXT, blocker=None)
    progress["execution502StartingState"]["status"] = "signed-dependent-visual-checkpoint-complete"
    progress["execution502CoordinatorCheckpoint"] = receipt
    progress["batch075VisualCheckpoint"] = receipt.copy()
    m.save(C / "progress.json", progress)
    m.save(L / "checkpoint-full.json", progress)
    m.save(L / "execution-502-checkpoint.json", receipt)
    body = f"""N1 kanji batch 075: visual confirmation checkpoint 502 saved locally at signed `{head}`; **not published**.

Claude Opus 5.5 and GPT-6.1 Sol established no actionable defect in complete new 典 / necessary support 香典 and the ten exact reused navigation passages. All twelve scoped surfaces are CLEAN for correctness, scoped coverage and bounded emulator comprehensibility. Same frozen teaching `f5b70805`, native envelope `fba1a886`, version `2759d7b13c89eb8f`; no teaching/app changes or native/HOST rerun.

Four reviewer processes exited sequentially. Process limits are preserved, not rebranded: Claude's visual pass batched three fixture ranges once (two overlapping starts); a subsequent one-resource serial correction fixes its inaccurate report, not that violation. Its initial eight multi-tool responses / thirty overlaps remain historical. Original GPT made fifty repeated image reads and certified only 27/51 screenshots despite successful binary tool returns; its partial report and withdrawn unsupported observations remain. A fresh isolated GPT context inspected the missing 24 PNGs exactly once with 26 serial calls, completing **27 inherited + 24 fresh**, not 51 fresh inspections.

All 111 original PNGs are preserved (51 unique, 60 exact-byte duplicates), along with complete reports, actual models/sessions/process/range/payload evidence and failed-archiver diagnostics. Both families cover all 117 scoped Han across four font rows, focused 奠/亅/厂/艹 plus look-alikes/six words, complementary reading-table views, actual meaning/on-reading choices and feedback/2-of-2 Done, twelve reciprocal pairs/24 directions, tracing/recall, articles and supplied offline/System Back. Unknown fallback face and phone readability are not certified; injected reference tracing is not human handwriting/MLKit evidence.

Fresh validator, unchanged manifest (8,352 runtime hashes), and original budgets pass: 8,374 archive entries; 30,153,315 compressed / 44,386,043 inflated / 44,117,705 retained bytes. Next checkpoint: fresh-main nonrewriting integration/combined validation, normal signing and authorized owner fast-forward publication, terminal green CI and every immutable public ZIP runtime hash/budget before delivery or batch076.

Published additions remain **101/1,228**, remaining **1,127**; necessary supports are not an N1 vocabulary deck. Compatible Android `f9b59a2+` required. Physical-phone, general-release and whole-set acceptance remain outstanding.
"""
    (L / "issue-502-body.txt").write_text(body, encoding="utf-8")
    print("Saved signed checkpoint502 with FULL live history; statuscontinue, runtimeNOTpublished.")


def finalize():
    progress = m.load(C / "progress.json")
    before = m.load(L / "starting-progress.json")
    assert progress["checkpoint"] == 502 and progress["status"] == "continue"
    for key, value in before.items():
        if key not in {"checkpoint", "stage", "nextAction", "execution502StartingState", "blocker"}:
            assert progress[key] == value, key
    head = m.git("rev-parse", "HEAD")
    assert head == progress["execution502CoordinatorCheckpoint"]["savedCommit"]
    assert m.git("log", "-1", "--format=%G?") == "G" and not m.git("status", "--porcelain")
    assert not m.git("diff", m.TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    assert not subprocess.check_output(
        ["git", "-C", str(C.parent / "kanji-cards-android"), "status", "--porcelain"], encoding="utf-8").strip()
    verify_reviews()
    record_path = R / "docs" / "n1-sources" / "execution-502.json"
    assert m.sha(record_path) == progress["execution502CoordinatorCheckpoint"]["recordSha256"]
    record = m.load(record_path)
    assert m.sha(R / record["reconciliation"]) == record["reconciliationSha256"]
    api = m.load(L / "issue-502-api.json")
    receipt = m.load(L / "issue-502-verified.json")
    assert receipt["author"] == api["user"]["login"] == "stop-cran" and receipt["bodyVerified"]
    assert api["body"].replace("\r\n", "\n").rstrip() == (
        L / "issue-502-body.txt").read_text(encoding="utf-8").rstrip()
    progress["batch075VisualIssueReceipt"] = receipt
    for key in ("execution502CoordinatorCheckpoint", "batch075VisualCheckpoint"):
        progress[key]["issueUpdate"] = receipt["url"]
        progress[key]["ownerAuthorAndBodyVerified"] = True
    m.save(C / "progress.json", progress)
    m.save(L / "checkpoint-full.json", progress)
    m.save(L / "execution-502-checkpoint.json", progress["execution502CoordinatorCheckpoint"])
    m.save(L / "execution-502-final-verification.json", {
        "execution": 502, "checkpoint": 502, "status": "continue", "batch": "075",
        "savedCommit": head, "signature": "G", "contentAndAndroidClean": True,
        "historicalRootValuesPreserved": True, "reviewerProcessesExitedSerially": True,
        "allVisualExecutionsInternallySerial": False, "allHistoricalDeviationsPreserved": True,
        "qualifiedTwoFamilyBoundedVisualScopeClosed": True, "runtimePublished": False,
        "issueReceipt": receipt, "verifiedAt": m.now(),
    })
    print("Checkpoint502 verified: signed local evidence, preserved full history, owner issue receipt; statuscontinue.")


if __name__ == "__main__":
    {"record": record, "checkpoint": checkpoint, "finalize": finalize}[sys.argv[1]]()
