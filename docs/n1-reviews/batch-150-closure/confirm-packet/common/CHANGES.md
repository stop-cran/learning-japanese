# Batch 150 revision: what changed from 2dd9d46b to 7e3c101b

Revised snapshot: `7e3c101b` (full hash `7e3c101b84848bd7a342cb1f44a421cd0f6f73e6`; also in `packet-manifest.json`). It is one
commit after the reviewed snapshot `2dd9d46bca2aa4cc2b439d08c2ef36e6d9067a41`. Nothing is published.

- Ten of the 15 new kanji cards changed (蒔 薦 虚 融 街 衝 裁 裸 視 覧). 葬 蓄 衆 裂 覆, every existing kanji card, every stroke file
  and every word article are unchanged.
- **Front-matter changes (`quiz_exclusions` only, line 14):**
  - removed: 苗 from 蒔 (now `[植, 種, 挿, 散]`); 布 from 裁 (now `[判, 審, 決, 定, 切, 断, 絶, 縫]`); 捜 from 視 (now
    `[見, 観, 看, 眺, 察, 監, 仰, 査, 検]`) and from 覧 (now `[視, 見, 観, 看, 眺, 察, 読, 検, 査, 仰, 監]`).
  - added: 径 to 街 (now `[町, 道, 路, 途, 径, 市, 区, 丁]`); 攻 to 衝 (now `[突, 抵, 撃, 打, 当, 攻, 刺, 押, 推, 争, 戦]`).
  No title, tag, metadata reading, `quizOnyomi`, `quizKunyomi` or `distractors` list changed in any card.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. 蒔 and 裁 each lost one line, so their later line numbers are one
  lower than in the reviewed snapshot; `diffs\changed-lines.txt` maps them.
- `diffs\fix.patch` is the exact patch from `2dd9d46b` to `7e3c101b`. `diffs\changed-lines.txt` lists the changed lines per file.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. The original packet's
  `evidence\audits\` files (quiz safety, reading exposure, reading options) describe the reviewed snapshot and are superseded by this
  packet's `checks\`.

## Changed lines

| File | Changed lines | Change |
| --- | --- | --- |
| 蒔 | 14, 46, old 50 | 14: 苗 no longer excluded. 46: "These four cards". The 苗 bullet (old line 50) is deleted. |
| 薦 | 47, 49 | 47: "JMdict's entry for 推薦 has a see-also cross-reference to 推奨" (the cross-reference is no longer inside gloss quotes). 49: Kanjipedia's second sense is given as こも。敷物。しとね。 "(straw mat; floor covering; a mat to sit or lie on)". |
| 虚 | 23 | The 邪心 sense names each source's wording: "(Kanjipedia: 邪心をもたない; Digital Daijisen: 邪心を持たない)". |
| 融 | 25 | The mnemonic describes 鬲 as "a flat stroke over a small box, which sits on a taller frame with a few strokes inside"; the image says "that tall boxy stack". |
| 街 | 14, 45, 48 | 14: 径 excluded. 45: "These eight cards". 48: 径 (“diameter; path”) joins the 道/路/途 bullet; JMdict's みち is "spelled 道, 途, 路, or 径" (JMdict 1454080). |
| 衝 | 14, 44, 48 | 14: 攻 excluded. 44: "These eleven cards". 48: 攻 (“attack; go on the offensive”) joins the 撃/打/当 bullet, which cites JMdict's 衝く “to hit” and “to attack”. |
| 裁 | 14, 45, old 51 | 14: 布 no longer excluded. 45: "These eight cards". The 布 bullet (old line 51) is deleted. |
| 裸 | 25 | The image is "Imagine a fruit whose clothing, its peel, has been stripped away until it stands bare." |
| 視 | 14, 44, 49 | 14: 捜 no longer excluded. 44: "These nine cards". 49: only 仰 remains in the bullet: "to look up at something is itself to look at it, so its “look up” overlaps the title's “look at.”" |
| 覧 | 14, 25, 43, 50 | 14: 捜 no longer excluded. 25: the mnemonic describes 𠂉 as "a slanting stroke with a short horizontal stroke to its right" and mentions "one more horizontal stroke below it" (KanjiVG stroke 10, outside any group). 43: "These eleven cards". 50: only 仰 remains in the bullet: "looking up at something and looking over something are both ways of looking at it, so its “look up” overlaps the title's “look over.”" |

## Audit tooling

`reading_exposure.py` and `reading_options.py` (workspace audit scripts, not repository files) now label readings passed with
`--extra` as "--extra list" instead of "card text"; the strings were never in the cards. The second line of
`checks\reading-exposure.txt` says what the `--extra` list contains. Counts and collision accounting are unchanged.

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 4 warnings (word articles whose Dictionary line cites no JMdict entry id), as at the freeze.
  `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: rebuilding `manifest.json` leaves it unchanged and the
  tree clean. `budget.txt` and `vocabulary.txt`: informational.
- `linkplan.txt`: 18 changed word files, 18 added link pairs, 0 declared remark edits, 0 problems.
- `kanji-remarks.txt`: 15 new cards, 0 modified existing cards, 0 problems.
- `quiz-safety.txt`: 0 errors, 0 warnings (rerun because six exclusion lists changed). Each of the 15 cards' three curated
  distractors fills every wrong meaning slot; the output is identical to the freeze's.
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, and the same 4 latent collisions as at the freeze (蒔 まい and
  まき, 街 また, 視 み; all KANJIDIC2 name-only readings of the target). The one-holder summary reports 0 ordinary-reading hits and 1
  more for a KANJIDIC2 name-only reading, as at the freeze.
- `reading-options.txt`: 0 problems.
- `evidence\meta-scan.txt`: informational output of `meta_scan.py` on the 15 cards. Compared with the freeze, the 薦 fragment こも・敷物 is
  gone and 虚's quotation 邪心を持たない appears as a fragment.
- The Android JVM tests that read the real content were not run, as at the freeze (no JDK on this machine).

## Process notes

- `7e3c101b` is the single fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `2dd9d46b`.
- The checks in `checks\` were run on the committed revision `7e3c101b`.
