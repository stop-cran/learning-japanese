## Turn 1: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-visual-source-packet.txt

**Resource 1 of 29: `batch-082-visual-source-packet.txt`.** I read it with one full `view` call, which gave no truncation notice. I am Claude Opus 5.5.

- **Sources:** All four articles show the same SHA256 as in my original review. The text matches lines 1–65 of 准.md, 1–62 of 准教授.md, 教.md:39 and 助教授.md:16. The text strings the test looks for match the article prose.
- **Run results:** These come from the supplied execution files; I did not run anything. The run used read-only emulator-5580 on API 35, with no network. Both tests reported status 0 ("OK (2 tests)") and adb exited with 0. The route log records:
  - 1,094 kanji, 5,050 words and 114 N1 cards imported, with zero problems;
  - content version 0739a82c9699f031 and reading-parser epoch 1;
  - on'yomi ジュン, kun'yomi empty, and quiz key じゅん;
  - two linked pairs (four directions) plus one comparison pair (two directions);
  - ten touch strokes injected from the reference data.

  The phone-evidence flag is false.
- **Font raster file:** It has 128 rows (124 single characters and 4 whole-word rows). For 冫, 氵, 辶 and 隹, the hashes are identical in all four font families, which suggests they come from one shared fallback font. The packet itself says fallback families may coincide, so this is not a glyph failure. Hashes cannot show readability; that depends on the PNGs.
- **End-of-test screen tree:** It shows the Kanji screen still loading, with "All · 0 cards" and disabled buttons. That conflicts with the passing run's earlier N1 checks. It was captured during the `finally` cleanup, so it may be a temporary reload. I am noting it, not counting it as a defect.
- **Screenshot list:** It names 51 PNGs, which matches the 51 captures expected.

I have not looked at any images yet.

## Turn 2: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-curated-on-done.png

**Resource 2 of 29: `n1-082-curated-on-done.png`.** I read it with one `view` call. The image I received appears downscaled to about 900×2000, from what is likely a 1080×2400 frame; I did not verify the original bytes.

- **What the pixels show:** The "Kanji readings" screen with a "← Back" link, the heading "Session complete" and the line "1 of 1 answers correct." Below that are a filled "Done" button and an outlined "Practice more" button. The status bar shows 2:44, and the signal icon has an exclamation mark, which fits being offline. All text is clear, with no blank areas or replacement boxes.
- **What it confirms:** The finished state of a one-question reading session, all correct. That matches the supplied counts of one answered and one correct.
- **What it cannot confirm:** The screen shows no kanji, reading key or question type. That the single question was the 准 on'yomi with key じゅん, and that a correct answer was saved to the log, rests only on the supplied test assertions and route log.

## Turn 3: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-curated-On-feedback.png

**Resource 3 of 29: `n1-082-curated-On-feedback.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Quiz screen:** It shows "Kanji readings" with a large serif 准. The two left-hand 冫 strokes (a dot and an upward-flicking stroke) are clearly separate, 隹 sits on the right, and there is no 十 below.
- **Feedback:** It reads "Correct! — on'yomi". The choices are カン, ジュウ, ジョウ and a green "✓ ジュン". Only one choice is ジュン. None of the other three appears in the frozen record for 准, so I see no second defensible answer here.
- **Summary line and buttons:** "quasi-; associate rank: ジュン" appears, followed by "Next" and "I guessed".
- **Article preview below the quiz:**
  - The heading and facts line match the source: Strokes 10, Key 冫 (no. 15), JLPT N1 (community list).
  - 准教授 appears as a link.
  - The opening of "Meaning and origin" is shown, with no blank areas or replacement boxes.
- **Limits:**
  - The 冫 in the facts line is small. At this resolution I can't reliably confirm that both of its strokes are distinct, though it isn't blank.
  - The reading じゅんきょうじゅ breaks across two lines ("じゅん / きょうじゅ"). This is ordinary wrapping and I am not counting it as a defect.
  - The image cannot show which font file was used, or that the result was saved to the log.

## Turn 4: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-curated-On-question.png

**Resource 4 of 29: `n1-082-curated-On-question.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** It shows "Kanji readings" with "Attempts left: 1" and a note explaining that queued repeats are included in the count.
- **The kanji:** A large 准 is drawn in a different calligraphic face from the feedback screen. That fits the font-variation setting the test turned on. The two left-hand 冫 strokes are distinct: an upper dot and a long sweeping lower stroke. 隹 sits on the right, there is no lower 十, and the character is not blank or a box.
- **Question and choices:** "Pick the on'yomi" is followed by four unselected buttons: カン, ジュウ, ジョウ and ジュン. Only one is the correct sourced reading. The order matches the feedback capture. There is also an "I don't know" link.
- **Limits:** The image cannot tell me which font was used. That this was the only question and the session was offline comes from supplied evidence, though the status-bar icon fits being offline.

## Turn 5: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-drawing-feedback.png

**Resource 5 of 29: `n1-082-drawing-feedback.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Header and status:** The "Drawing" screen shows "准 quasi-; associate rank", then "Practice only: this attempt is not graded." and "Well drawn!".
- **Two panels:**
  - "Your drawing" shows ten blue strokes from the injected reference paths. The two separate 冫 marks are on the left and 隹 is on the right, with no 十 below.
  - "Correct strokes" shows ten green strokes numbered 1 to 10. Strokes 1 and 2 are the 冫 marks, and 3 to 10 form 隹. The numbers can be read, though 6, 7 and 8 sit close together.
- **Grading note:** "Graded by stroke shapes only (handwriting model not available)." This shows the comparison is shape-only and does not use handwriting recognition.
- **Article below:** The heading and facts line appear again, with Strokes 10, 冫 (no. 15) and N1 (community list). The meaning text and the approval sentence "批准 ひじゅん means ratification" follow. The last line is cut off at the bottom edge, which is normal for a scrolling screen.
- **Limits:**
  - The small 冫 in the facts line can't be fully resolved at this resolution.
  - These strokes were injected by the test, not drawn by a person.
  - That nothing was saved to the drawing log for this practice attempt rests on the supplied test assertion.

## Turn 6: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-drawing-recall-feedback.png

**Resource 6 of 29: `n1-082-drawing-recall-feedback.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** "Drawing" with the header "准 quasi-; associate rank" and a red "Here is the kanji" message, which is what appears after giving up on recall.
- **Panels:** "Your drawing" is empty. "Correct strokes" shows ten numbered green strokes: 1 and 2 are the separate 冫 marks and 3 to 10 form 隹, with no 十 below. The numbers can be read, though 4, 6 and 7 sit close together. A "Next" button follows.
- **Article below:**
  - The heading and facts line appear again.
  - The meaning text and the approval sentence (批准 ひじゅん, "Not every compound containing 准…") follow.
  - The start of the "Modern-shape mnemonic, not etymology:" passage is cut off at the bottom edge, which is normal scrolling.
  - I see no blank areas or replacement boxes.
- **Limits:**
  - This shot does not show the earlier recall prompt, so I can't check whether 准 was hidden while recall was being tested.
  - That a failing grade was saved after "Next" rests on the supplied assertion.
  - The small 冫 in the facts line can't be fully resolved at this resolution.

## Turn 7: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-drawing-trace.png

**Resource 7 of 29: `n1-082-drawing-trace.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** "Drawing" with "Attempts left: 1", "Trace the kanji for", the prompt "quasi-; associate rank" and "Ungraded tracing practice. You'll try from memory later."
- **Trace guide:** A faint blue 准 sits on a quartered grid, with strokes numbered 1 to 10. Strokes 1 and 2 are clearly two separate 冫 marks, and 3 to 10 form 隹, with no lower 十. The numbers are readable, and the order matches the "Correct strokes" panel in resources 5 and 6.
- **Status line and buttons:** "Downloading the handwriting model (first use only)…" is shown, and Undo, Clear and Check are greyed out. This shot was taken before any strokes were injected.
- **Observation (app behaviour, outside the content scope, not a content defect):** The device was offline, yet the screen says the model is downloading. The later feedback screen says "handwriting model not available". This shows the transient state before that message appeared. Whether the download message is misleading offline is an app UX question.
- **Limits:** The image cannot show whether Check later became enabled; that rests on the supplied assertions. Injected strokes are not human handwriting.

## Turn 8: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-font-panel-1.png

**Resource 8 of 29: `n1-082-font-panel-1.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Panel content:** "Panel 1 / 3" shows the 24-character line (中 事 備 先 典 冫 准 助 十 基 大 女 学 彼 手 批 授 教 木 氵 準 生 田 義) in four rows labelled Gothic, Mincho, Textbook and Brush.
- **No missing glyphs:** I see no blank cells or replacement boxes in any of the four rows.
- **Typefaces:** The Mincho, Textbook and Brush rows are visibly different faces. Textbook spacing is wider, so 手 wraps to its second line.
- **冫 and 氵:** In every family these look like the same plain fallback shape, which matches their identical raster hashes. 冫 clearly shows two marks and 氵 three. The two are not collapsed into one shape. A change of font alone is not a defect.
- **准 versus 準:** 准 shows 冫 with 隹 and no lower 十. 準 shows 氵 and 隹 above a lower 十. They stay distinguishable in all four families.
- **Footer:** "Inspect all 31 scoped Han; focused 准/準/集/進/難, 冫/氵/辶/隹…" renders legibly.
- **Limits:** At 18sp and this resolution, fine stroke detail in the denser characters (備, 義, 準 in Brush) can't be checked closely. The image cannot identify the fallback font, and this is an emulator, not a phone.

## Turn 9: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-font-panel-2.png

**Resource 9 of 29: `n1-082-font-panel-2.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Panel content:** "Panel 2 / 3" shows 聞 講 辶 進 隹 集 難 in the Gothic, Mincho, Textbook and Brush rows.
- **No missing glyphs:** I see no blank cells or replacement boxes.
- **辶 and 隹:** Both look like the same plain fallback shape in every family. This is most noticeable in the Mincho and Textbook rows, where 隹 looks heavier than the neighbouring characters. That matches their identical raster hashes and is not a glyph failure.
- **Look-alikes:**
  - 進 keeps 辶 wrapping 隹.
  - 集 keeps 隹 above 木.
  - 難 keeps its dense left block beside 隹.

  None of the look-alikes collapses into another, and their shapes match the descriptions in 准.md:58–59.
- **Footer:** The footer line renders legibly.
- **Limits:**
  - I can't tell whether 辶 is drawn with one dot or two at this size and resolution. That detail does not affect the article's comparison (進 has 辶).
  - The image cannot identify the fallback font, and this is an emulator, not a phone.

## Turn 10: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-font-panel-3.png

**Resource 10 of 29: `n1-082-font-panel-3.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Panel content:** "Panel 3 / 3" shows 准 準 集 進 難 冫 氵 辶 隹 and the whole word 准教授 in the Gothic, Mincho, Textbook and Brush rows.
- **No missing glyphs:** I see no blank cells or replacement boxes. 准教授 appears in full, as three characters, in every family.
- **准 versus 準:** In every row, 准 shows two 冫 marks with no lower 十, while 準 shows three 氵 marks and a lower 十. When the standalone 冫 and 氵 are side by side, two marks and three marks are clearly distinct.
- **Fallback shapes:** 冫, 氵, 辶 and 隹 again look the same in every family. In the Mincho and Textbook rows the standalone 隹 looks heavier than its neighbours. That fits their identical hashes and the "Fallback families may coincide" note, and is not a defect.
- **Other characters:** 集, 進 and 難 keep their distinctive parts (木 below, 辶, the dense left block). The footer line renders legibly.
- **Limits:**
  - At 18sp and this resolution I can't check fine stroke detail, especially the Brush 難 and 準.
  - The image cannot identify the fallback font, and this is an emulator, not a phone.

## Turn 11: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-former-forward-30.png

**Resource 11 of 29: `n1-082-former-forward-30.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** The 准教授 "associate professor" article, scrolled to "Synonyms and antonyms". All four bullets match `准教授.md:37–44`:
  - 助教授 じょきょうじゅ is underlined as a link, with the line "replaced by 准教授 in April 2007".
  - 助教 じょきょう is plain text, with the line "separate rank, not an abbreviation".
  - 助手 じょしゅ is a link.
  - Both 教授 きょうじゅ and 先生 せんせい are links.
- **Following text:** "These are role and title comparisons, not strict antonyms." comes next, then both "Distinctive meaning" paragraphs in full: the 准教授です / not 准教授する paragraph and the one about no exact international equivalence, automatic promotion or 準教授.
- **Legibility:** All Japanese, kana and English are legible, with no blank areas or replacement boxes. 準教授 and 准教授 are visibly distinct when they appear side by side.
- **Minor wrapping:** The reading じゅんきょうじゅです breaks across lines as "じゅ / んきょうじゅです", which is ordinary wrapping. I'm not counting it as a defect.
- **Limits:** This is the state before the 助教授 link is tapped. That the tap actually opened 助教授 rests on later captures and the supplied route assertions.

## Turn 12: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-kanji-01.png

**Resource 12 of 29: `n1-082-kanji-01.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Header and facts line:** "准 quasi-; associate rank" with an "Article contents" link. The facts line reads Strokes 10 · Key 冫 (no. 15) · JLPT N1 (community list).
- **Body text:** The full "Meaning and origin" section is shown and matches `准.md:22–32`:
  - the rank text with a 准教授 じゅんきょうじゅ link;
  - "half-professor or a trainee awaiting automatic promotion";
  - the approval sentence with 批准 ひじゅん;
  - the labelled "Modern-shape mnemonic, not etymology" with 隹 and 冫.
- **Readings table:** "Scroll sideways to read all columns." is shown, then the ジュン | on row. The Typical-words cell starts 准教授 じゅんき… and is clipped at the right edge, which is what the scroll prompt anticipates. The cell continues "ょうじゅ — associate professor" on the next lines.
- **Legibility:** I see no blank areas or replacement boxes.
- **Unreadable detail:** The small 冫 used inline in the facts line and in "two marks of 冫" can't be resolved into two separate marks at this downscaled size. It isn't blank, and the article's claim is about the full character's shape, which the earlier large glyphs confirm. Whether it reads clearly on a real phone is unverified.

## Turn 13: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-kanji-03.png

**Resource 13 of 29: `n1-082-kanji-03.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** The 准 article, scrolled so "Meaning and origin" is at the top. All three paragraphs from `准.md:22–32` are shown in full:
  - the rank paragraph with the 准教授 じゅんきょうじゅ link and the warnings against "half-professor" and "trainee awaiting automatic promotion";
  - the approval paragraph with 批准 ひじゅん;
  - the labelled modern-shape mnemonic.
- **Readings table:** "Scroll sideways to read all columns." and the ジュン | on | 准教授 じゅんき… row appear again. The Typical-words cell is clipped at the right edge, as signposted.
- **Note below the table:** It matches lines 40–42 exactly: it covers the sole on-reading, says the record lists no kun-readings, and says other dictionaries' readings don't change the card's metadata.
- **"Common words" heading:** It is cut off at the bottom edge, which is normal scrolling.
- **Legibility:** I see no blank areas or replacement boxes.
- **Unreadable detail:** As before, the small inline 冫 in the mnemonic can't be resolved into two marks at this downscaled size, though it isn't blank. Readability on a real phone is not verified.

## Turn 14: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-kanji-10.png

**Resource 14 of 29: `n1-082-kanji-10.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Readings table:** The 准 article is scrolled to "Readings". It shows "Scroll sideways to read all columns." and the ジュン | on | 准教授 じゅんき… row, with the cell clipped at the right edge as signposted. The full note follows: sole on-reading, no kun-readings, other dictionaries don't change the metadata.
- **Common words:** Both bullets are shown in full: "准教授 じゅんきょうじゅ — associate professor" as a link, and "批准 ひじゅん — ratification" as plain text.
- **Notes:**
  - The 準 bullet is shown: 準 is a link and has 氵 at the upper left and 十 below, while 准 has two left-hand 冫 marks and no lower 十.
  - The spelling bullet is shown: 準備 じゅんび and 基準 きじゅん are links, 批准 ひじゅん is plain, and it includes "JMdict also recognizes 準教授… current… title… is 准教授".
  - The look-alike bullet starts (集 has 木 below 隹, 進 has 辶) but is cut off at the bottom edge, which is normal scrolling.
- **Legibility:** I see no blank areas or replacement boxes. 準教授 and 准教授 are distinct when they appear together.
- **Inline 冫 and 氵:** These differ visibly. 氵 shows three marks, and 冫 is a smaller two-part mark that is hard to resolve at this downscaled size. They don't collapse into one shape, but whether the inline 冫 is clear on a real phone is unverified.

## Turn 15: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-kanji-12.png

**Resource 15 of 29: `n1-082-kanji-12.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Table scrolled sideways:** This is the same "Readings" area as resource 14, but the table has been scrolled horizontally. The left labels are now clipped ("ading", "ュン"), and the Typical-words cell is fully visible: "准教授 じゅんきょうじゅ — associate professor", with 准教授 as a link. Taken together with resource 14, the left and right states make up the whole row. Nothing is missing.
- **Rest of the screen:** It matches resource 14:
  - the note about the sole on-reading and no kun-readings;
  - both Common words bullets (准教授 as a link, 批准 ひじゅん);
  - the Notes on 準 and 准 shapes, the spelling note with 準備 and 基準 links and 準教授 recognised;
  - the start of the look-alike bullet, cut off at the bottom edge.
- **Legibility:** I see no blank areas or replacement boxes.
- **Limits:** The small inline 冫 is still hard to resolve at this downscaled size, though it is visibly different from the three-mark 氵. Readability on a real phone is not verified.

## Turn 16: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-kanji-15.png

**Resource 16 of 29: `n1-082-kanji-15.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** The 准 article scrolled to the end. The bottom of the table cell ("professor") is cut off at the top edge, which is normal scrolling.
- **Common words:** The full reading note is shown, then both bullets: 准教授 じゅんきょうじゅ — associate professor (a link) and 批准 ひじゅん — ratification.
- **Notes:** All three bullets are shown in full and match `准.md:51–60`:
  - 準 (a link) with 氵 and 十, against 准 with two 冫 marks and no 十;
  - the spelling bullet with 準備 and 基準 as links, 批准 plain, and 準教授 recognised while 准教授 is the current title;
  - the look-alike bullet with 集, 進 and 難 as links ("集 has 木 below 隹, 進 has 辶, 難 dense left-hand block… not associate rank or approval").
- **Sources:** The metadata and source paragraph matches lines 62–65, with links to KANJIDIC2, CC BY-SA 4.0, JMdict, Digital Daijisen: 准, and Nipponica and 大学事典: 准教授.
- **Legibility:** I see no blank areas or replacement boxes.
- **Limits:** The small inline 冫 is still hard to resolve at this downscaled size, though it differs from 氵. Whether the external links would work is not tested.

## Turn 17: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-kanji-backlink.png

**Resource 17 of 29: `n1-082-kanji-backlink.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **What the pixels show:** The header "准 quasi-; associate rank" and the "Readings" section: the ジュン | on | 准教授 じゅんき… row (clipped on the right, with the scroll prompt), the reading note, both Common words bullets and the Notes. The look-alike bullet is cut off at the bottom edge.
- **Comparison with earlier captures:** The content looks the same as resource 14 (`kanji-10`) to the eye.
- **What it supports:** This shot fits the 准 card having been opened, and it is the state the test reaches after tapping the 准 link in the 准教授 article.
- **What it does not show:** The pixels themselves don't show how the screen was reached. That it came from the word article's 准 link (the word-to-kanji direction) rests on the supplied route sequence and assertions.
- **Legibility:** I see no blank areas or replacement boxes.
- **Limits:** The small inline 冫 is still hard to resolve at this downscaled size, though it differs from 氵.

## Turn 18: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-meaning-feedback.png

**Resource 18 of 29: `n1-082-meaning-feedback.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** "Quiz" shows a large serif 准, with the two 冫 marks clearly separate and no lower 十. Below it are "Correct!" and four choices: "whale", "imitate; emulate", a green "✓ quasi-; associate rank" and "crown; peerless". "Next" and "I guessed" follow, then the start of the article, which matches the source.
- **The choices shown are not the curated wrong answers.** None of the curated choices 集/進/難 (gather / advance / difficult) appears. The app chose other cards' titles, presumably because those three cards aren't in the N1 stack. So this capture does not show the curated set in use.
- **"imitate; emulate" overlaps one of 准's secondary senses.** This is a hypothesis about quiz ambiguity, not an established defect:
  - JMdict lists 准える (なぞらえる, "to liken; to pattern after; to imitate"), but only as a *rarely used kanji form*.
  - The supplied Daijisen and Jitsu observation gives a なぞらえる gloss for 准.
  - KANJIDIC2's Spanish meanings include "imitar", though its English meanings do not.

  A learner who knows that sense could find this choice defensible. Because the form is rare and the card doesn't teach that sense, I rate the risk as low. "whale" and "crown; peerless" don't overlap. This is the first rendered evidence for the random-pool limit I noted in my original review.
- **Legibility:** I see no blank areas or replacement boxes.
- **Limits:**
  - I can't identify which cards supplied "imitate; emulate" and "crown; peerless".
  - That the correct answer was recorded rests on the supplied assertions.

## Turn 19: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-meaning-question.png

**Resource 19 of 29: `n1-082-meaning-question.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** "Quiz" with "Attempts left: 1" and the note about queued repeats. A large calligraphic 准 is shown, with two separate 冫 strokes, 隹 on the right and no lower 十.
- **Question and choices:** "What does it mean?" is followed by four unselected buttons: whale, imitate; emulate, quasi-; associate rank and crown; peerless. There is also an "I don't know" link. The choices and their order match the feedback capture.
- **Curated wrong answers not in use:** This confirms the actual question did not offer the curated 集/進/難 titles (gather / advance / difficult).
- **Possible ambiguity:** The "imitate; emulate" concern from resource 18 applies here too. It is a low-risk hypothesis, not an established defect: 准 can carry an "imitate" sense only through the rare spelling 准える (なぞらえる), a Jitsu gloss and KANJIDIC2's Spanish meaning "imitar". The two other wrong choices don't overlap.
- **Legibility:** I see no blank areas or replacement boxes.
- **Limits:** The pixels can't show which cards supplied the wrong choices, or whether the curated choices would appear in other configurations.

## Turn 20: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-selection.png

**Resource 20 of 29: `n1-082-selection.png`.** I read it with one `view` call. The image appears downscaled to about 900×2000.

- **Screen:** "Kanji" shows "N1 · 114 cards", with the N1 chip highlighted among N5, N4, N3, N2, N1, All and a clipped "St…" chip, which suggests the chip row scrolls sideways. Below are "Only cards tagged N1." and "Each stack keeps its own review schedule."
- **Counts:**
  - Meaning quiz: 1 due, 0 new.
  - Drawing: 0 due, 1 new.
  - Readings (on'yomi and kun'yomi): 1 due, 0 new.

  Each has a Start button, and there is a "Browse all kanji" button.
- **What it supports:** This matches the supplied set-up: one 准 meaning item and the single on-reading key due, with no drawing state seeded. The 114-card N1 count is visible here.
- **Not visible:** Which card or reading is due. That rests on the supplied assertions.
- **Legibility:** I see no blank areas or replacement boxes.

## Turn 21: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-successor-reverse-31.png

**Resource 21/29: `n1-082-successor-reverse-31.png`.** I made one view call for this resource. Its pixels were then summarised out of my context, so this note relies on what I recorded at the time. I received a downscaled frame of about 900×2000, not full-resolution bytes.

- **Header:** the 助教授 article shows "associate professor (former Japanese title)".
- **Meaning paragraph:** it reads "renamed 准教授 (じゅんきょうじゅ), associate professor, in April 2007". 准教授 is an underlined link, which matches the change at `助教授.md:16`. The paragraph renders in full, with no blanks or replacement boxes.
- **Examples:** both examples are legible, with kana and English, and the 当時 note is present.
- **How the kanji combine:** shows 助, 教 and 教授 links and ジョ+キョウ+ジュ.
- **Synonyms (start):** "准教授 is the successor…" appears as plain text, followed by 助教 (じょきょう).

That this screen was reached through the reverse route, and that the link navigates to 准教授, rests on the supplied route evidence. The image does not show it. Nothing on this screen looks like a content defect.

## Turn 22: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-system-back-to-kanji.png

**Resource 22/29: `n1-082-system-back-to-kanji.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back 准 quasi-; associate rank".
- **Scroll position:** the screen is partway down the 准 article. A clipped "professor" from the end of the Readings table shows at the top, which suggests the scroll position was kept after the system back.
- **Readings note:** the sole ジュン on-reading, no kun-readings, and other dictionaries do not change the card's source metadata.
- **Common words:** "准教授 じゅんきょうじゅ — associate professor", with 准教授 underlined as a link, and "批准 ひじゅん — ratification" as plain text.
- **Notes:**
  - The 準/准 shape contrast: 氵 and 十 for 準, two left-hand 冫 marks and no lower 十 for 准.
  - Spellings are not interchangeable: 準備 and 基準 are links, 批准 is plain, and 準教授 is recognised while 准教授 is taught.
  - The 集/進/難 look-alikes are links, with "not associate rank or approval".
- **Metadata and sources:** fully visible.

There are no blanks or replacement boxes. The inline 氵 visibly differs from the smaller inline 冫, but I can't confirm at this size that the 冫 shows two marks. That this screen came from a system back from the word article rests on the supplied route; the pixels alone don't show it. I see no content defect.

## Turn 23: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-system-back-to-teach.png

**Resource 23/29: `n1-082-system-back-to-teach.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back 教 teach, instruct".
- **Readings table:** the end of the table shows おし.える and おそ.わる (kun) rows. The table is clipped on the right, which is expected for the sideways-scrolling table.
- **Common words:** 教える, 教わる, 教室, 教科書 and 儒教 appear as before. The added last bullet "准教授 じゅんきょうじゅ — associate professor" is an underlined link (the `教.md:39` change). It has the same reading and gloss as the 准 card.
- **Notes:** the existing 教える/教わる note and the 考/校/木 note are unchanged.
- **Metadata:** fully visible.

There are no blanks or replacement boxes, and the added bullet fits with the existing list. That this screen came from a system back from 准教授 rests on the supplied route; the pixels alone don't show it. I see no content defect.

## Turn 24: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-system-back-to-word-from-teach.png

**Resource 24/29: `n1-082-system-back-to-word-from-teach.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back 准教授 associate professor".
- **How the kanji combine:**
  - 准, 教授 and 教 are underlined links. 授 is plain text. That fits my earlier limit that the existence of a 授 card is unverified, and it isn't a defect.
  - It explains the modifier and head structure, teaching and imparting, ジュン+キョウ+ジュ, and "not 'half a professor.'"
- **Synonyms and antonyms:**
  - 助教授 is a link: "former title replaced… April 2007".
  - 助教 is plain text: "a separate rank, not an abbreviation".
  - 助手 is a link: "assistant… does not by itself identify".
  - 教授 and 先生 are links: "professor rank" and "broader designation/address".
  - Closing line: "not strict antonyms".
- **Distinctive meaning:** it begins with "rank noun, not a verb" and 准教授です. It is cut off at the bottom after "教授する does not".

There are no blanks or replacement boxes. じゅんきょうじゅです wraps mid-word, which is not a defect. That this screen came from a system back from 教 rests on the supplied route; the pixels alone don't show it. I see no content defect.

## Turn 25: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-system-back-to-word.png

**Resource 25/29: `n1-082-system-back-to-word.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Same article view as R24:** the content looks identical: the "← Back 准教授 associate professor" header, the How-the-kanji-combine paragraph and the full Synonyms list. The Distinctive-meaning paragraph is cut off at the same point, after "教授する does not".
- **Status-bar time:** shows 2:43, against 2:44 in R24, so this was a separate capture.
- **Links and rendering:** 准, 教授, 教, 助教授, 助手, 教授 and 先生 are underlined links; 授 and 助教 are plain. There are no blanks or replacement boxes, and じゅんきょうじゅです wraps mid-word.

That this screen came from a system back from 准 (not from 教) rests on the supplied route; the pixels don't tell the two routes apart. I see no content defect.

## Turn 26: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-word-02.png

**Resource 26/29: `n1-082-word-02.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back 准教授 associate professor".
- **Meaning:** describes an established academic rank below 教授 (shown as a link, with きょうじゅ), with teaching and research responsibilities, and "not a professor's personal helper".
- **Examples:** both appear with full kana and English, and match the source.
  - 彼女は大学の准教授です。 (かのじょはだいがくのじゅんきょうじゅです。) — She is an associate professor at a university.
  - 田中准教授の講義を聞きました。 (たなかじゅんきょうじゅのこうぎをききました。) — I listened to Associate Professor Tanaka's lecture.
- **Address note:** follows the examples. 田中先生 (たなかせんせい) is given as the respectful form of direct address, and 先生 (a link) "is not itself a statement of this particular academic rank".
- **How the kanji combine:** appears as in R24.
- **Synonyms:** begins with the 助教授 link; the bullet is cut off at the bottom edge.

There are no blanks or replacement boxes, and the kana in the examples wraps at line ends, which is not a defect. I see no content defect.

## Turn 27: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-word-07.png

**Resource 27/29: `n1-082-word-07.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Same view as R24 and R25:** the content looks identical: the "← Back 准教授 associate professor" header, How the kanji combine and the full Synonyms list. The Distinctive-meaning paragraph is cut off at the same point, after "教授する does not".
- **Status-bar time:** shows 2:43.
- **Links and rendering:** 准, 教授, 教, 助教授, 助手, 教授 and 先生 are links; 授 and 助教 are plain. There are no blanks or replacement boxes.

This screen adds no new content beyond R24 and R25. Whether it is byte-identical to either is not established. I see no content defect.

## Turn 28: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-word-09.png

**Resource 28/29: `n1-082-word-09.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back 准教授 associate professor".
- **Synonyms:** the full list, matching R24.
- **Distinctive meaning:** both paragraphs now appear in full, and they match the source.
  - The first says 准教授 is a rank noun, not a verb. It uses 准教授です and says 教授する "does not license 准教授する for having this job."
  - The second warns against assuming exact international equivalence or automatic promotion. It notes that JMdict lists 準教授 with the same reading and that 准教授 is the current title.
- **Rendering:** there are no blanks or replacement boxes. じゅんきょうじゅです wraps mid-word, which is not a defect.

This is the first capture in this sequence that shows the whole Distinctive-meaning section. Only the Sources/metadata lines at the end aren't in this frame. I see no content defect.

## Turn 29: C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-082-native\attempt-1\n1-082-word-15.png

**Resource 29/29: `n1-082-word-15.png`.** I made one view call. The frame I received was about 900×2000, so likely downscaled; I can't claim full-resolution bytes.

- **Header:** "← Back 准教授 associate professor".
- **Scroll position:** the screen is at the end of the article. The top line ("relevant when reading older documents") is clipped by scrolling.
- **Synonyms:** 助教 (plain), 助手, 教授 and 先生 (links), and "not strict antonyms".
- **Distinctive meaning:** both paragraphs appear in full, matching R28.
- **Sources line:**
  - "Dictionary: JMdict, entry 2178020; comparisons 1237160, 1344540, 1344550, 1344650 and 1387990."
  - "Japanese rank and April 2007 reform: Nipponica and 大学事典: 准教授", shown as a link.
  - 2178020 matches the 准教授 entry and 1344550 matches 助教授 in my notes. I did not independently check the other comparison IDs.

There are no blanks or replacement boxes. With R26 and R28, this completes the visual coverage of the word article down to its source footer. I see no content defect.

## Turn 30: FINAL REPORT

# SAME082: dependent original-session visual confirmation of batch 082

I found no defects in any of the four scoped items: every verdict is CLEAN and there are no findings. The visual pass agrees with my original textual review and reverses none of it. All of this is emulator evidence only, not a physical phone, and I did not verify anything in Git or upstream myself.

## Snapshot

- **Evidence HEAD:** 276df59577c2e4dcfe47fa53e9e820d228c9d5bf.
- **Teaching content reviewed:** b6bcc8f144cd781917abdb2ca510f663d1339a56.
- **Native archive:** 4f5812bc.
- **Model:** Claude Opus 5.5 (claude-opus-5.5). Only the `view` tool was available.

## Scope

**Original textual phase.** I read `control\batch-082-initial-packet.txt` with one full view call and saw no truncation notice. I couldn't confirm the 3084-line count myself because the output had no line numbers. My findings and optional items from that phase are carried forward unchanged.

**Visual phase.**
- I read `batch-082-visual-source-packet.txt` once, then 28 original PNGs, one view call per turn. The host says these represent all 51 captures after byte-level deduplication. I did not verify that grouping.
- No reads were denied or missing. The images I received appear downscaled to about 900×2000; I make no claim to full-resolution bytes or independent hash checks.
- The pixels for resources 1–21 were later summarised out of my context. For those, this report relies on the observations I wrote at the time. Resources 22–29 were inspected directly in this context.

**Items reviewed:**
- the new `kanji\准.md`
- the new `words\准教授.md`
- the bullet added at `kanji\教.md:39`
- the successor link added at `words\助教授.md:16`, read with its paragraph

Other reused content was treated as context only. I made no fresh dictionary lookups.

## Verdicts

| Item | Correctness | Scoped coverage | Visual comprehensibility (bounded) |
|---|---|---|---|
| New `准.md` | CLEAN | CLEAN | CLEAN |
| New `准教授.md` | CLEAN | CLEAN | CLEAN |
| `教.md:39` added bullet | CLEAN | CLEAN | CLEAN |
| `助教授.md:16` successor link | CLEAN | CLEAN | CLEAN |

My original textual conclusions carry over unchanged:
- **Reading:** ジュン is the only reading, with no kun-reading, and the card doesn't deny other dictionaries' readings.
- **Senses:** both the rank sense and the approval sense (批准 ひじゅん) are covered.
- **准 vs 準:** the shape contrast is explained; the two spellings are not presented as freely interchangeable; 準教授 is recognised as an alternative spelling.
- **准教授:** 准 modifies the head 教授; 教 contributes teaching and 授 imparting.
- **Rank and history:** 准教授 is the current title. It replaced 助教授 in April 2007. 助教, 助手 and 先生 are kept distinct. The article rules out "helper", "half a professor", automatic promotion and international equivalence, and it rejects the verb 准教授する.
- **Card facts:** the mnemonic is qualified, not presented as etymology. The facts are 10 strokes, grade 8, radical 冫 (15) as opposed to 氵. N1 is presented as a community level, not an official syllabus.

What the pixels showed:
- **准 card, all sections rendered:** both 准 article routes rendered fully (R12–R17, R22).
- **准教授 article, all sections rendered:** both example sentences, kana, English and the Sources footer all render (R11, R24–R29). The article reads correctly from top to bottom across R26, R28 and R29.
- **Readings table:** the table scrolls sideways and says so on screen. Its two scroll states together show the whole row (R12–R15).
- **教 bullet:** the added bullet is visible and is a link (R23).
- **助教授 link:** the successor link is visible inside the full paragraph (R21).
- **Fonts:** all 31 Han characters in scope and 准教授 render in all four families (Gothic, Mincho, Textbook, Brush) with no blanks or replacement boxes (R8–R10).
  - 冫 (two marks) and 氵 (three) look distinct, and so do 准 and 準.
  - 集, 進 and 難 keep their distinguishing parts.
  - Pixels and hashes don't identify which fallback font is used, and a font being absent from the character map is not a glyph failure.
- **Quiz and drawing:** the reading quiz shows one valid answer (R3–R4). The drawing screens show the ten reference strokes (R5–R7). The N1 stack shows 114 cards (R20).

## Findings

None proven.

## Optional (not defects)

1. **Quiz ambiguity in a larger pool (carried from my original review):** 準.md teaches "semi-, quasi-, associate", so in a larger, uncurated 準 quiz pool, 准's title could also be a defensible answer.
   - R18–R19 are the first rendered evidence for this. The captured meaning-quiz alternatives were whale, "imitate; emulate", crown and peerless; the curated 集/進/難 distractors did not appear.
   - "imitate; emulate" overlaps a minor sense of 准 (准える, a rarely used spelling). This is a low-risk hypothesis. I make no claim that the random pool is safe in general.
2. **Possible additions (carried from my original review):** 批准 could be added to the ジュン reading row, and 准看護師 or 准尉 could be added as rank examples.
3. **Small inline 冫:** in the facts line and body text, the inline 冫 can't be resolved into two marks at the size I received, though it visibly differs from 氵. Readability on a real phone is unknown.
4. **授 not linked:** in the How-the-kanji-combine paragraph, 授 is plain text. This fits my unverified limit about whether a 授 card exists, and it is not a defect.
5. **App UX, outside content scope:**
   - While offline, the trace screen shows "Downloading the handwriting model…" with its buttons disabled (R7).
   - The screen tree captured at teardown showed a loading state, likely a transient reload during cleanup.

## Limits

**Pixel evidence:**
- Everything comes from an API 35 read-only emulator (emulator-5580), not a physical phone.
- The images were downscaled; fine strokes, the 辶 dot form and small inline radicals can't be resolved.
- I could not identify which font face is rendering any character.
- That System Back and link taps reached the expected screens rests on the supplied route evidence. The pixels show only the destination screens.
- R24, R25 and R27 look identical, and I did not establish whether any are byte-identical.

**Supplied execution evidence, not run by me:**
- the production archive sync, with the counts, version and zero problems as stated in the packet
- the fixture and test pass status, adb exit and log file
- the persisted quiz key and progress log
- the offline state
- that the drawing grade is saved on Next
- the inherited all-40 font evidence and 558/559 test runs, which were not rerun
- the original out-of-memory failure (557) and the test-only Android build note

**Drawing:** the strokes were reference strokes injected by the test, not human handwriting. There was no successful recall, no ML Kit recognition and no model download.

**Not verified at all:**
- anything in Git or upstream
- title uniqueness across all cards, whether a 授 card exists, and the other JMdict comparison IDs
- native-speaker acceptance, real fonts on a physical phone, and learning effectiveness

**Reconciliation of my earlier limits:**
- **Partially resolved:** rendering and runtime. The emulator pixels show the content renders, but not on a physical phone.
- **Unresolved:**
  - physical-phone, native-speaker and learning evidence
  - final integration with current main, publication, CI, an immutable ZIP and general release
  - safety of the random quiz pool across the whole set
