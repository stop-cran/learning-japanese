# Batch 146 revision: what changed from 38833c7f to 872d6502

Revised snapshot: `872d6502` (full hash `872d6502c5fd1be09df200017fca607456a20321`; also in `packet-manifest.json`). It is
reached from the reviewed snapshot `38833c7f58bdd2406dbb808c6b2a74257ef29f12` by two commits, `5e61ef07` and `872d6502`;
`diffs\fix.patch` is their combined patch. The second commit changes only 甚 (lines 34, 35, 41), 牧 (line 54) and 盛 (line 37),
after a Claude confirmation of `5e61ef07`. Nothing is published.

- Nine new kanji cards changed (煮 熟 牧 玄 甚 癖 益 盛 睡). The other six new cards (狂 狭 献 環 盾 眺), the existing 潔
  card, all word articles and all 15 stroke files are unchanged from the reviewed snapshot.
- **One front-matter change:** the `quiz_exclusions` list of 牧 shrank from 17 to 12 kanji (5 removed: 治 御 官 司 導).
  No title, tag, metadata reading or `distractors` list changed in any card.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. No card gained or lost a line.
- `diffs\fix.patch` is the exact patch from `38833c7f` to `872d6502`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- No Metadata line changed.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 煮 | 36, 39 | Line 36: the に.える row no longer cites "the repo's aligner"; it says に.える shares the stem に with に.る, so it is not selected as a separate reading. Line 39: 煮凝り にこごり is now 煮 に + 凝り こごり; only 煮麺 にゅうめん is called a whole-word reading. |
| 熟 | 51 | The sentence now speaks of the one linked word 熟語 (other kanji 語, ゴ) and of "the examples without word articles" 熟練 (練, レン) and 熟慮 (慮, リョ; no card here). |
| 牧 | 14, 53-54 | Line 14: `quiz_exclusions` is now `[畜, 養, 育, 農, 牛, 馬, 羊, 草, 野, 僧, 坊, 師]` (12; was 17). Line 53: kana added for 牧童 ぼくどう and 牧羊 ぼくよう, and a livestock-overlap statement for 畜 養 育 農 牛 馬 羊 草 野. Line 54: the title's "pastor" overlaps 僧 坊 師; the Daijisen "govern" and official senses are shared with 治 御 官 司 導, but are not in the displayed title, so those five are no longer excluded. The title is unchanged. The wording of the exclusion count on line 54 is the final one (the nine kanji of the previous bullet and these three). |
| 玄 | 34 | The mnemonic says a two-stroke lid (was "cap stroke"). |
| 甚 | 33, 34, 35, 37, 41 | Line 33: ジン is plain `on` (was "on, source-only here"). Line 34: the はなは.だ row says 甚だしい is spelled with the longer ending だしい and shares the stem はなは with this reading. Line 35: the はなは.だしい row says 甚 writes はなは and だしい is okurigana and that it shares the stem はなは with はなは.だ, so it is not selected separately. Line 37: the okurigana paragraph is rewritten (甚だしい: はなは + だしい; 甚だ: はなは + だ; KANJIDIC2 lists はなは.だ and はなは.だしい) with no aligner wording. Line 41: the Joyo paragraph says "Practice selects はなは.だ; the linked word article 甚だしい has the same stem はなは." |
| 癖 | 33, 37 | Line 33: ヘキ is plain `on`. Line 37: くせ "often becomes ぐせ" (口癖, 酒癖), 手癖 is てくせ or てぐせ, 難癖 keeps くせ; in 潔癖 ヘキ becomes ペキ after the small っ; "the 潔 card links back here for it". |
| 益 | 43 | 益体 やくたい is 益 ヤク + 体 タイ; 益荒男 ますらお is the whole-word reading. |
| 盛 | 36, 37, 39, 43 | Lines 36-37: 盛り stays on the さか.る row; 盛ん is linked on the さか.ん row (glossed "active; JMdict "prosperous; flourishing; thriving; successful""), which says it shares the stem さか with さか.る and is not selected separately. Line 39: the aligner sentences are gone. Line 43: the Joyo paragraph says さか.ん has the same stem さか as さか.る. |
| 睡 | 37 | 昏睡 "has no word article here" (the aligner wording is gone). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter (16 kanji cards: the 15 new cards and the modified 潔; 25 word articles touched by the
  batch): 0 errors, 3 warnings, all Dictionary lines that cite no JMdict entry id on existing word articles (煮る,
  矛盾, 不潔). The same three were reported at the freeze. With `--no-jmdict` there are 0 warnings.
- `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes. `manifest.txt`: `manifest.json`
  regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt`: 23 added link pairs expected and found, 0 problems.
- `kanji-remarks.txt`: 15 of 15 new cards present; one modified existing card (潔), its declared remark edit applied,
  0 problems.
- The Android app's JVM tests that read the real content were not run for this revision either, and the Kotlin
  cross-check of the reading audit was not run, as at the freeze.

### Quiz and reading audits

`quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt` were rerun at `872d6502`:

- `quiz-safety.txt`: 0 errors, 0 warnings (the 牧 exclusion list changed, so the simulation was rerun).
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, 0 one-holder padded hits, and 10 latent collisions
  (9 distinct pairs), as at the freeze.
- `reading-options.txt`: 0 problems.

## Process notes

- `5e61ef07` and `872d6502` are the two fix commits; `diffs\fix.patch` is the whole change from the reviewed snapshot `38833c7f`.
- The checks in `checks\` were run on the committed revision.
