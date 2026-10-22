## Snapshot: 71dd9a70dcda63c2a0619f79eae8fbfcfcfb897a — committed files only

The frozen snapshot records a clean worktree and 65-file scope, based on `8df545e4faeca74bd0e27e08e5d03123e4d5065a`. **File tools were available, but Git execution was not**; those provenance assertions were not independently verified.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Reviewed all 16 pages below completely, sequentially and read-only, without delegation. Read the three required instruction/format sources and the allowed source snapshots. Compared all 15 kanji metadata records, all 32 reading rows—including the two qualified source-only rows—and all 45 distractor assignments. Checked the supporting word’s answer-label overlaps and direct exclusions, plus the older two-distractor kanji fallback candidates.

Reviewed link-bearing passages and surrounding explanations in these 29 existing word articles: お祝い, お祭り, 万年筆, 予算, 児童, 切符, 封筒, 文章, 祝い, 祝う, 祭, 禁止, 禁煙, 秒, 移す, 移る, 移動, 税, 税金, 章, 競争, 競技, 筆, 管, 管理, 計算, 鉛筆, 松 and 梅.

**Omissions:** unchanged material outside those linked contexts was not comprehensively rereviewed. Stroke drawing paths, manifest integrity and application implementation were not reviewed. The prohibited authoring notes, review ledgers/directories, session authoring inputs, author-check receipts and other reviewers’ outputs were not read.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\祝.md` | CLEAN | CLEAN | CLEAN |
| `kanji\祭.md` | NEEDS FIX | CLEAN | CLEAN |
| `kanji\禁.md` | CLEAN | CLEAN | CLEAN |
| `kanji\秒.md` | CLEAN | CLEAN | CLEAN |
| `kanji\移.md` | CLEAN | CLEAN | CLEAN |
| `kanji\税.md` | CLEAN | CLEAN | CLEAN |
| `kanji\章.md` | CLEAN | CLEAN | CLEAN |
| `kanji\童.md` | CLEAN | CLEAN | CLEAN |
| `kanji\競.md` | CLEAN | CLEAN | CLEAN |
| `kanji\竹.md` | CLEAN | CLEAN | CLEAN |
| `kanji\符.md` | CLEAN | CLEAN | CLEAN |
| `kanji\筆.md` | CLEAN | CLEAN | CLEAN |
| `kanji\筒.md` | CLEAN | CLEAN | CLEAN |
| `kanji\算.md` | CLEAN | CLEAN | CLEAN |
| `kanji\管.md` | CLEAN | CLEAN | CLEAN |
| `words\竹.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within the assigned scope—not exhaustive truth or native-speaker certification.

## Findings:

**F01 — Minor; correctness, quiz-answer ambiguity — `kanji\祭.md:11`.**

祭 assigns 察 as a distractor, displaying its title **“observe; infer”** (`kanji\察.md:3`). English *observe* also means celebrating or keeping a festival. Consequently, a learner can reasonably interpret that option as ritual observance—a defensible meaning of 祭—even though 察’s Japanese meaning concerns observation and inference. The ambiguity is in the displayed English label, not a claim that the Japanese characters are synonyms.

**Impact:** one of the three intended wrong options is not unambiguously wrong in the context-free meaning quiz.

**Minimal remedy:** replace 察 with a semantically distinct existing card, such as 禁 (“prohibit; ban”). No change to the older 察 card is necessary.

**Exact evidence:** `docs\n2-batch-sources\batch-16.json:66–72` includes “celebrate” among 祭’s KANJIDIC2 meanings; `kanji\祭.md:20` explicitly teaches ritual observance. The successfully fetched [Oxford *observe* entry, sense 5](https://www.oxfordlearnersdictionaries.com/definition/english/observe), confirms the festival-celebration meaning. `docs\content-format.md:40–46` requires semantically distinct wrong options and warns that different labels can still yield defensible answers.

**Confidence:** high.

No other actionable defect was established in the remaining distractor assignments, the new supporting word, or the 29 linked passages. The qualified 競・くら.べる and 算・そろ rows appropriately distinguish character-dictionary lookup information from recommended lexical examples.

## Optional:

None.

## Limits:

Without Git execution, I could not independently verify HEAD, worktree cleanliness, the baseline diff, the exact 65-file scope or recorded hashes. Verdicts apply to the file contents presented under the declared frozen snapshot.

The dictionary evidence is selected rather than exhaustive; omitted spellings were not treated as dictionary absence, and priority flags were not used to infer rarity. The 15 generated stroke files’ provenance was accepted as supplied; **exhaustive drawing-path review was not performed**. No additional consequential linguistic claim remains unresolved within the reviewed scope.
