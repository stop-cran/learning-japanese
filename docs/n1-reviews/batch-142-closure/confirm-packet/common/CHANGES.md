# Batch 142 revision: what changed from 9d393a8f to 3a0399bd

Revised snapshot: `3a0399bd` (full hash in `diffs\fix.patch`'s header and `packet-manifest.json`). It is reached from the
reviewed snapshot `9d393a8f7bbf04114668b40f84b67a9a4b2ef7e3` by one commit. Nothing is published.

- Five of the 15 new kanji cards changed: 描, 提, 揺, 斉 and 斎. The other ten (挙 振 挿 掌 推 揮 操 故 敵 斜) are
  unchanged. The existing card 仮 (declared remark edit), all 24 word articles and all 15 stroke files are unchanged
  from the reviewed snapshot.
- No front matter changed: no title, tag, metadata reading, `distractors` or `quiz_exclusions` list. The meaning and
  reading quiz options are therefore unchanged (see "Checks" below).
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. 揺 gained 4 lines (line 25 became lines 25-27, line
  29 became line 31, line 47 became lines 49-51, line 56 became line 60); 斉 gained 4 lines (line 25 became lines 25-29);
  斎 gained 4 lines (line 32 became lines 32-36). The Metadata and Usage lines of those three cards moved down by 4.
  提 and 描 did not change length.
- `diffs\fix.patch` is the exact patch from `9d393a8f` to `3a0399bd`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every link on a changed line and the title quoted after it are listed in `checks\link-targets.tsv`, with the target's
  real `title:`.
- Metadata lines changed in two cards only, by adding JMdict entry ids: 提 gains 1734790 (提灯行列), 1734800
  (提灯持ち) and 1446650 (唐音); 描 gains 2751570 (すがき). `evidence\meta-scan.txt` finds no word without its entry.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 提 | 40, 46, 62 | Line 40, the チョウ row: the claim that 提灯 is チョウ's only JMdict word, that ちょうちん belongs to the whole word and that no source assigns ちょう to 提 alone is removed. The row now says チョウ is listed in KANJIDIC2 and, as outside the official table, by Kanjipedia; that it is the reading of 提 in 提灯 ちょうちん, which Daijisen writes ▽提▽灯 and labels 唐音 (JMdict 1446650: "tō-on; Tang reading; on reading of a kanji based on Song dynasty and later Chinese"); that JMdict also has compounds such as 提灯行列 and 提灯持ち; and that there is no word article yet and it is not selected for questions. Line 46: `チョウ has no ordinary example of its own.` is replaced by `no word article has 提灯 yet.` Line 62: Metadata gains 1734790, 1734800 and 1446650. Support: `evidence\weblio-chouchin.txt` (Daijisen `ちょう‐ちん【▽提▽灯】`, 《唐音》), `evidence\jmdict-cited-entries.xml`, and the original packet's `evidence\kanjipedia-outside-readings.json`. |
| 斎 | 32-36 | The single paragraph is split into three. Line 32 keeps the Daijisen kun readings and now says `in 斎宮, 斎 is read いつき, the の is not written and 宮 is みや` instead of the blanket `these are readings of the whole word and are not split between the kanji`. Line 34 (new paragraph): the さい【斎】 summary now reads `a Buddhist noun that also follows the names of rooms and the pen names of writers and artists` (was `names of studios and rooms`). Line 36 (new paragraph) is the ▽い and ▽ゆ paragraph, unchanged. Support: `evidence\weblio-saigu.txt` (`いつき‐の‐みや【▽斎宮】`), and the original packet's Daijisen extract for さい【斎】 (`居室の名や文人などの雅号に添えて用いる`). |
| 揺 | 25-27, 31, 49-51, 60 | Line 25 is split so the hard-to-guess-reading sentence starts line 27 (new paragraph). Line 31, the mnemonic: `a claw-like top over [缶](缶.md), "tin can; container."` now reads `a claw-like top over a shape like [缶](缶.md), "tin can; container," with one stroke fewer.` Lines 49-51: the paragraph after the readings table is split so `Practice selects ゆ.れる …` starts its own paragraph. Line 60, first Notes bullet: `[缶](缶.md), "tin can; container," is the bottom of the right part of 揺.` now reads `[缶](缶.md), "tin can; container," has six strokes; the bottom of the right part of 揺 is a five-stroke shape like it.` The same-wording sentence about 採 and 稲 is unchanged. Support: `evidence\stroke-types.txt` (KanjiVG stroke types of the repository files `strokes\揺.json` and `strokes\缶.json`: 缶 is ㇒ ㇐ ㇐ ㇑a ㇄a ㇑, and 揺 strokes 8 to 12 are ㇐ ㇐ ㇑a ㇄a ㇑, so the lower right part is 缶 without its first stroke ㇒). |
| 斉 | 25-29 | The single paragraph of Daijisen senses is split in three: line 25 (first sense and its examples), line 27 (second sense, the state of Qi), line 29 (the セイ and サイ readings and the kun-reading remarks). Wording is unchanged. |
| 描 | 52 | Metadata gains JMdict 2751570 (すがき, "uncolored sketch; line sketch; rough sketch", also written 素描), the entry the card already mentions on line 37. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter (16 kanji cards: the 15 new ones and 仮; 30 word articles): 0 errors, 6 warnings, all on
  word articles whose Dictionary line cites no JMdict entry id. The same six warnings were reported at the reviewed
  snapshot.
- `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes. `manifest.txt`: `manifest.json`
  regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt`: 24 changed word files, 24 expected and 24 added link pairs, 0 declared remark edits, 0 problems.
- `kanji-remarks.txt`: existing kanji cards are unchanged apart from the declared remark edit in 仮 (1 modified, 15 of
  15 new cards present, 0 problems).
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine), so there is no `jvm.txt`.
- `quiz-safety.txt` is identical to the original packet's `evidence\audits\quiz-safety.txt`: 0 errors, 0 warnings.

### Reading audits

`reading-exposure.txt` and `reading-options.txt` were rerun with the same `--extra` input as at the freeze. Apart from
line 1 (the command), both are identical to the original packet's `evidence\audits\` files, because no front matter
changed.

- `reading-exposure.txt` line 276: 0 production hits, 0 padded-session hits, 12 latent collisions, as at the freeze;
  0 one-holder padded hits.
- `reading-options.txt` line 233: 1 problem, the same one as at the freeze: 斎 い. The pool-aware reading-exposure audit
  shows it cannot be drawn (see the original packet).

## Process notes

- `3a0399bd` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `9d393a8f`.
- The checks in `checks\` were run on the committed revision.
