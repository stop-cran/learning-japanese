"""Reproducible capacity estimates and hard pre-phase-2 gates, including selected dictionary evidence."""
import json
import math
from pathlib import Path

from b131_review_v2_common import CALIBRATION, CALIBRATION_SHA, FORECAST, HERE, PACKET, frozen, require, sha

CAP_OPTIONS = (40, 35, 30, 25, 20)
E_CAP = 10
BOOTSTRAP = 80000
REPORT_ALLOWANCE = 30000
STARTUP_GATE = 700000
PHASE2_GATE = 740000
CURRENT_OFFSET = 7000
FIT = {"docs": .354, "jlpt": .374, "cards": .502, "evjson": .522,
       "extract": .446, "jmdict": .543, "kanjidic": .526, "titleidx": .531}


def source_class(name):
    if name == "evidence/kanjidic2-review-projection.xml":
        return "kanjidic-projection", .65
    if name == "evidence/jmdict-review-core.xml":
        return "jmdict", FIT["jmdict"]
    if name == "repo/docs/jlpt-levels.md":
        return "jlpt", FIT["jlpt"]
    if name.endswith(("-extract.txt", "/extract.txt")):
        return "extract", FIT["extract"]
    if name in {"evidence/title-index.txt", "evidence/title-index-delta.txt"}:
        return "titleidx", FIT["titleidx"]
    if name.startswith(("snapshot/", "baseline/", "repo/kanji/", "repo/words/")) and name.endswith(".md"):
        return "cards", FIT["cards"]
    if name.startswith("evidence/") or name.startswith("snapshot/strokes/"):
        return "evjson", FIT["evjson"]
    return "docs", FIT["docs"]


def forecast_core(chain, calibration):
    require(calibration["fittedTokensPerByteNNLS"] == FIT, "Calibration fitted coefficients changed")
    measured = {row["sha256"]: row for row in calibration["segments"]
                if type(row.get("measuredInputTokenDelta")) is int}
    old = json.loads(frozen(calibration["coreChain"], calibration["coreChainSha256"]))
    old_segments = {row["index"]: row for row in old["segments"]}
    for row in calibration["segments"]:
        original = old_segments[row["index"]]
        require(original["sha256"] == row["sha256"] and original["bytes"] == row["bytes"],
                "Calibration is not bound to the exact original segment")
    results = []
    for segment in chain["segments"]:
        raw = frozen(segment["path"], segment["sha256"])
        if segment["sha256"] in measured:
            row = measured[segment["sha256"]]
            tokens = math.ceil(row["measuredInputTokenDelta"] * 1.05)
            results.append({"index": segment["index"], "sha256": sha(raw), "method": "identical-measured-x1.05",
                            "measuredDelta": row["measuredInputTokenDelta"], "tokens": tokens})
            continue
        lines, parts = raw.splitlines(keepends=True), []
        total = 0.0
        for part in segment["parts"]:
            payload = b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
            source = frozen(PACKET / part["source"], part["sha256"]).splitlines(keepends=True)
            require(payload == b"".join(source[part["a"] - 1:part["b"]]), "Segment source range changed")
            label, tpb = source_class(part["source"])
            contribution = len(payload) * tpb * 1.10
            total += contribution
            parts.append({"source": part["source"], "first": part["a"], "last": part["b"],
                          "bytes": len(payload), "class": label, "fittedTPB": tpb,
                          "margin": 1.10, "tokensUnrounded": contribution})
        results.append({"index": segment["index"], "sha256": sha(raw), "method": "part-class-x1.10",
                        "tokens": math.ceil(total), "parts": parts})
    return results


def extension_tokens(article_bytes, dictionary_bytes, article_count, dictionary_records):
    require(all(type(v) is int and v >= 0 for v in
                (article_bytes, dictionary_bytes, article_count, dictionary_records)), "Invalid extension cost")
    source_tokens = math.ceil((article_bytes + dictionary_bytes) * .55)
    headers = 1024 + article_count * 512 + dictionary_records * 128
    return {"articleBytes": article_bytes, "supplementalDictionaryBytes": dictionary_bytes,
            "articleCount": article_count, "supplementalRecords": dictionary_records,
            "sourceTPB": .55, "sourceTokens": source_tokens, "headerAllowanceTokens": headers,
            "headerMethod": "1024 fixed +512 per requested article +128 per supplemental complete record; "
                            "a conservative estimated allowance, not a context guarantee.",
            "tokens": source_tokens + headers}


def eligible_costs(sums, reference, catalog):
    new = set(reference["newCards"]) | set(reference["otherRequiredCards"])
    curated = {c for row in reference["cards"] for c in row["distractors"]}
    guards = {c for row in reference["cards"] for c in row["quiz_exclusions"]}
    articles = {Path(name).stem: (PACKET / name).stat().st_size for name in sums
                if name.startswith("repo/kanji/") and name.endswith(".md")}
    universe = set(articles) | {c for c in catalog if len(c) == 1 and "\u4e00" <= c <= "\u9fff"}
    result = {"D": [], "E": []}
    for char in sorted(universe):
        if char in new | curated:
            continue
        group = "E" if char in guards else "D"
        ids = catalog.get(char, {}).get("matchingRemainderIds", [])
        extra = sum((PACKET / f"evidence/jmdict-extension-records/{identity}.xml").stat().st_size
                    for identity in ids)
        cost = extension_tokens(articles.get(char, 0), extra, 1, len(ids))
        # Additive per-character scores intentionally overcount records shared by choices.
        score = (articles.get(char, 0) + extra) * .55 + 512 + len(ids) * 128
        result[group].append({"character": char, "articleBytes": articles.get(char, 0),
                              "supplementalDictionaryBytes": extra, "supplementalRecords": len(ids),
                              "dictionaryIds": ids, "score": score})
    return result


def choose_cap(core_tokens, eligible):
    trials = []
    for dcap in CAP_OPTIONS:
        selected = sorted(eligible["D"], key=lambda row: (-row["score"], row["character"]))[:dcap]
        selected += sorted(eligible["E"], key=lambda row: (-row["score"], row["character"]))[:E_CAP]
        extension = extension_tokens(
            sum(r["articleBytes"] for r in selected),
            sum(r["supplementalDictionaryBytes"] for r in selected), len(selected),
            sum(r["supplementalRecords"] for r in selected))
        peak = BOOTSTRAP + core_tokens + extension["tokens"] + REPORT_ALLOWANCE
        trials.append({"D": dcap, "E": E_CAP, "worstCaseExtension": extension,
                       "projectedWorstCasePeak": peak, "passes": peak <= STARTUP_GATE,
                       "selectionIndependentUpperBound": selected})
    chosen = next((trial for trial in trials if trial["passes"]), None)
    return trials, chosen


def compute_forecast(chain, calibration, sums, reference, catalog):
    segments = forecast_core(chain, calibration)
    core = sum(row["tokens"] for row in segments)
    eligible = eligible_costs(sums, reference, catalog)
    trials, chosen = choose_cap(core, eligible)
    return {
        "status": "PASS_CAPACITY_FORECAST" if chosen else "HOLD_NO_PERMITTED_CAP",
        "coreTokens": core, "segments": segments, "bootstrapTokens": BOOTSTRAP,
        "reportMessageAllowance": REPORT_ALLOWANCE, "startupGate": STARTUP_GATE,
        "prePhase2Gate": PHASE2_GATE, "currentTokenOffset": CURRENT_OFFSET,
        "chosenCaps": None if chosen is None else {"D": chosen["D"], "E": E_CAP},
        "projectedWorstCasePeak": None if chosen is None else chosen["projectedWorstCasePeak"],
        "trials": trials, "eligibleCounts": {key: len(rows) for key, rows in eligible.items()},
        "supplementalCostRequired": True,
        "worstCaseMethod": "Largest additive combined article-plus-exact-keb-remainder evidence costs "
                           "within each disjoint D/E eligibility class. Shared family records are "
                           "overcounted for a selection-independent upper bound. Actual extensions deduplicate.",
        "projectionTPB": ".65 class override, then the required x1.10 margin.",
        "limits": "Forecast is not a guarantee. Actual long-context identity, no compaction and the "
                  "pre-phase-2 actual-token plus selected-article/dictionary capacity gate remain mandatory."}


def load_forecast():
    result = json.loads(frozen(FORECAST))
    require(result["status"] == "PASS_CAPACITY_FORECAST" and result["projectedWorstCasePeak"] <= STARTUP_GATE
            and result["chosenCaps"]["D"] in CAP_OPTIONS and result["chosenCaps"]["E"] == E_CAP
            and result["supplementalCostRequired"] is True, "No passing frozen capacity forecast")
    return result


def telemetry(events, forecast):
    usages = [(event.get("data") or {}).get("usage") or {} for event in events
              if event.get("type") == "session.usage_record"]
    tokens = [usage.get("inputTokens") for usage in usages]
    compactions = [event["type"] for event in events
                   if str(event.get("type", "")).startswith("session.compaction")]
    errors = []
    if not tokens or any(type(value) is not int or value < 0 for value in tokens):
        errors.append("Missing/invalid actual inputTokens telemetry")
    if not usages or any(type(row.get("maxPromptTokens")) is not int or row["maxPromptTokens"] < 952000
                         for row in usages):
        errors.append("Actual context window is below the calibrated952000")
    if compactions:
        errors.append("Context compaction occurred")
    valid_tokens = [value for value in tokens if type(value) is int and value >= 0]
    peak = max(valid_tokens) if valid_tokens else None
    expected = forecast["bootstrapTokens"] + forecast["coreTokens"]
    return {"status": "HOLD" if errors else "PASS", "errors": errors, "compactions": compactions,
            "actualPeakInputTokens": peak, "actualPeakWithCurrentOffset": None if peak is None else peak + CURRENT_OFFSET,
            "lastInputTokens": valid_tokens[-1] if valid_tokens else None,
            "forecastPhase1Tokens": expected,
            "actualMinusForecast": None if peak is None else peak + CURRENT_OFFSET - expected}


def phase2_gate(events, forecast, extension):
    observed = telemetry(events, forecast)
    required = extension_tokens(extension["articleBytes"], extension["supplementalDictionaryBytes"],
                                extension["articleCount"], extension["supplementalRecords"])
    require(extension == required, "Actual extension capacity cost was altered or omitted")
    peak = None if observed["lastInputTokens"] is None else (
        observed["lastInputTokens"] + CURRENT_OFFSET + extension["tokens"] + REPORT_ALLOWANCE)
    passed = observed["status"] == "PASS" and peak is not None and peak <= PHASE2_GATE
    return {"status": "PASS_PRE_PHASE2_CAPACITY" if passed else "HOLD_PRE_PHASE2_CAPACITY",
            "sendPhase2Message": passed, "telemetry": observed, "extension": extension,
            "projectedPeak": peak, "gate": PHASE2_GATE, "reportAllowance": REPORT_ALLOWANCE}
