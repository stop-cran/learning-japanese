"""Exact model profiles and a predeclared stricter GPT004 gate; no forecast coefficient changes."""
import json

from b131_review_v4_common import (
    CORE, FORECAST, IMMUTABLE_BINDINGS, POLICY, TELEMETRY, TELEMETRY_SHA, frozen, require, sha)
from b131_capacity_002 import (
    BOOTSTRAP, CAP_OPTIONS, CURRENT_OFFSET, E_CAP, FIT, REPORT_ALLOWANCE, STARTUP_GATE,
    choose_cap, compute_forecast, eligible_costs, extension_tokens, forecast_core, source_class)

PROFILES = {
    "claude": {"selectedModel": "claude-opus-5.5", "maxPromptTokens": 952000, "prePhase2Gate": 740000},
    "gpt": {"selectedModel": "gpt-6.1-sol", "maxPromptTokens": 922000, "prePhase2Gate": 710000},
}
PHASE2_GATE = 710000


def load_forecast():
    verify_policy()
    value = json.loads(frozen(FORECAST, IMMUTABLE_BINDINGS[4][1]))
    require(value["status"] == "PASS_CAPACITY_FORECAST"
            and value["startupGate"] == STARTUP_GATE
            and value["projectedWorstCasePeak"] <= STARTUP_GATE
            and value["chosenCaps"] == {"D": 25, "E": 10}
            and value["supplementalCostRequired"] is True, "No passing unchanged startup forecast")
    return value


def verify_neutral_telemetry():
    raw = frozen(TELEMETRY, TELEMETRY_SHA)
    evidence = json.loads(raw)
    core = json.loads(frozen(CORE, IMMUTABLE_BINDINGS[2][1]))
    require(evidence["status"] == "VERIFIED_NEUTRAL_TELEMETRY_ONLY"
            and evidence["selectedModel"] == PROFILES["gpt"]["selectedModel"]
            and evidence["contextTier"] == "long_context"
            and evidence["maxPromptTokens"] == [PROFILES["gpt"]["maxPromptTokens"]]
            and evidence["compactions"] == []
            and evidence["coreChainSha256"] == IMMUTABLE_BINDINGS[2][1],
            "Neutral capacity evidence identity differs")
    require(len(evidence["segments"]) == len(core["segments"]) == 66, "Neutral segment count differs")
    for row, segment in zip(evidence["segments"], core["segments"]):
        require(all(row[key] == segment[key] for key in ("index", "sha256", "bytes"))
                and all(type(row[key]) is int and row[key] >= 0 for key in
                        ("inputTokensBefore", "inputTokensAfter", "measuredInputTokenDelta"))
                and row["inputTokensAfter"] - row["inputTokensBefore"] == row["measuredInputTokenDelta"],
                "Neutral core delta/chain binding differs")
    require(sum(row["measuredInputTokenDelta"] for row in evidence["segments"]) == 273135
            and evidence["measuredCoreTokens"] == 273135
            and evidence["actualPeakInputTokens"] == evidence["lastInputTokens"] == 322200,
            "Neutral measured totals differ")
    return {"path": str(TELEMETRY), "sha256": sha(raw), "coreSegments": 66,
            "maxPromptTokens": 922000, "actualPeakInputTokens": 322200, "measuredCoreTokens": 273135,
            "limits": "Capacity telemetry only. No prior review accepted/reclassified; no forecast reduction."}


def verify_policy():
    value = json.loads(frozen(POLICY))
    require(value["profiles"] == PROFILES and value["startupGate"] == STARTUP_GATE
            and value["forecastSha256"] == IMMUTABLE_BINDINGS[4][1]
            and value["neutralTelemetrySha256"] == TELEMETRY_SHA
            and value["forecastUnchanged"] is True, "Capacity policy changed")
    return value


def validate_capacity_config(config):
    require(config["capacityPolicySha256"] == sha(frozen(POLICY)), "Capacity policy binding changed")
    verify_policy()
    family = config["expectedFamily"]
    require(family in PROFILES and config["contextProfile"] == PROFILES[family],
            "Audit model/context profile differs")
    return PROFILES[family]


def telemetry(events, forecast, family=None):
    errors, usages, compactions, starts = [], [], [], []
    for event in events:
        if not isinstance(event, dict):
            errors.append("Invalid event shape")
            continue
        kind, data = event.get("type"), event.get("data") or {}
        if not isinstance(data, dict):
            errors.append("Invalid event data")
            continue
        if str(kind).startswith("session.compaction"):
            compactions.append(kind)
        if kind == "session.start":
            starts.append(data)
        if kind == "session.usage_record":
            usage = data.get("usage")
            if not isinstance(usage, dict):
                errors.append("Missing/invalid usage object")
            else:
                usages.append(usage)
    if family is None and len(starts) == 1:
        family = next((name for name, spec in PROFILES.items()
                       if spec["selectedModel"] == starts[0].get("selectedModel")), None)
    profile = PROFILES.get(family)
    if profile is None:
        errors.append("Unsupported/missing model context profile")
    if (len(starts) != 1 or starts[0].get("contextTier") != "long_context"
            or profile is None or starts[0].get("selectedModel") != profile["selectedModel"]):
        errors.append("Expected one exact selected model/long_context session.start")
    tokens = [usage.get("inputTokens") for usage in usages]
    limits = [usage.get("maxPromptTokens") for usage in usages]
    if not tokens or any(type(value) is not int or value < 0 for value in tokens):
        errors.append("Missing/invalid actual inputTokens telemetry")
    if (not usages or profile is None or any(type(value) is not int or value != profile["maxPromptTokens"]
                                              for value in limits)):
        errors.append("Actual context limits below-minimum, mixed, invalid or outside the declared exact profile")
    for usage in usages:
        for key in ("model", "responseModel"):
            model = usage.get(key)
            if model is not None and (not isinstance(model, str) or not family
                                      or not model.lower().startswith(family)):
                errors.append("Mixed/invalid usage model family")
        if (type(usage.get("inputTokens")) is int and type(usage.get("maxPromptTokens")) is int
                and usage["inputTokens"] > usage["maxPromptTokens"]):
            errors.append("Input tokens exceed the actual context limit")
    if compactions:
        errors.append("Context compaction occurred")
    valid = [value for value in tokens if type(value) is int and value >= 0]
    peak = max(valid) if valid else None
    expected = forecast["bootstrapTokens"] + forecast["coreTokens"]
    return {"status": "HOLD" if errors else "PASS", "errors": errors, "compactions": compactions,
            "family": family, "contextProfile": profile, "observedMaxPromptTokens": limits,
            "actualPeakInputTokens": peak, "actualPeakWithCurrentOffset": None if peak is None else peak + CURRENT_OFFSET,
            "lastInputTokens": valid[-1] if valid else None, "forecastPhase1Tokens": expected,
            "actualMinusForecast": None if peak is None else peak + CURRENT_OFFSET - expected}


def phase2_gate(events, forecast, extension, family=None):
    observed = telemetry(events, forecast, family)
    required = extension_tokens(extension["articleBytes"], extension["supplementalDictionaryBytes"],
                                extension["articleCount"], extension["supplementalRecords"])
    require(extension == required, "Actual extension capacity cost was altered or omitted")
    profile = observed["contextProfile"]
    limit = profile["prePhase2Gate"] if profile else None
    peak = None if observed["lastInputTokens"] is None else (
        observed["lastInputTokens"] + CURRENT_OFFSET + extension["tokens"] + REPORT_ALLOWANCE)
    passed = observed["status"] == "PASS" and peak is not None and peak <= limit
    return {"status": "PASS_PRE_PHASE2_CAPACITY" if passed else "HOLD_PRE_PHASE2_CAPACITY",
            "sendPhase2Message": passed, "telemetry": observed, "extension": extension,
            "projectedPeak": peak, "gate": limit, "reportAllowance": REPORT_ALLOWANCE}
