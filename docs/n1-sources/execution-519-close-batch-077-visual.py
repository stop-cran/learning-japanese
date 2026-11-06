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
HEAD = "45191e3dcdee657fd872a8c416227480b95cbc3e"
TEACHING = "02877a257d6b265625e637e6a304fc8440ddd337"
NEXT = (
    "SAME077 combined-current-main acceptance/publication checkpoint next. Read docs\\n1-sources\\execution-519.json "
    "and docs\\n1-reviews\\batch-077-visual-reconciliation.json. Two original-session different-family visual confirmations "
    "completed serially, internally serial, actual Claude claude-opus-5.5 and GPT gpt-6.1-sol; both exit0, "
    "each complete common sourcepacket plus33uniquePNGgroups covering54originals through21exact-bytealiases. "
    "Both actual model-visible imagepayloads900x2000, NOT original1080x2400; returnedbytes preserved. "
    "All39scopedHan/fourproductionfamilies/focused冒日目官冂阜阝険犯侵/冒険冒す legible in bounded captures; "
    "fallbackface/physicalphone unknown. No actionable teaching/rendering defect established. Original攻める safeguard disagreement, "
    "optionalおかlure hypothesis, alias/lastloadingtree limitations preserved. No new algorithm or teachingchange. "
    "Fresh516HOST3+1 and518native2terminal0/zeroskips retained without rerun; full46dff146nativeGitarchive "
    "productionContentSyncONCE1089kanji5046words109N1/version2944928c13e2165a/problems0/epoch1; "
    "Full/Liteボウおか.す; actualぼうおかすGood/Done2correct; all3mappedpairs6directions/SystemBack/offline. "
    "Nine reference-touchstrokes/ungradedtrace/recallAgain NOT humanhandwriting/successfulrecall/MLKit. "
    "Meaning actual stackmatechoices NOT newlyexercised authored日目官; textualchoicesaudit retained. "
    "Fetch latestoriginmain, merge normally only if needed; revalidate actualcombinedtree with required Python suite, "
    "vocabulary/manifest/budget/baseline/link/membership audits and applicable Android checks. "
    "Independently review changed substantive teaching if integration changes it. Then normalsigning/ownerfastforward/"
    "verifiedremoteSHA/greenCI/EVERYimmutableZIPruntimeentryhash/original18000entry42compressed80inflated56retainedMiBbudgets/"
    "ownerissue60receipt before marking published. No078 until publiclyverified. No signingretry/permissionworkaround/"
    "heaporguardchange/authoragents/secondrunner. Preserve FULLlivehistory, all originalsource/review/process/denial/OOM/"
    "failedlookup/readdepthlimitations and reviewedbaseline虎猿丘山exceptions. Published103/1228,remaining1125; "
    "necessarysupportsNOTN1vocabulary. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
    "Overall project incomplete."
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


def prepare_record():
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    reconciliation = load(V / "batch-077-visual-reconciliation.json")
    freeze = load(V / "batch-077-visual-freeze.json")
    previous_end = None
    for family in ["claude", "gpt"]:
        record = load(V / f"batch-077-visual-{family}-execution.json")
        assert record["processAndCoverageAccepted"] and record["exitCode"] == 0
        assert sha(V / f"batch-077-visual-{family}.md") == record["reportSha256"]
        assert sha(Path(record["rawExecutionLocation"])) == record["rawExecutionSha256"]
        if previous_end:
            assert datetime.fromisoformat(previous_end) < datetime.fromisoformat(record["startedAt"])
        previous_end = record["completedAt"]
        images = [x for x in record["toolCalls"] if "imagePayload" in x]
        assert [Path(x["arguments"]["path"]).name for x in images] == [names[0] for names in freeze["imageAliasGroups"].values()]
        for row in images:
            image = row["imagePayload"]
            assert sha(Path(row["arguments"]["path"])) == image["sourceSha256"]
            assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
    for digest, names in freeze["imageAliasGroups"].items():
        assert all(sha(V / "batch-077-native" / "attempt-1" / name) == digest for name in names)
    for name in ["review-batch-077-visual.py", "close-batch-077-visual.py"]:
        target = S / ("execution-519-" + name)
        shutil.copyfile(C / name, target)
    manifest = load(R / "manifest.json")
    record = {
        "schemaVersion": 1, "execution": 519, "checkpoint": 519, "batch": "077",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "startingHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "nativeEnvelopeSnapshot": freeze["nativeEnvelopeSnapshot"], "recordedAt": now(),
        "authorization": load(C / "progress.json")["execution519StartingState"]["authorization"],
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": reconciliation["scope"],
        "models": reconciliation["models"],
        "bothOriginalSessionProcessesSerialAndExited": True,
        "bothVisualExecutionsInternallySerial": True,
        "eachReviewerCompleteSourcePackets": 1, "eachReviewerUniqueImages": 33,
        "sourceCaptures": 54, "hashMappedDuplicateCaptures": 21,
        "sourceImageDimensions": [1080, 2400], "modelVisibleImageDimensions": [900, 2000],
        "boundedIndependentVisualConfirmation": True,
        "actionableRemainingFindings": 0, "consequentialUnresolvedScopedTeachingFindings": 0,
        "reconciliation": "docs\\n1-reviews\\batch-077-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-077-visual-reconciliation.json"),
        "runtimeEditsMade": False, "runtimeBytesUnchanged": True,
        "manifestSha256": sha(R / "manifest.json"), "contentVersion": manifest["contentVersion"],
        "freshAndroidOrNativeRun": False, "retained516HostCases": 4, "retained518NativeCases": 2,
        "runtimePublished": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 103, "remainingAdditions": 1125,
        "lastPublishedCommit": "da5364e9cc72885b8fe08a4bf187e79721f595df",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "diagnostics": [
            "First request metadata display hit Windows cp1252 UnicodeEncodeError after the complete file was loaded/parsed; reran display with UTF-8. No authorization/source bytes missing.",
            "Optional workspace archive-visual-436.py was absent; used existing workspace archive-visual-420.py only as implementation prior art and created reusable077helpers in control. No historical session-state helper accessed.",
            "copilot --model help without prompt reports no prompt; actual supported catalog obtained with copilot help config before review launch.",
        ],
        "limits": "Dependent bounded visual acceptance, not independent upstream retrieval or phone/native-speaker/general-release acceptance. All prior source/review/process/permission/OOM/lookup limits remain. No publication or new native run.",
    }
    files = sorted(V.glob("batch-077-visual-*"))
    files += sorted((V / "batch-077-native" / "visual-claude-returned").glob("*.png"))
    files += sorted((V / "batch-077-native" / "visual-gpt-returned").glob("*.png"))
    files += [S / "batch-077-progress.json", *sorted(S.glob("execution-519-*.py"))]
    record["artifacts"] = [{"path": str(p.relative_to(R)), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files]
    save(S / "execution-519.json", record)
    print("Record/evidence hashes verified; normal signed local evidence commit is next.", flush=True)


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = subprocess.check_output(["git", "-C", str(R), "diff", "--name-only", "-z", HEAD, head]).decode("utf-8").split("\0")
    assert all(not path or path.startswith("docs/") for path in changed)
    before = load(C / "execution-519-progress-before.json")
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 518
    record_path = S / "execution-519.json"
    entry = {
        "execution": 519, "checkpoint": 519, "batch": "077", "savedCommit": head, "signature": "G",
        "record": "docs\\n1-sources\\execution-519.json", "recordSha256": sha(record_path),
        "status": "continue", "stage": "batch-077-visual-confirmation-closed-awaiting-integration",
        "runtimePublished": False, "boundedIndependentVisualConfirmation": True,
        "bothOriginalSessionProcessesSerialAndExited": True, "bothVisualExecutionsInternallySerial": True,
        "eachReviewerUniqueImages": 33, "sourceCaptures": 54,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "publishedAdditions": 103, "remainingAdditions": 1125,
        "nextAction": NEXT, "recordedAt": now(),
    }
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    progress.update(checkpoint=519, status="continue", stage=entry["stage"], nextAction=NEXT, blocker=None)
    progress["execution519StartingState"]["status"] = "signed-dependent-visual-checkpoint-complete"
    progress["batch077VisualCheckpoint"] = entry
    progress["execution519CoordinatorCheckpoint"] = dict(entry)
    for key, value in before.items():
        if key not in allowed:
            assert progress[key] == value, f"Historical value changed: {key}"
    progress["execution519HistoryVerification"] = {
        "originalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "changedRootFields": sorted(allowed), "dedicatedWorktreesClean": True,
        "runtimeBytesUnchanged": True, "ownerIssueAuthorAndBodyVerified": False,
    }
    save(C / "progress.json", progress)
    assert load(C / "progress.json") == progress
    issue = (
        f"Batch **077 (冒)** — bounded independent visual confirmation complete; **not published**.\n\n"
        f"Normally signed local evidence `{head}` (`G`); teaching unchanged at `{TEACHING}`. "
        "Original Claude Opus 5.5 (`claude-opus-5.5`) and GPT-6.1 Sol (`gpt-6.1-sol`) sessions ran serially and exited 0. "
        "Each used 34 strictly serial read-only calls: one complete source packet plus all 33 unique PNG groups covering 54 originals "
        "(21 exact-byte aliases). Actual tool-returned 900×2000 payloads are preserved separately from 1080×2400 originals. "
        "Both give CLEAN correctness/scoped coverage/bounded visual comprehensibility for new 冒/冒す and the two changed reused paragraphs; "
        "no actionable scoped defect remains. Original optional observations, disagreement and limitations remain in complete reports/reconciliation.\n\n"
        "All 39 scoped Han/four production font families and focused 冂/阝/look-alikes are legible in these captures; "
        "no fallback-face or physical-phone claim. Existing four non-skipped host cases and two terminal-0 native cases are retained, not rerun. "
        "Actual reading Good/Done 2/2, mapped links/System Back/offline and nine reference-injected drawing strokes are bounded fixture evidence, "
        "not human handwriting, successful recall or MLKit. Runtime/manifest bytes unchanged; version `2944928c13e2165a`.\n\n"
        "Next checkpoint: same077 current-main integration/revalidation, normal signing and authorized publication only after remote/CI/"
        "every immutable-ZIP runtime hash/original budget acceptance. No078 started. **103/1,228 additions published; 1,125 remaining.** "
        "Compatible Android `f9b59a2+` required; physical-phone/general-release/whole-set acceptance remains outstanding. "
        "Durable source: `docs/n1-sources/execution-519.json`; reconciliation: `docs/n1-reviews/batch-077-visual-reconciliation.json`. "
        "No optional historical session-state helpers, new denial, app/heap/guard change or second runner."
    )
    (C / "batch-077-visual-checkpoint-issue.txt").write_text(issue + "\n", encoding="utf-8")
    print("Checkpoint519 saved; preserved all", len(before), "original root keys; signed", head, flush=True)


if __name__ == "__main__":
    {"record": prepare_record, "checkpoint": checkpoint}[sys.argv[1]]()
