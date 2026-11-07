import gzip
import importlib.util
import re
import shutil
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("verify686", C / "verify-batch-094-correction-686.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R, A, L, W = m.R, m.A, m.L, m.WORK
DEST = R / "docs" / "n1-reviews" / "batch-094-native" / "execution-686"
EVIDENCE = R / "docs" / "n1-sources" / "execution-686.json"
REVIEW = R / "docs" / "n1-reviews" / "batch-094-correction-reconciliation-686.json"
STAGE = "corrected-native-passed-awaiting-combined-current-main-checks"
NEXT = (
    "SAME094 only: read docs/n1-sources/execution-686.json and "
    "docs/n1-reviews/batch-094-correction-reconciliation-686.json. Exact corrected fullarchive "
    "5f0be667/version74b7e886a1afbd46/every8438runtimehash imported through productionContentSync "
    "ONCE:1117kanji5070words126N1/zeroProblems/acceptedRoomepoch1. Focused native case terminal0/no "
    "skips;128 productionWordQuizBuilder checks for direct 削る/縮める guard, BOTHtargetorientations/"
    "BOTHdirections/All+boundedcustom/16seeds. Direct declaration+runtime finding RESOLVED using "
    "original-session textual confirmations685 plus native686. No fullpool semantic certification. "
    "Fresh native686 is not a new visual/phone review;85 unchanged captures/font/route682 and "
    "rendered original-session confirmations683 remain inherited, original683 overlap/rejection/"
    "serialrepair preserved. Owned emulator5580 parent29596/QEMU23836 stopped, temporary Android "
    "source/asset removed; heaps/archiveguards unchanged. No need repeat121families/85captures "
    "absent new concern. Next bounded checkpoint: fetch latest origin/main, normal nonrewriting "
    "merge/reconcile only if needed; independently re-review changed substantive teaching. Run "
    "ALL required combined-current-tree content/Python/vocabulary/baseline/link/membership/"
    "reading/font/budget and applicable Android checks with RealContent/RareHan non-skipped. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Keep normal "
    "signing/ownerfastforward/terminalgreenCI/EVERY immutable publicZIP runtimehash/original "
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue "
    "gates. Native686 local GitZIP is NOT publicGithubZIP acceptance. No095/runtimepublication/"
    "secondrunner at686; reviewClosed/runtimeAccepted/runtimePublished remain pending combined "
    "acceptance. Parent19008 retainsrunner.lock: verify live ancestry/session/signedheads/whollyclean; "
    "NOchild acquire/delete/unlock. Approvedcontrol/committed packets only, NO optionalhistorical"
    "sessionhelpers. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. No physical"
    "phone/humanhandwriting/successfulMLKit claim. Published120/1228,1108remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding."
)


def audit():
    v, execution, result = [m.load(W / name) for name in [
        "verification.json", "execution.json", "n1-094-correction-686.json"]]
    assert execution["passed"] and execution["failure"] is None
    assert execution["compiled"] and execution["compileExitCode"] == 0
    assert execution["nativeExecuted"] and execution["adbExitCode"] == 0
    assert execution["terminalSuccessCases"] == 1
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"] and execution["stopAdbExitCode"] == 0
    assert not any(execution[k] for k in ["guestOrAppHeapChanged", "guardsChanged", "parentLockTouched"])
    assert execution["contentSnapshot"] == result["contentSnapshot"] == m.HEAD
    assert execution["contentVersion"] == result["contentVersion"] == m.VERSION
    assert (result["archiveRequests"], result["importedKanji"], result["importedWords"],
            result["n1Cards"], result["problems"], result["acceptedReadingParserEpoch"]) == (1, 1117, 5070, 126, 0, 1)
    rows = result["directGuardBuilderChecks"]
    expected = {(target, excluded, pool, direction, seed)
                for target, excluded in [("削る", "縮める"), ("縮める", "削る")]
                for pool in ["All", "boundedCustom"]
                for direction in ["JpToEn", "EnToJp"] for seed in range(16)}
    assert len(rows) == len(expected) == 128
    assert {(r["target"], r["excluded"], r["pool"], r["direction"], r["seed"]) for r in rows} == expected
    for row in rows:
        assert row["poolSize"] == (5070 if row["pool"] == "All" else 14)
        assert len(row["options"]) == len({r["label"] for r in row["options"]}) == 4
        assert sum(r["word"] == row["target"] for r in row["options"]) == 1
        assert not any(r["word"] == row["excluded"] for r in row["options"])
    raw = (W / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0\s*$", raw, re.MULTILINE)) == 1
    assert "OK (1 test)" in raw
    assert not re.search(r"INSTRUMENTATION_STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED|ignored|assumptionFailure", raw)
    assert v["runtimeHashesVerified"] == 8438
    assert m.sha(m.ARCHIVE) == v["archiveSha256"] == execution["archiveSha256"]
    assert m.sha(m.FIXTURE) == v["fixtureSha256"] == execution["fixtureSha256"]
    assert m.sha(W / "corrected-test.apk") == execution["testApkSha256"]
    prior = m.load(R / "docs" / "n1-sources" / "execution-681.json")["fixtureVerification"]
    for key in ["fixture", "archive"]:
        assert m.sha(Path(prior[key])) == prior[key + "Sha256"]
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    assert build_manifest(R) == m.load(R / "manifest.json")
    return v, execution, result


def archive():
    m.clean()
    v, execution, result = audit()
    assert not DEST.exists() and not EVIDENCE.exists() and not REVIEW.exists()
    DEST.mkdir()
    sources = [Path(__file__), C / "verify-batch-094-correction-686.py",
               C / "run-batch-094-correction-686.ps1", C / "post-batch-094-correction-686.ps1",
               m.FIXTURE, L / "runner-role-686.json"]
    sources += [W / name for name in ["verification.json", "execution.json", "n1-094-correction-686.json",
                                     "instrumentation.txt", "compile.txt", "adb-operations.txt",
                                     "emulator-stdout.txt", "emulator-stderr.txt"]]
    receipts = []
    for source in sources:
        compressed = source.name in {"n1-094-correction-686.json", "compile.txt", "adb-operations.txt",
                                     "emulator-stdout.txt", "emulator-stderr.txt"}
        target = DEST / (source.name + (".gz" if compressed else ""))
        assert not target.exists()
        if compressed:
            target.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(target.read_bytes()) == source.read_bytes()
        else:
            shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": m.sha(source), "archiveSha256": m.sha(target),
                         "losslessGzip": compressed})
    finding = {
        "id": "094-observed-kezuru-chijimeru", "status": "resolved", "severity": "minor",
        "facet": "word meaning quiz correctness", "file": "words/削る.md:9",
        "textualEvidence": "Original-session source/declaration confirmations685 on signed b85d7a4d, frozen JMdict1298090 sense2/1337570 sense1.",
        "runtimeEvidence": "Native686 exact corrected archive productionContentSync ONCE and128 productionWordQuizBuilder checks; both targets/directions/All+custom/16seeds.",
        "confidence": "High for this directly declared pair in tested configurations; no exhaustive other-option semantic claim.",
        "newBlindReviewCredit": False,
    }
    m.save(REVIEW, {
        "schemaVersion": 1, "execution": 686, "batch": "094", "status": STAGE,
        "contentSnapshot": m.HEAD, "contentVersion": m.VERSION, "reconciliation": [finding],
        "previousEvidence": "docs/n1-reviews/batch-094-correction-reconciliation-685.json",
        "runtimeEvidence": EVIDENCE.relative_to(R).as_posix(), "independentReviewersLaunched": 0,
        "limits": ["Narrow runtime confirmation, not new blind linguistic or rendered review.",
                   "Native682 unchanged visuals and original-session683 rendered findings inherited.",
                   "No physical phone, human handwriting, successful MLKit, latestappmain, exhaustive pool semantics, publication or whole-set acceptance."],
        "runtimeAccepted": False, "runtimePublished": False, "nextAction": NEXT,
    })
    m.save(EVIDENCE, {
        "schemaVersion": 1, "execution": 686, "batch": "094", "status": STAGE,
        "startingState": m.load(C / "progress.json")["execution686StartingState"],
        "fixtureVerification": v, "nativeExecution": execution, "receipts": receipts,
        "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "fullArchiveImportedOnce": True, "runtimeHashesVerified": 8438, "manifestFresh": True,
        "importedKanji": 1117, "importedWords": 5070, "n1Cards": 126, "problems": 0,
        "acceptedReadingParserEpoch": 1, "nativeTestsPassed": 1, "nativeTestsSkipped": 0,
        "directGuardBuilderChecks": 128, "directGuardFindingDisposition": "resolved",
        "inheritedNativeVisualEvidence": "docs/n1-sources/execution-682.json",
        "inheritedRenderedFindings": "docs/n1-sources/execution-683.json",
        "independentReviewersLaunched": 0, "runtimeChangedThisExecution": False,
        "runtimeAccepted": False, "runtimePublished": False, "publicGithubZipAcceptance": False,
        "actualNewPermissionDenials": [], "parentLockReacquiredWrittenDeletedOrUnlocked": False,
        "optionalHistoricalSessionHelpersAccessed": False, "previousFixturesUnchanged": True,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": "48765e20846e1d6769c6ddc35146f6ce58deab57",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": [
            "Focused runtime assertion evidence on qualified TESTONLYAndroid1c1b7bf4 with productionf9b59a2 unchanged, not latestappmain.",
            "Local GitZIP/all runtime bytes verified, not exact immutable publicGithubZIP acceptance.",
            "No fresh visual/font/linguistic review, phone, handwriting, MLKit or full-pool semantic certification.",
            "Combined-current-main integration, all required checks, normal signing/owner fastforward/terminalCI/publicZIP/ownerissue gates remain.",
        ],
        "nextAction": NEXT,
    })
    path = R / "docs" / "n1-sources" / "batch-094-progress.json"
    ledger = m.load(path)
    changed = ["status", "nextAction", "pendingGates"]
    ledger["preCorrectedNative686State"] = {key: ledger[key] for key in changed}
    ledger["status"], ledger["nextAction"] = STAGE, NEXT
    ledger["pendingGates"] = [
        "Fresh combined-current-main normal integration, changed substantive teaching independent re-review if required, ALL content/Python/vocabulary/baseline/link/membership/reading/font/budget/applicable Android checks.",
        "Normal signed accepted integration, owner fastforward publication, terminalgreenCI, EVERY immutable publicZIP runtimehash and unchanged budget/perfile/media/path checks, verified ownerissue.",
        "Physicalphone/generalrelease/whole-set acceptance remains outstanding; no095 until accepted publication and checkpoint.",
    ]
    ledger["correctedNativeExecution686"] = {
        "evidence": EVIDENCE.relative_to(R).as_posix(), "status": STAGE,
        "contentSnapshot": m.HEAD, "contentVersion": m.VERSION,
        "terminalPerCaseStatus": [0], "testsSkipped": 0, "fullArchiveImportedOnce": True,
        "runtimeHashesVerified": 8438, "directGuardBuilderChecks": 128,
        "finding": finding, "originalSessionTextualConfirmation": "docs/n1-reviews/batch-094-correction-reconciliation-685.json",
        "priorNative682AndRendered683Evidence": "inherited, not rerun or rebranded",
        "runtimeAccepted": False, "runtimePublished": False,
    }
    m.save(path, ledger)
    print("Native correction closure archived; runtime content unchanged; no publication.")


def finalize():
    head = m.git(R, "rev-parse", "HEAD")
    assert head != m.HEAD
    m.clean(head)
    audit()
    evidence = m.load(EVIDENCE)
    expected = {r["archive"] for r in evidence["receipts"]} | {
        EVIDENCE.relative_to(R).as_posix(), REVIEW.relative_to(R).as_posix(),
        "docs/n1-sources/batch-094-progress.json"}
    assert set(m.git(R, "diff", "--name-only", m.HEAD, head).splitlines()) == expected
    for row in evidence["receipts"]:
        assert m.sha(R / row["archive"]) == row["archiveSha256"]
    issue = m.load(C / "batch-094-correction-686-issue-final-receipt.json")
    body = (C / "batch-094-correction-686-issue-final-body.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body and head in body
    state = m.load(C / "progress.json")
    before = m.load(L / "progress-before-686.json")
    assert state["checkpoint"] == before["checkpoint"] == 685
    changes = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[key] == value for key, value in before.items() if key not in changes)
    checkpoint = {
        "schemaVersion": 1, "execution": 686, "checkpoint": 686, "batch": "094",
        "savedCommit": head, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": EVIDENCE.relative_to(R).as_posix(), "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "nativeTestsPassed": 1, "nativeTestsSkipped": 0, "terminalPerCaseStatus": [0],
        "fullArchiveImportedOnce": True, "runtimeHashesVerified": 8438, "contentVersion": m.VERSION,
        "directGuardBuilderChecks": 128, "directGuardFindingDisposition": "resolved",
        "runtimeChangedThisExecution": False, "runtimeAccepted": False, "runtimePublished": False,
        "publicGithubZipAcceptance": False, "dedicatedWorktreesClean": True,
        "ownedHelperStopped": True, "ownedQemuStopped": True, "temporaryAndroidSourceAndAssetRemoved": True,
        "parentLockReacquiredWrittenDeletedOrUnlocked": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False, "independentReviewersLaunched": 0,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    state.update(checkpoint=686, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution686StartingState"]["status"] = "signed-local-corrected-native-checkpoint-complete"
    state["execution686CoordinatorCheckpoint"] = checkpoint
    state["batch094CorrectedNativeCheckpoint"] = checkpoint
    assert all(state[key] == value for key, value in before.items() if key not in changes)
    m.persist(state)
    final = m.load(C / "progress.json")
    assert all(final[key] == value for key, value in before.items() if key not in changes)
    m.save(L / "checkpoint-686.json", checkpoint)
    print("Checkpoint686 persisted; all original historical values preserved; both worktrees clean.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
