## Snapshot: dfe4fb06ebb16b9a224e63b56f23a787b8502880; committed files only

**Three minor quiz-safety findings; no established defects in the 15 new kanji cards.** Baseline: `5b47e12b71bd4fdbc818da671cebec910a6e8635`.

The snapshot identity, clean worktree and exact 63-file scope are author-supplied assertions. I have file tools, **not Git execution**, so I could not independently verify those assertions or reconstruct the commit diff.

## Scope: gpt-6.1-sol; family gpt

Reviewed independently and sequentially, without delegation or file edits. Read all 18 new teaching pages completely, the three required instruction/format passages, and the pinned metadata and selected dictionary evidence.

Inspected the component-link passages in these 24 existing word articles in context: 毛, 毛布, 髪の毛, 氷, 永久, 永遠, 汗, 汚い, 汚れる, 汚染, 池, 沈む, 河, 沸く, 沸かす, 油, 石油, 状況, 泉, 宿泊, 泊まる, 波, 泥 and 泥棒. Also inspected `kanji\川.md`’s added 州 distractor, relevant comparison cards, existing word answer labels and direct exclusions, older two-distractor headers, and relevant `docs\confusable-words.md` passages. This was **not a comprehensive review of unchanged articles**.

Did not read `docs\n2-authoring-notes.md`, `docs\n2-review.md`, `REVIEW.md`, `docs\n2-reviews\`, session authoring inputs or another reviewer’s output. Exhaustive stroke-path review was not assigned and was not performed.

## Verdicts:

Quiz-answer ambiguity is classified under **correctness** below; it does not imply an error in the accompanying Japanese explanation.

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\毛.md` | CLEAN | CLEAN | CLEAN |
| `kanji\氷.md` | CLEAN | CLEAN | CLEAN |
| `kanji\永.md` | CLEAN | CLEAN | CLEAN |
| `kanji\汗.md` | CLEAN | CLEAN | CLEAN |
| `kanji\汚.md` | CLEAN | CLEAN | CLEAN |
| `kanji\池.md` | CLEAN | CLEAN | CLEAN |
| `kanji\沈.md` | CLEAN | CLEAN | CLEAN |
| `kanji\河.md` | CLEAN | CLEAN | CLEAN |
| `kanji\沸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\油.md` | CLEAN | CLEAN | CLEAN |
| `kanji\況.md` | CLEAN | CLEAN | CLEAN |
| `kanji\泉.md` | CLEAN | CLEAN | CLEAN |
| `kanji\泊.md` | CLEAN | CLEAN | CLEAN |
| `kanji\波.md` | CLEAN | CLEAN | CLEAN |
| `kanji\泥.md` | CLEAN | CLEAN | CLEAN |
| `words\汚す.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\沈める.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\泊める.md` | NEEDS FIX | CLEAN | CLEAN |

All kanji reading lists, primary stroke counts, canonical radicals and grade tags match the pinned metadata. The 44 lexical reading examples respect the inspected spelling/reading/sense restrictions; the four source-only rows are honestly qualified. All **45 new-kanji distractor assignments** have existing, semantically wrong answer labels, and every new kanji has a useful linked word article.

The 川→州 addition is suitable: “state; province” is wrong for 川. Supplying the third curated option also addresses the default four-choice fallback risk introduced by the synonymous new 河 card. No actionable defect was established in the 24 component-link edits.

## Findings:

### GPT-01 — Minor; correctness: English-label ambiguity remains between 汚す and 汚れる

**Location:** `words\汚す.md:4–8`; comparison `words\汚れる.md:4,15`.

The title **“soil; stain”** does not unambiguously encode transitivity. Both English verbs also have intransitive uses meaning becoming dirty or stained. Consequently, a meaning question for 汚れる can present both its intended “get dirty” answer and the new “soil; stain” label as defensible choices. The existing exclusion protects 土, not 汚れる; neither article declares this direct pair.

**Minimal remedy:** Add 汚れる to 汚す’s `quiz_exclusions`. Alternatively, make the label explicitly transitive, such as “make dirty; stain something,” with a matching heading.

**Exact evidence:** Pinned JMdict entry **1178960**, よごす, sense 1 is transitive (`docs\n2-batch-sources\batch-12.json:1496–1509`); entry **1179005**, よごれる, sense 1 is intransitive “get/become dirty” (`:1585–1595`). The fetched American Heritage entries explicitly give [soil](https://www.ahdictionary.com/word/search.html?q=soil) an intransitive “become dirty, stained, or tarnished” sense and [stain](https://www.ahdictionary.com/word/search.html?q=stain) an intransitive discoloration sense, illustrated by upholstery staining easily.

**Confidence:** High. The Japanese distinction is correctly explained in the bodies; the defect concerns the independently displayed English labels.

### GPT-02 — Minor; correctness: 沈める’s applicable “lower” sense lacks direct quiz exclusions

**Location:** `words\沈める.md:8,45–46`; comparison titles at `words\下げる.md:4`, `words\下ろす.md:4` and `words\降ろす.md:4`.

沈める correctly acknowledges the dictionary sense of lowering one’s body into a seat. That makes the existing answer alternatives **“lower; hang,” “lower; take down,” and “lower; unload; drop off”** potentially defensible for 沈める: each contains the applicable gloss “lower.”

Its sole exclusion, 沈む, does not protect these pairs. The existing exclusions among the lowering verbs do not protect them either, because exclusions are symmetric **but not transitive**.

**Minimal remedy:** Add direct exclusions for **下げる, 下ろす and 降ろす** on 沈める. Retain the accurate secondary-sense explanation.

**Exact evidence:** Pinned JMdict entry **1431680**, sense 2, expressly gives “to lower (e.g. one’s body into a chair),” without spelling or reading restrictions (`docs\n2-batch-sources\batch-12.json:2101–2114`). Successfully fetched entries verify [下げる・さげる, 1184170](https://takoboto.jp/?w=1184170), including “to lower,” and [下ろす／降ろす・おろす, 1589580](https://takoboto.jp/?w=1589580), whose first sense includes lowering. The inspected exclusion declarations contain no direct link to 沈める.

**Confidence:** High. This follows an applicable secondary meaning, not a claim that all three verbs freely substitute for 沈める in sentences.

### GPT-03 — Minor; correctness: 泊める’s second English alternative can describe the guest staying

**Location:** `words\泊める.md:4–8,11`; comparison `words\泊まる.md:4`.

Although **“lodge someone”** clearly describes hosting, the separate alternative **“put up overnight”** also has an established intransitive English interpretation: stay somewhere for the night. That alternative can therefore answer 泊まる, whose label is “stay overnight.” There is no direct exclusion between these cards.

The body correctly teaches 泊める as transitive; this is an English answer-label defect, not an incorrect Japanese construction.

**Minimal remedy:** Change the title and matching heading to **“lodge someone; put someone up overnight.”** This preserves the intended meaning while removing the guest/host ambiguity.

**Exact evidence:** The fetched [Oxford Learner’s Dictionaries “put up” entry](https://www.oxfordlearnersdictionaries.com/definition/english/put-up) distinguishes **put somebody up**, accommodating somebody at home, from **put up (at …)**, especially British English, meaning staying somewhere for the night. Pinned JMdict entry **1474860**, とめる, is transitive accommodation (`docs\n2-batch-sources\batch-12.json:3077–3089`); **1474850**, とまる, has the intransitive hotel-stay sense (`:3021–3031`).

**Confidence:** High.

## Optional:

None.

## Limits:

- Without Git execution, commit identity, worktree cleanliness, the baseline diff and the exact 63-file changed set remain independently unverified. Findings refer to the inspected files under the author-asserted frozen snapshot.
- The source JSON is selected evidence, not complete JMdict. Omitted spellings were not treated as dictionary absence. 況’s `まし.て`／`おもむき` and 泥’s `デ`／`ニ` remain explicitly lookup-only, without invented lexical attestations.
- The 15 converter-generated stroke files did not receive exhaustive drawing-path review. Generated-manifest integrity and runtime quiz sampling were outside this content review.
- Merriam-Webster, Cambridge and Collins English fetches failed and supplied no evidence; the English-sense findings rely on successfully fetched American Heritage and Oxford entries.
- No consequential linguistic question raised during this review remains unresolved. **CLEAN** means no established actionable defect within this scope, not exhaustive truth, frequency verification or native-speaker certification.
