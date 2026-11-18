"""Measure complete-record-first B134 capacity with corrected inherited source classes."""
import json
import math
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
OUT = ROOT / "fresh-independent-002" / "projected-successor-008"
PACKET = OUT / "packet"
FULL_TRIAL = OUT / "complete-record-trial-009"
sys.path.insert(0, str(WS / "review-tools"))
sys.path.insert(0, str(OUT / "tools"))
sys.path.insert(0, str(OUT / "protocol-003"))

from common import require, sha, start_guard, write_frozen
from capacity008 import CAPS, project, source_class, xml_bytes
from capacity008_units import chain_cost, extension_upper, source_tokens
from review_chain_with_optional import build_chain

STARTUP_GATE = 700000
BOOTSTRAP = 80000
REPORT = 30000
OPTIONAL = 20000
EXCLUSIONS = 56


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def eligibility(files):
    card = files["repo/kanji/紫.md"].decode("utf-8")
    frontmatter = card.split("---", 2)[1]
    exclusion_line = next(line for line in frontmatter.splitlines() if line.startswith("quiz_exclusions:"))
    exclusions = [x.strip() for x in exclusion_line.split(":", 1)[1].strip().strip("[]").split(",") if x.strip()]
    ref = json.loads(files["eligibility-reference.json"])
    require(ref["cards"][0]["quiz_exclusions"] == exclusions and len(exclusions) == EXCLUSIONS,
            "Exclusion list/reference differs from signed card")
    excluded = set(exclusions) | set(ref["newCards"]) | set(ref["otherRequiredCards"])
    distractors = {c for row in ref["cards"] for c in row["distractors"]}
    excluded |= distractors
    targets = set(exclusions) - set(ref["newCards"])
    d_rows, e_rows = [], []
    for name, raw in files.items():
        if not (name.startswith("repo/kanji/") and name.endswith(".md")):
            continue
        char = Path(name).stem
        cost = extension_upper([(name, raw, None)])["tokens"]
        if char in targets:
            e_rows.append((cost, name, raw))
        elif char not in excluded:
            d_rows.append((cost, name, raw))
    require(len(e_rows) == EXCLUSIONS and len(d_rows) >= 1, "D/E eligible pool is incomplete")
    return d_rows, e_rows


def trial_capacity(core_cost, files):
    d_rows, e_rows = eligibility(files)
    trials = []
    for d, e in CAPS:
        chosen = sorted(d_rows, reverse=True)[:d] + sorted(e_rows, reverse=True)[:e]
        extension = extension_upper([(name, raw, None) for _, name, raw in chosen])
        startup = core_cost["tokens"] + extension["tokens"] + OPTIONAL + BOOTSTRAP + REPORT
        trials.append({
            "caps": {"D": d, "E": e},
            "articleBytes": extension["payloadBytes"],
            "articleForecastIncludingEnvelopes": extension["tokens"],
            "optionalReserve": OPTIONAL, "startupForecast": startup,
            "excess": max(0, startup - STARTUP_GATE),
            "outcome": "PASS_ESTIMATE" if startup <= STARTUP_GATE else "HOLD_ESTIMATE",
        })
    return trials, len(d_rows), len(e_rows)


def class_summary(sources):
    counts, bytes_by_class, tokens_by_class, mapping = Counter(), Counter(), Counter(), []
    for name, raw, _ in sources:
        kind, coefficient = source_class(name)
        cost = source_tokens(name, raw)
        counts[kind] += 1
        bytes_by_class[kind] += len(raw)
        tokens_by_class[kind] += cost
        mapping.append({"source": name, "class": kind, "coefficient": coefficient,
                        "bytes": len(raw), "tokens": cost})
    return {
        "counts": dict(counts), "bytes": dict(bytes_by_class), "tokens": dict(tokens_by_class),
        "sources": mapping,
        "correctedMappings": [
            row for row in mapping if row["source"].startswith(
                ("reconciliation/evidence/native-", "reconciliation/checks/"))
        ],
    }


def make_core(names, label, guard, directory, manifest_name):
    sources = [(name, (PACKET / name).read_bytes(), None) for name in names]
    manifest_path = directory / manifest_name
    chain = build_chain(sources, directory / "chains" / (label + "-001"),
                        manifest_path, guard, label)
    return chain, sources, chain_cost(chain, sources)


def main():
    if FULL_TRIAL.exists() or (OUT / "core-chain-002.json").exists():
        raise RuntimeError("Capacity output already exists; preserve it and use a new successor")
    core_spec = json.loads((OUT / "core-sources-002.json").read_text(encoding="utf-8"))
    names = list(core_spec["sources"])
    sums = json.loads((PACKET / "SHA256SUMS.json").read_text(encoding="utf-8"))
    files = {name: (PACKET / name).read_bytes() for name in sums}
    require(set(names) <= set(files), "Core contains an unlisted packet source")
    require("evidence/kanjidic2-review-projection.xml" in names
            and "evidence/kanjidic2-complete-union.xml" in files
            and "evidence/kanjidic2-full-unit-index.json" in names,
            "Full union, projection or full-unit index missing")

    guard, _ = start_guard("B134 complete-record-first successor 008 forecast")
    try:
        FULL_TRIAL.mkdir(parents=True)
        full_names = list(names)
        full_names[full_names.index("evidence/kanjidic2-review-projection.xml")] = \
            "evidence/kanjidic2-complete-union.xml"
        full_chain, full_sources, full_cost = make_core(
            full_names, "complete-record-core-008", guard, FULL_TRIAL, "core-full-record-008.json")
        full_trials, eligible_d, eligible_e = trial_capacity(full_cost, files)
        full_classes = class_summary(full_sources)
        full_record = {
            "status": "MEASURED_COMPLETE_RECORDS_BEFORE_PROJECTION",
            "candidate": core_spec["candidate"], "base": core_spec["base"],
            "publishedBaseline": core_spec["publishedBaseline"],
            "representation": "Complete 522 JMdict families and complete 85-record KANJIDIC2 union in forecast-only core.",
            "sourceRecords": len(full_sources), "segments": len(full_chain["segments"]),
            "segmentBytes": full_cost["chainBytes"], "payloadBytes": full_cost["payloadBytes"],
            "envelopeBytes": full_cost["envelopeBytes"], "coreTokens": full_cost["tokens"],
            "recordCounts": {"jmdict": 522, "kanjidic2": 85},
            "eligibleD": eligible_d, "eligibleE": eligible_e,
            "sourceClassification": full_classes, "trials": full_trials,
            "limits": "Conservative forecast only; no reviewer admission or launch. Full KD file is measured before the only permitted fallback.",
        }
        write_frozen(FULL_TRIAL / "capacity-full-record-008.json", json_bytes(full_record))
        full_first_pass = next((row for row in full_trials if row["outcome"] == "PASS_ESTIMATE"), None)
        if full_first_pass:
            final_names = full_names
            representation = "COMPLETE_RECORDS"
            optional_units = []
        else:
            full_union = files["evidence/kanjidic2-complete-union.xml"]
            projected_raw = xml_bytes(project(full_union))
            projected_path = PACKET / "evidence" / "kanjidic2-review-projection.xml"
            if projected_path.read_bytes() != projected_raw:
                raise RuntimeError("Existing KD projection is not the prescribed exact projection")
            full_root = ET.fromstring(full_union)
            lines = full_union.splitlines(keepends=True)[1:-1]
            unit_rows = []
            for node, raw in zip(full_root, lines):
                literal = node.findtext("literal")
                path = f"evidence/kanjidic2-full-records/{literal}.xml"
                if files[path] != raw:
                    raise RuntimeError("Full KD unit is not the exact complete record: " + literal)
                unit_rows.append((path, raw, None))
            if len(unit_rows) != 85:
                raise RuntimeError("Full KD optional-unit inventory is incomplete")
            optional_units = unit_rows + [
                (name, files[name], None)
                for name in ("evidence/xml-presentation.json", "evidence/font-cmap.json",
                             "evidence/dictionary-index.json")
            ]
            final_names = list(names)
            representation = "PRESCRIBED_B133_004_KD_FIELD_PROJECTION"

        final_chain, final_sources, final_cost = make_core(
            final_names, "fresh-independent-core-009", guard, OUT, "core-chain-002.json")
        final_trials, eligible_d, eligible_e = trial_capacity(final_cost, files)
        chosen = next((row for row in final_trials if row["outcome"] == "PASS_ESTIMATE"), None)
        if not chosen and representation != "PRESCRIBED_B133_004_KD_FIELD_PROJECTION":
            raise RuntimeError("Complete records hold but the prescribed projection was not measured")
        optional_rows = []
        for name, raw, _ in optional_units:
            optional_rows.append({
                "unit": name, "sha256": sha(raw), "bytes": len(raw),
                "forecastUpperTokens": extension_upper([(name, raw, None)])["tokens"],
            })
        if optional_rows and max(row["forecastUpperTokens"] for row in optional_rows) > OPTIONAL:
            raise RuntimeError("A complete optional unit exceeds the unchanged shared allowance")
        capacity = {
            "status": "MEASURED_NOT_ADMITTED",
            "decision": "PASS_ESTIMATE" if chosen else "HOLD_ESTIMATE",
            "candidate": core_spec["candidate"], "base": core_spec["base"],
            "publishedBaseline": core_spec["publishedBaseline"],
            "representation": representation,
            "completeRecordTrial": {
                "sourceRecords": len(full_sources), "segments": len(full_chain["segments"]),
                "chainBytes": full_cost["chainBytes"], "payloadBytes": full_cost["payloadBytes"],
                "envelopeBytes": full_cost["envelopeBytes"], "coreTokens": full_cost["tokens"],
                "trials": full_trials,
            },
            "finalCoreSources": len(final_sources), "finalCoreSegments": len(final_chain["segments"]),
            "finalChainBytes": final_cost["chainBytes"], "finalPayloadBytes": final_cost["payloadBytes"],
            "finalEnvelopeBytes": final_cost["envelopeBytes"], "coreTokens": final_cost["tokens"],
            "maxSegmentBytes": max(row["bytes"] for row in final_chain["segments"]),
            "eligibleArticleCounts": {"D": eligible_d, "E": eligible_e},
            "trials": final_trials, "chosenCaps": chosen["caps"] if chosen else None,
            "optionalUnitAllowance": OPTIONAL, "optionalUnits": optional_rows,
            "largestOptionalUnitTokens": max((row["forecastUpperTokens"] for row in optional_rows), default=0),
            "maximumExtensionTokens": (
                chosen["articleForecastIncludingEnvelopes"] + OPTIONAL if chosen else None),
            "packetManifestSha256": sha((PACKET / "SHA256SUMS.json").read_bytes()),
            "packetFiles": len(sums), "startupGate": STARTUP_GATE,
            "bootstrapTokens": BOOTSTRAP, "reportTokens": REPORT,
            "prePhase2Gates": {"claude": 740000, "gpt": 710000},
            "profiles": {
                "claude": {"selectedModel": "claude-opus-5.5", "contextTier": "long_context",
                           "maxPromptTokens": 952000},
                "gpt": {"selectedModel": "gpt-6.1-sol", "contextTier": "long_context",
                        "maxPromptTokens": 922000},
            },
            "sourceClassification": class_summary(final_sources),
            "sourceClassRule": "Inherited coefficients x1.10 unchanged; nested reconciliation extract/check paths explicitly mapped to extract/check classes.",
            "limits": "Forecast, not measured tokenizer usage. No tier/source reduction. Actual model, explicit long_context, exact usage profile, event-snapshot binding, and zero-compaction authorization remain mandatory before chain delivery.",
        }
        write_frozen(OUT / "capacity-measurement-002.json", json_bytes(capacity))
        print(json.dumps({
            "status": capacity["decision"], "representation": representation,
            "packetFiles": len(sums), "coreSources": len(final_sources),
            "fullRecordD25E10": full_trials[0]["startupForecast"],
            "fullRecordTrials": full_trials,
            "finalCoreTokens": final_cost["tokens"], "finalTrials": final_trials,
            "eligible": {"D": eligible_d, "E": eligible_e},
            "optionalCount": len(optional_rows),
            "largestOptionalUnitTokens": capacity["largestOptionalUnitTokens"],
            "packetManifestSha256": capacity["packetManifestSha256"],
        }, ensure_ascii=False))
    finally:
        require(not guard.finish()["breach"], "Capacity forecast RAM breach")


if __name__ == "__main__":
    main()
