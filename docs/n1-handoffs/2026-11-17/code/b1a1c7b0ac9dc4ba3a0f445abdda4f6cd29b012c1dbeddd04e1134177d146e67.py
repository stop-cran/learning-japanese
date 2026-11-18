"""Use the already verified B133 calibration on exact complete confirmation sources."""
import math

from common import frozen, require, sha


def confirmation_cost(chain):
    from b133_capacity import chain_cost, load_forecast
    from capacity004_units import source_tokens

    load_forecast()
    rows = chain["sources"]
    names = [row["source"] for row in rows]
    require(len(names) == len(set(names)) and names, "Duplicate or missing confirmation sources")
    rebuilt = {name: b"" for name in names}
    next_line = dict.fromkeys(names, 1)
    identities = {row["source"]: row for row in rows}
    for index, segment in enumerate(chain["segments"], 1):
        raw = frozen(segment["path"], segment["sha256"])
        require(segment["index"] == index and len(raw) == segment["bytes"] < 16000,
                "Confirmation segment exceeds the verified bound")
        lines = raw.splitlines(keepends=True)
        for part in segment["parts"]:
            name = part["source"]
            require(name in identities and part["a"] == next_line[name]
                    and part["sha256"] == identities[name]["sha256"], "Source identity/order differs")
            value = b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
            require(len(value.splitlines()) == part["b"] - part["a"] + 1, "Source range differs")
            rebuilt[name] += value
            next_line[name] = part["b"] + 1
    for name, raw in rebuilt.items():
        row = identities[name]
        require(sha(raw) == row["sha256"] == row["selectedSha256"]
                and len(raw.splitlines()) == row["sourceLines"] == row["selectedLines"],
                "Confirmation source is incomplete or changed")
    sources = [(name, rebuilt[name], None) for name in names]
    result = chain_cost(chain, sources)
    # Original review prose is not one of the source classes in the calibration.
    adjustment = sum(len(raw) - source_tokens(name, raw) for name, raw, _ in sources
                     if name.startswith("initial-report/"))
    require(adjustment >= 0, "Invalid report allowance")
    result["tokens"] += adjustment
    result["reportFallbackTokens"] = adjustment
    result["envelopeTokens"] = math.ceil(result["envelopeBytes"] * .574)
    result["method"] = (
        "Exact reconstructed source bytes with existing verified B133 source-class fit x1.10; "
        "envelopes .574 tokens/byte; original report conservatively one token/byte. "
        "Unchanged 700000 startup gate, 12000 drift and 30000 report reserves. "
        "Forecast only; original-reviewer live telemetry and zero compactions remain mandatory."
    )
    return result
