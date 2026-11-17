"""Bind the actual archive retry and all preparation failures for finalization."""
import json

from b130_context_confirmation import ROOT, binding
from b130_delta_closure_support import FINALS, LOCAL_ONLY_EXECUTIONS
from common import TOOLS, freeze_json, require, sha
from finalize_b130 import execution_files
from prepare_b130_delta_closure_inputs_retry import (
    EXECUTIONS as PREVIOUS_EXECUTIONS, TOOLING as PREVIOUS_TOOLING, accepted_finals, proofs,
)
from verify_b130_delta_evidence import CANDIDATE


EXECUTIONS = {
    **PREVIOUS_EXECUTIONS,
    "delta-closure-archive-execution-001": 1,
    "delta-closure-void-tests-001": 0,
    "delta-closure-void-preparation-001": 0,
    "delta-closure-archive-execution-002": 0,
}
TOOLING = (*PREVIOUS_TOOLING, "delta-closure-spec-002.json", "delta-closure-void-retry-001.json")


def main():
    accepted_finals()
    proof_bindings = proofs()
    require(not set(EXECUTIONS) & LOCAL_ONLY_EXECUTIONS, "Raw execution payload requested for publication")
    retained = {}
    for name, code in {**EXECUTIONS, **{name: 0 for name in LOCAL_ONLY_EXECUTIONS}}.items():
        files = execution_files(ROOT / name, code)
        retained[name] = {
            "exitCode": code, "files": {key: sha(raw) for key, raw in files.items()},
            "rawPayloadLocalOnly": name in LOCAL_ONLY_EXECUTIONS,
        }
    retention = freeze_json(ROOT / "delta-closure-execution-retention-001.json", {
        "batch": 130, "records": retained,
        "limits": "Raw event/usage-tail observation logs remain local. Their hashes/receipts are "
                  "retained, not copied into published execution logs. All failed preparation, "
                  "archive and raw final-audit exits remain failures. Successful input preparation "
                  "and archive are both attempt002; no attempt001 is relabelled.",
    })
    tooling = {name: binding(ROOT / name) for name in TOOLING}
    tooling["delta-closure-execution-retention-001.json"] = {
        "path": retention["path"], "sha256": retention["sha256"],
    }
    tooling["prepare_b130_delta_finalizer_inputs.py"] = binding(TOOLS / "prepare_b130_delta_finalizer_inputs.py")
    for run in FINALS.values():
        name = f"{run}-citation-check.json"
        tooling[name] = binding(ROOT / "confirm" / name)
    print(json.dumps(freeze_json(ROOT / "delta-closure-finalizer-spec-001.json", {
        "batch": 130, "candidate": CANDIDATE,
        "parent": "d440617274eef6ea7611e60f147d6483f29ca710",
        **proof_bindings,
        "closureSpec": binding(ROOT / "delta-closure-spec-002.json"),
        "archiveVerification": binding(ROOT / "delta-closure-archive-verification-001.json"),
        "tooling": tooling, "executions": EXECUTIONS,
        "localOnlyExecutions": sorted(LOCAL_ONLY_EXECUTIONS),
        "preservedFailures": "Family-named neutral presentation; CRLF-sensitive test insertion; "
                             "initial-session test-fixture mismatch; writable historical protocol "
                             "receipt; accepted-only audit presenter rejecting excluded VOID initials; "
                             "original runtime-reminder HOLD audits. No historical input or failed "
                             "receipt was rewritten. Protocol receipt bytes were frozen only at closure.",
        "producer": binding(__file__),
    })))


if __name__ == "__main__":
    main()
