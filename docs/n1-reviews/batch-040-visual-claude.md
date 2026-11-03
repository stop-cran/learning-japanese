## Batch 040 visual confirmation: 鵬 (original session)

**Snapshot:** The tracked content is at `f5a9e442b4906128cb943d05330a7aa2b1e8b4af`. You state the teaching text is unchanged from `baa525f2d6c2331530bab235ce97a5eaf38b33af`, with no teaching diff. You also note one untracked, non-runtime file from the original session, `N1Batch040NativeTest.kt`, so I am not claiming the whole worktree is clean. I could not check Git, hashes or image dimensions myself because I only had read-only `view` access.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`), in the same session that wrote the initial review. This is a bounded visual check that depends on the earlier review, not a new blind textual review. Each read was one call, made in order:
- my own archived initial report, read once;
- lines 175–230 of the test fixture;
- the eight named screenshots from the emulator.

**Verdicts:**
- **kanji/鵬.md:** correctness and scoped coverage are CLEAN, carried over from the initial review and not re-reviewed. Visual comprehensibility in the inspected screens is CLEAN.
- **words/鵬.md:** correctness and scoped coverage are CLEAN, carried over in the same way. Visual comprehensibility in the inspected screens is CLEAN.

What is visible in each screenshot:
- **font-pairs:** 鵬, 鳳, 鳴 and 島 (U+9D6C, U+9CF3, U+9CF4, U+5CF6) appear in four labelled families: Gothic, Mincho, Textbook and Brush.
  - No glyph is missing and none shows as a blank box.
  - In every family 鵬 shows the paired left shapes beside 鳥, and 鳳 shows the bird inside its frame. 鳴 shows 口 on the left, and 島 shows 山 at the bottom.
  - The Brush 鵬 is heavier and its left half is denser, but it is still clearly different from the other three.
  - The caption sentence below the samples renders fully.
- **selection:** shows "N1 · 72 cards" with N1 selected, and "Browse all kanji" is visible. The rightmost stack chip ("St…") is cut off at the right edge, which reads as a horizontally scrolling row.
- **kanji-mnemonic:** The heading "Modern-shape mnemonic, not etymology:" is bold and visible, together with the "not a claim that the character historically means…" disclaimer. The 鵬 link (ほう) and the 鳳凰 (ほうおう) link with its distinction are visible.
- **kanji-reading-disposition:**
  - The ホウ (on) row and its linked 鵬 (ほう) example are fully visible.
  - In the おおとり (kun) row, the right edge of the third column is cut off ("alternate nam…", "mythica…", "recognitio…"). The "Scroll sideways to read all columns." hint is shown, and the closing "selected for questions." is fully visible.
  - The paragraph "Both full source readings are preserved… practises **ホウ**" is fully visible.
- **kanji-lookalikes:** The Notes bullets for 鳴, 島 and 月, the 大トリ performer boundary, the ぼう variant and the grade-9 qualification all render. The source links render.
- **word-example:** 鵬は想像上の鳥です。 renders with its kana reading and translation, followed by the "not a claimed sighting" qualifier.
- **word-components:** The explanation of the single-character Sino-Japanese noun ("ホウ here", "ほう, not ほ") is visible. The おおとり, 鳳凰, 鳥 and 鴻鵠 comparisons are visible, and so is the Distinctive meaning paragraph covering ほう, ぼう and おおとり.
- **word-reading-boundary:** The 大トリ performer boundary, the passage that keeps the peng apart from the fenghuang and from the rebirth phoenix, and the dictionary links are all fully visible.

Partly cut text lines at the very top of some screens are scrolling artifacts, not lost content.

**Findings:** None.

**Optional:** In the kanji card's おおとり reading row, the long explanation in the third column is cut off at the right edge on this viewport. The scroll hint mitigates this, but a shorter cell, or moving the explanation into the paragraph below the table, would remove the need to scroll sideways. This is nonblocking polish. The four optional suggestions from the initial review stay nonblocking and were not reconsidered.

**Limits:**
- Everything from the initial review carries over: supplied frozen evidence only, the HTML line ranges as given, the regex-only confusable-words search, and the early end of `jlpt-levels.md`.
- **Evidence I only saw as supplied or asserted:** The test assertions in the fixture are not observed native evidence in themselves. The following I did not observe myself:
  - the passed runs, sync counts and the Room or reading-adapter data;
  - the `hasGlyph` probes and the per-character raster hashes;
  - offline navigation and system-back behaviour.

  Still screenshots do not prove navigation or queue behaviour.
- **What I did not inspect:** two of the fixture's captures, "backlink-kanji" and "word-mythology-boundary", because they were not among the eight assigned images. I also did not see offscreen rows, the whole articles, or other font and layout settings. The viewing tool may have resized the images.
- **Device coverage:** Only the API 35 emulator screenshots are covered. There is no physical-phone or native-speaker evidence. Current-main, CI, public ZIP and publication acceptance are not covered. Compatible Android `f9b59a2` or later is required; phone and general-release acceptance remain outstanding.
- **Process:** There was no fresh meaning, reading or drawing session, and no tool calls overlapped or failed.
