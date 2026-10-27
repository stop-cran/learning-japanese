## Snapshot: 2a1d30f2abe197b94ac8a92730fd8e69086ae30a; committed content only

Parent: `10eb0db442aca4eca75f52f4e15c81ebcd977b01`.

**Result: NEEDS FIX.** The twenty article associations and selected-sense mappings are supported. Findings concern missing reciprocal reading-row examples, one inaccurate spelling attribution, and omitted direct quiz exclusions.

The frozen snapshot was read first. Its committed-content and clean-worktree assertions are author-provided: the available file tools cannot execute Git, so I could not independently resolve the commit, verify the parent diff, or establish worktree cleanliness.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Independent, read-only review; no agents, delegation, or edits.

**Repository reads:** all seventeen new articles and all three reused articles completely; complete `kanji\低.md`, `kanji\券.md`, and `kanji\停.md`; both requested instruction files; `docs\content-format.md:18–126`; `docs\confusable-words.md`; `docs\jlpt-levels.md`; both permitted source snapshots; and only assigned rows 1122–1141 of `docs\n2-vocabulary-sources.tsv`.

**Private evidence reads:** the frozen snapshot, related patch, all four compact JSONL files, principal reading, all six complete family-inspection renderings, support-comparison rendering, and all three public-body TXT/JSON pairs. This included the twenty complete principal families/42 senses, component records, labels, restrictions, flags, inherited POS, and selected/additional sense associations. `review-evidence.json` itself was read only through line 140; the complete compact renderings supplied the corresponding records. No prohibited ledgers, rationale-bearing original batch JSON, authoring inputs/checks, or reviewer reports were read.

**Old-article inspection:** 82 additional complete word bodies—not the author’s reported 84. These comprise all 67 distinct pre-existing targets named in the assigned articles’ `quiz_exclusions`, plus 強力, 適当, 一致, 揃う, 回数券, 祝日, 落ちる, 釣る, 入口, 出口, 玄関, 裏口, 停留所, 発車, and 壊れる. Exclusions were considered directly in both directions and among choices, without assuming transitivity or treating every comparison cluster as a clique.

Fresh lexical sections were also retrieved from Kotobank for 揃う, 適当, 出入, 釣合う, 上がる, 落ちる, and 壊れる. Three fresh Weblio requests returned attribution/footer material without usable definitions and were not counted as verification.

## Verdicts: twenty source rows, related edits, and mappings

Every article below is `words\<article>.md`. For reused articles, verdicts cover the assigned source association, narrow edits, and preservation requirements—not a redesign of unchanged baseline teaching or exclusions. Scoped coverage includes the expressly required reciprocal kanji surfaces.

| Source | Article / association | JMdict selected senses | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1122 | 強気 — new | 1236230:1–2 | CLEAN | CLEAN | CLEAN |
| N2:1123 | 釣り合う — new | 1434050:1–2 | CLEAN | NEEDS FIX — F05 | CLEAN |
| N2:1124 | 吊る — new | 1434020:1 | CLEAN | CLEAN | CLEAN |
| N2:1125 | 吊るす — new; raw 吊す | 1433980:1 | CLEAN | CLEAN | CLEAN |
| N2:1126 | 出会い — reused; raw 出合い | 1338400:1–2 | CLEAN | CLEAN | CLEAN |
| N2:1127 | 手洗い — new | 1328020:1–3 | CLEAN | CLEAN | CLEAN |
| N2:1128 | 定員 — new | 1435400:1–2 | CLEAN | CLEAN | CLEAN |
| N2:1129 | 定価 — new | 1435410:1 | CLEAN | CLEAN | CLEAN |
| N2:1130 | 低下 — new | 1434250:1 | CLEAN | NEEDS FIX — F03 | CLEAN |
| N2:1131 | 定期券 — new | 1435510:1 | CLEAN | NEEDS FIX — F01 | CLEAN |
| N2:1132 | 定休日 — new | 1435540:1 | CLEAN | CLEAN | CLEAN |
| N2:1133 | 停止 — new | 1434920:1–3 | CLEAN | NEEDS FIX — F04 | CLEAN |
| N2:1134 | 停車 — new | 1434960:1 | CLEAN | NEEDS FIX — F01 | CLEAN |
| N2:1135 | 停電 — new | 1435020:1 | CLEAN | NEEDS FIX — F01 | CLEAN |
| N2:1136 | 出入り — new | 1339910:1–4 | NEEDS FIX — F02 | CLEAN | CLEAN |
| N2:1137 | 出入口 — reused | 1598540:1 | CLEAN | CLEAN | CLEAN |
| N2:1138 | 手入れ — new | 1328250:1; additional 2 | CLEAN | CLEAN | CLEAN |
| N2:1139 | テーマ — new | 1078830:1 | CLEAN | CLEAN | CLEAN |
| N2:1140 | 出かける — reused; raw 出掛ける | 1598550:1–2 | CLEAN | CLEAN | CLEAN |
| N2:1141 | 出来上がり — new | 1340600:1–2 | CLEAN | CLEAN | CLEAN |

**Mapping assessment: CLEAN for all twenty identity, reading, level, and selected/additional-sense associations.** In particular:

- 吊す is explicitly recognized under 吊るす; 吊る remains separate from fishing 釣る. The failed raw-alias endpoint supplies no positive evidence, but the canonical capture does.
- 強気 teaches つよき, not the unrelated ごうぎ headings. 停止 correctly excludes mourning sense 4 from ordinary ていし teaching.
- The public 手洗い body supports する. 停車’s examples are appropriately bounded rather than asserting universal intransitivity.
- 定期券’s period/section conditions and 定休日’s recurring closure schedule have substantive supplementary support.
- 手入れ’s police-raid sense is explicitly additional, not independently N2-labelled. テーマ’s German origin is explicit; search-only テマ is not promoted.
- 出来上がり is correctly taught as a noun rather than reproducing the raw list’s defective predicative/made-for glosses.

**Related kanji edits:**

| File | Correctness | Scoped coverage | Comprehensibility | Baseline metadata preservation |
|---|---|---|---|---|
| `kanji\低.md` | CLEAN | CLEAN | CLEAN | CLEAN |
| `kanji\券.md` | CLEAN | NEEDS FIX — F01 | CLEAN | CLEAN |
| `kanji\停.md` | CLEAN | NEEDS FIX — F01 | CLEAN | CLEAN |

| Required pair / actual word reading | Substantive word-side link | Relevant reading-row example | Common words link |
|---|---|---|---|
| 低 / 低下 — ていか | Present | Present | Present |
| 券 / 定期券 — ていきけん | Present | **Missing** | Present |
| 停 / 停止 — ていし | Present | Present | Present |
| 停 / 停車 — ていしゃ | Present | **Missing** | Present |
| 停 / 停電 — ていでん | Present | **Missing** | Present |

All written Han characters are retained in new-word metadata, and existing component cards receive substantive word-side links. The absent 逢/価/遭/吊/釣/這 cards were not invented.

**Reused-card preservation: CLEAN against the supplied patch.** 出会い retains its primary identity, title, N3, `[出, 会]`, and original 出会う guard; the 出合い recognition and 合 link address encounter senses 1–2 without claiming confluence coverage. 出かける retains its primary identity, title, N5, and `[出]`; the 掛 link and `出かけるところです` guidance are bounded and distinguish impending departure from resulting absence in `出かけています`. 出入口 preserves its identity, reading, title, and components while adding sourced N2, translated examples, and a defensible correction to the architectural restriction.

## Findings: five actionable findings

**F01 — Minor; scoped coverage; `kanji\券.md:30,38`, `kanji\停.md:30,37–39`.**

The Common words additions do not complete the explicitly requested reading-row reciprocity. 券’s ケン row contains only 券; 停’s テイ row contains only 停止. Consequently, 定期券, 停車, and 停電 remain absent from their relevant reading rows.

**Minimal remedy:** add linked whole-word examples 定期券 **ていきけん**, 停車 **ていしゃ**, and 停電 **ていでん** to the existing on-reading rows. Preserve metadata. **Evidence:** complete kanji cards, the related patch, and substantive word-side links in `words\定期券.md:27`, `words\停車.md:27`, and `words\停電.md:26`. **Confidence: high.**

**F02 — Minor; correctness/source attribution; `words\出入り.md:35–37`.**

“The dictionary also has ではいり, but **its spelling 出入**…” inaccurately describes the pinned family. Complete entry 1339910 lists 出入り, rare 出這入り, and search-only 出はいり—not 出入. It restricts でいり to 出入り while leaving ではいり unrestricted within its listed spellings.

The card’s recommendation to use 出入り is sound, but its explanation invents a spelling association in the cited entry. Moreover, the fresh [精選版 日本国語大辞典 entry for 出入](https://kotobank.jp/word/%E5%87%BA%E5%85%A5-529006) has a でいり heading, so the pinned restriction must not be generalized into a language-wide prohibition.

**Minimal remedy:** replace the problematic clause with: “The pinned entry restricts でいり to 出入り and also records ではいり. Use 出入り for this card.” **Evidence:** complete principal record 1339910 in both principal renderings; the cited public lexical entry. **Confidence: high.**

**F03 — Minor; scoped coverage/quiz ambiguity; `words\低下.md:9`.**

The direct **低下 / 落ちる** exclusion is missing from both headers. Their complete titles differ—“decline; lowering; deterioration” versus “fall down”—but 落ちる has an ordinary decline/deterioration sense. When 落ちる is the prompt, 低下’s label is therefore defensible. The old article’s expressly physical teaching focus does not remove that ordinary secondary meaning from the word.

**Minimal remedy:** add 落ちる to 低下’s exclusions; no old-body expansion is required. **Evidence:** `words\落ちる.md:4,38–41`; complete JMdict **1548550:3**, explicitly covering decreases in popularity, quality, speed, and sales, including “decline” and “deteriorate”; corroborating 精選版 日本国語大辞典, 落ちる, section 三. **Confidence: high.**

**F04 — Minor; scoped coverage/quiz ambiguity; `words\停止.md:9`.**

Direct guards are missing between **停止 and 上がる, 壊れる, and 落ちる**. These are not merely machine-related vocabulary:

- 上がる’s ordinary secondary senses include cessation of rain and cutting out/stopping work.
- 壊れる’s complete title is **“break; stop working”**; the latter alternative can reasonably answer the stopping-of-operation use of 停止.
- 落ちる ordinarily describes a website/server going down or crashing.

Thus “stoppage; suspension” can be a defensible alternative for the relevant secondary readings, despite the older cards’ different primary labels. Existing guards elsewhere do not protect these direct pairs.

**Minimal remedy:** add the three IDs to 停止’s exclusions, without claiming unrestricted substitution between the Japanese words. **Evidence:** `words\停止.md:4,16–21`; `words\上がる.md:4,32`; `words\壊れる.md:4,15,34`; complete JMdict **1352290:13–14** and **1548550:23**. Fresh corroboration: [Digital Daijisen 上がる, 6㋒/㋖](https://kotobank.jp/word/%E4%B8%8A%E3%81%8C%E3%82%8B-422942), and [精選版 日本国語大辞典 壊れる, ②](https://kotobank.jp/word/%E5%A3%8A%E3%82%8C%E3%82%8B-505755). **Confidence: high.**

**F05 — Minor; scoped coverage/quiz ambiguity; `words\釣り合う.md:9,16–23`.**

Direct guards to **揃う** and **適当** are absent. Their complete titles are “be complete; be all present; **match**” and “**suitable**; careless.” The matching and suitability alternatives overlap the selected 釣り合う sense “to suit; go well together; be a good match,” explicitly taught in the desk/chair example and suitable-match construction.

This is not an assertion that uniformity always means compatibility, or that 適当’s careless sense applies to 釣り合う. It is a narrower quiz-label ambiguity; existing 合う/マッチ/適する guards cannot supply these edges transitively.

**Minimal remedy:** add 揃う and 適当 to 釣り合う’s exclusions. **Evidence:** both complete old bodies and titles (`words\揃う.md:4,16–24`; `words\適当.md:4`); principal **1434050:2**; fresh 精選版 日本国語大辞典 entries [揃う, ①](https://kotobank.jp/word/%E6%8F%83%E3%81%86-555686), [適当, ②](https://kotobank.jp/word/%E9%81%A9%E5%BD%93-575436), and [釣合う, ②](https://kotobank.jp/word/%E9%87%A3%E5%90%88%E3%81%86-572796). **Confidence: medium-high.**

## Optional: none

No exhaustive synonym expansion, additional missing kanji cards, or unrelated baseline redesign is recommended.

## Limits: provenance and bounded linguistic review

- Git resolution, parent-object comparison, hashes, and derivative equivalence were **not independently executed**. Metadata-preservation judgments use the supplied patch and visible files.
- Supplied public captures remain author captures. Their twenty-two positive lexical bodies represent **one dictionary service/source collection**, not twenty-two independent dictionaries. The failed raw 吊す endpoint is not positive evidence.
- Fresh Weblio requests for 揃う, 適当, and 出入 yielded no usable lexical bodies. Kotobank supplied relevant alternative evidence; empty Digital Daijisen sections and the unrelated 落ちる book heading were not used as lexical verification.
- The reported 136-family/358-sense union is an author inventory, not an independently executed count. Reading all supplied family renderings does not establish absence elsewhere.
- This is a bounded editorial review, not exhaustive corpus/frequency analysis, every possible quiz-pair audit, or native-speaker certification. **CLEAN** means no actionable defect established within the stated scope.
