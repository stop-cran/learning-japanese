# Author's statement for the reviewer of `b158-60d2-reports\grok.md`

This statement answers only the points in YOUR initial report. X1-X9 are your report's Findings 1-9, and O1-O7 are the seven
points of your Optional paragraph in order. Your Limits describe your own method and need no answer. The statement is the author's
claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\`
outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised
files in this packet. Several line numbers in your report do not match the files (for example, 升's opening is line 23 of
`kanji\升.md`, not line 19); this statement uses the line numbers of the files in `snapshot\`. Nine batch kanji cards changed (all
but 匠), as did six of the ten new word articles (偏見 傍観 勲章 升 即座 師匠). The ledger `docs\n1-sources\batch-158-progress.json`,
the batch's pinned JMdict extract `batch-158-jmdict.xml` and its entry list `batch-158-jmdict-selection.json` changed (13 entries
added for the newly cited ids), and the generated `manifest.json` was regenerated. Every stroke file, every reused kanji card and
every other word article is unchanged. See `CHANGES.md`. Give a disposition for each of X1-X9 and O1-O7, and judge the other
reviews' changes described below.

## Findings

### X1: the grid-square sense of the word 升

Author action: **changed**. `words\升.md:15` no longer gives the grid-square sense (JMdict 1346290 sense 3, noted "esp. マス"). It
now explains sense 2, "a box, as in box seating at a theatre and similar places", with 升席 ますせき, a tatami "box seat" for four
people at sumo, kabuki and similar shows (entry 1706800). The Dictionary line (line 34) cites senses 1-2 and compares entries
2248100, 1706800 and 1288370. The kanji card keeps 升目 ますめ (entry 1654590) in its ます row (`kanji\升.md:30`). The word's title is now
"measuring box" (lines 4 and 11).

### X2: the 昇 interchange on 升

Author action: **changed**. `kanji\升.md:23` now reads: "Digital Daijisen also gives two more senses, rising and, from grain
ripening, a peaceful, well-governed age; it notes that in these two senses 升 is used interchangeably with 昇." This limits the
statement to the two senses of Daijisen's 補説 「2・3は「昇」と通用する」 (original packet, `evidence\public-source\weblio-升.txt`).

- The card does not add "it is not a free substitute for 昇" or a claim about 上昇. Daijisen does not say this, and the author has
  no source for it; "in these two senses" is the limit the source sets.
- のぼ.る is not added to the metadata. Line 40 says only that Kanjipedia gives the kun reading のぼ.る, marked as outside the Joyo
  table (外), and that it is not in the card's metadata and is not quizzed.

### X3: the support word 升 ます carries only news2/spec2

Author action: **not changed** (升 ます remains the support word), **record changed**.

- The rule that governs support words is in `evidence\rule-7058679348.md`, point 2 ("Choice of word"). It prefers a spelling with
  one of news1, ichi1, spec1 or gai1, and says: "where none exists, an untagged word may be used with a justification reviewed for
  that row." The frozen ledger recorded the missing tag but gave no row-specific justification, as you found.
- Ledger line 29 (`selectionReason`) now says that no candidate written with 升 carries a qualifying tag, "so the rule's untagged
  route applies", and that the row-specific justification is in the 升 support mapping and must receive independent review.
- Ledger line 132 (`exceptionReason`) is that justification. It says that:
  - 升 ます (1346290) is the only 升 entry with any priority marker (news2/spec2, treated as untagged);
  - its spelling and reading carry no irregular, rare, outdated, ateji or gikun mark;
  - ます is a KANJIDIC2 reading of 升, and the word is the single kanji, so no other card is needed;
  - its sense 1, "measuring box", matches the first KANJIDIC2 meaning of 升 and the card's main meaning, and it backs the quizzed
    kun reading ます;
  - the alternatives are all untagged: 升 しょう (2248100) is the volume unit; 一升 (1163460) and 一升瓶 (1163470) use the
    unselected ショウ reading; 升目 (1654590) is a derived word.
- The same record precedes this batch for 仙人 and 伯仲 (B156) and 諸侯 (B157). `evidence\support-selection.json` holds the
  selection statement and every support mapping at the revised snapshot, and the entries are in
  `evidence\jmdict-cited-entries.xml`.
- The owner has not yet ruled on whether news2/spec2 should count as qualifying; the author will ask again when the batch is
  published.

Please judge whether this justification satisfies the rule's untagged route for this row.

### X4: 即's opening

Author action: **changed**. `kanji\即.md:23`: "Digital Daijisen also gives the sense of attaching closely to something, read つく,
and lists 即位 そくい, accession to the throne, under it; it also gives the sense “that is; namely,” read すなわち."

- The accession gloss is now in the same sentence as the sense. The bridge is the reading つく, given in that sentence; the table's
  つ.く row (line 30) shows 即く つく, "ascend (the throne)", which JMdict 1331530 lists as another spelling of 就く for that sense.
- 色即是空 is dropped. The すなわち sense is given with its reading, and the table's すなわ.ち row (line 32) gives 即ち すなわち,
  "that is; namely" (entry 1404100).
- Daijisen's character entry is in the original packet, `evidence\public-source\weblio-即.txt`: 「そのものにぴったりくっつく。つく。」
  with 即位 among its examples, and 「すなわち。」 as the next sense.

### X5: 債権 and 債券

Author action: **changed**. `kanji\債.md:23` gives the readings ふさい, さいむ and さいけん at first mention and says: "債権 and 債券
sound the same but are different words." 債権 is "a claim" and 債券 is "a bond", with 国債 and 社債 as the bond examples. The サイ row
(line 29) adds 債券 さいけん, "bond; debenture" (entry 1292070).

### X6: 勲's rank example and 元勲

Author action: **changed**. `kanji\勲.md:23` now gives 元勲 げんくん, "elder statesman" (entry 1260770), and illustrates the rank
sense with 勲一等 くんいっとう, "order of the 1st class" (entry 1247200), instead of 叙勲. 叙勲 じょくん stays in the クン row (line
29) and the common words (line 36) as "conferring of decorations".

### X7: 却's "doing something completely"

Author action: **changed**. `kanji\却.md:23` now illustrates the sense with 忘却 ぼうきゃく, which JMdict glosses as "forgetting
completely; oblivion" (entry 1519260). 冷却 is no longer cited for this sense.

### X8: priority-tag jargon in the 升 Notes

Author action: **changed**. The sentence naming JMdict's priority tags is deleted from `kanji\升.md:40`; the tag audit stays in the
ledger (X3). The kokuji clause is kept.

### X9: 匿 and 皮

Author action: **changed**. `kanji\匿.md:14` now excludes 皮. Line 40 gives the reason: 皮 ("skin; hide") shares only the English
word "hide", there meaning an animal skin. The cards are not merged.

## Optional notes

### O1: "order" in 勲章

Author action: **changed**. `words\勲章.md:15`: "Here “order” means an order of merit, an honour awarded for service, not a command."

### O2: Rakugo in 師匠

Author action: **changed**. `words\師匠.md:18` glosses it: "Rakugo (traditional Japanese comic storytelling) performers train under
a master for many years." Line 15 also explains a stable master as "the head of a sumo stable".

### O3: kana at first mention

Author action: **changed**. 偏狭 へんきょう and 人偏 にんべん (`kanji\偏.md:23`), 傍系 and 傍流 (`kanji\傍.md:23`), and 元勲 げんくん
(`kanji\勲.md:23`) now have their readings at first mention.

### O4: 座 in 即座

Author action: **changed**. `words\即座.md:24`: "[座] means a seat or to sit."

### O5: だけではいけません in 傍観

Author action: **changed**. `words\傍観.md:17`: "You must not just stand by and watch people in trouble."

### O6: "spurious article" and "source-only"

Author action: **changed**. 偽物's gloss in the にせ row (`kanji\偽.md:32`) is now "forgery; counterfeit; imitation", three of the
glosses of JMdict 1577800 sense 1, without "spurious article". The label "source-only" is kept because the readings tables use it,
and it is now defined where it is used: "Here “source-only” means that a source lists the reading but no checked word example uses
it" (`kanji\偽.md:44`, `kanji\却.md:43`).

### O7: the repeated "meaning-quiz distractors are…" sentences

Author action: **not changed**. All ten cards in this batch, and 126 kanji cards in the repository, state their curated distractors
this way, so a reader can check that none of them is a correct answer. You did not report them as errors.

## Changes made for the other reviews

The other two reviews asked for the changes below. Please judge each change as a reviewer of the revised text, not only as an
answer to your own notes.

1. **偏見 excludes 意見.** `words\偏見.md:8`; line 28 glosses 意見 "an opinion or view in general" (entry 1156530) and says 偏見 is a
   view that leans to one side. `evidence\word-quiz.txt`, lines 8-18, shows the new option set.
2. **The word 升 excludes 腰掛け** "seat; bench" (`words\升.md:8`), which the reviewed snapshot could offer. Line 28 says why:
   腰掛け is a seat or bench (JMdict entry 1288370), while 升 in its second sense is a whole box of seating. `CHANGES.md` explains
   why 席, 座席 and 客席 are not excluded.
3. **偏 excludes 側** (`kanji\偏.md:14`; reason at line 40: KANJIDIC2 lists "side" among the meanings of 偏).
4. **偽's distractor 犬 is replaced by 耳** "ear" (`kanji\偽.md:13`, `48`). JMdict 1258330 sense 4 of 犬 is "counterfeit; inferior;
   useless; wasteful" (`evidence\distractor-senses.txt`), so "none means fake or false" did not hold for 犬.
5. **債's antonym note** (`kanji\債.md:40`): "the debt owed by one side and the claim held by the other" (was "held by the
   lender").
6. **Readings the sources give but the cards did not show.** One Notes line each names the reading, its source and its Kanjipedia
   外 mark, and says it is not in the card's metadata and is not quizzed: 偏 ひとえに, spelled 偏に (entry 1510320)
   (`kanji\偏.md:42`); 傍 ホウ with 傍輩 ほうばい (entry 1517130) and そ.う (`kanji\傍.md:46`); 匿す as a rarely used spelling of 隠す
   (entry 1170650), and ジョク and かく.れる (`kanji\匿.md:42`); 即 ショク (`kanji\即.md:45`); 債 か.り and か.し
   (`kanji\債.md:42`); 勲 いさおし (`kanji\勲.md:42`); 升 のぼ.る (`kanji\升.md:40`).
7. **"a wooden masu (measuring box)"** in the 升 sake example (`words\升.md:18`).
8. **Evidence.** `evidence\jmdict-cited-entries.xml` includes the complete pinned entries for every id the revised text cites;
   `evidence\verify-commit.txt` holds the signature checks for both snapshots; `evidence\selection-order.tsv` lists the frozen
   source rows 1-140 with grade and card status at the base, showing that this batch is the first ten Joyo rows with no card.

Every other changed line is a Metadata line or Dictionary line that adds the JMdict entry ids cited above, a ledger line that
records the same changes, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
