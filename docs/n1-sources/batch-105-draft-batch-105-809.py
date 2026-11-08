"""Batch105 bounded local draft receipts; never reviews or publishes content."""
import argparse
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "1a8efc89-5c08-4ef4-8a51-6813b11bd676"
HEAD = "ddd01d5fea912de7a3d43cd25bdc631b5e0ac0ed"
MAIN = "047c2cef6b6a48b1738f2c5957de01be481c63e1"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
sys.path.insert(0, str(R / "tools"))
sys.stdout.reconfigure(encoding="utf-8")


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def save(p, v):
    tmp = p.with_suffix(p.suffix + ".809.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(v, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == v
    tmp.replace(p)


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=root)


def role():
    runner = load(C / "runner.json")
    assert runner["pid"] == 13320 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    ps = r"""
$ErrorActionPreference='Stop'
$id=$PID; $chain=@()
for($i=0;$i -lt 7 -and $id;$i++){
 $x=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(-not $x){break}
 $chain+=@{pid=[int]$x.ProcessId;parent=[int]$x.ParentProcessId;name=$x.Name}
 $id=$x.ParentProcessId
}
$r=Get-CimInstance Win32_Process -Filter 'ProcessId=13320'
if(-not $r){throw 'Parent absent'}
$encoded=($r.CommandLine -split '-EncodedCommand ')[1]
$decoded=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded))
@{chain=$chain;decodedLauncher=$decoded}|ConvertTo-Json -Depth 5 -Compress
"""
    result = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", ps], encoding="utf-8"))
    assert 13320 in [x["pid"] for x in result["chain"]]
    assert str(C / "runner.ps1") in result["decodedLauncher"]
    result.update(sessionId=L.name, liveParentPid=13320, lockTouched=False,
                  role="Child inherits live parent protection; no lock acquisition/read/delete/unlock.")
    return result


def start():
    clean(R, HEAD)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    cp = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):",
        1)[1])
    assert cp["checkpoint"] == 808 and cp["batch"] == "105"
    p = load(C / "progress.json")
    assert p["checkpoint"] == 808 and p["status"] == "continue" and p["batch"] == "105"
    assert p["lastPublishedCommit"] == MAIN and p["remainingAdditions"] == 1097
    assert not (L / "progress-before-809.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-809.json")
    preflight = role()
    save(L / "preflight-809.json", preflight)
    p["execution809StartingState"] = {
        "execution": 809, "batch": "105", "startingHead": HEAD,
        "freshOriginMain": MAIN, "androidHead": APP,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME105 bounded runtime draft and signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,106 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete issue and final808 inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": preflight,
        "artifactPathPreflight": "Approved control helpers, committed packets and frozen inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main unchanged.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-105-runtime-draft-in-progress", blocker=None,
             nextAction=p["execution809StartingState"]["scope"])
    save(C / "progress.json", p)
    print("809 scope persisted; clean signed heads and actual parent/session verified.")


def strokes():
    from generate_strokes import convert
    from build_manifest import sha256

    assert sha256(R / "tools" / "generate_strokes.py") == (
        "22677a42589c5a8e21c2f1cf25ada71ad4987684d8309820ea70b1354fe06625")
    svg = (S / "batch-105-kanjivg.svg").read_bytes()
    evidence = load(S / "batch-105-stroke-evidence.json")
    print(json.dumps(evidence, ensure_ascii=False))
    out = R / "strokes" / "勁.json"
    assert not out.exists()
    data = convert("勁", svg.decode("utf-8"))
    assert data["strokeCount"] == 9
    assert all(len(x["points"]) == 16 for x in data["strokes"])
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                   encoding="utf-8")
    print("Generated 9 paths/16 points each using unchanged pinned converter.")


def audit():
    from audit_n1_pilot import metadata as read_metadata
    from build_manifest import build_manifest, sha256 as normalized_sha
    from generate_strokes import convert
    from fontTools.ttLib import TTFont

    assert git("rev-parse", "HEAD") == HEAD
    clean(A, APP)
    role()
    baseline = json.loads(subprocess.check_output(
        ["git", "show", f"{HEAD}:manifest.json"], cwd=R, encoding="utf-8"))
    generated = build_manifest(R)
    current = load(R / "manifest.json")
    assert generated == current
    def metadata(path):
        return read_metadata(path.parent, path.name)

    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, rec in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert sha(raw) == rec["sha256"] and len(raw) == rec["bytes"], name
    assert "勁" in load(C / "inputs" / "n1-kanji-source-20261102.json")
    kd = ET.fromstring(gzip.decompress(
        (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    character = next(x for x in kd.findall("character") if x.findtext("literal") == "勁")
    assert [x.text for x in character.findall(".//reading[@r_type='ja_on']")] == ["ケイ"]
    assert [x.text for x in character.findall(".//reading[@r_type='ja_kun']")] == ["つよ.い"]
    assert character.findtext("radical/rad_value[@rad_type='classical']") == "19"
    assert character.findtext("misc/stroke_count") == "9"
    maps = ["files", "images", "scenes", "curriculum", "listening", "audio",
            "listeningTasks", "listeningTaskAudio", "listeningTaskImages"]
    baseline_count = 0
    additions = {}
    for kind in maps:
        before, after = baseline.get(kind, {}), current.get(kind, {})
        for path, digest in before.items():
            assert after[path] == digest, (kind, path)
            actual = ((R / path).read_bytes() if kind in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else
                (R / path).read_bytes().replace(b"\r\n", b"\n"))
            assert sha(actual) == digest, path
            baseline_count += 1
        additions[kind] = sorted(set(after) - set(before))
    expected = ["kanji/勁.md", "strokes/勁.json", "words/雄勁.md"]
    assert additions["files"] == expected
    assert all(not paths for kind, paths in additions.items() if kind != "files")
    k = metadata(R / "kanji" / "勁.md")
    w = metadata(R / "words" / "雄勁.md")
    assert k["onyomi"] == ["ケイ"] and k["kunyomi"] == ["つよ.い"]
    assert k["quizOnyomi"] == ["ケイ"] and k["quizKunyomi"] == []
    assert k["distractors"] == ["功", "劾", "剖"]
    assert k["quiz_exclusions"] == ["強", "剛", "力", "勢"]
    assert k["radical"] == "力" and k["radicalNumber"] == 19 and k["strokes"] == 9
    assert k["jlpt"] == 1 and k["tags"] == ["jlpt-n1", "grade-9", "structure-unclassified"]
    assert "phonetic" not in k
    assert w["kanji"] == ["雄", "勁"] and w["reading"] == "ゆうけい"
    assert w["quiz_exclusions"] == ["強い", "強力", "力強い", "剛健", "力", "勢い"]
    assert "jlpt" not in w and not (R / "kanji" / "雄.md").exists()
    assert not (R / "words" / "勁い.md").exists()
    kanji_text = (R / "kanji" / "勁.md").read_text(encoding="utf-8")
    word_text = (R / "words" / "雄勁.md").read_text(encoding="utf-8")
    assert "../words/雄勁.md" in kanji_text and "../kanji/勁.md" in word_text
    all_mapped = [p for p in (R / "words").glob("*.md") if "勁" in metadata(p).get("kanji", [])]
    assert [p.stem for p in all_mapped] == ["雄勁"]
    for char in k["distractors"]:
        assert metadata(R / "kanji" / f"{char}.md")["jlpt"] == 1
    d = load(R / "strokes" / "勁.json")
    assert d == convert("勁", (S / "batch-105-kanjivg.svg").read_text(encoding="utf-8"))
    assert d["sourceRevision"] == "70a0b7ae0c18ceb5cb358274b029cce0234a43bc"
    svg = (S / "batch-105-kanjivg.svg").read_bytes()
    assert hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest() == (
        "240719c1247f47703af5264c0f860083c5de233d")
    assert normalized_sha(R / "tools" / "generate_strokes.py") == (
        "22677a42589c5a8e21c2f1cf25ada71ad4987684d8309820ea70b1354fe06625")
    han = sorted({c for c in kanji_text + word_text
                  if 0x3400 <= ord(c) <= 0x9fff or 0xf900 <= ord(c) <= 0xfaff})
    ranges = []
    range_start = None
    radical_checked = False
    for line in (C / "inputs" / "n1-UnicodeData-17.0.0.txt").read_text(
            encoding="utf-8").splitlines():
        fields = line.split(";")
        code = int(fields[0], 16)
        if fields[1].endswith(", First>"):
            range_start = code
        elif fields[1].endswith(", Last>"):
            assert range_start is not None
            ranges.append((range_start, code))
            range_start = None
        else:
            ranges.append((code, code))
        if code == 0x2F00 + 19 - 1:
            assert fields[5] == "<compat> 529B"
            radical_checked = True
    assert radical_checked
    assert all(any(first <= ord(c) <= last for first, last in ranges) for c in han)
    fonts = []
    for path in sorted((A / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path.relative_to(A)), "sha256": sha(path.read_bytes()),
                      "missing": [c for c in han if ord(c) not in cmap]})
    assert len(fonts) == 3
    result = {
        "schemaVersion": 1, "execution": 809, "batch": "105", "sourceBase": HEAD,
        "frozenInputHashesVerified": 5, "exactSourceMembershipAndRawMetadataVerified": True,
        "baselineRuntimeHashesPreserved": baseline_count,
        "runtimeAdditions": additions, "baselineRuntimeEdits": [],
        "contentVersion": current["contentVersion"],
        "allMappedPairs": [["勁", "words/雄勁.md"]],
        "requiredLinkDirectionsVerified": 2, "activatedBaselinePairs": [],
        "fullOnyomi": k["onyomi"], "fullKunyomi": k["kunyomi"],
        "quizOnyomi": k["quizOnyomi"], "quizKunyomi": k["quizKunyomi"],
        "offeredOnKeys": ["けい"], "offeredKunKeys": [],
        "directKanjiGuards": k["quiz_exclusions"], "directWordGuards": w["quiz_exclusions"],
        "guardsSymmetricNotTransitive": True,
        "curatedWrongChoices": k["distractors"],
        "strokePaths": 9, "pointsPerPath": 16, "exactPinnedConverterOutput": True,
        "actualRuntimeHan": han, "hanCount": len(han), "bundledFonts": fonts,
        "allActualHanInFrozenUnicode": True, "canonicalRadicalFromFrozenUnicode": True,
        "absentFromAllBundledCmaps": [c for c in han if all(c in f["missing"] for f in fonts)],
        "missingCmapIsRenderingFailure": False,
        "runtimeHashes": {p: current["files"][p] for p in expected},
        "sourcePlan": "batch-105-source-completion-plan.json",
        "freshAuthorReads": "Complete member XML/character record, exact public 勁/雄勁/雄 blocks, source plan and selected comparison bodies/families. Complete49-body/28-comparison preparation inspection is inherited808 evidence, not claimed as a fresh full reread.",
        "limits": "Mechanical and author draft audits, not independent linguistic review, live quiz safety, Android/native/font/phone acceptance. Two serial blind families and every original downstream acceptance gate remain mandatory.",
    }
    save(S / "batch-105-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def evidence():
    audit_record = load(S / "batch-105-draft-audit.json")
    receipts = {}
    for name in ["validate", "manifest", "focused-tests", "vocabulary", "budget", "audit", "whitespace"]:
        path = L / f"809-{name}.txt"
        raw = path.read_bytes()
        dest = S / f"batch-105-draft-{name}-809.txt.gz"
        dest.write_bytes(gzip.compress(raw, mtime=0))
        receipts[name] = {"archive": dest.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                          "archiveSha256": sha(dest.read_bytes())}
    helpers = [Path(__file__), C / "checks-batch-105-draft-809.ps1",
               C / "post-batch-105-draft-809.ps1"]
    for source in helpers:
        shutil.copyfile(source, S / f"batch-105-{source.name}")
    next_action = (
        "SAME105 two SERIAL blind different-model-family independent initial textual reviews on the SAME "
        "signed LOCAL UNREVIEWED draft; cover kanji/勁.md and words/雄勁.md, all correctness/scoped coverage/"
        "phone comprehensibility facets with serial internal tools and full bounded source access. Persist "
        "complete original reports and actual model/process/read limits before reconciliation. No author "
        "adjudication/other report in initial prompts, no snapshot edits during review; confirm process exit "
        "before second family. Do not publish, start106, run Android/native or create a second runner in that "
        "review checkpoint. Source plan808 and draft audit809 preserve row116/full[ケイ]/[つよ.い], "
        "selected[ケイ]/[] keyけい, search-only勁い, one support雄勁/no inferred vocabularylevel, "
        "four direct kanji/six direct word guards, one reciprocal pair/two directions/zero baseline edits. "
        "All original qualified Androidbf30cdead HOST+finite semantic defaultN1/All/custom and fresh native "
        "ContentSyncONCE/N1/All/meaning/reading/drawing/article/Back/offline/four-font/default rendering "
        "gates remain after textual reconciliation. Actual draft Han/font inventory is in batch-105-draft-audit.json; "
        "cmap absence is NOT glyph failure. Preserve original806/807/808 records and every historical "
        "source/review/process/readdepth/permission/OOM/ANR/routing/phone limit without retroacceptance. "
        "Then combined-current-main/fullPython/vocabulary/baseline-membership-links/manifest/per-file/media/"
        "safe-path/18000entry42MiBcompressed80MiBinflated56MiBretained budgets/normal signing/owner fastforward/"
        "greenCI/every immutableZIP runtimehash/verifiedownerissue. Verify clean signed heads/freshmain/"
        "liveparent13320 ancestry/decodedlauncher/exactsession; child must not touch runner.lock. Approved "
        "control/committed sources/frozen inputs only, no optional historical session recipes. Preserve/report/"
        "yield actual new denial, signing hang or uncertain ownership. Published131/1228,1097remaining unchanged; "
        "support words are NOT N1 vocabulary delivery. Compatible Android#125+#132 required; old clients ignore "
        "curation/guards. Physicalphone/generalrelease/whole-set outstanding; project incomplete.")
    record = {
        "schemaVersion": 1, "execution": 809, "checkpoint": 809, "batch": "105",
        "stage": "batch-105-local-unreviewed-runtime-draft",
        "baseCommit": HEAD, "publishedBase": MAIN, "androidSignedHead": APP,
        "membership": ["勁"], "sourceRows": [116],
        "draftAudit": "batch-105-draft-audit.json", "validation": receipts,
        "runnerPreflight": load(L / "preflight-809.json"),
        "runtimeDrafted": ["勁"], "necessarySupportDrafted": ["雄勁"],
        "reviewClosed": [], "published": [], "runtimeChanged": True, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 131, "remainingAdditions": 1097, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "nextAction": next_action,
        "limits": audit_record["limits"],
        "durableHelperHashes": {
            f"batch-105-{source.name}": sha(source.read_bytes())
            for source in helpers},
        "focusedTestsPassed": 87, "validatorErrors": 0,
        "actualBuilderChecked": False, "nativeDrawingAccepted": False,
        "renderedAcceptance": False,
    }
    save(S / "execution-809.json", record)
    progress = load(S / "batch-105-progress.json")
    progress.update(status="local-unreviewed-runtime-draft", drafted=["勁"], runtimeChanged=True,
                    draftExecution=809, draftAudit="batch-105-draft-audit.json",
                    draftContentVersion=audit_record["contentVersion"], nextAction=next_action,
                    limits="Source-complete author plan followed by a LOCAL UNREVIEWED runtime draft. Original807/808 source records remain historical and unchanged. Draft audit is not independent linguistic review or Android/native/rendered/phone acceptance; every original downstream gate and outstanding general-release/whole-set limit remains.")
    save(S / "batch-105-progress.json", progress)
    print("Draft audit, command receipts, durable recipes and unreviewed state preserved.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != HEAD
    clean(R, head)
    clean(A, APP)
    assert git("rev-parse", "HEAD^") == HEAD
    assert git("rev-parse", "origin/main") == MAIN
    role_receipt = role()
    p = load(C / "progress.json")
    old = load(L / "progress-before-809.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in old.items():
        if key not in allowed:
            assert p[key] == value, key
    record = load(S / "execution-809.json")
    checkpoint = dict(record)
    checkpoint.update(savedCommit=head, signature="G", status="continue",
                      dedicatedWorktreesClean=True, finalRunnerPreflight=role_receipt,
                      originalHistoricalRootValuesPreserved=True,
                      originalRootKeysCompared=len(old))
    issue = load(L / "issue-receipt-809.json")
    assert issue["verified"] and issue["author"] == "stop-cran" and issue["localCommit"] == head
    checkpoint.update(issueUpdate=issue["url"], ownerIssueAuthorAndBodyVerified=True)
    p["batch105DraftIssueReceipt"] = issue
    p["execution809CoordinatorCheckpoint"] = checkpoint
    p.update(checkpoint=809, status="continue", stage=record["stage"],
             nextAction=record["nextAction"], blocker=None)
    save(C / "progress.json", p)
    reloaded = load(C / "progress.json")
    for key, value in old.items():
        if key not in allowed:
            assert reloaded[key] == value, key
    assert reloaded["checkpoint"] == 809 and reloaded["lastPublishedCommit"] == MAIN
    save(L / "checkpoint-809-verification.json", {
        "savedCommit": head, "signature": "G", "originalRootKeysCompared": len(old),
        "allOriginalHistoricalValuesPreserved": True,
        "dedicatedWorktreesClean": True, "published": False, "wholeProjectComplete": False})
    print(f"Checkpoint809 saved and verified: {head}; LOCAL UNREVIEWED, not published.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=["start", "strokes", "audit", "evidence", "finish"])
    globals()[parser.parse_args().operation]()
