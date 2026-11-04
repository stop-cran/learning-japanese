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
teaching = "a532c4d436726e6eeb46ff78cc3dc1a039d6f19e"
assert head == "9361f6129024a65699081cd1a62b589929e3fd60"
assert main == "998eca51e8d6620a4e60f7b66fdb8c1ff515a545"
assert subprocess.run(["git", "merge-base", "--is-ancestor", main, head], cwd=r).returncode == 0
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
state_path = c / "progress.json"
state = load(state_path)
assert state["checkpoint"] == 314 and state["activeExecution"]["execution"] == 315
native = load(reviews / "batch-055-native-acceptance.json")
reconciliation = load(reviews / "batch-055-reconciliation.json")
assert native["status"] == "native-and-original-two-family-visual-evidence-closed-pending-combined-main-publication"
assert reconciliation["findings"] == reconciliation["unresolvedConsequentialClaims"] == []
initials = reconciliation["reviewProcesses"]
assert [p["model"] for p in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
for row in initials:
    label = row["label"]
    assert row["exitCode"] == 0
    assert sha(reviews / f"batch-055-{label}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-055-{label}-execution.json") == row["executionRecordSha256"]
    assert sha(c / f"batch-055-{label}.jsonl") == row["rawExecutionSha256"]
assert [len(x["observedInternalOverlaps"]) for x in initials] == [2, 0]
visuals = []
for label, initial in zip(["claude", "gpt"], initials):
    row = load(reviews / f"batch-055-visual-{label}-execution.json")
    assert row["sessionId"] == initial["sessionId"]
    assert row["actualModels"] == [initial["model"]] and row["exitCode"] == 0
    assert not row["observedToolOverlaps"] and not row["unfinishedTools"]
    assert len(row["toolCalls"]) == 27 and row["imagePayloadsVerified"] == 20
    assert sha(reviews / f"batch-055-visual-{label}.md") == row["reportSha256"]
    assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
    for call in row["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
    visuals.append(row)
assert datetime.fromisoformat(visuals[0]["completedAt"]) < datetime.fromisoformat(visuals[1]["startedAt"])
for row in native["receiptFiles"]:
    assert sha(r / row["path"]) == row["sha256"]
android = load(s / "execution-310.json")
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
execution = load(s / "execution-312.json")
log = r / execution["nativeRawLog"]
assert sha(log) == execution["rawLogSha256"]
codes = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                   log.read_text(encoding="utf-8"), re.M)
assert codes == ["1", "0", "1", "0"]
assert execution["nativeExecution"]["terminalSuccessCases"] == 2
assert execution["nativeExecution"]["passed"] and execution["nativeExecution"]["ownedHelperStopped"]
route = load(reviews / "batch-055-native" / "attempt-1" / "n1-055-article-route.json")
assert route == execution["productionImportEvidence"] and route["archiveRequests"] == 1
assert [route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]] == [1067, 5025, 87, 0]
assert route["acceptedReadingParserEpoch"] == 1 and route["offline"] and not route["phoneEvidence"]
index = load(reviews / "batch-055-native" / "artifact-index.json")
for row in index["sourceArtifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
baseline = load(s / "baseline-inventory.json")["files"]
original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
current = {p.stem for p in (r / "kanji").glob("*.md")}
expected = set(state["publicationCheckpoint"]["pilotMembership"])
for path in sorted(s.glob("batch-*-progress.json")):
    ledger = load(path)
    if int(ledger["batch"]) <= 55:
        members = set(ledger["membership"])
        assert not expected & members
        assert ledger["reviewClosed"] == ledger["membership"]
        expected.update(members)
assert current - original == expected and len(expected) == 82 and original <= current
receipts = load(c / "artifacts" / "execution-315-validation-receipts.json")
for row in receipts:
    assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
tests = (c / "logs" / "execution-315-python-tests.txt").read_text(encoding="utf-8")
match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
assert match
test_count = int(match[1])
budget = ast.literal_eval((c / "logs" / "execution-315-budget.txt").read_text())
limits = (
    "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
    "Initial Claude42calls/TWO internal overlaps and GPT44calls/zero retained;26 assigned resources each. "
    "Four Claude optional groups not adopted; older wholewordしょうじょう constituent allocation UNVERIFIED "
    "and omitted from positive teaching/practice. No new blind reviews or native/Android reruns. "
    "Original-session visual confirmations27 serial calls/20 PNG payloads each/zero overlaps;1080x2400 sources "
    "resized900x2000, both byte sets preserved. Bounded viewports/table clipping, not every-cell/full-article evidence. "
    "Actual meaning options yuzu citrus/carp/monme differ from authored蒸乗水; no all-pool quiz certification. "
    "Reference-touch six strokes/ungraded trace/geometric-only model unavailable/recall miss/persisted Again "
    "are not MLKit recognition/human recall success/negative geometry/reverse-order evidence. "
    "Four readable production rows do not identify actual fallback faces. Synthetic source/queues/logs, not ownerprogress. "
    "Original312 permission denial and exact parent shell1 from absent stopped PIDs retained; separately verified "
    "clean Android/owned process absence, no unowned device modified. Original049HOST512MiB OOM/1GiB HOST-only "
    "test qualification not native heap authorization; native192m576m/font/archive guards unchanged. "
    "Current main998eca5 already ancestral; no new runtime/teaching merge delta or concern requiring duplicate tests."
)
audit = load(s / "batch-055-acceptance-source-audit.json")
audit.update(
    status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=head,
    latestMainIntegrated=main, normalMergeResult="Fresh fetch and normal merge: already up to date; no conflicts.",
    exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": test_count, "failures": 0, "errors": 0},
    validationReceipts=receipts, budget=budget, acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
    originalInitialToolCalls=[42, 44], originalInitialOverlaps=[2, 0],
    originalVisualToolCalls=[27, 27], originalVisualPngReturns=[20, 20], originalVisualOverlaps=[0, 0],
    nativeSourceArtifactsReverified=len(index["sourceArtifacts"]), acceptedAndroidNativeTestsRerun=False,
    reviewedBatchTeachingUnchanged=True, nativeContentVersion=route["contentVersion"],
    mergedContentVersion=load(r / "manifest.json")["contentVersion"], limits=limits,
)
save(s / "batch-055-acceptance-audit.json", audit)
save(s / "execution-315.json", {
    "schemaVersion": 1, "execution": 315, "batch": "055",
    "status": "combined-tree-locally-accepted-pending-publication",
    "startingHead": head, "integratedMain": main, "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": "batch-055-acceptance-audit.json", "publishedAdditions": 81,
    "remainingAdditions": 1147, "limits": limits,
    "nextAction": "Normal signing/owner fastforward/terminalgreenCI/every immutable public ZIP runtimehash/terminal receipts/owner issue60 before055 delivery or056.",
})
dest = s / "batch-055-acceptance"
dest.mkdir(exist_ok=False)
for row in receipts:
    shutil.copyfile(Path(row["log"]), dest / Path(row["log"]).name)
for path in [Path(__file__), c / "audit-batch-055-acceptance.py", c / "audit-batch-055-draft.py",
             c / "validate-execution-315.py", c / "start-execution-315.py"]:
    shutil.copyfile(path, dest / path.name)
state["activeExecution"].update(status="combined-tree-locally-accepted-pending-normal-signing",
                                integratedMain=main, pythonTests=test_count)
state["stage"] = "batch-055-combined-accepted-pending-normal-signing"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Combined acceptance: Python{test_count};8293runtime hashes; exact82local additions; Android4/native2/reviews reverified, not rerun. Publication pending.")
