"""Archive bounded rendered confirmations and persist a history-preserving checkpoint."""
import copy
import gzip
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("rendered_review", C / "render-batch-100-759.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
R, A, V, S, L = review.R, review.A, review.V, review.S, review.L
load, sha, git, now, save = review.load, review.sha, review.git, review.now, review.save
NEXT = (
    "SAME100 rendered confirmations COMPLETE on signed frozen cffdad1291d2acd847c669ab87c3c8b58572824f, "
    "runtime606c836e4be33ba9/qualifiedAndroidbf30cdead8515739bc0e671d57a54b9a3109dd46. "
    "Read docs/n1-sources/execution-759.json and docs/n1-reviews/batch-100-rendered-759-reconciliation.json. "
    "OriginalClaude4975f494/claude-opus-5.5 then GPTc9e3c7f4/gpt-6.1-sol exited0 serially; "
    "each read ownoriginalreports/common232523bytepacket and15actualPNGs(11sheets43captures,3originalfontpanels,"
    "1originalmeaningquestion);17serialviewcalls each,zerooverlaps,actualmodels/completeoriginalreports/captures "
    "retained. Claude initial normalization-only coverage assertion failed despite EXACT raw returned/file byte "
    "equality; immutableoriginalaudit plus exactbyte coverageaddendum resolves access, no reviewer rerun. "
    "Both CLEAN correctness/scopedcoverage/comprehensibility on創 andthree reusedchangedpassages, actual22labels/"
    "64sampledchoices and21Han/fourproductionfamily readability. N753-fallback-establish RESOLVED semantically755/"
    "mechanically758/rendered759; default蚕silkworm, no樹establish, no newlabels vs755set-minus樹. "
    "All11guards direct/symmetric/NONTRANSITIVE;2464direct/1760neighbor/2304word/64builder758checks retained. "
    "N1 TWOcurated剣倹 plusfallback because験N4; no mask/relevel/futurepoolguarantee. "
    "Sixfullreadings/order and selectedソウ/つく.る preserved. Sourceonlyショウ/けず.しける allocation remains "
    "UNVERIFIED/unselected, no invented resolution; no consequential unqualified teaching claim established. "
    "OriginalF1/C1-establish/H1-initial resolved andH1-woundwithdrawn;創/初 conservative not provenhistoricallivefailure. "
    "OptionalO1-O4/wrapping/old754linereferences nonblocking; no teaching edit. "
    "Rendering emulatorAPI35 notphone/fallbackfaceproof. Route sheets reduced; systemBack/offline relies on758"
    "execution notstillimages;12injectedstrokes/seededdue/shapeonly notMLKit/humanmastery. "
    "NEXT bounded SAME100 combined-current-main acceptance preparation/checks, THEN signedLOCALcheckpoint/yield: "
    "fresh signedheads/whollyclean/fetchoriginmain, inspect nonrewritingintegration need; no rewrite/push yet. "
    "FullrequiredPythonunittests/validator/manifestfreshness/vocabulary/baselinepreservation/exactmembership/"
    "reading/link/quiz/font/strokeaudits and actualcombinedarchive/path/media/budgets mandatory. "
    "Inherit756HOST3+1 and758native ONLY if runtime/Androidexactlyunchanged; changedpayload requires applicable"
    "HOST/native/rendered acceptance and changedsubstantiveteaching needs independentreview. Do not gratuitously"
    "rerun native on docs-only evidence HEAD. All8453runtimehashes/version/compiledarchiveequality must still match. "
    "Batch NOTreviewclosed/published until required combinedacceptance closes; nextpublication normal"
    "signing/ownerfastforward/exactremoteSHA/terminalgreenCI/EVERYimmutableZIPmanifesthash/budgets/verifiedownerissue. "
    "No unreviewedpush/101/authoragent/concurrentheavywork/secondrunner/signingretry/guardincrease. "
    "18000entries/42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia unchanged. "
    "Liveparent5920 ownsrunner.lock: verify ancestry/decodedlauncher/exactsession, no childacquire/delete/"
    "unlock/readprobe. Approvedcommittedsource/frozeninputs/controlhelpers only, not optionalhistoricalsession"
    "recipes; preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Published126/1228,1102acceptanceremainder,lastpublished716c610153234e8d2240dcf528de3ef83b654b27 unchanged. "
    "SixearlierN2placements保案派第策結 separate, neverduplicate/relevel. "
    "Physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def new(path, value):
    assert not path.exists(), path
    save(path, value)


def archive(source, destination):
    assert not destination.exists(), destination
    raw = source.read_bytes()
    destination.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(destination.read_bytes()) == raw
    return {"archive": destination.name, "rawBytes": len(raw), "rawSha256": sha(source),
            "archiveSha256": sha(destination), "lossless": True}


def verify_reports():
    records = {}
    for label, model in review.base.MODELS.items():
        prefix = f"batch-100-rendered-759-{label}"
        record = load(C / (prefix + "-execution.json"))
        assert record["snapshot"] == review.HEAD
        assert record["actualModels"] == [model] and record["usageCurrentModel"] == model
        assert record["sessionId"] == review.base.SESSIONS[label]
        assert record["exitCode"] == 0 and record["reviewerProcessExitVerified"]
        assert review.absent(record["launcherPid"])
        if label == "claude":
            addendum = load(C / (prefix + "-coverage-addendum.json"))
            assert addendum["originalExecutionSha256"] == sha(C / (prefix + "-execution.json"))
            assert addendum["allAssignedResourcesReturned"] and addendum["exactRawWholeFileBytesEqual"]
            assert record["missingResources"] == [str(review.PACKET)]
        else:
            assert record["allAssignedResourcesReturned"] and not record["missingResources"]
        assert not record["observedToolOverlaps"] and not record["unfinishedTools"]
        assert record["multiToolResponseCount"] == 0 and record["availableTools"] == ["view"]
        assert len(record["toolCalls"]) == 17
        assert all(call["success"] and not call["truncationMarker"] for call in record["toolCalls"])
        images = [call["arguments"]["path"] for call in record["toolCalls"]
                  if call["arguments"]["path"].endswith(".png")]
        provenance = load(L / "rendered-759-provenance.json")
        assert images == [row["path"] for row in provenance["images"]]
        assert sha(C / (prefix + ".md")) == record["reportSha256"]
        assert sha(C / (prefix + ".jsonl")) == record["rawExecutionSha256"]
        records[label] = record
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    return records


def record():
    review.frozen()
    records = verify_reports()
    storage = []
    for label in records:
        prefix = f"batch-100-rendered-759-{label}"
        for suffix in [".md", "-execution.json", "-stderr.txt", "-prompt.txt", "-usage.json"]:
            destination = V / (prefix + suffix)
            assert not destination.exists()
            shutil.copyfile(C / (prefix + suffix), destination)
        for suffix in [".jsonl", "-own-reports.txt"]:
            storage.append(archive(C / (prefix + suffix), V / (prefix + suffix + ".gz")))
    destination = V / "batch-100-rendered-759-claude-coverage-addendum.json"
    assert not destination.exists()
    shutil.copyfile(C / destination.name, destination)
    storage.append(archive(review.PACKET, V / "batch-100-rendered-759-packet.txt.gz"))
    for kind in ["help", "config-help"]:
        storage.append(archive(L / f"copilot-{kind}-759.txt", V / f"batch-100-cli-{kind}-execution-759.txt.gz"))
    for source, target in [
        (L / "rendered-759-provenance.json", V / "batch-100-rendered-759-provenance.json"),
        (L / "preflight-759.json", V / "batch-100-rendered-759-runner-role.json"),
        (L / "render-batch-100-759-original.py", S / "batch-100-rendered-759-original-recipe.py"),
        (C / "render-batch-100-759.py", S / "batch-100-rendered-759-recipe.py"),
        (C / "checkpoint-rendered-759.py", S / "batch-100-rendered-759-checkpoint-recipe.py"),
        (C / "preflight-759.ps1", V / "batch-100-rendered-759-preflight.ps1.txt"),
        (C / "post-batch-100-rendered-759.ps1", V / "batch-100-rendered-759-issue-recipe.ps1.txt"),
    ]:
        assert not target.exists()
        shutil.copyfile(source, target)
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    assert manifest["contentVersion"] == "606c836e4be33ba9"
    entries = {name: value for group in manifest.values() if isinstance(group, dict)
               for name, value in group.items()}
    assert len(entries) == 8453
    assert (R / "manifest.json").read_bytes() == subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", f"{review.HEAD}:manifest.json"])
    confirmations = {
        label: {**{k: row[k] for k in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
            "actualModels", "snapshot", "reportSha256", "rawExecutionSha256"]},
            "report": f"batch-100-rendered-759-{label}.md",
            "execution": f"batch-100-rendered-759-{label}-execution.json",
            "processExitVerified": True, "internalToolCalls": 17,
            "internalToolOverlaps": 0, "requiredImagesViewed": 15,
            "completeSuppliedTextReturned": True}
        for label, row in records.items()
    }
    reconciliation = {
        "schemaVersion": 1, "execution": 759, "batch": "100", "snapshot": review.HEAD,
        "status": "rendered-confirmations-complete-awaiting-combined-acceptance",
        "qualifiedAndroidHead": review.base.APP, "contentVersion": manifest["contentVersion"],
        "confirmations": confirmations, "serialProcessesAndInternalToolsVerified": True,
        "originalReportsAndRawExecutionsPreserved": True,
        "independentRenderedReviewClosed": True, "freshBlindReviewCredit": False,
        "verdicts": {unit: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
                             "comprehensibility": "CLEAN"}
                     for unit in ["kanji/創.md", "words/創作.md:30", "words/作る.md:36", "kanji/作.md:45"]},
        "sampledMeaningSemantics": "CLEAN", "fourFamilyRenderedReadability": "CLEAN",
        "findings": [],
        "reconciliation": {
            "N753-fallback-establish": {
                "status": "resolved",
                "evidence": "755source/diff confirmation;758changed-version direct樹guard/pools enforced;759both original families inspected actual question/options and22labels/64projectedchoices. Default蚕silkworm is distinct;樹establish removed.",
                "scope": "Source-backed direct pair and actual sampled states, not universal future fallback safety."},
            "F1": {"status": "resolved", "evidence": "創立/創傷 examples/register retained and readable."},
            "C1-establish": {"status": "resolved", "evidence": "Direct創/設 overlap retained, no legacy edit."},
            "H1-initial": {"status": "resolved", "evidence": "Conservative創/初 safeguard retained; not proven historical live failure or universal synonymy."},
            "H1-wound": {"status": "withdrawn", "evidence": "Word傷 namespace does not create missing kanji choice."},
        },
        "optional": [
            "Claude retains O1-O4 shape-comparison precision/fabrication wording/qualified phonetic note/table brevity; all nonblocking.",
            "Claude notes mid-word wrapping/hyphenation as optional, not essential clipping. Old754line references already qualified in755; immutable evidence unchanged.",
        ],
        "interpretiveQualifications": [
            "Claude's 'none of22 labels overlaps' is read against its preceding actual-option assessment as excluding the correct target創; both reports identify創 as target. No new all-pairs claim.",
            "Possible fallback visual appearance is not proof of actual selected face; both reviewers expressly disclaim font provenance.",
            "Both saw15images each:11reduced contact sheets covering43routecaptures plus3originalfontpanels and1originalmeaningquestion. Neither claims full-resolution inspection of all46originalPNGs.",
            "Offline/SystemBack rely on758execution records, not still-image proof.",
        ],
        "accessDiagnostic": load(C / "batch-100-rendered-759-claude-coverage-addendum.json"),
        "sourceOnlyReadingLimits": "ショウ/けず.しける independent lexical allocation remains explicitlyUNVERIFIED/unselected; full metadata/order preserved. No new consequential unqualified teaching claim established.",
        "nativeAcceptance": "758two namedterminalcase0/no skips inherited, not repeated.2464direct/1760NONTRANSITIVEneighbor/2304word/64builderchecks; N1two curated剣倹 plusfallback;験N4. Twelve injectedstrokes/shapeonly fallback notMLKit/humanmastery.",
        "hostAcceptance": "756HOST3RealContentTest+1RareHanTest retained for byte-identical runtime; not rerun here.",
        "limits": [
            "Dependent original-session confirmation, not fresh blind review, independent upstream/Git/native reproduction or equal comprehension.",
            "API35 emulator/192m is not physical-phone or all-device acceptance. No measured learning effectiveness.",
            "Coordinator supplied full755packet and current758 scalar/all64choices projection; repeated memberships/mechanical rows omitted from projection, full original retained.",
            "Runtime acceptance/publication still requires combined-current-main checks, normal signing and publication gates.",
        ],
        "runtimeHashesVerified": 8453, "runtimeChanged": False, "manifestChanged": False,
        "runtimeAccepted": False, "runtimePublished": False, "reviewClosed": [], "published": [],
        "nextAction": NEXT,
    }
    new(V / "batch-100-rendered-759-reconciliation.json", reconciliation)
    new(V / "batch-100-rendered-759-lossless-storage.json", storage)
    previous = load(V / "batch-100-reconciliation.json")
    assert "renderedConfirmation759" not in previous
    previous["statusBefore759"] = previous["status"]
    previous["status"] = reconciliation["status"]
    previous["renderedConfirmation759"] = reconciliation
    save(V / "batch-100-reconciliation.json", previous)
    ledger = load(S / "batch-100-progress.json")
    assert ledger["reviewClosed"] == ledger["published"] == []
    ledger["statusBefore759"] = ledger["status"]
    ledger["nextActionBefore759"] = ledger["nextAction"]
    ledger["limitsBefore759"] = ledger["limits"]
    ledger.update(
        status=reconciliation["status"], independentRenderedReviewClosed=True,
        renderedConfirmation759="docs/n1-reviews/batch-100-rendered-759-reconciliation.json",
        runtimeAccepted=False, runtimePublished=False, nextAction=NEXT)
    ledger["limits"] = [
        "Original750/755textual,756HOST,758correctednative and759original-family rendered confirmations complete on exact runtime606c836e4be33ba9. Combined-current-main acceptance/publication pending; batch NOTreviewclosed.",
        "Sixfullreadings/order retained; sourceonlyショウ/けず.しける independent lexical allocation remains explicitlyUNVERIFIED/unselected.",
        "Fiveallmappedpairs/ten directions/oneactivatedbaselinepair; threeexactreusedchanges andN2/N5metadata/13&5wordguards preserved.",
        "Eleven direct symmetric NONTRANSITIVE guards; actual22labels/64sampledchoices CLEAN, not universal futurepool safety. N1two curated剣倹 plusfallback;験N4.",
        "21Han/fourproduction-family panels readable. Contact sheets reduced; no fallback-face provenance, physical-phone, MLKit/humanmastery or all-device claim.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/path/media/budget/owner-issue gates retained; no101 or second runner.",
        "Published126/1228,1102acceptanceremainder unchanged; sixearlierN2placements separate; physicalphone/generalrelease/whole-set outstanding.",
    ]
    save(S / "batch-100-progress.json", ledger)
    new(S / "execution-759.json", {
        "schemaVersion": 1, "execution": 759, "batch": "100", "stage": reconciliation["status"],
        "startingState": load(C / "progress.json")["execution759StartingState"],
        "snapshot": review.HEAD, "qualifiedAndroidHead": review.base.APP,
        "freshOriginMain": review.base.MAIN, "confirmations": confirmations,
        "reconciliation": "docs/n1-reviews/batch-100-rendered-759-reconciliation.json",
        "independentRenderedReviewClosed": True, "freshBlindReviewCredit": False,
        "finding": "N753-fallback-establish", "findingStatus": "resolved semantically755/mechanically758/rendered759",
        "runtimeHashesVerified": 8453, "contentVersion": manifest["contentVersion"],
        "runtimeChanged": False, "manifestChanged": False,
        "freshAndroidOrNativeClaimed": False, "runtimeAccepted": False, "runtimePublished": False,
        "reviewClosed": [], "published": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 126, "remainingAdditions": 1102,
        "lastPublishedCommit": review.base.MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "validation": "Docs-only evidence; build_manifest equality recomputed,8453runtimehashes verified. Validator and generator commands recorded separately before signed checkpoint; unchanged manifest required.",
        "nextAction": NEXT,
    })
    print("Both complete serial rendered confirmations archived; combined acceptance/publication still pending.")


def finish():
    current = load(C / "progress.json")
    before = load(L / "progress-before-759.json")
    assert (current["checkpoint"], current["batch"], current["status"]) == (758, "100", "continue")
    runner = load(C / "runner.json")
    assert (runner["status"], runner["sessionId"], runner["pid"]) == ("running", L.name, 5920)
    assert not review.absent(5920)
    head = git("rev-parse", "HEAD")
    assert head != review.HEAD and git("rev-parse", "HEAD^") == review.HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "origin/main") == review.base.MAIN
    assert git("rev-parse", "HEAD", root=A) == review.base.APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    assert not git("diff", review.HEAD, head, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    verify_reports()
    comment = load(L / "issue-759-reread.json")
    posted = load(L / "issue-759-posted.json")
    bodypath = C / "batch-100-rendered-759-issue-body.txt"
    body = bodypath.read_bytes().decode("utf-8")
    assert comment["user"]["login"] == posted["author"] == "stop-cran"
    assert comment["body"] == body and head in body and sha(bodypath) == posted["bodySha256"]
    assert comment["html_url"] == posted["url"]
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in changed:
            assert current[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 759, "checkpoint": 759, "batch": "100",
        "status": "continue", "stage": "batch-100-rendered-confirmations-complete-awaiting-combined-acceptance",
        "recordedAt": now(), "savedCommit": head, "signature": "G",
        "qualifiedAndroidHead": review.base.APP, "evidence": "docs/n1-sources/execution-759.json",
        "issueUpdate": comment["html_url"], "ownerIssueAuthorAndExactBodyVerified": True,
        "independentRenderedReviewClosed": True, "originalSessionConfirmations": 2,
        "actualModels": list(review.base.MODELS.values()), "serialReviewerProcessExitsVerified": True,
        "internalToolOverlaps": 0, "toolCallsEach": 17, "imagesEach": 15,
        "contactSheetsEach": 11, "routeCapturesCovered": 43, "originalFontPanelsEach": 3,
        "completeSuppliedTextReturnedEach": True, "packetBytes": 232523, "packetLines": 11686,
        "claudeCoverageAddendum": "docs/n1-reviews/batch-100-rendered-759-claude-coverage-addendum.json",
        "finding": "N753-fallback-establish", "findingStatus": "resolved semantically755/mechanically758/rendered759",
        "runtimeHashesVerified": 8453, "contentVersion": "606c836e4be33ba9",
        "runtimeChanged": False, "manifestChanged": False, "runtimeAccepted": False,
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "reviewClosed": [], "published": [], "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "publishedAdditions": 126, "remainingAdditions": 1102,
        "lastPublishedCommit": review.base.MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "nextAction": f"SAME100 signed LOCAL evidenceHEAD{head}. " + NEXT,
        "inherited758NextActionPreserved": before["nextAction"],
        "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "blocker": None,
    }
    after = copy.deepcopy(current)
    assert "execution759CoordinatorCheckpoint" not in after
    after["execution759CoordinatorCheckpoint"] = checkpoint
    for key in changed:
        after[key] = checkpoint[key]
    for key, value in before.items():
        if key not in changed:
            assert after[key] == value, key
    new(L / "checkpoint-759-summary.json", checkpoint)
    assert load(C / "progress.json") == current
    save(C / "progress.json", after)
    assert load(C / "progress.json") == after
    print(json.dumps({"checkpoint": 759, "status": "continue", "savedCommit": head,
                      "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True}))


if __name__ == "__main__":
    {"record": record, "finish": finish}[sys.argv[1]]()
