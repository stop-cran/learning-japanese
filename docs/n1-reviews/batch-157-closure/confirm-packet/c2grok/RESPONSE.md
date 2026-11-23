# Author's statement for the reviewer of `b157-confirm-reports\grok.md`

This statement answers only the points in YOUR confirmation report on cd5d75d1. Your report has no findings. O1-O3 are three
points of your Optional paragraph in order: O1, the distractor sets that can be rejected as a kinship cluster; O2, the labels
question; O3, the note that 不倫 could mention Daijisen's broader 道徳にはずれる clause. Your other Optional judgments accept the
changes they cover, and your Limits describe your own method; they need no answer. The statement is the author's claim about what
changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the
`evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this
packet. The batch cards 侍, 侯, 俵 and 倫 changed, as did `words\倫理.md` (front matter only), the ledger
`docs\n1-sources\batch-157-progress.json` and the regenerated `manifest.json`. Every other batch card, word article, reused card
(助, 理), tool and supplement file is unchanged since cd5d75d1. See `CHANGES.md`. Give a disposition for each of O1-O3, and judge
the other reviews' changes described below.

## Optional notes

### O1: 佐 and 侍 can be rejected as a kinship cluster

Author action: **changed** for 侍; **not changed** for 佐.

- 侍 is now `[父, 雨, 魚]` (`kanji\侍.md:13`; the sentence at line 43 no longer says “they name family members”).
- 佐 `[母, 友, 子]` is kept. The answer “aide; assistant” also names a person, so the person category does not single out the
  answer, and 友 “friend” is not a relative.
- You judged 俊 and 俵 not one rejectable category. 俊 is unchanged; 俵 changed for the other reviews (see below).
- The ledger's `quizAudit` rows for 侍, 侯, 俵 and 倫 (lines 112, 114, 117 and 118) carry the new sets and their titles.
- `CHANGES.md` (“Distractor choices”) lists the senses checked for each new distractor and the candidates rejected. Please judge
  the new sets and the kept 佐 set. The new sets add no reading collision: see `CHANGES.md`, “What the new sets change in the
  reading quiz” (0 production hits, the same four latent readings).

### O2: keep “source-only here” off the batch and on 助 and 理

Author action: **not changed**, as you advised. The batch Readings rows keep their plain-language text, and 助
(`kanji\助.md:32-33`) and 理 (`kanji\理.md:26`, `31`) keep the label. Item 6 below describes a quiz point another review raised
about these two cards.

### O3: 不倫 and Daijisen's broader clause

Author action: **changed**, with your suggestion.

- `kanji\倫.md:34` now reads “不倫 ふりん — immorality; especially infidelity, an extramarital affair” (was “infidelity; an
  extramarital affair”).
- Line 38 now says “倫理 is ethics, while Digital Daijisen defines 不倫 as departing from morality, especially a sexual relationship
  with someone other than one's spouse” (was “ethics versus infidelity”).
- Source: `evidence\weblio-不倫.txt`, line 7 (道徳にはずれること。特に、配偶者以外と肉体関係をもつこと。).

## Changes made for the other reviews

The other two confirmation reports asked for the changes below. Please judge each change as a reviewer of the revised text, not
only as an answer to your own notes.

1. **五倫 is removed from 倫.** Both other reports judged JMdict's gloss of 五倫 (entry 1593605), “the five Confucian
   filial-piety relationships”, misleading, because in their view the five relationships are not all parent-child ones. The
   author dropped the sentence from `kanji\倫.md:38` rather than paraphrase it, and the Metadata line (line 42) no longer lists
   entry 1593605.
2. **倫理 no longer excludes 仁.** Another review judged 仁 “benevolence; compassion” a related moral concept, not a second correct
   answer for “ethics; morals”. `words\倫理.md:8` is `[道徳, 善]`, and the ledger's word-exclusion row (line 55) and `status`
   (line 136) match. Line 28 still compares 仁 with JMdict's gloss, and line 34 still cites entry 1369620. 仁 now scores 7, above
   the last slot, so it is offered in every 倫理 meaning quiz (`evidence\word-quiz.txt:2083`); 倫理 is likewise offered in every
   仁 quiz (line 2796). Please say whether 仁 is safe as a wrong option for 倫理.
3. **倫's distractor 事 is replaced by 時.** Another review noted that 事 “matter, affair” sits next to the card's own 不倫 example
   “affair”. 倫 is now `[力, 時, 名]` (`kanji\倫.md:13`, sentence at line 40). The author did not put 時 on 侍, judging that 侍's
   component 寺 would make 時 a visual near-match there.
4. **侯's distractors** are now `[女, 国, 金]` (`kanji\侯.md:13`, sentence at line 39). Another review judged the old set (国 京 社:
   places and institutions, whose answer is a person's rank) a strong category cue. `CHANGES.md` gives the senses checked, including
   女 すけ “helper”, 国 “province” and 金 “gold general” and “Jin dynasty”, and why 男, 子 and 父 were rejected for 侯.
5. **俵's distractors** are now `[田, 車, 本]` (`kanji\俵.md:13`, sentence at line 44). Both other reports judged 田 土 木 an easy
   nature group. `CHANGES.md` notes that 本's counter senses are for long, thin objects (1522150 sense 5) and plants or trees
   (1260670 sense 10), not for sacks.
6. **Labels:** another review suggested “reference reading” for 助 and 理. It was declined, because 97 other kanji cards already
   use the label in their Readings tables (as “kun, source-only here” on 70 cards and “on, source-only here” on 43; search `repo\kanji\` of the original packet), and
   changing two cards only would make them differ from the rest. That review also noted that 助 and 理 have no `quizKunyomi`, so
   their legacy reading questions can still ask the readings the table calls source-only; the front matter of both cards is
   unchanged since before the batch.

**Process notes** (details in `CHANGES.md`): no review ran on the intermediate commits `81142e4a` and `0daebfba`. `81142e4a` first
set 侍's distractors to `[父, 男, 魚]`; the author judged 男 too generic and replaced it with 雨 in `0daebfba`, before any review.
The last commit, `24201899`, changes only the ledger's audit sentence (line 127).
