import copy
import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("batch096", C / "review-batch-096.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.review
R, A, S, V, L = r.R, r.A, r.S, r.V, r.L
load, sha, git = r.load, r.sha, r.git
SNAPSHOT = r.SNAPSHOT
STAGE = "batch-096-textual-review-closed-awaiting-android-native"
NEXT = (
    "SAME096 fresh non-skipped THREE RealContentTest and ONE RareHanTest against THIS sibling next; "
    "textual closure ONLY on signed b26bcf9b, NOT native or full batch acceptance. "
    "Actual ClaudeOpus5.5 original session de7596b6-1f69-43e0-b297-c3e600fa712a and GPT6.1Sol "
    "original session ca536738-97f2-4841-b985-321ce12b37c1 completed serial blind initial reviews "
    "and identical dependent coverage supplements. Initial packet100 distinct families omitted final-label "
    "two families; supplement completed102 distinct/105 occurrences,12 raw records and31 total existing/new "
    "article bodies. Complete originals and exact full returned packet/process evidence preserved; no teaching edit. "
    "Use explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot and "
    "ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, oneGradleworker and quoted "
    "'-Pkotlin.compiler.execution.strategy=in-process'; inspect terminal test cases and actual sibling path. "
    "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain. Then fresh fullarchive "
    "productionContentSync ONCE/native N1-All actual choices/twelve directguards/onlyごう/no kun/tenstroke "
    "drawing/complete剛 and剛健 articles/SystemBack/offline/all28Han/fourfonts with fresh safe port/device "
    "ownership checks; 冂/刂 cmap absence NOT glyph failure. Preserve exact fixture/hash and terminal percase0, "
    "no doubleparse, heap/archiveguard increase or shared-device interference. Original two model sessions "
    "need serial bounded rendered confirmations; current textual review certifies neither native/phone nor "
    "widercustom/random/fallback pools. All combined-current-main/nonrewritingmerge/changedteachingreview/"
    "checks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/"
    "unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/media/path/verifiedownerissue gates remain. "
    "Parent19008 retains runner.lock throughout child lifetime; NO child acquire/delete/unlock/readprobe. "
    "Approved control/committed evidence/frozen inputs only, no optional historical-session helper access. "
    "Preserve/report/yield actual new denial/signing hang/uncertain ownership. Published122/1228 and1106 "
    "acceptance remainder unchanged; physicalphone/generalrelease/whole-set outstanding. No097, "
    "unreviewedpush or secondrunner."
)


def save(path, value):
    temp = path.with_suffix(path.suffix + ".702.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def processes():
    records, previous = {}, None
    for phase in ["initial", "supplement"]:
        for label, model in r.MODELS.items():
            prefix = f"batch-096-{phase}-{label}"
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
            packet = C / f"batch-096-{phase}-packet.txt"
            assert call["name"] == "view" and call["success"]
            assert call["arguments"] == {"path": str(packet), "forceReadLargeFiles": True}
            assert call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
            assert sha(V / (prefix + ".md")) == record["reportSha256"]
            assert sha(V / (prefix + ".jsonl")) == record["rawExecutionSha256"]
            assert r.absent(record["launcherPid"])
            if previous:
                assert previous < record["startedAt"]
            previous = record["completedAt"]
            if phase == "supplement":
                assert records[f"initial-{label}"]["sessionId"] == record["sessionId"]
                assert "--resume" in record["command"]
            records[f"{phase}-{label}"] = {
                **{k: record[k] for k in [
                    "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
                    "requestedModel", "actualModels", "snapshot", "reportSha256", "rawExecutionSha256",
                ]},
                "report": prefix + ".md", "execution": prefix + "-execution.json",
                "coverage": prefix + "-coverage.json", "allAssignedRangesReturned": True,
                "toolCalls": 1, "observedToolOverlaps": 0, "exactFullPacketReturnedInOneCall": True,
                "limits": "Actual complete returned bytes/ranges verified, not comprehension certification.",
            }
    return records


def prepare():
    r.frozen()
    records = processes()
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for phase in ["initial", "supplement"]:
        assert (C / f"batch-096-{phase}-packet.txt").read_bytes() == (V / f"batch-096-{phase}-packet.txt").read_bytes()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (701, "096")
    ledger = load(S / "batch-096-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    receipts = {}
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "096"],
        "tests": [sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
                  "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources"],
        "vocabulary": [sys.executable, "-B", str(R / "tools" / "grammar_vocabulary.py"), "check"],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
    }
    for name, command in commands.items():
        path = V / f"batch-096-textual-review-{name}-702.txt.gz"
        assert not path.exists()
        run = subprocess.run(command, cwd=R / "tools" if name == "tests" else R,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        path.write_bytes(gzip.compress(run.stdout, mtime=0))
        assert run.returncode == 0, (name, run.stdout.decode("utf-8", errors="replace")[-2000:])
        if name == "tests":
            assert b"Ran 43 tests" in run.stdout and run.stdout.rstrip().endswith(b"OK")
        receipts[name] = {
            "path": path.relative_to(R).as_posix(), "sha256": sha(path),
            "uncompressedSha256": hashlib.sha256(run.stdout).hexdigest(),
        }
        print(name, "passed", flush=True)
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from build_manifest import build_manifest, sha256

    mechanical = audit(R, "096")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "54645b95fe8e939c"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8444
    for provenance in ["review-dictionary-provenance", "supplement-provenance"]:
        for source in load(V / f"batch-096-{provenance}.json")["sources"]:
            assert sha(Path(source["path"])) == source["sha256"]
    assert ledger["allMappedReciprocalPairs"] == [["剛", "words/剛健.md"]]
    assert "(../words/剛健.md)" in (R / "kanji" / "剛.md").read_text(encoding="utf-8")
    assert "(../kanji/剛.md)" in (R / "words" / "剛健.md").read_text(encoding="utf-8")
    assert not (R / "words" / "頑丈.md").exists()
    reviewed = {name: sha(R / name) for name in [
        "kanji/剛.md", "words/剛健.md", "strokes/剛.json", "manifest.json",
    ]}
    rec = {
        "schemaVersion": 1, "execution": 702, "batch": "096", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False, "reviewedRuntimeHashes": reviewed,
        "initialModels": list(r.MODELS.values()), "processes": records,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 235770, "initialPacketLines": 5205,
        "supplementPacketBytes": 12666, "supplementPacketLines": 246,
        "initialDistinctCompleteFamilies": 100, "initialFamilyOccurrences": 103,
        "completeSupplementalFamilies": 2, "combinedDistinctCompleteFamilies": 102,
        "combinedFamilyOccurrences": 105, "rawCharacterRecords": 12,
        "initialCompleteArticleBodies": 27, "additionalCompleteArticleBodies": 4,
        "newArticleBodies": 2, "changedReusedPassages": 0,
        "coverageCorrection": "Coordinator initial packet omitted separately committed final-label two families and four linked/comparison bodies. Original initial reports preserved. Identical bounded original-session supplements completed both families' scope serially; no claim that the initial reads alone covered all102 families. Initial preparation assertion exposed100 rather than102 in first two packets; final union of THREE packets is102.",
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
            for name in ["kanji/剛.md:1-48", "words/剛健.md:1-37"]
        },
        "findings": [],
        "optionalDispositions": [
            {"reportedBy": "Claude", "location": "words/剛健.md:19",
             "claim": "Busy is an unrelated contrast.", "status": "optional",
             "decision": "No edit. It is an explicit negative boundary, not a purported definition or substitution rule."},
            {"reportedBy": "Claude", "location": "words/剛健.md:33",
             "claim": "Traditional is not explicit in either definition.", "status": "optional",
             "decision": "No edit. The historical masculine association is described as a connotation and immediately separated from any grammatical/subject restriction. Both actual dictionary definitions say男性的; the paragraph does not assert an origin, date or demographic frequency.",
             "evidence": "Exact supplied Daijisen and Seisenban definitions; archived early/historical examples. This is scoped description, not a measured usage study."},
            {"reportedBy": "both", "location": "words/剛健.md:15-19",
             "claim": "Add another full sentence or bodily-strength example.", "status": "optional",
             "decision": "No edit. Current attested phrase, attachment patterns and qualified compound example suffice for the bounded sole-reading support article. No mandatory sentence quota."},
            {"reportedBy": "Claude", "location": "kanji/剛.md",
             "claim": "Add nounごう through柔よく剛を制す.", "status": "optional",
             "decision": "No edit. Recognition expansion is not required for the selected linkedゴウ example."},
            {"reportedBy": "Claude", "location": "words/剛健.md:8",
             "claim": "Optionalばりばり exclusion.", "status": "optional",
             "decision": "No added guard. Actual ripping/crunching/working-vigorously label describes activity, not robust bodily/mental constitution. Complete sense4 permits nominal/na classification, so grammar alone is NOT the rationale. Both models considered the exact final label and all senses; neither established a required guard. Existing 活力/ばりばり guard does not imply a transitive clique.",
             "evidence": "Complete frozen1010340 and actual words/ばりばり.md; 剛健1284120 and final paragraph."},
        ],
        "hypothesisDispositions": [
            {"reportedBy": "Claude initially; GPT initial inference also limited",
             "claim": "Twelfth 活力 guard not directly final-label verified.", "status": "resolved",
             "decision": "Both original sessions read actual title vitality; energy, complete article and full1208480. Guard justified by actual vigor/vitality overlap, not an unrestricted Japanese substitution claim."},
            {"reportedBy": "Claude; equivalent GPT contextual observation",
             "claim": "If頑丈 has a card its sense may require a guard.", "status": "withdrawn",
             "decision": "Current words/頑丈.md absent, verified by coordinator. Complete family1217690 is recognition evidence, not proof of an existing displayed target. Both reviewers explicitly distinguish supplied inventory from independent filesystem verification."},
            {"reportedBy": "Claude",
             "claim": "山/刀 target context was not supplied initially.", "status": "resolved",
             "decision": "Both complete unchanged articles supplied to both sessions. Modern-shape/radical explanations remain consistent; no legacy full rewrite implied."},
            {"reportedBy": "Claude",
             "claim": "No attested full predicate剛健です or native-speaker judgment.", "status": "withdrawn",
             "decision": "Absence of such evidence is not an established unnaturalness claim. Actual dictionaries classify noun/形動; politeです predicate andな attachment are ordinary productive grammar. No claim that this exact predicate is frequent or an attested quotation. GPT explicitly checked it as grammatical. Native-speaker certification remains absent; adjudication rests on grammar/evidence, not votes."},
            {"reportedBy": "Claude",
             "claim": "Title uniqueness across full kanji inventory not independently checked.", "status": "resolved",
             "decision": "Coordinator fresh validator reports zero errors and batch audit passes; title collision is structurally checked. Reviewer independence limits preserved."},
            {"reportedBy": "both",
             "claim": "Larger/random/legacy fallback may expose 強/硬 strength/stiffness overlap.", "status": "unresolved",
             "severity": "runtime gate, not a current default-four teaching defect",
             "decision": "Three authored semantically wrong options cover default four choices. No wider-pool safety claimed. Actual N1/All production choices and any demonstrated semantic ambiguity remain required before full batch acceptance; do not mark runtime accepted or publish now.",
             "evidence": "Actual current 削/剖/則 labels; complete strong/hard character contexts; existing quiz contract."},
        ],
        "modelContributionComparison": {
            "shared": "Both reviewed definitions/whole constructions/translation, noun-na morphology, masculine association without subject restriction, reading allocation and supplementalコウ, source metadata, radical/mnemonic/strokes, three default wrong choices, pairwise guards and links. Both noted extra-source/runtime limits. Supplemental 活力/ばりばり observations equivalent despite differing initial labels; not unique discoveries.",
            "claudeUniqueVerifiedUseful": [], "gptUniqueVerifiedUseful": [],
            "claudeUniqueNonblocking": "Optional negative-boundary/traditional wording and nounごう expansion; explicit predicate attestation and title-list limits are not demonstrated teaching errors.",
            "unsupportedMandatorySuggestions": "No mandatory extra example, indiscriminate synonym clique, invented missing-ID guard or historical reconstruction established.",
            "limits": "Matched sample/source access; original coverage omission disclosed and completed. Not a general model benchmark, equal-depth comprehension certification or native-speaker review.",
        },
        "actionableRemainingTextualFindingGroups": 0, "consequentialUnresolvedTeachingClaims": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "previousCompleteSourceBaselineFontStrokeAudit": "docs/n1-sources/batch-096-draft-audit.json",
        "previousCompleteSourceBaselineFontStrokeAuditSha256": sha(S / "batch-096-draft-audit.json"),
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "activatedBaselinePairs": 0,
        "newDirectWordExclusionPairsAppliedInDraft": 12,
        "actualHanCount": 28, "nativeFontPending": ["冂", "刂"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT,
        "limits": [
            "TEXTUAL closure only, NOT full batch review closure, runtime acceptance or publication; reviewClosed/published arrays remain empty.",
            "All four original reports/executions preserved. Each process returned its exact entire assigned packet in one call, no truncation/missinglines/overlap/unfinishedtool, and exited before the next process. Returned bytes do not certify comprehension.",
            "Initial common evidence omitted final-label packet; same original-session supplementary task/source access completed both models'102-family scope. Not relabelled as fresh blind review.",
            "Public text is coordinator-supplied committed extraction, not independent upstream retrieval. Gaiji may be omitted; no historical/phonetic reconstruction adopted.",
            "Runtime and all8444 payload hashes unchanged; prior complete source/baseline/stroke/font audit is execution701, not relabelled as fresh full linguistic inspection.",
            "Default-four three kanjichoices accepted textually. Actual N1/All and widercustom/random/fallback pools remain runtime gates; unresolved exposure is not certified safe.",
            "Fresh Android/RareHan/native/fourfonts/drawing/reading/N1-All/Back/offline/ContentSyncONCE and dependent original-session rendered review remain pending.",
            "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Compatibleclientf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
            "Published122/1228 and1106 acceptance remainder unchanged; six separate earlierN2source members保案派第策結 and separate妖exception retained. No097 or project completion.",
            "All original combined-main/signing/ownerpush/terminalCI/EVERYimmutableZIPhash/originalbudgets/ownerissue gates remain. Parent lock untouched, no optional historical helper access or new permission denial.",
        ],
    }
    save(V / "batch-096-reconciliation.json", rec)
    ledger["initialDraftLimits"] = copy.deepcopy(ledger["limits"])
    ledger.update(status=STAGE, initialReviewSnapshot=SNAPSHOT, reviewedTeachingSnapshot=SNAPSHOT,
                  textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False, nextAction=NEXT)
    ledger["limits"][0] = rec["limits"][0]
    ledger["independentReviewersLaunched"] = 2
    ledger["quizAudit"]["剛"]["limits"] = "Default-four textually accepted; actual production N1/All and wider-pool review pending."
    ledger["textualReview"] = {
        "snapshot": SNAPSHOT, "models": rec["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-096-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-096-reconciliation.json"),
        "teachingChanged": False, "textualReviewClosed": True,
        "actionableRemainingTextualFindings": 0, "runtimeAccepted": False,
    }
    ledger["pendingGates"] = [
        "Fresh non-skipped THREE RealContentTest/ONE RareHanTest against actual sibling.",
        "Full productionContentSyncONCE/native N1-All choices/twelve guards/onlyごう/no kun/tenstroke drawing/articles/Back/offline/all28Han/fourfonts; dependent original-session rendered confirmations.",
        "Combined-current-main integration, changed teaching re-review if needed, all checks/normal signing/owner fastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/originalbudgets/verifiedownerissue.",
    ]
    for row in ledger["supportMappings"]:
        row["status"] = "textual-review-closed-awaiting-android-native"
    save(S / "batch-096-progress.json", ledger)
    membership = load(S / "batch-096-membership.json")
    membership["initialDraftLimits"] = copy.deepcopy(membership["limits"])
    membership.update(status=STAGE, initialReviewSnapshot=SNAPSHOT,
                      textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False)
    membership["limits"] = rec["limits"][0]
    save(S / "batch-096-membership.json", membership)
    recipe = S / Path(__file__).name
    shutil.copyfile(Path(__file__), recipe)
    shutil.copyfile(C / "preflight-702.ps1", S / "batch-096-textual-preflight-702.ps1.txt")
    save(S / "execution-702.json", {
        "schemaVersion": 1, "execution": 702, "batch": "096", "status": STAGE,
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "startingState": p["execution702StartingState"],
        "reconciliation": "docs/n1-reviews/batch-096-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-096-reconciliation.json"),
        "recipeHashes": {path.relative_to(R).as_posix(): sha(path) for path in [
            recipe, V / "review-batch-096.py", V / "supplement-batch-096.py",
            V / "batch-096-serial-review-base-recipe.py", S / "batch-096-textual-preflight-702.ps1.txt",
        ]},
        "checks": receipts, "runtimeBytesChanged": False,
        "publishedAdditions": 122, "remainingAdditions": 1106,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
    })
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    print("SAME096 two-family TEXTUAL closure saved; Android/native/publication remain.", flush=True)


def verify_signed():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == SNAPSHOT
    for repo, expected in [(R, head), (A, r.ANDROID)]:
        assert git("rev-parse", "HEAD", repo=repo) == expected
        assert git("log", "-1", "--format=%G?", repo=repo) == "G"
        assert not git("status", "--porcelain", repo=repo)
    assert not git("diff", SNAPSHOT, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert not r.absent(19008)
    processes()
    rec = load(V / "batch-096-reconciliation.json")
    evidence = load(S / "execution-702.json")
    assert sha(V / "batch-096-reconciliation.json") == evidence["reconciliationSha256"]
    for name, expected in {**rec["reviewedRuntimeHashes"], **evidence["recipeHashes"]}.items():
        assert sha(R / name) == expected
    for info in evidence["checks"].values():
        assert sha(R / info["path"]) == info["sha256"]
    return head, rec


def seal():
    head, rec = verify_signed()
    original = load(L / "progress-before-702.json")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (701, "096")
    cp = {
        "schemaVersion": 1, "execution": 702, "checkpoint": 702, "batch": "096",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "evidence": "docs/n1-sources/execution-702.json",
        "sourcePacket": "docs/n1-sources/batch-096-progress.json",
        "reconciliation": "docs/n1-reviews/batch-096-reconciliation.json",
        "textualReviewClosed": True, "runtimeDrafted": ["剛"], "reviewClosed": [], "published": [],
        "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionCoverageSupplements": 2, "serialReviewerExitAndScopeReverified": True,
        "allFourProcessesOneCallExactFullPacketReturned": True,
        "actionableRemainingTextualFindings": 0, "teachingChanged": False,
        "completeDictionaryFamilies": 102, "familyOccurrences": 105,
        "completeRawCharacterRecords": 12, "metadataReadings": 1,
        "newSupportArticles": 1, "changedReusedArticles": 0,
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "activatedBaselinePairs": 0,
        "newDirectWordExclusionPairsAppliedInDraft": 12, "generatedStrokePaths": 10,
        "actualHanCount": 28, "pendingNativeFallbackLabels": ["冂", "刂"],
        "contentVersion": "54645b95fe8e939c", "allRuntimePayloadHashesVerified": 8444,
        "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 122, "remainingAdditions": 1106,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=702, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution702CoordinatorCheckpoint"] = cp
    p["batch096TextualReviewCheckpoint"] = copy.deepcopy(cp)
    p["execution702StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-096-textual-702-seal.json", cp)
    save(L / "checkpoint-702.json", cp)
    print("Verified signed clean checkpoint702:", head)


def issue_body():
    head, rec = verify_signed()
    body = (
        f"Batch096 (剛) — two-family TEXTUAL review closed at normally signed LOCAL checkpoint702 "
        f"`{head}` (signature G). Not Android/native acceptance, publication or project completion.\n\n"
        f"Same frozen draft `{SNAPSHOT}` reviewed serially by actual Claude Opus5.5 "
        "(`claude-opus-5.5`, session de7596b6-1f69-43e0-b297-c3e600fa712a), then GPT6.1Sol "
        "(`gpt-6.1-sol`, session ca536738-97f2-4841-b985-321ce12b37c1). Initial common packet "
        "235770 bytes/5205 lines covered100 distinct complete families,12 raw character records "
        "and27 complete article bodies. It omitted the committed final-label two-family packet "
        "and four context articles. Originals preserved; identical bounded original-session "
        "supplements (12666bytes/246lines) completed102 distinct families/105 occurrences and31 "
        "total article bodies for BOTH models. Each of four isolated view-only processes returned "
        "its exact complete packet in one call without truncation/missinglines/tooloverlap/unfinishedtool "
        "and exited before the next. Full original reports/models/sessions/executions/coverage "
        "and omission disposition archived under docs/n1-reviews/batch-096-*. Returned bytes "
        "are not comprehension certification or independent upstream retrieval.\n\n"
        "Complete new剛 and necessary剛健: correctness, scoped coverage and phone-TEXT "
        "comprehensibility CLEAN in scope; no actionable textual defect established. Optional "
        "wording/additional example/nounごう suggestions not adopted. 活力 guard directly verified "
        "by both original-session supplements; ばりばり activity label does not establish a "
        "mandatory robust-constitution guard, and guards are not transitive cliques. 頑丈 "
        "recognition does not establish a current card (absent); 山/刀 supplied and consistent. "
        "Ordinary noun/na-adjective morphology supports剛健です without claiming exact-phrase "
        "frequency or native-speaker certification. Wider/random/legacy fallback strength/stiffness "
        "exposure remains explicitly pending, NOT certified safe. No teaching edits.\n\n"
        "Full soleゴウ/emptykun retained; explicit[ゴウ]/[] selectsごう via own linked剛健ごうけん. "
        "Supplementalコウ acknowledged without mutating frozen metadata; search-only剛い/name "
        "readings do not create questions. No inferred vocabulary level. Twelve directguards; "
        "ONE allmappedpair/TWO directions/ZERO activatedbaselinepairs. Ten pinned generated "
        "strokes/all28Han unchanged; 冂/刂 cmap absence is NOT glyph failure.\n\n"
        "Fresh validator0, regenerated unchanged manifest54645b95fe8e939c,43 focused tests, "
        "exact batch audit, vocabularyconsistency and original archivebudget checks passed; "
        "all8444runtimepayloadhashes verified. Prior complete source/baseline/stroke/font audit "
        "retained as execution701, not relabelled as fresh full linguistic inspection. Runtime "
        "bytes unchanged; only evidence/ledger local commit, no push.\n\n"
        "Next SAME096 fresh non-skipped THREE RealContentTest/ONE RareHanTest, production "
        "ContentSync ONCE/fullarchive/N1-All choices/twelve guards/onlyごう/no kun/tenstroke "
        "drawing/articles/SystemBack/offline/all28Han/fourfonts, then original-session rendered "
        "confirmations. Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest "
        "appmain. All combined-current-main/signing/ownerfastforward/terminalgreenCI/EVERY "
        "immutableZIP runtime manifesthash/originalbudgets/verifiedownerissue gates remain.\n\n"
        "Published122/1228;1106 acceptance remainder unchanged. Physical-phone/general-release/"
        "whole-set outstanding. Compatible updated client required. No097, unreviewedpush, "
        "parent-lock manipulation, optional historical-session helper access, actual new "
        "permission denial or secondrunner. Full historicalprogress preserved; statuscontinue."
    )
    (C / "batch-096-textual-702-issue-body.txt").write_text(body, encoding="utf-8")


def receipt():
    head, rec = verify_signed()
    posted = load(C / "batch-096-textual-702-issue-reread.json")
    body = (C / "batch-096-textual-702-issue-body.txt").read_bytes().decode("utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    p = load(C / "progress.json")
    original = load(L / "progress-before-702.json")
    assert (p["checkpoint"], p["status"], p["stage"]) == (702, "continue", STAGE)
    record = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "verified": True, "comparison": "Exact UTF-8 bytes.",
    }
    p["batch096TextualReviewIssueReceipt"] = record
    for key in ["execution702CoordinatorCheckpoint", "batch096TextualReviewCheckpoint"]:
        p[key]["issueUpdate"] = record["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-096-textual-702-issue-receipt.json", record)
    save(L / "checkpoint-702.json", p["execution702CoordinatorCheckpoint"])
    save(C / "batch-096-textual-702-final-verification.json", p["execution702CoordinatorCheckpoint"])
    assert load(C / "progress.json") == p
    print("Verified persisted checkpoint702, historical preservation and owner issue:", record["url"])


if __name__ == "__main__":
    {"prepare": prepare, "seal": seal, "issue-body": issue_body, "receipt": receipt}[sys.argv[1]]()
