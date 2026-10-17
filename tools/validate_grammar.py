#!/usr/bin/env python3
"""Validate the versioned grammar exercise sets in grammar/*.json."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ID = re.compile(r"^[a-z0-9-]+$")
ARTICLE = re.compile(r"^articles/[a-z0-9-]+\.md$")
SET_KEYS = {"schemaVersion", "id", "title", "article", "constructions", "relationships", "exercises"}


def check_grammar(err, root: Path = ROOT) -> int:
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
        if set(data) != SET_KEYS:
            err(path, f"fields must be exactly {sorted(SET_KEYS)}")
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
            if not isinstance(exercise, dict) or set(exercise) != {
                    "id", "target", "relationship", "prompt", "translation", "evidence",
                    "explanation", "answer", "acceptedAnswers", "options"}:
                err(path, "each exercise has an invalid shape")
                continue
            ident = exercise["id"]
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
        for ident, members in relation_map.items():
            if not members <= covered.get(ident, set()):
                err(path, f"{ident}: exercises must target every construction in the relationship")
    return len(files)
