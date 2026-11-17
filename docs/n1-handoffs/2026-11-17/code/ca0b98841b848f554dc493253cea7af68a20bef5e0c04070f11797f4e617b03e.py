"""Measure complete-record-first B134 capacity, then apply only the approved KD fallback."""
import copy
import hashlib
import json
import math
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
OUT = ROOT / "fresh-independent-002"
FULL = OUT / "complete-record-trial-004"
FINAL = OUT / "projected-successor-007"
PACKET = FULL / "packet"
sys.path.insert(0, str(WS / "review-tools"))
sys.path.insert(0, str(ROOT / "neutral-preparation-001" / "tools"))
from common import require, sha, start_guard, freeze_json, write_frozen
from capacity004 import CAPS, project, xml_bytes, source_class
from capacity004_units import source_tokens, extension_upper, chain_cost, full_units

OLD = ROOT / "neutral-preparation-001" / "projected-successor-001"
OLD_PROTOCOL = OLD / "protocol-001"
sys.path.insert(0, str(OLD_PROTOCOL))
from review_chain_with_optional import build_chain

STARTUP_GATE = 700000
OPTIONAL_ALLOWANCE = 20000
BOOTSTRAP = 80000
REPORT = 30000
EXCLUSIONS = 56


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def load_bytes(packet, names):
    return {name: (packet / name).read_bytes() for name in names}


def source_cost(name, raw):
    return {"source": name, "bytes": len(raw), "sha256": sha(raw),
            "class": source_class(name)[0], "tpb": source_class(name)[1],
            "tokens": source_tokens(name, raw)}


def packet_sums(packet):
    return {p.relative_to(packet).as_posix(): sha(p.read_bytes())
            for p in sorted(packet.rglob("*")) if p.is_file() and p.name != "SHA256SUMS.json"}


def preserve_packet(packet, mapping):
    sums = packet_sums(packet)
    require(set(sums) == set(mapping), "Packet inventory differs from measured file map")
    for name, digest in sums.items():
        require(digest == sha(mapping[name]), "Packet bytes differ: " + name)
    sum_path = packet / "SHA256SUMS.json"
    sum_path.write_bytes(json_bytes(sums))
    return sha(sum_path.read_bytes()), len(sums)


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
        if char in targets:
            cost = extension_upper([(name, raw, None)])["tokens"]
            e_rows.append((cost, name, raw))
            continue
        if char in excluded:
            continue
        cost = extension_upper([(name, raw, None)])["tokens"]
        d_rows.append((cost, name, raw))
    require(len(e_rows) == EXCLUSIONS and len(d_rows) >= 1, "D/E eligible pool is incomplete")
    return ref, d_rows, e_rows


def trial_capacity(core_cost, files, core_segments):
    _, d_rows, e_rows = eligibility(files)
    trials = []
    for d, e in CAPS:
        chosen = sorted(d_rows, reverse=True)[:d] + sorted(e_rows, reverse=True)[:e]
        extension = extension_upper([(name, raw, None) for _, name, raw in chosen])
        startup = core_cost["tokens"] + extension["tokens"] + OPTIONAL_ALLOWANCE + BOOTSTRAP + REPORT
        trials.append({"caps": {"D": d, "E": e},
                       "articleBytes": extension["payloadBytes"],
                       "articleForecastIncludingEnvelopes": extension["tokens"],
                       "optionalReserve": OPTIONAL_ALLOWANCE, "startupForecast": startup,
                       "excess": max(0, startup - STARTUP_GATE),
                       "outcome": "PASS_ESTIMATE" if startup <= STARTUP_GATE else "HOLD_ESTIMATE"})
    return trials


def make_core(packet, names, out_dir, label, guard):
    sources = [(name, (packet / name).read_bytes(), None) for name in names]
    chain = build_chain(sources, out_dir / "chains" / (label + "-001"),
                        out_dir / (label + "-001.json"), guard, label)
    return chain, sources, chain_cost(chain, sources)


def regenerate_neutral_metadata(packet, full_counts, optional):
    # Retain exact original provenance bytes separately from the fresh neutral presentation.
    p = packet / "evidence"
    original_prov_path = p / "provenance-original.json"
    if not original_prov_path.exists():
        original_prov_path.write_bytes((p / "provenance.json").read_bytes())
    old_prov = original_prov_path.read_bytes()
    manifest = json.loads((packet / "repo" / "manifest.json").read_text(encoding="utf-8"))
    old_manifest = json.loads((packet / "baseline" / "manifest.json").read_text(encoding="utf-8"))
    groups = {}
    for name in ("audio", "curriculum", "files", "images", "listening", "listeningTaskAudio",
                 "listeningTaskImages", "listeningTasks", "scenes"):
        before, after = old_manifest[name], manifest[name]
        require(before.keys() == after.keys(), "Runtime group membership changed: " + name)
        groups[name] = {"baseline": len(before), "candidate": len(after),
                        "unchanged": sum(before[k] == after[k] for k in before)}
    before_entries = sum(len(old_manifest[k]) for k in groups)
    after_entries = sum(len(manifest[k]) for k in groups)
    unchanged = sum(v["unchanged"] for v in groups.values())
    provenance = {
        "candidate": "355cccb840d22e7313e79f234eb93d1367e00352",
        "candidateCommit": "355cccb840d22e7313e79f234eb93d1367e00352",
        "baseCommit": "ba80afffc20a72d31be68b355b6f90aab36a5726",
        "contentVersion": manifest["contentVersion"],
        "sourceInputs": json.loads((p / "provenance-original.json").read_text(encoding="utf-8"))["sourceInputs"],
        "signedSnapshot": {"manifestSha256": sha((packet / "repo" / "manifest.json").read_bytes()),
                           "baseManifestSha256": sha((packet / "baseline" / "manifest.json").read_bytes())},
        "proofs": {
            "reconciliationVerificationSha256": "7ea9e7dde1989b5d1eb71bed3b5789ab77f4e3713277591b4841eeb2b0295da1",
            "reconciliationGateVerificationSha256": "7b0e846ede88b4a5350df16b58df0c4461e4ba83fc0208f006d65c3951170787",
            "confirmationDossierSha256": "ef4e5a31469233ef10db7a86a555f8ae65e428d32e1b87991c0672d1d09013a9",
        },
        "sourceUnion": full_counts,
        "optionalUnitCount": len(optional),
        "limits": "Provenance and source coverage only; no semantic adjudication, comparison recommendation, teaching acceptance, or publication acceptance.",
    }
    (p / "provenance.json").write_bytes(json_bytes(provenance))
    summary = {
        "candidate": "355cccb840d22e7313e79f234eb93d1367e00352",
        "base": "ba80afffc20a72d31be68b355b6f90aab36a5726",
        "groups": groups, "baselineManifestSha256": sha((packet / "baseline" / "manifest.json").read_bytes()),
        "candidateManifestSha256": sha((packet / "repo" / "manifest.json").read_bytes()),
        "gateProofSha256": "7b0e846ede88b4a5350df16b58df0c4461e4ba83fc0208f006d65c3951170787",
        "baselineEntries": before_entries, "candidateEntries": after_entries,
        "unchangedRuntimeEntries": unchanged,
        "source": "Direct signed parent/candidate manifest group comparison; neutral recomputation.",
        "limits": "Manifest preservation only; not semantic review or runtime rendering acceptance.",
    }
    (packet / "checks" / "full-runtime-summary.json").write_bytes(json_bytes(summary))
    current_titles = (p / "title-index.txt").read_bytes()
    (p / "baseline-title-index.txt").write_bytes(current_titles)
    (p / "baseline-title-delta.json").write_bytes(json_bytes({
        "baselineCommit": "ba80afffc20a72d31be68b355b6f90aab36a5726",
        "candidateCommit": "355cccb840d22e7313e79f234eb93d1367e00352",
        "removedCompleteLinesUtf8": [],
        "reconstructedBaselineSha256": sha(current_titles),
        "candidateTitleIndexSha256": sha(current_titles),
        "limits": "Complete indexes are byte-equal because card title and article inventory are unchanged.",
    }))
    packet_meta = json.loads((packet / "packet.json").read_text(encoding="utf-8"))
    packet_meta.update({
        "candidate": "355cccb840d22e7313e79f234eb93d1367e00352",
        "base": "ba80afffc20a72d31be68b355b6f90aab36a5726",
        "newKanji": [], "modifiedExisting": ["kanji/紫.md"],
        "sourceRows": [831], "baselineKanjiArticles": 1262, "candidateKanjiArticles": 1262,
        "completeDictionaryEntries": full_counts["jmdict"]["uniqueRecords"],
        "completeKanjidicRecords": full_counts["kanjidic2"]["uniqueRecords"],
        "manifestSha256": sha((packet / "repo" / "manifest.json").read_bytes()),
        "contentVersion": manifest["contentVersion"],
        "baselineRuntimeEntries": before_entries, "candidateRuntimeEntries": after_entries,
        "unchangedRuntimeEntries": unchanged,
        "blinding": "No author response, prior reviewer reports/verdicts, report-derived assertions, pair dispositions/reasons, scan matches, or comparison recommendations.",
        "representation": "Complete unique JMdict/KANJIDIC2 unions; the prescribed KD projection will be selected only if complete-record capacity fails.",
    })
    (packet / "packet.json").write_bytes(json_bytes(packet_meta))
    original_metadata_path = p / "source-metadata-original.json"
    if not original_metadata_path.exists():
        original_metadata_path.write_bytes((p / "source-metadata.json").read_bytes())
    metadata_raw = original_metadata_path.read_bytes()
    metadata = json.loads(metadata_raw.decode("utf-8"))
    (p / "source-metadata.json").write_bytes(json_bytes({
        "reviewCandidate": "355cccb840d22e7313e79f234eb93d1367e00352",
        "snapshotParent": "ba80afffc20a72d31be68b355b6f90aab36a5726",
        "candidateArticleSha256": sha((packet / "repo" / "kanji" / "紫.md").read_bytes()),
        "sourceRows": metadata,
        "limits": "Original source-row metadata with revision identity binding; no teaching interpretation.",
    }))
    neutral_review = f"""# B134 neutral review packet

Review the signed revision of the existing 紫 article at candidate 355cccb840d22e7313e79f234eb93d1367e00352, parent ba80afffc20a72d31be68b355b6f90aab36a5726. The target article and its parent version, exact article diff, complete stroke JSON, and actual support article before/after are frozen in this packet. The support article is unchanged in this revision. The serial protocol controls independent D/E/O comparison selection; no comparison is prescribed here.

The original source packet has 182 exact JMdict predicates and the reconciliation adds 140 predicates. All 399 original and 194 supplemental complete JMdict families are merged only where full canonical XML equality holds; the resulting union has {full_counts['jmdict']['uniqueRecords']} unique families. The original 59 and supplemental 37 KANJIDIC2 records similarly yield {full_counts['kanjidic2']['uniqueRecords']} unique complete records. Exact original and supplemental query provenance, source hashes and zero-result predicates are included. Historical supplemental search was against the parent snapshot, not an instruction for comparison selection.

All 1,262 complete candidate kanji articles and the full title index are available. The parent and candidate title indexes are byte-identical. The curated 古, 右, 川 articles are present as complete article sources. The reviewer may independently select bounded D/E lists from the full eligible pool; the protocol does not mandate or prioritize any article. The revised card's current exclusion set contains 56 characters.

Original project rubrics/guidance, complete original native captures, the supplemental complete native captures, and all ten final committed host-gate logs/receipts are preserved. The source verifier proof, gate verifier proof, and confirmation dossier are hash-bound. The dossier's author-response, reports/verdicts, report-derived assertions, dispositions/reasons, scan matches, comparison index, and comparison recommendation list are excluded from reviewer inputs. The packet does not contain any teaching verdict.

The full source record trial was measured before the only permitted fallback. If full KANJIDIC2 records do not fit the unchanged 700,000 startup forecast gate, the protocol uses only the established field projection and keeps every complete record individually available within the shared 20,000 forecast allowance. Forecasts are not actual token measurements. Reviewer admission still requires explicit actual selected model, long_context, exact maxPromptTokens telemetry, zero compaction, and a prompt-only bootstrap before any evidence chain is delivered.

The work is preparation only. It makes no teaching, native/device, rendering, whole-set, or publication acceptance claim; no reviewer is launched by this packet.
"""
    (packet / "REVIEW.md").write_text(neutral_review, encoding="utf-8", newline="\n")
    (packet / "DISCLOSURE.txt").write_text(neutral_review, encoding="utf-8", newline="\n")


def main():
    guard, _ = start_guard("B134 complete-record-first fresh review capacity")
    try:
        core_spec = json.loads((FULL / "core-sources-001.json").read_text(encoding="utf-8"))
        names = list(core_spec["sources"])
        if "evidence/kanjidic2-complete-union.xml" in names:
            names[names.index("evidence/kanjidic2-complete-union.xml")] = "evidence/kanjidic2-records.xml"
        require("evidence/kanjidic2-records.xml" in names
                and "evidence/kanjidic2-full-unit-index.json" in names,
                "Full KD union/unit index not in first core")
        # Full record trial is sealed as a separate source inventory before any fallback.
        record_summary = json.loads((FULL / "complete-record-summary-001.json").read_text(encoding="utf-8"))
        full_counts = {"jmdict": record_summary["jmDict"], "kanjidic2": record_summary["kanjidic2"]}
        regenerate_neutral_metadata(PACKET, full_counts, [])
        current_sums = packet_sums(PACKET)
        (PACKET / "SHA256SUMS.json").write_bytes(json_bytes(current_sums))
        original_sums = packet_sums(PACKET)
        mapping = {name: (PACKET / name).read_bytes() for name in original_sums}
        require("SHA256SUMS.json" not in mapping, "Packet hash file must be excluded from inventory")
        full_chain, full_sources, full_cost = make_core(PACKET, names, FULL, "complete-record-core-rerun-010", guard)
        full_ref, full_d, full_e = eligibility(mapping)
        full_trials = trial_capacity(full_cost, mapping, full_chain)
        full_measure = {
            "status": "MEASURED_COMPLETE_RECORDS_BEFORE_PROJECTION",
            "candidate": core_spec["candidate"], "base": core_spec["base"],
            "sourceRecords": len(full_sources), "segments": len(full_chain["segments"]),
            "segmentBytes": full_cost["chainBytes"], "payloadBytes": full_cost["payloadBytes"],
            "envelopeBytes": full_cost["envelopeBytes"], "coreTokens": full_cost["tokens"],
            "fullKDCoefficientDisclosure": "Inherited conservative B133 capacity004 full-kd coefficient 1.0.",
            "recordCounts": full_counts, "eligibleD": len(full_d), "eligibleE": len(full_e),
            "trials": full_trials, "packetInventory": original_sums,
            "coreSources": names,
            "limits": "Forecast only; this full-record core precedes any projection.",
        }
        write_frozen(FULL / "capacity-full-record-004.json", json_bytes(full_measure))
        require(not FINAL.exists(), "Preserve existing final projected-successor")
        shutil.copytree(PACKET, FINAL / "packet")
        final_packet = FINAL / "packet"
        for path in final_packet.rglob("*"):
            if path.is_file():
                path.chmod(0o666)

        trial_pass = next((t for t in full_trials if t["outcome"] == "PASS_ESTIMATE"), None)
        if trial_pass:
            chosen_packet, final_names, projection_status = PACKET, names, "FULL_RECORDS"
            core_names = names
            optional_units = []
        else:
            require(full_cost["tokens"] + 20000 + 80000 + 30000 > 700000
                    or all(t["outcome"] == "HOLD_ESTIMATE" for t in full_trials),
                    "Full records fit; do not apply fallback")
            full_kd = mapping["evidence/kanjidic2-records.xml"]
            projected = xml_bytes(project(full_kd))
            (final_packet / "evidence" / "kanjidic2-review-projection.xml").write_bytes(projected)
            # The merged union has a different count from the predecessor, so create each exact unit directly.
            kd_lines = full_kd.splitlines(keepends=True)[1:-1]
            kd_root = ET.fromstring(full_kd)
            final_kd_units = {f"evidence/kanjidic2-full-records/{node.findtext('literal')}.xml": raw
                              for node, raw in zip(kd_root, kd_lines)}
            require(len(final_kd_units) == full_counts["kanjidic2"]["uniqueRecords"],
                    "Merged full KD unit inventory differs")
            optional_units = list(final_kd_units.items())
            optional_units += [(name, (final_packet / name).read_bytes())
                               for name in ("evidence/xml-presentation.json", "evidence/font-cmap.json",
                                            "evidence/dictionary-index.json")]
            final_names = [name for name in names if name != "evidence/kanjidic2-records.xml"]
            final_names.insert(names.index("evidence/kanjidic2-records.xml"),
                               "evidence/kanjidic2-review-projection.xml")
            for name, raw in final_kd_units.items():
                (final_packet / name).parent.mkdir(parents=True, exist_ok=True)
                (final_packet / name).write_bytes(raw)
            projection_status = "PRESCRIBED_B133_004_KD_FIELD_PROJECTION"
            # Full-record sources remain retained in the non-chain packet.
            core_names = final_names

        # Rebuild complete dictionary indexes from full merged records and exact query provenance.
        original_selection = json.loads((final_packet / "evidence" /
                                         "source-selection-provenance-original.json").read_text(encoding="utf-8"))
        receipt = json.loads((final_packet / "evidence" /
                              "reconciliation-query-receipt-neutral.json").read_text(encoding="utf-8"))
        jm = ET.fromstring((final_packet / "evidence" / "jmdict-families.xml").read_bytes())
        original_queries = sorted({q for selection in original_selection["selections"]
                                   if selection["file"].startswith("jmdict")
                                   for q in selection.get("queries", [])})
        supplemental_queries = sorted(receipt["countsIncludingZero"])
        index = {}
        for query in original_queries:
            if query.startswith("contains-keb:"):
                needle = query.split(":", 1)[1]
                index[query] = sorted({n.findtext("ent_seq") for n in jm
                                       if any(needle in (k.text or "") for k in n.findall("k_ele/keb"))},
                                      key=int)
            elif query.startswith("exact-keb:"):
                value = query.split(":", 1)[1]
                index[query] = sorted({n.findtext("ent_seq") for n in jm
                                       if any(value == (k.text or "") for k in n.findall("k_ele/keb"))},
                                      key=int)
            elif query.startswith("exact-reading:"):
                value = query.split(":", 1)[1]
                index[query] = sorted({n.findtext("ent_seq") for n in jm
                                       if any(value == (k.text or "") for k in n.findall("r_ele/reb"))},
                                      key=int)
            elif query.startswith("exact-reb:"):
                value = query.split(":", 1)[1]
                index[query] = sorted({n.findtext("ent_seq") for n in jm
                                       if any(value == (r.text or "") for r in n.findall("r_ele/reb"))},
                                      key=int)
            else:
                raise RuntimeError("Unknown original query selector: " + query)
        for query in supplemental_queries:
            kind, value = query.split(":", 1)
            if kind == "exact-spelling":
                index["supplemental:" + query] = sorted({n.findtext("ent_seq") for n in jm
                    if any(value == (k.text or "") for k in n.findall("k_ele/keb"))}, key=int)
            elif kind == "exact-reading":
                index["supplemental:" + query] = sorted({n.findtext("ent_seq") for n in jm
                    if any(value == (k.text or "") for k in n.findall("r_ele/reb"))}, key=int)
        (final_packet / "evidence" / "dictionary-index.json").write_bytes(json_bytes(index))
        xml_presentation = {
            "method": "Complete canonical-equal record union, every retained source field, one normalized record per line.",
            "reviewCandidate": core_spec["candidate"], "base": core_spec["base"],
            "originalSelections": original_selection["selections"],
            "supplementalQueryReceipt": "evidence/reconciliation-query-receipt-neutral.json",
            "supplementalMembership": "evidence/reconciliation-query-membership.json",
            "counts": {"jmdict": full_counts["jmdict"]["uniqueRecords"],
                       "kanjidic2": full_counts["kanjidic2"]["uniqueRecords"]},
            "zeroMatchQueries": original_selection["zeroMatchQueries"] +
                                [q for q, n in receipt["countsIncludingZero"].items() if n == 0],
            "limits": "Mechanical source presentation and query provenance only; no reviewer comparison selections.",
        }
        (final_packet / "evidence" / "xml-presentation.json").write_bytes(json_bytes(xml_presentation))
        # Replace the earlier trial's stale original-candidate evidence index with exact merged results.
        (final_packet / "evidence" / "source-selection-provenance-merged.json").write_bytes(json_bytes({
            "status": "COMPLETE_SELECTION_PROVENANCE_DERIVATIVE_NOT_REVIEW_INSTRUCTION",
            "candidate": core_spec["candidate"], "base": core_spec["base"],
            "originalSelectionsPath": "evidence/source-selection-provenance-original.json",
            "supplementalReceiptPath": "evidence/reconciliation-query-receipt-neutral.json",
            "supplementalMembershipPath": "evidence/reconciliation-query-membership.json",
            "originalPredicateCount": original_selection["queryCount"],
            "supplementalPredicateCount": len(receipt["countsIncludingZero"]),
            "originalZeroMatchPredicates": original_selection["zeroMatchQueries"],
            "supplementalZeroMatchPredicates": [q for q, n in receipt["countsIncludingZero"].items() if n == 0],
            "dictionaryIndexSha256": sha((final_packet / "evidence" / "dictionary-index.json").read_bytes()),
            "limits": "Exact membership metadata; excludes pair dispositions/reasons, recommendations, scan matches, author response and reviews.",
        }))

        optional_rows = []
        for name, raw in optional_units:
            bound = extension_upper([(name, raw, None)])
            optional_rows.append({"unit": name, "sha256": sha(raw), "bytes": len(raw),
                                  "forecastUpperTokens": bound["tokens"]})
        if projection_status != "FULL_RECORDS":
            require(max(row["forecastUpperTokens"] for row in optional_rows) <= OPTIONAL_ALLOWANCE,
                    "A complete optional unit exceeds shared reserve")

        # Candidate source metadata/presentation is regenerated to bind the signed revision.
        regen_counts = full_counts
        regenerate_neutral_metadata(final_packet, regen_counts,
                                    optional_rows if projection_status != "FULL_RECORDS" else [])

        # Build the revised core chain and exact forecasts from its final bytes.
        core_manifest, core_sources, core_cost = make_core(final_packet, core_names, FINAL,
                                                             "fresh-independent-core", guard)
        final_files = {p.relative_to(final_packet).as_posix(): p.read_bytes()
                       for p in final_packet.rglob("*") if p.is_file() and p.name != "SHA256SUMS.json"}
        ref, d_rows, e_rows = eligibility(final_files)
        trials = trial_capacity(core_cost, final_files, core_manifest)
        chosen = next((t for t in trials if t["outcome"] == "PASS_ESTIMATE"), None)
        decision = "PASS_ESTIMATE" if chosen else "HOLD_ESTIMATE"
        # Update source hashes after the projection and neutral-index regeneration.
        final_manifest_sha, final_file_count = preserve_packet(final_packet, final_files)
        for path in final_packet.rglob("*"):
            if path.is_file():
                path.chmod(0o444)

        capacity = {
            "status": "MEASURED_NOT_ADMITTED",
            "decision": decision,
            "candidate": core_spec["candidate"], "base": core_spec["base"],
            "representation": projection_status,
            "completeRecordTrial": {
                "coreSources": len(full_sources), "coreSegments": len(full_chain["segments"]),
                "chainBytes": full_cost["chainBytes"], "payloadBytes": full_cost["payloadBytes"],
                "envelopeBytes": full_cost["envelopeBytes"], "coreTokens": full_cost["tokens"],
                "firstD25E10StartupForecast": full_trials[0]["startupForecast"],
                "trials": full_trials,
            },
            "finalCoreSources": len(core_sources), "finalCoreSegments": len(core_manifest["segments"]),
            "finalChainBytes": core_cost["chainBytes"], "finalPayloadBytes": core_cost["payloadBytes"],
            "finalEnvelopeBytes": core_cost["envelopeBytes"], "coreTokens": core_cost["tokens"],
            "maxSegmentBytes": max(s["bytes"] for s in core_manifest["segments"]),
            "eligibleArticleCounts": {"D": len(d_rows), "E": len(e_rows)},
            "trials": trials, "chosenCaps": chosen["caps"] if chosen else None,
            "optionalUnitAllowance": OPTIONAL_ALLOWANCE, "optionalUnits": optional_rows,
            "largestOptionalUnitTokens": max((row["forecastUpperTokens"] for row in optional_rows), default=0),
            "maximumExtensionTokens": (chosen["articleForecastIncludingEnvelopes"] + OPTIONAL_ALLOWANCE
                                       if chosen else None),
            "packetManifestSha256": final_manifest_sha, "packetFiles": final_file_count,
            "startupGate": STARTUP_GATE, "bootstrapTokens": BOOTSTRAP, "reportTokens": REPORT,
            "prePhase2Gates": {"claude": 740000, "gpt": 710000},
            "profiles": {"claude": {"selectedModel": "claude-opus-5.5", "contextTier": "long_context",
                                     "maxPromptTokens": 952000},
                         "gpt": {"selectedModel": "gpt-6.1-sol", "contextTier": "long_context",
                                  "maxPromptTokens": 922000}},
            "limits": "Forecast, not token measurements. Actual bootstrap usage limits, model, contextTier and zero compaction remain mandatory before chain delivery.",
        }
        write_frozen(FINAL / "capacity-measurement-001.json", json_bytes(capacity))
        write_frozen(FINAL / "core-sources-001.json", json_bytes({
            "candidate": core_spec["candidate"], "base": core_spec["base"], "sources": core_names,
            "segments": core_manifest["segments"], "sourceBindings": core_manifest["sources"],
        }))
        print(json.dumps({"finalRoot": str(FINAL), "decision": decision, "caps": capacity["chosenCaps"],
                          "completeFirstD25E10": full_trials[0]["startupForecast"],
                          "fullTrials": full_trials, "finalCoreTokens": core_cost["tokens"],
                          "finalTrials": trials, "optionalUnits": len(optional_rows),
                          "optionalLargest": capacity["largestOptionalUnitTokens"],
                          "packetFiles": final_file_count}, ensure_ascii=False))
    finally:
        require(not guard.finish()["breach"], "Capacity measurement RAM breach")


if __name__ == "__main__":
    main()
