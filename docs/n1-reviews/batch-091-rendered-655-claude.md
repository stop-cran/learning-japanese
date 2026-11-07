**Snapshot:** Frozen signed HEAD 4d6ea7640109a90a510d94083480b7c33c6e7ab2. You report no uncommitted changes; I did not check Git. The teaching content is unchanged since my 653 confirmation of 1cfd5bd. The screenshot is from native run 654 and shows the current content version, bfe65483a821fc13. This is a dependent confirmation, not a new blind review.

**Scope:**
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`), session 075924f2-f60b-4ae0-bf3f-341db3dfbd74, working alone.
- **Reads:** three resources, each read in full with one `view` call per response, each after the previous result:
  1. My earlier report, `batch-091-mnemonic-653-claude.md`.
  2. The current `kanji/刃.md` (50 lines).
  3. The original capture `execution-654\n1-091-kanji-04.png`, viewed directly. The decoded image looks portrait-shaped; I did not measure its pixel size.
- **Not reread:** dictionaries, `words/刃.md`, other images or other reports.

**Verdicts:**
- **`kanji/刃.md`, changed mnemonic paragraph (line 24):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN. Comprehensibility is now confirmed on the device for this screenshot.
- **Rest of `kanji/刃.md`:** carried over from my earlier text reports, not checked again. The file still matches the version I confirmed in 653.
- **`words/刃.md`:** unchanged and carried over (all three facets CLEAN). It was not reread.

**What the screenshot shows:**
- **Paragraph matches the article:** the paragraph appears in full under "Meaning and origin", after the opening paragraph and before "Readings". Its wording matches line 24 exactly:
  - the bold label "Modern-shape mnemonic, not etymology:";
  - the 刀 link with "sword; blade";
  - "Some fonts show it as a separate stroke";
  - "the stroke-order diagram here shows it crossing the longer sloping stroke";
  - the closing statement "…not a historical explanation."
- **Layout:**
  - The paragraph wraps over eight lines with nothing cut off or overlapping.
  - The heading 刃 and the inline 刀 link both render.
  - The bold label stands on its own line.
- **Regression:** none in this paragraph or the parts of the article around it.
  - The opening paragraph and the "Readings" heading appear intact.
  - The reading table is cut off on the right but shows the "Scroll sideways to read all columns." hint. That is the expected horizontal-scroll layout, not part of the change.
- **Glyph shape:** the 刃 in the heading and opening paragraph uses the default Gothic shape, with the short mark separate. This fits "Some fonts show it as a separate stroke". The diagram's crossing stroke comes from the 650 drawing capture and is not shown here.

**Findings:** None.

**Reconciliation:**
- **Limitation "revised version not rendered" (from my 653 report):** **partially resolved**. The changed paragraph has now rendered natively in content version bfe65483a821fc13, in this one emulator screenshot. That does not cover other screens, the other 46 captures I did not view, other font selections, text sizes or a physical phone.
- **Visual Finding 1 (mnemonic did not match the Gothic rendering):** stays **resolved**, now with confirmation on the device.
- **Unchanged earlier items:**
  - The 先端 and 刃傷 findings stay resolved.
  - The 刃/ナイフ hypothesis stays unresolved and not actionable.
  - The fallback-choices limit stays resolved only for the tested N1 setup.
- **Optional notes:** they stay as written earlier; I do not now count them as agreement or as defects.
  - From earlier reviews: "のはは", the 歯 homophone, the 刄 variant, more ジン words, and き.る shown as "きる".
  - From 653: "separate" vs "detached", the direction of the mark, and "here".

**Optional:** None new. The 653 suggestion still applies: "detached" or "standing apart" would be more exact than "separate stroke".

**Limits:**
- **Native-run receipts (coordinator's, not my tests):**
  - Run 654 imported full archive fe3ec10b once through the production ContentSync.
  - 1,114 kanji, 5,070 words, 123 N1, zero problems, Room epoch 1.
  - One ArticleTest case passed with no skips.
- **Fonts:** GlyphTest was not rerun, so the 650 font evidence and its limits still apply. The fallback font face is unidentified, and no Paint-probe PNGs were viewed.
- **Device and build:** test-only Android 1c1b7bf4, which retains production f9b59a2 and is not the latest app main. This is an API 35 emulator, not a phone, and no native speaker reviewed it.
- **Drawing:** the trace was injected, not human handwriting, and the handwriting model never ran successfully.
- **No independent verification:** no Git, upstream or hash checks of my own. Hashes are not viewing evidence.
- **Process:** my 651 follow-up batched its image views and remains rejected. This follow-up was done serially.
- **Outside scope:** current main, combined checks, CI, the public ZIP, publication, phone acceptance, general release and the whole N1 set. Learning effectiveness was not measured.
