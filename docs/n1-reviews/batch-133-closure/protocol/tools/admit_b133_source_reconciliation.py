"""Admit the original author for a finite source-only reconciliation."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from b133_closure_records import collect_initial_record
from common import COORDINATOR, WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b133_payload import BASE, HERE, REPO, RUNNER
from verify_b133_sources import FINGERPRINT, Git, OWNER

CANDIDATE = "ad047ace020579f81bde250ac948b9a4cb597887"
AUTHOR = "be3530d0-89ae-4a1c-a6f8-6648ba0ae43e"
P = HERE / "neutral-preparation-004" / "successor-002"
OUT = HERE / "source-reconciliation-admission-001"
BRIEF = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b"
             r"\files\b133-source-reconciliation-001-brief.txt")
PREFLIGHT = {"path": str(P / "audit-configs-004" / "preflight.json"),
             "sha256": "cb5ea2edefe2037dae0b00edc26830152e715707fce1cbd40d98b610ac4ebc56"}
INITIALS = {
    "claude": {
        "session": "83ee993b-d768-4da6-94b0-9b5e584fc044", "verdict": "CLEAN",
        "acceptance": "6dc2439acf0e6fe5dacb632b37fc9409e800c51daa81a859d477172838cc81e0",
        "final": "0fba2ca29b8368d0c178197c48a2cf16c657fd72a8e8655a5f2a49a81bba8c25",
        "claims": {"acceptedFindings": [], "openClaimIds": [],
                   "coordinatorClaimIds": ["C1", "C2", "C3"]},
    },
    "gpt": {
        "session": "7b55fcad-b8eb-4917-81fa-8b606cd369de", "verdict": "UNVERIFIED",
        "acceptance": "ae3b82d01ec59dd7631d948ba5cfac32d0b7d7ea6d59f72848abdfb382e81007",
        "final": "33212f853c4389cfd1b1b1c71e5db909431fe5be45fe76f321f4ea1a2c610e7b",
        "claims": {"acceptedFindings": [], "openClaimIds": ["Q1", "Q2", "Q3", "Q4"],
                   "coordinatorClaimIds": ["C4", "C5", "C6"]},
    },
}


def assess_snapshot(status, roster, observed, now):
    rows = status["sessions"]
    ids, roster_ids = [row["id"] for row in rows], [row["id"] for row in roster]
    require(status["summary"]["total"] == len(rows) == len(roster)
            and len(set(ids)) == len(ids) and len(set(roster_ids)) == len(roster_ids)
            and set(ids) == set(roster_ids) and {COORDINATOR, AUTHOR} <= set(ids),
            "Incomplete, duplicate or mismatched app snapshots")
    require(observed.tzinfo is not None and now.tzinfo is not None
            and 0 <= (now - observed).total_seconds() < 120, "Stale or future observation")
    for row in rows:
        if row["id"] != COORDINATOR:
            require(row.get("activity", {}).get("status") == "idle"
                    and row.get("is_running") is False
                    and not row.get("awaiting_user_input") and not row.get("awaiting_plan_approval"),
                    f"Session is not idle and unblocked: {row['id']}")
    return len(rows)


def collect_initials():
    result = {}
    for family, expected in INITIALS.items():
        run = "N1-B133-" + family.upper() + "-001"
        acceptance = {"path": str(P / f"{run}-acceptance.json"), "sha256": expected["acceptance"]}
        final = {"path": str(P / f"{run}-final.json"), "sha256": expected["final"]}
        spec = {"family": family, "run": run, "role": "initial", "snapshot": CANDIDATE,
                "session": expected["session"], "verdict": expected["verdict"], "acceptance": acceptance}
        refs, _, claims = collect_initial_record(spec, PREFLIGHT, final, frozen)
        require(claims == expected["claims"], "Initial consequential claims differ")
        result[family] = {"run": run, "session": expected["session"], "verdict": expected["verdict"],
                          "acceptance": acceptance, "final": final,
                          "adjudication": refs["adjudication"], **claims}
    return result


def main(status_path, roster_path):
    require(not OUT.exists() and not (WS / "scratch-133" / "source-reconciliation-001").exists(),
            "Preserve existing admission or source outputs")
    status_raw, roster_raw = status_path.read_bytes(), roster_path.read_bytes()
    status = json.loads(status_raw)
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    observed = datetime.fromtimestamp(min(status_path.stat().st_mtime, roster_path.stat().st_mtime),
                                      timezone.utc)
    count = assess_snapshot(status, roster, observed, datetime.now(timezone.utc))
    brief = frozen(BRIEF)
    guard, _ = start_guard("B133 source-only reconciliation admission")
    try:
        initials = collect_initials()
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is changed or dirty")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate identity differs")
        require(b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
                in git("show", "-s", "--format=%B", CANDIDATE), "Required trailer missing")
        guard.check()
        assess_snapshot(status, roster, observed, datetime.now(timezone.utc))
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    snapshots = {"status": write_frozen(OUT / "status.json", status_raw),
                 "roster": write_frozen(OUT / "roster.txt", roster_raw)}
    record = {
        "batch": 133, "candidate": CANDIDATE, "base": BASE, "session": AUTHOR,
        "purpose": "source-reconciliation-only", "admitted": True,
        "observedAt": observed.isoformat(), "createdAt": datetime.now(timezone.utc).isoformat(),
        "sessionCount": count, "snapshots": snapshots, "initials": initials,
        "brief": {"path": str(BRIEF), "sha256": sha(brief)}, "memory": memory,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "Startup observation only, not a reservation. One existing author; source-only "
                  "follow-up. No teaching edits, reviewers, commits, publication or delivery credit.",
    }
    print(json.dumps(freeze_json(OUT / "admission.json", record)))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: admit_b133_source_reconciliation.py STATUS ROSTER")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
