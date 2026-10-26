## Snapshot: 36f7c0c4bdb997b4d2939cb191ee6cfe43a58cdb; committed content only

Frozen parent: `2d4524abd2a54dd70692950f443230d2d0a1204f`. The snapshot identifies **19 physical additions and one reused article, 紅葉**.

This identifies the supplied frozen snapshot, not an independently executed Git check. Available file tools cannot execute Git; I could not independently verify HEAD, worktree cleanliness, hashes, or equivalence with committed blobs.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Read-only review; no agents, delegation, edits, or concurrent calls. **57 sequential tool calls**.

Completely read:
- All twenty assigned articles; current 燃, 缶, and unchanged 紅 kanji bodies; `related.patch`; and the supplied three-kanji baseline inspection.
- Both instruction files and `docs\content-format.md:18–103`.
- TSV header and exactly physical rows **1682–1701**.
- All **20 mappings, 21 source/primary families, 34 component records, and 179 comparison labels**, using every prescribed lossless JSONL range.
- All **408 lines** of `public-bodies.txt`, distinguishing applicable headings/readings from wrapper material. These captures represent **one public dictionary authority**, not twenty independent authorities.
- Complete comparison-family files `family-inspection-01`, `-02`, `-04`, and `final-precard-comparison-reading`: **104 distinct complete JMdict families overall**, including the required 21.
- **20 distinct older word bodies**: 近代, 現代, 新しい, 流行, 米, 菓子, 無駄, 惜しい, 機能, きつい, 訓練, 指導, ごしごし, 元, 利口, 賢い, ずるい, 論争, 厄介, 迷惑.

Checked primary-component card existence with one narrowly scoped kanji glob. No prohibited ledgers, rationale-bearing batch file, authoring materials, or other reviewer reports were read. Remaining comparison bodies and families were not mechanically inspected; label availability was not counted as body inspection.

## Verdicts:

**Two localized quiz-exclusion defects were established.** The instructional prose, source coverage, and comprehensibility otherwise had no actionable defect established within the inspected scope.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1682 | モダン | CLEAN | CLEAN | CLEAN | Contemporary style, な/に attachment, and newness distinction taught. |
| N2:1683 | 餅 | CLEAN | CLEAN | CLEAN | Mochi identity clear; savory uses and compound-name qualification appropriate. |
| N2:1684 | もったいない | CLEAN | CLEAN | CLEAN | Waste and undeserving-recipient uses distinguished; religious use qualified. |
| N2:1685 | モデル | CLEAN | CLEAN | CLEAN | Core model/version uses covered; theoretical and inspiration uses distinguished. |
| N2:1686 | 元々 | CLEAN | CLEAN | CLEAN | Original-state uses, の modification, and bounded no-worse-off construction clear. |
| N2:1687 | 物置 | CLEAN | CLEAN | CLEAN | Storage place distinguished from storage activity and broader shed category. |
| N2:1688 | 物語る | CLEAN | CLEAN | CLEAN | Recounting and evidential indication covered with correct transitivity. |
| N2:1689 | 物差し | CLEAN | CLEAN | CLEAN | Measuring tool and figurative criterion both explicitly taught. |
| N2:1690 | 物凄い | NEEDS FIX | CLEAN | CLEAN | Missing direct guard with きつい; F85-01. |
| N2:1691 | モノレール | CLEAN | CLEAN | CLEAN | Single-rail identity and both principal designs covered without overrestriction. |
| N2:1692 | 紅葉（もみじ） | CLEAN | CLEAN | CLEAN | Maple coverage explicit; primary こうよう identity and earlier teaching retained. |
| N2:1693 | 揉む | NEEDS FIX | CLEAN | CLEAN | Recognized training/coaching meaning lacks two direct guards; F85-02. |
| N2:1694 | 燃やす | CLEAN | CLEAN | CLEAN | Literal/emotional uses, を, godan forms, and 燃える contrast correct. |
| N2:1695 | 催し | CLEAN | CLEAN | CLEAN | Organized-event noun and formation explained; accidental events and capability distinguished. |
| N2:1696 | 盛る（もる） | CLEAN | CLEAN | CLEAN | Serving, heaping, medicinal use, and slang separated from other readings. |
| N2:1697 | 問答 | CLEAN | CLEAN | CLEAN | Exchange/dialogue and discussion covered; individual questions/answers distinguished. |
| N2:1698 | やかましい | CLEAN | CLEAN | CLEAN | Noise, strictness, fussiness, に attachment, and public bothersome use handled. |
| N2:1699 | 夜間 | CLEAN | CLEAN | CLEAN | Nighttime period and modification clear; no universal clock-hour claim. |
| N2:1700 | 薬缶 | CLEAN | CLEAN | CLEAN | Kettle identity, usual kana, established reading, and historical/current-use distinction clear. |
| N2:1701 | 役者 | CLEAN | CLEAN | CLEAN | Performer and figurative shrewd-person uses distinguished; identical-title deduplication applicable to 俳優. |

**Kanji/baseline preservation — CLEAN within the supplied comparison evidence.** The patch preserves 燃/缶 metadata and unrelated teaching, adding the intended links, common-word entries, and 薬缶 source citation. 紅葉 changes only the source-scope sentence; its primary metadata and existing maple/foliage teaching remain intact. The supplied 紅 baseline matches the current body.

**Components — CLEAN.** All 21 distinct Han characters in the primary written forms are represented in word metadata. All 16 existing primary-component cards are substantively linked. 餅, 凄, 揉, 催, and 盛 have no matching card in the inspected kanji directory; their written metadata is nevertheless retained. No missing card or invented もみじ component reading is required.

**Reciprocity — CLEAN.** 燃/燃やす and 缶/薬缶 are reciprocal; existing 紅/紅葉 reciprocity remains intact.

**Mappings — CLEAN.** All twenty mappings agree with the assigned TSV rows and applicable families. In particular, source `2857870/もみじ` maple sense 1 is explicitly carried by `additionalSenses: 2857870:1,2`; preserved primary `1578780/こうよう` is not substituted for maple coverage. 燃す/もす restrictions and 盛る/もる identity are respected. Additional recognition is not treated as an independent N2 assignment.

## Findings:

**F85-01 — Minor; correctness, quiz ambiguity**

**Location:** `words\物凄い.md:9`; comparison `words\きつい.md:4,9,16–22`.

物凄い and きつい can still appear together despite overlapping intensity meanings. For 物凄い, the competing label **“tight; tough; intense”** contains a defensible answer, “intense.” This is lexical overlap, not merely a shared descriptive category.

**Minimal remedy:** Add `きつい` to 物凄い’s `quiz_exclusions`, or declare that single pair on the other card. Existing exclusions involving 激しい do not protect this pair: guards are nontransitive.

**Exact evidence:** Complete pinned `1502630:1` includes “tremendous,” “extreme”; complete `1003450:3` includes “strong,” “severe,” “intense,” and sense 5 includes “extreme,” “unusually strong.” The actual きつい body explicitly teaches intensity and strong smells/sunlight. Neither endpoint declares this pair. **Confidence: high.**

**F85-02 — Minor; correctness, quiz ambiguity**

**Location:** `words\揉む.md:9,47`; comparisons `words\訓練.md:4,9,16–20` and `words\指導.md:4,15–19`.

揉む expressly recognizes its training use, but lacks direct exclusions with **訓練** and **指導**. Their labels, “training; drill” and “guidance; instruction; coaching,” can be defensible answers for that ordinary secondary use. Different noun/verb presentation does not remove the underlying ambiguity.

**Minimal remedy:** Add `訓練` and `指導` to 揉む’s exclusions. No new N2 sense assignment or expansion of the lesson is necessary.

**Exact evidence:** Complete pinned `1567610:4` gives “to train,” “to coach.” The public **もむ** lexical entry, numbered differently, includes `相手になって教えてやる`. Complete `1247470:1` gives training/drill/practice, and `1309950:1` gives instruction/coaching. The actual older bodies teach `訓練する` as “train” and depict 指導 as coaching young athletes. 揉む’s list omits both; 訓練 excludes only 練習, and 指導 has no exclusion declaration. **Confidence: high.**

No excessive guard was established from the complete families and older bodies actually inspected; this is not certification of every declared edge.

## Optional:

None.

## Limits:

Git state, committed-blob identity, hashes, and rendering equivalence remain **independently unverified**; their supplied author-executed checks were not represented as reviewer checks. Preservation conclusions rely on the supplied patch/baseline and current file bodies.

Public evidence was read from the supplied captures, not freshly fetched. I did not inspect all author-read comparison families or older bodies, independently validate every kanji metadata field against original KANJIDIC XML, or run the app’s quiz builder. Beyond the inspected evidence, exhaustive missing/excessive-guard claims remain unverified. **CLEAN** means no actionable defect established in this actual scope—not exhaustive correctness or native-speaker certification.
