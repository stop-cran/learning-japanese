# Batch 159 revision: what changed from f85ff382 to 0ba7df63

The revised snapshot is `0ba7df63`, “N1 B159: correct the ledger's lint warning count”, one commit whose parent is `f85ff382`. The range has no merges. Every commit from the reviewed freeze `1a9bb910` through `0ba7df63` is signed with key D4C9A275A218AF747B787AFA9D94B9D311BD26A7 (`evidence\verify-commit.txt`).

This revision answers finding 1 of your confirmation report on `f85ff382`. No other confirmation report on `f85ff382` exists: the other reviews of this round are made on `0ba7df63` directly.

`RESPONSE.md` answers your own report only.

- **Changed:** the ledger `docs/n1-sources/batch-159-progress.json`, line 948 (`mechanicalChecks.n1Lint`). The sentence “Of the 37 warnings, 35 are on reused cards and words.” becomes: “Of the 42 warnings, 40 are on reused cards and words. They report a missing N1 source-index entry, quiz reading list or Metadata line, or a missing Dictionary line or one that cites no JMdict entry id; B159 changes none of these fields, because it only adds or links one Common words line on each of those cards and does not change those word articles.” The rest of the statement is unchanged.
- **Unchanged:** every card, every word article, the rest of the ledger, `tools/`, the pinned JMdict selection and extract, and every other file.
- **Generated file:** `manifest.json` is rebuilt and unchanged (contentVersion `18c1f24ea8d2caf8`): the ledger is not app content.

## The new statement against the lint output

- `checks\lint.txt` ends “3 error(s), 42 warning(s)”. Two warnings are on `kanji/又.md` (the また examples または and また). The other 40 are on eight reused cards and twelve reused word articles:
  - 28 on the cards 不 味 太 官 情 服 母 贈: “not in the N1 source index; source comparison skipped” (8), “no quizOnyomi” (8), “no quizKunyomi” (8) and “no Metadata: line” (4: 不 味 服 母);
  - 12 on the word articles お母さん 不潔 不規則 不運 味 和服 太る 太鼓 官庁 服 洋服 調味料: “no Dictionary: line” (5: お母さん 味 太る 服 洋服) and “Dictionary: line cites no JMdict entry id” (7).
- `evidence\reused-lint-diff.txt` (new) shows everything B159 changes in those 20 files, from the batch base `2787e43b` to `0ba7df63`: seven cards gain one Common words line each, the existing 贈呈 line on `kanji/贈.md` gains a link, and none of the twelve word articles changes.

## Checks run on the revised snapshot (outputs in `checks\`)

Every output is identical to the `f85ff382` output apart from the header line (and the run time in `unittest.txt`).

- **audit** (`tools\audit_n1_batch.py --batch 159`): exit 0; 87 complete JMdict families; the manifest is fresh (`18c1f24ea8d2caf8`).
- **budget:** retained 56,881,426 bytes, inflated 57,317,498 and local ZIP 36,535,519. The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **quiz-safety:** 0 errors, 0 warnings. **reading-exposure:** 0 production hits, 0 padded-session hits. **reading-options:** 0 problems.
- **lint:** exit 1 with 3 errors (on the reused cards 太 and 情, present at the batch base `2787e43b`) and 42 warnings (listed above).
- **Other checks:** manifest rebuild identical; diffcheck clean from the batch base `2787e43b`; validate 0 errors; unittest 444 tests OK; vocabulary 3201/3539.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Evidence

- `evidence\verify-commit.txt` adds `git verify-commit -v 0ba7df63` and extends the `git log --show-signature` range to `0ba7df63`.
- `evidence\reused-lint-diff.txt` is new (see above).
- `evidence\jmdict-scan-c5.txt` and `evidence\support-selection.json` are identical to the earlier round's files.