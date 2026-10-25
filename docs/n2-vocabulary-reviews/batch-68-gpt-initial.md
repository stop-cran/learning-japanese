## Snapshot: fc23c8b22dc373e0a087e4ee7f09b550a50d870f — committed content only

Parent: `b2ae1ea479c1b24020216c361ceb4f69b23a13d9`.

This review targets the committed freeze identified by `frozen-snapshot.json`, which I read first. The available file tools cannot execute Git, so I could not independently verify HEAD, worktree cleanliness, or correspondence with the parent; those assertions rely on the supplied snapshot and patch.

## Scope

**Reviewer:** gpt-6.1-sol, family **gpt**. Read-only; no agents, delegation, or edits.

Read all twenty assigned articles completely, all four edited kanji articles completely, and the complete `related.patch`. Also read the required repository instructions and `docs\content-format.md:18–103`; the TSV header and exactly N2:1342–N2:1361; both permitted repository source snapshots; all twenty mappings and complete principal families, including restrictions, flags, inherited POS, raw fields, and selected/additional senses.

Evidence reads included all fifteen complete-family renderings—the supplied 398-family/914-sense union—all 31 component records, all 228 navigation labels, and all sixteen older-body renderings containing 131 complete comparison articles. Additional complete bodies read directly were **示す, あんまり, 案, 背, 過剰, 強い, オーバー, 大層, 言い出す, あまり**, plus the separate convention checks **毎朝, 台所, 場所**. Read both allowed comparison/policy documents and all frozen public bodies and receipts.

Used the compact derivatives rather than reading the large `review-evidence.json` end-to-end; only its first 130 lines were additionally inspected. Author rationale, excluded ledgers, and other reviewers’ reports were not read. The author’s 96 unselected older-body candidates were not all independently inspected.

## Verdicts

**Ten rows have an actionable finding; ten are CLEAN across all three facets.** The ばつ lexical-type classification remains **UNVERIFIED**. Required quiz-guard omissions are recorded under scoped coverage; this does not make otherwise sound definitions incorrect. CLEAN means no actionable defect established within the actual scope.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1342 | 肌着 | CLEAN | CLEAN | CLEAN | はだぎ, next-to-skin meaning, metadata and component links sound. |
| N2:1343 | 果たして | CLEAN | NEEDS FIX | CLEAN | 果して recognized; confirmation/question distinction sound. F03. |
| N2:1344 | 鉢 | CLEAN | CLEAN | CLEAN | Assigned はち meanings distinguished; 鉢 retained despite absent component card. |
| N2:1345 | ばつ | UNVERIFIED | NEEDS FIX | CLEAN | Mark meaning verified; type unresolved and raw ｘ needs positive source binding. F01–02. |
| N2:1346 | 発揮 | CLEAN | CLEAN | CLEAN | Ability/power use, transitivity and limits adequately explained. |
| N2:1347 | バック | CLEAN | NEEDS FIX | CLEAN | Blank source spelling preserved; recognition senses qualified. F04. |
| N2:1348 | 発射 | NEEDS FIX | NEEDS FIX | CLEAN | Projectile action—not apparatus—correct; 打つ comparison/guard needs correction. F05. |
| N2:1349 | 発想 | CLEAN | NEEDS FIX | CLEAN | Idea, approach and musical-expression teaching distinguished. F06. |
| N2:1350 | 発電 | CLEAN | CLEAN | CLEAN | Electricity generation and additional telegram recognition properly separated. |
| N2:1351 | 発売 | CLEAN | CLEAN | CLEAN | Release-for-sale meaning and 発売中 distinctions sound. |
| N2:1352 | 派手 | CLEAN | NEEDS FIX | CLEAN | Mixed/on-first classification follows checked convention. F07. |
| N2:1353 | 話し合い | CLEAN | NEEDS FIX | CLEAN | 話合い recognized; mutual discussion need not produce agreement. F08. |
| N2:1354 | 話しかける | CLEAN | NEEDS FIX | CLEAN | 話し掛ける recognized; addressee に and ichidan forms sound. F09. |
| N2:1355 | 話し中 | CLEAN | CLEAN | CLEAN | 話中 recognized; telephone and ongoing-talk senses appropriately limited. |
| N2:1356 | 甚だしい | CLEAN | NEEDS FIX | CLEAN | Degree, negative tendency, conjugation and register sound. F10. |
| N2:1357 | 花火 | CLEAN | CLEAN | CLEAN | Reused article; patch adds only sourced `jlpt: 2`. |
| N2:1358 | 花嫁 | CLEAN | CLEAN | CLEAN | Bride/newlywed role and component associations adequately qualified. |
| N2:1359 | 放れる | CLEAN | NEEDS FIX | NEEDS FIX | Release-focused identity correct; explain departure/source を. F11. |
| N2:1360 | 羽 | CLEAN | CLEAN | CLEAN | 羽根 はね shuttlecock teaching satisfies the restricted senses; stable 羽 stays N3. |
| N2:1361 | ばね | CLEAN | CLEAN | CLEAN | Blank source spelling, kana identity and variant/sense restrictions preserved. |

**Kanji edits — each CLEAN / CLEAN / CLEAN**, in correctness/scoped-coverage/comprehensibility order:

- **肌:** `kanji\肌.md:32,37,45` supplies reciprocal 肌着 **はだぎ**, substantive compound teaching, and footer ID **1476500**.
- **羽:** existing 羽 **はね** pair remains; `kanji\羽.md:43–46` adds the 羽根 alias link and appropriate restrictions, retaining **1171680**.
- **根:** `kanji\根.md:43–46` substantively links 羽根 **はね** to the stable 羽 article, adds **1171680**, and does not assert a new character reading or literal plant-root interpretation.
- **放:** `kanji\放.md:33,40,52` supplies reciprocal 放れる **はなれる** and **1516540**. Its header remains **N3**, not a new N2-kanji claim.

**Baseline preservation — CLEAN / CLEAN / CLEAN:** the supplied patch preserves all four kanji headers. 花火’s existing body is unchanged. 羽 retains its stable identity, primary reading/title, `jlpt: 3`, primary metadata, original 翼 exclusion, and original feather/wing teaching. Those reused passages are not newly authored. Primary written Han remain represented in metadata; missing component cards were not invented.

**Mappings:** all twenty row→article→family/reading/sense associations are **CLEAN**, with twenty distinct identities: eighteen new and two reused. Raw blanks are preserved. 羽根’s `teachingSpelling: 羽根` correctly supports its spelling-restricted hanetsuki sense within stable 羽. Mapping comprehensibility is **CLEAN**; the declared explicit source-form coverage for N2:1345 needs the article clarification in F02. Additional recognition teaching does not independently establish N2 for every added sense.

## Findings

For quiz findings, I compared full titles, complete older bodies, and relevant ordinary secondary senses. Each reported pair lacks a direct exclusion at both endpoints. Add each justified edge once; symmetric guards suffice, but neighboring edges do not provide transitive protection.

**F01 — Medium; correctness UNVERIFIED — `words\ばつ.md:6–8,23–25`.**

`wago` is assigned as a “practical grouping” although the derivation remains uncertain. Kana spelling and uncertainty do not positively establish native origin. The frozen mark-name evidence and the independently retrieved [Kotobank/Seisenban ばつ entry](https://kotobank.jp/word/%E3%81%B0%E3%81%A4-602173) tentatively connect it with ばってん/罰点; neither settles the classification. **Remedy:** substantiate the type through lexical evidence or an explicitly sanctioned classification convention; do not automatically substitute `kango` either. **Confidence:** high that the present evidence leaves the type unresolved—not that `wago` has been disproved.

**F02 — Minor; scoped coverage — `words\ばつ.md:15–16,35–37`.**

The positive teaching binds ばつ/バツ to **×**. Raw source **ｘ** appears only in the alphabet-letter warning, without explicitly stating its source-row mark reading. The warning is qualified correctly; it does not say ｘ can never be ばつ. **Remedy:** add one sentence explaining that this source row writes ｘ and supplies バツ for the incorrect-answer cross, not the alphabet-letter name. **Evidence:** N2:1345, mapping/principal **2197150:1**, and the cited passages. Preserve the blank gloss and stable kana identity. **Confidence: high.**

**F03 — Medium; scoped coverage — `words\果たして.md:4,9,16–20`.**

Add a direct **果たして / さすが** guard. “Sure enough” and “as expected” collide in expectation-confirming uses; `words\さすが.md:4,16,46` explicitly permits that positive confirmation. Complete families **1600780:1** and **1552390:1** support the overlap. Existing やはり/やっぱり edges are nontransitive. **Remedy:** exclude the pair at either endpoint without erasing their distinctions. **Confidence: high.**

**F04 — Medium; scoped coverage — `words\バック.md:9,17–25,43–45`.**

Missing direct guards remain for **下がる, 背, バッグ, 返す, 賛成**. These arise independently: 下がる explicitly teaches “step back” (`:18`); 背 recognizes back/rear (`:30–32`); バッグ’s family **1099100** flags バック as irregular kana usage; 返す’s title is “return something” and fits the explicitly recognized refund sense; 賛成’s title includes “support,” matching backing/support. See **1098760:1,3,4,6**, `words\返す.md:4,15–16`, and `words\賛成.md:4,15–17`. **Remedy:** add these specific guards, retaining the restrictions and spelling qualification—not a general support/return clique. **Confidence: high for the first three; medium-high for the context-specific refund/support collisions.**

**F05 — Medium; correctness and scoped coverage — `words\発射.md:9,30`.**

The shooting comparison is attached to **打つ**, whose linked title is “hit; strike,” rather than the modern shooting identity **撃つ／射つ**. Complete captured **1408810** has seventeen 打つ senses; **1253570:1** positively supplies “shoot/fire” with 撃つ／射つ. Exact evidence: `batch-68-family-inspection-07.txt:89–108` and `batch-68-family-inspection-04.txt:47–50`. Shared うつ pronunciation does not justify transferring that identity or its quiz guard. **Remedy:** distinguish **撃つ（うつ）** in plain text and remove the unsupported 打つ exclusion unless a separate actual-title collision is demonstrated. No missing 撃つ card needs creating. **Confidence: high for the modern instructional distinction; this is not a claim about every historical spelling.**

**F06 — Medium; scoped coverage — `words\発想.md:4,9,16–20`.**

Add **発想 / 案**. The complete existing 案 body explicitly defines an idea and translates 何かいい案はありますか as “Do you have any good ideas?” (`words\案.md:4,16–18`). Thus 発想’s displayed “idea” label is defensible for 案 even though 案’s own title foregrounds proposal/draft. **Remedy:** add the direct guard; do not inherit every “thought/plan” neighbor. **Confidence: high.**

**F07 — Medium; scoped coverage — `words\派手.md:2–9,15–20`.**

Add **派手 / オーバー** for behavioral overstatement. This is not merely shared appearance vocabulary: the frozen Daijisen 派手 definition includes exaggerated behavior, while `words\オーバー.md:4,9,16,20,30` teaches exaggerated/overdone expression and behavior. **Remedy:** add the specific pair while retaining 派手’s ordinary flashy/showy teaching. Its mixed-reading `kango` label is not the defect. **Confidence: medium-high.**

**F08 — Medium; scoped coverage — `words\話し合い.md:4,9,16–20`.**

Add direct guards with **話, 話す, 論じる**. 話’s title includes “talk” and complete **1600900:3** includes discussion/negotiation; **1562350:2** gives 話す a discussion use; 論じる’s full body and title explicitly teach “discuss” (`words\論じる.md:4,16–18`). Their relevant English labels collide with discussion/talking things over. **Remedy:** guard these pairs independently; the existing 話し合う edge does not protect them. Different POS alone is not an exemption. **Confidence: high.**

**F09 — Medium; scoped coverage — `words\話しかける.md:4,9,16–23`.**

Add **話しかける / 言い出す** and **話しかける / しゃべる**. 言い出す explicitly teaches beginning to say something (`:4,16–18`), overlapping the additional beginning-to-talk sense **1562300:2**. しゃべる’s “talk; chat” title and person-に addressing pattern (`:4,21`) overlap the talk-to-someone sense **1562300:1**. **Remedy:** add both direct guards without claiming unrestricted substitutability. **Confidence: high for 言い出す; medium-high for しゃべる.**

**F10 — Medium; scoped coverage — `words\甚だしい.md:4,9,16–21,38`.**

Add direct guards with **過剰, あんまり, あまり, 大変**. 過剰 teaches excess beyond appropriateness, including excessive reactions (`:4,16,33`); あんまり explicitly teaches “excessively” and “That is too much” (`:4,16,21`); あまり independently recognizes affirmative excessive degree (`:33`); 大変’s title includes “serious,” supported by **1415000:3** and the serious/severe range of **1370010:1**. **Remedy:** add these evidenced pairs, not every intensity adjective or adverb. The あまり judgment is independent of its あんまり edge. **Confidence: high for excess collisions; medium-high for 大変.**

**F11 — Minor; scoped coverage and comprehensibility — `words\放れる.md:16–20`.**

The article correctly labels the verb intransitive and explains から, then gives the correct attested 矢が弦を放れる without explaining を. A learner can mistake 弦 for a transitive object. **Remedy:** state that を here marks the point/source left, not an object acted upon. **Evidence:** the article’s own example and intransitivity statement; the complete existing 離れる article also explains this departure pattern. This is missing attachment guidance, not an incorrect example. **Confidence: high.**

## Optional

In `words\バック.md:41–42`, replace “facing backwards” with **“moving backwards”**. Reversing concerns motion direction, not where the vehicle or person faces. This is nonblocking wording polish.

## Limits

Git execution, hash recomputation, and independent equivalence checks were unavailable. Author-executed hash/equivalence checks were not counted as reviewer-executed checks. This is not exhaustive corpus, frequency, historical-origin, or native-speaker certification; navigation labels were not treated as complete-body evidence.

The frozen **26 requests / 24 nonempty extractions / 23 target-positive captures** represent **one authority: Digital Daijisen via Weblio**. Raw ｘ returned the wrong target エックス; raw 話合い and 話中 lacked selected bodies, while canonical forms were positive. I independently inspected the Seisenban cross-mark ばつ definition and Weblio’s modern 打つ・うつ section. Other attempted うつ/撃つ lookups returned unrelated headings or no usable target definition and were not treated as verification; F05 rests on the complete captured modern families and actual article identities. The unresolved positive classification claim is F01.
