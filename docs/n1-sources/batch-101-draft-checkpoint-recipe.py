"""Persist batch101's signed LOCAL UNREVIEWED freeze and full-history checkpoint."""
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
L = C / "logs" / "ff1e9841-2508-4a32-b027-5ce26ca5834d"
BASE = "b1da01c20d896866431670213d584c5ca056b096"
MAIN = "ba1a7f467a2431523e3131d4f259c1d3260c93af"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
NEXT = (
    "SAME101 TWO serial blind different-model-family initial textual reviews on the "
    "normally signed LOCAL UNREVIEWED draft; complete功 plus exact navigation-only "
    "words/功績.md words/成功.md kanji/成.md changes, correctness/scoped coverage/phone "
    "comprehensibility on ONE fixed snapshot. Both receive same frozen99member+23comparison "
    "families/18rawcharacterrecords, original authority-headed public blocks and actual labels. "
    "Preserve full[コウ,ク]/[いさお] source order; onlyコウ selected with own-row links to "
    "功績こうせきN2/成功せいこうN3. ク valid religious-compound recognition, いさお dated "
    "lexical noun NOT merely nanori; no new support word/level. Reused metadata/all seven "
    "功績 guards unchanged. FOURallmappedpairs/EIGHTdirections/FIVEnew/TWOactivatedbaselinepairs "
    "include existing成-to-成功. Three wrong labels加幼刀 and THIRTEEN DIRECT symmetric "
    "NONTRANSITIVE guards need independent semantic review, no edits to unrelated cards. "
    "Actual N1-only fallback remains production-builder/native acceptance (two curated choices "
    "outside N1). Canonical力19 right/工 left, five pinned converted paths, structure-unclassified/"
    "labelled modern-shape mnemonic/no adopted etymology. Actual19Han present in all three "
    "bundledcmaps/zeroRareHan is NOT rendered acceptance. Original762read99/763read7applicable+"
    "23comparison/764fresh7applicable+23comparison retained with exact read limits; no fresh99 "
    "reread or independent review claimed. Discover actual CLI model IDs; serial reviewer "
    "processes AND internal tools, actual exit before next reviewer, preserve complete original "
    "reports/models/snapshot/interruptions/readlimits. Reconcile by precise source evidence and "
    "reuse original sessions for bounded changed-passage confirmation. Then fresh non-skipped "
    "qualifiedAndroidbf30cdead RealContent/RareHan, productionContentSyncONCE/native N1/All/"
    "meaning/curatedreading/drawing/article/Back/offline/four-font/all-Han/rendered review, "
    "combinedcurrentmain/allrequiredPython/vocabulary/normal signing/ownerfastforward/"
    "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed80MiB"
    "inflated56MiBretained/perfilepathmedia/verifiedownerissue gates remain mandatory. "
    "No unreviewedpush/102/authoragent/concurrentheavywork/secondrunner/signingretry/"
    "guardincrease. Verify whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/"
    "exactsession. Parent5920 ownsrunner.lock: no childacquire/delete/unlock/readprobe. "
    "Approvedcontrol/committedsource/frozeninputs only, not optional historicalsessionrecipes; "
    "preserve/report/yield actualnewdenial/signinghang/uncertainownership. QualifiedAndroid "
    "approvedpairguard+schemaonly, NOT unrelated latestmain. Published127/1228,1101acceptance "
    "remainder unchanged; six earlierN2placements保案派第策結 separate, never duplicate/relevel. "
    "CompatibleAndroid#125+#132 required; oldclientsignorecuration/guards. Physicalphone/"
    "generalrelease/whole-setoutstanding;projectincomplete. Historical limitations preserved."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".764.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def record():
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    audit = load(S / "batch-101-draft-audit.json")
    assert audit["allRuntimePayloadHashesVerified"] == 8455 and audit["manifestFresh"]
    checks = {}
    for label in ["tests", "validate", "manifest", "budget", "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{label}-764.txt").read_bytes()
        target = S / f"batch-101-draft-{label}-764.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    assert "Ran 43 tests" in (L / "tests-764.txt").read_text(encoding="utf-8")
    assert (L / "tests-764.txt").read_text(encoding="utf-8").rstrip().endswith("OK")
    assert (L / "validate-764.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    ledger = load(S / "batch-101-progress.json")
    ledger["nextAction"] = NEXT
    save(S / "batch-101-progress.json", ledger)
    helpers = {}
    for name, target in [
        ("draft-batch-101-764.py", "batch-101-draft-recipe.py"),
        ("checkpoint-draft-764.py", "batch-101-draft-checkpoint-recipe.py"),
        ("preflight-764.ps1", "batch-101-preflight-764.ps1.txt"),
        ("checks-batch-101-draft-764.ps1", "batch-101-checks-draft-764.ps1.txt"),
        ("post-batch-101-draft-764.ps1", "batch-101-post-draft-764.ps1.txt"),
    ]:
        shutil.copyfile(C / name, S / target)
        assert (C / name).read_bytes() == (S / target).read_bytes()
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-764.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    shutil.copyfile(L / "preflight-764.json", S / "batch-101-runner-role-764.json")
    starting = load(C / "progress.json")["execution764StartingState"]
    save(S / "execution-764.json", {
        "schemaVersion": 1, "execution": 764, "checkpoint": 764, "batch": "101",
        "stage": "batch-101-local-unreviewed-draft-frozen", "baseCommit": BASE,
        "lastPublishedCommit": MAIN, "androidSignedHead": APP,
        "membership": ["功"], "sourceRows": [112],
        "draftAudit": audit, "authoringPlan": "batch-101-authoring-plan.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "authorizationRead": starting["request"],
        "runtimeDrafted": ["功"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False, "sourcePreparationComplete": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 127, "remainingAdditions": 1101,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Normally signed LOCAL UNREVIEWED recovery freeze only. Not independent content review, app/native/rendered acceptance, push or runtime publication. Original checkpoints and all acceptance gates remain historical/intact. Cmap presence is not rendering evidence; N1-only fallback needs actual production-builder/native acceptance.",
    })
    print("Draft audits, validation logs, durable helpers and LOCAL UNREVIEWED evidence archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    body = (
        "Batch 101 / checkpoint 764: **LOCAL UNREVIEWED draft frozen**, not published teaching.\n\n"
        f"Normally signed saved commit: `{head}`; published main remains `{MAIN}`.\n\n"
        "Drafted 功 (frozen row112), with five strokes generated from the exact pinned KanjiVG "
        "SVG using the unchanged converter. Full `[コウ, ク] / [いさお]` source readings/order "
        "remain intact; only コウ is selected, with its own-row links to existing 功績こうせき "
        "(N2) and 成功せいこう (N3). ク remains valid religious-compound recognition; いさお "
        "is a documented dated lexical noun, not merely a personal name. No new support article "
        "or vocabulary level was added.\n\n"
        "The three reused changes are exact navigation-only replacements in 功績, 成功 and 成. "
        "All metadata, easier levels, readings, titles and 功績's seven exclusions are preserved. "
        "Four all-mapped pairs/eight link directions are closed (five new directions), including "
        "two activated baseline pairs and the existing 成→成功 link. Three curated wrong labels "
        "(加/幼/刀) and thirteen conservative direct symmetric nontransitive guards remain "
        "subject to independent semantic review. Actual N1-only fallback acceptance is pending "
        "because two curated choices are outside N1.\n\n"
        "43 focused tests, validation, regenerated/fresh manifest, vocabulary consistency, "
        "baseline/source/membership/reading/link/stroke/font/hash audits and unchanged "
        "publishing budgets passed. Draft contentVersion `6e9b74967e21fc3c`: all 8,455 runtime "
        "payload hashes verified; 8,450 prior payload hashes are unchanged outside the three "
        "navigation edits. Archive estimate: 8,477 entries, 30,297,440 compressed bytes, "
        "44,654,563 inflated bytes and 44,386,225 retained bytes; exact immutable GitHub ZIP "
        "acceptance remains a later publication gate. All nineteen actual Han characters occur "
        "in all three bundled font cmaps, with no new RareHan-range character; **this is not "
        "native rendering acceptance**.\n\n"
        "99 member plus 23 comparison families and 18 raw character records remain frozen and "
        "freshly match the frozen dictionaries mechanically. This author freshly inspected seven "
        "applicable member families and all 23 comparison families, not a fresh99-family read. "
        "No independent reviewer, Android/native run, rendered acceptance or push was performed. "
        "The live parent/session/ancestry were verified; the parent lock was not touched. Helpers "
        "are in approved control and archived with evidence; no optional historical-session "
        "helper was accessed and no new permission denial occurred.\n\n"
        "**127/1,228 additions published; 1,101 acceptance remainder unchanged.** Compatible "
        "stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 mechanisms remain "
        "required. Six separately placed source members retain earlier N2 levels. Physical-phone, "
        "general-release and whole-set acceptance remain outstanding. Next: SAME101 two serial "
        "blind different-family initial textual reviews on this signed snapshot, with original "
        "reports/read limits and all subsequent qualified Android/native/rendered, combined-main, "
        "normal signing and publication gates retained. No102 or second runner.\n"
    )
    (C / "batch-101-draft-764-issue.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G" and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "origin/main") == MAIN
    allowed = {"kanji/功.md", "strokes/功.json", "kanji/成.md", "words/功績.md",
               "words/成功.md", "manifest.json", "docs/n1-sources/execution-764.json"}
    changed = git("-c", "core.quotepath=false", "diff", "--name-only", BASE, head).splitlines()
    assert changed and all(p in allowed or p.startswith("docs/n1-sources/batch-101-") for p in changed)
    posted = load(L / "issue-764-verified.json")
    body = (C / "batch-101-draft-764-issue.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    assert "LOCAL UNREVIEWED draft frozen" in body and head in body
    before = load(L / "progress-before-764.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    audit = load(S / "batch-101-draft-audit.json")
    receipt = {
        "schemaVersion": 1, "execution": 764, "checkpoint": 764, "batch": "101",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-764.json", "draftAudit": audit,
        "membership": ["功"], "sourceRows": [112], "sourcePreparationComplete": True,
        "runtimeDrafted": ["功"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 127, "remainingAdditions": 1101,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-101-local-unreviewed-draft-frozen",
        "runtimeManifestHashesVerified": 8455, "contentVersion": audit["contentVersion"],
        "sourceTestsPassed": 43, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None,
    }
    p["execution764CoordinatorCheckpoint"] = receipt
    p.update(checkpoint=764, status="continue", stage=receipt["stage"], nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-764-final-verification.json", receipt)
    print(json.dumps({k: receipt[k] for k in [
        "checkpoint", "savedCommit", "signature", "status", "stage", "dedicatedWorktreesClean",
        "originalHistoricalRootValuesPreservedExactly", "originalRootKeysCompared", "issueUpdate",
        "runtimeChanged", "runtimePublished", "publishedAdditions", "remainingAdditions",
    ]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["record", "issue", "finish"])
    globals()[parser.parse_args().step]()
