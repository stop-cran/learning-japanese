Snapshot: f8f3db8c9ae7d88d72cdc3d8eaae84c8f736ca5f, batch 154. Reviewer: OpenAI GPT-family model; the exact model/version identifier is not exposed to me. The packet-manifest.json SHA-256 matches 12817983e0c88ddba45c5a38130c88ff9770e8eb246f3e5bdadf1bbf135ca3aa.

Scope:

Independent, blind, read-only review of all 15 new cards, all 15 stroke files, and all 22 existing-file diffs. Consistency/quiz safety and beginner comprehensibility received the deepest examination. Paths below are relative to the supplied packet.

Files actually opened:

- **Full text reviewed:** INSTRUCTIONS.md; mechanical-checks.md; rubric\copilot-instructions.md.
- **Full text reviewed:** snapshot\kanji\随.md, 隠.md, 隣.md, 雄.md, 雷.md, 霧.md, 項.md, 顕.md, 飼.md, 飽.md, 飾.md, 驚.md, 鬼.md, 鮮.md, 黙.md.
- **Full files parsed and structurally checked:** snapshot\strokes\随.json, 隠.json, 隣.json, 雄.json, 雷.json, 霧.json, 項.json, 顕.json, 飼.json, 飽.json, 飾.json, 驚.json, 鬼.json, 鮮.json, 黙.json. This included every stroke's ID, type and points, source revision, counts and identity.
- **Full files loaded for replacement checks; semantic reading limited to changed passages and their context:** snapshot\kanji\塊.md, 微.md, 鏡.md; snapshot\words\新鮮.md, 随筆.md, 隠す.md, 隠れる.md, 隣.md, 雄勁.md, 雷.md, 霧.md, 項目.md, 顕微鏡.md, 飼う.md, 飽きる.md, 飽くまで.md, 飾り.md, 飾る.md, 驚かす.md, 驚く.md, 鬼.md, 黙る.md.
- **All 22 diffs read in full:** diffs\kanji__塊.md.diff, kanji__微.md.diff, kanji__鏡.md.diff; diffs\words__新鮮.md.diff, words__随筆.md.diff, words__隠す.md.diff, words__隠れる.md.diff, words__隣.md.diff, words__雄勁.md.diff, words__雷.md.diff, words__霧.md.diff, words__項目.md.diff, words__顕微鏡.md.diff, words__飼う.md.diff, words__飽きる.md.diff, words__飽くまで.md.diff, words__飾り.md.diff, words__飾る.md.diff, words__驚かす.md.diff, words__驚く.md.diff, words__鬼.md.diff, words__黙る.md.diff.
- **Full text reviewed:** evidence\joyo-pages.md; evidence\kanjivg-components.txt; evidence\daijisen-heads.txt; evidence\okurigana-scan.txt; evidence\audits\quiz-safety.txt; evidence\audits\reading-exposure.txt; evidence\audits\reading-options.txt; evidence\audits\kanji-remarks.json; evidence\audits\word-remarks.json; evidence\audits\kanji_remarks.py.
- **Full files parsed; relevant records examined:** evidence\source-metadata.json and evidence\kanjidic2-records.xml, checking all 15 characters; evidence\jmdict-families.xml, examining the complete cited entries, readings, restrictions and senses for all 15 cards; evidence\jmdict-digest.tsv, with focused inspection of 雄 and 飽 vocabulary priorities; evidence\kanjipedia-outside-readings.json, including the URLs used for independent retrieval.
- **Full file parsed, partial direct text reading:** evidence\kanjivg-svgs.txt. All 15 SVG documents were parsed and their stroke order, types and rounded starting coordinates compared with the JSON; its opening 65 lines were also read directly.
- **Full indexes parsed:** titles\kanji-titles.tsv; titles\word-titles.tsv. These supplied corpus-level title uniqueness, exact quoted titles, link identities and comparison labels, without opening corpus folders wholesale.
- **Full text reviewed:** evidence\app-code\QuizBuilder.kt; evidence\app-code\KanjiMeaningMetadata.kt; repo\kanji\仏.md, 追.md, 側.md, 沈.md.
- **Partial text reviewed:** evidence\app-code\KanjiReadings.kt, lines 1–205; evidence\audits\extra-readings.json, lines 1–340; evidence\provenance.json, its opening 65 lines; packet-manifest.json, its opening 20 lines plus a whole-file hash; repo\docs\content-format.md, the kanji/quiz and stroke-format material around lines 86–326; repo\docs\confusable-words.md, its opening 85 lines. Two initial oversized read results were truncated; relevant material was subsequently retrieved in bounded reads. I do not count unseen output as reviewed.

Independent public checks inspected actual entries, not search snippets:

- Live Kanjipedia entries linked by every new card: readings, 外 marks and relevant senses for all 15 characters.
- Live Weblio Digital Daijisen entries for all 15 characters, plus まにまに, 隠る, 蓮霧, 雄勁, 飽かす, 飽く, 黙す, 隣る, 仏, 追う, 側, 沈 and 沈む.
- Actual Jisho dictionary API entries for 随筆, 随に, 随う, 隠す, 隠れる, 隠居, 隠密, 隠し, 隣, 隣人, 隣る, 雄勁, 雄しべ, 雄, 雷, 雷雨, 霧, 濃霧, 蓮霧, 項, 項目, 顕微鏡, 顕れる, 飼う, 飼育, 飽きる, 飽くまで, 飽く, 飽かす, 飽和, 飾る, 飾り, 装飾, 驚く, 驚かす, 驚異, 鬼, 鬼才, 鬼百合, 新鮮, 鮮やか, 黙る, 沈黙, 黙す, 黙り, しじま, 追う, そば, いんぺい, 雷こう, もくする, 黙とう, 鮮少 and 英雄. Endpoint: https://jisho.org/api/v1/search/words?keyword= followed by the encoded term. Relevant Japanese forms, readings, senses, restrictions and register fields were inspected.
- Actual Jisho kanji entries for 隠, 霧, 顕, 黙 and 雷, independently corroborating the unusual/source-only reading lists.

Verdicts:

- Correctness: **CLEAN**.
- Scoped coverage: **CLEAN**.
- Consistency and quiz safety: **NEEDS FIX** — two missing direct exclusions, G1–G2. Neither is a collision in the default full-pool options printed by the packet.
- Comprehensibility: **CLEAN**, with nonblocking suggestions below.

Per-card verdicts:

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 随 | CLEAN | CLEAN | NEEDS FIX — G1 | CLEAN |
| 隠 | CLEAN | CLEAN | CLEAN | CLEAN |
| 隣 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 雄 | CLEAN | CLEAN | CLEAN | CLEAN |
| 雷 | CLEAN | CLEAN | CLEAN | CLEAN |
| 霧 | CLEAN | CLEAN | CLEAN | CLEAN |
| 項 | CLEAN | CLEAN | CLEAN | CLEAN |
| 顕 | CLEAN | CLEAN | CLEAN | CLEAN |
| 飼 | CLEAN | CLEAN | CLEAN | CLEAN |
| 飽 | CLEAN | CLEAN | CLEAN | CLEAN |
| 飾 | CLEAN | CLEAN | CLEAN | CLEAN |
| 驚 | CLEAN | CLEAN | CLEAN | CLEAN |
| 鬼 | CLEAN | CLEAN | CLEAN | CLEAN |
| 鮮 | CLEAN | CLEAN | CLEAN | CLEAN |
| 黙 | CLEAN | CLEAN | CLEAN | CLEAN |

All 15 stroke files and the scoped changes to 塊, 微, 鏡 and the 19 word articles are CLEAN within the checks described here.

Review observations supporting those verdicts:

- All 15 cards' stroke counts, grades, classical radical numbers and ordered on/kun lists agree with the supplied metadata and XML. Every metadata reading has a table row, including explicitly source-only readings. Every selected quiz reading has the required linked example. All new titles are unique in the title index, and checked quoted card titles match, allowing normal sentence punctuation inside English quotation marks.
- Rare spellings, archaic 隣る, poetical いかずち, literary 黙す, the お-/おに- notation and the non-KANJIDIC2 readings in Notes are appropriately distinguished from selected quiz material. Source-only よる, ボウ and ボク are not presented as ordinary example-backed questions. The Joyo reading/example/old-form statements match the supplied official-table extracts.
- The modern-shape mnemonics are explicitly non-etymological. Their component and placement descriptions agree with the pinned KanjiVG groups; notably 随's sweep belongs to the right-hand construction, and 黙's bottom dots run beneath both upper portions. I found no unsupported historical claim.
- I examined all 45 curated meaning distractors against the displayed labels and ordinary secondary meanings in both directions. The printed default choices remain defensibly wrong. Shared weather, food-side shapes, emotional associations or membership in compounds do not alone make two answers synonymous. The listed within-batch contrasts likewise do not establish another necessary exclusion.
- Existing exclusions were assessed as direct pairs, not as transitive cliques. The supplied character senses and dictionary entries substantiate the broad-title and secondary-sense precautions. G1–G2 concern additional direct overlaps, not a proposal to expand the existing groups into cliques.
- 鬼/仏 requires care because both can concern the deceased. However, the actual option “Buddha; Buddhism” is not a gloss for 鬼's deceased-spirit sense, and “demon; ogre” is not a gloss for 仏. I did not establish a double-correct displayed answer from that association.
- The reading audits are consistent with the inspected selection code: curated readings are attempted first, full metadata readings and mutations are protected, and fallback is used only for remaining slots. 鮮's on question gets タン from 淡 and requires two fallback options; 腐 and 濁 do not supply on options.
- The exposure report contains exactly the stated eight latent collision records: 隠 お/なまる; 雄 かつ/ゆ/よう; 飼 かい; 飽 あき; 飾 しか. Its three one-holder cases are the name-only readings 雄 ゆ, 雄 よう and 飼 かい. The zero production and base padded-session counts are not contradicted by those different cases. The absence of HIT in reading-options.txt does not mean that no lower-tier or name-only candidate exists.
- The okurigana-scan additions have traceable lexical provenance. Forms such as いんぺい, らいこう and もくとう are conservative audit inputs from whole written words, not grounds for teaching those entire strings as independent kun readings of 隠, 雷 or 黙.
- Each word diff removes one line and adds one line; undoing its single new kanji link exactly recovers the old line. All 19 targets are the intended new cards; no changed line adds or removes Dictionary:. Each of the three kanji diffs is exactly its declared old-to-new replacement. The passages remain grammatical, the quoted 鬼/顕 titles are exact, 顕 supplies けん in けんびきょう, and 眼 is absent from the kanji title index as the remaining 鏡 note says.
- The learner-facing core is understandable: central meanings come first, concrete mnemonics are honest, and okurigana/stem explanations are supplied where needed. There are no new Japanese example sentences whose grammar or translation needs separate adjudication. The main presentation weakness is reference density rather than an established misleading explanation.

Findings:

1. **G1 — Minor; consistency and quiz safety; snapshot\kanji\随.md:14. Missing direct exclusion with 追.**

   **Claim and impact:** 随's displayed “follow; at will” overlaps an ordinary meaning of 追, whose displayed title is “chase; pursue.” This is not inferred merely from 追随: the existing 追 card explicitly teaches “following after something” and “chasing or following.” Public dictionaries independently give 追う “to follow after,” and Daijisen's first sense includes あとをついて行く. Consequently the 随 title can be accepted as a meaning answer for 追, even though pursuing is not identical to every use of 随.

   Neither card records the pair. Both currently have three curated options in the full pool, so the supplied default simulation does not expose it. The omission matters when fallback is needed: in a reduced pool containing 追, 近, 週 and 随, 追's available curated cards fill two wrong slots and 随 fills the remaining slot. This is a reduced-pool illustration of the inspected builder, not a claimed shipped-stack reproduction.

   **Remedy:** Add 追 to 随's quiz_exclusions; one declaration suffices. Do not change either accurate title or infer exclusions through other cards.

   **Evidence:** repo\kanji\追.md:20–21,31; evidence\app-code\QuizBuilder.kt; actual [Daijisen 追う](https://www.weblio.jp/content/%E8%BF%BD%E3%81%86); actual [Jisho 追う entry](https://jisho.org/api/v1/search/words?keyword=%E8%BF%BD%E3%81%86).

   **Confidence:** High for the direct semantic overlap and missing reciprocal declaration; bounded as to runtime exposure.

2. **G2 — Minor; consistency and quiz safety; snapshot\kanji\隣.md:14. Missing direct exclusion with 側.**

   **Claim and impact:** The ordinary locational reading 側 そば includes “(place) right next to” and “beside,” overlapping 隣 となり “next (to); adjoining; adjacent.” The existing 側 card explicitly teaches “the part next to something.” Thus the generic “side” and “next door; adjoining” labels are not safely separated merely by assigning different English words to them. The overlap is limited to the locational senses; this does not assert that every use of 側 means a next-door neighbour.

   Neither card records the pair. Again, the printed full-pool curated choices are safe. In a reduced pool containing 側, 内, 右 and 隣, 側 has only two available curated cards, allowing the overlapping 隣 label into the remaining slot.

   **Remedy:** Add 側 to 隣's quiz_exclusions. Keep the exclusion pairwise; no broader spatial clique is warranted.

   **Evidence:** repo\kanji\側.md:23,31; 隣's cited JMdict entry 1555830; actual [Daijisen 側](https://www.weblio.jp/content/%E5%81%B4), including the そば entry and usage discussion; actual [Jisho そば entries](https://jisho.org/api/v1/search/words?keyword=%E3%81%9D%E3%81%B0), specifically 側/傍 rather than 蕎麦; evidence\app-code\QuizBuilder.kt.

   **Confidence:** Medium-high; the direct dictionary overlap is clear, while the severity is limited by the currently curated full-pool choices.

Optional:

- **飽.md:33–44:** Briefly gloss the already quoted ……に飽かして as “using freely/lavishly,” rather than leaving only 飽かす's “bore; tire” sense nearby. JMdict 1518280 sense 2 and live Daijisen support this. Also consider marking independent 飽く as written/literary in modern usage; Daijisen explicitly contrasts it with everyday 飽きる. That qualification should not suggest that the common adverb あくまで is itself rare or literary.
- **雄.md, Common words:** One plain-text example 英雄 えいゆう — hero would connect the title's “hero” directly to a high-priority familiar family. The sole linked example 雄勁 is correctly read and glossed, but the live Daijisen entry places it especially in forceful artistic/literary expression. No new word article is required for this polish.
- Consider shortening the learner-visible dictionary-by-dictionary explanations and long exclusion rationales, especially on 随, 隠, 雄, 顕 and 鮮, while retaining the source references and all justified metadata. Their openings are clear, but the reference apparatus makes phone reading substantially longer than the core lesson.

Limits:

- Exact model/version identity is unavailable; I have not invented one or independently verified the other reviewer's model family. I did not seek or inspect another review or the author's rationale.
- Calls were serial, one tool call per response; no agents, other sessions, background jobs or corpus-folder scans were used. Public retrieval loops were synchronous. No generated oversized-output capture outside the packet was opened.
- Full-file parsing is distinguished from full human-readable inspection in Scope. I did not independently examine all unrelated JMdict families, every row of either title index, or the rest of the two large repository-format documents.
- The packet's production/padded-pool audit outputs were inspected against relevant app logic, not regenerated by scanning the corpus. Reduced-pool illustrations in G1–G2 are deliberately not assertions of current production hits. I found no established non-name reading collision in the reported production or padded pools.
- I did not regenerate cubic-curve interpolation or render stroke animations on a phone. JSON structure, all stroke types/order/startpoints and pinned component evidence were checked; interior sample fidelity was not independently recomputed.
- Five kanjiapi.dev requests returned HTTP 403. Live Jisho kanji entries supplied the needed unusual-reading corroboration instead. Live Jisho's word API does not expose every pinned spelling-level rarity flag; those flags were checked directly in the packet XML rather than inferred from API omissions.
- CLEAN means no actionable defect established within the stated scope, not exhaustive correctness or measured beginner usability. Existing material outside the edited passages was not subjected to a new full linguistic review. Packet completeness and its representation of the base-to-snapshot diff were accepted; no external checkout was accessed.
