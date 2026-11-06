import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

spec = importlib.util.spec_from_file_location("execution494", Path(__file__).with_name("execution-494.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
L, C, R, V, F = m.L, m.C, m.R, m.V, m.F
NEXT = (
    "SAME074 dependent visual confirmations494 complete: original Claudeaf76d4d5 THEN "
    "GPTc7f3d66f processes exited serially; actual claude-opus-5.5/gpt-6.1-sol; "
    "both full task/own original reports/five teaching context files/595line native fixture/"
    "terminalinstrumentation/route/32uniquePNG returned, exact payload/range/process archival. "
    "Read docs\\n1-sources\\execution-494.json and batch-074-visual-reconciliation.json. "
    "Allfive scoped surfaces/allthree facets CLEAN, no actionable defect. Both visual executions "
    "internally serial, no overlap/multitoolresponses. Historical initial Claude ONE concurrent "
    "兄/元 read remains disclosed, not erased. No teaching/app changes or new blind initial review. "
    "Inherit490textual/491HOST3+1/493native2terminal0noskips; do not rerun absentnewconcern. "
    "Complementary tables expose allthree labels/examples/variant qualifications; newword "
    "source link clipped in09 but fully visible in12. Fourfontrows all43Han+threewords readable; "
    "fallbackface/physicalphone not identified. NEXT freshfetchorigin/main/nonrewritingintegration "
    "ifneeded; validate actualcombined source/baseline/readings/links/font/stroke/Python/vocab/"
    "validator/freshmanifest/original18000entries42MiBcompressed80MiBinflated56MiBretained; "
    "normal signing/ownerfastforward/publicSHA/terminalgreenCI/EVERYimmutablepublicZIP"
    "runtimehash+budgets/ownerissue60 BEFOREdelivery or075. Preserve FULLlivehistory/"
    "originalsource recipe/baselineexceptions/fullreadingorder/allhistoricalfailures. "
    "No signingretry/permissionworkaround/secondrunner/supervisoredits/concurrentheavywork. "
    "Published100/1228,remaining1128; local074NOTdelivered;100publishednecessarysupports "
    "NOTN1vocabulary. CompatibleAndroidf9b59a2+ required; "
    "physicalphone/generalrelease/whole-setacceptanceoutstanding. Overallprojectincomplete."
)
LIMITS = (
    "Dependent original-session visual confirmations, not new blind initial reviews or fresh "
    "upstream retrieval. Initial lexical findings/optional/source limits inherited unchanged. "
    "Historical initial Claude ONE concurrent兄/元 read remains disclosed, not erased; BOTH "
    "494visual reviewers internally serial, zero overlap/multi-tool responses. Reviewer processes "
    "serial and exited; original reports/executions/payloads preserved. Returned bytes/ranges "
    "establish access, not comprehension.32unique source captures/57originalPNGs;25duplicates "
    "hash-mapped, not freshly viewed.64returned900x2000 payloads from1080x2400 sources are "
    "identical per source across models, not everypixel/gesture/physicalviewingsize proof. "
    "Complementary reading-table views clip opposite columns but jointly expose complete "
    "labels/examples; word source-link clipped in09 and visible in12. Actual fallback face "
    "not identified; no all-phone certificate. Native493attempt3/HOST491 not rerun. No "
    "reviewer device execution, new persisted meaning grade, MLKit/human handwriting/"
    "successful recall/model download/reversed or negative geometry evidence. Native "
    "attempt1 ASCII-only capture loss/attempt2 ownership refusal/attempt3 complete retrieval "
    "and all historical denials/OOMs retained. Current-main/CI/public ZIP/physical-phone/"
    "general-release/whole-set acceptance remains outstanding. CompatibleAndroidf9b59a2+ "
    "required. No runtime edits/publication/guard/heap changes."
)


def exited(pid):
    result = subprocess.run(
        ["pwsh", "-NoProfile", "-Command", f"Get-Process -Id {pid} -ErrorAction SilentlyContinue"],
        capture_output=True)
    assert not result.stdout.strip(), f"Reviewer PID{pid} still exists"


def verify_reviews():
    frozen = m.freeze()
    reviews = {}
    ordered = []
    for family, (model, session) in m.SESSIONS.items():
        path = V / f"batch-074-visual-{family}-execution.json"
        item = m.load(path)
        assert item["processAndCoverageAccepted"] and item["exitCode"] == 0
        assert item["actualModels"] == [model] == [item["usage"]["currentModel"]]
        assert item["sessionId"] == session and item["availableTools"] == ["view"]
        assert not item["missingRequiredText"] and not item["unexpectedReadPaths"]
        assert not item["unfinishedTools"] and not item["observedToolOverlaps"]
        assert item["multiToolResponses"] == 0 and item["imagePayloadsVerified"] == 32
        exited(item["launcherPid"])
        report = V / f"batch-074-visual-{family}.md"
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
        reviews[family] = {
            "report": str(report.relative_to(R)), "reportSha256": m.sha(report),
            "execution": str(path.relative_to(R)), "executionSha256": m.sha(path),
            "actualModel": model, "sessionId": session, "launcherPid": item["launcherPid"],
            "startedAt": item["startedAt"], "completedAt": item["completedAt"],
            "exitCode": 0, "toolCalls": len(item["toolCalls"]),
            "verifiedReturnedImages": 32, "processAndCoverageAccepted": True,
            "toolOverlapStarts": 0, "multiToolResponses": 0,
            "usageQualification": "Raw usage is retained session-cumulative; not claimed as per-pass usage.",
        }
        ordered.append(item)
    assert ordered[0]["completedAt"] < ordered[1]["startedAt"]
    for source in frozen["images"]:
        copies = [F.parent / f"visual-{name}-returned" / Path(source).name for name in reviews]
        assert len({m.sha(path) for path in copies}) == 1
    return frozen, reviews


def record():
    frozen, reviews = verify_reviews()
    checks = {}
    for name in ("validate", "manifest", "budget"):
        source = L / f"{name}.txt"
        target = V / f"batch-074-visual-{name}-execution-494.txt"
        shutil.copyfile(source, target)
        checks[name] = {"path": str(target.relative_to(R)), "sha256": m.sha(target), "exitCode": 0}
    for name in ("help", "models"):
        shutil.copyfile(L / f"copilot-{name}.txt", V / f"batch-074-visual-{name}-execution-494.txt")
    m.save(V / "batch-074-visual-freeze.json", frozen)
    reconciliation = {
        "schemaVersion": 1, "execution": 494, "batch": "074",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": m.HEAD, "reviewedTeachingSnapshot": m.TEACHING,
        "nativeEnvelopeSnapshot": "4078c7d42e6bc2173c555e73d0bd39fb5d69eb08",
        "dependentNotBlind": True, "models": [pair[0] for pair in m.SESSIONS.values()],
        "scope": "Whole new kanji/免.md and words/免れる.md; exact reused words/免許.md:25 link, words/免税.md:26 link, kanji/許.md:38 example. Full reused files as context only. Both original sessions received complete595line fixture, terminal log/route and32uniquePNG; original lexical conclusions inherited.",
        "allReviewerProcessesSerialAndExited": True,
        "bothVisualExecutionsInternallySerial": True,
        "allHistoricalInternalCallsSerial": False,
        "historicalProcessQualification": "Initial490Claude ONE concurrent兄/元 read remains disclosed; serial494 confirmations do not erase it.",
        "findings": [],
        "verdicts": {
            path: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
                   "boundedVisualComprehensibility": "CLEAN"}
            for path in ("kanji/免.md", "words/免れる.md", "words/免許.md:25 link",
                         "words/免税.md:26 link", "kanji/許.md:38 example")
        },
        "observations": [
            "Neither family established a new actionable teaching/rendering defect. Initial bounded lexical verdicts retained; no teaching/app changes.",
            "Four production rows show all43Han and免れる/免許/免税 readable, including isolated儿 and免/兄/元/先/許/税 distinctions.172singlePaint+12word probes are not all-phone readability/fallback-face evidence.",
            "Complementary table views show allthree reading labels and full linked examples/qualified alternate, with differing horizontal clipping and explicit scroll hint. Rawメン/まぬか.れる/まぬが.れる source order preserved. Both pronunciations valid; quiz selectsメン/まぬが.れる to avoid duplicate variants, not to label alternate rare/wrong.",
            "New免 meaning/dismissal qualification/invented-shape mnemonic/notes and new免れる adverse-eventを/examples/ichidan forms/both pronunciations/lexicalれる/transitivity qualification visible. Exact reused component links and許example readable; N3免許/N2免税 retained, no inferred word level.",
            "Actual meaning choices exempt;be spared / scarce;lacking / overcome / plan;undertake are distinct; not authored兄元先 or whole-pool certification. Actual Onイン/カン/メン/リン and Kunくすのき/まぬがれる/くわだてる/たちばな each have one valid answer. Both feedback and2of2Done visible; supplied Next assertions persist bothGood/no alternate key or log.",
            "Allfive reciprocalpairs/10directions andSystemBack/offline supported by supplied fixture/receipts and representative static destinations/returns, not reviewer-performed gestures.",
            "Inherited493native both named terminal0/no skips128.836s; complete productionContentSyncONCE1086kanji5043words106N1/problems0/versionc507eceeb764bc3f/epoch1. Disposable synthetic source, otherN1postponed/twohistoricalGoodmeaninglogs/no drawingstateseeded. Meaning exits before Next. Eightreference touch strokes/ungradedtrace/model-unavailablegeometry/recallmiss/persistedDrawAgain not human handwriting/MLKit.",
            "Newword source-link line below09 viewport is fully visible in12. This refines conservative493 viewport limitation without asserting every-character/all-viewport completeness.",
        ],
        "optional": [
            {"status": "optional", "reportedBy": ["Claude"],
             "claim": "Add1533130 to許source line; add勉/晩 comparisons; dismissal example; 謗りを免れない pattern.",
             "decision": "Retain490 precise nonblocking dispositions; no new evidence or necessary prerequisite, no scope expansion."}
        ],
        "hypothesisDispositions": [
            {"status": "withdrawn", "claim": "Claude visual report says Mincho row looks sans-like.",
             "evidence": "Direct coordinator font-pairs PNG shows Mincho serif forms; isolated儿 inTextbook appears heavier. Neither fixture raster hashes nor style impression identifies fallback face.",
             "decision": "Do not adopt speculative style/fallback-face attribution. Allactual glyphs readable; no actionable missing-glyph finding. Original report preserved unchanged."}
        ],
        "reportQualifications": [
            "Reviewers lackGit/shell. Coordinator verifies exact frozen hashes/no teachingdiff/signature separately; reports preserved unchanged.",
            "Claude scope lists exact reused lines; execution receipts establish complete reused context files returned. No whole reused-article certification.",
            "Statements that links return/systemBack works are supplied runtime assertions plus static destinations, not reviewer-performed gestures. Same for complete-table scrolling: complementary actualframes, not everyoffset/gesture proof.",
            "No alternate in these questions/logs does not certify every larger/random/live pool. Drawing 'Well drawn' refers to injected reference/shape fallback and ungradedpractice, not human-recognition evidence.",
            "494source12 visibly exposes final newword source link; keep per-frame clipping and transport limitation, not superseded blanket claim that link was never visible.",
        ],
        "modelContributionComparison": {
            "matchedScope": "Same frozen teaching/native fixture/receipts/32identical returned PNG payloads, dependent original-session confirmations.",
            "shared": "No actionable teaching/rendering defect; scoped glyph/reading/route acceptance with originalsource/phone limits.",
            "uniqueVerifiedClaudeDefects": [], "uniqueVerifiedGPTDefects": [],
            "qualification": "Findings/optional/limits compared together; no manufactured finding or general model benchmark. GPT precisely identified09versus12footer visibility; original Claude also noted source link fully visible, so not a unique discovery.",
        },
        "payloadAccounting": {
            "archivedSourceCaptures": 57, "assignedUniqueSourceCaptures": 32,
            "otherByteIdenticalSourceFiles": 25, "claudePayloads": 32, "gptPayloads": 32,
            "totalReturnedPayloads": 64, "sourceDimensions": [1080, 2400],
            "returnedDimensions": [900, 2000], "sameReturnedBytesAcrossBoth": True,
            "actualImagePaths": frozen["images"],
        },
        "inheritedEvidence": {
            "textual": "batch-074-reconciliation.json/execution490 unchanged; original reports/range receipts retained.",
            "android": "execution-491.json freshRealContentTest3+RareHanTest1, not rerun.",
            "native": "execution-493.json attempt3 two named terminal0/no skips128.836s, not rerun; all attempts preserved.",
        },
        "reviews": reviews, "checks": checks, "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False, "limits": LIMITS, "nextAction": NEXT,
    }
    m.save(V / "batch-074-visual-reconciliation.json", reconciliation)
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = m.load(R / "manifest.json")
    assert manifest == build_manifest(R)
    count = sum(len(section) for section in manifest.values() if isinstance(section, dict))
    assert count == 8349
    result = {
        "schemaVersion": 1, "execution": 494, "checkpoint": 494, "batch": "074",
        "status": reconciliation["status"], "startingHead": m.HEAD,
        "reviewedTeachingSnapshot": m.TEACHING,
        "authorization": m.load(L / "starting-state.json")["authorization"],
        "scope": m.load(L / "starting-state.json")["scope"], "reviews": reviews,
        "reconciliation": r"docs\n1-reviews\batch-074-visual-reconciliation.json",
        "reconciliationSha256": m.sha(V / "batch-074-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "bothVisualExecutionsInternallySerial": True, "allHistoricalInternalCallsSerial": False,
        "allOriginalReportsAndTeachingUnmodified": True, "runtimeEditsMade": False,
        "nativeOrAndroidRerun": False, "publicationAttempted": False, "runtimePublished": False,
        "publishedAdditions": 100, "remainingAdditions": 1128, "phoneEvidence": False,
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None, "limits": LIMITS,
        "checks": checks, "recordedAt": m.now(),
        "checksSummary": {
            "validatorErrors": 0, "manifestFresh": True, "runtimeHashesVerified": count,
            "contentVersion": "c507eceeb764bc3f",
            "budget": {"entries": 8371, "localZipBytes": 30148761,
                       "inflatedBytes": 44377402, "retainedBytes": 44109064},
            "originalLimitsUnchanged": True,
        },
        "coordinatorDirectImageChecks": [
            "n1-074-font-pairs.png", "n1-074-kanji-09.png", "n1-074-kanji-11.png",
            "n1-074-免れる-12.png", "n1-074-meaning-question.png",
            "n1-074-drawing-feedback.png", "n1-074-curated-Kun-question.png",
        ],
        "evidenceWhitespace": {
            "initialCachedDiffCheckExitCode": 2,
            "affectedFile": "docs/n1-reviews/batch-074-visual-models-execution-494.txt",
            "actualDiagnostic": "line262: new blank line at EOF.",
            "disposition": "Preserve actual current CLI catalog bytes/hash. This sole raw-evidence terminalblank is not runtime/teaching; check allother stagedfiles separately. No signing command started before this check.",
        },
    }
    m.save(R / "docs" / "n1-sources" / "execution-494.json", result)
    batch = m.load(R / "docs" / "n1-sources" / "batch-074-progress.json")
    batch.update(status=reconciliation["status"], nextAction=NEXT, limits=LIMITS)
    batch["visualReviewCheckpoint"] = {
        "execution": 494, "evidenceHead": m.HEAD, "reviewedSnapshot": m.TEACHING,
        "reconciliation": str((V / "batch-074-visual-reconciliation.json").relative_to(R)),
        "reconciliationSha256": result["reconciliationSha256"],
        "boundedIndependentVisualConfirmation": True, "runtimePublished": False,
        "bothVisualExecutionsInternallySerial": True,
    }
    m.save(R / "docs" / "n1-sources" / "batch-074-progress.json", batch)
    receipts = V / "batch-074-visual-receipts"
    receipts.mkdir(exist_ok=True)
    for name in ("execution-494.py", "finish-494.py"):
        shutil.copyfile(L / name, receipts / name)
    print("Both original reports/executions,64returned payloads and qualified reconciliation preserved.")


def checkpoint():
    progress = m.load(C / "progress.json")
    before = m.load(L / "before-progress.json")
    assert progress["checkpoint"] == 493
    for key, value in before.items():
        if key not in {"stage", "nextAction"}:
            assert progress[key] == value, key
    head = m.git("rev-parse", "HEAD")
    assert head != m.HEAD and m.git("log", "-1", "--format=%G?") == "G"
    assert not m.git("status", "--porcelain")
    assert not m.git("diff", m.TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    record_path = R / "docs" / "n1-sources" / "execution-494.json"
    receipt = {
        "execution": 494, "checkpoint": 494, "batch": "074", "status": "continue",
        "savedCommit": head, "signature": "G", "record": str(record_path.relative_to(R)),
        "recordSha256": m.sha(record_path), "runtimePublished": False,
        "boundedIndependentVisualAcceptance": True, "bothVisualExecutionsInternallySerial": True,
        "historicalInitialClaudeOverlapPreserved": True, "nextAction": NEXT,
        "publishedAdditions": 100, "remainingAdditions": 1128,
        "allOriginalHistoricalRootKeysPreserved": True,
    }
    progress.update(checkpoint=494, status="continue", stage="batch-074-visual-closed-awaiting-integration",
                    nextAction=NEXT, blocker=None)
    progress["execution494StartingState"]["status"] = "signed-dependent-visual-checkpoint-complete"
    progress["execution494CoordinatorCheckpoint"] = receipt
    progress["batch074VisualCheckpoint"] = receipt.copy()
    m.save(C / "progress.json", progress)
    m.save(L / "checkpoint-full.json", progress)
    m.save(L / "execution-494-checkpoint.json", receipt)
    body = f"""N1 kanji batch 074: bounded visual confirmation checkpoint 494 saved locally at signed `{head}`; **not published**.

Original reviewers Claude Opus 5.5 and GPT-6.1 Sol confirmed complete new 免 / necessary supporting 免れる and exact reused 免許/免税 component links plus 許 example against the same frozen teaching and native evidence. All five scoped surfaces/all three facets CLEAN; no actionable content defect established. Both reviewer processes exited serially; each execution used only single awaited view calls, zero overlaps or multi-tool responses. The initial Claude 兄/元 parallel read remains explicitly historical, not erased. No new blind initial review, teaching/app changes or native/HOST rerun.

Both families inspected all 32 unique PNGs (25 other captures are exact-byte duplicates), complete 595-line native fixture and terminal/route receipts. Complete reports, actual models/sessions/processes/ranges and all 64 returned image payloads are preserved. Four font rows/all 43 authored Han including isolated 儿 plus three whole words are readable. Complementary tables show every reading disposition; both actual curated kinds/feedback/2-of-2 Done, five reciprocal pairs/ten directions, meaning, tracing/recall and offline/System Back are accepted within the bounded emulator scope. Newword source-link clipped in one frame is fully visible in another. Actual fallback face and every-phone readability are not certified; injected reference tracing is not human handwriting or MLKit evidence.

Fresh validator, unchanged manifest (8,349 runtime hashes; version `c507eceeb764bc3f`) and original budgets pass. Next: fresh-main nonrewriting integration/combined validation, normal signing, authorized owner fast-forward publication, terminal green CI and every immutable public ZIP runtime hash/budget before delivery or batch075.

Published additions remain **100/1,228**, remaining **1,128**; 100 published necessary supports are not an N1 vocabulary deck. Compatible Android `f9b59a2+` required. Physical-phone, general-release and whole-set acceptance remain outstanding.
"""
    (L / "issue-494-body.txt").write_text(body, encoding="utf-8")
    print(f"Saved checkpoint494 signed{head}; statuscontinue; runtimeNOTpublished.")


def finalize():
    progress = m.load(C / "progress.json")
    before = m.load(L / "before-progress.json")
    assert progress["checkpoint"] == 494 and progress["status"] == "continue"
    for key, value in before.items():
        if key not in {"checkpoint", "stage", "nextAction"}:
            assert progress[key] == value, key
    head = m.git("rev-parse", "HEAD")
    assert head == progress["execution494CoordinatorCheckpoint"]["savedCommit"]
    assert m.git("log", "-1", "--format=%G?") == "G" and not m.git("status", "--porcelain")
    assert not m.git("diff", m.TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    android = C.parent / "kanji-cards-android"
    assert not subprocess.check_output(
        ["git", "-C", str(android), "status", "--porcelain"], encoding="utf-8").strip()
    for path, digest in m.load(L / "visual-freeze.json")["resourceHashes"].items():
        assert m.sha(Path(path)) == digest, path
    record_path = R / "docs" / "n1-sources" / "execution-494.json"
    assert m.sha(record_path) == progress["execution494CoordinatorCheckpoint"]["recordSha256"]
    result = m.load(record_path)
    assert m.sha(R / result["reconciliation"]) == result["reconciliationSha256"]
    for review in result["reviews"].values():
        assert m.sha(R / review["report"]) == review["reportSha256"]
        assert m.sha(R / review["execution"]) == review["executionSha256"]
        item = m.load(R / review["execution"])
        exited(item["launcherPid"])
        assert m.sha(Path(item["rawExecutionLocation"])) == item["rawExecutionSha256"]
        for row in item["toolCalls"]:
            if "imagePayload" in row:
                payload = row["imagePayload"]
                assert m.sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
    api = m.load(L / "issue-494-api.json")
    receipt = m.load(L / "issue-494-verified.json")
    assert receipt["author"] == api["user"]["login"] == "stop-cran" and receipt["bodyVerified"]
    assert api["body"].replace("\r\n", "\n").rstrip() == (
        L / "issue-494-body.txt").read_text(encoding="utf-8").rstrip()
    progress["batch074VisualIssueReceipt"] = receipt
    for key in ("execution494CoordinatorCheckpoint", "batch074VisualCheckpoint"):
        progress[key]["issueUpdate"] = receipt["url"]
        progress[key]["ownerAuthorAndBodyVerified"] = True
    m.save(C / "progress.json", progress)
    m.save(L / "checkpoint-full.json", progress)
    m.save(L / "execution-494-checkpoint.json", progress["execution494CoordinatorCheckpoint"])
    m.save(L / "execution-494-final-verification.json", {
        "execution": 494, "checkpoint": 494, "status": "continue", "batch": "074",
        "savedCommit": head, "signature": "G", "contentAndAndroidClean": True,
        "historicalRootValuesPreserved": True, "reviewerProcessesExitedSerially": True,
        "bothVisualExecutionsInternallySerial": True, "historicalInitialDeviationPreserved": True,
        "returnedPayloadsVerified": 64, "runtimePublished": False,
        "issueReceipt": receipt, "verifiedAt": m.now(),
    })
    print("Checkpoint494 verified: signed local evidence, FULL historical values preserved, owner issue receipt; statuscontinue.")


if __name__ == "__main__":
    {"record": record, "checkpoint": checkpoint, "finalize": finalize}[sys.argv[1]]()
