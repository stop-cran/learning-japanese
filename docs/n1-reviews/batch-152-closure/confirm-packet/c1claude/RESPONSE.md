# Author's statement for the reviewer of `reports-152\initial-claude.md`

This statement answers only the points in YOUR initial report. Your report has no Findings; your Optional list has seven items,
O1 to O7, and they are answered below. The statement is the author's claim about what changed and why. Verify each claim against
the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet. Eight of the 15 new cards changed (跳 踏 載 輝 迫 遂 遣 避);
趣 躍 較 輩 逸 郡 郷, every existing kanji card, every stroke file and every word article are unchanged. Only `quiz_exclusions` lists
changed in front matter (seven cards, entries added only); no title, tag, `distractors` list, metadata reading, `quizOnyomi` or
`quizKunyomi` changed. See `CHANGES.md`. Give a disposition for each of O1 to O7.

## Optional

- **O1 (迫 coverage, 迫力): not changed.** The card is correct as it stands (you said so), and 迫力 would be a new sourced claim in a
  revision whose scope is the quiz-exclusion fixes. It is noted for a later polish pass.
- **O2 (迫/押): applied.** 押 is excluded on 迫 (`迫.md:14`), with the bullet "JMdict 押す sense 5 is “to push (someone for
  something); to press; to put pressure on (someone)” (entry 1180470), close to 迫る sense 2 and to this card's “press”." (`迫.md:50`;
  迫る sense 2 is “to press (someone for something); to urge; to compel”, entry 1475720). Entry 1180470 is added to the Metadata ids
  (`迫.md:54`).
- **O3 (exclusion candidates): applied for 避/脱, 輝/艶 and 跳/弾; 輝/華 added; 輝/映 not applied.**
  - 避/脱 (`避.md:14,52`): Kanjipedia gives のがれる for 避, KANJIDIC2 gives 脱 “escape from”, and JMdict 脱税 is “tax evasion”
    (entry 1416550). 脱 already excludes 逃 and 除, which 避 also excludes.
  - 輝/艶 (`輝.md:14,49`): JMdict 艶 つや sense 1 is “gloss; luster; lustre; shine; sheen; polish” (entry 1177680).
  - 跳/弾 (`跳.md:14,50`): JMdict 弾む sense 1 is “to spring; to bound; to bounce” (entry 1419400), close to 跳ねる's “to spring up;
    to bound; to hop”.
  - 輝/華 (`輝.md:14,50`), not in your list: KANJIDIC2 lists “shine” and “luster” for 華, and the existing card 華 (“flower;
    splendor; showiness”) already excludes 光 and 照, as 艶 does.
  - 輝/映: not applied. The displayed title of 映 is “reflect, project”, neither of which is a sense of 輝; the shine sense of 映 lives
    only in the verb 映える (JMdict 1600620 sense 1, “to shine; to glow”). The existing shine-family cards 光, 照, 華 and 艶 do not
    exclude 映 either, so excluding it here would be the first such pair.
- **O4 (easy Starter distractors for 迫 and 逸): not changed.** As you note, both sets are defensibly wrong both ways, and 迫's set
  keeps its Starter session curated-filled, which masks the 迫 せる / 競 collision.
- **O5 (遣 -つか.い example): applied, by replacing the example.** `遣.md:33` now gives 蛇遣い へびつかい “snake charmer” (JMdict
  entry 1753470, which also spells it 蛇使い and gives only the unvoiced reading), instead of 人形遣い, whose priority-tagged reading
  is the voiced にんぎょうづかい. The row therefore no longer needs a "usually づかい" qualifier. The Metadata id 1367140 is replaced
  by 1753470 (`遣.md:63`).
- **O6 (Daijisen name readings): checked; no card change needed.** `evidence\o6-daijisen-names.txt` re-runs `reading_exposure.py`
  on 載 迫 郷 輩 較 趣 with each card's audited `--extra` list plus the name readings you listed (載 こと, 迫 とお, 郷 あき and
  のり, 輩 とも, 較 あつ, とお and なお, 趣 とし). It reports 0 production hits, 0 padded-session hits and 0 one-holder hits; the only
  one-holder case is the known KANJIDIC2 name-only 載 のり (with 則, 法 or 準). For 載 こと (offered by 事, 琴 and 言): "it cannot be
  drawn in the N1 stack, All stack or Starter practice session pool", and a Starter session that borrows one holder card cannot
  draw it either (3 holders tried).
- **O7 (郷/区): not changed.** The displayed title of 区 is “ward; district”. KANJIDIC2 lists “district” for 郷, and Kanjipedia's
  fourth sense of 郷 is 昔の行政区画の一つ (an old administrative division), so “ward; district” is a defensible answer for 郷 under
  the rule that a pair needs an exclusion when a learner could reasonably accept either title for either word.

## Other changes in this revision (from the other review)

These were not raised by you; they are listed so that every hunk is accounted for. Direct "carry out" pairs are now excluded: 執
施 遂 on 踏 (`踏.md:14,49,50`, with entry 1372620 added to the Metadata ids at `踏.md:54`) and 執 施 履 on 遂 (`遂.md:14,54`). 運
(“carry; luck”) is excluded on 載 and joins the existing 積/荷 bullet, which cites JMdict 1600270 sense 3 “to load (luggage); to
carry; to take on board” (`載.md:14,50`). The "These N cards" counts are updated on every card whose list grew.
