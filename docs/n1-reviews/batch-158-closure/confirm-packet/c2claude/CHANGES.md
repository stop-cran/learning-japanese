# Batch 158 revision: what changed from 6605a8b0 to ccc046bb

Your confirmation report reviewed `6605a8b0`. The revised snapshot is `ccc046bb`, one commit later; its parent is `6605a8b0`. The range has no merges. Both commits are signed with key 9D94B9D311BD26A7 (`evidence\verify-commit.txt`). This revision answers your confirmation report only; no other confirmation report had been received when it was made.

- **Changed:**
  - the word article `words/升.md` (two body lines);
  - the ledger `docs/n1-sources/batch-158-progress.json` (one line);
  - the pinned JMdict selection `docs/n1-sources/batch-158-jmdict-selection.json` and extract `docs/n1-sources/batch-158-jmdict.xml`, which gain one complete entry, 1288370 (腰掛け).
- **Unchanged:**
  - all ten batch kanji cards;
  - the other nine word articles, and the front matter of `words/升.md` (title, tags and `quiz_exclusions`);
  - `tools/`, every stroke file and every other file.
- **Generated file:** `manifest.json` is regenerated (contentVersion `d5b0861e10d1bf24`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `words/升.md` | 28 | The Synonyms paragraph adds one sentence at its end: “[腰掛け](腰掛け.md) (こしかけ) is a seat or bench (JMdict entry 1288370); in its second sense, 升 is a whole box of seating, such as a 升席, not a single seat or bench.” The two sentences before it (箱 and 容器) are unchanged. |
| | 34 | The Dictionary line now ends “compare entries 2248100, 1706800 and 1288370” (was “compare entries 2248100 and 1706800”). |
| `docs/n1-sources/batch-158-progress.json` | 1053 | `batchAudit` says “87 complete JMdict families” (was 86). |
| `docs/n1-sources/batch-158-jmdict-selection.json` | 88 | adds the id `1288370`. |
| `docs/n1-sources/batch-158-jmdict.xml` | 32 added lines | the complete entry 1288370, copied unmodified from the pinned JMdict input by `tools\extract_n1_jmdict.py`. |

## Sources for the new sentence

The complete entries are in `evidence\jmdict-cited-entries.xml`.

- **1288370 腰掛け:** sense 1 “seat; bench”; sense 2 “temporary job while looking for a better job or until one marries”. The word article `words\腰掛け.md` has the title “seat; bench”.
- **1346290 升:** sense 2 “box (seating at a theatre, etc.)”.
- **1706800 升席:** “tatami "box seat" for four people at sumo, kabuki, etc.” The phrase “a whole box of seating … not a single seat” rests on this “for four people”.

## Word-quiz options (`evidence\word-quiz.txt`)

- **No option changed.** The front matter of every word article is unchanged, so every block is the same as at `6605a8b0`; only the header line naming the commit differs.
- **The word 升** (block from line 1690): the nine exclusions, including 腰掛け “seat; bench”, are at line 1692. 俵 is the one candidate above the last slot (score 7); 668 words tie at score 5.
- **Why 腰掛け is excluded and 席, 座席 and 客席 are not:** `evidence\Words.kt` lines 197–199 score a candidate as 2 per shared tag, plus 1 for the same type and 1 for a shared kanji.
  - 腰掛け (type wago; tags wago, noun, furniture, posture) shares wago and noun with 升 and has its type: score 5. Without the exclusion it would be one of the 668 tied words, any two of which can be drawn.
  - 席, 座席 and 客席 are type kango and share only the tag noun: score 2, below the last slot. None of them can be drawn for 升.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `6605a8b0`, except the numbers named here.

- **audit** (`tools\audit_n1_batch.py --batch 158`): exit 0; 87 complete JMdict families (was 86); the manifest is fresh (`d5b0861e10d1bf24`).
- **budget:** retained 56,811,698 bytes, inflated 57,247,770 and local ZIP 36,498,291 (+191 retained bytes from `6605a8b0`). The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **quiz-safety, reading-exposure and reading-options:** unchanged; no kanji card or word front matter changed.
- **lint:** exit 1 with the same 4 errors and 59 warnings as at `6605a8b0`. The errors are on the reused cards 師, 観 and 負: metadata readings with no Readings row. The batch adds only a word link to each of these three cards.
- **Other checks:** manifest rebuild identical; diffcheck clean from the batch base `ad1694c1`; validate 0 errors; unittest 439 tests OK; vocabulary 3201/3539.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Process notes

- **Amends before review:** `ccc046bb` was amended in place several times before any review, and each version was signed. Only the final `ccc046bb` is in this range.
  - The new sentence first stood as its own paragraph. It was folded into the existing Synonyms paragraph, as in the other nine words, so no other line number moved.
  - The ledger's family count was then corrected from 86 to 87.
