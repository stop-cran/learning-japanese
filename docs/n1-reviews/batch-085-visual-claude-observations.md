TURN1; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-visual-source-packet.txt
I read resource 1 of 24 once, in full, with no truncation marker; I can't confirm its byte or line count from the output. It is the common packet only, so I have not looked at any screenshots yet and cannot judge rendering.

- **Teaching text:** the hashes for all four new articles, the 固 bullet and the revised 凝らす (`40d5f79a…`) match my earlier packets. The only teaching change is still the 努力 exclusion.
- **Reported quiz and import results:**
  - The route JSON reports the four default meaning choices 凝 / 准 / 冗 / 凹, with no fallback padding in either the N1 pool or the full pool.
  - It reports the full six readings kept, with on ギョウ and kun こ.る / こ.らす selected for quizzing. These reduce to the quiz keys ぎょう and こる only, and both kinds were marked good and done.
  - It also reports four reciprocal pairs (eight link directions), offline use, and one import with zero problems.
- **Test run:** two named instrumentation tests passed ("OK (2 tests)").
- **What is not covered:** the run used a test-only Android build on an API 35 emulator, not a phone. Drawing used 16 injected reference strokes, not human handwriting or ML Kit. These remain open limits.
- **Coverage index:** the 15 sheets list all 87 original screenshots (6 per sheet, 3 on the last).

The 15 sheets and 8 focused screenshots still need inspecting before any verdict.

TURN2; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-01.png
**Resource 2 of 24: `sheet-01.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames, absorbed-02, -03, -04, -05, -06 and -08. Frame 07 isn't on this sheet; I expect it is on sheet 2.
  - Frames 02–06 look the same: the top of the 凝る article.
  - Frame 08 is scrolled further down, through "Distinctive meaning".
- **Japanese and English text:** the header reads "凝る become stiff; get absorbed" with a Back link. Everything I could read matches the source:
  - the three example sentences (肩が凝る, ゴルフに凝っています, 凝った衣装) with kana readings and translations;
  - the notes on が / に, the godan forms 凝ります / 凝って / 凝らない, and the warning not to add な after 凝った;
  - the links to 熱中 / 夢中 / 集中 and 凝らす / 工夫を凝らす;
  - the 硬い contrast;
  - the こごる / しこる paragraph.
- **Glyphs:** no blank characters or tofu boxes. At this resolution, 凝 shows its 冫 radical clearly and doesn't look like any other character.
- **Cut-off text:** frame 08 ends at "not an exhaustive definition." at the bottom of the screen. That is the normal screen edge, not lost content.
- **Resolution:** small kana and the underlines under links are only just readable, but nothing important is illegible.

TURN3; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-02.png
**Resource 3 of 24: `sheet-02.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames, absorbed-10, -11, -13, -14, -15 and absorbed-forward. Frames 07, 09 and 12 are on neither sheet 1 nor sheet 2. That could be gaps in the capture numbering or frames placed on other sheets; I can't tell from these two sheets.
- **Frames 10–15 (the 凝る article):** all five show the same lower part of the article. Everything I could read matches the source:
  - the synonyms 熱中 / 夢中 / 集中;
  - the 凝らす / 工夫を凝らす note, including the warning not to swap に for を;
  - the contrast with 硬い;
  - the こごる / しこる paragraph;
  - the JMdict entries 1239070, 1238990, 1239060, 1594250 and 1636550, and the Digital Daijisen: 凝る link.

  The article's last line is visible, so the bottom of the article was reached.
- **Absorbed-forward (the 凝 kanji article, opened from the 凝る article):** the header reads "凝 congeal; become absorbed".
  - **Common words:** 凝固 / 凝る / 凝らす, 肩が凝る and 工夫を凝らす, with kana and English glosses.
  - **Notes:** the に凝る / を凝らす contrast, 凝った衣装 described as an inflected form, the 凍 / 固 / 硬 overlap, and the shape comparison.
  - **Shape comparison:** 准 is described as 隹 beside 冫, and 凝 as having a 疑-shaped right side. 冫, 隹, 冗 and 凹 are all legible and distinct.
  - The metadata line at the bottom is cut off by the screen edge, which is normal and not lost content.
- **Glyphs:** no blank characters or tofu boxes, and no lookalike characters collapsed into a misleading shape.
- **Resolution:** small kana and the underlines under links are only just readable.

TURN4; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-03.png
**Resource 4 of 24: `sheet-03.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames: absorbed-kanji-backlink, absorbed-reverse, absorbed-system-back-to-kanji, absorbed-system-back-to-word, curated-Kun-feedback and curated-Kun-question.
- **Kanji backlink (the 凝 readings table):**
  - The hint "Scroll sideways to read all columns." is shown above the table.
  - All six readings appear in source order: ギョウ (on), then こ.る, こ.らす, こご.らす, こご.らせる and こご.る (kun).
  - ギョウ, こ.る and こ.らす link to 凝固, 凝る and 凝らす. The three こご rows show unlinked forms (凝らす こごらす, 凝らせる こごらせる, 凝る こごる) and are worded as separately recorded readings.
  - The "Typical words" column is cut off at the right edge and the last row at the bottom. Both are normal table scrolling, which the hint signposts, not lost content.
- **Back navigation:**
  - Reverse and system-back-to-word both return to the 凝る article.
  - System-back-to-kanji returns to 凝's Common words and Notes, the same screen as absorbed-forward.
- **Kun question:**
  - The screen shows a large, legible 凝 with the prompt "Pick the kun'yomi" and "Attempts left: 2".
  - The choices are こる, こい, こずえ and へこむ, plus "I don't know".
  - None of the wrong choices is a reading of 凝. へこむ belongs to 凹, which is fine as a distractor.
  - こらす isn't offered as a separate answer, which fits こる being the only normalized kun key.
- **Kun feedback:**
  - The screen shows "Correct! — kun'yomi" with こる highlighted, and the full list "ギョウ、こる、こらす、こごらす、こごらせる、こごる". The list drops the okurigana dots; that's a display style, not an error.
  - The Next and "I guessed" buttons are shown.
  - The embedded article shows: 16 strokes, radical 冫 described as the two-stroke ice radical (no. 15), "N1 (community list)", and the start of "Meaning and origin".
- **Glyphs:** no blank characters or tofu boxes. 冫 and 隹 stay distinct, including in the shape note.
- **Resolution:** small labels are only just readable.

TURN5; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-04.png
**Resource 5 of 24: `sheet-04.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames: curated-On-feedback, curated-on-kun-done, curated-On-question, drawing-feedback, drawing-recall-feedback and drawing-trace.
- **On question:**
  - The screen shows a large, legible 凝 with the prompt "Pick the on'yomi" and "Attempts left: 1".
  - The choices are ジュン, オウ, ギョウ and ジョウ, plus "I don't know".
  - The three wrong choices are readings of the lookalikes 准 (ジュン), 凹 (オウ) and 冗 (ジョウ), and none is a reading of 凝.
- **On feedback:**
  - The screen shows "Correct! — on'yomi" with ギョウ highlighted, and the same full reading list as in the kun feedback.
  - The embedded article shows: 16 strokes, radical 冫 (no. 15), "N1 (community list)".
- **Done screen:** "Session complete" and "2 of 2 answers correct", with Done and "Practice more" buttons. That fits both quiz kinds finishing with a correct answer.
- **Drawing, trace stage:**
  - The trace guide shows a 凝 outline with strokes numbered 1 to 16, and the subtitle "Ungraded tracing practice".
  - The status line reads "Downloading the handwriting model (first use only)…" while Undo, Clear and Check look disabled. That fits the run being offline with no handwriting model.
  - At this resolution I can't confirm that each stroke's direction and order is correct.
- **Drawing, feedback stage:**
  - The screen shows "Practice only: this attempt is not graded." and "Well drawn!".
  - "Your drawing" shows the 16 injected reference strokes forming a recognisable 凝, beside the numbered correct strokes.
  - The note "Graded by stroke shapes only (handwriting model not available)" is shown. These are reference strokes injected by the test, not human handwriting.
- **Drawing, recall feedback (give-up path):** the screen shows "Here is the kanji" with an empty "Your drawing" panel and the numbered correct strokes.
- **Mnemonic text:** it reads "Modern-shape mnemonic, not etymology… an invented memory scene, not a historical or phonetic explanation." It does not deny that 疑 is a phonetic component.
- **Glyphs:** no blank characters or tofu boxes. 冫 renders in the radical line and in the mnemonic.
- **Resolution:** small stroke numbers and fine text are only just readable.

TURN6; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-05.png
**Resource 6 of 24: `sheet-05.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames, effort-02, -03, -04, -05, -07 and -09. Frames 06 and 08 aren't on this sheet.
  - Frames 02–05 look the same: the top of the 凝らす article.
  - Frames 07 and 09 scroll down through "Distinctive meaning" to the dictionary footer.
- **Header:** "凝らす concentrate; apply effort" with a Back link.
- **Text:** everything I could read matches the source:
  - the を-object framing;
  - the examples 目を凝らして見ました and 工夫を凝らしました, with kana readings and translations;
  - the 目を凝らす / 工夫を凝らす contrast;
  - the godan forms 凝らします / 凝らして / 凝らさない.
- **How the kanji combine:** 凝 writes こ and らす is the written ending.
- **Synonyms:** links to 集中 and 注ぐ, and the contrast between ゴルフに凝る and 工夫を凝らす.
- **Distinctive meaning:**
  - 息を凝らす is translated as "hold one's breath".
  - こごらす is described as a separately recorded reading.
  - The potential こらせる is told apart from the separate verb こごらせる.
  - The homophone 懲らす means "punish; chastise".
- **Footer:** frame 09 shows the full dictionary footer: JMdict entries 1239010, 1239000, 1239020, 1309500, 2572530, 2835904 and 1428180, plus the Digital Daijisen: 凝らす link. Frame 07 is cut off at that footer by the screen edge, which is normal.
- **Spacing:** a small gap appears before "（くふうをこらす）" in the 工夫を凝らす sentence. That is cosmetic and doesn't affect meaning.
- **Glyphs:** no blank characters or tofu boxes.
- **Resolution:** small kana and the underlines under links are only just readable.

TURN7; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-06.png
**Resource 7 of 24: `sheet-06.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames: effort-10, -12, -13, -14, effort-forward and effort-kanji-backlink. Frames 06, 08 and 11 are on neither sheet 5 nor sheet 6. I can't tell from these two sheets whether the numbering skips them or they are on other sheets.
- **Frames 10–14 (bottom of the 凝らす article):** all four show the same text, and it matches the source:
  - the How the kanji combine section and the 集中 / 注ぐ synonyms;
  - the contrast between ゴルフに凝る and 工夫を凝らす;
  - 息を凝らす, translated as "hold one's breath";
  - こごらす, the potential こらせる told apart from こごらせる, and 懲らす;
  - the full dictionary footer: JMdict entries 1239010 to 1428180 and the Digital Daijisen: 凝らす link.

  The article's last line is visible, so the bottom of the article was reached.
- **Effort-forward (the 凝 kanji article):** shows the same Common words and Notes content as absorbed-forward on sheet 2.
  - The 凝らす bullet reads "こらす — concentrate; apply effort".
  - In the shape note, 准 is described as 隹 beside 冫, and 冗 and 凹 are legible and distinct.
  - The metadata line is cut off at the bottom of the screen, which is normal.
- **Effort-kanji-backlink (the 凝 readings table):** the same table as on sheet 3.
  - The hint "Scroll sideways to read all columns." is shown.
  - All six readings appear in source order. ギョウ, こ.る and こ.らす are linked; the three こご rows are marked as separately recorded readings.
  - The right-hand and bottom edges are cut off by normal table scrolling, which the hint signposts.
- **Glyphs:** no blank characters or tofu boxes, and no lookalike characters collapsed into a misleading shape.
- **Resolution:** small kana and the underlines under links are only just readable.

TURN8; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-07.png
**Resource 8 of 24: `sheet-07.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames: effort-reverse, effort-system-back-to-kanji, effort-system-back-to-word, and font panels 1, 2 and 3.
- **Back navigation:**
  - Reverse and system-back-to-word both return to the 凝らす article at "How the kanji combine". The text matches the source, and the dictionary footer is cut off by the screen edge, which is normal.
  - System-back-to-kanji returns to the 凝 card's Common words and Notes, the same content as the forward frames.
- **Font panels, coverage:**
  - Panel 1 has 24 characters: 中付冗冫冷准凍凝凹力努固堅夢夫工度心息意懲気注液.
  - Panel 2 has 15: 濃点焦熱疑的目硬肩血衣装見隹集.
  - That makes 39 characters, matching the scoped count. Each appears in four rows: Gothic, Mincho, Textbook and Brush.
  - Panel 3 repeats the focus set 凝 疑 准 冗 凹 冫 隹 凍 固 硬 and the whole words 凝固, 凝る and 凝らす in all four families.
- **Font panels, glyph quality:**
  - I see no blank characters or tofu boxes.
  - 冫 renders as a small two-dot mark, clearly different from 隹.
  - 凝 and 疑 stay distinct, with 冫 on the left of 凝 only. 准, 冗 and 凹 are each distinguishable.
  - In the Textbook and Brush rows, 隹 (and possibly 冫) looks heavier or in a different style. That suggests a fallback typeface, which is a font change and not a defect. The pixels alone can't tell me which font was used.
  - The Textbook rows have wider letter spacing and wrap differently.
- **Resolution:** at this size I can't make out fine stroke detail, for example the exact shapes of the 疑 components in the Brush row. The characters themselves are identifiable.

TURN9; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-08.png
**Resource 9 of 24: `sheet-08.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames, kanji-01, -03, -04, -09, -11 and -12. Frames 02, 05–08 and 10 aren't on this sheet.
- **kanji-01 (top of the 凝 article):**
  - An "Article contents" link and the title "凝 — congeal; become absorbed".
  - The details line reads: 16 strokes, radical 冫 described as the two-stroke ice radical at left (no. 15), "N1 (community list)".
  - Meaning and origin links 凝固 and 凝る.
  - The mnemonic is labelled "Modern-shape mnemonic, not etymology" and is described as not a historical or phonetic explanation.
  - The Readings table starts with its "Scroll sideways" hint.
- **kanji-03 and -04:** the same content from Meaning and origin down to the こご.らす row.
- **kanji-09 and -12:** the full readings table from its top; the right edge is cut off as on earlier sheets.
- **kanji-11:** the table is scrolled sideways, so more of the "Typical words" column is visible.
  - The こご rows can now be read further: 凝らす こごらす — "cause to congeal; freeze; a separately recorded reading, not the linked article's primary こらす"; 凝らせる こごらせる — "cause to congeal; freeze; written ending らせる"; 凝る こごる — "congeal; jell; usually written in …".
  - The Reading column is cut off on the left (for example "ading" and "ョウ"). That is the expected cost of scrolling sideways, not lost content.
- **Text and glyphs:**
  - The readings show source order: ギョウ, こ.る, こ.らす, こご.らす, こご.らせる, こご.る.
  - There are no blank characters or tofu boxes. 冫 renders as a small two-dot mark in the details line and in the mnemonic.
- **Readability:**
  - The last row ("usually written …") is cut off at the bottom edge in every frame on this sheet.
  - At this resolution, small kana and fine strokes are only just readable.

TURN10; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-09.png
**Resource 10 of 24: `sheet-09.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames, kanji-14, -15, -17, -18, -20 and -21, all showing the 凝 readings table. Frames 13, 16 and 19 aren't on this sheet.
- **Two scroll positions alternate:**
  - **Scrolled sideways (14, 17, 20):** the Reading column is cut off on the left ("ading", "ョウ", "ご.らす"). The full width of the Typical words column is visible:
    - 凝固 ぎょうこ — coagulation; solidification
    - 凝る こる — become stiff; get absorbed in; be elaborate
    - 凝らす こらす — concentrate; apply effort
    - 凝らす こごらす — cause to congeal; freeze; a separately recorded reading, not the linked article's primary こらす
    - 凝らせる こごらせる — cause to congeal; freeze; written ending らせる
    - 凝る こごる — congeal; jell; usually written in …
  - **Unscrolled (15, 18, 21):** the full Reading column is visible (ギョウ, こ.る, こ.らす, こご.らす, こご.らせる, こご.る) and the right edge of Typical words is cut off.
- **Assessment of the cut-offs:** the "Scroll sideways" hint is shown in every frame. Between the two positions, each cell can be read, which fits target cells being shifted into view one at a time.
- **Last row:** in every frame, the こご.る gloss is cut off at the bottom of the screen after "usually written in". This sheet doesn't show the rest of that cell; it should show up when the page is scrolled down.
- **Text and glyphs:**
  - No blank characters or tofu boxes.
  - こご is clearly distinct from こ.
  - The okurigana dots show correctly in the Reading column.
  - The links on 凝固, 凝る and 凝らす are underlined, and the こご rows are not linked.
- **Resolution:** small kana are only just readable.

TURN11; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-10.png
**Resource 11 of 24: `sheet-10.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames, kanji-23, -24, -26, -27, -29 and -30. Frames 22, 25 and 28 aren't on this sheet.
- **kanji-23 and -24:** the readings table, scrolled sideways in 23 and unscrolled in 24, the same as on sheet 9.
- **kanji-26 and -27:** the page is scrolled down. These frames settle what sheet 9 left open:
  - The こご.る row ends "凝る こごる — congeal; jell; usually written in kana as こごる". The cell is complete.
  - The paragraph after the table reads: "The three こご readings are dictionary-verified recognition material, not additional readings of every example above … shoulder stiffness and enthusiasm in the linked 凝る article use こる, not こごる. The written ending of 凝らす is らす in both こらす and こごらす." This matches the source.
- **All frames:** the Common words section lists 凝固 ぎょうこ, 凝る こる, 凝らす こらす, 肩が凝る and 工夫を凝らす, with glosses.
- **kanji-29 and -30 (Notes):**
  - The に凝る / を凝らす contrast and 凝った衣装.
  - The 凍 / 固 / 硬 overlap.
  - The shape comparison: 准 is described as 隹 beside 冫, 凝 as having a 疑-shaped right side, 冗 as having a cover-like top and 凹 an inward dip, and the note says none of them means congealing or absorption.
  - The metadata line begins "KANJIDIC2, database 2026-306, 2026-11-02 (EDRDG; CC BY-SA 4.0). Words: JMdict, entries 1238990, 1239000, 1239010," and is cut off at the bottom of the screen. That is the normal screen edge.
- **Glyphs:** no blank characters or tofu boxes. 冫 and 隹 are distinct, and 冗 and 凹 are legible.
- **Resolution:** small kana are only just readable.

TURN12; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-11.png
**Resource 12 of 24: `sheet-11.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames, kanji-31, -32, -33, -35, -36 and -37. Frame 34 isn't on this sheet.
- **kanji-31, -32 and -33:** the same Common words and Notes view as on sheet 10. The metadata line is cut off at the bottom of the screen after "1239010,".
- **kanji-35, -36 and -37:** scrolled to the end of the 凝 article, so the bottom of the page is reached.
  - The metadata ends: "JMdict, entries 1238990, 1239000, 1239010, 1239020, 1239060, 1239070, 1239120, 1309500 and 1636550. Usage: Digital Daijisen: 凝る, 凝らす and 凝固."
  - The Common words bullets (凝る, 凝らす, 肩が凝る and 工夫を凝らす) and all the Notes text match the source.
- **Glyphs:** no blank characters or tofu boxes. In the shape note, 准, 隹, 冫, 疑, 冗 and 凹 are all legible and distinct.
- **Resolution:** small kana are only just readable.

TURN13; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-12.png
**Resource 13 of 24: `sheet-12.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames: kanji-38, kanji-39, meaning-feedback, meaning-question, selection and solid-back-to-reused-kanji.
- **kanji-38 and -39:** the bottom of the 凝 article, the same content as on sheet 11, with the full metadata and usage links visible.
- **Meaning question:**
  - A large 凝 with the prompt "What does it mean?" and "Attempts left: 1".
  - The choices are "concave; sunken" (凹), "quasi-; associate rank" (准), "superfluous; redundant" (冗) and "congeal; become absorbed", plus "I don't know".
  - That is the three curated wrong answers and no padding choices, which matches the source packet. None of the wrong answers overlaps with congeal or absorb.
- **Meaning feedback:**
  - "Correct!" with "congeal; become absorbed" highlighted, and the Next and "I guessed" buttons.
  - The embedded article shows 16 strokes, radical 冫 (no. 15) and "N1 (community list)".
- **Selection (the Kanji screen):**
  - "N1 · 117 cards", with the N1 chip selected and the "Only cards tagged N1." note.
  - Meaning quiz: 1 due, 0 new. Drawing: 0 due, 1 new. Readings (on'yomi and kun'yomi): 2 due, 0 new.
  - The chip row is cut off at the right edge ("St…"), which is normal horizontal overflow.
- **Back to the reused card (固 "firm; harden"):** the readings table is shown partly scrolled, cut off at the top and right edges.
  - Common words lists 固い かたい, 固体 こたい, and the changed bullet "凝固 ぎょうこ — coagulation; solidification". The link resolves, and the reading and gloss are correct.
  - The changed bullet visibly uses an em dash "—" while the neighbouring bullets use " - ". This confirms in the rendered app the cosmetic optional point I made before; it doesn't affect meaning.
  - The Notes and metadata of 固 are unchanged baseline content.
- **Glyphs:** no blank characters or tofu boxes. 冫, 隹, 冗 and 凹 are distinct.
- **Resolution:** small text is only just readable.

TURN14; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-13.png
**Resource 14 of 24: `sheet-13.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames: solid-back-to-word, solid-changed-bullet, solid-kanji, and solidify-02, -03 and -04.
- **Solidify 02–04 (top of the 凝固 article):** the three frames look the same. The text matches the source:
  - "With する… the material takes が", with the example 血液が凝固する。(けつえきがぎょうこする。) "Blood coagulates."
  - The water-to-ice sense, the choice between "coagulates" and "solidify", and "Not every 凝固 is water freezing."
  - How the kanji combine: 凝 + 固, read ギョウ + コ.
  - Synonyms 固まる, 凍る and 冷凍.
  - Distinctive meaning: contrasted with 集中.

  The text is cut off at the bottom of the screen, which is normal.
- **Solid-back-to-word and solid-kanji:** the lower part of the 凝固 article.
  - "Not the term for mental concentration", "not necessarily a change to ice", and "does not provide medical advice".
  - The footer: JMdict entry 1239120 and the Digital Daijisen: 凝固 link. The end of the article is reached.
- **Solid-changed-bullet (固 "firm; harden"):**
  - Common words lists 固い, 固体, and "凝固 ぎょうこ — coagulation; solidification". The bullet is linked and its reading and gloss are correct.
  - It again uses an em dash where the neighbouring bullets use " - ". That is cosmetic and was already noted as optional.
  - The readings table above is partly cut off at the top and right edges, which is normal scrolling. The rest of 固 is unchanged baseline content.
- **Glyphs:** no blank characters or tofu boxes. 凝, 固, 凍 and 冷 are legible and distinct.
- **Resolution:** small kana are only just readable.

TURN15; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-14.png
**Resource 15 of 24: `sheet-14.png`** (one full read; the tool may have downscaled the image)

- **Frames:** six labelled frames: solidify-06, -08, -10 and -11, solidify-forward and solidify-kanji-backlink. Frames 05, 07 and 09 aren't on this sheet.
- **Solidify 06–11:** the lower part of the 凝固 article, the same content as in solid-back-to-word on sheet 13.
  - The blood example's line is cut off at the top of the screen; the visible text runs from "Blood coagulates." through the footer.
  - The footer shows JMdict entry 1239120 and the Digital Daijisen: 凝固 link.
  - The end of the article is reached, and the text matches the source.
- **Solidify-forward (the 凝 kanji article, opened from 凝固):** the same Common words and Notes view as the other forward frames. The metadata line is cut off at the bottom of the screen, which is normal.
- **Solidify-kanji-backlink:** the 凝 readings table with the "Scroll sideways" hint.
  - All six readings appear in source order.
  - The right-hand and bottom edges are cut off, which is normal table scrolling.
- **Glyphs:** no blank characters or tofu boxes. 冫, 隹, 冗, 凹, 凍 and 硬 are distinct.
- **Resolution:** small kana are only just readable.

TURN16; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\inspection\sheet-15.png
**Resource 16 of 24: `sheet-15.png`** (one full read; the tool may have downscaled the image)

- **Frames:** three labelled frames: solidify-reverse, solidify-system-back-to-kanji and solidify-system-back-to-word. The lower half of the sheet is empty filler.
- **Frame count:** 14 sheets × 6 frames + 3 = 87, which matches the stated number of original screenshots.
  - So the frame numbers missing from individual sheets (for example absorbed-07, -09, -12 and effort-06, -08, -11) are gaps in the capture numbering, not frames left off the sheets.
  - This rests on the sheet totals. I didn't check it against a separate file listing.
- **Solidify-reverse and system-back-to-word:** both return to the lower part of the 凝固 article. The text matches the source and the footer shows JMdict 1239120 and the Digital Daijisen: 凝固 link.
- **System-back-to-kanji:** returns to 凝's Common words and Notes. The metadata line is cut off at the bottom of the screen, which is normal.
- **Glyphs:** no blank characters or tofu boxes. 冫, 隹, 冗, 凹, 凍, 固 and 硬 are distinct.
- **Resolution:** the cut-off blood-example line at the top of the screen is a normal scroll edge. Small kana are only just readable.

TURN17; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\n1-085-font-panel-1.png
**Resource 17 of 24: `n1-085-font-panel-1.png`** (one full read at closer to full resolution than the sheet thumbnails; the tool may still have resized it)

- **Coverage:** each of the four rows (Gothic, Mincho, Textbook and Brush) shows all 24 characters of panel 1: 中 付 冗 冫 冷 准 凍 凝 凹 力 努 固 堅 夢 夫 工 度 心 息 意 懲 気 注 液. I see no blank characters, tofu boxes or missing positions.
- **Lookalikes:**
  - 冫 renders as a two-dot mark in every row and stays distinct.
  - 冷, 准, 凍 and 凝 each show 冫 on the left with clearly different right-hand parts.
  - 冗 and 凹 are unambiguous.
  - 努 is distinct from 怒-like shapes.
- **Typeface differences (not defects):**
  - Mincho and Brush draw 冷 with the alternative form of its right-hand part, which is a normal font-style variant.
  - Textbook uses wider spacing. Its 冫 looks somewhat heavier than its neighbours, which may be a fallback font.
  - The Brush row is a calligraphic style, and every character in it is still identifiable.
  - The pixels can't tell me which font actually supplied each character, and cmap checks wouldn't settle that either.
- **Footer:** the caption repeats the focus set 凝 / 疑 / 准 / 冗 / 凹 and 冫 / 隹, in the default UI font.
- **Resolution:** fine stroke details, such as the inner strokes of 懲 and 凝 in the Brush row, are legible but small.

TURN18; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\n1-085-font-panel-2.png
**Resource 18 of 24: `n1-085-font-panel-2.png`** (one full read; the tool may have resized it)

- **Coverage:** each of the four rows (Gothic, Mincho, Textbook and Brush) shows all 15 characters of panel 2: 濃 点 焦 熱 疑 的 目 硬 肩 血 衣 装 見 隹 集. That makes 39 together with panel 1. I see no blank characters, tofu boxes or missing positions.
- **隹:** in Mincho and Textbook it is visibly heavier, in a Gothic-like style, so it is very likely drawn by a fallback font. In Brush it is less obviously different.
  - It is still the correct, legible 隹, clearly different from 集 and 焦 and from 冫. It is a typeface change, not a blank glyph or a misleading lookalike.
  - The pixels can't tell me which font actually supplied it.
- **疑:** legible in all four rows. Its matrix-like right-hand part is clearly visible, so it doesn't collapse into 凝 or anything else.
- **Other characters:** 硬, 肩 and 装 are distinct.
- **Layout:** in the Textbook row, the wider spacing wraps 集 onto a second line. That is layout only.
- **Resolution:** the inner strokes of 濃 and 疑 in the Brush row are legible but small.

TURN19; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\n1-085-font-panel-3.png
**Resource 19 of 24: `n1-085-font-panel-3.png`** (one full read; the tool may have resized it)

- **Coverage:** each of the four rows (Gothic, Mincho, Textbook and Brush) shows the full focus set 凝 疑 准 冗 凹 冫 隹 凍 固 硬 and the whole words 凝固, 凝る and 凝らす. I see no blank characters, tofu boxes or missing positions.
- **Lookalikes:** all pairs stay distinct in every row.
  - 凝 and 疑: only 凝 has 冫 on the left.
  - 准 and 隹: 准 has 冫 on the left; 隹 stands alone.
  - 冫 renders as a two-dot mark, never as 隹.
  - 冗 and 凹 are different shapes.
  - 凍 and 凝: their right-hand parts are clearly different.
- **Whole words:** 凝固, 凝る and 凝らす render correctly, with kana spacing appropriate to each style.
  - The る and らす endings are clearly kana.
  - The line wraps inside 凝らす (す, or らす in Textbook, drops to the next line). That is a line break in the probe panel only, not a rendering defect.
- **隹:** in the Mincho and Textbook rows it is again visibly heavier, so it is likely drawn by a fallback font. It is still the correct and legible 隹, so this is a typeface change, not a defect. The pixels can't tell me which font supplied it.
- **Resolution:** the inner strokes of 凝 and 疑 in the Brush row are legible but small.

TURN20; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\n1-085-drawing-feedback.png
**Resource 20 of 24: `n1-085-drawing-feedback.png`** (one full read; the tool may have resized it)

- **Header and status:** "凝 congeal; become absorbed", then "Practice only: this attempt is not graded." and "Well drawn!".
- **Drawing panels:**
  - "Your drawing" (blue) shows a well-formed, recognisable 凝 made from the 16 strokes injected by the test.
  - "Correct strokes" (green) is numbered 1–16, which matches the 16-stroke count.
- **Stroke order at this resolution:** the order looks plausible. 冫 takes strokes 1–2, the 匕-like part 3–4, the 矢-like part about 5–9, and the マ/疋-like part about 10–16. The labels overlap in places (for example 8, 12, 15 and 16), so I can't certify every stroke's order or direction from these pixels.
- **Wording:** "Graded by stroke shapes only (handwriting model not available)" appears even though the screen also says the attempt is not graded. That wording is general to the app, not specific to this batch, so I don't count it as a batch finding.
- **Embedded article:** 16 strokes, radical 冫 described as the two-stroke ice radical at left (no. 15), and "N1 (community list)".
  - Meaning and origin links 凝固 and 凝る.
  - The mnemonic is labelled "Modern-shape mnemonic, not etymology" and mentions 冫 beside 疑. It is cut off at the bottom of the screen, which is normal.
- **Glyphs:** no blank characters or tofu boxes. 冫 renders clearly as a two-dot mark.
- **Limits:** this is injected reference input, not human handwriting, ML Kit recognition or phone evidence.

TURN21; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\n1-085-kanji-20.png
**Resource 21 of 24: `n1-085-kanji-20.png`** (one full read; the tool may have resized it)

- **What's shown:** the 凝 readings table scrolled sideways, with the "Scroll sideways to read all columns." hint visible.
- **Left edge:** the Reading column is cut off on the left ("ading", "ョウ", "る", "らす", "ご.らす", "ご.らせる", "ご.る"). The Type column (on, then kun ×5) is fully visible.
- **Typical words column:** fully visible and legible.
  - 凝固 ぎょうこ — coagulation; solidification
  - 凝る こる — become stiff; get absorbed in; be elaborate
  - 凝らす こらす — concentrate; apply effort
  - 凝らす こごらす — cause to congeal; freeze; a separately recorded reading, not the linked article's primary こらす
  - 凝らせる こごらせる — cause to congeal; freeze; written ending らせる
  - 凝る こごる — congeal; jell; usually written in …
  - The first three are linked and the こご rows are not.
- **Assessment:** this is the scrolled position of the same table. The Reading column was confirmed complete in the unscrolled frames, and the last gloss was confirmed complete in kanji-26/27. So the cut-off is signposted table scrolling plus the normal bottom edge of the screen, not lost content.
- **Glyphs:** no blank characters or tofu boxes. ご and the small kana are clear at this resolution.

TURN22; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\n1-085-effort-13.png
**Resource 22 of 24: `n1-085-effort-13.png`** (one full read; the tool may have resized it)

- **What's shown:** the bottom of the 凝らす article, header "凝らす concentrate; apply effort". The end of the article is reached. Every piece of text I could read matches the source.
- **How the kanji combine:** 凝 writes こ and らす is the written ending; it is one native verb.
- **Synonyms:** 集中 and 注ぐ, with the caution that their objects and particles must fit the expression. Then the contrast between 凝る / ゴルフに凝る ("be really into golf") and 工夫を凝らす ("exercise one's ingenuity").
- **Distinctive meaning:**
  - 息を凝らす (いきをこらす) is translated as "hold one's breath", not "stare at one's breath".
  - こごらす is described as a separately recorded reading meaning "cause to congeal; freeze".
  - The article teaches こらす.
  - 凝らせる can be the potential こらせる, while the dictionary verb 凝らせる こごらせる is a different reading.
  - 懲らす (こらす) means "punish; chastise". As before, the article doesn't mention that JMdict flags 懲らす as dated, which stays an optional point only.
- **Footer:** JMdict entries 1239010, 1239000, 1239020, 1309500, 2572530, 2835904 and 1428180, and the Digital Daijisen: 凝らす link.
- **Glyphs:** no blank characters or tofu boxes. 凝 and 懲 are legible, and bold こごらす / こらす / こごらせる render clearly.
- **Spacing:** the earlier small-gap observation from the sheet doesn't appear in this frame.

TURN23; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\n1-085-curated-Kun-feedback.png
**Resource 23 of 24: `n1-085-curated-Kun-feedback.png`** (one full read; the tool may have resized it)

- **Header and prompt:** "Kanji readings" with a large 凝. It is drawn in a heavier, brush-like style, and 冫 plus the 疑-shaped right side are clearly legible. That is a typeface style, not a defect.
- **Feedback:** "Correct! — kun'yomi" with こる highlighted in green.
- **Wrong answers:** こい, こずえ and へこむ. None is a reading of 凝, and nothing ambiguous is offered: こらす is not a separate choice, which fits こる being the only normalized kun key.
- **Reading list:** "congeal; become absorbed: ギョウ、こる、こらす、こごらす、こごらせる、こごる", showing all six readings in source order without the okurigana dots. That is a display style.
- **Buttons:** Next and "I guessed".
- **Embedded article:** 16 strokes, radical 冫 described as the two-stroke ice radical at left (no. 15), "N1 (community list)". Meaning and origin links 凝固 ぎょうこ and 凝る こる. The page is cut off at the bottom of the screen, which is normal.
- **Glyphs:** no blank characters or tofu boxes. The small kana in the reading list are clear.

TURN24; C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-085-native\attempt-596\n1-085-absorbed-14.png
**Resource 24 of 24: `n1-085-absorbed-14.png`** (one full read; the tool may have resized it)

- **What's shown:** the bottom of the 凝る article, header "凝る become stiff; get absorbed". The end of the article is reached, and every piece of text I could read matches the source.
- **Synonyms:** 熱中 and 夢中 overlap in absorption; 集中 focuses on concentration.
- **凝らす note:** 凝らす (こらす) is transitive in 工夫を凝らす "exercise one's ingenuity", with the warning not to swap the に in ゴルフに凝る for を.
- **Distinctive meaning:**
  - 凝る is not the general adjective "hard"; it is contrasted with 硬い (かたい).
  - Getting absorbed in a hobby need not be a problem, and the elaborate-detail use can praise craftsmanship.
  - The primary reading is こる. The separately recorded こごる ("congeal; jell", usually written in kana) and しこる ("stiffen; harden") are covered, with the warning not to read the shoulder and golf examples with them.
  - It notes that Daijisen also records a gathering or cold-solidification sense, and that the three branches are not an exhaustive definition.
- **Footer:** JMdict entries 1239070, 1238990, 1239060, 1594250 and 1636550, and the Digital Daijisen: 凝る link.
- **Screen edge:** the first line at the top is cut off by the scroll position, which is normal.
- **Glyphs:** no blank characters or tofu boxes. 凝, 硬, 熱, 夢 and 集 are legible, and bold こる / こごる / しこる render clearly.
- **Optional point still open:** the Nに凝る "be particular about" example (家のつくりに凝る) is still absent, as noted before.

TURN25; None
# Batch 085: dependent visual confirmation, final report

## Snapshot
- **Evidence HEAD:** 6921ddbd75e93e43974d2e9340f41c7f8848e626, as stated in the host's source packet.
- **Teaching content:** my initial snapshot a7512a5e plus the 努力 exclusion in `words\凝らす.md`. The packet gives that as commit 29a53380, content envelope 1d2e3290 and content version 0c514711ae8d3212.
- **Article hashes in the packet:** 凝 41ea4033…, 凝固 e156f599…, 凝る 14ee1bf1…, revised 凝らす 40d5f79a…, 固 3ec01320…. They match the earlier packets.
- **Build tested:** test-only Android build 1c1b7bf4 on top of unchanged production f9b59a2. This is not the latest app main.
- **Not independently checked:** I verified none of this with Git or upstream sources.

## Scope
- **Model and session:** Claude Opus 5.5 (`claude-opus-5.5`). This is the original session resumed after a context summary, and it is a dependent confirmation, not a new blind review.
- **Reads:** 24 serial `view` calls, one per resource, with `forceReadLargeFiles=true` and no `view_range`. There were no denials, shell, edits, delegation, parallel calls or unassigned reads.
  - **Source packet:** read in full, with no truncation marker.
  - **15 sheets:** 14 × 6 + 3 = 87 frames, matching the stated 87 originals. I didn't compare this against a separate file listing.
  - **8 focused originals:** font panels 1–3, drawing-feedback, kanji-20, effort-13, curated-Kun-feedback and absorbed-14.
- **Image resolution:** the sheets are thumbnails, and the tool may have resized every image again. So this was 87 frames at reduced resolution plus 8 originals at closer to full resolution, not 87 full-resolution reads. Small kana, link underlines, labels where stroke numbers overlap, and fine Brush-style strokes were only just readable.

## Verdicts
CLEAN means no actionable defect was established in what I observed for this scope. It is not exhaustive certification. "Comprehensibility" here means the rendered text reads clearly on the emulator; it is not native-speaker certification.

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\凝.md` | CLEAN | CLEAN | CLEAN |
| `words\凝固.md` | CLEAN | CLEAN | CLEAN |
| `words\凝る.md` | CLEAN | CLEAN | CLEAN |
| `words\凝らす.md` | CLEAN | CLEAN | CLEAN |

- **Changed 固 Common words bullet:** CLEAN.
  - I saw it rendered fresh in solid-back-to-reused-kanji and solid-changed-bullet: "凝固 ぎょうこ — coagulation; solidification". The link resolves and the reading and gloss are correct.
  - The rest of 固 was not reviewed fresh; it is unchanged baseline content.

## Findings
**Proved defects: none new.**

**Earlier finding (not new):** the 凝らす/努力 quiz exclusion.
- Minor; quiz coverage; `words\凝らす.md:4,8`.
- **Resolved** by my textual confirmation, high confidence.
- This visual run shows no regression, but it doesn't directly show the exclusion working, because no 努力 choice appears in any captured quiz.

**What the pixels support:**
- **Rendered text:** the Japanese, kana, examples and English translations all match the source in every article. None of the cut-off text I saw was lost content; it was screen edges or table scrolling.
- **Readings table:**
  - The "Scroll sideways" hint is always shown.
  - Between the unscrolled and scrolled frames, every cell can be read. kanji-26 and -27 show the end of the こご.る cell ("usually written in kana as こごる").
- **Glyphs:**
  - All 39 Han characters appear in all four font families. There are no blank glyphs or tofu boxes.
  - The lookalikes stay distinct: 凝/疑, 准/隹, 冫 versus 隹, 冗/凹, 凍/凝, 固/硬.
  - The whole words 凝固, 凝る and 凝らす render correctly.
  - In Mincho and Textbook, 隹 looks heavier, which suggests a fallback font. That is a typeface change only, and I can't tell from pixels which font supplied it.
- **Meaning quiz:** the choices are congeal; become absorbed / quasi-; associate rank / superfluous; redundant / concave; sunken, with no padding choices.
- **Reading quizzes:**
  - On'yomi: ギョウ against ジュン / オウ / ジョウ.
  - Kun'yomi: こる against こい / こずえ / へこむ. こらす is not offered as a separate answer.
  - The feedback screens show all six readings. The done screen shows 2 of 2 correct.
- **Selection screen:** "N1 · 117 cards"; readings 2 due, meaning 1 due, drawing 1 new.
- **Drawing:**
  - Trace stage, then feedback ("not graded", "Well drawn!"), then recall give-up ("Here is the kanji"), with 16 numbered strokes.
  - "Handwriting model not available" is consistent with the run being offline.
- **Navigation:** forward, reverse and system-back work for all three words.

## Optional
These are unchanged from my earlier reports; none is required:
- `凝る.md:23`: the "despite ending in る" wording.
- `凝る.md`: an Nに凝る example for "be particular about", such as 家のつくりに凝る. It is still absent in the rendered article.
- `凝らす.md:51`: JMdict flags 懲らす as "dated"; the article doesn't say so.
- `凝らす.md:49`: 凝らせる is also the causative of こる.
- `凝固.md:41`: repeats the "not ice" point from line 22.
- `固.md:40`: uses an em dash where its neighbours use " - ". The rendered app confirms this; it is cosmetic.

One new cosmetic observation:
- **Possible spacing gap:** before "（くふうをこらす）" in the Meaning section of 凝らす, seen only on sheet 5 thumbnails.
- **Correction:** in my resource-22 note I said the gap doesn't appear in effort-13. That frame doesn't contain the sentence at all, so the gap remains unverified at full resolution.
- **Unrelated to this batch:** the drawing screen says both "not graded" and "Graded by stroke shapes only". That wording is shared across the app, so it is not a batch finding.

## Limits
**My earlier unknowns:**

| Unknown | Status | Basis |
|---|---|---|
| Font and glyph rendering | Partially resolved | Emulator pixels only; the fallback font is not identified; the 40 historical fallback characters were inherited, not re-inspected |
| Default four-choice quiz exposure | Resolved for the default pools | Pixels plus packet route data |
| Regenerated manifest | Partially resolved | Content import is consistent with the packet's single import and zero problems; I never saw the manifest itself |
| Quiz safety in larger or random pools | Unresolved | Words such as 専念 and 頑張る, and complete families, were not checked |
| Drawing | Partially resolved | Injected reference strokes only; no human handwriting or ML Kit |
| Stroke order and direction | Not certified | Labels overlap at this resolution |

**Outstanding gates, separate from the above:**
- physical phone, general release, current-main integration, publication, CI and immutable ZIP;
- whole-set coverage and owner progress;
- native-speaker review and corpus checks;
- measured learning effectiveness.
