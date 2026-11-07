"""Save the signed source-completion checkpoint and preserve all live history."""
import argparse
import gzip
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "4e67593f-d049-419a-bffc-99f4ebf29f79"
BASE = "1a25e38563f59f91b50cfaa3a8d8329ef2acd6f2"
MAIN = "ba1a7f467a2431523e3131d4f259c1d3260c93af"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
NEXT = (
    "SAME101 bounded LOCAL UNREVIEWED runtime draft/freeze only from completed "
    "docs/n1-sources/batch-101-authoring-plan.json and its preparation audit. "
    "Frozen row112\u529f; preserve [\u30b3\u30a6,\u30af]/[\u3044\u3055\u304a] in source order; "
    "select only\u30b3\u30a6 with its own-row linked\u529f\u7e3e\u3053\u3046\u305b\u304dN2/"
    "\u6210\u529f\u305b\u3044\u3053\u3046N3; \u30af is valid religious recognition and "
    "\u3044\u3055\u304a a dated lexical noun, NOT merely nanori. No new support needed. "
    "Three EXACT navigation-only reused changes: words/\u529f\u7e3e.md, words/\u6210\u529f.md, "
    "kanji/\u6210.md. Preserve full metadata, easier levels, readings, titles and all seven "
    "\u529f\u7e3e exclusions. FOUR allmappedpairs/EIGHTdirections/THREEalready/FIVEnew/"
    "TWOactivatedbaselinepairs include existing\u6210-to-\u6210\u529f navigation. "
    "Proposed merit;achievement label, THREE wrong choices\u52a0\u5e7c\u5200 and THIRTEEN "
    "conservative DIRECT symmetric NONTRANSITIVE guards; actual N1-only fallback remains "
    "later production-builder/native acceptance work (two curated choices are not N1). "
    "All99 memberfamilies retained;763 freshly read7 applicable plus23 completecomparison/"
    "18 rawcharacter records/19existingarticles; do not claim fresh99family reread or independent "
    "review. Proposed20Han all present in three cmaps/zero newRareHan; NOT rendered acceptance. "
    "Generate strokes only using pinned five-path SVG and unchanged converter; no hand geometry "
    "or adopted etymology. Actual draft baseline/reading/link/quiz/font/membership audits, "
    "validator and regenerated manifest precede normal signed LOCAL freeze. No reviewer/"
    "Android/native/publication/102 in that draft checkpoint. All original TWOserialblind"
    "differentfamilies/serialinternaltools/originalsessionconfirmation/non-skipped qualified"
    "Android/ContentSyncONCE/native/rendered/combinedcurrentmain/normal signing/ownerfastforward/"
    "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed80MiBinflated"
    "56MiBretained/perfilepathmedia/verifiedownerissue gates remain. Verify whollyclean signedheads/"
    "freshmain/liveparentancestry/decodedlauncher/exactsession. Parent5920 ownsrunner.lock: "
    "NOchildacquire/delete/unlock/readprobe; approvedcontrol/committedsource/frozeninputs only, "
    "NOoptional historicalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. QualifiedsignedAndroidbf30cdead8515739bc0e671d57a54b9a3109dd46 "
    "is approvedpairguard+schemaonly, NOT unrelated latestmain. No unreviewed push/authoragents/"
    "concurrent heavywork/secondrunner/signingretry/guardincrease. Published127/1228,1101 "
    "acceptance remainder unchanged. Six earlierN2placements\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50 "
    "remain separate, never duplicate/relevel. CompatibleAndroid#125+#132 required; oldclients"
    "ignorecuration/guards. Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. "
    "All historical source/review/process/permission/OOM/pending limitations preserved; no retroacceptance."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".763.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def record():
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    checks = {}
    for label in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                  "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{label}-763.txt").read_bytes()
        target = S / f"batch-101-{label}-763.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    tests = (L / "source-tests-763.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-763.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    audit = load(S / "batch-101-preparation-audit.json")
    assert audit["runtimeManifestHashesVerified"] == 8453 and audit["sourcePreparationComplete"]
    helpers = {}
    for name, target in [
        ("source-763.py", "batch-101-source-completion-recipe.py"),
        ("checkpoint-763.py", "batch-101-source-completion-checkpoint-recipe.py"),
        ("preflight-763.ps1", "batch-101-preflight-763.ps1.txt"),
        ("checks-source-763.ps1", "batch-101-checks-source-763.ps1.txt"),
    ]:
        shutil.copyfile(C / name, S / target)
        assert (C / name).read_bytes() == (S / target).read_bytes()
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-763.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    shutil.copyfile(L / "preflight-763.json", S / "batch-101-runner-role-763.json")
    starting = load(C / "progress.json")["execution763StartingState"]
    save(S / "execution-763.json", {
        "schemaVersion": 1, "execution": 763, "checkpoint": 763, "batch": "101",
        "stage": "batch-101-source-prepared-not-drafted", "baseCommit": BASE,
        "lastPublishedCommit": MAIN, "androidSignedHead": APP,
        "membership": ["\u529f"], "sourceRows": [112],
        "sourcePreparationAudit": audit, "authoringPlan": "batch-101-authoring-plan.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "authorizationRead": starting["request"],
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 127, "remainingAdditions": 1101,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Normally signed LOCAL source-completion checkpoint; no push, independent content review, app/native/rendered acceptance or runtime publication. Original checkpoints and all acceptance gates remain historical/intact. Cmap presence is not rendering evidence; conservative guards require actual later builder/default fallback checks.",
    })
    print("Source-completion evidence, validation results and durable helpers archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    body = (
        "Batch 101 / checkpoint 763: **LOCAL source completion**, not newly published teaching.\n\n"
        f"Normally signed saved commit: `{head}`; published main remains `{MAIN}`.\n\n"
        "Completed the authoring plan for frozen row112 功: all three full readings stay in "
        "source order `[コウ, ク] / [いさお]`; only コウ is proposed for practice with the existing "
        "功績こうせき (N2) and 成功せいこう (N3). ク has verified religious-compound evidence; "
        "いさお is a documented dated lexical noun, not merely a name. Both remain qualified "
        "recognition material. No new support article or vocabulary level is needed.\n\n"
        "The original 99 complete member families remain preserved; this execution freshly read "
        "seven applicable member families, 23 complete comparison families and 19 existing "
        "articles, and inspected the relevant Japanese/English fields of 18 full character records. "
        "The exact navigation-only plan closes four mapped reciprocal pairs/eight directions "
        "(three already present, five proposed), including the existing 成→成功 gap and two "
        "activated baseline pairs. All existing metadata, easier levels, and 功績's seven "
        "word exclusions are preserved in in-memory simulations.\n\n"
        "Planned meaning choices are 加/幼/刀, with 13 conservative direct symmetric "
        "nontransitive guards based on actual displayed labels/secondary senses, not a synonym "
        "clique. Two curated choices are outside N1, so actual N1-only fallback-builder/label "
        "acceptance remains explicitly pending. Twenty proposed Han characters occur in all "
        "three bundled font cmaps; this is **not native rendering acceptance**. The pinned "
        "five-path SVG and unchanged converter are verified, not converted in this checkpoint.\n\n"
        "43 focused source tests, validation, unchanged regenerated manifest, vocabulary "
        "consistency, source/baseline/link/font audits and unchanged publishing budgets passed. "
        "All 8,453 runtime manifest hashes and contentVersion `606c836e4be33ba9` are unchanged. "
        "No runtime drafting, reviewer, app/native execution, push or acceptance is claimed. "
        "Live parent/session/ancestry were verified; the parent lock was not touched. Helpers "
        "reside in approved control and are archived with the source evidence; no optional "
        "historical session helper was accessed and no new permission denial occurred.\n\n"
        "**127/1,228 additions published; 1,101 acceptance remainder unchanged.** Compatible "
        "stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 mechanisms remain "
        "required. Six separately placed source members retain earlier N2 levels. Physical-phone, "
        "general-release and whole-set acceptance remain outstanding. Next: SAME101 bounded "
        "LOCAL UNREVIEWED runtime draft/freeze only, preserving every later two-family review, "
        "qualified Android/native/rendered, combined-main/signing/publication gate. No102 or second runner.\n"
    )
    (C / "issue-763.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G" and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "origin/main") == MAIN
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert changed and all(p.startswith("docs/n1-sources/batch-101-") or
                           p == "docs/n1-sources/execution-763.json" for p in changed)
    assert not git("diff", BASE, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    posted = load(L / "issue-763-verified.json")
    expected_body = (C / "issue-763.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == expected_body
    assert "LOCAL source completion" in expected_body and head in expected_body
    before = load(L / "progress-before-763.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    audit = load(S / "batch-101-preparation-audit.json")
    receipt = {
        "schemaVersion": 1, "execution": 763, "checkpoint": 763, "batch": "101",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-763.json",
        "authoringPlan": "docs/n1-sources/batch-101-authoring-plan.json",
        "preparationAudit": audit, "membership": ["\u529f"], "sourceRows": [112],
        "sourcePreparationComplete": True, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 127, "remainingAdditions": 1101,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-101-source-prepared-not-drafted",
        "runtimeManifestHashesVerified": 8453, "contentVersion": "606c836e4be33ba9",
        "sourceTestsPassed": 43, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None,
    }
    p["execution763CoordinatorCheckpoint"] = receipt
    p.update(checkpoint=763, status="continue", stage=receipt["stage"], nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-763-final-verification.json", receipt)
    print(json.dumps({k: receipt[k] for k in [
        "checkpoint", "savedCommit", "signature", "status", "stage",
        "sourcePreparationComplete", "dedicatedWorktreesClean",
        "originalHistoricalRootValuesPreservedExactly", "originalRootKeysCompared", "issueUpdate",
        "runtimeChanged", "publishedAdditions", "remainingAdditions",
    ]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["record", "issue", "finish"])
    globals()[parser.parse_args().step]()
