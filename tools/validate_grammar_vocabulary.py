"""Strict authoring checks for optional, occurrence-addressed Grammar vocabulary."""

import hashlib
import unicodedata


def prompt_hash(prompt):
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def vocabulary_problems(exercise, root):
    if "vocabulary" not in exercise:
        return []
    prompt, data = exercise.get("prompt"), exercise["vocabulary"]
    if not isinstance(prompt, str):
        return ["vocabulary needs a valid prompt"]
    if not isinstance(data, dict) or set(data) != {"schemaVersion", "promptSha256", "spans"}:
        return ["vocabulary needs exactly schemaVersion, promptSha256 and spans"]
    problems = []
    if type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1:
        problems.append("unsupported vocabulary schema")
    if data["promptSha256"] != prompt_hash(prompt):
        problems.append("vocabulary belongs to a different prompt revision")
    spans = data["spans"]
    if not isinstance(spans, list) or len(spans) > 128:
        return problems + ["spans must be an array of at most 128 entries"]
    required = {"start", "end", "text", "reading", "headword", "gloss"}
    previous_end = 0
    blank = prompt.find("____")
    for span in spans:
        if not isinstance(span, dict) or set(span) - {"word"} != required:
            problems.append("invalid vocabulary span fields")
            continue
        start, end = span["start"], span["end"]
        if type(start) is not int or type(end) is not int or not previous_end <= start < end <= len(prompt):
            problems.append("invalid, overlapping or unsorted vocabulary span")
            continue
        previous_end = end
        if prompt[start:end] != span["text"]:
            problems.append("span text does not match its occurrence")
        if not (end <= blank or start >= blank + 4):
            problems.append("span overlaps the grammar blank")
        if any(at < len(prompt) and unicodedata.category(prompt[at]).startswith("M") for at in (start, end)):
            problems.append("span splits a combining sequence")
        for field, limit in (("text", 80), ("reading", 80), ("headword", 80), ("gloss", 240)):
            value = span[field]
            if not isinstance(value, str) or not value.strip() or len(value) > limit:
                problems.append(f"{field} must contain 1-{limit} characters")
        if "word" in span:
            word = span["word"]
            if (not isinstance(word, str) or not word.strip() or len(word) > 80
                    or word in (".", "..") or any(c in "/\\" or unicodedata.category(c) == "Cc" for c in word)):
                problems.append("invalid word reference")
            elif not (root / "words" / f"{word}.md").is_file():
                problems.append(f"word reference does not exist: {word}")
    return problems
