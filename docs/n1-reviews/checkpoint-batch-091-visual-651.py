import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("visual651", C / "review-batch-091-visual-651.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, L = review.R, review.A, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
STAGE = "visual-partial-process-contract-violation-awaiting-reconciliation"
NEXT = (
    "SAME091 only: read docs/n1-sources/execution-651.json and "
    "docs/n1-reviews/batch-091-visual-partial-651.json. Original Claude session "
    "075924f2-f60b-4ae0-bf3f-341db3dfbd74 returned a complete dependent report "
    "(actual claude-opus-5.5, process25128 exited0), but violated explicitly required "
    "serial tool work: fifteen image views launched together, fourteen overlaps. "
    "Wrapper correctly rejected process-contract acceptance; preserve report/raw events "
    "and violation, NOT successful serial/two-family visual closure. Original GPT "
    "8da57d75-100b-4996-acf7-f52b0b446472 has NOT received visual follow-up. "
    "Runtime remains unchanged from textually confirmed c2a59d5c, native archivef6b2ee39. "
    "Complete original GPT visual assessment on this SAME frozen teaching/native sample "
    "without exposing Claude findings; require actual serial calls/process exit and "
    "preserve all evidence, no blind initial credit. Use approved control packet/contact-map/"
    "originals; full50captures map26distinct bytes (23nonfontframes in12sheets,3originalfontpanels). "
    "Do not blindly rerun failed helper or erase its overlap assertions/evidence. "
    "Resolve Claude minor rendered mnemonic finding by exact evidence: kanji/刃.md:24 "
    "describes extra mark as shaped like丶, but original defaultGothic question and "
    "font-panel3 show detached left-falling shortmark while pinned drawingreference and "
    "otherfonts show crossing right-fallingmark. Coordinator separately viewed these "
    "THREE originals and agrees qualifier is warranted, not missingglyph/requiredfontchange. "
    "After preserved originalGPT assessment, make only necessary font-variable modernshape "
    "wording correction under full authoringinstructions/source requirements, validate/"
    "regeneratemanifest/normal signed localfreeze, then bounded changed-passage and relevant "
    "rendered confirmation in BOTH original sessions with actual serial toolwork. "
    "Claude's prior overlap-bearing observations remain useful hypotheses, not compliant "
    "serial visual acceptance. No repeated broad dictionaries/native/fullpacket loops "
    "unless specific changedcontent requires them. Preserve all original textual "
    "findings/disagreement/optional/readlimits, native650 two terminalcases0/noskips "
    "and fullarchive ContentSyncONCE1114kanji5070words123N1zeroProblems/versioncb3c857f3614485d/"
    "Roomreadingepoch1;8432runtimehashes. Onlykunは/noon keys; rawジンニン/はやいばき.る "
    "retained in sourceorder; recognition not uniformlyrare/sourceonly; threepinned "
    "drawingstrokes/injectedtrace/recallgiveup NOT humanhandwriting/successfulMLKit/phone. "
    "Bothnewarticles/onepairtwodirections/先端forefrontroute/SystemBack/offline/fivedirectguards/"
    "N1andAllthreecuratedwrongcards/zerofallback inherited, not latestappmain/phone. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2. Parent19008 retains "
    "runner.lock: verify liveancestry/session/decodedlauncher/checkpoint/exactsignedheads/"
    "whollyclean, NOchildlockreacquisition/delete/unlock. Approvedcontrol/committedsources "
    "only, NOoptionalhistoricalsessionrecipes. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. All original source/baseline/link/reading/twofamily/"
    "native/currentmainnormalmerge/changedteachingreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPentryhash/original18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/ownerissue gates remain. "
    "Published117/1228,1111remaining unchanged; physicalphone/generalrelease/whole-set "
    "outstanding. No092/runtimepublication/newrunner."
)


def runtime():
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
                    verified[path] = actual
    assert len(verified) == 8432 and manifest["contentVersion"] == "cb3c857f3614485d"
    assert not git("diff", review.TEACHING, "HEAD", "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")
    return {"runtimeHashesVerified": len(verified), "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True}


def archive():
    review.frozen()
    target = V / "batch-091-visual-partial-651.json"
    assert not target.exists()
    record = load(C / "batch-091-visual-651-claude-execution.json")
    assert record["exitCode"] == 0 and record["actualModels"] == ["claude-opus-5.5"]
    assert record["usageCurrentModel"] == "claude-opus-5.5"
    assert record["allAssignedResourcesSuccessfullyReturned"] and not record["unfinishedTools"]
    assert len(record["toolCalls"]) == 19 and len(record["observedToolOverlaps"]) == 14
    assert len(record["actualDecodedImageReturns"]) == 15
    subprocess.run(["pwsh", "-NoProfile", "-Command",
                    f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                   check=True, capture_output=True)
    assert not (C / "batch-091-visual-651-gpt.jsonl").exists()
    prefix = C / "batch-091-visual-651-claude"
    raw = prefix.with_suffix(".jsonl")
    assert sha(raw) == record["rawSha256"]
    assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
    verification = runtime()
    for artifact in load(R / "docs" / "n1-sources" / "execution-650.json")["artifacts"]:
        assert sha(R.joinpath(*artifact["path"].split("/"))) == artifact["sha256"]
    receipts = []
    archived = V / (raw.name + ".gz")
    archived.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
    assert gzip.decompress(archived.read_bytes()) == raw.read_bytes()
    receipts.append({"source": str(raw), "archive": archived.relative_to(R).as_posix(),
                     "sourceSha256": sha(raw), "archiveSha256": sha(archived), "losslessGzip": True})
    sources = [Path(__file__), C / "review-batch-091-visual-651.py", review.PACKET,
               C / "batch-091-visual-651-inputs.json", C / "post-batch-091-visual-651.ps1",
               C / "batch-091-visual-cli-help-651.txt", C / "batch-091-visual-cli-config-651.txt",
               C / "review-batch-089-visual-633.py",
               C / "batch-091-visual-651-claude-execution.json"]
    sources += [prefix.with_suffix(s) for s in [".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"]]
    for source in sources:
        name = "batch-091-visual-651-base-recipe.py" if source.name == "review-batch-089-visual-633.py" else source.name
        archived = V / name
        assert not archived.exists()
        shutil.copyfile(source, archived)
        receipts.append({"source": str(source), "archive": archived.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(archived)})
    sheets = V / "batch-091-visual-651-inspection"
    assert not sheets.exists()
    shutil.copytree(review.INSPECTION, sheets)
    for source in sorted(review.INSPECTION.iterdir()):
        archived = sheets / source.name
        assert sha(archived) == sha(source)
        receipts.append({"source": str(source), "archive": archived.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(archived)})
    partial = {
        "schemaVersion": 1, "execution": 651, "batch": "091", "status": STAGE,
        "snapshot": review.HEAD, "teachingSnapshot": review.TEACHING,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "originalReportsPreserved": True, "newBlindInitialReviewCredit": False,
        "processes": {"claude": record},
        "gptVisualLaunched": False, "serialReviewerProcessCount": 1,
        "claudeProcessActuallyExited": True,
        "toolProcessContract": {
            "accepted": False, "required": "One view per response, no overlapping tool calls.",
            "actual": "Three serial text reads; fifteen simultaneous image calls (fourteen overlap starts); one later serial original-image view.",
            "coordinatorWrapperExitCode": 1, "reviewerExitCode": 0,
            "assertion": "Wrapper rejected actual tool overlap after preserving complete original report/events/execution record.",
            "permissionDenial": False,
            "disposition": "Preserve useful finding as evidence; do not call this compliant serial visual closure. Yield recoverable partial checkpoint; no GPT launch or runtime edit.",
        },
        "findings": [{
            "id": "V1", "severity": "minor", "facet": "rendered comprehensibility",
            "file": "kanji/刃.md:24", "reportedBy": "Claude",
            "status": "unresolved", "coordinatorAssessment": "verified localized explanation mismatch; minimal font-variable qualifier warranted",
            "claim": "Mnemonic's extra mark shaped like丶 does not match the detached left-falling inner shortmark in default Gothic; other three font selections and pinned drawing reference use a right-falling crossing mark.",
            "impact": "Learner is asked to identify a specific visual direction/shape not present in the default quiz glyph, then traces a different supported form.",
            "remedy": "Qualify modern-shape mnemonic as font-variable extra shortmark; reference actual stroke-order diagram without asserting universal glyph shape. No font/geometry/metadata change required.",
            "evidence": [str(review.N / name) for name in [
                "n1-091-font-panel-3.png", "n1-091-meaning-question.png", "n1-091-drawing-trace.png"]],
            "confidence": "High visible difference; medium learning impact. Coordinator separately viewed all three originals; tool scales1080x2400 to900x2000.",
            "limits": "Claude tool concurrency was noncompliant. Preserve report and verify with exact evidence/original reviewers; no new two-family closure claim.",
        }],
        "verdicts": {
            "kanji/刃.md": {"correctness": "CLEAN-inherited-textual",
                            "scopedCoverage": "CLEAN-inherited-textual",
                            "renderedComprehensibility": "NEEDS FIX",
                            "limits": "One noncompliant visual follow-up; two-family closure pending."},
            "words/刃.md": {"correctness": "CLEAN-inherited-textual",
                            "scopedCoverage": "CLEAN-inherited-textual",
                            "renderedComprehensibility": "UNVERIFIED",
                            "limits": "Claude reported CLEAN, but process-contract rejection and pending GPT prevent acceptance."},
        },
        "priorDispositions": "Original textual correction resolved; Claude optional expansions/slang hypothesis and supplied-receipt/device/font-face limits retained in complete report. No new mandatory word guard or app change established.",
        "runtime": verification,
        "freshAndroidOrNativeClaimed": False, "independentVisualConfirmationClosed": False,
        "limits": [
            "One reviewer process, actual Claude family only this checkpoint. Initial two-family textual evidence remains intact.",
            "All assigned resources returned; payload delivery and hashes not comprehension. Extra original meaning-question was also returned; 15 requested image returns audited for decoding, extra original retained in raw events and report.",
            "Twelve resized sheets cover23distinct nonfontframes, mapping47captures via exact duplicates; three originalfontpanels cover remaining3. Not50separatefreshviews or88PaintPNGs/fallbackface identification.",
            "No new native/device/phone/humanhandwriting/successfulMLKit/native-speaker/learningeffectiveness certification.",
            "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latestappmain.",
            "All currentmain/combinedchecks/twofamilyconfirmation/normalsigning/publication/CI/publicZIP/phone/generalrelease/whole-set gates remain.",
        ],
        "nextAction": NEXT,
    }
    save(target, partial)
    save(R / "docs" / "n1-sources" / "execution-651.json", {
        "schemaVersion": 1, "execution": 651, "batch": "091",
        "startingState": load(C / "progress.json")["execution651StartingState"],
        "status": STAGE, "snapshot": review.HEAD, "teachingSnapshot": review.TEACHING,
        "runtime": verification, "reviewRecord": target.relative_to(R).as_posix(),
        "receipts": receipts, "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "independentReviewersLaunched": 1, "compliantVisualConfirmations": 0,
        "toolOverlapViolationPreserved": True, "gptVisualLaunched": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": "7100a3873282b54515b9ef130766e77cf151a47b",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Preserved complete partial report, noncompliance, finding and all recipes; runtime unchanged.")


def finalize():
    review.ownership()
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == review.HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == review.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G" and not git("status", "--porcelain", repo=A)
    verification = runtime()
    for receipt in load(R / "docs" / "n1-sources" / "execution-651.json")["receipts"]:
        archived = R.joinpath(*receipt["archive"].split("/"))
        assert sha(archived) == receipt["archiveSha256"]
        if receipt.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(archived.read_bytes())).hexdigest() == receipt["sourceSha256"]
    body = (C / "batch-091-visual-651-issue-body.txt").read_text(encoding="utf-8-sig")
    posted, receipt = [load(C / f"batch-091-visual-651-issue-{name}.json") for name in ["posted", "receipt"]]
    assert posted["id"] == receipt["id"] and posted["body"] == receipt["body"] == body
    assert posted["user"]["login"] == receipt["user"]["login"] == "stop-cran"
    state, before = load(C / "progress.json"), load(L / "progress-before-651.json")
    assert state["checkpoint"] == 650 and state["stage"] == "batch-091-dependent-visual-confirmations"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 651, "checkpoint": 651, "batch": "091",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-651.json",
        "reviewRecord": "docs/n1-reviews/batch-091-visual-partial-651.json",
        "independentReviewersLaunched": 1, "compliantVisualConfirmations": 0,
        "toolOverlapViolationPreserved": True, "observedOverlapStarts": 14,
        "reviewerProcessExited": True, "gptVisualLaunched": False,
        "unresolvedMinorRenderedFindings": 1, "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        **verification, "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": "7100a3873282b54515b9ef130766e77cf151a47b",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    state.update(checkpoint=651, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution651CoordinatorCheckpoint"] = checkpoint
    state["batch091VisualPartialCheckpoint"] = checkpoint
    state["execution651StartingState"]["status"] = "signed-local-partial-visual-evidence-checkpoint-complete"
    save(C / "progress.json", state)
    reread = load(C / "progress.json")
    assert all(reread[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-651.json", checkpoint)
    print("Checkpoint651 persisted; original historical root values preserved:", len(before))
    print("Saved signed evidence", saved, "issue", receipt["html_url"])


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
