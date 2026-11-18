# Author's statement for the reviewer of `reports-139\confirm-claude.md`

This statement answers only the points in YOUR confirmation report. Your report had no Findings and one Optional point,
which had no label; here it is P1. Your follow-up check of the earlier `CHANGES.md` noted two wording inaccuracies;
here they are W1 and W2. The statement is the author's claim about what changed and why. Verify each claim against the
revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet. One of the 15 cards changed (嬢), on one line,
and the other fourteen did not (see `CHANGES.md`). Give a disposition for P1, W1 and W2.

## Optional points

### P1: the second gloss of 嬢さん じょうさん is truncated (`嬢.md:47`)

Author action: **changed.**

- `嬢.md:47` now quotes 嬢さん じょうさん as `"(another's) daughter; young lady (esp. of respectable upbringing)."`; it
  quoted `"(another's) daughter; young lady."` Nothing else on the line changed (`diffs\changed-lines.txt`).
- The text is the two glosses of entry 2230740 as JMdict gives them, joined by a semicolon, the same way the line
  quotes the other entries. Support: `evidence\jmdict-cited-entries.xml`, entry 2230740.
- 2230740 was already on the Metadata line (line 51), so that line is unchanged.

To verify: that the quoted text now matches entry 2230740 and that nothing else on the line changed.

## Corrections to the earlier `CHANGES.md`

### W1: "moves before" on the 嬢 and 峠 Metadata lines

Author action: **corrected in this packet's `CHANGES.md`.** Entries 1531190 (嬢) and 1896840 (峠) stayed at the end of
the old list, and the new entries were appended after them, as your check of `fix.patch` found.

### W2: "this revision changes only the colon" in the 宴会 row

Author action: **corrected in this packet's `CHANGES.md`.** The colon became a full stop and "The on readings are" was
added, as your check found.

To verify: that the "Corrections to the earlier `CHANGES.md`" section of this packet's `CHANGES.md` states both
corrections accurately.

## Other limits in your report

No disposition is needed for these.

- **Quiz audits.** No front matter changed. `checks\quiz-safety.txt` is byte-identical to the earlier confirmation
  packet's copy, and `checks\reading-exposure.txt` and `checks\reading-options.txt` are identical to it apart from line 1.
- **Android JVM tests and the Kotlin cross-check.** Not run for this revision either.
- **Stroke files and word articles.** None changed in this revision; `diffs\fix.patch` is the complete patch apart from
  `manifest.json`.
- **meta-scan.** `evidence\meta-scan.txt` is identical to the earlier confirmation packet's copy apart from line 1.

## Process notes

- The checks in `checks\` were run on the committed revision.
