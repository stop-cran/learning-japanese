import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("visual633", C / "review-batch-089-visual-633.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, N, L = review.R, review.A, review.V, review.N, review.L
HEAD, ANDROID, TEACHING = review.HEAD, review.ANDROID, review.TEACHING
load, save, sha, git = review.load, review.save, review.sha, review.git
NEXT = (
    "SAME089 bounded current-main integration and actual combined-tree acceptance next; no090. "
    "Read docs/n1-sources/execution-633.json and docs/n1-reviews/batch-089-visual-reconciliation-633.json. "
    "Original Claudea56b5dcb and GPT3286add7 dependent visual confirmations CLOSED on unchanged "
    "teaching4b84608b/evidencecc8e9041. Actual claude-opus-5.5 then gpt-6.1-sol; "
    "each13strictlyserialviewcalls/11decodedPNGs (8mappedcontact sheets/all43captures plus3fontpanels), "
    "exit0/nooverlap/eachprocessactuallyexited before next; no newblindinitialcredit. "
    "Bothnewarticles plus ONLYchanged作navigationline renderedCLEAN with inheritedtextualcorrectness/"
    "coverage; noactionabledefect. Original GPT redundant/truncatedtail read limits remain. "
    "Actualtoolresized sheets1500x2260->1327x2000 andfontpanels1080x2400->900x2000; returnedhashesagree "
    "acrossreviewers, notsourcebyteidentity or96PaintPNGs/fallbackface. All23Han/fourComposefonts "
    "including乂U+4E42/凵U+51F5 distinguishable. Agriculturalnoun/verypooryield notharvestverb/"
    "necessaryzeroyield/famine/badwork; compound-specific作crop/yield. "
    "PicturedN1/suppliedAllproduction choices illfortune;evil versus凡commonplace;mediocre/"
    "凸convex;protruding/凹concave;sunken all3available/zerofallback; notfuturecustompool/oldclient. "
    "SingleonきょうGood/done, rawkun[]/explicitquizkun[]/FullLiteagreement. "
    "Inherited632native BOTHterminalcase0/noskips, fullarchive72614eda productionContentSyncONCE/"
    "1112kanji5068words121N1zeroProblems/versionc6562f11cb371053/epoch1; fourstrokeinjectedtrace/"
    "recallgiveup/botharticles/2mappedpairs4directions/1directguard/SystemBack/offline. "
    "No freshnative633/humanhandwriting/offlineMLKit/phone claim; qualifiedTESTONLYAndroid1c1b7bf4 "
    "retains productionf9b59a2, NOTlatestappmain. Recheck freshmain/exactsignedheads/whollycleanworktrees/"
    "source-membership/fullbaseline-preservation/links/readings/guards/stroke-fontdispositions; normal "
    "nonrewriting originmainmerge, regenerate derivedmanifest ifchanged, independently rereview "
    "substantiveteachingchanges. Required fullPython/vocabularyconsistency/manifestfreshness/budget/"
    "audits/applicablenonskippedAndroid onactualcombinedtree before normallysignedreviewclosedacceptance. "
    "Then normalownerfastforward/terminalgreenCI/EVERYimmutablepublicZIP runtimeentryhash/original"
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/ownerissue gates. "
    "No publication until prerequisites pass; no090/forcepush/amend/guardheapincrease/productionappchange. "
    "Parent19008 ownsrunner.lock: verify liveancestry/currentrunnersession/checkpoint/signedheads/"
    "cleanstate; NOchildreacquire/delete/unlock. Approvedcontrol/committedsources only, notoptional"
    "historicalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Published115/1228,1113remaining unchanged; physicalphone/generalrelease/whole-setoutstanding; "
    "projectincomplete."
)


def verify_runtime():
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
    assert len(verified) == 8426
    assert manifest["contentVersion"] == "c6562f11cb371053"
    assert not git("diff", TEACHING, "HEAD", "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")
    return {"runtimeHashesVerified": len(verified), "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json")}


def archive():
    review.frozen()
    target = V / "batch-089-visual-reconciliation-633.json"
    assert not target.exists()
    records = {label: load(C / f"batch-089-visual-633-{label}-execution.json")
               for label in review.SESSIONS}
    for label, record in records.items():
        prefix = C / f"batch-089-visual-633-{label}"
        model = review.SESSIONS[label][0]
        assert record["actualModels"] == [model] and record["usageCurrentModel"] == model
        assert record["exitCode"] == 0 and not record["unfinishedTools"]
        assert record["allAssignedResourcesSuccessfullyReturned"] and not record["observedToolOverlaps"]
        assert len(record["toolCalls"]) == 13
        assert len(record["actualDecodedImageReturns"]) == 11
        assert sha(prefix.with_suffix(".jsonl")) == record["rawSha256"]
        assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       check=True, capture_output=True)
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    assert all(a["returnedSha256"] == b["returnedSha256"] for a, b in zip(
        records["claude"]["actualDecodedImageReturns"], records["gpt"]["actualDecodedImageReturns"]))
    runtime = verify_runtime()
    for receipt in load(R / "docs" / "n1-sources" / "execution-632.json")["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    receipts = []
    sources = [Path(__file__), C / "review-batch-089-visual-633.py", review.PACKET,
               C / "batch-089-visual-633-inputs.json", C / "post-batch-089-visual-633.ps1",
               C / "batch-089-visual-cli-help-633.txt", C / "batch-089-visual-cli-config-633.txt"]
    for label in review.SESSIONS:
        prefix = C / f"batch-089-visual-633-{label}"
        sources.extend(prefix.with_suffix(suffix) for suffix in [
            ".md", ".prompt.txt", ".stderr.txt", ".usage.json"])
        sources.append(C / (prefix.name + "-execution.json"))
        raw = prefix.with_suffix(".jsonl")
        archived = V / (raw.name + ".gz")
        assert not archived.exists()
        archived.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archived.read_bytes()) == raw.read_bytes()
        receipts.append({"source": str(raw), "archive": archived.relative_to(R).as_posix(),
                         "sourceSha256": sha(raw), "archiveSha256": sha(archived), "losslessGzip": True})
    for source in sources:
        archived = V / source.name
        assert not archived.exists()
        shutil.copyfile(source, archived)
        receipts.append({"source": str(source), "archive": archived.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(archived)})
    reconciliation = {
        "schemaVersion": 1, "execution": 633, "batch": "089",
        "evidenceSnapshot": HEAD, "teachingSnapshot": TEACHING,
        "status": "dependent-visual-review-closed-awaiting-combined-acceptance",
        "teachingChanged": False, "originalInitialReviewsPreserved": True,
        "newBlindInitialReviewCredit": False, "processes": records,
        "serialReviewerProcessesExited": True, "allToolViewsSerial": True,
        "eachOriginalReportPreservedBeforeNextLaunch": True,
        "eachReviewerImagesDecoded": 11, "allAssignedResourcesReturned": True,
        "sameActualReturnedImageHashesAcrossReviewers": True,
        "verdicts": {path: {"correctness": "CLEAN-inherited-textual",
                            "scopedCoverage": "CLEAN-inherited-textual",
                            "renderedComprehensibility": "CLEAN"}
                     for path in ["kanji/\u51f6.md", "words/\u51f6\u4f5c.md",
                                  "kanji/\u4f5c.md:44 changed navigation line only"]},
        "findings": [],
        "dispositions": [
            {"claim": "Initial font/article/session rendering unavailable",
             "status": "resolved", "scope": "bounded supplied API35 captures only",
             "evidence": "Both original models decoded11PNGs each:8mapped sheets/all43captures plus3separatefontpanels. All23Han/fourfonts, especially乂/凵/凶/凡/凸/凹, distinguishable; bothcomplete newarticles andonlychanged作navigationline readable.",
             "limits": "Tool resized sheets1500x2260to1327x2000/panels1080x2400to900x2000. Not96viewedPaintPNGs or identifiedfallbackface/physicalphone."},
            {"claim": "Possible overlapping evil choices in N1/All fallback",
             "status": "resolved", "scope": "two tested production configurations only",
             "evidence": "PicturedN1 options and suppliedN1/All production receipts show exactly凶/凡/凸/凹, all3curatedavailable/zerofallback.",
             "limits": "No separately picturedAll question or everyfuturecustompool/oldclient certification; original Claude widerpool hypothesis retained as out-of-tested-scope."},
            {"claim": "Native import/key persistence/navigation/Back/offline",
             "status": "resolved", "scope": "supplied native632 receipts",
             "evidence": "Both distinguish pictured routes/questions from supplied passing instrumentation. Fullarchive72614eda ContentSyncONCE/1112kanji5068words121N1zeroProblems/versionc6562f11cb371053/epoch1; both terminalcases0/noskips; 2pairs4directions/1guard.",
             "limits": "Not reviewer-executed tests or fresh633native; injectedtrace/giveup not humanhandwriting/offlineMLKit/phone."},
            {"claim": "Original strongerword/crop-sense/crimeweapon optional additions",
             "status": "optional", "decision": "No edit. Original textual reconciliation629 preserves the source-backed teaching boundaries and optional status; no unsupported universal strength ordering introduced."},
            {"claim": "Fallback weight differences and no kana in word title bar",
             "status": "optional", "decision": "No content/app edit. Correct distinguishable glyphs and kana in body/linked reading row; no cosmetic uniformity requirement or established learner-visible content defect."},
            {"claim": "Scrollable table clips at initial horizontal position",
             "status": "optional", "decision": "No edit. Explicit scrolling instruction and complementary captures expose full linkedreading row; static clipping alone not missing content."},
        ],
        "modelContributionComparison": {
            "sharedVerifiedDefects": [], "claudeUniqueVerifiedDefect": None,
            "gptUniqueVerifiedDefect": None,
            "sharedObservations": "Both no actionable defect; bounded glyph/article/session comprehensibility and testedN1/All choice disposition. Claude optionalfontweight/header remarks not verified defects or generalbenchmark.",
            "limits": "Matched dependentvisual sample; inherited initialtext conclusions; notnewblindreview ormodelranking.",
        },
        "runtime": runtime, "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "limits": [
            "Original GPT redundant overlapping serialtailreads/two truncatedtailresponses remain historical; fresh visualfollowup does not erase them.",
            "No new independent upstream/Git/signature verification by reviewers; coordinator verifies hashes and supplied receipts.",
            "No fresh633Android/native, phone, fallbackface identification, humanhandwriting/offlineMLKit/native-speaker/learningeffectiveness certification.",
            "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2; not latestappmain.",
            "Currentmain/combinedacceptance/normal signing/publication/terminalCI/everyimmutablepublicZIPhash/phone/generalrelease/whole-set remain later gates.",
        ],
        "nextAction": NEXT,
    }
    save(target, reconciliation)
    save(R / "docs" / "n1-sources" / "execution-633.json", {
        "schemaVersion": 1, "execution": 633, "batch": "089",
        "startingState": load(C / "progress.json")["execution633StartingState"],
        "snapshot": HEAD, "teachingSnapshot": TEACHING, "status": reconciliation["status"],
        "runtime": runtime, "reconciliation": target.relative_to(R).as_posix(), "receipts": receipts,
        "runtimeChanged": False, "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 115, "remainingAdditions": 1113,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Archived both complete reports, lossless raw events and audited image/process evidence.")


def finalize():
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    runtime = verify_runtime()
    for receipt in load(R / "docs" / "n1-sources" / "execution-633.json")["receipts"]:
        archived = R.joinpath(*receipt["archive"].split("/"))
        assert sha(archived) == receipt["archiveSha256"]
        if receipt.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(archived.read_bytes())).hexdigest() == receipt["sourceSha256"]
    body = (C / "batch-089-visual-633-issue-body.txt").read_bytes().decode("utf-8-sig")
    posted, receipt = [load(C / f"batch-089-visual-633-issue-{name}.json")
                       for name in ["posted", "receipt"]]
    assert posted["id"] == receipt["id"]
    assert posted["body"] == receipt["body"] == body
    assert posted["user"]["login"] == receipt["user"]["login"] == "stop-cran"
    state, before = load(C / "progress.json"), load(L / "progress-before-633.json")
    assert state["checkpoint"] == 632 and state["stage"] == "batch-089-dependent-visual-confirmations"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 633, "checkpoint": 633, "batch": "089",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "visual-review-closed-awaiting-combined-acceptance",
        "evidence": "docs/n1-sources/execution-633.json",
        "reconciliation": "docs/n1-reviews/batch-089-visual-reconciliation-633.json",
        "runtime": runtime, "independentVisualConfirmationsComplete": True,
        "originalSessionsReused": {label: session for label, (_, session) in review.SESSIONS.items()},
        "actualModels": [model for model, _ in review.SESSIONS.values()],
        "eachReviewerPngsDecoded": 11, "eachReviewerViewCalls": 13,
        "allToolViewsSerial": True, "serialReviewerProcessesExited": True,
        "actionableFindings": [], "runtimeChanged": False,
        "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "publishedAdditions": 115, "remainingAdditions": 1113,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueBodySha256": hashlib.sha256(body.encode()).hexdigest(),
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update({"checkpoint": 633, "status": "continue", "stage": checkpoint["stage"],
                  "nextAction": NEXT, "blocker": None})
    state["execution633CoordinatorCheckpoint"] = checkpoint
    temporary = C / "progress-execution-633.tmp"
    save(temporary, state)
    temporary.replace(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert load(C / "progress.json")[key] == value, key
    save(L / "checkpoint-final-633.json", checkpoint)
    print(json.dumps({key: checkpoint[key] for key in [
        "checkpoint", "status", "stage", "savedCommit", "runtime",
        "ownerAuthorAndBodyVerified", "allOriginalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
