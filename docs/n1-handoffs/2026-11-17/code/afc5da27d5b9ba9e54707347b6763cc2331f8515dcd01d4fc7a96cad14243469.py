"""Admit one preparation worker using complete fresh app snapshots and actual candidate proofs."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from common import COORDINATOR, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b133_payload import BASE, HERE, REPO, RUNNER
from verify_b133_sources import FINGERPRINT, Git, OWNER

CANDIDATE = "ad047ace020579f81bde250ac948b9a4cb597887"
PROOFS = {
    "source-verification-001.json": "5d8c9aee7a31a35e5eeae047d35ff3a79aedb4ecc81cb7f72358d9515974cd12",
    "payload-verification-001.json": "692ecc9d3af90157b97733ff29c2b11ebe4d271893308a2c6eb2cf4e9b61c2cb",
    "gate-verification-001/verification.json": "65e292b34893b15862d70f37a9dfdb94bc22972bbc70044bc6431716349181fb",
}


def main(status_path, roster_path, brief_path):
    status_raw, roster_raw = Path(status_path).read_bytes(), Path(roster_path).read_bytes()
    status = json.loads(status_raw)
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    require(status["summary"]["total"] == len(status["sessions"]) == len(roster)
            and {row["id"] for row in status["sessions"]} == {row["id"] for row in roster},
            "Full app snapshots differ or were filtered")
    require(all(row["id"] == COORDINATOR or row["activity"]["status"] == "idle"
                for row in status["sessions"]), "Another session is active or has unknown activity")
    require([row["name"] for row in status["sessions"] if "B133" in row["name"]] == ["B133 kanji authoring"],
            "Duplicate B133 preparation/reviewer session exists")
    observed = datetime.fromtimestamp(Path(status_path).stat().st_mtime, timezone.utc)
    require(0 <= (datetime.now(timezone.utc) - observed).total_seconds() < 120,
            "Refresh the app status snapshot")
    brief_raw = frozen(brief_path)
    require(not (HERE / "review-preparation-admission-001.json").exists(), "Preserve admission")
    guard, _ = start_guard("B133 neutral review preparation admission")
    git = Git(REPO, RUNNER, guard)
    try:
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate identity differs")
        for name, digest in PROOFS.items():
            proof = json.loads(frozen(HERE / name, digest))
            require(proof["candidate"] == CANDIDATE and proof["base"] == BASE
                    and proof["status"] == "PASS" and not proof["memory"]["breach"], "Candidate proof differs")
        snapshots = {
            "status": write_frozen(HERE / "review-preparation-full-status-001.json", status_raw),
            "roster": write_frozen(HERE / "review-preparation-full-roster-001.txt", roster_raw),
        }
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "review-preparation-admission-001.json", {
        "status": "ADMITTED_PREPARATION_ONLY", "preparedAt": datetime.now(timezone.utc).isoformat(),
        "observedAt": observed.isoformat(), "candidate": CANDIDATE, "base": BASE, "sessionCount": len(roster),
        "snapshots": snapshots, "proofs": PROOFS,
        "brief": {"path": str(brief_path), "sha256": sha(brief_raw)}, "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))),
        "scope": "One bounded neutral-review preparation worker. Coordinator independently verifies "
                 "remaining finite packet evidence; its actual proof is required before reviewer admission.",
        "limits": "Not worker startup, content-review acceptance or publication.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: admit_b133_review_preparation.py STATUS ROSTER BRIEF")
    main(*sys.argv[1:])
