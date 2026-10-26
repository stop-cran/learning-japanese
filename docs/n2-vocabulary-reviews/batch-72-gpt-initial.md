## Snapshot: ded07a6f4969b3f63f2e62ae73511fade363ead1; committed content only

**Outcome: quiz-exclusion corrections are needed in five articles.** I found no actionable defect in the twenty source mappings, the required reciprocal kanji links, or the preservation of the existing 皮膚 article.

The frozen declaration identifies parent `a36e204d10a23de890c76655f8d2ac1b7954fac1`. This review uses the supplied committed-content evidence. File tools cannot execute Git, so I could not independently establish checkout cleanliness, commit contents, or hashes.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family gpt

This was read-only, without agents, delegation, or edits. I read:

- The frozen declaration first; all required instructions and `docs\content-format.md:18–103`; the two allowed source/snapshot JSON documents; and only TSV header line 1 and assigned physical lines 1422–1441.
- All twenty assigned articles completely; `related.patch`; complete `kanji\皮.md`, `kanji\準.md`, and unchanged `kanji\膚.md`.
- All twenty blind mappings and complete principal families, including raw fields, spelling/reading restrictions, flags, POS inheritance, and selected/additional senses; all 32 component records and 178 label/metadata records.
- All ten complete family-inspection renderings, the seven supplementary families, all thirteen complete older-body renderings, and both complete frozen public-capture renderings.
- Complete ordinary articles for 夜明け, 字, 文字, 拡張, 拡充, 増大, 伸びる, 散らかる, 散る, 揺れる, 騒ぎ, 代表, 住宅, 校舎, 寺院, 図鑑, 体積, and 休む. I also read the allowed confusables and JLPT documentation and performed narrowly scoped searches within `words\` and `kanji\`.

The large aggregate `review-evidence.json` was read only through line 100; its complete compact equivalents and bounded renderings supplied the substantive evidence instead. Labels were not counted as inspected article bodies. I did not access the excluded author rationale, ledgers, or other reviewers’ reports.

All twenty frozen public responses contained applicable **Digital Daijisen via Weblio** headings: one dictionary authority, not twenty independent dictionaries. Additional live retrievals supplied applicable Seisenban definitions for 拡張, 拡充, and ひびく. Retrieval limitations are recorded below.

## Verdicts:

The three facet columns assess each article, including its quiz metadata. **CLEAN** means no actionable defect established within this scope.

For **each of the twenty mappings individually**, correctness, scoped coverage, and comprehensibility are **CLEAN / CLEAN / CLEAN**. The entry and sense references in the notes identify those mapping judgments. “Additional” denotes separately assessed recognition coverage, not an independent N2 assignment.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1422 | 日の出 | CLEAN | CLEAN | CLEAN | Mapping 1463790:1. Sunrise event/time explicitly distinguished from dawn and daybreak. |
| N2:1423 | 響き | CLEAN | NEEDS FIX | CLEAN | Mapping 1602130:1–2; additional :3 appropriately explained. Missing effect-sense guards: F72-02. |
| N2:1424 | 響く | CLEAN | NEEDS FIX | CLEAN | Mapping 1238610:1; additional :2–4 qualified correctly, including figurative “come home.” Missing vibration-sense guard: F72-03. |
| N2:1425 | 皮膚 | CLEAN | CLEAN | CLEAN | Mapping 1483920:1. Supplied baseline comparison supports the required `jlpt: 2`-only change. |
| N2:1426 | 冷やす | CLEAN | CLEAN | CLEAN | Mapping 1556770:1; additional :2–3 contextualized. Transitivity, cooling comparisons, and whole fright idiom are handled appropriately. |
| N2:1427 | 百科事典 | CLEAN | CLEAN | CLEAN | Mapping 1602190:1. Blank source spelling retained; 百科事典 and 百科辞典 correctly identify the same family. |
| N2:1428 | 美容 | NEEDS FIX | CLEAN | CLEAN | Mapping 1486670:1; additional :2 covered separately. Prose distinguishes appearance/care from “beautiful”; two exclusions contradict that distinction: F72-04. |
| N2:1429 | 表紙 | CLEAN | CLEAN | CLEAN | Mapping 1489600:1; additional :2 explicitly slang. No front-only, paper-only, or detachable-jacket rule imposed. |
| N2:1430 | 標識 | CLEAN | CLEAN | CLEAN | Mapping 1488700:1; additional linguistic :2 qualified. Physical markers, signals, and indications are compared without unrestricted substitution. |
| N2:1431 | 標準 | CLEAN | CLEAN | CLEAN | Mapping 1488710:1; additional :2 covered. Overlap with 基準 acknowledged; no arithmetic-average or highest-quality rule. |
| N2:1432 | 標本 | CLEAN | CLEAN | CLEAN | Mapping 1488820:1–2; additional statistical :3 qualified. Specimen and classic-example coverage is adequate. |
| N2:1433 | 評論 | CLEAN | CLEAN | CLEAN | Mapping 1490080:1. Noun/transitive する construction and evaluative rather than necessarily hostile meaning are clear. |
| N2:1434 | 平仮名 | CLEAN | CLEAN | CLEAN | Mapping 1507090:1. Stable identity preserved with explicit usual ひらがな spelling; raw “47 syllables” is not taught as a modern count. |
| N2:1435 | ビルディング | CLEAN | CLEAN | CLEAN | Mapping 1106040:1. Blank source spelling retained; multistory-building scope, variant, and abbreviation are distinguished from construction activity. |
| N2:1436 | 昼寝 | CLEAN | CLEAN | CLEAN | Mapping 1426370:1. Daytime sleep and intransitive する taught without home-only, bed-only, or after-lunch restrictions. |
| N2:1437 | 広げる | CLEAN | NEEDS FIX | CLEAN | Mapping 1602370:1; additional :2–4 recognized. Grammar and physical/abstract distinctions are sound; expansion guards are incomplete: F72-01. |
| N2:1438 | 広さ | CLEAN | CLEAN | CLEAN | Mapping 1278440:1; additional :2 covered. Formation and spatial extent are clear without implying large size or square units exclusively. |
| N2:1439 | 広場 | CLEAN | CLEAN | CLEAN | Mapping 1278590:1; additional :2 recognized. Plaza, clearing, park, and figurative forum are usefully distinguished. |
| N2:1440 | 広々 | CLEAN | CLEAN | CLEAN | Mapping 1602380:1. Modern ひろびろ, actual attachment patterns, and iteration mark explained; archaic こうこう remains separate. |
| N2:1441 | 広める | CLEAN | NEEDS FIX | CLEAN | Mapping 1278460:1–2 correctly selects both propagation and broadening. Missing direct expansion guards: F72-01. |

**皮 edit — CLEAN / CLEAN / CLEAN.** `kanji\皮.md:28,35` now links 皮膚 at the actual whole-word reading **ひふ**. Footer line 45 already contains matching JMdict **1483920**. The supplied patch preserves existing headers and examples.

**準 edit — CLEAN / CLEAN / CLEAN.** `kanji\準.md:30,45` adds substantive 標準 links at **ひょうじゅん**; footer line 54 adds matching **1488710** while retaining existing IDs and examples.

**Unchanged 膚 — CLEAN / CLEAN / CLEAN.** Existing links at `kanji\膚.md:20,30,35` already establish 膚/皮膚 **ひふ**, and footer line 44 contains **1483920**. No edit is needed.

**Baseline preservation — CLEAN / CLEAN / CLEAN against the supplied baseline and patch.** The complete old 皮膚 body matches the reviewed body apart from the added level. Its identity, reading, title, and `[肌, 皮]` exclusions remain intact. Existing easier-level comparison cards were not changed by the supplied patch.

**Metadata and mapping details — CLEAN.** Every distinct primary written Han character is retained. Alternative spellings do not alter primary metadata; 々 is treated as an iteration mark. Existing component links are substantive, and missing component cards—including 典—are not invented. Both blank raw spellings remain blank in the mappings.

## Findings:

**F72-01 — Medium; scoped coverage; `words\広げる.md:9` and `words\広める.md:9`: missing direct expansion guards.**

The unguarded pairs are **広げる–拡張, 広める–拡張, 広げる–拡充, and 広める–拡充**. These are not inferred merely from an expansion-related exclusion clique. 広げる explicitly teaches widening a road, while the complete 拡張 card gives the same action. 広める’s selected second sense expressly includes broadening, extending, widening, and enlarging. 拡充’s complete card teaches expansion of facilities and services; its title includes the ordinary expansion sense.

The labels differ, so identical-title deduplication does not protect these pairs. Existing guards involving 拡大, 展開, or 広がる do not propagate to them.

**Minimal remedy:** add 拡張 and 拡充 to each new verb’s exclusions; one declaration per direct pair is sufficient.

**Exact evidence:** `words\広げる.md:16–25,36–41`; `words\広める.md:16–24,36–40`; `words\拡張.md:4,9,16–19,31`; `words\拡充.md:4,9,16–19,27–31`; complete JMdict **1602370:1** and **1278460:2**. The live Seisenban entries for [拡張](https://kotobank.jp/word/拡張-2302) and [拡充](https://kotobank.jp/word/拡充-460323) directly describe widening/expanding range or provision. **Confidence: high.**

**F72-02 — Medium; scoped coverage; `words\響き.md:9`: the effect/influence sense remains unguarded.**

**響き–影響** and **響き–効果** can present defensible competing answers. The applicable frozen **ひびき** heading—not どよめき—records influence/effect as sense 5, illustrated by an economic-impact example. The older answer labels are respectively “influence; effect” and “effect; effectiveness.” Neither reverse exclusion list supplies the missing pair.

This does **not** require adding that sense to the selected N2 lesson. It requires accounting for it when judging context-free quiz ambiguity. The guards declared on 響く are nontransitive and do not protect 響き.

**Minimal remedy:** add 影響 and 効果 to 響き’s exclusions.

**Exact evidence:** frozen `batch-72-public-bodies.txt`, **ひびき【響き】**, sense **5**; `words\響き.md:4,9`; complete `words\影響.md:4,9,16–27`; complete `words\効果.md:4,9,16–23,41–44`. **Confidence: high.**

**F72-03 — Medium; scoped coverage; `words\響く.md:9`: vibration recognition is not guarded against 揺れる.**

The complete principal family **1238610:2** explicitly includes reverberating, shaking, and vibrating. The article recognizes vibration at lines 24–26. The existing 揺れる answer label, **“shake; sway,”** therefore supplies a defensible first gloss for that recognition sense, but neither card excludes the other.

This judgment concerns the supported **shake/vibration** overlap, not a claim that 響く freely means “sway,” and not the separate どよめく reading.

**Minimal remedy:** add 揺れる to 響く’s exclusions.

**Exact evidence:** complete JMdict **1238610:2**, unrestricted at reading **ひびく**; `words\響く.md:9,24–26`; complete `words\揺れる.md:4,15–20` and its absence of a reverse guard. The frozen Daijisen **ひびく** heading, sense **4**, independently supports transmitted vibration. **Confidence: medium-high.**

**F72-04 — Low; correctness of quiz metadata; `words\美容.md:9`: two exclusions are excessive.**

The direct pairs **美容–美しい** and **美容–きれい** lack a defensible competing answer under their actual titles. “Beauty care; beautification” does not mean “beautiful” or “beautiful; clean.” Conversely, those adjectives do not name beauty care or beautification. 美容’s recognized beautiful-appearance/features sense remains a noun denoting appearance, not the general descriptive adjective.

This is a direct semantic and label judgment, not a blanket exemption based on differing POS. The article itself makes the useful distinction correctly at lines 38–39.

**Minimal remedy:** remove 美しい and きれい from 美容’s exclusions; retain 化粧.

**Exact evidence:** `words\美容.md:4,9,16–25,36–45`; complete JMdict **1486670:1–2**; complete `words\美しい.md:5,15–21,38–40`; complete `words\きれい.md:4,15–20,28–32`. Neither older body gives a beauty-care/beautification sense. **Confidence: high.**

## Optional:

None. Additional dictionary senses do not need to be expanded into the N2 teaching merely to address the quiz guards above.

## Limits:

I could not execute Git, independently recompute hashes/equivalence checks, or verify the author’s inspection chronology. Supplied receipts and preparation/completion statuses were not treated as my own checks or as proof of a contemporaneous pre-authoring gate.

I did not inspect every older article suggested by the navigation labels or exhaustively enumerate every possible quiz pair. Findings rely on complete relevant bodies and applicable lexical evidence, not labels alone.

Live Weblio retrievals for 響き/響く did not return useful lexical definitions; a live Kotobank 響き response was also irrelevant. Live 美容 and 代表 responses were encyclopedic and were not counted as lexical verification. The complete frozen applicable headings remained available. Dictionary recognition establishes supported senses, not frequency, unrestricted substitution, or native-speaker certification.
