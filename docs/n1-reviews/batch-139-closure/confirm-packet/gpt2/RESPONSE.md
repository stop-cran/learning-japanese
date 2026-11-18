# Author's statement for the reviewer of `reports-139\confirm-gpt.md`

This statement answers only the points in YOUR confirmation report. The statement is the author's claim about what
changed and why. Verify each claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent
sources; do not rely on this text as evidence. Card line numbers refer to the revised cards in this packet. One of the
15 cards changed (嬢), on one line, and the other fourteen did not (see `CHANGES.md`). Give a disposition for G2.

## Findings

### G2: the new attributed JMdict gloss of 嬢さん じょうさん omits its qualification (`嬢.md:47`)

Author action: **changed** (your first remedy).

- `嬢.md:47` now quotes 嬢さん じょうさん as `"(another's) daughter; young lady (esp. of respectable upbringing)."`; it
  quoted `"(another's) daughter; young lady."` Nothing else on the line changed (`diffs\changed-lines.txt`).
- The text is the two glosses of entry 2230740 as JMdict gives them, joined by a semicolon, the same way the line
  quotes the other entries. Support: `evidence\jmdict-cited-entries.xml`, entry 2230740.
- The quotation keeps "esp."; the card does not turn it into a restriction.
- 2230740 was already on the Metadata line (line 51), so that line is unchanged.

To verify: that the quoted text now matches entry 2230740, that the separate とうさん entry (2216510) is still quoted
as before, and that nothing else on the line changed.

## Other points in your report

No disposition is needed for these.

- **G1, Optional 1, Optional 2 and Optional 3.** Your report resolved G1 and Optional 3 and accepted the declines of
  Optional 1 and Optional 2. This revision changes no text those points concern.
- **Quiz audits.** No front matter changed. `checks\quiz-safety.txt` is byte-identical to the earlier confirmation
  packet's copy, and `checks\reading-exposure.txt` and `checks\reading-options.txt` are identical to it apart from line 1.
- **Android JVM tests and the Kotlin cross-check.** Not run for this revision either.

## Process notes

- The author also corrected two wording slips in the earlier `CHANGES.md`; see "Corrections to the earlier
  `CHANGES.md`" in this packet's `CHANGES.md`. Neither concerns card text.
- The checks in `checks\` were run on the committed revision.
