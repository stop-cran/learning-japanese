## Snapshot: b943db187ef28180325d18358d1251547249d0bf; committed files only

Snapshot identity and clean-worktree status are author-supplied, not independently Git-verified.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Independent, read-only review; no delegation or file edits. All 18 pages in the verdict table were read completely. Checks covered metadata, all **58 reading rows**—47 lexical examples and eleven qualified source-only rows—teaching content, all **45 kanji distractor assignments**, useful word links, and relevant word-quiz labels and direct exclusions.

The changed component-link passages were inspected with surrounding context in these 21 articles under `words\`: `予測.md`, `体温.md`, `加減.md`, `気温.md`, `水準.md`, `浅い.md`, `涙.md`, `涼しい.md`, `混乱.md`, `混雑.md`, `清潔.md`, `減らす.md`, `減る.md`, `温い.md`, `温度.md`, `温暖.md`, `湖.md`, `湯.md`, `湾.md`, `準備.md`, and `あびる.md`. The third distractor 木 in `kanji\水.md` and the related fallback concern were also inspected.

Required instructions and format documentation, both permitted source records, relevant comparisons, and fetched dictionary entries were consulted. **No assigned teaching page or related changed-link passage was omitted.** Unchanged articles were not comprehensively reviewed; generated stroke drawings were not examined. Forbidden ledgers, authoring inputs, and other reviewers’ outputs were not consulted.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\浅.md` | CLEAN | CLEAN | CLEAN |
| `kanji\浴.md` | CLEAN | CLEAN | CLEAN |
| `kanji\涙.md` | CLEAN | CLEAN | CLEAN |
| `kanji\液.md` | CLEAN | CLEAN | CLEAN |
| `kanji\涼.md` | CLEAN | CLEAN | CLEAN |
| `kanji\混.md` | CLEAN | CLEAN | CLEAN |
| `kanji\清.md` | CLEAN | CLEAN | CLEAN |
| `kanji\減.md` | CLEAN | CLEAN | CLEAN |
| `kanji\温.md` | CLEAN | CLEAN | CLEAN |
| `kanji\測.md` | CLEAN | CLEAN | CLEAN |
| `kanji\湖.md` | CLEAN | CLEAN | CLEAN |
| `kanji\湯.md` | CLEAN | CLEAN | CLEAN |
| `kanji\湾.md` | CLEAN | CLEAN | CLEAN |
| `kanji\湿.md` | CLEAN | CLEAN | CLEAN |
| `kanji\準.md` | CLEAN | CLEAN | CLEAN |
| `words\浴びせる.md` | CLEAN | NEEDS FIX | CLEAN |
| `words\液体.md` | CLEAN | CLEAN | CLEAN |
| `words\湿度.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within this scope, not exhaustive truth or native-speaker certification.

## Findings:

**GPT-01 — Minor; scoped coverage: missing direct quiz exclusion.**  
**Location:** `words\浴びせる.md:4,8`; related declarations at `words\流す.md:4,9` and `words\注ぐ.md:9`.

The new answer label **“pour over; shower someone with”** can also describe 流す in its liquid-pouring/body-rinsing use. Nevertheless, 浴びせる and 流す remain eligible to appear together: 浴びせる excludes 注ぐ, and 注ぐ excludes 流す, but exclusions are **not transitive**. When this pair appears, the “pour over” portion can make a second answer defensible, including in an English-to-Japanese question.

**Minimal remedy:** Add `流す` to `浴びせる`’s `quiz_exclusions`. Preserve the existing definitions; the words need not be synonymous in every use to require protection.

**Exact evidence:**
- `docs\n2-batch-sources\batch-13.json:1376-1428`, JMdict entry **1547440**, retains 浴びせる／あびせる, “to pour on,” transitive ichidan.
- The fetched [JMdict-derived Jisho entry for 流す／ながす](https://jisho.org/api/v1/search/words?keyword=%E6%B5%81%E3%81%99), sense 1, explicitly includes **“to pour.”**
- The fetched [精選版 日本国語大辞典 entry for 流す](https://kotobank.jp/word/%E6%B5%81%E3%81%99-587809), section 一④, specifies pouring water over the body to wash it: 「からだに湯や水をかけて洗う」. This supports the overlap beyond a generic shared “water” association.
- `docs\content-format.md:85-99` establishes symmetric, nontransitive exclusions and requires protection when either label is a reasonable answer for the other word.

**Confidence:** High in the missing direct protection and dictionary-supported physical-sense overlap; this does not assert interchangeability in the figurative question-bombarding sense.

No additional actionable defect was established. All requested metadata matched the pinned records; the eleven source-only rows were honestly qualified. All 45 curated kanji options were semantically wrong answers. 木 is a valid third distractor for 水 and removes the relevant default four-choice fallback exposure.

## Optional:

None.

## Limits:

- **No Git execution was available.** I could not independently verify HEAD, cleanliness, or the exact diff from baseline `44231580a12fef12ac51b536d4baffe7ec2c3a57`; I relied on the supplied frozen-snapshot identification and scope.
- The fifteen generated stroke JSON files, drawing paths, converter execution, and generated manifest were not audited. Pinned converter provenance was read; exhaustive drawing-path review was outside the assignment.
- The selected evidence is not complete JMdict. Source-only qualifications were not treated as proof of dictionary-wide absence. Nanori and obsolete four-level JLPT assignments were excluded.
- Live JMdictDB was access-gated; goo and Cambridge fetches failed. Those attempts were not evidence for any conclusion. Successful pinned records and fetched entries support the finding above.
- No consequential linguistic claim remains unresolved within the assigned scope. Sentence naturalness was assessed editorially, not through exhaustive corpus or native-speaker validation.
