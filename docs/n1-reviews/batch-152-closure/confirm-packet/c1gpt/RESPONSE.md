# Author's statement for the reviewer of `reports-152\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 and G2 are your report's own Findings labels; your Optional
section has two bullets, called GO1 (shorten or separate the source-audit material in Notes, translate source quotations, gloss
"ateji") and GO2 (the wording of 迫's distractor sentence about 出) below, and L1 is the unresolved `../articles/compound-sound-changes.md`
links in your Limits. The statement is the author's claim about what changed and why. Verify each claim against the revised text in
`snapshot\`, `diffs\fix.patch`, the `checks\` outputs and independent sources; do not rely on this text as evidence. Card line
numbers refer to the revised cards in this packet. Eight of the 15 new cards changed (跳 踏 載 輝 迫 遂 遣 避); 趣 躍 較 輩 逸 郡 郷,
every existing kanji card, every stroke file and every word article are unchanged. Only `quiz_exclusions` lists changed in front
matter (seven cards, entries added only); no title, tag, `distractors` list, metadata reading, `quizOnyomi` or `quizKunyomi`
changed. See `CHANGES.md`. Give a disposition for each of G1, G2, GO1, GO2 and L1.

## Findings

### G1: missing direct "carry out / complete" exclusions

Author action: **changed** as you proposed; each pair is declared once, on the new cards.

- 踏 now excludes 執 施 遂 (`踏.md:14`; "These five cards" at `踏.md:45`). `踏.md:49` explains 執 and 施: "both titles include
  “carry out”, which matches Kanjipedia's ふみ行う and KANJIDIC2's “carry through” for 踏." `踏.md:50` explains 遂: "KANJIDIC2 lists
  “carry through” for 踏 and “accomplish” for 遂; JMdict 踏む sense 4 ends “to complete”, and JMdict 遂げる とげる begins “to
  accomplish; to achieve; to carry out” (entry 1372620)." Entry 1372620 is added to the Metadata ids (`踏.md:54`).
- 遂 now excludes 執 施 履 (`遂.md:14`; "These twelve cards" at `遂.md:46`). `遂.md:54`: "each title includes “carry out”, which is
  in JMdict's first sense of 遂げる, “to accomplish; to achieve; to carry out” (entry 1372620)." The 踏/遂 pair is declared on 踏 only.
- 執, 施 and 履 already exclude one another (執: 履; 施: 執 履), so no existing card changed. `checks\quiz-safety.txt` shows that the
  curated distractors of 踏 (握 掘 拾) and 遂 (既 更 必) still fill every wrong meaning slot; none of them is newly excluded.

### G2: missing 載/運 exclusion

Author action: **changed** as you proposed. 運 (“carry; luck”) is excluded on 載 (`載.md:14`; "These twelve cards" at `載.md:45`)
and joins the existing 積/荷 bullet (`載.md:50`), whose evidence already documents the carrying sense: Kanjipedia's first sense of
載 includes 車や船に積む。, JMdict 積載 “loading; carrying” (entry 1383040), and JMdict entry 1600270 sense 3 “to load (luggage); to
carry; to take on board”. No transitive pairs were added; in particular 載 is not excluded against 執, 施 or 履, whose shared
“carry out” is a different sense (performing an action, not transporting a load).

## Optional

- **GO1 (shorter Notes; translate quotations; gloss "ateji"): not changed.** The exclusion list with one sourced reason per
  excluded card, and the paragraph naming each distractor, is the Notes format used across the existing N1 cards, and
  `quiz_safety.py` checks that each distractor is named in Notes; shortening them in one batch would make it inconsistent with the
  rest. "ateji" appears in many existing cards, often without a gloss (for example `供.md:22`); a glossary-level change belongs to
  a separate pass over all of them, not to this batch.
- **GO2 (迫's distractor sentence): not changed.** The sentence (now `迫.md:52`) reads "Going out moves away rather than drawing
  near, entering goes inside rather than closing in, and resting is the opposite of pressing hard; none of them means to press or
  approach." As you note, 出 is not a valid answer for 迫 either way; the sentence contrasts the typical motion of each word, and
  "none of them means to press or approach" carries the conclusion.

## Limits

- **L1 (links to `../articles/compound-sound-changes.md` on 載, 輩 and 遣): verified, no change needed.** The article is tracked in
  the repository at the reviewed snapshot and at this revision with the same blob (`6d5e1f06fba93f5db9b3a518fd21ec854abe5f11`); it is
  also linked from the existing cards 井, 傑 and 貢. The links are at `載.md:42`, `輩.md:31` and `遣.md:38`. This packet includes the
  article unchanged as `evidence\compound-sound-changes.md`. The repository is public, and the published copy is at
  https://github.com/stop-cran/learning-japanese/blob/main/articles/compound-sound-changes.md (raw:
  https://raw.githubusercontent.com/stop-cran/learning-japanese/main/articles/compound-sound-changes.md).

## Other changes in this revision (from the other review)

These were not raised by you; they are listed so that every hunk is accounted for. New exclusions with sourced bullets: 押 on 迫
(JMdict 押す sense 5 “to push (someone for something); to press; to put pressure on (someone)”, entry 1180470; `迫.md:14,50,54`), 脱
on 避 (Kanjipedia のがれる for 避, KANJIDIC2 脱 “escape from”, JMdict 脱税 “tax evasion”, entry 1416550; `避.md:14,52,56`), 艶 and
華 on 輝 (JMdict 艶 つや “gloss; luster; lustre; shine; sheen; polish”, entry 1177680; KANJIDIC2 “shine” and “luster” for 華;
`輝.md:14,49,50,54`), and 弾 on 跳 (JMdict 弾む “to spring; to bound; to bounce”, entry 1419400; `跳.md:14,50,56`). 遣's -つか.い
example row now gives 蛇遣い へびつかい “snake charmer” (JMdict 1753470, also spelled 蛇使い) instead of 人形遣い, whose
priority-tagged reading is the voiced にんぎょうづかい (`遣.md:33,63`).
