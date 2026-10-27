## Snapshot

**CLEAN for this bounded follow-up.** Model: **GPT-6.1 Sol** (`gpt-6.1-sol`, GPT family).

The author’s snapshot identifies commit `dd4d6de435d91c2ab362a89660d97b173a9cf8d1` and reports a clean worktree at freeze. The supplied patch shows one metadata line changed.

## Scope

Exactly **one file and two new direct pairs**: `一応/くらい` and `一応/ほど`, declared at `words\一応.md:9`.

Independently inspected the three requested cards, `docs\content-format.md:88-116`, and the relevant batch JSON evidence, including complete entries **1161170, 1154340 and 1436510**. The previously confirmed twelve-file correction was not reopened.

## Verdicts

| Facet | Status | Assessment |
|---|---|---|
| Correctness | **CLEAN** | Both pairs address defensible context-free English-answer ambiguity. |
| Scoped coverage | **CLEAN** | Both assigned pairs are explicitly declared. No reciprocal declarations or unrelated additions are required. |
| Comprehensibility | **CLEAN** | Titles and explanatory prose remain intact; the guards do not imply grammatical interchangeability. |
| Visible regressions | **CLEAN** | The patch preserves all eight existing exclusions and adds two distinct, existing card IDs without changing other metadata or teaching content. |

## Findings

**No defects established.**

`words\一応.md:4` includes **“roughly”**; `words\くらい.md:4` and `words\ほど.md:4` include **“approximately.”** This is substantive English-gloss overlap, not merely shared subject matter. Entry **1161170**, sense 1, supports “more or less” and “roughly”; **1154340**, sense 1, and **1436510**, sense 6, support “approximately.”

For **each pair**, a learner seeing those titles without a sentence can reasonably recognize “roughly” and “approximately” as competing answers. The additional, nonshared title senses do not eliminate that overlap. This meets the criterion at `docs\content-format.md:95-99`.

The Japanese distinction remains important: `words\一応.md:16-25` describes qualified adequacy, provisionality and precaution, expressly rejecting percentage quantification. `words\くらい.md:16-22` and `words\ほど.md:15-27` explain quantity/degree constructions. Neither guard asserts that 一応 can replace a numerical suffix; different syntax also does not resolve the displayed English-answer ambiguity.

## Optional

None. No retitling or additional pair expansion is warranted by this bounded review.

## Limits

**UNVERIFIED — Git/hash provenance and runtime behavior.** No shell or Git was executed, and hashes could not be recomputed. Commit identity, clean-at-freeze status and recorded SHA-256 values remain **author-verified receipt claims**, not independently reproduced checks. The card contents and supplied patch were independently read.

No edits, agents, other-model reports, review ledger, separate author notes or other private data were used. Acceptance here is limited to the two guards—not a fresh full-batch review or native-language certification.
