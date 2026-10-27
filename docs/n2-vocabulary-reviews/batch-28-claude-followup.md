**Snapshot:** The new commit is `77294a7957b94d1102e421fb5cfca231431abb0a`, with parent `f97be4e9b16d7aba1282551c4afe9610a21806f7`. I had file and web tools only, no Git or hashing. The commit identity, clean-tree claim, file and diff hashes, and the derivative's equivalence are all author-run checks that I did not repeat. I did confirm one thing myself: `docs\n2-vocabulary-snapshot.json:34` now holds `a9621e2f…`, which matches the TSV hash in the receipt.

**Scope:** claude-opus-5.5 (claude family), working alone, read-only. I read:
- My own confirmation report and the follow-up receipt.
- The whole follow-up patch (66 lines), after first confirming it contains no quiz-rationale text.
- In the repository: TSV row N2:552 and snapshot.json lines 34 and 49–51.
- In the follow-up derivative:
  - the N2:552 row (lines 186–206);
  - `sourceMappingCorrection` originalRecord and correctedRecord (lines 14591–14632);
  - `publicEvidence` and the complete `confirmationFollowThrough` (lines 14815–14847).
- An "audience" search across the TSV and the derivative.
- A line-count and section-position comparison with the earlier confirmation derivative.

I did not reread the articles or re-review the batch.

**Verdicts:** correctness / scoped coverage / comprehensibility.
- **N2:552 source note** (TSV:552 and derivative lines 202 and 14629): CLEAN / CLEAN / CLEAN.
- **Preserved mapping and raw fields** (raw gloss `to cross,to pass,to tide over`, selected sense 4, additional senses 1,2,3,5, level 3, `words/越す.md`, entry 1175300, the mapping and identity notes, and the originalRecord with its 1–3 selection): CLEAN / CLEAN / CLEAN.
- **Appended confirmationFollowThrough and the snapshot hash:** CLEAN / CLEAN / CLEAN.
  - The derivative grew by exactly the 13 appended lines (14834 → 14847).
  - Earlier section positions are unchanged, and the snapshot row counts are unchanged.
  - The only remaining "audience-related" wording is the deliberately kept `previousSourceNote`. The TSV row keeps all 16 fields.

**Findings:**
- **B28-C04 (inaccurate audience-gloss note): resolved.** The row note and the corrected-record copy now quote the exact CSV gloss, which matches the pinned CSV row I fetched earlier. The earlier note is preserved in `previousSourceNote`, and no article, sense, level or exclusion changed.
- No new actionable issue. This edit introduced no regressions.

**Optional:**
- The new note says the raw gloss "does not describe" the quantity-exceeding use. English "to pass" can mean "to exceed", so "does not explicitly name" would be more precise. This is not blocking: the wording errs on the conservative side, and the sense-4 selection stands on the 超す spelling and JMdict's "often 超す".
- Carried over, outside this edit:
  - The source-list reference in 越す.md:42.
  - The コック title "tap valve" could become "tap; valve".

**Limits:**
- No Git or hashing; the receipt's hashes and derivative equivalence beyond what I compared are the author's claims.
- I did not read the canonical batch-28.json directly, only its hunks in the patch.
- I cannot check B28-GPT-03 because the other family's report is off-limits.
- Coverage of the articles, guards and the other 19 mappings carries over from my earlier reviews.
- No app draws were run; this is not corpus or native-speaker certification, and the source is a community list, not an official JLPT syllabus.
