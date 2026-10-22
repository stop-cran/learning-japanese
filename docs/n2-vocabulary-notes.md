# N2 vocabulary authoring notes

## Scope and plan

Cover all **1,812 rows** of `original_data/n2.csv` in the pinned
[Kraus distribution](https://github.com/stephenmk/yomitan-jlpt-vocab/tree/b062d4e38c4bdd0950ae1d4ec55f04b176182e03/original_data).
This is a named community list, not an official JLPT syllabus. The baseline is
`f1a93f249b78ae87c8233da1fbb48e92f02d4b44`: 3,273 word articles after the completed
[N2 kanji expansion](n2-review.md).

Use **20 consecutive source rows per batch**: 90 full batches and a final 12-row batch.
Split a batch if its lexical or review complexity requires it; do not increase concurrent work.
The [index](n2-vocabulary-sources.tsv), [snapshot](n2-vocabulary-snapshot.json), and
[review ledger](n2-vocabulary-review.md) distinguish pending, drafted, and review-closed work.
Source IDs use physical CSV lines, including the header: the first row is `N2:2`.

Initial navigation found 75 exact-filename candidates and 76 additional same-entry spelling
candidates. These **151 candidate rows are not verified coverage**. The other 1,661 rows
have neither candidate; none of these counts establishes the eventual number of new articles.
There are 1,808 distinct source forms and 1,794 supplied entry IDs, all present in the pinned JMdict.

## Batch sequence

1. Inspect the original rows, complete applicable dictionary entries, existing cards and comparisons.
   Establish the spelling, reading, intended sense, restrictions, and any uncertain source intent.
2. Author original teaching text or make a narrowly necessary addition to a reusable article.
   Record the exact mapping and dictionary senses; unresolved rows remain explicitly unresolved.
3. Add useful word-to-kanji and kanji-to-word links, check answer-label ambiguity, validate content,
   regenerate the manifest, and commit the authored snapshot as `stop-cran`.
4. Run independent GPT and Claude reviews **sequentially**, on the same frozen snapshot and scope,
   without sharing the other report or the author's adjudication. Each reviewer process must exit
   before the next starts; no nested agents or background reviewer pool.
5. Reconcile against evidence, fix supported defects, and obtain bounded changed-passage confirmation
   where needed. Archive reports, record model contributions and limitations, and commit closure.

The user authorized batch authoring and commits. The completed kanji branch was pushed separately;
this vocabulary branch starts from that completed work. A drafted or structurally valid row is not
review-closed merely because a commit exists.

## Authoring contract

The canonical [format](content-format.md#word-article), [source policy](jlpt-levels.md#vocabulary-baseline),
and [repository review guidance](../.github/copilot-instructions.md) remain authoritative.
These notes add project-specific decisions, not a replacement format or a linguistic validator.

- Preserve stable word IDs, primary readings, existing teaching, and easier sourced article levels.
  A source alias counts only if the article actually teaches the applicable spelling, reading and use.
- Preserve original source fields separately from selected teaching identities. A shared JMdict ID
  is not proof that every spelling accepts every reading or sense. Read `re_restr`, `re_nokanji`,
  `stagk`, `stagr`, spelling/readings flags, inherited parts of speech, and sense-local qualifications.
- Inspect complete relevant entry families, not the kanji project's abbreviated candidate cache.
  Sense indices are one-based within the **2026-10-21** JMdict snapshot. Additional senses do not
  acquire an N2 label merely because an article teaches them.
- Keep all written Han characters in `kanji`, including those without cards. Link every existing
  written component substantively. For a newly covered word containing an N2 kanji card, add or
  update a useful reciprocal example on that card, with the word article's actual reading.
  Other useful backlinks can update existing plain-text examples; do not invent constituent readings
  to accommodate an irregular whole-word reading.
- Inspect actual meanings behind candidate English labels, including ordinary secondary senses.
  Curate direct `quiz_exclusions` where two displayed answers are defensible; the relation is
  symmetric but not transitive. Identical titles already deduplicate. Shared topics alone do not
  justify an exclusion, and distinct wording alone does not establish semantic uniqueness.
- Examples need English translations and selective kana. Distinguish lexical recognition from
  frequency and naturalness; do not turn dictionary order, missing priority, or an unusual source
  spelling into a frequency claim.

## Review and evidence

The requester checks each report's Snapshot / Scope / Verdicts / Findings / Optional / Limits
contract and adjudicates recommendations. The repository validator enforces structure and links;
neither it nor a CLEAN model verdict certifies exhaustive linguistic correctness.
Review correctness, scoped coverage, and comprehensibility for every new article and changed passage.
An unchanged reused article is checked for the specific claimed source coverage, not silently
reported as a new whole-article review.

Record useful unique contributions, shared observations, unsupported findings, optional suggestions,
and evidence unavailable to a reviewer. Compare equivalent observations across the entire reports,
not only their Findings headings. This measures usefulness on the reviewed sample, not a model ranking.

Before each content commit run `python -X utf8 -B tools/validate.py`,
`python -X utf8 -B tools/build_manifest.py`, and the whitespace check; commit the manifest.
For final closure check every source row, preserved baseline identities/levels, exact spelling and
sense mappings, reciprocal N2 links, review coverage, deterministic manifest and commit authorship.

## Current limits and feedback

The initial inventory is navigation only; unworked rows have no selected teaching mapping.
Dictionary evidence establishes lexical identity, not an official modern level or every example's
idiomaticity. Pause consequential unresolved claims rather than manufacturing coverage.
These notes will accumulate grounded corrections from the actual batches.

Report concrete content or guidance gaps through
[repository issues](https://github.com/stop-cran/learning-japanese/issues), identifying the passage,
evidence and learning impact; issue creation requires authorization.

## Recorded lessons

- **Planning:** `揚げる` and `挙げる` have separate modern JMdict entries from the giving
  article `あげる`; matching kana is not adequate reuse evidence. The original source gloss
  remains in provenance even when its broad English wording needs correction.
- **Planning:** Source `明き` can map to stable `空き` only after explicit alias teaching is
  present. Source kana `あかんぼう` can reuse `赤ん坊` without changing its N4 label.
