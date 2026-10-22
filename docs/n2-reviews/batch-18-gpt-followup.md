## Snapshot:

**Corrected:** `093d288e79ecdae3aa14ff6d1f00853c5bef6683`  
**Original:** `78ce7d7b97b863a034746ed2fcd43084233756db`

Committed files only, as identified by the supplied snapshot information. **No Git execution:** commit identity, clean-worktree status and exact eleven-file correction scope are author-verified, not independently Git-verified here.

## Scope:

GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Sequential, read-only confirmation; no commands, edits or delegation.

Read my original report, the complete supplied `n2-batch-18-fix.patch`, and all five changed pages in full: `words\群れ.md`, `words\耕す.md`, `words\脂.md`, `kanji\脂.md`, and `kanji\耕.md`.

Inspected comparison pages `words\学校.md`, `words\起す.md`, `words\打つ.md`, and `words\石油.md`; the relevant quiz-format rules; and complete source-packet records for 群れ, 起す, 打つ, 耕す and 石油. No other reviewer’s report or prohibited authoring material was inspected.

## Verdicts:

**Both original findings are resolved. No regression established within the changed passages.**

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `words\群れ.md` | CLEAN | CLEAN | CLEAN |
| `words\耕す.md` | CLEAN | CLEAN | CLEAN |
| `words\脂.md` | CLEAN | CLEAN | CLEAN |
| `kanji\脂.md` | CLEAN | CLEAN | CLEAN |
| `kanji\耕.md` | CLEAN | CLEAN | CLEAN |

## Findings:

**F001 — RESOLVED; original severity Medium; correctness / scoped coverage.**  
`words\群れ.md:8` now directly excludes 学校, preserving the definition and all previous exclusions. 学校’s displayed title remains unqualified “school”; JMdict **1247510**, sense 1, permits the collective “school” meaning for 群れ・むれ. The complete record at `docs\n2-batch-sources\batch-18.json:2970-3032` contains no blocking spelling or reading restriction. The direct declaration satisfies the symmetric exclusion contract without implying that 群れ means an educational institution. **Confidence: high.**

**F002 — RESOLVED; original severity Medium; correctness / scoped coverage.**  
`words\耕す.md:8` now directly excludes both 起す and 打つ. The committed source packet corroborates the relevant identities and applicable senses: **1223660**, 起す・おこす, sense 5, “to plough / plow / till” (`batch-18.json:3755-3952`); and **1408810**, 打つ・うつ, sense 9, “to till (soil)” (`batch-18.json:3954-4293`). Neither record restricts those senses away from the selected spelling or reading.

Both IDs appear in `words\耕す.md:50` and `kanji\耕.md:45`. The vocabulary correction preserves the agricultural explanation and conjugations; the kanji change is citation-only. **Confidence: high.**

**Regressions: none established.** The inspected pages agree with the supplied teaching diff. Definitions, reading rows and existing safeguards were not distorted to accommodate the corrections.

## Optional:

**Register clarification — optional, adopted and verified.** My original report proposed no optional changes. Nevertheless, the added qualification at `words\脂.md:39` and `kanji\脂.md:44` accurately reflects JMdict **1382830**, sense 2, marked “colloquial” in `batch-18.json:6236-6307`. It qualifies kerosene—not the primary oil/petroleum sense—and preserves the direct 油/石油 exclusions.

No outstanding optional change is required.

## Limits:

This is a **bounded changed-passage confirmation**, not a renewed full-batch review. No consequential linguistic claim remains unresolved within the inspected corrections. F002 now has committed source-packet corroboration rather than solely live-source evidence; I did not independently reproduce dictionary extraction or hashes.

No Git, validator, audit or manifest-build execution was performed. The reported clean worktree, zero validator errors, unchanged 808-row audit, baseline preservation and reproducible manifest/contentVersion checks remain **author-run checks**.

No exhaustive stroke-path inspection, runtime quiz testing or native-fluency certification was performed. CLEAN means no established actionable defect within this bounded scope.
