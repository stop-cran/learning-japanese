"""Persist batch101's bounded textual-review evidence, not publication acceptance."""
import ast
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "df7fcd8c-a828-4dec-92fb-7b2ca99864f3"
SNAPSHOT = "7f275e0de16fe3a4588fac1845af5af80d487415"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
MAIN = "ba1a7f467a2431523e3131d4f259c1d3260c93af"
NEXT = (
    "SAME101 fresh qualifiedAndroidbf30cdead HOST acceptance checkpoint: non-skipped RealContentTest/"
    "RareHanTest plus actual production meaning-builder defaultN1/All/custom-pool choices and direct "
    "symmetric NONTRANSITIVE guards. Two blind different-family initial TEXTUAL reviews COMPLETE on "
    "signed7f275e0d; reconciliation has no actionable changed-text defect and no teaching correction "
    "was needed. Do not rerun initials or claim full batch closure/publication. Preserve Claude "
    "3bed863f-b19d-4de6-9a11-1ba15e409a84 and GPTd82fb475-a4fb-4ea4-9da9-945d176127cd original "
    "reports/model/process/exact full packet return/read limits. Both received same99member+23comparison "
    "families/18rawcharacterrecords/20articlebodies; exact byte return is not comprehension or independent "
    "upstream retrieval. Optional alternate-spelling/etymology expansions declined; valid-in-religious-"
    "compounds is not exclusively/mainly religious, no invented frequency. GPT's six uninspected retained "
    "word-guard labels remain UNVERIFIED outside the exact navigation-only scope; unchanged guards were "
    "not newly certified. Inspect actual labels if making a later complete word-choice claim. "
    "Preserve [コウ,ク]/[いさお] order, onlyコウ selected with own-row links to 功績こうせきN2/"
    "成功せいこうN3; ク valid recognition, いさお dated lexical noun NOT merely nanori. No new "
    "support identity/level. Three exact navigation-only reused changes/all metadata/seven功績guards "
    "preserved. Four allmappedpairs/eightdirections/fivenew/twoactivatedbaselinepairs include成-成功. "
    "Three semantically wrong curated labels加幼刀 and thirteen direct kanji guards textually accepted; "
    "two choices outsideN1 require actual defaultN1 fallback acceptance. Any newly established ambiguity "
    "requires exact full frozen source/labels, minimal justified change, recomputed audits/manifest, "
    "normal signed changed-tree freeze and BOTH original-session changed-passage confirmations. "
    "Then productionContentSyncONCE/native N1/All/meaning/curatedreading/drawing/article/Back/offline/"
    "four-font/all-Han/rendered acceptance and two serial rendered reviews as applicable. Five pinned "
    "paths/canonical力19right/工left/labelledmodernshapemnemonic/structure-unclassified; actual19Han "
    "allcmaps/zeroRareHan is NOT rendering acceptance. Native fixtures must bind current content/"
    "signedqualifiedapp, unchanged2gguest/192mheap/oneworker, exactownedport/device checks, terminal "
    "case0 evidence and owned-helper cleanup. No current native/rendered/physical-phone claim. "
    "Keep combinedcurrentmain/allrequiredPython/vocabulary/normal signing/ownerfastforward/"
    "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed80MiBinflated"
    "56MiBretained/perfilepathmedia/verifiedownerissue gates. No unreviewedpush/102/authoragent/"
    "concurrentheavywork/secondrunner/signingretry/guardincrease. Verify whollyclean signedheads/"
    "freshmain/liveparentancestry/decodedlauncher/exactsession. Parent5920 ownsrunner.lock: no "
    "childacquire/delete/unlock/readprobe. Approvedcontrol/committedsource/frozeninputs only, not "
    "optional historicalsessionrecipes; preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. QualifiedAndroidapprovedpairguard+schemaonly, NOT unrelated latestmain. "
    "Published127/1228,1101acceptance remainder unchanged; six earlierN2placements保案派第策結 "
    "separate. CompatibleAndroid#125+#132 required; oldclientsignorecuration/guards. Physicalphone/"
    "generalrelease/whole-setoutstanding;projectincomplete. Historical limitations preserved."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".765.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == data
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


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
    assert all(n.startswith("docs/n1-reviews/batch-101-")
               or n == "docs/n1-sources/batch-101-progress.json"
               or n == "docs/n1-sources/execution-765.json" for n in changes), changes
    assert not git("status", "--porcelain", "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    assert git("rev-parse", "origin/main") == MAIN
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (764, "101", "continue")


def record():
    identity()
    processes = {}
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        prefix = f"batch-101-initial-{label}"
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
        assert sha(V / (prefix + ".md")) == execution["reportSha256"]
        raw = V / (prefix + ".jsonl")
        assert sha(raw) == execution["rawExecutionSha256"]
        archive = V / (prefix + ".jsonl.gz")
        assert not archive.exists()
        archive.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw.read_bytes()
        processes[label] = {k: execution[k] for k in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
            "snapshot", "reportSha256", "rawExecutionSha256"]}
        processes[label].update(
            report=prefix + ".md", execution=prefix + "-execution.json",
            coverage=prefix + "-coverage.json", allAssignedRangesReturned=True,
            toolCalls=1, observedToolOverlaps=0, exactFullPacketReturnedInFirstCall=True,
            losslessExecutionArchive=archive.name, archiveSha256=sha(archive))
        raw.unlink()
    assert processes["claude"]["completedAt"] < processes["gpt"]["startedAt"]
    required = load(V / "batch-101-required-review-ranges.json")[0]
    assert sha(C / "batch-101-initial-packet.txt") == required["sha256"]
    provenance = load(V / "batch-101-review-dictionary-provenance.json")
    assert provenance["distinctCompleteFamilies"] == 122 and provenance["rawCharacterRecords"] == 18
    reconciliation = {
        "schemaVersion": 1, "execution": 765, "batch": "101",
        "status": "textual-review-closed-runtime-acceptance-pending",
        "originalTeachingSnapshot": SNAPSHOT, "teachingChangedAfterInitialReviews": False,
        "initialModels": ["claude-opus-5.5", "gpt-6.1-sol"], "processes": processes,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 244842, "initialPacketLines": 5743,
        "completeFamiliesSupplied": 122, "rawCharacterRecordsSupplied": 18,
        "completeArticleBodies": 20, "newArticleBodies": 1, "changedReusedPassages": 3,
        "readDepthLimits": "Both executions returned exact full packet in one serial view call. Byte access is not comprehension, native-speaker certification or independent upstream retrieval. Both report inspecting all122 families but did not independently verify byte/line counts. Raw功 record supplied in comparison packet, not separate duplicate raw packet.",
        "verdicts": {
            unit: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
            for unit in ["kanji/功.md:1-51", "words/功績.md:28-30",
                         "words/成功.md:28-30", "kanji/成.md:38"]
        },
        "findings": [],
        "consequentialUnresolvedChangedTeachingClaims": [],
        "optional": [
            {"id": "O1", "status": "optional", "reviewer": "claude",
             "claim": "Note that JMdict2411570 lists勲 before功.",
             "disposition": "No edit. Complete dated noun family supports exact功/いさお with no spelling restriction; listing order does not invalidate this documented spelling or require a spelling detour. No commonness claim is made.",
             "evidence": "Complete frozen2411570 and actual Seisenbanいさお【功・勲・績】heading."},
            {"id": "O2", "status": "withdrawn", "reviewer": "claude optional",
             "claim": "Change valid reading in religious compounds to mainly in religious compounds because Daijisen also lists功夫くふう.",
             "disposition": "No defect established: valid in does not say only in. Adding mainly would introduce an unmeasured distribution claim. The actual row gives a precisely sourced religious example, not an unrestricted/exhaustive lexical partition.",
             "evidence": "kanji/功.md:34,37; Daijisen characterク lists功徳/功力 and功夫. Complete1275080 has Buddhist and Christian senses."},
            {"id": "O3", "status": "optional", "reviewer": "claude",
             "claim": "Could add sourced phonetic history from Jitsu/SVG.",
             "disposition": "No edit or scope expansion. Labelled modern-shape mnemonic/structure-unclassified explicitly adopts no historical/phonetic account; omission is not a claim that no phonetic component exists.",
             "evidence": "kanji/功.md:5,27 and supplied Jitsu/SVG. Both reviewers found current approach acceptable."},
        ],
        "boundedEvidenceLimits": [
            {
                "id": "L1", "status": "unresolved", "reviewer": "gpt",
                "facet": "unchanged legacy guard label audit, outside exact navigation-only review closure",
                "claim": "Six of功績's seven guarded word articles and displayed titles were not supplied. Their exact full label-level behavior remains UNVERIFIED.",
                "disposition": "Preserve explicitly, do not claim new complete legacy-word-choice certification. No title/guard changed, and exact old seven exclusions are preserved. No new missing pair or contradictory teaching established. Later complete word-choice claim requires actual labels/evidence; no legacy rewrite or automatic exclusion expansion.",
            },
            {
                "id": "L2", "status": "unresolved", "facet": "runtime/native acceptance",
                "claim": "Default N1 uses fallback because加/幼 are outside N1; no production-builder/native/font/rendered acceptance performed.",
                "disposition": "Mandatory next gates, not CLEAN runtime acceptance. Three curated choices and thirteen direct guards are textually defensible; test actual live pools and reconcile any established ambiguity before native/publication.",
            },
        ],
        "matchedSampleContributions": {
            "shared": "All four assigned teaching units CLEAN in three facets; full readings/order and qualified recognition rows, exact selected allocation/support, merit/effect scope, three wrong labels, thirteen direct conservative guards, eight reciprocal directions, navigation-only preservation and mnemonic metadata accepted.",
            "claudeUnique": "Two optional expansion observations and the nonexclusive-religious wording suggestion. None established an actionable defect; no useful defect credit invented.",
            "gptUnique": "Explicit exact-label coverage limitation for six unchanged word guards. Claude generally noted unavailable whole corpus labels, but did not identify this precise six-word evidence boundary. Useful scoped reporting clarification, not a proved teaching defect.",
            "limits": "Common matched sample; compare equivalent optional/limits/hypothesis observations, not severity labels. Not a general model ranking or equal-comprehension certification.",
        },
        "coordinatorEvidence": "Freshly inspected all three reused article bodies, target body, seven applicable complete member families and all23 complete comparison families in bounded12/11 ranges after an initial21.3KiB output was truncated. Actual public authority-headed extracted blocks inspected. No new upstream fetch or fresh99-family reread claimed.",
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "fullBatchAcceptanceComplete": False, "reviewClosed": [],
        "runtimeChangedThisExecution": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT,
    }
    save(V / "batch-101-reconciliation.json", reconciliation)
    ledger_path = S / "batch-101-progress.json"
    ledger = load(ledger_path)
    ledger["status"] = reconciliation["status"]
    ledger["limits"][0] = "Two blind serial textual initial reviews reconciled without teaching changes; full batch review closure awaits fresh qualified Android/production choices/native/rendered/integration/publication gates. No runtime publication."
    ledger["textualReview"] = {
        "execution": 765, "snapshot": SNAPSHOT, "models": reconciliation["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-101-reconciliation.json",
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "fullBatchAcceptanceComplete": False, "runtimeChangedThisExecution": False,
        "reviewClosed": [], "legacyWordGuardFullLabelAudit": "UNVERIFIED; six old guard titles not supplied, outside exact unchanged-navigation review closure",
    }
    ledger["nextAction"] = NEXT
    save(ledger_path, ledger)
    checks = {}
    for label in ["tests", "validate", "budget", "vocabulary", "audit", "whitespace"]:
        path = L / f"{label}-765.txt"
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
            assert audit["dictionaryFamilies"] == 122 and audit["readingDispositions"] == 3
        else:
            assert not text.strip()
        dest = V / f"batch-101-textual-review-{label}-765.txt.gz"
        dest.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        assert gzip.decompress(dest.read_bytes()) == path.read_bytes()
        checks[label] = {"archive": dest.name, "rawSha256": sha(path), "archiveSha256": sha(dest)}
    manifest = load(R / "manifest.json")
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    assert build_manifest(R) == manifest
    payloads = {name: value for entries in manifest.values() if isinstance(entries, dict)
                for name, value in entries.items()}
    assert len(payloads) == 8455 and manifest["contentVersion"] == "6e9b74967e21fc3c"
    assert (R / "manifest.json").read_bytes() == subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", f"{SNAPSHOT}:manifest.json"])
    save(V / "batch-101-runtime-preservation-765.json", {
        "snapshot": SNAPSHOT, "contentVersion": manifest["contentVersion"],
        "runtimeHashesVerified": len(payloads), "runtimeDiffSinceFrozenDraft": [],
        "manifestBytesUnchanged": True, "manifestFreshFromProductionGenerator": True,
        "limits": "No runtime change, app/native/rendered evidence or exact immutable GitHub ZIP acceptance inferred.",
    })
    for name in ["preflight-765.ps1", "checks-batch-101-review-765.ps1", "checkpoint-review-765.py",
                 "post-batch-101-review-765.ps1"]:
        shutil.copyfile(C / name, V / ("batch-101-" + name + (".txt" if name.endswith(".ps1") else "")))
    shutil.copyfile(L / "preflight-765.json", V / "batch-101-runner-role-765.json")
    save(S / "execution-765.json", {
        "schemaVersion": 1, "execution": 765, "batch": "101",
        "stage": reconciliation["status"], "originalTeachingSnapshot": SNAPSHOT,
        "androidSignedHead": APP, "freshOriginMain": MAIN,
        "startingState": load(C / "progress.json")["execution765StartingState"],
        "initialReviewers": processes, "reconciliation": "docs/n1-reviews/batch-101-reconciliation.json",
        "checks": checks, "pythonTestsPassed": 43, "validatorErrors": 0, "localBudget": budget,
        "runtimeHashesVerified": 8455, "runtimeChangedThisExecution": False,
        "contentVersion": manifest["contentVersion"], "runtimePublished": False, "reviewClosed": [],
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "fullBatchAcceptanceComplete": False, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 127, "remainingAdditions": 1101, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "legacyWordGuardFullLabelAudit": reconciliation["boundedEvidenceLimits"][0],
        "nextAction": NEXT,
    })
    print("Both complete initial reviews, reconciliation and unchanged-runtime evidence archived.")


def issue():
    identity(signed=True)
    head = git("rev-parse", "HEAD")
    target = C / "batch-101-review-765-issue.txt"
    assert not target.exists()
    target.write_text(
        "Batch101 / checkpoint765: **two independent textual reviews completed and reconciled; "
        "runtime acceptance remains pending**.\n\n"
        f"Normally signed local evidence `{head}` preserves unchanged teaching snapshot `{SNAPSHOT}`. "
        "Claude Opus5.5 and GPT-6.1 Sol ran serially with view-only tools against the same "
        "244842-byte/5743-line packet:99member+23comparison complete families,18raw character "
        "records,20complete article bodies. Actual model IDs, full exact packet return, zero "
        "internal tool overlap and process exit before the second launch verified. Byte delivery "
        "is not comprehension or independent upstream retrieval; complete original reports, "
        "lossless JSONL, session/process/coverage evidence retained.\n\n"
        "Both reviews found no actionable correctness, scoped-coverage or text-comprehensibility "
        "defect in new功 or the three exact navigation-only changes (功績,成功,成). Reading "
        "order/qualification, selectedコウ examples, three curated wrong labels, thirteen direct "
        "nontransitive guards and four mapped pairs/eight link directions accepted textually. "
        "No teaching change was needed. Optional spelling-order/phonetic expansion declined; "
        "valid-in-religious-compounds is nonexclusive and does not justify adding an unmeasured "
        "mainly-frequency claim. GPT explicitly left six retained功績 word-guard labels unverified "
        "because those old cards were not supplied; no new full legacy-word-choice certification "
        "is claimed. Reports and limits: docs/n1-reviews/batch-101-reconciliation.json; "
        "docs/n1-sources/execution-765.json.\n\n"
        "Runtime bytes/manifest unchanged; all8455 hashes and contentVersion6e9b74967e21fc3c "
        "verified through the production manifest generator.43focused tests, validator0errors, "
        "batch/source/baseline/link/reading audits and unchanged local publishing budgets passed. "
        "Vocabulary consistency retains its2122/2431pilot scope. No fresh Android/native/rendered "
        "acceptance, push, batch102 or second runner. Parent5920/exact session/ancestry verified; "
        "runner.lock untouched; durable control/committed evidence only; no new denial.\n\n"
        "Next SAME101 fresh qualified Android host checks/non-skipped RealContentTest/RareHanTest "
        "and actual defaultN1/All production meaning-builder/fallback acceptance (加/幼 are "
        "outsideN1), followed by current-content native/rendered and every original integration/"
        "publication gate. Compatible stop-cran/kanji-cards-android#125 and "
        "stop-cran/kanji-cards-android#132 mechanisms remain required. **127/1228 published; "
        "1101 acceptance remainder unchanged.** Physical-phone/general-release/whole-set "
        "acceptance outstanding; project incomplete.\n",
        encoding="utf-8", newline="\n")
    (L / "signed-head-765.txt").write_text(head + "\n", encoding="ascii")
    print("Signed clean local textual-review checkpoint verified; owner issue body prepared.")


def archive():
    identity()
    archives = []
    for name in ["batch-101-initial-packet.txt", "batch-101-cli-config-help-execution-765.txt"]:
        raw = V / name
        target = V / (name + ".gz")
        assert raw.exists() and not target.exists()
        target.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw.read_bytes()
        archives.append({"rawName": name, "rawSha256": sha(raw), "archive": target.name,
                         "archiveSha256": sha(target), "losslessGzip": True})
        raw.unlink()
    save(V / "batch-101-evidence-packaging-765.json", {
        "snapshot": SNAPSHOT, "archives": archives,
        "diagnostic": "First staged diff --check found whitespace originating in supplied XML and CLI catalog output; the chained command stopped before git commit, so no signing attempt occurred. Preserve exact original bytes using lossless gzip rather than modifying reviewer inputs or relaxing whitespace checks. Original control packet remains unchanged.",
        "runtimeChanged": False, "reviewerInputsChanged": False, "signingAttemptedOnFailedCheck": False,
    })
    shutil.copyfile(Path(__file__), V / "batch-101-checkpoint-review-765.py")
    print("Exact packet and CLI catalog archived losslessly; original reviewer inputs unchanged.")


def finish():
    identity(signed=True)
    head = git("rev-parse", "HEAD")
    issue_data = load(L / "issue-765-verified.json")
    assert issue_data["user"]["login"] == "stop-cran"
    assert issue_data["body"] == (C / "batch-101-review-765-issue.txt").read_text(encoding="utf-8")
    assert head in issue_data["body"]
    before, p = load(L / "progress-before-765.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    state = {
        "schemaVersion": 1, "execution": 765, "checkpoint": 765, "batch": "101",
        "savedCommit": head, "signature": "G", "originalTeachingSnapshot": SNAPSHOT,
        "freshOriginMain": MAIN, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-765.json",
        "reconciliation": "docs/n1-reviews/batch-101-reconciliation.json",
        "contentVersion": "6e9b74967e21fc3c", "initialReviewsComplete": True,
        "textualAcceptanceComplete": True, "fullBatchAcceptanceComplete": False,
        "runtimeDrafted": ["功"], "reviewClosed": [], "published": [],
        "runtimeChangedThisExecution": False, "runtimePublished": False,
        "independentReviewersLaunched": 2, "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "allAssignedRangesReturned": True, "freshAndroidOrNativeClaimed": False,
        "pythonTestsPassed": 43, "validatorErrors": 0, "runtimeHashesVerified": 8455,
        "unresolvedChangedTeachingFindings": [],
        "legacyWordGuardFullLabelAudit": "UNVERIFIED; six old guard titles not supplied, outside navigation-only textual scope. Full native/runtime acceptance also pending.",
        "publishedAdditions": 127, "remainingAdditions": 1101, "lastPublishedCommit": MAIN,
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before), "ownerIssueAuthorAndExactBodyVerified": True,
        "issueUpdate": issue_data["html_url"], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-101-textual-review-closed-runtime-acceptance-pending",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
    }
    p["execution765CoordinatorCheckpoint"] = state
    p["execution765StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    p.update(checkpoint=765, status="continue", stage=state["stage"], batch="101",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    assert persisted == p
    assert all(persisted[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-765-final-verification.json", state)
    print(json.dumps({k: state[k] for k in ["checkpoint", "savedCommit", "status", "stage", "issueUpdate",
                                         "originalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"record": record, "archive": archive, "issue": issue, "finish": finish}[sys.argv[1]]()
