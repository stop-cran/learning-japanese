"""Archive serial correction confirmations and preserve the complete live history."""
import gzip
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("correction685", C / "confirm-batch-094-correction-685.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
V, R, L = m.V, m.R, m.L
E = R / "docs" / "n1-sources" / "execution-685.json"
REVIEW = V / "batch-094-correction-reconciliation-685.json"
STAGE = "correction-textually-confirmed-awaiting-exact-native-import"
NEXT = (
    "SAME094 only: read docs/n1-sources/execution-685.json and "
    "docs/n1-reviews/batch-094-correction-reconciliation-685.json. BOTH original sessions "
    "confirmed exact signed correction b85d7a4d, version74b7e886a1afbd46: direct "
    "削る/縮める declaration textually resolved; corrected runtime enforcement STILL PENDING. "
    "Processes29888Claude/25728GPT exited0, actual claude-opus-5.5/gpt-6.1-sol, strict serial "
    "3/2 complete text reads/no overlaps. Dependent confirmations, NOT newblind review. "
    "Next bounded checkpoint: exact corrected manifest/full git archive through production "
    "ContentSync ONCE, assert1117kanji5070words126N1/zeroProblems/Roomepoch1/version/"
    "every8438runtimehash. Focus production builder guard checks for 削る/縮める, BOTH directions "
    "and BOTH target orientations, All+boundedcustom, with non-skipped terminal native evidence. "
    "Use durable control/native682 recipes and committed source packets; inspect before reuse "
    "and update exact frozen heads/version/hash, retain old fixtures immutable. Native682/archive"
    "18ad4bed/versioneeae47753a460f72 and85unchanged visual captures remain inherited ONLY, "
    "not corrected-import evidence. No repeat121families/85captures without new concern. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "Immediately inspect device/port ownership; start/stop only owned helper, original limits "
    "and flags, no shared/owner interference, heaps/archive guards unchanged. No physicalphone/"
    "humanhandwriting/successfulMLKit claim. Resolve consequential claims before acceptance. "
    "Then fresh current-main normal merge/reconcile, changedteaching review and ALL combined "
    "content/Python/vocabulary/baseline/link/membership/reading/font/budget/applicable Android "
    "checks remain. Normal signing/ownerfastforward/terminalgreenCI/EVERY immutable publicZIP "
    "runtimehash/18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/"
    "verifiedownerissue gates unchanged. No095/runtimepublication/secondrunner at this checkpoint. "
    "Parent19008 ownsrunner.lock: verify live ancestry/session/signedheads/whollyclean, NOchild "
    "acquire/delete/unlock. Approvedcontrol/committed packets only, NO optionalhistoricalsession"
    "helpers. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "OriginalClaude683overlap/rejection/serialrepair retained unchanged. Published120/1228,"
    "1108remaining; physicalphone/generalrelease/whole-set outstanding."
)


def archive():
    m.frozen()
    runtime = m.runtime()
    records = [m.m.load(C / f"batch-094-correction-685-{label}-execution.json")
               for label in ["claude", "gpt"]]
    assert records[0]["completedAt"] < records[1]["startedAt"]
    for label, record, expected_reads in zip(["claude", "gpt"], records, [3, 2]):
        assert record["acceptedExecution"] and record["exitCode"] == 0
        assert record["processExitVerified"] and not record["observedToolOverlaps"]
        assert len(record["toolCalls"]) == expected_reads and not record["unfinishedTools"]
        assert record["successfullyReturnedResources"] == record["requiredResources"]
        m.stopped(record["launcherPid"])
    sources = [Path(__file__), C / "confirm-batch-094-correction-685.py",
               C / "post-batch-094-correction-685.ps1", C / "batch-094-correction-common-685.txt"]
    sources += [C / f"batch-094-correction-cli-{kind}-685.txt" for kind in ["help", "config"]]
    receipts = []
    for label, record in zip(["claude", "gpt"], records):
        prefix = C / f"batch-094-correction-685-{label}"
        assert m.m.sha(prefix.with_suffix(".jsonl")) == record["rawSha256"]
        assert m.m.sha(prefix.with_suffix(".md")) == record["reportSha256"]
        sources += [prefix.with_suffix(suffix) for suffix in [
            ".jsonl", ".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"]]
        sources += [C / f"{prefix.name}-execution.json",
                    C / f"batch-094-correction-{label}-resources-685.json"]
    for source in sources:
        compressed = source.suffix == ".jsonl" or source.name in {
            "batch-094-correction-cli-config-685.txt", "batch-094-correction-common-685.txt"}
        target = V / (source.name + (".gz" if compressed else ""))
        assert not target.exists(), str(target)
        if compressed:
            target.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(target.read_bytes()) == source.read_bytes()
        else:
            shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": m.m.sha(source), "archiveSha256": m.m.sha(target),
                         "losslessGzip": compressed})
    reconciliation = {
        "schemaVersion": 1, "execution": 685, "batch": "094",
        "snapshot": m.HEAD, "contentVersion": m.VERSION, "status": STAGE,
        "dependentOriginalSession": True, "newBlindInitialReviewCredit": False,
        "originalSessionRecords": [
            f"docs/n1-reviews/batch-094-correction-685-{label}-execution.json"
            for label in ["claude", "gpt"]],
        "processAcceptance": {
            "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"],
            "launcherPids": [record["launcherPid"] for record in records],
            "strictSerialToolReads": [3, 2], "noToolOverlap": True,
            "allRequestedTextsCompletelyReturnedInOrder": True,
            "firstProcessExitVerifiedBeforeSecondLaunch": True,
            "allProcessesExited": True,
            "original683OverlapRejectionAndSerialRepairUnchanged": True,
        },
        "reconciliation": [{
            "id": "094-observed-kezuru-chijimeru", "status": "partially resolved",
            "severity": "minor", "facet": "word meaning quiz correctness",
            "file": "words/削る.md:9",
            "textualDisposition": "Resolved: one directly justified exclusion appended; both original sessions confirm narrow correctness/coverage/comprehensibility with no new actionable defect.",
            "runtimeDisposition": "Unresolved/pending: exact corrected native ContentSync import and production builder enforcement have not been run.",
            "evidence": [
                "Exact da2905cd..b85d7a4d runtime diff; only appended 縮める and generated manifest hash/version.",
                "Complete frozen JMdict1298090 sense2 and1337570 sense1 directly support shared reduction senses.",
                "Both complete current articles and docs/content-format.md direct-pair contract supplied to both reviewers.",
                "Both original-session complete reports and audited serial full-text returns retained.",
            ],
            "confidence": "High for direct lexical overlap and source/declaration closure; no extrapolation to corrected runtime enforcement.",
            "discoveryCredit": "Prior coordinator-supplied hypothesis, dependent confirmations; no new blind discovery or comparative-model credit.",
        }],
        "facetVerdicts": {"narrowDirectPairDeclaration": {
            "correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"},
            "correctedRuntimeEnforcement": {
                "correctness": "UNVERIFIED", "scopedCoverage": "UNVERIFIED", "comprehensibility": "UNVERIFIED"}},
        "baseClarification": "684 audit baseCommit48765e20 is published batch baseline; correctionBaseda2905cd is immediate pre-correction signed snapshot. Exact diff uses the latter; no source-version substitution.",
        "optional": "Earlier optional polish remains optional; no prose/title expansion and no new exclusion inferred through transitive closure.",
        "limits": [
            "Full requested text delivery and process compliance verified, not proof of comprehension.",
            "No fresh121family/visual/upstream review; original sources and85unchanged visual captures inherited.",
            "No reviewer-run tests, corrected native import, full-pool semantic certification, physicalphone, handwriting/MLKit, latestappmain, generalrelease, whole-set or publication acceptance.",
        ],
        "runtimeChangedThisExecution": False, "runtimeAccepted": False, "runtimePublished": False,
        "nextAction": NEXT,
    }
    m.m.save(REVIEW, reconciliation)
    m.m.save(E, {
        "schemaVersion": 1, "execution": 685, "batch": "094", "status": STAGE,
        "startingState": m.m.load(C / "progress.json")["execution685StartingState"],
        "reviewRecord": REVIEW.relative_to(R).as_posix(), "receipts": receipts, "runtime": runtime,
        "originalSessionReviewerProcesses": 2, "allReviewerProcessesExited": True,
        "strictSerialProcessesAndToolReadsAccepted": True,
        "findingDisposition": "Source/declaration textually resolved; corrected native enforcement pending.",
        "runtimeAccepted": False, "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": "48765e20846e1d6769c6ddc35146f6ce58deab57",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Both original-session confirmations archived; textual closure only.")


def finalize():
    m.frozen(final=True)
    runtime = m.runtime()
    evidence = m.m.load(E)
    expected = {row["archive"] for row in evidence["receipts"]} | {
        E.relative_to(R).as_posix(), REVIEW.relative_to(R).as_posix()}
    changed = subprocess.check_output(
        ["git", "-C", str(R), "diff", "--name-only", "-z", m.HEAD, "HEAD"]).decode("utf-8").split("\0")
    assert set(filter(None, changed)) == expected
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert m.m.sha(path) == row["archiveSha256"]
        if row["losslessGzip"]:
            assert m.hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == row["sourceSha256"]
    prefix = C / "batch-094-correction-685-issue-"
    body = Path(str(prefix) + "body.txt").read_bytes().decode("utf-8-sig")
    receipt = m.m.load(Path(str(prefix) + "receipt.json"))
    posted = m.m.load(Path(str(prefix) + "posted.json"))
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state = m.m.load(C / "progress.json")
    before = m.m.load(L / "progress-before-685.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[key] == value for key, value in before.items() if key not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 685, "checkpoint": 685, "batch": "094",
        "savedCommit": m.m.git("rev-parse", "HEAD"), "signature": "G",
        "status": "continue", "stage": STAGE, "evidence": E.relative_to(R).as_posix(),
        "reviewRecord": evidence["reviewRecord"], "originalSessionReviewerProcesses": 2,
        "allReviewerProcessesExited": True, "strictSerialProcessesAndToolReadsAccepted": True,
        "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "findingDisposition": evidence["findingDisposition"], "newBlindInitialReviewCredit": False,
        **runtime, "runtimeAccepted": False, "runtimePublished": False,
        "correctedNativeImportAndBuilderChecks": "pending", "freshAndroidOrNativeClaimed": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": "48765e20846e1d6769c6ddc35146f6ce58deab57",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    state.update(checkpoint=685, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution685CoordinatorCheckpoint"] = checkpoint
    state["batch094CorrectionConfirmationCheckpoint"] = checkpoint
    state["execution685StartingState"]["status"] = "signed-local-correction-confirmation-checkpoint-complete"
    m.m.save(C / "progress.json", state)
    reread = m.m.load(C / "progress.json")
    assert all(reread[key] == value for key, value in before.items() if key not in allowed)
    m.m.save(L / "checkpoint-685.json", checkpoint)
    print("Checkpoint685 persisted; all", len(before), "original historical root values preserved.")
    print(checkpoint["savedCommit"], checkpoint["issueUpdate"])


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
