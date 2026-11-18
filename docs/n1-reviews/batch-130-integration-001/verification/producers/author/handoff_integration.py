import json
import re
import stat
from pathlib import Path
from integration_common import CONTENT, DELTA, FIRST, HERE, REPO, SCRATCH, SECOND, git, live_target, load, parents, sha, start_guard, write

DEST = HERE / "handoff-001"
assert not DEST.exists()
DEST.mkdir()
guard = start_guard()
try:
    head = parents("committed")
    assert head == "37a53e75446bacad8ade4e212404b121d4a01af1"
    live_target()
    inspection = load(HERE / "inspection-001" / "summary.json")
    author = load(HERE / "author-preserve-001" / "summary.json")
    committed = load(HERE / "committed-preserve-001" / "summary.json")
    signing = load(HERE / "signing-001" / "summary.json")
    assert author["status"] == committed["status"] == "PASS"
    assert signing["status"] == "SIGNED" and signing["attempt"] == 1
    assert author["tree"] == committed["tree"] == signing["tree"] == git("rev-parse", "HEAD^{tree}").decode().strip()
    assert author["trackedComparisonSha256"] == committed["trackedComparisonSha256"]
    assert author["runtimeHashesSha256"] == committed["runtimeHashesSha256"]
    assert author["manifestSha256"] == committed["manifestSha256"]
    git("verify-commit", "HEAD")
    write(DEST / "merge-signature.log", git("show", "-s", "--show-signature", "--format=fuller", "HEAD"))
    directories = ("inspection-001", "merge-001", "manifest-resolution-001",
                   "author-gates-001", "author-preserve-001", "signing-001",
                   "committed-gates-001", "committed-preserve-001")
    bindings = {}
    for name in directories:
        directory = HERE / name
        if "gates" in name:
            summary = load(directory / "summary.json")
            assert summary["status"] == "PASS" and summary["serial"] and len(summary["checks"]) == 10
            assert summary["manifestSha256"] == committed["manifestSha256"]
            for check in summary["checks"]:
                receipt = load(directory / (check + ".json"))
                assert receipt["exitCode"] == 0 and not receipt["memory"]["breach"]
                assert sha((directory / (check + ".log")).read_bytes()) == summary["logs"][check]["logSha256"]
                assert sha((directory / (check + ".json")).read_bytes()) == summary["logs"][check]["receiptSha256"]
        binding = {}
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                guard.check()
                relative = path.relative_to(directory)
                raw = path.read_bytes()
                write(DEST / "evidence" / name / relative, raw)
                binding[relative.as_posix()] = sha(raw)
        bindings[name] = {"originalDirectory": str(directory), "bundledDirectory": "evidence/" + name, "files": binding}
    for path in sorted(HERE.glob("*.py")):
        write(DEST / "tooling" / path.name, path.read_bytes())
    for path in (SCRATCH / "b130_common.py", SCRATCH / "run_b130_gates.py", SCRATCH / "check_reading_b130.py",
                 SCRATCH.parent / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"):
        write(DEST / "tooling" / "original" / path.name, path.read_bytes())
    brief = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b130-integration-author-brief.txt")
    admission = SCRATCH / "review" / "integration-author-admission-001" / "admission.json"
    assert sha(brief.read_bytes()) == inspection["briefSha256"]
    assert sha(admission.read_bytes()) == inspection["coordinatorAdmissionSha256"]
    write(DEST / "frozen-inputs" / brief.name, brief.read_bytes())
    write(DEST / "frozen-inputs" / "coordinator-admission.json", admission.read_bytes())
    for rel in CONTENT:
        raw = (REPO / rel).read_bytes()
        assert raw == git("show", SECOND + ":" + rel)
        write(DEST / "incoming-content" / rel, raw)
    write(DEST / "incoming-content.patch", (HERE / "inspection-001" / "incoming-content.patch").read_bytes())
    write(DEST / "integrated-manifest.json", (REPO / "manifest.json").read_bytes())
    write(DEST / "integration.patch", (HERE / "committed-preserve-001" / "integration.patch").read_bytes())
    exact = {}
    for rel in sorted(DELTA):
        raw = git("show", head + ":" + rel)
        exact[rel] = {
            "firstParentBlob": git("rev-parse", FIRST + ":" + rel).decode().strip(),
            "integrationBlob": git("rev-parse", head + ":" + rel).decode().strip(),
            "incomingBlob": git("rev-parse", SECOND + ":" + rel).decode().strip(),
            "integrationSha256": sha(raw), "incomingSha256": inspection["before"][rel]["incomingSha256"],
            "byteExactIncoming": rel in CONTENT,
        }
    tests = (HERE / "committed-gates-001" / "unittest.log").read_text(encoding="utf-8")
    test_count = re.search(r"Ran (\d+) tests in [\d.]+s", tests)
    assert test_count and "\nOK\n" in tests
    safety = (HERE / "committed-gates-001" / "quiz-safety.log").read_text(encoding="utf-8")
    warnings = [line for line in safety.splitlines() if line.startswith("WARN")]
    assert len(warnings) == 83
    readings = (HERE / "committed-gates-001" / "reading-exposure.log").read_text(encoding="utf-8")
    assert "0 production hit(s)" in readings and "0 padded-session hit(s)" in readings
    write(DEST / "handoff.json", {
        "status": "LOCAL-SIGNED-AUTHOR-INTEGRATION-NOT-CONFIRMATION-OR-PUBLICATION",
        "candidate": head, "parentsInOrder": [FIRST, SECOND], "mergeBase": inspection["mergeBase"],
        "tree": committed["tree"], "clean": True, "worktree": str(REPO),
        "ownerSignature": committed["ownerSignature"],
        "requiredCopilotAppTrailerVerified": True, "signingAttempts": 1,
        "parentSignatureEvidence": inspection["signatures"],
        "exactThreeFileDeltaFromFirstParent": exact,
        "incomingCompleteContentFiles": ["incoming-content/" + rel for rel in sorted(CONTENT)],
        "incomingContentDiff": "incoming-content.patch",
        "fullIntegrationDiff": "integration.patch",
        "mergeResolution": {
            "normalNoCommitTwoParentMerge": True, "expectedConflictOnly": ["manifest.json"],
            "conflictBytesPreserved": "evidence/merge-001/conflicted-manifest.json",
            "resolvedBy": "Unchanged existing build_manifest.py; neither parent manifest selected wholesale.",
            "readOnlyTargetsBeforeMerge": inspection["before"],
            "attributeAdjustments": [],
        },
        "trackedMembershipPreserved": True,
        "fullTrackedBlobAndModeComparison": {
            "path": "evidence/committed-preserve-001/tracked-blob-comparison.json",
            "sha256": committed["trackedComparisonSha256"], "entries": committed["trackedBlobsCompared"],
            "unchangedExceptThree": committed["allOtherTrackedBlobsAndModesUnchanged"],
        },
        "runtimeMembershipPreserved": True,
        "allRuntimeHashes": {
            "path": "evidence/committed-preserve-001/runtime-hashes.json",
            "sha256": committed["runtimeHashesSha256"], "entries": 8730,
            "changedOnly": sorted(CONTENT), "unchanged": 8728,
            "changedValuesMatchIncomingCommitAndManifest": True,
        },
        "allN1CardsSupportsMetadataPracticeExclusionsSourcesReviewsProgressNotesUnchanged": True,
        "manifestSha256": committed["manifestSha256"], "contentVersion": committed["contentVersion"],
        "manifestReproducibleByteExactly": True,
        "authorGateSummarySha256": bindings["author-gates-001"]["files"]["summary.json"],
        "committedGateSummarySha256": bindings["committed-gates-001"]["files"]["summary.json"],
        "committedPreservationSummarySha256": bindings["committed-preserve-001"]["files"]["summary.json"],
        "bothTenGateSets": "PASS; same original commands/order and full f237a8d5 published-base lint/link/payload scope.",
        "actualHostTests": int(test_count.group(1)), "nonfatalNotesMentionWarnings": warnings,
        "receiptBindings": bindings,
        "tooling": "Exact scratch integration envelopes and original reused helper/gate/reading/guard implementations are bundled. They retain the original absolute-layout dependencies; no standalone portability claim.",
        "resourceAndCleanup": "Every original memory/cleanup receipt is bundled; >2GiB admission, <1GiB abort,0.25s sampling, child waits<=0.1s, terminate/kill<=10s each. No guard weakening or unrelated process changes.",
        "remote": {"mainBeforeMerge": SECOND, "mainCheckedAgainBeforeSigningAndAtHandoff": SECOND,
                   "noAlternativeFetchTargetSubstituted": True, "pushPerformed": False},
        "retainedLimits": [
            "Author integration evidence only; earlier closure and confirmations remain historical on their exact reviewed snapshot, not approval of this new global manifest.",
            "No new independent linguistic/source review of the counter fix; its two complete signed incoming files are preserved byte-exactly.",
            "Existing N1 historical image/rare-spelling allocations, unread-index scope and supplemental-reading limitations remain unchanged.",
            "Bounded host N1/All/Starter-plus-one readings only: zero tested production/padded hits but latent 拍ひゃく and 耗ぼう remain outside drawable tested pools.",
            "No arbitrary/custom/multiple-borrow/Kotlin/native/device/old-APK/font-rendering acceptance; prior 尸/并/扌/耒 cmap limitation remains.",
            "Mechanical gates and manifest reproduction are not served-archive identity, CI/publication acceptance, release approval or whole-N1 completion.",
        ],
        "accounting": {"publishedDelivered": 261, "frozenTotal": 1228, "undelivered": 967,
                       "localUnpublishedDrafts": 3, "deliveryCredit": 0},
        "boundary": "One normal local two-parent integration, no rebase/amend/force/history rewrite, reviewer contact/launch, push/publication or next batch. All new tooling/proof/receipts are scratch-only.",
        "freezeDisclosure": "New bundle files are made read-only only after their final writes and hashes; no historical immutability claim.",
        "bundleInventory": "evidence-inventory.json",
        "collectorSha256": sha(Path(__file__).read_bytes()),
    })
    assert parents("committed") == head
    assert git("rev-parse", "HEAD^{tree}").decode().strip() == committed["tree"]
finally:
    write(DEST / "memory.json", guard.finish())

inventory = {path.relative_to(DEST).as_posix(): sha(path.read_bytes())
             for path in sorted(DEST.rglob("*")) if path.is_file()}
write(DEST / "evidence-inventory.json", {"files": inventory, "selfExcluded": True,
                                       "freeze": "Read-only applied after final file writes/hash; not historical immutability."})
for path in DEST.rglob("*"):
    if path.is_file():
        path.chmod(stat.S_IREAD)
assert all(path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
           for path in DEST.rglob("*") if path.is_file())
print(json.dumps({
    "candidate": head, "parentsInOrder": [FIRST, SECOND], "tree": committed["tree"],
    "handoff": str(DEST / "handoff.json"), "handoffSha256": sha((DEST / "handoff.json").read_bytes()),
    "bundleInventorySha256": sha((DEST / "evidence-inventory.json").read_bytes()),
    "bundleBoundFiles": len(inventory),
    "authorGatesSummarySha256": bindings["author-gates-001"]["files"]["summary.json"],
    "committedGatesSummarySha256": bindings["committed-gates-001"]["files"]["summary.json"],
    "committedPreservationSummarySha256": bindings["committed-preserve-001"]["files"]["summary.json"],
    "manifestSha256": committed["manifestSha256"], "contentVersion": committed["contentVersion"],
    "newBundleReadOnly": True,
}))
