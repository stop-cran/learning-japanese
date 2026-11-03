I looked at all five screenshots and found nothing that needs fixing. All six verdicts stay CLEAN. Comprehensibility is confirmed only for what was on screen in the API 35 emulator at font scale 1.

**Snapshot:** signed snapshot `392c176fe50512e306813ece23ac9b6490e5dca9`, with teaching unchanged since my original review at `43428b8…`, as you stated. I did not run git to confirm this. Only non-runtime evidence is uncommitted.

**Scope:**
- **Model and session:** Claude Opus 5.5 (`claude-opus-5.5`), same session 6da9e279. This is a dependent visual check, not a new blind or 28-family review.
- **Read once:** my own `docs\n1-reviews\batch-023-initial-claude.md`.
- **Screenshots viewed directly, one per response, each once:** `n1-023-font-pairs.png`, `n1-023-selection.png`, `n1-023-kanji-catfish-readings.png`, `n1-023-kanji-component-notes.png`, `n1-023-word-catfish.png`.
- **Not read:** `n1-023-font-raster.json` and `n1-023-article-route.json`, other reviewers' opinions, and the author's adjudication.

**Verdicts:**
- `kanji\鮎.md`: correctness CLEAN (carried forward); scoped coverage CLEAN (carried forward); comprehensibility CLEAN (on-screen only).
- `words\鮎.md`: correctness CLEAN (carried forward); scoped coverage CLEAN (carried forward); comprehensibility CLEAN (on-screen only).

**Findings:** none. What I saw:
- **Font pairs:** the screenshot labels four rows Gothic, Mincho, Textbook and Brush. Every row shows 广, 店, 鯰 and 鮎 with no tofu (empty boxes) and no clipping.
  - 广 and 鯰 look the same in all four rows, while 店 and 鮎 change style. That fits your note that the system draws these two glyphs, but I can't confirm the source from a screenshot.
  - 广 versus 店 is clear, since 店 adds 占 under the roof.
  - 鯰 versus 鮎 is clear, since 鯰 has 念 on the right and 鮎 has 占. The caption "广: component in 店. 鯰: catfish; 鮎: ayu." reads cleanly.
- **Selection screen:** the screen shows "N1 · 55 cards" with N1 selected and a meaning quiz showing "0 due, 10 new". Drawing and readings show as locked. No overlays.
- **Readings table:** the view is scrolled sideways, so I assessed only the visible cells.
  - The Type column and the visible Typical-words cells are legible, including 瓢鮎図 ひょうねんず and the linked 鮎 あゆ.
  - The table header and the last row are cut off, so I did not assess them.
- **Component notes:** the 占, 店 (with 广) and 点 comparison, the 魚 and 鯉 links, the Common words list and the source line are all legible. The topmost line is partly hidden under the fixed header while scrolling, which is ordinary scroll behaviour.
- **Word article:** the catfish passage "なまず・ナマズ・鯰" renders, and 鯰 is legible next to its kana. The links to 焼く, 食べる, 魚, 鯉 and 川 are visible.

**Optional:**
1. "Character-dictionary" wraps mid-word in the narrow table column ("Character-dictio / nary"). It is still readable. Shortening it to "Dictionary" or "Source-only" in the table cells would avoid the break.
2. Kana break across lines in two places ("あ / ゆ" and "ナ / マズ"). This is ordinary Japanese line breaking and not a defect.
3. My original optional notes (the 广 gloss, naming Jitsu inline, the 瓢鮎図 catfish note and the hedged origin note) are unchanged. The screenshots don't show any visual problem that would make the 广 gloss necessary.

**Limits:**
- **Not checked:** the offscreen table cells and the cut-off row, any states other than these five screenshots, and quiz rendering.
- **Coordinator-supplied, not seen by me:** device identity, the bundled font file contents (cmap), the import or route, whether tests passed, and file hashes. These include the emulator details (API 35, font scale 1), the single exact-archive sync and the identical-render claim; I did not run or confirm any of it.
- **Phone:** physical-phone and general-release acceptance are still outstanding.
- **Carried forward:** correctness and coverage rest on my original text review, not a fresh source check. The one-call-rule breach in my original review still stands; I made no parallel calls this time.
