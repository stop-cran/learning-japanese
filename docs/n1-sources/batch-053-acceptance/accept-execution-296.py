import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
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
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = git("rev-parse", "HEAD")
assert head == "5564579c9778c1ed55f77f81dbbdfce118a03241"
assert git("rev-parse", "origin/main") == "e16c95b3edc55975b7a2c7985bf730425baa2f83"
assert not git("diff", head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert not git("diff", "3e37ebdac9af2880ceaa810ca34a7588d8c1d602", "--",
               "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
state_path = c / "progress.json"
state = load(state_path)
assert state["checkpoint"] == 295 and state["batch"] == "053"
save(c / "execution-296-starting-progress.json", state)
native = load(reviews / "batch-053-native-acceptance.json")
reconciliation = load(reviews / "batch-053-reconciliation.json")
assert native["status"] == "native-visual-closed-pending-combined-publication"
assert reconciliation["findings"] == reconciliation["unresolvedConsequentialClaims"] == []
assert not reconciliation["nativeVisualAcceptancePending"]
for row in native["evidenceCopies"]:
    assert sha(r / row["path"]) == row["sha256"] == sha(Path(row["source"])), row
for row in reconciliation["reviewProcesses"]:
    label = row["label"]
    assert sha(reviews / f"batch-053-{label}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-053-{label}-execution.json") == row["executionRecordSha256"]
    assert sha(c / f"batch-053-{label}.jsonl") == row["rawExecutionSha256"]
    assert row["exitCode"] == 0
initials = reconciliation["reviewProcesses"]
assert [p["model"] for p in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
for label, row in zip(["claude", "gpt"], native["originalReviewerVisualProcesses"]):
    assert sha(reviews / f"batch-053-visual-{label}.md") == row["reportSha256"]
    assert sha(c / f"batch-053-visual-{label}.jsonl") == row["rawExecutionSha256"]
    assert row["exitCode"] == 0 and not row["observedToolOverlaps"] and not row["unfinishedTools"]
    assert len(row["toolCalls"]) == 28 and row["imagePayloadsVerified"] == 21
    for call in row["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
visuals = native["originalReviewerVisualProcesses"]
assert datetime.fromisoformat(visuals[0]["completedAt"]) < datetime.fromisoformat(visuals[1]["startedAt"])
prep = load(s / "batch-053-native-preparation.json")
for path, digest in {**prep["originalFixtureHashesUnchanged"], **prep["originalInitialReportHashesUnchanged"]}.items():
    assert sha(r / path) == digest
assert sha(Path(prep["archive"])) == prep["archiveSha256"]
android = load(s / "execution-292.json")
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
actual = native["native"]["actualResult"]
assert sha(Path(actual["log"])) == actual["logSha256"]
codes = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                   Path(actual["log"]).read_text(encoding="utf-8"), re.M)
assert codes == ["1", "0", "1", "0"] and actual["skips"] == 0
route = load(reviews / "batch-053-native" / "attempt-1" / "n1-053-article-route.json")
assert route == actual["route"] and route["archiveRequests"] == 1
assert [route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]] == [1065, 5023, 85, 0]
assert route["acceptedReadingParserEpoch"] == 1 and route["offline"] and not route["phoneEvidence"]
baseline = load(s / "baseline-inventory.json")["files"]
original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
current = {p.stem for p in (r / "kanji").glob("*.md")}
expected = set(state["publicationCheckpoint"]["pilotMembership"])
for path in sorted(s.glob("batch-*-progress.json")):
    ledger = load(path)
    if int(ledger["batch"]) <= 53:
        members = set(ledger["membership"])
        assert not expected & members
        assert ledger["reviewClosed"] == ledger["membership"]
        expected.update(members)
assert current - original == expected and len(expected) == 80
assert original <= current
receipts = load(c / "artifacts" / "execution-296-validation-receipts.json")
for row in receipts:
    assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
tests = (c / "logs" / "execution-296-python-tests.txt").read_text(encoding="utf-8")
assert re.search(r"Ran 368 tests in [\d.]+s\s+OK", tests)
budget = ast.literal_eval((c / "logs" / "execution-296-budget.txt").read_text())
audit = load(s / "batch-053-acceptance-source-audit.json")
limits = (
    "Bounded owner-testing acceptance only; physical-phone/general-release and whole-set outstanding. "
    "Compatible Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection. "
    "Original textual/native/visual reports and failures remain immutable. Initial Claude two internal overlaps, "
    "recovered oversized guide read, GPT nine-versus-actual-eight comparison-word count correction retained. "
    "Actual meaning choices differ from authored trio; no all-pool certification. Native screenshots clipped; "
    "not all columns/fullarticle. Geometry-only reference touches/recall miss, not MLKit recognition/human "
    "successful recall/negative geometry/reverse order. Source-only radical not authored; no new fallback-face "
    "claim. Original294 denial/exact parent recovery/owned helper cleanup preserved. Fresh292Android3+1, "
    "294native2terminal0 and295originalvisual confirmations reverified, NOT rerun. Original049HOSTOOM/"
    "1GiBHOST-onlyheadroom retained; native192m576m/font/archiveguards unchanged."
)
audit.update(
    status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=head,
    latestMainIntegrated=git("rev-parse", "origin/main"), normalMergeResult="Already up to date; no substantive conflict.",
    exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": 368, "failures": 0, "errors": 0},
    validationReceipts=receipts, budget=budget, acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
    originalInitialToolCalls=[56, 58], originalInitialOverlaps=[2, 0],
    originalVisualToolCalls=[28, 28], originalVisualPngReturns=[21, 21], originalVisualOverlaps=[0, 0],
    exactEvidenceCopiesReverified=len(native["evidenceCopies"]), testsRerun=False,
    testBoundary="Current296 Python368 rerun; accepted292Android/294native/295visual evidence reverified without rerun.",
    reviewedTeachingAndRuntimeUnchanged=True, limits=limits,
)
save(s / "batch-053-acceptance-audit.json", audit)
save(s / "execution-296.json", {
    "schemaVersion": 1, "execution": 296, "batch": "053", "status": "combined-tree-locally-accepted-pending-publication",
    "startedHead": head, "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": "batch-053-acceptance-audit.json", "publishedAdditions": 79,
    "remainingAdditions": 1149, "limits": limits,
    "nextAction": "Normal signing/owner fastforward/actual greenCI/every immutable public ZIP runtimehash/terminal receipts/owner issue60 before053 delivery or054.",
})
dest = s / "batch-053-acceptance"
dest.mkdir(exist_ok=False)
for row in receipts:
    shutil.copyfile(Path(row["log"]), dest / Path(row["log"]).name)
for path in [Path(__file__), c / "audit-batch-053-acceptance.py", c / "validate-execution-296.py"]:
    shutil.copyfile(path, dest / path.name)
save(c / "execution-296-local-acceptance.json", {
    "head": head, "pythonTests": 368, "androidCasesReverified": 4,
    "nativeTerminalCodesReverified": [0, 0], "runtimeHashesVerified": 8287,
    "exactLocalAdditions": 80, "publishedAdditions": 79, "remainingAdditions": 1149,
    "limits": limits,
})
print("Combined acceptance passed: Python368; all8287runtime hashes; exact80local additions; Android4/native2 and original reports reverified, not rerun. Publication pending.")
