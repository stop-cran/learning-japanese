import ast
import contextlib
import copy
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-061-acceptance"
START = "9b80ce1e"
BASE = "af7bae60d24ee20fe6eea1c31100eca5f09459df"
TEACHING = "2567f5e7b3888f2df3ed560f618341266b471902"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution378.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", *args],
        cwd=tree, text=True, encoding="utf-8").strip()


def unchanged():
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    app = C.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", tree=app)
    subprocess.run(["git", "merge-base", "--is-ancestor", git("rev-parse", "origin/main"), "HEAD"],
                   cwd=R, check=True)


def start():
    request = C / "logs" / "dedac0e9-132e-4c2c-a135-4980b9bdeb0d" / "request.txt"
    raw = request.read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    embedded = json.loads(text.split(marker, 1)[1])
    p = load(C / "progress.json")
    assert embedded["checkpoint"] == p["checkpoint"] == 377 and p["batch"] == "061"
    assert git("rev-parse", "HEAD").startswith(START) and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == BASE
    unchanged()
    assert not (C / "execution-378-starting-progress.json").exists()
    save(C / "execution-378-starting-progress.json", p)
    record = {
        "execution": 378, "batch": "061", "startingHead": git("rev-parse", "HEAD"),
        "scope": "SAME061 combined-main acceptance and bounded owner-testing publication; no062, duplicate accepted Android/native/review run or second runner absent a new concern.",
        "status": "starting-combined-main-acceptance",
        "recordedAt": datetime.now().astimezone().isoformat(),
        "authorization": {
            "requestSha256": hashlib.sha256(raw).hexdigest(),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final377 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
        },
        "integratedMain": BASE,
        "mergeResult": "Fresh fetch; normal non-rewriting merge already up to date. No new runtime or teaching delta.",
    }
    p["execution378StartingState"] = copy.deepcopy(record)
    p["activeExecution"] = record
    p["stage"] = "batch-061-combined-main-acceptance"
    save(C / "progress.json", p)
    print(json.dumps(record, indent=2))


def source_audit():
    source = C / "execution-370.py"
    text = source.read_text(encoding="utf-8")
    replacements = {
        'assert ledger["reviewClosed"] == ledger["published"] == []':
            'assert ledger["reviewClosed"] == ["俳"] and ledger["published"] == []',
        '    assert git("rev-parse", "HEAD") == BASE\n    row = next':
            '    row = next',
        'save(FOLDER / "batch-061-draft-audit.json", result)':
            'save(FOLDER / "batch-061-acceptance-source-audit.json", result)',
    }
    for before, after in replacements.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    scope = {"__file__": str(source), "__name__": "combined_acceptance"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(text, str(source), "exec"), scope)
        scope["audit"]()
    path = S / "batch-061-acceptance-source-audit.json"
    result = load(path)
    result.update(
        execution=378, status="combined-source-audit-pending-evidence-reverification",
        freshLinguisticReviewOfAllFamiliesClaimed=False,
        coordinatorInspection="Fresh mechanical re-extraction of45frozen families; original linguistic inspection/reconciliation retained, not newly performed.",
        auditReuse="Unchanged execution370 audit with only draft HEAD/review-state preconditions replaced and a separately named acceptance output. Actual HEAD, ancestry, frozen teaching equality and accepted review state verified independently.",
    )
    save(path, result)
    print("Combined source/baseline/readings/three-pair/stroke/font/budget audit passed.")


def validate():
    commands = [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]
    receipts = []
    for name, arguments in commands:
        path = C / "logs" / f"execution-378-{name}.txt"
        assert not path.exists(), path
        with path.open("wb") as stream:
            process = subprocess.run([sys.executable, "-X", "utf8", "-B", *arguments],
                                     cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({
            "check": name, "command": ["python", "-X", "utf8", "-B", *arguments],
            "exitCode": process.returncode, "log": str(path), "sha256": sha(path),
        })
        print(json.dumps(receipts[-1]), flush=True)
        if process.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(process.returncode)
    save(C / "artifacts" / "execution-378-validation-receipts.json", receipts)


LIMITS = (
    "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
    "Historical Claude061-P1/P2 initial overlaps/151-line reads and061-P3 paired visual response/one overlap remain "
    "explicit, NOT retroactive strict acceptance. Four supervised original-Claude lexical turns and two single-image "
    "visual confirmations prospectively remediate bounded resources; both actual model families retain all four "
    "scoped articles/three facets CLEAN with no actionable teaching finding. Four original optionals and paragraph "
    "wrapping not adopted.45frozen families mechanically re-extracted, not newly linguistically reviewed. "
    "Visual Claude31/GPT30calls plus two single-image turns:20distinct source PNGs,40source copies,42actual "
    "900x2000modelpayloads separately retained from1080x2400sources. Unseen cells/pixels and fallbackface unknown; "
    "fourproductionfontrows俳非悲借優 and人亻昔心句憂/俳句/俳優 readable/distinct/no blankboxes on tested emulator. "
    "Accepted374Android3+1/noskips and376native2terminal0/108.92s reverified, not rerun: "
    "fullContentSyncONCE1073kanji5031words93N1/d01d660cc41262fe/problems0/epoch1/Full+Liteハイ/emptykun/"
    "curatedはい/no-kun/threepairs-sixdirections/SystemBack/offline/meaningBackwithoutNext/solecuratedOnGood/"
    "tenreference-touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain. NOTMLKit/correcthumanrecall/phone. "
    "Synthetic source/queues/logs are not ownerprogress. Original373permissiondenial and parent exact recovery, "
    "049HOST512MiBOOM and same qualified host-only1GiB init unchanged; no guest/app heap/font/archiveguard increase. "
    "Latestmainaf7bae60 already ancestral; no new runtime/teaching merge delta requiring duplicateAndroid/native/review."
)


def accept():
    unchanged()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 377 and p["batch"] == "061"
    assert git("rev-parse", "HEAD").startswith(START)
    evidence_path = C / "close-execution-377.py"
    evidence_tree = ast.parse(evidence_path.read_text(encoding="utf-8"))
    assert isinstance(evidence_tree.body[-1], ast.Expr)
    assert ast.unparse(evidence_tree.body[-1]) == "main()"
    evidence_tree.body.pop()
    evidence_scope = {"__file__": str(evidence_path), "__name__": "evidence_audit_only"}
    exec(compile(evidence_tree, str(evidence_path), "exec"), evidence_scope)
    index, processes = evidence_scope["audit"]()
    visual = load(V / "batch-061-native-acceptance.json")
    assert visual["nativeAssertionsPassed"] and visual["boundedIndependentVisualAcceptance"]
    assert not visual["findings"] and not visual["newActionableDefects"]
    assert not visual["strictHistoricalProcessContractAccepted"]
    assert visual["prospectiveSupervisedRemediationAccepted"]
    assert not visual["strictFirstVisualProcessContractAccepted"]
    reconciliation = load(V / "batch-061-reconciliation.json")
    assert reconciliation["textualReviewClosed"] and not reconciliation["findings"]
    assert not reconciliation["strictInitialProcessContractAccepted"]
    assert reconciliation["strictDependentProcessContractAccepted"]
    original = load(V / reconciliation["initialReviewRecord"])
    initials = original["reviewProcesses"]
    assert [row["model"] for row in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert all(row["snapshot"] == TEACHING and row["exitCode"] == 0 for row in initials)
    assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
    assert [len(row["observedInternalOverlaps"]) for row in initials] == [2, 0]
    dependent = []
    for name, report in zip(reconciliation["dependentExecutionRecords"], reconciliation["dependentReports"]):
        row = load(V / name)
        assert row["exitCode"] == 0 and row["sessionId"] == initials[0]["sessionId"]
        assert row["actualModels"] == ["claude-opus-5.5"]
        assert sha(V / report) == row["reportSha256"]
        assert len(row["toolCalls"]) == 1 and not row["internalOverlaps"] and not row["multiToolResponses"]
        assert not row["oversizedReads"] and row["supervisedTurnAccepted"]
        assert sha(C / (report.removesuffix(".md") + ".jsonl")) == row["rawExecutionSha256"]
        for call in row["toolCalls"]:
            assert call["success"] and call["exactRequestedTextContainedInResult"]
        dependent.append(row)
    for first, following in zip(dependent, dependent[1:]):
        assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(following["startedAt"])
    record377 = load(S / "execution-377.json")
    assert sha(V / "batch-061-native-acceptance.json") == record377["acceptanceSha256"]
    for row in record377["archivedExecutionReceipts"]:
        assert sha(R / row["path"]) == row["sha256"]
    for reviewer in visual["reviewers"]:
        assert sha(V / reviewer["report"]) == reviewer["reportSha256"]
        assert sha(V / reviewer["execution"]) == reviewer["executionSha256"]
    assert sha(V / visual["textualReconciliation"]) == visual["textualReconciliationSha256"]
    assert sha(R / "docs" / visual["nativeEvidence"]) == visual["nativeEvidenceSha256"]
    native = load(S / "execution-376.json")
    assert native["directedReciprocalTransitions"] == 6 and len(native["reciprocalPairs"]) == 3
    assert sha(R / native["nativeRawLog"]) == native["rawLogSha256"]
    baseline = load(S / "baseline-inventory.json")["files"]
    original_chars = {Path(n).stem for n in baseline if n.startswith("kanji/")}
    current_chars = {path.stem for path in (R / "kanji").glob("*.md")}
    expected = set(p["publicationCheckpoint"]["pilotMembership"])
    for path in sorted(S.glob("batch-*-progress.json")):
        ledger = load(path)
        if int(ledger["batch"]) <= 61:
            members = set(ledger["membership"])
            assert not expected & members and ledger["reviewClosed"] == ledger["membership"]
            if int(ledger["batch"]) <= 60:
                assert ledger["published"] == ledger["membership"]
            expected.update(members)
    assert current_chars - original_chars == expected and len(expected) == 88 and original_chars <= current_chars
    receipts = load(C / "artifacts" / "execution-378-validation-receipts.json")
    for row in receipts:
        assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
    tests = (C / "logs" / "execution-378-python-tests.txt").read_text(encoding="utf-8")
    match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
    assert match
    audit = load(S / "batch-061-acceptance-source-audit.json")
    audit.update(
        status="combined-tree-locally-accepted-pending-publication",
        integratedHeadBeforeAcceptance=git("rev-parse", "HEAD"), latestMainIntegrated=BASE,
        normalMergeResult="Fresh fetch and normal merge already up to date; no conflicts or changed teaching.",
        exactLocalAdditionMembership=sorted(expected),
        pythonTests={"passed": int(match[1]), "failures": 0, "errors": 0},
        validationReceipts=receipts,
        budget=ast.literal_eval((C / "logs" / "execution-378-budget.txt").read_text()),
        acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
        indexedNativeArtifactsReverified=len(index["files"]),
        initialToolCalls=[row["toolCalls"] for row in initials],
        initialOverlaps=[len(row["observedInternalOverlaps"]) for row in initials],
        dependentToolCalls=[len(row["toolCalls"]) for row in dependent],
        visualToolCalls=[len(row["toolCalls"]) for row in processes],
        acceptedAndroidNativeTestsRerun=False, reviewedBatchTeachingUnchanged=True,
        strictHistoricalProcessContractAccepted=False,
        strictInitialProcessContractAccepted=False, strictDependentProcessContractAccepted=True,
        strictFirstVisualProcessContractAccepted=False, prospectiveSupervisedVisualRemediationAccepted=True,
        limits=LIMITS,
    )
    save(S / "batch-061-acceptance-audit.json", audit)
    save(S / "execution-378.json", {
        "schemaVersion": 1, "execution": 378, "batch": "061",
        "status": audit["status"], "startingHead": git("rev-parse", "HEAD"), "integratedMain": BASE,
        "recordedAt": datetime.now().astimezone().isoformat(),
        "acceptance": "batch-061-acceptance-audit.json",
        "publishedAdditions": 87, "remainingAdditions": 1141, "limits": LIMITS,
        "nextAction": "Normal signing/ownerfastforward/greenCI/every immutable public ZIP runtimehash/terminal receipts/ownerissue60 before061 delivery or062.",
    })
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "execution-370.py", C / "close-execution-377.py"):
        shutil.copyfile(path, D / path.name)
    p["activeExecution"].update(status="combined-tree-locally-accepted-pending-normal-signing",
                               pythonTests=int(match[1]), limits=LIMITS)
    p["stage"] = "batch-061-combined-accepted-pending-normal-signing"
    save(C / "progress.json", p)
    print(f"Combined acceptance: {match[1]} Python tests,8311hashes,88exact additions,Android4/native2 reverified; no062.")


if __name__ == "__main__":
    {"start": start, "source-audit": source_audit, "validate": validate, "accept": accept}[sys.argv[1]]()
