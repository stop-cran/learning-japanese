"""Admit the existing author for a bounded, additive response-attribution correction."""
import datetime
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_batch, require, sha, start_guard, write_frozen
from confirm_v2 import clean
from scoped_admission import assess_status

AUTHOR = "968b727f-61e7-4abf-bf6a-a144903ab93a"
CANDIDATE = "be2aaeac504be19860a9a69de499d8202863bde9"
REVIEW = WS / "scratch-124" / "review"
PROOF_SHA = "d914e5e63ab5e576aae26104276b8bb7b1fad1b81656923d48b510a522594dc2"


def main(status_path):
    require(abs(datetime.datetime.now().timestamp() - status_path.stat().st_mtime) < 180, "Status is stale")
    raw = status_path.read_bytes()
    status = json.loads(raw)
    authors = [item for item in status["sessions"] if item["id"] == AUTHOR]
    require(len(authors) == 1 and authors[0]["activity"]["status"] == "idle"
            and not authors[0].get("awaiting_user_input") and not authors[0].get("awaiting_plan_approval"),
            "Existing author is not ready")
    proof = json.loads(frozen(REVIEW / "coordinator-reconciliation-verification-002.json", PROOF_SHA))
    require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE
            and not proof["memory"]["breach"], "Signed candidate verification differs")
    clean(load_batch(124), CANDIDATE)
    brief = REVIEW / "b124-response-correction-001-brief.txt"
    brief_raw = frozen(brief)
    guard, resource = start_guard("B124 additive response correction admission")
    try:
        assessment = assess_status(status, "", resource.available_ram())
        require(assessment["statusAllowsAdmission"], json.dumps(assessment, ensure_ascii=False))
        captured = write_frozen(REVIEW / "response-correction-001-status.json", raw)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Admission RAM guard breached")
    print(json.dumps(freeze_json(REVIEW / "response-correction-001-admission.json", {
        "candidate": CANDIDATE, "author": AUTHOR, "verificationSha256": PROOF_SHA,
        "brief": {"path": str(brief), "sha256": sha(brief_raw)}, "status": captured,
        "assessment": assessment, "memory": memory,
        "scope": "Two additive contributor documents only; no reviewer launch or publication acceptance.",
    })))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
