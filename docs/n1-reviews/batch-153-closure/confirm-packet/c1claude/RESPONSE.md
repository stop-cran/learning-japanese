# Author's statement for the reviewer of `reports-153\initial-claude.md`

This statement answers only the points in YOUR initial report. Your report has no Findings; your Optional list has six items,
O1 to O6, and they are answered below. The statement is the author's claim about what changed and why. Verify each claim against
the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet. Four of the 15 new cards changed (醜 釈 鎖 陥); 酌 酔 酢 釣
鈴 銃 銭 鐘 鑑 附 陰, every existing kanji card (including the remark edit on 属), every stroke file and every word article are
unchanged. The only front-matter change is 陥's `quiz_exclusions`, which gained 捕 and 釣; no title, tag, `distractors` list,
metadata reading, `quizOnyomi` or `quizKunyomi` changed. See `CHANGES.md`. Give a disposition for each of O1 to O6.

## Optional

- **O1 (鐘, シュ row order): not changed.** On the N1 cards, a reading that is not in KANJIDIC2 gets its row after the KANJIDIC2
  rows, on and kun alike. Examples are 華 (ゲ after はな), 覆 (フウ and フ after the kun rows) and, in this batch, 附 (ブ after つ.く).
  On 鐘, ショウ and かね are the KANJIDIC2 readings and シュ comes from Kanjipedia and Digital Daijisen, so it comes last.
- **O2 (醜, Joyo note): applied.** `醜.md:41` now ends the Joyo sentence with "and みにくい, with 醜い and 醜さ みにくさ." The Joyo
  table (PDF p. 74, row 醜) prints "みにくい 醜い，醜さ". 醜さ has no JMdict entry of its own, so no entry id was added.
- **O3 (釈, Common words): applied, both words.** `釈.md:40` adds "釈放 しゃくほう — release; liberation; acquittal" (JMdict
  1324260, which the Metadata line already cited). `釈.md:41` adds "会釈 えしゃく — slight bow; nod", shortened from JMdict 1198600
  sense 1, "slight bow (as a greeting or sign of gratitude); nod; salutation". Entry 1198600 is added to the Metadata ids
  (`釈.md:66`). Neither word has an article, so the bullets are plain text, as on many existing cards.
- **O4 (鎖, じょう): applied, as a Notes line.** `鎖.md:43` reads: "Digital Daijisen also lists 鎖 under the headword
  じょう【錠／▽鎖／×鏁】, a lock that is opened and closed with a key, and its note says this sense was originally written 鎖, with 錠
  applied later. JMdict entry 1633480, headed 錠 じょう (“lock; padlock”), lists 鎖 as a rarely used kanji form. じょう is not a
  KANJIDIC2 reading and has no table row here." The Daijisen entry's sense 1 is 他人に開けられないように、ドア・引き出し・金庫などに
  取り付け、鍵(かぎ)で開閉する装置, and its [補説] reads 1 は本来「鎖」であるが、後世「錠」の字を当てるようになった
  (`evidence\daijisen-joo.txt`). Entry 1633480 is added to the Metadata ids (`鎖.md:58`). There is no 錠, 鍵 or 鑰 card, so the
  note creates no new meaning-choice pair.
- **O5 (weak exclusions): not changed.** As you say, each of these pairs rests on a cited source sense. An extra exclusion only
  shrinks the pool that fills empty slots, and each of these cards keeps its three curated distractors, which fill every wrong
  meaning slot (`checks\quiz-safety.txt`). Removing a sourced pair would make a learner's defensible answer possible again in custom
  pools.
- **O6 (鎖 audit lacked じょう): fixed in the audit tooling; no card change.** The root cause was the parser that builds
  `daijisen-heads.txt`, the list of Digital Daijisen headwords from which the audit `--extra` lists are derived. It did not accept
  katakana or ｜ inside the 〔〕 kana note, so it cut short headwords such as じょう〔ヂヤウ｜ジヤウ〕【錠／▽鎖／×鏁】. With the
  parser fixed, only two headword lines change, 醜 しゅう〔シウ〕 and 鎖 じょう; the only `--extra` change is that 鎖 gains じょう
  (`evidence\daijisen-heads-diff.txt`). In `checks\reading-exposure.txt` and `checks\reading-options.txt`, じょう for 鎖 is now
  marked "--extra list". The totals are the same as at the freeze. The freeze audit had already listed じょう as attested for 鎖,
  from JMdict 1633480, without a collision line, and that is still so: 鎖's only reading prompt is the kun くさり, and no card offers
  じょう as a kun quiz reading. Nineteen cards offer it as an on reading (`evidence\joo-holders.txt`). Re-running the fixed parser on the headwords of batches 144 to 152 found
  one reading not already on a card: 益 よう (batch 146). Batch 146's own audit had already tested it, from JMdict 1576560. With
  `--extra 益=よう`, `reading_exposure.py` on `3f8b951d` reports 0 production, 0 padded-session and 0 one-holder hits. The only
  result is 1 latent collision: "it cannot be drawn in the N1 stack, All stack or Starter practice session pool", nor in a Starter
  session that also borrows one card that offers よう ("18 holders tried"; `evidence\retro-check-yoh.txt`). No card changed.

## Other changes in this revision (from the other review)

You did not raise these; they are listed so that every hunk is accounted for. 陥 now excludes 捕 (“capture”) and 釣 (“angling;
lure”) (`陥.md:14`), "These fourteen cards" (`陥.md:44`), with the new bullet at `陥.md:52`: "JMdict glosses 陥れる おとしいれる
with “to lure (into a trap)” and “to capture (a castle, fortress, etc.)” (entry 1216130)." Entry 1216130 was already in the
Metadata ids and in the Readings row at `陥.md:33`. 捕 and 釣 are unchanged; each pair is declared once, on 陥. Neither of them is a
curated distractor of 陥, and 陥 is not a curated distractor of either.
