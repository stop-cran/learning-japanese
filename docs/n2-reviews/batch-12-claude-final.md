## Snapshot
Checkpoint `db1138dcae050e32c4eb859d64957c3352932af0`, committed files only. The previous confirmed correction was `55afc4add77d21ec8c8aae013bac072d39e9e881`. I had no Git or execution tool, so the commit identity, the four-file scope, the clean worktree, validation, the 180/550 counts and manifest `ad69e220cc204eb9` rest on the author's checks.

## Scope
- **Model:** claude-opus-5.5 (claude family). I worked alone and read only; no edits, no delegation.
- **Diff:** `n2-batch-12-consistency.diff`, read completely. It has one hunk in `words\汗.md` (lines 29–34), changing exactly two lines: 32 and 34.
- **Article:** `words\汗.md`, read completely (34 lines).
- **Kanji card:** `kanji\汗.md`, the Notes and Metadata (lines 38–44).
- **Source record:** the complete entry 2463120 in `docs\n2-batch-sources\batch-12.json` (lines 1150–1193).
- **Earlier report:** my own `docs\n2-reviews\batch-12-claude-followup.md`.
- **Not read:** the other family's report and the author ledgers.

## Verdicts
| Page (changed scope) | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| words\汗.md, lines 32 and 34 | CLEAN | CLEAN | CLEAN |

## Findings
None remain.

- **Accuracy:** Line 32 says JMdict lists 汗する (あせする), "perspire; sweat". Entry 2463120 has exactly that: spelling 汗する, reading あせする, glosses "to perspire; to sweat", a suru verb, intransitive. It has no flags, priorities or restrictions.
  - Line 34's citation "related verb 2463120" is exact.
  - The line makes no frequency or register comparison, which the record could not support.
- **Consistency:** The line now matches the kanji card's Notes (line 40), which attests 汗する and points to the article for 汗をかく. The two pages no longer pull in opposite directions.
  - The Meaning section still teaches 汗をかく as the whole expression.
  - The front matter, examples and other teaching text are unchanged.
- **Ambiguity:** No new consequential ambiguity. One small imprecision: "the examples above use 汗をかく" is true only of the first example, since the second uses 汗を拭く. In context it clearly refers to the act of sweating, so it is not actionable.
- **My earlier Optional #2 (`words\汗.md:32`):** Resolved and recalibrated.
  - The old warning has been replaced as intended.
  - My suggested wording, "Use 汗をかく for everyday 'I sweat'", implied a usage ranking the pinned record does not support. The neutral wording adopted is better calibrated.

## Optional
None.

## Limits
- **Narrow review:** this covers only the changed passage, its linked kanji-card Notes and entry 2463120. I did not re-review the whole batch.
- **Earlier verdicts:** the seven-page verdicts at `55afc4a` stand, and the other 11 pages keep their initial verdicts.
- **Dictionary evidence:** batch-12 is a selected extraction. These verdicts are not native-speaker certification.
