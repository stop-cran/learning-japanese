**Snapshot:** Supplied frozen snapshot `a532c4d436726e6eeb46ff78cc3dc1a039d6f19e`; no uncommitted teaching included by the task’s declaration. Git identity, signature and worktree cleanliness were not independently verified under the permitted tools. Review was read-only.

**Scope:** One reviewer, GPT-6.1 Sol (`gpt-6.1-sol`), reviewing complete `kanji\丞.md` and `words\丞相.md` for correctness, scoped coverage and textual comprehensibility.

Read all assigned ranges completely: three frozen JMdict files containing all **14 complete entry families**; seven comparison kanji articles (`蒸`, `乗`, `水`, `助`, `承`, `相`, `臣`); six comparison word articles (`大臣`, `首相`, `総理大臣`, `助ける`, `救う`, `役人`); repository review/structure guidance, content-format lines 1–180 and JLPT-policy lines 1–32; all 14 lines of raw character JSON; both archived HTML ranges 1750–1810, including their exact Digital Daijisen headings and sense boundaries; and the complete 66-line pinned SVG. Also inspected scoped confusable-word guidance, actual metadata for all twelve specified legacy fallback cards, and article existence for `宰相`/`補佐`.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\丞.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\丞相.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded review, not exhaustive correctness.

**Findings:** None.

Supporting determinations:

- **Character metadata and practice:** The raw KANJIDIC2 record supports six strokes, classical radical 1 (`一`), grade 9, ordered on readings `[ジョウ, ショウ]` and ordered kun readings `[すく.う, たす.ける]`. All remain intact. Practice selects only `[ジョウ]`, yielding `じょう`, and disables kun questions with `[]`. Its own reading row links the actual `丞相` article. Daijisen’s character heading **じょう【丞】** and compound heading **じょう‐しょう【丞相】** support the selected allocation; the older whole-word `しょうじょう` is correctly not treated as allocation evidence.
- **Source-only readings and shape:** The kun rows distinguish character metadata from verified lexical spellings. Neither `救う` nor `助ける` is presented as an example written with 丞; the complete supplied families establish no such spelling. The text neither invents `丞う`/`丞ける` nor claims universal nonexistence. The mnemonic is explicitly modern-shape guidance. The SVG contains six numbered paths, with the bottom horizontal identified as 一; its grouping is not used to establish etymology.
- **Historical meanings and example:** JMdict 1885990 and archived Daijisen separately support the ancient Chinese chancellorship and Japanese Chinese-style ministerial title. The teaching does not equate these with modern cabinets or with standalone 丞’s separate third-rank office sense. 唐名 sense 1 supports the office-title explanation; sense 2’s `からな` restriction and archaic alias meaning do not apply. The generic example, complete kana and English translation agree and naturally describe the sourced role without inventing a named event or asserting identical duties across every period.
- **Component explanation:** Daijisen’s explicit statement that 丞 and 相 both mean helping supports the related-meaning explanation. The article correctly rejects “mutual” as the explanation of 相 here.
- **Support and navigation:** One support article supplies the selected reciprocal pair, `丞 ↔ 丞相`, with both directed links present. The substantive 相 component link resolves to its existing card. No additional support article or baseline reciprocal-pair activation is needed within the assigned scope. Neither `宰相.md` nor `補佐.md` exists in the checked word directory; neither is falsely linked. No vocabulary JLPT level is inferred from 丞’s N1 label.
- **Quiz labels:** 蒸’s “steam; sultry heat,” 乗’s “ride; board,” and 水’s “water” are defensibly wrong for 丞. Actual 助 metadata confirms assistance overlap, and 助 is appropriately absent from this distractor list. The twelve specified legacy cards each have two curated distractors; adding 丞’s assistance label introduces no established ambiguity with their inspected target meanings. The three direct exclusions connecting 丞相 to 大臣, 首相 and 総理大臣 conservatively protect overlapping minister/chancellor interpretations. They do not imply unrestricted synonymy or a transitive exclusion clique. The scoped confusable-word search found no matching inventory entries.

**Optional:** None.

**Limits:** Dictionary XML, raw character records, archived Daijisen sections and SVG were supplied evidence, not fresh internet retrievals. No web lookups failed or returned irrelevant evidence because none were attempted. No requested read was left truncated or incomplete. This review remained blind to author rationale and other reports.

The fallback check does not certify every larger, random or live quiz pool, unchanged baseline bytes, or current application behavior. No validation commands or app execution were performed. Font-cmap coverage of the nineteen authored Han characters is task-supplied information, not independently inspected visual evidence. Textual comprehensibility does not certify glyph rendering, drawing interaction or physical-phone usability. Compatible Android `f9b59a2+` is required; native, physical-phone and general-release acceptance remain outstanding, without constituting a blanket veto on bounded owner testing.

All tool calls in this review were issued singly and awaited; no parallel tools, shell commands, delegation, edits, commits or issues were used.
