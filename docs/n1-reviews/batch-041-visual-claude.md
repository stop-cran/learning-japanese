I viewed all eight screenshots, and the visual check is CLEAN for both cards. All four characters render as distinct glyphs in four font families. Every assigned teaching passage is readable on screen, and I found no blocking defects. The original text review stands unchanged: CLEAN on all facets, no findings, four optional suggestions.

**Snapshot:** Tracked content at `e4b8aba582d203636c4e7421b0c6fed40b34e3b8`; I was told the teaching is unchanged from `75b4ae840933a9002d07a0bfa549539cea0b2554`. The only extra file is the untracked native test fixture. I had no shell, so I could not check Git or hashes. I did confirm that both teaching files read today match what I quoted in my original review.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (claude-opus-5.5), same session as the original review (59c10618-fb54-4c21-9ba0-2a1a41a59da6). This is a dependent visual follow-up, not a new blind review.
- **Text read:**
  - my original report, `docs\n1-reviews\batch-041-initial-claude.md`, in full
  - `kanji\隼.md` and `words\隼.md` in full
  - `N1Batch041NativeTest.kt`, lines 175–230 only
- **Screenshots viewed one at a time**, all in `control\artifacts\batch-041-parent-native-attempt-6\`:
  1. `n1-041-font-pairs.png`
  2. `n1-041-selection.png`
  3. `n1-041-kanji-mnemonic.png`
  4. `n1-041-kanji-reading-disposition.png`
  5. `n1-041-kanji-lookalikes.png`
  6. `n1-041-word-example.png`
  7. `n1-041-word-components.png`
  8. `n1-041-word-naming-boundary.png`

**Verdicts:**
- **Text review (carried over from the original):** `kanji\隼.md` and `words\隼.md` are both correctness CLEAN, scoped coverage CLEAN and comprehensibility CLEAN. I did not redo the linguistic review.
- **Visual check, kanji card:** CLEAN.
  - The fonts screenshot shows 隼, 準, 集 and 十 as clearly different glyphs in Gothic, Mincho, Textbook and Brush, with no tofu boxes.
  - "Modern-shape mnemonic, not etymology" and the "not … 'ten birds'" disclaimer are fully visible.
  - The inherited radical 隹 renders inline.
  - All three reading rows (シュン/on, ジュン/on, はやぶさ/kun) appear in source order, with the source-only label on ジュン.
  - The "practices はやぶさ only" paragraph and all Notes bullets are fully readable.
  - The selection screen shows "N1 · 73 cards", matching the supplied count.
- **Visual check, word article:** CLEAN. Both examples, their kana readings and translations are readable. So are the component explanation, the 鷹/鳥/動物/生き物/鷲 boundaries, the one-to-one species caveat, the spacecraft/personal-name boundary and the dictionary line.

**Findings:** None blocking.

**Optional:** The Readings table's third column is clipped on the right ("ようしゅ…", "archai…", "but n…", "はやぶ…"). The app shows a "Scroll sideways to read all columns" hint. The key reading decisions are still readable without sideways scrolling, both in the visible text and in the full paragraph below the table. So this is nonblocking polish, either a narrower table or moving more qualification into prose. The cut-off "St…" filter chip is part of the app's horizontal scroll row, not content.

**Limits:**
- **Process:**
  - This session used 13 view calls, made one at a time, with no repeats.
  - The task also asked me to keep the original review's figures: 33 calls, one internal overlap (the two comparison-packet ranges requested together) and 0 XML violations.
  - All dictionary evidence is still the supplied material only.
- **What I did not see:**
  - The clipped table text and its sideways-scroll content.
  - Parts of the articles outside the eight screenshots.
  - The fixture's other captures (`backlink-kanji`, `system-back-word`, `word-name-boundary`).
  - Anything outside lines 175–230 of the fixture.
- **Not independently verified:** The fixture runs and environment details you supplied: attempts 1–6, the 2 terminal cases with no skips, the 16 hasGlyph probes, the sync and import counts, the hash matches, the separately verified 186-test Android run, the emulator details, the system ANR (app not responding) cause and the helper cleanup. I also did not check image hashes or dimensions.
- **Not done:** Meaning, reading or drawing quiz sessions, physical-phone testing, native-speaker review, general release, current-main, CI and public ZIP checks. The screenshots come from an emulator and show text readability only.
