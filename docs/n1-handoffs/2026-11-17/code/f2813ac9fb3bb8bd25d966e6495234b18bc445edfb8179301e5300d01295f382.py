"""Bind lifecycle gates to the exact successor-011 meter and unchanged article bounds."""
import json
import sys
from pathlib import Path

from b134_common import (
    ARTICLE_BOUNDS, ARTICLE_BOUNDS_SHA, CAPACITY, CAPACITY_SHA, CORE_SHA, HERE,
    LOSSLESS_SHA, METER_AUDITS, METER_SHA, PREPARATION, PREPARATION_SHA,
    frozen, require, sha,
)

sys.path.insert(0, str(HERE / "tools"))
from capacity011_units import chain_cost, extension_upper

PROFILES = {
    "claude": {
        "selectedModel": "claude-opus-5.5", "contextTier": "long_context",
        "maxPromptTokens": 952000, "prePhase2Gate": 740000,
    },
    "gpt": {
        "selectedModel": "gpt-6.1-sol", "contextTier": "long_context",
        "maxPromptTokens": 922000, "prePhase2Gate": 710000,
    },
}
CAPS = ((25, 10), (20, 10), (15, 10), (10, 10), (10, 5))
BOOTSTRAP_ALLOWANCE = 80000
REPORT_ALLOWANCE = 30000
OPTIONAL_ALLOWANCE = 20000
STARTUP_GATE = 700000
CURRENT_OFFSET = 7000
EXPECTED_TRIALS = (
    (155395, 708147, "HOLD_ESTIMATE"),
    (133798, 686550, "PASS_ESTIMATE"),
    (111756, 664508, "PASS_ESTIMATE"),
    (88893, 641645, "PASS_ESTIMATE"),
    (74277, 627029, "PASS_ESTIMATE"),
)


def load_forecast():
    raw = frozen(CAPACITY, CAPACITY_SHA)
    record = json.loads(raw)
    require(record.get("purpose") == "capacity-forecast-only"
            and record.get("reviewAccepted") is False
            and record.get("coreManifestSha256") == CORE_SHA
            and record.get("chosenCaps") == {"D": 20, "E": 10}
            and len(record.get("trials", [])) == len(CAPS)
            and record.get("completionDeviations") == [],
            "Measured capacity binding differs")
    for (d_cap, e_cap), (article, startup, outcome), trial in zip(CAPS, EXPECTED_TRIALS, record["trials"]):
        require(trial.get("caps") == {"D": d_cap, "E": e_cap}
                and trial.get("measuredCoreBoundIncludingDrift") == 422752
                and trial.get("articleForecastIncludingEnvelopes") == article
                and trial.get("optionalReserve") == OPTIONAL_ALLOWANCE
                and trial.get("bootstrapAllowance") == BOOTSTRAP_ALLOWANCE
                and trial.get("reportAllowance") == REPORT_ALLOWANCE
                and trial.get("startupForecast") == startup
                and trial.get("outcome") == outcome
                and startup == 422752 + article + OPTIONAL_ALLOWANCE
                            + BOOTSTRAP_ALLOWANCE + REPORT_ALLOWANCE
                and outcome == ("PASS_ESTIMATE" if startup <= STARTUP_GATE else "HOLD_ESTIMATE"),
                "Capacity arithmetic or tier order differs")
    require(record["trials"][0]["outcome"] == "HOLD_ESTIMATE"
            and record["trials"][1]["outcome"] == "PASS_ESTIMATE"
            and all(row["outcome"] == "PASS_ESTIMATE" for row in record["trials"][1:]),
            "D20/E10 is not the first passing ceiling")
    for family, expected_path in METER_AUDITS.items():
        binding = record["measurements"][family]
        require(Path(binding["path"]) == expected_path and binding["sha256"] == METER_SHA[family],
                "Exact-core meter binding differs")
        frozen(expected_path, METER_SHA[family])
    require(record["preparation"] == {"path": str(PREPARATION), "sha256": PREPARATION_SHA},
            "Meter preparation binding differs")
    frozen(PREPARATION, PREPARATION_SHA)
    require(record["articleBounds"] == {"path": str(ARTICLE_BOUNDS), "sha256": ARTICLE_BOUNDS_SHA},
            "Article-bound evidence differs")
    bounds = json.loads(frozen(ARTICLE_BOUNDS, ARTICLE_BOUNDS_SHA))
    require(bounds["candidate"] == "355cccb840d22e7313e79f234eb93d1367e00352"
            and bounds["base"] == "ba80afffc20a72d31be68b355b6f90aab36a5726"
            and bounds["publishedBaseline"] == "e17cb97c53ca4e3193dae5e11b52ba517fe86e76",
            "Article bounds mix candidate or baseline identity")
    require(record["losslessVerification"]["sha256"] == LOSSLESS_SHA,
            "Lossless source verification binding differs")
    frozen(record["losslessVerification"]["path"], LOSSLESS_SHA)
    return record


def validate_capacity_config(config):
    require(config.get("capacityForecastSha256") == sha(frozen(CAPACITY, CAPACITY_SHA)),
            "Measured capacity evidence binding differs")
    family = config["expectedFamily"]
    require(family in PROFILES and config.get("contextProfile") == PROFILES[family],
            "Explicit model/context profile differs")
    return PROFILES[family]


def startup_bound(forecast, family, prompt_bytes):
    require(family in PROFILES and type(prompt_bytes) is int and 0 < prompt_bytes <= 40000,
            "Invalid profile or unbudgeted instruction size")
    chosen = next(row for row in forecast["trials"] if row["caps"] == {"D": 20, "E": 10})
    upper = chosen["startupForecast"]
    return {
        "status": "PASS_ESTIMATE" if upper <= STARTUP_GATE else "HOLD_ESTIMATE",
        "estimatedUpper": upper, "limit": STARTUP_GATE,
        "coreBound": chosen["measuredCoreBoundIncludingDrift"],
        "articleForecast": chosen["articleForecastIncludingEnvelopes"],
        "optionalReserve": chosen["optionalReserve"],
        "bootstrapAllowance": chosen["bootstrapAllowance"],
        "reportAllowance": chosen["reportAllowance"],
        "selectedCaps": {"D": 20, "E": 10},
        "headroom": STARTUP_GATE - upper,
        "promptBytes": prompt_bytes,
        "method": "Exact-core token growth measured in both current families; larger growth plus 10% and 12000 drift; unchanged full-article bounds and reserves.",
        "limits": "Conservative forecast, not a tokenizer guarantee or reviewer admission; exact runtime profile and zero-compaction gates still apply.",
    }


def telemetry(events, forecast, family, session=None):
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
    if (profile is None or len(starts) != 1
            or starts[0].get("selectedModel") != profile["selectedModel"]
            or starts[0].get("contextTier") != "long_context"
            or session is not None and starts[0].get("sessionId") != session):
        errors.append("Expected one exact selected model/long_context session.start")
    tokens = [usage.get("inputTokens") for usage in usages]
    limits = [usage.get("maxPromptTokens") for usage in usages]
    if not tokens or any(type(value) is not int or value < 0 for value in tokens):
        errors.append("Missing/invalid actual inputTokens")
    if (not limits or profile is None
            or any(type(value) is not int or value != profile["maxPromptTokens"] for value in limits)):
        errors.append("Missing/invalid actual maxPromptTokens")
    for usage in usages:
        if usage.get("model") is not None and usage["model"] != profile["selectedModel"]:
            errors.append("Usage model differs from selected model")
        if usage.get("responseModel") is not None and usage["responseModel"] != profile["selectedModel"]:
            errors.append("Usage response model differs from selected model")
        if (type(usage.get("inputTokens")) is int and type(usage.get("maxPromptTokens")) is int
                and usage["inputTokens"] > usage["maxPromptTokens"]):
            errors.append("Actual input exceeds context")
    if compactions:
        errors.append("Context compaction occurred")
    valid = [value for value in tokens if type(value) is int and value >= 0]
    return {
        "status": "HOLD" if errors else "PASS", "errors": errors,
        "compactions": compactions, "family": family, "contextProfile": profile,
        "observedMaxPromptTokens": limits,
        "actualPeakInputTokens": max(valid) if valid else None,
        "lastInputTokens": valid[-1] if valid else None,
    }


def phase2_gate(events, forecast, extension_tokens, family, session=None):
    require(type(extension_tokens) is int and 0 <= extension_tokens <= OPTIONAL_ALLOWANCE
            + next(row["articleForecastIncludingEnvelopes"] for row in forecast["trials"]
                   if row["caps"] == {"D": 20, "E": 10}),
            "Extension forecast bound exceeded")
    observed = telemetry(events, forecast, family, session)
    projected = None if observed["lastInputTokens"] is None else (
        observed["lastInputTokens"] + CURRENT_OFFSET + extension_tokens + REPORT_ALLOWANCE)
    limit = PROFILES[family]["prePhase2Gate"]
    passed = observed["status"] == "PASS" and projected is not None and projected <= limit
    return {
        "status": "PASS_PRE_PHASE2_CAPACITY" if passed else "HOLD_PRE_PHASE2_CAPACITY",
        "sendPhase2Message": passed, "telemetry": observed, "extensionTokens": extension_tokens,
        "projectedPeak": projected, "limit": limit,
        "formula": "lastInputTokens + 7000 + selected-extension-forecast + 30000",
        "limits": "Uses observed runtime input and conservative full-article/optional-unit bounds; any compaction invalidates.",
    }
