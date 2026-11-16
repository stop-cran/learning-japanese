"""Extend the two actually accepted followups to the exact signed integration."""
import json
from pathlib import Path

from b130_context_confirmation import binding
from b130_delta_closure_support import ACCEPTANCE_SHA, FINALS as PREVIOUS, ledger_acceptance
from b130_followup_lineage_v2 import require_followup_identity as require_previous_identity
from common import frozen, require, sha

CANDIDATE = "37a53e75446bacad8ade4e212404b121d4a01af1"
PRIOR_CANDIDATE = "1ac4053c5da955c3afaafc1e879e63a98ee42526"
RUNS = {"claude": "N1-B130-CLAUDE-CONFIRM-005", "gpt": "N1-B130-GPT-CONFIRM-004"}
BYTE_LIMITS = {"claude": 120000, "gpt": 180000}
INPUT_LIMITS = {"claude": 700000, "gpt": 600000}


def read(item):
    return json.loads(frozen(item["path"], item["sha256"]))


def require_followup_identity(spec, initial, launch, records):
    family = spec["family"]
    require(family in RUNS and spec["batch"] == 130 and spec["run"] == RUNS[family]
            and spec["candidate"] == CANDIDATE and spec["basis"] == "accepted-confirmation"
            and spec["priorVerdict"] == "CONFIRMED" and spec["openClaimIds"] == [],
            "Integration followup changes its fixed scope")
    prior_path = records / "confirm" / f"{PREVIOUS[family]}-acceptance.json"
    require(spec["prior"] == {"path": str(prior_path), "sha256": ACCEPTANCE_SHA[family]},
            "Integration skips the actual accepted prior report")
    previous_spec = json.loads(frozen(records / "confirm" / f"{PREVIOUS[family]}-spec.json"))
    require_previous_identity(previous_spec, initial, launch, records)
    prior = read(spec["prior"])
    previous_preflight = json.loads(frozen(records / "confirm" / f"{PREVIOUS[family]}-preflight.json"))
    ledger_acceptance(prior, previous_preflight)
    require(prior["candidate"] == PRIOR_CANDIDATE and prior["confirmationAccepted"] is True
            and prior["reviewEvidenceAccepted"] is True and prior["verdict"] == "CONFIRMED"
            and not prior["openClaimIds"] and not prior["acceptedNewFindings"]
            and all(spec[key] == previous_spec[key] for key in
                    ("session", "originalSession", "acceptance", "reviewerOrigin"))
            and spec["session"] == prior["session"] != launch["session"],
            "Integration does not continue the actual same-family reviewer")
    if family == "claude":
        require(spec["preparedOnlyPriorRun"] == previous_spec["preparedOnlyPriorRun"],
                "Historical unused preparation was changed")
    return previous_spec


def require_followup_preflight(record, config):
    records = Path(config["prompt"]).parent.parent
    spec_binding = binding(records / "confirm" / f"{record['run']}-spec.json")
    require(spec_binding in config["files"], "Integration spec is not bound")
    spec = read(spec_binding)
    initial = read(spec["acceptance"])
    launch = json.loads(frozen(records / f"{initial['run']}-launch.json"))
    require_followup_identity(spec, initial, launch, records)
    require(all(record[key] == spec[key] for key in
                ("run", "batch", "session", "candidate", "basis", "originalSession",
                 "reviewerOrigin", "prior", "capacityObservation"))
            and record["diffBase"] == PRIOR_CANDIDATE and record["priorRun"] == PREVIOUS[spec["family"]]
            and config["run"] == spec["run"] and config["expectedFamily"] == spec["family"],
            "Integration preflight changes lineage")


def check_capacity(observation, family, session, events_sha, chain_bytes):
    matches = [row for row in observation["reviewers"] if row["family"] == family]
    require(len(matches) == 1, "Missing or ambiguous capacity observation")
    row = matches[0]
    require(row["session"] == session and row["eventsSha256"] == events_sha
            and not row["observedCompactions"]
            and row["lastUsage"]["inputTokens"] <= INPUT_LIMITS[family]
            and row["remainingToReportedMaximum"] >= 250000
            and chain_bytes <= BYTE_LIMITS[family],
            "Current context or bounded integration packet exceeds the chosen safety envelope")
    return {"observedInputTokens": row["lastUsage"]["inputTokens"], "chainBytes": chain_bytes,
            "inputCeiling": INPUT_LIMITS[family], "packetByteCeiling": BYTE_LIMITS[family],
            "unchangedObservedEventPrefix": True,
            "limit": "Conservative per-run bounds, not a token-growth prediction or compaction guarantee."}


def verify_capacity(record, config, raw):
    observation = read(record["capacityObservation"])
    chain = read(record["chain"])
    return check_capacity(observation, config["expectedFamily"], record["session"], sha(raw),
                          sum(segment["bytes"] for segment in chain["segments"]))
