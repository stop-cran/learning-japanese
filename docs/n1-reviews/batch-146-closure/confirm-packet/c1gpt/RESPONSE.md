# Author's statement for the reviewer of `reports-146\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 to G3 are your report's own Findings labels; your
Optional section has three bullets, called O-A (shorten audit explanations and the exclusion inventories in learner
text), O-B ("not quizzed here" instead of "source-only here" for 甚 ジン and 癖 ヘキ) and O-C (clearer wording for the 潔
link to 癖 and for the 熟 "other examples") below. The statement is the author's claim about what changed and why.
Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on
this text as evidence. Card line numbers refer to the revised cards in this packet. Nine cards (煮 熟 牧 玄 甚 癖 益 盛
睡) changed, and one front-matter list changed (牧 `quiz_exclusions`); see `CHANGES.md`. Give a disposition for each of
G1 to G3 and O-A to O-C.

## Findings

### G1: 甚 okurigana of 甚だしい

Author action: **changed** as you proposed. `甚.md:37` now says 甚 writes はなは and だしい is okurigana, and likewise
for the adverb 甚だ (はなは + だ); it says KANJIDIC2 lists はなは.だ and the longer はなは.だしい. `甚.md:34`, `35` and `41` say that 甚だしい (linked on the はなは.だ row) shares the stem はなは with
はなは.だしい, so that row is not selected separately.

### G2: 癖 sound statements

Author action: **changed** as you proposed. `癖.md:37`: くせ "often becomes ぐせ" (口癖, 酒癖); 手癖 is てくせ or てぐせ;
難癖 keeps くせ; in 潔癖 ヘキ becomes ペキ after the small っ, with no "voiced" wording. The 潔 cross-reference now reads
"the 潔 card links back here for it".

### G3: 牧 exclusions 牛, 馬, 羊

Author action: **partly changed; the three pairs you named are kept.**

- Changed: the five exclusions that rested on a sense not in the displayed title (治 御 官 司 導) were removed from
  `quiz_exclusions` (`牧.md:14`; 12 kanji remain, was 17), and `牧.md:54` explains the new list and says why the five
  are not excluded.
- Kept: 牛 馬 羊 (and 畜 養 育 農 草 野). The title says "raise livestock", and the pairs are livestock animals and
  farm words; `牧.md:53` now states this as a livestock overlap. The author judged them close enough in a quiz that a
  learner could defend "cattle, cow" for "livestock", and exclusions only remove options. You may judge the displayed
  "raise livestock" against "cattle, cow", "horse" and "sheep" differently; give your view of whether keeping these
  three is a defect or only an over-cautious choice.

## Optional

- **O-A (shorten audit explanations): partly applied.** The "repo's aligner/alignment" sentences were removed from 煮
  (`煮.md:36`), 甚 (`甚.md:37`, `41`), 盛 (`盛.md:39`) and 睡 (`睡.md:37`). The exclusion inventories were not moved out
  of the Notes.
- **O-B ("not quizzed here" instead of "source-only"): applied differently.** `甚.md:33` and `癖.md:33` now give the
  Type cell as plain `on` (these are official Joyo readings), keeping "no word article yet, not selected for questions
  here".
- **O-C (潔/癖 and 熟 wording): applied.** `癖.md:37` says the 潔 card links back here; `熟.md:51` speaks of "the examples
  without word articles" for 熟練 and 熟慮.

## Process notes

- `5e61ef07` and `872d6502` are the two fix commits; `diffs\fix.patch` is the whole change from the reviewed snapshot `38833c7f`.
- `872d6502` follows a Claude confirmation of `5e61ef07`. It changes only 甚 (lines 34, 35, 41: 甚だしい and the shared stem はなは), 牧
  (line 54: the exclusion count wording) and 盛 (line 37: a duplicated "thriving" gloss). Please check those lines too.
- The checks in `checks\` were run on the committed revision.
