"""Persist reconciled rendered evidence while preserving all project history."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("rendered695", C / "confirm-batch-095-rendered-695.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R, V, L = m.R, m.V, m.L
E = R / "docs" / "n1-sources" / "execution-695.json"
REVIEW = V / "batch-095-rendered-reconciliation-695.json"
STAGE = "rendered-confirmed-awaiting-combined-main-acceptance"
NEXT = (
    "SAME095 combined-current-main acceptance next; read docs/n1-sources/execution-695.json and "
    "docs/n1-reviews/batch-095-rendered-reconciliation-695.json. "
    "Original-session Claude ede78c28-e889-47b5-be0b-21533da61551 and GPT "
    "ee7498e0-d3ad-46bf-bbc9-82761892cab0 rendered confirmations complete; NOT fresh blind credit. "
    "OriginalClaude695 panels1+2 overlap remains REJECTED for strict serial execution forever; "
    "accepted smallest THREE-read serial repair preserves all other historical observations. "
    "GPT read all14chunks/18assignedimages plus originalkai11 serially; no overlaps/unfinishedtools. "
    "No actionable defect or consequential unresolved claim in assigned teaching/rendered/bounded "
    "64kanji/384three-directwordguard samples; untested seeds/pools remain UNVERIFIED. "
    "H1 missing1199270 from existing解 citation line adjudicated OPTIONAL: new navigation links "
    "fullysourced解剖 article, no per-listword duplicatecitation requirement; no runtime edit. "
    "All32Han/fourfonts/60originalPNG/two reciprocalpairs/fourdirections/zeroactivatedbaselinepairs "
    "and onlyonぼう/noKun/teninjectedstrokes/Back/offline inherited694; two terminalcase0/no skips. "
    "Exact fullarchivecc748347/version463619d79972e9f2/8441hashes/1118kanji5071words127N1/"
    "zeroProblems/Roomepoch1 through productionContentSyncONCE; owned5580 stopped. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain; fresh692 JVM4/no skips. "
    "Fetch latestoriginmain (da374717 at695), normal NONREWRITING merge into content/n1-kanji, "
    "surgical conflict resolution preserving newer main and approved teaching/sourcebaselines; "
    "regenerate derived manifest, independently review ANY substantive changed teaching/overlap. "
    "Run ALL required applicable combined-tree validate/build_manifest/Python/vocabulary/"
    "baseline+membership+reading+stroke+allmappedlinks/font/archivebudget and non-skipped Android "
    "RealContentTest/RareHan checks. Inspect actual test reports; do not relabel old native archive "
    "as a changed combined manifest import. Decide exact changed-native scope by actual merged diff. "
    "No publication until combined-tree acceptance and normally signed reviewclosed evidence; "
    "normal ownerfastforward to origin/main, handle mainadvance with remerge/revalidate; verify "
    "remoteSHA/terminalgreenCI/EVERY immutable publicZIP runtimeentryhash/unchanged18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue. "
    "Preserve exact authored/reviewed/integrated/publishedSHAs. Parent19008 retainsrunner.lock: "
    "verify liveancestry/session/signedheads/whollyclean, NOchild acquire/delete/unlock. "
    "Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper access. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Published121/1228,1107remaining unchanged; physicalphone/generalrelease/whole-set outstanding. "
    "No096/runtimepublication/secondrunner at695."
)


def stopped(record):
    subprocess.run(["pwsh", "-NoProfile", "-Command",
                    f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                   capture_output=True, check=True)


def update_packet():
    path = R / "docs" / "n1-sources" / "batch-095-progress.json"
    text = path.read_text(encoding="utf-8")
    current = json.loads(text)
    current["status"] = STAGE
    current["nextAction"] = NEXT
    current["pendingGates"] = [
        "Rendered695 bounded confirmation complete; combined-current-main normal merge, changed-teaching review if needed and all applicable combined-tree acceptance checks remain.",
        "Normally signed reviewclosed evidence, ownerfastforward, terminalgreenCI, EVERYimmutablepublicZIPentryhash, originalbudgets and verifiedownerissue; no batch096 before public acceptance.",
    ]
    current["androidAcceptance"]["nativeAcceptance"] = "execution694-native-and695-bounded-rendered-confirmed"
    decoder = json.JSONDecoder()
    for key in ["status", "nextAction", "pendingGates", "androidAcceptance"]:
        match = re.search(r'^  "' + key + r'": ', text, re.MULTILINE)
        assert match
        _, end = decoder.raw_decode(text, match.end())
        value = json.dumps(current[key], ensure_ascii=False, indent=2).replace("\n", "\n  ")
        text = text[:match.end()] + value + text[end:]
    current["renderedConfirmation695"] = {
        "evidence": E.relative_to(R).as_posix(), "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "status": STAGE, "newBlindInitialReviewCredit": False, "runtimeChanged": False,
        "originalClaudeOverlapPreservedRejected": True, "smallestSerialRepairAccepted": True,
        "gptSerialExecutionAccepted": True, "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "boundedSampleSemanticVerdict": "CLEAN",
        "untestedSeedsAndPools": "UNVERIFIED", "runtimeAccepted": False, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier pending fields are historical. This additive record supersedes the pending rendered gate only, not combined-tree acceptance or publication.",
    }
    end = text.rfind("}")
    extra = json.dumps({"renderedConfirmation695": current["renderedConfirmation695"]},
                       ensure_ascii=False, indent=2)[1:-1]
    text = text[:end].rstrip() + "," + extra + "\n" + text[end:]
    assert json.loads(text) == current
    path.write_text(text, encoding="utf-8", newline="")


def archive():
    m.frozen()
    runtime = m.runtime()
    names = ["claude", "claude-serial-repair", "gpt"]
    records = [m.load(C / f"batch-095-rendered-695-{name}-execution.json") for name in names]
    original, repair, gpt = records
    assert not original["acceptedExecution"] and len(original["observedToolOverlaps"]) == 1
    assert len(original["actualDecodedImageReturns"]) == 18
    assert set(original["requiredResources"]) == set(original["successfullyReturnedResources"])
    assert repair["acceptedExecution"] and len(repair["toolCalls"]) == 3
    assert len(repair["actualDecodedImageReturns"]) == 2
    assert gpt["acceptedExecution"] and len(gpt["actualDecodedImageReturns"]) == 19
    assert original["completedAt"] < repair["startedAt"] < repair["completedAt"] < gpt["startedAt"]
    for record in records:
        assert record["exitCode"] == 0 and not record["unfinishedTools"]
        stopped(record)
    receipts = []
    sources = [Path(__file__), C / "confirm-batch-095-rendered-695.py",
               C / "confirm-batch-095-rendered-695-original.py",
               C / "post-batch-095-rendered-695.ps1",
               C / "batch-095-rendered-packet-provenance-695.json",
               L / "runtime-preflight-695.json"]
    sources += [C / f"batch-095-rendered-cli-{kind}-695.txt" for kind in ["help", "config"]]
    packed = []
    for label in ["claude", "gpt"]:
        resource = C / f"batch-095-rendered-{label}-resources-695.json"
        sources.append(resource)
        packed += [Path(p) for p in m.load(resource) if p.endswith(".txt")]
    for name, record in zip(names, records):
        prefix = C / f"batch-095-rendered-695-{name}"
        raw = prefix.with_suffix(".jsonl")
        assert m.sha(raw) == record["rawSha256"]
        assert m.sha(prefix.with_suffix(".md")) == record["reportSha256"]
        packed.append(raw)
        sources += [prefix.with_suffix(s) for s in [
            ".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"]]
        sources.append(C / f"{prefix.name}-execution.json")
    for source in packed:
        target = V / (source.name + ".gz")
        assert not target.exists()
        target.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
        assert gzip.decompress(target.read_bytes()) == source.read_bytes()
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": m.sha(source), "archiveSha256": m.sha(target), "losslessGzip": True})
    for source in sources:
        target = V / source.name
        assert not target.exists(), str(target)
        shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": m.sha(source), "archiveSha256": m.sha(target)})
    evidence = {
        "schemaVersion": 1, "execution": 695, "batch": "095", "status": STAGE,
        "reviewedSnapshot": m.HEAD, "reviewedTeachingSnapshot": "8c4e16500d57749f90f08c196fbb8980981967a6",
        "nativeReceipt": "docs/n1-sources/execution-694.json",
        "dependentOriginalSessionRecords": [
            f"docs/n1-reviews/batch-095-rendered-695-{name}-execution.json" for name in names],
        "newBlindInitialReviewCredit": False, "runtime": runtime,
        "processDisposition": {
            "originalClaude": "Rejected for strict serial execution: panels1+2 overlapped; complete original report/raw/execution retained.",
            "serialRepair": "Three complete serial views: own report, panel1, panel2. Fresh dependent observations only; never retroactively labels original execution compliant.",
            "gpt": "Complete original-session rendered evidence review; serial reads and actual PNG payload delivery audited, including one additional original table capture.",
            "reviewerProcessesLaunched": 3, "atMostOneActiveReviewerVerified": True,
            "originalOverlapNeverRelabeledCompliant": True,
            "allOtherOriginalClaudeReadsSerial": True,
            "claudeTextSizeRefusalRecovered": True, "gptTextSizeRefusalRecovered": True,
        },
        "reconciliation": [{
            "id": "095-added-navigation-citation-line", "status": "optional", "severity": "nonblocking",
            "facet": "provenance/scoped coverage", "file": "kanji/解.md:39,50",
            "claim": "New linked 解剖 is not repeated as entry1199270 in existing 解 article's final vocabulary citation list.",
            "reportedBy": "Claude dependent695 H1, low confidence; not a blind initial discovery.",
            "decision": "No edit. The navigation points to the fully sourced 解剖 article, whose final line explicitly cites1199270/1199280 and Daijisen. Required per-occurrence lexical/allocation evidence is committed and reviewed. No format rule requires duplicating every linked support word's entry ID in an existing navigation-only article's citation list. No false citation or contradicted lexical claim established.",
            "evidence": ["Current kanji/解.md:39,50", "Current words/解剖.md:39",
                         "Complete batch095 JMdict1199270 and source/review ledgers",
                         "Content-format kanji/word and source requirements"],
            "confidence": "High that this is optional provenance polish, not a consequential unresolved teaching claim.",
        }],
        "facetVerdicts": {
            key: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"}
            for key in ["kanji/剖.md:1-46", "words/解剖.md:1-39", "kanji/解.md:39",
                        "boundedRenderedEvidence", "bounded64KanjiChoices", "threeDirectWordGuards384Records"]
        },
        "boundedSemanticAdjudication": {
            "defaultN1": "剖/dissect;split open versus 冒/brave danger;venture,刈/mow;reap,企/plan;undertake. Cutting/harvesting vegetation is not dissecting/splitting open; venturing/planning likewise not competing answers.",
            "curatedAvailability": "Zero in N1 because 部N3/倍N2/副N2 are excluded; three actual production fallbacks retained and inspected. All/custom contain the preserved curated labels.",
            "kanjiRecords": "All64 exact records across16seeds/fourpools reviewed. Closest ordinary related concepts 刃blade/cutting edge,削shave/sharpen/pare and偵covert investigation do not establish equivalents for dissect/split open. Others concern roles, ranks, objects, plants/animals or different actions; no demonstrated competing answer.",
            "wordRecords": "All384 exact records preserve three direct guards across two directions/two targetorientations/All+custom/16seeds. 解剖-target samples have 解決/解放/解答/解説/解散/輸血 and unrelated kana controls: solution, release, answer, explanation, dissolution and blood transfusion are not ordinary substitutes for dissection/autopsy/detailed analysis. No new precise consequential ambiguous displayed option established.",
            "priorHypotheses": "Earlier clinical診察/調査 concerns remain evidence-based withdrawn/not established, not universally disproved by nonoccurrence in these samples. 解体 card remains absent. Original source/review qualifications preserved.",
            "scope": "Bounded actual records CLEAN, not exhaustive semantic certification of all word options or untested seeds/pools.",
            "untestedSeedsAndPools": "UNVERIFIED",
        },
        "renderedDisposition": "Both model families' dependent observations support no actionable visual defect in FOURfontpanels/all32Han and14contactsheets/all56routePNGs. Exact fallback font face NOT identified; visible components recognizable. GPT additionally opened originalkai11 to distinguish wrapping from clipping.",
        "optional": [
            "Initial Claude suggestions (to examine it wording, extra recognition-only剖検, short gloss consistency) remain optional with original evidence-based no-edit dispositions.",
            "GPT's new narrow English-table-cell wrapping observation is nonblocking app polish in unchanged 解 table, not a content rewrite or app task.",
        ],
        "modelContributionComparison": {
            "shared": "Both confirm scoped glyph distinctions, source-qualified prose/reading tables/navigation and actual fallback semantics; both consider blade/shaving/investigation relations and the three direct guards. No unique verified mandatory defect.",
            "claudeUniqueNonblocking": "H1 optional repeated citation ID hypothesis; no established source gap.",
            "gptUniqueNonblocking": "Additional originalkai11 screenshot distinguishes narrow English wrapping from clipping.",
            "limits": "Dependent followups, not new blind discovery or general model benchmark. Full returned payloads are not comprehension certification.",
        },
        "actionableRemainingFindings": 0, "consequentialUnresolvedInScopeClaims": 0,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "limits": [
            "Original Claude overlapping panels rejected; only the two observations re-obtained in accepted serial repair. Original run never rebranded compliant.",
            "Contact sheets reduced and PNG returns may be resized; dimensions and returned hashes retained. Exact fallback face not identified.",
            "Native694 results inherited, not rerun here. Static images rely on coordinator receipts for interactions/offline/persistence.",
            "No new blind initial review, independent upstream retrieval, native-speaker certification or measured learning effectiveness.",
            "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, not latest app main; ten injected strokes/give-up recall are not human handwriting/MLKit.",
            "Physical-phone/general-release and whole-set outstanding. Current-main integration/combined acceptance and public ZIP/CI still pending.",
        ],
        "nextAction": NEXT,
    }
    m.save(REVIEW, evidence)
    update_packet()
    m.save(E, {
        "schemaVersion": 1, "execution": 695, "batch": "095", "status": STAGE,
        "startingState": m.load(C / "progress.json")["execution695StartingState"],
        "reviewRecord": REVIEW.relative_to(R).as_posix(), "receipts": receipts, "runtime": runtime,
        "originalSessionReviewerProcesses": 3, "atMostOneReviewerActive": True,
        "originalClaudeOverlapPreservedRejected": True, "smallestSerialRepairAccepted": True,
        "gptSerialExecutionAccepted": True, "newBlindInitialReviewCredit": False,
        "actionableRemainingFindings": 0, "consequentialUnresolvedInScopeClaims": 0,
        "boundedSampleSemanticVerdict": "CLEAN", "untestedSeedsAndPools": "UNVERIFIED",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 121, "remainingAdditions": 1107,
        "lastPublishedCommit": "d6a261903f269d6223afc067815b02c595da41a3",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Complete reports, original rejected overlap, accepted serial repair and reconciliation archived.")


def finalize():
    m.ownership()
    assert m.git("rev-parse", "HEAD^") == m.HEAD
    assert m.git("log", "-1", "--format=%G?") == "G"
    for repo in [R, m.A]:
        assert not m.git("status", "--porcelain", "--untracked-files=all", repo=repo)
    assert m.git("rev-parse", "HEAD", repo=m.A) == m.APP
    assert m.git("log", "-1", "--format=%G?", repo=m.A) == "G"
    runtime = m.runtime()
    assert not m.git("diff", m.HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = m.load(E)
    expected = {r["archive"] for r in evidence["receipts"]} | {
        E.relative_to(R).as_posix(), REVIEW.relative_to(R).as_posix(), "docs/n1-sources/batch-095-progress.json"}
    changed = m.git("diff", "--name-only", m.HEAD, "HEAD").splitlines()
    assert set(changed) == expected
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert m.sha(path) == row["archiveSha256"]
        if row.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == row["sourceSha256"]
    prefix = C / "batch-095-rendered-695-issue-"
    body = Path(str(prefix) + "body.txt").read_text(encoding="utf-8-sig")
    receipt, posted = m.load(Path(str(prefix) + "receipt.json")), m.load(Path(str(prefix) + "posted.json"))
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = m.load(C / "progress.json"), m.load(L / "progress-before-695.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 695, "checkpoint": 695, "batch": "095",
        "savedCommit": m.git("rev-parse", "HEAD"), "signature": "G",
        "status": "continue", "stage": STAGE, "evidence": E.relative_to(R).as_posix(),
        "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "originalSessionReviewerProcesses": 3, "allReviewerProcessesExited": True,
        "originalClaudeOverlapPreservedRejected": True, "smallestSerialRepairAccepted": True,
        "gptSerialExecutionAccepted": True, "newBlindInitialReviewCredit": False,
        "actionableRemainingFindings": 0, "consequentialUnresolvedInScopeClaims": 0,
        "boundedSampleSemanticVerdict": "CLEAN", "untestedSeedsAndPools": "UNVERIFIED",
        **runtime, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 121, "remainingAdditions": 1107,
        "lastPublishedCommit": "d6a261903f269d6223afc067815b02c595da41a3",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    state.update(checkpoint=695, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution695CoordinatorCheckpoint"] = checkpoint
    state["batch095RenderedReviewCheckpoint"] = checkpoint
    state["execution695StartingState"]["status"] = "signed-local-rendered-review-checkpoint-complete"
    m.persist(state)
    reread = m.load(C / "progress.json")
    assert all(reread[k] == v for k, v in before.items() if k not in allowed)
    m.save(L / "checkpoint-695.json", checkpoint)
    print("Checkpoint695 persisted; all", len(before), "original historical root values preserved.")
    print(checkpoint["savedCommit"], checkpoint["issueUpdate"])


if __name__ == "__main__":
    if sys.argv[1] == "archive":
        archive()
    elif sys.argv[1] == "finalize":
        finalize()
