"""Accept the bounded combined tree locally; the launcher retains runner.lock."""
import ast
import copy
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
L = C / "logs" / "34bc00a6-747c-4edf-a3f2-a116b65e8556"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-099-combined-acceptance-743"
HEAD = "92a9b12ff51f6877fcb21d2a504cc355555ec81e"
MAIN = "2d3a3fa022d48aca6ea8a2ac629bd7ee66b85f9f"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
VERSION = "39eb4a86902c6dec"
CHAR = "\u5270"
STAGE = "batch-099-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME099 publication only next. Read docs/n1-sources/execution-743.json and "
    "docs/n1-reviews/batch-099-combined-acceptance-743.json at the signed LOCAL "
    "review-closed checkpoint. Fresh origin/main2d3a3fa0 is already ancestor; "
    "normal nonrewriting merge Already up to date, ZERO incoming/runtime/teaching "
    "changes. Fresh full Python/validate/regenerated manifest/vocabulary/budget/"
    "frozen sources/full baseline/all readings/pinned strokes/all mapped links/"
    "font provenance and exact supported kanji guard audits passed. All8451 runtime "
    "hashes/version39eb4a86902c6dec equal compiled739 archive749ea11b. Qualified "
    "Android remains signedbf30cdead8515739bc0e671d57a54b9a3109dd46, approved "
    "guard+schema-only bridges, not latest appmain. HOST740 six non-skipped cases "
    "and native741 TWO named terminalcase0 inherited, not freshly rerun: "
    "ContentSyncONCE/1122kanji5073words131N1/zeroProblems/both accepted epochs1/"
    "224kanjiguards/64surpluschoices/captured pool order/896preservedwordguards/"
    "curatedonlyonじょう/nokun/elevenstrokes/article/Back/offline/fourfont routes. "
    "Both ORIGINAL-session742 dependent guard/rendered confirmations serial with "
    "actual exits/14calls each/zerooverlaps; original733734 and Claude false "
    "serialclaim/nineoverlaps/max9 preserved NOTretroaccepted. No new blind credit. "
    "Full raw readings/titles/levels/support identities preserved, no new word, "
    "TWO all-mapped pairs/FOUR directions/ONE activated baseline pair, seven "
    "preserved word guards. Local quiz_exclusions:[冗] on剰 review-closed only for "
    "compatible-client direct symmetricnontransitive guard; olderclientsignore, "
    "not universal synonym detection/exhaustivepoolcertification/phone/generalrelease. "
    "Next fresh main fetch; if advanced nonrewritingmerge/surgicalreconciliation/"
    "regenerate/revalidate actualcombinedtree/independent changedteaching review/"
    "native-scope reassessment. Then normal signed owner-command-scoped stop-cran "
    "fastforwardpush/noauthswitch/noforcepush/noamend, exactremoteSHA/terminalgreenCI/"
    "EVERYimmutableGitHubZIP runtimeentryhash/manifest equality/18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/"
    "verifiedownerissue/durablepublication ledgers BEFORE100/counting delivery. "
    "Published125/1228,remaining1103,lastpublished098d5a376ee unchanged until "
    "deliveryverified. Physicalphone/generalrelease/whole-set outstanding. "
    "Parent5920 ownsrunner.lock throughoutchildlifetime: verifyliveancestry/"
    "currentrunnersession/checkpoint/exactsignedheads/whollyclean, NOchild "
    "acquire/delete/unlock/readprobe. Approvedcontrol/committedsource/frozeninputs "
    "only; nooptionalhistoricalsessionhelpers. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. No secondrunner/unreviewedpush/batch100."
)
sys.path.insert(0, str(R / "tools"))


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data, replace=False):
    assert replace or not p.exists(), p
    temp = p.with_suffix(p.suffix + ".743.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    os.replace(temp, p)
    assert load(p) == data


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(root), *args],
        encoding="utf-8").strip()


def preflight(label, head=HEAD):
    assert not os.environ.get("GH_TOKEN")
    subprocess.run(["pwsh", "-NoProfile", "-NonInteractive", "-File",
                    str(C / "preflight-743.ps1"), "-ExpectedHead", head,
                    "-ReceiptName", f"preflight-743-{label}.json"], check=True)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("merge-base", MAIN, head) == MAIN


def runtime():
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    evidence = load(S / "execution-739.json")["preparation"]
    archive = Path(evidence["archive"])
    assert archive.is_relative_to(C) and sha(archive) == evidence["archiveSha256"]
    with zipfile.ZipFile(archive) as z:
        names = [n for n in z.namelist() if n.endswith("/manifest.json") or n == "manifest.json"]
        assert len(names) == 1
        prefix = names[0][:-len("manifest.json")]
        assert json.loads(z.read(names[0])) == manifest
        count = 0
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, digest in entries.items():
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert (sha(R / name) if binary else sha256(R / name)) == digest, name
                raw, local = z.read(prefix + name), (R / name).read_bytes()
                if not binary:
                    raw, local = raw.replace(b"\r\n", b"\n"), local.replace(b"\r\n", b"\n")
                assert raw == local and hashlib.sha256(raw).hexdigest() == digest, name
                count += 1
        assert count == 8451 and manifest["contentVersion"] == VERSION
    return {"runtimeHashesVerified": count, "contentVersion": VERSION,
            "manifestSha256": sha(R / "manifest.json"), "manifestFresh": True,
            "compiled739ArchiveSha256": evidence["archiveSha256"],
            "everyNativeArchivePayloadEqual": True, "runtimeChanged": False}


def start():
    preflight("start-representation-checked")
    state = load(C / "progress.json")
    assert state == load(L / "checkpoint-full.json")
    if (L / "progress-before-743.json").exists():
        assert load(L / "progress-before-743.json") == state
    else:
        save(L / "progress-before-743.json", state)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    request_checkpoint = embedded["execution742CoordinatorCheckpoint"]
    live_checkpoint = state["execution742CoordinatorCheckpoint"]
    assert request_checkpoint.keys() == live_checkpoint.keys()
    assert all(value == live_checkpoint[key] for key, value in request_checkpoint.items() if key != "recordedAt")
    assert datetime.fromisoformat(request_checkpoint["recordedAt"]) == datetime.fromisoformat(live_checkpoint["recordedAt"])
    starting = {
        "execution": 743, "batch": "099", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME099 combined-current-main acceptance and normally signed LOCAL review-closed checkpoint; publication next, no100.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed; operative contract, entire approved issue and final742 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": load(L / "preflight-743-start-representation-checked.json"),
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers accessed.",
        "runtime": runtime(), "actualNewPermissionDenials": [],
        "helperDiagnostics": [
            "Initial helper syntax error corrected before execution; no worktree/state change.",
            "Strict request/live comparison stopped before state write on recordedAt timezone formatting only. Exact immutable full snapshot equals live; every other checkpoint field identical and parsed instants equal. Original request/live bytes preserved."
        ],
    }
    save(L / "starting-state-743.json", starting)
    after = copy.deepcopy(state)
    assert "execution743StartingState" not in after
    after["execution743StartingState"] = starting
    after.update(stage="batch-099-combined-main-acceptance-in-progress",
                 nextAction=starting["scope"], blocker=None)
    assert all(after[k] == v for k, v in state.items() if k not in {"stage", "nextAction", "blocker"})
    assert load(C / "progress.json") == state
    save(C / "progress.json", after, replace=True)
    print("SAME099 combined acceptance started; complete history preserved.", flush=True)


def source_audit():
    from audit_n1_pilot import metadata
    path = S / "batch-099-draft-recipe.py"
    spec = importlib.util.spec_from_file_location("frozen099sourceaudit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.C, module.R, module.A, module.L, module.S = C, R, A, L, S
    module.identity = lambda: None
    module.git = git
    captured = {}

    def capture(target, data):
        assert target.parent == S and target.name in {
            "batch-099-draft-audit.json", "batch-099-draft-font-audit.json",
            "batch-099-draft-stroke-audit.json"}
        assert target.name not in captured
        captured[target.name] = data

    module.save = capture
    import contextlib
    audit_log = L / "source-audit-743.txt"
    if audit_log.exists() and not (L / "source-audit-initial-743.txt").exists():
        audit_log.rename(L / "source-audit-initial-743.txt")
        save(L / "source-audit-diagnostic-743.json", {
            "initialFailure": "Archived recipe's git root default was bound at import time to docs/learning-japanese. Failed nonexistent-directory lookup after source/baseline comparisons, before any audit output or evidence write.",
            "remedy": "Bind archived recipe git calls to the current dedicated worktree explicitly; unchanged audit assertions and capture-only outputs. Rerun only source audit, not the already-passed five Python commands.",
            "permissionDenial": False, "originalEvidenceChanged": False})
    if audit_log.exists():
        audit_log = L / "source-audit-normalized-delta-743.txt"
        assert not audit_log.exists()
        save(L / "source-delta-normalization-743.json", {
            "initialComparison": "Strict CRLF/LF comparison stopped after complete source audit; initial Git blob had51 CRLF lines, current text read normalized.",
            "verified": "Under repository-standard CRLF-to-LF normalization the sole difference is exactly quiz_exclusions:[冗]. No runtime byte edit or changed teaching.",
            "permissionDenial": False, "originalEvidenceChanged": False})
    with audit_log.open("x", encoding="utf-8") as output:
        with contextlib.redirect_stdout(output):
            module.audit()
    result = captured["batch-099-draft-audit.json"]
    assert result["currentCounts"] == {"kanji": 1122, "words": 5073, "n1Labels": 131,
                                      "namedSourceMembersPresent": 136}
    assert result["allMappedReciprocalPairs"] == 2 and result["directedLinksVerified"] == 4
    assert metadata(R, f"kanji/{CHAR}.md")["quiz_exclusions"] == ["\u5197"]
    old = subprocess.check_output(["git", "-C", str(R), "show",
        "70dfe3344d167e5152a3685b09689d73fa1cdab1:kanji/" + CHAR + ".md"]).decode("utf-8").replace("\r\n", "\n")
    current = (R / "kanji" / (CHAR + ".md")).read_text(encoding="utf-8")
    assert current == old.replace("distractors: [\u4e57, \u5263, \u5247]\n",
        "distractors: [\u4e57, \u5263, \u5247]\nquiz_exclusions: [\u5197]\n", 1)
    result.update(execution=743, stage=STAGE, combinedContentHead=HEAD, integratedMain=MAIN,
                  reviewClosed=[CHAR], draftOnlyAdditions=[], runtimeAccepted=True,
                  runtimePublished=False, runtime=runtime(), sourceAuditRecipe=path.relative_to(R).as_posix(),
                  sourceAuditRecipeSha256=sha(path),
                  auditReuse="Unchanged committed source-bound audit executed after743 live-parent/signed-head/wholly-clean preflight; original identity replaced only for this current scope, all outputs captured in new receipts, no historical evidence overwritten.",
                  sourceAuditHistoricalFields="Captured729 result contains historical pending-native/limits fields. Those are inherited provenance, superseded only by separately verified740/741/742 within this bounded local acceptance.",
                  supportedKanjiExclusion=[CHAR, "\u5197"],
                  exactOnlyDeltaFromInitialReviewedCard="quiz_exclusions:[\u5197]",
                  limits="Fresh mechanical source/baseline/reading/stroke/link/font audit; inherited host740/native741/rendered742, no fresh linguistic/native/phone evidence.")
    save(L / "combined-source-audit-743.json", result)
    save(L / "combined-font-provenance-743.json", captured["batch-099-draft-font-audit.json"])
    save(L / "combined-stroke-provenance-743.json", captured["batch-099-draft-stroke-audit.json"])
    print("Frozen sources/baseline/all readings/strokes/all mapped links/font provenance passed.", flush=True)


def checks():
    preflight("checks")
    merge = subprocess.run(["git", "-C", str(R), "merge", "--no-edit", "origin/main"],
                           capture_output=True, text=True, encoding="utf-8")
    save(L / "main-integration-743.json", {
        "command": ["git", "merge", "--no-edit", "origin/main"], "exitCode": merge.returncode,
        "stdout": merge.stdout, "stderr": merge.stderr, "main": MAIN, "head": HEAD})
    assert merge.returncode == 0 and git("rev-parse", "HEAD") == HEAD
    assert not git("diff", HEAD + "...origin/main", "--name-only")
    for name, arguments in [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]), ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]:
        command = [sys.executable, "-X", "utf8", "-B", *arguments]
        with (L / f"{name}-743.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-743.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    preflight("after-python")
    source_audit()


def inherit():
    initial = load(V / "batch-099-reconciliation.json")
    rendered = load(V / "batch-099-guard-742-reconciliation.json")
    native = load(S / "execution-741.json")
    host = load(S / "execution-740.json")
    review = load(S / "execution-742.json")
    assert initial["findings"] == [] and initial["serialReviewerProcessesVerified"] and initial["allInternalToolsSerial"]
    previous = None
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        p = initial["processes"][label]
        assert p["actualModels"] == [model] and p["exitCode"] == 0
        assert p["allAssignedRangesReturned"] and not p["observedToolOverlaps"]
        assert sha(V / p["report"]) == p["reportSha256"]
        assert sha(V / f"batch-099-initial-{label}.jsonl") == p["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(p["startedAt"])
        previous = p["completedAt"]
    assert rendered["independentRenderedReviewClosed"] and rendered["changedGuardSemanticReviewClosed"]
    assert review["processesSerial"] and review["actualProcessExitsVerified"]
    assert not rendered["original733734Retroaccepted"] and not review["newBlindReviewCredit"]
    assert all(f["status"] == "resolved" for f in rendered["findings"])
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        p = next(p for p in review["reviewers"] if p["requestedModel"] == model)
        assert p["actualModels"] == [model] and p["exitCode"] == 0
        assert not p["observedToolOverlaps"] and not p["unfinishedTools"]
        assert p["sessionId"] == initial["processes"][label]["sessionId"]
        a = review["supplementaryPacketReturnAudit"][label]
        assert a["allNonblankLinesExactlyEqualAndInOrder"] and a["toolCalls"] == 14 and a["toolOverlaps"] == 0
    hashes = 0
    for row in load(V / "batch-099-guard-review-742" / "artifact-index.json"):
        assert sha(R / row["archive"]) == row["sha256"]
        raw = gzip.decompress((R / row["archive"]).read_bytes()) if row["compressed"] else (R / row["archive"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
        hashes += 1
    for row in load(R / native["artifactIndex"]):
        path = R / row["archive"]
        assert sha(path) == row["sha256"]
        raw = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
        hashes += 1
    assert host["qualifiedAndroidHead"] == APP if "qualifiedAndroidHead" in host else host["command"]["androidHead"] == APP
    assert host["totalTests"] == 6 and all(host[k] == 0 for k in ("failures", "errors", "skipped"))
    assert host["allTestsFreshAfterCommandStart"]
    for row in host["tests"]:
        assert sha(R / row["archive"]) == row["sha256"]
        xml = ET.parse(R / row["archive"]).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(xml.attrib[k] == "0" for k in ("skipped", "errors", "failures"))
        assert {t.attrib["name"] for t in xml.findall("testcase")} == set(row["caseNames"])
        hashes += 1
    assert all((A / module / ".." / ".." / "learning-japanese").resolve() == R for module in ("app", "core"))
    raw = V / "batch-099-guard-native-741" / "raw"
    text = gzip.decompress((raw / "instrumentation.txt.gz").read_bytes()).decode("utf-8-sig")
    assert text.count("INSTRUMENTATION_STATUS_CODE: 0") == 2 and "OK (2 tests)" in text
    for name in ("N1Batch099GuardArticleTest", "N1Batch099GuardGlyphTest",
                 "fullSingleImportGuardedSurplusBothOrientationsFilteredPoolsOfflineRoutesAndSystemBack",
                 "surplusLookalikesAndScopedHanAcrossFourProductionFamilies"):
        assert name in text
    assert all(f"INSTRUMENTATION_STATUS_CODE: {n}" not in text for n in (-2, -3, -4))
    route = json.loads(gzip.decompress((raw / "n1-099-article-route.json.gz").read_bytes()))
    assert route["passed"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"],
            route["acceptedReadingParserEpoch"], route["acceptedMeaningParserEpoch"]) == (1122, 5073, 131, 0, 1, 1)
    assert route["kanjiQuizExclusions"] == ["\u5197"]
    assert route["quizOnKeys"] == ["\u3058\u3087\u3046"] and route["quizKunKeys"] == []
    assert route["touchInjectedReferenceStrokes"] == 11 and route["offline"] and route["reciprocalLinkAndSystemBack"]
    assert len(route["kanjiDirectGuardChecks"]) == 224
    assert len(route["productionBuilderN1AndAllExactChoices"]) == 64
    assert native["preservedWordGuardChecks"] == 896
    assert all("poolMembershipInOrder" in row for row in route["kanjiDirectGuardChecks"])
    assert all("poolMembershipInOrder" in row for row in route["productionBuilderN1AndAllExactChoices"])
    assert native["nativeExecution"]["ownedHelperStopped"] and native["nativeExecution"]["ownedQemuStopped"]
    assert not git("diff", review["archiveSnapshot"], HEAD, "--", "manifest.json")
    ci = load(L / "app-prerequisite-main-ci-743.json")
    assert ci["headSha"] == "2edbf366a4a6fce594b2a6580bfc4252b98d3f6d"
    assert ci["status"] == "completed" and ci["conclusion"] == "success"
    assert ci["jobs"] and all(j["conclusion"] == "success" for j in ci["jobs"])
    return {
        "initialRecord": "docs/n1-reviews/batch-099-reconciliation.json",
        "hostRecord": "docs/n1-sources/execution-740.json",
        "nativeRecord": "docs/n1-sources/execution-741.json",
        "dependentReviewRecord": "docs/n1-reviews/batch-099-guard-742-reconciliation.json",
        "receiptHashesReverified": hashes, "nativeTerminalCaseSuccesses": 2,
        "hostTests": 6, "hostSkipped": 0, "nativeArchiveMatchesEveryCurrentPayload": True,
        "kanjiDirectGuardChecks": 224, "productionSurplusChoiceChecks": 64,
        "preservedWordGuardChecks": 896, "capturedPoolMembershipAndOrder": True,
        "newHostRuns": 0, "newNativeRuns": 0, "newReviewers": 0,
        "approvedAndroidPrerequisiteMainCi": {
            "databaseId": ci["databaseId"], "headSha": ci["headSha"],
            "status": ci["status"], "conclusion": ci["conclusion"]},
        "justification": "No incoming changes and all runtime payloads/manifest plus qualified Android HEAD exactly identical to740/741/742; no redundant heavy run or changed-teaching review needed.",
        "original733734Retroaccepted": False, "newBlindReviewCredit": False,
        "limits": [native["limits"], review["sourceReadScope"], review["imageReadScopePerReviewer"]],
    }


def record():
    preflight("record")
    text = (L / "python-tests-743.txt").read_text(encoding="utf-8")
    count = int(re.search(r"^Ran (\d+) tests in ", text, re.M)[1])
    assert count >= 377 and re.search(r"^OK$", text, re.M) and "skipped=" not in text
    assert (L / "validate-743.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    for name in ("python-tests", "validate", "manifest", "vocabulary", "budget"):
        assert load(L / f"{name}-exit-743.json")["exitCode"] == 0
    budget = ast.literal_eval((L / "budget-743.txt").read_text(encoding="utf-8"))
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    for key, limit in [("entries", MAX_ENTRIES), ("localZipBytes", MAX_COMPRESSED),
                       ("inflatedBytes", MAX_INFLATED), ("retainedBytes", MAX_RETAINED)]:
        assert budget[key] <= limit
    inherited = inherit()
    D.mkdir()
    receipts = []
    sources = [*sorted(L.glob("*-743.txt")), *sorted(L.glob("*-743.json")),
               *sorted(L.glob("preflight-743-*.json")), Path(__file__), C / "preflight-743.ps1",
               C / "post-batch-099-combined-743.ps1",
               C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt"]
    for path in sources:
        if path.name == "progress-before-743.json":
            continue
        raw = path.read_bytes()
        compressed = path.suffix == ".txt"
        target = D / (path.name + (".gz" if compressed else ".txt" if path.suffix == ".ps1" else ""))
        assert not target.exists(), target
        target.write_bytes(gzip.compress(raw, mtime=0) if compressed else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "archiveSha256": sha(target), "losslessGzip": compressed})
    evidence = {
        "schemaVersion": 1, "execution": 743, "batch": "099", "status": STAGE,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "startingState": load(L / "starting-state-743.json"),
        "authoredTeachingSnapshot": "70dfe3344d167e5152a3685b09689d73fa1cdab1",
        "reviewedSnapshot": "1ff076b11b37f2280b7b976746b788a5de842f7c",
        "combinedTestedSnapshot": HEAD, "integratedMain": MAIN,
        "qualifiedAndroidHead": APP, "mainAlreadyAncestor": True,
        "incomingChanges": [], "substantiveTeachingChanged": False,
        "runtime": runtime(), "checks": {
            "pythonTests": count, "validatorErrors": 0, "manifestFresh": True,
            "vocabulary": (L / "vocabulary-743.txt").read_text(encoding="utf-8").strip(),
            "localArchiveBudgets": budget, "freshPythonExecution": True,
            "inheritedAndroidTests": 6, "androidSkipped": 0, "freshAndroidExecution": False,
            "actualResolvedContentRoot": str(R)},
        "sourceAudit": load(L / "combined-source-audit-743.json"),
        "inheritedAcceptance": inherited, "receipts": receipts,
        "reviewClosed": [CHAR], "published": [], "runtimeAccepted": True,
        "runtimeAcceptanceScope": "Local bounded compatible-client owner testing, not public delivery/general release.",
        "runtimePublished": False, "actionableRemainingFindings": 0,
        "consequentialUnresolvedInScopeClaims": 0,
        "changedGuardSemanticReviewClosed": True, "independentRenderedReviewClosed": True,
        "original733734Retroaccepted": False, "newBlindReviewCredit": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": "d5a376ee2b014aae3c47c58eea47b327e44be6d2",
        "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "limits": [
            "Compatible kanji-exclusion-aware and curated-reading client required; old clients ignore both fields.",
            "Direct symmetric nontransitive guard, not universal synonym detection or exhaustive pool certification.",
            "HOST740/native741/dependent confirmations742 inherited, not fresh runs or fresh blind review.",
            "Reviewer panels/contact sheets are not full-resolution reads of every PNG; actual fallback face unidentified.",
            "Injected reference tracing and give-up recall are not human handwriting/MLKit/phone evidence.",
            "Physical-phone/general-release and whole-set acceptance outstanding.",
            "Fresh-main check/normal owner fast-forward/terminal CI/every immutable public ZIP hash and budgets/verified issue remain pending before publication or100.",
        ],
        "nextAction": NEXT,
    }
    save(S / "execution-743.json", evidence)
    save(V / "batch-099-combined-acceptance-743.json", evidence)
    ledger = load(S / "batch-099-progress.json")
    assert "preCombinedAcceptance743" not in ledger
    ledger["preCombinedAcceptance743"] = {
        k: copy.deepcopy(ledger.get(k)) for k in ("status", "reviewClosed", "limits", "nextAction", "pendingGates")}
    ledger.update(status=STAGE, reviewClosed=[CHAR], published=[], runtimeAccepted=True,
                  runtimePublished=False, limits=evidence["limits"], nextAction=NEXT)
    ledger["combinedAcceptance743"] = {
        "evidence": "docs/n1-sources/execution-743.json",
        "reviewRecord": "docs/n1-reviews/batch-099-combined-acceptance-743.json",
        "contentVersion": VERSION, "mainAlreadyAncestor": True, "incomingChanges": [],
        "freshPythonTests": count, "inheritedHostTests": 6, "inheritedHostSkipped": 0,
        "inheritedNativeTerminalSuccesses": 2, "native741StillExact": True,
        "guardAndRendered742Closed": True, "runtimeAccepted": True, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier pending/draft/blocker states remain preserved as historical; superseded only for bounded current compatible-client local acceptance."}
    ledger["pendingGates"] = [
        "Fresh main fetch; if advanced nonrewriting merge/reconcile/regenerate/revalidate actual combined tree and independently review changed teaching/reassess native scope.",
        "Normal signed owner fast-forward, exact remote SHA, terminal green CI, every immutable GitHub ZIP entry/hash under unchanged guards and verified owner issue/durable publication checkpoint before100."]
    save(S / "batch-099-progress.json", ledger, replace=True)
    body = (
        "Batch099 / checkpoint743: **combined-current-main acceptance complete locally; not yet published**.\n\n"
        f"Fresh main`{MAIN[:8]}` is already ancestor of signed`{HEAD[:8]}`; normal nonrewriting merge "
        "returned Already up to date. Zero incoming teaching/runtime changes. All8,451 runtime payload hashes "
        f"and manifest/version`{VERSION}` exactly match compiled739's full archive. "
        f"Fresh combined checks passed:{count} Python tests, validator0 errors, unchanged regenerated manifest, "
        "vocabulary consistency, frozen dictionaries/full baseline/readings/pinned strokes/all mapped links/font provenance "
        "and exact supported guard declaration. Two all-mapped pairs/four directions/one activated baseline; "
        "no new support word, N2\u904e\u5270 identity/readings/seven word guards preserved.\n\n"
        "HOST740 six tests with no skips and native741 two named terminalcase0 successes are inherited, not rerun: "
        "production ContentSyncONCE,1122kanji/5073words/131N1/zero problems/both epochs1,224kanji guards/"
        "64surplus choice sets with pool order/896preserved word guards, curated only on\u3058\u3087\u3046/no kun, "
        "eleven strokes/article/Back/offline/four-font routes. Qualified Android`bf30cdea` includes only the approved "
        "guard/schema bridges, not latest app main. Both original-session742 dependent confirmations closed the "
        "guard/rendered gates with actual serial process exits and14 serial calls each. Original733/734 and Claude's "
        "false serial-read claim/nine overlaps remain historical, not retroaccepted or new blind credit.\n\n"
        f"Local archive:{budget['entries']} entries/{budget['localZipBytes']} compressed/"
        f"{budget['inflatedBytes']} inflated/{budget['retainedBytes']} retained bytes; guards unchanged. "
        "Evidence:`docs/n1-sources/execution-743.json` and `docs/n1-reviews/batch-099-combined-acceptance-743.json`.\n\n"
        "**Next:** fresh-main check, normal authorized owner fast-forward, terminal-green CI and EVERY immutable "
        "GitHub ZIP runtime hash/budget check, then publication ledgers/checkpoint before100. Published coverage "
        "stays125/1228,1103 remaining until delivery verified. Older APKs ignore guards/curation: compatible-client "
        "owner testing only, not universal synonym detection/exhaustive pool certification. Contact-sheet/fallback-face/"
        "injected-drawing limits retained. Phone/general-release/whole-set outstanding. Parent lock untouched; "
        "no optional historical-session helper access or new permission denial.\n")
    (C / "batch-099-combined-743-issue-body.txt").write_text(body, encoding="utf-8")
    print("Bounded local acceptance archived; no runtime edit/publication.", flush=True)


def finalize():
    head = git("rev-parse", "HEAD")
    preflight("final", head)
    assert git("rev-parse", "HEAD^") == HEAD
    e = load(S / "execution-743.json")
    assert e == load(V / "batch-099-combined-acceptance-743.json")
    expected = {r["archive"] for r in e["receipts"]} | {
        "docs/n1-sources/execution-743.json", "docs/n1-reviews/batch-099-combined-acceptance-743.json",
        "docs/n1-sources/batch-099-progress.json"}
    assert set(git("diff", "--name-only", HEAD, head).splitlines()) == expected
    for row in e["receipts"]:
        assert sha(R / row["archive"]) == row["archiveSha256"]
    assert runtime() == e["runtime"]
    posted, receipt = load(L / "issue-743-posted.json"), load(L / "issue-743-reread.json")
    body = (C / "batch-099-combined-743-issue-body.txt").read_bytes().decode("utf-8-sig")
    assert posted["id"] == receipt["id"] and receipt["user"]["login"] == "stop-cran"
    assert posted["body"] == receipt["body"] == body
    before, state = load(L / "progress-before-743.json"), load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 743, "checkpoint": 743, "batch": "099",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "savedCommit": head,
        "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-743.json",
        "reviewRecord": "docs/n1-reviews/batch-099-combined-acceptance-743.json",
        "combinedTestedSnapshot": HEAD, "integratedMain": MAIN, "qualifiedAndroidHead": APP,
        **runtime(), "freshPythonTests": e["checks"]["pythonTests"],
        "inheritedHostTests": 6, "inheritedHostSkipped": 0, "native741StillExact": True,
        "inheritedNativeTerminalSuccesses": 2, "freshHostOrNativeExecuted": False,
        "newReviewers": 0, "incomingChanges": [], "changedGuardSemanticReviewClosed": True,
        "independentRenderedReviewClosed": True, "original733734Retroaccepted": False,
        "reviewClosed": [CHAR], "published": [], "runtimeAccepted": True,
        "runtimeAcceptanceScope": e["runtimeAcceptanceScope"], "runtimePublished": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerIssueAuthorAndBodyVerified": True,
        "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "nextAction": NEXT}
    after = copy.deepcopy(state)
    assert "execution743CoordinatorCheckpoint" not in after
    after["execution743CoordinatorCheckpoint"] = checkpoint
    after.update(checkpoint=743, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    assert load(C / "progress.json") == state
    save(C / "progress.json", after, replace=True)
    assert all(load(C / "progress.json")[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-743.json", checkpoint)
    print("Checkpoint743 persisted; all original historical root values preserved.")
    print(head, receipt["html_url"])


if __name__ == "__main__":
    if sys.argv[1] == "audit":
        preflight("source-audit-normalized-delta")
        source_audit()
    else:
        {"start": start, "checks": checks, "record": record, "finalize": finalize}[sys.argv[1]]()
