"""Validate continued work by an explicitly audited replacement reviewer."""
import json
from pathlib import Path

from common import frozen, require, sha
from confirm_replacement import require_replacement


def read(item):
    return json.loads(frozen(Path(item["path"]), item["sha256"]))


def verify_origin(spec, initial, launch, records):
    reference = spec["reviewerOrigin"]
    origin = read(reference)
    require(origin["session"] == spec["session"] != launch["session"]
            and origin["originalSession"] == launch["session"]
            and origin["family"] == spec["family"] and origin["batch"] == spec["batch"]
            and origin["acceptance"] == spec["acceptance"],
            "Replacement origin belongs to another reviewer or initial review")
    held = read(origin["unavailable"])
    require_replacement(origin, initial, launch, held, read(held["context"]), read(origin["prior"]))
    accepted_path = records / "confirm" / f"{origin['run']}-acceptance.json"
    accepted = json.loads(frozen(accepted_path))
    mechanics = read(accepted["final"])
    require(accepted["reviewEvidenceAccepted"] is True
            and accepted["run"] == mechanics["run"] == origin["run"]
            and accepted["candidate"] == mechanics["candidate"] == origin["candidate"]
            and accepted["session"] == mechanics["session"] == origin["session"]
            and accepted["family"] == origin["family"]
            and accepted["verdict"] == mechanics["confirmation"]
            and accepted["report"] == mechanics["report"]
            and mechanics["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
            "Replacement origin has no accepted mechanical review evidence")
    context, structure, audit = (read(mechanics[key]) for key in ("context", "structure", "audit"))
    require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
            and audit["eventsSha256"] == context["eventsSha256"]
            and not audit["breaches"] and audit["reviewerIdle"]
            and audit["chainRead"] == audit["chainRequired"],
            "Replacement origin audit failed")
    read(accepted["adjudication"])
    frozen(Path(accepted["report"]["path"]), accepted["report"]["sha256"])
    prior = read(spec["prior"])
    prior_spec_path = records / "confirm" / f"{prior['run']}-spec.json"
    prior_spec_raw = frozen(prior_spec_path)
    prior_spec = json.loads(prior_spec_raw)
    if prior["run"] == origin["run"]:
        require(sha(prior_spec_raw) == reference["sha256"]
                and prior_spec_path.resolve() == Path(reference["path"]).resolve(),
                "Follow-up changes its replacement origin")
    else:
        require(prior_spec.get("reviewerOrigin") == reference,
                "Follow-up skips its recorded replacement origin")
    require(prior["session"] == spec["session"] and prior["family"] == spec["family"],
            "Follow-up changes the continuing reviewer")
    return origin


def require_followup_identity(spec, initial, launch, records):
    if spec["session"] == launch["session"]:
        require("reviewerOrigin" not in spec, "Original reviewer has an unexpected replacement origin")
        return None
    require("reviewerOrigin" in spec, "Changed reviewer has no audited replacement origin")
    return verify_origin(spec, initial, launch, records)
