**Snapshot:** The corrected teaching snapshot is `b99945c23eb8eb9a3cdd10a8a736a51d6c6cce71`, compared against the original `6ce5676`. No uncommitted teaching was included. The added evidence is `docs\n1-sources\batch-003-review-supplement-jmdict.xml`, which the coordinator extracted. I did not retrieve it upstream myself.

**Scope:** I'm Claude Opus 5.5 (`claude-opus-5.5`). I worked alone and used one tool call at a time. Files read completely:
- `docs\n1-reviews\batch-003-confirmation-prompt.txt`
- `docs\n1-reviews\batch-003-confirmation.diff` (one hunk: the `quiz_exclusions` line)
- `words\苗.md`, `words\植える.md`, `words\稲.md` and `words\植物.md`
- the supplement XML (JMdict entries 1357250 and 1167820)

The full 苗 family (JMdict 1490470) comes from what I read in the original pass; I didn't reread it. I didn't inspect the manifest, the validator or the app, and I read no other reports or ledgers.

**Verdicts for the changed `words\苗.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:** None.

**Checks on the two new exclusions**
- **Format:** line 8 now reads `quiz_exclusions: [芽, 植物, 木, 植える, 稲]`. It's a valid inline list. Both target words exist, nothing repeats or points to itself, and there's no `quiz_distractors` field to conflict with. The body is unchanged, so no text regressed.
- **苗 / 植える:** this guard is justified.
  - The displayed title of 植える is just "plant". Nothing in the label marks it as a verb.
  - In a quiz, a learner shown 苗 ("seedling; young plant") could reasonably pick "plant" as a noun. The reverse also works: shown "plant", 苗 is a defensible choice.
  - The evidence keeps the two words separate: JMdict 1357250 sense 1 is the verb "to plant; to grow; to raise", and 1490470 sense 1 is the noun "seedling; young plant". The safeguard comes from the ambiguous label, not from the words meaning the same thing.
  - The existing 苗/植物 and 植物/植える exclusions don't cover this pair, because exclusions only apply to the exact pair listed.
- **苗 / 稲:** this guard is justified, kept narrow.
  - 稲's title "rice plant" (1167820 sense 1, Oryza sativa) can fit 苗's second sense, "rice seedling" (1490470 sense 2).
  - Both 苗.md ("It can name rice seedlings") and 稲.md (the crop growing in a field) put the words in overlapping contexts.
  - It works like the existing 苗/木 young-tree guard. It doesn't treat the words as synonyms, and it doesn't require excluding every plant-related word.
- **Coverage:** neither new pair is linked or discussed in the body. That's fine, because an exclusion only protects the quiz and doesn't need to be taught.

**Reconciliation of my original observations**
- **Original findings:** there were none, so nothing is left unresolved.
- **Optional #6 (苗 vs 稲):** I'd said it didn't need an exclusion. Now that it's been adopted, this observation is resolved. Adding the guard is a reasonable and slightly more cautious call, not a contradiction of my original verdict.
- **My original claim that no remaining title pair had overlapping acceptable answers needs qualifying.** I missed 苗/植える. The bare title "plant" makes that pair ambiguous, and the new exclusion fixes it. This is a correction to my own coverage claim, not a new open defect.
- **Optional #1–5:** these weren't adopted. They are still optional and nonblocking.

**Overall:** apart from the 苗/植える correction above, my original ten-file textual verdicts stand. No consequential in-scope textual claim remains unresolved.

**Optional:** None new.

**Limits**
- The supplement is coordinator-extracted evidence from frozen JMdict, not my own live retrieval.
- I didn't check that the regenerated manifest is current or how the app handles the exclusions in practice.
- This is a bounded confirmation, not a second full review. It is not native-speaker, phone or measured-learning certification.
