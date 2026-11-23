# Author's statement for the reviewer of `reports-156-hold\confirm-gpt.md`

This statement answers your confirmation report and states one item the author raised. Your report had no Findings. Its
Optional section has one point; here it is P1. Its Limits describe what you did not verify and need no answer. A1 is an item
the author raised after your report; it is the whole of this revision. The statement is the author's claim about what
changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the
`evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in
this packet. Give a disposition for P1 and A1.

## Optional points

### P1: a ん + /p/ example in the compound-sound-changes article

Author action: **not changed in this batch; recorded as a follow-up.**

- `articles/compound-sound-changes.md` is a shared article: the batch's 伐 card, the 亜熱帯 and 伐採 articles, the existing
  潜 card and the published 輩 card link it. The gap you describe is not a regression of this batch: the published 輩 card
  links the article in the same way for ぱい in 先輩.
- Adding an example after ん (for instance 先輩 せんぱい or 散歩 さんぽ) changes a shared article and every page that links it,
  so the author records it as a follow-up for a separate change.
- The article is unchanged in this revision (`diffs\changed-files.txt`).

To verify: that the article is unchanged, and judge whether the decline is acceptable.

## Author-raised item

### A1: six words named on the cards had no JMdict entry on their card's Metadata line

Author action: **changed.** See `CHANGES.md` for the table of ids and the reason.

- The rule: a card's Metadata line lists the JMdict entry of every word the card names. At the reviewed snapshot six named
  words lacked their entry: 乙種 (乙:42), 亜麻 (亜:40), 仁術 (仁:41), 仙骨 and 酒仙 (仙:40), 伯母さん (伯:33 and 38).
- The revision adds 1862630, 1149860, 1369740, 1387150, 1329130 and 2261500 to the Metadata lines of 乙, 亜, 仁, 仙 and 伯.
  No other text changed.
- `evidence\meta-scan-before.txt` lists the six gaps; `evidence\meta-scan-after.txt` lists none.

To verify: that each added id is the JMdict entry of the word the card names (`evidence\jmdict-cited-entries.xml`, and the
online JMdict if you wish); that the reading and meaning 伯 gives for 伯母さん agree with entry 2261500; that the patch changes
nothing else on those lines; and that the checks are as `CHANGES.md` describes.

## Process notes

- The checks in `checks\` and the evidence audits were run on the committed revision `a7cc61e2`.
