"""Validate the actual B132 confirmation schema and return bounded archive derivatives."""
import datetime
import json

from common import json_bytes, require, sha


def validate_confirmation(spec, acceptance, final, audit, context, structure, adjudication, preflight):
    family, run, session, candidate = (spec[key] for key in ("family", "run", "session", "snapshot"))
    require(family in ("claude", "gpt") and spec["role"] == "confirmation"
            and spec["confirmation"] == "CONFIRMED"
            and run == "N1-B132-" + family.upper() + "-CONFIRM-002", "Wrong confirmation identity")
    for record in (acceptance, final, preflight):
        require(record["run"] == run and record["session"] == session and record["candidate"] == candidate,
                "Confirmation snapshot/session differs")
    require(acceptance["reviewAccepted"] is True and acceptance["confirmation"] == "CONFIRMED"
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and final["confirmation"] == "CONFIRMED", "Confirmation is not accepted")
    require(audit["session"] == session and audit["final"] is True
            and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and audit["bootstrapVerified"] is True
            and audit["reviewerIdle"] is True and audit["recordIncomplete"] is False
            and audit["breaches"] == [] and type(audit["unexpectedUserMessages"]) is int
            and audit["unexpectedUserMessages"] == audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"] is True
            and audit["chainRequired"] > 0 and audit["chainRead"] == audit["chainRequired"]
            and len(audit["messages"]) == 1 and audit["messages"][0].strip() == "CONFIRMED",
            "Confirmation execution is incomplete/breached")
    require(audit["actualResponseModels"]
            and all(model.startswith(family + "-") for model in audit["actualResponseModels"])
            and context["status"] == "PASS" and context["errors"] == [] and context["compactions"] == []
            and context["family"] == family and context["eventsSha256"] == audit["eventsSha256"],
            "Actual confirmation context differs")
    require(structure["status"] == "PASS" and structure["confirmation"] == "CONFIRMED"
            and structure["findings"] == 0 and not structure["nonAccepting"],
            "Confirmation structure is not accepting")
    require(adjudication["run"] == run and adjudication["candidate"] == candidate
            and adjudication["claimsAdjudicated"] is True and adjudication["openClaimIds"] == []
            and adjudication["acceptedFindings"] == [] and adjudication["claimChecks"]
            and set(adjudication["dispositions"]) == ({"O1", "O2"} if family == "claude" else {"Q1", "Q2"}),
            "Substantive confirmation adjudication is incomplete")


def collect_confirmation(spec, read):
    def checked(ref):
        return json.loads(read(ref["path"], ref["sha256"]))

    acceptance = checked(spec["acceptance"])
    final = checked(acceptance["final"])
    audit = checked(final["audit"])
    context = checked(final["context"])
    structure = checked(final["structure"])
    adjudication = checked(acceptance["adjudication"])
    preflight = checked(spec["preflight"])
    validate_confirmation(spec, acceptance, final, audit, context, structure, adjudication, preflight)
    require(acceptance["report"] == final["report"]
            and adjudication["reportSha256"] == final["report"]["sha256"]
            and adjudication["finalSha256"] == acceptance["final"]["sha256"], "Unbound confirmation report")
    read(final["report"]["path"], final["report"]["sha256"])
    admission = checked(spec["admission"])
    require(admission["admitted"] is True and admission["session"] == spec["session"]
            and admission["candidate"] == spec["snapshot"] and admission["run"] == spec["run"]
            and audit["offset"] == admission["offset"] and audit["prefixSha256"] == admission["prefixSha256"],
            "Confirmation admission prefix differs")
    raw = read(spec["events"]["path"], audit["eventsSha256"])
    require(sha(raw[:admission["offset"]]) == admission["prefixSha256"], "Changed prefix")
    events = [json.loads(line) for line in raw[admission["offset"]:].decode("utf-8").splitlines()]
    messages = [row for row in events if row["type"] == "user.message"]
    require(len(messages) == 1, "Confirmation must have one kickoff")
    delivered = datetime.datetime.fromisoformat(messages[0]["timestamp"])
    observed = datetime.datetime.fromisoformat(admission["observedAt"])
    require(0 <= (delivered - observed).total_seconds() < 120, "Admission expired before actual delivery")
    fields = ("session", "eventsSha256", "eventsBytes", "status", "breaches", "bootstrapVerified",
              "actualResponseModels", "reviewerIdle", "recordIncomplete", "chainRead", "chainRequired",
              "writes", "readbacks", "readbackVerified", "reportBinding", "fetches", "offset", "prefixSha256")
    summary = {field: audit[field] for field in fields}
    summary.update(originalAuditSha256=final["audit"]["sha256"],
                   representation="Bounded derivative; original calls, messages and events remain local.")
    refs = {
        "report": final["report"], "final": acceptance["final"], "acceptance": spec["acceptance"],
        "adjudication": acceptance["adjudication"], "context": final["context"],
        "structure": final["structure"], "audit": final["audit"], "preflight": spec["preflight"],
    }
    return refs, {"audit-summary": json_bytes(summary)}, adjudication
