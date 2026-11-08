#!/usr/bin/env python3
"""Audit one later N1 batch against its exact base; not linguistic acceptance."""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from audit_n1_pilot import metadata, offered_keys, quiz_readings
from build_manifest import build_manifest
from freeze_n1_sources import KVG_REVISION, require

ROOT = Path(__file__).resolve().parent.parent


def runtime_delta(before, after, additions, changed):
    def payload(manifest):
        return {(section, name): value
                for section, entries in manifest.items() if isinstance(entries, dict)
                for name, value in entries.items()}

    old, new = payload(before), payload(after)
    require(not old.keys() - new.keys(), "Baseline runtime payload removed")
    require(new.keys() - old.keys() == {("files", name) for name in additions},
            "Runtime additions differ from this batch")
    actual_changes = {name for name in old if old[name] != new[name]}
    require(actual_changes == {("files", name) for name in changed},
            "Changed baseline payload differs from recorded reused passages")


def lexical_pair(entry, spelling, reading):
    spellings = {v.text for v in entry.findall("k_ele/keb")}
    if spelling not in spellings:
        return False
    for row in entry.findall("r_ele"):
        restrictions = {v.text for v in row.findall("re_restr")}
        if (row.findtext("reb") == reading and row.find("re_nokanji") is None
                and (not restrictions or spelling in restrictions)):
            return True
    return False


def base_file(root, commit, name):
    return subprocess.check_output(
        ["git", "--no-pager", "show", f"{commit}:{name}"], cwd=root).decode("utf-8")


def reused_changes(old, new, rows, exclusions=None):
    old = old.replace("\r\n", "\n")
    new = new.replace("\r\n", "\n")
    expected = old
    for row in rows:
        require(expected.count(row["before"]) == 1,
                "Reused passage must match exactly once")
        expected = expected.replace(row["before"], row["after"], 1)
    require(expected == new, "Reused passage exceeds recorded exact edits")
    before = yaml.safe_load(old.split("---", 2)[1])
    after = yaml.safe_load(new.split("---", 2)[1])
    if exclusions is not None:
        previous = before.get("quiz_exclusions", [])
        require(len(exclusions) == len(set(exclusions))
                and set(previous) < set(exclusions),
                "Reused exclusions must be distinct additive safeguards")
        before["quiz_exclusions"] = exclusions
    require(before == after, "Reused metadata changed outside recorded exclusions")


def required_fields(value, fields, label):
    require(isinstance(value, dict), f"{label} must be an object")
    missing = sorted(set(fields) - value.keys())
    require(not missing, f"{label} missing required fields: {', '.join(missing)}")


def recorded_pairs(value, label):
    require(isinstance(value, list), f"{label} must be a list")
    require(all(isinstance(row, list) and len(row) == 2
                and all(isinstance(item, str) and item for item in row)
                for row in value), f"Invalid {label}")
    pairs = [tuple(row) for row in value]
    require(len(pairs) == len(set(pairs)), f"Duplicate {label}")
    return pairs


def safe_identifier(value):
    return (isinstance(value, str) and bool(value) and value not in {".", ".."}
            and not any(char in value for char in "/\\:\0"))


def source_plan_packets(folder, batch, plan, source_audit, variant):
    packets = [
        (f"batch-{batch}-lexical-selection.json", f"batch-{batch}-jmdict.xml"),
        (f"batch-{batch}-comparison-selection.json", f"batch-{batch}-comparisons.xml"),
    ]
    if variant == "current":
        required_fields(plan["sourceEvidence"],
                        {"memberFamilies", "initialComparisons", "completionComparisons",
                         "completeFamilyCounts", "distinctCompleteFamilies"},
                        "Source evidence")
        packets.append((f"batch-{batch}-completion-selection.json",
                        f"batch-{batch}-completion-comparisons.xml"))
        evidence = plan["sourceEvidence"]
        require([evidence["memberFamilies"], evidence["initialComparisons"],
                 evidence["completionComparisons"]] == [name for _, name in packets],
                "Source plan dictionary packet names differ")

    families, counts = {}, []
    for selection_name, packet_name in packets:
        selection = json.loads((folder / selection_name).read_text(encoding="utf-8"))
        required_fields(selection, {"schemaVersion", "batch", "entryIds"}, "Dictionary selection")
        require(selection["schemaVersion"] == 1 and selection["batch"] == batch
                and isinstance(selection["entryIds"], list), "Invalid dictionary selection identity")
        entries = ET.parse(folder / packet_name).getroot().findall("entry")
        ids = [entry.findtext("ent_seq") for entry in entries]
        require(ids == selection["entryIds"] and all(isinstance(i, str) and i.isdigit() for i in ids)
                and len(ids) == len(set(ids)), f"Dictionary packet membership/order differs: {packet_name}")
        counts.append(len(ids))
        for entry_id, entry in zip(ids, entries):
            if entry_id in families:
                first, second = copy.deepcopy(families[entry_id]), copy.deepcopy(entry)
                first.tail = second.tail = None
                require(ET.tostring(first) == ET.tostring(second),
                        f"Conflicting duplicate dictionary family: {entry_id}")
            else:
                families[entry_id] = entry

    if variant == "current":
        required_fields(source_audit, {"memberFamilies", "comparisonFamilies",
                                      "completeDictionaryFamilies"}, "Source-completion audit")
        require(counts == plan["sourceEvidence"]["completeFamilyCounts"]
                and len(families) == plan["sourceEvidence"]["distinctCompleteFamilies"]
                and counts[0] == source_audit["memberFamilies"]
                and sum(counts[1:]) == source_audit["comparisonFamilies"]
                and len(families) == source_audit["completeDictionaryFamilies"],
                "Dictionary family counts differ from source evidence")
    else:
        required_fields(source_audit, {"completeMemberFamilies", "completeComparisonFamilies",
                                      "distinctFamilyUnion"}, "Source-completion audit")
        require(counts == [source_audit["completeMemberFamilies"],
                           source_audit["completeComparisonFamilies"]]
                and len(families) == source_audit["distinctFamilyUnion"],
                "Dictionary family counts differ from source evidence")
    return families


def teachable_lexical_pair(entry, spelling, reading, sense_number=None):
    if not lexical_pair(entry, spelling, reading):
        return False
    written = [row for row in entry.findall("k_ele") if row.findtext("keb") == spelling]
    if not any(all("search-only" not in (flag.text or "").lower()
                   for flag in row.findall("ke_inf")) for row in written):
        return False
    senses = entry.findall("sense")
    if sense_number is not None:
        if type(sense_number) is not int or not 1 <= sense_number <= len(senses):
            return False
        senses = [senses[sense_number - 1]]
    for sense in senses:
        written_restrictions = {row.text for row in sense.findall("stagk")}
        reading_restrictions = {row.text for row in sense.findall("stagr")}
        if ((not written_restrictions or spelling in written_restrictions)
                and (not reading_restrictions or reading in reading_restrictions)):
            return True
    return False


def audit_pinned_strokes(root, folder, batch, c, meta, source_row, snapshot, plan, draft, variant, commit):
    import generate_strokes

    evidence_name = f"batch-{batch}-stroke-evidence.json"
    svg_name = f"batch-{batch}-kanjivg.svg"
    evidence = json.loads((folder / evidence_name).read_text(encoding="utf-8"))
    required_fields(evidence, {"revision", "gitBlob", "sha256", "bytes",
                               "dictionaryStrokeCount", "sourceStrokePaths",
                               "converterNormalizedSha256"}, "Stroke evidence")
    required_fields(source_row, {"kanjivgInventory"}, "Frozen source row")
    inventory = source_row["kanjivgInventory"]
    required_fields(inventory, {"path", "type", "sha", "size"}, "Frozen KanjiVG inventory")
    required_fields(snapshot, {"kanjivg"}, "Frozen source snapshot")
    required_fields(snapshot["kanjivg"], {"revision", "converter"}, "Frozen KanjiVG snapshot")
    required_fields(snapshot["kanjivg"]["converter"], {"normalizedSha256"}, "Frozen converter")
    if variant == "current":
        stroke_plan = plan["strokePlan"]
        required_fields(stroke_plan, {"source", "evidence", "sourceRevision",
                                     "dictionaryAndSvgCount", "converterNormalizedSha256"},
                        "Stroke plan")
        require(stroke_plan["source"] == svg_name and stroke_plan["evidence"] == evidence_name
                and stroke_plan["sourceRevision"] == evidence["revision"]
                and stroke_plan["dictionaryAndSvgCount"] == meta["strokes"]
                and stroke_plan["converterNormalizedSha256"] == evidence["converterNormalizedSha256"],
                "Stroke plan differs from pinned evidence")
    else:
        stroke_plan = plan["strokeAndFontPlan"]
        required_fields(stroke_plan, {"pinnedSvg", "paths"}, "Stroke plan")
        require(stroke_plan["pinnedSvg"] == svg_name and stroke_plan["paths"] == meta["strokes"],
                "Stroke plan differs from pinned evidence")
    svg = (folder / svg_name).read_bytes()
    # Git can expand an LF source blob to CRLF in the working tree.
    if len(svg) != inventory["size"]:
        svg = svg.replace(b"\r\n", b"\n")
    blob = hashlib.sha1(b"blob " + str(len(svg)).encode("ascii") + b"\0" + svg).hexdigest()
    converter = Path(generate_strokes.__file__).read_bytes().replace(b"\r\n", b"\n")
    require(evidence["revision"] == KVG_REVISION == generate_strokes.KANJIVG_REVISION
            == snapshot["kanjivg"]["revision"]
            and len(svg) == evidence["bytes"] and hashlib.sha256(svg).hexdigest() == evidence["sha256"]
            and blob == evidence["gitBlob"] == inventory["sha"]
            and inventory["type"] == "blob" and inventory["path"] == f"kanji/{ord(c):05x}.svg"
            and inventory["size"] == len(svg)
            and hashlib.sha256(converter).hexdigest() == evidence["converterNormalizedSha256"]
            == snapshot["kanjivg"]["converter"]["normalizedSha256"]
            and evidence["dictionaryStrokeCount"] == evidence["sourceStrokePaths"] == meta["strokes"],
            f"Pinned SVG or converter differs: {c}")
    converted = generate_strokes.convert(c, svg.decode("utf-8"))
    variants_name = "tools/order_variants.json"
    variants_text = (root / variants_name).read_text(encoding="utf-8")
    require(variants_text == base_file(root, commit, variants_name).replace("\r\n", "\n"),
            "Frozen stroke variants changed")
    variants = json.loads(variants_text)
    require(isinstance(variants, dict), "Invalid stroke variant table")
    if c in variants:
        converted["orderVariants"] = variants[c]
    actual = json.loads((root / f"strokes/{c}.json").read_text(encoding="utf-8"))
    require(actual == converted and actual["kanji"] == c
            and actual["sourceRevision"] == KVG_REVISION
            and actual["strokeCount"] == len(actual["strokes"]) == meta["strokes"]
            and all(len(stroke["points"]) == generate_strokes.POINTS_PER_STROKE
                    for stroke in actual["strokes"])
            and draft["strokePaths"] == meta["strokes"]
            and draft["pointsPerPath"] == generate_strokes.POINTS_PER_STROKE
            and draft["exactPinnedConverterOutput"] is True,
            f"Stroke geometry differs from pinned converter output: {c}")


def audit_source_plan(root, batch, ledger, frozen, members, commit, source, before, current):
    folder = root / "docs" / "n1-sources"
    required_fields(frozen, {"sourceRows"}, "Source-plan frozen membership")
    require(len(members) == 1 and safe_identifier(members[0]) and len(members[0]) == 1,
            "Source-plan audit currently requires one frozen kanji")
    c = members[0]
    require(ledger["sourceCompletionPlan"] == f"batch-{batch}-source-completion-plan.json"
            and ledger["draftAudit"] == f"batch-{batch}-draft-audit.json"
            and ledger.get("sourceCompletionAudit") == f"batch-{batch}-source-completion-audit.json",
            "Unsupported source-plan evidence paths")
    runtime_audit = ledger.get("runtimeAudit", ledger["draftAudit"])
    original_audit = runtime_audit == ledger["draftAudit"]
    require(isinstance(runtime_audit, str) and (original_audit or re.fullmatch(
        rf"batch-{batch}-[a-z0-9]+(?:-[a-z0-9]+)*-audit\.json", runtime_audit)),
        "Unsupported runtime-audit evidence path")
    plan = json.loads((folder / ledger["sourceCompletionPlan"]).read_text(encoding="utf-8"))
    draft = json.loads((folder / runtime_audit).read_text(encoding="utf-8"))
    source_audit = json.loads((folder / ledger["sourceCompletionAudit"]).read_text(encoding="utf-8"))
    required_fields(plan, {"schemaVersion", "batch", "membership", "sourceRows",
                           "sourcePreparationComplete"}, "Source plan")
    required_fields(draft, {"schemaVersion", "batch", "runtimeAdditions", "baselineRuntimeEdits",
                            "contentVersion", "allMappedPairs", "activatedBaselinePairs",
                            "fullOnyomi", "fullKunyomi", "quizOnyomi", "quizKunyomi",
                            "directKanjiGuards", "directWordGuards", "curatedWrongChoices",
                            "strokePaths", "pointsPerPath", "exactPinnedConverterOutput",
                            "runtimeHashes", "sourcePlan", "frozenInputHashesVerified",
                            "exactSourceMembershipAndRawMetadataVerified"}, "Draft audit")
    required_fields(source_audit, {"schemaVersion", "batch"}, "Source-completion audit")
    if not original_audit:
        required_fields(ledger, {"runtimeAuditContentVersion"}, "Batch ledger")
        original_path = folder / ledger["draftAudit"]
        require(original_path.is_file(), "Original draft audit is missing")
        original = json.loads(original_path.read_text(encoding="utf-8"))
        required_fields(original, {"schemaVersion", "batch", "sourcePlan", "contentVersion"},
                        "Original draft audit")
        require(draft.get("supersedesDraftAudit") == ledger["draftAudit"]
                and ledger["runtimeAuditContentVersion"] == draft["contentVersion"]
                and original["schemaVersion"] == 1 and original["batch"] == batch
                and original["sourcePlan"] == ledger["sourceCompletionPlan"]
                and ledger.get("draftContentVersion", original["contentVersion"]) == original["contentVersion"],
                "Runtime audit does not identify its original draft and content version")
    require(plan["schemaVersion"] == draft["schemaVersion"] == source_audit["schemaVersion"] == 1
            and plan["batch"] == draft["batch"] == source_audit["batch"] == batch
            and plan["membership"] == members and plan["sourceRows"] == frozen["sourceRows"]
            and frozen["sourceRows"] == [row["sourceRow"] for row in frozen["members"]]
            and plan["sourcePreparationComplete"] is True
            and type(draft["frozenInputHashesVerified"]) is int and draft["frozenInputHashesVerified"] > 0
            and draft["exactSourceMembershipAndRawMetadataVerified"] is True
            and draft["sourcePlan"] == ledger["sourceCompletionPlan"],
            "Source-plan evidence identity differs")

    if "kanjiTeachingPlan" in plan and "kanjiPlan" not in plan:
        variant = "teaching"
        required_fields(plan, {"publishedBase", "kanjiTeachingPlan", "supportTeachingPlan",
                               "navigationAndBaselinePlan", "strokeAndFontPlan"}, "Source plan")
        require(plan["publishedBase"] == commit, "Source plan has a different published base")
        kanji_plan, support = plan["kanjiTeachingPlan"], plan["supportTeachingPlan"]
        navigation = plan["navigationAndBaselinePlan"]
        required_fields(kanji_plan, {"title", "jlpt", "tags", "strokes", "radical", "radicalNumber",
                                     "fullOnyomi", "fullKunyomi", "quizOnyomi", "quizKunyomi",
                                     "offeredOnKeys", "offeredKunKeys", "onRow", "kunRow",
                                     "curatedDistractors", "quizExclusions"}, "Kanji teaching plan")
        required_fields(support, {"newNecessaryArticles", "reusedSupportArticles", "word", "reading",
                                  "title", "type", "kanji", "tags", "quizExclusions"}, "Support plan")
        required_fields(navigation, {"runtimePathsToAddLater", "baselineRuntimePathsToChange",
                                     "proposedAllMappedPairs", "requiredDirections",
                                     "activatedBaselinePairs"}, "Navigation plan")
        require(isinstance(support["newNecessaryArticles"], list)
                and len(support["newNecessaryArticles"]) == 1 and support["reusedSupportArticles"] == [],
                "Unsupported source-plan support articles")
        word_plan = support
        word_article = support["newNecessaryArticles"][0]
        plan_pairs = navigation["proposedAllMappedPairs"]
        directions = navigation["requiredDirections"]
        planned_activated = navigation["activatedBaselinePairs"]
        changes = navigation["baselineRuntimePathsToChange"]
        require(changes == [], "Unsupported teaching-plan baseline edits")
        require(isinstance(kanji_plan["fullOnyomi"], list) and isinstance(kanji_plan["fullKunyomi"], list)
                and len(kanji_plan["fullOnyomi"]) == len(kanji_plan["fullKunyomi"]) == 1,
                "Unsupported teaching-plan reading rows")
        reading_rows = [("on", kanji_plan["onRow"]), ("kun", kanji_plan["kunRow"])]
        offered_plan = {"on": kanji_plan["offeredOnKeys"], "kun": kanji_plan["offeredKunKeys"]}
        full_plan = {"onyomi": kanji_plan["fullOnyomi"], "kunyomi": kanji_plan["fullKunyomi"]}
    elif "kanjiPlan" in plan and "kanjiTeachingPlan" not in plan:
        variant = "current"
        required_fields(plan, {"publishedBaseline", "sourceEvidence", "kanjiPlan", "supportPlan",
                               "linkPlan", "strokePlan"}, "Source plan")
        required_fields(draft, {"publishedBaseline", "membership", "sourceRow"}, "Draft audit")
        require(plan["publishedBaseline"] == draft["publishedBaseline"] == commit
                and draft["membership"] == members and draft["sourceRow"] == frozen["sourceRows"][0],
                "Source plan or draft has a different published base or membership")
        kanji_plan, support, navigation = plan["kanjiPlan"], plan["supportPlan"], plan["linkPlan"]
        required_fields(kanji_plan, {"article", "title", "jlpt", "tags", "strokes", "radical",
                                     "radicalNumber", "onyomi", "kunyomi", "quizOnyomi", "quizKunyomi",
                                     "offeredKeys", "readingRows", "curatedDistractors", "quizExclusions"},
                        "Kanji plan")
        required_fields(support, {"reused", "newNecessary"}, "Support plan")
        required_fields(navigation, {"allMappedPairs", "requiredDirections", "activatedBaselinePairs"},
                        "Link plan")
        require(kanji_plan["article"] == f"kanji/{c}.md"
                and isinstance(support["newNecessary"], list)
                and len(support["newNecessary"]) == 1 and support["reused"] == [],
                "Unsupported source-plan support articles")
        word_plan = support["newNecessary"][0]
        required_fields(word_plan, {"article", "word", "reading", "title", "type", "kanji", "tags",
                                    "entryId", "selectedSense", "quizExclusions"}, "Support word plan")
        word_article = word_plan["article"]
        plan_pairs = navigation["allMappedPairs"]
        directions = navigation["requiredDirections"]
        planned_activated = navigation["activatedBaselinePairs"]
        changes = draft["baselineRuntimeEdits"]
        require(isinstance(kanji_plan["readingRows"], list)
                and all(isinstance(row, dict) for row in kanji_plan["readingRows"]),
                "Invalid source-plan reading rows")
        reading_rows = [(row.get("kind"), row) for row in kanji_plan["readingRows"]]
        offered_plan = kanji_plan["offeredKeys"]
        full_plan = {"onyomi": kanji_plan["onyomi"], "kunyomi": kanji_plan["kunyomi"]}
    else:
        raise ValueError("Unsupported or incomplete source-plan schema")

    require(safe_identifier(word_plan["word"])
            and word_article == f"words/{word_plan['word']}.md",
            "Invalid support article identity")
    new_words = {word_article}
    additions = {f"kanji/{c}.md", f"strokes/{c}.json"} | new_words
    if variant == "teaching":
        require(isinstance(navigation["runtimePathsToAddLater"], list)
                and all(isinstance(name, str) for name in navigation["runtimePathsToAddLater"])
                and len(navigation["runtimePathsToAddLater"]) == len(additions)
                and set(navigation["runtimePathsToAddLater"]) == additions,
                "Source-plan runtime additions differ")
    required_fields(draft["runtimeAdditions"], {"files"}, "Draft runtime additions")
    require(all(isinstance(rows, list) for rows in draft["runtimeAdditions"].values())
            and all(isinstance(name, str) for name in draft["runtimeAdditions"]["files"])
            and len(draft["runtimeAdditions"]["files"]) == len(additions)
            and set(draft["runtimeAdditions"]["files"]) == additions
            and all(not rows for key, rows in draft["runtimeAdditions"].items() if key != "files")
            and isinstance(changes, list) and all(isinstance(name, str) for name in changes)
            and len(changes) == len(set(changes))
            and draft["baselineRuntimeEdits"] == changes,
            "Draft runtime changes differ from source plan")
    runtime_delta(before, current, additions, set(changes))
    require(isinstance(draft["runtimeHashes"], dict)
            and current["contentVersion"] == draft["contentVersion"]
            and (not original_audit
                 or ledger.get("draftContentVersion", draft["contentVersion"]) == draft["contentVersion"])
            and set(draft["runtimeHashes"]) == additions | set(changes)
            and all(current["files"].get(name) == value for name, value in draft["runtimeHashes"].items()),
            "Draft audit does not describe the current runtime snapshot")
    if changes:
        edit = navigation.get("exactReusedChange")
        required_fields(edit, {"article", "afterExistingLine", "addLine"}, "Reused edit")
        name = edit["article"]
        require(isinstance(name, str) and name.startswith("kanji/") and name.endswith(".md")
                and len(name[len("kanji/"):-len(".md")]) == 1
                and all(isinstance(edit[key], str) and edit[key] for key in ("afterExistingLine", "addLine"))
                and name in before["files"] and changes == [name],
                "Unsupported source-plan baseline edits")
        rows = [{"before": edit["afterExistingLine"],
                 "after": edit["afterExistingLine"] + "\n" + edit["addLine"]}]
        reused_changes(base_file(root, commit, edit["article"]),
                       (root / edit["article"]).read_text(encoding="utf-8"), rows)

    families = source_plan_packets(folder, batch, plan, source_audit, variant)
    if variant == "current":
        require(draft.get("distinctCompleteDictionaryFamiliesReproduced") == len(families),
                "Draft dictionary family count differs")
    word_meta = metadata(root, word_article)
    required_fields(word_meta, {"word", "reading", "title", "type", "kanji", "tags", "quiz_exclusions"},
                    "Support metadata")
    require(all(word_meta[key] == word_plan[key]
                for key in ("word", "reading", "title", "type", "kanji", "tags"))
            and word_meta["quiz_exclusions"] == word_plan["quizExclusions"] == draft["directWordGuards"]
            and isinstance(word_meta["kanji"], list)
            and all(isinstance(item, str) and len(item) == 1 for item in word_meta["kanji"])
            and len(word_meta["kanji"]) == len(set(word_meta["kanji"]))
            and "jlpt" not in word_meta, "Support word identity or exclusions differ")
    if variant == "current":
        selected_ids = [word_plan["entryId"]]
        sense = word_plan["selectedSense"]
    else:
        selected_ids = list(families)
        sense = None
    require(selected_ids and all(isinstance(item, str) and item.isdigit() for item in selected_ids)
            and set(selected_ids) <= families.keys()
            and any(teachable_lexical_pair(families[i], word_meta["word"], word_meta["reading"], sense)
                    for i in selected_ids), f"Support identity/restrictions mismatch: {word_article}")

    pairs = recorded_pairs(plan_pairs, "source-plan reciprocal pairs")
    require(pairs == recorded_pairs(draft["allMappedPairs"], "draft reciprocal pairs"),
            "Reciprocal mappings differ")
    component_pairs = {(component, word_article) for component in word_meta["kanji"]
                       if f"kanji/{component}.md" in current["files"]}
    require(set(pairs) == component_pairs
            and all(component in members or f"kanji/{component}.md" in before["files"]
                    for component, _ in pairs), "Reciprocal mappings do not cover existing components")
    expected_directions = {(f"kanji/{component}.md", article)
                           for component, article in pairs}
    expected_directions |= {(article, f"kanji/{component}.md") for component, article in pairs}
    require(isinstance(directions, list), "Required link directions must be a list")
    actual_directions = []
    for direction in directions:
        required_fields(direction, {"from", "to"}, "Required link direction")
        origin, target = direction["from"], direction["to"]
        href = direction.get("href", direction.get("relative"))
        require((origin, target) in expected_directions and href == f"../{target}",
                "Invalid required reciprocal link direction")
        lines = [line for line in (root / origin).read_text(encoding="utf-8").splitlines()
                 if f"({href})" in line]
        require(lines and (not direction.get("reading")
                           or any(direction["reading"] in line for line in lines)),
                f"Missing reciprocal link: {origin} / {target}")
        actual_directions.append((origin, target))
    require(len(actual_directions) == len(set(actual_directions))
            and set(actual_directions) == expected_directions
            and draft.get("requiredLinkDirectionsVerified") == len(expected_directions),
            "Required reciprocal link directions differ")
    candidates = json.loads((folder / "baseline-word-candidates.json").read_text(encoding="utf-8"))
    activated = {(row["kanji"], row["article"]) for row in candidates if row["kanji"] in members}
    require(activated <= set(pairs)
            and set(recorded_pairs(planned_activated, "planned activated pairs")) == activated
            and set(recorded_pairs(draft["activatedBaselinePairs"], "draft activated pairs")) == activated,
            "Activated baseline pair missing from mappings")

    meta = metadata(root, f"kanji/{c}.md")
    required_fields(meta, {"kanji", "title", "jlpt", "tags", "strokes", "radical", "radicalNumber",
                           "onyomi", "kunyomi", "quizOnyomi", "quizKunyomi", "distractors",
                           "quiz_exclusions"}, "Kanji metadata")
    for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        require(meta[field] == source[c]["metadata"][field], f"Source metadata changed: {c}")
    require(all(meta[field] == kanji_plan[field]
                for field in ("title", "jlpt", "tags", "strokes", "radical", "radicalNumber"))
            and meta["jlpt"] == 1 and "jlpt-n1" in meta["tags"]
            and f"grade-{source[c]['metadata']['grade']}" in meta["tags"]
            and meta["onyomi"] == full_plan["onyomi"] == draft["fullOnyomi"]
            and meta["kunyomi"] == full_plan["kunyomi"] == draft["fullKunyomi"],
            f"Kanji plan or source metadata differs: {c}")
    body = (root / f"kanji/{c}.md").read_text(encoding="utf-8")
    require("## Readings\n" in body and "## Common words" in body, f"Missing reading sections: {c}")
    table = body.split("## Readings\n", 1)[1].split("## Common words", 1)[0]
    decisions = []
    for kind, row in reading_rows:
        required_fields(row, {"reading", "type"} if variant == "teaching" else
                        {"raw", "kind", "selected"}, "Reading decision")
        raw = row["reading"] if variant == "teaching" else row["raw"]
        require(isinstance(kind, str) and kind in {"on", "kun"} and isinstance(raw, str) and raw
                and (row["type"] == kind if variant == "teaching" else type(row["selected"]) is bool),
                f"Invalid reading decision: {c}")
        selected = (raw in kanji_plan["quizOnyomi" if kind == "on" else "quizKunyomi"]
                    if variant == "teaching" else row["selected"])
        reason = row.get("usefulness") if selected else row.get("disposition")
        require(isinstance(reason, str) and reason.strip(), f"Reading decision lacks a reason: {c} {raw}")
        lines = [line for line in table.splitlines() if line.startswith(f"| {raw} |")]
        require(len(lines) == 1, f"Missing/duplicate reading row: {c} {raw}")
        if selected:
            required_fields(row, {"example", "link"} | ({"kana"} if variant == "teaching" else {"reading"}),
                            "Selected reading")
            example_reading = row["kana"] if variant == "teaching" else row["reading"]
            require(row["example"] == word_meta["word"] and example_reading == word_meta["reading"]
                    and row["link"] == f"../{word_article}" and (c, word_article) in pairs
                    and f"({row['link']})" in lines[0] and row["example"] in lines[0]
                    and example_reading in lines[0],
                    f"Selected reading lacks mapped table support: {c}")
        if variant == "teaching" and "search-only" in row.get("qualification", "").lower():
            require(not selected and "search-only" in lines[0].lower()
                    and any(any(k.findtext("keb") == row.get("word")
                                and any("search-only" in (v.text or "").lower()
                                        for v in k.findall("ke_inf"))
                                for k in entry.findall("k_ele"))
                            and lexical_pair(entry, row.get("word"), row.get("kana"))
                            for entry in families.values()),
                    f"Search-only reading unqualified/offered: {c}")
        decisions.append((kind, raw, selected))
    expected = [(kind, raw) for kind, field in (("on", "onyomi"), ("kun", "kunyomi"))
                for raw in source[c]["metadata"][field]]
    require([(kind, raw) for kind, raw, _ in decisions] == expected,
            "Full reading dispositions/order differ from source")
    required_fields(offered_plan, {"on", "kun"}, "Offered reading keys")
    offered = 0
    for kind, field in (("on", "onyomi"), ("kun", "kunyomi")):
        quiz_field = "quiz" + field[0].upper() + field[1:]
        selected = quiz_readings(meta, field)
        require(selected == kanji_plan[quiz_field] == draft[quiz_field]
                == [raw for row_kind, raw, included in decisions if row_kind == kind and included],
                f"Curated subset differs from decisions: {c}")
        draft_key = ("offeredOnKeys" if kind == "on" else "offeredKunKeys") + (
            "MirrorNotAppExecution" if variant == "current" else "")
        require(draft_key in draft and offered_keys(selected) == offered_plan[kind] == draft[draft_key],
                f"Offered key ledger mismatch: {c}")
        offered += len(offered_keys(selected))

    distractors = kanji_plan["curatedDistractors"]
    require(isinstance(distractors, list) and len(distractors) == 3,
            "Invalid curated distractor plan")
    for row in distractors:
        required_fields(row, {"kanji", "displayedTitle" if variant == "teaching" else "actualTitle"},
                        "Curated distractor")
    distractor_ids = [row["kanji"] for row in distractors]
    distractor_titles = [row["displayedTitle" if variant == "teaching" else "actualTitle"]
                         for row in distractors]
    require(meta["distractors"] == draft["curatedWrongChoices"] == distractor_ids
            and all(safe_identifier(item) and len(item) == 1 for item in distractor_ids)
            and len(set(distractor_ids)) == 3 and c not in distractor_ids
            and meta["quiz_exclusions"] == kanji_plan["quizExclusions"] == draft["directKanjiGuards"],
            f"Quiz labels or direct exclusions differ: {c}")
    choices = [c] + distractor_ids
    choice_metadata = {item: metadata(root, f"kanji/{item}.md") for item in choices}
    labels = [choice_metadata[item].get("title") for item in choices]
    require(all(choice_metadata[item].get("kanji") == item for item in choices)
            and all(isinstance(label, str) and label.strip() for label in labels)
            and len(labels) == len({label.strip().casefold() for label in labels})
            and distractor_titles == labels[1:],
            f"Quiz labels differ: {c}")
    for choice in choices:
        exclusions = choice_metadata[choice].get("quiz_exclusions", [])
        require(isinstance(exclusions, list) and all(isinstance(item, str) for item in exclusions)
                and len(exclusions) == len(set(exclusions))
                and choice not in exclusions, f"Invalid direct kanji exclusions: {choice}")
    for i, first in enumerate(choices):
        exclusions = choice_metadata[first].get("quiz_exclusions", [])
        for second in choices[i + 1:]:
            require(second not in exclusions
                    and first not in choice_metadata[second].get("quiz_exclusions", []),
                    f"Curated choices contain a directly excluded pair: {first} / {second}")
    for kind, target, exclusions in (("kanji", c, meta["quiz_exclusions"]),
                                     ("words", word_meta["word"], word_meta["quiz_exclusions"])):
        require(isinstance(exclusions, list) and all(isinstance(item, str) for item in exclusions)
                and len(exclusions) == len(set(exclusions))
                and target not in exclusions, f"Invalid direct {kind} exclusions")
        for excluded in exclusions:
            require(safe_identifier(excluded)
                    and (root / f"{kind}/{excluded}.md").is_file(),
                    f"Missing direct {kind} exclusion: {excluded}")
            id_field = "kanji" if kind == "kanji" else "word"
            require(metadata(root, f"{kind}/{excluded}.md").get(id_field) == excluded,
                    f"Direct {kind} exclusion identity differs: {excluded}")
    snapshot_name = "docs/n1-source-snapshot.json"
    snapshot_text = (root / snapshot_name).read_text(encoding="utf-8")
    require(snapshot_text == base_file(root, commit, snapshot_name), "Immutable source snapshot changed")
    audit_pinned_strokes(root, folder, batch, c, meta, source[c], json.loads(snapshot_text),
                         plan, draft, variant, commit)
    return {"batch": batch, "baseCommit": commit, "draftKanji": 1,
            "newWords": len(new_words), "changedReusedArticles": len(changes),
            "requiredReciprocalPairs": len(pairs), "activatedBaselinePairs": len(activated),
            "readingDispositions": len(decisions), "curatedOfferedKeys": offered,
            "sourceOnlyOfferedKeys": 0, "dictionaryFamilies": len(families),
            "exactBaseRuntimePreservedOutsideRecordedChanges": True,
            "manifestFresh": True, "contentVersion": current["contentVersion"],
            "limits": "Mechanical source-plan draft audit, not independent source extraction, "
                      "lexical-allocation/naturalness verification, independent review, "
                      "native/phone acceptance or publication."}


def audit(root, batch):
    require(isinstance(batch, str) and len(batch) == 3 and batch.isascii() and batch.isdigit(),
            "Batch must be a three-digit number")
    folder = root / "docs" / "n1-sources"
    ledger = json.loads((folder / f"batch-{batch}-progress.json").read_text(encoding="utf-8"))
    frozen = json.loads((folder / f"batch-{batch}-membership.json").read_text(encoding="utf-8"))
    required_fields(ledger, {"batch", "membership", "baseCommit", "drafted"}, "Batch ledger")
    required_fields(frozen, {"batch", "membership", "baseCommit", "members"},
                    "Frozen membership")
    if "supportMappings" in ledger:
        required_fields(ledger, {"requiredReciprocalPairs", "changedReusedPassages", "wordQuizAudit",
                                 "dictionaryPackets", "readingDispositions", "curatedProjection", "quizAudit"},
                        "Legacy batch ledger")
    else:
        required_fields(ledger, {"sourceCompletionPlan", "sourceCompletionAudit", "draftAudit"},
                        "Unsupported or incomplete batch ledger")
    members, commit = ledger["membership"], ledger["baseCommit"]
    require(isinstance(commit, str) and ledger["batch"] == frozen["batch"] == batch
            and commit == frozen["baseCommit"]
            and len(commit) == 40 and all(c in "0123456789abcdef" for c in commit),
            "Invalid batch/base identity")
    require(isinstance(members, list) and all(isinstance(c, str) and c for c in members)
            and isinstance(frozen["members"], list)
            and all(isinstance(row, dict) and {"kanji", "sourceRow"} <= row.keys()
                    for row in frozen["members"])
            and 0 < len(members) <= 15 and len(set(members)) == len(members)
            and members == frozen["membership"]
            and members == [row["kanji"] for row in frozen["members"]]
            and ledger["drafted"] == members, "Incomplete or changed frozen membership")
    source_name = "docs/n1-sources/source-index.json"
    require((root / source_name).read_text(encoding="utf-8")
            == base_file(root, commit, source_name), "Immutable source index changed")
    source = {r["kanji"]: r for r in json.loads((root / source_name).read_text(encoding="utf-8"))}
    for row in frozen["members"]:
        require(source[row["kanji"]]["sourceRow"] == row["sourceRow"],
                "Frozen source-row identity changed")
    current = build_manifest(root)
    require(json.loads((root / "manifest.json").read_text(encoding="utf-8")) == current,
            "Manifest is stale")
    before = json.loads(base_file(root, commit, "manifest.json"))
    if "supportMappings" not in ledger:
        return audit_source_plan(root, batch, ledger, frozen, members, commit, source, before, current)
    mappings = ledger["supportMappings"]
    pairs = {(r["kanji"], r["article"]) for r in mappings}
    recorded_pairs = [tuple(p) for p in ledger["requiredReciprocalPairs"]]
    require(len(mappings) == len(pairs) == len(recorded_pairs)
            and pairs == set(recorded_pairs), "Reciprocal mappings differ")
    new_words = {r["article"] for r in mappings if r["newArticle"]}
    additions = {f"{kind}/{c}.{suffix}" for c in members
                 for kind, suffix in (("kanji", "md"), ("strokes", "json"))} | new_words
    changes = {r["article"] for r in ledger["changedReusedPassages"]}
    runtime_delta(before, current, additions, changes)
    for name in changes:
        rows = [r for r in ledger["changedReusedPassages"] if r["article"] == name]
        exclusion_rows = [r for r in ledger["wordQuizAudit"]["directExclusions"]
                          if f"words/{r['word']}.md" == name]
        require(len(exclusion_rows) <= 1, "Duplicate reused exclusion decision")
        reused_changes(base_file(root, commit, name),
                       (root / name).read_text(encoding="utf-8"), rows,
                       exclusion_rows[0]["exclude"] if exclusion_rows else None)
    families = {}
    for packet in ledger["dictionaryPackets"]:
        selection = json.loads((folder / packet["selection"]).read_text(encoding="utf-8"))
        entries = ET.parse(folder / packet["xml"]).getroot().findall("entry")
        ids = [e.findtext("ent_seq") for e in entries]
        require(ids == selection["entryIds"] and len(ids) == len(set(ids)),
                "Dictionary packet membership/order differs")
        families.update(zip(ids, entries))
    for row in mappings:
        c, name = row["kanji"], row["article"]
        require(c in members and name.startswith("words/") and name.endswith(".md"),
                "Invalid support mapping")
        meta = metadata(root, name)
        require(meta["reading"] == row["primaryReading"]
                and bool(row["newArticle"]) == (name in new_words)
                and row["entryIds"] and set(row["entryIds"]) <= families.keys()
                and any(lexical_pair(families[i], meta["word"], meta["reading"])
                        for i in row["entryIds"]), f"Support identity/restrictions mismatch: {name}")
        require(f"(../kanji/{c}.md)" in (root / name).read_text(encoding="utf-8")
                and f"(../{name})" in (root / f"kanji/{c}.md").read_text(encoding="utf-8"),
                f"Missing reciprocal link: {c} / {name}")
    candidates = json.loads((folder / "baseline-word-candidates.json").read_text(encoding="utf-8"))
    activated = {(r["kanji"], r["article"]) for r in candidates if r["kanji"] in members}
    require(activated <= pairs, "Activated baseline pair missing from mappings")
    decisions = ledger["readingDispositions"]
    identities = [(r["kanji"], r["kind"], r["reading"]) for r in decisions]
    expected = [(c, kind, reading) for c in members
                for kind, field in (("on", "onyomi"), ("kun", "kunyomi"))
                for reading in source[c]["metadata"][field]]
    require(identities == expected, "Full reading dispositions/order differ from source")
    projections = ledger["curatedProjection"]
    require([r["kanji"] for r in projections] == members, "Curated membership/order differs")
    offered = 0
    for c, projection in zip(members, projections):
        meta = metadata(root, f"kanji/{c}.md")
        for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
            require(meta[field] == source[c]["metadata"][field], f"Source metadata changed: {c}")
        require(meta["jlpt"] == 1 and "jlpt-n1" in meta["tags"]
                and f"grade-{source[c]['metadata']['grade']}" in meta["tags"],
                f"Level/grade changed: {c}")
        strokes = json.loads((root / f"strokes/{c}.json").read_text(encoding="utf-8"))
        require(strokes["kanji"] == c and strokes["sourceRevision"] == KVG_REVISION
                and strokes["strokeCount"] == len(strokes["strokes"]) == meta["strokes"],
                f"Stroke identity/count/revision mismatch: {c}")
        body = (root / f"kanji/{c}.md").read_text(encoding="utf-8")
        table = body.split("## Readings\n", 1)[1].split("## Common words", 1)[0]
        for row in (r for r in decisions if r["kanji"] == c):
            require(type(row["selected"]) is bool and row["reason"].strip()
                    and set(row["entryIds"]) <= families.keys(), f"Invalid reading decision: {c}")
            lines = [line for line in table.splitlines()
                     if line.startswith(f"| {row['reading']} |")]
            require(len(lines) == 1, f"Missing/duplicate reading row: {c} {row['reading']}")
            if row.get("sourceOnly"):
                require(not row["selected"] and "source-only" in lines[0],
                        f"Source-only reading unqualified/offered: {c}")
            if row["selected"]:
                require(row["entryIds"] and (c, row["article"]) in pairs
                        and f"(../{row['article']})" in lines[0],
                        f"Selected reading lacks mapped table support: {c}")
        for kind, field, key in (("on", "onyomi", "onKeys"), ("kun", "kunyomi", "kunKeys")):
            selected = quiz_readings(meta, field)
            quiz_field = "quiz" + field[0].upper() + field[1:]
            require(meta[quiz_field] == projection[quiz_field]
                    == [r["reading"] for r in decisions
                        if r["kanji"] == c and r["kind"] == kind and r["selected"]],
                    f"Curated subset differs from decisions: {c}")
            keys = offered_keys(selected)
            require(keys == projection[key], f"Offered key ledger mismatch: {c}")
            offered += len(keys)
        quiz = ledger["quizAudit"][c]
        require(meta["title"] == quiz["title"] and meta["distractors"] == quiz["distractors"]
                and len(set(meta["distractors"])) == 3
                and quiz["labels"] == [metadata(root, f"kanji/{d}.md")["title"]
                                       for d in meta["distractors"]], f"Quiz labels differ: {c}")
    for row in ledger["wordQuizAudit"]["directExclusions"]:
        require(metadata(root, f"words/{row['word']}.md")["quiz_exclusions"] == row["exclude"],
                "Word exclusion ledger mismatch")
    return {"batch": batch, "baseCommit": commit, "draftKanji": len(members),
            "newWords": len(new_words), "changedReusedArticles": len(changes),
            "requiredReciprocalPairs": len(pairs), "activatedBaselinePairs": len(activated),
            "readingDispositions": len(decisions), "curatedOfferedKeys": offered,
            "sourceOnlyOfferedKeys": 0, "dictionaryFamilies": len(families),
            "exactBaseRuntimePreservedOutsideRecordedChanges": True,
            "manifestFresh": True, "contentVersion": current["contentVersion"],
            "limits": "Mechanical draft audit, not lexical-allocation/naturalness verification, independent review, native/phone acceptance or publication."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", required=True)
    args = parser.parse_args()
    print(json.dumps(audit(ROOT, args.batch), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
