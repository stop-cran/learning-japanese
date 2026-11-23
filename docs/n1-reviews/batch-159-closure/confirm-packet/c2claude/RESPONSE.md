# Author's statement for the reviewer of the confirmation report on `5c04be73`

This statement answers only the points in YOUR confirmation report on `5c04be73` (the earlier confirmation report named in `INSTRUCTIONS.md`). You confirmed `5c04be73` with no findings. O1-O3 are your three Optional notes in order: 太后 wording; the 吟 exclusions; `support_spelling`.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet.

What changed, in brief (`CHANGES.md` lists every line): one front-matter line and one Notes line of `kanji\吟.md`, one body line each of `words\太后.md` and `words\吟味.md`, five ledger lines, and the regenerated `manifest.json`. Give a disposition for O1-O3, and judge the other reviews' changes described below.

## Optional notes

### O1: 太后 wording read as two different people

Author action: **changed**. `words\太后.md:15` now reads: “In plain terms, Digital Daijisen describes 太皇太后 as the empress of the emperor two reigns back and 皇太后 as the empress of the previous emperor; in a narrower sense, 皇太后 is such an empress who is also the current emperor's birth mother.” Sources: Digital Daijisen 皇太后「前天皇の皇后。また、前天皇の皇后で、現天皇の生母。」 and 太皇太后「先々代の天皇の皇后。」 (`evidence\daijisen-kotobank.json`). The wording follows your suggestion, with “in a narrower sense” in place of “especially”, because Daijisen gives the second clause as an alternative definition (また), not as a typical case.

### O2: the 吟 exclusions are over-exclusion at the level of the titles

Author action: **one exclusion added; none removed.** Another review asked to exclude 験 (“test; verify”) as well, because Digital Daijisen's first sense of 験, 証拠によって確かめる, overlaps 吟's taught sense 内容を探り確かめる. `kanji\吟.md:14` now adds 験, and line 42 names it with its title. As you note, the curated meaning distractors 二 自 社 never use these cards; the exclusions act only in fallback or custom pools (`evidence\QuizBuilder.kt` lines 26–34).

### O3: `support_spelling` checks only that the spelling appears in the article text

Author action: **none.** As you note, the other conditions still hold, and no other support check is loosened.

## Changes made for the other reviews

Please judge each change as a reviewer of the revised text, not only as an answer to your own notes.

1. **吟 / 験.** This is the change described under O2.
2. **吟味** (`words\吟味.md:24`).
   - One review noted that “savoring its flavor” was attributed to both sources, while only Daijisen says 味わう.
   - The last sentence now reads: “Both sources mark poetry recitation as the original meaning of 吟味: Digital Daijisen sense 3 is reciting a poem and savoring its flavor, and JMdict sense 4 (archaic) is “reciting and appreciating traditional poetry”.”
   - Sources: Daijisen 吟味 《3が原義》 and JMdict 1243390 sense 4, [arch], s_inf “orig. meaning”.
3. **叔's reason** (ledger lines 29, 78 and 952).
   - One review held that, under the letter of point 2 of the issue #60 rule (`evidence\rule-7058679348.md`), the tagged spellings 叔父 and 叔母 (ichi1/news1) are candidates through their unflagged シュク readings しゅくふ and しゅくぼ. So the earlier statement that no candidate qualifies was wrong.
   - The ledger now describes the 伯叔 row as an author's exception to point 2's preference, reported to the owner for a decision. The reasons are unchanged:
     - the tags in those entries also sit on the whole-word readings おじ and おば;
     - an article headed 叔父 or 叔母 would teach おじ or おば;
     - B156 applied the same interpretation to 伯 (`evidence\b156-selection.json`).
   - The ledger names the fallback, if the owner prefers the letter of the rule: an article headed 叔父 whose reading is しゅくふ.
   - `CHANGES.md` quotes line 78 in full. The batch content (`words\伯叔.md`, `kanji\叔.md`) is unchanged.
4. **Reading-option statements** (ledger line 947, and a correction in `CHANGES.md`).
   - The earlier ledger and one earlier RESPONSE said that the curated distractors fill all three wrong options of every reading question, or of every shipped pool for 吟. That holds for meaning questions.
   - For 吟's ギン prompt, it does not: 二 and 自 both show ジ in one of four outcomes, and the fallback fills the open slot (`checks\reading-exposure.txt` lines 138–150; `evidence\KanjiReadings.kt` lines 100 and 110–111, new in this packet).
   - The audit finds no exposure hit, and the card is unchanged.
