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
spec = importlib.util.spec_from_file_location("batch097", C / "review-batch-097.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.review
R, A, S, V, L = r.R, r.A, r.S, r.V, r.L
load, sha, git = r.load, r.sha, r.git
SNAPSHOT = r.SNAPSHOT
STAGE = "batch-097-textual-review-closed-awaiting-android-native"
NEXT = (
    "SAME097 fresh non-skipped THREE RealContentTest and ONE RareHanTest against THIS sibling next; "
    "textual closure ONLY on signed1fa1ac69, NOT native or full batch acceptance. "
    "Actual ClaudeOpus5.5 original session3a0b6dd8-6212-4ceb-a430-3127aac6969e and GPT6.1Sol "
    "original session9f31594c-f091-4d47-9276-12249f0c848d completed serial blind initial reviews "
    "on SAME240886byte/5345line packet:137distinct complete dictionary families/139occurrences, "
    "11raw records,22complete article bodies including new剣/剣つるぎ and exact reused真剣/真 changes. "
    "Both returned exact whole packet in ONE serial view; reports/models/sessions/process/read limits archived. "
    "No actionable textual defect or consequential unresolved teaching claim; no teaching edit, so no dependent "
    "textual fix confirmation needed. Frequency hypothesis/old-form/clock-hand/zoology expansions remain "
    "unproved or optional; actual N1/All/custom/random/legacy fallback safety remains runtime gate. "
    "Use explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot and "
    "ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, oneGradleworker and quoted "
    "'-Pkotlin.compiler.execution.strategy=in-process'; inspect terminal test cases and actual sibling path. "
    "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain. Then fresh fullarchive "
    "productionContentSync ONCE/native N1-All actual choices/FOURdirectguards/けん+つるぎ/tenstroke "
    "drawing/complete剣 and剣つるぎ articles/reusedlinks/SystemBack/offline/all20Han/fourfonts with fresh "
    "safe port/device ownership checks; 刂cmap absence NOT glyph failure. Preserve exact fixture/hash "
    "and terminal percase0, no doubleparse, heap/archiveguard increase or shared-device interference. "
    "Original two model sessions need serial bounded rendered confirmations; current textual review "
    "certifies neither native/phone nor widercustom/random/fallback pools. All combined-current-main/"
    "nonrewritingmerge/changedteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutableZIPmanifestentryhash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/"
    "media/path/verifiedownerissue gates remain. Parent19008 retains runner.lock throughout child lifetime; "
    "NO child acquire/delete/unlock/readprobe. Approved control/committed evidence/frozen inputs only, "
    "no optional historical-session helper access. Preserve/report/yield actual new denial/signing hang/"
    "uncertain ownership. Published123/1228 and1105 acceptance remainder unchanged; physicalphone/"
    "generalrelease/whole-set outstanding. No098, unreviewedpush or secondrunner."
)


def save(path, value):
    temp = path.with_suffix(path.suffix + ".711.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def processes():
    records, previous = {}, None
    for label, model in r.MODELS.items():
        prefix = f"batch-097-initial-{label}"
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
        records[label] = {
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
    assert r.PACKET.read_bytes() == (V / r.PACKET.name).read_bytes()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (710, "097")
    ledger = load(S / "batch-097-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    receipts = {}
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "097"],
        "tests": [sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
                  "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources"],
        "vocabulary": [sys.executable, "-B", str(R / "tools" / "grammar_vocabulary.py"), "check"],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
    }
    for name, command in commands.items():
        path = V / f"batch-097-textual-review-{name}-711.txt.gz"
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

    mechanical = audit(R, "097")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "a066afceaf1f447a"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8447
    for source in load(V / "batch-097-review-dictionary-provenance.json")["sources"]:
        assert sha(Path(source["path"])) == source["sha256"]
    pairs = ledger["allMappedReciprocalPairs"]
    assert len(pairs) == 3
    for char, word in pairs:
        assert "(../" + word + ")" in (R / "kanji" / (char + ".md")).read_text(encoding="utf-8")
        assert "(../kanji/" + char + ".md)" in (R / word).read_text(encoding="utf-8")
    assert (R / "kanji" / "口.md").is_file()
    reviewed = {name: sha(R / name) for name in [
        "kanji/剣.md", "words/剣.md", "words/真剣.md", "kanji/真.md",
        "strokes/剣.json", "manifest.json",
    ]}
    limits = [
        "TEXTUAL closure only, NOT full batch review closure, runtime acceptance or publication; reviewClosed/published arrays remain empty.",
        "Both original reports/executions preserved. Each process returned its exact entire assigned packet in one call, no truncation/missinglines/overlap/unfinishedtool, and exited before the next process. Returned bytes do not certify comprehension.",
        "Both initial reviewers received the same137-family packet and exact two reused diffs, independently of other findings or author adjudication. Public text is coordinator-supplied committed extraction, not independent upstream retrieval; gaiji may be omitted.",
        "Runtime and all8447 payload hashes unchanged; prior complete source/baseline/stroke/font audit is execution710, not relabelled as fresh full linguistic inspection.",
        "Default-four three kanjichoices accepted textually. Actual N1/All and widercustom/random/legacy fallback pools remain runtime gates; exposure is not certified safe.",
        "Fresh Android/RareHan/native/fourfonts/drawing/reading/N1-All/Back/offline/ContentSyncONCE and dependent original-session rendered review remain pending.",
        "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Compatibleclientf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
        "Published123/1228 and1105 acceptance remainder unchanged; six separate earlierN2source members保案派第策結 and separate妖exception retained. No098 or project completion.",
        "All original combined-main/signing/ownerpush/terminalCI/EVERYimmutableZIPhash/originalbudgets/ownerissue gates remain. Parent lock untouched, no optional historical helper access or new permission denial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 711, "batch": "097", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False, "reviewedRuntimeHashes": reviewed,
        "initialModels": list(r.MODELS.values()), "processes": records,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 240886, "initialPacketLines": 5345,
        "distinctCompleteFamilies": 137, "familyOccurrences": 139, "rawCharacterRecords": 11,
        "completeArticleBodies": 22, "newArticleBodies": 2, "changedReusedPassages": 2,
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
            for name in ["kanji/剣.md:1-48", "words/剣.md:1-38", "words/真剣.md:27", "kanji/真.md:37"]
        },
        "findings": [],
        "optionalDispositions": [
            {"reportedBy": "Claude", "claim": "Add sourcedつるぎ/けん register guidance.",
             "status": "optional", "decision": "No edit. Both documented readings are preserved, and no frequency ranking or exclusive usage claim is made. Neither priority flags nor clusters of dictionary examples establish a new categorical register rule."},
            {"reportedBy": "Claude", "claim": "Gloss zoological senses as stinger/ovipositor.",
             "status": "optional", "decision": "No edit. The article explicitly excludesけん-only senses from thisつるぎ lesson; those senses are not necessary new learning targets."},
            {"reportedBy": "Claude", "claim": "Add clock-hand compounds and old劍/劒 forms.",
             "status": "optional", "decision": "No edit. Complete source families retain them as recognition evidence. Selected current readings, practical sword examples and qualified meaning are sufficiently covered; no exhaustive historical-form or compound course is in scope."},
        ],
        "hypothesisDispositions": [
            {"reportedBy": "Claude", "claim": "Standaloneけん may be more common thanつるぎ.",
             "status": "unresolved", "severity": "nonconsequential unused frequency hypothesis",
             "decision": "No unsupported frequency claim adopted. Priority flags and dictionary-example distribution alone do not prove frequency/register. Both actual dictionary headings verify readings; museum example explicitly suppliesつるぎ. GPT independently rejects a categorical rarity/register label from this packet. Not a current contradicted teaching claim."},
            {"reportedBy": "Claude; equivalent GPT runtime limit", "claim": "Wider/legacy fallback can expose刀 or刃 overlap.",
             "status": "unresolved", "severity": "runtime gate, not a current default-four teaching defect",
             "decision": "Three authored semantically wrong options cover default four choices. Both reviewers identify actual N1/All and larger/custom/random/legacy fallback as pending, not certified. Runtime acceptance and publication remain blocked on their original checks; no general safety claim."},
            {"reportedBy": "Claude", "claim": "口 link existence not independently checked.",
             "status": "resolved", "decision": "Coordinator confirms actual kanji/口.md exists; fresh validator and exact batch audit pass. Original review independence limit preserved."},
        ],
        "modelContributionComparison": {
            "shared": "Both checked reading-specific sword senses, nonexclusive blade taxonomy, whole examples/translations,真剣 literal/earnest distinction, exact source readings/allocation, curation, radical/mnemonic/strokes, all direct guards and default wrong labels, all six links and two bounded reused changes. Both disclose runtime/fallback and upstream/native limits; differently labelled equivalent observations are shared, not unique discoveries.",
            "claudeUniqueVerifiedUseful": [], "gptUniqueVerifiedUseful": [],
            "claudeUniqueNonblocking": "Optional alternate-reading guidance, zoology gloss and historical/clock-hand expansion; unused frequency hypothesis and口existence limit.",
            "unsupportedMandatorySuggestions": "No mandatory textual fix, new frequency rule, exhaustive historical expansion or extra synonym clique established.",
            "limits": "Matched sample/source access; not a general model benchmark, equal-depth comprehension certification or native-speaker review.",
        },
        "actionableRemainingTextualFindingGroups": 0, "consequentialUnresolvedTeachingClaims": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "dependentTextualConfirmation": "Not needed: no teaching edit or established textual defect. Original sessions retained for required later rendered confirmation.",
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "previousCompleteSourceBaselineFontStrokeAudit": "docs/n1-sources/batch-097-draft-audit.json",
        "previousCompleteSourceBaselineFontStrokeAuditSha256": sha(S / "batch-097-draft-audit.json"),
        "allMappedReciprocalPairs": 3, "directedLinksVerified": 6, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairsAppliedInDraft": 4,
        "actualHanCount": 20, "nativeFontPending": ["刂"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    save(V / "batch-097-reconciliation.json", rec)
    ledger["initialDraftLimits"] = copy.deepcopy(ledger["limits"])
    ledger.update(status=STAGE, initialReviewSnapshot=SNAPSHOT, reviewedTeachingSnapshot=SNAPSHOT,
                  textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False, nextAction=NEXT)
    ledger["limits"][0] = limits[0]
    ledger["independentReviewersLaunched"] = 2
    ledger["quizAudit"]["剣"]["limits"] = "Default-four textually accepted; actual production N1/All and wider-pool review pending."
    ledger["textualReview"] = {
        "snapshot": SNAPSHOT, "models": rec["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-097-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-097-reconciliation.json"),
        "teachingChanged": False, "textualReviewClosed": True,
        "actionableRemainingTextualFindings": 0, "runtimeAccepted": False,
    }
    ledger["pendingGates"] = [
        "Fresh non-skipped THREE RealContentTest/ONE RareHanTest against actual sibling.",
        "Full productionContentSyncONCE/native N1-All choices/four guards/けん+つるぎ/tenstroke drawing/articles/reusedlinks/Back/offline/all20Han/fourfonts; dependent original-session rendered confirmations.",
        "Combined-current-main integration, changed teaching re-review if needed, all checks/normal signing/owner fastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/originalbudgets/verifiedownerissue.",
    ]
    for row in ledger["supportMappings"]:
        row["status"] = "textual-review-closed-awaiting-android-native"
    save(S / "batch-097-progress.json", ledger)
    membership = load(S / "batch-097-membership.json")
    membership["initialDraftLimits"] = copy.deepcopy(membership["limits"])
    membership.update(status=STAGE, initialReviewSnapshot=SNAPSHOT,
                      textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False)
    membership["limits"] = limits[0]
    save(S / "batch-097-membership.json", membership)
    recipe = S / Path(__file__).name
    shutil.copyfile(Path(__file__), recipe)
    shutil.copyfile(C / "preflight-711.ps1", S / "batch-097-textual-preflight-711.ps1.txt")
    save(S / "execution-711.json", {
        "schemaVersion": 1, "execution": 711, "batch": "097", "status": STAGE,
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "startingState": p["execution711StartingState"],
        "reconciliation": "docs/n1-reviews/batch-097-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-097-reconciliation.json"),
        "recipeHashes": {path.relative_to(R).as_posix(): sha(path) for path in [
            recipe, V / "review-batch-097.py", V / "batch-097-serial-review-base-recipe.py",
            S / "batch-097-textual-preflight-711.ps1.txt",
        ]},
        "checks": receipts, "runtimeBytesChanged": False,
        "publishedAdditions": 123, "remainingAdditions": 1105,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
    })
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    print("SAME097 two-family TEXTUAL closure saved; Android/native/publication remain.", flush=True)


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
    rec = load(V / "batch-097-reconciliation.json")
    evidence = load(S / "execution-711.json")
    assert sha(V / "batch-097-reconciliation.json") == evidence["reconciliationSha256"]
    for name, expected in {**rec["reviewedRuntimeHashes"], **evidence["recipeHashes"]}.items():
        assert sha(R / name) == expected
    for info in evidence["checks"].values():
        assert sha(R / info["path"]) == info["sha256"]
    return head, rec


def seal():
    head, rec = verify_signed()
    original = load(L / "progress-before-711.json")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (710, "097")
    cp = {
        "schemaVersion": 1, "execution": 711, "checkpoint": 711, "batch": "097",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "evidence": "docs/n1-sources/execution-711.json",
        "sourcePacket": "docs/n1-sources/batch-097-progress.json",
        "reconciliation": "docs/n1-reviews/batch-097-reconciliation.json",
        "textualReviewClosed": True, "runtimeDrafted": ["剣"], "reviewClosed": [], "published": [],
        "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionCoverageSupplements": 0, "serialReviewerExitAndScopeReverified": True,
        "bothProcessesOneCallExactFullPacketReturned": True,
        "actionableRemainingTextualFindings": 0, "teachingChanged": False,
        "completeDictionaryFamilies": 137, "familyOccurrences": 139,
        "completeRawCharacterRecords": 11, "metadataReadings": 2,
        "newSupportArticles": 1, "changedReusedArticles": 2,
        "allMappedReciprocalPairs": 3, "directedLinksVerified": 6, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairsAppliedInDraft": 4, "generatedStrokePaths": 10,
        "actualHanCount": 20, "pendingNativeFallbackLabels": ["刂"],
        "contentVersion": "a066afceaf1f447a", "allRuntimePayloadHashesVerified": 8447,
        "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 123, "remainingAdditions": 1105,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT,
    }
    p.update(checkpoint=711, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution711CoordinatorCheckpoint"] = cp
    p["batch097TextualReviewCheckpoint"] = copy.deepcopy(cp)
    p["execution711StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-097-textual-711-seal.json", cp)
    save(L / "checkpoint-711.json", cp)
    print("Verified signed clean checkpoint711:", head)


def issue_body():
    head, rec = verify_signed()
    body = (
        f"Batch097 (剣) — two-family TEXTUAL review closed at normally signed LOCAL checkpoint711 "
        f"`{head}` (signature G). Not Android/native acceptance, publication or project completion.\n\n"
        f"Same frozen draft `{SNAPSHOT}` reviewed serially by actual Claude Opus5.5 "
        "(`claude-opus-5.5`, session3a0b6dd8-6212-4ceb-a430-3127aac6969e), then GPT6.1Sol "
        "(`gpt-6.1-sol`, session9f31594c-f091-4d47-9276-12249f0c848d). Identical common "
        "packet240886bytes/5345lines covered137 distinct complete dictionary families/139occurrences, "
        "11raw records and22complete article bodies, including complete new剣/剣つるぎ and exact "
        "reused真剣/真 changes. Each isolated view-only process returned its exact entire packet "
        "in one serial call without truncation/missinglines/tooloverlap/unfinishedtool, and exited "
        "before the next. Full original reports/models/sessions/executions/coverage retained in "
        "docs/n1-reviews/batch-097-*. Returned bytes are not comprehension certification or "
        "independent upstream retrieval.\n\n"
        "Both complete new articles and both bounded reused passages: correctness, scoped "
        "coverage and phone-TEXT comprehensibility CLEAN in scope; no actionable textual defect "
        "or consequential unresolved teaching claim established. Teaching unchanged, so no "
        "dependent textual fix confirmation needed; original sessions retained for later "
        "rendered confirmation. Optional register/zoology/clock-hand/old-form expansions not "
        "adopted. Unusedけん-versusつるぎ frequency hypothesis remains unproved; priority flags "
        "do not establish frequency. Wider/custom/random/legacy fallback overlap is a pending "
        "runtime gate, NOT certified safe. Actual口 link target confirmed by coordinator.\n\n"
        "Fullケン/[つるぎ] retained in source order; both selected with their own linked "
        "source-allocated examples. Nonexclusive double-edge association, valid standaloneけん "
        "andけん-only senses kept distinct. Necessaryつるぎ article has no inferred word level; "
        "reused真剣しんけん retains N3 metadata and originalまじめ guard;真 remains N4. "
        "FOUR directwordguards, THREE allmappedpairs/SIX directions/ONE activatedbaselinepair. "
        "Ten pinned generated strokes/all20Han unchanged;刂cmap absence is NOT glyph failure.\n\n"
        "Fresh validator0, regenerated unchanged manifesta066afceaf1f447a,43focusedtests, exact "
        "batch audit, vocabularyconsistency and original archivebudget checks passed; all8447 "
        "runtimepayloadhashes verified. Prior complete source/baseline/stroke/font audit retained "
        "as execution710, not relabelled as fresh linguistic inspection. Runtime bytes unchanged; "
        "only evidence/ledger local commit, no push.\n\n"
        "Next SAME097 fresh non-skipped THREE RealContentTest/ONE RareHanTest, production "
        "ContentSync ONCE/fullarchive/N1-All actual choices/four guards/けん+つるぎ/tenstroke "
        "drawing/articles/reusedlinks/SystemBack/offline/all20Han/fourfonts, then original-session "
        "rendered confirmations. Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, "
        "NOT latest appmain. All combined-current-main/signing/ownerfastforward/terminalgreenCI/"
        "EVERYimmutableZIP runtime manifesthash/originalbudgets/verifiedownerissue gates remain.\n\n"
        "Published123/1228;1105 acceptance remainder unchanged. Physical-phone/general-release/"
        "whole-set outstanding. Compatible updated client required. No098, unreviewedpush, "
        "parent-lock manipulation, optional historical-session helper access, actual new "
        "permission denial or secondrunner. Full historicalprogress preserved; statuscontinue."
    )
    (C / "batch-097-textual-711-issue-body.txt").write_text(body, encoding="utf-8")


def receipt():
    verify_signed()
    posted = load(L / "issue-711-reread.json")
    body = (C / "batch-097-textual-711-issue-body.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    p = load(C / "progress.json")
    original = load(L / "progress-before-711.json")
    assert (p["checkpoint"], p["status"], p["stage"]) == (711, "continue", STAGE)
    record = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "verified": True, "comparison": "Exact UTF-8 bytes.",
    }
    p["batch097TextualReviewIssueReceipt"] = record
    for key in ["execution711CoordinatorCheckpoint", "batch097TextualReviewCheckpoint"]:
        p[key]["issueUpdate"] = record["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-097-textual-711-issue-receipt.json", record)
    save(L / "checkpoint-711.json", p["execution711CoordinatorCheckpoint"])
    save(C / "batch-097-textual-711-final-verification.json", p["execution711CoordinatorCheckpoint"])
    assert load(C / "progress.json") == p
    print("Verified persisted checkpoint711, historical preservation and owner issue:", record["url"])


if __name__ == "__main__":
    {"prepare": prepare, "seal": seal, "issue-body": issue_body, "receipt": receipt}[sys.argv[1]]()
