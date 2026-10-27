## Snapshot: 54b4f9d77337e80b47f42b9a0b7a9acd6f8eb846; committed content only

**Seven articles need localized quiz-exclusion fixes. No actionable defect was established in the twenty source mappings or four kanji edits.**

Parent: `51d5355510987eef1816e164903d8c1ec6907067`. The frozen manifest declares clean committed content. File tools cannot execute Git, so I could not independently establish that the accessible files match those committed blobs or verify the absence of unrelated changes. No repository or supplied-evidence edits were made.

## Scope: gpt-6.1-sol; family gpt

Independent review, without agents or delegation. Read completely: all twenty assigned articles; `kanji\池.md`, `kanji\柱.md`, `kanji\波.md`, `kanji\銅.md`; and `related.patch`.

Read the required repository instructions, `docs\content-format.md:18-103`, both allowed snapshot files, `docs\confusable-words.md`, `docs\jlpt-levels.md`, and the TSV header plus exactly the twenty assigned rows. Inspected all twenty mappings and complete principal records, including raw fields, restrictions, flags, inherited POS, and selected/additional senses.

Private evidence references below use the supplied exact prefix:

`C:\Users\romanko\.copilot\session-state\b6f215e3-8bdf-4125-a626-75bc6c871123\files\n2-vocabulary\batch-59-`

Completely read `frozen-snapshot.json` first, then the permitted compact mappings/principals/components/labels renderings, all nine family-inspection chunks, both comparison supplements, and both public-bodies files. This includes the twenty principal families/31 senses, 29 component records, and 231 labels/exclusions. The large `review-evidence.json` was not read separately; the supplied equivalent renderings were used. No prohibited ledgers, rationale-bearing batch JSON, scripts, or reviewer reports were read.

**Complete older-body inspection: 112 distinct `words\<word>.md` files**, not the author’s reported inspection count:

- 電灯、電気、明かり、灯、光、蛍光灯、スタンド、乾電池、柱、棒、波、信号、サイン、合図、直流、交流、流れ、力、エネルギー
- 点、成績、数、数字、採点、評価、移る、伝わる、流行、病気、あちこち、方々、ぽつぽつ、ぱらぱら、ごろごろ、印、記号、徐々に、散らかる、転がる
- 移動、引っ越す、転ぶ、ころころ、くるくる、回す、王、国王、王様、金属、銅貨、金、鉄、銀、どう、一致、合同、揃える、合わせる
- 同じ、平等、同様、同一、等しい、イコール、匹敵、相当、地位、質問、問い、問題、疑問、聞く、尋ねる、調査、相談、返事
- 山、頂上、盛り、計算、資料、行動、運動、活動、態度、操作、動く、働く、働き、機能、運転、作業、行儀、真似、自動、様
- 揃う、合う、頂点、速度、速力、調子、東、西、全国、西洋、欧米、世界、作法、礼儀、エチケット、手術

Also inspected exact-filename component/comparison availability and a bounded semantic-title search within `words\`. Labels and search hits were not counted as complete article reads.

The twenty supplied public captures were inspected as captures from **one dictionary service**, separating relevant headings from mixed results. Additional live evidence was read from Kotobank for 採点、合図、転がる、散らかる、速力、揃う、頂点 and the complete relevant **よう** headings under 様, plus Jisho’s complete relevant サイン records.

## Verdicts: twenty source rows, kanji edits, metadata, and mappings

**Correctness includes quiz configuration.** The NEEDS FIX judgments below concern quiz metadata, not an established error in the article’s Japanese explanation. Scoped coverage and comprehensibility assess the teaching body separately.

Mapping notation: `entry:selected senses`; `+` identifies additional mapped senses. Sense numbers are one-based. Every mapping verdict is **CLEAN**; additional senses are not treated as independently sourced N2 labels.

| Source row | Exact article | Correctness | Scoped coverage | Comprehensibility | Mapping |
|---|---|---|---|---|---|
| N2:1162 | `words\電球.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1443170:1 |
| N2:1163 | `words\点数.md` | NEEDS FIX — F01 | CLEAN | CLEAN | CLEAN — 1441660:1 +2 |
| N2:1164 | `words\伝染.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1442110:1 |
| N2:1165 | `words\電池.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1443620:1 |
| N2:1166 | `words\点々.md` | NEEDS FIX — F02 | CLEAN | CLEAN | CLEAN — 1598460:1 +2 |
| N2:1167 | `words\転々.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1704220:1 +2 |
| N2:1168 | `words\電柱.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1443630:1 |
| N2:1169 | `words\天皇.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1582030:1 |
| N2:1170 | `words\電波.md` | NEEDS FIX — F03 | CLEAN | CLEAN | CLEAN — 1443720:1 +2 |
| N2:1171 | `words\テンポ.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1081120:1 |
| N2:1172 | `words\電流.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1443790:1 |
| N2:1173 | `words\電力.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1443810:1 |
| N2:1174 | `words\問い合わせ.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1598590:1 |
| N2:1175 | `words\銅.md` | NEEDS FIX — F07 | CLEAN | CLEAN | CLEAN — 1582390:1 +2 |
| N2:1176 | `words\統一.md` | NEEDS FIX — F04 | CLEAN | CLEAN | CLEAN — 1449670:1 |
| N2:1177 | `words\同格.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1452000:1 +2 |
| N2:1178 | `words\峠.md` | NEEDS FIX — F05 | CLEAN | CLEAN | CLEAN — 1454420:1,2 |
| N2:1179 | `words\統計.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1449710:1 |
| N2:1180 | `words\動作.md` | NEEDS FIX — F06 | CLEAN | CLEAN | CLEAN — 1451350:1,2,3 |
| N2:1181 | `words\東西.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1447910:1,2 +3 |

All twenty explicitly teach the assigned source spelling, reading, and applicable meaning. The material distinctions are appropriately bounded: bulb versus fixture; rechargeable versus disposable batteries; overhead-wire poles; scores versus item counts; scattered appearances versus successive movement/rolling; current versus power versus energy; inquiry noun patterns; transitive unification; grammatical apposition; passes versus summits; and bodily versus machine 動作.

The consequential restrictions are preserved: actual **てんのう** and its 連声 explanation, without an unrestricted 皇ノウ reading; ordinary radio **でんぱ** versus kana-only slang forms; copper spelling/reading restrictions and **どう**-only medal abbreviation; obsolete **ひがしにし** and the **とうざい**-restricted attention call. テンポ’s pace use has separate public support. 統計 correctly teaches statistics while the erroneous raw gloss remains provenance, not teaching.

| Related card | Correctness | Scoped coverage | Comprehensibility | Required reciprocal evidence |
|---|---|---|---|---|
| `kanji\池.md` | CLEAN | CLEAN | CLEAN | 電池 **でんち**: word-side introduction; reading row `:30`; Common words `:36` |
| `kanji\柱.md` | CLEAN | CLEAN | CLEAN | 電柱 **でんちゅう**: word-side introduction; reading row `:28`; Common words `:35` |
| `kanji\波.md` | CLEAN | CLEAN | CLEAN | 電波 **でんぱ**: word-side introduction; reading row `:30`; Common words `:37`; word explains ハ→ぱ |
| `kanji\銅.md` | CLEAN | CLEAN | CLEAN | 銅 **どう**: word-side introduction; reading row `:30`; Common words `:36`; あかがね also linked separately |

**Metadata preservation:** CLEAN against the supplied related patch: all four kanji headers are unchanged, including stable IDs, levels, readings, strokes, radicals, and distractors. All primary written Han are represented in the twenty word headers, and existing primary component cards receive substantive links. Missing 染・皇・統・峠 cards are not fabricated. The existing `words\どう.md` remains the unrelated “how” adverb with `jlpt: 5`; it has not been conflated with copper in the inspected content.

**Repository-wide preservation against the parent commit: UNVERIFIED**, because Git/blob comparison was unavailable. The supplied declaration of no reused word edits was not independently executed or reconstructed as a Git check.

## Findings: stable IDs, impact, remedies, and evidence

The governing behavior is `docs\content-format.md:79-96`: different title strings do not establish semantic uniqueness; exclusions are symmetric, apply among choices, and are nontransitive. Each missing pair below exposes an acceptable alternative in at least one quiz direction. Existing intermediary guards do not protect it.

**F01 — Minor; correctness / missing quiz exclusion; `words\点数.md:4,9`.**

**Claim/impact:** 点数 is not guarded against 採点’s ordinary result-noun sense. A quiz asking about 採点 can therefore offer both its own “marking; grading; scoring” and 点数’s “score; number of items” as defensible answers.

**Minimal remedy:** Add `採点` to 点数’s exclusions.

**Exact evidence:** Complete `words\採点.md`, especially `:4,9,21`, explicitly recognizes the assigned score itself. Independently retrieved [Digital Daijisen and Seisenban 採点](https://kotobank.jp/word/採点-508119) both include the resulting assigned points, not only the marking activity. Neither card declares this pair.

**Confidence:** High.

**F02 — Minor; correctness / missing quiz exclusions; `words\点々.md:4,9,16`.**

**Claim/impact:** The scattered-distribution title remains exposed against **散らかる** and the static secondary sense of **転がる**. This is not the rolling sense or merely a shared character: both older words have actual “lying scattered around” uses.

**Minimal remedy:** Add `散らかる` and `転がる` to 点々’s exclusions.

**Exact evidence:** `words\散らかる.md:4,9,16-20`; `words\転がる.md:4,9,38`. Complete JMdict 1441000, sense 4, explicitly records being scattered about/lying around (`batch-59-family-inspection-05.txt:2-10`). Live [転がる](https://kotobank.jp/word/転がる-505534), Daijisen 4㋐, and [散らかる](https://kotobank.jp/word/散らかる-569640), Seisenban ③, corroborate the static uses. Untidiness is an additional implication of 散らかる, not a reason the broader English “scattered here and there” becomes an unequivocally wrong answer.

**Confidence:** High.

**F03 — Minor; correctness / displayed-label ambiguity; `words\電波.md:4,9`.**

**Claim/impact:** 電波’s unqualified title branch **“signal”** remains exposed against **サイン** and **合図**. Their titles also offer ordinary “signal” meanings. The radio-versus-cue distinctions in the bodies do not appear in the competing English labels. This does **not** mean the Japanese words are freely interchangeable.

**Minimal remedy:** Add `サイン` and `合図` to 電波’s exclusions, or qualify the English labels enough to remove the ambiguity and reassess the pairs.

**Exact evidence:** Complete `words\サイン.md:4,9` and `words\合図.md:4,9`; neither guards 電波. Principal JMdict 1443720:1 supplies reception/signal alongside radio wave. The live [Jisho サイン response](https://jisho.org/api/v1/search/words?keyword=サイン) separately records sign/signal/indication, distinct from mathematical sine; [Nipponica 合図](https://kotobank.jp/word/合図-421387) documents signaling/cues. Guards through 信号 or through サイン/合図 are nontransitive.

**Confidence:** Medium-high, specifically for the displayed-label ambiguity.

**F04 — Minor; correctness / missing quiz exclusion; `words\統一.md:4,9`.**

**Claim/impact:** The **uniformity** sense remains exposed against **揃う**’s ordinary matching/uniform-state sense. Excluding 揃える does not exclude its intransitive counterpart. A noun/verb difference alone does not make these meaning choices unambiguous.

**Minimal remedy:** Add `揃う` to 統一’s exclusions.

**Exact evidence:** Complete `words\揃う.md:4,9,22,44-47`, including the explicit “boxes are uniform in size” example and unison use. Complete principal JMdict 1449670:1 includes uniformity. Live [Seisenban 揃う](https://kotobank.jp/word/揃う-555686), intransitive ①–②, records becoming equal/the same and coming into unity. Neither declaration guards this pair.

**Confidence:** High.

**F05 — Minor; correctness / missing quiz exclusion; `words\峠.md:4,9,17-20`.**

**Claim/impact:** **頂点** is unguarded despite its ordinary figurative peak/climax sense. The overlap concerns a development’s peak, not a mistaken equation of a mountain pass with a mountain summit. Existing guards through 頂上, 盛り, or 山 do not protect this pair.

**Minimal remedy:** Add `頂点` to 峠’s exclusions.

**Exact evidence:** Complete `words\頂点.md:4,9,16-17,44-47`; complete principal JMdict 1454420:2; live [Seisenban 頂点](https://kotobank.jp/word/頂点-98104), sense ②, records a climax or extreme point. Neither card declares 峠/頂点.

**Confidence:** High.

**F06 — Minor; correctness / missing quiz exclusions; `words\動作.md:4,9,16`.**

**Claim/impact:** Two displayed-label overlaps remain: **移動** supplies ordinary “movement,” and **様** supplies unqualified “manner,” which can answer 動作’s bearing/manner sense. The latter is a label problem, not permission to substitute bare よう for 動作 in Japanese constructions.

**Minimal remedy:** Add `移動` and `様` to 動作’s exclusions.

**Exact evidence:** Complete `words\移動.md:4,15,28` and `words\様.md:4,9,16-22`; complete JMdict 1158400:1 (`batch-59-family-inspection-02.txt:32-36`) and principal 1451350:1–2. 動作 itself explicitly introduces bodily movement and manner of moving at `:16`. The relevant live **よう** headings under [様](https://kotobank.jp/word/様-511903) were distinguished from unrelated **さま** headings. Neither older card supplies the missing guard.

**Confidence:** High for 移動; medium-high for the English “manner” ambiguity.

**F07 — Minor; correctness / excessive quiz exclusion; `words\銅.md:9,32`.**

**Claim/impact:** The 銅/金属 guard suppresses a category/member distinction without an established overlapping lexical sense. Copper is a metal, but that fact alone does not make “metal” and “copper; bronze medal (abbreviation)” equivalent answer labels. It unnecessarily removes distinguishable choices and can reduce a constrained pool.

**Minimal remedy:** Remove `金属` from 銅’s exclusions; retain the useful broader-category comparison in the body.

**Exact evidence:** Complete principal JMdict 1582390 contains copper and the restricted bronze-medal abbreviation, not generic metal. Complete JMdict 1243040 contains metal (`batch-59-family-inspection-02.txt:124-127`). Complete `words\金属.md:4,15` describes the material/class; 銅’s own `:32` correctly calls it the broader category. No copper-specific secondary sense of 金属 or generic-metal sense of 銅 was established.

**Confidence:** High.

## Optional: none

No additional expansion is required for the assigned practical scope. In particular, the evidence does not justify turning the two てんてん families into a homophone exclusion, treating current and power as interchangeable, expanding 東西 into unrestricted 全国, or making an etiquette-wide exclusion clique around 動作.

## Limits: provenance, corpus coverage, and retrieval boundaries

- **Git limitation:** Commit identity and clean-committed-content status come from the frozen declaration. Checkout/blob identity, the complete parent diff, and repository-wide preservation remain unverified. Author-executed hash/equivalence checks were not independently executed.
- **Coverage boundary:** All assigned bodies, four related cards, and twenty mappings were read completely. The 231 labels are not 231 complete-body inspections. Older bodies outside the explicit 112-file inventory and uninspected corpus-wide secondary senses remain outside these CLEAN judgments.
- **Public evidence boundary:** The supplied twenty captures are one service, not twenty independent dictionaries or fresh reviewer retrievals. A fresh Weblio 採点 extraction returned irrelevant Wikipedia material; Kotobank サイン returned 404. Neither was counted as verification; the consequential claims were checked through the successful alternatives cited above.
- **Heading boundary:** Several live Kotobank Daijisen sections contained headings without definitions; only actual returned dictionary text was used. The 様 page continued into unrelated material and was truncated after the complete relevant よう entries; no whole-page completeness is claimed.
- CLEAN means no actionable defect established within this actual scope, not exhaustive correctness, complete quiz-pool certification, or native-speaker certification.
