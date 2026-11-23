# Author's statement for the reviewer of `reports-150\initial-claude.md`

This statement answers only the points in YOUR initial report: finding C1 and optional items O1 to O12. The statement is the
author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the
`checks\` outputs and independent sources; do not rely on this text as evidence. Card line numbers refer to the revised cards in this packet. Ten of the 15 new cards changed (蒔 薦 虚 融 街 衝 裁 裸 視 覧); 葬 蓄 衆 裂 覆, every existing kanji card, every stroke file and every word article are unchanged. Six `quiz_exclusions` lists changed (蒔 裁 視 覧 lost an entry; 街 and 衝 gained one); no title, tag, metadata reading, `quizOnyomi`, `quizKunyomi` or `distractors` list changed. See `CHANGES.md`. Give a disposition for C1 and for
each of O1 to O12.

## Finding

### C1: provenance label of the extra readings in the reading audit

Author action: **changed**, in the audit tooling rather than in the cards. `reading_exposure.py` and `reading_options.py` (workspace
audit scripts, not repository files) now label every reading passed with `--extra` as "--extra list" instead of "card text", and
their docstrings say what that list contains. The regenerated `checks\reading-exposure.txt` and `checks\reading-options.txt` carry
the new label; the header of `checks\reading-exposure.txt` records the command and the source of each extra reading (the KANJIDIC2
and source-only readings of the cards and the JMdict okurigana parses in the original packet's `evidence\okurigana-scan.txt`). The
counts and collision accounting are unchanged by the relabelling.

## Optional

- **O1 (虚 quotation): applied.** `虚.md:23` now attributes each wording to its source: "(Kanjipedia: 邪心をもたない; Digital
  Daijisen: 邪心を持たない)". Kanjipedia's sense ③ is 邪心をもたない。すなお。「謙虚」 and the Daijisen extract's 〈キョ〉 sense 6 is
  邪心を持たない。「虚心／謙虚」.
- **O2 (薦 quotation and punctuation): applied.** `薦.md:47`: "JMdict's entry for 推薦 has a see-also cross-reference to 推奨"; the
  bracketed cross-reference is no longer inside gloss quotes. `薦.md:49`: Kanjipedia's second sense is given in its own punctuation,
  こも。敷物。しとね。, glossed "(straw mat; floor covering; a mat to sit or lie on)".
- **O3 (街/径): applied.** 径 (“diameter; path”) is excluded (`街.md:14`), and the みち bullet now names all four JMdict spellings,
  道, 途, 路 and 径 (`街.md:48`, JMdict 1454080). The count reads "These eight cards" (`街.md:45`).
- **O4 (衝/攻): applied.** 攻 (“attack; go on the offensive”) is excluded (`衝.md:14`) and joins the bullet that cites JMdict's
  衝く glosses “to hit” and “to attack” (`衝.md:48`). The count reads "These eleven cards" (`衝.md:44`).
- **O5 (覆/転): not changed.** 転's displayed title is “turn; roll”; it names neither covering nor overturning, and neither title
  answers for the other. 倒 is excluded on the strength of JMdict 覆る “to topple over”, which matches 倒's own title “topple;
  collapse”; 転's title has no such sense.
- **O6 (葬/墓): not changed**, for the reason you give: a grave is a place, not the act of burying or a funeral.
- **O7 to O9 (coverage): not changed.** The suggested words are good study material, but adding them would add new sourced claims
  to this revision; both initial reviews judged scoped coverage clean.
- **O10 (鬲 and 𠂉): applied, as shape descriptions only.** `融.md:25`: "the tall shape 鬲 (a flat stroke over a small box, which
  sits on a taller frame with a few strokes inside)", and the image now says "that tall boxy stack". `覧.md:25`: "the small shape 𠂉
  (a slanting stroke with a short horizontal stroke to its right) and one more horizontal stroke below it" (KanjiVG strokes 8 and 9
  are 𠂉; stroke 10 is a horizontal outside any group). No meaning is given for 鬲 or 𠂉: neither has a card, the pinned evidence
  has no KANJIDIC2 record for them, and a meaning would read as an etymological claim the mnemonics disclaim.
- **O11 (裸 image): applied.** `裸.md:25`: "Imagine a fruit whose clothing, its peel, has been stripped away until it stands bare."
- **O12 (okurigana parses): not changed.** `okurigana-scan.txt` is the mechanical output of the scan over JMdict, kept as evidence;
  the parses are passed to the audit only as extra readings to test. C1's relabelling and the audit header now say where they
  come from.

## Other changes in this revision (from the other review)

These were not raised by you; they are listed so that every hunk is accounted for. 苗 is removed from 蒔's exclusions and its bullet
deleted (`蒔.md:14,46`); 布 is removed from 裁's exclusions and its bullet deleted (`裁.md:14,45`); 捜 is removed from the exclusions
of 視 and 覧, and the remaining 仰 bullets are restated (`視.md:14,44,49`, `覧.md:14,43,50`).