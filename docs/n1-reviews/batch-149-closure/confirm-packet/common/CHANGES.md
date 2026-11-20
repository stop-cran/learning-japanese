# Batch 149 revision: what changed from 070b6f69 to 06b2db87

Revised snapshot: `06b2db87` (full hash `06b2db87bfd9f516f313f63101c40f1fe724f40f`; also in `packet-manifest.json`). It is two
commits after the reviewed snapshot `070b6f694216c7580346cc1b1432519b3284e919`. Nothing is published.

- All 15 new kanji cards changed (翻 翼 脈 腐 臨 臭 興 舌 舎 艶 芝 芽 茂 荘 華). No existing kanji card and no stroke file changed.
- Two word articles changed, each by one declared remark edit (`evidence\word-remarks.json` lists the exact old and new text):
  - `words\艶.md`: the sentence "There is no separate 艶 card in the current collection." is deleted (old line 31).
  - `words\芝居.md:27`: 芝 is quoted as "turf; lawn," (was "grass; turf,"), matching the 芝 card title.
  The other 15 word articles are unchanged from the reviewed snapshot.
- **Front-matter changes (`distractors` and `quiz_exclusions` only):**
  - `distractors` (line 13): 舎 `[雨, 木, 山]` became `[道, 京, 雨]`; 芝 `[犬, 石, 山]` became `[田, 木, 花]`; 芽 `[犬, 山, 水]`
    became `[木, 土, 雨]`; 茂 `[犬, 山, 水]` became `[山, 川, 土]`; 荘 `[犬, 日, 雨]` became `[校, 駅, 海]`; 華 `[犬, 月, 水]` became
    `[月, 天, 川]`. All new distractors are Starter cards.
  - `quiz_exclusions` (line 14): 腐 `[酸]` became `[酸, 甘, 傷]`; 興 gained 復 (now `[娯, 楽, 快, 愉, 歓, 享, 起, 昇, 栄, 盛, 設, 復]`);
    茂 `[]` became `[密, 盛, 豊]`.
  No title, tag, metadata reading, `quizOnyomi` or `quizKunyomi` list changed in any card.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. Several cards gained lines (翻 脈 腐 臨 舎 艶 茂 荘 華), so
  later line numbers differ from the reviewed snapshot; `diffs\changed-lines.txt` maps them.
- `diffs\fix.patch` is the exact patch from `070b6f69` to `06b2db87`. `diffs\changed-lines.txt` lists the changed lines per file.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. The original packet's
  `evidence\audits\` files (quiz safety, reading exposure, reading options, word remarks, kanji remarks) describe the reviewed
  snapshot and are superseded by this packet's `checks\` and `evidence\word-remarks.json`.

## Reading-row label convention

One convention now applies to every Readings row that is not a quiz reading:

- "source-only here" (the spelling already used on existing corpus cards) marks only a reading with no checked JMdict word
  example. The row names the source that lists the reading and says it is "not selected for questions here".
- A reading that has a checked JMdict word example is labelled plain "on" or "kun", gives the example and its entry id, and says
  it is not selected for questions (芝 シ, 芽 めぐむ, 荘 ショウ and チャン, 腐 くさ.す, 華 ケ and ゲ, 翻 ハン, and 艶's extra kun rows).
- 腐 -くさ.る is labelled "kun suffix".

## Changed lines

| File | Changed lines | Change |
| --- | --- | --- |
| 翻 | 32, 42, 44-49 | 32: the ハン row is labelled "on", cites JMdict 2833260 as a mahjong counter and says it is not selected for questions here. 42: KANJIDIC2 lists ハン, and only Kanjipedia is said to mark it outside the Jōyō readings. 44-49: the exclusion paragraph became an intro line and four bullets for the same eight exclusions; 反, 逆 and 転 now carry their quoted titles. |
| 翼 | 33 | たすける is "kun, source-only here"; the quoted English “help” is gone ("list this reading, meaning to help"); not selected for questions here. |
| 脈 | 32-33, 38-40, 50 | 32-33: すじ and バク are "source-only here"; only Kanjipedia is said to mark them outside the Jōyō readings (KANJIDIC2 is said only to list すじ). 38-40: Common words add 脈絡, 山脈 and 動脈. 50: Metadata adds 1303190 (山脈) and 1451580 (動脈). |
| 腐 | 14, 31, 33, 37, 42-43, 47, 49, 53 | 14: 甘 and 傷 excluded. 31: the フ row adds 豆腐 とうふ. 33: "kun suffix". 37: くさ.す is plain "kun", not selected for questions here. 42-43: Common words add 豆腐 and 腐敗. 47: "These additional forms". 49: the 甘 and 傷 exclusions, with JMdict's 甘やかす “to pamper; to spoil” and 傷む “to be spoiled (e.g. food)”. 53: Metadata adds 1450070, 1213470 and 1432710. |
| 臨 | 37, 41-51 | 37: Common words add 臨床. 41-43: the reading and sense paragraph became three bullets (み is a name-only form; the JMdict 臨む glosses; the Kanjipedia senses). 45-51: an intro line and five bullets for the same thirteen exclusions. |
| 臭 | 46 | "Do not use the noun 臭い (におい) to justify that selection." became "The noun 臭い (におい) is a different word and does not show this reading." |
| 興 | 14, 52 | 14: 復 excluded. 52: KANJIDIC2 also lists “revive” for 興, which overlaps 復 (“restore; repeat”); the count is now "All twelve". |
| 舌 | 49 | "none names the tongue, speech, or language" became "none of these titles names the tongue, speech, or language". |
| 舎 | 13, 32-34, 44, 50, 52-60 | 13: new distractors. 32-34: セキ, やど.る and おく are "source-only here", each naming its source. 44: "Do not use 田舎 (いなか) to justify a reading of 舎." became "田舎 (いなか) is read as a whole word, so it does not show any single reading of 舎." 50: the sense paragraph no longer carries the exclusion reasons. 52-58: an intro line and five bullets for the same ten exclusions. 60: the distractor sentence. |
| 艶 | 31-36, 43-45, 52-55, 57-64, 68 | 31-36: each row says whether it is selected; the つや row adds 艶やか つややか; the あでやか row says "usually written in kana"; the つやめく row adds "look alluring". 43-45: Common words add 艶やか (both readings) and 艶めく つやめく. 52-55: reading bullets (the 艶めく senses overlap; 艶やか has two readings). 57-64: an intro line and six bullets for the same twelve exclusions. 68: Metadata adds 2682080. |
| 芝 | 13, 31, 41, 45 | 13: new distractors. 31: シ is labelled "on". 41: "The on-reading シ". 45: the distractor sentence. |
| 芽 | 13, 33, 44 | 13: new distractors. 33: めぐむ is labelled "kun". 44: the distractor sentence. |
| 茂 | 13-14, 43, 45 | 13: new distractors. 14: 密, 盛 and 豊 excluded. 43: a new Notes bullet with the JMdict 茂る glosses and the KANJIDIC2 “grow thick” and “be luxuriant”, naming the three exclusions. 45: the distractor sentence. |
| 荘 | 13, 23, 32-35, 43, 46-56 | 13: new distractors (see Process notes). 23: the ツ of 別 (ベツ) becomes a small っ before ソウ: べっそう. 32-33: ショウ and チャン are labelled "on". 34-35: ほうき and おごそ.か are "source-only here". 43: "Do not merge these distinct scopes" is deleted. The old exclusion paragraph (old line 45) is deleted; 46-52 are an intro line and bullets for the same eight exclusions. 54: the 舎/荘 pair is declared on 舎. 56: the distractor sentence. |
| 華 | 13, 32, 34, 39, 46, 48-60 | 13: new distractors. 32 and 34: ケ and ゲ are labelled "on". 39: Common words add 華やか. 46: the bullet keeps only the quiz-selection sentence. 48-56: an intro line and bullets for the same ten exclusions. 58: the 艶/華 pair is declared on 艶. 60: the distractor sentence. |
| words/艶 | old 31 | The stale sentence "There is no separate 艶 card in the current collection." is deleted. |
| words/芝居 | 27 | 芝 is quoted as "turf; lawn," (was "grass; turf,"). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 3 warnings (the word articles 校舎, 翻訳 and 艶: no JMdict entry id on the Dictionary line), as at the
  freeze. `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: rebuilding `manifest.json` leaves it unchanged
  and the tree clean. `budget.txt` and `vocabulary.txt`: informational.
- `linkplan.txt`: 17 changed word files, 17 added link pairs, 2 declared remark edits, 0 problems (checked against
  `evidence\word-remarks.json`).
- `kanji-remarks.txt`: 15 new cards, 0 modified existing cards, 0 problems.
- `quiz-safety.txt`: 0 errors, 0 warnings (rerun because distractors and exclusions changed).
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, and the same 16 latent collisions as at the freeze. For each of 舎 芝 芽
  茂 荘 華 the curated options fill all three wrong slots in every outcome in all three pools.
- `reading-options.txt`: 1 problem, as at the freeze: 脈 ばく, a label the script prints because it ignores curated slots;
  脈's three curated Starter options (目 手 足) fill every wrong slot, so ばく is not drawable. The 荘 block has an
  "info (can be drawn)" line for そ, a KANJIDIC2 name-only reading; it is the same static label, and the simulation sees only the four
  curated readings. `reading-exposure.txt` lists そ for 荘 as a latent collision.
- `evidence\meta-scan.txt`: informational output of `meta_scan.py` on the 15 cards.
- The Android JVM tests that read the real content were not run, as at the freeze (no JDK on this machine).

## Process notes

- `b007a0a6` and `06b2db87` are the two fix commits; `diffs\fix.patch` is the whole change from the reviewed snapshot `070b6f69`.
  `06b2db87` changes only 荘's distractor 京 to 駅 (line 13 and the distractor sentence on line 56): with 校 and 京, both read
  キョウ, one of six reading-quiz outcomes had an open wrong slot, and the fallback could fill it with そ, a KANJIDIC2 name-only
  reading of 荘.
- The checks in `checks\` were run on the committed revision `06b2db87`.
