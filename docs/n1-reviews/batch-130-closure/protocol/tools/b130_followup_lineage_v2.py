"""Verify continuation of the actual fresh002 reviewers, not the original authors."""
import json
from pathlib import Path

from b130_context_confirmation import binding, verify_replacement
from common import frozen, load_batch, require
from confirm_followup import require_prior_state

PRIOR_SHA = {
    "claude": "4c10a6005fafd8a243265efed7bb73b040a9d0e833247b33da41f974624a039f",
    "gpt": "07ca737011314f7b7f55bcf6e5fea6be26821738c0d09d06c87326cbcc742c08",
}


def read(item):
    return json.loads(frozen(item["path"], item["sha256"]))


def require_followup_identity(spec, initial, launch, records):
    family = spec["family"]
    require(family in PRIOR_SHA and spec["batch"] == 130
            and spec["run"] == ("N1-B130-CLAUDE-CONFIRM-004" if family == "claude"
                            else "N1-B130-GPT-CONFIRM-003"),
            "New follow-up history requires an explicit successor")
    if family == "claude":
        from prepare_b130_claude004 import require_unused_claude003
        require(spec["preparedOnlyPriorRun"] == require_unused_claude003(),
                "Unused Claude003 preparation was skipped or relabelled")
    prior_run = f"N1-B130-{family.upper()}-CONFIRM-002"
    prior_path = records / "confirm" / f"{prior_run}-acceptance.json"
    origin_path = records / "confirm" / f"{prior_run}-spec.json"
    require(spec["prior"] == {"path": str(prior_path), "sha256": PRIOR_SHA[family]}
            and spec["reviewerOrigin"] == binding(origin_path), "Follow-up skips its actual origin")
    origin = read(spec["reviewerOrigin"])
    verify_replacement(origin, load_batch(130), initial, launch, records)
    prior = read(spec["prior"])
    require(prior["run"] == origin["run"] == prior_run
            and prior["family"] == family and spec["acceptance"] == origin["acceptance"]
            and spec["session"] == prior["session"] == origin["session"] != launch["session"]
            and spec["originalSession"] == origin["originalSession"] == launch["session"]
            and prior["candidate"] == origin["candidate"]
            and spec["candidate"] != prior["candidate"],
            "Continuing fresh reviewer or earlier snapshot differs")
    require_prior_state(spec, prior, [])
    final = read(prior["final"])
    audit, context, structure = (read(final[key]) for key in ("audit", "context", "structure"))
    require(final["session"] == prior["session"] and final["candidate"] == prior["candidate"]
            and final["run"] == prior_run and final["confirmation"] == prior["verdict"]
            and final["report"] == prior["report"]
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and context["status"] == structure["status"] == "PASS"
            and not context["compactions"] and context["eventsSha256"] == audit["eventsSha256"]
            and not audit["breaches"] and not audit["unexpectedUserMessages"]
            and audit["chainRead"] == audit["chainRequired"]
            and audit["reviewerIdle"] and not audit["recordIncomplete"],
            "Prior confirmation audit is not usable evidence")
    read(prior["adjudication"])
    frozen(prior["report"]["path"], prior["report"]["sha256"])
    return origin


def require_followup_preflight(record, config):
    records = Path(config["prompt"]).parent.parent
    spec_path = records / "confirm" / f"{record['run']}-spec.json"
    spec_binding = binding(spec_path)
    require(spec_binding in config["files"], "Follow-up spec is not bound to the packet")
    spec = read(spec_binding)
    initial = read(spec["acceptance"])
    launch = json.loads(frozen(records / f"{initial['run']}-launch.json"))
    require_followup_identity(spec, initial, launch, records)
    prior = read(spec["prior"])
    require(all(record[key] == spec[key] for key in
                ("run", "batch", "session", "candidate", "basis", "originalSession", "reviewerOrigin", "prior"))
            and record["diffBase"] == prior["candidate"] and record["priorRun"] == prior["run"]
            and config["run"] == spec["run"] and config["expectedFamily"] == spec["family"],
            "Follow-up preflight changes its bound lineage")
