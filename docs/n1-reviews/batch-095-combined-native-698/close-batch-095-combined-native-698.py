"""Persist exact native combined-import evidence without claiming publication."""
import gzip
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prepare698", C / "prepare-batch-095-combined-native-698.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R, A, L = m.R, m.A, m.L
V = R / "docs" / "n1-reviews" / "batch-095-combined-native-698"
E = R / "docs" / "n1-sources" / "execution-698.json"
STAGE = "exact-combined-native-import-passed-awaiting-reviewclosed-publication"
NEXT = (
    "SAME095 only: finish normal signed reviewclosed/combinedacceptance and publication. "
    "Read docs/n1-sources/execution-698.json and docs/n1-reviews/batch-095-combined-native-698/acceptance.json. "
    "Signed6a7514c1/combinedmerged5a6823c runtime3eebfff0fdad5e28/all8441hashes passed NEW exactfullcombinedarchive "
    "native698 through productionContentSync ONCE:1118kanji5071words127N1/zeroProblems/acceptedRoomversion+readingepoch1; "
    "full+Lite rawボウ/[] explicitボウ/[] and onぼう/noKun preserved; THREEdirectguards/384builderchecks/"
    "64meaningpoolchecks/TWOreciprocalpairs/FOURlinkdirections pass. Native terminalcase0/ONEcase/no skips, "
    "ownedreadonlyAPI35 emulator5580 parent23116/QEMU5148 stopped; no heap/guard changes. "
    "NEW localgitarchive dbe15eb1 is NOT old native694archive9e65d18d and NOT publicGitHubZIP acceptance. "
    "No new glyph/route evidence: inherit all32Han/fourfonts/60PNG/native694/accepted695 confirmations unchanged; "
    "originalClaude695overlap staysREJECTED with separate smallestserialrepair. Original691blind and697 originalClaude"
    "ede78c28-e889-47b5-be0b-21533da61551 THEN GPTee7498e0-d3ad-46bf-bbc9-82761892cab0 elevenincomingpassage "
    "strictserial confirmations remain inherited; zeroactionable/consequentialunresolved. No newblindcredit. "
    "Combined696 all372Python/validate/manifest/vocabularypilot2122of2431/fullsource/baseline/readings/strokes/"
    "allmappedlinks/fontprovenance/FOURAndroidRealContentTHREE+RareHanONE/no skips remain applicable, not freshly rerun698. "
    "698freshvalidate/build_manifest/budget/runtimehashes recorded. QualifiedTESTONLYAndroid1c1b7bf4 retains "
    "productionf9b59a2, NOT latestappmain. Recheck freshorigin/main (da374717 at698); if advanced, nonrewritingmerge/"
    "surgicalreconciliation/regeneratedmanifest/combinedchecks/independent substantivechangedpassage confirmation/"
    "newexactcombinedimport if manifest changed. Normal signing; yield on passphrasehang, no retries/workaround. "
    "Ownerfastforward to origin/main ONLY after ALLgates. Verify exactremoteSHA/terminalgreenCI/EVERYimmutablepublicZIP"
    "runtimeentryhash/manifest equality/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue before counting delivery or096. "
    "Parent19008 ownsrunner.lock: verifyliveancestry/session/checkpoint/exactsignedheads/whollyclean, "
    "NOchildacquire/delete/unlock. Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelpers. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. No runtimepublication/096/secondrunner698. "
    "Published121of1228/1107remaining unchanged; physicalphone/generalrelease/whole-set outstanding; "
    "no phone/humanhandwriting/MLKit/fullpool certification."
)


def stopped(pid):
    output = subprocess.check_output(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command",
         f"if(Get-Process -Id {int(pid)} -ErrorAction SilentlyContinue){{'RUNNING'}}else{{'STOPPED'}}"],
        text=True).strip()
    assert output == "STOPPED", (pid, output)


def check_native():
    result = m.load(C / "batch-095-native-attempt-698-execution.json")
    assert result["passed"] and result["nativeExecuted"] and result["failure"] is None
    assert result["terminalSuccessCases"] == 1 and result["adbExitCode"] == 0
    assert result["ownedHelperStopped"] and result["ownedQemuStopped"] and result["stopAdbExitCode"] == 0
    for pid in [result["parentEmulatorPid"], result["qemuPid"]]:
        stopped(pid)
    assert not result["guardsChanged"] and not result["guestOrAppHeapChanged"] and not result["parentLockTouched"]
    assert result["contentSnapshot"] == m.HEAD and result["androidSnapshot"] == m.APP
    folder = C / "artifacts" / "batch-095-native-attempt-698"
    text = (folder / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0\s*$", text, re.M)) == 1
    assert "OK (1 test)" in text and "INSTRUMENTATION_CODE: -1" in text
    assert not re.search(r"STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED|assumptionFailure|ignored", text)
    imported = m.load(folder / "n1-095-combined-import-698.json")
    expected = {"contentSnapshot": m.HEAD, "contentVersion": m.VERSION, "archiveRequests": 1,
                "importedKanji": 1118, "importedWords": 5071, "n1Cards": 127,
                "problems": 0, "acceptedReadingParserEpoch": 1, "passed": True,
                "reciprocalPairs": 2, "linkDirections": 4,
                "quizOnKeys": ["ぼう"], "quizKunKeys": []}
    for key, value in expected.items():
        assert imported[key] == value, key
    for key in ["fullOnyomi", "fullQuizOnyomi", "liteOnyomi", "liteQuizOnyomi"]:
        assert imported[key] == ["ボウ"]
    for key in ["fullKunyomi", "fullQuizKunyomi", "liteKunyomi", "liteQuizKunyomi"]:
        assert imported[key] == []
    guards = imported["directGuardBuilderChecks"]
    assert len(guards) == 384 and len(imported["productionBuilderChoices"]) == 64
    assert {(x["target"], x["excluded"]) for x in guards} == {
        ("解剖", word) for word in ["分析", "分解", "検査"]} | {
        (word, "解剖") for word in ["分析", "分解", "検査"]}
    assert {(x["pool"], x["direction"], x["seed"]) for x in guards} == {
        (pool, direction, seed) for pool in ["All", "boundedCustom"]
        for direction in ["JpToEn", "EnToJp"] for seed in range(16)}
    for check in guards:
        assert check["excluded"] not in [x["word"] for x in check["options"]]
    return result, imported


def archive():
    m.clean()
    m.runtime()
    result, imported = check_native()
    assert not V.exists() and not E.exists()
    checks = []
    for tool, name in [("validate.py", "validate-698.txt"), ("build_manifest.py", "manifest-698.txt"),
                       ("check_content_budget.py", "budget-698.txt")]:
        target = L / name
        assert not target.exists()
        command = ["python", "-X", "utf8", "-B", str(R / "tools" / tool)]
        with target.open("w", encoding="utf-8") as log:
            result_check = subprocess.run(command, cwd=R, stdout=log, stderr=subprocess.STDOUT)
        assert result_check.returncode == 0, target
        checks.append({"command": command, "exitCode": 0, "log": str(target), "logSha256": m.sha(target)})
    m.clean()
    m.runtime()
    V.mkdir()
    sources = [Path(__file__), C / "prepare-batch-095-combined-native-698.py",
               C / "adapt-batch-095-combined-native-698.py", C / "preflight-698.ps1",
               C / "run-698-native-compile.ps1", C / "run-698-native.ps1",
               C / "post-batch-095-combined-native-698.ps1",
               m.VERIFY, C / "batch-095-combined-native-698-compiled.json", m.FIXTURE,
               C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt",
               L / "preflight-698.json", L / "native-compile-command.json",
               L / "native-compile-start.txt", L / "native-compile-end.txt", L / "native-compile-exit.txt"]
    sources += [Path(check["log"]) for check in checks]
    folder = C / "artifacts" / "batch-095-native-attempt-698"
    sources += sorted(folder.iterdir())
    packed = {L / "native-compile.txt", L / "validate-698.txt", folder / "adb-operations.txt",
              folder / "emulator-stdout.txt", folder / "n1-095-combined-import-698.json"}
    sources += [L / "native-compile.txt"]
    receipts = []
    for source in sources:
        assert source.is_file(), source
        target = V / (source.name + ".gz" if source in packed else source.name)
        assert not target.exists(), target
        if source in packed:
            target.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(target.read_bytes()) == source.read_bytes()
        else:
            shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": m.sha(source), "archiveSha256": m.sha(target),
                         "losslessGzip": source in packed})
    acceptance = {
        "schemaVersion": 1, "batch": "095", "execution": 698, "status": STAGE,
        "contentSnapshot": m.HEAD, "combinedMerge": "d5a6823c70583ab5c64a63a863993b9577466937",
        "contentVersion": m.VERSION, "runtimeHashesVerified": 8441, "exactCombinedNativeImport": "passed",
        "terminalSuccessCases": 1, "skipped": 0,
        "imported": {key: value for key, value in imported.items()
                     if key not in {"directGuardBuilderChecks", "productionBuilderChoices"}},
        "directGuardBuilderChecks": 384, "meaningPoolBuilderChecks": 64,
        "newIndependentReviewers": 0, "newVisualOrRouteAcceptance": False,
        "inheritedContentReview": "691 blind initial; 695 accepted rendered confirmations and separate minimal serial repair; 697 eleven incoming teaching delta confirmations, all with original limits.",
        "originalClaude695Overlap": "REJECTED, immutable original; separate repair does not retroactively change it",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "publicGithubZipAcceptance": False, "phoneEvidence": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "nextAction": NEXT,
    }
    m.save(V / "acceptance.json", acceptance)
    evidence = {
        "schemaVersion": 1, "execution": 698, "batch": "095", "status": "continue", "stage": STAGE,
        "startingState": m.load(C / "progress.json")["execution698StartingState"],
        "fixtureVerification": m.load(m.VERIFY),
        "compiled": m.load(C / "batch-095-combined-native-698-compiled.json"),
        "nativeExecution": result, "acceptance": acceptance, "receipts": receipts, "freshChecks": checks,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "exactCombinedNativeImport": "passed", "publicGithubZipAcceptance": False,
        "publishedAdditions": 121, "remainingAdditions": 1107, "wholeProjectComplete": False,
        "nextBatchStarted": False,
        "inheritedChecks": "696 all372Python/4Android(no skips), frozen source/baseline/readings/strokes/links/fonts/vocabularypilot checks; not freshly executed698. 694 native and 695 rendered teaching unchanged.",
        "limits": [
            "Exact local full git archive native import is not immutable public GitHub ZIP acceptance.",
            "Qualified TESTONLY Android1c1b7bf4 keeps productionf9b59a2; not latest app main.",
            "No new glyph/route/human handwriting/MLKit/phone/full quiz-pool/general-release/whole-set certification.",
            "The 384 direct guard checks cover specified pairs/seeds/directions/pools, not all possible content quiz options.",
            "All original historical checkpoint/review limitations remain intact; no new independent review credit.",
        ],
        "diagnostics": [
            "Initial preflight conservatively rejected an expected lock syntax mismatch before any start/build/native operation. Inspected same-hash committed launcher: actual 'None' enum-string lock syntax; corrected only child textual contract check. No lock access or permission denial.",
            "Wrapper adaptation asserted seven occurrences of 694 but actual committed wrapper has five; generation stopped before native wrapper write. Corrected count, verified already generated compile wrapper byte-equivalent; no evidence or attempt overwritten.",
        ],
        "nextAction": NEXT,
    }
    m.save(E, evidence)
    packet = R / "docs" / "n1-sources" / "batch-095-progress.json"
    raw = packet.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = packet.read_text(encoding="utf-8")
    current = json.loads(text)
    changes = {"status": STAGE, "nextAction": NEXT, "pendingGates": [
        "Exact combined native import3eebfff0fdad5e28 passed698; 697 teaching confirmations and 696 combined automated checks inherited with limits.",
        "Normal signed reviewclosed/combinedacceptance; freshmain check/remerge and revalidation if needed; ownerfastforward; terminalgreenCI; EVERYimmutablepublicZIPentryhash/originalbudgets/verifiedownerissue before096.",
    ]}
    decoder = json.JSONDecoder()
    for key, value in changes.items():
        match = re.search(r'^  "' + key + r'": ', text, re.M)
        assert match
        _, end = decoder.raw_decode(text, match.end())
        text = text[:match.end()] + json.dumps(value, ensure_ascii=True, indent=2).replace("\n", "\n  ") + text[end:]
    current.update(changes)
    extra = {"combinedNativeImport698": {
        "status": STAGE, "evidence": E.relative_to(R).as_posix(),
        "acceptance": (V / "acceptance.json").relative_to(R).as_posix(),
        "contentSnapshot": m.HEAD, "contentVersion": m.VERSION,
        "exactCombinedNativeImport": "passed", "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False, "newIndependentReviewers": 0,
        "historicalLimitDisposition": "Earlier pending fields remain historical; this additive record supersedes the pending exact combined native import gate only.",
    }}
    assert not set(extra) & set(current)
    end = text.rfind("}")
    text = text[:end].rstrip() + "," + json.dumps(extra, ensure_ascii=True, indent=2)[1:-1] + text[end:]
    current.update(extra)
    assert json.loads(text) == current
    packet.write_text(text, encoding="utf-8", newline=newline)
    print("Combined native evidence archived; batch runtime remains unpublished.")


def checkpoint():
    head = m.git("rev-parse", "HEAD")
    assert m.git("rev-parse", "HEAD^") == m.HEAD and m.git("log", "-1", "--format=%G?") == "G"
    for root in [R, A]:
        assert not m.git("status", "--porcelain", "--untracked-files=all", root=root)
    m.runtime()
    check_native()
    assert m.git("rev-parse", "HEAD", root=A) == m.APP
    post = m.load(C / "batch-095-combined-native-698-issue-receipt.json")
    body = (C / "batch-095-combined-native-698-issue-body.txt").read_text(encoding="utf-8")
    assert post["user"]["login"] == "stop-cran" and post["body"] == body
    before = m.load(L / "progress-before-698.json")
    state = m.load(C / "progress.json")
    assert state["checkpoint"] == 697 and state["batch"] == "095" and state["status"] == "continue"
    allowed = {"stage", "nextAction"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    state["execution698StartingState"]["status"] = "signed-local-exact-combined-native-checkpoint-complete"
    record = {
        "schemaVersion": 1, "execution": 698, "checkpoint": 698, "batch": "095",
        "savedCommit": head, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": E.relative_to(R).as_posix(), "acceptance": (V / "acceptance.json").relative_to(R).as_posix(),
        "contentSnapshot": m.HEAD, "contentVersion": m.VERSION, "runtimeHashesVerified": 8441,
        "exactCombinedNativeImport": "passed", "importedKanji": 1118, "importedWords": 5071,
        "n1Cards": 127, "problems": 0, "acceptedReadingParserEpoch": 1,
        "terminalSuccessCases": 1, "skipped": 0, "newIndependentReviewers": 0,
        "directGuardBuilderChecks": 384, "meaningPoolBuilderChecks": 64,
        "reciprocalPairs": 2, "linkDirections": 4, "ownedEmulatorStopped": True,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "publicGithubZipAcceptance": False, "publishedAdditions": 121, "remainingAdditions": 1107,
        "lastPublishedCommit": before["lastPublishedCommit"], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False, "issueUpdate": post["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    state.update(checkpoint=698, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution698CoordinatorCheckpoint"] = record
    state["batch095CombinedNativeImportCheckpoint"] = record.copy()
    temp = C / "progress.698.tmp"
    assert not temp.exists()
    m.save(temp, state)
    assert m.load(temp) == state
    temp.replace(C / "progress.json")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    {"archive": archive, "checkpoint": checkpoint}[sys.argv[1]]()
