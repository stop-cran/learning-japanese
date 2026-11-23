# Batch 156 revisions: what changed from 3c5ef845 to ba44b280

Revised snapshot: `ba44b2809e6f46a6532ad58a016cb9d639ad2afc`. Nothing is published.

Your last confirmation report reviewed `3c5ef8450e38051682dab2bea5fce320b992e5ea`. Since then the batch line has four
commits, each a child of the one before:

| Commit | Kind | Batch files changed | Where to review it |
| --- | --- | --- | --- |
| `e37ad00b` | merge of main (`9766dbd5`) | none | `evidence\merge-scope-e37ad00b.txt` |
| `a7cc61e2` | revision: JMdict ids on Metadata lines | five cards, one line each | `diffs\intermediate.patch`; section 2 |
| `eafee44b` | merge of main (`0697b768`) | none | `evidence\merge-scope.txt` |
| `ba44b280` | revision: the 乙 word 甲乙 replaced by 乙種 | the 乙 card (3 lines); one word article added, one deleted | `diffs\fix.patch`; section 3 |

The text at `3c5ef845` is in your earlier confirmation packet's `snapshot\`. `manifest.json` was regenerated at each step;
it is a generated index and outside the review.

## 1. The two merges of main

- **`e37ad00b`** (full id `e37ad00b796ed16dc752f5e60f0fd119f14dfa5e`; first parent `3c5ef845`, second parent `9766dbd5`,
  main at the time) brought in 102 paths from main. `evidence\merge-scope-e37ad00b.txt` lists every path the batch had added
  or changed since its base `0638544c`, shows that the merge's diff restricted to those paths is empty, and lists the 102
  paths.
- **`eafee44b`** (full id `eafee44b5129b283cd0e62d07303fd49d842204a`; first parent `a7cc61e2`, second parent `0697b768`,
  main at the time) brought in 11 paths: an onomatopoeia word article, a grammar file, two docs, `REVIEW.md`, two scene
  catalogs, three images and `manifest.json`. `evidence\merge-scope.txt` lists the 33 paths that the batch's own commits add,
  change or delete, and shows that the merge's diff restricted to them is empty.

So neither merge changed batch text: the batch text at `e37ad00b` is the text at `3c5ef845`, and at `eafee44b` the text at
`a7cc61e2`.

## 2. Intermediate revision `a7cc61e2`: JMdict ids on five Metadata lines

`diffs\intermediate.patch` is the exact patch from `3c5ef845` to `a7cc61e2`, restricted to the batch's paths (main's content
merged in between is excluded). Five kanji cards changed, each on one line only: its Metadata line. No other line of any
card, no word article, article or stroke file changed.

| File | Line | Change |
| --- | --- | --- |
| kanji 乙 | 60 | Metadata line: JMdict entry 1862630 (乙種) inserted after 1182945, before 2855480 (乙女). |
| kanji 亜 | 53 | Metadata line: JMdict entry 1149860 (亜麻) appended. |
| kanji 仁 | 55 | Metadata line: JMdict entry 1369740 (仁術) appended. |
| kanji 仙 | 51 | Metadata line: JMdict entries 1387150 (仙骨) and 1329130 (酒仙) appended. |
| kanji 伯 | 53 | Metadata line: JMdict entry 2261500 (伯母さん) appended. |

Nothing else on these lines changed: the KANJIDIC2 note, the Digital Daijisen, Kanjipedia and Joyo-table links are as before.

Why: the repository's authoring rule since batch 138 is that a card's Metadata line lists the JMdict entry of every word the
card names; the author's `meta_scan.py` (`evidence\meta_scan.py`) checks it before freeze. It checks whole runs of Japanese
script that contain a kanji, so it does not check kana-only or single-kanji words. At the frozen snapshot the scan found six
named words without their entry on the Metadata line; the original packet's `mechanical-checks.md`, section "card Metadata
entry ids (meta scan)", lists them. The author did not fix them before freeze. `evidence\meta-scan-before.txt` is the scan at
the merge `e37ad00b` (batch text identical to `3c5ef845`), and `evidence\meta-scan-after.txt` the scan at `ba44b280`.

| Word | Where the card names it (unchanged line) | JMdict entry | Written forms; reading | Gloss (pinned JMdict) |
| --- | --- | --- | --- | --- |
| 乙種 | 乙:42, the Joyo table's example words | 1862630 | 乙種; おつしゅ | "B-grade; second-class" |
| 亜麻 | 亜:40, the Joyo table's example words | 1149860 | 亜麻; あま, アマ | "flax (Linum usitatissimum); linseed" |
| 仁術 | 仁:41, the Joyo table's example words | 1369740 | 仁術; じんじゅつ | "benevolent act; healing act" |
| 仙骨 | 仙:40, the Joyo table's example words | 1387150 | 仙骨, 薦骨; せんこつ | "sacrum; sacral bone" / "hermitry; appearance of a hermit; ..." |
| 酒仙 | 仙:40, the Joyo table's example words | 1329130 | 酒仙; しゅせん | "heavy drinker" |
| 伯母さん | 伯:33 and 伯:38, links to the existing article | 2261500 | 伯母さん, 叔母さん; おばさん | "aunt" |

The complete entries are in `evidence\jmdict-cited-entries.xml`. In the pinned JMdict each of the six written forms belongs
to exactly one entry; 仙骨's single entry 1387150 carries both senses. The cards name the five Joyo example words only as
written forms, with no reading or meaning. 伯 gives 伯母さん the reading おばさん (lines 33 and 38) and the meaning "aunt"
(line 38), both as in entry 2261500.

After the fix the scan reports no whole-run gap. It still reports four "part-of-run" matches: a shorter dictionary word found
inside a longer word that the card names (熱帯 in 亜熱帯, 歌舞 in 歌舞伎, 伏せ in 伏せる, 母さん in 伯母さん). The longer words'
own entries are on the Metadata lines, and the shorter words are not named on the cards, so they are not added.

## 3. This revision `ba44b280`: the 乙 word 甲乙 replaced by 乙種

`diffs\fix.patch` is the exact patch from `eafee44b` to `ba44b280` (`manifest.json` excluded); `diffs\changed-lines.txt`
lists the changed lines. It changes three lines of one card, adds one word article and deletes one. No other card, word
article, article or stroke file changed.

| File | Line | Change |
| --- | --- | --- |
| kanji 乙 | 23 | Meaning: the last clause linked the 甲乙 article ("こうおつ pairs it with 甲: "first and second; A and B""); it now links the 乙種 article: "おつしゅ is "B-grade; second-class" (JMdict)". |
| kanji 乙 | 31 | オツ row: the linked word is 乙種 おつしゅ "B grade; second class" instead of 甲乙 こうおつ "first and second; A and B; relative merit". The row keeps the sentence on 乙 おつ (JMdict 1182940) and adds "and 甲乙 こうおつ pairs it with 甲 (JMdict entry 1280080)", unlinked. |
| kanji 乙 | 38 | Common words: 乙種 おつしゅ "B grade; second class" instead of 甲乙. |
| `words\乙種.md` | all | New article (41 lines); its full text is in `snapshot\words\`. |
| `words\甲乙.md` | all | Deleted. The text you reviewed is in your earlier confirmation packet's `snapshot\words\`. |

Nothing else on the 乙 card changed in this revision. Its Notes line 42 still names 乙種 and 甲乙 as the Joyo table's
examples, and its Metadata line 60 lists 1862630 (乙種, added by `a7cc61e2`) and 1280080 (甲乙). No other file in the
repository links `words/甲乙.md` (`evidence\link-scan.txt`, a `git grep` of the whole revision). Among the other cards and word articles, two mention 甲乙, both only inside the longer word
甲乙丙丁: the 丁 card (line 57) and the 丙 word article (line 28). Both are unchanged.

### Why

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

Compared with your earlier confirmation packet (at `3c5ef845`):

- **`lint.txt`:** 0 errors, 1 warning (`words/潜る.md`: the Dictionary line cites no JMdict entry id), as before.
  **`unittest.txt`:** 439 tests, OK. **`validate.txt`:** 0 errors. **`linkplan.txt`:** 0 problems; its line for the new
  article reads "NEW ARTICLE: words/乙種.md declares 乙種; unlinked batch kanji: none" where the 甲乙 line used to be.
  **`kanji-remarks.txt`:** 0 problems; it now compares with main at the latest merge (`0697b768`) instead of the batch's base
  `0638544c`.
- **`vocabulary.txt`:** one line more than in your earlier packet:
  "onomatopoeia-next-100-cohort-7.json:onoma-c7-nechinechi-criticism: prompt/context changed; vocabulary review is stale".
  The file is main's (`grammar/onomatopoeia-next-100-cohort-7.json`, brought in by the merge `eafee44b`; see
  `evidence\merge-scope.txt`) and no batch file is read by this check. Main's own CI fails the same way at `0697b768`: GitHub
  Actions run 44933684389 (https://github.com/stop-cran/learning-japanese/actions/runs/44933684389), step "Run python
  tools/grammar_vocabulary.py check". The batch does not fix it; the owner's main branch is red until it is fixed there.
- **`manifest.txt`:** rebuilding `manifest.json` leaves it unchanged and the tree clean.
- **`budget.txt`:** informational. Retained bytes are 56,679,021, 107,035 more than at `3c5ef845` (56,571,986). By step, from
  the author's runs: the merge `e37ad00b` +36,869 (`evidence\budget-at-merge-e37ad00b.txt`: 56,608,855); `a7cc61e2` +54 (the
  six ids with their separators, 9 bytes each); the merge `eafee44b` +70,430 (`evidence\budget-at-merge.txt`: 56,679,339);
  this revision -318.
- **`quiz-safety.txt`:** byte-identical to your earlier packet's `checks\quiz-safety.txt`; the file has no command line.
  **`reading-exposure.txt`, `reading-options.txt`:** identical to your earlier packet's copies except line 1, which names the
  revision; the command's arguments on that line are unchanged. These audits read the cards' reading rows, and no reading
  row's reading or selection changed.
- **`evidence\word-quiz.txt`:** the word-quiz option audit rerun at `ba44b280`. The audit at `a7cc61e2` was byte-identical to
  your earlier packet's copy (at `3c5ef845`), although the merge `e37ad00b` changed the `quiz_exclusions` line of 29 of
  main's word articles and the `tags` line of 2. Against your earlier packet's copy every difference comes from replacing
  甲乙 with 乙種:
  - line 2 (the command) names 乙種 instead of 甲乙;
  - lines 74-86 are the 乙種 section, replacing the 甲乙 section;
  - line 179: 乙種 is listed among 仁's scored candidates at score 5; 甲乙's line in the same list (old line 1038) is gone;
  - line 2133, in the 伯仲 section: "excluded from the other side" now reads "none"; before, it named 甲乙, whose quiz
    exclusions included 伯仲;
  - the reverse meaning lines (2421 onward): 1,150 pairs instead of 1,158; the 甲乙 lines are replaced by the 乙種 lines
    2543-2598; several tie counts for 丹念 and 伯仲 drop by one;
  - the reverse reading lines (3572 onward): 72 pairs instead of 70; 甲乙 shown for 諺 is replaced by 乙種 shown for 一種,
    人種 and 種.
- **`evidence\meta-scan-before.txt`, `evidence\meta-scan-after.txt`:** see section 2.
- **JVM tests:** the Android JVM tests that read the real content were not run (no JDK on this machine).

## Process notes

- The checks in `checks\` and the evidence audits were run on the committed revision `ba44b280`.
- The packet builder's list of batch paths, used to check the merge `eafee44b` and to build `diffs\intermediate.patch`, now
  comes from the batch's own commits on the first-parent line, with merges of main excluded. Before, it came from a diff from
  the batch's base and so would also have counted the 102 paths that the merge `e37ad00b` brought in from main. The new list
  has one path more than the old one would have: `words/乙.md`, which `c6afa163` added and `7eaf5c24` deleted.
