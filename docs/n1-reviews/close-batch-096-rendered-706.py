"""Archive bounded rendered review and preserve the complete project checkpoint."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("rendered706", C / "confirm-batch-096-rendered-706.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R, V, L = m.R, m.V, m.L
E = R / "docs" / "n1-sources" / "execution-706.json"
REVIEW = V / "batch-096-rendered-reconciliation-706.json"
STAGE = "rendered-confirmed-awaiting-combined-main-acceptance"
NEXT = (
    "SAME096 combined-current-main acceptance next; read docs/n1-sources/execution-706.json and "
    "docs/n1-reviews/batch-096-rendered-reconciliation-706.json. Original-session Claude "
    "de7596b6-1f69-43e0-b297-c3e600fa712a THEN GPT ca536738-97f2-4841-b985-321ce12b37c1 "
    "rendered confirmations complete, both actual model identities verified; NOT new blind credit. "
    "Each process exited0 before the next, each36 serialviews:22complete textchunks+14decodedPNG "
    "(FOURfontpanels/all28Han+TENcontactsheets/all37otherPNG), no overlap/unfinished/missingread. "
    "No actionable defect or consequential unresolved claim in assigned teaching/rendered/bounded "
    "64kanji/1536twelve-directwordguard samples; untested seeds/pools/all-otherword-options remain "
    "UNVERIFIED. ActualdefaultN1:剛strength vs剖dissect/splitopen,削shave/sharpen/pare,儒Confucian/scholar; "
    "TWOcurated/ONEfallback, not allthreecurated. Sampled克overcome related, not synonymous. "
    "Soleonごう/noKun, TWOarticles/ONEreciprocalpair/TWOdirections/ZEROactivatedbaselinepairs/Back/offline/"
    "teninjectedstrokes inherited705;2 terminalcase0/no skips. Exactfullarchive58129f19/version54645b95fe8e939c/"
    "8444hashes/1119kanji5072words128N1/zeroProblems/Roomepoch1 through productionContentSyncONCE; "
    "owned5580 stopped. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain; "
    "fresh703 JVM4/no skips. Fetch latestoriginmain, normal NONREWRITING merge into content/n1-kanji, "
    "surgical conflictresolution preserving newer main/sourcebaseline; regenerate derived manifest, "
    "independently review ANY substantive changed teaching/overlap. Run ALL required applicable combined-tree "
    "validate/build_manifest/Python/vocabulary/baseline+membership+reading+stroke+allmappedlinks/font/"
    "archivebudget and non-skipped AndroidRealContentTest/RareHan checks. Inspect actual test reports; "
    "do not relabel old nativearchive as a changed combinedmanifest import. Decide exact changed-native "
    "scope from actual merged diff. No publication until combined-tree acceptance and normallysigned "
    "reviewclosed evidence; normal ownerfastforward to origin/main, handle mainadvance with remerge/"
    "revalidate; verify remoteSHA/terminalgreenCI/EVERYimmutablepublicZIPruntimeentryhash/unchanged"
    "18000entries/42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue. "
    "Preserve exact authored/reviewed/integrated/publishedSHAs. Parent19008 retainsrunner.lock: verify "
    "liveancestry/session/signedheads/whollyclean, NOchild acquire/delete/unlock/readprobe. "
    "Approvedcontrol/committedpackets only; no optionalhistoricalsessionhelper. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. Published122/1228,1106remaining unchanged; "
    "physicalphone/generalrelease/whole-set outstanding. No097/runtimepublication/secondrunner at706."
)


def update_packet():
    path = R / "docs" / "n1-sources" / "batch-096-progress.json"
    text = path.read_text(encoding="utf-8")
    current = json.loads(text)
    current["status"] = STAGE
    current["nextAction"] = NEXT
    current["pendingGates"] = [
        "Rendered706 bounded confirmation complete; combined-current-main normal merge, changed-teaching review if needed and all applicable combined-tree acceptance checks remain.",
        "Normally signed reviewclosed evidence, ownerfastforward, terminalgreenCI, EVERYimmutablepublicZIPentryhash, originalbudgets and verifiedownerissue; no097 before public acceptance.",
    ]
    current["androidAcceptance"]["nativeAcceptance"] = "execution705-native-and706-bounded-rendered-confirmed"
    decoder = json.JSONDecoder()
    for key in ["status", "nextAction", "pendingGates", "androidAcceptance"]:
        match = re.search(r'^  "' + key + r'": ', text, re.MULTILINE)
        assert match
        _, end = decoder.raw_decode(text, match.end())
        value = json.dumps(current[key], ensure_ascii=True, indent=2).replace("\n", "\n  ")
        text = text[:match.end()] + value + text[end:]
    current["renderedConfirmation706"] = {
        "evidence": E.relative_to(R).as_posix(), "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "status": STAGE, "newBlindInitialReviewCredit": False, "runtimeChanged": False,
        "claudeSerialExecutionAccepted": True, "gptSerialExecutionAccepted": True,
        "actionableRemainingFindings": 0, "consequentialUnresolvedInScopeClaims": 0,
        "boundedSampleSemanticVerdict": "CLEAN", "untestedSeedsAndPools": "UNVERIFIED",
        "runtimeAccepted": False, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier pending fields are historical. This additive record supersedes the pending rendered gate only, not combined-tree acceptance or publication.",
    }
    end = text.rfind("}")
    extra = json.dumps({"renderedConfirmation706": current["renderedConfirmation706"]},
                       ensure_ascii=True, indent=2)[1:-1]
    text = text[:end].rstrip() + "," + extra + "\n" + text[end:]
    assert json.loads(text) == current
    path.write_text(text, encoding="utf-8", newline="")


def archive():
    m.frozen()
    runtime = m.runtime()
    records = [m.load(C / f"batch-096-rendered-706-{label}-execution.json") for label in m.MODELS]
    assert records[0]["completedAt"] < records[1]["startedAt"]
    for record in records:
        assert record["acceptedExecution"] and record["exitCode"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert len(record["actualDecodedImageReturns"]) == 14
        assert len(record["toolCalls"]) == len(record["requiredResources"]) == 36
        m.stopped(record)
    receipts = []
    sources = [Path(__file__), C / "confirm-batch-096-rendered-706.py",
               C / "post-batch-096-rendered-706.ps1",
               C / "batch-096-rendered-packet-provenance-706.json"]
    sources += [C / f"batch-096-rendered-cli-{kind}-706.txt" for kind in ["help", "config"]]
    packed = []
    for label, record in zip(m.MODELS, records):
        resource = C / f"batch-096-rendered-{label}-resources-706.json"
        sources.append(resource)
        packed += [Path(p) for p in m.load(resource) if p.endswith(".txt")]
        prefix = C / f"batch-096-rendered-706-{label}"
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
        "schemaVersion": 1, "execution": 706, "batch": "096", "status": STAGE,
        "reviewedSnapshot": m.HEAD, "reviewedTeachingSnapshot": "b26bcf9b328872b1575cf89e187973fea0a32a31",
        "nativeReceipt": "docs/n1-sources/execution-705.json",
        "dependentOriginalSessionRecords": [
            f"docs/n1-reviews/batch-096-rendered-706-{label}-execution.json" for label in m.MODELS],
        "newBlindInitialReviewCredit": False, "runtime": runtime,
        "processDisposition": {
            "reviewerProcessesLaunched": 2, "atMostOneActiveReviewerVerified": True,
            "claude": "Accepted original-session dependent confirmation:36 serial views,22 complete text chunks and14 actual decoded PNG payloads, zero overlaps/unfinished/missing reads; process2876 exited0 before GPT launch.",
            "gpt": "Accepted original-session dependent confirmation:36 serial views,22 complete text chunks and14 actual decoded PNG payloads, zero overlaps/unfinished/missing reads; process29012 exited0.",
            "images": "Four original font panels returned900x2000 and10contact sheets returned885x2000; all37other original captures represented at reduced scale. Neither reviewer opened extra original screenshots.",
            "limits": "Actual payload/serial audits establish returned scope, not comprehension. No unrequested parallel nested work.",
        },
        "facetVerdicts": {
            key: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"}
            for key in ["kanji/剛.md:1-48", "words/剛健.md:1-37",
                        "boundedRenderedEvidence", "bounded64KanjiChoices", "twelveDirectWordGuards1536Records"]
        },
        "findings": [],
        "reconciliation": [
            {
                "claim": "Initial possible overlapping strength/hardness fallback options.",
                "status": "partially resolved",
                "decision": "No competing answer in actual default N1 capture or all64 bounded records. Neither 強 nor 硬 appears in these records. Arbitrary untested seeds/pools remain UNVERIFIED, not universally cleared.",
                "evidence": "Exact native705 default options and all64 imported builder rows; both dependent reports.",
            },
            {
                "claim": "Original title uniqueness limitation.",
                "status": "resolved",
                "decision": "Repository structural validator in textual702 already checked corpus title uniqueness; both rendered reviewers assess the sampled choices, not a fresh whole-corpus audit. A semantically overlapping title outside the sample is not ruled out.",
                "evidence": "Preserved batch096-textual-review-validate-702.txt.gz and exact64 native705 records.",
            },
            {
                "claim": "Whether predicate 剛健です requires another attested example.",
                "status": "optional",
                "decision": "No edit. Frozen JMdict classifies 剛健 as noun/na-adjective; the article's copular attachment pattern is supported by that class. No false idiomaticity or frequency claim is made. Additional native-speaker/attested predicate evidence was not obtained; both original textual verdicts remain CLEAN. Extra attested prose is optional enrichment, not a consequential unresolved construction error.",
                "evidence": "Complete frozen1284120; actual words/剛健.md:13-19; both initial and dependent reports.",
            },
            {
                "claim": "Initial source/link/direct-guard hypotheses and editorial suggestions.",
                "status": "resolved",
                "decision": "Original textual702 evidence-based dispositions preserved: 活力 and linked山/刀 resolved; missing頑丈 article hypothesis withdrawn; ばりばり guard, extra bodily-strength sentence, busy contrast, traditional connotation and noun/proverb expansion remain optional. No transitive guard or unsupported article added.",
                "evidence": "docs/n1-reviews/batch-096-reconciliation.json; both own-report supplements and dependent706 reports.",
            },
        ],
        "boundedSemanticAdjudication": {
            "defaultN1": "剛/sturdy;unyielding strength versus 剖/dissect;split open,削/shave;sharpen;pare,儒/Confucian;Confucian scholar. Ordinary senses do not make a competing answer.",
            "curatedAvailability": "TWO authored wrongcards available inN1, 則N2 excluded; ONE actual fallback儒. All/custom retain三 authored labels; captured UI is not builderseed0償.",
            "kanjiRecords": "All64 exact rows across16seeds/fourpools assessed. 克overcome is related to successful exertion but not the noun/quality sturdy strength; other sampled labels concern different actions, concepts or objects. No demonstrated competing answer.",
            "wordRecords": "All1536 exact rows verified by lossless dictionary/index reconstruction and both reviewer reads. Twelve directguards absent across both directions, bothtargetorientations, All/custom,16seeds. Guard success does not certify every accompanying baseline option.",
            "newTargetRows": "Claude additionally notes no equivalent in64剛健-target rows; 乱暴violent/rough/reckless is not robust constitution. GPT does not claim semantic certification of all-other-word options. No unique verified mandatory defect.",
            "scope": "Bounded actual records CLEAN, not exhaustive semantic certification of all word options or untested seeds/pools.",
            "untestedSeedsAndPoolsAndAllOtherWordOptions": "UNVERIFIED",
        },
        "renderedDisposition": "Both model families support no actionable visual defect in fourfontpanels/all28Han andtencontactsheets/all37routePNG: both complete articles, horizontally scrollable readingtable, onlyonごう/noKun, meaning, one reciprocalpair/twodirections/SystemBack/offline and teninjectedstrokes. Exact fallback font face NOT identified; 冂/刂 visibly recognizable. Reduced images are not physical-phone acceptance.",
        "optional": "No edits: preserve textual702's evidence-based optional/no-edit decisions; no new mandatory content or app defect established.",
        "modelContributionComparison": {
            "shared": "Both confirm glyph distinctions, accessible table scrolling, source-qualified prose and actual default/bounded fallback semantics and12directguards. No verified mandatory defect unique to either.",
            "claudeAdditionalObservation": "Closest剛健-target random option乱暴 is not equivalent. Notes unrelated existing guard-target rows may contain baseline ambiguity, without assigning it to this batch.",
            "gptAdditionalClarification": "Explicitly distinguishes captured儒fallback from builderseed0償, and earlier three authored wrongcards from onlytwo N1-available ones.",
            "limits": "Dependent followups, not new blind discovery or general model benchmark. Observations compared across findings, optional, hypotheses and limits.",
        },
        "actionableRemainingFindings": 0, "consequentialUnresolvedInScopeClaims": 0,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "limits": [
            "Both reviewers received supplied source/native evidence, not independent upstream retrieval or reviewer-run native tests.",
            "Twenty-two complete text chunks and14decoded PNGs each; contact sheets reduced and returned images resized. Exact fallback face unidentified.",
            "Native705 and four non-skipped JVM703 cases inherited, not rerun here. Static captures rely on execution receipts for interaction/offline/persistence.",
            "No new blind initial review, native-speaker certification or measured learning effectiveness.",
            "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, not latestappmain; injectedstrokes/give-up recall are not humanhandwriting/MLKit.",
            "Physicalphone/generalrelease/whole-set outstanding. Combined-current-main integration, all applicable combined checks and publicZIP/CI remain required.",
            "Untested seeds/pools and all-other-word-option semantic safety remain UNVERIFIED; no universal quiz-safety claim.",
        ],
        "nextAction": NEXT,
    }
    m.save(REVIEW, evidence)
    update_packet()
    m.save(E, {
        "schemaVersion": 1, "execution": 706, "batch": "096", "status": STAGE,
        "startingState": m.load(C / "progress.json")["execution706StartingState"],
        "reviewRecord": REVIEW.relative_to(R).as_posix(), "receipts": receipts, "runtime": runtime,
        "originalSessionReviewerProcesses": 2, "atMostOneReviewerActive": True,
        "claudeSerialExecutionAccepted": True, "gptSerialExecutionAccepted": True,
        "newBlindInitialReviewCredit": False, "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "boundedSampleSemanticVerdict": "CLEAN",
        "untestedSeedsAndPoolsAndAllOtherWordOptions": "UNVERIFIED",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 122, "remainingAdditions": 1106,
        "lastPublishedCommit": "4c2416e4c5925e6910b32215412bb1b795f60524",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Both complete serial reports, actual returned payload evidence and reconciliation archived.")


def issue():
    m.ownership()
    assert m.git("rev-parse", "HEAD^") == m.HEAD
    assert m.git("log", "-1", "--format=%G?") == "G"
    assert not m.git("status", "--porcelain", "--untracked-files=all")
    body = (
        "N1 kanji batch 096 / checkpoint 706: **bounded rendered confirmations complete; not published**.\n\n"
        f"Normally signed local evidence: `{m.git('rev-parse', 'HEAD')}`. Unchanged teaching `b26bcf9b`; "
        "native archive `58129f19`, contentVersion `54645b95fe8e939c`. Original Claude Opus 5.5 and GPT-6.1 Sol "
        "review sessions resumed serially; each process exited 0, each returned 22 full text chunks and 14 decoded images "
        "(four font panels/all 28 Han plus ten reduced contact sheets covering 37 route captures), with no tool overlap "
        "or missing/unfinished reads. These are dependent confirmations, not new blind-review credit.\n\n"
        "Both report no actionable defect in the two articles, rendered presentation, captured N1 choices, all 64 bounded "
        "kanji builder records or enforcement of twelve direct word guards across 1,536 exact indexed records. "
        "The actual N1 choices use two curated wrong cards and one fallback (儒); untested pools/seeds and semantic "
        "safety of every other baseline word option remain UNVERIFIED. Four-font 冂/刂 are visibly recognizable; "
        "the exact fallback face remains unidentified. Optional textual suggestions retain their earlier no-edit dispositions.\n\n"
        "Inherited native705 evidence remains two terminal-case successes/no skips, full archive through production "
        "ContentSync once, 1,119 kanji / 5,072 words / 128 N1 / zero problems / parser epoch1; owned emulator stopped. "
        "No native rerun, physical-phone, human-handwriting or MLKit acceptance is claimed. Qualified test-only Android "
        "`1c1b7bf4` retains production `f9b59a2`, not latest app main.\n\n"
        "Evidence: `docs/n1-sources/execution-706.json` and "
        "`docs/n1-reviews/batch-096-rendered-reconciliation-706.json`; original complete reports/raw executions preserved.\n\n"
        "**Next:** same096 latest-main non-rewriting integration and all applicable combined-tree checks, changed-teaching "
        "review if needed, normal signing/owner fast-forward, terminal-green CI and every immutable public ZIP runtime "
        "entry/hash under unchanged budgets. No097 or runtime push at this checkpoint. Published count stays "
        "122/1,228; 1,106 remain. Physical-phone/general-release and whole-set acceptance remain outstanding. "
        "Parent runner lock untouched; no optional historical-session helpers or new permission denials."
    )
    (C / "batch-096-rendered-706-issue-body.txt").write_text(body + "\n", encoding="utf-8")
    print("Owner issue body prepared for exact-author/body verified post.")


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
        E.relative_to(R).as_posix(), REVIEW.relative_to(R).as_posix(), "docs/n1-sources/batch-096-progress.json"}
    assert set(m.git("diff", "--name-only", m.HEAD, "HEAD").splitlines()) == expected
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert m.sha(path) == row["archiveSha256"]
        if row.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == row["sourceSha256"]
    prefix = C / "batch-096-rendered-706-issue-"
    body = Path(str(prefix) + "body.txt").read_bytes().decode("utf-8-sig")
    receipt, posted = m.load(Path(str(prefix) + "receipt.json")), m.load(Path(str(prefix) + "posted.json"))
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = m.load(C / "progress.json"), m.load(L / "progress-before-706.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 706, "checkpoint": 706, "batch": "096",
        "savedCommit": m.git("rev-parse", "HEAD"), "signature": "G",
        "status": "continue", "stage": STAGE, "evidence": E.relative_to(R).as_posix(),
        "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "originalSessionReviewerProcesses": 2, "allReviewerProcessesExited": True,
        "claudeSerialExecutionAccepted": True, "gptSerialExecutionAccepted": True,
        "newBlindInitialReviewCredit": False, "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "boundedSampleSemanticVerdict": "CLEAN",
        "untestedSeedsAndPoolsAndAllOtherWordOptions": "UNVERIFIED",
        **runtime, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 122, "remainingAdditions": 1106,
        "lastPublishedCommit": "4c2416e4c5925e6910b32215412bb1b795f60524",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "checkpointHelper": str(Path(__file__)), "checkpointHelperSha256": m.sha(Path(__file__)),
        "nextAction": NEXT,
    }
    state.update(checkpoint=706, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution706CoordinatorCheckpoint"] = checkpoint
    state["batch096RenderedReviewCheckpoint"] = checkpoint
    state["execution706StartingState"]["status"] = "signed-local-rendered-review-checkpoint-complete"
    m.persist(state)
    reread = m.load(C / "progress.json")
    assert all(reread[k] == v for k, v in before.items() if k not in allowed)
    m.save(L / "checkpoint-706.json", checkpoint)
    print("Checkpoint706 persisted; all", len(before), "original historical root values preserved.")
    print(checkpoint["savedCommit"], checkpoint["issueUpdate"])


if __name__ == "__main__":
    {"archive": archive, "issue": issue, "finalize": finalize}[sys.argv[1]]()
