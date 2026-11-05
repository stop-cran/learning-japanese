In drawing-recall-feedback, "Your drawing" is empty and the screen shows "Here is the kanji" in red. In the Correct strokes panel, "7" sits inside the 口 enclosure above stroke 5, and "6" sits beside the top of 乚 rather than 丿. This is the most misleading of the three label layouts.

**Snapshot:** Evidence HEAD 27813d5, with teaching files unchanged from c8c2a0b and envelope 5d32234 (confirmed in the route JSON). Git verification was not possible because the task allowed only `view`.

**Correction:** My earlier visual report wrongly claimed it used "one view call at a time." That pass actually made one parallel group of 7 reads (5 fixture ranges plus 2 receipts) and one parallel group of 18 PNG views. This repair redid all of those reads one at a time, each followed by an observation.

**Scope:** In this repair, Claude Opus 5.5 read:
- `N1Batch073NativeTest.kt` ranges [1,120], [121,240], [241,360], [361,480] and [481,521];
- `instrumentation.txt` (OK, 2 tests, 82.165 s);
- `n1-073-article-route.json` (passed, offline, phoneEvidence false, archiveRequests 1);
- 18 PNGs: font-pairs, kanji-01, -03, -09, -11, -17, word-reused-07, clothing-reused-03, word-kanji-backlink, selection, meaning-question, meaning-feedback, curated-On-question, curated-On-feedback, curated-on-only-done, drawing-trace, drawing-feedback and drawing-recall-feedback.

The twelve duplicate captures were not viewed.

**Verdicts:**
- `克.md` (whole card): correctness CLEAN, scoped coverage CLEAN, comprehensibility CLEAN.
- `克服.md` line 24: correctness CLEAN, scoped coverage CLEAN, comprehensibility CLEAN.
- `服.md` line 21: correctness CLEAN, scoped coverage CLEAN, comprehensibility CLEAN.

**Findings:** None.

**Optional:**
1. **Stroke-number labels (reassessed, app-side polish, not a content defect).** The new pixels confirm and sharpen the earlier hypothesis.
   - drawing-trace: "6" lies between the tops of 丿 and 乚, and "7" sits above stroke 5, away from 乚.
   - drawing-recall-feedback: "7" sits inside the 口 enclosure and "6" sits beside 乚, which is the most misleading layout.
   - drawing-feedback: the labels are crowded but readable.
   - Confidence is moderate. This is a placement heuristic in the app, not a stroke-data error: the fixture injected all 7 reference strokes.
2. Carried over from the original report:
   - **兄 contrast note:** the note could add that 克 is a 十 above a 兄-like shape.
   - **克明:** a brief mention of 克明 (こくめい).
3. **Fallback meaning distractors:** the quiz showed chrysanthemum / strange; extraordinary / vertebra; chinquapin, not the authored 古/兄/元. These come from the app, not the content.

**Limits:**
- **Readings table:** the right column is clipped until scrolled sideways (kanji-01/-03/-09). kanji-11 shows it complete after sideways scrolling, so this is not a content defect.
- **Textbook typeface:** the standalone 儿 renders in an unidentified fallback typeface.
- **Device:** evidence comes from an API 35 emulator only. There was no physical phone, ML Kit recognition ("handwriting model not available"), or human handwriting or recall.
- **Inherited from the original report:**
  - There is a tension between Nikkoku's enemy-subjugation sense of 克服 and the unchanged 克服.md:32.
  - The Kotobank pages were truncated.
  - There was no baseline diff.
  - The N1 snapshot JSON was not read.
