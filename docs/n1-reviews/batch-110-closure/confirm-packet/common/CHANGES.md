# Batch 110 revision: what changed from 453af714 to 10d79652

Revised snapshot: `10d7965266b69ed81703ab69f20cff873a0526e9`, a child of the reviewed snapshot
`453af714d56aa573204d477ff863cb4da756b4c3`. Nothing is published.

- All 15 kanji cards changed: every long Meaning and Readings paragraph was split into shorter paragraphs, and ten cards
  (器, 基, 価, 嫌, 応, 激, 級, 素, 縮, 騒) also have changes of wording, exclusions or notes. 張, 仮, 統, 整 and 暖 are
  paragraph breaks only: their text is identical to the reviewed card once whitespace is normalised.
- One word article changed: `words\応援.md` (revised text in `snapshot\words\応援.md`). The other 92 word articles of the
  batch, all 15 stroke files and all titles are unchanged.
- Front matter changed only in `quiz_exclusions` (line 14) of 嫌, 応, 級 and 素. `distractors`, titles, tags and metadata
  readings are unchanged on all 15 cards.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Every quoted title in the new text was checked by script against the linked card's real `title:` (109 links on
  changed lines, 0 unresolved or mismatched; see `checks\link-targets.tsv`).

| Card | Changed lines | Change |
| --- | --- | --- |
| 張 | 23-27, 40-44 | Paragraph breaks only; the wording is unchanged. The opening is three paragraphs (the common words; the Daijisen senses and counters; the verb 張る) and the readings are three (compound breakdowns; the voicing in 張り切る, 欲張り and 引っ張る; the Joyo table and practice selection). |
| 仮 | 23-25, 38-42 | Paragraph breaks only. The Daijisen senses are their own paragraph (25); the readings are the compound breakdowns (38), the Joyo table and practice selection (40) and 虚仮 (42). |
| 価 | 23-25, 37-41 | One correction at 37: "In 価格, 格 supplies カク, so 価 is か in both syllables of かかく" is now "In 価格, 価 is read か and 格 supplies カク." Otherwise paragraph breaks: the Daijisen senses (25); the readings are the breakdowns (37), the Joyo table and あたい (39) and the suffix か, ケ and practice selection (41). |
| 器 | 23, 25-29 | The opening is split (word list 23; Daijisen and JMdict senses 25). New paragraph 27: the Joyo table also prints an older form of 器 in round brackets, with a dot in its centre like 犬; this card teaches the standard form, whose centre is plain 大. The mnemonic (29) is rebuilt around [大](大.md), "big, large," with no dot ("one big serving bowl"); the disclaimer now says 口 or 大; the link to the 犬 card is gone. |
| 基 | 23-25, 37-47 | The opening (23) is shortened to 基礎 and 基本 and ends "The other common words are listed below." Every word link removed from it is still present in the card's Common words section (and, in the Readings table, lines 33-34). The senses are their own paragraph (25). The readings are six paragraphs (37-47); no sourced reading or qualification was removed. |
| 嫌 | 14, 23-25, 39-43, 58 | `quiz_exclusions` gains 怪 (now `[憎, 疑, 怪]`). "in some older compounds suspecting it" is now "in a few compounds suspecting it". The Daijisen senses are their own paragraph (25); the readings are three paragraphs (39, 41, 43). Note 58 is rewritten: 憎 shares the KANJIDIC2 glosses "hate" and "detest"; 疑 and 怪 overlap the Daijisen sense of suspecting and the title word "suspicion"; all three are kept out of the quiz options. |
| 応 | 14, 23-25, 38-42, 44, 60-61 | `quiz_exclusions` loses 募 (now `[答, 承, 受, 適, 対]`). The まさに row (38) now says JMdict marks まさに as usually written in kana alone. At 40, "In 応用, 用 supplies ヨウ, which is why ヨウ appears in the word without being a reading of 応" is now "In 応用, 応 is read オウ and 用 supplies ヨウ." The opening is split (23, 25) and the readings are three paragraphs (40, 42, 44; the wording of 44 is unchanged). Note 60 no longer lists 募. New bullet 61: 募 is a contrast, not an overlap (in 応募 おうぼ, 募 is the recruiting side and 応 the responding side), so it is not kept out of the quiz options. |
| 整 | 23-25, 37-41 | Paragraph breaks only. The senses are their own paragraph (25); the readings are three paragraphs (37, 39, 41). |
| 暖 | 38-42 | Paragraph breaks only. The readings are three paragraphs (38, 40, 42). |
| 激 | 23, 25-27, 36-40 | The mnemonic (27) is corrected: 氵 at the left, [白](白.md) above [方](方.md) in the middle, 攵 standing at the far right; 方 and 攵 together make [放](放.md), "release"; the disclaimer covers 白, 方 or 放. The opening is split (23; the Daijisen and JMdict senses at 25) and the readings are three paragraphs (36, 38, 40). |
| 級 | 14, 23-27, 37-41, 55-56 | `quiz_exclusions` loses 校 (now `[位, 格, 段, 等, 階, 組]`). The opening is three paragraphs (23, 25, 27) and the readings are three (37, 39, 41; the wording is unchanged). Note 55 no longer lists 校. New bullet 56: 校 is a contrast, not an overlap (学校 がっこう is the school itself, a 学級 がっきゅう is one class within it), so it is not kept out of the quiz options. |
| 素 | 14, 23-25, 37-45, 61, 63 | `quiz_exclusions` gains 料 (now `[原, 単, 純, 具, 材, 料, 要, 元, 本]`). The opening (23) is shortened in the same way as 基; every word link removed from it is still present in the card's Common words section. The Daijisen ソ and ス senses are their own paragraph (25). The readings are five paragraphs (37-45), including a new paragraph (39) on 素敵 すてき and 素晴らしい すばらしい: JMdict marks both spellings as ateji, so they help you recognise 素 but do not show its meaning. Note 61 adds 料, "materials, fee," to the ingredient and material overlap. Metadata (63) adds JMdict entries 1397350 and 1397300. |
| 統 | 23-25, 36-38 | Paragraph breaks only. The senses are their own paragraph (25); the readings are two paragraphs (36, 38). |
| 縮 | 23-25, 40-42, 56 | Paragraph breaks (senses 25; readings 40 and 42; the ちじむ sentence is unchanged). Note 56: "It is read as a whole word, with 縮 as ちり ..." is now "In this word 縮 is read ちり, which is not one of the readings above." |
| 騒 | 23-25, 38-42, 56 | Paragraph breaks (senses 25; readings 38, 40 and 42). Note 56 gets the same rewording for さい. |
| `words\応援.md` | 32-33 | The stale clause "neither currently has a kanji card here" (応 now has a card) is replaced: "Both written characters belong in the word, though 援 does not have a kanji card here." |

## Paragraph structure (comprehensibility)

Prose paragraphs of `## Meaning and origin` and `## Readings` in each card, reviewed snapshot -> revised snapshot. Tables,
bullets and headings are excluded, link destinations are removed, and words are whitespace-separated tokens (a rough
measure for text that mixes English and Japanese).

| Card | Paragraphs | Longest paragraph (words) |
| --- | --- | --- |
| 張 | 3 -> 7 | 175 -> 81 |
| 器 | 3 -> 5 | 144 -> 94 |
| 素 | 3 -> 8 | 244 -> 82 |
| 応 | 3 -> 6 | 179 -> 74 |
| 仮 | 3 -> 6 | 172 -> 92 |
| 基 | 3 -> 9 | 264 -> 88 |
| 価 | 3 -> 6 | 170 -> 86 |
| 激 | 3 -> 6 | 135 -> 85 |
| 嫌 | 3 -> 6 | 152 -> 76 |
| 縮 | 3 -> 5 | 127 -> 72 |
| 騒 | 3 -> 6 | 154 -> 88 |
| 統 | 3 -> 5 | 114 -> 76 |
| 級 | 3 -> 7 | 189 -> 94 |
| 整 | 3 -> 6 | 142 -> 85 |
| 暖 | 3 -> 5 | 175 -> 99 |
| All 15 | 45 -> 93 | 264 -> 99 |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on the 15 cards and the 93 word articles edited by the batch: 0 errors, 17 warnings. All 17
  are the same warning, on word articles: the Dictionary line cites no JMdict id, or there is no Dictionary line. They are
  not claims introduced by this revision.
- `unittest.txt`: 431 tests, OK. `validate.txt`: 0 errors. `budget.txt`: content archive budgets met.
  `vocabulary.txt`: vocabulary coverage check passes. `manifest.txt`: `manifest.json` regenerated and committed.
- `jvm.txt` and `jvm-readings.txt`: the Android app's JVM tests that read the real content (`RealContentTest` 3 tests,
  `RareHanTest` 1 test, `KanjiReadingsTest` 14 tests) pass with no skips.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether the
  gloss quoted after the link equals that title.
- `quiz-safety.txt` and `reading-options.txt`: see the next section.

## Quiz mechanics the changes rely on

- `tools\validate.py` rules (all pass): `quiz_exclusions` has no duplicates, no self, every entry has a card, and **no
  entry may also be one of the same card's `distractors`**.
- Meaning quiz: the app's `QuizBuilder` is in `evidence\QuizBuilder.kt`: options are the curated `distractors` in order;
  any candidate that is excluded against the target or an already chosen option is skipped; `excluded(a, b)` is true if
  **either** card lists the other, so a pair needs to be listed on one side only (the repository lists each pair once).
  Only when fewer than three curated distractors survive are other cards added (tag-similar first).
- `checks\quiz-safety.txt` prints the four meaning options now shown for each of the 15 cards (the first option is the
  correct title). The "reading ... wrong options from distractors N/3" lines under each card count curated slots for the
  reading prompts, not the options themselves. Lines 48-59 list 11 existing cards outside this batch (人 休 何 入 出 口 女
  日 月 男 買) whose options use the tag-similar fallback; they are not part of this review.
- Reading quiz: `quiz_exclusions` affect only the meaning quiz. Reading prompts are built by `KanjiReadingQuiz` in
  `evidence\KanjiReadings.kt`. Each curated `distractors` card offers one random usable reading of the asked kind (skipped
  if it is empty, excluded or a duplicate); the remaining slots are filled from the other cards' readings, those closest to
  the target reading first (length within one kana, same first or same last kana), then any other readings.
  `excludedKeys(target)` is every on and kun reading of the target card plus the sound-change variants made by
  `ReadingOptions.mutations` in `evidence\Words.kt`.
- `checks\reading-options.txt` is the author's audit of every reading prompt of the 15 cards. For each prompt it lists the
  excluded keys, what the curated option cards offer, the fallback candidates by closeness tier, whether a reading that is
  attested for the card but not listed in its metadata (KANJIDIC2 name readings, or readings given in the card text) can be
  offered as a wrong option, and a simulation of 200 seeded draws. Result: "0 problem(s)". It cannot show the exact draws:
  the pool is every card in `kanji\` (1,161 cards, the largest possible pool, while the app draws from the cards the learner
  has studied), fallback options are random within closeness tiers, and the audit's random generator is not the app's, so
  it reports candidate sets. Three "note" lines (the 張 prompt は.る with わり, the 基 prompt もと with とも, the 騒 prompt ソウ
  with さい) record an unlisted reading that other cards offer only from a lower closeness tier, so the fallback cannot
  reach it while higher tiers are available. One informational case: for the 応 prompt オウ, the KANJIDIC2 name-only
  reading お can appear among the wrong options (offered by 和, 悪 and 汚; 3 of 200 seeds;
  `checks\reading-options.txt` lines 82-84).
- Exclusion changes in this revision: 応 and 募 and 級 and 校 are no longer excluded (they are described as contrasts in
  the notes); 嫌 now lists 怪 and 素 now lists 料, each on one side only (`怪.md` and `料.md` are unchanged).
