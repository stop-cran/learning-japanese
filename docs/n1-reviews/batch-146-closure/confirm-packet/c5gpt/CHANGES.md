# Batch 146 fifth revision: what changed from 09e376bd to d276f63b

Revised snapshot: `d276f63b` (full hash `d276f63b4d2adf4985f8bf929bdad1103987556b`). It is two commits after `09e376bd5763106a4602f6e1d9b95f97d9fdb036`, the snapshot of your
earlier confirmation report: `8d16c582` and `d276f63b`. Nothing is published.

- One kanji card changed: 牧 (front-matter line 14 and lines 26, 53 and 54). Everything else is unchanged from `09e376bd`. No card gained or lost a line.
- Front matter:
  `quiz_exclusions` of 牧 is now `[畜, 養, 育, 農, 野, 治, 御, 官, 司, 導, 師]` (11 entries). The meaning choices from `distractors`
  (歌 山 雨) are unchanged. For the history: the freeze `38833c7f` had 17 entries, `[畜, 養, 育, 農, 牛, 馬, 羊, 草, 野, 僧, 坊, 治, 御, 官, 司, 導, 師]`;
  `5e61ef07` and `872d6502` had 12, `[畜, 養, 育, 農, 牛, 馬, 羊, 草, 野, 僧, 坊, 師]`; `09e376bd` had 13 and `8d16c582` had 12,
  `[畜, 養, 育, 農, 野, 僧, 治, 御, 官, 司, 導, 師]`.
- `diffs\fix.patch` is the exact combined patch from `09e376bd` to `d276f63b`. `diffs\changed-lines.txt` lists the changed lines.
- `manifest.json` was regenerated; it is a generated index and outside the review.

| File | Changed lines | Change |
| --- | --- | --- |
| 牧 | 14 | `quiz_exclusions`: 11 entries; 牛 馬 羊 草 坊 僧 are not in it. |
| 牧 | 26 | The label of the second sense is now "Govern and guide people". |
| 牧 | 53 | The bullet is headed "Kanji related to the first sense" and names 畜 養 育 農 野; it says 牛 馬 羊 草 are animals and plants of the scene, not meanings of 牧, so they are not excluded. |
| 牧 | 54 | The bullet says the title's "pastor" and the other senses overlap with 師 治 御 官 司 導 (with displayed titles); these six, with 畜 養 育 農 野, are kept out of the quiz options; 僧 and 坊 are Buddhist clergy, not meanings of 牧, and are not excluded. |

The rule behind the list is the one in `content-format.md` (quiz authoring): an exclusion is authored only from the displayed labels
and the target's ordinary meanings. The card's own Meaning section teaches three Daijisen senses (graze livestock; govern, with 牧師 as
the example; governing official), so labels that give those senses are excluded. Labels of animals and plants in the pasture scene
(牛 馬 羊 草) and of Buddhist clergy (僧 "Buddhist monk; priest", 坊 "Buddhist priest; boy") are not meanings of 牧 and are not excluded.
The two earlier reviewers disagreed only about this last pair (one said remove 坊; the other said 僧 and 坊 must be treated alike);
the author applied the common principle to both.

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the same three Dictionary lines as before). `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors.
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean. `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt`: rerun at `d276f63b`; 0 errors, 0 production or padded hits,
  10 latent collisions (unchanged), 0 reading-option problems.
- The Android JVM tests that read the real content were not run, as before.
