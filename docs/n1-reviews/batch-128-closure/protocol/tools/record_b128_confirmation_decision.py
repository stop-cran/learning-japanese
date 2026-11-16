"""Bind a coordinator's explicit substantive adjudication to its audited raw report."""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha


def main(run):
    require(re.fullmatch(r"N1-B128-(CLAUDE|GPT)-CONFIRM-001", run), "Unexpected confirmation run")
    root = WS / "scratch-128" / "review" / "confirm"
    adjudication_path = root / f"{run}-adjudication.json"
    adjudication_raw = frozen(adjudication_path)
    adjudication = json.loads(adjudication_raw)
    final_path = root / f"{run}-final.json"
    final_raw = frozen(final_path, adjudication["evidence"]["mechanicalFinalSha256"])
    final = json.loads(final_raw)
    spec = json.loads(frozen(root / f"{run}-spec.json"))
    require(final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and final["run"] == adjudication["run"] == run
            and final["candidate"] == adjudication["candidate"] == spec["candidate"]
            and final["session"] == spec["session"] and final["report"] == adjudication["report"]
            and final["confirmation"] == adjudication["rawVerdict"]
            and adjudication["reviewEvidenceAccepted"] is True, "Decision and audited evidence differ")
    report = frozen(Path(final["report"]["path"]), final["report"]["sha256"]).decode("utf-8").replace("\r\n", "\n")
    findings = re.findall(r"(?m)^### (F\d+):", report)
    require(set(findings) == set(adjudication["acceptedNewFindings"]), "Unadjudicated new finding")
    if adjudication["confirmationAccepted"]:
        require(adjudication["rawVerdict"] == "CONFIRMED" and not findings
                and adjudication["openClaimIds"] == [], "A held report cannot become accepted")
    else:
        require(adjudication["openClaimIds"] or findings, "Unaccepted evidence needs an explicit hold")
    for name in ("context", "structure"):
        value = json.loads(frozen(final[name]["path"], final[name]["sha256"]))
        require(value["status"] == "PASS", f"Failed {name}")
    result = {
        "run": run, "family": spec["family"], "session": spec["session"], "candidate": final["candidate"],
        "verdict": adjudication["rawVerdict"], "reviewEvidenceAccepted": True,
        "confirmationAccepted": adjudication["confirmationAccepted"],
        "acceptedNewFindings": adjudication["acceptedNewFindings"], "openClaimIds": adjudication["openClaimIds"],
        "report": final["report"], "final": {"path": str(final_path), "sha256": sha(final_raw)},
        "adjudication": {"path": str(adjudication_path), "sha256": sha(adjudication_raw)},
    }
    print(freeze_json(root / f"{run}-acceptance.json", result))


if __name__ == "__main__":
    main(sys.argv[1])
