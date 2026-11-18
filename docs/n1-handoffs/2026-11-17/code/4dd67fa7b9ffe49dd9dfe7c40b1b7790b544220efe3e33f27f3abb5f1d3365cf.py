"""Pure scope checks for a guard-only B131 signed successor, not semantic acceptance."""
import difflib
import re

from common import require

CARDS = {f"kanji/{char}.md" for char in ("\u885b", "\u7f8a", "\u971c")}
PREFIX = "docs/n1-sources/batch-131-reconciliation/"
NOTES = "docs/n1-authoring-notes.md"


def check_paths(changes, expected_cards):
    require(bool(expected_cards) and expected_cards <= CARDS, "Invalid runtime correction scope")
    require(changes.get("manifest.json") == "M"
            and all(changes.get(path) == "M" for path in expected_cards),
            "Required runtime correction is missing")
    for path, status in changes.items():
        require((status == "M" and path in expected_cards | {"manifest.json", NOTES})
                or (status == "A" and (path.startswith(PREFIX)
                    or re.fullmatch(r"docs/n1-sources/batch-131-progress-reconciliation-\d{3}\.json", path))),
                f"Out-of-scope change: {status} {path}")


def check_metadata(old, new, allowed, required):
    require(required <= allowed and all(isinstance(char, str) and len(char) == 1 for char in allowed),
            "Invalid finite guard scope")
    require({key: value for key, value in old.items() if key != "quiz_exclusions"}
            == {key: value for key, value in new.items() if key != "quiz_exclusions"},
            "Non-exclusion metadata changed")
    before, after = old.get("quiz_exclusions", []), new.get("quiz_exclusions", [])
    require(isinstance(before, list) and isinstance(after, list)
            and all(isinstance(char, str) and len(char) == 1 for char in before + after)
            and len(before) == len(set(before)) and len(after) == len(set(after))
            and set(before) <= set(after)
            and [char for char in after if char in before] == before,
            "Original guards removed, duplicated or reordered")
    added = set(after) - set(before)
    require(required <= added <= allowed, "Added guards differ from the finite correction scope")
    require(new["kanji"] not in after and not set(after) & set(new["distractors"]),
            "Self-exclusion or excluded curated option")
    return [char for char in after if char not in before]


def check_runtime(before, after, expected_cards):
    require(bool(expected_cards) and expected_cards <= CARDS, "Invalid runtime correction scope")
    require(before.keys() == after.keys(), "Runtime membership changed")
    require({name for name in after if before[name] != after[name]} == expected_cards,
            "Unexpected runtime delta")
    require(all(before[name][1] == after[name][1] for name in before),
            "Runtime text/binary classification changed")


def check_notes(before, after):
    old, new = before.splitlines(keepends=True), after.splitlines(keepends=True)
    edits = [op for op in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes()
             if op[0] != "equal"]
    require(edits and all(op[0] == "insert" for op in edits), "Existing authoring notes changed")
    inserted = b"".join(line for _, _, _, start, end in edits for line in new[start:end])
    require(re.search(rb"(?m)^#{2,3} Batch 131(?: reconciliation \d{3})?:", inserted),
            "Unlabelled authoring-notes insertion")
