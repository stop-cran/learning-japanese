## Snapshot: 5d465aa16c582cd0f6d372c857711e27aef158b0

Original snapshot: `e80e0c452d4cd55c9bee9a3ab125b40fc85be953`. **Committed files only; no Git execution.** Commit identity and cleanliness are author-provided, not independently Git-verified.

## Scope: gpt-6.1-sol; family gpt

Sequential, read-only confirmation without delegation. Read my original report, the actual `n2-batch-17-fix.patch`, and all four changed pages completely: `kanji\糸.md`, `kanji\綿.md`, `words\粒.md`, and `kanji\粒.md`.

Evidence inspected: `kanji\毛.md`, `words\玉.md`, `words\球.md`, the relevant quiz-format rules, pinned batch-12 毛 metadata, and complete relevant batch-17 dictionary records—including both newly retained 玉／たま and 球／たま records. No other reviewer’s report was inspected.

## Verdicts: four changed pages

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\糸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\綿.md` | CLEAN | CLEAN | CLEAN |
| `words\粒.md` | CLEAN | CLEAN | CLEAN |
| `kanji\粒.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within this bounded scope.

## Findings: original finding resolved; no established regressions

**GPT-17-01 — RESOLVED.** Formerly medium severity, correctness/quiz-answer ambiguity. `words\粒.md:8` now directly excludes **both 玉 and 球**, preserving the accurate “grain; bead; drop” label and teaching text. This implements both necessary pairwise protections without relying on transitivity.

**Evidence:** `docs\n2-batch-sources\batch-17.json:2672–3281` contains the complete applicable records for 玉／たま and 球／たま, JMdict **1240530**. Both retain sense 2, “bead (of sweat, dew, etc.); drop; droplet,” without spelling or reading restrictions preventing either pair. Entry **1552890** retains 粒／つぶ’s corresponding noun sense. The symmetric, nontransitive exclusion contract supports declaring both pairs on 粒 alone. The added citations at `words\粒.md:53` and `kanji\粒.md:45` correctly identify entry 1240530. **Confidence: high.**

**Additional 糸 correction — confirmed correct.** `kanji\糸.md:41` now explicitly identifies 毛’s **kun reading け**. Pinned `batch-12.json:22–46` records on モウ and kun け; batch-17 entries **1533860** and **1592710** support 毛糸／けいと and 絹糸’s retained readings. No pronunciation or reading-metadata regression was established. **Confidence: high.**

No consequential unresolved claim or new actionable regression was established in the four-page correction scope.

## Optional: adopted 綿 clarification accepted

**Optional — adopted and confirmed.** `kanji\綿.md:31` now places “usually written in kana” beside the cotton-plant sense alone. The introduction and Notes (`:20,40`) preserve padding coverage and the distinction in flag scope. This matches JMdict **1533340**, whose plant sense carries the usually-kana flag while its padding sense does not (`batch-17.json:5054–5135`). **Confidence: high.**

My original report contained no optional suggestions; this independently accepted clarification is not attributed to that report. No further optional polish is requested.

## Limits: bounded changed-passage review

This was not a new full-batch or eleven-file correction audit. No commands, Git checks, validator execution, runtime quiz testing, or exhaustive stroke-path review were performed; no native-fluency certification is implied. Author-reported validation, cumulative-audit, baseline-preservation and manifest-repeatability checks were not reproduced. Runtime exclusion behavior is assessed against the documented contract, not an executed app.
