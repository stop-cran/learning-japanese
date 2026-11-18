"""Collect fresh B134 review evidence without treating it as original confirmation."""
import re

from b132_closure_records import UUID, checked_json
from b134_initial_records import INITIALS, MECHANICAL_STATUS, disposition_ids, normalize_claims
from b134_review_history import FAILED_SESSION
from b134_token_meter import PROFILES
from common import json_bytes, require, sha


def collect_replacement_record(spec, preflight_ref, final_ref, read):
    family, run, session, snapshot = (spec[name] for name in ("family", "run", "session", "snapshot"))
    require(family in INITIALS and spec["role"] == "replacement-independent"
            and UUID.fullmatch(session) and session not in
            {FAILED_SESSION, *(known["session"] for known in INITIALS.values())}
            and re.fullmatch("N1-B134-" + family.upper() + r"-FRESH-[0-9]{3}", run)
            and re.fullmatch(r"[0-9a-f]{40}", snapshot)
            and spec["originalSession"] == INITIALS[family]["session"]
            and spec["originalReviewerConfirmation"] is False
            and "confirmation" not in spec, "Invalid fresh independent-review identity")
    acceptance = checked_json(spec["acceptance"], read)
    final = checked_json(final_ref, read)
    preflight = checked_json(preflight_ref, read)
    launch = preflight["runs"][family]
    config = checked_json(launch["auditConfig"], read)
    adjudication = checked_json(acceptance["adjudication"], read)
    audit = checked_json(final["audit"], read)
    for label, record in (("acceptance", acceptance), ("final", final), ("adjudication", adjudication)):
        require(record["run"] == run and record["candidate"] == snapshot,
                label + " identifies another replacement review")
    require(spec["verdict"] in ("CLEAN", "NEEDS FIX", "UNVERIFIED")
            and acceptance["reviewAccepted"] is True and acceptance["verdict"] == spec["verdict"]
            and acceptance["finalSha256"] == final_ref["sha256"]
            and final["session"] == session and final["status"] == MECHANICAL_STATUS
            and final["problems"] == [], "Unaccepted or incomplete fresh final")
    report = final["report"]
    require(config["candidate"] == preflight["candidate"] == snapshot
            and launch["run"] == config["run"] == run and config["expectedFamily"] == family
            and config["report"] == launch["report"] == report["path"],
            "Fresh report or configuration binding differs")
    require(isinstance(config["files"], list) and config["files"], "Missing frozen input inventory")
    for ref in config["files"]:
        require(sha(read(ref["path"], ref["sha256"])) == ref["sha256"], "Fresh input changed")
    report_raw = read(report["path"], report["sha256"])
    require(sha(report_raw) == report["sha256"] == acceptance["reportSha256"]
            == adjudication["reportSha256"]
            and adjudication["finalSha256"] == final_ref["sha256"],
            "Fresh report or adjudication hash differs")
    require(adjudication["claimsAdjudicated"] is True and adjudication["verdict"] == spec["verdict"]
            and isinstance(adjudication["claimChecks"], list) and adjudication["claimChecks"]
            and all(isinstance(item, dict)
                    and all(isinstance(item.get(key), str) and item[key].strip()
                            for key in ("claim", "evidence", "disposition"))
                    for item in adjudication["claimChecks"]),
            "Fresh substantive adjudication is missing")
    require(audit["run"] == run and audit["session"] == session and audit["final"] is True
            and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and audit["bootstrapVerified"] is True
            and audit["reviewerIdle"] is True and audit["recordIncomplete"] is False
            and audit["breaches"] == [] and type(audit["unexpectedUserMessages"]) is int
            and audit["unexpectedUserMessages"] == audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"] is True
            and len(audit["messages"]) == 2 and audit["messages"][-1].strip() == spec["verdict"],
            "Incomplete or breached fresh execution audit")
    for name in ("core", "extension"):
        require(type(audit[f"{name}Required"]) is int and audit[f"{name}Required"] > 0
                and type(audit[f"{name}Read"]) is int
                and audit[f"{name}Read"] == audit[f"{name}Required"], "Incomplete fresh read coverage")
    models, telemetry, profile = audit["actualResponseModels"], audit["capacityTelemetry"], PROFILES[family]
    require(models and all(isinstance(model, str) and model.startswith(family + "-") for model in models)
            and telemetry["status"] == "PASS" and telemetry["errors"] == []
            and telemetry["compactions"] == [] and telemetry["family"] == family
            and all(config["contextProfile"][key] == telemetry["contextProfile"][key] == value
                    for key, value in profile.items())
            and isinstance(telemetry["observedMaxPromptTokens"], list)
            and telemetry["observedMaxPromptTokens"]
            and all(type(value) is int and value == profile["maxPromptTokens"]
                    for value in telemetry["observedMaxPromptTokens"])
            and type(telemetry["actualPeakInputTokens"]) is int
            and 0 <= telemetry["actualPeakInputTokens"] <= profile["maxPromptTokens"],
            "Fresh observed model or context telemetry differs")
    bootstrap_ref = audit.get("bootstrapRecord")
    authorization_ref = audit.get("coreAuthorization")
    snapshot_ref = audit.get("bootstrapEventSnapshot")
    require(isinstance(bootstrap_ref, dict) and bootstrap_ref.get("path") == config["bootstrapRecordPath"]
            and isinstance(bootstrap_ref.get("sha256"), str)
            and isinstance(authorization_ref, dict)
            and authorization_ref.get("path") == config["coreAuthorizationPath"]
            and isinstance(authorization_ref.get("sha256"), str)
            and isinstance(snapshot_ref, dict)
            and isinstance(snapshot_ref.get("path"), str)
            and isinstance(snapshot_ref.get("sha256"), str),
            "Fresh prompt-only bootstrap evidence references are missing")
    bootstrap = checked_json(bootstrap_ref, read)
    authorization = checked_json(authorization_ref, read)
    snapshot_raw = read(snapshot_ref["path"], snapshot_ref["sha256"])
    require(bootstrap["status"] == "PROMPT_ONLY_BOOTSTRAP_PASS"
            and bootstrap["run"] == run and bootstrap["sessionId"] == session
            and bootstrap["candidate"] == snapshot and bootstrap["configSha256"] == launch["auditConfig"]["sha256"]
            and bootstrap["eventSnapshotPath"] == snapshot_ref["path"]
            and bootstrap["eventSnapshotSha256"] == snapshot_ref["sha256"]
            and sha(snapshot_raw) == snapshot_ref["sha256"]
            and authorization["status"] == "CORE_RELEASE_AUTHORIZED"
            and authorization["run"] == run and authorization["sessionId"] == session
            and authorization["candidate"] == snapshot
            and authorization["configSha256"] == launch["auditConfig"]["sha256"]
            and authorization["bootstrapRecordSha256"] == bootstrap_ref["sha256"]
            and authorization["eventSnapshotPath"] == snapshot_ref["path"]
            and authorization["eventSnapshotSha256"] == snapshot_ref["sha256"],
            "Fresh prompt-only bootstrap/core-release evidence is not bound to the review")
    structure = final["structure"]
    require(structure["status"] == "PASS" and structure["overall"] == spec["verdict"],
            "Fresh report structure or raw verdict differs")
    require("coordinatorClaimIds" in adjudication, "Fresh coordinator claims must be explicit")
    claims = normalize_claims(adjudication, family)
    all_claims = disposition_ids(report_raw, claims)
    fields = ("run", "session", "eventsSha256", "eventsBytes", "status", "breaches",
              "bootstrapVerified", "actualResponseModels", "reviewerIdle", "recordIncomplete",
              "coreRead", "coreRequired", "extensionRead", "extensionRequired",
              "writes", "readbacks", "readbackVerified", "reportBinding", "fetches")
    summary = {field: audit[field] for field in fields}
    summary.update(originalAuditSha256=final["audit"]["sha256"], rawExecutionPayloadsRemainLocal=True,
                   originalReviewerConfirmation=False,
                   representation="Bounded derivative of fresh independent execution, not confirmation.")
    refs = {
        "acceptance": spec["acceptance"], "final": final_ref, "report": report,
        "adjudication": acceptance["adjudication"], "audit": final["audit"],
        "preflight": preflight_ref, "auditConfig": launch["auditConfig"],
        "bootstrap": bootstrap_ref, "coreAuthorization": authorization_ref,
        "bootstrapEventSnapshot": snapshot_ref,
    }
    derivatives = {
        "audit-summary": json_bytes(summary),
        "context": json_bytes({"status": "PASS", "eventsSha256": audit["eventsSha256"],
                              "originalAuditSha256": final["audit"]["sha256"],
                              "capacityTelemetry": telemetry}),
        "structure": json_bytes({"originalFinalSha256": final_ref["sha256"], "structure": structure}),
        "claims": json_bytes({"originalAdjudication": acceptance["adjudication"], **claims,
                             "allReportAndAdjudicationIds": all_claims,
                             "representation": "Identity-only inventory; raw report and adjudication unchanged."}),
    }
    return refs, derivatives, claims
