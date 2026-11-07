import base64
import gzip
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("visual624", C / "review-batch-088-visual-624.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, N, L = review.R, review.A, review.V, review.N, review.L
HEAD, ANDROID, TEACHING = review.HEAD, review.ANDROID, review.TEACHING
load, save, sha, git = review.load, review.save, review.sha, review.git
NEXT = (
    "SAME088 bounded current-main integration and combined-tree acceptance next; no089. "
    "Read docs/n1-sources/execution-624.json and docs/n1-reviews/batch-088-visual-reconciliation-624.json. "
    "Original Claude915d0745 and GPT11925f67 dependent visual confirmations CLOSED on unchanged teaching42077c31/"
    "evidence7e514fe5. Both actual original models viewed11PNGs (8mapped sheets/all46captures plus3fontpanels). "
    "Claude initial first2TEXTviews overlapped7-12ms, preserved honestly; all11IMAGEviews serial. "
    "SameClaude process exited; bounded original-session correction freshly reread BOTHtexts in2strictlyserialcalls/"
    "exit0, unchanged conclusions; then GPT13strictlyserialcalls/exit0. No overlappingreviewerprocesses ornewblindcredit. "
    "ReturnedPNGpayloads decoded/dimensions recorded, not assumed sourcebyteidentity or112PaintPNGs. "
    "Botharticles renderedCLEAN with inheritedtextualcorrectness/coverage; noactionabledefect. "
    "Actual N1pictured/Allproductionreceipt choices victorysong;triumph versus凡commonplace;mediocre/"
    "凸convex;protruding/凹concave;sunken, all3curatedavailable/zero fallback; not futurecustompool certification. "
    "All27Han/fourComposefonts including几/豈/鬨 visible; exactfallbackface unknown. "
    "Rawonガイ/カイ+kunかちどき/やわらぐ retained/order; selectedonガイonly, explicitkun[]. "
    "Inherited623native BOTHterminalcase0/no skips, fullarchivee445d826 productionContentSyncONCE/"
    "1111kanji5067words120N1zeroProblems/versionafff40af0e155dbe/epoch1; singleがいGood/done,12stroke"
    "injectedtrace/practice/recallgiveup, botharticles/1mappedpair/2directions/4directguards/SystemBack/offline. "
    "No freshnative624, humanhandwriting/MLKit/phone claim. QualifiedTESTONLYAndroid1c1b7bf4 retains "
    "productionf9b59a2, not latestappmain. Recheck freshmain/exactsignedheads/whollycleanworktrees/"
    "source-membership/fullbaseline-preservation/links/readings/guards/stroke-font dispositions; "
    "normalnonrewriting originmainmerge, regenerate derivedmanifest if changed, independently rereview "
    "substantiveteachingchanges. Required fullPython/vocabularyconsistency/manifestfreshness/budget/audits/"
    "applicablenonskippedAndroid on actualcombinedtree before normallysignedreviewclosed acceptance. "
    "Then normalownerfastforward/terminalgreenCI/EVERYimmutablepublicZIP runtimeentryhash/original"
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/ownerissue gates. "
    "No publication until prerequisites pass; no089/forcepush/amend/guardheapincrease/productionappchange. "
    "Parent19008 ownsrunner.lock: verify liveancestry/currentrunnersession/checkpoint/signedheads/cleanstate; "
    "NOchild reacquire/delete/unlock. Approvedcontrol/committedsources only, not optionalhistoricalsessionrecipes. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Published114/1228,1114remaining "
    "unchanged; physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def verify_runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    verified = {}
    for kind, section in manifest.items():
        if isinstance(section, dict):
            for path, expected in section.items():
                if isinstance(expected, str) and len(expected) == 64:
                    file = R.joinpath(*path.split("/"))
                    actual = sha(file) if kind in {
                        "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                    } else sha256(file)
                    assert actual == expected, path
                    verified[path] = expected
    assert len(verified) == 8423
    assert manifest["contentVersion"] == "afff40af0e155dbe"
    assert not git("diff", TEACHING, "HEAD", "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")
    return {"runtimeHashesVerified": len(verified),
            "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json")}


def process_record(label):
    record = load(C / f"batch-088-visual-624-{label}-execution.json")
    model = review.SESSIONS["claude" if label.startswith("claude") else "gpt"][0]
    assert record["actualModels"] == [model] and record["usageCurrentModel"] == model
    assert record["exitCode"] == 0 and not record["unfinishedTools"]
    assert record["allAssignedResourcesSuccessfullyReturned"]
    assert subprocess.run(["pwsh", "-NoProfile", "-Command",
                           f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                          capture_output=True).returncode == 0
    return record


def audit_images(label):
    prefix = C / f"batch-088-visual-624-{label}"
    record = process_record(label)
    assert sha(prefix.with_suffix(".jsonl")) == record["rawSha256"]
    assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
    images, paths, active, overlaps = [], {}, set(), []
    for line in prefix.with_suffix(".jsonl").open(encoding="utf-8-sig"):
        event = json.loads(line)
        data = event.get("data", {})
        if event["type"] == "tool.execution_start":
            key = data["toolCallId"]
            path = data["arguments"].get("path")
            paths[key] = path
            if active:
                overlaps.append({"starting": path, "active": [paths[k] for k in active]})
            active.add(key)
        elif event["type"] == "tool.execution_complete":
            key = data["toolCallId"]
            active.remove(key)
            path = paths[key]
            if path and path.endswith(".png"):
                assert data["success"]
                payloads = data.get("result", {}).get("binaryResultsForLlm", [])
                assert len(payloads) == 1
                payload = payloads[0]
                assert payload["type"] == "image" and payload["mimeType"] == "image/png"
                raw = base64.b64decode(payload["data"], validate=True)
                digest = hashlib.sha256(raw).hexdigest()
                with Image.open(io.BytesIO(raw)) as image:
                    image.load()
                    assert image.format == "PNG"
                    returned_dimensions = list(image.size)
                with Image.open(path) as image:
                    source_dimensions = list(image.size)
                images.append({
                    "path": path, "sourceImageSha256": sha(Path(path)),
                    "sourceDimensions": source_dimensions,
                    "actualReturnedImageSha256": digest,
                    "actualReturnedImageBytes": len(raw),
                    "actualReturnedDimensions": returned_dimensions,
                    "exactSourceImageBytesReturned": digest == sha(Path(path)),
                    "toolResizedImage": returned_dimensions != source_dimensions,
                })
    assert not active
    if label == "claude":
        assert len(overlaps) == 1
        assert overlaps[0]["starting"] == str(review.PACKET)
        assert overlaps[0]["active"] == [str(V / "batch-088-initial-claude.md")]
        assert len(record["toolCalls"]) == 13
    else:
        assert not overlaps and len(record["toolCalls"]) == 13
    assert [item["path"] for item in images] == list(map(str, review.IMAGES))
    result = {
        "snapshot": HEAD, "model": record["requestedModel"], "sessionId": record["sessionId"],
        "dependentNotNewBlindInitialCredit": True,
        "actualImageReturns": images, "allElevenPayloadsDecoded": True,
        "allImageViewsSerial": True, "allToolViewsSerial": not overlaps,
        "textReadOverlaps": overlaps,
        "wholePacketReturned": True, "ownOriginalReportReturned": True,
        "processExited": True,
        "limits": "Resource and payload audit, not comprehension certification. Source images and actual resized returns are distinguished.",
    }
    return record, result


def archive():
    review.frozen()
    assert not (V / "batch-088-visual-reconciliation-624.json").exists()
    records, coverage = {}, {}
    for label in ["claude", "gpt"]:
        records[label], coverage[label] = audit_images(label)
    correction = process_record("claude-serial-text")
    assert not correction["observedToolOverlaps"] and len(correction["toolCalls"]) == 2
    assert records["claude"]["completedAt"] < correction["startedAt"]
    assert correction["completedAt"] < records["gpt"]["startedAt"]
    assert all(a["actualReturnedImageSha256"] == b["actualReturnedImageSha256"]
               for a, b in zip(coverage["claude"]["actualImageReturns"],
                               coverage["gpt"]["actualImageReturns"]))
    runtime = verify_runtime()
    prior = load(R / "docs" / "n1-sources" / "execution-623.json")
    for receipt in prior["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    receipts = []
    sources = [Path(__file__), C / "review-batch-088-visual-624.py", review.PACKET,
               C / "batch-088-visual-624-inputs.json",
               C / "batch-088-cli-help-execution-624.txt",
               C / "batch-088-cli-config-help-execution-624.txt",
               C / "batch-088-cli-config-reference-execution-624.txt"]
    for label in ["claude", "claude-serial-text", "gpt"]:
        prefix = C / f"batch-088-visual-624-{label}"
        sources.extend(prefix.with_suffix(suffix) for suffix in [
            ".md", ".prompt.txt", ".stderr.txt", ".usage.json"])
        sources.append(C / (prefix.name + "-execution.json"))
        raw = prefix.with_suffix(".jsonl")
        target = V / (raw.name + ".gz")
        assert not target.exists()
        target.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw.read_bytes()
        receipts.append({"source": str(raw), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(raw), "archiveSha256": sha(target),
                         "losslessGzip": True})
    for source in sources:
        target = V / source.name
        assert not target.exists()
        shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(target)})
    for label, item in coverage.items():
        save(V / f"batch-088-visual-624-{label}-coverage.json", item)
    reconciliation = {
        "schemaVersion": 1, "execution": 624, "batch": "088",
        "evidenceSnapshot": HEAD, "teachingSnapshot": TEACHING,
        "status": "dependent-visual-review-closed-awaiting-combined-acceptance",
        "teachingChanged": False, "originalInitialReviewsPreserved": True,
        "newBlindInitialReviewCredit": False, "processes": records,
        "claudeSerialTextCorrection": correction,
        "serialReviewerProcessesExited": True,
        "eachOriginalReportPreservedBeforeNextLaunch": True,
        "eachReviewerImagesDecoded": 11,
        "allImageViewsSerial": True,
        "entireOriginalClaudeToolRunSerial": False,
        "claudeTextOverlapRemediation": {
            "originalOverlap": records["claude"]["observedToolOverlaps"],
            "actualOverlapScope": "Own initial report and visual packet text reads only; starts00:43:14.565Z, completions.572Z/.577Z. All eleven image reads serial.",
            "status": "corrected-with-preserved-original-process-deviation",
            "remedy": "Same original model/session freshly reread both text resources in two strictly serial calls after first process exited; conclusions unchanged. Then original GPT launched only after corrective process exited.",
            "historicalViolationNotErased": True,
            "limits": "No claim the first entire run complied; no repeated image credit and no weakening of linguistic/native/publication acceptance.",
        },
        "allAssignedResourcesReturned": True,
        "sameActualReturnedImageHashesAcrossReviewers": True,
        "imageCoverageRecords": {label: f"docs/n1-reviews/batch-088-visual-624-{label}-coverage.json"
                                 for label in coverage},
        "verdicts": {path: {"correctness": "CLEAN-inherited-textual",
                            "scopedCoverage": "CLEAN-inherited-textual",
                            "renderedComprehensibility": "CLEAN"}
                     for path in ["kanji/\u51f1.md", "words/\u51f1\u65cb.md"]},
        "findings": [],
        "dispositions": [
            {"claim": "Actual glyph/article/session rendering unverified in initial textual reviews",
             "status": "resolved", "scope": "bounded supplied API35 captures",
             "evidence": "Both original reviewers decoded all eleven requested PNGs: eight mapped sheets cover46captures and three original font panels. All27Han including U+51E0/U+8C48/U+9B28 readable/distinguishable in four production font selections; both complete article projections readable.",
             "limits": "Tool resized payloads recorded in coverage. No fallback font-face, native-speaker, physical-phone or112PaintPNG claim."},
            {"claim": "N1/All fallback could offer overlapping victory-related choices",
             "status": "resolved", "scope": "two tested production configurations only",
             "evidence": "Both inspected pictured victorysong;triumph versus 凡commonplace;mediocre/凸convex;protruding/凹concave;sunken. N1 and All production route receipts independently record exactly these four identities,3curatedavailable/0fallback.",
             "limits": "All configuration is supplied JSON, not a separately pictured All question; no futurecustompool/oldclient certification."},
            {"claim": "Side-scroll table clipping, word wrapping and full-readings feedback",
             "status": "optional",
             "evidence": "Complementary captures expose complete table columns with explicit scrolling instruction. Character-dictio/nary wrap cosmetic; feedback full readings followed by article explanation. No established content defect.",
             "decision": "No article/app edit. Preserve original observations without claiming every screen qualifies all source-only readings."},
            {"claim": "Original wording suggestions, 山 target and destinationへ source limitation",
             "status": "optional",
             "evidence": "Original textual reconciliation620 already preserves and adjudicates these: three nonblocking wordings, mechanical target verification and coordinator Tofugu directional-particle evidence. Claude did not independently verify them in visual follow-up; this remains a reviewer evidence limit, not a new unresolved construction claim.",
             "decision": "No content edit or new source-review credit; retain both original reports and prior evidence-based dispositions."},
            {"claim": "Native import, persisted grade/key queues and route assertions",
             "status": "resolved", "scope": "supplied native623 receipts only",
             "evidence": "Both distinguish actual visible selection/question/feedback/done/drawing/article screens from imported counts, queues/persistence/offline/Back assertions supplied by passing native tests.",
             "limits": "Not reviewer-executed tests, real handwriting, offlineMLKit, physical phone or new native624 execution."},
        ],
        "modelContributionComparison": {
            "sharedVerifiedDefects": [], "claudeUniqueVerifiedDefect": None,
            "gptUniqueVerifiedDefect": None,
            "sharedObservations": "Both no actionable defect; readable fonts/articles, bounded distinct choices, explicit scrollable table and separate source-only readings.",
            "optionalOrLimits": "Claude optional feedback/wrapping and previous wordings are not verified defects or general model-ranking evidence; previous textual limitations preserved. Process deviation belongs to execution audit, not linguistic model contribution.",
            "limits": "Dependent matched visual sample, inherited text conclusions, not a new blind review or benchmark.",
        },
        "runtime": runtime, "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "limits": [
            "No fresh full lexical/source review or independent Git/upstream verification.",
            "Eleven decoded image payloads per original reviewer; actual tool resizing and dimensions recorded, not byte-identical source views.",
            "108individual+4wholewordPaint probes recycled, not separately viewed exportedPNGs.",
            "No fresh native/Android624 execution; qualified TESTONLY app retains productionf9b59a2 and is not latestappmain.",
            "Injectedtrace/giveup not humanhandwriting/offlineMLKit/phone; no physicalphone/native-speaker/learningeffectiveness certification.",
            "Initial Claude two text views overlapped; complete original deviation preserved and corrected with same-session strictlyserial text rereads, not erased.",
            "Combined current-main acceptance/normal signing/publication/terminalCI/every immutableZIP hash/phone/generalrelease/whole-set remain later gates.",
        ],
        "nextAction": NEXT,
    }
    save(V / "batch-088-visual-reconciliation-624.json", reconciliation)
    save(R / "docs" / "n1-sources" / "execution-624.json", {
        "schemaVersion": 1, "execution": 624, "batch": "088",
        "startingState": load(C / "progress.json")["execution624StartingState"],
        "snapshot": HEAD, "teachingSnapshot": TEACHING, "status": reconciliation["status"],
        "runtime": runtime,
        "reconciliation": "docs/n1-reviews/batch-088-visual-reconciliation-624.json",
        "receipts": receipts, "runtimeChanged": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "actualNewPermissionDenials": [],
        "diagnostics": [
            "Installed1.0.107 config --help no longer enumerates model IDs. Read actual copilot help config; both original models explicitly listed. No guessed model or Auto substitution.",
            "First Claude wrapper exited1 after completed reviewer exit0 because two initial text views overlapped. Original report/raw/process preserved. All11image reads serial. Same-session bounded2text strictlyserial correction exit0 completed before GPT13serialcalls/exit0. No acceptance bypass or historical rewrite.",
        ],
        "publishedAdditions": 114, "remainingAdditions": 1114,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Archived complete reports, actual image payload audits and original process correction; runtime unchanged.")


def finalize():
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    runtime = verify_runtime()
    evidence = load(R / "docs" / "n1-sources" / "execution-624.json")
    for receipt in evidence["receipts"]:
        archived = R.joinpath(*receipt["archive"].split("/"))
        assert sha(archived) == receipt["archiveSha256"]
        if receipt.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(archived.read_bytes())).hexdigest() == receipt["sourceSha256"]
    body = (C / "batch-088-visual-624-issue-body.txt").read_text(encoding="utf-8-sig")
    posted = load(C / "batch-088-visual-624-issue-posted.json")
    receipt = load(C / "batch-088-visual-624-issue-receipt.json")
    assert posted["id"] == receipt["id"]
    assert posted["body"] == receipt["body"] == body
    assert posted["user"]["login"] == receipt["user"]["login"] == "stop-cran"
    state = load(C / "progress.json")
    before = load(L / "progress-before-624.json")
    assert state["checkpoint"] == 623
    assert state["stage"] == "batch-088-dependent-visual-confirmations"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 624, "checkpoint": 624, "batch": "088",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "visual-review-closed-awaiting-combined-acceptance",
        "evidence": "docs/n1-sources/execution-624.json",
        "reconciliation": "docs/n1-reviews/batch-088-visual-reconciliation-624.json",
        "runtime": runtime, "independentVisualConfirmationsComplete": True,
        "originalSessionsReused": {label: session for label, (_, session) in review.SESSIONS.items()},
        "actualModels": [model for model, _ in review.SESSIONS.values()],
        "eachReviewerPngsDecoded": 11, "allImageViewsSerial": True,
        "claudeInitialTextOverlapPreserved": True, "claudeCorrectiveSerialTextCalls": 2,
        "gptAllViewsSerial": True, "gptViewCalls": 13,
        "serialReviewerProcessesExited": True, "actionableFindings": [],
        "runtimeChanged": False, "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "publishedAdditions": 114, "remainingAdditions": 1114,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueBodySha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update({"checkpoint": 624, "status": "continue", "stage": checkpoint["stage"],
                  "nextAction": NEXT, "blocker": None})
    state["execution624CoordinatorCheckpoint"] = checkpoint
    state["batch088VisualReviewCheckpoint"] = checkpoint.copy()
    temporary = C / "progress-execution-624.tmp"
    save(temporary, state)
    temporary.replace(C / "progress.json")
    final = load(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert final[key] == value, key
    save(L / "checkpoint-final-624.json", checkpoint)
    print(json.dumps({key: checkpoint[key] for key in [
        "checkpoint", "status", "stage", "savedCommit", "runtime",
        "ownerAuthorAndBodyVerified", "allOriginalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
