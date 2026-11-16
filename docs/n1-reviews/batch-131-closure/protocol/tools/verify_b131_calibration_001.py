"""Verify capacity telemetry without emitting reviewer text or selections."""
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
REVIEW = WS / "scratch-131" / "review"
PREP = REVIEW / "preparation-001"
CALIBRATION = REVIEW / "capacity" / "claude001-calibration-001.json"
CALIBRATION_SHA = "aca593742a9191eec34aa7b8774b4042789bdf7d0025fcfe0d06896b0a3041da"
CORE = PREP / "core-chain-compact-001.json"
CORE_SHA = "1226ce87e7d7a92685de6845406678dac668ece7508002f4389b4f8ab97df32b"
EVENTS = PREP / "N1-B131-CLAUDE-001" / "audit-20261116T174509032926" / "events.jsonl"
EVENTS_SHA = "11c417ef912e2f004dece4a9c8f78e22162d5ef1f66dd14eaef16be9b98534c5"


def frozen(path, expected):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f"Hash mismatch: {path.name}")
    if not os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_READONLY:
        raise ValueError(f"Input is writable: {path.name}")
    return raw


def category(source):
    if source.startswith(("snapshot/kanji/", "repo/kanji/", "snapshot/words/", "baseline/words/")):
        return "cards"
    if source == "repo/docs/jlpt-levels.md":
        return "jlpt"
    if source.startswith(("rubric/", "repo/docs/")) or source == "REVIEW.md":
        return "docs"
    if source.endswith("-extract.txt"):
        return "extract"
    if source.endswith("jmdict-families.xml"):
        return "jmdict"
    if source.endswith("kanjidic2-records.xml"):
        return "kanjidic"
    if source.endswith(("title-index.txt", "baseline-title-index.txt")):
        return "titleidx"
    return "evjson"


def telemetry(path, segments):
    by_path = {s["path"]: s for s in segments}
    previous = None
    pending = None
    first = None
    bootstrap = None
    generation = 0
    limits, models = set(), set()
    deltas, compactions, indices = {}, [], []
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for line in stream:
            digest.update(line)
            event = json.loads(line)
            kind, data = event.get("type"), event.get("data") or {}
            if kind in {"session.compaction_start", "session.compaction_complete"}:
                generation += 1
                allowed = ("currentTokens", "tokenLimit", "trigger", "preCompactionTokens",
                           "postCompactionTokens")
                compactions.append({"type": kind, "timestamp": event.get("timestamp"),
                                    **{k: data[k] for k in allowed if k in data}})
            elif kind == "session.usage_record":
                usage = data["usage"]
                tokens = usage["inputTokens"]
                if not isinstance(tokens, int) or tokens < 0:
                    raise ValueError("Invalid input-token telemetry")
                limits.add(usage.get("maxPromptTokens"))
                models.add(usage.get("responseModel"))
                if first is None:
                    first = tokens
                if pending is not None:
                    index, before, epoch = pending
                    delta = tokens - before
                    deltas[index] = delta if epoch == generation and delta >= 0 else None
                    pending = None
                previous = tokens
            elif kind == "tool.execution_start" and data.get("toolName") == "view":
                args = data.get("arguments") or {}
                if isinstance(args, str):
                    args = json.loads(args)
                segment = by_path.get(args.get("path"))
                if segment is not None:
                    if previous is None or pending is not None:
                        raise ValueError("Ambiguous usage/view boundary")
                    index = segment["index"]
                    if index in indices:
                        raise ValueError("Repeated core segment")
                    indices.append(index)
                    if bootstrap is None:
                        bootstrap = previous
                    pending = (index, previous, generation)
    if pending is not None:
        raise ValueError("No following usage record for final core view")
    if digest.hexdigest() != EVENTS_SHA:
        raise ValueError("Event stream differs from the frozen audit")
    return first, bootstrap, deltas, compactions, indices, sorted(limits), sorted(models)


def main(output):
    output = Path(output)
    if output.parent != REVIEW / "capacity" or output.exists():
        raise ValueError("Output must be a new direct child of review/capacity")
    calibration = json.loads(frozen(CALIBRATION, CALIBRATION_SHA))
    core = json.loads(frozen(CORE, CORE_SHA))
    if not os.stat(EVENTS).st_file_attributes & stat.FILE_ATTRIBUTE_READONLY:
        raise ValueError("Event snapshot is writable")
    segments = core["segments"]
    first, bootstrap, deltas, compactions, indices, limits, models = telemetry(EVENTS, segments)
    problems, rows = [], []
    if indices != [s["index"] for s in segments]:
        problems.append("View sequence differs from complete core order")
    if first != calibration["firstCallInputTokens"]:
        problems.append("First input-token value differs")
    if bootstrap != calibration["inputTokensBeforeSegment1"]:
        problems.append("Core bootstrap value differs")
    if limits != [calibration["maxPromptTokens"]]:
        problems.append("Prompt limits differ")
    if compactions != calibration["compactionEvents"]:
        problems.append("Compaction telemetry differs")
    recorded = {s["index"]: s for s in calibration["segments"]}
    if set(recorded) != set(indices):
        problems.append("Calibration segment membership differs")
    for segment in segments:
        raw = frozen(Path(segment["path"]), segment["sha256"])
        index = segment["index"]
        row = recorded.get(index, {})
        classes = sorted({category(p["source"]) for p in segment["parts"]})
        if (row.get("sha256") != segment["sha256"] or row.get("bytes") != len(raw)
                or row.get("measuredInputTokenDelta") != deltas.get(index)):
            problems.append(f"Segment {index} binding or delta differs")
        rows.append({"index": index, "bytes": len(raw), "classes": classes,
                     "inputTokenDelta": deltas.get(index),
                     "tokensPerByte": None if deltas.get(index) is None else deltas[index] / len(raw)})
    total = sum(v for v in deltas.values() if v is not None)
    missing = [i for i in indices if deltas.get(i) is None]
    if total != calibration["measuredCoreTokensExcludingCompactionSpan"]:
        problems.append("Measured core total differs")
    if missing != calibration["unmeasuredSegments"]:
        problems.append("Unmeasured segment set differs")
    ratios = {}
    for name in sorted({c for r in rows for c in r["classes"]}):
        samples = [r for r in rows if r["classes"] == [name] and r["inputTokenDelta"] is not None]
        if samples:
            ratios[name] = {
                "segments": len(samples),
                "weightedTokensPerByte": sum(r["inputTokenDelta"] for r in samples) / sum(r["bytes"] for r in samples),
                "maximumSegmentTokensPerByte": max(r["tokensPerByte"] for r in samples),
            }
    result = {
        "status": "PASS" if not problems else "FAIL", "problems": problems,
        "calibrationSha256": CALIBRATION_SHA, "coreSha256": CORE_SHA, "eventsSha256": EVENTS_SHA,
        "firstCallInputTokens": first, "coreBootstrapInputTokens": bootstrap,
        "actualResponseModels": models, "maxPromptTokens": limits,
        "compactions": compactions, "measuredCoreTokens": total, "unmeasuredSegments": missing,
        "pureClassRatios": ratios, "segments": rows,
        "limits": "Token telemetry only. Fitted coefficients, forecasts and future context acceptance are not certified. "
                  "No reviewer messages, summary content, choices or findings are emitted or used.",
    }
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    output.chmod(stat.S_IREAD)
    print(json.dumps({k: result[k] for k in ("status", "problems", "measuredCoreTokens",
                                           "unmeasuredSegments", "pureClassRatios")}))
    print("Record SHA256: " + hashlib.sha256(output.read_bytes()).hexdigest())
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
