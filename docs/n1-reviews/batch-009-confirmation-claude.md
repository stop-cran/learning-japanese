No regressions found. The correction is supported, and both revised 杏 files stay CLEAN on all three facets. My initial report had no 杏 finding, so this confirms the change rather than claiming I found a defect earlier.

**Snapshot:** Revised snapshot 8534b8989d7a0aeaff80f5ed55eeb6c2683cc642, committed teaching only; original snapshot 09e480adadc433f54cdbe20e3691ab38126bb711. I did not run Git, so both commits are the ones given in the task.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), the same session as the initial review. This is a bounded check of the changed passages, not a new blind review. I made one tool call per response and saw no overlapping calls.
- **Read fresh in full:**
  - my original report, `docs\n1-reviews\batch-009-initial-claude.md`
  - `control\batch-009-correction.diff`
  - revised `kanji\杏.md` and `words\杏.md`
  - `docs\n1-sources\batch-009-origin-evidence.json` (a coordinator paraphrase, used only as a pointer)
- **Fetched fresh:** the Kotobank 杏子 page (Seisenban あん‐ず【杏子・杏】).
- **Inherited from the initial review, not reread:** both 李 files, the KANJIDIC2/JMdict packets, the comparison cards and articles, and the format docs.
- **What changed:** the 杏 card's first Note and source line; the 杏 word article's type and tag (wago to kango), one new origin paragraph and its source line; and the manifest hashes.

**Verdicts:**
- `kanji\杏.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\杏.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `kanji\李.md` and `words\李.md`: the initial CLEAN verdicts for all three facets are carried over. The diff shows no change to either file.

**Findings:**
1. **Lexical-origin correction: supported, no regressions (confidence: high).**
   - **Source:** The Seisenban 【杏子・杏】 entry says 「あん」「す」はそれぞれ「杏」「子」の唐宋音. In other words, the あん and す of あんず are later Chinese-derived readings of 杏 and 子. Its 語誌 (word-history) section says the borrowed fruit name spread to the tree and flowers.
   - **What this supports:**
     - replacing "native noun" with "standalone plant noun";
     - classifying the word as kango;
     - stating that KANJIDIC2's kun label for the character does not settle whether the word is native.
   - **What stayed the same:** KANJIDIC2 still lists あんず as kun, so the card keeps its kun reading row, quiz selection, full reading list and order. The new text doesn't invent a reading for 子 and doesn't claim every kun-reading word is native.
   - **No contradiction with the existing warning:** the article already tells learners not to treat ず as a reusable reading of 子, and the new text fits with it.
   - **Unchanged:** examples, translations, title, quiz exclusions and level. 梅 was not reopened.
   - I found no remaining "native" wording about 杏 in either revised file.

**Optional:** Both earlier optional notes still apply and are unchanged:
- the "plum blossoms" translation in the 李 files;
- the unqualified "almond jelly" for 杏仁豆腐 in `kanji\杏.md`.

New optional note: Seisenban gives the unvoiced す for 子. The word article could say the second syllable is voiced to ず in あんず. The current "Chinese-derived readings of 杏子" is not wrong.

**Limits:**
- **Kotobank:** The Seisenban entry and its 語誌 section came through in full. The Daijisen and other panels on that page showed only headings. I did not fetch the Nipponica あんず page myself; I know its lexical-history paragraph only from the coordinator paraphrase.
- **Not run:** `validate.py` and the manifest check (no shell). The manifest hashes appear in the diff but I did not recompute them.
- **Not checked:** whether the change from wago to kango affects how the app picks quiz choices.
- **Text-only:** no phone, native-speaker, frequency or learning-effectiveness evidence.
