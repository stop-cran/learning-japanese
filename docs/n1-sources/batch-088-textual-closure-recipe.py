import copy
import gzip
import importlib.util
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("review088", C / "review-batch-088.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
SNAPSHOT = review.SNAPSHOT
NEXT = (
    "SAME088 fresh non-skipped sibling Android RealContentTest THREE cases and RareHanTest ONE case "
    "against THIS content tree; preserve exact XML/provenance and normally signed local evidence, then yield. "
    "Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d atop unchanged productionf9b59a2 "
    "is not latest app main. Explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot "
    "and ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, one Gradle worker and "
    "quoted '-Pkotlin.compiler.execution.strategy=in-process'. Parent19008 already owns runner.lock; "
    "NO child reacquisition/delete/unlock or parent recovery wrapper copy. Keep exact signed-head/checkpoint/"
    "wholly-clean-worktree/verified-parent-ancestry checks; preserve/report/yield actual new denial, signing "
    "hang or uncertain ownership. Textual088 closed with two serial blind families on unchanged42077c31; "
    "no actionable defect or consequential unresolved teaching claim. All four raw readings/order retained: "
    "onガイ/カイ, undottedkunかちどき/やわらぐ; onlyガイselected, explicitkun[]. "
    "Source-only character glosses remain distinct from 勝どき/勝鬨/和らぐ and 凱風がいふう. "
    "One all-mapped pair/two directions, four direct word guards, no changed reused teaching. "
    "Later native gate requires all27 scoped Han especially几/豈/鬨, four production font families/system "
    "fallback, twelve-stroke drawing, singlequeuedkeyがい, both new article/SystemBack/offline routes and "
    "full archive production ContentSync ONCE with terminal case0; no guard or heap increase. Actual "
    "N1/All production choices remain required despite allthree curated wrongcards being N1-available. "
    "Both original review sessions retained for dependent visuals, no new blind credit. All original "
    "source/baseline/link/reading/twofamily/native/currentmain-normalmerge/re-review/checks/normal-signing/"
    "owner-fastforward/terminalCI/EVERYimmutableZIPentryhash/original18000entries42MiBcompressed80MiBinflated"
    "56MiBretained/media/path/ownerissue gates remain. Published114/1228,1114remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No089, native/reviewer/publication or second runner "
    "in next host checkpoint."
)


def records():
    result = {}
    prior = None
    for label, model in review.MODELS.items():
        prefix = f"batch-088-initial-{label}"
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
        assert subprocess.run(
            ["pwsh", "-NoProfile", "-Command",
             f"if (Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
            capture_output=True,
        ).returncode == 0
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
    ledger = load(S / "batch-088-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    mechanical = audit(R, "088")
    assert mechanical["dictionaryFamilies"] == 25
    assert mechanical["changedReusedArticles"] == 0 and mechanical["newWords"] == 1
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
    for name in ["batch-088-kanjidic2.xml", "batch-088-comparison-kanjidic2.xml"]:
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
    assert pairs == {("凱", "words/凱旋.md")}
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
    assert checked == 8423 and manifest["contentVersion"] == "afff40af0e155dbe"
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    title = metadata(R, "kanji/凱.md")["title"]
    assert sum(metadata(R, "kanji/" + p.name)["title"] == title for p in (R / "kanji").glob("*.md")) == 1
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "tests-invocation-diagnostic"]:
        name = (f"batch-088-textual-review-tests-620-invocation-diagnostic.txt"
                if stem == "tests-invocation-diagnostic" else f"batch-088-textual-review-{stem}-620.txt")
        src = C / name
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
    reviewed = ["kanji/凱.md", "words/凱旋.md"]
    limits = [
        "Textual closure only. Fresh non-skipped Android/native/fourfont/visual/combinedmain/signing/publication gates pending; runtime not accepted or published.",
        "Both actual model families independently received identical141101byte2665line packet with25distinct completeJMdictfamilies,6rawcharacters,14completearticlebodies including2new and0changedreuseddiffs. Each returned one exact fullpacketview, no truncation/tooloverlap/unfinishedtool. Bytes do not prove comprehension or equivalent fresh-read depth; Claude's rough2620line estimate is retained in its originalreport.",
        "Original reports preserved verbatim. No author adjudication or other report supplied to initial reviewers. No teaching fix needed; zero dependent textual confirmations, original sessions retained for later visuals.",
        "PublicDaijisen/Jitsu/Nikkoku text extracted by coordinator from committedHTML; formatting/links stripped, imageplaceholders retained. Not independentupstream retrieval, historical-glyphinspection or contemporaryfrequencymeasurement.",
        "All four rawreadings/order preserved: onガイ/カイ and undottedkunかちどき/やわらぐ. Onlyガイselected, explicitkun[]. Characterdictionary glosses are not manufactured ordinary wordspellings. No frequency/name-only inference or wordlevel inferred.",
        "Oneallmappedpair/twodirections, noactivatedbaselinepair/reusedteaching. Fourdirectguards not transitivecliques or universal livepool safety. Allthree curatedwrongcards N1-available; actualN1/All production and broader custom/randompools remain uncertified.",
        "All27scopedHan especially几/豈/鬨 missingmainbundledcmap needfreshnativefourfont/systemfallback legibility; cmapabsence notglyphfailure. Twelvepinnedstrokes unchanged. Inheritedall40font evidence stayshistorical.",
        "QualifiedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9b59a2 is not latestappmain. Compatibleclientf9b59a2+ required; oldclients ignorecuration/wordguards. Physicalphone/generalrelease/whole-set outstanding.",
        "Published114/1228,1114acceptanceremainder unchanged. Sixseparate earlierN2sourcemembers保案派第策結 are not acceptedissue60 additions or candidates toduplicate/relevel; separate妖exception retained.",
        "Alloriginalnormalmerge/substantiveteachingreview/validation/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemedia/safepaths/ownerissue gates remain; no guardincrease or algorithmchange.",
        "Liveparent19008 retainsrunner.lock; nochildacquisition/delete/unlock. Approvedcontrolhelpers/committedsourcepackets/frozenworkspaceinputs only; nooptionalhistoricalsessionhelper access, policychange or actualnewpermissiondenial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 620, "batch": "088",
        "status": "textually-review-closed-awaiting-fresh-android",
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False,
        "reviewedRuntimeHashes": {n: sha(R / n) for n in reviewed + ["strokes/凱.json", "manifest.json"]},
        "initialModels": list(review.MODELS.values()), "processes": processes,
        "serialReviewerProcessesVerified": True, "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": review.PACKET.stat().st_size, "initialPacketLines": 2665,
        "initialDistinctCompleteFamilies": 25, "rawCharacterRecords": 6,
        "completeArticleBodiesSupplied": 14, "newArticleBodies": 2, "changedReusedBodies": 0,
        "originalSessionSupplements": 0,
        "verdicts": {n: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"} for n in reviewed},
        "findings": [],
        "hypothesisDispositions": [
            {"claim": "Fallback 勝victory can overlap with 凱triumph", "reportedBy": ["Claude Limits", "GPT Limits broader-pool caveat"],
             "status": "unresolved", "category": "pending-native-production-acceptance-not-article-defect",
             "evidence": "Actual 凱distractors凡/凸/凹 are all N1-available; 勝/歌already have three curatedwrongcards. No defaultmissing-slot or demonstratedbadquestion established. Larger/random/custompools not certified.",
             "decision": "No inventedtextualfix. Actual N1/All production choices remain mandatory before runtimeacceptance/publication."},
            {"claim": "Destinationへ statement lacks a direct 凱旋へ example in the suppliedpacket",
             "reportedBy": ["Claude Limits; GPT accepts construction"],
             "status": "resolved", "confidence": "high for directional-particle construction, not phrasefrequency",
             "evidence": "Daijisen establishes directionalreturn and actual故国に凱旋する. Coordinator inspected Tofugu Particleへ, sections Basics and PhysicalDestinations:へmarks destination/direction and is followed by directional-movementverbs. This supports productive construction, not independentattestation or unrestrictedに/へsubstitution.",
             "source": "https://www.tofugu.com/japanese-grammar/particle-he/",
             "sourceAccess": "Coordinator web_fetch on2026-11-07; inspected first12000characters through relevant complete sections; laterpage truncated. Not supplied to initialreviewers or claimed as their retrieval.",
             "decision": "No established defect; destinationへ is a standard directional-return construction. No universal substitution rule or new naturalness/frequency claim added."},
            {"claim": "Whole-corpus kanjititle uniqueness and comparison山card not independentlychecked",
             "reportedBy": ["Claude Limits"], "status": "resolved",
             "resolution": "Coordinator fresh allactualkanjititle scan finds victorysong;triumph exactlyonce. Validator0errors, baseline山metadata and everyruntimehash rechecked. Mnemonic uses only actual山shape/meaning; no change or independentreviewofentire山article claimed."},
            {"claim": "Possible uncarded帰国/帰還 could overlap in a futurepool", "reportedBy": ["Claude Limits"],
             "status": "optional", "decision": "No newarticle/pool requirement invented. Currentguards use existing exactIDs and actual articles; broaderfuture/custompools remain explicitlyuncertified."},
        ],
        "optionalDispositions": [
            {"claim": "Clarify the compoundsabove as 凱旋and凱歌", "reportedBy": ["Claude"],
             "status": "optional", "decision": "Noedit. Samearticle already explicitly separates凱風and forbids forcingvictory into it atlines24-26; no demonstrated teachingdefect."},
            {"claim": "Use gentlesoutherlywind instead of southerlywind", "reportedBy": ["Claude"],
             "status": "optional", "decision": "Noedit. Currentgloss matches completeJMdict1791660; preceding sentence already explains calm/gentlecharactersense. No expandedfrequency or lexicalclaim required."},
            {"claim": "Replace unsuccessfulreturn/fixedopposite sentence with nofixedantonym", "reportedBy": ["Claude"],
             "status": "optional", "decision": "Noedit. Currentsentence avoids inventing a fixedopposite; suggested universalnofixedantonym would exceed inspected evidence."},
        ],
        "modelContributionComparison": {
            "shared": "Bothinitials accepted bothcompletearticles, fourrawreadings/allocation/source-onlyboundaries, selectedガイ/kun[], intransitivesuru/nominalを/にへ, militarysportsperformanceextension, compound-specific旋return,3wrongkanjilabels,4directguards,1mappedpair andnative/quizpoollimitations.",
            "claudeUnique": "Three optionalclarity/polishsuggestions and explicitsupplementalへevidencelimit; no verifiedmandatorydefect. Titleuniqueness mechanicallychecked; nativepoolrisk overlapsGPTLimits, not a uniquefinding.",
            "gptUnique": "No uniqueverifieddefect; detailedsupportingchecks, substantiveconclusions shared.",
            "limits": "Common matchedsnapshot/task/sourceaccess; no defectquota or generalmodelranking. Allsectionsincludinghypotheses/optional/limits compared; labeldifferences do not create uniquecontribution.",
        },
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "freshFrozenLexicalPacketsVerified": 2, "frozenInputHashesVerified": 5,
        "completeRawCharacterRecordsVerified": raw_count,
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "directWordExclusionPairs": 4,
        "actualHanCount": 27, "nativeFontPending": ["几", "豈", "鬨"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "diagnostics": ["Initial unittest package invocation lacked tools in module search path; four import errors before tests. Original diagnostic archived. Explicit workspace tools PYTHONPATH then ran43tests successfully; no dependency installed or code modified."],
        "newNativeOrAndroidClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    assert not (V / "batch-088-reconciliation.json").exists()
    save(V / "batch-088-reconciliation.json", rec)
    ledger["runtimeDraftLimits"] = ledger["limits"]
    ledger.update(status=rec["status"], textualReviewClosed=True, runtimeAccepted=False,
                  reviewClosed=[], published=[], reviewSnapshot=SNAPSHOT,
                  reviewEvidence="docs/n1-reviews/batch-088-reconciliation.json",
                  textuallyResolvedFindings=[], nextAction=NEXT, limits=limits)
    save(S / "batch-088-progress.json", ledger)
    for src, name in [(C / "review-batch-088.py", "batch-088-review-recipe.py"),
                      (Path(__file__), "batch-088-textual-closure-recipe.py")]:
        shutil.copyfile(src, S / name)
    save(S / "execution-620.json", {
        "schemaVersion": 1, "execution": 620, "batch": "088", "teachingSnapshot": SNAPSHOT,
        "status": rec["status"], "reconciliation": "docs/n1-reviews/batch-088-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-088-reconciliation.json"),
        "recipeHashes": {n: sha(S / n) for n in ["batch-088-review-recipe.py", "batch-088-textual-closure-recipe.py"]},
        "checks": receipts, "runtimeHashesReverified": checked, "focusedTestsPassed": 43,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "newAndroidOrNativeClaimed": False, "wholeProjectComplete": False,
        "publishedAdditions": 114, "remainingAdditions": 1114,
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
    rec = load(V / "batch-088-reconciliation.json")
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    p = load(C / "progress.json")
    original = load(L / "progress-before-620.json")
    assert p["checkpoint"] == 619
    p["execution620StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    cp = {
        "schemaVersion": 1, "execution": 620, "checkpoint": 620, "batch": "088",
        "savedCommit": head, "signature": "G", "initialTeachingSnapshot": SNAPSHOT,
        "status": "continue", "stage": rec["status"],
        "reconciliation": "docs/n1-reviews/batch-088-reconciliation.json",
        "evidence": "docs/n1-sources/execution-620.json",
        "actualInitialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionSupplements": 0, "serialProcessesAndInternalToolsVerified": True,
        "allAssignedPacketRangesReturned": True, "originalReportsPreserved": True,
        "initialDistinctCompleteFamilies": 25, "rawCharacterRecords": 6,
        "textualReviewClosed": True, "actionableRemainingTeachingFindings": 0,
        "consequentialUnresolvedTeachingFindings": 0, "runtimeHashesReverified": 8423,
        "focusedTestsPassedThisCheckpoint": 43, "runtimeChanged": False,
        "runtimePublished": False, "runtimeAccepted": False, "newAndroidOrNativeClaimed": False,
        "nativeFontPending": rec["nativeFontPending"], "actualHanCount": 27,
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "directWordExclusionPairs": 4,
        "reviewClosed": [], "published": [], "publishedAdditions": 114, "remainingAdditions": 1114,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "dedicatedWorktreesClean": True,
        "originalHistoricalRootKeysCompared": len(original), "allOriginalHistoricalValuesPreserved": True,
    }
    p["execution620CoordinatorCheckpoint"] = cp
    p["batch088TextualReviewCheckpoint"] = dict(cp)
    p.update(checkpoint=620, status="continue", stage=rec["status"], nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    temp = C / "progress.620-checkpoint.tmp"
    assert not temp.exists()
    save(temp, p)
    assert load(temp) == p
    temp.replace(C / "progress.json")
    assert load(C / "progress.json") == p
    print("Checkpoint620 saved:", head, "; historical root values preserved:", len(original))


if __name__ == "__main__":
    {"close": close, "checkpoint": checkpoint}[sys.argv[1]]()
