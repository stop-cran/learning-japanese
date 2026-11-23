# Author's statement for the reviewer of `reports-150\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 and G2 are your report's own Findings labels; your Optional
section has three bullets, called GO1 (shorten repeated qualifications and mnemonic disclaimers), GO2 (explain "Joyo" and
"transitive" locally) and GO3 (a 虚偽 example) below. The statement is the author's claim about what changed and why. Verify each
claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and independent sources; do not rely on
this text as evidence. Card line numbers refer to the revised cards in this packet. Ten of the 15 new cards changed (蒔 薦 虚 融 街 衝 裁 裸 視 覧); 葬 蓄 衆 裂 覆, every existing kanji card, every stroke file and every word article are unchanged. Six `quiz_exclusions` lists changed (蒔 裁 視 覧 lost an entry; 街 and 衝 gained one); no title, tag, metadata reading, `quizOnyomi`, `quizKunyomi` or `distractors` list changed. See `CHANGES.md`. Give a disposition for each of G1, G2 and GO1 to GO3.

## Findings

### G1: 蒔/苗 and 裁/布

Author action: **changed** as you proposed. 苗 is removed from 蒔's exclusions (`蒔.md:14`) and its bullet, which equated seedlings
with seeds, is deleted; the count reads "These four cards" (`蒔.md:46`). The separately sourced replanting sense (う.える) is
untouched. 布 is removed from 裁's exclusions (`裁.md:14`) and its bullet is deleted; the count reads "These eight cards"
(`裁.md:45`). No replacement contrast was added. `checks\quiz-safety.txt` was rerun: both cards' three curated distractors still
fill every wrong meaning slot.

### G2: 捜 on 視 and 覧

Author action: **changed** as you proposed. 捜 is removed from the exclusions of 視 (`視.md:14`) and 覧 (`覧.md:14`), and from the
bullet it shared with 仰. The counts read "These nine cards" (`視.md:44`) and "These eleven cards" (`覧.md:43`). The 仰 bullets keep
仰 but restate the reason without relying on the shared word "look": `視.md:49` "to look up at something is itself to look at it, so
its “look up” overlaps the title's “look at.”"; `覧.md:50` "looking up at something and looking over something are both ways of
looking at it, so its “look up” overlaps the title's “look over.”"

## Optional

- **GO1 (shorter qualifications and disclaimers): not changed.** "Not selected for questions here" and the mnemonic disclaimer are
  the wording used on the existing N1 cards; shortening them in one batch would make it inconsistent with the rest.
- **GO2 (explain Joyo and transitive locally): not changed**, for the same consistency reason; the Usage line links the official
  Joyo table.
- **GO3 (虚偽): not changed.** It would add a new sourced claim to this revision; scoped coverage was judged clean.

## Other changes in this revision (from the other review)

These were not raised by you; they are listed so that every hunk is accounted for. 街 gains 径 (`街.md:14,45,48`); 衝 gains 攻
(`衝.md:14,44,48`); 虚's 邪心 quotation names each source's exact wording (`虚.md:23`); 薦's JMdict cross-reference and Kanjipedia
mat sense are restated (`薦.md:47,49`); the 融 and 覧 mnemonics describe the shapes 鬲 and 𠂉 (`融.md:25`, `覧.md:25`); the 裸 image is
simplified (`裸.md:25`). The reading audits label extra readings "--extra list" instead of "card text".
