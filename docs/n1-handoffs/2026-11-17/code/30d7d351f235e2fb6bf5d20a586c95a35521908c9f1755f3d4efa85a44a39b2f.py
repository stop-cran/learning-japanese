"""Record both usable, unaccepted confirmations and admit their bounded repair."""
import datetime
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_batch, require, sha, start_guard, write_frozen
from confirm_v2 import binding, clean
from scoped_admission import assess_status

ROOT = WS / "scratch-124" / "review"
CANDIDATE = "fa394d237e28df96319495a003718cc9c880a069"
AUTHOR = "968b727f-61e7-4abf-bf6a-a144903ab93a"
RUNS = {
    "claude": ("CONFIRMED", "965e4ff377443a615262397fd61066aeda38fa9d5764f9e3a79606b284a7cdf8",
               ["Q1", "Q5"]),
    "gpt": ("UNVERIFIED", "784c1d2e55ac85a216240ec18fffc70a17892da1ff937b459948138fa514312f",
            ["Q1", "Q3", "Q4", "Q5", "Q7", "Q8", "Q10", "Q11", "Q16"]),
}


def main(snapshot):
    config = load_batch(124)
    clean(config, CANDIDATE)
    source_path = ROOT / "coordinator-reconciliation-verification-001.json"
    source = json.loads(frozen(source_path,
                              "4a2622178667f86cb0c6a80b4e1e2cedde2846d2d34511b84c828f09c24edcc0"))
    require(source["status"] == "PASS" and source["candidate"] == CANDIDATE
            and not source["memory"]["breach"], "Source verification differs")
    brief = ROOT / "b124-reconciliation-002-brief.txt"
    frozen(brief)
    mechanics = {}
    for family, (verdict, digest, _) in RUNS.items():
        run = f"N1-B124-{family.upper()}-CONFIRM-001"
        final_path = ROOT / "confirm" / f"{run}-final.json"
        final = json.loads(frozen(final_path, digest))
        require(final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
                and final["confirmation"] == verdict and final["candidate"] == CANDIDATE
                and final["run"] == run, "Confirmation mechanics differ")
        for field in ("report", "context", "structure", "audit"):
            frozen(final[field]["path"], final[field]["sha256"])
        for suffix in ("acceptance", "adjudication"):
            require(not (ROOT / "confirm" / f"{run}-{suffix}.json").exists(),
                    "Preserve existing adjudications")
        mechanics[family] = (final_path, final)
    status_path = Path(snapshot)
    now = datetime.datetime.now(datetime.timezone.utc)
    require(abs(now.timestamp() - status_path.stat().st_mtime) < 180, "Status snapshot stale")
    raw = status_path.read_bytes()
    status = json.loads(raw)
    guard, resource = start_guard("B124 reconciliation 002 admission")
    try:
        assessment = assess_status(status, "", resource.available_ram())
        require(assessment["startupFloorMet"] and not assessment["blockingSessions"],
                json.dumps(assessment, ensure_ascii=False))
        author = [row for row in status["sessions"] if row["id"] == AUTHOR]
        require(len(author) == 1 and author[0]["activity"]["status"] == "idle"
                and not author[0].get("awaiting_user_input") and not author[0].get("awaiting_input")
                and not author[0].get("pending_plan"), "Original author is not ready")
        clean(config, CANDIDATE)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Author admission RAM breach")
    accepted = []
    for family, (verdict, _, claims) in RUNS.items():
        final_path, final = mechanics[family]
        run = final["run"]
        adjudication = freeze_json(ROOT / "confirm" / f"{run}-adjudication.json", {
            "run": run, "candidate": CANDIDATE, "rawVerdict": verdict,
            "status": "USABLE_EVIDENCE_WITH_CONSEQUENTIAL_OPEN_CLAIMS",
            "reviewEvidenceAccepted": True, "confirmationAccepted": False,
            "acceptedNewFindings": [], "openClaimIds": claims,
            "requiredFixAssessment": "Original required corrections are source-supported and resolved.",
            "semanticAssessment": (
                "The positive character-level wealth evidence leaves Q1/Q5 consequential. "
                "The optional harmless judgment is not adopted merely from narrower displayed titles "
                "or absence in a selected standalone word entry. Punctuation normalization is "
                "contributor-only and not a runtime defect."
                if family == "claude" else
                "Accept the nine explicit source-bounded unresolved comparisons as consequential "
                "uncertainty, not established new findings. The five no-new-guard assessments "
                "explicitly consider the supplied secondary senses and remain bounded judgments."
            ),
            "coordinatorDecision": "Apply conservative direct guards for the nine retained pairs "
                                   "under the separately frozen correction brief; this is not "
                                   "a claim of universal Japanese synonymy or a reviewer finding.",
            "limits": "Raw verdict, optional judgments and all report limits remain unchanged. "
                      "No publication or exact-snapshot confirmation acceptance.",
        })
        accepted.append(freeze_json(ROOT / "confirm" / f"{run}-acceptance.json", {
            "run": run, "family": family, "session": final["session"], "candidate": CANDIDATE,
            "verdict": verdict, "reviewEvidenceAccepted": True, "confirmationAccepted": False,
            "acceptedNewFindings": [], "openClaimIds": claims,
            "report": final["report"], "final": binding(final_path), "adjudication": adjudication,
        }))
    result = freeze_json(ROOT / "reconciliation-002-author-admission.json", {
        "batch": 124, "candidate": CANDIDATE, "author": AUTHOR,
        "brief": binding(brief), "sourceProof": binding(source_path),
        "heldConfirmations": accepted,
        "status": write_frozen(ROOT / "reconciliation-002-author-status.json", raw),
        "assessment": assessment, "memory": memory, "admittedAt": now.isoformat(),
        "producerSha256": sha(frozen(Path(__file__))),
        "scope": "Resume the existing author for nine conservative direct-pair guards only. "
                 "No publication, reviewer restart or new batch is admitted.",
    })
    print(json.dumps(result))
    print(json.dumps(binding(brief)))


if __name__ == "__main__":
    main(sys.argv[1])
