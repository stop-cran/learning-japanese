# Author's statement for the reviewer of `reports-149\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 to G4 are your report's own Findings labels; your Optional
section has four bullets, called GO1 (rotate the grass-crown distractors), GO2 (simplify the Notes of 舎, 荘 and 華), GO3 (舌,
"physical tongue") and GO4 (the pool boundary of the latent reading forms) below. The statement is the author's claim about what
changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely
on this text as evidence. Card line numbers refer to the revised cards in this packet. All 15 cards changed, two word articles
changed by declared remark edits, six `distractors` lists (舎 芝 芽 茂 荘 華) and three `quiz_exclusions` lists (腐 興 茂) changed;
see `CHANGES.md`. Give a disposition for each of G1 to G4 and GO1 to GO4.

## Findings

### G1: stale "no separate 艶 card" sentence

Author action: **changed** as you proposed. The sentence is deleted from `words\艶.md` (it was old line 31) as a declared remark
edit; `evidence\word-remarks.json` lists the exact old and new text, and `checks\linkplan.txt` verifies the word articles against
it.

### G2: the small っ in 別荘

Author action: **changed**. `荘.md:23`: the reading is ソウ for 荘, and the ツ of 別 (ベツ) becomes a small っ before it: べっそう.

### G3: 興/復, 茂/密, 茂/盛

Author action: **changed** as you proposed, one declaration per pair. 復 is added to 興's exclusions (`興.md:14`), with KANJIDIC2's
“revive” for 興 named in `興.md:52`. 密 and 盛 are added to 茂's exclusions (`茂.md:14`), with the JMdict 茂る glosses and the
KANJIDIC2 “grow thick” and “be luxuriant” in a new Notes bullet (`茂.md:43`). The same bullet also names 豊, which is excluded
for the luxuriant sense.

### G4: dense 臨 and 艶 Notes

Author action: **changed**. `臨.md:41-43` and `艶.md:52-55` give the reading and name qualifications as short bullets; each card
then has an intro line and short bullets for the same exclusions, one reason per group (`臨.md:45-51`, thirteen cards;
`艶.md:57-64`, twelve cards). The exclusions are unchanged. Their evidence stays on the cards rather than moving to maintainer
evidence, because the corpus documents each exclusion in the card Notes.

## Optional

- **GO1 (rotate distractors): applied.** New Starter sets: 芝 田 木 花, 芽 木 土 雨, 茂 山 川 土, 荘 校 駅 海, 華 月 天 川 and 舎
  道 京 雨 (line 13 of each card and its distractor sentence). 犬 no longer appears; no two of these cards share a set.
- **GO2 (simplify 舎, 荘, 華): applied.** The same intro-and-bullets form is used on 舎 (`舎.md:52-58`), 荘 (`荘.md:46-52`) and
  華 (`華.md:48-56`), and also on 翻 (`翻.md:44-49`).
- **GO3 (舌, "physical tongue"): applied in a different form.** `舌.md:49` now reads "none of these titles names the tongue,
  speech, or language", which makes the displayed-title context explicit instead of narrowing the contrast to the physical tongue.
- **GO4 (pool boundary of latent forms): noted.** `checks\reading-exposure.txt` keeps the boundary: production hits, padded-session
  hits and latent collisions are counted separately.

## Process notes

- `b007a0a6` and `06b2db87` are the two fix commits; `diffs\fix.patch` is the whole change from the reviewed snapshot `070b6f69`.
  `06b2db87` changes only 荘's distractor 京 to 駅 (see `CHANGES.md`).
- The checks in `checks\` were run on the committed revision `06b2db87`.
- The commit also follows the Claude reviewer's findings (not shown to you): the reading-row label convention, 豆腐, 艶やか
  つややか, the 翼 wording, the exclusions 腐/甘, 腐/傷 and 茂/豊, and several added common words. See `CHANGES.md` for all changed
  lines.
