"""Versioned retained-context continuation adapter; initial-review admission is unchanged.

The frozen v1 sources, 700000 startup evidence, all source/RAM/serial/event/read/write
gates and 49000 reserves remain intact. Only the NEW follow-up context forecast uses
the exact original launch.prePhase2Gate (Claude740000/GPT710000), not v1's additional
min(700000, continuation gate). No projection or source reduction is introduced.
"""
import json
import sys
from pathlib import Path

from common import WS, frozen, load_module, require

ROOT = WS / "scratch-134" / "review"
V1 = ROOT / "integration-confirmation-prep-001" / "selected-runtime-002" / "b134_integration_confirmation_v1.py"
V1_SHA = "4070171ab891062859a5df1e07d7f6ab76732c66832db353e08aacf271a45f61"
PREFLIGHT = ROOT / "fresh-independent-002" / "lifecycle-011" / "audit-configs-020" / "preflight.json"
PREFLIGHT_SHA = "797dc1491edceafba6e8ba580c09588144a2f2f4e6238c0176fada7167828eaa"
EXPECTED = {
    "claude": {"selectedModel": "claude-opus-5.5", "contextTier": "long_context",
               "maxPromptTokens": 952000, "prePhase2Gate": 740000},
    "gpt": {"selectedModel": "gpt-6.1-sol", "contextTier": "long_context",
            "maxPromptTokens": 922000, "prePhase2Gate": 710000},
}
frozen(V1, V1_SHA)
legacy = load_module("b134_followup_pinned_v1", V1)
legacy.PINS["followupV1"] = (V1, V1_SHA)
legacy.PINS["continuationPreflight"] = (PREFLIGHT, PREFLIGHT_SHA)


def continuation_profile(family):
    require(family in EXPECTED, "Unknown retained-continuation family")
    _, _, capacity, _ = legacy.modules()
    launch = json.loads(frozen(PREFLIGHT, PREFLIGHT_SHA))["runs"][family]["launch"]
    expected = EXPECTED[family]
    require(capacity.STARTUP_GATE == 700000 and capacity.PROFILES[family] == expected
            and launch["mode"] == "interactive"
            and launch["model"] == expected["selectedModel"]
            and all(launch[key] == expected[key] for key in ("contextTier", "maxPromptTokens", "prePhase2Gate")),
            "Unknown/unpinned continuation profile or altered original startup gate")
    return expected


def context(events, family, session, dossier_bound):
    profile = continuation_profile(family)
    _, _, capacity, _ = legacy.modules()
    result = capacity.telemetry(events, {}, family, session)
    require(result["status"] == "PASS", "Retained context/model/usage/zero-compaction gate failed")
    require(type(dossier_bound) is int and dossier_bound >= 0, "Invalid complete dossier byte bound")
    forecast = result["lastInputTokens"] + 7000 + dossier_bound + 12000 + 30000
    limit = profile["prePhase2Gate"]
    require(forecast <= limit, f"Retained continuation HOLD: {forecast} > {limit}")
    return {**result, "forecast": forecast, "limit": limit, "dossierBound": dossier_bound,
            "reserves": {"offset": 7000, "drift": 12000, "report": 30000},
            "policy": "exact-original-launch-continuation-v2", "originalStartupGateUnchanged": 700000,
            "continuationPreflight": {"path": str(PREFLIGHT), "sha256": PREFLIGHT_SHA}}


legacy.context = context
# Provenance belongs to this explicitly pinned adapter, not its frozen implementation dependency.
legacy.__file__ = __file__


def main(argv=None):
    return legacy.main(argv)


if __name__ == "__main__":
    sys.exit(main())
