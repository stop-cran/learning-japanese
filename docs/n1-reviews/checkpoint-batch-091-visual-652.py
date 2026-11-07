import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("visual652", C / "review-batch-091-visual-652.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, L = review.R, review.A, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
STAGE = "mnemonic-corrected-awaiting-two-original-session-confirmations"
NEXT = (
    "SAME091 only: read docs/n1-sources/execution-652.json and "
    "docs/n1-reviews/batch-091-visual-reconciliation-652.json. Original GPT "
    "8da57d75-100b-4996-acf7-f52b0b446472 completed compliant dependent visual "
    "assessment on unchanged c2a59d5c teaching: actual gpt-6.1-sol/PID28408/exited0/"
    "18serialviews/15PNGs/nooverlap/allassignedtextreturned. It reported no defect; "
    "preserve disagreement with Claude rather than inventing agreement. Coordinator "
    "freshly viewed original font-panel3/meaningquestion/drawingtrace and accepts "
    "Claude's localized font-variable mnemonic concern despite GPT CLEAN verdict. "
    "Only kanji/刃.md:24 now describes an extra shortmark: somefonts separate, "
    "pinneddiagram crosses longer slopingstroke. Metadata/word/strokes/quiz/links unchanged. "
    "Current manifest version bfe65483a821fc13; all8432hashes/freshness verified. "
    "This is a signed LOCAL UNCONFIRMED correction, not review-closed or published. "
    "Next freeze is execution652 savedCommit. Reuse ORIGINAL Claude "
    "075924f2-f60b-4ae0-bf3f-341db3dfbd74 then ORIGINAL GPT "
    "8da57d75-100b-4996-acf7-f52b0b446472 SERIAL dependent changed-passage and "
    "relevant-rendered confirmations. Give each own report/exactdiff/newcompletekanji/"
    "threeoriginalfont-and-drawingPNGs; one toolcall at a time, actualexit/read audit. "
    "Claude651 fourteenoverlaps remain rejected process evidence, NOT compliant serial "
    "visualclosure; no newblindinitialcredit. No repeated broad dictionary/fullnative/"
    "packetloops unless newly necessary. Native650 passed TWO terminalcases0/noskips "
    "on OLD archivef6b2ee39/versioncb3c857f3614485d: ContentSyncONCE1114kanji5070words"
    "123N1zeroProblems/Roomepoch1. Do NOT relabel that as import/rendering of revised "
    "mnemonic/version. OldPNGssupport actualfontdifference, not revisedtextlayout. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latestappmain/phone. "
    "Onlykunは/noon/rawジンニン/はやいばき.る/sourceorder preserved; threepinnedstrokes/"
    "injectedtrace not humanhandwriting/successfulMLKit. Bothnewarticles/onepairtwodirections/"
    "先端route/fivedirectguards/N1andAllthreewrongcards/zerofallback inherited in exact "
    "historical receipts, not universalpoolcertification. Parent19008 retainsrunner.lock: "
    "verifyliveancestry/exactsession/decodedlauncher/checkpoint/exactsignedheads/whollyclean; "
    "NOchildreacquire/delete/unlock. Approvedcontrol/committedsources only, NOoptional "
    "historicalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. All originalsource/baseline/link/reading/twofamily/native/"
    "currentmainnormalmerge/changedteachingreview/combinedchecks/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPentryhash/original18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/ownerissue gates remain. "
    "Published117/1228,1111remaining; physicalphone/generalrelease/whole-set outstanding. "
    "No092/runtimepublication/newrunner."
)


def ownership():
    review.prior.L = L
    review.prior.ownership()
    assert git("rev-parse", "HEAD", repo=A) == review.prior.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 651 and state["batch"] == "091"


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    previous = json.loads(git("show", review.HEAD + ":manifest.json"))
    assert build_manifest(R) == manifest
    verified, changed = {}, []
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
                    if previous[kind][path] != actual:
                        changed.append(path)
            assert set(section) == set(previous[kind]), kind
    assert len(verified) == 8432 and changed == ["kanji/\u5203.md"]
    assert manifest["contentVersion"] == "bfe65483a821fc13"
    old = git("show", review.HEAD + ":kanji/\u5203.md")
    new = (R / "kanji" / "\u5203.md").read_text(encoding="utf-8").strip()
    before = next(line for line in old.splitlines() if line.startswith("**Modern-shape"))
    after = next(line for line in new.splitlines() if line.startswith("**Modern-shape"))
    assert old.replace(before, after) == new
    return {
        "runtimeHashesVerified": len(verified), "contentVersion": manifest["contentVersion"],
        "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True,
        "changedRuntimePayloads": changed, "onlyMnemonicParagraphChanged": True,
        "allOtherRuntimePayloadsPreserved": True,
        "metadataReadingsOrderQuizLinksWordExclusionsAndStrokesUnchanged": True,
        "before": before, "after": after,
    }


def archive():
    ownership()
    assert git("rev-parse", "HEAD") == review.HEAD and git("log", "-1", "--format=%G?") == "G"
    target = V / "batch-091-visual-reconciliation-652.json"
    assert not target.exists()
    record = load(C / "batch-091-visual-652-gpt-execution.json")
    assert record["exitCode"] == 0 and record["actualModels"] == ["gpt-6.1-sol"]
    assert record["usageCurrentModel"] == "gpt-6.1-sol"
    assert len(record["toolCalls"]) == 18 and len(record["actualDecodedImageReturns"]) == 15
    assert record["allAssignedResourcesSuccessfullyReturned"]
    assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
    subprocess.run(["pwsh", "-NoProfile", "-Command",
                    f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                   check=True, capture_output=True)
    verification = runtime()
    prefix = C / "batch-091-visual-652-gpt"
    raw = prefix.with_suffix(".jsonl")
    assert sha(raw) == record["rawSha256"]
    assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
    archived_raw = V / (raw.name + ".gz")
    assert gzip.decompress(archived_raw.read_bytes()) == raw.read_bytes()
    receipts = [{
        "source": str(raw), "archive": archived_raw.relative_to(R).as_posix(),
        "sourceSha256": sha(raw), "archiveSha256": sha(archived_raw), "losslessGzip": True,
    }]
    sources = [Path(__file__), C / "review-batch-091-visual-652.py",
               C / "post-batch-091-visual-652.ps1",
               C / "batch-091-visual-cli-help-652.txt",
               C / "batch-091-visual-cli-config-652.txt",
               C / "batch-091-visual-652-gpt-execution.json",
               C / "batch-091-visual-652-validation.txt",
               C / "batch-091-visual-652-manifest.txt"]
    sources += [prefix.with_suffix(s) for s in [".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"]]
    for source in sources:
        archived = V / source.name
        assert not archived.exists()
        shutil.copyfile(source, archived)
        receipts.append({"source": str(source), "archive": archived.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(archived)})
    diff = git("diff", review.HEAD, "--", str(R / "kanji" / "\u5203.md"), str(R / "manifest.json"))
    (V / "batch-091-mnemonic-correction-652.diff").write_text(diff + "\n", encoding="utf-8")
    evidence = []
    native = V / "batch-091-native" / "execution-650"
    for name in ["n1-091-font-panel-3.png", "n1-091-meaning-question.png", "n1-091-drawing-trace.png"]:
        file = native / name
        evidence.append({"path": file.relative_to(R).as_posix(), "sha256": sha(file),
                         "freshCoordinatorView": True,
                         "limits": "Original capture, tool resized1080x2400 to900x2000; not revised-text rendering."})
    reconciliation = {
        "schemaVersion": 1, "execution": 652, "batch": "091", "status": STAGE,
        "reviewedSnapshot": review.HEAD, "reviewedTeachingSnapshot": review.prior.TEACHING,
        "correctionSnapshot": "Commit containing this file; see execution652CoordinatorCheckpoint.savedCommit.",
        "originalReportsPreserved": True, "newBlindInitialReviewCredit": False,
        "gptVisualExecution": record,
        "priorClaudeVisualExecution": "batch-091-visual-partial-651.json",
        "priorClaudeToolOverlapViolationPreservedNotAccepted": True,
        "gptVisualAcceptedOnlyForPreCorrectionSnapshot": True,
        "reconciliation": [{
            "id": "V1", "severity": "minor", "facet": "rendered comprehensibility",
            "file": "kanji/\u5203.md:24", "status": "partially resolved",
            "claim": "Unqualified mark shaped like\u4e36 does not describe the separate left-falling shortmark in default Gothic, unlike crossing mark in other fonts/pinned diagram.",
            "claude": "Established minor concern, but original execution violated serial tool contract.",
            "gpt": "Reported CLEAN after compliant serial inspection; mentioned modern-shape mnemonic including visible\u4e36, without specifically adjudicating default-versus-diagram mark shape.",
            "disagreement": "Preserved. No claim that GPT independently found or agreed with the concern; no model-vote decision.",
            "coordinatorAssessment": "Fresh inspection of all three original captures verifies detached left-falling versus crossing right-falling marks. A narrow qualifier helps match both supported shapes, without a missing-glyph or font-change claim.",
            "remedy": "Describe extra shortmark, explicitly distinguish some font renderings from the actual stroke-order diagram. No historical classification, spelling, reading, geometry or app change.",
            "independentChangedPassageConfirmation": "Pending in BOTH original sessions.",
            "evidence": evidence, "confidence": "High visible difference; medium localized learning impact.",
        }],
        "priorDispositions": "All original initial/textual-confirmation reports, optional expansions, nonactionable hypotheses, source/read limits and Claude/GPT disagreement remain intact in their exact original reports.",
        "validation": verification,
        "runtimeChanged": True, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False,
        "limits": [
            "One new compliant original GPT dependent visual review; prior Claude noncompliance remains rejected, not silently repaired or two-family visual closure.",
            "Fifteen PNG views represent50captures via exact duplicate mapping, not50freshoriginalviews. Delivery/ranges/hashes not comprehension.",
            "New mnemonic and manifest version have NOT been independently confirmed, imported or rendered natively. Native650 only certifies its old archive/version; no rebranding.",
            "Original API35/test-onlyAndroid/fontface/Paintprobe/injectedtrace/MLKit/phone/source limits remain; no latest-app-main or general-release claim.",
            "All publication, combined-current-main, archive/CI and whole-set gates remain unchanged.",
        ],
        "nextAction": NEXT,
    }
    save(target, reconciliation)
    save(R / "docs" / "n1-sources" / "execution-652.json", {
        "schemaVersion": 1, "execution": 652, "batch": "091", "status": STAGE,
        "startingState": load(C / "progress.json")["execution652StartingState"],
        "reviewRecord": target.relative_to(R).as_posix(), "receipts": receipts,
        "runtime": verification, "runtimeChanged": True, "runtimeAccepted": False,
        "runtimePublished": False, "independentReviewersLaunched": 1,
        "gptVisualAssessmentCompleted": True, "serialProcessAndToolsVerified": True,
        "twoFamilyCorrectionConfirmation": "pending", "priorClaudeViolationPreserved": True,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": "7100a3873282b54515b9ef130766e77cf151a47b",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Archived original GPT assessment and exact localized correction; both confirmations pending.")


def finalize():
    ownership()
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == review.HEAD
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    verification = runtime()
    for item in load(R / "docs" / "n1-sources" / "execution-652.json")["receipts"]:
        archived = R.joinpath(*item["archive"].split("/"))
        assert sha(archived) == item["archiveSha256"]
        if item.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(archived.read_bytes())).hexdigest() == item["sourceSha256"]
    body = (C / "batch-091-visual-652-issue-body.txt").read_bytes().decode("utf-8-sig")
    posted, receipt = [load(C / f"batch-091-visual-652-issue-{name}.json") for name in ["posted", "receipt"]]
    assert posted["id"] == receipt["id"] and posted["body"] == receipt["body"] == body
    assert posted["user"]["login"] == receipt["user"]["login"] == "stop-cran"
    state, before = load(C / "progress.json"), load(L / "progress-before-652.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[key] == value for key, value in before.items() if key not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 652, "checkpoint": 652, "batch": "091",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-652.json",
        "reviewRecord": "docs/n1-reviews/batch-091-visual-reconciliation-652.json",
        "gptOriginalSession": "8da57d75-100b-4996-acf7-f52b0b446472",
        "actualModel": "gpt-6.1-sol", "reviewerPid": 28408, "reviewerExited": True,
        "serialViewCalls": 18, "imagesViewed": 15, "observedToolOverlaps": 0,
        "priorClaudeToolOverlapViolationPreserved": True,
        "twoFamilyCorrectionConfirmation": "pending", "runtimeChanged": True,
        "runtimeAccepted": False, "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
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
    state.update(checkpoint=652, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution652CoordinatorCheckpoint"] = checkpoint
    state["batch091MnemonicCorrectionCheckpoint"] = checkpoint
    state["execution652StartingState"]["status"] = "signed-local-unconfirmed-mnemonic-correction-persisted"
    save(C / "progress.json", state)
    reread = load(C / "progress.json")
    assert all(reread[key] == value for key, value in before.items() if key not in allowed)
    save(L / "checkpoint-652.json", checkpoint)
    print("Checkpoint652 persisted; original historical root values preserved:", len(before))
    print("Saved signed local correction", saved, "issue", receipt["html_url"])


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
