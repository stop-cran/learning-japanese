#!/usr/bin/env python3
"""Audit the bounded N1 pilot mechanically; not linguistic or native acceptance."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from build_manifest import build_manifest
from freeze_n1_sources import KVG_REVISION, digest, require

ROOT = Path(__file__).resolve().parent.parent


def reading_key(raw):
    folded = "".join(chr(ord(c) - 0x60) if "\u30a1" <= c <= "\u30f6" else c for c in raw)
    return "".join(c for c in folded if c not in ".-・" and not c.isspace())


def offered_keys(readings):
    """Mirror the pinned ReadingCard.quizReadings, not app execution."""
    stems, keys, result = set(), set(), []
    for raw in readings:
        key = reading_key(raw)
        stem = reading_key(raw.split(".", 1)[0])
        if not key or stem in stems:
            continue
        stems.add(stem)
        if key not in keys:
            keys.add(key)
            result.append(key)
    return result[:3]


def quiz_readings(meta, field):
    readings = meta.get("quiz" + field[0].upper() + field[1:], meta[field])
    require(isinstance(readings, list) and all(isinstance(r, str) and r for r in readings),
            f"Invalid curated readings: {field}")
    require(len(readings) == len(set(readings)) and set(readings) <= set(meta[field]),
            f"Curated readings are not an exact distinct source subset: {field}")
    return readings


def metadata(root, name):
    return yaml.safe_load((root / name).read_text(encoding="utf-8").split("---", 2)[1])


def reconciled_baseline_manifest(baseline, current, changes):
    result = {key: dict(value) if isinstance(value, dict) else value
              for key, value in baseline.items()}
    seen = set()
    for row in changes:
        require(set(row) == {"section", "path", "before", "after", "sourceCommit"},
                "Malformed integrated-main manifest change")
        section, name = row["section"], row["path"]
        require(section in {"images", "scenes"} and name.startswith(section + "/"),
                "Integrated-main exception must be an image or scene")
        require(len(row["sourceCommit"]) == 40
                and all(c in "0123456789abcdef" for c in row["sourceCommit"]),
                "Integrated-main exception needs an exact source commit")
        require((section, name) not in seen, "Duplicate integrated-main exception")
        seen.add((section, name))
        require(row["before"] is not None and row["before"] != row["after"]
                and baseline.get(section, {}).get(name) == row["before"]
                and current.get(section, {}).get(name) == row["after"],
                f"Integrated-main before/after hash mismatch: {name}")
        if row["after"] is None:
            result[section].pop(name)
        else:
            result[section][name] = row["after"]
    return result


def audit(root):
    evidence = root / "docs" / "n1-sources"
    baseline = json.loads((evidence / "baseline-inventory.json").read_text(encoding="utf-8"))
    ledger = json.loads((evidence / "pilot-progress.json").read_text(encoding="utf-8"))
    curation = json.loads((evidence / "pilot-curated-readings.json").read_text(encoding="utf-8"))
    frozen = json.loads((evidence / "pilot-membership.json").read_text(encoding="utf-8"))
    members = [r["kanji"] for r in frozen["members"]]
    require(ledger["membership"] == members, "Pilot membership/order changed")
    require([r["kanji"] for r in curation["cards"]] == members,
            "Curated pilot membership/order changed")
    curated = {r["kanji"]: r for r in curation["cards"]}
    require(set(ledger["drafted"]) == set(members) and not ledger["pendingTeaching"],
            "This audit requires the complete pilot draft")
    rows = json.loads((evidence / "source-index.json").read_text(encoding="utf-8"))
    source = {r["kanji"]: r for r in rows}
    community = json.loads((evidence / "community-list-20261102.json").read_text(encoding="utf-8"))
    require([r["kanji"] for r in rows] == community, "Source membership/order mismatch")
    current = build_manifest(root)
    require(json.loads((root / "manifest.json").read_text(encoding="utf-8")) == current,
            "Manifest is stale")
    mappings = ledger["supportMappings"]
    pairs = {(r["kanji"], r["article"]) for r in mappings}
    recorded_pairs = [tuple(p) for p in ledger["requiredReciprocalPairsAtThisDraft"]]
    require(len(recorded_pairs) == len(set(recorded_pairs)) and pairs == set(recorded_pairs),
            "Reciprocal ledger differs from all selected support mappings")
    changed_reuses = {r["article"] for r in mappings if not r["newArticle"]}
    counts = {"baselineKanjiMetadataPreserved": 0, "baselineWordMetadataPreserved": 0,
              "baselineStrokeHashesPreserved": 0}
    for name, old in baseline["files"].items():
        if name.startswith(("kanji/", "words/")):
            require(metadata(root, name) == old["metadata"], f"Baseline metadata changed: {name}")
            key = "baselineKanjiMetadataPreserved" if name.startswith("kanji/") else "baselineWordMetadataPreserved"
            counts[key] += 1
        if name.startswith("strokes/"):
            require(digest((root / name).read_bytes()) == old["sha256"],
                    f"Baseline stroke bytes changed: {name}")
            counts["baselineStrokeHashesPreserved"] += 1
    main_changes = ledger.get("integratedMainManifestChanges", [])
    old_manifest = reconciled_baseline_manifest(
        baseline["files"]["manifest.json"]["manifest"], current, main_changes)
    for category, entries in old_manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, expected in entries.items():
            if name not in changed_reuses:
                require(current.get(category, {}).get(name) == expected,
                        f"Unrelated baseline payload changed: {name}")
    expected_new = {source[c]["article"] for c in members} | {source[c]["strokeFile"] for c in members}
    expected_new |= {r["article"] for r in mappings if r["newArticle"]}
    for category, entries in current.items():
        if isinstance(entries, dict):
            additions = set(entries) - old_manifest.get(category, {}).keys()
            require(additions <= expected_new, f"Out-of-pilot runtime addition: {sorted(additions - expected_new)}")
    require(expected_new <= current["files"].keys(), "Missing pilot runtime files")
    families = {}
    for selection_name, packet_name in (
        ("pilot-lexical-selection.json", "pilot-jmdict.xml"),
        ("pilot-comparison-selection.json", "pilot-comparisons-jmdict.xml"),
        ("pilot-label-selection.json", "pilot-label-jmdict.xml"),
        ("pilot-curation-comparison-selection.json", "pilot-curation-comparisons-jmdict.xml"),
        ("pilot-curation-followup-selection.json", "pilot-curation-followup-jmdict.xml"),
    ):
        selection = json.loads((evidence / selection_name).read_text(encoding="utf-8"))
        entries = ET.parse(evidence / packet_name).getroot().findall("entry")
        require([e.findtext("ent_seq") for e in entries] == selection["entryIds"],
                f"Dictionary packet selection/order mismatch: {packet_name}")
        families.update({e.findtext("ent_seq"): e for e in entries})
    dispositions = ledger["draftedReadingDispositions"]
    actual_readings = [(r["kanji"], r["kind"], r["reading"]) for r in dispositions]
    require(len(actual_readings) == len(set(actual_readings)), "Duplicate reading disposition")
    expected_readings = set()
    projections = {r["kanji"]: r for r in ledger["readingCompatibility"]["sourceOrderProjection"]}
    legacy_source_only_offered, source_only_offered = set(), set()
    curated_key_count = 0
    for c in members:
        row = source[c]
        meta = metadata(root, row["article"])
        for key in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
            require(meta[key] == row["metadata"][key], f"Source metadata changed: {c} {key}")
        require(meta["jlpt"] == 1 and "jlpt-n1" in meta["tags"], f"Wrong N1 label: {c}")
        require(f"grade-{row['metadata']['grade']}" in meta["tags"], f"Grade missing: {c}")
        quiz = ledger["quizAuditAtThisDraft"][c]
        require(meta["title"] == quiz["title"] and meta["distractors"] == quiz["distractors"]
                and len(set(meta["distractors"])) == 3, f"Quiz ledger mismatch: {c}")
        strokes = json.loads((root / row["strokeFile"]).read_text(encoding="utf-8"))
        require(strokes["kanji"] == c and strokes["sourceRevision"] == KVG_REVISION
                and strokes["strokeCount"] == len(strokes["strokes"]) == meta["strokes"],
                f"Stroke identity/count/revision mismatch: {c}")
        body = (root / row["article"]).read_text(encoding="utf-8")
        reading_table = body.split("## Readings\n", 1)[1].split("## Common words", 1)[0]
        selected = curated[c]["selected"]
        excluded = curated[c]["excluded"]
        decisions = [(r["kind"], r["reading"]) for r in selected + excluded]
        require(len(decisions) == len(set(decisions))
                and set(decisions) == {("on", r) for r in meta["onyomi"]}
                | {("kun", r) for r in meta["kunyomi"]},
                f"Curated dispositions do not cover every full reading exactly once: {c}")
        require(all(r["reason"].strip() for r in selected + excluded),
                f"Missing curation reason: {c}")
        for r in selected:
            require((c, r["article"]) in pairs and r["entryIds"]
                    and set(r["entryIds"]) <= families.keys(),
                    f"Missing mapped lexical support for selected reading: {c} {r}")
            table_row = next(line for line in reading_table.splitlines()
                             if line.startswith(f"| {r['reading']} |"))
            require(f"(../{r['article']})" in table_row,
                    f"Selected reading lacks its linked table example: {c} {r['reading']}")
        for kind, field, projection in (("on", "onyomi", "onKeys"), ("kun", "kunyomi", "kunKeys")):
            keys = offered_keys(meta[field])
            require(projections[c][projection] == keys, f"Offered key projection changed: {c} {kind}")
            quiz_field = "quiz" + field[0].upper() + field[1:]
            require(quiz_field in meta and meta[quiz_field] == curated[c][quiz_field],
                    f"Explicit curated subset differs from ledger: {c} {kind}")
            selected_raw = quiz_readings(meta, field)
            require([r["reading"] for r in selected if r["kind"] == kind] == selected_raw,
                    f"Selected evidence differs from quiz subset/order: {c} {kind}")
            curated_keys = offered_keys(selected_raw)
            require(curated[c][projection] == curated_keys,
                    f"Curated offered keys differ from ledger: {c} {kind}")
            curated_key_count += len(curated_keys)
            for reading in meta[field]:
                expected_readings.add((c, kind, reading))
                require(f"| {reading} |" in reading_table, f"Missing reading-table row: {c} {reading}")
            for r in dispositions:
                if r["kanji"] != c or r["kind"] != kind:
                    continue
                require(set(r["entryIds"]) <= families.keys(), f"Missing lexical family: {r}")
                if r.get("sourceOnly"):
                    table_row = next(line for line in reading_table.splitlines()
                                     if line.startswith(f"| {r['reading']} |"))
                    require("source-only" in table_row, f"Unqualified source-only row: {c} {r['reading']}")
                    if reading_key(r["reading"]) in keys:
                        legacy_source_only_offered.add((c, kind, reading_key(r["reading"])))
                    if reading_key(r["reading"]) in curated_keys:
                        source_only_offered.add((c, kind, reading_key(r["reading"])))
    require(set(actual_readings) == expected_readings, "Reading dispositions differ from full metadata")
    recorded_source_only = {(r["kanji"], r["kind"], k)
                            for r in ledger["readingCompatibility"]["sourceOnlyOfferedKeys"]
                            for k in r["keys"]}
    require(legacy_source_only_offered == recorded_source_only,
            "Historical source-only offered-key ledger mismatch")
    require(not source_only_offered, "Source-only reading still offered by pilot curation")
    for r in mappings:
        name, c = r["article"], r["kanji"]
        meta = metadata(root, name)
        require(meta["reading"] == r["primaryReading"], f"Primary support reading mismatch: {name}")
        entries = [families[seq] for seq in r["entryIds"]]
        require(any(meta["reading"] in [v.text for v in e.findall("r_ele/reb")]
                    and (meta["word"] in [v.text for v in e.findall("k_ele/keb")]
                         or meta["word"] == meta["reading"]) for e in entries),
                f"No matching lexical identity/reading: {name}")
        word_body = (root / name).read_text(encoding="utf-8")
        kanji_body = (root / source[c]["article"]).read_text(encoding="utf-8")
        require(f"(../kanji/{c}.md)" in word_body, f"Missing support backlink: {name} -> {c}")
        require(f"(../{name})" in kanji_body, f"Missing kanji forward link: {c} -> {name}")
    candidates = json.loads((evidence / "baseline-word-candidates.json").read_text(encoding="utf-8"))
    activated = {(r["kanji"], r["article"]) for r in candidates if r["kanji"] in members}
    require(activated <= pairs, "Activated baseline candidate missing from mappings")
    for r in ledger["newWordQuizAudit"]["directExclusions"]:
        require(metadata(root, f"words/{r['word']}.md")["quiz_exclusions"] == r["exclude"],
                f"Word exclusion ledger mismatch: {r['word']}")
    return {**counts, "draftKanji": len(members),
            "newWords": len({r["article"] for r in mappings if r["newArticle"]}),
            "requiredReciprocalPairs": len(pairs), "activatedDeclaredPairs": len(activated),
            "readingDispositions": len(actual_readings), "sourceOnlyReadings": sum(
                bool(r.get("sourceOnly")) for r in dispositions),
            "legacySourceOnlyOfferedKeys": len(legacy_source_only_offered),
            "curatedOfferedKeys": curated_key_count,
            "sourceOnlyOfferedKeys": len(source_only_offered), "dictionaryFamilies": len(families),
            "manifestFresh": True, "contentVersion": current["contentVersion"],
            "accountedMainManifestChanges": len(main_changes),
            "limits": "Mechanical draft audit; not independent content review, app execution, native/phone acceptance or publication."}


if __name__ == "__main__":
    print(json.dumps(audit(ROOT), ensure_ascii=False, indent=2))
