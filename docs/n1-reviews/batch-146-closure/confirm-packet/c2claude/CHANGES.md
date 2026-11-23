# Batch 146 second revision: what changed from 5e61ef07 to 872d6502

Second-round revised snapshot: `872d6502` (full hash `872d6502c5fd1be09df200017fca607456a20321`). It is one commit
after `5e61ef074618251796ad971f99736e5663f36df6`, the snapshot of your earlier confirmation report. Nothing is published.

- Three kanji cards changed: 甚 (lines 34, 35, 41), 牧 (line 54) and 盛 (line 37). The other 12 new cards, the existing card
  潔, all word articles and all stroke files are unchanged from `5e61ef07`.
- No front matter changed, so the meaning and reading options are unchanged. The quiz and reading audits were rerun at
  `872d6502` with the same `--extra` input and are unchanged in content (0 production hits, 0 padded hits, 0 one-holder hits,
  10 latent collisions, 0 reading-option problems).
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. No card gained or lost a line.
- `diffs\fix.patch` is the exact patch from `5e61ef07` to `872d6502` (this round's change only). `diffs\changed-lines.txt` lists the
  changed lines per file.
- New evidence in this packet: `evidence\README.md` describes each file. All other evidence stays in the earlier packets.

| File | Changed lines | Change |
| --- | --- | --- |
| 甚 | 34 | The はなは.だ row now ends `extreme; excessive; the word is spelled with the longer ending だしい and shares the stem はなは with this reading`. |
| 甚 | 35 | The はなは.だしい row now says it `shares the stem はなは with はなは.だ, so it is not selected separately` (was `not selected separately`). |
| 甚 | 41 | `Practice selects はなは.だ, the reading in the linked word article 甚だしい.` is replaced by `Practice selects はなは.だ; the linked word article 甚だしい has the same stem はなは.` |
| 牧 | 54 | `All twelve kanji named in the last two bullets are kept out…` is replaced by `These three and the nine kanji in the previous bullet are kept out…` |
| 盛 | 37 | The 盛ん row gloss `thriving; active; "prosperous; flourishing; thriving; successful"` is now `active; JMdict "prosperous; flourishing; thriving; successful"`. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the same three Dictionary lines as before). `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors.
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean. `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt`: unchanged in content.
- The Android JVM tests that read the real content were not run, as before.

## Process notes

- `872d6502` is the only commit in this round; `diffs\fix.patch` is the change from your reviewed snapshot.
