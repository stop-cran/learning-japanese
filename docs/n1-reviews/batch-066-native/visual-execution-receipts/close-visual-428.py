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
HEAD = "b37c5ad6ffb5ab62cf4525b50afe4e2a6cdd011b"
TEACHING = "6c23db00d2d14ec6d0a3537a1ef72b273e3d55e7"
NEXT = (
    "SAME066 signed bounded visual checkpoint428: ORIGINAL Claude9db759dd and GPT81338bd1 "
    "dependent confirmations complete; both30calls entirelyserial,19distinct sourcePNG each/"
    "38actual returned900x2000payloads from41sourcecapture names, complete3teachingfiles/"
    "523linefixture/log/route. Read docs\\n1-sources\\execution-428.json and "
    "docs\\n1-reviews\\batch-066-visual-reconciliation.json. No actionable defect established; "
    "no teaching/app changes. Preserve original reports, limited viewport/table/fallbackface/"
    "MLKit/humanrecall/phone qualifications. Claude Mincho-style description withdrawn by "
    "coordinator direct pixels (serifs visible, face identity unverified); initial distractor "
    "no-filler inference corrected: observed N1 meaning options differ from authored "
    "療/像/値, all visibly wrong for僚. Authored-choice native presentation NOT certified. "
    "Accepted427native2terminal0/93.971s and425freshAndroid3+1 inherited without rerun; "
    "no redundant reviewer/native/Gradle absentnewconcern. Historicaldenials/HOSTOOMs retained; "
    "qualifiedHOST-only2GiBinit NEVER nativebuilds. NEXT bounded checkpoint: freshfetchlatest"
    "origin/main/nonrewritingintegration as needed, allactualcombinedsource-membership/"
    "baseline/reading/link/font/stroke/Python/vocab/validator/freshmanifest and original"
    "18000entries42MiBcompressed80MiBinflated56MiBretainedbudget gates; normal signing/"
    "ownerfastforward/publicSHA/terminalgreenCI/EVERYimmutablepublicZIP runtimehash/budgets/"
    "ownerissue60 BEFOREdelivery or067. Permissiondenial/signingwait: preserve precise "
    "failure and yield, no retry/workaround/secondrunner/concurrentheavywork/supervisorchanges. "
    "PreserveFULLlivehistory. Published92/1228,1136remain/latest06544645f54; "
    "local066 NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/"
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
    freeze = load(C / "batch-066-visual-freeze.json")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for key in ("teachingHashes", "originalReportHashes"):
        for path, digest in freeze[key].items():
            assert sha(R / path) == digest
    index = V / "batch-066-native" / "execution-427-artifact-index.json"
    assert sha(index) == freeze["nativeArtifactIndexSha256"]
    for row in load(index)["files"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"]
    records = {}
    for family in ("claude", "gpt"):
        prefix = "batch-066-visual-" + family
        record = load(V / f"{prefix}-execution.json")
        assert record["processAndCoverageAccepted"] and record["exitCode"] == 0
        assert record["actualModels"] == [record["requestedModel"]] == [record["usage"]["currentModel"]]
        assert not record["observedToolOverlaps"] and not record["multiToolResponses"]
        assert not record["missingRequiredText"] and not record["unexpectedReadPaths"] and not record["unfinishedTools"]
        assert record["imagePayloadsVerified"] == 19 and record["expectedPngMembershipReturned"]
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
    assert datetime.fromisoformat(records["claude"]["completedAt"]) < datetime.fromisoformat(records["gpt"]["startedAt"])
    assert records["gpt"]["priorExitAndArchiveVerifiedBeforeLaunch"]
    android = C.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "-C", str(android), "status", "--porcelain"])
    return freeze, records


mode = sys.argv[1]
freeze, records = verify()
if mode == "prepare":
    assert git("rev-parse", "HEAD") == HEAD
    checks = {}
    for label in ("validate", "manifest", "budget"):
        source = C / f"execution-428-{label}.txt"
        target = V / f"batch-066-visual-{label}-execution-428.txt"
        assert not target.exists()
        shutil.copyfile(source, target)
        checks[label] = {"path": str(target.relative_to(R)), "sha256": sha(target)}
    for source, target in [
        (C / "batch-066-visual-task.txt", V / "batch-066-visual-task.txt"),
        (C / "batch-066-model-catalog-execution-428.txt", V / "batch-066-model-catalog-execution-428.txt"),
        (C / "batch-066-copilot-help-execution-428.txt", V / "batch-066-copilot-help-execution-428.txt"),
    ]:
        assert not target.exists()
        target.write_text(source.read_text(encoding="utf-8-sig").rstrip() + "\n", encoding="utf-8")
    save(V / "batch-066-visual-freeze.json", freeze)
    limits = (
        "No established actionable defect in bounded reviewed content/scenes, not complete native/phone certification. "
        "Complementary captures show the reviewed teaching, but unshown viewport portions/simultaneous whole-table visibility "
        "remain unverified. Actual fallback faces, every-phone readability, physical-phone/general-release/current-main/"
        "whole-set/publication remain unverified. No MLKit, human successful recall, negative geometry tests or successful "
        "model download inferred. Original source/retrieval limits remain. Compatible Androidf9b59a2+ required."
    )
    reconciliation = {
        "schemaVersion": 1, "execution": 428, "batch": "066",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "dependentNotBlind": True, "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "reviewScope": "Complete new 僚, words/同僚.md:28 component link and kanji/同.md:36 common-word addition. Three facets per file; complete reused files read as context. Nineteen distinct captured scenes per model; complete own initial reports/523line fixture/log/route.",
        "allReviewerProcessesSerialAndExited": True, "allInternalReadsSerial": True,
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "boundedVisualComprehensibility": "CLEAN"}
            for name in ("kanji/僚.md", "words/同僚.md:28 component link", "kanji/同.md:36 common-word addition")
        },
        "findings": [],
        "reportErrata": [
            {
                "id": "V1", "status": "resolved",
                "claim": "Initial Claude explanation assumed three authored distractors eliminate fallback in the actual stack.",
                "evidence": "Actual meaning-question shows enjoy/receive benefits, vertebra/chinquapin, crane (bird), colleague. QuizBuilder.kt:16-24 resolves authored IDs only against its supplied pool.",
                "disposition": "Claude explicitly corrects its original inference in the visual report. Both models independently inspect actual displayed labels and find them wrong for 僚. Original report preserved; native presentation of authored 療/像/値 is not certified, and larger/live pools remain unverified.",
            },
            {
                "id": "V2", "status": "withdrawn",
                "claim": "Claude describes the font-pairs Mincho row as the same sans face as Gothic.",
                "evidence": "Coordinator direct view of original n1-066-font-pairs.png shows clearly serifed Mincho 同/口 and other differentiated forms versus Gothic; GPT makes no same-sans claim.",
                "disposition": "The visual style description is not adopted. Actual fallback face remains unidentified; all four rows readable/distinguishable. No content/metadata/font change or consequential unresolved claim; original report unchanged.",
                "confidence": "high for visible serif difference, unverified for actual font identity",
            },
        ],
        "optional": [
            {"status": "optional", "decision": "Claude mid-word kana wrapping and crowded stroke-number spacing are nonblocking app polish, not in-scope content defects. No Android changes or new issues."},
            {"status": "optional", "decision": "Original optional extra compounds/phonetic detail/extra reused row/equal-rank sense remain optional; no teaching expansion manufactured."},
        ],
        "observations": [
            "All nine assigned glyphs and 同僚 readable/distinguishable across four production rows; no blank/replacement boxes. Person亻 versusillness疒 and 像/値 right components remain distinct.",
            "Complementary pixels show complete new meanings/mnemonic disclaimer, radical facts, linked リョウ example and comparison notes; reused component link and common-word addition, coworker examples/particle/plural/rank boundaries are visible.",
            "Table horizontal clipping occurs with explicit sideways-scroll hint and complementary captures. Not a demonstrated inaccessible row; simultaneous whole-row visibility is not certified.",
            "Actual On question/feedback shows リョウ versusホウ/ヨウ/リュウ; sole normalizedりょう persisted and no Kun log from supplied fixture assertions. Meaning grade was not newly persisted: Back before Next.",
            "Navigation/SystemBack transitions and persisted grades are native fixture/log evidence, not proof from screenshot filenames. Both component pairs/four directions are covered by passed fixture.",
        ],
        "payloadAccounting": {
            "sourceCaptureNames": 41, "distinctSourceHashes": 19,
            "claudePayloads": 19, "gptPayloads": 19, "totalArchivedReturnedPayloads": 38,
            "sourceDimensions": [1080, 2400], "actualReturnedDimensions": [900, 2000],
            "boundary": "Exact source/model-visible bytes separately preserved. Hashes/ranges establish access, not comprehension. Reviewers estimated dimensions; coordinator checks actual PNG headers.",
        },
        "modelContributionComparison": {
            "sharedScope": "Same snapshot, three teaching scopes/all facets, nineteen identical distinct scenes, own original report/complete native fixture/log/route.",
            "shared": "No actionable content/rendering defect established; visible reading/meaning choices, glyph distinctions, changed links and legible teaching accepted with viewport/phone limits.",
            "additionalVerifiedClaudeDefects": [], "additionalVerifiedGPTDefects": [],
            "qualification": "No general model ranking; Claude corrects its own original fallback inference, while the same-sans observation is unsupported.",
        },
        "inheritedEvidence": {
            "textual": "batch-066-reconciliation.json / signed4c0a3b6f, retained unchanged",
            "android": "execution-425.json fresh3+1 retained without rerun",
            "native": "execution-427.json both terminal0/no skips93.971s retained without rerun",
            "sourceLimits": "Original frozenXML/publiclookup/truncation/heading-only/gaiji limits retained. No fresh dictionary retrieval.",
            "failures": "Historical permission denials/HOST OOMs retained. HOST-only2GiB initialization NEVER used in native builds.",
        },
        "checks": checks, "boundedIndependentVisualConfirmation": True,
        "runtimeAccepted": False, "runtimePublished": False, "limits": limits, "nextAction": NEXT,
    }
    save(V / "batch-066-visual-reconciliation.json", reconciliation)
    summaries = {
        family: {
            "report": f"docs\\n1-reviews\\batch-066-visual-{family}.md",
            "reportSha256": record["reportSha256"],
            "execution": f"docs\\n1-reviews\\batch-066-visual-{family}-execution.json",
            "executionSha256": sha(V / f"batch-066-visual-{family}-execution.json"),
            "model": record["actualModels"][0], "sessionId": record["sessionId"],
            "startedAt": record["startedAt"], "completedAt": record["completedAt"],
            "exitCode": record["exitCode"], "calls": len(record["toolCalls"]),
            "returnedImages": record["imagePayloadsVerified"], "processAndCoverageAccepted": True,
        } for family, record in records.items()
    }
    record = {
        "schemaVersion": 1, "execution": 428, "checkpoint": 428, "batch": "066",
        "status": reconciliation["status"], "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "authorization": load(C / "execution-428-start.json")["authorization"],
        "scope": load(C / "execution-428-start.json")["scope"], "reviews": summaries,
        "reconciliation": r"docs\n1-reviews\batch-066-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-066-visual-reconciliation.json"),
        "verifiedIndexedNativeArtifacts": freeze["indexedArtifactsVerified"],
        "boundedIndependentVisualConfirmation": True, "allReviewerProcessesAndInternalReadsSerial": True,
        "allOriginalReportsAndTeachingUnmodified": True, "runtimeEditsMade": False,
        "nativeOrAndroidRerun": False, "publicationAttempted": False, "runtimePublished": False,
        "publishedAdditions": 92, "remainingAdditions": 1136, "phoneEvidence": False,
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
        "recordedAt": datetime.now(timezone.utc).isoformat(), "limits": limits, "checks": checks,
    }
    save(S / "execution-428.json", record)
    batch_path = S / "batch-066-progress.json"
    batch = load(batch_path)
    batch.update(status=record["status"], nextAction=NEXT, limits=limits)
    batch["nativeVisualCheckpoint"] = {
        "execution": 428, "record": "execution-428.json", "boundedIndependentVisualConfirmation": True,
        "reconciliation": "../n1-reviews/batch-066-visual-reconciliation.json",
        "allReviewerProcessesAndInternalReadsSerial": True, "runtimePublished": False, "limits": limits,
    }
    save(batch_path, batch)
    receipts = V / "batch-066-native" / "visual-execution-receipts"
    receipts.mkdir()
    for name in ("execution-428.py", "run-visual-428.ps1", "close-visual-428.py"):
        shutil.copyfile(C / name, receipts / name)
    print("Reconciled visual evidence; preserved original reports, historical limitations and38returned PNGs.")
elif mode == "checkpoint":
    signed = git("rev-parse", "HEAD")
    assert signed != HEAD and git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == "44645f54b3fadb4b792b91c12a895ebf9f495d4e"
    record = load(S / "execution-428.json")
    assert sha(R / record["reconciliation"]) == record["reconciliationSha256"]
    before = load(C / "execution-428-before-progress.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 427 and progress["batch"] == "066"
    summary = {
        "execution": 428, "checkpoint": 428, "batch": "066", "savedCommit": signed, "signature": "G",
        "record": r"docs\n1-sources\execution-428.json", "recordSha256": sha(S / "execution-428.json"),
        "status": "continue", "boundedIndependentVisualConfirmation": True,
        "allReviewerProcessesAndInternalReadsSerial": True, "runtimePublished": False,
        "allOriginalHistoricalKeysPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=428, status="continue", stage="batch-066-bounded-visual-confirmation-closed-awaiting-integration",
                    nextAction=NEXT, blocker=None)
    progress["execution428StartingState"]["status"] = "signed-bounded-visual-checkpoint-complete"
    progress["batch066VisualConfirmationCheckpoint"] = summary
    progress["execution428CoordinatorCheckpoint"] = dict(summary)
    for key in before.keys() - {"checkpoint", "status", "stage", "nextAction", "blocker"}:
        assert progress[key] == before[key], key
    temp = C / "execution-428-progress.tmp"
    save(temp, progress)
    temp.replace(C / "progress.json")
    save(C / "execution-428-checkpoint.json", summary)
    body = (
        f"Batch066 bounded visual checkpoint **428** saved locally at signed `{signed}`; no runtime publication.\n\n"
        "Original Claude Opus5.5 and GPT6.1Sol sessions each inspected the same **19 distinct native PNGs** "
        "(41 capture names), complete three teaching files/523-line native fixture/log/route. Each used "
        "**30 strictly serial view calls**, with no overlaps, failed/truncated/missing assigned reads or "
        "unexpected paths. Claude exited and its complete report was archived before GPT launched. "
        "**38 actual returned900x2000 PNG payloads** are archived separately from1080x2400sources; hashes "
        "establish access, not comprehension. No actionable correctness/coverage/bounded visual defect established.\n\n"
        "Actual On question/feedback, glyph distinctions, component links, examples/particle/rank guidance and "
        "meaning choices inspected. Actual N1 meaning wrong options differ from authored distractors; all "
        "displayed labels are wrong for僚. Claude corrects its earlier no-filler inference; its unsupported "
        "same-sans Mincho description is explicitly not adopted (serifs visible; fallback face unidentified). "
        "Original reports preserved; table viewport clipping/scroll cues and optional app polish documented. "
        "No teaching/app changes or extra content invented.\n\n"
        "Accepted427 native2cases terminal0/93.971s and425 freshAndroid3+1 retained without rerun. "
        "No MLKit/human-recall/physical-phone/general-release claim. All historical denials/HOST OOMs "
        "preserved; qualifiedHOST-only2GiB init NEVER applies to native builds.\n\n"
        "**Next bounded checkpoint:** freshlatest-main integration and all combined content/baseline/source/"
        "link/font/stroke/Python/vocabulary/manifest/original archive-budget gates, then normal signed owner "
        "fast-forward publication, terminalgreenCI and every immutable-ZIP runtime hash before delivery or067. "
        "**92/1,228 published;1,136 remain**. CompatibleAndroid`f9b59a2`+ required; whole project incomplete."
    )
    (C / "execution-428-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps({"checkpoint": 428, "savedCommit": signed, "status": "continue",
                      "historyPreserved": True, "runtimePublished": False}, indent=2))
else:
    assert mode == "verify"
    print("Verified original teaching/reports, native artifacts, two serial model processes and38actual returned payloads.")
