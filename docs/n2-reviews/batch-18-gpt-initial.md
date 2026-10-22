## Snapshot: 78ce7d7b97b863a034746ed2fcd43084233756db; committed files only

Baseline: `c3f3b0aebc7905e7a48421cd5230a1876b951d5d`. The frozen snapshot records `clean: true` and a 51-file scope. **I have file tools, not Git execution:** committed-only status and scope identification therefore rely on that snapshot and the supplied scope verification, not an independent Git check.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Reviewed sequentially, without delegation or edits. Read all 21 assigned teaching pages completely, the required instructions, `docs\content-format.md:18-109`, and the complete batch metadata and selected lexical records.

Inspected the added links in their surrounding passages: `words\練習.md:23`, `訓練.md:29`, `成績.md:25`, `缶.md:15`, `署名.md:24`, `羽.md:27`, `肌.md:25`, `肩.md:24`, `胃.md:25`, and `胸.md:25`. No actionable link defect established; their unchanged lexical content did not receive a comprehensive new review.

Checked all **45 curated kanji distractor assignments**, useful vocabulary links, relevant vocabulary labels and direct exclusions, and the older two-distractor kanji cards for newly activated direct-synonym risks.

Omitted deliberately: `docs\n2-authoring-notes.md`, `docs\n2-review.md`, `REVIEW.md`, `docs\n2-reviews\`, session authoring inputs, author-check receipts, and other reviewers’ outputs. Generated stroke files were not inspected; exhaustive drawing-path review was not assigned.

## Verdicts: two pages need quiz-exclusion fixes

The kanji metadata matches the pinned records, and all 34 reading rows have lexical examples realizing the indicated readings. The two NEEDS FIX verdicts below concern quiz safety, not incorrect Japanese examples.

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\編.md` | CLEAN | CLEAN | CLEAN |
| `kanji\練.md` | CLEAN | CLEAN | CLEAN |
| `kanji\績.md` | CLEAN | CLEAN | CLEAN |
| `kanji\缶.md` | CLEAN | CLEAN | CLEAN |
| `kanji\署.md` | CLEAN | CLEAN | CLEAN |
| `kanji\群.md` | CLEAN | CLEAN | CLEAN |
| `kanji\羽.md` | CLEAN | CLEAN | CLEAN |
| `kanji\翌.md` | CLEAN | CLEAN | CLEAN |
| `kanji\耕.md` | CLEAN | CLEAN | CLEAN |
| `kanji\肌.md` | CLEAN | CLEAN | CLEAN |
| `kanji\肩.md` | CLEAN | CLEAN | CLEAN |
| `kanji\肯.md` | CLEAN | CLEAN | CLEAN |
| `kanji\胃.md` | CLEAN | CLEAN | CLEAN |
| `kanji\胸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\脂.md` | CLEAN | CLEAN | CLEAN |
| `words\編む.md` | CLEAN | CLEAN | CLEAN |
| `words\群れ.md` | NEEDS FIX | NEEDS FIX | CLEAN |
| `words\翌日.md` | CLEAN | CLEAN | CLEAN |
| `words\耕す.md` | NEEDS FIX | NEEDS FIX | CLEAN |
| `words\肯定.md` | CLEAN | CLEAN | CLEAN |
| `words\脂.md` | CLEAN | CLEAN | CLEAN |

## Findings:

**F001 — Medium; correctness / scoped coverage — `words\群れ.md:4-8`; comparison `words\学校.md:5-10`.**  
The exclusions omit **学校**, whose answer label is the unqualified English **“school.”** 群れ has an applicable *school* sense for grouped animals. Consequently, an English-to-Japanese question displaying “school” can admit both 学校 and 群れ if both are offered. This is an English-label homograph collision—not a claim that 群れ denotes an educational institution.

**Minimal remedy:** add `学校` to 群れ’s `quiz_exclusions`. One declaration suffices because exclusions are symmetric.

**Exact evidence:** `docs\n2-batch-sources\batch-18.json:2968-3030`, JMdict **1247510**, 群れ・むれ, sense 1, includes “school” without spelling or reading restrictions. 学校’s complete header contains no reciprocal exclusion. `docs\content-format.md:82-104` establishes the context-free title labels and pairwise exclusion mechanism. **Confidence: high.**

**F002 — Medium; correctness / scoped coverage — `words\耕す.md:4-8`; comparisons `words\起す.md:2-9` and `words\打つ.md:2-9`.**  
耕す has no direct exclusions for **起す** or **打つ**, although both existing written words have applicable tillage senses. Their displayed labels—“wake someone up” and “hit; strike”—do not eliminate their other lexical meanings. In an English-to-Japanese question asking **“till; plough,”** either can therefore be a defensible alternative to 耕す. Neither older header declares a reciprocal exclusion.

**Minimal remedy:** add `quiz_exclusions: [起す, 打つ]` to 耕す. This does not require expanding the older articles’ teaching text.

**Exact evidence:** the pinned 耕す record is JMdict **1280950**, `docs\n2-batch-sources\batch-18.json:3827-3884`. Independently fetched evidence:
- [JapanDict/JMdict 1223660](https://www.japandict.com/%E8%B5%B7%E3%81%99#entry-1223660), **起す・おこす**, sense 5: “to plough, to plow, to till.” The [Jisho JMdict response](https://jisho.org/api/v1/search/words?keyword=%E8%B5%B7%E3%81%99) lists both 起こす and 起す and no restriction on this sense.
- [Jisho/JMdict](https://jisho.org/api/v1/search/words?keyword=%E6%89%93%E3%81%A4), **打つ・うつ**, entry **1408810**, sense 9: “to till (soil),” with no restriction.

These entries were fetched on **2026-10-22**. **Confidence: high.**

## Optional: none

## Limits:

No Git status, baseline diff, repository validation, or live-app execution was available. Quiz findings establish semantic ambiguity when the pairs are offered, not observed selection frequency; low candidate scores are not safeguards.

The pinned evidence is selected, not complete JMdict. Omitted records were not treated as dictionary absence; F002 uses successful external lookups of the actual headwords, readings and senses. Live dictionary pages are not independently hash-pinned to the repository’s download.

Nanori, obsolete four-level JLPT assignments, exhaustive historical analysis, unchanged-page correctness outside the linked passages, and generated stroke-path correctness remain outside this review. **CLEAN means no established actionable defect within the assigned scope—not exhaustive truth or native-speaker certification.**
