## Snapshot:

**Corrected:** `fd607e1404e6b7891ff643d31b8a201eecc1b527`  
**Original:** `e02823f4e2628344b9ba4fd896fde675e6bce08d`

Committed files only, as identified by the supplied snapshots. **No Git execution:** commit identity, clean worktree and nine-file correction scope are recorded author assertions, not independently verified Git results.

## Scope:

GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Sequential, read-only confirmation; no commands, edits or delegation.

Read my original report, the complete supplied teaching diff, and both changed pages completely: `kanji\跡.md` and `words\軟らかい.md`. Inspected `words\もちもち.md`, `words\もこもこ.md`, `words\柔らかい.md`, the direct-exclusion declarations, relevant format rules, 跡 metadata, and complete relevant JMdict records for entries **1581330, 1605630, 1460730, 2403780 and 2104980** in `docs\n2-batch-sources\batch-22.json`. No other reviewer’s report was inspected.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\跡.md` | CLEAN | CLEAN | CLEAN |
| `words\軟らかい.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within this bounded scope.

## Findings:

**No established regression.** My original report contained no blocking findings; the two corrections below were not findings I originally raised.

- **跡 clarification — confirmed.** `kanji\跡.md:41` now distinguishes the displayed あしあと example from the valid alternative 足跡 そくせき. Entry **1581330**, including both exact reading records (`docs\n2-batch-sources\batch-22.json:4635–4788`), supports both pronunciations and restricts そくせき to **足跡**, not 足あと. No rarity flag is present, and the revision makes no comparative-frequency claim. The two reading rows at `kanji\跡.md:30–31` remain unchanged. **Confidence: high.**

- **軟らかい exclusions and comparison — confirmed.** `words\軟らかい.md:8` directly excludes both もちもち and もこもこ; their existing exclusions against 柔らかい did not transitively protect 軟らかい. The declarations now total **32 batch pairs**: 21 on 軟らかい and 11 on 超過. The new passage at `words\軟らかい.md:33`, with citations at line 43, preserves meaningful distinctions. Entry **2403780** records springy/doughy/elastic texture, consistent with the existing article’s soft-elastic texture and supple-skin teaching. Entry **2104980** separates “fluffy” from lumpy/uneven/bulging senses (`docs\n2-batch-sources\batch-22.json:8575–8687`). The paragraph explicitly avoids equating lumpiness with softness or asserting unrestricted interchangeability. **Confidence: high for the もちもち protection and sense distinctions; moderate for the conservative もこもこ protection.** The latter is defensible protection against a broad soft label, not proof that every fluffy or bulky object is soft.

- **O1 — optional, not adopted.** No correction to older 出 was required by my original conclusion. The supplied teaching diff does not change the full-pool fallback analysis: 日 shares three tags with 出, while 超 shares none, so the pinned algorithm’s single default remaining slot is filled ahead of 超. The lexical “exceed” overlap remains real; reduced pools, larger quizzes and other revisions remain limitations, not an established default defect.

The patch adds no unsupported rarity, register or usual-spelling labels. Nothing in this correction establishes a need to transfer あまり’s reading-restricted noun/suffix senses to あんまり.

## Optional:

None newly identified. Original **O1** remains nonblocking.

## Limits:

This was a **bounded changed-passage confirmation**, not a new full-batch review. I did not independently recount all source families, repeat the 983-row audit, or re-review unchanged teaching pages and all prior quiz comparisons.

No Git or validator execution, manifest rebuilding, exhaustive stroke-path review, runtime quiz testing or native-fluency certification was performed. The clean-state, validation, audit and repeated-build results—including contentVersion `087a40fcf7840aab`—remain **author-run checks**. No consequential linguistic claim remains unresolved within the confirmed scope.
