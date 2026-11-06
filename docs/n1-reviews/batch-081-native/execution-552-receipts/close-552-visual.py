import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual", C / "review-batch-081-visual.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
R, V, N, LOG = v.R, v.V, v.N, v.LOG
load, save, sha, git = v.load, v.save, v.sha, v.git
S = R / "docs" / "n1-sources"
E = S / "execution-552.json"
NEXT = (
    "SAME081 combined-current-main acceptance/integration and authorized owner-testing publication "
    "ONLY if every original gate passes; no082 or second runner. Start from signed execution552 "
    "visual-closed evidence; both original sessions independently inspected complete common packet "
    "and25 direct original PNG groups covering45 originals, serial27 children per family/all exits0. "
    "Actual ClaudeOpus5.5 and GPT6.1Sol; no actionable scoped defect. Preserve Claude compressed-history "
    "disclosure, source/returned1080x2400-to900x2000 auto-resizing and complete original reports. "
    "Scope complete冶/冶金 plus ONLY added金bullet.29Han/fourfamilies incl.冫/氵 readable; "
    "faint prose冫 optional, not phone evidence or identified fallback face. Curated治/台/始 "
    "textually reviewed but NOT the captured random meaning alternatives; no every-pool claim. "
    "Inherit textualb7bf953d, fresh549HOST3+1/no skips,550compile and551bothnamednativecases "
    "terminal0/no skips without rerun absent new concern. Exact full95a87783archive through "
    "productionContentSyncONCE1093kanji5049words113N1/versionf1dd5d8b9d2ff535/zeroProblems/epoch1; "
    "full onヤ/kunい.る preserved, selectedonヤ/kun[], soleやgoodlog/1of1Done. Two pairs/four "
    "directions/SystemBack/offline/seveninjectedstrokes/shape-only/giveuprecall NOT humanmemory "
    "or MLKitrecognition/modeldownload. Owned5580 stopped; owner5556 untouched. Fetchlatestmain/"
    "nonrewritingmerge/surgicalreconciliation/regeneratedmanifest/fullrequiredPython+vocabulary+"
    "budget+baseline/link/membershipchecks on actual combined tree; independently review substantive "
    "teaching changes if any. Fresh549Android may be inherited ONLY when runtime/tools unchanged; "
    "otherwise applicablefreshnon-skippedtests. Normal signing; onhang preserve/report/yield, "
    "no retry/bypass. Authorizedownerfastforward/publicSHA/terminalgreenCI/EVERYimmutableZIP "
    "runtimehash/original18000entries42MiBcompressed80MiBinflated56MiBretainedguards/verifiedowner "
    "issue60 receipt required before counting delivery. No unreviewedpush/guardincrease/appchange/"
    "nextbatch. Durablecontrolhelpers/approvedworkspaceinputs/committedsourcepackets only; optional "
    "historical session recipes skipped. Actualnewdenial preserve/report/yield. Preserve FULLlivehistory/"
    "all source/lookup/citation/read-depth/process/permission/OOM/viewport/phone/baseline limits. "
    "Published107/1228,remaining1121; local108th addition NOT delivered. CompatibleAndroidf9b59a2+ "
    "required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def record():
    freeze = v.frozen()
    previous = None
    process = {}
    for family in ["claude", "gpt"]:
        prefix = f"batch-081-visual-{family}"
        row = load(V / (prefix + "-execution.json"))
        assert row["processAndCoverageAccepted"] and row["completePacketReturned"]
        assert row["actualModels"] == [v.SESSIONS[family][0]]
        assert row["sessionId"] == v.SESSIONS[family][1]
        assert row["distinctImagePayloadsVerified"] == 25 and len(row["turns"]) == 27
        assert sha(V / (prefix + ".md")) == row["reportSha256"]
        assert sha(Path(row["rawExecutionLocation"])) == row["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(row["startedAt"])
        previous = row["completedAt"]
        for i, t in enumerate(row["turns"]):
            assert t["singleResourceAccepted"] and t["exitCode"] == 0
            if i:
                assert datetime.fromisoformat(row["turns"][i-1]["completedAt"]) < datetime.fromisoformat(t["startedAt"])
            if "imagePayload" in t:
                assert sha(R / t["imagePayload"]["returnedPayloadCopy"]) == t["imagePayload"]["sha256"]
        events = [json.loads(s) for s in Path(row["rawExecutionLocation"]).read_text(
            encoding="utf-8-sig").splitlines() if s.strip()]
        process[family] = {
            **{k: row[k] for k in ["requestedModel", "actualModels", "sessionId", "startedAt",
                                  "completedAt", "reportSha256", "rawExecutionSha256"]},
            "execution": prefix + "-execution.json", "report": prefix + ".md",
            "observations": prefix + "-observations.md",
            "compactionEventTypes": sorted({e["type"] for e in events if "compact" in e["type"]}),
            "sourceDimensions": sorted({tuple(t["imagePayload"]["sourceDimensions"])
                                        for t in row["turns"] if "imagePayload" in t}),
            "returnedDimensions": sorted({tuple(t["imagePayload"]["returnedDimensions"])
                                          for t in row["turns"] if "imagePayload" in t}),
        }
    reconciliation = {
        "schemaVersion": 1, "execution": 552, "batch": "081",
        "status": "bounded-visual-confirmation-closed-awaiting-integration",
        "evidenceHead": v.HEAD, "reviewedTeachingSnapshot": v.TEACHING,
        "nativeEnvelopeSnapshot": "95a87783e4be501c4b2b788d6906f6cc76b3c751",
        "reviewType": "Dependent original-session confirmations, not replacement blind linguistic initials.",
        "processes": process,
        "process": {
            "oneReviewerFamilyActiveAtATime": True, "hostDispatchedChildrenPerFamily": 27,
            "resourceTurnsPerFamily": 26, "sourcePacketsPerFamily": 1, "distinctPngsPerFamily": 25,
            "zeroToolFinalReportTurnsPerFamily": 1, "allChildrenExitedBeforeNext": True,
            "firstFamilyReportAndEvidenceArchivedBeforeSecondLaunch": True,
            "availableTools": ["view"], "observedToolOverlaps": 0, "unfinishedTools": 0,
            "commonTaskAndSourceAccess": True, "otherReportOrCoordinatorVerdictSupplied": False,
            "runtimeEditsDuringReviews": False,
        },
        "coverage": {
            "originalPngs": 45, "distinctByteGroupsPerFamily": 25, "byteAliasCaptures": 20,
            "completePacketReturnedBothFamilies": True, "originalAndReturnedPayloadsPreserved": True,
            "sourceByteIdenticalReturnedImages": 0,
            "qualification": "Both families directly opened original files. Full-frame auto-resizing from1080x2400 to900x2000 is recorded; no original-resolution-byte claim. Delivery/hashes are not comprehension certification.",
            "claudeReadDepth": "All resources directly returned in serial processes; final report discloses resource26 observation after history compression, from its own view notes rather than fresh pixels. Original per-turn observations retained.",
            "gptReadDepth": "All resources returned serially. Final report discloses no summary-only subset. No equal live-context-depth or comprehension guarantee.",
        },
        "assignedScope": {
            "kanji/冶.md": "Complete NEW article, all three facets; unchanged lexical findings inherited.",
            "words/冶金.md": "Complete necessary NEW article, all three facets; unchanged lexical findings inherited.",
            "kanji/金.md:39": "ONLY the added reciprocal Common words bullet; other content context only.",
        },
        "verdicts": {name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
                            "boundedVisualComprehensibility": "CLEAN"}
                     for name in ["kanji/冶.md", "words/冶金.md", "kanji/金.md:39 added bullet"]},
        "findings": [], "actionableRemainingFindings": 0,
        "consequentialUnresolvedScopedTeachingFindings": 0, "teachingChanges": [],
        "reconciliation": [
            {"claim": "No actual rendered article/font/quiz evidence at textual closure.",
             "status": "resolved", "scope": "Both complete new articles and exact reused bullet,29Han/fourfamilies and whole冶金 readable in bounded emulator pixels; not physical-phone/general UI certification."},
            {"claim": "Tables or source line absent because clipped in one frame.",
             "status": "resolved", "scope": "Signposted horizontal scrolling and complementary left/shifted states collectively expose labels and source-only explanation.冶金 ending/source line visible in a complementary scroll state; not all columns in one frame."},
            {"claim": "Faint standalone冫 in prose and original wording/citation/comparison expansions.",
             "status": "optional", "decision": "No edit. Both reviewers see distinct冫/氵 in actual panels. Claude's faint prose-radical polish does not establish an unreadable scoped detail or new app prerequisite. Original five optional textual suggestions retained unchanged; physical-phone legibility outstanding."},
            {"claim": "Captured meaning alternatives certify curated治/台/始 at runtime or every random pool.",
             "status": "unresolved", "scope": "Outside bounded certification. Captured wrong labels two(formal numeral),chrysanthemum,moreover/also are defensibly wrong for冶. Curated trio retains original textual review, not captured-use evidence. No cause inferred or app fix added."},
            {"claim": "Pixels prove import/persistence/tap order/offline or fallback-face identity.",
             "status": "partially resolved", "scope": "Destination pixels consistent with full supplied fixture/terminal/route and native551 terminal0 receipts; not reviewer-executed tests. Final tree is transient loading, not loaded-route proof. Pixels/Paint/raster hashes do not identify fallback face."},
            {"claim": "Injected strokes and give-up recall demonstrate human recognition/successful memory.",
             "status": "unresolved", "scope": "Not claimed. Seven injected references,shape-only feedback and grade persistence are bounded fixture evidence; offline handwriting model unavailable. No human/MLKit/model-download/phone inference."},
        ],
        "modelContributionComparison": {
            "shared": "No actionable defect across same complete packet/25PNGgroups/three teaching scopes. Both recognize differing captured meaning choices,table complementarity,legible glyphs and supplied-execution limits.",
            "claudeOnlyVerifiedUseful": "Explicit resource26 compressed-history qualification and optional faint standalone prose冫 observation. No unique actionable defect.",
            "gptOnlyVerifiedUseful": "No unique actionable defect established; final-tree loading observation also in Claude packet-turn notes, not unique.",
            "limits": "Compared equivalent observations in final/optional/limits/per-turn notes, not model ranking or equal-comprehension claim.",
        },
        "reportQualifications": [
            "Claude's 'all40font families' wording is retained verbatim but not adopted: original audit covers40 target characters; this batch shows four font families.",
            "Claude's 'article names' wording for curated choices refers to metadata in source packet, not necessarily learner prose.",
            "Reports do not independently verify hashes/Git/upstream. Successful actual delivery does not certify fresh semantic comprehension.",
        ],
        "boundedIndependentVisualConfirmation": True, "runtimePublished": False,
        "nextBatchStarted": False,
        "limits": [
            "Original textual source/citation/lookup/reading/quiz/baseline limitations inherited, not freshly dictionary-verified.",
            "Full-frame resized25PNGgroups per family, not45 independent captures or120Paint-probe PNG reads; no fallback-face identification.",
            "Claude compressed-history disclosure retained; both complete original reports and visible per-turn observations unchanged.",
            "Fresh549 HOST3+1/no skips,550compile and551two native terminal0 cases inherited, not rerun. Disposable synthetic source/seeds, not owner progress.",
            "Physicalphone/generalrelease/whole-set and final combined-main integration/publication/CI/immutableZIP acceptance outstanding.",
            "No new emulator/Android run, optional historical session helper, actual permission denial,publication,082 or second runner.",
        ],
    }
    save(V / "batch-081-visual-reconciliation.json", reconciliation)
    ledger_path = S / "batch-081-progress.json"
    ledger = load(ledger_path)
    assert "preVisual552AcceptanceState" not in ledger
    ledger["preVisual552AcceptanceState"] = {
        k: ledger[k] for k in ["status", "reviewClosed", "runtimeAccepted", "independentVisualAcceptance",
                              "nextAction", "limits", "fontDisposition"]}
    ledger.update(
        status=reconciliation["status"], reviewClosed=["冶"],
        independentVisualAcceptance=True, runtimeAccepted=False,
        visualEvidence="docs/n1-reviews/batch-081-visual-reconciliation.json",
        fontDisposition="Both original model families directly inspected29Han/fourfamilies in three Compose panels plus whole冶金;冫/氵 distinct. Bounded API35 emulator pixels, not physical-phone or fallback-face evidence.",
        nextAction=NEXT, limits=reconciliation["limits"],
    )
    save(ledger_path, ledger)
    evidence = {
        **load(LOG / "starting-state-552.json"), "schemaVersion": 1, "checkpoint": 552,
        "status": "continue", "stage": reconciliation["status"], "completedAt": v.now(),
        "reconciliation": "docs/n1-reviews/batch-081-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-081-visual-reconciliation.json"),
        "reviewedTeachingSnapshot": v.TEACHING, "evidenceHead": v.HEAD,
        "processes": process, "independentVisualAcceptance": True,
        "runtimePublished": False, "runtimeBytesUnchanged": True,
        "publishedAdditions": 107, "remainingAdditions": 1121,
        "lastPublishedCommit": "a7b119ed36adf7a3a92bba03700bc1c51f812bef",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT, "limits": reconciliation["limits"],
    }
    save(E, evidence)
    print("Both complete original reports reconciled; no actionable scoped defect.")


def seal():
    v.frozen()
    e = load(E)
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from build_manifest import build_manifest, sha256
    e["mechanicalBatchAudit"] = audit(R, "081")
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert manifest == json.loads(git("show", f"{v.HEAD}:manifest.json"))
    count = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                count += 1
    assert count == 8369
    whitespace = subprocess.run(
        ["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check"],
        capture_output=True, encoding="utf-8")
    assert whitespace.returncode in (0, 2)
    warning_headers = [line for line in whitespace.stdout.splitlines()
                       if line.startswith("docs/") and ": " in line]
    assert all(line.startswith((
        "docs/n1-reviews/batch-081-visual-source-packet.txt:",
        "docs/n1-reviews/batch-081-visual-config-help-execution-552.txt:"))
        for line in warning_headers)
    save(V / "batch-081-visual-whitespace-disposition.json", {
        "execution": 552, "checkExitCode": whitespace.returncode,
        "originalOutput": whitespace.stdout, "warningCount": len(warning_headers),
        "decision": "Preserve exact already-reviewed line-numbered packet (number plus space on source blank lines) and original CLI help terminal blank line. No runtime or authored-code whitespace warning. No altered report/source bytes or production lint exception.",
    })
    receipts = N / "execution-552-receipts"
    receipts.mkdir(exist_ok=True)
    for path in [Path(__file__), C / "review-batch-081-visual.py", C / "post-552-issue.ps1",
                 LOG / "validate-552.txt", LOG / "manifest-552.txt"]:
        shutil.copyfile(path, receipts / path.name)
    e.update(
        runtimePayloadHashesVerified=count, manifestSha256=sha(R / "manifest.json"),
        validatorErrors=0, manifestFresh=True, runtimeBytesUnchanged=True,
        validationReceipts=[{"path": str(p.relative_to(R)), "sha256": sha(p)}
                            for p in sorted(receipts.iterdir())],
        whitespaceDisposition="docs/n1-reviews/batch-081-visual-whitespace-disposition.json",
    )
    save(E, e)
    print("8369 runtime hashes, exact frozen manifest, batch baseline/link/reading audit verified.")


def checkpoint():
    original = load(LOG / "progress-before-552.json")
    p = load(C / "progress.json")
    e = load(E)
    receipt = load(LOG / "issue-response-552.json")
    body = (LOG / "issue-body-552.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.rstrip()
    assert git("rev-parse", "HEAD^") == v.HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    android = C.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "-C", str(android), "status", "--porcelain"])
    assert not git("diff", v.HEAD, "HEAD", "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    assert sha(R / "manifest.json") == e["manifestSha256"]
    for r in e["validationReceipts"]:
        assert sha(R / r["path"]) == r["sha256"]
    result = {
        "schemaVersion": 1, "execution": 552, "checkpoint": 552, "batch": "081",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": e["stage"], "evidence": "docs/n1-sources/execution-552.json",
        "evidenceSha256": sha(E), "independentVisualAcceptance": True,
        "actualModels": [v.SESSIONS[f][0] for f in ["claude", "gpt"]],
        "serialReviewerChildren": 54, "allChildExits": 0, "sourcePacketsPerFamily": 1,
        "originalPngs": 45, "distinctPngGroupsPerFamily": 25,
        "runtimePayloadHashesVerified": 8369, "runtimeBytesUnchanged": True,
        "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 107, "remainingAdditions": 1121,
        "lastPublishedCommit": e["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "originalRootKeyCountCompared": len(original),
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "changedRootFields": ["checkpoint", "status", "stage", "nextAction", "blocker"],
    }
    assert p["checkpoint"] == 551 and p["batch"] == "081"
    p.update(checkpoint=552, status="continue", stage=e["stage"], nextAction=NEXT, blocker=None)
    p["execution552CoordinatorCheckpoint"] = result
    p["batch081VisualExecution552"] = result
    allowed = set(result["changedRootFields"])
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread[k] == value for k, value in original.items() if k not in allowed)
    save(LOG / "coordinator-checkpoint-552.json", result)
    print(json.dumps({k: result[k] for k in ["checkpoint", "status", "savedCommit", "issueUpdate",
                                           "allOriginalHistoricalRootKeysPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"record": record, "seal": seal, "checkpoint": checkpoint}[sys.argv[1]]()
