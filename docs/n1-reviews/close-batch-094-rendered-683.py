"""Archive actual rendered-review outcomes and checkpoint without publication."""
import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("rendered683", C / "confirm-batch-094-rendered-683.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R, V, L = m.R, m.V, m.L
E = R / "docs" / "n1-sources" / "execution-683.json"
STAGE = "rendered-confirmed-observed-word-quiz-safeguard-pending"
NEXT = (
    "SAME094 only: read docs/n1-sources/execution-683.json and "
    "docs/n1-reviews/batch-094-rendered-reconciliation-683.json. "
    "Original-session rendered confirmations and bounded observed-choice adjudication preserved; "
    "NOT new blind review or runtime acceptance/publication. Append ONLY source-backed direct "
    "quiz_exclusion 縮める to words/削る.md (or equivalent one-sided declaration), preserving all "
    "original exclusions/order, titles, identities, levels, readings, prose, links and geometry. "
    "Observed exact production All seeds7/15 in both directions includes 削る/縮める; "
    "complete frozen JMdict1298090 sense2 and1337570 sense1 support shared reduce/shorten senses. "
    "No transitive-clique rationale. Run validate/build_manifest and focused baseline/link/reading/"
    "membership/audits, freeze normally signed LOCAL correction, obtain bounded original-session "
    "confirmation from BOTH original models. Retain original Claude683 panels1+2 overlap as "
    "rejected, plus accepted three-read serial repair; no retroactive compliance claim. "
    "Run exact changed manifest/full-archive production ContentSync ONCE and focused production "
    "builder checks for new direct pair both directions/both target orientations/All+custom with "
    "non-skipped native evidence as applicable. Inherit unchanged visual evidence honestly; do "
    "not repeat all85 captures or121families without a new concern. Resolve consequential claims "
    "before acceptance. Then fresh current-main normal merge if needed, independently review "
    "changed teaching and ALL combined-tree content/Python/vocabulary/baseline/link/membership/"
    "reading/font/budget/applicable Android checks. Keep normal signing/owner fastforward/"
    "terminalgreenCI/EVERY immutable publicZIP runtimehash and18000entries/42MiBcompressed/"
    "80MiBinflated/56MiBretained/perfile-media-safepath/verifiedownerissue gates. "
    "No095/runtimepublication/secondrunner at this checkpoint. Parent19008 retainsrunner.lock: "
    "verify live ancestry/session/signedheads/whollyclean, NOchild acquire/delete/unlock. "
    "Approved control and committed packets only, NO optionalhistoricalsessionhelpers. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. QualifiedTESTONLY"
    "Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Native682 exact original "
    "archive18ad4bed/versioneeae47753a460f72/8438hashes/1117kanji5070words126N1/zeroProblems/"
    "Roomepoch1/two terminalcase0/no skips inherited; owned5580 stopped. No phone/humanhandwriting/"
    "successfulMLKit claim. Published120/1228,1108remaining; physicalphone/generalrelease/whole-set outstanding."
)


def stopped(record):
    subprocess.run(["pwsh", "-NoProfile", "-Command",
                    f"if(Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue){{exit 1}}"],
                   capture_output=True, check=True)


def archive():
    m.frozen()
    runtime = m.runtime()
    names = ["claude", "claude-serial-repair", "gpt"]
    records = [m.load(C / f"batch-094-rendered-683-{name}-execution.json") for name in names]
    original, repair, gpt = records
    assert not original["acceptedExecution"] and len(original["observedToolOverlaps"]) == 1
    assert len(original["actualDecodedImageReturns"]) == 25
    assert len(original["toolCalls"]) == 37 and all(
        p in original["successfullyReturnedResources"] for p in original["requiredResources"])
    assert repair["acceptedExecution"] and len(repair["toolCalls"]) == 3
    assert len(repair["actualDecodedImageReturns"]) == 2
    assert gpt["acceptedExecution"] and len(gpt["actualDecodedImageReturns"]) >= 25
    assert original["completedAt"] < repair["startedAt"] < repair["completedAt"] < gpt["startedAt"]
    for record in records:
        assert record["exitCode"] == 0 and not record["unfinishedTools"]
        stopped(record)
    receipts = []
    sources = [Path(__file__), C / "confirm-batch-094-rendered-683.py",
               C / "confirm-batch-094-rendered-683-original.py",
               C / "post-batch-094-rendered-683.ps1",
               C / "batch-094-rendered-packet-provenance-683.json",
               C / "batch-094-rendered-observed-pair-683.xml"]
    sources += [C / f"batch-094-rendered-cli-{kind}-683.txt" for kind in ["help", "config"]]
    for label in ["claude", "gpt"]:
        resources = C / f"batch-094-rendered-{label}-resources-683.json"
        sources.append(resources)
        sources += [Path(p) for p in m.load(resources) if p.endswith(".txt")]
    for name, record in zip(names, records):
        prefix = C / f"batch-094-rendered-683-{name}"
        raw = prefix.with_suffix(".jsonl")
        assert m.sha(raw) == record["rawSha256"]
        assert m.sha(prefix.with_suffix(".md")) == record["reportSha256"]
        target = V / (raw.name + ".gz")
        assert not target.exists()
        target.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw.read_bytes()
        receipts.append({"source": str(raw), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": m.sha(raw), "archiveSha256": m.sha(target), "losslessGzip": True})
        sources += [prefix.with_suffix(s) for s in [
            ".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"]]
        sources.append(C / f"{prefix.name}-execution.json")
    for source in sources:
        target = V / source.name
        assert not target.exists(), str(target)
        shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": m.sha(source), "archiveSha256": m.sha(target)})
    evidence = {
        "schemaVersion": 1, "execution": 683, "batch": "094", "status": STAGE,
        "reviewedSnapshot": m.HEAD, "reviewedTeachingSnapshot": "4089e881d605ce92c4c425d57816bc795605ded8",
        "nativeReceipt": "docs/n1-sources/execution-682.json",
        "dependentOriginalSessionRecords": [
            f"docs/n1-reviews/batch-094-rendered-683-{name}-execution.json" for name in names],
        "newBlindInitialReviewCredit": False, "runtime": runtime,
        "processDisposition": {
            "originalClaude": "Rejected for strict serial execution: panels1+2 overlapped; complete original report/raw/execution retained.",
            "serialRepair": "Three complete serial views: own report, panel1, panel2. Fresh dependent confirmation only; does not retroactively repair original execution.",
            "gpt": "Complete original-session rendered evidence review; serial read and image payload delivery audited.",
            "reviewerProcessesLaunched": 3, "atMostOneActiveReviewerVerified": True,
            "originalOverlapNeverRelabeledCompliant": True,
        },
        "reconciliation": [{
            "id": "094-observed-kezuru-chijimeru", "status": "unresolved", "severity": "minor",
            "facet": "word meaning quiz correctness", "file": "words/削る.md:9",
            "claim": "Actual All-stack choices place 削る beside 縮める; ordinary reduce/shorten senses overlap and the uncontextualized labels can mark a defensible answer wrong.",
            "evidence": [
                "native682 directGuardBuilderChecks zero-based indices7,15,23,31,135,143,151,159; All seeds7/15 both directions",
                "Complete frozen JMdict1298090 sense2: cut down budget/expenses/staff/time; curtail; reduce",
                "Complete frozen JMdict1337570 sense1: shorten; reduce; condense; shrink",
                "Current 削る teaches time/budget reduction; current 縮める teaches shortening meeting time",
                "docs/content-format.md:169-177 requires direct guards for overlapping displayed meanings",
            ],
            "remedy": "Append 縮める to 削る quiz_exclusions; retain other declarations and prose; validate/regenerate manifest and obtain bounded two-original-session correction confirmations plus exact changed builder/import evidence.",
            "confidence": "High that observed pair is present and the shared ordinary reduction sense warrants the repository's conservative direct guard. No universal lexical substitution or transitive-clique claim.",
            "reviewerDispositions": {
                "claude": "Low; medium confidence; original overlap rejected for process acceptance, report retained as a hypothesis/evidence contribution. Serial repair leaves this finding unchanged.",
                "gpt": "Moderate; high confidence specifically for Japanese-to-English ambiguity; does not require identical English-to-Japanese applicability.",
                "coordinator": "Minor localized metadata omission: demonstrable competing reduction label in observed Japanese-to-English samples, no teaching-prose defect or global quiz correctness collapse. Precise evidence, not model votes or shared third-party exclusions, justifies the direct guard.",
            },
            "discoveryCredit": "Coordinator-supplied hypothesis adjudicated in dependent followups; not a new independent blind discovery or comparative-model credit.",
        }],
        "facetVerdicts": {
            "kanji/削.md": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"},
            "words/削る.md": {"correctness": "NEEDS FIX", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"},
            "words/削除.md": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"},
            "kanji/除.md:41": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"},
            "boundedRenderedEvidence": {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"},
            "boundedWordChoiceEvidence": {"correctness": "NEEDS FIX", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"},
        },
        "renderedDisposition": "No actionable visual defect established in actual supplied five font panels/all41Han and20contact sheets/all80route captures; dependent bounded confirmation only.",
        "optional": [
            "Keep prior optional polish optional. Mixed link wrapping and shave/sharpen/pare gloss consistency do not require runtime rewriting.",
            "Any out-of-assignment 除く/取り出す hypothesis is not established by this packet and does not expand this checkpoint.",
        ],
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "limits": [
            "Contact sheets reduced and image returns resized; hashes establish delivery, not comprehension. Exact returned dimensions and actual read coverage retained per execution.",
            "No new blind initial review, fresh full121family review, upstream verification, native-speaker certification or exhaustive random-pool safety.",
            "Native tests are inherited682 coordinator receipts, not newly executed here; qualified TESTONLYAndroid1c1b7bf4 is not latest app main.",
            "API35 emulator evidence is not physical-phone, human-handwriting or successful MLKit acceptance; phone/general release and whole-set outstanding.",
            "A later quiz metadata correction changes the runtime manifest; old native682 archive must not be relabeled as the corrected import.",
        ],
        "nextAction": NEXT,
    }
    m.save(V / "batch-094-rendered-reconciliation-683.json", evidence)
    m.save(E, {
        "schemaVersion": 1, "execution": 683, "batch": "094", "status": STAGE,
        "startingState": m.load(C / "progress.json")["execution683StartingState"],
        "reviewRecord": "docs/n1-reviews/batch-094-rendered-reconciliation-683.json",
        "receipts": receipts, "runtime": runtime, "originalSessionReviewerProcesses": 3,
        "atMostOneReviewerActive": True, "originalClaudeOverlapPreservedRejected": True,
        "boundedSerialRepairAccepted": True, "gptSerialExecutionAccepted": True,
        "observedWordQuizDefect": "094-observed-kezuru-chijimeru unresolved; correction not applied",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": "48765e20846e1d6769c6ddc35146f6ce58deab57",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    })
    print("Complete reports, process violations, serial repair and source adjudication archived; no runtime edit.")


def finalize():
    m.frozen(final=True)
    runtime = m.runtime()
    evidence = m.load(E)
    expected = {r["archive"] for r in evidence["receipts"]} | {
        E.relative_to(R).as_posix(), "docs/n1-reviews/batch-094-rendered-reconciliation-683.json"}
    changed = subprocess.check_output(
        ["git", "-C", str(R), "diff", "--name-only", "-z", m.HEAD, "HEAD"]).decode("utf-8").split("\0")
    assert set(filter(None, changed)) == expected
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert m.sha(path) == row["archiveSha256"]
        if row.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == row["sourceSha256"]
    prefix = str(C / "batch-094-rendered-683-issue-")
    body = Path(prefix + "body.txt").read_bytes().decode("utf-8-sig")
    receipt, posted = m.load(Path(prefix + "receipt.json")), m.load(Path(prefix + "posted.json"))
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = m.load(C / "progress.json"), m.load(L / "progress-before-683.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 683, "checkpoint": 683, "batch": "094",
        "savedCommit": m.git("rev-parse", "HEAD"), "signature": "G",
        "status": "continue", "stage": STAGE, "evidence": E.relative_to(R).as_posix(),
        "reviewRecord": evidence["reviewRecord"], "observedWordQuizDefect": evidence["observedWordQuizDefect"],
        "originalSessionReviewerProcesses": 3, "allReviewerProcessesExited": True,
        "originalClaudeOverlapPreservedRejected": True, "boundedSerialRepairAccepted": True,
        "gptSerialExecutionAccepted": True, "newBlindInitialReviewCredit": False,
        **runtime, "runtimeAccepted": False, "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": "48765e20846e1d6769c6ddc35146f6ce58deab57",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    state.update(checkpoint=683, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution683CoordinatorCheckpoint"] = checkpoint
    state["batch094RenderedReviewCheckpoint"] = checkpoint
    state["execution683StartingState"]["status"] = "signed-local-rendered-review-checkpoint-complete"
    m.save(C / "progress.json", state)
    reread = m.load(C / "progress.json")
    assert all(reread[k] == v for k, v in before.items() if k not in allowed)
    m.save(L / "checkpoint-683.json", checkpoint)
    print("Checkpoint683 persisted; all", len(before), "original historical root values preserved.")
    print(checkpoint["savedCommit"], checkpoint["issueUpdate"])


def pack_evidence():
    assert m.git("rev-parse", "HEAD") == m.HEAD
    evidence = m.load(E)
    packed = []
    for row in evidence["receipts"]:
        path = R / row["archive"]
        if ("-packet-683-" not in path.name and path.name != "batch-094-rendered-cli-config-683.txt"):
            continue
        assert path.parent == V and path.suffix == ".txt"
        assert m.sha(path) == row["archiveSha256"] == row["sourceSha256"]
        target = path.with_suffix(path.suffix + ".gz")
        assert not target.exists()
        target.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        assert gzip.decompress(target.read_bytes()) == path.read_bytes()
        old = row["archive"]
        row.update(archive=target.relative_to(R).as_posix(), archiveSha256=m.sha(target), losslessGzip=True)
        subprocess.run(["git", "-C", str(R), "rm", "--cached", "--quiet", "--", old], check=True)
        path.unlink()
        packed.append({"oldArchive": old, "losslessArchive": row["archive"], "sourceSha256": row["sourceSha256"]})
    assert len(packed) == 25
    disposition = C / "batch-094-rendered-evidence-packaging-683.json"
    assert not disposition.exists()
    m.save(disposition, {
        "execution": 683, "batch": "094",
        "diagnostic": "Staged git diff --check found whitespace from line-numbered blank article lines, chunk boundaries and exact CLI capture. Signing was not invoked.",
        "disposition": "Preserve exact originally reviewed/control bytes losslessly in gzip rather than edit evidence or weaken whitespace checks. Only newly created contributor evidence paths replaced; no runtime edit.",
        "packed": packed, "originalReviewerResourcesUnchanged": True,
    })
    target = V / disposition.name
    shutil.copyfile(disposition, target)
    evidence["receipts"].append({
        "source": str(disposition), "archive": target.relative_to(R).as_posix(),
        "sourceSha256": m.sha(disposition), "archiveSha256": m.sha(target)})
    helper = V / Path(__file__).name
    shutil.copyfile(Path(__file__), helper)
    row = next(r for r in evidence["receipts"] if r["archive"] == helper.relative_to(R).as_posix())
    row.update(sourceSha256=m.sha(helper), archiveSha256=m.sha(helper))
    m.save(E, evidence)
    print("Losslessly packaged", len(packed), "exact raw evidence files; original reviewed inputs unchanged.")


if __name__ == "__main__":
    {"archive": archive, "pack": pack_evidence, "finalize": finalize}[sys.argv[1]]()
