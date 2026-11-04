import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
reviews = r / "docs" / "n1-reviews"
sources = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
start = "73593c32886b12443c6da65b9b6c2e393ba01ace"
published = "672266d5fffae425e608cdfa5a631ac147d1d08c"


def save(path, data):
    assert not path.exists(), path
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


mode = sys.argv[1]
assert mode in ["precommit", "issue", "checkpoint"]
acceptance = load(reviews / "batch-054-native-acceptance.json")
record_path = sources / "execution-304.json"
record = load(record_path)
assert acceptance["status"] == "native-visual-closed-pending-combined-publication"
assert not acceptance["published"] and record["testsRerun"] is False
for row in acceptance["evidenceCopies"]:
    assert sha(r / row["path"]) == row["sha256"] == sha(Path(row["source"]))
for label, process in zip(["claude", "gpt"], acceptance["originalReviewerVisualProcesses"]):
    assert len(process["toolCalls"]) == 24 and process["imagePayloadsVerified"] == 18
    assert process["exitCode"] == 0 and not process["observedToolOverlaps"] and not process["unfinishedTools"]
    assert sha(reviews / f"batch-054-visual-{label}.md") == process["reportSha256"]
    assert sha(c / f"batch-054-visual-{label}.jsonl") == process["rawExecutionSha256"]
    for call in process["toolCalls"]:
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
assert not git("diff", record["reviewedTeachingSnapshot"], "--", "kanji", "words", "articles", "strokes", "manifest.json")
prep = load(sources / "batch-054-native-preparation.json")
for rel, expected in {**prep["originalFixtureHashesUnchanged"], **prep["originalInitialReportHashesUnchanged"]}.items():
    assert sha(r / rel) == expected
for path in [
    reviews / "batch-054-reconciliation.json",
    sources / "batch-054-progress.json",
    sources / "batch-054-review-source-audit.json",
]:
    old = json.loads(git("show", f"{start}:{path.relative_to(r).as_posix()}"))
    current = load(path)
    assert old.keys() <= current.keys()
    assert all(current[key] == old[key] for key in old.keys() - {"status", "limits", "nextAction"})
    assert current["preNativeVisualClosure"] == {key: old[key] for key in ["status", "limits", "nextAction"] if key in old}
rec = load(reviews / "batch-054-reconciliation.json")
ledger = load(sources / "batch-054-progress.json")
assert rec["findings"] == rec["unresolvedConsequentialClaims"] == []
assert not rec["nativeVisualAcceptancePending"]
assert ledger["published"] == [] and ledger["reviewClosed"] == ["且"]
android = c.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=android)
before = load(c / "execution-304-starting-progress.json")
progress = load(c / "progress.json")
assert before == progress and progress["checkpoint"] == 303
assert progress["lastPublishedCommit"] == published and progress["remainingAdditions"] == 1148
if mode == "precommit":
    assert git("rev-parse", "HEAD") == start
    validation = {}
    for name in ["validate", "manifest", "budget"]:
        source = c / "logs" / f"execution-304-{name}.txt"
        text = source.read_text(encoding="utf-8-sig")
        expected = "0 error(s)" if name == "validate" else "fa89fc674144b377" if name == "manifest" else "'entries': 8312"
        assert expected in text
        dest = reviews / "batch-054-native" / "receipts" / source.name
        assert not dest.exists()
        shutil.copyfile(source, dest)
        validation[name] = {"exitCode": 0, "sha256": sha(dest), "path": str(dest.relative_to(r))}
    self_copy = reviews / "batch-054-native" / "receipts" / Path(__file__).name
    assert not self_copy.exists()
    shutil.copyfile(Path(__file__), self_copy)
    record["validation"] = validation
    record["validationBoundary"] = (
        "Fresh evidence-only validator/unchanged regenerated manifest/original budgets. "
        "No fresh Python368/vocabulary/current-main acceptance claimed. All70 prior native fixtures/"
        "two initial reports unchanged; full prior live history preserved."
    )
    record["remoteMainObservedNotIntegrated"] = git("ls-remote", "origin", "refs/heads/main").split()[0]
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save(c / "execution-304-precommit-verification.json", {
        "execution": 304, "runtimeUnchanged": True, "oldLedgerUnrelatedValuesPreserved": True,
        "fullLiveHistoryPreserved": True, "originalNativeFixturesUnchanged": 70,
        "originalInitialReportsUnchanged": 2, "evidenceCopiesVerified": len(acceptance["evidenceCopies"]),
        "actualImagePayloadsPerReviewer": [18, 18], "actualViewCalls": [24, 24],
        "toolOverlaps": [0, 0], "validation": validation,
        "remoteMainObservedNotIntegrated": record["remoteMainObservedNotIntegrated"],
        "publishedAdditions": 80, "remainingAdditions": 1148,
    })
    print("Precommit verified: all18receipts/36returnedpayloads/70originalfixtures/twoinitials/unchangedruntime/history; freshvalidator/manifest/budgets passed.")
else:
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == start
    assert git("log", "-1", "--format=%G?") == "G"
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("status", "--porcelain")
    assert git("branch", "--show-current") == "content/n1-kanji"
    body_path = c / "execution-304-issue-body.txt"
    receipt_path = c / "execution-304-issue-receipt.json"
    if mode == "issue":
        assert not body_path.exists() and not receipt_path.exists()
        body = f"""Checkpoint **304 — batch 054 且 native/visual evidence closed**, normally signed local commit `{head}` (signature G), **unpublished**. Teaching and runtime content unchanged from reviewed `4fb51498f6912169499456031380ce2353373397`. No batch055, test rerun, content push or second runner.

Both ORIGINAL sessions resumed strictly serially: actual **claude-opus-5.5** (`1bed2f69-6d63-4a81-91f7-05f664ff3030`) then **gpt-6.1-sol** (`572484bf-b4d8-4206-94b6-d046f9157dc7`), each **24 serial view calls / 18 distinct PNGs / zero overlaps, failed or truncated reads**. Actual terminal session IDs/model identities/exits verified; first complete report archived before second launch. Both retain **CLEAN separately for correctness, scoped coverage and comprehensibility** of complete 且 and 且つ, with no actionable teaching defect. Reports, prompts, process/range/payload receipts and separate source1080×2400/returned900×2000 bytes/hashes preserved.

Native303 attempt1 evidence reverified, **not rerun**: **two terminal case0, zero skips,118.893s**, unchanged compiled302fixture and exact signed `b957500752f3f62f5228706db9f1ea6d4a17d0ed` full envelope. Production **ContentSync once** imported **1066 kanji / 5024 words / 86 N1 / zero problems / parser epoch1**, schema1 EN/ja, contentVersion **fa89fc674144b377**; all **8290 current/frozen runtime hashes** matched. Ordered **ショ・ソ・ショウ／か.つ** preserved in Full/Lite; on[] and kun[か.つ], keyかつ. One necessary 且つかつ support/one reciprocal pair/two directions/nine direct guards/no inferred word level.

**20 Paint probes/four production rows** show distinguishable 且目日助 and readable 苟. 苟 shares one fallback design; its actual face remains unidentified. THREE bundled cmaps lack 苟—not evidence that the Gothic/system face lacks it. Claude's overbroad four-font wording and near-identical-content/every-cell wording are qualified in the reconciliation without editing the original report. **32sourcePNGs/18distincthashes/14additional hash-equivalentcopies** remain separate from visual-context counts. Table opposite edges/qualification tails clip; こうしょ wraps. No every-cell/all-columns/full-article certification. Both reviewers note the visible sideways-scroll hint; wrapping is optional app polish, outside this task.

Actual meaning fallback labels are **Japanese cedar/chicken/mosquito**, not authored目日助; one defensible answer. Kun choices **まつ/たつ/かえで/かつ**, correctかつ and persistedGood assertion; full lookup readings in feedback do not become practice keys. Five generated-reference touch strokes/ungraded trace, explicit unavailable handwriting model/**geometry-only** feedback, recall miss and Draw persistence on Next; offline reciprocal/SystemBack route. Meaning feedback was **not persisted before Back**. This is **not ML Kit recognition, human successful recall, negative geometry, reverse order or phone evidence**. Synthetic due source/historical meaning logs are not owner progress.

Fresh301Android **RealContent3 + RareHan1** source/copy XML/UTC/testimplementation hashes reverified **without rerun**. All70 prior native fixtures/two blind reports unchanged. Initial Claude56calls/one internal overlap and GPT55calls/zero/all32resources retained; five Claude optional suggestions unadopted. Comparative register remains **UNVERIFIED and omitted**, not a formal-only ban. Owned303helpers stopped/unowned5556 untouched/temporary source-assets absent/Androidclean retained. Guest192m/576m unchanged; requested2048MB auto2560MB/MemTotal2532900kB. Original049HOST512MiBOOM/existing1GiB :core HOSTTest-only allowance remains **not guest/native authorization**.

Fresh evidence-only validator **0 errors**, regenerated manifest unchanged and original **18000-entry / 42MiB compressed / 80MiB inflated / 56MiB retained** budgets pass. Python368/vocabulary/source-baseline audit remain explicitly inherited—not newly rerun here. Current coordinator directly inspected font/drawing/recall images; remaining pixels retain303andbothreviewer provenance. Reviewers inspected pixels/fixture, not underlying operational runs.

Status **continue**, full live history preserved. Next bounded gate: fresh latest-main normal nonrewriting integration, all combined source/baseline/exact虎[酔っ払い]/猿[馬鹿]/membership/readings/links/strokes/fonts/Python/vocabulary/validator/manifest/budgets, normal owner signing/fast-forward publication, actual terminal green CI and every immutable public ZIP runtime hash/terminal receipt before counting054delivery or starting055. **Published80/1228,1148remaining**, unchanged. Compatible Android **f9b59a2+** required; physical-phone/general-release and whole-set acceptance explicitly outstanding.
"""
        body_path.write_text(body, encoding="utf-8")
        global_before = subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip()
        assert global_before == "romanko-ms"
        token = subprocess.check_output(["gh", "auth", "token", "--user", "stop-cran"], text=True).strip()
        child_env = dict(os.environ, GH_TOKEN=token)
        try:
            owner = subprocess.check_output(["gh", "api", "user", "--jq", ".login"], env=child_env, text=True).strip()
            assert owner == "stop-cran"
            result = subprocess.run(
                ["gh", "issue", "comment", "60", "--repo", "stop-cran/learning-japanese", "--body-file", str(body_path)],
                env=child_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            (c / "logs" / "execution-304-issue-post-stdout.txt").write_bytes(result.stdout)
            (c / "logs" / "execution-304-issue-post-stderr.txt").write_bytes(result.stderr)
            assert result.returncode == 0, "Owner issue update failed; exact output retained, no retry."
            url = result.stdout.decode("utf-8").strip()
        finally:
            child_env.pop("GH_TOKEN", None)
            token = None
        comment_id = url.split("#issuecomment-")[1]
        comment = json.loads(subprocess.check_output(
            ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{comment_id}"],
        ))
        assert comment["user"]["login"] == owner
        assert comment["body"].replace("\r\n", "\n").strip() == body.strip()
        assert comment["html_url"] == url
        global_after = subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip()
        assert global_after == global_before
        save(receipt_path, {
            "schemaVersion": 1, "execution": 304, "batch": "054",
            "recordedAt": datetime.now().astimezone().isoformat(),
            "globalIdentityBefore": global_before, "globalIdentityAfter": global_after,
            "author": owner, "authorAndBodyVerified": True, "url": url, "savedCommit": head,
            "bodySha256": sha(body_path), "scope": "Local signed evidence checkpoint only; no publication/055.",
        })
        print(url)
    else:
        receipt = load(receipt_path)
        assert receipt["savedCommit"] == head and receipt["authorAndBodyVerified"]
        assert receipt["author"] == "stop-cran" and receipt["bodySha256"] == sha(body_path)
        assert receipt["globalIdentityBefore"] == receipt["globalIdentityAfter"] == "romanko-ms"
        state = copy.deepcopy(progress["execution304StartingState"])
        state.update(
            status="signed-native-visual-evidence-checkpoint", savedCommit=head,
            recordedAt=datetime.now().astimezone().isoformat(), issueUpdate=receipt["url"],
            result="SAME054 native303two terminal0/Android3013+1reverified/no rerun; originalClaude/GPT24serialcalls18PNGs each0overlaps; no teachingfix. Signed LOCAL evidence only; no publication/055/secondrunner.",
        )
        progress.update(
            checkpoint=304, status="continue", stage=record["stage"], activeExecution=state,
            execution304CoordinatorCheckpoint=copy.deepcopy(state),
            nextAction=record["nextAction"], blocker=None,
        )
        progress["batch054NativeVisualCheckpoint"] = {
            "execution": 304, "savedCommit": head, "signature": "G",
            "acceptance": record["acceptance"], "actualModels": record["actualModels"],
            "calls": [24, 24], "pngReturns": [18, 18], "overlaps": [0, 0],
            "nativeCaseCodes": [0, 0], "android301Cases": 4, "testsRerun": False,
            "issueUpdate": receipt, "published": False, "publishedAdditions": 80,
            "remainingAdditions": 1148, "limits": record["limits"], "nextAction": record["nextAction"],
        }
        allowed = {"checkpoint", "status", "stage", "activeExecution", "nextAction", "blocker"}
        assert before.keys() <= progress.keys()
        assert all(before[key] == progress[key] for key in before.keys() - allowed)
        temporary = c / "execution-304-progress.tmp"
        assert not temporary.exists()
        temporary.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        assert load(temporary) == progress
        temporary.replace(c / "progress.json")
        assert load(c / "progress.json") == progress
        save(c / "execution-304-final-verification.json", {
            "execution": 304, "checkpoint": 304, "status": "continue", "savedCommit": head,
            "signature": "G", "dedicatedWorktreesClean": True, "fullHistoricalValuesPreserved": True,
            "ownerIssueReadbackVerified": True, "issueUrl": receipt["url"],
            "runtimeUnchanged": True, "nativeVisualClosed": True, "published": False,
            "lastPublishedCommit": published, "publishedAdditions": 80, "remainingAdditions": 1148,
            "overallProjectComplete": False, "nextAction": record["nextAction"],
        })
        print(f"Checkpoint304 continue persisted/verified; signed local {head}; fullhistory and owner readback preserved. No publication.")
