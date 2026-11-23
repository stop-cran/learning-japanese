# Author's statement for the reviewer of `reports-142\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 to G4 are your report's own Findings labels, and
"Optional 1" to "Optional 3" are its three Optional bullets in order. The statement is the author's claim about what
changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch` and independent
sources; do not rely on this text as evidence. Card line numbers refer to the revised cards in this packet. Five of
the 15 new cards changed (描 提 揺 斉 斎), the other ten did not; no front matter or stroke file changed (see
`CHANGES.md`). Give a disposition for each of G1 to G4 and Optional 1 to 3.

## Findings

### G1 (minor): 提's チョウ row (`提.md:40,46`)

Author action: **changed** as you proposed.

- `提.md:40`: the claims that ちょうちん belongs to the whole word, that no source assigns ちょう to 提 alone and that 提灯
  is the only JMdict word are gone. The row now says that チョウ is listed in KANJIDIC2 and, as outside the official table,
  by Kanjipedia; that it is the reading of 提 in 提灯 ちょうちん, which Daijisen writes ▽提▽灯 and labels 唐音 (JMdict
  1446650 is quoted for 唐音); that JMdict also has compounds such as 提灯行列 and 提灯持ち; and that there is no word
  article yet and it is not selected for questions.
- `提.md:46`: `チョウ has no ordinary example of its own.` became `no word article has 提灯 yet.`
- `提.md:62` (Metadata) gained JMdict 1734790 (提灯行列), 1734800 (提灯持ち) and 1446650 (唐音).
- Support: `evidence\weblio-chouchin.txt` (the Daijisen headword `ちょう‐ちん【▽提▽灯】` and its 《唐音》 label),
  `evidence\jmdict-cited-entries.xml`, and the original packet's `evidence\kanjipedia-outside-readings.json`.
- To verify: that the rewritten row is correct and still teaches nothing the sources do not support, and that the 唐音
  quotation is JMdict's wording.

### G2 (minor): 斎's "not split between the kanji" claim (`斎.md:32`)

Author action: **changed** as you proposed.

- `斎.md:32` now ends `in 斎宮, 斎 is read いつき, the の is not written and 宮 is みや`; the blanket statement that these
  are readings of the whole word is gone. 斎王 いつきのみこ keeps its listing as a Daijisen word reading without a
  segmentation claim.
- Support: `evidence\weblio-saigu.txt` (Daijisen `いつき‐の‐みや【▽斎宮】`).
- To verify: that the new sentence is correct for 斎宮 and that no remaining sentence in the paragraph still claims
  non-segmentation.

### G3 (minor): 揺's 缶-shaped part (`揺.md:29,56` in your report)

Author action: **changed** as you proposed.

- The mnemonic is now `揺.md:31`: `a claw-like top over a shape like [缶](缶.md), "tin can; container," with one stroke
  fewer.` The first Notes bullet is now `揺.md:60`: `缶 has six strokes; the bottom of the right part of 揺 is a
  five-stroke shape like it.`
- Support: `evidence\stroke-types.txt` (KanjiVG stroke types of the repository stroke files: 揺's strokes 8 to 12 equal
  strokes 2 to 6 of 缶).
- To verify: the stroke-count claim against `snapshot\strokes\揺.json` and the repository's `缶.md`.

### G4 (minor): wall-of-text paragraphs in 斎, 斉 and 揺

Author action: **changed in part.**

- Done: the long single paragraphs were split into short paragraphs: 斎 `斎.md:32, 34, 36` (was one paragraph at line
  32), 斉 `斉.md:25, 27, 29` (was one paragraph at line 25), 揺 `揺.md:25, 27` and `揺.md:49, 51` (were lines 25 and 47).
  Wording of the split paragraphs is unchanged apart from the edits listed in `CHANGES.md`.
- Not done: the secondary source inventories and wrong-option assurances were not moved to bullets at the end of
  Notes. They stay where they are, at the end of their paragraphs, so that each paragraph still reads as one idea.
  Moving them would also mean re-checking the Notes cross-references of three cards without changing what a learner
  can practise.
- To verify: whether the split paragraphs are short enough for the phone audience, or whether the move you proposed is
  still needed.

## Optional

- **Optional 1 (描, JMdict 2751570): applied.** `描.md:52` (Metadata) now lists 2751570 (すがき, written 素描, "uncolored
  sketch; line sketch; rough sketch"), the entry quoted on `描.md:37`.
- **Optional 2 (favor useful compounds over repeated disclaimers): no card change.** It is guidance for future
  shortening; nothing in this revision removed or added disclaimers beyond the edits listed.
- **Optional 3 (conservative exclusions 挿/苗 and 敵/恨): not applied.** Your report did not ask for a change; both
  pairs stay declared.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **斎's さい【斎】 sentence (`斎.md:34`)** now reads `the pen names of writers and artists` instead of `names of
  studios and rooms`; it does not answer a point in your report.
- **A new JMdict citation, 唐音 (1446650), was needed on 提** after the G1 rewording (`evidence\meta-scan.txt` finds no
  word without its entry).

## Process notes

- `3a0399bd` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `9d393a8f`.
- The checks in `checks\` were run on the committed revision. No front matter changed, so the quiz and reading audits
  are identical to the freeze apart from their command lines.
