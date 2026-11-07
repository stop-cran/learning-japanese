"""Persist the batch100 completed-source checkpoint without losing live history."""
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
L = C / "logs" / "7af9c34a-0eb0-446e-a0c2-4e6b5aee3383"
BASE = "961b94b6e9456a6f55585482c67b9cb8c4d0c2e7"
MAIN = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
NEXT = (
    "SAME100 bounded LOCAL UNREVIEWED runtime draft/freeze only from completed source plan "
    "docs/n1-sources/batch-100-authoring-plan.json and preparation-audit.json. Frozen row111 創: "
    "137complete member+16comparison families/13raw character records; six exact readings preserved "
    "in source order. Proposed quizソウ/つく.る, keysそう/つくる. Reuse創作そうさく N2 and "
    "same-family作るつくる N5 (explicitly teaches創る); zero new word identities, preserve "
    "thirteen/five original exclusions and metadata. No rigid作る/造る/創る compartments or "
    "cooking/crop substitutions. Rare spelling創める limited to establishment sense2, not "
    "始める-only senses1/3; rare standalone創きず does not makeきず pronunciation rare. "
    "ショウ/けず.しける remain exact, explicitly qualified source-only lookup tokens: no verified "
    "lexical allocation/gloss, no invented examples/invalidity/obsolescence/source repair; "
    "both excluded from quiz. FIVE all-mapped pairs/TENdirections/FIVEexisting/FIVEnew, "
    "ONEactivatedbaselinepair; exact THREEreused changes: 創作 componentlink, 作る existing創る "
    "componentlink, 作 Commonwords創作 link. Proposedtitle originate; create; three actual wrong "
    "labels剣/倹/験 and eight DIRECTnontransitive guards作造始元原本緒産 require final semantic "
    "review, no edits to unrelated existing cards. Explain canonical刀18 as right-hand刂; "
    "structure-unclassified/no unverified phonetic/etymology. Convert pinned12pathSVG using "
    "unchanged tools/generate_strokes.py; no hand geometry. Proposed18Han includes刂 absent in "
    "three maincmaps; absence is NOT glyphfailure; final actualHan/font/native checks mandatory. "
    "Draft actualsource/reading/link/quiz/font/baseline audits, validator and regenerated manifest "
    "before normal signed LOCAL UNREVIEWED freeze; no reviewer/Android/native/publication/101 "
    "during that draft checkpoint. All later TWOserialblinddifferentfamilies/serialinternaltools/"
    "originalsessionconfirmation/non-skipped qualifiedAndroidbf30cdead/ContentSyncONCE/native/"
    "rendered/combinedcurrentmain/normal signing/ownerfastforward/terminalgreenCI/EVERYimmutableZIP"
    "manifesthash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia/"
    "verifiedownerissue gates remain mandatory. No unreviewedpush/authoragents/concurrentheavywork/"
    "secondrunner/signingretry/guardincrease. Verify whollyclean signedheads/freshmain/liveparent"
    "ancestry/decodedlauncher/exactsession. Parent5920 ownsrunner.lock: no childacquire/delete/"
    "unlock/readprobe. Approvedcontrol/committedsource/frozeninputs only, not optional historical"
    "sessionrecipes; preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Published126/1228,1102acceptanceremainder unchanged; six earlierN2placements保案派第策結 "
    "remain separate, never duplicate/relevel. Physicalphone/generalrelease/whole-setoutstanding; "
    "projectincomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".746.tmp")
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
        raw = (L / f"{label}-746.txt").read_bytes()
        target = S / f"batch-100-{label}-746.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    tests = (L / "source-tests-746.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-746.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    helpers = {}
    for source, target in [
        (C / "source-746.py", S / "batch-100-source-completion-recipe.py"),
        (C / "checkpoint-746.py", S / "batch-100-source-completion-checkpoint-recipe.py"),
        (C / "preflight-746.ps1", S / "batch-100-preflight-746.ps1.txt"),
        (C / "checks-source-746.ps1", S / "batch-100-checks-source-746.ps1.txt"),
    ]:
        shutil.copyfile(source, target)
        assert source.read_bytes() == target.read_bytes()
        helpers[target.name] = sha(target.read_bytes())
    role = load(L / "preflight-746.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    shutil.copyfile(L / "preflight-746.json", S / "batch-100-runner-role-746.json")
    audit = load(S / "batch-100-preparation-audit.json")
    assert audit["runtimeHashesVerified"] == 8451 and audit["runtimeBytesUnchanged"]
    save(S / "batch-100-source-completion-diagnostic.json", {
        "execution": 746,
        "requestRead": "Entire request loaded/decoded and checkpoint parsed before acting. Initial console output failed under cp1252 after loading; UTF-8 output enabled and final checkpoint inspected. No input was skipped.",
        "firstAudit": "Control-only helper initially normalized too few textual manifest categories and failed at curriculum/grammar.json. Inspected actual build_manifest.py; matched its five textual and four binary maps with an explicit category guard. Subsequent complete audit passed all8451 hashes; no runtime bytes were changed or repaired.",
        "navigation": "Candidate lookups kanji/検.md and kanji/倉.md were absent, not permission denials. Neither is used as a distractor. 倉 is only a visible shape label grounded in pinned SVG; no reading/meaning allocation is invented.",
        "actualNewPermissionDenials": [],
        "signingBypass": False,
        "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False
    })
    save(S / "execution-746.json", {
        "schemaVersion": 1, "execution": 746, "checkpoint": 746, "batch": "100",
        "stage": "batch-100-source-prepared-not-drafted", "baseCommit": BASE,
        "freshOriginMain": MAIN, "androidSignedHead": APP, "membership": ["創"], "sourceRows": [111],
        "sourcePreparationComplete": True, "authoringPlan": "batch-100-authoring-plan.json",
        "sourcePacketAudit": audit, "validation": checks, "durableHelperHashes": helpers,
        "runnerPreflight": role, "diagnostic": "batch-100-source-completion-diagnostic.json",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 126, "remainingAdditions": 1102,
        "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Normally signed LOCAL source-completion checkpoint only, not a runtime draft, independent review or publication. All original acceptance gates/history remain. Source-only lexical allocation remains explicitly unverified rather than silently repaired.",
    })
    print("Source plan, validations, diagnostics and durable control helpers archived.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G" and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "origin/main") == MAIN
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert changed and all(p.startswith("docs/n1-sources/batch-100-") or
                           p == "docs/n1-sources/execution-746.json" for p in changed)
    assert not git("diff", BASE, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    issue = load(L / "issue-746-verified.json")
    expected_body = (C / "issue-746.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == expected_body
    assert "LOCAL source-completion" in expected_body and head in expected_body
    before, p = load(L / "progress-before-746.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    audit = load(S / "batch-100-preparation-audit.json")
    receipt = {
        "schemaVersion": 1, "execution": 746, "checkpoint": 746, "batch": "100",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "freshOriginMain": MAIN,
        "androidSignedHead": APP, "evidence": "docs/n1-sources/execution-746.json",
        "membership": ["創"], "sourceRows": [111], "completeMemberFamilies": 137,
        "completeComparisonFamilies": 16, "completeRawCharacterRecords": 13,
        "sourcePreparationComplete": True, "metadataReadingDispositions": 6,
        "proposedOnKeys": ["そう"], "proposedKunKeys": ["つくる"],
        "proposedNewSupportArticles": 0, "proposedReusedSupportArticles": 2,
        "allMappedReciprocalPairs": 5, "requiredDirectedLinks": 10,
        "alreadyExistingDirections": 5, "newDirectionsRequired": 5,
        "proposedNewDirectKanjiGuards": 8, "proposedHanCount": 18,
        "mainFontCmapAbsences": audit["mainFontCmapAbsences"],
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 126, "remainingAdditions": 1102,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": issue["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-100-source-prepared-not-drafted",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
    }
    p["execution746CoordinatorCheckpoint"] = receipt
    p.update(checkpoint=746, status="continue", batch="100", stage=receipt["stage"],
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-746-final-verification.json", receipt)
    print(json.dumps(receipt, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["record", "finish"])
    globals()[parser.parse_args().step]()
