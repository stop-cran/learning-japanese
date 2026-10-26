## Snapshot

**All four original GPT findings are resolved. One additional, pre-existing quiz-exclusion omission remains.**

Revised frozen commit: **`5398d39999695042b16b4af3c4c42fcad307c889`**. Parent/authored snapshot: **`ded07a6f4969b3f63f2e62ae73511fade363ead1`**.

This is a committed-content-only review against the supplied snapshot declaration and patch. File-only tools cannot execute Git; I did not independently establish HEAD, checkout cleanliness, hashes, or rendering equivalence. Those checks remain author-executed.

## Scope

Actual model: **GPT-6.1 Sol (`gpt-6.1-sol`), family gpt**. No edits, agents, delegation, or shell.

Fresh, complete reads covered:

- The correction snapshot first, then the complete correction patch and reconciliation.
- All twenty assigned current articles; complete current kanji cards **皮, 準, 膚**.
- All twenty mappings, twenty complete principal families/39 senses, and 32 component records.
- Only the TSV header and physical rows **1422–1441**.
- Complete correction comparison rendering—sixteen families/31 senses—the public-inspection summaries, and the complete original frozen public rendering, including the applicable **ひびき5, ひろげる6, ひので, ひろびろ** headings.
- Fourteen complete actual older articles: **拡張, 拡充, 揺れる, 美しい, きれい, 夜明け, 明け方, 日の入り, 暮れ, 伝える, 伝わる, 宣伝, 影響, 効果**.
- Both repository instruction files, `docs\content-format.md:18–103`, and `docs\confusable-words.md`.

I independently retrieved applicable **Seisenban** definitions for 拡張, 拡充, 伝える, 響く, and 伝わる. The 夜明け retrieval supplied encyclopedic context, not a fresh lexical definition; the 明け方 retrieval returned no applicable definition.

The original session’s complete ten family chunks, thirteen older-body chunks, supplement, and other comparison reads are inherited evidence—not fresh rereads. I did not reopen the optional correction evidence/receipt files or forbidden material. Author cumulative family/body counts and navigation-label counts are not substituted for my actual inspection depth.

## Verdicts

CLEAN means no actionable defect established within the stated scope, not exhaustive correctness.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1422 | 日の出 | CLEAN | CLEAN | CLEAN | Solar appearance/time distinguished from dawn. |
| N2:1423 | 響き | CLEAN | CLEAN | CLEAN | Both effect guards added; selected/additional footer clarified. |
| N2:1424 | 響く | CLEAN | NEEDS FIX | CLEAN | 揺れる fix accepted; additional 伝わる guard needed. |
| N2:1425 | 皮膚 | CLEAN | CLEAN | CLEAN | Existing identity, body, and 肌/皮 safeguards preserved. |
| N2:1426 | 冷やす | CLEAN | CLEAN | CLEAN | Cooling, transitivity, and contextual idioms appropriately distinguished. |
| N2:1427 | 百科事典 | CLEAN | CLEAN | CLEAN | Blank raw spelling retained; both encyclopedia spellings recognized. |
| N2:1428 | 美容 | CLEAN | CLEAN | CLEAN | Excess adjective guards removed; 化粧 retained. |
| N2:1429 | 表紙 | CLEAN | CLEAN | CLEAN | Not restricted to front covers or paper; slang separately qualified. |
| N2:1430 | 標識 | CLEAN | CLEAN | CLEAN | Sign/marker teaching and additional linguistic recognition remain scoped. |
| N2:1431 | 標準 | CLEAN | CLEAN | CLEAN | Reference standard and ordinary level distinguished; footer clarified. |
| N2:1432 | 標本 | CLEAN | CLEAN | CLEAN | 標準 removal accepted; specimen/example/statistical uses distinguished. |
| N2:1433 | 評論 | CLEAN | CLEAN | CLEAN | Critical assessment, noun/する usage, and translations remain sound. |
| N2:1434 | 平仮名 | CLEAN | CLEAN | CLEAN | Usually-kana spelling explicit; “47 syllables” not made a modern rule. |
| N2:1435 | ビルディング | CLEAN | CLEAN | CLEAN | Blank raw spelling retained; Japanese building sense appropriately scoped. |
| N2:1436 | 昼寝 | CLEAN | CLEAN | CLEAN | Daytime sleep taught without an at-home restriction. |
| N2:1437 | 広げる | CLEAN | CLEAN | CLEAN | Expansion additions and two removals accepted; 伝える retention accepted. |
| N2:1438 | 広さ | CLEAN | CLEAN | CLEAN | Extent/width and adjective-to-noun formation clearly distinguished. |
| N2:1439 | 広場 | CLEAN | CLEAN | CLEAN | Plaza, clearing, and figurative forum coverage appropriately qualified. |
| N2:1440 | 広々 | CLEAN | CLEAN | CLEAN | Both attachment variants explicit; examples preserved. |
| N2:1441 | 広める | CLEAN | CLEAN | CLEAN | Both source-selected senses retained; expansion guards added. |

**Kanji:** Both original edits remain CLEAN across correctness, scoped coverage, and comprehensibility. `kanji\皮.md:28,35,45` supplies reading-table/common-word links for **皮膚 ひふ**, with footer entry **1483920**. `kanji\準.md:30,45,54` supplies **標準 ひょうじゅん**, with **1488710**. Unchanged `kanji\膚.md:30,35,44` already supplies **皮膚 ひふ**, with **1483920**. Whole-word readings are correct; the supplied original patch preserved existing headers/examples, and the correction patch makes no further kanji changes.

**Mappings:** Each of the twenty mappings is CLEAN across all three facets. Associations, raw fields, restrictions/flags, inherited POS, and one-based selected/additional senses agree with the assigned TSV rows and complete families. Recognition does not acquire an independent N2 assignment. 広める correctly selects **1278460:1–2**.

**Baseline preservation:** Against the originally inspected baseline evidence at `a36e204d10a23de890c76655f8d2ac1b7954fac1`, 皮膚 remains a **`jlpt: 2`-only reuse**; its body, identity, reading, title, and `[肌, 皮]` remain intact. Primary kanji metadata remains complete, including characters without cards; no missing component card is invented, and 々 is not treated as a separate kanji. The supplied correction patch shows no identity, mapping, asset, or scene changes. The nineteen new cards currently contain **95 exclusion declarations**, apart from 皮膚’s two preserved declarations.

## Findings

**GPT-F72-01 — resolved.** Original severity: medium; facet: scoped coverage.

`words\広げる.md:9` and `words\広める.md:9` now each declare both 拡張 and 拡充. These are four independently supported pairs: **1602370:1** and **1278460:2** cover broadening/extension; `words\拡張.md:16–19` includes road widening, while `words\拡充.md:16–19` covers expanded facilities/services. Fresh Seisenban definitions support extending range/scale and fuller provision respectively. No expansion clique is inferred. **Confidence: high.**

**GPT-F72-02 — resolved.** Original severity: medium; facet: scoped coverage.

`words\響き.md:9` now declares 影響 and 効果. Applicable frozen **ひびき5** expressly records influence causing reaction/change, with the economic-impact example. Actual titles and complete bodies of `words\影響.md` and `words\効果.md` support the displayed effect answers. The mapping remains **1602130:1–2 selected, :3 additional**; the guard does not select another N2 sense. **Confidence: high.**

**GPT-F72-03 — resolved.** Original severity: medium; facet: scoped coverage.

`words\響く.md:9` now declares 揺れる. **1238610:2**, **1545710:1**, the full 揺れる body, and applicable frozen **ひびく4** support the shaking/vibration overlap. This does not equate 響く with every swaying or figurative-wavering use. **Confidence: high.**

**GPT-F72-04 — resolved.** Original severity: low; facet: correctness of quiz metadata.

`words\美容.md:9` removes 美しい and きれい while preserving 化粧. “Beauty care; beautification” is not the actual “beautiful” or “beautiful; clean” answer, including after considering **1486670:1–2**, **1486360:1**, **1591900:1–3**, and both complete older bodies. This is a lexical judgment, not a noun/adjective exemption. **Confidence: high.**

**Claude-F-01 — withdrawn as a defect in this confirmation; author’s decline accepted.**

`words\日の出.md:15–16,33–35`, `words\夜明け.md:15,30`, and `words\明け方.md:15–16` distinguish the sun’s appearance/time from the daylight transition. Complete **1463790:1**, **1537150:1**, **1532300:1**, and frozen ひので do not establish a direct competing translation for these actual labels. 夜明け/明け方 have identical titles and deduplicate with each other; that does not establish either edge to 日の出. Crucially, **1514950:1 explicitly includes sunset/sundown**, supporting 日の入り–暮れ independently rather than through a dusk/dawn analogy. No guard addition is required on this evidence. **Confidence: medium-high.**

**Claude-F-02 — resolved; 標本–標準 removal accepted.**

At `words\標本.md:9`, the edge is removed. Complete **1488710:1–2** and `words\標準.md:16–24,34–38` concern a reference criterion/model or ordinary level. Complete **1488820:1–3** and `words\標本.md:16–18,43–47` concern study specimens or descriptive representative/classic examples, not necessarily recommended models. Considering both full labels, the shared “model” neighborhood does not establish a directly defensible competing answer. Shared 標 and separate 典型 guards provide no transitive justification. **Confidence: medium-high.**

**Claude-F-03 — partially resolved; remaining removal recommendation withdrawn in this confirmation.**

At `words\広げる.md:9`, removing **伝わる** and **宣伝** is accepted: their actual transmitted/handed-down and publicity/advertising/propaganda labels do not directly translate this card’s spread-out/widen/unfold meanings merely because all concern dissemination.

I explicitly **accept retaining 伝える**. Applicable frozen **ひろげる6** positively records wide dissemination; complete **1441870:1** includes convey/impart/propagate, and `words\伝える.md:15–20` teaches conveying information. The fresh [Seisenban 伝える definition](https://kotobank.jp/word/伝える-571710), **[1]②(ハ)**, additionally records telling widely/spreading by telling. This is direct pair evidence—not inheritance through 広める, and not a claim of unrestricted substitution or frequency. **Confidence: high.**

**GPT-F72-05 — unresolved, newly identified pre-existing omission.**

**Severity:** medium. **Facet:** scoped coverage/quiz ambiguity.

**Location:** `words\響く.md:9,25–26`; compared with `words\伝わる.md:4,9,16–24,45`.

Neither card declares **響く–伝わる**, although the actual “be transmitted” label is defensible for 響く’s vibration-propagation sense. Applicable frozen **ひびく4** defines transmitted vibration; fresh [Seisenban ひびく②](https://kotobank.jp/word/響く-585232) likewise expressly includes vibration being transmitted. Complete **1441900:5** includes sound propagation/transmission, and the full older body demonstrates sound travelling through a wall. This establishes a specific secondary-sense overlap, not merely a shared sound topic.

The titles differ, so identical-title deduplication does not protect this pair. Other exclusions provide no transitive protection. **Minimal remedy:** add `伝わる` to 響く’s `quiz_exclusions`; one declaration suffices under symmetric guards. No mapping or N2 selection change is needed. **Confidence: medium-high.** This corrects a gap in my initial review; it was not introduced by the correction.

No correction-introduced content regression was established.

## Optional

**Optional footer and 広々 changes: adopted correctly.** `words\響き.md:53` and `words\標準.md:51` now explicitly distinguish selected/additional senses without changing mappings. `words\広々.md:17–22` clearly supplies both と variants and preserves the examples; frozen ひろびろ supports optional と.

No further nonblocking expansion is proposed. The broader 平仮名/字/文字 re-audit and older 片仮名/日の入り link polish remain deferred; this confirmation establishes no new consequential defect there.

## Limits

The supplied twenty frozen public responses represent **Digital Daijisen via Weblio, one authority**, not twenty independent dictionaries. Their applicable headings do not verify every article claim. The correction public-inspection file contains author summaries, not raw captures; the failed Cambridge request supplies no lexical evidence.

Fresh Seisenban lexical returns were inspected independently. The fresh 夜明け material was encyclopedic context only; the 明け方 retrieval supplied no lexical verification. Neither failed/irrelevant retrieval was used as proof.

Git state, manifest hashes, rendering equivalence, runtime quiz behavior, usage frequency, exhaustive correctness, and native-speaker certification were not independently established.
