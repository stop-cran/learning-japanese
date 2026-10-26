## Snapshot: `4693f23da69e63b383e068163a606d6e1e0b94f9`; committed content only

Parent: `8e0a6f058a1d2e3c62d3402cc6ceb7dceb841eff`.

These identifiers and the clean-commit status come from the supplied author-executed receipts. I did not independently execute Git or verify hashes.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), GPT family

Read completely: the supplied review/structure instructions and word-format contract; all twenty raw mappings, twenty complete principal dictionary families, 42 component records, 219 comparison labels, twenty assigned articles, four related kanji bodies, the exact six-file teaching patch, and all 21 public lexical wrappers. The public wrappers represent **one dictionary authority**, not 21 independent authorities.

Additional complete reads: `docs\confusable-words.md`, `docs\jlpt-levels.md`, `kanji\用.md`, and ten older word bodies—うれしい, 汚染, いよいよ, 楽しみ, 祝う, 歓迎, 預ける, 開く, けち, わがまま. Inspected their applicable complete comparison families: 1219510, 1179040, 1587670, 1207250, 1337390, 1212960, 1544990, 1202440, 2234080 and 1197020. Also performed targeted component-metadata checks and dictionary navigation.

Used 32 serial tool calls, with no agents, delegation, edits, shell execution or concurrent work. Did not read prohibited ledgers, author rationale, scripts, source-note columns or other reviewer reports. Did not exhaustively reread the 426-family union or the 165 available older bodies. Two live public-page attempts yielded no usable lexical verification.

## Verdicts: Four rows need quiz-coverage fixes

**Correctness** below assesses the teaching and lexical assertions. Missing required quiz safeguards are recorded under **Scoped coverage**; CLEAN correctness cells do not certify quiz-answer uniqueness.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
| --- | --- | --- | --- | --- | --- |
| N2:1742 用途 | `words\用途.md` | CLEAN | CLEAN | CLEAN | Correctly teaches use/intended purpose rather than mechanically copying “usefulness.” |
| N2:1743 洋品店 | `words\洋品店.md` | CLEAN | CLEAN | CLEAN | Apparel/accessories scope matches 洋品 sense 1; does not transfer the separate imported-goods sense. |
| N2:1744 養分 | `words\養分.md` | CLEAN | CLEAN | CLEAN | Nutrients/nourishment and absorption examples are clear; no false plants-only restriction. |
| N2:1745 羊毛 | `words\羊毛.md` | CLEAN | CLEAN | CLEAN | Covers fleece and textile material, distinguishing fibre from yarn. |
| N2:1746 漸く | `words\ようやく.md` | CLEAN | CLEAN | CLEAN | Explicitly recognizes 漸く; teaches finally, barely and gradually without importing historical “slowly” as the main lesson. |
| N2:1747 要領 | `words\要領.md` | CLEAN | CLEAN | CLEAN | Gist and practical knack are distinguished; contextual criticism is qualified. |
| N2:1748 欲張り | `words\欲張り.md` | CLEAN | CLEAN | CLEAN | Noun/な-adjective usage and on-first mixed formation are explained without invented history. |
| N2:1749 余計 | `words\余計.md` | CLEAN | NEEDS FIX | CLEAN | Direct いよいよ exclusion is missing: B88-GPT-01. |
| N2:1750 よこす | `words\よこす.md` | CLEAN | CLEAN | CLEAN | Speakerward direction, blunt request and て-form auxiliary are appropriately qualified. |
| N2:1751 汚す | `words\汚す.md` | CLEAN | NEEDS FIX | CLEAN | Reading restrictions and figurative overlap are accurate; inherited 汚染 quiz gap: B88-GPT-02. |
| N2:1752 寄せる | `words\寄せる.md` | CLEAN | CLEAN | CLEAN | Practical constructions cover the source meanings; the wave use is supported by the public よせる entry despite JMdict’s transitivity tagging. |
| N2:1753 余所 | `words\よそ.md` | CLEAN | CLEAN | CLEAN | Source spelling, social/spatial meanings and ～をよそに construction are explicit. |
| N2:1754 四つ角 | `words\四つ角.md` | CLEAN | CLEAN | CLEAN | Both source meanings are taught; よつかど versus independent よっつ is clear. |
| N2:1755 酔っ払い | `words\酔っ払い.md` | CLEAN | CLEAN | CLEAN | Person/state meanings are covered without equating temporary drunkenness with dependence. |
| N2:1756 予備 | `words\予備.md` | CLEAN | CLEAN | CLEAN | Reserve and preliminary preparation are covered; の versus な guidance is usable. |
| N2:1757 呼び掛ける | `words\呼び掛ける.md` | CLEAN | CLEAN | CLEAN | Calling/addressing and appeals are distinguished, with appropriate に/を patterns. |
| N2:1758 呼び出す | `words\呼び出す.md` | CLEAN | CLEAN | CLEAN | Summoning and computing uses are supported; 開く comparison correctly identifies ひらく. |
| N2:1759 蘇る | `words\蘇る.md` | CLEAN | CLEAN | CLEAN | Intransitive godan conjugation, revival and returning memories are clearly taught. |
| N2:1760 慶び | `words\喜び.md` | CLEAN | NEEDS FIX | CLEAN | Rare-spelling recognition and N3 identity are preserved; inherited 楽しみ quiz gap: B88-GPT-03. |
| N2:1761 慶ぶ | `words\喜ぶ.md` | CLEAN | NEEDS FIX | CLEAN | Dictionary-backed recognition is compatible with the blank raw gloss; inherited quiz gaps: B88-GPT-04. |

**Mappings — CLEAN within lexical scope.** All twenty supplied mappings have compatible written forms, readings and teaching anchors. 漸く→ようやく and 余所→よそ are explicitly taught normalizations. 慶び/慶ぶ are recognized rare spellings of the retained 喜び/喜ぶ identities, not asserted separate N2 words. The empty 慶ぶ gloss does not establish the original compiler’s intended sense, but the chosen delight/rejoicing anchor is supported by the unrestricted よろこぶ family.

**Baseline preservation — CLEAN against the supplied exact patch.** 汚す changes only by adding `jlpt: 2`. 喜び and 喜ぶ retain their original metadata, N3/N4 levels, identities, readings, titles, exclusion state and existing teaching; their changes are recognition paragraphs only. The quiz findings below are therefore inherited gaps, not regressions introduced by those recognition additions.

**Kanji preservation, components and reciprocity — CLEAN within the supplied patch and targeted inventory.** Every written primary Han character appears in the corresponding word metadata. Existing substantive component links are present; absent component cards are not fabricated, and whole-word spellings do not acquire invented constituent readings. The scoped reciprocal links are present at:

- 毛/羊毛: `kanji\毛.md:36` ↔ `words\羊毛.md:27`.
- 領/要領: `kanji\領.md:38` ↔ `words\要領.md:29`.
- 角/四つ角: `kanji\角.md:36` ↔ `words\四つ角.md:28`.
- 汚/汚す: `kanji\汚.md:34,42` ↔ `words\汚す.md:28`.

The patch preserves all four kanji headers and unrelated teaching. 毛, 領 and 角 receive only their new linked word and dictionary-entry reference; 汚 is unchanged.

No excessive declaration was established in the fully inspected comparisons. In particular, 呼び出す/開く is justified by the older article’s additional ひらく identity and complete family 1202440, sense 10, “open a file”; judging only the primary あく reading would incorrectly reject that safeguard.

## Findings: Required direct quiz safeguards

**B88-GPT-01 — Medium; scoped coverage.**  
**Location:** `words\余計.md:9,16–22`; `words\いよいよ.md:4,9,16–21`.

余計 and いよいよ remain eligible together despite a direct increasing-degree overlap. Complete family **1544090:3** gives 余計 “all the more; even more”; complete family **1587670:1** gives いよいよ “more and more; all the more; increasingly,” without a spelling, reading or register restriction separating this use. The whole older article explicitly teaches that increasing-degree meaning.

Their titles differ, so exact-title deduplication does not protect them. Existing exclusions through もっと, 一層 or ますます are not transitive. A meaning quiz can consequently offer two defensible answers. **Minimal remedy:** declare the direct 余計/いよいよ pair on either card. **Confidence: high.**

**B88-GPT-02 — Medium; scoped coverage; inherited baseline gap.**  
**Location:** `words\汚す.md:9,39–41,46–50`; `words\汚染.md:1–9,15–23`.

Neither card excludes the other, although applicable よごす family **1178960:1** explicitly includes “pollute; contaminate,” and complete 汚染 family **1179040:1** supplies “pollution; contamination” with する-verb usage. The older 汚染 body demonstrates actual transitive pollution of a river, not merely a thematic association with dirt. The public **よごす【汚す】** entry independently includes dirtying water.

The differing “soil; stain” and “pollution; contamination” titles do not make these safe opposing answers. The exclusion 汚す/汚れる provides no transitive protection. **Minimal remedy:** add 汚す to 汚染’s exclusions, preserving the assigned 汚す article’s level-only change. **Confidence: high.**

**B88-GPT-03 — Medium; scoped coverage; inherited baseline gap.**  
**Location:** `words\喜び.md:1–9,15,33`; `words\楽しみ.md:1–9,15–19`.

喜び and 楽しみ have no direct exclusion. Complete **1606140:1** includes joy, delight and pleasure; complete **1207250:1** includes enjoyment, pleasure, delight and joy. 楽しみ’s whole older body expressly teaches present enjoyment and illustrates a daily pleasure; its additional anticipation sense does not remove the ordinary overlap.

Thus “joy; delight” can reasonably answer 楽しみ, while enjoyment/pleasure can answer 喜び. Different titles prevent automatic deduplication. **Minimal remedy:** add 喜び to 楽しみ’s exclusions, leaving the preserved 喜び header untouched. **Confidence: high.**

**B88-GPT-04 — Medium; scoped coverage; inherited baseline gaps.**  
**Location:** `words\喜ぶ.md:1–9,15–19,35–45`; `words\うれしい.md:1–9,15–20`; `words\祝う.md:1–9,15–22`; `words\歓迎.md:9,16–24`.

Three direct overlaps remain unprotected:

| Pair | Precise evidence |
| --- | --- |
| 喜ぶ/うれしい | **1218760:1**: delighted/glad/pleased; complete **1219510:1**: happy/glad/pleased/delighted. The older body teaches the same positive reaction. Verb versus adjective does not make their displayed labels safe alternatives. |
| 喜ぶ/祝う | Ordinary, unrestricted **1218760:2**: “congratulate”; complete **1337390:1**: celebrate/congratulate. The older body explicitly teaches congratulating someone on an event. |
| 喜ぶ/歓迎 | Ordinary, unrestricted **1218760:3**: welcome a proposal/advice, take kindly to; complete **1212960:1**: welcome/reception. The older body explicitly demonstrates welcoming opinions, not only greeting visitors. |

The supplied public **よろこぶ【喜ぶ／悦ぶ／歓ぶ／慶ぶ】** heading also distinguishes accepting something favorably and congratulating someone. These are applicable senses, not transferred historical entries or restricted homographs.

Each pair can produce a defensible competing answer; protecting one does not protect the others. **Minimal remedy:** declare 喜ぶ on each of the three counterpart cards, preserving the assigned 喜ぶ metadata and keeping its practical lesson focused. **Confidence: high.**

## Optional: Nonblocking illustration

A translated gradual-change example would strengthen `words\ようやく.md:42–47`, since the two existing examples illustrate result attainment. The gradual meaning is already explicitly explained and dictionary-supported; this is not a coverage defect.

## Limits: Evidence and execution boundaries

File tools cannot independently execute Git, compute hashes or run the app. Snapshot identity, committed cleanliness and hash correspondence therefore remain supplied author receipts—not reviewer certification. The quiz consequences above follow from the supplied exclusion/deduplication contract; they were not reproduced in a running app.

The live Weblio いよいよ retrieval returned licensing material without the lexical entry; the Kotobank 愈々 request returned 404. Neither counts as verification. The corresponding finding rests on the complete frozen dictionary family and actual older body.

This was a complete read of the assigned evidence with selective consequential comparison retrieval, not exhaustive certification of all 426 families, 1,026 senses, 165 older bodies, corpus frequency, historical compiler intent or native-speaker naturalness. CLEAN means no actionable defect established in that actual scope.
