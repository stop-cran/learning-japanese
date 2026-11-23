# Batch 148 revision: what changed from 8408b3a5 to cc286cc3

Revised snapshot: `cc286cc3` (full hash `cc286cc34ca20370000e6c042a2dbb045cac3d99`; also in `packet-manifest.json`). It is one
commit after the reviewed snapshot `8408b3a5a52cccea74fe2eaf65601568968b6b26`. Nothing is published.

- Eleven new kanji cards changed (継 綱 緊 締 緯 縁 縄 縦 織 繕 罰). The other four new cards (絞 緩 縛 繰), the three
  modified existing cards (張 慢 修), all 17 word articles and all 15 stroke files are unchanged from the reviewed snapshot.
- **Front-matter changes (quiz_exclusions only):**
  - 緊: 筋 replaced by 縛 (`[張, 急, 密, 詰, 勁, 硬, 固, 堅, 縮, 圧, 要, 筋]` became `[張, 急, 密, 詰, 勁, 硬, 固, 堅, 縮, 圧, 要, 縛]`).
  - 罰: 犯 removed (now `[刑, 罪, 償, 責, 処]`).
  - 緯: 経 and 織 removed (now `[横, 糸, 線]`).
  - 綱: 科 removed (now `[縄, 索, 緒, 概, 旨, 要, 線, 級, 類, 般]`).
  - 縦: 経 added (now `[垂, 長, 高, 任, 従, 経]`).
  No title, tag, metadata reading or `distractors` list changed in any card.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. No card gained or lost a line.
- `diffs\fix.patch` is the exact patch from `8408b3a5` to `cc286cc3`. `diffs\changed-lines.txt` lists the changed lines per file.
- No Metadata line changed. New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file.

| File | Changed lines | Change |
| --- | --- | --- |
| 継 | 25 | Sense 1 now reads "to take over from what came before and carry it on" (was "take over what follows"). |
| 綱 | 14, 53-54 | Line 14: 科 removed. Line 53: the overlap note no longer names 科. Line 54: 海 and 夏 are said to have short two-kana kun readings (うみ, なつ). |
| 緊 | 14, 54 | Line 14: 筋 replaced by 縛. Line 54: 筋 is no longer named as an overlap; 縛 is named, with its title. |
| 締 | 25, 40, 51-52 | Line 25: the Daijisen テイ senses are paraphrased without quotation marks. Line 40: 締 supplies し (め is okurigana) and 切 supplies き (り and る are okurigana); the "quiz tool" sentence is deleted. Line 51: the raw entry id of 閉める is removed. Line 52: the "tie" and "conclude an agreement" quotation marks are removed. |
| 緯 | 14, 54 | Line 14: 経 and 織 removed. Line 54: 経 is described as the warp partner and said not to be excluded; 織 is no longer named; only 横 糸 線 are said to be kept out. |
| 縁 | 49, 59 | Lines 49 and 59: in 縁取る, 縁 supplies ふち, 取 supplies ど (the voiced form of と) and only る is okurigana; JMdict also spells the word 縁どる. |
| 縄 | 55 | The last Notes bullet now says Daijisen, like the Joyo table, prints the traditional form 繩 in brackets. |
| 縦 | 14, 53, 56 | Line 14: 経 added. Line 53: 経 is named as the warp thread with たていと and as overlapping the vertical sense. Line 56: the 経 spelling is described as a JMdict spelling tagged "rarely used kanji form". |
| 織 | 28, 32 | Line 28: the 織豊時代 gloss is quoted as "Shokuhō period (i.e. the Azuchi-Momoyama period, approx. 1568-1600)" and "historical term" is given as a tag. Line 32: the mnemonic says a 戈-like shape beside 音. |
| 繕 | 47 | The comparison with 継 now says 繕 is about mending and putting things in order (was "only about mending"). |
| 罰 | 14, 55, 57-58 | Line 14: 犯 removed. Line 55: the overlap note no longer names 犯. Lines 57-58: the examples promised at the start are now listed (罰金 罰則 刑罰 厳罰 重罰 賞罰 体罰; 処罰 懲罰 信賞必罰; 神罰 天罰 冥罰), and the fragment is a full sentence. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the existing word articles 綱, 緯度 and 威張る: "Dictionary: line cites no JMdict entry id"),
  as at the freeze. `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: `manifest.json` regenerated,
  rebuild idempotent. `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `quiz-safety.txt`: 0 errors, 0 warnings (rerun because exclusions changed).
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, 9 latent collisions, as at the freeze.
- `reading-options.txt`: 0 problems, as at the freeze.
- The Android JVM tests that read the real content were not run, as at the freeze.

## Process notes

- `cc286cc3` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `8408b3a5`.
- The checks in `checks\` were run on the committed revision `cc286cc3`.
