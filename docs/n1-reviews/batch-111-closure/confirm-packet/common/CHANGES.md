# Batch 111 revision: what changed from 3b30803e to bf9ee962

Revised snapshot: `bf9ee9622723078438a021d54cac5ce8252f95d8`, a child of the reviewed snapshot
`3b30803e33438dab7a1071aea34ceb7764189c1f`. Nothing is published.

- Six of the 15 kanji cards changed: 房, 敷, 節, 義, 評 and 鏡. The other nine (修, 句, 授, 旬, 標, 独, 率, 製, 養) are
  unchanged, and so are all 15 stroke files and all titles. No word article changed in this revision.
- Front matter changed only in `quiz_exclusions` (line 14) of 節 and 義. `distractors`, titles, tags and metadata readings
  are unchanged on all 15 cards.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Every quoted title in the new text was checked by script against the linked card's real `title:` (23 links on changed
  lines, 0 unresolved or mismatched; see `checks\link-targets.tsv`). The four links in the 敷 table rows (lines 34 and 35)
  carry no quoted gloss, so the table shows "n/a" for them.
- New evidence in this packet is everything under `evidence\`, including the Joyo table page extracts in `evidence\joyo\`
  (pages 34, 39, 93, 132, 134 and 142, one per changed card); `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| Card | Changed lines | Change |
| --- | --- | --- |
| 房 | 25 | The Daijisen's fourth ボウ sense (the old province of Awa) is now illustrated with the words the Daijisen gives for it: `as in 房州 and 房総. JMdict has the province name as 安房 あわ` (it read `as in 安房 あわ`). JMdict's gloss for 安房 is kept and is now attributed to JMdict, and the next sentence begins `For ふさ the Daijisen gives threads bundled` (it began `For ふさ it gives threads bundled`). No reading, gloss or JMdict id was added for 房州 or 房総: neither occurs in the original packet's `evidence\jmdict-families.xml`, which holds every JMdict entry written with 房, so neither is a JMdict kanji form, and the Daijisen prints them without readings. |
| 敷 | 34, 35, 37, 39 | 敷地 しきち moves from the -し.き row to the し.く row (line 34), because its しき begins the word. The -し.き row (line 35) is now typed `kun suffix` (it was `kun, bound form`; `氏.md` line 32 and `始.md` line 30 of the original packet already use `kun suffix`) and keeps only 座敷 and 風呂敷, whose しき follows another element. Line 37: `In 敷地, 敷 reads しき at the start of the word, as in 敷居 and 敷金, and 地 supplies チ.` now comes before the sentence on 座敷 (it read `In 敷地, 敷 reads しき and 地 supplies チ.` and came after the sentence on 風呂敷), and the dash sentence reads `The leading dash in -し.き marks a suffix use, one that follows another element` (it read `The dash in -し.き marks a bound form, one that appears inside compounds`). Line 39 gains `The Daijisen lists its しき words in two groups separated by a slash`, naming the two groups and where this card files 敷地, 座敷 and 風呂敷. |
| 節 | 14, 25, 36, 39, 56 | Line 14: `quiz_exclusions` gains 句 and 旬 and now reads `quiz_exclusions: [季, 春, 期, 接, 制, 倹, 限, 際, 祭, 部, 句, 旬]`; each pair is declared once, on 節's side, and `句.md` and `旬.md` are unchanged. Line 25: the separate noun 節 せつ, which has no word article here, is now also glossed with its second JMdict sense, `"section (of a literary work or piece of music); passage; paragraph; verse; stanza" in its second` (JMdict 1386140; its first sense, "occasion; time", is unchanged). Lines 36 and 39: the -ぶし row is typed `kun suffix` (it was `kun, bound form`) and the dash sentence reads `The leading dash in -ぶし marks a suffix use, one that follows another element; it is not pronounced.` (it read `The dash in -ぶし marks a bound form, one that appears inside compounds; it is not pronounced.`). Line 56: the overlap bullet now names `[句](句.md), "phrase; verse," and [旬](旬.md), "ten days; peak season,"`, adds "verse" to the overlapping senses and ends `Do not treat "season," "verse" or "restraint" as exclusive to any one character.` |
| 義 | 14, 52 | Line 14: 税 is removed from `quiz_exclusions`, which now reads `quiz_exclusions: [役, 務, 意, 理, 正, 替, 敬]`. Line 52: the overlap bullet no longer names 税 or its title and now begins `[役](役.md), "role; duty," and [務](務.md), "duties," overlap the sense "duty" that 義 and 義務 carry` (it began `[役](役.md), "role; duty," [務](務.md), "duties," and [税](税.md), "tax; fiscal duty," overlap the sense "duty"`). `税.md` is unchanged. |
| 評 | 35 | `in 評判, 判 supplies バン, an on reading of 判 besides ハン` (it read `in 評判, 判 supplies ハン`). 評判 is read ひょうばん (JMdict 1490070), so 判 supplies バン there; バン is a listed on reading of 判 (`evidence\kanjidic2-judge.xml`: on ハン and バン). |
| 鏡 | 25, 39, 56 | Line 25: `as in 眼鏡 がんきょう, "glasses; eyeglasses; spectacles," 顕微鏡 and 望遠鏡` (it read `as in 眼鏡, 顕微鏡 and 望遠鏡`); 眼鏡 がんきょう is JMdict 2862467, whose one sense is "glasses; eyeglasses; spectacles". Line 39 gains `The Daijisen lists 眼鏡 twice: once among its キョウ words, where it matches the separate JMdict entry 眼鏡 がんきょう, and once among its hard-to-read words, as めがね.` Line 56: the JMdict id list now ends `1737930, 1238580 and 2862467` (it ended `1737930 and 1238580`). The title `mirror; lens` is unchanged. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on 17 kanji cards (the 15 batch cards and 価 and 暖, the two existing cards the batch also
  edits) and 69 word articles: 0 errors, 13 warnings. All 13 are on word articles and are of two kinds: 10 say the
  Dictionary line cites no JMdict entry id (女房 標本 標準 標識 独り言 能率 製作 評論 調節 風呂敷) and 3 say there is no
  Dictionary line (授業 眼鏡 鏡). The output is the same as for the reviewed snapshot, and no word article changed.
- `unittest.txt`: 431 tests, OK. `validate.txt`: 0 errors. `budget.txt`: content archive budgets met. `vocabulary.txt`:
  vocabulary coverage check passes (2122 of 2431 reviewed prompts, stage pilot). `manifest.txt`: `manifest.json`
  regenerated (8571 files) and committed.
- The Android app's JVM tests that read the real content (`RealContentTest`, `RareHanTest`, `KanjiReadingsTest`) were not
  run for this revision, so there is no `jvm.txt`. The original packet's `mechanical-checks.md` lists them as not run for
  the reviewed snapshot too.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether
  the gloss quoted after the link equals that title.
- `quiz-safety.txt`, `reading-options.txt` and `reading-exposure.txt`: see the next section.

## Quiz mechanics the changes rely on

- The repository validator's rules (all pass; `validate.txt`: 0 errors): `quiz_exclusions` has no duplicates, no self,
  every entry has a card, and no entry may also be one of the same card's `distractors`.
- Meaning quiz: the app's `QuizBuilder` is in `evidence\QuizBuilder.kt`: options are the curated `distractors` in order;
  any candidate that is excluded against the target or an already chosen option is skipped; `excluded(a, b)` is true if
  **either** card lists the other, so a pair needs to be listed on one side only (the repository lists each pair once).
  Only when fewer than three curated distractors survive are other cards added (tag-similar first).
- `checks\quiz-safety.txt` prints the four meaning options now shown for each of the 15 cards (the first option is the
  correct title). The "reading ... wrong options from distractors N/3" lines under each card count curated slots for the
  reading prompts, not the options themselves. Lines 36-47 list 11 existing cards outside this batch (人 休 何 入 出 口
  女 日 月 男 買) whose options use the tag-similar fallback; they are not part of this review. No title, distractor or
  shown option changed in this revision.
- Reading quiz: `quiz_exclusions` affect only the meaning quiz. Reading prompts are built by `KanjiReadingQuiz` in
  `evidence\KanjiReadings.kt`. Each curated `distractors` card offers one random usable reading of the asked kind (skipped
  if it is empty, excluded or a duplicate); the remaining slots are filled from the other cards' readings, those closest to
  the target reading first (length within one kana, same first or same last kana), then any other readings.
  `excludedKeys(target)` is every on and kun reading of the target card plus the sound-change variants made by
  `ReadingOptions.mutations` in `evidence\Words.kt`.
- `checks\reading-options.txt` is the author's audit of every reading prompt of the 15 cards: 19 prompts in 18 of the 30
  card-and-kind pairs (率 has two on prompts, ソツ and リツ; the other 12 pairs have no reading prompt and say so). For each prompt it lists the excluded keys, what the
  curated option cards offer, the fallback candidates by closeness tier, whether a reading that is attested for the card
  but not listed in its metadata (a KANJIDIC2 name reading, for example) can be offered as a wrong option, and a simulation
  of 400 seeded draws. Result: "0 problem(s)". It cannot show the exact draws: the pool is every card in `kanji\` (1,176
  cards, the largest possible pool, while the app draws from the cards the learner has studied), fallback options are
  random within closeness tiers, and the audit's random generator is not the app's, so it reports candidate sets. Four
  "note" lines (lines 39, 40, 212 and 236: 房 ボウ with お and わ, 養 ヨウ with や, 鏡 かがみ with あき) record an unlisted
  reading that other cards offer only from a lower closeness tier, so the fallback cannot reach it while higher tiers are
  available. No case is only informational.
- `checks\reading-exposure.txt` is the author's audit of the pools as the app builds them (`content.inStack`): the N1
  stack and the All stack, 1,176 cards each, and the Starter practice session (the 118 cards tagged starter plus the
  borrowed target). For each reading prompt of the 15 cards it checks whether another card in those pools offers an
  attested but unlisted reading of the target as a wrong option. Result (line 257): 0 production hits (N1 and All stack
  pools), 0 padded-session hits (Starter practice session only) and 6 latent collisions, that is, an attested reading that
  another card offers but that no pool above can draw: 房 ボウ with お (line 42) and わ (line 45), 節 セツ with よ (line
  159), 節 ふし with よ (line 169), 養 ヨウ with や (line 227) and 鏡 かがみ with あき (line 251). The output is the same
  as for the reviewed snapshot.
- Exclusion changes in this revision: 節 gains 句 and 旬 (`節.md` line 14), each pair declared once, on 節's side; `句.md`
  and `旬.md` are unchanged. 義 loses 税 (`義.md` line 14); `税.md` is unchanged. The original packet's `repo\kanji\` holds
  all 1,176 cards of the reviewed snapshot; only the six cards above differ from it. Over all 1,176 cards: only 節 lists 句
  or 旬 in `quiz_exclusions`; no card lists 句 or 旬 in `distractors`; 句 and 旬 list neither each other nor 節; and
  neither 義 nor 税 lists the other in `quiz_exclusions` or `distractors`.
