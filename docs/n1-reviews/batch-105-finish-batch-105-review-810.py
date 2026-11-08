"""Persist textual reconciliation without advancing runtime/publication acceptance."""
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "595bb5b4-8cc4-4f57-bcb1-4b31d3c6e957"
HEAD = "27e252daa091e21c907ff6799818f6b2da74c7aa"
MAIN = "047c2cef6b6a48b1738f2c5957de01be481c63e1"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
NEXT = (
    "SAME105 qualified Androidbf30cdead HOST+finite semantic defaultN1/All/custom actual options "
    "on the unchanged textually reconciled signed draft27e252d and new evidence checkpoint. "
    "Two serial blind initial families claude-opus-5.5/gpt-6.1-sol are complete; no actionable "
    "textual defect or consequential unresolved textual claim remains, no teaching changed and "
    "no changed-passage confirmation is required. Preserve both original reports/process/read "
    "limits and optional/withdrawn dispositions; do not promote textual acceptance to live quiz "
    "or native acceptance. Verify non-skipped RealContent/RareHan, exact qualified signed app "
    "and wholly clean dedicated heads, freshmain, live parent13320 ancestry/decoded launcher/"
    "exact session; child must not touch runner.lock. No optional historical-session recipes; "
    "use approved control/committed sources/frozen inputs. Source plan808/draft audit809 retain "
    "row116勁 full[ケイ]/[つよ.い],selected[ケイ]/[] keyけい,search-only勁い, one support雄勁/"
    "no inferred vocabularylevel, four direct kanji/six direct word guards, one reciprocalpair/"
    "two directions/zero baseline edits. All fresh native ContentSyncONCE/N1/All/meaning/"
    "curatedreading/drawing/article/Back/offline/four-font/default rendering of actual14Han "
    "including勁/巠/刂 remain mandatory after host acceptance; cmap absence is NOT glyphfailure. "
    "Then combined-current-main/fullPython/vocabulary/baseline-membership-links/manifest/per-file/"
    "media/safe-path/18000entry42MiBcompressed80MiBinflated56MiBretained budgets/normal signing/"
    "ownerfastforward/terminalgreenCI/every immutableZIP runtimehash/verifiedownerissue. "
    "Preserve every original source/review/process/readdepth/permission/OOM/ANR/routing/phone "
    "limit without retroacceptance. Preserve/report/yield actual new denial, signing hang or "
    "uncertain ownership. No106 or second runner. Published131/1228,1097remaining unchanged; "
    "supportwords are NOT N1 vocabulary delivery. Compatible Android#125+#132 required; old "
    "clients ignore curation/guards. Physicalphone/generalrelease/whole-set outstanding; project incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, repo=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(repo), *args],
                                   encoding="utf-8").strip()


def atomic(path, value):
    tmp = path.with_suffix(path.suffix + ".810.tmp")
    assert not tmp.exists()
    save(tmp, value)
    assert load(tmp) == value
    os.replace(tmp, path)


def evidence_audit():
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", repo=A) == APP and git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", repo=A)
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (13320, L.name, "running")
    executions = load(V / "batch-105-initial-executions-810.json")["initialExecutions"]
    provenance = load(V / "batch-105-review-dictionary-provenance.json")
    assert sha(C / "batch-105-initial-packet.txt") == provenance["packetSha256"]
    assert gzip.decompress((V / "batch-105-initial-packet.txt.gz").read_bytes()) == (C / "batch-105-initial-packet.txt").read_bytes()
    for row in provenance["sources"]:
        assert sha(Path(row["path"])) == row["sha256"]
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        execution = load(V / f"batch-105-initial-{label}-execution.json")
        coverage = load(V / f"batch-105-initial-{label}-coverage.json")
        assert execution["actualModels"] == [model] and execution["usageCurrentModel"] == model
        assert execution["exitCode"] == 0 and execution["multiToolResponseCount"] == 0
        assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
        assert coverage["allAssignedRangesReturned"] and len(execution["toolCalls"]) == 1
        call = execution["toolCalls"][0]
        assert call["name"] == "view" and call["success"] and call["exactRequestedTextContainedInResult"]
        assert not call["truncationMarker"] and execution["availableTools"] == ["view"]
        assert sha(V / f"batch-105-initial-{label}.md") == execution["reportSha256"]
        raw = gzip.decompress((V / f"batch-105-initial-{label}.jsonl.gz").read_bytes())
        assert hashlib.sha256(raw).hexdigest() == execution["rawExecutionSha256"]
        result = subprocess.run(["pwsh", "-NoProfile", "-Command",
                                 f"if (Get-Process -Id {execution['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                                capture_output=True)
        assert result.returncode == 0
    assert executions["claude"]["completedAt"] < executions["gpt"]["startedAt"]
    manifest = load(R / "manifest.json")
    assert manifest == json.loads(git("show", HEAD + ":manifest.json"))
    baseline = json.loads(git("show", MAIN + ":manifest.json"))
    for section, entries in baseline.items():
        if isinstance(entries, dict):
            for name, value in entries.items():
                assert manifest[section][name] == value
    new = {name for name in manifest["files"] if name not in baseline["files"]}
    assert new == {"kanji/勁.md", "words/雄勁.md", "strokes/勁.json"}
    for name in new:
        normalized = (R / name).read_bytes().replace(b"\r\n", b"\n")
        blob = subprocess.check_output(["git", "-C", str(R), "show", HEAD + ":" + name])
        assert normalized == blob
        assert hashlib.sha256(blob).hexdigest() == manifest["files"][name]
    reconciliation = load(V / "batch-105-reconciliation.json")
    assert not reconciliation["establishedActionableFindings"]
    assert not reconciliation["consequentialUnresolvedTextualClaims"]
    assert not reconciliation["teachingChangesAfterReview"]
    print(json.dumps({
        "snapshot": HEAD, "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "completeReturnedPackets": 2, "toolCallsPerReviewer": 1,
        "internalToolOverlaps": 0, "serialProcessExitVerified": True,
        "allPacketSourceHashesPreserved": True,
        "baselineRuntimeHashesPreserved": sum(len(v) for v in baseline.values() if isinstance(v, dict)),
        "runtimeAndManifestUnchangedSinceDraft": True, "runtimeAdditionsRelativeToPublishedBase": sorted(new),
        "textuallyReconciledWithoutTeachingEdits": True, "nativeOrPhoneAcceptance": False,
    }, ensure_ascii=False, indent=2))


def prepare():
    evidence_audit()
    ledger = load(S / "batch-105-progress.json")
    assert ledger["status"] == "local-unreviewed-runtime-draft"
    ledger.update(
        status="textually-reconciled-awaiting-qualified-host-and-native-acceptance",
        textualReviewClosed=["勁"], reviewClosed=[], published=[],
        independentInitialReviewSnapshot=HEAD,
        independentInitialModels=["claude-opus-5.5", "gpt-6.1-sol"],
        textualReconciliation="../n1-reviews/batch-105-reconciliation.json",
        textualReviewExecution=810, teachingChangedAfterInitialReview=False,
        limits="Both new articles are textually reconciled with no established actionable defect; no teaching changed. Full batch reviewClosed remains empty until required qualified host/finite-semantic/native/rendered acceptance. Textual CLEAN is not runtime/phone acceptance or publication; all historical limits and remaining gates are preserved.",
        nextAction=NEXT)
    save(S / "batch-105-progress.json", ledger)
    for name in ["review-batch-105-810.py", "finish-batch-105-review-810.py",
                 "preflight-810.ps1", "checks-batch-105-review-810.ps1", "issue-batch-105-review-810.ps1"]:
        shutil.copyfile(C / name, V / ("batch-105-" + name))
    shutil.copyfile(L / "preflight-810.json", V / "batch-105-runner-role-810.json")
    print("Textual reconciliation, unchanged-teaching disposition and durable recipes saved.")


def package():
    evidence_audit()
    logs = {}
    for name in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                 "vocabulary", "review-audit", "whitespace"]:
        raw = L / f"{name}-810.txt"
        archive = V / f"batch-105-{name}-810.txt.gz"
        assert raw.exists() and not archive.exists()
        archive.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        logs[name] = {"archive": archive.name, "rawBytes": raw.stat().st_size,
                      "rawSha256": sha(raw), "archiveSha256": sha(archive)}
    for name in ["batch-105-cli-help-execution-810.txt", "batch-105-cli-config-help-execution-810.txt"]:
        raw = V / name
        archive = raw.with_name(raw.name + ".gz")
        archive.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw.read_bytes()
        raw.unlink()
    save(V / "batch-105-execution-810.json", {
        "schemaVersion": 1, "execution": 810, "batch": "105", "snapshot": HEAD,
        "status": "textually-reconciled-unchanged-not-published",
        "reconciliation": "batch-105-reconciliation.json",
        "validation": logs, "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalHelpersAccessed": False, "runtimeChangedThisExecution": False,
        "runtimePublished": False, "publishedAdditions": 131, "remainingAdditions": 1097,
        "nextAction": NEXT, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "limits": "Textual and mechanical checkpoint only; no Android/native/finite live semantic/rendered/font/phone acceptance. Full original downstream gates remain mandatory.",
    })
    print("Validation logs archived losslessly; execution evidence ready for normal signed local commit.")


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert not git("diff", HEAD, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", repo=A) == APP and not git("status", "--porcelain", repo=A)
    issue = load(L / "issue-receipt-810.json")
    assert issue["verified"] and issue["author"] == "stop-cran" and issue["localCommit"] == head
    original = load(L / "progress-before-810.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 809 and p["batch"] == "105" and p["status"] == "continue"
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in original.items() if k not in changed)
    p.update(checkpoint=810, status="continue",
             stage="batch-105-textually-reconciled-awaiting-qualified-host",
             nextAction=NEXT, blocker=None)
    p["batch105TextualReviewIssueReceipt"] = issue
    p["execution810CoordinatorCheckpoint"] = {
        "schemaVersion": 1, "execution": 810, "checkpoint": 810, "batch": "105",
        "status": "continue", "stage": p["stage"], "savedCommit": head, "signature": "G",
        "reviewSnapshot": HEAD, "publishedBase": MAIN, "androidSignedHead": APP,
        "membership": ["勁"], "sourceRows": [116],
        "initialExecutions": load(V / "batch-105-initial-executions-810.json"),
        "textualReconciliation": "docs/n1-reviews/batch-105-reconciliation.json",
        "evidence": "docs/n1-reviews/batch-105-execution-810.json",
        "textualReviewClosed": ["勁"], "reviewClosed": [], "published": [],
        "consequentialUnresolvedTextualClaims": [], "teachingChanged": False,
        "runtimeChangedThisExecution": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "actualBuilderChecked": False,
        "nativeDrawingAccepted": False, "renderedAcceptance": False,
        "publishedAdditions": 131, "remainingAdditions": 1097, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False,
        "finalRunnerPreflight": load(L / "preflight-810-final.json"),
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreserved": True,
        "originalRootKeysCompared": len(original), "issueUpdate": issue["url"],
        "ownerIssueAuthorAndBodyVerified": True, "nextAction": NEXT,
        "limits": "Textual reconciliation is complete without edits; full batch reviewClosed remains empty pending required host/live semantic/native/rendered gates. No publication or project-completion claim.",
    }
    assert all(p[k] == value for k, value in original.items() if k not in changed)
    atomic(C / "progress.json", p)
    check = load(C / "progress.json")
    assert check == p
    assert all(check[k] == value for k, value in original.items() if k not in changed)
    save(L / "checkpoint-verification-810.json", {
        "checkpoint": 810, "originalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "changedRootFields": sorted(changed),
        "savedCommit": head, "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "ownerIssueAuthorAndBodyVerified": True, "status": "continue",
    })
    print("Checkpoint810 persisted and all original historical values verified unchanged.")


if __name__ == "__main__":
    {"audit": evidence_audit, "prepare": prepare, "package": package, "checkpoint": checkpoint}[sys.argv[1]]()
