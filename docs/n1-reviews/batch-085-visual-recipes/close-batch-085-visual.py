import gzip
import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual085", C / "review-batch-085-visual.py")
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)
R, A, V, N, L = x.R, x.A, x.V, x.N, x.L
load, save, sha, git = x.load, x.save, x.sha, x.git
STAGE = "native-and-original-family-visual-accepted-awaiting-combined-main"
E = R / "docs" / "n1-sources" / "execution-597.json"
NEXT = (
    "SAME085 fresh latest-main normal integration and combined-tree acceptance NEXT; "
    "persist/yield before publication if necessary, no086. Read execution-597.json and "
    "batch-085-visual-reconciliation.json, original593 textual/two-family reports, fresh594 HOST4 "
    "zero-skips, compiled595 and596 TWO native terminalcase0 receipts. Same reviewed teachinga7512a5e "
    "plus exact effort exclusion29a53380, envelope1d2e3290/version0c514711ae8d3212/8413runtimehashes. "
    "OriginalClaudeOpus5.5 session58040cfc-7f07-4bd0-bb1e-18ba6bf9c793 and GPT6.1Sol "
    "session7e74aba9-d92a-4615-b858-c68100c7dfdb serial dependent visual confirmations archived597; "
    "actual models/toolpayloads/process exits/read-depth/resize/coverage limits retained. "
    "No new blind-review credit, fallbackface identification, equal comprehension or87fullresolutionreads. "
    "39Han/fourfamilies/threewholewords, complete scoped articleprojections plus changed固bullet, "
    "N1selection/meaning/readings/drawing/articles/Back within capturedscope; source/terminal/route "
    "versus pixels and any reviewed limits explicit. Full metadata sixreadings retained; curated"
    "onギョウ/kunこ.る,こ.らす yields exactlyぎょう/こる BOTHkindspersistedGood/done, selectedこ.らす "
    "shares normalizedこる NOT independentqueuedmastery. ProductionContentSyncONCE1108kanji5063words"
    "117N1/zeroProblems/version/acceptedRoomepoch1, fourreciprocalpairs/eightdirections/offline, "
    "defaultfour凝/准/冗/凹 IDs+titles N1ANDAll builder/N1UI inherited. AllUI/custom/padded/partial/"
    "larger/random pools uncertified.16reference-injectedstrokes/trace/recallgiveup/gradepersistence "
    "NOT humanhandwriting/MLKit/phone; offline handwritingmodel unavailable. QualifiedTESTONLY"
    "Android1c1b7bf4 atop unchangedproductionf9b59a2, notlatestappmain. No repeatedHOST/native absent"
    "actualchange/newconcern. Require freshorigin/main normalnonrewritingmerge, surgical reconciliation, "
    "regeneratedmanifest and combinedPythonunittest/validate/vocabulary/manifestfreshness/everyruntimehash/"
    "membership/baseline/link/readings/exact32directguards/original18000entries42MiBcompressed80MiBinflated"
    "56MiBretained/perfile-media-safepaths budgets and applicable actualcombinedtree Android checks, "
    "substantivechangedteaching independentboundedrereview. Then normallysignedownerfastforward/"
    "exactremote/terminalgreenCI/EVERYimmutablepublicZIPmanifestentryhash/verifiedownerissue60 BEFORE086. "
    "No unreviewed teaching push. Parent19008runner.lock remains parent-only; verify liveancestry/"
    "session/checkpoint/exactsignedheads/whollycleanworktrees; NOchildacquisition/delete/unlock. "
    "Approvedcontrolhelpers/committedsources only/nooptionalhistoricalsessionhelpers. Preserve/report/"
    "yield actualnewdenial/signinghang/uncertainownership. Any trulyneeded future native requires "
    "freshlocalANDremote5580/5581 inclTimeWait/device/PIDinspection, ownedreadonlyAPI35hostGPU/-Vulkan/"
    "2048MiB2cores/explicitserial5580/noalternateport/no shareddeviceinterference/noheapguardincrease/"
    "ownedonlycleanup. All original source/reviewer/lookup/readdepth/process/viewport limitations and "
    "Q1resolved/otheroptional dispositions preserved. Published111/1228,remaining1117/latestpublic"
    "97a16b0027b05c0528d78971dd3b17cce17d8056 unchanged;085notdelivered. Physicalphone/generalrelease/"
    "whole-setoutstanding; projectincomplete. No086."
)


def audit():
    f = x.frozen()
    x.ancestry()
    processes = {}
    previous = None
    for family, (model, session) in x.SESSIONS.items():
        prefix = x.PREFIX + "-" + family
        record = load(V / (prefix + "-execution.json"))
        assert record["processAndCoverageAccepted"] and record["sourcePacketComplete"]
        assert record["actualModels"] == [model] and record["sessionId"] == session
        assert record["acceptedImagePayloads"] == 23 and len(record["turns"]) == 25
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(record["startedAt"])
        previous = record["completedAt"]
        folder = C / (prefix + "-turns")
        for i, turn in enumerate(record["turns"]):
            assert turn["exitCode"] == 0
            assert turn["actualModels"] == [model]
            assert turn["toolCalls"] == (0 if i == 24 else 1)
            if i:
                assert datetime.fromisoformat(record["turns"][i-1]["completedAt"]) < datetime.fromisoformat(turn["startedAt"])
            raw = folder / f"turn-{i+1:02d}.jsonl"
            assert sha(raw) == turn["rawSha256"]
            if "imagePayload" in turn:
                p = turn["imagePayload"]
                assert sha(R / p["returnedPayloadCopy"]) == p["sha256"]
                assert sha(Path(turn["resource"])) == p["sourceSha256"]
        raw_events = gzip.decompress((V / (prefix + "-turns.jsonl.gz")).read_bytes())
        assert raw_events == b"".join(p.read_bytes() for p in sorted(folder.glob("turn-*.jsonl")))
        events = [json.loads(s) for s in raw_events.decode("utf-8-sig").splitlines() if s.strip()]
        active = set()
        calls = 0
        for event in events:
            d = event.get("data", {})
            if event["type"] == "tool.execution_start":
                assert not active and d["toolName"] == "view"
                active.add(d["toolCallId"])
                calls += 1
            elif event["type"] == "tool.execution_complete":
                active.remove(d["toolCallId"])
                assert d["success"]
        assert not active and calls == 24
        processes[family] = {
            "actualModel": model, "sessionId": session,
            "startedAt": record["startedAt"], "completedAt": record["completedAt"],
            "report": prefix + ".md", "reportSha256": sha(V / (prefix + ".md")),
            "execution": prefix + "-execution.json",
            "rawArchive": prefix + "-turns.jsonl.gz",
            "rawArchiveSha256": sha(V / (prefix + "-turns.jsonl.gz")),
            "verifiedChildExits": 25, "completePacketReturned": True,
            "acceptedImagePayloads": 23, "observedToolOverlaps": 0,
            "compactionEventTypes": sorted({e["type"] for e in events if "compact" in e["type"]}),
            "sourceDimensions": sorted({tuple(t["imagePayload"]["sourceDimensions"])
                                       for t in record["turns"] if "imagePayload" in t}),
            "returnedDimensions": sorted({tuple(t["imagePayload"]["returnedDimensions"])
                                         for t in record["turns"] if "imagePayload" in t}),
        }
    return f, processes


def record():
    f, processes = audit()
    adjudication = load(C / "batch-085-visual-adjudication-597.json")
    assert adjudication["actionableRemainingFindings"] == 0
    assert adjudication["consequentialUnresolvedScopedClaims"] == 0
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256 as text_sha256
    from audit_n1_batch import audit as batch_audit
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest == json.loads(git(R, "show", f"{x.HEAD}:manifest.json"))
    verified = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert (sha(R / name) if binary else text_sha256(R / name)) == digest, name
                verified += 1
    assert verified == 8413
    native = load(R / "docs" / "n1-sources" / "execution-596.json")["nativeAcceptance"]
    assert native["nativeAcceptancePassed"] and native["nativeSkips"] == 0
    assert len(native["caseResults"]) == 2 and all(r["status"] == 0 for r in native["caseResults"])
    reconciliation = {
        "schemaVersion": 1, "execution": 597, "batch": "085", "status": STAGE,
        "evidenceHead": x.HEAD, "processes": processes,
        "process": {
            "oneReviewerFamilyActiveAtATime": True, "hostDispatchedChildrenPerFamily": 25,
            "completeSourcePacketsPerFamily": 1, "contactSheetsPerFamily": 15,
            "focusedOriginalPathsPerFamily": 8, "allChildrenExitedBeforeNext": True,
            "firstReportArchivedBeforeSecondLaunch": True, "availableTools": ["view"],
            "observedToolOverlaps": 0, "unfinishedTools": 0, "sameTaskSourceImages": True,
            "otherReportOrCoordinatorVerdictSupplied": False, "runtimeEditsDuringReviews": False,
        },
        "coverage": {
            "originalPngs": 87, "fullFrameContactSheetsPerFamily": 15,
            "focusedOriginalPathsPerFamily": 8, "actualHan": 39, "productionFontFamilies": 4,
            "originalAndReturnedPayloadsPreserved": True,
            "limits": f["limits"],
        },
        **adjudication, "independentVisualAcceptance": True,
        "runtimeAccepted": True, "runtimePublished": False,
        "newHostOrNativeRuns": 0, "nextBatchStarted": False, "nextAction": NEXT,
    }
    save(V / "batch-085-visual-reconciliation.json", reconciliation)
    for path in [V / "batch-085-reconciliation.json", R / "docs" / "n1-sources" / "batch-085-progress.json"]:
        ledger = load(path)
        ledger["preVisual597State"] = {
            k: ledger.get(k) for k in ["status", "reviewClosed", "runtimeAccepted", "runtimePublished", "nextAction"]
        }
        if "nativeFontPending" in ledger:
            ledger["preVisual597State"]["nativeFontPending"] = ledger["nativeFontPending"]
            ledger.update(nativeFontPending=[], nativeVisualHanCount=39)
        ledger.update(status=STAGE, runtimeAccepted=True, runtimePublished=False,
                      independentVisualAcceptance=True,
                      visualConfirmation="docs/n1-reviews/batch-085-visual-reconciliation.json",
                      nextAction=NEXT, visual597Limits=adjudication["limits"])
        if path.name == "batch-085-progress.json":
            ledger.update(reviewClosed=["凝"], published=[])
        save(path, ledger)
    receipts = V / "batch-085-visual-recipes"
    receipts.mkdir(exist_ok=False)
    for path in [Path(__file__), C / "review-batch-085-visual.py",
                 C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
                 C / "batch-085-visual-adjudication-597.json",
                 C / "post-batch-085-visual-597.ps1",
                 L / "visual-597-validate.txt", L / "visual-597-manifest.txt"]:
        shutil.copyfile(path, receipts / path.name)
    save(E, {
        "schemaVersion": 1, "execution": 597, "batch": "085", "status": "continue", "stage": STAGE,
        "startingState": load(C / "progress.json")["execution597StartingState"],
        "evidenceHead": x.HEAD, "androidHead": x.APP, "processes": processes,
        "reconciliation": "docs/n1-reviews/batch-085-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-085-visual-reconciliation.json"),
        "runtimeManifestFresh": True, "runtimeBytesUnchanged": True,
        "runtimePayloadHashesVerified": verified, "batchAudit": batch_audit(R, "085"),
        "independentVisualAcceptance": True, "runtimeAccepted": True, "runtimePublished": False,
        "newHostOrNativeRuns": 0, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "publishedAdditions": 111, "remainingAdditions": 1117,
        "lastPublishedCommit": "97a16b0027b05c0528d78971dd3b17cce17d8056",
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "limits": adjudication["limits"],
        "recipeReceipts": [{"path": str(path.relative_to(R)), "sha256": sha(path)}
                           for path in sorted(receipts.iterdir())],
        "diagnostics": [
            "An initial copilot config help invocation treated help as an unknown settings key and exited1; no setting changed or permission denial. Correct actual copilot --help and copilot help config catalog were captured before reviewer launch.",
            "Initial record helper used raw-byte hashes for all manifest payloads and correctly stopped on CRLF text before changing any ledger. Corrected to repository build_manifest.sha256 for normalized text and raw binary hashes, matching the existing manifest contract. Validator remained0errors, regenerated manifest unchanged; no content or permission failure."
        ],
    })
    print("Both original-family reports reconciled; runtime unchanged and publication remains gated.")


def finalize():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 596 and p["stage"] == "batch-085-original-family-visual-confirmations"
    saved = git(R, "rev-parse", "HEAD")
    assert git(R, "rev-parse", "HEAD^") == x.HEAD
    assert git(R, "log", "-1", "--format=%G?") == "G"
    assert not git(R, "status", "--porcelain") and not git(A, "status", "--porcelain")
    assert git(A, "rev-parse", "HEAD") == x.APP
    assert not git(R, "diff", x.HEAD, "HEAD", "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    x.ancestry()
    receiptpath = C / "batch-085-visual-597-issue-receipt.json"
    receipt = load(receiptpath)
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (C / "batch-085-visual-597-issue-body.txt").read_bytes().decode("utf-8-sig")
    old = load(L / "progress-before-597.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in old.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 597, "checkpoint": 597, "batch": "085",
        "status": "continue", "stage": STAGE, "savedCommit": saved, "signature": "G",
        "evidence": "docs/n1-sources/execution-597.json",
        "independentVisualAcceptance": True, "runtimeAccepted": True, "runtimePublished": False,
        "dedicatedWorktreesClean": True, "newHostOrNativeRuns": 0,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "publishedAdditions": 111, "remainingAdditions": 1117,
        "lastPublishedCommit": "97a16b0027b05c0528d78971dd3b17cce17d8056",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(receiptpath), "nextAction": NEXT,
        "originalRootKeysCompared": len(old),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
        "actualModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "serialReviewerChildren": 50, "allChildrenExitedZero": True,
        "completeSourcePacketsPerFamily": 1, "contactSheetsPerFamily": 15,
        "focusedOriginalPathsPerFamily": 8, "originalPngs": 87,
        "runtimeBytesUnchanged": True, "runtimePayloadHashesVerified": 8413,
    }
    p.update(checkpoint=597, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution597CoordinatorCheckpoint"] = checkpoint
    p["batch085VisualCheckpoint"] = checkpoint
    x.persist(p)
    reread = load(C / "progress.json")
    assert all(reread[k] == v for k, v in old.items() if k not in allowed)
    save(L / "batch-085-visual-checkpoint.json", checkpoint)
    evidence = load(E)
    for row in evidence["recipeReceipts"]:
        assert sha(R / row["path"]) == row["sha256"]
    changed = git(R, "diff-tree", "--no-commit-id", "--name-only", "-r", saved).splitlines()
    for name in changed:
        blob = subprocess.check_output(["git", "-C", str(R), "show", f"{saved}:{name}"])
        assert blob == (R / name).read_bytes(), name
    save(L / "execution-597-final-verification.json", {
        **checkpoint, "committedEvidenceFilesByteVerified": len(changed),
        "evidenceSha256": sha(E), "verifiedAt": x.now(),
    })
    print(saved, receipt["html_url"], "checkpoint597 continue; history preserved")


def seal():
    recipes = V / "batch-085-visual-recipes"
    shutil.copyfile(Path(__file__), recipes / Path(__file__).name)
    evidence = load(E)
    evidence["recipeReceipts"] = [
        {"path": str(path.relative_to(R)), "sha256": sha(path)}
        for path in sorted(recipes.iterdir())
    ]
    for relative, allowed in [
        ("docs/n1-reviews/batch-085-reconciliation.json",
         {"status", "runtimeAccepted", "nextAction", "nativeFontPending"}),
        ("docs/n1-sources/batch-085-progress.json",
         {"status", "runtimeAccepted", "nextAction", "reviewClosed"}),
    ]:
        original = json.loads(git(R, "show", f"{x.HEAD}:{relative}"))
        current = load(R / relative)
        assert all(current[k] == value for k, value in original.items() if k not in allowed)
    staged = git(R, "diff", "--cached", "--name-only").splitlines()
    assert staged and all(name.startswith((
        "docs/n1-reviews/batch-085-visual-", "docs/n1-reviews/batch-085-reconciliation.json",
        "docs/n1-sources/batch-085-progress.json", "docs/n1-sources/execution-597.json",
    )) for name in staged)
    result = subprocess.run(
        ["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check"],
        capture_output=True, encoding="utf-8"
    )
    assert result.returncode in (0, 2)
    warnings = [line for line in result.stdout.splitlines() if line.startswith("docs/")]
    exact_evidence = {
        "batch-085-visual-source-packet.txt", "batch-085-visual-task.txt",
        "batch-085-visual-claude-observations.md", "batch-085-visual-gpt-observations.md",
        "batch-085-visual-claude.md", "batch-085-visual-gpt.md",
        "batch-085-visual-copilot-help-execution-597.txt",
        "batch-085-visual-copilot-model-catalog-execution-597.txt",
    }
    assert all(line.split(":")[0].split("/")[-1] in exact_evidence
               or "-returned/turn-" in line and "-prompt.txt:" in line for line in warnings), result.stdout
    assert all(": trailing whitespace." in line or ": new blank line at EOF." in line
               for line in warnings), result.stdout
    save(V / "batch-085-visual-whitespace-disposition.json", {
        "execution": 597, "checkExitCode": result.returncode,
        "originalOutput": result.stdout, "warningCount": len(warnings),
        "decision": "Preserve exact reviewed line-numbered packet, task, CLI captures and original reviewer text/prompts. No runtime or authored-code whitespace exception.",
    })
    evidence["whitespaceDisposition"] = "docs/n1-reviews/batch-085-visual-whitespace-disposition.json"
    save(E, evidence)
    print("Historical ledger preservation and evidence-only whitespace disposition verified.")


if __name__ == "__main__":
    if sys.argv[1] == "record":
        record()
    elif sys.argv[1] == "finalize":
        finalize()
    elif sys.argv[1] == "seal":
        seal()
