## Snapshot: a14eb7276298c2231ac00aa70cea55948bb3e7fc — committed content only

The frozen receipt identifies parent `760cf55d180e2ce3105ea569f9443632c653408c` and attests clean committed content. **I had file tools, not Git execution**, so commit identity, cleanliness, parentage and file-to-commit correspondence are receipt-attested, not independently Git-verified.

## Scope

Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`, family `gpt`. Independent, read-only review; no delegation or repository edits.

Read all 18 new articles completely, as listed below. Reviewed the actual related patch and changed passages in context: `kanji\児.md:20,42`, `kanji\勇.md:38,45`, and `kanji\衣.md:38,46`. Checked only the specified reuse claims in `words\一昨日.md` and `words\一昨年.md`.

Used the required instructions, format reference, assigned mappings **N2:62–N2:81**, complete relevant headword families, component evidence, actual comparison-card passages, and public dictionary entries. N2 here denotes the pinned **community list**, not an official modern JLPT syllabus.

Excluded prohibited authoring/review materials, other reviewers’ output, unassigned source rows, and comprehensive review of unchanged existing-card teaching.

## Verdicts

Each row names `words\<word>.md`. Quiz-answer defects are classified under **correctness**; coverage separately assesses the article’s practical teaching scope.

| New article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 育児 | CLEAN | CLEAN | CLEAN |
| 幾分 | NEEDS FIX | NEEDS FIX | CLEAN |
| 生け花 | CLEAN | CLEAN | CLEAN |
| 以後 | NEEDS FIX | CLEAN | CLEAN |
| 以降 | NEEDS FIX | CLEAN | CLEAN |
| イコール | NEEDS FIX | CLEAN | CLEAN |
| 勇ましい | CLEAN | CLEAN | CLEAN |
| 衣食住 | CLEAN | CLEAN | CLEAN |
| 意地悪 | CLEAN | CLEAN | CLEAN |
| いちいち | NEEDS FIX | CLEAN | CLEAN |
| 一応 | NEEDS FIX | CLEAN | CLEAN |
| 一段 | CLEAN | CLEAN | CLEAN |
| 一流 | NEEDS FIX | CLEAN | CLEAN |
| 佚 | NEEDS FIX | CLEAN | CLEAN |
| 一斉 | CLEAN | CLEAN | CLEAN |
| 一旦 | CLEAN | CLEAN | CLEAN |
| 一定 | CLEAN | CLEAN | CLEAN |
| いってらっしゃい | CLEAN | CLEAN | CLEAN |

**Related passages:** 児, 勇 and 衣 are each **CLEAN / CLEAN / CLEAN** within the changed scope. Their reciprocal word links supply the correct readings and useful meanings; no invented constituent reading is introduced.

**Reuse claims:** both are **CLEAN / CLEAN / CLEAN** within the specified scope. `一昨日.md:2-7,15,25` explicitly covers 一昨日／いっさくじつ with the intended meaning while retaining primary おととい and N5. `一昨年.md:2-7,14-16,22-25` likewise covers 一昨年／いっさくねん while retaining おととし and N5. The complete dictionary families support these combinations, including the 一昨年 restriction on いっさくねん.

All 20 source rows have lexical teaching anchors. In particular, **佚’s inconsistent source gloss is appropriately preserved as provenance rather than promoted wholesale into noun meanings**. CLEAN means no actionable defect established in scope—not exhaustive correctness or native-speaker certification.

## Findings

The quiz findings below concern **context-free English-answer ambiguity**, not unrestricted Japanese interchangeability. Different title strings do not resolve them. Each listed pair needs a **direct** exclusion; protection through an intermediate card is insufficient.

**GPT04-01 — Minor · Correctness / scoped coverage — Native-first 幾分 is classified as kango without explaining its mixed reading.**  
`words\幾分.md:6-8,26-30` declares `type: kango` and a kango tag, but merely says to learn いくぶん as a whole. **いく is kun; ブン is on**. This obscures the reading distinction and conflicts with the repository’s native-first grouping. Minimal remedy: use the existing `wago` grouping and explicitly explain the mixed kun+on reading, without implying both components are native. Evidence: `docs\n2-vocabulary-batch-sources\batch-04.json:2164-2182,2729-2742`; the established treatment in `words\場所.md:6,24`; compare the on-first convention in `docs\content-format.md:63`. **Confidence: high.**

**GPT04-02 — Minor · Correctness (quiz) — 幾分 lacks a direct guard against 気持ち’s ordinary degree sense.**  
`words\幾分.md:4,9` offers “somewhat; to a degree” but does not exclude 気持ち; `words\気持ち.md:1-9` supplies no reverse exclusion. Although that card’s title is “feeling; state of mind,” 気持ち also ordinarily means **slightly/a bit/a little**, making the new title defensible on a 気持ち question. Minimal remedy: add `気持ち` to 幾分’s exclusions. Evidence: pinned 幾分 entry 1220060, sense 1; independently retrieved [Jisho/JMdict 気持ち](https://jisho.org/api/v1/search/words?keyword=気持ち), exact きもち entry, sense 4, with no spelling/reading restriction. **Confidence: high.**

**GPT04-03 — Minor · Correctness (quiz) — Both temporal cards remain exposed to 来’s “since” answer label.**  
`words\以後.md:4,9` and `words\以降.md:4,9` exclude 以来 but not 来. `words\来.md:4,15` displays and explicitly teaches **“since”**; it has no reverse guards. Thus “since” is a valid competing answer for these temporal uses. The existing 以来／来 exclusion does not extend transitively. Minimal remedy: add `来` directly to **both** new cards. Evidence: pinned 以後 1155100, sense 2, and 以降 1155110, sense 1; independently retrieved [来／らい](https://jisho.org/api/v1/search/words?keyword=来%20らい), suffix sense 2, “since …; for ….” **Confidence: high.**

**GPT04-04 — Minor · Correctness (quiz) — イコール omits overlapping 同一 and 同様.**  
`words\イコール.md:4,9` displays “equal; equals sign” and excludes 同じ, but not 同一 or 同様. Their actual titles are “identical; one and the same” and “same; similar” (`words\同一.md:4,9`; `words\同様.md:4,9`); both also have an **equal** sense. “Equal” can therefore be a valid answer on their questions. Minimal remedy: add `同一` and `同様` directly to イコール’s exclusions. Evidence: pinned イコール 1021220, sense 1; independently retrieved [同一／どういつ, sense 1](https://jisho.org/api/v1/search/words?keyword=同一) and [同様／どうよう, sense 1](https://jisho.org/api/v1/search/words?keyword=同様). **Confidence: high.**

**GPT04-05 — Minor · Correctness (quiz) — いちいち’s “every single” conflicts with あらゆる’s “every.”**  
`words\いちいち.md:4,9` lacks あらゆる, while `words\あらゆる.md:4,9,16` displays “every; all kinds of” without a reverse guard. The comprehensive **each-and-every** meaning—not merely a shared quantity topic—makes these context-free labels overlap. Their different attachment patterns are not visible in the quiz. Minimal remedy: add `あらゆる` directly to いちいち’s exclusions. Evidence: pinned いちいち 1587320, sense 2, “every single; each and every”; independently retrieved [あらゆる](https://jisho.org/api/v1/search/words?keyword=あらゆる), sense 1, “all; every,” usually kana. **Confidence: high.**

**GPT04-06 — Minor · Correctness (quiz) — 一応’s “roughly” remains a valid competing label for およそ.**  
`words\一応.md:4,9` excludes ざっと and 大体 but not およそ. `words\およそ.md:4,9,16` displays “approximately; generally” and explicitly teaches **roughly**, with no reverse exclusion. Minimal remedy: add `およそ` directly to 一応’s exclusions; retain the distinctions between their constructions. Evidence: pinned 一応 1161170, sense 1; independently retrieved [およそ](https://jisho.org/api/v1/search/words?keyword=およそ), senses 1–2; actual [Digital Daijisen 一応](https://kotobank.jp/word/一応-433210) entry inspected in raw HTML, adverb sense 1, 大略, with およそ among that sense’s comparisons. This finding does **not** generalize 一応’s separate “once” gloss into numerical counting. **Confidence: high.**

**GPT04-07 — Minor · Correctness (quiz) — 一流’s quality label overlaps 上等 and 優秀 without direct guards.**  
`words\一流.md:4,9` displays “first-rate; leading” but excludes neither `words\上等.md:4,9` (“superior quality; excellent”) nor `words\優秀.md:4` (“excellent; outstanding”). These are overlapping quality evaluations, not merely unrelated positive attributes: **上等 explicitly includes first-class**, and 優秀 evaluates outstanding ability or quality. Minimal remedy: add `上等` and `優秀` directly to 一流’s exclusions. Evidence: pinned 一流 1167270, sense 1; actual comparison-card definitions at 上等:16 and 優秀:15; independently retrieved [上等, sense 1](https://jisho.org/api/v1/search/words?keyword=上等) and [優秀, sense 1](https://jisho.org/api/v1/search/words?keyword=優秀). **Confidence: high.**

**GPT04-08 — Minor · Correctness (quiz) — 佚 lacks protection against ゆっくり’s leisure/relaxation use.**  
`words\佚.md:4,9` displays “ease; relaxation” and excludes のんびり, but not ゆっくり. `words\ゆっくり.md:4,15-19` displays “slowly, at leisure” and explicitly teaches relaxing at home. That ordinary use makes “ease; relaxation” defensible on a ゆっくり question. The のんびり bridge does not protect this pair. Minimal remedy: add `ゆっくり` directly to 佚’s exclusions. Evidence: pinned 佚 1585390, sense 1; independently inspected [Seisenban 佚](https://kotobank.jp/word/佚-433903), defining the noun through のんびりすること; [Jisho/JMdict ゆっくり](https://jisho.org/api/v1/search/words?keyword=ゆっくり), leisure sense 1 and comfortable-rest sense 3. **Confidence: high.**

## Optional

None.

## Limits

The frozen receipt’s hashes and the supplied JMdict/KANJIDIC2 extracts were **not independently recomputed**. Author inspection receipts were not treated as independent reviewer retrieval; public entries cited above were retrieved directly. Jisho is JMdict-derived, so independent retrieval does not make it an independent lexicographic source.

This was a content and metadata review, not runtime quiz execution, exhaustive corpus verification, or comprehensive review of unchanged cards. No finding assumes that dictionary inclusion alone establishes frequency, every possible collocation, or official JLPT membership.
