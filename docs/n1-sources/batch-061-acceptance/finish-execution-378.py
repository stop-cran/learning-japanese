import copy
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
S = R / "docs" / "n1-sources"
D = S / "batch-061-acceptance"
TEACHING = "2567f5e7b3888f2df3ed560f618341266b471902"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution378.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree,
                                   text=True, encoding="utf-8").strip()


def prepare():
    publication = load(S / "batch-061-publication.json")
    assert publication["ci"]["conclusion"] == "success"
    accepted = publication["acceptedCommit"]
    assert accepted == git("rev-parse", "HEAD")
    for path in (
        C / "artifacts" / "batch-061-accepted-ci.json",
        C / "artifacts" / f"content-{accepted[:7]}-acceptance.json",
        Path(__file__),
    ):
        assert not (D / path.name).exists()
        shutil.copyfile(path, D / path.name)
    receipts = []
    for name, arguments in (
        ("validate", ["tools\\validate.py"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ):
        path = D / f"execution-378-terminal-{name}.txt"
        assert not path.exists()
        with path.open("wb") as stream:
            process = subprocess.run([sys.executable, "-X", "utf8", "-B", *arguments],
                                     cwd=R, stdout=stream, stderr=subprocess.STDOUT)
        receipts.append({
            "command": ["python", "-X", "utf8", "-B", *arguments],
            "exitCode": process.returncode, "log": path.relative_to(R).as_posix(), "sha256": sha(path),
        })
        assert process.returncode == 0, path
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not (S / "batch-061-terminal-validation.json").exists()
    save(S / "batch-061-terminal-validation.json", receipts)
    print("Terminal validator, manifest freshness and original archive budgets passed; runtime unchanged.")


def comment():
    p = load(C / "progress.json")
    head = git("rev-parse", "HEAD")
    publication = load(S / "batch-061-publication.json")
    ci = load(C / "artifacts" / "batch-061-terminal-ci.json")
    archive = load(C / "artifacts" / f"content-{head[:7]}-acceptance.json")
    assert ci["headSha"] == head and ci["conclusion"] == "success"
    assert archive["commit"] == head and archive["verifiedRuntimeHashes"] == 8311
    assert p["batch"] == "061" and p["checkpoint"] == 377
    text = f"""Batch **061 (俳)** is published and verified for bounded owner testing.

- Authored/reviewed teaching: `{TEACHING}`; textual closure: `{publication['textualClosureSnapshot']}`; visual closure: `{publication['visualClosureSnapshot']}`.
- Latest main `{publication['latestMainIntegrated']}` was already ancestral after a fresh fetch/normal merge. Normally signed accepted/integrated publication `{publication['acceptedCommit']}`; terminal evidence/remote main `{head}`. Both normal owner-scoped fast-forward pushes; global GitHub identity unchanged.
- Fresh combined-tree checks: **368 Python tests**, validator, vocabulary consistency (existing pilot coverage 2122/2431, not repaired or claimed complete), manifest freshness, frozen-source/45-family mechanical re-extraction, baseline metadata/readings/levels/exclusions/strokes, exact membership, one reading disposition, **three reciprocal pairs/six links**, two activated baseline pairs, generated ten-stroke geometry and actual font cmaps. Accepted fresh Android **3 RealContentTest + 1 RareHanTest**, no skips, and **two native terminal-0 cases** independently reverified without reruns; single full production ContentSync import 1073 kanji/5031 words/93 N1 labels, zero problems, parser epoch 1.
- Meaning, sole curated ハイ/no-kun, three pairs/six native transitions, System Back/offline, reference-touch drawing/recall-miss/persisted Draw Again retained. Both original model families' dependent visual confirmations retained; no actionable teaching finding. Historical Claude **061-P1/P2/P3** process violations remain explicit: supervised lexical/single-image remediation is prospective, **not retroactive strict acceptance**. Unseen article pixels and unknown fallback face remain limits; emulator evidence is not physical-phone, MLKit or successful human recall evidence.
- Accepted CI [{publication['ci']['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{publication['ci']['databaseId']}) and terminal CI [{ci['databaseId']}](https://github.com/stop-cran/learning-japanese/actions/runs/{ci['databaseId']}) are green. Both immutable GitHub ZIPs preserve **all 8,311 runtime hashes** and manifest `d01d660cc41262fe`; terminal ZIP **{archive['zipEntries']:,} entries / {archive['compressedBytes']:,} compressed / {archive['inflatedBytes']:,} inflated / {archive['retainedBytes']:,} retained bytes**, within unchanged 18,000-entry/42-MiB/80-MiB/56-MiB guards. Contributor evidence excluded from runtime ZIPs.

Published **88/1,228 additions; 1,140 remain**. Current collection: **1,073 kanji, 5,031 words, 93 N1-labelled cards, 92 named-source members plus the separate 妖 exception**. This batch adds no support words; 89 necessary support-word additions project-wide, not an N1 vocabulary deck. Three reused articles receive only reviewed links.

Compatible **stop-cran/kanji-cards-android#125 (`f9b59a2`+)** is required; old clients ignore curation. Physical-phone/general-release and whole-set acceptance remain **outstanding**. Original373 permission denial/parent exact recovery and qualified host-only heap history are preserved. Durable evidence: `docs/n1-sources/batch-061-publication.json`, `batch-061-acceptance-audit.json`, `execution-378.json`, original source/review/native records. Checkpoint378 will persist status `continue` and yield before062; no062/second runner started.
"""
    target = C / "batch-061-publication-comment.txt"
    assert not target.exists()
    target.write_text(text, encoding="utf-8")
    print("Prepared exact terminal publication issue receipt.")


def verify():
    initial = load(C / "execution-378-starting-progress.json")
    p = load(C / "progress.json")
    head = git("rev-parse", "HEAD")
    assert p["checkpoint"] == 378 and p["status"] == "continue" and p["blocker"] is None
    assert p["batch"] == "061" and p["stage"] == "batch-061-published-verified-before-062"
    assert p["lastPublishedCommit"] == head and p["remainingAdditions"] == 1140
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("ls-remote", "origin", "refs/heads/main").split()[0] == head
    app = C.parent / "kanji-cards-android"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", tree=app)
    assert git("rev-parse", "HEAD", tree=app) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    allowed = {"activeExecution", "stage", "nextAction", "checkpoint", "status",
               "lastPublishedCommit", "remainingAdditions", "blocker", "unmetAcceptanceGates"}
    assert initial.keys() <= p.keys()
    assert all(p[key] == value for key, value in initial.items() if key not in allowed)
    assert not (S / "batch-062-progress.json").exists()
    publication = p["batch061PublicationCheckpoint"]
    assert publication["finalPublishedCommit"] == publication["remoteMainVerified"] == head
    assert not publication["strictInitialProcessContractAccepted"]
    assert not publication["strictFirstVisualProcessContractAccepted"]
    assert not publication["strictHistoricalProcessContractAccepted"]
    assert publication["strictDependentProcessContractAccepted"]
    assert publication["prospectiveSupervisedVisualRemediationAccepted"] and not publication["nextBatchStarted"]
    for phase, commit in (("accepted", publication["acceptedCommit"]), ("terminal", head)):
        ci = load(C / "artifacts" / f"batch-061-{phase}-ci.json")
        archive = load(C / "artifacts" / f"content-{commit[:7]}-acceptance.json")
        assert ci["headSha"] == commit and ci["status"] == "completed" and ci["conclusion"] == "success"
        assert ci["jobs"] and all(job["conclusion"] == "success" for job in ci["jobs"])
        assert archive["commit"] == commit and archive["contentVersion"] == "d01d660cc41262fe"
        assert archive["verifiedRuntimeHashes"] == 8311 and archive["manifestEqual"]
        assert archive["allPublishingBudgetsPassed"] and archive["contributorEvidenceExcluded"]
        assert archive["perFileLimitsAndSafePathsPassed"]
        assert sha(C / "artifacts" / f"content-{commit[:7]}.zip") == archive["sha256"]
    for row in load(S / "batch-061-terminal-validation.json"):
        assert row["exitCode"] == 0 and sha(R / row["log"]) == row["sha256"]
    ledger = load(S / "batch-061-progress.json")
    assert ledger["published"] == ledger["reviewClosed"] == ledger["membership"] == ["俳"]
    assert ledger["publishedAdditions"] == 88 and ledger["remainingAdditions"] == 1140
    receipt = load(C / "batch-061-publication-issue-receipt.json")
    remote = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/stop-cran/learning-japanese/issues/comments/{receipt['id']}"],
        text=True, encoding="utf-8"))
    body = (C / "batch-061-publication-comment.txt").read_text(encoding="utf-8-sig")
    assert remote["user"]["login"] == "stop-cran"
    assert remote["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
    assert head in body and publication["issueUpdate"] == remote["html_url"]
    assert subprocess.check_output(["gh", "api", "user", "--jq", ".login"], text=True).strip() == "romanko-ms"
    record = {
        "schemaVersion": 1, "execution": 378, "checkpoint": 378, "batch": "061",
        "savedCommit": head, "signature": "G", "remoteMainVerified": head,
        "dedicatedWorktreesClean": True, "reviewedTeachingAndRuntimeUnchanged": True,
        "freshPythonTestsPassed": 368, "acceptedAndroidCasesReverified": 4,
        "acceptedNativeTerminalCasesReverified": 2, "nativeArtifactsReverified": 53,
        "acceptedCi": publication["ci"]["databaseId"], "terminalCi": publication["terminalCi"]["databaseId"],
        "bothImmutablePublicArchivesVerified": True, "runtimeHashesPerArchive": 8311,
        "originalArchiveGuardsUnchanged": True, "allOriginalHistoricalKeysPreservedExactly": True,
        "oldTopLevelKeys": len(initial), "currentTopLevelKeys": len(p),
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "globalIdentityUnchanged": True, "publishedAdditions": 88, "remainingAdditions": 1140,
        "strictInitialProcessContractAccepted": False, "strictFirstVisualProcessContractAccepted": False,
        "strictHistoricalProcessContractAccepted": False, "strictDependentProcessContractAccepted": True,
        "prospectiveSupervisedVisualRemediationAccepted": True,
        "phoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "verifiedAt": datetime.now().astimezone().isoformat(),
    }
    assert not (C / "execution-378-final-verification.json").exists()
    save(C / "execution-378-final-verification.json", record)
    for key in ("activeExecution", "execution378CoordinatorCheckpoint", "batch061PublicationCheckpoint"):
        p[key]["verification"] = copy.deepcopy(record)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "comment": comment, "verify": verify}[sys.argv[1]]()
