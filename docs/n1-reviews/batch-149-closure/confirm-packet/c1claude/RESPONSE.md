# Author's statement for the reviewer of `reports-149\initial-claude.md`

This statement answers only the points in YOUR initial report: findings C1 to C6 and optional items O1 to O12. The statement is
the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch` and
independent sources; do not rely on this text as evidence. Card line numbers refer to the revised cards in this packet. All 15
cards changed, two word articles changed by declared remark edits, six `distractors` lists (舎 芝 芽 茂 荘 華) and three
`quiz_exclusions` lists (腐 興 茂) changed; see `CHANGES.md`. Give a disposition for each of C1 to C6 and O1 to O12.

## Findings

### C1: the small っ in べっそう

Author action: **changed**. `荘.md:23`: the reading is ソウ for 荘, and the ツ of 別 (ベツ) becomes a small っ before it: べっそう.

### C2: "source-only" applied inconsistently

Author action: **changed**, by applying one convention instead of the label you proposed. "source-only here" is the spelling
already used on existing corpus cards, so it is kept, but it now marks only readings with no checked JMdict word example; each such
row names the source that lists the reading and says it is not selected for questions here (翼:33, 脈:32-33, 舎:32-34, 荘:34-35).
Readings that do have a checked JMdict example are labelled plain on or kun and say they are not selected for questions:
芝 シ (`芝.md:31`), 芽 めぐむ (`芽.md:33`), 荘 ショウ and チャン (`荘.md:32-33`, so the two mahjong counters now match), 腐 くさ.す
(`腐.md:37`), 華 ケ and ゲ (`華.md:32,34`) and 翻 ハン (`翻.md:32`). 艶's four extra kun rows state that they are not selected
(`艶.md:33-36`). 腐 -くさ.る is labelled "kun suffix" (`腐.md:33`). No one-line gloss of the convention was added; each row now
says in plain words why it is not quizzed.

### C3: 豆腐

Author action: **changed** in part. 豆腐 とうふ, "tofu; bean curd" (JMdict 1450070), is added to the フ row (`腐.md:31`) and to
Common words (`腐.md:42`), and 1450070 is in Metadata (`腐.md:53`). 腐敗 is also listed under Common words (`腐.md:43`). The
extra clause saying the word does not mean spoiled tofu was not added: the row's gloss already gives the meaning, and the card does
not explain why 腐 is written in 豆腐.

### C4: 艶やか

Author action: **changed** as you proposed. The つや row (`艶.md:32`), Common words (`艶.md:43-44`) and Notes (`艶.md:53`) give
both readings of 艶やか, つややか "glossy (e.g. hair); sleek; shiny; lustrous" and あでやか, which is usually written in kana
(also `艶.md:34`). 2682080 is in Metadata (`艶.md:68`).

### C5: implausible distractors

Author action: **changed**, with different cards from the ones you suggested. All replacements are Starter cards, so they are in
every documented pool (including the Starter practice session) and the curated options fill every wrong reading slot of these six
cards (`checks\reading-exposure.txt`); 葉, 稲, 植, 株 and 村 are not Starter cards. The new sets are 芝 田 木 花, 芽 木 土 雨, 茂 山 川 土, 荘 校 駅 海,
華 月 天 川 and 舎 道 京 雨 (line 13 of each card and the distractor sentences 芝:45, 芽:44, 茂:45, 荘:56, 華:60, 舎:60). 犬 no
longer appears. 花 is not used on 芽 or 華, 土 not on 芝, 校 not on 舎 (校舎), and 生 多 大 長 not on 茂. `checks\quiz-safety.txt`
was rerun.

### C6: “help” on 翼

Author action: **changed**. `翼.md:33`: "Kanjipedia and Digital Daijisen list this reading, meaning to help"; the quoted English
word is gone.

## Optional

- **O1 (author-facing wording): applied.** `臭.md:46`: "The noun 臭い (におい) is a different word and does not show this
  reading." `舎.md:44`: "田舎 (いなか) is read as a whole word, so it does not show any single reading of 舎." For the same reason
  荘's "Do not merge these distinct scopes" is deleted (`荘.md:43`).
- **O2 (艶めく senses): applied.** `艶.md:52` says the senses overlap; the つやめく row adds "look alluring" (`艶.md:35`).
- **O3 (possible exclusions): applied.** 腐 excludes 甘 (JMdict 甘やかす “to pamper; to spoil”) and 傷 (JMdict 傷む “to be spoiled
  (e.g. food)”) (`腐.md:14,49`). 興 excludes 復 (KANJIDIC2 “revive” for 興; `興.md:14,52`). 茂 excludes 豊 (KANJIDIC2 “be
  luxuriant”; JMdict 茂る “to luxuriate; to be luxurious”; `茂.md:14,43`).
- **O4 (weak but harmless exclusions): not applied**, as you judged; exclusions only remove options.
- **O5 (coverage extras): applied in part.** 山脈 and 動脈 (`脈.md:39-40`) and 華やか (`華.md:39`) are added. 静脈, 中華, 芽生える,
  新芽, 茂み, 生い茂る, 色艶 and 艶々 are not added; optional coverage.
- **O6 (Metadata ids without a word): applied.** 脈絡 (`脈.md:38`) and 臨床 (`臨.md:37`) are now named on the cards.
- **O7 (Metadata format): not applied.** `content-format.md` sets no Metadata format; harmonizing is churn for this batch.
- **O8 (脈 attribution): applied.** `脈.md:32-33`: KANJIDIC2 lists すじ, and only Kanjipedia is said to mark すじ and バク outside
  the Jōyō readings. The same misattribution was fixed on 翻 (`翻.md:42`): KANJIDIC2 lists ハン, and Kanjipedia marks it outside the
  Jōyō readings.
- **O9 (dense exclusion paragraphs): applied.** The exclusion paragraphs on 華, 翻, 舎, 荘, 臨 and 艶 are now an intro line and
  short bullets with the same evidence (`華.md:48-56`, `翻.md:44-49`, `舎.md:52-58`, `荘.md:46-52`, `臨.md:45-51`, `艶.md:57-64`).
  The evidence stays on the cards, because the corpus documents each exclusion in the card Notes.
- **O10 (興/起 Jōyō contrast): not applied.** The card does not discuss the ⇔ contrast; adding it is optional.
- **O11 (芝居 quote): applied** as a declared remark edit. `words\芝居.md:27` quotes 芝 as "turf; lawn," (listed in
  `evidence\word-remarks.json`).
- **O12 (脈 ばく): noted.** 脈's distractors 目 手 足 are unchanged; `checks\reading-options.txt` still prints the ばく label.

## Process notes

- `b007a0a6` and `06b2db87` are the two fix commits; `diffs\fix.patch` is the whole change from the reviewed snapshot `070b6f69`.
  `06b2db87` changes only 荘's distractor 京 to 駅 (see `CHANGES.md`).
- The checks in `checks\` were run on the committed revision `06b2db87`.
- The commit also follows the GPT reviewer's findings (not shown to you): the stale sentence in `words\艶.md`, the exclusions 茂/密
  and 茂/盛, and the bullet form of the 臨 and 艶 Notes. See `CHANGES.md` for all changed lines.
