"""Reconcile batch 103 evidence without replaying reviewers or native tests."""
import base64
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "3c20e297-aae7-4653-9b55-0bd5bb918848"
D = R / "docs" / "n1-reviews" / "batch-103-reconciliation-794"
REV = R / "docs" / "n1-reviews" / "batch-103-rendered-793"
NATIVE = R / "docs" / "n1-reviews" / "batch-103-native-791"
BASE = "25fa6be700a42368427b93e13a8270dca8fbc7da"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, repo=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(repo), *args], encoding="utf-8"
    ).strip()


def runtime():
    m = load(R / "manifest.json")
    assert m["contentVersion"] == "38c32a8df5fd6063"
    count = 0
    for section, entries in m.items():
        if not isinstance(entries, dict):
            continue
        binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        for name, digest in entries.items():
            raw = (R / Path(*name.split("/"))).read_bytes()
            assert sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest, name
            count += 1
    assert count == 8463
    assert not git("diff", BASE, "--", "manifest.json", "kanji", "words", "strokes", "articles", "tools")
    return count


def start():
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (793, "103", "continue")
    assert git("rev-parse", "HEAD") == BASE
    assert git("rev-parse", "origin/main") == p["lastPublishedCommit"]
    assert not (L / "progress-before-794.json").exists()
    save(L / "progress-before-794.json", p)
    request = (L / "request.txt").read_bytes()
    s = request.decode("utf-8-sig")
    label = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    parsed, end = json.JSONDecoder().raw_decode(s.split(label, 1)[1].lstrip())
    assert parsed["checkpoint"] == 793
    state = {
        "execution": 794, "batch": "103", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": BASE, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME103 final bounded source/rendered/native reconciliation and fresh content acceptance checks; signed LOCAL evidence checkpoint. No reviewer/native/JVM rerun, publication or104.",
        "request": {
            "sha256": sha(request), "bytes": len(request), "characters": len(s),
            "lines": len(s.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint decoded; operative contract, complete issue and final checkpoint directly inspected. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerPreflight": load(L / "preflight-794.json"),
        "artifactPathPreflight": "Approved committed packets and workspace control only; no optional historical-session helpers accessed.",
        "runtimeHashesVerified": runtime(), "status": "acceptance-reconciliation-in-progress",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-794.json", state)
    updated = copy.deepcopy(p)
    assert "execution794StartingState" not in updated
    updated["execution794StartingState"] = state
    tmp = C / "progress.json.794-start.tmp"
    assert not tmp.exists()
    save(tmp, updated)
    assert load(C / "progress.json") == p
    os.replace(tmp, C / "progress.json")
    assert load(C / "progress.json") == updated
    print("Starting scope saved; complete historical checkpoint preserved.")


def audit():
    assert git("rev-parse", "HEAD") == BASE
    D.mkdir(exist_ok=False)
    native_index = load(NATIVE / "artifact-index.json")
    native_pngs = []
    for row in native_index:
        p = NATIVE / Path(*row["file"].split("/"))
        raw = p.read_bytes()
        assert sha(raw) == row["storedSha256"], p
        restored = gzip.decompress(raw) if p.suffix == ".gz" else raw
        assert len(restored) == row["sourceBytes"] and sha(restored) == row["sourceSha256"]
        if p.suffix == ".png":
            assert struct.unpack(">II", raw[16:24]) == (1080, 2400)
            native_pngs.append({"file": row["file"], "sha256": sha(raw)})
    assert len(native_pngs) == 73
    payloads = {}
    for row in load(REV / "image-payload-index.json"):
        raw = (REV / Path(*row["file"].split("/"))).read_bytes()
        assert sha(raw) == row["sha256"]
        assert struct.unpack(">II", raw[16:24]) == (900, 2000)
        payloads[row["sha256"]] = base64.b64encode(raw)
    restored_archives = []
    for row in load(REV / "archive-integrity.json"):
        raw = (REV / row["archive"]).read_bytes()
        assert sha(raw) == row["archiveSha256"]
        restored = gzip.decompress(raw)
        if "factoredSha256" in row:
            assert sha(restored) == row["factoredSha256"]
            restored = re.sub(
                rb"__N1_IMAGE_PAYLOAD_SHA256_([0-9a-f]{64})__",
                lambda m: payloads[m[1].decode("ascii")], restored
            )
        assert len(restored) == row["rawBytes"] and sha(restored) == row["rawSha256"]
        restored_archives.append({"archive": row["archive"], "exactRawBytesVerified": len(restored)})
    processes = load(REV / "process-order.json")
    for i, row in enumerate(processes):
        assert row["exitCode"] == 0 and row["processExited"]
        assert row["actualModels"] == [row["requestedModel"]]
        if i:
            assert processes[i - 1]["completedAt"] < row["startedAt"]
    save(D / "integrity-audit.json", {
        "nativeArtifactsVerified": len(native_index), "originalPngs": native_pngs,
        "originalDimensions": [1080, 2400], "actualDeliveredPayloads": len(payloads),
        "deliveredDimensions": [900, 2000], "restoredArchives": restored_archives,
        "fourProcessesSerialAndExited": True, "actualModelsVerified": True,
        "runtimeHashesVerified": runtime(),
        "limits": "Byte verification is not visual inspection or proof of model-request image retention.",
    })
    print("Native artifact hashes, transport payloads and exact archived stdout reconstruction verified.")


def seal():
    assert git("rev-parse", "HEAD") == BASE
    expected_names = {Path(row["file"]).name for row in load(D / "integrity-audit.json")["originalPngs"]}
    coverage = {}
    for who, count in [("claude", 73), ("gpt", 125)]:
        e = load(REV / f"{who}-execution.json")
        assert e["availableTools"] == ["view"] and e["exitCode"] == 0 and e["processExited"]
        assert not e["observedToolOverlaps"] and not e["unfinishedTools"] and not e["multiToolResponseCount"]
        assert e["allAssignedTextReturned"] and not e["missingImages"]
        assert sha((REV / f"{who}.md").read_bytes()) == e["reportSha256"]
        image_calls = [c for c in e["toolCalls"] if c.get("imagePayloads")]
        assert len(image_calls) == count
        mapped = {}
        for call in image_calls:
            assert call["success"]
            path = Path(call["arguments"]["path"]).name
            assert path in expected_names
            row = mapped.setdefault(path, {"successfulReturns": 0, "deliveredPayloadHashes": []})
            row["successfulReturns"] += 1
            for image in call["imagePayloads"]:
                assert image["pngDimensions"] == [900, 2000]
                assert image["originalPngDimensions"] == [1080, 2400]
                assert image["equalsOriginalBytes"] is False
                if image["sha256"] not in row["deliveredPayloadHashes"]:
                    row["deliveredPayloadHashes"].append(image["sha256"])
        assert set(mapped) == expected_names
        coverage[who] = {
            "model": e["requestedModel"], "session": e["sessionId"],
            "textCoverage": e["textCoverage"], "successfulImageReturns": count,
            "distinctRequestedPaths": len(mapped), "repeatedPathReturns": count - len(mapped),
            "perPath": mapped, "toolsSerial": True,
            "independentlyReconstructableCompleteVisualRetention": "UNVERIFIED",
            "originalPixelDelivery": False,
        }
    save(D / "per-path-delivery-audit.json", coverage)
    route = json.loads(gzip.decompress((NATIVE / "native" / "n1-103-article-route.json.gz").read_bytes()))
    raster = json.loads(gzip.decompress((NATIVE / "native" / "n1-103-font-raster.json.gz").read_bytes()))
    terminal = gzip.decompress((NATIVE / "native" / "instrumentation.txt.gz").read_bytes()).decode()
    assert terminal.count("INSTRUMENTATION_STATUS_CODE: 0") == 2 and "OK (2 tests)" in terminal
    assert route["passed"] and route["archiveRequests"] == 1 and route["problems"] == 0
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"]) == (1126, 5077, 135)
    assert len(route["productionBuilderN1AndAllExactChoices"]) == 64
    assert route["twoCuratedKeysPersistedGoodAndDone"] and route["offline"]
    assert route["mappedReciprocalPairs"] == 3 and route["directedLinkTransitions"] == 6
    glyphs = [row for row in raster["rows"] if "character" in row]
    words = [row for row in raster["rows"] if "word" in row]
    assert len(glyphs) == raster["individualGlyphProbes"] == 188
    assert all(row["hasGlyph"] for row in glyphs)
    assert len(words) == raster["wholeWordRasterProbes"] == 12
    assert all(row["renderedCharactersNonblank"] == len(row["word"]) for row in words)
    assert {row["font"] for row in glyphs} == {"Gothic", "Mincho", "Textbook", "Brush"}
    assert len({row["character"] for row in glyphs}) == 47
    assert len([row for row in glyphs if row["character"] == "厂"]) == 4
    save(D / "inherited-native-audit.json", {
        "execution": 791, "freshNativeExecuted": False, "terminalSuccessCases": 2,
        "productionArchiveRequests": 1, "productionChoices": 64,
        "scopedHan": 47, "fourFontHasGlyphProbes": 188,
        "explicitCliffFallbackProbes": 4,
        "importedCounts": {"kanji": 1126, "words": 5077, "n1": 135, "problems": 0},
        "twoCuratedKeysPersistedGoodAndDone": True, "directedReciprocalTransitions": 6,
        "offline": True, "limits": "Inherited actual execution; glyph probes are not comprehension or original-pixel visual inspection.",
    })
    checks = {}
    for name in ["validate", "manifest", "manifest-diff", "tests", "batch-audit", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{name}-794.txt").read_bytes()
        packed = gzip.compress(raw, compresslevel=9, mtime=0)
        p = D / f"{name}.txt.gz"
        assert not p.exists()
        p.write_bytes(packed)
        checks[name] = {"archive": p.name, "rawSha256": sha(raw), "archiveSha256": sha(packed)}
    assert "Ran 377 tests" in (L / "tests-794.txt").read_text(encoding="utf-8-sig")
    assert "0 error(s)" in (L / "validate-794.txt").read_text(encoding="utf-8-sig")
    batch_audit = json.loads((L / "batch-audit-794.txt").read_text(encoding="utf-8-sig"))
    assert batch_audit["exactBaseRuntimePreservedOutsideRecordedChanges"]
    assert batch_audit["requiredReciprocalPairs"] == 3 and batch_audit["readingDispositions"] == 3
    assert batch_audit["curatedOfferedKeys"] == 2
    assert git("merge-base", "HEAD", "origin/main") == git("rev-parse", "origin/main")
    assert not git("diff", "08e76c1688ada4898a79e25e13650687dadf65d1", "--",
                   "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    e = {
        "schemaVersion": 1, "execution": 794, "batch": "103",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "stage": "bounded-rendered-native-reconciliation-closed-publication-pending",
        "startingState": load(L / "starting-state-794.json"),
        "sourceSnapshot": BASE, "teachingSnapshot": "08e76c1688ada4898a79e25e13650687dadf65d1",
        "qualifiedAndroidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "mainAlreadyAncestor": True, "integrationMergeNecessaryAtCheck": False,
        "evidenceDirectory": str(D.relative_to(R)).replace("\\", "/"),
        "reconciliation": str((D / "disposition.json").relative_to(R)).replace("\\", "/"),
        "checks": checks, "pythonTests": 377, "validatorErrors": 0,
        "batchAudit": batch_audit, "runtimeHashesVerified": runtime(),
        "contentVersion": "38c32a8df5fd6063", "manifestChanged": False,
        "independentRenderedReviewClosed": True,
        "independentRenderedReviewClosedScope": "Delivered900x2000 rendition only; original-pixel approval and complete retained-context inspection UNVERIFIED.",
        "nativeRouteExecutionAccepted": True, "nativeEvidenceExecution": 791,
        "nonSkippedHostAcceptanceInheritedFrom": 789,
        "newReviewerProcesses": 0, "freshNativeOrJvmExecuted": False,
        "fullBatchAcceptanceComplete": False, "runtimeAcceptedForPublication": False,
        "runtimeChanged": False, "runtimePublished": False, "reviewClosed": [], "published": [],
        "publishedAdditions": 129, "remainingAdditions": 1099,
        "lastPublishedCommit": git("rev-parse", "origin/main"),
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "nextAction": "SAME103 reviewed acceptance/publication ledger reconciliation, then fresh-current-main gate and normal signed owner fast-forward publication. Reuse unchanged789 HOST and791 native evidence; do not rerun merely for unchanged bytes. If main changes runtime, nonrewriting merge/regenerate/revalidate and independently confirm changed teaching. Require terminal green CI and every exact immutable GitHub ZIP runtime hash/budget/path/media check, verified owner issue and durable full-history checkpoint before counting delivery or104. No new blind review or all73-image loop; bounded delivered-scale approval is NOT original/native-pixel/equal-comprehension/retention certification. All prior gates and historical denials remain intact.",
    }
    save(R / "docs" / "n1-sources" / "execution-794.json", e)
    for source, target in [
        (Path(__file__), D / "checkpoint-recipe.py"),
        (C / "preflight-794.ps1", D / "preflight-recipe.ps1.txt"),
        (C / "checks-794.ps1", D / "checks-recipe.ps1.txt"),
        (L / "preflight-794.json", D / "runner-preflight.json"),
    ]:
        target.write_bytes(source.read_bytes())
    print("Bounded rendering/native reconciliation and fresh377-test acceptance evidence sealed.")


def finish():
    before = load(L / "progress-before-794.json")
    current = load(C / "progress.json")
    assert set(current) == set(before) | {"execution794StartingState"}
    assert all(current[k] == v for k, v in before.items())
    assert (current["checkpoint"], current["batch"], current["status"]) == (793, "103", "continue")
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD", repo=A) == APP and git("log", "-1", "--format=%G?", repo=A) == "G"
    for repo in [R, A]:
        assert not git("status", "--porcelain", "--untracked-files=all", repo=repo)
    paths = git("diff", "--name-only", BASE, head).splitlines()
    assert paths and all(p.startswith("docs/n1-reviews/batch-103-reconciliation-794/") or
                         p == "docs/n1-sources/execution-794.json" for p in paths)
    assert git("rev-parse", "origin/main") == before["lastPublishedCommit"]
    role = load(L / "preflight-794-before-issue.json")
    assert role["contentHead"] == head and not role["lockTouched"]
    count = runtime()
    posted = load(L / "issue-794-posted.json")
    reread = load(L / "issue-794-reread.json")
    body = (C / "batch-103-reconciliation-794-issue-body.txt").read_bytes()
    assert posted["author"] == reread["user"]["login"] == "stop-cran"
    assert posted["bodySha256"] == sha(body) and body.decode("utf-8") == reread["body"]
    assert posted["url"] == reread["html_url"]
    e = load(R / "docs" / "n1-sources" / "execution-794.json")
    next_action = (
        f"SAME103 checkpoint794 signed LOCAL bounded-acceptance evidence HEAD{head}, qualifiedAndroid{APP}. "
        "Read docs/n1-sources/execution-794.json and docs/n1-reviews/batch-103-reconciliation-794/disposition.json. "
        "FINAL BOUNDED RECONCILIATION COMPLETE: initial788 two-family text/changed-passage confirmations; "
        "789 non-skipped RealContent3/RareHan1+production builder;791 TWOterminalnativecase0/ContentSyncONCE/"
        "1126kanji5077words135N1zeroissues/twoofferedkeys/sixlinkdirections/drawing/Back/offline;793 original-family "
        "rendered+transport clarifications reconciled. Rendering gate CLOSED ONLY for delivered900x2000renditions "
        "of1080x2400captures;47Han/fourfonts/actual厂 distinguishability and reading/drawing/route textCLEAN. "
        "Originalpixels/equalcomprehension/fallbackface/everyrequestretention/GPTindependentlyreconstructable"
        "completevisualcoverage remainUNVERIFIED; no claim promoted, no actual glyph/textfailure established. "
        "No more all73image-loop/newblindcredit or requirement for unapproved stronger pixel/retention guarantees. "
        "Finite128exactHOST/nativeoptionsets+livedefaultCLEANonly; unrestrictedpoolUNVERIFIED. "
        "All original reports/clarifications unchanged; original GPT52failedreads accounting corrected to125"
        "successfulreturns73paths52repeats/ONEwarning25prunedimages; Claude larger-captureclaimwithdrawn. "
        "794 exact nativeartifact hashes and lossless originalstdout reconstruction freshly verified; per-path "
        "delivery audit retained without claiming comprehension. Fresh377Python testsPASS/validator0errors/"
        "vocabularypilot2122of2431/batchbaseline-membership-reading-three-mappedpairs-sixdirections/"
        "manifestfresh8463hashes version38c32a8df5fd6063/budgets8485entries30308245localZIPbytes44674131inflated"
        "44405793retained PASS. originmain fresha38f4cf alreadyancestor; NOmergedruntimechange, no app/native/JVM"
        "rerun merelyforunchangedbytes. NEXT SAME103 actionable PUBLICATION checkpoint: reconcile "
        "review-closed source-row/inventory/batch acceptance ledgers and normally sign reviewed acceptance"
        "record, freshfetch/nonrewritingmerge if needed/regenerate/revalidate actualcombinedtree/independently"
        "confirmchangedteaching, ownernormalfastforwardpush, terminalgreenrelevantCI and EVERY immutable"
        "GitHubZIP runtimeentryhash/18000entries42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia "
        "checks, verifiedownerissue and fullhistorycheckpoint. Do not count local acceptance as delivery. "
        "No104 until publicacceptance. All existing publication gates preserved, no unreviewedpush/"
        "signingretry/guardincrease. Freshliveparentancestry/decodedlauncher/exactsession/checkpoint/"
        "clean signedheads/fetchedmain preflight; parent13320holdsrunner.lock, nochildacquire/delete/unlock/"
        "readprobe. Approvedcommittedsources/control/frozeninputs only, nooptionalhistoricalhelpers. "
        "Preserve/report/yield actualnewdenial/signinghang/uncertainownership; original792denial/causeunknown/"
        "parentrecovery retained. Published129of1228/remainder1099unchanged; sixseparateN2placementsnot"
        "counted, no relevel/duplicate. CompatibleAndroid#125+#132required;oldclientsignorecuration/guards. "
        "Qualifiedbf30 approvedpairguard+schemaonly, NOTlatestappmain. Physicalphone/generalrelease/whole-set"
        "outstanding;projectincomplete."
    )
    checkpoint = {
        "schemaVersion": 1, "execution": 794, "checkpoint": 794, "batch": "103",
        "status": "continue", "stage": "batch-103-bounded-acceptance-reconciled-publication-pending",
        "savedCommit": head, "signature": "G", "qualifiedAndroidHead": APP,
        "evidence": "docs/n1-sources/execution-794.json", "issueUpdate": posted["url"],
        "ownerIssueAuthorAndExactBodyVerified": True,
        "independentRenderedReviewClosed": True,
        "independentRenderedReviewClosedScope": e["independentRenderedReviewClosedScope"],
        "originalPixelAndEqualComprehensionAcceptance": "UNVERIFIED",
        "gptEveryRequestRetentionAndIndependentlyReconstructableVisualCoverage": "UNVERIFIED",
        "nativeRouteExecutionAccepted": True, "nativeEvidenceExecution": 791,
        "pythonTests": 377, "validatorErrors": 0, "manifestChanged": False,
        "runtimeHashesVerified": count, "contentVersion": "38c32a8df5fd6063",
        "fullBatchAcceptanceComplete": False, "runtimeAcceptedForPublication": False,
        "runtimeChanged": False, "runtimePublished": False, "reviewClosed": [], "published": [],
        "freshNativeOrJvmExecuted": False, "newReviewerProcesses": 0, "nextBatchStarted": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 129, "remainingAdditions": 1099,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": next_action, "blocker": None,
        "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
    }
    updated = copy.deepcopy(current)
    assert "execution794CoordinatorCheckpoint" not in updated
    assert "historicalExecution793Before794Reconciliation" not in updated
    updated["historicalExecution793Before794Reconciliation"] = {
        k: copy.deepcopy(before[k]) for k in ["checkpoint", "status", "stage", "batch", "nextAction", "blocker"]
    }
    updated["execution794CoordinatorCheckpoint"] = checkpoint
    updated["execution794StartingState"]["status"] = "signed-local-bounded-reconciliation-complete"
    root_changes = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for k in root_changes:
        updated[k] = checkpoint[k]
    for k, value in before.items():
        if k not in root_changes:
            assert updated[k] == value, k
    temp = C / "progress.json.794-finish.tmp"
    assert not temp.exists()
    save(temp, updated)
    assert load(C / "progress.json") == current
    os.replace(temp, C / "progress.json")
    assert load(C / "progress.json") == updated
    save(L / "checkpoint-794-summary.json", checkpoint)
    save(L / "checkpoint-794-final-verification.json", {
        "checkpoint": 794, "head": head, "signature": "G", "bothWorktreesClean": True,
        "runtimeHashesVerified": count, "allOriginalHistoricalValuesPreserved": True,
        "historicalRootKeysCompared": len(before), "ownerIssueAuthorAndExactBodyVerified": True,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
    })
    print(f"Checkpoint794 durably saved at signed{head}; all{len(before)} historical roots preserved.")


{"start": start, "audit": audit, "seal": seal, "finish": finish}[sys.argv[1]]()
