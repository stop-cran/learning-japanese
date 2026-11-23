# Author's statement for the reviewer of `reports-154\initial-claude.md`

This statement answers only the points in YOUR initial report: two Findings, C1 and C2; six Optional items, O1 to O6; and one
assumption in your Limits, answered as L1. The statement is the author's claim about what changed and why. Verify each claim against
the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet. Seven of the 15 new cards changed (随 隣 雄 項 飽 飾 黙); 隠 雷
霧 顕 飼 驚 鬼 鮮, every existing kanji card (including the remark edits on 塊, 微 and 鏡), every stroke file and every word article are
unchanged. The only front-matter changes are two `quiz_exclusions` lists: 随 gained 追, and 隣 gained 辺 and 側. No title, tag,
`distractors` list, metadata reading, `quizOnyomi` or `quizKunyomi` changed. See `CHANGES.md`. Give a disposition for each of C1, C2,
O1 to O6 and L1.

## Findings

- **C1 (雄 omits 英雄 and 雄大): fixed.** `雄.md:39-40` add two Common words: "英雄 えいゆう — hero; heroine; great person" (JMdict
  1174680, sense 1, in full) and "雄大 ゆうだい — grand; magnificent; majestic" (JMdict 1542540, whose only sense is "grand;
  magnificent; majestic; great; sublime"). `雄.md:45` now reads "Joyo lists ユウ, with 雄大, 英雄 and 雌雄 as examples; …"; the Joyo
  table (PDF p. 150, row 雄) prints "ユウ 雄大，英雄，雌雄". Entries 1174680, 1542540 and 1312940 (雌雄 しゆう) are added to the
  Metadata ids (`雄.md:61`). 雄勁 stays the linked word in the ユウ row (`雄.md:31`) that establishes the quiz reading, as you
  suggested. The two words went into Common words rather than into the ユウ row; see L1.
  - Your optional sub-remedy, naming 英雄 in the 英 exclusion note (`雄.md:57`), was **not applied**. That bullet justifies a shared
    meaning: 雄's sense "excellence; greatness; … great person" against 英's "outstanding". That both kanji appear in one compound is
    not a shared meaning, so naming 英雄 there would not strengthen the exclusion. 英雄 is now on the card, in Common words.
- **C2 (随 omits 随分): fixed.** `随.md:38` adds the Common word "随分 ずいぶん — very; considerably (JMdict marks it as usually written
  in kana)". The gloss is shortened from sense 1 of JMdict 1372800, "very; extremely; surprisingly; fairly; quite; considerably;
  awfully; terribly", which is marked "word usually written using kana alone". There is no 随分 article, so the bullet is plain text.
  Entry 1372800 is added to the Metadata ids (`随.md:60`).
  - 随時 and 随所, which you called less important, were **not added**. The card already names 随筆, 随意, 随伴, 随行 and 追随, and now
    随分, for ズイ.

## Optional

- **O1 (隣, とな.る row): applied.** `隣.md:32` now leads with "隣り合う となりあう — to adjoin each other; to sit side by side; JMdict
  entry 1598830, the Joyo example for this reading." It then says that the bare verb 隣る となる ("to neighbor (neighbour); to be
  adjacent to; to be next to") is marked archaic in JMdict 2163190. The Joyo line (`隣.md:41`) no longer repeats the 隣り合う gloss.
  Neither word is a quiz reading; the row still ends "Not selected for questions here."
- **O2 (飾, unnumbered senses): applied.** `飾.md:23` now reads "In JMdict, the first sense of the verb 飾る かざる is …, its second is
  …, and its fourth is … (entry 1357210)." The quoted glosses are unchanged, and the numbering matches the 華 bullet's "fourth sense".
  JMdict 1357210 has four senses; the third, "to mark (e.g. the day with a victory); to adorn (e.g. the front page); to grace (e.g.
  the cover)", is not quoted.
- **O3 (黙 coverage): applied in part.**
  - `黙.md:34`: the もだ.す row now adds "Kanjipedia lists もだす outside the table (外)". The Kanjipedia 黙 entry marks ボク, だんまり
    and もだす as 外 (`evidence\kanjipedia-outside-readings.json` in the original packet).
  - `黙.md:39-40` add the Common words "沈黙 ちんもく — silence; being silent" (JMdict 1431810, already cited) and "暗黙 あんもく —
    tacit; unspoken; implicit" (JMdict 1154700, its only sense). `黙.md:44` now reads "Joyo lists モク, with 暗黙 and 沈黙 among its
    examples, and だまる, …"; the Joyo table (PDF p. 148, row 黙) prints "モク 黙殺，暗黙，沈黙". Entry 1154700 is added to the
    Metadata ids (`黙.md:54`).
  - 黙祷 was **not added**. In JMdict 1535010, only the spelling 黙とう carries a priority mark (news1, nf22); 黙祷 has none. The card
    now names two everyday モク words.
- **O4 (黙 distractor 走): not changed.** You found 走 defensibly wrong; your point is that it is too easy. A curated distractor only
  has to be clearly wrong in both directions, and 走 "run" is. How hard distractors should be is a choice made across the whole corpus,
  not a defect of this card.
- **O5 (項 mnemonic wording): applied.** `項.md:25` now reads "… and 頁 stands on the right: a horizontal stroke and a left-falling
  stroke over 貝, "shellfish; seashell," which is made of 目, "eye," over 八, "eight."" In KanjiVG 09805 (`evidence\kanjivg-components.txt`
  in the original packet), 頁 is a horizontal stroke and a left-falling stroke over 貝, and 貝 is 目 over 八. There is no 頁 card, so 頁
  is described rather than linked. "Left-falling stroke" is the term used on the 人 card (original packet, `repo\kanji\人.md:23-24`).
- **O6 (card density): not changed.** As you say, the density is consistent with corpus style. Shortening the exclusion notes would be
  a corpus-wide change, not a change to this batch.

## Limits

- **L1 (your assumption that Common words lists only existing word articles): the assumption does not hold, and it decided where C1
  and C2 were fixed.** Common words bullets without a link are an established pattern. In the original packet's `repo\kanji\` (the
  reviewed snapshot), 1,812 Common words bullets on 1,003 kanji cards start without a link. In batch 153, for example,
  `repo\kanji\釈.md:40-41` list 釈放 and 会釈 unlinked. So 英雄, 雄大, 随分, 沈黙 and 暗黙 were added there as plain-text bullets, and
  the reading rows were left to the word that establishes the reading.

## Other changes in this revision (from the other review and the author's own checks)

You did not raise these; they are listed so that every hunk is accounted for.

- **随 excludes 追** (`随.md:14`, "These eleven cards" at `随.md:45`, new bullet at `随.md:56`): "the first sense of 追う おう is “to
  chase; to run after; to pursue; to follow after” (JMdict 1432410), which overlaps this card's “follow”; the 追 card lists お.う."
  Entry 1432410 is added to the Metadata ids (`随.md:60`).
- **隣 excludes 側 and 辺** (`隣.md:14`, "These seven cards" at `隣.md:44`):
  - `隣.md:50` (new): "the first sense of 側 そば (JMdict 1403830), a word usually written in kana, includes “(place) right next to”
    and “beside”, which overlap the first sense of 隣 となり, “next (to); adjoining; adjacent”; the 側 card lists そば."
  - `隣.md:49`: the 町 bullet now also covers 辺 (“vicinity; edge”): "the first sense of 辺り あたり is “(in the) neighbourhood;
    neighborhood; vicinity; nearby; surroundings” (1512080); the 辺 card lists あた.り." This came from the author's own check, not
    from a review. It rests on the same "neighbourhood" basis on which 隣 already excluded 町.
  - Entries 1512080 and 1403830 are added to the Metadata ids (`隣.md:54`).
  - 追, 辺 and 側 are unchanged, and each pair is declared once, on the batch card. None of the three is a curated distractor of 随 or
    隣, and neither 随 nor 隣 is a curated distractor of any card (`checks\quiz-safety.txt`).
  - The author also checked 逮 (“arrest; chase”) against 随 and did not add it. KANJIDIC2 lists only "apprehend" and "chase" for 逮,
    with no kun reading, so it has no "follow" sense to overlap 随's "follow; at will".
- **飽** (`飽.md:33-34, 56`):
  - The あ.かす row adds the second sense of 飽かす, "to use lavishly (and without regret)", often in the form 〜に飽かして (JMdict
    1518280).
  - The あ.く row adds, directly after 飽く and before 飽くまで: "For this verb, Digital Daijisen notes that modern standard Japanese
    generally uses あきる and that あく is a written-style expression (「あく」は文章語的な表現)." The note is placed before 飽くまで so
    that it does not attach to the adverb.
  - `evidence\daijisen-aku.txt` is the retrieved Digital Daijisen 飽く entry, including its [補説]. The entry is linked in the
    Metadata line as "Word register: [Digital Daijisen, 飽く](…)" (`飽.md:56`).
