import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
HEAD = "18c87f8ac27f3bd0eb59f4320130bfdfd34a755f"
TEACHING = "45c275e7c041d8486705ab860a31f34e51ac7a70"
NEXT = (
    "SAME065 checkpoint420: bounded dependent visual confirmations archived from ORIGINAL "
    "Claude9555ba9e and GPT491afc55 on unchanged45c275e7 teaching/evidence18c87f8a. "
    "Read docs/n1-sources/execution-420.json and docs/n1-reviews/batch-065-visual-reconciliation.json. "
    "Both saw30distinct sourcePNG payloads, complete four teaching files/562line fixture/log/route. "
    "Claude original44calls had TWO internal overlaps: original process remains NONCONFORMANT "
    "and preserved; a separate5call serial recovery freshly re-read exactly4affected resources "
    "plus original report, corrected provenance/one-at-a-time overclaims, no new defect. "
    "GPT44calls entirelyserial; Claude recovery exited/archived before GPT launch. "
    "Original provider models verified;62actual returned900x2000 payloads archived separately "
    "from1080x2400sources; counts/hashes establish access not comprehension. "
    "No actionable content/rendering defect established in bounded captures. Keep unseen "
    "table/article regions, unidentified fallbackface/phone/MLKit/humanrecall explicit. "
    "Accepted419native2cases terminal0/148.883s and417freshAndroid3+1 RETAINED, do not rerun "
    "absentnewconcern. Original416denial/actual1GiBOOM/049512MiBfailure and qualifiedHOST-only2GiB "
    "init retained; NEVER use host init for native builds. NEXT bounded checkpoint: fresh fetch "
    "latestorigin/main, nonrewriting integrate as needed, all actualcombined source-membership/"
    "baseline/reading/link/font/stroke/Python/vocab/validator/freshmanifest and original18000entries/"
    "42MiBcompressed/80MiBinflated/56MiBretained gates; normal signing, owner fastforward publication/"
    "publicSHA/terminalgreenCI/EVERYimmutableZIP runtimehash/budgets/terminalreceipts/ownerissue60 "
    "BEFOREdelivery or066. No publish from old results alone. Actualpermissiondenial or signingwait: "
    "preserve exact failure/report/yield, no retry/workaround. No secondrunner/concurrentheavywork/"
    "supervisorchanges; preserveFULLlivehistory. Published91/1228,1137remain/latest0640fe60920; "
    "localdraft92 NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/"
    "whole-set outstanding. Overallproject incomplete."
)
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == value


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=R, encoding="utf-8").strip()


def verify():
    freeze = load(C / "batch-065-visual-freeze.json")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for key in ("teachingHashes", "originalReportHashes"):
        for path, digest in freeze[key].items():
            assert sha(R / path) == digest, path
    native = load(S / "execution-419.json")
    index = R / native["artifactIndex"]
    assert sha(index) == native["artifactIndexSha256"] == freeze["nativeArtifactIndexSha256"]
    for item in load(index)["files"]:
        path = R / item["path"]
        assert sha(path) == item["sha256"] and path.stat().st_size == item["bytes"], path
    records = {}
    for label in ("claude", "claude-serial-recovery", "gpt"):
        prefix = "batch-065-visual-" + label
        record = load(V / f"{prefix}-execution.json")
        records[label] = record
        assert record["exitCode"] == 0
        assert record["actualModels"] == [record["requestedModel"]] == [record["usage"]["currentModel"]]
        assert sha(V / f"{prefix}.md") == record["reportSha256"]
        assert sha(Path(record["rawExecutionLocation"])) == record["rawExecutionSha256"]
        assert not record["missingRequiredText"] and not record["unexpectedReadPaths"]
        assert not record["unfinishedTools"] and not record["failedTools"]
        assert record["expectedPngMembershipReturned"]
        for call in record["toolCalls"]:
            if "imagePayload" in call:
                payload = call["imagePayload"]
                assert sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
                assert sha(Path(call["arguments"]["path"])) == payload["sourceSha256"]
                assert payload["sourceDimensions"] == [1080, 2400]
                assert payload["returnedDimensions"] == [900, 2000]
        if label == "claude":
            assert not record["processAndCoverageAccepted"]
            assert len(record["observedToolOverlaps"]) == len(record["multiToolResponses"]) == 2
            assert record["imagePayloadsVerified"] == 30
        else:
            assert record["processAndCoverageAccepted"]
            assert not record["observedToolOverlaps"] and not record["multiToolResponses"]
            assert record["imagePayloadsVerified"] == (2 if label.endswith("recovery") else 30)
    parse = datetime.fromisoformat
    assert parse(records["claude"]["completedAt"]) < parse(records["claude-serial-recovery"]["startedAt"])
    assert parse(records["claude-serial-recovery"]["completedAt"]) < parse(records["gpt"]["startedAt"])
    assert records["gpt"]["priorExitAndArchiveVerifiedBeforeLaunch"]
    return freeze, records


mode = sys.argv[1]
freeze, records = verify()
if mode == "prepare":
    assert git("rev-parse", "HEAD") == HEAD
    for name in ("help", "model-catalog"):
        source = C / f"batch-065-copilot-{name}-execution-420.txt"
        target = V / source.name
        assert not target.exists()
        shutil.copyfile(source, target)
    task = V / "batch-065-visual-task.txt"
    assert not task.exists()
    shutil.copyfile(C / task.name, task)
    recovery_task = V / "batch-065-visual-claude-serial-recovery-task.txt"
    shutil.copyfile(C / "batch-065-visual-claude-serial-recovery-prompt.txt", recovery_task)
    save(V / "batch-065-visual-freeze.json", freeze)
    reconciliation = {
        "schemaVersion": 1, "execution": 420, "batch": "065",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "dependentNotBlind": True, "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "reviewScope": "Complete new 倹/倹約/倹しい and added 倹約 common-word line in reused 約; three facets, thirty distinct captured scenes per model. Complete original own reports and562line native fixture/log/route returned.",
        "allReviewerProcessesSerialAndExited": True,
        "allOriginalInternalReadsSerial": False,
        "processDisposition": {
            "status": "partially resolved",
            "historicalViolation": "Claude original44calls contained two two-tool responses and two measured overlaps: confirmation report/shared task, then agreement-approximate-reading/agreement-mnemonic. Original audit remains processAndCoverageAccepted=false; not retrospectively serial.",
            "boundedRemedy": "Same Claude original session freshly re-read the four affected resources plus its original visual report in five strictly serial calls. No whole-dossier repetition; original report preserved. Recovery passed before GPT launch.",
            "remainingQualification": "The historical process violation remains explicitly recorded. Bounded affected-resource confirmation is accepted; no claim that the original entire turn conformed.",
            "gpt": "44calls, no multi-tool responses, overlaps, failed/truncated/missing assigned reads or unexpected paths. Actual original family and terminal exit verified.",
        },
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "boundedVisualComprehensibility": "CLEAN"}
            for name in ("kanji/倹.md", "words/倹約.md", "words/倹しい.md", "kanji/約.md:added common-word line")
        },
        "findings": [],
        "reportErrata": [
            {"id": "V1", "status": "resolved", "claim": "Claude original says all30PNGs one at a time despite an overlapping image response.", "disposition": "Recovery explicitly corrects the false serial claim; historical report unchanged. All30 returned originally, affected2 freshly returned serially."},
            {"id": "V2", "status": "resolved", "claim": "Original 約 pixel provenance called inherited from earlier image reads.", "disposition": "Fresh original-turn image reads, not older textual evidence. Two affected scenes freshly serially confirmed; facts line rests on original serial agreement-radical image."},
            {"id": "V3", "status": "withdrawn", "claim": "Original labels some distinct hashes effectively same scenes.", "disposition": "Distinct bytes do not establish materially distinct visible content. Recovery withdraws unsupported agreement comparison;30source hashes/60capture names/62returned payloads remain separate mechanical counts."},
            {"id": "V4", "status": "resolved", "claim": "Different weight presumably identifies fallback face.", "disposition": "Weight difference does not identify fallback. Actual face remains UNVERIFIED; readable four-font rows do not establish every-phone acceptance."},
        ],
        "observations": [
            "Four production-font rows render all12probe glyphs and two support words readably/distinguishably in bounded captures. Wrapped勺 is visible, not absent.",
            "Both actual curated questions/feedback show ケン andつましい; full source-onlyつづまやか remains in dictionary information, not offered. Actual meaning choices are frugal/thrifty, firefly, willow and cocoon, not authored三labels.",
            "Both support article attachment/examples/kana/translations and six component directions/two support-comparison directions are visible in text and selected scenes. Navigation transitions/persisted grades come from native fixture assertions, not still-image inference.",
            "Table horizontal clipping occurs with explicit scroll cue and complementary viewports. No accessibility defect established; unshown cells/regions not certified.",
        ],
        "optional": [
            {"status": "optional", "decision": "No spelling-polish/phonetic/new-exclusion expansion; inherited C1/C2 closure and original disagreement retained."},
            {"status": "optional", "decision": "Claude flags app wording not-graded versus graded-by-shapes on tracing feedback. No in-scope content defect established; no unrelated Android edits or issue created."},
        ],
        "payloadAccounting": {
            "sourceCaptureNames": 60, "distinctSourceHashes": 30,
            "claudeOriginalPayloads": 30, "claudeRecoveryPayloads": 2, "gptPayloads": 30,
            "totalArchivedReturnedPayloads": 62,
            "sourceDimensions": [1080, 2400], "actualReturnedDimensions": [900, 2000],
            "boundary": "Exact source/model-visible bytes separately preserved. Returned ranges, hashes and reads establish access, not comprehension or a fresh independent dictionary audit.",
        },
        "inheritedEvidence": {
            "textualClosure": "batch-065-reconciliation.json / ae36905b",
            "android": "execution-417.json qualified fresh3+1, retained without rerun",
            "native": "execution-419.json both namedcases terminal0/no skips148.883s, retained without rerun",
            "sourceAndCitationLimits": "Original complete reports/executions preserved. No new public lookup; original frozenXML/truncation/heading-only/gaiji limits retained.",
        },
        "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False,
        "limits": "CLEAN only means no established actionable defect in bounded reviewed content/scenes. Unseen article/table portions, fallback-face identity, physical-phone/general-release/current-main/whole-set/publication remain unverified. No MLKit or successful human recall/model download/negative geometry tests inferred. Original internal process violation remains historical. CompatibleAndroidf9b59a2+ required.",
        "nextAction": NEXT,
    }
    save(V / "batch-065-visual-reconciliation.json", reconciliation)
    summaries = {
        label: {
            "report": f"docs\\n1-reviews\\batch-065-visual-{label}.md",
            "reportSha256": record["reportSha256"],
            "execution": f"docs\\n1-reviews\\batch-065-visual-{label}-execution.json",
            "executionSha256": sha(V / f"batch-065-visual-{label}-execution.json"),
            "model": record["actualModels"][0], "sessionId": record["sessionId"],
            "startedAt": record["startedAt"], "completedAt": record["completedAt"],
            "exitCode": record["exitCode"], "calls": len(record["toolCalls"]),
            "returnedImages": record["imagePayloadsVerified"],
            "processAndCoverageAccepted": record["processAndCoverageAccepted"],
            "overlaps": len(record["observedToolOverlaps"]),
        } for label, record in records.items()
    }
    record = {
        "schemaVersion": 1, "execution": 420, "checkpoint": 420, "batch": "065",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "authorization": load(C / "execution-420-start.json")["authorization"],
        "scope": load(C / "execution-420-start.json")["scope"],
        "reviews": summaries,
        "reconciliation": r"docs\n1-reviews\batch-065-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-065-visual-reconciliation.json"),
        "verifiedIndexedNativeArtifacts": freeze["indexedArtifactsVerified"],
        "boundedIndependentVisualConfirmation": True,
        "originalClaudeTurnSerial": False, "affectedResourcesSeriallyReconfirmed": True,
        "allReviewerProcessesSerialAndExited": True,
        "allOriginalReportsAndTeachingUnmodified": True,
        "runtimeEditsMade": False, "nativeOrAndroidRerun": False,
        "publicationAttempted": False, "runtimePublished": False,
        "publishedAdditions": 91, "remainingAdditions": 1137,
        "phoneEvidence": False, "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "limits": reconciliation["limits"],
    }
    save(S / "execution-420.json", record)
    batch_path = S / "batch-065-progress.json"
    batch = load(batch_path)
    batch["status"] = record["status"]
    batch["nextAction"] = NEXT
    batch["limits"] = record["limits"]
    batch["nativeVisualCheckpoint"] = {
        "execution": 420, "record": "execution-420.json",
        "boundedIndependentVisualConfirmation": True,
        "originalClaudeTurnSerial": False, "affectedResourcesSeriallyReconfirmed": True,
        "reconciliation": "../n1-reviews/batch-065-visual-reconciliation.json",
        "runtimePublished": False, "limits": record["limits"],
    }
    save(batch_path, batch)
    receipts = V / "batch-065-native" / "visual-execution-receipts"
    receipts.mkdir()
    for name in ("prepare-visual-420.py", "run-visual-420.ps1", "archive-visual-420.py", "close-visual-420.py"):
        shutil.copyfile(C / name, receipts / name)
    print("Reconciled bounded visual evidence; preserved original overlaps/reports and62actual returned payloads.")
elif mode == "checkpoint":
    signed_head = git("rev-parse", "HEAD")
    assert signed_head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == "0fe60920ee7e2de1504edb44e673aa370d928a17"
    record = load(S / "execution-420.json")
    assert sha(R / record["reconciliation"]) == record["reconciliationSha256"]
    before = load(C / "execution-420-before-progress.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 419 and progress["batch"] == "065"
    summary = {
        "execution": 420, "checkpoint": 420, "batch": "065",
        "savedCommit": signed_head, "signature": "G",
        "record": r"docs\n1-sources\execution-420.json",
        "recordSha256": sha(S / "execution-420.json"),
        "status": "continue", "boundedIndependentVisualConfirmation": True,
        "originalClaudeTurnSerial": False, "affectedResourcesSeriallyReconfirmed": True,
        "runtimePublished": False, "allOriginalHistoricalKeysPreservedExactly": True,
        "nextAction": NEXT,
    }
    progress.update(checkpoint=420, status="continue", stage="batch-065-bounded-visual-confirmation-closed-awaiting-integration",
                    nextAction=NEXT, blocker=None)
    progress["execution420StartingState"]["status"] = "signed-bounded-visual-checkpoint-complete"
    progress["batch065VisualConfirmationCheckpoint"] = summary
    progress["execution420CoordinatorCheckpoint"] = summary
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    temporary = C / "execution-420-progress.tmp"
    save(temporary, progress)
    temporary.replace(C / "progress.json")
    save(C / "execution-420-checkpoint.json", summary)
    body = (
        f"Batch065 bounded visual checkpoint **420** saved locally at signed `{signed_head}`; no runtime publication.\n\n"
        "Original Claude Opus5.5 and GPT6.1Sol sessions each received the same **30 distinct source PNGs** (60 capture names), complete four teaching files/562-line native fixture/log/route. No actionable defect was established in bounded correctness, coverage or visual comprehensibility. Both actual curated readings and feedback, font/look-alike rows, attachment/examples, added reciprocal link and observed fallback meaning choices were inspected. **62 actual returned900x2000 image payloads** are archived separately from1080x2400sources; byte accounting is not comprehension or every-phone certification.\n\n"
        "**Process qualification:** Claude's original44calls had **two internal overlaps**; its original report/audit remain intact and NONCONFORMANT, not retrospectively called serial. A bounded original-session recovery re-read exactly the four affected resources plus its report in five strictly serial calls, correcting serial/provenance/fallback overclaims. GPT's44calls were fully serial. Each process exited and its report was archived before the next launched. The original process breach remains explicit; only the affected-resource remediation is closed.\n\n"
        "Accepted419native2case terminal0/148.883s and417freshAndroid3+1 retained without rerun. No teaching/app edit, new native run, MLKit/human-recall claim, physical-phone/general-release acceptance or push. Unseen article/table regions and actual fallback identity remain unverified. Original416 denial/1GiB OOM/049512MiB history retained; qualifiedHOST-only2GiB init NEVER applies to native builds.\n\n"
        "**Next bounded checkpoint:** freshlatest-main integration and all combined content/baseline/source/link/font/stroke/Python/vocabulary/manifest/original archive-budget gates, then normal signed owner fast-forward publication, terminalgreenCI and every immutable-ZIP runtime hash before delivery or066. **91/1,228 published;1,137 remain**. CompatibleAndroid`f9b59a2`+ required; whole project incomplete."
    )
    (C / "execution-420-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps({"checkpoint": 420, "savedCommit": signed_head, "status": "continue",
                      "historyPreserved": True, "runtimePublished": False}, indent=2))
else:
    assert mode == "verify"
    print("Verified original teaching/reports,75native artifacts,3model/process reports and62actual returned payloads.")
