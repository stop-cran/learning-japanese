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
HEAD = "9ed58b037d40d7506ec9dc14ea4ee2ecb7f110f3"
TEACHING = "02b9634acda285bd60d00884479dee2a29ccb6e2"
NEXT = (
    "SAME078 combined-current-main acceptance/publication checkpoint next, then persist/yield; no079 or second runner. "
    "Read docs\\n1-sources\\execution-527.json and docs\\n1-reviews\\batch-078-visual-reconciliation.json. "
    "Two original-session different-family visual confirmations completed serially, internally serial, actual "
    "claude-opus-5.5 and gpt-6.1-sol; both exit0. Each complete common sourcepacket plus24uniquePNGgroups covering43originals "
    "through19exactbytealiases; actual modelvisible900x2000 payloads preserved separately from1080x2400 originals. "
    "New冗/complete reused冗談/changed談37 all three facets CLEAN, no actionable defect established; zero new word article. "
    "All27Han/fourproductionfamilies/focused冖几冗元兄見口目 and wholeword冗談 readable in bounded captures. "
    "Corrected literalnegative/conversational rejection visible;078-C1resolved, unsupported polite-remedy extension withdrawn. "
    "Optional glossary/citation/stroke-label observations and loadingtree limitations retained. Actual meaning choices were "
    "stackmates NOT authored元兄見; no newlypersisted meaninggrade claimed. Fresh524HOST3+1zeroskips and526native2terminal0 "
    "retained without rerun. Whole signed7fb6c463archive productionContentSyncONCE1090kanji5046words110N1/"
    "version8e06edf2b0857b26/problems0/epoch1. Full+Liteジョウ,emptykun,soleじょうGood/Done1of1; "
    "all2mappedpairs4directions/SystemBack/offline. Four reference-touchstrokes/ungradedtrace/giveuprecallAgain NOT "
    "humanhandwriting/successfulrecall/MLKit/modeldownload. Phone/fallbackface unknown. "
    "Fetch latestoriginmain, merge nonrewriting only if needed; revalidate actualcombinedtree with required Python suite, "
    "vocabulary/manifest/budget/baseline/link/membership audits and applicable Android checks. Independently review any "
    "substantive teaching changed by integration. Then normalsigning/ownerfastforward/verifiedremoteSHA/greenCI/"
    "EVERYimmutableZIPruntimeentryhash/original18000entry42compressed80inflated56retainedMiBbudgets/"
    "verifiedownerissue60receipt before markingpublished. No unreviewedpush, signingretry, permissionworkaround, "
    "guest/appheap/archiveguardchange, authoragents or secondrunner. HOST-only2GiBinit NEVER enters native builds. "
    "Use committed source packets/approvedcontrolinputs/durablecontrolhelpers, not optional historical session-state recipes. "
    "Preserve FULLlivehistory, all originalsource/review/process/denial/OOM/lookup/readdepthlimitations and reviewedbaseline "
    "exceptions. Preserve/report/yield on actualnewdenials. Published104/1228,remaining1124; local105th addition notpublished. "
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


def record():
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    freeze = load(V / "batch-078-visual-freeze.json")
    assert sha(Path(freeze["packet"])) == freeze["packetSha256"]
    for source in freeze["sources"]:
        assert sha(Path(source["path"])) == source["sha256"]
    previous_end = None
    reviews = {}
    for family in ["claude", "gpt"]:
        review = load(V / f"batch-078-visual-{family}-execution.json")
        assert review["processAndCoverageAccepted"] and review["exitCode"] == 0
        assert sha(V / f"batch-078-visual-{family}.md") == review["reportSha256"]
        assert sha(Path(review["rawExecutionLocation"])) == review["rawExecutionSha256"]
        if previous_end:
            assert datetime.fromisoformat(previous_end) < datetime.fromisoformat(review["startedAt"])
        previous_end = review["completedAt"]
        images = [x for x in review["toolCalls"] if "imagePayload" in x]
        assert len(images) == 24
        assert [Path(x["arguments"]["path"]).name for x in images] == [names[0] for names in freeze["imageAliasGroups"].values()]
        for row in images:
            payload = row["imagePayload"]
            assert sha(Path(row["arguments"]["path"])) == payload["sourceSha256"]
            assert sha(R / payload["returnedPayloadCopy"]) == payload["sha256"]
            assert payload["sourceDimensions"] == [1080, 2400]
            assert payload["returnedDimensions"] == [900, 2000]
        reviews[family] = {
            "sessionId": review["sessionId"], "actualModels": review["actualModels"],
            "startedAt": review["startedAt"], "completedAt": review["completedAt"],
            "exitCode": review["exitCode"], "imagePayloadsVerified": len(images),
            "completeSourcePacketReturned": review["completeSourcePacketReturned"],
            "observedToolOverlaps": len(review["observedToolOverlaps"]),
            "multiToolResponses": len(review["multiToolResponses"]),
        }
    for digest, names in freeze["imageAliasGroups"].items():
        assert all(sha(V / "batch-078-native" / "attempt-1" / name) == digest for name in names)
    for name in ["review-batch-078-visual.py", "close-batch-078-visual.py"]:
        shutil.copyfile(C / name, S / ("execution-527-" + name))
    manifest = load(R / "manifest.json")
    entries = {}
    for section, mapping in manifest.items():
        if isinstance(mapping, dict):
            for name, digest in mapping.items():
                assert name not in entries
                entries[name] = (section, digest)
    assert len(entries) == 8360
    for name, (section, digest) in entries.items():
        data = R.joinpath(*name.split("/")).read_bytes()
        binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        canonical = data if binary else data.replace(b"\r\n", b"\n")
        assert hashlib.sha256(canonical).hexdigest() == digest, name
    progress = load(S / "batch-078-progress.json")
    progress["status"] = "bounded-native-and-visual-closed-awaiting-integration"
    progress["visualReviewCheckpoint"] = {
        "execution": 527, "reviewedTeachingSnapshot": TEACHING,
        "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "reconciliation": "docs/n1-reviews/batch-078-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-078-visual-reconciliation.json"),
        "boundedIndependentVisualConfirmation": True, "runtimePublished": False,
        "actionableRemainingFindings": 0, "sourceCaptures": 43, "eachReviewerDistinctPngs": 24,
    }
    progress["nextGate"] = NEXT
    save(S / "batch-078-progress.json", progress)
    files = sorted(V.glob("batch-078-visual-*"))
    for family in ["claude", "gpt"]:
        files += sorted((V / "batch-078-native" / f"visual-{family}-returned").glob("*.png"))
    files += [S / "batch-078-progress.json", *sorted(S.glob("execution-527-*.py"))]
    save(S / "execution-527.json", {
        "schemaVersion": 1, "execution": 527, "checkpoint": 527, "batch": "078",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "nativeEnvelopeSnapshot": freeze["nativeEnvelopeSnapshot"], "recordedAt": now(),
        "authorization": load(C / "progress.json")["execution527StartingState"]["authorization"],
        "freshOriginMain": git("rev-parse", "origin/main"), "reviews": reviews,
        "reconciliation": "docs\\n1-reviews\\batch-078-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-078-visual-reconciliation.json"),
        "bothOriginalSessionProcessesSerialAndExited": True, "bothVisualExecutionsInternallySerial": True,
        "boundedIndependentVisualConfirmation": True,
        "eachReviewerCompleteSourcePackets": 1, "eachReviewerUniqueImages": 24,
        "sourceCaptures": 43, "hashMappedDuplicateCaptures": 19,
        "sourceImageDimensions": [1080, 2400], "modelVisibleImageDimensions": [900, 2000],
        "actionableRemainingFindings": 0, "consequentialUnresolvedScopedTeachingFindings": 0,
        "runtimeEditsMade": False, "runtimeBytesUnchanged": True, "runtimePayloadHashesVerified": len(entries),
        "manifestSha256": sha(R / "manifest.json"), "contentVersion": manifest["contentVersion"],
        "freshAndroidOrNativeRun": False, "retained524HostCases": 4, "retained526NativeCases": 2,
        "runtimePublished": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 104, "remainingAdditions": 1124,
        "lastPublishedCommit": "d7170f11e271a8de47bd2fd152e7196b96bff189",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "diagnostics": [
            "First request metadata display encountered cp1252 UnicodeEncodeError only after complete request load and checkpoint parse. UTF8 subsequent bounded displays succeeded; no authorization bytes missing.",
            "Broad durable-helper inventory display was oversized; narrowed to named workspace recipes. No optional historical session-state helper accessed.",
            "First closure helper stopped before record/ledger writes because it counted only manifest.files instead of all dictionary-valued sections. Corrected to existing section-specific manifest hashing, including CRLF normalization for text and raw binary bytes. No runtime/evidence source changed.",
            "Full staged diff whitespace check reports only preserved raw GPT Markdown hard breaks, verbatim model-catalog blank EOF, and numbered sourcepacket empty-line prefixes. Those three frozen artifacts are deliberately not reformatted. Other authored evidence passes the targeted whitespace check. No signing command ran in that first check."
        ],
        "artifacts": [{"path": str(p.relative_to(R)), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files],
        "limits": "Dependent bounded visual acceptance, not independent upstream retrieval or phone/native-speaker/general-release acceptance. All prior source/review/process/permission/OOM/lookup limits remain. No publication or new native run. Original publishing budgets unchanged.",
    })
    print("Both complete original reports, serial process/coverage/image receipts and8360runtimehashes verified.", flush=True)


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = subprocess.check_output(["git", "-C", str(R), "diff", "--name-only", "-z", HEAD, head]).decode("utf-8").split("\0")
    assert all(not path or path.startswith("docs/") for path in changed)
    android = R.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "-C", str(android), "status", "--porcelain"])
    before = load(C / "execution-527-progress-before.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 526
    entry = {
        "schemaVersion": 1, "execution": 527, "checkpoint": 527, "batch": "078",
        "savedCommit": head, "signature": "G", "record": "docs\\n1-sources\\execution-527.json",
        "recordSha256": sha(S / "execution-527.json"),
        "status": "continue", "stage": "batch-078-visual-confirmation-closed-awaiting-integration",
        "runtimePublished": False, "boundedIndependentVisualConfirmation": True,
        "bothOriginalSessionProcessesSerialAndExited": True, "bothVisualExecutionsInternallySerial": True,
        "eachReviewerUniqueImages": 24, "sourceCaptures": 43,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "contentVersion": "8e06edf2b0857b26", "publishedAdditions": 104, "remainingAdditions": 1124,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "recordedAt": now(),
    }
    progress.update(checkpoint=527, status="continue", stage=entry["stage"], nextAction=NEXT, blocker=None)
    progress["execution527StartingState"]["status"] = "signed-dependent-visual-checkpoint-complete"
    progress["batch078VisualCheckpoint"] = entry
    progress["execution527CoordinatorCheckpoint"] = dict(entry)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert progress[key] == value, f"Historical value changed: {key}"
    progress["execution527HistoryVerification"] = {
        "originalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "changedRootFields": sorted(k for k in allowed if before.get(k) != progress.get(k)),
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True, "ownerIssueAuthorAndBodyVerified": False,
    }
    save(C / "progress.json", progress)
    assert load(C / "progress.json") == progress
    issue = (
        f"Batch **078 (冗)** — bounded independent visual confirmation complete; **not published**.\n\n"
        f"Normally signed local evidence `{head}` (`G`); teaching unchanged at `{TEACHING}`. "
        "Original Claude Opus 5.5 (`claude-opus-5.5`) and GPT-6.1 Sol (`gpt-6.1-sol`) sessions ran serially and exited 0. "
        "Each made 25 strictly serial read-only calls: one complete common source packet plus all 24 unique PNG groups covering "
        "43 originals (19 exact-byte aliases). Actual tool-returned 900×2000 payloads are preserved separately from 1080×2400 originals. "
        "Both give CLEAN correctness/scoped coverage/bounded visual comprehensibility for new 冗, complete reused 冗談 and changed 談:37. "
        "No actionable scoped defect remains; original reports, optional observations and limitations are preserved.\n\n"
        "All 27 scoped Han/four production font families, exact 冖/几 and focused look-alikes are legible in these captures. "
        "The corrected literal-negative/conversational-rejection distinction is visible. No fallback-face or physical-phone claim. "
        "Existing four non-skipped host cases and two terminal-0 native cases are retained, not rerun. "
        "Actual sole reading Good/Done 1/1, mapped links/System Back/offline and four reference-injected drawing strokes are bounded "
        "fixture evidence, not human handwriting, successful recall, MLKit or newly persisted meaning-grade evidence. "
        "Runtime/manifest unchanged; all 8,360 payload hashes verified; version `8e06edf2b0857b26`. Zero new word articles.\n\n"
        "Next checkpoint: same078 current-main integration/revalidation, normal signing and authorized publication only after "
        "remote/CI/every immutable-ZIP runtime hash/original budget acceptance. No079 started. "
        "**104/1,228 additions published; 1,124 remaining.** Compatible Android `f9b59a2+` required; "
        "physical-phone/general-release/whole-set acceptance remains outstanding. "
        "Evidence: `docs/n1-sources/execution-527.json` and `docs/n1-reviews/batch-078-visual-reconciliation.json`. "
        "No optional historical session-state helpers, new denial, app/heap/guard change or second runner."
    )
    (C / "batch-078-visual-checkpoint-issue.txt").write_text(issue + "\n", encoding="utf-8")
    print("Checkpoint527 saved; all", len(before), "original root keys preserved; signed", head, flush=True)


if __name__ == "__main__":
    {"record": record, "checkpoint": checkpoint}[sys.argv[1]]()
