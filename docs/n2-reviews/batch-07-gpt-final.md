**Snapshot:** `ddd5f71dc59f48ebf43d560c4ce3b1c3fbf83827`; clean committed files only, as authenticated by the author. My file tools cannot execute Git, so commit identity, cleanliness, and diff provenance were not independently verified.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Sequential, read-only confirmation of the supplied diff and `words\巻く.md:8`, using the surrounding article, `words\ぐるぐる.md`, `scenes\ぐるぐる.json`, and the content-format rules. All other teaching passages retain prior coverage and were not reopened. No edits, delegation, or other reviewer reports.

**Verdicts:** Correctness **CLEAN** · Scoped coverage **CLEAN** · Comprehensibility **CLEAN**.

**Findings:** None remaining. The diff adds only the direct **巻く ↔ ぐるぐる** exclusion, retaining 包む, 風, and くるくる. Its justification is concrete: `words\ぐるぐる.md:4,20` supplies the overlapping “winding around” label and string-around-box example; `scenes\ぐるぐる.json:13–17` declares that winding scene quiz-eligible. The direct pair is necessary because exclusions through くるくる are not transitive (`docs\content-format.md:85–88`), and word-level exclusions apply to every eligible scene (`:127`). This prevents ambiguous opposing choices without asserting lexical interchangeability. My earlier confirmation did not identify this additional pair; it is now explicitly covered. **Confidence: high.**

**Optional:** None.

**Limits:** The scene’s eligibility and description were inspected, not its image bytes or runtime rendering. No app execution or manifest verification was performed. No consequential uncertainty remains about the changed line within this bounded review.
