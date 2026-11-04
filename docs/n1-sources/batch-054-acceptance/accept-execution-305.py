import ast
import copy
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
main = git("rev-parse", "origin/main")
teaching = "4fb51498f6912169499456031380ce2353373397"
assert head == "0fe8e4f8c0804fe41a26bd1ee4f6fc9b0a9c2fa0"
assert main == git("rev-parse", "MERGE_HEAD") == "dfd87ba949dc41493c800411675c44d782482c46"
assert not git("diff", "--name-only", "--diff-filter=U")
upstream = [f"kanji/{ch}.md" for ch in "九四回度"]
delta = git("diff", "--name-only", head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
assert len(delta.splitlines()) == 5
for name in upstream:
    assert (r / name).read_bytes() == subprocess.check_output(["git", "show", f"{main}:{name}"], cwd=r)
assert not git("diff", teaching, "--", "kanji/且.md", "words/且つ.md", "strokes/且.json")
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
state_path = c / "progress.json"
state = load(state_path)
before_state = copy.deepcopy(state)
assert state["checkpoint"] == 304 and state["activeExecution"]["execution"] == 305
native = load(reviews / "batch-054-native-acceptance.json")
reconciliation = load(reviews / "batch-054-reconciliation.json")
assert native["status"] == "native-visual-closed-pending-combined-publication"
assert reconciliation["findings"] == reconciliation["unresolvedConsequentialClaims"] == []
assert not reconciliation["nativeVisualAcceptancePending"]
for key in ["nativeEvidence", "androidEvidence", "nativeFixture"]:
    row = native[key]
    assert sha(r / row["path"]) == row["sha256"]
for row in native["evidenceCopies"]:
    assert sha(r / row["path"]) == row["sha256"] == sha(Path(row["source"]))
for row in reconciliation["reviewProcesses"]:
    label = row["label"]
    assert sha(reviews / f"batch-054-{label}.md") == row["reportSha256"]
    assert sha(reviews / f"batch-054-{label}-execution.json") == row["executionRecordSha256"]
    assert sha(c / f"batch-054-{label}.jsonl") == row["rawExecutionSha256"]
    assert row["exitCode"] == 0
initials = reconciliation["reviewProcesses"]
assert [p["model"] for p in initials] == ["claude-opus-5.5", "gpt-6.1-sol"]
assert datetime.fromisoformat(initials[0]["completedAt"]) < datetime.fromisoformat(initials[1]["startedAt"])
for label, row in zip(["claude", "gpt"], native["originalReviewerVisualProcesses"]):
    assert sha(reviews / f"batch-054-visual-{label}.md") == row["reportSha256"]
    assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
    assert row["exitCode"] == 0 and not row["observedToolOverlaps"] and not row["unfinishedTools"]
    assert len(row["toolCalls"]) == 24 and row["imagePayloadsVerified"] == 18
    for call in row["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
visuals = native["originalReviewerVisualProcesses"]
assert datetime.fromisoformat(visuals[0]["completedAt"]) < datetime.fromisoformat(visuals[1]["startedAt"])
prep = load(s / "batch-054-native-preparation.json")
for path, digest in {**prep["originalFixtureHashesUnchanged"], **prep["originalInitialReportHashesUnchanged"]}.items():
    assert sha(r / path) == digest
assert sha(Path(prep["archive"])) == prep["archiveSha256"]
android = load(s / "execution-301.json")
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
execution = load(s / "execution-303.json")
log = r / execution["nativeRawLog"]
assert sha(log) == execution["rawLogSha256"]
codes = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)\s*$", log.read_text(encoding="utf-8"), re.M)
assert codes == ["1", "0", "1", "0"]
assert execution["nativeExecution"]["terminalSuccessCases"] == 2 and execution["nativeExecution"]["passed"]
route = load(reviews / "batch-054-native" / "attempt-1" / "n1-054-article-route.json")
assert route == execution["productionImportEvidence"] and route["archiveRequests"] == 1
assert [route[k] for k in ["importedKanji", "importedWords", "n1Cards", "problems"]] == [1066, 5024, 86, 0]
assert route["acceptedReadingParserEpoch"] == 1 and route["offline"] and not route["phoneEvidence"]
index = load(reviews / "batch-054-native" / "artifact-index.json")
for row in index["sourceArtifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
baseline = load(s / "baseline-inventory.json")["files"]
original = {Path(p).stem for p in baseline if p.startswith("kanji/")}
current = {p.stem for p in (r / "kanji").glob("*.md")}
expected = set(state["publicationCheckpoint"]["pilotMembership"])
for path in sorted(s.glob("batch-*-progress.json")):
    ledger = load(path)
    if int(ledger["batch"]) <= 54:
        members = set(ledger["membership"])
        assert not expected & members
        assert ledger["reviewClosed"] == ledger["membership"]
        expected.update(members)
assert current - original == expected and len(expected) == 81 and original <= current
receipts = load(c / "artifacts" / "execution-305-validation-receipts.json")
for row in receipts:
    assert row["exitCode"] == 0 and sha(Path(row["log"])) == row["sha256"]
final_log = c / "logs" / "execution-305-source-audit-final.txt"
assert not final_log.exists()
with final_log.open("wb") as stream:
    result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(c / "audit-batch-054-acceptance.py")],
                            cwd=r, stdout=stream, stderr=subprocess.STDOUT)
assert result.returncode == 0, final_log
receipts.append({"check": "source-audit-final",
                 "command": ["python", "-X", "utf8", "-B", str(c / "audit-batch-054-acceptance.py")],
                 "exitCode": result.returncode, "log": str(final_log), "sha256": sha(final_log),
                 "reason": "Qualify mechanical audit's exact-base boundary with the four independently accepted upstream-only bodies; same source/baseline checks, no gate relaxation."})
tests = (c / "logs" / "execution-305-python-tests.txt").read_text(encoding="utf-8")
match = re.search(r"Ran (\d+) tests in [\d.]+s\s+OK", tests)
assert match
test_count = int(match[1])
budget = ast.literal_eval((c / "logs" / "execution-305-budget.txt").read_text())
audit = load(s / "batch-054-acceptance-source-audit.json")
limits = (
    "Bounded owner-testing acceptance only; physical-phone/general-release and whole-set outstanding. "
    "Compatible Android f9b59a2+ required; old clients ignore curation and8000-entry clients reject collection. "
    "Original textual/native/visual reports and failures remain immutable. Initial Claude ONE internal overlap, "
    "GPT zero, complete32resources each; five Claude optional groups not adopted. Comparative register UNVERIFIED "
    "and OMITTED. Visual confirmations24serialcalls/18returnedPNGs each/zerooverlap;1080x2400source resized900x2000, "
    "bytes separately retained. Actual cedar/chicken/mosquito meaning choices differ from authored目日助; no all-pool "
    "certification. Screenshots clipped; not all columns/fullarticle. Geometry-only reference touches/recall miss, "
    "not MLKit recognition/human successful recall/negative geometry/reverse order. 苟 readable shared fallback "
    "actual face unknown, not four bundled designs. Synthetic source/due queues/historical logs, not ownerprogress. "
    "Fresh301Android3+1,303native2terminal0 and304originalvisual confirmations reverified, NOT rerun. "
    "Original049HOSTOOM/1GiBHOST-onlyheadroom retained; native192m576m/font/archiveguards unchanged. "
    "Native versionfa89fc674144b377 remains the actual tested envelope, NOT current merged version8846e9a9dc29d24c. "
    "Four upstream-only article bodies九四回度 are byte-identical to currentmain; no metadata/quiz/app/test changes "
    "or batch054 teaching overlap. No new concern requiring duplicate accepted tests/reviews was established."
)
audit.update(
    status="combined-tree-locally-accepted-pending-publication", integratedHeadBeforeAcceptance=head,
    latestMainIntegrated=main,
    normalMergeResult="Non-rewriting merge; only derived manifest conflict, regenerated. Four upstream bodies preserved verbatim; no substantive teaching conflict.",
    exactLocalAdditionMembership=sorted(expected), pythonTests={"passed": test_count, "failures": 0, "errors": 0},
    validationReceipts=receipts, budget=budget, acceptedAndroidCases=4, acceptedNativeTerminalCodes=[0, 0],
    originalInitialToolCalls=[56, 55], originalInitialOverlaps=[1, 0],
    originalVisualToolCalls=[24, 24], originalVisualPngReturns=[18, 18], originalVisualOverlaps=[0, 0],
    evidenceCopiesReverified=len(native["evidenceCopies"]), nativeSourceArtifactsReverified=len(index["sourceArtifacts"]),
    acceptedAndroidNativeTestsRerun=False, reviewedBatchTeachingUnchanged=True,
    testBoundary=f"Current305 Python{test_count} rerun; accepted301Android/303native/304visual evidence reverified without rerun.",
    nativeContentVersion=route["contentVersion"], mergedContentVersion="8846e9a9dc29d24c", limits=limits,
)
save(s / "batch-054-acceptance-audit.json", audit)
save(s / "execution-305.json", {
    "schemaVersion": 1, "execution": 305, "batch": "054", "status": "combined-tree-locally-accepted-pending-publication",
    "startedHead": head, "integratedMain": main, "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": "batch-054-acceptance-audit.json", "publishedAdditions": 80,
    "remainingAdditions": 1148, "limits": limits,
    "nextAction": "Normal signing/owner fastforward/actual greenCI/every immutable public ZIP runtimehash/terminal receipts/owner issue60 before054 delivery or055.",
})
dest = s / "batch-054-acceptance"
dest.mkdir(exist_ok=False)
for row in receipts:
    shutil.copyfile(Path(row["log"]), dest / Path(row["log"]).name)
for path in [Path(__file__), c / "audit-batch-054-acceptance.py", c / "audit-batch-054-draft.py",
             c / "validate-execution-305.py"]:
    shutil.copyfile(path, dest / path.name)
state["activeExecution"].update(status="combined-tree-locally-accepted-pending-normal-signing",
                                integratedMain=main, currentContentVersion="8846e9a9dc29d24c",
                                pythonTests=test_count)
state["stage"] = "batch-054-combined-accepted-pending-normal-signing"
assert all(state[k] == v for k, v in before_state.items() if k not in {"activeExecution", "stage"})
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Combined acceptance passed: Python{test_count};8290runtime hashes; exact81local additions; Android4/native2/reviews reverified, not rerun. Publication pending.")
