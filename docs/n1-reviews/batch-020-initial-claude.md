**Snapshot:** commit `8fb440f492c7d66df29a65b029286b039f6a34b6`. I reviewed only the committed teaching text. No uncommitted changes were included, and I made no edits.

**Scope:** Model: Claude Opus 5.5. Facets: correctness, scoped coverage and how readable the text is on a phone screen.
- **Teaching files:** I read all of `kanji\蝶.md` and `words\蝶.md`.
- **Instructions:** I read `.github\copilot-instructions.md` lines 1–160 and 161–218, `content-structure.instructions.md`, `docs\content-format.md` lines 42–148 and `docs\jlpt-levels.md` lines 1–110.
- **Metadata:** I read all of `batch-020-input-metadata.json`, including the raw KANJIDIC2 element.
- **Dictionary packets:** I read all 96 families in full.
  - Main packet: lines 1–1588 in eight ranges, 81 families.
  - Comparisons: lines 1–232, 7 families.
  - Notes: lines 1–191, 4 families.
  - Supplement: lines 1–132, 4 families.
- **Comparison cards:** kanji 葉, 世, 採 and 虫; words 虫, 蛍, 蚊, ネクタイ and 採る.
- **Searches:** `docs\confusable-words.md` for 蝶, 虫, 蛍, 蚊, 蛾 and ネクタイ (no matches). I also checked that the linked files exist (木, 虫, 世, 葉, 採, 蛍, 蚊, ネクタイ).
- **Web source:** Kotobank page fetched as simplified markdown. I read the Digital Daijisen and Seisenban (Nihon Kokugo Daijiten) bodies.

**Verdicts:**
- `kanji\蝶.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- `words\蝶.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

Basis:
- **Metadata:** Matches KANJIDIC2: one reading, チョウ (on), no kun-readings, 15 strokes, radical 142, grade 9. Only チョウ is selected for the quiz, and its row links to the word article.
- **Reading and spelling:** Daijisen supports the on-reading チョウ, the historical kana テフ and the name-use (人名用漢字) status. JMdict 1429010 supports ちょう and チョウ.
- **Compounds:** JMdict supports 蝶々 (ちょうちょう / ちょうちょ), 蝶ネクタイ (bow tie) and 蝶結び (bow; bowknot). The reading ちょうつがい is restricted to the spelling 蝶番, which matches the card. Daijisen lists 蝶番 as a hard-to-read word.
- **胡蝶:** JMdict marks it as a poetic term, as the article says.
- **Example sentences and translations:** Natural; the note on singular versus plural is accurate.
- **No word level:** The word article has no `jlpt` field, so no vocabulary level is inferred from the N1 kanji.
- **Quiz distractors:** leaf; world, generation; pick; collect; adopt. None of these could reasonably be accepted for "butterfly." Leaving out 虫 ("insect; bug") and excluding the 虫/蝶 word pair is justified.
- **Links:** The kanji card and word article link to each other.
- **Mnemonic:** Labelled as a memory aid, not etymology. "世-like shape above 木" fits the modern shape.

**Findings:** None.

**Optional:**
1. In `kanji\蝶.md`, the 葉 note could say that 葉 contains the same 世-over-木 shape under its plant top. That shared part is the actual source of confusion.
2. "grade-9/name-use" could be shortened to "name-use (jinmeiyō)", since learners may not know what "grade-9" means.
3. `words\蝶.md` could cite JMdict 1197760 for 蛾 among its sources.
4. Unchanged `words\虫.md` mentions 蝶 without a link; a link to the new article could be added later.
5. Things the cards leave out, which are acceptable for this scope:
   - Seisenban records the old native name かわひらこ.
   - Daijisen and Seisenban record a family-crest (紋所) sense.
   - JMdict records the reading ちょうばん for 蝶番 and a "joint" sense for ちょうつがい.

**Limits:**
- **Web source:** The 字通 and 動植物名よみかた辞典 sections came back with headings only. I did not read raw HTML.
- **Search scope:** I searched only part of the confusable-pairs list. I did not check every word title in the deck for semantic overlap.
- **App behaviour:** I did not check the app's fallback choices or larger quizzes.
- **Device testing:** This was a text-only review, with no native/phone or font checks. Android, combined-main, CI, public ZIP and physical-phone checks remain outstanding.
- **Process deviation:** During setup I made one parallel batch of three reads: `content-structure.instructions.md`, `content-format.md` 42–148 and `jlpt-levels.md` 1–110. Every other step was a single serial call.
