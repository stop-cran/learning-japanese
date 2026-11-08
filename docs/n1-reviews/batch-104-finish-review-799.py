"""Persist batch 104 textual closure without claiming runtime acceptance."""
import gzip
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("batch104", C / "review-batch-104-799.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
r = b.review
R, A, S, V, L = b.R, b.A, b.S, b.V, b.L
INITIAL = b.HEAD
REVISED = "089a60b2e7f94d57d24758777ba9d586d45209cf"
STAGE = "batch-104-textual-review-closed-runtime-acceptance-pending"
NEXT = (
    "SAME104 fresh qualifiedAndroidbf30cdead HOST acceptance: non-skipped RealContentTest/RareHanTest "
    "and actual production meaning-builder defaultN1/All/custom-pool choices, reverse/pairwise direct "
    "symmetric NONTRANSITIVE guards, finite semantic optionset acceptance. Explicitly adjudicate "
    "the retained LOW-RISK/unproved Claude hypotheses 劾/偵 and 弾劾/叱る against actual labels/options; "
    "GPT and coordinator established no direct ambiguity in supplied evidence, not universal safety. "
    "Two serial blind different-family INITIAL reviews complete on signed636b995; both ORIGINAL "
    "sessions confirmed sole English contrast/outcome clarification on signed089a60b2. All Japanese/"
    "metadata/readingorder/curation/guards/geometry and other runtime bytes unchanged. Full packet "
    "280103bytes/5163lines, FOURmember+23comparison=27completefamilies/15rawcharacters/33complete"
    "articlebodies/FOURpublictexts; each reviewer made exactlyONEserialview returning exact full packet "
    "without truncation/overlap. Confirmations same52296bytes/618lines, one exact serial view each. "
    "Byte return/self-report NOT equal comprehension, native-speaker or independent upstream retrieval. "
    "Minor wording defect resolved; GPT treated original as nonblocking clarity, not incorrect legal "
    "definition; preserve calibrated disagreement, original reports and four optional polish items. "
    "Full/selectedガイ gives keyがい/displayガイ; kunempty. ONEallmappedpair/TWOdirections/ZEROactivated"
    "pairs/ZERObaselineedits. THREEwrong刻効努/FIVEkanjiguards責詰査調究/SEVENwordguards "
    "批判批評評論責める攻撃叩く切る; no inferred wordlevel. 弾hasnoKANJIcard, plain component/fullmetadata; "
    "existing弾たま unchanged/notcompoundreuse. Actual28Han unchanged, 刂U+5202 absentallTHREEcmaps, "
    "NOTglyphfailure: actual刂fallback/readability in ALLfour selected/defaultfontmodes remains mandatory. "
    "Then productionContentSyncONCE/nativeN1/All/meaning/curatedreading/eightstrokeDrawing/article/Back/"
    "offline/fourfonts/rendered acceptance; fresh owneddevice/port, actual terminalcase0, unchanged2g/"
    "192mheap/oneworker, scopedcleanup. Qualified signedAPPbf30cdead approvedguard+schemaonly, NOT "
    "unrelatedlatestmain; compatibleAndroid#125+#132 required, oldclientsignore. Every original "
    "combinedcurrentmain/fullPython/vocabulary/baseline-membership-links/manifestbudget/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed"
    "80MiBinflated56MiBretained/perfilemediasafepaths/verifiedownerissue gate remains. "
    "Verify whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. "
    "Parent13320 ownsrunner.lock: no childacquire/delete/unlock/readprobe; approvedcontrol/committed"
    "source/frozeninputs only, not optional historicalsessionrecipes. Preserve/report/yield actual"
    "newdenial/signinghang/uncertainownership. No105/unreviewedpush/authoragents/concurrentheavywork/"
    "secondrunner/signingretry/guardincrease. Published130/1228,1098acceptance-remainder unchanged; "
    "draft1127kanji5078words includes unaccepted劾/one necessarysupport, NOT N1vocabulary. Six separately"
    "placed保案派第策結 retainN2/noacceptedcredit/noduplicate/relevel. Original103finite128optionset/"
    "native/rendered acceptance remains bounded as795;900x2000renditions NOToriginal1080x2400/"
    "equalcomprehension/fallbackface/retention certification; GPTcompletevisualcoverageUNVERIFIED; "
    "no new73image-loop/newblindcredit or unapproved stronger pixel guarantee. All original historical "
    "readdepth/image/process/permission/OOM/pending/source-only limitations preserved, not retroaccepted. "
    "Physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)


def common():
    assert r.git("log", "-1", "--format=%G?") == "G"
    assert r.git("rev-parse", "origin/main") == b.MAIN
    assert r.git("rev-parse", "HEAD", repo=A) == b.APP
    assert r.git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not r.git("status", "--porcelain", "--untracked-files=all", repo=A)
    runner = r.load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 13320, L.name)
    assert not r.absent(13320) and not r.load(L / "preflight-799.json")["lockTouched"]
    p = r.load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (798, "104", "continue")


def archive(path):
    target = path.with_name(path.name + ".gz")
    assert path.exists() and not target.exists(), path
    raw = path.read_bytes()
    target.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(target.read_bytes()) == raw
    receipt = {"rawName": path.name, "rawSha256": r.sha(path),
               "archive": target.name, "archiveSha256": r.sha(target), "losslessGzip": True}
    path.unlink()
    return receipt


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256 as manifest_sha256
    from audit_n1_batch import audit as batch_audit
    manifest = r.load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            path = R / name
            actual = r.sha(path) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else manifest_sha256(path)
            assert actual == digest, name
            count += 1
    assert count == 8466
    assert not r.git("diff", REVISED, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    result = batch_audit(R, "104")
    assert result["dictionaryFamilies"] == 27 and result["curatedOfferedKeys"] == 1
    assert result["requiredReciprocalPairs"] == 1
    return {"runtimeManifestHashesVerified": count, "contentVersion": manifest["contentVersion"],
            "runtimeUnchangedSinceBothConfirmations": True, "batchAudit": result}


def record():
    common()
    assert r.git("rev-parse", "HEAD") == REVISED
    initial = r.load(V / "batch-104-initial-reconciliation-799.json")
    confirmations = {}
    for label, model in r.MODELS.items():
        prefix = f"batch-104-confirmation-{label}"
        execution = r.load(V / (prefix + "-execution.json"))
        coverage = r.load(V / (prefix + "-coverage.json"))
        original = r.load(V / f"batch-104-initial-{label}-execution.json")
        assert execution["sessionId"] == original["sessionId"] and execution["snapshot"] == REVISED
        assert execution["actualModels"] == [model] and execution["usageCurrentModel"] == model
        assert execution["exitCode"] == 0 and r.absent(execution["launcherPid"])
        assert coverage["allAssignedRangesReturned"] and not execution["observedToolOverlaps"]
        assert not execution["unfinishedTools"] and execution["multiToolResponseCount"] == 0
        assert len(execution["toolCalls"]) == 1
        assert execution["toolCalls"][0]["exactRequestedTextContainedInResult"]
        assert not execution["toolCalls"][0]["truncationMarker"]
        assert r.sha(V / (prefix + ".md")) == execution["reportSha256"]
        assert r.sha(V / (prefix + ".jsonl")) == execution["rawExecutionSha256"]
        confirmations[label] = {key: execution[key] for key in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
            "snapshot", "reportSha256", "rawExecutionSha256"]}
        confirmations[label].update(
            report=prefix + ".md", coverage=prefix + "-coverage.json",
            fullPacketReturnedExactly=True, serialInternalToolCalls=True,
            losslessExecutionArchive=archive(V / (prefix + ".jsonl")))
    assert initial["initialExecutions"]["gpt"]["completedAt"] < confirmations["claude"]["startedAt"]
    assert confirmations["claude"]["completedAt"] < confirmations["gpt"]["startedAt"]
    finding = dict(initial["uniqueVerifiedUsefulInitialFinding"])
    finding.update(status="resolved", revisedTeachingSnapshot=REVISED, bothOriginalSessionsConfirmed=True,
                   finalDisposition="Claude confirms localized Minor clarity resolved; GPT accepts improvement but retains original nonblocking/no-proved-substantive-error assessment. No majority-vote or retroactive defect claim.")
    hypotheses = initial["hypotheses"]
    for row in hypotheses:
        row.update(status="unresolved",
                   consequence="Unproved low-risk pair hypothesis, NOT established textual defect; retain in qualified actual finite-optionset acceptance.",
                   originalReviewerDisposition="Claude retains hypothesis unresolved; GPT establishes no direct ambiguity. Coordinator reasoning in original reason field retained, not a purported reviewer withdrawal.")
    current = runtime()
    reconciliation = {
        "schemaVersion": 1, "batch": "104", "execution": 799, "status": STAGE,
        "originalTeachingSnapshot": INITIAL, "revisedTeachingSnapshot": REVISED,
        "initialExecutions": initial["initialExecutions"], "confirmations": confirmations,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 280103, "initialPacketLines": 5163,
        "confirmationPacketBytes": 52296, "confirmationPacketLines": 618,
        "completeFamiliesSupplied": 27, "rawCharacterRecordsSupplied": 15,
        "completeArticleBodies": 33, "newArticleBodies": 2, "changedReusedPassages": 0,
        "verdicts": {name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
                     for name in ["kanji/劾.md:1-47", "words/弾劾.md:1-38"]},
        "findings": [finding], "hypotheses": hypotheses, "optional": initial["optional"],
        "consequentialUnresolvedChangedTeachingClaims": [], "runtime": current,
        "matchedSampleContributions": {
            "shared": "No Japanese/reading/allocation/metadata/three-wrongchoice/directguard/link defect established; both accept current two articles textually.",
            "claudeUnique": "Minor outcome/antonym grouping clarity finding implemented and confirmed. Pair hypotheses and optional items retained, not credited as proved defects.",
            "gptUnique": "No unique proved defect; preserves bounded original CLEAN and no-retroactive-error assessment. Equivalent pair observations appear throughout report and are not unique Claude discoveries.",
            "limits": initial["modelComparisonLimits"],
        },
        "boundedEvidenceLimits": [
            "Actual one full exact returned initial packet and one full exact confirmation packet per reviewer; no internal/external overlap or truncation. Returned bytes do not prove equal comprehension or fresh sense-by-sense inspection.",
            "All upstream dictionary evidence supplied by coordinator from committed packets/archives. No independent upstream retrieval/Git/hash/font-cmap inspection by reviewers.",
            "Confirmations reread both complete revised new articles, four complete member families and exact archived character/compound dictionary blocks. Broader comparison families/articles carried forward from originals, not reread.",
            "Actual28Han/cmap inventory unchanged; native 刂 fallback/readability in ALLfourfonts/default remains mandatory. Cmap absence is not glyphfailure.",
            "No exhaustive future-pool semantics, native-speaker certification, actual drawing/renderedUI/physical-phone/general-release acceptance or measured learning-effectiveness claim.",
        ],
        "initialReviewsComplete": True, "bothOriginalSessionsConfirmed": True,
        "textualAcceptanceComplete": True, "fullBatchAcceptanceComplete": False, "reviewClosed": [],
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
    }
    r.save(V / "batch-104-reconciliation.json", reconciliation)
    ledger = r.load(S / "batch-104-progress.json")
    ledger.update(status=STAGE, nextAction=NEXT,
                  textualReview={"initialSnapshot": INITIAL, "revisedSnapshot": REVISED,
                                 "initialReviewsComplete": True, "bothOriginalSessionsConfirmed": True,
                                 "textualAcceptanceComplete": True, "fullBatchAcceptanceComplete": False,
                                 "reconciliation": "docs/n1-reviews/batch-104-reconciliation.json",
                                 "scopeLimits": reconciliation["boundedEvidenceLimits"]})
    ledger["limits"][0] = "Textual reviews and both original-session confirmations complete; full batch acceptance/publication still pending."
    ledger["limits"][3] = "Fresh non-skipped qualified Android, finite-option semantic, ContentSyncONCE/native/rendered/font acceptance and every publication gate remain."
    r.save(S / "batch-104-progress.json", ledger)
    packaging = [archive(V / name) for name in [
        "batch-104-cli-help-execution-799.txt", "batch-104-cli-config-help-execution-799.txt",
        "batch-104-confirmation-claude-task.txt", "batch-104-confirmation-gpt-task.txt"]]
    r.save(V / "batch-104-evidence-packaging-799.json", {
        "archives": packaging,
        "diagnostic": "Original staged exact CLI config capture had a trailing blank EOF line; initial freeze retained it as evidence. Final evidence archives original CLI and confirmation prompt bytes losslessly rather than modifying reviewer inputs or suppressing whitespace checks. No amendment or runtime change.",
    })
    r.save(S / "execution-799.json", {
        "schemaVersion": 1, "execution": 799, "checkpoint": 799, "batch": "104", "stage": STAGE,
        "startingState": r.load(C / "progress.json")["execution799StartingState"],
        "originalTeachingSnapshot": INITIAL, "revisedTeachingSnapshot": REVISED,
        "androidSignedHead": b.APP, "freshOriginMain": b.MAIN,
        "initialExecutions": initial["initialExecutions"], "confirmations": confirmations,
        "reconciliation": "docs/n1-reviews/batch-104-reconciliation.json",
        "validation": r.load(V / "batch-104-clarity-correction-audit-799.json"),
        "currentRuntime": current, "sourceTestsPassed": 43, "validatorErrors": 0,
        "initialReviewsComplete": True, "bothOriginalSessionsConfirmed": True,
        "textualAcceptanceComplete": True, "fullBatchAcceptanceComplete": False,
        "runtimeChangedThisExecution": True, "runtimePublished": False, "reviewClosed": [],
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 130, "remainingAdditions": 1098,
        "lastPublishedCommit": b.MAIN, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
    })
    shutil.copyfile(Path(__file__), V / "batch-104-finish-review-799.py")
    print("Both original sessions confirmed; calibrated reconciliation and pending runtime gates persisted.")


def signed_final():
    common()
    head = r.git("rev-parse", "HEAD")
    assert head != REVISED and r.git("rev-parse", "HEAD^") == REVISED
    assert not r.git("status", "--porcelain", "--untracked-files=all")
    changes = r.git("-c", "core.quotepath=false", "diff", "--name-only", REVISED, head).splitlines()
    assert all(n.startswith("docs/n1-reviews/batch-104-") or n in {
        "docs/n1-sources/batch-104-progress.json", "docs/n1-sources/execution-799.json"} for n in changes)
    current = runtime()
    assert current == r.load(S / "execution-799.json")["currentRuntime"]
    return head, current


def issue():
    head, current = signed_final()
    body = (
        "Batch104 / checkpoint799: **two independent textual reviews and both original-session "
        "confirmations complete; runtime/native/publication acceptance pending**.\n\n"
        f"Normally signed local evidence `{head}` preserves initial teaching `{INITIAL}` and revised "
        f"teaching `{REVISED}`. Claude Opus5.5 (`claude-opus-5.5`) and GPT-6.1 Sol (`gpt-6.1-sol`) "
        "ran serially, view-only, on the same280103-byte/5163-line blind packet: FOURmember+23comparison="
        "27complete JMdict families,15rawcharacters,33completearticlebodies,FOURarchivedpublictexts. "
        "Each made exactly ONE serial view returning the exact entire packet without truncation. "
        "Actual models and process exit before each following reviewer verified; complete original "
        "reports/model/session/process/read evidence retained. Byte return is not equal comprehension "
        "or independent upstream retrieval.\n\n"
        "**One minor clarity correction** at words/弾劾.md:30 separates praise as a contextual contrast "
        "from removal as a possible outcome of impeachment. Japanese/kana, titles, metadata, sole "
        "reading keyがい/displayガイ, guards, links, geometry and every other runtime payload are "
        "unchanged. Claude confirms the localized clarity finding resolved; GPT accepts the improvement "
        "but did not call the original a substantive error. Both ORIGINAL sessions confirmed the same "
        "signed revised tree using the identical52296-byte/618-line changed-passage packet, one exact "
        "serial view each. No consequential textual defect remains established; this is NOT native or "
        "full batch acceptance.\n\n"
        "Claude retains two **unproved low-risk hypotheses** (劾/偵, 弾劾/叱る); GPT and coordinator "
        "established no direct ambiguity from actual displayed labels/senses. Neither hypothesis is "
        "silently withdrawn or credited as a defect: explicit finite live-option adjudication remains "
        "mandatory. Four wording/mnemonic/display polish items remain optional. All five kanji/seven "
        "word guards remain direct, symmetric and nontransitive; three curated wrong choices unchanged.\n\n"
        f"43focusedsource tests, validation(0errors), batch/baseline/link audit, vocabulary consistency, "
        f"manifest freshness and budgets passed; all **{current['runtimeManifestHashesVerified']} runtime "
        f"manifest hashes** verified, contentVersion `{current['contentVersion']}`. Published count "
        "remains130/1228;1098acceptance remainder. Draft1127kanji/5078words includes ONEunaccepted "
        "kanji and ONEnecessary support, not N1vocabulary delivery. Actual28Han unchanged; "
        "**刂U+5202** absentallTHREEbundledcmaps is NOTglyphfailure; four-mode native fallback/readability "
        "and eightstroke drawing remain mandatory.\n\n"
        "Next SAME104: fresh non-skipped qualified Android tests, actual N1/All/custom builder/pair/"
        "finite-optionset checks, then ContentSyncONCE/native/rendered/fourfont and all original "
        "combined-current-main/full-suite/signing/ownerfastforward/terminalCI/EVERYimmutableZIPhash/"
        "unchanged18000entries42MiBcompressed80MiBinflated56MiBretained gates before publication or105. "
        "Qualified signed Android `bf30cdead8515739bc0e671d57a54b9a3109dd46` remains approved guard+"
        "schema-only, NOT unrelated latestmain. Compatible stop-cran/kanji-cards-android#125 and "
        "stop-cran/kanji-cards-android#132 required; oldclientsignore. Parent launcher/session verified, "
        "lock untouched; only approved control/committed/frozen inputs used; no new denial. Historical "
        "process/image/read-depth/permission/OOM/source-only limits unchanged. No push, new batch or "
        "second runner. Physicalphone/generalrelease/whole-set outstanding; project incomplete.\n"
    )
    assert not (C / "issue-request-799.json").exists()
    r.save(C / "issue-request-799.json", {"body": body})
    (C / "issue-799.txt").write_text(body, encoding="utf-8")
    print("Generated exact owner issue update.")


def finish():
    head, current = signed_final()
    posted = r.load(L / "issue-799-verified.json")
    body = r.load(C / "issue-request-799.json")["body"]
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body and head in body
    before = r.load(L / "progress-before-799.json")
    p = r.load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    receipt = {
        "schemaVersion": 1, "execution": 799, "checkpoint": 799, "batch": "104",
        "savedCommit": head, "signature": "G", "originalTeachingSnapshot": INITIAL,
        "revisedTeachingSnapshot": REVISED, "androidSignedHead": b.APP,
        "evidence": "docs/n1-sources/execution-799.json",
        "reconciliation": "docs/n1-reviews/batch-104-reconciliation.json",
        "initialReviewsComplete": True, "bothOriginalSessionsConfirmed": True,
        "textualAcceptanceComplete": True, "fullBatchAcceptanceComplete": False,
        "runtimeDrafted": ["劾"], "reviewClosed": [], "published": [],
        "runtimePublished": False, "runtimeChangedThisExecution": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 130, "remainingAdditions": 1098,
        "lastPublishedCommit": b.MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "runtime": current, "sourceTestsPassed": 43,
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue", "stage": STAGE,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
    }
    p["execution799StartingState"]["status"] = "textual-review-checkpoint-complete"
    p["execution799CoordinatorCheckpoint"] = receipt
    p["batch104TextualReviewIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": __import__("hashlib").sha256(body.encode("utf-8")).hexdigest(), "verified": True}
    p.update(checkpoint=799, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    b.atomic(C / "progress.json", p)
    reread = r.load(C / "progress.json")
    assert reread == p and all(reread[k] == v for k, v in before.items() if k not in mutable)
    r.save(L / "checkpoint-799-final-verification.json", receipt)
    print(json.dumps({"checkpoint": 799, "status": "continue", "savedCommit": head,
                      "historicalRootKeysPreserved": len(before), "issueUpdate": posted["html_url"],
                      "runtimePublished": False, "textualAcceptanceComplete": True}))


if __name__ == "__main__":
    {"record": record, "issue": issue, "finish": finish}[sys.argv[1]]()
