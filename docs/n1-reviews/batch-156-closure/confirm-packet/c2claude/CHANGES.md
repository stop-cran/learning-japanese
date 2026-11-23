# Batch 156 second revision: what changed from 395f5364 to 3c5ef845

Revised snapshot: `3c5ef8450e38051682dab2bea5fce320b992e5ea`, a child of the earlier revision
`395f53643988ba24f444a376187c803aa6794654`, which the earlier confirmation round reviewed. That revision descends from the
initially reviewed snapshot `c6afa16315d5a88b5045eeb85d429b8f7fd90b1f`. Nothing is published.

- One file changed: the word article 甲乙 (`snapshot\words\甲乙.md`), on lines 16, 18-20 and 25. No kanji card, stroke file or
  other word article changed, and the article's front matter (lines 1-10) is unchanged. No line was added or removed.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- The text at `395f5364` is in the earlier confirmation packet's `snapshot\words\甲乙.md`. `diffs\fix.patch` is the exact patch
  from `395f5364` to `3c5ef845` (`manifest.json` excluded); `diffs\changed-lines.txt` lists the changed lines.

| File | Line | Change |
| --- | --- | --- |
| words 甲乙 | 16 | The sentence "In a contract, 甲 labels the first party and 乙 the second, so 甲乙 can name both parties together." is removed. The rest of the paragraph is unchanged. |
| words 甲乙 | 18-20 | The first example was `契約書は二通作り、甲乙が一通ずつ持ちます。` (けいやくしょはにつうつくり、こうおつがいっつうずつもちます。) "Two copies of the contract are made, and the two parties each keep one." It is now `姉妹の演奏は、甲乙を争う出来ばえだった。` (しまいのえんそうは、こうおつをあらそうできばえだった。) "The two sisters' performances were evenly matched in quality." |
| words 甲乙 | 25 | "These are original usage examples, not quotations. The second one uses the phrase with を, as Digital Daijisen's own example for the second sense does: 甲乙をつけがたい." becomes "These are original usage examples, not quotations. Both use the second sense, in phrases from Digital Daijisen's own examples for that sense: 甲乙を争う出来ばえ and 甲乙をつけがたい." |

Why: no supplied source gives 甲乙 a sense "both parties to a contract".

- JMdict has one entry spelled 甲乙, 1280080, with two senses: "first and second; A and B" and "superiority and (or)
  inferiority; distinction (in quality); discernment; discrimination" (`evidence\kouotsu-scan.txt`,
  `evidence\jmdict-cited-entries.xml`).
- Digital Daijisen gives １ 第一と第二 and ２ 二つのものの間の優劣, with the examples 「―をつけがたい」 and 「―を争う出来ばえ」
  (`evidence\甲乙-daijisen.txt`).
- So the sentence and the contract example were removed, and the first example now uses the second sense.

Line 39 (unchanged) still gives the JMdict senses of 甲 and 乙 on their own: one sense of 甲 is the A party or first party, for
example in a contract (1578730), and one sense of 乙 is the second party, rank or grade (1182940). No other file of the batch
states the removed sense; the 乙 kanji card's line 23 quotes JMdict's gloss of the word 乙, "(the) second (party, rank, etc.)",
and is unchanged.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `395f5364` (the earlier confirmation packet's `checks\`), apart from command lines,
timings and the figures below.

- **`lint.txt`:** 0 errors, 1 warning (`words/潜る.md`: the Dictionary line cites no JMdict entry id). **`unittest.txt`:** 439
  tests, OK. **`validate.txt`:** 0 errors. **`linkplan.txt`:** 0 problems. **`kanji-remarks.txt`:** 0 problems.
- **`manifest.txt`:** rebuilding `manifest.json` leaves it unchanged and the tree clean.
- **`budget.txt`:** informational. Retained bytes are 56,571,986: 105 fewer than at `395f5364`, 247 more than at `c6afa163`.
- **`quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`:** the same as at `395f5364` apart from line 1. These audits
  read kanji cards only, and no kanji card changed.
- **`evidence\word-quiz.txt`:** the word-quiz audit at `3c5ef845`. It is byte-identical to the earlier confirmation packet's
  `evidence\word-quiz.txt`: the audit reads front matter, and the 甲乙 front matter did not change.
- **`evidence\kouotsu-scan.txt`:** new; see `RESPONSE.md` L1.
- **JVM tests:** the Android JVM tests that read the real content were not run (no JDK on this machine).

## Process notes

- The checks in `checks\` and the evidence audits were run on the committed revision `3c5ef845`.
