**Snapshot:** f59c65fde644ed36958d74495da59a66c1d82570. I reviewed only the frozen draft supplied in the packet. I did not inspect the working tree.

**Scope:**
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`).
- **Read:** One `view` call with `forceReadLargeFiles=true` and no range read `C:\Users\stop-\n1-kanji-workspace\control\batch-086-initial-packet.txt`. The output showed no truncation marker and ended in the closing "MECHANICAL SCOPE / ACCEPTANCE LIMITS" section. The tool did not report byte or line counts, so I could not confirm 215474 bytes / 4300 lines.
- **New articles:** I read all of `kanji\凡.md` (lines 1–68) and `words\凡例.md` (lines 1–54).
- **Diffs:** I checked all six reused diffs.
  - Words: 平凡, およそ, 全て.
  - Kanji: 平, 例, 全.
- **Comparison articles:** I used 丸, 九, 凹, 常, 般, 毎, 各, 皆, 総, 例(word), おおよそ, 栞, 注, 説明, 解説, メモ, 筆記, はじめに, 概論 and 鍵 only for their actual titles and passages.
- **Dictionary data:** I counted 71 distinct JMdict entries (49 + 12 + 10) and seven KANJIDIC2 character records (凡, 平, 例, 丸, 九, 凹, 全). The packet also contained KanjiVG data, stroke JSON, input metadata and Daijisen/Nikkoku text supplied by the coordinator.

**Verdicts:**
- **kanji\凡.md:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- **words\凡例.md:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- **Six reused diffs:** all CLEAN.
  - 平凡 link: CLEAN.
  - およそ link: CLEAN.
  - 全て 凡て alias: CLEAN.
  - 平 bullet: CLEAN.
  - 例 bullet: CLEAN.
  - 全 link to 全て: CLEAN.

Points I verified:
- **Readings and order:** on ボン, ハン and kun およ.そ, おうよ.そ, すべ.て match KANJIDIC2 exactly, in the same order.
- **Selected on readings:** ボン is linked to 平凡 and ハン to 凡例. Daijisen supports both assignments: ボン(呉) lists 平凡 and ハン(漢) lists 凡例.
- **Kun questions:** `quizKunyomi: []` turns them off while keeping all three kun readings in the metadata.
- **Raw おうよ.そ:** It stays source-only and unverified. It is not changed to おおよ.そ and not called a typo.
- **凡そ:** JMdict 1523450 gives 凡そ with ichi1 priority and marks the word as usually written in kana.
- **凡て:** JMdict 1595730 marks it as a rarely used kanji form. Both articles say the spelling is rare, not the pronunciation.
- **Radical, strokes, labels:** Radical 几 is no. 16 and the stroke count is 3, matching KANJIDIC2, KanjiVG and the stroke JSON. The mnemonic is labelled as a modern-shape aid. N1 is labelled a community list. The card does not deny a phonetic component.
- **凡例 reading and senses:** はんれい matches JMdict 1523690, sense 1 (book notes and usage guide) and sense 2 (legend on maps, drawings, etc.). 判例 is correctly kept apart (JMdict 1478740, law).
- **Example sentences:** 凡例を読む and 地図の凡例で記号の意味を確認 are natural. Their translations are accurate.
- **Wrong-answer kanji:** The displayed titles are "round; circle" (丸), "nine" (九) and "concave; sunken" (凹). None overlaps "commonplace; mediocre". 丸's "whole" sense does not appear in its displayed title.
- **Eight exclusions on 凡例:** 注, 説明, 解説, メモ, 筆記, はじめに, 概論 and 鍵 are each justified by an actual title overlap. Examples are "explanatory note", "introduction" and "key". All targets exist. They are direct pairs only.
- **Reciprocal links:** All seven pairs (14 directions) are present with correct relative paths and readings: 凡↔平凡, 凡↔凡例, 凡↔およそ, 凡↔全て, 平↔平凡, 例↔凡例, 全↔全て. The 凡/平凡 pair is the one new link added to existing text. No unneeded baseline edits were found.
- **Levels and IDs:** 凡例 has no inferred word level. 平凡 keeps N2, and およそ and 全て keep N3. IDs and original exclusions are unchanged.
- **Neighbouring kanji cards:** 常, 般, 全, 毎, 各, 皆, 総 and 平 each have three curated wrong-answer kanji.

**Findings:** None proved. No actionable defect was established.

**Hypotheses (not established defects):**
- **Low; quiz safety:** 栞 ("bookmark; guidebook") has no exclusion with 凡例. JMdict glosses 凡例 as "usage guide", but the displayed 凡例 title does not use that wording, so a learner is unlikely to accept "guidebook". Confidence is low.
- **Effect of the kanji-based level fallback:**
  - **Old apps:** They ignore a word's `jlpt` and use the hardest known kanji instead. On those apps, 平凡 will now count as N1 because the 凡 card is N1.
  - **Current apps:** 凡例 has no word level, so its level falls back to N1 from 凡.
  - **Old APKs:** They also ignore the quiz-reading lists, so they will ask all readings, including the source-only おうよ.そ.
  - These follow from the documented app behaviour rather than from an error in the articles.

**Optional:**
- `kanji\凡.md:59-61`: "position of the dot" fits 丸, but 九 has no dot. A brief clause could make the difference explicit.
- `words\凡例.md:15`: Daijisen's 編述の方針 (editorial policy) could be named. 例言 (れいげん), a synonym in both supplied Japanese dictionaries, could be mentioned.
- `kanji\凡.md:37`: JMdict 1415050 also lists 凡そ as a rare spelling of おおよそ, which could be noted.
- 凡人, 非凡 and 凡庸 could be mentioned without links.

**Limits:**
- I did not independently check Git, upstream sources or the web. The dictionary page text was extracted by the coordinator.
- There is no evidence on native-font rendering, stroke drawing, the app UI, phone display, live or custom quiz pools, native-speaker judgement or measured learning effect.
- I could not check that the 凡 title is unique across all kanji cards.
- The おうよ.そ modern usage remains unverified.
