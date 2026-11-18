"""Read-only lower-bound measurement before the actual signed merge exists."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
import b134_integrated_v1 as git_helpers
from common import freeze_json, frozen, load_module, start_guard
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
R = "cc374051efa75199212a87c9abf08d7391419055"
C = "ae1555736086fa6a7ee29c9707ba4b07e82bf979"


def main():
    guard, _ = start_guard("B134 integration followup capacity lower bound")
    try:
        git = Git(git_helpers.REPO, RUNNER, guard)
        git_helpers.identity(git, C, [R])
        sizes = {p: len(git_helpers.blob(git, git_helpers.INCOMING, p))
                 for p in sorted(git_helpers.CONTENT)}
        sizes["signed-incoming.patch"] = len(git("diff", "--no-ext-diff", "--no-color", "--no-renames",
                                                 "--binary", git_helpers.BASE, git_helpers.INCOMING))
        module = load_module("b134_capacity_probe_v3",
                            REVIEW / "authorization-runtime-004" / "b134_authorized_confirmation_v3.py")
        t = module.legacy
        families = {}
        for family in ("claude", "gpt"):
            accepted = json.loads(frozen(REVIEW / f"authorized-{family}-accept-001" / "acceptance.json"))
            events = (Path.home() / ".copilot" / "session-state" / accepted["session"] / "events.jsonl").read_bytes()
            prior_sizes = {k: len(t.read(accepted[k])) for k in ("report", "adjudication")}
            bound = sum(sizes.values()) + sum(prior_sizes.values())
            families[family] = {"mandatoryCompleteBytesLowerBound": bound, "priorSizes": prior_sizes,
                                "context": t.context(t.parse_events(events), family, accepted["session"], bound)}
        result = {"status": "LOWER_BOUND_ONLY_NOT_READINESS", "completeUnitBytes": sizes, "families": families,
                  "excludedFromBound": "Future exact merged runtime patch, neutral preservation/gate proof, chain and prompt"}
        freeze_json(ROOT / "capacity-lower-bound.json", result)
        print(json.dumps(result))
    finally:
        freeze_json(ROOT / "capacity-probe-memory.json", guard.finish())


if __name__ == "__main__":
    main()
