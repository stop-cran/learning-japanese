## Snapshot: `b002896e6b26b58dd7bd5b73194d73ec834c8997` — committed content only, per frozen receipt

Parent: `f574c3a900041cbc460fdfa1306e54204ca24220`.

The frozen receipt identifies this as clean committed content. **Only file tools were available; no Git execution was available.** I therefore cannot independently verify the commit tree, checkout cleanliness, or correspondence of the supplied files and patch to that commit.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`; family `gpt`)

Read-only, sequential review without delegation or edits. I read all nineteen new articles completely, all twenty complete principal dictionary families, mappings **N2:342–N2:361**, the entire eighteen-file related patch, and its changed passages in context. I assessed the narrowly claimed reuse of 乾燥, component evidence, relevant comparison families/cards, and selected public dictionary entries.

**Result: four actionable quiz-choice issues.** No actionable defect was established in the source mappings, scoped lexical coverage, or article comprehensibility. Unchanged teaching in related files is not comprehensively recertified. Comparison evidence was examined selectively; this was not an exhaustive review of every supplied comparison family or every repository word.

## Verdicts

Correctness includes quiz-answer correctness. The four **NEEDS FIX** judgments below concern missing exclusions, not an established error in the articles’ lexical explanations. **CLEAN** means no actionable defect established within the assigned scope.

All articles below are under `words\`. Sense numbers refer to the supplied principal JMdict families.

| Article | Source row; source reading; selected senses | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| 代わる | N2:342 **代る → 代わる**; かわる; 1–3 | CLEAN | CLEAN | CLEAN |
| 間隔 | N2:343; かんかく; 1–2 | CLEAN | CLEAN | CLEAN |
| 換気 | N2:344; かんき; 1 | NEEDS FIX | CLEAN | CLEAN |
| 感激 | N2:345; かんげき; 1 | NEEDS FIX | CLEAN | CLEAN |
| 関西 | N2:346; かんさい; 1–2 | CLEAN | CLEAN | CLEAN |
| 鑑賞 | N2:347; かんしょう; 1 | CLEAN | CLEAN | CLEAN |
| 感ずる | N2:348; かんずる; 1–2 | CLEAN | CLEAN | CLEAN |
| 間接 | N2:349; かんせつ; 1 | CLEAN | CLEAN | CLEAN |
| 感想 | N2:351; かんそう; 1 | CLEAN | CLEAN | CLEAN |
| 観測 | N2:352; かんそく; 1–2 | NEEDS FIX | CLEAN | CLEAN |
| 寒帯 | N2:353; かんたい; 1 | CLEAN | CLEAN | CLEAN |
| 官庁 | N2:354; かんちょう; 1 | CLEAN | CLEAN | CLEAN |
| 勘違い | N2:355; かんちがい; 1 | CLEAN | CLEAN | CLEAN |
| 缶詰 | N2:356; かんづめ; 1–3 | CLEAN | CLEAN | CLEAN |
| 乾電池 | N2:357; かんでんち; 1 | CLEAN | CLEAN | CLEAN |
| 関東 | N2:358; かんとう; 1–2 | CLEAN | CLEAN | CLEAN |
| 観念 | N2:359; かんねん; 1–3 | CLEAN | CLEAN | CLEAN |
| 乾杯 | N2:360; かんぱい; 1–3 | CLEAN | CLEAN | CLEAN |
| 看板 | N2:361; かんばん; 1–5 | NEEDS FIX | CLEAN | CLEAN |

**All twenty mappings: CLEAN / CLEAN / CLEAN as mappings.** The twentieth is **N2:350 → 乾燥／かんそう**, JMdict **1209920**, senses **1–2**. Its source spelling, reading, and drying/dryness coverage are present. The supplied diff adds only `jlpt: 2`; it does not rewrite the teaching or change its stable identity.

The important qualifications are retained: 代る is explicitly taught rather than inferred from shared kana; 替わる/換わる receive spelling/use explanations; historical regional meanings are distinguished from modern 関西/関東; 感ずる’s additional illness sense is dated; 缶詰’s confinement use is constructed rather than promoted as an unrestricted English verb; 観念 distinguishes ideas/awareness from resignation; and 看板 teaches its secondary senses separately. The community-list N2 label is not treated as independent N2 certification of every secondary sense.

**All eighteen related changes: CLEAN / CLEAN / CLEAN within their actual deltas:**

- **Twelve kanji files:** `kanji\替.md`, `換.md`, `賞.md`, `接.md`, `測.md`, `帯.md`, `庁.md`, `缶.md`, `詰.md`, `乾.md`, `池.md`, and `板.md`. Alias backlinks target explicitly taught forms; added reciprocal examples use the actual compound readings; applicable identities are supported. Missing component cards are not replaced with invented readings or speculative additions.
- **Three comparison links:** `words\感覚.md`, `words\缶.md`, and `words\意見.md` link their existing comparisons appropriately.
- **Related-form link:** `words\感じる.md` correctly links 感ずる without rewriting its conjugation teaching.
- **Two introductory links:** `articles\kaeru-change-replace-and-return.md` links the replacement article in the relevant existing introductions.
- **Level-only reuse:** `words\乾燥.md` passes the narrow claim described above. This is not comprehensive recertification of its unchanged content.

## Findings

The governing behavior is documented at `docs\content-format.md:83–105`: different titles are not semantically deduplicated; exclusions are symmetric, pairwise, and nontransitive, including between other choices. For every pair below, neither endpoint declares the direct exclusion. These are possible ambiguous choices, not claims that a particular app draw was observed.

**B18-GPT-01 — Moderate · Correctness: quiz choices · High confidence**  
**Location:** `words\感激.md:4,9`; counterpart `words\感じる.md:4,9`.

感激 has the label **“being profoundly moved; deep emotion”**, but remains eligible alongside 感じる, **“feel; sense.”** 感じる has an ordinary emotional-response sense—not just sensory perception—so the 感激 label can also describe 感じる. This can penalize a learner for recognizing a valid secondary meaning.

**Evidence:** Complete comparison family **1212260**, sense **2**, at `docs\n2-vocabulary-batch-sources\batch-18.json:3754–3849`, includes being moved, touched, and impressed, without a dated or rare qualifier on that sense. The exclusions through 感ずる do not protect the 感激/感じる pair.

**Minimal remedy:** Add `感じる` directly to 感激’s `quiz_exclusions`. No change to either definition is needed.

**B18-GPT-02 — Moderate · Correctness: quiz choices · High confidence**  
**Location:** `words\観測.md:4,9,46–49`; counterparts `words\予報.md:4,9,16` and `words\占う.md:4,9,16–26`.

観測 explicitly teaches prediction/assessment and uses **“observation; prediction”** as its answer label, but lacks direct guards against **予報** (“forecast”) and **占う** (“tell fortunes; predict”). Both have genuine predictive meanings. In particular, 占う is not restricted to supernatural divination. These labels can therefore supply defensible competing answers.

**Evidence:** Principal family **1214980**, sense **2**, supports 観測’s prediction meaning. Independently retrieved [予報](https://jisho.org/api/v1/search/words?keyword=予報) defines よほう as forecast/prediction; [占う](https://jisho.org/api/v1/search/words?keyword=占う) gives a separate unrestricted sense **2** for prediction/forecasting. The existing exclusions through 予想/予測 are not transitive.

**Minimal remedy:** Add `予報` and `占う` directly to 観測’s `quiz_exclusions`. This does not imply that forecasting, divination, and scientific observation are interchangeable constructions.

**B18-GPT-03 — Minor · Correctness: English quiz-label ambiguity · High confidence**  
**Location:** `words\換気.md:1–9,15–16`; counterpart `words\干す.md:4,14–18`.

換気 has **“ventilation; airing a room”** and no exclusions. 干す has **“hang out to dry; air out.”** Although their Japanese household uses differ, the unqualified English **“air out”** can correctly describe 換気. The room qualifier on 換気’s own title does not constrain the competing title’s wording.

**Evidence:** Complete family **1603510**, sense **1**, at `docs\n2-vocabulary-batch-sources\batch-18.json:9713–9826` supports 干す’s airing/drying use. [Oxford’s *air* verb entry](https://www.oxfordlearnersdictionaries.com/definition/english/air_2) explicitly gives North American **“air (something) out”** for allowing fresh air into a room/building—the activity taught for 換気.

**Minimal remedy:** Add `干す` to 換気’s `quiz_exclusions`. Do not teach that 干す and 換気する are generally interchangeable.

**B18-GPT-04 — Minor · Correctness: English quiz-label ambiguity · Medium-high confidence**  
**Location:** `words\看板.md:4,9,27`; counterpart `words\模様.md:4,9,16`.

看板 explicitly teaches an outward-show/appearance sense, but can coexist with 模様’s label **“pattern; appearance.”** In a sense-unspecified meaning question, that unqualified appearance branch is not uniquely wrong for 看板. The direct 看板/様子 and 模様/様子 exclusions do not exclude 看板/模様.

**Evidence:** Principal family **1213990**, sense **4**, at `docs\n2-vocabulary-batch-sources\batch-18.json:787–918`, supports appearance/look/show; 看板’s own article teaches the narrower outward-show interpretation. 模様’s displayed title leaves “appearance” unqualified even though its body explains a situation’s state/appearance. This is an English-label ambiguity, not a claim of unrestricted Japanese synonymy.

**Minimal remedy:** Add `模様` directly to 看板’s `quiz_exclusions`.

## Optional

None.

## Limits

Commit identity, cleanliness, file hashes, and patch completeness remain **receipt-supported rather than independently Git-verified**. Component hash verification likewise rests on the supplied evidence records.

The supplied dictionary selection is not the whole dictionary; omitted records were not treated as evidence of lexical absence. Author mapping notes, quiz rationales, and the permitted inspection records were assessed as assertions, not counted as independent reviewer retrieval. Live dictionary responses are additional lexical evidence, not verification of the pinned snapshot’s hashes or of N2 membership.

Public 代わる lookups did not yield usable lexical text; its assessment relies on the complete pinned family and editorial construction analysis. Original example naturalness was assessed editorially, not through exhaustive corpus attestation or native-speaker certification. The quiz findings follow the documented selection contract; no app draw was executed.
