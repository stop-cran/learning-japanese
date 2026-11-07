"""Archive serial combined-main confirmations and checkpoint without publishing."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("combined697", C / "confirm-batch-095-combined-697.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R, L = m.R, m.L
V = R / "docs" / "n1-reviews"
E = R / "docs" / "n1-sources" / "execution-697.json"
REVIEW = V / "batch-095-combined-teaching-reconciliation-697.json"
STAGE = "combined-main-teaching-confirmed-awaiting-exact-combined-native-import"
NEXT = (
    "SAME095 only: finish exact combined native import before reviewclosed/publication. "
    "Signed incoming teaching at6c945042/merge d5a6823c (parents515666e9+da374717), "
    "contentVersion3eebfff0fdad5e28/all8441hashes unchanged. "
    "Read docs/n1-sources/execution-697.json and "
    "docs/n1-reviews/batch-095-combined-teaching-reconciliation-697.json. "
    "OriginalClaude ede78c28-e889-47b5-be0b-21533da61551 THEN originalGPT "
    "ee7498e0-d3ad-46bf-bbc9-82761892cab0 completed accepted strictserial dependent "
    "changed-passage confirmations on SAME signed6c945042: all6commonchunks/11incomingarticles/"
    "3comparisonarticles/10completefrozenJMdictfamilies and live8sourceURLs each. Actualmodels "
    "claude-opus-5.5/gpt-6.1-sol; both process exits verified, no overlaps/unfinishedtools. "
    "All11 incoming passages CLEAN separately correctness/scopedcoverage/comprehensibility, "
    "zero actionable findings/consequential unresolved claims. NOT new blind batch review. "
    "Claude optional liveWiktionary revisionpin/source-smallness explanation preserved OPTIONAL, "
    "no runtime edit; actual partialKotobank limits explicit: Nipponica supports fruit history, "
    "neither reviewer freshly inspected Daijisen菓子. No ultimateetymology consensus claim. "
    "Original691blind/694native/695rendered unchanged and inherited with all limits; original "
    "Claude695overlap remains REJECTED forever, separate small serialrepair retained. "
    "Combined696 all372Python/validate/regeneratedmanifest/vocabularypilot2122of2431/"
    "originalbudgets/fullfrozendictionaries/fullbaseline/readings/strokes/allmappedlinks/fontprovenance/"
    "FOURAndroidRealContentTHREE+RareHanONE/no skips remain applicable, not freshly rerun as697. "
    "697 runtime8441hashes/manifestfresh/validate/build_manifest/budget reverified. "
    "All32batch095Han/fourfonts/60PNG and teaching/geometry/reading/quizmetadata unchanged, "
    "so no manufactured glyph/route rerun requirement. BUT exact combined manifest DIFFERS "
    "from native694version463619d79972e9f2: obtain bounded new full combined gitarchive "
    "through productionContentSync ONCE, assert1118kanji5071words127N1/zeroProblems/"
    "acceptedRoomversion3eebfff0fdad5e28+readingepoch1 and preserved full/Liteボウ/[] explicitボウ/[] "
    "plus THREEdirectguards and links. Do NOT relabel old fullarchivecc748347/native694 as new import. "
    "Keep old fixture/hash immutable; new clearly named fixture/evidence, no guards/heap changes. "
    "Freshport/device/PID5580/5581ownership for ownedreadonlyAPI35 emulator "
    "N3_Acceptance_20261029 emulator5580 hostGPU/-Vulkan/2048MiB/2cores; stop onlyownedhelper. "
    "Explicit JDK17/SDK and oneGradleworker/inprocessKotlin; no concurrent heavy/reviewer work. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "Then normal signed reviewclosed/combinedacceptance evidence; freshmain recheck "
    "(origin/main da374717 at697), nonrewriting merge/revalidate and independent substantive-change "
    "confirmation if advanced. Ownerfastforward to origin/main ONLY after ALLgates. Verify exactremoteSHA/"
    "terminalgreenCI/EVERYimmutablepublicZIPruntimeentryhash/manifest equality/original18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue. "
    "LocalZIP not publicacceptance. Parent19008 ownsrunner.lock: verifyliveancestry/session/checkpoint/"
    "exactsignedheads/whollyclean, NOchildacquire/delete/unlock. Approvedcontrol/committedpackets only; "
    "no optionalhistoricalsessionhelpers. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. No runtimepublication/096/secondrunner at697. Published121of1228/"
    "1107remaining unchanged; physicalphone/generalrelease/whole-set outstanding, "
    "no phone/humanhandwriting/MLKit/fullpool certification."
)


def update_packet():
    path = R / "docs" / "n1-sources" / "batch-095-progress.json"
    newline = "\r\n" if b"\r\n" in path.read_bytes() else "\n"
    text = path.read_text(encoding="utf-8")
    current = json.loads(text)
    current.update(status=STAGE, nextAction=NEXT, pendingGates=[
        "Incoming eleven-file combined-main teaching delta confirmed697 by original two families; exact combined native import3eebfff0fdad5e28 remains pending.",
        "Normally signed reviewclosed/combinedacceptance evidence; freshmain recheck/remerge/revalidation if advanced; ownerfastforward, terminalgreenCI, EVERYimmutablepublicZIPentryhash, originalbudgets, verifiedownerissue; no096 before public acceptance.",
    ])
    decoder = json.JSONDecoder()
    for key in ["status", "nextAction", "pendingGates"]:
        match = re.search(r'^  "' + key + r'": ', text, re.MULTILINE)
        assert match
        _, end = decoder.raw_decode(text, match.end())
        value = json.dumps(current[key], ensure_ascii=True, indent=2).replace("\n", "\n  ")
        text = text[:match.end()] + value + text[end:]
    current["combinedTeachingConfirmation697"] = {
        "evidence": E.relative_to(R).as_posix(), "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "status": STAGE, "newBlindInitialReviewCredit": False, "runtimeChanged": False,
        "incomingTeachingFiles": 11, "completeFrozenFamilies": 10, "commonChunks": 6,
        "reviewerProcesses": 2, "allReviewerProcessesExited": True,
        "strictSerialAccepted": True, "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "exactCombinedNativeImport": "pending",
        "runtimeAccepted": False, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier pending fields remain historical. This additive record supersedes the pending incoming teaching-confirmation gate only, not exact combined native import or publication.",
    }
    end = text.rfind("}")
    extra = json.dumps({"combinedTeachingConfirmation697": current["combinedTeachingConfirmation697"]},
                       ensure_ascii=True, indent=2)[1:-1]
    text = text[:end].rstrip() + "," + extra + text[end:]
    assert json.loads(text) == current
    path.write_text(text, encoding="utf-8", newline=newline)


def archive():
    m.frozen()
    runtime = m.runtime()
    records = [m.load(C / f"batch-095-combined-697-{name}-execution.json") for name in ["claude", "gpt"]]
    for record in records:
        assert record["acceptedExecution"] and record["exitCode"] == 0
        assert record["processExitedVerified"] and not record["unfinishedTools"] and not record["observedToolOverlaps"]
        m.stopped(record["launcherPid"])
    assert records[0]["completedAt"] < records[1]["startedAt"]
    provenance = m.load(C / "batch-095-combined-697-packet-provenance.json")
    receipts = []
    sources = [Path(__file__), C / "confirm-batch-095-combined-697.py",
               C / "post-batch-095-combined-697.ps1",
               C / "batch-095-combined-697-resources.json",
               C / "batch-095-combined-697-packet-provenance.json",
               L / "runtime-preflight-697.json"]
    packed = [Path(s) for s in m.load(C / "batch-095-combined-697-resources.json")]
    packed += [C / f"batch-095-combined-697-cli-{kind}.txt" for kind in ["help", "config"]]
    for name, record in zip(["claude", "gpt"], records):
        prefix = C / f"batch-095-combined-697-{name}"
        assert m.sha(prefix.with_suffix(".jsonl")) == record["rawSha256"]
        assert m.sha(prefix.with_suffix(".md")) == record["reportSha256"]
        packed.append(prefix.with_suffix(".jsonl"))
        sources += [prefix.with_suffix(s) for s in [".md", ".prompt.txt", ".stderr.txt", ".usage.json", ".active.json"]]
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
        assert not target.exists()
        shutil.copyfile(source, target)
        receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": m.sha(source), "archiveSha256": m.sha(target)})
    source = C / "batch-095-combined-697-jmdict.xml"
    target = R / "docs" / "n1-sources" / source.name
    assert not target.exists()
    shutil.copyfile(source, target)
    receipts.append({"source": str(source), "archive": target.relative_to(R).as_posix(),
                     "sourceSha256": m.sha(source), "archiveSha256": m.sha(target)})
    review = {
        "schemaVersion": 1, "batch": "095", "execution": 697, "status": STAGE,
        "snapshot": m.HEAD, "combinedMerge": provenance["combinedMerge"],
        "contentVersion": runtime["contentVersion"], "incomingScope": provenance["incomingPaths"],
        "newBlindInitialReviewCredit": False,
        "reviewers": [
            {"actualModel": row["actualModels"][0], "sessionId": row["sessionId"],
             "report": f"docs/n1-reviews/batch-095-combined-697-{name}.md",
             "executionRecord": f"docs/n1-reviews/batch-095-combined-697-{name}-execution.json",
             "allSixCommonTextChunksReturned": True, "liveSourceUrlsFetched": 8,
             "exitCode": row["exitCode"], "processExitedVerified": True,
             "internalToolOverlaps": 0, "unfinishedTools": 0}
            for name, row in zip(["claude", "gpt"], records)
        ],
        "facetVerdicts": {
            path: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"}
            for path in provenance["incomingPaths"]
        },
        "findings": [],
        "reconciliation": [
            {"id": "697-wiktionary-revision-pin", "reportedBy": "Claude optional1 only; GPT optional none",
             "status": "optional", "file": "words/柚.md:26",
             "claim": "Live Wiktionary link could drift from checked revision1925322.",
             "decision": "No edit. Exact inspected revision and complete returned Japanese grouping are preserved in source/review evidence. Current attribution is correct; stable runtime link is useful navigation. No contradicted teaching established.",
             "evidence": ["docs/ko-nominal-endings-sources.json:sources", "Both actual revision1925322 returned payloads"],
             "confidence": "high"},
            {"id": "697-source-smallness-wording", "reportedBy": "Claude optional2; GPT observed source wording but no actionable finding",
             "status": "optional", "file": "kanji/子.md:32-34; words/帽子.md:24",
             "claim": "Gogen-yurai 帽子 gloss mentions small things; Daijisen nominal-ending sense9 and abstract examples establish a broader scope.",
             "decision": "No edit. Article does not claim Gogen-yurai settles every suffix use; the explicit Daijisen sense9 distinguishes nominal endings from small-particle sense7 and includes 調子/様子. Source-local wording is not an absolute general restriction. Optional visibility of this difference is preserved, not inflated into a consequential unresolved claim.",
             "evidence": ["Daijisen 子 sense9 and ス referring to9", "Actual Gogen-yurai 帽子/椅子 returned headings", "kanji/子.md:26-34,63-65"],
             "confidence": "high"},
        ],
        "sourceAdjudication": [
            {"claim": "Nominal endings versus offspring/person and scientific particles",
             "evidence": "Actual Daijisen し【子】漢字項目 senses1/7/9, ス same as9; both models inspected the relevant heading.",
             "decision": "Supported; neither changed teaching nor this review claims every whole compound or modern referent was borrowed."},
            {"claim": "Former fruit sense of 菓子",
             "evidence": "Both fetched results exposed Nipponica; Claude read preview only, GPT read first6000chars plus later chunks.",
             "decision": "Direct Nipponica support suffices. Neither freshly inspected Daijisen 菓子; do not claim otherwise."},
            {"claim": "柚 label and ultimate origin",
             "evidence": "Complete frozen JMdict1605750 plus live Daijisen/Seisenban plant headings, actual Gogen-yurai Chinese-origin account and Wiktionary revision1925322 和語の漢字表記.",
             "decision": "Qualified source attribution is accurate. Ultimate etymology remains unsettled, not a consensus claimed by the article; not an unexplained consequential teaching claim."},
        ],
        "contributionComparison": {
            "sharedActionableFindings": [], "verifiedUsefulUniqueActionableFindings": [],
            "sharedSupportedObservations": "Both families support all eleven bounded deltas and identify actual evidence and source limits. No model ranking or manufactured defect quota.",
            "claudeOnlyOptional": ["Pin Wiktionary revision", "Explain source-local smallness wording more explicitly"],
            "unsupportedSuggestions": [],
            "limits": "Dependent original-session confirmations, not fresh blind comparison. No fresh Daijisen菓子 heading; different returned page depths retained."},
        "actionableRemainingFindings": 0, "consequentialUnresolvedInScopeClaims": 0,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "exactCombinedNativeImport": "pending",
        "limits": [
            "Bounded changed-passage confirmation only. Initial691/Native694/Rendered695 and their independent/dependent limits remain historical.",
            "OriginalClaude695 overlap remains rejected forever; separate smallest serial repair not retroactively called compliance.",
            "All six common chunks returned completely to both reviewers, including all11articles/3comparisonarticles/10complete frozenfamilies. Returned bytes do not establish comprehension or full untouched-corpus review.",
            "Actual source limits: Claude 子 first20000chars, 菓子 preview only, 障子 first8000chars. GPT 子 first11000chars, 菓子 first6000chars plus12000/18000 offsets, 障子 first10000chars. Neither Daijisen菓子 heading freshly inspected.",
            "Oversize-output messages are preserved as tool delivery limits, not permission denials. Extra current-tool temporary web-output reads were actual public-source evidence, not optional historical-session helpers.",
            "No new rendering/native/device/phone/humanhandwriting/MLKit/fullpool/CI/publicZIP/publication/generalrelease evidence. All unchanged native/rendered claims inherited only.",
            "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2; not latestappmain. Exact new merged manifest import remains required.",
        ],
        "evidence": E.relative_to(R).as_posix(), "nextAction": NEXT,
    }
    m.save(REVIEW, review)
    evidence = {
        "schemaVersion": 1, "execution": 697, "batch": "095", "status": "continue", "stage": STAGE,
        "startingState": m.load(C / "progress.json")["execution697StartingState"],
        "reviewedSnapshot": m.HEAD, "combinedMerge": provenance["combinedMerge"],
        "runtime": runtime, "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "incomingChangedPassages": 11, "sourceProvenance": provenance,
        "reviewerProcesses": 2, "allReviewerProcessesExited": True,
        "atMostOneActiveReviewerVerified": True, "strictSerialToolExecutionAccepted": True,
        "actualModels": [row["actualModels"][0] for row in records],
        "newBlindInitialReviewCredit": False, "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "optionalDispositions": review["reconciliation"],
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "exactCombinedNativeImport": "pending", "freshAndroidOrNativeClaimed": False,
        "inheritedCombinedAutomatedChecks": "execution696:372Python;4Android/no skips; source/baseline/link/readings/strokes/font/vocabularypilot/budget checks, unchanged runtime.",
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "publishedAdditions": 121, "remainingAdditions": 1107, "wholeProjectComplete": False,
        "nextBatchStarted": False, "receipts": receipts, "limits": review["limits"], "nextAction": NEXT,
    }
    m.save(E, evidence)
    update_packet()
    print(f"Archived both complete reports, actual serial execution, full common evidence and ten frozen families; {len(receipts)} receipts.")


def checks():
    evidence = m.load(E)
    names = [("validate", ["python", "-X", "utf8", "-B", "tools\\validate.py"]),
             ("manifest", ["python", "-X", "utf8", "-B", "tools\\build_manifest.py"]),
             ("budget", ["python", "-X", "utf8", "-B", "tools\\check_content_budget.py"])]
    import subprocess
    results = []
    for name, command in names:
        result = subprocess.run(command, cwd=R, capture_output=True)
        log = L / f"{name}-697.txt"
        log.write_bytes(result.stdout + result.stderr)
        assert result.returncode == 0, log
        results.append({"command": command, "exitCode": result.returncode, "log": str(log),
                        "logSha256": m.sha(log)})
    assert m.runtime() == evidence["runtime"]
    evidence["freshEvidenceOnlyChecks"] = results
    m.save(E, evidence)
    print("Validate, manifest freshness/all8441payloadhashes, original archive budgets pass; runtime unchanged.")


def finalize():
    m.ownership()
    head = m.git("rev-parse", "HEAD")
    assert m.git("rev-parse", "HEAD^") == m.HEAD
    assert m.git("log", "-1", "--format=%G?") == "G"
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in m.git("log", "-1", "--format=%B")
    for repo in [R, m.A]:
        assert not m.git("status", "--porcelain", "--untracked-files=all", repo=repo)
    assert m.git("rev-parse", "HEAD", repo=m.A) == m.APP
    assert m.git("log", "-1", "--format=%G?", repo=m.A) == "G"
    runtime = m.runtime()
    assert not m.git("diff", m.HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = m.load(E)
    expected = {r["archive"] for r in evidence["receipts"]} | {
        E.relative_to(R).as_posix(), REVIEW.relative_to(R).as_posix(), "docs/n1-sources/batch-095-progress.json"}
    assert set(m.git("diff", "--name-only", m.HEAD, "HEAD").splitlines()) == expected
    for row in evidence["receipts"]:
        path = R / row["archive"]
        assert m.sha(path) == row["archiveSha256"]
        if row.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == row["sourceSha256"]
    for model in ["claude", "gpt"]:
        m.stopped(m.load(C / f"batch-095-combined-697-{model}-execution.json")["launcherPid"])
    prefix = C / "batch-095-combined-697-issue-"
    body = Path(str(prefix) + "body.txt").read_bytes().decode("utf-8-sig")
    receipt = m.load(Path(str(prefix) + "receipt.json"))
    posted = m.load(Path(str(prefix) + "posted.json"))
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = m.load(C / "progress.json"), m.load(L / "progress-before-697.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 697, "checkpoint": 697, "batch": "095",
        "savedCommit": head, "signature": "G", "status": "continue", "stage": STAGE,
        "combinedMerge": evidence["combinedMerge"], "reviewedSnapshot": m.HEAD,
        "evidence": E.relative_to(R).as_posix(), "reviewRecord": REVIEW.relative_to(R).as_posix(),
        "incomingChangedPassages": 11, "changedTeachingConfirmation": "complete",
        "originalSessionReviewerProcesses": 2, "allReviewerProcessesExited": True,
        "strictSerialToolExecutionAccepted": True, "actualModels": evidence["actualModels"],
        "newBlindInitialReviewCredit": False, "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0, "optionalSuggestions": 2,
        **runtime, "runtimeAccepted": False, "runtimePublished": False,
        "exactCombinedNativeImport": "pending", "publicGithubZipAcceptance": False,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 121, "remainingAdditions": 1107,
        "lastPublishedCommit": "d6a261903f269d6223afc067815b02c595da41a3",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "checkpointHelper": str(Path(__file__)), "checkpointHelperSha256": m.sha(Path(__file__)),
        "nextAction": NEXT,
    }
    state.update(checkpoint=697, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    state["execution697CoordinatorCheckpoint"] = checkpoint
    state["batch095CombinedTeachingCheckpoint"] = checkpoint
    state["execution697StartingState"]["status"] = "signed-local-combined-teaching-checkpoint-complete"
    m.persist(state)
    reread = m.load(C / "progress.json")
    assert all(reread[k] == v for k, v in before.items() if k not in allowed)
    m.save(L / "checkpoint-697.json", checkpoint)
    print(f"Checkpoint697 persisted; all {len(before)} original historical root values preserved.")
    print(head, receipt["html_url"])


if __name__ == "__main__":
    {"archive": archive, "checks": checks, "finalize": finalize}[sys.argv[1]]()
