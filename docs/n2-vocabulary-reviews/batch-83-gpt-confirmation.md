## Snapshot: fefa0999ef3171b8fd54f5609376ddd4f714e227

**The revised snapshot is not fully clear: two direct quiz-exclusion gaps remain on 巡る.** The five revised cards otherwise preserve correct teaching and show no established regression.

Parent: `f6a02bca0885a78dac2568e8da448be0954756df`. This is a **committed-content review**, using the correction manifest’s commit association. File tools cannot execute Git; I could not independently verify HEAD, worktree cleanliness, commit contents, or supplied hashes. No files were changed.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

In this original reviewer session, I reread all twenty current articles, all four current related kanji bodies, all twenty mappings and complete principal families, all 28 component records, all 268 comparison labels, the TSV header and exactly physical lines 1642–1661, both repository snapshots, the required instructions, and `docs\content-format.md:18–103`.

Confirmation-specific inspection included the complete reconciliation, both complete patches, all thirty correction-family records in three ranges, complete benefit comparisons, all four complete correction older-body files, actual complete 利益・見物・サークル articles, complete runtime evidence, supplied baseline 群れ and four baseline kanji bodies, and relevant corrected blind-derivative sections. The enumerated confirmation reads cover **44 distinct complete dictionary families and eighteen unassigned comparison bodies**, beyond the twenty assigned articles. I did not read the entire large derivative or all 415 prepared families.

I completely reread the 302-line original public text and 13-line canonical text. These contain nineteen original positive Daijisen bodies, the failed 目覚し extraction, and one successful canonical 目覚まし capture—**twenty positive captures from one Japanese dictionary authority**. I additionally fetched the applicable American Heritage entries for *benefit*, *circle*, and *command*, and the 精選版日本国語大辞典 **けんぶつ** entry through Kotobank.

No agents, delegation, edits, or concurrent calls were used. Each call was awaited before the next. The supplied native-event record establishes initial GPT maximum outstanding calls **1**, Claude **4**, although the reviewer processes themselves ran sequentially; Claude’s claimed internally serial execution must not be repeated as fact. The supplied audit also counts the initial GPT inspection as 105 families/232 senses rather than my reported 104 families; that correction is audit-attributed, not independently recomputed here.

## Verdicts:

Correctness includes quiz-answer validity. Scoped coverage below assesses the selected teaching and necessary recognition, not exhaustive dictionary expansion.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1642 | 紫 | CLEAN | CLEAN | CLEAN | Color primary; plant and culinary recognition appropriately qualified. |
| N2:1643 | 群れ | CLEAN | CLEAN | CLEAN | Bounded reuse; original body, stable metadata and twelve guards preserved. |
| N2:1644 | 姪 | CLEAN | CLEAN | CLEAN | Correct niece relationship; relocated caution is clearer. |
| N2:1645 | 名作 | CLEAN | CLEAN | CLEAN | Evaluative masterpiece meaning retained; no required 創作 edge established. |
| N2:1646 | 名刺 | CLEAN | CLEAN | CLEAN | Correct business-card identity, readings and reciprocal 刺 link. |
| N2:1647 | 名詞 | CLEAN | CLEAN | CLEAN | Modern reading and grammar-framework qualification correct. |
| N2:1648 | 名所 | CLEAN | CLEAN | CLEAN | Noted-place teaching distinguished from scenery and ordinary landmarks. |
| N2:1649 | 命ずる | CLEAN | CLEAN | CLEAN | Command/appointment, particles and shared conjugated forms correct. |
| N2:1650 | 迷信 | CLEAN | CLEAN | CLEAN | Evaluative register explained without equating religion with superstition. |
| N2:1651 | 名物 | CLEAN | CLEAN | CLEAN | Product primary; sourced local-character recognition supports 特徴 guard. |
| N2:1652 | めいめい ← 銘々 | CLEAN | CLEAN | CLEAN | Source spelling explicit; revised luggage explanation matches the example. |
| N2:1653 | 目上 | CLEAN | CLEAN | CLEAN | Whole social-superiority label distinguishes excellence-related 優れる. |
| N2:1654 | メーター | CLEAN | CLEAN | CLEAN | Instrument primary; unit recognition and メータ variant qualified. |
| N2:1655 | 恵まれる | CLEAN | CLEAN | CLEAN | Favorable Nに construction preserved; benefit-label safeguards supported. |
| N2:1656 | 巡る | NEEDS FIX | CLEAN | CLEAN | All five senses taught correctly; missing 見物 and サークル direct guards. |
| N2:1657 | 目指す | CLEAN | CLEAN | CLEAN | Achievement and destination uses, target を and conjugation correct. |
| N2:1658 | 目覚まし ← 目覚し | CLEAN | CLEAN | CLEAN | Exact source spelling recognized; pronunciation and additional uses distinguished. |
| N2:1659 | 目下 | CLEAN | CLEAN | CLEAN | Correct めした identity; separate もっか contrast and new prompt-layer guards. |
| N2:1660 | 目印 | CLEAN | CLEAN | CLEAN | めじるし identity preserved; ordinary もくひょう navigation not denied. |
| N2:1661 | 目立つ | CLEAN | CLEAN | CLEAN | Intransitive subject, forms and neutral conspicuousness explained correctly. |

**Mappings — CLEAN.** All twenty raw source associations and selected one-based senses remain supported. 銘々→めいめい/1532810 and 目覚し→目覚まし/1535340 explicitly preserve source recognition. The contradictory raw 目下 gloss remains intact while the card correctly follows めした/1535320 and distinguishes もっか/1535330. Additional recognition is not treated as independent N2 assignment.

**Components and reciprocal links — CLEAN.** Every distinct primary written Han is in metadata. All seventeen existing relevant character cards have substantive links; absent 紫・姪・銘・恵・巡 cards are not invented. Kana-primary めいめい appropriately has `kanji: []`. 名刺↔刺, 名詞↔詞, 目印↔印 and existing 群れ↔群 are present, with whole-word readings explained rather than mechanically inferred.

**Kanji and baseline preservation — CLEAN within supplied baseline evidence.** The three kanji edits add only the intended links and necessary entry citations; metadata and unrelated teaching remain unchanged. 群 is unchanged. 群れ differs from its supplied original only by sourced `jlpt: 2`; its complete body, identity, title, tags and twelve exclusions are preserved. This comparison was textual, not an independently executed Git/hash check.

## Findings:

**B83-R1 — OPEN; Moderate; Correctness: quiz ambiguity.**

**Location:** `words\巡る.md:9,18–21`; comparison `words\見物.md:4,15,29`.

巡る explicitly teaches touring places and “I toured old temples.” The actual 見物 title is **“sightseeing,”** and its complete body teaches 京都を見物する. Complete entry **1342050:4** supplies travelling around/making a tour; complete **1260000:1** supplies sightseeing/watching/viewing. The applicable Kotobank 精選版 **けんぶつ** entry independently includes enjoying sights and noted places.

Consequently, “sightseeing” is a defensible alternative for an ordinary taught use of 巡る. Neither article declares their direct pair. Adding 観光 does not protect 見物 through 観光’s exclusion: guards are nontransitive.

**Minimal remedy:** add `見物` to 巡る’s exclusions. This protects both directions and among-choice combinations without changing either word’s meaning. **Confidence: high.**

**B83-R2 — OPEN; Minor; Correctness: ambiguous English label.**

**Location:** `words\巡る.md:9`; comparison `words\サークル.md:4,9,21`.

サークル’s actual title contains bare **“circle,”** and its complete body explicitly teaches the circular-shape sense. Complete entry **1054850:1–2** confirms both club and shape meanings. American Heritage’s applicable *circle* verb senses describe forming or moving around something, matching complete **1342050:1–2** and the taught 巡る constructions.

This is the same direct English-label ambiguity that justifies retaining 丸・円・輪. Neither side declares 巡る/サークル. サークル’s guards against the shape nouns do not transitively protect this pair.

**Minimal remedy:** add `サークル` to 巡る’s exclusions. Do not merge the Japanese identities or inherit a broader clique. **Confidence: high.**

**Correction dispositions:**

- **B83-C1 — RESOLVED; Moderate; Correctness.** `words\目下.md:9,39–43` now guards 現在 and 今 while preserving the correct めした identity. Supplied pinned `WordQuizScreen.kt:131–145` displays `word.word` initially; `WordKanjiHelpView.kt:65–88` reveals the reading through interaction. The optional tip is not an always-visible disambiguator. Complete 1535320/1535330/1263650/1288850 families and complete 現在・今 bodies support the correction. **My initial blanket CLEAN missed this quiz-layer issue. Confidence: high.**
- **B83-C2 — RESOLVED; Minor; Correctness.** `words\恵まれる.md:9` adds 恩恵 and independently 利益. Their actual titles contain bare *benefit*; their complete bodies and families support favorable benefit/advantage. American Heritage confirms the intransitive “derive benefit” interpretation. The 利益 edge uses **1549470:1–2**, not the **りやく-only sense 3** religious blessing. This is a limited label safeguard, not noun/verb interchangeability. **Confidence: moderate-high.**
- **B83-C3 — removal recommendation correctly withdrawn.** Retain 丸・円・輪 on `words\巡る.md:9`: actual labels, complete noun families and the fetched English verb entry establish direct ambiguity. Retain 行く independently on its actual “to go” title, complete 1578850 movement/traversal senses and complete body. Neither POS differences nor topic proximity decide these pairs. **Confidence: high.**
- **B83-C4 — removal recommendation correctly withdrawn.** Retain 望む on `words\命ずる.md:9`. Complete **1519630:3**, the actual 海を望む部屋 example, and American Heritage *command* transitive **5b** support the outlook interpretation of bare “command.” The authoritative and outlook meanings remain distinct. **Confidence: high.**
- **観光 addition — supported but incomplete follow-through.** Complete 1214840 and its actual sightseeing/tourism body support the new edge. B83-R1 identifies the separately evidenced remaining 見物 edge; it is not inherited from 観光.
- **Other rejected hypotheses — supported.** No required 目上/優れる edge follows from the socially qualified whole title. No required 名作/創作 edge follows merely because some original works are masterpieces. Retaining 名物/特徴 is supported by the explicitly taught, Daijisen-sourced local distinguishing-character use.

The prior all-CLEAN conclusion is therefore superseded for quiz safeguards. No additional actionable lexical, mapping, component, preservation or prose defect was established.

## Optional:

The 姪 caution relocation and めいめい luggage clarification are sound nonblocking improvements, with no established regression.

`人にVように命ずる` and an example retaining literal 命ずる remain optional production expansion; the existing payment, appointment and shared-form explanations are correct. The explicit めいめい/各々 guard remains harmless redundancy because their exact titles already deduplicate.

No くるり guard is established: its whole title specifies **one quick compact turn**, unlike unrestricted circuit movement. Its complete family was kept separate from the unrelated hinge identity. No further expansion is assigned.

## Limits:

**Two actionable defects remain: B83-R1 and B83-R2.** No other consequential unresolved content claim was identified within the inspected scope.

Commit association, hashes, equivalence receipts and historical read-count audits were not independently executed. Runtime conclusions concern the supplied pinned Android source excerpts at `5044d589b64eb857ccf73b31207d1d48757543b0`, not an emulator run, observed quiz draw, every app version, or every candidate combination.

The live Weblio 見物 retrieval did not expose the applicable Daijisen body and was not counted as that verification; the applicable Kotobank **けんぶつ** body was used instead. Failed 目覚し and reported failed 命ずる extractions remain failures, not corroboration. CLEAN is bounded to actual inspection—not exhaustive corpus coverage, frequency measurement, native-speaker certification, or measured model-bias reduction.
