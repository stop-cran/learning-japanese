## Turn 1: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-visual-source-packet.txt

I've read resource 1/26, the packet. This is an observation for this resource only, not a verdict.

**Read:** one `view` call with `forceReadLargeFiles=true` and no `view_range`. The tool showed no truncation, and the text ran to "EXACT TEACHING DIFF SINCE ORIGINAL TEXTUAL REVIEW: EMPTY."

**What the packet shows:**
- **Teaching text:** The kanji and word 凜 articles match the text I reviewed earlier (same SHA256 values), and the teaching diff is empty.
- **Test run:** two cases, `OK (2 tests)`, with `adbExitCode` 0. The route JSON reports 1096 kanji, 5053 words, 116 N1 cards, 0 problems, version 74b87b47347b78c1 and reading parser epoch 1. It also records:
  - full on リン and kun きびし.い;
  - one on key, りん, and no kun keys;
  - exact options 凜, 准, 冗, 凹 in both the N1 (116) and All (1096) pools;
  - one reciprocal pair (two directions), offline, and `phoneEvidence` false.
  These are supplied claims, not tests I ran.
- **Font rasters:** 冫, 凛, 凜 and 稟 each produce the same raster hash in all four font families, which fits a shared fallback face. In every family, 凜 and 凛 hashes differ. Hashes only show distinct pixels; they don't establish readability. I need the PNGs to judge the 禾 vs 示 contrast.
- **Captures:** `execution.json` lists 42 PNGs (3 font panels and 39 route captures), which matches the 42 captures stated.

**Pending:** the 25 deduplicated PNGs, which haven't been read yet.

## Turn 2: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-curated-on-done.png

Resource 2/26 (`n1-084-curated-on-done.png`): the reading session's completion screen renders cleanly.

- **What it shows:** the "Kanji readings" screen with "← Back", "Session complete", "1 of 1 answers correct." and the buttons "Done" and "Practice more". The emulator status bar shows 7:53.
- **Condition:** no blank areas, replacement boxes or clipped text. Everything is legible at the returned size (about 900×2000; it may have been resized).
- **Relevance:** this fits the claim of one reading answered correctly, then Done. The screen doesn't show 凜, the reading りん, the persisted log or kun suppression, so those rest on the route JSON and test code.

## Turn 3: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-curated-On-feedback.png

Resource 3/26 (`n1-084-curated-On-feedback.png`): the on'yomi feedback screen renders correctly. One app-level point to carry forward: the feedback line shows the source-only kun reading.

- **Large glyph:** 凜 is fully drawn. I can see the two 冫 marks, then 亠 and 回 on the right, with a 禾-shaped bottom (a slanting top stroke over 木). There is no box or blank.
- **Answer:** "Correct! — on'yomi" with ✓ リン highlighted green. The other choices are ジュン, オウ and ジョウ, the on readings of 准, 凹 and 冗.
- **Feedback line:** "dignified; bracing cold: リン、きびしい". This is the app's full-reading summary, so it includes the source-only kun きびしい without the article's qualification. The article immediately below explains that limit, and kun isn't being quizzed. I treat this as app display behaviour, not a teaching defect, and will carry it forward as an observation.
- **Article below:** the heading, the facts line with the 冫 key (small but present) and the "Meaning and origin" paragraph are legible. The inline 凜 link and 凜とした are rendered.
- **Layout:** the "Next" and "I guessed" buttons are intact. Nothing is clipped or replaced at the returned size (about 900×2000; it may have been resized).

## Turn 4: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-curated-On-question.png

**Resource 4/26: `n1-084-curated-On-question.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes.

- **Screen:** "← Back", the title "Kanji readings", "Attempts left: 1" and the note about queued repeats are all fully legible.
- **Prompt glyph:** a large 凜 is drawn cleanly, with no blank area or replacement box.
  - On the left are the two 冫 marks.
  - On the right are 亠, then 回, then a bottom with one long horizontal stroke, a central vertical and two long sweeping diagonals. That bottom is 禾/木-shaped, not 示 (示 would have a 二 top and small side dots). It matches 凜, not 凛.
  - I can't clearly make out the short slanted top stroke of 禾 as separate from the strokes around it at this resolution, but the overall bottom component is clearly not 示.
- **Question:** "Pick the on'yomi" with four choices, ジュン / オウ / リン / ジョウ. These match the 准/凹/凜/冗 readings, with リン as the correct key. No kun choice is offered. Below the choices is "I don't know".
- **Layout:** nothing is clipped or overlapping, and the lower part of the screen is empty background.
- **Issues:** I found no defect in this capture.

## Turn 5: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-drawing-feedback.png

**Resource 5/26: `n1-084-drawing-feedback.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Header:** "← Back", the title "Drawing", then "凜 dignified; bracing cold", "Practice only: this attempt is not graded." and "Well drawn!" in green.
- **Drawing panels:**
  - "Your drawing" (blue) and "Correct strokes" (green) both show 凜, with the two 冫 marks, 亠, 回 and a 禾/木-type bottom (long horizontal, central vertical, two sweeping diagonals). Neither shows a 示 bottom.
  - The reference panel numbers strokes 1–15. Labels 13, 14 and 15 crowd together at the bottom junction, so the exact order there is hard to read at this resolution.
  - The blue strokes are the reference-injected touch input, not human handwriting.
- **Grading note:** "Graded by stroke shapes only (handwriting model not available)." This honestly says the model isn't available. Next to "Practice only: … not graded", the two uses of "graded" could look contradictory, but I read the first as "no scheduling credit" and the second as how the feedback was judged. That is app wording, not a teaching defect.
- **Article excerpt:** below "Next" the article starts.
  - The heading "凜 — dignified; bracing cold" and the facts line are shown: 15 strokes, radical 冫 "(the two left-hand marks, no. 15)", "JLPT: N1 (community list)".
  - "Meaning and origin" includes the linked 凜 (りん), 凜とした before a noun, the clear ringing sound sense, and the sentence about "strict".
  - "Modern-shape mnemonic, not etymology" starts, with 冫 and the plain-text 稟 (りん). The text is cut off at the bottom edge only because of where the screen is scrolled.
- **Glyphs:** 冫, 凜 and 稟 are drawn cleanly and are legible, with no replacement boxes, blank areas or clipping other than the scroll cut-off.

## Turn 6: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-drawing-recall-feedback.png

**Resource 6/26: `n1-084-drawing-recall-feedback.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Header:** "← Back", the title "Drawing", then "凜 dignified; bracing cold" and "Here is the kanji" in red, which is consistent with the give-up/recall reveal.
- **"Your drawing":** the panel is empty white. That is expected for the give-up path, not a rendering failure.
- **"Correct strokes":** the green 凜 is complete.
  - Its strokes are numbered 1–15: the two 冫 marks (1, 2), then 亠, 回 and a 禾-shaped bottom (12 short slant, long horizontal, vertical, two diagonals). There is no 示 bottom.
  - The labels 14, 13 and 15 sit near the bottom junction, placed differently from the earlier feedback capture. They are crowded but readable.
- **Article excerpt:**
  - The heading, the facts line (15 strokes, radical 冫, "no. 15", "N1 (community list)") and the Meaning paragraph match the article, including the linked 凜 (りん) and 凜とした.
  - The mnemonic continues further than in the previous capture: "…The bottom of that block has the 禾 shape. This is an invented memory aid,". So the mnemonic is shown as invented and 禾 appears as a visible glyph. 稟 (りん) is plain text and 凜 is linked.
  - The text is cut off at the bottom edge only because of where the screen is scrolled.
- **Glyphs:** 冫, 凜, 稟 and 禾 are drawn cleanly, with no replacement boxes or unexpected blank areas.

## Turn 7: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-drawing-trace.png

**Resource 7/26: `n1-084-drawing-trace.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no teaching or rendering defect in it.

- **Text:** "← Back", the title "Drawing", "Attempts left: 1", the note about queued repeats, "Trace the kanji for", a large "dignified; bracing cold" and "Ungraded tracing practice. You'll try from memory later." are all legible.
- **Trace guide:** the faint blue outline of 凜 is large and complete, with strokes numbered 1–15.
  - Strokes 1 and 2 are 冫; 3 and 4 are 亠; 5–10 are 回; then the bottom.
  - At this size the 禾 bottom is clear: a short top slant (stroke 11), a long horizontal (12), a vertical (13), and the left and right sweeps (14, 15). It is plainly not 示.
  - The labels are readable, with no crowding problem here.
- **Model status:** the line "Downloading the handwriting model (first use only)…" is shown, and Undo/Clear/Check are greyed out.
  - This is a transient state on an offline device. The later feedback capture says "handwriting model not available".
  - So this screen shows no successful download, and I make no claim about recognition.
  - The greyed buttons fit a guide-only frame captured before input.
- **Glyphs:** no replacement boxes, unexpected blank areas or clipping.

## Turn 8: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-font-panel-1.png

**Resource 8/26: `n1-084-font-panel-1.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no glyph failure in it.

- **Panel text:** the header "Batch 084: dignified / look-alikes / radical fallback", "Panel 1 / 3", and sections for Gothic, Mincho, Textbook and Brush.
- **Characters shown:** each section shows the same 24 Han in order: 冗 冫 冴 冷 准 凍 凛 凜 凹 厳 声 寒 揚 明 朗 朝 気 澄 激 確 示 禾 稟 透.
  - 通, 険, 静 and 鷹 are not in this panel; presumably they are on panels 2 or 3, which I haven't viewed yet.
  - The footer reads "Inspect all 28 scoped Han; focused 凜/凛/冫/稟 and 禾/示, 准/冗/凹. Fallback families may coincide."
- **Rendering:** all 96 glyph instances are drawn, with no blank areas or replacement boxes.
  - In Textbook and Brush, 冫, 凛, 凜 and 稟 visibly switch to a plainer Gothic-like face. This fits the shared-fallback raster hashes, and it changes the typeface only; it is not a failure.
  - The section typefaces otherwise differ visibly: Mincho has serifs, Textbook is lighter with wider spacing, and Brush is heavy and calligraphic.
- **Look-alikes:** 示 and 禾 are clearly distinct in every family. 准/冗/凹 are distinct, and 冫 is visible as two marks.
- **Limit:** at this returned size, the 凛 (7th) versus 凜 (8th) bottom components are too small for me to tell 示 from 禾 with confidence in any family. So this panel alone does not visually confirm that 凛 and 凜 are distinct. I rely on the earlier larger captures and the raster hashes for that.

## Turn 9: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-font-panel-2.png

**Resource 9/26: `n1-084-font-panel-2.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no glyph failure in it.

- **Panel text:** the same header, "Panel 2 / 3", and sections for Gothic, Mincho, Textbook and Brush. Each section shows the remaining four scoped Han: 通 険 静 鷹. The footer instruction is the same as on Panel 1.
- **Rendering:** all 16 glyph instances are drawn, with no blank areas or replacement boxes.
  - The typefaces visibly differ: Mincho has serifs, Textbook is lighter with wider spacing, and Brush is heavy and calligraphic.
  - In Brush, 険 and 鷹 are especially stylised but still recognisable.
- **Coverage:** together with Panel 1 (24 characters), these four make up all 28 scoped Han.
- **Layout:** the lower two-thirds of the frame is empty background, which is expected for a short panel. There is no clipping.
- **Limit:** at this size I can't verify every fine stroke of 険 or 鷹, but their overall shapes are clearly recognisable.

## Turn 10: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-font-panel-3.png

**Resource 10/26: `n1-084-font-panel-3.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no glyph failure or defect in it.

- **Panel text:** the header, "Panel 3 / 3", and the focused set in each of Gothic, Mincho, Textbook and Brush: 凜 凛 冫 稟 禾 示 准 冗 凹 凜とした 凛とした. The footer is the same as on the other panels.
- **Rendering:** every glyph is drawn, with no blank areas or replacement boxes.
- **凜 vs 凛:** the 1st and 2nd glyphs look distinct in every family. In the first, the bottom has a 禾 shape with long sweeping diagonals; in the second, the bottom is a lighter 示 shape. The same holds for the leading characters of 凜とした and 凛とした.
  - I'm only moderately confident about the fine strokes at this size.
  - The within-family raster-hash difference between 凜 and 凛 supports that they are distinct, but that is not proof of readability.
- **Other look-alikes:** 稟 and 冫 are recognisable. 禾 and 示 are clearly different from each other, and 准, 冗 and 凹 are clearly distinct.
- **Fallback:** in Textbook and Brush, 凜, 凛, 冫 and 稟 (and the Han in the two phrases) use the plainer Gothic-like fallback face, while 禾, 示, 准, 冗, 凹 and the kana for とした take on the family's own style. That is a typeface change only and fits the shared-fallback hashes.
- **Wrapping:** in Textbook, the final た of "凛とした" wraps onto the next line. All the text is still there, so it is harmless.

## Turn 11: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-kanji-01.png

**Resource 11/26: `n1-084-kanji-01.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Header:** "← Back", the title "凜 dignified; bracing cold" and the "Article contents" link.
- **Body:** the heading "凜 — dignified; bracing cold" and the facts line: 15 strokes, radical 冫 "(the two left-hand marks, no. 15)", "JLPT: N1 (community list)".
  - "Meaning and origin" is complete, including the linked 凜 (りん), 凜とした before a noun, the ringing sound sense, and the sentence about "strict".
  - The full mnemonic paragraph is now visible. It ends: "…The bottom of that block has the 禾 shape. This is an invented memory aid, not a verified historical or phonetic explanation." This flags the mnemonic correctly without denying that there is a phonetic component.
- **Readings:** "Both source readings are preserved in source order. Only リン is selected for reading practice; there are no selected kun questions." Then "Scroll sideways to read all columns." and the table headers Reading / Type / Typical words.
  - The first row is リン / on / linked 凜 りん — "dignified; bracing cold, a…". The text is cut at the right edge. That is the sideways-scroll viewport, not lost content, so I'll judge the table as a whole across the captures.
- **Glyphs:** 冫, 凜, 稟 and 禾 are drawn and legible, with no replacement boxes or unexpected blank areas.

## Turn 12: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-kanji-03.png

**Resource 12/26: `n1-084-kanji-03.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Scroll position:** a little further down than kanji-01. The title bar is the same, and "Meaning and origin" and the full mnemonic paragraph (ending "…not a verified historical or phonetic explanation.") are legible again.
- **Readings intro:** the same as in kanji-01, followed by "Scroll sideways to read all columns."
- **Reading rows:** both are now visible, in source order.
  - Row 1: リン / on / linked 凜 りん — "dignified; bracing cold, a[…] in 凜とした".
  - Row 2: きびし.い / kun / "source-only character-dicti[…]nary lookup information; n[…] exact non-nam[…]". This is the bounded kun limit, worded as source-only with no invented 凜しい.
- **Right-edge clipping:** text in the Typical words column is cut at the right edge (for example "dicti…nary", where the "o" of dictionary falls outside the viewport, and "n…" and "non-nam…"). That fits the sideways-scroll viewport and does not show lost content. I'll judge it together with the shifted-table captures.
- **Bottom edge:** the next line is just starting at the very bottom of the frame and is unreadable there.
- **Glyphs:** 冫, 凜, 稟 and 禾 are drawn and legible, with no replacement boxes.

## Turn 13: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-kanji-06.png

**Resource 13/26: `n1-084-kanji-06.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Readings table:** the Readings intro is followed by the full vertical extent of the table.
  - Row 1: リン / on / linked 凜 りん — "dignified; bracing cold, a[…] in 凜とした".
  - Row 2: きびし.い / kun / "source-only character-dicti[…]nary lookup information; n[…] exact non-nam[…] example established in the inspected families".
  - Text is still cut at the right edge of the sideways-scroll viewport (dicti…nary, n…, nam…). I'll judge that together with the shifted-table captures; it does not show lost content.
- **Bounded-limit paragraph:** it is fully legible.
  - "Do not invent a spelling such as 凜しい from the source-only row."
  - "The ordinary adjective 厳しい (きびしい) is a different spelling, not evidence for an example written with 凜." Here 厳しい is linked.
  - "This is a bounded evidence limit, not a claim that no dictionary could record such a form."
  - This is correct, and it does not overstate the limit as a rule that the form cannot exist.
- **Common words:** the section starts with "• linked 凜 りん — dignified; bracing cold". The second bullet, "• 凜とした声 (りんとしたこえ) — a clear, firm voice…", is cut by the bottom edge of the frame. I can mostly read it, but the bottom of the glyphs is clipped, so it should show fully in the next scroll state.
- **Glyphs:** 凜 and 厳 are drawn cleanly, with no replacement boxes.

## Turn 14: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-kanji-12.png

**Resource 14/26: `n1-084-kanji-12.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Table scrolled sideways:** the table is now shifted left.
  - The left labels are clipped ("ading", "ン", "びし.い"). That is the sideways shift; the earlier frames show those labels in full.
  - The Typical words column is now complete.
  - Row 1: "凜 りん — dignified; bracing cold, as in 凜とした", with 凜 linked.
  - Row 2: "source-only character-dictionary lookup information; no exact non-name example established in the inspected families".
- **Table as a whole:** together with kanji-01, -03 and -06, every cell's text is retained across the scroll states. Nothing is missing, and the "Scroll sideways" instruction explains the behaviour.
- **Rest of the frame:** the "Do not invent… 凜しい…厳しい (linked)…bounded evidence limit…" paragraph is complete and legible, and "Common words" begins with the linked 凜 りん bullet.
  - The second bullet, 凜とした声 (りんとしたこえ) — "a clear, firm voice…", is again cut off by the bottom edge of the frame. It is mostly readable, but the bottom of the glyphs is clipped.
- **Glyphs:** no replacement boxes.

## Turn 15: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-kanji-18.png

**Resource 15/26: `n1-084-kanji-18.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Common words:** all three bullets are now fully visible.
  - 凜 りん (linked) — "dignified; bracing cold".
  - 凜とした声 (りんとしたこえ) — "a clear, firm voice".
  - 凜とした朝の寒気 (りんとしたあさのかんき) — "the bracing chill of the morning".
  - The examples are unlinked, and the kana and translations are legible.
- **Notes:**
  - "凛 is a recognized variant of 凜, with the same りん reading in the linked word's dictionary family. Compare the lowest right-hand part: 凜 has 禾, while 凛 has a 示-shaped bottom (示 linked)."
  - "They are different characters for typing and this card's identity; practice writing the displayed 凜."
  - "No separate variant card or personal-name reading course… grade-9… name-use kanji, not name-only usage."
  - 凛 stays plain text.
  - At body-text size, the 凜 and 凛 glyphs are both drawn. I can't make out their tiny bottom strokes reliably at this size, so the visual contrast depends on the larger captures and the font panels.
- **Look-alike paragraph:** 准 (bird-shaped right side), 冗 (cover-like top) and 凹 (sunken outline) are linked, with "Their meanings are not dignified bearing or bracing cold."
- **Metadata line:** linked KANJIDIC2, database 2026-306, 2026-11-02; linked JMdict, entry 1564320; and linked "Digital Daijisen: 凜".
- **Rendering:** the earlier clipped bullet is resolved, and there are no replacement boxes or clipping.

## Turn 16: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-meaning-feedback.png

**Resource 16/26: `n1-084-meaning-feedback.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Quiz screen:** "← Back", the title "Quiz", and a large 凜 with the two 冫 marks, 亠, 回 and a 禾-type bottom (long sweeping diagonals, not 示).
- **Answer:** "Correct!" in green. The four meaning choices are "quasi-; associate rank", "✓ dignified; bracing cold" in green, "superfluous; redundant" and "concave; sunken".
  - These are exactly the curated labels for 准, 凜, 冗 and 凹, with no fallback padding. They are clearly distinct from each other.
- **Feedback line:** it reads only "dignified; bracing cold". Unlike the on-reading feedback (resource 3), it doesn't show the source-only kun きびしい.
- **Buttons:** "Next" and "I guessed".
- **Article below:** the heading, the facts line (15 strokes, radical 冫, no. 15, "N1 (community list)") and the complete "Meaning and origin" paragraph, including the linked 凜 (りん) and 凜とした. All of it is legible.
- **Rendering:** no replacement boxes, blank areas or clipping.

## Turn 17: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-meaning-question.png

**Resource 17/26: `n1-084-meaning-question.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Header:** "← Back", the title "Quiz", "Attempts left: 1" and the note about queued repeats.
- **Prompt:** a large 凜 with the two 冫 marks, 亠, 回 and a 禾-type bottom (long horizontal, vertical and two long sweeps). It is not a 示 bottom.
- **Choices:** under "What does it mean?" are four:
  1. quasi-; associate rank
  2. dignified; bracing cold
  3. superfluous; redundant
  4. concave; sunken
  - These are the curated labels for 准, 凜, 冗 and 凹, with no fallback padding. Each is clearly a different meaning, so none is ambiguous with 凜'''s label.
  - "I don't know" follows the choices.
- **Rendering:** all of it is legible. There are no replacement boxes or clipping, and the lower part of the frame is empty background.

## Turn 18: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-selection.png

**Resource 18/26: `n1-084-selection.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Header:** "← Back", the title "Kanji", and "N1 · 116 cards", which matches the N1 selection of 116 cards.
- **Level chips:** N5 / N4 / N3 / N2 / N1 (selected, highlighted) / All, then a chip clipped at the right edge as "St…".
  - The clipped chip looks like the start of a horizontally scrollable chip row. I can't identify it from this frame.
  - Below the chips: "Only cards tagged N1." and "Each stack keeps its own review schedule."
- **Stacks:**
  - Meaning quiz: "1 due, 0 new" with Start.
  - Drawing: "0 due, 1 new" with Start.
  - Readings (on'yomi and kun'yomi): "1 due, 0 new" with Start.
  - Then "Browse all kanji".
- **Readings stack title:** it reads "(on'yomi and kun'yomi)", but it is a generic stack title. The 凜 reading quiz itself offered only the リン on-reading question (resource 4), so this doesn't contradict `quizKunyomi: []`.
- **Fixture:** the due/new counts fit the synthetic fixture (Drawing unlocked by the seeded meaning logs). They are not owner progress.
- **Rendering:** no Han glyphs appear in this frame. All text is legible with no unexpected clipping, and the lower part of the frame is empty background.

## Turn 19: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-word-02.png

**Resource 19/26: `n1-084-word-02.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no new defect in it.

- **Title bar:** the title is "凜 dignified; bracing cold". This is the word article: its sections are Meaning, How the kanji combine, and Synonyms.
- **Meaning:** the bearing, bracing-cold and ringing-voice senses. "Learn the constructions **凜と** and **凜とした + noun**, rather than adding な as if this were an ordinary な-adjective."
- **Examples:** both are legible and complete.
  - 凜とした声がひびく。(りんとしたこえがひびく。) — "A clear, firm voice rings out."
  - 凜とした朝の寒気 (りんとしたあさのかんき) — "The bracing chill of the morning."
- **Note on the examples:** it is fully legible.
  - It covers Daijisen as the source, the second example as a noun phrase, としたdescribing the following noun rather than necessarily reporting an earlier change, and "凜と can modify an action."
  - It says JMdict labels the word a *taru adjective* and an adverb taking と, and that this does not make it an い-adjective.
  - This all matches my textual review. "凜と can modify an action" still has no example; that is my original optional suggestion.
- **How the kanji combine:**
  - "single-character Sino-Japanese word, not a compound. 凜 (linked) supplies the whole on reading リン… JMdict also recognizes 凛 (りん) in the same lexical family. The variant spelling does not introduce another pronunciation or word."
  - 凛 is plain text. The "also recognizes" wording is the passage behind C1, which remains optional.
- **Synonyms and antonyms:** the heading starts. The first line, apparently a linked 寒い (さむい)…, is cut off by the bottom edge of the frame and I can't read it here.
- **Rendering:** no replacement boxes.

## Turn 20: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-word-03.png

**Resource 20/26: `n1-084-word-03.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no new defect in it.

- **Compared with word-02:** the visible content is the same as in word-02. The only visible difference is the status-bar time (7:53 instead of 7:52), and the scroll position looks the same.
- **Content:** the Meaning section, both Daijisen examples with kana and translations, the note about examples and taru/と, "How the kanji combine" (with 凛 as plain text and the "also recognizes" wording behind optional C1), and the "Synonyms and antonyms" heading.
  - The first synonym line is again cut off by the bottom edge of the frame and I can't read it.
- **Rendering:** all of it is legible, with no replacement boxes or clipping other than that bottom line.
- **Byte identity:** I can't say whether this frame is byte-identical to word-02 or simply captured at the same scroll position in a later step. I note it as a near-duplicate, not as evidence of an extra scroll state.

## Turn 21: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-word-07.png

**Resource 21/26: `n1-084-word-07.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **How the kanji combine:** shown in full, as in word-02, with 凛 (りん) as plain text. The "also recognizes" wording is still the passage behind optional C1.
- **Synonyms and antonyms:** now fully legible.
  - "寒い (さむい) (linked) is the broader everyday adjective for cold weather or surroundings. 凜とした adds the sharp, bracing quality in the morning example; it is not a neutral substitute for every occurrence of 寒い."
  - "厳しい (きびしい) (linked) can describe severe cold, but also strict standards and harsh circumstances; do not transfer all those uses to 凜."
  - "澄む (すむ) (linked) overlaps for a clear, resonant voice. 冷静 (れいせい) (linked) emphasizes mental composure… not necessarily the dignified outward bearing… Warmth contrasts with the cold sense, but is not an opposite of dignity."
  - All the comparison links show their readings, and the synonym boundaries are appropriately qualified.
- **Distinctive meaning:** "A 凜とした声 can sound clear and firm without being loud, angry or cruel. Likewise, a dignified manner does not establish someone's social rank or moral superiority. Select the translation from what is being described." This avoids generalising to rank, morals or strictness.
- **Wrapping:** the linked 冷静 breaks across a line (冷 / 静), as does 寒 / い. All the text is retained, so this is harmless word-wrapping.
- **Rendering:** no replacement boxes or clipping.

## Turn 22: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-word-09.png

**Resource 22/26: `n1-084-word-09.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no new defect in it.

- **Repeated sections:** "Synonyms and antonyms" and "Distinctive meaning" read exactly as in word-07. The 寒い, 厳しい, 澄む and 冷静 links show their readings, and the rank/moral caution is there.
- **Final paragraph:** now fully visible.
  - "The full dictionary family also records a tense atmosphere sense. This article focuses on bearing, sound and bracing cold; it is not an exhaustive account of every literary or historical construction."
  - "Neither dictionary inclusion nor the variant spelling establishes a frequency ranking."
  - "Personal-name usage is outside this article's scope."
- **Assessment:**
  - The tense-atmosphere sense is disclosed as out of focus. That is appropriate scoping.
  - The frequency disclaimer is the other half of the C1 passage. It is accurate, and C1 remains optional, as I decided in the reconciliation.
- **Rendering:** all of it is legible, with no replacement boxes, clipping or unexpected blank areas.

## Turn 23: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-word-12.png

**Resource 23/26: `n1-084-word-12.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **Scroll position:** this appears to be the end of the word article. The top line ("cold weather or surroundings. 凜とした adds the…") is partly hidden under the title bar, which is ordinary mid-line scrolling, and the full text appears in word-07 and word-09.
- **Repeated sections:** the synonym paragraphs (厳しい, 澄む and 冷静 with readings), "Distinctive meaning" and the scope/frequency/personal-name paragraph are the same as in word-09.
- **Sources line:** "Dictionary: JMdict (linked), entry 1564320, all four senses. Constructions and short example bases: Digital Daijisen: 凜 (linked); adverbial senses: Seisen: 凜と (linked)."
  - The source attribution is complete and legible, and it matches the textual review.
- **Rendering:** no replacement boxes or unexpected blank areas. Nothing is clipped except the partly hidden top line.

## Turn 24: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-word-kanji-backlink.png

**Resource 24/26: `n1-084-word-kanji-backlink.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **What it shows:** this is the kanji article. It has a Readings table, the 凜しい/厳しい bounded-limit paragraph and Common words, so it fits the word → kanji transition of the reciprocal pair. The title bar reads "凜 dignified; bracing cold", and the time is 7:53.
- **Content:** it looks the same as kanji-06.
  - The Readings intro.
  - "Scroll sideways to read all columns."
  - The rows リン / on / linked 凜 りん… and きびし.い / kun / "source-only character-dicti[…]nary…".
  - The full "Do not invent a spelling such as 凜しい… 厳しい (linked)… bounded evidence limit…" paragraph.
  - The start of Common words.
- **Clipping:** the right edge of the table is clipped by the sideways-scroll viewport, as before, and the full text is shown in kanji-12. The 凜とした声 bullet is cut off at the bottom of the frame and is shown in full in kanji-18.
- **Navigation:** the frame alone doesn't show the tap or route that led here. The fact that this was the word → kanji transition comes from the fixture/route evidence and the filename, not from the pixels alone.
- **Rendering:** no replacement boxes or unexpected blank areas.

## Turn 25: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-word-reverse.png

**Resource 25/26: `n1-084-word-reverse.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **What it shows:** this is the word article, at the same scroll position as word-07. The title bar reads "凜 dignified; bracing cold", and the time is 7:53.
- **Content:** it looks the same as word-07.
  - "How the kanji combine": the linked 凜, リン, "also recognizes 凛 (りん)" with 凛 as plain text, and the variant not introducing another pronunciation.
  - "Synonyms and antonyms": 寒い, 厳しい, 澄む and 冷静, linked and with readings.
  - "Distinctive meaning", with the rank/moral caution.
- **Navigation:** the pixels alone don't show that this frame came from the kanji → word reverse transition. Arriving at the word article fits that, but the route evidence comes from the fixture and filename. Taken together with resource 24, the frames are consistent with links working in both directions.
- **Rendering:** all of it is legible, with no replacement boxes, clipping or unexpected blank areas. As before, 冷静 and 寒い break harmlessly across lines.

## Turn 26: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-084-native-retry1\attempt-587\n1-084-word-system-back-to-kanji.png

**Resource 26/26: `n1-084-word-system-back-to-kanji.png`.** I viewed this one capture once, as the image the tool returned (about 900×2000, possibly resized). I can't vouch for the original full-resolution bytes. I found no defect in it.

- **What it shows:** this is the end of the kanji article, at 7:53. It looks the same as kanji-18 (7:52).
  - The tail of the bounded-limit paragraph.
  - Common words: the linked 凜 りん, 凜とした声 and 凜とした朝の寒気, with readings and translations.
  - Notes: the 凛 versus 凜 contrast, with the 禾 bottom versus the 示-shaped bottom (示 linked), "practice writing the displayed 凜", "No separate variant card…", and "grade-9… name-use kanji, not name-only usage".
  - The 准/冗/凹 contrasts, linked.
  - The metadata line with links to KANJIDIC2, JMdict 1564320 and Digital Daijisen: 凜.
- **Navigation:** returning to the kanji article fits a system Back from the word article, with the earlier scroll position kept. The fact that it was a system Back, not the in-app "← Back", comes from the fixture/route evidence and the filename; the pixels can't show it.
- **Rendering:** all of it is legible, with no replacement boxes, clipping or unexpected blank areas.

## Turn 27: FINAL REPORT

# Batch 084 凜: final visual-confirmation report

I found no actionable defect in either new article: both are CLEAN for correctness, scoped coverage and rendered comprehensibility. All the article text was legible across the screenshots, with no blank areas, replacement boxes or collapsed look-alike characters. The one gap is small-size rendering of the variant 凛, which I could only partly confirm.

## Snapshot
- **Teaching content:** 030b144a6aeefc6fe77f76683219832db91bef4f, unchanged according to the packet.
- **Evidence:** HEAD a445a3f154afd5833fa99ba0c6abe13379402e1f; native envelope 53b6819b22787a2517cd0ad14aa855d357cbc70a, content version 74b87b47347b78c1.
- I did not check Git, the hashes or upstream sources myself.

## Scope
- **Model and session:** Claude Opus 5.5 (claude-opus-5.5), continuing the original Batch 084 session. This is a follow-up visual check that depends on my earlier reports, not a new blind language review.
- **What I read:** 26 single `view` calls, one per turn. The first was the complete `batch-084-visual-source-packet.txt`, with no truncation shown. The other 25 were these PNGs:
  - quiz and session screens: curated-on-done, curated-On-feedback, curated-On-question, meaning-question, meaning-feedback, selection;
  - drawing screens: drawing-trace, drawing-feedback, drawing-recall-feedback;
  - font panels 1–3;
  - kanji article: kanji-01, -03, -06, -12, -18;
  - word article: word-02, -03, -07, -09, -12;
  - navigation: word-kanji-backlink, word-reverse, word-system-back-to-kanji.
- **Unverified mapping:** the host says these 25 stand for all 42 captures after removing exact-byte duplicates. I did not verify that mapping. word-forward and the second system-back capture were not served separately.
- **Image size:** each image came back at about 900×2000 and may have been downscaled. I judged only those returned pixels and claim nothing about the original full-resolution bytes.
- **Earlier reports:** the dictionary findings from my initial review and reconciliation stand as written. This stage did not re-review the dictionary families.

## Verdicts

| Article | Correctness | Scoped coverage | Rendered comprehensibility |
|---|---|---|---|
| `kanji\凜.md` | CLEAN | CLEAN | CLEAN |
| `words\凜.md` | CLEAN | CLEAN | CLEAN |

CLEAN means I found no established actionable defect in scope. It is not a guarantee of exhaustive correctness, a native-speaker check, or evidence that the articles help learners.

## Findings
**Proven defects:** none.

What the screenshots confirm:
- **Readings:**
  - The table lists リン (on) then きびし.い (kun), in source order.
  - It says "Only リン is selected… no selected kun questions".
  - The reading quiz offered only リン, against ジュン/オウ/ジョウ.
  - The きびし.い row is marked source-only, and the 凜しい/厳しい paragraph says it is a bounded evidence limit, not a claim the form cannot exist.
  - The table is clipped at the right edge in single frames, but across kanji-01, -03, -06 and -12 every cell's text is present, and the "Scroll sideways" note explains it.
- **Facts and notes:** both are shown in full.
  - The facts line shows 15 strokes, radical 冫 ("the two left-hand marks, no. 15") and "N1 (community list)".
  - The mnemonic is labelled "invented memory aid, not a verified historical or phonetic explanation".
  - The notes say grade 9 means a name-use kanji, not name-only usage.
- **Shapes:**
  - The large 凜 (quiz prompts, tracing guide, stroke panels) clearly has the two 冫 marks, 亠, 回 and a 禾 bottom.
  - 禾 and 示 are clearly different in all four font families.
  - The notes explain the 禾 versus 示 contrast and that the two are different characters for typing and card identity. 凛 and 稟 are plain text.
- **Word article:**
  - The 凜と / 凜とした + noun constructions are explained, with the warning against treating it as an ordinary な-adjective, the point that とした does not have to mean an earlier change, and the qualified taru-adjective / adverb classification.
  - Both Daijisen examples have kana and translations, and the morning example is identified as a noun phrase.
  - The 寒い/厳しい/澄む/冷静 comparisons and the rank/moral/"strict" cautions are legible, as are the scope note on the tense-atmosphere sense and the sources line (JMdict 1564320, Daijisen, Seisen).
- **Meaning quiz:** the four choices are exactly 凜, 准, 冗 and 凹 ("dignified; bracing cold", "quasi-; associate rank", "superfluous; redundant", "concave; sunken"), with no filler from other cards. The N1 selection screen shows 116 cards.
- **Links and offline:** the screens are consistent with links working in both directions and with system Back keeping the scroll position. Offline mode is shown honestly ("handwriting model not available"). The fact that each screen came from a particular navigation step rests on the route evidence and filenames, not the pixels.

**Carried forward from earlier reports:**
- **C1 (the word article says "JMdict also recognizes 凛", though JMdict lists 凛 first, with newspaper-frequency tags):** OPTIONAL. Shown at word-02, -07 and -09. I still disagree mildly with the wording; low impact on learners.
- **C2 (possible overlap with 涼しい):** WITHDRAWN.
- **C3 (quiz exposure):**
  - The default quiz is RESOLVED: confirmed both in the packet and on screen.
  - Larger, random, custom, padded or reverse quiz pools remain UNVERIFIED and are not claimed safe.

## Observations on app behaviour (optional, not article defects)
1. **Reading feedback:** after the on-reading question, the feedback line reads "dignified; bracing cold: リン、きびしい". It shows the source-only kun with no qualifier, unlike the article. This is low severity and app-level; at most, consider marking or omitting non-selected readings there. The meaning-quiz feedback shows the title only.
2. **Drawing wording:** "Practice only: this attempt is not graded" sits next to "Graded by stroke shapes only", which could read as contradictory. Wording only.
3. **Model download message:** the tracing screen showed "Downloading the handwriting model (first use only)…" while offline. Later screens say "not available". This was a transient status; there is no claim of a successful download.

My original optional suggestions remain optional: briefly explain the taru adjective (凜たる), add an attested 凜と + verb example, mention 凜々しい (りりしい), and simplify the "strict" sentence.

## Limits and how the earlier rendering uncertainty settled
- **Resolved:**
  - The 凜 glyph renders as 禾-bottomed at large size, with the two 冫 marks visible.
  - All 28 scoped Han render in Gothic, Mincho, Textbook and Brush across the three panels, with no blank areas or replacement boxes.
  - Typeface fallback to a Gothic-like face for 冫, 凛, 凜 and 稟 in Textbook and Brush is a typeface change only.
  - Article scroll states and table columns are complete when judged together, and the whole-word wraps (冷/静, 寒/い, the Textbook た) keep all the text.
- **Partially resolved:** 凛 versus 凜 at small and body-text sizes.
  - Panel 3 shows them as distinct with moderate confidence; panel 1 was too small to decide.
  - 凛 never appeared at large size, so its 示 bottom is confirmed only at small size, supported by the within-family raster-hash difference, which is not proof of readability.
  - Some stroke-number labels (13–15) were crowded, and fine strokes of 険 and 鷹 at panel size were unresolved.
- **Unresolved:** safety in larger or custom quiz pools (C3); real handwriting recognition (the strokes were injected from reference data, and the ML Kit model was unavailable); human handwriting.
- **Evidence I relied on but did not see in pixels:** the fixture, route, persisted-log and curation evidence. That includes the claim that two tests passed on run 587, the inherited host and compile results, the synthetic progress data, and the 1096/5053/116 content counts.
- **Not established, and separate from this review:**
  - Hardware: no physical phone or native-font check on a device; the test device was an API 35 emulator.
  - Release steps: latest-main merge, combined checks, signing, owner push, remote CI, public ZIP hashes, archive guards and owner issue 60.
  - Scope: general release and the whole N1 set.
  - Learning effectiveness: not measured.
  - My own checks: no independent Git, hash or upstream lookups.
- **Process:** no reads were denied or missing within the 26 resources I was assigned; I made no edits and reread nothing.
