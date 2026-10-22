## Snapshot:

**New:** `31860fc0aba7f7110b8e31e8787828e2bcc85a15`  
**Previous:** `093d288e79ecdae3aa14ff6d1f00853c5bef6683`

Committed files only, as identified by the supplied snapshot information. **No Git execution:** commit identity and worktree cleanliness are author-verified, not independently Git-verified here.

## Scope:

GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Sequential, read-only confirmation without commands, edits or delegation.

Read my archived first confirmation, the complete supplied two-page diff, both changed pages completely (`words\耕す.md`, `kanji\耕.md`), `words\作る.md`, the complete 作る・つくる source record **1597890**, and the relevant symmetric, pairwise quiz-exclusion rules. No other reviewer’s report was inspected.

## Verdicts:

**The additional safeguard resolves the demonstrated overlap; no regression established.**

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `words\耕す.md` | CLEAN | CLEAN | CLEAN |
| `kanji\耕.md` | CLEAN | CLEAN | CLEAN |

## Findings:

**Additional 耕す/作る overlap — RESOLVED.**  
`words\耕す.md:8` now directly excludes 作る while retaining 起す and 打つ. The complete record at `docs\n2-batch-sources\batch-18.json:4295-4570`, JMdict **1597890**, gives 作る・つくる sense 4 as **“to till”**, with no spelling or reading restriction excluding this pair. 作る’s beginner label “make; prepare” (`words\作る.md:5`) does not erase that applicable sense. The direct exclusion therefore prevents a defensible alternative to “till; plough” under the documented exclusion-aware quiz contract (`docs\content-format.md:85-98`). **Confidence: high.**

**Citations — confirmed.**  
Entry **1597890** is included at `words\耕す.md:50` and `kanji\耕.md:45`. The kanji change is citation-only. The supplied diff and complete pages preserve the definitions, examples, readings, conjugations and previous safeguards. **No consequential regression established; confidence: high.**

**Prior disposition:** F002 remains **RESOLVED** for its original 起す/打つ pairs. My previous CLEAN scoped-coverage verdict did not identify the additional 作る overlap; that was a missed gap, now corrected. The present CLEAN verdict includes this newly verified safeguard.

## Optional:

None.

## Limits:

This is a bounded confirmation of the additional exclusion and citations, not a renewed batch review or exhaustive synonymy proof. The author’s broader gloss sweep was not independently reproduced.

No Git, validator, audit or manifest-build execution was performed. Reported cleanliness, scope, counts, preservation checks and deterministic manifest remain author-run results. No runtime quiz testing, exhaustive stroke-path inspection or native-fluency certification was performed. The safeguard’s effect is confirmed against the documented exclusion-aware contract, not observed in a running app.

CLEAN means no established actionable defect within this narrow scope.
