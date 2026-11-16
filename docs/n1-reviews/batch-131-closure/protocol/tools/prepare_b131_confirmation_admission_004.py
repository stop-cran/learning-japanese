"""Rebuild the unlaunched first-family run after an input/output name collision."""
import json
from pathlib import Path

from b131_confirmation_routing_001 import INITIALS, capacity_check, check_context
from common import WS, freeze_json, frozen, sha
from confirm_b131_003 import build, preflight

ROOT = WS / "scratch-131" / "review"
OUT = ROOT / "confirm-003"


def main():
    spec = json.loads(frozen(OUT / "N1-B131-CLAUDE-CONFIRM-002-spec.json"))
    spec["run"] = "N1-B131-CLAUDE-CONFIRM-003"
    path = OUT / (spec["run"] + "-spec.json")
    freeze_json(path, spec)
    build(path)
    result = json.loads(frozen(ROOT / "confirmation-003-preparation.json"))
    record, config = preflight(OUT / (spec["run"] + "-preflight.json"))
    chain = json.loads(frozen(config["chainManifest"]))
    context = check_context(Path.home() / ".copilot" / "session-state" /
                            INITIALS["claude"]["session"] / "events.jsonl", "claude")
    result["runs"][0] = {
        "run": record["run"], "session": record["session"],
        "preflight": {"path": str(OUT / (record["run"] + "-preflight.json")),
                      "sha256": sha(frozen(OUT / (record["run"] + "-preflight.json")))},
        "capacity": capacity_check(context, chain),
        "segments": len(chain["segments"]), "sources": len(chain["sources"]),
    }
    result["producerSha256"] = sha(frozen(Path(__file__)))
    result["preservedFailures"].append(
        "Claude002 admission input was mistakenly named as the exclusive admission-request output. "
        "Admission stopped after writing immutable prefix/status/roster but before an admission record "
        "or launch. This run changes only the run identity. Its input request must live outside "
        "the protocol's reserved output namespace; earlier partial outputs remain intact.")
    print(json.dumps(freeze_json(ROOT / "confirmation-004-preparation.json", result)))


if __name__ == "__main__":
    main()
