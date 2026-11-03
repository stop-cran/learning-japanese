**Snapshot:** `09e480adadc433f54cdbe20e3691ab38126bb711`; committed teaching only, with no uncommitted teaching changes included, as identified by the task. Git state was not independently verified.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), independent read-only initial review. Reviewed all four teaching files completely for correctness, scoped coverage and textual comprehensibility, including examples/translations, metadata, reading allocation, curation, labels, exclusions, links, botanical distinctions and mnemonics.

Complete evidence reads: batch-009 input metadata; all 44 lexical families in `batch-009-jmdict.xml` and all 22 comparison families in `batch-009-comparisons-jmdict.xml`, including restrictions, flags and every sense. Complete comparison reads: kanji 古・村・相・子・木・口・下・梅; words 梅・桃・木・植物・植える・植木・果物・果実・実. Read both instruction files, the requested format/level-policy ranges, README Approach and the entire confusable-word inventory. Independently inspected the five suggested Kotobank pages plus the 杏 and 杏子 pages.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\杏.md` | **NEEDS FIX** | **CLEAN** | **CLEAN** |
| `kanji\李.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\杏.md` | **NEEDS FIX** | **CLEAN** | **CLEAN** |
| `words\李.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded scope, not exhaustive certification.

**Findings:**

1. **Minor; correctness—lexical classification; `kanji\杏.md:43`, `words\杏.md:5,7`.** Calling あんず a “native noun” and classifying it unqualifiedly as `wago` conflates its modern kun-reading treatment with its lexical origin. Learners could infer that a dictionary kun reading necessarily identifies a Japanese-origin word.

   **Remedy:** Replace “native noun” with “standalone plant noun.” Briefly distinguish the established reading from the word’s Chinese-derived origin, and align the word type/tag accordingly—or explain an explicitly reading-based repository convention. Preserve KANJIDIC2’s あんず kunyomi and its quiz selection. The existing warning against freely extracting ず from 子 remains useful.

   **Evidence:** [Seisenban Nihon Kokugo Daijiten, あん‐ず【杏子・杏】](https://kotobank.jp/word/%E6%9D%8F%E5%AD%90-429332) explicitly identifies あん and す as the 唐宋音 of 杏 and 子. [Nipponica, アンズ](https://kotobank.jp/word/%E3%81%82%E3%82%93%E3%81%9A-1730201) likewise identifies アンズ as 杏子の唐音. Independently, [字通, 杏](https://kotobank.jp/word/%E6%9D%8F-429037) lists あんず under 字訓 while explaining the Chinese-derived word—directly demonstrating that these are different linguistic layers.

   **Confidence:** High for the origin/native-word distinction; moderate for the precise metadata replacement because the supplied format does not explicitly settle this historical-loan classification edge case.

No other actionable defect was established. All six sourced readings retain their original order. The selected あんず and すもも each have direct dictionary-supported allocation and reciprocal support-article links. キョウ・アン・リ have independently supported recognition examples; コウ is appropriately qualified as source-only without claiming nonexistence. Botanical qualifications and all four sentence translations are sound. Both new word cards directly guard all eight assigned overlapping comparison labels; no botanical exclusion clique is needed.

**Optional:** None.

**Limits:** All mandatory teaching, metadata, XML and comparison reads completed without truncation. The XML packets are supplied frozen evidence, not fresh upstream retrieval or independently verified source hashes. Live extraction exposed the relevant dictionary/encyclopedia headings and passages; several other sections returned headings only, and those were not treated as verification.

The confusable-word inventory was read completely, but comparisons were bounded to the assigned articles—not a whole-deck ambiguity audit. Larger-quiz fallback safety was not exhaustively certified. README search output was truncated; its Approach section was subsequently read completely. No other reviewer reports or restricted batch records were opened.

One tool call was issued per response, awaiting each result; no internal tool overlap was observed. No edits, shell commands, delegation, commits or issues occurred. Review was textual only: no native-speaker acceptance, physical-phone execution, measured readability, frequency or learning-effectiveness certification.
