# Author's statement for the reviewer of `reports-143\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 to C9 are your report's own Findings labels, and O1
to O8 are your Optional labels. The statement is the author's claim about what changed and why. Verify each claim
against the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet; other line numbers refer to the named file in
the original packet unless stated. Twelve of the 15 new cards changed (旋 既 旦 旨 暑 朗 条 架 柄 染 株 桜), the other three
(施 旗 暦) did not; front matter changed in 既 and 旋 only (`quiz_exclusions`, see `CHANGES.md`). Give a disposition for
each of C1 to C9 and O1 to O8.

## Findings

### C1 (minor): 既 and 朗 call the Joyo parenthesised form a "compatibility ideograph"

Author action: **changed** as you proposed.

- `既.md:38` now reads `It adds the traditional (Kangxi dictionary) form in parentheses.` and `朗.md:43` reads
  `The Joyo table adds the traditional (Kangxi dictionary) form in parentheses.` The compatibility-ideograph wording is gone.
- Support: `evidence\joyo-item6.txt` (表の見方 item 6, bunka.go.jp).

### C2 (minor): 桜 whole-word caveat covers 桜ん坊

Author action: **changed** as you proposed. `桜.md:37` limits the whole-word caveat to 桜桃 read さくらんぼ and says that
in 桜ん坊 桜 is plainly さくら, followed by ん and 坊 read ぼ. Support: `evidence\jmdict-cited-entries.xml` (1298460).

### C3 (minor): 桜 "mizaru cherry"

Author action: **changed**. `桜.md:25` now says `the fruit-cherry tree (ミザクラ, mizakura)`. Your remedy wrote `the fruit
cherry`; the author kept `tree` because Daijisen's sense reads 「木の名。ミザクラ」 (original packet,
`public-source\weblio-桜.txt`). Verify that this is a correct reading of ミザクラ.

### C4 (minor): 染 愛染 "whole-word reading" contradicts ゼン recorded by Daijisen

Author action: **changed** as you proposed. The ゼン row and `染.md:40` now say that 染 is read ゼン in 愛染, an on
reading outside the Joyo table, and the `does not establish an independent reading` sentence is gone. `染.md:42` now
says Daijisen and Kanjipedia record ゼン. Support: original packet `public-source\weblio-染.txt`,
`kanjipedia-outside-readings.json`; `evidence\jmdict-cited-entries.xml` (2583650).

### C5 (minor): 旨 旨味 is a separate JMdict entry; 上手い/巧い spelling

Author action: **changed** as you proposed. `旨.md:37` now cites the separate うまみ entry (旨み, 旨味 tagged ateji, 旨 read
うま in both) and drops `not a reading to split`; `旨.md:25` says JMdict spells the skillful sense 上手い or 巧い.
Support: `evidence\jmdict-cited-entries.xml` (1310520) and the original packet's `jmdict-families.xml` (1310460).

### C6 (minor): 株 守株 is transparently シュ + シュ

Author action: **changed** as you proposed. `株.md:25` presents 守株 しゅしゅ as 守 シュ + 株 シュ, an idiom from the fable of
guarding a tree stump. Your optional mention of 株を守る くいぜをまもる was not added. Support:
`evidence\jmdict-cited-entries.xml` (1882040). The echo at `株.md:36` (`The standalone シュ word and 守株 are separate lexical identities.`) is unchanged; check that it still reads correctly.

### C7 (minor): 旗 title shares "standard" with 準, 範 and 規

Author action: **declined**, with reasons. Neither the title nor `旗.md:14` changed.

- The curated distractors (施, 旋, 旅) fill all three slots on the 旗 prompt, so the pair cannot occur on that prompt.
  `quiz-safety.txt` shows 0 errors and 0 warnings for the batch, and you did not open it.
- The author's view is that, in the title text, military "standard" (a flag) and normative "standard" (a norm) are
  distinguishable. Dropping a word from a published
  title is a change to the title index, which affects every card that links to 旗 and its word article; it was not made
  for a medium-confidence concern about fallback draws.
- To verify: whether a 準, 範 or 規 prompt can draw 旗 as a fallback option in a shipped pool (`reading-exposure.txt` and
  `QuizBuilder.kt` in the original packet), and whether you still regard this as only minor.

### C8 (minor): 旦 garbled sentences; ダンナ in katakana

Author action: **changed** as you proposed. `旦.md:25` and `旦.md:52` now say that no ordinary JMdict word was found that
uses あした and that 一旦 is read いっ + タン; `旦.md:41` writes だんな.

### C9 (minor): 柄 Common words pairs え with "pattern"

Author action: **changed**. `柄.md:48-49` now has two bullets, `柄 え — handle; grip` and `柄 がら — pattern; design`, both
linking the same word article. Support: `evidence\jmdict-cited-entries.xml` (1508290 え; 1508300 がら).

## Optional

- **O1 (条 すじ row, lead with "line; stripe"): not applied.** The row follows JMdict's entry for 筋 and its sense
  order; the card already says that no word article exists yet and that the reading is not selected for questions.
- **O2 (条 stroke wording; jargon paragraph): partly applied.** `条.md:58` now says `an added horizontal stroke` instead of
  `a changed upper stroke`. The jargon paragraph was not trimmed.
- **O3 (架 attribution): applied.** `架.md:25` now uses 書架 しょか, bookshelf, an example in the Daijisen extract.
- **O4 (朗 distractors named): applied.** `朗.md:51` says `The cards 月, 有 and 朝 supply the distractors`.
- **O5 (odd English in the copied word-article titles): not applied.** The word articles are outside this batch's scope.
- **O6 (施 title overlaps): no change.** Your own judgement was that the meanings differ clearly enough.
- **O7 (add 菌株 to 株): not applied.** 雌雄異株 is the Daijisen example for the rooted-plant sense; 菌株 is not in the
  Daijisen extract and the Metadata line would gain another entry.
- **O8 (朗 name readings): no change.** Name readings need no account on the card.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **旦 `旦つく` (a slighting word)** (`旦.md:34`) and **暑 蒸し暑い** (`暑.md:36`; 蒸 writes む, し is okurigana) are explained
  in `CHANGES.md`.
- **Exclusions:** 旋 lost 凱 and 既 lost 在, 存 and 有 from `quiz_exclusions`, with the matching Notes sentences on
  `旋.md:54` and `既.md:48`. The author's reason is that those pairs are associations through a shared compound or
  topic, not direct meaning confusions: the displayed titles are 既 "already; previously", 在 "exist; be located", 存
  "exist; be aware", 有 "have, exist", 凱 "victory song; triumph" and 旋. Your report treated the exclusions as direct
  pairs, so please re-check both cards' meaning-quiz options with the exclusions removed, using `QuizBuilder.kt` and
  those titles, and say whether any resulting pair now has two defensible answers.
- **条 `条.md:61` (new since the previous revision):** the whole-word caveat now applies to 発条 ばね only; in 条彫り and 条播き 条 is read すじ, the kun reading already in the table. Support: the original packet's `public-source\weblio-条.txt`. **旨 `旨.md:25`:** the skillful-sense spelling is now worded as JMdict's `esp.` marking (`especially written 上手い or 巧い`). Both are listed in `CHANGES.md`.

## Process notes

- `9b8f50a8` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `6b5934e7`.
- The checks in `checks\` were run on the committed revision. Front matter changed in 旋 and 既, and the three quiz and
  reading audits are unchanged apart from their command lines (see `CHANGES.md`).
