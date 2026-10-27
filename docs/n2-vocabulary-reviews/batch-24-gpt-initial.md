## Snapshot: 15d8c88a4e49aef85600feb3a6cb1886f7425b14

**Committed content only, as designated by the frozen receipt.** Parent: `3fedae16ef2885a2873b3e63275f0a5813c3c091`.

I have file tools, not Git execution. I therefore cannot independently verify the checkout’s commit, cleanliness, file hashes, or evidence-derivative equivalence; those assurances come from the receipt.

## Scope

**Reviewer:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Sequential, read-only review; no delegation, agents, or file edits.

Read all twenty assigned new articles completely; inspected the actual three-file related patch and changed kanji passages in context; assessed mappings **N2:462–N2:481**, including selected/additional-sense qualifications. Consulted the required instructions, format specification, pinned provenance, all twenty complete principal dictionary families, component evidence, all 109 supplied comparison labels/exclusion lists, targeted complete comparison records and existing cards, and actual public dictionary entries. No reused principal articles or forbidden authoring/reviewer material were reviewed.

## Verdicts

**Three actionable quiz-exclusion gaps were established.** These affect quiz correctness, not the articles’ source-form coverage or the correctness of their prose explanations.

| Source mapping → new article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| N2:462 → `words\激増.md` | CLEAN | CLEAN | CLEAN |
| N2:463 → `words\下車.md` | CLEAN | CLEAN | CLEAN |
| N2:464 → `words\下旬.md` | CLEAN | CLEAN | CLEAN |
| N2:465 → `words\下水.md` | CLEAN | CLEAN | CLEAN |
| N2:466 → `words\削る.md` | CLEAN | CLEAN | CLEAN |
| N2:467 → `words\桁.md` | CLEAN | CLEAN | CLEAN |
| N2:468 → `words\下駄.md` | CLEAN | CLEAN | CLEAN |
| N2:469 → `words\血圧.md` | CLEAN | CLEAN | CLEAN |
| N2:470 → `words\血液.md` | CLEAN | CLEAN | CLEAN |
| N2:471 → `words\月給.md` | CLEAN | CLEAN | CLEAN |
| N2:472 → `words\傑作.md` | NEEDS FIX | CLEAN | CLEAN |
| N2:473 → `words\月末.md` | CLEAN | CLEAN | CLEAN |
| N2:474 → `words\気配.md` | NEEDS FIX | CLEAN | CLEAN |
| N2:475 → `words\下品.md` | CLEAN | CLEAN | CLEAN |
| N2:476 → `words\煙い.md` | CLEAN | CLEAN | CLEAN |
| N2:477 → `words\蹴る.md` | CLEAN | CLEAN | CLEAN |
| N2:478 → `words\険しい.md` | CLEAN | CLEAN | CLEAN |
| N2:479 → `words\見学.md` | CLEAN | CLEAN | CLEAN |
| N2:480 → `words\謙虚.md` | CLEAN | CLEAN | CLEAN |
| N2:481 → `words\原稿.md` | NEEDS FIX | CLEAN | CLEAN |

**Related changes—changed passages only:**

| File and change | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\圧.md`: 血圧 example and source-footer entry | CLEAN | CLEAN | CLEAN |
| `kanji\血.md`: 血液 links; 血圧 example and source-footer entry | CLEAN | CLEAN | CLEAN |
| `kanji\液.md`: 血液 common-word link | CLEAN | CLEAN | CLEAN |

The four reciprocal word/component pairs use the actual readings **けつあつ** and **けつえき**. All twenty new articles retain every written kanji in metadata and substantively link the existing component cards. The ten absent primary component cards are not metadata omissions or a requirement to create kanji/stroke files.

**Source mappings:** Each of the twenty mappings listed above is **CLEAN / CLEAN / CLEAN** for mapping correctness, scoped coverage, and comprehensibility. Every source spelling, reading, and applicable teaching meaning is explicitly covered—not merely matched by entry ID. In particular:

- 下水 teaches both drainage infrastructure and wastewater, respecting the different JMdict/Daijisen numbering.
- 削る correctly follows the agreeing **けずる / 1298090** identity rather than importing “take a percentage” from **はつる / 1298100:2**. Text deletion is separately additional.
- 桁 qualifies “column”; 傑作 explicitly teaches the qualified humorous sense; 気配 teaches market tone without promoting the unestablished raw “worry” gloss.
- 下品 and 険しい appropriately interpret their misleading raw glosses rather than teaching stinginess, a place noun, or keen eyesight.
- 蹴る’s refusal/foot-pressure senses and 見学’s PE sitting-out sense are explicitly additional, not independently assigned N2. The spelling/reading variants and rare/search-only qualifications inspected are preserved.

No actionable prerequisite, conjugation, particle, kana, translation, or whole-construction defect was otherwise established within the declared teaching scope.

## Findings

**N2B24-GPT-01 — Minor; correctness (quiz): missing direct 傑作/愉快 exclusion.**

**Locations:** `words\傑作.md:4,9,16–24`; `words\愉快.md:4,9,16–18`.

傑作’s explicitly taught humorous sense makes **“enjoyable; amusing”**, 愉快’s actual title, a defensible alternative English answer. The titles differ, so exact-title deduplication does not protect this pair. Both cards’ existing exclusions involving 面白い do not establish a direct 傑作/愉快 exclusion. This can penalize recognition of the humorous sense rather than a vocabulary mistake.

**Minimal remedy:** Add `愉快` to 傑作’s `quiz_exclusions`; retain both accurate titles and the dated/jocular qualification.

**Evidence:** Packet JMdict **1253840:2**, “(unintentionally) hilarious”; inspected [Daijisen 傑作, sense 2](https://www.weblio.jp/content/傑作), describing absurdly comic conduct/speech; [Jisho’s JMdict-derived 愉快 entry](https://jisho.org/api/v1/search/words?keyword=%E6%84%89%E5%BF%AB), sense 1, explicitly including “amusing.” Pairwise behavior is specified in `docs\content-format.md:79–95`.

**Confidence:** High.

**N2B24-GPT-02 — Minor; correctness (quiz): 気配’s financial sense collides with 調子’s unqualified English label.**

**Locations:** `words\気配.md:4,9,22–24`; `words\調子.md:4,9,16–21`.

For 気配’s taught **market-tone** meaning, 調子’s displayed **“tone; condition”** is a defensible English answer. Neither card directly excludes the other. The body’s musical/physical examples for 調子 are not visible qualifications on that answer label. This is an English-label ambiguity, not a claim that 調子 freely substitutes for financial 気配.

**Minimal remedy:** Add `調子` to 気配’s `quiz_exclusions`, without changing the lexical explanations.

**Evidence:** Packet JMdict **1222510:2**, “tone (of the market)”; inspected [Daijisen けはい, sense 2](https://www.weblio.jp/content/気配), market/business conditions; the actual 調子 title above and its [JMdict-derived entry](https://jisho.org/api/v1/search/words?keyword=%E8%AA%BF%E5%AD%90), which separately records tone, mood/manner, condition, and trend. The quiz contract requires assessment of the displayed English labels, not unrestricted Japanese interchangeability.

**Confidence:** Medium-high.

**N2B24-GPT-03 — Minor; correctness (quiz): missing direct 原稿/テキスト exclusion.**

**Locations:** `words\原稿.md:4,9,16–21`; `words\テキスト.md:4,15–18`.

原稿 explicitly includes a prepared **text**, including presentation text. テキスト’s actual **“text; course textbook”** label therefore supplies a defensible alternative answer through its ordinary written-text meaning; it is not restricted to textbooks. Neither header excludes the pair. 原稿’s exclusion of 文章 does not protect it from テキスト.

**Minimal remedy:** Add `テキスト` to 原稿’s `quiz_exclusions`; preserve テキスト’s existing N4 identity and title.

**Evidence:** Packet JMdict **1261340:1**; 原稿’s own definition/examples; inspected [Daijisen 原稿, senses 1–2](https://www.weblio.jp/content/原稿), publication-source writing and speech drafts; inspected [Daijisen テキスト, senses 1 and 3](https://www.weblio.jp/content/テキスト), written/source text and computer-handled textual content.

**Confidence:** High.

## Optional

None.

## Limits

Git identity, cleanliness, hashes, and derivative equivalence remain receipt-backed rather than independently executed. Author-inspection receipts were treated as assertions; the public-entry evidence cited above was independently retrieved.

The comparison review used all supplied labels/exclusions and targeted lexical records/card bodies, **not a complete rereading of all 227 comparison families or every existing article**. Quiz findings establish reachable unguarded pairs under the documented selection contract; no app execution was available to measure their selection frequency.

The community N2 list is not an official modern JLPT syllabus. CLEAN means no actionable defect established within this reviewed scope—not exhaustive dictionary coverage, corpus attestation of every original example, or native-speaker certification.
