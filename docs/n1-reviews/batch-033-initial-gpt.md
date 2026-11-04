**Snapshot:** `fc5bf4d83fb551b1f616976a64d8106771f95857`, as identified by the frozen task; no uncommitted teaching changes reported. Git identity, worktree cleanliness and the baseline diff were not independently checked. Review was read-only.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), independent initial review of correctness, scoped coverage and textual phone comprehensibility for all of `kanji\豚.md`, `words\豚.md` and reused `words\豚肉.md`.

Read the specified instructions and format/level guidance through their supplied tails; the complete input-metadata JSON, including all four raw KANJIDIC2 elements; and both complete frozen JMdict packets. All XML lines returned in consecutive ranges of at most 200 lines: main packet **2,737 lines / 138 families**, comparison packet **682 lines / 22 families**, **160 total**, with counts independently confirmed by scoped search.

Read complete comparison cards `kanji\月.md`, `kanji\服.md`, `kanji\腹.md`, and `words\ぶうぶう.md`, `words\家畜.md`, `words\肉.md`, `words\牛肉.md`, `words\鶏肉.md`, `words\飼う.md`, `words\鳴く.md`. The complete earlier read of `words\豚肉.md` also covered its comparison role.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\豚.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\豚.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\豚肉.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded textual review, not exhaustive certification.

**Findings:** None.

The following checks support those verdicts:

- **Readings and metadata:** 豚 preserves KANJIDIC2’s complete Japanese reading lists and order, トン / ぶた, with 11 strokes, grade 8 and classical radical 152. The alternative Nelson radical does not invalidate the chosen classical index. `quizOnyomi: []` and `quizKunyomi: [ぶた]` correctly distinguish recognition from production. The selected ぶた has its own row and dictionary-supported linked examples.
- **Lexical identity and restrictions:** JMdict 1457390 supports pig, pork and the derogatory person sense. Its rare 豕 spelling adds no reading to 豚. Entry 2763370 separately recognizes とん; 1547210 supports 養豚 / ようとん. Entry 1457440 recognizes both ぶたにく and とんにく, without undermining the article’s selected ぶたにく. Entry 1201670 supports the rare 海豚 spelling, whole-word いるか reading and usually-kana qualification; no invented constituent reading is taught.
- **Teaching and navigation:** The examples, kana transcriptions, translations, 飼う attachment and ongoing-state explanation are appropriate. Native-first mixed 豚肉 is explained without misclassifying にく as kun. The new word has no inferred vocabulary level; reused 豚肉 retains explicit N5 metadata. Both required reciprocal pairs—豚 kanji/豚 word and 豚 kanji/豚肉 word—are present. The mnemonic is explicitly non-etymological, and the indexing radical is distinguished from the left outline.
- **Quiz choices:** 月 “moon, month,” 服 “clothing” and 腹 “belly” provide three distinct default wrong answers. Their inspected secondary meanings do not introduce pig/pork overlap. These comparison cards omit curation fields and therefore retain legacy full-reading exposure; that is not a defect caused by this batch.
- **Proposed exclusions:** Both direct guards are justified. 豚 can mean **pork**, overlapping 豚肉’s actual label. Digital Daijisen recognizes a child-language **pig** noun for ぶうぶう, despite its displayed “oinking; honking; grumbling” label. This warrants protection without claiming unrestricted interchangeability. JMdict’s car-only noun sense does not contradict the additional dictionary evidence. Neither guard implies a 豚肉/ぶうぶう exclusion. Broader livestock/meat categories and distinct beef/chicken ingredients do not require exclusions merely through category membership.

**Optional:** None.

**Limits:** The JMdict packets are frozen supplied evidence, not fresh upstream retrieval. Independent web fetches confirmed the actual 豚 dictionary headings/body and 養豚 heading/opening definition. Weblio’s simplified fetch omitted the definition; I therefore inspected the supplied raw HTML at lines 1762–1780, including the Digital Daijisen heading and noun sense 1. This is direct inspection of coordinator-supplied evidence, not independent retrieval or hash verification of that archive.

`docs\confusable-words.md` received scoped search only, not complete inventory inspection. Baseline preservation beyond the visible current metadata and supplied change description remains unverified.

All calls were serial; no parallel tools, delegation, edits or other reviewers’ reports were used. No internal repeated-range overlaps or truncations occurred in the XML reads. Other processes’ execution evidence was unavailable.

Comprehensibility verdicts concern text, not rendered Android or physical-phone behavior. Supplied cmap counts and inherited pilot acceptance were not independently verified; missing cmap entries do not establish glyph failure. Fresh batch-033 Android, combined-main, CI and immutable public-ZIP checks remain pending. Compatible-client requirements and outstanding physical-phone/general-release acceptance remain separate from bounded owner-testing eligibility.
