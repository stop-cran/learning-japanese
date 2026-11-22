# N1 review records

This folder holds the review records of the N1 kanji batches. Each batch's progress file is
in [`../n1-sources/`](../n1-sources/). Batches 108–157 each have a `batch-N-closure/` record
(reports, prompts, packets, dispositions, merge proofs and limits) and a `batch-N-publication/`
receipt; `tools/n1_record_publication.py` writes the receipt for new batches.

`/docs` is `export-ignore`, so nothing here ships in the app archive or counts toward the
budgets in `tools/check_content_budget.py`.

## Pruned raw artifacts

On 2026-11-22, 5,998 raw artifacts (2,994,059,681 bytes) were removed from the folders of
batches 17–110:

| Kind | Files | Bytes |
| --- | ---: | ---: |
| Reviewer screenshots and rendered images (`*.png`) | 5,813 | 2,222,260,207 |
| Raw reviewer session transcripts (`*.jsonl`, `*.jsonl.gz`, `*.jsonl.factored.gz`) | 182 | 681,265,906 |
| Envelope archives in `batch-039…041-native/parent-receipts/` (`*.zip`) | 3 | 90,533,568 |

The current validation and publishing tools do not read them. Historical recipes that re-check
the old evidence, such as `batch-103-rendered-793/checkpoint-recipe.py`, need their inputs
restored first. The reports, artifact indexes and receipts that name the files are kept, and
5,991 of the 5,998 have their SHA-256 hash recorded in a kept file.

Three small files of the same kinds are kept because a kept record depends on them and no other
copy is in the tree: `batch-107-845-original-byte-evidence.zip` (the original CRLF bytes
described by `batch-107-845-byte-representation.json`) and the two Jōyō glyph crops in
`batch-110-closure/confirm-packet/common/evidence/`. The `pilot-*` files are also kept because
[`pilot-native-acceptance.md`](pilot-native-acceptance.md) links to its screenshots.

All removed files remain in Git history at `e2c25363`; for example:

    git ls-tree -r --name-only e2c25363 -- docs/n1-reviews/batch-075-native
    git restore --source=e2c25363 -- docs/n1-reviews/batch-075-native

This shrinks checkouts by about 2.8 GiB. History is not rewritten, so clone size is unchanged.
Batches after 110 committed none of these kinds of files.
