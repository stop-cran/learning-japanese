# Batch 141 second revision: what changed from 65b47299 to 094a1649

Revised snapshot: `094a1649552f7773f0a636a104cc797a765bec6e`, a child of the earlier revision
`65b47299831240115de12f5c9c5f0f6ed0e2065d`, which was reviewed in the earlier confirmation round. That revision is a
child of the initially reviewed snapshot `a92d134afd93566ba705b586daf8d7969c683a5f`. Nothing is published.

- Two of the 15 kanji cards changed, on three lines: 抽 (lines 34 and 36) and 懸 (line 46). The other thirteen are
  unchanged. So are all 15 stroke files, the front matter of every card, the existing card 張 and every word article the
  batch edits.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot). No line was added or
  removed. The text at `65b47299` is in the earlier confirmation packet's `snapshot\kanji\`.
- `diffs\fix.patch` is the exact patch from `65b47299` to `094a1649`. `diffs\changed-lines.txt` lists the changed lines
  per file.

| Card | Changed line | Change |
| --- | --- | --- |
| 抽 | 34 | The ひき- row's example is now `抽出し ひきだし - drawer`, not `抽斗 ひきだし - drawer`. The rest of the cell now reads: `JMdict heads the entry 引き出し, lists 抽出し as a search-only kanji form and marks 抽き出し and 抽斗 as rarely used kanji forms; this index form is not a recommended word example, and the word article 引き出し uses the usual spelling; not selected for questions here`. The words `no word article uses this spelling yet,` are removed. |
| 抽 | 36 | The sentence `In 抽斗, 抽 writes ひき and 斗 writes だし; Daijisen lists 抽斗 ひきだし as a hard-to-read word.` is removed. The 抽出し sentence now reads `In 抽出し, 抽 writes ひき, 出 writes だ and し is okurigana, the kana ending that follows the kanji; the same two kanji are read ちゅうしゅつ in 抽出.` (its search-only label moved to line 34). The 抽き出し sentence is unchanged. A new last sentence reads `Daijisen lists the rarely used spelling 抽斗 ひきだし as a hard-to-read word; this is a reading of the whole word, not a kanji-by-kanji reading, and KANJIDIC2 gives 斗 no reading だし.` |
| 懸 | 46 | The last clause, `JMdict lists けねん first and also the reading けんねん, where 懸 supplies ケン.`, now reads `JMdict lists けねん first and also けんねん, which it marks as irregular kana usage; in けんねん, 懸 supplies ケン.` Nothing else on the line changed. |

Why:

- 抽斗 ひきだし is a whole-word reading: Daijisen lists it among the hard-to-read words of its 抽 entry, and the pinned
  KANJIDIC2 snapshot gives 斗 only the on readings ト and トウ (and the name reading ます), so 斗 has no reading だし.
  The earlier revision split the word as if it had. In the search-only spelling 抽出し the reading ひき- of 抽 is
  visible on its own, so it is now the row's example, labelled in the wording other cards use for source-only rows whose
  only JMdict example is a search-only form (for example 双, 圧 and 訓). Support: `evidence\jmdict-cited-entries.xml`,
  entry 1601650 (`抽出し`: search-only kanji form; `抽き出し` and `抽斗`: rarely used kanji form; sense 1 "drawer" is
  not restricted to any spelling); `evidence\kanjidic2-斗.xml`, 斗's complete record in the pinned KANJIDIC2 input; the
  original packet's `evidence\kanjidic2-records.xml` for 抽's ひき- and its `evidence\public-source\weblio-抽.txt`,
  line 6, where Daijisen lists 抽斗 (ひきだし) under 難読, hard-to-read words.
- JMdict entry 1257720 tags the reading けんねん "word containing irregular kana usage"; けねん carries the priority
  tags. Support: `evidence\jmdict-cited-entries.xml`, entry 1257720. `扇.md:42` reports the same tag for おおぎ.
- Entries 1601650 and 1257720 were already on the Metadata lines of 抽 and 懸, so those lines are unchanged.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `65b47299`. The outputs are identical apart from line 1 of each audit (the
command, which names the commit), the test run time, the content budget sizes and one line number in `meta-scan.txt`:
the uncompressed sizes grow by 191 bytes, the length of the added text (抽 152, 懸 39), and the compressed size by 77
bytes.

- `lint.txt`: the batch linter (16 kanji cards: the 15 new ones and 張; 28 word articles): 0 errors, 2 warnings, both
  on word articles whose Dictionary line cites no JMdict entry id (扇風機, 威張る). Same as at `65b47299`.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage
  pilot). `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt` and `kanji-remarks.txt`: unchanged results: 21 changed word files, 21 added links, 2 declared remark
  edits, 0 problems; 15 of 15 new cards present, the one declared remark edit in 張 applied, 0 problems.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine), so there is no `jvm.txt`.
- `link-targets.tsv`: the links on the changed lines to other cards and word articles. It lists none: the changed lines
  have no link.
- `quiz-safety.txt`: the meaning-quiz audit, copied byte for byte. It is byte-identical to the earlier confirmation
  packet's `checks\quiz-safety.txt`; no front matter changed.
- `reading-exposure.txt` and `reading-options.txt`: identical to the earlier confirmation packet's copies apart from
  line 1. Summary lines: 0 production hits, 0 padded-session hits, 5 latent collisions, 0 one-holder padded hits; 0
  problems in `reading-options.txt`.
- `evidence\meta-scan.txt`: `meta_scan.py` on the 15 cards at `094a1649`. Apart from line 1 it differs from the earlier
  confirmation packet's copy in one line: `抽.md:36: 出し 1339160 not listed part of 抽出し` is now
  `抽.md:34: ...`, because 抽出し now first appears on line 34. The totals are unchanged: no word the script checks
  lacks its entry, and 30 words are found only inside a longer word.

## Process notes

- `094a1649` is a single signed commit on top of `65b47299`; nothing was published in between.
- The checks in `checks\` were run on the committed revision.
