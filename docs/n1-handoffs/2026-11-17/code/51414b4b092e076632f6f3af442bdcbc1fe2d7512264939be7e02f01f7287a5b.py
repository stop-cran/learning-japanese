"""Bind B133 initial reviews and reconciled claims without granting teaching approval.

The initial controller embeds report structure and capacity telemetry in its
final/audit records. Raw event payloads remain local; bounded derivatives retain
their original hashes. Confirmation records require their own protocol.
"""
import json
import re

from b132_closure_records import SHA256, UUID, archive_path, checked_json
from common import json_bytes, require, sha
from record_b133_publication import validate_progress, validate_reviews
from run_b133_closure_checks import BASE, BATCH, CANDIDATE, MEMBERS

MECHANICAL_STATUS = "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"


def collect_initial_record(spec, preflight_ref, final_ref, read):
    family, run, session = (spec[name] for name in ("family", "run", "session"))
    require(family in ("claude", "gpt") and spec["role"] == "initial"
            and spec["snapshot"] == CANDIDATE and UUID.fullmatch(session)
            and re.fullmatch("N1-B133-" + family.upper() + r"-[0-9]{3}", run),
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


def validate_resolution(resolution, lineage, reviewed, inventory):
    require(resolution["batch"] == BATCH and resolution["initialSnapshot"] == CANDIDATE
            and resolution["reviewedSnapshot"] == reviewed
            and resolution["remainingActionableFindings"] == []
            and resolution["remainingConsequentialClaims"] == [],
            "Resolution has the wrong snapshot or outstanding work")
    expected = {entry["run"]: entry["adjudication"]["sha256"] for entry in lineage}
    require(len(expected) == len(lineage) and resolution["adjudicationSha256"] == expected,
            "Resolution does not bind every distinct accepted adjudication")
    require(isinstance(resolution["dispositions"], list), "Missing claim dispositions")
    ids = set()
    for item in resolution["dispositions"]:
        identity = (item["run"], item["id"])
        require(item["run"] in expected and isinstance(item["id"], str) and item["id"]
                and identity not in ids, "Invalid or duplicate claim disposition")
        require(item["status"] in ("fixed", "source-backed-no-change", "excluded-from-delivered-teaching")
                and isinstance(item["reason"], str) and item["reason"].strip()
                and isinstance(item["evidence"], list) and item["evidence"],
                "Unresolved or unsupported claim disposition")
        for ref in item["evidence"]:
            archive_path(ref["path"])
            require(SHA256.fullmatch(ref["sha256"]) and inventory.get(ref["path"]) == ref["sha256"],
                    "Disposition evidence is not bound to the closure inventory")
        ids.add(identity)
    required = {(entry["run"], claim) for entry in lineage if entry["role"] == "initial"
                for claim in [*entry["acceptedFindings"], *entry["openClaimIds"],
                              *entry["coordinatorClaimIds"]]}
    require(required <= ids, "An accepted finding or consequential claim lacks a disposition")


def closed_progress(original, closure_raw, manifest, resolution):
    closure = json.loads(closure_raw)
    reviewed = closure["reviewedSnapshot"]
    validate_reviews(closure, reviewed)
    validate_resolution(resolution, closure["reviewLineage"], reviewed, closure["recordedFileSha256"])
    initials = [entry for entry in closure["reviewLineage"] if entry["role"] == "initial"]
    if any(entry[field] for entry in initials
           for field in ("acceptedFindings", "openClaimIds", "coordinatorClaimIds")):
        by_run = {entry["run"]: entry for entry in closure["reviewLineage"]}
        require(all(by_run[run]["role"] == "confirmation" for run in closure["finalRuns"]),
                "Consequential initial claims require both original-reviewer confirmations")
    require(original["batch"] == BATCH and original["members"] == MEMBERS
            and original["base"] == BASE and original["sourceRows"] == [707, 1120, 643]
            and original["status"] == "local-unreviewed-author-candidate"
            and original["publishedDelivered"] == 268 and original["undelivered"] == 960
            and original["frozenTotal"] == 1228 and original["localUnpublishedDrafts"] == 3
            and original["deliveryNotIncremented"] is True, "Unexpected original B133 ledger")
    require(closure["limits"] and all(isinstance(item, str) and item for item in closure["limits"]),
            "Explicit review/acceptance limits are required")
    value = {
        "batch": BATCH, "base": BASE, "governingIssue": 60,
        "status": "textual-review-closed-publication-pending",
        "members": MEMBERS, "sourceRows": original["sourceRows"], "supports": original["supports"],
        "initialSnapshot": CANDIDATE, "reviewedSnapshot": reviewed,
        "reviewClosed": MEMBERS, "published": [], "runtimePublished": False,
        "manifestSha256": sha(manifest), "contentVersion": json.loads(manifest)["contentVersion"],
        "accounting": {
            "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 268,
            "publishedN1Additions": 262, "n2Placements": 6, "undelivered": 960,
            "reviewClosedPendingRecordsWithCards": 271, "localUnreviewedDrafts": 0,
            "notStarted": 957, "overallN1TaskComplete": False,
        },
        "review": {
            "status": "closed-with-disclosed-limits", "finalRuns": closure["finalRuns"],
            "closure": "../n1-reviews/batch-133-closure/provenance.json",
            "closureProvenanceSha256": sha(closure_raw), "historicalReportsPreserved": True,
            "remainingActionableFindings": [], "remainingConsequentialClaims": [],
        },
        "originalAuthorProgress": "../n1-reviews/batch-133-closure/verification/original-progress.json",
        "originalAuthorWarnings": original["warnings"],
        "publicationGates": ["Owner-signed publication", "CI", "Exact served ZIP/runtime equality"],
        "limits": closure["limits"],
    }
    validate_progress(value, reviewed, manifest, closure_raw)
    return value
