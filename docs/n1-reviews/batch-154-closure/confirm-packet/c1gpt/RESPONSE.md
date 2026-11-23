# Author's statement for the reviewer of `reports-154\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 and G2 are your report's Findings. Your Optional section has
three bullets, called GO1 (gloss ……に飽かして and mark independent 飽く as written-style without implying that あくまで is), GO2 (a
plain-text 英雄 on 雄) and GO3 (shorten the learner-visible dictionary explanations and exclusion rationales) below. Your Limits
describe your own method and need no answer. The statement is the author's claim about what changed and why. Verify each claim
against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and independent sources; do not rely on this text
as evidence. Card line numbers refer to the revised cards in this packet. Seven of the 15 new cards changed (随 隣 雄 項 飽 飾 黙);
隠 雷 霧 顕 飼 驚 鬼 鮮, every existing kanji card (including the remark edits on 塊, 微 and 鏡), every stroke file and every word
article are unchanged. The only front-matter changes are two `quiz_exclusions` lists: 随 gained 追, and 隣 gained 辺 and 側. No
title, tag, `distractors` list, metadata reading, `quizOnyomi` or `quizKunyomi` changed. See `CHANGES.md`. Give a disposition for
each of G1, G2, GO1, GO2 and GO3.

## Findings

### G1: missing direct exclusion of 追 on 随

Author action: **changed** as you proposed; the pair is declared once, on 随.

- `随.md:14` is now `quiz_exclusions: [従, 循, 則, 守, 屈, 応, 供, 縦, 準, 仕, 追]`, and `随.md:45` reads "These eleven cards are
  excluded from meaning choices:".
- The new bullet at `随.md:56` reads: "[追](追.md) (“chase; pursue”): the first sense of 追う おう is “to chase; to run after; to
  pursue; to follow after” (JMdict 1432410), which overlaps this card's “follow”; the 追 card lists お.う." Entry 1432410 is added to
  the Metadata ids (`随.md:60`).
- 追 is unchanged and declares no exclusions. The curated distractors are unchanged: 随 has 逆 離 導 and 追 has 近 週 返, so neither
  is a curated distractor of the other. `checks\quiz-safety.txt` still shows 随's meaning options as its three curated titles. Under
  `docs/content-format.md`'s rule that a declaration on either card excludes the direct pair, your reduced pool `{追, 近, 週, 随}`
  can no longer offer “follow; at will” for 追, nor “chase; pursue” for 随.

### G2: missing direct exclusion of 側 on 隣

Author action: **changed** as you proposed, and 辺 was added on the same card after the author's own check (see below).

- `隣.md:14` is now `quiz_exclusions: [次, 翌, 接, 近, 町, 辺, 側]`, and `隣.md:44` reads "These seven cards are excluded from
  meaning choices:".
- The new bullet at `隣.md:50` reads: "[側](側.md) (“side”): the first sense of 側 そば (JMdict 1403830), a word usually written in
  kana, includes “(place) right next to” and “beside”, which overlap the first sense of 隣 となり, “next (to); adjoining; adjacent”;
  the 側 card lists そば." The bullet names only the locational overlap, as your finding does. Entry 1403830 is added to the Metadata
  ids (`隣.md:54`).
- 側 is unchanged and declares no exclusions. 隣 has the curated distractors 遠 奥 裏 and 側 has 内 右 左. `checks\quiz-safety.txt`
  still shows 隣's meaning options as its three curated titles. Your reduced pool `{側, 内, 右, 隣}` can no longer offer
  “next door; adjoining” for 側, nor “side” for 隣.
- **辺, from the author's own check.** A search of the kanji titles while checking 側 found 辺 (“vicinity; edge”). The 町 bullet at
  `隣.md:49` now also covers it: "the first sense of 辺り あたり is “(in the) neighbourhood; neighborhood; vicinity; nearby;
  surroundings” (1512080); the 辺 card lists あた.り." That is the same "neighbourhood" basis on which 隣 already excluded 町 (隣人
  “neighbour; neighbor; (people in the) neighbourhood; neighborhood”, 1555850). 辺 is unchanged, declares no exclusions and has the
  curated distractors 返 込 道. Entry 1512080 is added to the Metadata ids (`隣.md:54`).
- The author also checked 逮 (“arrest; chase”) against 随 and did not add it. KANJIDIC2 lists only "apprehend" and "chase" for 逮,
  with no kun reading, so it has no "follow" sense to overlap 随's "follow; at will".

## Optional

- **GO1 (飽かして and written-style 飽く): applied, both parts.**
  - `飽.md:33`: the あ.かす row now reads "飽かす あかす — to bore; to tire; to weary; JMdict entry 1518280, whose second sense is “to
    use lavishly (and without regret)”, often in the form 〜に飽かして." In JMdict 1518280, sense 2 carries the note "often
    intransitively as 〜に飽かして".
  - `飽.md:34`: the あ.く row now reads, directly after 飽く's entry id: "For this verb, Digital Daijisen notes that modern standard
    Japanese generally uses あきる and that あく is a written-style expression (「あく」は文章語的な表現). Also [飽くまで](…) あくまで
    — …". The note comes before 飽くまで and says "For this verb", so it does not attach to the adverb; the 飽くまで part of the row is
    unchanged apart from "Also". `evidence\daijisen-aku.txt` is the retrieved Digital Daijisen 飽く entry; its [補説] reads
    「現代、共通語では一般に「あきる」（上一）を用い、「あく」は文章語的な表現。また、「飽くまで」のような形で用いられる。」
  - The Daijisen 飽く entry is linked in the Metadata line as "Word register: [Digital Daijisen, 飽く](…)" (`飽.md:56`). Separate
    links to a word headword beside the character headword already exist, for example on 劾 ("Compound meanings: [Digital Daijisen,
    弾劾]", original packet `repo\kanji\劾.md`).
- **GO2 (英雄 on 雄): applied.** `雄.md:39` adds the plain-text Common word "英雄 えいゆう — hero; heroine; great person" (JMdict
  1174680, sense 1). The other reviewer independently asked for 英雄 and 雄大, so `雄.md:40` also adds "雄大 ゆうだい — grand;
  magnificent; majestic" (JMdict 1542540), and `雄.md:45` names the Joyo ユウ examples 雄大, 英雄 and 雌雄 (Joyo table, PDF p. 150).
  Entries 1174680, 1542540 and 1312940 (雌雄) are added to the Metadata ids (`雄.md:61`). 雄勁 stays the linked word that establishes
  the quiz reading.
- **GO3 (shorter explanations): not changed.** Each excluded card gets one bullet with its source reason. That is the Notes format
  across the existing N1 cards, and it lets a reviewer check each pair without leaving the card. Shortening the bullets on some
  cards of one batch would make them inconsistent with the rest. It is a style question for the whole corpus, not a defect of this
  batch.

## Other changes in this revision (from the other review)

You did not raise these; they are listed so that every hunk is accounted for.

- `随.md:38`: Common words add "随分 ずいぶん — very; considerably (JMdict marks it as usually written in kana)", shortened from JMdict
  1372800 sense 1. 1372800 is added to the Metadata ids (`随.md:60`).
- `隣.md:32`: the とな.る row now leads with the Joyo example 隣り合う となりあう (“to adjoin each other; to sit side by side”, JMdict
  1598830), and then says that the bare verb 隣る となる is marked archaic in JMdict 2163190. `隣.md:41`, the Joyo line, no longer
  repeats the 隣り合う gloss.
- `項.md:25`: the mnemonic now reads "… and 頁 stands on the right: a horizontal stroke and a left-falling stroke over 貝, … which is
  made of 目, … over 八, …" (it used to call 頁 "a shape").
- `飾.md:23`: the Meaning sentence now numbers the senses of 飾る it quotes ("the first sense …, its second is …, and its fourth is …",
  JMdict 1357210); the glosses are unchanged.
- `黙.md:34, 39-40, 44, 54`: the もだ.す row adds "Kanjipedia lists もだす outside the table (外)"; Common words add 沈黙 ちんもく
  “silence; being silent” and 暗黙 あんもく “tacit; unspoken; implicit” (JMdict 1154700); the Joyo line names 暗黙 and 沈黙 as モク
  examples (Joyo table, PDF p. 148); 1154700 is added to the Metadata ids.
