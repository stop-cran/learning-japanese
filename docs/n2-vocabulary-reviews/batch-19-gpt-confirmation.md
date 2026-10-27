## Snapshot: 976c03d8607af5db578c9ea79ba25650df59f42e

Committed correction snapshot designated by the receipt; parent `bec5240238e832cc953cbb1f04dbaaf3609a830c`. **Commit identity, cleanliness and hash checks are author-reported:** I have file tools, not Git execution, and did not independently execute Git or verify hashes.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Sequential, read-only confirmation by the original reviewer, without delegation or edits. I read my original report, the correction receipt and complete supplied patch, both changed articles in full, `words\道具.md`, the relevant `words\器具.md` declaration, the required instructions, and `docs\content-format.md:18–119`.

I inspected complete families **1220810, 1454180, 1119210 and 2845313**, plus the appended `correctionEvidence`, in `docs\n2-vocabulary-batch-sources\batch-19.json`. No other reviewer’s output or prohibited authoring/review material was consulted. This confirms the two corrections and checks their context for regressions; it is not a fresh whole-batch audit.

## Verdicts: both corrections confirmed

| Reviewed surface | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `words\機械.md` — direct exclusion correction and scoped apparatus reuse | CLEAN | CLEAN | CLEAN |
| `words\基地.md` — ベース clarification and citation | CLEAN | CLEAN | CLEAN |
| Packet additions — `correctionEvidence` | CLEAN | CLEAN | CLEAN |

The supplied patch preserves existing exclusion entries and their order while **appending 道具** to 機械’s list; the corrected list is not byte-for-byte unchanged. IDs, primary readings, titles, written-kanji metadata and easier levels are unchanged in the two-card diff. 機械 remains N3.

The packet accurately records the addition in `baselineQuizExclusionAdditions`. Earlier declarations and preservation statements remain historical authored-snapshot evidence; the correction is appended, not backdated.

## Findings: N2B19-GPT-01 resolved; no actionable regressions

**N2B19-GPT-01 — RESOLVED.** Original severity: Minor; facet: correctness, quiz-label ambiguity.

`words\機械.md:9` now declares `quiz_exclusions: [装置, 道具]`, implementing the requested direct guard without removing 装置. The actual titles remain **“machine; mechanism”** and **“tool; implement”** (`words\道具.md:5`). The apparatus use explicitly taught at `words\機械.md:35–43` supports the exclusion: complete **1220810:2** gives instrument/appliance/apparatus, “often 器械,” without a spelling restriction; complete **1454180:1** gives tool/implement/instrument/utensil/apparatus/device.

Evidence: `docs\n2-vocabulary-batch-sources\batch-19.json:750–827,10517–10606`; `words\道具.md:15–17`; exclusion semantics in `docs\content-format.md:83–105`. One declaration protects the pair symmetrically, including between other choices in both meaning-quiz directions. The existing 器具 guards are not relied upon transitively. This does not assert unrestricted Japanese substitution. **No further remedy is required. Confidence: high.** The apparatus sentence remains unchanged and was not the defect.

The clarification at `words\基地.md:29,35` introduces no regression. Complete **1119210** supports ベース’s basis and operating/military-base uses; separate **2845313** supports musical bass (`batch-19.json:3729–3813,14708–14787`). The revised wording plainly distinguishes the separate word and cites it without assigning its meanings an N2 level. **Confidence: high.**

## Optional: none outstanding

My original report contained no optional hypotheses to reconcile. The 基地 wording change is an adopted **nonblocking clarity improvement**, not a newly established defect. No additional examples, stylistic normalization or navigation expansion is required for this confirmation.

## Limits: file-based provenance and unexecuted app behavior

No independent Git/hash verification, app quiz draw, new dictionary extraction or public-source retrieval was performed in this confirmation. Lexical conclusions use the complete supplied families; appended author observations are not independent proof.

The unchanged mappings, other articles and full quiz pool were not re-audited. No actionable defect or consequential unresolved linguistic claim remains in this bounded scope. **CLEAN is not exhaustive correctness, measured frequency or native-speaker certification.**
