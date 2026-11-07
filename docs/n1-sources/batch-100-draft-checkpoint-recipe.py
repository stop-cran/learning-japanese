"""Archive draft evidence and persist the bounded checkpoint with full live history."""
import argparse
import ast
import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "cad52b97-90c7-458e-b57e-f78e2f3cdccd"
BASE = "8a8daf9c63527fb34379346641f4c577dca7623e"
MAIN = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
spec = importlib.util.spec_from_file_location("draft747", C / "draft-batch-100-747.py")
draft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(draft)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, data):
    tmp = path.with_suffix(path.suffix + ".747.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == data
    tmp.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def record():
    draft.identity()
    audit = load(S / "batch-100-draft-audit.json")
    checks = {}
    for label in ["tests", "validate", "manifest", "budget", "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{label}-747.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if label == "tests":
            assert "Ran 43 tests" in text and text.rstrip().endswith("OK") and "skipped" not in text
        elif label == "validate":
            assert text.strip() == "0 error(s)"
        elif label == "manifest":
            assert "8453 files" in text and audit["contentVersion"] in text
        elif label == "audit":
            assert json.loads(text) == audit
        elif label == "vocabulary":
            assert "2122/2431 reviewed prompts; stage=pilot" in text
        elif label == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        else:
            assert not text.strip()
        target = S / f"batch-100-draft-{label}-747.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    failure = (L / "audit-747-first-failed.txt").read_bytes()
    target = S / "batch-100-draft-first-audit-failure-747.txt.gz"
    target.write_bytes(gzip.compress(failure, mtime=0))
    assert gzip.decompress(target.read_bytes()) == failure
    save(S / "batch-100-draft-diagnostic-747.json", {
        "execution": 747,
        "firstAuditFailure": {
            "archive": target.name, "rawSha256": sha(failure),
            "cause": "Control audit mistakenly demanded unchanged whole-file bytes for guard neighbor作 even though its exact Common words link was authorized and already verified by reused_changes. No content or source failure.",
            "remedy": "Retain exact title check for every guard; require unchanged bytes only outside the three exact reused files. Existing batch audit still verifies every reused edit and all metadata. Corrected source/draft audit passed; content was not modified.",
        },
        "navigation": "Initial full-file view requests exceeded tool size limits and were completed using ranges. Archived public HTML initially included scripts/navigation; actual authority-headed entries were then inspected in bounded stripped blocks. A guessed tools/check_vocabulary_consistency.py path did not exist; used existing tools/grammar_vocabulary.py check, no tool added.",
        "fontScope": "Actual final scope has17 Han versus18 proposed: it includes unchanged凶作 as the exact insertion anchor but omits proposed人/口. Complete new card and exact changed passage strings are enumerated, all17 cmaps audited. Only刂 absent in three main fonts; native acceptance pending.",
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "signingBypass": False,
    })
    helpers = {}
    for name, target in [
        ("draft-batch-100-747.py", "batch-100-draft-recipe.py"),
        ("checkpoint-747.py", "batch-100-draft-checkpoint-recipe.py"),
        ("preflight-747.ps1", "batch-100-draft-preflight-747.ps1.txt"),
        ("checks-batch-100-draft-747.ps1", "batch-100-draft-checks-747.ps1.txt"),
        ("post-batch-100-draft-747.ps1", "batch-100-draft-issue-recipe-747.ps1.txt"),
    ]:
        source, dest = C / name, S / target
        shutil.copyfile(source, dest)
        assert source.read_bytes() == dest.read_bytes()
        helpers[target] = sha(dest.read_bytes())
    role = load(L / "preflight-747.json")
    shutil.copyfile(L / "preflight-747.json", S / "batch-100-draft-runner-role-747.json")
    assert not role["lockTouched"] and role["sessionId"] == L.name and role["liveParentPid"] == 5920
    save(S / "execution-747.json", {
        "schemaVersion": 1, "execution": 747, "checkpoint": 747, "batch": "100",
        "stage": "local-unreviewed-draft", "sourceCheckpoint": BASE,
        "publishedBase": MAIN, "androidSignedHead": APP,
        "startingState": load(C / "progress.json")["execution747StartingState"],
        "runtimeDrafted": ["創"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False,
        "contentVersion": audit["contentVersion"], "checks": checks,
        "pythonTestsPassed": 43, "validatorErrors": 0, "localBudget": budget,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "vocabularyLimits": "Existing reviewed-prompt consistency only, not unrelated coverage completion:2122/2431,stage=pilot.",
        "audit": "docs/n1-sources/batch-100-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-100-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-100-draft-stroke-audit.json",
        "diagnostic": "docs/n1-sources/batch-100-draft-diagnostic-747.json",
        "durableHelperHashes": helpers, "runnerPreflight": role,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 126, "remainingAdditions": 1102,
        "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "actualNewPermissionDenials": [], "nextAction": draft.NEXT,
        "limits": "Normally signed LOCAL UNREVIEWED freeze only. Source-only lexical allocation remains explicitly unverified; no independent content review, app/native/font/phone acceptance or publication claimed. All historical records and acceptance gates preserved.",
    })
    print("Local draft, full receipts, diagnostic and durable helper copies archived.")


def signed():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP and git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    names = git("-c", "core.quotepath=false", "diff", "--name-only", BASE, head).splitlines()
    runtime = {"kanji/創.md", "strokes/創.json", "words/創作.md", "words/作る.md", "kanji/作.md", "manifest.json"}
    assert runtime <= set(names)
    assert all(n in runtime or n.startswith("docs/n1-sources/batch-100-")
               or n == "docs/n1-sources/execution-747.json" for n in names)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (746, "100", "continue")
    return head


def issue():
    head = signed()
    target = C / "batch-100-draft-747-issue.txt"
    assert not target.exists()
    target.write_text(
        "Batch 100 checkpoint: **LOCAL UNREVIEWED draft**, not publication.\n\n"
        f"Normally signed local `{head}` freezes source row111 **創**, generated12-stroke geometry "
        "and three exact navigation-only reused changes (創作/作る/作). No new word identity: "
        "創作そうさく N2 and same-family作るつくる N5 retain all metadata and13/5 original exclusions. "
        "Six sourced readings/order preserved; onlyソウ/つく.る selected. Rare創める is limited to "
        "establishment, standalone創きず is a rare spelling rather than pronunciation. "
        "Exactショウ/けず.しける remain explicitly source-only/unverified lexical allocations, "
        "without invented examples, meaning, invalidity or obsolescence claims; neither is quizzed. "
        "Eight direct symmetric nontransitive kanji guards, five all-mapped pairs/ten directions, "
        "one activated baseline pair.\n\n"
        "43 focused tests, validator0 errors, frozen-source/full-family/raw-record, baseline/exact-diff, "
        "reading/link/quiz/font/manifest/budget checks passed; all8453 runtime hashes match "
        "`contentVersion=1bd5fb59e39b080d`. Actual17-Han scope: only刂 absent from three main cmaps; "
        "absence is not glyph failure. Source packets retain137 member+16comparison families and13 "
        "raw character records. One control-audit overstrict unchanged-byte assertion for the authorized "
        "作 insertion was corrected; original failure and remedy preserved, with no content repair. "
        "Reviewed-prompt vocabulary consistency passes at its existing2122/2431 pilot scope, not full coverage.\n\n"
        "Evidence: `docs/n1-sources/execution-747.json`, `batch-100-progress.json`, "
        "`batch-100-draft-audit.json` and font/stroke/diagnostic archives in the same directory. "
        "Next: SAME100 two serial blind different-family textual reviews on this snapshot, "
        "serial internal tools and actual process-exit confirmation; then every original "
        "reconciliation/qualified Android/native/rendered/current-main/signing/publication gate. "
        "No reviewer, Android/native run, push, batch101 or second runner in this checkpoint. "
        "Live parent5920/session ancestry verified; runner.lock untouched; durable control/committed "
        "evidence only, no historical-session recipes or new permission denials. "
        "Published coverage stays **126/1228;1102 acceptance remainder**. Physical-phone, "
        "general-release and whole-set acceptance remain outstanding; project incomplete.\n",
        encoding="utf-8")
    (L / "signed-head-747.txt").write_text(head + "\n", encoding="ascii")
    print("Signed clean local snapshot verified and owner issue body prepared.")


def finish():
    head = signed()
    issue = load(L / "issue-747-verified.json")
    assert issue["user"]["login"] == "stop-cran"
    assert issue["body"] == (C / "batch-100-draft-747-issue.txt").read_text(encoding="utf-8")
    assert head in issue["body"] and "LOCAL UNREVIEWED draft" in issue["body"]
    before, p = load(L / "progress-before-747.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    audit = load(S / "batch-100-draft-audit.json")
    state = {
        "schemaVersion": 1, "execution": 747, "checkpoint": 747, "batch": "100",
        "savedCommit": head, "signature": "G", "sourceCheckpoint": BASE,
        "freshOriginMain": MAIN, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-747.json", "contentVersion": audit["contentVersion"],
        "runtimeDrafted": ["創"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False,
        "metadataReadingDispositions": 6, "onKeys": ["そう"], "kunKeys": ["つくる"],
        "newWords": 0, "changedReusedArticles": 3, "newDirectKanjiExclusionPairs": 8,
        "allMappedReciprocalPairs": 5, "directedLinksVerified": 10, "activatedBaselinePairs": 1,
        "pythonTestsPassed": 43, "validatorErrors": 0, "runtimeHashesVerified": 8453,
        "actualHanCount": audit["actualHanCount"], "mainFontCmapAbsences": audit["pendingNativeFallbackLabels"],
        "sourceOnlyLexicalAllocation": "UNVERIFIED; explicitly limited source-only lookup rows, both excluded from quiz",
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before), "ownerIssueAuthorAndExactBodyVerified": True,
        "issueUpdate": issue["html_url"], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-100-local-unreviewed-draft-frozen",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": draft.NEXT, "blocker": None,
    }
    p["execution747CoordinatorCheckpoint"] = state
    p["execution747StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p.update(checkpoint=747, status="continue", stage=state["stage"], batch="100",
             nextAction=draft.NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    assert persisted == p
    assert all(persisted[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-747-final-verification.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["record", "issue", "finish"])
    globals()[parser.parse_args().step]()
