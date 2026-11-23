# Batch 145 second revision: what changed from e07ab312 to 97168e79

Second-round revised snapshot: `97168e79` (full hash `97168e795cfc47698d2445ec1886be503494b415`). It is one commit
after `e07ab3127d6ea3d9daa507b519fc993bd968f08c`, the snapshot of your earlier confirmation report. Nothing is published.

- One kanji card changed: 為 (lines 25 and 42). The other 14 new cards, the existing cards 暑 and 渋, all word articles and
  all stroke files are unchanged from `e07ab312`.
- No front matter changed, so the meaning and reading options are unchanged. The quiz and reading audits were rerun at
  `97168e79` with the same `--extra` input and are line-for-line identical to the rerun at `e07ab312` apart from the command line
  (the author's comparison, not a substitute for your own reading of the files).
- `manifest.json` and `docs\n1-sources\batch-145-progress.json` were regenerated; both are generated records and outside the review.
- Line numbers below refer to the revised snapshot in this packet. No card gained or lost a line.
- `diffs\fix.patch` is the exact patch from `e07ab312` to `97168e79` (this round's change only). `diffs\changed-lines.txt` lists the
  changed lines per file.
- New evidence in this packet: `evidence\README.md` describes each file. All other evidence stays in the earlier packets.

| File | Changed lines | Change |
| --- | --- | --- |
| 為 | 25 | `…, an aim, and acting for someone.` is replaced by `…, an aim, and a relation to someone, as in Daijisen's example 私のためには叔父にあたる, meaning he is an uncle to me.` (Daijisen ため, sense 4: 一定の関係のあること。…にとっては。) |
| 為 | 42 | `な.る and な.す share the stem な, so this card claims only…` is replaced by `な.る and な.す share the stem な; 為す uses な.す, so this card claims only…` |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 5 warnings (the same five Dictionary lines as before). `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors.
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean. `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `evidence\meta-scan.txt`: it now also lists 叔父 (JMdict 1607070/2648960) as "not listed part of" the Daijisen example 私のためには叔父にあたる
  quoted on line 25; the example is quoted as Daijisen's own, so the author did not add those ids to the Metadata line.
  The other lines are as before.
- `quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt`: unchanged in content (0 production, 0 padded,
  0 one-holder hits, 10 latent collisions, the labelled `reading-options` HITs).
- The Android JVM tests that read the real content were not run, as before.

## Process notes

- `97168e79` is the only commit in this round; `diffs\fix.patch` is the change from your reviewed snapshot.
