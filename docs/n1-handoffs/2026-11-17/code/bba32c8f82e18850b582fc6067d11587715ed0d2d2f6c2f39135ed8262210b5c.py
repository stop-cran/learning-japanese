"""Measure, without admission, the inherited KD projection fallback on the full dossier."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard
import confirm_b134 as confirm
from b134_confirmation_capacity import confirmation_cost
from capacity004 import project, xml_bytes

OUT = confirm.ROOT / "confirmation-capacity-fallback-001"


def main():
    require(not OUT.exists(), "Preserve the previous capacity trial")
    chain_path = confirm.OUT / "N1-B134-CLAUDE-CONFIRM-002-chain.json"
    chain = json.loads(frozen(chain_path))
    guard, _ = start_guard("B134 confirmation capacity fallback measurement")
    try:
        rows = {row["source"]: row for row in chain["sources"]}
        rebuilt = {name: b"" for name in rows}
        for segment in chain["segments"]:
            raw = frozen(segment["path"], segment["sha256"])
            lines = raw.splitlines(keepends=True)
            for part in segment["parts"]:
                rebuilt[part["source"]] += b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
        for name, raw in rebuilt.items():
            require(sha(raw) == rows[name]["sha256"], "Incomplete original source reconstruction")
        original = rebuilt.pop("evidence/kanjidic2-records.xml")
        projected = xml_bytes(project(original))
        require(ET.canonicalize(ET.tostring(project(original), encoding="unicode"), strip_text=True)
                == ET.canonicalize(projected, strip_text=True), "Inherited projection differs")
        rebuilt["evidence/kanjidic2-review-projection.xml"] = projected
        sources = [(name, raw, None) for name, raw in rebuilt.items()]
        manifest_path = OUT / "chain.json"
        trial = confirm.build_chain(sources, OUT / "segments", manifest_path, guard,
                                    "B134 capacity trial only; no reviewer admission")
        confirm.verify_chain(trial, sources)
        cost = confirmation_cost(trial)
        observed = confirm.context((Path.home() / ".copilot" / "session-state"
            / confirm.INITIALS["claude"]["session"] / "events.jsonl").read_bytes(), "claude")
        prompt = frozen(confirm.OUT / "N1-B134-CLAUDE-CONFIRM-002-prompt.txt")
        peak = observed["lastInputTokens"] + cost["tokens"] + len(prompt) + 12000 + 30000
        result = {
            "status": "HOLD" if peak >= 700000 else "FORECAST_ONLY_NOT_ADMITTED",
            "originalChainSha256": sha(frozen(chain_path)), "originalFullCost": confirmation_cost(chain),
            "fallbackChainSha256": sha(frozen(manifest_path)), "fallbackCost": cost,
            "priorInputTokens": observed["lastInputTokens"], "promptBytes": len(prompt),
            "driftAllowance": 12000, "reportAllowance": 30000, "startupGate": 700000,
            "projectedPeak": peak, "excess": max(0, peak - 700000),
            "originalKdBytes": len(original), "projectedKdBytes": len(projected),
            "scope": "Only the previously prescribed, mechanically equality-checked KD field projection. "
                     "Every other complete source, family, article and native capture unchanged.",
            "projectionEquality": "Canonical XML equality; formatting-only whitespace normalized.",
            "limits": "Capacity estimate, not actual tokenizer measurement or admission. No optional-unit "
                      "access or modified prompt was implemented; do not deliver this trial to a reviewer.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Capacity trial RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(OUT / "measurement.json", result)))
    print(json.dumps({key: result[key] for key in ("status", "projectedPeak", "startupGate", "excess")}))


if __name__ == "__main__":
    main()
