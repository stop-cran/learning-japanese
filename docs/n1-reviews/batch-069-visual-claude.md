In the 16 screenshots I viewed, 儒, 儒教 and the 儒教 line added to 教 display correctly and are readable on the emulator. I found no defects; every verdict is CLEAN. This rests on my viewing the images, not on the test's selectors or assertions. The lexical judgments are carried over unchanged from my initial report.

**Snapshot:** Teaching content unchanged from f5061bcdf101f8eba5729b21f222b57821df9a38. Supplied evidence HEAD 41390d7019b58dd8be521388865164d706b2b34d; imported content e245739783dbc2ebe33ee164b8cfa718d670551b. I had only the `view` tool, so I could not check any of these SHAs in Git. I made no edits.

**Scope:** I'm Claude Opus 5.5 (claude-opus-5.5), one `view` call per response throughout.
- **Text read in full:** the task file, my initial report, `儒.md`, `儒教.md`, `教.md`, the test fixture in ranges 1-120, 121-240, 241-360, 361-480 and 481-529, `instrumentation.txt` and `n1-069-article-route.json`.
- **Images viewed, one each (16 of 46):** font-pairs, kanji-01, kanji-11, word1-02, word1-07, word1-new-kanji-backlink, word1-legacy-backlink, component1-19, curated-On-question, curated-On-feedback, meaning-question, meaning-feedback, drawing-trace, drawing-feedback, drawing-recall-feedback, selection.
- **Deviations:**
  - The fixture names `component1-19` after the 教える bullet and gives the 儒教 bullet its own capture, `component1-23`. The `component1-19` image still shows the changed 儒教 line fully, so the check holds.
  - Images came back at about 900×2000, scaled down from 1080×2400.

**What the images show:**
- **Fonts:** all four production rows (Gothic, Mincho, Textbook, Brush) render every character with no blank or replacement boxes. 儒 is distinguishable from 需 by its left 亻; 儀/僧/優 have visibly different right sides; 人 and 亻, 教 with 子/攴/攵, and 考/校/木 are all legible. In Mincho and Textbook, 攴/攵 (and 亻 in Textbook) appear in a bolder fallback face. That is a style difference, not a defect.
- **儒 card (kanji-01, kanji-11):**
  - The facts line shows 16 strokes and 人 (as 亻, no. 9), and the mnemonic is labelled as invented.
  - The Readings table appears in two sideways scroll positions. Between them the whole row is visible, but no single position shows all three columns.
  - All three Notes bullets are fully visible, including the learned-person qualification and the 儒学 overlap note.
  - The final Metadata/Usage line is cut off in every 儒 card capture I saw.
- **儒教 article (word1-02, word1-07):** every section is visible, including both example sentences with kana and translations, the ジュ + キョウ formation, linked 宗教 and 思想, and the sources line.
- **Links, all four directions:**
  - 儒 → 儒教 and 教 → 儒教: the linked 儒教 line is visible in both cards.
  - 儒教 → 儒: tapping 儒 opens the card (new-kanji-backlink).
  - 儒教 → 教: 教 is a visible link (legacy-backlink).
- **Reading quiz:** the options were ジュ, ソウ, ジョウ and ギ. Only ジュ is a reading of 儒, and the feedback screen shows "Correct! — on'yomi" with ✓ジュ.
- **Meaning quiz:** the options were 儀's and 僧's titles, "frugal; thrifty" and the correct title. The authored distractor 優 was not offered; none of the wrong choices is a defensible meaning of 儒.
- **Drawing:**
  - The template has 16 numbered strokes matching 儒.
  - The feedback says the attempt is ungraded and that only stroke shape was checked because the handwriting model was unavailable. The "Downloading the handwriting model" text does not show a successful download.
  - The "I don't remember" screen shows the reference after a deliberate miss.
- **Selection:** "N1 · 101 cards".

**What the test itself reported (I did not run it):** the log shows "OK (2 tests)" in 158.188 s. The route file shows offline mode, a single import of 1,081 kanji and 5,038 words with no problems, content version 83ed94552dd1a9ce, full and quiz on'yomi ジュ, no kun'yomi, and 16 injected strokes. The test pressed Back before Next on the meaning feedback, so no new meaning grade was recorded. The drawing results are not handwriting recognition or a person recalling the kanji.

**Verdicts:**
- **儒:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **儒教:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **教 (added 儒教 line only):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:** None.

**Optional:**
- In the small "Correct strokes" panel, stroke numbers 5/7 and 11/13/15 overlap (drawing-feedback, drawing-recall-feedback). This is app display polish, not a content issue.
- Carried over from my initial report: 儒者 じゅしゃ or 儒学者 じゅがくしゃ could illustrate the "Confucian scholar" half of the title.

**Limits:**
- **Unviewed content:** 30 of the 46 screenshots, the 儒 card Metadata/Usage line, the other table scroll positions, and every other quiz draw, including random and larger pools.
- **Not identified:** which fallback fonts actually rendered the text, and which card supplied "frugal; thrifty". The rendering probes only show glyphs are non-blank and distinct.
- **Not tested:** a physical phone (this was an emulator, API 35, font scale 1), native-speaker judgment, real handwriting recognition, general release, the whole N1 set, current main, or publication. Displaying the curated reading requires Android f9b59a2 or later.
- **Not re-run:** no fresh dictionary lookups or native execution by me; earlier attempts and their failures are as supplied.
