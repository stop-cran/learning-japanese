"""Verify B134 integration closure without changing the linear tools or original ledger.

Unlike the B130 hard-coded closure verifier, future C/M/I and actual confirmation
references come from a frozen hash-bound plan. No semantic acceptance is manufactured.
Usage: PLAN INTEGRATION_CLOSURE NEW_REVIEW_OUTPUT
"""
import json
import sys
from pathlib import Path

import b134_integrated_v1 as contract
from common import freeze_json, frozen, require, sha, start_guard
from verify_b134_packet import RUNNER
from verify_b134_sources import Git


def main(plan_path, commit, output):
    plan, plan_raw = contract.load_plan(Path(plan_path))
    output = Path(output).resolve()
    require(output.parent == contract.REVIEW and not output.exists(), "Use a new review output")
    guard, _ = start_guard("B134 integration closure verification")
    try:
        git = Git(contract.REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == commit
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Wrong or dirty closure")
        context = contract.verify_closure(git, plan, commit)
        contract.plan_gates(git, plan)
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Closure changed")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Closure verifier RAM breach")
    print(json.dumps(freeze_json(output / "verification.json", {
        "status": "PASS_SIGNED_INTEGRATION_CLOSURE_ONLY", "commit": commit, "context": context,
        "planSha256": sha(plan_raw), "producerSha256": sha(frozen(Path(__file__))), "memory": memory,
        "publicationAccepted": False, "deliveryCredit": 0})))


if __name__ == "__main__":
    require(len(sys.argv) == 4, __doc__)
    main(*sys.argv[1:])
