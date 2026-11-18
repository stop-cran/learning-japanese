# Batch 135 revision: what changed from 163b384e to 2ef25d33

Revised snapshot: `2ef25d33ab16d928ac4f0a845b4d8f78005223da`, a child of the reviewed snapshot
`163b384e6cb8f75c06fe395f7b144cdd8b105673`. Nothing is published.

- Nine of the 15 kanji cards changed: 博, 履, 巡, 弾, 恵, 憶, 揚, 救 and 模. The other six (厳, 及, 姿, 彫, 我, 暇) are
  unchanged, and so are all 15 stroke files, all titles, tags, metadata readings and `quiz_exclusions`. No word article
  changed in this revision.
- Front matter changed only in `distractors` (line 13) of 巡 and 救.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Every quoted title in the new text was checked by script against the linked card's real `title:` (11 links on changed
  lines, 0 unresolved or mismatched; see `checks\link-targets.tsv`).
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other evidence
  stays in the original packet.

| Card | Changed lines | Change |
| --- | --- | --- |
| 博 | 27 | The mnemonic now reads `At the right is 甫, which has no card here, standing over [寸](寸.md), "sun (length unit); small"; the dot at the top right is part of 甫 itself.` (it read `At the right is a shape like 甫 with an extra dot at its top right (甫 has no card here), standing over [寸](寸.md), "sun (length unit); small."`). The rest of the paragraph is unchanged. Support: KANJIDIC2 gives 甫 7 strokes (`evidence\kanjidic2-甫.xml`, line 20); in `evidence\kanjivg\0535a.svg` the right-hand group 尃 (line 44) holds 甫 (lines 45-59: strokes 3 to 9, the dot being stroke 9 at lines 56-57) over 寸 (lines 61-65: strokes 10 to 12); 十 2 + 甫 7 + 寸 3 = 12, the card's `strokes: 12`. KanjiVG marks this 甫 `kvg:variant="true"` and 尃 `kvg:phon="尃"`, and also tags strokes 3 to 8 (甫 without its dot) and 寸 as parts 1 and 2 of 専 (lines 46 and 60); the mnemonic still makes no claim about formation or sound. |
| 履 | 36, 51 | Line 36: `The ぞう belongs to 草: Daijisen spells it ザウ in historical kana, the voiced form of サウ, its historical spelling of 草's ソウ. ぞう itself is not among 草's KANJIDIC2 readings, ソウ and くさ, and the Joyo table accordingly puts 草履 ぞうり in its appendix` (it read `The ぞう belongs to 草 and is not among its KANJIDIC2 readings, ソウ and くさ, which is why the Joyo table puts 草履 ぞうり in its appendix`). Line 51 adds `Historical kana of ぞう and ソウ: [Digital Daijisen, 草履](https://www.weblio.jp/content/草履) and [Digital Daijisen, 草](https://www.weblio.jp/content/草).` Support: `evidence\daijisen-草履.txt` line 7 (`ぞう‐り〔ザウ‐〕【草履】`), `evidence\daijisen-草.txt` line 7 (`［音］ ソウ （ サウ ）`), `evidence\joyo\p98.txt` line 9, `p155.txt` line 12 and `p163.txt` line 16. |
| 巡 | 13, 37, 39, 49 | Line 13: `distractors: [川, 道, 達]` (it was `[順, 川, 純]`). Line 37 gains a final sentence: `[Kanjipedia's character entry](https://www.kanjipedia.jp/kanji/0003246000) does list まわる as a kun reading outside the official table, so this card's quiz does not offer まわる as a wrong answer.` Line 39: `so めぐ.る supplies the one question for that stem, shown as めぐる;` (it read `so めぐ.る supplies the めぐ question;`). Line 49 gains `[道](道.md), "road, way," and [達](達.md), "reach, plural suffix," have the same 辶 wrapping the left side and the bottom.` after the 川 sentence; the sentences on 順 and 純 are unchanged. Support: `evidence\kanjipedia-巡.txt` line 6. |
| 弾 | 25-33, 67 | The single sense paragraph at line 25 is now an intro (line 25, `The Daijisen character entry gives five senses for ダン. One example of each:`), a five-bullet list with one example per sense (lines 27-31: 弾奏, 弾指, 弾圧 "besides 弾劾", 弾力, 爆弾) and the line `A separate entry uses だん to count bullets and installments; more Daijisen examples are listed at the end of the Notes.` (line 33). Every other example word and gloss of the old paragraph (弾琴, 連弾, 糾弾, 指弾, 弾性, 弾丸, 弾薬, 実弾, 銃弾, 砲弾) and the two JMdict counter glosses moved, unchanged, to a new last Notes bullet (line 67) beginning `For reference, more Daijisen examples of the ダン senses:`. No example, reading or gloss was added or dropped. |
| 恵 | 40 | `so めぐ.む supplies the one question for that stem, shown as めぐむ;` (it read `so めぐ.む supplies the めぐ question;`). |
| 憶 | 25, 49 | Line 25: after the unchanged JMdict sentence, `; 臆 does not have a kanji card here.` is replaced by `. The official Joyo table, however, gives 臆, which does not have a kanji card here, its own row, with オク and the examples 臆説, 臆測 and 臆病 おくびょう, "cowardly; timid; easily frightened," and notes that 臆説 and 臆測 are also written 憶説 and 憶測, so the table accepts both spellings.` Line 49: JMdict 1182790 (臆病) is added to the entry list. Support: `evidence\joyo\p18.txt` lines 45-47; `evidence\jmdict-cited-entries.xml` (1182790 lines 23-45, with 憶病 tagged `rarely used kanji form` at lines 29-30; 1182750 and 1589020 for 憶説/臆説 and 憶測/臆測). |
| 揚 | 40 | `so あ.げる supplies the one question for that stem, shown as あげる;` (it read `so the あ question comes from あ.げる;`). |
| 救 | 13, 48-49 | Line 13: `distractors: [敬, 球, 教]` (it was `[求, 球, 教]`). Line 48: `; and [敬](敬.md), "respect; honor," also has 攵 at the right` is appended to the look-alike list (the `and` that stood before 教 now stands before 敬, and the clause on 教 now ends with `;` instead of `.`). Line 49 is a new bullet: `[Kanjipedia's character entry](https://www.kanjipedia.jp/kanji/0001400000) marks the on readings グ and ク and the kun reading たすける as outside the official table. They are not in KANJIDIC2 or this card's metadata, so they are not asked, and this card's quiz does not offer them as wrong answers either. For that reason, 求, which is also read グ, is not among the look-alike kanji this card's quiz uses for wrong answers.` Support: `evidence\kanjipedia-救.txt` line 6. The mnemonic at line 27 still names 求 as the shape at the left; only the quiz option changed. |
| 模 | 36 | `Each is read as a whole word, so its reading is not split between its kanji.` (it read `Both are learned here as whole words.`). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on the 15 kanji cards and their 32 word articles: 0 errors, 7 warnings, all on unchanged word
  articles (6 say the Dictionary line cites no JMdict entry id, 1 says there is no Dictionary line). Same as for the
  reviewed snapshot.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage pilot).
  `manifest.txt`: `manifest.json` regenerated (8816 files), rebuild idempotent, tracked tree clean.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either, so there is no `jvm.txt`.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether the
  gloss quoted after the link equals that title.
- `quiz-safety.txt`, `reading-options.txt` and `reading-exposure.txt`: see the next section.

## Quiz mechanics the changes rely on

- Meaning quiz (`evidence\QuizBuilder.kt`): options are the curated `distractors` in order, skipping any that is excluded
  against the target or an already chosen option; other cards are added only when fewer than three survive.
  `checks\quiz-safety.txt` shows the post-fix meaning options: 巡 `river | road, way | reach, plural suffix` (line 15) and
  救 `respect; honor | ball; sphere | teach, instruct` (line 37). Its `reading ... wrong options from distractors N/3` lines
  count curated slots for the reading prompts.
- Reading quiz (`evidence\KanjiReadings.kt`, `KanjiReadingQuiz`; `evidence\Words.kt` for `ReadingOptions.mutations`):
  `quiz_exclusions` affect only the meaning quiz. Each curated `distractors` card offers one random usable reading of the
  asked kind (skipped if it is empty, excluded or a duplicate); remaining slots are filled from other cards' readings in
  closeness tiers (length within one kana, same first kana, same last kana), highest tier first. The excluded readings are
  the target's own readings and their sound-change variants.
- `checks\reading-exposure.txt` enumerates the pools the app builds: the N1 and All stacks (1,277 cards each) and the
  Starter practice session (the 118 starter cards plus the borrowed target), and for each attested but unlisted reading
  also tries a Starter session that borrows one extra holder card. This round it adds as attested readings every reading
  Kanjipedia marks as outside the official table (外) for the 15 kanji (`evidence\kanjipedia-outside-readings.json`;
  command at line 1). The tool labels readings given with `--extra` as `(card text)`. Result (line 396): 0 production
  hits, 0 padded-session hits, 25 latent collisions (19 at the reviewed snapshot; the 6 new ones are Kanjipedia 外
  readings: 巡 まわる, 弾 はずみ twice,   救 ぐ, く and たすける).
  The same command run on the reviewed snapshot (`evidence\reading-exposure-163b384e.txt`) reports 2 production hits,
  which this revision removes: 巡 まわる, offered by 回 in the N1 and All stacks (line 148), and 救 ぐ, offered by 供, 具,
  工 and 求 (line 338). The other 13 card blocks of the two audits are identical.
  - 巡 (lines 131-154): 川, 道 and 達 are all starter cards (lines 132-134) and fill all three wrong slots of both prompts
    in the N1 stack, the All stack and the Starter session, so the fallback is never consulted (lines 138-140 and
    145-147). まわる, offered by 回, cannot be drawn in any pool (line 148), including a Starter session that also
    borrows 回 (line 150).
  - 救 (lines 330-358): 敬, 球 and 教 are not starter cards (lines 331-333), so in the Starter session both 救 prompts
    take all three wrong options from the fallback (lines 339 and 352), as they did at the reviewed snapshot with 求, 球
    and 教 (original packet lines 255 and 259). ぐ, く and たすける cannot be drawn in any pool or with any single extra
    holder (lines 340-345, 353-355).
  - Unchanged from the reviewed snapshot (original packet `evidence\audits\reading-exposure.txt` lines 177, 180 and 229):
    a Starter session that borrows 恵 and also one of 丙 並 兵 塀 平 病 閉, or of 味 未 魅, can offer the KANJIDIC2 name
    reading へい or み as a wrong option for 恵's エ prompt (lines 238-243), and one that borrows 我 and also 蚊 or 香 can
    offer the name reading か for われ (lines 302-304). These are name readings only, not offered in the N1 or All stack or
    the plain Starter session.
- `checks\reading-options.txt` is the older superset audit over every card in `kanji\` with the same added readings. It
  reports `1 problem(s)` (line 348): 巡 まわる from 回 (line 132), because it does not model that the three curated
  options already fill every slot (lines 126-128). `reading-exposure.txt` is the exact enumeration for this case.
- Neither audit runs the app's own code or random generator; both are the author's Python ports of the Kotlin sources in
  `evidence\`. Sampled seeds are a sanity check; the enumerations are the result.
