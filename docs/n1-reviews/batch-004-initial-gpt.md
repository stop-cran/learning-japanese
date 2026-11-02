**Snapshot:** `bfea5052387e2327dac4e365ec11ccca1289b914`, base `c7b7bdcfb509b13b119fa8a85fdd2adb0878775d`; committed teaching only, as identified by the supplied task. Added evidence-only input: `docs\n1-reviews\batch-004-input-metadata.json`. No uncommitted teaching was intentionally included. Git identity and worktree cleanliness were not independently verified because commands were prohibited.

**Scope:** Independent read-only review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and textual phone comprehensibility. No edits, commands, delegation, publication or other reviewers’ reports/progress records were used.

Complete reads:
- All seven teaching files: `kanji\杉.md`, `kanji\桐.md`, `kanji\柳.md`, `words\桐.md`, `words\柳.md`, `words\川柳.md`, `words\杉.md`. The reused 杉 word article received complete contextual reading but verdicts concern its changed backlink passage and integration—not exhaustive recertification of unchanged content.
- Both frozen JMdict packets, all 23 families: `batch-004-jmdict.xml`, requested ranges 1–240, 241–280 and 281–340 through EOF; `batch-004-comparisons-jmdict.xml`, ranges 1–240 and 241–420 through EOF.
- Complete evidence-only metadata JSON, requested range 1–260 through EOF.
- Actual distractor cards: `kanji\形.md`, `村.md`, `羽.md`, `同.md`, `相.md`, `卵.md`, `印.md`.
- Actual comparison articles: `words\木.md`, `植物.md`, `植える.md`, `詩.md`, `句.md`, `俳句.md`, `茶.md`, `お茶.md`, `材木.md`, `木材.md`, `材料.md`, `植木.md`; also `kanji\川.md`.

Additional reads: `docs\content-format.md` lines 40–157; README heading search and lines 526–540. Live Kotobank extracts were inspected for 桐, 桐人, 桐油 and 柳. For 川柳, the oversized fetch was read from its generated tool-output file, lines 1–150, including the relevant 精選版 日本国語大辞典 headings and complete Nipponica 川柳（短詩） section. The remaining page tail was not read. No required local teaching or frozen dictionary packet was truncated or omitted.

**Verdicts:**

| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\杉.md` | CLEAN | CLEAN | CLEAN |
| `kanji\桐.md` | CLEAN | CLEAN | CLEAN |
| `kanji\柳.md` | CLEAN | CLEAN | CLEAN |
| `words\桐.md` | CLEAN | CLEAN | CLEAN |
| `words\柳.md` | CLEAN | CLEAN | CLEAN |
| `words\川柳.md` | CLEAN | CLEAN | CLEAN |
| `words\杉.md` — changed-passage integration | CLEAN | CLEAN | CLEAN |

**Findings:** None established within the assigned scope.

Supporting assessment:

- **Metadata and every reading:** Full raw on/kun lists and order match the supplied complete KANJIDIC2 records: 杉 `[サン] / [すぎ]`; 桐 `[トウ, ドウ] / [きり]`; 柳 `[リュウ] / [やなぎ]`. Stroke counts, grades and radical numbers also match. Each reading has its own table row. 杉 サン is explicitly qualified as source-only rather than furnished with a manufactured example. 桐 トウ is supported by JMdict 1240720, sense 1, 桐油 とうゆ; ドウ by the inspected 字通 **桐人【どうじん】** heading and its paulownia-figure definition. Its classical qualification and exclusion from questions are appropriate.

- **Actual offered reading-key suitability:** The offered keys are 杉 kun **すぎ**, 桐 kun **きり**, and 柳 on **りゅう** / kun **やなぎ**; 杉 and 桐 offer no on questions. Each selected entry has its own row and a relative linked word example. JMdict 1373520, 1240710 and 1538490 support the standalone native readings. 柳 リュウ is genuinely allocated in lexicalized 川柳 せんりゅう, not inferred merely from a kana substring: the inspected 川 card supplies セン, and the verse article explains both allocation and pen-name origin. JMdict 1390110 supports the complete verse word. These are useful recognition prompts; the astronomical standalone 柳 りゅう is not improperly substituted as the ordinary tree noun. All selections are exact raw-string subsets, with no separator or three-key-cap complication.

- **Lexical restrictions and claims:** 柳 correctly preserves the 楊柳-only restriction on ようりゅう and the reading restrictions on the weeping-willow sense in JMdict 1538490. 川柳 distinguishes verse family 1390110 from tree/tea family 1811520 and archaic tree family 2693770. The inspected public headings independently support the distinctions. 桐油’s source plants are supported by the inspected **きりあぶら** heading; the botanical contrast with 梧桐 agrees with family 1586170. The senryu form, subject matter and name origin agree with the inspected **せんりゅう** and Nipponica **川柳（短詩）** sections. Mnemonics are explicitly separated from etymology. New word articles do not infer vocabulary JLPT levels.

- **Meaning choices and exclusions:** All three new kanji have three inspected, defensibly wrong meaning distractors. Shape/form, village and feather/wing/counter do not supply ordinary cedar meanings; same/equal, mutual/aspect/minister and village do not supply paulownia meanings; egg/ovum, stamp/mark and mutual/aspect/minister do not supply willow meanings. Word exclusions directly cover the relevant broad tree/plant labels and 川柳’s poetry, willow and tea collisions; they do not depend on transitivity. Material and garden-plant comparisons do not establish another required pair merely because a particular tree can supply timber or grow in a garden.

- **Navigation and presentation:** Reciprocal selected-support links are present for 杉↔杉, 桐↔桐, 柳↔柳 and 柳↔川柳, including the reused 杉 backlink. Explanations stand alone, examples have kana and English translations, and rare or alternative readings are subordinate to practical recognition. No actionable example, translation or register defect was established.

**Optional:** None.

**Limits:** Frozen dictionary packets and metadata were supplied evidence, not independently downloaded or hash-verified upstream archives. Live dictionary inspection verified the identified headings, not every linked entry or historical citation; 字通’s classical quotation includes image-rendered characters. App transport and projection behavior were assessed against the supplied compatibility contract, not executed. No native archive/import/routes/drawing, actual font rendering, physical-phone acceptance, native-speaker review or measured-learning certification is claimed. CLEAN means no actionable defect established within this bounded review, not exhaustive correctness.
