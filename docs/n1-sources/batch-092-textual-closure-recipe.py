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
spec = importlib.util.spec_from_file_location("review092", C / "review-batch-092.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
review = module.review
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
load, sha, git = review.load, review.sha, review.git
SNAPSHOT = review.SNAPSHOT
STAGE = "textually-review-closed-awaiting-fresh-android"
NEXT = (
    "SAME092 fresh non-skipped sibling Android RealContentTest THREE cases and RareHanTest ONE case "
    "against THIS content tree; preserve exact XML/provenance and normally signed local evidence, then yield. "
    "Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d retains productionf9b59a2, "
    "not latest app main. Explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot "
    "and ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, one Gradle worker and "
    "quoted '-Pkotlin.compiler.execution.strategy=in-process'. Parent19008 already owns runner.lock; "
    "NO child reacquisition/delete/unlock or parent-only recovery wrapper copy. Keep exact signed-head/"
    "checkpoint/wholly-clean-worktree/verified-parent-ancestry checks; preserve/report/yield actual new denial, "
    "signing hang or uncertain ownership. Textual092 closed after serial blind Claude/GPT initials on6246dc62; "
    "no proved defect, consequential unresolved claim or teaching edit. Three raw readings ガイ/カイ/か.る "
    "retained in order; onlyか.る selected with own linked existing N3刈る row and offeredかる. Both刈除 "
    "readings recognized/unselected, not source-only/obsolete. One new刈card, no new support word; reused "
    "N3刈る preserves identity/reading/title/level/original切るguard, adds component link/direct収穫guard only. "
    "Shape-only mnemonic/刀-visible刂 distinction, three N1 wrong labels, one all-mapped/baseline pair/two "
    "directions. Later native gate requires all16 scopedHan especially刂 across FOUR productionfont families, "
    "FOUR pinned drawingstrokes, onlykunかる/noon keys, both articles/SystemBack/offline, actualN1/All "
    "productionchoices, fullarchive productionContentSync ONCE with terminalcase0/no skips. Cmapabsence "
    "notglyphfailure; originalsessions retained for dependent visuals, no newblindcredit. All original "
    "source/baseline/link/reading/twofamily/native/currentmain-normalmerge/substantiveteachingreview/checks/"
    "normal-signing/owner-fastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries"
    "42MiBcompressed80MiBinflated56MiBretained/media/path/ownerissue gates remain. Published118/1228 and1110"
    "acceptanceremainder unchanged; physicalphone/generalrelease/whole-set outstanding. No093, native/"
    "reviewer/publication or secondrunner in next hostcheckpoint. Approved control/committed evidence/"
    "frozen inputs only; no optional historical-session helper access."
)


def save(path, value):
    temp = path.with_suffix(path.suffix + ".660.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def processes():
    result = {}
    prior = None
    for label, model in review.MODELS.items():
        prefix = f"batch-092-initial-{label}"
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


def close():
    review.frozen()
    records = processes()
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 659 and p["batch"] == "092"
    ledger = load(S / "batch-092-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    assert review.PACKET.read_bytes() == (V / review.PACKET.name).read_bytes()
    ledger.update(
        status=STAGE, initialReviewSnapshot=SNAPSHOT, reviewedTeachingSnapshot=SNAPSHOT,
        reviewClosed=["刈"], textualReviewClosed=True, runtimeAccepted=False,
        runtimePublished=False, nextAction=NEXT,
    )
    ledger["initialDraftLimits"] = copy.deepcopy(ledger["limits"])
    ledger["limits"][0] = (
        "Textual review closed only, with unchanged runtime teaching. Both serial blind model-family "
        "reviews found no actionable defect. Fresh Android/native/font/visual and publication gates pending."
    )
    ledger["pendingGates"] = ledger["pendingGates"][3:]
    ledger["pendingGates"][0] = (
        "Fresh non-skipped RealContentTest and RareHanTest on qualified dedicated Android, actual "
        "16Han/four-font native rendering, production full ContentSync ONCE with unchanged limits, "
        "curated keys, N1/All meaning choices, four-stroke drawing/article/Back/offline assertions "
        "and dependent original-session rendered confirmation."
    )
    ledger["supportMappings"][0]["status"] = "textually-review-closed"
    ledger["quizAudit"]["刈"]["limits"] = (
        "Both independent textual reviews accept these three N1-available wrong labels; default-four "
        "fallback not required. Production N1/All options and wider live pools remain later runtime gates."
    )
    save(S / "batch-092-progress.json", ledger)
    receipts = {}
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "092"],
        "tests": [
            sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
            "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources",
        ],
        "vocabulary": [sys.executable, "-B", str(R / "tools" / "grammar_vocabulary.py"), "check"],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
    }
    for name, command in commands.items():
        path = V / f"batch-092-textual-review-{name}-660.txt.gz"
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

    mechanical = audit(R, "092")
    assert mechanical == json.loads(gzip.decompress(
        (V / "batch-092-textual-review-audit-660.txt.gz").read_bytes()))
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "8445a5717d080dcc"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8434
    assert (R / "words" / "髪.md").is_file()
    from audit_n1_pilot import metadata
    titles = [metadata(R, f"kanji/{path.name}")["title"] for path in (R / "kanji").glob("*.md")]
    assert titles.count("mow; reap") == 1
    reviewed = {name: sha(R / name) for name in [
        "kanji/刈.md", "words/刈る.md", "strokes/刈.json", "manifest.json",
    ]}
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    optional = [
        {
            "claim": "Hair example may also translate as I cropped my hair short.",
            "reportedBy": ["Claude optional", "GPT supporting assessment"],
            "status": "optional",
            "decision": "No edit. Both explicitly accept the existing contextual service reading; it does not assert that Japanese must be causative.",
        },
        {
            "claim": "Add kana for 刈った and 刈らない in reused N3 support.",
            "reportedBy": ["Claude"], "status": "optional",
            "decision": "No edit. Forms are correct and complete selected-reading support is already provided; no actionable comprehension defect established.",
        },
        {
            "claim": "Add a one-line contrast with 収穫 to explain the new exclusion.",
            "reportedBy": ["Claude"], "status": "optional",
            "decision": "No edit. Existing distinctive-meaning paragraph explains the cutting-versus-every-harvest boundary; the guard addresses overlapping labels, not unrestricted synonyms.",
        },
    ]
    limits = [
        "Textual closure only. No fresh Android/native/font/visual/phone or runtime publication acceptance.",
        "Both actual families received the same 162352byte/3624line packet with75completeJMdictfamilies, six raw character records and13completearticles. Each used one full-file view; exact returned full text, no truncation/overlap and process exit verified. Byte access is not comprehension or equal fresh-read-depth certification.",
        "Both complete original reports and original sessions retained; no mandatory finding or consequential unresolved textual claim. No teaching fix or dependent textual confirmation was necessary. Later rendered confirmations remain required in original sessions where possible.",
        "Public dictionary text is coordinator-supplied committed extraction, not independent upstream retrieval. Dictionaries establish recognition, not frequency. Jitsu corroboratesガイ only; both刈除readings are independently present in the frozen JMdict family.",
        "All three raw readings ガイ/カイ/か.る preserved in order; onlyか.る selected through existing N3刈る. No new support words, altered primary reading/level/title, hidden reading deletion or incidental backlink quota.",
        "One all-mapped/baseline pair and two directions; original切るguard retained, direct収穫guard added. Inbound剃る/取り入れるguards unchanged. No transitive clique or universal live-pool certification.",
        "Original draft source/baseline/font/stroke audit retained as historical execution659 evidence, not relabelled as fresh full source inspection in660. Current base/runtime/link/reading/quiz audit and every8434manifestpayloadhash freshly verified; five frozen-input hashes and baseline evidence remain valid via unchanged content/source bytes.",
        "All16scopedHan and four ordered generated strokes unchanged. Three main bundled cmaps lack刂; absence is not glyph failure. Fresh four-font/native/drawing/Back/offline/N1-All/ContentSyncONCE and dependent rendered review gates remain.",
        "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latestappmain. Compatibleclientf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
        "Published118/1228,1110acceptanceremainder unchanged. Separate earlierN2source保案派第策結 and separate妖exception retained; no093, nextbatch or project completion.",
        "All original normalmerge/substantiveteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemedia/path/ownerissue gates remain.",
        "Parent19008retainsrunner.lock untouched; no child acquisition/deletion/unlocking. Approved control/committed packets/frozen inputs only, no optional historical-session-helper access or actual new permission denial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 660, "batch": "092", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False, "reviewedRuntimeHashes": reviewed,
        "initialModels": list(review.MODELS.values()), "processes": records,
        "confirmations": {}, "serialReviewerProcessesVerified": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True,
        "allInternalToolsSerial": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": review.PACKET.stat().st_size, "initialPacketLines": 3624,
        "initialDistinctCompleteFamilies": 75, "lexicalFamilies": 62,
        "comparisonFamilies": 13, "rawCharacterRecords": 6,
        "completeArticleBodiesSupplied": 13, "newArticleBodies": 1, "changedReusedBodies": 1,
        "verdicts": {name: {
            "correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN",
            "scope": "complete new article" if name.startswith("kanji") else "complete reused article and exact link/guard diff",
        } for name in ["kanji/刈.md", "words/刈る.md"]},
        "findings": [], "hypothesisDispositions": [], "optionalDispositions": optional,
        "modelContributionComparison": {
            "shared": "Bothaccept completekanji/reusedsupport, readings/curation/recognition, examples/translations/godan/particles, cutting-versus-harvesting boundaries, shape-onlymnemonic/radicalvariant, threewrongkanjilabels, directguards and onepair/twodirections.",
            "claudeUnique": "Two additional nonblocking suggestions: kana on two inflections, and one explicit収穫contrast. No unique verified mandatory defect. Hairtranslation observation is also in GPT supporting assessment, not a unique discovery.",
            "gptUnique": "No unique verified mandatory defect; explicitly accepts contextual service translation and ordinary-versus-specialized scope.",
            "limits": "Common snapshot/task/source access; compare equivalent observations across findings/optional/limits/supportingnotes. No finding quota, general model ranking, native-speaker certification or equal comprehension claim.",
        },
        "mechanicalLimitsResolved": {
            "reportedBy": "Claude Limits",
            "claims": ["words/髪.md target not independently checked", "title uniqueness not independently checked"],
            "decision": "Coordinator verified actual link target and exactly one mow; reap kanji title. Reviewer independent-verification limitation remains; no linguistic finding manufactured.",
        },
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "previousCompleteSourceBaselineFontStrokeAudit": "docs/n1-sources/batch-092-draft-audit.json",
        "previousCompleteSourceBaselineFontStrokeAuditSha256": sha(S / "batch-092-draft-audit.json"),
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairs": 1, "actualHanCount": 16, "nativeFontPending": ["刂"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "newNativeOrAndroidClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    save(V / "batch-092-reconciliation.json", rec)
    ledger["textualReview"] = {
        "snapshot": SNAPSHOT, "models": rec["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-092-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-092-reconciliation.json"),
        "teachingChanged": False, "textualReviewClosed": True, "runtimeAccepted": False,
    }
    save(S / "batch-092-progress.json", ledger)
    recipe = S / "batch-092-textual-closure-recipe.py"
    shutil.copyfile(Path(__file__), recipe)
    save(S / "execution-660.json", {
        "schemaVersion": 1, "execution": 660, "batch": "092", "status": STAGE,
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "startingState": p["execution660StartingState"],
        "reconciliation": "docs/n1-reviews/batch-092-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-092-reconciliation.json"),
        "recipeHashes": {
            str(path.relative_to(R).as_posix()): sha(path) for path in [
                recipe, V / "review-batch-092.py", V / "batch-092-serial-review-base-recipe.py",
            ]
        },
        "checks": receipts, "runtimeBytesChanged": False,
        "publishedAdditions": 118, "remainingAdditions": 1110,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [],
        "diagnostics": [
            "Initial helper import used archived recipe-relative paths and stopped at git before any writes. Explicitly rebound dedicated workspace paths/default repo; no source access denial or gate waiver.",
            "A post-exit Get-Process check returned no processes and PowerShell exit1; actual reviewer exit and seriality independently confirmed from awaited child/process receipts.",
        ],
        "nextAction": NEXT,
    })
    print("SAME092 textual review closed; runtime unchanged and fresh Android gate remains.")


def seal():
    head = git("rev-parse", "HEAD")
    assert head != SNAPSHOT and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == review.ANDROID
    assert not git("status", "--porcelain", repo=A)
    assert not git("diff", SNAPSHOT, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    processes()
    rec = load(V / "batch-092-reconciliation.json")
    execution = load(S / "execution-660.json")
    assert sha(V / "batch-092-reconciliation.json") == execution["reconciliationSha256"]
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    original = load(L / "progress-before-660.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 659 and p["batch"] == "092"
    cp = {
        "schemaVersion": 1, "execution": 660, "checkpoint": 660, "batch": "092",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "evidence": "docs/n1-sources/execution-660.json",
        "sourcePacket": "docs/n1-sources/batch-092-progress.json",
        "reconciliation": "docs/n1-reviews/batch-092-reconciliation.json",
        "textualReviewClosed": True, "runtimeDrafted": ["刈"], "reviewClosed": ["刈"],
        "published": [], "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionConfirmations": 0, "serialReviewerExitAndScopeReverified": True,
        "allTwoProcessesOneCallExactFullPacketReturned": True,
        "mandatoryFindings": 0, "consequentialUnresolvedClaims": 0, "teachingChanged": False,
        "completeDictionaryFamilies": 75, "completeRawCharacterRecords": 6,
        "metadataReadings": 3, "newSupportArticles": 0, "reusedSupportArticles": 1,
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairs": 1, "generatedStrokePaths": 4,
        "actualHanCount": 16, "pendingNativeFallbackLabels": ["刂"],
        "contentVersion": "8445a5717d080dcc", "allRuntimePayloadHashesVerified": 8434,
        "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 118, "remainingAdditions": 1110,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=660, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution660CoordinatorCheckpoint"] = cp
    p["batch092TextualReviewCheckpoint"] = dict(cp)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[key] == value for key, value in original.items() if key not in allowed)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(C / "batch-092-textual-660-seal.json", cp)
    print("Verified signed clean checkpoint660:", head)


if __name__ == "__main__":
    {"close": close, "seal": seal}[sys.argv[1]]()
