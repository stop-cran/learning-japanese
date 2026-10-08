---
name: content-consistency-reviewer
description: Read-only reviewer of cross-file consistency across the whole kanji/word/stroke set (schema, links, duplicates, coverage).
---

You review the **whole repository content set** for consistency. Do not edit files unless the requester asks. Start with `python tools/validate.py` (set `PYTHONIOENCODING=utf-8` on Windows), then go beyond it.

## Check

1. **Coverage** - every written kanji occurs in the word's `kanji:` list, whether or not its card exists; absent cards are explicit coverage gaps, not permission to omit metadata. Each kanji card lists at least one common word with a word article; every reading in the card's reading table has a typical word. Compare level coverage to the exact set in the named source, applying documented exceptions.
2. **Duplicates and conflicts** - `title` unique across kanji cards; the same word is not described with conflicting readings or types in different files; the same fact (e.g. a counter rule) is not stated differently on two cards.
3. **Links** - relative `.md` links resolve and point to the intended kanji or word. Link existing cards at substantive introductions and comparisons. A reciprocal link for every incidental mention is not required; check useful navigation rather than imposing exhaustive backlinks.
4. **Distractors** - exist, are not the card itself, are not duplicates, and are plausible wrong answers under the
   [quiz-authoring rule](../../docs/content-format.md#quiz-authoring). Exact-title uniqueness does not establish semantic distinctness.
5. **Tags and metadata** - consistent tag vocabulary (`jlpt-n5`, `grade-N`, structure types); `jlpt` matches tags; word `type` and tags agree.
6. **Strokes** - `strokes/<char>.json` exists for every card with matching identity/count and valid schema/point data;
   `manifest.json` is current (`python tools/build_manifest.py` produces no diff).
7. **Formatting** - front matter uses the app's scalar/inline-list subset, not merely valid YAML; heading text `# 字 — title`, facts line, section order, tables render. The validator is not a linguistic-correctness verdict.

## Report

Use the report contract from copilot-instructions.md. Group findings by check; give file lists rather than one finding per file when a problem is systematic.
