import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual", C / "review-batch-082-visual.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
R, V, N, LOG = v.R, v.V, v.N, v.LOG
load, save, sha, git = v.load, v.save, v.sha, v.git
S = R / "docs" / "n1-sources"
E = S / "execution-561.json"
ANDROID = C.parent / "kanji-cards-android"
STAGE = "batch-082-visual-inspected-awaiting-runtime-choice-reconciliation"
NEXT = (
    "SAME082 bounded runtime-meaning-choice reconciliation next, then persist/yield; "
    "NO integration/publication/083 until consequential082-V1 is closed. Start signed execution561 "
    "and docs/n1-reviews/batch-082-visual-reconciliation.json plus "
    "batch-082-runtime-choice-investigation.json. BOTH original sessions completed serial dependent "
    "visual confirmations: ClaudeOpus5.5 session1c5aebb9-9903-4567-a88a-5da4b472781d then GPT6.1Sol "
    "sessionfd9a447c-6e9f-4874-a043-4851de97c996;30 exited children each, complete commonpacket/"
    "28originalPNGgroups covering51captures, actual returned900x2000 preserved. All31Han/"
    "fourfamilies, complete准/准教授 and exact教bullet/助教授successorlink readable. "
    "No proven prose/rendering defect, but overall independentVisualAcceptance FALSE: "
    "GPT correctnessUNVERIFIED for runtime准 meaning, Claude same hypothesis optional/lowrisk. "
    "Both saw captured imitate;emulate from倣, not curated集/進/難. Actual unchanged production "
    "QuizViewModel filters N1 BEFORE QuizBuilder; curated集N4/進N3/難N3 absent, fallbacktagpool "
    "supplies鯨/倣/冠. Code provenance and exact excerpts preserved; cause no longer speculative. "
    "FrozenJMdict1341500 recognizes rare准えるなぞらえる with imitate sense; public sourceJitsu "
    "observation alsoなぞらえる. Rarity is NOT disproof, dictionary recognition not ordinaryfrequency. "
    "Resolve precise semantic/learnerimpact with bounded source evidence and original sessions "
    "serially, not votes or silentlydowngradeGPT. If a necessary content correction is established, "
    "inspect complete applicable families/actual candidatearticles before authoring safe "
    "N1available curatedchoices and preserve source readings/titles; validate/regeneratemanifest/"
    "normal signedfreeze, twofamily changedpassagereview and applicablefreshHOST/native/screenshots "
    "on changedruntime. Do NOT make unrelatedAndroidalgorithmchanges; actual companion app "
    "prerequisite requires separate scope/authorization. Preserve original reports, sharedhypothesis/"
    "disagreement, Claude resource1-21 compressedhistory, all original source/lookup/citation/readdepth/"
    "process/denial/OOM/viewport/MLKit/phone limits. Inherit textualb6bcc8f1 and558HOST3+1+5/"
    "noskips/559compile/560TWOnativecases terminal0/noskips honestly, not proof disputedchoiceunique. "
    "Full4f5812bc productionContentSyncONCE1094kanji5050words114N1/version0739a82c9699f031/"
    "zeroProblems/epoch1; Full+Lite onジュン/kun[]/selectedonジュン/selectedkun[]/soleじゅん. "
    "Two mappedpairs+comparisonpair/sixdirections/SystemBack/offline/tenreferenceinjectedstrokes/"
    "shapeonly/giveuprecall NOT humanmemory/recognition/MLKitdownload/phone. QualifiedTESTONLY "
    "Android1c1b7bf4/G preserves productionf9b59a2, not latestappmain. HOSTonly2g init NEVERnative; "
    "noapp/guestheap/archiveguardincrease. AFTERclosure latestmain/nonrewritingintegration/"
    "combinedPython368/validator/vocabulary/freshmanifest/exact虎猿/baseline/link/membership/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedguards/normal signedowner "
    "fastforward/remoteSHA/terminalgreenCI/EVERYimmutableZIPhash/verifiedownerissue60 "
    "mandatorybefore083. Published108/1228,remaining1120,lastPublished1f317f0762513720709ab0ca215f19ff021ca596; "
    "082notdelivered. Physicalphone/generalrelease/whole-setoutstanding. FULLlivehistory/"
    "approvedworkspaceinputs/committedsourcepackets/controlhelpers only; optionalhistoricalsession "
    "recipes skipped. Onecoordinator/oneactive reviewermaximum/no secondrunner. Actualnewdenial "
    "or signinghang preserve/report/yield withoutworkaround."
)


def record():
    v.frozen()
    previous = None
    process = {}
    for family in ["claude", "gpt"]:
        prefix = f"batch-082-visual-{family}"
        row = load(V / (prefix + "-execution.json"))
        assert row["processAndCoverageAccepted"] and row["completePacketReturned"]
        assert row["actualModels"] == [v.SESSIONS[family][0]]
        assert row["sessionId"] == v.SESSIONS[family][1]
        assert row["distinctImagePayloadsVerified"] == 28 and len(row["turns"]) == 30
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
    android_head = subprocess.check_output(
        ["git", "-C", str(ANDROID), "rev-parse", "HEAD"], encoding="utf-8").strip()
    assert android_head == "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
    code = [
        ("core/src/main/kotlin/io/github/stopcran/kanji/core/quiz/QuizBuilder.kt", 13, 28),
        ("app/src/main/java/io/github/stopcran/kanji/ui/QuizViewModel.kt", 89, 102),
        ("app/src/main/java/io/github/stopcran/kanji/ui/QuizViewModel.kt", 156, 162),
        ("app/src/main/java/io/github/stopcran/kanji/data/SrsMapping.kt", 30, 37),
        ("core/src/main/kotlin/io/github/stopcran/kanji/core/srs/Stacks.kt", 7, 29),
    ]
    source_rows = []
    for name, first, last in code:
        path = ANDROID / name
        unchanged = subprocess.check_output([
            "git", "-C", str(ANDROID), "diff",
            "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", "HEAD", "--", name])
        assert not unchanged
        lines = path.read_text(encoding="utf-8").splitlines()
        source_rows.append({
            "path": str(path), "sha256": sha(path), "range": [first, last],
            "lines": [{"line": n, "text": lines[n-1]} for n in range(first, last+1)],
            "productionBytesUnchanged": True,
        })
    investigation = {
        "execution": 561, "batch": "082", "androidSnapshot": android_head,
        "productionBaseline": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "source": source_rows,
        "capturedChoices": ["whale", "imitate; emulate", "quasi-; associate rank", "crown; peerless"],
        "capturedWrongSourceCards": ["鯨", "倣", "冠"],
        "curatedChoices": [{"kanji": "集", "jlpt": 4}, {"kanji": "進", "jlpt": 3},
                           {"kanji": "難", "jlpt": 3}],
        "establishedCause": "QuizViewModel.start filters the content list to the selected stack before constructing quizCards. QuizBuilder resolves curated IDs only in that list, then falls back to tag-similar cards. These three curated IDs cannot be used in the N1-only pool. This explains the captured mismatch without a new parser or curation-transport failure.",
        "semanticEvidence": [
            {"path": "docs/n1-sources/batch-082-jmdict.xml", "lines": [63, 98],
             "entry": "1341500", "claim": "准える is a rarely used kanji form ofなぞらえる; usually-kana senses include pattern/model after, imitate. Recognition does not establish frequency, but rarity does not disprove possible semantic overlap."},
            {"path": "docs/n1-sources/batch-082-source-evidence.json",
             "claim": "Existing supplied public字通 observation hasなぞらえる. Not freshly independently retrieved."},
        ],
        "status": "selection-path-established-semantic-impact-unresolved",
        "runtimeAccepted": False, "runtimeChanged": False, "newTestsRun": False,
        "decision": "No speculative content/algorithm change or downgrading of UNVERIFIED. Next bounded source-backed reconciliation retains publication gate and original disagreement.",
        "limits": "Coordinator code inspection, not independent review of these new excerpts. Existing case success proves intended selection works, not alternative semantic uniqueness. No new native/phone test.",
    }
    save(V / "batch-082-runtime-choice-investigation.json", investigation)
    verdicts = {
        name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
               "boundedVisualComprehensibility": "CLEAN"}
        for name in ["kanji/准.md", "words/准教授.md", "kanji/教.md:39 added bullet",
                     "words/助教授.md:16 successor link"]
    }
    verdicts["kanji/准.md"]["correctness"] = "UNVERIFIED"
    finding = {
        "id": "082-V1", "status": "unresolved", "severity": "Moderate if semantic ambiguity confirmed",
        "facets": ["runtime quiz correctness"], "confidence": "High in observed mismatch and code path; medium in semantic impact",
        "locations": ["kanji/准.md:13", "docs/n1-reviews/batch-082-native/N1Batch082NativeTest.kt:359-367"],
        "claim": "Actual N1-only meaning question offers imitate; emulate from倣 rather than the three curated non-N1 cards. Rare准える imitation evidence creates a plausible competing interpretation.",
        "impact": "Potential defensible alternative could be graded wrong. Passing intended-answer assertion does not prove semantic uniqueness.",
        "evidence": "Both complete reports and resource18/19 observations, actual screenshots, frozenJMdict1341500 and coordinator production-code investigation.",
        "remedy": "Bounded exact-source and original-session reconciliation before publication; only source-justified content correction and applicable fresh gates if necessary. No unapproved algorithm change.",
        "reviewerDisagreement": "Claude records this same observation as optional low risk and returns CLEAN; GPT preserves textualCLEAN but combined runtime correctnessUNVERIFIED. Do not rank as a uniquely discovered GPT issue or resolve by voting.",
    }
    reconciliation = {
        "schemaVersion": 1, "execution": 561, "batch": "082", "status": STAGE,
        "evidenceHead": v.HEAD, "reviewedTeachingSnapshot": v.TEACHING,
        "nativeEnvelopeSnapshot": "4f5812bc7f33e7996214661e7dbf5f8e765df849",
        "reviewType": "Dependent original-session confirmations, not replacement blind linguistic initials.",
        "processes": process,
        "process": {
            "oneReviewerFamilyActiveAtATime": True, "hostDispatchedChildrenPerFamily": 30,
            "sourcePacketsPerFamily": 1, "distinctPngsPerFamily": 28,
            "zeroToolFinalReportTurnsPerFamily": 1, "allChildrenExitedBeforeNext": True,
            "firstFamilyReportAndEvidenceArchivedBeforeSecondLaunch": True,
            "availableTools": ["view"], "observedToolOverlaps": 0, "unfinishedTools": 0,
            "commonTaskAndSourceAccess": True, "otherReportOrCoordinatorVerdictSupplied": False,
            "runtimeEditsDuringReviews": False,
        },
        "coverage": {
            "originalPngs": 51, "distinctByteGroupsPerFamily": 28, "byteAliasCaptures": 23,
            "completePacketReturnedBothFamilies": True, "originalAndReturnedPayloadsPreserved": True,
            "sourceByteIdenticalReturnedImages": 0,
            "qualification": "Both families directly opened original files. Full-frame auto-resizing from1080x2400 to900x2000 is recorded; no original-resolution-byte claim. Delivery/hashes are not comprehension certification.",
            "claudeReadDepth": "All resources directly returned serially. Final report discloses resources1-21 were summarized out of context and relies on its original per-turn observations; resources22-29 inspected directly in final context. Original observations preserved.",
            "gptReadDepth": "All resources directly returned serially; no summary-only subset disclosed in final report. No equal live-context depth or comprehension guarantee.",
        },
        "verdicts": verdicts, "findings": [finding], "actionableRemainingFindings": 0,
        "consequentialUnresolvedScopedClaims": 1, "teachingChanges": [],
        "reconciliation": [
            {"claim": "Actual rendered article/font evidence absent at textual closure.",
             "status": "resolved", "scope": "Both new articles and two changed passages,31Han/fourfamilies and whole准教授 readable in bounded API35 emulator pixels; not physical-phone or fallback-face certification."},
            {"claim": "Readings row unavailable because clipped in one frame.",
             "status": "resolved", "scope": "Signposted horizontal scrolling and complementary left/shifted states collectively expose entire row, not simultaneously all columns."},
            {"claim": "Curated集/進/難 appeared in captured N1 meaning question.",
             "status": "withdrawn", "scope": "Not claimed by reviewers; original coordinator record did not adjudicate actual alternatives. Exact code cause established. No claim captured random alternatives are safe."},
            {"claim": "Potential imitate;emulate overlap and live default-N1 choice safety.",
             "status": "unresolved", "scope": "082-V1; preserve GPTUNVERIFIED and Claude optional disagreement. Original textual teaching closure remains inherited, not full runtime acceptance."},
            {"claim": "Small inline冫, optional extra examples, missing授 link and transient download/loading UX.",
             "status": "optional", "decision": "No content edit. Panels/largeglyphs distinguish冫/氵; received fine inline detail remains limited. 授 card absent mechanically, plain text appropriate. No speculative app fix."},
            {"claim": "Pixels prove import/persistence/tap order/offline or specific fallback face.",
             "status": "partially resolved", "scope": "Destinations consistent with supplied fixture/terminal/route. Not reviewer-executed tests, no fallback-face identification, final-tree loading state retained."},
            {"claim": "Injected tracing and give-up recall prove human recognition or successful recall.",
             "status": "unresolved", "scope": "Not claimed. Ten injected references/shape-only/giveup remain bounded fixture evidence; offline handwriting model unavailable."},
        ],
        "modelContributionComparison": {
            "shared": "No proven prose/rendering defect; all scoped glyph/article passages readable. BOTH observed captured noncurated alternatives and imitation hypothesis, regardless optional versus finding labels.",
            "claudeOnlyVerifiedUseful": "Explicit compressed-history/resources1-21 disclosure and optional fine-inline-radical concern. No unique actionable defect.",
            "gptOnlyVerifiedUseful": "Explicit consequentialUNVERIFIED/publication-gate calibration for shared hypothesis, not unique discovery.",
            "limits": "Compared final/findings/optional/limits/per-turn notes, not model ranking or equal-comprehension claim.",
        },
        "reportQualifications": [
            "Claude's 'only reading' shorthand is source-metadata scoped, not universal; full report preserves that qualification.",
            "Claude's first-rendered-evidence wording mixes prior準largerpool hypothesis with NEW captured准/倣 issue. Preserve reports verbatim; these are distinct underlying claims.",
            "Reports do not independently verify hashes/Git/upstream. Byte delivery is not fresh semantic comprehension.",
        ],
        "independentVisualInspectionComplete": True, "fontInspectionAccepted": True,
        "boundedIndependentVisualConfirmation": False, "runtimeAccepted": False,
        "runtimePublished": False, "nextBatchStarted": False,
        "limits": [
            "Original textual/source/citation/lookup/reading/quiz/baseline limitations inherited, not fresh dictionary verification.",
            "28 resized originalPNGgroups/family, not51 independent captures or128Paint-probe PNG reads; no fallback-face identification.",
            "Claude resources1-21 compressed-history disclosure and both complete original reports/per-turn observations retained.",
            "558HOST3+1+5/no skips,559compile and560two terminal0 native cases inherited, not rerun or proof disputed alternative semantically unique.",
            "Physicalphone/generalrelease/whole-set and final integration/publication/CI/immutableZIP outstanding. 082-V1 unresolved gates publication.",
            "No new emulator/Android run, optional historical session helper, actual permission denial, runtime edit, publication,083 or second runner.",
        ],
        "nextAction": NEXT,
    }
    save(V / "batch-082-visual-reconciliation.json", reconciliation)
    path = S / "batch-082-progress.json"
    ledger = load(path)
    if "preVisual561AcceptanceState" not in ledger:
        ledger["preVisual561AcceptanceState"] = {
            k: ledger[k] for k in ["status", "reviewClosed", "runtimeAccepted",
                                  "independentVisualAcceptance", "nextAction", "limits", "fontDisposition"]}
    ledger.update(
        status=STAGE, independentVisualAcceptance=False, independentVisualInspectionComplete=True,
        runtimeAccepted=False, visualEvidence="docs/n1-reviews/batch-082-visual-reconciliation.json",
        unresolvedRuntimeClaims=["082-V1"],
        fontDisposition="Both original model families inspected31Han/fourfamilies in three Compose panels plus whole准教授;冫/氵/辶/隹 distinguishable. Bounded API35 emulator, not phone or identified fallbackface. Runtime meaning-choice concern separate.",
        nextAction=NEXT, limits=reconciliation["limits"],
    )
    save(path, ledger)
    save(E, {
        **load(LOG / "starting-state-561.json"), "schemaVersion": 1, "checkpoint": 561,
        "status": "continue", "stage": STAGE, "completedAt": v.now(),
        "reconciliation": "docs/n1-reviews/batch-082-visual-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-082-visual-reconciliation.json"),
        "reviewedTeachingSnapshot": v.TEACHING, "evidenceHead": v.HEAD,
        "processes": process, "independentVisualInspectionComplete": True,
        "independentVisualAcceptance": False, "unresolvedRuntimeClaims": ["082-V1"],
        "runtimePublished": False, "runtimeBytesUnchanged": True,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": "1f317f0762513720709ab0ca215f19ff021ca596",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT, "limits": reconciliation["limits"],
    })
    print("Both complete visual reports preserved. 082-V1 unresolved; no publication acceptance.")


def seal():
    v.frozen()
    e = load(E)
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from build_manifest import build_manifest, sha256
    e["mechanicalBatchAudit"] = audit(R, "082")
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
    assert count == 8372
    whitespace = subprocess.run(
        ["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check"],
        capture_output=True, encoding="utf-8")
    assert whitespace.returncode in (0, 2)
    warning_headers = [line for line in whitespace.stdout.splitlines()
                       if line.startswith("docs/") and ": " in line]
    assert all(line.startswith((
        "docs/n1-reviews/batch-082-visual-source-packet.txt:",
        "docs/n1-reviews/batch-082-visual-catalog-execution-561.txt:"))
        for line in warning_headers)
    save(V / "batch-082-visual-whitespace-disposition.json", {
        "execution": 561, "checkExitCode": whitespace.returncode,
        "originalOutput": whitespace.stdout, "warningCount": len(warning_headers),
        "decision": "Preserve exact already-reviewed line-numbered packet (number plus space on source blank lines) and original CLI catalog terminal blank line. No runtime/authored-code whitespace warning, report alteration or production lint exception.",
    })
    receipts = N / "execution-561-receipts"
    receipts.mkdir(exist_ok=True)
    for path in [Path(__file__), C / "review-batch-082-visual.py", C / "post-561-issue.ps1",
                 LOG / "validate-561.txt", LOG / "manifest-561.txt"]:
        shutil.copyfile(path, receipts / path.name)
    e.update(
        runtimePayloadHashesVerified=count, manifestSha256=sha(R / "manifest.json"),
        validatorErrors=0, manifestFresh=True, runtimeBytesUnchanged=True,
        whitespaceDisposition="docs/n1-reviews/batch-082-visual-whitespace-disposition.json",
        validationReceipts=[{"path": str(p.relative_to(R)), "sha256": sha(p)}
                            for p in sorted(receipts.iterdir())],
    )
    save(E, e)
    print("8372 runtime hashes, exact frozen manifest, batch baseline/link/reading audit verified.")


def checkpoint():
    original = load(LOG / "progress-before-561.json")
    p = load(C / "progress.json")
    e = load(E)
    receipt = load(LOG / "issue-response-561.json")
    body = (LOG / "issue-body-561.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.rstrip()
    assert git("rev-parse", "HEAD^") == v.HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not subprocess.check_output(["git", "-C", str(ANDROID), "status", "--porcelain"])
    assert not git("diff", v.HEAD, "HEAD", "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    assert sha(R / "manifest.json") == e["manifestSha256"]
    for r in e["validationReceipts"]:
        assert sha(R / r["path"]) == r["sha256"]
    result = {
        "schemaVersion": 1, "execution": 561, "checkpoint": 561, "batch": "082",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": STAGE, "evidence": "docs/n1-sources/execution-561.json",
        "evidenceSha256": sha(E), "independentVisualInspectionComplete": True,
        "independentVisualAcceptance": False, "unresolvedRuntimeClaims": ["082-V1"],
        "actualModels": [v.SESSIONS[f][0] for f in ["claude", "gpt"]],
        "serialReviewerChildren": 60, "allChildExits": 0, "sourcePacketsPerFamily": 1,
        "originalPngs": 51, "distinctPngGroupsPerFamily": 28,
        "runtimePayloadHashesVerified": 8372, "runtimeBytesUnchanged": True,
        "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 108, "remainingAdditions": 1120,
        "lastPublishedCommit": e["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "originalRootKeyCountCompared": len(original),
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "changedRootFields": ["checkpoint", "status", "stage", "nextAction", "blocker"],
    }
    assert p["checkpoint"] == 560 and p["batch"] == "082"
    p.update(checkpoint=561, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution561StartingState"]["status"] = "signed-local-visual-inspection-checkpoint-complete"
    p["execution561CoordinatorCheckpoint"] = result
    p["batch082VisualExecution561"] = result
    allowed = set(result["changedRootFields"])
    assert all(p[k] == value for k, value in original.items() if k not in allowed)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread[k] == value for k, value in original.items() if k not in allowed)
    save(LOG / "coordinator-checkpoint-561.json", result)
    print(json.dumps({k: result[k] for k in ["checkpoint", "status", "savedCommit", "issueUpdate",
                                           "allOriginalHistoricalRootKeysPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"record": record, "seal": seal, "checkpoint": checkpoint}[sys.argv[1]]()
