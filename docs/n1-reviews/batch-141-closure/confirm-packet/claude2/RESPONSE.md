# Author's statement for the reviewer of `reports-141\confirm-claude.md`

This statement answers only the points in YOUR confirmation report. Your report had two Findings, F1 and F2, which are
also the open parts of C2 and O5. The statement is the author's claim about what changed and why. Verify each claim
against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text
as evidence. Card line numbers refer to the revised cards in this packet. Two of the 15 cards changed (抽 and 懸), on
three lines, and the other thirteen did not (see `CHANGES.md`). Give a disposition for F1 and F2.

## Findings

### F1: 抽斗 is split as if 斗 had the reading だし (`抽.md:36`, with line 34)

Author action: **changed** (your second remedy).

- The sentence `In 抽斗, 抽 writes ひき and 斗 writes だし; Daijisen lists 抽斗 ひきだし as a hard-to-read word.` is
  removed from line 36.
- The ひき- row (line 34) now uses the search-only spelling 抽出し ひきだし, "drawer", as its example, where 抽 writes
  ひき on its own. The cell says that JMdict heads the entry 引き出し, lists 抽出し as a search-only kanji form and marks
  抽き出し and 抽斗 as rarely used kanji forms, and that this index form is not a recommended word example. That is the
  wording other cards use for a source-only reading whose only JMdict example is a search-only form (for example 双, 圧
  and 訓, outside this packet).
- Line 36 explains 抽出し (抽 ひき, 出 だ, okurigana し), contrasts it with 抽出 ちゅうしゅつ, and keeps the unchanged
  抽き出し sentence. Its new last sentence keeps 抽斗 only as a whole-word reading: `Daijisen lists the rarely used
  spelling 抽斗 ひきだし as a hard-to-read word; this is a reading of the whole word, not a kanji-by-kanji reading, and
  KANJIDIC2 gives 斗 no reading だし.` This parallels `扇.md:58` on 団扇.
- Support: `evidence\jmdict-cited-entries.xml`, entry 1601650; `evidence\kanjidic2-斗.xml`, 斗's complete record in the
  pinned KANJIDIC2 input (ja_on ト and トウ, no ja_kun reading, nanori ます); the original packet's
  `evidence\public-source\weblio-抽.txt`, line 6.

To verify: that no sentence on lines 34-36 gives 斗 a reading or splits 抽斗 by kanji, that the 抽出し analysis and the
JMdict labels match entry 1601650, and that the 斗 claim matches the added KANJIDIC2 record.

### F2: けんねん is presented without JMdict's irregular-kana tag (`懸.md:46`)

Author action: **changed** (your first remedy).

- The last clause of line 46 now reads `JMdict lists けねん first and also けんねん, which it marks as irregular kana
  usage; in けんねん, 懸 supplies ケン.` It read `JMdict lists けねん first and also the reading けんねん, where 懸
  supplies ケン.` Nothing else on the line changed (`diffs\changed-lines.txt`).
- Support: `evidence\jmdict-cited-entries.xml`, entry 1257720 (`<re_inf>word containing irregular kana usage</re_inf>`
  on けんねん). The wording follows `扇.md:42` on おおぎ.

To verify: that the clause now reports the tag and that nothing else on the line changed.

## Other points in your report

No disposition is needed for these.

- **C1, O1, O2, O3 and O4.** Your report resolved C1, O1 and O3 and accepted the declines of O2 and O4. This revision
  changes no text those points concern.
- **Optional note on 懐's reading options (忙's うれえるさま).** No change: 忙 is outside this batch, and you noted the
  option as defensibly wrong. `checks\reading-options.txt` is identical to the earlier confirmation packet's copy apart
  from line 1.
- **Your limit on the 斗 reading.** The pinned KANJIDIC2 record for 斗 is now in `evidence\kanjidic2-斗.xml`.
- **Quiz audits.** No front matter changed. `checks\quiz-safety.txt` is byte-identical to the earlier confirmation
  packet's copy, and `checks\reading-exposure.txt` and `checks\reading-options.txt` are identical to it apart from line 1.
- **Android JVM tests and the Kotlin cross-check.** Not run for this revision either.

## Process notes

- The checks in `checks\` were run on the committed revision.
