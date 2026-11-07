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
spec = importlib.util.spec_from_file_location("review093", C / "review-batch-093.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
review = module.review
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
load, sha, git = review.load, review.sha, review.git
SNAPSHOT = review.SNAPSHOT
STAGE = "textually-review-closed-awaiting-fresh-android"
NEXT = (
    "SAME093 fresh non-skipped sibling Android RealContentTest THREE cases and RareHanTest ONE case "
    "against THIS content tree; preserve exact XML/provenance and normally signed local evidence, then yield. "
    "Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d retains productionf9b59a2, "
    "not latest app main. Explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot "
    "and ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, one Gradle worker and "
    "quoted '-Pkotlin.compiler.execution.strategy=in-process'. Parent19008 already owns runner.lock; "
    "NO child reacquisition/delete/unlock or parent-only recovery wrapper copy. Keep exact signed-head/"
    "checkpoint/wholly-clean-worktree/verified-parent-ancestry checks; preserve/report/yield actual new denial, "
    "signing hang or uncertain ownership. Textual093 closed after serial blind Claude/GPT initials on27663944; "
    "no proved teaching defect, consequential unresolved claim or teaching edit. Full rawケイ/emptykun "
    "retained; explicit[ケイ]/[] selects onlyけい through own linked existing N3刑事 row. "
    "Special whole-wordでか and outside-freezeギョウ remain distinguished. One new刑card/six generated "
    "paths, no new support word; reused N3刑事 adds component link/four DIRECT police-label guards only, "
    "preserving identity/reading/title/level/inbound探偵guard; 事 adds reciprocal navigation only. "
    "Two all-mapped pairs/four directions, one activated baseline刑/刑事 pair (NOT事/刑事; GPT report "
    "bookkeeping corrected in reconciliation without changing original). Later native gate requires "
    "all46 scopedHan especially亅/刂/彡 across FOUR productionfont families, SIX pinned drawingstrokes, "
    "onlyonけい/nokun keys, articles/SystemBack/offline, actualN1/All productionchoices and four direct "
    "police guards, fullarchive productionContentSync ONCE with terminalcase0/no skips. Cmapabsence "
    "notglyphfailure; originalsessions retained for dependent visuals, no newblindcredit. All original "
    "source/baseline/link/reading/twofamily/native/currentmain-normalmerge/substantiveteachingreview/checks/"
    "normal-signing/owner-fastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries"
    "42MiBcompressed80MiBinflated56MiBretained/media/path/ownerissue gates remain. Published119/1228 and1109 "
    "acceptanceremainder unchanged; physicalphone/generalrelease/whole-set outstanding. No094, native/"
    "reviewer/publication or secondrunner in next hostcheckpoint. Approved control/committed evidence/"
    "frozen inputs only; no optional historical-session helper access."
)


def save(path, value):
    temp = path.with_suffix(path.suffix + ".669.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def processes():
    result, prior = {}, None
    for label, model in review.MODELS.items():
        prefix = f"batch-093-initial-{label}"
        record = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert record["exitCode"] == 0 and record["actualModels"] == [model]
        assert record["usageCurrentModel"] == model
        assert record["multiToolResponseCount"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert coverage["allAssignedRangesReturned"]
        assert len(record["toolCalls"]) == (2 if label == "claude" else 3)
        first = record["toolCalls"][0]
        assert first["name"] == "view" and first["success"]
        assert first["exactRequestedTextContainedInResult"] and not first["truncationMarker"]
        assert all(call["name"] == "view" and call["success"] for call in record["toolCalls"])
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
            "toolCalls": len(record["toolCalls"]), "observedToolOverlaps": 0,
            "firstCallExactFullPacketReturned": True,
            "redundantTailReads": [
                {"range": call["arguments"]["view_range"],
                 "truncated": call["truncationMarker"],
                 "exactRequestedTextContainedInResult": call["exactRequestedTextContainedInResult"]}
                for call in record["toolCalls"][1:]
            ],
        }
    return result


def close():
    review.frozen()
    records = processes()
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 668 and p["batch"] == "093"
    ledger = load(S / "batch-093-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    assert review.PACKET.read_bytes() == (V / review.PACKET.name).read_bytes()
    ledger.update(
        status=STAGE, initialReviewSnapshot=SNAPSHOT, reviewedTeachingSnapshot=SNAPSHOT,
        reviewClosed=["刑"], textualReviewClosed=True, runtimeAccepted=False,
        runtimePublished=False, nextAction=NEXT,
    )
    ledger["initialDraftLimits"] = copy.deepcopy(ledger["limits"])
    ledger["limits"][0] = (
        "Textual review closed only, with unchanged runtime teaching. Both serial blind model-family "
        "reviews found no actionable teaching defect. Fresh Android/native/font/visual and publication gates pending."
    )
    ledger["pendingGates"] = [
        "Fresh non-skipped RealContentTest/RareHanTest against this sibling content worktree.",
        "All46 scopedHan/four-font native rendering, especially亅/刂/彡; six-stroke drawing, "
        "production full ContentSync ONCE, onlyonけい/nokun, N1/All meaning choices/four direct guards, "
        "article/Back/offline assertions and dependent original-session rendered confirmation.",
        "Combined current-main non-rewriting merge, substantive teaching re-review if changed, "
        "all required checks/normal signing/owner fast-forward push/terminal green CI/"
        "EVERY immutable ZIP runtime hash/original budgets/verified owner issue.",
    ]
    ledger["supportMappings"][0]["status"] = "textually-review-closed"
    ledger["quizAudit"]["刑"]["limits"] = (
        "Both independent textual reviews accept these three N1-available wrong labels; default-four "
        "fallback not required. Production N1/All options and wider live pools remain later runtime gates."
    )
    save(S / "batch-093-progress.json", ledger)
    membership = load(S / "batch-093-membership.json")
    membership["initialDraftLimits"] = membership["limits"]
    membership.update(status=STAGE, reviewClosed=["刑"], textualReviewClosed=True,
                      runtimeAccepted=False, runtimePublished=False)
    membership["limits"] = "Textual closure only; native/runtime/publication and whole-set acceptance remain pending."
    save(S / "batch-093-membership.json", membership)
    receipts = {}
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "093"],
        "tests": [
            sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
            "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources",
        ],
        "vocabulary": [sys.executable, "-B", str(R / "tools" / "grammar_vocabulary.py"), "check"],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
    }
    for name, command in commands.items():
        path = V / f"batch-093-textual-review-{name}-669.txt.gz"
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

    mechanical = audit(R, "093")
    assert mechanical == json.loads(gzip.decompress(
        (V / "batch-093-textual-review-audit-669.txt.gz").read_bytes()))
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "bf4cc85592bb9727"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8436
    for source in load(V / "batch-093-review-dictionary-provenance.json")["sources"]:
        assert sha(Path(source["path"])) == source["sha256"]
    reviewed = {name: sha(R / name) for name in [
        "kanji/刑.md", "words/刑事.md", "kanji/事.md", "strokes/刑.json", "manifest.json",
    ]}
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    rec = {
        "schemaVersion": 1, "execution": 669, "batch": "093", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False, "reviewedRuntimeHashes": reviewed,
        "initialModels": list(review.MODELS.values()), "processes": records,
        "confirmations": {}, "serialReviewerProcessesVerified": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": review.PACKET.stat().st_size, "initialPacketLines": 5392,
        "initialDistinctCompleteFamilies": 180, "lexicalFamilies": 157,
        "comparisonFamilies": 23, "rawCharacterRecords": 8,
        "completeArticleBodiesSupplied": 15, "newArticleBodies": 1, "changedReusedBodies": 2,
        "verdicts": {name: {
            "correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN",
            "scope": scope,
        } for name, scope in [
            ("kanji/刑.md", "complete new article"),
            ("words/刑事.md", "complete reused article and exact link/four-guard diff"),
            ("kanji/事.md:37", "added reciprocal-navigation line only; complete article supplied for context"),
        ]},
        "findings": [],
        "hypothesisDispositions": [
            {
                "reportedBy": "Claude", "claim": "Older model/form wording is not an explicit archaic flag in Daijisen.",
                "status": "optional",
                "decision": "No edit. The note recognizes the additional senses and explicitly rejects semantic disconnection; it neither labels all model/form compounds obsolete nor prohibits current usage. Both reviewers accept its scoped qualified wording. No dating or frequency inference is certified.",
                "evidence": "刑.md:45; Daijisen character senses2/3 (型/形通用) and complete JMdict1592030儀刑/儀型/儀形. Recognition is established; a historical dating claim is not added.",
            },
            {
                "reportedBy": "Claude", "claim": "文 sentence/writing may overlap in wider quiz pools.",
                "status": "unresolved",
                "scope": "later runtime/custom-pool limitation, not an established textual defect",
                "decision": "Default-four uses three explicit semantically wrong choices. Legal-versus-grammatical sentence is explicit; retain actual N1/All production-choice gate. Do not claim arbitrary pool certification.",
            },
        ],
        "reviewReportCorrections": [
            {
                "reportedBy": "GPT", "claim": "Activated baseline pair is事/刑事.",
                "status": "withdrawn", "decision": "Coordinator accounting correction only; preserve original report verbatim. Newly introduced刑 activates baseline刑/刑事, not the existing事/刑事 pair. The two-pair/four-direction count is correct.",
                "evidence": "batch-093-progress.json activatedBaselinePairs and basefe9e1a37:words/刑事.md metadata [刑,事]; base has事card but no刑card. Current changed component link is刑, current new事line closes the additional mapped pair.",
            },
        ],
        "optionalDispositions": [
            {
                "reportedBy": ["Claude"], "claim": "Translate witness example as is questioning a witness.",
                "status": "optional", "decision": "No edit. Existing is talking to a witness accurately conveys contextual話を聞いています; GPT independently accepts it. Stronger English questioning is not required.",
            },
            {
                "reportedBy": ["Claude"], "claim": "Mention katakanaデカ and add a pointer to reused刑事.",
                "status": "optional", "decision": "No edit. Whole-word slangでか is already explained in new刑; no new support article or exhaustive slang lesson is needed.",
            },
            {
                "reportedBy": ["Claude"], "claim": "Wrong labels are unambiguous but not very believable.",
                "status": "optional", "decision": "No edit. These approved existing N1 choices preserve a single defensible answer; shape comparisons形/型remain useful teaching but unsafe wrong answers. No proved defect.",
            },
            {
                "reportedBy": ["GPT"], "claim": "Explain detective designation is not a police rank.",
                "status": "optional", "decision": "No edit. The current two senses do not equate role with a rank. Public dictionaries corroborate optional clarification; the bounded article need not survey police ranks.",
            },
        ],
        "modelContributionComparison": {
            "shared": "Bothaccept complete刑/刑事andadded事line, readings/curation/specialwholeword/outsidefreeze, legal-role boundaries, examples/translations, shape-onlymnemonic/radicalvariant, threewrongkanjilabels, fourdirectguards and two mapped pairs/four directions.",
            "claudeUnique": "Nonblocking temporal-wording hypothesis, optional stronger witness translation, slangpointer and distractor plausibility. Wider custom-pool concern is also present in GPT limits, not unique. No unique verified mandatory defect.",
            "gptUnique": "Optional not-a-rank clarification; original report misidentifies activated baseline pair, corrected above from actual baseline. No unique verified mandatory defect.",
            "limits": "Common snapshot/task/source access; equivalent observations compared across findings/optional/hypotheses/limits/supportingnotes. No general model ranking, finding quota, native-speaker certification or equal comprehension claim.",
        },
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "previousCompleteSourceBaselineFontStrokeAudit": "docs/n1-sources/batch-093-draft-audit.json",
        "previousCompleteSourceBaselineFontStrokeAuditSha256": sha(S / "batch-093-draft-audit.json"),
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairs": 4, "actualHanCount": 46, "nativeFontPending": ["亅", "刂", "彡"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "newNativeOrAndroidClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT,
        "limits": [
            "Textual closure only. No fresh Android/native/font/visual/phone or runtime publication acceptance.",
            "Both actual families received identical222131byte/5392line packet,180completefamilies/eightcharacterrecords/15completearticles. First full-file view returned exact full packet in each process. Claude then made one redundant tail read; GPT two, first of which truncated then recovered. All reads serial, no missing packet lines or active tools; actual process exits verified.",
            "Returned bytes are not equal comprehension certification. Claude reports counting23comparisonfamilies but not manually tallying157lexicalfamilies, while reading all. Original reports, raw executions, actual model/session/tool ranges retained.",
            "Public text is coordinator-supplied committed extraction, not independent upstream retrieval. Missing gaiji prevents historical verification; dictionary presence is not frequency. No additional historical dating is certified.",
            "No teaching edit or dependent textual confirmation was necessary. Original sessions retained for required later rendered confirmations. GPT report baseline-pair error corrected explicitly without altering original report.",
            "Complete earlier source/baseline/font/stroke audit retained as execution668, not relabelled as fresh full source inspection. Fresh current baseline/runtime/link/reading/quiz audit and all8436manifestpayloadhashes verified; runtime/source bytes unchanged.",
            "One new刑card, no new support word, N3刑事identity/reading/title/level preserved; only component link/four direct safeguards and事navigation changed. Fullケイ/emptykun retained, onlyけいoffered; specialでかandpublicギョウdistinct.",
            "All46Han/sixstrokesunchanged; cmapsnotnativelegibility. Fresh四font/亅刂彡/native/drawing/N1-All/reading/Back/offline/ContentSyncONCE and dependent rendered review gates remain.",
            "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latestappmain. Compatibleclientf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
            "Published119/1228,1109acceptanceremainder unchanged; separate earlierN2source保案派第策結 and separate妖exception retained. No094 or wholeprojectcompletion.",
            "All original normalmerge/substantiveteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/media/path/ownerissue gates remain.",
            "Parent19008retainsrunner.lock untouched; no child acquisition/deletion/unlocking. Approved control/committed packets/frozen inputs only; no optional historical-session-helper access or actual new permission denial.",
        ],
    }
    save(V / "batch-093-reconciliation.json", rec)
    ledger["textualReview"] = {
        "snapshot": SNAPSHOT, "models": rec["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-093-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-093-reconciliation.json"),
        "teachingChanged": False, "textualReviewClosed": True, "runtimeAccepted": False,
    }
    save(S / "batch-093-progress.json", ledger)
    recipe = S / "batch-093-textual-closure-recipe.py"
    shutil.copyfile(Path(__file__), recipe)
    save(S / "execution-669.json", {
        "schemaVersion": 1, "execution": 669, "batch": "093", "status": STAGE,
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "startingState": p["execution669StartingState"],
        "reconciliation": "docs/n1-reviews/batch-093-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-093-reconciliation.json"),
        "recipeHashes": {
            path.relative_to(R).as_posix(): sha(path) for path in [
                recipe, V / "review-batch-093.py", V / "batch-093-serial-review-base-recipe.py",
            ]
        },
        "checks": receipts, "runtimeBytesChanged": False,
        "publishedAdditions": 119, "remainingAdditions": 1109,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [],
        "diagnostics": [
            "Two guessed durable helper filenames did not exist; discovered actual control close-batch-092-textual.py and batch-093-draft-668.py. No denied access or historical-session helper probe.",
            "Initial checkpoint property-count display emitted an overlarge index; full request parsed successfully and final checkpoint inspected. No dependency on truncated temporary output.",
        ],
        "nextAction": NEXT,
    })
    print("SAME093 textual review closed; runtime unchanged and fresh Android gate remains.")


def seal():
    head = git("rev-parse", "HEAD")
    assert head != SNAPSHOT and git("rev-parse", "HEAD^") == SNAPSHOT
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == review.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    assert not git("diff", SNAPSHOT, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    processes()
    rec = load(V / "batch-093-reconciliation.json")
    execution = load(S / "execution-669.json")
    assert sha(V / "batch-093-reconciliation.json") == execution["reconciliationSha256"]
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    original = load(L / "progress-before-669.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 668 and p["batch"] == "093"
    cp = {
        "schemaVersion": 1, "execution": 669, "checkpoint": 669, "batch": "093",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "evidence": "docs/n1-sources/execution-669.json",
        "sourcePacket": "docs/n1-sources/batch-093-progress.json",
        "reconciliation": "docs/n1-reviews/batch-093-reconciliation.json",
        "textualReviewClosed": True, "runtimeDrafted": ["刑"], "reviewClosed": ["刑"],
        "published": [], "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionConfirmations": 0, "serialReviewerExitAndScopeReverified": True,
        "allTwoProcessesFirstCallExactFullPacketReturned": True,
        "redundantTailReads": {"claude": 1, "gpt": 2}, "gptRedundantTailTruncationRecovered": True,
        "mandatoryTeachingFindings": 0, "consequentialUnresolvedTeachingClaims": 0,
        "reviewReportBaselinePairAccountingCorrected": True, "teachingChanged": False,
        "completeDictionaryFamilies": 180, "completeRawCharacterRecords": 8,
        "metadataReadings": 1, "newSupportArticles": 0, "reusedSupportArticles": 1,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairs": 4, "generatedStrokePaths": 6,
        "actualHanCount": 46, "pendingNativeFallbackLabels": ["亅", "刂", "彡"],
        "contentVersion": "bf4cc85592bb9727", "allRuntimePayloadHashesVerified": 8436,
        "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 119, "remainingAdditions": 1109,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=669, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution669CoordinatorCheckpoint"] = cp
    p["batch093TextualReviewCheckpoint"] = dict(cp)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[key] == value for key, value in original.items() if key not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(C / "batch-093-textual-669-seal.json", cp)
    print("Verified signed clean checkpoint669:", head)


if __name__ == "__main__":
    {"close": close, "seal": seal}[sys.argv[1]]()
