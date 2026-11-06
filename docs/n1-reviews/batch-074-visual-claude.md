I found no defects: all five teaching items are CLEAN, the screenshots show nothing that changes my earlier conclusions, and I made no edits.

Snapshot: evidence HEAD `564561b6…`; teaching files unchanged from `75fbfc7…`; content envelope `4078c7d4…` (content version `c507eceeb764bc3f`). No uncommitted changes included.

Scope: Claude Opus 5.5, serial reads only.
- **Text read:** the task file, both of my earlier reports, 免.md and 免れる.md in full, 免許 line 25, 免税 line 26 and 許 line 38.
- **Fixture and results:** the native test file (all 595 lines), the test-run log and the route results file.
- **Images (32, one at a time):** curated-both-done, curated-Kun-feedback, curated-Kun-question, curated-On-feedback, curated-On-question, drawing-feedback, drawing-recall-feedback, drawing-trace, font-pairs, kanji-01, 03, 09, 11 and 20, meaning-feedback, meaning-question, permit-example-18, selection, 免れる-02, 07, 09 and 12, 免税-07, 免税-kanji-backlink, 免税-system-back-to-component, 免税-system-back-to-kanji, 免許-07, 免許-component-backlink, 免許-kanji-backlink, 免許-system-back-from-component, 免許-system-back-to-component, 免許-system-back-to-kanji.
- **Not viewed:** the other 25 PNGs, which the task lists as hash-mapped duplicates.

Verdicts (correctness / coverage / comprehensibility; lexical conclusions carried over from my earlier reviews, kept separate from what the screenshots show):
- **免 (whole card):** CLEAN / CLEAN / CLEAN.
  - The meaning text, the dismissal sense and the qualified memory aid are all legible.
  - The readings table is complete when scrolled sideways, including the note that both まぬかれる and まぬがれる are valid.
  - Notes on 兄/元/先, 許 and 逃 are visible, and the source line is fully visible.
- **免れる (whole card):** CLEAN / CLEAN / CLEAN.
  - The を examples, the ichidan verb forms, the note that れる is not passive, the synonym paragraphs and the transitivity qualification are all legible.
  - Its source link is fully visible at the end of the article.
- **免許 line 25:** CLEAN ×3. The 免 and 許 links render, and following them then pressing system Back returns to 免許 at the same section.
- **免税 line 26:** CLEAN ×3. The 免 link renders and opens the 免 readings table; system Back returns correctly.
- **許 line 38:** CLEAN ×3. The 免許 example is linked under Common words.

What the screenshots show:
- **Readings quiz:** the kun question offered くすのき, まぬがれる, くわだてる and たちばな; the on question offered イン, カン, メン and リン. まぬかれる was never offered, there was exactly one correct key each time, and the session ended "2 of 2 answers correct."
- **Meaning quiz:** it offered "exempt; be spared", "scarce; lacking", "overcome" and "plan; undertake". The distractors are not near-synonyms, and they are not the authored look-alikes 兄/元/先.
- **Drawing:** practice is ungraded, eight reference strokes show, and grading was by stroke shape only ("handwriting model not available"), so this is not ML Kit recognition. The "Downloading" label does not show a successful download.
- **Fonts:** all four rows (Gothic, Mincho, Textbook, Brush) show all 43 characters plus 免れる, 免許 and 免税 with no missing-glyph boxes. The Mincho row looks sans-like, which fits the fixture's note that fallback faces may coincide; that is not a defect.
- **Clipping:** some screens cut off at the bottom or need sideways scrolling, but later frames show the hidden parts. These are viewport limits, not teaching defects.

Findings: none.

Optional (unchanged from my earlier reports):
- 許.md line 49 does not cite JMdict 1533130 (confirmed in the screenshots).
- 勉 and 晩 also contain the 免 shape.
- An example for the dismissal sense (e.g. 免職).
- The pattern 謗りを免れない.

Limits:
- I read 兄 and 元 in one parallel call during the initial review.
- The original evidence packet lacked the 救助 and 生存 dictionary entries, which I hadn't disclosed in the initial report.
- I did not run the tests; their results were supplied.
- The screenshots do not prove I performed the gestures.
- The fallback font face is not identified.
- The device was an emulator (SDK 35), not a phone. Physical-phone and general-release acceptance remain outstanding.
- An Android build at f9b59a2 or later is required.
- Larger quiz pools remain unverified.
