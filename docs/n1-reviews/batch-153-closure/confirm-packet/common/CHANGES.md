# Batch 153 revision: what changed from cdab83b3 to 3f8b951d

Revised snapshot: `3f8b951d` (full hash `3f8b951d38944704afbc74ed8e874e464b579956`; also in `packet-manifest.json`). It is one
commit after the reviewed snapshot `cdab83b375e68d14d6d58a4866959611e949c41a`. Nothing is published.

- Four of the 15 new kanji cards changed (醜 釈 鎖 陥). 酌 酔 酢 釣 鈴 銃 銭 鐘 鑑 附 陰, every existing kanji card (including the
  remark edit on 属), every stroke file and every word article are unchanged.
- **Front-matter changes:** only 陥's `quiz_exclusions` (line 14) changed. It gained 捕 and 釣, and nothing was removed:
  `[落, 崩, 倒, 沈, 凹, 欠, 乏, 誤, 穴, 捕, 釣, 敗, 負, 滑]`. No title, tag, `distractors` list, metadata reading, `quizOnyomi` or
  `quizKunyomi` changed in any card. No existing card's front matter changed. Each new pair is declared once, on 陥; 捕 and 釣 do
  not declare 陥.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. Three cards gained lines, so their later lines moved down: 釈 +2
  from line 40, 鎖 +1 from line 43 and 陥 +1 from line 52. 醜 kept its line numbers. `diffs\fix.patch` is the exact patch from
  `cdab83b3` to `3f8b951d`; `diffs\changed-lines.txt` lists the changed lines per file.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. The original packet's
  `evidence\audits\` files (quiz safety, reading exposure, reading options) describe the reviewed snapshot and are superseded by this
  packet's `checks\`.

## Changed lines

| File | Changed lines | Change |
| --- | --- | --- |
| 醜 | 41 | The Joyo note now ends "and みにくい, with 醜い and 醜さ みにくさ." (was "with 醜い."). |
| 釈 | 40, 41, 66 | 40 (new): "釈放 しゃくほう — release; liberation; acquittal". 41 (new): "会釈 えしゃく — slight bow; nod". 66: JMdict entry 1198600 added to the Metadata ids (1324260, 釈放, was already cited). |
| 鎖 | 43, 58 | 43 (new): "Digital Daijisen also lists 鎖 under the headword じょう【錠／▽鎖／×鏁】, a lock that is opened and closed with a key, and its note says this sense was originally written 鎖, with 錠 applied later. JMdict entry 1633480, headed 錠 じょう (“lock; padlock”), lists 鎖 as a rarely used kanji form. じょう is not a KANJIDIC2 reading and has no table row here." 58: entry 1633480 added to the Metadata ids. |
| 陥 | 14, 44, 52 | 14: 捕 釣 excluded. 44: "These fourteen cards". 52 (new): "[捕](捕.md) (“capture”) and [釣](釣.md) (“angling; lure”): JMdict glosses 陥れる おとしいれる with “to lure (into a trap)” and “to capture (a castle, fortress, etc.)” (entry 1216130)." Entry 1216130 was already in the Metadata ids. |

## Audit tooling change (no repository file)

The parser that builds the Digital Daijisen headword list for the audits' `--extra` readings did not accept katakana or ｜ inside
the 〔〕 kana note, so it cut short headwords such as じょう〔ヂヤウ｜ジヤウ〕【錠／▽鎖／×鏁】. It is fixed. In the regenerated list
only the 醜 しゅう〔シウ〕 and 鎖 じょう lines change, and the only `--extra` change is that 鎖 gains じょう
(`evidence\daijisen-heads-diff.txt`). The fixed parser was also run on the headword lists of batches 144 to 152. It found one reading
not already on a card, 益 よう; see `evidence\retro-check-yoh.txt`.

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the word articles 日陰, 醜い and 鑑賞, whose Dictionary line cites no JMdict entry id), as at
  the freeze. `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: rebuilding `manifest.json` leaves it
  unchanged and the tree clean. `budget.txt` and `vocabulary.txt`: informational.
- `linkplan.txt`: 20 changed word files, 20 added link pairs, 0 problems, as at the freeze.
- `kanji-remarks.txt`: 15 new cards, 1 modified existing card (属), 1 declared remark edit applied, 0 problems, as at the freeze.
- `quiz-safety.txt`: 0 errors, 0 warnings; identical to the freeze. 陥's meaning options are still its three curated titles, and
  neither 捕 nor 釣 is a curated distractor of any batch card.
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, the same 8 latent collisions and 0 one-holder hits, as at the
  freeze. Apart from the command line, the only difference is that じょう, attested for 鎖, is now marked "--extra list" as well as
  JMdict 1633480. It has no collision line, because 鎖's only reading prompt is the kun くさり and no card offers じょう as a kun quiz
  reading (`evidence\joo-holders.txt`).
- `reading-options.txt`: apart from the command line, the only difference is that 鎖's attested readings now include じょう, with no
  note. Its 2 problems are the ones at the freeze: 醜 たぐい, offered by 双 類, and 釈 おく, offered by 億 屋 憶. As the original
  packet's `INSTRUCTIONS.md` says, its HIT label ignores slots already filled by curated distractors. `reading-exposure.txt`, which
  models the pools the app builds, reports that neither reading can be drawn in the N1 stack, All stack or Starter practice session
  pool.
- The Android JVM tests that read the real content were not run, as at the freeze (no JDK on this machine).

## Process notes

- `3f8b951d` is the single fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `cdab83b3`.
- After the reviews, the author found that the first version of the fix quoted the Daijisen headword in `鎖.md:43` as
  じょう【錠／▽鎖】, without ×鏁. The unpublished fix commit was amended to quote it in full. `3f8b951d` is the amended commit.
- The checks in `checks\` were run on the committed revision `3f8b951d`.
