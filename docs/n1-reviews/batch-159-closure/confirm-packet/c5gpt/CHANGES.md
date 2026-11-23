# Batch 159 revision: what changed from 0ba7df63 to bad899ea

The revised snapshot is `bad899ea`, “N1 B159: correct the ledger's reading-options note”, one commit whose parent is `0ba7df63`. The range has no merges. Every commit from the reviewed freeze `1a9bb910` through `bad899ea` is signed with key D4C9A275A218AF747B787AFA9D94B9D311BD26A7 (`evidence\verify-commit.txt`).

This revision applies the first point of the Optional line of your confirmation report on `0ba7df63`. No other confirmation report on `0ba7df63` exists: the other reviews of this round are made on `bad899ea` directly.

`RESPONSE.md` answers your own report only.

- **Changed:** the ledger `docs/n1-sources/batch-159-progress.json`, line 953 (`mechanicalChecks.readingOptions`); see “The new reading-options statement” below. The rest of the ledger is unchanged.
- **Unchanged:** every card, every word article, the rest of the ledger, `tools/`, the pinned JMdict selection and extract, and every other file.
- **Generated file:** `manifest.json` is rebuilt and unchanged (contentVersion `18c1f24ea8d2caf8`): the ledger is not app content.

## The new reading-options statement

Ledger line 953 (`mechanicalChecks.readingOptions`) said: “lean reading_options.py with the same --extra list: 0 problems. The only informational note is 呉 ぐ, a KANJIDIC2 name-only reading offered by 供, 具, 工 and 求.” `bad899ea` changes it to: “lean reading_options.py with the same --extra list: 0 problems. Two informational notes concern KANJIDIC2 name-only readings that the tool marks as drawable from the fallback: 吉 き on the キツ prompt, offered by 28 cards (among them 気, 期 and 記), and 呉 ぐ on the ゴ prompt, offered by 供, 具, 工 and 求. On both prompts the curated options fill all three wrong slots in every outcome, so the fallback is never consulted, and reading_exposure.py lists both readings among the latent collisions.”

- `checks\reading-options.txt` has two informational notes (“info (can be drawn)”): line 74, on 吉's キツ prompt, for き, offered by 28 cards; and line 147, on 呉's ゴ prompt, for ぐ, offered by 供 具 工 求. Both notes are in the reading-options output of every round since the reviewed freeze `1a9bb910`; only the ledger sentence left out 吉 き.
- `checks\reading-exposure.txt` lines 82 and 175: on both prompts the curated options fill all three wrong slots in every outcome, and the fallback is never consulted. Lines 88 and 178 say that き and ぐ cannot be drawn in the N1 stack, All stack or Starter practice session pool; they are among the 10 latent collisions counted on line 186.

## Checks run on the revised snapshot (outputs in `checks\`)

Every output of the check runner is identical to the `0ba7df63` output apart from the header line (and the run time in `unittest.txt`). `checks\link-targets.tsv` is not a check output: the packet builder writes it for the changed lines of this packet's range only, so it differs between packets by design. In this packet it lists no links: its only changed line is in the ledger (“0 link(s) on changed lines”).

- **audit** (`tools\audit_n1_batch.py --batch 159`): exit 0; 87 complete JMdict families; the manifest is fresh (`18c1f24ea8d2caf8`).
- **budget:** retained 56,881,426 bytes, inflated 57,317,498 and local ZIP 36,535,519. The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **quiz-safety:** 0 errors, 0 warnings. **reading-exposure:** 0 production hits, 0 padded-session hits. **reading-options:** 0 problems.
- **lint:** exit 1 with 3 errors (on the reused cards 太 and 情, present at the batch base `2787e43b`) and 42 warnings (the counts in ledger line 948, unchanged in this revision).
- **Other checks:** manifest rebuild identical; diffcheck clean from the batch base `2787e43b`; validate 0 errors; unittest 444 tests OK; vocabulary 3201/3539.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Evidence

- `evidence\verify-commit.txt` adds `git verify-commit -v bad899ea` and extends the `git log --show-signature` range to `bad899ea`.
- `evidence\reused-lint-diff.txt` is regenerated for `bad899ea`; its diffs are identical to those of the earlier file, because `bad899ea` changes none of the 20 files.
- `evidence\jmdict-scan-c6.txt` and `evidence\support-selection.json` are identical to the earlier round's files.