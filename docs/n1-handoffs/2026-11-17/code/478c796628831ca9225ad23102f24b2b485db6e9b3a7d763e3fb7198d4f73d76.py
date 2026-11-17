"""Calibrated forecasts; actual runtime identity and pre-compaction gates remain mandatory."""
import json
import sys
from b134_common import FORECAST, FORECAST_SHA, HERE, frozen, require, sha

sys.path.insert(0, str(HERE / "tools"))
from capacity004_units import chain_cost, extension_upper

PROFILES = {
    "claude": {"selectedModel": "claude-opus-5.5", "contextTier": "long_context",
               "maxPromptTokens": 952000, "prePhase2Gate": 740000},
    "gpt": {"selectedModel": "gpt-6.1-sol", "contextTier": "long_context",
            "maxPromptTokens": 922000, "prePhase2Gate": 710000},
}
BOOTSTRAP_ALLOWANCE = 80000
REPORT_ALLOWANCE = 30000
STARTUP_GATE = 700000
CURRENT_OFFSET = 7000


def load_forecast():
    record = json.loads(frozen(FORECAST, FORECAST_SHA))
    require(record["status"] == "MEASURED_NOT_ADMITTED"
            and record["decision"] in ("PASS_ESTIMATE", "HOLD_ESTIMATE")
            and record["chosenCaps"] is None
            and len(record["trials"]) == 5
            and all(row["outcome"] == "HOLD_ESTIMATE" for row in record["trials"])
            and record["optionalUnitAllowance"] == 20000
            and record["optionalUnitAllowance"] >= record["largestOptionalUnitTokens"]
            and len(record["optionalUnits"]) == 88,
            "Capacity evidence differs")
    return record


def validate_capacity_config(config):
    require(config.get("capacityForecastSha256") == sha(frozen(FORECAST, FORECAST_SHA)),
            "Capacity evidence binding differs")
    family = config["expectedFamily"]
    require(family in PROFILES and config.get("contextProfile") == PROFILES[family],
            "Model profile differs")
    return PROFILES[family]


def startup_bound(forecast, family, prompt_bytes):
    require(family in PROFILES and type(prompt_bytes) is int and 0 < prompt_bytes <= 40000,
            "Invalid profile or unbudgeted instruction size")
    largest_trial = forecast["trials"][0]
    upper = largest_trial["startupForecast"]
    return {"status": "PASS_ESTIMATE" if forecast["decision"] == "PASS_ESTIMATE"
            and forecast["chosenCaps"] and upper <= STARTUP_GATE else "HOLD_ESTIMATE",
            "estimatedUpper": upper, "limit": STARTUP_GATE,
            "method": "B131 fit x1.10; all envelope bytes .574; complete optional KD records .60TPB. "
                      "80k bootstrap includes instruction read, as in numeric B132 bootstrap telemetry.",
            "limits": "Forecast, not observed current tokenizer usage or a guarantee; runtime gates required."}


def telemetry(events, forecast, family):
    errors, usages, starts, compactions = [], [], [], []
    for event in events:
        if not isinstance(event, dict) or not isinstance(event.get("data") or {}, dict):
            errors.append("Invalid event shape")
            continue
        kind, data = event.get("type"), event.get("data") or {}
        if str(kind).startswith("session.compaction"):
            compactions.append(kind)
        if kind == "session.start":
            starts.append(data)
        if kind == "session.usage_record":
            usage = data.get("usage")
            if not isinstance(usage, dict):
                errors.append("Invalid usage telemetry")
            else:
                usages.append(usage)
    profile = PROFILES.get(family)
    if (profile is None or len(starts) != 1 or starts[0].get("selectedModel") != profile["selectedModel"]
            or starts[0].get("contextTier") != profile["contextTier"]):
        errors.append("Expected one exact selected model/long_context session.start")
    tokens = [u.get("inputTokens") for u in usages]
    limits = [u.get("maxPromptTokens") for u in usages]
    if not tokens or any(type(n) is not int or n < 0 for n in tokens):
        errors.append("Missing/invalid actual inputTokens")
    if not limits or profile is None or any(type(n) is not int or n != profile["maxPromptTokens"] for n in limits):
        errors.append("Missing/invalid actual context limit")
    for usage in usages:
        for key in ("model", "responseModel"):
            value = usage.get(key)
            if value is not None and value != profile["selectedModel"]:
                errors.append("Mixed or invalid selected model")
        if (type(usage.get("inputTokens")) is int and type(usage.get("maxPromptTokens")) is int
                and usage["inputTokens"] > usage["maxPromptTokens"]):
            errors.append("Actual input exceeds context")
    if compactions:
        errors.append("Context compaction occurred")
    valid = [n for n in tokens if type(n) is int and n >= 0]
    return {"status": "HOLD" if errors else "PASS", "errors": errors, "compactions": compactions,
            "family": family, "contextProfile": profile, "observedMaxPromptTokens": limits,
            "actualPeakInputTokens": max(valid) if valid else None,
            "lastInputTokens": valid[-1] if valid else None}


def phase2_gate(events, forecast, extension_tokens, family):
    require(type(extension_tokens) is int and 0 <= extension_tokens <= forecast["maximumExtensionTokens"],
            "Extension forecast bound exceeded")
    observed = telemetry(events, forecast, family)
    peak = None if observed["lastInputTokens"] is None else (
        observed["lastInputTokens"] + CURRENT_OFFSET + extension_tokens + REPORT_ALLOWANCE)
    limit = PROFILES[family]["prePhase2Gate"]
    passed = observed["status"] == "PASS" and peak is not None and peak <= limit
    return {"status": "PASS_PRE_PHASE2_CAPACITY" if passed else "HOLD_PRE_PHASE2_CAPACITY",
            "sendPhase2Message": passed, "telemetry": observed, "extensionTokens": extension_tokens,
            "projectedPeak": peak, "limit": limit,
            "limits": "Actual last input plus calibrated selected-source forecast; any compaction invalidates."}
