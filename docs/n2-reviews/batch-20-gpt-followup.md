## Snapshot: corrected d14467be49e710ad2c59a881fbf9726dc5c80f94; original adaf3b4c7349e9d7ecb1360b91e9cd85d1ae20ac; committed files only; no Git execution

The corrected receipt reports a clean worktree and twelve-file correction scope. Commit identity, cleanliness and scope are receipt-backed, not independently Git-verified.

## Scope: gpt-6.1-sol; family gpt

Read my original report, the complete supplied five-page teaching patch, and all five changed pages completely. Inspected the eight added dictionary records with their spelling/reading restrictions, the existing 蒸す, cloth-bag and 裏面 comparison records, all six exclusion-target articles, `words\ほかほか.md`, `kanji\複.md`, relevant format rules, and contextual passages for “close friend,” “close by” and “draw to a close.” Independently refetched both cited American Heritage entries.

This was a sequential, read-only confirmation. No commands, edits, delegation or other reviewer reports were used.

## Verdicts:

**GPT-20-01 is resolved as a conservative English-label safeguard. No actionable regression was established in the five changed pages.**

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\蒸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\袋.md` | CLEAN | CLEAN | CLEAN |
| `kanji\裏.md` | CLEAN | CLEAN | CLEAN |
| `kanji\補.md` | CLEAN | CLEAN | CLEAN |
| `words\蒸す.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within this bounded scope.

## Findings:

**GPT-20-01 — RESOLVED; original severity Minor; facet correctness.**  
`words\蒸す.md:8` now directly excludes `べたべた`, `密`, `近い`, `親しい`, `閉じる` and `閉まる`, while retaining `暑い`, `じめじめ` and `じとじと`. This satisfies the original remedy without relying on transitive exclusions.

The explanation at `words\蒸す.md:45-49,66-69` correctly separates English-label safeguards from Japanese synonymy. Refetched [American Heritage *sticky*, adjective sense 3](https://www.ahdictionary.com/word/search.html?q=sticky), and [*close*, adjective sense 14](https://www.ahdictionary.com/word/search.html?q=close), confirm the warm/humid weather meanings. The six Japanese comparison families in `docs\n2-batch-sources\batch-20.json:1236-1847` support their taught non-weather senses; 蒸す entry **1356900**, senses 1–2, remains consistent with the article. `docs\content-format.md:85-99` confirms that the direct declarations are sufficient and symmetric.

`kanji\蒸.md:46` also includes all six comparison-family IDs. **Confidence:** high that the requested safeguards and supporting citations are present; practical ambiguity of the complete multi-gloss labels remains medium-confidence, not an observed app failure.

The other adopted changes are confirmed below. My original report contained no optional findings; these are not retroactive correctness defects.

| Changed passage | Disposition and evidence |
|---|---|
| `kanji\袋.md:44,47` | **Clarification accepted.** Entry **1690870** licenses cloth-bag ふたい and ぬのぶくろ; separate entry **1690880** licenses 布袋 ほてい, Hotei. Complete records at `docs\n2-batch-sources\batch-20.json:4115-4209` support the distinction. No comparative-frequency claim was introduced. |
| `kanji\裏.md:42,45` | **Optional expansion accepted.** Separate entries **1550670** and **2858813** license うらめん and りめん respectively, both with back/reverse senses. Their complete records begin at source-packet lines **5338** and **5424**. The note preserves valid りめん without ranking either pronunciation. |
| `kanji\補.md:11` | **Optional distractor replacement accepted.** `kanji\複.md:4,20` teaches multiplicity/compound structure, not supplementation or making good a shortage. Three distinct wrong options remain. The former 被 choice is not reclassified as an established defect. |

No regression was established in the changed passages or their surrounding teaching explanations.

## Optional:

None required. The context-bound labels “close friend,” “close by” and “draw to a close” do not justify mechanical exclusions. The retained distinction at `words\蒸す.md:55-57` supports leaving ほかほか unchanged; a shared English *steam* stem alone establishes no additional pair. Unchanged 家訓 wording and pre-existing 訓練 notation were not reopened.

## Limits:

This confirms only the supplied correction passages, with complete reads of the five affected pages—not a new full-batch review. The supplied patch leaves their reading tables and reading metadata unchanged; packet-wide identity, the other teaching pages, twenty-one older-word passages and stroke files were not re-audited.

No Git, validator, cumulative audit or manifest-build commands were executed. The reported zero errors, 907-row audit, 85-record/81-family totals, preserved older content and byte-identical builds with contentVersion `f07655f54123151e` remain author-run or author-reported checks. No exhaustive stroke-path inspection, runtime quiz testing or native-fluency certification was performed.
