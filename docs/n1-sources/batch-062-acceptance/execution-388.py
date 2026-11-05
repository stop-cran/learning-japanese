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
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
D = S / "batch-062-acceptance"
START = "274273a345f4a986d3eea0422c6b006dd6cab092"
BASE = "42f144c76f013bedc392b201c5be7eed35083b88"
TEACHING = "38ab6072d2041325142c54cf54be5d126928eb31"
VERSION = "545c56b5d4b4e8ef"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution388.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", *args],
        cwd=tree, text=True, encoding="utf-8").strip()


def unchanged():
    assert git("branch", "--show-current") == "content/n1-kanji"
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    app = C.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", tree=app)
    subprocess.run(["git", "merge-base", "--is-ancestor", git("rev-parse", "origin/main"), "HEAD"],
                   cwd=R, check=True)


LIMITS = (
    "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
    "Historical Claude062-P1 one overlapping start/two-view response and062-P2 one145-line guidance read/report "
    "discrepancy remain explicit, NOT retroactive strict acceptance. Two supervised original-Claude lexical "
    "confirmations remediate the bounded current gate; both actual initial model families and compliant dependent "
    "visual turns retain all three scoped articles/three facets CLEAN with no actionable teaching finding. "
    "Five original optionals not adopted.42 frozen families mechanically re-extracted, not newly linguistically "
    "reviewed. Visual Claude28/GPT27serial views,17distinct source images each,34actual900x2000payloads separately "
    "retained from37source1080x2400PNGs. Unseen viewports/horizontally cropped cells and actual fallbackface UNVERIFIED. "
    "Fourproductionfontrows俸棒奉借付人亻木給糸合/俸給 readable/distinct on testedAPI35. "
    "Accepted384Android3+1/noskips and386native2terminal0/96.065s reverified, not rerun: "
    "productionContentSyncONCE1074kanji5032words94N1/545c56b5d4b4e8ef/problems0/epoch1/Full+Liteホウ/emptykun/"
    "curatedほう/no-kun/twopairs-fourdirections/SystemBack/offline/meaningBackBEFORENextnotnewpersistedgrade/"
    "solecuratedOnGood/tenreference-touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain. "
    "NOTMLKit/correcthumanrecall/phone. Synthetic source/queues/logs are not ownerprogress. "
    "Source/publiclookup truncation/attribution-only headings/gaiji limits retained. Original383permissiondenial "
    "and parent exact recovery,049HOST512MiBOOM and same qualified host-only1GiB init remain historical; "
    "no guest/appheap/font/archiveguard increase. Fresh main42f144c7 already ancestral; no new runtime/teaching "
    "merge delta requiring duplicateAndroid/native/review."
)


def start():
    request = C / "logs" / "77866fa0-8774-4e47-8f94-c471745f9364" / "request.txt"
    raw = request.read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    embedded = json.loads(text.split(marker, 1)[1])
    p = load(C / "progress.json")
    assert embedded["checkpoint"] == p["checkpoint"] == 387 and p["batch"] == "062"
    assert git("rev-parse", "HEAD") == START and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and git("rev-parse", "origin/main") == BASE
    unchanged()
    assert not (C / "execution-388-starting-progress.json").exists()
    save(C / "execution-388-starting-progress.json", p)
    record = {
        "execution": 388, "batch": "062", "startingHead": START,
        "scope": "SAME062 combined-main acceptance and bounded owner-testing publication; no063, duplicate accepted Android/native/review run or second runner absent a new concern.",
        "status": "starting-combined-main-acceptance",
        "recordedAt": datetime.now().astimezone().isoformat(),
        "authorization": {
            "requestSha256": hashlib.sha256(raw).hexdigest(),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final387 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
        },
        "integratedMain": BASE,
        "mergeResult": "Fresh fetch; normal non-rewriting merge already up to date. No new runtime or teaching delta.",
    }
    p["execution388StartingState"] = copy.deepcopy(record)
    p["activeExecution"] = record
    p["stage"] = "batch-062-combined-main-acceptance"
    save(C / "progress.json", p)
    print("Starting bounded publication scope persisted; complete live history retained.")


def source_audit():
    source = C / "execution-380.py"
    text = source.read_text(encoding="utf-8")
    replacements = {
        'assert ledger["reviewClosed"] == ledger["published"] == []':
            'assert ledger["reviewClosed"] == ["俸"] and ledger["published"] == []',
        'assert ledger["status"] == "local-unreviewed-draft"':
            'assert ledger["status"] == "batch-062-bounded-native-visual-reconciled-pending-combined-main-publication"',
        'save(FOLDER / "batch-062-draft-audit.json", result)':
            'save(FOLDER / "batch-062-acceptance-source-audit.json", result)',
    }
    for before, after in replacements.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    scope = {"__file__": str(source), "__name__": "combined_acceptance"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(text, str(source), "exec"), scope)
        scope["audit"]()
    path = S / "batch-062-acceptance-source-audit.json"
    result = load(path)
    result.update(
        execution=388, status="combined-source-audit-pending-evidence-reverification",
        freshLinguisticReviewOfAllFamiliesClaimed=False,
        coordinatorInspection="Fresh mechanical re-extraction of42frozen families; original linguistic inspection/reconciliation retained, not newly performed.",
        auditReuse="Unchanged execution380 audit with only draft review-state preconditions replaced and separately named output. Actual HEAD, ancestry, frozen teaching equality and accepted review state verified independently.",
    )
    save(path, result)
    print("Combined source/baseline/readings/two-pair/stroke/font/budget audit passed.")


def validate():
    receipts = []
    for name, arguments in (
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("source-audit", [str(Path(__file__)), "source-audit"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = C / "logs" / f"execution-388-{name}.txt"
        assert not path.exists(), path
        with path.open("wb") as stream:
            process = subprocess.run([sys.executable, "-X", "utf8", "-B", *arguments],
                                     cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({"check": name, "command": ["python", "-X", "utf8", "-B", *arguments],
                         "exitCode": process.returncode, "log": str(path), "sha256": sha(path)})
        print(json.dumps(receipts[-1]), flush=True)
        if process.returncode:
            print(path.read_text(encoding="utf-8")[-6000:])
            raise SystemExit(process.returncode)
    save(C / "artifacts" / "execution-388-validation-receipts.json", receipts)


def evidence():
    path = C / "close-execution-387.py"
    scope = {"__file__": str(path), "__name__": "evidence_audit_only"}
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), scope)
    freeze, visual_processes = scope["audit"]()
    record = load(S / "execution-387.json")
    assert sha(V / "batch-062-native-acceptance.json") == record["acceptanceSha256"]
    for row in record["archivedExecutionArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    visual = load(V / "batch-062-native-acceptance.json")
    assert visual["nativeAssertionsPassed"] and visual["independentVisualAcceptance"]
    assert visual["boundedNativeAcceptance"] and not visual["findings"]
    assert not visual["strictHistoricalProcessContractAccepted"]
    reconciliation = load(V / "batch-062-reconciliation.json")
    assert reconciliation["textualReviewClosed"] and not reconciliation["findings"]
    assert not reconciliation["strictInitialProcessContractAccepted"]
    assert sha(V / reconciliation["originalInitialReview"]) == reconciliation["originalInitialReviewSha256"]
    initial = load(V / reconciliation["originalInitialReview"])["reviewProcesses"]
    assert [row["model"] for row in initial] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert all(row["exitCode"] == 0 and row["snapshot"] == TEACHING for row in initial)
    assert datetime.fromisoformat(initial[0]["completedAt"]) < datetime.fromisoformat(initial[1]["startedAt"])
    assert [len(row["observedInternalOverlaps"]) for row in initial] == [1, 0]
    for family, row in zip(("claude", "gpt"), initial):
        prefix = f"batch-062-initial-{family}"
        assert sha(V / (prefix + ".md")) == row["reportSha256"]
        assert sha(V / (prefix + "-execution.json")) == row["executionRecordSha256"]
        assert sha(C / (prefix + ".jsonl")) == row["rawExecutionSha256"]
    dependent = reconciliation["dependentTurns"]
    for row in dependent:
        prefix = f"batch-062-dependent-claude-turn-{row['turn']}"
        assert row["exitCode"] == 0 and row["actualModels"] == ["claude-opus-5.5"]
        assert row["sessionId"] == initial[0]["sessionId"] and row["supervisedTurnAccepted"]
        assert not row["internalOverlaps"] and not row["multiToolResponses"] and not row["oversizedReads"]
        assert len(row["toolCalls"]) == 1 and row["toolCalls"][0]["exactRequestedTextContainedInResult"]
        assert sha(V / (prefix + ".md")) == row["reportSha256"]
        assert sha(C / (prefix + ".jsonl")) == row["rawExecutionSha256"]
    assert datetime.fromisoformat(dependent[0]["completedAt"]) < datetime.fromisoformat(dependent[1]["startedAt"])
    android = load(S / "execution-384.json")
    for row in android["provenance"]:
        assert sha(Path(row["path"])) == row["sha256"]
    for row in android["archivedArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    for row in android["recovery"]["tests"]:
        assert sha(Path(row["sourcePath"])) == sha(Path(row["artifactPath"])) == row["sha256"]
        xml = ET.parse(row["artifactPath"]).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(int(xml.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
        assert Path(row["fixtureRoot"]) == R
    native_index = load(V / "batch-062-native" / "execution-386-artifact-index.json")
    for row in native_index["files"]:
        assert sha(R / row["path"]) == row["sha256"], row["path"]
    native = load(S / "execution-386.json")
    assert native["failedCases"] == native["skippedCases"] == 0
    assert len(native["terminalCases"]) == 2 and all(r["status"] == 0 for r in native["terminalCases"])
    assert native["productionImportEvidence"]["contentVersion"] == VERSION
    assert sha(R / native["nativeRawLog"]) == native["rawLogSha256"]
    return {
        "initialModels": [r["model"] for r in initial], "initialToolCalls": [r["toolCalls"] for r in initial],
        "initialHistoricalOverlaps": [len(r["observedInternalOverlaps"]) for r in initial],
        "dependentLexicalToolCalls": [len(r["toolCalls"]) for r in dependent],
        "visualToolCalls": [len(r["toolCalls"]) for r in visual_processes],
        "nativeArtifactsReverified": len(native_index["files"]),
        "visualFrozenNativeArtifactsReverified": len(freeze["nativeFiles"]),
        "acceptedAndroidCases": 4, "acceptedNativeTerminalCodes": [0, 0],
        "acceptedAndroidNativeTestsRerun": False,
    }


def accept():
    unchanged()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 387 and p["batch"] == "062" and git("rev-parse", "HEAD") == START
    audits = evidence()
    original_chars = {Path(n).stem for n in load(S / "baseline-inventory.json")["files"] if n.startswith("kanji/")}
    current_chars = {path.stem for path in (R / "kanji").glob("*.md")}
    expected = set(p["publicationCheckpoint"]["pilotMembership"])
    for path in sorted(S.glob("batch-*-progress.json")):
        ledger = load(path)
        if int(ledger["batch"]) <= 62:
            members = set(ledger["membership"])
            assert not expected & members and ledger["reviewClosed"] == ledger["membership"]
            if int(ledger["batch"]) <= 61:
                assert ledger["published"] == ledger["membership"]
            expected.update(members)
    assert current_chars - original_chars == expected and len(expected) == 89 and original_chars <= current_chars
    receipts = load(C / "artifacts" / "execution-388-validation-receipts.json")
    assert all(row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"] for row in receipts)
    tests = (C / "logs" / "execution-388-python-tests.txt").read_text(encoding="utf-8")
    match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
    assert match
    audit = load(S / "batch-062-acceptance-source-audit.json")
    audit.update(
        status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=START,
        latestMainIntegrated=BASE, normalMergeResult="Fresh fetch and normal merge already up to date; no conflicts or changed teaching.",
        exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": int(match[1]), "failures": 0, "errors": 0},
        validationReceipts=receipts,
        budget=ast.literal_eval((C / "logs" / "execution-388-budget.txt").read_text()),
        reviewedBatchTeachingUnchanged=True, strictHistoricalProcessContractAccepted=False,
        strictInitialProcessContractAccepted=False, prospectiveSupervisedRemediationAccepted=True,
        **audits, limits=LIMITS,
    )
    save(S / "batch-062-acceptance-audit.json", audit)
    save(S / "execution-388.json", {
        "schemaVersion": 1, "execution": 388, "batch": "062", "status": audit["status"],
        "startingHead": START, "integratedMain": BASE, "recordedAt": datetime.now().astimezone().isoformat(),
        "acceptance": "batch-062-acceptance-audit.json", "publishedAdditions": 88,
        "remainingAdditions": 1140, "limits": LIMITS,
        "nextAction": "Normal signing/ownerfastforward/greenCI/every immutable public ZIP runtimehash/terminal receipts/ownerissue60 before062 delivery or063.",
    })
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "execution-380.py", C / "close-execution-387.py"):
        shutil.copyfile(path, D / path.name)
    p["activeExecution"].update(status="combined-tree-locally-accepted-pending-normal-signing",
                               pythonTests=int(match[1]), limits=LIMITS)
    p["stage"] = "batch-062-combined-accepted-pending-normal-signing"
    save(C / "progress.json", p)
    print(f"Combined acceptance: {match[1]} Python tests,8314hashes,89exact additions,Android4/native2 reverified; no063.")


if __name__ == "__main__":
    {"start": start, "source-audit": source_audit, "validate": validate, "accept": accept}[sys.argv[1]]()
