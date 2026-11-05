import ast
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
teaching = "58b53fd31b6d55baba32c049fba62ac739feb004"
assert head == "378f4ba3b19cb81e46a0f9a6839e36998390fca9"
assert main == "c064f0c749bdc93bc1f86dbd01cec19212991bd7"
assert subprocess.run(["git", "merge-base", "--is-ancestor", main, head], cwd=r).returncode == 0
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
state_path = c / "progress.json"
state = load(state_path)
assert state["checkpoint"] == 348 and state["batch"] == "058"
native = load(reviews / "batch-058-native-acceptance.json")
reconciliation = load(reviews / "batch-058-reconciliation.json")
assert native["status"] == "bounded-native-original-visual-reconciled-pending-combined-main-publication"
assert reconciliation["reviewClosed"] and not reconciliation["findings"]
assert native["nativeAssertionsPassed"] and native["boundedIndependentVisualConfirmation"]
assert not native["strictInitialProcessContractAccepted"] and native["strictVisualProcessContractAccepted"]
initials = load(reviews / "batch-058-initial-review-checkpoint.json")["reviewProcesses"]
assert [p["model"] for p in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
assert [p["toolCalls"] for p in initials] == [49, 51]
assert [len(p["observedInternalOverlaps"]) for p in initials] == [3, 0]
for row in initials:
    label = row["label"]
    assert row["exitCode"] == 0 and row["snapshot"] == teaching
    assert sha(reviews / f"batch-058-{label}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-058-{label}-execution.json") == row["executionRecordSha256"]
    assert sha(c / f"batch-058-{label}.jsonl") == row["rawExecutionSha256"]
for row in reconciliation["confirmations"]:
    assert sha(reviews / row["report"]) == row["reportSha256"]
    assert sha(reviews / row["execution"]) == row["executionSha256"]
    assert sha(c / f"batch-058-{row['label']}.jsonl") == row["rawExecutionSha256"]
    assert row["exitCode"] == 0 and row["observedInternalOverlaps"] == 0
assert all(row["allAssignedRangesReturned"] for row in reconciliation["returnedRangeCoverage"])
visuals = []
for label, initial in zip(["claude", "gpt"], initials):
    row = load(reviews / f"batch-058-visual-{label}-execution.json")
    assert row["sessionId"] == initial["sessionId"]
    assert row["actualModels"] == [initial["model"]] and row["exitCode"] == 0
    assert not row["observedToolOverlaps"] and not row["unfinishedTools"]
    assert len(row["toolCalls"]) == 36 and row["imagePayloadsVerified"] == 25
    assert max(row["requestsPerAssistantResponse"]) == 1
    assert sha(reviews / f"batch-058-visual-{label}.md") == row["reportSha256"]
    assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
    for call in row["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
    visuals.append(row)
assert datetime.fromisoformat(visuals[0]["completedAt"]) < datetime.fromisoformat(visuals[1]["startedAt"])
for row in native["visualReports"]:
    assert sha(reviews / row["report"]) == row["reportSha256"]
    assert sha(reviews / row["audit"]) == row["auditSha256"]
for row in native["archivedExecutionReceipts"]:
    assert sha(r / row["path"]) == row["sha256"]
android = load(s / "execution-345.json")
for row in android["archivedArtifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
for row in android["provenance"]:
    assert sha(Path(row["path"])) == row["sha256"]
for row in android["recovery"]["tests"]:
    archived = reviews / "batch-058-android" / Path(row["artifactPath"]).name
    assert sha(Path(row["sourcePath"])) == row["sha256"] == sha(archived)
    xml = ET.parse(archived).getroot()
    assert int(xml.attrib["tests"]) == row["tests"]
    assert all(int(xml.attrib[key]) == 0 for key in ["errors", "failures", "skipped"])
    assert sorted(x.attrib["name"] for x in xml.findall("testcase")) == sorted(row["caseNames"])
    assert xml.attrib["timestamp"] == row["timestamp"]
    assert Path(row["fixtureRoot"]).resolve() == r.resolve()
assert [x["tests"] for x in android["recovery"]["tests"]] == [3, 1]
execution = load(s / "execution-347.json")
assert sha(r / native["nativeRecord"]) == native["nativeRecordSha256"]
assert sha(r / native["acceptedAndroidRecord"]) == native["acceptedAndroidRecordSha256"]
log = r / execution["nativeRawLog"]
assert sha(log) == execution["rawLogSha256"]
codes = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                   log.read_text(encoding="utf-8"), re.M)
assert codes == ["1", "0", "1", "0"]
assert execution["nativeExecution"]["terminalSuccessCases"] == 2
assert all(execution["nativeExecution"][k] for k in ["passed", "ownedHelperStopped", "ownedQemuStopped"])
route = load(reviews / "batch-058-native" / "attempt-1" / "n1-058-article-route.json")
assert route == execution["productionImportEvidence"]
assert route["archiveRequests"] == 1
assert [route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]] == [1070, 5029, 90, 0]
assert route["acceptedReadingParserEpoch"] == 1 and route["offline"] and not route["phoneEvidence"]
assert route["fullOnyomi"] == ["キュウ"] and route["fullKunyomi"] == ["おか"]
assert route["quizOnKeys"] == ["きゅう"] and route["quizKunKeys"] == ["おか"]
assert execution["directedReciprocalTransitions"] == 6 and len(execution["reciprocalPairs"]) == 3
preparation = load(s / "execution-346.json")
for row in preparation["artifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
assert sha(r / execution["artifactIndex"]) == execution["artifactIndexSha256"]
index = load(r / execution["artifactIndex"])
assert len(index["files"]) == 55
for row in index["files"]:
    assert sha(r / row["path"]) == row["sha256"]
baseline = load(s / "baseline-inventory.json")["files"]
original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
current = {p.stem for p in (r / "kanji").glob("*.md")}
expected = set(state["publicationCheckpoint"]["pilotMembership"])
for path in sorted(s.glob("batch-*-progress.json")):
    ledger = load(path)
    if int(ledger["batch"]) <= 58:
        members = set(ledger["membership"])
        assert not expected & members and ledger["reviewClosed"] == ledger["membership"]
        expected.update(members)
assert current - original == expected and len(expected) == 85 and original <= current
receipts = load(c / "artifacts" / "execution-349-validation-receipts.json")
for row in receipts:
    assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
tests = (c / "logs" / "execution-349-python-tests.txt").read_text(encoding="utf-8")
match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
assert match
test_count = int(match[1])
budget = ast.literal_eval((c / "logs" / "execution-349-budget.txt").read_text())
limits = (
    "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
    "Original blind Claude49/GPT51calls,3/0internaloverlaps across two Claude responses remain historical noncompliance; "
    "bounded original-session10/10call zero-overlap confirmations complete, not retroactive strict initial-process acceptance. "
    "No actionable teaching findings; three Claude optionals unadopted.68frozenfamilies mechanically re-extracted, not newly "
    "linguistically reviewed. Original-session visuals36/36calls,each one per response/zerooverlaps,25/25actualPNGpayloads "
    "and serial terminal0 processes retained.43sourcePNGs/25distinct/18equivalentcopies;1080x2400sources returned900x2000, "
    "both byte sets preserved. Cropped table cells/hiddencontent/fullarticle rendering UNVERIFIED; bounded viewport "
    "acceptance only. Four production-font rows show丘兵近共 distinct and一砂山/丘/砂丘 readable; fallbackface unidentified. "
    "Actual meaning choices chrysanthemum/hillknoll/pigpork/turtletortoise,not authored兵近共 or all-pool quiz certification. "
    "Meaning feedback exits Back without persistence; BOTHcurated Good logs and DrawAgain after Next. Five reference-touch "
    "strokes/ungradedtrace/modelunavailablegeometry-only/recallmiss NOTMLKit/correcthumanrecall/negativegeometry/reverseorder "
    "evidence. Synthetic source/queues/logs,not ownerprogress. Original344permissiondenial/parentexactrecovery and049HOST512MiBOOM/"
    "qualifiedexisting1GiBHOSTcoreTest-only init retained;native192m576m/font/archiveguards unchanged. Currentmainc064f0c7 "
    "already ancestral; no new runtime/teaching merge delta or concern requiring duplicate Android/native/reviewer work."
)
audit = load(s / "batch-058-acceptance-source-audit.json")
audit.update(
    status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=head,
    latestMainIntegrated=main, normalMergeResult="Fresh fetch and normal merge: already up to date; no conflicts.",
    exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": test_count, "failures": 0, "errors": 0},
    validationReceipts=receipts, budget=budget, acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
    originalInitialToolCalls=[49, 51], originalInitialOverlaps=[3, 0],
    originalVisualToolCalls=[36, 36], originalVisualPngReturns=[25, 25], originalVisualOverlaps=[0, 0],
    indexedNativeArtifactsReverified=55, acceptedAndroidNativeTestsRerun=False,
    reviewedBatchTeachingUnchanged=True, strictInitialProcessContractAccepted=False,
    strictVisualProcessContractAccepted=True, nativeContentVersion=route["contentVersion"],
    mergedContentVersion=load(r / "manifest.json")["contentVersion"], limits=limits,
)
save(s / "batch-058-acceptance-audit.json", audit)
save(s / "execution-349.json", {
    "schemaVersion": 1, "execution": 349, "batch": "058",
    "status": "combined-tree-locally-accepted-pending-publication",
    "startingHead": head, "integratedMain": main, "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": "batch-058-acceptance-audit.json", "publishedAdditions": 84,
    "remainingAdditions": 1144, "limits": limits,
    "nextAction": "Normal signing/owner fastforward/terminalgreenCI/every immutable public ZIP runtimehash/terminal receipts/owner issue60 before058 delivery or059.",
})
dest = s / "batch-058-acceptance"
dest.mkdir(exist_ok=False)
for row in receipts:
    shutil.copyfile(Path(row["log"]), dest / Path(row["log"]).name)
for path in [Path(__file__), c / "audit-batch-058-acceptance.py", c / "execution-341-audit.py",
             c / "validate-execution-349.py"]:
    shutil.copyfile(path, dest / path.name)
state["activeExecution"] = {
    "execution": 349, "batch": "058", "startingHead": head,
    "status": "combined-tree-locally-accepted-pending-normal-signing",
    "integratedMain": main, "pythonTests": test_count, "limits": limits,
}
state["stage"] = "batch-058-combined-accepted-pending-normal-signing"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Combined acceptance: Python{test_count};8303runtime hashes; exact85local additions; Android4/native2/reviews reverified, not rerun. Publication pending.")
