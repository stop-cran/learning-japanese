**Snapshot:** `f093f464c35423f728e3a0e756bee358b061d65c`, the task-identified frozen snapshot; committed teaching only, no uncommitted teaching included. Read-only review; no files changed.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), reviewing correctness, scoped coverage and textual phone comprehensibility of complete `kanji\榛.md` and `words\榛.md`. Read the complete repository instruction files, the specified content-format/JLPT ranges, complete input metadata and embedded raw KANJIDIC2 character element, and all **41 complete dictionary families**: main packet 9, comparisons 21, notes 10, supplement 1.

Read all four complete comparison kanji (`木`, `棒`, `春`, `稲`) and all seven complete comparison words (`木`, `植物`, `植える`, `植木`, `栗`, `楠`, `実`). Independently fetched and inspected the three assigned Kotobank entries. Comparison files were supporting evidence, not separately certified articles.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\榛.md` | CLEAN | CLEAN | CLEAN |
| `words\榛.md` | CLEAN | NEEDS FIX | CLEAN |

CLEAN means no actionable defect established within this scope, not exhaustive certification.

**Findings:**

1. **Minor; scoped coverage/navigation; `words\榛.md:20`.** The article substantively introduces 実 (み), explaining its nut referent, but never links its existing companion article. This omits the required navigation at a substantive introduction and prevents direct access to the broader fruit/nut/seed explanation.

   **Remedy:** Change this occurrence to `[実](実.md) (み)`; no sentence or exclusion change is needed.

   **Evidence:** Line 20 explicitly teaches 実’s meaning. The complete `words\実.md` supplies the relevant plant-fruit/nut/seed explanation and distinguishes its substance sense. `.github\instructions\content-structure.instructions.md`, “Authoring checks,” requires linking existing cards at substantive introductions or comparisons.

   **Confidence:** High. This is a localized navigation omission, not incorrect Japanese or a missing explanation of the example.

The remaining checks established no actionable defect:

- All four sourced readings and their order are preserved: **シン・ハン / はしばみ・はり**. The empty on-quiz list suppresses questions without deleting readings. Selected はしばみ has its own linked row and independently supported whole-noun allocation.
- JMdict 2066150 and the fetched **はしばみ** entries support the hazel plant noun; the native entries support deciduous-shrub status, rounded leaves with irregular edges, and edible nuts. Both learner sentences and their readings/translations fit those claims.
- Alder readings and identities are qualified appropriately. The fetched **はり** entry identifies an old alder name; **はんのき** identifies alder independently of hazel. ハン’s source classification is not inferred merely from compound kana.
- The complete 榛莽 family and fetched Seisenban entries support both pronunciations and vegetation/place meanings. The optional row provides kana, a component description and dictionary access without making the unbundled second character a required learner operation.
- Kana-only flags, rare nut-expression status, alternative readings and unrelated homographs do not establish an unrestricted replacement rule. The cards do not manufacture one.
- The three default kanji distractors have distinct ordinary meanings. The word’s four direct exclusions protect broader tree/plant/garden-plant labels and the ambiguous English “plant” label. No additional exclusion with 栗, 楠 or 実 was established from the actual labels and senses.
- The shape explanation is expressly mnemonic, not etymology.

**Optional:** None.

**Limits:** `docs\confusable-words.md` was read at lines 1–120 and searched for relevant Japanese forms and English cues; this was not a complete inventory audit. Initial instruction-file truncation was recovered by continuation; no required local packet remained truncated.

The 榛 page’s 字通 section returned no substantive body. A gaiji occurred in a compound-entry bibliography; neither was used as evidence. The relevant native definition bodies were available.

No fresh upstream JMdict/KANJIDIC2 download, independent Git-status verification, physical-phone execution, font/rendering measurement, corpus-frequency measurement or native-speaker certification was performed. Snapshot identity comes from the assignment. Calls were issued individually and awaited; no internal tool overlap was observed, and unavailable process evidence is not claimed.
