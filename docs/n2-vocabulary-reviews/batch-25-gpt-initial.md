## Snapshot: c6d44ce4b6dd2e8fceb2fa8ffae7c632ed87e801 — committed content only

The frozen receipt identifies this commit, with parent `3a3517322ec749d892e8fe5f97f4cac2a54431ae`, and asserts clean committed content. **File tools were available, but Git execution and independent hash calculation were not**; snapshot authentication therefore relies on that receipt.

## Scope: GPT-6.1 Sol; twenty articles, four related changes, twenty mappings

Actual model: **GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`**. I worked independently without agents or file edits.

I read all twenty articles completely, the actual four-file related patch and changed passages in context, all mappings N2:482–N2:501, the required instructions and format documentation, all twenty complete principal dictionary families, component evidence, and all 136 supplied comparison-label/exclusion records. I also inspected selected existing comparison articles and complete relevant dictionary records, and retrieved public dictionary bodies for consequential usage checks. I did **not** read all 307 comparison families or every comparison article body. No prohibited authoring rationale or other reviewer’s output was accessed.

## Verdicts: two quiz-correctness fixes

**CLEAN** means no actionable defect established within this scope—not exhaustive lexical or native-speaker certification. The two NEEDS FIX verdicts concern quiz choices, not the accuracy or clarity of the articles’ prose.

All article paths below are `words\<headword>.md`.

| Source row | Article / reading | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:482 | 原産 / げんさん | CLEAN | CLEAN | CLEAN |
| N2:483 | 原始 / げんし | CLEAN | CLEAN | CLEAN |
| N2:484 | 研修 / けんしゅう | CLEAN | CLEAN | CLEAN |
| N2:485 | 厳重 / げんじゅう | CLEAN | CLEAN | CLEAN |
| N2:486 | 謙遜 / けんそん | CLEAN | CLEAN | CLEAN |
| N2:487 | 県庁 / けんちょう | CLEAN | CLEAN | CLEAN |
| N2:488 | 限度 / げんど | CLEAN | CLEAN | CLEAN |
| N2:489 | 現に / げんに | CLEAN | CLEAN | CLEAN |
| N2:490 | 顕微鏡 / けんびきょう | CLEAN | CLEAN | CLEAN |
| N2:491 | 原理 / げんり | CLEAN | CLEAN | CLEAN |
| N2:492 | 原料 / げんりょう | CLEAN | CLEAN | CLEAN |
| N2:493 | 碁 / ご | CLEAN | CLEAN | CLEAN |
| N2:494 | 恋しい / こいしい | CLEAN | CLEAN | CLEAN |
| N2:495 | 請う / こう | **NEEDS FIX** | CLEAN | CLEAN |
| N2:496 | 工員 / こういん | CLEAN | CLEAN | CLEAN |
| N2:497 | 強引 / ごういん | CLEAN | CLEAN | CLEAN |
| N2:498 | 公害 / こうがい | CLEAN | CLEAN | CLEAN |
| N2:499 | 高級 / こうきゅう | CLEAN | CLEAN | CLEAN |
| N2:500 | 公共 / こうきょう | **NEEDS FIX** | CLEAN | CLEAN |
| N2:501 | 工芸 / こうげい | CLEAN | CLEAN | CLEAN |

**Source mappings:** Each of the twenty mappings listed above is **CLEAN / CLEAN / CLEAN** for correctness, scoped coverage and comprehensibility. Exact source spellings/readings and applicable meanings are explicitly taught. In particular:

- 原産 qualifies “habitat” as native provenance; 厳重 qualifies severity/firmness through strict handling and warnings; 現に qualifies “really” as factuality; 原理 positively teaches the applicable explanatory-theory meaning.
- 原始 teaches both selected meaning areas. 恋しい explains the longing required by the broad affection glosses. 公共 retains the society/community/public-service area with appropriate constructions rather than equating it with every community group.
- 請う’s prayer/wishing sense and 高級’s rank sense are explicitly additional, not independently assigned N2. 高級 preserves the sense-specific grammatical distinction. 工芸 covers techniques as well as useful/aesthetic making and works.

The level provenance is a pinned **community vocabulary list**, not an official modern JLPT syllabus. No easier-level identity replacement was established; unrelated こう and 郊外 remain distinct.

**Related kanji changes:**

| Changed passages | Correctness | Scoped coverage | Comprehensibility | Assessment |
|---|---|---|---|---|
| `kanji\県.md:36,44` | CLEAN | CLEAN | CLEAN | 県庁 supplies ケン and the matching source entry. |
| `kanji\庁.md:38,46` | CLEAN | CLEAN | CLEAN | 県庁 supplies チョウ and the matching source entry. |
| `kanji\恋.md:20,31,37` | CLEAN | CLEAN | CLEAN | Reciprocal 恋しい links use native こい.しい and correctly allow nonromantic longing. |
| `kanji\芸.md:43,52` | CLEAN | CLEAN | CLEAN | 工芸 supplies ゲイ and the matching source entry. |

All primary written-kanji components are retained in word metadata. Missing component cards were not replaced with invented files. The four existing N2 components needing these reciprocal examples receive them at the actual readings.

## Findings: two medium-severity correctness defects

**GPT25-01 — MEDIUM — Correctness: 請う and 拝む remain mutually eligible despite their shared “beg” meaning.**

**Locations:** `words\請う.md:4–9`; counterpart `words\拝む.md:4–9,16–18`.

The actual labels are **“beg; request; invite”** and **“worship; beg”**. Begging is explicitly taught on both cards, but neither directly excludes the other. Their shared exclusions through 頼む, 願う or 祈る do not protect this pair. A learner can therefore encounter a defensible alternative answer to a meaning question.

**Minimal remedy:** Add `拝む` to 請う’s `quiz_exclusions`, or declare the reverse pair on 拝む. One declaration suffices; retain both accurate meanings and titles.

**Evidence:** Supplied complete JMdict entry **1592920, sense 1** supports 請う’s begging meaning. Independently retrieved [精選版日本国語大辞典「拝む」](https://kotobank.jp/word/拝む), sense ⑤, defines earnest entreaty/supplication. This corroborates the existing card’s ordinary begging use, rather than merely associating both words with prayer. `docs\content-format.md:79–99` specifies semantic title review and symmetric, nontransitive exclusions. **Confidence: high.**

**GPT25-02 — MEDIUM — Correctness: 公共 lacks a direct guard against 世の中’s society label.**

**Locations:** `words\公共.md:4–9,16–19`; counterpart `words\世の中.md:4–9,16–17`.

公共’s label is **“public; communal”**; 世の中’s is **“society; the world”**. 公共’s taught and dictionary-supported noun meaning includes society generally/the public. Consequently, 世の中’s “society” label remains a reasonable answer for 公共 in a context-free meaning question. This is actual semantic overlap, not merely a shared social topic. Neither card directly excludes the other; links through 社会 or 世間 are nontransitive.

**Minimal remedy:** Add `世の中` to 公共’s `quiz_exclusions`, or declare the reverse pair.

**Evidence:** The actual retrieved [Daijisen entry 「公共」 via Weblio](https://www.weblio.jp/content/公共) defines it as society generally/the public and society-wide involvement. Independently retrieved [精選版日本国語大辞典「世の中」](https://kotobank.jp/word/世の中), section 一③, identifies human social life, society and 世間. The actual card labels and exclusion lists establish the unguarded pair under `docs\content-format.md:79–99`. **Confidence: high.**

## Optional: none

## Limits: snapshot authentication and selective comparison coverage

I could not independently authenticate the checkout against the commit, execute the supplied hashes, or verify the evidence derivative’s equivalence. Those remain receipt assertions.

Comparison review was selective beyond the 136 supplied label/exclusion records; this is not whole-repository certification of every possible distractor or ordinary secondary sense. Quiz consequences were assessed against the documented semantics, not an executed application.

Public lexical checks were also selective. Heading-only, irrelevant or unsuccessfully simplified fetches were not counted as lexical verification; the findings above rely on retrieved lexical bodies. Author-inspection receipts were treated as assertions, not independent retrieval.
