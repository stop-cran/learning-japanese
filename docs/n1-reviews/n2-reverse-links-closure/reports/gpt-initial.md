**One minor fix on 第:** the new 落第 note can mislead learners about where the ordinal prefix goes. All nine reciprocal link pairs and newly cited JMdict IDs match the packet. No quiz-field change appears in the supplied diff.

**Snapshot:** `3cbc312e31506bb099b599c7025030f44e820c0e`, based on B169 `6e1e0342c91d9d6ba88fee577abd9e638dd645d3`. No uncommitted changes were included in the review packet; the author’s draft checks are reported separately as covering the same content.

**Scope:** One independent reviewer (GPT-6.2 Sol). Reviewed the changed reading rows, Common words entries, four notes, and metadata on five retained N2 cards. Used the full cards for context and the nine word cards, JMdict excerpts, and supplied checks for evidence. Unchanged passages were not independently adjudicated.

| Card / on row | Verified word targets (reading; JMdict ID) | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| 保 / ホ | 保健 (ほけん; `1513410`), 保証 (ほしょう; `1603500`) | CLEAN | CLEAN | CLEAN |
| 案 / アン | 案外 (あんがい; `1154820`), 答案 (とうあん; `1449550`) | CLEAN | CLEAN | CLEAN |
| 派 / ハ | 立派 (りっぱ; `1551790`) | CLEAN | CLEAN | CLEAN |
| 結 / ケツ | 結局 (けっきょく; `1254730`), 結構 (けっこう; `1254760`), 結論 (けつろん; `1255020`) | CLEAN | CLEAN | CLEAN |
| 第 / ダイ | 落第 (らくだい; `1548810`) | CLEAN | CLEAN | NEEDS FIX |

**Finding — minor, comprehensibility, high confidence (`kanji/第.md:41`):** “第 follows 落 rather than a number” suggests that ordinal 第 would *follow* a number. The next note correctly says it goes *before* one, as in 第三回. The classification of 落第 itself is sound. Replace the note with: “In 落第 (らくだい), 第 is part of a fixed word. It does not introduce an ordinal number as it does in 第三 (だいさん, ‘third’). Learn 落第 as a whole.”

**Consistency and quiz-field preservation — CLEAN on all five.** Each new relative link points to the supplied word card in both the primary on-reading row and Common words. Each word declares the kanji and links back to it. The readings, glosses, and nine added metadata IDs agree with the word cards and JMdict excerpts. The diff leaves front matter, levels, quiz readings, and distractors untouched and shows no word-card edits, including to exclusions. The supplied checks report the same six lean quiz-safety errors and eight latent reading collisions at base and draft; these are not new regressions or a quiz-safety pass.

**Accounting:** Five retained N2 cards edited, nine distinct pairs, 18 new link placements, nine added ID citations, and zero card additions or removals. The recount is internally consistent: 712 published N1 + 6 retained N2 (including untouched 策) + 510 remaining = 1,228; 805 activated + 5 unactivated = 810 frozen candidates. This correction is not a new batch or an N1 addition. The supplied B169 audit still fails on the changed baseline payload; it is not a passing gate for this snapshot.

**Optional:** In `kanji/結.md:30`, add “In these examples” before the けっ/けつ contrast to keep the wording tied to the listed compounds.

**Limits:** Packet-only review. I did not independently rerun the gates or recount, verify archive bytes or manifest hashes, or inspect external pages or checkpoint receipts. No whole-deck quiz, publication, native-speaker, or device acceptance was established.
