**Snapshot:** `4a76569419b95c0e5d1823e1c62320066e127459`, as identified by the task; committed teaching only, no uncommitted content included. Git identity was not independently checked under the permitted tools. Review remained read-only.

**Scope:** Independent initial review by GPT-6.1 Sol (`gpt-6.1-sol`). Read both teaching files completely: `kanji\鯉.md` (52 lines) and `words\鯉.md` (40 lines), assessing correctness, scoped coverage and textual phone comprehensibility.

Completed the prescribed instruction/reference ranges, complete input metadata including the raw KANJIDIC2 element, and all **29 dictionary families**: 18 main, 10 comparison and one supplement. XML reads returned every line in explicit ranges of at most 200 lines. Read all four comparison kanji (`魚`, `理`, `量`, `恋`) and all six comparison words (`魚`, `恋`, `池`, `泳ぐ`, `量`, `金魚`) completely. Independently fetched and inspected the relevant Kotobank dictionary bodies.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\鯉.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\鯉.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded scope, not exhaustive certification.

**Findings:** None.

Supporting conclusions:
- Metadata preserves both sourced Japanese readings and their order: リ and こい; 18 strokes, radical 195 and grade 9 agree with the raw element. The name-use explanation is supported by 普及版 字通’s 人名用漢字 heading.
- The selected こい reading has its own row and useful reciprocal word link. JMdict entry 1271650 supports 鯉／こい; its separate コイ reading is explicitly kana-only. Neither article mistakes katakana spelling for loanword origin.
- Entry 1914730 supports 養鯉／ようり and explicitly marks it rare. Recognition-only treatment and disabled on-reading questions are defensible; compound allocation was not inferred merely from a kana substring.
- Entries 1241360 and 1592910 support 錦鯉／にしきごい and 鯉のぼり／こいのぼり with the taught meanings. The voiced ごい explanation is appropriately bounded.
- The fetched **精選版 日本国語大辞典**, heading こいこひ【鯉】, sense ① explicitly describes a freshwater fish and cultivated varieties including ニシキゴイ. This verifies the freshwater and ornamental-variety claims—not merely the page’s outer リ heading.
- The pond and swimming examples, complete kana readings, translations and particle/form explanations are correct and natural. The modern-shape mnemonic is clearly separated from etymology.
- The three actual kanji distractor labels—“reason, logic,” “quantity; amount,” and “romantic love; longing”—do not overlap ordinary 鯉 meanings. Three curated choices cover the documented default four-choice configuration. The direct word exclusion with 魚 addresses the broader “fish” label; “goldfish,” “romantic love,” “pond,” “swim,” and “quantity; amount” introduce no demonstrated ambiguity with “carp.”

**Optional:** None.

**Limits:** The dictionary packets are frozen supplied evidence, not fresh upstream JMdict retrieval. The targeted search of `docs\confusable-words.md` found no applicable matches; this was not a complete inventory review. Kotobank’s Daijisen section had no extracted body; verification instead used the relevant Seisenban body. Historical gaiji in 字通 were not resolved and are unnecessary for the bounded teaching claims.

Comprehensibility assessment was textual, not fresh Android or physical-phone acceptance. The stated bundled-font coverage is inherited task context, not independently checked here. Fresh batch-022 Android, combined-main, CI, public-ZIP and physical-phone/general-release acceptance remain outside this review.

Each tool invocation was issued individually and awaited; no tool-call overlap was observed. Internal backend execution and unavailable process records were not inspected. No other reviews or author-rationale records were read, and no files were changed.
