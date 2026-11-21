# Batch 154 revision: what changed from f8f3db8c to e5c945d6

Revised snapshot: `e5c945d6` (full hash `e5c945d6d3f83b97145100528e448747424fded5`; also in `packet-manifest.json`). It is one
commit after the reviewed snapshot `f8f3db8c9ae7d88d72cdc3d8eaae84c8f736ca5f`. Nothing is published.

- Seven of the 15 new kanji cards changed (随 隣 雄 項 飽 飾 黙). 隠 雷 霧 顕 飼 驚 鬼 鮮, every existing kanji card (including the
  remark edits on 塊, 微 and 鏡), every stroke file and every word article are unchanged.
- **Front-matter changes:** only two `quiz_exclusions` lists changed, and nothing was removed from either.
  - 随 (line 14) gained 追: `[従, 循, 則, 守, 屈, 応, 供, 縦, 準, 仕, 追]`.
  - 隣 (line 14) gained 辺 and 側: `[次, 翌, 接, 近, 町, 辺, 側]`.

  No title, tag, `distractors` list, metadata reading, `quizOnyomi` or `quizKunyomi` changed in any card. No existing card's front
  matter changed. Each new pair is declared once, on the batch card; 追, 辺 and 側 declare no `quiz_exclusions`.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. Four cards gained lines, so their later lines moved down:
  - 随 gained line 38 and line 56, so old lines 38-54 are now 39-55 and old lines from 55 on are two lines lower.
  - 隣 gained line 50, so old lines from 50 on are one line lower.
  - 雄 gained lines 39-40, so old lines from 39 on are two lines lower.
  - 黙 gained lines 39-40, so old lines from 39 on are two lines lower.

  項, 飽 and 飾 kept their line numbers.
- `diffs\fix.patch` is the exact patch from `f8f3db8c` to `e5c945d6`; `diffs\changed-lines.txt` lists the changed lines per file.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. The original packet's
  `evidence\audits\` files (quiz safety, reading exposure, reading options) describe the reviewed snapshot and are superseded by this
  packet's `checks\`.

## Changed lines

| File | Changed lines | Change |
| --- | --- | --- |
| 随 | 14, 38, 45, 56, 60 | 14: 追 excluded. 38 (new): Common words "随分 ずいぶん — very; considerably (JMdict marks it as usually written in kana)". 45: "These eleven cards" (was "ten"). 56 (new): "[追](追.md) (“chase; pursue”): the first sense of 追う おう is “to chase; to run after; to pursue; to follow after” (JMdict 1432410), which overlaps this card's “follow”; the 追 card lists お.う." 60: JMdict entries 1372800 and 1432410 added to the Metadata ids. |
| 隣 | 14, 32, 41, 44, 49, 50, 54 | 14: 辺 and 側 excluded. 32: the とな.る row now leads with 隣り合う となりあう (“to adjoin each other; to sit side by side”, JMdict 1598830, the Joyo example for this reading) and then says the bare verb 隣る となる is marked archaic in JMdict 2163190 (it used to show only 隣る). 41: the Joyo line no longer repeats the 隣り合う gloss, which is now in the row. 44: "These seven cards" (was "five"). 49: the 町 bullet now also covers [辺](辺.md) (“vicinity; edge”), adding "the first sense of 辺り あたり is “(in the) neighbourhood; neighborhood; vicinity; nearby; surroundings” (1512080); the 辺 card lists あた.り". 50 (new): "[側](側.md) (“side”): the first sense of 側 そば (JMdict 1403830), a word usually written in kana, includes “(place) right next to” and “beside”, which overlap the first sense of 隣 となり, “next (to); adjoining; adjacent”; the 側 card lists そば." 54: entries 1512080 and 1403830 added to the Metadata ids. |
| 雄 | 39, 40, 45, 61 | 39-40 (new): Common words "英雄 えいゆう — hero; heroine; great person" and "雄大 ゆうだい — grand; magnificent; majestic". 45: the Joyo line now reads "Joyo lists ユウ, with 雄大, 英雄 and 雌雄 as examples; …" (it used to name no ユウ example). 61: entries 1174680, 1542540 and 1312940 added to the Metadata ids. |
| 項 | 25 | The mnemonic now reads "… and 頁 stands on the right: a horizontal stroke and a left-falling stroke over [貝](貝.md), "shellfish; seashell," which is made of [目](目.md), "eye," over [八](八.md), "eight."" (was "and 頁, a shape, stands on the right; inside 頁 is [貝](貝.md), … made of …"). |
| 飽 | 33, 34, 56 | 33: the あ.かす row adds "whose second sense is “to use lavishly (and without regret)”, often in the form 〜に飽かして". 34: the あ.く row adds, directly after 飽く's entry id and before 飽くまで, "For this verb, Digital Daijisen notes that modern standard Japanese generally uses あきる and that あく is a written-style expression (「あく」は文章語的な表現)." and introduces 飽くまで with "Also". 56: Metadata adds "Word register: [Digital Daijisen, 飽く](https://www.weblio.jp/content/%E9%A3%BD%E3%81%8F)". |
| 飾 | 23 | The Meaning sentence now numbers the JMdict senses of 飾る it quotes: "In JMdict, the first sense of the verb [飾る](../words/飾る.md) かざる is …, its second is …, and its fourth is … (entry 1357210)." (It used to list the three glosses without saying which senses they are.) The quoted glosses are unchanged. |
| 黙 | 34, 39, 40, 44, 54 | 34: the もだ.す row adds "Kanjipedia lists もだす outside the table (外)". 39-40 (new): Common words "沈黙 ちんもく — silence; being silent" and "暗黙 あんもく — tacit; unspoken; implicit". 44: the Joyo line now reads "Joyo lists モク, with 暗黙 and 沈黙 among its examples, and だまる, …". 54: entry 1154700 added to the Metadata ids (沈黙, 1431810, was already cited). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the word articles 隣, 眼鏡 and 鏡, whose Dictionary line cites no JMdict entry id), as at the
  freeze. `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: rebuilding `manifest.json` leaves it unchanged
  and the tree clean. `budget.txt` and `vocabulary.txt`: informational.
- `linkplan.txt`: 19 changed word files, 19 added link pairs, 0 problems, as at the freeze.
- `kanji-remarks.txt`: 15 new cards, 3 modified existing cards (塊 微 鏡), 3 declared remark edits applied, 0 problems, as at the
  freeze.
- `quiz-safety.txt`: 0 errors, 0 warnings; identical to the freeze. The meaning options of 随 and 隣 are still their three curated
  titles. None of 追, 辺 and 側 is a curated distractor of a batch card, and neither 随 nor 隣 is a curated distractor of any card.
- `reading-exposure.txt`: apart from the command line, identical to the freeze: 0 production hits, 0 padded-session hits, the same 8
  latent collisions, 0 one-holder hits and the same 3 more for KANJIDIC2 name-only readings. No reading list changed.
- `reading-options.txt`: apart from the command line, identical to the freeze; 0 problems.
- `evidence\meta-scan.txt` (output of `meta_scan.py` on the 15 cards at `e5c945d6`) lists the same 10 whole-run gaps as at the
  freeze. Among its part-of-run matches, five lines differ from the freeze: 合う in 隣り合う     (隣:32; the scan reports each word in a given run once per card, at
    its first line, and at the freeze that was the Joyo line 41), 特に (雄:57, an unchanged line that moved down by two), and 文章, 文章語 and 表現 inside the quoted 「あく」は文章語的な表現
  (飽:34, new).
- The Android JVM tests that read the real content were not run, as at the freeze (no JDK on this machine).

## Process notes

- `e5c945d6` is the single fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `f8f3db8c`.
- One change comes from the author's own check, not from a review: while checking the 側 point, a search of the kanji titles found 辺
  (“vicinity; edge”), whose あたり sense matches the "neighbourhood" basis on which 隣 already excluded 町. It was added to the 町
  bullet (隣:49).
- Before the commit, a dry run of the checks showed 雌雄, newly named on 雄:45, as a meta-scan whole-run gap; JMdict 1312940 was added
  to 雄's Metadata ids in the same commit.
- The checks in `checks\` were run on the committed revision `e5c945d6`.
