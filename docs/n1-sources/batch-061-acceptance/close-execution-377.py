import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
N = V / "batch-061-native"
START = "f2267727d982589890b2f4ae0b17e82666337956"
TEACHING = "2567f5e7b3888f2df3ed560f618341266b471902"
STATUS = "bounded-native-visual-reconciled-pending-combined-main-publication"
LABELS = ("claude", "claude-glyph", "claude-selection", "gpt")
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution377.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=R):
    return subprocess.check_output(["git", "--no-pager", "-c", "core.quotepath=false", *args], cwd=tree, text=True, encoding="utf-8").strip()


def audit():
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    android = C.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", tree=android)
    freeze = load(C / "batch-061-visual-freeze.json")
    assert sha(N / "execution-376-artifact-index.json") == freeze["artifactIndexSha256"]
    for row in freeze["files"]:
        assert sha(Path(row["path"])) == row["sha256"]
    index = load(N / "execution-376-artifact-index.json")
    for row in index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
        assert (R / row["path"]).stat().st_size == row["bytes"]
    native = load(S / "execution-376.json")
    assert native["nativeAssertionsPassed"] and not native["independentVisualAcceptance"]
    raw = (N / "attempt-1" / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "Time: 108.92" in raw and "OK (2 tests)" in raw
    route = load(N / "attempt-1" / "n1-061-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1 and not route["phoneEvidence"]
    assert [route[x] for x in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1073, 5031, 93, 0, 1]
    assert route["contentVersion"] == "d01d660cc41262fe"
    assert route["fullOnyomi"] == ["ハイ"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["はい"] and route["quizKunKeys"] == []
    assert route["touchInjectedReferenceStrokes"] == 10
    assert all(route[x] for x in (
        "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
        "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
        "drawingGradeRecordedOnNext", "offline",
    ))
    android_evidence = load(S / "execution-374.json")
    for row in android_evidence["archivedArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    for row in android_evidence["recovery"]["tests"]:
        for path in (Path(row["sourcePath"]), Path(row["artifactPath"])):
            assert sha(path) == row["sha256"]
            suite = ET.parse(path).getroot()
            assert int(suite.attrib["tests"]) == row["tests"]
            assert all(int(suite.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
            assert suite.attrib["timestamp"] == row["timestamp"]
            assert sorted(x.attrib["name"] for x in suite.findall("testcase")) == sorted(row["caseNames"])
    for row in android_evidence["provenance"]:
        assert sha(Path(row["path"])) == row["sha256"]
    original = load(V / "batch-061-initial-review-checkpoint.json")
    for row in original["reviewProcesses"]:
        prefix = "batch-061-" + row["label"]
        for suffix, key in (
            (".md", "reportSha256"), ("-execution.json", "executionRecordSha256"),
            ("-coverage.json", "coverageRecordSha256"),
        ):
            assert sha(V / (prefix + suffix)) == row[key]
        assert sha(C / (prefix + ".jsonl")) == row["rawExecutionSha256"]
    assert sha(V / "batch-061-reconciliation.json") == android_evidence["reconciliationSha256"]
    processes = [load(V / f"batch-061-visual-{label}-execution.json") for label in LABELS]
    assert [p["actualModels"] for p in processes] == [["claude-opus-5.5"]] * 3 + [["gpt-6.1-sol"]]
    assert [len(p["toolCalls"]) for p in processes] == [31, 1, 1, 30]
    assert [p["imagePayloadsVerified"] for p in processes] == [20, 1, 1, 20]
    assert [len(p["observedToolOverlaps"]) for p in processes] == [1, 0, 0, 0]
    assert [len(p["multiToolResponses"]) for p in processes] == [1, 0, 0, 0]
    for prior, following, label in zip(processes, processes[1:], LABELS):
        assert datetime.fromisoformat(prior["completedAt"]) < datetime.fromisoformat(following["startedAt"])
        for suffix in (".md", "-execution.json"):
            assert (V / f"batch-061-visual-{label}{suffix}").stat().st_mtime < datetime.fromisoformat(following["startedAt"]).timestamp()
    for label, process in zip(LABELS, processes):
        assert process["exitCode"] == 0 and not process["unfinishedTools"]
        assert process["expectedPngMembershipReturned"]
        assert sha(V / f"batch-061-visual-{label}.md") == process["reportSha256"]
        assert sha(C / f"batch-061-visual-{label}.jsonl") == process["rawExecutionSha256"]
        assert process["usage"]["currentModel"] == process["actualModels"][0]
        assert len(process["terminalResults"]) == 1 and process["terminalResults"][0]["exitCode"] == 0
        assert process["terminalResults"][0]["sessionId"] == process["sessionId"]
        disabled = "\n".join(x["message"] for x in process["configurationEvidence"])
        assert all(x in disabled for x in ("powershell", "task", "web_fetch", "write_agent"))
        for call in process["toolCalls"]:
            assert call["name"] == "view" and call["success"] and not call["truncationOrLimitMarker"]
            if "imagePayload" in call:
                image = call["imagePayload"]
                assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
                assert image["sourceDimensions"] == [1080, 2400] and image["returnedDimensions"] == [900, 2000]
                assert not image["exactFileBytesReturnedToModel"]
            else:
                assert call["exactRequestedTextContainedInResult"]
    return index, processes


NEXT = (
    "SAME061 bounded original-session two-family native visual review reconciled; signed LOCAL evidence checkpoint377 only, "
    "NOT runtime publication or retroactive strict process acceptance. OriginalClaude537a357b actualclaude-opus-5.5 "
    "then supervised singlefont/singleselection turns THEN originalGPT89aec53d actualgpt-6.1-sol ALLexited0SERIAL; "
    "complete report/audit archived before every next launch. Both families20distinctPNGpayloads/fourcompletearticles/"
    "fixture54-148,150-270,271-350,351-430. Claudevisual061-P3 ONEpairedfont+selectionresponse/ONEoverlap remainshistorical; "
    "two separatelyexiting ONEimageprocesses prospectivelyreconfirm both resources; GPT30views/ZEROoverlaps/multitoolresponses. "
    "42actual900x2000modelpayloads separatelyarchived from40source1080x2400PNGs/20distinct/20equivalent. "
    "Both allfour boundedteachingscopes threefacetsCLEAN/no newactionableteachingorvisibletaskdefect. "
    "Claudeglyphclarification corrects itsfontstyledescription, NOTteaching. Fourfontrows actual俳非悲借優人亻昔心句憂/"
    "俳句/俳優 readable/distinct/no blankboxes; fallbackfaceunknown. Actualmeaningchoices translate;explanation/silkworm/"
    "haiku;actor/tree;establish; onoptionsナイハンツイハイ. Tablecroppedoffscreen/unseenpixels NOTwholearticlecertification. "
    "Originalreports/372textualclosure/Claude061-P1/P2 and newP3 processnoncompliance preserved; supervisedremediation "
    "NOTretroactivestrictacceptance. Accepted374freshAndroid3+1 and376native2case0/noskips108.92s/fullContentSyncONCE"
    "1073kanji5031words93N1/d01d660cc41262fe/problems0/epoch1/Full+Liteハイ/emptykun/curatedはい/no-kun/"
    "THREEpairsSIXdirections/SystemBack/offline/meaningBackwithoutNext/solecuratedOnGood/tenreference-touchstrokes/"
    "ungradedtrace/recallmiss/persistedDrawAgain retained without rerun. NOTMLKit/correcthumanrecall/phone. "
    "NEXTboundedcheckpoint latestorigin/main fetch/normalnonrewritingmerge, surgicalconflicts/reviewsubstantiveteaching; "
    "ALLcombined frozen-source/baseline/exactmembership/originalguards/readings/links/strokes/fonts/currentPython/"
    "vocabulary/validator/freshmanifest/18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normalsigning/"
    "ownerfastforward/exactremoteSHA/terminalgreenCI/EVERYimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 "
    "BEFOREdelivery or062. No accepted374Android/376native/initialreview/visual rerun absent new concern. "
    "Original373permissiondenial and049HOST512MiBOOM/qualifiedhost-only1GiBinit unchanged. Actualpermissiondenial/"
    "signingwait preserveexactcommand-error/report/yield, no retry/workaround. Preserve FULLlivehistory/"
    "no062/secondrunner/concurrentheavywork/supervisorchanges. Published87/1228,1141remaining latest060af7bae60unchanged; "
    "compatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)
LIMITS = (
    "Dependent original-session visual confirmation, not new blind initial or fresh upstream dictionary review. "
    "Operational hashes/XML/logs reverified by coordinator, not reviewer-executed. Drawing reference-touch trace/recallmiss "
    "is not MLKit or successful human recall. Unseen cells/pixels and unidentified fallback face remain limits. "
    "Resumed-session usage is cumulative, not current-turn cost. Historical061-P1/P2/P3 process noncompliance remains explicit. "
    "No runtime publication, physical-phone/general-release or whole-set acceptance."
)


def main():
    progress = load(C / "progress.json")
    before = load(C / "execution-377-starting-progress.json")
    assert progress["checkpoint"] == 376 and progress["batch"] == "061"
    index, processes = audit()
    if sys.argv[1] == "restage":
        record_path = S / "execution-377.json"
        record = load(record_path)
        archived_script = N / "visual-receipts" / Path(__file__).name
        shutil.copyfile(Path(__file__), archived_script)
        for row in record["archivedExecutionReceipts"]:
            if row["path"] == str(archived_script.relative_to(R)):
                row["sha256"] = sha(archived_script)
            else:
                assert sha(R / row["path"]) == row["sha256"]
        record["whitespaceCheck"] = "Authored files pass. Exact installed model-catalog capture retains the original final blank line; raw control/archive bytes are equal and hashed, not normalized."
        save(record_path, record)
        subprocess.run(["git", "add", "--", str(archived_script.relative_to(R)), str(record_path.relative_to(R))], cwd=R, check=True)
        subprocess.run(["git", "diff", "--cached", "--check", "--", ".",
                        ":(exclude)docs/n1-reviews/batch-061-native/visual-receipts/batch-061-visual-model-catalog-execution-377.txt"], cwd=R, check=True)
        inventory = git("diff", "--cached", "--name-only").splitlines()
        save(C / "execution-377-staged-inventory.json", inventory)
        print(f"Staged {len(inventory)} bounded evidence files; exact raw catalog final blank line preserved; authored whitespace check passes.")
        return
    if sys.argv[1] == "finish":
        saved = git("rev-parse", "HEAD")
        assert git("rev-parse", "HEAD^") == START
        assert git("log", "-1", "--format=%G?") == "G"
        assert not git("status", "--porcelain")
        assert not git("diff", START, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json")
        record_path = S / "execution-377.json"
        checkpoint = {
            "schemaVersion": 1, "execution": 377, "checkpoint": 377, "batch": "061", "status": STATUS,
            "savedCommit": saved, "signature": "G", "record": str(record_path.relative_to(R)),
            "recordSha256": sha(record_path), "nextAction": NEXT,
            "recordedAt": datetime.now().astimezone().isoformat(),
            "publishedAdditions": 87, "remainingAdditions": 1141,
            "publicationAttempted": False, "nativeRerun": False, "androidRerun": False,
            "boundedIndependentVisualAcceptance": True,
            "strictHistoricalProcessContractAccepted": False,
        }
        progress.update(
            checkpoint=377, status="continue",
            stage="batch-061-bounded-native-visual-reconciled-pending-combined-main-publication",
            blocker=None, nextAction=NEXT,
        )
        progress["execution377StartingState"]["status"] = "signed-bounded-native-visual-checkpoint-complete"
        progress["execution377CoordinatorCheckpoint"] = checkpoint
        progress["batch061NativeVisualCheckpoint"] = checkpoint.copy()
        mutable = {"checkpoint", "status", "stage", "blocker", "nextAction"}
        assert all(progress[k] == v for k, v in before.items() if k not in mutable)
        save(C / "progress.json", progress)
        verification = {
            **checkpoint, "dedicatedWorktreesClean": True, "runtimeUnchanged": True,
            "historicalRecordsCompared": len(before) - len(mutable),
            "fullHistoricalProgressPreserved": True,
            "nativeArtifactHashesReverified": len(index["files"]),
            "actualReturnedImagePayloadsVerified": 42, "reviewerProcessesExited": True,
            "wholeProjectComplete": False, "changedPaths": load(C / "execution-377-staged-inventory.json"),
        }
        save(C / "execution-377-final-verification.json", verification)
        print(f"Checkpoint377 persisted: signed G {saved}; continue SAME061 combined-main acceptance next.")
        return
    assert sys.argv[1] == "stage"
    assert git("rev-parse", "HEAD") == START and git("log", "-1", "--format=%G?") == "G"
    record_path = S / "execution-377.json"
    acceptance_path = V / "batch-061-native-acceptance.json"
    assert not record_path.exists() and not acceptance_path.exists()
    checks = []
    for args in (["tools\\validate.py"], ["tools\\build_manifest.py"], ["tools\\check_content_budget.py"]):
        result = subprocess.run(["python", "-X", "utf8", "-B", *args], cwd=R, text=True, encoding="utf-8", capture_output=True)
        check = {"command": ["python", "-X", "utf8", "-B", *args], "exitCode": result.returncode,
                 "stdout": result.stdout, "stderr": result.stderr}
        checks.append(check)
        assert result.returncode == 0, check
    assert not git("diff", "--", "manifest.json")
    receipts = N / "visual-receipts"
    receipts.mkdir()
    names = [
        "batch-061-visual-task.txt", "batch-061-visual-freeze.json",
        "batch-061-visual-claude-glyph-task.txt", "batch-061-visual-claude-selection-task.txt",
        "run-batch-061-visual.ps1", "run-batch-061-visual-single.ps1",
        "archive-batch-061-visual.py", "prepare-execution-377.py", "close-execution-377.py",
        "start-execution-377.py", "batch-061-visual-help-execution-377.txt",
        "batch-061-visual-model-catalog-execution-377.txt",
    ]
    for label in LABELS:
        names.extend(f"batch-061-visual-{label}{suffix}" for suffix in ("-process.json", "-usage.json", "-stderr.txt"))
    archived = []
    for name in names:
        target = receipts / name
        shutil.copyfile(C / name, target)
        archived.append({"path": str(target.relative_to(R)), "sha256": sha(target)})
    reviews = []
    for label, process in zip(LABELS, processes):
        report = V / f"batch-061-visual-{label}.md"
        execution = V / f"batch-061-visual-{label}-execution.json"
        reviews.append({
            "model": process["actualModels"][0], "sessionId": process["sessionId"],
            "report": report.name, "reportSha256": sha(report),
            "execution": execution.name, "executionSha256": sha(execution),
            "toolCalls": len(process["toolCalls"]), "imagePayloads": process["imagePayloadsVerified"],
            "overlaps": len(process["observedToolOverlaps"]),
            "multiToolResponses": len(process["multiToolResponses"]), "exitCode": process["exitCode"],
            "startedAt": process["startedAt"], "completedAt": process["completedAt"],
            "freshScope": (
                "Exactly one font-pairs PNG; original report's style description corrected."
                if label == "claude-glyph" else
                "Exactly one selection PNG; original visible selection judgment retained."
                if label == "claude-selection" else
                "Own initial report, complete俳/俳句/俳優/優, fixture54-148/150-270/271-350/351-430,20distinctPNGpayloads; Claude also own latest supervised lexical confirmation."
            ),
        })
    verdicts = {
        scope: dict(correctness="CLEAN", scopedCoverage="CLEAN", comprehensibility="CLEAN")
        for scope in ("kanji/俳.md", "words/俳句.md:changed-link-and-coupled-context",
                      "words/俳優.md:changed-link-and-coupled-context", "kanji/優.md:added-link-and-coupled-context")
    }
    acceptance = {
        "schemaVersion": 1, "execution": 377, "batch": "061", "status": STATUS,
        "snapshot": START, "reviewedTeachingSnapshot": TEACHING,
        "nativeEvidence": "n1-sources/execution-376.json", "nativeEvidenceSha256": sha(S / "execution-376.json"),
        "textualReconciliation": "batch-061-reconciliation.json",
        "textualReconciliationSha256": sha(V / "batch-061-reconciliation.json"),
        "reviewers": reviews, "verdicts": verdicts, "findings": [], "newActionableDefects": [],
        "processReconciliation": [{
            "id": "061-P3", "status": "partially resolved",
            "originalEvidence": "Claude visual report used one two-image response/font-pairs+selection, with one observed overlapping tool start. Original complete report/execution preserved. Archival assertion correctly failed and stopped subsequent launch.",
            "remediation": "Two separately exiting original-session processes each had exactly ONE image view and zero overlaps/multi-tool responses. Both complete reports and audits archived before GPT launch. Prospective resource-bound remediation complete; original strict process violation irreversible.",
        }],
        "reportCorrection": {
            "status": "resolved", "kind": "understated-font-style-differences",
            "resolution": "Original Claude visual report said only Textbook was clearly different. One-image original-session clarification explicitly identifies four different stroke styles. Readability/distinguishability judgments retained; no teaching edit. Actual fallback face remains unknown.",
        },
        "optional": [{
            "origin": "claude", "status": "optional", "claim": "One俳優 link wraps between its two characters.",
            "disposition": "Nonblocking paragraph wrapping; no demonstrated teaching defect or unrelated UI change.",
        }],
        "coordinatorAdjudication": [
            "Both reviews retain inherited textual correctness/coverage with new bounded screenshot comprehension evidence. No new actionable defect established; no teaching edits.",
            "Claude's complete-row wording is bounded by the separate actor-backlink capture showing the entireハイ row. The kanji-no-kun viewport clips the label and is not whole-table certification.",
            "Claude's six-link visual prose is conservatively limited: native fixture/raw route proves six transitions; static screenshots corroborate selected page regions, not tap chronology or every intermediate landing.",
            "GPT's source/destination separation and cropped-cell qualification are accepted. Static screenshot names and byte hashes do not prove comprehension.",
            "Original061-P1/P2 remain historical per unchanged372 reconciliation. New061-P3 has prospective supervised remediation, not retroactive strict process acceptance.",
            "No new actionable teaching finding unique to either family. Claude report-style correction and cosmetic optional do not establish a general model ranking.",
        ],
        "glyphObservation": "Fourproductionfontrows俳非悲借優 distinct; actual人亻昔心句憂/俳句/俳優 readable/no blankboxes. Actual人/亻 and非/昔 distinct; fourstroke styles visible; fallbackfaceunknown.",
        "actualMeaningOptions": ["translate; explanation", "silkworm", "haiku; actor", "tree; establish"],
        "actualOnOptions": ["ナイ", "ハン", "ツイ", "ハイ"],
        "pngAccounting": {
            "sourceFiles": 40, "distinctSourceHashes": 20, "equivalentCopies": 20,
            "sourceDimensions": [1080, 2400], "returnedDimensions": [900, 2000],
            "actualReturnedPayloadCopies": 42, "exactSourceBytesReturned": False,
        },
        "nativeAssertionsPassed": True, "boundedIndependentVisualAcceptance": True,
        "strictHistoricalProcessContractAccepted": False, "strictFirstVisualProcessContractAccepted": False,
        "prospectiveSupervisedRemediationAccepted": True,
        "wholeArticlePixelCoverage": False, "physicalPhoneAcceptance": False,
        "generalReleaseAcceptance": False, "publicationAttempted": False, "wholeSetAcceptance": False,
        "limits": LIMITS,
    }
    save(acceptance_path, acceptance)
    record = {
        **load(C / "execution-377-start.json"), "schemaVersion": 1, "status": STATUS,
        "recordedAt": datetime.now().astimezone().isoformat(),
        "acceptance": str(acceptance_path.relative_to(R)), "acceptanceSha256": sha(acceptance_path),
        "nativeArtifactHashesReverified": len(index["files"]),
        "originalReportsAndReconciliationReverified": True, "freshAndroidNamedCasesReverified": 4,
        "freshAndroidSkipped": 0, "nativeTerminalCaseStatusesReverified": [0, 0],
        "nativeRerun": False, "androidRerun": False, "teachingChanged": False,
        "reviewerProcessesSerialAndExited": True, "reportAndAuditArchivedBeforeEveryNextProcess": True,
        "newVisualOverlaps": 1, "newVisualMultiToolResponses": 1,
        "sourcePngCount": 40, "distinctPngCount": 20, "actualModelPayloadCopiesVerified": 42,
        "coordinatorDirectImageReadsThisExecution": [
            "n1-061-font-pairs.png", "n1-061-meaning-question.png",
            "n1-061-kanji-no-kun.png", "n1-061-actor-backlink.png",
        ],
        "historicalProcessNoncompliancePreserved": True, "validation": checks,
        "archivedExecutionReceipts": archived,
        "executionScriptBoundary": "Archived launcher includes GPT preflight checks added after Claude's first visual process, before GPT launch; invocation flags unchanged. Archived audit includes single-image label handling added after first strict serialization assertion failure. Original first execution and its exact observed breach remain immutable in the raw log/audit.",
        "strictHistoricalProcessContractAccepted": False,
        "boundedIndependentVisualAcceptance": True, "runtimePublished": False,
        "publishedAdditions": 87, "remainingAdditions": 1141,
        "limits": LIMITS, "nextAction": NEXT,
    }
    save(record_path, record)
    ledger_path = S / "batch-061-progress.json"
    ledger = load(ledger_path)
    ledger.update(
        status=STATUS, nativeVisualCheckpoint="execution-377.json",
        nativeAcceptance="docs/n1-reviews/batch-061-native-acceptance.json",
        boundedIndependentVisualAcceptance=True, strictFirstVisualProcessContractAccepted=False,
        prospectiveSupervisedVisualRemediationAccepted=True, limits=LIMITS, nextAction=NEXT,
    )
    save(ledger_path, ledger)
    paths = [
        "docs\\n1-authoring-notes.md", "docs\\n1-sources\\batch-061-progress.json",
        "docs\\n1-sources\\execution-377.json", str(acceptance_path.relative_to(R)),
    ]
    paths.extend(str(path.relative_to(R)) for path in receipts.rglob("*") if path.is_file())
    for label in LABELS:
        paths.extend(str((V / f"batch-061-visual-{label}{suffix}").relative_to(R)) for suffix in (".md", "-execution.json"))
        paths.extend(str(path.relative_to(R)) for path in (N / f"visual-{label}-returned").glob("*.png"))
    assert len(paths) == len(set(paths))
    subprocess.run(["git", "add", "--", *paths], cwd=R, check=True)
    inventory = git("diff", "--cached", "--name-only").splitlines()
    assert set(inventory) == {path.replace("\\", "/") for path in paths}
    subprocess.run(["git", "diff", "--cached", "--check", "--", ".",
                    ":(exclude)docs/n1-reviews/batch-061-native/visual-receipts/batch-061-visual-model-catalog-execution-377.txt"], cwd=R, check=True)
    save(C / "execution-377-staged-inventory.json", inventory)
    print(f"Staged {len(inventory)} bounded evidence files; runtime/manifest unchanged; validators and budgets pass.")


main()
