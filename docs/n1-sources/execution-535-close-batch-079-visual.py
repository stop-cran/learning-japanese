import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
HEAD = "dcfcbb43b30b63beef3f689d3ebae4e412c9120c"
TEACHING = "0f7f20e93b1e20cbc9943011e9ac69b20f75086e"
NEXT = (
    "SAME079 combined-current-main acceptance/publication checkpoint ONLY next, then persist/yield; no080 or second runner. "
    "Read docs\\n1-sources\\execution-535.json and docs\\n1-reviews\\batch-079-visual-reconciliation.json. "
    "Two original-session different-family dependent visual confirmations accepted: ClaudeOpus5.5 and GPT6.1Sol. "
    "Preserve original rejected Claude visual run: exit0 but25tooloverlaps/twomultitoolresponses. "
    "One finite host-dispatched Claude replay31serialCLIturns: completepacket+29images, one resource per child then zero-tool "
    "finalreport; allchildrenexitbeforeNext. Claude final synthesis explicitly uses ownsummary forresources1-17 andlive18-30. "
    "GPT subsequently completes samepacket+29images strictlyserial inoneprocess. Both accepted receipts exit0/zerooverlaps/nomultitool; "
    "each29distinctPNGgroups covers57originals/28bytealiases; original1080x2400 andmodelvisible900x2000payloads separatelyretained. "
    "Allfourassignments new冠/new王冠/complete reused冠/changed王39 correctness/scopedcoverage/boundedvisualCLEAN, noactionabledefect. "
    "All35Han/fourproductionfamilies andexact冖宀/lookalikes readable. Complementaryhorizontalreadingtable states, NOTallcolumnsoneframe. "
    "Prior531textual/all177families/fiverawrecords/N2source/namingclosure andfresh532HOST3+1zeroskips/fresh534native2terminal0 "
    "inherited honestly, not rerun. Signed3fdc0bf9fullarchive productionContentSyncONCE1091kanji5047words111N1/"
    "versiona01eb85b17601ac0/problems0/epoch1. Full+Liteカンかんむり/offeredかんかんむり, twonewgrade3readinglogs/Done2of2; "
    "all3pairs6directions/SystemBack/offline. Actualmeaningchoices were exempt/superfluous/frugal NOT authoredfull冗完守trio; "
    "nonewmeaninggradeclaim. Nineinjectedreferencepaths/ungradedtrace/shape-onlycomparison/giveuprecallgrade1 NOT "
    "humanhandwriting/successfulrecall/MLKit/modeldownload. Finaltree transientloading NOT loadedpersistenceproof. "
    "140individual+8wordnativePaint assertion/hashrecords NOT148PNGreads. Fallbackface/phone unknown. "
    "Fetch latestoriginmain, merge nonrewriting onlyifneeded; revalidate actualcombinedtree with required Python suite, "
    "vocabulary/manifest/budget/baseline/link/membership audits and applicable Androidchecks. Re-review substantiveteaching "
    "changed by integration. Normal signing, authorized ownerfastforward, verifiedremoteSHA/greenCI/EVERYimmutableZIPentryhash/"
    "original18000entry42compressed80inflated56retainedMiBguards andverifiedownerissue60receipt before markingpublished. "
    "Nounreviewedpush/signingretry/permissionworkaround/authoragents/concurrentheavywork/secondrunner; "
    "HOST-only2GiBinit NEVER native, noapp/guestheap/guardchange. Durablecontrolhelpers/committedpackets/approvedinputsONLY, "
    "NOT optional historicalsession-state recipes. PreserveFULLlivehistory/all originalsource/review/process/denial/OOM/"
    "readdepth/phone limitations/baselineexceptions; preserve/report/yieldactualnewdenials. "
    "Published105/1228,remaining1123; local106thaddition textually/native/visualclosedNOTpublished. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), *args], encoding="utf-8").strip()


def now():
    return datetime.now().astimezone().isoformat()


def runtime_hashes():
    manifest = load(R / "manifest.json")
    entries = {}
    for section, mapping in manifest.items():
        if isinstance(mapping, dict):
            for name, digest in mapping.items():
                assert name not in entries
                entries[name] = (section, digest)
    assert len(entries) == 8363
    for name, (section, digest) in entries.items():
        data = R.joinpath(*name.split("/")).read_bytes()
        binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        canonical = data if binary else data.replace(b"\r\n", b"\n")
        assert hashlib.sha256(canonical).hexdigest() == digest, name
    return manifest, len(entries)


def record():
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    freeze = load(V / "batch-079-visual-freeze.json")
    assert sha(Path(freeze["packet"])) == freeze["packetSha256"]
    for source in freeze["sources"]:
        assert sha(Path(source["path"])) == source["sha256"]
    native = load(S / "execution-534.json")
    assert native["nativeExecution"]["terminalSuccessCases"] == 2
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    rejected = load(V / "batch-079-visual-claude-execution.json")
    assert not rejected["processAndCoverageAccepted"] and len(rejected["observedToolOverlaps"]) == 25
    assert len(rejected["multiToolResponses"]) == 2
    reviews = {}
    previous_end = None
    for label in ["claude-serial", "gpt"]:
        path = V / f"batch-079-visual-{label}-execution.json"
        review = load(path)
        assert review["processAndCoverageAccepted"] and review["exitCode"] == 0
        assert sha(V / f"batch-079-visual-{label}.md") == review["reportSha256"]
        assert sha(Path(review["rawExecutionLocation"])) == review["rawExecutionSha256"]
        if previous_end:
            assert datetime.fromisoformat(previous_end) < datetime.fromisoformat(review["startedAt"])
        previous_end = review["completedAt"]
        images = [x for x in review["toolCalls"] if "imagePayload" in x]
        assert len(images) == 29
        assert [Path(x["arguments"]["path"]).name for x in images] == [names[0] for names in freeze["imageAliasGroups"].values()]
        for row in images:
            payload = row["imagePayload"]
            assert sha(Path(row["arguments"]["path"])) == payload["sourceSha256"]
            assert sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
            assert payload["sourceDimensions"] == [1080, 2400]
            assert payload["returnedDimensions"] == [900, 2000]
        if label == "claude-serial":
            children = review["hostDispatchedTurns"]
            assert len(children) == 31
            for i, child in enumerate(children):
                assert child["exitCode"] == 0 and child["singleResourceAccepted"]
                if i:
                    assert datetime.fromisoformat(children[i - 1]["completedAt"]) < datetime.fromisoformat(child["startedAt"])
        reviews[label] = {
            "sessionId": review["sessionId"], "actualModels": review["actualModels"],
            "startedAt": review["startedAt"], "completedAt": review["completedAt"], "exitCode": 0,
            "imagePayloadsVerified": 29, "completeSourcePacketReturned": True,
            "observedToolOverlaps": 0, "multiToolResponses": 0, "receiptSha256": sha(path),
            "reportSha256": review["reportSha256"], "rawExecutionSha256": review["rawExecutionSha256"],
            "readDepthQualification": "Own context summary for resources1-17; live18-30 at final synthesis." if label == "claude-serial" else "Single serial process; exact returned bytes verified, not comprehension certification.",
        }
    for digest, names in freeze["imageAliasGroups"].items():
        assert all(sha(V / "batch-079-native" / "attempt-1" / name) == digest for name in names)
    turn_notes = []
    for raw in sorted((C / "batch-079-visual-claude-serial-turns").glob("turn-*.jsonl")):
        events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        messages = [e["data"] for e in events if e["type"] == "assistant.message"]
        turn_notes.append({
            "raw": str(raw), "rawSha256": sha(raw),
            "finalVisibleReply": [m["content"] for m in messages if m.get("content")][-1],
        })
    save(V / "batch-079-visual-claude-serial-turn-notes.json", {
        "scope": "Original visible per-turn replies, preserved to distinguish firsthand reads from later context-summary synthesis. No provider reasoning or private instructions exported.",
        "turns": turn_notes,
    })
    for name in ["review-batch-079-visual.py", "review-batch-079-visual-serial.py", "close-batch-079-visual.py"]:
        shutil.copyfile(C / name, S / ("execution-535-" + name))
    manifest, count = runtime_hashes()
    progress = load(S / "batch-079-progress.json")
    progress["status"] = "bounded-native-and-visual-closed-awaiting-integration"
    progress["visualReviewCheckpoint"] = {
        "execution": 535, "reviewedTeachingSnapshot": TEACHING,
        "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "reconciliation": "docs/n1-reviews/batch-079-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-079-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "runtimePublished": False,
        "actionableRemainingFindings": 0, "sourceCaptures": 57, "eachReviewerDistinctPngs": 29,
        "rejectedClaudeProcessRetained": True, "finiteHostDispatchedRecovery": True,
    }
    progress["nextGate"] = NEXT
    save(S / "batch-079-progress.json", progress)
    files = sorted(V.glob("batch-079-visual-*"))
    for label in ["claude", "claude-serial", "gpt"]:
        files += sorted((V / "batch-079-native" / f"visual-{label}-returned").glob("*.png"))
    files += [S / "batch-079-progress.json", *sorted(S.glob("execution-535-*.py"))]
    save(S / "execution-535.json", {
        "schemaVersion": 1, "execution": 535, "checkpoint": 535, "batch": "079",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "nativeEnvelopeSnapshot": freeze["nativeEnvelopeSnapshot"], "recordedAt": now(),
        "authorization": load(C / "progress.json")["execution535StartingState"]["authorization"],
        "freshOriginMain": git("rev-parse", "origin/main"), "reviews": reviews,
        "reconciliation": "docs\\n1-reviews\\batch-079-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-079-visual-reconciliation.json"),
        "bothAcceptedOriginalFamilyExecutionsSerialAndExited": True,
        "bothAcceptedVisualExecutionsInternallySerial": True, "boundedIndependentVisualConfirmation": True,
        "eachReviewerCompleteSourcePackets": 1, "eachReviewerUniqueImages": 29,
        "sourceCaptures": 57, "hashMappedDuplicateCaptures": 28,
        "sourceImageDimensions": [1080, 2400], "modelVisibleImageDimensions": [900, 2000],
        "rejectedClaudeRun": {
            "receipt": "docs/n1-reviews/batch-079-visual-claude-execution.json",
            "receiptSha256": sha(V / "batch-079-visual-claude-execution.json"),
            "exitCode": 0, "accepted": False, "toolOverlaps": 25, "multiToolResponses": 2,
            "originalReportAndReturnedPayloadsPreserved": True,
        },
        "recovery": "One finite original-Claude host-dispatched replay, each single-resource child exits before next. GPT starts only after replay final report and full archive. Original failed report not accepted.",
        "actionableRemainingFindings": 0, "consequentialUnresolvedScopedTeachingFindings": 0,
        "runtimeEditsMade": False, "runtimeBytesUnchanged": True, "runtimePayloadHashesVerified": count,
        "manifestSha256": sha(R / "manifest.json"), "contentVersion": manifest["contentVersion"],
        "freshAndroidOrNativeRun": False, "retained532HostCases": 4, "retained534NativeCases": 2,
        "runtimePublished": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 105, "remainingAdditions": 1123,
        "lastPublishedCommit": "2a6777503de6c23c2ac5582b0265dd68d224f44c",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "diagnostics": [
            "First intake loaded and parsed the entire request before cp1252 UnicodeEncodeError displaying root state. UTF8 bounded displays succeeded. Historical request middle loaded/parsed, not freshly semantically reviewed.",
            "Broad control-helper listing was oversized; narrowed to dedicated named workspace recipes. No optional historical session-state helper accessed.",
            "Current root checkpoint534 is batch079 visual, not historical513 batch077 draft; acted on final checkpoint only.",
            "Final archived primary review recipe includes GPT gating adaptation to accepted Claude replay; not claimed byte-identical to the first rejected launch recipe. Shared frozen task unchanged.",
            "Full staged whitespace check reports only numbered empty sourcepacket lines and the verbatim model catalog's blank EOF. Frozen evidence remains byte-identical; all other staged evidence passes targeted whitespace checking.",
        ],
        "artifacts": [{"path": str(p.relative_to(R)), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files],
        "limits": "Dependent bounded visual acceptance, not fresh lexical/upstream/native/phone review. Claude context-summary read-depth qualification preserved. All prior source/review/process/permission/OOM/phone limits and original publishing budgets retained. No publication, native rerun or next batch.",
    })
    print("Reports, actual serial coverage/payloads and", count, "runtime hashes verified.", flush=True)


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = subprocess.check_output(["git", "-C", str(R), "diff", "--name-only", "-z", HEAD, head]).decode("utf-8").split("\0")
    assert all(not path or path.startswith("docs/") for path in changed)
    android = R.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "-C", str(android), "status", "--porcelain"])
    before = load(C / "execution-535-progress-before.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 534
    entry = {
        "schemaVersion": 1, "execution": 535, "checkpoint": 535, "batch": "079",
        "savedCommit": head, "signature": "G", "record": "docs\\n1-sources\\execution-535.json",
        "recordSha256": sha(S / "execution-535.json"),
        "status": "continue", "stage": "batch-079-visual-confirmation-closed-awaiting-integration",
        "runtimePublished": False, "boundedIndependentVisualConfirmation": True,
        "bothAcceptedOriginalFamilyExecutionsSerialAndExited": True,
        "bothAcceptedVisualExecutionsInternallySerial": True, "rejectedClaudeProcessPreserved": True,
        "eachReviewerUniqueImages": 29, "sourceCaptures": 57,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "contentVersion": "a01eb85b17601ac0", "publishedAdditions": 105, "remainingAdditions": 1123,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "recordedAt": now(),
    }
    progress.update(checkpoint=535, status="continue", stage=entry["stage"], nextAction=NEXT, blocker=None)
    progress["execution535StartingState"]["status"] = "signed-dependent-visual-checkpoint-complete"
    progress["batch079VisualCheckpoint"] = entry
    progress["execution535CoordinatorCheckpoint"] = dict(entry)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert progress[key] == value, f"Historical value changed: {key}"
    progress["execution535HistoryVerification"] = {
        "originalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "changedRootFields": sorted(k for k in allowed if before.get(k) != progress.get(k)),
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "ownerIssueAuthorAndBodyVerified": False,
    }
    save(C / "progress.json", progress)
    assert load(C / "progress.json") == progress
    issue = (
        f"Batch **079 (冠)**: bounded independent visual confirmation complete; **not published**.\n\n"
        f"Normally signed local evidence `{head}` (`G`); teaching remains `{TEACHING}`. "
        "Original Claude Opus 5.5 (`claude-opus-5.5`) and GPT-6.1 Sol (`gpt-6.1-sol`) confirmations completed serially. "
        "The first Claude run exited 0 but violated tool serialization (25 overlaps/two multi-tool responses); "
        "its original report and payloads are preserved and rejected for process compliance. "
        "One finite original-session recovery used 31 host-dispatched CLI turns: one complete packet, 29 one-image turns, "
        "then zero-tool final report, each child exited before the next. GPT subsequently used 30 strictly serial view calls. "
        "Both accepted executions have zero overlaps/multi-tool responses and actual model/exit/read receipts. "
        "Each covered all 29 distinct groups of 57 originals; returned 900×2000 payloads are preserved separately from 1080×2400 captures. "
        "Claude explicitly qualifies its final synthesis as own context-summary for resources 1–17 and live context for 18–30.\n\n"
        "All four assignments (new 冠, new 王冠, complete reused 冠, 王:39) are CLEAN in correctness/scoped coverage/bounded visual comprehension: "
        "no actionable scoped defect established. All 35 Han/four production families and exact 冖/宀 remain readable; "
        "both complete reading examples appear across complementary sideways-scroll states, not all columns in one frame. "
        "Prior four non-skipped host cases and two terminal-0 native cases are retained, not rerun. "
        "Production import once: 1,091 kanji/5,047 words/111 N1, `a01eb85b17601ac0`, zero problems, epoch 1; "
        "two reading Good logs/Done 2/2, all three pairs/six directions, Back/offline asserted. "
        "Nine injected reference strokes/shape-only feedback/give-up recall are not human handwriting, successful recall or MLKit. "
        "Actual meaning choices differ from the full authored trio; no new meaning-grade or final loading-tree persistence claim. "
        "All 8,363 runtime hashes verified; runtime/manifest unchanged.\n\n"
        "Checkpoint 535 next: same079 current-main integration/revalidation and authorized publication only after all "
        "normal signing/owner fast-forward/remote/CI/every immutable-ZIP runtime hash/original-budget gates. No080 started. "
        "**105/1,228 additions published; 1,123 remaining.** Physical-phone/general-release/whole-set acceptance outstanding; "
        "compatible Android `f9b59a2+` required. Evidence: `docs/n1-sources/execution-535.json` and "
        "`docs/n1-reviews/batch-079-visual-reconciliation.json`. Durable workspace helpers only; no new denial, app/heap/guard change or second runner."
    )
    (C / "batch-079-visual-checkpoint-issue.txt").write_text(issue + "\n", encoding="utf-8")
    print("Checkpoint535 saved;", len(before), "historical root values preserved; signed", head, flush=True)


if __name__ == "__main__":
    {"record": record, "checkpoint": checkpoint}[sys.argv[1]]()
