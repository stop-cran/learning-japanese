# Batch 097 final confirmation — 剣 kanji, 剣 つるぎ word, reused 真剣 and 真

No defect is established. Every scope is CLEAN for correctness, coverage and comprehensibility, within the bounded evidence below.

## Snapshot
- **Content and archive:** signed content HEAD e75b4bb14ba5ee3183a973be7752033721a5246e; native full archive 83e5c090.
- **Teaching content:** reviewed teaching 1fa1ac69 is unchanged; version a066afceaf1f447a.
- **Native build:** the native 714 run used a TEST-ONLY Android build, 1c1b7bf4, which keeps production f9b59a2. This is not the latest app main.

## Scope
- **Model and session:** Claude Opus 5.5 (`claude-opus-5.5`), my original session 3a0b6dd8. This is a dependent confirmation, not a fresh blind review.
- **Process:**
  - These 17 resource-gated turns made exactly one `view` call each, one at a time.
  - The earlier 715 batched attempt had 29 tool overlaps, so it does not count as serial reading.
  - These turns add corrected process evidence, not retroactive independence.
- **Text read:** `control\batch-097-resource-gated-715\claude-bounded-text.txt`, in full. It contained:
  - my original report and the native receipt;
  - the complete kanji\剣.md, words\剣.md, words\真剣.md and kanji\真.md, with the exact diff;
  - the quiz contract;
  - all 64 kanji choice records;
  - the label dictionary, all 512 word-guard records, and the contact-sheet index.
- **Images viewed:**
  - Font panels 1–3 at full size: all 20 Han in Gothic, Mincho, Textbook and Brush, plus the words 真剣 and 剣道.
  - Contact sheets 01–13 at reduced scale, covering 52 route captures. I opened no original screenshots.
- **Inherited, not re-reviewed:**
  - From my initial review: the full JMdict families, the 18 comparison articles, the raw metadata and the dictionary text.
  - Gaiji (non-standard characters) in the dictionary text are still not decoded.

## Verdicts
Each part is rated for correctness, scoped coverage and text comprehensibility.

| Part | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| kanji\剣.md (new) | CLEAN | CLEAN | CLEAN |
| words\剣.md, つるぎ (new) | CLEAN | CLEAN | CLEAN |
| words\真剣.md line 27 (changed) | CLEAN | CLEAN | CLEAN |
| kanji\真.md line 37 (changed) | CLEAN | CLEAN | CLEAN |
| Bounded rendered and quiz checks | CLEAN | CLEAN | CLEAN |

CLEAN means no defect shown in the actual bounded sample. It does not certify the wider custom, random or legacy pools.

## Findings
None proved. The evidence:

- **Glyphs:**
  - All 20 Han are legible in all four styles. The right-hand 刂 shows on its own in every style.
  - 剣, 剛, 剖 and 則 have clearly different left components.
  - 刃 shows the acceptable 刄-style variant in Mincho and Textbook, and leans that way in Brush.
- **Reading quiz:**
  - Raw readings ケン and [つるぎ] and the exact curation are kept in both the full and Lite data.
  - The ケン question and the つるぎ question are each answered "Correct!", ending at Done "2 of 2".
  - None of the wrong readings belongs to 剣.
- **Meaning quiz:**
  - The actual screen shows 剖 "dissect; split open", 剛 "sturdy; unyielding strength" and 蚊 "mosquito". This is different from the builder's seed-0 record (丙), and I did not infer the screen from it.
  - 則 is N2, so it is not available in the N1 pool. That leaves 2 curated wrong choices plus 1 fallback, matching the receipt.
- **All 64 kanji choice records:** none of the fallback labels is an answer equivalent to sword or blade. 矛 "spear; polearm" is in the weapon domain but means a different weapon.
- **All 512 word-guard records:**
  - The excluded partner never appears for any of the four guarded pairs (剣 with 刀, 日本刀, 刃 and 真剣), in either direction or either quiz orientation.
  - That proves only those four pairs. Among the other options, the related words are not equivalent: 武士 samurai, 鋏 scissors, のこぎり saw, 重要 important and 積極的 proactive.
- **Navigation:**
  - The captures fit the three link pairs (剣 kanji↔剣 word, 剣 kanji↔真剣, 真 kanji↔真剣), the six directions and System Back.
  - The changed lines render correctly: 真剣 line 27 shows 真 and 剣 as links, and the 真 line 37 bullet appears in Common words.
  - The route names come from the capture labels; I can't see tap targets at this scale.
- **Selection screen and drawing:**
  - N1 · 129 cards; meaning 1 due, drawing 1 new, readings 2 due.
  - Tracing, then "Well drawn!" (graded by stroke shapes only; the handwriting model was unavailable), then the give-up recall screen.
- **Articles at phone width:**
  - Both new articles render in full and wrap cleanly.
  - The cut-off "earne…" in the readings table is hidden content: the "Scroll sideways" hint is present, and the sideways-scrolled captures show it in full.
  - The □ boxes in some tile labels come from the contact-sheet tool, not the app.

## Reconciliation
- **Resolved:**
  - My hypothesis that fallback choices could bring in 刃 or 刀. The word guards hold, and the actual kanji fallback is 蚊.
  - Whether production choices would be safe, within the bounded 64 and 512 records only.
- **Partly resolved:** whether `kanji\口.md` exists. 口 renders as a link, but I did not check the file itself.
- **Unresolved, not a defect:** whether standalone 剣 is read けん more often than つるぎ. Both readings are presented as valid.
- **Withdrawn:**
  - My earlier claim that I read the 715 batch serially.
  - My panel-1 narrowing of the 刄-style 刃 to two fonts; panel 3 shows Brush also leans that way.
- **Kept as optional:** the original items, listed below.

## Optional
- A sourced note on when a text uses つるぎ versus けん.
- Explain the zoological senses as stinger/ovipositor.
- Mention the clock-hand meaning (短剣/長剣) and the old forms 劍/劒.
- 積極的 appears in every All-pool row of the 真剣 word guards. It is a related attitude word but not an equivalent answer, so this is a watch item only.
- The readings table needs sideways scrolling; the hint already covers this.
- A cosmetic "'" mark under the header when the kanji article is scrolled to the end, most likely the bottom of a cut-off line. Unconfirmed at this scale.

## Limits
- No independent Git or upstream checks. The dictionary gaiji are not decoded.
- The contact sheets are reduced scale.
- The native evidence comes from the supplied 714 receipt on an API 35 emulator: one full ContentSync import, 1120 kanji, 5073 words, 129 N1 cards, zero problems, Room epoch 1, two terminal cases with 0 failures and no skips.
- I ran no native tests myself. There is no physical-phone, human handwriting or ML Kit evidence; the ten injected strokes certify neither.
- I make no claim about the wider pools, a general release, the whole set, publication, or learning effectiveness.
