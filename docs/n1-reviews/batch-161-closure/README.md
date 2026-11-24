# Batch 161: textual-review reconciliation

**Status:** The reported findings were reconciled, and the content commit is published with matching
CI and exact ZIP/runtime verification. This is not Android, phone, native-speaker or general-release
acceptance; see [`batch-161-publication`](../batch-161-publication/provenance.json).

## Candidate snapshots

- Baseline: `e824da99c8a19479bfede4e6fbe88b1f21a4180b`.
- Initial reviewed commit: `bac3477e5323fad11c54e2f2bd424cd5c3693096`.
- Revised snapshot: that commit plus the working-tree changes recorded by
  `reviewedSnapshotDiffSha256` in [`provenance.json`](provenance.json). The hash covers the full
  baseline-to-candidate binary diff, excluding this closure archive to avoid a self-referential hash.
- Revised manifest content version: `09243c4be32646a3`.

The original reports are preserved under [`reports/`](reports/). Machine-specific absolute paths
were normalized to repository-relative paths; findings, evidence, scope and limitations are retained.

## Reviewers

| Report | Runtime model | Original facet |
|---|---|---|
| [`r1-claude.md`](reports/r1-claude.md) | Claude Sonnet 5.5 | Correctness and scoped coverage |
| [`r2-gpt.md`](reports/r2-gpt.md) | GPT-6.2 Sol | Consistency and quiz safety |
| [`r3-grok.md`](reports/r3-grok.md) | Grok 4.7 | Comprehensibility and scoped coverage |

Model names are from the agent execution records. These were synchronous, one-shot agent tasks.
Post-fix messages were rejected by the runtime, so no independent follow-up reports were obtained.
[`reconciliation.md`](reconciliation.md) records the author's direct post-fix check against each
original finding and its evidence; it does not represent reviewer confirmation.

## Checks and boundaries

The revised candidate passed:

- `python -X utf8 -B tools/validate.py` — 0 errors.
- `python -X utf8 -B tools/build_manifest.py` — 9,902 runtime files; manifest is fresh.
- `python -X utf8 -B tools/audit_n1_batch.py --batch 161` — 10 kanji, 9 new words, 11 changed
  reused articles, 18 required reciprocal support pairs, 25 reading dispositions, 132 dictionary
  families; exact baseline runtime preserved outside recorded changes.
- `python -X utf8 -B tools/check_content_budget.py` — 9,909 files / 9,925 entries; 57,018,225
  retained bytes; 57,454,297 inflated bytes; 36,609,817 local ZIP bytes.
- `git diff --check` — passed; Git emitted only the existing manifest LF-to-CRLF warning.

The progress ledger and full source records are in
[`docs/n1-sources`](../../n1-sources/), especially
[`batch-161-progress.json`](../../n1-sources/batch-161-progress.json) and the pinned
[`batch-161-jmdict.xml`](../../n1-sources/batch-161-jmdict.xml). The review is textual and
source-bounded; it does not establish runtime or device acceptance.
