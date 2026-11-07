"""Preserve one source-backed direct quiz guard and its bounded checkpoint."""
import base64
import copy
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "769afa09-4939-437e-a930-32c6a1328574"
HEAD = "da2905cd8eee44011d02582076101d47ec97daa9"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
STAGE = "corrected-local-freeze-awaiting-original-session-confirmations"
NEXT = (
    "SAME094 only: read docs/n1-sources/execution-684.json and "
    "batch-094-correction-audit-684.json. One direct 削る/縮める guard appended; "
    "normal signed LOCAL correction only, not runtime acceptance/publication. Obtain "
    "bounded confirmations from BOTH original sessions Claude edf22897-9f87-4a3b-b20f-4c2fd839013a "
    "and GPT 65fd64ff-aae2-40af-927e-bf19b52fecb6, serial processes AND serial tool reads, "
    "on the same corrected snapshot with exact diff, own original finding and frozen "
    "JMdict1298090 sense2/1337570 sense1. Preserve original683 overlap/rejection/repair. "
    "Then exact corrected manifest/full-archive production ContentSync ONCE and focused "
    "production builder checks for this direct pair, both directions/both target "
    "orientations/All+custom with non-skipped native evidence as applicable. Native682 "
    "and all85 unchanged visual captures remain inherited, NOT corrected-import evidence. "
    "No repeat full121families or85captures absent a new concern. Fresh current-main "
    "normal merge/reconcile, changed-teaching review and all combined content/Python/"
    "vocabulary/baseline/link/membership/reading/font/budget/applicable Android checks "
    "remain; normal signing, owner fastforward, terminalgreenCI, EVERY immutable public "
    "ZIP runtime hash,18000entries/42MiBcompressed/80MiBinflated/56MiBretained/"
    "perfile-media-safepath and verified ownerissue gates unchanged. No095, publication "
    "or secondrunner at this checkpoint. Parent19008 retains runner.lock: verify live "
    "ancestry/session/signedheads/whollyclean; NO child acquire/delete/unlock. Approved "
    "control/committed packets only, no optional historicalsessionhelpers. Preserve/"
    "report/yield actual new denial/signinghang/uncertainownership. Qualified TESTONLY "
    "Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. No new Android/native, "
    "phone/humanhandwriting/successfulMLKit claim. Published120/1228,1108remaining "
    "unchanged; physicalphone/generalrelease/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))


def load(p):
    return json.loads(p.read_bytes())


def save(p, value):
    temp = p.with_suffix(p.suffix + ".684.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(p)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, repo=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(repo), *args], encoding="utf-8").strip()


def ownership():
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    script = f"""
$id={os.getpid()}; $chain=@()
while($id -gt 0){{
 $p=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(!$p){{break}}
 $chain+=@{{pid=[int]$p.ProcessId;parent=[int]$p.ParentProcessId;name=$p.Name;command=$p.CommandLine}}
 if($id -eq 19008){{break}}
 $id=$p.ParentProcessId
}}
$chain | ConvertTo-Json -Depth 4 -Compress
"""
    chain = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert chain[-1]["pid"] == 19008
    assert any(p["name"].lower() == "copilot.exe" and L.name in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    launcher = (C / "runner.ps1").read_text(encoding="utf-8-sig")
    assert "$lock.Dispose()" in launcher
    assert "'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None'" in launcher
    return {"parentPid": 19008, "session": L.name, "decodedLauncherMatches": True,
            "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
            "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain]}


def identity(clean=False, final=False):
    proof = ownership()
    assert git("rev-parse", "HEAD^" if final else "HEAD") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    if clean:
        assert not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "HEAD", repo=A) == APP
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", repo=A)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (683, "094", "continue")
    return proof


def start():
    proof = identity(clean=True)
    p = load(C / "progress.json")
    before = L / "progress-before-684.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution683CoordinatorCheckpoint"] == p["execution683CoordinatorCheckpoint"]
    p["execution684StartingState"] = {
        "execution": 684, "batch": "094",
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME094 one direct quiz guard, exact audits and normally signed LOCAL correction freeze; yield before original-session confirmations/native/publication/095.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and complete embedded checkpoint decoded. Operative contract, complete issue and final683 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": proof,
        "artifactPathPreflight": "Approved control and committed packets only; no optional historical-session helper accessed.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-094-observed-direct-guard-correction-in-progress",
             nextAction=p["execution684StartingState"]["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Execution684 starting state persisted with all historical values preserved.")


def ledger():
    identity()
    p = load(S / "batch-094-progress.json")
    row = next(r for r in p["wordQuizAudit"]["directExclusions"] if r["word"] == "削る")
    previous = copy.deepcopy(row)
    assert row["exclude"] == ["切る", "減らす", "省く", "消す", "除く", "外す"]
    before = "quiz_exclusions: [" + ", ".join(row["exclude"]) + "]"
    row["exclude"].append("縮める")
    row["added"].append("縮める")
    row["status"] = "additional-observed-pair-awaiting-original-session-confirmations"
    row["observedPairEvidence684"] = {
        "pair": ["削る", "縮める"],
        "finding": "docs/n1-reviews/batch-094-rendered-reconciliation-683.json:094-observed-kezuru-chijimeru",
        "completeFamilies": "docs/n1-reviews/batch-094-rendered-observed-pair-683.xml",
        "senses": {"1298090": [2], "1337570": [1]},
        "reason": "Observed All seeds7/15 in both directions; ordinary cut-down/reduce and shorten/reduce senses overlap. Direct pair only, not transitive closure or unrestricted substitution.",
    }
    after = "quiz_exclusions: [" + ", ".join(row["exclude"]) + "]"
    p["changedReusedPassages"].append({
        "article": "words/削る.md", "before": before, "after": after,
        "reason": "Observed source-backed direct 削る/縮める quiz guard; original exclusions/order and all prose preserved.",
    })
    p["quizSafeguardCorrection684"] = {
        "previousSnapshot": HEAD, "priorDeclaration679": previous,
        "directPair": ["削る", "縮める"], "before": before, "after": after,
        "status": "applied-awaiting-original-session-confirmations-and-corrected-import",
        "bodiesUnchanged": True, "originalExclusionsAndOrderPreserved": True,
    }
    save(S / "batch-094-progress.json", p)
    print("One additive direct guard recorded; original679 declaration archived unchanged.")


def audit():
    identity()
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256

    old_word = subprocess.check_output(
        ["git", "-C", str(R), "show", f"{HEAD}:words/削る.md"])
    new_word = (R / "words" / "削る.md").read_bytes()
    before = "quiz_exclusions: [切る, 減らす, 省く, 消す, 除く, 外す]".encode()
    after = "quiz_exclusions: [切る, 減らす, 省く, 消す, 除く, 外す, 縮める]".encode()
    assert old_word.count(before) == 1 and new_word == old_word.replace(before, after, 1)
    result = batch_audit(R, "094")
    baseline = load(S / "baseline-inventory.json")
    exceptions = copy.deepcopy(load(S / "batch-094-correction-audit-679.json")["baselineMetadataExceptions"])
    exceptions["words/削る.md"] = metadata(R, "words/削る.md")["quiz_exclusions"]
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = ["川", "出", "木"]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    old = json.loads(subprocess.check_output(["git", "-C", str(R), "show", f"{HEAD}:manifest.json"]))
    current = load(R / "manifest.json")
    assert build_manifest(R) == current
    changed = []
    verified = 0
    for section, entries in current.items():
        if isinstance(entries, dict):
            assert entries.keys() == old[section].keys()
            for name, digest in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == digest, name
                if digest != old[section][name]:
                    changed.append(name)
                verified += 1
    assert verified == 8438 and changed == ["words/削る.md"]
    changed_paths = set(git("-c", "core.quotepath=false", "diff", HEAD, "--name-only",
                            "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools").splitlines())
    assert changed_paths == {"words/削る.md", "manifest.json"}
    p = load(S / "batch-094-progress.json")
    pairs = {(c, r["article"]) for r in p["supportMappings"]
             for c in metadata(R, r["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert pairs == {tuple(r) for r in p["allMappedReciprocalPairs"]} and len(pairs) == 3
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    observed = R / "docs" / "n1-reviews" / "batch-094-rendered-observed-pair-683.xml"
    assert sha(observed) == "5bb1f9aec869ecce6a61c8cfafa761aa0ad39f2002c898559bb43d270fef3ce4"
    result.update(
        execution=684, correctionBase=HEAD, oneDirectPairAdded=["削る", "縮める"],
        exactByteReplacement=True, allOtherRuntimePayloadsUnchanged=8437,
        allRuntimePayloadHashesVerified=verified, runtimeMembershipUnchanged=True,
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=exceptions, allMappedReciprocalPairs=3, directedLinksVerified=6,
        originalExclusionsAndOrderPreserved=True, observedCompleteFamilyPacketSha256=sha(observed),
        oldContentVersion=old["contentVersion"], contentVersion=current["contentVersion"],
        inheritedFontGeometrySourceEvidence="docs/n1-sources/batch-094-correction-audit-679.json and execution-682.json; all applicable article bodies, curation, geometry, fonts and source packets unchanged",
        originalSessionConfirmations="pending", correctedNativeImportAndBuilderChecks="pending",
        runtimeAccepted=False, runtimePublished=False, freshAndroidOrNativeClaimed=False,
        parentLockTouched=False, actualNewPermissionDenials=[],
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding")
    save(S / "batch-094-correction-audit-684.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def evidence():
    identity()
    checks = {}
    for name in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        source = L / f"{name}-684.txt"
        raw = source.read_bytes()
        if name == "tests":
            assert b"Ran 43 tests" in raw and raw.rstrip().endswith(b"OK")
        if name == "validate":
            assert raw.decode("utf-8-sig").strip() == "0 error(s)"
        target = S / f"batch-094-correction-{name}-684.txt.gz"
        assert not target.exists()
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[name] = {"path": target.relative_to(R).as_posix(), "sha256": sha(target),
                        "uncompressedSha256": sha(source)}
    target = S / "batch-094-correction-recipe-684.py"
    assert not target.exists()
    shutil.copyfile(Path(__file__), target)
    save(S / "execution-684.json", {
        "schemaVersion": 1, "execution": 684, "batch": "094", "status": STAGE,
        "startingState": load(C / "progress.json")["execution684StartingState"],
        "correctionBase": HEAD, "directPair": ["削る", "縮める"],
        "finding": "docs/n1-reviews/batch-094-rendered-reconciliation-683.json:094-observed-kezuru-chijimeru",
        "findingDisposition": "safeguard applied; original-session confirmations and corrected native import/builder evidence pending, not fully resolved",
        "checks": checks, "focusedTestsPassed": 43, "validatorErrors": 0,
        "audit": "docs/n1-sources/batch-094-correction-audit-684.json",
        "recipe": target.relative_to(R).as_posix(), "recipeSha256": sha(target),
        "contentVersion": load(R / "manifest.json")["contentVersion"],
        "runtimeChanged": True, "runtimeAccepted": False, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": "48765e20846e1d6769c6ddc35146f6ce58deab57",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": [
            "One direct pair, not transitive closure or unrestricted lexical equivalence. Titles, identities, easier levels, readings, bodies, links and stroke geometry unchanged.",
            "Original683 rejected overlap and accepted serial repair remain preserved; no new review credit.",
            "Native682 and unchanged rendered evidence inherited only; changed manifest/full-archive import and exact builder acceptance still required.",
            "No Android/native/phone/human handwriting/MLKit/general-release/whole-set acceptance or publication claimed.",
        ], "nextAction": NEXT,
    })
    print("Correction evidence archived for normal signed LOCAL freeze.")


def finalize():
    identity(clean=True, final=True)
    e = load(S / "execution-684.json")
    assert sha(S / "batch-094-correction-recipe-684.py") == e["recipeSha256"]
    for row in e["checks"].values():
        path = R / row["path"]
        assert sha(path) == row["sha256"]
        assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == row["uncompressedSha256"]
    posted = load(C / "batch-094-correction-684-issue-posted.json")
    receipt = load(C / "batch-094-correction-684-issue-receipt.json")
    body = (C / "batch-094-correction-684-issue-body.txt").read_bytes().decode("utf-8-sig")
    assert posted["body"] == receipt["body"] == body
    assert posted["user"]["login"] == receipt["user"]["login"] == "stop-cran"
    p = load(C / "progress.json")
    before = load(L / "progress-before-684.json")
    record = {
        "schemaVersion": 1, "execution": 684, "checkpoint": 684, "batch": "094",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G",
        "status": "continue", "stage": STAGE, "evidence": "docs/n1-sources/execution-684.json",
        "audit": "docs/n1-sources/batch-094-correction-audit-684.json",
        "directPairAdded": ["削る", "縮める"], "focusedTestsPassed": 43,
        "validatorErrors": 0, "runtimeHashesVerified": 8438,
        "contentVersion": e["contentVersion"], "runtimeChanged": True,
        "runtimeAccepted": False, "runtimePublished": False,
        "originalSessionConfirmations": "pending", "correctedNativeImportAndBuilderChecks": "pending",
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 120, "remainingAdditions": 1108,
        "lastPublishedCommit": e["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    p["execution684StartingState"]["status"] = "signed-local-correction-freeze-complete"
    p["execution684CoordinatorCheckpoint"] = record
    p["batch094ObservedQuizCorrectionCheckpoint"] = copy.deepcopy(record)
    p.update(checkpoint=684, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    assert all(persisted[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-684-verification.json", record)
    print(json.dumps(record, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    {"start": start, "ledger": ledger, "audit": audit, "evidence": evidence,
     "finalize": finalize}[sys.argv[1]]()
