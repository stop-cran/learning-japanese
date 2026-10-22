"""Revision-bound vocabulary coverage inventory and reviewed-segment authoring."""

import argparse
import hashlib
import json
from pathlib import Path

from validate_grammar_vocabulary import prompt_hash, vocabulary_problems

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = Path("docs") / "grammar-vocabulary-review.json"
EXCLUSIONS = {"function", "grammar-target", "punctuation", "supplied-reading"}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def context_hash(exercise):
    return digest({k: v for k, v in exercise.items() if k not in {"vocabulary", "jlpt"}})


def corpus(root):
    result = {}
    for path in sorted((root / "grammar").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for exercise in data["exercises"]:
            key = (path.name, exercise["id"])
            if key in result:
                raise ValueError(f"Duplicate exercise: {key}")
            result[key] = exercise
    return result


def initial_inventory(root, revision):
    return {
        "schemaVersion": 1,
        "baselineRevision": revision,
        "stage": "pilot",
        "records": [
            {"file": name, "exerciseId": identity, "promptSha256": prompt_hash(e["prompt"]),
             "contextSha256": context_hash(e), "status": "pending"}
            for (name, identity), e in corpus(root).items()
        ],
    }


def annotations(prompt, segments):
    spans, exclusions, text = [], [], ""
    for segment in segments:
        if not isinstance(segment, list) or not all(isinstance(v, str) and v for v in segment):
            raise ValueError("Each reviewed segment must contain nonempty strings")
        start = len(text)
        text += segment[0]
        interval = {"start": start, "end": len(text), "text": segment[0]}
        if len(segment) == 2 and segment[1] in EXCLUSIONS:
            exclusions.append(interval | {"reason": segment[1]})
        elif len(segment) in (4, 5):
            span = interval | dict(zip(("reading", "headword", "gloss"), segment[1:4]))
            if len(segment) == 5:
                span["word"] = segment[4]
            spans.append(span)
        else:
            raise ValueError(f"Invalid reviewed segment: {segment}")
    if text != prompt:
        raise ValueError("Reviewed segments must reproduce the entire original prompt exactly")
    return {"schemaVersion": 1, "promptSha256": prompt_hash(prompt), "spans": spans}, exclusions


def coverage_problems(root, inventory, require_complete=False):
    problems, entries = [], corpus(root)
    if inventory.get("schemaVersion") != 1 or inventory.get("stage") not in ("pilot", "complete"):
        return ["Invalid vocabulary inventory schema/stage"]
    seen = set()
    for record in inventory["records"]:
        key = (record["file"], record["exerciseId"])
        label = ":".join(key)
        if key in seen or key not in entries:
            problems.append(f"{label}: duplicate or obsolete coverage record")
            continue
        seen.add(key)
        exercise = entries[key]
        if (record.get("promptSha256") != prompt_hash(exercise["prompt"])
                or record.get("contextSha256") != context_hash(exercise)):
            problems.append(f"{label}: prompt/context changed; vocabulary review is stale")
        if record["status"] == "pending":
            if "vocabulary" in exercise or require_complete or inventory["stage"] == "complete":
                problems.append(f"{label}: vocabulary review is pending")
            continue
        if record["status"] != "reviewed" or not record.get("reviewer") or not record.get("notes"):
            problems.append(f"{label}: missing explicit review provenance")
            continue
        if record.get("vocabularySha256") != digest(exercise.get("vocabulary")):
            problems.append(f"{label}: annotations changed; vocabulary review is stale")
        invalid = vocabulary_problems(exercise, root)
        if invalid:
            problems.extend(f"{label}: {p}" for p in invalid)
            continue
        intervals = exercise.get("vocabulary", {}).get("spans", []) + record.get("exclusions", [])
        end = 0
        for interval in sorted(intervals, key=lambda i: i["start"]):
            if (interval["start"] != end or not end < interval["end"] <= len(exercise["prompt"])
                    or exercise["prompt"][end:interval["end"]] != interval["text"]):
                problems.append(f"{label}: incomplete or overlapping coverage")
                break
            if "reason" in interval and interval["reason"] not in EXCLUSIONS:
                problems.append(f"{label}: unknown exclusion reason")
            if "____" in interval["text"] and interval.get("reason") != "grammar-target":
                problems.append(f"{label}: the blank must be explicitly protected")
            end = interval["end"]
        if end != len(exercise["prompt"]):
            problems.append(f"{label}: coverage does not reach the end of the prompt")
    problems.extend(f"{name}:{identity}: no coverage record" for name, identity in entries.keys() - seen)
    return problems


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def apply_review(root, inventory, proposal):
    entries, files = corpus(root), {}
    records = {(r["file"], r["exerciseId"]): r for r in inventory["records"]}
    seen = set()
    for reviewed in proposal["exercises"]:
        key = (reviewed["file"], reviewed["exerciseId"])
        if key in seen or key not in entries:
            raise ValueError(f"Unknown/duplicate reviewed exercise: {key}")
        seen.add(key)
        exercise = entries[key]
        if reviewed["contextSha256"] != context_hash(exercise):
            raise ValueError(f"Context changed since review: {key}")
        hints, exclusions = annotations(exercise["prompt"], reviewed["segments"])
        problems = vocabulary_problems(exercise | {"vocabulary": hints}, root)
        if problems:
            raise ValueError(f"{key}: {'; '.join(problems)}")
        path = root / "grammar" / key[0]
        if path not in files:
            files[path] = json.loads(path.read_text(encoding="utf-8"))
        target = next(e for e in files[path]["exercises"] if e["id"] == key[1])
        target["vocabulary"] = hints
        records[key] = {
            "file": key[0], "exerciseId": key[1], "promptSha256": prompt_hash(exercise["prompt"]),
            "contextSha256": context_hash(exercise), "status": "reviewed",
            "vocabularySha256": digest(hints), "reviewer": proposal["reviewer"],
            "notes": reviewed["notes"], "exclusions": exclusions,
        }
    if not proposal.get("reviewer") or any(not e.get("notes") for e in proposal["exercises"]):
        raise ValueError("Explicit reviewer and per-exercise review notes are required")
    for path, data in files.items():
        write_json(path, data)
    inventory["records"] = [records[key] for key in sorted(records)]
    write_json(root / INVENTORY, inventory)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("init", "apply", "check"))
    parser.add_argument("--revision")
    parser.add_argument("--proposal", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    path = ROOT / INVENTORY
    if args.action == "init":
        if path.exists() or not args.revision:
            parser.error("init requires --revision and refuses to overwrite an inventory")
        write_json(path, initial_inventory(ROOT, args.revision))
    inventory = json.loads(path.read_text(encoding="utf-8"))
    if args.action == "apply":
        if args.proposal is None:
            parser.error("apply requires --proposal with explicitly reviewed segments")
        apply_review(ROOT, inventory, json.loads(args.proposal.read_text(encoding="utf-8")))
    problems = coverage_problems(ROOT, inventory, args.require_complete)
    for problem in problems:
        print(problem)
    reviewed = sum(r["status"] == "reviewed" for r in inventory["records"])
    print(f"Vocabulary coverage: {reviewed}/{len(inventory['records'])} reviewed prompts; stage={inventory['stage']}")
    raise SystemExit(bool(problems))


if __name__ == "__main__":
    main()
