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
D = S / "batch-063-acceptance"
START = "fe10b23680d2ef99e76488be1ae17beb8a47964c"
BASE = "54fd8ff471eec7c98a83860ae94b92a673cf05bd"
TEACHING = "ddad655f71c06e7cb2c749de18596863a800a73d"
VERSION = "c19b742b7e6320a7"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, data):
    temporary = p.with_suffix(p.suffix + ".execution398.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(p)


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


def start():
    request = C / "logs" / "257e9611-f471-4966-9761-460a65c899d7" / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    embedded = json.loads(text.split(marker, 1)[1])
    p = load(C / "progress.json")
    assert embedded["checkpoint"] == p["checkpoint"] == 397 and p["batch"] == "063"
    assert git("rev-parse", "HEAD") == START and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and git("rev-parse", "origin/main") == BASE
    unchanged()
    assert not (C / "execution-398-starting-progress.json").exists()
    save(C / "execution-398-starting-progress.json", p)
    record = {
        "execution": 398, "batch": "063", "startingHead": START,
        "scope": "SAME063 combined-main acceptance and bounded owner-testing publication; no064, duplicate accepted Android/native/review run or second runner absent a new concern.",
        "status": "starting-combined-main-acceptance",
        "recordedAt": datetime.now().astimezone().isoformat(),
        "authorization": {
            "requestSha256": sha(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete final397 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
        },
        "integratedMain": BASE,
        "mergeResult": "Fresh fetch and normal non-rewriting merge already up to date; no new runtime or teaching delta.",
    }
    p["execution398StartingState"] = copy.deepcopy(record)
    p["activeExecution"] = record
    p["stage"] = "batch-063-combined-main-acceptance"
    save(C / "progress.json", p)
    print("Starting bounded acceptance/publication scope persisted; full live history retained.")


def source_audit():
    path = C / "execution-390.py"
    text = path.read_text(encoding="utf-8")
    replacements = {
        'assert ledger["status"] == "local-unreviewed-draft"':
            'assert ledger["status"] == "bounded-native-visual-accepted-awaiting-integration"',
        'assert ledger["reviewClosed"] == ledger["published"] == []':
            'assert ledger["reviewClosed"] == ["倣"] and ledger["published"] == []',
        'save(FOLDER / "batch-063-draft-audit.json", result)':
            'save(FOLDER / "batch-063-acceptance-source-audit.json", result)',
    }
    for before, after in replacements.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    scope = {"__file__": str(path), "__name__": "combined_acceptance"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(text, str(path), "exec"), scope)
        scope["audit"]()
    target = S / "batch-063-acceptance-source-audit.json"
    result = load(target)
    result.update(
        execution=398, status="combined-source-audit-pending-evidence-reverification",
        freshLinguisticReviewOfAllFamiliesClaimed=False,
        coordinatorInspection="Fresh mechanical re-extraction of35frozen families; original linguistic inspection/reconciliation retained, not newly performed.",
        auditReuse="Unchanged execution390 audit with only draft review-state preconditions replaced and separately named output; frozen teaching equality and accepted review state verified independently.",
    )
    save(target, result)
    print("Combined frozen-source/baseline/readings/two-pair/stroke/font/budget audit passed.")


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
        path = C / "logs" / f"execution-398-{name}.txt"
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
    save(C / "artifacts" / "execution-398-validation-receipts.json", receipts)


def evidence():
    reconciled = load(V / "batch-063-reconciliation.json")
    assert reconciled["textualReviewClosed"] and reconciled["reviewClosed"] and not reconciled["findings"]
    assert not reconciled["strictInitialProcessContractAccepted"]
    assert sha(V / reconciled["originalInitialReview"]) == reconciled["originalInitialReviewSha256"]
    initial_record = load(V / reconciled["originalInitialReview"])
    assert initial_record["reviewedTeachingSnapshot"] == TEACHING
    initial = initial_record["reviewProcesses"]
    assert [r["model"] for r in initial] == ["claude-opus-5.5", "gpt-6.1-sol"]
    assert all(r["exitCode"] == 0 for r in initial)
    assert datetime.fromisoformat(initial[0]["completedAt"]) < datetime.fromisoformat(initial[1]["startedAt"])
    for family, row in zip(("claude", "gpt"), initial):
        prefix = f"batch-063-initial-{family}"
        assert sha(V / (prefix + ".md")) == row["reportSha256"]
        assert sha(V / (prefix + "-execution.json")) == row["executionRecordSha256"]
        assert sha(C / (prefix + ".jsonl")) == row["rawExecutionSha256"]
    for row in reconciled["dependentTurns"]:
        prefix = f"batch-063-dependent-claude-turn{reconciled['dependentTurns'].index(row) + 1}"
        assert row["exitCode"] == 0 and row["actualModels"] == ["claude-opus-5.5"]
        assert row["sessionId"] == initial[0]["sessionId"]
        assert not row["observedToolOverlaps"] and not row["multiToolResponses"] and not row["unfinishedTools"]
        assert sha(V / (prefix + ".md")) == row["reportSha256"]
        assert sha(C / (prefix + ".jsonl")) == row["rawExecutionSha256"]
        assert all(c["name"] == "view" and c["success"] and c["exactRequestedTextContainedInResult"]
                   and not c["truncationOrLimitMarker"] for c in row["toolCalls"])
    native = load(V / "batch-063-native-acceptance.json")
    assert native["nativeAcceptance"] and native["independentVisualAcceptance"] and not native["findings"]
    assert not native["strictInitialProcessContractAccepted"]
    visual = []
    for summary in native["reviewRecords"]:
        row = load(V / summary["executionRecord"])
        family = summary["family"]
        assert row["exitCode"] == 0 and row["actualModels"] == [summary["model"]]
        assert row["sessionId"] == initial[0 if family == "claude" else 1]["sessionId"]
        assert row["availableTools"] == ["view"] and not row["observedToolOverlaps"]
        assert not row["multiToolResponses"] and not row["unfinishedTools"]
        assert sha(V / summary["report"]) == summary["reportSha256"] == row["reportSha256"]
        assert sha(C / f"batch-063-visual-{family}.jsonl") == row["rawExecutionSha256"]
        assert all(c["name"] == "view" and c["success"] and not c["truncationOrLimitMarker"]
                   for c in row["toolCalls"])
        visual.append(row)
    assert datetime.fromisoformat(visual[0]["completedAt"]) < datetime.fromisoformat(visual[1]["startedAt"])
    index = load(V / "batch-063-native" / "execution-396-artifact-index.json")
    for row in index["files"]:
        assert sha(R / row["path"]) == row["sha256"], row["path"]
    execution = load(S / "execution-396.json")
    assert execution["failedCases"] == execution["skippedCases"] == 0
    assert len(execution["terminalCases"]) == 2 and all(r["status"] == 0 for r in execution["terminalCases"])
    raw = V / "batch-063-native" / "attempt-1" / "instrumentation.txt"
    log = raw.read_text(encoding="utf-8")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", log, re.M) == ["1", "0", "1", "0"]
    assert "Time: 114.805" in log and "OK (2 tests)" in log
    route = load(V / "batch-063-native" / "attempt-1" / "n1-063-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1 and not route["phoneEvidence"]
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1075, 5033, 95, 0, 1]
    assert route["contentVersion"] == VERSION
    assert route["fullOnyomi"] == ["ホウ"] and route["fullKunyomi"] == ["なら.う"]
    assert route["quizOnKeys"] == ["ほう"] and route["quizKunKeys"] == ["ならう"]
    android = load(S / "execution-394.json")
    for row in android["provenance"]:
        assert sha(Path(row["path"])) == row["sha256"]
    for row in android["archivedArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    for row in android["recovery"]["tests"]:
        assert sha(Path(row["artifactPath"])) == row["sha256"]
        xml = ET.parse(row["artifactPath"]).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(int(xml.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
        assert sorted(c.attrib["name"] for c in xml.findall("testcase")) == sorted(row["caseNames"])
        assert Path(row["fixtureRoot"]) == R
    return {
        "initialModels": [r["model"] for r in initial],
        "initialHistoricalOverlaps": [len(r["observedInternalOverlaps"]) for r in initial],
        "nativeArtifactsReverified": len(index["files"]),
        "visualToolCalls": [len(r["toolCalls"]) for r in visual],
        "acceptedAndroidCases": 4, "acceptedNativeTerminalCodes": [0, 0],
        "acceptedAndroidNativeTestsRerun": False,
    }


def accept():
    unchanged()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 397 and p["batch"] == "063" and git("rev-parse", "HEAD") == START
    checks = evidence()
    original = {Path(n).stem for n in load(S / "baseline-inventory.json")["files"] if n.startswith("kanji/")}
    current = {path.stem for path in (R / "kanji").glob("*.md")}
    expected = set(p["publicationCheckpoint"]["pilotMembership"])
    for path in sorted(S.glob("batch-*-progress.json")):
        ledger = load(path)
        if int(ledger["batch"]) <= 63:
            members = set(ledger["membership"])
            assert not expected & members and ledger["reviewClosed"] == ledger["membership"]
            if int(ledger["batch"]) <= 62:
                assert ledger["published"] == ledger["membership"]
            expected.update(members)
    assert current - original == expected and len(expected) == 90 and original <= current
    receipts = load(C / "artifacts" / "execution-398-validation-receipts.json")
    assert all(r["exitCode"] == 0 and sha(Path(r["log"])) == r["sha256"] for r in receipts)
    tests = (C / "logs" / "execution-398-python-tests.txt").read_text(encoding="utf-8")
    match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
    assert match
    audit = load(S / "batch-063-acceptance-source-audit.json")
    limits = (
        "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
        "Historical Claude063-P1 one overlapping two-view response remains noncompliant, NOT retroactive strict initial acceptance. "
        "Two serial dependent original-Claude lexical confirmations remediate bounded current gate; both actual initial model families "
        "and dependent visuals retain three scoped articles/three facets CLEAN without actionable teaching finding. "
        "35 frozen families mechanically re-extracted, not newly linguistically reviewed. Each visual reviewer25PNGnames/"
        "20distinct source hashes, not25independent scenes; returned900x2000 from1080x2400. Complete reading rows visible in "
        "kanji-meaning; shifted on-reading clips leftlabels. Four fontrows include readable distinguishable亻/傚/倣/放; actual "
        "fallbackface/otherfontscales/unseenpixels unverified. Accepted394Android3+1/noskips and396native2terminal0/114.805s "
        "reverified, not rerun: single full productionContentSync1075kanji5033words95N1/c19b742b7e6320a7/problems0/epoch1; "
        "fullOnホウ/fullKunなら.う/bothcuratedほう/ならう/Full+Lite/twopairs-fourdirections/SystemBack/offline/meaningBackBEFORENext"
        "notnewpersistedgrade/BOTHsolecuratedOnKunGood/tenreference-touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain. "
        "NOTMLKit/correcthumanrecall/phone. Source/publiclookup/attribution-only headings/incompletewrappers/gaijilimits retained. "
        "Original393permissiondenial and parent exact recovery,049HOST512MiBOOM and qualified host-only1GiB init retained; "
        "no guest/appheap/font/archiveguard increase. Fresh main54fd8ff4 ancestral; no new runtime/teaching merge delta."
    )
    audit.update(
        status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=START,
        latestMainIntegrated=BASE, normalMergeResult="Fresh fetch and normal merge already up to date; no conflicts or changed teaching.",
        exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": int(match[1]), "failures": 0, "errors": 0},
        validationReceipts=receipts, reviewedBatchTeachingUnchanged=True,
        strictHistoricalProcessContractAccepted=False, strictInitialProcessContractAccepted=False,
        prospectiveSupervisedRemediationAccepted=True, **checks, limits=limits,
    )
    save(S / "batch-063-acceptance-audit.json", audit)
    save(S / "execution-398.json", {
        "schemaVersion": 1, "execution": 398, "batch": "063", "status": audit["status"],
        "startingHead": START, "integratedMain": BASE, "recordedAt": datetime.now().astimezone().isoformat(),
        "acceptance": "batch-063-acceptance-audit.json", "publishedAdditions": 89, "remainingAdditions": 1139,
        "limits": limits, "nextAction": "Normal signing/ownerfastforward/greenCI/every immutable public ZIP runtimehash/terminal receipts/ownerissue60 before063 delivery or064.",
    })
    D.mkdir(exist_ok=False)
    for row in receipts:
        shutil.copyfile(Path(row["log"]), D / Path(row["log"]).name)
    for path in (Path(__file__), C / "execution-390.py"):
        shutil.copyfile(path, D / path.name)
    p["activeExecution"].update(status="combined-tree-locally-accepted-pending-normal-signing",
                               pythonTests=int(match[1]), limits=limits)
    p["stage"] = "batch-063-combined-accepted-pending-normal-signing"
    save(C / "progress.json", p)
    print(f"Combined acceptance: {match[1]} Python tests,8317hashes,90exact additions,Android4/native2 reverified; no064.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"start": start, "source-audit": source_audit, "validate": validate, "evidence": evidence, "accept": accept}[sys.argv[1]]()
