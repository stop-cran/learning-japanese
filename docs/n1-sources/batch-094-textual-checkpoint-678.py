import copy
import gzip
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("review094", C / "review-batch-094.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
review = module.review
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
load, sha, git = review.load, review.sha, review.git
SNAPSHOT = review.SNAPSHOT
STAGE = "batch-094-initial-reviews-complete-awaiting-quiz-safeguards"
NEXT = (
    "SAME094 bounded quiz-safeguard correction and original-session confirmations only: "
    "both blind initial textual reviews on signed d1e986ec are complete and archived; "
    "three direct overlaps are accepted but UNRESOLVED. Add ONLY 除く and 外す to existing "
    "words/削る.md quiz_exclusions, and 省く to words/削除.md quiz_exclusions, preserving all "
    "original exclusions/order, identities, primary readings, titles, N2 levels, bodies, "
    "full サク and けず.る/はつ.る/そ.ぐ order and explicit [サク]/[けず.る]. "
    "Record exact header edits/additive dispositions in batch094 ledger, re-audit full baseline "
    "exceptions, three mapped pairs/six directions/two activated baseline pairs, source/reading/"
    "quiz/font/stroke invariants; run validator and manifest generator, focused tests and "
    "normal signed LOCAL revised freeze. Resume original Claude edf22897-9f87-4a3b-b20f-4c2fd839013a "
    "then GPT 65fd64ff-aae2-40af-927e-bf19b52fecb6 SERIAL read-only CLI confirmations with each "
    "own original report, revised signed snapshot/exact diff and precise source evidence; "
    "actual available models, one tool at a time, actual exit before next reviewer, preserve "
    "complete reports/model/session/read/process limits, no newblind credit. Reconcile "
    "evidence, not votes; Claude also mentions 削除/省く in a low-risk hypothesis, so that "
    "observation is shared, NOT uniquely GPT. GPT uniquely establishes the other two "
    "unguarded pairs within this shared sample. No universal live-pool certification. "
    "If no actionable defect or consequential unresolved teaching claim remains, mark "
    "TEXTUAL closure only and yield before fresh Android/native. All later original gates "
    "remain: fresh non-skipped THREE RealContentTest and ONE RareHanTest against THIS sibling; "
    "qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain; "
    "productionContentSync ONCE/fullarchive, N1/All production choices and THREE new direct "
    "guards, onlyさく/けずる, nine-stroke drawing/articles/SystemBack/offline/all41Han/"
    "fourfonts (刂/斫/氵/阝 cmap absence is NOT glyph failure), original-session rendered "
    "confirmations; combined-main nonrewriting merge/review changed teaching/all checks/"
    "normal signing/owner fastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/"
    "unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/media/path/verifiedownerissue. "
    "Parent19008 owns runner.lock throughout child lifetime: NO child acquire/delete/unlock. "
    "Approved control/committed packets/frozen inputs only; no optional historical-session "
    "helper access. Preserve/report/yield actual new denial, signing hang or uncertain ownership. "
    "Published120/1228 and1108acceptanceremainder unchanged; physicalphone/generalrelease/"
    "whole-set outstanding. No095, unreviewed push or secondrunner."
)


def save(path, value):
    temp = path.with_suffix(path.suffix + ".678.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def processes():
    result, previous = {}, None
    for label, model in review.MODELS.items():
        prefix = f"batch-094-initial-{label}"
        record = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert record["snapshot"] == SNAPSHOT
        assert record["exitCode"] == 0 and record["actualModels"] == [model]
        assert record["usageCurrentModel"] == model
        assert record["multiToolResponseCount"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert coverage["allAssignedRangesReturned"]
        assert len(record["toolCalls"]) == 1
        call = record["toolCalls"][0]
        assert call["name"] == "view" and call["success"]
        assert call["arguments"] == {"path": str(review.PACKET), "forceReadLargeFiles": True}
        assert call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
        assert sha(V / (prefix + ".md")) == record["reportSha256"]
        assert sha(V / (prefix + ".jsonl")) == record["rawExecutionSha256"]
        assert review.absent(record["launcherPid"])
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


def prepare_checkpoint():
    review.frozen()
    records = processes()
    assert not git("diff", SNAPSHOT, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert review.PACKET.read_bytes() == (V / review.PACKET.name).read_bytes()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 677 and p["batch"] == "094"
    ledger = load(S / "batch-094-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    receipts = {}
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "094"],
        "tests": [
            sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
            "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources",
        ],
        "vocabulary": [sys.executable, "-B", str(R / "tools" / "grammar_vocabulary.py"), "check"],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
    }
    for name, command in commands.items():
        path = V / f"batch-094-textual-review-{name}-678.txt.gz"
        assert not path.exists()
        run = subprocess.run(command, cwd=R / "tools" if name == "tests" else R,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        path.write_bytes(gzip.compress(run.stdout, mtime=0))
        assert run.returncode == 0, (name, run.stdout.decode("utf-8", errors="replace")[-2000:])
        if name == "tests":
            assert b"Ran 43 tests" in run.stdout and run.stdout.rstrip().endswith(b"OK")
        receipts[name] = {
            "path": path.relative_to(R).as_posix(), "sha256": sha(path),
            "uncompressedSha256": review.hashlib.sha256(run.stdout).hexdigest(),
        }
        print(name, "passed", flush=True)

    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from build_manifest import build_manifest, sha256

    mechanical = audit(R, "094")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "c054efb36f283dc7"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8438
    for source in load(V / "batch-094-review-dictionary-provenance.json")["sources"]:
        assert sha(Path(source["path"])) == source["sha256"]
    reviewed = {name: sha(R / name) for name in [
        "kanji/\u524a.md", "words/\u524a\u308b.md", "words/\u524a\u9664.md",
        "kanji/\u9664.md", "strokes/\u524a.json", "manifest.json",
    ]}
    finding = {
        "id": "094-word-direct-guards",
        "reportedSeverity": "Moderate",
        "severity": "Moderate", "facet": "quiz correctness",
        "reportedBy": ["GPT"],
        "sourceReport": "batch-094-initial-gpt.md",
        "locations": ["words/\u524a\u308b.md:9,23-24,35-38",
                      "words/\u524a\u9664.md:9,16,30-33"],
        "status": "unresolved", "accepted": True, "remediationApplied": False,
        "claim": "Three overlapping word-title pairs lack direct exclusion guards.",
        "impact": "An ordinary taught removal/deletion sense permits a competing title to be accepted; shared guards do not protect the missing direct pair.",
        "pairs": [
            {
                "words": ["\u524a\u308b", "\u9664\u304f"],
                "reason": "The taught sentence-deletion/removal sense of \u524a\u308b overlaps displayed remove; exclude for \u9664\u304f.",
                "evidence": "JMdict1298090 sense3 versus1345640 senses1-2; complete actual articles and Daijisen\u3051\u305a\u308b sense3.",
                "minimalRemedy": "Append \u9664\u304f to \u524a\u308b quiz_exclusions.",
            },
            {
                "words": ["\u524a\u308b", "\u5916\u3059"],
                "reason": "Displayed remove; unfasten is defensible for the ordinary removal/deletion aspect of \u524a\u308b; staff/list removal overlaps the complete family of \u5916\u3059.",
                "evidence": "JMdict1298090 senses2-3 versus1203270 senses1-2; actual displayed labels and Daijisen personnel/list examples. This is not a claim of unrestricted substitution.",
                "minimalRemedy": "Append \u5916\u3059 to \u524a\u308b quiz_exclusions.",
            },
            {
                "words": ["\u524a\u9664", "\u7701\u304f"],
                "reason": "Displayed omit; cut down on overlaps deletion/elimination of textual material.",
                "evidence": "JMdict1298120 versus1351040 sense1; complete actual articles and Daijisen\u3055\u304f\u3058\u3087 definition.",
                "minimalRemedy": "Append \u7701\u304f to \u524a\u9664 quiz_exclusions.",
                "equivalentObservation": "Claude hypothesis mentions this same pair as low risk. Different label/confidence does not make the observation unique to GPT.",
            },
        ],
        "evidence": [
            "docs/n1-sources/batch-094-comparison-jmdict.xml",
            "docs/n1-sources/batch-094-kezuru-public-text.txt",
            "docs/n1-sources/batch-094-sakujo-public-text.txt",
            "docs/content-format.md:156-177",
        ],
        "confidence": "Medium-high semantic overlap; production co-occurrence not demonstrated.",
        "adjudication": "Accepted from exact titles, whole taught senses, complete dictionary families and pairwise contract, not model votes. Add only the three direct guards, preserve all originals; no prose rewrite or transitive clique.",
        "laterGate": "Confirm actual N1/All production choices and new three direct guards under original native gate; static semantic review does not certify every live pool.",
    }
    optional = [
        {
            "reportedBy": "Claude", "location": "kanji/\u524a.md:51",
            "claim": "Use characters instead of words interchangeable.",
            "status": "optional", "decision": "No edit in this checkpoint; the comparison does not imply the characters or words are semantically interchangeable.",
        },
        {
            "reportedBy": "Claude", "location": "kanji/\u524a.md:50",
            "claim": "Add attested figurative\u8208\u3092\u305d\u3050 example.",
            "status": "optional", "decision": "No edit; recognized figurative sense and its kana flag are already explained; no exhaustive alternate-reading course required.",
        },
        {
            "reportedBy": "Claude", "location": "words/\u524a\u308b.md:25,44; words/\u524a\u9664.md:38",
            "claim": "Internal source/N2 terminology and separate reading versus verb could be clearer.",
            "status": "optional", "decision": "No established actionable defect; existing text explicitly distinguishes separate\u306f\u3064\u308b from\u3051\u305a\u308b and does not infer a new N2 assignment.",
        },
        {
            "reportedBy": "Claude", "location": "words/\u524a\u9664.md:22,41",
            "claim": "Say passive past of\u3059\u308b and rephrase recoverability statement.",
            "status": "optional", "decision": "Current passive explanation is true, and word-alone-does-not-promise recovery is accurate without implying recovery impossible. No edit.",
        },
    ]
    rec = {
        "schemaVersion": 1, "execution": 678, "batch": "094", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False, "reviewedRuntimeHashes": reviewed,
        "initialModels": list(review.MODELS.values()), "processes": records,
        "confirmations": {}, "serialReviewerProcessesVerified": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": review.PACKET.stat().st_size, "initialPacketLines": 5902,
        "initialDistinctCompleteFamilies": 121, "lexicalFamilies": 99,
        "comparisonFamilies": 26, "familyOccurrences": 125,
        "rawCharacterRecords": 10, "completeArticleBodiesSupplied": 24,
        "newArticleBodies": 1, "changedReusedBodies": 3,
        "verdicts": {
            "kanji/\u524a.md": {
                "correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN",
                "scope": "Complete new article; bounded textual review only.",
            },
            "words/\u524a\u308b.md": {
                "correctness": "NEEDS FIX", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN",
                "scope": "Complete reused article; two accepted missing direct quiz guards, not erroneous prose.",
            },
            "words/\u524a\u9664.md": {
                "correctness": "NEEDS FIX", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN",
                "scope": "Complete reused article; one accepted missing direct quiz guard, not erroneous prose.",
            },
            "kanji/\u9664.md:41": {
                "correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN",
                "scope": "Added reciprocal-navigation line only; complete article supplied as context.",
            },
        },
        "findings": [finding], "optionalDispositions": optional,
        "modelContributionComparison": {
            "shared": "Both accept Japanese examples/translations, whole constructions, complete metadata/curation, separate\u306f\u3064\u308b, sense-local\u305d\u3050 flag, shape-only mnemonic/radical variant, three wrongkanji labels, mappings and preserved legacy identities. Both observe potential\u524a\u9664/\u7701\u304f overlap, Claude as a low-risk hypothesis and GPT as actionable.",
            "gptUniqueVerifiedUseful": ["\u524a\u308b/\u9664\u304f missing direct guard", "\u524a\u308b/\u5916\u3059 missing direct guard"],
            "claudeUnique": "Nonblocking wording/polish and explicit Weblio\u3078\u305a\u308b/\u4e2d\u6b62-target evidence limits. No unique verified mandatory teaching defect.",
            "unsupportedSuggestions": "No required etymological, frequency, broad semantic or additional-support claim accepted; optional wording does not become a mandatory defect.",
            "limits": "Same snapshot/task/source access, equivalent observations across findings/optional/hypotheses/limits compared. This sample is not a model benchmark, equal-depth comprehension certification or native-speaker review.",
        },
        "actionableRemainingFindingGroups": 1, "actionableRemainingDirectPairs": 3,
        "consequentialUnresolvedTeachingClaims": 0,
        "textualReviewClosed": False, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "previousCompleteSourceBaselineFontStrokeAudit": "docs/n1-sources/batch-094-draft-audit.json",
        "previousCompleteSourceBaselineFontStrokeAuditSha256": sha(S / "batch-094-draft-audit.json"),
        "allMappedReciprocalPairs": 3, "directedLinksVerified": 6, "activatedBaselinePairs": 2,
        "newDirectWordExclusionPairsApplied": 0, "acceptedDirectWordExclusionPairsPending": 3,
        "actualHanCount": 41, "nativeFontPending": ["\u5202", "\u65ab", "\u6c35", "\u961d"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT,
        "limits": [
            "Initial textual reviews and evidence adjudication complete, NOT textual closure, runtime acceptance or publication. Three accepted direct quiz-guard fixes and both original-session confirmations remain.",
            "Both actual model families received the same255427byte/5902linepacket:125completefamilyoccurrences/121distinctfamilies, tencharacterrecords and24completearticlebodies. Each made exactly ONE serial view call returning the exact full packet; no truncation/missinglines/tooloverlap/unfinishedtool; actualprocess exits verified.",
            "Returned bytes/hashes are not comprehension certification. Both report inspecting all applicable families; actual models/session IDs/full original reports/executions and supplied-source provenance preserved.",
            "Public text is coordinator-supplied committed extraction, not independent upstream retrieval. Gaiji may be omitted. Unchanged Webliofooter\u3078\u305a\u308b listing and\u4e2d\u6b62link target were not supplied to reviewers; not adopted as new claims or a new usage rule. Whole-deck title uniqueness not established by reviewers; structural validator remains separate.",
            "Existing runtime teaching/metadata and all8438payloadhashes are unchanged in this checkpoint. No newguard applied. Prior full source/baseline/stroke/font audit is retained as execution677, not relabelled as fresh linguistic inspection.",
            "Default-four three kanjichoices accepted textually; actualN1/All/widercustom pools remain runtime gates. Directguard semantic overlap does not establish unrestricted substitution or current production co-occurrence.",
            "All41Han/ninestrokes unchanged; cmapsnotnativelegibility. FreshAndroid/RareHan/native/fourfonts/drawing/reading/N1-All/Back/offline/ContentSyncONCE and dependent rendered review remain.",
            "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Compatibleclientf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
            "Published120/1228 and1108acceptanceremainder unchanged; six separate earlierN2source members\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50 and separate\u5996exception retained. No095 or wholeprojectcompletion.",
            "Original combined-main/normalmerge/changedteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/originalbudgets/media/path/verifiedownerissue gates remain.",
            "Parent19008 retainsrunner.lock untouched; no childacquire/delete/unlock, optional historical-session helper access, actual new permission denial or secondrunner.",
        ],
    }
    save(V / "batch-094-reconciliation.json", rec)
    ledger["initialDraftLimits"] = copy.deepcopy(ledger["limits"])
    ledger.update(
        status=STAGE, initialReviewSnapshot=SNAPSHOT, reviewedTeachingSnapshot=SNAPSHOT,
        textualReviewClosed=False, runtimeAccepted=False, runtimePublished=False,
        nextAction=NEXT,
    )
    ledger["limits"][0] = rec["limits"][0]
    ledger["textualReview"] = {
        "snapshot": SNAPSHOT, "models": rec["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-094-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-094-reconciliation.json"),
        "teachingChanged": False, "textualReviewClosed": False,
        "acceptedUnresolvedDirectQuizPairs": [
            ["\u524a\u308b", "\u9664\u304f"], ["\u524a\u308b", "\u5916\u3059"],
            ["\u524a\u9664", "\u7701\u304f"],
        ],
        "runtimeAccepted": False,
    }
    ledger["pendingGates"] = [
        "Three accepted additive quiz guards, exact ledger/header/baseline audit and normally signed revised local freeze; both serial original-session confirmations and evidence reconciliation.",
        "Fresh non-skipped THREE RealContentTest cases/ONE RareHanTest against actual sibling content.",
        "Full productionContentSyncONCE/native N1/All choices/three directguards/only\u3055\u304f,\u3051\u305a\u308b/ninestroke drawing/articles/SystemBack/offline/all41Han/fourfonts; dependent original-session rendered confirmations.",
        "Combined-current-main integration, substantive teaching re-review if changed, allchecks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/unchangedbudgets/verifiedownerissue.",
    ]
    for row in ledger["supportMappings"]:
        row["status"] = "initial-reviewed-awaiting-quiz-safeguard"
    save(S / "batch-094-progress.json", ledger)
    membership = load(S / "batch-094-membership.json")
    membership["initialDraftLimits"] = copy.deepcopy(membership["limits"])
    membership.update(status=STAGE, initialReviewSnapshot=SNAPSHOT,
                      textualReviewClosed=False, runtimeAccepted=False, runtimePublished=False)
    membership["limits"] = rec["limits"][0]
    save(S / "batch-094-membership.json", membership)
    recipe = S / "batch-094-textual-checkpoint-678.py"
    shutil.copyfile(Path(__file__), recipe)
    shutil.copyfile(C / "preflight-678.ps1", S / "batch-094-textual-preflight-678.ps1.txt")
    save(S / "execution-678.json", {
        "schemaVersion": 1, "execution": 678, "batch": "094", "status": STAGE,
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "startingState": p["execution678StartingState"],
        "reconciliation": "docs/n1-reviews/batch-094-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-094-reconciliation.json"),
        "recipeHashes": {path.relative_to(R).as_posix(): sha(path) for path in [
            recipe, V / "review-batch-094.py", V / "batch-094-serial-review-base-recipe.py",
            S / "batch-094-textual-preflight-678.ps1.txt",
        ]},
        "checks": receipts, "runtimeBytesChanged": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "acceptedQuizPairsPending": 3, "textualReviewClosed": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
    })
    assert not git("diff", SNAPSHOT, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    print("SAME094 original two-family reviews saved; three accepted quiz-guard pairs remain explicitly unresolved.")


def verify_signed():
    head = git("rev-parse", "HEAD")
    assert head != SNAPSHOT and git("rev-parse", "HEAD^") == SNAPSHOT
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == review.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    assert not git("diff", SNAPSHOT, head, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert not review.absent(19008)
    processes()
    rec = load(V / "batch-094-reconciliation.json")
    evidence = load(S / "execution-678.json")
    assert sha(V / "batch-094-reconciliation.json") == evidence["reconciliationSha256"]
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    for name, expected in evidence["recipeHashes"].items():
        assert sha(R / name) == expected
    for info in evidence["checks"].values():
        assert sha(R / info["path"]) == info["sha256"]
    assert rec["actionableRemainingDirectPairs"] == 3 and not rec["textualReviewClosed"]
    return head, rec


def seal():
    head, rec = verify_signed()
    original = load(L / "progress-before-678.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 677 and p["batch"] == "094"
    cp = {
        "schemaVersion": 1, "execution": 678, "checkpoint": 678, "batch": "094",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "evidence": "docs/n1-sources/execution-678.json",
        "sourcePacket": "docs/n1-sources/batch-094-progress.json",
        "reconciliation": "docs/n1-reviews/batch-094-reconciliation.json",
        "textualReviewClosed": False, "runtimeDrafted": ["\u524a"], "reviewClosed": [],
        "published": [], "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionConfirmations": 0, "serialReviewerExitAndScopeReverified": True,
        "bothProcessesOneCallExactFullPacketReturned": True,
        "acceptedUnresolvedFindingGroups": 1, "acceptedUnresolvedDirectQuizPairs": 3,
        "teachingChanged": False, "completeDictionaryFamilies": 121,
        "familyOccurrences": 125, "completeRawCharacterRecords": 10,
        "metadataReadings": 4, "newSupportArticles": 0, "reusedSupportArticles": 2,
        "changedReusedArticles": 3, "allMappedReciprocalPairs": 3,
        "directedLinksVerified": 6, "activatedBaselinePairs": 2,
        "newDirectWordExclusionPairsApplied": 0, "generatedStrokePaths": 9,
        "actualHanCount": 41, "pendingNativeFallbackLabels": ["\u5202", "\u65ab", "\u6c35", "\u961d"],
        "contentVersion": "c054efb36f283dc7", "allRuntimePayloadHashesVerified": 8438,
        "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 120, "remainingAdditions": 1108,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=678, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution678CoordinatorCheckpoint"] = cp
    p["batch094InitialTextualReviewCheckpoint"] = dict(cp)
    p["execution678StartingState"]["status"] = "signed-local-initial-review-checkpoint-complete"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[key] == value for key, value in original.items() if key not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(C / "batch-094-textual-678-seal.json", cp)
    save(L / "checkpoint-678.json", cp)
    print("Verified signed clean checkpoint678:", head)


def issue_body():
    head, rec = verify_signed()
    text = (
        f"Batch094 — two-family initial textual review and evidence adjudication saved at normally "
        f"signed LOCAL checkpoint678 `{head}` (signatureG). NOT textual closure, runtime acceptance "
        "or publication; three accepted direct quiz guards remain to fix.\n\n"
        f"Same frozen draft `{SNAPSHOT}` reviewed serially by actual Claude Opus5.5 "
        "(`claude-opus-5.5`, session edf22897-9f87-4a3b-b20f-4c2fd839013a) then GPT6.1Sol "
        "(`gpt-6.1-sol`, session65fd64ff-aae2-40af-927e-bf19b52fecb6). Each isolated view-only CLI "
        "made exactlyONE full-file read of identical255427byte/5902line packet, with exact full "
        "returned text, no truncation/tooloverlap/missinglines/unfinishedtool; actual process exits "
        "verified before next launch. Packet supplied125completefamilyoccurrences/121distinctJMdict "
        "families (99lexical+26comparison, fourduplicates), tenrawcharacterrecords,24completearticles "
        "and exactdiff/publicdictionaryprovenance. Bytes are not comprehension certification or "
        "independent upstream retrieval. Original complete reports/executions/model/session/read "
        "limits preserved under docs/n1-reviews/batch-094-*.\n\n"
        "New削 and added除 navigation line: correctness/scopedcoverage/phone-TEXT comprehension CLEAN "
        "within scope. Complete reused N2削る and削除: correctness NEEDS FIX for quiz metadata, "
        "coverage/comprehension CLEAN; Japanese examples/translations/forms are sound. Accepted "
        "moderate finding: missing DIRECT 削る/除く,削る/外す and削除/省く guards. Full source families, "
        "actual labels/removal-deletion senses and pairwise/nontransitive contract support three "
        "narrow additive safeguards; actual production co-occurrence remains untested. No fixes "
        "applied or original exclusions removed at this checkpoint. GPT uniquely raised firsttwo "
        "pairs; Claude's low-risk hypothesis already mentions削除/省く, so that observation is shared, "
        "not credited as uniquely GPT. No model vote or broad synonym clique. Claude wording/"
        "extra-example/passive-past suggestions remain optional, not mandatory defects.\n\n"
        "Fullサク andけず.る/はつ.る/そ.ぐ sourceorder retained, explicit[サク]/[けず.る] "
        "offersさく/けずる through own linked existing N2 articles. Separateはつる is not linked "
        "asけずる;そぐ's kanaflag remains sense-local. No new support article or prose rewrite. "
        "Three allmappedpairs/sixdirections, twoactivatedbaselinepairs, ninepinnedgeneratedstrokes "
        "and41scopedHan unchanged;刂/斫/氵/阝 cmap absence is NOT glyphfailure.\n\n"
        "Fresh validator0, regenerated unchanged manifestc054efb36f283dc7,43focusedtests, current "
        "batch baseline/link/membership/reading/quiz audit, vocabularyconsistency and original "
        "archivebudget check passed; all8438runtimepayloadhashes verified. Earlier complete frozen-"
        "source/baseline/font/stroke audit retained as execution677, not relabelled as fresh "
        "linguistic review. Runtime bytes unchanged.\n\n"
        "Next SAME094 bounded checkpoint: apply only THREE directguards with exactledger/"
        "baseline/validator/manifest checks, normal signedLOCAL revisedfreeze, then serial "
        "original-session Claude/GPT changed-passage confirmations and evidence reconciliation. "
        "Do not mark textualclosure until defects resolved. Fresh non-skippedAndroid/"
        "productionContentSyncONCE/fullarchive/N1-All choices/threeguards/reading/ninestroke"
        "drawing/articles/SystemBack/offline/all41Han/fourfonts and original-session rendered "
        "confirmations remain, then combined-current-main/normalmerge/signing/ownerfastforward/"
        "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchangedbudgets/verifiedownerissue. "
        "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain.\n\n"
        "Published120/1228 and1108acceptanceremainder unchanged; lastpublishedmain"
        "48765e20846e1d6769c6ddc35146f6ce58deab57. Compatibleclientf9b59a2+ required; "
        "physicalphone/generalrelease/whole-set explicitly outstanding. No095 or unreviewed push. "
        "Parent19008 ownsrunner.lock untouched; no childacquire/delete/unlock, optional historical-"
        "sessionhelperaccess, actualnewpermissiondenial or secondrunner. Dedicatedworktrees clean; "
        "progress.json preserves complete history with statuscontinue."
    )
    (C / "batch-094-textual-678-issue-body.txt").write_text(text, encoding="utf-8")
    print("Verified signed checkpoint and prepared owner issue update.")


def final():
    head, rec = verify_signed()
    path = C / "batch-094-textual-678-issue-body.txt"
    posted = load(C / "batch-094-textual-678-issue-posted.json")
    actual = load(C / "batch-094-textual-678-issue-reread.json")
    assert actual["id"] == posted["id"] and actual["user"]["login"] == "stop-cran"
    assert actual["body"].encode("utf-8") == path.read_bytes()
    receipt = {
        "id": actual["id"], "url": actual["html_url"], "author": actual["user"]["login"],
        "bodySha256": sha(path), "verified": True,
        "comparison": "Exact UTF-8 bytes, no line-ending normalization.",
    }
    save(C / "batch-094-textual-678-issue-receipt.json", receipt)
    p = load(C / "progress.json")
    original = load(L / "progress-before-678.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (678, "094", "continue")
    assert p["stage"] == STAGE and p["nextAction"] == NEXT and p["blocker"] is None
    assert p["remainingAdditions"] == original["remainingAdditions"] == 1108
    assert p["lastPublishedCommit"] == original["lastPublishedCommit"]
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    for key in ["execution678CoordinatorCheckpoint", "batch094InitialTextualReviewCheckpoint"]:
        assert p[key]["savedCommit"] == head
        p[key]["issueUpdate"] = receipt["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    p["batch094InitialTextualReviewIssueReceipt"] = receipt
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(L / "checkpoint-678.json", p["execution678CoordinatorCheckpoint"])
    save(C / "batch-094-textual-678-final-verification.json", {
        **p["execution678CoordinatorCheckpoint"],
        "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True,
        "serialReviewerExitAndScopeReverified": True,
        "ownerIssueAuthorAndBodyVerified": True,
    })
    print("Verified signed clean checkpoint678,", len(original), "historical root values preserved:", receipt["url"])


if __name__ == "__main__":
    {"prepare": prepare_checkpoint, "seal": seal, "body": issue_body, "final": final}[sys.argv[1]]()
