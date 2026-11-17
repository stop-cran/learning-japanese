"""Measure the complete-record core first; apply only the prescribed fallback."""
import importlib.util
import json
import math
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
PREP = ROOT / "neutral-preparation-001"
OLD = WS / "scratch-133" / "review" / "neutral-preparation-004" / "successor-002"
FULL = PREP / "complete-record-trial-003"
sys.path.insert(0, str(WS / "review-tools"))
from common import freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen


def load(path):
    return json.loads(frozen(path))


def derive_tools():
    for name in ("capacity004.py", "capacity004_units.py"):
        raw = frozen(OLD / "tools" / name)
        text = raw.decode().replace("len(root) != 83", "len(root) != 59")
        path = PREP / "tools" / name
        if path.exists():
            require(frozen(path) == text.encode(), "Existing derived tool differs")
        else:
            write_frozen(path, text.encode())
    raw = frozen(OLD / "protocol-003" / "review_chain_with_optional.py")
    text = raw.decode()
    text = text[:text.index("\n\nOPTIONAL_UNITS =")]
    path = PREP / "tools" / "chain_b134_initial.py"
    if path.exists():
        require(frozen(path) == text.encode(), "Existing chain tool differs")
    else:
        write_frozen(path, text.encode())


def trials_for(files, names, target, guard, label):
    from capacity004_units import CAPS, chain_cost, extension_upper, source_class, source_tokens
    from chain_b134_initial import build_chain
    sources = [(n, files[n], None) for n in names]
    chain = build_chain(sources, target / "chains" / "core-001", target / "core-chain-001.json", guard, label)
    cost = chain_cost(chain, sources)
    ref = json.loads(files["eligibility-reference.json"])
    excluded = set(ref["newCards"]) | set(ref["otherRequiredCards"]) | {
        c for row in ref["cards"] for c in row["distractors"]}
    targets = {c for row in ref["cards"] for c in row["quiz_exclusions"]} - excluded
    eligible = {"D": [], "E": []}
    for name, raw in files.items():
        if name.startswith("repo/kanji/") and name.endswith(".md") and Path(name).stem not in excluded:
            eligible["E" if Path(name).stem in targets else "D"].append(
                (extension_upper([(name, raw, None)])["tokens"], name, raw))
    trials = []
    for d, e in CAPS:
        rows = sorted(eligible["D"], reverse=True)[:d] + sorted(eligible["E"], reverse=True)[:e]
        upper = extension_upper([(n, raw, None) for _, n, raw in rows])
        peak = cost["tokens"] + upper["tokens"] + 20000 + 80000 + 30000
        trials.append({"caps": {"D": d, "E": e}, "articleUpper": upper, "startupPeak": peak,
                       "optionalUnitAllowance": 20000, "excess": max(0, peak - 700000),
                       "passes": peak <= 700000})
    return chain, {
        "status": "MEASURED_NOT_ADMITTED", "batch": 134,
        "coreSources": len(names), "coreSegments": len(chain["segments"]),
        "coreSegmentBytes": cost["chainBytes"], "coreTokens": cost["tokens"], "coreCost": cost,
        "maxSegmentBytes": max(s["bytes"] for s in chain["segments"]),
        "trials": trials, "eligibleArticleCounts": {k: len(v) for k, v in eligible.items()},
        "perSource": [{"source": n, "bytes": len(raw), "sha256": sha(raw), "class": source_class(n)[0],
                       "tpb": source_class(n)[1], "tokens": source_tokens(n, raw)} for n, raw, _ in sources]}


def main():
    guard, _ = start_guard("B134 complete-record-first measured capacity")
    try:
        derive_tools()
        sys.path.insert(0, str(PREP / "tools"))
        from capacity004_units import DERIVED, extension_upper, full_units, project, xml_bytes
        full_build = load(FULL / "packet-build.json")
        sums = load(FULL / "packet" / "SHA256SUMS.json")
        files = {n: frozen(FULL / "packet" / n, d) for n, d in sums.items()}
        full_names = full_build["coreSources"]
        chain, measure = trials_for(files, full_names, FULL, guard, "B134 complete-record core")
        # B133's unchanged full-KD source class uses the conservative 1.0 bound.
        measure["fullKDCoefficientDisclosure"] = "B133 capacity004 full-kd class 1.0; no invented full-record fit."
        full_measure = freeze_json(FULL / "complete-record-capacity-001.json", measure)
        if measure["trials"][0]["passes"]:
            target, names, units = FULL, full_names, {}
            chosen = measure["trials"][0]
            representation = "FULL_COMPLETE_RECORDS_UNCHANGED"
        else:
            target = PREP / "projected-successor-001"
            require(not target.exists(), "Preserve projected successor")
            full_kd = files["evidence/kanjidic2-records.xml"]
            projected = xml_bytes(project(full_kd))
            files["evidence/kanjidic2-review-projection.xml"] = projected
            units = full_units(full_kd)
            files.update(units)
            names = [n for n in full_names if n not in DERIVED]
            names[names.index("evidence/kanjidic2-records.xml")] = "evidence/kanjidic2-review-projection.xml"
            disclosure = """## B134 prescribed representation and capacity disclosure

All 399 complete JMdict families and every field remain in core, without trimming.
All 59 KANJIDIC2 records remain in original order as a mechanical per-field
projection. Drop only codepoint, dic_number, query_code; meanings with non-English
m_lang; and readings with r_type pinyin/korean_r/korean_h/vietnam. Retain literal,
radical, all misc, Japanese readings with attributes, English meanings and nanori.
The complete original union and all four original selections remain preserved.
Complete query predicates, provenance and zero matches are in the core.

The full KD file is outside the chain and NOT authorized as a whole-file read.
Each complete original KD record is separately requestable by K:<literal>.
Three whole derived-index optional units are evidence/xml-presentation.json,
evidence/font-cmap.json and evidence/dictionary-index.json. Request zero or more
distinct units using consecutive O1..O62, exact unit, space-hyphen-space and reason,
or O: none. Units reach you only through the phase-2 chain after D/E articles.
All 62 units individually fit the shared 20000-token optional reserve, including
payload and conservative envelopes. Multiple units must fit the summed reserve.
No truncation, substitution, ignored request, reselection or partial extension:
excess is HOLD/UNVERIFIED before phase 2; necessary unread evidence prevents closure.
Original raw XML selections and raw captures are provenance, not extra O units.

The complete candidate title index plus exact one-line deletion delta represents
the entire baseline; the raw baseline is preserved outside core. Disclose that,
not a fictional raw-baseline read. Missing historical glyph images are unavailable.

Forecasts are not actual token measurements or guarantees. B131 fitted coefficients
x1.10: docs .354, jlpt .374, cards .502, evjson .522, extract .446, JMdict .543,
titleidx .531; KD projection .65 x1.10; complete optional KD .60 per payload byte.
Every JSON, all diffs/checks use evjson; all chain/extension envelopes use .574.
Bootstrap80000 includes instructions; report30000; optional20000; startup700000.
Try D25/E10,D20/E10,D15/E10,D10/E10,D10/E5 in order; use first passing pair.
Actual exact model/long_context, zero compaction and complete core audit required.
Before phase2: lastInputTokens+7000+selected-extension-forecast+30000 must not exceed
740000 Claude or710000 GPT; otherwise HOLD without sending phase2.
This preparation is not teaching, rendering, native/device, whole-set or publication
acceptance. No reviewer is launched by any preparation or protocol command.
"""
            files["REVIEW.md"] += ("\n" + disclosure).encode()
            files["DISCLOSURE.txt"] = disclosure.encode()
            packet = json.loads(files["packet.json"])
            packet["representation"] = "B133-004 prescribed KD projection; complete originals retained"
            packet["optionalUnitAllowance"] = 20000
            packet["wholeKDFileAuthorized"] = False
            files["packet.json"] = json_bytes(packet)
            for n, raw in files.items():
                write_frozen(target / "packet" / n, raw)
                guard.check()
            for path in (FULL / "source-contract").rglob("*"):
                if path.is_file():
                    write_frozen(target / "source-contract" / path.relative_to(FULL / "source-contract"), frozen(path))
            sum_binding = freeze_json(target / "packet" / "SHA256SUMS.json", {n: sha(v) for n, v in sorted(files.items())})
            chain, measure = trials_for(files, names, target, guard, "B134 disclosed projected core")
            chosen = next((t for t in measure["trials"] if t["passes"]), None)
            representation = "PRESCRIBED_B133_004_KD_PROJECTION"
            write_frozen(target / "DISCLOSURE-001.txt", disclosure.encode())
        optional_sources = [(n, files[n], None) for n in list(units) + (list(DERIVED) if units else [])]
        optional_costs = [{"source": n, "sha256": sha(raw), **extension_upper([(n, raw, None)])}
                          for n, raw, _ in optional_sources]
        require(not optional_costs or max(r["tokens"] for r in optional_costs) <= 20000,
                "A complete optional unit cannot fit the prescribed reserve")
        caps = chosen["caps"] if chosen else None
        used = chosen if chosen else measure["trials"][-1]
        final_sums = load(target / "packet" / "SHA256SUMS.json")
        measure.update(
            decision="PASS_FORECAST_REQUIRES_ACTUAL_RUNTIME_ADMISSION" if chosen else "HOLD",
            representation=representation, caps=caps, chosenCaps=caps,
            packetManifestSha256=sha(frozen(target / "packet" / "SHA256SUMS.json")),
            chainManifestSha256=sha(frozen(target / "core-chain-001.json")),
            optionalUnitAllowance=20000, optionalUnits=optional_costs,
            largestOptionalUnitTokens=max((r["tokens"] for r in optional_costs), default=0),
            maximumExtensionTokens=used["articleUpper"]["tokens"] + 20000,
            maximumExtensionBytesUpperBound=used["articleUpper"]["payloadBytes"] + used["articleUpper"]["envelopeBytesUpper"] + 60000,
            maximumRawArticleBytes=used["articleUpper"]["payloadBytes"],
            maximumSelectedPresentArticles=sum(caps.values()) if caps else 0,
            dictionaryExtensionBytes=0, startupGate=700000, bootstrapTokens=80000, reportTokens=30000,
            prePhase2Gates={"claude": 740000, "gpt": 710000},
            completeRecordTrial=full_measure,
            selectionIndependentMethod="Largest additive whole-article and solo-envelope cost in each disjoint eligible D/E group. No semantic choices.",
            envelopeProof="Each <=13900-byte source flushes before insertion if it cannot wholly fit; 2100/source plus fixed2100. Large sources retain solo-parts+1.",
            limits="Forecast only; full-record first trial is preserved; no reviewer admission asserted.")
        forecast = freeze_json(target / "capacity-measurement-001.json", measure)
        if target != FULL:
            freeze_json(target / "packet-build.json", {
                **full_build, "packetManifest": {"path": str(target / "packet" / "SHA256SUMS.json"),
                    "sha256": sha(frozen(target / "packet" / "SHA256SUMS.json"))},
                "files": len(final_sums), "coreSources": names, "capacityMeasurement": forecast,
                "predecessor": str(FULL), "status": "PREPARED_NOT_ADMITTED",
                "sourceContract": full_build["sourceContract"]})
        freeze_json(PREP / "selected-packet-001.json", {
            "root": str(target), "caps": caps, "status": measure["decision"],
            "forecast": forecast, "completeRecordTrial": full_measure})
        print(json.dumps({"root": str(target), "caps": caps, "coreTokens": measure["coreTokens"],
                          "completeFirst": load(FULL / "complete-record-capacity-001.json")["trials"][0],
                          "trials": measure["trials"]}))
    finally:
        require(not guard.finish()["breach"], "Capacity measurement RAM breach")


if __name__ == "__main__":
    main()
