# Initial consistency and quiz-safety review

**Snapshot:** `stop-cran/learning-japanese` at
`bac3477e5323fad11c54e2f2bd424cd5c3693096`, parent
`e824da99c8a19479bfede4e6fbe88b1f21a4180b`.

**Scope:** Blind, read-only review of all nine new words, ten new kanji and stroke files, eleven
changed reused articles, and B161 source, progress and manifest records. Verified the next ten
Jōyō source rows, 18 reciprocal link pairs, 132 JMdict families, baseline preservation and manifest
integrity. No new exact-title collisions were found. Content validation and the mechanical batch
audit passed.

**Verdicts:** Consistency and quiz safety NEEDS FIX; scoped coverage NEEDS FIX; comprehensibility
UNVERIFIED.

**Findings**

1. **Blocking — `words/圏内.md`:** The exclusion covered 以内 but missed 内, whose “inside; within”
   meaning can answer 圏内’s physical-zone sense. Add 内 and record it in the ledger.
   **Confidence:** High.
2. **Blocking — `words/たえる.md`:** The exclusion covered こらえる and 凌ぐ but missed 我慢, whose
   article explicitly overlaps with 耐える for bearing difficulty. Add 我慢 and record it in the
   ledger. **Confidence:** High.
3. **Blocking — `kanji/培.md` and `words/培養.md`:** Existing 修 describes self-cultivation, while
   育てる overlaps with 培養's plant-growing and skill senses in the pinned JMdict packet. Add the
   direct 培/修 and 培養/育てる exclusions and update both audit lists. **Confidence:** High.
4. **Non-blocking — `batch-161-progress.json`:** `mechanicalChecks` recorded a stale manifest
   version and older byte counts. Refresh it from checks on the final candidate.
   **Confidence:** High.

**Optional:** None. One declaration per direct pair is sufficient because the documented compatible
client applies exclusions symmetrically.

**Limits:** No Android execution or independent retrieval of upstream source archives. Japanese
correctness and general comprehensibility were outside scope.
