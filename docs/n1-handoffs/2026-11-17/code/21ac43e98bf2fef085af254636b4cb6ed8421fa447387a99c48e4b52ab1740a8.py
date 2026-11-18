"""Collect bounded B133 confirmations without granting source or teaching approval.

The separate confirmation controller must supply this schema and audit the actual
read chain. Until then this collector is preparation, not a completed review.
"""
import datetime
import json
import re

from b132_closure_records import SHA256, UUID, checked_json, same_ref
from b133_closure_records import MECHANICAL_STATUS, collect_initial_record
from common import json_bytes, require, sha
from b133_fresh_confirmation_v2 import REASON, fresh_origin


def checked_bytes(ref, read):
    require(isinstance(ref["sha256"], str) and SHA256.fullmatch(ref["sha256"]),
            "Expected an exact SHA-256 reference")
    raw = read(ref["path"], ref["sha256"])
    require(sha(raw) == ref["sha256"], "Reader returned bytes outside the frozen binding")
    if "bytes" in ref:
        require(type(ref["bytes"]) is int and len(raw) == ref["bytes"], "Reference byte count differs")
    return raw


def disposition_ids(report, claims):
    report_ids = re.findall(r"(?m)^### ([FO]\d+):", report.decode("utf-8"))
    require(len(report_ids) == len(set(report_ids)), "Duplicate original report identity")
    return list(dict.fromkeys([
        *report_ids, *claims["acceptedFindings"], *claims["openClaimIds"],
        *claims["coordinatorClaimIds"],
    ]))


def validate_confirmation(spec, acceptance, final, audit, context, structure, adjudication,
                          preflight, required):
    family, run, session, candidate = (spec[key] for key in ("family", "run", "session", "snapshot"))
    require(family in ("claude", "gpt") and spec["role"] == "confirmation"
            and spec["confirmation"] == "CONFIRMED" and UUID.fullmatch(session)
            and re.fullmatch(r"[0-9a-f]{40}", candidate)
            and re.fullmatch("N1-B133-" + family.upper() + r"-CONFIRM-[0-9]{3}", run),
            "Wrong confirmation identity")
    for record in (acceptance, final, preflight):
        require(record["run"] == run and record["session"] == session and record["candidate"] == candidate,
                "Confirmation snapshot/session differs")
    require(acceptance["batch"] == preflight["batch"] == 133
            and acceptance["reviewAccepted"] is True and acceptance["confirmation"] == "CONFIRMED"
            and final["status"] == MECHANICAL_STATUS and final["confirmation"] == "CONFIRMED",
            "Confirmation is not accepted")
    require(audit["session"] == session and audit["final"] is True
            and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and audit["bootstrapVerified"] is True
            and audit["reviewerIdle"] is True and audit["recordIncomplete"] is False
            and audit["breaches"] == [] and type(audit["unexpectedUserMessages"]) is int
            and audit["unexpectedUserMessages"] == audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"] is True
            and type(audit["chainRequired"]) is int and type(audit["chainRead"]) is int
            and audit["chainRequired"] > 0 and audit["chainRead"] == audit["chainRequired"]
            and len(audit["messages"]) == 1 and audit["messages"][0].strip() == "CONFIRMED",
            "Confirmation execution is incomplete/breached")
    models = audit["actualResponseModels"]
    require(isinstance(models, list) and models
            and all(isinstance(model, str) and model.startswith(family + "-") for model in models)
            and context["status"] == "PASS" and context["errors"] == [] and context["compactions"] == []
            and context["family"] == family and context["eventsSha256"] == audit["eventsSha256"],
            "Actual confirmation context differs")
    require(structure["status"] == "PASS" and structure["confirmation"] == "CONFIRMED"
            and type(structure["findings"]) is int and structure["findings"] == 0
            and structure["nonAccepting"] == [], "Confirmation structure is not accepting")
    checks, dispositions = adjudication["claimChecks"], adjudication["dispositions"]
    require(adjudication["run"] == run and adjudication["candidate"] == candidate
            and adjudication["claimsAdjudicated"] is True and adjudication["openClaimIds"] == []
            and adjudication["acceptedFindings"] == [] and adjudication["coordinatorClaimIds"] == []
            and isinstance(checks, list) and checks
            and all(isinstance(item, dict)
                    and all(isinstance(item.get(key), str) and item[key].strip()
                            for key in ("claim", "evidence", "disposition")) for item in checks)
            and isinstance(dispositions, dict) and set(dispositions) == set(required)
            and all(isinstance(value, str) and value.strip() for value in dispositions.values()),
            "Substantive confirmation adjudication is incomplete")


def collect_confirmation(spec, initial, read):
    """read(path, sha256) must require ReadOnly files; hashes are also checked here."""
    initial_spec = initial["spec"]
    initial_refs, _, claims = collect_initial_record(
        initial_spec, initial["preflight"], initial["final"], read)
    require(spec["family"] == initial_spec["family"]
            and spec["reviewerOrigin"] == "fresh-context-replacement"
            and spec["originalSession"] == initial_spec["session"] != spec["session"],
            "Fresh confirmation must disclose the original accepted reviewer")
    required = disposition_ids(checked_bytes(initial_refs["report"], read), claims)
    acceptance = checked_json(spec["acceptance"], read)
    final = checked_json(acceptance["final"], read)
    audit = checked_json(final["audit"], read)
    context = checked_json(final["context"], read)
    structure = checked_json(final["structure"], read)
    adjudication = checked_json(acceptance["adjudication"], read)
    preflight = checked_json(spec["preflight"], read)
    observation = checked_json(preflight["contextObservation"], read)
    require(fresh_origin({"family": spec["family"], "run": spec["run"], "session": spec["session"],
                          "candidate": spec["snapshot"], "originalSession": spec["originalSession"],
                          "contextObservation": preflight["contextObservation"]})
            and observation["originalSession"] == spec["originalSession"]
            and all(record["originalSession"] == spec["originalSession"]
                    and record["replacementReason"] == REASON for record in (preflight, final))
            and acceptance["reviewerOrigin"] == spec["reviewerOrigin"]
            and acceptance["originalSession"] == spec["originalSession"]
            and acceptance["replacementReason"] == REASON
            and acceptance["contextObservation"] == preflight["contextObservation"],
            "Fresh-context origin is not disclosed throughout")
    validate_confirmation(spec, acceptance, final, audit, context, structure, adjudication,
                          preflight, required)
    same_ref(preflight["initialAcceptance"], initial_refs["acceptance"], "Original acceptance")
    same_ref(preflight["initialReport"], initial_refs["report"], "Original report")
    same_ref(acceptance["report"], final["report"], "Confirmation report")
    require(adjudication["reportSha256"] == final["report"]["sha256"]
            and adjudication["finalSha256"] == acceptance["final"]["sha256"],
            "Unbound confirmation adjudication")
    checked_bytes(final["report"], read)
    config = checked_json(preflight["config"], read)
    require(config["run"] == spec["run"] and config["candidate"] == spec["snapshot"]
            and config["expectedFamily"] == spec["family"] and config["report"] == final["report"]["path"]
            and config["dispositionIds"] == required and config["maxWebFetches"] == 0
            and config["chainManifest"] == preflight["chain"]["path"]
            and config["kickoff"] == preflight["kickoff"]["path"],
            "Confirmation configuration differs")
    files = config["files"]
    require(isinstance(files, list) and files
            and len(files) == len({ref["path"] for ref in files}), "Duplicate or absent config inputs")
    pinned = {ref["path"]: ref["sha256"] for ref in files}
    for ref in (preflight["chain"], preflight["kickoff"], *initial_refs.values()):
        require(pinned.get(ref["path"]) == ref["sha256"], "Required input missing from config bindings")
    require(config["prompt"] in pinned, "Prompt is not pinned")
    for ref in files:
        checked_bytes(ref, read)
    chain = checked_json(preflight["chain"], read)
    require(preflight["segments"] == len(chain["segments"]) == audit["chainRequired"]
            and len({row["path"] for row in chain["segments"]}) == len(chain["segments"]),
            "Actual read coverage does not match the frozen chain")
    for row in chain["segments"]:
        checked_bytes(row, read)
    admission = checked_json(spec["admission"], read)
    require(admission["admitted"] is True and admission["session"] == spec["session"]
            and admission["candidate"] == spec["snapshot"] and admission["run"] == spec["run"]
            and audit["offset"] == admission["offset"] and audit["prefixSha256"] == admission["prefixSha256"],
            "Confirmation admission prefix differs")
    for field in ("config", "chain", "kickoff"):
        same_ref(admission[field], preflight[field], "Admitted " + field)
    require(spec["events"]["sha256"] == audit["eventsSha256"], "Event reference differs from audit")
    raw = checked_bytes(spec["events"], read)
    offset = admission["offset"]
    require(type(offset) is int and 0 <= offset < len(raw) and len(raw) == audit["eventsBytes"]
            and raw.endswith(b"\n") and (offset == 0 or raw[:offset].endswith(b"\n"))
            and sha(raw[:offset]) == admission["prefixSha256"],
            "Changed, truncated or non-boundary event prefix")
    require(checked_bytes(admission["prefix"], read) == raw[:offset], "Frozen admission prefix differs")
    require(sha(raw[offset:]) == audit["sliceSha256"]
            and len(raw[offset:]) == audit["sliceBytes"], "Audited event slice differs")
    events = [json.loads(line) for line in raw[offset:].decode("utf-8").splitlines()]
    messages = [row for row in events if row["type"] == "user.message"]
    require(len(messages) == 1, "Confirmation must have one kickoff")
    delivered = datetime.datetime.fromisoformat(messages[0]["timestamp"])
    observed = datetime.datetime.fromisoformat(admission["observedAt"])
    require(delivered.tzinfo is not None and observed.tzinfo is not None
            and 0 <= (delivered - observed).total_seconds() < 120,
            "Admission expired before actual delivery")
    fields = ("session", "eventsSha256", "eventsBytes", "status", "breaches", "bootstrapVerified",
              "actualResponseModels", "reviewerIdle", "recordIncomplete", "chainRead", "chainRequired",
              "writes", "readbacks", "readbackVerified", "reportBinding", "fetches", "offset", "prefixSha256")
    summary = {field: audit[field] for field in fields}
    summary.update(originalAuditSha256=final["audit"]["sha256"], rawExecutionPayloadsRemainLocal=True,
                   representation="Bounded derivative; original calls, messages and events remain local.")
    refs = {
        "report": final["report"], "final": acceptance["final"], "acceptance": spec["acceptance"],
        "adjudication": acceptance["adjudication"], "context": final["context"],
        "structure": final["structure"], "audit": final["audit"], "preflight": spec["preflight"],
        "auditConfig": preflight["config"], "initialAcceptance": initial_refs["acceptance"],
        "contextObservation": preflight["contextObservation"],
        "initialAdjudication": initial_refs["adjudication"],
    }
    return refs, {"audit-summary": json_bytes(summary)}, adjudication
