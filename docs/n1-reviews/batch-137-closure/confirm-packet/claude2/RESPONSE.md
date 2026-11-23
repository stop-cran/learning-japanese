# Author's statement for the reviewer of `reports-137\confirm-claude.md`

This statement answers only the points in YOUR confirmation report. Your report had no Findings and one Optional point,
P1. The statement is the author's claim about what changed and why. Verify each claim against the revised card text in
`snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line numbers
refer to the revised cards in this packet; other line numbers refer to the named file in this packet. Three of the 15
cards changed (丁 呂 唯), each in its Metadata line only, and the other twelve did not (see `CHANGES.md`). Give a
disposition for P1.

## Optional points

### P1: 丁's Metadata line does not list JMdict 2829360 (仕丁)

Author action: **changed.**

- `丁.md:71` is the Metadata line (your report cites it as line 76). It now lists 2829360 after 2622400 (丁幾), in the
  order in which the words are first named on the card; 仕丁 is first named in line 40.
- Why it was applied although you found no rule for it in `content-format.md` or the rubric: the author's writing brief
  for this batch, which is not in any packet, asks the Metadata line to list "every JMdict entry id for every word named
  on the card". The earlier revision broke that rule when it added 仕丁 to line 40.
- Support: `evidence\jmdict-cited-entries.xml`, entry 2829360 (仕丁; readings しちょう, じちょう, してい and つかえのよほろ).

To verify: that 2829360 is the entry for 仕丁 as line 40 uses it, and that nothing else on the line changed.

## Other limits in your report

No disposition is needed for these.

- **"Only in つかえのよほろ".** Unchanged: it still rests on the author's search of the pinned JMdict.
- **Unchanged cards not reread.** 唯 was one of the four cards unchanged in the earlier revision; this revision changes
  its Metadata line (below). 井, 傷 and 哀 remain unchanged since the reviewed snapshot.
- **Audits are not the app.** The JVM tests and the Kotlin reading-audit cross-check were not run for this revision
  either.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk.

- **呂 and 唯: ids that were already missing in the reviewed snapshot** (`呂.md:55`, `唯.md:54`). After applying P1 the
  author checked all 15 cards with a script (`evidence\meta_scan.py`; scope and limits in `CHANGES.md`). It found three
  more words without their entry, all already in `d3c7394d`:
  - 当て字 (`呂.md:27`): 1448890 is added after 2240210 (呂).
  - 唯々 and 諾々 (`唯.md:39`, which names them as the two halves of 唯々諾々 with the readings いい and だくだく): 2672330
    and 1623580 are added after 1538910 (唯でさえ).
  - At this revision the script finds no such word without its entry (`evidence\meta-scan.txt` line 2). Words that appear
    only inside a longer word, such as 唯物 in 唯物論, are listed separately in that file and were not added.

To verify: that each added id is the entry for the word as the card uses it, and that the order matches the cards'
first mention.

## Process notes

- `48332d32` is the third local version of this fix commit. The first two, `0c7f25fe` (丁 only) and `fa9be05c` (丁 and
  呂), were replaced before this packet was built; neither was reviewed or published.
