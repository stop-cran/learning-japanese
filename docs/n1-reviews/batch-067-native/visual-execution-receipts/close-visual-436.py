import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
HEAD = "a6c57b57f7c90f5a9c78e5bdf953bd2df768d5ed"
TEACHING = "5cb2ea4bc804ac218b17d5c583d4fba95e60971c"
NEXT = (
    "SAME067 signed bounded visual checkpoint436: ORIGINAL Claude0d237a1b and GPTab7f642d "
    "dependent visual confirmations complete; each34calls/23distinct sourcePNG,46actual "
    "returned900x2000payloads from37sourcecapture names, complete3teachingfiles/518linefixture/"
    "terminal-log/route. Read docs\\n1-sources\\execution-436.json and "
    "docs\\n1-reviews\\batch-067-visual-reconciliation.json. No actionable teaching/rendering "
    "defect established; no teaching/app changes. Reviewer PROCESSES entirely serial and exited. "
    "Claude initial visual execution had ONE disclosed two-call overlap of the two small log/route "
    "receipts; original remains processAndCoverageAccepted=false, not rewritten or called fully "
    "serial. Same-session bounded repair reread exactly those two receipts serially before GPT; "
    "supplement archived. All46 image calls serial; GPT34calls fullyserial. Preserve this process "
    "exception and original reports. Viewport/table/fallbackface/MLKit/humanrecall/phone limits "
    "remain; actual N1 meaning options differ from authored増/値/倍 and are visibly wrong for僧. "
    "Authored-choice native presentation NOT certified. Accepted435native2terminal0/138.141s and "
    "433freshAndroid3+1 inherited without rerun; no redundant reviewer/native/Gradle absentnewconcern. "
    "Historicaldenials/HOSTOOMs retained; qualifiedHOST-only2GiBinit NEVER nativebuilds. NEXT bounded "
    "checkpoint: freshfetchlatestorigin/main/nonrewritingintegration as needed, allactualcombined "
    "source-membership/baseline/reading/link/font/stroke/Python/vocab/validator/freshmanifest and "
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudget gates; normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/EVERYimmutablepublicZIP runtimehash/budgets/"
    "ownerissue60 BEFOREdelivery or068. Permissiondenial/signingwait: preserve precise failure "
    "and yield, no retry/workaround/secondrunner/concurrentheavywork/supervisorchanges. "
    "PreserveFULLlivehistory. Published93/1228,1135remain/latest066f0b318eb; local067 NOTdelivered. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
    "Overallproject incomplete."
)
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == value


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), *args], encoding="utf-8").strip()


def verify():
    freeze = load(C / "batch-067-visual-freeze.json")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for key in ("teachingHashes", "originalReportHashes"):
        for path, digest in freeze[key].items():
            assert sha(R / path) == digest
    index = V / "batch-067-native" / "execution-435-artifact-index.json"
    assert sha(index) == freeze["nativeArtifactIndexSha256"]
    for row in load(index)["files"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"]
    records = {}
    for family in ("claude", "gpt"):
        prefix = "batch-067-visual-" + family
        record = load(V / f"{prefix}-execution.json")
        assert record["exitCode"] == 0
        assert record["actualModels"] == [record["requestedModel"]] == [record["usage"]["currentModel"]]
        assert not record["missingRequiredText"] and not record["unexpectedReadPaths"] and not record["unfinishedTools"]
        assert record["imagePayloadsVerified"] == 23 and record["expectedPngMembershipReturned"]
        assert len(record["toolCalls"]) == 34
        assert sha(V / f"{prefix}.md") == record["reportSha256"]
        assert sha(Path(record["rawExecutionLocation"])) == record["rawExecutionSha256"]
        for row in record["toolCalls"]:
            assert row["name"] == "view" and row["success"]
            if "imagePayload" in row:
                payload = row["imagePayload"]
                assert sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
                assert sha(Path(row["arguments"]["path"])) == payload["sourceSha256"]
                assert payload["sourceDimensions"] == [1080, 2400] and payload["returnedDimensions"] == [900, 2000]
        records[family] = record
    claude, gpt = records["claude"], records["gpt"]
    assert not claude["processAndCoverageAccepted"]
    assert len(claude["observedToolOverlaps"]) == claude["multiToolResponses"] == 1
    overlap = claude["observedToolOverlaps"][0]
    raw = [json.loads(s) for s in Path(claude["rawExecutionLocation"]).read_text(encoding="utf-8-sig").splitlines() if s.strip()]
    ids = {overlap["starting"], *overlap["active"]}
    overlapped = [e["data"]["arguments"]["path"] for e in raw if e["type"] == "tool.execution_start" and e["data"]["toolCallId"] in ids]
    assert {Path(p).name for p in overlapped} == {"instrumentation.txt", "n1-067-article-route.json"}
    repair = load(V / "batch-067-visual-claude-serial-repair-execution.json")
    assert repair["serialRepairAccepted"] and repair["actualModels"] == ["claude-opus-5.5"]
    assert sha(V / "batch-067-visual-claude-serial-repair.md") == repair["reportSha256"]
    assert sha(Path(repair["rawExecutionLocation"])) == repair["rawExecutionSha256"]
    assert gpt["processAndCoverageAccepted"] and not gpt["observedToolOverlaps"] and not gpt["multiToolResponses"]
    assert datetime.fromisoformat(claude["completedAt"]) < datetime.fromisoformat(repair["startedAt"])
    assert datetime.fromisoformat(repair["completedAt"]) < datetime.fromisoformat(gpt["startedAt"])
    android = C.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "-C", str(android), "status", "--porcelain"])
    return freeze, records, repair


mode = sys.argv[1]
freeze, records, repair = verify()
if mode == "prepare":
    assert git("rev-parse", "HEAD") == HEAD
    checks = {}
    for label in ("validate", "manifest", "budget"):
        source = C / f"execution-436-{label}.txt"
        target = V / f"batch-067-visual-{label}-execution-436.txt"
        assert not target.exists()
        shutil.copyfile(source, target)
        checks[label] = {"path": str(target.relative_to(R)), "sha256": sha(target)}
    for name in ("batch-067-visual-task.txt", "batch-067-model-catalog-execution-436.txt", "batch-067-copilot-help-execution-436.txt"):
        target = V / name
        assert not target.exists()
        target.write_text((C / name).read_text(encoding="utf-8-sig").rstrip() + "\n", encoding="utf-8")
    save(V / "batch-067-visual-freeze.json", freeze)
    limits = (
        "No established actionable defect in bounded reviewed content/scenes, not complete native/phone certification. "
        "Complementary captures show the reviewed teaching, but unshown viewport portions/simultaneous whole-table visibility "
        "remain unverified. Actual fallback faces, every-phone readability, physical-phone/general-release/current-main/"
        "whole-set/publication remain unverified. No MLKit, human successful recall, negative geometry tests or successful "
        "model download inferred. Original source/retrieval limits remain. Compatible Androidf9b59a2+ required. "
        "Original Claude two-small-text-read overlap is disclosed and retained as noncompliant, followed by bounded serial repair; "
        "not an all-internal-calls-serial execution."
    )
    reconciliation = {
        "schemaVersion": 1, "execution": 436, "batch": "067",
        "status": "bounded-visual-confirmation-closed-with-disclosed-process-exception-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "dependentNotBlind": True, "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "reviewScope": "Complete new 僧 and 僧侶; words/坊さん.md:30 comparison link. Three facets per file; complete reused file read as context. Twenty-three distinct captured source images per model; complete own initial reports/518line fixture/log/route.",
        "allReviewerProcessesSerialAndExited": True, "allInternalReadsSerial": False,
        "allImageReadsSerial": True, "gptAllInternalReadsSerial": True,
        "processDeviation": {
            "status": "resolved", "originalExecutionFullyCompliant": False,
            "claim": "Claude issued one response with overlapping views of two small operational receipts despite the one-call instruction.",
            "evidence": "Original execution audit preserves one overlap and one multi-tool response; all text fully returned and all23 image calls serial. Original report self-discloses it.",
            "remedy": "Same ORIGINAL session reread exactly instrumentation.txt and route.json, one complete view per response, no overlap, then supplied a supplementary unchanged-findings report. Original report/audit remain untouched, processAndCoverageAccepted=false. Repair archived and process exited before GPT.",
            "decision": "Access and content conclusions accepted with explicitly disclosed process exception and bounded serial repair; no assertion that the historical execution was fully serial or that rereads undo it. No permission failure or native rerun.",
            "repairExecution": "batch-067-visual-claude-serial-repair-execution.json",
            "repairSha256": sha(V / "batch-067-visual-claude-serial-repair-execution.json"),
        },
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "boundedVisualComprehensibility": "CLEAN"}
            for name in ("kanji/僧.md", "words/僧侶.md", "words/坊さん.md:30 comparison link")
        },
        "findings": [],
        "reportQualifications": [
            "Claude supplied no Git tools: its statement about no uncommitted teaching is not independent Git evidence. Coordinator verifies exact runtime diff and frozen hashes separately.",
            "Claude says Gothic and Mincho look similar; actual source pixels show clear serif differences. No identity/same-face conclusion adopted, no content defect. Fallback face remains unidentified.",
            "Claude visually near-identical screenshot groups are not byte-identical aliases. Source hash grouping, not the subjective scene estimate, controls counts:37capture names/23distinct hashes. Distinct hashes are not necessarily independent scenes.",
        ],
        "optional": [
            {"status": "optional", "decision": "Original voicing and explicit register-example polish remain optional, no teaching expansion manufactured."},
            {"status": "optional", "decision": "Claude observes ungraded-practice versus graded-by-shapes wording on unchanged app feedback. Geometry evaluation is not persisted SRS grading; native fixture explicitly confirms no trace log. Nonblocking out-of-scope UI wording, no app edits or new issue."},
        ],
        "observations": [
            "All eight characters and both support words readable/distinguishable in four production font rows; no blank/replacement boxes. Person亻 versus土 in僧/増 and differing値/倍 right components visible. 坊さん wraps but no characters disappear.",
            "Complementary pixels show new clerical versus believer/individual-community scope, mnemonic disclaimer, radical facts, linkedソウ example/compound warning and lookalike notes. 僧侶 allocation, companion versus individual, natural translated examples, Catholic/temple/register boundaries visible; changed坊さん link legible.",
            "Horizontal table clipping has explicit sideways-scroll hint and complementary captures. Not a demonstrated inaccessible row; simultaneous whole-row visibility is not certified.",
            "Actual On optionsソウ/ショウ/ホウ/ボウ; correctソウ feedback. Meaning options vertebra/chinquapin, mosquito, Buddhist monk/priest, Japanese cedar: visibly unambiguous but not authored増/値/倍. No authored-distractor native certification.",
            "Native fixture/log supports both mapped component directions, both comparison directions, SystemBack/offline/N1selection. Supplied assertions, not a proof from filenames. Meaning feedback exits Back before Next, not a newly persisted meaning grade.",
            "Thirteen generated reference strokes touch-injected; trace ungraded/noDrawlog, recall miss persistedAgain. Not MLKit, human recall or negative geometry evidence.",
        ],
        "payloadAccounting": {
            "sourceCaptureNames": 37, "distinctSourceHashes": 23, "claudePayloads": 23,
            "gptPayloads": 23, "totalArchivedReturnedPayloads": 46,
            "sourceDimensions": [1080, 2400], "actualReturnedDimensions": [900, 2000],
            "boundary": "Exact source/model-visible bytes separately preserved. Hashes/ranges establish access, not comprehension. Source hash count not independent scene count.",
        },
        "modelContributionComparison": {
            "sharedScope": "Same snapshot, three teaching scopes/all facets,23identical source images, own original report/complete native fixture/log/route.",
            "shared": "No actionable content/rendering defect established; glyph distinctions, visible choices and changed links accepted with viewport/phone limits.",
            "additionalVerifiedClaudeDefects": [], "additionalVerifiedGPTDefects": [],
            "qualification": "No general model ranking; optional UI wording is not a new content defect. Initial reports/lookup limits unchanged.",
        },
        "inheritedEvidence": {
            "textual": "batch-067-reconciliation.json / signedf1e5b99a, unchanged",
            "android": "execution-433.json fresh3+1 retained without rerun",
            "native": "execution-435.json both terminal0/no skips138.141s retained without rerun",
            "sourceLimits": "Original frozenXML/publiclookup/truncation/heading-only limits retained. No fresh dictionary retrieval.",
            "failures": "Historical permission denials/HOST OOMs retained. HOST-only2GiB initialization NEVER used in native builds.",
        },
        "checks": checks, "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False, "limits": limits, "nextAction": NEXT,
    }
    save(V / "batch-067-visual-reconciliation.json", reconciliation)
    summaries = {
        family: {
            "report": f"docs\\n1-reviews\\batch-067-visual-{family}.md",
            "reportSha256": record["reportSha256"],
            "execution": f"docs\\n1-reviews\\batch-067-visual-{family}-execution.json",
            "executionSha256": sha(V / f"batch-067-visual-{family}-execution.json"),
            "model": record["actualModels"][0], "sessionId": record["sessionId"],
            "startedAt": record["startedAt"], "completedAt": record["completedAt"],
            "exitCode": record["exitCode"], "calls": len(record["toolCalls"]),
            "returnedImages": record["imagePayloadsVerified"],
            "processAndCoverageAccepted": record["processAndCoverageAccepted"],
            "boundedConfirmationAcceptedWithDisclosedRepair": family == "claude",
        } for family, record in records.items()
    }
    record = {
        "schemaVersion": 1, "execution": 436, "checkpoint": 436, "batch": "067",
        "status": reconciliation["status"], "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "authorization": load(C / "execution-436-start.json")["authorization"],
        "scope": load(C / "execution-436-start.json")["scope"], "reviews": summaries,
        "repair": repair,
        "reconciliation": r"docs\n1-reviews\batch-067-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-067-visual-reconciliation.json"),
        "verifiedIndexedNativeArtifacts": freeze["indexedArtifactsVerified"],
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesSerialAndExited": True,
        "allInternalReadsSerial": False, "allImageReadsSerial": True,
        "allOriginalReportsAndTeachingUnmodified": True, "runtimeEditsMade": False,
        "nativeOrAndroidRerun": False, "publicationAttempted": False, "runtimePublished": False,
        "publishedAdditions": 93, "remainingAdditions": 1135, "phoneEvidence": False,
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
        "recordedAt": datetime.now(timezone.utc).isoformat(), "limits": limits, "checks": checks,
        "helperDiagnostics": [
            "Initial freeze was completely written before tuple/list JSON round-trip assertion failed; save comparison corrected, existing freeze verified without recreating evidence.",
            "First repair archiver encountered JSONL result event without data; get(data,{}) fixed before writing any repair report. No reviewer rerun.",
            "Read-only ledger inspection mistakenly looked for Claude execution under control rather than docs; correct original audit inspected, no file change or permission denial.",
        ],
    }
    save(S / "execution-436.json", record)
    batch_path = S / "batch-067-progress.json"
    batch = load(batch_path)
    batch.update(status=record["status"], nextAction=NEXT, limits=limits)
    batch["nativeVisualCheckpoint"] = {
        "execution": 436, "record": "execution-436.json", "boundedIndependentVisualConfirmation": True,
        "reconciliation": "../n1-reviews/batch-067-visual-reconciliation.json",
        "allReviewerProcessesSerialAndExited": True, "allInternalReadsSerial": False,
        "processExceptionAndRepairPreserved": True, "runtimePublished": False, "limits": limits,
    }
    save(batch_path, batch)
    receipts = V / "batch-067-native" / "visual-execution-receipts"
    receipts.mkdir()
    for name in ("execution-436.py", "run-visual-436.ps1", "close-visual-436.py", "batch-067-visual-claude-serial-repair-prompt.txt"):
        shutil.copyfile(C / name, receipts / name)
    print("Reconciled bounded visual evidence,46 returned PNGs; historical overlap and exact serial repair preserved.")
elif mode == "checkpoint":
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    record = load(S / "execution-436.json")
    assert sha(R / record["reconciliation"]) == record["reconciliationSha256"]
    before = load(C / "execution-436-before-progress.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 435 and progress["batch"] == "067"
    summary = {
        "execution": 436, "checkpoint": 436, "batch": "067", "savedCommit": signed, "signature": "G",
        "record": r"docs\n1-sources\execution-436.json", "recordSha256": sha(S / "execution-436.json"),
        "status": "continue", "boundedIndependentVisualConfirmation": True,
        "allReviewerProcessesSerialAndExited": True, "allInternalReadsSerial": False,
        "processExceptionAndRepairPreserved": True, "runtimePublished": False,
        "allOriginalHistoricalKeysPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=436, status="continue", stage="batch-067-bounded-visual-confirmation-closed-awaiting-integration",
                    nextAction=NEXT, blocker=None)
    progress["execution436StartingState"]["status"] = "signed-bounded-visual-checkpoint-complete"
    progress["batch067VisualConfirmationCheckpoint"] = summary
    progress["execution436CoordinatorCheckpoint"] = dict(summary)
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    temp = C / "execution-436-progress.tmp"
    save(temp, progress)
    temp.replace(C / "progress.json")
    body = (
        "Batch 067 (僧 / necessary support 僧侶): bounded original-session visual confirmations saved "
        f"locally in normally signed `{signed}`; runtime NOT published.\n\n"
        "Original Claude Opus5.5 and GPT6.1Sol processes ran serially and exited. Both inspected complete "
        "three teaching files,518-line fixture/log/route and23distinct source-image hashes each "
        "(37capture names;46actual900×2000 returned payloads archived). No actionable content/rendering "
        "defect established. Claude's original two-small-receipt overlap is disclosed, retained as "
        "noncompliant, and followed by a two-call serial reread/supplement before GPT; no claim that "
        "the historical execution was fully serial. All image calls and all GPT calls were serial.\n\n"
        "Four font rows readable/distinguishable; changed links, clerical/register boundaries, soleソウ "
        "question and actual meaning options accepted within captured views. Table clipping has an "
        "explicit scroll hint/complementary captures. Unchanged app practice-versus-geometry wording "
        "is optional UI polish, not a content/SRS defect. No teaching/app changes. Validator0errors, "
        "manifest68c767f176e68882 fresh/8329runtime hashes, original local budgets pass. Passing435native "
        "2terminal0/138.141s and433Android3+1 inherited without rerun.\n\n"
        "Published remains93/1228,1135remain; latest accepted066 `f0b318eb`. Next bounded checkpoint: "
        "fresh latest-main nonrewriting integration/combined audits and validation, normal signing/"
        "owner fast-forward push, green CI, exact immutable public ZIP/runtime hashes/budgets before "
        "counting067 delivered or starting068. Compatible Androidf9b59a2+ required; physical-phone/"
        "general-release/whole-set acceptance outstanding. No fallback-face identity, MLKit or human "
        "recall certification. Full reports/exception/repair/limits: `docs/n1-sources/execution-436.json` "
        "and `docs/n1-reviews/batch-067-visual-reconciliation.json`. Overall project incomplete.\n"
    )
    (C / "execution-436-issue-body.txt").write_text(body, encoding="utf-8")
    print(json.dumps({"checkpoint": 436, "status": "continue", "savedCommit": signed, "runtimePublished": False}))
elif mode == "finalize":
    progress = load(C / "progress.json")
    before = load(C / "execution-436-before-progress.json")
    receipt = load(C / "execution-436-issue-verified.json")
    body = (C / "execution-436-issue-body.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"].replace("\r\n", "\n") == body
    assert progress["checkpoint"] == 436 and progress["status"] == "continue"
    assert progress["batch"] == "067" and progress["remainingAdditions"] == 1135
    assert not git("status", "--porcelain") and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD") == progress["execution436CoordinatorCheckpoint"]["savedCommit"]
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    issue = {
        "url": receipt["html_url"], "id": receipt["id"], "author": receipt["user"]["login"],
        "createdAt": receipt["created_at"], "bodyVerified": True,
        "bodyComparison": "Exact after CRLF-to-LF normalization only.",
        "savedCommit": git("rev-parse", "HEAD"), "runtimePublished": False,
    }
    progress["batch067VisualIssueReceipt"] = issue
    for key in ("batch067VisualConfirmationCheckpoint", "execution436CoordinatorCheckpoint"):
        progress[key]["issueUpdate"] = issue["url"]
        progress[key]["ownerAuthorAndBodyVerified"] = True
    temp = C / "execution-436-progress-final.tmp"
    save(temp, progress)
    temp.replace(C / "progress.json")
    final = {
        "checkpoint": 436, "status": "continue", "batch": "067",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "contentWorktreeClean": True,
        "allPriorHistoryPreserved": True, "issue": issue, "runtimePublished": False,
        "publishedAdditions": 93, "remainingAdditions": 1135,
        "recordSha256": sha(S / "execution-436.json"),
        "nextStage": "Fresh latest-main combined validation and publication acceptance; no068 before delivery.",
    }
    save(C / "execution-436-final-verification.json", final)
    print(json.dumps(final, indent=2))
