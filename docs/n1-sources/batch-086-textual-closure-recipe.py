import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from importlib.util import module_from_spec, spec_from_file_location

C = Path(__file__).parent
R = C.parent / "learning-japanese"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
L = C / "logs" / "25340444-92a6-474e-80a4-df2c86d9481c"
SPEC = spec_from_file_location("batch086review", C / "review-batch-086.py")
review = module_from_spec(SPEC)
SPEC.loader.exec_module(review)
load, save, sha, git = review.load, review.save, review.sha, review.git
SNAPSHOT = review.SNAPSHOT
NEXT = (
    "SAME086 fresh non-skipped sibling Android RealContentTest THREE cases and RareHanTest ONE case "
    "against THIS content tree; preserve exact XML/provenance and normally signed local evidence, then yield. "
    "Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d atop unchanged productionf9b59a2 "
    "is not latest app main. Explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot "
    "and ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, one Gradle worker and "
    "quoted '-Pkotlin.compiler.execution.strategy=in-process'. Parent19008 already owns runner.lock; "
    "NO child reacquisition/delete/unlock or parent recovery wrapper copy. Keep exact signed-head/checkpoint/"
    "wholly-clean-worktree/verified-parent-ancestry checks; preserve/report/yield actual new denial, signing "
    "hang or uncertain ownership. Textual086 closed with two serial blind families on unchanged f59c65fd; "
    "no actionable defect or consequential unresolved teaching claim. Rawおうよ.そ modern usage explicitly "
    "UNVERIFIED source-only, not normalized. Allfive readings/order retained; onlyボン/ハン selected, kun[]. "
    "Seven all-mapped pairs/fourteen directions including aliases/reused平/例/全 and eight direct word guards. "
    "Later native gate requires all31 scoped Han especially丶/几, four production font families/system fallback, "
    "three-stroke drawing, two queuedkeysぼん/はん, all changed teaching/article/SystemBack/offline routes and "
    "full archive production ContentSync ONCE with terminal case0; no guard or heap increase. Both original "
    "review sessions retained for dependent visuals, no new blind credit. All original source/baseline/link/"
    "reading/twofamily/native/currentmain-normalmerge/re-review/checks/normal-signing/owner-fastforward/"
    "terminalCI/EVERYimmutableZIPentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "media/path/ownerissue gates remain. Published112/1228,1116remaining unchanged; physicalphone/"
    "generalrelease/whole-set outstanding. No087, native/reviewer/publication or second runner in next host checkpoint."
)


def records():
    result = {}
    prior = None
    for label, model in review.MODELS.items():
        prefix = f"batch-086-initial-{label}"
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
        check = subprocess.run(["pwsh", "-NoProfile", "-Command",
                                f"if (Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                               capture_output=True)
        assert check.returncode == 0
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
    from audit_n1_batch import audit, lexical_pair
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    import xml.etree.ElementTree as ET

    processes = records()
    for name in ["batch-086-initial-packet.txt"]:
        assert (C / name).read_bytes() == (V / name).read_bytes()
    ledger = load(S / "batch-086-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    mechanical = audit(R, "086")
    assert mechanical["dictionaryFamilies"] == 71
    assert mechanical["changedReusedArticles"] == 6 and mechanical["newWords"] == 1
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == info["sha256"]
        assert (C / "inputs" / name).stat().st_size == info["bytes"]
    dictionary = C / "inputs" / "n1-implementation-JMdict_e.gz"
    compressed = dictionary.read_bytes()
    families = {}
    for packet in ledger["dictionaryPackets"]:
        selection = load(S / packet["selection"])
        assert extract(compressed, snapshot["inputs"][dictionary.name]["sha256"],
                       selection["entryIds"]) == (S / packet["xml"]).read_bytes()
        families.update({e.findtext("ent_seq"): e for e in ET.parse(S / packet["xml"]).getroot().findall("entry")})
    assert len(families) == 71
    for row in ledger["recognitionAliasMappings"]:
        assert any(lexical_pair(families[i], row["spelling"], row["primaryReading"]) for i in row["entryIds"])
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(info["metadata"])
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
    assert len(pairs) == 7
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
    assert checked == 8416 and manifest["contentVersion"] == "86e8cb13aa72ecd0"
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    titles = [metadata(R, "kanji/" + p.name)["title"] for p in (R / "kanji").glob("*.md")]
    assert titles.count("commonplace; mediocre") == 1
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests"]:
        src = C / f"batch-086-textual-review-{stem}-602.txt"
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
    reviewed = ["kanji/凡.md", "words/凡例.md"] + [row["article"] for row in ledger["changedReusedPassages"]]
    limits = [
        "Textual closure only. Fresh non-skipped Android/native/fourfont/visual/combinedmain/signing/publication gates pending; runtime not accepted or published.",
        "Both actual model families independently received identical215474byte4300line packet with71distinct completeJMdictfamilies,7rawcharacters,28completearticlebodies including2new and6boundedreuseddiffs. Each returned one exact fullpacketview, no truncation/tooloverlap/unfinishedtool. Bytes do not prove comprehension or equivalent fresh-read depth.",
        "Original reports preserved verbatim. No author adjudication or other report supplied to initial reviewers. No teaching fix needed; zero dependent textual confirmations, original sessions retained for later visuals.",
        "PublicDaijisen/Seisen text was extracted by coordinator from committedHTML; formatting/links stripped, imageplaceholders retained, other dictionaryarticles omitted. Not independentupstream retrieval, etymologicalproof or contemporaryfrequencymeasurement.",
        "Rawおうよ.そ modern usage UNVERIFIED source-only; exact raw metadata/order preserved, not normalized toおおよ.そ or proven typo. Explicitkun[] excludes it; onlyボン/ハン selected. Recognition凡そ usuallykana and凡て rareKANJI spelling do not make kana pronunciation rare.",
        "Sevenallmappedpairs/fourteendirections include aliases and reused平/例/全; oneactivatedbaselinepair凡/平凡. Eightdirectguards not transitivecliques or universal livepool safety. Threecuratedwrongkanjifilldefaultfourchoices; larger/random/custom pools uncertified.",
        "All31scopedHan especially丶/几 missingmainbundledcmap needfreshnativefourfont/systemfallback legibility; cmapabsence notglyphfailure. Threepinnedstrokes unchanged. Inheritedall40font evidence stayshistorical.",
        "QualifiedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9b59a2 is not latestappmain. Compatibleclientf9b59a2+ required; oldclients ignorecuration/wordlevels. Physicalphone/generalrelease/whole-set outstanding.",
        "Published112/1228,1116acceptanceremainder unchanged. Sixseparate earlierN2sourcemembers保案派第策結 are not acceptedissue60 additions or candidates toduplicate/relevel.",
        "Alloriginalnormalmerge/substantiveteachingreview/validation/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemedia/safepaths/ownerissue gates remain; no guardincrease or algorithmchange.",
        "Liveparent19008 retainsrunner.lock; nochildacquisition/delete/unlock. Approvedcontrolhelpers/committedsourcepackets/frozenworkspaceinputs only; nooptionalhistoricalsessionhelper access, policychange or actualnewpermissiondenial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 602, "batch": "086",
        "status": "textually-review-closed-awaiting-fresh-android",
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False,
        "reviewedRuntimeHashes": {n: sha(R / n) for n in reviewed + ["strokes/凡.json", "manifest.json"]},
        "initialModels": list(review.MODELS.values()), "processes": processes,
        "serialReviewerProcessesVerified": True, "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": review.PACKET.stat().st_size, "initialPacketLines": 4300,
        "initialDistinctCompleteFamilies": 71, "rawCharacterRecords": 7,
        "completeArticleBodiesSupplied": 28, "newArticleBodies": 2, "changedReusedBodies": 6,
        "originalSessionSupplements": 0,
        "verdicts": {n: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"} for n in reviewed},
        "findings": [],
        "hypothesisDispositions": [
            {"claim": "Possible凡例/栞 missing direct quiz guard", "reportedBy": ["Claude hypothesis"],
             "status": "withdrawn", "confidence": "high for bounded disposition, not allpool safety",
             "evidence": "Actual凡例 titleexplanatory notes;legend and1523690usageguide/maplegend versus actual栞 titlebookmark;guidebook and1568040bookmark/guidebook. Complete families and actual栞 article supplied to both reviewers, freshly checked by coordinator. A work's usage conventions/legend are not the guidebook object or bookmark.",
             "decision": "No demonstrated overlapping displayed answer. Same book topic or broad English guide substring does not establish synonymy. Claude itself calls acceptance unlikely, GPT establishes no additionalguard. No edit or consequential unresolved teaching claim; not vote-based."},
            {"claim": "Oldclient wordlevel and reading-curation fallback", "reportedBy": ["Claude hypothesis", "GPT Limits"],
             "status": "resolved", "resolution": "Existing documented compatibleclient prerequisitef9b59a2+ remains mandatory. Currentwordlevel preserves平凡N2; no inferred newwordlevel. Oldclientfallback is not a teaching defect or a new waiver."},
            {"claim": "Unable to independently check title uniqueness", "reportedBy": ["Claude Limits"],
             "status": "resolved", "resolution": "Coordinator fresh allactualkanjititle scan finds commonplace;mediocre exactly once. Validator0errors, batchaudit and exactruntimehashes pass. Not retroactive reviewer-independentGitverification."},
        ],
        "optionalDispositions": [
            {"claim": "Clarifydotcomparisonbecause九hasnodot", "reportedBy": ["Claude"], "status": "optional",
             "decision": "No edit. Existing cue compares position ofdot andlongouterstroke rather than asserting九hasadot; exactnativevisualshape inspection remainspending."},
            {"claim": "Addeditorialpolicy or例言 synonym to凡例", "reportedBy": ["Claude"], "status": "optional",
             "decision": "No edit. Currentusageconventions and reference-book explanation answer scopedquestion; no exhaustive synonymquota."},
            {"claim": "Addrareおおよそreadingof凡そ", "reportedBy": ["Claude"], "status": "optional",
             "decision": "No edit. Currentexactおよそ entry andqualifiedrecognition valid; alternatefamily1415050 does not verifyrawおうよ.そ. Do not conflatespelling/pronunciation/source-onlyreading."},
            {"claim": "Add凡人/非凡/凡庸 examples", "reportedBy": ["Claude"], "status": "optional",
             "decision": "No edit. Two usefulselectedonexamples suffice; no supportarticleexpansionquota."},
        ],
        "modelContributionComparison": {
            "shared": "Bothinitials accepted complete2newarticles,6exactreuseddiffs,all5rawreadings/2selectedonkeys,aliasqualifications,3wrongkanjilabels,8guards,7mappedpairs and source/compatibilitylimits.",
            "claudeUnique": "Lowconfidence栞guardhypothesis and4optionalpolish/expansioncategories; none established usefulmandatoryfix. Titleuniquenesslimit checkedmechanically. Oldclientlimitation equivalent toGPTLimits, not unique.",
            "gptUnique": "No uniqueverifieddefect; detailed per-filefacetedverdicts and source-onlyreadingboundary shared in substance.",
            "limits": "Common matchedsnapshot/task/sourceaccess; no defectquota or generalmodelranking. Allsectionsincludinghypotheses/optional/limits compared; labeldifferences do not create uniquecontribution.",
        },
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "freshFrozenLexicalPacketsVerified": 3, "frozenInputHashesVerified": 5,
        "allMappedReciprocalPairs": 7, "directedLinksVerified": 14, "directWordExclusionPairs": 8,
        "actualHanCount": 31, "nativeFontPending": ["丶", "几"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 34,
        "newNativeOrAndroidClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    assert not (V / "batch-086-reconciliation.json").exists()
    save(V / "batch-086-reconciliation.json", rec)
    ledger["runtimeDraftLimits"] = ledger["limits"]
    ledger.update(status=rec["status"], textualReviewClosed=True, runtimeAccepted=False,
                  reviewClosed=[], published=[], reviewSnapshot=SNAPSHOT,
                  reviewEvidence="docs/n1-reviews/batch-086-reconciliation.json",
                  textuallyResolvedFindings=[], nextAction=NEXT, limits=limits)
    save(S / "batch-086-progress.json", ledger)
    for src, name in [(C / "review-batch-086.py", "batch-086-review-recipe.py"),
                      (Path(__file__), "batch-086-textual-closure-recipe.py")]:
        shutil.copyfile(src, S / name)
    save(S / "execution-602.json", {
        "schemaVersion": 1, "execution": 602, "batch": "086", "teachingSnapshot": SNAPSHOT,
        "status": rec["status"], "reconciliation": "docs/n1-reviews/batch-086-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-086-reconciliation.json"),
        "recipeHashes": {n: sha(S / n) for n in ["batch-086-review-recipe.py", "batch-086-textual-closure-recipe.py"]},
        "checks": receipts, "runtimeHashesReverified": checked, "focusedTestsPassed": 34,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "newAndroidOrNativeClaimed": False, "wholeProjectComplete": False,
        "publishedAdditions": 112, "remainingAdditions": 1116,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "limits": limits,
    })
    print("Textual closure persisted; unchanged runtime hashes verified:", checked)


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != SNAPSHOT and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=review.A) == review.ANDROID
    assert not git("status", "--porcelain", repo=review.A)
    rec = load(V / "batch-086-reconciliation.json")
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    p = load(C / "progress.json")
    original = load(L / "progress-before-602.json")
    assert p["checkpoint"] == 601
    p["execution602StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    cp = {
        "schemaVersion": 1, "execution": 602, "checkpoint": 602, "batch": "086",
        "savedCommit": head, "signature": "G", "initialTeachingSnapshot": SNAPSHOT,
        "status": "continue", "stage": rec["status"],
        "reconciliation": "docs/n1-reviews/batch-086-reconciliation.json",
        "evidence": "docs/n1-sources/execution-602.json",
        "actualInitialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionSupplements": 0, "serialProcessesAndInternalToolsVerified": True,
        "allAssignedPacketRangesReturned": True, "originalReportsPreserved": True,
        "initialDistinctCompleteFamilies": 71, "rawCharacterRecords": 7,
        "textualReviewClosed": True, "actionableRemainingTeachingFindings": 0,
        "consequentialUnresolvedTeachingFindings": 0, "runtimeHashesReverified": 8416,
        "focusedTestsPassedThisCheckpoint": 34, "runtimeChanged": False,
        "runtimePublished": False, "runtimeAccepted": False, "newAndroidOrNativeClaimed": False,
        "nativeFontPending": rec["nativeFontPending"], "actualHanCount": 31,
        "allMappedReciprocalPairs": 7, "directedLinksVerified": 14, "directWordExclusionPairs": 8,
        "reviewClosed": [], "published": [], "publishedAdditions": 112, "remainingAdditions": 1116,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "dedicatedWorktreesClean": True,
        "originalHistoricalRootKeysCompared": len(original), "allOriginalHistoricalValuesPreserved": True,
    }
    p["execution602CoordinatorCheckpoint"] = cp
    p["batch086TextualReviewCheckpoint"] = dict(cp)
    p.update(checkpoint=602, status="continue", stage=rec["status"], nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print("Checkpoint602 saved:", head, "; historical root values preserved:", len(original))


if __name__ == "__main__":
    {"close": close, "checkpoint": checkpoint}[sys.argv[1]]()
