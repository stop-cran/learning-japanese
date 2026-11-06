## Turn 1: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-visual-source-packet.txt

**Resource 1 of 32:** `batch-083-visual-source-packet.txt`, read in full with one `view` call. No truncation marker and no denial. These are notes on this resource only; I am not giving a verdict yet.

- **Teaching text:** The three new articles match what I previously reviewed, with the same hashes. `凌.md` 187e…, `凌ぐ.md` aac06d… and `凌駕.md` df0994… are unchanged since the corrected-choice confirmation, and the only diff is still `distractors: [准, 冶, 冴]`. The comparison bodies 准, 冶, 冴, 冴える and 次 are also unchanged.
- **Supplied execution results (not reviewer-run, not pixels):**
  - **Run:** Attempt 578 reports both named tests passed (`OK (2 tests)`, two terminal successes), running on emulator-5580 (API 35, read-only, no network).
  - **Import and readings:** The route JSON records one archive request, 1,095 kanji, 5,052 words, zero problems, content version `6dfe6a1e287ce5df` and 115 N1 cards. 凌's full and selected readings are リョウ / しの.ぐ, with keys りょう / しのぐ.
  - **Meaning quiz choices:** The exact four options are 凌, 准, 冶 and 冴 with their titles, in both N1 and All, with no padding. The live question shows the same four.
  - **Links and drawing:** Two link pairs were followed in four directions with System Back. The drawing test used ten injected strokes, not human handwriting.
- **Font raster JSON:** It has 120 individual and 8 whole-word Paint probes. 冫, 夌, 阝 and 隹 have identical raster hashes across all four fonts. This is consistent with one shared fallback face for those components. It is not a defect in itself, but it does not identify that face or show readability. The fixture only checks that hashes are unique within each font.
- **New concern to check against the screenshots:** The final article tree shows a home screen with "Loading your cards…", "All · 0 cards" and disabled Start buttons. Yet the fixture asserted the stack was still `jlpt-n1` just before. This was probably printed after the scenario moved on, but I will compare it with the captured screens.
- **Coverage:** The artifact list contains 56 PNGs: 53 route or quiz captures and 3 font panels. That matches the stated 56 captures; I will not infer pixel content from it.

## Turn 2: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-curated-Kun-feedback.png

**Resource 2/32: `n1-083-corrected-curated-Kun-feedback.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized; all text was readable.

- **Screen:** "Kanji readings" with a Back link at the top left. The large 凌 renders clearly in a serif typeface: the two 冫 marks on the left and 夌 on the right are distinct, with no replacement box.
- **Feedback:** "Correct! — kun'yomi" in green. The four options are さえる, しおり, しか and ✓しのぐ, which is highlighted green.
  - None of the three wrong options is a reading of 凌.
  - さえる is 冴's kun reading, so it is a plausible lookalike distractor rather than an ambiguous one.
- **Answer line:** "endure; surpass: リョウ、しのぐ", followed by the Next and "I guessed" buttons.
- **Article preview below the buttons:**
  - Heading "凌 — endure; surpass".
  - "Strokes: 10 · Key (radical): 冫 (the two left-hand strokes, no. 15) · JLPT: N1 (community list)". The small 冫 renders.
  - The "Meaning and origin" text separates enduring/getting through from surpassing. It shows 凌ぐ (しのぐ) and 凌駕 (りょうが) as links, and states that 凌駕 means surpassing, not sheltering from bad weather.
  - The frame cuts off at the "Modern-shape mnemonic, not etymology:" heading. That is expected for a single frame, not missing content.
- **Defects in this frame:** none found. No blank glyphs, collapsed lookalikes or mismatch with the article text.
- **Not proven by these pixels:** the persisted reading key and the 2-of-2 Done count.

## Turn 3: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-curated-Kun-question.png

**Resource 3/32: `n1-083-corrected-curated-Kun-question.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable.

- **Screen:** "Kanji readings" with Back at the top left. It shows "Attempts left: 1" and a note that the total includes queued repeats.
- **Glyph:** The large 凌 renders clearly in a serif face. The two 冫 marks are separate from the 夌 on the right. There is no replacement box.
- **Question:** "Pick the kun'yomi", with four outlined options: さえる, しおり, しか and しのぐ. Below them is an "I don't know" link.
  - The options match the order in the feedback frame (resource 2), and none is selected yet.
  - Only しのぐ is a reading of 凌. さえる (冴's reading) is a plausible look-alike, not an ambiguous answer.
- **Attempts left:** "1" fits this being the second of the two reading questions. The pixels alone do not show the order of the on/kun questions.
- **Defects in this frame:** None found.

## Turn 4: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-curated-On-feedback.png

**Resource 4/32: `n1-083-corrected-curated-On-feedback.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable.

- **Screen:** "Kanji readings" with Back. The large 凌 renders in a gothic (sans-serif) face this time; resources 2–3 used a serif face. Both the two 冫 marks and 夌 are distinct, and there is no replacement box. A typeface change on its own is not a defect.
- **Feedback:** "Correct! — on'yomi". ✓リョウ is highlighted green as the first option. The other options are ジュン, ヤ and リュウ.
  - ジュン is 准's reading and ヤ is 冶's.
  - リュウ is a near-sound look-alike, but it is not a reading of 凌; the frozen source gives only リョウ. So none of the wrong options is ambiguous.
- **Answer line:** "endure; surpass: リョウ、しのぐ", with the Next and "I guessed" buttons.
- **Article preview:** identical to resource 2. It shows the heading, strokes 10, radical 冫 no. 15, N1 (community list), and the Meaning text that separates enduring from surpassing, with links to 凌ぐ and 凌駕. The frame cuts off at the mnemonic heading, which is expected for a single frame.
- **Defects in this frame:** none found.

## Turn 5: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-curated-on-kun-done.png

**Resource 5/32: `n1-083-corrected-curated-on-kun-done.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable.

- **Screen:** "Kanji readings" with Back, then "Session complete" and "2 of 2 answers correct."
- **Buttons:** a filled "Done" button and an outlined "Practice more" button. The rest of the screen is empty, as expected.
- **What the pixels show:** the 2 of 2 completion count, which fits the on and kun feedback frames (resources 2 and 4).
- **What they do not show:** persisted reading keys, logs, or which question came first.
- **Defects in this frame:** none found.

## Turn 6: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-curated-On-question.png

**Resource 6/32: `n1-083-corrected-curated-On-question.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable.

- **Screen:** "Kanji readings" with Back. It shows "Attempts left: 2" and the queued-repeats note.
- **Glyph:** the large 凌 is clear in a gothic face. The two 冫 marks are separate from 夌, and there is no replacement box.
- **Question:** "Pick the on'yomi". The options are リョウ, ジュン, ヤ and リュウ, in the same order as the on feedback frame (resource 4). None is selected yet, and "I don't know" is shown below.
- **Order of the two questions:** "Attempts left: 2" here, followed by "1" on the kun frame (resource 3), shows the on question came first. That is consistent with the 2-of-2 Done screen.
- **Defects in this frame:** none found. Only リョウ is a reading of 凌, so no option is ambiguous.

## Turn 7: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-drawing-feedback.png

**Resource 7/32: `n1-083-corrected-drawing-feedback.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable, including the stroke numbers.

- **Screen:** "Drawing" with Back. Header "凌 endure; surpass", then "Practice only: this attempt is not graded." and "Well drawn!" in green.
- **Drawing panels:** "Your drawing" shows the 10 injected strokes in blue. "Correct strokes" shows the reference in green, numbered 1–10.
  - Strokes 1–2 are the two 冫 marks, consistent with the stroke data and the radical note.
  - Strokes 3–10 form 夌.
  - The numbers are legible and the strokes do not collapse into each other.
- **Grading note:** "Graded by stroke shapes only (handwriting model not available)." This honestly shows that no handwriting model ran.
- **UI wording (not a scoped finding):** "Practice only: this attempt is not graded" next to "Graded by stroke shapes only" reads a little contradictory. This is app UI wording outside this batch, not article content.
- **Article preview:** heading, strokes 10, radical 冫 no. 15, N1 (community list), and the Meaning text. More of the "Modern-shape mnemonic, not etymology:" text is visible here: the two 冫 marks as drops beside the right-hand 夌 shape pictured as a barrier, "weathering the drops or getting beyond the…". The inline 冫 and 夌 render with no boxes. The text cuts off at the bottom edge, which is expected for a single frame.
- **What these pixels do not show:** these are injected reference strokes. They are not human handwriting, successful handwriting recognition or ML Kit.
- **Defects in this frame:** none found.

## Turn 8: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-drawing-recall-feedback.png

**Resource 8/32: `n1-083-corrected-drawing-recall-feedback.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text and stroke numbers were readable.

- **Screen:** "Drawing" with Back and the header "凌 endure; surpass". The red "Here is the kanji" message is the response after "I don't remember".
- **Panels:**
  - "Your drawing" is blank, as expected when the learner gives up on recalling the kanji.
  - "Correct strokes" shows the green reference, numbered 1–10. Strokes 1–2 are 冫 and strokes 3–10 are 夌. The numbers and strokes are distinct.
  - There is no "Practice only" line and no grading note in this frame, which fits the recall mode.
  - The Next button is shown. The grading that happens after Next is not visible in these pixels.
- **Article preview:**
  - It shows the heading, metadata and Meaning text, and more of the mnemonic: "…getting beyond the barrier. This is an invented memory scene, not a historical derivation or a verified explanation of…".
  - This disclaimer matches the card's "not etymology" label.
  - The inline 冫 and 夌 render with no boxes.
  - The text runs past the bottom edge, which is normal for a single screen.
- **Defects in this frame:** none found.

## Turn 9: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-drawing-trace.png

**Resource 9/32: `n1-083-corrected-drawing-trace.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable. The faint stroke numbers 1–10 were legible.

- **Screen:** "Drawing" with Back. "Attempts left: 1" and the queued-repeats note.
- **Prompt:** "Trace the kanji for" followed by "endure; surpass". Below it: "Ungraded tracing practice. You'll try from memory later."
- **Trace guide:** A translucent 凌 on a quarter-grid, with strokes numbered 1–10.
  - 1–2 are the two 冫 marks; 3–10 make up 夌.
  - The order matches the reference panels in resources 7–8.
  - No strokes collapse together and nothing is blank.
- **Status:** "Downloading the handwriting model (first use only)…". This was on an offline emulator. The later feedback frame said "handwriting model not available", so the app reported the state honestly. These pixels do not show a successful download or ML Kit recognition.
- **Buttons:** Undo, Clear and Check are disabled, as expected before any strokes are drawn.
- **Defects in this frame:** None found.

## Turn 10: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-endure-word-02.png

**Resource 10/32: `n1-083-corrected-endure-word-02.png`.** I made one `view` call. The image came back at about 900×2000 px and may have been resized. All text was readable.

- **Screen:** The 凌ぐ word article, titled "凌ぐ endure; surpass", with Back. This frame starts at the Meaning section; the name suggests it is a later scroll position.
- **Meaning:** The text gives two branches: "endure, keep out, or get through something difficult" and "surpass or outdo… in ability, degree or quality". It advises learning the whole phrase rather than one English equivalent.
- **Examples:**
  - 風雨を凌ぐ (ふううをしのぐ), "shelter from wind and rain". My earlier optional note still stands: "keep out wind and rain" would be closer to JMdict.
  - 前作を凌ぐ傑作 (ぜんさくをしのぐけっさく), "a masterpiece surpassing the previous work".
- **Grammar:** The thing faced or surpassed takes を. The verb is a transitive godan verb ending in ぐ, with the forms しのぎます, しのいで, しのいだ and しのがない.
  - The line wraps between し and のぎます. This is normal Japanese line breaking, not a defect, though it is slightly awkward to read on a phone.
- **How the kanji combine:**
  - The text says 凌 provides しの- and ぐ is okurigana. It says one word, not a different reading, carries both branches.
  - 凌 is a link.
- **Synonyms and antonyms:**
  - こらえる and 我慢 (がまん) with する are said to overlap in endurance, but their restraint uses do not all carry over.
  - 凌駕 (りょうが) with する is said to overlap with surpassing, not with weather.
  - こらえる, 我慢 and 凌駕 are links.
  - The 忍ぶ (しのぶ) contrast starts at the bottom edge of the frame and is cut off there. That is expected for a single frame.
- **Glyphs:** 凌, 風, 雨, 前, 作, 傑, 我, 慢, 駕 and 忍 all render. There are no replacement boxes.
- **Defects in this frame:** None found.

## Turn 11: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-endure-word-07.png

**Resource 11/32: `n1-083-corrected-endure-word-07.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. Everything was readable except the top line, which is clipped under the app bar. That line is the end of the conjugation list, which was already readable in resource 10.

- **Screen:** the 凌ぐ article, scrolled further. It shows "How the kanji combine", which is the same text as in resource 10.
- **Synonyms and antonyms:**
  - The こらえる and 我慢 overlap, and the 凌駕 surpassing overlap, both appear in full.
  - The 忍ぶ contrast is now complete: "a separate verb that can also mean endure. Its ending is ぶ, not 凌ぐ's ぐ: do not confuse しのいで with しのんで." This is correct.
- **Distinctive meaning:**
  - The text says getting through a difficulty does not guarantee a permanent solution, and that 凌ぐ is not limited to brief emergencies. It hedges both ways and imposes no rule.
  - In comparisons, it says, the word means going above the other thing, not merely matching it. The weather phrase is protection or endurance; the masterpiece phrase is comparative quality.
- **Sources:**
  - JMdict entry 1554200, senses 1–3, and comparisons 2827352, 1196970, 1606270 and 1467450.
  - "Digital Daijisen: 凌ぐ, senses 2 and 4" for usage and short example phrases.
  - JMdict and the Daijisen line are links.
- **Glyphs:** all render, with no replacement boxes.
- **Defects in this frame:** none found.

## Turn 12: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-endure-word-forward-14.png

**Resource 12/32: `n1-083-corrected-endure-word-forward-14.png`.** I made one `view` call. The image came back at about 900×2000 px and may have been resized. Everything was readable except the top table row, which is clipped under the app bar. Only its tail, "endure; surpass", shows; I will judge the reading table across frames together.

- **Screen:** This is the **凌 kanji article** ("凌 endure; surpass"), reached forward from the 凌ぐ word. It is scrolled near the bottom.
- **Readings note:** "Both readings in the frozen KANJIDIC2 record are selected for practice." It also says the grade-9/name-use classification does not make these ordinary readings name readings. This is correct.
- **Common words:**
  - 凌ぐ しのぐ, "endure or pull through; surpass".
  - 凌駕 りょうが, "surpassing; outdoing, also with する".
  - Both are links.
- **Notes:**
  - The ぐ-ending forms are shown, contrasted with 忍ぶ, which ends in ぶ.
  - 陵 (りょう; みささぎ) is described as having 阝 on the left rather than two 冫 strokes. The rarer spelling 陵駕 is not presented as freely interchangeable.
  - The comparisons are 准 "quasi-; associate rank" with 隹, 冶 "smelt; work metals" with 台, and 次 "next" with 欠. They end with "Similar left-hand marks do not imply the same meaning."
  - Keeping 次 in the Notes is acceptable, independent of the quiz options.
  - 准, 冶, 台, 次 and 欠 are links.
- **Sources:** KANJIDIC2 (database 2026-306, 2026-11-02, EDRDG, CC BY-SA 4.0); JMdict entries 1554200, 1606270 and 1467450; Digital Daijisen for 凌ぐ and 凌駕.
- **Glyphs:**
  - 阝, 冫 and 隹 render inline. In the gothic face, 阝 is clearly distinct from the two 冫 marks.
  - 陵 and 凌 are distinguishable.
  - There are no replacement boxes.
- **Defects in this frame:** none found.

## Turn 13: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-endure-word-kanji-backlink.png

**Resource 13/32: `n1-083-corrected-endure-word-kanji-backlink.png`.** I made one `view` call. The image may have been resized to about 900×2000 px. Everything was readable except the right edge of the table, which is clipped as the layout intends.

- **Screen:** The 凌 kanji article ("凌 endure; surpass"), opened through the backlink from the 凌ぐ word. It shows the Readings section.
- **Readings table:**
  - "Scroll sideways to read all columns." signposts the horizontal scroll.
  - The columns are Reading, Type and Typical words.
  - Row リョウ / on / 凌駕 りょうが "surpassing; outdoing".
  - Row しの.ぐ / kun / 凌ぐ しのぐ – "endure; surpas…". The text is clipped at the right edge.
  - Each reading has its own row with a linked word, which confirms my earlier textual finding.
  - The リョウ row's word text may continue off-screen. I judge horizontal scrolling across frames together and do not infer missing content from this one frame.
- **Below the table:** the selected-readings note about grade 9 and names, the Common words (凌ぐ and 凌駕 as links), and the Notes on ぐ versus ぶ and on 陵 with 阝 versus two 冫 marks. These match resource 12.
- **Glyphs:** 凌, 陵, 駕, 忍, 阝 and 冫 all render, with no replacement boxes. 陵 and 凌 are distinguishable in this face.
- **Defects in this frame:** None found.

## Turn 14: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-endure-word-reverse-24.png

**Resource 14/32: `n1-083-corrected-endure-word-reverse-24.png`.** I made one `view` call. The image may have been resized; it came back at about 900×2000 px. Everything was readable except the top conjugation line, which is clipped under the app bar and was already read in resource 10.

- **Screen:** The 凌ぐ word article ("凌ぐ endure; surpass") at the same scroll position as resource 11. This fits the return from the kanji backlink.
- **Content:** It matches resource 11 exactly as far as I can tell by eye:
  - How the kanji combine: 凌 represents しの- and ぐ is okurigana.
  - Synonyms: こらえる and 我慢 overlap in endurance; 凌駕 overlaps in surpassing, not weather.
  - The 忍ぶ contrast: ぶ versus ぐ, しのいで versus しのんで.
  - The Distinctive meaning text hedges both ways.
  - Sources: JMdict 1554200 senses 1–3 with the comparison entries, and Digital Daijisen senses 2 and 4.
- **Rendering:** All glyphs render, with no replacement boxes. The links are underlined.
- **Not provable from pixels:** How this screen was reached (System Back versus the in-app Back button). That rests on the supplied route evidence.
- **Defects in this frame:** None found.

## Turn 15: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-endure-word-system-back-to-kanji.png

**Resource 15/32: `n1-083-corrected-endure-word-system-back-to-kanji.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. Everything was readable except the top reading-table row, which is clipped under the app bar. Only "endure; surpass" from that row is visible.

- **Screen:** The 凌 kanji article ("凌 endure; surpass") at the same scroll position as resource 12. The clock reads 5:44 here and 5:43 in resource 12.
- **Content:** It looks the same as resource 12:
  - the note on selected readings (grade 9 is not a name reading);
  - Common words: 凌ぐ "endure or pull through; surpass" and 凌駕 "surpassing; outdoing, also with する";
  - Notes: the ぐ/ぶ contrast, 陵 with 阝 versus two 冫 marks, the rarer spelling 陵駕 not being freely interchangeable, and the 准/冶/次 comparisons with 隹/台/欠;
  - the KANJIDIC2/JMdict/Daijisen source line.
- **Navigation:** The pixels are consistent with returning to the 凌 kanji article at its earlier scroll position. That System Back caused it comes from the filename and supplied route evidence, not the pixels.
- **Glyphs:** 阝, 冫, 隹 and the other inline glyphs render, with no replacement boxes.
- **Defects in this frame:** None found.

## Turn 16: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-font-panel-1.png

**Resource 16/32: `n1-083-corrected-font-panel-1.png`.** One `view` call. The returned image is about 900×2000 px and may have been resized. At this size the glyphs are small but each one is identifiable. I could not judge fine stroke detail, such as hook shapes.

- **What the panel shows:** "Panel 1 / 3", with Gothic, Mincho, Textbook and Brush rows. Each row has the same 24 characters: 上 作 傑 優 冫 冴 冶 准 凌 前 台 回 売 夌 忍 慢 我 欠 次 行 超 越 追 過. The footer names the focus characters and says fallback families may coincide.
- **All four faces:** every character renders, with no blanks or replacement boxes.
  - 冴, 冶, 准, 凌 and 次 are distinguishable in each face. Their right-hand parts 牙, 台, 隹, 夌 and 欠 are separable.
  - The two 冫 marks are visible as the left part of these characters.
- **Fallback is visible:**
  - In Textbook, the standalone 夌 is noticeably heavier and gothic-like, and 冫 also looks gothic.
  - In Brush and Mincho, the standalone 冫 also looks gothic-like.
  - This matches the supplied cmap-absence and identical-hash evidence. It is a typeface change, not a blank or misleading glyph, so it is not a defect.
  - The pixels do not identify which fallback font is used.
- **Defects in this frame:** none found.

## Turn 17: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-font-panel-2.png

**Resource 17/32: `n1-083-corrected-font-panel-2.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. The glyphs are small but each is identifiable; fine stroke detail is not judgeable at this size.

- **What the panel shows:** "Panel 2 / 3", with Gothic, Mincho, Textbook and Brush rows. Each row has the same 6 characters: 阝 陵 隹 雨 風 駕. Together with panel 1's 24, that makes the 30 scoped Han characters.
- **All four faces:** every character renders. There are no blanks or replacement boxes.
  - 陵 clearly shows 阝 on its left. That contrasts with 凌's two 冫 marks in panel 1, so the 陵/凌 contrast holds visually.
  - 駕 renders in each face. Its 加 over 馬 structure is identifiable even at this size.
- **Fallback is visible:**
  - The standalone 阝 and 隹 look the same, in a gothic-like style, in all four faces.
  - In Textbook, 隹 is noticeably heavier than the surrounding textbook-style glyphs.
  - This matches the supplied cmap-absence and identical-hash evidence. It is a change of typeface, not a blank or misleading glyph, so it is not a defect. The pixels do not identify the fallback face.
- **Defects in this frame:** none found.

## Turn 18: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-font-panel-3.png

**Resource 18/32: `n1-083-corrected-font-panel-3.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. The glyphs are small but each one is identifiable; I could not judge fine stroke detail.

- **Content:** "Panel 3 / 3" shows the focus set in Gothic, Mincho, Textbook and Brush: 凌 陵 准 冶 冴 次 冫 夌 阝 隹, then the whole words 凌ぐ and 凌駕.
- **All four faces:** Every glyph renders, with no blanks or replacement boxes.
  - 凌 (two 冫 marks) and 陵 (阝) stay distinct.
  - 准, 冶, 冴, 次 and 凌 can be told apart by their right-hand parts: 隹, 台, 牙, 欠 and 夌.
  - 凌ぐ and 凌駕 render as whole words, and their kana and kanji spacing is readable.
- **Fallback is visible:**
  - The standalone 冫, 夌, 阝 and 隹 look gothic in all four rows.
  - In Textbook they are noticeably heavier than their neighbours.
  - This matches the supplied evidence of identical hashes and absence from the cmap. It is a typeface change, not a misleading collapse, so it is not a defect. The pixels do not identify the fallback face.
- **Not covered:** These pixels do not cover the 120 individual and 8 whole-word Paint assertions; those come from supplied evidence.
- **Defects in this frame:** none found.

## Turn 19: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-kanji-01.png

**Resource 19/32: `n1-083-corrected-kanji-01.png`.** One `view` call. The image may have been resized to about 900×2000 px. The text was readable. The bottom line is clipped by the frame edge and the table's right edge is cut off; both are expected.

- **Screen:** The top of the 凌 kanji article ("凌 endure; surpass"), with Back and an "Article contents" link.
- **Header:** "凌 — endure; surpass". Strokes: 10. Key (radical): 冫 (the two left-hand strokes, no. 15). JLPT: N1 (community list).
- **Meaning and origin:** Two branches are given: enduring or getting through a difficulty, and surpassing something else. The text says context selects the branch in 凌ぐ, and that 凌駕 means surpassing, not weather shelter.
- **Mnemonic:** It is complete in this frame. Two 冫 drops sit beside a 夌 "barrier", followed by "This is an invented memory scene, not a historical derivation or a verified explanation of the sound." The labelling is correct and does not deny any phonetic component.
- **Readings table:**
  - The note "Scroll sideways to read all columns." is shown.
  - Row: リョウ / on / 凌駕 りょうが "surpassing; outdoing".
  - Row: しの.ぐ / kun / 凌ぐ しのぐ – "endure; surpas…", clipped at the right edge.
  - The リョウ row shows no visible dash after りょうが. It may sit beyond the clipped edge. I can't tell from this frame, so I am not calling it a defect.
- **Glyphs:** All render, including 冫 and 夌, with no replacement boxes.
- **Defects in this frame:** None found.

## Turn 20: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-kanji-03.png

**Resource 20/32: `n1-083-corrected-kanji-03.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable. The table is clipped at its right edge, and the Common words heading sits at the bottom of the frame.

- **Screen:** the 凌 kanji article, scrolled to start at Meaning and origin.
- **Meaning, mnemonic and readings:** these match resource 19.
  - The mnemonic is complete, including its disclaimer.
  - The readings table has the sideways-scroll note. Rows: リョウ/on/凌駕 and しの.ぐ/kun/凌ぐ.
- **Notes shown here:** the selected-readings note about grade 9 and names is visible in full. The "Common words" heading begins at the bottom.
- **Table:** the kun row is clipped at "surpas…", and the リョウ row's trailing text is not visible. Both are consistent with the signposted sideways scroll. I can't establish missing content from these frames.
- **Glyphs:** all glyphs render, with no replacement boxes.
- **Defects in this frame:** none found.

## Turn 21: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-kanji-09.png

**Resource 21/32: `n1-083-corrected-kanji-09.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable except the right edge of the table, which is clipped and signposted as scrollable.

- **Screen:** the 凌 kanji article (5:43), scrolled to Readings. The pixel content looks the same as the backlink frame (resource 13, 5:44).
- **Readings table:** the note "Scroll sideways to read all columns." is shown. The rows are リョウ/on/凌駕 りょうが and しの.ぐ/kun/凌ぐ しのぐ.
- **Visible below the table:**
  - the selected-readings note about grade 9 and names;
  - the Common words, 凌ぐ and 凌駕 (links);
  - the Notes on ぐ vs ぶ and on 陵 (阝) vs the two 冫 marks;
  - the note that the rarer spelling 陵駕 is not a free interchange.
- **Glyphs:** all render, with no replacement boxes.
- **Defects in this frame:** none found.

## Turn 22: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-kanji-11.png

**Resource 22/32: `n1-083-corrected-kanji-11.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable. The left labels are clipped because the table is scrolled sideways.

- **Screen:** The 凌 kanji Readings section with the table scrolled sideways. The left column is cut off as "ading", "ョウ" and "の.ぐ", while the Typical words column is now fully visible.
- **Typical words, now complete:**
  - リョウ row: "凌駕 りょうが – surpassing; outdoing". This settles the missing dash I flagged in resources 19–21: the dash was just off-screen.
  - kun row: "凌ぐ しのぐ – endure; surpass".
- **Table read across frames:** Taken together with resources 13 and 19–21, which show the full Reading and Type columns, all three columns are complete. Each reading has its own row and its own linked word. No content is missing.
- **Rest of the frame:** The selected-readings note, Common words and Notes are unchanged and render correctly, with no replacement boxes.
- **Defects in this frame:** None found.

## Turn 23: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-kanji-17.png

**Resource 23/32: `n1-083-corrected-kanji-17.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. Everything was readable except the top table row, which is clipped under the app bar. I already read that row in full in resource 22.

- **Screen:** The bottom of the 凌 kanji article. It looks the same as resources 12 and 15. The table is still in its sideways-scrolled state.
- **Content:**
  - The selected-readings note.
  - Common words: 凌ぐ and 凌駕.
  - Notes: ぐ versus ぶ; 陵 (阝) versus two 冫 marks, with 陵駕 described as a rarer spelling, not a free interchange; and 准/冶/次 compared with 隹/台/欠.
  - The full metadata, JMdict and Daijisen source line, with links.
- **Article coverage:** Together with resources 19–22, the whole 凌 article has now been seen.
- **Rendering:** All glyphs render, with no replacement boxes.
- **Defects in this frame:** None found.

## Turn 24: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-meaning-feedback.png

**Resource 24/32: `n1-083-corrected-meaning-feedback.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable.

- **Screen:** The Quiz screen with Back. The large 凌 is in a gothic face and renders clearly.
- **Feedback:** The screen shows "Correct!" with the four options in this order:
  1. "smelt; work metals" (冶)
  2. "✓ endure; surpass" (凌), highlighted green
  3. "clear; sharp-minded" (冴)
  4. "quasi-; associate rank" (准)
- **The corrected choice in pixels:**
  - Exactly the three curated distractors, 冶, 冴 and 准, appear alongside 凌. There is no 次 "next" and no fifth or random choice.
  - The order 冶, 凌, 冴, 准 matches the supplied live question order.
  - "clear; sharp-minded" is the only label shown for 冴. It does not mean enduring or surpassing, so it is unambiguously wrong for 凌. I am not claiming that 冴える's undisplayed "excel at" sense has no overlap with 凌.
- **Below the options:** The answer line reads "endure; surpass", followed by the Next and "I guessed" buttons. The article preview shows the metadata and the Meaning text, cut off at the mnemonic heading.
- **What these pixels cannot show:** Which stack this was (N1 or All), or the QuizBuilder ID assertions. Those come from supplied evidence.
- **Defects in this frame:** None found.

## Turn 25: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-meaning-question.png

**Resource 25/32: `n1-083-corrected-meaning-question.png`.** I made one `view` call. The image came back at about 900×2000 px and may have been resized. All text was readable.

- **Screen:** Quiz screen with Back, "Attempts left: 1" and the queued-repeats note. The large 凌 is in a gothic face, and the two 冫 marks and 夌 are clearly drawn.
- **Question:** "What does it mean?" with four options:
  - smelt; work metals
  - endure; surpass
  - clear; sharp-minded
  - quasi-; associate rank

  Nothing is selected, and "I don't know" sits below the options.
- **Consistency:** The options and their order match the feedback frame (resource 24) and the supplied live order 冶, 凌, 冴, 准. There are exactly four. 次 "next" does not appear, and there is no random padding option.
- **Ambiguity:** Only "endure; surpass" fits 凌. "clear; sharp-minded" is clearly a wrong answer as displayed.
- **Defects in this frame:** None found.

## Turn 26: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-selection.png

**Resource 26/32: `n1-083-corrected-selection.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable. The last stack chip is clipped at "St…", but the chip row is meant to scroll sideways.

- **Screen:** "Kanji" with Back. It shows "N1 · 115 cards", with the N1 chip highlighted among N5, N4, N3, N2, N1 and All, followed by "Only cards tagged N1." and "Each stack keeps its own review schedule."
- **Counts:**
  - Meaning quiz: 1 due, 0 new.
  - Drawing: 0 due, 1 new.
  - Readings (on'yomi and kun'yomi): 2 due, 0 new.
  - Each has a Start button, and there is a "Browse all kanji" button.
- **Agreement with supplied evidence:** The 115-card N1 stack matches the supplied import count. One meaning question, a new drawing card and two reading questions match the later 2-of-2 readings session.
- **The earlier "All · 0 cards" home-screen state:** This 5:43 frame shows N1 selected with 115 cards loaded. So that tree state is not what the learner saw during the captured scenario; it was most likely dumped later, in `finally`. The pixels do not prove when it was dumped.
- **Not shown:** That this N1 stack was the one used for the meaning-quiz frames.
- **Defects in this frame:** None found.

## Turn 27: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-surpass-word-02.png

**Resource 27/32: `n1-083-corrected-surpass-word-02.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. Everything was readable except the bottom line, which the frame edge cuts off.

- **Screen:** the 凌駕 word article, titled "凌駕 surpass; outdo", with Back.
- **Meaning:**
  - The text says 凌駕 names surpassing or outdoing, and is both a noun and a する-verb (凌駕する, 凌駕します, 凌駕した, 凌駕しない). The thing surpassed takes を.
  - The example is 前作を凌駕する売れ行き (ぜんさくをりょうがするうれゆき), "sales surpassing those of the previous work".
  - A note follows: "the comparison concerns sales, not a claim that the new work is artistically better". This is correct.
- **How the kanji combine:**
  - 凌 (a link) contributes surpassing and is read リョウ here. 駕 (ガ), which has no card and is shown as plain text, also has a rising-above-others sense documented with this compound.
  - The two characters are said to reinforce the surpassing idea, and the text warns against forcing 駕's vehicle meaning into a literal story. This is correct and sourced.
- **Synonyms and antonyms:**
  - 凌ぐ is said to overlap in surpassing but also to have endurance and weather-protection uses that 凌駕 lacks.
  - 優れる (すぐれる) is described as an intransitive verb meaning excellence, so it does not follow 凌駕する's object + を pattern.
  - 凌ぐ and 優れる are links.
  - The 上回る (うわまわる) "exceed; surpass", "also suits…" sentence is cut off at the bottom of the frame.
- **Glyphs:** all render, including 駕, 売 and 優, with no replacement boxes.
- **Defects in this frame:** none found.

## Turn 28: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-surpass-word-03.png

**Resource 28/32: `n1-083-corrected-surpass-word-03.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable except the bottom line, which is cut off by the frame edge.

- **Screen:** the 凌駕 word article ("凌駕 surpass; outdo").
- **Content:** it looks the same to me as resource 27. It shows:
  - the noun/する-verb forms and the を object;
  - the sales example, with its note that "sales, not artistically better" is being compared;
  - the explanation of how the kanji combine: リョウ + 駕 (ガ), meaning "rising above others", with no vehicle story;
  - the synonyms 凌ぐ and 優れる (intransitive).
  
  The 上回る sentence is again cut off at the bottom.
- **Not visible:** this frame does not show the rest of the 上回る sentence, the 陵駕 spelling note or the sources.
- **Defects in this frame:** none found.

## Turn 29: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-surpass-word-06.png

**Resource 29/32: `n1-083-corrected-surpass-word-06.png`.** I made one `view` call. The image may have been resized; it came back at about 900×2000 px. All text was readable except the bottom line, "Dictionary: JMdict, entry 1606270; comparisons…", which the frame edge cuts off.

- **Screen:** the 凌駕 word article, scrolled further down.
- **How the kanji combine and Synonyms:** both repeat what resources 27–28 showed.
- **上回る sentence:** now visible in full: "上回る (うわまわる), 'exceed; surpass,' also suits numerical comparisons. These related words are not unrestricted substitutes in every phrase." This is a fair, qualified claim.
- **Distinctive meaning:** "凌駕する means going above the comparison target, not simply reaching the same level." It goes on to say the learner should identify what is surpassed and in what respect, and that 凌駕 is not a general expression for surviving hardship. This is correct.
- **Rare spelling 陵駕:** "陵駕 (りょうが) is also recognized, but JMdict marks that spelling as rarely used. This does not make the pronunciation りょうが rare or make 凌 and 陵 freely interchangeable elsewhere." The rare-spelling versus rare-pronunciation distinction is shown correctly.
- **Glyphs:** 陵, 凌 and 駕 all render, and 陵 and 凌 are distinguishable. There are no replacement boxes.
- **Defects in this frame:** none found.

## Turn 30: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-surpass-word-08.png

**Resource 30/32: `n1-083-corrected-surpass-word-08.png`.** I made one `view` call. The returned image is about 900×2000 px and may have been resized. All text was readable except the top line, which is clipped under the app bar. That line was already read in full in resources 27–29.

- **Screen:** The bottom of the 凌駕 word article.
- **Content:** The end of "How the kanji combine", which warns not to read in 駕's vehicle sense. Then Synonyms (凌ぐ, 優れる as intransitive, 上回る for numerical comparisons, not unrestricted substitutes), Distinctive meaning, and the 陵駕 rare-spelling note. All of it is the same as earlier frames.
- **Sources, now visible in full:**
  - "Dictionary: JMdict, entry 1606270; comparisons 1554200, 1539080 and 1352770."
  - "Usage and short example phrase: Digital Daijisen: 凌駕."
  - "駕's contribution: Digital Daijisen: 駕, character-entry sense 2."
  - These match the sources I verified earlier. JMdict and both Daijisen citations are links.
- **Article coverage:** With resources 27–30, the 凌駕 article has now been seen from Meaning to the end. Its top title and header area appear only as the app-bar title in these frames.
- **Rendering:** All glyphs render with no replacement boxes.
- **Defects in this frame:** None found.

## Turn 31: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-surpass-word-kanji-backlink.png

**Resource 31/32: `n1-083-corrected-surpass-word-kanji-backlink.png`.** I made one `view` call. The image may have been resized; it came back at about 900×2000 px. Everything was readable except the right edge of the table, which is clipped; the screen itself says the table scrolls sideways.

- **Screen:** The 凌 kanji article ("凌 endure; surpass"), reached by the backlink from 凌駕. It is scrolled to Readings.
- **Content:** Visually the same as resources 13 and 21:
  - the readings table (リョウ/on/凌駕, しの.ぐ/kun/凌ぐ) with its scroll note;
  - the selected-readings note on grade 9 and names;
  - Common words 凌ぐ and 凌駕;
  - the ぐ/ぶ note and the 陵 (阝) versus 冫 note.
- **Navigation:** The pixels fit the 凌駕→凌 backlink direction. They do not show which link was tapped; that comes from the filename and the route evidence I was given.
- **Glyphs:** All render. There are no replacement boxes.
- **Defects in this frame:** None found.

## Turn 32: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-083-native-corrected\attempt-578\n1-083-corrected-surpass-word-system-back-to-kanji.png

**Resource 32/32: `n1-083-corrected-surpass-word-system-back-to-kanji.png`.** I made one `view` call. The image may have been resized; it came back at about 900×2000 px. Everything was readable except the top table row, which the app bar clips; I read that row in full in resource 22.

- **Screen:** The bottom of the 凌 kanji article ("凌 endure; surpass"), at 5:44. The table is still scrolled sideways.
- **Content:** Pixel for pixel it matches resources 12, 15 and 23:
  - the selected-readings note;
  - Common words 凌ぐ and 凌駕;
  - the Notes on ぐ/ぶ, 陵 (阝) versus 冫 and the rare spelling 陵駕, and 准/冶/次 with 隹/台/欠;
  - the KANJIDIC2, JMdict and Daijisen source line.
- **Navigation:** The pixels match a return to the 凌 article at its earlier scroll position. That this came from System Back, and not the in-app Back button, comes from the filename and the route evidence I was given, not from the pixels.
- **Rendering:** All glyphs render. There are no replacement boxes.
- **Defects in this frame:** None found.
- **Coverage gap for the final report:** None of the 31 PNGs I was sent shows the top of either word article: the 凌ぐ or 凌駕 header, reading line and any lead-in above Meaning. Those parts would be in frames numbered 00 or 01, which I was not sent. I saw the word title and gloss only in the app bar.

## Turn 33: FINAL REPORT

## Batch 083 visual confirmation (凌, 凌ぐ, 凌駕): final report

All three new articles come out CLEAN on all three facets, with no findings, and the 074 choice issue is resolved for the default four-choice N1 and All quiz. One gap: no frame shows the top (title, reading and anything above "Meaning") of either word article.

### Snapshot
- **Evidence HEAD:** 2f24c5c456ea7a026762f6c6c95b2bcdcebb337b.
- **Reviewed teaching commit:** 7cc896f488ae5315046453777aae6768b9ff18e8.
- **Native build:** envelope 867fe8be, content version 6dfe6a1e287ce5df, run attempt 578.
- All hashes and identities are as given in the packets. I did not check Git, upstream sources or hashes myself, and I don't know the uncommitted state.

### Scope
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), the original batch-083 reviewer, continuing my own work. This is a dependent visual confirmation, not a new blind review of the wording or the dictionaries.
- **What I read:** 32 single-view turns, one resource each.
  - Resource 1 was `docs\n1-reviews\batch-083-visual-source-packet.txt`. It came back complete, with no truncation marker and nothing denied.
  - Resources 2–32 were the 31 original PNGs in `attempt-578\`, which stand for all 56 captures after identical files were removed (deduplication was the host's; I did not check it).
  - Nothing was denied or missing. I made no extra reads and used no other tools.
- **Image limits:**
  - Every PNG came back at about 900×2000 px and may have been resized. I make no claims about full-resolution bytes or hashes.
  - The font panels were legible enough to identify each glyph, but too small to judge fine stroke detail.
  - The top lines of some frames sat under the app bar, and table columns were cut off at the edges. In each case another frame showed that content in full.

### Verdicts
| Article | Correctness | Scoped coverage | Bounded visual comprehensibility |
|---|---|---|---|
| `kanji\凌.md`, including the changed choice | CLEAN | CLEAN | CLEAN |
| `words\凌ぐ.md` | CLEAN | CLEAN | CLEAN (see coverage limit) |
| `words\凌駕.md` | CLEAN | CLEAN | CLEAN (see coverage limit) |

CLEAN means I found no actionable defect within scope. It is not an exhaustive certification.

### Findings
None. What the pixels showed:

**凌 article**
- I saw the whole article across the kanji-01/03/09/11/17 frames, the backlink frames and the System Back frames.
- The metadata on screen is right: 10 strokes, radical 冫 (no. 15), "N1 (community list)".
- The two meanings, enduring or getting through and surpassing, are kept apart. The text says 凌駕 means surpassing, not weather shelter.
- The mnemonic is labelled as an "invented memory scene, not a historical derivation or a verified explanation of the sound".
- The readings table:
  - The screen tells the learner to scroll sideways.
  - リョウ/on links to 凌駕 ("surpassing; outdoing"); しの.ぐ/kun links to 凌ぐ ("endure; surpass").
  - Read across frames, every column is complete. The dash I wondered about in kanji-01 is just off-screen, as kanji-11 shows.
- The note says grade 9 does not make these ordinary readings name readings.
- The notes cover:
  - ぐ versus 忍ぶ's ぶ.
  - 陵 with 阝 versus two 冫 marks; the rare spelling 陵駕 is not a free swap.
  - 准, 冶 and 次 compared via 隹, 台 and 欠. Keeping 次 in the notes is fine even though it is no longer a quiz option.
- The source line and links are present.

**凌ぐ article**
- The meaning has two parts: endure, keep out or get through; and surpass or outdo.
- Examples, with kana and translations:
  - 風雨を凌ぐ (ふううをしのぐ), "shelter from wind and rain".
  - 前作を凌ぐ傑作 (ぜんさくをしのぐけっさく), "a masterpiece surpassing the previous work".
- Grammar: takes を; a transitive godan verb ending in ぐ. The forms しのぎます, しのいで, しのいだ and しのがない are shown.
- 忍ぶ is contrasted: しのいで versus しのんで.
- The "Distinctive meaning" section imposes no rule about temporary, permanent or formal use.
- Synonyms (こらえる, 我慢, 凌駕) are qualified as partial overlaps.
- Sources: JMdict 1554200 and Daijisen.

**凌駕 article**
- It is a noun and a する-verb that takes を.
- Example: 前作を凌駕する売れ行き (ぜんさくをりょうがするうれゆき). The text says it compares sales, not artistic quality.
- How the kanji combine: 凌 is read リョウ; 駕 (plain text, ガ) has a "rising above others" sense. The text warns against reading in 駕's vehicle meaning.
- Synonyms:
  - 凌ぐ is noted for its extra uses.
  - 優れる is correctly called intransitive.
  - 上回る suits numerical comparisons and is not an unrestricted substitute.
- 陵駕 is described as a rare spelling, not a rare pronunciation and not a free swap.
- Sources include Daijisen's 駕 entry, sense 2.

**Changed quiz choice**
- The meaning question and its feedback show exactly four options in the live order:
  - smelt; work metals (冶)
  - endure; surpass (凌)
  - clear; sharp-minded (冴)
  - quasi-; associate rank (准)
- There is no 次 and no random filler option.
- As shown, "clear; sharp-minded" is clearly wrong for 凌. I am not claiming there is no overlap with 冴える's undisplayed "excel at" sense, or with 冴え's "skillfulness".
- The selection screen shows "N1 · 115 cards".

**Reading quizzes**
- On'yomi question (2 attempts left): リョウ/ジュン/ヤ/リュウ. Kun'yomi question (1 attempt left): さえる/しおり/しか/しのぐ.
- Both feedback screens are correct, followed by "Session complete, 2 of 2 answers correct."
- None of the wrong options is a reading of 凌.

**Drawing**
- The tracing screen shows strokes numbered 1–10. Strokes 1–2 are 冫, which matches the stroke data.
- The feedback screen shows the injected strokes and "Practice only: not graded".
- The give-up recall screen shows a blank drawing and the reference strokes.
- The app honestly shows first "Downloading the handwriting model…" and then "handwriting model not available".

**Fonts**
- All 30 scoped Han characters and the whole words 凌ぐ and 凌駕 render in all four faces (Gothic, Mincho, Textbook, Brush). There are no blanks or replacement boxes.
- 凌 and 陵 stay distinct, as do 准, 冶, 冴, 次 and 凌.
- The standalone components 冫, 夌, 阝 and 隹 visibly fall back to a gothic-looking face; this is clearest in Textbook. That is only a change of typeface, not a defect.

**Navigation**
- The pixels match 凌⇄凌ぐ and 凌⇄凌駕 in both directions, plus the word comparison links.
- That those returns came from System Back, and that the run was offline, comes from the supplied route data, not from pixels.

**Earlier "All · 0 cards" anomaly**
- The 5:43 selection frame shows N1 with 115 cards loaded.
- So the "All · 0 cards" screen tree was most likely dumped after the scenario finished, in the test's cleanup step. The pixels don't prove when it was taken.

### 083-NATIVE-574-CHOICE
- **Text:** resolved, as I said before. 冴 (N1) replaces 次 (N3), so all three planned wrong answers are available in the N1 and All stacks.
- **Run time:** resolved for the default four-choice quiz in N1 and All, based on the supplied evidence.
  - Attempt 578 reports OK (2 tests): both named native cases passed.
  - QuizBuilder's exact IDs and titles are reported for the 115-card and 1,095-card stacks, with no random filler.
  - The pixels independently confirm the four displayed options in one live question.
- **History:** the original attempt-574 failure is kept on record, not erased. The 麟 fallback captured then is not claimed to be ambiguous.
- **Not claimed:** safety of the All UI path, custom, padded, partial or larger stacks, or reverse questions.

### Optional (carried forward)
- `words\凌ぐ.md:20`: "keep out wind and rain" would be closer to JMdict than "shelter from". The current wording is visible on screen and is not wrong.
- `words\凌ぐ.md:15–17`: could mention sense 3, "defy; slight". Not required.
- **Legacy, not this batch:** `冴.md:13` still lists 次 (N3), so a 冴 question in the N1 stack will get a fallback option in the same way.
- **Legacy, not this batch:** extra-practice padding (`QuizViewModel.pad`) adds only the borrowed cards to the option pool, so curated distractors may be missing there.
- **App UI wording, outside scope:** "Practice only: not graded" next to "Graded by stroke shapes only" reads slightly contradictory.
- **Line breaking:** the conjugation list in 凌ぐ breaks between し and のぎます. This is normal Japanese line breaking.

### Limits
- **Word-article tops not seen:** no frame shows the 凌ぐ or 凌駕 heading, reading line or anything above "Meaning". I saw the title and gloss only in the app bar, so this part is not visually confirmed. My earlier text review covered it.
- **Supplied evidence, not pixels:** reading keys りょう/しのぐ being saved, the Full/Lite and raw-source data, the saved logs, the import counts (1,095/5,052/115, zero problems), the content version, the QuizBuilder ID assertions, System Back, offline mode, the emulator configuration, the test-only Android build 1c1b7bf4, the inherited HOST577 compile checks, and the 120 individual + 8 whole-word Paint checks. Those Paint checks are not 128 PNG reads.
- **Inherited, not freshly inspected:** the earlier all-40-font check.
- **Font limits:** pixels and hashes do not identify which fallback face is used, and a character missing from a font's character map is not a glyph failure.
- **Drawing:** the strokes were injected by the test. This is not human handwriting, successful recognition, ML Kit or a model download.
- **Device:** emulator only (API 35, emulator-5580). No physical phone, latest-main or native-speaker claims, and no evidence about learning effectiveness.
- **Publication still outstanding:** merge with current main, the combined checks, the signed owner push, remote CI, the exact immutable ZIP, owner issue 60, physical-phone testing, general release and the whole-set review.
- **Earlier limits still apply:** I checked no sources or upstream data myself; byte and line totals were unconfirmed; title uniqueness across the corpus was not checked; production code was read only in the excerpts supplied.
