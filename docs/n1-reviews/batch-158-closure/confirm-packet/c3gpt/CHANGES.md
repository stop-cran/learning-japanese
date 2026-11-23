# Batch 158 revision: what changed from 348c4f70 to ef00345d

The revised snapshot is `ef00345d`, one commit after `348c4f70`, which is its parent. The range has no merges. Every commit from the reviewed freeze `60d2cd5a` through `ef00345d` is signed with key 9D94B9D311BD26A7 (`evidence\verify-commit.txt`).

This revision answers the confirmation reports on `348c4f70`. Two reviewers confirmed with no findings, and one of them added an optional note on the wording of `words/升.md:28`. A third reviewer found no defect but returned UNVERIFIED because it could not check the signed objects, the manifest or the kanji-reading builder itself. `RESPONSE.md` answers your own report only.

- **Changed:** the word article `words/升.md` (one body line, wording only).
- **Unchanged:**
  - all ten batch kanji cards;
  - the other nine word articles;
  - the ledger `docs/n1-sources/batch-158-progress.json`;
  - the pinned JMdict selection and extract (still 87 complete families);
  - `tools/`, every stroke file and every other file.
- **Generated file:** `manifest.json` is regenerated (contentVersion `cdd61116919da088`, was `810f3bd3fa524c7a`) and left out of `diffs\`. Only two of its lines change: the `contentVersion` and the SHA-256 of `words/升.md`.
- **Line numbers** below are in the revised snapshot.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `words/升.md` | 28 | The last sentence of the Synonyms paragraph, “In its second sense, 升 is a whole box of seating, such as a 升席, not a single seat or bench.”, becomes “The second sense of 升 is a whole box of seating, such as a 升席, not a single seat or bench.” The preceding sentence is about 腰掛け, so “its” could be read as 腰掛け; the new wording names 升 first. Nothing else on the line changes. |

## Quiz options

The change is in an article body, which no quiz reads. No front matter, title, exclusion or distractor changed.

- `checks\quiz-safety.txt`, `checks\reading-exposure.txt` and `checks\reading-options.txt` are unchanged apart from their header lines.
- `evidence\word-quiz.txt`, `evidence\distractor-use.tsv`, `evidence\distractor-senses.txt`, `evidence\corpus-attested.txt` and `evidence\meta-scan.txt` are unchanged apart from the line naming the commit.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `348c4f70`, except the numbers named here.

- **audit** (`tools\audit_n1_batch.py --batch 158`): exit 0; 87 complete JMdict families; the manifest is fresh (`cdd61116919da088`).
- **budget:** retained 56,811,680 bytes, inflated 57,247,752 and local ZIP 36,498,286 (1 byte less than at `348c4f70` in each). The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **manifest:** a rebuild at `ef00345d` leaves `manifest.json` byte-identical (SHA-256 `D98BB0FB…`, before and after) and the tracked tree clean.
- **lint:** exit 1 with the same 4 errors and 59 warnings as at `348c4f70`. The errors are on the reused cards 師, 観 and 負: metadata readings with no Readings row, present at the batch base `ad1694c1`.
- **Other checks:**
  - diffcheck clean from the batch base `ad1694c1`;
  - validate 0 errors;
  - unittest 439 tests OK;
  - vocabulary 3201/3539.
- **quiz-safety, reading-exposure and reading-options:** reading-options still reports its 2 known over-reports, 傍 そう and 即 しょく; reading-exposure still reports 0 hits and 4 latent collisions.
- **JMdict extract:** `evidence\jmdict-check.txt` holds `tools\extract_n1_jmdict.py --check` run at `ef00345d`: “Verified 87 complete JMdict families”. The input and pin hashes match.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.
