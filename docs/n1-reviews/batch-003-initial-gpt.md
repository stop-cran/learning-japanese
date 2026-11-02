**Snapshot:** `6ce567650e6663d712bac25bebd5bead0d0af655`; base `fd75a6730bfd863202df1f4782ace9eb433f0e05`. Committed teaching only; no uncommitted teaching included. Added evidence-only input: `docs\n1-reviews\batch-003-input-metadata.json`. Snapshot identity and frozen status are supplied, not independently Git-verified.

**Scope:** Independent read-only review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and textual phone comprehensibility. No edits, commands, delegation or other reviewers’ reports/progress records were accessed.

Complete reads:
- Assigned teaching: `kanji\苗.md:1–51`, `kanji\畔.md:1–49`, `kanji\畝.md:1–51`; `words\苗.md:1–38`, `words\育苗.md:1–38`, `words\苗代.md:1–38`, `words\畔.md:1–40`, `words\湖畔.md:1–38`, `words\畝.md:1–39`, `words\名字.md:1–46`. 名字’s verdict concerns changed-passage integration, not fresh exhaustive certification of unchanged content.
- Frozen evidence: `docs\n1-sources\batch-003-jmdict.xml:1–393`, `docs\n1-sources\batch-003-comparisons-jmdict.xml:1–559`, and input metadata `1–37`, including its complete embedded character records.
- Required distractors: `kanji\猫.md:1–47`, `留.md:1–50`, `畜.md:1–40`, `半.md:1–41`, `判.md:1–46`, `久.md:1–45`.
- Existing comparisons under `words\`: `芽.md:1–43`, `植物.md:1–49`, `木.md:1–34`, `育てる.md:1–33`, `育つ.md:1–50`, `種.md:1–37`, `田.md:1–43`, `田んぼ.md:1–48`, `田植え.md:1–51`, `畑.md:1–34`, `道.md:1–31`, `湖.md:1–33`, `岸.md:1–35`, `陸.md:1–35`, `端.md:1–35`, `縁.md:1–43`.
- Additional title-search candidates: `words\植木.md:1–47`, `稲.md:1–34`, `植える.md:1–34`, `生長.md:1–47`, `海岸.md:1–34`.
- Contract: `docs\content-format.md:40–157`. Narrow searches also inspected matching titles throughout `words\`, relevant matching lines/context in `docs\confusable-words.md`, and audience/approach-related matching snippets in `README.md`; those documentation files were not read completely.

Live evidence inspected through all seven supplied Kotobank URLs: 苗’s Nipponica cultivation account; 苗代’s Seisenban entry; 代’s Daijisen **しろ**, sense 5; 畔’s Seisenban **あぜ**, **くろ** and regional-distribution discussion; 畝’s separate **うね／せ／ほ** entries and Nipponica **せ**; 湖畔’s geographical **こ‐はん** entry; and 育苗’s substantive encyclopedia text. The 代 fetch exceeded tool-display size; its relevant heading and senses were recovered from saved output, lines 1–45. No assigned teaching or frozen-packet read remained truncated.

**Verdicts:**

| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\苗.md` | CLEAN | CLEAN | CLEAN |
| `kanji\畔.md` | CLEAN | CLEAN | CLEAN |
| `kanji\畝.md` | CLEAN | CLEAN | CLEAN |
| `words\苗.md` | NEEDS FIX | NEEDS FIX | CLEAN |
| `words\育苗.md` | CLEAN | CLEAN | CLEAN |
| `words\苗代.md` | CLEAN | CLEAN | CLEAN |
| `words\畔.md` | CLEAN | CLEAN | CLEAN |
| `words\湖畔.md` | CLEAN | CLEAN | CLEAN |
| `words\畝.md` | CLEAN | CLEAN | CLEAN |
| `words\名字.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no actionable defect established within this bounded scope.

**Findings:**

**F1 — Minor; correctness/scoped coverage; `words\苗.md:8`, with meaning at lines 4 and 15.**  
The exclusions `[芽, 植物, 木]` leave an ambiguous displayed-label pair with `words\植える.md:4`, whose title is simply **“plant.”** For a question displaying 苗, both **“seedling; young plant”** and the unqualified noun reading of **“plant”** are defensible English answers. The learner cannot recover 植える’s intended verbal interpretation from that English label alone.

**Impact:** The authored pool permits an ambiguous meaning question; this is a missing quiz safeguard, not an incorrect definition or Japanese example.

**Remedy:** Add the direct exclusion `苗`/`植える`, preferably by adding `植える` to 苗’s existing list. The existing edges 苗/植物 and 植物/植える do not exclude 苗/植える.

**Evidence:** Frozen JMdict family **1490470, sense 1** explicitly defines 苗 as “seedling; young plant.” Actual inspected labels are `words\苗.md:4` and `words\植える.md:4`. `words\植物.md:9` already excludes 植える for the corresponding noun/verb-label collision. The direct-pair and displayed-label requirements are explicit in `docs\content-format.md:135–145`. This finding concerns eligibility under the documented builder contract, not an observed generated question.

**Confidence:** High.

**Actual reading-key suitability assessment:** All selected values are exact raw-string subsets, with full source lists and order preserved.

| Kanji | Offered projected keys | Assessment |
|---|---|---|
| 苗 | on: `びょう`, `みょう`; kun: `なえ`, `なわ` | Suitable. 育苗, 苗字, 苗 and 苗代 provide correctly allocated support. `なわ` is explicitly taught as the bound form `なわ-`, not an independent noun. |
| 畔 | on: `はん`; kun: `あぜ` | Suitable through 湖畔 and 畔. Regional `くろ` and rare-written `ほとり` remain explained but unselected. |
| 畝 | on: none; kun: `うね` | Suitable through 畝. Disabling on questions avoids unsupported ordinary prompts; `せ` remains explained as the separate traditional unit. |

Every selected reading has its own table row and relative linked word example. All on/kun metadata entries are accounted for, including 畝’s explicitly qualified source-only ボウ／モ／ム. The inspected Nipponica heading independently supports the limited ボウ statement. No manufactured examples are needed.

All nine authored kanji distractor slots provide defensibly wrong meaning choices after considering the actual cards and ordinary senses. Reciprocal kanji/support navigation is present for every selected support article, including the reused 名字 article’s 苗字 passage. The planting-ridge/boundary distinction, rice-specific nursery meaning, rare spellings, and separate Japanese/Chinese area units are appropriately explained.

**Optional:** None.

**Limits:** Frozen dictionary families and provenance were supplied evidence, not independently retrieved or hash-verified upstream archives. Live retrieval verified the consequential supplementary claims identified above; dictionary inclusion was not treated as proof of commonness. Examples received textual linguistic assessment, not native-speaker certification. No app execution, archive import, route/drawing/font inspection, physical-phone acceptance or measured-learning assessment was performed. No consequential linguistic claim remains unresolved within the reviewed scope.
