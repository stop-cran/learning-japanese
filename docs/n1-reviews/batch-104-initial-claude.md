**Snapshot:** 636b995e8cba91b5fde0d31369655a50fd8708ce. Only the two new files were reviewed; there are no changed reused passages.

**Scope:** I made one `view` call with `forceReadLargeFiles=true` on `batch-104-initial-packet.txt`. The output had no truncation marker and ended at `docs/jlpt-levels.md` line 23. Model: Claude Opus 5.5 (`claude-opus-5.5`). Articles reviewed: `kanji\劾.md` (lines 1–47) and `words\弾劾.md` (lines 1–38). Evidence used: the 31 comparison articles, JMdict and KANJIDIC2 records, KanjiVG and stroke data, public dictionary texts and receipts, `KanjiReadings.kt` lines 13–69, and the repository rules included in the packet.

**Verdicts:**
- **劾.md:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- **弾劾.md:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility NEEDS FIX.

**Findings:**

1. **Minor; comprehensibility; `words\弾劾.md:30`.**
   - **Problem:** The sentence "Praise, acquittal and removal from office are not one interchangeable antonym of 弾劾" lists removal from office as if it were a possible opposite. Removal is a possible result of impeachment (罷免 in Daijisen sense 2), not an opposite. A learner may mistake a result for a contrast. Line 36 correctly says reporting 弾劾 does not mean removal happened.
   - **Fix:** Say that praise or acquittal can contrast in context, and that removal from office is a possible outcome, not an antonym.
   - **Evidence:** Daijisen 弾劾 sense 2 (罷免または処罰する手続き) and the encyclopedia examples (Clinton acquitted, Nixon resigned).
   - **Confidence:** Medium.

**Checks with no defect found:**
- **Metadata:** These match KANJIDIC2: ガイ as the only reading, no kun-reading, 8 strokes, radical 力 (19) on the right, grade 8 and level 1. The level is labelled "community list", not an official syllabus. The word card correctly has no `jlpt` field (no inferred level).
- **Quiz reading:** `quizReadings(On)` gives [ガイ] (match key がい). The reading row has its own link to 弾劾.
- **Readings in 弾劾:** だんがい = ダン (弾) + ガイ (劾), confirmed from each character's record, not just the kana. JMdict 1419430 has no spelling or reading restrictions. Both senses are noun, する-verb and transitive.
- **Both uses covered:** The misrule example is the attested Daijisen example. The judges example is authored but natural. Kana, translations, を, the Nの弾劾について pattern and the polite, past and negative forms are correct.
- **弾 identity:** The article uses 弾's "expose wrongdoing; censure" sense (Daijisen sense 3 lists 弾劾). It correctly does not link to `words\弾.md` (たま, bullet).
- **No overclaiming:** The text does not claim guilt, fairness, completed removal, rules shared by every country, frequency or etymology. The mnemonic is labelled as a mnemonic, and no phonetic or origin claim is made, even though KanjiVG and 字通 mark 亥 as phonetic.
- **Wrong options (刻, 効, 努):** None of their labels or sense lists overlaps censure.
- **Kanji exclusions:** All five are justified. 責 overlaps censure. 査, 調 and 究 overlap "criminal investigation". 詰 has the secondary meanings reprove/rebuke.
- **Word exclusions:** 批判, 責める, 攻撃 (sense 2 includes "denunciation") and 叩く (sense 2) are justified. 批評, 評論 and 切る (sense 12, "criticize sharply") are conservative but harmless.
- **Links:** The 劾↔弾劾 pair is linked in both directions, and the packet's teaching diff shows only the two new files (no baseline edits).
- **Strokes:** The stroke JSON has 8 strokes, consistent with the KanjiVG paths.

**Hypotheses (not proven defects):**
- **Missing word exclusion:** 叱る ("to scold; reprimand") against 弾劾 ("censure"): "reprimand" is close to English "censure". Low to moderate risk.
- **Missing kanji exclusion:** 偵 ("spy; covert investigation") is in the same N1 pool and overlaps 劾's investigation sense. Low risk.
- 罪, 処, 絞る, 恨む, 意見, 不正 and 裁判官 looked low-risk.

**Optional:**
- `劾.md:34`: "selected for practice as がい" is the internal match key. The display function returns on-readings in katakana (ガイ); I did not see the quiz screen code.
- `劾.md:34`: "The source supplies no kun-reading" could name KANJIDIC2, because the cited kotobank page (字通) lists せめる・しらべる.
- `劾.md:45`: "standalone verb" suggests 劾 is a verb at all; it is not.
- `劾.md:26`: the mnemonic's "claim" is not tied to anything visible in the 亥 shape.

**Limits:**
- I cannot independently confirm the packet's 280103 bytes or 5163 lines, only that the output was not marked as truncated. I saw no font character-map (cmap) evidence in the output; the 刂 font point comes only from the task statement, and missing cmap entries are not evidence of rendering failure.
- I did not check the quiz screen code, `confusable-words.md`, title uniqueness across the whole corpus, or every possible future quiz pool.
- No independent Git or upstream checks were made. Native-speaker and font review, rendering, drawing, UI and phone checks, and measured learning effectiveness are all outside this review.
