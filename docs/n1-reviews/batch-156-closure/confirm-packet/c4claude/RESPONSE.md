# Author's statement for the reviewer of `reports-156-hold\confirm3-claude.md`

This statement answers your third confirmation report and states three items the author raised. Your report had no
Findings. Its Optional section has one numbered point; here it is P1. Its Limits describe what you did not verify and need
no answer; for one of them, a figure is now supplied (see the process notes).
A1 to A3 are items the author raised after your report. A1 is the whole of this revision; A2 and A3 concern two rows that
this revision leaves unchanged and ask you to review the author's justification for them. The statement is the author's
claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the
`checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer
to the revised files in this packet. Give a disposition for P1 and A1 to A3.

## Optional points

### P1: `CHANGES.md` misdescribed `checks\quiz-safety.txt`

Author action: **changed in this round's `CHANGES.md`** (the statement, not the batch).

- Your report found that the last round's `CHANGES.md` said `checks\quiz-safety.txt` matched the earlier packet "apart from
  line 1 (the command and label)", while the file has no command line and was byte-identical. The author agrees.
- This round's `CHANGES.md` says that `checks\quiz-safety.txt` is byte-identical to your earlier packet's copy and has no
  command line, and that `checks\reading-exposure.txt` and `checks\reading-options.txt` differ from your earlier packet's
  copies only on line 1, which names the revision.

To verify: compare those three files with the copies in your earlier confirmation packet's `checks\`.

## Author-raised items
### A1: the 乙 word 甲乙 did not meet the selection rule; replaced by 乙種

Author action: **changed.** See `CHANGES.md` for the changed lines and `evidence\selection-evidence.md` for the rule.

- **Why 甲乙 goes.** 甲乙 carries only news2 and spec2, which are not in the rule's tag list (news1, ichi1, spec1, gai1),
  and its other kanji 甲 has no card in the repository and is not in this batch, which the rule requires regardless of
  tags. At freeze the author counted news2 and spec2 as qualifying and did not check 甲. That was the author's error.
- **The listed-tag candidates** (`evidence\candidates.md`, 乙 table):
  - 乙 alone (JMdict 1182940, news1) was this batch's 乙 word at freeze. Revision `7eaf5c24` deleted it because its reading
    quiz could offer おと (from the corpus word 音), which is also a JMdict reading of the written form 乙 (entry 2837087,
    弟/乙 おと, archaic): the original packet's `evidence\audits\word-quiz.txt` flags it as ATTESTED (line 137) and counts
    one problem (line 3765). Bringing it back would bring back that collision.
  - 早乙女 さおとめ (1844500, news1; 早 and 女 have cards) is in the Joyo table's appendix of whole-word readings (p. 162;
    also 早's row, p. 97); note 13 on p. 3 says the appendix gives words whose readings are hard to give character by
    character. Point 3 of the rule says that words read only within a whole-word reading are not attached to a reading row and give no quizzed reading. The word does not use
    オツ, the only reading Joyo lists for 乙, and its meaning, a young woman planting rice, does not show 乙's main meaning
    of second place. Digital Daijisen lists it under 乙's ［難読］ (hard-to-read words) (`evidence\weblio-乙.txt`).
- **The other candidates:** 乙女 おとめ (2855480) is untagged and is also an appendix whole-word reading (p. 162).
- **Why 乙種.** 乙種 (1862630) is untagged, so it needs the per-row justification the rule allows:
  - no listed-tag candidate is usable (above);
  - it shows 乙's main meaning, second place in an order (乙 card line 23): it is the first example the Joyo table gives
    for 乙 (p. 19); Digital Daijisen gives it as the example of 乙's sense "順位で、第二位" under 〈オツ〉
    (`evidence\weblio-乙.txt`); Kanjipedia gives it for its meaning ② "物事の順位の二番目" (`evidence\kanjipedia-乙.txt`);
  - its reading おつしゅ uses オツ; 種 has a card; JMdict gives one reading and marks neither the spelling nor the reading;
  - the word-quiz audit at `ba44b280` reports no ATTESTED or too-few-candidate problem (`evidence\word-quiz.txt`, last
    line; the 乙種 section is lines 74-86).
- **The new article** `words\乙種.md` is new text. Its Daijisen statements rest on `evidence\weblio-乙種.txt` and
  `evidence\weblio-乙種合格.txt`; its glosses for 甲種, 丙種 and 甲乙丙 on the JMdict entries 1280150, 1907280 and 1280090
  (`evidence\jmdict-cited-entries.xml`).

To verify: the facts above against the named evidence and independent sources; review `words\乙種.md` in full and the three
changed lines of the 乙 card against all four facets, as new text; check its quiz options; and judge whether the
justification for an untagged word is acceptable. Give RESOLVED if the replacement is sound and justified.

### A2: the 仙 word 仙人 is not on the tag list; kept

Author action: **not changed; the row justification is given here for review.**

- 仙人 (JMdict 1387170) carries news2 and spec2 only. The one listed-tag candidate is 仙台 せんだい (2164680, spec1; 台
  has a card); 水仙 (1371750) has news2 and spec2 and is marked "usually written using kana alone" (`evidence\candidates.md`,
  仙 table).
- 仙台 is the name of a city: JMdict's only sense is "Sendai (city in Miyagi)". It shows none of 仙's meanings. The rule
  prefers a spelling with a listed tag and also prefers a word that shows the kanji's main meaning; it does not say which
  preference wins when they conflict. Here the author lets the main meaning win and treats the row like the untagged case:
  a justification reviewed for the row.
- 仙人 shows 仙's main meaning, a hermit or immortal of the mountains (仙 card line 23). It is a Joyo example for 仙 (p. 94),
  and Kanjipedia gives it as the example of its meaning ① (the original packet's `evidence\kanjipedia-senses.txt`, line 24).
  Its reading せんにん uses セン, the only reading Joyo lists; 人 has a card; JMdict marks neither the spelling nor the
  reading.

To verify: the facts above; judge whether keeping 仙人 on this justification is acceptable. Give DECLINE ACCEPTED if it is;
DECLINE REJECTED otherwise, naming the word you would choose and why.

### A3: the 伯 word 伯仲 is not on the tag list; kept

Author action: **not changed; the row justification is given here for review, with one open question.**

- 伯仲 (JMdict 1474280) carries news2 and spec2 only. The listed-tag candidates (`evidence\candidates.md`, 伯 table):
  - 伯父 (1607070; ichi1, news1) and 伯母 (1607100; ichi1 and news2 on the spelling): their tagged readings are おじ and おば, the
    whole-word readings in the Joyo appendix (p. 162; 伯's row, p. 126). Point 3 of the rule names 伯 among the cards whose
    existing articles read the kanji only within a whole-word reading and so need a word under point 2 (伯's is 伯母さん,
    伯 card line 33); an おじ or おば article would repeat that case. The readings はくふ and はくぼ, which do use ハク, are restricted to those
    spellings and carry no tag; the JMdict DTD notes that a priority can belong to one kanji/reading pair
    (`evidence\selection-evidence.md`, section 2).
  - 伯爵 (1474260, news1): its other kanji 爵 has no card and is not in this batch.
- The others: 伯 alone (1474240) and 画伯 (1197500) carry news2 and spec2, like 伯仲; 伯楽 (1601290) carries news2, and JMdict marks
  its sense "cattle or horse trader; good judge of horses or cattle" as sensitive; 伯父 read えおじ (2648950) is archaic.
- 伯仲 and 画伯 are both Joyo examples for 伯 (p. 126, in that order), and both other kanji (仲, 画) have cards. Neither
  shows Kanjipedia's meaning ① of 伯, a parent's older brother or sister (the original packet's
  `evidence\kanjipedia-senses.txt`, line 44). 伯仲 shows meaning ②, the eldest of siblings, the first of 伯・仲・叔・季,
  through its archaic sense "eldest and second eldest brother"; its main sense, "being evenly matched", does not
  show a meaning of 伯 directly. 画伯 shows meaning ④, a title for someone who excels in an art, and Kanjipedia gives 画伯 as the example of
  that meaning.
- The author's freeze notes give no reason for preferring 伯仲 to 画伯. The author keeps 伯仲 because it is the table's first
  example and because meaning ②, like ①, is about seniority among siblings, which ties the word to 伯父 and 伯母 on the
  same card. This is a judgment, not a rule: please weigh it against 画伯, whose meaning is more transparent.

To verify: the facts above; judge whether keeping 伯仲 is acceptable. Give DECLINE ACCEPTED if it is; DECLINE REJECTED if
画伯 or another word should replace it, saying why. A replacement would be a new article in a new revision.

## Process notes

- The checks in `checks\` and the evidence audits were run on the committed revision `ba44b280`.
- The author's working selection note (a session file, not in the repository or in any packet) wrongly described the words'
  priority tags as including news2 and spec2; it is being corrected.
- Your Limits noted that you had no merge-time budget figure. `evidence\budget-at-merge.txt` is the author's budget run at
  the merge `eafee44b`; `CHANGES.md` gives the step from it to `checks\budget.txt`.