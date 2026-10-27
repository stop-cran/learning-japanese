## Snapshot: 9f6464f5255dd6ece56e4c949a7a3102ae38fbcb; committed files only

Reviewed on the supplied clean-worktree assertion, against the stated baseline `d84e80eefe300d2eb93a2762c641952c6351d0d7`. **File tools were available, but Git execution was not:** I could not independently authenticate HEAD, cleanliness, the baseline diff, or the exact 56-file change set.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Sole reviewer; sequential and read-only, without delegation or edits. Read all 17 assigned teaching pages completely. Checked all 15 metadata sets, all 46 reading rows—including 38 lexical examples and eight qualified source-only rows—and all 45 curated kanji distractor assignments.

Inspected the linked passages in context in these 19 existing `words\` articles: お皿, 医療, 灰皿, 玉, 瓶, 甘い, 畳, 皮, 皿, 省く, 県, 砂, 砂漠, 砂糖, 硬い, 硬貨, 磨く, 祈る and 花瓶. Also checked relevant existing answer labels, direct word exclusions, and older two-distractor kanji fallback candidates.

Read the required instructions and format reference, both permitted source records, and relevant comparison evidence. **No assigned teaching page or related linked passage was omitted.** Unchanged word content was not comprehensively re-reviewed; stroke drawing paths and unassigned content were omitted. Forbidden authoring notes, review ledgers and other reviewers’ outputs were not accessed.

## Verdicts:

**One actionable quiz ambiguity was established.** The other pages have no established actionable defect within the assigned scope.

| Page | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\玉.md` | NEEDS FIX | CLEAN | CLEAN |
| `kanji\瓶.md` | CLEAN | CLEAN | CLEAN |
| `kanji\甘.md` | CLEAN | CLEAN | CLEAN |
| `kanji\畜.md` | CLEAN | CLEAN | CLEAN |
| `kanji\略.md` | CLEAN | CLEAN | CLEAN |
| `kanji\畳.md` | CLEAN | CLEAN | CLEAN |
| `kanji\療.md` | CLEAN | CLEAN | CLEAN |
| `kanji\皮.md` | CLEAN | CLEAN | CLEAN |
| `kanji\皿.md` | CLEAN | CLEAN | CLEAN |
| `kanji\省.md` | CLEAN | CLEAN | CLEAN |
| `kanji\県.md` | CLEAN | CLEAN | CLEAN |
| `kanji\砂.md` | CLEAN | CLEAN | CLEAN |
| `kanji\硬.md` | CLEAN | CLEAN | CLEAN |
| `kanji\磨.md` | CLEAN | CLEAN | CLEAN |
| `kanji\祈.md` | CLEAN | CLEAN | CLEAN |
| `words\家畜.md` | CLEAN | CLEAN | CLEAN |
| `words\略語.md` | CLEAN | CLEAN | CLEAN |

All readings, primary stroke counts, canonical radicals/numbers and grade tags match the pinned metadata. The source-only qualifications do not assert unattested everyday words or dictionary absence. All 15 kanji have a useful linked word article.

No additional defect was established in the related link edits or older two-choice fallback interactions. 家畜’s direct exclusion of 牛 protects the applicable “cattle” overlap; it does not imply transitive exclusion of 牛肉. The existing 株 label “stock share; stump” also disambiguates the English *stock* homograph.

## Findings:

### GPT-01 — Moderate; correctness; `kanji\玉.md:11`

**Claim and impact:** 王 is not a reliably wrong meaning-quiz distractor for 玉. Its displayed title is **“king”** (`kanji\王.md:3`), but standalone 玉, read ぎょく, also denotes the shogi king. A learner can therefore defend both “jewel; ball” and “king” when shown the uncontextualized character 玉. The distinction between the written characters does not eliminate this semantic overlap.

**Minimal remedy:** Replace 王 in the distractor list with an existing, semantically disjoint lookalike. The useful 王/玉 visual comparison can remain in the notes; expanding the lesson into shogi vocabulary is unnecessary.

**Exact evidence:**
- `docs\n2-batch-sources\batch-15.json:625–759`: JMdict entry **1921990**, exact spelling 玉 and reading ぎょく. Sense 7 at lines **727–740** supplies “king (of the junior player),” marked as an abbreviation, without a spelling or reading restriction excluding this pair.
- Independently fetched [Digital Daijisen, ぎょく【玉】](https://kotobank.jp/word/%E7%8E%89-53197), sense **5**, explicitly identifies it as an abbreviation of the shogi piece 玉将.
- `docs\content-format.md:40–46` requires three semantically wrong options and checks meanings rather than merely distinct title strings.

**Confidence:** High. This is an attested standalone sense, not an inference from a compound’s components.

## Optional:

None.

## Limits:

Snapshot provenance and the “links only” characterization remain supplied assertions because Git execution was unavailable. Pinned source records were inspected, but their upstream download hashes were not independently recomputed.

The 15 stroke files’ pinned-converter provenance was accepted as supplied; **no exhaustive drawing-path review was performed**. The eight source-only rows were checked as qualified character-dictionary information, not verified lexical examples. This review does not establish corpus frequency, native-speaker certification, or comprehensive correctness of unchanged articles or the entire quiz pool. No other consequential linguistic claim remained unresolved within the assigned scope.
