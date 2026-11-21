# Author's statement for the reviewer of `reports-155\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1, G2 and G3 are your report's Findings; your Optional section
says "None beyond the remedies above", and your Limits describe your own method and need no answer. The statement is the author's
claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\`
outputs and independent sources; do not rely on this text as evidence. Card line numbers refer to the revised cards in this
packet. All six new cards changed and the generated `manifest.json` was regenerated; every existing kanji card, every stroke file and every word article are unchanged. The only
front-matter changes are two `quiz_exclusions` lists, each of which lost one entry: 卑 lost 底 and 沙 lost 漠. No title, tag,
`distractors` list, metadata reading, `quizOnyomi` or `quizKunyomi` changed. See `CHANGES.md`. Give a disposition for each of G1,
G2 and G3.

## Findings

### G1: the 卑/底 exclusion rests only on the English word "base"

Author action: **changed** as you proposed.

- `卑.md:14` is now `quiz_exclusions: [低, 下, 劣, 汚, 謙, 凡, 粗, 貧, 悪, 近, 軽]`, and `卑.md:45` reads "These eleven cards are
  excluded from meaning choices:". The 底 bullet is gone.
- 底 declares no `quiz_exclusions`, and no other card lists 卑 in its `quiz_exclusions` or `distractors`, so the pair is no longer
  excluded anywhere. 卑's curated distractors (勇 賢 鋭) are unchanged and 底 is not among them, so `checks\quiz-safety.txt` still
  shows 卑's meaning options as its three curated titles; 底 can now appear only in a reduced pool that falls back to other cards.
- Your remedy also suggested a short contrast between moral baseness and a physical base. It is not on the learner card: the
  rewritten Notes (G3) give one reason per *excluded* group, and a bullet about a card that is not excluded would lengthen the Notes
  that G3 asks to shorten. The contrast is recorded in `evidence\exclusion-proofs.md`, section "Exclusions removed by the fix": "the
  only link was the English word "base" (moral baseness in KANJIDIC2's 卑 and JMdict's 卑劣, versus the physical bottom in 底's
  title)".

### G2: the 沙/漠 exclusion transfers the meaning of the word 沙漠 onto 沙

Author action: **changed** as you proposed, including the material-versus-region contrast.

- `沙.md:14` is now `quiz_exclusions: [砂, 岸, 粒, 石, 汰, 択, 選, 洗, 濯]`, and `沙.md:49` reads "These nine cards are excluded from
  meaning choices:". The 漠 bullet is gone.
- The rare-spelling information is kept as a Notes line, `沙.md:47`: "JMdict lists 沙漠 as a rarely used spelling of 砂漠 さばく,
  “desert”, and Digital Daijisen gives 沙漠 as an example of 沙 meaning sand. Sand is a material, while a desert is a region; compare
  the [漠](漠.md) card (“desert; vague”)." In JMdict 1593800 (on the Metadata line), 沙漠 carries the tag "rarely used kanji form".
  The original packet's `evidence\public-source\weblio-沙.txt` shows the Digital Daijisen character entry 〈サ〉 １ すな。「 沙漠 」.
- 漠 declares only `[広, 荒]` and no other card lists 沙 in its `quiz_exclusions` or `distractors`, so the pair is no longer excluded
  anywhere. 沙's curated distractors (鉄 銅 塩) are unchanged and 漠 is not among them.

### G3: the cards embed an editorial proof dossier

Author action: **changed**, in the layout this project already used when a reviewer raised the same problem on batch 149 (the 臨
and 艶 cards; see below). The other reviewer had judged the dense Notes acceptable as reference material placed after the teaching
core; this revision keeps a short reason on the card and moves the proofs, which is how the two positions were reconciled.

- **Meaning paragraph (line 23 on every card):** a plain-English description of the character's senses, KANJIDIC2's meaning list
  and the batch's common word, without the source-by-source comparison. For example, `卑.md:23` begins "卑 is about being low: low
  in rank or status, low in character (mean or vulgar), and looking down on others."
- **Notes:** the reading notes are shorter, and each group of excluded cards gets one bullet with one learner reason and, where a
  word is named, its kana and a gloss. For example, `鼓.md:47`: "[励](励.md) (“encourage; be diligent”), [勧](勧.md) (“recommend;
  encourage”) and [奨](奨.md) (“encourage; exhort; promote”): the encouraging sense, as in 鼓舞." The size table in `CHANGES.md`
  shows the `## Notes` sections falling to 198-281 words (from 331-525) and the cards to 3.6-5.0 KB (from 5.1-7.1 KB).
- **Proofs moved to editorial evidence:** `evidence\exclusion-proofs.md` holds each card's line-23 paragraph and Notes exactly as
  they were at `97c49eb2`; they will be filed with the batch's closure documents.
- **Unchanged:** the readings tables (including the source-only rows and their qualifications), Common words, mnemonics,
  distractor sentences, links, Metadata source links and every `quiz_exclusions` entry other than 底 and 漠. JMdict ids that the
  shorter text no longer names were removed from the Metadata lines (listed in `CHANGES.md`).
- **Precedent:** `evidence\batch-149-closure-README.md` (a copy of the published `docs/n1-reviews/batch-149-closure/README.md`),
  line 111, records the batch-149 fix for over-long Notes on 臨 and 艶: "short reading bullets and an "excluded from meaning
  choices" list with one reason per group". The six batch-155 cards now follow that layout.
- **Wording checks done in the same commit:** every quoted English gloss was re-checked against the cited JMdict entries, KANJIDIC2
  and the quoted card titles. A partial gloss is introduced with "can mean" or "includes"; a gloss given as a definition is the
  full JMdict sense; "rarer" was removed where it described a Kanjipedia sense, because the order of Kanjipedia's senses does not
  establish frequency. Please check that no simplification in the new text says more than its source.

The remaining exclusions you judged justified (the less obvious 下, 凡, 貧, 近, 軽; 抜, 抽, 濁, 汚, 誇; 岸 and the sorting/washing
pairs; 谷, 川, 多, 恵, 恩, 光, 輝; 洋, 嫌, 何, 乱, 長, 老, 蝶; and 撃, 拍, 脈, 激, 扇) are all still declared; only their reasons are
shorter. Please check that each shorter reason still states a true overlap.

## Other changes in this revision

The other review reported no findings. One of its optional notes raised the same 卑/底 point as your G1 and is settled by the G1
change; none of its other optional notes led to a change. Every changed hunk is one of the three changes above or a Metadata id trim
that follows from them.
