## Snapshot:
**Corrected:** `7ba55d7748c6716a7573516169a73d32c0ec1363`  
**Original:** `62d417f98be2f575ba851ecb4848923666a29fe8`  
**Committed files only.** F01 is resolved; no regression was established.

I have file tools but **no Git execution**. Commit identity, clean-worktree status and the nine-file correction scope therefore remain attributed to the author’s receipt.

## Scope:
Independent confirmation by **GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`**, without edits, commands or delegation.

Read my original report, the supplied actual two-page teaching diff, and both changed pages completely: `kanji\誌.md` and `words\貝.md`. Inspected `words\トップ.md`, `words\頂上.md`, `words\皮.md`, `words\馬鹿.md`, the relevant quiz-format rules, and complete source records for JMdict entries **2246880, 1085030, 1430220, 1483800 and 1601260**.

The source entry inventory contains **73 selected records representing 69 distinct entry IDs**, and the safeguard section records four direct pairs. Other reviewers’ reports and forbidden authoring materials were not inspected.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\誌.md` | CLEAN | CLEAN | CLEAN |
| `words\貝.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within this bounded scope.

## Findings:
**F01 — RESOLVED; originally Minor, correctness/quiz ambiguity.**

`words\貝.md:8` now directly excludes **トップ and 頂上**, while retaining **皮 and 馬鹿**. This implements the original remedy without relying on transitivity through トップ’s existing exclusions.

The explanation at `words\貝.md:34-40` preserves the primary **かい** lesson, distinguishes the separate **ばい** identity, and explicitly rejects both Japanese synonymy with the comparison words and the interpretation that **かい** names a spinning toy. The expanded citation at line 46 identifies the relevant entries accurately.

**Evidence:** `docs\n2-batch-sources\batch-21.json:4985-5050`, entry **2246880**, sense 2, records the spinning top. Its hiragana **ばい** reading has no spelling restriction and `kanaOnly: false`; the separate **バイ** reading has `kanaOnly: true`. Complete comparison records at lines **5963-6108** support トップ **1085030** and 頂上 **1430220**. Their actual article labels retain bare English *top*. `docs\content-format.md:85-98` establishes symmetric, nontransitive exclusions.

**Confidence:** High that the direct guards and explanatory distinctions resolve F01. Practical ambiguity of the complete multi-gloss labels remains **medium-confidence**, not an observed app failure. Failed English-dictionary fetches are not cited as evidence.

**Regressions:** None established. The retained 馬鹿 clam aside remains supported by entry **1601260**, sense 7, and explains an existing direct guard.

## Optional:
**Terminology improvement — optional, adopted and accepted.** `kanji\誌.md:39` now calls 持 and 時 “characters” rather than “words.” The supplied diff shows no accompanying metadata, reading or substantive meaning change. My original report contained no optional suggestions; this wording improvement is not being recast as an original defect.

No further optional polish or concrete review-guidance gap was identified.

## Limits:
This was a **bounded changed-passage confirmation**, not a renewed full-batch review. Unchanged reading rows, older linked passages and strokes were not re-audited.

No Git, validator, cumulative-audit or manifest-build execution was performed. The reported clean status, preservation checks, zero validator errors, 942-row audit and repeatable manifest builds remain **author-run checks**.

No exhaustive stroke-path inspection, runtime quiz testing or native-fluency certification was performed. No consequential linguistic claim remains unresolved in the changed passages.
