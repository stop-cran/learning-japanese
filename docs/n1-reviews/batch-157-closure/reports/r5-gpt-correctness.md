Snapshot: commit `f811f8eb`; reviewer model unknown
Scope: All 28 snapshot Markdown cards and 10 stroke JSONs; diffs, evidence, title indexes, rubric, and required repository docs. Correctness examined deepest.
Verdicts:
- Correctness: CLEAN.
- Scoped coverage: NEEDS FIX — `kanji/理.md`, `kanji/助.md`.
- Consistency and quiz safety: CLEAN.
- Comprehensibility: CLEAN.
Findings:
1. **Minor; scoped coverage;** `snapshot/kanji/理.md:10,26`; `snapshot/kanji/助.md:10,45`. The metadata includes `ことわり`, `す.ける`, and `すけ`, but the reading tables omit them; the notes only say they are retained as source readings. This leaves metadata readings without the rows required by the packet’s coverage criterion. Add rows with appropriate examples and qualifications. **Evidence:** the cited front matter and notes versus each card’s `## Readings` table. **Confidence:** high on the omission; medium on its learning impact.
Optional: None.
Limits: No app or phone testing, nor exhaustive corpus-frequency verification. Source data is pinned to JMdict 2026-11-17 and KANJIDIC2 2026-11-02; public-source checks were selective.