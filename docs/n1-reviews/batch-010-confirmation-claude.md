My original finding is **resolved**. On re-reading, the old wording was ambiguous rather than reversed, so I am downgrading it from Minor correctness to low-severity comprehensibility. The revised `words/椋.md` is CLEAN on all three facets. This was read-only; nothing was edited or written.

**Snapshot:**
- Revised snapshot: the signed correction commit returned by the launcher. I did not see its hash in the files I read, so I can't quote it.
- Initial snapshot: `69640717b7ce459bfe121cc57efcf632ed450db8`.
- Uncommitted changes: none included.
- Diff: one teaching paragraph in `words/椋.md` (line 26), a new `docs/n1-sources/batch-010-restriction-evidence.json` and the regenerated `manifest.json`. The manifest changes only `contentVersion` and the `words/椋.md` hash.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), the original Claude session. This is a confirmation of the changed passage, not a fresh blind review.
- **Read in full, one at a time:** my own report `docs\n1-reviews\batch-010-initial-claude.md`, `control\batch-010-correction.diff`, the complete revised `words\椋.md` and `batch-010-restriction-evidence.json`.
- **Partial read:** lines 250–281 of `batch-010-jmdict.xml`, covering the whole of entry 2216250.
- **Not re-read:** the other three teaching files, the 73 dictionary families, the comparison articles and the Kotobank pages. Their status comes from my initial review.

**Verdicts:**
- **`words/椋.md` (revised):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`kanji/笹.md`, `kanji/椋.md`, `words/笹.md`:** unchanged; all three facets CLEAN, carried over from my initial review.

**Findings:** none on the revised snapshot.

**Disposition of my original finding (Minor; correctness; `words/椋.md:26`):** resolved, with recalibration.
- **Recalibration:** I withdraw my description of the old wording as getting the restriction "backwards".
  - Its first sentence ("permits むく specifically for 椋") correctly stated that the short reading is restricted.
  - "Its longer reading むくのき belongs to the listed plant-name spellings", followed by the general caution, did not say that 椋 alone cannot be read むくのき. It only left that implicit.
  - A learner could still have read the caution that way, so the issue was ambiguity.
  - Corrected classification: low-severity comprehensibility, not a correctness defect.
- **Checked against entry 2216250:** the revised paragraph matches the source. The entry has four spellings (椋木, 椋の木, 樸樹, 椋). むく is restricted to 椋. むくのき has no restriction, so it covers all four spellings, including 椋 alone. ムクノキ is a kana-only form and is not presented as a third reading.
- **Primary reading kept:** "This article uses むく" keeps むく as the article's reading. "Permits" is a statement about what the dictionary allows, not a claim about how common it is.
- **No new confusion with the character card:** the paragraph talks about dictionary readings of the whole word. The kanji card still quizzes only むく and keeps its source readings (むく and リョウ) in their original order. Its existing note already warns against replacing むく with むくのき.
- **No regressions:** nothing else in the article changed. The paragraph agrees with the Meaning section's "longer name 椋の木 (むくのき), also written 椋木" and with JMdict's flag that the word is usually written in kana.

**Optional:**
- The paragraph could add that むくのき for 椋 is a reading of the whole written word, not a separate reading of the character. The kanji card already covers this, so it isn't required.

**Limits:**
- **Exposure to other judgments:** the assigned evidence file contains the coordinator's ruling and a one-line summary of the other model's outcome. I read it because the task required that file, but I judged the change against the JMdict entry itself.
- **Reads:** the JMdict packet was read only at lines 250–281. I made no live dictionary lookups this time.
- **Inherited verdicts:** the three unchanged files were not re-read.
- **Instruction overlap:** the repository instructions were in my session context again, and `content-structure.instructions.md` was re-supplied during this session.
- **What this review is not:** it is textual only, with no phone, native-speaker or frequency evidence.
