"""Verify actual own-only dossiers/capacity forecasts; NOT fresh admission or acceptance."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE / "selected-runtime-002"), r"C:\Users\stop-\n1-kanji-workspace\review-tools"]
import b134_integration_confirmation_v1 as tool
from common import WS, freeze_json, frozen, require, sha, start_guard

REVIEW = WS / "scratch-134" / "review"
TARGETS = {"claude": REVIEW / "revision-confirmation-claude-002",
           "gpt": REVIEW / "revision-confirmation-gpt-001"}
OPPOSITE = {"claude": ("N1-B134-GPT-FRESH-003",
                      "389d657aaee2977a256ab4a55a3b8e85e178a557251a03b6c468da837e9cb864"),
            "gpt": ("N1-B134-CLAUDE-FRESH-003",
                   "844961d7d05d23ebb0ee43b819b3c79e1105bdcf07d77cdf739ecba0bf80d2fe")}


def main():
    guard, _ = start_guard("B134 actual neutral dossier and retained-context forecast")
    rows = {}
    try:
        for family, folder in TARGETS.items():
            record, config, spec, chain = tool.preflight(folder / "preflight.json")
            refs, _, _ = tool.prior_evidence(spec)
            sources = tool.reconstruct(chain)
            require(sources["own-prior/report.md"] == tool.read(refs["report"])
                    and sources["own-prior/adjudication.json"] == tool.read(refs["adjudication"]),
                    "Own accepted report/adjudication bytes differ")
            for name, raw in sources.items():
                if not name.startswith("own-prior/"):
                    require(all(marker.encode() not in raw for marker in OPPOSITE[family]),
                            "Opposite-family result in neutral source: " + name)
            all_sources = b"".join(sources.values())
            scope = tool.value(spec["scopeProof"])
            for name in scope["evidencePaths"]:
                raw = tool.read(scope["bindings"]["snapshot/" + name])
                require(raw not in all_sources and "snapshot/" + name not in sources,
                        "Private author response leaked into reviewer source")
            require(not Path(config["report"]).exists(), "Report destination already used")
            final = tool.value(spec["prior"]["final"])
            audit = tool.value(final["audit"])
            raw = frozen(Path(final["audit"]["path"]).parent / "events.jsonl", audit["eventsSha256"])
            forecast = tool.context(tool.parse_events(raw), family, record["session"], record["dossierBound"])
            rows[family] = {
                "status": "PASS_ACTUAL_NEUTRAL_DOSSIER_NOT_ADMISSION",
                "preflight": tool.ref(folder / "preflight.json"), "chain": record["chain"],
                "scopeProof": spec["scopeProof"], "gateProof": spec["gateProof"],
                "run": record["run"], "session": record["session"], "candidate": record["candidate"],
                "sources": len(chain["sources"]), "segments": len(chain["segments"]),
                "dossierUtf8ByteBound": record["dossierBound"], "lastAcceptedInputTokens": forecast["lastInputTokens"],
                "forecast": forecast["forecast"], "limit": forecast["limit"],
                "context": forecast, "reportDestinationAbsent": True, "rawPriorVerdict": record["priorRawVerdict"],
                "requiredDispositionIds": [r["id"] for r in spec["obligations"]],
                "kickoffPath": config["kickoff"], "kickoffText": frozen(config["kickoff"]).decode(),
                "freshAdmissionRequired": True, "reviewAccepted": False, "publicationAccepted": False}
            guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Readiness check RAM breach")
    result = {"status": "PASS_PREPARATION_ONLY", "actualReviewerAdmission": False,
              "candidate": "cc374051efa75199212a87c9abf08d7391419055", "runs": rows, "memory": memory,
              "capacityDisclosure": "Forecast from each unchanged accepted003 audit, not a fresh status/roster gate "
              "or tokenizer measurement. Before each serial message admit() rechecks live raw context, "
              "all-session idle status, exact model/long_context, zero compaction and >2GiB RAM."}
    print(json.dumps(freeze_json(HERE / "actual-readiness.json", result)))
    print(json.dumps({family: {key: value[key] for key in ("sources", "segments", "dossierUtf8ByteBound",
          "lastAcceptedInputTokens", "forecast", "limit")} for family, value in rows.items()}))


if __name__ == "__main__":
    main()
