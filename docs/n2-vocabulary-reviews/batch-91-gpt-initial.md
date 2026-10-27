## Snapshot:

**Frozen commit:** `28ac612d4bd09064cc9c102fa6abd0d84c168434`  
**Parent:** `df3e8c4c53a7c5b8a962ccc20c5251e6cb9e39c6`

The review concerns the supplied **committed-content snapshot**, not uncommitted changes. Commit identity, clean state, addition counts and hashes are author-run receipts—not independently executed reviewer checks.

## Scope:

**Model:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Independent, read-only review; no agents, delegation, edits, shell execution or concurrent calls. Used **35 sequential tool calls**.

Read completely: all supplied instructions and contract excerpts, twelve raw mappings, twelve principal families, sixteen component records, 135 comparison labels, twelve new articles, the full 算 article, its exact patch, and all twelve public wrappers. Applied the relevant modern headings/readings, including **わん**, not the historical **もい／まり** entries.

Additional inspection comprised **18 complete comparison-family records**, including incidental records—not the entire 202-family/415-sense union—and these **eight complete older articles**: だいぶ, 沸く, 別, 割る, 割れる, 等分, 湯飲み and 割合. Also read `docs\jlpt-levels.md`, inspected the introductory portion of `docs\confusable-words.md`, searched that contract for the assigned vocabulary, and checked component-card metadata under `kanji\`. Other partial family records were not counted as complete reads.

Prohibited ledgers, rationale files, scripts, TSV author-note columns and other reviewer reports were not accessed. **One missing quiz safeguard is established; one possible excessive safeguard remains unresolved.**

## Verdicts:

**CLEAN** means no actionable defect established within the actual review scope, not exhaustive or native-speaker certification.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
| --- | --- | --- | --- | --- | --- |
| N2:1802 分かれる | `words\分かれる.md` | NEEDS FIX | CLEAN | CLEAN | F1: missing direct exclusion with 別. Definitions and intransitive constructions are sound. |
| N2:1803 若々しい | `words\若々しい.md` | CLEAN | CLEAN | CLEAN | Youthful impression, adjective forms and qualified literary recognition are distinguished. |
| N2:1804 湧く | `words\湧く.md` | CLEAN | CLEAN | CLEAN | Correctly separates emerging/welling uses from the source’s mixed-in 沸く glosses. |
| N2:1805 詫びる | `words\詫びる.md` | CLEAN | CLEAN | CLEAN | を／に／で attachment and omitted apology reason are explained correctly. |
| N2:1806 和服 | `words\和服.md` | CLEAN | CLEAN | CLEAN | Traditional style is distinguished from manufacturing location and nationality. |
| N2:1807 わりあいに | `words\割合に.md` | UNVERIFIED | CLEAN | CLEAN | Mapping and prose are clean; the だいぶ exclusion remains unresolved under U1. |
| N2:1808 割算 | `words\割り算.md` | CLEAN | CLEAN | CLEAN | Source spelling and reading are explicitly taught; mixed reading and arithmetic restrictions are clear. |
| N2:1809 割と | `words\割と.md` | UNVERIFIED | CLEAN | CLEAN | Comparative/degree explanation is sound; the だいぶ exclusion remains unresolved under U1. |
| N2:1810 割引 | `words\割引.md` | CLEAN | CLEAN | CLEAN | Correct discount arithmetic; separately sourced する use and additional recognition are qualified. |
| N2:1811 椀 | `words\椀.md` | CLEAN | CLEAN | CLEAN | Bowl and counter uses are taught without imposing an absolute material boundary. |
| N2:1812 碗 | `words\碗.md` | CLEAN | CLEAN | CLEAN | Applicable わん identity, counter use and spelling qualifications are preserved. |
| N2:1813 ワンピース | `words\ワンピース.md` | CLEAN | CLEAN | CLEAN | Dress and one-piece construction are distinguished; の attachment is demonstrated. |

**Mappings — CLEAN within the supplied lexical evidence.** All twelve source readings and applicable identities are taught. The kana-to-kanji normalization わりあいに → 割合に and spelling normalization 割算 → 割り算 are explicit and compatible with the complete families. The erroneous transitive implication of “dispense” is not imported into 分かれる; the boiling/heating glosses attached to 湧く are explicitly separated from its applicable senses. Additional dictionary recognition does not independently establish N2 status for every sense.

**Baseline and kanji preservation — CLEAN for the supplied related patch; UNVERIFIED repository-wide.** The exact 算 patch adds the linked division example and entry number `1606880` only. It preserves all metadata and unrelated teaching. The supplied receipts report twelve physical additions, no reuse and no other related-content edits; I could not independently certify that Git-level inventory or easier-level preservation throughout the repository.

**Components — CLEAN in inspected scope.** Every written primary Han character is included in metadata. Existing primary component cards—分, 若, 和, 服, 割, 合, 算 and 引—were located and substantively linked. No cards or unsupported readings were invented for the absent components.

**Reciprocity — CLEAN.** `words\割り算.md:28–32` links 算, and `kanji\算.md:42` links 割り算 with the compatible わりざん explanation.

## Findings:

**F1 — Medium; correctness, quiz exclusions; `words\分かれる.md:4,9,24`.**

The exclusion list omits **別**, whose actual older title is **“separate; different”** (`words\別.md:4`). That older article explicitly teaches “separate” and “different” at lines 15–20. 分かれる’s title includes **“separate”**, and its body also teaches opinions differing. These labels therefore permit a defensible competing answer; the adjective/verb distinction is not expressed sufficiently in the displayed English labels to make the pair safe.

**Minimal remedy:** add `別` to 分かれる’s `quiz_exclusions`. No reciprocal edit is required. Existing protection involving 別々 does not protect this pair because exclusions are nontransitive.

**Evidence:** complete JMdict families `1606600`, senses 2–3, and `1509430`, especially sense 2; the complete older 別 body; `docs\content-format.md:85–99`. Neither card declares this direct pair, and their titles are not exactly equal. **Confidence: high.**

**U1 — Unresolved, potentially minor; correctness, quiz exclusions; `words\割合に.md:9`; `words\割と.md:9`.**

Both cards exclude **だいぶ**. The complete older article teaches the 大分 degree adverb **“considerably”**, including substantial improvement or distance (`words\だいぶ.md:15–23,31–33`), whereas the new explanations emphasize relative assessment. That distinction raises a concrete possibility of unnecessary exclusion, particularly for 割合に.

However, the complete comparison evidence also contains **大部**, entry `1414830`, with reading だいぶ and a secondary adverbial gloss **“fairly”**. 割と and its cross-referenced 割に likewise include “fairly.” The matching reading and English gloss cannot simply be ignored—but neither alone establishes the contemporary applicability and title-level equivalence needed for these particular cards. The retrieved 大部 page’s applicable **たいぶ／だいぶ** heading supplied noun senses, not verification of that degree-adverb equivalence.

**Minimal resolution:** establish the directly applicable contemporary sense and quiz-label overlap for each pair separately. Retain a pair if supported; otherwise remove only that unsupported declaration. **No removal is certified by this review.**

**Evidence:** complete families `1414920`, `1414830`, `1612360`, `1606810`, `1983690` and `1606930`; the complete older だいぶ and 割合 bodies; the supplied 割合 adverb wrapper; [Kotobank’s 大部 heading](https://kotobank.jp/word/大部-558226). **Confidence: high about the evidence gap; insufficient to classify either declaration as erroneous.**

## Optional:

None.

## Limits:

**The quiz-exclusion conclusion is partial:** U1 remained unresolved when the 35-call bound was reached. It is not marked CLEAN.

File tools cannot independently execute **Git, hashes or the app**. I did not verify repository cleanliness, parentage, manifest integrity, importer behavior, or that additional filesystem reads exactly match the frozen commit. The supplied patch supports content-level preservation, not independent Git certification.

The 202 complete families are comparison records, **not 202 independent authorities**. I read selected complete families and eight of the 83 available older bodies, not all of them. Several live lookups returned irrelevant headings, attribution-only content, inaccessible output or an error; those results were not treated as linguistic verification. The supplied public wrappers remain evidence from one authority, and community-list membership is not an official JLPT assignment.
