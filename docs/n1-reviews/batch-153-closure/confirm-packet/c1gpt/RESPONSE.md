# Author's statement for the reviewer of `reports-153\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 is your report's Finding. Your Optional section has two bullets,
called GO1 (shorten the provenance-heavy exclusion explanations, especially on 鑑 and 附) and GO2 (the unusually easy Starter-level
distractors for 醜, 釈 and 附) below. L1 is the first item in your Limits: the unresolved link from 酢 to
`../articles/compound-sound-changes.md`. The statement is the author's claim about what changed and why. Verify each claim against
the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet. Four of the 15 new cards changed (醜 釈 鎖 陥); 酌 酔 酢 釣
鈴 銃 銭 鐘 鑑 附 陰, every existing kanji card (including the remark edit on 属), every stroke file and every word article are
unchanged. The only front-matter change is 陥's `quiz_exclusions`, which gained 捕 and 釣; no title, tag, `distractors` list,
metadata reading, `quizOnyomi` or `quizKunyomi` changed. See `CHANGES.md`. Give a disposition for each of G1, GO1, GO2 and L1.

## Findings

### G1: missing direct exclusions on 陥

Author action: **changed** as you proposed; both pairs are declared once, on 陥.

- `陥.md:14` is now `quiz_exclusions: [落, 崩, 倒, 沈, 凹, 欠, 乏, 誤, 穴, 捕, 釣, 敗, 負, 滑]`, and `陥.md:44` reads "These
  fourteen cards are excluded from meaning choices:".
- The new bullet at `陥.md:52` reads: "[捕](捕.md) (“capture”) and [釣](釣.md) (“angling; lure”): JMdict glosses 陥れる おとしいれる
  with “to lure (into a trap)” and “to capture (a castle, fortress, etc.)” (entry 1216130)." In JMdict 1216130, “to lure (into a
  trap)” is in sense 1 and “to capture (a castle, fortress, etc.)” begins sense 2. Entry 1216130 was already in the Metadata ids and
  in the Readings row at `陥.md:33`.
- 捕 and 釣 are unchanged. Neither declared 陥 (釣 excludes 魚 漁 捕 誘 艶; 捕 declares no exclusions). The curated distractors are
  unchanged: 陥 has 昇 跳 浮, 捕 has 指 掛 折 and 釣 has 刈 掘 潜, so none of the three is a curated distractor of another.
  `checks\quiz-safety.txt` still shows 陥's meaning options as its three curated titles. Under
  `docs/content-format.md`'s rule that a declaration on either card excludes the direct pair, your custom pools `{陥, 捕, 酢, 鈴}` and
  `{陥, 釣, 酢, 鈴}` can no longer offer “capture” or “angling; lure” for 陥. Nor can they offer 陥's title for 捕 or 釣.

## Optional

- **GO1 (shorter exclusion notes on 鑑 and 附): not changed.** Each excluded card gets one bullet with its source reason. This is
  the Notes format across the existing N1 cards, and it is what lets a reviewer check each pair without leaving the card. Compressing
  the bullets on two cards of one batch would make them inconsistent with the rest. Shortening them is a style question for the
  whole corpus, not a defect of this batch.
- **GO2 (easy Starter-level distractors for 醜, 釈 and 附): not changed.** As you note, they are plausible and unambiguously wrong.
  They also matter for the reading quiz. Their readings fill all three wrong reading slots of these cards
  (`checks\quiz-safety.txt`: "wrong options from distractors 3/3"). `checks\reading-exposure.txt` reports that the other cards that
  offer 醜's たぐい (双 類) or 釈's おく (億 屋 憶) "cannot be drawn in the N1 stack, All stack or Starter practice session pool", and
  it reports 0 one-holder hits. Harder replacements would need a fresh reading-safety audit for a gain that is only editorial.

## Limits

- **L1 (酢's link to `../articles/compound-sound-changes.md`): verified, no change needed.** The link is at `酢.md:40`. The article
  is tracked in the repository with the same blob at the reviewed snapshot and at this revision
  (`6d5e1f06fba93f5db9b3a518fd21ec854abe5f11`). It is headed "Sound changes in Japanese compounds" and has a section "Rendaku:
  voicing a later element". It is also linked from the existing cards 井, 傑, 貢, 載, 輩 and 遣. This packet includes it unchanged as
  `evidence\compound-sound-changes.md`. The published copy is at
  https://github.com/stop-cran/learning-japanese/blob/main/articles/compound-sound-changes.md.

## Other changes in this revision (from the other review)

You did not raise these; they are listed so that every hunk is accounted for.

- `醜.md:41`: the Joyo note now ends "and みにくい, with 醜い and 醜さ みにくさ". The Joyo table, p. 74, prints "みにくい 醜い，醜さ".
- `釈.md:40-41`: the Common words add "釈放 しゃくほう — release; liberation; acquittal" (JMdict 1324260, already cited) and
  "会釈 えしゃく — slight bow; nod" (JMdict 1198600 sense 1, "slight bow (as a greeting or sign of gratitude); nod; salutation").
  1198600 is added to the Metadata ids (`釈.md:66`).
- `鎖.md:43`: a new Notes line says that Digital Daijisen lists 鎖 under the headword じょう【錠／▽鎖／×鏁】, "a lock that is opened
  and closed with a key". The line also says that the entry's note calls 鎖 the original spelling, with 錠 applied later, and that
  JMdict 1633480 (錠 じょう, “lock; padlock”) lists 鎖 as a rarely used kanji form. じょう is not a KANJIDIC2 reading and has no table
  row; the Daijisen text is in `evidence\daijisen-joo.txt`. 1633480 is added to the Metadata ids (`鎖.md:58`).
- In the audit tooling (no repository file), the parser that builds the list of Digital Daijisen headwords is fixed. It used to cut
  short headwords whose 〔〕 kana note contains katakana or ｜. As a result, the audit `--extra` list for 鎖 now includes じょう;
  the audit totals are unchanged (`evidence\daijisen-heads-diff.txt`).
