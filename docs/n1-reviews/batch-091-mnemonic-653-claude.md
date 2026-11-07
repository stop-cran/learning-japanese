**Snapshot:** Frozen signed HEAD 1cfd5bd36e707ee78ba4401e48ffba9815854d58. The only teaching change is the 刃 kanji mnemonic paragraph; the diff also regenerates the manifest (`contentVersion` cb3c857f3614485d → bfe65483a821fc13, plus the `kanji/刃.md` entry). The new version bfe65483a821fc13 has not been imported or rendered on a device. This is a dependent confirmation, not a new blind review.

**Scope:**
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`), session 075924f2-f60b-4ae0-bf3f-341db3dfbd74, working alone.
- **Reads:** six resources, read in full, one `view` call per response, each after the previous result:
  1. My earlier visual report, `batch-091-visual-651-claude.md`.
  2. The correction diff, `batch-091-mnemonic-correction-652.diff`.
  3. The current `kanji/刃.md`.
  4. `n1-091-font-panel-3.png` (original).
  5. `n1-091-meaning-question.png` (original).
  6. `n1-091-drawing-trace.png` (original).
- **Not reread:** dictionaries, `words/刃.md` or other articles.
- **Process history:** My earlier visual follow-up batched its image views, so it remains rejected as serial-process evidence. This confirmation was done serially.

**Verdicts:**
- **`kanji/刃.md`, changed paragraph (line 24):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN (previously NEEDS FIX).
- **`kanji/刃.md`, rest of the article:** my earlier text conclusions carry over. Compared with the earlier article, the diff touches only line 24. The frontmatter, reading table and its order, quiz settings, links, notes and metadata line are unchanged.
- **`words/刃.md`:** carried over unchanged (correctness, scoped coverage and comprehensibility all CLEAN). It is not in this diff.

**What the original images show about the new wording:**
- **Default Gothic** (`n1-091-meaning-question.png` and the Gothic row of font panel 3): the short mark is a detached stroke left of the long sweep. "Some fonts show it as a separate stroke" is accurate.
- **Pinned stroke diagram** (`n1-091-drawing-trace.png`): stroke 3 crosses the longer sloping stroke 2. "The stroke-order diagram here shows it crossing the longer sloping stroke" is accurate.
- **Other fonts** (Mincho, Textbook and Brush rows of panel 3): the mark crosses the sweep, consistent with the diagram. The wording does not claim that every font except one detaches the mark.
- **No overclaim:** the paragraph still says "Modern-shape mnemonic, not etymology" and "not a historical explanation". It makes no claim about the history or direction of the stroke.
- **Regression:** none. The old shape claim ("shaped like 丶") was removed and nothing inaccurate replaced it. The original images establish that the new description is accurate for these rendered shapes, but they show the old content version, not the revised text layout.

**Findings:** None.

**Reconciliation of my earlier findings:**
- **Visual Finding 1 (mnemonic did not match the Gothic rendering):** **resolved** in the text. Whether the revised text displays correctly on a device has not been tested; that is not an article defect in itself.
- **Earlier text findings:** 先端 exclusion and figurative "cutting edge" note: stay **resolved**. 刃傷 gloss: stays **resolved**.
- **Hypothesis:** 刃/ナイフ: stays **unresolved but not actionable**.
- **Optional notes:** all **optional** and unchanged (the "のはは" kana parsing, the 歯 "tooth" homophone, the 刄 variant, more ジン words, き.る shown as "きる" in quiz feedback).
- **Limits:**
  - **Visual evidence:** stays **partially resolved** (emulator captures only, and none for the revised version).
  - **Fallback choices:** zero-fallback stays **resolved only for the tested N1 setup**; "All" stays receipt-only.

**Optional:**
- **"Separate" vs "detached":** in a stroke-count sense the mark is always a separate stroke. "Detached" or "standing apart from the sweep" would be more exact.
- **Direction:** the text does not mention that the Gothic mark slants down-left while the diagram's mark runs down-right. Leaving it out is not inaccurate.
- **"Here":** "the stroke-order diagram here" assumes the app's drawing view; if the article is read outside the app, "the app's stroke-order diagram" would be clearer.

**Limits:**
- **Revised version not rendered:** bfe65483a821fc13 has not been imported or rendered natively. The old screenshots (cb3c857f3614485d) support shape comparison only, not the revised text layout.
- **Native-run receipts:** these come from the coordinator, are inherited and are not my tests:
  - Two passing native test cases with no skips.
  - ContentSync run once from full archive f6b2ee39.
  - 1,114 kanji, 5,070 words, 123 N1 cards, zero problems, Room reading-parser epoch 1.
- **Device and build:** API 35 emulator and test-only Android build 1c1b7bf4, which retains production f9b59a2. The actual fallback font face is unidentified.
- **Drawing:** the trace was injected, not human handwriting, and the handwriting model did not run successfully.
- **Manifest hashes:** they differ from the raw file hashes (LF normalization is the coordinator's claim); I did not verify this independently.
- **No independent verification:** no Git or upstream retrieval.
- **Not certified here:** phone acceptance, general release, the whole N1 set, current main, CI and the public ZIP. Learning effectiveness was not measured.
