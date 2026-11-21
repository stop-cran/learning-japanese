# Author's statement for the reviewer of `reports-156-hold\confirm-claude.md`

This statement answers only the points in YOUR confirmation report. Your report had no Findings. Its Optional section has three
numbered points; here they are P1, P2 and P3. The first section of its Limits, "Not independently verified", has two items; here
they are L1 and L2. Your other Limits describe your own method and need no answer. The statement is the author's claim about
what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the
`evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this
packet. One file changed, the word article 甲乙, on lines 16, 18-20 and 25 (see `CHANGES.md`). Give a disposition for P1, P2, P3,
L1 and L2.

## Limits

### L1: that 甲乙 has no other JMdict reading or entry

Author action: **evidence supplied; no change.**

- `evidence\kouotsu-scan.txt` (produced by `evidence\kouotsu_scan.py`) scans the pinned `JMdict_e.gz` (sha256 on line 3).
- Exactly one entry has the written form 甲乙: 1280080, read こうおつ only, with two senses ("first and second; A and B";
  "superiority and (or) inferiority; distinction (in quality); discernment; discrimination").
- Three entries have a longer written form containing 甲乙: 1280090 甲乙丙 こうおつへい, 1874770 甲乙丙丁 こうおつへいてい and
  2124490 甲乙つけがたい こうおつつけがたい.
- One entry is read こうおつ (1280080), and none is read かるめる.

To verify: that the scan's output supports the article's "its only entry spelled 甲乙 is read こうおつ" (line 41) and its
readings, and that the word-quiz audit's 0 attested problems for 甲乙 agree with it.

### L2: that 甲乙 names the two parties together in contract boilerplate

Author action: **removed.**

- No supplied source gives 甲乙 that sense. JMdict 1280080 has the two senses above. Digital Daijisen
  (`evidence\甲乙-daijisen.txt`) gives １ 第一と第二 and ２ 二つのものの間の優劣.
- Line 16 no longer has the sentence "In a contract, 甲 labels the first party and 乙 the second, so 甲乙 can name both parties
  together."
- The contract example (old lines 18-20) is replaced by `姉妹の演奏は、甲乙を争う出来ばえだった。`
  (しまいのえんそうは、こうおつをあらそうできばえだった。) "The two sisters' performances were evenly matched in quality." It is
  built on Daijisen's example phrase 「―を争う出来ばえ」 for the second sense.
- Line 25 now says that both examples use the second sense, in phrases from Daijisen's own examples for it: 甲乙を争う出来ばえ and
  甲乙をつけがたい.
- Line 39 is unchanged: it gives JMdict's senses of 甲 (1578730, "the A party (e.g. in a contract); the first party") and of 乙
  (1182940, "(the) second (party, rank, etc.)") on their own, not as a sense of 甲乙.

To verify: that the removed text is gone and nothing else on the lines changed; that the new example is natural Japanese, its
reading and translation are right and it uses the relative-merit sense; and that no remaining text of the batch states the
removed sense.

## Optional points

### P1: a ん + /p/ example in the compound-sound-changes article

Author action: **not changed in this batch; recorded as a follow-up.**

- The article `articles/compound-sound-changes.md` is shared: `伐.md:31`, `words\亜熱帯.md:29`, `潜.md:57`, `words\伐採.md:28`
  and the published `輩.md:31` link it. It is unchanged since the freeze. As you note, the gap is not a regression of this batch:
  the published 輩 card links the article in the same way for ぱい in 先輩.
- Adding an example after ん (for instance 先輩 せんぱい or 散歩 さんぽ) changes a shared article and every page that links it, so
  the author records it as a follow-up for a separate change, not in this batch.

To verify: that the article is unchanged in this revision (`diffs\changed-files.txt`), and judge whether the decline is
acceptable.

### P2: the 中心 exclusion on 仁

Author action: **not changed.**

- The exclusions work at the level of the displayed titles. 中心's title is "center; core; focus", and JMdict 1424550 lists
  "heart; core". "core" overlaps 仁's "kernel" sense directly, as 芯 "core; wick" does.
- 中央's title is "center; middle", and JMdict 1423430 gives "centre; center; middle; heart" and "capital; seat of government",
  with no "core" or "kernel". Its title names a position, not the inner part of something, so it stays in the tie.
- Over-exclusion only removes options, as your report says, so keeping 中心 costs nothing.

To verify: the two titles in the word articles and the two JMdict entries.

### P3: the 甲乙 exclusions 対照 and 差

Author action: **not changed**, as your report suggests. 差 "difference; gap" and 対照 "contrast; comparison against" name a
difference between two things, close to 甲乙's "relative merit" and JMdict's "distinction (in quality)"; excluding them only
removes options.

## Process notes

- The checks in `checks\` and the evidence audits were run on the committed revision `3c5ef845`.
