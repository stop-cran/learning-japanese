import copy
import gzip
import importlib.util
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("review090", C / "review-batch-090.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
review = module.review
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
SNAPSHOT = review.SNAPSHOT
STAGE = "textually-review-closed-awaiting-fresh-android"
NEXT = (
    "SAME090 fresh non-skipped sibling Android RealContentTest THREE cases and RareHanTest ONE case "
    "against THIS content tree; preserve exact XML/provenance and normally signed local evidence, then yield. "
    "Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d atop unchanged productionf9b59a2 "
    "is not latest app main. Explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot "
    "and ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, one Gradle worker and "
    "quoted '-Pkotlin.compiler.execution.strategy=in-process'. Parent19008 already owns runner.lock; "
    "NO child reacquisition/delete/unlock or parent recovery wrapper copy. Keep exact signed-head/checkpoint/"
    "wholly-clean-worktree/verified-parent-ancestry checks; preserve/report/yield actual new denial, signing "
    "hang or uncertain ownership. Textual090 closed with two serial blind families on unchangede044e953; "
    "no actionable defect or consequential unresolved teaching claim. Rawトウ/かたな/そり in order, "
    "onlyトウ/かたな selected with own linked rows; source-onlyそり not inferred from jukujikun剃刀. "
    "New刀/日本刀 and exact four reused navigation/component diffs reviewed; traditional Japanese sword "
    "noun, neutral museum/photo sentences, lexical日本/Japan modifier plus刀/sword, bothにほんとう/"
    "にっぽんとう without frequency ranking or universal sound-change/shape rule. Five allmappedpairs/"
    "ten directions, one direct日本刀/刀guard. Both originals used exactly one fullpacketview; actual "
    "models/process exit/read coverage verified, no overlaps/truncation/recoveryreads. Later native "
    "requires all18scopedHan/fourproductionfonts, two pinned drawingstrokes, one onとう and one kunかたな "
    "key/noそり, both newarticles/SystemBack/offline plus affectedreusedroutes, actualN1/All production "
    "choices and fullarchive productionContentSync ONCE with terminal case0; no guard or heap increase. "
    "All18present in bundled maincmaps is not native legibility acceptance. Both original sessions "
    "retained for dependent visuals, no newblindcredit. All original source/baseline/link/reading/"
    "twofamily/native/currentmain-normalmerge/re-review/checks/normal-signing/owner-fastforward/"
    "terminalCI/EVERYimmutableZIPentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "media/path/ownerissue gates remain. Published116/1228,1112remaining unchanged; physicalphone/"
    "generalrelease/whole-set outstanding. No091, native/reviewer/publication or second runner in next host checkpoint."
)


def records():
    result = {}
    prior = None
    for label, model in review.MODELS.items():
        prefix = f"batch-090-initial-{label}"
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
        assert review.absent(record["launcherPid"])
        if prior:
            assert prior < record["startedAt"]
        prior = record["completedAt"]
        result[label] = {
            **{key: record[key] for key in [
                "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
                "requestedModel", "actualModels", "snapshot", "reportSha256", "rawExecutionSha256",
            ]},
            "report": prefix + ".md", "execution": prefix + "-execution.json",
            "coverage": prefix + "-coverage.json", "allAssignedRangesReturned": True,
            "toolCalls": 1, "observedToolOverlaps": 0, "firstCallExactFullPacketReturned": True,
        }
    return result


def checks():
    review.frozen()
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "090"],
        "tests": [
            sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
            "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources",
        ],
    }
    for name, command in commands.items():
        path = V / f"batch-090-textual-review-{name}-638.txt"
        assert not path.exists()
        with path.open("wb") as stream:
            result = subprocess.run(command, cwd=R / "tools" if name == "tests" else R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        print(name, "passed")


def close():
    review.frozen()
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract

    processes = records()
    assert review.PACKET.read_bytes() == (V / review.PACKET.name).read_bytes()
    ledger = load(S / "batch-090-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    mechanical = audit(R, "090")
    assert mechanical["dictionaryFamilies"] == 207
    assert mechanical["changedReusedArticles"] == 4 and mechanical["newWords"] == 1
    source = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in source["inputs"].items():
        assert sha(C / "inputs" / name) == info["sha256"]
        assert (C / "inputs" / name).stat().st_size == info["bytes"]
    dictionary = C / "inputs" / "n1-implementation-JMdict_e.gz"
    compressed = dictionary.read_bytes()
    assert review.hashlib.sha256(gzip.decompress(compressed)).hexdigest() == source["jmdict"]["xmlSha256"]
    for packet in ledger["dictionaryPackets"]:
        selection = load(S / packet["selection"])
        assert extract(compressed, source["inputs"][dictionary.name]["sha256"],
                       selection["entryIds"]) == (S / packet["xml"]).read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert review.hashlib.sha256(kd).hexdigest() == source["kanjidic2"]["xmlSha256"]
    chars = {entry.findtext("literal"): entry for entry in ET.fromstring(kd).findall("character")}
    canonical = lambda entry: ET.canonicalize(ET.tostring(entry, encoding="unicode"), strip_text=True)
    raw_count = 0
    for name in ["batch-090-kanjidic2.xml", "batch-090-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(chars[entry.findtext("literal")])
            raw_count += 1
    assert raw_count == 8
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
    assert pairs == {("刀", "words/刀.md"), ("刀", "words/剃刀.md"), ("刀", "words/日本刀.md"),
                     ("日", "words/日本刀.md"), ("本", "words/日本刀.md")}
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / (char + ".md")).read_text(encoding="utf-8")
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
    assert checked == 8429 and manifest["contentVersion"] == "ceee0f79a6d394df"
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    assert [path.stem for path in (R / "kanji").glob("*.md")
            if any(word in metadata(R, "kanji/" + path.name)["title"].lower()
                   for word in ["sword", "blade", "saber", "sabre", "knife"])] == ["刀"]
    receipts = {}
    for name in ["validate", "manifest", "audit", "tests"]:
        path = V / f"batch-090-textual-review-{name}-638.txt"
        text = path.read_text(encoding="utf-8-sig")
        if name == "validate":
            assert text.strip() == "0 error(s)"
        elif name == "tests":
            assert "Ran 43 tests" in text and text.rstrip().endswith("OK")
        elif name == "audit":
            assert json.loads(text) == mechanical
        receipts[name] = {"path": path.relative_to(R).as_posix(), "sha256": sha(path)}
    reviewed = ["kanji/刀.md", "words/日本刀.md", "words/刀.md", "words/剃刀.md", "kanji/日.md", "kanji/本.md"]
    limits = [
        "Textual closure only. Fresh non-skipped Android/native/fourfont/visual/combinedmain/signing/publication gates pending; runtime not accepted or published.",
        "Both actual families received identical248434byte6161line packet:207completeJMdictfamilies,8rawcharacters,14completearticles. Both used one fullpacketview with exact fulltext returned/no truncation/overlap. Byte access is not comprehension or equal fresh-read depth; Claude explicitly did not mechanically count194lexicalfamilies, coordinator verified packet207=194+13.",
        "Original reports preserved verbatim before reconciliation; blind initial reviewers received no other report or author adjudication. No teaching fix needed; zero dependent textual confirmations. Original sessions retained for dependent visuals.",
        "Supplied publicDaijisen/Nikkoku/Jitsu/encyclopedia text is coordinator extraction from archivedHTML, not independentupstream retrieval or verification of every historical/metallurgy assertion. 日本刀 lexical headings1-19 only, not encyclopedia remainder. No verified historical glyph/phonetic/frequency claims adopted.",
        "Rawトウ/かたな/そり retained in order; onlyトウ/かたな selected with own linked rows. Source-onlyそり not inferred nonexistent/archaic or allocated fromjukujikun剃刀. Japan lexicalmodifier, bothwholewordreadings, no inferredwordlevel.",
        "Fiveallmappedpairs/tendirections include reused刀/剃刀 and日/本. One direct日本刀/刀guard, not transitiveclique or universal livepool certification. Allthree curatedwrongcardsN1available; actualN1/All production and broader custom/randompools remain uncertified. Alternate documented word reading is explanatory, not a second primary wordquiz key.",
        "All18scopedHan present in mainbundledcmaps; nativefourfont/twostroke/drawing/SystemBack/offline acceptance still required. Cmap presence not legibility. Inheritedall40pilotfont evidence stayshistorical.",
        "QualifiedTESTONLYAndroid1c1b7bf4 atop unchangedproductionf9b59a2 is not latestappmain. Compatibleclientf9b59a2+ required; oldclients ignorecuration/wordguards. Physicalphone/generalrelease/whole-set outstanding.",
        "Published116/1228,1112acceptanceremainder unchanged. Sixseparate earlierN2sourcemembers保案派第策結 are not acceptedissue60 additions or candidates toduplicate/relevel; separate妖exception retained.",
        "Alloriginalnormalmerge/substantiveteachingreview/validation/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemedia/safepaths/ownerissue gates remain; no guardincrease or algorithmchange.",
        "Liveparent19008 retainsrunner.lock; nochildacquisition/delete/unlock. Approvedcontrolhelpers/committedsourcepackets/frozenworkspaceinputs only; nooptionalhistoricalsessionhelper access, policychange or actualnewpermissiondenial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 638, "batch": "090", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False,
        "reviewedRuntimeHashes": {name: sha(R / name) for name in reviewed + ["strokes/刀.json", "manifest.json"]},
        "initialModels": list(review.MODELS.values()), "processes": processes,
        "serialReviewerProcessesVerified": True, "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": review.PACKET.stat().st_size, "initialPacketLines": 6161,
        "initialDistinctCompleteFamilies": 207, "rawCharacterRecords": 8,
        "completeArticleBodiesSupplied": 14, "newArticleBodies": 2, "changedReusedBodies": 4,
        "originalSessionSupplements": 0,
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN",
                   "scope": "complete new article" if index < 2 else "exact navigation/component diff only"}
            for index, name in enumerate(reviewed)
        },
        "findings": [],
        "hypothesisDispositions": [{
            "claim": "Other sword/blade cards or larger automatic pools might create fallback overlap",
            "reportedBy": ["Claude Hypotheses; GPT Limits widerpool caveat"],
            "status": "unresolved", "category": "pending-runtime-acceptance-not-established-textual-defect",
            "evidence": "Fresh coordinator exact allcurrentkanjititle scan finds only刀 matching sword/blade/saber/sabre/knife; 刃/剣 currently absent. Allthree curatedwrongcardsN1available, 力/切alreadyhave3curatedchoices. No demonstrated defaultbadquestion; no universal futurepool safety.",
            "decision": "No inventedtextualfix. Mandatory nativeN1/All productionacceptance retained; widerchanged/custompools explicitlyuncertified.",
        }],
        "optionalDispositions": [
            {"claim": "Harmonize new刀startsinside versus unchanged力startson wording",
             "reportedBy": ["Claude Optional1"], "status": "optional",
             "decision": "Noedit. New刀correctlydescribes pinnedSVG andcrossingcontrast; unchanged力outside exactdiffnotrewriteassignment. Bothreviewers accept currentnewcontrast; no consequential inconsistency established."},
            {"claim": "Mentionとう-only knife-money sense", "reportedBy": ["Claude Optional2"],
             "status": "optional", "decision": "Noedit. Otherとう-onlysenses already illustrate restriction; source-onlyfullfamily preserved, exhaustivelexicalcoverage notrequired."},
            {"claim": "Add cited pictographic origin based on字通", "reportedBy": ["Claude Optional3"],
             "status": "optional", "decision": "Noedit. Explicitmodernshapemnemonic/structure-unclassified allowed; no need tobroadenhistoricalassertions or imply originalglyphimages inspected."},
            {"claim": "Add短刀/木刀 toトウrow", "reportedBy": ["Claude Optional4"],
             "status": "optional", "decision": "Noedit. Ownlinked日本刀already establishes selectedreading; noextraarticle/readingquota."},
        ],
        "modelContributionComparison": {
            "shared": "Bothaccept complete刀/日本刀 plus all4changedpassages, exactraw/selectedreadings/source-onlyqualification, noun/examples/translations, lexical日本modifier/bothwholewordreadings/category/tool distinctions, labelledmnemonic/力contrast,3wronglabels,1directguard and5mappedpairs. Both disclose livepool/native/phone limits.",
            "claudeUnique": "Four optionalproposals, noverifiedmandatorydefect. Explicitlargerpoolhypothesis overlapsGPTLimits, notuniquediscovery. Reportselflimits mechanicalfamilycount; coordinatorpacketcountnotmisrepresented asreviewercount.",
            "gptUnique": "No uniqueverifiedteachingdefect. Runtimecompatibility/native/widerpool caveats overlapClaudeLimits; no unique contribution credited from labels or placement.",
            "limits": "Common matchedsnapshot/task/sourceaccess; no defectquota or generalmodelranking. Allsectionsincludinghypotheses/optional/limits compared; labeldifferences do not create uniquecontribution.",
        },
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "freshFrozenLexicalPacketsVerified": 2, "frozenInputHashesVerified": 5,
        "completeRawCharacterRecordsVerified": raw_count,
        "allMappedReciprocalPairs": 5, "directedLinksVerified": 10, "directWordExclusionPairs": 1,
        "actualHanCount": 18, "nativeFontPending": [],
        "nativeFontQualification": "No mainbundledcmap absences among18Han; fresh nativefourfontlegibility still pending.",
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "newNativeOrAndroidClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    assert not (V / "batch-090-reconciliation.json").exists()
    save(V / "batch-090-reconciliation.json", rec)
    ledger["runtimeDraftLimits"] = ledger["limits"]
    ledger.update(status=STAGE, textualReviewClosed=True, runtimeAccepted=False,
                  reviewClosed=[], published=[], reviewSnapshot=SNAPSHOT,
                  reviewEvidence="docs/n1-reviews/batch-090-reconciliation.json",
                  textuallyResolvedFindings=[], nextAction=NEXT, limits=limits)
    save(S / "batch-090-progress.json", ledger)
    shutil.copyfile(Path(__file__), S / "batch-090-textual-closure-recipe.py")
    save(S / "execution-638.json", {
        "schemaVersion": 1, "execution": 638, "batch": "090", "teachingSnapshot": SNAPSHOT,
        "status": STAGE, "reconciliation": "docs/n1-reviews/batch-090-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-090-reconciliation.json"),
        "recipeHashes": {"docs/n1-sources/batch-090-textual-closure-recipe.py": sha(S / "batch-090-textual-closure-recipe.py"),
                        **{(V / name).relative_to(R).as_posix(): sha(V / name)
                           for name in ["review-batch-090.py", "batch-090-serial-review-base-recipe.py"]}},
        "checks": receipts, "runtimeHashesReverified": checked, "focusedTestsPassed": 43,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "newAndroidOrNativeClaimed": False, "wholeProjectComplete": False,
        "publishedAdditions": 116, "remainingAdditions": 1112,
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
    rec = load(V / "batch-090-reconciliation.json")
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    assert not git("diff", SNAPSHOT, head, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    records()
    progress = load(C / "progress.json")
    original = load(L / "progress-before-638.json")
    assert progress["checkpoint"] == 637
    progress["execution638StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    cp = {
        "schemaVersion": 1, "execution": 638, "checkpoint": 638, "batch": "090",
        "savedCommit": head, "signature": "G", "initialTeachingSnapshot": SNAPSHOT,
        "status": "continue", "stage": STAGE,
        "reconciliation": "docs/n1-reviews/batch-090-reconciliation.json",
        "evidence": "docs/n1-sources/execution-638.json",
        "actualInitialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionSupplements": 0, "serialProcessesAndInternalToolsVerified": True,
        "allAssignedPacketRangesReturned": True, "originalReportsPreserved": True,
        "bothOneCallExactFullPacketReturned": True, "initialDistinctCompleteFamilies": 207,
        "rawCharacterRecords": 8, "textualReviewClosed": True,
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "runtimeHashesReverified": 8429, "focusedTestsPassedThisCheckpoint": 43,
        "runtimeChanged": False, "runtimePublished": False, "runtimeAccepted": False,
        "newAndroidOrNativeClaimed": False, "actualHanCount": 18,
        "allMappedReciprocalPairs": 5, "directedLinksVerified": 10, "directWordExclusionPairs": 1,
        "reviewClosed": [], "published": [], "publishedAdditions": 116, "remainingAdditions": 1112,
        "lastPublishedCommit": progress["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "dedicatedWorktreesClean": True,
        "originalHistoricalRootKeysCompared": len(original), "allOriginalHistoricalValuesPreserved": True,
    }
    progress["execution638CoordinatorCheckpoint"] = cp
    progress["batch090TextualReviewCheckpoint"] = dict(cp)
    progress.update(checkpoint=638, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[key] == value for key, value in original.items() if key not in allowed)
    temp = C / "progress.638-checkpoint.tmp"
    assert not temp.exists()
    save(temp, progress)
    assert load(temp) == progress
    temp.replace(C / "progress.json")
    print("Checkpoint638 saved:", head, "; historical root values preserved:", len(original))


if __name__ == "__main__":
    {"checks": checks, "close": close, "checkpoint": checkpoint}[sys.argv[1]]()
