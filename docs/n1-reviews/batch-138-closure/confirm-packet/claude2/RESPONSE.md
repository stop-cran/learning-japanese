# Author's statement for the reviewer of `reports-138\confirm-claude.md`

This statement answers only the points in YOUR confirmation report. Your report had no Findings and one Optional point,
which had no label; here it is P1. The statement is the author's claim about what changed and why. Verify each claim
against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text
as evidence. Card line numbers refer to the revised cards in this packet; other line numbers refer to the named file in
this packet. One of the 15 cards changed (契), on one line, and the other fourteen did not (see `CHANGES.md`). Give a
disposition for P1 and for A1, the corrected reading audits, which change one figure your report quoted.

## Optional points

### P1: 契闊 is written in katakana (`契.md:43`)

Author action: **changed.**

- `契.md:43` now reads `as in 契闊 けっかつ, not seeing someone for a long time`; it read `as in 契闊 ケッカツ, ...`.
  Nothing else on the line changed (`diffs\changed-lines.txt`).
- The card's other word readings are in hiragana (けいやく, ちぎる, きったん, and the Daijisen examples on lines 27-30).
  In the batch, the only other katakana word reading is 墨西哥 メキシコ (`墨.md:36`), a foreign place name.
- Kanjipedia prints the word as 契闊(ケッカツ) (`evidence\kanjipedia-契.txt`). The card writes the reading in hiragana and
  keeps the link to that page.
- 契闊 has no JMdict entry, so the Metadata line is unchanged.

To verify: that the reading itself is unchanged apart from the script, and that nothing else on the line changed.

## Corrections by the author

### A1: the reading audits in the earlier packets left out some extra readings

Author action: **corrected audits supplied; no card change.** This bears on your "Quiz options" section and on your
first limit. RESOLVED here means the corrected audits are as stated and your verdicts still hold.

- Your report quoted `reading-exposure.txt`: 0 production hits, 0 padded-session hits, 8 latent collisions. That audit
  and `reading-options.txt`, in the original packet and in both earlier confirmation packets, left out some extra
  readings for 垂, 執, 壊, 奏 and 奪, because of a defect in the author's audit tools. `evidence\extras-merge-fix.txt`
  describes the defect, the fix and the readings that were left out.
- The corrected audits (`checks\reading-exposure.txt`, `checks\reading-options.txt`) find one more latent collision:
  壊 やぶれる, offered by 敗 and 破 under the prompt 壊 こわ.す (`reading-exposure.txt` lines 148-154). It cannot be
  drawn in the N1 stack, All stack or Starter practice session, nor with any single borrowed holder. The summary is
  now 0 production hits, 0 padded-session hits and 9 latent collisions (line 261), with 0 one-holder padded hits
  (line 262). `reading-options.txt` still reports the same two HIT labels, 噴 ほん and 契 けつ (lines 17 and 160), and
  gains a note for 壊 (line 132).
- Your first limit (a custom pool without the target's curated distractor cards) also covers this case: in such a pool
  やぶれる could be offered as a wrong option for 壊 こわす (risk class at `reading-exposure.txt` line 153). The author
  treats it, like the other eight, as a latent risk under O9, not a defect in this batch.
- The same corrected command at the reviewed snapshot `b6020f9e` gives the same outputs apart from line 1
  (`evidence\reading-exposure-b6020f9e.txt`, `evidence\reading-options-b6020f9e.txt`).

To verify: that line 1 of each corrected output passes the readings listed in `evidence\extras-merge-fix.txt` section 3,
and that the new case is as described.

## Other limits in your report

No disposition is needed for these.

- **`evidence\Words.kt` not opened.** `evidence\extras-merge-fix.txt` section 3 relies on the audit tools excluding
  the same sound-change variants as `ReadingOptions.mutations`. `evidence\Words.kt` is in this packet again if you want
  to check that.
- **Android JVM tests and the Kotlin cross-check.** Not run for this revision either.
- **Body of `fix.patch`.** This revision's patch has one hunk, in `kanji/契.md` (`manifest.json` is left out of it).
- **Stroke summaries.** No stroke file changed.

## Process notes

- `3158b2b9` is the second local version of this fix commit. The first, `a93ce9c0`, made the same change to the card
  and was replaced only to correct its commit message; it was not reviewed or published.
- The audit tool fix changed no card or other repository file; it is outside the repository.
- The checks in `checks\` were run on the committed revision.
