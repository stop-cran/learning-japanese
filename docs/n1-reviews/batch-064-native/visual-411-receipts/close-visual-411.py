import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
P = C / "progress.json"
S = R / "docs" / "n1-sources" / "execution-411.json"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
git = lambda *args, tree=R: subprocess.check_output(
    ["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".411.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


data = load(P)
head = "976b825f0d32d1074c63c6f7b71388daa9da81a9"
assert data["checkpoint"] == 410 and data["batch"] == "064"
if len(sys.argv) > 1:
    assert sys.argv[1] == "finish"
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == head
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert not git("diff", head, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json")
    record = load(S)
    receipt = load(C / "execution-411-issue-receipt.json")
    assert receipt["localCommit"] == saved and receipt["author"] == "stop-cran" and receipt["bodyVerified"]
    checkpoint = {
        "execution": 411, "checkpoint": 411, "batch": "064",
        "status": record["status"], "savedCommit": saved, "signature": "G",
        "record": str(S.relative_to(R)), "recordSha256": sha(S),
        "acceptanceRecord": record["acceptanceRecord"], "nextAction": record["nextAction"],
        "exactOriginalReviewerPathAccessRecovered": True,
        "independentVisualAcceptance": True, "runtimePublished": False,
        "issueUpdate": receipt["url"], "dedicatedContentClean": True,
        "lastPublishedCommit": data["lastPublishedCommit"], "remainingAdditions": data["remainingAdditions"],
        "recordedAt": datetime.now(timezone.utc).isoformat(),
    }
    old = dict(data)
    data.update(checkpoint=411, status="continue",
                stage="batch-064-scoped-access-and-dependent-visual-closed-pending-combined-main-acceptance",
                blocker=None, nextAction=record["nextAction"])
    data["execution411CoordinatorCheckpoint"] = checkpoint
    data["batch064NativeVisualCheckpoint"] = checkpoint.copy()
    data["execution411IssueReceipt"] = receipt
    data["execution411StartingState"] = {**data["execution411StartingState"],
                                        "status": "signed-scoped-path-recovery-and-visual-checkpoint-complete"}
    for key, value in old.items():
        if key not in {"checkpoint", "status", "stage", "blocker", "nextAction", "execution411StartingState"}:
            assert data[key] == value, key
    save(P, data)
    print(f"Checkpoint411 persisted: signed G {saved}; continue SAME064 combined-main acceptance next.")
    sys.exit(0)

assert git("rev-parse", "HEAD") == head and git("log", "-1", "--format=%G?") == "G"
assert not S.exists()
assert not git("diff", "ff6eb7893344b806bf517ebd41bf19089bed5021", "--",
               "kanji", "words", "articles", "strokes", "manifest.json")
app = C.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=app)
freeze = load(C / "batch-064-visual-freeze.json")
for path, expected in (freeze["teachingHashes"] | freeze["originalReportHashes"]).items():
    assert sha(R / path) == expected, path
assert sha(C / "batch-064-visual-task.txt") == freeze["sharedTaskSha256"]
historical = {}
for name in ("batch-064-visual-claude", "batch-064-visual-409-claude", "batch-064-visual-410-claude"):
    audit = load(V / f"{name}-execution.json")
    assert sha(V / f"{name}.md") == audit["reportSha256"]
    assert sha(Path(audit["rawExecutionLocation"])) == audit["rawExecutionSha256"]
    assert not audit["processAndCoverageAccepted"]
    historical[name] = {"reportSha256": sha(V / f"{name}.md"),
                        "executionSha256": sha(V / f"{name}-execution.json"),
                        "rawSha256": audit["rawExecutionSha256"], "strictAcceptance": False}
audits = [load(V / "batch-064-visual-411-claude-execution.json"),
          load(V / "batch-064-visual-411-gpt-execution-verified.json")]
assert [a["actualModels"] for a in audits] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
assert datetime.fromisoformat(audits[0]["completedAt"]) < datetime.fromisoformat(audits[1]["startedAt"])
assert audits[1]["priorExitAndArchiveVerifiedBeforeLaunch"]
for family, audit in zip(("claude", "gpt"), audits):
    assert audit["processAndCoverageAccepted"] and audit["exactFirstSharedTaskReadRecovered"]
    assert audit["exitCode"] == 0 and not audit["failedTools"] and not audit["unfinishedTools"]
    assert not audit["observedToolOverlaps"] and not audit["multiToolResponses"]
    assert sha(V / f"batch-064-visual-411-{family}.md") == audit["reportSha256"]
    assert sha(Path(audit["rawExecutionLocation"])) == audit["rawExecutionSha256"]
    for call in audit["toolCalls"]:
        assert call["name"] == "view" and call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
            assert image["sourceDimensions"] == [1080, 2400] and image["returnedDimensions"] == [900, 2000]
        else:
            assert call["exactRequestedTextContainedInResult"]
assert [len(a["toolCalls"]) for a in audits] == [10, 41]
assert [a["imagePayloadsVerified"] for a in audits] == [6, 28]
native = V / "batch-064-native" / "attempt-1"
prior = load(R / "docs" / "n1-sources" / "execution-407.json")
assert sha(native / "instrumentation.txt") == prior["rawLogSha256"]
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$",
                  (native / "instrumentation.txt").read_text(encoding="utf-8"), re.M) == ["1", "0", "1", "0"]
assert load(native / "n1-064-article-route.json") == prior["actualRouteReceipt"]
manifest = load(R / "manifest.json")
sys.path.insert(0, str(R / "tools"))
from build_manifest import build_manifest

assert build_manifest(R) == manifest
hash_count = sum(len(values) for values in manifest.values() if isinstance(values, dict))
assert hash_count == 8320
receipts = V / "batch-064-native" / "visual-411-receipts"
assert not receipts.exists()
receipts.mkdir()
files = [
    C / "prepare-visual-411.py", C / "run-visual-411.ps1", C / "archive-visual-411.py",
    Path(__file__), C / "batch-064-authorized-scoped-path-recovery.json",
    C / "reviewer-path-access-notes.txt", C / "batch-064-visual-task.txt",
    C / "batch-064-visual-freeze.json",
    C / "inputs" / "copilot-help-411.txt",
    C / "inputs" / "copilot-config-help-411.txt",
    C / "inputs" / "copilot-config-subcommand-help-411.txt",
]
for family in ("claude", "gpt"):
    files += [C / f"batch-064-visual-411-{family}-{suffix}"
              for suffix in ("prompt.txt", "process.json", "usage.json", "stderr.txt")]
artifacts = []
for source in files:
    target = receipts / source.name
    shutil.copyfile(source, target)
    assert sha(source) == sha(target)
    artifacts.append({"path": str(target.relative_to(R)), "sha256": sha(target),
                      "bytes": target.stat().st_size})
next_action = (
    "SAME064 checkpoint411: authorized scoped --add-dir control recovered ORIGINAL Claude and GPT exact "
    "shared-task access; dependent visual closure accepted, not retroactive408/409/410 acceptance. "
    "No further reviewer/Android/native rerun absent new substantive concern. Retain402 textual,404 Android3+1, "
    "406 native terminal2case0 and407 exact cleanup recovery with original source/citation/process/port limits. "
    "Next bounded coordinator: fetch latest origin/main, normal nonrewriting integration if advanced, "
    "all applicable combined-tree Python/vocabulary/membership/baseline/link/manifest/archive budget and "
    "Android checks as required; independently confirm changed substantive teaching only. Normal signed "
    "acceptance/evidence commit, owner-auth normal fastforward HEAD:main, verify public SHA, terminalgreenCI, "
    "every exact immutable public ZIP runtime entry/hash and original budgets, ownerissue60 acceptance receipt "
    "BEFORE counting delivery or065. No force/amend/signing workaround/global credential change. "
    "Published90/1228;1138remaining; lastPublished063d00bf868466437d39b0330a383de8448686b502d; "
    "local91 NOTdelivered. CompatibleAndroidf9b59a2+; physicalphone/generalrelease/whole-set outstanding. "
    "Keep future N1 reviewer scoped-control path preflight, originalcwd/read-only/onecallperresponse/serial "
    "processes, no allpaths/policy/ACL/globalgrant. New actual denial preserve/report/yield. No second runner."
)
acceptance = {
    "schemaVersion": 1, "execution": 411, "batch": "064",
    "status": "dependent-native-visual-accepted-awaiting-combined-main-publication",
    "teachingSnapshot": "ff6eb7893344b806bf517ebd41bf19089bed5021", "evidenceHead": head,
    "reviewerRecords": ["docs\\n1-reviews\\batch-064-visual-411-claude-execution.json",
                        "docs\\n1-reviews\\batch-064-visual-411-gpt-execution-verified.json"],
    "reviewerModels": ["claude-opus-5.5", "gpt-6.1-sol"],
    "dependentOriginalSessionsNotBlindInitials": True,
    "serialExitsAndFirstArchiveBeforeSecondLaunch": True,
    "exactOriginalReviewerPathAccessRecovered": True,
    "scopedGrant": str(C), "policyConfigurationAclChanges": False,
    "claimReconciliation": {
        "408-kun-dash-after-sideways-scroll": {
            "status": "withdrawn",
            "evidence": "Claude411 source lines34-39 and six fresh pixels: sole on row; visible dash belongs to Typical words gloss, not a kun cell. Coordinator inspected returned no-kun PNG and complete source.",
            "learningDefectEstablished": False,
        },
        "408-every-in-scope-paragraph-full-footer-visible": {
            "status": "resolved",
            "disposition": "Narrowed/qualified, not universal pixel certification. Claude411 identifies fresh versus retained and clipped/unseen portions; GPT411 expressly declines every-paragraph/footer claims. Unchanged reused context is not freshly reviewed; source knowledge does not establish unseen pixels.",
            "learningDefectEstablished": False,
        },
        "064-N1": {"status": "resolved", "disposition": "Original402 textual link closure retained; GPT411 observes both comparison links and supplied System Back assertions. No new teaching change."},
    },
    "actionableNewContentFindings": [],
    "optional": "Claude inherited nonblocking expansion/UI suggestions remain optional; no new mandatory scope.",
    "historical408409410Preserved": historical,
    "gptInitialAuditOnlyFalsePreserved": audits[1]["auditCorrection"],
    "nativeAcceptance": "Inherited406 two terminalcase0/407 archival and exact cleanup recovery, not rerun411.",
    "androidAcceptance": "Inherited404 non-skipped RealContentTest3/RareHanTest1, not rerun411.",
    "independentVisualAcceptance": True, "runtimePublished": False,
    "limits": "Two-family dependent bounded visual confirmation, not new blind initial or dictionary/native-speaker certification. Actual returned900x2000 versus source1080x2400 images, clipping/unseen text and actual fallback-face identity remain qualified. Synthetic fixture/injected drawing/meaning Back before Next/paint probe/hostheap/nonemptyport and all original source/citation/process limitations retained. No phone, general-release, whole-set, latest-main,CI or public ZIP acceptance.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
acceptance_path = V / "batch-064-native-visual-411-acceptance.json"
assert not acceptance_path.exists()
save(acceptance_path, acceptance)
record = {
    "schemaVersion": 1, "execution": 411, "checkpoint": 411, "batch": "064",
    "status": acceptance["status"], "startingHead": head,
    "scope": data["execution411StartingState"]["scope"],
    "acceptanceRecord": str(acceptance_path.relative_to(R)), "acceptanceRecordSha256": sha(acceptance_path),
    "authorization": data["execution411StartingState"]["authorization"],
    "readAndProcessCounts": {"claude": {"calls": 10, "freshImages": 6},
                            "gpt": {"calls": 41, "freshImages": 28}},
    "reviewerModels": acceptance["reviewerModels"], "archivedArtifacts": artifacts,
    "freshChecks": {"validatorErrors": 0, "manifestFresh": True, "runtimeHashesVerified": hash_count,
                    "contentVersion": "ae05977ba66f42f5",
                    "budget": {"entries": 8342, "retainedBytes": 44029340,
                               "inflatedBytes": 44297678, "localZipBytes": 30107045},
                    "pythonSuiteRerun": False,
                    "qualification": "Validator/build_manifest/check_content_budget freshly ran in411 with exit0; complete current manifest freshly recomputed by canonical build_manifest helper (text CRLF normalization, binary exact bytes). Preliminary raw-byte curriculum hash assertion was an evidence-helper bug, not runtime drift; corrected before archival. Python368 and Android404/native406 remain inherited, not rerun."},
    "runtimeTeachingAndManifestUnchanged": True, "dedicatedAndroidClean": True,
    "publishedAdditions": 90, "remainingAdditions": 1138, "localDraftAdditions": 91,
    "lastPublishedCommit": data["lastPublishedCommit"], "runtimePublished": False,
    "nextAction": next_action, "limits": acceptance["limits"],
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
save(S, record)
data["stage"] = "batch-064-scoped-access-visual-evidence-ready-for-normal-signing"
data["execution411StartingState"] = {**data["execution411StartingState"], "status": "reports-and-reconciliation-archived"}
save(P, data)
print("Execution411 visual closure and scoped recovery evidence archived; normal signed local checkpoint next.")
