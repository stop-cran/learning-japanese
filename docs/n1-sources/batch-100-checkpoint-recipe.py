"""Archive and finalize the source-only batch100 checkpoint, preserving live history."""
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
L = C / "logs" / "b54e1c11-ed77-4905-8fc1-6f5f338723d1"
BASE = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
NEXT = (
    "SAME100 source completion BEFORE runtime drafting. Signed initial packet for frozen row111 創 "
    "retains137 complete member families/one raw character/pinned12pathSVG; observations are NOT "
    "a fully prepared authoring plan or independent review. Resolve qualified source-only treatment "
    "of exact ショウ and けず.しける without asserting error/invalidity, silently repairing/dropping/"
    "reordering metadata or inventing examples. Complete six reading dispositions, useful curated "
    "keys and exact-spelling necessary support; true existing 創作そうさく N2 identity preserves "
    "thirteen exclusions. Full1597890作る/造る/創る usage tendencies are not fixed compartments; "
    "1307550創める rare spelling cannot inherit 始める-only senses1/3; 1580260創きず rare spelling "
    "does not make the pronunciation rare. Extract/inspect complete comparison families and actual "
    "reused/quiz passages; all-mapped+activated links including existing作/創作 pair; exact labels/"
    "ordinary secondary senses/direct nontransitive guards; full proposedHan/font/canonicalradical/"
    "pinnedconverter plan. Only then bounded LOCAL UNREVIEWED runtime draft/freeze. All original "
    "TWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmation/non-skipped "
    "qualifiedAndroid/ContentSyncONCE/native/rendered/combinedcurrentmain/normal signing/owner "
    "fastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed"
    "80MiBinflated56MiBretained/perfilepathmedia/verifiedownerissue gates remain. No unreviewed push, "
    "101, authoragents, concurrent heavy work, secondrunner, signingretry or guardincrease. "
    "Verify whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. "
    "Parent5920 ownsrunner.lock: no childacquire/delete/unlock/readprobe; use approvedcontrol/"
    "committedsource/frozeninputs only, not optional historicalsessionrecipes. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. Published126/1228,1102 acceptance remainder "
    "unchanged; six earlierN2sourceplacements保案派第策結 remain separate, never duplicate/relevel. "
    "Physicalphone/generalrelease/whole-setoutstanding; projectincomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".745.tmp")
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
        source = L / f"{label}-745.txt"
        raw = source.read_bytes()
        target = S / f"batch-100-{label}-745.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    assert "Ran 43 tests" in (L / "source-tests-745.txt").read_text(encoding="utf-8")
    assert (L / "source-tests-745.txt").read_text(encoding="utf-8").rstrip().endswith("OK")
    assert (L / "validate-745.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    helpers = {}
    for source, target in [
        (C / "source-745.py", S / "batch-100-source-recipe.py"),
        (C / "checkpoint-745.py", S / "batch-100-checkpoint-recipe.py"),
        (C / "preflight-745.ps1", S / "batch-100-preflight-745.ps1.txt"),
        (C / "checks-source-745.ps1", S / "batch-100-checks-source-745.ps1.txt"),
        (L / "preflight-745-original.ps1.txt", S / "batch-100-preflight-745-original.ps1.txt"),
    ]:
        shutil.copyfile(source, target)
        assert source.read_bytes() == target.read_bytes()
        helpers[target.name] = sha(target.read_bytes())
    role = load(L / "preflight-745.json")
    assert role["liveParentPid"] == 5920 and role["coordinatorPid"] == 26872 and not role["lockTouched"]
    shutil.copyfile(L / "preflight-745.json", S / "batch-100-runner-role-745.json")
    save(S / "execution-745.json", {
        "schemaVersion": 1, "execution": 745, "checkpoint": 745, "batch": "100",
        "stage": "batch-100-initial-source-packet-prepared-not-authoring-ready",
        "baseCommit": BASE, "androidSignedHead": APP, "membership": ["創"], "sourceRows": [111],
        "sourcePacketAudit": load(S / "batch-100-initial-packet-audit.json"),
        "sourceObservations": "batch-100-source-observations.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "diagnostic": "batch-100-preflight-diagnostic.json",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 126, "remainingAdditions": 1102,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Normally signed LOCAL source-only checkpoint; no push, content review, app/native acceptance or runtime publication. Original checkpoints and all acceptance gates remain historical/intact.",
    })
    print("Source evidence, validations, original preflight failure and durable helpers archived.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G" and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "origin/main") == BASE
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert changed and all(p.startswith("docs/n1-sources/batch-100-") or
                           p == "docs/n1-sources/execution-745.json" for p in changed)
    assert not git("diff", BASE, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    issue = load(L / "issue-745-verified.json")
    expected_body = (C / "issue-745.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == expected_body
    assert "LOCAL source-only" in expected_body and head in expected_body
    before = load(L / "progress-before-745.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    receipt = {
        "schemaVersion": 1, "execution": 745, "checkpoint": 745, "batch": "100",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-745.json", "membership": ["創"], "sourceRows": [111],
        "completeMemberFamilies": 137, "metadataReadingEntries": 6,
        "sourcePreparationComplete": False, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 126, "remainingAdditions": 1102,
        "lastPublishedCommit": BASE, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": issue["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-100-initial-source-packet-prepared-not-authoring-ready",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
    }
    p["execution745CoordinatorCheckpoint"] = receipt
    p.update(checkpoint=745, status="continue", batch="100", stage=receipt["stage"],
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-745-final-verification.json", receipt)
    print(json.dumps(receipt, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["record", "finish"])
    args = parser.parse_args()
    globals()[args.step]()
