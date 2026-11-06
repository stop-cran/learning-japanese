# SAME081 visual confirmation of batch 081 (冶, 冶金, 金 bullet): final report

All three in-scope items are CLEAN on every facet, and I found no defects. The only surprise is that the captured meaning question used different wrong choices from the three the article names (治 / 台 / 始); that is a limit on what was tested, not an article error.

## Snapshot
- **Reviewer model:** Claude Opus 5.5 (claude-opus-5.5).
- **Teaching snapshot reviewed:** b7bf953d137251f179a57128bb84bd70a37737c8.
- **Evidence HEAD:** 824045ee9eefca3c7ee883a7b7687d72a52d4f96.
- **Native archive:** 95a87783.
- **Files:** the article hashes in the source packet (`冶.md` 803fdcda…, `冶金.md` 4bf61335…, `金.md` 96bbf429…) match my textual review. I checked them by comparing text only, not with any independent Git or hash tool.

## Scope
**What I read.** Each resource got exactly one view call in its own turn, with nothing reread:
- the complete visual source packet (no truncation marker shown);
- 25 original PNGs, which the host says cover all 45 captures after byte-for-byte deduplication.

**Resource 26.** I viewed it before my conversation history was compressed, so my observation for it came from notes of that view, not a fresh look at the pixels.

**Image quality.** The view tool may have shrunk the frames. I make no full-resolution claims.

**Items reviewed:**
- the new `kanji\冶.md`;
- the new `words\冶金.md`;
- only the added `金.md` bullet, "冶金 やきん — metallurgy".

**What is inherited.** My lexical conclusions carry over from the textual review; I did no fresh dictionary lookups. The existing evidence from all 40 font families is inherited, not re-reviewed.

## Verdicts

| Item | Correctness | Scoped coverage | Bounded visual comprehensibility |
|---|---|---|---|
| `冶.md` | CLEAN | CLEAN | CLEAN |
| `冶金.md` | CLEAN | CLEAN | CLEAN |
| `金.md` bullet | CLEAN | CLEAN | CLEAN |

CLEAN means no established, actionable defect within scope. It is not exhaustive certification.

## Findings
**None.** The textual lexical conclusions are unchanged:
- **Readings:** the full source order is ヤ, then kun い.る. Only ヤ is selected, with an empty kun list.
- **いる:** the kun reading い.る is shown as dictionary information only. It is not evidence for a modern verb 冶る, and 鋳る is kept separate.
- **冶金 (やきん):** taught as technical metallurgy, not gold, money, a single melting or casting step, or alchemy.
- **鍛冶:** かじ is treated as a whole-word reading, with たんや kept separate and no invented ジ reading.
- **Teaching aids:** the mnemonic is qualified and not presented as etymology.
- **Facts:** seven strokes, grade 8 and radical 冫 (15) as opposed to 氵. N1 is a community level, not an official syllabus, and no word level is inferred.

**What the pixels show:**
- **Fonts:** all 29 scoped Han characters render in Gothic, Mincho, Textbook and Brush across the three panels, with no blank or replacement boxes.
- **Look-alikes:** 冶, 治, 台 and 始 are distinct, and 冫 (two marks) can be told apart from 氵 (three). 冶金 renders as a whole word in every family.
- **Reading question:** offers ヤ / ヤク / シ / ヘイ with one correct answer. The feedback "smelt; work metals: ヤ、いる" shows the full kun list, but no kun question was offered.
- **Done screen:** "1 of 1 answers correct."
- **Meaning quiz:** the prompt was 冶. The wrong choices captured were "two (formal numeral)", "chrysanthemum" and "moreover; also", not the curated 治 / 台 / 始. Only one answer was defensible. This is recorded under Limits, not as a finding.
- **Links:** the 冶 ↔ 冶金 and 金 ↔ 冶金 destinations show up in the frames, and the 金 bullet is linked and formatted correctly. System Back returned to the 冶 card.
- **Tables:** the long い.る cell is cut off before scrolling but fully readable in the scrolled state; the scroll is signposted. The 冶金 "Scope" line is cut off in three frames but fully visible in one.
- **Selection:** "N1 · 113 cards".

## Optional (my original suggestions, kept)
1. `冶.md:38`: make the "inspected families" and "source-only" wording plainer. The visuals support this: the cell wraps to about ten lines on the emulator screen.
2. `冶.md:52–58`: note that the dictionary marks 鍛治 as an irregular spelling and that たんや uses the regular ヤ reading.
3. `冶金.md:45–46`: mention the "money-making" sense of 錬金術.
4. `金.md:39`: consider adding a "(technical)" label.
5. `冶.md:64`: give the KANJIDIC2 version.
6. New, app-level: the standalone 冫 in prose renders small and faint. It is legible, but a more prominent rendering would help.

## Limits
**Earlier runtime and rendering limits, reconciled:**
- **Glyphs:** resolved, but only for emulator pixels.
- **冫 vs 氵:** partly resolved. They are distinguishable but faint, and legibility on a physical phone is unverified.
- **Clipped tables:** resolved by looking at the scrolled and unscrolled states together.
- **Links and Back:** the destinations are visible in pixels; the tap order comes only from the supplied route evidence.
- **Curated meaning distractors (治 / 台 / 始):** unresolved. They were not captured at runtime and the cause is unknown. I make no claim about whether every possible random set of choices is safe.

**What comes only from supplied evidence, not from pixels:**
- the ContentSync result (1093 kanji, 5049 words, 113 N1 cards, version f1dd5d8b9d2ff535, zero problems, epoch 1);
- the Full/Lite readings and quiz keys, the persisted good log, the seeded fixture state and offline status;
- 2/2 tests passing on emulator-5580 (API 35, read-only) and the stopped helper process;
- the 116 individual and 4 whole-word Paint assertions, which are not PNG reads.

Pixels, Paint.hasGlyph results and raster hashes do not identify which fallback font face was used.

**Drawing:** this was a shape-only comparison of seven injected reference strokes. It is not human handwriting, real recall, ML Kit recognition or a model download; the screen showed the handwriting model as unavailable.

**Not covered at all:**
- independent Git or upstream verification and fresh dictionary lookups;
- full-resolution or hash checks of the images;
- a physical phone;
- native-speaker review or learning-effectiveness evidence.

Final integration with current main, publication, CI, the immutable ZIP, the physical phone, general release and the whole-set review are still outstanding.
