"""Archive batch102's local draft evidence and preserve the complete checkpoint history."""
import argparse
import ast
import gzip
import importlib.util
import json
import shutil
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("draft774", C / "draft-batch-102-774.py")
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
R, A, S, L, BASE, MAIN, APP, NEXT = d.R, d.A, d.S, d.L, d.BASE, d.MAIN, d.APP, d.NEXT
load, save, sha, git = d.load, d.save, d.sha, d.git


def record():
    d.identity()
    audit = load(S / "batch-102-draft-audit.json")
    assert audit["allRuntimePayloadHashesVerified"] == 8458 and audit["manifestFresh"]
    checks = {}
    for label in ["tests", "validate", "manifest", "budget", "vocabulary", "audit", "whitespace",
                  "validate-initial-failed"]:
        name = f"{label}-774.txt" if label != "validate-initial-failed" else "validate-774-initial-failed.txt"
        raw = (L / name).read_bytes()
        target = S / f"batch-102-draft-{label}-774.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    assert "Ran 43 tests" in (L / "tests-774.txt").read_text(encoding="utf-8")
    assert (L / "tests-774.txt").read_text(encoding="utf-8").rstrip().endswith("OK")
    assert (L / "validate-774.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    budget = ast.literal_eval((L / "budget-774.txt").read_text(encoding="utf-8"))
    assert budget == {
        "files": 8465, "entries": 8480, "retainedBytes": 44393356, "inflatedBytes": 44661694,
        "localZipBytes": 30301385, "listeningTaskMediaBytes": 5893602,
    }
    helpers = {}
    for name, target in [
        ("draft-batch-102-774.py", "batch-102-draft-recipe.py"),
        ("checkpoint-draft-774.py", "batch-102-draft-checkpoint-recipe.py"),
        ("preflight-774.ps1", "batch-102-preflight-774.ps1.txt"),
        ("checks-batch-102-draft-774.ps1", "batch-102-checks-draft-774.ps1.txt"),
        ("post-batch-102-draft-774.ps1", "batch-102-post-draft-774.ps1.txt"),
    ]:
        shutil.copyfile(C / name, S / target)
        assert (C / name).read_bytes() == (S / target).read_bytes()
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-774.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    shutil.copyfile(L / "preflight-774.json", S / "batch-102-runner-role-774.json")
    starting = load(C / "progress.json")["execution774StartingState"]
    save(S / "execution-774.json", {
        "schemaVersion": 1, "execution": 774, "checkpoint": 774, "batch": "102",
        "stage": "batch-102-local-unreviewed-draft-frozen", "baseCommit": BASE,
        "lastPublishedCommit": MAIN, "androidSignedHead": APP,
        "membership": ["劣"], "sourceRows": [113],
        "draftAudit": audit, "authoringPlan": "batch-102-authoring-plan.json",
        "validation": checks, "localBudget": budget, "durableHelperHashes": helpers,
        "runnerPreflight": role, "authorizationRead": starting["request"],
        "runtimeDrafted": ["劣"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False, "sourcePreparationComplete": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 128, "remainingAdditions": 1100,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [], "nextAction": NEXT,
        "diagnostics": [
            "First request summary output hit cp1252 UnicodeEncodeError after full file loading/parsing; subsequent output explicit UTF-8/ASCII-safe.",
            "Two view calls required bounded ranges after size limits; an authoring-plan range beyond EOF returned no content. Full operative text and final checkpoint then inspected.",
            "Initial validator found a new link to absent奴.md. Removed that link while retaining the source-planned plain component; final validator0. Initial failure preserved, not reclassified as permission denial.",
        ],
        "limits": "Normally signed LOCAL UNREVIEWED recovery freeze only. Not independent content review, app/native/rendered acceptance, push or runtime publication. Original checkpoints and all acceptance gates remain historical/intact. Cmap presence is not rendering evidence; N1-only fallback needs production-builder/native acceptance. Full43-comparison/69-member fresh linguistic reread not claimed.",
    })
    print("Draft audits, validation logs, durable helpers and LOCAL UNREVIEWED evidence archived.")


def signed_clean():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G" and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "origin/main") == MAIN
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    allowed = {"kanji/劣.md", "strokes/劣.json", "words/優劣.md", "words/劣る.md",
               "kanji/優.md", "manifest.json", "docs/n1-sources/execution-774.json"}
    changed = git("-c", "core.quotepath=false", "diff", "--name-only", BASE, head).splitlines()
    assert changed and all(p in allowed or p.startswith("docs/n1-sources/batch-102-") for p in changed)
    return head


def issue():
    head = signed_clean()
    audit = load(S / "batch-102-draft-audit.json")
    body = (
        "Batch 102 / checkpoint 774: **LOCAL UNREVIEWED draft frozen**, not published teaching.\n\n"
        f"Normally signed saved commit: `{head}`; published main remains `{MAIN}`.\n\n"
        "Drafted 劣 (frozen row113), its necessary 優劣ゆうれつ article and six strokes generated "
        "from the exact pinned KanjiVG SVG with the unchanged converter. Full `[レツ] / [おと.る]` "
        "readings/order are retained and selected, with own-row links to 優劣 and existing "
        "劣るおとる (N3); only れつ/おとる are offered. 優劣 covers relative superiority and "
        "inferiority, not inferiority alone. No word-level assignment is inferred.\n\n"
        "The two reused changes are exact navigation-only edits in 劣る and 優 (N3). "
        "All 6,197 pre-existing kanji/word metadata records match the signed source base, "
        "including readings, easier levels, titles and guards. Three all-mapped pairs/six "
        "directions include 優→優劣 and the activated baseline 劣/劣る pair. Three wrong labels "
        "(努/功/省), seven direct symmetric nontransitive kanji guards and four direct word "
        "guards remain subject to independent semantic review. Actual N1-only fallback "
        "acceptance is pending: only 功 among the three curated distractors is N1.\n\n"
        "43 focused tests, validation, regenerated/fresh manifest, vocabulary consistency, "
        "baseline/source/membership/reading/link/stroke/font/hash audits and unchanged "
        f"publishing budgets passed. Draft contentVersion `{audit['contentVersion']}`: all "
        "8,458 runtime hashes verified; 8,453 prior hashes unchanged outside the two navigation "
        "edits. Local archive estimate: 8,480 entries, 30,301,385 compressed bytes, 44,661,694 "
        "inflated bytes and 44,393,356 retained bytes. Exact immutable public ZIP acceptance "
        "remains a later publication gate. All 31 actual Han characters occur in the three "
        "bundled font cmaps; no new RareHan-range character. **This is not native rendering "
        "acceptance**. An initially added link to absent 奴.md was removed; the original failed "
        "validator receipt is retained, and final validation has zero errors.\n\n"
        "69 member plus 43 comparison families and 16 raw character records remain frozen "
        "and freshly match frozen sources mechanically. This author freshly read three "
        "applicable member and nineteen applicable comparison families, seventeen existing "
        "articles, the target character record and all archived public dictionary text blocks, "
        "not all69/43 families again. Original source inspection/read/extraction limitations "
        "remain. No independent reviewer, Android/native run, rendered acceptance or push was "
        "performed. Parent/session/ancestry were verified; parent lock untouched. Helpers "
        "are in approved control and archived with evidence; no optional historical-session "
        "helper or new permission denial.\n\n"
        "**128/1,228 additions published; 1,100 acceptance remainder unchanged.** Compatible "
        "stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 mechanisms "
        "remain required; old clients ignore curation/guards. Six separately placed source "
        "members retain earlier N2 levels. Physical-phone, general-release and whole-set "
        "acceptance remain outstanding. Next: SAME102 two serial blind different-family "
        "initial textual reviews on this signed snapshot, with original reports/read limits "
        "and all subsequent qualified Android/native/rendered, combined-main, signing and "
        "publication gates retained. No103 or second runner.\n"
    )
    (C / "batch-102-draft-774-issue.txt").write_text(body, encoding="utf-8", newline="\n")
    save(C / "issue-request-774.json", {"body": body})
    print("Exact owner issue body generated.")


def finish():
    head = signed_clean()
    posted = load(L / "issue-774-verified.json")
    body = (C / "batch-102-draft-774-issue.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    assert "LOCAL UNREVIEWED draft frozen" in body and head in body
    before = load(L / "progress-before-774.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    audit = load(S / "batch-102-draft-audit.json")
    receipt = {
        "schemaVersion": 1, "execution": 774, "checkpoint": 774, "batch": "102",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-774.json", "draftAudit": audit,
        "membership": ["劣"], "sourceRows": [113], "sourcePreparationComplete": True,
        "runtimeDrafted": ["劣"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 128, "remainingAdditions": 1100,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-102-local-unreviewed-draft-frozen",
        "runtimeManifestHashesVerified": 8458, "contentVersion": audit["contentVersion"],
        "sourceTestsPassed": 43, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None,
    }
    p["execution774CoordinatorCheckpoint"] = receipt
    p["batch102DraftIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": sha(body.encode("utf-8")), "verified": True,
    }
    p["execution774StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p.update(checkpoint=774, status="continue", stage=receipt["stage"], nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-774-final-verification.json", receipt)
    print(json.dumps({k: receipt[k] for k in [
        "checkpoint", "savedCommit", "signature", "status", "stage", "dedicatedWorktreesClean",
        "originalHistoricalRootValuesPreservedExactly", "originalRootKeysCompared", "issueUpdate",
        "runtimeChanged", "runtimePublished", "publishedAdditions", "remainingAdditions",
    ]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["record", "issue", "finish"])
    globals()[parser.parse_args().step]()
