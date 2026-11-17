"""Represent two already-quarantined VOID initials without passing an accepted-audit assertion."""
import json
from pathlib import Path

from b130_context_confirmation import ROOT
from common import frozen, require, sha


def bounded_void_initial(path):
    path = Path(path)
    held_rows = [json.loads(frozen(ROOT / f"N1-B130-CLAUDE-00{n}-hold.json")) for n in (2, 3)]
    held = [row for row in held_rows if Path(row["audit"]["path"]) == path]
    require(len(held) == 1, "Only the two known quarantined VOID initials are supported")
    held = held[0]
    raw = frozen(path, held["audit"]["sha256"])
    audit = json.loads(raw)
    require(held["reviewAccepted"] is False and held["finalAcceptance"] is False
            and audit["status"] == "VOID" and audit["breaches"] and audit["reviewerIdle"]
            and not audit["recordIncomplete"] and audit["session"] == held["session"]
            and audit["eventsSha256"] == held["events"]["sha256"], "Excluded audit identity changed")
    fields = (
        "session", "eventsSha256", "eventsBytes", "eventsCount", "sliceSha256", "sliceBytes",
        "offset", "prefixSha256", "status", "breaches", "bootstrapVerified",
        "actualResponseModels", "reviewerIdle", "recordIncomplete", "unexpectedUserMessages",
        "coreRead", "coreRequired", "extensionRead", "extensionRequired",
        "writes", "readbacks", "readbackVerified", "reportBinding", "fetches",
    )
    result = {key: audit[key] for key in fields if key in audit}
    result.update(
        originalAuditSha256=sha(raw), rawExecutionPayloadsRemainLocal=True,
        reviewAccepted=False, finalAcceptance=False, excludedStatus=held["status"],
        rawCompletionMessageCount=len(audit["messages"]),
        rawCompletionMessageSha256=sha(json.dumps(audit["messages"], ensure_ascii=False).encode()),
        notesCount=len(audit["notes"]),
        notesSha256=sha(json.dumps(audit["notes"], ensure_ascii=False).encode()),
        callCount=len(audit["calls"]),
        rawCallsSha256=sha(json.dumps(audit["calls"], ensure_ascii=False, sort_keys=True).encode()),
        representation="Bounded derivative of the actual VOID audit; breaches and counts remain "
                       "unchanged. Calls, message payloads and full events remain local. "
                       "This helper cannot accept a review.",
    )
    return result


class ExcludedAuditSupport:
    def __init__(self, accepted_support):
        self.accepted_support = accepted_support

    def bounded_audit(self, path):
        raw = json.loads(frozen(path))
        if raw["status"] == "VOID":
            return bounded_void_initial(path)
        return self.accepted_support.bounded_audit(path)


def excluded_audit_support(accepted_support):
    return ExcludedAuditSupport(accepted_support)
