import copy
import gzip
import importlib.util
import json
import shutil
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("review089", C / "review-batch-089.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
SNAPSHOT = review.SNAPSHOT
NEXT = (
    "SAME089 fresh non-skipped sibling Android RealContentTest THREE cases and RareHanTest ONE case "
    "against THIS content tree; preserve exact XML/provenance and normally signed local evidence, then yield. "
    "Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d atop unchanged productionf9b59a2 "
    "is not latest app main. Explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot "
    "and ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, one Gradle worker and "
    "quoted '-Pkotlin.compiler.execution.strategy=in-process'. Parent19008 already owns runner.lock; "
    "NO child reacquisition/delete/unlock or parent recovery wrapper copy. Keep exact signed-head/checkpoint/"
    "wholly-clean-worktree/verified-parent-ancestry checks; preserve/report/yield actual new denial, signing "
    "hang or uncertain ownership. Textual089 closed with two serial blind families on unchanged4b84608b; "
    "no actionable defect or consequential unresolved teaching claim. Sole raw/selected onキョウ, rawkun[]/"
    "explicitquizkun[]; own linked凶作 row, noun/agriculturalverypooryield not harvestverb/necessaryzeroyield/"
    "famine/badwork, compound-specific modifier+head作crop/yield. New凶/凶作 and exact additive作navigation "
    "reviewed; two allmappedpairs/four directions, one direct収穫guard. GPT made an exact unrestricted "
    "fullpacketread then three unnecessary serial overlapping tailreads; two tailresponses truncated, "
    "original execution/report retained. No missing assigned range, overlap, denial or teaching fix. "
    "Later native gate requires all23 scopedHan especially乂/凵, four production font families/system "
    "fallback, fourstroke drawing, singlequeuedkeyきょう, both new article/SystemBack/offline routes and "
    "full archive production ContentSync ONCE with terminal case0; no guard or heap increase. Actual "
    "N1/All production choices remain required despite allthree curated wrongcards being N1-available. "
    "Both original review sessions retained for dependent visuals, no new blind credit. All original "
    "source/baseline/link/reading/twofamily/native/currentmain-normalmerge/re-review/checks/normal-signing/"
    "owner-fastforward/terminalCI/EVERYimmutableZIPentryhash/original18000entries42MiBcompressed80MiBinflated"
    "56MiBretained/media/path/ownerissue gates remain. Published115/1228,1113remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No090, native/reviewer/publication or second runner "
    "in next host checkpoint."
)


def records():
    result = {}
    prior = None
    for label, model in review.MODELS.items():
        prefix = f"batch-089-initial-{label}"
        record = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert record["exitCode"] == 0 and record["actualModels"] == [model]
        assert record["usageCurrentModel"] == model
        assert record["multiToolResponseCount"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert coverage["allAssignedRangesReturned"]
        assert len(record["toolCalls"]) == (1 if label == "claude" else 4)
        first = record["toolCalls"][0]
        assert first["name"] == "view" and first["success"]
        assert first["exactRequestedTextContainedInResult"] and not first["truncationMarker"]
        assert all(c["name"] == "view" and c["success"] for c in record["toolCalls"])
        assert sha(V / (prefix + ".md")) == record["reportSha256"]
        assert sha(V / (prefix + ".jsonl")) == record["rawExecutionSha256"]
        assert review.absent(record["launcherPid"])
        if prior:
            assert datetime.fromisoformat(prior) < datetime.fromisoformat(record["startedAt"])
        prior = record["completedAt"]
        result[label] = {
            **{k: record[k] for k in [
                "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
                "requestedModel", "actualModels", "snapshot", "reportSha256", "rawExecutionSha256"]},
            "report": prefix + ".md", "execution": prefix + "-execution.json",
            "coverage": prefix + "-coverage.json", "allAssignedRangesReturned": True,
            "toolCalls": len(record["toolCalls"]), "observedToolOverlaps": 0,
            "firstCallExactFullPacketReturned": True,
            "truncatedRedundantTailResponses": sum(c["truncationMarker"] for c in record["toolCalls"]),
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
    ledger = load(S / "batch-089-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    mechanical = audit(R, "089")
    assert mechanical["dictionaryFamilies"] == 73
    assert mechanical["changedReusedArticles"] == 1 and mechanical["newWords"] == 1
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        assert sha(C / "inputs" / name) == info["sha256"]
        assert (C / "inputs" / name).stat().st_size == info["bytes"]
    dictionary = C / "inputs" / "n1-implementation-JMdict_e.gz"
    compressed = dictionary.read_bytes()
    assert review.hashlib.sha256(gzip.decompress(compressed)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    for packet in ledger["dictionaryPackets"]:
        selection = load(S / packet["selection"])
        assert extract(compressed, snapshot["inputs"][dictionary.name]["sha256"],
                       selection["entryIds"]) == (S / packet["xml"]).read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert review.hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    chars = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    raw_count = 0
    for name in ["batch-089-kanjidic2.xml", "batch-089-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(chars[entry.findtext("literal")])
            raw_count += 1
    assert raw_count == 6
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
    assert pairs == {("凶", "words/凶作.md"), ("作", "words/凶作.md")}
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
    assert checked == 8426 and manifest["contentVersion"] == "c6562f11cb371053"
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    title = metadata(R, "kanji/凶.md")["title"]
    assert sum(metadata(R, "kanji/" + p.name)["title"] == title for p in (R / "kanji").glob("*.md")) == 1
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests"]:
        src = C / f"batch-089-textual-review-{stem}-629.txt"
        text = src.read_text(encoding="utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "tests":
            assert "Ran 43 tests" in text and text.rstrip().endswith("OK")
        elif stem == "audit":
            assert json.loads(text) == mechanical
        dst = V / src.name
        shutil.copyfile(src, dst)
        receipts[stem] = {"path": str(dst.relative_to(R)).replace("\\", "/"), "sha256": sha(dst)}
    reviewed = ["kanji/凶.md", "words/凶作.md", "kanji/作.md"]
    limits = [
        "Textual closure only. Fresh non-skipped Android/native/fourfont/visual/combinedmain/signing/publication gates pending; runtime not accepted or published.",
        "Both actual families independently received identical173695byte3568line packet with73completeJMdictfamilies,6rawcharacters and14completearticlebodies including2new and1changedreusednavigationdiff. Both firstcalls returned exact fullpacket, no truncation. Bytes do not prove comprehension or equivalent fresh-read depth.",
        "GPT unnecessarily repeated three serial overlappingtailreads after the complete firstread; two redundantresponses truncated, finaltail exact. Originalreport and execution retain deviation. Fourserialcalls not one, no concurrenttools, missingassignedrange or denial. No repeat reviewer run or retroactive onecallclaim.",
        "Original reports preserved verbatim before reconciliation. No author adjudication or other report supplied to initial reviewers. No teaching fix needed; zero dependent textual confirmations, original sessions retained for later visuals.",
        "PublicDaijisen/Nikkoku/Jitsu/encyclopedia text supplied as coordinator extraction from committedHTML; formatting/links stripped, imageplaceholders retained. Not independentupstream retrieval, historical-glyphinspection, contemporaryfrequencymeasurement or verification of every historical/agronomic statement.",
        "Sole raw/selected onキョウ and rawkun[]/explicitquizkun[] retained. Ownlinked凶作row, actual characterallocation, compound-specific作crop/yield. No extra readings from Jitsu glosses, wordlevel inference, numericalfailurethreshold or necessaryfamine/zeroyield claim.",
        "Twoallmappedpairs/fourdirections including reused作; noactivatedbaselinepair. One direct収穫guard not a transitiveclique or universal livepool safety. Allthree curatedwrongcards N1-available; actualN1/All production and broader custom/randompools remain uncertified.",
        "All23scopedHan especially乂/凵 missingmainbundledcmap needfreshnativefourfont/systemfallback legibility; cmapabsence notglyphfailure. Fourpinnedstrokes unchanged. Inheritedall40font evidence stayshistorical.",
        "QualifiedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9b59a2 is not latestappmain. Compatibleclientf9b59a2+ required; oldclients ignorecuration/wordguards. Physicalphone/generalrelease/whole-set outstanding.",
        "Published115/1228,1113acceptanceremainder unchanged. Sixseparate earlierN2sourcemembers保案派第策結 are not acceptedissue60 additions or candidates toduplicate/relevel; separate妖exception retained.",
        "Alloriginalnormalmerge/substantiveteachingreview/validation/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemedia/safepaths/ownerissue gates remain; no guardincrease or algorithmchange.",
        "Liveparent19008 retainsrunner.lock; nochildacquisition/delete/unlock. Approvedcontrolhelpers/committedsourcepackets/frozenworkspaceinputs only; nooptionalhistoricalsessionhelper access, policychange or actualnewpermissiondenial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 629, "batch": "089",
        "status": "textually-review-closed-awaiting-fresh-android",
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False,
        "reviewedRuntimeHashes": {n: sha(R / n) for n in reviewed + ["strokes/凶.json", "manifest.json"]},
        "initialModels": list(review.MODELS.values()), "processes": processes,
        "serialReviewerProcessesVerified": True, "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": review.PACKET.stat().st_size, "initialPacketLines": 3568,
        "initialDistinctCompleteFamilies": 73, "rawCharacterRecords": 6,
        "completeArticleBodiesSupplied": 14, "newArticleBodies": 2, "changedReusedBodies": 1,
        "originalSessionSupplements": 0,
        "verdicts": {n: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
                        "textComprehensibility": "CLEAN",
                        "scope": "additive navigation line44 only" if n == "kanji/作.md" else "complete new article"}
                     for n in reviewed},
        "findings": [],
        "hypothesisDispositions": [
            {"claim": "Overlapping evil titles of凶and悪 may become extra choices in larger/changed quiz pools",
             "reportedBy": ["Claude Hypothesis; GPT Limits widerpool caveat"],
             "status": "unresolved", "category": "pending-native-production-acceptance-not-article-defect",
             "evidence": "Actual凶distractors凡/凸/凹 are all N1-available; 悪alreadyhas意/急/思. No defaultmissing-slot or demonstratedbadquestion established. Both actualN1/All production and widercustompools not yet certified.",
             "decision": "No inventedtextualfix. Mandatory nativeN1/All productionacceptance retained; widerchanged/custompools explicitlyuncertified."},
            {"claim": "Whole-corpus kanjititle uniqueness not independently checked",
             "reportedBy": ["Claude Limits"], "status": "resolved",
             "resolution": "Coordinator fresh allactualkanjititle scan finds illfortune;evil exactlyonce. Validator0errors, originalbaseline metadata/strokes and everyruntimehash rechecked; not independentreviewer retrieval."},
        ],
        "optionalDispositions": [
            {"claim": "Add strongerword comparison against不作 and cite凶cropfailure sense",
             "reportedBy": ["Claude Optional1"], "status": "optional",
             "decision": "Noedit. Current凶explains unfavorable agriculturaloutcome and凶作 explicitlyverypoor; difference from不作 is already scoped. No universal strength ordering introduced."},
            {"claim": "Explain作crop/yield next to the new navigationline",
             "reportedBy": ["Claude Optional2"], "status": "optional",
             "decision": "Noedit. Newlinkedword article supplies verifiedcompound-specifichead sense. Existing作body outside additive navigation remains unchanged; no demonstrated teachinggap."},
            {"claim": "Qualify凶器 as oftencrime/murderweapon",
             "reportedBy": ["Claude Optional3"], "status": "optional",
             "decision": "Noedit. Dangerous/lethalweapon matches fullJMdict1591540. No demonstrated incorrectrestriction or requirement for a newfrequencyclaim."},
        ],
        "modelContributionComparison": {
            "shared": "Bothinitials accepted complete凶/凶作 and additive作line, sole raw/selectedreading/emptykun, agriculturalnoun/verypooryield/notnecessaryzeroyield/famine/badwork, naturalexamples/translations, compound-specific作crop/yield, mnemonic,3wrongkanjilabels,1directguard,2mappedpairs andnative/quizpoollimitations.",
            "claudeUnique": "Three optionalclarity/expansion proposals; no verifiedmandatorydefect. Explicitlargerpoolhypothesis overlapsGPTLimits, not a uniquediscovery.",
            "gptUnique": "No uniqueverifiedteachingdefect. Transparently reported unnecessaryserialoverlappingtailreads/truncatedresponses; execution verifies completeinitialread and no missingassignedscope.",
            "limits": "Common matchedsnapshot/task/sourceaccess; no defectquota or generalmodelranking. Allsectionsincludinghypotheses/optional/limits compared; labeldifferences do not create uniquecontribution.",
        },
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "freshFrozenLexicalPacketsVerified": 2, "frozenInputHashesVerified": 5,
        "completeRawCharacterRecordsVerified": raw_count,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "directWordExclusionPairs": 1,
        "actualHanCount": 23, "nativeFontPending": ["乂", "凵"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "diagnostics": ["Initial coordinator catalog command copilot config help was an unknown-key error, not a denial or settings change. Correct copilot help config exposed and archived actual advertisedmodels; both executed identities verified.",
                        "GPT redundanttailread accounting retained as above; no missingassignedrange, concurrenttool, retry arounddenial or freshreviewrequired."],
        "newNativeOrAndroidClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    assert not (V / "batch-089-reconciliation.json").exists()
    save(V / "batch-089-reconciliation.json", rec)
    ledger["runtimeDraftLimits"] = ledger["limits"]
    ledger.update(status=rec["status"], textualReviewClosed=True, runtimeAccepted=False,
                  reviewClosed=[], published=[], reviewSnapshot=SNAPSHOT,
                  reviewEvidence="docs/n1-reviews/batch-089-reconciliation.json",
                  textuallyResolvedFindings=[], nextAction=NEXT, limits=limits)
    save(S / "batch-089-progress.json", ledger)
    for src, name in [(C / "review-batch-089.py", "batch-089-review-recipe.py"),
                      (Path(__file__), "batch-089-textual-closure-recipe.py")]:
        shutil.copyfile(src, S / name)
    save(S / "execution-629.json", {
        "schemaVersion": 1, "execution": 629, "batch": "089", "teachingSnapshot": SNAPSHOT,
        "status": rec["status"], "reconciliation": "docs/n1-reviews/batch-089-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-089-reconciliation.json"),
        "recipeHashes": {n: sha(S / n) for n in ["batch-089-review-recipe.py", "batch-089-textual-closure-recipe.py"]},
        "checks": receipts, "runtimeHashesReverified": checked, "focusedTestsPassed": 43,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "newAndroidOrNativeClaimed": False, "wholeProjectComplete": False,
        "publishedAdditions": 115, "remainingAdditions": 1113,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "limits": limits,
    })
    print("Textual closure persisted; unchanged runtime hashes verified:", checked)


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != SNAPSHOT and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == review.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    rec = load(V / "batch-089-reconciliation.json")
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    p = load(C / "progress.json")
    original = load(L / "progress-before-629.json")
    assert p["checkpoint"] == 628
    p["execution629StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    cp = {
        "schemaVersion": 1, "execution": 629, "checkpoint": 629, "batch": "089",
        "savedCommit": head, "signature": "G", "initialTeachingSnapshot": SNAPSHOT,
        "status": "continue", "stage": rec["status"],
        "reconciliation": "docs/n1-reviews/batch-089-reconciliation.json",
        "evidence": "docs/n1-sources/execution-629.json",
        "actualInitialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionSupplements": 0, "serialProcessesAndInternalToolsVerified": True,
        "allAssignedPacketRangesReturned": True, "originalReportsPreserved": True,
        "gptRedundantSerialTailReads": 3, "gptTruncatedRedundantTailResponses": 2,
        "bothFirstCallsExactFullPacketReturned": True,
        "initialDistinctCompleteFamilies": 73, "rawCharacterRecords": 6,
        "textualReviewClosed": True, "actionableRemainingTeachingFindings": 0,
        "consequentialUnresolvedTeachingFindings": 0, "runtimeHashesReverified": 8426,
        "focusedTestsPassedThisCheckpoint": 43, "runtimeChanged": False,
        "runtimePublished": False, "runtimeAccepted": False, "newAndroidOrNativeClaimed": False,
        "nativeFontPending": rec["nativeFontPending"], "actualHanCount": 23,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "directWordExclusionPairs": 1,
        "reviewClosed": [], "published": [], "publishedAdditions": 115, "remainingAdditions": 1113,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "dedicatedWorktreesClean": True,
        "originalHistoricalRootKeysCompared": len(original), "allOriginalHistoricalValuesPreserved": True,
    }
    p["execution629CoordinatorCheckpoint"] = cp
    p["batch089TextualReviewCheckpoint"] = dict(cp)
    p.update(checkpoint=629, status="continue", stage=rec["status"], nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    temp = C / "progress.629-checkpoint.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")
    assert load(C / "progress.json") == p
    print("Checkpoint629 saved:", head, "; historical root values preserved:", len(original))


if __name__ == "__main__":
    {"close": close, "checkpoint": checkpoint}[sys.argv[1]]()
