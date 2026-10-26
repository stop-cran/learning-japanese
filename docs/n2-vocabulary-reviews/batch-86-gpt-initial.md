## Snapshot: 2c2ed2623f04773c93bc97c6820e3ef7131b8fea; committed content only

Parent: `4d7fea34f7e810000118e1438179acb86c3be9ee`. This is the frozen snapshot’s declared commit; its Git/hash assertions were not independently executed.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Independent, read-only review using **60 sequential tool calls**, without agents, delegation or edits.

Completed reads:
- All twenty assigned articles; both repository instruction files; `docs\content-format.md:18–105`; TSV header and exactly physical rows `1702–1721`.
- All twenty mappings, twenty complete primary families, thirty-five component records and 233 comparison labels, using every prescribed bounded JSONL range.
- Complete `kanji\印.md`, `刊.md`, `郵.md`, `軟.md`, and `batch-86-related.patch`.
- All 351 lines of `batch-86-public-bodies.txt`, distinguishing applicable lexical headings/readings from neighboring material.
- Complete family-inspection files **01, 04, 05, 08, 10, 13 and 14**, plus the complete 汽車 family in the final-comparisons JSON: **177 distinct complete dictionary families overall**, including the twenty primary families.
- Complete older comparison bodies: 公務, 主役, 行事, 直す, 片付ける, 破る, 主人, 大家, 非常, 失敗, 別れる, くたくた, 郵便, 便, 配達, 出す and 届ける; additionally, complete 夕飯 classification prior art and 柔らかい preservation comparison.

The 233 labels were inspected as metadata, not counted as 233 full-body reads. Remaining comparison families/bodies were not mechanically inspected.

## Verdicts:

**Two actionable quiz-exclusion omissions were established. No actionable defect was established in the twenty articles’ explanatory prose.**

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1702 | 役所 | CLEAN | CLEAN | CLEAN | Public-administration meaning and やくしょ identity maintained; separate やくどころ not imported. |
| N2:1703 | 訳す | CLEAN | CLEAN | CLEAN | Transitive godan forms and target-language に are correct; language interpretation is appropriately bounded. |
| N2:1704 | 役人 | CLEAN | CLEAN | CLEAN | Government-official meaning, capacity として and register qualifications are sound. |
| N2:1705 | 薬品 | CLEAN | CLEAN | CLEAN | Both medicinal and nonmedicinal chemical meanings are explicitly distinguished. |
| N2:1706 | 役目 | CLEAN | NEEDS FIX | CLEAN | Duty/function teaching is sound; direct 公務 guard is missing—F01. |
| N2:1707 | 火傷 | CLEAN | NEEDS FIX | CLEAN | Whole-word やけど and figurative recognition are correct; figurative overlap with 失敗 is unguarded—F02. |
| N2:1708 | 夜行 | CLEAN | CLEAN | CLEAN | Night-train sense remains やこう; やぎょう monster-procession recognition is separated. |
| N2:1709 | 矢印 | CLEAN | CLEAN | CLEAN | Symbol meaning, native reading and colloquial interest extension are distinguished. |
| N2:1710 | やたら | CLEAN | CLEAN | CLEAN | Indiscriminate manner versus excessive degree, に／と and attributive な are explained. |
| N2:1711 | 薬局 | CLEAN | CLEAN | CLEAN | Selected shop/pharmacy sense is taught; level-only baseline reuse is preserved. |
| N2:1712 | やっつける | CLEAN | CLEAN | CLEAN | Transitive ichidan behavior, defeat and task completion are sound; carelessness is qualified. |
| N2:1713 | 家主 | CLEAN | CLEAN | CLEAN | やぬし meanings and 大家 identities are separated; 主人’s broader meanings support comparison. |
| N2:1714 | 破く | CLEAN | CLEAN | CLEAN | Tear/rip meaning is dictionary-supported despite the empty raw source gloss; godan forms are correct. |
| N2:1715 | 破れる | CLEAN | CLEAN | CLEAN | Lexical intransitive, negotiation breakdown, potential-form homography and 敗れる distinction are handled. |
| N2:1716 | やむをえない | CLEAN | CLEAN | CLEAN | Complete expression and direct noun attachment are correct; しょうがない intensity construction is not transferred. |
| N2:1717 | 軟らかい | CLEAN | CLEAN | CLEAN | Unrestricted family senses are represented; baseline body/exclusions and N4 柔らかい are preserved. |
| N2:1718 | 遊園地 | CLEAN | CLEAN | CLEAN | Practical amusement-park meaning and destination/activity particles are clear. |
| N2:1719 | 夕刊 | CLEAN | CLEAN | CLEAN | Edition, rather than reading time, is correctly taught; mixed-reading storage matches 夕飯 prior art. |
| N2:1720 | 友好 | CLEAN | CLEAN | CLEAN | Friendly relations are not restricted exclusively to countries; relationship/person distinction is clear. |
| N2:1721 | 郵送 | CLEAN | CLEAN | CLEAN | Postal sending, transitive する construction and dispatch-versus-arrival distinction are sound. |

**Kanji/baseline preservation — CLEAN within the supplied patch.** 印, 刊 and 郵 retain their metadata and unrelated teaching; changes add links, the 夕刊 example and its citation. 薬局 and 軟らかい receive only `jlpt: 2`, preserving identities, readings, titles, bodies and exclusions. 柔らかい remains explicitly N4. This is a patch-based judgment, not an independently executed Git comparison.

**Components — CLEAN.** All 27 distinct primary written Han characters appear in their articles’ metadata. The scoped file lookup found cards for 25; substantive introductions link those existing components. 傷 and 矢 remain correctly included in metadata without invented kanji links. Kana-only primary spellings correctly retain empty kanji arrays despite recognized dictionary spellings.

**Reciprocity — CLEAN.** Both directions exist for 印／矢印, 刊／夕刊 and 郵／郵送. Existing 軟／軟らかい reciprocity remains present.

**Mappings — CLEAN.** All twenty associations agree with the requested source rows, TSV and complete primary families, including one-based senses and reading restrictions. 破く’s raw gloss remains empty. Additional recognition was not treated as an independent N2 assignment to every recognized meaning.

## Findings:

1. **F01 — Medium; scoped coverage — missing direct 役目／公務 exclusion.**  
   **Location:** `words\役目.md:9`; comparison `words\公務.md:4–9,16–24,37–43`.  
   **Claim/impact:** Neither article excludes the other. 公務’s displayed title is “official public duties”; its actual meaning is duties performed in a public-service role. 役目 explicitly means a duty or assigned role. Consequently, “duty; role; function” is a defensible broad answer for 公務, leaving an ambiguous quiz pairing available. Shared exclusions through 役, 役割 or 務め do not protect this pair because guards are nontransitive.  
   **Minimal remedy:** Add `公務` to 役目’s `quiz_exclusions`, or declare the reciprocal pair on 公務—one declaration suffices.  
   **Exact evidence:** Primary JMdict **1538080:1** gives “duty; role; function”; complete comparison family **1274810:1**, read in family-inspection **04:101–105**, gives “official business; public business.” The complete 公務 body explicitly teaches public duties and assigned-role comparisons. Both complete headers confirm the absent direct guard.  
   **Confidence:** High.

2. **F02 — Medium; scoped coverage — figurative 火傷／失敗 overlap is unguarded.**  
   **Location:** `words\火傷.md:9,41–43`; comparison `words\失敗.md:4–9,15–19`.  
   **Claim/impact:** 火傷 explicitly teaches figurative “getting one’s fingers burned,” but its exclusions cover only injury and burning comparisons. Neither header excludes 失敗. The ordinary figurative use can describe an unsuccessful, costly undertaking, making 失敗’s “failure; mistake” title defensible for 火傷 in that sense. Restricting the guard audit to literal skin injury misses teaching already present on the card.  
   **Minimal remedy:** Add `失敗` to 火傷’s `quiz_exclusions`, or declare the pair on 失敗. Do not generalize this into exclusions against every adverse event.  
   **Exact evidence:** Complete primary family **1577310:2** records figurative getting one’s fingers burned, including poor investment. The applicable **やけど** public capture, `batch-86-public-bodies.txt:89–98`, explicitly defines the figurative use as **「失敗したり、手痛い経験をしたりすること」**, with the futures-trading example. Complete comparison family **1320140:1**, read in inspection **05**, gives “failure; mistake; blunder”; the complete older 失敗 body teaches an undertaking going wrong. Both complete headers confirm the absent guard.  
   **Confidence:** High.

These findings concern direct pairs, not inherited exclusion cliques. No excessive guard was established in the inspected comparisons. Unchanged 軟らかい exclusions were assessed for preservation, not represented as entirely newly researched.

## Optional: None

## Limits:

File tools **cannot execute Git**. I could not independently verify HEAD, cleanliness, parentage, hashes, compact-rendering equivalence or that every current repository file matches the declared commit. The review targets the frozen committed snapshot and relies on its supplied assertions for that binding.

The public captures provide **one dictionary authority**, Digital Daijisen; they were read completely but not independently fetched live. No exhaustive corpus, frequency or native-speaker certification is claimed. Unread comparison families/bodies limit exhaustive quiz-pool assurance, not the two evidenced findings above.

The mandated TSV rows themselves exposed their `source_note` column. No prohibited author/review ledger, unblinded batch JSON or reviewer report was read, but complete blindness to author commentary cannot therefore be claimed.
