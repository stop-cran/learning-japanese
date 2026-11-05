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
teaching = "acc397033503a38aa88506fc3ad966761793db72"
assert head == "4aa811b55df37e07d93ec3aaf0d97a0f386881c7"
assert main == "e8dc74eba6a783552f069593c6fc1d3849986293"
assert subprocess.run(["git", "merge-base", "--is-ancestor", main, head], cwd=r).returncode == 0
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
state_path = c / "progress.json"
state = load(state_path)
assert state["checkpoint"] == 338 and state["activeExecution"]["execution"] == 339
native = load(reviews / "batch-057-native-acceptance.json")
reconciliation = load(reviews / "batch-057-reconciliation.json")
assert native["status"] == "bounded-native-original-visual-reconciled-pending-combined-main-publication"
assert reconciliation["reviewClosed"] and all(row["status"] == "resolved" for row in reconciliation["findings"])
assert not native["strictInitialProcessContractAccepted"] and not native["strictVisualProcessContractAccepted"]
initials = load(reviews / "batch-057-initial-review-checkpoint.json")["reviewProcesses"]
assert [p["model"] for p in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
assert [p["toolCalls"] for p in initials] == [78, 75]
assert [len(p["observedInternalOverlaps"]) for p in initials] == [52, 0]
for row in initials:
    label = row["label"]
    assert row["exitCode"] == 0
    assert sha(reviews / f"batch-057-{label}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-057-{label}-execution.json") == row["executionRecordSha256"]
    assert sha(c / f"batch-057-{label}.jsonl") == row["rawExecutionSha256"]
for row in reconciliation["confirmations"]:
    assert sha(reviews / row["report"]) == row["reportSha256"]
    assert sha(reviews / row["execution"]) == row["executionSha256"]
    assert sha(c / f"batch-057-{row['label']}.jsonl") == row["rawExecutionSha256"]
    assert row["exitCode"] == 0 and row["overlappingStarts"] == 0
    assert row["completeDossierByteHashVerified"]
visuals = []
for label, initial, calls, images, overlaps in [
    ("claude", initials[0], 32, 23, 1),
    ("gpt", initials[1], 32, 23, 0),
    ("claude-clarification", initials[0], 3, 2, 0),
]:
    row = load(reviews / f"batch-057-visual-{label}-execution.json")
    assert row["sessionId"] == initial["sessionId"]
    assert row["actualModels"] == [initial["model"]] and row["exitCode"] == 0
    assert len(row["observedToolOverlaps"]) == overlaps and not row["unfinishedTools"]
    assert len(row["toolCalls"]) == calls and row["imagePayloadsVerified"] == images
    assert sha(reviews / f"batch-057-visual-{label}.md") == row["reportSha256"]
    assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
    for call in row["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
    visuals.append(row)
assert all(datetime.fromisoformat(a["completedAt"]) < datetime.fromisoformat(b["startedAt"])
           for a, b in zip(visuals, visuals[1:]))
for row in native["receiptFiles"]:
    assert sha(r / row["path"]) == row["sha256"]
android = load(s / "execution-334.json")
for row in android["tests"]:
    assert sha(Path(row["sourcePath"])) == row["sha256"] == sha(r / row["artifactPath"])
    assert sha(app / row["testImplementation"]) == row["testImplementationSha256"]
    xml = ET.parse(r / row["artifactPath"]).getroot()
    assert int(xml.attrib["tests"]) == row["tests"]
    assert all(int(xml.attrib[key]) == 0 for key in ["errors", "failures", "skipped"])
    assert sorted(x.attrib["name"] for x in xml.findall("testcase")) == sorted(row["caseNames"])
    assert xml.attrib["timestamp"] == row["timestamp"]
    assert Path(row["fixtureRoot"]).resolve() == r.resolve()
assert [x["tests"] for x in android["tests"]] == [3, 1]
assert sha(Path(android["log"])) == android["logSha256"]
execution = load(s / "execution-336.json")
log = r / execution["nativeRawLog"]
assert sha(log) == execution["rawLogSha256"]
codes = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                   log.read_text(encoding="utf-8"), re.M)
assert codes == ["1", "0", "1", "0"]
assert execution["nativeExecution"]["terminalSuccessCases"] == 2
assert execution["nativeExecution"]["passed"] and execution["nativeExecution"]["ownedHelperStopped"]
route = load(reviews / "batch-057-native" / "attempt-1" / "n1-057-article-route.json")
assert route == execution["productionImportEvidence"] == native["nativeResult"]
assert route["archiveRequests"] == 1
assert [route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]] == [1069, 5028, 89, 0]
assert route["acceptedReadingParserEpoch"] == 1 and route["offline"] and not route["phoneEvidence"]
assert route["fullOnyomi"] == ["キ"] and route["fullKunyomi"] == ["くわだ.てる", "たくら.む"]
assert route["quizOnKeys"] == ["き"] and route["quizKunKeys"] == ["くわだてる"]
preparation = load(s / "execution-335.json")
for row in preparation["artifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
index = load(reviews / "batch-057-native" / "execution-336-artifact-index.json")
assert len(index["files"]) == 52
for row in index["files"]:
    assert sha(r / row["path"]) == row["sha256"]
archival = load(s / "execution-337.json")
assert sha(r / archival["priorExecutionRecord"]) == archival["priorExecutionRecordSha256"]
assert sha(r / archival["parentRecovery"]) == archival["parentRecoverySha256"]
assert archival["parentExactCommandExitCode"] == 0 and archival["originalDenialRetained"]
baseline = load(s / "baseline-inventory.json")["files"]
original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
current = {p.stem for p in (r / "kanji").glob("*.md")}
expected = set(state["publicationCheckpoint"]["pilotMembership"])
for path in sorted(s.glob("batch-*-progress.json")):
    ledger = load(path)
    if int(ledger["batch"]) <= 57:
        members = set(ledger["membership"])
        assert not expected & members
        assert ledger["reviewClosed"] == ledger["membership"]
        expected.update(members)
assert current - original == expected and len(expected) == 84 and original <= current
receipts = load(c / "artifacts" / "execution-339-validation-receipts.json")
for row in receipts:
    assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
tests = (c / "logs" / "execution-339-python-tests.txt").read_text(encoding="utf-8")
match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
assert match
test_count = int(match[1])
budget = ast.literal_eval((c / "logs" / "execution-339-budget.txt").read_text())
limits = (
    "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
    "Original blind Claude78calls/GPT75calls,52/0internaloverlaps and Claude false serial self-claim retained; "
    "strict original process acceptance NOT claimed. Both original-session one-call bounded confirmations resolved057-F1 "
    "practical ambiguity, without declaring the original synchronic sentence an established historical error. "
    "194frozenfamilies mechanically re-extracted, not newly linguistically reviewed. Optional hypotheses unadopted. "
    "Original-session visuals32/32/3calls and23/23/2actualPNGpayloads; ClaudeONE internal two-image overlap retained, "
    "GPT/clarificationzero. Both affected images reread serially; static-backlink sequence inference withdrawn. "
    "No retroactive strict initial/visual process acceptance.43sourcePNGs/23distinct/20equivalentcopies; "
    "1080x2400sources returned900x2000, both byte sets preserved. Cropped table cells/hiddencontent/fullarticle rendering "
    "UNVERIFIED; bounded viewport acceptance only. Four production-font rows show企全危休 distinct and人止業企業企てる "
    "readable; Textbook finalる wrap visible; actual fallback face unknown. Actual meaning choices tiger/riceplant/"
    "plan;undertake/mosquito, not authored危休全 or all-pool quiz certification. Meaning feedback exits Back without "
    "persistence; both curated Good logs and DrawAgain after Next. Six reference-touch strokes/ungradedtrace/"
    "modelunavailablegeometry-only/recallmiss NOTMLKit/correcthumanrecall/negativegeometry/reverseorder evidence. "
    "Synthetic source/queues/logs, not ownerprogress. Original336denial and parentEXACTcleanupverificationexit0 retained. "
    "Original049HOST512MiBOOM/existing1GiBHOSTcoreTest-only/native192m576m/font/archive guards unchanged. "
    "Current maine8dc74eb already ancestral; no new runtime/teaching merge delta or concern requiring duplicate tests."
)
audit = load(s / "batch-057-acceptance-source-audit.json")
audit.update(
    status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=head,
    latestMainIntegrated=main, normalMergeResult="Fresh fetch and normal merge: already up to date; no conflicts.",
    exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": test_count, "failures": 0, "errors": 0},
    validationReceipts=receipts, budget=budget, acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
    originalInitialToolCalls=[78, 75], originalInitialOverlaps=[52, 0],
    originalVisualToolCalls=[32, 32, 3], originalVisualPngReturns=[23, 23, 2],
    originalVisualOverlaps=[1, 0, 0], indexedNativeArtifactsReverified=52,
    acceptedAndroidNativeTestsRerun=False, reviewedBatchTeachingUnchanged=True,
    strictInitialProcessContractAccepted=False, strictVisualProcessContractAccepted=False,
    nativeContentVersion=route["contentVersion"], mergedContentVersion=load(r / "manifest.json")["contentVersion"],
    limits=limits,
)
save(s / "batch-057-acceptance-audit.json", audit)
save(s / "execution-339.json", {
    "schemaVersion": 1, "execution": 339, "batch": "057",
    "status": "combined-tree-locally-accepted-pending-publication",
    "startingHead": head, "integratedMain": main, "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": "batch-057-acceptance-audit.json", "publishedAdditions": 83,
    "remainingAdditions": 1145, "limits": limits,
    "nextAction": "Normal signing/owner fastforward/terminalgreenCI/every immutable public ZIP runtimehash/terminal receipts/owner issue60 before057 delivery or058.",
})
dest = s / "batch-057-acceptance"
dest.mkdir(exist_ok=False)
for row in receipts:
    shutil.copyfile(Path(row["log"]), dest / Path(row["log"]).name)
for path in [Path(__file__), c / "audit-batch-057-acceptance.py", c / "execution-331-audit.py",
             c / "validate-execution-339.py", c / "start-execution-339.py"]:
    shutil.copyfile(path, dest / path.name)
state["activeExecution"].update(status="combined-tree-locally-accepted-pending-normal-signing",
                                integratedMain=main, pythonTests=test_count)
state["stage"] = "batch-057-combined-accepted-pending-normal-signing"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Combined acceptance: Python{test_count};8300runtime hashes; exact84local additions; Android4/native2/reviews reverified, not rerun. Publication pending.")
