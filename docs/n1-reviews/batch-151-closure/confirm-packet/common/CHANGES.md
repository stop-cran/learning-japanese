# Batch 151 revision: what changed from b624890f to 15441514

Revised snapshot: `15441514` (full hash `15441514ec9a0a3835921e2031f7d79bec6c8920`; also in `packet-manifest.json`). It is one
commit after the reviewed snapshot `b624890f8aea8cfb6b5a08ee6beff21df5f8c807`. Nothing is published.

- Nine of the 15 new kanji cards changed (誓 誘 謙 譲 護 豆 豪 貢 貴). 訴 証 詩 詳 誇 謡, every existing kanji card (including
  the ten remark edits), every stroke file and every word article are unchanged.
- **Front-matter changes:**
  - 誘 `quiz_exclusions` (line 14): 訪 removed; now `[招, 惑, 導, 率, 連, 呼, 請, 問, 聞, 伺, 促, 勧, 艶]`.
  - 譲 `distractors` (line 13): `[食, 行, 来]` replaced by `[買, 話, 読]`.
  No title, tag, metadata reading, `quizOnyomi` or `quizKunyomi` changed in any card.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. No card gained or lost a line, so every line number is the same
  as in the reviewed snapshot. `diffs\fix.patch` is the exact patch from `b624890f` to `15441514`; `diffs\changed-lines.txt`
  lists the changed lines per file.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. The original packet's
  `evidence\audits\` files (quiz safety, reading exposure, reading options) describe the reviewed snapshot and are superseded by this
  packet's `checks\`.

## Changed lines

| File | Changed lines | Change |
| --- | --- | --- |
| 誓 | 32, 33 | The ゼイ row moves up to line 32, directly after the セイ row (31); the ちか.う row is now line 33. Neither row's text changed. |
| 誘 | 14, 45, 51, 59 | 14: 訪 no longer excluded. 45: "These thirteen cards". 51: the bullet is now only 呼: "[呼](呼.md) (“call out”): JMdict 誘う includes “to call (for)”, and JMdict 呼ぶ sense 3 is “to invite” (entry 1266440)." 59: JMdict entry 1266440 added to the Metadata ids. |
| 謙 | 25 | The mnemonic accounts for every stroke of 兼: after 八 at its top come "then a horizontal stroke, the shape ⺕, two vertical strokes 丨 and two final sweeping strokes." |
| 譲 | 13, 57 | 13: distractors 買 話 読. 57: "The meaning-quiz distractors are 買 (“buy”), 話 (“talk, speak”), and 読 (“read”). Buying is the other side of selling (譲る can mean “to sell”), and 話 and 読 share the radical 言 with 譲, but none of them means handing over or yielding." |
| 護 | 23, 51 | 23: "The example word 看護婦" (was "declaring word"). 51: "both characters appear in the example word 看護婦" (was "write the declaring word"). |
| 豆 | 23 | "The example word 豆" (was "declaring word"). |
| 豪 | 23, 52 | 23: "The example word 豪華". 52: "both characters appear in the example word 豪華". |
| 貢 | 23, 46 | 23: "In the example word 貢献". 46: "both characters appear in the example word 貢献". |
| 貴 | 23, 25 | 23: "The example word 貴重". 25: the mnemonic's 中 "sits at the top on a horizontal stroke 一" above 貝 (KanjiVG stroke 5). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 19 warnings (legacy word articles whose Dictionary line cites no JMdict entry id), as at the freeze.
  `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: rebuilding `manifest.json` leaves it unchanged and the
  tree clean. `budget.txt` and `vocabulary.txt`: informational.
- `linkplan.txt`: 19 changed word files, 19 added link pairs, 0 problems, as at the freeze.
- `kanji-remarks.txt`: 15 new cards, 10 modified existing cards, 10 declared remark edits applied, 0 problems, as at the freeze.
- `quiz-safety.txt`: 0 errors, 0 warnings. The only difference from the freeze is 譲's options line: "buy | talk, speak | read"
  instead of "eat, food | go | come". 誘's three curated distractors still fill every wrong meaning slot.
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, the same 3 latent collisions as at the freeze (詳 よし,
  譲 せめる, 貴 ぎ) and 0 one-holder hits. The only differences from the freeze are in the 譲 section: the curated cards are
  買 話 読, and its kun prompt ゆず.る now has 4 drawable wrong options (かう, はなす, はなし, よむ) instead of 11.
- `reading-options.txt`: 0 problems; the 譲 section changes in the same way.
- `evidence\meta-scan.txt`: informational output of `meta_scan.py` on the 15 cards; identical to the freeze apart from the
  command line.
- `evidence\distractor-trials.txt`: how the replacement for 譲's distractors was chosen (see the author's statement).
- The Android JVM tests that read the real content were not run, as at the freeze (no JDK on this machine).

## Process notes

- `15441514` is the single fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `b624890f`.
- The checks in `checks\` were run on the committed revision `15441514`.
