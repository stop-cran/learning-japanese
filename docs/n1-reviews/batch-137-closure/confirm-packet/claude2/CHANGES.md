# Batch 137 second revision: what changed from 2bc8e9b1 to 48332d32

Revised snapshot: `48332d3258953779dda24c0df6fb1c649e6defbb`, a child of the earlier revision
`2bc8e9b13ea85b39c533735f63643af44d1ce690`, which was the subject of the earlier confirmation round. That revision is a
child of the initially reviewed snapshot `d3c7394d38992b24d3689bc984fdb4a6cf60bc54`. Nothing is published.

- Three of the 15 kanji cards changed, each in its Metadata line only: 丁 (line 71), 呂 (line 55) and 唯 (line 54). The
  other twelve (井, 仰, 但, 傑, 傷, 僕, 卸, 司, 吐, 哀, 哲, 善) are unchanged, and so are all 15 stroke files, the front
  matter of every card and every word article. No teaching text changed.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot). No line was added or
  removed. The text at `2bc8e9b1` is in the earlier confirmation packet's `snapshot\kanji\`.
- `diffs\fix.patch` is the exact patch from `2bc8e9b1` to `48332d32`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. Earlier evidence
  stays in the earlier confirmation packet and the original packet.

| Card | Changed lines | Change |
| --- | --- | --- |
| 丁 | 71 | Metadata: JMdict entry 2829360 (仕丁, named in line 40 since the earlier revision) is added to the entry list, after 2622400 (丁幾). Support: `evidence\jmdict-cited-entries.xml`, entry 2829360. |
| 呂 | 55 | Metadata: entry 1448890 (当て字, named in line 27) is added, after 2240210 (呂). Support: `evidence\jmdict-cited-entries.xml`, entry 1448890 (当て字, あてじ). |
| 唯 | 54 | Metadata: entries 2672330 (唯々 いい) and 1623580 (諾々 だくだく) are added, after 1538910 (唯でさえ). Line 39 names both as the two halves of 唯々諾々, with these readings. Support: `evidence\jmdict-cited-entries.xml`, entries 2672330 (唯々, reading いい, "obedient; submissive; tame; slavish") and 1623580 (諾々, reading だくだく, the same gloss). |

Each id is placed in the order in which its word is first named on the card, as the existing ids are.

## How the 呂 and 唯 gaps were found

- The author's writing rule for these cards is that the Metadata line lists the JMdict entry of every word the card
  names. After applying your P1, the author ran a script over all 15 cards to look for other words without their entry:
  `evidence\meta_scan.py`, with its output at this revision in `evidence\meta-scan.txt`.
- The script checks every run of Japanese script (kanji, kana, 々, ー) outside the front matter, the Metadata line and
  link targets that has at least two characters, contains a kanji and exactly matches a JMdict kanji spelling. At
  `2bc8e9b1` it found 当て字 in 呂 line 27 and 唯々 and 諾々 in 唯 line 39, all three already in the reviewed snapshot
  `d3c7394d`. At `48332d32` it finds none (`meta-scan.txt` line 2).
- Limits: it does not check words written only in kana, single-kanji words, or words that appear only inside a longer
  word. It lists the last kind separately (24 at this revision, `meta-scan.txt` lines 4-27; for example 唯物 in 唯物論),
  and the author did not add their ids.

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on 17 kanji cards (the 15 new cards, 寧 and 敷) and 25 word articles: 0 errors, 4
  warnings, all on unchanged word articles whose Dictionary line cites no JMdict entry id (井戸, 但し, 吐き気, 風呂敷).
  Same as at `2bc8e9b1`. The linter checks only that each cited id exists in the pinned JMdict.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage pilot).
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either, so there is no `jvm.txt`.
- `link-targets.tsv`: every link to a card or word article on a changed line. It lists none: the three changed lines
  link only to external sources (KANJIDIC2, JMdict and Weblio), and those links did not change.
- `quiz-safety.txt`, `reading-options.txt` and `reading-exposure.txt`: no front matter changed, so the quiz options are
  unchanged. `quiz-safety.txt` is identical to the earlier confirmation packet's, and the other two differ from it only
  in line 1, the command line, which names this revision. That line no longer shows the interpreter as
  `python -X utf8 utf8`: the doubled `utf8` was a typo in the author's label, now corrected.

## Process notes

- `48332d32` is the third local version of this fix commit. The first two, `0c7f25fe` (丁 only) and `fa9be05c` (丁 and
  呂), were replaced before this packet was built; neither was reviewed or published.
