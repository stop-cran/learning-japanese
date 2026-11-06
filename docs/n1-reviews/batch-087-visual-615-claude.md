I viewed all 12 images and found no new defect. The three articles are readable across all 55 screenshots, 几 renders clearly in every font row, and the quiz choices I saw have exactly one defensible answer.

**Snapshot:** Evidence HEAD dbf9201eb2c70fd0e5819a14ef6b1e74b7cbc396; teaching f6391022356073dd3e53437be30885f9a09857d9 is unchanged (the supplied diff is empty). The screenshots come from content snapshot 404f507d and the qualified test-only Android build 1c1b7bf4, which keeps production f9b59a2. That build is not the latest app main.

**Scope:**
- **Model and session:** Claude Opus 5.5 (`claude-opus-5.5`), same session 2308e256. This is a dependent follow-up, not a new blind review.
- **Text reads:** my original report and the full visual packet, each in one complete view call with no truncation.
- **Images:** all 12 PNGs, viewed one at a time and all decoded: contact sheets 01–10 (55 whole screenshots) plus both full-size font panels.
- **Not used:** no shell, edits, delegation or parallel calls, and no other reviewer's report.

**Verdicts:** Correctness and scoped coverage are inherited from the textual review; the screenshots showed no new defect. The weather 凪ぐ versus feelings 和ぐ boundary and the exclusion of classical forms stay as qualified in the text.

| Article | Correctness | Scoped coverage | Rendered comprehensibility |
| --- | --- | --- | --- |
| `kanji\凪.md` | CLEAN (inherited) | CLEAN (inherited) | CLEAN |
| `words\凪.md` | CLEAN (inherited) | CLEAN (inherited) | CLEAN |
| `words\凪ぐ.md` | CLEAN (inherited) | CLEAN (inherited) | CLEAN |

**Findings:** None.
- **Fonts:** All 21 Han (今冷几凡凪凹化和夕心方日時朝止海着穏落静風) are visible in the Gothic, Mincho, Textbook and Brush rows, with no blank or replacement boxes.
  - 几 (U+51E0) shows an open frame with a hooked right leg. In the Mincho and Textbook rows it renders in a heavier fallback style. That is a style mismatch, not a readability problem.
  - It stays distinct from 凡 (dot inside), 凪 (止 inside), 風 (inner form) and 凹.
  - 凪ぐ, 朝凪 and 夕凪 are readable in every row.
- **Articles:**
  - Every section of all three articles is readable across the scroll captures, including the morning/evening words with kana and the full 凪ぐ conjugation list with kana.
  - The readings table scrolls sideways and shows a "Scroll sideways" hint. The "calm" cut off at the right edge (contact-02 #12, contact-03 #13–15) is fully visible in the right-scrolled captures (#16, #18). The left cells clipped in those right-scrolled captures appear in full in the left-scrolled ones.
  - All four kanji↔word link routes and both restored System Back positions appear (contact-07, -09, -10).
- **N1 deck and readings quiz:**
  - The N1 deck shows 119 cards, with 1 meaning, 1 drawing and 2 reading reviews available (contact-07 #42).
  - The なぎ quiz offers ぼこ/なぎ/なし/ならう. The なぐ quiz offers へこむ/なぐ/ならう/なえ. In each, only the target reading is correct; the others are not readings of 凪. Both were answered correctly and the done screen shows "2 of 2" (contact-01).
- **Meaning quiz:** The default N1 choices I saw were concave; sunken / calm seas; lull / yuzu citrus / commonplace; mediocre (contact-05 #27–28). Only one answer is defensible.
  - Chestnut (seed 613) and the All pool's "wind; style" appear only in the route JSON, not in any screenshot. Judged from those text labels, they are also unambiguous.
  - This partly resolves my original N1-fallback hypothesis, but only for these witnessed choices, not future random pools.
- **Drawing:** The six-stroke reference with numbers, the injected trace, the practice feedback and the give-up recall reference all appear (contact-01 #6, contact-02 #7–8).

**Optional (app wording, not article defects):**
- The practice drawing screen says both "this attempt is not graded" and "Graded by stroke shapes only."
- Text wrapping splits 凪/ぐ, 落/ち着く and (し/け) across lines. They remain readable.

**Limits:**
- **Supplied versus mine:** The successful native run, the 84+8 Paint probes and the route JSON are coordinator receipts. The Paint bitmaps were never exported, so I viewed none.
- **Image resolution:** I inspected screenshots only as downscaled contact-sheet tiles; only the two font panels were full size. The Again grade and the words' top header lines are not visible in any capture.
- **Device and handwriting:** This is an API 35 emulator, not a physical phone, and there was no native-speaker check. The strokes were injected and the recall was a give-up, so this is not human handwriting or offline MLKit recognition.
- **Not established:** fallback font identity, old-app behaviour, current-main integration, the public ZIP, CI, general release, the whole set, and measured learning effect.
