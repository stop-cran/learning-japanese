# Author's statement for the reviewer of `b157-confirm-reports\claude.md`

This statement answers only the points in YOUR confirmation report on cd5d75d1. F1 is your Finding F1, and O1-O5 are your
Optional notes O1-O5. Three of your Limits raise points this packet can answer; they are L1-L3 below. Your other Limits describe
your own method and need no answer. The statement is the author's claim about what changed and why. Verify each claim against the
revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely
on this text as evidence. Line numbers refer to the revised files in this packet. The batch cards 侍, 侯, 俵 and 倫 changed, as did
`words\倫理.md` (front matter only), the ledger `docs\n1-sources\batch-157-progress.json` and the regenerated `manifest.json`.
Every other batch card, word article, reused card (助, 理), tool and supplement file is unchanged since cd5d75d1. See `CHANGES.md`.
Give a disposition for each of F1, O1-O5 and L1-L3, and judge the other reviews' changes described below.

## Findings

### F1: the 五倫 gloss misleads a beginner

Author action: **changed**, but not with your wording: the claim is removed rather than reworded.

- `kanji\倫.md:38` no longer mentions 五倫. The author judged that the card teaches 倫 through 倫理, 不倫 and 絶倫 and does not
  need 五倫, and dropped the sentence instead of writing a new paraphrase that would need its own source.
- The Metadata line (line 42) no longer lists JMdict entry 1593605. 五倫 no longer appears anywhere in the batch.
- Another review made the same finding.

## Optional notes

### O1: distractor sets that can be rejected by category

Author action: **changed** for 侍 and 俵; **not changed** for 佐 and 俊.

- 侍 is now `[父, 雨, 魚]` (`kanji\侍.md:13`; sentence at line 43, which no longer says “they name family members”).
- 俵 is now `[田, 車, 本]` (`kanji\俵.md:13`; sentence at line 44).
- 侯 also changed, to `[女, 国, 金]`, for another review (see below).
- 佐 `[母, 友, 子]` is kept. The answer “aide; assistant” also names a person, so the person category does not single out the
  answer, and 友 “friend” is not a relative.
- 俊 `[安, 少, 多]` is kept. The answer is a quality, and the distractors are qualities or amounts. No one category holds the three
  distractors without the answer. The 少/多 antonym pair could draw a guesser toward one of those two, but it does not point to
  the answer.
- The ledger's `quizAudit` rows for 侍, 侯, 俵 and 倫 (lines 112, 114, 117 and 118) carry the new sets and their titles.
- `CHANGES.md` (“Distractor choices”) lists the senses checked for each new distractor and the candidates rejected. Please judge
  the new sets and the two kept sets.

### O2: 事 “matter, affair” next to 不倫 “affair”

Author action: **changed**. 倫's distractors are `[力, 時, 名]` (`kanji\倫.md:13`); 時 “time, hour” replaces 事 (sentence at
line 40). The author did not put 時 on 侍, judging that 侍's component 寺 would make 時 a visual near-match there.

### O3: over-exclusions, and possible mild overlaps 憎/侮 and 無視/侮る

Author action: **not changed**.

- **Over-exclusions:** you called them harmless, and they are kept as conservative guards.
  - 制作 for 佳作: JMdict 1374810 sense 1 for 制作 is “work (film, book)”, which `words\佳作.md:28` already quotes.
  - 併用 “combined use; using together”: the excluded 使う “use; spend”, 用 “use; purpose” and 用途 “use; intended purpose” all
    share the word “use” in their displayed titles.
- **憎/侮:** 侮's curated distractors `[聞, 話, 会]` (`kanji\侮.md:13`) fill all three wrong slots, so 憎 is never offered on
  侮's meaning quiz. 憎's own set is `[増, 層, 晴]` (unchanged; `repo\kanji\憎.md:11` in the original packet), so 侮 is never
  offered on 憎's.
- **無視/侮る:** `words\無視.md` exists (title “ignoring; disregarding”; `repo\words\無視.md` in the original packet), but 無視 does not appear anywhere in
  `evidence\word-quiz.txt`. It is not among 侮る's candidates (block at line 739: 0 candidates above the last slot, 610 tied at
  score 5, line 745), and 侮る is never shown for it.
- The closest titles in 侮る's tie are いじめる “bully; pick on” (line 755) and からかう “tease; make fun of” (line 764). The author
  judged neither a correct answer for “look down on; make light of”. Please check.
- Please say whether you still prefer removing any of these exclusions.

### O4: do not adopt “source-only here” on the batch

Author action: **not changed**, as you advised. The batch Readings rows keep their plain-language text.

- The reused cards 助 (`kanji\助.md:32-33`) and 理 (`kanji\理.md:31`) keep “kun, source-only here”, the label that 97 other kanji
  cards already use in their Readings tables (as “kun, source-only here” on 70 cards and “on, source-only here” on 43; search `repo\kanji\` of the original packet).
  Rewording it on two cards only would make them differ from the rest; a repository-wide rewording is outside this batch.
- The 理 intro sentence (`kanji\理.md:26`) reads “This table includes ことわり as a source-only kun reading alongside the common on
  reading リ.” It uses the same term, and is kept for the same reason.
- Another review noted that the label is prose and selects nothing for the quiz. This is true. On the 70 other cards with the kun
  label, the front matter has a `quizKunyomi` list that leaves the labelled reading out. 助 and 理 have no `quizKunyomi`, so their
  legacy reading questions can still ask す.ける or すけ (助) and ことわり (理), although the table calls these readings
  source-only. The batch added only the table rows; the front matter of both cards is unchanged since before the batch, and
  `docs\content-format.md` (line 153 in the original packet's `repo\`) does not require curating reading questions on existing
  cards.
- Please say whether the repository convention is an acceptable reason to keep the label on these two cards, and whether the
  label now misleads enough that the batch should add `quizKunyomi` to them (for example 助 `[たす.ける, たす.かる]` and 理 `[]`).

### O5: the sex-service sense of 風俗 on 俗

Author action: **not changed**. A first-round review asked for this sense. `kanji\俗.md:23` and `34` give it as a separate sense,
sourced to JMdict 1499960 sense 3 “sex service; sex industry; sex-oriented entertainment”, after the manners, customs and
public-morals senses. Please judge whether the wording is neutral, and whether this separately labelled sense is acceptable on a
beginner card.

## Limits answered

### L1: the word-quiz ties were taken from CHANGES.md

Author action: **evidence pointer**. `evidence\word-quiz.txt` is in this packet; please read the blocks directly. 倫理 (lines
2076-2094) is the only block whose candidates changed in this revision; see “Changes made for the other reviews”, item 1. The
other blocks you named start at these lines: 併用 34, 俗語 1376, 俵 1394, 諸侯 2149. `evidence\prior-word-quiz.txt` is the same
output at cd5d75d1.

### L2: KANJIDIC2 for 卑 and 併 not verified

Author action: **evidence pointer**; the cards are unchanged since cd5d75d1.

- 併: the original packet's `evidence\kanjidic2-records.xml` holds its record (`<literal>併</literal>` at line 149).
- 卑: that file has no 卑 record. This packet adds `evidence\kanjidic2-卑.xml`, the 卑 record copied verbatim from the repository's
  B155 closure evidence. It lists the meanings “lowly”, “base”, “vile”, “vulgar” and “despise”; `kanji\侮.md:40` cites the last.

### L3: the 俊/佐/佳/併 Daijisen extracts were relied on from round 1

Author action: **evidence pointer**; these cards are unchanged since cd5d75d1. The extracts are in the original packet's
`evidence\public-source\` folder as `weblio-俊.txt`, `weblio-佐.txt`, `weblio-佳.txt` and `weblio-併.txt`, each with its source
URL and retrieval time.

## Changes made for the other reviews

The other two confirmation reports asked for the changes below. Please judge each change as a reviewer of the revised text, not
only as an answer to your own notes.

1. **倫理 no longer excludes 仁.** Another review judged 仁 “benevolence; compassion” a related moral concept, not a second correct
   answer for “ethics; morals”. `words\倫理.md:8` is `[道徳, 善]`, and the ledger's word-exclusion row (line 55) and `status`
   (line 136) match. Line 28 still compares 仁 with JMdict's gloss, and line 34 still cites entry 1369620. 仁 now scores 7, above
   the last slot, so it is offered in every 倫理 meaning quiz (`evidence\word-quiz.txt:2083`); 倫理 is likewise offered in every
   仁 quiz (line 2796). Please say whether 仁 is safe as a wrong option for 倫理.
2. **侯's distractors** are now `[女, 国, 金]` (`kanji\侯.md:13`, sentence at line 39). Another review judged the old set (国 京 社:
   places and institutions, whose answer is a person's rank) a strong category cue. `CHANGES.md` gives the senses checked, including
   女 すけ “helper”, 国 “province” and 金 “gold general” and “Jin dynasty”, and why 男, 子 and 父 were rejected for 侯.
3. **不倫:** another review noted that Digital Daijisen's definition starts with the broader 道徳にはずれること clause. Line 34 now
   reads “immorality; especially infidelity, an extramarital affair”, and line 38 says that Digital Daijisen defines 不倫 as
   departing from morality, especially a sexual relationship with someone other than one's spouse (`evidence\weblio-不倫.txt`,
   line 7).

**Process notes** (details in `CHANGES.md`): no review ran on the intermediate commits `81142e4a` and `0daebfba`. `81142e4a` first
set 侍's distractors to `[父, 男, 魚]`; the author judged 男 too generic and replaced it with 雨 in `0daebfba`, before any review.
The last commit, `24201899`, changes only the ledger's audit sentence (line 127).
