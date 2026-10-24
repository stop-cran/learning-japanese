# Batch 35 review: N2:682–N2:701

**Snapshot:** Commit `978aed9979689800a07e505bf370846e4c3cc12c` (parent `3c899fabf15e967b5f8d815dd0ad6247ad110f04`); committed content only. I had file tools only and could not run Git, so the commit, file hashes and the evidence packet's claimed equivalence are unverified.

**Scope:**
- **Model:** claude-opus-5.5.
- **Read in full:** all 18 new articles; the 5-file related patch; the current `kanji\筆.md`, `恋.md` and `鉄.md`; the `湿度.md`/`児童.md` front matter; TSV rows 682–701.
- **Evidence packet:** all 20 principal families, all 150 comparison labels and exclusions, the 20 receipts, `quizDeclarations` and `sourceAccessLimits`.
- **Quiz checks:** front matter of selected existing words, plus a keyword search of `words\` titles (not exhaustive).
- **Public pages:** Kotobank (Daijisen and Nihon Kokugo Daijiten) for 絞る, 尻尾 and しみじみ; Japanese Wiktionary for しみじみ; a Weblio example-sentence count for しみじみとした.
- **Omissions:** the compact comparison file and most of the 302 comparison families were not read, and none of the captured comparison bodies. `docs\confusable-words.md` and `docs\jlpt-levels.md` were not consulted.

**Verdicts:** Missing quiz exclusions are counted under correctness.

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 執筆 | CLEAN | CLEAN | CLEAN |
| 実物 | CLEAN | CLEAN | CLEAN |
| しっぽ | CLEAN | NEEDS FIX (C2) | CLEAN |
| 実用 | CLEAN | CLEAN | CLEAN |
| 実力 | CLEAN | CLEAN | CLEAN |
| 実例 | CLEAN | CLEAN | CLEAN |
| 失恋 | CLEAN | CLEAN | CLEAN |
| 指定 | CLEAN | CLEAN | CLEAN |
| 私鉄 | CLEAN | CLEAN | CLEAN |
| 縛る | CLEAN | CLEAN | CLEAN |
| 地盤 | NEEDS FIX (Q2) | CLEAN | CLEAN |
| しびれる | NEEDS FIX (Q4) | CLEAN | CLEAN |
| 紙幣 | NEEDS FIX (Q1) | CLEAN | CLEAN |
| しぼむ | CLEAN | CLEAN | CLEAN |
| 絞る | CLEAN | NEEDS FIX (C3) | CLEAN |
| 縞 | CLEAN | CLEAN | CLEAN |
| 地味 | NEEDS FIX (Q3) | CLEAN | CLEAN |
| しみじみ | NEEDS FIX (C1, Q5) | NEEDS FIX (C1) | CLEAN |

- **Kanji edits (筆, 恋, 鉄):** CLEAN on all three facets.
  - 筆: the しっぴつ explanation (シツ + ヒツ) is correct.
  - 恋 and 鉄: the new links resolve, and existing readings and qualifications are kept.
  - Only 筆, 恋 and 鉄 are N2 among the linked kanji, so no other reciprocal examples are owed.
- **Reused 湿度 and 児童:** CLEAN on all three facets. The patch adds only `jlpt: 2`, and the identities match exactly.
- **Mappings:** 17 of 20 are CLEAN on all three facets. The exceptions:
  - N2:685 (しっぽ) coverage: C2.
  - N2:698 (絞る) coverage: C3.
  - N2:701 (しみじみ) correctness: its "or suru verb" note repeats C1.

**Findings:**
- **C1 (Moderate; correctness and coverage; しみじみ.md:37, TSV:701).**
  - Problem: "Do not add する… not a general-purpose する verb" will steer learners away from the very common しみじみ(と)した + noun pattern.
  - Fix: Say that adnominal しみじみ(と)した (as in しみじみとした話) is common, and keep only a narrower caution if needed.
  - Evidence: Weblio returns 30 dictionary example sentences containing しみじみとした (the sentences themselves did not render). JMdict and Nihon Kokugo Daijiten classify it as an adverb only, which does not show that する is ungrammatical.
  - Confidence: moderate-high.
- **C2 (Minor; coverage; しっぽ.md:23).**
  - Problem: the title promises "tail end", but the only illustration is しっぽの部分, with no non-animal object.
  - Fix: add 列のしっぽ or 大根のしっぽ.
  - Evidence: Nihon Kokugo Daijiten senses ③ and ④ (列の尻っぽ).
  - Confidence: high.
- **C3 (Minor; coverage and transparency; 絞る.md:52, TSV:698).**
  - Problem: only bow, sumo and go are declared out of scope, but JMdict sense 4 (extort/exploit) is neither taught nor excluded.
  - Fix: mention it in one line, or exclude it explicitly.
  - Evidence: Daijisen sense 2イ, 膏血を絞る.
  - Confidence: high.
- **Q1 (Minor; 紙幣.md:9).**
  - Problem: no exclusion against 金銭 "money; monetary matters". It has exactly the same tags (`[kango, noun, money]`), and お金 and 金 are already excluded on the same grounds.
  - Fix: add 金銭.
  - Confidence: high.
- **Q2 (Minor; 地盤.md:9, 23).**
  - Problem: the article teaches "foundation or base" and excludes 基礎 "foundation; basis", but not 基 "basis; foundation" or 基本 "basics; foundation". 基盤 and 基礎 already exclude both.
  - Fix: add 基 and 基本.
  - Confidence: moderate-high.
- **Q3 (Minor; 地味.md:9, 23).**
  - Problem: the article teaches "modest" (地味に暮らす), but there is no exclusion against 謙虚 "modest; humble". They share three tags.
  - Fix: add 謙虚.
  - Confidence: moderate.
- **Q4 (Minor; しびれる.md:9).**
  - Problem: 凍える "be chilled; become numb with cold" contains the exact phrase "become numb", yet じんじん is excluded on a weaker overlap.
  - Fix: add 凍える.
  - Confidence: moderate.
- **Q5 (Minor; しみじみ.md:9).**
  - Problem: "deeply felt" collides with 感激 "deep emotion" (shared `feelings` tag) and 感動 "being deeply moved", yet 深い "deep" is excluded on a weaker overlap.
  - Fix: add 感激 and 感動.
  - Confidence: moderate.

**Optional:**
- Possible extra exclusions or retitles:
  - 執筆 vs 文字 (shared word "writing", three shared tags).
  - 実力 vs 勢い (bare "force"; "coercive force" would be clearer).
  - 実例's "real case" vs ケース, 事件 and 場合.
  - 地味 vs 原 and 野 (the "plain" homograph).
  - 縛る vs 不自由.
- 縞↔棒 is an exclusion no body passage supports, and the titles do not collide.
- Wording polish:
  - しぼむ.md:23: the warning about an ichidan ending is vacuous.
  - 紙幣.md:33: "not a synonym for having no money" is a non sequitur.
  - しびれる.md:33: じんじん is a sensation mimetic, not a sound.
  - しびれる.md:35: "Neither emotional word is a diagnosis" is unclear.
- Possible additions:
  - An example sentence for the electric-shock sense of しびれる.
  - The idioms しっぽを出す and しっぽをつかむ.

**Limits:**
- Git and hashes could not be executed.
- Most Daijisen receipts are the author's paraphrases. I independently retrieved only 絞る, 尻尾 and しみじみ; the Weblio, goo and jisho fetches failed or did not render.
- My search for colliding titles was not exhaustive, and no app quizzes were actually generated.
- This is not native-speaker certification.
