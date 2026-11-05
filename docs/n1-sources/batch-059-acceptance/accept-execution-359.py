import ast
import copy
import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
app = c.parent / "kanji-cards-android"
s = r / "docs" / "n1-sources"
reviews = r / "docs" / "n1-reviews"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, value):
    assert not path.exists(), path
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree,
                                   text=True, encoding="utf-8").strip()


head = git("rev-parse", "HEAD")
main = git("rev-parse", "origin/main")
teaching = "769293c824dc41abb9386e76c4dd5f8c676e48e0"
assert head == "f074f1116460c112a61687f587bbda7b2b91b0cb"
assert main == "633f60022b4c42d5f3a6fa83f85465c39729cedd"
assert subprocess.run(["git", "merge-base", "--is-ancestor", main, head], cwd=r).returncode == 0
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
state_path = c / "progress.json"
state = load(state_path)
before_state = copy.deepcopy(state)
assert state["checkpoint"] == 358 and state["batch"] == "059"
native = load(reviews / "batch-059-native-acceptance.json")
reconciliation = load(reviews / "batch-059-reconciliation.json")
assert native["status"] == "bounded-native-visual-reconciled-pending-combined-main-publication"
assert reconciliation["reviewClosed"] and all(x["status"] == "resolved" for x in reconciliation["findings"])
assert native["nativeAssertionsPassed"] and native["boundedIndependentVisualAcceptance"]
assert not native["strictHistoricalProcessContractAccepted"]
assert reconciliation["processDeviation"]["historicalNoncomplianceRetained"]
initials = load(reviews / "batch-059-initial-review-checkpoint.json")["reviewProcesses"]
assert [p["model"] for p in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
assert [p["toolCalls"] for p in initials] == [55, 55]
assert [len(p["observedInternalOverlaps"]) for p in initials] == [0, 0]
for row in initials:
    label = row["label"]
    assert row["exitCode"] == 0 and row["snapshot"] == reconciliation["initialTeachingSnapshot"]
    assert row["allAssignedRangesReturned"] and not row["multiToolResponses"]
    assert sha(reviews / f"batch-059-{label}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-059-{label}-execution.json") == row["executionRecordSha256"]
    assert sha(reviews / f"batch-059-{label}-coverage.json") == row["coverageRecordSha256"]
    assert sha(c / f"batch-059-{label}.jsonl") == row["rawExecutionSha256"]
for row in reconciliation["confirmations"]:
    assert sha(reviews / row["report"]) == row["reportSha256"]
    assert sha(reviews / row["execution"]) == row["executionSha256"]
    assert sha(c / f"batch-059-{row['label']}.jsonl") == row["rawExecutionSha256"]
    assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
assert [row["internalOverlaps"] for row in reconciliation["confirmations"]] == [1, 0, 0]
visuals = []
for label, initial in zip(["claude", "gpt"], initials):
    row = load(reviews / f"batch-059-visual-{label}-execution.json")
    assert row["sessionId"] == initial["sessionId"]
    assert row["actualModels"] == [initial["model"]] and row["exitCode"] == 0
    assert not row["observedToolOverlaps"] and not row["unfinishedTools"]
    assert len(row["toolCalls"]) == 29 and row["imagePayloadsVerified"] == 20
    assert max(row["requestsPerAssistantResponse"]) == 1
    assert sha(reviews / f"batch-059-visual-{label}.md") == row["reportSha256"]
    assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
    for call in row["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
    visuals.append(row)
assert datetime.fromisoformat(visuals[0]["completedAt"]) < datetime.fromisoformat(visuals[1]["startedAt"])
for row in native["reviewers"]:
    assert sha(reviews / row["report"]) == row["reportSha256"]
    assert sha(reviews / row["execution"]) == row["executionSha256"]
visual_record = load(s / "execution-358.json")
for row in visual_record["archivedExecutionReceipts"]:
    assert sha(r / row["path"]) == row["sha256"]
assert sha(reviews / "batch-059-native-acceptance.json") == visual_record["acceptanceSha256"]
assert sha(reviews / native["textualReconciliation"]) == native["textualReconciliationSha256"]
assert sha(r / "docs" / native["nativeEvidence"]) == native["nativeEvidenceSha256"]
android = load(s / "execution-355.json")
for row in android["archivedArtifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
for row in android["provenance"]:
    assert sha(Path(row["path"])) == row["sha256"]
for row in android["recovery"]["tests"]:
    archived = reviews / "batch-059-android" / Path(row["artifactPath"]).name
    assert sha(Path(row["sourcePath"])) == row["sha256"] == sha(archived)
    xml = ET.parse(archived).getroot()
    assert int(xml.attrib["tests"]) == row["tests"]
    assert all(int(xml.attrib[key]) == 0 for key in ["errors", "failures", "skipped"])
    assert sorted(x.attrib["name"] for x in xml.findall("testcase")) == sorted(row["caseNames"])
    assert xml.attrib["timestamp"] == row["timestamp"]
    assert Path(row["fixtureRoot"]).resolve() == r.resolve()
assert [x["tests"] for x in android["recovery"]["tests"]] == [3, 1]
execution = load(s / "execution-357.json")
log = r / execution["nativeRawLog"]
assert sha(log) == execution["rawLogSha256"]
codes = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                   log.read_text(encoding="utf-8"), re.M)
assert codes == ["1", "0", "1", "0"]
assert execution["nativeExecution"]["terminalSuccessCases"] == 2
assert all(execution["nativeExecution"][k] for k in ["passed", "ownedHelperStopped", "ownedQemuStopped"])
route = load(reviews / "batch-059-native" / "attempt-1" / "n1-059-article-route.json")
assert route == execution["productionImportEvidence"]
assert route["archiveRequests"] == 1
assert [route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]] == [1071, 5030, 91, 0]
assert route["acceptedReadingParserEpoch"] == 1 and route["offline"] and not route["phoneEvidence"]
assert route["fullOnyomi"] == ["キョウ", "コウ"] and route["fullKunyomi"] == ["う.ける"]
assert route["quizOnKeys"] == ["きょう"] and route["quizKunKeys"] == []
assert execution["directedReciprocalTransitions"] == 4 and len(execution["reciprocalPairs"]) == 2
preparation = load(s / "execution-356.json")
for row in preparation["artifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
assert sha(r / execution["artifactIndex"]) == execution["artifactIndexSha256"]
index = load(r / execution["artifactIndex"])
assert len(index["files"]) == 48
for row in index["files"]:
    assert sha(r / row["path"]) == row["sha256"]
baseline = load(s / "baseline-inventory.json")["files"]
original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
current = {p.stem for p in (r / "kanji").glob("*.md")}
expected = set(state["publicationCheckpoint"]["pilotMembership"])
for path in sorted(s.glob("batch-*-progress.json")):
    ledger = load(path)
    if int(ledger["batch"]) <= 59:
        members = set(ledger["membership"])
        assert not expected & members and ledger["reviewClosed"] == ledger["membership"]
        expected.update(members)
assert current - original == expected and len(expected) == 86 and original <= current
receipts = load(c / "artifacts" / "execution-359-validation-receipts.json")
for row in receipts:
    assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
tests = (c / "logs" / "execution-359-python-tests.txt").read_text(encoding="utf-8")
match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
assert match
test_count = int(match[1])
budget = ast.literal_eval((c / "logs" / "execution-359-budget.txt").read_text())
limits = (
    "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
    "Original blind Claude55/GPT55calls zero internaloverlap; Claude first confirmation one overlapping/multitool response "
    "remains historical noncompliance. Same-session one-call boundedsource followup not retroactive strictacceptance. "
    "059-F1 resolved; three Claudeoptionals not adopted; larger/randomquiz pools untested.54frozenfamilies mechanically "
    "re-extracted, not newly linguistically reviewed. Original-sessionvisuals29/29calls zerooverlaps/onecallperresponse, "
    "20/20actualPNGpayloads and serial terminal0 processes retained.35sourcePNGs/20distinct/15equivalent; "
    "1080x2400sources and actual900x2000modelpayloads separately preserved. Recognitionexample visible but leftreadinglabel "
    "cropped; fulltable/everyarticlepixel UNVERIFIED. Fourproductionfontrows享京厚高 distinct/亠厂子口受享受 readable/no "
    "blankboxes; fallbackfaceunknown. Staticlinks not operationalroute proof; accepted357fourtransitions/SystemBack/offline/"
    "solecuratedOnGood/no-kun/meaningBackwithoutNext/eightreference-touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain "
    "retained. NOTMLKit/correcthumanrecall/phone. Synthetic source/queues/logs not ownerprogress. Original354permissiondenial/"
    "parentexactrecovery and049HOST512MiBOOM/samequalifiedhost-only1GiBinit unchanged; native192m576m/font/archiveguards unchanged. "
    "Latestmain633f6002 already ancestral; no new runtime/teaching merge delta or concern requiring duplicateAndroid/native/reviewer work."
)
audit = load(s / "batch-059-acceptance-source-audit.json")
audit.update(
    status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=head,
    latestMainIntegrated=main, normalMergeResult="Fresh fetch and normal merge: already up to date; no conflicts.",
    exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": test_count, "failures": 0, "errors": 0},
    validationReceipts=receipts, budget=budget, acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
    originalInitialToolCalls=[55, 55], originalInitialOverlaps=[0, 0],
    originalConfirmationOverlaps=[1, 0, 0], originalVisualToolCalls=[29, 29],
    originalVisualPngReturns=[20, 20], originalVisualOverlaps=[0, 0],
    indexedNativeArtifactsReverified=48, acceptedAndroidNativeTestsRerun=False,
    reviewedBatchTeachingUnchanged=True, strictHistoricalProcessContractAccepted=False,
    strictVisualProcessContractAccepted=True, nativeContentVersion=route["contentVersion"],
    mergedContentVersion=load(r / "manifest.json")["contentVersion"], limits=limits,
)
save(s / "batch-059-acceptance-audit.json", audit)
save(s / "execution-359.json", {
    "schemaVersion": 1, "execution": 359, "batch": "059",
    "status": "combined-tree-locally-accepted-pending-publication",
    "startingHead": head, "integratedMain": main, "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": "batch-059-acceptance-audit.json", "publishedAdditions": 85,
    "remainingAdditions": 1143, "limits": limits,
    "nextAction": "Normal signing/owner fastforward/terminalgreenCI/every immutable public ZIP runtimehash/terminal receipts/owner issue60 before059 delivery or060.",
})
dest = s / "batch-059-acceptance"
dest.mkdir(exist_ok=False)
for row in receipts:
    shutil.copyfile(Path(row["log"]), dest / Path(row["log"]).name)
for path in [Path(__file__), c / "audit-batch-059-acceptance.py", c / "execution-351-audit.py",
             c / "validate-execution-359.py", c / "start-execution-359.py"]:
    shutil.copyfile(path, dest / path.name)
state["activeExecution"].update(
    status="combined-tree-locally-accepted-pending-normal-signing",
    integratedMain=main, pythonTests=test_count, limits=limits)
state["stage"] = "batch-059-combined-accepted-pending-normal-signing"
assert all(state[k] == v for k, v in before_state.items() if k not in {"activeExecution", "stage"})
tmp = c / "progress.json.tmp"
assert not tmp.exists()
tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp.replace(state_path)
print(f"Combined acceptance: Python{test_count};8306runtime hashes; exact86local additions; Android4/native2/reviews reverified, not rerun. Publication pending.")
