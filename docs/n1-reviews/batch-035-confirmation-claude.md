I confirm the batch 035 fix: my one finding is resolved, and the revised snapshot has no remaining actionable defects. I made no edits. I'm also withdrawing part of the fix I originally suggested (details below).

**Snapshot:** revised `7c879289156ce0988b1355cbae16d9ad9b155f69` (compared against initial `7dc564035f254a380f481acd06fd7118ff748383`). No uncommitted teaching was included. I did not check the commit signature.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), in the same session that wrote the initial review. I did not read the other review or the author's records.
- **Read fresh, one call at a time:**
  - this confirmation prompt;
  - my original report, `docs\n1-reviews\batch-035-initial-claude.md`;
  - all of the revised `kanji\鹿.md` (64 lines);
  - all of `words\馬鹿.md` (38 lines);
  - `docs\n1-sources\batch-035-core-jmdict.xml` lines 50–145 (the 馬鹿 dictionary entry, 1601260).
- **Inherited from the initial review, not re-read:** `words\鹿.md`, the comparison cards, the KANJIDIC2 metadata, the other dictionary packets, the supplied Weblio text and the instruction files. You stated these are unchanged.
- **Facets checked:** correctness, scoped coverage and comprehensibility, mainly in the changed passage and anywhere it could cause a regression.

**Verdicts:**
- **`kanji\鹿.md`:** correctness **CLEAN** (was NEEDS FIX); scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- **`words\鹿.md`:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**. This is inherited: the file is unchanged and I did not re-read it.
- **`words\馬鹿.md` (the 鹿 link only):** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**. I re-read the file and it is unchanged.

**Findings:**
1. **Original Minor finding (`kanji\鹿.md`:47–49, 56–57): resolved.**
   - **What changed:** The card no longer says 馬鹿 can't be worked out character by character "in meaning or reading". Lines 47–49 now say only that 馬鹿 is a whole-word **ateji** (sound-based spelling) and that its meaning doesn't come from combining horse and deer.
   - **Why that's right:** this matches JMdict 1601260, which marks 馬鹿 as "ateji (phonetic) reading" and gives no gloss suggesting a horse + deer meaning. It also matches `words\馬鹿.md`:26 ("Do not derive 'fool' by combining the animals' meanings").
   - **Notes, lines 56–57:** "Do not use 馬鹿 ばか as evidence that 鹿 independently supplies か in that word" is acceptable.
     - It warns against using this one word as evidence for the か reading. It doesn't say a known か reading can't take part in the sound-based spelling.
     - The か reading row keeps its own support: KANJIDIC2, JMdict 2873068 and Daijisen.
   - **Part withdrawn:** my original suggestion to state that the spelling works as バ + か. The ateji label and the separately documented か reading don't establish how each character supplied the sound. The entry also lists other spellings (莫迦 as ateji; 破家, 馬稼 and 罵迦 as search-only forms). Leaving out that breakdown is correct and leaves nothing missing.
   - **No regressions:** the edited wording reads clearly on its own, the list item's continuation lines are intact, and the change adds no claim about origin or how the characters supply the sound.
   - **Confidence:** high.

**Optional:**
- "Learn its complete spelling and reading together" now appears at both line 49 and line 57. This is harmless repetition and can stay.
- My earlier optional suggestions (the historical male/female note, 鹿毛 かげ as a second か example, and the katakana シカ spelling) are still optional and not required.

**Limits:**
- **Dictionary range:** the assigned range starts on the first spelling line, so it doesn't show the line with the entry number. I identified it as 1601260 from my initial full read of the lexical packet, where the content is identical.
- **Not re-read:** the other dictionary packets, the Weblio text and the unchanged files.
- **Diff and manifest:** I didn't independently confirm the diff or manifest regeneration beyond reading the current text, which matches the diff you gave.
- **Device testing:** this was a text-only review. I didn't check how characters render on Android or on a real phone. Fresh Android, combined-main, CI and public ZIP checks are still pending, as are physical-phone and general-release acceptance.
- **Process:** I didn't run any tools in parallel in this confirmation. The initial review disclosed one accidental parallel read during step 1, when it read the instruction files.
