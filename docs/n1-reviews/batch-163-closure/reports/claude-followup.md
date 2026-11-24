**Snapshot:** original b89b7a45, revised afad8a17. This is a changed-passage confirmation, not a second blind review.

**Inspected:** `corrections.diff`, `revised-support.txt`, `evidence.txt`, and `revised-text-1` to `-4`. I compared each diff hunk with the revised text, and they match. I did not open `confirmation-task.txt`, because it wasn't on your list. There is no revised 奮う.md and no diff hunk for it, so its original text stands. I did not re-review unchanged articles.

**Reconciliation of my earlier findings**
- F1 奴 kanji, やつ vs やっこ outside-table status: **resolved**. Both rows now say outside-table. Optional wording nit: "usually written やつ" would be clearer as "usually written in kana (やつ)".
- F2 欠如, the 如 "state" claim: **resolved**. The claim is removed.
- F3 奴 word, sense 3: **resolved**. The "he/she" use is added with the JMdict tone, and "often" became "usually" for the sense 1–2 kana note.
- F4 妄想, example 2 translation: **resolved**. It now reads "The idea of a trip…".
- F5 奉仕, provenance and ご奉仕品:
  - **Resolved.**
  - Entries 2145970 and 1946830 are cited.
  - The invented sign example is replaced by 奉仕品, which matches JMdict 1946830.
  - The shop sense now matches JMdict sense 2 and sits in "Meaning".
- F6 一, source line: **resolved**. Entry 2138590 is cited.
- F7 奮う, 気力を奮って:
  - **Partially resolved, evidential only.**
  - The text is unchanged.
  - The author reports that Daijisen 奮う illustrates 気力を奮って.
  - I could not verify that, so it is not independently confirmed. It is non-blocking.
- F8 良, name-only ら: **resolved**. The bullet now says 良 is ら in this name, not リョウ. The Daijisen name-reading check is author-reported only.
- Optional items now adopted:
  - 奮 "long う" is reworded.
  - 奔る is tied to running away or eloping, matching the JMdict "occ. 奔る" note on sense 5.
  - The ご prefix is gone.
  - Quiz exclusions were added for 奮↔鼓, 奔走↔苦心 and せっせと, and 奉仕↔勤め. The label overlap is supported by `revised-support.txt` entries 1240810 and 2008620.

**New finding (regression)**
- **N1 — minor, NEEDS FIX, correctness, 奈 Notes and the いかん table row.**
  - The new Notes say "Distinguish 奈何 (いかん, 'how; in what way') from 如何 (いかが, 'how; how about')."
  - This misleads. JMdict 1582850 gives 如何 as the main spelling of いかん, with 奈何 as the rare variant. 如何 is also read いかが (2845606).
  - The gloss is off. JMdict gives いかん as "(depending on) how/what; nature (of)" and, at sentence end, "what is…?". "In what way" belongs to いかが.
  - The table row still says "how", so the article is also internally inconsistent.
  - Remedy: write "奈何 is a rare spelling of いかん, which JMdict usually writes 如何 ('depending on how/what'). 如何 is also read いかが ('how; how about'), usually in kana. Each reading belongs to the whole word; neither is a model for 奈良." Align the table gloss with it.
  - Confidence: high.

**Optional (nothing blocking)**
- 如 Notes: "欠如 does neither" is ambiguous. Say "欠如 expresses neither resemblance nor comparison."
- Still open from before:
  - The 振るう homophone and the adverb 奮って (JMdict 1504710) are unmentioned.
  - The ごとし register is not flagged.
  - 欠如 vs 不足 is not contrasted.
  - 奮う↔勇気 and 励ます have no quiz exclusion, so the labels may still overlap. That is outside my facet.

**Verdicts for the changed set** (correctness / coverage)
- CLEAN / CLEAN: kanji 奉, 奔, 奮, 奴, 如, 妃, 良; words 一, 奉仕, 奔走, 奴, 妄想, 欠如.
- 奈 kanji: NEEDS FIX (N1) / CLEAN.
- 奮う word: UNVERIFIED (F7, evidential) / CLEAN.

**Limits**
- I could not verify the author's Daijisen claims, the target of the new 似る link, or the batch audit figures (0 errors, 75 families, 17 pairs). The audit figures are the author's own. The 75 families are consistent with the four added entries in `revised-support.txt`.
- No native or device verification.
