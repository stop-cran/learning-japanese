# Author's statement for the reviewer of `b157-confirm-reports\gpt.md`

This statement answers only the points in YOUR confirmation report on cd5d75d1. F1 and F2 are your Findings 1 and 2. P1-P5 are
these points from your Optional section: P1, the “Only reading” note in item 10 of your judgments on the other-review changes;
P2, your curated-distractor table and the closing remark that mixing categories could help, especially for 侍 and 俵; P3, the
caution about 言語 under “Remaining word options”; P4, your labels question; P5, your phone-readability note, together with item
5's remark that the 俊足 reconciliation is dense. L1 is your Limit on the four latent readings. Your other Optional judgments
accept the changes they cover, and your other Limits describe your own method; they need no answer. The statement is the author's
claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\`
outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised
files in this packet. The batch cards 侍, 侯, 俵 and 倫 changed, as did `words\倫理.md` (front matter only), the ledger
`docs\n1-sources\batch-157-progress.json` and the regenerated `manifest.json`. Every other batch card, word article, reused card
(助, 理), tool and supplement file is unchanged since cd5d75d1. See `CHANGES.md`. Give a disposition for each of F1, F2, P1-P5 and
L1, and judge the other reviews' changes described below.

## Findings

### F1: 五倫 is reduced to filial piety (`kanji\倫.md:38`)

Author action: **changed**: the claim is removed rather than paraphrased.

- `kanji\倫.md:38` no longer mentions 五倫. The author judged that the card teaches 倫 through 倫理, 不倫 and 絶倫 and does not
  need 五倫, and dropped the sentence instead of writing a new paraphrase that would need its own source.
- The Metadata line (line 42) no longer lists JMdict entry 1593605. 五倫 no longer appears anywhere in the batch.
- Another review made the same finding.

### F2: the 仁 exclusion on 倫理 is not a direct overlap (`words\倫理.md:8`, `28`)

Author action: **changed**, with your remedy.

- `words\倫理.md:8` is `quiz_exclusions: [道徳, 善]`.
- The ledger's word-exclusion row (line 55) is `["道徳", "善"]`, and the `status` sentence (line 136) no longer lists 倫理/仁.
- Line 28 keeps the comparison, which quotes JMdict's gloss of 仁 and calls it another related moral concept. Line 34 still cites
  entry 1369620.
- In `evidence\word-quiz.txt`, the 倫理 block (lines 2076-2094) lists the exclusions as 道徳 and 善 (line 2078). 仁 now scores 7,
  above the last slot (line 2083), so it is offered in every 倫理 meaning quiz. The reverse pair 倫理 shown for 仁 is back (line
  2796, score 7 above the last slot), making 814 reverse meaning pairs (line 2171; 813 in `evidence\prior-word-quiz.txt`).

## Optional notes

### P1: “Only reading” on 俵

Author action: **not changed**. `kanji\俵.md:29` and `40` say that JMdict lists 俵 ひょう as “the only reading for the counter
sense”. This describes entry 1583390, whose counter sense is restricted to ひょう. The card also lists 一俵 いっぴょう (line 36,
JMdict 1166100), so it shows a sound-changed form. Please say whether the wording still needs a change.

### P2: distractor difficulty, especially 侍 and 俵

Author action: **changed** for 侍, 侯 and 俵; **not changed** for 佐 and 俊.

- 侍 is now `[父, 雨, 魚]` (`kanji\侍.md:13`, sentence at line 43). The clause “they name family members” is gone.
- 侯 is now `[女, 国, 金]` (`kanji\侯.md:13`, sentence at line 39), mixing a person, a place and a material instead of places and
  institutions.
- 俵 is now `[田, 車, 本]` (`kanji\俵.md:13`, sentence at line 44).
- 佐 `[母, 友, 子]` is kept. The answer “aide; assistant” also names a person, so the person category does not single out the
  answer, and 友 “friend” is not a relative.
- 俊 `[安, 少, 多]` is kept. The answer is a quality, and the distractors are qualities or amounts. No one category holds the three
  distractors without the answer.
- The ledger's `quizAudit` rows for 侍, 侯, 俵 and 倫 (lines 112, 114, 117 and 118) carry the new sets and their titles.
- `CHANGES.md` (“Distractor choices”) lists the senses checked for each new distractor, such as 女 すけ “helper” and 金
  “gold general” and “Jin dynasty”, and the candidates rejected. The reading-quiz effects are under “What the new sets change in
  the reading quiz”. Please judge the new sets and the two kept sets.

### P3: 言語 on 俗語

Author action: **not changed**. In the 俗語 block of `evidence\word-quiz.txt` (starting at line 1376), 言語 “language” scores 8
(line 1388), and 俗語 is offered for 言語 (line 2669). 俗語's title is “colloquial word; slang”; the author judged “language” the
broader subject, not a second correct answer. Please judge.

### P4: “reference reading” for 助 and 理

Author action: **not changed** so far; the quiz point is disclosed below for your judgment.

- 助 (`kanji\助.md:32-33`) and 理 (`kanji\理.md:26`, `31`) keep “kun, source-only here”, the label that 97 other kanji cards
  already use in their Readings tables (as “kun, source-only here” on 70 cards and “on, source-only here” on 43; search `repo\kanji\` of the original packet).
  Rewording two cards only would make them differ from the rest; a repository-wide rewording is outside this batch. The batch
  cards keep their plain-language rows.
- Your quiz point is correct. On the 70 other cards with the kun label, the front matter has a `quizKunyomi` list that leaves the
  labelled reading out. 助 and 理 have no `quizKunyomi`, so their legacy reading questions can still ask す.ける or すけ (助) and
  ことわり (理), although the table calls these readings source-only.
- The batch added only the table rows. The front matter of both cards is unchanged since before the batch, so the quiz behaviour
  is not new, and `docs\content-format.md` (line 153 in the original packet's `repo\`) does not require curating reading questions
  on existing cards.
- Please say whether the repository convention is an acceptable reason to keep the label on these two cards, and whether the
  label now misleads enough that the batch should add `quizKunyomi` to them (for example 助 `[たす.ける, たす.かる]` and 理 `[]`).

### P5: shorten `kanji\併.md:39` and `words\俊足.md:32`

Author action: **not changed**. Both paragraphs answer first-round findings and tie each claim to a dictionary entry: the rare
spelling and sense restriction of 併せる and 併せて on 併, and the Daijisen senses of 俊足 and 駿足 on 俊足. The author judged that
shortening them would drop sourced detail added for first-round findings. Please name any sentence you would still cut.

## Limits answered

### L1: four latent readings

Author action: **no change; unchanged state**. `checks\reading-exposure.txt` still reports four latent collisions, 0 production
hits and 0 padded-session hits (lines 168-169), as at cd5d75d1 (`evidence\prior-reading-exposure.txt`). The four are 佳 けい and
えい (lines 31, 34), 侍 かみ (line 68) and 俗 しょく (line 130). None of the new distractors 雨, 魚, 女, 金, 車, 本 and 時 holds
かみ, and each batch card's curated set still fills all three wrong slots, so the fallback is never consulted.

## Changes made for the other reviews

The other two confirmation reports asked for the changes below. Please judge each change as a reviewer of the revised text, not
only as an answer to your own notes.

1. **倫's distractor 事 is replaced by 時.** Another review noted that 事 “matter, affair” sits next to the card's own 不倫 example
   “affair”. 倫 is now `[力, 時, 名]` (`kanji\倫.md:13`, sentence at line 40). The author did not put 時 on 侍, judging that 侍's
   component 寺 would make 時 a visual near-match there.
2. **不倫:** another review noted that Digital Daijisen's definition starts with the broader 道徳にはずれること clause. Line 34 now
   reads “immorality; especially infidelity, an extramarital affair”, and line 38 says that Digital Daijisen defines 不倫 as
   departing from morality, especially a sexual relationship with someone other than one's spouse (`evidence\weblio-不倫.txt`,
   line 7).
3. **The 侍 and 俵 sets:** another report judged both the 侍 and 俵 sets guessable by category, and the third judged 侍's set a
   kinship cluster; the changes are under P2.

**Process notes** (details in `CHANGES.md`): no review ran on the intermediate commits `81142e4a` and `0daebfba`. `81142e4a` first
set 侍's distractors to `[父, 男, 魚]`; the author judged 男 too generic and replaced it with 雨 in `0daebfba`, before any review.
The last commit, `24201899`, changes only the ledger's audit sentence (line 127).
