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
teaching = "4dba935415312d39b1c2defdc05b938d37fe21f0"
assert head == "7f465a9dff08c9365ce6a32300280d8428fa979f"
assert main == "9b5e9fd9f596801eb78078ab14e4c4b35973479d"
assert subprocess.run(["git", "merge-base", "--is-ancestor", main, head], cwd=r).returncode == 0
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
state_path = c / "progress.json"
state = load(state_path)
assert state["checkpoint"] == 328 and state["activeExecution"]["execution"] == 329
native = load(reviews / "batch-056-native-acceptance.json")
reconciliation = load(reviews / "batch-056-reconciliation.json")
assert native["status"] == "native-and-original-two-family-bounded-visual-closed-pending-combined-main-publication"
assert reconciliation["findings"] == reconciliation["unresolvedConsequentialClaims"] == []
initials = reconciliation["reviewProcesses"]
assert [p["model"] for p in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
for row in initials:
    label = row["label"]
    assert row["exitCode"] == 0 and not row["observedInternalOverlaps"]
    assert sha(reviews / f"batch-056-{label}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-056-{label}-execution.json") == row["executionRecordSha256"]
    assert sha(c / f"batch-056-{label}.jsonl") == row["rawExecutionSha256"]
assert [p["toolCalls"] for p in initials] == [65, 68]
visuals = []
for label, initial, calls, images, overlaps in [
    ("claude", initials[0], 33, 24, 1),
    ("gpt", initials[1], 33, 24, 0),
    ("claude-clarification", initials[0], 3, 2, 0),
]:
    row = load(reviews / f"batch-056-visual-{label}-execution.json")
    assert row["sessionId"] == initial["sessionId"]
    assert row["actualModels"] == [initial["model"]] and row["exitCode"] == 0
    assert len(row["observedToolOverlaps"]) == overlaps and not row["unfinishedTools"]
    assert len(row["toolCalls"]) == calls and row["imagePayloadsVerified"] == images
    assert sha(reviews / f"batch-056-visual-{label}.md") == row["reportSha256"]
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
android = load(s / "execution-320.json")
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
execution = load(s / "execution-326.json")
log = r / execution["nativeRawLog"]
assert sha(log) == execution["rawLogSha256"]
codes = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$",
                   log.read_text(encoding="utf-8"), re.M)
assert codes == ["1", "0", "1", "0"]
assert execution["nativeExecution"]["terminalSuccessCases"] == 2
assert execution["nativeExecution"]["passed"] and execution["nativeExecution"]["ownedHelperStopped"]
route = load(reviews / "batch-056-native" / "attempt-3-retry2" / "n1-056-article-route.json")
assert route == execution["productionImportEvidence"] == native["nativeResult"]
assert route["archiveRequests"] == 1
assert [route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]] == [1068, 5027, 88, 0]
assert route["acceptedReadingParserEpoch"] == 1 and route["offline"] and not route["phoneEvidence"]
assert route["fullOnyomi"] == ["ボウ"] and route["fullKunyomi"] == ["とぼ.しい", "とも.しい"]
assert route["quizOnKeys"] == ["ぼう"] and route["quizKunKeys"] == ["とぼしい"]
artifact_counts = {}
for number in [322, 324, 326]:
    index = load(reviews / "batch-056-native" / f"execution-{number}-artifact-index.json")
    rows = index["sourceArtifacts"] if number == 322 else index["files"]
    for row in rows:
        assert sha(r / row["path"]) == row["sha256"]
    artifact_counts[str(number)] = len(rows)
assert artifact_counts == {"322": 13, "324": 24, "326": 63}
archival = load(s / "execution-327.json")
assert sha(r / archival["originalNativeRecord"]) == archival["originalNativeRecordSha256"]
assert sha(r / archival["parentCleanupRecoveryArchive"]) == archival["parentCleanupRecoveryArchiveSha256"]
baseline = load(s / "baseline-inventory.json")["files"]
original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
current = {p.stem for p in (r / "kanji").glob("*.md")}
expected = set(state["publicationCheckpoint"]["pilotMembership"])
for path in sorted(s.glob("batch-*-progress.json")):
    ledger = load(path)
    if int(ledger["batch"]) <= 56:
        members = set(ledger["membership"])
        assert not expected & members
        assert ledger["reviewClosed"] == ledger["membership"]
        expected.update(members)
assert current - original == expected and len(expected) == 83 and original <= current
receipts = load(c / "artifacts" / "execution-329-validation-receipts.json")
for row in receipts:
    assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
tests = (c / "logs" / "execution-329-python-tests.txt").read_text(encoding="utf-8")
match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
assert match
test_count = int(match[1])
budget = ast.literal_eval((c / "logs" / "execution-329-budget.txt").read_text())
limits = (
    "Bounded owner-testing only; physical-phone/general-release and whole-set outstanding. Android f9b59a2+ required. "
    "Original blind Claude65calls/GPT68calls, zero internal overlaps; all39assignedresources returned each, "
    "64completefamilies/15comparisonwords; Claude14word-count misstatement and failed fresh lookup retained. "
    "Three Claude optional suggestions not adopted; ともしい frequency/register UNVERIFIED, not claimed or practiced. "
    "Original-session visuals33/33/3calls and24/24/2actual PNGpayloads; ClaudeONE internal two-image overlap retained, "
    "GPT/clarificationzero. Original inaccurate universal visibility/choice identity/grade statements withdrawn by "
    "same-session supplement, complete reports retained. 54sourcePNGs/24distinct/30equivalentcopies; "
    "1080x2400sources returned900x2000, both byte sets preserved. Bounded viewports/table clipping, "
    "not every-cell/full-article evidence. Four production-font rows show乏久反乃 distinct and丿饉飢饉 readable; "
    "actual fallback face unknown. Actual meaning choices scarce;lacking/whale/handle;dealwith/thereupon;possessiveno "
    "include乃, not established之; not complete authored久反乃 trio or all-pool quiz certification. "
    "Meaning feedback exits Back without persistence; BOTH curated Good logs and DrawAgain after Next. "
    "Four reference-touch strokes/ungraded trace/geometric-only model unavailable/recall miss NOTMLKit/"
    "correct human recall/negative geometry/reverse order evidence. Synthetic source/queues/logs, not ownerprogress. "
    "Original322twofailures/324glyph0article-2/326denial and parentEXACTcleanupverificationexit0 retained. "
    "Original049HOST512MiBOOM/existing1GiBHOSTcoreTest-only/native192m576m/font/archive guards unchanged. "
    "Current main9b5e9fd already ancestral; no new runtime/teaching merge delta or concern requiring duplicate tests."
)
audit = load(s / "batch-056-acceptance-source-audit.json")
audit.update(
    status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=head,
    latestMainIntegrated=main, normalMergeResult="Fresh fetch and normal merge: already up to date; no conflicts.",
    exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": test_count, "failures": 0, "errors": 0},
    validationReceipts=receipts, budget=budget, acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
    originalInitialToolCalls=[65, 68], originalInitialOverlaps=[0, 0],
    originalVisualToolCalls=[33, 33, 3], originalVisualPngReturns=[24, 24, 2],
    originalVisualOverlaps=[1, 0, 0], indexedNativeArtifactsReverified=artifact_counts,
    acceptedAndroidNativeTestsRerun=False, reviewedBatchTeachingUnchanged=True,
    nativeContentVersion=route["contentVersion"], mergedContentVersion=load(r / "manifest.json")["contentVersion"],
    limits=limits,
)
save(s / "batch-056-acceptance-audit.json", audit)
save(s / "execution-329.json", {
    "schemaVersion": 1, "execution": 329, "batch": "056",
    "status": "combined-tree-locally-accepted-pending-publication",
    "startingHead": head, "integratedMain": main, "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": "batch-056-acceptance-audit.json", "publishedAdditions": 82,
    "remainingAdditions": 1146, "limits": limits,
    "nextAction": "Normal signing/owner fastforward/terminalgreenCI/every immutable public ZIP runtimehash/terminal receipts/owner issue60 before056 delivery or057.",
})
dest = s / "batch-056-acceptance"
dest.mkdir(exist_ok=False)
for row in receipts:
    shutil.copyfile(Path(row["log"]), dest / Path(row["log"]).name)
for path in [Path(__file__), c / "audit-batch-056-acceptance.py", c / "execution-318.py",
             c / "validate-execution-329.py", c / "start-execution-329.py"]:
    shutil.copyfile(path, dest / path.name)
state["activeExecution"].update(status="combined-tree-locally-accepted-pending-normal-signing",
                                integratedMain=main, pythonTests=test_count)
state["stage"] = "batch-056-combined-accepted-pending-normal-signing"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Combined acceptance: Python{test_count};8297runtime hashes; exact83local additions; Android4/native2/reviews reverified, not rerun. Publication pending.")
