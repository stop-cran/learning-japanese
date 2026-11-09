**Snapshot:** `0b6be1de66c9681b208ee2d27f0253baed4052cc`, obtained through the authorized serial `.git`, worktree `HEAD` and branch-ref reads. **You verified the signature separately; I verified only the returned ref value.**

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), dependent read-only follow-up. Read the complete returned `correction-fee-packet.txt` and my previous `confirmation-gpt.md`, without reported truncation. This assessment also retains previously read evidence; no other reviewer report or ledger was accessed, and no tests were independently executed.

**Verdicts:** The new **勘定/料金 exclusion is an acceptable conservative context-free quiz safeguard**, not overly broad or inadequate within this correction. **Confidence: medium-high for its editorial justification; high that the supplied declaration implements the intended direct pair.** My prior position is unchanged.

At `words\勘定.md:9`, 料金 is now directly excluded while both titles and explanations remain unchanged. JMdict **1210750, sense 2** gives 勘定 “bill; check; account; payment; settlement”; **1554280, sense 1** gives 料金 “fee; charge; fare.” Together with `words\勘定.md:16` and `words\料金.md:15`, this supports a contextual **bill/charge** collision between the displayed labels “reckoning; bill” and “fee; charge; fare.” It does not establish equivalence for abstract reckoning, every fare, or unrestricted substitution between the Japanese words. The safeguard needs no transitive argument through 代金.

| Facet, bounded correction | Verdict |
|---|---|
| Correctness, including declared quiz guard | **CLEAN** |
| Scoped coverage | **CLEAN** |
| Textual comprehensibility | **CLEAN** |

**Findings:** The previous fee-pair finding is **resolved**. The exact diff appends only 料金 and preserves `[計算, 支払う, 給与, 払う, 代金]`. The supplied test additionally asserts preservation of 勘/感覚 and checks all seven direct pairs.

The supplied `Words.kt:175–178` checks declarations from either endpoint and between selected distractors; both meaning directions use this selector. `Batch107FeeQuizTest.kt:53–64` exercises both endpoints and directions in two-card pools, expecting only the target. Lines 98–102 check that a neutral target cannot receive both excluded cards as distractors. Supplied current host samples show guarded All/custom choices and unguarded controls in both directions. These support **symmetric exclusion and permitted short pools**, but are supplied execution evidence—not tests I ran. Unguarded controls establish reachability, not linguistic ambiguity.

**Optional:** None. No material omission or additional remedy established within this correction.

**Limits:** The pre-existing **定/違 reading-explanation gaps** and **支払う/支払 comparison remain unresolved and nonblocking under the previously stated bounded scope**; this change does not fix them. No claim is made of native review, phone/font/UI acceptance, merged-tree validation, publication, global semantic safety, or compatibility with older clients that ignore exclusions.