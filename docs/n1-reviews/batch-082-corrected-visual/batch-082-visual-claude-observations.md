## Turn 1: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-corrected-visual\batch-082-visual-source-packet.txt

**Resource 1/29: corrected visual source packet.** I read `batch-082-corrected-visual\batch-082-visual-source-packet.txt` in full with one view call. There was no truncation notice and no denied access. I did not count lines myself, and I verified no hashes.

**The teaching change is confirmed again.** The diff changes only `准.md:13`, from `[集, 進, 難]` to `[冴, 冶, 隼]`, and updates the manifest (content version d82e7fefe3898a70 and the 准.md hash).

**The article text matches what I reviewed before.**
- The current 准.md is the same as the 9ce870d1 file I confirmed earlier.
- 准教授.md, the 教.md:39 bullet and the 助教授.md:16 paragraph and link read the same as the text I reviewed earlier.
- 冴, 冶 and 隼 have unchanged SHA256 values.

**Supplied execution evidence (not run by me):**
- **Test fixture:** `N1Batch082CorrectedNativeTest.kt` asserts:
  - a single full sync giving 1094 kanji, 5050 words, 114 N1 cards, version d82e7fef, 0 problems and parser epoch 1
  - 准's distractors are 冴, 冶 and 隼
  - ジュン is the only on-reading and there is no kun-reading
  - the meaning quiz shows exactly 4 options, mapped 准, 冴, 冶 and 隼 to the four expected titles, with no 倣, and each title is displayed
- **Instrumentation log:** OK (2 tests).
- **`execution.json`:** emulator-5580, API 35, read-only, no network, adb exit 0, both test cases status 0, helper and emulator stopped. It lists 53 capture PNGs.
- **Route record:** 4 options in the order 冴, 准, 隼, 冶; no fallback; 2 reciprocal pairs (4 link directions) and 1 comparison pair (2 directions); 10 injected drawing strokes; phone evidence false.
- **Font-raster record:** 140 rows.
  - 冫, 氵, 辶 and 隹 have the same hash in all four font families, so they come from a shared fallback.
  - 冴, 冶 and 隼 have hashes that differ by family.
  - Hashes don't identify the font face or show legibility.
- **Screen tree:** the tree captured at teardown again shows "Loading your cards…" and "All · 0 cards" with disabled buttons. As before, this looks like a transient state during cleanup, not a defect.

**Discrepancy:** the host says 51 captures, but `execution.json` lists 53 PNGs. I did not reconcile the difference. Anything that would come from the pixels, such as label truncation, has not been checked yet.

## Turn 2: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-curated-on-done.png

**Resource 2/29: `n1-082-corrected-curated-on-done.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back Kanji readings". The status-bar time is 3:45.
- **Session summary:** "Session complete" and "1 of 1 answers correct."
- **Buttons:** "Done" (filled) and "Practice more" (outlined).
- **Below the buttons:** the rest of the screen is blank, with no error text, blank boxes or replacement characters.

No kanji is visible. That this was the session for 准 with じゅん, and that a good grade was saved, rests on the supplied test assertions and route evidence, not on the pixels. I see no content defect.

## Turn 3: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-curated-On-feedback.png

**Resource 3/29: `n1-082-corrected-curated-On-feedback.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Kanji:** a large serif 准 with two separate 冫 marks on the left and no 十 below. It reads clearly as 准, not 準.
- **Feedback:** "Correct! — on'yomi".
- **Options:** ヤ, ジョウ, ケン and a highlighted ✓ジュン.
  - Only ジュン is a valid reading of 准, so the question has one correct answer.
  - The wrong readings have changed from the earlier run (カン/ジュウ/ジョウ). ヤ is 冶's on-reading, so the reading quiz may now draw on the new distractor cards. That doesn't make it ambiguous.
- **Summary line:** "quasi-; associate rank: ジュン", followed by the Next and I guessed buttons.
- **Article preview:**
  - The 准 heading, then "Strokes: 10 · Key (radical): 冫 (no. 15) · JLPT: N1 (community list)".
  - The Meaning paragraph matches lines 22–25 of the card, and 准教授 is shown as a link.
  - じゅんきょうじゅ wraps across a line, which is not a defect.

There are no blanks or replacement boxes. The small 冫 in the facts line can't be resolved into two marks at this size. I see no content defect.

## Turn 4: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-curated-On-question.png

**Resource 4/29: `n1-082-corrected-curated-On-question.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back Kanji readings".
- **Attempts note:** "Attempts left: 1", with the note that queued repeats are included.
- **Kanji:** a large 准 in a calligraphic serif style, different from the face in R3. That fits the varied-font setting. It shows two left-hand 冫 strokes and no 十 below, so it reads as 准, not 準.
- **Prompt:** "Pick the on'yomi".
- **Options:** ヤ, ジョウ, ケン and ジュン. These are the same four as in R3, and only ジュン is a valid reading of 准.
- **Below the options:** an "I don't know" link. The rest of the screen is empty.

There are no blanks, replacement boxes or cut-off labels. I see no content defect.

## Turn 5: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-drawing-feedback.png

**Resource 5/29: `n1-082-corrected-drawing-feedback.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back Drawing", then "准 quasi-; associate rank".
- **Grading status:** "Practice only: this attempt is not graded." and "Well drawn!".
- **Your drawing:** ten blue strokes form 准, with two left-hand 冫 strokes and the 隹 shape. These are reference strokes injected by the test, not human handwriting.
- **Correct strokes:** ten green strokes, numbered 1–10. Strokes 1–2 are the 冫 marks and strokes 3–10 build 隹. There is no lower 十.
- **Grading note:** "Graded by stroke shapes only (handwriting model not available)." Then a Next button.
- **Article preview:** the facts line (10 strokes, 冫 no. 15, N1 community list), the Meaning paragraph with 准教授 as a link, and the start of the approval paragraph with 批准 ひじゅん.

There are no blanks or replacement boxes. The bottom line is slightly clipped by the screen edge, which is just scrolling. The small 冫 in the facts line can't be resolved into two marks at this size. I see no content defect.

## Turn 6: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-drawing-recall-feedback.png

**Resource 6/29: `n1-082-corrected-drawing-recall-feedback.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back Drawing", then "准 quasi-; associate rank".
- **Prompt:** "Here is the kanji", shown in red.
- **Drawing panels:** "Your drawing" is empty, which fits giving up on recall. "Correct strokes" shows the same ten numbered green strokes as R5: two 冫 marks plus 隹, with no lower 十.
- **Below the panels:** a Next button.
- **Article preview:** the facts line, the full Meaning paragraph with 准教授 as a link, the complete approval paragraph with 批准 ひじゅん, and the start of the mnemonic ("Modern-shape mnemonic, not etymology: picture…"). The last line is cut off at the bottom edge by scrolling.

The screenshot doesn't show the earlier recall prompt, so I can't tell from it whether 准 was hidden then. That the grade was saved when Next was tapped rests on the supplied test assertion. There are no blanks or replacement boxes, and I see no content defect.

## Turn 7: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-drawing-trace.png

**R7: drawing-trace (`n1-082-corrected-drawing-trace.png`).** The frame I received was about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

- **Screen text:** the "Drawing" screen shows "Attempts left: 1" and the queued-repeats note. The prompt reads "Trace the kanji for", with the label **"quasi-; associate rank"** in full and not truncated. Below it is "Ungraded tracing practice. You'll try from memory later."
- **Tracing guide:** the guide is 准 with ten numbered strokes.
  - Strokes 1–2 form the 冫, two separate marks.
  - Strokes 3–10 form 隹, with four horizontal strokes and no lower 十.
  - Nothing looks like 氵 (three marks) or 準.
  - I did not check how plausible the stroke order is beyond the numbering.
- **Status line:** the screen shows "Downloading the handwriting model (first use only)…". This repeats the offline status UX point from my earlier review. It is not a content defect, and the drawing-feedback screen (R5) later shows "handwriting model not available".
- **Buttons:** Undo, Clear and Check are disabled, and no user strokes are drawn yet.

Emulator pixels only, no phone evidence.

## Turn 8: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-font-panel-1.png

**R8: font panel 1 of 3 (`n1-082-corrected-font-panel-1.png`).** I received the frame at about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

- **Contents:** the heading reads "Batch 082 corrected: associate rank / look-alikes / radical fallback, Panel 1 / 3". There are four labelled rows: Gothic, Mincho, Textbook and Brush.
- **Characters:** each row shows the same 24 Han: 中事備先典冫冴冶准助十基大女学彼手批授教木氵準生. All of them render, with no blank or replacement boxes. 隼, 進, 集, 難 and 辶/隹 are not in this panel's rows; they appear only in the footer note.
- **Shapes that can be told apart at this size:**
  - 冴 has 牙 on the right and 冶 has 台 on the right, in all four rows.
  - 准 has 冫 with 隹 and no lower 十.
  - 準 has 氵 and a lower 十.
  - Standalone 冫 shows two marks and 氵 shows three.
  - None of the lookalike pairs collapses into the same shape.
- **Typefaces:**
  - Gothic is heavier and Brush is bold and calligraphic.
  - Textbook has wider spacing and wraps differently, putting 学 on the second line. This is a layout difference, not a defect.
  - Mincho looks lighter but not clearly serif at this size. It may share its fallback with another family, and the panel itself warns "Fallback families may coincide."
  - The pixels don't identify which face is used.
- **Unreadable detail:** fine stroke detail, such as stroke endings and the exact 冫 tick angles, is not resolvable at the size I received.

These are emulator pixels only, not a phone.

## Turn 9: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-font-panel-2.png

**R9: font panel 2 of 3 (`n1-082-corrected-font-panel-2.png`).** The frame arrived at roughly 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

- **Contents:** each of the Gothic, Mincho, Textbook and Brush rows shows the same 10 Han: 田義聞講辶進隹隼集難.
  - Together with panel 1's 24 characters, that makes 34 distinct scoped Han, matching the "34 scoped Han" note in the footer.
  - Everything renders, with no blank or replacement boxes.
- **Lookalikes:**
  - 隼 shows 隹 above a small 十 and no water radical, so it differs from 准 (冫 beside 隹) and 準 (氵, 隹 and 十).
  - 集 has 隹 above 木, 進 has 辶 wrapping 隹, and 難 has 隹 on the right.
  - None of these collapse into one shape.
- **Fallback behaviour:**
  - In the Mincho, Textbook and Brush rows, the standalone 辶 and 隹 look the same as in Gothic: heavier, with no change of face.
  - This is consistent with the shared cross-family hash in the supplied raster evidence, which suggests a fallback face.
  - The glyphs still render correctly, and a typeface change alone is not a defect.
  - The pixels don't identify which face is used.
- **Unreadable detail:** at this size I can't resolve fine stroke detail, such as the length of 十 in 隼 or the internal strokes of 難.

These are emulator pixels only, not a phone.

## Turn 10: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-font-panel-3.png

**R10: font panel 3 of 3 (`n1-082-corrected-font-panel-3.png`).** The frame I received is about 900×2000 and likely downscaled; I did not verify full-resolution bytes or the hash.

- **Contents:** each of the Gothic, Mincho, Textbook and Brush rows shows the focused set 准冴冶隼準 and 冫氵辶隹, then the whole word **准教授**. Every glyph renders, with no blank or replacement boxes.
- **Lookalikes, side by side in each row:**
  - 准 has 冫 + 隹 and no 十.
  - 冴 has 冫 + 牙 and 冶 has 冫 + 台.
  - 隼 has 隹 over 十.
  - 準 has 氵 + 隹 over 十.
  - Standalone 冫 shows two marks and 氵 shows three.
  - None of these collapse into the same shape.
- **Whole word:** 准教授 reads correctly in every family. In the Textbook row it is set tighter and smaller than the spaced single characters, which is a layout difference only.
- **Fallback:** in the Mincho, Textbook and Brush rows, 冫, 氵, 辶 and 隹 look like the Gothic or other heavier forms. That fits the hash shared across families, which suggests a fallback face, but the glyphs are still correct. A change of typeface alone is not a defect, and the pixels don't identify the face.
- **Unreadable detail:** at this size I can't resolve the angles of the 冫 tick strokes or other fine stroke detail.

With panels 1 and 2, all 34 scoped Han have now been seen in all four families. These are emulator pixels only, not a phone.

## Turn 11: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-former-forward-30.png

**R11: former-forward-30 (`n1-082-corrected-former-forward-30.png`).** The frame I received was about 900×2000, likely downscaled; I did not verify full-resolution bytes or the hash. It shows the 准教授 article ("associate professor"), scrolled to "Synonyms and antonyms" and "Distinctive meaning".

- **助教授 entry:** 助教授 じょきょうじゅ is a link. The bullet reads "former Japanese title replaced by 准教授 in April 2007… older documents". This is the forward direction of the comparison.
- **Other synonym entries:**
  - 助教 じょきょう is described as a separate rank, not an abbreviation; it is not linked.
  - 助手 is linked and described as "assistant… does not by itself identify".
  - 教授 and 先生 are linked; 先生 is described as broader or a form of address.
  - The section closes with "role and title comparisons, not strict antonyms".
- **Distinctive meaning:**
  - 准教授 is a rank noun, not a verb, and 准教授です (じゅんきょうじゅです) is the way to state the role.
  - 教授する (instruction) is said not to license 准教授する.
  - The section adds that there is no exact international equivalence and no automatic promotion. It notes that JMdict lists 準教授 and that 准教授 is the current title.
- **Mismatches:** none against the source as I reviewed it earlier.
- **Layout and legibility:** the reading wraps mid-word as じゅ/んきょうじゅです, a layout point and not a defect. All the text is legible.

These are emulator pixels only, not a phone.

## Turn 12: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-kanji-01.png

**R12: kanji-01 (`n1-082-corrected-kanji-01.png`).** The frame I received is about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

- **Header:** "准 quasi-; associate rank", shown in full with no truncation, then "Strokes: 10 · Key (radical): 冫 (no. 15) · JLPT: N1 (community list)".
- **Meaning and origin:**
  - Covers the status/rank sense and links 准教授 じゅんきょうじゅ (associate professor).
  - Rules out "half-professor" and "trainee awaiting automatic promotion".
  - Covers the approval branch: 批准 ひじゅん, ratification, and says not every compound containing 准 is a rank.
  - Gives a qualified mnemonic, "Modern-shape mnemonic, not etymology", built on 隹 beside the two marks of 冫, described as an invented memory scene.
- **Readings:** "Scroll sideways to read all columns." is shown as a signpost. The row reads ジュン | on | 准教授 じゅんきょうじゅ – associate professor (linked).
  - The Typical words column is clipped at the right edge, with the reading cut as "じゅんき…". This is the signposted horizontal scroll, not a defect.
  - No kun row appears in this view.
- **Not checked:** I couldn't resolve the two separate marks of the inline 冫 glyphs at this size; this repeats my earlier note.
- **Source match:** no mismatches against the source I reviewed.

These are emulator pixels only, not a phone.

## Turn 13: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-kanji-03.png

**R13: kanji-03 (`n1-082-corrected-kanji-03.png`).** I received a frame of about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

- **Position:** the 准 article is scrolled to "Meaning and origin". The rank and approval (批准 ひじゅん) branches and the qualified mnemonic read the same as in R12.
- **Readings table:** a single on-reading row, ジュン, links 准教授. The "Typical words" column is clipped at the right edge, which is the signposted sideways scroll.
- **New text below the table:** "sole on-reading in the frozen KANJIDIC2 record; that record lists no kun-readings. Readings supplied by other dictionaries do not change this card's source metadata."
  - This matches the empty-kun source scope without denying other dictionaries' readings.
- **Bottom edge:** the "Common words" heading is cut off at the bottom; the next capture presumably continues from there.
- **Not resolvable:** the inline 冫 is too small to make out as two marks, as before.
- **Mismatches:** none against the source I reviewed.

These are emulator pixels only, not a phone.

## Turn 14: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-kanji-10.png

**R14: kanji-10 (`n1-082-corrected-kanji-10.png`).** The frame I received was about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

- **Readings:** the ジュン/on row and the note "no kun-readings… other dictionaries do not change this card's source metadata" are the same as in R13.
- **Common words:**
  - 准教授 じゅんきょうじゅ — associate professor (linked)
  - 批准 ひじゅん — ratification
- **Notes:**
  - 準 (linked) shares ジュン and has related meanings, but its shape has 氵 at the upper left and 十 below; 准 has two left-hand 冫 marks and no lower 十. At this size the inline 氵 looks like three marks and 冫 like two, but the exact strokes are only marginally resolvable.
  - The spellings are said not to be freely interchangeable: 準備, 基準 and 批准 are to be learned as written. The note also says JMdict recognizes 準教授, while 准教授 is the current title taught.
  - The lookalike bullet compares 集 (木 below 隹), 進 (辶) and 難 (dense left block). Its last line is cut off at the bottom of the frame.
  - These Notes comparisons stay the same, as the corrected source intended; only the quiz distractors changed.
- **Mismatches:** none found against the source I reviewed.

Emulator pixels only, not a phone.

## Turn 15: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-kanji-12.png

**R15: kanji-12 (`n1-082-corrected-kanji-12.png`).** The frame I received is about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

This is the same scroll position as R14, but the Readings table is shifted sideways:
- The left columns are clipped ("ading", "ュン").
- The Typical words cell is now fully visible: 准教授 (linked) じゅんきょうじゅ – associate professor. Nothing else appears to the right.

Taken together with R14, the signposted table reads in full. The rest matches R14:
- the source note saying there are no kun-readings and that other dictionaries' readings don't change the card
- Common words 准教授 and 批准
- the 準 shape and spelling notes, including the recognized alternative spelling 準教授
- the 集/進/難 lookalike line, cut off at the bottom of the frame

I found no mismatches against the source I reviewed. Fine detail of the inline 氵 and 冫 is only marginally resolvable at this size. Emulator pixels only, not a phone.

## Turn 16: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-kanji-15.png

**R16: kanji-15 (`n1-082-corrected-kanji-15.png`).** The frame I received was about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

This capture shows the end of the 准 article:
- **Readings note:** the source note on readings: no kun-readings, and other dictionaries' readings don't change the card.
- **Common words:** 准教授 (linked) and 批准 ひじゅん, ratification.
- **Notes on 準:** 準 differs in shape (氵 and 十). The spellings are not freely interchangeable: 準備, 基準 and 批准 are kept as written, and 準教授 is noted as the JMdict spelling while 准教授 is the current title.
- **Lookalike bullet:** now complete: 集 (木 below 隹), 進 (辶) and 難 (dense left block), ending "Their meanings are not associate rank or approval."
- **Metadata:** KANJIDIC2 (database 2026-306, 2026-11-02, EDRDG; CC BY-SA 4.0); JMdict entries 2178020, 1483390, 1341670 and 1591210; Digital Daijisen: 准; Nipponica and 大学事典: 准教授. The links are visible but were not followed.

The Notes still compare 集, 進 and 難 rather than the quiz distractors 冴, 冶 and 隼. That matches the source change, which touched only the distractors line. I found no mismatches against the source I reviewed.

The inline 冫 and 氵 are only marginally resolvable at this size. These are emulator pixels only, not a phone.

## Turn 17: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-kanji-18.png

**R17 (kanji-18).** I received a frame of about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

- **Content:** visually the same as R16. It shows the end of the 准 article: the readings note, the 准教授 and 批准 Common words, the 準 shape and spelling notes, the complete 集/進/難 lookalike bullet, and the full metadata line.
- **Only differences from R16:** the clock reads 3:45 instead of 3:44. Nothing in the content area visibly differs, so this looks like a repeated end-of-article state.
- **Source check:** I found no mismatches with the source I reviewed.
- **Limits:** the inline 冫 and 氵 are only marginally resolvable at this size. These are emulator pixels only, not a phone.

## Turn 18: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-kanji-backlink.png

**R18: kanji-backlink (`n1-082-corrected-kanji-backlink.png`).** The frame I received is about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

- **What it shows:** the 准 "quasi-; associate rank" article at 3:45. The content matches R14:
  - the Readings table (ジュン, on, linked 准教授; signposted right edge clipped)
  - the note that the source lists no kun-readings
  - the Common words 准教授 and 批准
  - the 準 shape and spelling notes
  - the 集/進/難 lookalike line, cut off at the bottom
- **Navigation not shown:** the pixels show only where the screen ended up. They do not show the navigation path, such as following the 准 link from the 准教授 article, so the backlink direction rests on the supplied route and assertions, not on this still.
- **Source match:** I found no mismatches against the source I reviewed.
- **Limits:**
  - The inline 冫 and 氵 are only marginally resolvable.
  - These are emulator pixels only, not a phone.

## Turn 19: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-meaning-feedback.png

**R19: meaning-feedback (`n1-082-corrected-meaning-feedback.png`).** I received the frame at about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

This is the main runtime check for the corrected distractors.

- **Prompt and result:** the Quiz screen shows a large 准 drawn with two 冫 marks next to 隹 and no lower 十, followed by "Correct!".
- **Answer options:** there are exactly four, in this order:
  - "clear; sharp-minded"
  - "✓ quasi-; associate rank" (highlighted green)
  - "falcon"
  - "smelt; work metals"
- **Labels:** every label is complete and untruncated, with no "imitate; emulate" and no 倣 or other fallback label.
  - This order matches the supplied route order 冴, 准, 隼, 冶.
  - The pixels show the labels only. That they belong to 冴/冶/隼 rests on the supplied assertions and route data.
  - I found no competing meaning among these labels within the existing source scope.
- **Rest of the screen:** below the options are the summary line "quasi-; associate rank" and the Next and "I guessed" buttons. The article preview below them shows the header line (10 strokes, key 冫 no. 15, N1 community list) and the start of "Meaning and origin", which match the source.

These are emulator pixels from a single session only, not a phone.

## Turn 20: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-meaning-question.png

**R20: meaning-question (`n1-082-corrected-meaning-question.png`).** The frame I received is about 900×2000, likely downscaled; I didn't verify full-resolution bytes or the hash.

- **Prompt:** the quiz shows "Attempts left: 1" and the queued-repeats note, then a large serif 准 with two 冫 marks and 隹 and no lower 十. The question is "What does it mean?".
- **Options:** exactly four, all complete:
  - "clear; sharp-minded"
  - "quasi-; associate rank"
  - "falcon"
  - "smelt; work metals"
- **Order and fallback:** the order matches R19 and the supplied route (冴, 准, 隼, 冶). There is no "imitate; emulate", no 倣 label, and no other fallback label. Nothing is pre-selected, and an "I don't know" link is shown.
- **Answer clarity:** only one label fits 准 within the existing source scope.
- **Limits:** the mapping from labels to kanji rests on the supplied assertions, not on the pixels alone. These are emulator pixels only, not a phone.

## Turn 21: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-selection.png

**R21: selection (`n1-082-corrected-selection.png`).** I received the frame at about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

- **Stack and scope:** the Kanji screen shows "N1 · 114 cards" with the N1 chip selected, and the note "Only cards tagged N1. Each stack keeps its own review schedule."
  - The chips are N5, N4, N3, N2, N1, All and a cut-off "Sta…". The chip row is clipped at the right edge, which looks like normal horizontal scrolling.
- **Due counts:**
  - Meaning quiz: 1 due, 0 new
  - Drawing: 0 due, 1 new
  - Readings (on'yomi and kun'yomi): 1 due, 0 new
  - Each has a Start button, and there is a "Browse all kanji" button.
- **Source of the counts:** the 114-card total matches the supplied sync assertion. The due and new counts reflect the fixture's synthetic seeding, not real progress, and the pixels alone don't show which cards are due.
- **Content kanji:** none are visible on this screen.

These are emulator pixels only, not from a phone.

## Turn 22: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-successor-reverse-31.png

**R22: successor-reverse-31 (`n1-082-corrected-successor-reverse-31.png`).** I received a frame of about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

- **What it shows:** the reused 助教授 article, titled "associate professor (former Japanese title)", scrolled to Meaning.
- **Changed passage:** the paragraph reads "The Japanese rank was renamed **准教授** (じゅんきょうじゅ), associate professor, in April 2007". 准教授 is a link, so this is the first successor-name link, matching the source change at `助教授.md:16`.
- **Later mention:** further down, under "Synonyms and antonyms", the text "准教授 is the successor Japanese title" is not linked. That matches the scope, which links only the first mention.
- **Unchanged content I could see:**
  - the two historical examples, 当時 and 古い資料, with their readings and translations
  - the note on how the kanji combine (助/教/授), including "not just any helper"
  - 助教 described as a separate rank, cut off at the bottom of the frame
- **Navigation:** the "reverse" direction rests on the supplied route data; the pixels only show the article state and the visible link.

I found no mismatches against the source I reviewed. These are emulator pixels only, not a phone.

## Turn 23: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-system-back-to-teach.png

**R23: system-back-to-teach (`n1-082-corrected-system-back-to-teach.png`).** I received the frame at about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

- **What it shows:** the reused 教 article, "teach, instruct", scrolled to the readings table and Common words. The table's right column is clipped, which is the signposted sideways scroll.
- **Changed bullet:** the last Common words bullet reads "**准教授** (linked) じゅんきょうじゅ — associate professor", which matches the source change at `教.md:39`.
  - The other bullets (教える, 教わる, 教室, 教科書, 儒教), the Notes and the metadata are unchanged material.
- **System Back:** the pixels show only the end state. That System Back led here rests on the supplied route assertions, not on this still.

No mismatches against the source I reviewed. These are emulator pixels only, not a phone.

## Turn 24: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-system-back-to-word-from-teach.png

**R24: system-back-to-word-from-teach (`n1-082-corrected-system-back-to-word-from-teach.png`).** The frame I received is about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

**What the frame shows:** the 准教授 "associate professor" article, scrolled to "How the kanji combine".
- 准 (linked) modifies the rank head 教授 (linked).
- Within 教授, 教 (linked) contributes teaching and 授 contributes imparting knowledge.
- The on-readings are given as ジュン + キョウ + ジュ, with the warning not to translate the title as "half a professor".

**Below that:**
- The Synonyms section matches R11: the 助教授 April-2007 link, 助教 as a separate rank, 助手 and 教授/先生.
- The Distinctive meaning section begins with the rank noun, not a verb, and 准教授です. The じゅ/んきょうじゅです wrap repeats here.

**Earlier optional point:** standalone 授 is still plain text, not a link.

**Navigation:** the pixels show only where the screen ended up. That System Back from 教 returned here rests on the supplied route assertions, not on this still.

I found no mismatches against the source I reviewed. These are emulator pixels only, not a phone.

## Turn 25: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-system-back-to-word.png

**R25: system-back-to-word (`n1-082-corrected-system-back-to-word.png`).** The frame I received is about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

- **Content:** visually identical to R24. It shows the 准教授 article at "How the kanji combine": 准 modifies the head 教授, 教 means teaching, 授 means imparting, the reading is ジュン+キョウ+ジュ, and the "not half a professor" warning.
- **Further down:** the Synonyms section (助教授 with April 2007, 助教 as a separate rank, 助手, 教授 and 先生) and the start of "Distinctive meaning". 授 is still unlinked, and the じゅ/ん wrap repeats.
- **Navigation:** the pixels don't show which page System Back came from. That depends on the supplied route assertions.

I found no mismatches against the source I reviewed. These are emulator pixels only, not a phone.

## Turn 26: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-word-02.png

**R26: word-02 (`n1-082-corrected-word-02.png`).** The frame I received was about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

**What it shows:** the 准教授 "associate professor" article, scrolled to "Meaning".
- **Meaning section:** an established academic rank below 教授 きょうじゅ (professor, linked), with teaching and research responsibilities, and explicitly not a professor's personal helper.
- **Example 1:** 彼女は大学の准教授です。 (かのじょはだいがくのじゅんきょうじゅです。) "She is an associate professor at a university." The kana, particles and English are correct and natural.
- **Example 2:** 田中准教授の講義を聞きました。 (たなかじゅんきょうじゅのこうぎをききました。) "I listened to Associate Professor Tanaka's lecture." Correct and natural, with past tense and the を object.
- **Note on 先生:** 田中先生 (たなかせんせい) is used for direct address, and 先生 (linked) is not itself a statement of this academic rank.
- **Below that:** "How the kanji combine", same as R24, and the start of the 助教授 April-2007 synonym bullet, cut off at the bottom of the frame.

I found no mismatches against the source I reviewed. These are emulator pixels only, not a phone.

## Turn 27: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-word-09.png

**R27: word-09 (`n1-082-corrected-word-09.png`).** The frame I received is about 900×2000, likely downscaled. I did not verify full-resolution bytes or the hash.

This is the 准教授 article at "Synonyms and antonyms" and "Distinctive meaning". It looks identical to R11.
- **Synonyms and antonyms:**
  - 助教授 is linked and described as replaced in April 2007 and relevant for older documents.
  - 助教 is a separate rank and not an abbreviation; it is not linked.
  - 助手 is linked and noted as not identifying someone by itself.
  - 教授 and 先生 are linked.
  - The section says these are not strict antonyms.
- **Distinctive meaning:**
  - 准教授 is a rank noun. Use 准教授です; 教授する does not license 准教授する.
  - It warns against assuming international equivalence or automatic promotion.
  - It notes that JMdict lists 準教授 and that 准教授 is the current title.

The じゅ/ん line break repeats here. The text is legible, and I found no mismatches against the source I reviewed. These are emulator pixels only, not a phone.

## Turn 28: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-word-15.png

**R28: word-15 (`n1-082-corrected-word-15.png`).** I received the frame at about 900×2000, likely downscaled, and did not verify full-resolution bytes or the hash.

This capture shows the end of the 准教授 article:
- The remaining Synonyms bullets: 助教, 助手 (linked), 教授 and 先生 (linked).
- The note "not strict antonyms".
- The full Distinctive meaning section: rank noun, 准教授です, no 准教授する, no international equivalence or automatic promotion, and the JMdict spelling 準教授 alongside the current title 准教授.
- The source line: JMdict entry 2178020; comparisons 1237160, 1344540, 1344550, 1344650 and 1387990; and "Japanese rank and April 2007 reform: Nipponica and 大学事典: 准教授". The links are visible but I did not follow them.

The top line is partly scrolled off. The じゅ/ん line break repeats here, as before. I found no mismatches against the source I reviewed. These are emulator pixels only, not a phone.

## Turn 29: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native-corrected\attempt-565\n1-082-corrected-word-forward-13.png

**R29: word-forward-13 (`n1-082-corrected-word-forward-13.png`).** The frame I received is about 900×2000, likely downscaled. I didn't verify full-resolution bytes or the hash.

- **Content:** this frame looks identical to R16 and R17. It shows the end of the 准 article:
  - the readings note (no kun-readings in the source; other dictionaries don't change this card)
  - the Common words section, with 准教授 linked
  - the 準 shape and spelling notes, including the alias 準教授
  - the full 集/進/難 lookalike bullet
  - the metadata line
- **Navigation:** only the 准教授 link is visible here. The pixels don't show the forward navigation itself, so whether that link actually opens the 准教授 page rests on the supplied route assertions.
- **Source check:** no mismatches against the source I reviewed.
- **Limits:** the inline 冫 and 氵 are only marginally resolvable at this size. These are emulator pixels only, not a phone.

## Turn 30: FINAL REPORT

# SAME082 corrected-runtime visual confirmation: final report

All four scoped items are CLEAN on every facet, there are no findings, and 082-V1 is resolved for the default four-choice N1 meaning quiz on emulator evidence.

## Snapshot

- **Evidence HEAD:** 86c77107638e0adf2aa2752c50533124c389b371.
- **Corrected teaching snapshot:** 9ce870d190d5c519d65ed20b118de64371350c0c.
- **Native archive:** e108bbeb, content version d82e7fefe3898a70.
- **Builds:** test-only Android 1c1b7bf4, which preserves production f9b59a2. It is not the latest app main.
- **Native execution:** attempt 565.
- **Earlier artifacts:** the old 559/560/561 runs are historical and not used here as corrected acceptance.

## Scope

- **Model:** Claude Opus 5.5 (claude-opus-5.5).
- **What I read:** 29 resources, one `view` call each, with no rereads, shell, edits, delegation or parallel calls:
  - R1 was the complete source packet `batch-082-visual-source-packet.txt`, read with forceReadLargeFiles and no view range.
  - R2–R29 were 28 original PNGs from `batch-082-native-corrected\attempt-565\`. These are the host's byte-group representatives for 51 captures; I did not see the other 23 captures directly.
- **Image size:** every frame arrived at about 900×2000, which may be downscaled. I can't claim full-resolution bytes and did not verify any hashes.
- **Compressed history:** my notes on R1–R6 come from summarized session history, not my original wording. Those notes say R1's `execution.json` lists 53 PNGs while the host states 51 captures, and I did not reconcile the two.
- **Items assessed:**
  - new `kanji\准.md`
  - new `words\准教授.md`
  - the 准教授 Common words bullet in `kanji\教.md:39`
  - the successor paragraph and link in `words\助教授.md:16`
- **Context only:** the 冴, 冶, 隼 and 教 cards were supplied as background, not given a new whole-card review.
- **Inherited conclusions:**
  - My earlier textual review and visual pass.
  - My choice-reconciliation report and changed-metadata confirmation.
  - The source-level 082-V1 correction verdict.
  - The prior all-40 font evidence.

## Verdicts

Each facet below is CLEAN. That means no actionable defect was established within scope; it is not exhaustive certification.

| Item | Correctness | Scoped coverage | Bounded visual comprehensibility |
|---|---|---|---|
| New 准.md | CLEAN | CLEAN | CLEAN |
| New 准教授.md | CLEAN | CLEAN | CLEAN |
| 教.md:39 bullet | CLEAN | CLEAN | CLEAN |
| 助教授.md:16 successor paragraph and link | CLEAN | CLEAN | CLEAN |

### What the pixels showed

**准.md:**
- Header: "quasi-; associate rank", 10 strokes, key radical 冫 (no. 15), N1 (community list).
- Rank and approval senses: the rank sense, plus 批准 ひじゅん for the approval sense. The text warns it is not a "half-professor" or "trainee".
- Mnemonic: qualified as a modern-shape aid, not etymology.
- Readings: a single on-reading ジュン linked to 准教授. The note says the source record has no kun-readings without denying other dictionaries' readings.
  - The sideways-scrolling table is signposted; R14 showed it unscrolled and R15 shifted, and together they cover all columns.
- Common words: 准教授 and 批准.
- 準 shape and spelling: 準 has 氵 and a lower 十, while 准 has 冫 and no 十. The spellings are not freely interchangeable, and 準教授 is noted as recognized with 准教授 as the current title.
- The 集/進/難 lookalike note is unchanged and complete, and the metadata and source links appear.
- Runtime flows:
  - The on-reading quiz showed a single valid answer.
  - Tracing and recall drawing ran with ten reference strokes, graded by shape only, and the screen said "handwriting model not available".
  - The N1 selection screen showed 114 cards.

**准教授.md:**
- Meaning: a rank below 教授 with teaching and research duties, and not a personal helper.
- Two original examples (彼女は大学の准教授です。 and 田中准教授の講義を聞きました。) have correct kana, particles and English, and read naturally.
- The note on 田中先生 versus 先生 as a rank is present.
- How the kanji combine: 准 modifies the head 教授; 教 contributes teaching and 授 contributes imparting; the readings are ジュン+キョウ+ジュ.
- Comparisons:
  - 助教授 is the former title, replaced in April 2007.
  - 助教 is a separate rank and 助手 does not identify the role.
  - 教授 and 先生 are explained separately.
  - None of these is presented as an antonym.
- Usage: a noun, not 准教授する; no international equivalence or automatic promotion is implied; the JMdict spelling 準教授 is mentioned; sources are listed.

**教.md:39:** the bullet reads exactly "[准教授] じゅんきょうじゅ – associate professor", with the link.

**助教授.md:16:** the paragraph says the rank was "renamed [准教授] (じゅんきょうじゅ)… in April 2007". This is the first linked mention; the later Synonyms mention is unlinked, as scoped.

**Fonts (R8–R10):**
- All 34 scoped Han rendered in the Gothic, Mincho, Textbook and Brush families, as did the whole word 准教授.
- No blank or replacement boxes appeared.
- No lookalikes collapsed into each other:
  - 冴 has 牙 on the right and 冶 has 台.
  - 隼 has 隹 over 十.
  - 准 has 冫 and no 十, while 準 has 氵 and 十.
  - Standalone 冫 shows two marks and 氵 shows three.
- 辶, 隹, 冫 and 氵 look the same across families. That fits a fallback face, which is a typeface change, not a defect.

**Navigation:** the pixels show only end states. That 准↔准教授 and 教↔准教授 (four directions), 助教授↔准教授 (two directions) and System Back all work rests on the supplied route and assertions.

## Findings

None.

## 082-V1 runtime reconciliation

**Resolved** for the default four-choice N1 meaning quiz on this emulator evidence.

- **Pixels (R19 question, R20 feedback):** exactly four untruncated labels: "clear; sharp-minded", "quasi-; associate rank", "falcon" and "smelt; work metals". There is no "imitate; emulate", no 倣 and no tag-based fallback, and only one label fits 准 within the existing source scope.
- **Supplied evidence:** the mapping of those labels to 冴/准/隼/冶 and the route order rest on the supplied native assertions and route data.
- **Not shown in pixels:** the All-stack quiz was not captured, so it rests on the supplied, content-level evidence only.
- **Still open:**
  - The rare imitation sense of 准える (なぞらえる) remains recognized. Its rarity is not disproof, and ordinary frequency or learner impact is not established.
  - Custom, partial, larger or future pools remain uncertified, including the earlier hypothesis about 準 in a larger pool.
  - The new distractors also feed the on-reading quiz (ヤ appeared there); that quiz was not ambiguous.

## Optional (carried forward, not findings)

- The 准 readings row could add 批准, and the card could add 准看護師 or 准尉 as rank examples.
- Standalone 授 in 准教授's "How the kanji combine" is not linked.
- App UX:
  - The trace screen shows "Downloading the handwriting model…" while offline.
  - A loading state appeared in the teardown screen tree.
- The reading じゅんきょうじゅです wraps mid-word; this is layout only.
- The 准 Notes compare 集/進/難, not the quiz distractors 冴/冶/隼. This is consistent with the scoped diff; a lookalike note for 冴/冶 is optional.
- The earlier withdrawn claim about 準's curated distractors stays unverified.

## Limits

- **Pixels versus supplied evidence:** these items were supplied as execution evidence and not observed in the stills:
  - the sync counts: 1094 kanji, 5050 words and 114 N1 cards; version d82e7fef; zero problems; parser epoch 1
  - the single archive request
  - both test cases ending with status 0 and no skips
  - the API 35 read-only emulator-5580, with the helper stopped
  - Full and Lite modes, the quiz key and the persisted good-answer logs
  - the injected drawing strokes and the grade saved on Next
  - System Back and offline behaviour
  - the synthetic seeding, with no owner progress
- **Inherited without rerun:** the 563 host run (3+1+5, no skips) and the 564 compile.
- **No independent verification:** I did not check Git, upstream or hashes, and did no fresh dictionary lookup.
- **Fonts:**
  - Cmap absence is not glyph failure.
  - Pixels, Paint.hasGlyph and raster hashes do not identify the fallback face.
  - The 136 individual and 4 whole-word Paint assertions are not 140 PNG reads.
  - Inline 冫 and 氵 marks and fine stroke detail were only marginally resolvable at the size received.
- **Drawing:** the strokes were injected by the test. This is not human handwriting, successful recall, ML Kit recognition or a model download.
- **Not established:** physical-phone rendering, native-speaker certification and learning effectiveness.
- **Still outstanding:** final combined-main integration, publication, CI, an immutable ZIP, phone and general release, and whole-set acceptance.
- **Preserved limits:** the original OOM, denial, source, citation, lookup, read-depth and process limits are unchanged.
