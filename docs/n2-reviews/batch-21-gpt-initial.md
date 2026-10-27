## Snapshot: 62d417f98be2f575ba851ecb4848923666a29fe8; committed files only

**One localized vocabulary-quiz ambiguity needs fixing.** No actionable defect was established on the other 16 new pages.

The frozen snapshot records a clean worktree and 60-file scope, based on `6118337fa9470ecb8e906ed746703de93dbdff2d`. I have file tools, **not Git execution**; those provenance assertions were not independently verified.

## Scope:

Independent review by **GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`**, without delegation or edits.

All 17 assigned teaching pages were read completely. All 23 link-only component passages were inspected with surrounding context: `words\動詞.md`, `印象.md`, `対象.md`, `建設.md`, `現象.md`, `硬貨.md`, `設備.md`, `設計.md`, `詰める.md`, `課.md`, `課長.md`, `講堂.md`, `講演.md`, `講義.md`, `谷.md`, `豊か.md`, `豊富.md`, `象.md`, `販売.md`, `貯金.md`, `貿易.md`, `銅貨.md`, and `雑誌.md`.

All 15 metadata records and 35 reading rows were checked against the pinned evidence. The 33 lexical examples respect the recorded spelling/reading/sense restrictions; the two qualified lookup/index rows are appropriately distinguished from recommended examples. All **45 curated kanji distractor assignments** are semantically wrong options, and every new kanji has a useful linked word article. No newly activated direct-synonym risk was established in the older two-choice kanji fallbacks.

**Omissions:** No assigned teaching page or related passage was omitted. Unchanged portions of the 23 older articles were not comprehensively reviewed. Stroke drawing paths and unassigned pages were not reviewed comprehensively. Forbidden authoring/review materials and other reviewers’ outputs were not read.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\設.md` | CLEAN | CLEAN | CLEAN |
| `kanji\詞.md` | CLEAN | CLEAN | CLEAN |
| `kanji\詰.md` | CLEAN | CLEAN | CLEAN |
| `kanji\誌.md` | CLEAN | CLEAN | CLEAN |
| `kanji\課.md` | CLEAN | CLEAN | CLEAN |
| `kanji\諸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\講.md` | CLEAN | CLEAN | CLEAN |
| `kanji\谷.md` | CLEAN | CLEAN | CLEAN |
| `kanji\豊.md` | CLEAN | CLEAN | CLEAN |
| `kanji\象.md` | CLEAN | CLEAN | CLEAN |
| `kanji\貝.md` | CLEAN | CLEAN | CLEAN |
| `kanji\貨.md` | CLEAN | CLEAN | CLEAN |
| `kanji\販.md` | CLEAN | CLEAN | CLEAN |
| `kanji\貯.md` | CLEAN | CLEAN | CLEAN |
| `kanji\貿.md` | CLEAN | CLEAN | CLEAN |
| `words\諸島.md` | CLEAN | CLEAN | CLEAN |
| `words\貝.md` | **NEEDS FIX** | CLEAN | CLEAN |

CLEAN means no established actionable defect within this scope, not exhaustive truth or native-speaker certification.

## Findings:

**F01 — Minor; correctness, vocabulary-quiz ambiguity — `words\貝.md:8`**

The exclusions protect 貝 against 皮 and 馬鹿, but not against the existing answer labels **“top; leading position”** (`words\トップ.md:4`) and **“summit; top”** (`words\頂上.md:4`).

The written form 貝 also licenses **ばい**, whose second applicable sense is a **spinning top**. Consequently, the bare English noun *top* retained in both labels can supply a dictionary-defensible answer to the written prompt 貝. The neighboring ranking/summit glosses signal their intended meanings but do not remove that standalone answer-label homograph. This is **not** a claim that トップ or 頂上 means a spinning toy, or that かい is the toy’s pronunciation.

**Impact:** If either pair is selected, the quiz can reject an interpretation supported by another reading of the displayed spelling.

**Minimal remedy:** Add both `トップ` and `頂上` directly to 貝’s `quiz_exclusions`. No expansion of the article’s primary かい lesson is necessary. トップ’s existing exclusion of 頂上 (`words\トップ.md:9`) does not protect either pair with 貝: exclusions are not transitive.

**Exact evidence:** `docs\n2-batch-sources\batch-21.json:4985-5050`, JMdict entry **2246880**, sense 2, records “spinning top (traditionally made from a Japanese Babylon shell)”; its spelling/sense restrictions are empty, and the **ばい** reading has `kanaOnly: false`. The separate **バイ** reading has `kanaOnly: true`, which is not the basis of this finding. Quiz-label and pairwise-exclusion rules appear at `docs\content-format.md:79-98`.

**Confidence:** High for the applicable dictionary identity and missing direct guards; medium for the practical ambiguity of the multi-gloss English labels. This is a conservative quiz-safety finding, not a frequency claim.

## Optional:

None.

## Limits:

The file tools cannot independently establish HEAD, clean status, the baseline diff, or exact correspondence between inspected files and the frozen commit. The report relies on the supplied snapshot’s committed-file identification.

The 15 new stroke files’ pinned-converter provenance was accepted; **exhaustive drawing-path review was not assigned or performed**. Stroke counts were checked against the source metadata, not by auditing drawing paths.

Example naturalness received editorial assessment, not corpus-frequency measurement or native-speaker certification. Public English-dictionary lookups for *top* failed and were not used as evidence; F01 rests on the pinned JMdict record, the stored answer labels, and the supplied quiz rubric. Runtime candidate selection was not exercised, so no claim is made about how often the problematic pairs appear.
