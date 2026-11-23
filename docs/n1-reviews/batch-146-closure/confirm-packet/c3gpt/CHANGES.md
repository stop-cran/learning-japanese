# Batch 146 third revision: what changed from 872d6502 to 09e376bd

Third-round revised snapshot: `09e376bd` (full hash `09e376bd5763106a4602f6e1d9b95f97d9fdb036`). It is one commit after `872d6502c5fd1be09df200017fca607456a20321`,
the snapshot of the previous confirmation reports. Nothing is published.

- One kanji card changed: 牧 (front-matter line 14 and lines 53 and 54). The other 14 new cards, the existing card 潔, all word
  articles and all stroke files are unchanged from `872d6502`. No card gained or lost a line.
- Front matter: `quiz_exclusions` of 牧 was `[畜, 養, 育, 農, 牛, 馬, 羊, 草, 野, 僧, 坊, 師]` (12) at `872d6502` and is now
  `[畜, 養, 育, 農, 野, 僧, 坊, 治, 御, 官, 司, 導, 師]` (13). The meaning choices that come from `distractors` (歌 山 雨) are
  unchanged. For the history: the freeze `38833c7f` had 17 entries, `[畜, 養, 育, 農, 牛, 馬, 羊, 草, 野, 僧, 坊, 治, 御, 官, 司, 導, 師]`.
  The current list is that list without 牛 馬 羊 草.
- `diffs\fix.patch` is the exact patch from `872d6502` to `09e376bd` (this round's change only). `diffs\changed-lines.txt` lists the
  changed lines.
- `manifest.json` was regenerated; it is a generated index and outside the review.

| File | Changed lines | Change |
| --- | --- | --- |
| 牧 | 14 | `quiz_exclusions`: 牛 馬 羊 草 removed; 治 御 官 司 導 restored (see above). |
| 牧 | 53 | The bullet now names 畜 養 育 農 野 as the words for the first sense, and says that 牛 馬 羊 草 belong to the scene but are animals and plants, not meanings of 牧, so they are not excluded. |
| 牧 | 54 | The bullet now says that the title's "pastor" and the other senses taught on the card overlap with 僧 坊 師 and 治 御 官 司 導 (with their displayed titles), and that these eight, with the five kanji of the previous bullet, are kept out of the quiz options. |

The rule behind the change is the one in `content-format.md` (quiz authoring): an exclusion is authored only from the displayed labels
and the target's ordinary meanings. The card's own Meaning section teaches three Daijisen senses (graze livestock; govern, with 牧師 as
the example; governing official), so labels that give those senses are excluded; labels of animals and plants in the pasture scene are not.

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the same three Dictionary lines as before). `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors.
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean. `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt`: rerun at `09e376bd`; 0 errors, 0 production or padded hits,
  10 latent collisions (unchanged), 0 reading-option problems.
- The Android JVM tests that read the real content were not run, as before.
