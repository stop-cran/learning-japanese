# Batch 084 凜: fine-detail addendum (凜 vs 凛 at panel size)

The crop resolves the question at panel size: 凜 and 凛 are clearly different characters there, in all four font families. I have moderately high confidence in that. The difference is subtle, though, and the crop doesn't cover smaller body text or a real phone, so I call this partly resolved overall, not a clean pass at every size. No teaching change is needed. My original visual report stands unchanged.

## Snapshot
- **Teaching content:** 030b144a6aeefc6fe77f76683219832db91bef4f.
- **Evidence:** HEAD a445a3f154afd5833fa99ba0c6abe13379402e1f; runtime 53b6819b22787a2517cd0ad14aa855d357cbc70a, version 74b87b47347b78c1.
- I didn't check Git or the hashes myself.

## Scope
- **Model and session:** Claude Opus 5.5 (claude-opus-5.5), continuing the original Batch 084 session. This is a narrow follow-up on one question, not a new blind review.
- **What I read:** one `view` call on `batch-084-visual-detail-crop.png`.
  - The image came back at about 632×760, matching the stated crop size, so this time it wasn't visibly downscaled.
  - I can't independently confirm that it was cut losslessly from the original panel-3 screenshot.
- **What the crop shows:** the left part of each of the four font rows (Gothic, Mincho, Textbook, Brush): 凜 凛 冫 稟 禾 示 准 冗 凹, then the start of 凜とした. The rest of each row is cut off.

## Verdicts

| Article | Correctness | Scoped coverage | Rendered comprehensibility |
|---|---|---|---|
| `kanji\凜.md` | CLEAN | CLEAN | CLEAN |
| `words\凜.md` | CLEAN | CLEAN | CLEAN |

These are unchanged from my visual report. CLEAN means I found no established defect within scope; it does not certify every detail.

## Findings
**Proven defects:** none.

What the crop shows, row by row:
- **凜 vs 凛:** in all four rows the first two characters look different.
  - 凜 has a 禾-type bottom: a long horizontal stroke, a central vertical, and two long diagonals sweeping out to the lower corners.
  - 凛 has a 示-type bottom: a short vertical with a hook and two small side strokes, which reads lighter and more compact.
  - Both have the two 冫 marks on the left and the 亠/回 block above.
  - The difference is in the lower quarter of glyphs about 40 px tall, so it is subtle but visible. The two do not collapse into the same character.
- **Same face in every row:** 凜, 凛, 冫 and 稟 look the same in all four rows. That fits the shared-fallback raster hashes. I can't name the fallback face from the pixels.
- **Other contrasts:** standalone 禾 and 示 are clearly different, and each row draws them in its own style (light in Textbook, heavy in Brush). 冫 shows as two marks. 稟 is recognisable. 准, 冗 and 凹 are clearly distinct.
- **Wrapping:** the wrapped た below the Textbook row is visible, and the text is retained.

## How this changes my earlier uncertainty
- **At font-panel size:** resolved, with moderately high confidence. My earlier "unable to decide" on panel 1 and "moderate" on panel 3 came from the downscaled full-frame images. The original-pixel crop removes that doubt at this size.
- **Overall:** still partly resolved, because:
  - body text at smaller sizes, other screen densities and a physical phone remain uncertified;
  - the subtle bottom difference may need a learner's attention at small sizes;
  - 凛 was never shown large, though the article notes explain the 禾/示 contrast in words.

## Optional
These are unchanged:
- C1 (spelling priority) remains optional.
- The app-level feedback line showing リン、きびしい, and the drawing-screen wording, remain optional observations.
- My original teaching suggestions remain optional.

## Limits
- The crop is not a new scale or device test, and it can't certify unseen body text, every fine stroke, or which typeface the fallback is.
- These remain outstanding and unverified:
  - phone and real native-font evidence;
  - ML Kit handwriting recognition and human handwriting;
  - larger, custom or random quiz pools (C3);
  - all publication and release steps;
  - learning effectiveness.
- No reads were denied. I made no edits and reread nothing.
