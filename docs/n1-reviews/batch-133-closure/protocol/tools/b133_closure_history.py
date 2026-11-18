"""Archive bounded B133 held-review evidence without promoting it to acceptance."""
import json
from pathlib import Path

from close_b133 import keep_confirmation_chain, put
from common import frozen, json_bytes, require, sha
from confirm_b133_v2 import OUT, preflight


def unaccepted_entry(files, run, adjudication_path, adjudication_sha):
    final_path = OUT / (run + "-final.json")
    final_raw = frozen(final_path)
    final = json.loads(final_raw)
    record, config, chain = preflight(OUT / (run + "-preflight.json"))
    adjudication_raw = frozen(adjudication_path, adjudication_sha)
    adjudication = json.loads(adjudication_raw)
    require(final["run"] == record["run"] == adjudication["run"] == run
            and final["candidate"] == record["candidate"] == adjudication["candidate"]
            and final["confirmation"] == adjudication["confirmation"] == "UNVERIFIED"
            and adjudication["finalSha256"] == sha(final_raw)
            and adjudication["reportSha256"] == final["report"]["sha256"],
            "Held review binding differs")
    audit = json.loads(frozen(final["audit"]["path"], final["audit"]["sha256"]))
    context = json.loads(frozen(final["context"]["path"], final["context"]["sha256"]))
    structure = json.loads(frozen(final["structure"]["path"], final["structure"]["sha256"]))
    require(audit["session"] == final["session"] == record["session"]
            and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and audit["final"] is True
            and audit["reviewerIdle"] is True and audit["recordIncomplete"] is False
            and audit["bootstrapVerified"] is True and audit["breaches"] == []
            and audit["unexpectedUserMessages"] == audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"] is True
            and audit["chainRead"] == audit["chainRequired"] == len(chain["segments"])
            and [value.strip() for value in audit["messages"]] == ["UNVERIFIED"]
            and context["status"] == structure["status"] == "PASS"
            and context["errors"] == context["compactions"] == []
            and structure["confirmation"] == "UNVERIFIED", "Held execution is incomplete")
    events_path = Path(final["audit"]["path"]).parent / "events.jsonl"
    events = frozen(events_path, audit["eventsSha256"])
    require(len(events) == audit["eventsBytes"] and events.endswith(b"\n")
            and sha(events[:audit["offset"]]) == audit["prefixSha256"]
            and sha(events[audit["offset"]:]) == audit["sliceSha256"]
            and context["eventsSha256"] == audit["eventsSha256"], "Held events differ")
    prefix = "reviews/" + run + "/"
    entry = {
        "run": run, "role": "unaccepted-confirmation", "session": final["session"],
        "snapshot": final["candidate"], "confirmation": "UNVERIFIED", "reviewAccepted": False,
    }
    for field in ("report", "context", "structure"):
        ref = final[field]
        entry[field] = put(files, prefix + field + (".md" if field == "report" else ".json"),
                           frozen(ref["path"], ref["sha256"]))
    entry["final"] = put(files, prefix + "final.json", final_raw)
    fields = ("session", "eventsSha256", "eventsBytes", "status", "breaches",
              "actualResponseModels", "reviewerIdle", "recordIncomplete",
              "chainRead", "chainRequired", "writes", "readbacks", "readbackVerified", "fetches")
    summary = {key: audit[key] for key in fields}
    summary.update(originalAuditSha256=final["audit"]["sha256"], rawExecutionPayloadsRemainLocal=True)
    entry["audit-summary"] = put(files, prefix + "audit-summary.json", json_bytes(summary))
    correction = (
        "The original GPT confirmation held the missing direct liquid precaution. It was added in "
        "reconciliation-002. The waterfall-water interpretation used by that coordinator adjudication "
        "was subsequently withdrawn: the specified historical compound reading names an Edo sake."
        if "GPT" in run else
        "The fresh Claude confirmation held the unresolved compound gloss. Source adjudication required "
        "a sake-name correction and direct alcohol/sake precaution, delivered in reconciliation-003. "
        "The adjudication's L8 line-offset assertion was itself mistaken: existing liquid-source "
        "pointers 12 and 17 were correct. No pointer edit or teaching credit follows that correction."
    )
    derivative = {
        "run": run, "candidate": final["candidate"], "confirmation": "UNVERIFIED",
        "status": "EVIDENCE_ONLY_NOT_ACCEPTED_AS_CONFIRMATION",
        "originalAdjudicationSha256": adjudication_sha,
        "finalSha256": sha(final_raw), "reportSha256": final["report"]["sha256"],
        "dispositionSummary": correction,
        "representation": "Bounded coordinator derivative; complete original adjudication with external "
                          "source quotations remains immutable locally. This is not an accepting verdict.",
    }
    entry["adjudication"] = put(files, prefix + "adjudication-summary.json", json_bytes(derivative))
    entry["adjudication"]["originalSha256"] = adjudication_sha
    local = [
        {"path": str(adjudication_path), "sha256": adjudication_sha}, final["audit"],
        {"path": str(events_path), "sha256": audit["eventsSha256"]},
    ]
    for suffix in ("spec", "admission"):
        path = OUT / (run + "-" + suffix + ".json")
        local.append({"path": str(path), "sha256": sha(frozen(path))})
    for key in ("prompt", "kickoff"):
        put(files, prefix + key + ".txt", frozen(config[key]))
    put(files, prefix + "config.json", frozen(record["config"]["path"], record["config"]["sha256"]))
    retained = keep_confirmation_chain(files, run, config["chainManifest"])
    return entry, local, retained
