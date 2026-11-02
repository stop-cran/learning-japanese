**Snapshot:** `8602dc702dccc11de5fbcccace4ba204fafb930e`; base `45d973442c19e0a0b73e9fe7fece453fdb066536`. Reviewed the designated frozen committed teaching, with no uncommitted teaching included. Additional evidence-only input: `docs\n1-reviews\batch-006-input-metadata.json`, outside that snapshot. Snapshot identity and upstream hashes were supplied, not independently recomputed.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), independently assessing correctness, scoped coverage and textual phone comprehensibility. Read-only throughout; no commands, edits, delegation, other review reports or author progress records.

Actual file reads:
- **Complete, L1–EOF**, requested L1–240: `kanji\栗.md`, `kanji\梨.md`, `words\栗.md`, `words\梨.md`.
- **Complete dictionary packets:** `docs\n1-sources\batch-006-jmdict.xml` (requested L1–240); `batch-006-comparisons-jmdict.xml` (L1–260 and L261–360, through EOF); `batch-006-supplement-jmdict.xml` and `batch-006-notes-jmdict.xml` (requested L1–240 each). All 18 supplied families were read.
- **Complete evidence input**, requested L1–260: `docs\n1-reviews\batch-006-input-metadata.json`, including both complete embedded character records and projected keys.
- **Complete kanji comparisons**, requested L1–240 each: `kanji\西.md`, `要.md`, `相.md`, `利.md`, `村.md`, `木.md`, `園.md`.
- **Complete word comparisons**, requested L1–240 each: `words\木.md`, `植物.md`, `植える.md`, `果物.md`, `果実.md`, `実.md`, `木材.md`, `材木.md`, `茶色.md`, `茶色い.md`, `植木.md`, `大木.md`, `桃.md`, `無し.md`.
- Supporting instructions: complete task prompt; `docs\content-format.md` L40–157; `README.md` L526–EOF (requested through L560). Heading-only search of README; targeted search of `docs\confusable-words.md` returned no matches and was not a full read.

Independently fetched the four linked Kotobank pages and inspected the relevant dictionary headings described below. No required local read was truncated.

**Verdicts:**

| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\栗.md` | CLEAN | CLEAN | CLEAN |
| `kanji\梨.md` | CLEAN | CLEAN | CLEAN |
| `words\栗.md` | CLEAN | CLEAN | CLEAN |
| `words\梨.md` | CLEAN | CLEAN | CLEAN |

**Findings:** None established within the assigned scope.

Supporting assessment:

- **Metadata and reading coverage:** 栗 preserves on readings `[リツ, リ]` and kun readings `[くり, おののく]`; 梨 preserves `[リ]` and `[なし]`, respectively, exactly and in source order. Every entry has its own explanatory reading-table row. Stroke counts, classical radical numbers and grade tags match the supplied KANJIDIC2 records. Neither word receives an inferred vocabulary JLPT level. Modern-shape associations are explicitly distinguished from etymology.
- **Actual reading-key suitability:** The offered keys are **栗 → くり** and **梨 → なし**, with no on-reading questions. Both are useful, unambiguous standalone native nouns, supported by their own relative-linked word articles and JMdict families **1246880** and **1549860**. Allocation is to the entire single-character noun, not inferred from a kana substring. Neither selection introduces stem-folding, separator or three-key-cap complications. Both kanji/word support pairs link reciprocally.
- **Unselected readings:** 栗’s リツ, リ and おののく remain explicitly source-only rather than being presented as modern chestnut pronunciations. JMdict **1390130** supports the separate usually-kana trembling verb with spellings 戦く／慄く, not a modern 栗 spelling; the card accurately preserves that distinction. 梨’s リ is supported by 梨園 **1549880**, the live Daijisen character heading **り【梨】［漢字項目］**, and Seisenban **り‐えん【梨園】**. Retaining that recognition example without offering an on-reading question is appropriate.
- **Selected senses and qualifications:** Live Seisenban **くり【栗】**, senses **①–③**, supports tree/nut, timber and colour abbreviation; sense ① also mentions other cultivated chestnuts. Live Daijisen and Seisenban **くり‐いろ【栗色】** support the shell-colour explanation. Live Seisenban **なし【梨・梨子】**, **[1]①**, explicitly allows broader reference including European pears and wild species. Seisenban **り‐えん【梨園】**, sense **②**, supports the theatrical-world gloss and particular kabuki association. The articles do not turn these recognitions into unrestricted substitution or frequency claims.
- **Quiz choices and exclusions:** 栗’s displayed distractors—“west,” “necessity; essentials,” and “mutual; aspect”—and 梨’s—“benefit; advantage,” “village,” and “mutual; aspect”—are defensibly wrong, including consideration of ordinary secondary meanings. 栗 directly excludes all ten listed overlapping tree/plant/fruit/material/colour comparisons; 梨 directly excludes its six tree/plant/fruit comparisons. These do not depend on transitivity. 植木 and 大木 add cultivation or size conditions not inherent in either noun; 桃 names another species; 無し has a distinct meaning despite the shared pronunciation. No additional exclusion was established.
- **Learner-facing text:** The four Japanese sentence examples are natural and correctly translated. Kana support, tree-versus-fruit expressions, usually-kana qualifications, the rare 梨子 spelling and the 梨／無し contrast are clear. The explanations remain standalone and practically prioritized.

**Optional:** None.

**Limits:** The frozen XML packets and KANJIDIC2 records are supplied evidence, not my own upstream retrieval. Public checks were fresh simplified-page fetches: the relevant Seisenban entries, 梨’s Daijisen character heading and both 栗色 definitions were available. Daijisen definition bodies for 栗 and 梨園 were absent from those extractions; the inspected Seisenban entries supplied the necessary evidence instead. No essential consequential claim remains unverified within this bounded review.

No app execution, archive import, route/drawing verification, physical-phone/font acceptance, native-speaker review or measured-learning certification was performed. Curation requires the stipulated compatible app; older APKs can still ask the full metadata readings. CLEAN means no actionable defect established here, not exhaustive correctness.
