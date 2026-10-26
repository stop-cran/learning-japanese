## Snapshot: 1e39beb7f4a0f18f01f4851698fb346ea443f6c6 — committed content only

Parent: `f3c0ec4d7cda9b6f1948d7989b15221cb90d12b1`.

This review targets the committed snapshot identified by `frozen-snapshot.json`, which was read first. **File tools cannot execute Git**: commit identity, committed-only status and supplied hash/equivalence receipts were not independently verified through Git.

## Scope

Actual model: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`, family `gpt`. The review was read-only and serial, without agents, delegation, edits or concurrent calls.

Complete reads covered:

- Both required instruction files; `docs\content-format.md:18-103`; both repository source/snapshot JSON documents; the TSV header and exactly physical rows **1602–1621**.
- All **twenty assigned articles**, all **twenty mappings**, all **twenty principal families / thirty-four senses**, all **twenty-eight component records**, and all **316 comparison labels**.
- All thirteen selected family chunks, supplemental comparisons and extra comparisons: **348 complete frozen families / 829 senses**, including the principals—not all 536 prepared families.
- All twenty-three older-body chunks: **183 complete baseline/comparison renderings**, including both N4 reuses. Additional direct comparison reads included 見える, ビル, ホーム, ぎゅうぎゅう, 売り切れ, 売り切れる, 現れる, 成績, 葬式 and 出る.
- Complete current and baseline 順 bodies, `related.patch`, and the existing 付 card.
- Complete `public-bodies.txt` through EOF: twenty applicable lexical wrappers from **Digital Daijisen via Weblio, one authority**. Live Jisho responses supplied additional applicable records for 現れる and 出る; these are separate, unfrozen JMdict-derived evidence.

Author rationale, prohibited ledgers and other reviewers’ reports were not read. `review-evidence.json` was read only at lines 1–200; the required lossless JSONL records were read completely.

## Verdicts

**Five findings:** four quiz-guard gaps and one component-link gap. No actionable defect was established in the selected lexical teaching, examples, conjugations or translations. Quiz metadata defects are classified under **Correctness**; missing useful component navigation under **Scoped coverage**.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1602 | マラソン | CLEAN | CLEAN | CLEAN | Standard race distance and qualified extended uses are appropriately distinguished. |
| N2:1603 | まれ — source 稀 | CLEAN | CLEAN | CLEAN | Exact source spelling recognized; まれな／まれに attachment is clear. |
| N2:1604 | 回り道 | CLEAN | CLEAN | CLEAN | Physical detour and figurative indirect approach are scoped clearly. |
| N2:1605 | 満員 | NEEDS FIX | CLEAN | CLEAN | Admissions “sold out” recognition needs two direct guards: F01. |
| N2:1606 | マンション | CLEAN | CLEAN | CLEAN | Japanese apartment/building meanings are separated from English “mansion”; construction and ownership are tendencies. |
| N2:1607 | 満点 | CLEAN | CLEAN | CLEAN | Maximum possible score—not necessarily 100—and figurative excellence are distinguished. |
| N2:1608 | 見送る | CLEAN | CLEAN | CLEAN | Selected departure/pass-over/defer meanings and additional recognition are adequately bounded. |
| N2:1609 | 見下ろす | CLEAN | CLEAN | CLEAN | Elevated viewing and contempt are distinguished; forms and constructions are sound. |
| N2:1610 | 見かけ — source 見掛け | NEEDS FIX | CLEAN | CLEAN | Source spelling and apparent-size recognition are taught; missing 表情 guard: F02. |
| N2:1611 | 三日月 | CLEAN | CLEAN | CLEAN | みかづき and young visible crescent are distinguished from 三日 and astronomical new moon. |
| N2:1612 | 岬 | CLEAN | CLEAN | CLEAN | Applicable みさき meaning includes sea/lake projections; alternative 崎 is recognized. |
| N2:1613 | みじめ | CLEAN | CLEAN | CLEAN | Modern na-adjective use and potentially humiliating tone are clear; raw “arch” is not imposed. |
| N2:1614 | ミシン | CLEAN | CLEAN | CLEAN | Sewing machine, rather than machinery or sewing activity generally, is explicit. |
| N2:1615 | 店屋 | CLEAN | CLEAN | CLEAN | Correct みせや shop/store identity and native formation; unrelated てんや excluded. |
| N2:1616 | 見出し | CLEAN | CLEAN | CLEAN | Heading/headline, index recognition and additional headword use are supported. |
| N2:1617 | 道順 | CLEAN | CLEAN | CLEAN | Route/directions, mixed reading and reciprocal 順 links are clear. |
| N2:1618 | 見つかる — source 見付かる | NEEDS FIX | NEEDS FIX | CLEAN | N4 teaching preserved; missing appearance/finding guards F03 and 付 link F05. |
| N2:1619 | 見つける — source 見付ける | CLEAN | NEEDS FIX | CLEAN | N4 teaching preserved; new visual-familiarity sense is correctly explained. Existing alias lacks 付 link: F05. |
| N2:1620 | みっともない | CLEAN | CLEAN | CLEAN | Appearance/conduct, harsh register and i-adjective behavior are appropriately explained. |
| N2:1621 | 見直す | NEEDS FIX | CLEAN | CLEAN | Reviewing, improved opinion and intransitive recovery are distinguished; missing 復習 guard: F04. |

**Mappings — CLEAN.** All twenty source associations, identities, readings, selected one-based senses and additional-recognition mappings match the inspected records. 稀→まれ, 見掛け→見かけ, 見付かる→見つかる and 見付ける→見つける retain explicit source recognition. Additional senses are not treated as separate N2 assignments.

**Baseline preservation — CLEAN.** Both reused articles retain their stable word, reading, title, N4 level and old teaching. The new rare-spelling recognition in 見つかる and visual-familiarity teaching in 見つける are genuinely additive; the latter was not already taught in the old body.

**順 preservation and reciprocity — CLEAN.** Metadata is unchanged, including twelve strokes, radical 頁/181, ジュン, empty kunyomi and existing distractors. Unrelated teaching and the explicitly modern-shape mnemonic are preserved. 道順 is added to the reading table and common-word list, with reciprocal 道順→順 linking and an additive citation.

**Components — primary metadata CLEAN; navigation NEEDS FIX under F05.** Every written primary Han is represented in metadata. Kana-primary aliases do not require their alternate characters in the primary array. Existing substantive component links are generally useful; absent cards such as 岬, 崎, 稀 and 惨 must not be invented.

No excessive guard was established from the inspected evidence. In particular, 採点’s complete body also records the assigned-score result, so its 満点 guard is not invalid merely because grading is its main use. Shared topics or common exclusion neighbors were not treated as automatic cliques.

## Findings

**F01 — Medium severity · Correctness · Missing admissions/sold-out guards**

**Locations:** `words\満員.md:9,33`; comparison evidence at `words\売り切れ.md:4,9,16-20` and `words\売り切れる.md:4,9,16-23`.

満員 explicitly permits an admissions “sold-out” translation. The complete comparison articles also cover tickets—not only merchandise—and their titles are “sold out; no stock left” and “be sold out.” These are defensible context-free answers for the supported admissions use of 満員.

Neither direct pair is guarded. **Minimal remedy:** add both 売り切れ and 売り切れる to 満員’s exclusions, or declare each pair at its opposite endpoint. The existing 売り切れ／売り切れる edge does not propagate transitively.

**Exact evidence:** 満員’s scoped admissions statement; both ticket examples; complete pinned families 1526720, 1473870 and 1473880, sense 1. This does not assert unrestricted substitution for merchandise. **Confidence: high.**

**F02 — Medium severity · Correctness · Missing 見かけ／表情 guard**

**Locations:** `words\見かけ.md:4,9,16`; `words\表情.md:4,15,24,32`.

表情 is principally taught as facial expression, but its complete body explicitly extends to other expressive appearances. Its complete pinned family also includes the ordinary secondary sense “look; appearance; expression (vocal, etc.).” Consequently, 見かけ’s unqualified title **“outward appearance”** is a plausible answer for 表情 in a context-free quiz.

**Minimal remedy:** declare the direct 見かけ／表情 exclusion at either endpoint. Do not broaden either article into a claim that facial expression and general appearance are unrestricted synonyms.

**Exact evidence:** complete 表情 body, especially its extension at line 32; JMdict 1489700, sense 2, with no spelling/reading restriction separating it from ひょうじょう; 見かけ 1604420, sense 1. **Confidence: medium-high.**

**F03 — Medium severity · Correctness · Missing 見つかる／出る and 見つかる／現れる guards**

**Locations:** `words\見つかる.md:4,9,16`; `words\出る.md:4,15`; `words\現れる.md:4,9,16`.

見つかる retains **“be found; turn up.”** 出る’s actual title is “go out or appear,” and 現れる’s is “appear; become apparent.” Their complete bodies teach the applicable appearance uses. These overlap the context-free “turn up” label; 出る additionally has an ordinary finding/discovery use.

**Minimal remedy:** add both 出る and 現れる to 見つかる’s exclusions. 現れる already guards 出る, but that does not protect either missing pair.

**Exact evidence:** the three complete article bodies; the complete applicable live Jisho 出る record expressly gives “turn up,” “be found,” “be detected” and “be discovered” in its fifth presented sense; the applicable 現れる record gives appearance/becoming visible. Those live indices are **not claimed as verification of pinned JMdict numbering**. The remedy preserves the N4 title and teaching. **Confidence: high.**

**F04 — Medium severity · Correctness · Missing 見直す／復習 guard**

**Locations:** `words\見直す.md:4,9,16,35`; `words\復習.md:4,15`.

見直す’s title contains unqualified **“review.”** 復習’s title is “study review,” and its complete body teaches reviewing previously learned material. Although 見直す correctly explains the Japanese distinction, that explanation does not accompany a context-free title choice: “review” remains a legitimate English answer for 復習.

**Minimal remedy:** add 復習 to 見直す’s exclusions, or the reciprocal declaration to 復習. Keep the accurate scoped distinction and existing titles.

**Exact evidence:** complete bodies; pinned 見直す 1259900, sense 2, and 復習 1500800, sense 1. This is English-label ambiguity, not a claim that all study revision and plan reconsideration are interchangeable. **Confidence: high.**

**F05 — Low severity · Scoped coverage · Existing 付 card is unlinked at source-spelling recognition**

**Locations:** `words\見つかる.md:23`; `words\見つける.md:27`; supporting card `kanji\付.md:2-10,20-21`.

Both source spellings introduce 付 substantively without linking its existing card. This is a **new omission** in the added 見付かる paragraph and an **inherited omission**, not a preservation regression, in the existing 見付ける paragraph.

**Minimal remedy:** link the existing 付 card within each spelling-recognition paragraph. Preserve the rare/standard spelling distinction, both N4 levels and `kanji: [見]`. No attachment-based etymology needs to be added.

**Exact evidence:** the two complete spelling paragraphs, the complete existing 付 card and the repository instruction to link existing cards at substantive introductions or comparisons. **Confidence: high.**

## Optional

None.

## Limits

Git status, committed-file equivalence and author-executed hash checks were not independently executable. The review therefore relies on the supplied frozen-snapshot provenance rather than independently proving that each file-tool read matches the named commit.

The frozen family inspection covers **348/829**, not all prepared families. Comparison labels were not counted as full-body reads. The twenty captured public wrappers represent one dictionary authority; the live Jisho records are unfrozen derivatives and do not replace pinned raw records. A Cambridge retrieval failed with HTTP 520 and was not counted as verification.

No corpus-frequency survey or native-speaker certification was performed. **CLEAN means no actionable defect established within this inspected scope**, not exhaustive correctness.
