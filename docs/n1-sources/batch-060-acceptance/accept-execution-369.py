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
teaching = "ea1dac1a6fd2c452db9cf602442e1f287ff95c67"
assert head == "8afd309e239befc132fe476a9dde53ea21f345a1"
assert main == "48d7110f893a2700dce2f73c5f14653b19b1a14d"
assert subprocess.run(["git", "merge-base", "--is-ancestor", main, head], cwd=r).returncode == 0
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
state_path = c / "progress.json"
state = load(state_path)
before_state = copy.deepcopy(state)
assert state["checkpoint"] == 368 and state["batch"] == "060"
native = load(reviews / "batch-060-native-acceptance.json")
reconciliation = load(reviews / "batch-060-reconciliation.json")
assert native["status"] == "bounded-native-visual-reconciled-pending-combined-main-publication"
assert reconciliation["textualReviewClosed"] and not reconciliation["findings"]
assert reconciliation["supervisedRemediationAccepted"]
assert not reconciliation["strictInitialInternalSerializationAccepted"]
assert [x["status"] for x in reconciliation["processFindings"]] == ["partially resolved"] * 2
assert native["nativeAssertionsPassed"] and native["boundedIndependentVisualAcceptance"]
assert not native["strictHistoricalProcessContractAccepted"]
initial_record = reviews / reconciliation["initialReviewRecord"]
assert sha(initial_record) == reconciliation["initialReviewRecordSha256"]
initials = load(initial_record)["reviewProcesses"]
assert [p["model"] for p in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
assert [p["toolCalls"] for p in initials] == [48, 45]
assert [len(p["observedInternalOverlaps"]) for p in initials] == [1, 0]
for row in initials:
    label = row["label"]
    assert row["exitCode"] == 0 and row["snapshot"] == teaching
    assert row["allAssignedRangesReturned"]
    assert sha(reviews / f"batch-060-{label}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-060-{label}-execution.json") == row["executionRecordSha256"]
    assert sha(reviews / f"batch-060-{label}-coverage.json") == row["coverageRecordSha256"]
    assert sha(c / f"batch-060-{label}.jsonl") == row["rawExecutionSha256"]
for row in reconciliation["dependentExecutions"]:
    assert sha(reviews / f"batch-060-{row['label']}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-060-{row['label']}-execution.json") == row["executionRecordSha256"]
    assert sha(c / f"batch-060-{row['label']}.jsonl") == row["rawExecutionSha256"]
    assert row["exitCode"] == 0 and row["allAssignedRangesReturned"]
assert [row["toolCalls"] for row in reconciliation["dependentExecutions"]] == [8, 1, 1]
assert [len(row["internalOverlaps"]) for row in reconciliation["dependentExecutions"]] == [5, 0, 0]
visuals = []
for label, initial, calls, images in [
    ("claude", initials[0], 29, 19), ("gpt", initials[1], 28, 19),
    ("claude-glyph", initials[0], 1, 1),
]:
    row = load(reviews / f"batch-060-visual-{label}-execution.json")
    assert row["sessionId"] == initial["sessionId"]
    assert row["actualModels"] == [initial["model"]] and row["exitCode"] == 0
    assert not row["observedToolOverlaps"] and not row["unfinishedTools"] and not row["multiToolResponses"]
    assert len(row["toolCalls"]) == calls and row["imagePayloadsVerified"] == images
    assert max(row["requestsPerAssistantResponse"]) == 1
    assert sha(reviews / f"batch-060-visual-{label}.md") == row["reportSha256"]
    assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
    for call in row["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
    visuals.append(row)
for first, second in zip(visuals, visuals[1:]):
    assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
for row in native["reviewers"]:
    assert sha(reviews / row["report"]) == row["reportSha256"]
    assert sha(reviews / row["execution"]) == row["executionSha256"]
visual_record = load(s / "execution-368.json")
for row in visual_record["archivedExecutionReceipts"]:
    assert sha(r / row["path"]) == row["sha256"]
assert sha(reviews / "batch-060-native-acceptance.json") == visual_record["acceptanceSha256"]
assert sha(reviews / native["textualReconciliation"]) == native["textualReconciliationSha256"]
assert sha(r / "docs" / native["nativeEvidence"]) == native["nativeEvidenceSha256"]
android = load(s / "execution-365.json")
for row in android["archivedArtifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
for row in android["provenance"]:
    assert sha(Path(row["path"])) == row["sha256"]
for row in android["recovery"]["tests"]:
    archived = reviews / "batch-060-android" / Path(row["artifactPath"]).name
    assert sha(Path(row["sourcePath"])) == row["sha256"] == sha(archived)
    xml = ET.parse(archived).getroot()
    assert int(xml.attrib["tests"]) == row["tests"]
    assert all(int(xml.attrib[key]) == 0 for key in ["errors", "failures", "skipped"])
    assert sorted(x.attrib["name"] for x in xml.findall("testcase")) == sorted(row["caseNames"])
    assert xml.attrib["timestamp"] == row["timestamp"]
    assert Path(row["fixtureRoot"]).resolve() == r.resolve()
assert [x["tests"] for x in android["recovery"]["tests"]] == [3, 1]
execution = load(s / "execution-367.json")
log = r / execution["nativeRawLog"]
assert sha(log) == execution["rawLogSha256"]
codes = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                   log.read_text(encoding="utf-8"), re.M)
assert codes == ["1", "0", "1", "0"]
assert execution["nativeExecution"]["terminalSuccessCases"] == 2
assert all(execution["nativeExecution"][k] for k in ["passed", "ownedHelperStopped", "ownedQemuStopped"])
route = load(reviews / "batch-060-native" / "attempt-1" / "n1-060-article-route.json")
assert route == execution["productionImportEvidence"]
assert route["archiveRequests"] == 1
assert [route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]] == [1072, 5031, 92, 0]
assert route["acceptedReadingParserEpoch"] == 1 and route["offline"] and not route["phoneEvidence"]
assert route["fullOnyomi"] == ["テイ", "チン"] and route["fullKunyomi"] == []
assert route["quizOnKeys"] == ["てい"] and route["quizKunKeys"] == []
assert execution["directedReciprocalTransitions"] == 4 and len(execution["reciprocalPairs"]) == 2
preparation = load(s / "execution-366.json")
for row in preparation["artifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
assert sha(r / execution["artifactIndex"]) == execution["artifactIndexSha256"]
index = load(r / execution["artifactIndex"])
assert len(index["files"]) == 49
for row in index["files"]:
    assert sha(r / row["path"]) == row["sha256"]
baseline = load(s / "baseline-inventory.json")["files"]
original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
current = {p.stem for p in (r / "kanji").glob("*.md")}
expected = set(state["publicationCheckpoint"]["pilotMembership"])
for path in sorted(s.glob("batch-*-progress.json")):
    ledger = load(path)
    if int(ledger["batch"]) <= 60:
        members = set(ledger["membership"])
        assert not expected & members and ledger["reviewClosed"] == ledger["membership"]
        expected.update(members)
assert current - original == expected and len(expected) == 87 and original <= current
receipts = load(c / "artifacts" / "execution-369-validation-receipts.json")
for row in receipts:
    assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
tests = (c / "logs" / "execution-369-python-tests.txt").read_text(encoding="utf-8")
match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
assert match
test_count = int(match[1])
budget = ast.literal_eval((c / "logs" / "execution-369-budget.txt").read_text())
limits = (
    "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
    "Original blind Claude48/GPT45calls one/zero internaloverlaps; Claude060-P1 and faileddependent060-P2 remain "
    "partially resolved historical noncompliance. Two supervised original-session single-resource lexical confirmations "
    "complete, not retroactive strictinitialacceptance. No actionable teaching findings; three optionals not adopted; "
    "larger/randomquiz pools untested.51frozenfamilies mechanically re-extracted, not newly linguistically reviewed. "
    "Original-sessionvisuals29/28calls plus Claudeone-image clarification, zerooverlaps/onecallperresponse,19/19/1actual "
    "PNGpayloads and serial terminal0 retained.36sourcePNGs/19distinct/17equivalent;1080x2400sources and actual900x2000 "
    "modelpayloads separately preserved. Fulltable/everyarticlepixel/停native route UNVERIFIED. Fourproductionfontrows "
    "亭停京享高 distinct/亠亻冖丁小子口料料亭 readable/no blankboxes; fallbackfaceunknown. Staticlinks not operationalroute "
    "proof; accepted367fourtransitions/SystemBack/offline/solecuratedOnGood/no-kun/meaningBackwithoutNext/"
    "ninereference-touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain retained. NOTMLKit/correcthumanrecall/phone. "
    "Synthetic source/queues/logs not ownerprogress. Original364permissiondenial/parentexactrecovery and049HOST512MiBOOM/"
    "samequalifiedhost-only1GiBinit unchanged; native192m576m/font/archiveguards unchanged. Latestmain48d7110f already "
    "ancestral; no new runtime/teaching merge delta or concern requiring duplicateAndroid/native/reviewer work."
)
audit = load(s / "batch-060-acceptance-source-audit.json")
audit.update(
    status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=head,
    latestMainIntegrated=main, normalMergeResult="Fresh fetch and normal merge: already up to date; no conflicts.",
    exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": test_count, "failures": 0, "errors": 0},
    validationReceipts=receipts, budget=budget, acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
    originalInitialToolCalls=[48, 45], originalInitialOverlaps=[1, 0],
    originalDependentOverlaps=[5, 0, 0], originalVisualToolCalls=[29, 28, 1],
    originalVisualPngReturns=[19, 19, 1], originalVisualOverlaps=[0, 0, 0],
    indexedNativeArtifactsReverified=49, acceptedAndroidNativeTestsRerun=False,
    reviewedBatchTeachingUnchanged=True, strictHistoricalProcessContractAccepted=False,
    supervisedLexicalRemediationAccepted=True, strictVisualProcessContractAccepted=True,
    nativeContentVersion=route["contentVersion"],
    mergedContentVersion=load(r / "manifest.json")["contentVersion"], limits=limits,
)
save(s / "batch-060-acceptance-audit.json", audit)
save(s / "execution-369.json", {
    "schemaVersion": 1, "execution": 369, "batch": "060",
    "status": "combined-tree-locally-accepted-pending-publication",
    "startingHead": head, "integratedMain": main, "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": "batch-060-acceptance-audit.json", "publishedAdditions": 86,
    "remainingAdditions": 1142, "limits": limits,
    "nextAction": "Normal signing/owner fastforward/terminalgreenCI/every immutable public ZIP runtimehash/terminal receipts/owner issue60 before060 delivery or061.",
})
dest = s / "batch-060-acceptance"
dest.mkdir(exist_ok=False)
for row in receipts:
    shutil.copyfile(Path(row["log"]), dest / Path(row["log"]).name)
for path in [Path(__file__), c / "audit-batch-060-acceptance.py", c / "execution-361-audit.py",
             c / "validate-execution-369.py", c / "start-execution-369.py"]:
    shutil.copyfile(path, dest / path.name)
state["activeExecution"].update(
    status="combined-tree-locally-accepted-pending-normal-signing",
    integratedMain=main, pythonTests=test_count, limits=limits)
state["stage"] = "batch-060-combined-accepted-pending-normal-signing"
assert all(state[k] == v for k, v in before_state.items() if k not in {"activeExecution", "stage"})
tmp = c / "progress.json.tmp"
assert not tmp.exists()
tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp.replace(state_path)
print(f"Combined acceptance: Python{test_count};8309runtime hashes; exact87local additions; Android4/native2/reviews reverified, not rerun. Publication pending.")
