This visual follow-up found no blocking defect: all three facets are CLEAN for both 丑 articles and both changed 寅 links, and 丑五互土宀氵牜 are readable and distinguishable. This is not a new blind review and does not replace the two initial reviews.

**Snapshot:**
- **Commits:** tracked content `080cf0774f00bc16616dc6479a469578bce0b67d`; native frozen envelope `049c34b2d1527267d567b2f794825cbac1f28f37`, which is said to differ only in contributor evidence.
- **Unchanged teaching:** I read all four teaching files in full. Their text matches what I reviewed in the initial at `0e73a4115a1f747ef7370efdb5ef271e5ecdfe94`, including both changed links: 寅 kanji line 62 and 寅 word line 52.
- **Not verified:** I had no shell, so I could not check Git, signatures, hashes, image dimensions or the envelope.

**Scope:**
- **Reviewer:** the original Claude reviewer from session 91d3d776-3bc6-4f71-9e40-049257c10a01, model `claude-opus-5.5`.
- **Calls:** 18 view calls, strictly one per response, nothing in parallel.
- **Text reads, in order:**
  1. the task prompt;
  2. `docs\n1-reviews\batch-049-initial-claude.md` (my original report, full);
  3. `kanji\丑.md`, `words\丑.md`, `kanji\寅.md`, `words\寅.md` (each full, each in its own response);
  4. `N1Batch049NativeTest.kt`, lines 140–289 only.
- **PNGs, one per response, in this order:** font-pairs, selection, kanji-radical, kanji-mnemonic, kanji-reading-disposition, kanji-lookalikes, reused-tiger-kanji-link, reused-tiger-word-link, word-sign-example, word-components, word-sign-boundary.
- **Not seen as separate images:** the 11 screenshots described as hash-identical to these. I did not open them; they are supplied claims only.

**Verdicts:**

*Carried over from the initial text review (no teaching change since):*
- `kanji\丑.md`: correctness, coverage and comprehensibility CLEAN.
- `words\丑.md`: correctness, coverage and comprehensibility CLEAN.
- `kanji\寅.md:62`: correctness, coverage and comprehensibility CLEAN.
- `words\寅.md:52`: correctness, coverage and comprehensibility CLEAN.

*Bounded visual verdicts:*
- **Glyphs:** CLEAN.
  - 丑, 五, 互 and 土 are drawn differently in each of the four rows (Gothic, Mincho, Textbook, Brush) and are distinguishable in every row.
  - 宀, 氵 and 牜 look the same in all four rows, which fits a shared system fallback, but they are readable. The actual fallback font is unknown.
- **`kanji\丑.md`:** CLEAN for every assigned point I could see.
  - The facts line shows "一 (no. 1)". The mnemonic shows the crossbar wording, the bent top-and-right stroke, the descending inner stroke and the "not etymology" label.
  - The reading rows show チュウ (on) and うし (kun). The disposition paragraph is complete: only うし is selected, チュウ is calendar recognition and not obsolete or name-only, and it includes 丁丑 ていちゅう and the sixty-term versus twelve-sign note.
  - The Notes show the 五/互 inner turns, 土's single upright, and 牛 as the animal.
  - The historical note shows both hour ranges (1–3 a.m. and 2–4 a.m.), north-northeast versus 丑寅 northeast, and "not Gregorian December".
- **`words\丑.md`:** CLEAN.
  - Both examples and their translations are readable, as is the かんし/えと limit.
  - Also readable: the single-character explanation, 丑年 うしどし, 牛/ウシ versus the 丑 sign, and the full historical paragraph with 丑寅 linked through 寅.
- **Changed passage at `kanji\寅.md:62`:** CLEAN. The screenshot shows "[丑]寅 (うしとら), northeast … not the same direction as standalone 寅", with only 丑 styled as a link. In the surrounding notes, 氵 renders readably.
- **Changed passage at `words\寅.md:52`:** CLEAN. The screenshot shows "distinct from [丑]寅 (うしとら), northeast", with only 丑 styled as a link.

**Findings:** None blocking or actionable.

**Optional (nonblocking):**
- **Clipped reading table:** In the kanji-radical, kanji-mnemonic and kanji-reading-disposition screenshots, the Typical words column is cut off at the right ("ていちゅ…", "term…", "recognition on…", "丑…", "yea…"). A "Scroll sideways to read all columns" hint is shown. The disposition paragraph repeats ていちゅう in full. I do not certify the hidden columns.
- **Input-method toolbar:** It covers the bottom of the initial radical screenshot; the うし row is visible again in the next screenshot.
- **Selection chips:** The chip row on the selection screen is cut off at the right ("Sta…").
- **Viewport edges:** In reused-tiger-word-link and word-sign-boundary, the top line sits partly under the header. In word-components, the bottom line is cut off; the next screenshot shows it in full.
- **Small gap after 氵:** There is a small gap after 氵 in the 寅 kanji notes; it is still readable.
- **My original optional groups:** All four remain nondefects and were not adopted. I am not raising them again.

**Limits:**
- **Supplied, not checked by me:**
  - The test run: 2 terminal cases, 0 skips, 39.557 s, 28 glyph probes.
  - The import counts: 1061 kanji, 5019 words, 81 N1 cards, version `1a13e8e6d637bc5b`, 0 problems.
  - The reading fields: full on チュウ, full kun うし, empty on'yomi quiz list, うし as the only kun'yomi quiz key. The fixture's assertions match these, but I saw no run output.
  - Link and System Back navigation passing, the emulator fingerprint and memory settings, and the Android/host-OOM history.
- **Fixture versus results:** I read the fixture's code only, not its execution or evidence JSON.
- **Not done:** no quiz, meaning, reading or drawing session; no physical-phone or native-speaker check; no general-release, current-main, CI or public-ZIP claim. Source re-verification, the calendar-alternate discrepancy and the geometry limits stay open as stated in the task.
- **Initials:** I preserved the recorded facts about the two blind initials (different model families, 39 and 38 serial calls, zero overlaps, zero range violations, all 24 resources) as stated in the task. This follow-up is dependent and not blind, and it does not re-certify them.
