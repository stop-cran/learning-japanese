"""Persist a signed source-only checkpoint without discarding live progress history."""
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
L = C / "logs" / "a0d936ec-01ae-4b86-bd0f-368644d4eba0"
BASE = "ba1a7f467a2431523e3131d4f259c1d3260c93af"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
NEXT = (
    "SAME101 source completion BEFORE runtime drafting. Signed initial packet for frozen row112 "
    "\u529f preserves99 complete member families/one raw character/pinned5pathSVG. This is NOT a "
    "fully prepared authoring plan or independent review. Finish all three reading dispositions "
    "and useful curated own-row linked examples while preserving full source order "
    "[\u30b3\u30a6,\u30af]/[\u3044\u3055\u304a]. Existing\u529f\u7e3e\u3053\u3046\u305b\u304dN2 "
    "and\u6210\u529f\u305b\u3044\u3053\u3046N3 are exact reusable identities; preserve all metadata "
    "and\u529f\u7e3e seven exclusions. Proposed\u30b3\u30a6only; \u30af has actual "
    "\u529f\u5fb3\u304f\u3069\u304f religious evidence, NOT invalid; \u3044\u3055\u304a is a dated "
    "lexical native noun, NOT merely nanori. No new support needed solely to select dated/"
    "specialist readings. Complete comparison families/actual article passages/meaning labels/"
    "three existing defensibly wrong distractors/direct symmetric NONTRANSITIVE guards, "
    "especially\u529f/\u7e3e achievement overlap. FOUR proposed allmappedpairs/EIGHTdirections/"
    "TWOactivatedbaselinepairs include missing existing\u6210-to-\u6210\u529f navigation; "
    "not only new-card links. Finish exact navigation changes, baseline/fullmetadata, proposedHan/"
    "font/canonicalradical/pinnedconverter plan. Only then bounded LOCAL UNREVIEWED draft/freeze. "
    "All original TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/"
    "non-skipped qualifiedAndroid/ContentSyncONCE/native/rendered/combinedcurrentmain/normal "
    "signing/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry"
    "42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia/verifiedownerissue gates remain. "
    "Verify whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. "
    "Parent5920 ownsrunner.lock: no childacquire/delete/unlock/readprobe; approvedcontrol/"
    "committedsource/frozeninputs only, no optional historicalsessionrecipes. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. No unreviewed push,102,authoragents,concurrent "
    "heavywork,secondrunner,signingretry or guardincrease. Published127/1228,1101 acceptance "
    "remainder unchanged. Six earlierN2sourceplacements\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50 "
    "remain separate, never duplicate/relevel. Physicalphone/generalrelease/whole-setoutstanding; "
    "projectincomplete. Initial raw-vs-normalized manifest audit defect preserved/corrected using "
    "production hash helper; runtime bytes unchanged, no content error or permission denial."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".762.tmp")
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
                  "vocabulary", "audit", "audit-762-initial-failed", "whitespace"]:
        source = L / (f"{label}.txt" if label == "audit-762-initial-failed" else f"{label}-762.txt")
        raw = source.read_bytes()
        target = S / (f"batch-101-{label}.txt.gz" if label == "audit-762-initial-failed"
                      else f"batch-101-{label}-762.txt.gz")
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    tests = (L / "source-tests-762.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-762.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    audit = load(S / "batch-101-initial-packet-audit.json")
    assert audit["runtimeManifestHashesVerified"] == 8453 and audit["completeMemberFamilies"] == 99
    helpers = {}
    for name, target in [
        ("source-762.py", "batch-101-source-recipe.py"),
        ("checkpoint-762.py", "batch-101-checkpoint-recipe.py"),
        ("preflight-762.ps1", "batch-101-preflight-762.ps1.txt"),
        ("checks-source-762.ps1", "batch-101-checks-source-762.ps1.txt"),
    ]:
        shutil.copyfile(C / name, S / target)
        assert (C / name).read_bytes() == (S / target).read_bytes()
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-762.json")
    assert role["liveParentPid"] == 5920 and role["coordinatorPid"] == 19732 and not role["lockTouched"]
    shutil.copyfile(L / "preflight-762.json", S / "batch-101-runner-role-762.json")
    save(S / "execution-762.json", {
        "schemaVersion": 1, "execution": 762, "checkpoint": 762, "batch": "101",
        "stage": "batch-101-initial-source-packet-prepared-not-authoring-ready",
        "baseCommit": BASE, "androidSignedHead": APP, "membership": ["\u529f"], "sourceRows": [112],
        "sourcePacketAudit": audit, "sourceObservations": "batch-101-source-observations.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "diagnostic": "batch-101-preparation-diagnostic.json",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 127, "remainingAdditions": 1101,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Normally signed LOCAL source-only checkpoint; no push, independent content review, app/native acceptance or runtime publication. Original checkpoints and all acceptance gates remain historical/intact.",
    })
    print("Source evidence, validations, audit diagnostic and durable helpers archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    body = (
        "Batch 101 / checkpoint 762: **LOCAL source-only checkpoint**, not newly published teaching.\n\n"
        f"Normally signed saved commit: `{head}`; published main remains `{BASE}`.\n\n"
        "Frozen row 112 功: retained and inspected all 99 complete applicable JMdict families, "
        "the full character record, actual dictionary reading headings, and the pinned five-path SVG "
        "(not converted). Verified the five frozen inputs and both decompressed dictionary hashes. "
        "功績こうせき (N2) and 成功せいこう (N3) are exact reusable identities; no new support "
        "article or vocabulary level is inferred. All three source readings stay in original order. "
        "コウ is the provisional useful selection; ク has religious-compound evidence and いさお "
        "is a documented dated lexical noun, not merely a name. Final curation remains source-completion work.\n\n"
        "Four proposed all-mapped pairs include the existing 成→成功 navigation gap; exact quiz "
        "labels/comparison families/direct symmetric nontransitive guards, all links and Han/font "
        "planning still need completion before any runtime draft. No reviewer/app/native run or "
        "publication is claimed here. The original source-audit raw-vs-normalized hash failure is "
        "preserved and corrected by reusing the production text hash helper; no content was changed.\n\n"
        "43 focused source tests, structural validation, unchanged regenerated manifest, vocabulary "
        "consistency, budget check and corrected packet audit passed. All 8,453 runtime manifest "
        "hashes and contentVersion `606c836e4be33ba9` remain unchanged. No guard was raised. "
        "Live parent launcher/session/ancestry were verified; its lock was not touched. Reusable "
        "helpers are in approved control and archived with this packet; no historical session recipe "
        "was accessed and no new permission denial occurred.\n\n"
        "**127/1,228 additions published; 1,101 acceptance remainder unchanged.** "
        "Compatible stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 "
        "mechanisms remain required; six separately placed source "
        "members retain earlier N2 levels. Physical-phone, general-release and whole-set acceptance "
        "remain outstanding. Next: same101 source completion only, preserving every original gate; "
        "no next batch or second runner.\n"
    )
    (C / "issue-762.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G" and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "origin/main") == BASE
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert changed and all(p.startswith("docs/n1-sources/batch-101-") or
                           p == "docs/n1-sources/execution-762.json" for p in changed)
    assert not git("diff", BASE, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    posted = load(L / "issue-762-verified.json")
    expected_body = (C / "issue-762.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == expected_body
    assert "LOCAL source-only" in expected_body and head in expected_body
    before = load(L / "progress-before-762.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    receipt = {
        "schemaVersion": 1, "execution": 762, "checkpoint": 762, "batch": "101",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-762.json", "membership": ["\u529f"], "sourceRows": [112],
        "completeMemberFamilies": 99, "metadataReadingEntries": 3,
        "sourcePreparationComplete": False, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 127, "remainingAdditions": 1101,
        "lastPublishedCommit": BASE, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-101-initial-source-packet-prepared-not-authoring-ready",
        "runtimeManifestHashesVerified": 8453, "contentVersion": "606c836e4be33ba9",
        "sourceTestsPassed": 43, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None,
    }
    p["execution762CoordinatorCheckpoint"] = receipt
    p.update(checkpoint=762, status="continue", batch="101", stage=receipt["stage"],
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-762-final-verification.json", receipt)
    print(json.dumps(receipt, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["record", "issue", "finish"])
    globals()[parser.parse_args().step]()
