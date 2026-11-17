# Batch 134 integration with current main

B134 (紫, frozen source row 831) closed its two-family textual review on
snapshot `cc374051` and closure `ae155573`. A first integration merge `b140716f`
was made before the cross-PC handoff `2eb0e9c9`. Main then gained 29 commits of N3
grammar articles and 気 see-also links (`830f740b..9d7b5121`). This record
covers the second merge `bf9aa740` (parents `2eb0e9c9` and `9d7b5121`).

## Merge

- `manifest.json` was the only textual conflict. It was regenerated with
  `tools/build_manifest.py`; CI's rebuild-and-diff check is clean.
- [`merge-proof.json`](merge-proof.json) is produced by
  [`merge_proof.py`](merge_proof.py):
  `python -X utf8 merge_proof.py <repo> bf9aa740 merge-proof.json`.
  - All 45,076 compared non-derived paths equal one parent byte-for-byte.
  - `kanji/紫.md`, `strokes/紫.json` and `words/紫.md` equal `cc374051` and `ae155573`.
  - No path linked from the 紫 cards was changed by main.
  - No main-changed file mentions 紫.
- Gates on `bf9aa740`: `validate.py` passed with 0 errors. The 431 unit tests passed.
  `check_content_budget.py` passed with 8,808 entries, 50,373,821 retained bytes and
  31,719,104 local ZIP bytes. `grammar_vocabulary.py check` passed, and the manifest
  rebuild shows no diff.

## Integration-impact confirmations

The issue #60 contract requires integration review only for changed teaching
or an overlapping substantive conflict. The B134 reviewer sessions could not be
resumed on the new PC. Two **fresh replacement** reviewers, one from each model
family, independently checked the frozen merge `bf9aa740`. They are labelled as
replacements and do not reuse any original session. They ran one after the other,
each with a read-only mandate ([instructions](packet/INSTRUCTIONS.md),
[prompts](prompts/)). Neither read the other's report.

| Reviewer | Model | Report | Verdict |
| --- | --- | --- | --- |
| N1-B134-INTEG-CLAUDE-REPLACEMENT-001 | claude-opus-5.5 | [report](reports/claude-integration.md) | CLEAN, 0 findings |
| N1-B134-INTEG-GPT-REPLACEMENT-001 | gpt-6.1-sol | [report](reports/gpt-integration.md) | CLEAN, 0 findings |

Both reviewers independently re-derived the M2 manifest from git blobs and found it
byte-identical. Both found no change on main affecting the following, and no new
content using 紫:
- 紫's links, distractors (古・右・川) or 58 quiz exclusions;
- meaning pools;
- reading practice.

## Limits

- These confirmations are bounded integration checks, not a re-review of
  the closed 紫 card. Every B134 closure limit still applies. See
  [`batch-134-progress.json`](../../n1-sources/batch-134-progress.json).
- Android JVM tests (RealContentTest, RareHanTest, KanjiReadingsTest) were
  NOT RUN because no JDK is available on this machine. No native, device, phone,
  rendered-font or whole-set acceptance is claimed.
- The packet evidence copies (the 紫 card, main's change stat and runtime diff,
  and the B134 closure resolution) were taken from the commits named above. Only
  the instructions, prompts and reports are retained here.
