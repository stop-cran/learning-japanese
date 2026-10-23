## Snapshot
I reviewed frozen commit **b002896e6b26b58dd7bd5b73194d73ec834c8997** (parent f574c3a900041cbc460fdfa1306e54204ca24220), committed content only. The receipt reports cleanCommittedContent true.

I had file tools only and couldn't run Git. I read the files in the working tree and assumed, without verifying, that they match the commit. The 18-file related diff was read from the frozen patch.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), working sequentially with no delegation and no edits.
- **New articles:** all 19 read in full.
- **Reuse claim:** 乾燥. I checked the source spelling, the reading, both drying and dryness senses, and that only the level changed. This is not a recertification of its unchanged teaching.
- **Related changes:** all 18 read, with each changed passage checked in context.
- **Mappings:** all 20 rows, N2:342–N2:361, checked against the TSV, the batch rows and the principal families.
- **Quiz checks:** I checked titles across the whole `words\` folder for overlapping English labels, plus the quiz declarations and their rationale.
- **Forbidden files:** none read.
- **Partly read:**
  - The KANJIDIC2 component records (batch-18.json lines 1860–2688). I relied on the kanji card front matter instead.
  - The 109 comparison families (lines 2716–11388), which I only searched for specific forms.
  - The inspection receipts, which I treated as the author's assertions.

## Verdicts
Values are correctness / scoped coverage / comprehensibility.

| Article | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| 代わる | CLEAN | NEEDS FIX (F1) | CLEAN |
| 間隔 | CLEAN | CLEAN | CLEAN |
| 換気 | NEEDS FIX (F2) | CLEAN | NEEDS FIX (F4) |
| 感激 | CLEAN | CLEAN | CLEAN |
| 関西 | CLEAN | CLEAN | CLEAN |
| 鑑賞 | CLEAN | CLEAN | CLEAN |
| 感ずる | NEEDS FIX (F5) | CLEAN | CLEAN |
| 間接 | CLEAN | CLEAN | CLEAN |
| 感想 | NEEDS FIX (F5) | CLEAN | CLEAN |
| 観測 | NEEDS FIX (F3) | CLEAN | CLEAN |
| 寒帯 | CLEAN | CLEAN | CLEAN |
| 官庁 | CLEAN | CLEAN | CLEAN |
| 勘違い | CLEAN | CLEAN | CLEAN |
| 缶詰 | CLEAN | CLEAN | CLEAN |
| 乾電池 | CLEAN | CLEAN | CLEAN |
| 関東 | CLEAN | CLEAN | CLEAN |
| 観念 | CLEAN | CLEAN | CLEAN |
| 乾杯 | CLEAN | CLEAN | CLEAN |
| 看板 | NEEDS FIX (F6) | CLEAN | CLEAN |

**Related changes (18 files)**
- **kanji\替.md and kanji\換.md:** the links are valid, but these two need a fix. The 替わる/換わる spellings are named in the target article, and 1590820 is in both metadata lines. However, the meanings the links promise ("take over", "change places") aren't demonstrated there (F1).
- **kanji\賞.md, 接.md, 測.md, 帯.md, 庁.md, 缶.md, 詰.md, 乾.md, 池.md and 板.md:** CLEAN. Each has a reciprocal example at the actual reading and its source identity.
- **words\感覚.md, words\缶.md, words\意見.md and words\感じる.md:** CLEAN. The comparison and related-form links are narrow and accurate.
- **articles\kaeru-change-replace-and-return.md:** CLEAN. Both links (around lines 60 and 88) point to the correct article; the depth of the target's teaching falls under F1.
- **words\乾燥.md:** CLEAN. Only `jlpt: 2` was added.

**Reuse claim:** CLEAN. 乾燥 teaches both physical drying (sense 1) and figurative insipidity (sense 2), and its identity and exclusions are preserved.

**Mappings:**
- **N2:342 (代る):** spelling and reading CLEAN, because the 代る spelling is taught explicitly. Selected-sense coverage NEEDS FIX (F1).
- **The other 19 mappings:** CLEAN on all three facets.
  - Blank raw gloss (N2:346): handled correctly.
  - Additional dated sense 1609650:3 (N2:348): qualified as recognition-only.
  - Raw glosses with no JMdict counterpart (N2:361 "poster", N2:356 "tin can"): not promoted to taught meanings.
- **Article-level issues:** F2–F6 affect the articles, not the source identities.

## Findings
All findings are Minor except F1 (Moderate).

**F1 — 代わる: two of the three selected senses aren't demonstrated**
- **Severity / facet:** Moderate; coverage.
- **Location:** words\代わる.md:16–28 and 37–40. Linked from kanji\替.md:33,38 and kanji\換.md:33,40.
- **Claim:** The mapping selects senses 1–3, and the raw gloss includes "to relieve". Both examples show only sense 2 ("in someone's place" and handing over the phone).
  - Sense 1 (succeed, relieve, replace) gets only the title gloss and "being replaced" in the definition.
  - Sense 3 (be exchanged, change places, switch) appears only as a spelling tendency.
  - The alias links promise "be replaced; take over" and "be exchanged; change places", and a learner following them finds neither demonstrated.
  - The bare "intransitive" label also leaves the common を-marked uses unexplained (席を代わる "switch seats", 運転を代わる "take over the driving").
- **Remedy:** Add one relief or takeover example, such as 運転を代わる or 担当者が替わる. Add one seat-switch example, such as 席を代わる/替わる. Note that を there marks the role or position taken over.
- **Evidence:** batch-18.json rows (N2:342, selectedSenses [1,2,3]) and the 1590820 family senses 1 and 3.
- **Confidence:** high for the missing coverage; medium for the を-usage point, which relies on reviewer knowledge because my fetches failed.

**F2 — 換気 / 干す: missing quiz exclusion**
- **Severity / facet:** Minor; correctness (quiz).
- **Location:** words\換気.md:1–9, which has no quiz_exclusions.
- **Claim:** 干す's title is "hang out to dry; air out", and JMdict gives 干す sense 1 as "to air". "Air out the room" is an ordinary English gloss of 換気する, so 干す's label is a defensible answer for 換気.
- **Remedy:** Add `quiz_exclusions: [干す]`.
- **Evidence:** words\干す.md:4; batch-18.json:9717–9750.
- **Confidence:** medium.

**F3 — 観測: incomplete prediction guard**
- **Severity / facet:** Minor; correctness (quiz).
- **Location:** words\観測.md:9.
- **Claim:** The author excluded 予想 and 予測 ("prediction") but not 予報 ("forecast") or 占う ("tell fortunes; predict").
  - 占う shares the `prediction` tag with 観測.
  - 占う already excludes 予想, 予測 and 予報, so the repository treats "predict" and "forecast" as overlapping labels.
- **Remedy:** Add 予報 and 占う to 観測's exclusions.
- **Evidence:** words\予報.md:4; words\占う.md:4, 8 and 9.
- **Confidence:** medium.

**F4 — 換気: unexplained sentence about verb classification**
- **Severity / facet:** Minor; comprehensibility.
- **Location:** words\換気.md:45–46.
- **Claim:** "The dictionary's verb classification is not a rule forbidding…" refers to a classification (intransitive in JMdict) that the article never states. A learner can't tell whether 部屋を換気する is acceptable, although it is common.
- **Remedy:** Either state that JMdict labels it intransitive and that 部屋を換気する also occurs, or delete the sentence.
- **Evidence:** JMdict 1212780 lists vs and vi only; the N2:344 source note.
- **Confidence:** medium-high.

**F5 — 感ずる and 感想: missing 気味 exclusion**
- **Severity / facet:** Minor; correctness (quiz).
- **Location:** words\感ずる.md:9 and words\感想.md:9.
- **Claim:** 気味's title is "sensation; feeling", and it shares the kango type, the noun tag and the `feelings` tag with these words.
  - The author's own rationale excludes 感覚 ("sense; sensation"), 感じ, 気持ち and 気分 from 感ずる, and says noun/verb differences don't restrict a bare label.
  - 感想's JMdict glosses include "feelings".
- **Remedy:** Add 気味 to both exclusion lists.
- **Evidence:** words\気味.md:4 and 8; batch-18.json quizGuardRationale.
- **Confidence:** medium for 感ずる; medium-low for 感想.

**F6 — 看板 / 兆候: "sign" label overlap**
- **Severity / facet:** Minor; correctness (quiz).
- **Location:** words\看板.md:9.
- **Claim:** The author excluded 印 ("mark; sign") and サイン because of the English word "sign", but not 兆候 ("sign; indication"). 兆候 itself already excludes both 印 and サイン.
- **Remedy:** Add 兆候 to 看板's exclusions.
- **Evidence:** words\兆候.md:4 and 9.
- **Confidence:** medium-low. Impact is low because the two words share no tags.

## Optional
- **Unlinked mentions in non-N2 kanji cards:** these mention the new words as plain text. Backlinks aren't required, so linking them is optional.
  - kanji\代.md:21, 35, 46 (代わる). This is the primary kanji of that article.
  - 官.md (官庁).
  - 感.md and 想.md (感想).
  - 東.md (関東).
  - 西.md (関西).
  - 杯.md (乾杯).
- **感ずる:** a short register note (感じる is the everyday form) and the polite form 感じます.
- **関西:** the proper noun 関西学院 keeps the reading かんせい.
- **看板:** a note that the raw gloss "poster" normally corresponds to ポスター.

## Limits
- I couldn't run Git, so I didn't verify that the files I read match the commit hashes.
- My fetches of public dictionary pages for 代わる failed: kotobank returned 404, the goo hostname didn't resolve, and the weblio and Wiktionary pages returned no usable content. The を-usage point in F1 therefore rests on reviewer knowledge.
- I didn't fully read the KANJIDIC2 component records or the comparison families. I treated the receipts as author assertions and didn't independently re-fetch them.
- No quiz draw was executed in the app, and this is not a native-speaker certification.
- Comprehensive review of unchanged teaching (including 乾燥's body and the context around the related edits) is outside this scope.
