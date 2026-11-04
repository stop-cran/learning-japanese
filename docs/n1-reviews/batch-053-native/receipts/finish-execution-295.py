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
start = "c3880ee222728c1209e988b0d0b6d6563c1bfc38"
published = "e16c95b3edc55975b7a2c7985bf730425baa2f83"


def save(path, data):
    assert not path.exists(), path
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


mode = sys.argv[1]
assert mode in ["precommit", "issue", "checkpoint"]
acceptance = load(reviews / "batch-053-native-acceptance.json")
record_path = sources / "execution-295.json"
record = load(record_path)
assert acceptance["status"] == "native-visual-closed-pending-combined-publication"
assert not acceptance["published"] and record["testsRerun"] is False
for row in acceptance["evidenceCopies"]:
    assert sha(r / row["path"]) == row["sha256"] == sha(Path(row["source"])), row
for label, process in zip(["claude", "gpt"], acceptance["originalReviewerVisualProcesses"]):
    assert len(process["toolCalls"]) == 28 and process["imagePayloadsVerified"] == 21
    assert process["exitCode"] == 0 and not process["observedToolOverlaps"] and not process["unfinishedTools"]
    assert sha(reviews / f"batch-053-visual-{label}.md") == process["reportSha256"]
    assert sha(c / f"batch-053-visual-{label}.jsonl") == process["rawExecutionSha256"]
    for call in process["toolCalls"]:
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
assert not git("diff", record["reviewedTeachingSnapshot"], "--",
               "kanji", "words", "articles", "strokes", "manifest.json")
prep = load(sources / "batch-053-native-preparation.json")
for rel, expected in {**prep["originalFixtureHashesUnchanged"], **prep["originalInitialReportHashesUnchanged"]}.items():
    assert sha(r / rel) == expected
allowed = {
    "status", "limits", "nextAction", "quizAudit", "pendingQualification",
}
for path in [
    reviews / "batch-053-reconciliation.json",
    sources / "batch-053-progress.json",
    sources / "batch-053-review-source-audit.json",
]:
    old = json.loads(git("show", f"{start}:{path.relative_to(r).as_posix()}"))
    current = load(path)
    assert old.keys() <= current.keys()
    assert all(current[k] == old[k] for k in old.keys() - allowed)
    if "quizAudit" in old:
        assert all(current["quizAudit"]["丙"][k] == value for k, value in old["quizAudit"]["丙"].items())
rec = load(reviews / "batch-053-reconciliation.json")
ledger = load(sources / "batch-053-progress.json")
assert rec["findings"] == rec["unresolvedConsequentialClaims"] == []
assert not rec["nativeVisualAcceptancePending"]
assert ledger["published"] == [] and ledger["reviewClosed"] == ["丙"]
android = c.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=android)
before = load(c / "execution-295-starting-progress.json")
progress = load(c / "progress.json")
assert before == progress
assert progress["checkpoint"] == 294
assert progress["lastPublishedCommit"] == published and progress["remainingAdditions"] == 1149
if mode == "precommit":
    assert git("rev-parse", "HEAD") == start
    validation = {}
    for name in ["validate", "manifest", "budget"]:
        source = c / "logs" / f"execution-295-{name}.txt"
        text = source.read_text(encoding="utf-8-sig")
        expected = "0 error(s)" if name == "validate" else "ba2d74eac9ea12e1" if name == "manifest" else "'entries': 8309"
        assert expected in text
        dest = reviews / "batch-053-native" / "receipts" / source.name
        assert not dest.exists()
        shutil.copyfile(source, dest)
        validation[name] = {"exitCode": 0, "sha256": sha(dest), "path": str(dest.relative_to(r))}
    self_copy = reviews / "batch-053-native" / "receipts" / Path(__file__).name
    assert not self_copy.exists()
    shutil.copyfile(Path(__file__), self_copy)
    record["validation"] = validation
    record["validationBoundary"] = (
        "Fresh evidence-only validator/unchanged regenerated manifest/original budgets. "
        "No fresh Python368/vocabulary/current-main acceptance claimed. All68 prior native fixtures/"
        "two initial reports unchanged; full prior live history preserved."
    )
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save(c / "execution-295-precommit-verification.json", {
        "execution": 295, "runtimeUnchanged": True, "oldLedgerUnrelatedValuesPreserved": True,
        "fullLiveHistoryPreserved": True, "originalNativeFixturesUnchanged": 68,
        "originalInitialReportsUnchanged": 2, "evidenceCopiesVerified": len(acceptance["evidenceCopies"]),
        "actualImagePayloadsPerReviewer": [21, 21], "actualViewCalls": [28, 28],
        "toolOverlaps": [0, 0], "validation": validation,
        "publishedAdditions": 79, "remainingAdditions": 1149,
    })
    print("Precommit verified: all61evidence copies/42returned payloads/68original fixtures/two initials/unchanged runtime/history; fresh validator/manifest/budgets passed.")
else:
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == start
    assert git("log", "-1", "--format=%G?") == "G"
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("status", "--porcelain")
    assert git("branch", "--show-current") == "content/n1-kanji"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == published
    body_path = c / "execution-295-issue-body.txt"
    receipt_path = c / "execution-295-issue-receipt.json"
    if mode == "issue":
        assert not body_path.exists() and not receipt_path.exists()
        body = f"""Checkpoint **295 — batch 053 丙 native/visual evidence closed**, signed local commit `{head}` (signature G), **unpublished**. Teaching and all runtime content remain unchanged from reviewed `3e37ebdac9af2880ceaa810ca34a7588d8c1d602`. No batch054 or second runner.

Recovered parent native attempt1 is verified, not rerun: **two actual terminal case0, zero skips, 92.792s**, unchanged compiled fixture. Exact full `93c55a2c17bd61123e2a5bacf1ff47a5c2ad48cf` Git envelope through production **ContentSync once**: **1065 kanji / 5023 words / 85 N1 / zero problems / parser epoch1**, contentVersion **ba2d74eac9ea12e1**; all **8287 canonical runtime hashes** rechecked. Complete ordered **ヘイ / ひのえ**, both curated keys **へい / ひのえ**, actual both-kind session (kun then on) and persisted grade3 assertions. Meaning-correct feedback was **not persisted before Back**. Five generated-reference touch strokes, ungraded trace “Well drawn!”, recall miss and Draw-grade persistence on Next; offline two support reciprocal pairs/four directions plus丙午→existing午/SystemBack. **16 Paint probes/four distinct raster styles each for丙内肉病**.

Both ORIGINAL sessions resumed serially: actual **claude-opus-5.5**, then **gpt-6.1-sol**, each **28 serial view calls / 21 distinct PNGs / zero overlaps, failures or truncations**. First process exited and complete report archived before second launch. Both retain **CLEAN separately for correctness, scoped coverage and comprehensibility** of all three articles, with no actionable teaching defect. Reports, model/process/range/payload receipts and both source1080×2400/returned900×2000 PNG bytes are preserved. **35 source PNGs include21distinct viewports and14hash-equivalent copies**, not35independent views. Actual meaning wrong labels were **monkey / handle; deal with / concave; sunken**, not authored内肉病; both reviewers found one defensible answer. Original metadata-only choice assumption is qualified, not treated as actual pool delivery. Four prior Claude optional groups remain unadopted; stroke-number proximity is nonblocking app rendering outside this kanji task.

All original initial reports and their limitations remain: Claude56calls/two internal overlaps/oversized level-guide read recovered; GPT58calls/zero overlaps and original nine-versus-actual-eight comparison-word count correction. All **68** prior native Kotlin fixtures and two initial reports are unchanged. Original294 permission denial and exact parent-approved discovery/ownership recovery, stopped owned helper/temporary cleanup/unowned5556 untouched are retained. Fresh292 Android **RealContent3 + RareHan1** source/copy XML/UTC/test implementation hashes reverified **without rerun**. Original049 HOST512MiB OOM and existing1GiB :core HOST-Test-only allowance retained; native192m/576m unchanged/no HOST init.

**Limits:** bounded screenshots, clipped reading-table edges, not all columns/full article. Trace first-use download message followed by explicit unavailable handwriting model: **geometry-only**, not ML Kit recognition, human successful recall, negative geometry/reverse-order or phone evidence. Existing午 is route context only, not freshly certified teaching. Operational assertions are supplied actual native evidence, not tests run by reviewers. Current coordinator directly inspected font/drawing/recall images, other pixels have parent and both reviewer provenance. Fresh evidence-only validator **0 errors**, regenerated manifest unchanged and original **18000-entry / 42MiB compressed / 80MiB inflated / 56MiB retained** budgets pass; Python368/vocabulary remain inherited, not newly run here.

Status **continue**; full live history preserved. Next bounded checkpoint: latest-main normal nonrewriting integration, all combined-source/baseline/exact虎[酔っ払い]/猿[馬鹿]/membership/readings/links/strokes/fonts/Python/vocabulary/validator/manifest/budgets, normal signing and owner fast-forward push, actual terminal green CI and every immutable public ZIP runtime hash/terminal receipt before counting delivery or starting054. **Published79/1228,1149remaining**, unchanged. Compatible Android **f9b59a2+** required; physical-phone/general-release and whole-set acceptance explicitly outstanding. No content push/publication performed here.
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
            (c / "logs" / "execution-295-issue-post-stdout.txt").write_bytes(result.stdout)
            (c / "logs" / "execution-295-issue-post-stderr.txt").write_bytes(result.stderr)
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
            "schemaVersion": 1, "execution": 295, "batch": "053",
            "recordedAt": datetime.now().astimezone().isoformat(),
            "globalIdentityBefore": global_before, "globalIdentityAfter": global_after,
            "author": owner, "authorAndBodyVerified": True, "url": url, "savedCommit": head,
            "bodySha256": sha(body_path), "scope": "Local signed evidence checkpoint only; no publication/054.",
        })
        print(url)
    else:
        receipt = load(receipt_path)
        assert receipt["savedCommit"] == head and receipt["authorAndBodyVerified"]
        assert receipt["author"] == "stop-cran" and receipt["bodySha256"] == sha(body_path)
        assert receipt["globalIdentityBefore"] == receipt["globalIdentityAfter"] == "romanko-ms"
        state = copy.deepcopy(progress["execution295StartingState"])
        state.update(
            status="signed-native-visual-evidence-checkpoint", savedCommit=head,
            recordedAt=datetime.now().astimezone().isoformat(), issueUpdate=receipt["url"],
            result="SAME053native2terminal0/Android2923+1reverified/no rerun; originalClaude/GPT28serialcalls21PNGs each0overlaps; no teachingfix. Signed LOCAL evidence only; no publication/054/secondrunner.",
        )
        progress.update(
            checkpoint=295, status="continue", stage=record["stage"], activeExecution=state,
            execution295CoordinatorCheckpoint=copy.deepcopy(state),
            nextAction=record["nextAction"], blocker=None,
        )
        progress["batch053NativeVisualCheckpoint"] = {
            "execution": 295, "savedCommit": head, "signature": "G",
            "acceptance": record["acceptance"], "actualModels": record["actualModels"],
            "calls": [28, 28], "pngReturns": [21, 21], "overlaps": [0, 0],
            "nativeCaseCodes": [0, 0], "android292Cases": 4, "testsRerun": False,
            "issueUpdate": receipt, "published": False, "publishedAdditions": 79,
            "remainingAdditions": 1149, "limits": record["limits"], "nextAction": record["nextAction"],
        }
        allowed_progress = {"checkpoint", "status", "stage", "activeExecution", "nextAction", "blocker"}
        assert before.keys() <= progress.keys()
        assert all(before[k] == progress[k] for k in before.keys() - allowed_progress)
        temporary = c / "execution-295-progress.tmp"
        assert not temporary.exists()
        temporary.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        assert load(temporary) == progress
        temporary.replace(c / "progress.json")
        assert load(c / "progress.json") == progress
        save(c / "execution-295-final-verification.json", {
            "execution": 295, "checkpoint": 295, "status": "continue", "savedCommit": head,
            "signature": "G", "dedicatedWorktreesClean": True, "fullHistoricalValuesPreserved": True,
            "ownerIssueReadbackVerified": True, "issueUrl": receipt["url"],
            "runtimeUnchanged": True, "nativeVisualClosed": True, "published": False,
            "lastPublishedCommit": published, "publishedAdditions": 79, "remainingAdditions": 1149,
            "overallProjectComplete": False, "nextAction": record["nextAction"],
        })
        print(f"Checkpoint295 continue persisted/verified; signed local {head}; full history and owner readback preserved. No publication.")
