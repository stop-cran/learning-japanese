I'm marking the visual evidence CLEAN within its narrow scope: in all five screenshots I saw no defect. The older form 螢 and current 蛍 are distinguishable in all four font rows and in the two article passages that show 螢. There are no findings.

**Snapshot:** tracked snapshot 862bdef3122b55ab2f3490a728c54d09529dc7de, with teaching unchanged since b751248ea6f9f3d2cd2084e7e744d9de4d7ff30d. You said only non-runtime evidence is uncommitted. I wrote no files.

**Scope:**
- **Model and role:** Claude Opus 5.5 (claude-opus-5.5), same session as before. This is a dependent visual confirmation, not a new blind review or a fresh 72-family source check.
- **Reads:** one call per response, each awaited:
  - my earlier report `docs\n1-reviews\batch-017-bounded-claude.md`, once;
  - the five PNGs in `control\artifacts\batch-017-parent-native-attempt-4\`, once each: `n1-017-font-pairs.png`, `n1-017-selection.png`, `n1-017-kanji-old-form.png`, `n1-017-word-old-form.png` and `n1-017-reused-component-link.png`.
- **Not read:** `n1-017-font-raster.json`, `n1-017-article-route.json`, and any other reviewer's or the author's opinions.
- **Facets:** correctness and coverage carry forward from my earlier text reviews without fresh source checks. Comprehensibility is limited to what these viewports show at the stated API 35, font scale 1.

**What the screenshots show:**
- **Font pairs:** four labelled rows: Gothic, Mincho, Textbook and Brush.
  - In every row, 螢 and 蛍 are complete and clearly different. 螢 shows the two 火 above 冖 and 虫; 蛍 shows the three short strokes ⺍.
  - The 蛍 glyph changes design from row to row; the Brush version is heavy but still recognisable.
  - The 螢 glyph looks the same in all four rows. This matches the coordinator's note that one older-form raster is used across the rows; it does not show four different older-form typefaces. A typeface difference is not a defect.
  - The caption "螢 is the older character form of 蛍." renders both characters with no missing-glyph boxes.
- **Selection screen:** the Kanji screen shows "N1 · 49 cards" with N1 selected, "Meaning quiz 0 due, 10 new", and Drawing and Readings locked. The rightmost chip ("Sta…") is cut off at the screen edge; that looks like a horizontally scrolling row, and I did not check it.
- **Kanji card (蛍 firefly):** this view is scrolled.
  - The "Common words" heading is partly hidden under the header, which is the normal result of scrolling.
  - All five common words with their kana are readable.
  - In Notes, "The older character form is **螢**" is bold, smaller than the headline glyph, but still clearly different from the surrounding 蛍.
  - The 虫, 学, 栄 and 営 links and the metadata and source line are readable. I saw no missing-glyph boxes or overlays.
- **Word article (蛍 firefly):**
  - "How the kanji combine" shows **螢** (bold) next to several 蛍, and the two are distinguishable.
  - Two words break across lines: ホタ/ル and ケ/イ. This is ordinary Japanese line-breaking and not a defect.
  - The last line is cut at the bottom of the screen, which is scroll position.
  - The 虫, 蚊 and 蛍光灯 links are readable.
- **Reused 蛍光灯 article:**
  - The three-line header wraps cleanly with Back.
  - In "How the kanji combine", the new 蛍 link is underlined and coloured at the start of the paragraph, next to the 光 and 灯 links. The text reads "The readings are ケイ + コウ + トウ."
  - This article does not show 螢, as expected from its text. Nothing is clipped or covered.

**Verdicts:**

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\蛍.md` | CLEAN (carried forward) | CLEAN (carried forward) | CLEAN (in the observed viewport) |
| `words\蛍.md` | CLEAN (carried forward) | CLEAN (carried forward) | CLEAN (in the observed viewport) |
| `words\蛍光灯.md` | CLEAN (carried forward) | CLEAN (carried forward) | CLEAN (in the observed viewport) |

**Findings:** none.

**Optional:** none new. My earlier optional items remain as recorded: the 蛍/火 exclusion is kept as conservative, expanding "Seisenban" once is polish, and the glow wording and the larger-quiz fallback need no change.

**Limits:**
- **What screenshots cannot show:** they cannot prove whether 螢 is present in the bundled fonts, which device was used, that routes or import worked, that tests passed, or file hashes. Archive and sync provenance came from the coordinator; I did not run anything myself.
- **Partial views:** each article screenshot covers only one scroll position, so passages outside it were not seen. That includes the kanji card's top, mnemonic and readings table.
- **Not seen:** the backlink and system-back screenshots, which you said are byte-identical. I also did not see the quiz screens.
- **Original process slip still stands:** in the initial review, one response made six parallel `view` calls. Later serial work does not fix that.
- **Still outstanding before publication:** this evidence is one API 35 emulator at font scale 1. Physical-phone native acceptance and general-release acceptance remain outstanding and are not certified here.
