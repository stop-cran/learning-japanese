**Snapshot:** `296b6cc3bc9447def9a8fde835360d5a59bd9a39`, as identified by the frozen task; no uncommitted teaching included. Commit/worktree status was not independently verified with Git.

**Scope:** Independent initial read-only review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and textual comprehensibility of all 52 lines of `kanji\蚕.md` and all 38 lines of `words\蚕.md`.

Read all required instruction/format ranges, the complete input metadata—including the raw KANJIDIC2 element—and all four complete dictionary packets: 826/236/187/55 lines, respectively, comprising 48/6/9/1 families (**64 total**). XML reads used explicit ranges of at most 200 lines, with no missing or truncated returns.

Read all four complete comparison kanji cards (`天`, `春`, `蛍`, `繭`) and all eight complete comparison word articles (`虫`, `繭`, `桑`, `絹`, `糸`, `蛍`, `飼う`, `買う`). Searched `docs\confusable-words.md` for these terms and 蚕; no matches returned. Independently fetched and inspected the relevant Digital Daijisen and Seisenban bodies for [蚕](https://kotobank.jp/word/%E8%9A%95-457167) and [春蚕](https://kotobank.jp/word/%E6%98%A5%E8%9A%95-529877). No other reviews or author-rationale records consulted.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\蚕.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\蚕.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded scope, not exhaustive certification.

**Findings:** None.

The metadata preserves the exact sourced reading order, stroke count, grade and classical radical. Only `かいこ` is selected, with its own reading row and useful reciprocal word/kanji links. `サン` has a supported 養蚕 example; `テン` is explicitly unallocated lookup information rather than a guessed compound reading. Digital Daijisen’s `こ` entry explicitly illustrates 春ご, and its 春蚕 entries support both はるご and しゅんさん. The older standalone qualification is also supported by Seisenban.

The articles distinguish the reared larva, cocoon, pupa and silk material without denying the broader moth sense documented by Seisenban. Both Japanese examples, their kana transcriptions, translations and particle explanations are sound; 飼っています expresses ongoing animal keeping rather than purchasing. Kana/katakana spellings are correctly separated from lexical origin. The shape explanation is expressly a mnemonic, not etymology or phonetic allocation.

The three actual kanji distractor labels—“heaven, sky,” “spring season,” and “firefly”—are not defensible ordinary meanings of 蚕. The direct 蚕/虫 exclusion addresses the broader-category ambiguity; it does not imply a transitive exclusion with 蛍. The supporting word has no vocabulary level inferred from the N1 character.

**Optional:** None.

**Limits:** Dictionary packets were inspected as supplied frozen evidence, not freshly retrieved upstream JMdict. The confusable-word inventory received only the disclosed scoped search. A few historical quotation characters appeared as gaiji images in the web extraction; the relevant definitions and reading bodies were available, so no consequential teaching claim depended on those images. Empty 字通/other dictionary sections were not treated as verification.

This was textual review, not fresh native or physical-phone acceptance. The task’s unchanged-font cmap coverage was supplied context, not independently rerun; it does not establish rendering or comprehension on a device. Fresh batch-021 Android, combined-main, CI and public-ZIP checks remain pending; physical-phone/general-release acceptance remains outstanding. Larger quizzes, fallback algorithms and publication readiness were not certified.

All visible tool calls were issued individually and awaited; no visible tool-call overlap occurred. Internal execution/process overlap beyond the returned tool evidence was not observable. No files were modified.
