"""Capture full app snapshots and admit one serial neutral-packet preparation worker."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from common import COORDINATOR, freeze_json, frozen, require, sha, start_guard, write_frozen
from prepare_b131_source_facts import CANDIDATE, CANDIDATE_BASE, HERE, REPO, RUNNER
from verify_b131_sources import FINGERPRINT, Git, OWNER

PROOFS = {
    "source-verification-001.json": "99a7a9a11c213280ddae0110fceec9599a7d4d47451e1b3fb1ae6a9e2ab6ac33",
    "source-union-verification-001.json": "1735390e50f8768da2cdf264b8157dc19a31e690970cd689b4fc9077e97677f5",
    "payload-verification-001.json": "dc3f1068362350bd81fdc8ec94e20b32589b0fdcdb25248a911e4817ffb068d6",
    "gate-verification-002/verification.json": "82fbf0d68e879e0371e9226ac322c81c2e13118fdbd5711e7901bef79f155751",
    "packet-verification-002/verification.json": "cefe31cf4020dcad2601bafff5446451c73cda86b451f34b54da7683a8167c89",
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
    require([row["name"] for row in status["sessions"] if "B131" in row["name"]] == ["B131 kanji authoring"],
            "Duplicate B131 preparation/reviewer session exists")
    require(datetime.now(timezone.utc).timestamp() - Path(status_path).stat().st_mtime < 600,
            "Refresh the app status snapshot")
    brief_raw = frozen(brief_path)
    require(not (HERE / "review-preparation-admission-001.json").exists(), "Preserve admission")
    guard, _ = start_guard("B131 neutral review preparation admission")
    git = Git(REPO, RUNNER, guard)
    try:
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{CANDIDATE_BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate identity differs")
        for name, digest in PROOFS.items():
            proof = json.loads(frozen(HERE / name, digest))
            require(proof["candidate"] == CANDIDATE and proof["base"] == CANDIDATE_BASE
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
        "candidate": CANDIDATE, "base": CANDIDATE_BASE, "sessionCount": len(roster),
        "snapshots": snapshots, "proofs": PROOFS,
        "brief": {"path": str(brief_path), "sha256": sha(brief_raw)}, "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))),
        "scope": "One bounded neutral-review preparation worker. All other listed sessions were idle "
                 "at this snapshot; this observation does not reserve unrelated work or admit a future reviewer.",
        "limits": "Not worker startup, content-review acceptance or publication.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: admit_b131_review_preparation.py STATUS ROSTER BRIEF")
    main(*sys.argv[1:])
