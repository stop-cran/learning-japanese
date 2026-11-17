"""Build both complete merged dossiers; never create/contact a reviewer."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import freeze_json, frozen, load_module, require, start_guard


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    require(len(argv) == 3, "finalize-integration.py FROZEN_RUNTIME ACTUAL_PLAN_JSON NEW_PREFIX")
    runtime, plan_path, prefix = Path(argv[0]), Path(argv[1]), argv[2]
    require(re.fullmatch(r"integration-followup-packet-\d{3}", prefix), "Use a fresh numbered packet prefix")
    m = load_module("b134_finalizing_complete_integration_dossiers", runtime)
    plan = json.loads(frozen(plan_path))
    require(set(plan) == {"candidate", "originalGates", "mergeGates", "preservationProof"}
            and set(plan["originalGates"]) == {"closure", "committed"}
            and set(plan["mergeGates"]) == {"merge", "committed-merge"},
            "Exact actual signed-merge plan/gate/preservation references required")
    target = m.t.output(m.ROOT / prefix)
    guard, _ = start_guard("B134 actual complete merged dossier finalization")
    try:
        outputs = {}
        for family in ("claude", "gpt"):
            spec = {
                **plan, "schemaVersion": 1, "mode": "integration", "scope": m.SCOPE,
                "family": family, "run": "N1-B134-" + family.upper() + "-INTEGRATION-001",
                "session": None if family == "claude" else m.t.OWN["gpt"],
                "basisSnapshot": m.REVIEWED, "signedClosure": m.CLOSURE,
                "basisAcceptance": m.PRIOR[family], "authorization": m.AUTH, "obligations": [],
                "templateOnly": family == "claude", "bootstrap": None,
                "reviewerOrigin": {
                    "kind": ("replacement-Claude-family-integration-impact-confirmation"
                             if family == "claude" else "same-reviewer-integration-impact"),
                    "priorSession": m.t.OWN[family],
                    "priorRun": "N1-B134-" + family.upper() + "-REVISION-002",
                },
            }
            request = target / ("request-" + family + ".json")
            freeze_json(request, spec)
            output = m.ROOT / (prefix + ("-claude-template" if family == "claude" else "-gpt"))
            m.main(["prepare", str(request), str(output)])
            outputs[family] = {
                "request": m.t.ref(request), "preflight": m.t.ref(output / "preflight.json"),
                "readiness": m.t.ref(output / "readiness.json"),
                "templateOnly": family == "claude",
            }
        creation = {
            "name": "B134 replacement Claude impact",
            "session_kind": "project",
            "execution_location": "local", "coordinate_with_creator": True, "notify_on_idle": "always",
            "kickoff": {"model": "claude-opus-5.5", "context_tier": "long_context",
                        "mode": "interactive", "prompt": m.BOOTSTRAP},
        }
        freeze_json(target / "parent-create-session-parameters.json", creation)
        freeze_json(target / "parent-send-session-message-fields.json", {
            "session_id": "<ACTUAL_ADMITTED_REVIEWER_ID>",
            "source_user_message": m.SOURCE, "mode": "interactive", "delivery_mode": "immediate",
            "message": "<EXACT_FROZEN_KICKOFF_TEXT_FROM_ADMITTED_CONFIG_NO_TRIMMING>",
        })
        freeze_json(target / "index.json", {
            "status": "PREPARED_ONLY_NOT_ADMITTED", "candidate": plan["candidate"],
            "producer": m.t.ref(runtime), "plan": m.t.ref(plan_path), "outputs": outputs,
            "requiresActualClaudeBootstrapAndBind": True, "serialOrder": ["claude", "gpt"],
            "noReviewerContact": True, "publicationAccepted": False,
        })
        print(json.dumps(outputs))
    finally:
        freeze_json(target / "finalization-memory.json", guard.finish())


if __name__ == "__main__":
    main()
