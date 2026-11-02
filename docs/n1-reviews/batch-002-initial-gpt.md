**Snapshot:** `9fee5174f695d5cbc1a45752e633c9622b011e38`, base `560c9dd37103852ef8ddf07cd3b740a975243de1`; committed teaching only, no uncommitted teaching included. Added evidence-only input: `docs\n1-reviews\batch-002-input-metadata.json`, outside the frozen teaching snapshot.

**Scope:** Independent textual review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and phone comprehensibility.

Read completely, without truncation:
- All nine assigned teaching files: `kanji\{稲,穂,桑,芋}.md` and `words\{稲穂,水稲,桑,芋,稲}.md`. For reused `words\稲.md`, the verdict concerns changed-link integration, informed by its complete surrounding text—not fresh exhaustive certification of unchanged content.
- All three frozen packets: `batch-002-jmdict.xml` (lines 1–260, then 261–EOF), `batch-002-comparisons-jmdict.xml` and `batch-002-quiz-jmdict.xml` (both complete), under `docs\n1-sources\`; all 19 selected families.
- Complete `docs\n1-reviews\batch-002-input-metadata.json`, including all four raw character records and projected keys.
- Required distractor cards: `kanji\{移,秒,秋,積,想,息,森,友,茶,宇,干,字}.md`.
- Comparison/candidate articles: `words\{米,ご飯,木,くだらない,屑,塵,無駄,紙屑,穀物,粒}.md`.
- `docs\content-format.md`, lines 40–157.

Additional searches were limited to potentially overlapping English titles under `words\*.md`. No other reports, progress ledgers, execution records, adjudication or review rationale were read. No commands, edits, delegation or publication were performed.

**Verdicts:**

| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\稲.md` | CLEAN | CLEAN | CLEAN |
| `kanji\穂.md` | CLEAN | CLEAN | CLEAN |
| `kanji\桑.md` | CLEAN | CLEAN | CLEAN |
| `kanji\芋.md` | CLEAN | CLEAN | CLEAN |
| `words\稲穂.md` | CLEAN | CLEAN | CLEAN |
| `words\水稲.md` | CLEAN | CLEAN | CLEAN |
| `words\桑.md` | CLEAN | CLEAN | CLEAN |
| `words\芋.md` | CLEAN | CLEAN | CLEAN |
| `words\稲.md` — changed-link integration | CLEAN | CLEAN | CLEAN |

**Findings:** None established within the assigned scope.

The complete on/kun metadata lists and their order match the supplied KANJIDIC2 records: 稲 `[トウ, テ]` / `[いね, いな-]`; 穂 `[スイ]` / `[ほ]`; 桑 `[ソウ]` / `[くわ]`; 芋 `[ウ]` / `[いも]`. Every entry has a reading-table row. テ is explicitly source-only, without a manufactured example. Nonselected スイ, ソウ and ウ have appropriately bounded examples supported by JMdict families 1779070 (出穂), 1247070 (桑園) and 1772660 (海芋). Strokes, classical radicals and grade metadata also agree with the supplied records.

**Actual reading-key suitability:** The offered keys are suitable for this bounded recognition packet:
- 稲: `とう` through 水稲; `いね` through 稲; `いな` through the explicitly bound いな- in 稲穂.
- 穂: `ほ` through 稲穂.
- 桑: `くわ` through 桑.
- 芋: `いも` through 芋.

Each selected raw value is an exact metadata subset entry with its own table row and relative linked example. Allocation is defensible by character: 水＝スイ / 稲＝トウ and 稲＝いな- / 穂＝ほ, not merely matching kana substrings. The projected `いな` key remains useful because the article explains its bound status; it is not presented as an independent noun. The selections stay below the per-kind cap. Disabling the other on-reading questions does not create a coverage defect.

All four new kanji have three defensibly wrong displayed meaning choices. In particular, 穂’s documented tip, crest and scion senses do not make “pile up,” “thought; conception,” or “breath” correct alternatives.

The word articles preserve the supported plant/part/grain/food distinctions, qualify agricultural and usually-kana vocabulary appropriately, and do not infer new word JLPT levels. 芋’s derogatory and dismissive senses are acknowledged rather than hidden behind its food title. Its direct exclusions with くだらない and 屑 address plausible evaluative overlap; the inspected evidence does not establish a necessary additional 芋–塵 pair merely through 屑. No additional actionable title ambiguity was established in the inspected candidates.

Reciprocal navigation is present for every selected support relationship, including reused 稲. The changed introduction link in `words\稲.md` targets the new character card without changing the noun’s explanation. Mnemonics are clearly separated from history. Examples, translations, selective kana and contrasts are adequate for standalone textual use.

**Optional:** None.

**Limits:** Snapshot identity, frozen status and source provenance were supplied; I did not independently verify Git state or recompute hashes. Dictionary evidence was inspected from the complete coordinator-supplied packets, not retrieved live. Dictionary inclusion was not treated as proof of commonness. Additional comparison articles received only the bounded checks relevant here, not exhaustive historical/N2 review.

No consequential unresolved textual claim was identified. CLEAN means no actionable defect established within this scope, not exhaustive correctness. This report does not certify native app execution, archive import, routes/drawing, actual fonts, physical-phone acceptance, native-speaker review or measured learning effectiveness.
