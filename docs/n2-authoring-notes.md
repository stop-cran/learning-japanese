# N2 expansion notes

## Scope and evidence

The [source snapshot](n2-source-snapshot.json) fixes the kanjiapi.dev N2 community set retrieved on 2026-10-21:
367 characters, including the existing cards for 珍 and 短. The expansion therefore needs 365 additions, not an assumed
generic N2 count. Modern JLPT does not publish an exhaustive kanji syllabus.

The baseline is `7a92dde23107173af8aabef51971dbc66b754a93`. Existing cards and word identities are preserved.
Use existing word articles where useful; add supporting articles only where needed. A kanji's level does not establish
a word's vocabulary level. Dictionary readings and senses must respect spelling, reading and sense restrictions.
Per-batch records under [n2-batch-sources](n2-batch-sources) retain the inspected metadata and dictionary entries.

The canonical [format](content-format.md), [authoring checks](../.github/instructions/content-structure.instructions.md),
[review guidance](../.github/copilot-instructions.md) and [JLPT policy](jlpt-levels.md) apply; this note does not replace them.

## Observed authoring pitfalls

- Candidate dictionary examples need inspection: an existing filename can teach a different reading or lexical identity.
  For example, the companion 仲間 なかま is not the historical 仲間 ちゅうげん.
- Adding a kanji card activates link checks in existing word articles that declare that kanji. Link the existing substantive
  component explanation; a new card's forward link to the word does not satisfy that separate check.
- Dictionary inclusion is not evidence of everyday frequency. Preserve unusual source readings without manufacturing
  ordinary examples. The pilot retains the unmatched readings of 並 and 乱 as character-dictionary-only lookup information.
- Inspect non-initial positions before declaring a reading source-only. The pilot's word-initial candidate heuristic
  missed 胡乱 うろん for 乱's ロン. Candidate discovery now also considers word-final matches; a kana match is still not
  proof of character-by-character reading allocation. The proposed 乱りに example does not by itself establish `みだ.る`.
- Keep spelling, pronunciation and register qualifications separate. JMdict's rare-spelling flag on 依る does not make
  よる a rare pronunciation; missing priority flags do not prove that a word is rare. Batch records retain spelling and
  reading priorities separately, with their union used only for candidate navigation.
- Preserve evidence for additional pairs asserted in notes, not only the reading-table examples. The pilot now records
  仏語 ぶつご, 乳房 ちぶさ and 依存 いそん explicitly. For external dictionaries, inspect the exact headword and any notation
  guide needed to interpret symbols; the 乾 usage notes cite the entries and Daijisen's outside-Joyo reading marker.
- The current validator enforces explained kunyomi only for N5/N4. N2 needs an explicit metadata-to-reading-table audit,
  even after structural validation passes.
- Three curated wrong answers avoid default four-choice fallback for new cards. Review the meanings, not just title strings.
  The pilot also gives existing 下 and 長 a third wrong answer because new low/long-time answers could otherwise appear
  as defensible random fallback choices.
- Use labelled modern-shape mnemonics when historical or phonetic analysis has not been established. Keep canonical radical
  metadata and explain visible variants rather than replacing the indexing radical.

## Review and checkpoint protocol

Work in the source snapshot's batches, sequentially. Checkpoint content and regenerated manifests before review, then
commit confirmed fixes and their reconciliation. Git author and committer are `stop-cran`.

Each batch receives independent GPT and Claude review of the same frozen snapshot, files, facets and evidence.
Run one short-lived reviewer process at a time and confirm exit before starting another; there is no explicit agent-unload
tool in this environment. Initial reports stay blind to one another and to the author's preferred adjudication.
Record actual models and review limits in the [review ledger](n2-review.md).

Reconcile against evidence, not votes. Retain the initial reports and mark findings resolved, partially resolved, unresolved,
withdrawn or optional. Review changed passages for regressions. Compare model contributions only after deduplicating
equivalent observations across findings, optional suggestions, limits and per-card notes.

## Current limits

Source records and structural checks are not native-speaker certification or exhaustive historical analysis.
Dual-model usefulness is an observation about the reviewed sample, not proof that model bias has been eliminated.
The pilot's initial and changed-passage GPT/Claude reports are preserved in the review ledger. They found complementary
issues, but the reports also contained unsupported frequency inferences and each missed something the other established.
Both confirmed the corrected passages without an actionable remaining defect in that scope.

Reviewer file permissions are separate from tool permissions: `--allow-all-tools` alone did not authorize a diff in the
parent session's artifact directory. The event record showed a noninteractive path-approval failure, not content exclusion.
Grant only that artifact directory with `--add-dir`. Reviewer session IDs can be recovered from the local session store
for same-task follow-up; `--resume` and `--trust-folder` cannot be combined. Exit each resumed process before the next.
