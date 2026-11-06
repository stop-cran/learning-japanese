import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
N = V / "batch-080-native"
LOG = C / "logs" / "7c021a91-7f02-420f-a4bb-b5817a498af3"
HEAD = "2bfc8456f33d1625509321e1e946f1402d5eb672"
TEACHING = "3f883347e81422abce490ee633e874be55ef01ad"
NEXT = (
    "SAME080 combined-current-main acceptance/integration/publication ONLY next, then persist/yield; "
    "no081 or second runner. Read docs\\n1-sources\\execution-544.json and "
    "docs\\n1-reviews\\batch-080-visual-reconciliation.json. Two serial original-session different-family "
    "dependent visual confirmations closed on unchanged teaching3f883347/evidence2bfc8456: "
    "ClaudeOpus5.5 a3b94466-63e4-4403-a67d-3249751e5a1b then GPT6.1Sol "
    "27fb4006-7e5d-4d5c-aabb-c8316fb8f334. Each host-dispatched28serialCLIturns: "
    "completepacket+26distinctoriginalPNGgroups covering49captures, thenzero-tool completefinalreport; "
    "onechild/resource, exit/archive beforeNextfamily; no nested/concurrenttools. Actual source1080x2400 "
    "andmodelvisiblepayloads separately retained; view automatically resizes, not all sourcebytes "
    "returned. Preserve coordinator's initial overstrict raw-byte-equality assertion and qualified "
    "transport recovery, NOTpermissiondenial or rejected linguisticreview. Both articles冴/冴える "
    "correctness/scopedcoverage/boundedvisualCLEAN; noactionablefinding. Claude final synthesis uses "
    "own compressedsummary forresources1-12, not liveoriginalpixels; preserve completeperturnnotes. "
    "All30Han/fourproductionfamilies/readable冫冱氵; fallbackface notidentified. Complementary "
    "horizontaltablestates, notallcolumnsoneframe; no generalizedUIcertification. Inherit fresh539 "
    "textualreview/540HOST3+1zeroskips/543native2terminal0 without rerun absent new concern. "
    "Exactfull0d2c9aee archive through productionContentSyncONCE1092kanji5048words112N1/"
    "version4572f7b1d0d95059/zeroProblems/epoch1. Full+Lite fullゴコ/さ.えるこお.るひ.える "
    "unchanged; selectedon[]/kun[さ.える], offeredさえる/goodlog/Done1of1. "
    "Onepairtwodirections/SystemBack/offline/N1selection/actualmeaningchoices passed; finalsemanticsdump "
    "isloading, notsettledroute/persistenceproof. "
    "Seveninjectedreferencepaths/ungradedtrace/shape-onlycomparison/giveuprecallgrade1 NOT "
    "humanhandwriting/successfulrecall/MLKitrecognition/modeldownload; offline model unavailable. "
    "120individual+4wholewordPaint assertions NOT124PNGreads; seededdisposableschedule NOTownerprogress. "
    "Owned543emulator5580 stopped; owner5556 untouched. HOST-only2GiBinit NEVERnative; noheap/guardchanges. "
    "Fetch latestoriginmain; nonrewritingmerge onlyifneeded, regenerate/revalidate actualcombinedtree "
    "with requiredPython/vocabulary/manifest/budget/baseline/link/membership/applicableAndroidchecks; "
    "independentlyreview substantiveteaching changes. Normal signing, authorizedownerfastforward, "
    "verifyremoteSHA/terminalgreenCI/EVERYimmutableZIPruntimeentryhash and original18000entries/"
    "42compressed80inflated56retainedMiBguards; ownerissue60verifiedreceipt beforecountingpublished. "
    "Durablecontrolhelpers/committedpackets/approvedinputsonly; skipoptionalhistoricalsessionrecipes. "
    "PreserveFULLlivehistory/source/lookup/citation/readdepth/review/process/denial/OOM/viewport/phone "
    "limits. Actualnewdenial/signinghang preserve/report/yield, no retry/workaround. "
    "Published106/1228,remaining1122/latest079b120125ae5cdbfe9f3bcb1b0a7ae8a61e422ec8d; "
    "local107thadditionNOTpublished. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/"
    "whole-set outstanding. Noauthoragent/concurrentheavywork/unreviewedpush/nextbatch/secondrunner."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def now():
    return datetime.now().astimezone().isoformat()


def hashes():
    manifest = load(R / "manifest.json")
    count = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            path = R.joinpath(*name.split("/"))
            data = path.read_bytes()
            binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
            canonical = data if binary else data.replace(b"\r\n", b"\n")
            assert hashlib.sha256(canonical).hexdigest() == digest, name
            count += 1
    assert count == 8366
    return manifest, count


def record():
    spec = importlib.util.spec_from_file_location("visual", C / "review-batch-080-visual.py")
    visual = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(visual)
    freeze = visual.verify_freeze()
    reconciliation = load(V / "batch-080-visual-reconciliation.json")
    assert reconciliation["actionableRemainingFindings"] == 0
    assert reconciliation["consequentialUnresolvedScopedTeachingFindings"] == 0
    reviews = {}
    prior_end = None
    for family in ["claude", "gpt"]:
        prefix = "batch-080-visual-" + family
        receipt = load(V / (prefix + "-execution.json"))
        assert receipt["processAndCoverageAccepted"] and receipt["exitCode"] == 0
        assert receipt["actualModels"] == [receipt["requestedModel"]]
        assert sha(V / (prefix + ".md")) == receipt["reportSha256"]
        assert sha(Path(receipt["rawExecutionLocation"])) == receipt["rawExecutionSha256"]
        assert len(receipt["turns"]) == 28 and receipt["completePacketReturned"]
        assert receipt["distinctImagePayloadsVerified"] == 26
        if prior_end:
            assert datetime.fromisoformat(prior_end) < datetime.fromisoformat(receipt["startedAt"])
        prior_end = receipt["completedAt"]
        for i, row in enumerate(receipt["turns"]):
            assert row["singleResourceAccepted"] and row["exitCode"] == 0
            assert row["actualModels"] == receipt["actualModels"]
            if i:
                assert datetime.fromisoformat(receipt["turns"][i-1]["completedAt"]) < datetime.fromisoformat(row["startedAt"])
            if "imagePayload" in row:
                image = row["imagePayload"]
                assert sha(Path(row["resource"])) == image["sourceSha256"]
                assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                assert visual.image_transport_valid(row)
        reviews[family] = {
            "sessionId": receipt["sessionId"], "actualModels": receipt["actualModels"],
            "startedAt": receipt["startedAt"], "completedAt": receipt["completedAt"],
            "exitCode": 0, "serialChildProcesses": 28, "completePackets": 1,
            "distinctImages": 26, "sourceByteIdenticalImages": receipt["sourceByteIdenticalImages"],
            "reportSha256": receipt["reportSha256"], "executionReceiptSha256": sha(V / (prefix + "-execution.json")),
            "rawExecutionSha256": receipt["rawExecutionSha256"],
            "readDepthQualification": reconciliation["reviewReadDepth"][family],
        }
    manifest, count = hashes()
    assert not git("status", "--porcelain", root=R.parent / "kanji-cards-android")
    batch = load(S / "batch-080-progress.json")
    assert batch["textualReviewClosed"] and batch["nativeExecutionCases"] == 2
    original_batch = json.loads(git("show", f"{HEAD}:docs/n1-sources/batch-080-progress.json"))
    batch.setdefault("preVisual544AcceptanceState", {
        key: original_batch[key] for key in ["status", "limits", "independentVisualAcceptance"]
    })
    batch["status"] = "bounded-native-and-visual-closed-awaiting-integration"
    batch["independentVisualAcceptance"] = True
    batch["limits"] = " ".join(reconciliation["limits"])
    batch["visualReviewCheckpoint"] = {
        "execution": 544, "reviewedTeachingSnapshot": TEACHING,
        "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "reconciliation": "docs/n1-reviews/batch-080-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-080-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "runtimePublished": False,
        "actionableRemainingFindings": 0, "sourceCaptures": 49, "eachReviewerDistinctPngs": 26,
    }
    batch["nextAction"] = NEXT
    save(S / "batch-080-progress.json", batch)
    whitespace = subprocess.run(
        ["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check"],
        capture_output=True, encoding="utf-8", check=False,
    )
    exceptions = {
        "docs/n1-reviews/batch-080-visual-source-packet.txt",
        "docs/n1-reviews/batch-080-visual-models-execution-544.txt",
    }
    warnings = [line for line in whitespace.stdout.splitlines() if line.startswith("docs/")]
    assert whitespace.returncode in (0, 2)
    assert all(any(line.startswith(name + ":") for name in exceptions) for line in warnings)
    assert all(re.fullmatch(r"\+\d+: ", line) for line in whitespace.stdout.splitlines() if line.startswith("+"))
    staged = git("diff", "--cached", "--name-only", "-z").split("\0")
    checked = [name.replace("/", "\\") for name in staged if name and name not in exceptions]
    subprocess.run(
        ["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check", "--", *checked],
        check=True, capture_output=True, encoding="utf-8",
    )
    save(V / "batch-080-visual-whitespace-disposition.json", {
        "fullStagedCheckExitCode": whitespace.returncode, "warnings": warnings,
        "targetedOtherStagedFilesExitCode": 0, "targetedOtherStagedFiles": len(checked),
        "decision": "Preserve frozen exact source packet numbered empty lines and verbatim model-catalog blank EOF. Do not edit evidence already returned to reviewers. No other staged whitespace defect.",
        "frozenPacketSha256": freeze["packetSha256"],
    })
    recipe_dir = N / "execution-544-recipes"
    recipe_dir.mkdir(exist_ok=True)
    for name in ["review-batch-080-visual.py", "close-batch-080-visual.py", "post-execution-544.ps1"]:
        shutil.copyfile(C / name, recipe_dir / name)
    shutil.copyfile(C / "batch-080-visual-claude-turns" / "processes-before-transport-classification.json",
                    recipe_dir / "processes-before-transport-classification.json")
    for label in ["validate", "manifest"]:
        shutil.copyfile(LOG / f"{label}-544.txt", N / f"execution-544-{label}.txt")
    assert (LOG / "validate-544.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    assert "version 4572f7b1d0d95059" in (LOG / "manifest-544.txt").read_text(encoding="utf-8")
    files = sorted(V.glob("batch-080-visual-*"))
    for family in ["claude", "gpt"]:
        files += sorted((N / ("visual-" + family + "-returned")).glob("*.png"))
    files += sorted(recipe_dir.iterdir()) + [
        S / "batch-080-progress.json", N / "execution-544-validate.txt", N / "execution-544-manifest.txt",
    ]
    evidence = {
        "schemaVersion": 1, "execution": 544, "checkpoint": 544, "batch": "080",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING, "recordedAt": now(),
        "nativeEnvelopeSnapshot": "0d2c9aee6de9e4f430935b38e31228db4bd47908",
        "authorization": load(LOG / "starting-state-544.json")["authorization"],
        "freshOriginMain": git("rev-parse", "origin/main"), "reviews": reviews,
        "reconciliation": "docs/n1-reviews/batch-080-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-080-visual-reconciliation.json"),
        "bothOriginalFamilyExecutionsSerialAndExited": True,
        "bothVisualExecutionsInternallyHostSerialized": True,
        "boundedIndependentVisualConfirmation": True, "originalCaptures": 49,
        "eachReviewerDistinctPngs": 26, "byteAliasCaptures": 23,
        "sourceImageDimensions": [1080, 2400],
        "modelVisibleDimensionsQualification": "Actual per-payload dimensions/hashes in receipts; automatic tool resize preserved, not silently equated with source bytes.",
        "transportDisposition": "docs/n1-reviews/batch-080-visual-transport-disposition.json",
        "actionableRemainingFindings": 0, "consequentialUnresolvedScopedTeachingFindings": 0,
        "runtimeEditsMade": False, "runtimeBytesUnchanged": True, "runtimePayloadHashesVerified": count,
        "manifestSha256": sha(R / "manifest.json"), "contentVersion": manifest["contentVersion"],
        "freshAndroidOrNativeRun": False, "inherited540HostCases": 4, "inherited543NativeCases": 2,
        "freshContentValidationErrors": 0, "manifestRegeneratedAndUnchanged": True,
        "pythonSuiteAndAndroid": "Not rerun for this evidence-only checkpoint; inherited fresh540 host/native543 receipts remain qualified. Combined-main publication acceptance remains a later mandatory gate.",
        "runtimePublished": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": "b120125ae5cdbfe9f3bcb1b0a7ae8a61e422ec8d",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "artifacts": [{"path": str(p.relative_to(R)), "bytes": p.stat().st_size, "sha256": sha(p)}
                      for p in files if p.is_file()],
        "limits": reconciliation["limits"],
        "diagnostics": [
            "Entire request parsed before cp1252 display failure; UTF8 bounded displays recovered without permission denial.",
            "A broad durable control listing exceeded tool output size; narrowed to named workspace recipes. Optional historical session-state helpers not accessed.",
            "Initial helper's raw-byte-equality assertion rejected a successful auto-resized PNG. Successful tool/model/process/image evidence retained; qualified full-frame transport recovery resumed without rereading. Original-source hashes and all linguistic/publication gates unchanged.",
            "First record attempt stopped on a missing local N constant after updating only batch source state; fixed the helper, reran source/runtime/receipt assertions and regenerated consistent final evidence. No runtime changes or permission denial.",
        ],
    }
    save(S / "execution-544.json", evidence)
    print("Visual reconciliation/evidence recorded; runtime hashes unchanged:", count)


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", HEAD, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    before = load(LOG / "progress-before-544.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 543
    evidence = load(S / "execution-544.json")
    summary = {
        "schemaVersion": 1, "execution": 544, "checkpoint": 544, "batch": "080",
        "status": "continue", "stage": "visual-confirmed-awaiting-combined-main-acceptance",
        "savedCommit": head, "signature": "G", "evidence": "docs\\n1-sources\\execution-544.json",
        "evidenceSha256": sha(S / "execution-544.json"),
        "independentVisualAcceptance": True, "originalFamilies": ["claude-opus-5.5", "gpt-6.1-sol"],
        "eachReviewerDistinctPngs": 26, "originalCaptures": 49, "eachReviewerSerialChildren": 28,
        "actionableRemainingFindings": 0, "consequentialUnresolvedScopedTeachingFindings": 0,
        "runtimeBytesUnchanged": True, "runtimePayloadHashesVerified": 8366,
        "runtimePublished": False, "dedicatedWorktreesClean": True,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": evidence["lastPublishedCommit"], "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
    }
    progress.update(checkpoint=544, status="continue", stage=summary["stage"], nextAction=NEXT, blocker=None)
    progress["execution544CoordinatorCheckpoint"] = summary
    progress["batch080VisualCheckpoint"] = dict(summary)
    progress["execution544StartingState"]["status"] = "signed-local-visual-confirmation-checkpoint-complete"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert progress[key] == value, f"Historical root changed: {key}"
    progress["execution544HistoryVerification"] = {
        "originalRootKeyCountCompared": len(before), "allOriginalHistoricalRootKeysPreservedExactly": True,
        "changedRootFields": sorted(k for k in allowed if before.get(k) != progress.get(k)),
        "runtimeBytesUnchanged": True, "ownerIssueAuthorAndBodyVerified": False,
    }
    save(C / "progress.json", progress)
    save(LOG / "coordinator-checkpoint-544.json", summary)
    body = (
        f"Batch080 independent visual checkpoint saved locally at normally signed `{head}` "
        f"(teaching `{TEACHING}`, native evidence `{HEAD}`).\n\n"
        "Both original reviewers, Claude Opus5.5 and GPT6.1Sol, completed serial dependent visual "
        "confirmations: each complete source packet plus26 distinct original PNG groups covering49 "
        "captures, one host-dispatched resource per child followed by a zero-tool report. "
        "Both new articles 冴/冴える are bounded correctness/coverage/visual CLEAN; no actionable finding. "
        "Complete reports, per-turn observations, actual models/processes, original and model-visible "
        "image hashes/dimensions, and reconciliation are preserved in docs/n1-reviews. "
        "Automatic tool resizing and an initial overstrict coordinator byte-equality assertion are "
        "explicitly preserved; no permission denial or source substitution. Claude final synthesis "
        "uses its own compressed summary for resources1–12; this is not a full-resolution/fresh lexical claim.\n\n"
        "Native543 two terminal-success cases and host540 four non-skipped cases are inherited, not rerun. "
        "All30 scoped Han render across four production families, including 冫/冱/氵; fallback face "
        "not identified. Complementary horizontal table states are not a single-frame/all-device claim. "
        "Exact full archive production import once, curated soleさえる/Done1of1, reciprocal pair, "
        "SystemBack/offline and seven injected reference strokes remain supplied execution evidence. "
        "No human handwriting/MLKit recognition/physical-phone acceptance is claimed.\n\n"
        "**Not published:**106/1228 additions delivered,1122 remain; this107th addition is still local. "
        "Next checkpoint is SAME080 combined-current-main integration/revalidation and authorized "
        "publication only after normal signing, public SHA, terminal green CI and every immutable-ZIP "
        "runtime hash/original budget gate. No081 started. Android f9b59a2+ required; phone, general-release "
        "and whole-set acceptance remain outstanding. No second runner or actual new permission denial. "
        "Full live checkpoint history is preserved."
    )
    (LOG / "issue-body-544.txt").write_text(body, encoding="utf-8")
    print("Checkpoint544 continue persisted; original root values preserved:", len(before))


def verify():
    progress = load(C / "progress.json")
    before = load(LOG / "progress-before-544.json")
    receipt = load(LOG / "issue-response-544.json")
    body = (LOG / "issue-body-544.txt").read_text(encoding="utf-8")
    normalize = lambda s: s.replace("\r\n", "\n").strip()
    assert receipt["user"]["login"] == "stop-cran" and normalize(receipt["body"]) == normalize(body)
    assert progress["checkpoint"] == 544 and progress["status"] == "continue" and progress["batch"] == "080"
    assert git("rev-parse", "HEAD") == progress["execution544CoordinatorCheckpoint"]["savedCommit"]
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert not git("status", "--porcelain", root=R.parent / "kanji-cards-android")
    for row in load(S / "execution-544.json")["artifacts"]:
        path = R / row["path"]
        assert sha(path) == row["sha256"] and path.stat().st_size == row["bytes"], row["path"]
    hashes()
    for key in ["execution544CoordinatorCheckpoint", "batch080VisualCheckpoint"]:
        progress[key].update(
            issueUpdate=receipt["html_url"], ownerAuthorAndBodyVerified=True,
            ownerReceiptPath=str(LOG / "issue-response-544.json"), ownerReceiptSha256=sha(LOG / "issue-response-544.json"),
        )
    progress["execution544HistoryVerification"]["ownerIssueAuthorAndBodyVerified"] = True
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", progress)
    assert load(C / "progress.json") == progress
    save(LOG / "final-verification-544.json", {
        "checkpoint": 544, "savedCommit": git("rev-parse", "HEAD"), "signature": "G",
        "runtimeHashesVerified": 8366, "allOriginalHistoricalRootKeysPreserved": True,
        "ownerIssueAuthorAndBodyVerified": True, "dedicatedWorktreesClean": True,
        "issueUpdate": receipt["html_url"], "runtimePublished": False, "wholeProjectComplete": False,
    })
    print("Signed local checkpoint, artifact hashes, full history and owner issue receipt verified.")
    print(receipt["html_url"])


if __name__ == "__main__":
    {"record": record, "checkpoint": checkpoint, "verify": verify}[sys.argv[1]]()
