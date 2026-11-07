"""Archive actual review execution, reconcile bounded evidence, persist checkpoint."""
import copy
import gzip
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("confirmation715", C / "confirm-batch-097-rendered-715.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
load, save, sha, git = m.load, m.save, m.sha, m.git
R, A, L = m.R, m.A, m.L
G = C / "batch-097-resource-gated-715"
D = R / "docs" / "n1-reviews" / "batch-097-rendered" / "execution-715"
E = R / "docs" / "n1-sources" / "execution-715.json"
STAGE = "batch-097-rendered-confirmed-awaiting-combined-acceptance"
NEXT = (
    "SAME097 combined-current-main acceptance and authorized publication next, only if ALL original gates pass. "
    "Read docs/n1-sources/execution-715.json and docs/n1-reviews/batch-097-rendered/execution-715/reconciliation.json. "
    "Signed LOCAL evidence checkpoint; runtime teaching remains reviewed1fa1ac69/versiona066afceaf1f447a/"
    "8447hashes. Native714 archive83e5c090 through productionContentSync ONCE:1120kanji/5073words/129N1/"
    "zeroProblems/Roomepoch1, BOTH terminalcase0/no skips. Fresh712 JVM4/no skips retained. "
    "Original-session Claude3a0b6dd8 THEN GPT9f31594c resource-gated rendered confirmations accepted: "
    "36 serial exited CLI turns,34 single view calls,32 decoded image returns,zero overlaps in recovery; "
    "each model one bounded text/THREE four-font panels all20Han/13contact sheets all52routecaptures. "
    "Initial715Claude batched attempt29overlaps retained and NOT accepted; its seriality assertion withdrawn. "
    "Font originals1080x2400 returned900x2000; sheets1000x2260 returned885x2000. Not full-resolution evidence. "
    "Both models no actionable defect in two new articles/exact two reused changes/rendered bounded quiz samples. "
    "ActualN1 wronglabels剖/dissect;splitopen,剛/sturdy;unyieldingstrength,蚊/mosquito. TWOcurated available;"
    "ONEfallback蚊,NOT則N2. All64 N1/All/custom/randomN1subset records and512 FOUR directwordguards inspected; "
    "矛/spear;polearm different weapon, not sword. Bounded samples CLEAN, wider custom/random/legacy "
    "semantic safety UNVERIFIED, not whole-pool certification. Bothけん/つるぎGood/Done2of2; exact raw/curation "
    "full+Lite; ten injectedtrace/giveuprecall/persistence NOT humanhandwriting/MLKit. THREEallmappedpairs/"
    "SIXdirections/ONEactivatedbaselinepair/Back/offline/N1selection retained. Glyph刂 visibly renders; "
    "exact fallbackface unidentified. Unusedfrequencyhypothesis remains unresolved/nonconsequential; "
    "optionalpolish declined, no teaching change. QualifiedTESTONLYAndroid1c1b7bf4 retainsproductionf9b59a2,"
    "NOTlatestappmain. Native5580 helpers already stopped; no fresh native run needed absent changes. "
    "Fetch latestorigin/main, nonrewritingmerge if needed, surgical reconciliation/derived regeneration/"
    "independent changed-teaching review, required combinedPython/vocabulary/manifest/baseline/link/membership/"
    "archive/app checks; normal signing/owner fastforward/terminalgreenCI/EVERY immutablepublicZIPentryhash/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue "
    "before counting delivery. Never publish unresolved teaching or claim this local checkpoint published. "
    "Parent19008 owns runner.lock; verifyliveancestry/session/signedheads/whollyclean, NOchildlockoperation. "
    "Approvedcontrol/committedsource only, no optionalhistoricalsessionhelper. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. Published123/1228,1105remaining unchanged; "
    "phone/generalrelease/whole-set outstanding. No098/secondrunner."
)


def collect():
    m.frozen()
    assert not D.exists() and not E.exists()
    summaries = {label: load(G / f"{label}-summary.json") for label in m.MODELS}
    for label, summary in summaries.items():
        assert summary["acceptedExecution"] and len(summary["turns"]) == 18
        turns = summary["turns"]
        for i, t in enumerate(turns):
            assert t["acceptedExecution"] and t["actualModels"] == [m.MODELS[label][0]]
            assert not t["observedToolOverlaps"] and not t["unfinishedTools"]
            assert len(t["toolCalls"]) == (0 if i == 17 else 1)
            assert sha(G / f"{label}-{i:02d}.jsonl") == t["rawSha256"]
            assert sha(G / f"{label}-{i:02d}.md") == t["reportSha256"]
            m.stopped(t)
            if i:
                assert turns[i - 1]["completedAt"] < t["startedAt"]
    assert summaries["claude"]["turns"][-1]["completedAt"] < summaries["gpt"]["turns"][0]["startedAt"]
    runtime = m.runtime()
    assert (R / "kanji" / "口.md").is_file()
    D.mkdir(parents=True)

    def archive(source, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix == ".jsonl":
            target = Path(str(target) + ".gz")
            target.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
            assert gzip.decompress(target.read_bytes()) == source.read_bytes()
        else:
            shutil.copyfile(source, target)
            assert sha(source) == sha(target)

    for source in sorted(G.iterdir()):
        assert source.is_file()
        archive(source, D / "resource-gated" / source.name)
    for source in sorted(C.glob("batch-097-rendered-715-claude.*")):
        archive(source, D / "nonconforming-attempt" / source.name)
    for name in ["batch-097-rendered-715-claude-execution.json",
                 "batch-097-rendered-packet-provenance-715.json",
                 "batch-097-rendered-claude-resources-715.json",
                 "batch-097-rendered-gpt-resources-715.json",
                 "batch-097-rendered-cli-help-715.txt", "batch-097-rendered-cli-config-715.txt"]:
        archive(C / name, D / "preparation" / name)
    for source in sorted(C.glob("batch-097-rendered-*-packet-715-*.txt")):
        archive(source, D / "preparation" / source.name)
    for source in [Path(__file__), C / "confirm-batch-097-rendered-715.py",
                   C / "confirm-batch-097-resource-gated-715.py", m.BASE,
                   C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
                   C / "post-batch-097-rendered-715.ps1"]:
        archive(source, D / "receipts" / source.name)
    review = {
        "schemaVersion": 1, "execution": 715, "batch": "097", "snapshot": m.HEAD,
        "reviewedTeachingSnapshot": "1fa1ac69b88383ef424c0a69d34020ccca83c313",
        "nativeArchiveSnapshot": "83e5c0901a2d080e33b3583da7e0271a6aa329a0",
        "teachingChanged": False, "dependentOriginalSessionConfirmations": True,
        "newBlindInitialReviewCredit": False, "actualModels": [v[0] for v in m.MODELS.values()],
        "originalSessions": {k: v[1] for k, v in m.MODELS.items()},
        "acceptedSerialProcessTurns": 36, "acceptedSingleResourceViewCalls": 34,
        "acceptedDecodedImageReturns": 32, "acceptedToolOverlaps": 0,
        "eachModelScope": {
            "textResources": 1, "fontPanels": 3, "scopedHan": 20, "fontFamilies": 4,
            "contactSheets": 13, "routeCaptures": 52, "kanjiBuilderRecords": 64,
            "directWordGuardRecords": 512, "newArticles": 2, "exactChangedReusedPassages": 2,
            "dictionaryEvidence": "Full initial dictionary reviews inherited; no fresh full-family review claimed.",
        },
        "imageScales": {
            "fontSource": [1080, 2400], "fontReturned": [900, 2000],
            "contactSheetSource": [1000, 2260], "contactSheetReturned": [885, 2000],
            "correction": "Claude report's full-size phrase does not establish original-resolution reading; actual decoded payload sizes govern.",
        },
        "nonconformingAttempt": {
            "model": "claude-opus-5.5", "launcherPid": 1528, "exitCode": 0,
            "toolCalls": 32, "toolOverlaps": 29, "allAssignedResourcesReturned": True,
            "accepted": False,
            "disposition": "Preserved verbatim. Initial in-order/serial assertion contradicted by actual overlapping execution and withdrawn in final report. Recovery exposes one resource per CLI turn; no retroactive serial claim.",
        },
        "verdicts": {
            scope: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "boundedComprehensibility": "CLEAN"}
            for scope in ["kanji/剣.md:1-48", "words/剣.md:1-38", "words/真剣.md:27",
                          "kanji/真.md:37", "rendered routes/glyphs/64kanji+512word sample"]
        },
        "findings": [],
        "reconciliation": [
            {"claim": "No native/font/rendered or actual-choice evidence at initial textual review.",
             "status": "resolved", "scope": "Native714 receipt plus actual decoded captures and bounded records; not physical phone or whole-pool safety."},
            {"claim": "刀/刃 overlap through wider or legacy fallback.",
             "status": "partially resolved", "scope": "Four direct wordguards and observed options pass; wider/legacy pool safety remains UNVERIFIED. Claude resolved wording is restricted to that actual bounded sample, not a universal waiver."},
            {"claim": "Standaloneけん may be more common thanつるぎ.",
             "status": "unresolved", "severity": "nonconsequential unused frequency hypothesis",
             "decision": "No frequency claim adopted; both attested readings remain taught. No new corpus assertion."},
            {"claim": "口 link target not independently checked by Claude.",
             "status": "resolved", "evidence": "Actual kanji/口.md exists; original independent inspection limitation retained."},
            {"claim": "Reading table initially clipped on right.",
             "status": "resolved", "evidence": "Advertised sideways scroll and complementary captures expose full text."},
            {"claim": "Small mark below sticky header in kanji-25 capture.",
             "status": "optional", "decision": "Coordinator inspected original-resolution input; a clipped residual mark is visible at scroll boundary, without loss of teaching or an established content defect. No unrelated UI change."},
            {"claim": "Original optional register/zoological-gloss/clock-hand/historical-form expansion.",
             "status": "optional", "decision": "Declined; original textual reconciliation remains applicable. No unsupported frequency or scope expansion."},
            {"claim": "積極的/proactive and矛/spear appear among sampled alternatives.",
             "status": "resolved", "evidence": "Both models establish no answer equivalence to earnest/serious or sword in the actual supplied labels. Related attitudes/weapons alone are not duplicate answers."},
        ],
        "modelContributionComparison": {
            "shared": "Both inspected same bounded text, all three panels and thirteen sheets, exact64/512 records, both readings, links and drawing limits; neither established an actionable content defect.",
            "uniqueVerifiedActionableFindings": {"claude": [], "gpt": []},
            "claudeOnlyNonblocking": "Cosmetic residual mark and積極的 watch item; optional original expansion retained.",
            "limits": "Dependent rendered confirmations, not blind initial reviews or model benchmark. Source retrieval/Git/terminal output verification remains coordinator evidence.",
        },
        "boundedSemanticAcceptance": "CLEAN", "wholePoolSemanticAcceptance": "UNVERIFIED",
        "renderedConfirmationsClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "limits": [
            "API35 emulator/default fontScale1; physical-phone/general-release acceptance outstanding.",
            "Actual image payloads are resized; contact sheets reduced scale. Hashes prove delivery, not comprehension.",
            "Fallback刂 is visible; exact fallback font face unidentified. Font stylistic刃 variation does not change underlying code point.",
            "No new reviewer-run native/JVM tests; two terminal cases/no skips inherited from714 and JVM4 from712.",
            "GPT final report correctly states terminal instrumentation logs were not exposed in its bounded text; coordinator714 verification is separate evidence.",
            "Ten injected strokes/give-up/shape-only feedback are not human-handwriting or MLKit acceptance.",
            "Static route endpoints plus supplied instrumentation assertions, not independent gesture observation.",
            "Wider custom/random/legacy pools not certified;64/512 samples are not a universal semantic gate.",
            "Initial dictionaries, source qualifications and raw metadata inherited; no new native-speaker or measured-learning claim.",
        ],
    }
    save(D / "reconciliation.json", review)
    progress = load(C / "progress.json")
    evidence = {
        "schemaVersion": 1, "execution": 715, "batch": "097", "status": STAGE,
        "startingState": copy.deepcopy(progress["execution715StartingState"]),
        "snapshot": m.HEAD, "reviewedTeachingSnapshot": review["reviewedTeachingSnapshot"],
        "nativeSnapshot": review["nativeArchiveSnapshot"], "runtime": runtime,
        "renderedConfirmations": review, "nativeTestsRerun": False, "androidTestsRerun": False,
        "nativeAcceptanceEvidence": "docs/n1-sources/execution-714.json",
        "freshJvmEvidence": "docs/n1-sources/execution-712.json",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False, "publishedAdditions": 123,
        "remainingAdditions": 1105, "lastPublishedCommit": progress["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    }
    save(E, evidence)
    packet = R / "docs" / "n1-sources" / "batch-097-progress.json"
    batch = load(packet)
    batch["status"] = STAGE
    batch["renderedConfirmation715"] = {
        "evidence": str(E.relative_to(R)).replace("\\", "/"),
        "reconciliation": str((D / "reconciliation.json").relative_to(R)).replace("\\", "/"),
        "renderedConfirmationsClosed": True, "boundedSemanticAcceptance": "CLEAN",
        "wholePoolSemanticAcceptance": "UNVERIFIED", "runtimeAccepted": False, "published": False,
        "originalSessions": review["originalSessions"], "newBlindInitialReviewCredit": False,
        "nonconformingAttemptPreserved": True,
    }
    batch["limits"].append("Execution715 closes bounded two-family rendered confirmation only; combined-main acceptance/signing/publication/CI/exact public ZIP still pending. Native714 and fresh712 JVM evidence retained; original limitations remain historical.")
    save(packet, batch)
    index = [{"path": str(p.relative_to(R)).replace("\\", "/"), "sha256": sha(p)}
             for p in sorted(D.rglob("*")) if p.is_file()]
    save(D / "artifact-index.json", index)
    subprocess.run(["git", "-C", str(R), "diff", "--check"], check=True)
    print("Archived both accepted resource-gated confirmations and original nonconforming attempt; runtime unchanged.")


def issue():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == m.HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    body = (
        "Batch097 bounded rendered checkpoint715: original-session Claude Opus5.5 then GPT-6.1Sol "
        "confirmed both new articles and exact two reused changes; no actionable defect established. "
        "Both inspected all20Han/fourfonts/three panels,52routecaptures via13sheets,64 exact kanji and512 "
        "four-direct-wordguard records. These are dependent confirmations, not new blind review credit.\n\n"
        "Initial Claude attempt issued29 overlapping view calls and is preserved NOT accepted; recovery "
        "used36 serial exited CLI turns with exactly34 single-resource reads/32 decoded images/zero "
        "tool overlaps. Resized payloads/contact-sheet limits are recorded. Original full dictionaries "
        "and two-family initial review remain inherited. Actual N1 fallback is mosquito, not N2則; "
        "sampled spear/polearm is not sword. Bounded semantic sample CLEAN, wider/custom/random/legacy "
        "pools UNVERIFIED. No universal safety claim.\n\n"
        f"Normally signed LOCAL evidence commit `{head}`; teaching1fa1ac69/versiona066afceaf1f447a/"
        "8447 runtime hashes unchanged. Native714 full-import/two terminalcase0 and fresh712 JVM4 "
        "retained, not rerun. No publication or batch098. Published123/1228,1105 remaining unchanged; "
        "phone/general-release/whole-set outstanding. Next: combined-current-main acceptance, normal "
        "owner publication only after all original CI/immutable-ZIP/hash/budget gates. "
        "Parent runner lock untouched; no new permission denial or historical-session helper access.\n\n"
        "Evidence: `docs/n1-sources/execution-715.json` and "
        "`docs/n1-reviews/batch-097-rendered/execution-715/reconciliation.json`."
    )
    (C / "batch-097-rendered-715-issue-body.txt").write_text(body, encoding="utf-8")
    print(head)


def seal_whitespace():
    result = subprocess.run(["git", "--no-pager", "-C", str(R), "diff", "--cached", "--check"],
                            capture_output=True, encoding="utf-8")
    assert result.returncode == 2
    output = result.stdout + result.stderr
    diagnostics = D / "initial-whitespace-diagnostic.txt.gz"
    diagnostics.write_bytes(gzip.compress(output.encode("utf-8"), mtime=0))
    names = sorted({line.split(":")[0] for line in output.splitlines()
                    if line.startswith("docs/")})
    packed = []
    for name in names:
        source = R.joinpath(*name.split("/"))
        assert D in source.parents and source.suffix == ".txt"
        target = Path(str(source) + ".gz")
        assert source.is_file() and not target.exists()
        data = source.read_bytes()
        target.write_bytes(gzip.compress(data, mtime=0))
        assert gzip.decompress(target.read_bytes()) == data
        packed.append({"originalPath": name, "originalSha256": sha(source),
                       "archive": str(target.relative_to(R)).replace("\\", "/"),
                       "archiveSha256": sha(target)})
        source.unlink()
    disposition = {
        "initialCheckExitCode": result.returncode,
        "reason": "Numbered blank source lines and exact diff-context bytes retain trailing spaces. No signing command ran because the chained whitespace check stopped first.",
        "disposition": "Lossless deterministic gzip preserves exact reviewer-visible bytes, rather than normalizing evidence or waiving the check.",
        "packed": packed, "originalDiagnostic": diagnostics.name,
        "teachingChanged": False, "runtimeChanged": False,
    }
    save(D / "whitespace-disposition.json", disposition)
    evidence = load(E)
    evidence["evidencePackagingDiagnostic"] = disposition
    save(E, evidence)
    shutil.copyfile(Path(__file__), D / "receipts" / Path(__file__).name)
    index = [{"path": str(p.relative_to(R)).replace("\\", "/"), "sha256": sha(p)}
             for p in sorted(D.rglob("*")) if p.is_file() and p.name != "artifact-index.json"]
    save(D / "artifact-index.json", index)
    print("Losslessly packed", len(packed), "immutable whitespace-bearing evidence files.")


def checkpoint():
    p = load(C / "progress.json")
    original = load(L / "progress-before-715.json")
    assert p["checkpoint"] == original["checkpoint"] == 714
    m.prior.ownership()
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == m.HEAD and git("log", "-1", "--format=%G?") == "G"
    for repo in [R, A]:
        assert not git("status", "--porcelain", "--untracked-files=all", repo=repo)
    assert git("rev-parse", "HEAD", repo=A) == m.APP
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    paths = git("diff", "--name-only", m.HEAD, head).splitlines()
    assert all(n.startswith(("docs/n1-reviews/batch-097-rendered/execution-715/",
                             "docs/n1-sources/execution-715.json",
                             "docs/n1-sources/batch-097-progress.json")) for n in paths)
    assert not git("diff", m.HEAD, head, "--", "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    for row in load(D / "artifact-index.json"):
        assert sha(R.joinpath(*row["path"].split("/"))) == row["sha256"]
    m.runtime()
    receipt = load(C / "batch-097-rendered-715-issue-receipt.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (C / "batch-097-rendered-715-issue-body.txt").read_text(encoding="utf-8")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in original.items() if k not in mutable)
    record = {
        "schemaVersion": 1, "execution": 715, "checkpoint": 715, "batch": "097",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "evidence": "docs/n1-sources/execution-715.json",
        "independentRenderedConfirmations": "closed-dependent-original-sessions",
        "actualModels": [v[0] for v in m.MODELS.values()],
        "acceptedSerialProcessTurns": 36, "acceptedSingleResourceViewCalls": 34,
        "decodedImageReturns": 32, "acceptedToolOverlaps": 0,
        "nonconformingClaudeAttemptOverlaps": 29, "nonconformingAttemptAccepted": False,
        "boundedSemanticAcceptance": "CLEAN", "wholePoolSemanticAcceptance": "UNVERIFIED",
        "runtimeHashesVerifiedAgain": 8447, "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "nativeTestsRerun": False, "androidTestsRerun": False,
        "publishedAdditions": 123, "remainingAdditions": 1105,
        "lastPublishedCommit": original["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(original), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT, "checkpointHelper": str(Path(__file__)), "checkpointHelperSha256": sha(Path(__file__)),
    }
    p.update(checkpoint=715, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution715CoordinatorCheckpoint"] = record
    p["batch097RenderedConfirmationCheckpoint"] = copy.deepcopy(record)
    m.persist(p)
    saved = load(C / "progress.json")
    assert all(saved[k] == value for k, value in original.items() if k not in mutable)
    save(L / "checkpoint-715-verification.json", record)
    print(json.dumps({"checkpoint": 715, "savedCommit": head, "historyPreserved": True,
                      "issueUpdate": receipt["html_url"]}, indent=2))


if __name__ == "__main__":
    {"collect": collect, "issue": issue, "seal-whitespace": seal_whitespace,
     "checkpoint": checkpoint}[sys.argv[1]]()
