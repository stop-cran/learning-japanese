"""Preserve exact necessary-source byte bounds, including an explicit capacity HOLD."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
import b134_integrated_v1 as git_helpers
from common import freeze_json, frozen, load_module, require, sha, start_guard
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
R = "cc374051efa75199212a87c9abf08d7391419055"
C = "ae1555736086fa6a7ee29c9707ba4b07e82bf979"
PRIOR = {
    "claude": "86c82a358a68a05eae50842d45f98e5568bd013cbb1a758438bd4d042cc0cea8",
    "gpt": "c1fc8643366a1f7dd9c3f2dba849f8532e64cafc73a8533c4955f1521ccb739c",
}


def main():
    guard, _ = start_guard("B134 complete-source integration capacity decision")
    try:
        git = Git(git_helpers.REPO, RUNNER, guard)
        git_helpers.identity(git, C, [R])
        git_helpers.identity(git, git_helpers.INCOMING, [git_helpers.BASE])
        sources = {}
        for path in sorted(git_helpers.CONTENT):
            raw = git_helpers.blob(git, git_helpers.INCOMING, path)
            sources[path] = {"bytes": len(raw), "sha256": sha(raw)}
        incoming_patch = git("diff", "--no-ext-diff", "--no-color", "--no-renames",
                             "--binary", git_helpers.BASE, git_helpers.INCOMING)
        sources["signed-incoming.patch"] = {"bytes": len(incoming_patch), "sha256": sha(incoming_patch)}
        module = load_module("b134_capacity_exact_active_v3",
                            REVIEW / "authorization-runtime-004" / "b134_authorized_confirmation_v3.py")
        t = module.legacy
        _, _, capacity, _ = t.modules()
        families = {}
        for family in ("claude", "gpt"):
            accepted_path = REVIEW / f"authorized-{family}-accept-001" / "acceptance.json"
            accepted = json.loads(frozen(accepted_path, PRIOR[family]))
            require(accepted["verdict"] == "CONFIRMED" and accepted["confirmationAccepted"] is True
                    and accepted["reviewEvidenceAccepted"] is True and accepted["candidate"] == R
                    and accepted["mode"] == "revision"
                    and accepted["acceptedNewFindings"] == accepted["openClaimIds"] == [],
                    "Not the actual accepted own revision basis")
            raw_events = (Path.home() / ".copilot" / "session-state" / accepted["session"] / "events.jsonl").read_bytes()
            telemetry = capacity.telemetry(t.parse_events(raw_events), {}, family, accepted["session"])
            require(telemetry["status"] == "PASS", "Actual model/context/zero-compaction failed")
            profile = capacity.PROFILES[family]
            cap = 740000 if family == "claude" else 710000
            require(capacity.STARTUP_GATE == 700000 and profile["prePhase2Gate"] == cap,
                    "Continuation/startup profile changed")
            own = {k: {"bytes": len(t.read(accepted[k])), "ref": accepted[k]} for k in ("report", "adjudication")}
            # Excluding the optional adjudication makes this an optimistic bound,
            # so it cannot produce a spurious rejection of the full dossier.
            required_bytes = sum(row["bytes"] for row in sources.values()) + own["report"]["bytes"]
            minimal_bytes = sum(sources[p]["bytes"] for p in git_helpers.CONTENT) + own["report"]["bytes"]
            def bound(size):
                projected = telemetry["lastInputTokens"] + size + 49000
                return {"completeSourceBytes": size, "forecast": projected, "limit": cap,
                        "excess": max(0, projected-cap),
                        "status": "HOLD" if projected > cap else "LOWER_BOUND_ONLY_NOT_READINESS"}
            families[family] = {
                "priorAcceptance": {"path": str(accepted_path), "sha256": PRIOR[family]},
                "session": accepted["session"], "telemetry": telemetry, "priorSources": own,
                "reserves": {"offset": 7000, "drift": 12000, "report": 30000},
                "strictNecessaryUnitsOnly": bound(minimal_bytes),
                "withRequiredSignedIncomingPatch": bound(required_bytes),
                "withOptionalOwnAdjudication": bound(required_bytes + own["adjudication"]["bytes"]),
                "exclusions": ["future actual cc374..M runtime patch", "neutral docs-only closure bindings",
                               "actual preservation and host-gate proof", "chain envelopes", "prompt", "kickoff"],
            }
        result = {
            "status": "HOLD_SAME_CLAUDE_COMPLETE_UNITS_EXCEED_CONTINUATION"
                      if families["claude"]["strictNecessaryUnitsOnly"]["status"] == "HOLD"
                      else "LOWER_BOUND_ONLY_AWAIT_ACTUAL_M",
            "reviewed": R, "signedClosure": C, "incoming": git_helpers.INCOMING,
            "completeSourceUnits": sources, "families": families, "initialStartupGateUnchanged": 700000,
            "measurement": "Actual raw UTF8 bytes and actual retained telemetry; forecasts are not token measurements.",
            "noReviewerContact": True, "actualMergeNotYetRequiredForThisNecessaryBound": True,
            "noAdmissionOrAcceptance": True,
        }
        freeze_json(ROOT / "capacity-decision-002.json", result)
        print(json.dumps(result, ensure_ascii=False))
    finally:
        freeze_json(ROOT / "capacity-probe-memory-002.json", guard.finish())


if __name__ == "__main__":
    main()
