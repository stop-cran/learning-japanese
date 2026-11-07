# Batch 100 rendered confirmation (759): 創 and three reused passages are clean on screen

All four passages pass on correctness, scoped coverage and comprehensibility in the rendered app. 樹 is gone from the meaning options, and I found no new defect. This depends on my earlier reviews; it is not a fresh blind review.

**Snapshot:** frozen signed cffdad1291d2acd847c669ab87c3c8b58572824f. The runtime content is the same as 755. The native run is 758, with content version 606c836e4be33ba9.

## Scope
- **Model and session:** claude-opus-5.5, resuming session 4975f494-5c25-4a2d-8060-775ded9c734c.
- **Text read:**
  - `batch-100-rendered-759-claude-own-reports.txt`, in full.
  - `batch-100-rendered-759-packet.txt`, in one view call with forceReadLargeFiles. It returned complete content through the image list, with no truncation marker. I could not count the 232,523 bytes / 11,686 lines myself.
- **Images:** I viewed all 15 listed PNGs serially, one per response:
  - 11 reduced-size contact sheets, covering 43 route captures (some are duplicate final-view captures).
  - The 3 original font panels.
  - The original meaning-question screen.
  - I opened no other original route PNGs.
- **Provenance:** all evidence was supplied by the coordinator, including the native-run results and its checks: 2464 kanji-guard, 1760 neighbor, 2304 word-guard and 64 choice checks. I did not reproduce any of it.
- **System Back and offline route:** I saw on-screen Back buttons and link destinations. I did not see captures I could identify as system-Back or offline states, so for those I rely only on the packet text.

## Verdicts

| Passage | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\創.md` (article, reading/meaning/drawing feedback) | CLEAN | CLEAN | CLEAN |
| `words\創作.md` line 30 (創 link, sheet 10) | CLEAN | CLEAN | CLEAN |
| `words\作る.md` line 36 (創る link, sheet 11) | CLEAN | CLEAN | CLEAN |
| `kanji\作.md` line 45 (創作 entry, sheet 10) | CLEAN | CLEAN | CLEAN |

**Sampled meaning semantics: CLEAN, for these options only.**
- The original screen shows: frugal; thrifty (倹) / originate; create (創) / silkworm (蚕) / sword; double-edged blade (剣). The 4-option feedback screen matches.
- None of the 22 sampled labels overlaps 創's taught senses (create, originate, establish, start, wound). 蚕 is not a creation meaning.
- The `meaningFallbackNeedsSemanticReview=true` flag neither counts as a recurrence nor proves the result clean.

**Reading questions: CLEAN.**
- ソウ: options ケン/ソウ/オウ/ボウ. つくる: options つましい/つるぎ/つる/つくる.
- No wrong option is a valid reading of 創. Both feedback screens list all six readings, and the session ends "2 of 2 correct".

**Drawing:** trace and recall show 12 numbered strokes, legible. Grading was by stroke shape only, because the handwriting model was unavailable.

**Four-font rendered readability: CLEAN for distinguishing.**
- All 21 Han characters are legible in all four rows. That includes 刂, 樹, and the lookalikes 創, 倉, 剣, 倹 and 験.
- I saw no blank glyph or replacement box.
- 刂 in the Mincho, Textbook and Brush rows looks like a fallback glyph, but it stays readable.
- The Textbook row's final 設 wraps to a second line and remains visible.

## Findings
None.
- The reading table is cut off at its right edge in the first view, but a visible "Scroll sideways to read all columns." prompt explains it, and the scrolled views show the full text.
- Mid-word breaks like "creation-oriente / d" are cosmetic only.

## Reconciliation
- **N753-fallback-establish: resolved.**
  - The meaning was settled textually in 755.
  - The coordinator's 758 run shows the change is enforced.
  - The rendered option set no longer contains 樹, and the replacement default 蚕 is semantically safe.
  - In N1 there are two curated wrong answers (剣, 倹) plus one fallback; 験 stays at N4. Nothing was relevelled or masked.
- **F1, C1-establish and H1-initial:** still resolved, as history. The conservative 創/初 guard is not a proven live failure and not a claim that the two are synonyms.
- **H1-wound:** still withdrawn.
- **Rendered checks on inherited points:**
  - The six readings appear in their original order.
  - ショウ and けず.しける are shown as source-only, unselected readings. Their usage remains unverified.
  - 創める is limited to establishing something, and 創 is a rare spelling of きず.
  - The 作る (N5) and 創作 (N2) identities are intact.

## Optional
- O1–O4 from earlier reviews are still optional:
  - O1: in Notes, say which parts actually look alike.
  - O2: "fabricated story" could become "fabrication; made-up account".
  - O3: a hedged note that 倉 is phonetic.
  - O4: the source-only reading rows are long for a phone screen.
- The 754 decisions file cites wrong line numbers.
- New, optional: add hyphenation or soft-wrap hints to avoid mid-word breaks in the table.

## Limits
- **Device and fonts:**
  - The captures come from an API 35 emulator, not a phone.
  - The contact sheets are reduced size.
  - From pixels I cannot prove which typeface is used or which fallback face is substituted; the Gothic and Mincho rows look very similar.
- **Drawing:** the 12 strokes were injected and graded by shape only. That is neither ML Kit recognition nor evidence of human recall.
- **Not done:** no Git, upstream or native reproduction.
- **Not certified:**
  - future random option pools
  - how well the card teaches
  - acceptance of the whole project
