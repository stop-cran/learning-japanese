import copy
import gzip
import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("batch087review", C / "review-batch-087.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
SNAPSHOT = review.SNAPSHOT
NEXT = (
    "SAME087 fresh non-skipped sibling Android RealContentTest THREE cases and RareHanTest ONE case "
    "against THIS content tree; preserve exact XML/provenance and normally signed local evidence, then yield. "
    "Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d atop unchanged productionf9b59a2 "
    "is not latest app main. Explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot "
    "and ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, one Gradle worker and "
    "quoted '-Pkotlin.compiler.execution.strategy=in-process'. Parent19008 already owns runner.lock; "
    "NO child reacquisition/delete/unlock or parent recovery wrapper copy. Keep exact signed-head/checkpoint/"
    "wholly-clean-worktree/verified-parent-ancestry checks; preserve/report/yield actual new denial, signing "
    "hang or uncertain ownership. Textual087 closed with two serial blind families on unchanged f6391022; "
    "no actionable defect or consequential unresolved teaching claim. Both kun entries/order retained and "
    "selected: なぎ/な.ぐ; explicit on[]. Modern weather 凪ぐ and feelings 和ぐ/classical forms kept separate. "
    "Two all-mapped pairs/four directions, seven direct word guards, no changed reused teaching. "
    "Later native gate requires all21 scoped Han especially几, four production font families/system fallback, "
    "six-stroke drawing, two queuedkeysなぎ/なぐ, all three new article/SystemBack/offline routes and "
    "full archive production ContentSync ONCE with terminal case0; no guard or heap increase. N1 pool lacks "
    "N4風 and needs an actual production fallback check; All pool differs. Both original review sessions "
    "retained for dependent visuals, no new blind credit. All original source/baseline/link/reading/twofamily/"
    "native/currentmain-normalmerge/re-review/checks/normal-signing/owner-fastforward/terminalCI/"
    "EVERYimmutableZIPentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "media/path/ownerissue gates remain. Published113/1228,1115remaining unchanged; physicalphone/"
    "generalrelease/whole-set outstanding. No088, native/reviewer/publication or second runner in next host checkpoint."
)


def records():
    result = {}
    prior = None
    for label, model in review.MODELS.items():
        prefix = f"batch-087-initial-{label}"
        record = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert record["exitCode"] == 0 and record["actualModels"] == [model]
        assert record["usageCurrentModel"] == model
        assert record["multiToolResponseCount"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert coverage["allAssignedRangesReturned"]
        assert len(record["toolCalls"]) == 1
        call = record["toolCalls"][0]
        assert call["name"] == "view" and call["success"]
        assert call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
        assert sha(V / (prefix + ".md")) == record["reportSha256"]
        assert sha(V / (prefix + ".jsonl")) == record["rawExecutionSha256"]
        assert subprocess.run(["pwsh", "-NoProfile", "-Command",
                               f"if (Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                              capture_output=True).returncode == 0
        if prior:
            assert datetime.fromisoformat(prior) < datetime.fromisoformat(record["startedAt"])
        prior = record["completedAt"]
        result[label] = {
            **{k: record[k] for k in [
                "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
                "requestedModel", "actualModels", "snapshot", "reportSha256", "rawExecutionSha256"]},
            "report": prefix + ".md", "execution": prefix + "-execution.json",
            "coverage": prefix + "-coverage.json", "allAssignedRangesReturned": True,
            "toolCalls": 1, "observedToolOverlaps": 0,
        }
    return result


def close():
    review.frozen()
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract

    processes = records()
    assert review.PACKET.read_bytes() == (V / review.PACKET.name).read_bytes()
    ledger = load(S / "batch-087-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    mechanical = audit(R, "087")
    assert mechanical["dictionaryFamilies"] == 25
    assert mechanical["changedReusedArticles"] == 0 and mechanical["newWords"] == 2
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == info["sha256"]
        assert (C / "inputs" / name).stat().st_size == info["bytes"]
    dictionary = C / "inputs" / "n1-implementation-JMdict_e.gz"
    compressed = dictionary.read_bytes()
    for packet in ledger["dictionaryPackets"]:
        selection = load(S / packet["selection"])
        assert extract(compressed, snapshot["inputs"][dictionary.name]["sha256"],
                       selection["entryIds"]) == (S / packet["xml"]).read_bytes()
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = ["川", "出", "木"]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    pairs = {tuple(row) for row in ledger["allMappedReciprocalPairs"]}
    assert len(pairs) == 2
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / (c + ".md")).read_text(encoding="utf-8")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8420 and manifest["contentVersion"] == "eb3a9413cccd4f57"
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    title = metadata(R, "kanji/凪.md")["title"]
    assert sum(metadata(R, "kanji/" + p.name)["title"] == title for p in (R / "kanji").glob("*.md")) == 1
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests"]:
        src = C / f"batch-087-textual-review-{stem}-611.txt"
        text = src.read_text(encoding="utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "tests":
            assert "Ran 34 tests" in text and text.rstrip().endswith("OK")
        elif stem == "audit":
            assert json.loads(text) == mechanical
        dst = V / src.name
        shutil.copyfile(src, dst)
        receipts[stem] = {"path": str(dst.relative_to(R)).replace("\\", "/"), "sha256": sha(dst)}
    reviewed = ["kanji/凪.md", "words/凪.md", "words/凪ぐ.md"]
    limits = [
        "Textual closure only. Fresh non-skipped Android/native/fourfont/visual/combinedmain/signing/publication gates pending; runtime not accepted or published.",
        "Both actual model families independently received identical146190byte2830line packet with25distinct completeJMdictfamilies,5rawcharacters,16completearticlebodies including3new and0changedreuseddiffs. Each returned one exact fullpacketview, no truncation/tooloverlap/unfinishedtool. Bytes do not prove comprehension or equivalent fresh-read depth.",
        "Original reports preserved verbatim. No author adjudication or other report supplied to initial reviewers. No teaching fix needed; zero dependent textual confirmations, original sessions retained for later visuals.",
        "PublicDaijisen/Jitsu/Nipponica/Paraglider text extracted by coordinator from committedHTML; formatting/links stripped, imageplaceholders retained. Not independentupstream retrieval, historical-glyphinspection or contemporaryfrequencymeasurement.",
        "Both rawkunreadings/order preserved and selectedなぎ/な.ぐ; expliciton[]. Weather noun/modern gu-endingverb kept separate from feelings和ぐ and classical conjugation. No universal ban on creative figurativeusage or wordlevel/frequency inferred from character membership/grade9.",
        "Twoallmappedpairs/fourdirections, noactivatedbaselinepair/reusedteaching. Sevendirectguards not transitivecliques or universal livepool safety. Allpool has3curatedwrongcards; N1 excludes N4風 and needs actualproductionfallbackcheck. Larger/random/custompools uncertified.",
        "All21scopedHan especially几 missingmainbundledcmap needfreshnativefourfont/systemfallback legibility; cmapabsence notglyphfailure. Sixpinnedstrokes unchanged. Inheritedall40font evidence stayshistorical.",
        "QualifiedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9b59a2 is not latestappmain. Compatibleclientf9b59a2+ required; oldclients ignorecuration/wordguards. Physicalphone/generalrelease/whole-set outstanding.",
        "Published113/1228,1115acceptanceremainder unchanged. Sixseparate earlierN2sourcemembers保案派第策結 are not acceptedissue60 additions or candidates toduplicate/relevel.",
        "Alloriginalnormalmerge/substantiveteachingreview/validation/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemedia/safepaths/ownerissue gates remain; no guardincrease or algorithmchange.",
        "Liveparent19008 retainsrunner.lock; nochildacquisition/delete/unlock. Approvedcontrolhelpers/committedsourcepackets/frozenworkspaceinputs only; nooptionalhistoricalsessionhelper access, policychange or actualnewpermissiondenial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 611, "batch": "087",
        "status": "textually-review-closed-awaiting-fresh-android",
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False,
        "reviewedRuntimeHashes": {n: sha(R / n) for n in reviewed + ["strokes/凪.json", "manifest.json"]},
        "initialModels": list(review.MODELS.values()), "processes": processes,
        "serialReviewerProcessesVerified": True, "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": review.PACKET.stat().st_size, "initialPacketLines": 2830,
        "initialDistinctCompleteFamilies": 25, "rawCharacterRecords": 5,
        "completeArticleBodiesSupplied": 16, "newArticleBodies": 3, "changedReusedBodies": 0,
        "originalSessionSupplements": 0,
        "verdicts": {n: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"} for n in reviewed},
        "findings": [],
        "hypothesisDispositions": [
            {"claim": "N1-only fallback could produce an overlapping calm/quiet label", "reportedBy": ["Claude hypothesis", "GPT Limits"],
             "status": "unresolved", "category": "pending-native-production-acceptance-not-article-defect",
             "evidence": "Actual N4風 is excluded from N1; three curated slots are only fully available in All. No actual fallback run is claimed.",
             "decision": "No invented textual fix or universal safety claim. Required actual N1/All production choices remain a native gate before runtime acceptance/publication."},
            {"claim": "Oldclient ignores wordquizguards", "reportedBy": ["Claude hypothesis", "GPT Limits"],
             "status": "resolved", "resolution": "Existing documented compatibleclient prerequisitef9b59a2+ remains mandatory. This does not certify oldclient pools."},
            {"claim": "Potential figurative emotional uses could qualify the not-composure wording", "reportedBy": ["Claude hypothesis"],
             "status": "withdrawn", "confidence": "high for scoped disposition, not corpus-wide impossibility",
             "evidence": "JMdict1459650 weathernoun and1459660 weatherverb versus separate2859999feelings和ぐ; actual Daijisen modern sense1凪ぐ versus sense2和ぐ. words凪:41-45 says not a GENERAL equivalent and focuses HERE on wind/sea; words凪ぐ:44-48 explicitly teaches modernweather and ordinaryweather spelling.",
             "decision": "No current sentence forbids all figurative creativity. No corpus evidence establishes a defect; preserve the hypothesis without manufacturing a rule or expanding the assignment."},
            {"claim": "Whole-corpus kanjititle uniqueness not independently verified by reviewer", "reportedBy": ["Claude Limits"],
             "status": "resolved", "resolution": "Coordinator fresh allactualkanjititle scan finds calm seas;lull exactly once; validator0errors, batchaudit and exactruntimehashes pass. Not retroactive reviewer-independentGitverification."},
        ],
        "optionalDispositions": [
            {"claim": "Mention nounなぎ and verb凪ぎます stem kana overlap", "reportedBy": ["Claude"], "status": "optional",
             "decision": "No edit. Current distinct dictionaryforms plus full kana paradigm and noun comparison already explain the scoped contrast."},
            {"claim": "Add comparison JMdict1589220 citation in凪ぐ article", "reportedBy": ["Claude"], "status": "optional",
             "decision": "No edit. Complete applicable family already in source/review evidence; no mandatory percomparison footercitation quota."},
            {"claim": "CiteJitsu historical wind-abbreviation derivation", "reportedBy": ["Claude"], "status": "optional",
             "decision": "No edit. Current clearly labelled mnemonic is not a historicalclaim. Supplied imageplaceholder limits do not authorize an expanded etymology."},
            {"claim": "Smooth nounversusなadjective wording", "reportedBy": ["Claude"], "status": "optional",
             "decision": "No edit. Existing 凪です with kana and explicit noun explanation is comprehensible; no actionable defect established."},
        ],
        "modelContributionComparison": {
            "shared": "Bothinitials accepted all3completearticles, bothrawkunentries/separateexamples, no inventedon, modernweather/feelings/classicalboundary, 3wrongkanjilabels,7directguards,2mappedpairs and source/compatibility/nativefallbacklimits.",
            "claudeUnique": "Unprovedfigurativeusagehypothesis and4optionalpolish/expansioncategories; none established mandatoryfix. Wholecorpusuniquenesslimit checkedmechanically. N1fallback/oldclientobservations equivalent toGPTLimits, not unique.",
            "gptUnique": "No uniqueverifieddefect; detailed per-filefacetedverdicts and dictionaryfamily enumeration, substantive conclusions shared.",
            "limits": "Common matchedsnapshot/task/sourceaccess; no defectquota or generalmodelranking. Allsectionsincludinghypotheses/optional/limits compared; labeldifferences do not create uniquecontribution.",
        },
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "freshFrozenLexicalPacketsVerified": 2, "frozenInputHashesVerified": 5,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "directWordExclusionPairs": 7,
        "actualHanCount": 21, "nativeFontPending": ["几"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 34,
        "newNativeOrAndroidClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    assert not (V / "batch-087-reconciliation.json").exists()
    save(V / "batch-087-reconciliation.json", rec)
    ledger["runtimeDraftLimits"] = ledger["limits"]
    ledger.update(status=rec["status"], textualReviewClosed=True, runtimeAccepted=False,
                  reviewClosed=[], published=[], reviewSnapshot=SNAPSHOT,
                  reviewEvidence="docs/n1-reviews/batch-087-reconciliation.json",
                  textuallyResolvedFindings=[], nextAction=NEXT, limits=limits)
    save(S / "batch-087-progress.json", ledger)
    for src, name in [(C / "review-batch-087.py", "batch-087-review-recipe.py"),
                      (Path(__file__), "batch-087-textual-closure-recipe.py")]:
        shutil.copyfile(src, S / name)
    save(S / "execution-611.json", {
        "schemaVersion": 1, "execution": 611, "batch": "087", "teachingSnapshot": SNAPSHOT,
        "status": rec["status"], "reconciliation": "docs/n1-reviews/batch-087-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-087-reconciliation.json"),
        "recipeHashes": {n: sha(S / n) for n in ["batch-087-review-recipe.py", "batch-087-textual-closure-recipe.py"]},
        "checks": receipts, "runtimeHashesReverified": checked, "focusedTestsPassed": 34,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "newAndroidOrNativeClaimed": False, "wholeProjectComplete": False,
        "publishedAdditions": 113, "remainingAdditions": 1115,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "limits": limits,
    })
    print("Textual closure persisted; unchanged runtime hashes verified:", checked)


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != SNAPSHOT and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == review.ANDROID
    assert not git("status", "--porcelain", repo=A)
    rec = load(V / "batch-087-reconciliation.json")
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    p = load(C / "progress.json")
    original = load(L / "progress-before-611.json")
    assert p["checkpoint"] == 610
    p["execution611StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    cp = {
        "schemaVersion": 1, "execution": 611, "checkpoint": 611, "batch": "087",
        "savedCommit": head, "signature": "G", "initialTeachingSnapshot": SNAPSHOT,
        "status": "continue", "stage": rec["status"],
        "reconciliation": "docs/n1-reviews/batch-087-reconciliation.json",
        "evidence": "docs/n1-sources/execution-611.json",
        "actualInitialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionSupplements": 0, "serialProcessesAndInternalToolsVerified": True,
        "allAssignedPacketRangesReturned": True, "originalReportsPreserved": True,
        "initialDistinctCompleteFamilies": 25, "rawCharacterRecords": 5,
        "textualReviewClosed": True, "actionableRemainingTeachingFindings": 0,
        "consequentialUnresolvedTeachingFindings": 0, "runtimeHashesReverified": 8420,
        "focusedTestsPassedThisCheckpoint": 34, "runtimeChanged": False,
        "runtimePublished": False, "runtimeAccepted": False, "newAndroidOrNativeClaimed": False,
        "nativeFontPending": rec["nativeFontPending"], "actualHanCount": 21,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "directWordExclusionPairs": 7,
        "reviewClosed": [], "published": [], "publishedAdditions": 113, "remainingAdditions": 1115,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "dedicatedWorktreesClean": True,
        "originalHistoricalRootKeysCompared": len(original), "allOriginalHistoricalValuesPreserved": True,
    }
    p["execution611CoordinatorCheckpoint"] = cp
    p["batch087TextualReviewCheckpoint"] = dict(cp)
    p.update(checkpoint=611, status="continue", stage=rec["status"], nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print("Checkpoint611 saved:", head, "; historical root values preserved:", len(original))


if __name__ == "__main__":
    {"close": close, "checkpoint": checkpoint}[sys.argv[1]]()
