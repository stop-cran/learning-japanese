import base64
import gzip
import hashlib
import io
import json
import runpy
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
L = C / "logs" / "bbb21faa-bfac-4aa3-8a39-56c8dd5c3499"
HEAD = "81238670fbf9619a94454f81618ce1a68782981d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
NEXT = (
    "SAME086 current-main integration and combined-tree validation checkpoint next; NO087. "
    "Read docs/n1-sources/execution-606.json and docs/n1-reviews/batch-086-visual-606-reconciliation.json. "
    "Original-session dependent Claude3008102f-fcab-48aa-8298-7bf950377cc3 and GPT60bd24a1-86d7-476d-a371-9af354cab393 "
    "visual confirmations CLOSED on unchanged teachingf59c65fd/evidence81238670: each actual original model, exit0, "
    "whole common98288byte packet and original report,24 successful serial PNGviews representing76originals via19sheets "
    "plus5originalfileviews. Tool resized sheets1080x2456to879x2000 and originals1080x2400to900x2000; "
    "all24returnedimagepayloadhashes match BETWEEN reviewers, not originalsourcebytes. "
    "No overlaps/nestedtools/edits/newblindcredit. "
    "No actionable visual defect or consequential unresolved teaching claim. Rawおうよ.そ modern usage remains "
    "UNVERIFIED source-only, retained exactly/order, not normalized; onボン/ハン only, kun[]. "
    "N1 meaning needs TWO fallbacks because only凹 curated available; actual Englishlabels "
    "concave;sunken/quasi-;associate rank/commonplace;mediocre/beast;animal and recordedseed604 mosquito/pavilion "
    "are bounded safe displayed choices, not arbitrary-pool certification. Allpool丸/九/凹. "
    "All31scopedHan/fourfamilies including丶/几 readable; exactfallbackface unknown,140rasterprobes not separatePNGs. "
    "Native605 BOTHterminalcase0/no skips/errors; full archive6667318d productionContentSync ONCE/1109kanji/"
    "5064words/118N1/zeroProblems/version86e8cb13aa72ecd0/Roomreadingepoch1;8416runtime+archivehashes "
    "and manifest freshness reverified606. Sevenreciprocalpairs/fourteendirections inclaliases/reused平/例/全,"
    "eight directwordguards,two complete newarticle projections/six changedreused passages,SystemBack/offline,"
    "two queuedkeysぼん/はん persistedGood/done,no kunquestion/log. Three-stroke injectedtrace/giveuprecall "
    "NOT humanhandwriting/MLKit/phone. Owned emulator5580 stopped605; do not relaunch for identical evidence. "
    "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, not latestappmain. "
    "Fetch latestorigin/main, normal nonrewritingmerge, resolve surgically, regenerate derivedmanifest if tree changes, "
    "independently re-review changed substantive teaching and rerun required Python/fullchecks/vocabulary/baseline/"
    "membership/reading/link/budget/manifest and applicable non-skipped Android checks on actualcombinedtree. "
    "Do not merely count premerge checks as integrated acceptance. Normal signing/ownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIPentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfilemedia/safepaths/verifiedownerissue gates remain. No guard/heap increase or productionappchange. "
    "Parent19008 owns runner.lock; verifyliveancestry/session/checkpoint/exactsignedheads/whollycleanworktrees;"
    "NOchild reacquire/delete/unlock. Approvedcontrol/committedsources only; preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. Published112/1228,1116remaining unchanged until actualpublication; "
    "physicalphone/generalrelease/whole-set outstanding; project incomplete. No087 or unreviewed push."
)


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def now():
    return datetime.now().astimezone().isoformat()


def verify_runtime():
    return runpy.run_path(str(C / "checkpoint-native-605.py"))["verify_runtime"]()


def audit_images(label):
    prefix = f"batch-086-visual-606-{label}"
    raw = C / (prefix + ".jsonl")
    record = load(V / (prefix + "-execution.json"))
    assert sha(raw) == record["rawExecutionSha256"]
    required = load(C / "batch-086-visual-606-required.json")
    paths = {}
    image_returns = []
    for line in raw.open(encoding="utf-8-sig"):
        e = json.loads(line)
        d = e.get("data", {})
        if e.get("type") == "tool.execution_start":
            paths[d["toolCallId"]] = d["arguments"].get("path")
        elif e.get("type") == "tool.execution_complete":
            path = paths[d["toolCallId"]]
            binary = d.get("result", {}).get("binaryResultsForLlm", [])
            if path and Path(path).suffix == ".png":
                assert d["success"] and len(binary) == 1
                image = binary[0]
                assert image["type"] == "image" and image["mimeType"] == "image/png"
                data = base64.b64decode(image["data"], validate=True)
                digest = hashlib.sha256(data).hexdigest()
                with Image.open(Path(path)) as original_image:
                    source_size = list(original_image.size)
                with Image.open(io.BytesIO(data)) as returned_image:
                    returned_size = list(returned_image.size)
                    assert returned_image.format == "PNG"
                expected_size = [879, 2000] if Path(path).name.startswith("sheet-") else [900, 2000]
                assert returned_size == expected_size
                image_returns.append({
                    "path": path, "actualReturnedImageSha256": digest,
                    "actualReturnedImageBytes": len(data), "mimeType": image["mimeType"],
                    "sourceImageSha256": sha(Path(path)), "sourceDimensions": source_size,
                    "actualReturnedDimensions": returned_size,
                    "exactSourceImageBytesReturned": digest == sha(Path(path)),
                    "toolResizedImage": True,
                })
    assert [i["path"] for i in image_returns] == [i["path"] for i in required["requiredImages"]]
    assert len(image_returns) == 24
    assert record["exitCode"] == 0 and not record["missingRequiredImages"]
    assert record["completePacketReturned"] and record["originalReportReturnedCompletely"]
    assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
    assert not record["multiToolResponseCount"]
    assert record["actualModels"] == [record["requestedModel"]] == [record["usageCurrentModel"]]
    assert subprocess.run(["pwsh", "-NoProfile", "-Command",
                           f"if (Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                          capture_output=True).returncode == 0
    compressed = V / (prefix + ".jsonl.gz")
    assert not compressed.exists()
    original = raw.read_bytes()
    compressed.write_bytes(gzip.compress(original, mtime=0))
    assert gzip.decompress(compressed.read_bytes()) == original
    # The uncompressed control original remains; Git retains its lossless gzip copy.
    generated_copy = V / (prefix + ".jsonl")
    assert generated_copy.read_bytes() == original
    assert not git("ls-files", "--", str(generated_copy.relative_to(R)))
    generated_copy.unlink()
    coverage = {
        "snapshot": HEAD, "model": record["requestedModel"], "sessionId": record["sessionId"],
        "dependentNotNewBlindInitialCredit": True, "actualImageReturns": image_returns,
        "all24ImagePayloadsDecodedAndDimensionsVerified": True,
        "sourceImagesUnchanged": True,
        "allImageReturnsToolResized": True,
        "allRequiredViewsSerial": True, "wholePacketReturned": True,
        "originalReportReturnedCompletely": True, "processExited": True,
        "rawOriginalSha256": sha(raw), "rawOriginalBytes": raw.stat().st_size,
        "losslessRawArchive": str(compressed.relative_to(R)).replace("\\", "/"),
        "losslessRawArchiveSha256": sha(compressed), "decompressionByteEqualityVerified": True,
        "limits": "Exact successful model image returns and process/range evidence, not comprehension certification.",
    }
    save(V / (prefix + "-coverage.json"), coverage)
    return record, coverage


def prepare():
    state = load(C / "progress.json")
    assert state["checkpoint"] == 605 and state["stage"] == "batch-086-dependent-visual-confirmations-in-progress"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    assert not git("diff", "--name-only") and not git("diff", "--cached", "--name-only")
    runtime = verify_runtime()
    records, coverage = {}, {}
    for label in ["claude", "gpt"]:
        records[label], coverage[label] = audit_images(label)
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    assert coverage["claude"]["actualImageReturns"] == coverage["gpt"]["actualImageReturns"]
    for name in [
        "review-batch-086-visual-606.py", "close-batch-086-visual-606.py",
        "batch-086-visual-606-packet.txt", "batch-086-visual-606-required.json",
        "batch-086-visual-606-claude-prompt.txt", "batch-086-visual-606-gpt-prompt.txt",
        "batch-086-visual-606-claude-image-return-diagnostic.json",
        "batch-086-visual-606-gpt-image-return-diagnostic.json",
    ]:
        target = V / name
        assert not target.exists()
        shutil.copyfile(C / name, target)
    for args, name in [
        (["--help"], "batch-086-visual-606-cli-help.txt"),
        (["help", "config"], "batch-086-visual-606-cli-model-catalog.txt"),
    ]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True)
        assert result.returncode == 0
        (V / name).write_bytes(result.stdout)
    catalog = (V / "batch-086-visual-606-cli-model-catalog.txt").read_text(encoding="utf-8-sig")
    assert "claude-opus-5.5" in catalog and "gpt-6.1-sol" in catalog
    article_paths = [
        "kanji/凡.md", "words/凡例.md", "words/平凡.md", "words/およそ.md",
        "words/全て.md", "kanji/平.md", "kanji/例.md", "kanji/全.md",
    ]
    reconciliation = {
        "schemaVersion": 1, "execution": 606, "batch": "086",
        "status": "dependent-visual-confirmations-closed-awaiting-current-main-integration",
        "evidenceSnapshot": HEAD, "teachingSnapshot": "f59c65fde644ed36958d74495da59a66c1d82570",
        "teachingChanged": False, "nativeArchiveSnapshot": "6667318d9d5bdf8ec8c899db64395e2955612432",
        "independentInitialReviews": "Original602 two blind families remain unchanged and preserved; these606 reports are dependent original-session visual supplements, no new blind credit.",
        "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "processes": {
            label: {k: record[k] for k in [
                "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
                "usageCurrentModel", "reportSha256", "rawExecutionSha256", "actualDistinctImageViews",
                "completePacketReturned", "originalReportReturnedCompletely", "resumedOriginalSession",
                "dependentNotNewBlindInitialCredit", "multiToolResponseCount", "observedToolOverlaps",
            ]} for label, record in records.items()
        },
        "serialReviewerProcessExitVerified": True, "allInternalToolCallsSerial": True,
        "all24ReturnedImagePayloadHashesMatchedBetweenReviewers": True,
        "returnedImagesNotByteIdenticalToSource": True,
        "commonPacketSha256": sha(C / "batch-086-visual-606-packet.txt"),
        "commonPacketBytes": (C / "batch-086-visual-606-packet.txt").stat().st_size,
        "screenshotCoverageEachReviewer": {
            "labelledSheets": 19, "originalCapturesRepresented": 76,
            "separateOriginalFileReads": [
                "n1-086-font-panel-1.png", "n1-086-font-panel-2.png",
                "n1-086-font-panel-3.png", "n1-086-meaning-question.png", "n1-086-legend-02.png",
            ], "extraOriginalReads": 0,
            "limits": "All76 native captures represented in source half-size labelled sheets, but view additionally resizes1080x2456 sheets to879x2000. Five separately opened1080x2400 originalfiles are returned900x2000, NOT actual native pixel size. Original reports use original-size informally for originalfile versus sheet; technically inaccurate, corrected here without rewriting reports. Successful decodedimage returns do not certify comprehension.",
        },
        "verdicts": {
            path: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "renderedComprehensibility": "CLEAN"}
            for path in article_paths
        },
        "findings": [],
        "dispositions": [
            {
                "claim": "Actual image return dimensions differ from source; original-size language and proposed byte-equivalence audit",
                "reportedBy": ["coordinator606 binary-return audit"],
                "status": "resolved",
                "evidence": "Exact actual binaryResultsForLlm base64 decoded for all24views per reviewer: source sheets1080x2456 returned879x2000; source originalfiles1080x2400 returned900x2000. Both models received identical corresponding returnedPNG bytes, not sourcebytes.",
                "decision": "Preserve complete original reports, raw events and failed first source-byte assertion. Correct provenance claims: originalfile read is not nativepixel display. No native-size reviewer claim retained. Fresh reports identify legibility from actual returnedimages; no required pixel-exact inspection gate or unresolved visual claim was established. No unnecessary rerun/crop expansion.",
            },
            {
                "claim": "Initial textual default-distractor availability assumption",
                "reportedBy": ["GPT visual606", "coordinator native605"],
                "status": "resolved",
                "evidence": "Actual native605 N1 question shows English labels concave;sunken/quasi-;associate rank/commonplace;mediocre/beast;animal. Native route and fixture show only凹 curated available in N1, twofallbacks; seeded604 alternatives mosquito/pavilion. All uses丸/九/凹.",
                "decision": "Correct assumption in supplemental ledger, preserve original602 report. No displayed semantic ambiguity; only intended commonplace;mediocre fits凡. Not arbitrary-pool safety.",
                "confidence": "high for bounded tested presentation",
            },
            {
                "claim": "Claude describes meaning choices using corresponding characters rather than literal displayed labels",
                "reportedBy": ["coordinator606 report audit"],
                "status": "resolved",
                "evidence": "Originalsheet17 and originalmeaningquestion show four English labels, not四kanji options. Claude's凹/准/凡/獣 are shorthand identities.",
                "decision": "Record actual labels above; do not rewrite original report or claim glyph options were displayed.",
            },
            {
                "claim": "Heavy Gothic-like几 appearance in some family rows",
                "reportedBy": ["Claude visual606", "GPT visual606 fallback similarity limit"],
                "status": "resolved",
                "evidence": "Originalfilepanel1 freshly viewed by both reviewers and coordinator606, returned900x2000 byview:几/丶 visible and distinguishable from凡/丸/九/凹 across four labelled families. Other panels cover31scopedHan and wordforms.",
                "decision": "No blank/replacement/materially misleading glyph established. Typeface difference not defect; no exact actual fallback face identified or inferred from appearance.",
            },
            {
                "claim": "Full rawreading feedback includesおうよそ without inline source-only flag",
                "reportedBy": ["Claude visual606 Optional", "GPT visual606 rawmetadata/scheduling distinction", "coordinator605"],
                "status": "optional",
                "evidence": "Sheet02/03 show on-key correct feedback then articleprojection; sheet08-10 include table/source-only caveat. Exactfixture/route asserts onlyぼん/はん scheduled and no kunquestion/log, rawmetadata preserved.",
                "decision": "Expected current app fullmetadata rendering, not evidence that raw source-only item was scheduled or verified. Article retains explicit source-only qualification. No content or unauthorized algorithm/UI change required; no broad live-quiz safety claim.",
            },
            {
                "claim": "Claude initial栞 directguard hypothesis",
                "status": "withdrawn", "reportedBy": ["Claude original-session606"],
                "decision": "Reviewer explicitly withdraws. Original dictionary/title-based602 resolution retained.",
            },
            {
                "claim": "Claude initial dotcue,editorialpolicy/synonym,alternateおおよそ,extra compound suggestions",
                "status": "optional", "reportedBy": ["Claude602", "Claude606"],
                "decision": "Remain nonblocking and not implemented. 九 lacks dot, but comparative wording does not assert a dot on九. No new mandatory defect established.",
            },
            {
                "claim": "Original native rendering/route/persistence/offline limits",
                "status": "partially resolved", "reportedBy": ["both original-session606"],
                "decision": "Fresh emulator images resolve bounded legibility/renderedcomprehensibility; supplied native605 terminal evidence supports exact testedconfig routes/persistence/offline. No independent rerun or phone/realnetwork/ownerprogress certification.",
            },
            {
                "claim": "Rawおうよ.そ modern usage",
                "status": "unresolved", "verdict": "UNVERIFIED",
                "decision": "Explicit source-only non-assertion retained; not a consequential asserted modern teaching claim and not quizscheduled. Never normalize toおおよ.そ or call proven typo.",
            },
        ],
        "modelContributionComparison": {
            "shared": "All24images/commonpacket/originalreport; all31Han/fourfamilies legible; two newarticles and six diffprojections clear; expected rawmetadatafeedback not scheduling; emulator/phone/handwriting/fallbackface limits. No established required content fix.",
            "gpt": "Explicitly corrects original defaultcuratedavailability assumption; equivalent fact already in commonnativepacket/coordinator605, not unique independent discovery. Perfile threefacet table.",
            "claude": "Optional feedback qualification placement and heavier几 appearance; GPT discusses equivalent fullmetadata and fallback similarity limits. No unique verified mandatory defect.",
            "limits": "Dependent matched visual confirmation, not new blind study/generalmodelbenchmark. Equivalent observations across Findings/Optional/Limits compared.",
        },
        "actionableRemainingFindings": 0, "consequentialUnresolvedTeachingClaims": 0,
        "textualReviewClosed": True, "dependentVisualConfirmationClosed": True,
        "runtimeAccepted": False, "runtimePublished": False,
        "runtimeVerification": runtime,
        "nativeRerunThisCheckpoint": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
    }
    save(V / "batch-086-visual-606-reconciliation.json", reconciliation)
    evidence = {
        "schemaVersion": 1, "execution": 606, "batch": "086",
        "status": reconciliation["status"], "startingState": state["execution606StartingState"],
        "evidenceSnapshot": HEAD, "teachingSnapshot": reconciliation["teachingSnapshot"],
        "androidHead": APP, "productionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "androidQualification": "TESTONLY sibling; unchanged production; not latest app main.",
        "reconciliation": "docs/n1-reviews/batch-086-visual-606-reconciliation.json",
        "originalInitialReportsPreserved": True,
        "dependentOriginalSessionModels": reconciliation["models"],
        "dependentVisualConfirmationClosed": True,
        "independentInitialReviewCreditAdded": 0,
        "actualRequiredImageViewsPerReviewer": 24,
        "allReturnedImageBytesMatchedBetweenReviewers": True,
        "allReturnedImagesToolResizedNotOriginalPixels": True,
        "eachOriginalReportAndCommonPacketReturnedCompletely": True,
        "reviewersLaunchedSeriallyAndExited": True,
        "native605TerminalPerCaseStatuses": [0, 0], "native605Failures": 0, "native605Skips": 0,
        "freshNativeExecuted": False, "nativeOwnedEmulatorRemainsStopped": True,
        "runtimeVerification": runtime, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "publishedAdditions": 112, "remainingAdditions": 1116,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False,
        "validation": "Evidence-only change: no runtime content edit or new teaching; exact manifest freshness and all8416 current+archive payload hashes reverified. No new Android/native/full Python-suite execution claimed.",
        "diagnostics": [
            "First closing audit correctly rejected false proposed source-byte equality before writing final evidence. Actual view tool resizes images. Audited decoded actualPNG dimensions/hashes instead; all24 corresponding returns identical between models, sourceimages unchanged. Original reviewer native-size wording corrected in supplemental ledger, reports/raw events preserved.",
            "Read-only process absence query ended exit1 because Get-Process found neither exited reviewer; explicit Python absence checks separately passed. Not permission denial, test failure or reason to restart a reviewer.",
        ],
        "limits": [
            "Both models inspected all76 captures via19source-halfsize labelled sheets returned879x2000, plus5originalfile views returned900x2000. Not actualnativepixels; original reports informal original-size language corrected in ledger. Exact returnedbinarypayload hashes match between reviewers only, not sourcebytes; successful views do not certify comprehension.",
            "Original605 execution is supplied evidence, not fresh606rerun. Emulator/fixtureisolatedsynthetictransport/injectedtrace not phone/ownerprogress/livenetwork/humanhandwriting/MLKit.",
            "Rawおうよ.そ modern usage UNVERIFIED source-only; exactfallbackface unknown; arbitrarypool safety unproven.",
            "Combinedcurrentmain/merge/re-reviewofchangedteaching/fullrequiredchecks/normalsigning/ownerfastforward/CI/EVERYimmutableZIPhash/budgets/publication issue gates remain.",
        ], "nextAction": NEXT,
    }
    save(S / "execution-606.json", evidence)
    inventory = {}
    for path in sorted(V.glob("batch-086-visual-606-*")):
        inventory[str(path.relative_to(R)).replace("\\", "/")] = sha(path)
    save(S / "batch-086-visual-606-artifact-hashes.json", inventory)
    print(json.dumps({
        "status": reconciliation["status"], "models": reconciliation["models"],
        "allReturnedImagePayloadsMatchedBetweenModels": 24, "runtimeHashesVerified": runtime["runtimePayloadHashesVerified"],
        "remainingActionableFindings": 0, "artifacts": len(inventory),
    }))


def finish():
    state = load(C / "progress.json")
    before = load(L / "progress-before-606.json")
    assert state["checkpoint"] == 605 and state["stage"] == "batch-086-dependent-visual-confirmations-in-progress"
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "HEAD", root=A) == APP
    runtime = verify_runtime()
    for name, digest in load(S / "batch-086-visual-606-artifact-hashes.json").items():
        assert sha(R / name) == digest
        raw = subprocess.check_output(["git", "-C", str(R), "show", f"HEAD:{name}"])
        assert hashlib.sha256(raw).hexdigest() == digest, name
    issue = load(C / "batch-086-visual-606-issue-receipt.json")
    body = (C / "batch-086-visual-606-issue-body.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    checkpoint = {
        "schemaVersion": 1, "execution": 606, "checkpoint": 606, "batch": "086",
        "savedCommit": head, "signature": "G", "status": "continue",
        "stage": "dependent-visual-closed-awaiting-current-main-integration",
        "evidence": "docs/n1-sources/execution-606.json",
        "reconciliation": "docs/n1-reviews/batch-086-visual-606-reconciliation.json",
        "dedicatedWorktreesClean": True, "textualReviewClosed": True,
        "dependentVisualConfirmationClosed": True,
        "dependentOriginalSessionModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "actualReturnedImagePayloadsDecodedPerReviewer": 24,
        "allReturnedImagePayloadHashesMatchBetweenModels": True,
        "toolResizingDisclosed": True, "serialProcessesExited": True,
        "originalReportsAndCommonPacketReturnedCompletely": True,
        "independentInitialReviewCreditAdded": 0,
        "native605TerminalPerCaseStatuses": [0, 0], "freshNativeExecuted": False,
        "runtimeVerification": runtime, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [], "optionalHistoricalHelpersAccessed": False,
        "publishedAdditions": 112, "remainingAdditions": 1116, "lastPublishedCommit": state["lastPublishedCommit"],
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(C / "batch-086-visual-606-issue-receipt.json"),
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": now(), "nextAction": NEXT,
    }
    state["execution606StartingState"]["status"] = "signed-local-dependent-visual-checkpoint-complete"
    state["execution606CoordinatorCheckpoint"] = checkpoint
    state["batch086DependentVisualCheckpoint"] = checkpoint
    state.update(checkpoint=606, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    for key, value in before.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert state[key] == value, key
    save(C / "progress.606.tmp", state)
    assert load(C / "progress.606.tmp") == state
    (C / "progress.606.tmp").replace(C / "progress.json")
    assert load(C / "progress.json") == state
    save(L / "final-verification-606.json", checkpoint)
    print(json.dumps({key: checkpoint[key] for key in [
        "checkpoint", "savedCommit", "stage", "issueUpdate", "originalRootKeysCompared",
    ]}))


if __name__ == "__main__":
    {"prepare": prepare, "finish": finish}[sys.argv[1]]()
