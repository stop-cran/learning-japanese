# Author's statement for the reviewer of `reports-146\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 to C9 are your report's own Findings labels; your
Optional section has nine bullets, called O1 to O9 below in the order of the report (O1 implementation jargon, O2 kana in
Notes, O3 玄孫, O4 狭霧, O5 reading-exposure labels, O6 環/鳴, O7 眺/相, O8 癖 exclusions, O9 眺める diff). The statement
is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`,
`diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line numbers refer to the revised
cards in this packet. Nine cards (煮 熟 牧 玄 甚 癖 益 盛 睡) changed, and one front-matter list changed (牧
`quiz_exclusions`); see `CHANGES.md`. Give a disposition for each of C1 to C9 and O1 to O9.

## Findings

### C1: 甚 okurigana of 甚だしい

Author action: **changed** as you proposed. `甚.md:37` now says 甚 writes はなは and だしい is okurigana, and the same
for the adverb 甚だ (はなは + だ); KANJIDIC2 lists はなは.だ and はなは.だしい. `甚.md:35` (the はなは.だしい row) says the
same, and the aligner wording on `甚.md:41` is gone.

### C2: ジン and ヘキ labelled "source-only here"

Author action: **changed** as you proposed. `甚.md:33` and `癖.md:33` now give the Type cell as plain `on`; "no word
article yet, not selected for questions here" is kept.

### C3: 益体 as whole-word reading

Author action: **changed** as you proposed. `益.md:43`: 益体 やくたい is 益 ヤク + 体 タイ; only 益荒男 ますらお is a
whole-word reading.

### C4: 煮凝り as whole-word reading

Author action: **changed** as you proposed. `煮.md:39`: 煮凝り is 煮 に + 凝り こごり; only 煮麺 にゅうめん is called a
whole-word reading.

### C5: 熟 "linked words"

Author action: **changed**. `熟.md:51` now names the one linked word 熟語 (other kanji 語, ゴ) and, separately, "the
examples without word articles": 練 (レン) in 熟練 and 慮 (リョ) in 熟慮, the latter with no card here. 語 and 練 were
not given new links in this sentence beyond what the line already had; verify whether that is acceptable.

### C6: 玄 "cap stroke"

Author action: **changed** as you proposed. `玄.md:34` says a two-stroke lid.

### C7: 癖 sound statements and the 潔 cross-reference

Author action: **changed**. `癖.md:37`: くせ "often becomes ぐせ" (口癖, 酒癖); 手癖 can be てくせ or てぐせ; 難癖 keeps くせ;
in 潔癖 ヘキ becomes ペキ after the small っ; "the 潔 card links back here for it".

### C8: 牧 title "pastor" and exclusions

Author action: **partly changed**.

- Changed: kana added for 牧童 ぼくどう and 牧羊 ぼくよう (`牧.md:53`). The five exclusions that rested only on a sense
  the title does not show (治 御 官 司 導) were removed from `quiz_exclusions` (`牧.md:14`, 12 kanji remain) and
  `牧.md:54` says why they are not excluded. The aligner jargon is not in this card.
- Not changed: the title keeps "pastor". 牧師 is the Joyo example and Daijisen's second sense for 牧 is shepherding
  people, so 僧 坊 師 ("Buddhist monk; priest", "Buddhist priest; boy", "teacher; specialist") overlap the displayed
  word and stay excluded. Verify whether keeping the title is defensible.

### C9: 盛ん filed under さか.る

Author action: **changed** as you proposed. `盛.md:36-37`: 盛り stays on the さか.る row; 盛ん is linked on the さか.ん
row, which says it shares the stem さか with さか.る and is not selected separately. `盛.md:39` no longer explains this
with the aligner, and `盛.md:43` says さか.ん has the same stem さか as さか.る.

## Optional

- **O1 (implementation jargon): applied** in 煮 (`煮.md:36`), 甚 (`甚.md:37`, `41`), 盛 (`盛.md:39`) and 睡
  (`睡.md:37`).
- **O2 (kana for words in Notes of 狭, 狂, 癖, 牧): partly applied.** 牧童 and 牧羊 now have kana (`牧.md:53`). 狭, 狂
  and 癖 are not changed: those words are listed as further examples with their meanings in the Notes.
- **O3 (玄孫 やしゃご): not applied.** An optional extra reading of one example.
- **O4 (狭霧 wording): not applied.** The line is accurate as written.
- **O5 (reading-exposure label "card text"): not applied.** An audit-label nit with no effect on the counts.
- **O6 (環 / 鳴 "ring"): not applied.** Different senses; no realistic ambiguity; no exclusion added.
- **O7 (眺 / 相 "aspect"): not applied.** Unlikely to be chosen; the distractors are unchanged.
- **O8 (癖 exclusions 風 様 柄): not applied.** Exclusions only remove options.
- **O9 (眺める link style): not applied.** It matches the link-wrap rule.

## Process notes

- `5e61ef07` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `38833c7f`.
- The checks in `checks\` were run on the committed revision.
