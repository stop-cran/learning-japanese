import copy
import gzip
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("review095", C / "review-batch-095.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.review
R, A, S, V, L = r.R, r.A, r.S, r.V, r.L
load, sha, git = r.load, r.sha, r.git
SNAPSHOT = r.SNAPSHOT
STAGE = "batch-095-textual-review-closed-awaiting-android-native"
NEXT = (
    "SAME095 fresh Android checkpoint next; textual closure ONLY on signed8c4e1650. "
    "Both serial blind actual ClaudeOpus5.5 and GPT6.1Sol initial reviews returned complete "
    "identical packet and found no actionable textual defect; optional wording/example "
    "suggestions not adopted, no teaching change or changed-passage confirmation needed. "
    "Run fresh non-skipped THREE RealContentTest and ONE RareHanTest against THIS sibling; "
    "qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Use explicit "
    "JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot and "
    "ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, oneGradleworker "
    "and quoted '-Pkotlin.compiler.execution.strategy=in-process'; inspect terminal test reports "
    "and actual sibling path, no skip assumptions. Then fresh fullarchive productionContentSync "
    "ONCE/native N1/All production choices and THREE directguards解剖/分析,解剖/分解,解剖/検査, "
    "onlyぼう reading/no kun, ten-stroke drawing, complete剖/解剖 and reciprocal解 articles, "
    "SystemBack/offline/all32Han/fourfonts with fresh safe port/device ownership checks; "
    "亻/刂/阝 cmap absence is NOT glyphfailure. Preserve exact fixture/hash and actual terminalcase0; "
    "no heap/archiveguard increase, preflight doubleparse or shared-device interference. "
    "Original Claude ede78c28-e889-47b5-be0b-21533da61551 then GPT "
    "ee7498e0-d3ad-46bf-bbc9-82761892cab0 need serial bounded rendered confirmations; current "
    "textualreview is not native/phone/live-pool acceptance. All original combined-current-main/"
    "nonrewritingmerge/changedteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutableZIPmanifestentryhash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/"
    "media/path/verifiedownerissue gates remain. Parent19008 retains runner.lock throughout child "
    "lifetime: NO child acquire/delete/unlock. Approved control/committed packets/frozen inputs "
    "only; no optional historical-session helper access. Preserve/report/yield actual new denial, "
    "signing hang or uncertain ownership. Published121/1228 and1107acceptanceremainder unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No096, unreviewedpush or secondrunner."
)


def save(path, value):
    temp = path.with_suffix(path.suffix + ".691.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def processes():
    result, previous = {}, None
    for label, model in r.MODELS.items():
        prefix = f"batch-095-initial-{label}"
        record = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert record["snapshot"] == SNAPSHOT
        assert record["exitCode"] == 0 and record["actualModels"] == [model]
        assert record["usageCurrentModel"] == model
        assert record["availableTools"] == ["view"] and "--available-tools=view" in record["command"]
        assert record["multiToolResponseCount"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert coverage["allAssignedRangesReturned"]
        assert len(record["toolCalls"]) == 1
        call = record["toolCalls"][0]
        assert call["name"] == "view" and call["success"]
        assert call["arguments"] == {"path": str(r.PACKET), "forceReadLargeFiles": True}
        assert call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
        assert sha(V / (prefix + ".md")) == record["reportSha256"]
        assert sha(V / (prefix + ".jsonl")) == record["rawExecutionSha256"]
        assert r.absent(record["launcherPid"])
        if previous:
            assert previous < record["startedAt"]
        previous = record["completedAt"]
        result[label] = {
            **{key: record[key] for key in [
                "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
                "requestedModel", "actualModels", "snapshot", "reportSha256",
                "rawExecutionSha256",
            ]},
            "report": prefix + ".md", "execution": prefix + "-execution.json",
            "coverage": prefix + "-coverage.json", "allAssignedRangesReturned": True,
            "toolCalls": 1, "observedToolOverlaps": 0,
            "exactFullPacketReturnedInOneCall": True,
            "limits": "Actual complete returned bytes/ranges verified, not comprehension certification.",
        }
    return result


def prepare():
    r.frozen()
    records = processes()
    assert not git("diff", SNAPSHOT, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert r.PACKET.read_bytes() == (V / r.PACKET.name).read_bytes()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 690 and p["batch"] == "095"
    ledger = load(S / "batch-095-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    receipts = {}
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "095"],
        "tests": [
            sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
            "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources",
        ],
        "vocabulary": [sys.executable, "-B", str(R / "tools" / "grammar_vocabulary.py"), "check"],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
    }
    for name, command in commands.items():
        path = V / f"batch-095-textual-review-{name}-691.txt.gz"
        assert not path.exists()
        run = subprocess.run(command, cwd=R / "tools" if name == "tests" else R,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        path.write_bytes(gzip.compress(run.stdout, mtime=0))
        assert run.returncode == 0, (name, run.stdout.decode("utf-8", errors="replace")[-2000:])
        if name == "tests":
            assert b"Ran 43 tests" in run.stdout and run.stdout.rstrip().endswith(b"OK")
        receipts[name] = {
            "path": path.relative_to(R).as_posix(), "sha256": sha(path),
            "uncompressedSha256": r.hashlib.sha256(run.stdout).hexdigest(),
        }
        print(name, "passed", flush=True)

    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from build_manifest import build_manifest, sha256

    mechanical = audit(R, "095")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "463619d79972e9f2"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8441
    for source in load(V / "batch-095-review-dictionary-provenance.json")["sources"]:
        assert sha(Path(source["path"])) == source["sha256"]
    pairs = ledger["allMappedReciprocalPairs"]
    assert pairs == [["剖", "words/解剖.md"], ["解", "words/解剖.md"]]
    for char, word in pairs:
        assert f"(../{word})" in (R / "kanji" / (char + ".md")).read_text(encoding="utf-8")
        assert f"(../kanji/{char}.md)" in (R / word).read_text(encoding="utf-8")
    assert not (R / "words" / "解体.md").exists()
    reviewed = {name: sha(R / name) for name in [
        "kanji/剖.md", "words/解剖.md", "kanji/解.md", "strokes/剖.json", "manifest.json",
    ]}
    rec = {
        "schemaVersion": 1, "execution": 691, "batch": "095", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False,
        "reviewedRuntimeHashes": reviewed,
        "initialModels": list(r.MODELS.values()), "processes": records,
        "confirmations": {}, "originalSessionChangedPassageConfirmationRequired": False,
        "confirmationReason": "No actionable textual defect or teaching edit after the blind reviews. Original sessions remain required for later rendered evidence.",
        "serialReviewerProcessesVerified": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": r.PACKET.stat().st_size, "initialPacketLines": 3124,
        "initialDistinctCompleteFamilies": 37, "lexicalFamilies": 16,
        "comparisonFamilies": 21, "familyOccurrences": 37,
        "rawCharacterRecords": 7, "completeArticleBodiesSupplied": 15,
        "newArticleBodies": 2, "changedReusedPassages": 1,
        "verdicts": {
            name: {
                "correctness": "CLEAN", "scopedCoverage": "CLEAN",
                "textComprehensibility": "CLEAN",
                "scope": scope,
            } for name, scope in [
                ("kanji/剖.md:1-46", "Complete new article; bounded textual review only."),
                ("words/解剖.md:1-39", "Complete necessary new support article; no sourced vocabulary level inferred."),
                ("kanji/解.md:39", "Added reciprocal-navigation line only; complete article supplied as context."),
            ]
        },
        "findings": [],
        "optionalDispositions": [
            {
                "reportedBy": "Claude", "location": "kanji/剖.md:22",
                "claim": "To examine it is narrower than the character-level cutting/splitting gloss.",
                "status": "optional", "decision": "No edit. The passage scopes its explanation to 解剖 and immediately explains the compound. It does not impose examination as an unrestricted condition on all compounds or deny the broader split-open gloss in the title.",
                "evidence": "Actual title and line22; JMdict1199270; Daijisen剖 cutting-open sense and解剖 physical/figurative senses.",
            },
            {
                "reportedBy": "Claude", "location": "kanji/剖.md:34-37",
                "claim": "Add recognition-only 剖検ぼうけん as another ボウ example.",
                "status": "optional", "decision": "No edit; one useful linked support already demonstrates the sole selected reading. An additional recognition example is not required for scoped coverage.",
                "evidence": "Complete JMdict1519040 retained in source packet; existing own linked解剖 reading row.",
            },
            {
                "reportedBy": "Claude", "location": "kanji/剖.md:30,36",
                "claim": "Align figurative analysis versus analysis wording.",
                "status": "optional", "decision": "No edit; the article explicitly qualifies the figurative sense, and the short unqualified gloss is not a contrary claim.",
                "evidence": "Actual explanatory text and JMdict1199270 sense2.",
            },
        ],
        "hypothesisDispositions": [
            {
                "reportedBy": "Claude", "claim": "Possible 解剖/診察 or 解剖/調査 title overlap.",
                "status": "withdrawn", "meaning": "Not established as an actionable textual defect; not a claim that every possible production pool is certified.",
                "decision": "No new guard on this evidence. 診察 medical examination; consultation is specifically clinician assessment/checkup of a patient, not ordinary autopsy/dissection. 調査 investigation; survey concerns obtaining information, not an ordinary synonym for detailed dissection/analysis. Broadly shared purpose alone does not establish a competing displayed answer. GPT considered the same comparisons and established no defect. Judge evidence, not agreement.",
                "evidence": "Complete JMdict1365460 and1429120; actual complete words/診察.md and調査.md; 解剖1199270 and Daijisen exact definitions. Existing 検査 guard conservatively handles its unqualified examination label; no transitive guard assumption.",
                "laterGate": "Actual N1/All production choice inspection and any demonstrated semantic ambiguity remain required.",
            },
            {
                "reportedBy": "Claude", "claim": "If a 解体 card exists, its dissection sense could overlap.",
                "status": "withdrawn",
                "decision": "Actual words/解体.md does not exist in this frozen tree. Complete JMdict1199120 sense3 does overlap, but no current displayed card establishes a missing guard; do not invent a missing-ID exclusion. Future additions require their own label/sense audit.",
                "evidence": "Complete supplied family1199120 and direct current-tree path existence check.",
            },
        ],
        "modelContributionComparison": {
            "shared": "Both substantively inspect and accept whole constructions/examples/translations, physical/figurative boundaries, reading allocation and supplementalホウ, full frozen metadata/curation, radical variant/shape-only mnemonic, three modern wrong-kanji labels, direct wordguards, four links and preserved existing解. Both consider clinical/investigation/dissection comparisons and absence of a displayed解体 card; those are not unique discoveries merely because Claude labels them hypotheses and GPT discusses them under checks.",
            "gptUniqueVerifiedUseful": [],
            "claudeUniqueVerifiedUseful": [],
            "claudeUniqueNonblocking": "Three optional wording/extra-example observations; no demonstrated mandatory teaching defect.",
            "unsupportedSuggestions": "No new mandatory teaching or guard fix established; no inferred frequency, etymology, additional support quota or broad synonym clique.",
            "limits": "Same snapshot/task/source access; equivalent observations across findings/optional/hypotheses/limits compared. This sample is not a model benchmark, equal-depth comprehension certification or native-speaker review.",
        },
        "actionableRemainingFindingGroups": 0,
        "consequentialUnresolvedTeachingClaims": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "previousCompleteSourceBaselineFontStrokeAudit": "docs/n1-sources/batch-095-draft-audit.json",
        "previousCompleteSourceBaselineFontStrokeAuditSha256": sha(S / "batch-095-draft-audit.json"),
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 0,
        "newDirectWordExclusionPairsAppliedInDraft": 3,
        "actualHanCount": 32, "nativeFontPending": ["亻", "刂", "阝"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT,
        "limits": [
            "TEXTUAL closure only, NOT full batch review closure, runtime acceptance or publication; reviewClosed/published arrays remain empty.",
            "Actual models/session IDs/full original reports/executions preserved. Each reviewer made one exact fullpacket read without truncation/missinglines/tooloverlap/unfinishedtool and exited before the next. Returned bytes are not comprehension certification.",
            "Public text is coordinator-supplied committed extraction, not independent upstream retrieval. Gaiji may be omitted; no historical/phonetic reconstruction adopted.",
            "All8441runtimepayloadhashes and teaching bytes unchanged in this checkpoint. Previous complete frozen-source/baseline/stroke/font audit is retained as execution690, not relabelled as fresh full linguistic inspection.",
            "Default-four three kanjichoices accepted textually; actualN1/All/widercustom pools remain runtime gates. Directguards do not establish unrestricted substitution or current production co-occurrence.",
            "All32Han/tenstrokes unchanged; cmapsnotnativelegibility. FreshAndroid/RareHan/native/fourfonts/drawing/reading/N1-All/Back/offline/ContentSyncONCE and dependent original-session rendered review remain.",
            "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Compatibleclientf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
            "Published121/1228 and1107acceptanceremainder unchanged; six separate earlierN2source members保案派第策結 and separate妖exception retained. No096 or wholeprojectcompletion.",
            "All original combined-main/normalmerge/changedteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/originalbudgets/media/path/verifiedownerissue gates remain.",
            "Parent19008 retainsrunner.lock untouched; no childacquire/delete/unlock, optional historical-session helper access, actual new permission denial or secondrunner.",
        ],
    }
    save(V / "batch-095-reconciliation.json", rec)
    ledger["initialDraftLimits"] = copy.deepcopy(ledger["limits"])
    ledger.update(
        status=STAGE, initialReviewSnapshot=SNAPSHOT, reviewedTeachingSnapshot=SNAPSHOT,
        textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False,
        nextAction=NEXT,
    )
    ledger["limits"][0] = rec["limits"][0]
    ledger["quizAudit"]["剖"]["limits"] = "Default-four fallback unnecessary; bounded textual semantic review closed. Actual production N1/All/wider-pool review pending."
    ledger["textualReview"] = {
        "snapshot": SNAPSHOT, "models": rec["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-095-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-095-reconciliation.json"),
        "teachingChanged": False, "textualReviewClosed": True,
        "actionableRemainingFindings": 0, "runtimeAccepted": False,
    }
    ledger["pendingGates"] = [
        "Fresh non-skipped THREE RealContentTest cases/ONE RareHanTest against actual sibling content.",
        "Full productionContentSyncONCE/native N1/All choices/three directguards/onlyぼう/no kun/tenstroke drawing/articles/SystemBack/offline/all32Han/fourfonts; dependent original-session rendered confirmations.",
        "Combined-current-main integration, substantive teaching re-review if changed, allchecks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/unchangedbudgets/verifiedownerissue.",
    ]
    for row in ledger["supportMappings"]:
        row["status"] = "textual-review-closed-awaiting-android-native"
    save(S / "batch-095-progress.json", ledger)
    membership = load(S / "batch-095-membership.json")
    membership["initialDraftLimits"] = copy.deepcopy(membership["limits"])
    membership.update(status=STAGE, initialReviewSnapshot=SNAPSHOT,
                      textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False)
    membership["limits"] = rec["limits"][0]
    save(S / "batch-095-membership.json", membership)
    recipe = S / "batch-095-textual-checkpoint-691.py"
    shutil.copyfile(Path(__file__), recipe)
    shutil.copyfile(C / "preflight-691.ps1", S / "batch-095-textual-preflight-691.ps1.txt")
    save(S / "execution-691.json", {
        "schemaVersion": 1, "execution": 691, "batch": "095", "status": STAGE,
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "startingState": p["execution691StartingState"],
        "reconciliation": "docs/n1-reviews/batch-095-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-095-reconciliation.json"),
        "recipeHashes": {path.relative_to(R).as_posix(): sha(path) for path in [
            recipe, V / "review-batch-095.py", V / "batch-095-serial-review-base-recipe.py",
            S / "batch-095-textual-preflight-691.ps1.txt",
        ]},
        "checks": receipts, "runtimeBytesChanged": False,
        "publishedAdditions": 121, "remainingAdditions": 1107,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
    })
    assert not git("diff", SNAPSHOT, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    print("SAME095 two-family TEXTUAL closure saved; Android/native/publication remain.")


def verify_signed():
    head = git("rev-parse", "HEAD")
    assert head != SNAPSHOT and git("rev-parse", "HEAD^") == SNAPSHOT
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == r.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    assert not git("diff", SNAPSHOT, head, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert not r.absent(19008)
    processes()
    rec = load(V / "batch-095-reconciliation.json")
    evidence = load(S / "execution-691.json")
    assert sha(V / "batch-095-reconciliation.json") == evidence["reconciliationSha256"]
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    for name, expected in evidence["recipeHashes"].items():
        assert sha(R / name) == expected
    for info in evidence["checks"].values():
        assert sha(R / info["path"]) == info["sha256"]
    assert rec["actionableRemainingFindingGroups"] == 0 and rec["textualReviewClosed"]
    return head, rec


def seal():
    head, rec = verify_signed()
    original = load(L / "progress-before-691.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 690 and p["batch"] == "095"
    cp = {
        "schemaVersion": 1, "execution": 691, "checkpoint": 691, "batch": "095",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "evidence": "docs/n1-sources/execution-691.json",
        "sourcePacket": "docs/n1-sources/batch-095-progress.json",
        "reconciliation": "docs/n1-reviews/batch-095-reconciliation.json",
        "textualReviewClosed": True, "runtimeDrafted": ["剖"], "reviewClosed": [],
        "published": [], "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionConfirmations": 0, "serialReviewerExitAndScopeReverified": True,
        "bothProcessesOneCallExactFullPacketReturned": True,
        "actionableRemainingFindings": 0, "teachingChanged": False,
        "completeDictionaryFamilies": 37, "completeRawCharacterRecords": 7,
        "metadataReadings": 1, "newSupportArticles": 1, "changedReusedArticles": 1,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 0,
        "newDirectWordExclusionPairsAppliedInDraft": 3, "generatedStrokePaths": 10,
        "actualHanCount": 32, "pendingNativeFallbackLabels": ["亻", "刂", "阝"],
        "contentVersion": "463619d79972e9f2", "allRuntimePayloadHashesVerified": 8441,
        "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 121, "remainingAdditions": 1107,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=691, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution691CoordinatorCheckpoint"] = cp
    p["batch095TextualReviewCheckpoint"] = copy.deepcopy(cp)
    p["execution691StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[key] == value for key, value in original.items() if key not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(C / "batch-095-textual-691-seal.json", cp)
    save(L / "checkpoint-691.json", cp)
    print("Verified signed clean checkpoint691:", head)


def issue_body():
    head, rec = verify_signed()
    body = (
        f"Batch095 (剖) — TEXTUAL review closed at normally signed LOCAL checkpoint691 "
        f"`{head}` (signatureG). Not Android/native acceptance, publication or whole-project completion.\n\n"
        f"Same frozen draft `{SNAPSHOT}` reviewed serially by actual Claude Opus5.5 "
        "(`claude-opus-5.5`, session ede78c28-e889-47b5-be0b-21533da61551), then GPT6.1Sol "
        "(`gpt-6.1-sol`, session ee7498e0-d3ad-46bf-bbc9-82761892cab0). Each isolated view-only "
        "CLI returned the exact full identical172035byte/3124line packet in ONE call without "
        "truncation/missinglines/tooloverlap/unfinishedtool. Actual exit verified before the next "
        "launch. Same15completearticles,37distinctcompleteJMdictfamilies (16lexical+21comparison), "
        "sevenrawcharacterrecords, exactdiff/SVG/generatedstrokes/publicdictionaryprovenance. "
        "Complete original reports/model/session/read/process evidence under docs/n1-reviews/"
        "batch-095-*. Returned bytes are not comprehension certification or fresh upstream retrieval.\n\n"
        "Complete new剖 and necessary解剖, plus added解 navigation passage: correctness, scoped "
        "coverage and phone-TEXT comprehension CLEAN within scope. No actionable defect "
        "established. Three Claude wording/extra-example suggestions remain optional. "
        "Clinical診察 and information-gathering調査 hypotheses do not establish a competing "
        "displayed answer from the exact complete families/current labels; 解体 has a dissection "
        "sense but no current card. Both models considered those comparisons, so not unique "
        "discoveries under different report labels. Actual production pools remain a later gate. "
        "No teaching edits or unnecessary changed-passage confirmations; original sessions retained "
        "for rendered confirmations. Reconciliation is evidence-based, not a model vote.\n\n"
        "Sole fullボウ/emptykun retained, explicit[ボウ]/[] offersぼう through own linked解剖かいぼう; "
        "supplementalホウ acknowledged without mutating frozen metadata. No inferred vocabulary "
        "level. Three directguards解剖/分析,解剖/分解,解剖/検査 retained, not an unrestricted "
        "substitution claim or transitive clique. Two allmappedpairs/fourdirections including "
        "existing解; zeroactivatedbaselinepairs. Tenpinnedgeneratedstrokes and32scopedHan unchanged; "
        "亻/刂/阝 cmap absence is NOT glyphfailure.\n\n"
        "Fresh validator0, regenerated unchanged manifest463619d79972e9f2,43focusedtests, exact "
        "batch baseline/link/membership/reading/quiz audit, vocabularyconsistency and original "
        "archivebudget check passed; all8441runtimepayloadhashes verified. Earlier complete "
        "frozen-source/baseline/font/stroke audit retained as execution690, not relabelled as "
        "fresh linguistic review. Runtime bytes unchanged.\n\n"
        "Next SAME095 fresh non-skippedAndroid, then productionContentSyncONCE/fullarchive/"
        "N1-All choices/threeguards/onlyぼう/nokun/tenstroke drawing/articles/SystemBack/offline/"
        "all32Han/fourfonts and serial original-session rendered confirmations; then combined-"
        "current-main/normalmerge/signing/ownerfastforward/terminalgreenCI/EVERYimmutableZIP"
        "manifesthash/unchangedbudgets/verifiedownerissue. QualifiedTESTONLYAndroid1c1b7bf4 "
        "retains productionf9b59a2, NOT latestappmain. Compatible updated client required.\n\n"
        "Published121/1228 and1107acceptanceremainder unchanged. Physical-phone, general-release "
        "and whole-set acceptance outstanding. No096 or unreviewedpush. Parent19008/runner.lock "
        "untouched; approved workspace artifacts only, no optional historical-session helper "
        "access, actual new permission denial or secondrunner. Full historicalprogress preserved; "
        "statuscontinue at the bounded Android/native gate."
    )
    (C / "batch-095-textual-691-issue-body.txt").write_text(body, encoding="utf-8")
    print("Prepared exact owner issue update.")


def receipt():
    head, rec = verify_signed()
    posted = load(C / "batch-095-textual-691-issue-reread.json")
    body = (C / "batch-095-textual-691-issue-body.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    p = load(C / "progress.json")
    original = load(L / "progress-before-691.json")
    assert p["checkpoint"] == 691 and p["status"] == "continue" and p["stage"] == STAGE
    record = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": r.hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "verified": True, "comparison": "Exact UTF-8 bytes.",
    }
    p["batch095TextualReviewIssueReceipt"] = record
    for key in ["execution691CoordinatorCheckpoint", "batch095TextualReviewCheckpoint"]:
        p[key]["issueUpdate"] = record["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[key] == value for key, value in original.items() if key not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-095-textual-691-issue-receipt.json", record)
    save(L / "checkpoint-691.json", p["execution691CoordinatorCheckpoint"])
    save(C / "batch-095-textual-691-final-verification.json", p["execution691CoordinatorCheckpoint"])
    assert load(C / "progress.json") == p
    print("Verified persisted checkpoint691, historical preservation and owner issue:", record["url"])


if __name__ == "__main__":
    {"prepare": prepare, "seal": seal, "issue-body": issue_body, "receipt": receipt}[sys.argv[1]]()
