# Batch 156 revision: what changed from a7cc61e2 to ba44b280

Revised snapshot: `ba44b2809e6f46a6532ad58a016cb9d639ad2afc`. Nothing is published.

- Your last confirmation report reviewed `a7cc61e27261c62e84c3bd1f28e8a9254d9dcb04`. After it, the author merged current main
  (`0697b768`) into the batch again: merge `eafee44b5129b283cd0e62d07303fd49d842204a`, whose first parent is `a7cc61e2`. The
  merge brought in 11 paths from main (an onomatopoeia word article, a grammar file, two docs, `REVIEW.md`, two scene
  catalogs, three images and `manifest.json`) and changed none of the batch's files: `evidence\merge-scope.txt` lists the 33
  paths that the batch's own commits add, change or delete, and shows that the merge's diff restricted to them is empty. So
  the batch text at `eafee44b` is the text at `a7cc61e2`.
- This revision is one commit on top of the merge. `diffs\fix.patch` is the exact patch from `eafee44b` to `ba44b280`
  (`manifest.json` excluded); `diffs\changed-lines.txt` lists the changed lines. The text at `a7cc61e2` is in your earlier
  confirmation packet's `snapshot\`.
- It changes three lines of one card, adds one word article and deletes one. No other card, word article, article or
  stroke file changed. `manifest.json` was regenerated; it is a generated index and outside the review.

| File | Line | Change |
| --- | --- | --- |
| kanji 乙 | 23 | Meaning: the last clause linked the 甲乙 article ("こうおつ pairs it with 甲: "first and second; A and B""); it now links the 乙種 article: "おつしゅ is "B-grade; second-class" (JMdict)". |
| kanji 乙 | 31 | オツ row: the linked word is 乙種 おつしゅ "B grade; second class" instead of 甲乙 こうおつ "first and second; A and B; relative merit". The row keeps the sentence on 乙 おつ (JMdict 1182940) and adds "and 甲乙 こうおつ pairs it with 甲 (JMdict entry 1280080)", unlinked. |
| kanji 乙 | 38 | Common words: 乙種 おつしゅ "B grade; second class" instead of 甲乙. |
| `words\乙種.md` | all | New article (41 lines); its full text is in `snapshot\words\`. |
| `words\甲乙.md` | all | Deleted. The text you reviewed is in your earlier confirmation packet's `snapshot\words\`. |

Nothing else on the 乙 card changed. Its Notes line 42 still names 乙種 and 甲乙 as the Joyo table's examples, and its
Metadata line 60 already listed 1862630 (乙種) and 1280080 (甲乙). No other file in the repository links `words/甲乙.md` (`evidence\link-scan.txt`, a `git grep` of the whole revision).
Among the other cards and word articles, two mention 甲乙, both only inside the longer word 甲乙丙丁: the 丁 card (line 57)
and the 丙 word article (line 28). Both are unchanged.

## Why

From this batch on, every kanji gets a supporting word article chosen by the rule in the proposal posted on issue #60
(point 2, quoted in `evidence\selection-evidence.md`). In brief: prefer a spelling with one of JMdict's common-word tags
news1, ichi1, spec1 or gai1; where none exists, an untagged word may be used with a justification reviewed for that row; the
word's other kanji must already have cards or join the same batch.

- **The author's selection error.** At freeze the author treated news2 and spec2 as qualifying tags as well, so no row was
  flagged for justification. Rechecked against the list, seven of the ten words carry a listed tag (丹念, 亜熱帯, 仁, 歌舞伎,
  降伏, 伐採, 同伴); 甲乙, 仙人 and 伯仲 carry only news2 and spec2. Their rows therefore need the per-row justification that
  the rule asks for, and none was given. `evidence\candidates.md` lists the tagged candidates for 乙, 仙 and 伯.
- **甲乙 also fails a requirement that does not depend on tags:** its other kanji 甲 has no card in the repository and is not
  in this batch. So 甲乙 is replaced. `RESPONSE.md` item A1 explains why 乙種 was chosen and why the two tagged candidates
  (乙 alone and 早乙女) were not.
- 仙人 and 伯仲 meet every hard requirement. They are kept, and `RESPONSE.md` items A2 and A3 give the row justifications for
  review.

## Checks run on the revised snapshot (outputs in `checks\`)

- **`lint.txt`:** 0 errors, 1 warning (`words/潜る.md`: the Dictionary line cites no JMdict entry id), as before.
  **`unittest.txt`:** 439 tests, OK. **`validate.txt`:** 0 errors. **`linkplan.txt`:** 0 problems; its line for the new
  article reads "NEW ARTICLE: words/乙種.md declares 乙種; unlinked batch kanji: none" where the 甲乙 line used to be.
  **`kanji-remarks.txt`:** 0 problems; it now compares with main at the merge (`0697b768`) instead of `9766dbd5`.
- **`vocabulary.txt`:** one line more than in your earlier packet:
  "onomatopoeia-next-100-cohort-7.json:onoma-c7-nechinechi-criticism: prompt/context changed; vocabulary review is stale".
  The file is main's (`grammar/onomatopoeia-next-100-cohort-7.json`, brought in by the merge; see `evidence\merge-scope.txt`)
  and no batch file is read by this check. Main's own CI fails the same way at `0697b768`: GitHub Actions run 44933684389
  (https://github.com/stop-cran/learning-japanese/actions/runs/44933684389), step "Run python tools/grammar_vocabulary.py
  check". The batch does not fix it; the owner's main branch is red until it is fixed there.
- **`manifest.txt`:** rebuilding `manifest.json` leaves it unchanged and the tree clean.
- **`budget.txt`:** informational. Retained bytes are 56,679,021, 70,112 more than at `a7cc61e2`. The merge accounts for
  70,430 of that (the author's run at `eafee44b`, `evidence\budget-at-merge.txt`: 56,679,339), and this revision for -318.
- **`quiz-safety.txt`:** byte-identical to your earlier confirmation packet's `checks\quiz-safety.txt` (at `a7cc61e2`); the
  file has no command line. **`reading-exposure.txt`, `reading-options.txt`:** identical to your earlier packet's copies
  except line 1, which names the revision; the command's arguments on that line are unchanged. These audits read the cards'
  reading rows, and no reading row's reading or selection changed.
- **`evidence\word-quiz.txt`:** the word-quiz option audit rerun at `ba44b280`. Against your earlier packet's copy (at
  `a7cc61e2`) every difference comes from replacing 甲乙 with 乙種:
  - line 2 (the command) names 乙種 instead of 甲乙;
  - lines 74-86 are the 乙種 section, replacing the 甲乙 section;
  - line 179: 乙種 is listed among 仁's scored candidates at score 5; 甲乙's line in the same list (old line 1038) is gone;
  - line 2133, in the 伯仲 section: "excluded from the other side" now reads "none"; before, it named 甲乙, whose quiz
    exclusions included 伯仲;
  - the reverse meaning lines (2421 onward): 1,150 pairs instead of 1,158; the 甲乙 lines are replaced by the 乙種 lines
    2543-2598; several tie counts for 丹念 and 伯仲 drop by one;
  - the reverse reading lines (3572 onward): 72 pairs instead of 70; 甲乙 shown for 諺 is replaced by 乙種 shown for 一種,
    人種 and 種.
- **`evidence\meta-scan-after.txt`:** the Metadata-id scan at `ba44b280`: no whole-run gap, and the same four part-of-run
  matches as at `a7cc61e2` (熱帯 in 亜熱帯, 歌舞 in 歌舞伎, 伏せ in 伏せる, 母さん in 伯母さん). It reads the cards only.
- **JVM tests:** the Android JVM tests that read the real content were not run (no JDK on this machine).

## Process notes

- The checks in `checks\` and the evidence audits were run on the committed revision `ba44b280`.
- The packet builder's list of batch paths, used to check the merge, now comes from the batch's own commits on the first-parent
  line, with merges of main excluded. Before, it came from a diff from the batch's base and so would also have counted the
  102 paths that the earlier merge `e37ad00b` brought in from main. The new list has one path more than the old one would
  have: `words/乙.md`, which `c6afa163` added and `7eaf5c24` deleted.
