"""Freeze the B134 integration plan from actual evidence refs.

Usage:
  freeze-b134-integration-plan.py preflight NEW_REVIEW_OUTPUT
      Writes a DRAFT plan whose confirmation refs are placeholders and validates only
      load_plan + plan_gates (original and merge gates) against the real repository.
      The draft is never usable for assembly: accepted() rejects the placeholders.
  freeze-b134-integration-plan.py real CLAUDE_ACCEPTANCE GPT_ACCEPTANCE NEW_REVIEW_OUTPUT
      Writes the real plan.json (read-only) and validates load_plan + plan_gates + accepted.
"""
import json
import sys
from pathlib import Path

import b134_integrated_v2 as contract
from common import freeze_json, frozen, require, sha, start_guard
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

C = "ae1555736086fa6a7ee29c9707ba4b07e82bf979"
M = "b140716f5df6d17fb872f477556ef77d2cd59b0e"
HERE = contract.SCRATCH
GATES = {
    "originalGates": {"closure": HERE / "closure-checks-001" / "summary.json",
                      "committed": HERE / "committed-checks-001" / "summary.json"},
    "mergeGates": {"merge": contract.REVIEW / "integration-merge-gates-003" / "summary.json",
                   "committed-merge": contract.REVIEW / "integration-merge-committed-gates-001" / "summary.json"},
}
INVENTORY = contract.REVIEW / "integration-v2-prep-001" / "tool-inventory.json"


def ref(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": sha(frozen(path))}


def main(mode, *args):
    require(mode in ("preflight", "real"), __doc__)
    if mode == "real":
        require(len(args) == 3, __doc__)
        claude, gpt, output = ref(args[0]), ref(args[1]), Path(args[2]).resolve()
    else:
        require(len(args) == 1, __doc__)
        output = Path(args[0]).resolve()
    require(output.parent == contract.REVIEW and not output.exists(), "Use a new direct review output")
    output.mkdir()
    if mode == "preflight":
        placeholder = freeze_json(output / "placeholder-not-a-confirmation.json",
                                  {"placeholder": True, "acceptable": False})
        claude = gpt = {"path": str((output / "placeholder-not-a-confirmation.json").resolve()),
                        "sha256": sha(frozen(output / "placeholder-not-a-confirmation.json"))}
        del placeholder
    plan = {
        "schemaVersion": 1, "batch": 134, "reviewedSnapshot": contract.REVIEWED,
        "signedClosure": C, "merge": M, "incoming": contract.INCOMING,
        "originalGates": {k: ref(v) for k, v in GATES["originalGates"].items()},
        "mergeGates": {k: ref(v) for k, v in GATES["mergeGates"].items()},
        "confirmations": {"claude": claude, "gpt": gpt},
        "toolInventory": ref(INVENTORY),
    }
    name = "plan.json" if mode == "real" else "draft-plan-not-for-assembly.json"
    freeze_json(output / name, plan)
    guard, _ = start_guard("B134 integration plan " + mode)
    try:
        git = Git(contract.REPO, RUNNER, guard)
        loaded, raw = contract.load_plan(output / name)
        contract.merge(git, loaded["signedClosure"], loaded["merge"])
        contract.plan_gates(git, loaded)
        accepted = None
        if mode == "real":
            accepted = {f: {"run": v["run"], "session": v["session"]}
                        for f, v in contract.accepted(loaded).items()}
        else:
            try:
                contract.accepted(loaded)
                raise AssertionError("Placeholder confirmation was accepted")
            except (ValueError, KeyError):
                pass
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Plan RAM breach")
    result = {"status": "PASS_PLAN_" + mode.upper(), "planSha256": sha(raw), "plan": str(output / name),
              "acceptedConfirmations": accepted, "gatesValidated": True,
              "usableForAssembly": mode == "real", "memory": memory}
    print(json.dumps(freeze_json(output / "result.json", result)))


if __name__ == "__main__":
    main(*sys.argv[1:])
