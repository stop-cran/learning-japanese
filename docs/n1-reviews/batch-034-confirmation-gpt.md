**Snapshot:** Initial `9800f1a1935fff861e4a9c0374bc6cad8ecf2f34`, plus the supplied uncommitted teaching diff:

```diff
 tags: [wago, noun, animals]
+quiz_exclusions: [動物]
```

The revised `words\猪.md` confirms this addition and otherwise matches the initially reviewed teaching. The task also reports a corresponding source-ledger pair and regenerated manifest; neither was inspected in this bounded confirmation. Git state was not independently verified. No edits made.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), original-session confirmation. Read my complete archived initial GPT report, all 52 lines of revised `words\猪.md`, all 34 lines of `words\動物.md`, and `docs\content-format.md:115–148`. Assessed the precise exclusion change and textual regressions across correctness, scoped coverage and comprehensibility. The unchanged kanji verdict carries forward from the complete initial review; its file was not reread.

**Verdicts:**

| File | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\猪.md` — unchanged; initial verdict retained | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\猪.md` — revised | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\動物.md` — comparison, bounded scope | **CLEAN** | **CLEAN** | **CLEAN** |

**Findings:** Original finding 1 — **resolved**.

The original **Minor correctness/quiz-uniqueness** finding concerned the unguarded `wild boar`/`animal` labels. `words\猪.md:8` now declares the exact existing ID `動物` once, in a valid inline exclusion list. Under `docs\content-format.md:133–140`, this directly protects the pair in both directions without requiring a reciprocal declaration or relying on the bear/animal exclusion.

The accurate labels remain unchanged (`words\猪.md:4`, `words\動物.md:4`). The category distinction remains explicit at `words\猪.md:33–36`; the guard does not assert that the Japanese nouns are interchangeable. It introduces no transitive clique, blanket category rule, pig exclusion, or change to identity, reading, level, examples or prose.

**Confidence:** High for resolution at the authored-content/contract level. Runtime enforcement was not tested. No new actionable defect or consequential unresolved linguistic claim established within this scope.

**Optional:** None. Additional い compounds, the いぐち homograph or a katakana example remain nonblocking expansion, not prerequisites for this animal lesson. The existing text already qualifies historical readings and compound meanings.

**Limits:** All confirmation reads completed without truncation. Calls were strictly serial, with no parallel tools or overlapping ranges. No other reviewer’s report was read. The initial supplied dictionary evidence remains the linguistic basis; no packet reread or independent upstream lookup occurred during confirmation.

This is textual confirmation, not new Android, glyph, physical-phone, combined-main, CI, manifest-hash or public-ZIP certification. Those outstanding boundaries remain unchanged; the exclusion requires an exclusion-aware client. No publication acceptance is inferred.
