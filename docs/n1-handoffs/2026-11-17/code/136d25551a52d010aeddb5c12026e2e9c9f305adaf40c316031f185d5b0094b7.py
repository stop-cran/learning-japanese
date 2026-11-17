"""Admit the original author for the adjudicated bounded B133 teaching revision."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from admit_b133_source_reconciliation import AUTHOR, CANDIDATE, assess_snapshot, collect_initials
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b133_payload import BASE, HERE, REPO, RUNNER
from verify_b133_sources import FINGERPRINT, Git, OWNER

OUT = HERE / "teaching-reconciliation-admission-001"
BRIEF = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b"
             r"\files\b133-teaching-revision-001-brief.txt")
ADJUDICATION = (HERE / "coordinator-adjudication-001.json",
                "cc04c27c12c3fd9fcced0075acfb817f8f0427049c1cfdcc18db146ac1d4f549")
VERIFICATION = (HERE / "source-reconciliation-verification-001.json",
                "d6c01b0501e4c3d23c8ab250a5cd674a32270058e5f7a3252b39bf5d185443fb")


def main(status_path, roster_path):
    require(not OUT.exists() and not (WS / "scratch-133" / "teaching-reconciliation-001").exists(),
            "Preserve existing admission or teaching outputs")
    status_raw, roster_raw = status_path.read_bytes(), roster_path.read_bytes()
    status = json.loads(status_raw)
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    observed = datetime.fromtimestamp(min(status_path.stat().st_mtime, roster_path.stat().st_mtime),
                                      timezone.utc)
    count = assess_snapshot(status, roster, observed, datetime.now(timezone.utc))
    brief = frozen(BRIEF)
    decision_raw = frozen(*ADJUDICATION)
    decision = json.loads(decision_raw)
    require(decision["candidate"] == CANDIDATE and decision["publication"] == "BLOCKED"
            and decision["added"] == 11 and decision["retained"] == 7, "Adjudication differs")
    for path, letters in decision["changeBoundary"]["quizExclusionsAdded"].items():
        for letter in letters:
            require(letter.encode("utf-8") in brief, f"Brief omits {path} {letter}")
    verification_raw = frozen(*VERIFICATION)
    guard, _ = start_guard("B133 bounded teaching revision admission")
    try:
        initials = collect_initials()
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is changed or dirty")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate identity differs")
        guard.check()
        assess_snapshot(status, roster, observed, datetime.now(timezone.utc))
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    snapshots = {"status": write_frozen(OUT / "status.json", status_raw),
                 "roster": write_frozen(OUT / "roster.txt", roster_raw)}
    record = {
        "batch": 133, "candidate": CANDIDATE, "base": BASE, "session": AUTHOR,
        "purpose": "implement-adjudicated-precautions-and-owner-sign-no-push", "admitted": True,
        "observedAt": observed.isoformat(), "createdAt": datetime.now(timezone.utc).isoformat(),
        "sessionCount": count, "snapshots": snapshots, "initials": initials,
        "brief": {"path": str(BRIEF), "sha256": sha(brief)},
        "adjudication": {"path": str(ADJUDICATION[0]), "sha256": sha(decision_raw)},
        "sourceVerification": {"path": str(VERIFICATION[0]), "sha256": sha(verification_raw)},
        "memory": memory,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "Startup observation only, not a reservation. One existing author; bounded signed teaching "
                  "revision. No push, reviewers, confirmation, publication or delivery credit.",
    }
    print(json.dumps(freeze_json(OUT / "admission.json", record)))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: admit_b133_teaching_reconciliation.py STATUS ROSTER")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
