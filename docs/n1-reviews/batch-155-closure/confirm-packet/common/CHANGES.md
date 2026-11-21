# Batch 155 revision: what changed from 97c49eb2 to 25609582

Revised snapshot: `25609582` (full hash `25609582e7d44eed71b10b3fe8ab7e9a5a3931e9`; also in `packet-manifest.json`). It is one
commit after the reviewed snapshot `97c49eb27abbd2961ed93de7c67ece0fa53b5c8a`. Nothing is published.

- All six new kanji cards changed (卑 汰 沙 沢 胡 鼓). Every existing kanji card, every stroke file and every word article (including
  the link edits on 卑怯, 太鼓, 胡椒, 贅沢, 無沙汰 and 御無沙汰, and the declared remark edit on 無沙汰) are unchanged.
- **Front-matter changes:** only two `quiz_exclusions` lists changed, and each only lost one entry.
  - 卑 (line 14) lost 底: `[低, 下, 劣, 汚, 謙, 凡, 粗, 貧, 悪, 近, 軽]`.
  - 沙 (line 14) lost 漠: `[砂, 岸, 粒, 石, 汰, 択, 選, 洗, 濯]`.

  No title, tag, `distractors` list, metadata reading, `quizOnyomi` or `quizKunyomi` changed in any card. No existing card's front
  matter changed. 底 declares no `quiz_exclusions` and 漠 declares only `[広, 荒]`, and no other card lists 卑 or 沙 in its
  `quiz_exclusions` or `distractors`, so after this change neither the 卑/底 pair nor the 沙/漠 pair is excluded by any card.
- **Learner text:** on every card, the line-23 Meaning paragraph and the `## Notes` section were rewritten in shorter, plain English.
  The Readings table, Common words, mnemonic, distractor sentence and links are unchanged. Each group of excluded cards now has one
  short reason with kana-supported glosses instead of a source-by-source proof for each card.
- **Editorial proofs moved off the cards:** `evidence\exclusion-proofs.md` holds, for each card, the line-23 paragraph and the
  `## Notes` section exactly as they were at `97c49eb2`, plus a final section on the two removed exclusions. It records the source
  comparisons that the cards no longer carry. It is review evidence, not learner content, and will be filed with the batch's closure
  documents.
- **Metadata lines:** JMdict ids that the shorter text no longer names were removed; no id was added. 卑 dropped 1434180, 2080200,
  1178940, 1151260 and 1242130; 汰 dropped 1415960; 沢 dropped 1390020, 2843433 and 1224010; 胡 dropped 1203620, 2740960, 1267590 and
  1610940; 鼓 dropped 1253760, 1609000 and 1390750. 沙's Metadata line is unchanged. The character-source links (Digital Daijisen,
  Kanjipedia, Joyo PDF page) are unchanged on every card.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. Five cards got shorter; 沙 kept 61 lines.
- `diffs\fix.patch` is the exact patch from `97c49eb2` to `25609582`; `diffs\changed-lines.txt` lists the changed lines per file.

## Size of the learner text

| Card | Bytes before → after | Words in `## Notes` before → after |
| --- | --- | --- |
| 卑 | 7,070 → 4,374 | 525 → 248 |
| 汰 | 6,789 → 5,027 | 405 → 252 |
| 沙 | 6,215 → 4,817 | 357 → 281 |
| 沢 | 7,007 → 4,762 | 490 → 266 |
| 胡 | 6,597 → 4,671 | 456 → 266 |
| 鼓 | 5,051 → 3,612 | 331 → 198 |

Both columns were measured on the committed files at `97c49eb2` and `25609582` (bytes of the whole file; whitespace-separated words between
`## Notes` and the next `## ` heading).

## Changed lines

| File | Changed lines (revised numbering) | Change |
| --- | --- | --- |
| 卑 | 14, 23, 42, 45-52, 56 | 14: 底 removed. 23: Meaning paragraph in plain English (low rank or status, low character, looking down on others, a humble word for oneself, Kanjipedia's near-or-familiar sense with 卑近 ひきん “common; simple”, KANJIDIC2's list, and the two JMdict senses of 卑怯). 42: the Joyo line names the three kun readings without their example words and no longer mentions Kanjipedia's 高 mark; ひくい gets the gloss “(low)”. 45: "These eleven cards" (was "twelve"); 46 is the blank line after it, inside the same patch hunk. 47-52: six group bullets replace the twelve per-card bullets (old 47-58); the 底 bullet is gone. 56: Metadata ids trimmed. |
| 汰 | 23, 44, 49-54, 56, 60 | 23: Meaning paragraph in plain English, adding 淘汰 とうた (weeding out; culling) and Kanjipedia's muddy, unclean-conduct and luxury-or-boasting senses. 44: 沙汰 さた is "first glossed “affair; state; incident; issue; matter”" (its entry id is now only on the Metadata line). 49-54: six group bullets replace eight bullets (old 49-56). 56: the 汰/沙 sibling sentence now says that Kanjipedia gives both characters "the sense よなげる, sifting by washing in water" (it used to say "gives よなげる for both characters"). 60: Metadata ids trimmed. |
| 沙 | 14, 23, 44, 47, 49, 51-56 | 14: 漠 removed. 23: Meaning paragraph in plain English (sand, sandy ground at the water's edge, sifting by washing as in 沙汰). 44: みぎわ gets the gloss “(the water's edge)”, and the entry id after 沙汰 is now only on the Metadata line. 47 (new): "JMdict lists 沙漠 as a rarely used spelling of 砂漠 さばく, “desert”, and Digital Daijisen gives 沙漠 as an example of 沙 meaning sand. Sand is a material, while a desert is a region; compare the [漠](漠.md) card (“desert; vague”)." 49: "These nine cards" (was "ten"). 51-56: six group bullets replace seven bullets (old 50-56); the 漠 bullet is gone. |
| 沢 | 23, 43, 48-52, 56 | 23: Meaning paragraph in plain English (marsh or wetland, mountain stream or valley, moisture and blessing, richness and abundance, gloss or brilliance; 贅沢 "first means “luxury; extravagance”"). 43: the clause on Digital Daijisen's ［音］/［訓］ labels is dropped. 48-52: five group bullets replace nine bullets (old 48-56). 56: Metadata ids trimmed. |
| 胡 | 23, 49-54, 58 | 23: Meaning paragraph in plain English (peoples to the north and west of China, goods produced abroad as in 胡椒 and 胡麻, careless, doubtful or suspicious as in 胡散臭い, KANJIDIC2's list, Kanjipedia's long-life and question-word senses). 49-54: six group bullets replace nine bullets (old 49-57). 58: Metadata ids trimmed. |
| 鼓 | 23, 40, 45-48, 52 | 23: Meaning paragraph in plain English (a drum such as the hourglass-shaped tsuzumi; beating or striking; rousing or encouraging; KANJIDIC2's list; 太鼓 and 鼓舞). 40: 小鼓 こつづみ is “small hand drum” (the しょうこ reading and the entry id are gone from this line). 45-48: four group bullets replace six bullets (old 45-50). 52: Metadata ids trimmed. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 2 warnings (the word articles 卑怯 and 太鼓, whose Dictionary line cites no JMdict entry id); identical to
  the freeze. `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: rebuilding `manifest.json` leaves it unchanged
  and the tree clean. `budget.txt` and `vocabulary.txt`: informational; the retained content is 11,825 bytes smaller than at the
  freeze.
- `linkplan.txt`: 6 changed word files, 8 expected and 8 added link pairs, 1 declared remark edit, 0 problems; identical to the
  freeze.
- `kanji-remarks.txt`: 6 new cards, 0 modified existing cards, 0 problems; apart from the command line, identical to the freeze.
- `quiz-safety.txt`: 0 errors, 0 warnings; identical to the freeze. Every batch card's meaning options are still its three curated
  titles. Neither 底 nor 漠 is a curated distractor of a batch card, and neither 卑 nor 沙 is a curated distractor of any card, so the
  two removed exclusions matter only in reduced pools that fall back to other cards.
- `reading-exposure.txt`: apart from the command line, identical to the freeze: 0 production hits, 0 padded-session hits, 1 latent
  collision (沢's name reading さ), 0 one-holder hits and 0 more for KANJIDIC2 name-only readings. No reading list changed.
- `reading-options.txt`: apart from the command line, identical to the freeze; 0 problems.
- `evidence\meta-scan.txt` (output of `meta_scan.py` on the six cards at `25609582`): 1 whole-run gap (人名用漢字 on 胡:42, a quoted
  Digital Daijisen label), down from 4 at the freeze (湿地, 人名用漢字, 老人 and 励ます; the other three were in rewritten text), and 8
  part-of-run matches, down from 75.
- The Android JVM tests that read the real content were not run, as at the freeze (no JDK on this machine).

## Process notes

- `25609582` is the single fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `97c49eb2`.
- After the main rewrite, every quoted English gloss on the six cards was re-checked against the cited JMdict entries, KANJIDIC2
  and the quoted card titles, and wording that the sources do not support was changed in the same commit:
  - a partial gloss is introduced with "can mean" or "includes" (淘汰, 抜く, 抽出, 沢山, 卑しむ), and a gloss given as a definition is
    the full JMdict sense (胡散臭い, 異民族, 乱り sense 1, 下品, 軽んじる);
  - "rarer" was removed wherever it described a Kanjipedia sense, because the order of senses in Kanjipedia does not establish
    frequency;
  - the 沢 wetland bullet compares 沼沢 with 泥沼 instead of implying that 泥沼 contains 沢.
- The checks in `checks\` were run on the committed revision `25609582`.
