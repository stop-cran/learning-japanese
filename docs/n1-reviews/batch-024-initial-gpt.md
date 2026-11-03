**Snapshot:** `9281b9c2b8a6d2c87480514533037c30a5d20602`, identified by the supplied frozen task; no uncommitted teaching included. Git state was not independently checked. Review was read-only.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`); correctness, scoped coverage and textual phone comprehensibility of the complete `kanji\鯛.md` (51 lines) and `words\鯛.md` (42 lines).

Read all assigned instruction/format/source-policy ranges, the complete input metadata—including the raw KANJIDIC2 element—and both complete JMdict packets: **71 target families plus 10 comparison families, 81 total**. XML reads covered lines 1–1367 and 1–340 in serial, explicit ranges of at most 200 lines; no returned range was truncated. Read all six assigned comparison kanji and all six comparison words completely. Scoped `docs\confusable-words.md` search found no matching fish/sea/cooking entries; the full inventory was not inspected.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\鯛.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\鯛.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded review, not exhaustive certification.

**Findings:** None.

The full Japanese reading lists preserve sourced **チョウ** and **たい** and their order. Selecting only **たい** is defensible: its individual row links to the verified standalone fish noun, while チョウ is explicitly source-only rather than declared nonexistent. The reciprocal 鯛 kanji/word links are present. Stroke count, classical radical and grade metadata agree with the supplied character element; the name-use grade explanation and explicitly nonhistorical mnemonic avoid misleading classification claims.

The fish definition, kana spellings, 真鯛／まだい, 金目鯛／きんめだい and たい焼き・鯛焼き／たいやき match their applicable dictionary entries and restrictions. The articles do not promote search-only spellings, confuse idiomatic English glosses with animal identities, or generalize compound voicing into an alternative standalone reading.

Both example sentences, kana readings, translations and particle explanations are sound. “Grilled” is a fitting contextual translation of 焼いて, not presented as its exclusive meaning. The supporting word has no vocabulary level inferred from the N1 kanji.

The three actual kanji distractor labels—“circumference; circuit,” “investigate; tune,” and “week”—are semantically distinct from “sea bream,” including the inspected secondary meanings. The direct word exclusion 鯛／魚 appropriately handles the broader fish label; carp and ayu remain different animals, with no transitive exclusion assumption.

**Optional:** None.

**Limits:** The dictionary packets are frozen supplied evidence, not fresh upstream retrieval. The supplied Kotobank facts support Daijisen’s fish definition and Jitsu’s readings; their original archived HTML and hash were not independently inspected. An independent fetch of the canonical [鯛 entry](https://kotobank.jp/word/%E9%AF%9B-556223) returned and confirmed Seisenban’s marine-fish definition, particular reference to マダイ and food use. Its simplified extraction omitted Daijisen and Jitsu bodies, so those details remain supplied rather than independently retrieved evidence.

Comprehensibility was assessed textually, not on a physical phone. Supplied unchanged-font cmap coverage is not native rendering certification. Fresh batch-024 Android, combined-main, CI, immutable public ZIP and physical-phone/general-release checks remain outstanding. No broader quiz/fallback algorithm or historical-origin certification is claimed. All review tool calls were issued singly and awaited; no internal tool overlap was observed, and no external process evidence was inspected.
