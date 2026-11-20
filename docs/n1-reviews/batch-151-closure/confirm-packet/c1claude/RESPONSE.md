# Author's statement for the reviewer of `reports-151\initial-claude.md`

This statement answers only the points in YOUR initial report: finding C1 and optional items O1 to O6 (your Optional list,
numbered 1 to 6). The statement is the author's claim about what changed and why. Verify each claim against the revised text in
`snapshot\`, `diffs\fix.patch`, the `checks\` outputs and independent sources; do not rely on this text as evidence. Card line
numbers refer to the revised cards in this packet. Nine of the 15 new cards changed (誓 誘 謙 譲 護 豆 豪 貢 貴); 訴 証 詩 詳 誇 謡,
every existing kanji card, every stroke file and every word article are unchanged. One `quiz_exclusions` list (誘) and one
`distractors` list (譲) changed; no title, tag, metadata reading, `quizOnyomi` or `quizKunyomi` changed. See `CHANGES.md`. Give a
disposition for C1 and for each of O1 to O6.

## Finding

### C1: 貴's mnemonic misses one stroke

Author action: **changed** as you proposed. `貴.md:25` now says that 中 "sits at the top on a horizontal stroke 一," and 貝 sits at
the bottom, so the parts account for all 12 strokes (中 1-4, the ungrouped horizontal stroke 5, 貝 6-12 in
`evidence\kanjivg\08cb4.svg`). The picture is unchanged.

## Optional

- **O1 (謙 mnemonic): applied.** `謙.md:25` now describes 兼 as 八 at its top, "then a horizontal stroke, the shape ⺕, two vertical
  strokes 丨 and two final sweeping strokes", which accounts for KanjiVG strokes 8-17 (`evidence\kanjivg\08b19.svg`: 八 8-9, an
  ungrouped stroke 10, ⺕ 11-13, 丨 14 and 15, and the ungrouped strokes 16-17).
- **O2 (護 via 看護婦): not changed.** 看護婦 is the only word article in the repository that contains 護, so it remains the example
  word for the selected reading ゴ. The card states the obsolete status and the JMdict cross-reference to 看護師, and gives 保護
  ほご as a Joyo example (`護.md:23`). A new word article (保護 or 看護師) is outside this batch's scope; it can replace 看護婦 as the
  example when one exists.
- **O3 (誓 reading order): applied.** The ゼイ row now follows the セイ row, before the kun reading ちか.う (`誓.md:31-33`); neither
  row's text changed. The existing N1 cards almost always list an on reading that is outside the official table before the kun
  rows; three earlier cards (脈 華 覆) still list one after them and were not touched in this batch.
- **O4 (coverage polish: 告訴/起訴/控訴, 誘拐/おびき出す, 宣誓): not changed.** The suggested words are good study material, but adding
  them would add new sourced claims to this revision; both initial reviews judged scoped coverage clean.
- **O5 (譲 distractors): applied.** `譲.md:13` now lists 買 話 読, and `譲.md:57` explains them: buying is the other side of selling
  (譲る can mean “to sell”, JMdict 1357030 sense 4), and 話 and 読 share the radical 言 with 譲, but none means handing over or
  yielding. Your suggested 奪 and 受 were tried first and rejected: every tried set that included one of them (or 拾, 借 or 握) lets
  a Starter practice session that also borrows the card 攻 or 責 offer せめる, an attested reading of 譲, as a wrong answer to the
  ゆず.る prompt. Sets of Starter cards do not have this exposure. `evidence\distractor-trials.txt` records all eleven trials;
  `checks\quiz-safety.txt` and `checks\reading-exposure.txt` show the committed set.
- **O6 (縫 diff): no change needed.** The dropped clause, "this does not change the complete word's reading", qualified the old
  remark that 裁 had no kanji card yet. With 裁 now linked, that remark and its qualification no longer apply. The replacement
  line is the declared remark edit and `checks\kanji-remarks.txt` reports it applied as declared.

## Other changes in this revision (from the other review)

These were not raised by you; they are listed so that every hunk is accounted for. 訪 is removed from 誘's exclusions, the count
reads "These thirteen cards", and the 呼 bullet now cites JMdict 呼ぶ sense 3 “to invite” (entry 1266440, added to the Metadata
ids) (`誘.md:14,45,51,59`). The phrase "declaring word" is replaced by "example word" (and "both characters write the declaring
word X" by "both characters appear in the example word X") on `護.md:23,51`, `豆.md:23`, `豪.md:23,52`, `貢.md:23,46` and
`貴.md:23`.
