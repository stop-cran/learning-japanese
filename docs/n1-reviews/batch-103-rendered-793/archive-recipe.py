"""Preserve original reports and measured delivery limits without publication."""
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import importlib.util

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("review793", C / "review-rendered-793.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, W, L = review.R, review.W, review.L
D = R / "docs" / "n1-reviews" / "batch-103-rendered-793"
review.frozen()
assert not D.exists()
labels = ["claude", "gpt", "claude-transport", "gpt-transport"]
records = []
archive_records = []
for label in labels:
    record = review.load(W / f"{label}-execution.json")
    family = label.split("-")[0]
    assert record["actualModels"] == [review.MODELS[family]]
    assert record["usageCurrentModel"] == review.MODELS[family]
    assert record["exitCode"] == 0 and record["processExited"]
    assert review.absent(record["launcherPid"])
    assert not record["observedToolOverlaps"] and not record["unfinishedTools"]
    assert record["multiToolResponseCount"] == 0
    assert all(c["name"] == "view" for c in record["toolCalls"])
    if "transport" not in label:
        assert record["allAssignedTextReturned"] and not record["missingImages"]
        assert len({i["path"] for i in record["successfulImageOpens"]}) == 73
        assert not record["allOriginalImageBytesDelivered"]
        assert all(p["pngDimensions"] == [900, 2000]
                   and p["originalPngDimensions"] == [1080, 2400]
                   and not p["equalsOriginalBytes"]
                   for i in record["successfulImageOpens"] for p in i["payloads"])
    else:
        assert not record["toolCalls"]
    records.append(record)
for previous, current in zip(records, records[1:]):
    assert previous["completedAt"] < current["startedAt"]
D.mkdir()
for label, record in zip(labels, records):
    for suffix in [".md", "-execution.json", "-process.json", "-stderr.txt", "-usage.json"]:
        shutil.copyfile(W / (label + suffix), D / (label + suffix))
    for suffix in [".jsonl", "-task.txt"]:
        source = W / (label + suffix)
        archived = D / (label + suffix + ".gz")
        raw = source.read_bytes()
        archived.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(archived.read_bytes()) == raw
        archive_records.append({
            "archive": archived.name, "archiveSha256": review.sha(archived),
            "rawSha256": review.sha(source), "rawBytes": len(raw),
            "archiveBytes": archived.stat().st_size,
        })
    if (W / f"{label}-initial-audit.json").exists():
        shutil.copyfile(W / f"{label}-initial-audit.json", D / f"{label}-initial-audit.json")
for name in ["cli-help.txt", "cli-config-help.txt"]:
    source = W / name
    archived = D / (name + ".gz")
    archived.write_bytes(gzip.compress(source.read_bytes(), compresslevel=9, mtime=0))
    assert gzip.decompress(archived.read_bytes()) == source.read_bytes()
    archive_records.append({"archive": archived.name, "archiveSha256": review.sha(archived),
                            "rawSha256": review.sha(source), "rawBytes": source.stat().st_size,
                            "archiveBytes": archived.stat().st_size})
for source, target in [
    (C / "review-rendered-793.py", "review-recipe.py"),
    (C / "preflight-793.ps1", "preflight-recipe.ps1.txt"),
    (Path(__file__), "archive-recipe.py"),
]:
    shutil.copyfile(source, D / target)
warnings = {}
compactions = {}
for label in labels:
    events = [json.loads(line) for line in (W / f"{label}.jsonl").read_text(
        encoding="utf-8-sig").splitlines() if line.strip()]
    warnings[label] = [e for e in events if e["type"] == "session.warning"]
    compactions[label] = sum(e["type"] == "session.compaction_complete" for e in events)
review.save(D / "archive-integrity.json", archive_records)
review.save(D / "process-order.json", [
    {k: record[k] for k in ["sessionId", "requestedModel", "actualModels", "launcherPid",
                            "startedAt", "completedAt", "exitCode", "processExited"]}
    for record in records
])
evidence = {
    "schemaVersion": 1, "execution": 793, "batch": "103", "recordedAt": review.now(),
    "stage": "original-family-rendered-confirmations-and-delivery-scope-reconciliation-preserved",
    "startingState": review.load(L / "starting-state-793.json"),
    "sourceSnapshot": review.HEAD, "unchangedTeachingSnapshot": "08e76c1688ada4898a79e25e13650687dadf65d1",
    "qualifiedAndroidHead": review.APP,
    "evidenceDirectory": str(D.relative_to(R)).replace("\\", "/"),
    "originalSessionConfirmationsExecuted": 2, "deliveryScopeClarificationsExecuted": 2,
    "newBlindInitialReviewCredit": 0, "reviewerProcessesSerial": True,
    "reviewerToolsSerial": True, "allReviewerProcessesExited": True,
    "actualModels": review.MODELS, "originalSessions": review.SESSIONS,
    "commonResourceCount": 9, "commonResourceBytes": 770700,
    "bothCompleteAssignedTextRangesReturnedExactly": True,
    "sourceEvidenceInherited": {
        "execution": 792, "completeDictionaryFamilies": 333, "completeRawCharacterRecords": 46,
        "suppliedArticleBodies": 120, "distinctSampledLabels": 39,
        "hostExactOptionSets": 64, "nativeExactOptionSets": 64,
        "limits": "Supplied frozen records; byte/range delivery is not equal comprehension or independent upstream retrieval.",
    },
    "actualImageTransport": {
        "requestedOriginalPathsPerReviewer": 73,
        "originalDimensions": [1080, 2400], "deliveredDimensions": [900, 2000],
        "claudeSuccessfulToolResponses": 73, "gptSuccessfulToolResponses": 125,
        "gptRepeatedPathResponsesBeyond73": 52,
        "originalPixelPayloadsDelivered": 0, "coordinatorCreatedRescaledSubstitutes": False,
        "mechanism": "CLI view automatically returned rescaled binaryResultsForLlm for original source paths.",
        "originalFileHashesUnchanged": True, "sourceDistinctByteHashes": 33,
        "gptReportedVisualCoverage": "All73 paths eventually inspected; independently reconstructable visual inspection and uninterrupted retention of every payload UNVERIFIED.",
        "originalPixelAndEqualComprehensionAcceptance": "UNVERIFIED",
        "limits": "Successful tool return does not prove availability in every later model request or comprehension. No fresh native rerun/full-resolution review claimed.",
    },
    "warnings": warnings, "contextCompactions": compactions,
    "reviewDispositions": [
        {
            "observation": "Four new articles and exact three navigation-only reused passages",
            "status": "resolved", "verdict": "Both retain correctness/scoped coverage/comprehensibility CLEAN in bounded text and delivered-scale scope.",
        },
        {
            "observation": "Ordinary-secondary-sense ambiguity in128 exact HOST/native samples plus live default",
            "status": "resolved", "verdict": "Both CLEAN for exact finite samples; no demonstrated competing answer. Unrestricted pool remains UNVERIFIED.",
        },
        {
            "observation": "Four-font47Han/厂 and reading/drawing/route presentation",
            "status": "partially resolved",
            "verdict": "Both retain delivered900x2000 rendition readability/distinguishability CLEAN. Original/native pixels, equal comprehension and GPT independently reconstructable complete visual retention remain UNVERIFIED; no demonstrated consequential glyph/text defect.",
        },
        {
            "observation": "GPT original report described52 unsuccessful/image-limit reads",
            "status": "resolved", "severity": "Moderate reporting defect",
            "evidence": "Actual125 successful tool responses,73 unique paths,52 repeats, ONE request-pruning warning removing25 images to meet50-image request limit. Original complete report preserved; original-session clarification corrects accounting.",
        },
        {
            "observation": "Claude original report calls word-2-13 a larger capture",
            "status": "withdrawn", "evidence": "All delivered images are900x2000; own clarification withdraws size-difference claim.",
        },
        {
            "observation": "Full-resolution/original-pixel and every-request image-retention evidence",
            "status": "unresolved", "verdict": "UNVERIFIED limitation; not converted to a demonstrated content failure or silently treated as completed original-pixel acceptance.",
        },
        {
            "observation": "App-wide Practice not graded versus Graded by stroke shapes wording",
            "status": "optional", "evidence": "Both independently noticed same wording; no required in-batch teaching correction. No app changes authorized here.",
        },
    ],
    "ordinarySenseFallbackSemanticAcceptance": "CLEAN only128 exact sampled sets plus live default",
    "independentRenderedReviewClosed": False,
    "boundedDeliveredRenditionReviewVerdict": "CLEAN with explicit original-pixel/retention limitations",
    "fullBatchAcceptanceComplete": False, "runtimeAccepted": False, "runtimePublished": False,
    "runtimeChanged": False, "manifestChanged": False, "freshNativeExecuted": False,
    "reviewClosed": [], "published": [], "nextBatchStarted": False,
    "publishedAdditions": 129, "remainingAdditions": 1099,
    "lastPublishedCommit": "a38f4cf554300ce34ee65aada79e87b7c9d0319e",
    "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
    "actualNewPermissionDenials": [],
    "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
    "wholeProjectComplete": False,
    "nextAction": "SAME103 bounded final acceptance reconciliation of original reports+transport clarifications, exact per-call/model-request image coverage limitations and inherited native791 evidence. Do not equate scaled payloads with original pixels or GPT125 successful tool returns with125 inspections/52 failures. No new blind initial credit; no repeated all73 reread loop. Establish honest bounded rendering disposition before batch acceptance. Then, only if no consequential unresolved in-scope claim remains, required combined-current-main/nonrewriting merge/changed-teaching review/Python/vocabulary/baseline/link/membership/manifest/budget/app checks/normal signed owner fast-forward/terminal CI/all immutable ZIP hashes/media/path checks and issue receipt before delivery. No104 or publication at this checkpoint.",
}
assert not (R / "docs" / "n1-sources" / "execution-793.json").exists()
review.save(R / "docs" / "n1-sources" / "execution-793.json", evidence)
review.save(W / "archival-summary.json", {
    "recordedAt": review.now(), "evidence": "docs/n1-sources/execution-793.json",
    "archives": len(archive_records), "archiveBytes": sum(a["archiveBytes"] for a in archive_records),
    "allProcessesExited": True, "runtimeChanged": False,
})
print("Preserved four complete reports, raw execution archives, exact source/image audits and honest limitations.")
