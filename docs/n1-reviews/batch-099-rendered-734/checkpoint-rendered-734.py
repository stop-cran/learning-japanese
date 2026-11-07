import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "4e0734f9-7880-47af-a669-55d01f8a0b08"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
HEAD = "a580bb1c79174b57842e2ba5df32c4ff562239a3"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
FOLDER = V / "batch-099-rendered-734"
STAGE = "batch-099-blocked-verified-kanji-fallback-ambiguity"
BLOCKER = (
    "N099-FALLBACK-JOU verified: production randomN1Subset seeds4/7 offer "
    "superfluous; redundant (冗) as a wrong answer for剰 remainder; surplus amount. "
    "Frozen dictionaries support overlapping meanings; both original reviewer families confirm. "
    "No supported kanji semantic exclusion exists in the current client. An app/parser/builder "
    "mechanism is outside issue60 authorization; narrow prerequisite authorization is required. "
    "Also retain unresolved Claude per-tool serialization deviation; its report falsely says reads "
    "were serial, while9tool overlap-start events occurred. No runtime publication or100."
)
NEXT = (
    "SAME099 is blocked, not accepted/published. Read docs/n1-sources/execution-734.json and "
    "docs/n1-reviews/batch-099-rendered-734-reconciliation.json. Establish explicit owner authorization "
    "for a narrow compatible-client kanji semantic-pair guard prerequisite before any app change; "
    "do not distort titles, invent semantic compartments, add ignored fields, alter membership/levels, "
    "or pretend curated availability covers arbitrary filtered pools. Reproduce exact observed "
    "randomN1Subset seeds4/7 剰-vs冗 from native733 in prerequisite regressions, cover both relevant "
    "target orientations/import/projections/supported pool filtering, retain actual dictionaries "
    "and original reports. Determine narrow evidence-based content declarations only after an approved "
    "mechanism exists. Both original-session follow-ups executed one process at a time: "
    "Claude2ac79fdb opus5.5 then GPT240faa46 gpt6.1sol,13calls each/full13families+2characters/12images. "
    "Claude9overlapstart events contradict its serial-read claim; preserve raw reports and audit. "
    "GPT tools fully serial. Overall renderedreview NOTclosed; obtain only necessary compliant "
    "Claude bounded confirmation after resolving toolserialization, no repeated-read loop/newblindcredit. "
    "Textual article verdicts remain CLEAN; fallbacksemantic NEEDSFIX. Native733 TWOterminalcase0/"
    "no skips and fresh731JVM4noskips remain historical passed bounded evidence, not phone/fullacceptance. "
    "No freshnative/JVM rerun needed merely to repeat unchanged work; revalidate actual changed "
    "prerequisite/content/integrated tree when justified. All12Han/fourfonts have bounded legible panels "
    "but actualfallbackface unknown;2fontpanels+10contactsheets is NOT39fullresolutionroute reads. "
    "Preserve rawreadingsジョウ/あまつさえ/あま.り/あま.る; quizジョウ/[]; elevenpinnedstrokes, "
    "two reciprocalpairs/fourdirections/oneactivatedbaselinepair; reused過剰N2/sevenwordguards unchanged. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. No app/runtime edit "
    "or push in734. Parent15692 owns runner.lock throughout child lifetime: verifyliveancestry/session/"
    "exactsignedheads/whollyclean, NOchildacquire/delete/unlock/readprobe. Approvedcontrol/committed "
    "sources/frozeninputs only, no optionalhistoricalsessionhelper. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. All original source/review/process/denial/OOM/history and "
    "latestmainnonrewritingmerge/changedteachingreview/combinedchecks/normalsigning/ownerfastforward/"
    "terminalgreenCI/EVERYimmutableZIPmanifesthash/18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue gates remain. Published125/1228,1103remaining unchanged. "
    "Physicalphone/generalrelease/whole-set outstanding. No100/unreviewedpush/secondrunner."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "-C", str(root), "--no-pager", *args],
                                   encoding="utf-8").strip()


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    before_manifest = json.loads(subprocess.check_output(
        ["git", "-C", str(R), "show", HEAD + ":manifest.json"], encoding="utf-8"))
    current = load(R / "manifest.json")
    assert build_manifest(R) == current == before_manifest
    count = 0
    for section, entries in current.items():
        if not isinstance(entries, dict):
            continue
        for path, digest in entries.items():
            actual = sha(R / path) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"
            } else sha256(R / path)
            assert actual == digest, path
            count += 1
    assert count == 8451 and current["contentVersion"] == "5408632b5aa1382c"
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {"verifiedRuntimeHashes": count, "contentVersion": current["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "manifestFreshAndUnchanged": True}


def capture():
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    assert load(C / "progress.json")["checkpoint"] == 733
    assert not FOLDER.exists()
    FOLDER.mkdir()
    records = []
    for label in ["claude", "gpt"]:
        prefix = f"batch-099-rendered-734-{label}"
        record = load(C / (prefix + "-execution.json"))
        assert record["exitCode"] == 0 and not record["unfinishedTools"]
        assert any(c.get("exactCompletePacketReturned") for c in record["toolCalls"])
        images = [c for c in record["toolCalls"] if c["arguments"].get("path", "").endswith(".png")]
        assert len(images) == 12 and all(c["success"] for c in images)
        records.append(record)
        for suffix in [".md", "-execution.json", "-stderr.txt", "-usage.json"]:
            shutil.copyfile(C / (prefix + suffix), FOLDER / (prefix + suffix))
        raw = (C / (prefix + ".jsonl")).read_bytes()
        packed = FOLDER / (prefix + ".jsonl.gz")
        packed.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
    assert records[0]["completedAt"] < records[1]["startedAt"]
    assert len(records[0]["observedToolOverlaps"]) == 9
    assert not records[1]["observedToolOverlaps"]
    for record in records:
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if (Get-Process -Id {record['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                       check=True)
    for name in [
        "batch-099-rendered-734-packet.txt", "batch-099-rendered-734-prompt.txt",
        "batch-099-rendered-734-required.json", "review-batch-099-rendered-734.py",
        "preflight-734.ps1", Path(__file__).name,
    ]:
        shutil.copyfile(C / name, FOLDER / name)
    for name in ["preflight-734.json", "copilot-help-734.txt", "copilot-config-734.txt"]:
        shutil.copyfile(L / name, FOLDER / name)
    builder = A / "core" / "src" / "main" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "quiz" / "QuizBuilder.kt"
    shutil.copyfile(builder, FOLDER / "QuizBuilder.kt.txt")
    checked = runtime()
    evidence = {
        "schemaVersion": 1, "execution": 734, "batch": "099", "status": STAGE,
        "startingState": load(C / "progress.json")["execution734StartingState"],
        "snapshot": HEAD, "teachingSnapshot": "70dfe3344d167e5152a3685b09689d73fa1cdab1",
        "androidHead": APP, "runtime": checked,
        "reconciliation": "docs/n1-reviews/batch-099-rendered-734-reconciliation.json",
        "artifacts": FOLDER.relative_to(R).as_posix(),
        "reviewers": [{k: v for k, v in record.items()
                       if k in {"sessionId", "requestedModel", "actualModels", "usageCurrentModel",
                                "launcherPid", "startedAt", "completedAt", "exitCode",
                                "observedToolOverlaps", "unfinishedTools", "reportSha256", "rawSha256"}}
                      for record in records],
        "reviewerProcessesSerialAndExited": True,
        "twoFamilyToolSerializationCompliant": False,
        "independentRenderedReviewClosed": False,
        "textualTeachingReviewClosed": True,
        "fallbackSemanticVerdict": "NEEDS FIX",
        "finding": "N099-FALLBACK-JOU",
        "blocker": BLOCKER, "nextAction": NEXT,
        "sourcePacket": {"completeFamilies": 13, "completeCharacterRecords": 2,
                         "independentUpstreamRetrieval": False},
        "diagnostics": [
            "Initial console summary encoding failed after entire request was loaded and checkpoint parsed; no state change.",
            "Preparation stopped before any reviewer because1543910 is in the comparison packet, not primary packet. Corrected exact source location; original progress-before snapshot retained, starting record not overwritten.",
            "Claude claims serial tool reads, but actual tool timestamps show9overlap-start events. Original complete report preserved unchanged and not accepted as protocol-compliant."
        ],
        "builder": {"path": "core/src/main/kotlin/io/github/stopcran/kanji/core/quiz/QuizBuilder.kt",
                    "sha256": sha(builder), "lines": len(builder.read_text(encoding="utf-8").splitlines()),
                    "qualifiedTestOnlyHead": APP, "appChanged": False},
        "nativeOrJvmRerun": False, "runtimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "reviewClosed": [], "published": [],
        "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": "d5a376ee2b014aae3c47c58eea47b327e44be6d2",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
    }
    save(S / "execution-734.json", evidence)
    path = S / "batch-099-progress.json"
    batch = load(path)
    batch["status"] = STAGE
    batch["renderedReconciliation734"] = {
        "evidence": "docs/n1-sources/execution-734.json", "status": "blocked",
        "fallbackSemanticVerdict": "NEEDS FIX", "finding": "N099-FALLBACK-JOU",
        "independentRenderedReviewClosed": False, "twoFamilyToolSerializationCompliant": False,
        "runtimeAccepted": False, "runtimePublished": False,
        "blocker": BLOCKER, "nextAction": NEXT,
    }
    batch["limits"].append(
        "734 source-backed observed剰/冗 fallback ambiguity verified by both original families; "
        "separate narrowly authorized app prerequisite required. Both processes exited serially, "
        "but Claude tools overlapped despite report claiming serial reads; overall rendered gate NOTclosed. "
        "No runtime change, publication or100.")
    assert batch["reviewClosed"] == batch["published"] == []
    save(path, batch)
    index = [{"path": path.relative_to(FOLDER).as_posix(), "sha256": sha(path),
              "bytes": path.stat().st_size} for path in sorted(FOLDER.rglob("*")) if path.is_file()]
    save(FOLDER / "artifact-index.json", index)
    print(json.dumps({"capturedArtifacts": len(index), "runtime": checked}))


def seal():
    p = load(C / "progress.json")
    original = load(L / "progress-before-734.json")
    assert p["checkpoint"] == 733 and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    issue = load(L / "issue-734-reread.json")
    expected = (C / "batch-099-rendered-734-issue-body.txt").read_bytes().decode("utf-8-sig")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == expected
    record = {
        "schemaVersion": 1, "execution": 734, "checkpoint": 734, "batch": "099",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G",
        "status": "blocked", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-734.json",
        "reconciliation": "docs/n1-reviews/batch-099-rendered-734-reconciliation.json",
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "dedicatedWorktreesClean": True, "runtime": runtime(),
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "textualTeachingReviewClosed": True, "independentRenderedReviewClosed": False,
        "fallbackSemanticVerdict": "NEEDS FIX", "finding": "N099-FALLBACK-JOU",
        "bothOriginalSessionProcessesExitedSerially": True,
        "claudeToolOverlapStartEvents": 9, "gptToolOverlapStartEvents": 0,
        "twoFamilyToolSerializationCompliant": False,
        "reviewClosed": [], "published": [], "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": "d5a376ee2b014aae3c47c58eea47b327e44be6d2",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "blocker": BLOCKER, "nextAction": NEXT,
    }
    p.update(checkpoint=734, status="blocked", stage=STAGE, blocker=BLOCKER, nextAction=NEXT)
    p["execution734CoordinatorCheckpoint"] = record
    p["batch099RenderedReconciliationCheckpoint"] = record.copy()
    allowed = {"checkpoint", "status", "stage", "blocker", "nextAction"}
    for key, value in original.items():
        if key not in allowed:
            assert p[key] == value, key
    record["originalRootKeysCompared"] = len(original)
    record["allOriginalHistoricalRootValuesPreservedExactly"] = True
    p["batch099RenderedReconciliationCheckpoint"] = record.copy()
    temporary = C / "progress.734.tmp"
    assert not temporary.exists()
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")
    save(L / "checkpoint-734.json", record)
    print(json.dumps(record, ensure_ascii=True, indent=2))


def pack_text():
    archives = []
    for name in ["batch-099-rendered-734-packet.txt", "copilot-config-734.txt"]:
        path = FOLDER / name
        data = path.read_bytes()
        packed = FOLDER / (name + ".gz")
        assert not packed.exists()
        packed.write_bytes(gzip.compress(data, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == data
        archives.append({"archive": packed.relative_to(R).as_posix(),
                         "sha256": sha(packed),
                         "sourceSha256": hashlib.sha256(data).hexdigest(),
                         "losslessGzipVerified": True})
        path.unlink()
    for name in ["validate-734.txt", "manifest-734.txt"]:
        shutil.copyfile(L / name, FOLDER / name)
    shutil.copyfile(Path(__file__), FOLDER / Path(__file__).name)
    path = S / "execution-734.json"
    evidence = load(path)
    evidence["losslessOriginalTextArchives"] = archives
    evidence["diagnostics"].append(
        "Staged whitespace check flagged verbatim unified-diff blank context lines in the packet "
        "and original model-catalog EOF spacing. Preserved both unchanged as verified lossless gzip; "
        "original control inputs remain intact. No reviewer report rewritten.")
    save(path, evidence)
    index = FOLDER / "artifact-index.json"
    save(index, [{"path": path.relative_to(FOLDER).as_posix(), "sha256": sha(path),
                  "bytes": path.stat().st_size} for path in sorted(FOLDER.rglob("*"))
                 if path.is_file() and path != index])
    print(json.dumps({"losslessTextArchives": archives}, indent=2))


if __name__ == "__main__":
    {"capture": capture, "seal": seal, "pack-text": pack_text}[sys.argv[1]]()
