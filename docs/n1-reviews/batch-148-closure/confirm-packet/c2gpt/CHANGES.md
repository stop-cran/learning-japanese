# Batch 148 further revision: what changed from 4162ea2c to 04900b9c

Latest revised snapshot: `04900b9c` (full hash `04900b9ce968180c6ab8a7f271b5c3c80d30e6e8`). It is one commit after
`4162ea2cb44a59bdf9829dbbcddd7a6ff00532b9`, the snapshot of your earlier confirmation report. Nothing is published.

- Two kanji cards changed: 緊 (lines 14 and 54) and 締 (line 40). The other 13 new cards, the three modified existing cards,
  all word articles and all stroke files are unchanged from `4162ea2c`.
- Front matter: the `quiz_exclusions` of 緊 changed from `[張, 急, 密, 詰, 勁, 硬, 固, 堅, 縮, 圧, 要, 縛]` to
  `[張, 急, 密, 詰, 勁, 硬, 固, 堅, 縮, 圧, 要]`. No title, tag, metadata reading or `distractors` list changed.
- `diffs\fix.patch` is the exact patch from `4162ea2c` to `04900b9c`. `manifest.json` was regenerated (a generated index,
  outside the review).

| File | Changed lines | Change |
| --- | --- | --- |
| 緊 | 14, 54 | Line 14: 縛 removed from `quiz_exclusions`. Line 54: 縛 and its title are removed from the overlap list, which now ends `and [要](要.md), "necessity; essentials," overlap the senses of tension, tightness, urgency and pressure that 緊 and its words carry` (the word "binding" is dropped from the list of senses). |
| 締 | 40 | `whose reading is し.める with め as okurigana` is now `whose reading is し.める with める as okurigana`. |

## Checks run on the revised snapshot (outputs in `checks\`)

- The checks were rerun at `04900b9c` with the same results as at `4162ea2c`: lint 0 errors and the same 3 warnings; 439 unit
  tests OK; validate 0 errors; linkplan and kanji-remarks 0 problems; quiz-safety 0 errors and 0 warnings; reading-exposure 0
  production hits, 0 padded-session hits and 9 latent collisions; reading-options 0 problems.
- The Android JVM tests that read the real content were not run, as before.
