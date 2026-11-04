## Review of batch 035 (鹿) at 7dc5640

I found one minor wording problem, in the 鹿 kanji card. The new 鹿 word article and the link added to 馬鹿 have no actionable defects. I made no edits.

**Process note:** In step 1 I opened two instruction files at the same time (`content-structure.instructions.md` and `content-format.md`), which broke your one-tool-call rule. Every other read was done one at a time.

**Snapshot:** `7dc564035f254a380f481acd06fd7118ff748383`. I did not inspect uncommitted changes, as instructed.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), working alone and without seeing other reviews.
- **Teaching files read in full:** `kanji\鹿.md` (64 lines), `words\鹿.md` (46 lines) and `words\馬鹿.md` (38 lines). For 馬鹿, only the added link around 鹿 at line 26 was judged; the rest was context.
- **Instructions:** all assigned ranges.
- **Source data:**
  - All of `batch-035-input-metadata.json`, including the raw KANJIDIC2 entries for 鹿, 麓, 麗 and 鏡.
  - All three dictionary (JMdict) packets, every line, in ranges of 200 lines or fewer: 4079, 265 and 381 lines.
- **Comparison cards:** 席, 庭, 底, 馬, 動物, 山 and 見る.
- **`confusable-words.md`:** a targeted search only.
- **Supplied Weblio (Digital Daijisen) text:** lines 1770–1820, then 1821–1878.
- **Checked:** correctness, scoped coverage and how readable the text is on a phone screen.

**Verdicts:**
- `kanji\鹿.md`: correctness **NEEDS FIX** (minor); scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- `words\鹿.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- `words\馬鹿.md` (added link only): correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

**Findings:**
1. **Minor; correctness / qualified claims; `kanji\鹿.md`:47–49 and 56–57.**
   - **Claim:** 馬鹿 is "not a deer compound whose meaning **or reading** can be worked out character by character". The Notes add that 馬鹿 is not "evidence that 鹿 independently supplies か".
   - **Problem:** JMdict marks 馬鹿 as a sound-based spelling ("ateji (phonetic) reading"). The characters were chosen for their sounds: バ (from 馬) + か, which is a sourced reading of 鹿. So it is the *meaning* that can't be worked out from the parts. The *sound* can. The wording overstates this, and a learner may decide 鹿 has nothing to do with か in 馬鹿.
   - **Fix:** Say the meaning "fool" doesn't come from horse + deer, and the spelling uses the characters for their sounds (ば + か). Keep the advice to learn the whole word and to not treat it as a deer word or as support for the か reading row.
   - **Evidence:**
     - JMdict 1601260: 馬鹿 is marked "ateji (phonetic) reading".
     - KANJIDIC2: 鹿 has the kun reading か.
     - JMdict 2873068: 鹿/か means deer (archaic).
     - `words\馬鹿.md`:26 already words this correctly: "Do not derive 'fool' by combining the animals' meanings".
   - **Confidence:** medium. The card avoiding 馬鹿 as support for the か reading is a reasonable choice; only the "or reading" wording is the problem.

**Checked and found correct:**
- **Readings and metadata:** ロク; しか, か; 11 strokes; radical 198; grade 4 all match KANJIDIC2, in source order. Only しか is used in reading quizzes (`quizOnyomi: []`, `quizKunyomi: [しか]`). The しか row links to the 鹿 word article.
- **Archaic か:** JMdict 2873068 and Daijisen ("シカの古名") both support か as an old word for deer.
- **神鹿 / しんろく:** matches JMdict 2663000. It is correctly labelled as something to recognise.
- **鹿の子:** all four JMdict 1866430 senses are handled accurately, including the archaic "fawn" sense.
- **Word article meaning:** "deer generally, especially sika deer" matches JMdict 1319030 (its single sense, "cervid" included) and Daijisen ㋐/㋑.
- **Example sentences:** both are natural. The notes on で, を and いる are correct.
- **Links and memory aid:** both two-way link pairs are present. The memory aid is clearly labelled as one, and the card correctly says the radical is the whole 鹿, not the 广 shape.
- **Quiz answers:**
  - The comparison cards' titles ("seat; place", "garden; yard", "bottom; base") can't be mistaken for "deer".
  - Nothing else in `kanji\` or `words\` has the title "deer".
  - Excluding 鹿 and 動物 from the same quiz is justified, since "animal" would also be a reasonable answer for 鹿.
  - 鹿 and 馬 need no exclusion.

**Optional:**
- Daijisen says that in older usage しか meant the male and めか the female. The modern "does not specify sex" statement is correct; a one-line historical note is optional.
- Daijisen's example for the か reading is 鹿毛 (かげ, a fawn/bay coat colour, JMdict 2077830). It would be a useful second example in that row.
- The words article could mention that the katakana シカ is the common spelling in biology and that it has its own JMdict reading entry.
- The readings しし and かのしし (Daijisen and JMdict) are not KANJIDIC2 on/kun readings, so leaving them out is fine.

**Limits:**
- **Evidence:** I used only the supplied frozen dictionary packets and Weblio text. I did no fresh lookups online or from the original dictionary files.
- **Other files:** I searched `confusable-words.md` only for 鹿 and 動物, not the whole file.
- **Device testing:** this was a text-only review. I did not check how characters render on Android or on a real phone. Fresh Android, combined-main, CI and public ZIP checks are still pending. Physical-phone and general-release acceptance remain outstanding.
- **Records and history:** I did not read the author's records or other reviews. I judged only the final text of the 馬鹿 link, not the diff.
