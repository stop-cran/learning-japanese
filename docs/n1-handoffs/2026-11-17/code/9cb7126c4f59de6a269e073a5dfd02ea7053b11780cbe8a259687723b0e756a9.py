"""Record the actual conservative HOLD; never substitute for admit() or lower its gate."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE / "selected-runtime-002"), r"C:\Users\stop-\n1-kanji-workspace\review-tools"]
import b134_integration_confirmation_v1 as tool
from common import WS, freeze_json, frozen, require, start_guard

ROOT = WS / "scratch-134" / "review"
TARGETS = {"claude": ROOT / "revision-confirmation-claude-002", "gpt": ROOT / "revision-confirmation-gpt-001"}
OTHER = {"claude": ("N1-B134-GPT-FRESH-003", "389d657aaee2977a256ab4a55a3b8e85e178a557251a03b6c468da837e9cb864"),
         "gpt": ("N1-B134-CLAUDE-FRESH-003", "844961d7d05d23ebb0ee43b819b3c79e1105bdcf07d77cdf739ecba0bf80d2fe")}
guard, _ = start_guard("B134 actual neutral validation and capacity HOLD record")
rows = {}
try:
    for family, folder in TARGETS.items():
        record, config, spec, chain = tool.preflight(folder / "preflight.json")
        refs, _, _ = tool.prior_evidence(spec)
        sources = tool.reconstruct(chain)
        require(sources["own-prior/report.md"] == tool.read(refs["report"])
                and sources["own-prior/adjudication.json"] == tool.read(refs["adjudication"]),
                "Own accepted raw results differ")
        for label, raw in sources.items():
            if not label.startswith("own-prior/"):
                require(all(marker.encode() not in raw for marker in OTHER[family]),
                        "Opposite-family identity/result leaked into neutral input")
        scope = tool.value(spec["scopeProof"])
        for name in scope["evidencePaths"]:
            raw = tool.read(scope["bindings"]["snapshot/" + name])
            require(raw not in b"".join(sources.values()) and "snapshot/" + name not in sources,
                    "Private raw author response leaked into reviewer source")
        final = tool.value(spec["prior"]["final"]); audit = tool.value(final["audit"])
        raw = frozen(Path(final["audit"]["path"]).parent / "events.jsonl", audit["eventsSha256"])
        _, _, capacity, _ = tool.modules()
        context = capacity.telemetry(tool.parse_events(raw), {}, family, record["session"])
        require(context["status"] == "PASS", "Actual retained model/context/compaction check failed")
        forecast = context["lastInputTokens"] + record["dossierBound"] + 49000
        limit = min(700000, capacity.PROFILES[family]["prePhase2Gate"])
        require(not Path(config["report"]).exists(), "Report destination already used")
        rows[family] = {"status": "HOLD_CONTEXT" if forecast > limit else "FORECAST_FITS_NOT_ADMITTED",
            "preflight": tool.ref(folder / "preflight.json"), "chain": record["chain"],
            "scopeProof": spec["scopeProof"], "gateProof": spec["gateProof"],
            "run": record["run"], "session": record["session"], "candidate": record["candidate"],
            "sources": len(chain["sources"]), "segments": len(chain["segments"]),
            "dossierUtf8ByteBound": record["dossierBound"], "lastAcceptedInputTokens": context["lastInputTokens"],
            "forecast": forecast, "limit": limit, "reserves": {"offset": 7000, "drift": 12000, "report": 30000},
            "neutralOnlyChecks": "PASS", "rawPriorVerdict": record["priorRawVerdict"],
            "requiredDispositionIds": [r["id"] for r in spec["obligations"]],
            "kickoffPath": config["kickoff"], "kickoffText": frozen(config["kickoff"]).decode(),
            "actualContext": context, "reportDestinationAbsent": True, "freshAdmissionRequired": True,
            "admissionAuthorized": False, "reviewAccepted": False, "publicationAccepted": False}
        guard.check()
finally:
    memory = guard.finish()
require(not memory["breach"], "Capacity diagnostic RAM breach")
require(rows["claude"]["status"] == "HOLD_CONTEXT", "Expected conservative Claude hold changed; investigate")
print(json.dumps(freeze_json(HERE / "actual-hold.json", {
    "status": "HOLD_CLAUDE_CONTEXT_GPT_SERIAL_BLOCKED", "actualAdmission": False, "runs": rows, "memory": memory,
    "disclosure": "Actual raw accepted003 usage plus complete new UTF8 dossier byte bound. This is a conservative "
    "forecast, not a tokenizer measurement. Admission remains fail-closed and unchanged. Even all-value JSON "
    "whitespace normalization saves too little; it was measured only and was NOT adopted. No reviewer contacted."})))
print(json.dumps({family: {key: row[key] for key in ("status", "sources", "segments",
      "dossierUtf8ByteBound", "lastAcceptedInputTokens", "forecast", "limit")} for family, row in rows.items()}))
