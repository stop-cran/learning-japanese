"""Verify mixed final identities, unused preparation and exact control-tail adjudications."""
import json
from pathlib import Path

from b130_context_confirmation import ROOT, binding
from b130_followup_lineage_v2 import require_followup_identity
from common import frozen, require
from prepare_b130_claude004 import require_unused_claude003
from prepare_b130_followup_closure import FOLLOWUP_TOOLS, archive_origins
from b130_fresh_archive import require_origin
from b130_followup_closure_history import HISTORICAL, PREVIOUS

FINALS = {"claude": "N1-B130-CLAUDE-CONFIRM-004", "gpt": "N1-B130-GPT-CONFIRM-003"}
ACCEPTANCE_SHA = {
    "claude": "2c9081afbdf499aa6ed8695a452910e886ae128a464fd4713dadca4b9cbee4b4",
    "gpt": "b36f812d74f543c2136715d637cbf31f486cc4e64d7fc52d11fb5e39ad358cc9",
}
LOCAL_ONLY_EXECUTIONS = {
    "followup003-capacity-comparison-001",
    "gpt003-tail-observation-001",
    "claude004-tail-observation-001",
}


def read(item):
    return json.loads(frozen(item["path"], item["sha256"]))


def ledger_acceptance(accepted, preflight):
    family = accepted["family"]
    require(family in FINALS and preflight["batch"] == 130
            and all(accepted[key] == preflight[key] for key in ("run", "candidate", "session"))
            and accepted["run"] == FINALS[family] and preflight["priorRun"] == HISTORICAL[family]
            and accepted["batch"] == 130, "Mixed-final acceptance identity differs")
    expected = json.loads(frozen(ROOT / "confirm" / f"{FINALS[family]}-acceptance.json",
                                 ACCEPTANCE_SHA[family]))
    require(accepted == expected, "Acceptance differs from the actually adjudicated review")
    return dict(accepted)


def additional_history(finals):
    require(len(finals) == 2 and {row["family"] for row in finals} == set(FINALS),
            "Two actual families required")
    unused = require_unused_claude003()
    unused_chain = json.loads(frozen(ROOT / "confirm" / f"{unused['run']}-chain.json"))
    for segment in unused_chain["segments"]:
        frozen(segment["path"], segment["sha256"])
    preparations = [{**unused, "chainRetainedLocally": True,
                     "segments": len(unused_chain["segments"]),
                     "chainBytes": sum(row["bytes"] for row in unused_chain["segments"])}]
    controls = []
    for family in FINALS:
        accepted = next(row for row in finals if row["family"] == family)
        expected = json.loads(frozen(ROOT / "confirm" / f"{FINALS[family]}-acceptance.json",
                                     ACCEPTANCE_SHA[family]))
        require(accepted == expected, "Unadjudicated final supplied")
        final = read(accepted["final"])
        audit, raw, certificate = (read(final[key]) for key in
                                    ("audit", "rawAudit", "controlAdjudication"))
        require(final["rawAudit"] == accepted["rawAudit"] == audit["rawAudit"]
                and final["controlAdjudication"] == accepted["controlAdjudication"]
                == audit["controlAdjudication"]
                and certificate["rawAudit"] == final["rawAudit"]
                and raw["status"] == "HOLD" and raw["unexpectedUserMessages"] == 1
                and not raw["breaches"] and raw["reviewerIdle"] and not raw["recordIncomplete"]
                and raw["eventsSha256"] == audit["eventsSha256"] == certificate["events"]["sha256"]
                and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
                and not audit["unexpectedUserMessages"] and not audit["breaches"]
                and certificate["rawUnexpectedUserMessages"]
                == certificate["classifiedRuntimeCompletionReminders"] == 1,
                "Original control hold or exact adjudication was hidden")
        frozen(certificate["events"]["path"], certificate["events"]["sha256"])
        controls.append({
            "run": accepted["run"], "rawAudit": final["rawAudit"],
            "adjudicatedAudit": final["audit"], "certificate": final["controlAdjudication"],
            "rawStatus": "HOLD", "rawUnexpectedUserMessages": 1,
            "classifiedRuntimeCompletionReminders": 1,
            "eventSha256": certificate["eventSha256"], "eventsSha256": raw["eventsSha256"],
            "rawExecutionPayloadsRemainLocal": True,
        })
    return preparations, controls


def check_additional_history(provenance, finals):
    prepared, controls = additional_history(finals)
    require(provenance["preparedOnlyFollowups"] == prepared
            and provenance["runtimeControlAdjudications"] == controls,
            "Unused follow-up or exact control-history record was changed")


def retain_additional_history(finals, copy, dump, audit_support):
    prepared, controls = additional_history(finals)
    for row in prepared:
        for item in row["files"]:
            copy(Path(item["path"]), f"prepared-only/{row['run']}/{Path(item['path']).name}",
                 item["sha256"])
    for row in controls:
        prefix = f"runs/{row['run']}"
        summary = audit_support.bounded_audit(Path(row["rawAudit"]["path"]))
        summary["unexpectedUserMessages"] = row["rawUnexpectedUserMessages"]
        dump(f"{prefix}/original-control-hold-audit-summary.json", summary)
        copy(Path(row["certificate"]["path"]), f"{prefix}/control-adjudication.json",
             row["certificate"]["sha256"])
    return prepared, controls


def require_archive_origin(spec, mechanics, launch, accepted, family, candidate, origins):
    if spec["run"] == HISTORICAL[family]:
        require_origin(spec, mechanics, launch, accepted, family, PREVIOUS, origins)
        return
    initial = read(spec["acceptance"])
    require_followup_identity(spec, initial, launch, ROOT)
    require(spec["run"] == mechanics["run"] == accepted["run"] == FINALS[family]
            and spec["session"] == mechanics["session"] == accepted["session"] == origins[family]["session"]
            and spec["candidate"] == mechanics["candidate"] == accepted["candidate"] == candidate,
            "Mixed final attribution differs")
