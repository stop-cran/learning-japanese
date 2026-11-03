**Snapshot:** `3e2bf34ee3b9621cbaec8713f2b157fdeb74c764`, the task-designated frozen batch019 snapshot; committed teaching only, no uncommitted teaching included. Commit/worktree status was supplied by the task, not independently checked.

**Scope:** Independent initial read-only review by GPT-6.1 Sol (`gpt-6.1-sol`). Reviewed both complete teaching files, `kanji\蚊.md` and `words\蚊.md`, for correctness, scoped coverage, and textual phone comprehensibility, including every sentence, translation, metadata field, reading row, quiz selection, and substantive link.

Read the prescribed instruction/contract ranges; complete input metadata, including the raw KANJIDIC2 element; and all four complete frozen JMdict packets: main 999 lines/44 families, comparisons 312/9, notes 186/5, supplement 366/7—**1,863 lines and 65 complete families**. Inspected spelling/reading restrictions, sense restrictions, secondary senses, and register/search-only/obsolete/kana-only flags.

Read all five complete comparison kanji (`文`, `枚`, `改`, `虫`, `蛍`) and all three complete comparison words (`虫`, `蛍`, `刺す`). Searched `docs\confusable-words.md` for 蚊/虫/蛍/刺す; no matches returned. Independently fetched both specified Kotobank pages, including relevant raw-HTML Digital Daijisen bodies.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\蚊.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\蚊.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded review, not exhaustive certification.

**Findings:** None.

Supporting checks:
- KANJIDIC2 supports 10 strokes, classical radical 142, grade 8, meaning “mosquito,” and the complete ordered readings `[ブン]` / `[か]`. Both readings receive rows. Selecting only `か` provides a useful, directly verified linked animal noun; disabling on-reading questions preserves metadata without requiring medical vocabulary production.
- JMdict 1196540 supports 蚊・か “mosquito” and the kana-only カ alternative. Digital Daijisen’s actual `ぶん【蚊】［漢字項目］` explicitly places 飛蚊症 under ブン, independently establishing the allocation rather than relying on a kana substring. Its 飛蚊症 entry and Seisenban support the visual-symptom explanation.
- The modern short pronunciation is appropriately distinguished from Seisenban’s historical long-pronunciation note. 蚊帳・かや and 蚊取り線香・かとりせんこう match their dictionary families without extending obsolete alternatives or irregular whole-word readings into unrestricted rules.
- Both word examples are natural, with accurate readings and translations. 一匹・いっぴき fits the small-animal counter; the passive mosquito construction and its actor marked by に agree with the biting/stinging sense of 刺す.
- The reciprocal 蚊 kanji/word links resolve to the articles reviewed. The reused word retains its explicit **N2 vocabulary classification**, independently of the new N1 kanji classification.
- The mnemonic explicitly disclaims etymology. The 文/枚/改 shape comparisons fit their modern forms. Their actual answer labels—“sentence, writing,” “counter for thin flat objects,” and “revise; reform”—are semantically distinct from ordinary 蚊 meanings.
- 虫 is correctly treated as a broader category, omitted from the curated kanji distractors, and directly excluded in the word quiz. 蛍’s ordinary insect meaning does not introduce a mosquito overlap; its contextual historical senses do not justify transitive exclusions.

**Optional:** None.

**Limits:** All required local reads returned completely; every XML request used an explicit range of at most 200 lines. The frozen dictionary packets were inspected, not freshly retrieved upstream. The confusable-word inventory inspection was a scoped search, not a complete inventory review.

Simplified Kotobank extraction omitted Digital Daijisen bodies; targeted raw HTML supplied the relevant complete entries. Raw windows ended in unrelated subsequent sections; no consequential teaching claim depended on those unfinished tails. Gaiji images were not decoded, but the reading labels and compound grouping needed here were explicit text.

This was textual review, not fresh Android rendering, physical-phone/native acceptance, or combined-main/CI/public-ZIP verification. The task-supplied unchanged-font coverage and prior acceptance remain inherited evidence within their stated scope. Fresh019 integration/publication checks and physical-phone/general-release acceptance remain pending.

No internal tool-call overlap was observed: calls were issued individually and results awaited. No external reviewer-process evidence was inspected. No edits, shell commands, delegation, commits, issues, or other review reports were used.
