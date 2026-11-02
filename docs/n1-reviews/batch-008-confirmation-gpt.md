**Snapshot:** `dd8cd880fcfe212256e8825b1486c5c7fbc8b8b7`, task-identified revised frozen snapshot; original `2a9ffe40c77c8fb74cd97c422932ddfe868a3248`. No uncommitted changes included in the assigned scope; Git state and signatures were not independently verified.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), original-session read-only confirmation. Freshly read my own original report, the complete correction diff, complete revised `words\楓.md`, and complete `words\紅葉.md` for the cross-reference. Assessed the changed passage for correctness, scoped coverage, comprehensibility, and regressions. The unchanged three-file review is inherited, not freshly repeated.

**Verdicts:**

| File | Correctness | Scoped coverage | Comprehensibility | Basis |
|---|---|---|---|---|
| `words\楓.md` | CLEAN | CLEAN | CLEAN | Fresh revised-file and changed-passage check |
| `kanji\楓.md` | CLEAN | CLEAN | CLEAN | Inherited unchanged initial review |
| `kanji\楠.md` | CLEAN | CLEAN | CLEAN | Inherited unchanged initial review |
| `words\楠.md` | CLEAN | CLEAN | CLEAN | Inherited unchanged initial review |

**Findings:** No remaining actionable defect or regression established.

**Reconciliation: resolved** — Minor; comprehensibility; original `words\楓.md:28`. “The maple-tree example above” ambiguously referred to local 楓/かえで examples, whereas the relevant 紅葉/もみじ example was in the linked article. Revised line 28 directly identifies the spelling and sense: “When 紅葉 means a maple tree, read it もみじ, not こうよう.” This removes the reference ambiguity without changing a Japanese example or introducing an incorrect reading.

Evidence: the exact one-line diff; revised `words\楓.md:28`; freshly checked `words\紅葉.md` maple example 庭に紅葉を植えました, explicitly read もみじ; and initially inspected JMdict families 1578780 (こうよう, autumn foliage) and 2857870 (もみじ, maple and autumn foliage). The new statement is conditional on the maple-tree sense, not a claim that もみじ cannot mean foliage or that these exhaust every reading and sense. **Confidence: high.**

My initial report was CLEAN and did not identify this ambiguity; this confirmation does not retroactively claim that catch.

**Optional:** None. No mandatory new exclusion pair or expansion is established by this change.

**Limits:** Dictionary-family evidence is inherited from the initial full-packet inspection; no new live lookup or full-dossier reread was performed. Unchanged metadata, quiz selections, exclusions, and the other three teaching files were not freshly re-audited. All confirmation reads returned completely without observed truncation. Calls were issued individually after preceding results; no internal overlap was visible, but backend scheduling was not independently observable. Assessment is textual, without app execution, native-speaker testing, physical-phone rendering, or measured readability. No other reviewer’s report was read and no files were changed.
