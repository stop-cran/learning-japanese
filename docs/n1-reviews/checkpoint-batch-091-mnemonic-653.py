import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("confirmation653", C / "confirm-batch-091-mnemonic-653.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, L = review.R, review.A, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
STAGE = "two-family-mnemonic-confirmed-awaiting-revised-native-and-combined-acceptance"
NEXT = (
    "SAME091 only: read docs/n1-sources/execution-653.json and "
    "docs/n1-reviews/batch-091-mnemonic-reconciliation-653.json. Both ORIGINAL sessions "
    "confirmed corrected kanji/刃.md:24 on signed1cfd5bd3, serially: Claude "
    "075924f2-f60b-4ae0-bf3f-341db3dfbd74/claude-opus-5.5/PID18224 then GPT "
    "8da57d75-100b-4996-acf7-f52b0b446472/gpt-6.1-sol/PID30260; both exited0, "
    "six serial complete views each/three decoded original PNGs/nooverlaps/nounfinishedtools. "
    "Localized V1 resolved in text by both; GPT's earlier CLEAN/non-discovery and Claude651 "
    "fourteen overlap starts remain historical, not rewritten agreement or accepted serial execution. "
    "Optional detached-vs-separate/direction/here wording stays optional; no further teaching edit required. "
    "Only old PNGs were viewed, supporting shape description NOT revised-text layout. "
    "Current8432hashes/freshmanifest/versionbfe65483a821fc13 verified; runtime untouched this execution. "
    "Next bounded checkpoint: establish the smallest justified revised-version native import/rendering "
    "confirmation using the existing approved control fixture and test-only Android checkout, "
    "preserving old archive/test receipts; revised mnemonic/version has NOT been natively imported/rendered. "
    "Do not blindly rerun broad dictionaries or reviews. Native650's two terminalcases0/no skips/"
    "ContentSyncONCE/fullarchivef6b2ee39/versioncb3c857f3614485d/1114kanji5070words123N1/"
    "zeroProblems/Roomepoch1 remain OLD-version functional evidence. Existing source/read/phone/"
    "fontface/Paintprobe/injectedtrace/MLKit/testonlyAndroid1c1b7bf4/productionf9b59a2 limitations "
    "remain; no latest-app-main claim. Verify fresh exact device/port ownership before native "
    "launch, never touch other emulators; no resource-heavy concurrency. Parent19008 retainsrunner.lock: "
    "verify live ancestry/exact session/decoded launcher/checkpoint/exact signed heads/whollyclean, "
    "NOchild reacquire/delete/unlock. Approved control/committed evidence only; no optional historical "
    "session recipes. Preserve/report/yield actual new denial/signinghang/uncertainownership. "
    "All original source/baseline/link/reading/twofamily/native/currentmain-normalmerge/"
    "changedteachingreview/combinedchecks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIPentryhash/original18000entries/42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/ownerissue gates remain. No runtimepublication/092/newrunner. "
    "Published117/1228,1111remaining; physicalphone/generalrelease/whole-set outstanding."
)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    verified = 0
    for kind, section in manifest.items():
        if isinstance(section, dict):
            for path, expected in section.items():
                if isinstance(expected, str) and len(expected) == 64:
                    file = R.joinpath(*path.split("/"))
                    actual = sha(file) if kind in {
                        "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                    } else sha256(file)
                    assert actual == expected, path
                    verified += 1
    assert verified == 8432 and manifest["contentVersion"] == "bfe65483a821fc13"
    assert not git("diff", review.HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    return {"runtimeHashesVerified": verified, "manifestFresh": True,
            "contentVersion": manifest["contentVersion"], "manifestSha256": sha(R / "manifest.json"),
            "runtimeUnchangedFromSignedCorrection": True}


def archive():
    review.frozen()
    verification = runtime()
    records = [load(C / f"batch-091-mnemonic-653-{label}-execution.json") for label in ["claude", "gpt"]]
    assert records[0]["completedAt"] < records[1]["startedAt"]
    for record in records:
        assert record["acceptedExecution"] and record["exitCode"] == 0
        assert not record["observedToolOverlaps"] and not record["unfinishedTools"]
        assert len(record["toolCalls"]) == 6 and len(record["actualDecodedImageReturns"]) == 3
        assert record["successfullyReturnedResources"] == record["requiredResources"]
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       check=True, capture_output=True)
    receipts = []
    sources = [Path(__file__), C / "confirm-batch-091-mnemonic-653.py",
               C / "post-batch-091-mnemonic-653.ps1"]
    sources += [C / f"batch-091-mnemonic-cli-{kind}-653.txt" for kind in ["help", "config"]]
    for label, record in zip(["claude", "gpt"], records):
        prefix = C / f"batch-091-mnemonic-653-{label}"
        raw = prefix.with_suffix(".jsonl")
        assert sha(raw) == record["rawSha256"]
        assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
        target = V / (raw.name + ".gz")
        assert not target.exists()
        with target.open("wb") as file:
            with gzip.GzipFile(filename="", mode="wb", fileobj=file, mtime=0) as archive_file:
                archive_file.write(raw.read_bytes())
        assert gzip.decompress(target.read_bytes()) == raw.read_bytes()
        receipts.append({"source": str(raw), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(raw), "archiveSha256": sha(target), "losslessGzip": True})
        sources += [prefix.with_suffix(s) for s in [".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"]]
        sources.append(C / (prefix.name + "-execution.json"))
    for source in sources:
        target = V / source.name
        assert not target.exists()
        shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(target)})
    evidence = {
        "schemaVersion": 1, "execution": 653, "batch": "091", "status": STAGE,
        "reviewedSnapshot": review.HEAD, "dependentOriginalSessionConfirmations": records,
        "newBlindInitialReviewCredit": False, "originalReportsAndProcessViolationsPreserved": True,
        "reconciliation": [{
            "id": "V1", "severity": "minor", "facet": "rendered comprehensibility",
            "file": "kanji/\u5203.md:24", "status": "resolved",
            "claim": "Previous unqualified dot-shape description mismatched detached default Gothic shortmark.",
            "remedy": "Existing signed correction describes extra shortmark, some font renderings separate, pinned diagram crossing longer sloping stroke.",
            "evidence": "Both complete original-session reports confirm accuracy against all three freshly viewed original PNGs and exact diff; no regression established.",
            "disagreement": "GPT's earlier CLEAN verdict remains unchanged; it does not retroactively claim discovery or agreement with the original finding. Coordinator accepted concern on evidence, not votes.",
            "processDisposition": "Claude651's14overlaps remain rejected; new six-call Claude653 execution complies, without retroactive repair or fresh blind initial credit.",
            "nativeRevisedVersionDisposition": "Unperformed; old captures support shape comparison, not revised paragraph layout/import.",
            "confidence": "High descriptive accuracy for pictured forms; no claim about every font/device.",
        }],
        "optional": [
            "Claude: detached rather than separate is more precise about spatial separation; direction and replacing here with app's diagram are optional, not established defects.",
            "All original textual/visual optional suggestions and nonactionable hypotheses preserved in complete original reports, not silently closed.",
        ],
        "validation": verification, "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "limits": [
            "Both dependent correction confirmations, not new blind initial reviews or native-speaker certification.",
            "Six complete serial returns per reviewer; payload audits establish delivery/process, not comprehension. PNG returns resized by view, not original-size native viewing.",
            "Current bfe65483a821fc13 not natively imported/rendered; old native650 archivef6b2ee39/versioncb3c857f3614485d retains only its exact original acceptance scope.",
            "API35 emulator/test-onlyAndroid1c1b7bf4 retaining productionf9b59a2, unidentified fallbackface, recycled Paintprobes, injectedtrace/no successful MLKit, no phone evidence remain.",
            "Current-main integration, combined checks, CI, public ZIP, publication, physical-phone/general-release and whole-set gates remain outstanding.",
        ],
        "nextAction": NEXT,
    }
    save(V / "batch-091-mnemonic-reconciliation-653.json", evidence)
    save(R / "docs" / "n1-sources" / "execution-653.json", {
        "schemaVersion": 1, "execution": 653, "batch": "091", "status": STAGE,
        "startingState": load(C / "progress.json")["execution653StartingState"],
        "reviewRecord": "docs/n1-reviews/batch-091-mnemonic-reconciliation-653.json",
        "receipts": receipts, "runtime": verification, "twoFamilyCorrectionConfirmation": "complete",
        "independentReviewerProcessesLaunched": 2, "serialProcessAndToolsVerified": True,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": "7100a3873282b54515b9ef130766e77cf151a47b",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Both complete serial correction confirmations archived; V1 resolved, runtime untouched.")


def finalize():
    review.prior.L = L
    review.prior.ownership()
    assert git("rev-parse", "HEAD^") == review.HEAD
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == review.prior.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G" and not git("status", "--porcelain", repo=A)
    verification = runtime()
    for item in load(R / "docs" / "n1-sources" / "execution-653.json")["receipts"]:
        file = R.joinpath(*item["archive"].split("/"))
        assert sha(file) == item["archiveSha256"]
        if item.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(file.read_bytes())).hexdigest() == item["sourceSha256"]
    prefix = C / "batch-091-mnemonic-653-issue-"
    body = Path(str(prefix) + "body.txt").read_text(encoding="utf-8-sig")
    receipt = load(Path(str(prefix) + "receipt.json"))
    posted = load(Path(str(prefix) + "posted.json"))
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = load(C / "progress.json"), load(L / "progress-before-653.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert state["checkpoint"] == 652
    assert all(state[key] == value for key, value in before.items() if key not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 653, "checkpoint": 653, "batch": "091",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-653.json",
        "reviewRecord": "docs/n1-reviews/batch-091-mnemonic-reconciliation-653.json",
        "twoFamilyCorrectionConfirmation": "complete", "V1": "resolved",
        "originalClaudePid": 18224, "originalGptPid": 30260,
        "bothReviewerProcessesExited": True, "serialViewCallsPerReviewer": 6,
        "decodedOriginalPngsPerReviewer": 3, "observedToolOverlaps": 0,
        "priorClaudeToolOverlapViolationPreserved": True,
        **verification, "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": "7100a3873282b54515b9ef130766e77cf151a47b",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    state.update(checkpoint=653, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution653CoordinatorCheckpoint"] = checkpoint
    state["batch091MnemonicConfirmationCheckpoint"] = checkpoint
    state["execution653StartingState"]["status"] = "signed-local-two-family-confirmation-checkpoint-complete"
    save(C / "progress.json", state)
    reread = load(C / "progress.json")
    assert all(reread[key] == value for key, value in before.items() if key not in allowed)
    save(L / "checkpoint-653.json", checkpoint)
    print("Persisted checkpoint653; original historical values preserved:", len(before))
    print(checkpoint["savedCommit"], receipt["html_url"])


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
