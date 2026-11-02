**Snapshot:** Coordinator-designated corrected signed snapshot `267bbbf`, compared with initial `33e9c9438c912bd701b05dd989114f23a85b08a9`. No uncommitted teaching changes specified. Full corrected SHA and signature verification were not independently available.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), same original GPT review session; bounded changed-passage confirmation, not a third independent review.

Fresh complete reads: my assigned original report, exact correction diff, all four current teaching files, supplemental `batch-007-guard-jmdict.xml`, and current `words\植木.md`. Inherited from my actual initial inspection: required instructions/contracts, raw character metadata, 30 complete dictionary families, 11 kanji comparisons, 13 word comparisons, confusable-word inventory and four relevant live dictionary lookups. The supplemental complete 植木 family brings inspected lexical evidence to **31 families**. No other review report was read.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\柚.md` | CLEAN | CLEAN | CLEAN |
| `kanji\椿.md` | CLEAN | CLEAN | CLEAN |
| `words\柚.md` | CLEAN | CLEAN | CLEAN |
| `words\椿.md` | CLEAN | CLEAN | CLEAN |

**Findings:** No new actionable defect or regression established. **Accepted** the bounded correction.

**Disposition: resolved — conservative contextual quiz safeguard.**  
**Facet/location:** Quiz ambiguity; `words\柚.md:8` and `words\椿.md:8`. Both now directly exclude 植木 while preserving all previous exclusions. JMdict entry **1587970**, inspected completely, supports 植木／うえき as “garden plant/tree” and “potted plant”; 植え木 is search-only. Both new articles explicitly illustrate garden contexts, so these direct guards reasonably prevent contextual English-to-Japanese ambiguity. They do not assert unrestricted synonymy or that every yuzu or camellia is cultivated.

**Severity:** Minor potential quiz ambiguity, now guarded; no medium-level teaching defect established by this confirmation. **Confidence:** High that the correction supplies both direct protections without changing teaching meaning.

My original review established **no mandatory additional exclusion**. I retain that narrower assessment: accepting this conservative safeguard does not retrospectively establish that its absence was necessarily defective. There is no remaining consequential disagreement requiring a teaching change.

The supplied diff changes only those two exclusion lists and corresponding manifest hashes/content version. Fresh teaching reads show no changes to bodies, examples, full reading metadata, ordering or curated selections, and no new exclusion/distractor conflict.

**Optional:** None required. Chinese-mahogany coverage, additional 山茶／山茶花 context and historical/phonetic derivation remain nonblocking expansions, not prerequisites for this bounded lesson.

**Limits:** Snapshot/signature and clean-worktree status are coordinator-supplied. Manifest hashes were inspected in the diff, not independently recomputed. No new live lookup, validation, app execution, native-speaker assessment or physical-phone testing was performed.

Historical initial oversized/truncated reads were recovered; the initial Git-administrative verification failed and remains a disclosed limitation. No such paths were attempted during confirmation. All required fresh reads completed without truncation. Each current tool result returned before the next invocation; no overlap was observed, although tool-internal execution is not independently observable. No files were written.
