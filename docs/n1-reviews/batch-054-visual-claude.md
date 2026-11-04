**Snapshot:** Frozen signed HEAD 73593c32886b12443c6da65b9b6c2e393ba01ace; the coordinator reports teaching unchanged from 4fb51498f6912169499456031380ce2353373397, with an empty teaching diff. Without shell/Git I couldn't verify the SHA, the diff or the 302-fixture/envelope identity myself. The current `kanji\且.md` and `words\且つ.md` read as identical to the text I originally reviewed. Uncommitted contributor evidence was not inspected.

**Scope:** Claude Opus 5.5 (claude-opus-5.5), same session 1bed2f69. This is a dependent visual follow-up, not a blind review. It covers both teaching files for correctness, scoped coverage and comprehensibility, now with on-screen evidence.

Reads, all serial, one call per response, 24 calls in total:
1. The task prompt.
2. My original report, `batch-054-initial-claude.md` (it matches what I returned).
3. `kanji\且.md`, complete.
4. `words\且つ.md`, complete.
5. `N1Batch054NativeTest.kt` lines 210–300.
6. `N1Batch054NativeTest.kt` lines 301–380.
7–24. The 18 PNGs, one per call, in the order listed in the task.

All PNGs came back at 900×2000, apparently downscaled from 1080×2400; text was still legible.

**Verdicts:**
- `kanji\且.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- `words\且つ.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

**Inherited text judgments (unchanged from my original review):**
- Readings ショ/ソ/ショウ/か.つ are in source order, with on'yomi practice off and only か.つ practised.
- ショ is labelled recognition-only, with archaic 苟且 こうしょ as its example.
- ソ and ショウ are honestly marked as having no allocated example.
- 苟且 かりそめ is treated as a separate whole word, not evidence of a ソ reading.
- 5 strokes, radical 一 (no. 1), and the mnemonic is labelled as not historical.
- One 且つ (かつ) supporting article, one link pair in two directions, nine direct quiz exclusions, and no word level inferred from the kanji.
- Both examples are attested dictionary examples; the おもしろく and 必要かつ十分な + noun attachment notes are scoped as two frames, not a universal rule.
- The additive, parallel-action, substitution and noun-listing limits are all qualified.
- The text makes no comparative register claim or formal-only ban, so that claim stays unverified and correctly absent.

**Newly visible on screen:**
- **Font rows (font-pairs):** in Gothic, Mincho, Textbook and Brush, 且, 目, 日 and 助 each appear in a distinct style and are easy to tell apart. 且's extended bottom bar, 目's two inner bars and 日's single bar are clear, and 助's 力 is visible. 苟 appears as the same heavier fallback glyph in all four rows and is readable. I can't identify that font, and the four fonts lacking 苟 doesn't mean the glyph fails to display.
- **Article screens:**
  - The facts line, the labelled mnemonic and the 一 radical are visible (kanji-radical, kanji-mnemonic, backlink-kanji).
  - The "Scroll sideways" hint is shown above the readings table.
  - Practice/curation paragraph, Common words, the 目/日/助 notes, the "and" limit and sources are all visible (selected-reading, curation, connector-boundary).
- **Readings table:** it is wider than the screen.
  - Scrolled right (archaic-reading-fallback), the reading labels are cut off ("ョ", a blank for ソ, "ョウ", "つ"), and こうしょ breaks after し.
  - Scrolled left (mnemonic, radical and backlink screens), the qualification column is cut off ("Recognition o…", "wor…").
  - No single screenshot shows every cell. This is a layout limit, not an error in the teaching text.
- **Word article (word-additive, word-component):** both examples show readings, English translations and sources. The bold おもしろく and 必要かつ十分な + noun notes, the substitution and noun-listing limits, and the parallel-action note are readable. The lecture bullet runs to the right edge but wraps.
- **Quiz:**
  - **Stack:** N1 with 86 cards.
  - **Meaning:** the wrong answers shown were Japanese cedar, chicken and mosquito, not the authored 目/日/助, and none could pass as "moreover; also"; the "Correct!" feedback screen is shown.
  - **Reading:** a kun'yomi question offered まつ, たつ, かえで and かつ, with no on'yomi options; かつ was marked correct.
  - **Reading feedback:** the line shows the full lookup readings ショ、ソ、ショウ、かつ.
- **Drawing:**
  - Five numbered strokes in an ungraded trace while the handwriting model was still downloading.
  - The feedback says "Practice only… not graded" and was checked by stroke shapes only because the model was unavailable.
  - A recall miss showed "Here is the kanji" with a blank drawing next to the five-stroke model.
- **Duplicate screenshots:** kanji-curation is pixel-identical in content to kanji-selected-reading, and backlink-kanji matches kanji-mnemonic apart from the timestamp. I treated these as 18 views, not independent evidence.

**Supplied operational results (not tests I ran):** the fixture code confirms the scripted route. It asserts:
- the full ordered readings and the curation lists;
- 5 strokes;
- correct key かつ with no ショ/ソ/ショウ options;
- a saved Good reading grade and a saved Draw grade on Next;
- offline operation and one archive request.

The pass/timing/ADB results, the ContentSync counts, the hash/ZIP/budget checks, the heap/process cleanup and the reconfirmation of the earlier 301 run are as supplied by the coordinator. I did not see or re-run them.

**Findings:** None. The table clipping and wrapping come from the app's horizontal-scroll layout, and the "Scroll sideways" hint is shown. Every teaching cell is legible in at least one screenshot, apart from the ソ/ショウ qualification tails and the か.つ label, which are partly cut off in the captured views. That doesn't establish a learning defect in the teaching files.

**Optional:** My five original suggestions stand unchanged and are not adopted. As app-layout polish outside these files, the readings table could wrap or stack on narrow screens so labels and qualifications don't clip.

**Limits:**
- **Not shown on screen:** the screenshots don't cover every cell or column, so this is not a full-article certification. I didn't view the extra source-only table, whole-word boundary, look-alike, lecture, attachment or word back-navigation captures named in the fixture.
- **Text reads:** fixture lines outside 210–380 were not read. The ContentSync, hash and ZIP figures and the APK/emulator results are supplied, not observed by me.
- **Drawing:** there is no ML Kit handwriting recognition, no human recall success, and no negative-geometry or reverse-order evidence.
- **Device coverage:** API 35 emulator only, default font scale. There was no enlarged text, other API level or physical phone, and no native-speaker check.
- **Not performed:** current-main integration, publication, general-release and whole-set acceptance.
- **Process:** this session made no parallel calls and used no shell, search, edits or delegation. My original blind review had one recorded parallel overlap. This follow-up is not blind or a fresh source retrieval, and it is not a model benchmark.
