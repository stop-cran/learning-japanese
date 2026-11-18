# Author's statement for the reviewer of `reports-138\confirm-gpt.md`

This statement answers only the points in YOUR confirmation report. Your report had no Findings and no new Optional
points, but three of its remarks bear on this revision; here they are A1 (your limit on the "stated ... extra-reading
list"), OR (your disposition of the original OR point, which counted eight latent cases) and L1 (your "line for line"
note). The statement is the author's claim about what changed and why. Verify each claim against the revised card text
in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line numbers
refer to the revised cards in this packet; other line numbers refer to the named file in this packet. One of the 15
cards changed (契), on one line, and the other fourteen did not (see `CHANGES.md`). Give a disposition for each of A1, OR
and L1.

## The change in this revision

This change answers no point in your report; please review it like any other changed hunk.

- `契.md:43` now writes the reading of 契闊 in hiragana, `as in 契闊 けっかつ, not seeing someone for a long time`; it
  read `ケッカツ`. The other reviewer suggested this as an optional point, for consistency with the card's other word
  readings (けいやく, ちぎる, きったん). Kanjipedia prints the word as 契闊(ケッカツ) (`evidence\kanjipedia-契.txt`).
  契闊 has no JMdict entry, so the Metadata line is unchanged.

To verify: that the reading itself is unchanged apart from the script, and that nothing else on the line changed.

## Corrections by the author

### A1: the reading audits in the earlier packets left out some extra readings

Author action: **corrected audits supplied; no card change.** RESOLVED here means the corrected audits are as stated
and your conclusions on the reading quiz still hold.

- Your limit says audit safety is bounded to the stated extra-reading list. The earlier audits did not apply the whole
  list: because of a defect in the author's audit tools, they left out some extra readings for 垂, 執, 壊, 奏 and 奪,
  and eight of those readings were not checked at all. `evidence\extras-merge-fix.txt` describes the defect, the fix
  and the readings that were left out.
- The corrected audits (`checks\reading-exposure.txt`, `checks\reading-options.txt`) find one more latent collision,
  壊 やぶれる, offered by 敗 and 破 under the prompt 壊 こわ.す (`reading-exposure.txt` lines 148-154). It cannot be
  drawn in the N1 stack, All stack or Starter practice session, nor with any single borrowed holder. The summary is
  now 0 production hits, 0 padded-session hits and 9 latent collisions (line 261), with 0 one-holder padded hits
  (line 262). `reading-options.txt` still reports the same two HIT labels, 噴 ほん and 契 けつ (lines 17 and 160).
- The same corrected command at the reviewed snapshot `b6020f9e` gives the same outputs apart from line 1
  (`evidence\reading-exposure-b6020f9e.txt`, `evidence\reading-options-b6020f9e.txt`).

To verify: that line 1 of each corrected output passes the readings listed in `evidence\extras-merge-fix.txt` section 3,
and that the new case is as described.

### OR: keeping the latent cases as reference material

Author action: **the corrected audit records nine cases.** Your earlier disposition (RESOLVED, for case retention)
counted eight. The corrected `checks\reading-exposure.txt` records all nine, including 壊 やぶれる (lines 152-154).

### L1: "line for line"

Author action: **corrected.** You noted that the meaning-audit output in the earlier confirmation packet had one blank
line fewer than the original packet's copy. `CHANGES.md` ("Corrections to the earlier `CHANGES.md`") corrects the
statement and names the cause: the packet builder dropped every blank line from the check outputs it summarizes. This
packet's `checks\quiz-safety.txt` is copied unchanged and is byte-identical to the original packet's
`evidence\audits\quiz-safety.txt`.

## Your other remarks

No disposition is needed for this.

- **"Card text" labels.** Agreed: the tools label every extra reading "(card text)", whatever its source.
  `evidence\extras-merge-fix.txt` section 1 says so; line 2 of each output names the sources.

## Process notes

- `3158b2b9` is the second local version of this fix commit. The first, `a93ce9c0`, made the same change to the card
  and was replaced only to correct its commit message; it was not reviewed or published.
- The audit tool fix changed no card or other repository file; it is outside the repository.
- The checks in `checks\` were run on the committed revision.
