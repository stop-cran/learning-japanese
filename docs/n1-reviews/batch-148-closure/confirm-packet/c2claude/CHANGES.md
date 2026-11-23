# Batch 148 second revision: what changed from cc286cc3 to 4162ea2c

Second-round revised snapshot: `4162ea2c` (full hash `4162ea2cb44a59bdf9829dbbcddd7a6ff00532b9`). It is one commit after
`cc286cc34ca20370000e6c042a2dbb045cac3d99`, the snapshot of your earlier confirmation report. Nothing is published.

- Two kanji cards changed, one line each: 締 (line 52) and 緊 (line 56). The other 13 new cards, the three modified existing
  cards, all word articles and all stroke files are unchanged from `cc286cc3`. No front matter changed.
- `diffs\fix.patch` is the exact patch from `cc286cc3` to `4162ea2c`. `manifest.json` was regenerated (a generated index,
  outside the review).

| File | Changed lines | Change |
| --- | --- | --- |
| 締 | 52 | `[縛](縛.md) overlaps "bind";` is now `[縛](縛.md), "bind; tie up; restrain," overlaps binding;`. |
| 緊 | 56 | `and [筋](筋.md), so none` is now `and [筋](筋.md), "muscle; sinew; line; plot," so none`. |

## Checks run on the revised snapshot (outputs in `checks\`)

- The checks were rerun at `4162ea2c` with the same results as at `cc286cc3`: lint 0 errors and the same 3 warnings; 439 unit
  tests OK; validate 0 errors; linkplan and kanji-remarks 0 problems; quiz-safety 0 errors and 0 warnings; reading-exposure 0
  production hits, 0 padded-session hits and 9 latent collisions; reading-options 0 problems.
- The Android JVM tests that read the real content were not run, as before.
