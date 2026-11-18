"""Admit one B134 neutral review-preparation worker from fresh full app snapshots and actual proofs."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from scoped_admission import assess_status
from verify_b134_payload import BASE, HERE, REPO, RUNNER
from verify_b134_sources import FINGERPRINT, Git, OWNER

CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
SESSION = "B134 review preparation"
PROOFS = {
    "source-proof-002.json": "f3a80ee569a1bfd4f452e3f413a6377f5d01cac665e978dfc3e6db722c809393",
    "payload-proof-001.json": "ec47228ee313a82d872e7235f6f4a6b048737f24254d26405418c840dbd65d1a",
    "gate-verification-002/verification.json": "1caed56d80a213605d59eac6cc7ecc69829083cbdaa606b684edd77fb9162694",
}
OUTPUT = HERE / "review-preparation-admission-001.json"


def main(status_path, roster_path, brief_path):
    status_path, roster_path = Path(status_path), Path(roster_path)
    observed = min(status_path.stat().st_mtime, roster_path.stat().st_mtime)
    require(0 <= datetime.now(timezone.utc).timestamp() - observed < 120, "Refresh the app snapshots")
    status_raw, roster_raw = status_path.read_bytes(), roster_path.read_bytes()
    status = json.loads(status_raw)
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    ids = [row["id"] for row in roster]
    require(len(ids) == len(set(ids)) == status["summary"]["total"] == len(status["sessions"])
            and set(ids) == {row["id"] for row in status["sessions"]},
            "Full app snapshots differ or were filtered")
    batch_names = sorted(row.get("name") or "" for row in status["sessions"] if "B134" in (row.get("name") or ""))
    require(batch_names == ["B134 kanji authoring"], f"Unexpected B134 sessions: {batch_names}")
    brief_raw = frozen(brief_path)
    require(not OUTPUT.exists(), "Preserve the existing admission")
    guard, resource = start_guard("B134 neutral review preparation admission")
    try:
        assessment = assess_status(status, SESSION, resource.available_ram())
        require(assessment["statusAllowsAdmission"], json.dumps(assessment, ensure_ascii=False))
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate identity differs")
        for name, digest in PROOFS.items():
            proof = json.loads(frozen(HERE / name, digest))
            require(proof["candidate"] == CANDIDATE and proof["base"] == BASE
                    and proof["status"] == "PASS" and not proof["memory"]["breach"], f"Proof differs: {name}")
        snapshots = {
            "status": write_frozen(HERE / "review-preparation-full-status-001.json", status_raw),
            "roster": write_frozen(HERE / "review-preparation-full-roster-001.txt", roster_raw),
        }
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    require(datetime.now(timezone.utc).timestamp() - observed < 120, "Admission expired")
    print(json.dumps(freeze_json(OUTPUT, {
        **assessment, "status": "ADMITTED_PREPARATION_ONLY", "batch": 134, "sessionName": SESSION,
        "preparedAt": datetime.now(timezone.utc).isoformat(),
        "observedAt": datetime.fromtimestamp(observed, timezone.utc).isoformat(),
        "candidate": CANDIDATE, "base": BASE, "sessionCount": len(ids), "batchSessions": batch_names,
        "snapshots": snapshots, "proofs": PROOFS,
        "brief": {"path": str(brief_path), "sha256": sha(brief_raw)}, "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))),
        "scope": "One bounded neutral-review preparation worker. Coordinator independently verifies "
                 "remaining finite packet evidence; its actual proof is required before reviewer admission.",
        "limits": "Not worker startup, content-review acceptance or publication.",
    }), ensure_ascii=False))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: admit_b134_review_preparation.py STATUS ROSTER BRIEF")
    main(*sys.argv[1:])
