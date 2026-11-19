# Batch 144 second revision: what changed from 2be716f0 to 8db07f74

Second-round revised snapshot: `8db07f74` (full hash `8db07f740a2071609b29539cc1a29e4420bc43e5`). It is one commit
after `2be716f0661f17c03da9b4854665fb8e35f1af7a`, the snapshot of your earlier confirmation report. Nothing is published.

- Two kanji cards changed: 欄 (line 44) and 棚 (line 53). The other 13 cards, the existing card 討, all word articles and
  all stroke files are unchanged from `2be716f0`.
- No front matter changed in any card, so the meaning and reading options are unchanged. The quiz and reading audits
  were rerun at `8db07f74` with the same `--extra` input and are line-for-line identical to the rerun at `2be716f0`
  apart from the command line (the author's comparison, not a substitute for your own reading of the files).
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. No card changed its line count.
- `diffs\fix.patch` is the exact patch from `2be716f0` to `8db07f74` (this round's change only). `diffs\changed-lines.txt`
  lists the changed lines per file.
- New evidence in this packet: `evidence\README.md` describes each file. All other evidence stays in the earlier
  packets.

| File | Changed lines | Change |
| --- | --- | --- |
| 欄 | 44 | `It prints a parenthesized form after 欄, a compatibility form of the same kanji that this card does not teach separately.` is replaced by `It prints the older form of 欄 in parentheses; this card does not teach that form separately.` |
| 棚 | 53 | The Metadata line's JMdict entry list `…, 1579640 and 1499260.` now reads `…, 1579640, 1499260 and 1551120.` (1551120 is 陸棚, named in the ホウ row at `棚.md:33`). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the same three words without a JMdict entry id as before: 戸棚, 淡水, 特殊).
  `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: `manifest.json` regenerated, rebuild
  idempotent, tracked tree clean. `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `evidence\meta-scan.txt`: line 3 of its summary now reports 0 whole-run gaps (it reported 1, 陸棚 1551120 not listed,
  at `2be716f0`).
- `quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt`: unchanged in content (0 production, 0 padded,
  0 one-holder hits, 6 latent collisions, the one accepted labelled HIT for 殻 かい).
- The Android JVM tests that read the real content were not run, as before.

## Process notes

- `8db07f74` is the only commit in this round; `diffs\fix.patch` is the whole change from your reviewed snapshot.
