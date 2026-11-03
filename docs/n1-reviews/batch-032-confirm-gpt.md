**Snapshot:** Revised `23ce40fee3aea6718d56958c2b9f24e5d813bac7`, compared with original `2cbbb0b836a5a2363a175a0df7cd14f12c5f99fc`. Identities and absence of uncommitted teaching are supplied by the task, not independently Git-verified.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), original-session dependent confirmation of the exact correction diff. Completely read current `words\鶏.md`, `words\鳥.md`, `words\鳴く.md` and `words\肉.md`; actual line counts are **49, 42, 42 and 41**, respectively, rather than the supplied 48, 42, 41 and 36. All tails returned. Rechecked complete JMdict families 1252990, 1253020 and 1430250 in the prescribed ranges, plus the scoped canonical exclusion and linking contracts.

**Verdicts:** Within the changed-passage scope, retaining the original review for unchanged teaching:

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\鶏.md` | CLEAN | CLEAN | CLEAN |
| `words\鶏.md` | CLEAN | CLEAN | CLEAN |
| `words\鶏肉.md` | CLEAN | CLEAN | CLEAN |

**Findings:** No remaining actionable defect established.

**Reconciliation:** The original **minor scoped-coverage/navigation finding is resolved** at `words\鶏.md:22,29`: `[鳴く](鳴く.md)` and `[肉](肉.md)` now link the substantive explanations to the existing, fully inspected support articles. Their content supports the animal-call explanation and on-reading ニク. Wording, examples and reading allocation are otherwise unchanged. **Confidence: high.**

The added direct **鶏/鳥 exclusion is justified** at `words\鶏.md:8`. JMdict 1430250 sense 2 documents bird meat, especially chicken meat; `esp. 鶏` is a qualification, not an exclusive spelling restriction. Current `words\鳥.md:39–42` also explicitly teaches the chicken-meat food use. Consequently, 鳥/とり can be a defensible Japanese choice for the bare English answer “chicken” understood as food. This narrows my original conclusion about additional exclusions: the pair is supported by its applicable secondary sense, **not** by treating broad “bird” and specific “chicken” as exact animal synonyms. **Confidence: high.**

The retained **鶏/鶏肉 exclusion remains justified** by 1252990’s chicken-meat sense and 1253020’s chicken-meat sense. Both exclusions follow the canonical one-sided, bidirectional, pairwise contract; they create no transitive exclusion or broader category rule. No regression was established in the revised passages.

**Optional:** None required. Additional example links, baseline backlinks and presentation expansions remain nonblocking.

**Limits:** This was not a fresh blind review or fresh read of all 131 families. Unchanged kanji metadata, strokes and reused 鶏肉 teaching retain the original review’s evidence and limitations. Dictionary confirmation used frozen supplied packets; no fresh web lookup or hash verification occurred. Only my own archived initial report was inspected; no other reviewer report or author ledger was read.

No edits, shell commands, delegation, commits or issues occurred. Tool calls were issued individually and awaited; no overlap was observed in this session, without claiming unavailable external process evidence. Native/font, physical-phone, fresh Android, combined-main, CI and public-ZIP acceptance remain outstanding; textual CLEAN verdicts do not certify those checks. Compatible Android `f9b59a2` or later remains required.
