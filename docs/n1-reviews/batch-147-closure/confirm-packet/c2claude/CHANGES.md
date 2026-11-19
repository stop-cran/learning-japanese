# Batch 147 second revision: what changed from 99487bb5 to 886671da

Second-round revised snapshot: `886671da` (full hash `886671da825c2da9ccbbf34506cf0b7747d7804c`). It is one commit after `99487bb5bef47b4e43be5b3223db7cb4dbb3bec1`, the snapshot of your
earlier confirmation report. Nothing is published.

- Two kanji cards changed, one line each: 穏 (line 25) and 稚 (line 40). The other 13 new cards, the three modified existing
  cards, all word articles and all stroke files are unchanged from `99487bb5`. No front matter changed.
- `diffs\fix.patch` is the exact patch from `99487bb5` to `886671da`. `manifest.json` was regenerated (a generated index, outside
  the review).

| File | Changed lines | Change |
| --- | --- | --- |
| 穏 | 25 | `Its examples are 穏健 おんけん, 穏和 おんわ, 安穏, 不穏 ふおん and 平穏 へいおん.` is now `Its examples include 穏健 おんけん, 穏和 おんわ, 安穏, 静穏, 不穏 ふおん and 平穏 へいおん.` |
| 稚 | 40 | `in the other JMdict spelling 稚けない` is now `in the JMdict spelling 稚けない`. |

## Checks run on the revised snapshot (outputs in `checks\`)

- The checks were rerun at `886671da` with the same results as at `99487bb5`: lint 0 errors and the same 2 warnings; 439 unit
  tests OK; validate 0 errors; linkplan and kanji-remarks 0 problems; quiz-safety 0 errors and 0 warnings; reading-exposure 0
  production hits, 0 padded-session hits and 7 latent collisions; reading-options the same one known problem (やすらか of 穏
  flagged as offered by 安 by the older check).
- The Android JVM tests that read the real content were not run, as before.
