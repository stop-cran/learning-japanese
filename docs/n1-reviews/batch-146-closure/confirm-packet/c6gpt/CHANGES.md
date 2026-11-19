# Batch 146 sixth revision: what changed from d276f63b to 1c941a7a

Revised snapshot: `1c941a7a` (full hash `1c941a7a15e9eb53179d4fe37b596dc97c14b1f6`). It is one commit after `d276f63b4d2adf4985f8bf929bdad1103987556b`, the snapshot of your
earlier confirmation report. Nothing is published.

- One kanji card changed: 牧 (front-matter line 14 and line 54). Everything else is unchanged from `d276f63b`. No card gained or lost a line.
- Front matter: `quiz_exclusions` of 牧 is now `[畜, 養, 育, 農, 野, 僧, 治, 御, 官, 司, 導, 師]` (12 entries); `僧` is restored. The meaning choices from
  `distractors` (歌 山 雨) are unchanged. History: freeze `38833c7f` 17 entries; `5e61ef07`, `872d6502` 12 (with 牛 馬 羊 草 坊 僧);
  `09e376bd` 13; `8d16c582` 12 (`[畜, 養, 育, 農, 野, 僧, 治, 御, 官, 司, 導, 師]`); `d276f63b` 11 (without 僧).
- `diffs\fix.patch` is the exact patch from `d276f63b` to `1c941a7a`. `diffs\changed-lines.txt` lists the changed lines.
- `manifest.json` was regenerated; it is a generated index and outside the review.

| File | Changed lines | Change |
| --- | --- | --- |
| 牧 | 14 | `quiz_exclusions`: 僧 restored (12 entries). |
| 牧 | 54 | 僧 "Buddhist monk; priest" is back in the overlap list with the note that Daijisen's kanji entry gives 僧 the general sense "clergy" (聖職者), like the "clergyman" of 牧師; the count is "These seven, with 畜 養 育 農 野 above"; 坊 "Buddhist priest; boy" is stated not to be a meaning of 牧 and is not excluded. |

Why: the reviewers of the two model families disagreed on the pair 僧 and 坊. One held that neither is a meaning of 牧 and that they must be treated alike;
the other, after checking the Daijisen entries, held that 僧 (unlike 坊) has the general clergy sense in its kanji entry (聖職者) and that 僧 must stay excluded
while 坊 stays out. The author applied the second, dictionary-based criterion: an exclusion is kept where a dictionary sense of the other kanji overlaps a
taught sense of 牧 (the rule in `content-format.md`, displayed labels and ordinary meanings). Exclusions only remove wrong options; they cannot create a second correct answer.

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the same three Dictionary lines as before). `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors.
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean. `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt`: rerun at `1c941a7a`; 0 errors, 0 production or padded hits,
  10 latent collisions (unchanged), 0 reading-option problems.
- The Android JVM tests that read the real content were not run, as before.
