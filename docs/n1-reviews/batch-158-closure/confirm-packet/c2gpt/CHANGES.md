# Batch 158 revision: what changed from ccc046bb to 348c4f70

The revised snapshot is `348c4f70`, one commit after `ccc046bb`, which is its parent. The range has no merges. Every commit from the reviewed freeze `60d2cd5a` through `348c4f70` is signed with key 9D94B9D311BD26A7 (`evidence\verify-commit.txt`).

This revision answers the confirmation reports on `ccc046bb`:
- two reviewers confirmed with no findings, each with an optional note;
- a third reviewer reported two minor findings (NEEDS FIX).

`RESPONSE.md` answers your own report only.

- **Changed:**
  - the kanji card `kanji/匿.md` (front matter, one line);
  - the word article `words/升.md` (one front-matter line and one body line);
  - the word article `words/勲章.md` (one body line, spelling only);
  - the ledger `docs/n1-sources/batch-158-progress.json` (two exclusion rows, regenerated from the front matter).
- **Unchanged:**
  - the other nine batch kanji cards;
  - the other eight word articles;
  - the pinned JMdict selection and extract (still 87 complete families; entry 1288370 stays because `words/升.md:28` still cites it);
  - `tools/`, every stroke file and every other file.
- **Generated file:** `manifest.json` is regenerated (contentVersion `810f3bd3fa524c7a`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `kanji/匿.md` | 14 | `quiz_exclusions: [隠, 秘, 密, 潜, 伏]`; 皮 removed. |
| `words/升.md` | 8 | `quiz_exclusions: [箱, 容器, 入れ物, ケース, 計る, 測定, 計, 容積]`; 腰掛け removed. |
| | 28 | The last sentence of the Synonyms paragraph is split in two at its semicolon: “[腰掛け](腰掛け.md) (こしかけ) is a seat or bench (JMdict entry 1288370). In its second sense, 升 is a whole box of seating, such as a 升席, not a single seat or bench.” The wording is otherwise unchanged. |
| `words/勲章.md` | 15 | “an honour awarded for service” becomes “an honor awarded for service”. The batch kanji card `kanji/勲.md` (lines 23 and 40) uses “honor”. Across `kanji/` and `words/`, 186 lines contain a word starting “honor” and 8 lines a word starting “honour”. |
| `docs/n1-sources/batch-158-progress.json` | 327–337, 427–434 | The word-exclusion row for 升 drops 腰掛け. The kanji-exclusion row for 匿 drops 皮. Both rows are generated from the front matter. |

## What did not change in the card text

- **`kanji/匿.md:40`** still contrasts 皮: “皮 (“skin; hide”) shares only the English word “hide,” there meaning an animal skin.” The sentence makes no claim about quiz options.
- **`words/升.md:28`** still contrasts 腰掛け, with JMdict 1288370. Line 34 still lists 1288370 among the compared entries.

## Quiz options

### Word quiz (`evidence\word-quiz.txt`)

- **The word 升** (block from line 1690):
  - It now lists 8 exclusions.
  - 俵 is still the one candidate above the last slot (score 7). 669 words tie at score 5 (was 668).
  - 腰掛け “seat; bench” is one of the 669 (line 2215). It shares the tags wago and noun and has the same type.
- **The reverse section** (from line 2478):
  - It lists no row for 腰掛け, as before.
  - Questions on 腰掛け cannot draw 升. 腰掛け's own options come from higher-scoring words; its tags furniture and posture are not tags of 升.
- **Every other block** is unchanged except the header line naming the commit.

### Kanji quiz (`checks\quiz-safety.txt`)

- 匿 has three curated distractors (父 魚 年), and 皮 has three (波 彼 坂, in `kanji/皮.md`).
- Each card's curated distractors fill all three wrong options of its meaning and reading questions, so neither card can draw the other, with or without the exclusion.
- The output is unchanged except its header line.

### Third-card questions

`evidence\QuizBuilder.kt` line 30 and `evidence\Words.kt` line 186 also keep an excluded pair apart as wrong options for a third card. With the two exclusions gone, a question on some other card can now show 匿 and 皮 together, or 升 and 腰掛け together, as wrong options. Both are then wrong, so no question gains a second correct answer.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `ccc046bb`, except the numbers named here.

- **audit** (`tools\audit_n1_batch.py --batch 158`): exit 0; 87 complete JMdict families; the manifest is fresh (`810f3bd3fa524c7a`, was `d5b0861e10d1bf24`).
- **budget:** retained 56,811,681 bytes, inflated 57,247,753 and local ZIP 36,498,287 (−17 retained bytes from `ccc046bb`). The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **quiz-safety, reading-exposure and reading-options:** unchanged apart from the header line.
  - reading-options still reports its 2 known over-reports, 傍 そう and 即 しょく.
  - reading-exposure still reports 0 hits and 4 latent collisions.
- **lint:** exit 1 with the same 4 errors and 59 warnings as at `ccc046bb`. The errors are on the reused cards 師, 観 and 負: metadata readings with no Readings row, present at the batch base `ad1694c1`.
- **Other checks:**
  - manifest rebuild identical;
  - diffcheck clean from the batch base `ad1694c1`;
  - validate 0 errors;
  - unittest 439 tests OK;
  - vocabulary 3201/3539.
- **JMdict extract:** `evidence\jmdict-check.txt` holds `tools\extract_n1_jmdict.py --check` run at `348c4f70`: “Verified 87 complete JMdict families”. The input and pin hashes match.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.
