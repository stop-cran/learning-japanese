# Batch 139 second revision: what changed from 3b6f9727 to f1b2bdb8

Revised snapshot: `f1b2bdb84f7e932dfe59cb68829fc004415d0a74`, a child of the earlier revision
`3b6f972767928e01261440466899f32df398d7f1`, which was reviewed in the earlier confirmation round. That revision is a
child of the initially reviewed snapshot `a47efe9af926316eaa86656033bf6e109f2be697`. Nothing is published.

- One of the 15 kanji cards changed, on one line: 嬢 (line 47). The other fourteen are unchanged. So are all 15 stroke
  files, the front matter of every card and every word article the batch edits.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot). No line was added or
  removed. The text at `3b6f9727` is in the earlier confirmation packet's `snapshot\kanji\`.
- `diffs\fix.patch` is the exact patch from `3b6f9727` to `f1b2bdb8`. `diffs\changed-lines.txt` lists the changed lines
  per file.

| Card | Changed line | Change |
| --- | --- | --- |
| 嬢 | 47 | The quoted JMdict glosses of 嬢さん じょうさん, `"(another's) daughter; young lady."`, now read `"(another's) daughter; young lady (esp. of respectable upbringing)."` Nothing else on the line changed. |

Why: the second sense of JMdict entry 2230740 (嬢さん じょうさん) is "young lady (esp. of respectable upbringing)". The
earlier revision quoted it without the parenthesis, so the quotation was not the full gloss. Support:
`evidence\jmdict-cited-entries.xml`, entry 2230740. The entry was already on the Metadata line (line 51), so that line is
unchanged.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `3b6f9727`. The outputs are identical apart from line 1 of each audit (the
command, which names the commit), the test run time and the content budget sizes: the uncompressed sizes grow by 33
bytes, the length of the added text, and the compressed size by 14 bytes.

- `lint.txt`: the batch linter on the 15 kanji cards and 20 word articles: 0 errors, 2 warnings, both on word articles
  whose Dictionary line cites no JMdict entry id (宣伝, 宴会). Same as at `3b6f9727`.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage
  pilot). `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt` and `kanji-remarks.txt`: the word-article link plan (20 changed word files, 20 added links, 4 declared
  remark edits, 0 problems) and the check that existing kanji cards are unchanged (0 modified, 0 problems).
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine), so there is no `jvm.txt`.
- `link-targets.tsv`: the links on the changed line to other cards and word articles. It lists none: the changed line
  has no link.
- `quiz-safety.txt`: the meaning-quiz audit, copied byte for byte. It is byte-identical to the earlier confirmation
  packet's `checks\quiz-safety.txt`; no front matter changed.
- `reading-exposure.txt` and `reading-options.txt`: identical to the earlier confirmation packet's copies apart from
  line 1. Summary lines: 0 production hits, 0 padded-session hits, 11 latent collisions, 0 one-holder padded hits; 1
  problem in `reading-options.txt`, the same 岬 さき HIT label (offered by 先), which cannot be drawn because 岬's three
  curated distractors fill every reading slot.
- `evidence\meta-scan.txt`: `meta_scan.py` on the 15 cards at `f1b2bdb8`. Apart from line 1 it is identical to the
  earlier confirmation packet's copy: the added parenthesis names no Japanese word.

## Corrections to the earlier `CHANGES.md`

- The 嬢 row said that entry 1531190 "moves before" the four new entries on the Metadata line, and the 峠 row said the
  same of entry 1896840. Neither moved: each stayed where it was, at the end of the old list, and the new entries were
  appended after it (`diffs\fix.patch` in the earlier confirmation packet).
- The 宴会 row said "this revision changes only the colon". That understated the edit: the colon became a full stop and
  the words "The on readings are" were added. The row's quoted old and new text were exact.

## Process notes

- `f1b2bdb8` is a single signed commit on top of `3b6f9727`; nothing was published in between.
- The checks in `checks\` were run on the committed revision.
