#!/usr/bin/env python3
"""Validate the versioned grammar exercise sets in grammar/*.json."""
import json
import re
import sys
import unicodedata
from pathlib import Path
from validate_grammar_vocabulary import vocabulary_problems

ROOT = Path(__file__).resolve().parent.parent
ID = re.compile(r"^[a-z0-9-]+$")
ARTICLE = re.compile(r"^articles/[a-z0-9-]+\.md$")
SET_KEYS = {"schemaVersion", "id", "title", "article", "constructions", "relationships", "exercises"}


def check_grammar(err, root: Path = ROOT) -> int:
    report = err
    failed = set()
    parsed = {}

    def err(path, message):
        failed.add(path)
        report(path, message)

    files = sorted((root / "grammar").glob("*.json"))
    set_ids: set[str] = set()
    exercise_ids: set[str] = set()
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
            err(path, f"not valid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            err(path, "must be a JSON object")
            continue
        parsed[path] = data
        if set(data) - {"introductionGroups"} != SET_KEYS:
            err(path, f"fields must be {sorted(SET_KEYS)}, with optional introductionGroups")
        set_id = data.get("id")
        if not isinstance(set_id, str) or not ID.fullmatch(set_id) or set_id != path.stem:
            err(path, "'id' must be a lowercase slug matching the file name")
            continue
        if set_id in set_ids:
            err(path, f"duplicate set ID '{set_id}'")
            continue
        set_ids.add(set_id)
        if data.get("schemaVersion") != 1:
            err(path, "'schemaVersion' must be 1")
        if not isinstance(data.get("title"), str) or not data["title"].strip():
            err(path, "missing 'title'")
        article = data.get("article")
        if not isinstance(article, str) or not ARTICLE.fullmatch(article):
            err(path, "'article' must be an articles/<slug>.md path")
        elif not (root / article).is_file():
            err(path, f"linked article '{article}' does not exist")
        constructions = data.get("constructions")
        if not isinstance(constructions, list) or len(constructions) < 2:
            err(path, "'constructions' must contain at least two entries")
            continue
        construction_ids: set[str] = set()
        for item in constructions:
            if not isinstance(item, dict) or set(item) != {"id", "label"}:
                err(path, "each construction needs exactly 'id' and 'label'")
                continue
            ident = item["id"]
            if not isinstance(ident, str) or not ID.fullmatch(ident) or ident in construction_ids:
                err(path, f"invalid or duplicate construction ID '{ident}'")
            else:
                construction_ids.add(ident)
            if not isinstance(item["label"], str) or not item["label"].strip():
                err(path, f"{ident}: missing construction label")
        relationships = data.get("relationships")
        if not isinstance(relationships, list) or not relationships:
            err(path, "'relationships' must be a non-empty list")
            continue
        relation_map: dict[str, set[str]] = {}
        for item in relationships:
            if not isinstance(item, dict) or set(item) != {"id", "label", "constructions"}:
                err(path, "each relationship needs exactly 'id', 'label' and 'constructions'")
                continue
            ident, members = item["id"], item["constructions"]
            if not isinstance(ident, str) or not ID.fullmatch(ident) or ident in relation_map:
                err(path, f"invalid or duplicate relationship ID '{ident}'")
                continue
            if not isinstance(item["label"], str) or not item["label"].strip():
                err(path, f"{ident}: missing relationship label")
            if (not isinstance(members, list) or len(members) < 2
                    or any(not isinstance(member, str) for member in members)
                    or len(set(members)) != len(members) or not set(members) <= construction_ids):
                err(path, f"{ident}: relationship needs at least two distinct known constructions")
                continue
            relation_map[ident] = set(members)
        exercises = data.get("exercises")
        if not isinstance(exercises, list) or not exercises:
            err(path, "'exercises' must be a non-empty list")
            continue
        covered = {ident: set() for ident in relation_map}
        for exercise in exercises:
            if not isinstance(exercise, dict) or set(exercise) - {"jlpt", "vocabulary", "additionalCorrectOptions"} != {
                    "id", "target", "relationship", "prompt", "translation", "evidence",
                    "explanation", "answer", "acceptedAnswers", "options"}:
                err(path, "each exercise has an invalid shape")
                continue
            ident = exercise["id"]
            for problem in vocabulary_problems(exercise, root):
                err(path, f"{ident}: {problem}")
            if "jlpt" in exercise and (type(exercise["jlpt"]) is not int or not 1 <= exercise["jlpt"] <= 5):
                err(path, f"{ident}: 'jlpt' must be an integer from 1 to 5, or omitted")
            if not isinstance(ident, str) or not ID.fullmatch(ident) or ident in exercise_ids:
                err(path, f"invalid or duplicate exercise ID '{ident}'")
            else:
                exercise_ids.add(ident)
            target, relation = exercise["target"], exercise["relationship"]
            if not isinstance(target, str) or target not in construction_ids:
                err(path, f"{ident}: unknown target construction")
            if not isinstance(relation, str) or relation not in relation_map or not isinstance(target, str) or target not in relation_map.get(relation, set()):
                err(path, f"{ident}: target is not in its relationship")
            else:
                covered[relation].add(target)
            if not isinstance(exercise["prompt"], str) or exercise["prompt"].count("____") != 1:
                err(path, f"{ident}: prompt needs exactly one ____ blank")
            for field in ("translation", "evidence", "explanation"):
                if not isinstance(exercise[field], str) or not exercise[field].strip():
                    err(path, f"{ident}: missing '{field}'")
            if exercise["answer"] != target:
                err(path, f"{ident}: answer must equal target")
            accepted = exercise["acceptedAnswers"]
            if not isinstance(accepted, list) or not accepted or any(not isinstance(v, str) or not v.strip() for v in accepted):
                err(path, f"{ident}: acceptedAnswers must be non-empty strings")
                accepted = []
            options = exercise["options"]
            if not isinstance(options, list) or len(options) < 2 or any(
                    not isinstance(option, dict) or set(option) != {"id", "label", "rationale"} for option in options):
                err(path, f"{ident}: options need at least two entries with id, label and rationale")
                continue
            option_ids = [option["id"] for option in options]
            if any(not isinstance(option_id, str) for option_id in option_ids) or len(option_ids) != len(set(option_ids)) or target not in option_ids:
                err(path, f"{ident}: options need unique IDs including the target")
            for option in options:
                if not isinstance(option["id"], str) or option["id"] not in relation_map.get(relation, set()):
                    err(path, f"{ident}: option '{option['id']}' is outside its relationship")
                for field in ("label", "rationale"):
                    if not isinstance(option[field], str) or not option[field].strip():
                        err(path, f"{ident}: option '{option['id']}' is missing '{field}'")
            normalized_answers = {unicodedata.normalize("NFKC", value.strip()) for value in accepted}
            normalized_labels = [
                unicodedata.normalize("NFKC", option["label"].strip())
                for option in options if isinstance(option["label"], str)
            ]
            if len(normalized_labels) != len(set(normalized_labels)):
                err(path, f"{ident}: option labels must remain distinct after answer normalization")
            for option in options:
                if (option["id"] != target and isinstance(option["label"], str)
                        and unicodedata.normalize("NFKC", option["label"].strip()) in normalized_answers):
                    err(path, f"{ident}: distractor label must not be an accepted typed answer")
            answer_labels = [option["label"] for option in options if option["id"] == target]
            if len(answer_labels) == 1 and answer_labels[0] not in accepted:
                err(path, f"{ident}: acceptedAnswers must include the answer option label")
            _check_additional_options(err, path, exercise, normalized_answers, normalized_labels)
        for ident, members in relation_map.items():
            if not members <= covered.get(ident, set()):
                err(path, f"{ident}: exercises must target every construction in the relationship")
    groups = {}
    for path, data in parsed.items():
        if path not in failed:
            groups[path] = _check_groups(err, path, data)
    groups = {path: items for path, items in groups.items() if path not in failed}
    _check_group_references(err, groups)
    return len(files)


def _check_additional_options(err, path, exercise, accepted, labels):
    additional = exercise.get("additionalCorrectOptions", [])
    ident = exercise["id"]
    if not isinstance(additional, list):
        err(path, f"{ident}: additionalCorrectOptions must be an array, or omitted")
        return
    seen_ids = {option["id"] for option in exercise["options"] if isinstance(option["id"], str)}
    seen_labels = set(labels)
    for option in additional:
        if not isinstance(option, dict) or set(option) != {"id", "label", "rationale"}:
            err(path, f"{ident}: additional correct options need exactly id, label and rationale")
            continue
        option_id = option["id"]
        if not isinstance(option_id, str) or not ID.fullmatch(option_id) or option_id in seen_ids:
            err(path, f"{ident}: additional option IDs must be distinct lowercase slugs")
        else:
            seen_ids.add(option_id)
        if any(not isinstance(option[key], str) or not option[key].strip() for key in ("label", "rationale")):
            err(path, f"{ident}: additional options need nonblank labels and rationales")
            continue
        label = unicodedata.normalize("NFKC", option["label"].strip())
        if label in seen_labels:
            err(path, f"{ident}: all option labels must remain distinct after answer normalization")
        seen_labels.add(label)
        if label not in accepted:
            err(path, f"{ident}: additional correct option label must be an accepted typed answer")


def _shape(value, required, optional=()):
    return isinstance(value, dict) and set(required) <= set(value) <= set(required) | set(optional)


def _ids(values):
    return (isinstance(values, list) and all(isinstance(value, str) and ID.fullmatch(value) for value in values)
            and len(set(values)) == len(values))


def _strings(value, keys):
    return all(isinstance(value.get(key), str) and value[key].strip() for key in keys)


def _check_groups(err, path, data):
    groups = data.get("introductionGroups", [])
    if not isinstance(groups, list):
        err(path, "introductionGroups must be an array, or omitted")
        return []
    owned, ids = set(), set()
    exercises = {exercise["id"]: exercise for exercise in data["exercises"]}
    for group in groups:
        if not _shape(group, ("id", "label", "facets", "members"), ("next", "requires")):
            err(path, "invalid introduction group shape")
            continue
        if not _strings(group, ("id", "label")) or not ID.fullmatch(group["id"]) or group["id"] in ids:
            err(path, "invalid or duplicate introduction group ID/label")
            continue
        ids.add(group["id"])
        facets, members = group["facets"], group["members"]
        if (not isinstance(facets, list) or not facets
                or any(not _shape(facet, ("id", "label")) or not _strings(facet, ("id", "label")) for facet in facets)):
            err(path, f"{group['id']}: invalid facets")
            continue
        facet_ids = [facet["id"] for facet in facets]
        if not _ids(facet_ids):
            err(path, f"{group['id']}: invalid or duplicate facets")
            continue
        if not isinstance(members, list) or not members:
            err(path, f"{group['id']}: members must not be empty")
            continue
        valid_members = []
        for member in members:
            if (not _shape(member, ("exerciseId", "facetId", "exampleKey"))
                    or not _strings(member, ("exerciseId", "facetId", "exampleKey"))
                    or any(not ID.fullmatch(value) for value in member.values())):
                err(path, f"{group['id']}: invalid member")
                continue
            if member["exerciseId"] not in exercises or member["facetId"] not in facet_ids:
                err(path, f"{group['id']}: member needs a local exercise and facet")
                continue
            if member["exerciseId"] in owned:
                err(path, f"{group['id']}: duplicate exercise ownership")
            owned.add(member["exerciseId"])
            valid_members.append(member)
        for facet in facet_ids:
            own = [member for member in valid_members if member["facetId"] == facet]
            if len({member["exampleKey"] for member in own}) < 2:
                err(path, f"{group['id']}/{facet}: needs two distinct example keys")
            if len({exercises[member["exerciseId"]]["target"] for member in own}) != 1:
                err(path, f"{group['id']}/{facet}: members must target one answer class")
        requires = group.get("requires", [])
        if not _ids(requires) or group["id"] in requires:
            err(path, f"{group['id']}: requires needs distinct non-self group-ID strings")
        links = group.get("next", [])
        if (not isinstance(links, list) or any(
                not _shape(link, ("groupId", "importance", "reason"))
                or not _strings(link, ("groupId", "reason"))
                or type(link.get("importance")) is not int or not 1 <= link["importance"] <= 3 for link in links)):
            err(path, f"{group['id']}: invalid recommendation shape/importance")
        elif not _ids([link["groupId"] for link in links]) or any(link["groupId"] == group["id"] for link in links):
            err(path, f"{group['id']}: invalid, duplicate or self recommendation")
    return groups


def _check_group_references(err, by_file):
    owners = {}
    for path, groups in by_file.items():
        for group in groups:
            owners.setdefault(group["id"], []).append(path)
    duplicates = {path for paths in owners.values() if len(paths) > 1 for path in paths}
    for path in duplicates:
        err(path, "duplicate source-global group ID")
    kept = {path: groups for path, groups in by_file.items() if path not in duplicates}
    while True:
        groups = {group["id"]: group for items in kept.values() for group in items}
        remaining = {ident: len(group.get("requires", [])) for ident, group in groups.items()}
        dependents = {}
        for ident, group in groups.items():
            for required in group.get("requires", []):
                dependents.setdefault(required, []).append(ident)
        ready = [ident for ident, count in remaining.items() if count == 0]
        while ready:
            ident = ready.pop()
            del remaining[ident]
            for dependent in dependents.get(ident, []):
                remaining[dependent] -= 1
                if remaining[dependent] == 0:
                    ready.append(dependent)
        rejected = {path for path, items in kept.items() if any(group["id"] in remaining for group in items)}
        if not rejected:
            break
        for path in rejected:
            err(path, "missing/cyclic prerequisite chain")
            del kept[path]
    known = {group["id"] for items in kept.values() for group in items}
    for path, items in kept.items():
        for group in items:
            for link in group.get("next", []):
                if link["groupId"] not in known:
                    print(f"warning: {path}: missing optional next target '{link['groupId']}' will be dropped by the app", file=sys.stderr)
