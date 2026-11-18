"""Collect the actual B132 initial-controller schema without rewriting its evidence.

The earlier collector describes B131's separate context/structure records. B132
embeds structure in its final record and context telemetry in its event audit.
Derivatives returned here must be archived with their explicit original hashes.
Confirmation collection is deliberately not inferred from this initial schema.
"""
import re

from common import json_bytes, require, sha
from b132_closure_records import (CANDIDATE, MECHANICAL_STATUS, UUID, checked_json,
                                 archive_path, closed_progress, validate_resolution)


def collect_initial_record(spec, preflight_ref, final_ref, read):
    family, run, session = (spec[name] for name in ("family", "run", "session"))
    require(family in ("claude", "gpt") and spec["role"] == "initial"
            and spec["snapshot"] == CANDIDATE and UUID.fullmatch(session)
            and re.fullmatch("N1-B132-" + family.upper() + r"-[0-9]{3}", run),
            "Invalid initial-review identity")
    acceptance = checked_json(spec["acceptance"], read)
    final = checked_json(final_ref, read)
    preflight = checked_json(preflight_ref, read)
    launch = preflight["runs"][family]
    config = checked_json(launch["auditConfig"], read)
    adjudication = checked_json(acceptance["adjudication"], read)
    audit = checked_json(final["audit"], read)
    for label, record in (("acceptance", acceptance), ("final", final), ("adjudication", adjudication)):
        require(record["run"] == run and record["candidate"] == CANDIDATE,
                f"{label} identifies another review")
    require(acceptance["reviewAccepted"] is True and acceptance["verdict"] == spec["verdict"]
            and acceptance["finalSha256"] == final_ref["sha256"],
            "Unaccepted or unbound initial review")
    require(final["session"] == session and final["status"] == MECHANICAL_STATUS
            and final["problems"] == [], "Mechanical final is incomplete")
    report = final["report"]
    require(config["candidate"] == preflight["candidate"] == CANDIDATE
            and launch["run"] == config["run"] == run and config["expectedFamily"] == family
            and config["report"] == launch["report"] == report["path"],
            "Report, preflight or audit configuration differs")
    require(sha(read(report["path"], report["sha256"])) == report["sha256"]
            == acceptance["reportSha256"] == adjudication["reportSha256"]
            and adjudication["finalSha256"] == final_ref["sha256"],
            "Report/adjudication hash binding differs")
    require(adjudication["claimsAdjudicated"] is True
            and adjudication["verdict"] == spec["verdict"]
            and isinstance(adjudication["claimChecks"], list) and adjudication["claimChecks"]
            and all(isinstance(item, dict)
                    and all(isinstance(item.get(key), str) and item[key].strip()
                            for key in ("claim", "evidence", "disposition"))
                    for item in adjudication["claimChecks"]),
            "Substantive claim adjudication is missing")
    require(audit["run"] == run and audit["session"] == session and audit["final"] is True
            and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and audit["bootstrapVerified"] is True
            and audit["reviewerIdle"] is True and audit["recordIncomplete"] is False
            and audit["breaches"] == [] and type(audit["unexpectedUserMessages"]) is int
            and audit["unexpectedUserMessages"] == audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"] is True
            and len(audit["messages"]) == 2 and audit["messages"][-1].strip() == spec["verdict"],
            "Incomplete or breached execution audit")
    for name in ("core", "extension"):
        require(type(audit[f"{name}Required"]) is int and audit[f"{name}Required"] > 0
                and type(audit[f"{name}Read"]) is int
                and audit[f"{name}Read"] == audit[f"{name}Required"], "Incomplete read coverage")
    models = audit["actualResponseModels"]
    telemetry = audit["capacityTelemetry"]
    require(models and all(isinstance(model, str) and model.startswith(family + "-") for model in models)
            and telemetry["status"] == "PASS" and telemetry["errors"] == []
            and telemetry["compactions"] == [] and telemetry["family"] == family,
            "Observed family/context telemetry differs")
    structure = final["structure"]
    require(structure["status"] == "PASS" and structure["overall"] == spec["verdict"]
            and spec["verdict"] in ("CLEAN", "NEEDS FIX", "UNVERIFIED"), "Structure or verdict differs")
    claims = {}
    for field in ("acceptedFindings", "openClaimIds", "coordinatorClaimIds"):
        ids = adjudication[field]
        require(isinstance(ids, list) and all(isinstance(item, str) and item for item in ids)
                and len(ids) == len(set(ids)), f"Explicit unique {field} inventory required")
        claims[field] = ids
    fields = ("run", "session", "eventsSha256", "eventsBytes", "status", "breaches",
              "bootstrapVerified", "actualResponseModels", "reviewerIdle", "recordIncomplete",
              "coreRead", "coreRequired", "extensionRead", "extensionRequired",
              "writes", "readbacks", "readbackVerified", "reportBinding", "fetches")
    summary = {field: audit[field] for field in fields}
    summary.update(originalAuditSha256=final["audit"]["sha256"], rawExecutionPayloadsRemainLocal=True,
                   representation="Bounded derivative; raw calls, messages and events remain local.")
    context = {
        "status": "PASS", "eventsSha256": audit["eventsSha256"],
        "originalAuditSha256": final["audit"]["sha256"], "capacityTelemetry": telemetry,
        "representation": "Exact capacityTelemetry member from the frozen original event audit.",
    }
    refs = {
        "acceptance": spec["acceptance"], "final": final_ref, "report": report,
        "adjudication": acceptance["adjudication"], "audit": final["audit"],
        "preflight": preflight_ref, "auditConfig": launch["auditConfig"],
    }
    derivatives = {"audit-summary": json_bytes(summary), "context": json_bytes(context),
                   "structure": json_bytes({
                       "originalFinalSha256": final_ref["sha256"], "structure": structure,
                       "representation": "Exact structure member from the frozen final record."})}
    return refs, derivatives, claims
