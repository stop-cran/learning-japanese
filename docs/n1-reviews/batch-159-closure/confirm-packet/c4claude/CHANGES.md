# Batch 159 revision: what changed from 54b00e0c to bad899ea

The revised snapshot is `bad899ea`. The range `54b00e0c..bad899ea` has three commits and no merges:
- `f85ff382`, “N1 B159: apply a third-round review note” (parent `54b00e0c`);
- `0ba7df63`, “N1 B159: correct the ledger's lint warning count” (parent `f85ff382`);
- `bad899ea`, “N1 B159: correct the ledger's reading-options note” (parent `0ba7df63`).

Every commit from the reviewed freeze `1a9bb910` through `bad899ea` is signed with key D4C9A275A218AF747B787AFA9D94B9D311BD26A7 (`evidence\verify-commit.txt`). `diffs\fix.patch` and `diffs\changed-lines.txt` show the combined change from `54b00e0c`.

- `f85ff382` applies optional note 1 of your confirmation report on `54b00e0c`.
- `0ba7df63` answers another reviewer's confirmation report on `f85ff382`, which found one stale count in the ledger.
- `bad899ea` applies an optional note of that reviewer's confirmation report on `0ba7df63`: the ledger's reading-options statement (line 953) named only one of the two informational notes in `checks\reading-options.txt`.

`RESPONSE.md` answers your own report, and describes the changes made for the other review.

- **Changed:**
  - the existing card `kanji/母.md`, line 38 (Common words): “- [叔母](../words/叔母.md) しゅくぼ — aunt (a parent's younger sister)” becomes “- [叔母](../words/叔母.md) おば, also しゅくぼ — aunt (a parent's younger sister)”. The word order now matches `kanji/叔.md:34`, “[叔母](../words/叔母.md) おば, also しゅくぼ — aunt (written 叔母 when younger than one's parent)”;
  - the ledger `docs/n1-sources/batch-159-progress.json`, line 221: the `after` text of the changed reused passage for `kanji/母.md`, regenerated to match the new line;
  - the ledger, line 948 (`mechanicalChecks.n1Lint`): the sentence “Of the 37 warnings, 35 are on reused cards and words.” becomes: “Of the 42 warnings, 40 are on reused cards and words. They report a missing N1 source-index entry, quiz reading list or Metadata line, or a missing Dictionary line or one that cites no JMdict entry id; B159 changes none of these fields, because it only adds or links one Common words line on each of those cards and does not change those word articles.” The rest of the statement is unchanged;
  - the ledger, line 953 (`mechanicalChecks.readingOptions`): see “The new reading-options statement” below.
- **Unchanged:** every batch card, every word article, the rest of the ledger (including the selection statement, the support mappings and the status), `tools/`, the pinned JMdict selection and extract, and every other file.
- **Generated file:** `manifest.json` is regenerated (contentVersion `18c1f24ea8d2caf8`; was `523a882a9af5a7e3`) and left out of `diffs\`. `0ba7df63` and `bad899ea` do not change it: the ledger is not app content.

## The new statement against the lint output

- `checks\lint.txt` ends “3 error(s), 42 warning(s)”. Two warnings are on `kanji/又.md` (the また examples または and また). The other 40 are on eight reused cards and twelve reused word articles:
  - 28 on the cards 不 味 太 官 情 服 母 贈: “not in the N1 source index; source comparison skipped” (8), “no quizOnyomi” (8), “no quizKunyomi” (8) and “no Metadata: line” (4: 不 味 服 母);
  - 12 on the word articles お母さん 不潔 不規則 不運 味 和服 太る 太鼓 官庁 服 洋服 調味料: “no Dictionary: line” (5: お母さん 味 太る 服 洋服) and “Dictionary: line cites no JMdict entry id” (7).
- `evidence\reused-lint-diff.txt` (new) shows everything B159 changes in those 20 files, from the batch base `2787e43b` to `bad899ea`: seven cards gain one Common words line each, the existing 贈呈 line on `kanji/贈.md` gains a link, and none of the twelve word articles changes.

The lint reported 37 warnings through `4f8ebea7`. At `54b00e0c`, `kanji/母.md` (four warnings) and `words/お母さん.md` (one warning) entered the lint scope and the count became 42, but `54b00e0c` did not update the ledger sentence.

## The new reading-options statement

Ledger line 953 (`mechanicalChecks.readingOptions`) said: “lean reading_options.py with the same --extra list: 0 problems. The only informational note is 呉 ぐ, a KANJIDIC2 name-only reading offered by 供, 具, 工 and 求.” `bad899ea` changes it to: “lean reading_options.py with the same --extra list: 0 problems. Two informational notes concern KANJIDIC2 name-only readings that the tool marks as drawable from the fallback: 吉 き on the キツ prompt, offered by 28 cards (among them 気, 期 and 記), and 呉 ぐ on the ゴ prompt, offered by 供, 具, 工 and 求. On both prompts the curated options fill all three wrong slots in every outcome, so the fallback is never consulted, and reading_exposure.py lists both readings among the latent collisions.”

- `checks\reading-options.txt` has two informational notes (“info (can be drawn)”): line 74, on 吉's キツ prompt, for き, offered by 28 cards; and line 147, on 呉's ゴ prompt, for ぐ, offered by 供 具 工 求. Both notes are in the reading-options output of every round since the reviewed freeze `1a9bb910`; only the ledger sentence left out 吉 き.
- `checks\reading-exposure.txt` lines 82 and 175: on both prompts the curated options fill all three wrong slots in every outcome, and the fallback is never consulted. Lines 88 and 178 say that き and ぐ cannot be drawn in the N1 stack, All stack or Starter practice session pool; they are among the 10 latent collisions counted on line 186.

## Checks run on the revised snapshot (outputs in `checks\`)

Every output of the check runner is identical to the `54b00e0c` output apart from the header line (and the run time in `unittest.txt`), except these numbers: the audit and manifest outputs give contentVersion `18c1f24ea8d2caf8` (was `523a882a9af5a7e3`), and the budget grows by 13 retained bytes, 13 inflated bytes and 5 local ZIP bytes, from the 母.md:38 change. `checks\link-targets.tsv` is not a check output: the packet builder writes it for the changed lines of this packet's range only, so it differs between packets by design. In this packet it lists the one link on the changed line `母.md:38`, resolved.

- **audit** (`tools\audit_n1_batch.py --batch 159`): exit 0; 87 complete JMdict families; the manifest is fresh (`18c1f24ea8d2caf8`).
- **budget:** retained 56,881,426 bytes, inflated 57,317,498 and local ZIP 36,535,519. The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **quiz-safety:** 0 errors, 0 warnings. **reading-exposure:** 0 production hits, 0 padded-session hits. **reading-options:** 0 problems.
- **lint:** exit 1 with 3 errors (on the reused cards 太 and 情, present at the batch base `2787e43b`) and 42 warnings (listed above).
- **Other checks:** manifest rebuild identical; diffcheck clean from the batch base `2787e43b`; validate 0 errors; unittest 444 tests OK; vocabulary 3201/3539.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Evidence

- `evidence\verify-commit.txt` adds `git verify-commit -v` for `f85ff382`, `0ba7df63` and `bad899ea` and extends the `git log --show-signature` range to `bad899ea`.
- `evidence\reused-lint-diff.txt` is new (see above).
- `evidence\jmdict-scan-c6.txt` and `evidence\support-selection.json` are identical to the earlier round's files.