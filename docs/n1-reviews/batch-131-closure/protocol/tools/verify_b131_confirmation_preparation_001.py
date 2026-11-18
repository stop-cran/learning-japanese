"""Verify prepared protocol and actual original contexts without admitting a reviewer."""
import json
import re
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, load_module, require, sha, start_guard
import b131_confirmation_routing_001 as routing

ROOT = WS / "scratch-131" / "review"
ENGINE = TOOLS / "confirm_b131_003.py"
ENGINE_SHA = "02fdfe00aa34e2780904e335a8b0fba869ae9ad2c79e2166d3c24c903ccfe8c0"
OUTPUT = ROOT / "confirmation-preparation-verification-001.json"


def bound(path):
    return {"path": str(path), "sha256": sha(frozen(path))}


def main():
    frozen(ENGINE, ENGINE_SHA)
    engine = load_module("b131_confirm_verified_engine", ENGINE)
    config = engine.load_batch(131)
    require(config["candidate"] == routing.PARENT, "Wrong original review snapshot")
    out = ROOT / "confirm-003"
    tooling = json.loads(frozen(out / "tooling-preflight.json"))
    require(tooling["exitCode"] == 0 and tooling["rendererChecks"] == 3, "Protocol preparation failed")
    log = frozen(tooling["tests"]["path"], tooling["tests"]["sha256"])
    require(re.search(rb"Ran 21 tests in", log) and re.search(rb"\bOK\b", log),
            "Expected protocol test execution is missing")
    for row in tooling["derivations"]:
        source = frozen(row["source"]["path"], row["source"]["sha256"])
        derived = frozen(row["output"]["path"], row["output"]["sha256"])
        if Path(row["output"]["path"]).name == "audit-confirm.py":
            expected = source.replace(b"B116", b"B131").replace(
                b"sys.path.insert(0, str(HERE.parent))",
                b"sys.path.insert(0, str(HERE.parent / 'preparation-003'))")
            require(derived == expected, "Auditor differs beyond batch label and import namespace")
        elif Path(row["output"]["path"]).name != "renderer.py":
            require(derived == source.replace(b"B116", b"B131"), "Report/checker semantics changed")
    guard, _ = start_guard("B131 actual confirmation routing verification")
    try:
        packet, sums, digest = engine.verify_packet(config, guard)
        require(packet.name == "batch-131-1359b467-compact-002", "Wrong original packet")
        observations = {}
        for family, expected in routing.INITIALS.items():
            path = routing.initial_directory(family) / (expected["run"] + "-acceptance.json")
            accepted = json.loads(frozen(path, expected["acceptanceSha256"]))
            spec = {"batch": 131, "family": family, "session": expected["session"],
                    "acceptance": {"path": str(path), "sha256": expected["acceptanceSha256"]}}
            routing.initial_launch(spec, accepted, config)
            for item in routing.routing_bindings(family):
                frozen(item["path"], item["sha256"])
            events = Path.home() / ".copilot" / "session-state" / expected["session"] / "events.jsonl"
            context = routing.check_context(events, family)
            require(context["status"] == "PASS", "Original context fails: " + family)
            observations[family] = {
                "originalSession": expected["session"], "initialAcceptance": spec["acceptance"],
                "checker": context["checker"], "eventsSha256": context["eventsSha256"],
                "actualPeakInputTokens": context["exactProfile"]["actualPeakInputTokens"],
                "lastInputTokens": context["exactProfile"]["lastInputTokens"],
                "contextProfile": context["exactProfile"]["contextProfile"],
                "compactions": context["exactProfile"]["compactions"],
                "capacityAccepted": False,
            }
            guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation verification RAM breach")
    print(json.dumps(freeze_json(OUTPUT, {
        "batch": 131, "candidate": routing.PARENT, "status": "PASS_PROTOCOL_PREPARATION_ONLY",
        "engine": bound(ENGINE), "protocol": bound(out / "tooling-preflight.json"),
        "derivations": [bound(ROOT / f"confirmation-engine-derivation-{i:03}.json") for i in (1, 2, 3)],
        "packet": {"path": str(packet), "manifestSha256": digest, "filesRehashed": len(sums)},
        "originalReviewers": observations, "memory": memory,
        "producer": bound(Path(__file__)),
        "limits": "No signed successor is asserted by this observation. Successor verification, "
                  "isolated response/source chains, actual-chain capacity forecasts and fresh serial "
                  "full-roster admission remain required. Raw failed preparations are preserved. "
                  "No reviewer is launched, no confirmation or semantic/publication acceptance is granted.",
        "reviewersLaunched": False, "publicationAccepted": False,
    })))


if __name__ == "__main__":
    main()
