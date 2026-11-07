"""Persist the completed initial-review checkpoint without claiming batch acceptance."""
import ast
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "33f532e6-b106-4689-8fd5-4a56512a813f"
SNAPSHOT = "5a52b28e9f6f506171c5041bd52b0d9f8c261323"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
MAIN = "716c610153234e8d2240dcf528de3ef83b654b27"
NEXT = (
    "SAME100 bounded correction/source-supplement checkpoint before original-session confirmations. "
    "Two blind different-family initial textual reviews are COMPLETE on signed5a52b28e; "
    "do not rerun initial reviews or count this batch review-closed. Preserve complete original "
    "Claude4975f494 and GPTc9e3c7f4 sessions/reports/actualmodels/read/process evidence. "
    "Resolve F1 localized coverage using complete frozen1398640創立そうりつ founding and "
    "1398490創傷そうしょう formal/literary wound examples; no new word article or inferred level "
    "needed. Both families already preserved; do not manufacture a frequency claim. "
    "Reconcile source-confirmed missing direct創/設 guard: actual設 label establish; provide "
    "overlaps explicitly taught establishment sense. Inspect exact frozen設 family/raw metadata "
    "and actual初 label first time; initial to decide independently whether創/初 merits a direct "
    "guard; 初 is still a hypothesis, not an accepted defect. 傷-kanji guard hypothesis withdrawn "
    "because kanji/傷.md DOES NOT EXIST; words/傷.md is a different quiz namespace. No missing-card "
    "guard, new傷 card, transitive clique or unrelated legacy rewrite. "
    "Recompute all applicable source/metadata/reading/quiz/link/baseline/Han/font audits, validate "
    "and regenerate manifest after authorized changes; normal signed LOCAL changed-tree freeze "
    "before TWO SERIAL original-session changed-passage confirmations with exact diff and "
    "supplemental full evidence. Keep all six full readings/order and selectedソウ/つく.る, "
    "same-family作るN5/創作N2 identities/exclusions, source-onlyショウ/けず.しける lexical "
    "allocation UNVERIFIED without invented gloss/example/invalidity/obsolescence/source repair. "
    "Then fresh non-skipped qualifiedAndroidbf30cdead RealContent/RareHan, productionContentSyncONCE/"
    "native N1-All/meaning/curatedreading/drawing/article/Back/offline/four-font/all-Han/rendered "
    "acceptance, combinedcurrentmain checks, normal signing/ownerfastforward/terminalgreenCI/"
    "EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/"
    "perfilepathmedia/verifiedownerissue gates remain mandatory. No unreviewedpush/101/authoragent/"
    "concurrentheavywork/secondrunner/signingretry/guardincrease. Verify whollyclean signedheads/"
    "freshmain/liveparentancestry/decodedlauncher/exactsession. Parent5920 ownsrunner.lock: no "
    "childacquire/delete/unlock/readprobe. Approvedcontrol/committedsource/frozeninputs only, not "
    "optional historicalsessionrecipes; preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Published126/1228,1102acceptanceremainder unchanged; six earlierN2placements "
    "保案派第策結 remain separate, never duplicate/relevel. Physicalphone/generalrelease/whole-set "
    "outstanding; projectincomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    tmp = path.with_suffix(path.suffix + ".748.tmp")
    assert not tmp.exists()
    tmp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == data
    tmp.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def identity(signed=False):
    assert git("log", "-1", "--format=%G?") == "G"
    if signed:
        assert git("rev-parse", "HEAD^") == SNAPSHOT
        assert not git("status", "--porcelain")
        changes = git("-c", "core.quotepath=false", "diff", "--name-only", SNAPSHOT, "HEAD").splitlines()
        assert changes and all(n.startswith("docs/n1-reviews/batch-100-")
                               or n == "docs/n1-reviews/review-batch-100.py"
                               or n.startswith("docs/n1-sources/batch-100-")
                               or n == "docs/n1-sources/execution-748.json" for n in changes)
    else:
        assert git("rev-parse", "HEAD") == SNAPSHOT
    assert not git("status", "--porcelain", "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    android = C.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", root=android) == APP
    assert git("log", "-1", "--format=%G?", root=android) == "G"
    assert not git("status", "--porcelain", root=android)
    assert git("rev-parse", "origin/main") == MAIN
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (747, "100", "continue")


def record():
    identity()
    processes = {}
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        prefix = f"batch-100-initial-{label}"
        execution = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert execution["snapshot"] == coverage["snapshot"] == SNAPSHOT
        assert execution["exitCode"] == 0
        assert execution["actualModels"] == [model] and execution["usageCurrentModel"] == model
        assert coverage["allAssignedRangesReturned"]
        assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
        assert execution["availableTools"] == ["view"] and len(execution["toolCalls"]) == 1
        call = execution["toolCalls"][0]
        assert call["success"] and call["exactRequestedTextContainedInResult"]
        assert not call["truncationMarker"] and execution["multiToolResponseCount"] == 0
        result = subprocess.run(
            ["pwsh", "-NoProfile", "-Command",
             f"if (Get-Process -Id {execution['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
            capture_output=True)
        assert result.returncode == 0
        processes[label] = {k: execution[k] for k in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
            "snapshot", "reportSha256", "rawExecutionSha256"]}
        processes[label].update(
            report=prefix + ".md", execution=prefix + "-execution.json",
            coverage=prefix + "-coverage.json", allAssignedRangesReturned=True,
            toolCalls=1, observedToolOverlaps=0, exactFullPacketReturnedInFirstCall=True)
    assert processes["claude"]["completedAt"] < processes["gpt"]["startedAt"]
    provenance = load(V / "batch-100-review-dictionary-provenance.json")
    assert provenance["distinctCompleteFamilies"] == 153 and provenance["rawCharacterRecords"] == 13
    assert not (R / "kanji" / "傷.md").exists()
    supplemental = []
    for name in ["設", "初"]:
        path = R / "kanji" / (name + ".md")
        assert path.read_bytes() == subprocess.check_output(
            ["git", "--no-pager", "-C", str(R), "show", f"{SNAPSHOT}:kanji/{name}.md"])
        supplemental.append({"path": f"kanji/{name}.md", "sha256": sha(path),
                             "completeText": path.read_text(encoding="utf-8"),
                             "scope": "Coordinator post-review inspection, not initial reviewer coverage."})
    save(V / "batch-100-post-review-card-evidence-748.json", {
        "snapshot": SNAPSHOT, "cards": supplemental, "missingKanjiCard": "kanji/傷.md",
        "wordArticleNotKanjiQuizCard": "words/傷.md",
        "limits": "Actual card namespace and labels checked. No full frozen設/初 source supplement or independent follow-up review claimed.",
    })
    reconciliation = {
        "schemaVersion": 1, "execution": 748, "batch": "100",
        "status": "initial-textual-reviews-complete-reconciliation-required",
        "originalTeachingSnapshot": SNAPSHOT, "teachingChangedAfterInitialReviews": False,
        "initialModels": ["claude-opus-5.5", "gpt-6.1-sol"], "processes": processes,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 260254, "initialPacketLines": 6694,
        "completeFamiliesSupplied": 153, "rawCharacterRecordsSupplied": 13,
        "completeArticleBodies": 17, "newArticleBodies": 1, "changedReusedPassages": 3,
        "readDepthLimits": "Both executions returned the exact full packet in one serial view call. This proves byte access, not equal comprehension. Claude explicitly did not independently count137 member families; GPT reports inspecting all153. Public dictionaries are coordinator extractions, not reviewers' upstream retrieval.",
        "verdicts": {
            "kanji/創.md": {"correctness": "CLEAN", "scopedCoverage": "NEEDS FIX",
                           "textComprehensibility": "CLEAN",
                           "quizPoolAcceptance": "UNVERIFIED; post-review設 overlap requires correction/source confirmation"},
            "words/創作.md:30": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"},
            "words/作る.md:36": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"},
            "kanji/作.md:45": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"},
        },
        "findings": [
            {
                "id": "F1", "reviewer": "claude", "status": "unresolved", "severity": "Minor",
                "facet": "scoped coverage", "locations": ["kanji/創.md:25", "kanji/創.md:33", "kanji/創.md:46-49"],
                "claim": "No ordinary compound demonstrates the expressly taught wound sense or establishment sense; existing examples foreground creative work and a rare standalone/verb spelling.",
                "evidence": "Actual Daijisen創 sense1 lists創傷 and sense2創立; complete frozen JMdict1398490創傷そうしょう is formal/literary wound/injury,1398640創立そうりつ is establishment/founding.",
                "coordinatorDisposition": "Accept the localized teaching improvement, without a universal every-sense example quota. Two short qualified unlinked compound examples would suffice; no extra word identity, frequency claim or創造/idiom expansion required.",
                "reviewerDisagreement": "GPT reported scoped coverage CLEAN and no optional suggestions. This disagreement remains explicit; no majority/model-prestige adjudication.",
                "remedy": "Add minimal source-verified創立 and formal/literary創傷 recognition examples, recompute affected audits, then both original-session changed-passage confirmations.",
                "confidence": "High that examples are absent and cited families support them; moderate that the localized coverage omission warrants a fix rather than optional expansion.",
            },
            {
                "id": "H1-wound", "reviewer": "claude", "status": "withdrawn", "severity": None,
                "facet": "meaning-choice hypothesis", "claim": "Potential missing創/傷 kanji guard if an existing wound-titled傷 card exists.",
                "evidence": "Exact kanji/傷.md does not exist at frozen snapshot/current tree. Existing words/傷.md is a separate quiz namespace.",
                "remedy": "No missing-card reference, new傷 card or namespace-crossing guard. Do not claim original hypothesis was a verified defect.",
                "confidence": "High for exact current membership.",
            },
            {
                "id": "C1-establish", "reviewer": "coordinator post-review", "status": "unresolved",
                "severity": "Minor", "facet": "meaning-quiz ambiguity",
                "locations": ["kanji/創.md:14", "kanji/創.md:36", "kanji/設.md:3", "kanji/設.md:21"],
                "claim": "Existing設 label establish; provide can defensibly describe創's explicitly taught establishment/start-up meaning; no direct exclusion is declared.",
                "evidence": "Exact unchanged設 card and target創める establishment row; supplied frozen1307550 sense2 and Daijisen創 sense2. 設 was not in the blind initial packet.",
                "remedy": "Retain exact full frozen設 source/ordinary senses, add justified direct創/設 guard on new創 only, and submit exact metadata/diff/supplement to both original reviewers. No change to unrelated設 teaching.",
                "confidence": "High for displayed-label overlap; not live-pool acceptance.",
            },
            {
                "id": "H1-initial", "reviewer": "claude tentative cue; coordinator post-review",
                "status": "unresolved", "severity": None, "facet": "bounded supplementary source check",
                "claim": "初 first time; initial may overlap創's first-creation/start sense, but an additional direct pair has not been established.",
                "evidence": "Exact初 label inspected; full frozen初 family/raw source and independent follow-up judgment not yet supplied.",
                "remedy": "Resolve from actual source and precise labels in the SAME100 correction/source supplement; do not automatically add a transitive or merely topic-based pair.",
                "confidence": "Low-moderate hypothesis; not counted as verified defect.",
            },
        ],
        "optional": [
            {"id": "O1", "status": "optional", "reviewer": "claude",
             "claim": "More explicit look-alike block comparison at line55.", "disposition": "Nonblocking wording preference; existing distinction is not established false."},
            {"id": "O2", "status": "optional", "reviewer": "claude",
             "claim": "Use fabrication/made-up account instead of fabricated story at line23.",
             "disposition": "Existing can also mean a fabricated story is an instance, not an exhaustive gloss; no consequential mistranslation established."},
            {"id": "O3", "status": "optional", "reviewer": "claude",
             "claim": "Add sourced phonetic history.", "disposition": "Do not broaden: explicitly labelled mnemonic/structure-unclassified acceptable to both reviewers."},
            {"id": "O4", "status": "optional", "reviewer": "claude",
             "claim": "Shorten source-only phone text.", "disposition": "Nonblocking polish; preserve exact source/lexical-uncertainty distinctions."},
        ],
        "matchedSampleContributions": {
            "shared": "Readings/order, exact-spelling support, restrictions, rare spelling not pronunciation, three curated wrong choices, eight proposed direct guards, reciprocal navigation and shape/metadata accepted in both bounded reports.",
            "claudeUnique": "Localized compound-coverage findingF1, conditional missing-guard hypothesisH1 and four optional observations. H1's proposed傷 pair was not verified; follow-up established no such kanji card.",
            "gptUniqueVerifiedUsefulFindings": [],
            "coordinatorUnique": "Actual existing設 displayed-label overlap established after both initial reviews; initial reviewers did not inspect設 or初 cards.",
            "limits": "Compare equivalent observations across findings/optional/hypotheses/limits. These are sample observations, not a general model ranking; exact full-byte delivery is not comprehension certification.",
        },
        "sourceOnlyLexicalAllocation": "UNVERIFIED forショウ/けず.しける, explicitly qualified lookup-only and unselected; no invented lexical assertion accepted.",
        "initialReviewsComplete": True, "textualAcceptanceComplete": False, "reviewClosed": [],
        "runtimeChangedThisExecution": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT,
    }
    save(V / "batch-100-reconciliation.json", reconciliation)
    ledger_path = S / "batch-100-progress.json"
    ledger = load(ledger_path)
    ledger["status"] = "initial-textual-reviews-complete-reconciliation-required"
    ledger["limits"][0] = "Two blind serial textual initial reviews complete; unresolved localized coverage/meaning-guard reconciliation prevents review closure. No fresh Android/native/font/phone acceptance or publication."
    ledger["textualReview"] = {
        "execution": 748, "snapshot": SNAPSHOT, "models": reconciliation["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-100-reconciliation.json",
        "initialReviewsComplete": True, "textualAcceptanceComplete": False,
        "runtimeChangedThisExecution": False, "reviewClosed": [],
    }
    ledger["nextAction"] = NEXT
    save(ledger_path, ledger)
    checks = {}
    for label in ["tests", "validate", "manifest", "budget", "vocabulary", "audit", "whitespace"]:
        path = L / f"{label}-748.txt"
        text = path.read_text(encoding="utf-8-sig")
        if label == "tests":
            assert "Ran 43 tests" in text and text.rstrip().endswith("OK")
        elif label == "validate":
            assert text.strip() == "0 error(s)"
        elif label == "manifest":
            assert "8453 files" in text and "1bd5fb59e39b080d" in text
        elif label == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        elif label == "vocabulary":
            assert "2122/2431 reviewed prompts; stage=pilot" in text
        elif label == "audit":
            audit = json.loads(text)
            assert audit["exactBaseRuntimePreservedOutsideRecordedChanges"] and audit["manifestFresh"]
            assert audit["dictionaryFamilies"] == 153 and audit["readingDispositions"] == 6
        else:
            assert not text.strip()
        dest = V / f"batch-100-textual-review-{label}-748.txt.gz"
        dest.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        assert gzip.decompress(dest.read_bytes()) == path.read_bytes()
        checks[label] = {"archive": dest.name, "rawSha256": sha(path), "archiveSha256": sha(dest)}
    manifest = load(R / "manifest.json")
    payloads = {name: value for entries in manifest.values() if isinstance(entries, dict)
                for name, value in entries.items()}
    assert len(payloads) == 8453
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    assert build_manifest(R) == manifest
    save(V / "batch-100-runtime-preservation-748.json", {
        "snapshot": SNAPSHOT, "contentVersion": "1bd5fb59e39b080d",
        "runtimeHashesVerified": len(payloads), "runtimeDiffSinceFrozenDraft": [],
        "manifestByteUnchanged": True, "sourceAudit": "tools/audit_n1_batch.py --batch 100 passed",
        "limits": "No new linguistic/native acceptance inferred.",
    })
    save(V / "batch-100-textual-diagnostic-748.json", {
        "firstRecordAttempt": "AssertionError at raw-byte runtime hash comparison before commit. First differing entry curriculum/grammar.json has CRLF and its normalized hash exactly matches the existing manifest.",
        "rootCause": "Control checkpoint helper incorrectly used raw hashing for every payload. Production build_manifest.py deliberately normalizes CRLF for text and preserves binary bytes.",
        "remedy": "Use unchanged production build_manifest(root) equality for every current payload hash, language/schema and version. Keep separately verified git-clean runtime/manifest preservation. No runtime, manifest or validator rule changed.",
        "originalFailure": "checkpoint-748.py record, original line263: assert sha(R / Path(name)) == value; AssertionError",
        "actualNewPermissionDenials": [], "signingRetried": False,
        "archivalWhitespace": "Staged diff check found original dictionary whitespace and CLI trailing blank lines in immutable captures. Preserve both originals in lossless deterministic gzip, not rewritten/trimmed bytes or whitespace-rule relaxation. Original control review packet unchanged.",
    })
    archives = []
    for name in ["batch-100-initial-packet.txt", "batch-100-cli-config-help-execution-748.txt"]:
        path = V / (name + ".gz")
        raw = gzip.decompress(path.read_bytes())
        if "packet" in name:
            assert raw == (C / name).read_bytes()
        archives.append({"originalPath": name, "archive": path.name, "rawBytes": len(raw),
                         "rawSha256": hashlib.sha256(raw).hexdigest(),
                         "archiveSha256": sha(path), "lossless": True})
    save(V / "batch-100-lossless-capture-storage-748.json", archives)
    raw = (L / "staged-archival-whitespace-748.txt").read_bytes()
    (V / "batch-100-staged-archival-whitespace-748.txt.gz").write_bytes(gzip.compress(raw, mtime=0))
    for src, dest in [
        (C / "checkpoint-748.py", S / "batch-100-textual-checkpoint-recipe.py"),
        (C / "preflight-748.ps1", V / "batch-100-textual-preflight-748.ps1.txt"),
        (L / "preflight-748.json", V / "batch-100-textual-runner-role-748.json"),
    ]:
        shutil.copyfile(src, dest)
    save(S / "execution-748.json", {
        "schemaVersion": 1, "execution": 748, "batch": "100",
        "stage": reconciliation["status"], "originalTeachingSnapshot": SNAPSHOT,
        "androidSignedHead": APP, "freshOriginMain": MAIN,
        "startingState": load(C / "progress.json")["execution748StartingState"],
        "initialReviewers": processes, "reconciliation": "docs/n1-reviews/batch-100-reconciliation.json",
        "checks": checks, "pythonTestsPassed": 43, "validatorErrors": 0, "localBudget": budget,
        "runtimeHashesVerified": 8453, "runtimeChangedThisExecution": False,
        "contentVersion": "1bd5fb59e39b080d", "runtimePublished": False, "reviewClosed": [],
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 126,
        "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": NEXT,
    })
    print("Both complete initial reviews, reconciliation, actual process/read limits and runtime-preservation evidence archived.")


def issue():
    identity(signed=True)
    head = git("rev-parse", "HEAD")
    target = C / "batch-100-review-748-issue.txt"
    assert not target.exists()
    target.write_text(
        "Batch100: **two independent initial textual reviews completed; reconciliation remains open**.\n\n"
        f"Normally signed local evidence `{head}` preserves unchanged teaching snapshot `{SNAPSHOT}`. "
        "Claude Opus5.5 and GPT-6.1 Sol ran serially with view-only tools; each received the same "
        "260254-byte/6694-line packet (137member+16comparison complete families,13raw character "
        "records,17article bodies). Exact full packet return, zero internal tool overlap, actual "
        "model IDs and process exit before next reviewer verified. Byte delivery is not equal "
        "comprehension: Claude did not independently count137 member families. Full original "
        "reports/JSONL/session evidence retained.\n\n"
        "Claude identified a minor compound-example coverage gap; GPT judged coverage clean. "
        "Evidence-based reconciliation accepts minimal source-verified founding/wound examples, "
        "not a universal example quota; no teaching fix is yet applied. Conditional wound-guard "
        "hypothesis withdrawn because no kanji/傷.md exists (word article is another quiz namespace). "
        "Coordinator follow-up found actual設 label establish; provide overlapping the taught "
        "establishment sense: source supplement/direct-guard correction and original-session "
        "confirmations required. 初 remains a hypothesis, not a verified defect. Optional polish "
        "is separate; no model ranking or native-speaker certification.\n\n"
        "Evidence: docs/n1-reviews/batch-100-reconciliation.json, complete initial reports and "
        "process/coverage records; docs/n1-sources/execution-748.json. Runtime unchanged, all8453 "
        "hashes and contentVersion1bd5fb59e39b080d preserved;43focused tests/validator0errors/"
        "manifest/source-audit/budget checks passed. Vocabulary consistency retains its existing "
        "2122/2431pilot scope. No Android/native/rendered rerun, publication, batch101 or second "
        "runner. Parent5920/session ancestry verified; runner.lock untouched; durable control/"
        "committed evidence only; no new permission denial. Next SAME100 bounded correction/"
        "source supplement, signed changed-tree freeze and two serial original-session "
        "confirmations; every original later acceptance gate remains. Published coverage "
        "**126/1228;1102 acceptance remainder** unchanged. Physical-phone/general-release/"
        "whole-set acceptance outstanding; project incomplete.\n",
        encoding="utf-8")
    (L / "signed-head-748.txt").write_text(head + "\n", encoding="ascii")
    print("Signed clean local review-evidence checkpoint verified; owner issue body prepared.")


def finish():
    identity(signed=True)
    head = git("rev-parse", "HEAD")
    issue_data = load(L / "issue-748-verified.json")
    assert issue_data["user"]["login"] == "stop-cran"
    assert issue_data["body"] == (C / "batch-100-review-748-issue.txt").read_bytes().decode("utf-8")
    assert head in issue_data["body"]
    before, p = load(L / "progress-before-748.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    state = {
        "schemaVersion": 1, "execution": 748, "checkpoint": 748, "batch": "100",
        "savedCommit": head, "signature": "G", "originalTeachingSnapshot": SNAPSHOT,
        "freshOriginMain": MAIN, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-748.json",
        "reconciliation": "docs/n1-reviews/batch-100-reconciliation.json",
        "contentVersion": "1bd5fb59e39b080d", "initialReviewsComplete": True,
        "textualAcceptanceComplete": False, "runtimeDrafted": ["創"], "reviewClosed": [],
        "published": [], "runtimeChangedThisExecution": False, "runtimePublished": False,
        "independentReviewersLaunched": 2, "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "allAssignedRangesReturned": True, "freshAndroidOrNativeClaimed": False,
        "pythonTestsPassed": 43, "validatorErrors": 0, "runtimeHashesVerified": 8453,
        "unresolvedFindings": ["F1", "C1-establish"], "pendingHypotheses": ["H1-initial"],
        "withdrawnHypotheses": ["H1-wound"], "sourceOnlyLexicalAllocation": "UNVERIFIED; explicit source-only lookup rows, both unselected",
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before), "ownerIssueAuthorAndExactBodyVerified": True,
        "issueUpdate": issue_data["html_url"], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-100-initial-textual-reviews-complete-reconciliation-required",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
    }
    p["execution748CoordinatorCheckpoint"] = state
    p["execution748StartingState"]["status"] = "signed-local-initial-review-checkpoint-complete"
    p.update(checkpoint=748, status="continue", stage=state["stage"], batch="100",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    assert persisted == p
    assert all(persisted[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-748-final-verification.json", state)
    print(json.dumps({k: state[k] for k in ["checkpoint", "savedCommit", "status", "stage", "issueUpdate",
                                         "originalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"record": record, "issue": issue, "finish": finish}[sys.argv[1]]()
