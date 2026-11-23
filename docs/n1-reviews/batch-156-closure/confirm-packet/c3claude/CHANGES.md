# Batch 156 third revision: what changed from 3c5ef845 to a7cc61e2

Revised snapshot: `a7cc61e27261c62e84c3bd1f28e8a9254d9dcb04`. Nothing is published.

- Your last confirmation report reviewed `3c5ef8450e38051682dab2bea5fce320b992e5ea`. After it, the author merged current main
  (`9766dbd5`) into the batch: merge `e37ad00b796ed16dc752f5e60f0fd119f14dfa5e`, whose first parent is `3c5ef845`. The merge
  brought in 102 paths from main (onomatopoeia word articles and articles, grammar files, docs) and changed none of the batch's
  files: `evidence\merge-scope.txt` lists the batch's paths and shows that the merge's diff restricted to them is empty. So the
  batch text at `e37ad00b` is the text at `3c5ef845`.
- This revision is one commit on top of the merge. `diffs\fix.patch` is the exact patch from `e37ad00b` to `a7cc61e2`
  (`manifest.json` excluded); `diffs\changed-lines.txt` lists the changed lines. The text at `3c5ef845` is in your earlier
  confirmation packet's `snapshot\kanji\`.
- Five kanji cards changed, each on one line only: its Metadata line. No other line of any card, no word article, article or
  stroke file changed. `manifest.json` was regenerated; it is a generated index and outside the review.

| File | Line | Change |
| --- | --- | --- |
| kanji 乙 | 60 | Metadata line: JMdict entry 1862630 (乙種) inserted after 1182945, before 2855480 (乙女). |
| kanji 亜 | 53 | Metadata line: JMdict entry 1149860 (亜麻) appended. |
| kanji 仁 | 55 | Metadata line: JMdict entry 1369740 (仁術) appended. |
| kanji 仙 | 51 | Metadata line: JMdict entries 1387150 (仙骨) and 1329130 (酒仙) appended. |
| kanji 伯 | 53 | Metadata line: JMdict entry 2261500 (伯母さん) appended. |

Nothing else on these lines changed: the KANJIDIC2 note, the Digital Daijisen, Kanjipedia and Joyo-table links are as before.

## Why

The repository's authoring rule since batch 138 is that a card's Metadata line lists the JMdict entry of every word the card
names; the author's `meta_scan.py` checks it before freeze. It checks whole runs of Japanese script that contain a kanji, so it
does not check kana-only or single-kanji words. At the reviewed snapshot the scan found six named words without their entry on
the Metadata line; the original packet's `mechanical-checks.md`, section "card Metadata entry ids (meta scan)", lists them. The
author did not fix them before freeze, and fixes them now. `evidence\meta-scan-before.txt` is the scan at the merge `e37ad00b`
and `evidence\meta-scan-after.txt` the scan at `a7cc61e2`.

| Word | Where the card names it (unchanged line) | JMdict entry | Written forms; reading | Gloss (pinned JMdict) |
| --- | --- | --- | --- | --- |
| 乙種 | 乙:42, the Joyo table's example words | 1862630 | 乙種; おつしゅ | "B-grade; second-class" |
| 亜麻 | 亜:40, the Joyo table's example words | 1149860 | 亜麻; あま, アマ | "flax (Linum usitatissimum); linseed" |
| 仁術 | 仁:41, the Joyo table's example words | 1369740 | 仁術; じんじゅつ | "benevolent act; healing act" |
| 仙骨 | 仙:40, the Joyo table's example words | 1387150 | 仙骨, 薦骨; せんこつ | "sacrum; sacral bone" / "hermitry; appearance of a hermit; ..." |
| 酒仙 | 仙:40, the Joyo table's example words | 1329130 | 酒仙; しゅせん | "heavy drinker" |
| 伯母さん | 伯:33 and 伯:38, links to the existing article | 2261500 | 伯母さん, 叔母さん; おばさん | "aunt" |

The complete entries are in `evidence\jmdict-cited-entries.xml`. In the pinned JMdict each of the six written forms belongs
to exactly one entry, so there is no other id to choose; 仙骨's single entry 1387150 carries both senses. The cards name the
five Joyo example words (乙種, 亜麻, 仁術, 仙骨, 酒仙) only as written forms, with no reading or meaning. 伯 gives 伯母さん the
reading おばさん (lines 33 and 38) and the meaning "aunt" (line 38), both as in entry 2261500. No line other than the Metadata
lines changed.

After the fix the scan reports no whole-run gap. It still reports four "part-of-run" matches: a shorter dictionary word found
inside a longer word that the card names (熱帯 in 亜熱帯, 歌舞 in 歌舞伎, 伏せ in 伏せる, 母さん in 伯母さん). The longer words'
own entries are on the Metadata lines, and the shorter words are not named on the cards, so they are not added.

## Checks run on the revised snapshot (outputs in `checks\`)

- **`lint.txt`:** 0 errors, 1 warning (`words/潜る.md`: the Dictionary line cites no JMdict entry id). **`unittest.txt`:** 439
  tests, OK. **`validate.txt`:** 0 errors. **`linkplan.txt`:** 0 problems. **`kanji-remarks.txt`:** 0 problems.
  **`vocabulary.txt`:** the same as before.
- **`manifest.txt`:** rebuilding `manifest.json` leaves it unchanged and the tree clean.
- **`budget.txt`:** informational. Retained bytes are 56,608,909: 54 more than at the merge `e37ad00b` (the six ids with their
  separators, 9 bytes each). The figure differs from your earlier packet's `checks\budget.txt` mainly because of the files
  that the merge brought in from main.
- **`quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`:** the same as in your earlier confirmation packet's
  `checks\` (at `3c5ef845`) apart from line 1 (the command and label). The Metadata line is not read by these audits.
- **`evidence\word-quiz.txt`:** the word-quiz audit, rerun at `a7cc61e2`. It is byte-identical to your earlier confirmation
  packet's `evidence\word-quiz.txt` (at `3c5ef845`), although main changed `quiz_exclusions` on 29 of its own onomatopoeia
  word articles and tags on 2.
- **JVM tests:** the Android JVM tests that read the real content were not run (no JDK on this machine).

## Process notes

- The checks in `checks\` and the evidence audits were run on the committed revision `a7cc61e2`.
