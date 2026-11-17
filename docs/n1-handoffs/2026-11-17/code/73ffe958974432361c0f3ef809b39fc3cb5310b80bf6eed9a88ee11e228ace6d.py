"""Prepare exclusive closure specs from actual accepted evidence, never assumed verdicts."""
import ast
import json
import sys
from pathlib import Path

from b130_context_confirmation import binding
from b130_fresh_archive import NEW_TOOLS
from b130_fresh_closure_history import confirmation_origins
from common import TOOLS, freeze_json, frozen, require, sha
from finalize_b130 import CANDIDATE, ROOT, execution_files

EXECUTIONS = {
    "fresh-archive-tests-001": 0, "fresh-archive-preparation-execution-001": 0,
    "fresh-finalizer-tests-001": 1, "fresh-finalizer-tests-002": 0,
    "fresh-claude-final-execution-002": 0, "fresh-claude-adjudication-execution-002": 1,
    "fresh-claude-adjudication-execution-003": 0,
    "fresh-gpt-final-execution-002": 0, "fresh-gpt-adjudication-execution-002": 0,
    "fresh-closure-archive-execution-001": 0, "fresh-closure-archive-verification-execution-001": 0,
}
TOOLING = (
    "confirmation-capacity-observation-001.json", "fresh-confirmation-tooling-001.json",
    "fresh-confirmation-admission-tooling-001.json", "fresh-closure-ledger-preparation-001.json",
    "fresh-archive-tooling-001.json", "closure-spec-001.json",
    "revision-runtime-tooling-001.json",
)


def accepted_finals():
    finals = []
    for family in ("claude", "gpt"):
        run = f"N1-B130-{family.upper()}-CONFIRM-002"
        row = json.loads(frozen(ROOT / "confirm" / f"{run}-acceptance.json"))
        require(row["run"] == run and row["family"] == family
                and row["candidate"] == CANDIDATE and row["verdict"] == "CONFIRMED"
                and row["confirmationAccepted"] is True and row["openClaimIds"] == [],
                "Two actual accepted confirmations required before closure preparation")
        for key in ("report", "final", "adjudication"):
            frozen(row[key]["path"], row[key]["sha256"])
        finals.append(row)
    confirmation_origins(finals, CANDIDATE)
    return finals


def retained_tools():
    tree = ast.parse(frozen(TOOLS / "close_b130_fresh.py"))
    loops = [node for node in ast.walk(tree) if isinstance(node, ast.For)
             and isinstance(node.iter, ast.Tuple)
             and any(isinstance(item, ast.Starred) and isinstance(item.value, ast.Name)
                     and item.value.id == "additional_tools" for item in node.iter.elts)]
    require(len(loops) == 1, "Archive tool inventory anchor differs")
    existing = {node.value for node in loops[0].iter.elts if isinstance(node, ast.Constant)}
    existing.update(NEW_TOOLS)
    extra = sorted(path.name for path in TOOLS.glob("*b130*.py") if path.name not in existing)
    for name in extra:
        frozen(TOOLS / name)
    return extra


def prepare_closure():
    finals = accepted_finals()
    readiness = ROOT / "protocol-tooling-readiness-001.json"
    require(not readiness.exists(), "Preserve existing readiness metadata")
    test_dir = ROOT / "protocol-tests-002"
    captured = execution_files(test_dir, 0)
    freeze_json(readiness, {
        "batch": 130, "phase": "closure-time-retrospective-binding-not-prelaunch",
        "execution": str(test_dir),
        "files": {name: sha(raw) for name, raw in captured.items()},
        "scope": "Created at closure preparation from preserved successful original protocol tests. "
                 "This file did not exist before review launch and is not retroactive admission.",
    })
    result = freeze_json(ROOT / "closure-spec-001.json", {
        "batch": 130, "candidate": CANDIDATE, "finalRuns": [row["run"] for row in finals],
        "intermediateRuns": [], "preflight": str(ROOT / "prompts" / "preflight-compact-004.json"),
        "excludedInitials": [str(ROOT / f"N1-B130-CLAUDE-00{n}-hold.json") for n in (1, 2, 3)],
        "confirmationProtocol": [], "additionalTools": retained_tools(),
    })
    print(json.dumps(result))


def prepare_finalizer():
    accepted_finals()
    for name, code in EXECUTIONS.items():
        execution_files(ROOT / name, code)
    tooling = {name: binding(ROOT / name) for name in TOOLING}
    for family in ("CLAUDE", "GPT"):
        name = f"N1-B130-{family}-CONFIRM-002-citation-check.json"
        tooling[name] = binding(ROOT / "confirm" / name)
    result = freeze_json(ROOT / "closure-finalizer-spec-001.json", {
        "batch": 130, "candidate": CANDIDATE,
        "archiveVerification": binding(ROOT / "closure-archive-verification-001.json"),
        "tooling": tooling, "executions": EXECUTIONS,
        "preservedFailures": {
            "fresh-finalizer-tests-001": "Required retained failed-Claude receipt was writable. "
                "Verified its recorded log hash/exit/cleanup/RAM, then froze unchanged bytes now; "
                "unchanged finalizer and tests passed in002. No historical immutability claimed.",
            "fresh-claude-adjudication-execution-002": "Raw versus unique citation-count error; "
                "explicit predecessor and successful successor preserved separately.",
        },
    })
    print(json.dumps(result))


if __name__ == "__main__":
    require(len(sys.argv) == 2 and sys.argv[1] in ("closure", "finalizer"),
            "Usage: prepare_b130_closure_inputs.py closure|finalizer")
    (prepare_closure if sys.argv[1] == "closure" else prepare_finalizer)()
