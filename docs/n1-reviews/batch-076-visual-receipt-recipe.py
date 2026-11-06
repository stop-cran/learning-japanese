from datetime import datetime
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

spec = importlib.util.spec_from_file_location("execution510", Path(__file__).with_name("execution-510.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
L, C, R, V, F = m.L, m.C, m.R, m.V, m.F

NEXT = (
    "SAME076 bounded visual confirmation closed at510; no publication/077 this checkpoint. "
    "Read docs\\n1-sources\\execution-510.json and batch-076-visual-reconciliation.json. "
    "Complete兼/兼任 plus exact兼ねる26/30 linkedparagraphs and任38bullet allthreefacetsCLEAN "
    "within supplied scope; no new actionable teaching/rendering defect. Actualmodels "
    "claude-opus-5.5/gpt-6.1-sol originalsessions reused. AllTHREEreviewerprocesses exited "
    "serially. OriginalClaude34uniquePNG/4completeTEXTreturns includes ONEresponse/TWO "
    "concurrentPNG/ONEoverlap; originalflagFALSE preserved. Bounded originalsession correction "
    "re-viewed ONLY thoseTWOimages genuinelyserial/onepacket, inheritedother32; fallbackface "
    "guess withdrawn. GPT34uniquePNG/4completeTEXTreturns actuallyserial/no repeats/overlaps. "
    "57originalcaptures=34unique+23hashduplicates, not57freshviews. Full570linefixture and "
    "fourcompletearticles in one59715byte sourcepacket toboth; originallexicalconclusions "
    "inherited, not newblindinitial/dictionaryretrieval. Fullrawケン,か.ねる/-か.ねる "
    "sourceorder; curatedケン/か.ねる, actualけん/かねる eachGood/Done2correct/no duplicates. "
    "41Han/fourproductionfamilies/twowords/threepanels readable; fallbackface unknown. "
    "All3mappedpairs6directions/SystemBack/offline suppliednative; extra兼ねる-to兼任 link "
    "visible, not separately traversed. Native509bothnamedterminal0noskips/507HOST3+1 "
    "retained, no rerun. Tenreference-touchstrokes/ungradedtrace/recallAgain NOT "
    "humanhandwriting/MLKit/successfulrecall; modelunavailableoffline. "
    "NEXT freshfetchorigin/main/nonrewritingmergeifneeded and validate actualcombined "
    "source/membership/baseline/readings/quiz/links/fonts/strokes/Python/vocab/validator/"
    "freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained; "
    "normalsigning/authorizedownerfastforward/publicSHA/terminalgreenCI/EVERYimmutable"
    "publicZIPruntimehash+budgets/ownerissue60 BEFOREdelivery or077. Preserve FULLlivehistory/"
    "originalreports/allhistoricaldenials and baseline虎猿丘山exceptions. No signingretry/"
    "permissionworkaround/heaporguardchanges/authoragents/secondrunner/supervisoredits/"
    "concurrentheavywork. Published102/1228,remaining1126; local076NOTdelivered; necessary"
    "supportsNOTN1vocabulary. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/"
    "whole-setacceptanceoutstanding. Projectincomplete."
)
LIMITS = (
    "Dependent original-session visual confirmations, not new blind initial reviews or fresh "
    "upstream retrieval. All3reviewerprocesses serial/exited. Original Claude ONEresponse "
    "TWOconcurrentPNG/ONEoverlap remains noncompliant and original flag FALSE; subsequent "
    "2image serial correction does not change history. GPT34uniqueimages onceeach genuinely "
    "serial. All57originalcaptures=34unique+23hashduplicates, not57freshimages. Access/"
    "ranges/hashes not comprehension. Source1080x2400 resized900x2000; not everypixel/"
    "gesture/everyphone evidence. Tables require complementaryviews. Fallbackface unknown; "
    "Claude's guess withdrawn. Extra word-to-word link visible but not separately traversed. "
    "Original lexical/optional/source limits retained. No reviewerdevice execution/"
    "freshdictionary/native-speaker/MLKit/humanhandwriting/successfulrecall/modeldownload/"
    "newpersistedmeaninggrade. HOST507/native509 retained, no rerun. Current-main/CI/"
    "publicZIP/physicalphone/generalrelease/whole-setacceptance remains outstanding. "
    "CompatibleAndroidf9b59a2+ required. No runtime/app edits, native/HOST rerun, publication,"
    "heap/guard changes or077."
)
SURFACES = ("kanji\\兼.md", "words\\兼任.md", "words\\兼ねる.md:26",
            "words\\兼ねる.md:30", "kanji\\任.md:38")
PREFIXES = ("batch-076-visual-claude", "batch-076-visual-claude-confirmation", "batch-076-visual-gpt")


def verify_reviews():
    frozen = m.freeze()
    reviews = {}
    ordered = []
    for prefix in PREFIXES:
        path = V / f"{prefix}-execution.json"
        item = m.load(path)
        assert item["exitCode"] == 0
        assert item["actualModels"] == [item["requestedModel"]] == [item["usage"]["currentModel"]]
        assert not item["missingRequiredText"] and not item["unexpectedReadPaths"] and not item["unfinishedTools"]
        report = V / f"{prefix}.md"
        assert m.sha(report) == item["reportSha256"]
        assert m.sha(Path(item["rawExecutionLocation"])) == item["rawExecutionSha256"]
        for row in item["toolCalls"]:
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
            "toolCalls": len(item["toolCalls"]), "imagesReturned": item["imagePayloadsVerified"],
            "processAndCoverageAccepted": item["processAndCoverageAccepted"],
            "usageQualification": "Resumed-session usage can be cumulative, not per-pass cost.",
        }
        ordered.append(item)
    for first, second in zip(ordered, ordered[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
    claude, correction, gpt = ordered
    assert claude["imagePayloadsVerified"] == gpt["imagePayloadsVerified"] == 34
    assert not claude["processAndCoverageAccepted"]
    assert claude["multiToolResponses"] == 1 and len(claude["observedToolOverlaps"]) == 1
    assert correction["processAndCoverageAccepted"] and len(correction["toolCalls"]) == 3
    assert correction["imagePayloadsVerified"] == 2
    assert gpt["processAndCoverageAccepted"] and len(gpt["toolCalls"]) == 38
    assert gpt["sessionId"] == m.SESSIONS["gpt"][1]
    assert claude["sessionId"] == correction["sessionId"] == m.SESSIONS["claude"][1]
    for family, item in (("claude", claude), ("gpt", gpt)):
        images = [row["arguments"]["path"] for row in item["toolCalls"] if "imagePayload" in row]
        assert images == frozen["images"]
        assert len(images) == len(set(images)) == 34
    return frozen, reviews


def record():
    frozen, reviews = verify_reviews()
    checks = {}
    for name in ("validate", "manifest", "budget"):
        source = L / f"{name}.txt"
        target = V / f"batch-076-visual-{name}-execution-510.txt"
        assert not target.exists()
        shutil.copyfile(source, target)
        checks[name] = {"path": str(target.relative_to(R)), "sha256": m.sha(target), "exitCode": 0}
    for name in ("help", "model-catalog"):
        target = V / f"batch-076-visual-copilot-{name}-execution-510.txt"
        shutil.copyfile(L / f"copilot-{name}.txt", target)
    reconciliation = {
        "schemaVersion": 1, "execution": 510, "batch": "076",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": m.HEAD, "reviewedTeachingSnapshot": m.TEACHING,
        "nativeEnvelopeSnapshot": "b89b333682fa5bfb4123ea8f4a74c2cc59935a7c",
        "dependentNotBlind": True, "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "scope": "Two complete new articles; exact reused linked paragraphs兼ねる26/30 and任38bullet. Four complete articles/570linefixture/terminal/route supplied in one sourcepacket; original lexical conclusions inherited, fresh visual pixels distinguished from supplied runtime assertions.",
        "allThreeReviewerProcessesSerialAndExited": True,
        "allVisualExecutionsInternallySerial": False,
        "claudeBoundedSerialCorrectionAndGptAccepted": True,
        "findings": [],
        "verdicts": {
            path: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
                   "boundedVisualComprehensibility": "CLEAN"} for path in SURFACES
        },
        "observations": [
            "Neither family established a new actionable scoped teaching/rendering defect. Claude original34pixels plus2serialre-views; GPT34pixels onceeach actualserial.",
            "All41scopedHan in fourproductionfamilies and focused兼/典/具/曲/八/人/亻 plus兼任/兼ねる readable; no blank/replacementbox/collapsedlookalike established. Actualfallbackface unknown;164singlePaint+8wordrasters not readability evidence.",
            "Complementary captures jointly show allthree raw readings, linked wholewordexamples and suffixattachment/polarity/sharedstem/かねない distinction. Horizontalclipping of othercolumn is disclosed, not missing teaching.",
            "Actualonケン/テン/カン/デン andkunかねる/さる/かつ/かつら intendedkey/feedbackCorrect/Done2of2; actualmeaningcombine;concurrentroles/reference texts;rules;ceremony/suspicious;uncanny/monkey distinct. Not universal/random/livepool certification.",
            "兼任 additionalpost or twojoinedposts takeを wording, both complete examples/kana/translations and就任にcontrast visible. Existing076-C1 remains resolved. Modernshape not history;八12top;tenstrokes.",
            "All3mappedpairs6directions/SystemBack/offline suppliedfixture/terminal/route plus representativeimages. Extra兼ねる-to兼任 wordlink visible but not separately traversed; no native traversal claim for that extra link.",
            "FullsignednativeGitarchive productionContentSyncONCE1088kanji5045words108N1/problems0/version8bd0a375668bee11/epoch1; supplied API35bothnamedterminal0/zero skips. Meaning exitsbeforeNext; not newlypersistedmeaninggrade.",
            "Tenreference-injectedtouchstrokes/ungradedtrace/modelunavailablegeometry, then recallmiss/persistedDrawAgain; not humanhandwriting/successfulrecall/MLKit or successfulmodeldownload.",
        ],
        "optional": [
            {"status": "optional", "reportedBy": ["Claude"],
             "claim": "Sharper lookalike wording; modifier/head qualification; 勤める1240825 in source note.",
             "decision": "No edit. Original textual dispositions retained; visible wording establishes no new defect. GPT also accepts unchanged text."},
            {"status": "optional", "reportedBy": ["Claude"],
             "claim": "App drawing text 'Graded by stroke shapes only' beside 'not graded' is awkward.",
             "decision": "Pre-existing app wording, not a content rendering defect; no app changes within this bounded content checkpoint."},
        ],
        "hypothesisDispositions": [
            {"status": "withdrawn", "reportedBy": ["Claude"],
             "claim": "亻 likely uses a fallback face.",
             "evidence": "Actual resolved face cannot be identified from screenshots; original reviewer explicitly withdraws inference in serial correction."},
        ],
        "processReconciliation": {
            "originalClaudeFlag": False,
            "originalClaudeMultiToolResponses": 1,
            "originalClaudeOverlappingStarts": 1,
            "originalClaudeConcurrentImages": ["n1-076-curated-both-done.png", "n1-076-curated-Kun-feedback.png"],
            "originalClaudePreserved": True,
            "correction": "Same session; complete ownreport/processpacket and two affectedPNGs read serially. Other32images and source conclusions inherited. Original noncompliance remains; no retroactive flag change.",
            "gpt": "Original session;4complete textresources then34uniquePNG onceeach,38serialcalls,no overlaps/multicalls.",
        },
        "modelContributionComparison": {
            "sharedVerifiedNewDefects": [], "uniqueVerifiedNewDefects": {"Claude": [], "GPT": []},
            "overlappingObservations": "Both inspect same34unique captures/complete sourcepacket and retain clean bounded teaching/rendering verdicts.",
            "limits": "Dependent visual confirmation, not model benchmark. Original optional commentary retained; no manufactured discovery.",
        },
        "reviews": reviews, "sourceCaptures": 57, "uniqueAssignedCaptures": 34,
        "hashMappedDuplicateCaptures": 23, "runtimeEditsMade": False,
        "boundedIndependentVisualConfirmation": True, "runtimePublished": False,
        "physicalPhoneAcceptance": False, "limits": LIMITS, "nextAction": NEXT,
    }
    destination = V / "batch-076-visual-reconciliation.json"
    m.save(destination, reconciliation)
    record = {
        "schemaVersion": 1, "execution": 510, "checkpoint": 510, "batch": "076",
        "status": reconciliation["status"], "startingHead": m.HEAD,
        "reviewedTeachingSnapshot": m.TEACHING,
        "authorization": m.load(L / "starting-state.json")["authorization"],
        "scope": m.load(L / "starting-state.json")["scope"],
        "reviews": reviews, "reconciliation": str(destination.relative_to(R)),
        "reconciliationSha256": m.sha(destination),
        "boundedIndependentVisualConfirmation": True,
        "allReviewerProcessesSerialAndExited": True,
        "allVisualExecutionsInternallySerial": False,
        "claudeBoundedSerialCorrectionAndGptAccepted": True,
        "allOriginalReportsAndTeachingUnmodified": True,
        "checks": checks,
        "checksSummary": {
            "validatorErrors": 0, "manifestFresh": True, "runtimeHashesVerified": 8355,
            "contentVersion": "8bd0a375668bee11",
            "budget": {"files": 8362, "entries": 8377, "retainedBytes": 44126521,
                       "inflatedBytes": 44394859, "localZipBytes": 30157926,
                       "listeningTaskMediaBytes": 5893602},
            "originalLimitsUnchanged": True,
        },
        "accepted507HostCasesRetainedWithoutRerun": 4,
        "accepted509NativeCasesRetainedWithoutRerun": 2,
        "runtimeEditsMade": False, "nativeOrAndroidRerun": False,
        "publicationAttempted": False, "runtimePublished": False,
        "publishedAdditions": 102, "remainingAdditions": 1126,
        "phoneEvidence": False, "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None, "limits": LIMITS, "recordedAt": m.now(),
        "coordinatorDirectImageChecks": [
            "n1-076-font-panel-1.png", "n1-076-font-panel-2.png", "n1-076-font-panel-3.png",
            "n1-076-curated-both-done.png", "n1-076-meaning-question.png",
            "n1-076-kanji-11.png", "n1-076-兼任-03.png",
        ],
    }
    m.save(R / "docs" / "n1-sources" / "execution-510.json", record)
    progress_path = R / "docs" / "n1-sources" / "batch-076-progress.json"
    progress = m.load(progress_path)
    progress.update(status=reconciliation["status"], nextAction=NEXT, nextGate=NEXT,
                    remainingGates="Fresh combined-current-main integration/revalidation, normal signing and owner fast-forward publication, green CI, exact immutable ZIP hashes and original budgets. Physicalphone/generalrelease/whole-set outstanding.",
                    visualCheckpoint={"execution": 510, "record": "execution-510.json",
                                      "reconciliation": str(destination.relative_to(R)),
                                      "reconciliationSha256": m.sha(destination),
                                      "boundedVisualConfirmation": True, "runtimePublished": False,
                                      "processDeviationPreserved": True})
    m.save(progress_path, progress)
    shutil.copyfile(Path(__file__), V / "batch-076-visual-receipt-recipe.py")
    shutil.copyfile(L / "execution-510.py", V / "batch-076-visual-execution-recipe.py")
    print("Reconciled bounded visual evidence; no teaching changes; original violation preserved.")


def checkpoint():
    commit = m.git("rev-parse", "HEAD")
    assert commit != m.HEAD and m.git("log", "-1", "--format=%G?") == "G"
    assert not m.git("status", "--porcelain")
    assert not m.git("diff", m.TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    progress = m.load(C / "progress.json")
    original = m.load(L / "starting-progress.json")
    assert progress["checkpoint"] == original["checkpoint"] == 509
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker", "activeExecution"}
    for key, value in original.items():
        if key not in mutable:
            assert progress[key] == value, key
    record_path = R / "docs" / "n1-sources" / "execution-510.json"
    receipt = {
        "execution": 510, "checkpoint": 510, "batch": "076",
        "savedCommit": commit, "signature": "G",
        "record": str(record_path.relative_to(R)), "recordSha256": m.sha(record_path),
        "status": "continue", "stage": "batch-076-visual-closed-awaiting-current-main-integration",
        "runtimePublished": False, "boundedIndependentVisualConfirmation": True,
        "originalClaudeProcessFlagPreservedFalse": True,
        "reviewerProcessesSerialAndExited": True, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootKeysPreserved": True,
        "publishedAdditions": 102, "remainingAdditions": 1126,
        "nextAction": NEXT, "recordedAt": m.now(),
    }
    progress.update(checkpoint=510, status="continue", stage=receipt["stage"],
                    nextAction=NEXT, blocker=None, activeExecution=receipt)
    progress["execution510StartingState"]["status"] = "signed-dependent-visual-checkpoint-complete"
    progress["execution510CoordinatorCheckpoint"] = receipt
    progress["batch076VisualCheckpoint"] = receipt
    m.save(C / "progress.json", progress)
    m.save(L / "checkpoint-510.json", receipt)
    assert progress["lastPublishedCommit"] == original["lastPublishedCommit"]
    assert progress["remainingAdditions"] == original["remainingAdditions"] == 1126
    print("Saved FULL historical progress checkpoint510:", commit, "continue; NOT published.")


if __name__ == "__main__":
    if sys.argv[1] == "record":
        record()
    elif sys.argv[1] == "checkpoint":
        checkpoint()
