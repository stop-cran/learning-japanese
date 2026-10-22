## Snapshot: c81161be3a918430076da745d079fca534a520e8; committed files only

**The added direct exclusion is justified. No actionable defect remains in this correction scope.**

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Reviewed read-only and sequentially, without delegation. Read my preserved `docs\n2-reviews\batch-11-gpt-followup.md`, the complete supplied `n2-batch-11-final-correction.diff`, both `words\極める.md` and `words\選ぶ.md` fully, the complete entry **1254180** record in `docs\n2-batch-sources\batch-11.json:2548–2746`, and the applicable exclusion rules in `docs\content-format.md:85–100`.

No assigned material was omitted. Unchanged batch pages, unrelated candidate pairs, other reviewers’ reports, contributor-documentation changes, and the manifest were not reviewed.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `words\極める.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within this assigned scope, not exhaustive truth or linguistic certification.

## Findings:

**B11-GPT-R4 — RESOLVED; Moderate; correctness/quiz integrity; `words\極める.md:8`.**

Adding **選ぶ** directly to `quiz_exclusions` addresses a genuine answer ambiguity. JMdict entry **1254180**, sense 1, includes **“to choose”**, permits the spelling **極める**, and permits **きめる** without spelling restrictions or a kana-only constraint. This matches `words\選ぶ.md:5`’s actual answer label, **choose**. The separate kana-only **キメる** alternate is not needed to establish the pair.

Thus, a reading-free Japanese-to-English prompt showing **極める** can admit **choose**, even though this article teaches **きわめる**. Reverse choices containing **極める (きわめる)** are more disambiguated; equal ambiguity in every reverse presentation is not established. The symmetric direct exclusion nevertheless protects both directions under the documented contract. The existing exclusion with 決める cannot substitute for this pair because exclusions are not transitive.

The diff changes only that exclusion list. The article’s primary **きわめる** reading, extreme/limit meaning, prose, and other lexical metadata remain intact. No regression was established. My prior “no remaining finding” conclusion missed this additional pair and is superseded accordingly. **Confidence: high.**

## Optional:

None.

## Limits:

File tools were available, but Git execution was not. Snapshot identity, cleanliness, the exact seven-file commit scope, zero validator errors, and manifest determinism are author-reported—not independently verified here.

No app execution or validator run was performed. No consequential linguistic claim remains unresolved within the changed scope.
