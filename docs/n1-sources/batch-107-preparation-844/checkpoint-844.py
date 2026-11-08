"""Persist the bounded batch107 draft checkpoint without touching runner.lock."""
import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "rollout-recovered" / "learning-japanese"
L = C / "logs" / "70ed1fca-b2a0-4267-bff3-7b7e4362d9ea"
START = "dfed2c150d7fe921aacdb1d616ff527df1935f3b"
BASE = "476f429108415d00f9d41863af9d2f9470b5bbc0"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), *args], encoding="utf-8"
    ).strip()


def save(path, value):
    temporary = path.with_name(path.name + ".844.tmp")
    with temporary.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=True, indent=2) + "\n")
    assert load(temporary) == value
    temporary.replace(path)


def current():
    runner = load(C / "runner.json")
    assert runner["status"] == "running" and runner["pid"] == 31724 and runner["sessionId"] == L.name
    progress = load(C / "progress.json")
    assert progress["checkpoint"] == 843 and progress["status"] == "continue" and progress["batch"] == "107"
    assert progress["lastPublishedCommit"] == BASE and progress["remainingAdditions"] == 1095
    assert progress["execution792HistoryCorrection"]["ownerReportCorrection"].startswith("https://github.com/")
    return progress


def start():
    p = current()
    assert load(L / "checkpoint-full.json") == p
    assert git("rev-parse", "HEAD") == START and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    before = L / "progress-before-844.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    request = L / "request.txt"
    projected = json.loads(request.read_text(encoding="utf-8-sig").split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert projected["checkpoint"] == 843 and projected["execution843CoordinatorCheckpoint"]["savedCommit"] == START
    state = {
        "execution": 844, "batch": "107", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": START, "baseCommit": BASE,
        "scope": "Local unreviewed runtime draft and exact-current mechanical audit only; no reviewer, HOST/native, publication or108.",
        "request": {"sha256": sha(request), "bytes": request.stat().st_size,
                    "completeRequestAndFinalCheckpointRead": True,
                    "limits": "Full request read in ranges and final long checkpoint in disjoint character ranges; historical records not newly linguistically reviewed."},
        "runnerPreflight": load(L / "preflight-844.json"),
        "fullHistoryBefore": str(before), "fullHistoryBeforeSha256": sha(before),
        "artifactPathPreflight": "Committed sources/approved frozen inputs only; new reusable helpers in control.",
        "parentLockTouched": False, "actualNewPermissionDenials": [],
    }
    p["execution844StartingState"] = state
    p.update(stage="batch-107-local-unreviewed-draft-in-progress", nextAction=state["scope"])
    save(C / "progress.json", p)
    print("Full-history starting scope saved.")


def finish():
    p = current()
    head = git("rev-parse", "HEAD")
    assert head != START and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    record = R / "docs" / "n1-sources" / "execution-844.json"
    issue = load(L / "issue-receipt-844.json")
    assert issue["user"]["login"] == "stop-cran" and issue["html_url"].startswith("https://github.com/")
    audit = load(R / "docs" / "n1-sources" / "batch-107-runtime-audit.json")
    next_action = (
        "SAME107 signed LOCAL UNREVIEWED draft next needs TWO SERIAL blind isolated headless CLI "
        "DIFFERENT actual model-family initial reviews on the SAME frozen complete snapshot "
        + head + ". Read execution-844.json and batch-107-runtime-draft.json/audit; "
        "all six complete affected cards (new 勘; reused 勘/勘定/勘違い/定/違), "
        "134 complete frozen families,18 character records,exact public wrapper,comparisons/legacy and source qualifications. "
        "No new support words; all5pairs10directions/3activatedbaselinepairs/5exactreusededits; "
        "定/違 bullets are teaching, not navigation-only. Fullカン/[] and quizカン/[]; "
        "supplementary勘えるかんがえる rareSPELLING ofusual考える, not rarepronunciation or metadataextension. "
        "Curated勤/助/期; direct nontransitive感/思/考/判/査/比/算/察; seven originalwordpairs unchanged. "
        "Dedicated equivalent exact-current mechanical audit passed; generic incompatible sourceplan schema "
        "is NOT claimed executed or waived. Preserve audited fullsource/membership/allbaseline/runtimehashes/"
        "allpairs/readings/guard/pinnedgeometry/manifest invariants. Production defaultN1/All/custom/reduced options, "
        "11legacyfallbacktargets/eightguardorientations/wordbothdirections/otheractualdefensiblelabels remain pending; "
        "no all-pool guarantee. FINAL Han/font targets in runtimeaudit require ALLfouractualmodes "
        "defaultsystem/brush/mincho/textbook; four baseline cmaps missing宀/辵/辶/韋 are inspectiontargets NOT glyphfailures. "
        "Serial reviewer processes AND internaltools, no shell/edit/delegation/authoragents/broadapprovals; "
        "actualmodels/process-exit/readranges/complete originalreports/evidenceadjudication/originalsessionfixconfirmations "
        "required. Qualified signed whollyclean bf30cde Android no-skipsHOST/nativeContentSyncONCE/meaning/curatedreading/"
        "drawing/articles/Back/offline/fonts/rendered; full Python/vocabulary/validator/freshmanifest/budget/"
        "exactcurrentaudits; latestmainnonrewritingintegration/changedteachingreview/actualcombinedvalidation/"
        "normalsignature/ownerfastforward/exactterminalgreenCI/EVERYimmutableZIPruntimehash/"
        "18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemedia-safepath/verifiedownerissue "
        "remain mandatory BEFOREcounting107or108. Published133/1228remaining1095unchanged. "
        "Preserve full live history/792correction/report/106acceptance/nonblocking勅訓いましめるlimits/"
        "alloriginaldenials/OOMs/viewport/process/finitepool/phonequalifications. Approved recoveredsiblings/control/"
        "committedsources/frozeninputs only; optional historicalsessionrecipes not dependencies. "
        "Authenticate live exact-File launcher/session/ancestry/checkpoint/signedcleanaccountedheads/freshmain; "
        "parentownsrunner.lock NOchildacquire/delete/unlock/readprobe. Preserve/report/yield actualnewdenial/"
        "signinghang/uncertainownership; no signingretry/bypass/algorithmchange/concurrentheavywork/secondrunner. "
        "CompatibleAndroid125/132required; physicalphone/generalrelease/whole-setoutstanding; projectincomplete."
    )
    checkpoint = {
        "execution": 844, "checkpoint": 844, "batch": "107", "status": "continue",
        "stage": "batch-107-local-draft-signed-awaiting-independent-initial-reviews",
        "savedCommit": head, "signature": "G", "record": "docs/n1-sources/execution-844.json",
        "recordSha256": sha(record), "runtimeAudit": audit,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "runtimePublished": False, "reviewersLaunched": 0, "freshAndroidOrNative": False,
        "publishedAdditions": 133, "remainingAdditions": 1095,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "nextAction": next_action, "recordedAt": datetime.now(timezone.utc).isoformat(),
    }
    before = load(L / "progress-before-844.json")
    for key, value in before.items():
        if key not in {"stage", "nextAction", "checkpointHistory", "checkpoint", "status", "blocker"}:
            assert p[key] == value, key
    p["execution844StartingState"]["status"] = "signed-local-unreviewed-runtime-draft-complete"
    p["execution844CoordinatorCheckpoint"] = checkpoint
    p.update(checkpoint=844, stage=checkpoint["stage"], status="continue", nextAction=next_action, blocker=None)
    p["checkpointHistory"] = {
        "completeSnapshot": str(L / "checkpoint-after-844.json"), "liveProgressPath": str(C / "progress.json"),
        "invariant": "Full live history preserved; immutable checkpoint is observer input.",
    }
    save(C / "progress.json", p)
    save(L / "checkpoint-after-844.json", p)
    print(json.dumps(checkpoint, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["start", "finish"])
    args = parser.parse_args()
    {"start": start, "finish": finish}[args.mode]()
