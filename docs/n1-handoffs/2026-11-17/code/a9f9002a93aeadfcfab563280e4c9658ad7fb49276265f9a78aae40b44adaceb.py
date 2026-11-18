"""Numeric-only out-of-sample check of the B131 calibrated capacity model.

Reads only call roles/event indices from B132 phase-1 audits and only numeric usage
fields from their event logs. No reviewer prose, selections or findings are emitted.
"""
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
B132 = ROOT / r"scratch-132\review\neutral-preparation-002"
B133 = ROOT / r"scratch-133\review\neutral-preparation-003"
CALIBRATION = ROOT / r"scratch-131\review\capacity\claude001-calibration-001.json"
CALIBRATION_SHA = "aca593742a9191eec34aa7b8774b4042789bdf7d0025fcfe0d06896b0a3041da"
FIT = {"docs": .354, "jlpt": .374, "cards": .502, "evjson": .522,
       "extract": .446, "jmdict": .543, "kanjidic": .526, "titleidx": .531}
MARGIN = 1.10
AUDITS = {
    "claude": B132 / r"protocol-001\N1-B132-CLAUDE-001\audit-20261116T224610648195",
    "gpt": B132 / r"protocol-001\N1-B132-GPT-001\audit-20261116T225330964420",
}
USAGE_FIELDS = ("inputTokens", "outputTokens", "maxPromptTokens")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_class(name):
    if name in {"evidence/jmdict-families.xml", "evidence/jmdict-review-core.xml"}:
        return "jmdict"
    if name == "evidence/kanjidic2-records.xml":
        return "kanjidic"
    if name == "repo/docs/jlpt-levels.md":
        return "jlpt"
    if name.endswith(("-extract.txt", "/extract.txt")):
        return "extract"
    if name in {"evidence/title-index.txt", "evidence/baseline-title-index.txt",
                "evidence/title-index-delta.txt"}:
        return "titleidx"
    if name.startswith(("snapshot/", "baseline/", "repo/kanji/", "repo/words/")) and name.endswith(".md"):
        return "cards"
    if name.startswith("evidence/") or name.startswith("snapshot/strokes/"):
        return "evjson"
    return "docs"


def segment_parts(segment):
    raw = Path(segment["path"]).read_bytes()
    if sha(raw) != segment["sha256"] or len(raw) != segment["bytes"]:
        raise SystemExit(f"Segment changed: {segment['path']}")
    lines = raw.splitlines(keepends=True)
    parts = Counter()
    for part in segment["parts"]:
        parts[source_class(part["source"])] += len(b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]]))
    return parts


def forecast(parts):
    return sum(count * FIT[label] * MARGIN for label, count in parts.items())


def numeric_usage(events_path):
    records = []
    with events_path.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            event = json.loads(line)
            if event.get("type") == "session.usage_record":
                usage = (event.get("data") or {}).get("usage") or {}
                records.append({"event": index, **{k: usage.get(k) for k in USAGE_FIELDS}})
            elif str(event.get("type", "")).startswith("session.compaction"):
                raise SystemExit("Compaction present in calibration source")
    return records


def actual_deltas(audit_dir, segments):
    audit = json.loads((audit_dir / "audit.json").read_bytes())
    events = audit_dir / "events.jsonl"
    if sha(events.read_bytes()) != audit["eventsSha256"]:
        raise SystemExit("events hash mismatch")
    usage = numeric_usage(events)
    roles = {call.get("role"): call["event"] for call in audit["calls"] if call.get("role")}
    after = lambda event: next(row for row in usage if row["event"] > event)
    rows, previous = [], after(roles["bootstrap"])
    for segment in segments:
        current = after(roles[f"core-{segment['index']}"])
        rows.append({"index": segment["index"], "delta": current["inputTokens"] - previous["inputTokens"]})
        previous = current
    return {"auditSha256": sha((audit_dir / "audit.json").read_bytes()), "eventsSha256": audit["eventsSha256"],
            "firstInputTokens": usage[0]["inputTokens"], "bootstrapInputTokens": after(roles["bootstrap"])["inputTokens"],
            "lastCoreInputTokens": previous["inputTokens"],
            "maxPromptTokens": sorted({row["maxPromptTokens"] for row in usage}), "rows": rows}


def main(output):
    if sha(CALIBRATION.read_bytes()) != CALIBRATION_SHA:
        raise SystemExit("Calibration hash mismatch")
    if json.loads(CALIBRATION.read_bytes())["fittedTokensPerByteNNLS"] != FIT:
        raise SystemExit("Fitted coefficients differ")
    chain132 = json.loads((B132 / "core-chain-001.json").read_bytes())
    segs = chain132["segments"]
    parts132 = {s["index"]: segment_parts(s) for s in segs}
    result = {"kind": "numeric-capacity-crossvalidation", "calibrationSha256": CALIBRATION_SHA,
              "fit": FIT, "margin": MARGIN,
              "b132CoreChainSha256": sha((B132 / "core-chain-001.json").read_bytes()),
              "b132CoreBytes": sum(s["bytes"] for s in segs), "families": {}}
    for family, audit_dir in AUDITS.items():
        actual = actual_deltas(audit_dir, segs)
        rows = []
        for row in actual["rows"]:
            seg = next(s for s in segs if s["index"] == row["index"])
            fc = forecast(parts132[row["index"]])
            rows.append({"index": row["index"], "bytes": seg["bytes"], "classes": dict(parts132[row["index"]]),
                         "actualDelta": row["delta"], "forecast": math.ceil(fc),
                         "actualTokensPerSegmentByte": row["delta"] / seg["bytes"],
                         "forecastMinusActual": math.ceil(fc) - row["delta"]})
        under = [r["index"] for r in rows if r["forecastMinusActual"] < 0]
        result["families"][family] = {
            **{k: v for k, v in actual.items() if k != "rows"},
            "actualCoreTokens": sum(r["actualDelta"] for r in rows),
            "forecastCoreTokens": sum(r["forecast"] for r in rows),
            "segmentsUnderForecast": under,
            "worstSegmentUnderrun": min(r["forecastMinusActual"] for r in rows),
            "maxActualTokensPerSegmentByte": max(r["actualTokensPerSegmentByte"] for r in rows),
            "rows": rows}
    chain133 = json.loads((B133 / "core-chain-001.json").read_bytes())
    totals = Counter()
    for s in chain133["segments"]:
        totals.update(segment_parts(s))
    envelope = sum(s["bytes"] for s in chain133["segments"]) - sum(totals.values())
    result["b133"] = {"coreChainSha256": sha((B133 / "core-chain-001.json").read_bytes()),
                      "segments": len(chain133["segments"]),
                      "bytes": sum(s["bytes"] for s in chain133["segments"]),
                      "classBytes": dict(totals), "envelopeBytes": envelope,
                      "fittedForecastTokens": math.ceil(forecast(totals)),
                      "fittedPlusEnvelopeAtOneTPB": math.ceil(forecast(totals)) + envelope}
    data = json.dumps(result, indent=1, ensure_ascii=False).encode("utf-8")
    Path(output).write_bytes(data)
    summary = {k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in result["families"].items()}
    print(json.dumps({"families": summary, "b133": result["b133"], "sha256": sha(data)}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
