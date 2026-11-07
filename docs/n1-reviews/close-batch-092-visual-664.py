import copy
import gzip
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual664", C / "review-batch-092-visual-664.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, L = review.R, review.A, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
STAGE = "dependent-visual-review-closed-awaiting-combined-acceptance"
NEXT = (
    "SAME092 bounded fresh-current-main integration and actual combined-tree acceptance next; no093. "
    "Read docs/n1-sources/execution-664.json and docs/n1-reviews/batch-092-visual-reconciliation-664.json. "
    "Original Claude2f27854e and GPT4ff2dfd7 dependent visual confirmations CLOSED on unchanged "
    "teaching6246dc62/evidence09c9cfde. Actualclaude-opus-5.5 then gpt-6.1-sol; "
    "each27strictlyserialviewcalls/25decodedoriginalPNGviews/22distinctsourceimages, "
    "exit0/nooverlap/allassignedtextreturned/processactuallyexitedbeforenext. "
    "No newblindinitialcredit, independentupstreamclaim or equalcomprehensionclaim. "
    "Eachcompletekanji刈/reusedN3刈る CLEAN inheritedcorrectness/coverage and boundedrendered"
    "comprehensibility; noactionablefinding. Completeoriginalreports/optionalpolish/readlimits retained. "
    "25of42originalPNGsviewed/17notseparatelyviewed; actualtoolresized1080x2400to900x2000. "
    "All16scopedHan/THREEComposepanels/FOURproductionfonts readable, especiallyfallbackU+5202刂 "
    "and刈/切/刀/乃/凹/凸 distinction/whole刈除. 64individual+4wholewordPaintprobes NOT68viewedPNGs "
    "or identifiedfallbackface. Complementaryhorizontalscrolledreadingtable readable; "
    "wordbodyheadingnotseparatelypictured remainsClaudeexplicitlimit, notmissingteaching. "
    "Rawonガイ,カイ then kunか.る sourceorder kept; ONLYkunかるoffered/persistedGood/1of1Done/"
    "NOonkeys/fullLiteagreement. Both刈除がいじょ/かいじょ recognized/unselected, "
    "NOTsourceonly/obsolete/frequencyranking. ReusedN3刈る identity/reading/title/level/"
    "original切るguard preserved; componentlink/direct収穫guard only. ONEallmappedbaselinepair/"
    "TWOdirections/SystemBack/offline/N1selection/meaning/reading/drawing. "
    "PicturedN1/suppliedAll choices mow;reap versus乃thereupon;possessiveno/凹concave;sunken/"
    "凸convex;protruding all3available/zerofallback; NOTeverycustompool/oldclient. "
    "Inherited663native TWOterminalcase0/noskips/fullarchive62c6d3e2 productionContentSyncONCE/"
    "1115kanji5070words124N1zeroProblems/version8445a5717d080dcc/acceptedRoomreadingEpoch1. "
    "Fourpinnedstrokes/injectedtrace/recallgiveup NOThumanhandwriting/successfulMLKit/phone; "
    "actualUI explicitlymodelunavailable/shapeonly. QualifiedTESTONLYAndroid1c1b7bf4 retains "
    "productionf9b59a2, NOTlatestappmain. No fresh664Android/nativeclaim; owned663helpersstopped. "
    "Recheck freshmain/exactsignedheads/whollyclean/source-membership/fullbaselinepreservation/"
    "links/readings/guards/stroke-fontdispositions; normalnonrewritingoriginmainmerge, "
    "regeneratederivedmanifestifchanged, independentlyrereview substantiveteachingchanges. "
    "Required fullPython/vocabularyconsistency/manifestfreshness/budget/audits/applicablenonskipped"
    "Android on ACTUALcombinedtree before normallysignedreviewclosedacceptance. "
    "Then normalownerfastforward/terminalgreenCI/EVERYimmutablepublicZIP runtimeentryhash/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/ownerissue "
    "gates. No publicationuntilprerequisitespass; no093/forcepush/amend/guardheapincrease/"
    "productionappchange. Parent19008 retainsrunner.lock: verifyliveancestry/currentrunnersession/"
    "decodedlauncher/checkpoint/exactsignedheads/whollyclean; NOchildreacquire/delete/unlock. "
    "Approvedcontrol/committedsources only, NOToptionalhistoricalsessionrecipes. Preserve/report/"
    "yieldactualnewdenial/signinghang/uncertainownership. Published118/1228,1110remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    verified = {}
    for kind, section in manifest.items():
        if isinstance(section, dict):
            for name, expected in section.items():
                if isinstance(expected, str) and len(expected) == 64:
                    path = R.joinpath(*name.split("/"))
                    actual = sha(path) if kind in {
                        "images", "audio", "listeningTaskAudio", "listeningTaskImages"
                    } else sha256(path)
                    assert actual == expected, name
                    verified[name] = actual
    assert len(verified) == 8434
    assert manifest["contentVersion"] == "8445a5717d080dcc"
    assert not git("diff", review.TEACHING, "HEAD", "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {
        "runtimeHashesVerified": len(verified), "contentVersion": manifest["contentVersion"],
        "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True,
        "teachingAndAllRuntimeBytesUnchanged": True,
    }


def archive():
    review.frozen()
    target = V / "batch-092-visual-reconciliation-664.json"
    assert not target.exists()
    records = {label: load(C / f"batch-092-visual-664-{label}-execution.json")
               for label in review.SESSIONS}
    for label, record in records.items():
        prefix = C / f"batch-092-visual-664-{label}"
        model, session = review.SESSIONS[label]
        assert record["actualModels"] == [model] and record["usageCurrentModel"] == model
        assert record["sessionId"] == session and record["exitCode"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert record["allAssignedResourcesSuccessfullyReturned"]
        assert len(record["toolCalls"]) == 27 and all(
            item["name"] == "view" and item["success"] for item in record["toolCalls"])
        images = record["actualDecodedImageReturns"]
        assert len(images) == 25 and len({item["sourceSha256"] for item in images}) == 22
        assert {tuple(item["returnedDimensions"]) for item in images} == {(900, 2000)}
        assert sha(prefix.with_suffix(".jsonl")) == record["rawSha256"]
        assert sha(prefix.with_suffix(".md")) == record["reportSha256"]
        assert review.absent(record["launcherPid"])
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    assert all(a["returnedSha256"] == b["returnedSha256"] for a, b in zip(
        records["claude"]["actualDecodedImageReturns"], records["gpt"]["actualDecodedImageReturns"]))
    checked = runtime()
    receipts = []
    sources = [
        Path(__file__), C / "review-batch-092-visual-664.py", review.PACKET,
        C / "batch-092-visual-664-inputs.json", C / "post-batch-092-visual-664.ps1",
        C / "batch-092-visual-cli-help-664.txt", C / "batch-092-visual-cli-config-664.txt",
    ]
    for label in review.SESSIONS:
        prefix = C / f"batch-092-visual-664-{label}"
        sources.extend(prefix.with_suffix(suffix) for suffix in [
            ".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"])
        sources.append(C / (prefix.name + "-execution.json"))
        raw = prefix.with_suffix(".jsonl")
        archived = V / (raw.name + ".gz")
        assert not archived.exists()
        archived.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archived.read_bytes()) == raw.read_bytes()
        receipts.append({
            "source": str(raw), "archive": archived.relative_to(R).as_posix(),
            "sourceSha256": sha(raw), "archiveSha256": sha(archived), "losslessGzip": True,
        })
    for source in sources:
        archived = V / source.name
        assert not archived.exists()
        shutil.copyfile(source, archived)
        assert sha(source) == sha(archived)
        receipts.append({
            "source": str(source), "archive": archived.relative_to(R).as_posix(),
            "sourceSha256": sha(source), "archiveSha256": sha(archived),
        })
    inputs = load(C / "batch-092-visual-664-inputs.json")
    groups = {}
    for image in inputs["images"]:
        groups.setdefault(image["sha256"], []).append(image["path"])
    reconciliation = {
        "schemaVersion": 1, "execution": 664, "batch": "092", "status": STAGE,
        "evidenceSnapshot": review.HEAD, "teachingSnapshot": review.TEACHING,
        "teachingChanged": False, "originalInitialReviewsPreserved": True,
        "newBlindInitialReviewCredit": False, "processes": records,
        "serialReviewerProcessesExited": True, "allToolViewsSerial": True,
        "eachOriginalReportPreservedBeforeNextLaunch": True,
        "eachReviewerImagesDecoded": 25, "distinctSourceImageHashes": 22,
        "remainingUnassignedPngs": 17, "allAssignedResourcesReturned": True,
        "sameActualReturnedImageHashesAcrossReviewers": True,
        "exactDuplicateSourceGroups": [paths for paths in groups.values() if len(paths) > 1],
        "verdicts": {
            path: {"correctness": "CLEAN-inherited-textual",
                   "scopedCoverage": "CLEAN-inherited-textual",
                   "renderedComprehensibility": "CLEAN-bounded-emulator"}
            for path in ["kanji/\u5208.md", "words/\u5208\u308b.md"]
        },
        "findings": [],
        "actionableRemainingFindings": 0, "consequentialUnresolvedInScopeClaims": 0,
        "dispositions": [
            {
                "claim": "Initial font/article/session visual evidence unavailable",
                "status": "resolved", "scope": "assigned bounded API35 captures and supplied native663 receipts only",
                "evidence": "Both original reviewers decoded25PNGs each, including three Compose panels/all16Han/fourfonts and both article projections. U+5202 readable/distinguishable; no missing-glyph finding. Complementary reading-table views accepted.",
                "limits": "17of42captures not separately viewed. Wordbodyheading not separately pictured, as Claude expressly notes. Complete articles also assessed against supplied fulltext/native-scrollassertions. Not physical-phone or fallback-face identification.",
            },
            {
                "claim": "Production N1/All fallback choice uncertainty",
                "status": "resolved", "scope": "tested production default configurations only",
                "evidence": "Pictured N1 meaning question/feedback and supplied N1/All receipts: exactlymow;reap versus乃/凹/凸, allthreecuratedwrongcards/zerofallback.",
                "limits": "No separately picturedAll question or universal custom/random-pool/old-client certification.",
            },
            {
                "claim": "Offered key and native persistence/navigation/offline",
                "status": "resolved", "scope": "viewed questions/routes plus supplied native663 receipts",
                "evidence": "Onlykunかるquestion/correctfeedback/1of1Done; noonkeys/fullLiteagreement supplied. Fourstrokeinjectedtrace/practice/recallgiveup; reciprocalpair/twodirections/SystemBack/offline. Fullarchive ContentSyncONCE/two terminalcases0/no skips preserved in original663.",
                "limits": "Not reviewer-executed tests, fresh664native, humanhandwriting or successfulMLKitrecognition. Feedback explicitlymodelunavailable/shapeonly.",
            },
            {
                "claim": "Claude original optional hair translation, inflection kana and explicit収穫 contrast",
                "status": "optional", "decision": "No edit. Original textual660 dispositions retained; no actionable defect established. Hairtranslation alternative appears in GPT original supporting assessment as well, not unique Claude discovery.",
            },
            {
                "claim": "Font-weight variation and wrapping within がいじょ",
                "status": "optional", "reportedBy": "Claude visual follow-up",
                "decision": "No edit or app change. Both reviewers find glyphs/text readable; cosmetic uniformity and nonbreaking text are not acceptance requirements.",
            },
            {
                "claim": "Actual system fallback face and64individual+4wholewordPaint probes",
                "status": "unresolved", "category": "outside-scoped-acceptance",
                "decision": "Do not identify a face or claim68viewedPNG exports. Compose panels demonstrate bounded readable glyphs; retain explicit evidence limits.",
            },
            {
                "claim": "髪 link target and mow;reap title uniqueness not independently verified by Claude",
                "status": "resolved", "scope": "coordinator mechanical verification only",
                "decision": "Original660 coordinator resolution remains. Target exists and exactly one kanji has this title; do not relabel this as independent reviewer verification.",
            },
            {
                "claim": "Claude visual resemblance estimates for duplicate captures",
                "status": "optional", "category": "evidence-precision",
                "decision": "Preserve report verbatim; use exactDuplicateSourceGroups above, not subjective resemblance, for byte-identical duplicate accounting.25views correspond to22distinctsourcehashes.",
            },
        ],
        "modelContributionComparison": {
            "sharedVerifiedDefects": [], "claudeUniqueVerifiedDefect": None,
            "gptUniqueVerifiedDefect": None,
            "sharedObservations": "Both accept bounded glyph/article/session comprehensibility; no actionable defect. Same unchanged teaching, packet and25actualPNGviews.",
            "claudeUniqueObservations": "Nonblockingfontweight/kana-wrap observations and explicit unpictured wordbodyheading limitation. Preserve as polish/readlimits, not verified defects.",
            "limits": "Matched dependent visual sample, inherited text conclusions; not newblindinitialreview/equalcomprehension/generalmodelranking. All complete original reports and prior optional dispositions remain.",
        },
        "runtime": checked, "runtimeAcceptedForPublication": False, "runtimePublished": False,
        "limits": [
            "Initial textual reports/provenance/readlimits remain; this is a dependent visual follow-up in original sessions, not new blind coverage.",
            "Each27serialviews/25decodedoriginalPNGs,22distinctsourceimages. Tool resized1080x2400to900x2000; returnedhashes agree across reviewers, not sourcebyteidentity or equal comprehension.",
            "17unassignedcaptures not separately viewed; some route views exactduplicates; fullarticle completeness also relies on fulltext/native-scrollassertions; wordbodyheading not separately pictured.",
            "No fresh664Android/native; inherited663native and qualifiedTESTONLYAndroid1c1b7bf4 retainingproductionf9b59a2, not latestappmain/phone.",
            "No independentupstream/Git/signature verification by reviewers; no identifiedfallbackface,68PaintPNGs,humanhandwriting/successfulMLKit,native-speaker or measuredlearning claim.",
            "Currentmain/combinedchecks/normal signing/ownerfastforward/terminalCI/EVERYimmutablepublicZIPhash/phone/generalrelease/whole-set remain later gates.",
        ],
        "nextAction": NEXT,
    }
    assert (R / "words" / "\u9aea.md").is_file()
    import yaml
    titles = []
    for path in (R / "kanji").glob("*.md"):
        front = yaml.safe_load(path.read_text(encoding="utf-8-sig").split("---", 2)[1])
        if front["title"] == "mow; reap":
            titles.append(path.name)
    assert titles == ["\u5208.md"]
    save(target, reconciliation)
    save(R / "docs" / "n1-sources" / "execution-664.json", {
        "schemaVersion": 1, "execution": 664, "batch": "092", "status": STAGE,
        "startingState": load(C / "progress.json")["execution664StartingState"],
        "snapshot": review.HEAD, "teachingSnapshot": review.TEACHING,
        "runtime": checked, "reconciliation": target.relative_to(R).as_posix(), "receipts": receipts,
        "independentReviewersLaunched": 2, "dependentVisualConfirmation": "closed",
        "newBlindInitialReviewCredit": False, "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 118, "remainingAdditions": 1110,
        "lastPublishedCommit": load(C / "progress.json")["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Both complete reports and lossless raw events archived; 8434 unchanged runtime hashes verified.")


def finalize():
    review.ownership()
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == review.HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "HEAD", root=A) == review.ANDROID
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    changed = git("-c", "core.quotepath=false", "diff", "--name-only", review.HEAD, saved).splitlines()
    assert all(path.startswith("docs/n1-reviews/") or path == "docs/n1-sources/execution-664.json"
               for path in changed)
    checked = runtime()
    evidence = load(R / "docs" / "n1-sources" / "execution-664.json")
    for receipt in evidence["receipts"]:
        path = R.joinpath(*receipt["archive"].split("/"))
        assert sha(path) == receipt["archiveSha256"]
        if receipt.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == receipt["sourceSha256"]
    body = (C / "batch-092-visual-664-issue-body.txt").read_text(encoding="utf-8-sig")
    posted, issue = [load(C / f"batch-092-visual-664-issue-{name}.json")
                     for name in ["posted", "receipt"]]
    assert posted["id"] == issue["id"] and posted["body"] == issue["body"] == body
    assert issue["user"]["login"] == "stop-cran"
    before = load(L / "progress-before-664.json")
    state = load(C / "progress.json")
    assert state["checkpoint"] == 663 and state["batch"] == "092"
    checkpoint = {
        "schemaVersion": 1, "execution": 664, "checkpoint": 664, "batch": "092",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-664.json",
        "reconciliation": "docs/n1-reviews/batch-092-visual-reconciliation-664.json",
        "reviewedTeachingSnapshot": review.TEACHING, "androidHead": review.ANDROID,
        "dependentVisualConfirmation": "closed", "independentReviewersLaunched": 2,
        "serialReviewerProcessesExited": True, "allToolViewsSerial": True,
        "eachReviewerDecodedImageViews": 25, "distinctSourceImageHashes": 22,
        "remainingUnassignedPngs": 17, "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "actionableRemainingFindings": 0, "runtime": checked,
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "newBlindInitialReviewCredit": False,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 118, "remainingAdditions": 1110,
        "lastPublishedCommit": state["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    assert "execution664CoordinatorCheckpoint" not in state
    state.update(checkpoint=664, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution664CoordinatorCheckpoint"] = checkpoint
    state["batch092VisualAcceptanceCheckpoint"] = copy.deepcopy(checkpoint)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    temp = C / "progress.664.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")
    save(L / "visual-664-final-verification.json", checkpoint)
    print(json.dumps({
        "checkpoint": 664, "savedCommit": saved, "issue": issue["html_url"],
        "historicalRootValuesPreserved": len(before), "status": "continue",
    }))


if __name__ == "__main__":
    {"archive": archive, "finalize": finalize}[sys.argv[1]]()
