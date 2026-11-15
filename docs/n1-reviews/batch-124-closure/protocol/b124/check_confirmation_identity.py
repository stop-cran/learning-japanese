"""Record the scoped original-reviewer identity assessment for an already admitted confirmation."""
import json
import sys

from common import COORDINATOR, WS, freeze_json, frozen, require, sha
from scoped_confirmation_admission import assess_confirmation_status

CONFIRM = WS / "scratch-124" / "review" / "confirm"


def main(run):
    admission_path = CONFIRM / f"{run}-admission.json"
    admission_raw = frozen(admission_path)
    admission = json.loads(admission_raw)
    status_raw = frozen(admission["status"]["path"], admission["status"]["sha256"])
    status = json.loads(status_raw)
    assessment = assess_confirmation_status(status, admission["session"], admission["freeRamBytes"])
    others = [s["id"] for s in status["sessions"] if s["id"] != COORDINATOR
              and ((s.get("activity") or {}).get("status") != "idle" or s.get("is_running"))]
    require(assessment["statusAllowsAdmission"] and not others, "Admitted status fails the scoped identity check")
    print(json.dumps(freeze_json(CONFIRM / f"{run}-scoped-identity.json", {
        "run": run, "admission": {"path": str(admission_path), "sha256": sha(admission_raw)},
        "status": admission["status"], "assessment": assessment, "otherActiveSessions": others,
        "limits": "Post-admission check of the frozen admitted snapshot. The strict all-idle confirm_v2 gate "
                  "admitted the run; this adds the original-reviewer name/scope checks only.",
    }), ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
