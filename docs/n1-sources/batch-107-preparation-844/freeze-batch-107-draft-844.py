"""Archive checked draft evidence before the normal local signed freeze."""
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "rollout-recovered" / "learning-japanese"
S = R / "docs" / "n1-sources"
L = C / "logs" / "70ed1fca-b2a0-4267-bff3-7b7e4362d9ea"
START = "dfed2c150d7fe921aacdb1d616ff527df1935f3b"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=True, indent=2) + "\n")


p = load(C / "progress.json")
assert p["checkpoint"] == 843 and p["status"] == "continue" and p["batch"] == "107"
assert subprocess.check_output(["git", "-C", str(R), "rev-parse", "HEAD"], text=True).strip() == START
plan = load(S / "batch-107-source-completion-plan.json")
audit = load(S / "batch-107-runtime-audit.json")
assert audit["manifestFresh"] and audit["exactPinnedConverterOutput"]
suite = (L / "python-suite-844.txt").read_text(encoding="utf-8-sig")
assert "\nOK\n" in suite and "FAILED" not in suite
for name in ("validator", "manifest", "vocabulary", "budget", "whitespace"):
    assert (L / f"{name}-844.txt").exists()
checks = load(L / "preflight-844-checks.json")
assert checks["sessionId"] == L.name and checks["checkpoint"] == 843 and not checks["lockTouched"]
draft = {
    "schemaVersion": 1, "batch": "107", "execution": 844, "status": "local-unreviewed-runtime-draft",
    "baseCommit": audit["baseCommit"], "signedSourceSnapshot": START,
    "membership": ["勘"], "sourceRows": [118], "runtimeDrafted": ["勘"],
    "reviewClosed": [], "published": [], "newSupportingWordArticles": [],
    "reusedSupportingWordArticles": plan["supportPlan"]["reused"],
    "sourceCompletionPlan": "batch-107-source-completion-plan.json",
    "runtimeAudit": "batch-107-runtime-audit.json",
    "fullReadingDispositions": plan["kanjiPlan"]["readingRows"],
    "supplementaryRecognition": plan["kanjiPlan"]["supplementaryRecognition"],
    "allMappedPairs": plan["linkPlan"]["allMappedPairs"],
    "requiredDirections": plan["linkPlan"]["requiredDirections"],
    "requiredDirectionsCurrentStatus": "All ten authored and mechanically verified; historical currentlyPresent flags describe source preparation only.",
    "exactReusedChanges": plan["linkPlan"]["exactReusedChanges"],
    "newTeaching": ["kanji/勘.md", "kanji/定.md Common words 勘定 bullet",
                    "kanji/違.md Common words 勘違い bullet"],
    "initialReviewerScope": ["kanji/勘.md", "words/勘.md", "words/勘定.md",
                             "words/勘違い.md", "kanji/定.md", "kanji/違.md"],
    "initialReviewEvidence": "Same complete frozen member/comparison packets, full raw character records, "
                             "public Daijisen wrapper, all affected complete cards, actual comparison/legacy cards. "
                             "Two different actual model families; blind initial prompts, serial processes AND tools, "
                             "no shell/edit/delegation or broad approval; retain complete reports and actual ranges/model/exit evidence.",
    "curatedWrongChoices": audit["curatedWrongChoices"],
    "directKanjiGuards": plan["kanjiPlan"]["directGuardRationale"],
    "preservedDirectWordPairs": audit["preservedDirectWordPairs"],
    "laterProductionQuizScope": plan["legacyFallbackPlan"]["laterAcceptance"],
    "finalLearnerHanCount": audit["finalLearnerHanCount"],
    "allInspectionHanCount": audit["allInspectionHanCount"],
    "fontDisposition": "Four baseline missing cmap points 宀/辵/辶/韋 remain native inspection targets, not glyph failures. "
                       "All four actual modes/default system plus three bundled fonts and every audited Han remain pending.",
    "strokeGeneration": "Unchanged repository tools/generate_strokes.py convert on retained exact batch107 SVG, "
                        "16points/path,11ordered paths, pinned revision; order_variants applied only if already recorded. "
                        "No upstream refetch, hand geometry edit or converter change.",
    "coordinatorSourceReads": {
        "memberPacketRanges": [[1,350],[351,700],[701,1050],[1051,1400],[1401,1733]],
        "comparisonPacketRanges": [[1,365],[366,730],[731,1095],[1096,1463]],
        "rawMemberRecord": "Entire75line record",
        "rawComparisonRanges": [[1,330],[331,660],[661,990],[991,1289]],
        "otherCompleteReads": ["exact13lineDaijisenwrapper", "exactpinnedSVG", "allfiveaffectedbaselinecards",
                               "words/考える.md", "kanji/勤.md", "kanji/助.md", "kanji/期.md"],
        "limits": "Coordinator fresh returned text, not independent review, equal semantic depth or new "
                  "fresh read of every baseline comparison snapshot. Original843 source inspection retained separately.",
    },
    "auditRepresentationCorrection": audit["originalAuditFailure"],
    "mechanicalDraftChecksOnly": True, "reviewersLaunched": 0, "freshHostOrNative": False,
    "runtimePublished": False, "publishedAdditions": 133, "remainingAdditions": 1095,
    "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
    "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False,
    "remainingAcceptance": p["execution843CoordinatorCheckpoint"]["nextAction"],
    "limits": "Signed LOCAL UNREVIEWED freeze is not review closure or delivery. Original source/review/"
              "productionQuiz/HOST/native/rendered/latestmain/signature/CI/immutableZIP/budget/ownerreport gates "
              "remain mandatory before counting107 or starting108.",
}
new(S / "batch-107-runtime-draft.json", draft)
archive = S / "batch-107-preparation-844"
archive.mkdir(exist_ok=False)
files = [
    C / name for name in ("preflight-844.ps1", "checkpoint-844.py", "audit-batch-107-runtime.py",
                         "test-batch-107-runtime.py", "checks-batch-107-draft-844.ps1",
                         "freeze-batch-107-draft-844.py", "post-batch-107-draft-844.ps1",
                         "batch-107-draft-844-issue-template.txt", "authoring-artifact-path-notes.txt",
                         "runner-lock-role-notes.txt", "progress-reader-lock-notes.txt")
]
files += [L / name for name in (
    "preflight-844.json", "preflight-844-checks.json", "audit-regressions-844.txt",
    "runtime-audit-844.txt", "audit-regressions-844-lf.txt", "runtime-audit-844-lf.txt",
    "audit-regressions-844-final.txt", "runtime-audit-844-final.txt",
    "python-suite-844.txt", "validator-844.txt", "manifest-844.txt", "vocabulary-844.txt",
    "budget-844.txt", "whitespace-844.txt",
)]
archived = []
for source in files:
    target = archive / source.name
    assert source.exists() and not target.exists()
    shutil.copyfile(source, target)
    assert sha(source) == sha(target)
    archived.append({"path": target.relative_to(R).as_posix(), "sha256": sha(target)})
record = {
    "schemaVersion": 1, "execution": 844, "batch": "107",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
    "baseCommit": audit["baseCommit"], "signedSourceSnapshot": START,
    "stage": "local-unreviewed-runtime-draft-awaiting-normal-signature",
    "runtimeDraft": "batch-107-runtime-draft.json", "runtimeAudit": audit,
    "draftSha256": sha(S / "batch-107-runtime-draft.json"),
    "runtimeAuditSha256": sha(S / "batch-107-runtime-audit.json"),
    "archivedArtifacts": archived,
    "startingState": p["execution844StartingState"],
    "pythonSuiteResult": suite[suite.rfind("\nRan "):].strip(),
    "allOriginalAcceptanceGatesRemainMandatory": True,
    "reviewersLaunched": 0, "nativeOrHostAcceptance": False, "runtimePublished": False,
    "publishedAdditions": 133, "remainingAdditions": 1095, "parentLockTouched": False,
    "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
    "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False,
}
new(S / "execution-844.json", record)
print("Bounded runtime draft, audit, failures and current reusable helpers archived; no review/publication claimed.")
