# Batch 095 font panels 1–2: serial repair report

**Result:** Both panels decode cleanly. Every scoped glyph is legible and the look-alike distinctions hold in all four fonts, so there is no regression. My original verdicts, findings, hypotheses, optional items and limits stand as written.

## Snapshot
- Signed content HEAD: 86966dc49fb3a22014aea0dac2b568bc7045e56d. Runtime and teaching content are unchanged.
- My execution-695 report and that run stay as they are; this repair doesn't change them.

## Scope
- **Model and session:** Claude Opus 5.5 (claude-opus-5.5), session ede78c28-e889-47b5-be0b-21533da61551.
- **Three serial reads:** I made exactly three reads, one view call per response, each waiting for the previous result:
  1. `control\batch-095-rendered-695-claude.md` (my own report).
  2. `n1-095-font-panel-1.png`, decoded at full scale.
  3. `n1-095-font-panel-2.png`, decoded at full scale.
- Nothing else was read.

## Verdicts (these two panels only)

| Panel | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Panel 1 | CLEAN | CLEAN | CLEAN |
| Panel 2 | CLEAN | CLEAN | CLEAN |

**Panel 1** shows 事, 亻, 件, 体, 倍, 刀, 刂, 分, 剖, 副, 医 and 口 in the Gothic, Mincho, Textbook and Brush rows.
- 剖 and 倍 share the 立-over-口 stack but differ by the right-hand 刂 versus the left-hand 亻.
- 剖 and 副 share the right-hand 刂 but have different left blocks: 立 over 口 versus 一, 口 and 田.
- The full-height blade form 刀 and the side form 刂 are clearly different shapes.
- 分 visibly contains 刀 under 八.
- 件 and 体 both have the left-hand 亻 and are told apart by their right-hand parts.
- All glyphs are legible in every row, including the heavier Brush row.

**Panel 2** shows 問, 学, 料, 析, 査, 検, 構, 牛, 物, 特, 理 and 生 in the same four rows.
- 料 and 析 are distinct: 米 with 斗 versus 木 with 斤.
- 検 and 構 are distinct right-hand parts beside the same 木.
- 物 and 特 share the left-hand 牛 but have different right-hand parts.
- 査 and 理 are distinct from the rest.
- Brush 構 is dense but legible.

**Fallback components.** The standalone 亻 and 刂 render in a plain fallback style rather than the row's typeface. In the Textbook row, 刂 looks somewhat heavier than the thin surrounding glyphs. The panel itself notes that "fallback families may coincide." Both components stay legible and recognisable, so this isn't a defect. It does slightly refine my earlier wording that they use "the same system fallback glyph in every font."

## Findings
- Proved defects: none.
- Regressions from these two images: none.
- Hypothesis H1 (the 解.md:50 citation line) stays a hypothesis, not a proven defect.

## Reconciliation
- My original execution-695 viewed panels 1 and 2 in one response. That overlap stays rejected for strict serial acceptance, and this repair doesn't make it compliant.
- This repair adds only these two fresh serial observations. It isn't new blind credit and doesn't redo the whole review.
- All other original observations stand as historical evidence, unchanged.
- The original findings, hypotheses (including H1), optional items (a)–(c) and limits are unchanged.

## Optional
None new.

## Limits
- I ran no tests and did no Git or upstream checks.
- The native receipts are inherited from the coordinator, not re-run by me.
- These are reference renderings: they're not evidence from a physical phone, of successful MLKit recognition, or of the latest app main.
- Seeing the glyphs rendered doesn't certify how well a learner tells them apart.
- This makes no claim about publication or a general release.
