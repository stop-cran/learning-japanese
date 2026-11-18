"""Admit the same author for the nine source-specific held comparisons."""
import datetime
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_batch, require, sha, start_guard, write_frozen
from confirm_v2 import binding, clean
from scoped_admission import assess_status

REVIEW = WS / "scratch-123" / "review"
CANDIDATE = "047970a055903c0337d73823288695938648dd1d"
AUTHOR = "3fb8a285-ebf3-456e-89ed-5e4b77b0f0a1"


def main(snapshot):
    config = load_batch(123)
    clean(config, CANDIDATE)
    proofs = []
    for name, digest in (
        ("coordinator-reconciliation-verification-002.json",
         "c7a9b6721556e4db4d7619d4f677a75957c834c6ce31cc03d40b8ce86ea11713"),
        ("coordinator-reconciliation-selection-002.json",
         "e6242f59ed47fed5a58a5af2a1260616cea3bdc158fb2f3a84776ae29bf9ae43"),
    ):
        proof = json.loads(frozen(REVIEW / name, digest))
        require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE,
                "Prior candidate proof differs")
        proofs.append(binding(REVIEW / name))
    source = REVIEW / "open-pair-sources-001" / "provenance.json"
    record = json.loads(frozen(source, "e0ae19c482922dab9076bb08768b6395e55fb0cef4d83773b0dce0febe612996"))
    require(record["candidate"] == CANDIDATE and len(record["sources"]) == 9,
            "New source scope differs")
    for item in record["sources"]:
        for key in ("raw", "extract"):
            frozen(Path(item[key]["path"]), item[key]["sha256"])
    held_path = REVIEW / "confirm" / "N1-B123-GPT-CONFIRM-002-acceptance.json"
    held = json.loads(frozen(held_path))
    require(held["candidate"] == CANDIDATE and held["verdict"] == "UNVERIFIED"
            and held["reviewEvidenceAccepted"] and not held["confirmationAccepted"]
            and held["acceptedNewFindings"] == []
            and held["openClaimIds"] == [f"Q{i}" for i in range(1, 10)],
            "Held GPT evidence or claim identity differs")
    adjudication = json.loads(frozen(Path(held["adjudication"]["path"]),
                                    held["adjudication"]["sha256"]))
    require([item["id"] for item in adjudication["coordinatorFindings"]] == ["C2", "C3"],
            "New source findings differ")
    for key in ("report", "final"):
        frozen(Path(held[key]["path"]), held[key]["sha256"])
    status_path = Path(snapshot)
    now = datetime.datetime.now(datetime.timezone.utc)
    require(abs(now.timestamp() - status_path.stat().st_mtime) < 180, "Status snapshot stale")
    raw = status_path.read_bytes()
    status = json.loads(raw)
    guard, resource = start_guard("B123 reconciliation 003 admission")
    try:
        assessment = assess_status(status, "", resource.available_ram())
        require(assessment["startupFloorMet"] and not assessment["blockingSessions"],
                json.dumps(assessment, ensure_ascii=False))
        author = [item for item in status["sessions"] if item["id"] == AUTHOR]
        require(len(author) == 1 and author[0]["activity"]["status"] == "idle"
                and not author[0].get("awaiting_user_input")
                and not author[0].get("awaiting_input") and not author[0].get("pending_plan"),
                "Original author not ready")
        clean(config, CANDIDATE)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Admission RAM breach")
    brief = REVIEW / "b123-reconciliation-003-brief.txt"
    brief.chmod(0o444)
    Path(held["adjudication"]["path"]).chmod(0o444)
    Path(__file__).chmod(0o444)
    print(json.dumps(freeze_json(REVIEW / "b123-reconciliation-003-admission.json", {
        "batch": 123, "candidate": CANDIDATE, "author": AUTHOR,
        "brief": binding(brief), "proofs": proofs, "heldConfirmation": binding(held_path),
        "newSources": binding(source), "adjudication": held["adjudication"],
        "status": write_frozen(REVIEW / "b123-reconciliation-003-admission-status.json", raw),
        "assessment": assessment, "memory": memory, "admittedAt": now.isoformat(),
        "producerSha256": sha(Path(__file__).read_bytes()),
        "scope": "One original author, source-specific reconciliation only; no publication or reviews.",
    })))
    print(json.dumps(binding(brief)))


if __name__ == "__main__":
    main(sys.argv[1])
