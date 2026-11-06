**Snapshot:** I was given `75fbfc7dc734c7ff5d9771fbd5103afd3f3fdc1c`. I couldn't check this independently because shell and Git weren't available, so I can't confirm the working-tree state or compare against the earlier version. I made no teaching edits.

**Scope:** Reviewed by Claude Opus 5.5 (`claude-opus-5.5`).
- **Files read:** every assigned range, in full: 免, 許, 税, 兄, 元, 先, 逃, 放 and 允 kanji cards; 免れる, 免許, 免税, 助かる, 逃げる, 避ける, 救う, 救助 and 生存 word articles; the JMdict file (lines 1–3237, 27 chunks); the KANJIDIC2 file (lines 1–588, all 8 records); `strokes/免.json`; the KanjiVG SVG; the guidance files.
- **Targeted searches:** the confusable-words guide (no entries for these words), word titles that overlap in meaning, distractor lists that name 免, and the 勉/晩 cards' titles.
- **Public sources fetched live:** Kotobank 免れる (Nikkoku entry, plus the Daijisen body from the raw HTML at offset 65000), Kotobank 免 (Daijisen, Nikkoku and encyclopedias), and kanjiapi.dev/v1/kanji/免.
- **Line numbers:** the 免 link in 免許 is at line **25**, not 24. 免税 line 26 and 許 line 38 match their labels.

**Verdicts** (correctness / scoped coverage / comprehensibility)
- **New 免:** CLEAN / CLEAN / CLEAN
  - Metadata matches KANJIDIC2 and kanjiapi: 8 strokes, radical 儿 (no. 10), grade 8, JLPT 1, readings in the original order.
  - All three readings have their own rows. The two quiz selections have linked examples.
  - The mnemonic is clearly labelled as invented, and the stroke file has 8 strokes matching the SVG.
  - 兄, 元 and 先 are suitable wrong answers.
- **New 免れる:** CLEAN / CLEAN / CLEAN
  - JMdict 1584670 lists まぬがれる (with frequency flags) and まぬかれる (none), both senses ichidan and transitive.
  - Nikkoku labels the verb intransitive; Daijisen notes「まぬかれる」とも and gives 責任を―・れる and 戦火を―・れる.
  - The を construction, the verb forms and the explanation that れる is not a passive ending are all correct.
  - The three quiz exclusions are justified (助かる's sense 2 is "to escape harm"). 救う, 救助 and 生存 rightly stay unexcluded.
  - It has no inferred vocabulary level.
- **Changed 免許 link (line 25):** CLEAN / CLEAN / CLEAN
- **Changed 免税 link (line 26):** CLEAN / CLEAN / CLEAN
- **Changed 許 example (line 38):** CLEAN / CLEAN / CLEAN

All ten required links (both directions for five pairs) are present, with the correct readings めんきょ and めんぜい.

**Findings:** None.

**Optional:**
- The source line at `kanji/許.md:49` doesn't list JMdict 1533130 for the newly added 免許. By contrast, 税.md lists 1533230 for 免税.
- The 免 card could note that the 勉 and 晩 cards contain the 免 shape. Both cards already mention it in plain text.
- The dismissal sense on the 免 card has no example. 免職 めんしょく or 罷免 ひめん would work, and ごめん (御免, usually written in kana) could help recognition.
- The 免れる article could mention the common negative pattern 謗りを免れない "unable to escape criticism" (JMdict 2837307).

**Limits:**
- **Process:** I broke the strict serial rule once by reading 兄 and 元 in a single parallel call. All other calls were serial.
- **Sources:** I didn't use the cached HTML. The Jitsu body for 免 wasn't returned, but the card makes no origin claims, so this doesn't affect the review.
- **Not freshly checked:**
  - 免許's unchanged sentence about what each character contributes.
  - 許's existing もと reading, which has no row; it is unchanged and out of scope.
  - Earlier-version JLPT levels, exclusions and distractors.
- **Quiz pools:** larger or random choice pools are unverified. One untested possibility: a fallback could pick 逃 ("escape; flee", which shares 免's tags), and that title partly overlaps the meaning of 免れる.
- **Not done:** device testing on Android f9b59a2 or later, native-speaker, drawing, rendering and physical-phone checks. This review covers phone text only.
