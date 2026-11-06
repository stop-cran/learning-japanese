## Turn 1: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-visual-source-packet.txt

**Resource 1 of 26: `docs\n1-reviews\batch-081-visual-source-packet.txt`**

I read it with one `view` call (`forceReadLargeFiles=true`, no range). There was no truncation marker. Reviewer model: Claude Opus 5.5 (claude-opus-5.5).

- **Article sources:** The SHA256 values printed for `冶.md` (803fdcdab…), `冶金.md` (4bf61335…) and `金.md` (96bbf429…) match those in the original textual packet, and the text is identical. The `金.md:39` bullet is unchanged. My original textual dispositions carry forward: no findings, five optional suggestions.
- **Supplied execution evidence:** The packet reports 2 of 2 tests passing on `emulator-5580` (SDK 35), with one archive request, 1093 kanji, 5049 words, 113 N1 cards, version `f1dd5d8b9d2ff535`, zero problems and reading-parser epoch 1. It also reports full reading lists on [ヤ] and kun [い.る], selected on [ヤ] and kun [], quiz keys や and [], and `phoneEvidence:false`. `INSTRUMENTATION_CODE: -1` is a normal `am instrument` result. These are supplied claims, not pixels.
- **Captures:** 45 PNGs are listed, matching the stated total.
- **Glyph rasters:** The four 冶金 whole-word probes show both characters non-blank in every font family. The isolated 冫 and 氵 produce the same raster hash in all four families, so they likely come from one shared fallback. That is not a glyph failure, and hashes do not identify the face. Real-pixel checks of the three font panels are still needed.
- **Accessibility tree:** The final dump shows a transient loading state ("Loading your cards…", "All · 0 cards", Start buttons disabled), even though the test asserts the N1 stack. I'm treating this as a timing artefact to check against the pixels later, not a defect.

## Turn 2: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-curated-on-done.png

**Resource 2 of 26: `n1-081-curated-on-done.png`**

What the pixels show (the view may have been downscaled; all text is legible): the "Kanji readings" screen with a "← Back" link. It reads "Session complete" and "1 of 1 answers correct.", with a filled "Done" button and an outlined "Practice more" button. The rest of the screen is blank, and the status bar shows 10:34 with the mobile-data indicator crossed out (no data connection).

- This matches the supplied 1-of-1 Done result. Nothing on screen is clipped, overlapping or a blank glyph box.
- No kanji, reading or reading type (on/kun) appears here, so this frame cannot confirm that only the ヤ on reading was asked. That, and the persisted good log, come from supplied fixture and route evidence, not these pixels.
- The status-bar icon is consistent with being offline but doesn't prove it.
- No defect seen in this resource.

## Turn 3: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-curated-On-feedback.png

**Resource 3 of 26: `n1-081-curated-On-feedback.png`**

What the pixels show (the view may have been downscaled; the main text is legible):

- **Question area:** The "Kanji readings" screen shows a large 冶 drawn clearly with two left-hand ice strokes (冫), not three water strokes (氵), and the right side shaped like 台. There are no blank or replacement boxes.
- **Feedback:** "Correct! — on'yomi". The chosen answer is "✓ ヤ" in green; the other choices are ヤク, シ and ヘイ. None of those is a source reading of 冶, so only one answer is right. シ is the on reading of the look-alike 始, which makes it a fair wrong choice.
- **Reading line:** "smelt; work metals: ヤ、いる" lists the full source readings, with いる shown without its dot. This is feedback text only; no kun question was offered, consistent with the empty kun selection.
- **Buttons:** "Next" and "I guessed".
- **Article preview below:**
  - The heading reads "冶 — smelt; work metals".
  - The facts line shows strokes 7, the radical 冫 ("the two left-hand strokes, no. 15"), and "JLPT: N1 (community list)". The 冫 glyph there is small, and at this resolution I can't confirm its two separate strokes with certainty.
  - The "Meaning and origin" text matches the source, including the underlined 冶金 link, (やきん), 陶冶 and (とうや).

Nothing is clipped or overlapping.

One observation, not a defect: the feedback line lists いる without the article's "source-only" qualification. That is the app's normal feedback format, and the article below gives the qualification.

## Turn 4: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-curated-On-question.png

**Resource 4 of 26: `n1-081-curated-On-question.png`**

What the pixels show (the view may have been downscaled; all text is legible):

- The "Kanji readings" screen shows "Attempts left: 1" and a note about queued repeats.
- 冶 is drawn large in a brush-like style, a different typeface from the feedback frame. Its two left-hand ice strokes (冫) are clearly separate, and it can't be mistaken for 治 with three water strokes. There are no blank or replacement boxes.
- The prompt is "Pick the on'yomi", with choices ヤ, ヤク, シ and ヘイ (the same set as the feedback frame), plus "I don't know". No answer is preselected.
- Only ヤ is a source reading of 冶, so there is one correct choice. The screen asks only for the on'yomi and has no kun prompt. "Attempts left: 1" fits the single selected on question.

Nothing is clipped or overlapping. No defect seen in this resource.

## Turn 5: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-drawing-feedback.png

**Resource 5 of 26: `n1-081-drawing-feedback.png`**

What the pixels show (the view may have been downscaled):

- **Header:** The "Drawing" screen is headed "冶 smelt; work metals", with "Practice only: this attempt is not graded." and "Well drawn!".
- **Your drawing (left panel):** The injected seven strokes, in blue.
- **Correct strokes (right panel):** Seven green strokes numbered 1 to 7. Strokes 1 and 2 are the two 冫 strokes (a dot and a rising stroke), separate and on the left. Strokes 3 and 4 form 厶, and strokes 5 to 7 form 口. This matches 7 strokes, 冫 rather than 氵, and the KanjiVG ordering.
- **Grading note:** "Graded by stroke shapes only (handwriting model not available)", which confirms that the ML Kit handwriting model was unavailable. This is shape matching of injected reference strokes, not human handwriting or recognition.
- **Below "Next":**
  - The heading, facts line and "Meaning and origin" text match the source.
  - The mnemonic begins "imagine the two cold 冫 marks beside a 台-shaped…", and the 台 link is visible.

**Display concern:** where 冫 stands alone in the facts line and the mnemonic, it renders as a small, thin mark followed by a wide gap. At this resolution I can't tell whether it shows two distinct strokes or reads like a single ">"-like mark. It is present, not a blank box. Whether it weakens the "two strokes" teaching point is **UNVERIFIED**. The font panels or a higher-resolution view would settle it. The 冶 glyphs here clearly show 冫.

## Turn 6: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-drawing-recall-feedback.png

**Resource 6 of 26: `n1-081-drawing-recall-feedback.png`**

What the pixels show (the view may have been downscaled):

- **Header:** The "Drawing" screen is headed "冶 smelt; work metals", with red "Here is the kanji". This is the recall screen after "I don't remember".
- **Your drawing:** The panel is blank, as expected after giving up.
- **Correct strokes:** The same seven numbered green strokes as before. Strokes 1 and 2 are the separate 冫 strokes, 3 and 4 form 厶, and 5 to 7 form 口.
- **Article below "Next":**
  - The heading, facts line and "Meaning and origin" text match the source.
  - The mnemonic is now complete through "…not a historical derivation or a verified explanation of the sound."

Recording the grade when Next is pressed comes from the supplied route evidence; a still frame can't show it.

The 冫 concern from resource 5 carries over. The standalone 冫 in the facts line and the mnemonic is again a small, thin mark followed by a wide gap, and at this resolution it still can't be confirmed as two distinct strokes. It is present, not a blank box. This remains **UNVERIFIED**, pending the font panels. Nothing else is clipped, and no other defect is seen.

## Turn 7: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-drawing-trace.png

**Resource 7 of 26: `n1-081-drawing-trace.png`**

What the pixels show (the view may have been downscaled; all text is legible):

- **Header:** The "Drawing" screen shows "Attempts left: 1", "Trace the kanji for", "smelt; work metals" and "Ungraded tracing practice. You'll try from memory later." The meaning prompt matches the card title.
- **Tracing grid:** Seven faint numbered guide strokes, before any input. Strokes 1 and 2 are the two separate 冫 strokes, 3 and 4 form 厶, and 5 to 7 form 口. This matches the seven-stroke 冫 form (not 氵) and the KanjiVG order.
- **Below the grid:** "Downloading the handwriting model (first use only)…", with Undo, Clear and Check all disabled.

**Status-message observation:** The download message appears while the emulator is offline. The later feedback frame says the model is "not available" and grades by stroke shape only. This is an app-level runtime message, not a problem with this batch's content. Whether the message is acceptable offline is outside this content review.

No content defect seen in this resource.

## Turn 8: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-font-panel-1.png

**Resource 8 of 26: `n1-081-font-panel-1.png`** (font panel 1 of 3)

What the pixels show (the view may have been downscaled):

- **Characters shown:** All 24 Han on this panel appear in each of the four families: Gothic, Mincho, Textbook and Brush. Textbook spaces the characters more widely and wraps 溶 onto the next line, which is fine.
- **No missing glyphs:** There are no blank, replacement or tofu boxes.
- **冶 versus 治:** In every family, 冶 has two left-hand strokes and 治 has three water strokes, and the two are clearly distinguishable. 台 and 始 (女 on the left) are also distinct.
- **冫 and 氵 alone:** On their own they look the same in all four rows, which fits the shared-fallback hashes and is acceptable. 冫 shows as two short marks and 氵 as three, but 冫 is lighter and smaller than the surrounding characters, with a gap after it.
- **Bottom caption:** Both forms are also visible in "冶/治/台/始, 冫/氵".

**Effect on the earlier 冫 concern:** This partly resolves the hypothesis from resources 5–6. At this size the two strokes of 冫 can be told apart from 氵's three, so it doesn't collapse into a misleading look-alike. It is still visually faint, so its legibility on a physical phone remains unverified.

No defect is established in this resource.

## Turn 9: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-font-panel-2.png

**Resource 9 of 26: `n1-081-font-panel-2.png`** (font panel 2 of 3)

What the pixels show (the view may have been downscaled):

- **Characters shown:** 金, 鋳, 錬, 鍛 and 陶 appear in all four families: Gothic, Mincho, Textbook and Brush.
- **No missing glyphs:** There are no blank, replacement or tofu boxes, and all five characters look complete at this size.
- **Family differences:** Each row is visibly different in weight and style. Brush is bold and calligraphic, and Textbook is lighter with wider spacing.
- **金 radical side:** The 金 component on the left of 鋳, 錬 and 鍛 is recognisable in every family.
- **Caption:** "冶/治/台/始, 冫/氵" is legible again, with 冫 lighter and smaller as in panel 1.

**Limit:** fine internal detail, such as the right-hand part of 鍛 or the inner strokes of 陶, can't be checked stroke by stroke at this scale. Nothing suggests a misleading look-alike substitution.

No defect seen in this resource.

## Turn 10: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-font-panel-3.png

**Resource 10 of 26: `n1-081-font-panel-3.png`** (font panel 3 of 3)

What the pixels show (the view may have been downscaled):

- **Look-alikes side by side:** All four families show "冶 治 台 始 冫 氵 冶金 金 鋳 錬 鍛 陶 溶" on one line each. In every family, 冶 has two left-hand strokes and 治 has three water strokes, and the two are clearly distinct. 台 and 始 (女 on the left) are also distinct.
- **冫 and 氵 alone:** Side by side, 冫 shows two marks and 氵 three. They look the same across families, which fits the shared fallback, but they are not collapsed into one look-alike. Both are lighter and smaller than the other Han, with a gap after them.
- **冶金 as a word:** Both characters render together, with no gap or box, in all four families.
- **No missing glyphs:** There are no blank or replacement boxes.

This supports the resolution I reached in panel 1: 冫 is legible as two strokes here. Its faintness on a physical phone remains unverified. Fine stroke-level detail of 鍛 and 陶 is limited by the resolution.

No defect seen in this resource.

## Turn 11: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-gold-forward-26.png

**Resource 11 of 26: `n1-081-gold-forward-26.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Header:** The 冶金 word article is open, headed "冶金 metallurgy".
- **How the kanji combine:** Matches source lines 28–32. 冶 (ヤ) and 金 (キン) are underlined links, and the 金 link is the one tapped for the 冶金 → 金 direction.
- **Synonyms and antonyms:** Matches source lines 36–40, including 冶金学 (やきんがく), the underlined 金属 (きんぞく) link, and 製錬 and 精錬 (both せいれん).
- **Distinctive meaning:** Matches source lines 44–50, including 錬金術 (れんきんじゅつ) "alchemy" and the 溶かす (とかす) link.
- **Sources line:** "Dictionary: JMdict, entry 1536310; related entries…" is shown. The final "Scope: 世界大百科事典: 冶金." line sits at the bottom edge with its descenders slightly clipped, but it is still legible.

The kanji, kana and English all match the source, with no blank or replacement glyphs and no overlaps. The way the reading れんきんじゅつ wraps across two lines is ordinary.

Following the link to 金 comes from the supplied route evidence; this still frame only shows the tap source.

No defect seen in this resource.

## Turn 12: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-gold-reverse-27.png

**Resource 12 of 26: `n1-081-gold-reverse-27.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Header:** The 金 kanji card is open, headed "金 gold, money".
- **Readings table (unchanged context):** The rows for かね, かな- and -がね are visible. Their example cells are cut off at the right edge, for example "金持ち" and "黄金 こが…". This is the existing horizontal-scroll state of an unchanged part of the card, not something introduced by this batch.
- **Common words:** The four bullets are 金曜日 きんようび — Friday, お金 おかね — money, 現金 げんきん — cash, and **冶金 やきん — metallurgy**. The added bullet is underlined as a link and follows the same format as the others. It matches source line 39 exactly, including the correct reading やきん and gloss.
- **Notes:** Unchanged context, fully legible.

This frame shows where the 金 → 冶金 link is tapped. The link resolving to the word article comes from the supplied route evidence.

The bullet renders correctly. No defect seen in this resource.

## Turn 13: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-kanji-01.png

**Resource 13 of 26: `n1-081-kanji-01.png`**

What the pixels show (the view may have been downscaled; most text is legible):

- **Header and top:** The 冶 card is headed "冶 smelt; work metals", with "Article contents" below.
- **Facts line, Meaning and origin, and mnemonic:** All match the source, including the underlined 冶金 (やきん), 陶冶 (とうや) and 台 links.
- **Readings:**
  - The text says "Both source readings remain below. Only ヤ is selected for reading practice.", followed by the signpost "Scroll sideways to read all columns."
  - The table headings are Reading, Type and Typical words. The ヤ row shows "on" and "冶金 やきん — metallurgy" (linked).
  - The い.る row shows "kun" and "source-only character-dicti… nary lookup". The right edge cuts the cell, and the "o" of "dictionary" is clipped.
- **Order:** The rows keep the source order, ヤ then い.る.

**Display points:**

- The clipped table cell is expected in this signposted horizontal-scroll state. I'll judge it together with the shifted-cell frames (kanji-13 and kanji-15), not as a defect from this frame alone.
- The standalone 冫 in the facts line and the mnemonic again renders as a small, faint mark followed by a wide gap. The font panels showed it can be read as two strokes, so I'm not treating it as a misleading look-alike. Its faintness on a phone remains unverified.

No defect is established in this resource.

## Turn 14: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-kanji-03.png

**Resource 14 of 26: `n1-081-kanji-03.png`**

What the pixels show (the view may have been downscaled):

- **Header:** The 冶 card is open, headed "冶 smelt; work metals".
- **Meaning and origin, and mnemonic:** Fully visible and matching source lines 22–29, with the 冶金, 陶冶 and 台 links and kana.
- **Readings:** The intro text and the signpost "Scroll sideways to read all columns." are shown. The ヤ row shows "on" and "冶金 やきん — metallurgy".
- **い.る (kun) row:** The cell wraps into about ten narrow lines: "source-only / character-dicti… / nary lookup / information; n… / exact modern / word example / written 冶る w… / established in / the inspected / f…". The right edge clips characters, and the last line ("families") is cut at the bottom of the frame.
  - The meaning is still mostly readable.
  - The written form 冶る renders correctly.
  - The cell has to be judged together with the shifted-cell frames still to come, not from this state alone.
- **Glyphs:** The standalone 冫 in the mnemonic looks as it did in earlier frames, a small faint mark that is present, not a box.

**Optional point (supports earlier optional item):** The long "source-only … inspected families" cell in the narrow third column becomes a very tall, edge-clipped block on a phone-width screen. This is extra evidence for the optional plain-wording suggestion about `冶.md:38`, and possibly for moving the qualification out of the table. It is not a defect, because the table is signposted for scrolling and the full qualification is repeated in prose at lines 40–43.

No defect is established in this resource.

## Turn 15: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-kanji-06.png

**Resource 15 of 26: `n1-081-kanji-06.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Readings table:** The whole table is visible vertically, with the scroll signpost. The ヤ row shows "on" and "冶金 やきん — metallurgy" (linked). The い.る row shows "kun", and its cell now runs to "…the inspected families", with only the right edge clipped ("dicti…", "n…", "w…").
- **Prose after the table:** Matches source lines 40–43 in full: "鋳る (いる), "cast metal," is a separately documented spelling, not proof of a word written 冶る…". Both 鋳る and 冶る render correctly. This prose repeats the full qualification, so the clipped table cell loses no essential content.
- **Common words:** The bullets are "冶金 やきん — metallurgy" (linked) and "冶金学 (やきんがく) — metallurgy as a science", matching lines 47–48.
- **Notes:** The heading is visible at the bottom.

The edge-clipped letters still need to be checked against the shifted-cell frame later (kanji-15). The tall cell is still only the optional wording point.

No defect seen in this resource.

## Turn 16: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-kanji-12.png

**Resource 16 of 26: `n1-081-kanji-12.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Readings table, scrolled sideways:** The table has been scrolled horizontally, so the left labels are cut off: "ading" instead of "Reading", the ヤ cell has gone out of view, and only "る" of い.る remains. The Type column ("on" / "kun") and the Typical words column are now fully in view.
- **い.る row:** The cell now reads in full, with no edge clipping: "source-only character-dictio / nary lookup information; no exact modern word example written 冶る was established in the inspected families". This matches source line 38.
- **ヤ row:** "冶金 やきん — metallurgy" (linked) is intact.
- **Prose and Common words below:** Same as resource 15 and matching the source.

**Assessment together with the earlier frames:** The unscrolled frames showed the row labels (ヤ / い.る, on / kun), and this scrolled frame shows the whole third-column text. Together they confirm that the signposted scroll exposes all of the table content. The earlier edge-clipping is resolved, and it is not a defect. The tall cell is still only the optional wording point.

No defect seen in this resource.

## Turn 17: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-kanji-18.png

**Resource 17 of 26: `n1-081-kanji-18.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Spelling prose, end of Readings:** Matches lines 40–43, with 鋳る (いる) and 冶る rendered correctly.
- **Common words:** 冶金 やきん — metallurgy (linked) and 冶金学 (やきんがく) — metallurgy as a science.
- **Notes:** Fully visible and matching lines 52–67.
  - The 治 link is followed by "three water strokes, 氵, rather than 冶's two strokes, 冫."
  - The 始 and 女 links are present.
  - 鍛冶 (かじ), "ジ" and "たんや for 鍛冶" are shown, along with the 溶 and 溶かす (とかす) links.
  - The metadata, JMdict and Daijisen/字通 source links are present.
- **冫 versus 氵 in the contrast sentence:** In the sentence that teaches the difference, 氵 shows three marks and 冫 shows two. They are small and light, but distinguishable side by side, so the two-versus-three distinction isn't lost.
- **Glyphs:** 鍛冶, 冶 and 溶 have no boxes or substitutions, and nothing overlaps or is clipped.

This supports the earlier resolution of the 冫 concern: the strokes are legible, though faint, and physical-phone legibility remains unverified.

No defect seen in this resource.

## Turn 18: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-kanji-backlink.png

**Resource 18 of 26: `n1-081-kanji-backlink.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Destination card:** The 冶 card is open ("冶 smelt; work metals"), arrived at by following the 冶 link from the 冶金 word article. The frame shows the Readings section.
- **Readings table:** Back at the left scroll position. The ヤ row shows "on" and "冶金 やきん — metallurgy" (linked). The い.る row shows "kun" and the source-only cell, edge-clipped as in resource 15. The full text was confirmed in the scrolled frame (resource 16).
- **Rest of the screen:** The spelling prose (鋳る / 冶る), Common words (冶金 やきん; 冶金学 (やきんがく)) and the Notes heading match the source.

The frame is the same as resource 15 and consistent with it. From the pixels, it confirms that the destination of the 冶金 → 冶 link is the 冶 card. That the tap started at the right offset in the 冶金 article, and the back-stack behaviour, come from the supplied route evidence.

No defect seen in this resource.

## Turn 19: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-meaning-feedback.png

**Resource 19 of 26: `n1-081-meaning-feedback.png`**

What the pixels show (the view may have been downscaled; all text is legible):

- **Quiz:** A large 冶, clearly drawn with 冫 and no boxes, under "Correct!".
- **Choices:** "two (formal numeral)", "chrysanthemum", "✓ smelt; work metals" (green) and "moreover; also", followed by the answer line "smelt; work metals", "Next" and "I guessed".
- **Article preview:** Matches the source.

**Unexpected wrong choices:** None of the three wrong choices is a curated title: "govern; heal" (治), "stand, machine counter" (台) and "begin, start" (始) are all absent. The shown labels look like other cards' titles, probably N1 cards. My guess is that the app takes wrong choices from the active N1 stack, which would exclude the N3–N4 curated cards. These pixels can't establish that mechanism.

This contradicts the premise I was given that the default meaning quiz uses the three curated choices 治, 台 and 始. Those cards' titles were checked in the textual review, but in this captured question the visual look-alike contrast the distractors were meant to provide didn't appear.

For this question there is no ambiguity: the shown wrong labels have nothing in common with "smelt; work metals", so only one answer is defensible.

**Classification:** This is a runtime discrepancy affecting the claim that the curated distractors are used. It is not a defect in the batch's article content.

## Turn 20: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-meaning-question.png

**Resource 20 of 26: `n1-081-meaning-question.png`**

What the pixels show (the view may have been downscaled; all text is legible):

- **Header:** The "Quiz" screen shows "Attempts left: 1" and the note about queued repeats.
- **Kanji:** A large, heavy-Gothic 冶 (a third typeface, consistent with varied fonts being enabled). It has two clearly separate 冫 strokes, a 台-shaped right side and no boxes.
- **Question:** "What does it mean?", with choices "two (formal numeral)", "chrysanthemum", "smelt; work metals" and "moreover; also", plus "I don't know". No answer is preselected.

This confirms resource 19: the wrong choices offered in the question were already the non-curated titles, before any answer. None of 治 "govern; heal", 台 "stand, machine counter" or 始 "begin, start" appears.

Only "smelt; work metals" can be correct here. The discrepancy is runtime: the three curated distractors were not used in this captured N1-stack question, so this capture gives no visual evidence that they are. I can't tell the cause from the pixels. It isn't a defect in the article content, and no ambiguous choice is shown.

## Turn 21: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-selection.png

**Resource 21 of 26: `n1-081-selection.png`**

What the pixels show (the view may have been downscaled; all text is legible):

- **Header:** The "Kanji" screen shows "N1 · 113 cards", with the N1 chip selected in the row N5 / N4 / N3 / N2 / N1 / All / "St…". The last chip is cut off at the edge of the horizontally scrolling row, which is normal.
- **Stack description:** "Only cards tagged N1." and "Each stack keeps its own review schedule."
- **Study sections:**
  - Meaning quiz: "1 due, 0 new", with Start.
  - Drawing: "0 due, 1 new", with Start.
  - Readings (on'yomi and kun'yomi): "1 due, 0 new", with Start.
- **Browse all kanji** button at the bottom.

**Consistency with supplied evidence:** The counts match the supplied fixture: the 冶 meaning question and the single ヤ reading question due, and drawing new. Here the readings section shows one due item, consistent with only one selected reading key.

**Bearing on resources 19–20:** "Only cards tagged N1" fits the guess that wrong meaning choices come from the active N1 stack, which would exclude the N3/N4 cards 治, 台 and 始. That mechanism is still not proven from pixels.

The accessibility tree's "All · 0 cards / Loading" state from resource 1 doesn't appear here, which supports reading it as a transient state when the tree was dumped.

No content defect seen in this resource.

## Turn 22: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-system-back-to-kanji.png

**Resource 22 of 26: `n1-081-system-back-to-kanji.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Destination:** After the system Back gesture, the screen shows the 冶 card ("冶 smelt; work metals") again.
- **Content:** The spelling prose, the Common words section (冶金 やきん linked; 冶金学) and the full Notes all match the source and are the same as resource 17. That includes 氵 (three marks) against 冫 (two marks), 鍛冶 (かじ), ジ, たんや, the 溶 / 溶かす links and the source links.
- **Glyphs:** No boxes, clipping or overlaps.

From the pixels, this frame confirms that system Back returned from the 冶金 word article to the 冶 card at Common words, where the original link was tapped. That the screens were visited in this order is supplied route evidence, not something a still frame proves.

No defect seen in this resource.

## Turn 23: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-word-02.png

**Resource 23 of 26: `n1-081-word-02.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Header:** The 冶金 word article is open, headed "冶金 metallurgy" and scrolled to "Meaning".
- **Meaning:** The definition matches lines 14–16.
- **Examples:** Both match the source exactly:
  - 大学で冶金を学んでいます。 (だいがくでやきんをまなんでいます。) — "I am studying metallurgy at university."
  - 冶金について研究しています。 (やきんについてけんきゅうしています。) — "I am doing research on metallurgy."

  The Japanese, kana, particles (で, を, について), ている forms and English are all intact.
- **Phrase glosses:** 冶金を学ぶ (やきんをまなぶ) and 冶金について (やきんについて) are shown with their meanings.
- **How the kanji combine:** Shown with the 冶 (ヤ) and 金 (キン) links.
- **Synonyms and antonyms:** Visible down to "製錬 and 精錬 (both せいれん) concern smelting or…". The next line is cut at the bottom of the frame, and resource 11 already showed it in full.

The body's "冶金 (やきん) — metallurgy" heading is above this scroll position, but the reading やきん is visible in the examples.

No blank glyphs, overlaps or mismatches. No defect seen in this resource.

## Turn 24: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-word-07.png

**Resource 24 of 26: `n1-081-word-07.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Header:** The 冶金 word article is open, headed "冶金 metallurgy" and scrolled to "How the kanji combine".
- **How the kanji combine:** The 冶 (ヤ) and 金 (キン) links are shown, and the action-plus-object wording is labelled as a meaning aid, not word history.
- **Synonyms and antonyms:** 冶金学 (やきんがく), the 金属 (きんぞく) link, 製錬/精錬 (せいれん) and the line about there being no everyday opposite.
- **Distinctive meaning:** It says the word is not about money and not limited to gold, gives 錬金術 (れんきんじゅつ) "alchemy", and has the 溶かす (とかす) link.
- **Sources:** The JMdict line is shown, and the "Scope: 世界大百科事典: 冶金." line is slightly clipped at the bottom edge but legible.

The frame is the same as resource 11 and matches source lines 28–54. There are no blank glyphs and no overlaps.

No defect seen in this resource.

## Turn 25: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-word-09.png

**Resource 25 of 26: `n1-081-word-09.png`**

What the pixels show (the view may have been downscaled; the text is legible):

- **Header:** The 冶金 word article is open, headed "冶金 metallurgy", from "How the kanji combine" through to the end of the article.
- **Content:** Matches source lines 28–54. It includes the 冶 (ヤ) and 金 (キン) links, the meaning-aid caveat, 冶金学 (やきんがく), 金属 (きんぞく), 製錬/精錬 (せいれん), the line saying it is not money or gold, 錬金術 (れんきんじゅつ) "alchemy", and the 溶かす (とかす) link.
- **Last line:** "Scope: 世界大百科事典: 冶金." now appears in full, underlined and unclipped. This resolves the bottom-edge clipping seen in resources 11 and 24.

There are no blank glyphs, overlaps or mismatches. No defect seen in this resource.

## Turn 26: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-081-native\attempt-1\n1-081-word-reverse-25.png

**Resource 26/26: `n1-081-word-reverse-25.png`**

I made the one allowed view call for this resource before the conversation history was compressed, and I did not view it again. This observation therefore comes from the notes I kept of that view, not a fresh look at the pixels.

- **What the frame shows:** the 冶金 word article, from "How the kanji combine" to the end. The 冶 (ヤ) and 金 (キン) links appear in the expected formatting.
- **Match with the source:** the text I could see matches `words\冶金.md`. Han characters render normally, with no empty boxes.
- **Clipping:** the "Scope" line is slightly cut off at the bottom edge, as in resources 11 and 24. Resource 25 shows that line fully, so the content can be reached and this is not a defect.
- **Unreadable detail:** the view tool may have shrunk the full frame, so I'm not claiming full-resolution detail. I did not check any file hashes.

No content defect found for this resource.

## Turn 27: FINAL REPORT

# SAME081 visual confirmation of batch 081 (冶, 冶金, 金 bullet): final report

All three in-scope items are CLEAN on every facet, and I found no defects. The only surprise is that the captured meaning question used different wrong choices from the three the article names (治 / 台 / 始); that is a limit on what was tested, not an article error.

## Snapshot
- **Reviewer model:** Claude Opus 5.5 (claude-opus-5.5).
- **Teaching snapshot reviewed:** b7bf953d137251f179a57128bb84bd70a37737c8.
- **Evidence HEAD:** 824045ee9eefca3c7ee883a7b7687d72a52d4f96.
- **Native archive:** 95a87783.
- **Files:** the article hashes in the source packet (`冶.md` 803fdcda…, `冶金.md` 4bf61335…, `金.md` 96bbf429…) match my textual review. I checked them by comparing text only, not with any independent Git or hash tool.

## Scope
**What I read.** Each resource got exactly one view call in its own turn, with nothing reread:
- the complete visual source packet (no truncation marker shown);
- 25 original PNGs, which the host says cover all 45 captures after byte-for-byte deduplication.

**Resource 26.** I viewed it before my conversation history was compressed, so my observation for it came from notes of that view, not a fresh look at the pixels.

**Image quality.** The view tool may have shrunk the frames. I make no full-resolution claims.

**Items reviewed:**
- the new `kanji\冶.md`;
- the new `words\冶金.md`;
- only the added `金.md` bullet, "冶金 やきん — metallurgy".

**What is inherited.** My lexical conclusions carry over from the textual review; I did no fresh dictionary lookups. The existing evidence from all 40 font families is inherited, not re-reviewed.

## Verdicts

| Item | Correctness | Scoped coverage | Bounded visual comprehensibility |
|---|---|---|---|
| `冶.md` | CLEAN | CLEAN | CLEAN |
| `冶金.md` | CLEAN | CLEAN | CLEAN |
| `金.md` bullet | CLEAN | CLEAN | CLEAN |

CLEAN means no established, actionable defect within scope. It is not exhaustive certification.

## Findings
**None.** The textual lexical conclusions are unchanged:
- **Readings:** the full source order is ヤ, then kun い.る. Only ヤ is selected, with an empty kun list.
- **いる:** the kun reading い.る is shown as dictionary information only. It is not evidence for a modern verb 冶る, and 鋳る is kept separate.
- **冶金 (やきん):** taught as technical metallurgy, not gold, money, a single melting or casting step, or alchemy.
- **鍛冶:** かじ is treated as a whole-word reading, with たんや kept separate and no invented ジ reading.
- **Teaching aids:** the mnemonic is qualified and not presented as etymology.
- **Facts:** seven strokes, grade 8 and radical 冫 (15) as opposed to 氵. N1 is a community level, not an official syllabus, and no word level is inferred.

**What the pixels show:**
- **Fonts:** all 29 scoped Han characters render in Gothic, Mincho, Textbook and Brush across the three panels, with no blank or replacement boxes.
- **Look-alikes:** 冶, 治, 台 and 始 are distinct, and 冫 (two marks) can be told apart from 氵 (three). 冶金 renders as a whole word in every family.
- **Reading question:** offers ヤ / ヤク / シ / ヘイ with one correct answer. The feedback "smelt; work metals: ヤ、いる" shows the full kun list, but no kun question was offered.
- **Done screen:** "1 of 1 answers correct."
- **Meaning quiz:** the prompt was 冶. The wrong choices captured were "two (formal numeral)", "chrysanthemum" and "moreover; also", not the curated 治 / 台 / 始. Only one answer was defensible. This is recorded under Limits, not as a finding.
- **Links:** the 冶 ↔ 冶金 and 金 ↔ 冶金 destinations show up in the frames, and the 金 bullet is linked and formatted correctly. System Back returned to the 冶 card.
- **Tables:** the long い.る cell is cut off before scrolling but fully readable in the scrolled state; the scroll is signposted. The 冶金 "Scope" line is cut off in three frames but fully visible in one.
- **Selection:** "N1 · 113 cards".

## Optional (my original suggestions, kept)
1. `冶.md:38`: make the "inspected families" and "source-only" wording plainer. The visuals support this: the cell wraps to about ten lines on the emulator screen.
2. `冶.md:52–58`: note that the dictionary marks 鍛治 as an irregular spelling and that たんや uses the regular ヤ reading.
3. `冶金.md:45–46`: mention the "money-making" sense of 錬金術.
4. `金.md:39`: consider adding a "(technical)" label.
5. `冶.md:64`: give the KANJIDIC2 version.
6. New, app-level: the standalone 冫 in prose renders small and faint. It is legible, but a more prominent rendering would help.

## Limits
**Earlier runtime and rendering limits, reconciled:**
- **Glyphs:** resolved, but only for emulator pixels.
- **冫 vs 氵:** partly resolved. They are distinguishable but faint, and legibility on a physical phone is unverified.
- **Clipped tables:** resolved by looking at the scrolled and unscrolled states together.
- **Links and Back:** the destinations are visible in pixels; the tap order comes only from the supplied route evidence.
- **Curated meaning distractors (治 / 台 / 始):** unresolved. They were not captured at runtime and the cause is unknown. I make no claim about whether every possible random set of choices is safe.

**What comes only from supplied evidence, not from pixels:**
- the ContentSync result (1093 kanji, 5049 words, 113 N1 cards, version f1dd5d8b9d2ff535, zero problems, epoch 1);
- the Full/Lite readings and quiz keys, the persisted good log, the seeded fixture state and offline status;
- 2/2 tests passing on emulator-5580 (API 35, read-only) and the stopped helper process;
- the 116 individual and 4 whole-word Paint assertions, which are not PNG reads.

Pixels, Paint.hasGlyph results and raster hashes do not identify which fallback font face was used.

**Drawing:** this was a shape-only comparison of seven injected reference strokes. It is not human handwriting, real recall, ML Kit recognition or a model download; the screen showed the handwriting model as unavailable.

**Not covered at all:**
- independent Git or upstream verification and fresh dictionary lookups;
- full-resolution or hash checks of the images;
- a physical phone;
- native-speaker review or learning-effectiveness evidence.

Final integration with current main, publication, CI, the immutable ZIP, the physical phone, general release and the whole-set review are still outstanding.
