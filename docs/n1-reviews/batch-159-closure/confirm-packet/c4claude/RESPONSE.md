# Author's statement for the reviewer of the confirmation report on `54b00e0c`

This statement answers only the points in YOUR confirmation report on `54b00e0c` (the earlier confirmation report named in `INSTRUCTIONS.md`). You confirmed `54b00e0c` with no findings and three optional notes; O1–O3 are those notes in order.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and the `evidence\` files; do not rely on this text as evidence.

What changed (`CHANGES.md` lists every line): one line of `kanji\母.md`, three lines of the ledger and the regenerated `manifest.json`. Give a disposition for O1–O3, and judge the changes made for the other review as a reviewer of the revised text.

## O1: 叔母 on the 母 card gives only しゅくぼ

Author action: **applied**. `kanji\母.md:38` now reads “- [叔母](../words/叔母.md) おば, also しゅくぼ — aunt (a parent's younger sister)”, in the same order as `kanji\叔.md:34`. The link still points to the article that teaches しゅくぼ; the line now shows おば, the Joyo special reading and the reading JMdict tags (entry 1607100), first.

## O2: the two examples in 叔母 are annotated with しゅくぼ

Author action: **none**. The article exists to teach the reading しゅくぼ, so its examples are annotated with that reading; the second example also uses はくぼ, the JMdict reading restricted to 伯母 (entry 1607100). Line 20 says that the examples are original. The “Distinctive meaning” section (line 32) says that 叔母 is also read おば, that the Joyo table lists おば as its special reading, that JMdict tags おば and not しゅくぼ, and that not every printed 叔母 is pronounced しゅくぼ. A further note on how often each reading is used in speech would need a frequency source that the packet does not have, so the article keeps the statements it can source.

## O3: 叔父 in the 叔 card's Common words list has no “also しゅくふ”

Author action: **none**. The シュク Readings row (`kanji\叔.md:29`) gives 叔父 しゅくふ with its Digital Daijisen definition and JMdict entry, and the Notes (line 38) say “Read with シュク, 叔父 is しゅくふ and 叔母 is しゅくぼ”. The 叔母 Common words line names しゅくぼ because it links the article that teaches that reading; 叔父 has no article.

## Changes made for the other review

Please judge each change as a reviewer of the revised snapshot.

1. **Ledger lint statement** (line 948, in `0ba7df63`). Another review of `f85ff382` found that ledger line 948 still gave the lint warning count from before the 叔母 support was added: “Of the 37 warnings, 35 are on reused cards and words.”, while `checks\lint.txt` reports 42. `0ba7df63` changes the sentence to: “Of the 42 warnings, 40 are on reused cards and words. They report a missing N1 source-index entry, quiz reading list or Metadata line, or a missing Dictionary line or one that cites no JMdict entry id; B159 changes none of these fields, because it only adds or links one Common words line on each of those cards and does not change those word articles.” `CHANGES.md` lists the warnings by kind, and `evidence\reused-lint-diff.txt` shows what B159 changes in the 20 warned files.
2. **Ledger reading-options statement** (line 953, in `bad899ea`). The same reviewer, confirming `0ba7df63`, noted that line 953 named only the 呉 ぐ informational note, while `checks\reading-options.txt` also has one for 吉 き (line 74). The statement now names both and says that the fallback is never consulted on either prompt (`CHANGES.md`, “The new reading-options statement”).
