"""Seal evidence, then save an atomic full-history continuation after signing."""
import base64
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "1b433be5-2dc7-4b81-b332-57694a5f3bd0"
D = R / "docs" / "n1-reviews" / "batch-103-rendered-793"
E = R / "docs" / "n1-sources" / "execution-793.json"
BASE = "ba8917b6d35e044bf96d059beb44a7bd7392f2de"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, repo=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(repo), *args],
                                   encoding="utf-8").strip()


def verify_runtime():
    manifest = load(R / "manifest.json")
    assert manifest["contentVersion"] == "38c32a8df5fd6063"
    count = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        for name, digest in entries.items():
            raw = (R / Path(*name.split("/"))).read_bytes()
            normalized = raw if binary else raw.replace(b"\r\n", b"\n")
            assert sha(normalized) == digest, name
            count += 1
    assert count == 8463
    assert not git("diff", BASE, "--", "manifest.json", "kanji", "words", "strokes", "articles", "tools")
    return count


def seal():
    assert git("rev-parse", "HEAD") == BASE
    report = D / "gpt-transport.md"
    original = report.read_bytes()
    assert original == (C / "batch-103-rendered-793" / report.name).read_bytes()
    archive = D / "gpt-transport.md.gz"
    assert not archive.exists()
    archive.write_bytes(gzip.compress(original, compresslevel=9, mtime=0))
    assert gzip.decompress(archive.read_bytes()) == original
    report.unlink()
    for row in load(D / "archive-integrity.json"):
        packed = D / row["archive"]
        assert sha(packed.read_bytes()) == row["archiveSha256"]
        restored = gzip.decompress(packed.read_bytes())
        if "factoredSha256" in row:
            assert sha(restored) == row["factoredSha256"]
            for payload in load(D / "image-payload-index.json"):
                image = (D / payload["file"]).read_bytes()
                assert sha(image) == payload["sha256"]
                marker = ("__N1_IMAGE_PAYLOAD_SHA256_" + payload["sha256"] + "__").encode("ascii")
                restored = restored.replace(marker, base64.b64encode(image))
        assert len(restored) == row["rawBytes"] and sha(restored) == row["rawSha256"]
    count = verify_runtime()
    e = load(E)
    e["validation"]["runtimeHashesVerified"] = count
    e["reportPackaging"] = {
        "archive": "gpt-transport.md.gz", "archiveSha256": sha(archive.read_bytes()),
        "originalSha256": sha(original), "originalBytes": len(original),
        "reason": "Preserve original Markdown hard-break spaces exactly without staged whitespace errors; no report trimming or rewriting.",
    }
    save(E, e)
    shutil.copyfile(Path(__file__), D / "checkpoint-recipe.py")
    print("All8463 runtime hashes and exact raw execution reconstruction verified; original report losslessly retained.")


def finish():
    before = load(L / "progress-before-793.json")
    current = load(C / "progress.json")
    assert all(current[k] == v for k, v in before.items())
    assert set(current) == set(before) | {"execution793StartingState"}
    assert (current["checkpoint"], current["batch"], current["status"]) == (792, "103", "continue")
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD", repo=A) == APP and git("log", "-1", "--format=%G?", repo=A) == "G"
    for repo in [R, A]:
        assert not git("status", "--porcelain", "--untracked-files=all", repo=repo)
    assert not git("diff", BASE, head, "--", "kanji", "words", "strokes", "articles", "tools", "manifest.json")
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert all(p.startswith("docs/n1-reviews/batch-103-rendered-793/") or
               p == "docs/n1-sources/execution-793.json" for p in changed)
    assert git("rev-parse", "origin/main") == before["lastPublishedCommit"]
    role = load(L / "preflight-793-before-issue.json")
    assert role["contentHead"] == head and not role["lockTouched"]
    count = verify_runtime()
    posted = load(L / "issue-793-posted.json")
    reread = load(L / "issue-793-reread.json")
    body = (C / "batch-103-rendered-793-issue-body.txt").read_bytes()
    assert posted["author"] == reread["user"]["login"] == "stop-cran"
    assert posted["bodySha256"] == sha(body) and body.decode("utf-8") == reread["body"]
    assert posted["url"] == reread["html_url"]
    e = load(E)
    next_action = (
        f"SAME103 checkpoint793 signed LOCAL rendered-review evidence HEAD{head}, qualifiedAndroid{APP}. "
        "Read docs/n1-sources/execution-793.json and docs/n1-reviews/batch-103-rendered-793/. "
        "TWO original-session dependent rendered confirmations completed SERIAL: ClaudeOpus5.5 "
        "eb1a8995-1568-4cd5-b7bb-0a1056233592 then GPT6.1Sol93b54be3-157e-4b13-a32c-e48e9f51c8d8; "
        "then serial own-report delivery clarifications. AllFOURprocesses terminal0/actualmodels verified/"
        "exited, ONEtoolperresponse/nooverlap; frozen signed teaching08e76c16 UNCHANGED. "
        "Both exact9resource text ranges returned;333completefamilies46rawcharacters120articlebodies39labels/"
        "64HOST+64nativechoices/liveN1default inherited from792. Both retain text and finite128sampledsets+"
        "livedefault semanticsCLEAN; no consequential content fix established. "
        "Actual image audit IMPORTANT: originals1080x2400; CLIview automatically delivered900x2000, NOT"
        "originalpixels. Coordinator requested originalfiles/norescaledsubstitutes. Claude73successful"
        "responses/73paths; GPT125successfulresponses/73paths/52repeats, NOT52failedreads. ONEGPT"
        "sessionwarning removed25images from modelrequest to meet50-image limit; compaction/pruning "
        "prevents independent reconstruction of uninterrupted image retention. GPTown clarification "
        "corrects ModerateREPORTINGdefect; Claude withdraws unsupportedword2-13largercaptureclaim. "
        "Both retain delivered-scale47Han/fourfonts/readings/drawing/route legibilityCLEAN. Fullresolution"
        "original/nativepixels/equalcomprehension/GPTindependentlyreconstructablecompletevisualretention "
        "remainUNVERIFIED; do NOT imply complete native-pixel acceptance. Originalreports+corrections "
        "preserved verbatim, GPTtransport.md losslesslygzipped to retain originalhardbreakspaces. "
        "Rawexecutions losslessly factored: 33actualreturnedPNGpayloads +factoredJSONL reconstruct EVERY"
        "originalstdoutBYTE/hash exactly; noevents omitted, originalrawstdout remainscontrol. Actual"
        "900x2000payloads are archival deliveryevidence NOT replacement nativefiles/newreviews. "
        "NEXT SAME103 bounded FINAL ACCEPTANCE RECONCILIATION of originalreports/transportclarifications/"
        "per-call coverage and inheritednative791; establish honest bounded rendered disposition before "
        "batchacceptance. NO repeatedall73readloop/newblindinitialcredit. No new consequential glyph/text"
        "failure established; do not manufacture one merely from scaling or silently certify unreadpixels. "
        "No final rendered/fullbatch acceptance or publication claimed793. Only after no consequential"
        "unresolvedin-scopeclaim remains: ALLrequired combinedcurrentmain/nonrewritingmerge/"
        "changedteachingreview/Python/vocabulary/baseline/link/membership/manifest/budget/appchecks/"
        "normal signing/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/18000entries"
        "42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia/verifiedownerissue beforedelivery. "
        "All originalgates retained in historicalExecution792Before793Rendered.nextAction and fullhistory. "
        "No native/JVMrerun merelyforunchangedbytes/no104/unreviewedpush/secondrunner/concurrentheavywork. "
        "Validator0errors/manifestunchanged/runtime8463hashes version38c32a8df5fd6063/normalsignatureG/"
        "bothworktreesclean. Parent13320ownsrunner.lock/nochildacquire/delete/unlock/readprobe; "
        "freshliveparentancestry/decodedlauncher/exactsession/checkpoint/signedheads/whollyclean/fetchedmain "
        "required next. Approvedcontrol/committedsources/frozeninputs only; nooptionalhistoricalhelpers/"
        "newpermissiondenial. Execution792denial retained/causeunknown/parentrecovery honored, no retry"
        "orbypass. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. QualifiedAndroid"
        "approvedpairguard+schemaonly, NOTlatestappmain. Published129/1228/remainder1099unchanged;"
        "sixearlierN2placementsseparate;compatibleAndroid#125+#132required;oldclientsignorecuration/guards. "
        "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete."
    )
    checkpoint = {
        "schemaVersion": 1, "execution": 793, "checkpoint": 793, "batch": "103",
        "status": "continue", "stage": "batch-103-original-family-rendered-confirmations-preserved-awaiting-final-acceptance-reconciliation",
        "savedCommit": head, "signature": "G", "qualifiedAndroidHead": APP,
        "evidence": "docs/n1-sources/execution-793.json", "issueUpdate": posted["url"],
        "ownerIssueAuthorAndExactBodyVerified": True,
        "originalSessionConfirmationsExecuted": 2, "deliveryScopeClarificationsExecuted": 2,
        "allFourReviewerProcessesExited": True, "actualModels": e["actualModels"],
        "toolsAndProcessesSerial": True, "bothAssignedTextRangesReturnedExactly": True,
        "ordinarySenseFallbackSemanticAcceptance": e["ordinarySenseFallbackSemanticAcceptance"],
        "independentRenderedReviewClosed": False,
        "boundedDeliveredRenditionReviewVerdict": e["boundedDeliveredRenditionReviewVerdict"],
        "originalPixelAndEqualComprehensionAcceptance": "UNVERIFIED",
        "gptEveryRequestRetentionAndIndependentlyReconstructableVisualCoverage": "UNVERIFIED",
        "fullBatchAcceptanceComplete": False, "runtimeAccepted": False, "runtimePublished": False,
        "runtimeChanged": False, "manifestChanged": False, "freshNativeExecuted": False,
        "reviewClosed": [], "published": [], "nextBatchStarted": False,
        "runtimeHashesVerified": count, "contentVersion": "38c32a8df5fd6063",
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 129, "remainingAdditions": 1099,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": next_action, "blocker": None,
        "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
    }
    updated = copy.deepcopy(current)
    assert "execution793CoordinatorCheckpoint" not in updated
    assert "historicalExecution792Before793Rendered" not in updated
    updated["historicalExecution792Before793Rendered"] = {
        k: copy.deepcopy(before[k]) for k in ["checkpoint", "status", "stage", "batch", "nextAction", "blocker"]
    }
    updated["execution793CoordinatorCheckpoint"] = checkpoint
    updated["execution793StartingState"]["status"] = "signed-local-review-and-delivery-scope-checkpoint-complete"
    root_changes = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for k in root_changes:
        updated[k] = checkpoint[k]
    for k, v in before.items():
        if k not in root_changes:
            assert updated[k] == v, k
    temp = C / "progress.json.793-finish.tmp"
    assert not temp.exists()
    save(temp, updated)
    assert load(C / "progress.json") == current
    os.replace(temp, C / "progress.json")
    assert load(C / "progress.json") == updated
    save(L / "checkpoint-793-summary.json", checkpoint)
    save(L / "checkpoint-793-final-verification.json", {
        "checkpoint": 793, "head": head, "signature": "G", "bothWorktreesClean": True,
        "runtimeHashesVerified": count, "allOriginalHistoricalValuesPreserved": True,
        "historicalRootKeysCompared": len(before), "ownerIssueAuthorAndExactBodyVerified": True,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
    })
    print(f"Checkpoint793 durably saved at signed{head}; all{len(before)} historical roots preserved.")


{"seal": seal, "finish": finish}[sys.argv[1]]()
