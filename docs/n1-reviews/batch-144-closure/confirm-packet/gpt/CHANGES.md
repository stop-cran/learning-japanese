# Batch 144 revision: what changed from b073abd8 to 8db07f74

Revised snapshot: `8db07f74` (full hash `8db07f740a2071609b29539cc1a29e4420bc43e5`; also in `packet-manifest.json`). It is
reached from the reviewed snapshot `b073abd8f2ab578f29cf2b5e25f36e02fc1aab58` by two commits, `2be716f0` and `8db07f74`;
`diffs\fix.patch` is their combined patch. Nothing is published.

- Ten kanji cards changed: nine new cards (棋 棚 欄 歓 殻 汁 沖 淡 渋) and the existing card 討 (its declared remark edit
  was reworded). The other six new cards (検 概 殊 泡 泣 渇), all 18 word articles and all 15 stroke files are unchanged
  from the reviewed snapshot.
- **No front matter changed.** No title, tag, metadata reading, `distractors` or `quiz_exclusions` list changed in any
  card, so the meaning and reading options are unchanged; the three quiz and reading audits were rerun and are
  line-for-line identical to the freeze output apart from their command lines.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. 殻, 汁 and 渋 gained lines because long paragraphs were
  split; every other changed card keeps its line count.
- `diffs\fix.patch` is the exact patch from `b073abd8` to `8db07f74`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every link on a changed line and the title quoted after it are listed in `checks\link-targets.tsv`.
- Only one Metadata line changed: 棚 (line 53, see the table).
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 棚 | 25, 33, 53 | Line 25: the separate Daijisen entry is now written with its real headword mark, たな【▽店／棚】, and the text says the ▽ marks 店 (the spelling whose reading is outside the Joyo table), not 棚; the claim that 棚 is a non-standard form is gone. Line 33 (ホウ row): the claim that 氷棚 is the only JMdict word with ほう is replaced by 陸棚 りくほう (also りくだな), "continental shelf," and 氷棚 ひょうほう, "ice shelf." Support: `evidence\jmdict-cited-entries.xml` (1551120 陸棚, with りくだな and りくほう) and the original packet's `evidence\daijisen-heads.txt` lines 5-7. Line 53 (Metadata): JMdict entry 1551120 (陸棚) is added to the entries list, so that the word now named in the ホウ row is listed. |
| 歓 | 45 | The Notes sentence that 権 has a similar-looking left part now says 権 has a part at its right that looks like the left part of 歓 (権's left is 木). |
| 淡 | 32 | `the name-only readings あわ, あわし and あわじ` now reads `あわ, as in 淡雪 あわゆき, and the name readings あわし and あわじ`. Support: the original packet's `public-source\weblio-淡.txt` (〈あわ〉「淡雪」 apart from ［名のり］ あわ・あわし・あわじ) and `evidence\jmdict-cited-entries.xml` (1418470 淡雪). |
| 欄 | 42, 44 | The double-quoted gloss of 欄 おばしま no longer includes the `archaic` tag: it is `"handrail; railing; banister; balustrade,"` and the sentence says JMdict marks the entry archaic. Support: `evidence\jmdict-cited-entries.xml` (2844081: `misc` archaic; four glosses). Line 44: `It prints a parenthesized form after 欄, a compatibility form of the same kanji that this card does not teach separately` is replaced by `It prints the older form of 欄 in parentheses; this card does not teach that form separately`, the wording used for the bracketed forms on the other cards of this batch. |
| 棋 | 32 | ご row: `KANJIDIC2 files it under kun, but Kanjipedia lists ゴ as an on reading` added. Support: the original packet's `evidence\kanjipedia-outside-readings.json` (棋: on キ and ゴ). The metadata lists are unchanged. |
| 沖 | 34 | ちゅう.する row: `KANJIDIC2 files it under kun, but the Joyo table files 沖する under チュウ` added. Support: the original packet's `evidence\joyo-pages.md` (チュウ: 沖積層, 沖天, 沖する). The metadata lists are unchanged. |
| 討 | 95 | The declared remark edit is reworded. The bullet read `In 検討, [検](検.md) supplies ケン. This does not change the complete word's reading.`; it now reads `In 検討, [検](検.md) supplies ケン and 討 supplies トウ.` The `This` of the second sentence had lost its antecedent. `evidence\kanji-remarks.json` is the updated declaration (old text unchanged, new text as above). |
| 殻 | 37, 39 | The single long reading paragraph is split in two at `Whole words are not split:`; the text is otherwise identical. |
| 汁 | 36, 38, 40 | The long paragraph is split into three: the JMdict entry and しる/つゆ restriction (line 36); the -しる row, 果汁 and 墨汁 (line 38); the whole words 灰汁 and 苦汁 (line 40). Text otherwise identical. |
| 渋 | 44, 46, 48 | The long paragraph is split into three: 渋滞 and ジュウ (line 44); 渋い and 渋る with their senses (line 46); 渋々, 渋み and the search-only 澁い (line 48). Text otherwise identical. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter (16 kanji cards: the 15 new cards and the modified 討; 19 word articles touched by the batch): 0 errors, 3 warnings, all on word articles whose
  Dictionary line cites no JMdict entry id (戸棚, 淡水, 特殊). The same three warnings were reported at the reviewed
  snapshot. With `--no-jmdict` there are 0 warnings.
- `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes. `manifest.txt`: `manifest.json`
  regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt`: 18 changed word files, 18 expected and 18 added link pairs, 1 declared remark edit (特殊), 0 problems.
- `kanji-remarks.txt`: 15 of 15 new cards present; one modified existing card (討), its declared remark edit applied
  (the updated declaration), 0 problems.
- The Android app's JVM tests that read the real content were not run for this revision either, and the Kotlin
  cross-check of the reading audit was not run, as at the freeze.

### Quiz and reading audits

`quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt` were rerun at `8db07f74` with the same `--extra`
input as at the freeze. They are line-for-line identical to the freeze output apart from the command line (the author's
comparison of the two runs, not a substitute for your own reading of the files):

- `quiz-safety.txt`: 0 errors, 0 warnings.
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, 0 one-holder padded hits, and 6 latent collisions
  (欄 わく, 歓 ぶ, 殊 け, 殻 かい, 沖 とぶ, 沖 むなしい), as at the freeze.
- `reading-options.txt`: 1 labelled HIT (殻 かい, offered by 貝), as at the freeze; the exposure audit shows it cannot be
  drawn because the curated distractors 休, 本 and 木 fill every slot.

## Process notes

- `2be716f0` and `8db07f74` are the two fix commits; `diffs\fix.patch` is the whole change from the reviewed snapshot `b073abd8`.
- The checks in `checks\` were run on the committed revision.
