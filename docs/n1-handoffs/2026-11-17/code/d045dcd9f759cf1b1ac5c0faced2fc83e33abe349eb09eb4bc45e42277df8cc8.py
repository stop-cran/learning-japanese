"""Admit one new author from fresh matching full status and roster evidence."""
import datetime
import json
import sys
import time
from pathlib import Path

FILES = Path(__file__).resolve().parent
ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
sys.path.insert(0, str(ROOT / "review-tools"))
from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from scoped_admission import assess_status
from verify_b133_packet import RUNNER
from verify_b133_sources import FINGERPRINT, OWNER, Git

BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"


def main(status_path, roster_path):
    observed = min(status_path.stat().st_mtime, roster_path.stat().st_mtime)
    require(0 <= time.time() - observed < 120, "Admission inputs are stale")
    status_raw, roster_raw = status_path.read_bytes(), roster_path.read_bytes()
    status = json.loads(status_raw)
    roster_text = roster_raw.decode("utf-8")
    roster = json.loads(roster_text[roster_text.index("["):])
    ids = [row["id"] for row in roster]
    require(len(ids) == len(set(ids)) and set(ids) == {row["id"] for row in status["sessions"]}
            and len(ids) == status["summary"]["total"], "Full status/roster identity sets differ")
    prepared_path = FILES / "b134-preparation-001" / "prepared.json"
    prepared_raw = frozen(prepared_path)
    prepared = json.loads(prepared_raw)
    kickoff = frozen(FILES / "b134-author-kickoff.txt", prepared["kickoff"]["sha256"])
    require(prepared["batch"] == 134 and prepared["base"] == BASE and prepared["clean"]
            and prepared["publishedRecords"] == 271 and prepared["remaining"] == 957,
            "Preparation binding differs")
    guard, resource = start_guard("B134 author admission")
    try:
        assessment = assess_status(status, "B134 kanji authoring", resource.available_ram())
        require(assessment["statusAllowsAdmission"], json.dumps(assessment))
        git = Git(ROOT / "b134-worktree", RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == BASE
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and git("show", "-s", "--format=%G?|%GF|%ae|%ce", BASE).decode().strip()
                == f"G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == BASE,
                "Prepared tree, owner signature or remote base changed")
        status_ref = write_frozen(FILES / "b134-launch-full-status-001.json", status_raw)
        roster_ref = write_frozen(FILES / "b134-launch-full-roster-001.txt", roster_raw)
    finally:
        memory = guard.finish()
    require(not memory["breach"] and time.time() - observed < 120, "Admission expired or RAM breach")
    print(freeze_json(FILES / "b134-launch-admission-001.json", {
        **assessment, "batch": 134, "base": BASE, "preparedSha256": sha(prepared_raw),
        "kickoffSha256": sha(kickoff), "observedAtEpochMs": int(observed * 1000),
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "statusSnapshot": status_ref, "rosterSnapshot": roster_ref, "rosterCount": len(ids),
        "admitted": True, "memory": memory, "producerSha256": sha(frozen(Path(__file__))),
    }))


if __name__ == "__main__":
    main(*(Path(value) for value in sys.argv[1:]))
