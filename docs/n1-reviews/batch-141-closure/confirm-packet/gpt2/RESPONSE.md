# Author's statement for the reviewer of `reports-141\confirm-gpt.md`

This statement answers only the points in YOUR confirmation report. Your report had one Finding, G2, and one Optional
point, which had no label; here it is P1. The statement is the author's claim about what changed and why. Verify each
claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this
text as evidence. Card line numbers refer to the revised cards in this packet. Two of the 15 cards changed (抽 and 懸),
on three lines, and the other thirteen did not (see `CHANGES.md`). Give a disposition for G2 and P1.

## Findings

### G2: 抽斗 is explained by a false per-character split (`抽.md:34-36`)

Author action: **changed** (your remedy: 抽斗 kept as a whole-word spelling, ひき- illustrated by a transparent
spelling with its search-only qualification; the sourced metadata reading is kept).

- The sentence `In 抽斗, 抽 writes ひき and 斗 writes だし; Daijisen lists 抽斗 ひきだし as a hard-to-read word.` is
  removed from line 36.
- The ひき- row (line 34) now uses 抽出し ひきだし, "drawer", as its example, where 抽 writes ひき on its own. The cell
  says that JMdict heads the entry 引き出し, lists 抽出し as a search-only kanji form and marks 抽き出し and 抽斗 as
  rarely used kanji forms, and that this index form is not a recommended word example. That is the wording other cards
  use for a source-only reading whose only JMdict example is a search-only form (for example 双, 圧 and 訓, outside this
  packet).
- Line 36 explains 抽出し (抽 ひき, 出 だ, okurigana し), contrasts it with 抽出 ちゅうしゅつ, and keeps the unchanged
  抽き出し sentence. Its new last sentence keeps 抽斗 only as a whole-word reading: `Daijisen lists the rarely used
  spelling 抽斗 ひきだし as a hard-to-read word; this is a reading of the whole word, not a kanji-by-kanji reading, and
  KANJIDIC2 gives 斗 no reading だし.`
- The ひき- reading stays in the card's metadata and reading table.
- Support: `evidence\jmdict-cited-entries.xml`, entry 1601650; `evidence\kanjidic2-斗.xml`, 斗's complete record in the
  pinned KANJIDIC2 input (ja_on ト and トウ, no ja_kun reading, nanori ます); the original packet's
  `evidence\public-source\weblio-抽.txt`, line 6, where Daijisen lists 抽斗 under 難読.

To verify: that no sentence on lines 34-36 gives 斗 a reading or splits 抽斗 by kanji, that the 抽出し analysis and the
JMdict labels match entry 1601650, and that the 斗 claim matches the added KANJIDIC2 record.

## Optional points

### P1: qualify けんねん as irregular kana (`懸.md:46`)

Author action: **changed.**

- The last clause of line 46 now reads `JMdict lists けねん first and also けんねん, which it marks as irregular kana
  usage; in けんねん, 懸 supplies ケン.` It read `JMdict lists けねん first and also the reading けんねん, where 懸
  supplies ケン.` Nothing else on the line changed (`diffs\changed-lines.txt`).
- Support: `evidence\jmdict-cited-entries.xml`, entry 1257720 (`<re_inf>word containing irregular kana usage</re_inf>`
  on けんねん).

To verify: that the clause now reports the tag and that nothing else on the line changed.

## Other points in your report

No disposition is needed for these.

- **G1, Optional 1, Optional 2 and Optional 3.** Your report resolved G1, Optional 1 and Optional 3 and accepted the
  decline of Optional 2. This revision changes no text those points concern.
- **Quiz audits.** No front matter changed. `checks\quiz-safety.txt` is byte-identical to the earlier confirmation
  packet's copy, and `checks\reading-exposure.txt` and `checks\reading-options.txt` are identical to it apart from line 1.
- **Android JVM tests and the Kotlin cross-check.** Not run for this revision either.

## Process notes

- The checks in `checks\` were run on the committed revision.
