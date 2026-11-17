"""Measure only an all-values, key-order-preserving JSON whitespace adaptation."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE / "selected-runtime-002"), r"C:\Users\stop-\n1-kanji-workspace\review-tools"]
import b134_integration_confirmation_v1 as tool
from common import WS, freeze_json, require, sha, start_guard

guard, _ = start_guard("B134 complete JSON whitespace savings measurement")
rows = {}
try:
    for family, name in (("claude", "revision-confirmation-claude-002"), ("gpt", "revision-confirmation-gpt-001")):
        record, config, spec, chain = tool.preflight(WS / "scratch-134" / "review" / name / "preflight.json")
        changes = {}
        for label, raw in tool.reconstruct(chain).items():
            if not label.endswith(".json"):
                continue
            derived = (json.dumps(json.loads(raw), ensure_ascii=False, indent=0) + "\n").encode()
            require(json.loads(raw, object_pairs_hook=list) == json.loads(derived, object_pairs_hook=list),
                    "A value/key order/duplicate JSON property would change")
            changes[label] = {"originalBytes": len(raw), "derivedBytes": len(derived),
                              "savedBytes": len(raw) - len(derived), "originalSha256": sha(raw),
                              "derivedSha256": sha(derived)}
        rows[family] = changes
finally:
    memory = guard.finish()
print(json.dumps(freeze_json(HERE / "lossless-json-measurement.json",
                            {"measurementOnly": True, "noProtocolChange": True, "runs": rows, "memory": memory})))
print(json.dumps(rows, indent=2))
