"""Persist reviewed text separately from pending batch/runtime acceptance."""
import ast
import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "c78a4783-a062-42bb-9fd0-e132d134da9d"
SNAPSHOT = "54be1c9ad3f052b23b0bde1c74e7f6c580cd4477"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
MAIN = "1621cf6cbd2283d377936c77f9c81851baffdf20"
NEXT = (
    "SAME102 fresh qualifiedAndroidbf30cdead HOST acceptance checkpoint: non-skipped RealContentTest/"
    "RareHanTest plus actual production meaning-builder defaultN1/All/custom-pool choices and direct "
    "symmetric NONTRANSITIVE guards. Two blind different-family initial TEXTUAL reviews COMPLETE on "
    "signed54be1c9a; reconciliation has no actionable changed-text defect and no teaching correction "
    "was needed. No repeat initials or full batch closure/publication claim. Preserve Claude "
    "112f8849-4cce-4f19-8ed8-a6b25e6f9d2e and GPTcd6cf58b-fbd1-4835-af8e-04079396d864 "
    "complete original reports and original-session Claude dependent scope clarification. Exact full "
    "272741byte/6196line packet returned to both in ONE serial view call; 69member+43comparison="
    "112completefamilies/16rawcharacterrecords/32articlebodies/THREEpublicdictionarytexts. Original "
    "Claude110family/23comparisonarticle miscounts retained; scope clarification attributes these "
    "to reporting approximations and confirms original read, with unrelated families only briefly "
    "checked for relevance. Byte access/self-report is not exhaustive sense-by-sense comprehension, "
    "equal depth or independent upstream retrieval. Both new劣/優劣 and exact reused劣る/優 navigation "
    "passages CLEAN in correctness/scopedcoverage/textcomprehensibility; runtime remains UNVERIFIED. "
    "No optional劣化/moralcompound/fixedellipsis expansion or speculative長所/特長 guard required. "
    "七directkanjiguards弱悪下低貧負少 and four directwordguards質長短利害損得 accepted textually; "
    "少 is conservative quantitative/source overlap, NOT justified by mnemonic/component alone. "
    "Only功 of努功省 isN1, so test actual defaultN1 fallback; actual choice labels/ordinary senses "
    "and reverse/pairwise exclusion enforcement mandatory. Preserve [レツ]/[おと.る] fullsourceorder/"
    "bothselections/ownrowlinks to優劣ゆうれつ and existing劣るおとるN3; onlyれつ/おとる. "
    "優劣 two-sidedrelative superiority/inferiority; no inferredwordlevel. All existingmetadata/"
    "levels/readings/exclusions unchanged; threeallmappedpairs/sixdirections/oneactivatedbaselinepair "
    "include優-to-優劣. Six pinned paths/canonical力19below少/labelledmodernshapemnemonic/"
    "structure-unclassified/noadoptedetymology;31actualHan/allcmaps/zeroRareHan NOT rendering "
    "acceptance. Any newly established defect requires exact frozen family/labels, minimal change, "
    "recomputed audits/manifest, normal signed changed-tree freeze and BOTH original-session "
    "changed-passage confirmations. Then productionContentSyncONCE/native N1/All/meaning/"
    "curatedreading/drawing/article/Back/offline/fourfont/allHan/rendered review gates; native "
    "fixtures bind actual currentcontent/signedqualifiedapp, unchanged2gguest/192mheap/oneworker, "
    "ownedport/device checks, terminalcase0 and cleanup. Keep combinedcurrentmain/allrequiredPython/"
    "vocabulary/normal signing/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/"
    "unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia/verifiedownerissue "
    "gates. No unreviewedpush/103/authoragents/concurrentheavywork/secondrunner/signingretry/"
    "guardincrease. Verify whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/"
    "exactsession. Parent5920 ownsrunner.lock: no childacquire/delete/unlock/readprobe. Approvedcontrol/"
    "committedsource/frozeninputs only, not optional historicalsessionrecipes; preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. QualifiedAndroidapprovedpairguard+schemaonly, "
    "NOT unrelated latestmain. Published128/1228,1100acceptanceremainderunchanged; six earlierN2"
    "placements保案派第策結separate. CompatibleAndroid#125+#132 required; oldclientsignorecuration/"
    "guards. Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. Historical "
    "limitations preserved."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".775.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == data
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def absent(pid):
    result = subprocess.run(["pwsh", "-NoProfile", "-Command",
                             f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                            capture_output=True)
    return result.returncode == 0


def identity(signed=False):
    assert git("log", "-1", "--format=%G?") == "G"
    if signed:
        assert git("rev-parse", "HEAD^") == SNAPSHOT
        assert not git("status", "--porcelain")
        changes = git("-c", "core.quotepath=false", "diff", "--name-only", SNAPSHOT, "HEAD").splitlines()
    else:
        assert git("rev-parse", "HEAD") == SNAPSHOT
        changes = [line[3:] for line in git("-c", "core.quotepath=false", "status",
                                         "--porcelain", "--untracked-files=all").splitlines()]
    assert all(n.startswith("docs/n1-reviews/batch-102-")
               or n == "docs/n1-sources/batch-102-progress.json"
               or n == "docs/n1-sources/execution-775.json" for n in changes), changes
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    assert not git("status", "--porcelain", "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    assert git("rev-parse", "origin/main") == MAIN
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    assert not absent(5920)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (774, "102", "continue")


def archive(path):
    target = path.with_name(path.name + ".gz")
    assert not target.exists()
    target.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
    assert gzip.decompress(target.read_bytes()) == path.read_bytes()
    receipt = {"rawName": path.name, "rawSha256": sha(path), "archive": target.name,
               "archiveSha256": sha(target), "losslessGzip": True}
    path.unlink()
    return receipt


def record():
    identity()
    processes = {}
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        prefix = f"batch-102-initial-{label}"
        execution = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert execution["snapshot"] == coverage["snapshot"] == SNAPSHOT
        assert execution["exitCode"] == 0 and execution["actualModels"] == [model]
        assert execution["usageCurrentModel"] == model and coverage["allAssignedRangesReturned"]
        assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
        assert execution["availableTools"] == ["view"] and len(execution["toolCalls"]) == 1
        call = execution["toolCalls"][0]
        assert call["success"] and call["exactRequestedTextContainedInResult"]
        assert not call["truncationMarker"] and execution["multiToolResponseCount"] == 0
        assert absent(execution["launcherPid"])
        assert sha(V / (prefix + ".md")) == execution["reportSha256"]
        assert sha(V / (prefix + ".jsonl")) == execution["rawExecutionSha256"]
        archived = archive(V / (prefix + ".jsonl"))
        processes[label] = {k: execution[k] for k in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
            "snapshot", "reportSha256", "rawExecutionSha256"]}
        processes[label].update(
            report=prefix + ".md", execution=prefix + "-execution.json",
            coverage=prefix + "-coverage.json", allAssignedRangesReturned=True,
            toolCalls=1, observedToolOverlaps=0, exactFullPacketReturnedInFirstCall=True,
            losslessExecutionArchive=archived)
    assert processes["claude"]["completedAt"] < processes["gpt"]["startedAt"]
    scope = load(V / "batch-102-scope-claude-execution.json")
    assert scope["exitCode"] == 0 and scope["actualModels"] == ["claude-opus-5.5"]
    assert scope["originalSessionId"] == processes["claude"]["sessionId"]
    assert scope["usageCurrentModel"] == "claude-opus-5.5" and not scope["toolCalls"]
    assert not scope["observedToolOverlaps"] and not scope["unfinishedTools"]
    assert absent(scope["launcherPid"]) and processes["gpt"]["completedAt"] < scope["startedAt"]
    assert sha(V / "batch-102-scope-claude.md") == scope["reportSha256"]
    assert sha(V / "batch-102-scope-claude.jsonl") == scope["rawExecutionSha256"]
    scope_archive = archive(V / "batch-102-scope-claude.jsonl")
    required = load(V / "batch-102-required-review-ranges.json")[0]
    assert sha(C / "batch-102-initial-packet.txt") == required["sha256"]
    assert required["end"] == 6196
    provenance = load(V / "batch-102-review-dictionary-provenance.json")
    assert provenance["distinctCompleteFamilies"] == 112 and provenance["rawCharacterRecords"] == 16
    reconciliation = {
        "schemaVersion": 1, "execution": 775, "batch": "102",
        "status": "textual-review-closed-runtime-acceptance-pending",
        "originalTeachingSnapshot": SNAPSHOT, "teachingChangedAfterInitialReviews": False,
        "initialModels": ["claude-opus-5.5", "gpt-6.1-sol"], "processes": processes,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 272741, "initialPacketLines": 6196,
        "completeFamiliesSupplied": 112, "rawCharacterRecordsSupplied": 16,
        "completeArticleBodies": 32, "newArticleBodies": 2, "changedReusedPassages": 2,
        "scopeClarification": {
            "report": "batch-102-scope-claude.md", "execution": "batch-102-scope-claude-execution.json",
            "losslessExecutionArchive": scope_archive,
            "originalReportUnchanged": True, "dependentOriginalSession": True,
            "disposition": "resolved reporting discrepancy, not a teaching defect",
            "claim": "Initial Claude report incorrectly counted110 families and23 comparison articles.",
            "evidence": "Exact full original packet returned; XML parser enumerates69+43 unique IDs and provenance32 article bodies. Original-session clarification says approximate counts were wrong and all records were read originally; unrelated entries only briefly checked for relevance.",
            "limits": "No fresh reads in clarification. Actual access plus self-report is not exhaustive sense-by-sense semantic review or proof of equal comprehension.",
        },
        "verdicts": {
            unit: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
            for unit in ["kanji/劣.md:1-50", "words/優劣.md:1-36",
                         "words/劣る.md:26-27", "kanji/優.md:42"]
        },
        "findings": [], "consequentialUnresolvedChangedTeachingClaims": [],
        "optional": [
            {"id": "O1", "status": "optional", "reviewer": "claude",
             "claim": "Add劣化れっか as another example.",
             "disposition": "Declined scope expansion. Existing two selected readings already have verified useful linked examples; no missing attachment or useful-reading explanation established."},
            {"id": "O2", "status": "optional", "reviewer": "claude",
             "claim": "Add卑劣/下劣 to illustrate judgments of character.",
             "disposition": "No edit. Current says not EVERY comparison is moral, not that moral character is excluded. Source品性 evidence is preserved; no consequential false compartment asserted."},
            {"id": "O3", "status": "optional", "reviewer": "claude",
             "claim": "Mention fixed優劣つけがたい withoutを.",
             "disposition": "No edit. Natural particle-bearing construction supported by complete2860720 plus2108410; ordinary grammar is not invalidated by a separate lexical spelling list. Both products explicitly favorable. No required fixed-expression expansion."},
            {"id": "H1", "status": "withdrawn", "reviewer": "claude optional hypothesis; GPT equivalent observation",
             "claim": "長所/特長 labels merit might overlap relative merits.",
             "disposition": "No new pair established. Complete1430030/1455200 give one-sided strengths;1539620 is relative superiority/inferiority. Both reviews found existing choice defensibly distinct. Shared English substring is not proof; do not make a transitive clique.",
             "evidence": "Complete112-family packet and actual displayed article labels; all four direct new word guards remain."},
        ],
        "guardQualification": "Seven kanji guards are direct conservative pairs, not universal synonyms. 少 rests on actual字通訓義2 and Daijisen劣るquantity comparison, not visible component/mnemonic alone. Claude initially foregrounded mnemonic; GPT and coordinator explicitly retain quantitative/source basis. No metadata or teaching change needed.",
        "boundedEvidenceLimits": [
            "No independent reviewer upstream/Git/signature verification; coordinator-supplied archived dictionary blocks, formatting stripped/image-gaiji unavailable.",
            "Both received full packet; Claude admits unequal depth, with unrelated entries briefly checked for relevance, not exhaustive sense-by-sense certification. Original miscounts and clarification retained.",
            "Actual N1/All/custom fallback, reverse and pairwise exclusions, curated reading/native/drawing/four-font/rendered/physical-phone acceptance UNVERIFIED; only功 of three curated distractors is N1.",
            "No exhaustive whole-corpus/future-choice semantic guarantee or measured frequency/learning-effectiveness/native-speaker approval.",
        ],
        "matchedSampleContributions": {
            "shared": "All four assigned units CLEAN in three textual facets; exact readings/allocation, two-sided優劣, translations, seven direct kanji/four word guards, three wrong labels, six reciprocal links and preserved navigation-only legacy metadata accepted.",
            "claudeUnique": "Optional劣化/moral-compound/fixed-ellipsis expansions, no actionable defect. Reporting-count discrepancy explicitly resolved in original session, with unequal semantic attention disclosed.",
            "gptUnique": "Explicit2860720 support for particle-bearing優劣をつける and search-alias boundary; detailed quantitative少 guard basis. These support existing correct teaching rather than inventing unique defect credit.",
            "limits": "Shared same snapshot/scope/evidence; equivalent optional/hypothesis/limit observations compared. Not a general model benchmark or equal-read-depth claim.",
        },
        "coordinatorEvidence": "Fresh complete target/support/reused bodies, three actual public dictionary extracted blocks, four applicable complete member families1539620/1558400/2108410/2860720 and all43 complete comparison families inspected in16/14/13 bounded returned ranges. Freshly read three distractor and four word-guard article bodies. No fresh full69-member-family semantic inspection or new upstream retrieval claimed; original772/773/774 evidence preserved.",
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "fullBatchAcceptanceComplete": False, "reviewClosed": [], "runtimeChangedThisExecution": False,
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
    }
    save(V / "batch-102-reconciliation.json", reconciliation)
    ledger_path = S / "batch-102-progress.json"
    ledger = load(ledger_path)
    ledger["status"] = reconciliation["status"]
    ledger["limits"][0] = "Two blind serial textual initial reviews reconciled without teaching changes; full batch closure awaits fresh qualified Android/production choices/native/rendered/integration/publication gates. No runtime publication."
    ledger["textualReview"] = {
        "execution": 775, "snapshot": SNAPSHOT, "models": reconciliation["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-102-reconciliation.json",
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "fullBatchAcceptanceComplete": False, "runtimeChangedThisExecution": False, "reviewClosed": [],
        "scopeLimits": reconciliation["boundedEvidenceLimits"],
    }
    ledger["nextAction"] = NEXT
    save(ledger_path, ledger)
    checks = {}
    for label in ["tests", "validate", "budget", "vocabulary", "audit"]:
        path = L / f"{label}-775.txt"
        text = path.read_text(encoding="utf-8-sig")
        if label == "tests":
            assert "Ran 43 tests" in text and text.rstrip().endswith("OK")
        elif label == "validate":
            assert text.strip() == "0 error(s)"
        elif label == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        elif label == "vocabulary":
            assert "2122/2431 reviewed prompts; stage=pilot" in text
        elif label == "audit":
            audit = json.loads(text)
            assert audit["exactBaseRuntimePreservedOutsideRecordedChanges"] and audit["manifestFresh"]
            assert audit["dictionaryFamilies"] == 112 and audit["readingDispositions"] == 2
        dest = V / f"batch-102-textual-review-{label}-775.txt.gz"
        dest.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        assert gzip.decompress(dest.read_bytes()) == path.read_bytes()
        checks[label] = {"archive": dest.name, "rawSha256": sha(path), "archiveSha256": sha(dest)}
    manifest = load(R / "manifest.json")
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    assert build_manifest(R) == manifest
    payloads = {name: value for entries in manifest.values() if isinstance(entries, dict)
                for name, value in entries.items()}
    assert len(payloads) == 8458 and manifest["contentVersion"] == "f376333b242ebb23"
    assert (R / "manifest.json").read_bytes() == subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", f"{SNAPSHOT}:manifest.json"])
    assert (R / "kanji" / "目.md").is_file() and (R / "kanji" / "工.md").is_file()
    save(V / "batch-102-runtime-preservation-775.json", {
        "snapshot": SNAPSHOT, "contentVersion": manifest["contentVersion"],
        "runtimeHashesVerified": len(payloads), "runtimeDiffSinceFrozenDraft": [],
        "manifestBytesUnchanged": True, "manifestFreshFromProductionGenerator": True,
        "reviewerUnverifiedLinkTargetsConfirmedByCoordinator": ["kanji/目.md", "kanji/工.md"],
        "limits": "No runtime change, app/native/rendered evidence or exact immutable GitHub ZIP acceptance inferred.",
    })
    archives = [archive(V / name) for name in [
        "batch-102-initial-packet.txt", "batch-102-cli-config-help-execution-775.txt"]]
    save(V / "batch-102-evidence-packaging-775.json", {
        "snapshot": SNAPSHOT, "archives": archives, "runtimeChanged": False,
        "reason": "Lossless archives preserve original XML/catalog whitespace without changing reviewer inputs or relaxing diff checks.",
        "diagnostics": "Initial complete request output hit console encoding failure after load/parse. Initial prepare equality assertion compared scoped request to full live history and stopped before any write; corrected to exact current checkpoint comparison and preserved complete live history. No permission denial, source substitution, reviewer input change or signing attempt resulted.",
    })
    for name in ["preflight-775.ps1", "checks-batch-102-review-775.ps1", "checkpoint-review-775.py",
                 "post-batch-102-review-775.ps1", "confirm-batch-102-scope-775.py"]:
        shutil.copyfile(C / name, V / ("batch-102-" + name + (".txt" if name.endswith(".ps1") else "")))
    shutil.copyfile(L / "preflight-775.json", V / "batch-102-runner-role-775.json")
    save(S / "execution-775.json", {
        "schemaVersion": 1, "execution": 775, "batch": "102",
        "stage": reconciliation["status"], "originalTeachingSnapshot": SNAPSHOT,
        "androidSignedHead": APP, "freshOriginMain": MAIN,
        "startingState": load(C / "progress.json")["execution775StartingState"],
        "initialReviewers": processes, "scopeClarification": reconciliation["scopeClarification"],
        "reconciliation": "docs/n1-reviews/batch-102-reconciliation.json",
        "checks": checks, "pythonTestsPassed": 43, "validatorErrors": 0, "localBudget": budget,
        "runtimeHashesVerified": 8458, "runtimeChangedThisExecution": False,
        "contentVersion": manifest["contentVersion"], "runtimePublished": False, "reviewClosed": [],
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "fullBatchAcceptanceComplete": False, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 128, "remainingAdditions": 1100, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": NEXT,
    })
    print("Both complete initial reports, scope clarification, reconciliation and unchanged-runtime evidence archived.")


def issue():
    identity(signed=True)
    head = git("rev-parse", "HEAD")
    target = C / "batch-102-review-775-issue.txt"
    assert not target.exists()
    target.write_text(
        "Batch102 / checkpoint775: **two independent textual reviews completed and reconciled; "
        "runtime acceptance remains pending**.\n\n"
        f"Normally signed local evidence `{head}` preserves unchanged teaching snapshot `{SNAPSHOT}`. "
        "Claude Opus5.5 and GPT-6.1 Sol ran serially with view-only tools against the same "
        "272741-byte/6196-line packet:69member+43comparison complete families,16raw character "
        "records,32complete article bodies,3archived public dictionary texts. Actual model IDs, full "
        "exact packet return, zero internal tool overlap and process exit before the second launch "
        "verified. Original complete reports and lossless JSONL/model/session/coverage evidence retained. "
        "Claude's original110-family/23-comparison-article miscounts remain unchanged; dependent "
        "original-session clarification corrects them to112/28, attributes them to reporting "
        "approximations, and discloses brief relevance inspection of unrelated families rather than "
        "exhaustive sense-by-sense review. Byte access and self-report do not prove equal comprehension "
        "or independent upstream retrieval.\n\n"
        "Both reviews found no actionable correctness, scoped-coverage or text-comprehensibility "
        "defect in new劣/優劣 or the two navigation-only changes (劣る,優). Both source readings/order/"
        "selected own-row links, two-sided優劣 and examples,3wronglabels,7directkanjiguards/"
        "4directwordguards and3mappedpairs/6linkdirections accepted textually. 少 is a conservative "
        "quantitative/source guard, not a mnemonic-only inference. Optional vocabulary/moral-compound/"
        "ellipsis expansions and speculative長所/特長 guard are not required fixes. Teaching unchanged. "
        "Reconciliation and limits: docs/n1-reviews/batch-102-reconciliation.json; "
        "docs/n1-sources/execution-775.json.\n\n"
        "Runtime bytes/manifest unchanged; all8458 hashes and contentVersionf376333b242ebb23 "
        "verified through the production manifest generator.43focused tests, validator0errors, "
        "batch/source/baseline/link/reading audits and unchanged local publishing budgets passed. "
        "Vocabulary consistency retains its2122/2431pilot scope. No fresh Android/native/rendered "
        "acceptance, push, batch103 or second runner. Parent5920/exact session/ancestry verified; "
        "runner.lock untouched; durable control/committed evidence only; no new denial.\n\n"
        "Next SAME102 fresh qualified Android host checks/non-skipped RealContentTest/RareHanTest "
        "and actual defaultN1/All/custom production meaning-builder/fallback/direct-symmetric-"
        "nontransitive guard acceptance (only功 of努功省 isN1), followed by current-content native/"
        "four-font/rendered and every original integration/publication gate. Compatible "
        "stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 mechanisms remain "
        "required. **128/1228 published;1100 acceptance remainder unchanged.** Physical-phone/"
        "general-release/whole-set acceptance outstanding; project incomplete.\n",
        encoding="utf-8", newline="\n")
    (L / "signed-head-775.txt").write_text(head + "\n", encoding="ascii")
    print("Signed clean local textual-review checkpoint verified; owner issue body prepared.")


def finish():
    identity(signed=True)
    head = git("rev-parse", "HEAD")
    issue_data = load(L / "issue-775-verified.json")
    assert issue_data["user"]["login"] == "stop-cran"
    assert issue_data["body"] == (C / "batch-102-review-775-issue.txt").read_text(encoding="utf-8")
    assert head in issue_data["body"]
    before, p = load(L / "progress-before-775.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    state = {
        "schemaVersion": 1, "execution": 775, "checkpoint": 775, "batch": "102",
        "savedCommit": head, "signature": "G", "originalTeachingSnapshot": SNAPSHOT,
        "freshOriginMain": MAIN, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-775.json",
        "reconciliation": "docs/n1-reviews/batch-102-reconciliation.json",
        "contentVersion": "f376333b242ebb23", "initialReviewsComplete": True,
        "textualAcceptanceComplete": True, "fullBatchAcceptanceComplete": False,
        "runtimeDrafted": ["劣"], "reviewClosed": [], "published": [],
        "runtimeChangedThisExecution": False, "runtimePublished": False,
        "independentReviewersLaunched": 2, "dependentOriginalSessionScopeClarifications": 1,
        "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "allAssignedRangesReturned": True, "freshAndroidOrNativeClaimed": False,
        "pythonTestsPassed": 43, "validatorErrors": 0, "runtimeHashesVerified": 8458,
        "unresolvedChangedTeachingFindings": [],
        "readDepthLimits": "Claude original counts corrected in dependent original-session clarification; unrelated entries briefly checked, not exhaustive sense-by-sense review. Original reports preserved. Exact byte access is not comprehension or independent upstream retrieval.",
        "publishedAdditions": 128, "remainingAdditions": 1100, "lastPublishedCommit": MAIN,
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before), "ownerIssueAuthorAndExactBodyVerified": True,
        "issueUpdate": issue_data["html_url"], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-102-textual-review-closed-runtime-acceptance-pending",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
    }
    p["execution775CoordinatorCheckpoint"] = state
    p["execution775StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    p.update(checkpoint=775, status="continue", stage=state["stage"], batch="102",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    assert persisted == p
    assert all(persisted[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-775-final-verification.json", state)
    print(json.dumps({k: state[k] for k in ["checkpoint", "savedCommit", "status", "stage", "issueUpdate",
                                         "originalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"record": record, "issue": issue, "finish": finish}[sys.argv[1]]()
