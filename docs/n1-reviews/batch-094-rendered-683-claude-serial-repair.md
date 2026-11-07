# Batch 094 font panels 1–2 repair: no regression, original findings unchanged

Fresh serial reads of font panels 1 and 2 show every character legible and every distinction this review needs readable in all four fonts. They establish no regression. My original findings stay unchanged, including the unresolved 削る/縮める exclusion.

## Snapshot
- Signed content HEAD 577eb626dafec18e5bbd8d9eb257a75b1dac775e. Runtime and teaching snapshot (4089e881) unchanged. Native receipts are inherited, not re-run.

## Scope
- **Model and session:** claude-opus-5.5, original session edf22897-9f87-4a3b-b20f-4c2fd839013a.
- **Reads:** exactly three, one view call per response, each waiting for the previous result:
  1. `control\batch-094-rendered-683-claude.md`, my own complete 683 report, read in full.
  2. `n1-094-font-panel-1.png`, freshly decoded.
  3. `n1-094-font-panel-2.png`, freshly decoded.
- Nothing else was read.

## Verdicts (panels 1 and 2 only)

| Panel | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Panel 1: 一 不 中 予 余 刀 刂 切 刑 判 削 前 | CLEAN | CLEAN | CLEAN |
| Panel 2: 加 取 外 掃 文 斫 日 曜 止 氵 消 添 | CLEAN | CLEAN | CLEAN |

**What the panels show:**
- **Coverage:** each panel shows 12 characters in Gothic, Mincho, Textbook and Brush. No row has blank boxes or tofu.
- **Blade forms:**
  - 刀 (standalone) and 刂 (the right-side blade form) are clearly different in every font.
  - 切 correctly shows 刀, not 刂.
  - 刑, 判, 削 and 前 all show the right-side 刂, and their left parts (开, 半, 肖, the top of 前) stay distinguishable.
- **Side forms:** 消 shows a left-side 氵 next to the 肖 shape, so it stays distinct from 削.
- **Source-only 斫:** legible as 石 + 斤 in all four fonts.
- **Lookalikes:** 日 vs 曜, 余 vs 予 and 掃 vs 添 are distinct.

## Findings
- **None for panels 1–2.** No regression in anything the original report concluded.
- **Original finding stays open:** the Low / NEEDS FIX finding that `words\削る.md:9` needs 縮める added to its quiz exclusions remains unresolved, because no edit has occurred.

## Reconciliation
- **Execution 683 overlap:** the overlapping read of panels 1 and 2 in execution 683 is rejected for strict serial acceptance, permanently. It is not relabelled compliant.
- **What this repair adds:** only two fresh serial observations, for panels 1 and 2. It adds nothing to the original execution, gives no new blind credit, and does not re-review the whole batch.
- **Reads after the overlap:** the serial reads after the overlap (panels 3–5 and sheets 01–20) remain historical evidence, as stated.
- **Everything else unchanged:** all earlier findings, the 除く/取り出す hypothesis, the optional items and the limits stand as written.

## Optional
- None new.

## Limits
- **Font fallback, refined:** my original report said only the Textbook font falls back for 斫, 刂, 氵 and 阝. On these two panels:
  - 斫 also looks like a fallback (Gothic-like) glyph in the Mincho and Brush rows.
  - 刂 and 氵 also look like fallbacks in the Brush row.
  - The glyphs are still correct and recognisable, so this is a disclosure, not a defect.
- **Not covered:** these are static font panels. They give no evidence about the article screens, native font metrics beyond what is rendered, handwriting or ML Kit recognition, a physical phone, the latest app main, tests, upstream sources, signatures, or publication.
