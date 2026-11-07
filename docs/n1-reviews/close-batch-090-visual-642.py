import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("visual642", C / "review-batch-090-visual-642.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, L = review.R, review.A, review.V, review.L
HEAD, ANDROID, TEACHING = review.HEAD, review.ANDROID, review.TEACHING
load, save, sha, git = review.load, review.save, review.sha, review.git
NEXT = (
    "SAME090 bounded current-main integration and actual combined-tree acceptance next; no091. "
    "Read docs/n1-sources/execution-642.json and docs/n1-reviews/batch-090-visual-reconciliation-642.json. "
    "Original Claude63fa1d59 and GPTf0995652 dependent visual confirmations CLOSED on unchanged "
    "teachinge044e953/evidence8308d49f. Actual claude-opus-5.5 then gpt-6.1-sol; "
    "each16strictlyserialviewcalls/14decodedPNGs (11mappedcontact sheets/all64captures plus3fontpanels), "
    "exit0/nooverlap/eachprocessactuallyexited before next; no newblindinitialcredit. "
    "Bothnewarticles plus ONLYfourchangedreusedpassages renderedCLEAN with inheritedtextualcorrectness/"
    "coverage; noactionabledefect. Claude explicitly used compacted same-session notes for first4sheets; "
    "preserve original read/provenance limits and complete original reports, not equal fresh-read claim. "
    "Actualtoolresized sheets1500x2260->1327x2000 andfontpanels1080x2400->900x2000; returnedhashesagree "
    "acrossreviewers, notsourcebyteidentity or76PaintPNGs/fallbackface. All18Han/fourComposefonts "
    "including inward-starting刀 versus crossing力 and乃/凹/凸 distinguishable. "
    "Rawトウ/かたな/そり retained in sourceorder; onlyトウ/かたな selected with own linkedrows; "
    "sourceonlyそり not inferred fromjukujikun剃刀. TraditionalJapaneseSwordnoun,neutralmuseum/"
    "photosentences,lexical日本modifier+sword,bothにほんとう/にっぽんとう withoutfrequencyranking/"
    "universalsoundchange/shape rule. PicturedN1/suppliedAll choices sword;blade versus乃thereupon;"
    "possessiveno/凹concave;sunken/凸convex;protruding all3available/zerofallback; notfuturecustompools/"
    "oldclients. Exactly onとう/kunかたな Good/2of2done;FullLiteagreement supplied. "
    "Inherited641native BOTHterminalcase0/noskips, fullarchive40bc5a55 productionContentSyncONCE/"
    "1113kanji5069words122N1zeroProblems/versionceee0f79a6d394df/epoch1; twostrokeinjectedtrace/"
    "recallgiveup/botharticles/5mappedpairs10directions/1direct日本刀-刀guard/SystemBack/offline. "
    "Existing刀N3/剃刀N2/鋭いguard preserved. No freshnative642/humanhandwriting/offlineMLKit/phone "
    "claim; qualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. "
    "First641wrapper escapingfailure beforedevicelaunch remains historical, notdenial/lockrecovery. "
    "Recheck freshmain/exactsignedheads/whollycleanworktrees/source-membership/fullbaseline-preservation/"
    "links/readings/guards/stroke-fontdispositions; normal nonrewriting originmainmerge, regenerate "
    "derivedmanifest ifchanged, independently rereview substantiveteachingchanges. Required fullPython/"
    "vocabularyconsistency/manifestfreshness/budget/audits/applicablenonskippedAndroid onactualcombinedtree "
    "before normallysignedreviewclosedacceptance. Then normalownerfastforward/terminalgreenCI/"
    "EVERYimmutablepublicZIP runtimeentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/ownerissue gates. No publication until prerequisites pass; no091/forcepush/"
    "amend/guardheapincrease/productionappchange. Parent19008 ownsrunner.lock: verify liveancestry/"
    "currentrunnersession/decodedlauncher/checkpoint/signedheads/cleanstate; NOchildreacquire/delete/"
    "unlock. Approvedcontrol/committedsources only, notoptionalhistoricalsessionrecipes. Preserve/report/"
    "yield actualnewdenial/signinghang/uncertainownership. Published116/1228,1112remaining unchanged; "
    "physicalphone/generalrelease/whole-setoutstanding; projectincomplete."
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
    assert len(verified) == 8429
    assert manifest["contentVersion"] == "ceee0f79a6d394df"
    assert not git("diff", TEACHING, "HEAD", "--",
                   "kanji", "words", "articles", "strokes", "manifest.json")
    return {"runtimeHashesVerified": len(verified), "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json")}


def archive():
    review.frozen()
    target = V / "batch-090-visual-reconciliation-642.json"
    assert not target.exists()
    records = {label: load(C / f"batch-090-visual-642-{label}-execution.json")
               for label in review.SESSIONS}
    for label, record in records.items():
        prefix = C / f"batch-090-visual-642-{label}"
        model = review.SESSIONS[label][0]
        assert record["actualModels"] == [model] and record["usageCurrentModel"] == model
        assert record["exitCode"] == 0 and not record["unfinishedTools"]
        assert record["allAssignedResourcesSuccessfullyReturned"] and not record["observedToolOverlaps"]
        assert len(record["toolCalls"]) == 16 and len(record["actualDecodedImageReturns"]) == 14
        assert sha(prefix.with_suffix(".jsonl")) == record["rawSha256"]
        assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                       check=True, capture_output=True)
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    assert all(a["returnedSha256"] == b["returnedSha256"] for a, b in zip(
        records["claude"]["actualDecodedImageReturns"], records["gpt"]["actualDecodedImageReturns"]))
    runtime = verify_runtime()
    for receipt in load(R / "docs" / "n1-sources" / "execution-641.json")["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    receipts = []
    sources = [Path(__file__), C / "review-batch-090-visual-642.py", review.PACKET,
               C / "batch-090-visual-642-inputs.json", C / "post-batch-090-visual-642.ps1",
               C / "batch-090-visual-cli-help-642.txt", C / "batch-090-visual-cli-config-642.txt"]
    sources.append(C / "review-batch-089-visual-633.py")
    for label in review.SESSIONS:
        prefix = C / f"batch-090-visual-642-{label}"
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
        name = "batch-090-visual-642-base-recipe.py" if source.name == "review-batch-089-visual-633.py" else source.name
        archived = V / name
        assert not archived.exists()
        shutil.copyfile(source, archived)
        receipts.append({"source": str(source), "archive": archived.relative_to(R).as_posix(),
                         "sourceSha256": sha(source), "archiveSha256": sha(archived)})
    reconciliation = {
        "schemaVersion": 1, "execution": 642, "batch": "090",
        "evidenceSnapshot": HEAD, "teachingSnapshot": TEACHING,
        "status": "dependent-visual-review-closed-awaiting-combined-acceptance",
        "teachingChanged": False, "originalInitialReviewsPreserved": True,
        "newBlindInitialReviewCredit": False, "processes": records,
        "serialReviewerProcessesExited": True, "allToolViewsSerial": True,
        "eachOriginalReportPreservedBeforeNextLaunch": True,
        "eachReviewerImagesDecoded": 14, "allAssignedResourcesReturned": True,
        "sameActualReturnedImageHashesAcrossReviewers": True,
        "verdicts": {path: {"correctness": "CLEAN-inherited-textual",
                            "scopedCoverage": "CLEAN-inherited-textual",
                            "renderedComprehensibility": "CLEAN"}
                     for path in ["kanji/\u5200.md", "words/\u65e5\u672c\u5200.md",
                                  "words/\u5200.md:24 only", "words/\u5243\u5200.md:25 only",
                                  "kanji/\u65e5.md:48 only", "kanji/\u672c.md:37 only"]},
        "findings": [],
        "dispositions": [
            {"claim": "Initial font/article/session rendering unavailable",
             "status": "resolved", "scope": "bounded supplied API35 captures only",
             "evidence": "Both originals decoded14PNGs each:11mapped sheets/all64captures plus3fontpanels. All18Han/fourfonts, especially inward-starting刀 versus crossing力 and乃/凹/凸, distinguishable; bothcomplete newarticles andonlyfourchangedpassages readable.",
             "limits": "Claude used same-session compacted notes for first4sheets. Tool resized sheets1500x2260to1327x2000/panels1080x2400to900x2000. Not76viewedPaintPNGs or identifiedfallbackface/physicalphone."},
            {"claim": "Possible sword/blade fallback overlap in N1/All",
             "status": "resolved", "scope": "two tested production configurations only",
             "evidence": "PicturedN1 and suppliedN1/All receipts show exactly刀/乃/凹/凸, all3curatedavailable/zerofallback.",
             "limits": "No separately picturedAll question or everyfuturecustompool/oldclient certification. Claude repeats widerpool hypothesis; that out-of-tested-scope limit remains, not a consequential unresolved scoped teaching claim."},
            {"claim": "Native import/key persistence/navigation/Back/offline",
             "status": "resolved", "scope": "supplied native641 receipts",
             "evidence": "Both distinguish pictured routes/questions from supplied passing instrumentation. Fullarchive40bc5a55 ContentSyncONCE/1113kanji5069words122N1zeroProblems/versionceee0f79a6d394df/epoch1; both terminalcases0/noskips; 5pairs10directions/1directguard. Exactly onとう/kunかたな Good/2of2done; rawそり reference not an offeredquizkey.",
             "limits": "Not reviewer-executed tests or fresh642native; injectedtrace/giveup not humanhandwriting/offlineMLKit/phone."},
            {"claim": "Claude original four optional expansions",
             "status": "optional", "decision": "No edit. Harmonized力wording,刀money sense, historicalorigin andextraトウcompounds remain nonblocking; textual638 reconciliation preserved."},
            {"claim": "Kana wrapping in rendered prose",
             "status": "optional", "reportedBy": "Claude visual follow-up",
             "decision": "No edit. Ordinary line wrapping remains legible; no demonstrated learning defect or justification for new nonbreaking/layout mechanism."},
            {"claim": "Possible shared fallbackface or font-weight similarity",
             "status": "unresolved", "category": "outside-scoped-acceptance",
             "decision": "No inferred fallbackidentity. Actual face not identified; distinct recognizableglyphs meet bounded font requirement, cosmeticuniformity not required."},
            {"claim": "Scrollable reading table clipped at initial position",
             "status": "optional", "decision": "No edit. Explicit scrolling instruction and complementary captures expose full linkedreading rows; static clipping alone not missing content."},
        ],
        "modelContributionComparison": {
            "sharedVerifiedDefects": [], "claudeUniqueVerifiedDefect": None,
            "gptUniqueVerifiedDefect": None,
            "sharedObservations": "Both no actionable defect; bounded glyph/article/session comprehensibility and testedN1/All choice disposition. Claude optionalkana wrapping/fallbackface speculation are not verified defects or generalbenchmark.",
            "limits": "Matched dependentvisual sample; inherited initialtext conclusions; notnewblindreview/equalfreshreaddepth/modelranking. Claude compacted notes explicitly retained.",
        },
        "runtime": runtime, "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "limits": [
            "Original textual reports/provenance/read limitations remain. Claude original familycount not independently confirmed; packetdelivery audits establish bytes, not comprehension. Claude visual report explicitly relies on same-session compacted notes for first4sheets.",
            "No new independent upstream/Git/signature verification by reviewers; coordinator verifies hashes and supplied receipts.",
            "No fresh642Android/native, phone, fallbackface identification, humanhandwriting/offlineMLKit/native-speaker/learningeffectiveness certification.",
            "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2; not latestappmain.",
            "Currentmain/combinedacceptance/normal signing/publication/terminalCI/everyimmutablepublicZIPhash/phone/generalrelease/whole-set remain later gates.",
        ],
        "nextAction": NEXT,
    }
    save(target, reconciliation)
    save(R / "docs" / "n1-sources" / "execution-642.json", {
        "schemaVersion": 1, "execution": 642, "batch": "090",
        "startingState": load(C / "progress.json")["execution642StartingState"],
        "snapshot": HEAD, "teachingSnapshot": TEACHING, "status": reconciliation["status"],
        "runtime": runtime, "reconciliation": target.relative_to(R).as_posix(), "receipts": receipts,
        "runtimeChanged": False, "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 116, "remainingAdditions": 1112,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Archived both complete reports, lossless raw events and audited image/process evidence.")


def finalize():
    review.ownership()
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    runtime = verify_runtime()
    for receipt in load(R / "docs" / "n1-sources" / "execution-642.json")["receipts"]:
        archived = R.joinpath(*receipt["archive"].split("/"))
        assert sha(archived) == receipt["archiveSha256"]
        if receipt.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(archived.read_bytes())).hexdigest() == receipt["sourceSha256"]
    body = (C / "batch-090-visual-642-issue-body.txt").read_bytes().decode("utf-8-sig")
    posted, receipt = [load(C / f"batch-090-visual-642-issue-{name}.json")
                       for name in ["posted", "receipt"]]
    assert posted["id"] == receipt["id"] and posted["body"] == receipt["body"] == body
    assert posted["user"]["login"] == receipt["user"]["login"] == "stop-cran"
    state, before = load(C / "progress.json"), load(L / "progress-before-642.json")
    assert state["checkpoint"] == 641 and state["stage"] == "batch-090-dependent-visual-confirmations"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 642, "checkpoint": 642, "batch": "090",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "visual-review-closed-awaiting-combined-acceptance",
        "evidence": "docs/n1-sources/execution-642.json",
        "reconciliation": "docs/n1-reviews/batch-090-visual-reconciliation-642.json",
        "runtime": runtime, "independentVisualConfirmationsComplete": True,
        "originalSessionsReused": {label: session for label, (_, session) in review.SESSIONS.items()},
        "actualModels": [model for model, _ in review.SESSIONS.values()],
        "eachReviewerPngsDecoded": 14, "eachReviewerViewCalls": 16,
        "allToolViewsSerial": True, "serialReviewerProcessesExited": True,
        "actionableFindings": [], "runtimeChanged": False,
        "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "publishedAdditions": 116, "remainingAdditions": 1112,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueBodySha256": hashlib.sha256(body.encode()).hexdigest(),
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    state.update({"checkpoint": 642, "status": "continue", "stage": checkpoint["stage"],
                  "nextAction": NEXT, "blocker": None})
    state["execution642CoordinatorCheckpoint"] = checkpoint
    temporary = C / "progress-execution-642.tmp"
    save(temporary, state)
    temporary.replace(C / "progress.json")
    after = load(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert after[key] == value, key
    save(L / "checkpoint-final-642.json", checkpoint)
    print(json.dumps({key: checkpoint[key] for key in [
        "checkpoint", "status", "stage", "savedCommit", "runtime",
        "ownerAuthorAndBodyVerified", "allOriginalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
