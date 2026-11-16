"""Prepare closure inputs only from both actual accepted successor confirmations."""
import ast
import json
import sys
from pathlib import Path

from b130_context_confirmation import ROOT, binding
from b130_delta_closure_support import (
    FINALS, FOLLOWUP_TOOLS, HISTORICAL, LOCAL_ONLY_EXECUTIONS, additional_history, ledger_acceptance,
)
from b130_fresh_archive import NEW_TOOLS
from common import TOOLS, freeze_json, frozen, load_batch, require, sha
from confirm_b130_fresh_context import clean, preflight
from finalize_b130 import execution_files
from finalize_b130_followup_v3 import check_proofs, read_binding
from verify_b130_delta_evidence import CANDIDATE

EXECUTIONS = {
    "delta-evidence-verification-execution-001": 0,
    "followup-ready-tests-001": 0, "followup-ready-preparation-execution-001": 0,
    "followup003-preparation-execution-001": 0, "followup003-capacity-execution-001": 0,
    "gpt003-admission-execution-001": 0,
    "claude004-selection-tests-001": 0, "claude004-preparation-execution-001": 1,
    "claude004-preparation-repair-execution-001": 0, "claude004-preparation-execution-002": 0,
    "gpt003-final-execution-001": 1, "gpt003-control-binding-001": 0,
    "gpt003-control-tests-001": 0, "gpt003-control-adjudication-execution-001": 0,
    "claude004-admission-execution-001": 0, "claude004-final-execution-001": 1,
    "claude004-control-preparation-execution-001": 1, "claude004-control-preparation-execution-002": 0,
    "claude004-control-tests-001": 0, "claude004-control-adjudication-execution-001": 0,
    "delta-confirmation-acceptance-execution-001": 0,
    "delta-closure-tooling-execution-001": 0, "delta-closure-history-tests-001": 1,
    "delta-closure-test-fix-execution-001": 0, "delta-closure-history-tests-002": 0,
    "delta-closure-inputs-execution-001": 1, "delta-closure-inputs-execution-002": 0, "delta-closure-archive-execution-001": 0,
    "delta-closure-archive-verification-execution-001": 0,
}
TOOLING = (
    "delta-runtime-tooling-001.json", "delta-gate-tooling-001.json",
    "followup-ready-tooling-001.json", "confirmation-003-preparation.json",
    "followup003-capacity-observation-001.json", "claude004-preparation-repair-001.json",
    "claude004-preparation.json", "claude004-control-tooling-001.json",
    "delta-confirmation-acceptances-001.json", "delta-closure-tooling-001.json",
    "delta-closure-test-fix-001.json", "delta-closure-spec-001.json",
    "delta-closure-inputs-repair-001.json",
)


def accepted_finals():
    finals = []
    for family, run in FINALS.items():
        accepted = json.loads(frozen(ROOT / "confirm" / f"{run}-acceptance.json"))
        record, _ = preflight(ROOT / "confirm" / f"{run}-preflight.json")
        require(accepted["candidate"] == CANDIDATE and accepted["confirmationAccepted"] is True
                and accepted["verdict"] == "CONFIRMED" and accepted["openClaimIds"] == [],
                "Actual current-snapshot confirmation required")
        finals.append(ledger_acceptance(accepted, record))
    additional_history(finals)
    return finals


def retained_tools():
    tree = ast.parse(frozen(TOOLS / "close_b130_followup_v2.py"))
    loops = [node for node in ast.walk(tree) if isinstance(node, ast.For)
             and isinstance(node.iter, ast.Tuple)
             and any(isinstance(item, ast.Starred) and isinstance(item.value, ast.Name)
                     and item.value.id == "additional_tools" for item in node.iter.elts)]
    require(len(loops) == 1, "Archive tool inventory anchor differs")
    existing = {node.value for node in loops[0].iter.elts if isinstance(node, ast.Constant)}
    existing.update(NEW_TOOLS)
    existing.update(FOLLOWUP_TOOLS)
    extra = sorted(path.name for path in TOOLS.glob("*b130*.py") if path.name not in existing)
    for name in extra:
        frozen(TOOLS / name)
    return extra


def proofs():
    evidence = binding(ROOT / "delta-evidence-001" / "verification.json")
    require(evidence["sha256"] == "0288e16198420c4e8b8b14a109ce6af2ac7cf4b8572468639b923aa59affa5a9",
            "Actual independent proof differs")
    _, proof = read_binding(evidence)
    _, runtime = read_binding(proof["proofs"]["runtime"])
    _, sources = read_binding(proof["proofs"]["sourceReuse"])
    check_proofs(CANDIDATE, proof, runtime, sources,
                 proof["proofs"]["runtime"], proof["proofs"]["sourceReuse"])
    return {"evidenceProof": evidence, "runtimeProof": proof["proofs"]["runtime"],
            "sourceReuseProof": proof["proofs"]["sourceReuse"]}


def prepare_closure():
    finals = accepted_finals()
    proof_bindings = proofs()
    clean(load_batch(130), CANDIDATE)
    tools = retained_tools()
    execution_files(ROOT / "delta-closure-history-tests-002", 0)
    test_dir = ROOT / "protocol-tests-002"
    captured = execution_files(test_dir, 0)
    readiness = freeze_json(ROOT / "protocol-tooling-readiness-001.json", {
        "batch": 130, "phase": "closure-time-retrospective-binding-not-prelaunch",
        "execution": str(test_dir), "files": {name: sha(raw) for name, raw in captured.items()},
        "scope": "Created now from preserved original successful protocol tests, not retroactive "
                 "prelaunch readiness or admission. The old75-test receipt/log were initially writable "
                 "at closure preparation. Their current exit/log hash/cleanup/RAM and "
                 "75-test output were checked, then those bytes were frozen now; "
                 "no historical read-only state is asserted. Successor history tests "
                 "are separately bound.",
    })
    print(json.dumps(freeze_json(ROOT / "delta-closure-spec-001.json", {
        "batch": 130, "candidate": CANDIDATE, "finalRuns": [row["run"] for row in finals],
        "intermediateRuns": list(HISTORICAL.values()),
        "preflight": str(ROOT / "prompts" / "preflight-compact-004.json"),
        "excludedInitials": [str(ROOT / f"N1-B130-CLAUDE-00{n}-hold.json") for n in (1, 2, 3)],
        "confirmationProtocol": [], "additionalTools": tools, "readiness": readiness,
        **proof_bindings, "producer": binding(__file__),
    })))


def prepare_finalizer():
    accepted_finals()
    proof_bindings = proofs()
    require(not set(EXECUTIONS) & LOCAL_ONLY_EXECUTIONS, "Raw execution payload requested for publication")
    retained = {}
    for name, code in {**EXECUTIONS, **{name: 0 for name in LOCAL_ONLY_EXECUTIONS}}.items():
        files = execution_files(ROOT / name, code)
        retained[name] = {"exitCode": code, "files": {key: sha(raw) for key, raw in files.items()},
                          "rawPayloadLocalOnly": name in LOCAL_ONLY_EXECUTIONS}
    retention = freeze_json(ROOT / "delta-closure-execution-retention-001.json", {
        "batch": 130, "records": retained,
        "limits": "Raw event/usage-tail observation logs remain local. Their hashes/receipts are "
                  "retained, not copied into published execution logs. Failed preparation and raw "
                  "final-audit exits remain failures, distinct from later successful adjudication.",
    })
    tooling = {name: binding(ROOT / name) for name in TOOLING}
    tooling["delta-closure-execution-retention-001.json"] = {
        "path": retention["path"], "sha256": retention["sha256"]}
    for run in FINALS.values():
        name = f"{run}-citation-check.json"
        tooling[name] = binding(ROOT / "confirm" / name)
    print(json.dumps(freeze_json(ROOT / "delta-closure-finalizer-spec-001.json", {
        "batch": 130, "candidate": CANDIDATE,
        "parent": "d440617274eef6ea7611e60f147d6483f29ca710",
        **proof_bindings, "archiveVerification": binding(ROOT / "delta-closure-archive-verification-001.json"),
        "tooling": tooling, "executions": EXECUTIONS,
        "localOnlyExecutions": sorted(LOCAL_ONLY_EXECUTIONS),
        "preservedFailures": "Family-named neutral presentation; CRLF-sensitive test insertion; "
                             "initial-session test-fixture mismatch; original runtime-reminder "
                             "HOLD audits. No historical input or failed receipt was rewritten.",
        "producer": binding(__file__),
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 2 and sys.argv[1] in ("closure", "finalizer"),
            "Usage: prepare_b130_delta_closure_inputs.py closure|finalizer")
    (prepare_closure if sys.argv[1] == "closure" else prepare_finalizer)()
