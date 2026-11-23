# Batch 138 second revision: what changed from acf7297e to 3158b2b9

Revised snapshot: `3158b2b97cc9ba61368b722d0c45c37536a909c5`, a child of the earlier revision
`acf7297ef66a82f620a6c5551d95a2e3fa356bc7`, which both reviewers confirmed in the earlier confirmation round. That
revision is a child of the initially reviewed snapshot `b6020f9e490298de1756e33c51bf9ce314132f4e`. Nothing is published.

- One of the 15 kanji cards changed, on one line: 契 (line 43). The other fourteen are unchanged. So are all 15 stroke
  files, the front matter of every card, the older card the batch edits (張) and every word article the batch edits.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot). No line was added or
  removed. The text at `acf7297e` is in the earlier confirmation packet's `snapshot\kanji\`.
- `diffs\fix.patch` is the exact patch from `acf7297e` to `3158b2b9`. `diffs\changed-lines.txt` lists the changed lines
  per file.

| Card | Changed line | Change |
| --- | --- | --- |
| 契 | 43 | The reading of 契闊 is now written in hiragana: "as in 契闊 ケッカツ, not seeing someone for a long time" becomes "as in 契闊 けっかつ, not seeing someone for a long time". Nothing else on the line changed. |

Why: every other word reading on the card is in hiragana (けいやく, ちぎる, きったん), and this was the only reading of a
Sino-Japanese word in katakana among the 15 cards. The batch's other katakana word readings are loanwords and foreign
names. Kanjipedia prints the word as 契闊(ケッカツ) (the earlier confirmation packet's `evidence\kanjipedia-契.txt`).
契闊 has no JMdict entry, so the Metadata line is unchanged.

## Corrected reading audits

The reading audits in the original packet and in the earlier confirmation packets left out some extra readings for
five kanji (垂, 執, 壊, 奏, 奪), because of a defect in the author's audit tools. `evidence\extras-merge-fix.txt`
describes the defect, the fix, the readings that were left out and what the corrected audits show. In short:

- Of the 12 readings left out, eight were not checked at all: 垂 なんなんとする, しずる, しずれ; 執 とらえる; 壊 やぶれる,
  こわる; 奏 すすめる, もうす.
- With them, `checks\reading-exposure.txt` finds one more latent collision, 壊 やぶれる (offered by 敗 and 破; lines
  152-154). It cannot be drawn in any pool the app builds from the shipped stacks, nor with any single borrowed holder
  card. The summary is now 0 production hits, 0 padded-session hits, 9 latent collisions (line 261; was 8), and 0
  one-holder padded hits (line 262).
- `checks\reading-options.txt` still reports 2 problems, the same two HIT labels (噴 ほん, line 17; 契 けつ, line
  160). 壊 gains a note (line 132): やぶれる is offered only by 敗 and 破 and cannot be drawn from the full pool.
- The same corrected command at the reviewed snapshot `b6020f9e` gives the same outputs apart from line 1
  (`evidence\reading-exposure-b6020f9e.txt`, `evidence\reading-options-b6020f9e.txt`): no revision changed a reading or
  a `distractors` list, and the two tools do not read `quiz_exclusions`.

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on 16 kanji cards (the 15 new cards and 張) and 24 word articles: 0 errors, 3 warnings,
  all on word articles whose Dictionary line cites no JMdict entry id (噴火, 墨, 威張る). Same as at `acf7297e`.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage
  pilot). `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine), so there is no `jvm.txt`.
- `link-targets.tsv`: the links on the changed line to other cards and word articles. It lists none: the line's only
  link is to Kanjipedia, an external page the table does not cover, and that link did not change.
- `quiz-safety.txt`: the meaning-quiz audit, copied byte for byte this time. It is byte-identical to the original
  packet's `evidence\audits\quiz-safety.txt` (same SHA-256); no front matter changed.
- `reading-exposure.txt` and `reading-options.txt`: the corrected audits described above.
- `evidence\meta-scan.txt`: `meta_scan.py` on the 15 cards at `3158b2b9`; line 4 says no word the script checks lacks
  its JMdict entry in the Metadata line. Its output is the same as at `acf7297e` apart from line 1.

## Corrections to the earlier `CHANGES.md`

- It said that `quiz-safety.txt` "matches the original packet's `evidence\audits\quiz-safety.txt` line for line". The
  text was the same, but that packet's copy lacked the blank line before the summary (line 44 of the original): the
  packet builder dropped every blank line from the check outputs it summarizes, and that file had one. So "line for
  line" was not exact. In this packet, `quiz-safety.txt` is copied unchanged.
- It said that `reading-exposure.txt` reports 8 latent collisions. That count came from the defective run; the
  corrected count is 9 (above).

## Process notes

- `3158b2b9` is the second local version of this fix commit. The first, `a93ce9c0`, made the same change to the card
  and was replaced only to correct its commit message, which overstated the change; it was not reviewed or published.
